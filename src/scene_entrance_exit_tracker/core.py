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
    if not isinstance(scenes, list):
        raise TypeError("scenes must be a list")
    ids = [str(scene.get("id", "")) for scene in scenes]
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError("scenes need unique non-empty ids")
    prior: set[str] = set()
    rows = []
    summaries: dict[str, dict[str, Any]] = {}
    warnings = []
    for scene in scenes:
        if not isinstance(scene.get("characters", []), list):
            raise TypeError("scene characters must be a list")
        present = set(map(str, scene.get("characters", [])))
        entered = sorted(present - prior)
        exited = sorted(prior - present)
        rows.append(
            {
                "scene": str(scene["id"]),
                "present": sorted(present),
                "entered": entered,
                "exited": exited,
            }
        )
        if not present:
            warnings.append({"scene": str(scene["id"]), "warning": "empty character roster"})
        for name in present | prior:
            summary = summaries.setdefault(
                name,
                {
                    "scenes_present": 0,
                    "entrances": 0,
                    "exits": 0,
                    "first_scene": None,
                    "last_scene": None,
                },
            )
            if name in present:
                summary["scenes_present"] += 1
                summary["first_scene"] = summary["first_scene"] or str(scene["id"])
                summary["last_scene"] = str(scene["id"])
            summary["entrances"] += name in entered
            summary["exits"] += name in exited
        prior = present
    return {
        "characters": sorted(summaries),
        "transition_count": sum(len(row["entered"]) + len(row["exited"]) for row in rows),
        "character_summaries": dict(sorted(summaries.items())),
        "warnings": warnings,
        "scenes": rows,
    }


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
