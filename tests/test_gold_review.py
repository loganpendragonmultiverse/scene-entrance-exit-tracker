import copy
import json

import pytest

from scene_entrance_exit_tracker.cli import main
from scene_entrance_exit_tracker.core import analyze


@pytest.mark.parametrize("value", [None, [], 1, True, "text"])
def test_malformed_roots(value):
    with pytest.raises(TypeError, match="JSON object"):
        analyze(value)


@pytest.mark.parametrize("value", [None, [], 1, True, "text"])
def test_malformed_scene(value):
    with pytest.raises(TypeError, match="scene"):
        analyze({"scenes": [value]})


@pytest.mark.parametrize("names", [[None], [False], [3], [{}], [""], [" A"], ["A "], ["A", "A"]])
def test_roster_identity_is_explicit(names):
    with pytest.raises(ValueError):
        analyze({"scenes": [{"id": "one", "characters": names}]})


@pytest.mark.parametrize("identity", [None, 1, False, "", " one", "one "])
def test_scene_identity_is_explicit(identity):
    with pytest.raises(ValueError):
        analyze({"scenes": [{"id": identity}]})


def test_ordered_presence_and_source_evidence_unchanged():
    data = {
        "scenes": [
            {
                "id": "one",
                "characters": ["A"],
                "events": [
                    {"action": "exit", "character": "A"},
                    {"action": "enter", "character": "B"},
                    {"action": "exit", "character": "B"},
                    {"action": "enter", "character": "B"},
                ],
            },
            {"id": "two", "characters": ["B"]},
        ]
    }
    before = copy.deepcopy(data)
    report = analyze(data)
    assert data == before
    assert report["scenes"][0]["present"] == ["A"]
    assert report["scenes"][0]["end_present"] == ["B"]
    assert report["scenes"][1]["entered"] == []
    assert report["character_summaries"]["B"]["scenes_present"] == 2
    assert report["character_summaries"]["B"]["entrances"] == 2
    assert report["transition_count"] == 5


def test_cli_malformed_input_and_exclusive_output(tmp_path, capsys):
    source = tmp_path / "input.json"
    source.write_text(json.dumps({"scenes": [None]}))
    assert main([str(source)]) == 2
    assert "Traceback" not in capsys.readouterr().err
    source.write_text(json.dumps({"scenes": [{"id": "one"}]}))
    output = tmp_path / "report.json"
    output.write_text("valuable")
    assert main([str(source), "--output", str(output)]) == 2
    assert output.read_text() == "valuable"


def test_padded_event_identity_rejected():
    with pytest.raises(ValueError):
        analyze({"scenes": [{"id": "one", "events": [{"action": "enter", "character": " A"}]}]})
