"""Pages for 0.7: palettes, the Reflex-composed components and the Knight Lab timeline.

/palettes     Colour for every chart and component: presets, a palette builder, sections.
/components   Level A (table, pagination, breadcrumb, avatar…) and level B (modal, drawer,
              popover, tooltip, select, menu, toast), wired to Python.
/timeline     Knight Lab TimelineJS drawn in silverpoint: skin and hand-inked frames.
"""

from typing import Any

import reflex as rx
from reflex_silverpoint_react import (
    PALETTE_PROPERTIES,
    PALETTES,
    bar_chart,
    check_palette,
    donut_chart,
    line_chart,
    radar_chart,
    silverpoint_palette,
    sort_rows,
    sp_avatar,
    sp_avatar_group,
    sp_breadcrumb,
    sp_button,
    sp_card,
    sp_collapse,
    sp_collapse_item,
    sp_descriptions,
    sp_drawer,
    sp_dropdown_menu,
    sp_empty,
    sp_input_number,
    sp_modal,
    sp_pagination,
    sp_popover,
    sp_progress,
    sp_result,
    sp_select,
    sp_statistic,
    sp_switch,
    sp_table,
    sp_tag,
    sp_textarea,
    sp_timeline,
    sp_timeline_list,
    sp_toast,
    sp_toaster,
    sp_tooltip,
    sp_trigger,
)

from .layout import button, card, code, page, select

GROUNDS = ["silverpoint", "cyanotype"]
SUBSTRATES = ["cream", "green", "blue", "ochre"]
MODES = ["ink", "precision"]
PALETTE_CHOICES = ["none", *PALETTES]
FIELDS = list(PALETTE_PROPERTIES)


def _preset(name: str) -> dict[str, str]:
    preset = PALETTES.get(name)
    return preset.to_dict() if preset else {}


# ── Palettes ────────────────────────────────────────────────────────────────────────────


class PaletteState(rx.State):
    """The palette builder."""

    custom: dict[str, str] = PALETTES["sanguine"].to_dict()
    preset: str = "sanguine"
    section: str = "indigo"

    @rx.event
    def set_field(self, field: str, value: str):
        self.custom = {**self.custom, field: value}

    @rx.event
    def load_preset(self, name: str):
        self.preset = name
        self.custom = _preset(name) or PALETTES["silverpoint"].to_dict()

    @rx.event
    def set_section(self, value: str):
        self.section = value

    @rx.var
    def problems(self) -> list[str]:
        return check_palette(self.custom)

    @rx.var
    def section_fields(self) -> dict[str, str]:
        return _preset(self.section)

    @rx.var
    def code(self) -> str:
        body = "".join(f"    {key}={value!r},\n" for key, value in self.custom.items())
        return (
            "from reflex_silverpoint_react import Palette, bar_chart, check_palette\n\n"
            f"MINE = Palette(\n{body})\n\n"
            "assert not check_palette(MINE)  # contrast thresholds of the data model (§3.2)\n\n"
            'bar_chart(title="Orders", palette=MINE)'
        )


def _swatches(fields: dict[str, str]) -> rx.Component:
    return rx.el.div(
        *[
            rx.el.span(title=f"{key} {value}", style={"background": value}, class_name="demo-swatch")
            for key, value in fields.items()
            if key != "heighten"
        ],
        class_name="demo-swatches",
    )


def _preset_card(name: str) -> rx.Component:
    problems = check_palette(name)
    return card(
        rx.el.div(
            rx.el.strong(name),
            rx.el.span("passes" if not problems else f"{len(problems)} below threshold"),
            class_name="demo-card-title",
        ),
        _swatches(_preset(name)),
        line_chart(title=name.replace("_", " ").title(), palette=name, height=110, footer_right=f'palette="{name}"'),
        rx.el.div(
            sp_button("Primary", variant="primary", palette=name),
            sp_tag("tag", tone=2, palette=name),
            sp_progress(value=64, palette=name),
            style={"display": "flex", "gap": "10px", "alignItems": "center", "marginTop": "10px"},
        ),
    )


