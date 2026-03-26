# Day 11 Notes

## What I built

- OpenCV preprocessing helpers
- calibration config file
- calibration loading helper
- measurement and size-status logic
- local measurement pipeline test script
- measurement report output
- calibration notes document

## What worked

- image metadata loaded successfully
- calibration config loaded successfully
- bbox dimensions were converted from pixels to millimeters
- size status was computed correctly according to the rules
- measurement report was saved to `artifacts/reports/`

## Why this matters

The project now has the post-processing layer that turns raw detection boxes into business-ready inspection output.

## Next step

Wire the trained model, preprocessing, and measurement logic into the real FastAPI inference service.