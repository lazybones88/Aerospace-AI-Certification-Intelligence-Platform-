from pathlib import Path

from graph_engine.memory_store import InMemoryGraphStore
from intelligence.agents.impact import ImpactAnalysisAgent
from intelligence.rag.grounded_answer import build_grounded_answer
from intelligence.rag.local_retriever import LocalDocumentRetriever
from intelligence.rag.pipeline import RAGPipeline
from intelligence.validators.trace import CitationRequiredValidator


def repo_root() -> Path:
    """Resolve monorepo root from services/gateway/src/gateway/demo.py."""
    return Path(__file__).resolve().parents[4]


def public_data_dir() -> Path:
    return repo_root() / "data" / "public"


def load_demo_rag() -> RAGPipeline:
    retriever = LocalDocumentRetriever.from_directory(public_data_dir(), program_id="dap-100")

    class GroundedPipeline(RAGPipeline):
        async def query(self, q):  # type: ignore[override]
            response = await super().query(q)
            if response.evidence and response.confidence.value != "insufficient_evidence":
                chunks = await retriever.retrieve(q)
                response.answer = build_grounded_answer(q.question, chunks)
            return response

    return GroundedPipeline(
        retriever=retriever,
        validators=[CitationRequiredValidator()],
    )


def load_demo_impact_agent() -> ImpactAnalysisAgent:
    graph_path = public_data_dir() / "graph" / "dap-100-graph.json"
    store = InMemoryGraphStore(graph_path)

    class MemoryImpactAnalyzer:
        async def analyze(self, entity_id: str, change_description: str):
            return store.impact_from(entity_id, change_description)

    return ImpactAnalysisAgent(impact_analyzer=MemoryImpactAnalyzer())


def demo_dashboard_metrics() -> dict:
    store = InMemoryGraphStore(public_data_dir() / "graph" / "dap-100-graph.json")
    requirements = [n for n in store._data.get("nodes", []) if n.get("entity_type") == "requirement"]
    tests = [n for n in store._data.get("nodes", []) if n.get("entity_type") == "test_case"]
    traced = 2  # demo: 2 of 3 reqs have tests in graph; 1 gap (1042 on 2.4.1)
    total_req = max(len(requirements), 1)
    return {
        "requirements_total": total_req,
        "requirements_traced_pct": round(100 * traced / total_req, 1),
        "open_gaps": 3,
        "audit_readiness_score": 62.0,
        "unresolved_risks": 3,
        "demo_program": store.program_id,
    }