def _colour_input(field: str) -> rx.Component:
    return rx.el.div(
        rx.el.label(field.replace("_", " "), html_for=f"pal-{field}"),
        rx.el.input(
            id=f"pal-{field}",
            type="color",
            value=PaletteState.custom[field].to(str),
            on_change=lambda value: PaletteState.set_field(field, value),
            style={"width": "64px", "height": "32px", "padding": "0"},
        ),
        class_name="sp-control",
    )


SECTION_CODE = """silverpoint_palette(
    dashboard(...),            # every chart, UI component and dashboard inside
    sp_card(...),
    palette="indigo",          # a preset, a Palette, a dict or a state var
)

# An element's own palette always wins over its section's:
bar_chart(palette={"ink": "#8A3A24"})"""


def palettes_page() -> rx.Component:
    return page(
        rx.el.h1("Palettes"),
        rx.el.p(
            "silverpoint never writes a colour into its drawing: every stroke is painted by CSS through the --sp- "
            "properties of the ground. A palette sets them, so it re-colours any chart, UI component, dashboard, "
            "Reflex-composed component or timeline without re-rendering. It is monochrome by design: two inks, "
            "tone by hatch density. precision and the system's high-contrast modes still apply on top.",
            class_name="sp-lede",
        ),
        rx.el.h2("Presets"),
        rx.el.p(
            "Named after historical drawing media; each one is verified against the contrast thresholds of the data model."
        ),
        rx.el.div(*[_preset_card(name) for name in PALETTES], class_name="sp-grid"),
        rx.el.h2("Build your own"),
        rx.el.div(
            *[_colour_input(field) for field in FIELDS if field != "focus"],
            select("Start from", PaletteState.preset, list(PALETTES), PaletteState.load_preset),
            class_name="sp-controls",
        ),
        rx.el.div(
            card(bar_chart(title="Orders per quarter", palette=PaletteState.custom, height=140)),
            card(donut_chart(title="Household budget", center_label="%", palette=PaletteState.custom)),
            card(
                sp_card(
                    rx.el.p("UI components take the same palette."),
                    rx.el.div(
                        sp_button("Save", variant="primary", palette=PaletteState.custom),
                        sp_switch(label="Sync", default_checked=True, palette=PaletteState.custom),
                        style={"display": "flex", "gap": "12px", "alignItems": "center"},
                    ),
                    sp_progress(value=72, palette=PaletteState.custom),
                    title="A card",
                    palette=PaletteState.custom,
                ),
            ),
            class_name="sp-grid",
        ),
        card(
            rx.cond(
                PaletteState.problems.length() > 0,
                rx.el.div(
                    rx.el.strong("Below the contrast thresholds:"),
                    rx.foreach(PaletteState.problems, lambda text: rx.el.p(text, class_name="sp-note")),
                ),
                rx.el.p("check_palette: every field passes its contrast threshold.", class_name="sp-note"),
            ),
        ),
        code(PaletteState.code),
        rx.el.h2("A whole section"),
        rx.el.p(
            "silverpoint_palette colours every silverpoint element inside it; an element's own palette still wins."
        ),
        rx.el.div(
            select("Section palette", PaletteState.section, list(PALETTES), PaletteState.set_section),
            class_name="sp-controls",
        ),
        silverpoint_palette(
            rx.el.div(
                card(line_chart(title="In the section")),
                card(radar_chart(title="In the section")),
                card(bar_chart(title="Own palette: sanguine", palette="sanguine")),
                card(sp_card(rx.el.p("A card in the section."), sp_button("Button"), title="Card")),
                class_name="sp-grid",
            ),
            palette=PaletteState.section_fields,
        ),
        code(SECTION_CODE),
    )


# ── Reflex-composed components ──────────────────────────────────────────────────────────

