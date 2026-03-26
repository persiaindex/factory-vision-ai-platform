from __future__ import annotations

import json
from pathlib import Path

from ml.utils.calibration import load_calibration_config
from ml.utils.image_preprocessing import prepare_image_report, read_image_bgr
from ml.utils.measurement import measure_detection


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    image_path = base_dir / "shared" / "sample_data" / "dataset_v1" / "images" / "image_001.jpg"
    annotation_path = base_dir / "shared" / "sample_data" / "dataset_v1" / "annotations" / "image_001.json"
    calibration_path = base_dir / "artifacts" / "models" / "current" / "calibration_config.json"
    output_path = base_dir / "artifacts" / "reports" / "measurement_report.json"

    image_bgr = read_image_bgr(str(image_path))
    image_report = prepare_image_report(image_bgr)

    annotation = json.loads(annotation_path.read_text(encoding="utf-8"))
    calibration_config = load_calibration_config(calibration_path)

    detections = []
    for obj in annotation["objects"]:
        class_name = obj["class_name"]
        bbox = [
            float(obj["bbox"]["x_min"]),
            float(obj["bbox"]["y_min"]),
            float(obj["bbox"]["x_max"]),
            float(obj["bbox"]["y_max"]),
        ]

        measurement = measure_detection(
            box=bbox,
            class_name=class_name,
            calibration_config=calibration_config,
        )

        detections.append(
            {
                "class_name": class_name,
                "bbox": bbox,
                **measurement,
            }
        )

    report = {
        "status": "ok",
        "image_path": str(image_path),
        "image_report": image_report,
        "calibration_version": calibration_config["version"],
        "detections": detections,
    }

    output_path.write_text(json.dumps(report, indent=2), encoding="utf-8")

    print("Measurement pipeline test completed successfully.")
    print(f"Measurement report: {output_path}")


if __name__ == "__main__":
    main()