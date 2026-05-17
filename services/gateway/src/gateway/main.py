from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from gateway.config import settings
from gateway.demo import demo_dashboard_metrics, load_demo_impact_agent, load_demo_rag, public_data_dir
from intelligence.agents.impact import ImpactAnalysisAgent
from intelligence.agents.base import AgentContext
from intelligence.rag.pipeline import RAGQuery, RAGResponse
from intelligence.validators.trace import CitationRequiredValidator


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag = load_demo_rag()
    app.state.impact_agent = load_demo_impact_agent()
    app.state.public_data_loaded = public_data_dir().is_dir()
    yield


app = FastAPI(
    title=settings.app_name,
    version="0.1.0",
    description="Traceability-first certification intelligence API",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "service": "gateway"}


@app.get("/api/v1/documents")
async def list_documents() -> dict[str, Any]:
    """List public demo certification documents available for ingestion/testing."""
    root = public_data_dir()
    if not root.is_dir():
        return {"documents": [], "note": "data/public not found"}
    docs = [
        {
            "path": p.relative_to(root).as_posix(),
            "source_uri": f"data/public/{p.relative_to(root).as_posix()}",
        }
        for p in sorted(root.rglob("*.md"))
        if p.name.lower() != "readme.md"
        and "graph" not in p.parts
    ]
    return {
        "program_id": "dap-100",
        "count": len(docs),
        "documents": docs,
        "graph": "data/public/graph/dap-100-graph.json",
    }


class AskRequest(BaseModel):
    question: str
    program_id: str = "dap-100"
    subsystem_id: str | None = None


@app.post("/api/v1/ask", response_model=RAGResponse)
async def ask(req: AskRequest) -> RAGResponse:
    """Natural-language query grounded in certification evidence."""
    rag = app.state.rag
    return await rag.query(
        RAGQuery(
            question=req.question,
            program_id=req.program_id,
            subsystem_id=req.subsystem_id,
        )
    )


class ImpactRequest(BaseModel):
    entity_id: str
    program_id: str = "dap-100"
    change_description: str = Field(..., min_length=3)


@app.post("/api/v1/impact/analyze")
async def analyze_impact(req: ImpactRequest) -> dict[str, Any]:
    """Run impact analysis agent for a change to a certification artifact."""
    agent: ImpactAnalysisAgent = app.state.impact_agent
    result = await agent.run(
        AgentContext(
            program_id=req.program_id,
            user_id="api",
            entity_ids=[req.entity_id],
            parameters={"change_description": req.change_description},
        )
    )
    return result.model_dump()


@app.get("/api/v1/programs/{program_id}/dashboard")
async def program_dashboard(program_id: str) -> dict[str, Any]:
    """Certification progress snapshot from demo public data."""
    if program_id != "dap-100":
        return {
            "program_id": program_id,
            "metrics": demo_dashboard_metrics(),
            "note": "Only dap-100 has seeded demo data; metrics shown are illustrative.",
        }
    return {
        "program_id": program_id,
        "metrics": demo_dashboard_metrics(),
        "data_source": "data/public (synthetic demo documents)",
    }
