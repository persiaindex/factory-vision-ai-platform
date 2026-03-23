from fastapi import APIRouter, File, UploadFile

from app.core.config import MODEL_DIR, SERVICE_NAME, SERVICE_VERSION
from app.schemas.prediction import PredictionResponseSchema
from app.services.predictor import run_stub_prediction

router = APIRouter()


@router.get("/health")
def health_check() -> dict:
    return {
        "status": "ok",
        "service": SERVICE_NAME,
        "version": SERVICE_VERSION,
        "model_dir": str(MODEL_DIR),
    }


@router.post("/predict", response_model=PredictionResponseSchema)
async def predict(file: UploadFile = File(...)) -> PredictionResponseSchema:
    _ = file.filename
    return run_stub_prediction()