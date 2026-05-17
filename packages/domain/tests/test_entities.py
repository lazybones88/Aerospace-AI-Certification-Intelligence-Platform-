from datetime import datetime, timezone

from domain import (
    ConfidenceTier,
    EvidenceRef,
    ExportControl,
    Provenance,
    Requirement,
    SourceSystem,
)
from domain.enums import EntityType


def test_requirement_with_provenance():
    now = datetime.now(timezone.utc)
    prov = Provenance(
        source_system=SourceSystem.POLARION,
        source_uri="PRJ/REQ-1042",
        ingested_at=now,
        ingest_job_id="job-1",
        content_hash="sha256:abc",
        export_control=ExportControl.EAR99,
    )
    req = Requirement(
        id="req-1042",
        program_id="prog-fc",
        provenance=prov,
        created_at=now,
        updated_at=now,
        entity_type=EntityType.REQUIREMENT,
        title="Flight control latency bound",
        requirement_id="REQ-1042",
    )
    assert req.provenance.source_system == SourceSystem.POLARION
    assert req.requirement_id == "REQ-1042"


def test_evidence_ref_defaults():
    ref = EvidenceRef(ref_type="graph_node", ref_id="node-1")
    assert ref.confidence == ConfidenceTier.AUTHORITATIVE
