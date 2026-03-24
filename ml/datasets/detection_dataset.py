from __future__ import annotations

import json
from pathlib import Path
from typing import Callable

import torch
from PIL import Image
from torch.utils.data import Dataset
from torchvision.transforms import functional as F


class BottleDetectionDataset(Dataset):
    def __init__(
        self,
        dataset_dir: str | Path,
        split: str,
        transforms: Callable | None = None,
    ) -> None:
        self.dataset_dir = Path(dataset_dir)
        self.images_dir = self.dataset_dir / "images"
        self.annotations_dir = self.dataset_dir / "annotations"
        self.splits_dir = self.dataset_dir / "splits"
        self.transforms = transforms

        self.label_map = json.loads((self.dataset_dir / "label_map.json").read_text(encoding="utf-8"))
        self.sample_ids = self._load_split_ids(split)

    def _load_split_ids(self, split: str) -> list[str]:
        split_path = self.splits_dir / f"{split}.txt"
        if not split_path.exists():
            raise FileNotFoundError(f"Split file not found: {split_path}")

        sample_ids = [line.strip() for line in split_path.read_text(encoding="utf-8").splitlines() if line.strip()]
        if not sample_ids:
            raise ValueError(f"Split file is empty: {split_path}")
        return sample_ids

    def _find_image_path(self, sample_id: str) -> Path:
        candidates = []
        for extension in [".jpg", ".jpeg", ".png"]:
            image_path = self.images_dir / f"{sample_id}{extension}"
            if image_path.exists():
                candidates.append(image_path)

        if len(candidates) != 1:
            raise FileNotFoundError(
                f"Expected exactly one image file for sample '{sample_id}', found {len(candidates)}"
            )

        return candidates[0]

    def __len__(self) -> int:
        return len(self.sample_ids)

    def __getitem__(self, index: int):
        sample_id = self.sample_ids[index]
        image_path = self._find_image_path(sample_id)
        annotation_path = self.annotations_dir / f"{sample_id}.json"

        if not annotation_path.exists():
            raise FileNotFoundError(f"Annotation file not found: {annotation_path}")

        image = Image.open(image_path).convert("RGB")
        annotation = json.loads(annotation_path.read_text(encoding="utf-8"))

        boxes = []
        labels = []
        areas = []

        for obj in annotation["objects"]:
            bbox = obj["bbox"]
            x_min = float(bbox["x_min"])
            y_min = float(bbox["y_min"])
            x_max = float(bbox["x_max"])
            y_max = float(bbox["y_max"])

            boxes.append([x_min, y_min, x_max, y_max])
            labels.append(self.label_map[obj["class_name"]])
            areas.append((x_max - x_min) * (y_max - y_min))

        boxes_tensor = torch.tensor(boxes, dtype=torch.float32)
        labels_tensor = torch.tensor(labels, dtype=torch.int64)
        area_tensor = torch.tensor(areas, dtype=torch.float32)
        iscrowd_tensor = torch.zeros((len(boxes),), dtype=torch.int64)

        target = {
            "boxes": boxes_tensor,
            "labels": labels_tensor,
            "image_id": torch.tensor([index], dtype=torch.int64),
            "area": area_tensor,
            "iscrowd": iscrowd_tensor,
        }

        image_tensor = F.pil_to_tensor(image).float() / 255.0

        if self.transforms is not None:
            image_tensor, target = self.transforms(image_tensor, target)

        return image_tensor, target