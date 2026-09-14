"""Deterministic text chunking for the first local prototype."""

def chunk_text(text: str, size: int = 8000, overlap: int = 600) -> list[str]:
    if size <= 0 or overlap < 0 or overlap >= size:
        raise ValueError("Require size > 0 and 0 <= overlap < size")
    clean = "\n".join(line.strip() for line in text.splitlines() if line.strip())
    if not clean:
        return []
    chunks, start = [], 0
    while start < len(clean):
        end = min(start + size, len(clean))
        if end < len(clean):
            boundary = clean.rfind("\n", start, end)
            if boundary > start + size // 2:
                end = boundary
        chunks.append(clean[start:end])
        if end == len(clean):
            break
        start = end - overlap
    return chunks

# TODO(CAP-RAG): Replace character chunks with section/table-aware chunks.
