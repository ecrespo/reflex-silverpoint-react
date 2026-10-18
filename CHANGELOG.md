# Changelog

All notable changes to `reflex-silverpoint-react`. The format follows
[Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versions follow
[Semantic Versioning](https://semver.org/).

## [0.7.0] — 2026-10-18

### Added

- **Palettes**: `palette=` on every chart, UI component, dashboard and composed component;
  `Palette`, `PALETTES` (presets `silverpoint`, `sanguine`, `sepia`, `iron_gall`, `verdigris`,
  `indigo`), `silverpoint_palette(...)` for a whole section, `check_palette()`, `contrast_ratio()`,
  `palette_css()` and `PALETTE_PROPERTIES`.
- **Composed components, level A** (native markup on silverpoint surfaces): `sp_table` (+
  `sort_rows`), `sp_pagination`, `sp_breadcrumb`, `sp_avatar` (+ `sp_avatar_group`),
  `sp_statistic`, `sp_descriptions`, `sp_timeline_list`, `sp_collapse` (+ `sp_collapse_item`),
  `sp_empty`, `sp_result`, `sp_textarea`, `sp_input_number`.
- **Composed components, level B** (overlays on Radix primitives): `sp_modal`, `sp_drawer`,
  `sp_popover`, `sp_tooltip`, `sp_select`, `sp_dropdown_menu`, `sp_toast` (+ `sp_toaster`) and
  `sp_trigger`.
- **`sp_timeline`**: Knight Lab TimelineJS drawn in silverpoint (optional extra
  `reflex-silverpoint-react[timeline]`), plus `timeline_available()`.
- `sp_surface` and `sp_glyph`, the building blocks of the composed components.
- `scripts/make_stubs.py` to regenerate the `.pyi` stubs.
- Demo pages `/components`, `/palettes` and `/timeline`; palette control on Gallery and Playground.
- `AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md` and a `.pre-commit-config.yaml` mirroring CI.

### Changed

- Requires **Reflex 0.10.0** and therefore **Python 3.11+** (CI matrix 3.11–3.13).
- The package ships `assets/*.jsx` and `assets/*.css` as package data.

### Removed

- Python 3.10 support. `reflex component build` (removed by Reflex 0.10) is replaced by
  `scripts/make_stubs.py` + `uv build`.

## [0.6.0]

- 27 new charts (silverpoint 0.6 second catalog) — 60 in total — and drill-down on
  `squarified_treemap` and `sunburst_chart` (`root_id`, `on_root_change`).

## [0.3.0]

- The 17 `Sp` UI components, `UI_COMPONENTS`, `UI_DEMOS`, `ui_demo()`; `substrate="prussian"`.

## [0.2.0]

- `dashboard`, `dashboard_cell`, `dashboard_link`; the `cyanotype` ground.

## [0.1.0]

- First release: the silverpoint charts, `SilverpointProvider`, events, readouts and the
  imperative handle (SVG export, geometry).

[0.7.0]: https://github.com/ecrespo/reflex-silverpoint-react/compare/v0.6.0...v0.7.0
[0.6.0]: https://github.com/ecrespo/reflex-silverpoint-react/compare/v0.3.0...v0.6.0
[0.3.0]: https://github.com/ecrespo/reflex-silverpoint-react/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/ecrespo/reflex-silverpoint-react/releases/tag/v0.2.0
[0.1.0]: https://github.com/ecrespo/reflex-silverpoint-react/releases/tag/v0.1.0
