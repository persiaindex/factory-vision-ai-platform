# Day 12 Notes

## What I built

- real FastAPI inference runtime
- startup-time model and calibration loading
- real `/predict` endpoint using the trained model
- OpenCV byte decoding for uploaded images
- confidence filtering and measurement logic integration
- local API smoke test script

## What worked

- FastAPI started successfully from the repo root
- `/health` reported model and calibration metadata
- `/predict` accepted an uploaded image
- the service returned real detections with estimated dimensions and size status
- the smoke test script successfully called the API

## Why this matters

The project now has a real ML-backed inference microservice instead of a stub response.

## Next step

Connect Django upload handling to the inference service and persist results.