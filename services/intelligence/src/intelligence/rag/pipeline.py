from pydantic import BaseModel, Field

from domain.enums import ConfidenceTier
from domain.evidence import EvidenceRef, ValidatorResult


class RAGQuery(BaseModel):
    question: str
    program_id: str
    subsystem_id: str | None = None
    max_chunks: int = 8
    require_citations: bool = True


class RAGResponse(BaseModel):
    answer: str
    confidence: ConfidenceTier
    evidence: list[EvidenceRef] = Field(default_factory=list)
    validator_results: list[ValidatorResult] = Field(default_factory=list)


class RAGPipeline:
    """
    Retrieval-augmented generation with mandatory grounding.
    Phase 1: stub retriever; wire vector + graph context in deployment.
    """

    def __init__(self, retriever=None, llm=None, validators: list | None = None) -> None:
        self._retriever = retriever
        self._llm = llm
        self._validators = validators or []

    async def query(self, q: RAGQuery) -> RAGResponse:
        chunks = []
        if self._retriever:
            chunks = await self._retriever.retrieve(q)

        if not chunks and q.require_citations:
            return RAGResponse(
                answer=(
                    "Insufficient authoritative evidence was retrieved to answer this question. "
                    "Please refine the query or ingest additional source material."
                ),
                confidence=ConfidenceTier.INSUFFICIENT_EVIDENCE,
                evidence=[],
            )

        evidence = [
            EvidenceRef(
                ref_type="document_chunk",
                ref_id=c.get("chunk_id", "unknown"),
                excerpt=c.get("text", "")[:500],
                source_uri=c.get("source_uri"),
            )
            for c in chunks
        ]

        if self._llm:
            answer = await self._llm.generate(q.question, context=chunks)
        else:
            answer = self._stub_answer(q.question, evidence)

        validator_results = []
        for v in self._validators:
            validator_results.append(await v.validate(answer=answer, evidence=evidence, query=q))

        confidence = ConfidenceTier.AUTHORITATIVE if evidence else ConfidenceTier.INFERRED
        if any(not r.passed for r in validator_results):
            confidence = ConfidenceTier.INFERRED

        return RAGResponse(
            answer=answer,
            confidence=confidence,
            evidence=evidence,
            validator_results=validator_results,
        )

    @staticmethod
    def _stub_answer(question: str, evidence: list[EvidenceRef]) -> str:
        refs = ", ".join(e.ref_id for e in evidence[:3]) or "none"
        return (
            f"[Grounded response stub] Based on {len(evidence)} evidence chunk(s) ({refs}): "
            f"analysis for: {question}"
        )
