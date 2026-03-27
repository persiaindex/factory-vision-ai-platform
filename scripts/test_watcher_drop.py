from __future__ import annotations

import shutil
from pathlib import Path


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    source_path = base_dir / "shared" / "sample_data" / "dataset_v1" / "images" / "image_001.jpg"
    target_dir = base_dir / "shared" / "input"
    target_dir.mkdir(parents=True, exist_ok=True)
    target_path = target_dir / source_path.name

    shutil.copy2(source_path, target_path)
    print(f"Copied sample image into watcher input folder: {target_path}")


if __name__ == "__main__":
    main()