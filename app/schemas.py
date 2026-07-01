from typing import Literal

from pydantic import BaseModel, Field


SourceType = Literal["uploaded_document", "web_source", "prior_analysis"]
RiskSeverity = Literal["low", "medium", "high", "unknown"]


class Citation(BaseModel):
    source_type: SourceType
    source_label: str
    quote_or_summary: str


class RiskFinding(BaseModel):
    title: str
    severity: RiskSeverity
    explanation: str
    citations: list[Citation] = Field(min_length=1)


class AnalysisResult(BaseModel):
    summary: str
    key_findings: list[str]
    risks: list[RiskFinding]
    limitations: list[str]
    questions_for_professional: list[str]
    not_legal_advice: bool = True
