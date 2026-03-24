from __future__ import annotations

from pathlib import Path

from torch.utils.data import DataLoader

from ml.datasets.collate import detection_collate_fn
from ml.datasets.detection_dataset import BottleDetectionDataset


def build_detection_dataloader(
    dataset_dir: str | Path,
    split: str,
    batch_size: int,
    shuffle: bool,
    num_workers: int = 0,
):
    dataset = BottleDetectionDataset(dataset_dir=dataset_dir, split=split)
    loader = DataLoader(
        dataset,
        batch_size=batch_size,
        shuffle=shuffle,
        num_workers=num_workers,
        collate_fn=detection_collate_fn,
    )
    return dataset, loader