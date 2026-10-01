"""The UI components of silverpoint 0.3 in the demo.

Pages:
    /ui             The reference panels of the upstream example apps, the components wired to
                    Python state, and a native form submit.
    /ui/<slug>      One page per component: every declared state on both grounds, and its props.
"""

from typing import Any

import reflex as rx
from reflex_silverpoint_react import (
    UI_COMMON_PROPS,
    UI_COMPONENTS,
    UI_DEMOS,
    UI_GROUPS,
    UiComponentInfo,
    bar_chart,
    gauge_arc,
    kpi_card,
    line_chart,
    sp_alert,
    sp_badge,
    sp_button,
    sp_checkbox,
    sp_divider,
    sp_input,
    sp_progress,
    sp_radio_group,
    sp_rate,
    sp_segmented,
    sp_slider,
    sp_steps,
    sp_switch,
    sp_tab_panel,
    sp_tabs,
    sp_tag,
    ui_demo,
    ui_item,
)

from .datasets import OPS_HOURLY
from .layout import card, code, page
from .state import UiState

# ── The reference panels ─────────────────────────────────────────────────────────────────

#: Sections of a panel, ``[component, state]`` pairs, as the upstream ``UI_PAGE`` orders them.
UI_PAGE_SECTIONS: list[tuple[str, list[tuple[str, str]]]] = [
    ("Button", [("button", "default"), ("button", "primary"), ("button", "danger"), ("button", "disabled")]),
    ("Input", [("input", "empty"), ("input", "invalid")]),
    (
        "Checkbox · Switch",
        [
            ("checkbox", "checked"),
            ("checkbox", "indeterminate"),
            ("checkbox", "unchecked"),
            ("switch", "on"),
            ("switch", "off"),
        ],
    ),
    ("RadioGroup · Rate", [("radio-group", "selected"), ("rate", "three")]),
    ("Slider", [("slider", "marks")]),
    ("Segmented", [("segmented", "middle")]),
    ("Steps", [("steps", "current")]),
    ("Progress", [("progress", "line"), ("progress", "circle"), ("progress", "indeterminate")]),
    ("Skeleton", [("skeleton", "avatar")]),
    ("Tabs", [("tabs", "disabled-tab")]),
    (
        "Card · Tag · Badge",
        [
            ("card", "titled"),
            ("tag", "tone-1"),
            ("tag", "closable"),
            ("badge", "count"),
            ("badge", "dot"),
            ("badge", "overflow"),
        ],
    ),
    ("Alert", [("alert", "info"), ("alert", "success"), ("alert", "warning"), ("alert", "error")]),
    ("Divider", [("divider", "text")]),
]

#: The three panels: the same sections under their own ground, substrate and mode.
UI_PAGE_PANELS: list[dict[str, str]] = [
    {
        "key": "silverpoint",
        "title": "silverpoint · cream · ink",
        "note": "Tone by hatching, heightening on the current item",
        "ground": "silverpoint",
        "substrate": "cream",
        "mode": "ink",
    },
    {
        "key": "precision",
        "title": "precision mode",
        "note": "Same components, inking switched off",
        "ground": "silverpoint",
        "substrate": "cream",
        "mode": "precision",
    },
    {
        "key": "cyanotype",
        "title": "cyanotype · prussian",
        "note": "Tone is the weight of an exact white line",
        "ground": "cyanotype",
        "substrate": "prussian",
        "mode": "ink",
    },
]


def demo_item(prefix: str, slug: str, state: str, look: dict[str, Any]) -> rx.Component:
    """One reference state, under a panel's look and an id of its own.

    The Card holds a KPI and its sparkline, as upstream's concept draws it; the Tabs get a panel
    per tab.
    """
    demo = UI_DEMOS[slug][state]
    props: dict[str, Any] = {"id": f"{prefix}-{demo['id']}", **look}
    if slug == "card":
        kpi = kpi_card(id=f"{prefix}-card-kpi", width=280, metric="thousands", **look)
        return ui_demo(slug, state, kpi, heading_level=4, **props)
    if slug == "tabs":
        panels = [
            sp_tab_panel(f"{item['label']}: the charts of this view.", value=item["key"]) for item in demo["items"]
        ]
        return ui_demo(slug, state, *panels, **props)
    return ui_demo(slug, state, **props)


