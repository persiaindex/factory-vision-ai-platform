from __future__ import annotations

import torch


def build_optimizer(model, learning_rate: float, momentum: float, weight_decay: float):
    trainable_params = [param for param in model.parameters() if param.requires_grad]
    return torch.optim.SGD(
        trainable_params,
        lr=learning_rate,
        momentum=momentum,
        weight_decay=weight_decay,
    )