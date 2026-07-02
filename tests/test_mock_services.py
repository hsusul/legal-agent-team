from io import BytesIO

from app.mock_services import (
    MockKnowledgeBase,
    build_mock_analysis_result,
    process_mock_document,
)
from app.schemas import AnalysisResult


class FakeUpload:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self._buffer = BytesIO(content)
        self.size = len(content)

    def getbuffer(self):
        return self._buffer.getbuffer()


def test_mock_analysis_returns_valid_analysis_result():
    result = build_mock_analysis_result(
        prompt="Analyze this.",
        knowledge_base=MockKnowledgeBase(
            filename="contract.txt",
            text_preview="Sample contract text.",
        ),
    )

    assert isinstance(result, AnalysisResult)
    assert result.not_legal_advice is True
    assert result.risks[0].citations[0].source_label == "contract.txt"


def test_process_mock_document_uses_local_upload_only():
    upload = FakeUpload("contract.txt", b"Plain text contract")

    knowledge_base = process_mock_document(upload)

    assert knowledge_base.filename == "contract.txt"
    assert knowledge_base.text_preview == "Plain text contract"