def reference_panel(panel: dict[str, str]) -> rx.Component:
    """A panel of every section, as a form: its radios and inputs are grouped and submitted by it."""
    look = {"ground": panel["ground"], "substrate": panel["substrate"], "mode": panel["mode"]}
    return rx.el.form(
        rx.el.h2(panel["title"], id=f"{panel['key']}-title"),
        rx.el.p(panel["note"], class_name="demo-ui-panel-note"),
        rx.el.div(
            *[
                rx.el.section(
                    rx.el.h3(title),
                    rx.el.div(
                        *[demo_item(panel["key"], slug, state, look) for slug, state in items],
                        class_name="demo-ui-items",
                    ),
                    class_name="demo-ui-section",
                    aria_label=title,
                )
                for title, items in UI_PAGE_SECTIONS
            ],
            class_name="demo-ui-sections",
        ),
        on_submit=rx.prevent_default,
        class_name=f"demo-ui-panel sp-ground-{panel['ground']}",
        custom_attrs={"data-substrate": panel["substrate"], "aria-labelledby": f"{panel['key']}-title"},
    )


# ── Wired to Python ──────────────────────────────────────────────────────────────────────

UI_CODE = """from reflex_silverpoint_react import sp_button, sp_input, sp_segmented, sp_switch, ui_item

class State(rx.State):
    city: str = "Caracas"
    precision: bool = False
    series: str = "hits"
    ...

rx.el.form(
    sp_input(label="City", name="city", value=State.city, on_change=State.set_city,
             invalid=State.city_invalid, message=State.city_message),
    sp_switch(label="Precision", checked=State.precision, on_change=State.set_precision),
    sp_segmented(label="Series", name="series", value=State.series, on_change=State.set_series,
                 items=[ui_item("hits", "Hits"), ui_item("errors", "Errors"), ui_item("load", "Load")]),
    sp_button("Save", type="submit", variant="primary"),
    on_submit=State.submit,   # receives {"city": "Caracas", "series": "hits", ...}
)"""

SUBSTRATE_ITEMS = [ui_item(s, s) for s in ("cream", "green", "blue", "ochre")]
SIZE_ITEMS = [ui_item("sm", "sm"), ui_item("md", "md"), ui_item("lg", "lg")]
SERIES_ITEMS = [ui_item("hits", "Hits"), ui_item("errors", "Errors"), ui_item("load", "Load")]
VIEW_ITEMS = [ui_item("traffic", "Traffic"), ui_item("errors", "Errors"), ui_item("capacity", "Capacity")]


