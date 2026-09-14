"""Minimal extraction entry point for one local document."""
from __future__ import annotations
import json
from pathlib import Path
from .chunking import chunk_text
from .config import settings
from .documents import parse_html, parse_pdf
from .llm import extract_cap_record

def extract_file(source_id: str, path: Path, source_url: str | None = None) -> Path:
    settings.ensure_directories()
    if path.suffix.lower() == ".pdf":
        units = parse_pdf(path)
    elif path.suffix.lower() in {".html", ".htm"}:
        units = [{"page": None, "text": parse_html(path)}]
    else:
        raise ValueError("Use this extractor for HTML/PDF; read XLSX deterministically with pandas.")
    output = settings.extracted_root / f"{source_id}.jsonl"
    with output.open("w", encoding="utf-8") as handle:
        for unit_index, unit in enumerate(units, 1):
            for chunk_index, chunk in enumerate(chunk_text(str(unit["text"]), settings.chunk_size, settings.chunk_overlap), 1):
                record = extract_cap_record(source_id=f"{source_id}-u{unit_index}-c{chunk_index}", text=chunk, source_url=source_url, page=unit["page"] if isinstance(unit["page"], int) else None)
                handle.write(json.dumps(record.model_dump(mode="json"), ensure_ascii=False) + "\n")
    return output

# TODO(CAP-RAG): Add registry batches, checkpoints, deduplication and final tables.
