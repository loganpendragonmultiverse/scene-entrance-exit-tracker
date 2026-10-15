import pytest

from scene_entrance_exit_tracker.core import analyze


def test_ordered_events_rosters_and_reentry():
    r = analyze(
        {
            "scenes": [
                {
                    "id": "1",
                    "characters": ["A"],
                    "events": [
                        {"action": "exit", "character": "A"},
                        {"action": "enter", "character": "B"},
                        {"action": "exit", "character": "B"},
                        {"action": "enter", "character": "B"},
                    ],
                },
                {"id": "2", "characters": ["B"]},
            ]
        }
    )
    assert r["scenes"][0]["present"] == ["A"]
    assert r["scenes"][0]["end_present"] == ["B"]
    assert r["scenes"][1]["entered"] == []
    assert r["scenes"][1]["exited"] == []
    assert r["transition_count"] == 5
    assert r["character_summaries"]["B"]["scenes_present"] == 2


@pytest.mark.parametrize(
    "events",
    [
        [{"action": "enter", "character": "A"}],
        [{"action": "exit", "character": "B"}],
        [{"action": "exit", "character": "A"}, {"action": "exit", "character": "A"}],
        {},
        [None],
        [{"action": "wait", "character": "A"}],
        [{"action": "enter", "character": ""}],
    ],
)
def test_invalid_events(events):
    with pytest.raises((ValueError, TypeError)):
        analyze({"scenes": [{"id": "1", "characters": ["A"], "events": events}]})


def test_empty_events_and_default():
    base = analyze({"scenes": [{"id": "1", "characters": ["A"]}]})
    assert "events" not in base["scenes"][0]
    r = analyze({"scenes": [{"id": "1", "characters": ["A"], "events": []}]})
    assert r["scenes"][0]["end_present"] == ["A"]
    assert r["transition_count"] == base["transition_count"]
