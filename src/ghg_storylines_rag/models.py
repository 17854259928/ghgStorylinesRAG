"""Validated records produced by the CAP extraction pipeline."""
from __future__ import annotations
from typing import Literal
from pydantic import BaseModel, Field

class Evidence(BaseModel):
    field_name: str
    evidence_text: str
    page: int | None = None

class CAPExtraction(BaseModel):
    source_id: str
    document_type: Literal["legal_act", "strategic_plan", "intervention", "performance_report", "other"] = "other"
    policy_name: str | None = None
    legal_identifier: str | None = None
    jurisdiction: str | None = None
    participating_countries: list[str] = Field(default_factory=list)
    adoption_date: str | None = None
    effective_date: str | None = None
    implementation_start: str | None = None
    implementation_end: str | None = None
    instrument_type: str | None = None
    target_sectors: list[str] = Field(default_factory=list)
    target_gases: list[str] = Field(default_factory=list)
    budget_amount: float | None = None
    currency: str | None = None
    funding_sources: list[str] = Field(default_factory=list)
    national_cofinancing_included: bool | None = None
    planned_outputs: list[str] = Field(default_factory=list)
    reported_outputs: list[str] = Field(default_factory=list)
    reported_outcomes: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    source_url: str | None = None
    source_page: int | None = None
    model_name: str | None = None
    prompt_version: str = "cap-extraction-v1"

# TODO(CAP-RAG): Add controlled vocabularies after inspecting official workbooks.
