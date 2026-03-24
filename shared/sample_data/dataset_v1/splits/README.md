# Dataset V1

Starter object detection dataset for the Factory Vision AI Platform.

## Current class scope

- bottle

## Folder structure

```text
dataset_v1/
├── images/
├── annotations/
├── splits/
│   ├── train.txt
│   └── val.txt
├── examples/
├── label_map.json
├── DATASET_RULES.md
└── README.md
```

## Pairing rule

Each image must have one JSON annotation file with the same base name.

Example:

- `images/image_001.jpg`
- `annotations/image_001.json`

## Annotation structure

Each JSON file contains:

- image file name
- image width
- image height
- object list
- bounding boxes in pixel corner format

## Split format

The `train.txt` and `val.txt` files contain sample ids without extensions.