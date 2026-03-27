# Factory Vision AI Platform

Production-style industrial computer vision portfolio project.

## Goal

Train a PyTorch detector from raw images, watch an input folder, send images to Django, run inference through FastAPI, store results in PostgreSQL, and show them in a React dashboard.

## Planned stack

- React
- Django
- FastAPI
- PostgreSQL
- PyTorch
- OpenCV
- Docker Compose

## Why this project matters

This project demonstrates an end-to-end AI engineering workflow:

- model training with PyTorch
- model serving with FastAPI
- backend orchestration with Django
- PostgreSQL persistence
- watcher-based file ingestion
- frontend visualization with React
- practical computer vision post-processing with OpenCV

A new image can be dropped into an input folder, processed automatically, stored as an inspection job, and then displayed in a live dashboard with image, detections, and status.

## Architecture Diagram

```text
shared/input/ 
    ↓
watcher service
    ↓
Django upload endpoint
    ↓
InspectionJob stored in PostgreSQL
    ↓
FastAPI inference service
    ↓
DetectionResult stored in PostgreSQL
    ↓
React dashboard polling `/api/inspections/jobs/`
```

## Current progress

- [x] Day 01 project skeleton
- [x] Day 02 Django backend bootstrap
- [x] Day 03 inspection data model and admin
- [x] Day 04 FastAPI inference service skeleton
- [x] Day 05 React dashboard skeleton
- [x] Day 06 dataset format and sample data
- [x] Day 07 PyTorch dataset loader
- [x] Day 08 training pipeline skeleton
- [x] Day 09 first CPU detector training
- [x] Day 10 evaluation and artifact versioning
- [x] Day 11 preprocessing and calibration logic
- [x] Day 12 real FastAPI inference
- [x] Day 13 Django upload endpoint and service call
- [x] Day 14 watcher service
- [x] Day 15 end-to-end happy path
- [x] Day 16 portfolio polish and demo readiness
- [x] Day 17 Docker packaging and one-command startup

## Core roadmap status

The 15-day core roadmap is complete.

Optional polish work continues after Day 15 and focuses on documentation quality, UI polish, demo readiness, and portfolio presentation.

## Local setup

```powershell
Copy-Item .env.example .env -Force
docker compose up -d postgres
```

## Docker Compose startup

To start the packaged stack:

```powershell
cp .env.example .env
# adjust values if needed

docker compose up --build
```

Main local URLs:

- Django: `http://127.0.0.1:8000`
- FastAPI: `http://127.0.0.1:8001/docs`
- React: `http://localhost:3000`
