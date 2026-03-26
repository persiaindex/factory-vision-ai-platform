# Current Active Model

This folder contains the currently active model artifact used by downstream services.

## Files

- `model.pt` — active checkpoint
- `model_info.json` — metadata about the active model

## Rule

Training runs save versioned outputs under `artifacts/runs/`.

Only the model currently selected for serving should be copied here.