TEAMS = [
    {"team": "Atlas", "region": "North", "load": 72, "incidents": 3},
    {"team": "Borealis", "region": "East", "load": 41, "incidents": 1},
    {"team": "Cygnus", "region": "South", "load": 88, "incidents": 6},
    {"team": "Draco", "region": "West", "load": 15, "incidents": 0},
    {"team": "Eridanus", "region": "North", "load": 57, "incidents": 2},
    {"team": "Fornax", "region": "East", "load": 33, "incidents": 1},
]


class ComposedState(rx.State):
    """State of the components page."""

    ground: str = "silverpoint"
    substrate: str = "cream"
    mode: str = "ink"
    palette: str = "none"

    rows: list[dict[str, Any]] = [dict(row) for row in TEAMS]
    sort_key: str = ""
    sort_order: str = "asc"
    page: int = 3
    quantity: float = 4
    notes: str = "Hatching builds tone; heightening marks the live value."
    modal_open: bool = False
    toast_open: bool = False
    toast_text: str = ""
    region: str = "North"
    log: list[str] = []

    @rx.event
    def set_ground(self, value: str):
        self.ground = value

    @rx.event
    def set_substrate(self, value: str):
        self.substrate = value

    @rx.event
    def set_mode(self, value: str):
        self.mode = value

    @rx.event
    def set_palette(self, value: str):
        self.palette = value

    @rx.var
    def palette_fields(self) -> dict[str, str]:
        return _preset(self.palette)

    @rx.event
    def sort(self, key: str):
        self.sort_order = "desc" if self.sort_key == key and self.sort_order == "asc" else "asc"
        self.sort_key = key
        self.rows = sort_rows(self.rows, key, self.sort_order)

    @rx.event
    def set_page(self, page: int):
        self.page = page
        self._note(f"pagination → page {page}")

    @rx.event
    def set_quantity(self, value: float | None):
        self.quantity = value if value is not None else 0
        self._note(f"input number → {value}")

    @rx.event
    def set_notes(self, value: str):
        self.notes = value

    @rx.event
    def set_modal_open(self, value: bool):
        self.modal_open = value

    @rx.event
    def confirm(self):
        self.modal_open = False
        self.toast_text = "Changes saved."
        self.toast_open = True
        self._note("modal → confirmed")

    @rx.event
    def set_toast_open(self, value: bool):
        self.toast_open = value

    @rx.event
    def show_toast(self):
        self.toast_text = f"Region {self.region}: {len([r for r in self.rows if r['region'] == self.region])} teams."
        self.toast_open = True

    @rx.event
    def set_region(self, value: str):
        self.region = value
        self._note(f"select → {value}")

    @rx.event
    def menu(self, key: str):
        self._note(f"menu → {key}")
        if key == "toast":
            self.show_toast()

    def _note(self, text: str):
        self.log = [text, *self.log][:6]


def _surface() -> dict[str, Any]:
    return {
        "ground": ComposedState.ground,
        "substrate": ComposedState.substrate,
        "mode": ComposedState.mode,
        "palette": ComposedState.palette_fields,
    }


def _section(title: str, *children: rx.Component, snippet: str | None = None) -> list[rx.Component]:
    parts: list[rx.Component] = [rx.el.h2(title), *children]
    if snippet:
        parts.append(code(snippet))
    return parts


TABLE_CODE = """sp_table(
    [{"key": "team", "title": "Team", "sortable": True},
     {"key": "load", "title": "Load", "align": "end", "sortable": True}],
    State.rows,
    caption="On-call teams",
    sort_key=State.sort_key, sort_order=State.sort_order,
    on_sort=State.sort,               # receives the column key; pair it with sort_rows()
    striped=True,
)
sp_pagination(total=240, page_size=10, current=State.page, on_change=State.set_page, show_total=True)"""

