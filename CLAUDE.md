# CLAUDE.md

Read [AGENTS.md](AGENTS.md) first: it holds the layout, commands, conventions and release flow of
this repository. The essentials:

- Reflex custom component wrapping `@silverpoint/react` 0.8.0; package version 0.8.1;
  Reflex ≥ 0.10.0, Python ≥ 3.11. Everything rendered is an npm component except `sp_trigger`.
- Test-driven: write the failing test in `tests/` before the implementation.
- Never edit `*.pyi` by hand — run `uv run python scripts/make_stubs.py`.
- Before committing: `pre-commit run --all-files` (ruff check + format, also on README code blocks;
  `uv lock --check`) and `uv run pytest`.
- New public symbols go into `__init__.py` and its sorted `__all__`.
- Work in this repository only; don't touch sibling repos (e.g. `reflex-knightlab-timeline`)
  without asking.
- Release by tag `vX.Y.Z` on `main` (matches `pyproject.toml`); PyPI via Trusted Publishing.
- Agent files are generated: after changing a builder, its props or the version, run
  `uv run python scripts/export_catalog.py` and `uv run python scripts/make_skill.py` (CI fails
  otherwise); edit the skill only in `skills/reflex-silverpoint/templates/`. A version bump also
  moves both `.claude-plugin/*.json` versions (a test checks them).

## Status: silverpoint feature-005 (agent access)

This repository's half, released in `v0.8.0` (2026-10-21):

- T-230 done — `reflex-catalog.json` (`scripts/export_catalog.py`, Data Model §2.30), checked in CI,
  attached to each GitHub release. It equals silverpoint's derived pin except `deprecated` (the
  pin's reader cannot see aliases) and `on_root_change` on the two drillable charts. Once silverpoint
  pins this export instead of its derived one, REQ-556 is strict: a silverpoint release fails while
  this package wraps an older silverpoint.
- T-246 done — `skills/reflex-silverpoint/` (`scripts/make_skill.py`, checked in CI).
- T-247 done (this half) — `tests/test_skill.py` imports and renders every `python` fence of the
  skill and checks each builder keyword against the catalog; other fences must be `sh`, `text`, `json`.
- T-248 done (this half) — `.claude-plugin/` (skill + hosted MCP inline); validated with
  `claude plugin validate`, install tested against a throwaway `CLAUDE_CONFIG_DIR`.
- T-250 done (this half) — this status, the README and the CHANGELOG.
