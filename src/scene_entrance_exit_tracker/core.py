from __future__ import annotations

import json
from typing import Any

PROJECT = "scene-entrance-exit-tracker"


def _require(data: dict[str, Any], key: str) -> Any:
    if not isinstance(data, dict):
        raise TypeError("input must be a JSON object")
    value = data.get(key)
    if value is None or value == "" or value == []:
        raise ValueError(f"{key} is required")
    return value


def _scene_presence(data: dict[str, Any]) -> dict[str, Any]:
    scenes = _require(data, "scenes")
    if not isinstance(scenes, list):
        raise TypeError("scenes must be a list")
    if any(not isinstance(scene, dict) for scene in scenes):
        raise TypeError("each scene must be an object")
    ids = [scene.get("id", "") for scene in scenes]
    if any(not isinstance(item, str) or not item.strip() or item != item.strip() for item in ids):
        raise ValueError("scene ids must be nonempty text without surrounding whitespace")
    if any(not item for item in ids) or len(ids) != len(set(ids)):
        raise ValueError("scenes need unique non-empty ids")
    prior: set[str] = set()
    rows: list[dict[str, Any]] = []
    summaries: dict[str, dict[str, Any]] = {}
    warnings = []
    for scene in scenes:
        if not isinstance(scene.get("characters", []), list):
            raise TypeError("scene characters must be a list")
        roster = scene.get("characters", [])
        if any(
            not isinstance(name, str) or not name.strip() or name != name.strip() for name in roster
        ):
            raise ValueError("character names must be nonempty text without surrounding whitespace")
        if len(roster) != len(set(roster)):
            raise ValueError("scene character rosters must not repeat identities")
        present = set(roster)
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
        if "events" in scene:
            events = scene["events"]
            if not isinstance(events, list):
                raise TypeError("scene events must be an ordered list")
            end = set(present)
            reviewed = []
            for index, event in enumerate(events):
                if (
                    not isinstance(event, dict)
                    or event.get("action") not in ("enter", "exit")
                    or not isinstance(event.get("character"), str)
                    or not event["character"].strip()
                    or event["character"] != event["character"].strip()
                ):
                    raise ValueError("events require an enter/exit action and nonempty character")
                name, action = event["character"], event["action"]
                if (action == "enter") == (name in end):
                    raise ValueError(
                        f"scene {scene['id']} event {index}: {action} contradicts presence"
                    )
                if action == "enter":
                    end.add(name)
                else:
                    end.remove(name)
                reviewed.append({"action": action, "character": name})
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
                summary["entrances" if action == "enter" else "exits"] += 1
                if action == "enter" and name not in present:
                    summary["scenes_present"] += 1
                    summary["first_scene"] = summary["first_scene"] or str(scene["id"])
                    summary["last_scene"] = str(scene["id"])
                    present.add(name)
            rows[-1]["events"] = reviewed
            rows[-1]["end_present"] = sorted(end)
            prior = end
        else:
            prior = present
    return {
        "characters": sorted(summaries),
        "transition_count": sum(
            len(row["entered"]) + len(row["exited"]) + len(row.get("events", [])) for row in rows
        ),
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
