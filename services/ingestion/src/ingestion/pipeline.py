from dataclasses import dataclass
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Callable, Awaitable

from domain.entities import CertificationEntity
from domain.provenance import Provenance
from domain.enums import SourceSystem
from ingestion.connectors.base import RawPayload


class PipelineStage(str, Enum):
    ACQUIRE = "acquire"
    CLASSIFY = "classify"
    EXTRACT = "extract"
    CHUNK = "chunk"
    ENRICH = "enrich"
    NORMALIZE = "normalize"
    PUBLISH = "publish"


StageHandler = Callable[[dict[str, Any]], Awaitable[dict[str, Any]]]


@dataclass
class IngestionJob:
    job_id: str
    connector_id: str
    source_system: SourceSystem
    started_at: datetime
    status: str = "running"
    stages_completed: list[PipelineStage] | None = None

    def __post_init__(self) -> None:
        if self.stages_completed is None:
            self.stages_completed = []


class IngestionPipeline:
    """Composable async pipeline for ingest → normalize → publish."""

    def __init__(self) -> None:
        self._handlers: dict[PipelineStage, StageHandler] = {}

    def register(self, stage: PipelineStage, handler: StageHandler) -> None:
        self._handlers[stage] = handler

    async def run(self, job: IngestionJob, payload: RawPayload) -> list[CertificationEntity]:
        context: dict[str, Any] = {
            "job": job,
            "payload": payload,
            "entities": [],
        }
        for stage in PipelineStage:
            handler = self._handlers.get(stage)
            if handler:
                context = await handler(context)
                job.stages_completed.append(stage)
        return context.get("entities", [])

    @staticmethod
    def build_provenance(job: IngestionJob, payload: RawPayload) -> Provenance:
        return Provenance(
            source_system=job.source_system,
            source_uri=payload.source_uri,
            ingested_at=datetime.now(timezone.utc),
            ingest_job_id=job.job_id,
            content_hash=payload.content_hash,
            raw_storage_uri=payload.bytes_ref,
            metadata=payload.metadata,
        )
