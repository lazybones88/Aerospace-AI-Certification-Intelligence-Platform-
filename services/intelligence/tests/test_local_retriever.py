import asyncio
from pathlib import Path

import pytest

from intelligence.rag.local_retriever import LocalDocumentRetriever
from intelligence.rag.pipeline import RAGPipeline, RAGQuery
from intelligence.rag.grounded_answer import build_grounded_answer
from intelligence.validators.trace import CitationRequiredValidator


REPO_ROOT = Path(__file__).resolve().parents[3]
PUBLIC_DATA = REPO_ROOT / "data" / "public"


@pytest.fixture
def retriever():
    if not PUBLIC_DATA.is_dir():
        pytest.skip("data/public not present")
    return LocalDocumentRetriever.from_directory(PUBLIC_DATA, program_id="dap-100")


@pytest.mark.asyncio
async def test_retriever_finds_flight_test_risk(retriever):
    chunks = await retriever.retrieve(
        RAGQuery(
            question="Which certification risks could delay flight testing?",
            program_id="dap-100",
        )
    )
    assert len(chunks) >= 1
    combined = " ".join(c["text"] for c in chunks)
    assert "RISK-CERT" in combined or "flight test" in combined.lower()


@pytest.mark.asyncio
async def test_rag_pipeline_with_demo_data(retriever):
    rag = RAGPipeline(retriever=retriever, validators=[CitationRequiredValidator()])
    response = await rag.query(
        RAGQuery(
            question="Which certification risks could delay flight testing?",
            program_id="dap-100",
        )
    )
    assert response.confidence.value != "insufficient_evidence"
    assert len(response.evidence) >= 1


def test_grounded_answer_flight_test(retriever):
    chunks = asyncio.run(
        retriever.retrieve(
            RAGQuery(question="flight testing delay risks", program_id="dap-100")
        )
    )
    answer = build_grounded_answer("Which risks could delay flight testing?", chunks)
    assert "flight" in answer.lower() or "RISK" in answer
