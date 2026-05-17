from datetime import datetime
from typing import Literal

from pydantic import Field

from domain.enums import DalLevel, EntityType, StandardFramework
from domain.provenance import TraceableRecord


class CertificationEntity(TraceableRecord):
    """Base certification entity stored in graph and search indices."""

    entity_type: EntityType
    title: str
    description: str | None = None
    subsystem_id: str | None = None
    tags: list[str] = Field(default_factory=list)


class Subsystem(CertificationEntity):
    entity_type: Literal[EntityType.SUBSYSTEM] = EntityType.SUBSYSTEM
    dal: DalLevel | None = None
    part_number: str | None = None


class Requirement(CertificationEntity):
    entity_type: Literal[EntityType.REQUIREMENT] = EntityType.REQUIREMENT
    requirement_id: str  # e.g. SYS-REQ-1042
    priority: str | None = None
    status: str = "draft"  # draft | approved | obsolete


class SoftwareBuild(CertificationEntity):
    entity_type: Literal[EntityType.SOFTWARE_BUILD] = EntityType.SOFTWARE_BUILD
    version: str
    baseline_id: str | None = None
    repository_uri: str | None = None


class TestCase(CertificationEntity):
    entity_type: Literal[EntityType.TEST_CASE] = EntityType.TEST_CASE
    procedure_id: str | None = None


class TestResult(CertificationEntity):
    entity_type: Literal[EntityType.TEST_RESULT] = EntityType.TEST_RESULT
    test_case_id: str
    outcome: str  # pass | fail | blocked | not_run
    executed_at: datetime | None = None


class Hazard(CertificationEntity):
    entity_type: Literal[EntityType.HAZARD] = EntityType.HAZARD
    severity: str | None = None
    classification: str | None = None


class Mitigation(CertificationEntity):
    entity_type: Literal[EntityType.MITIGATION] = EntityType.MITIGATION
    hazard_id: str


class CertificationObjective(CertificationEntity):
    entity_type: Literal[EntityType.CERTIFICATION_OBJECTIVE] = (
        EntityType.CERTIFICATION_OBJECTIVE
    )
    framework: StandardFramework
    objective_code: str  # e.g. DO-178C Table A-7 objective 6
    dal_scope: list[DalLevel] = Field(default_factory=list)


class Approval(CertificationEntity):
    entity_type: Literal[EntityType.APPROVAL] = EntityType.APPROVAL
    approver_role: str
    approved_entity_id: str
    signed_at: datetime


class Supplier(CertificationEntity):
    entity_type: Literal[EntityType.SUPPLIER] = EntityType.SUPPLIER
    cage_code: str | None = None


class DocumentArtifact(CertificationEntity):
    entity_type: Literal[EntityType.DOCUMENT] = EntityType.DOCUMENT
    mime_type: str
    page_count: int | None = None
    chunk_ids: list[str] = Field(default_factory=list)