OVERLAY_CODE = """sp_modal(
    rx.el.p("Apply the new ground to every chart?"),
    trigger="Open modal",                       # a string becomes sp_trigger(...)
    title="Apply changes", description="…",
    footer=sp_trigger("Apply", variant="primary", on_click=State.confirm),
    open=State.modal_open, on_open_change=State.set_modal_open,
    ground="silverpoint", palette="sepia",       # overlays render in a portal: pass them explicitly
)
sp_select(["North", "East", "South", "West"], value=State.region, on_change=State.set_region)
sp_dropdown_menu("Actions", [{"key": "edit", "label": "Edit", "shortcut": "E"},
                             {"type": "separator"},
                             {"key": "delete", "label": "Delete", "danger": True}], on_select=State.menu)
sp_toaster(sp_toast("Saved", State.toast_text, kind="success", open=State.toast_open,
                    on_open_change=State.set_toast_open))"""


def components_page() -> rx.Component:
    s = _surface()
    return page(
        rx.el.h1("More components"),
        rx.el.p(
            "Built in Reflex on silverpoint's markup contract: the UI stylesheet draws its hand-inked frames, hatched "
            "tones and heightening on any element that follows it. Level A is native markup (a table, details, a "
            "textarea); level B are overlays whose behaviour — focus, keyboard, dismissal, positioning — is Radix's. "
            "They are Reflex-only: silverpoint's React, Vue and Angular adapters do not have them.",
            class_name="sp-lede",
        ),
        rx.el.div(
            select("Ground", ComposedState.ground, GROUNDS, ComposedState.set_ground),
            select("Substrate", ComposedState.substrate, SUBSTRATES, ComposedState.set_substrate),
            select("Mode", ComposedState.mode, MODES, ComposedState.set_mode),
            select("Palette", ComposedState.palette, PALETTE_CHOICES, ComposedState.set_palette),
            class_name="sp-controls",
        ),
        rx.el.p(
            "With the cyanotype ground the page behind the components turns Prussian blue, as a cyanotype print would.",
            style={"color": "var(--muted)", "fontSize": "0.95rem"},
        ),
        card(
            rx.el.strong("Events received by Python: "),
            rx.foreach(
                ComposedState.log, lambda text: rx.el.span(text, class_name="sp-note", style={"marginRight": "6px"})
            ),
        ),
        rx.el.div(
            *_section(
                "Table and pagination",
                sp_table(
                    [
                        {"key": "team", "title": "Team", "sortable": True},
                        {"key": "region", "title": "Region", "sortable": True},
                        {"key": "incidents", "title": "Incidents", "align": "end", "sortable": True},
                        {"key": "load", "title": "Load %", "align": "end", "sortable": True},
                    ],
                    ComposedState.rows,
                    caption="On-call teams",
                    sort_key=ComposedState.sort_key,
                    sort_order=ComposedState.sort_order,
                    on_sort=ComposedState.sort,
                    striped=True,
                    id="teams",
                    **s,
                ),
                rx.el.div(
                    sp_pagination(
                        total=240, current=ComposedState.page, on_change=ComposedState.set_page, show_total=True, **s
                    ),
                    style={"marginTop": "12px"},
                ),
                snippet=TABLE_CODE,
            ),
            *_section(
                "Navigation and identity",
                rx.el.div(
                    sp_breadcrumb(
                        [
                            {"label": "Home", "href": "/"},
                            {"label": "Components", "href": "/components"},
                            {"label": "Breadcrumb"},
                        ],
                        **s,
                    ),
                    rx.el.div(
                        sp_avatar(name="Ernesto Crespo", **s),
                        sp_avatar(name="Cennino Cennini", size="lg", seed=4, **s),
                        sp_avatar(name="Square", shape="square", **s),
                        sp_avatar_group(
                            sp_avatar(name="Atlas", size="sm", **s),
                            sp_avatar(name="Borealis", size="sm", seed=2, **s),
                            sp_avatar(name="Cygnus", size="sm", seed=3, **s),
                            label="On call",
                        ),
                        style={"display": "flex", "gap": "14px", "alignItems": "center"},
                    ),
                    style={"display": "flex", "flexDirection": "column", "gap": "16px"},
                ),
            ),
            *_section(
                "Data display",
                rx.el.div(
                    sp_statistic("Revenue", "1,204", prefix="$", trend="up", delta="+8.2 %", **s),
                    sp_statistic("Uptime", "99.94", suffix="%", **s),
                    sp_statistic("Open incidents", "13", trend="down", delta="−3 since Monday", **s),
                    style={"display": "flex", "gap": "48px", "flexWrap": "wrap"},
                ),
                rx.el.div(
                    sp_descriptions(
                        [
                            {"label": "Package", "value": "reflex-silverpoint-react"},
                            {"label": "Version", "value": "0.7.0"},
                            {"label": "Reflex", "value": "0.10.0"},
                            {"label": "Charts", "value": "60"},
                            {"label": "UI components", "value": "17 + 20 composed"},
                            {"label": "Ground", "value": ComposedState.ground},
                        ],
                        title="Release",
                        **s,
                    ),
                    style={"marginTop": "18px"},
                ),
                rx.el.div(
                    sp_timeline_list(
                        [
                            {"time": "2026-09-25", "title": "0.1.0", "description": "33 charts", "status": "done"},
                            {
                                "time": "2026-10-01",
                                "title": "0.3.0",
                                "description": "17 UI components",
                                "status": "done",
                            },
                            {
                                "time": "2026-10-10",
                                "title": "0.6.0",
                                "description": "60 charts, drill-down",
                                "status": "done",
                            },
                            {
                                "time": "now",
                                "title": "0.7.0",
                                "description": "Palettes, composed components, timeline",
                                "status": "current",
                            },
                            {"time": "next", "title": "1.0.0", "status": "pending"},
                        ],
                        label="Releases",
                        **s,
                    ),
                    style={"marginTop": "18px"},
                ),
            ),
            *_section(
                "Disclosure and feedback",
                sp_collapse(
                    sp_collapse_item(
                        "What is silverpoint?", "Drawing with a silver stylus on a prepared ground.", open=True
                    ),
                    sp_collapse_item(
                        "Why is tone hatched?", "Value is built from hatch density, never flat fill (Art. 6)."
                    ),
                    sp_collapse_item("A disabled panel", "Unreachable.", disabled=True),
                    accordion=True,
                    **s,
                ),
                rx.el.div(
                    sp_empty(sp_trigger("Create a chart", variant="primary", **s), description="No charts yet", **s),
                    sp_result(
                        sp_trigger("Back to the gallery", **s),
                        status="success",
                        title="Published",
                        subtitle="0.7.0 is ready",
                        **s,
                    ),
                    sp_result(status="error", title="Build failed", subtitle="See the log", **s),
                    class_name="sp-grid",
                    style={"marginTop": "16px"},
                ),
            ),
            *_section(
                "Data entry",
                rx.el.div(
                    sp_textarea(
                        value=ComposedState.notes,
                        on_change=ComposedState.set_notes,
                        rows=4,
                        max_length=200,
                        show_count=True,
                        label="Notes",
                        message="Saved with the dashboard.",
                        textarea_id="notes",
                        **s,
                    ),
                    sp_input_number(
                        value=ComposedState.quantity,
                        on_change=ComposedState.set_quantity,
                        min=0,
                        max=10,
                        step=0.5,
                        precision=1,
                        label="Quantity",
                        message="0 to 10, by 0.5",
                        input_id="quantity",
                        **s,
                    ),
                    style={"display": "flex", "gap": "24px", "alignItems": "start", "flexWrap": "wrap"},
                ),
            ),
            *_section(
                "Overlays",
                rx.el.div(
                    sp_modal(
                        rx.el.p("Apply the new ground to every chart of the dashboard?"),
                        trigger="Open modal",
                        title="Apply changes",
                        description="The drawing is re-inked; the data does not change.",
                        footer=rx.el.div(
                            sp_trigger("Cancel", on_click=ComposedState.set_modal_open(False), **s),
                            sp_trigger("Apply", variant="primary", on_click=ComposedState.confirm, **s),
                            style={"display": "flex", "gap": "8px"},
                        ),
                        open=ComposedState.modal_open,
                        on_open_change=ComposedState.set_modal_open,
                        **s,
                    ),
                    sp_drawer(
                        sp_descriptions(
                            [
                                {"label": "Ground", "value": ComposedState.ground},
                                {"label": "Mode", "value": ComposedState.mode},
                            ],
                            columns=1,
                            bordered=False,
                            **s,
                        ),
                        trigger=sp_trigger("Open drawer", **s),
                        title="Settings",
                        description="A panel from the right edge.",
                        **s,
                    ),
                    sp_popover(
                        rx.el.p("Silverpoint cannot be erased: every line stays."),
                        trigger=sp_trigger("Popover", **s),
                        title="A note",
                        closable=True,
                        **s,
                    ),
                    sp_tooltip(sp_trigger("Hover or focus me", **s), "Tooltips use the control frame", **s),
                    sp_select(
                        ["North", "East", "South", "West"],
                        value=ComposedState.region,
                        on_change=ComposedState.set_region,
                        label="Region",
                        **s,
                    ),
                    sp_dropdown_menu(
                        sp_trigger("Actions", chevron=True, **s),
                        [
                            {"key": "edit", "label": "Edit", "shortcut": "E"},
                            {"key": "duplicate", "label": "Duplicate", "shortcut": "D"},
                            {"key": "toast", "label": "Show a toast"},
                            {"type": "separator"},
                            {"type": "label", "label": "Danger zone"},
                            {"key": "delete", "label": "Delete", "danger": True},
                        ],
                        on_select=ComposedState.menu,
                        **s,
                    ),
                    sp_trigger("Toast", on_click=ComposedState.show_toast, **s),
                    style={"display": "flex", "gap": "12px", "flexWrap": "wrap", "alignItems": "center"},
                ),
                snippet=OVERLAY_CODE,
            ),
            class_name="demo-stage",
            custom_attrs={"data-ground": ComposedState.ground},
        ),
        sp_toaster(
            sp_toast(
                "Done",
                ComposedState.toast_text,
                kind="success",
                open=ComposedState.toast_open,
                on_open_change=ComposedState.set_toast_open,
                **s,
            )
        ),
    )


