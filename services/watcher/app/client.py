from __future__ import annotations

from pathlib import Path

import requests

from .config import WATCHER_API_URL


class WatcherUploadError(Exception):
    pass


def _short_response_text(response: requests.Response, max_length: int = 300) -> str:
    content_type = response.headers.get("Content-Type", "")
    if "application/json" in content_type:
        try:
            return str(response.json())[:max_length]
        except ValueError:
            pass
    return response.text[:max_length].replace("", " ")


def upload_file_to_django(file_path: str | Path) -> dict:
    file_path = Path(file_path)
    if not file_path.exists():
        raise WatcherUploadError(f"File not found: {file_path}")

    try:
        with file_path.open("rb") as image_file:
            response = requests.post(
                WATCHER_API_URL,
                files={"file": (file_path.name, image_file, "image/jpeg")},
                timeout=180,
            )
    except requests.RequestException as exc:
        raise WatcherUploadError(f"Could not reach Django upload endpoint: {exc}") from exc

    if not response.ok:
        raise WatcherUploadError(
            f"Django upload failed with status {response.status_code}: {_short_response_text(response)}"
        )

    try:
        return response.json()
    except ValueError as exc:
        raise WatcherUploadError("Django upload endpoint returned a non-JSON response.") from exc