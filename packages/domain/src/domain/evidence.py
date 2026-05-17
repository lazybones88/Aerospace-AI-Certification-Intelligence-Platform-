from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from domain.enums import ConfidenceTier, EntityType, RelationshipType


class EvidenceRef(BaseModel):
    """Pointer to authoritative source material supporting an AI claim."""

    ref_type: str  # graph_node | document_chunk | regulatory_clause
    ref_id: str
    excerpt: str | None = None
    source_uri: str | None = None
    page: int | None = None
    confidence: ConfidenceTier = ConfidenceTier.AUTHORITATIVE


class ValidatorResult(BaseModel):
    rule_id: str
    passed: bool
    message: str
    details: dict[str, Any] = Field(default_factory=dict)


class AgentResult(BaseModel):
    """Structured output from a certification agent."""

    agent_id: str
    task_type: str
    summary: str
    confidence: ConfidenceTier
    evidence: list[EvidenceRef] = Field(default_factory=list)
    validator_results: list[ValidatorResult] = Field(default_factory=list)
    recommended_actions: list[str] = Field(default_factory=list)
    completed_at: datetime


class ImpactItem(BaseModel):
    entity_id: str
    entity_type: EntityType
    title: str
    relationship_path: list[RelationshipType]
    depth: int
    is_stale_approval: bool = False


class ImpactReport(BaseModel):
    """Result of graph impact propagation from a change event."""

    source_entity_id: str
    change_description: str
    impacted_items: list[ImpactItem] = Field(default_factory=list)
    impacted_objectives: list[str] = Field(default_factory=list)
    generated_at: datetime
