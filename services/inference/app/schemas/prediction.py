from pydantic import BaseModel, Field


class DetectionSchema(BaseModel):
    object_name: str = Field(..., examples=["bottle"])
    confidence: float = Field(..., examples=[0.97])
    bbox_x_min: float = Field(..., examples=[12.0])
    bbox_y_min: float = Field(..., examples=[24.0])
    bbox_x_max: float = Field(..., examples=[128.0])
    bbox_y_max: float = Field(..., examples=[256.0])
    estimated_width_mm: float | None = Field(default=None, examples=[55.0])
    estimated_height_mm: float | None = Field(default=None, examples=[210.0])
    estimated_scale_mm_per_pixel: float | None = Field(default=None, examples=[0.5])
    size_status: str = Field(..., examples=["OK"])


class PredictionResponseSchema(BaseModel):
    status: str = Field(..., examples=["ok"])
    model_version: str = Field(..., examples=["stub-model-v1"])
    detections: list[DetectionSchema]