import json
from pathlib import Path

import pytest

from scene_entrance_exit_tracker.cli import main
from scene_entrance_exit_tracker.core import PROJECT, analyze, render_json, render_markdown


def test_representative_sample_has_expected_result():
    data = json.loads(
        (Path(__file__).parents[1] / "examples" / "sample.json").read_text(encoding="utf-8")
    )
    report = analyze(data)
    assert report["version"] == 1
    assert report["project"] == PROJECT
    assert report["scenes"][1]["entered"] == ["Ivo"]
    assert report["character_summaries"]["Mara"]["scenes_present"] == 2
    assert report["character_summaries"]["Ivo"]["first_scene"] == "2"
    assert report["transition_count"] == 3
    assert f'"project": "{PROJECT}"' in render_json(report)
    assert PROJECT.replace("-", " ").title() in render_markdown(report)


def test_missing_required_input_is_rejected():
    with pytest.raises(ValueError):
        analyze({})


def test_empty_scenes_are_flagged_and_character_lists_validated():
    report = analyze({"scenes": [{"id": "one", "characters": ["Mara"]}, {"id": "two"}]})
    assert report["warnings"] == [{"scene": "two", "warning": "empty character roster"}]
    assert report["character_summaries"]["Mara"]["exits"] == 1
    with pytest.raises(TypeError, match="characters"):
        analyze({"scenes": [{"id": "one", "characters": "Mara"}]})


def test_cli_json_and_output_safety(tmp_path, capsys):
    source = Path(__file__).parents[1] / "examples" / "sample.json"
    assert main([str(source), "--format", "json"]) == 0
    assert json.loads(capsys.readouterr().out)["project"] == PROJECT
    output = tmp_path / "report.md"
    output.write_text("keep", encoding="utf-8")
    assert main([str(source), "--output", str(output)]) == 2
