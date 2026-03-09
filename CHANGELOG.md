# Changelog

## Unreleased

- Fix path resolution to allow running `main.py` from any working directory. Previously, relative paths like `./commands` and `./config` required the script to be run from the py_frame directory. Now uses `SCRIPT_DIR` (based on `__file__`) for absolute path resolution.
- Fix `ConfigLoader` to use absolute paths based on `_PYFRAME_ROOT` instead of relative paths.
