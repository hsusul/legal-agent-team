from pathlib import Path
from typing import BinaryIO, Iterable


ALLOWED_UPLOAD_EXTENSIONS = {
    ".csv",
    ".docx",
    ".htm",
    ".html",
    ".json",
    ".pdf",
    ".pptx",
    ".txt",
    ".xlsx",
    ".xml",
}
MAX_UPLOAD_SIZE_BYTES = 10 * 1024 * 1024


class UploadValidationError(ValueError):
    """Raised when an uploaded file fails validation."""


def sanitize_uploaded_filename(filename: str) -> str:
    """Return only the final path component from an uploaded filename."""
    safe_name = Path(filename).name
    if not safe_name or safe_name in {".", ".."}:
        raise UploadValidationError("Uploaded file must have a valid filename.")
    return safe_name


def validate_allowed_extension(
    filename: str, allowed_extensions: Iterable[str] = ALLOWED_UPLOAD_EXTENSIONS
) -> None:
    """Validate that the filename has a supported extension."""
    suffix = Path(filename).suffix.lower()
    allowed = {extension.lower() for extension in allowed_extensions}
    if suffix not in allowed:
        allowed_list = ", ".join(sorted(allowed))
        raise UploadValidationError(
            f"Unsupported file type '{suffix or '<none>'}'. Allowed types: {allowed_list}."
        )


def validate_upload_size(uploaded_file: BinaryIO, max_size: int = MAX_UPLOAD_SIZE_BYTES) -> None:
    """Validate that the uploaded file is within the configured size limit."""
    file_size = getattr(uploaded_file, "size", None)
    if file_size is None:
        file_size = len(uploaded_file.getbuffer())
    if file_size > max_size:
        raise UploadValidationError(
            f"Uploaded file is too large. Maximum size is {max_size} bytes."
        )


def write_upload_to_temp(
    uploaded_file: BinaryIO,
    temp_dir: str | Path,
    allowed_extensions: Iterable[str] = ALLOWED_UPLOAD_EXTENSIONS,
    max_size: int = MAX_UPLOAD_SIZE_BYTES,
) -> Path:
    """Validate and write an uploaded file inside the provided temp directory."""
    safe_name = sanitize_uploaded_filename(uploaded_file.name)
    validate_allowed_extension(safe_name, allowed_extensions)
    validate_upload_size(uploaded_file, max_size)

    destination = Path(temp_dir) / safe_name
    destination.write_bytes(bytes(uploaded_file.getbuffer()))
    return destination
