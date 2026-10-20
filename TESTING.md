# Testing

Run `python -m pip install -e ".[dev]"`, `ruff format --check .`, `ruff check .`, `mypy src`, `pytest`, and `python -m build`.

## 1.2.0 acceptance

Exercise the optional input with the full regression suite, including validation, inclusive boundaries, deterministic ordering and legacy default behavior. Each scene may supply ordered `events`, for example `[{"action":"exit","character":"Mara"},{"action":"enter","character":"Ivo"}]`. `characters` is the initial roster; events produce `end_present`, which becomes the prior roster for the next scene. Entering a present character or exiting an absent one is rejected. Re-entry after an exit is valid. Summaries count each transition and each scene occupied at least once; `present` remains the initial roster. Omitted events retain legacy output.

## 1.2.2 acceptance

Run all commands above and `tests/test_gold_review.py`. Cover malformed roots and
scene objects, blank/non-string/duplicate/padded identities, ordered re-entry,
prior-scene state and source immutability. Install each built wheel and sdist;
from outside the checkout run the full suite against site-packages and execute
`scene-presence` on the installed JSON example in both report formats. Confirm
four authority documents match source. Keep the 90% coverage floor and protected
cross-platform CI/CodeQL requirements.

`tests/test_output_links.py` checks refusal of existing dangling-link metadata
on every platform and actual dangling symlinks where creation is supported.
