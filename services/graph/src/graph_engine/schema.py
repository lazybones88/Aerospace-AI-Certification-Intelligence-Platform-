"""Neo4j schema: constraints and indexes for certification graph."""

GRAPH_CONSTRAINTS = [
    "CREATE CONSTRAINT entity_id IF NOT EXISTS FOR (n:CertificationEntity) REQUIRE n.id IS UNIQUE",
    "CREATE CONSTRAINT program_id IF NOT EXISTS FOR (p:Program) REQUIRE p.id IS UNIQUE",
    "CREATE CONSTRAINT requirement_id IF NOT EXISTS FOR (r:Requirement) REQUIRE r.requirement_id IS UNIQUE",
]

GRAPH_INDEXES = [
    "CREATE INDEX entity_type IF NOT EXISTS FOR (n:CertificationEntity) ON (n.entity_type)",
    "CREATE INDEX program_scope IF NOT EXISTS FOR (n:CertificationEntity) ON (n.program_id)",
    "CREATE INDEX subsystem_scope IF NOT EXISTS FOR (n:CertificationEntity) ON (n.subsystem_id)",
]

# Relationship types used in Cypher templates
RELATIONSHIP_TYPES = [
    "TRACES_TO",
    "IMPLEMENTS",
    "VERIFIES",
    "SATISFIES",
    "MITIGATES",
    "AFFECTS",
    "DERIVES_FROM",
    "APPROVES",
    "REFERENCES",
]
