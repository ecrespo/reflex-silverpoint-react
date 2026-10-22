---
name: reflex-silverpoint
description: Build silverpoint charts, dashboards and UI in Python with Reflex through reflex-silverpoint-react. Use whenever code imports reflex_silverpoint_react or the user wants silverpoint in Reflex.
---

# reflex-silverpoint

This skill describes **reflex-silverpoint-react {{version}}**, which wraps **silverpoint {{wraps}}**
(`@silverpoint/react@{{wraps}}`). If the project pins another version, check the builders and props
you write against `reflex_silverpoint_react.__all__` and the `.pyi` stubs of that version.

`reflex-silverpoint-react` is a Reflex custom component: the 60 silverpoint charts, the dashboard,
38 UI, composed and overlay components, palettes and a Knight Lab timeline, as snake_case Python
builders. Everything it renders is the npm component of `@silverpoint/react`, so the drawing is the
one React, Vue and Angular draw: hatched tone, a hand-inked line, prepared paper, deterministic for a
given `id` or `seed`.

## Prefer the silverpoint MCP tools when they are connected

When the `silverpoint` MCP server is connected, prefer its tools over these files for anything about
a chart or a component. They read the catalog silverpoint builds with this package's export
(`reflex-catalog.json`), so they carry the Reflex names too, and they also check and draw:

- `recommend_chart`: up to five charts for a data shape and an intent.
- `get_chart`, `get_component`: props with their defaults and notes, data fields, and the Reflex
  builder and Python prop names beside the React ones.
- `generate_code` with `framework: "reflex"`: the imports and the builder call for one chart or
  component.
- `validate_props`: the diagnostics the library raises for a set of props (pass the JS names).
- `render_chart`: the chart as a standalone SVG, to look at before writing the code.
- `check_palette`, `search_catalog`, `list_charts`, `list_components`, `get_version`.

