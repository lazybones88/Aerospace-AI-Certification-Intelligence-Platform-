from datetime import datetime, timezone

from domain.evidence import ImpactItem, ImpactReport
from domain.enums import EntityType, RelationshipType
from graph_engine.client import GraphClient


class ImpactAnalyzer:
    """Propagates change impact through the certification knowledge graph."""

    def __init__(self, client: GraphClient, max_depth: int = 5) -> None:
        self._client = client
        self._max_depth = max_depth

    async def analyze(self, entity_id: str, change_description: str) -> ImpactReport:
        neighbors = await self._client.get_neighbors(
            entity_id,
            rel_types=[
                RelationshipType.AFFECTS.value,
                RelationshipType.IMPLEMENTS.value,
                RelationshipType.VERIFIES.value,
                RelationshipType.SATISFIES.value,
                RelationshipType.TRACES_TO.value,
            ],
        )
        items: list[ImpactItem] = []
        objectives: list[str] = []
        for n in neighbors:
            label = (n.get("labels") or ["Unknown"])[0]
            entity_type = self._label_to_entity_type(label)
            item = ImpactItem(
                entity_id=n["id"],
                entity_type=entity_type,
                title=n.get("title") or n["id"],
                relationship_path=[RelationshipType(n["relationship"])],
                depth=1,
            )
            items.append(item)
            if entity_type == EntityType.CERTIFICATION_OBJECTIVE:
                objectives.append(n["id"])
        return ImpactReport(
            source_entity_id=entity_id,
            change_description=change_description,
            impacted_items=items,
            impacted_objectives=objectives,
            generated_at=datetime.now(timezone.utc),
        )

    @staticmethod
    def _label_to_entity_type(label: str) -> EntityType:
        mapping = {
            "Requirement": EntityType.REQUIREMENT,
            "TestCase": EntityType.TEST_CASE,
            "Hazard": EntityType.HAZARD,
            "CertificationObjective": EntityType.CERTIFICATION_OBJECTIVE,
            "Approval": EntityType.APPROVAL,
        }
        return mapping.get(label, EntityType.DOCUMENT)
