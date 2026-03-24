# Dataset Loader

Custom PyTorch dataset loader for the Factory Vision AI Platform.

## Current scope

- loads `dataset_v1`
- parses image + JSON annotation pairs
- returns torchvision-style detection targets
- supports train and validation splits

## Current target keys

- `boxes`
- `labels`
- `image_id`
- `area`
- `iscrowd`