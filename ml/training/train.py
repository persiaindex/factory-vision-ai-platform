from __future__ import annotations

from pathlib import Path

import torch

from ml.datasets.build import build_detection_dataloader
from ml.training.artifacts import create_run_dir, write_json
from ml.training.checkpoints import promote_to_current, save_checkpoint
from ml.training.config import TrainingConfig
from ml.training.engine import train_one_epoch
from ml.training.model_factory import build_detection_model
from ml.training.optim import build_optimizer
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

    val_dataset, _ = build_detection_dataloader(
        dataset_dir=config.dataset_dir,
        split=config.val_split,
        batch_size=config.batch_size,
        shuffle=False,
        num_workers=config.num_workers,
    )

    device = torch.device(config.device)

    model = build_detection_model(
        num_classes=config.num_classes,
        use_pretrained_weights=config.use_pretrained_weights,
    )
    model.to(device)

    optimizer = build_optimizer(
        model=model,
        learning_rate=config.learning_rate,
        momentum=config.momentum,
        weight_decay=config.weight_decay,
    )

    epoch_logs = []

    for epoch in range(1, config.num_epochs + 1):
        epoch_result = train_one_epoch(
            model=model,
            optimizer=optimizer,
            data_loader=train_loader,
            device=device,
        )
        epoch_result["epoch"] = epoch
        epoch_logs.append(epoch_result)
        print(f"Epoch {epoch}/{config.num_epochs} - average loss: {epoch_result['average_total_loss']:.4f}")

    run_checkpoint_path = run_dir / "model.pt"
    save_checkpoint(
        path=run_checkpoint_path,
        model=model,
        optimizer=optimizer,
        epoch=config.num_epochs,
        config=config.to_dict(),
    )

    current_model_path = promote_to_current(
        run_checkpoint_path=run_checkpoint_path,
        current_model_dir=config.current_model_dir,
    )

    training_summary = {
        "status": "ok",
        "device": str(device),
        "model_name": config.model_name,
        "use_pretrained_weights": config.use_pretrained_weights,
        "train_dataset_size": len(train_dataset),
        "val_dataset_size": len(val_dataset),
        "num_epochs": config.num_epochs,
        "epoch_logs": epoch_logs,
        "run_checkpoint_path": str(run_checkpoint_path),
        "current_model_path": str(current_model_path),
    }

    write_json(run_dir / "training_summary.json", training_summary)
    write_json(
        Path(config.current_model_dir) / "model_info.json",
        {
            "model_name": config.model_name,
            "num_classes": config.num_classes,
            "use_pretrained_weights": config.use_pretrained_weights,
            "checkpoint_path": str(current_model_path),
            "source_run_dir": str(run_dir),
            "num_epochs": config.num_epochs,
            "device": str(device),
        },
    )

    print("Training completed successfully.")
    print(f"Run checkpoint: {run_checkpoint_path}")
    print(f"Current model path: {current_model_path}")


if __name__ == "__main__":
    main()