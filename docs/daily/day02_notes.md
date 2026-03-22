# Day 02 Notes

## What I built

- Django project inside `apps/api`
- split settings package
- PostgreSQL-backed Django configuration
- `core` app with health endpoint
- `inspections` app placeholder for domain logic
- successful Django migrations

## What worked

- Django server started successfully
- `/health/` returned JSON
- PostgreSQL tables were created by migrations

## Why this matters

The project now has a real backend service instead of only infrastructure.

## Next step

Design inspection data models and register them in admin.