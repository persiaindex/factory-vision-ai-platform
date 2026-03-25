from __future__ import annotations

from pathlib import Path

import torch

from ml.datasets.build import build_detection_dataloader
from ml.training.artifacts import create_run_dir, write_json
from ml.training.config import TrainingConfig
from ml.training.model_factory import build_detection_model
from ml.utils.seed import set_seed


def main() -> None:
    base_dir = Path(__file__).resolve().parents[2]
    config = TrainingConfig.default(base_dir)

    set_seed(config.seed)

    run_dir = create_run_dir(config.output_root)
    write_json(run_dir / "config_snapshot.json", config.to_dict())

    train_dataset, train_loader = build_detection_dataloader(
        dataset_dir=config.dataset_dir,
        split=config.train_split,
        batch_size=config.batch_size,
        shuffle=True,
        num_workers=config.num_workers,
    )

    val_dataset, val_loader = build_detection_dataloader(
        dataset_dir=config.dataset_dir,
        split=config.val_split,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=config.num_workers,
    )

    model = build_detection_model(num_classes=config.num_classes)
    device = torch.device(config.device)
    model.to(device)

    first_images, first_targets = next(iter(train_loader))

    setup_report = {
        "status": "ok",
        "run_dir": str(run_dir),
        "device": str(device),
        "model_name": config.model_name,
        "train_dataset_size": len(train_dataset),
        "val_dataset_size": len(val_dataset),
        "batch_size": config.batch_size,
        "num_workers": config.num_workers,
        "first_batch_num_images": len(first_images),
        "first_image_shape": list(first_images[0].shape),
        "first_target_keys": list(first_targets[0].keys()),
        "first_target_num_boxes": int(first_targets[0]["boxes"].shape[0]),
    }

    write_json(run_dir / "training_setup_report.json", setup_report)

    print("Training pipeline setup completed successfully.")
    print(f"Run directory: {run_dir}")
    print(f"Train dataset size: {len(train_dataset)}")
    print(f"Validation dataset size: {len(val_dataset)}")
    print(f"First image shape: {tuple(first_images[0].shape)}")
    print(f"First target keys: {list(first_targets[0].keys())}")


if __name__ == "__main__":
    main()