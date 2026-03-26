from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as patches


def save_prediction_visualization(image_tensor, pred_boxes, pred_scores, gt_boxes, output_path: str | Path) -> None:
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    image_np = image_tensor.permute(1, 2, 0).cpu().numpy()

    fig, ax = plt.subplots(figsize=(8, 6))
    ax.imshow(image_np)

    for box in gt_boxes:
        x_min, y_min, x_max, y_max = box
        rect = patches.Rectangle(
            (x_min, y_min),
            x_max - x_min,
            y_max - y_min,
            linewidth=2,
            edgecolor="green",
            facecolor="none",
        )
        ax.add_patch(rect)

    for box, score in zip(pred_boxes, pred_scores):
        x_min, y_min, x_max, y_max = box
        rect = patches.Rectangle(
            (x_min, y_min),
            x_max - x_min,
            y_max - y_min,
            linewidth=2,
            edgecolor="red",
            facecolor="none",
        )
        ax.add_patch(rect)
        ax.text(x_min, max(0, y_min - 5), f"pred {score:.2f}", fontsize=9, bbox={"facecolor": "white", "alpha": 0.8})

    ax.set_title("Green = ground truth, Red = prediction")
    ax.axis("off")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150)
    plt.close(fig)