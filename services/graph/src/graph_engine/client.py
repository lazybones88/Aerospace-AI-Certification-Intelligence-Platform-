from typing import Any

from neo4j import AsyncGraphDatabase, AsyncDriver

from graph_engine.schema import GRAPH_CONSTRAINTS, GRAPH_INDEXES


class GraphClient:
    """Async Neo4j client for certification graph operations."""

    def __init__(self, uri: str, user: str, password: str, database: str = "neo4j") -> None:
        self._uri = uri
        self._auth = (user, password)
        self._database = database
        self._driver: AsyncDriver | None = None

    async def connect(self) -> None:
        self._driver = AsyncGraphDatabase.driver(self._uri, auth=self._auth)

    async def close(self) -> None:
        if self._driver:
            await self._driver.close()

    async def init_schema(self) -> None:
        async with self.session() as session:
            for stmt in GRAPH_CONSTRAINTS + GRAPH_INDEXES:
                await session.run(stmt)

    def session(self):
        if not self._driver:
            raise RuntimeError("GraphClient not connected")
        return self._driver.session(database=self._database)

    async def upsert_entity(self, label: str, properties: dict[str, Any]) -> None:
        entity_id = properties["id"]
        async with self.session() as session:
            await session.run(
                f"""
                MERGE (n:CertificationEntity:{label} {{id: $id}})
                SET n += $props, n.updated_at = datetime()
                """,
                id=entity_id,
                props=properties,
            )

    async def create_relationship(
        self,
        from_id: str,
        to_id: str,
        rel_type: str,
        properties: dict[str, Any] | None = None,
    ) -> None:
        props = properties or {}
        async with self.session() as session:
            await session.run(
                f"""
                MATCH (a:CertificationEntity {{id: $from_id}})
                MATCH (b:CertificationEntity {{id: $to_id}})
                MERGE (a)-[r:{rel_type}]->(b)
                SET r += $props
                """,
                from_id=from_id,
                to_id=to_id,
                props=props,
            )

    async def get_neighbors(self, entity_id: str, rel_types: list[str] | None = None) -> list[dict]:
        filter_clause = ""
        if rel_types:
            types = "|".join(rel_types)
            filter_clause = f"WHERE type(r) IN [{', '.join(repr(t) for t in rel_types)}]"
        async with self.session() as session:
            result = await session.run(
                f"""
                MATCH (n:CertificationEntity {{id: $entity_id}})-[r]-(m)
                {filter_clause}
                RETURN m.id AS id, labels(m) AS labels, type(r) AS relationship, m.title AS title
                """,
                entity_id=entity_id,
            )
            return [record.data() async for record in result]
