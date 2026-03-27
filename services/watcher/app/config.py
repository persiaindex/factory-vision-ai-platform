from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")

WATCHER_INPUT_DIR = BASE_DIR / os.getenv("WATCHER_INPUT_DIR", "shared/input")
WATCHER_FAILED_DIR = BASE_DIR / os.getenv("WATCHER_FAILED_DIR", "shared/input_failed")
WATCHER_API_URL = os.getenv("WATCHER_API_URL", "http://127.0.0.1:8000/api/inspections/upload/")
WATCHER_POLL_SECONDS = int(os.getenv("WATCHER_POLL_SECONDS", "2"))
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png"}