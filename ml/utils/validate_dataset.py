from __future__ import annotations

import json
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parents[2]
DATASET_DIR = BASE_DIR / "shared" / "sample_data" / "dataset_v1"
IMAGES_DIR = DATASET_DIR / "images"
ANNOTATIONS_DIR = DATASET_DIR / "annotations"
SPLITS_DIR = DATASET_DIR / "splits"

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
ALLOWED_CLASSES = {"bottle"}


def load_split_ids(split_path: Path) -> list[str]:
    return [line.strip() for line in split_path.read_text().splitlines() if line.strip()]


def validate_annotation(annotation_path: Path) -> list[str]:
    errors: list[str] = []
    data = json.loads(annotation_path.read_text(encoding="utf-8"))

    required_top_keys = {"image_filename", "image_width", "image_height", "objects"}
    missing_keys = required_top_keys - data.keys()
    if missing_keys:
        errors.append(f"{annotation_path.name}: missing keys {sorted(missing_keys)}")
        return errors

    if not isinstance(data["objects"], list):
        errors.append(f"{annotation_path.name}: 'objects' must be a list")
        return errors

    width = data["image_width"]
    height = data["image_height"]

    for index, obj in enumerate(data["objects"]):
        class_name = obj.get("class_name")
        bbox = obj.get("bbox", {})

        if class_name not in ALLOWED_CLASSES:
            errors.append(f"{annotation_path.name}: object {index} has invalid class '{class_name}'")

        bbox_keys = {"x_min", "y_min", "x_max", "y_max"}
        if bbox_keys - bbox.keys():
            errors.append(f"{annotation_path.name}: object {index} missing bbox keys")
            continue

        x_min = bbox["x_min"]
        y_min = bbox["y_min"]
        x_max = bbox["x_max"]
        y_max = bbox["y_max"]

        if not (0 <= x_min < x_max <= width):
            errors.append(f"{annotation_path.name}: object {index} has invalid x bbox")
        if not (0 <= y_min < y_max <= height):
            errors.append(f"{annotation_path.name}: object {index} has invalid y bbox")

    return errors


def validate_split(split_name: str) -> list[str]:
    errors: list[str] = []
    split_ids = load_split_ids(SPLITS_DIR / f"{split_name}.txt")

    for sample_id in split_ids:
        matching_images = [
            path for path in IMAGES_DIR.iterdir()
            if path.is_file() and path.stem == sample_id and path.suffix.lower() in ALLOWED_IMAGE_EXTENSIONS
        ]

        if len(matching_images) != 1:
            errors.append(f"{split_name}: sample '{sample_id}' must have exactly one matching image file")
            continue

        annotation_path = ANNOTATIONS_DIR / f"{sample_id}.json"
        if not annotation_path.exists():
            errors.append(f"{split_name}: missing annotation file for '{sample_id}'")
            continue

        errors.extend(validate_annotation(annotation_path))

    return errors


def main() -> None:
    all_errors = []
    for split_name in ["train", "val"]:
        all_errors.extend(validate_split(split_name))

    if all_errors:
        print("Dataset validation failed:")
        for error in all_errors:
            print(f"- {error}")
        raise SystemExit(1)

    print("Dataset validation passed.")


if __name__ == "__main__":
    main()