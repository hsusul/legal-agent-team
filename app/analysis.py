from dataclasses import dataclass
from typing import Callable, Literal

from app.mock_services import (
    MockKnowledgeBase,
    MockResponse,
    build_mock_analysis_result,
    format_analysis_result,
)
from app.prompts import (
    build_analysis_prompt,
    build_considerations_prompt,
    build_key_points_prompt,
)

AppMode = Literal["live", "mock"]

ANALYSIS_CONFIGS = {
    "Contract Review": {
        "query": "Review this contract and identify key terms, obligations, and potential issues.",
        "agents": ["Contract Analyst"],
        "description": "Detailed contract analysis focusing on terms and obligations",
    },
    "Legal Research": {
        "query": "Research relevant cases and precedents related to this document.",
        "agents": ["Legal Researcher"],
        "description": "Research on relevant legal cases and precedents",
    },
    "Risk Assessment": {
        "query": "Analyze potential legal risks and liabilities in this document.",
        "agents": ["Contract Analyst", "Legal Strategist"],
        "description": "Combined risk analysis and strategic assessment",
    },
    "Compliance Check": {
        "query": "Check this document for regulatory compliance issues.",
        "agents": ["Legal Researcher", "Contract Analyst", "Legal Strategist"],
        "description": "Comprehensive compliance analysis",
    },
    "Custom Query": {
        "query": None,
        "agents": ["Legal Researcher", "Contract Analyst", "Legal Strategist"],
        "description": "Custom analysis using all available agents",
    },
}


@dataclass(frozen=True)
class AnalysisRequest:
    document_text: str
    analysis_type: str
    custom_query: str | None = None
    app_mode: AppMode = "live"


@dataclass(frozen=True)
class AnalysisRunResult:
    response: object
    key_points_response: object
    considerations_response: object


def get_analysis_config(analysis_type: str) -> dict:
    try:
        return ANALYSIS_CONFIGS[analysis_type]
    except KeyError as exc:
        raise ValueError(f"Unknown analysis type: {analysis_type}") from exc


def run_analysis_request(
    request: AnalysisRequest,
    analysis_runner: Callable[[str], object] | None = None,
) -> AnalysisRunResult:
    """Run the analysis flow in live mode or deterministic mock mode."""
    config = get_analysis_config(request.analysis_type)
    if request.app_mode == "mock":
        return _run_mock_analysis(request)

    if analysis_runner is None:
        raise ValueError("analysis_runner is required in live mode")

    analysis_prompt = build_analysis_prompt(
        analysis_task=config["query"],
        focus_agents=config["agents"],
        user_query=request.custom_query
        if request.analysis_type == "Custom Query"
        else None,
    )
    response = analysis_runner(analysis_prompt)

    key_points_response = analysis_runner(
        build_key_points_prompt(
            previous_analysis=_response_content(response),
            focus_agents=config["agents"],
        )
    )
    considerations_response = analysis_runner(
        build_considerations_prompt(
            previous_analysis=_response_content(response),
            focus_agents=config["agents"],
        )
    )

    return AnalysisRunResult(
        response=response,
        key_points_response=key_points_response,
        considerations_response=considerations_response,
    )


def _run_mock_analysis(request: AnalysisRequest) -> AnalysisRunResult:
    knowledge_base = MockKnowledgeBase(
        filename="mock-uploaded-document",
        text_preview=request.document_text or "Mock source material.",
    )
    result = build_mock_analysis_result(
        prompt=request.custom_query or request.analysis_type,
        knowledge_base=knowledge_base,
    )
    response = MockResponse(content=format_analysis_result(result), raw_result=result)
    key_points_response = MockResponse(
        content="\n".join(f"- {finding}" for finding in result.key_findings),
        raw_result=result,
    )
    considerations_response = MockResponse(
        content="\n".join(result.questions_for_professional),
        raw_result=result,
    )
    return AnalysisRunResult(
        response=response,
        key_points_response=key_points_response,
        considerations_response=considerations_response,
    )


def _response_content(response: object) -> str:
    return getattr(response, "content", str(response))
