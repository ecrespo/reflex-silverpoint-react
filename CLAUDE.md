# CLAUDE.md

Read [AGENTS.md](AGENTS.md) first: it holds the layout, commands, conventions and release flow of
this repository. The essentials:

- Reflex custom component wrapping `@silverpoint/react` 0.7.0; package version 0.7.1;
  Reflex ≥ 0.10.0, Python ≥ 3.11. Everything rendered is an npm component except `sp_trigger`.
- Test-driven: write the failing test in `tests/` before the implementation.
- Never edit `*.pyi` by hand — run `uv run python scripts/make_stubs.py`.
- Before committing: `pre-commit run --all-files` (ruff check + format, also on README code blocks;
  `uv lock --check`) and `uv run pytest`.
- New public symbols go into `__init__.py` and its sorted `__all__`.
- Work in this repository only; don't touch sibling repos (e.g. `reflex-knightlab-timeline`)
  without asking.
- Release by tag `vX.Y.Z` on `main` (matches `pyproject.toml`); PyPI via Trusted Publishing.
