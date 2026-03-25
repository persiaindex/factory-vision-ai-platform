from __future__ import annotations

from torchvision.models import MobileNet_V3_Large_Weights
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
    backbone_weights = None if use_pretrained_weights else None

    model = fasterrcnn_mobilenet_v3_large_320_fpn(
        weights=detection_weights,
        weights_backbone=backbone_weights,
    )
    in_features = model.roi_heads.box_predictor.cls_score.in_features
    model.roi_heads.box_predictor = FastRCNNPredictor(in_features, num_classes)
    return model