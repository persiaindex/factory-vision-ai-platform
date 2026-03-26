from __future__ import annotations

from pathlib import Path

import requests
from django.conf import settings


class InferenceServiceError(Exception):
    pass


def call_inference_service(image_path: str | Path) -> dict:
    image_path = Path(image_path)
    if not image_path.exists():
        raise InferenceServiceError(f"Image file does not exist: {image_path}")

    with image_path.open("rb") as image_file:
        response = requests.post(
            settings.INFERENCE_SERVICE_URL,
            files={"file": (image_path.name, image_file, "image/jpeg")},
            timeout=120,
        )

    if not response.ok:
        raise InferenceServiceError(
            f"Inference service failed with status {response.status_code}: {response.text}"
        )

    return response.json()