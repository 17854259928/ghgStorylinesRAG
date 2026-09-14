"""Download and parse official CAP HTML, PDF and XLSX sources."""
from __future__ import annotations
import hashlib
from pathlib import Path
import pandas as pd
import requests
from bs4 import BeautifulSoup
from pypdf import PdfReader

USER_AGENT = "ghgStorylinesRAG academic policy research"

def download(url: str, document_type: str, raw_root: Path, timeout: int = 90) -> Path:
    suffixes = {"html": ".html", "pdf": ".pdf", "xlsx": ".xlsx"}
    if document_type not in suffixes:
        raise ValueError(f"Unsupported document type: {document_type}")
    response = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=timeout)
    response.raise_for_status()
    folder = raw_root / document_type
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / (hashlib.sha256(url.encode()).hexdigest()[:16] + suffixes[document_type])
    target.write_bytes(response.content)
    return target

def parse_html(path: Path) -> str:
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "lxml")
    for node in soup(["script", "style", "nav", "footer", "noscript"]):
        node.decompose()
    return "\n".join(line.strip() for line in soup.get_text("\n").splitlines() if line.strip())

def parse_pdf(path: Path) -> list[dict[str, int | str]]:
    return [{"page": n, "text": page.extract_text() or ""} for n, page in enumerate(PdfReader(path).pages, 1)]

def parse_xlsx(path: Path) -> dict[str, pd.DataFrame]:
    workbook = pd.ExcelFile(path)
    return {sheet: pd.read_excel(path, sheet_name=sheet) for sheet in workbook.sheet_names}

# TODO(CAP-RAG): Add OCR fallback and source content hashes/versioning.
