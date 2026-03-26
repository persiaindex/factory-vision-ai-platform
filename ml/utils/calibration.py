from __future__ import annotations

import json
from pathlib import Path


def load_calibration_config(config_path: str | Path) -> dict:
    config_path = Path(config_path)
    if not config_path.exists():
        raise FileNotFoundError(f"Calibration config not found: {config_path}")
    return json.loads(config_path.read_text(encoding="utf-8"))