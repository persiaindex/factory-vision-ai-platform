from __future__ import annotations

from pathlib import Path

import torch
from torchvision.models.detection import (
    FasterRCNN_MobileNet_V3_Large_320_FPN_Weights,
    fasterrcnn_mobilenet_v3_large_320_fpn,
)
from torchvision.models.detection.faster_rcnn import FastRCNNPredictor


def build_detection_model(num_classes: int, use_pretrained_weights: bool = True):
    detection_weights = (
        FasterRCNN_MobileNet_V3_Large_320_FPN_Weights.DEFAULT
        if use_pretrained_weights
        else None
    )

    model = fasterrcnn_mobilenet_v3_large_320_fpn(
        weights=detection_weights,
        weights_backbone=None,
    )
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model


def load_trained_detection_model(checkpoint_path: str | Path, num_classes: int, device: torch.device):
    model = build_detection_model(num_classes=num_classes, use_pretrained_weights=False)
    checkpoint = torch.load(Path(checkpoint_path), map_location=device)
    model.load_state_dict(checkpoint["model_state_dict"])
    model.to(device)
    model.eval()
    return model