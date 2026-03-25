from __future__ import annotations

from typing import Any

import torch


def train_one_epoch(model, optimizer, data_loader, device: torch.device) -> dict[str, Any]:
    model.train()
    running_loss = 0.0
    num_batches = 0

    for images, targets in data_loader:
        images = [image.to(device) for image in images]
        targets = [
            {key: value.to(device) for key, value in target.items()}
            for target in targets
        ]

        loss_dict = model(images, targets)
        total_loss = sum(loss for loss in loss_dict.values())

        optimizer.zero_grad()
        total_loss.backward()
        optimizer.step()

        running_loss += float(total_loss.item())
        num_batches += 1

    average_loss = running_loss / max(num_batches, 1)

    return {
        "num_batches": num_batches,
        "average_total_loss": average_loss,
    }