# AGENTS.md — reflex-silverpoint-react

Guide for coding agents working in this repository. Humans: see [README.md](README.md).

## What this is

A Reflex custom component (published on PyPI as `reflex-silverpoint-react`) that wraps the npm
package `@silverpoint/react` — charts and UI drawn in the manner of a Renaissance silverpoint
drawing. Version **0.8.0**, wrapping silverpoint **0.8.0** (`SILVERPOINT_VERSION` in `base.py`). Every
component it renders is an npm component of `@silverpoint/react` (silverpoint's parity contract);
the only JS of its own is `sp_trigger` (`assets/trigger.jsx`).
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
  palette.py      Palette, PALETTES (= @silverpoint/core/palettes), check_palette (the core's PALETTE_PAIRS),
                  palette_prop (the npm `palette` prop), silverpoint_palette (a provider with a palette)
  surfaces.py     npm SpSurface / SpGlyph, SpPagination, SpInputNumber (/ui)
  composed.py     npm composed components (/ui): sp_table, sp_breadcrumb, sp_avatar, …; sort_rows (= uiSortRows)
  overlays.py     npm overlays (/ui): sp_modal, sp_drawer, sp_popover, sp_tooltip, sp_select, sp_dropdown_menu,
                  sp_toast, sp_toaster; sp_trigger (SpTrigger, our own JS: a drawn button that keeps cloned props)
  timeline.py     npm SpTimeline (/timeline) + @knight-lab/timelinejs as its npm dependency
  assets/         trigger.jsx (shipped as package data)
  *.pyi           generated stubs — never edit by hand
scripts/make_stubs.py   regenerates the .pyi stubs (Reflex 0.10 removed `reflex component build`)
scripts/export_catalog.py  writes reflex-catalog.json, the catalog silverpoint's agent catalog joins
scripts/make_skill.py   writes skills/reflex-silverpoint/ from its templates/ and reflex-catalog.json
skills/reflex-silverpoint/  the agent skill (generated; prose in templates/)
.claude-plugin/         the Claude plugin: the skill and the hosted silverpoint MCP server
tests/                  pytest suite (test_components.py, test_demo_data.py, test_v07.py,
                        test_agent_catalog.py, test_skill.py, test_plugin.py)
silverpoint_react_demo/ demo Reflex app (gallery, playground, dashboard, /ui, /components, /palettes, /timeline)
docs/                   screenshots used by the README
```

## Commands

```bash
uv sync --extra dev                     # environment
uv run pytest                           # tests
uv run ruff check . && uv run ruff format --check .   # lint + format (also formats README code blocks)
pre-commit run --all-files              # everything CI's lint job checks, plus file hygiene
uv run python scripts/make_stubs.py     # regenerate .pyi stubs after changing a component's props
uv run python scripts/export_catalog.py # regenerate reflex-catalog.json (CI: --check)
uv run python scripts/make_skill.py     # regenerate the skill from its templates (CI: --check)
uv build                                # sdist + wheel
cd silverpoint_react_demo && uv run reflex compile   # what the CI "demo" job runs
```

## Conventions

- **Tests first.** Write the failing test before the implementation (`tests/test_v07.py` shows
  the style: render a component and assert on its props).
- Every public symbol is re-exported from `__init__.py` and listed in `__all__` (sorted).
- Public builders are snake_case (`bar_chart`, `sp_table`); component classes are PascalCase.
- Keep the Python API a thin layer over the npm one: a prop exists here only if `@silverpoint/react`
  has it (check `packages/core/src/ui/types.ts` and `packages/react/src/ui/*.tsx` in the silverpoint
  repo). Renamed 0.7.0 arguments stay as deprecated aliases (`DeprecationWarning`), never silently.
- Bumping silverpoint: change `SILVERPOINT_VERSION`, diff the npm API (API Spec deltas in
  `silverpoint/changes/`), update the wrappers, tests, README and CHANGELOG, then compile the demo
  with `reflex export --frontend-only` (it installs the npm packages and bundles them).
- Agent files: after changing a builder, a prop or a version, regenerate `reflex-catalog.json` and
  the skill; the skill's prose lives only in `skills/reflex-silverpoint/templates/`. Every `python`
  block of the skill is imported and rendered by the tests, and its builder keywords must be in the
  catalog. A version bump moves both `.claude-plugin/*.json` versions too.
- Composed components and overlays read `silverpoint_provider`, like the `Sp` components; overlays
  render in place (top layer), so section palettes reach them. `sp_trigger` reads no provider.
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
- Release: bump `version` in `pyproject.toml` and `.claude-plugin/*.json`, regenerate the catalog
  and the skill, update `CHANGELOG.md`, merge to `main`, then push a tag `vX.Y.Z` matching the
  version. The GitHub release carries `reflex-catalog.json`, which silverpoint pins. `release.yml` re-runs quality and security and publishes to
  PyPI by Trusted Publishing (no token in the repo).
