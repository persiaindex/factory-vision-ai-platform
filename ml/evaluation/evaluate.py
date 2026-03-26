from __future__ import annotations

from pathlib import Path

import torch

from ml.datasets.build import build_detection_dataloader
from ml.evaluation.metrics import evaluate_image_predictions, summarize_counts
from ml.evaluation.visualization import save_prediction_visualization
from ml.training.artifacts import create_run_dir, write_json
from ml.training.config import TrainingConfig
from ml.training.model_factory import load_trained_detection_model


def main() -> None:
    base_dir = Path(__file__).resolve().parents[2]
    config = TrainingConfig.default(base_dir)
    device = torch.device(config.device)

    _, val_loader = build_detection_dataloader(
        dataset_dir=config.dataset_dir,
        split=config.val_split,
        batch_size=1,
        shuffle=False,
        num_workers=config.num_workers,
    )

    current_model_dir = base_dir / "artifacts" / "models" / "current"
    checkpoint_path = current_model_dir / "model.pt"
    model = load_trained_detection_model(
        checkpoint_path=checkpoint_path,
        num_classes=config.num_classes,
        device=device,
    )

    run_dir = create_run_dir(config.output_root)
    evaluation_dir = run_dir / "evaluation"
    visuals_dir = evaluation_dir / "visuals"
    visuals_dir.mkdir(parents=True, exist_ok=True)

    confidence_threshold = 0.1
    total_tp = 0
    total_fp = 0
    total_fn = 0
    per_image_results = []

    with torch.no_grad():
        for image_index, (images, targets) in enumerate(val_loader):
            image = images[0].to(device)
            target = targets[0]

            outputs = model([image])
            output = outputs[0]

            pred_boxes = []
            pred_scores = []
            for box, score, label in zip(output["boxes"], output["scores"], output["labels"]):
                if int(label.item()) != 1:
                    continue
                if float(score.item()) < confidence_threshold:
                    continue
                pred_boxes.append(box.cpu().tolist())
                pred_scores.append(float(score.item()))

            gt_boxes = target["boxes"].cpu().tolist()
            counts = evaluate_image_predictions(pred_boxes=pred_boxes, gt_boxes=gt_boxes, iou_threshold=0.5)

            total_tp += counts["true_positives"]
            total_fp += counts["false_positives"]
            total_fn += counts["false_negatives"]

            per_image_results.append(
                {
                    "image_index": image_index,
                    "num_predictions": len(pred_boxes),
                    "num_ground_truth_boxes": len(gt_boxes),
                    **counts,
                }
            )

            save_prediction_visualization(
                image_tensor=images[0],
                pred_boxes=pred_boxes,
                pred_scores=pred_scores,
                gt_boxes=gt_boxes,
                output_path=visuals_dir / f"val_sample_{image_index:03d}.png",
            )

    summary = summarize_counts(total_tp, total_fp, total_fn)
    evaluation_report = {
        "status": "ok",
        "checkpoint_path": str(checkpoint_path),
        "confidence_threshold": confidence_threshold,
        "iou_threshold": 0.5,
        "total_true_positives": total_tp,
        "total_false_positives": total_fp,
        "total_false_negatives": total_fn,
        **summary,
        "per_image_results": per_image_results,
        "visuals_dir": str(visuals_dir),
    }

    write_json(evaluation_dir / "evaluation_report.json", evaluation_report)

    write_json(
        current_model_dir / "model_info.json",
        {
            **evaluation_report,
            "model_name": config.model_name,
            "num_classes": config.num_classes,
            "active_checkpoint": str(checkpoint_path),
        },
    )

    print("Evaluation completed successfully.")
    print(f"Precision: {summary['precision']:.4f}")
    print(f"Recall: {summary['recall']:.4f}")
    print(f"F1: {summary['f1']:.4f}")
    print(f"Evaluation report: {evaluation_dir / 'evaluation_report.json'}")


if __name__ == "__main__":
    main()