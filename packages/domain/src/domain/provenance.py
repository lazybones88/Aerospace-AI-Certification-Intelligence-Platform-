from datetime import datetime
from typing import Any

from pydantic import BaseModel, Field

from domain.enums import ExportControl, SourceSystem


class Provenance(BaseModel):
    """Immutable ingest provenance attached to every certification artifact."""

    source_system: SourceSystem
    source_uri: str
    ingested_at: datetime
    ingest_job_id: str
    content_hash: str
    classification: list[str] = Field(default_factory=list)
    export_control: ExportControl = ExportControl.UNKNOWN
    raw_storage_uri: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class TraceableRecord(BaseModel):
    """Base mixin for all persisted certification records."""

    id: str
    program_id: str
    provenance: Provenance
    created_at: datetime
    updated_at: datetime
    version: int = 1