`get_version` answers `reflex: {version, wraps, stale}`. When `stale` is true, or its `reflex.version`
is not the one the project installs, the server's Reflex names describe another release: trust
these references for the Python side. To connect the hosted server in
Claude Code: `claude mcp add --transport http silverpoint https://silverpointweb.vercel.app/mcp`
(this skill's plugin declares it already). The State patterns, events and the demo app's idioms are
only here: read [references/state-and-events.md](references/state-and-events.md).

## Install

```sh
pip install reflex-silverpoint-react
```

Reflex installs the npm packages and imports the stylesheets each component needs; there is nothing
to add on the JavaScript side, no Tailwind and no CDN. It needs Reflex 0.10.0 or later and Python
3.11 or later.

## Workflow

1. **Choose the chart** with `recommend_chart`, or from the chart index below: name the rows' data
   shape (series, categories, parts, hierarchy, links, points, distribution…) and what the reader
   should see (trend, compare, part-to-whole, flow…).
2. **Read its entry** in `references/charts/<family>.md`: its own props with their JS names, an
   example, and the demo rows that show which fields its accessors read.
3. **Keep the data in a `rx.State` field** (a `list[dict]`) and pass the field itself as `data`.
   Wire events to `@rx.event` handlers. See
   [references/state-and-events.md](references/state-and-events.md).
4. **Check it** against the rules below before you finish.

## The rules that matter most

- **Builders and props are snake_case.** The React prop `valueKey` is `value_key`, `hatchFill` is
  `hatch_fill`, `onActiveChange` is `on_active_change`. Charts carry no prefix (`line_chart`); every
  UI, composed and overlay builder is `sp_…` (`sp_button`, `sp_modal`). Each builder has a class of
  the same name in PascalCase (`LineChart`, `SpModal`).
- **Import from the package root**: `from reflex_silverpoint_react import line_chart, sp_table`.
  There are no subpaths in Python; each component imports its own npm subpath.
- **Accessors are field names**, strings: `x_key="hour"`, `value_key="hits"`, `keys=["a", "b"]`. Read
  them from your rows; never reuse the example's names. The JavaScript API also takes functions; from
  Python, shape the rows instead.
- **Without `data`, a chart draws its demo rows** and ignores its accessors. A chart that shows
  plausible numbers is not proof that your data reached it.
- **Pass state vars directly**: `data=State.rows`, `items=State.items`, `value=State.city`. No
  `rx.foreach` is needed to feed a chart or a component; use it only to repeat components yourself.
- **Event handlers receive values, not DOM events**: `on_change` a string, bool or number,
  `on_open_change` a bool, `on_select` the chart item (a dict). See the payload table in
  [references/state-and-events.md](references/state-and-events.md).
- **Controlled or uncontrolled, never both**: `value=` / `checked=` / `open=` with their handler, or
  `default_value=` / `default_checked=` / `default_open=` alone.
- **A chart takes its container's width.** Give the container a width, or pass `width`. `height` is
  the drawing area (160 px by default), without the card's title and footer.
- **Give each chart a stable `id`** (and a dashboard its required `id`): the hand-inked line is
  seeded from it, and download or geometry helpers find the chart by it. Never derive it from
  `random`.
- **Name every chart**: `title` or `label` is its accessible name, `description` the long one.
- **Appearance is `ground`, `substrate`, `mode` and `palette`.** `ground` is `silverpoint` (hatched,
  the default) or `cyanotype` (a white line on Prussian blue, whose only substrate is `prussian`);
  `mode="precision"` turns the inking off. `palette` takes a preset's **name** (`"sanguine"`), a
  `Palette`, a dict of fields or a state var. See [references/palettes.md](references/palettes.md).
- **Tone is not colour.** Palettes are monochrome by design (`ink` and `ink_secondary`): categories
  differ by hatch density, never by a colour per series.
- **`silverpoint_provider(...)` sets ground, substrate, mode, locale and palette for a subtree.** A
  prop on the chart wins over its dashboard, and the dashboard over the provider.
- **Overlay triggers are native:** `trigger="Open"` (the string becomes `sp_trigger`), an
  `rx.el.button`, or `sp_trigger(...)`. Never `trigger=sp_button(...)`: `SpButton` drops the ARIA and
  the click the overlay clones onto its trigger. `sp_trigger` reads no provider: give it `ground`,
  `substrate`, `mode` and `palette` yourself. See [references/overlays.md](references/overlays.md).
- **`sp_table` does not sort for you.** Sort the rows in `on_sort` with `sort_rows(rows, key,
  order)`, then hand them back.
- **`gauge_arc` and `meter_chart` take `percent`** (0–100) instead of `data`; `ridgeline_chart` needs
  `group_key`, `diverging_bar_chart` `levels` and `parallel_coordinates_chart` `dimensions` with your
  own rows.
- **Hierarchy charts take flat rows** with an id and a parent id (`None` for the root), not nested
  children. `squarified_treemap` and `sunburst_chart` drill down only through `root_id` and
  `on_root_change`.
- **Charts switch to `precision` by themselves** under `prefers-contrast: more` or
  `forced-colors: active`; no prop overrides that.

## Charts

<!-- generated:chart-index -->

### Common chart props

Every chart takes these besides its own:

<!-- generated:common-chart-props -->

## Components

<!-- generated:component-index -->

Every UI, composed and overlay component also takes `id`, `class_name` and these:

<!-- generated:common-ui-props -->

## Helpers

<!-- generated:helpers -->

## A first page

```python
import reflex as rx
from reflex_silverpoint_react import line_chart, silverpoint_provider


class State(rx.State):
    rows: list[dict] = [
        {"hour": "00", "hits": 18},
        {"hour": "08", "hits": 42},
        {"hour": "16", "hits": 57},
    ]


def index() -> rx.Component:
    return silverpoint_provider(
        rx.box(
            line_chart(data=State.rows, x_key="hour", value_key="hits", title="Hits per hour", id="hits"),
            width="480px",
        ),
        ground="silverpoint",
        substrate="cream",
    )
```

## Composition

- **Dashboard:** a titled, responsive grid of chart cards with an optional linked highlight. See
  [references/dashboard.md](references/dashboard.md).
- **Timeline:** `sp_timeline`, Knight Lab TimelineJS drawn in silverpoint. See
  [references/timeline.md](references/timeline.md).
- **Components and overlays:** [references/components.md](references/components.md),
  [references/overlays.md](references/overlays.md).
- **React, Vue or Angular** code is the `silverpoint` skill's, not this one's.
