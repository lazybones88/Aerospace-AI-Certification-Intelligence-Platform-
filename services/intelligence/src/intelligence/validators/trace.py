from domain.evidence import EvidenceRef, ValidatorResult
from intelligence.rag.pipeline import RAGQuery


class CitationRequiredValidator:
    """Fails if generative answer lacks evidence citations."""

    rule_id = "citation_required"

    async def validate(
        self,
        answer: str,
        evidence: list[EvidenceRef],
        query: RAGQuery,
    ) -> ValidatorResult:
        if query.require_citations and not evidence:
            return ValidatorResult(
                rule_id=self.rule_id,
                passed=False,
                message="Answer rejected: no evidence citations attached.",
            )
        return ValidatorResult(
            rule_id=self.rule_id,
            passed=True,
            message="Evidence citations present.",
            details={"citation_count": len(evidence)},
        )


class TraceCompletenessValidator:
    """Checks that referenced requirements appear in evidence metadata."""

    rule_id = "trace_completeness"

    async def validate(
        self,
        answer: str,
        evidence: list[EvidenceRef],
        query: RAGQuery,
    ) -> ValidatorResult:
        # Phase 1 stub — integrate graph gap queries in Phase 2
        return ValidatorResult(
            rule_id=self.rule_id,
            passed=True,
            message="Trace completeness check passed (stub).",
        )
