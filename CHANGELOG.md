# Changelog

## Unreleased

- Fix path resolution to allow running `main.py` from any working directory. Previously, relative paths like `./commands` and `./config` required the script to be run from the py_frame directory. Now uses `SCRIPT_DIR` (based on `__file__`) for absolute path resolution.
- Fix `ConfigLoader` to use absolute paths based on `_PYFRAME_ROOT` instead of relative paths.
- **Fix log file path resolution** (`classes/base/Log.py`): Log `file_path` in `debug.py` configs is now always resolved relative to the py_frame root directory (via `_PY_FRAME_ROOT` = `__file__` 3 levels up), not relative to CWD. Prevents `output/` log directories from being created wherever `main.py` is invoked from.
