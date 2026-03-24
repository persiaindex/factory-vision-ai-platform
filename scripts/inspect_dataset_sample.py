from __future__ import annotations

from pathlib import Path

from torch.utils.data import DataLoader

from ml.datasets.collate import detection_collate_fn
from ml.datasets.detection_dataset import BottleDetectionDataset


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    dataset_dir = base_dir / "shared" / "sample_data" / "dataset_v1"

    dataset = BottleDetectionDataset(dataset_dir=dataset_dir, split="train")
    print(f"Dataset length: {len(dataset)}")

    image, target = dataset[0]
    print(f"Single image shape: {tuple(image.shape)}")
    print(f"Single target keys: {list(target.keys())}")
    print(f"Single target boxes shape: {tuple(target['boxes'].shape)}")
    print(f"Single target labels: {target['labels'].tolist()}")

    loader = DataLoader(
        dataset,
        batch_size=2,
        shuffle=False,
        collate_fn=detection_collate_fn,
    )

    images, targets = next(iter(loader))
    print(f"Batch size: {len(images)}")
    print(f"First batched image shape: {tuple(images[0].shape)}")
    print(f"First batched target keys: {list(targets[0].keys())}")
    print(f"First batched target boxes: {targets[0]['boxes']}")


if __name__ == "__main__":
    main()