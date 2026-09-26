"""Demo of reflex-silverpoint-react: the 33 silverpoint charts in Reflex.

Pages:
    /               Start: quickstart, provider, precision mode.
    /gallery        Every chart, with ground controls and demo-vs-state data.
    /playground     One chart, every rendering choice, and the Python to reproduce it.
    /interaction    Events, custom tooltips, a turning volvelle, live data and SVG export.
    /chart/<slug>   One page per chart, with the reference of its props.
"""

from typing import Any

import reflex as rx
from reflex_silverpoint_react import (
    CHARTS,
    COMMON_PROPS,
    FAMILIES,
    ChartInfo,
    PropDoc,
    bar_chart,
    donut_chart,
    download_svg,
    gauge_arc,
    get_geometry,
    get_svg,
    heatmap_chart,
    kpi_card,
    line_chart,
    meter_chart,
    radar_chart,
    sankey_chart,
    silverpoint_provider,
    tooltip_template,
    volvelle_chart,
)

from .datasets import BAR_CHART, DONUT_CHART, HEATMAP_CHART, KEY_PROPS, LINE_CHART, VOLVELLE_CHART
from .layout import button, card, code, page, select
from .state import SIZES, DemoState, InteractionState, PlaygroundState

SUBSTRATES = ["cream", "green", "blue", "ochre"]
MODES = ["ink", "precision"]
HATCH_FILLS = ["tile", "per-shape"]


# ── Charts fed from state ─────────────────────────────────────────────────────────────────


def state_chart(info: ChartInfo, **common: Any) -> rx.Component:
    """A chart fed from ``DemoState`` instead of its own demo dataset.

    Args:
        info: The chart.
        **common: Props shared by every chart on the page.

    Returns:
        The chart.
    """
    slug = info.slug
    if slug == "gauge-arc":
        return info.factory(percent=DemoState.gauge_percent, caption="Capacity used", **common)
    if slug == "meter-chart":
        return info.factory(percent=DemoState.meter_percent, caption="Load", **common)
    if slug == "kpi-card":
        return info.factory(data=DemoState.datasets[slug], metric="orders per day", delta=DemoState.kpi_delta, **common)
    return info.factory(data=DemoState.datasets[slug], **KEY_PROPS.get(slug, {}), **common)


def gallery_card(info: ChartInfo) -> rx.Component:
    common = {"title": info.chart, "footer_right": "silverpoint", "hatch_fill": DemoState.hatch_fill}
    return card(
        rx.el.div(
            rx.el.a(info.chart, href=f"/chart/{info.slug}"),
            rx.el.span(info.family),
            class_name="sp-card-title",
        ),
        rx.cond(DemoState.use_state_data, state_chart(info, **common), info.factory(**common)),
    )


# ── Start ───────────────────────────────────────────────────────────────────────────────

QUICKSTART = """import reflex as rx
from reflex_silverpoint_react import line_chart

DATA = [
    {"hour": "00", "hits": 18},
    {"hour": "04", "hits": 11},
    {"hour": "08", "hits": 42},
    {"hour": "12", "hits": 64},
    {"hour": "16", "hits": 57},
    {"hour": "20", "hits": 30},
]


def index() -> rx.Component:
    return rx.box(
        line_chart(data=DATA, x_key="hour", value_key="hits", title="Hits per hour"),
        width="480px",
    )


app = rx.App()
app.add_page(index)"""

PROVIDER_CODE = """silverpoint_provider(
    bar_chart(data=sales, x_key="month", value_key="units", title="Units sold", unit="units"),
    donut_chart(data=channels, name_key="channel", value_key="share",
                title="Sales by channel", center_label="%"),
    ground="silverpoint",
    substrate="green",
    locale="en-GB",
)"""

SALES = [{"month": "Jan", "units": 120}, {"month": "Feb", "units": 98}, {"month": "Mar", "units": 143}]
CHANNELS = [{"channel": "Web", "share": 54}, {"channel": "Stores", "share": 31}, {"channel": "Partners", "share": 15}]


