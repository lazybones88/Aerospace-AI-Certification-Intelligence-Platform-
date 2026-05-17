from pydantic import BaseModel, Field

from domain.enums import DalLevel, StandardFramework


class RegulatoryObligation(BaseModel):
    """Machine-readable clause from an aerospace standard."""

    id: str
    framework: StandardFramework
    clause_path: str  # e.g. DO-178C / Section 6 / Table A-7
    title: str
    text: str
    dal_scope: list[DalLevel] = Field(default_factory=list)
    related_frameworks: list[str] = Field(default_factory=list)


class ObjectiveMapping(BaseModel):
    """Links a certification objective to expected evidence types."""

    objective_id: str
    obligation_id: str
    evidence_types: list[str] = Field(default_factory=list)
    activity_types: list[str] = Field(default_factory=list)


# Phase 1 seed obligations — expand via regulatory ingestion pipeline
SEED_OBLIGATIONS: list[RegulatoryObligation] = [
    RegulatoryObligation(
        id="do178c-a7-obj6",
        framework=StandardFramework.DO_178C,
        clause_path="DO-178C / Table A-7 / Objective 6",
        title="Verification of outputs of software verification process",
        text="Verify that outputs of software verification process comply with software verification standards.",
        dal_scope=[DalLevel.A, DalLevel.B, DalLevel.C],
    ),
    RegulatoryObligation(
        id="arp4754a-5-2",
        framework=StandardFramework.ARP4754A,
        clause_path="ARP4754A / Section 5.2",
        title="Safety assessment process",
        text="Perform safety assessment activities consistent with development assurance level.",
        dal_scope=[DalLevel.A, DalLevel.B, DalLevel.C, DalLevel.D],
        related_frameworks=["DO-178C", "DO-254"],
    ),
]