# ── Knight Lab timeline ─────────────────────────────────────────────────────────────────


def _event(year: int, headline: str, text: str, unique_id: str) -> dict[str, Any]:
    return {
        "start_date": {"year": year},
        "text": {"headline": headline, "text": f"<p>{text}</p>"},
        "unique_id": unique_id,
    }


SILVERPOINT_HISTORY: dict[str, Any] = {
    "title": {
        "text": {
            "headline": "Silverpoint",
            "text": "<p>Drawing with a silver stylus on a prepared ground: a line that cannot be erased, "
            "tone built from hatching, white heightening on the light.</p>",
        },
        "unique_id": "title",
    },
    "eras": [
        {"start_date": {"year": 1390}, "end_date": {"year": 1450}, "text": {"headline": "Workshop manuals"}},
        {"start_date": {"year": 1450}, "end_date": {"year": 1530}, "text": {"headline": "Renaissance studies"}},
        {"start_date": {"year": 1530}, "end_date": {"year": 1600}, "text": {"headline": "Graphite arrives"}},
    ],
    "events": [
        _event(
            1400, "Cennini's handbook", "Il libro dell'arte describes how to prepare a ground with bone ash.", "cennini"
        ),
        _event(1435, "Van Eyck", "Portrait of Cardinal Albergati, a silverpoint study for the painting.", "van-eyck"),
        _event(1478, "Leonardo", "Head studies in metalpoint on tinted grounds.", "leonardo"),
        _event(1484, "Dürer at thirteen", "Self-portrait in silverpoint: no correction is possible.", "durer"),
        _event(1503, "Raphael", "Studies for the Madonnas, heightened with white.", "raphael"),
        _event(1565, "Graphite", "Borrowdale graphite reaches the workshops; metalpoint fades.", "graphite"),
    ],
}


