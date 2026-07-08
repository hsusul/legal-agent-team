from app.analysis import AnalysisRequest, run_analysis_request
from app.schemas import AnalysisResult


class FakeResponse:
    def __init__(self, content: str):
        self.content = content
        self.messages = []


def test_mock_mode_returns_deterministic_analysis_result():
    result = run_analysis_request(
        AnalysisRequest(
            document_text="Sample contract text.",
            analysis_type="Contract Review",
            app_mode="mock",
        )
    )

    assert isinstance(result.response.raw_result, AnalysisResult)
    assert result.response.raw_result.not_legal_advice is True
    assert "without external API calls" in result.response.content


def test_custom_query_is_passed_to_live_runner():
    prompts = []

    def fake_runner(prompt: str):
        prompts.append(prompt)
        return FakeResponse("Live response")

    run_analysis_request(
        AnalysisRequest(
            document_text="Sample contract text.",
            analysis_type="Custom Query",
            custom_query="Find renewal language.",
            app_mode="live",
        ),
        analysis_runner=fake_runner,
    )

    assert "Find renewal language." in prompts[0]


def test_mock_mode_does_not_require_external_runner():
    result = run_analysis_request(
        AnalysisRequest(
            document_text="Sample contract text.",
            analysis_type="Risk Assessment",
            app_mode="mock",
        )
    )

    assert result.key_points_response.content
    assert result.considerations_response.content
