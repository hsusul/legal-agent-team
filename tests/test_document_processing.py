from io import BytesIO

import pytest

from app.document_processing import (
    UploadValidationError,
    sanitize_uploaded_filename,
    validate_allowed_extension,
    validate_upload_size,
    write_upload_to_temp,
)


class FakeUpload:
    def __init__(self, name: str, content: bytes):
        self.name = name
        self._buffer = BytesIO(content)
        self.size = len(content)

    def getbuffer(self):
        return self._buffer.getbuffer()


def test_sanitize_uploaded_filename_removes_path_traversal():
    assert sanitize_uploaded_filename("../secret.pdf") == "secret.pdf"


def test_validate_allowed_extension_rejects_disallowed_extension():
    with pytest.raises(UploadValidationError, match="Unsupported file type"):
        validate_allowed_extension("payload.exe")


def test_validate_upload_size_rejects_oversized_upload():
    upload = FakeUpload("large.pdf", b"abcdef")

    with pytest.raises(UploadValidationError, match="too large"):
        validate_upload_size(upload, max_size=5)


def test_write_upload_to_temp_writes_to_safe_path(tmp_path):
    upload = FakeUpload("../secret.pdf", b"pdf bytes")

    written_path = write_upload_to_temp(upload, tmp_path)

    assert written_path == tmp_path / "secret.pdf"
    assert written_path.read_bytes() == b"pdf bytes"
    assert written_path.parent == tmp_path
