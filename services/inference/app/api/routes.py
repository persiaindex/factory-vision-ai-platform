from fastapi import APIRouter, File, HTTPException, Request, UploadFile

from services.inference.app.schemas.prediction import PredictionResponseSchema

router = APIRouter()


@router.get("/health")
def health_check(request: Request) -> dict:
    runtime = request.app.state.runtime
    return {
        "status": "ok",
        "service": "inference-service",
        "model_checkpoint": str(runtime.model_checkpoint_path),
        "calibration_version": runtime.calibration_config.get("version", "unknown"),
        "confidence_threshold": runtime.confidence_threshold,
    }


@router.post("/predict", response_model=PredictionResponseSchema)
async def predict(request: Request, file: UploadFile = File(...)) -> PredictionResponseSchema:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Uploaded file must have a filename.")

    file_bytes = await file.read()
    if not file_bytes:
        raise HTTPException(status_code=400, detail="Uploaded file is empty.")

    runtime = request.app.state.runtime
    try:
        return runtime.predict_from_bytes(file_bytes)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Inference failed: {exc}") from exc