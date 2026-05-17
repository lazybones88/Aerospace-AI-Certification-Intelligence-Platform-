from dataclasses import dataclass
from typing import Any


@dataclass
class DocumentChunk:
    """Semantic chunk with aerospace-aware metadata slots."""

    chunk_id: str
    document_id: str
    text: str
    section: str | None
    page: int | None
    entities: dict[str, list[str]]  # subsystem, dal, requirement_id, standard_ref
    embedding_ready: bool = True


class DocumentParser:
    """
    Document parsing pipeline stage.
    Phase 1: structure-aware chunking; OCR/NER integrations plug in here.
    """

    def __init__(self, chunk_size: int = 512, chunk_overlap: int = 64) -> None:
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def parse_text(self, document_id: str, text: str, metadata: dict[str, Any] | None = None) -> list[DocumentChunk]:
        metadata = metadata or {}
        chunks: list[DocumentChunk] = []
        start = 0
        idx = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            chunk_text = text[start:end].strip()
            if chunk_text:
                chunks.append(
                    DocumentChunk(
                        chunk_id=f"{document_id}:chunk:{idx}",
                        document_id=document_id,
                        text=chunk_text,
                        section=metadata.get("section"),
                        page=metadata.get("page"),
                        entities=self._extract_entities(chunk_text),
                    )
                )
                idx += 1
            start = end - self.chunk_overlap if end < len(text) else end
        return chunks

    def _extract_entities(self, text: str) -> dict[str, list[str]]:
        """Placeholder NER — replace with aerospace-tuned model in production."""
        entities: dict[str, list[str]] = {
            "requirement_id": [],
            "standard_ref": [],
            "subsystem": [],
            "dal": [],
        }
        for token in text.split():
            upper = token.upper()
            if upper.startswith("REQ-") or upper.startswith("SYS-REQ-"):
                entities["requirement_id"].append(token.rstrip(".,;"))
            if upper.startswith("DO-") or upper.startswith("ARP"):
                entities["standard_ref"].append(token.rstrip(".,;"))
            if upper in ("DAL-A", "DAL-B", "DAL-C", "DAL-D", "DAL-E", "LEVEL-A"):
                entities["dal"].append(upper)
        return entities
