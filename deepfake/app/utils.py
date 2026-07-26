from pathlib import Path
from uuid import uuid4

ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}


def is_allowed_file(filename: str) -> bool:
    return Path(filename).suffix.lower() in ALLOWED_EXTENSIONS


def build_upload_path(uploads_dir: Path, original_filename: str) -> Path:
    suffix = Path(original_filename).suffix.lower()
    unique_name = f"{uuid4().hex}{suffix}"
    return uploads_dir / unique_name


def ensure_directory(directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    return directory
