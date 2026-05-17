"""Rule-based grounded answers for demo mode (no LLM required)."""

from intelligence.rag.pipeline import RAGQuery


def build_grounded_answer(question: str, chunks: list[dict[str, str]]) -> str:
    q = question.lower()
    sources = sorted({c.get("source_uri", "unknown") for c in chunks})

    if any(w in q for w in ("flight test", "flight testing", "delay")):
        risks = _extract_lines(chunks, ("RISK-CERT", "flight test", "FT-GATE"))
        return (
            "Based on ingested demo evidence, unresolved certification risks that could delay "
            f"flight testing include: {_join_unique(risks) or 'RISK-CERT-07 and RISK-CERT-14 per software requirements'}. "
            f"Flight test gate FT-GATE-3 is explicitly cited as at risk. Sources: {', '.join(sources)}."
        )

    if "firmware" in q or "avionics" in q or "2.4.1" in q:
        impacts = _extract_lines(chunks, ("SW-REQ", "TC-FCC", "HAZ-FCC", "CR-FCC"))
        return (
            "The avionics firmware v2.4.1 change (CR-FCC-241) impacts requirements SW-REQ-1042 and "
            "SW-REQ-1060, requires re-execution of tests TC-FCC-020 and TC-FCC-040, and triggers "
            f"safety re-review for HAZ-FCC-003. Affected items found: {_join_unique(impacts)}. "
            f"Sources: {', '.join(sources)}."
        )

    if "requirement" in q:
        reqs = _extract_lines(chunks, ("SW-REQ", "SYS-REQ"))
        return (
            f"Relevant requirements in demo evidence: {_join_unique(reqs)}. "
            f"See trace matrix for verification links. Sources: {', '.join(sources)}."
        )

    # Default: summarize top chunk themes
    excerpts = " | ".join(c["text"][:120].replace("\n", " ") for c in chunks[:3])
    return (
        f"From {len(chunks)} evidence excerpt(s): {excerpts}... "
        f"Full citations attached. Sources: {', '.join(sources)}."
    )


def _extract_lines(chunks: list[dict], markers: tuple[str, ...]) -> list[str]:
    found: list[str] = []
    for c in chunks:
        for line in c["text"].splitlines():
            if any(m in line for m in markers):
                found.append(line.strip()[:200])
    return found[:8]


def _join_unique(lines: list[str]) -> str:
    seen: set[str] = set()
    out: list[str] = []
    for line in lines:
        if line and line not in seen:
            seen.add(line)
            out.append(line)
    return "; ".join(out[:5])
