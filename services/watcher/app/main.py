from __future__ import annotations

import time
from pathlib import Path

from .config import ALLOWED_EXTENSIONS, WATCHER_INPUT_DIR, WATCHER_POLL_SECONDS
from .processor import process_file


def iter_candidate_files(input_dir: Path):
    input_dir.mkdir(parents=True, exist_ok=True)
    for path in sorted(input_dir.iterdir()):
        if path.is_file() and path.suffix.lower() in ALLOWED_EXTENSIONS:
            yield path


def main() -> None:
    print(f"Watcher started. Monitoring: {WATCHER_INPUT_DIR}")
    print(f"Polling interval: {WATCHER_POLL_SECONDS} seconds")

    while True:
        try:
            candidate_files = list(iter_candidate_files(WATCHER_INPUT_DIR))

            for file_path in candidate_files:
                print(f"[watcher] Found file: {file_path.name}")
                result = process_file(file_path)
                print(f"[watcher] status={result.status} message={result.message}")

            time.sleep(WATCHER_POLL_SECONDS)
        except Exception as exc:
            print(f"[watcher] loop_error={exc}")
            time.sleep(WATCHER_POLL_SECONDS)


if __name__ == "__main__":
    main()