"""Compile-level tests: every chart renders to the right tag with camelCase props."""

import pytest
import reflex as rx
import reflex_silverpoint_react as sp


def _props(component: rx.Component) -> dict[str, str]:
    rendered = component.render()
    return dict(prop.split(":", 1) for prop in rendered["props"])


def test_catalog_has_33_charts() -> None:
    assert len(sp.CHARTS) == 33
    assert len({info.slug for info in sp.CHARTS}) == 33
    assert sp.chart_by_slug("wind-rose").chart == "WindRose"
    assert sp.chart_by_name("OrbitChart").factory is sp.orbit_chart


@pytest.mark.parametrize("info", sp.CHARTS, ids=lambda info: info.slug)
def test_every_chart_renders_its_tag(info: sp.ChartInfo) -> None:
    component = info.factory(title=info.chart, substrate="green", mode="precision", hatch_fill="per-shape")
    assert component.render()["name"] == info.chart
    props = _props(component)
    assert props["hatchFill"] == '"per-shape"'
    assert props["substrate"] == '"green"'
    assert info.component.library == sp.SILVERPOINT_LIBRARY


@pytest.mark.parametrize("info", sp.CHARTS, ids=lambda info: info.slug)
def test_own_props_are_declared(info: sp.ChartInfo) -> None:
    fields = info.component.get_props()
    for prop in info.props:
        assert prop.name in fields, f"{info.chart}.{prop.name} missing"


def test_snake_case_maps_to_camel_case() -> None:
    props = _props(
        sp.line_chart(x_key="hour", value_key="hits", secondary_key="base", connect_nulls=True, footer_left="a")
    )
    assert props["xKey"] == '"hour"'
    assert props["valueKey"] == '"hits"'
    assert props["secondaryKey"] == '"base"'
    assert props["connectNulls"] == "true"
    assert props["footerLeft"] == '"a"'


def test_stylesheets_are_imported() -> None:
    side_effects = {var.tag for var in sp.bar_chart()._get_all_imports()[""]}
    assert {"@silverpoint/grounds/styles.css", "@silverpoint/fonts/fonts.css"} <= side_effects


def test_id_gives_a_ref_for_the_handle() -> None:
    props = _props(sp.donut_chart(id="sales-by-channel"))
    assert props["ref"] == sp.chart_ref("sales-by-channel") == "ref_sales_by_channel"


def test_events_are_wired() -> None:
    class S(rx.State):
        @rx.event
        def pick(self, item: dict):
            pass

        @rx.event
        def hover(self, item: dict | None):
            pass

    rendered = str(sp.bar_chart(on_select=S.pick, on_active_change=S.hover).render())
    assert "onSelect" in rendered and "onActiveChange" in rendered


def test_tooltip_template() -> None:
    js = str(sp.tooltip_template("{datum.hour} h · {value} `x` {{literal}}"))
    assert js.startswith("((item, r) => `")
    assert 'item.datum?.["hour"]' in js and "item.value" in js
    assert "\\`x\\`" in js and "{literal}" in js
    with pytest.raises(ValueError):
        sp.tooltip_template("{nope}")


def test_provider() -> None:
    component = sp.silverpoint_provider(sp.line_chart(), substrate="ochre", locale="es-VE")
    assert component.render()["name"] == "SilverpointProvider"
    assert _props(component)["locale"] == '"es-VE"'


def test_version_pins_silverpoint_0_3() -> None:
    assert sp.SILVERPOINT_VERSION == "0.3.0"
    assert sp.SILVERPOINT_LIBRARY == "@silverpoint/react@0.3.0"


def test_cyanotype_ground() -> None:
    assert _props(sp.bar_chart(ground="cyanotype"))["ground"] == '"cyanotype"'
    assert _props(sp.silverpoint_provider(sp.line_chart(), ground="cyanotype"))["ground"] == '"cyanotype"'


def _silverpoint_imports(component: rx.Component) -> dict[str, list[str]]:
    from reflex.compiler.utils import compile_imports

    return {i["lib"]: i["rest"] for i in compile_imports(component._get_all_imports()) if "silverpoint" in i["lib"]}


def test_dashboard_imports_from_its_subpath() -> None:
    component = sp.dashboard(sp.dashboard_cell(sp.line_chart(), cell="trend"), sp.bar_chart(), id="ops", title="Ops")
    imports = _silverpoint_imports(component)
    assert imports["@silverpoint/react/dashboard"] == ["Dashboard", "DashboardCell"]
    assert imports["@silverpoint/react"] == ["BarChart", "LineChart"]
    assert component.render()["name"] == "Dashboard"
    assert "@silverpoint/react/dashboard-link" in _silverpoint_imports(sp.dashboard_link(sp.line_chart(), link="x"))


