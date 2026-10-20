# Changelog

## 1.2.2 - 2026-10-20

- Reject malformed roots, scenes and ambiguous character identities before transition analysis.
- Preserve duplicate-roster evidence by refusing duplicate identities instead of collapsing them.
- Create reports exclusively and ship authority documents plus the representative example.

## 1.2.1

- Correct released documentation labels; package behavior is unchanged.
- Preserve the original v1.2.0 tags and artifacts. This patch supplies corrected documentation in new artifacts.

## 1.2.0 - 2026-10-15

- Each scene may supply ordered `events`, for example `[{"action":"exit","character":"Mara"},{"action":"enter","character":"Ivo"}]`.

## 1.1.0 - 2026-07-27

- Added per-character scene, entrance, exit, first-scene, and last-scene summaries.
- Added total transition counts and explicit empty-roster warnings.
- Added stricter scene roster validation.

## 1.0.0 - 2026-07-26

- Released the first complete Scene Entrance/Exit Tracker command-line workflow.
- Added deterministic JSON and Markdown reporting, representative examples, and cross-platform tests.
