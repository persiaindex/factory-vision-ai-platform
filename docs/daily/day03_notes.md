# Day 03 Notes

## What I built

- `InspectionJob` model
- `DetectionResult` model
- status choices for jobs and size results
- custom migrations for inspection tables
- Django admin registration for both models
- inline detections inside job admin
- superuser and admin CRUD testing

## What worked

- inspection tables were created in PostgreSQL
- models appeared in Django admin
- I created sample jobs and detections manually
- foreign key relationship worked correctly

## Why this matters

The backend now has a real persistence layer for inspection workflow data.

## Next step

Build the FastAPI inference microservice skeleton and define prediction contracts.