# Day 04 Notes

## What I built

- FastAPI inference service skeleton
- clean app folder structure
- `/health` endpoint
- `/predict` stub endpoint
- request and response schemas
- stub predictor service function
- service README

## What worked

- FastAPI started successfully
- `/health` returned service metadata
- Swagger UI loaded
- `/predict` accepted a file and returned a structured stub response

## Why this matters

The project now has a real inference service boundary instead of mixing ML-serving logic into Django.

## Next step

Connect real preprocessing and model inference logic.