def wired_panel() -> rx.Component:
    """Controlled components: every value lives in ``UiState`` and every change goes through Python."""
    look = {"ground": UiState.ground, "substrate": UiState.substrate, "mode": UiState.mode, "size": UiState.size}
    return rx.el.div(
        rx.el.div(
            sp_radio_group(
                id="look-ground",
                label="Ground",
                name="ground",
                items=[ui_item("silverpoint", "silverpoint"), ui_item("cyanotype", "cyanotype")],
                orientation="horizontal",
                value=UiState.ground,
                on_change=UiState.set_ground,
                **look,
            ),
            sp_segmented(
                id="look-substrate",
                label="Substrate (silverpoint)",
                name="substrate",
                items=SUBSTRATE_ITEMS,
                value=UiState.substrate,
                on_change=UiState.set_substrate,
                **look,
            ),
            sp_segmented(
                id="look-size",
                label="Size",
                name="size",
                items=SIZE_ITEMS,
                value=UiState.size,
                on_change=UiState.set_size,
                **look,
            ),
            sp_switch(
                id="look-precision",
                label="Precision",
                checked=UiState.precision,
                on_change=UiState.set_precision,
                **look,
            ),
            class_name="demo-ui-row",
        ),
        sp_divider(text="a form, submitted natively", **look),
        rx.el.form(
            rx.el.div(
                sp_input(
                    id="form-city",
                    label="City",
                    name="city",
                    value=UiState.city,
                    on_change=UiState.set_city,
                    invalid=UiState.city_invalid,
                    message=UiState.city_message,
                    **look,
                ),
                sp_checkbox(
                    id="form-newsletter",
                    label="Send me the release notes",
                    name="newsletter",
                    checked=UiState.newsletter,
                    on_change=UiState.set_newsletter,
                    **look,
                ),
                sp_rate(
                    id="form-quality",
                    label="Quality",
                    name="quality",
                    value=UiState.quality,
                    on_change=UiState.set_quality,
                    **look,
                ),
                class_name="demo-ui-row",
            ),
            sp_slider(
                id="form-volume",
                label="Volume",
                name="volume",
                marks=[0, 25, 50, 75, 100],
                value=UiState.volume,
                on_change=UiState.set_volume,
                **look,
            ),
            rx.el.div(
                sp_button("Save", type="submit", variant="primary", **look),
                sp_button("Reset", type="reset", **look),
                sp_button("Docs", href="https://github.com/ecrespo/silverpoint", **look),
                class_name="demo-ui-row",
            ),
            on_submit=UiState.submit,
            reset_on_submit=False,
            class_name="demo-ui-stack",
        ),
        sp_divider(text="driven by buttons", **look),
        rx.el.div(
            sp_progress(id="live-progress", label=UiState.progress_label, value=UiState.progress, **look),
            sp_progress(id="live-ring", label="Coverage", shape="circle", value=UiState.progress, **look),
            sp_button("+20 %", on_click=UiState.advance, **look),
            sp_button("Restart", on_click=UiState.restart, **look),
            class_name="demo-ui-row",
        ),
        sp_steps(id="live-steps", label="Release", items=UiState.release_items, current=UiState.step, **look),
        rx.el.div(
            sp_button("Back", on_click=UiState.previous_step, **look),
            sp_button("Next", variant="primary", on_click=UiState.next_step, **look),
            sp_badge("Inbox", id="live-inbox", count=UiState.inbox, label="unread messages", **look),
            sp_button("New message", on_click=UiState.receive, **look),
            sp_button("Mark all read", on_click=UiState.read_all, **look),
            class_name="demo-ui-row",
        ),
        rx.el.div(
            rx.foreach(
                UiState.tags,
                lambda tag: sp_tag(tag, closable=True, tone=2, on_close=UiState.remove_tag(tag), **look),
            ),
            sp_button("Restore tags", on_click=UiState.reset_tags, **look),
            class_name="demo-ui-row",
        ),
        rx.cond(
            UiState.alert_open,
            sp_alert(
                "Changes in this panel are sent to Python and come back as props.",
                id="live-alert",
                kind="success",
                title="Wired to the backend",
                closable=True,
                on_close=UiState.close_alert,
                **look,
            ),
            sp_button("Show the alert again", on_click=UiState.open_alert, **look),
        ),
        sp_divider(text="tabs that hold charts", **look),
        sp_segmented(
            id="live-series",
            label="Series",
            name="series",
            items=SERIES_ITEMS,
            value=UiState.series,
            on_change=UiState.set_series,
            **look,
        ),
        sp_tabs(
            sp_tab_panel(
                rx.match(
                    UiState.series,
                    *[
                        (
                            key,
                            line_chart(
                                data=OPS_HOURLY,
                                x_key="hour",
                                value_key=key,
                                title=label,
                                chrome="bare",
                                width=600,
                                ground=UiState.ground,
                                substrate=UiState.substrate,
                                mode=UiState.mode,
                            ),
                        )
                        for key, label in (("hits", "Hits"), ("errors", "Errors"), ("load", "Load"))
                    ],
                    rx.fragment(),
                ),
                value="traffic",
            ),
            sp_tab_panel(
                bar_chart(
                    data=OPS_HOURLY,
                    x_key="hour",
                    value_key="errors",
                    title="Errors",
                    chrome="bare",
                    width=600,
                    ground=UiState.ground,
                    substrate=UiState.substrate,
                    mode=UiState.mode,
                ),
                value="errors",
            ),
            sp_tab_panel(
                gauge_arc(
                    percent=UiState.volume,
                    caption="The slider's value",
                    title="Capacity",
                    chrome="bare",
                    width=600,
                    ground=UiState.ground,
                    substrate=UiState.substrate,
                    mode=UiState.mode,
                ),
                value="capacity",
            ),
            id="live-tabs",
            label="Views",
            items=VIEW_ITEMS,
            value=UiState.view,
            on_change=UiState.set_view,
            **look,
        ),
        class_name=rx.cond(
            UiState.ground == "cyanotype",
            "demo-ui-panel demo-ui-stack sp-ground-cyanotype",
            "demo-ui-panel demo-ui-stack sp-ground-silverpoint",
        ),
        custom_attrs={"data-substrate": rx.cond(UiState.ground == "cyanotype", "prussian", UiState.substrate)},
    )


def ui_page() -> rx.Component:
    return page(
        rx.el.h1("UI components"),
        rx.el.p(
            "New in silverpoint 0.3: seventeen interface components drawn as the charts are. Frames are hand-drawn "
            "once by each ground's own inker; tone is hatching on silverpoint and the weight of an exact white line "
            "on cyanotype; precision mode switches the inking off. Underneath, each one is a native control, so forms "
            "submit and the keyboard follows the WAI-ARIA patterns.",
            class_name="sp-lede",
        ),
        rx.el.p(
            *[
                part
                for group, title in UI_GROUPS
                for part in (
                    rx.el.strong(f"{title}: "),
                    *[
                        piece
                        for info in UI_COMPONENTS
                        if info.group == group
                        for piece in (rx.el.a(info.component, href=f"/ui/{info.slug}"), " ")
                    ],
                    rx.el.br(),
                )
            ],
        ),
        rx.el.h2("Wired to Python"),
        rx.el.p(
            "Every component below is controlled: its value lives in a Reflex state var and on_change sends the new "
            "value (a string, a bool or a number, never a DOM event) to Python. The radio group, the segmented "
            "controls and the switch restyle the whole panel. Save submits the form natively: the components' inputs "
            "submit under their name."
        ),
        rx.el.div(
            wired_panel(),
            card(
                rx.el.p(rx.el.strong("Submitted: ")),
                rx.el.p(UiState.submitted, class_name="sp-note"),
                rx.el.p(rx.el.strong("Events (latest first):")),
                rx.foreach(UiState.events, lambda text: rx.el.p(text, class_name="sp-note")),
            ),
            class_name="sp-grid-2",
            style={"gridTemplateColumns": "minmax(0, 2fr) minmax(0, 1fr)", "alignItems": "start"},
        ),
        rx.el.h3("In your code"),
        code(UI_CODE),
        rx.el.h2("The reference panels"),
        rx.el.p(
            "The page every upstream example app ships at /ui: the reference states of the catalog, uncontrolled "
            "(ui_demo passes each demo's value as its default), in three panels that differ only in ground, substrate "
            "and mode."
        ),
        rx.el.div(*[reference_panel(panel) for panel in UI_PAGE_PANELS], class_name="demo-ui-panels"),
    )


