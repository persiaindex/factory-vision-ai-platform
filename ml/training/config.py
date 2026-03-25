from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass
class TrainingConfig:
    dataset_dir: str
    train_split: str = "train"
    val_split: str = "val"
    num_classes: int = 2
    batch_size: int = 2
    num_workers: int = 0
    learning_rate: float = 0.001
    momentum: float = 0.9
    weight_decay: float = 0.0005
    num_epochs: int = 3
    seed: int = 42
    device: str = "cpu"
    model_name: str = "fasterrcnn_mobilenet_v3_large_320_fpn"
    use_pretrained_weights: bool = True
    output_root: str = "artifacts/runs"
    current_model_dir: str = "artifacts/models/current"

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def default(cls, base_dir: Path) -> "TrainingConfig":
        return cls(
            dataset_dir=str(base_dir / "shared" / "sample_data" / "dataset_v1"),
            output_root=str(base_dir / "artifacts" / "runs"),
            current_model_dir=str(base_dir / "artifacts" / "models" / "current"),
        )