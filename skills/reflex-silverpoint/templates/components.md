# Components

**Contents:** [Usage](#usage) · [Reference](#reference)

The 17 UI components (silverpoint 0.3), the composed components (0.7) and the parts they are built
from. Each is the npm component of `@silverpoint/react/ui`: a native control underneath (a
`<button>`, an `<input>`, a `<fieldset>` of radios, a `<details>`), so forms submit natively and the
keyboard follows the WAI-ARIA patterns. They read `silverpoint_provider` and the dashboard they sit
in; a prop on the component always wins. Overlays are in [overlays.md](overlays.md).

## Usage

- **Shared props:** `id`, `class_name`, `ground`, `substrate`, `mode`, `seed`, `size`
  (`sm`/`md`/`lg`) and `palette`.
- **Values** are controlled (`value=` / `checked=` with `on_change`) or uncontrolled
  (`default_value=` / `default_checked=`). `on_change` receives the new value itself.
- **Items:** `ui_item(key, label, disabled=False)` for tabs, segmented controls and radio groups;
  `step_item(key, title, description=None, status=None)` for steps. A state var holding the same
  dicts works too.
- **Slots:** children are a button's or tag's text, a card's or alert's body; `sp_card` also takes
  `extra` and `footer`, `sp_input` `prefix` and `suffix`.
- **`sp_table` does not sort:** it reports the column in `on_sort`, and you sort with `sort_rows`.
- Text inputs controlled from state make a round trip per keystroke; for long text, use
  `default_value` and read the value on submit (the inputs submit under their `name`).

A settings form, every control bound to state:

```python
import reflex as rx
from reflex_silverpoint_react import sp_button, sp_input, sp_segmented, sp_switch, ui_item


class State(rx.State):
    city: str = "Caracas"
    precision: bool = False
    series: str = "hits"
    submitted: dict = {}

    @rx.event
    def set_city(self, value: str):
        self.city = value

    @rx.event
    def set_precision(self, value: bool):
        self.precision = value

    @rx.event
    def set_series(self, value: str):
        self.series = value

    @rx.event
    def save(self, form: dict):
        self.submitted = form


def settings() -> rx.Component:
    return rx.el.form(
        sp_input(
            label="City",
            name="city",
            value=State.city,
            on_change=State.set_city,
            invalid=State.city == "",
            message="Required: pick a city",
        ),
        sp_switch(label="Precision", name="precision", checked=State.precision, on_change=State.set_precision),
        sp_segmented(
            label="Series",
            name="series",
            items=[ui_item("hits", "Hits"), ui_item("errors", "Errors")],
            value=State.series,
            on_change=State.set_series,
        ),
        sp_button("Save", type="submit", variant="primary"),
        on_submit=State.save,
    )
```

Tabs hold one `sp_tab_panel` per item, matched by `value`:

```python
import reflex as rx
from reflex_silverpoint_react import bar_chart, line_chart, sp_tab_panel, sp_tabs, ui_item


class State(rx.State):
    view: str = "traffic"

    @rx.event
    def set_view(self, value: str):
        self.view = value


def views() -> rx.Component:
    return sp_tabs(
        sp_tab_panel(line_chart(title="Traffic", id="tab-traffic"), value="traffic"),
        sp_tab_panel(bar_chart(title="Errors", id="tab-errors"), value="errors"),
        items=[ui_item("traffic", "Traffic"), ui_item("errors", "Errors")],
        label="Views",
        value=State.view,
        on_change=State.set_view,
    )
```

A sortable, paged table:

```python
import reflex as rx
from reflex_silverpoint_react import sort_rows, sp_pagination, sp_table

COLUMNS = [
    {"key": "team", "title": "Team", "sortable": True},
    {"key": "load", "title": "Load", "align": "end", "sortable": True},
]


class State(rx.State):
    rows: list[dict] = [{"team": "Atlas", "load": 72}, {"team": "Borealis", "load": 41}]
    sort_key: str = ""
    sort_order: str = "asc"
    page: int = 1

    @rx.event
    def sort(self, key: str):
        self.sort_order = "desc" if self.sort_key == key and self.sort_order == "asc" else "asc"
        self.sort_key = key
        self.rows = sort_rows(self.rows, key, self.sort_order)

    @rx.event
    def set_page(self, page: int):
        self.page = page


def teams() -> rx.Component:
    return rx.el.div(
        sp_table(
            COLUMNS,
            State.rows,
            caption="On-call teams",
            sort_key=State.sort_key,
            sort_order=State.sort_order,
            on_sort=State.sort,
            striped=True,
        ),
        sp_pagination(total=240, page_size=10, current=State.page, on_change=State.set_page, show_total=True),
    )
```

Display components take plain values or state vars:

```python
import reflex as rx
from reflex_silverpoint_react import (
    sp_avatar,
    sp_breadcrumb,
    sp_card,
    sp_collapse,
    sp_collapse_item,
    sp_descriptions,
    sp_statistic,
    sp_steps,
    step_item,
)


def overview() -> rx.Component:
    return sp_card(
        sp_breadcrumb([{"label": "Home", "href": "/"}, {"label": "Reports", "href": "#"}]),
        sp_statistic("Revenue", "1,204", prefix="$", trend="up", delta="+8.2 %"),
        sp_descriptions([{"label": "Ground", "value": "silverpoint"}, {"label": "Mode", "value": "ink"}], columns=2),
        sp_steps(items=[step_item("install", "Install"), step_item("import", "Import")], current=1, label="Setup"),
        sp_collapse(sp_collapse_item("What is silverpoint?", "A silver stylus on a prepared ground.")),
        sp_avatar(name="Cennino Cennini"),
        title="Overview",
    )
```

## Reference

<!-- generated:components -->