# ── One page per component ───────────────────────────────────────────────────────────────


def _props_table(props) -> rx.Component:
    return rx.el.table(
        rx.el.thead(
            rx.el.tr(rx.el.th("Python prop"), rx.el.th("React prop"), rx.el.th("Type"), rx.el.th("What it does"))
        ),
        rx.el.tbody(
            *[
                rx.el.tr(
                    rx.el.td(rx.el.code(p.name)),
                    rx.el.td(rx.el.code(p.js)),
                    rx.el.td(rx.el.code(p.type)),
                    rx.el.td(p.doc or "—"),
                )
                for p in props
            ]
        ),
        class_name="sp-props",
    )


def ui_usage(info: UiComponentInfo) -> str:
    """The Python that renders the component's first declared state."""
    demo = {k: v for k, v in UI_DEMOS[info.slug][info.states[0]].items() if k != "id"}
    content = demo.pop("content", None)
    if "value" in demo and info.slug != "progress":
        value = demo.pop("value")
        bound = "checked" if isinstance(value, bool) else "value"
        demo[bound] = f"State.{demo.get('name', 'value')}"
        demo["on_change"] = f"State.set_{demo.get('name', 'value')}"
    lines = [f"from reflex_silverpoint_react import {info.factory_name}", "", f"{info.factory_name}("]
    if content is not None:
        lines.append(f"    {content!r},")
    for key, value in demo.items():
        shown = value if isinstance(value, str) and value.startswith("State.") else repr(value)
        lines.append(f"    {key}={shown},")
    lines.append(")")
    return "\n".join(lines)


def ui_component_page(info: UiComponentInfo):
    def render() -> rx.Component:
        looks = [panel for panel in UI_PAGE_PANELS if panel["key"] != "precision"]
        return page(
            rx.el.p(
                *[
                    item
                    for other in UI_COMPONENTS
                    for item in (
                        rx.el.a(
                            other.component,
                            href=f"/ui/{other.slug}",
                            style={"fontWeight": "600"} if other is info else {},
                        ),
                        " · ",
                    )
                ][:-1],
                style={"fontSize": "0.9rem", "color": "var(--muted)"},
            ),
            rx.el.h1(info.component),
            rx.el.p(
                info.summary,
                " Group: ",
                dict(UI_GROUPS)[info.group],
                ". npm: @silverpoint/react/ui/",
                info.slug,
                ".",
                class_name="sp-lede",
            ),
            rx.el.div(
                *[
                    rx.el.div(
                        rx.el.h2(f"{look['ground']} · {look['substrate']}"),
                        # One form per state: two states' radios share a name, and a form groups them.
                        *[
                            rx.el.form(
                                rx.el.h3(state),
                                rx.el.div(
                                    demo_item(
                                        f"{look['key']}-page",
                                        info.slug,
                                        state,
                                        {"ground": look["ground"], "substrate": look["substrate"]},
                                    ),
                                    class_name="demo-ui-items",
                                ),
                                on_submit=rx.prevent_default,
                                class_name="demo-ui-section",
                            )
                            for state in info.states
                        ],
                        class_name=f"demo-ui-panel demo-ui-stack sp-ground-{look['ground']}",
                        custom_attrs={"data-substrate": look["substrate"]},
                    )
                    for look in looks
                ],
                class_name="sp-grid-2",
            ),
            rx.el.h2("Usage"),
            code(ui_usage(info)),
            rx.el.h2("Its own props"),
            _props_table(info.props) if info.props else rx.el.p("None besides the common ones."),
            rx.el.h2("Props every UI component takes"),
            _props_table(UI_COMMON_PROPS),
        )

    render.__name__ = f"ui_{info.factory_name}"
    return render