class TimelineState(rx.State):
    """State of the timeline page."""

    ground: str = "silverpoint"
    substrate: str = "cream"
    mode: str = "ink"
    palette: str = "none"
    inked: bool = True
    current: str = "title"
    moves: int = 0

    @rx.event
    def set_ground(self, value: str):
        self.ground = value

    @rx.event
    def set_substrate(self, value: str):
        self.substrate = value

    @rx.event
    def set_mode(self, value: str):
        self.mode = value

    @rx.event
    def set_palette(self, value: str):
        self.palette = value

    @rx.event
    def set_inked(self, value: str):
        self.inked = value == "hand-inked"

    @rx.var
    def palette_fields(self) -> dict[str, str]:
        return _preset(self.palette)

    @rx.event
    def on_change(self, unique_id: str):
        self.current = unique_id
        self.moves += 1


TIMELINE_CODE = """from reflex_silverpoint_react import sp_timeline   # pip install "reflex-silverpoint-react[timeline]"

sp_timeline(
    SILVERPOINT_HISTORY,                 # TimelineJS data: title, events, eras
    height=560,
    ground="silverpoint", substrate="cream", mode="ink",
    palette="sepia",                     # any palette
    inked_frames=True,                   # phase 2: the ground's hand-drawn frames and tone tiles
    on_change=State.on_change,           # the unique_id of the slide shown
)"""


