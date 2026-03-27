# Day 14 Notes

## What I built

- watcher service under `services/watcher`
- watcher config loader
- Django upload client helper
- file-processing logic with success delete and failure move
- polling watcher loop
- file-drop smoke test script

## What worked

- watcher detected new files in `shared/input/`
- watcher uploaded files to Django successfully
- files were deleted only after successful upload
- failed uploads moved files into `shared/input_failed/`
- watcher logs clearly showed each action

## Why this matters

The project now supports automatic file-based ingestion instead of only manual upload requests.

## Next step

Run the complete happy path and verify the full end-to-end system.