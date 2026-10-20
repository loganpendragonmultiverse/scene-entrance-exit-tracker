# Development contract

Build a scene-by-scene character presence matrix and explicit entrance and exit transitions.

Version 1.1 adds deterministic per-character summaries, transition totals, empty-roster warnings, and stricter roster validation.

Preserve deterministic, source-safe behavior and the interpretation boundary documented in the README. Every feature release must update tests, version metadata, `CHANGELOG.md`, README claims and limitations, repository metadata, release assets, and the Forge catalog together.

## 1.2.0

Each scene may supply ordered `events`, for example `[{"action":"exit","character":"Mara"},{"action":"enter","character":"Ivo"}]`. `characters` is the initial roster; events produce `end_present`, which becomes the prior roster for the next scene. Entering a present character or exiting an absent one is rejected. Re-entry after an exit is valid. Summaries count each transition and each scene occupied at least once; `present` remains the initial roster. Omitted events retain legacy output.

## Identity and packaging contract

Validate roots, scene objects, unique scene IDs and initial rosters before
computing transitions. Preserve exact authored case-sensitive identities and reject
blank or padded identities. Events may re-enter after an exit but must never
invent an entrance or exit from a malformed value. Keep initial roster evidence
separate from end-of-scene state. Include four authority documents and the
representative JSON example in wheel and source distributions.
