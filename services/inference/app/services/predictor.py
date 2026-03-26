from __future__ import annotations

import json
from pathlib import Path

import torch
from torchvision.transforms import functional as F

from ml.training.model_factory import load_trained_detection_model
from ml.utils.calibration import load_calibration_config
from ml.utils.image_preprocessing import bgr_to_rgb, decode_image_bytes_to_bgr
from ml.utils.measurement import measure_detection
from services.inference.app.schemas.prediction import DetectionSchema, PredictionResponseSchema


class InferenceRuntime:
    def __init__(self, base_dir: Path, device_name: str = "cpu", confidence_threshold: float = 0.1) -> None:
        self.base_dir = base_dir
        self.device = torch.device(device_name)
        self.confidence_threshold = confidence_threshold

        self.current_model_dir = self.base_dir / "artifacts" / "models" / "current"
        self.model_info_path = self.current_model_dir / "model_info.json"
        self.model_checkpoint_path = self.current_model_dir / "model.pt"
        self.calibration_config_path = self.current_model_dir / "calibration_config.json"

        self.model_info = json.loads(self.model_info_path.read_text(encoding="utf-8"))
        self.calibration_config = load_calibration_config(self.calibration_config_path)
        self.model = load_trained_detection_model(
            checkpoint_path=self.model_checkpoint_path,
            num_classes=self.model_info["num_classes"],
            device=self.device,
        )

    def predict_from_bytes(self, file_bytes: bytes) -> PredictionResponseSchema:
        image_bgr = decode_image_bytes_to_bgr(file_bytes)
        image_rgb = bgr_to_rgb(image_bgr)

        image_tensor = F.to_tensor(image_rgb).to(self.device)

        with torch.no_grad():
            outputs = self.model([image_tensor])

        output = outputs[0]
        detections: list[DetectionSchema] = []

        for box, score, label in zip(output["boxes"], output["scores"], output["labels"]):
            score_value = float(score.item())
            label_value = int(label.item())

            if label_value != 1:
                continue
            if score_value < self.confidence_threshold:
                continue

            box_list = [float(value) for value in box.tolist()]
            measurement = measure_detection(
                box=box_list,
                class_name="bottle",
                calibration_config=self.calibration_config,
            )

            detections.append(
                DetectionSchema(
                    object_name="bottle",
                    confidence=score_value,
                    bbox_x_min=box_list[0],
                    bbox_y_min=box_list[1],
                    bbox_x_max=box_list[2],
                    bbox_y_max=box_list[3],
                    estimated_width_mm=measurement["estimated_width_mm"],
                    estimated_height_mm=measurement["estimated_height_mm"],
                    estimated_scale_mm_per_pixel=measurement["estimated_scale_mm_per_pixel"],
                    size_status=measurement["size_status"],
                )
            )

        return PredictionResponseSchema(
            status="ok",
            model_version=self.model_info.get("model_name", "current-model"),
            confidence_threshold=self.confidence_threshold,
            num_detections=len(detections),
            detections=detections,
        )