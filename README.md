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

## Current progress

- [x] Day 01 project skeleton
- [ ] Django backend
- [ ] FastAPI inference service
- [ ] React dashboard
- [ ] training pipeline
- [ ] watcher service
- [ ] full end-to-end integration

## Local setup

```powershell
Copy-Item .env.example .env -Force
docker compose up -d postgres