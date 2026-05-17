from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

from domain.evidence import ImpactReport
from gateway.config import settings
from intelligence.agents.impact import ImpactAnalysisAgent
from intelligence.agents.base import AgentContext
from intelligence.rag.pipeline import RAGPipeline, RAGQuery, RAGResponse
from intelligence.validators.trace import CitationRequiredValidator


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.rag = RAGPipeline(validators=[CitationRequiredValidator()])
    app.state.impact_agent = ImpactAnalysisAgent()
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


class AskRequest(BaseModel):
    question: str
    program_id: str
    subsystem_id: str | None = None


@app.post("/api/v1/ask", response_model=RAGResponse)
async def ask(req: AskRequest) -> RAGResponse:
    """Natural-language query grounded in certification evidence."""
    rag: RAGPipeline = app.state.rag
    return await rag.query(
        RAGQuery(
            question=req.question,
            program_id=req.program_id,
            subsystem_id=req.subsystem_id,
        )
    )


class ImpactRequest(BaseModel):
    entity_id: str
    program_id: str
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
    """Certification progress snapshot (Phase 1 placeholder metrics)."""
    return {
        "program_id": program_id,
        "metrics": {
            "requirements_total": 0,
            "requirements_traced_pct": 0.0,
            "open_gaps": 0,
            "audit_readiness_score": 0.0,
            "unresolved_risks": 0,
        },
        "note": "Connect graph and ingestion pipelines to populate live metrics.",
    }
