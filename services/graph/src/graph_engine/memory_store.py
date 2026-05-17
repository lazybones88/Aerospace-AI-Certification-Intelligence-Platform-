import json
from pathlib import Path
from typing import Any

from domain.enums import EntityType, RelationshipType
from domain.evidence import ImpactItem, ImpactReport
from datetime import datetime, timezone


class InMemoryGraphStore:
    """JSON-backed graph for demo and environments without Neo4j."""

    def __init__(self, graph_path: Path) -> None:
        self._path = graph_path
        self._data: dict[str, Any] = {"nodes": [], "edges": []}
        if graph_path.is_file():
            self._data = json.loads(graph_path.read_text(encoding="utf-8"))

    @property
    def program_id(self) -> str:
        return self._data.get("program_id", "dap-100")

    def get_node(self, node_id: str) -> dict | None:
        for n in self._data.get("nodes", []):
            if n["id"] == node_id:
                return n
        return None

    def impact_from(self, entity_id: str, change_description: str, max_depth: int = 5) -> ImpactReport:
        edges = self._data.get("edges", [])
        nodes = {n["id"]: n for n in self._data.get("nodes", [])}
        visited: set[str] = set()
        items: list[ImpactItem] = []
        objectives: list[str] = []

        frontier = [entity_id]
        depth_map = {entity_id: 0}

        while frontier:
            current = frontier.pop(0)
            depth = depth_map[current]
            if current in visited or depth > max_depth:
                continue
            visited.add(current)

            for edge in edges:
                if edge["from"] != current:
                    continue
                target = edge["to"]
                rel = RelationshipType(edge["type"])
                node = nodes.get(target)
                if not node or target == entity_id:
                    continue
                entity_type = EntityType(node.get("entity_type", "document"))
                items.append(
                    ImpactItem(
                        entity_id=target,
                        entity_type=entity_type,
                        title=node.get("title", target),
                        relationship_path=[rel],
                        depth=depth + 1,
                    )
                )
                if entity_type == EntityType.CERTIFICATION_OBJECTIVE:
                    objectives.append(target)
                if target not in visited and depth + 1 <= max_depth:
                    depth_map[target] = depth + 1
                    frontier.append(target)

        return ImpactReport(
            source_entity_id=entity_id,
            change_description=change_description,
            impacted_items=items,
            impacted_objectives=objectives,
            generated_at=datetime.now(timezone.utc),
        )
