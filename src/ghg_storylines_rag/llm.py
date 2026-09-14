"""OpenAI-compatible client for the locally served Qwen model."""
from __future__ import annotations
import json
import re
from .config import PROJECT_ROOT, settings
from .models import CAPExtraction
from openai import OpenAI

def _json_object(text: str) -> dict:
    cleaned = re.sub(r"^```(?:json)?\s*|\s*```$", "", text.strip(), flags=re.IGNORECASE)
    return json.loads(cleaned)

def extract_cap_record(*, source_id: str, text: str, source_url: str | None = None, page: int | None = None) -> CAPExtraction:
    template = (PROJECT_ROOT / "prompts" / "cap_extraction.txt").read_text(encoding="utf-8")
    prompt = template.format(source_id=source_id, source_url=source_url or "unknown", page=page or "unknown", text=text)
    client = OpenAI(base_url=settings.llm_base_url, api_key=settings.llm_api_key)
    response = client.chat.completions.create(
        model=settings.llm_model,
        temperature=0,
        messages=[{"role": "system", "content": "Extract traceable evidence from EU CAP documents. Return JSON only."}, {"role": "user", "content": prompt}],
    )
    payload = _json_object(response.choices[0].message.content or "{}")
    payload.update({"source_id": source_id, "source_url": source_url, "source_page": page, "model_name": settings.llm_model})
    return CAPExtraction.model_validate(payload)

# TODO(CAP-RAG): Add JSON repair, retries, caching, hashes and evidence checks.
