from datetime import datetime, timezone

from domain.enums import ConfidenceTier
from domain.evidence import AgentResult, EvidenceRef
from intelligence.agents.base import AgentContext, BaseAgent


class ImpactAnalysisAgent(BaseAgent):
    """Identifies certification artifacts affected by a proposed change."""

    agent_id = "impact-analysis"
    task_type = "impact_analysis"

    def __init__(self, impact_analyzer=None) -> None:
        self._analyzer = impact_analyzer

    async def run(self, context: AgentContext) -> AgentResult:
        entity_id = context.entity_ids[0] if context.entity_ids else ""
        change_desc = context.parameters.get("change_description", "Unspecified change")

        evidence: list[EvidenceRef] = []
        summary = f"Impact analysis for entity {entity_id}: no graph connection configured."

        if self._analyzer and entity_id:
            report = await self._analyzer.analyze(entity_id, change_desc)
            summary = (
                f"Change '{change_desc}' impacts {len(report.impacted_items)} artifact(s) "
                f"and {len(report.impacted_objectives)} certification objective(s)."
            )
            evidence = [
                EvidenceRef(ref_type="graph_node", ref_id=item.entity_id, excerpt=item.title)
                for item in report.impacted_items[:20]
            ]

        return AgentResult(
            agent_id=self.agent_id,
            task_type=self.task_type,
            summary=summary,
            confidence=ConfidenceTier.AUTHORITATIVE if evidence else ConfidenceTier.INFERRED,
            evidence=evidence,
            recommended_actions=[
                "Review impacted certification objectives with certification lead.",
                "Re-run affected test procedures before approval.",
            ],
            completed_at=datetime.now(timezone.utc),
        )
