import re
from pathlib import Path

from intelligence.rag.pipeline import RAGQuery


class LocalDocumentRetriever:
    """
    Loads markdown/text from data/public and retrieves chunks by keyword relevance.
    No external vector DB required — suitable for demo and CI.
    """

    def __init__(self, chunks: list[dict[str, str]]) -> None:
        self._chunks = chunks

    @classmethod
    def from_directory(cls, root: Path, program_id: str | None = None) -> "LocalDocumentRetriever":
        chunks: list[dict[str, str]] = []
        if not root.is_dir():
            return cls(chunks)

        for path in sorted(root.rglob("*.md")):
            rel = path.relative_to(root).as_posix()
            if rel.startswith("graph/") or path.name.upper() == "README.MD":
                continue
            text = path.read_text(encoding="utf-8")
            doc_id = rel.replace("/", ":").replace(".md", "")
            for i, block in enumerate(cls._split_blocks(text)):
                chunk_text = block.strip()
                if len(chunk_text) < 40:
                    continue
                chunks.append(
                    {
                        "chunk_id": f"{doc_id}:block:{i}",
                        "document_id": doc_id,
                        "text": chunk_text,
                        "source_uri": f"data/public/{rel}",
                        "program_id": program_id or "dap-100",
                    }
                )
        return cls(chunks)

    @staticmethod
    def _split_blocks(text: str) -> list[str]:
        parts = re.split(r"\n(?=#{1,3}\s)", text)
        if len(parts) <= 1:
            parts = re.split(r"\n(?=---\n)", text)
        return parts if parts else [text]

    async def retrieve(self, q: RAGQuery) -> list[dict[str, str]]:
        if not self._chunks:
            return []

        query_tokens = set(_tokenize(q.question))
        scored: list[tuple[float, dict[str, str]]] = []

        for chunk in self._chunks:
            if q.program_id and chunk.get("program_id") != q.program_id:
                continue
            text_tokens = set(_tokenize(chunk["text"]))
            overlap = len(query_tokens & text_tokens)
            if overlap == 0:
                continue
            # Boost certification-domain terms in the question
            boost = 0.0
            for term in ("risk", "flight", "test", "firmware", "requirement", "hazard", "certification"):
                if term in q.question.lower() and term in chunk["text"].lower():
                    boost += 0.5
            scored.append((overlap + boost, chunk))

        scored.sort(key=lambda x: x[0], reverse=True)
        return [c for _, c in scored[: q.max_chunks]]


def _tokenize(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())