def index() -> rx.Component:
    return page(
        rx.el.h1("silverpoint, in Reflex"),
        rx.el.p(
            "Charts drawn in the manner of a Renaissance silverpoint drawing: a fine silver line on a "
            "prepared ground, tone built from hatching, and white heightening on the live value. The "
            "hand-drawn irregularity lives only in the ornament; the data geometry is exact, and every "
            "chart has a precision mode that turns the inking off. All 33 charts of @silverpoint/react, "
            "as Python components.",
            class_name="sp-lede",
        ),
        rx.el.div(
            card(
                line_chart(
                    data=LINE_CHART,
                    **KEY_PROPS["line-chart"],
                    title="Throughput per hour",
                    badge="Live",
                    value=88,
                    unit="requests",
                    footer_left="00–22 h",
                    footer_right="silverpoint",
                )
            ),
            card(donut_chart(title="Household budget", center_label="%", footer_right="silverpoint")),
            card(radar_chart(title="Product scores", footer_right="silverpoint")),
            class_name="sp-grid",
        ),
        rx.el.h2("Quickstart"),
        rx.el.p(
            "Install the package; Reflex installs the npm side (@silverpoint/react, grounds and fonts) and imports the stylesheets for you."
        ),
        code("pip install reflex-silverpoint-react"),
        code(QUICKSTART),
        rx.el.h2("One ground for the whole app"),
        rx.el.p(
            "silverpoint_provider sets the ground, the substrate, the mode and the locale for every chart below it. A prop on a chart always wins."
        ),
        rx.el.div(
            card(
                silverpoint_provider(
                    rx.el.div(
                        bar_chart(data=SALES, x_key="month", value_key="units", title="Units sold", unit="units"),
                        donut_chart(
                            data=CHANNELS,
                            name_key="channel",
                            value_key="share",
                            title="Sales by channel",
                            center_label="%",
                        ),
                        class_name="sp-grid-2",
                    ),
                    ground="silverpoint",
                    substrate="green",
                    locale="en-GB",
                ),
            ),
            code(PROVIDER_CODE),
            class_name="sp-grid-2",
        ),
        rx.el.h2("Ink and precision"),
        rx.el.p(
            'mode="precision" switches the inking off and draws exact, even strokes: for print, dense dashboards '
            "and readers who prefer it. The charts switch to it by themselves under prefers-contrast: more or forced-colors."
        ),
        rx.el.div(
            card(heatmap_chart(title="Load by weekday · ink", footer_right='mode="ink"')),
            card(heatmap_chart(title="Load by weekday · precision", mode="precision", footer_right='mode="precision"')),
            card(sankey_chart(title="Signup flow · ink", substrate="ochre", footer_right='substrate="ochre"')),
            card(
                sankey_chart(
                    title="Signup flow · precision",
                    substrate="ochre",
                    mode="precision",
                    footer_right='mode="precision"',
                )
            ),
            class_name="sp-grid",
        ),
        rx.el.p(
            rx.el.a("See the 33 charts in the gallery", href="/gallery"),
            ", try every rendering choice in the ",
            rx.el.a("playground", href="/playground"),
            ", or wire events in ",
            rx.el.a("interaction", href="/interaction"),
            ".",
        ),
    )


# ── Gallery ─────────────────────────────────────────────────────────────────────────────


def gallery() -> rx.Component:
    families = []
    for family in FAMILIES:
        members = [info for info in CHARTS if info.family == family]
        families.append(rx.el.h2(f"{family} · {len(members)}", class_name="sp-family"))
        families.append(rx.el.div(*[gallery_card(info) for info in members], class_name="sp-grid"))
    return page(
        rx.el.h1("Gallery"),
        rx.el.p(
            f"The {len(CHARTS)} charts. With “demo datasets”, each chart draws the data it ships with, "
            "which is what it shows before it is given any. With “Python state”, every chart is fed from "
            "a Reflex state var: re-roll to see the charts redraw from the backend.",
            class_name="sp-lede",
        ),
        rx.el.div(
            select("Substrate", DemoState.substrate, SUBSTRATES, DemoState.set_substrate),
            select("Mode", DemoState.mode, MODES, DemoState.set_mode),
            select("Hatch fill", DemoState.hatch_fill, HATCH_FILLS, DemoState.set_hatch_fill),
            rx.el.div(
                rx.el.label("Data"),
                rx.el.div(
                    button("Demo datasets", on_click=DemoState.set_use_state_data(False)),
                    button("Python state", on_click=DemoState.set_use_state_data(True)),
                    style={"display": "flex", "gap": "6px"},
                ),
                class_name="sp-control",
            ),
            button("Re-roll data", on_click=DemoState.reroll_all),
            button("Reset", on_click=DemoState.reset_data),
            rx.el.p(
                rx.cond(DemoState.use_state_data, "Source: Python state · rolls: ", "Source: demo datasets · rolls: "),
                DemoState.rolls,
                style={"color": "var(--muted)"},
            ),
            class_name="sp-controls",
        ),
        silverpoint_provider(*families, substrate=DemoState.substrate, mode=DemoState.mode),
    )


# ── Playground ──────────────────────────────────────────────────────────────────────────


