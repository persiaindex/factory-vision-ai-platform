# Architecture Overview

## Services

- Django API: receives uploads, creates jobs, stores results, serves frontend-facing endpoints
- FastAPI inference service: loads active model and returns predictions
- Watcher service: monitors input folder and uploads new images to Django
- React frontend: displays latest inspection and history
- PostgreSQL: stores jobs, detections, and audit information

## Shared directories

- `shared/input/`: folder watched for incoming images
- `shared/media/`: persisted uploaded images
- `artifacts/models/current/`: currently active trained model and metadata

## Main runtime flow

1. Train a model from labeled images.
2. Save artifacts into `artifacts/models/current/`.
3. Watcher sees a new image in `shared/input/`.
4. Watcher uploads image to Django.
5. Django stores job and image.
6. Django sends image to FastAPI.
7. FastAPI returns detections.
8. Django stores results.
9. React displays latest result and history.