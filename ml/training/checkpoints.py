from __future__ import annotations

import shutil
from pathlib import Path

import torch


def save_checkpoint(path: str | Path, model, optimizer, epoch: int, config: dict) -> None:
    path = Path(path)
    torch.save(
        {
            "model_state_dict": model.state_dict(),
            "optimizer_state_dict": optimizer.state_dict(),
            "epoch": epoch,
            "config": config,
        },
        path,
    )


def promote_to_current(run_checkpoint_path: str | Path, current_model_dir: str | Path) -> Path:
    run_checkpoint_path = Path(run_checkpoint_path)
    current_model_dir = Path(current_model_dir)
    current_model_dir.mkdir(parents=True, exist_ok=True)

    target_path = current_model_dir / "model.pt"
    shutil.copy2(run_checkpoint_path, target_path)
    return target_path