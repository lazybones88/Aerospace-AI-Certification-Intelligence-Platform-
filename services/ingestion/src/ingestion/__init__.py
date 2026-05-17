"""Ingestion layer: connectors, parsers, and normalization pipelines."""

from ingestion.connectors.base import BaseConnector, ConnectorConfig, RawPayload
from ingestion.pipeline import IngestionPipeline, PipelineStage

__all__ = [
    "BaseConnector",
    "ConnectorConfig",
    "IngestionPipeline",
    "PipelineStage",
    "RawPayload",
]
