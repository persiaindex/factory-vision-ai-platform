from __future__ import annotations

import shutil
from pathlib import Path

from .client import WatcherUploadError, upload_file_to_django
from .config import WATCHER_FAILED_DIR


class FileProcessResult:
    def __init__(self, status: str, message: str, response_data: dict | None = None) -> None:
        self.status = status
        self.message = message
        self.response_data = response_data or {}


def move_to_failed_folder(file_path: str | Path) -> Path:
    file_path = Path(file_path)
    WATCHER_FAILED_DIR.mkdir(parents=True, exist_ok=True)
    target_path = WATCHER_FAILED_DIR / file_path.name
    shutil.move(str(file_path), str(target_path))
    return target_path


def process_file(file_path: str | Path) -> FileProcessResult:
    file_path = Path(file_path)

    try:
        response_data = upload_file_to_django(file_path)
        file_path.unlink()
        return FileProcessResult(
            status="success",
            message=f"Uploaded successfully and deleted local file: {file_path.name}",
            response_data=response_data,
        )
    except WatcherUploadError as exc:
        failed_path = move_to_failed_folder(file_path)
        return FileProcessResult(
            status="failed",
            message=f"Upload failed and file moved to failed folder: {failed_path} | error={exc}",
        )
    except Exception as exc:
        failed_path = move_to_failed_folder(file_path)
        return FileProcessResult(
            status="failed",
            message=f"Unexpected watcher error, file moved to failed folder: {failed_path} | error={exc}",
        )