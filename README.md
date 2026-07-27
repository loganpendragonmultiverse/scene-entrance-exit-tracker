# Scene Entrance/Exit Tracker

[![CI](https://github.com/loganpendragonmultiverse/scene-entrance-exit-tracker/actions/workflows/ci.yml/badge.svg)](https://github.com/loganpendragonmultiverse/scene-entrance-exit-tracker/actions/workflows/ci.yml)

Build a scene-by-scene character presence matrix and explicit entrance and exit transitions. The command runs locally, uses explicit UTF-8 JSON input, and produces deterministic JSON or Markdown reports without modifying the supplied source material.

## Three-minute start

```bash
python -m pip install .
scene-presence examples/sample.json
scene-presence examples/sample.json --format json --output report.json
```

The example documents the complete input shape. Version 1.1 adds per-character scene/transition summaries, a total transition count, and explicit warnings for empty scene rosters. Markdown is intended for immediate review; JSON preserves structured evidence for scripts and later comparison. An existing output file is never overwritten.

## Privacy and platforms

All scene data stays local.

Python 3.10 or newer is supported on Windows, macOS, and Linux. The package has no runtime dependencies, telemetry, account, or hosted service.

## Interpretation boundary

The tracker uses supplied scene rosters. It does not infer physical presence from prose or decide whether off-page characters count.

## Development

```bash
python -m pip install -e ".[dev]"
ruff format --check .
ruff check .
mypy src
pytest
python -m build
```

The project is feature-complete for its documented v1 scope. Maintenance focuses on correctness, security, compatibility, and well-supported input improvements.

Part of the [Logan Pendragon Forge open-source collection](https://www.loganpendragonforge.com/open-source/). Licensed under the [MIT License](LICENSE).
