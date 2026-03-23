from app.schemas.prediction import DetectionSchema, PredictionResponseSchema


def run_stub_prediction() -> PredictionResponseSchema:
    detection = DetectionSchema(
        object_name="bottle",
        confidence=0.97,
        bbox_x_min=12.0,
        bbox_y_min=24.0,
        bbox_x_max=128.0,
        bbox_y_max=256.0,
        estimated_width_mm=55.0,
        estimated_height_mm=210.0,
        estimated_scale_mm_per_pixel=0.5,
        size_status="OK",
    )

    return PredictionResponseSchema(
        status="ok",
        model_version="stub-model-v1",
        detections=[detection],
    )