from __future__ import annotations


def detection_collate_fn(batch):
    return tuple(zip(*batch))