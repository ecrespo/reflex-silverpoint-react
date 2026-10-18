# AGENTS.md — reflex-silverpoint-react

Guide for coding agents working in this repository. Humans: see [README.md](README.md).

## What this is

A Reflex custom component (published on PyPI as `reflex-silverpoint-react`) that wraps the npm
package `@silverpoint/react` — charts and UI drawn in the manner of a Renaissance silverpoint
drawing. Version **0.7.0**, wrapping silverpoint **0.6.0** (`SILVERPOINT_VERSION` in `base.py`).
It requires **Reflex ≥ 0.10.0** and **Python ≥ 3.11**.

## Layout

```
custom_components/reflex_silverpoint_react/
  base.py         SilverpointChart base class, SilverpointProvider, npm versions, stylesheets
  charts.py       the 60 chart wrappers (class + snake_case builder per chart)
  catalog.py      CHARTS / FAMILIES / prop docs (drives the gallery, playground and tests)
  dashboard.py    Dashboard, DashboardCell, DashboardLink (subpath imports of @silverpoint/react)
  ui.py           the 17 Sp UI components (/ui subpath + @silverpoint/grounds/ui.css)
  ui_catalog.py   UI_COMPONENTS (17 components, 45 states), UI_DEMOS, ui_demo()
  helpers.py      tooltip_template, chart_ref, download_svg, get_svg, get_geometry
  palette.py      0.7 — Palette, PALETTES presets, check_palette, silverpoint_palette, palette=
  surfaces.py     0.7 — SpSurface / SpGlyph (the ui.css markup contract), sp_pagination, sp_input_number
  composed.py     0.7 — level A composed components (native markup): sp_table, sp_breadcrumb, …
  overlays.py     0.7 — level B composed components on Radix primitives: sp_modal, sp_select, sp_toast, …
  timeline.py     0.7 — sp_timeline (Knight Lab TimelineJS, optional extra `[timeline]`)
  assets/         surface.jsx, surfaces.css, timeline.jsx, timeline.css (shipped as package data)
  *.pyi           generated stubs — never edit by hand
scripts/make_stubs.py   regenerates the .pyi stubs (Reflex 0.10 removed `reflex component build`)
tests/                  pytest suite (test_components.py, test_demo_data.py, test_v07.py)
silverpoint_react_demo/ demo Reflex app (gallery, playground, dashboard, /ui, /components, /palettes, /timeline)
docs/                   screenshots used by the README
```

## Commands

```bash
uv sync --extra dev                     # environment (dev extra includes the timeline extra)
uv run pytest                           # tests
uv run ruff check . && uv run ruff format --check .   # lint + format (also formats README code blocks)
pre-commit run --all-files              # everything CI's lint job checks, plus file hygiene
uv run python scripts/make_stubs.py     # regenerate .pyi stubs after changing a component's props
uv build                                # sdist + wheel
cd silverpoint_react_demo && uv run reflex compile   # what the CI "demo" job runs
```

## Conventions

- **Tests first.** Write the failing test before the implementation (`tests/test_v07.py` shows
  the style: render a component and assert on its props).
- Every public symbol is re-exported from `__init__.py` and listed in `__all__` (sorted).
- Public builders are snake_case (`bar_chart`, `sp_table`); component classes are PascalCase.
- Composed components (levels A and B) do **not** read `silverpoint_provider`: they take `ground`,
  `substrate`, `mode`, `palette` explicitly. Overlays render in a portal, outside any
  `silverpoint_palette` section.
- Palettes are monochrome by design (`ink` + `ink_secondary`), never a colour per series.
- After changing props, regenerate the stubs with `scripts/make_stubs.py`; `*.pyi` files are
  excluded from ruff.
- The CI wheel smoke test asserts `len(sp.CHARTS) == 60`; update it if the catalog changes.
- Line length is 120. Demo `state.py` / `extra_pages.py` and `tests/` allow mutable class
  defaults (RUF012), as Reflex state requires.

## Git and release flow

- Branch from `develop` (`feat/…`, `fix/…`, `docs/…`); PR into `develop`, then `develop` into `main`.
- Conventional commits (`feat:`, `fix:`, `docs:`, `ci:` …).
- CI: `quality.yml` (ruff, pytest on 3.11–3.13, build + twine + wheel smoke test, demo compile) and
  `security.yml` (gitleaks, bandit, pip-audit, dependency review, CodeQL).
- Release: bump `version` in `pyproject.toml`, update `CHANGELOG.md`, merge to `main`, then push a
  tag `vX.Y.Z` matching the version. `release.yml` re-runs quality and security and publishes to
  PyPI by Trusted Publishing (no token in the repo).
