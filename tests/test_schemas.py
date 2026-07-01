import pytest
from pydantic import ValidationError

from app.schemas import AnalysisResult, RiskFinding


def _valid_citation():
    return {
        "source_type": "uploaded_document",
        "source_label": "sample.pdf page 1",
        "quote_or_summary": "The agreement includes a termination clause.",
    }


def _valid_risk():
    return {
        "title": "Ambiguous termination timing",
        "severity": "medium",
        "explanation": "The clause does not clearly define the notice period.",
        "citations": [_valid_citation()],
    }


def test_valid_analysis_result_parses():
    result = AnalysisResult(
        summary="Research summary.",
        key_findings=["Termination language may need review."],
        risks=[_valid_risk()],
        limitations=["This is based only on the uploaded document."],
        questions_for_professional=["What jurisdiction governs the agreement?"],
    )

    assert result.not_legal_advice is True
    assert result.risks[0].citations[0].source_type == "uploaded_document"


def test_invalid_severity_is_rejected():
    payload = _valid_risk()
    payload["severity"] = "critical"

    with pytest.raises(ValidationError):
        RiskFinding.model_validate(payload)


def test_missing_citations_on_risk_finding_is_rejected():
    payload = _valid_risk()
    payload["citations"] = []

    with pytest.raises(ValidationError):
        RiskFinding.model_validate(payload)


def test_not_legal_advice_defaults_to_true():
    result = AnalysisResult(
        summary="Research summary.",
        key_findings=[],
        risks=[],
        limitations=[],
        questions_for_professional=[],
    )

    assert result.not_legal_advice is True
