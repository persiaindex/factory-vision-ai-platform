from __future__ import annotations

from pathlib import Path

import requests


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    image_path = base_dir / "shared" / "sample_data" / "dataset_v1" / "images" / "image_001.jpg"

    with image_path.open("rb") as image_file:
        response = requests.post(
            "http://127.0.0.1:8001/predict",
            files={"file": (image_path.name, image_file, "image/jpeg")},
            timeout=60,
        )

    print("Status code:", response.status_code)
    print(response.json())


if __name__ == "__main__":
    main()