// Impact propagation from a changed entity (parameter: $entity_id, $max_depth)
// Returns impacted certification objectives, hazards, and approvals

MATCH (source:CertificationEntity {id: $entity_id})
CALL apoc.path.subgraphAll(source, {
  relationshipFilter: "AFFECTS>|IMPLEMENTS<|VERIFIES<|SATISFIES<|TRACES_TO>",
  maxLevel: $max_depth
}) YIELD nodes, relationships
UNWIND nodes AS n
WITH DISTINCT n
WHERE n:CertificationObjective OR n:Hazard OR n:Approval OR n:Requirement OR n:TestCase
RETURN n.id AS entity_id,
       labels(n)[0] AS label,
       n.title AS title,
       n.entity_type AS entity_type