def timeline_page() -> rx.Component:
    return page(
        rx.el.h1("Timeline"),
        rx.el.p(
            "Knight Lab TimelineJS (through reflex-knightlab-timeline) drawn in silverpoint. The skin replaces its "
            "colours, type and rules with the ground's; the hand lays the ground's own hand-inked frames and tone "
            "tiles on its markers, eras and buttons. The current marker is heightened; eras are hatched by density.",
            class_name="sp-lede",
        ),
        rx.el.div(
            select("Ground", TimelineState.ground, GROUNDS, TimelineState.set_ground),
            select("Substrate", TimelineState.substrate, SUBSTRATES, TimelineState.set_substrate),
            select("Mode", TimelineState.mode, MODES, TimelineState.set_mode),
            select("Palette", TimelineState.palette, PALETTE_CHOICES, TimelineState.set_palette),
            select(
                "Frames",
                rx.cond(TimelineState.inked, "hand-inked", "skin only"),
                ["hand-inked", "skin only"],
                TimelineState.set_inked,
            ),
            rx.el.p("Slide: ", rx.el.code(TimelineState.current), " · moves: ", TimelineState.moves),
            class_name="sp-controls",
        ),
        rx.cond(
            TimelineState.inked,
            sp_timeline(
                SILVERPOINT_HISTORY,
                height=560,
                inked_frames=True,
                on_change=TimelineState.on_change,
                ground=TimelineState.ground,
                substrate=TimelineState.substrate,
                mode=TimelineState.mode,
                palette=TimelineState.palette_fields,
                id="history",
            ),
            sp_timeline(
                SILVERPOINT_HISTORY,
                height=560,
                inked_frames=False,
                on_change=TimelineState.on_change,
                ground=TimelineState.ground,
                substrate=TimelineState.substrate,
                mode=TimelineState.mode,
                palette=TimelineState.palette_fields,
                id="history-skin",
            ),
        ),
        code(TIMELINE_CODE),
        rx.el.h2("A lighter list"),
        rx.el.p("For a plain sequence of events, sp_timeline_list draws one without TimelineJS."),
        sp_timeline_list(
            [
                {
                    "time": "c. 1400",
                    "title": "Cennini's handbook",
                    "description": "The prepared ground.",
                    "status": "done",
                },
                {"time": "1478", "title": "Leonardo", "description": "Studies on tinted grounds.", "status": "done"},
                {"time": "1503", "title": "Raphael", "description": "Heightened with white.", "status": "current"},
                {"time": "1565", "title": "Graphite", "description": "Metalpoint fades.", "status": "pending"},
            ],
            ground=TimelineState.ground,
            substrate=TimelineState.substrate,
            mode=TimelineState.mode,
            palette=TimelineState.palette_fields,
        ),
        rx.el.p(button("Back to the components", on_click=rx.redirect("/components")), style={"marginTop": "18px"}),
    )
