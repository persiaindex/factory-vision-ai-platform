from __future__ import annotations

import json
from datetime import datetime
from pathlib import Path


def create_run_dir(output_root: str | Path) -> Path:
    output_root = Path(output_root)
    output_root.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    run_dir = output_root / f"run_{timestamp}"
    run_dir.mkdir(parents=True, exist_ok=False)
    return run_dir


def write_json(path: str | Path, data: dict) -> None:
    path = Path(path)
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")