def playground() -> rx.Component:
    common = {
        "substrate": PlaygroundState.substrate,
        "mode": PlaygroundState.mode,
        "hatch_fill": PlaygroundState.hatch_fill,
        "chrome": PlaygroundState.chrome,
        "data_table": PlaygroundState.data_table,
        "seed": PlaygroundState.seed,
        "width": PlaygroundState.width,
        "height": PlaygroundState.height,
        "footer_right": "silverpoint",
    }
    return page(
        rx.el.h1("Ground playground"),
        rx.el.p(
            "One chart, every rendering choice. The data never changes: only the substrate, the inking, the way "
            "tone is hatched, the frame, the size and the seed of the hand.",
            class_name="sp-lede",
        ),
        rx.el.div(
            select("Chart", PlaygroundState.chart, [info.chart for info in CHARTS], PlaygroundState.set_chart),
            select("Substrate", PlaygroundState.substrate, SUBSTRATES, PlaygroundState.set_substrate),
            select("Mode", PlaygroundState.mode, MODES, PlaygroundState.set_mode),
            select("Hatch fill", PlaygroundState.hatch_fill, HATCH_FILLS, PlaygroundState.set_hatch_fill),
            select("Chrome", PlaygroundState.chrome, ["card", "bare"], PlaygroundState.set_chrome),
            select(
                "Data table", PlaygroundState.data_table, ["hidden", "visible", "none"], PlaygroundState.set_data_table
            ),
            select("Size", PlaygroundState.size, list(SIZES), PlaygroundState.set_size),
            rx.el.div(
                rx.el.label("Seed", html_for="ctl-seed"),
                rx.el.input(
                    id="ctl-seed", type="number", value=PlaygroundState.seed, on_change=PlaygroundState.set_seed
                ),
                class_name="sp-control",
            ),
            button("New hand", on_click=PlaygroundState.new_seed),
            class_name="sp-controls",
        ),
        card(
            rx.match(
                PlaygroundState.chart,
                *[(info.chart, info.factory(title=info.chart, **common)) for info in CHARTS],
                rx.el.p("Pick a chart."),
            ),
            style={"width": "fit-content", "maxWidth": "100%"},
        ),
        rx.el.h3("In your code"),
        code(PlaygroundState.code),
    )


# ── Interaction ─────────────────────────────────────────────────────────────────────────


def interaction() -> rx.Component:
    on = {"on_active_change": InteractionState.on_active, "on_select": InteractionState.on_select}
    return page(
        rx.el.h1("Interaction"),
        rx.el.p(
            "Every chart reports the item under the pointer or keyboard focus (on_active_change) and the item "
            "chosen by click, Enter or Space (on_select) to Python. Focus a chart with Tab and move with the arrow keys.",
            class_name="sp-lede",
        ),
        rx.el.h2("Events and a custom readout"),
        rx.el.div(
            card(
                line_chart(
                    data=LINE_CHART,
                    **KEY_PROPS["line-chart"],
                    title="Hits per hour",
                    tooltip=tooltip_template("{datum.hour} h · {value} hits"),
                    footer_right='tooltip_template("{datum.hour} h · {value} hits")',
                    **on,
                ),
            ),
            card(bar_chart(data=BAR_CHART, **KEY_PROPS["bar-chart"], title="Orders per quarter", unit="orders", **on)),
            card(donut_chart(data=DONUT_CHART, title="Household budget", center_label="%", **on)),
            card(
                heatmap_chart(
                    data=HEATMAP_CHART,
                    title="Load by weekday",
                    column_labels=["6h", "9h", "12h", "15h", "18h", "21h"],
                    **on,
                )
            ),
            class_name="sp-grid-2",
        ),
        card(
            rx.el.p(rx.el.strong("Under the pointer: "), InteractionState.active, class_name="sp-note"),
            rx.el.p(rx.el.strong("Selected (latest first):")),
            rx.foreach(InteractionState.selections, lambda text: rx.el.p(text, class_name="sp-note")),
            button("Clear", on_click=InteractionState.clear_selections),
        ),
        rx.el.h2("A volvelle that turns"),
        rx.el.p(
            "Click any segment: on_select sends it to Python, which sets index_ring and index_value, and the wheel turns that segment under the index."
        ),
        rx.el.div(
            card(
                volvelle_chart(
                    # index_ring / index_value only apply to your own rings, so pass data explicitly.
                    data=VOLVELLE_CHART,
                    title="On-call wheel",
                    index_ring=InteractionState.volvelle_ring,
                    index_value=InteractionState.volvelle_value,
                    on_select=InteractionState.volvelle_select,
                    height=260,
                    footer_left="click a segment",
                ),
            ),
            card(
                rx.el.p("index_ring = ", InteractionState.volvelle_ring, class_name="sp-note"),
                rx.el.p("index_value = ", InteractionState.volvelle_value, class_name="sp-note"),
            ),
            class_name="sp-grid-2",
        ),
        rx.el.h2("Live values from the backend"),
        rx.el.div(
            card(
                kpi_card(
                    data=InteractionState.kpi_series,
                    metric="orders per day",
                    delta=InteractionState.kpi_delta,
                    title="Orders",
                ),
                rx.el.div(button("Next day", on_click=InteractionState.tick_kpi), style={"marginTop": "10px"}),
            ),
            card(
                gauge_arc(percent=DemoState.gauge_percent, caption="Capacity used", title="Capacity"),
                rx.slider(
                    value=[DemoState.gauge_percent],
                    on_change=DemoState.set_gauge_percent,
                    min=0,
                    max=100,
                    margin_top="14px",
                ),
            ),
            card(
                meter_chart(percent=DemoState.meter_percent, caption="Load", title="Load"),
                rx.slider(
                    value=[DemoState.meter_percent],
                    on_change=DemoState.set_meter_percent,
                    min=0,
                    max=100,
                    margin_top="14px",
                ),
            ),
            class_name="sp-grid",
        ),
        rx.el.h2("The imperative handle: export"),
        rx.el.p(
            "Give a chart an id and its ChartHandle is reachable from Python helpers: download_svg downloads a "
            "standalone SVG in the browser; get_svg and get_geometry send the markup or the geometry to a handler."
        ),
        rx.el.div(
            card(
                line_chart(
                    id="export-me", data=LINE_CHART, **KEY_PROPS["line-chart"], title="Exportable", substrate="blue"
                )
            ),
            card(
                rx.el.div(
                    button("Download SVG", on_click=download_svg("export-me", "hits-per-hour.svg")),
                    button("Send SVG to Python", on_click=get_svg("export-me", InteractionState.receive_svg)),
                    button(
                        "Send geometry to Python", on_click=get_geometry("export-me", InteractionState.receive_geometry)
                    ),
                    style={"display": "flex", "flexWrap": "wrap", "gap": "8px"},
                ),
                rx.el.p(InteractionState.svg_report, class_name="sp-note"),
                rx.el.p(InteractionState.geometry_report, class_name="sp-note"),
            ),
            class_name="sp-grid-2",
        ),
    )


