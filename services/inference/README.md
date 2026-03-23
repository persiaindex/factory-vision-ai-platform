# Inference Service

FastAPI microservice for computer vision inference.

## Current scope

- `/health` endpoint
- `/predict` stub endpoint
- request/response schema foundation

## Planned future scope

- load PyTorch model from `artifacts/models/current/`
- preprocess images with OpenCV
- run inference
- return structured detections