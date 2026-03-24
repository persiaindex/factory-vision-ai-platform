from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches

from ml.datasets.detection_dataset import BottleDetectionDataset


def main() -> None:
    base_dir = Path(__file__).resolve().parents[1]
    dataset_dir = base_dir / "shared" / "sample_data" / "dataset_v1"

    dataset = BottleDetectionDataset(dataset_dir=dataset_dir, split="train")
    image, target = dataset[0]

    image_np = image.permute(1, 2, 0).numpy()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(image_np)

    for box, label in zip(target["boxes"], target["labels"]):
        x_min, y_min, x_max, y_max = box.tolist()
        width = x_max - x_min
        height = y_max - y_min

        rect = patches.Rectangle(
            (x_min, y_min),
            width,
            height,
            linewidth=2,
            edgecolor="red",
            facecolor="none",
        )
        ax.add_patch(rect)
        ax.text(x_min, y_min - 5, f"label={int(label)}", fontsize=10, bbox={"facecolor": "white", "alpha": 0.8})

    ax.set_title("Dataset sample visualization")
    ax.axis("off")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()