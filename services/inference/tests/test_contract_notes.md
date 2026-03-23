# Inference Contract Notes

## Current endpoints

- `GET /health`
- `POST /predict`

## Current predict behavior

- accepts one uploaded file
- returns stub detection payload
- response contract already matches future Django persistence fields

## Next step

Replace stub logic with real model loading and inference.