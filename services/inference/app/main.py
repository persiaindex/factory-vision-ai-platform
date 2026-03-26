from __future__ import annotations

from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI

from services.inference.app.api.routes import router
from services.inference.app.services.predictor import InferenceRuntime


@asynccontextmanager
async def lifespan(app: FastAPI):
    base_dir = Path(__file__).resolve().parents[3]
    app.state.runtime = InferenceRuntime(
        base_dir=base_dir,
        device_name="cpu",
        confidence_threshold=0.1,
    )
    yield


app = FastAPI(
    title="inference-service",
    version="0.2.0",
    description="Real inference microservice for industrial computer vision predictions.",
    lifespan=lifespan,
)

app.include_router(router)