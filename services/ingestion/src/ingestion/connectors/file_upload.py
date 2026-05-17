from datetime import datetime, timezone
from pathlib import Path
from typing import AsyncIterator
import hashlib

from ingestion.connectors.base import BaseConnector, ConnectorConfig, RawPayload
from domain.enums import SourceSystem


class FileUploadConnector(BaseConnector):
    """Ingest local files (PDF, XLSX, DOCX) from a watch directory."""

    def __init__(self, config: ConnectorConfig, watch_path: Path) -> None:
        super().__init__(config)
        self.watch_path = watch_path

    async def health_check(self) -> bool:
        return self.watch_path.is_dir()

    def _hash_file(self, path: Path) -> str:
        h = hashlib.sha256()
        with path.open("rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                h.update(chunk)
        return f"sha256:{h.hexdigest()}"

    async def fetch(self) -> AsyncIterator[RawPayload]:
        if not self.watch_path.exists():
            return
        for path in self.watch_path.rglob("*"):
            if not path.is_file():
                continue
            content_hash = self._hash_file(path)
            yield RawPayload(
                source_uri=str(path.relative_to(self.watch_path)),
                content_type="application/octet-stream",
                content_hash=content_hash,
                acquired_at=datetime.now(timezone.utc),
                bytes_ref=f"file://{path.resolve()}",
                metadata={"filename": path.name, "size": path.stat().st_size},
            )

    async def fetch_one(self, source_uri: str) -> RawPayload | None:
        path = self.watch_path / source_uri
        if not path.is_file():
            return None
        return RawPayload(
            source_uri=source_uri,
            content_type="application/octet-stream",
            content_hash=self._hash_file(path),
            acquired_at=datetime.now(timezone.utc),
            bytes_ref=f"file://{path.resolve()}",
        )


def default_file_connector(watch_path: Path) -> FileUploadConnector:
    return FileUploadConnector(
        ConnectorConfig(
            connector_id="file-upload",
            source_system=SourceSystem.FILE_UPLOAD,
        ),
        watch_path,
    )
