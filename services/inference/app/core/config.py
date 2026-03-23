from pathlib import Path
import os

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[4]
load_dotenv(BASE_DIR / ".env")

SERVICE_NAME = "inference-service"
SERVICE_VERSION = "0.1.0"
API_PREFIX = ""
MODEL_DIR = BASE_DIR / "artifacts" / "models" / "current"