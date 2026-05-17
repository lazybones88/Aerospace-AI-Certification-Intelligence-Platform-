from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, AsyncIterator

from pydantic import BaseModel, Field

from domain.enums import SourceSystem


class ConnectorConfig(BaseModel):
    connector_id: str
    source_system: SourceSystem
    enabled: bool = True
    poll_interval_seconds: int = 300
    credentials_ref: str | None = None  # vault path, never inline secrets
    options: dict[str, Any] = Field(default_factory=dict)


class RawPayload(BaseModel):
    """Raw artifact acquired from a source system before normalization."""

    source_uri: str
    content_type: str
    content_hash: str
    acquired_at: datetime
    bytes_ref: str  # object storage URI
    metadata: dict[str, Any] = Field(default_factory=dict)


class BaseConnector(ABC):
    """Abstract connector for engineering and document source systems."""

    def __init__(self, config: ConnectorConfig) -> None:
        self.config = config

    @abstractmethod
    async def health_check(self) -> bool:
        """Verify connectivity and credentials."""

    @abstractmethod
    async def fetch(self) -> AsyncIterator[RawPayload]:
        """Yield new or updated raw payloads since last cursor."""

    @abstractmethod
    async def fetch_one(self, source_uri: str) -> RawPayload | None:
        """Fetch a single artifact by source URI."""
