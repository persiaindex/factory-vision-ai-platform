# Day 10 Notes

## What I built

- checkpoint loading helper
- IoU-based evaluation helpers
- qualitative prediction visualization helper
- evaluation entry point
- evaluation report JSON
- active model metadata update with evaluation info

## What worked

- the trained model reloaded successfully
- evaluation ran on the validation split
- qualitative images were saved
- evaluation metrics were written to JSON
- the active model folder now contains richer metadata

## Why this matters

The project now has inspectable validation output and a clearer model artifact package instead of only a raw checkpoint.

## Next step

Add preprocessing and calibration logic for size estimation.