def test_dashboard_props() -> None:
    layout = sp.dashboard_layout(
        ["kpi", sp.dashboard_cell_layout("trend", col_span={"md": 2, "lg": 4}, row_span=2)],
        columns={"lg": 3},
        row_height=200,
        gap=12,
    )
    assert layout == {
        "columns": {"lg": 3},
        "rowHeight": 200,
        "gap": 12,
        "cells": [{"id": "kpi"}, {"id": "trend", "colSpan": {"md": 2, "lg": 4}, "rowSpan": 2}],
    }
    props = _props(sp.dashboard(id="ops", title="Ops", layout=layout, link="hour", heading_level=3, ssr_width=900))
    assert props["id"] == '"ops"'
    assert props["headingLevel"] == "3"
    assert props["ssrWidth"] == "900"
    assert '["key"] : "hour"' in props["link"]
    assert '["rowHeight"] : 200' in props["layout"]
    assert _props(sp.dashboard_cell(sp.kpi_card(), cell="kpi"))["cell"] == '"kpi"'


def test_link_change_is_wired() -> None:
    class L(rx.State):
        @rx.event
        def linked(self, link: dict | None):
            pass

    assert "onLinkChange" in str(sp.dashboard(id="d", title="D", link="hour", on_link_change=L.linked).render())
    assert "onLinkChange" in str(sp.dashboard_link(link={"key": "hour"}, on_link_change=L.linked).render())


# ── UI components (silverpoint 0.3) ──────────────────────────────────────────────────────


def test_ui_catalog_has_17_components_and_45_states() -> None:
    assert len(sp.UI_COMPONENTS) == 17
    assert sum(len(info.states) for info in sp.UI_COMPONENTS) == 45
    assert {info.slug for info in sp.UI_COMPONENTS} == set(sp.UI_DEMOS)
    for info in sp.UI_COMPONENTS:
        assert tuple(sp.UI_DEMOS[info.slug]) == info.states
    assert sp.ui_component_by_slug("radio-group").component == "SpRadioGroup"
    assert sp.ui_component_by_slug("radio-group").factory is sp.sp_radio_group


@pytest.mark.parametrize(
    ("slug", "state"),
    [(info.slug, state) for info in sp.UI_COMPONENTS for state in info.states],
    ids=lambda value: value,
)
def test_every_ui_state_renders(slug: str, state: str) -> None:
    info = sp.ui_component_by_slug(slug)
    component = sp.ui_demo(slug, state, ground="cyanotype", substrate="prussian", mode="precision")
    assert component.render()["name"] == info.component
    props = _props(component)
    assert props["ground"] == '"cyanotype"'
    assert props["mode"] == '"precision"'
    assert props["id"] == f'"{slug}--{state}"'


@pytest.mark.parametrize("info", sp.UI_COMPONENTS, ids=lambda info: info.slug)
def test_ui_props_are_documented(info: sp.UiComponentInfo) -> None:
    fields = info.component_class.get_props()
    assert info.props
    for prop in info.props:
        assert prop.name in fields, f"{info.component}.{prop.name} missing"
        assert prop.doc, f"{info.component}.{prop.name} undocumented"


def test_ui_imports_from_its_subpath_with_ui_css() -> None:
    component = sp.sp_tabs(sp.sp_tab_panel("a", value="a"), items=[sp.ui_item("a", "A")])
    imports = _silverpoint_imports(component)
    assert imports["@silverpoint/react/ui"] == ["SpTabPanel", "SpTabs"]
    side_effects = {var.tag for var in sp.sp_button("x")._get_all_imports()[""]}
    assert {
        sp.SILVERPOINT_UI_STYLESHEET,
        "@silverpoint/grounds/styles.css",
        "@silverpoint/fonts/fonts.css",
    } <= side_effects


def test_ui_demo_binds_value_as_default_or_controlled() -> None:
    assert _props(sp.ui_demo("input", "filled"))["defaultValue"] == '"Caracas"'
    assert _props(sp.ui_demo("checkbox", "checked"))["defaultChecked"] == "true"
    assert _props(sp.ui_demo("switch", "on", controlled=True))["checked"] == "true"
    assert _props(sp.ui_demo("progress", "line"))["value"] == "40"
    assert _props(sp.ui_demo("rate", "read-only"))["readOnly"] == "true"


def test_ui_snake_case_maps_to_camel_case() -> None:
    assert _props(sp.sp_progress(label="x", show_value=False))["showValue"] == "false"
    assert _props(sp.sp_alert("x", close_label="Dismiss"))["closeLabel"] == '"Dismiss"'
    assert _props(sp.sp_card("x", heading_level=4))["headingLevel"] == "4"
    assert "jsx" in _props(sp.sp_input(prefix=rx.el.span("€")))["prefix"]


def test_ui_items() -> None:
    assert sp.ui_item("a", "A") == {"key": "a", "label": "A"}
    assert sp.ui_item("a", "A", disabled=True)["disabled"] is True
    assert sp.step_item("s", "S", status="error") == {"key": "s", "title": "S", "status": "error"}


def test_ui_events_are_wired() -> None:
    class U(rx.State):
        text: str = ""

        @rx.event
        def changed(self, value: str):
            self.text = value

        @rx.event
        def closed(self):
            pass

    assert "onChange" in str(sp.sp_input(value=U.text, on_change=U.changed).render())
    assert "onChange" in str(sp.sp_segmented(label="P", items=[], on_change=U.changed).render())
    assert "onClose" in str(sp.sp_tag("t", closable=True, on_close=U.closed).render())
    assert "onClose" in str(sp.sp_alert("t", closable=True, on_close=U.closed).render())
