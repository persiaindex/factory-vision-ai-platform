# Final Demo Checklist

## Services Running

- Django backend
- FastAPI inference service
- watcher service
- React frontend
- PostgreSQL container

## Happy Path Demo

1. Drop a sample image into `shared/input/`
2. Watch the watcher upload it automatically
3. Confirm the input file is removed after success
4. Confirm a new `InspectionJob` is created in Django
5. Confirm detections are stored in PostgreSQL
6. Confirm the React dashboard updates automatically
7. Confirm the latest image is visible on the dashboard
8. Confirm the job appears in recent history