# State and events

**Contents:** [Data from state](#data-from-state) · [Controlled and uncontrolled](#controlled-and-uncontrolled) ·
[Event payloads](#event-payloads) · [Chart events](#chart-events) · [Drill-down](#drill-down) ·
[The imperative handle](#the-imperative-handle) · [Every event](#every-event)

The patterns of the package's demo app (`silverpoint_react_demo/`), which wires every chart and
component to Python state.

## Data from state

Keep rows in a `rx.State` field, a `list[dict]`, and pass **the field itself** as `data`. The
component serialises the var and redraws when it changes; there is no `rx.foreach` between your
state and a chart, a table, a select's items or a step list. Use `rx.foreach` only to repeat
components of your own (a log, one `sp_tag` per tag).

- Rows are plain dicts of JSON values: strings, numbers, booleans, `None`, nested lists or dicts
  where a chart's field holds them (a sparkline's `points`, a heatmap row's `values`). Dates are ISO
  strings (`"2026-03-15"`).
- Assign a new list to redraw (`self.rows = [...]`), as the demo's re-roll does.
- A computed `@rx.var` works as data like any field, for a filtered or derived series.
- Constant rows can be a module-level list; a chart re-reads nothing then.

```python
import random

import reflex as rx
from reflex_silverpoint_react import bar_chart, sp_button, sp_steps


class State(rx.State):
    rows: list[dict] = [{"x": "Mon", "value": 12}, {"x": "Tue", "value": 18}, {"x": "Wed", "value": 9}]
    step: int = 0
    tags: list[str] = ["ink", "ground"]

    @rx.event
    def reroll(self):
        self.rows = [{**row, "value": random.randint(5, 40)} for row in self.rows]

    @rx.var
    def busy_days(self) -> list[dict]:
        return [row for row in self.rows if row["value"] > 10]

    @rx.var
    def steps(self) -> list[dict[str, str]]:
        return [{"key": "draft", "title": "Draft"}, {"key": "review", "title": "Review"}]


def weekly() -> rx.Component:
    return rx.el.div(
        bar_chart(data=State.rows, x_key="x", value_key="value", title="This week", id="week"),
        bar_chart(data=State.busy_days, x_key="x", value_key="value", title="Busy days", id="busy"),
        sp_steps(items=State.steps, current=State.step, label="Release"),
        rx.foreach(State.tags, lambda tag: rx.el.span(tag)),
        sp_button("Re-roll", on_click=State.reroll),
    )
```

## Controlled and uncontrolled

Every component with a value or an open state works both ways; pick one per component.

| Component | Controlled | Uncontrolled | Handler receives |
|---|---|---|---|
| `sp_input`, `sp_textarea` | `value` + `on_change` | `default_value` | the text, a `str` |
| `sp_input_number` | `value` + `on_change` | `default_value` | a number, or `None` when cleared |
| `sp_checkbox`, `sp_switch` | `checked` + `on_change` | `default_checked` | a `bool` |
| `sp_radio_group`, `sp_segmented`, `sp_tabs` | `value` + `on_change` | `default_value` | the item's key, a `str` |
| `sp_slider`, `sp_rate` | `value` + `on_change` | `default_value` | a number (`float`) |
| `sp_select` | `value` + `on_change` | `default_value` | the option's key, a `str` |
| `sp_pagination` | `current` + `on_change` | `default_current` | the page, an `int` |
| `sp_modal`, `sp_drawer`, `sp_popover`, `sp_tooltip`, `sp_select`, `sp_dropdown_menu`, `sp_toast` | `open` + `on_open_change` | `default_open` | a `bool` |
| `sp_collapse_item` | `open` + `on_toggle` | — | the new open state, a `bool` |
| `sp_table` | `sort_key` + `sort_order` + `on_sort` | — | the column key, a `str` |

- Controlled means the component shows the state's value and asks for a change; the handler must
  write it back, or the control does not move.
- Value events fire on user input only: setting the field from Python does not call `on_change`.
- A text input controlled from state makes a round trip per keystroke. For long text, use
  `default_value`, give it a `name`, and read it from the form's `on_submit` dict, where the native
  inputs submit under their names.

```python
import reflex as rx
from reflex_silverpoint_react import sp_input, sp_input_number, sp_slider, sp_textarea


class State(rx.State):
    volume: int = 30
    quantity: float = 4
    form: dict = {}

    @rx.event
    def set_volume(self, value: float):
        self.volume = int(value)

    @rx.event
    def set_quantity(self, value: float | None):
        self.quantity = value if value is not None else 0

    @rx.event
    def submit(self, form: dict):
        self.form = form


def order() -> rx.Component:
    return rx.el.form(
        sp_slider(label="Volume", min=0, max=100, value=State.volume, on_change=State.set_volume),
        sp_input_number(label="Quantity", min=0, value=State.quantity, on_change=State.set_quantity),
        sp_input(label="Reference", name="reference", default_value="A-1042"),
        sp_textarea(label="Notes", name="notes", default_value=""),
        rx.el.button("Send", type="submit"),
        on_submit=State.submit,
    )
```

## Event payloads

| Event | Payload |
|---|---|
| `on_active_change` (charts) | the item under the pointer or keyboard focus, or `None` when it leaves |
| `on_select` (charts) | the item clicked or chosen with Enter or Space |
| `on_root_change` (`squarified_treemap`, `sunburst_chart`) | the node id to draw as root, `None` at the top |
| `on_link_change` (`dashboard`, `dashboard_link`) | `{"key", "value"}`, or `None` when it clears |
| `on_sort` (`sp_table`) | the column key |
| `on_select` (`sp_dropdown_menu`) | the item's key |
| `on_close` (`sp_tag`, `sp_alert`) | nothing |
| `on_change` (`sp_timeline`) | the `unique_id` of the slide shown |
| `on_loaded` (`sp_timeline`) | TimelineJS's `loaded` payload |

A chart item is `{"seriesKey", "index", "datum", "value", "point": {"x", "y"}}`: `datum` is your row,
so `item["datum"]["hour"]` reads its field. Type the handler's argument `dict | None` for
`on_active_change`. To pass extra arguments, call the handler with them: `on_close=State.remove(tag)`.

## Chart events

```python
import reflex as rx
from reflex_silverpoint_react import line_chart, tooltip_template


class State(rx.State):
    rows: list[dict] = [{"hour": "00", "hits": 18}, {"hour": "12", "hits": 64}]
    active: str = "—"
    picked: list[str] = []

    @rx.event
    def on_active(self, item: dict | None):
        self.active = "—" if item is None else f"{item['datum']['hour']}: {item['value']}"

    @rx.event
    def on_pick(self, item: dict):
        self.picked = [str(item["datum"]["hour"]), *self.picked][:6]


def traffic() -> rx.Component:
    return rx.el.div(
        line_chart(
            data=State.rows,
            x_key="hour",
            value_key="hits",
            title="Traffic",
            id="traffic",
            on_active_change=State.on_active,
            on_select=State.on_pick,
            tooltip=tooltip_template("{datum.hour} h · {value} hits"),
        ),
        rx.el.p(State.active),
    )
```

`tooltip_template(text)` builds the `tooltip` readout from a format string: `{heading}`, `{text}`
(the built-in readout's two lines), `{announcement}`, `{value}`, `{index}`, `{series}` and
`{datum.<field>}`; `{{` and `}}` print braces.

## Drill-down

`squarified_treemap` and `sunburst_chart` keep no root of their own: a click, Enter or Space on a
node sends its id to `on_root_change` (the parent's id from the centre or the frame, `None` at the
top), and you pass it back as `root_id`. Two charts given the same `root_id` drill together.

```python
import reflex as rx
from reflex_silverpoint_react import squarified_treemap, sunburst_chart

BUDGET = [
    {"id": "budget", "parent": None, "name": "City budget"},
    {"id": "works", "parent": "budget", "name": "Public works", "amount": 40},
    {"id": "parks", "parent": "budget", "name": "Parks", "amount": 25},
]
KEYS = {"id_key": "id", "parent_key": "parent", "label_key": "name", "value_key": "amount"}


class State(rx.State):
    root: str | None = None

    @rx.event
    def drill(self, node_id: str | None):
        self.root = node_id


def budget() -> rx.Component:
    return rx.el.div(
        squarified_treemap(data=BUDGET, **KEYS, root_id=State.root, on_root_change=State.drill, id="budget-map"),
        sunburst_chart(data=BUDGET, **KEYS, root_id=State.root, on_root_change=State.drill, id="budget-sun"),
    )
```

## The imperative handle

Give a chart an `id` and its handle is reachable from Python events: `download_svg(id, filename)`
downloads a standalone SVG in the browser; `get_svg(id, handler)` sends the markup to a handler (a
`str`, or `None` when no chart answers) and `get_geometry(id, handler)` the geometry (a `dict`).
`chart_ref(id)` is the name of the Reflex ref those helpers read.

```python
import reflex as rx
from reflex_silverpoint_react import download_svg, get_svg, line_chart


class State(rx.State):
    size: int = 0

    @rx.event
    def receive(self, svg: str | None):
        self.size = len(svg or "")


def export() -> rx.Component:
    return rx.el.div(
        line_chart(title="Hits", id="export-me"),
        rx.el.button("Download SVG", on_click=download_svg("export-me", "hits.svg")),
        rx.el.button("Send to Python", on_click=get_svg("export-me", State.receive)),
    )
```

## Every event

Generated from the catalog: the event props of each builder.

<!-- generated:events -->