# ── One page per chart ──────────────────────────────────────────────────────────────────


def props_table(props: tuple[PropDoc, ...]) -> rx.Component:
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


def usage(info: ChartInfo) -> str:
    keys = KEY_PROPS.get(info.slug, {})
    lines = [f"from reflex_silverpoint_react import {info.factory_name}", "", f"{info.factory_name}("]
    if info.slug in ("gauge-arc", "meter-chart"):
        lines.append("    percent=State.percent,")
    else:
        lines.append("    data=State.rows,  # list of dicts; omit it to draw the demo dataset")
    lines += [f"    {key}={value!r}," for key, value in keys.items()]
    lines += [f'    title="{info.chart}",', "    on_select=State.on_select,", ")"]
    return "\n".join(lines)


def chart_page(info: ChartInfo):
    def render() -> rx.Component:
        return page(
            rx.el.p(
                *[
                    item
                    for other in CHARTS
                    for item in (
                        rx.el.a(
                            other.chart,
                            href=f"/chart/{other.slug}",
                            style={"fontWeight": "600"} if other is info else {},
                        ),
                        " · ",
                    )
                ][:-1],
                style={"fontSize": "0.9rem", "color": "var(--muted)"},
            ),
            rx.el.h1(info.chart),
            rx.el.p(info.summary, " Family: ", info.family, ".", class_name="sp-lede"),
            card(
                info.factory(
                    title=info.chart, footer_right="silverpoint", width=640, height=300, id=f"chart-{info.slug}"
                ),
                rx.el.div(
                    button("Download SVG", on_click=download_svg(f"chart-{info.slug}", f"{info.slug}.svg")),
                    style={"marginTop": "8px"},
                ),
                class_name="sp-chart-lg",
            ),
            rx.el.h2("Usage"),
            code(usage(info)),
            rx.el.h2("Its own props"),
            props_table(info.props) if info.props else rx.el.p("None besides the common ones."),
            rx.el.h2("Props every chart takes"),
            props_table(COMMON_PROPS),
            rx.el.p(
                rx.el.code("on_active_change"),
                " and ",
                rx.el.code("on_select"),
                " receive the item {seriesKey, index, datum, value, point}; ",
                rx.el.code("tooltip"),
                " takes tooltip_template(...).",
            ),
        )

    render.__name__ = f"chart_{info.factory_name}"
    return render


app = rx.App(stylesheets=["/silverpoint_demo.css"])
app.add_page(index, title="silverpoint for Reflex")
app.add_page(gallery, route="/gallery", title="Gallery · silverpoint for Reflex")
app.add_page(playground, route="/playground", title="Playground · silverpoint for Reflex")
app.add_page(interaction, route="/interaction", title="Interaction · silverpoint for Reflex")
for _info in CHARTS:
    app.add_page(chart_page(_info), route=f"/chart/{_info.slug}", title=f"{_info.chart} · silverpoint for Reflex")
