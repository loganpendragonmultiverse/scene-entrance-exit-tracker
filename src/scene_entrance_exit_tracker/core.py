from __future__ import annotations

import json
from typing import Any

PROJECT = "scene-entrance-exit-tracker"


def _require(data: dict[str, Any], key: str) -> Any:
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _scene_presence(data: dict[str, Any]) -> dict[str, Any]:
    scenes = _require(data, "scenes")
    ids = [str(scene.get("id", "")) for scene in scenes]
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError("scenes need unique non-empty ids")
    prior: set[str] = set()
    rows = []
    for scene in scenes:
        present = set(map(str, scene.get("characters", [])))
        rows.append(
            {
                "scene": str(scene["id"]),
                "present": sorted(present),
                "entered": sorted(present - prior),
                "exited": sorted(prior - present),
            }
        )
        prior = present
    return {"characters": sorted({name for row in rows for name in row["present"]}), "scenes": rows}


def analyze(data: dict[str, Any]) -> dict[str, Any]:
    return {"version": 1, "project": PROJECT, **_scene_presence(data)}


def render_json(report: dict[str, Any]) -> str:
    return json.dumps(report, indent=2, ensure_ascii=False) + "\n"


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# {report['project'].replace('-', ' ').title()} report", ""]
    for key, value in report.items():
        if key not in {"version", "project"}:
            lines.append(f"## {key.replace('_', ' ').title()}")
            lines.append("")
            lines.append(f"```json\n{json.dumps(value, indent=2, ensure_ascii=False)}\n```")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"
