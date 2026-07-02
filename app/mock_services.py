from dataclasses import dataclass, field
from pathlib import Path
from tempfile import TemporaryDirectory

from app.document_processing import write_upload_to_temp
from app.schemas import AnalysisResult, Citation, RiskFinding


@dataclass
class MockKnowledgeBase:
    filename: str
    text_preview: str


@dataclass
class MockResponse:
    content: str
    raw_result: AnalysisResult
    messages: list[object] = field(default_factory=list)


def process_mock_document(uploaded_file) -> MockKnowledgeBase:
    """Save and summarize an uploaded document without external services."""
    with TemporaryDirectory() as temp_dir:
        temp_file_path = write_upload_to_temp(uploaded_file, temp_dir)
        text_preview = _read_preview(temp_file_path)
        return MockKnowledgeBase(
            filename=temp_file_path.name,
            text_preview=text_preview,
        )


def build_mock_analysis_result(
    prompt: str = "",
    knowledge_base: MockKnowledgeBase | None = None,
) -> AnalysisResult:
    """Return deterministic analysis data for demos and tests."""
    source_label = knowledge_base.filename if knowledge_base else "mock document"
    source_summary = (
        knowledge_base.text_preview if knowledge_base else "Mock source material."
    )
    citation = Citation(
        source_type="uploaded_document",
        source_label=source_label,
        quote_or_summary=source_summary,
    )
    risk = RiskFinding(
        title="Mock review item",
        severity="unknown",
        explanation=(
            "This deterministic mock finding is for local demos and tests. "
            "It does not evaluate legal meaning."
        ),
        citations=[citation],
    )
    return AnalysisResult(
        summary="Mock analysis generated without external API calls.",
        key_findings=[
            "The uploaded document was accepted by the local mock workflow.",
            "No OpenAI, Anthropic, Qdrant, or DuckDuckGo calls were made.",
        ],
        risks=[risk],
        limitations=[
            "Mock mode is deterministic and does not perform legal analysis.",
            "Use live mode only when configured with real service credentials.",
        ],
        questions_for_professional=[
            "Which clauses should a qualified legal professional review first?",
            "What jurisdiction-specific context is required?",
        ],
        not_legal_advice=True,
    )


def format_analysis_result(result: AnalysisResult) -> str:
    """Render a mock AnalysisResult as Markdown for the existing UI."""
    findings = "\n".join(f"- {finding}" for finding in result.key_findings)
    limitations = "\n".join(f"- {limitation}" for limitation in result.limitations)
    questions = "\n".join(
        f"- {question}" for question in result.questions_for_professional
    )
    risks = "\n".join(
        f"- **{risk.title}** ({risk.severity}): {risk.explanation}"
        for risk in result.risks
    )
    return f"""### Mock Analysis

{result.summary}

**Key Findings**
{findings}

**Risks**
{risks}

**Limitations**
{limitations}

**Questions for a Qualified Legal Professional**
{questions}

Not legal advice: {result.not_legal_advice}
"""


class MockLegalTeam:
    def __init__(self, knowledge_base: MockKnowledgeBase | None = None):
        self.knowledge_base = knowledge_base

    def run(self, prompt: str) -> MockResponse:
        result = build_mock_analysis_result(prompt, self.knowledge_base)
        return MockResponse(content=format_analysis_result(result), raw_result=result)


class MockChatModel:
    def __init__(self, knowledge_base: MockKnowledgeBase | None = None):
        self.knowledge_base = knowledge_base

    def chat(self, prompt: str) -> MockResponse:
        result = build_mock_analysis_result(prompt, self.knowledge_base)
        return MockResponse(content=format_analysis_result(result), raw_result=result)


def _read_preview(path: Path, max_chars: int = 500) -> str:
    if path.suffix.lower() == ".pdf":
        return f"Uploaded PDF file: {path.name}"
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except Exception:
        return f"Uploaded file: {path.name}"
    return text[:max_chars] or f"Uploaded file: {path.name}"
