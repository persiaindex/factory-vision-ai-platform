# Troubleshooting Guide

## Admin page has no CSS

Check:

- `STATIC_URL = "/static/"`
- the browser can open `/static/admin/css/base.css`

## Django cannot connect to PostgreSQL

If Django runs locally and PostgreSQL runs in Docker, use:

```env
POSTGRES_HOST=localhost
```

Do not use `postgres` unless Django also runs inside Docker.

## `ModuleNotFoundError: No module named 'ml'`

Run project scripts from the repository root with module execution:

```powershell
python -m scripts.inspect_dataset_sample
```

## FastAPI cannot find model artifacts

Check the repo-root path logic in `services/inference/app/main.py` and confirm the active model exists under:

```text
artifacts/models/current/
```

## Watcher crashes when backend services are down

Use the resilient watcher client and processor versions from Day 14 so request errors are caught and files are moved to `shared/input_failed/`.