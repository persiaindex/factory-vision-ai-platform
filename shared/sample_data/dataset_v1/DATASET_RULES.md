# Dataset Rules

## Image rules

- allowed formats: `.jpg`, `.jpeg`, `.png`
- each image must have exactly one annotation JSON file with the same base name
- image file names should use lowercase letters, numbers, and underscores only
- example: `image_001.jpg`

## Annotation rules

- JSON file must have the same base name as the image
- example: `image_001.json`
- `image_filename` must match the real image file name exactly
- `image_width` and `image_height` must match the real image size
- `objects` may contain one or more labeled objects
- each object must have a valid `class_name`
- each object must have a valid bounding box

## Bounding box rules

- `x_min < x_max`
- `y_min < y_max`
- all coordinates must stay inside image bounds
- bounding boxes use pixel coordinates
- no negative coordinates

## Current allowed classes

- `bottle`