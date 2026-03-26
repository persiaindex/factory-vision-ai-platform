from __future__ import annotations


def bbox_to_dimensions_px(box: list[float]) -> dict:
    x_min, y_min, x_max, y_max = box
    width_px = max(0.0, x_max - x_min)
    height_px = max(0.0, y_max - y_min)
    return {
        "width_px": width_px,
        "height_px": height_px,
    }


def convert_px_to_mm(size_px: float, scale_mm_per_pixel: float) -> float:
    return size_px * scale_mm_per_pixel


def classify_dimension(measured_mm: float, expected_mm: float, tolerance_mm: float) -> str:
    lower_bound = expected_mm - tolerance_mm
    upper_bound = expected_mm + tolerance_mm

    if measured_mm < lower_bound:
        return "UNDER"
    if measured_mm > upper_bound:
        return "OVER"
    return "OK"


def classify_size_status(
    measured_width_mm: float,
    measured_height_mm: float,
    expected_width_mm: float,
    expected_height_mm: float,
    width_tolerance_mm: float,
    height_tolerance_mm: float,
) -> str:
    width_status = classify_dimension(measured_width_mm, expected_width_mm, width_tolerance_mm)
    height_status = classify_dimension(measured_height_mm, expected_height_mm, height_tolerance_mm)

    if width_status == "OK" and height_status == "OK":
        return "OK"
    if width_status == "UNDER" or height_status == "UNDER":
        return "UNDER"
    return "OVER"


def measure_detection(box: list[float], class_name: str, calibration_config: dict) -> dict:
    scale_mm_per_pixel = calibration_config["scale_mm_per_pixel"]
    rules = calibration_config["size_rules"][class_name]

    dimensions_px = bbox_to_dimensions_px(box)
    width_mm = convert_px_to_mm(dimensions_px["width_px"], scale_mm_per_pixel)
    height_mm = convert_px_to_mm(dimensions_px["height_px"], scale_mm_per_pixel)

    size_status = classify_size_status(
        measured_width_mm=width_mm,
        measured_height_mm=height_mm,
        expected_width_mm=rules["expected_width_mm"],
        expected_height_mm=rules["expected_height_mm"],
        width_tolerance_mm=rules["width_tolerance_mm"],
        height_tolerance_mm=rules["height_tolerance_mm"],
    )

    return {
        "estimated_width_mm": width_mm,
        "estimated_height_mm": height_mm,
        "estimated_scale_mm_per_pixel": scale_mm_per_pixel,
        "size_status": size_status,
    }