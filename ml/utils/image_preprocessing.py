from __future__ import annotations

import cv2
import numpy as np


def read_image_bgr(image_path: str) -> np.ndarray:
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not read image: {image_path}")
    return image


def bgr_to_rgb(image_bgr: np.ndarray) -> np.ndarray:
    return cv2.cvtColor(image_bgr, cv2.COLOR_BGR2RGB)


def resize_for_visualization(image: np.ndarray, max_width: int = 960) -> np.ndarray:
    height, width = image.shape[:2]
    if width <= max_width:
        return image

    scale = max_width / width
    new_size = (int(width * scale), int(height * scale))
    return cv2.resize(image, new_size, interpolation=cv2.INTER_AREA)


def prepare_image_report(image_bgr: np.ndarray) -> dict:
    height, width = image_bgr.shape[:2]
    return {
        "image_width_px": width,
        "image_height_px": height,
        "channels": image_bgr.shape[2] if image_bgr.ndim == 3 else 1,
    }