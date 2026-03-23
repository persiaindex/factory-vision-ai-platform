from fastapi import FastAPI

from app.api.routes import router
from app.core.config import API_PREFIX, SERVICE_NAME, SERVICE_VERSION

app = FastAPI(
    title=SERVICE_NAME,
    version=SERVICE_VERSION,
    description="Inference microservice for industrial computer vision predictions.",
)

app.include_router(router, prefix=API_PREFIX)