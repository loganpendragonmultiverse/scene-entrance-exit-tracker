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

## Version 1.2.0

Each scene may supply ordered `events`, for example `[{"action":"exit","character":"Mara"},{"action":"enter","character":"Ivo"}]`. `characters` is the initial roster; events produce `end_present`, which becomes the prior roster for the next scene. Entering a present character or exiting an absent one is rejected. Re-entry after an exit is valid. Summaries count each transition and each scene occupied at least once; `present` remains the initial roster. Omitted events retain legacy output.

## Version 1.2.1: documentation correction

Version 1.2.0 was released on October 15, 2026. Version 1.2.1 corrects its release labels without changing behavior. The original v1.2.0 tag and downloadable artifacts remain unchanged; use v1.2.1 for the corrected packaged documentation.

## Explicit identities (1.2.2)

Scene IDs and character names must be nonempty strings with no surrounding
whitespace. Names are case-sensitive; duplicate names within one initial roster
are rejected rather than silently collapsed. Event identities follow the same
rules, so malformed or padded identities are refused. Names remain explicit and
case-sensitive; spelling and identity resolution are the author's responsibility.
Malformed roots and scene records produce actionable errors. Ordered re-entry,
initial rosters, end rosters and prior-scene transitions retain their documented
meaning. Output files are created exclusively.

Installed packages include documents and `examples/sample.json` under
`share/doc/scene-entrance-exit-tracker/` in the Python environment, whose root
is printed by `python -c "import sys; print(sys.prefix)"`.

Existing output paths, including dangling symbolic links, are refused before
exclusive file creation. This protects ordinary output collisions; it does not
promise protection against hostile concurrent file-system changes.
