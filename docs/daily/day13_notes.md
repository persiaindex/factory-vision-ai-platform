# Day 13 Notes

## What I built

- Django serializers for jobs and detections
- inference service client helper
- upload orchestration API endpoint
- job list and detail endpoints
- environment-backed inference service URL
- Django-side upload flow test script

## What worked

- Django accepted uploaded images
- an `InspectionJob` was created before inference started
- Django called FastAPI successfully
- detections were persisted in PostgreSQL
- job status and timestamps were updated correctly
- list and detail endpoints returned stored results

## Why this matters

The project now has the backend orchestration layer that connects uploads, inference, persistence, and API responses.

## Next step

Build the watcher service that monitors `shared/input/` and uploads files automatically.