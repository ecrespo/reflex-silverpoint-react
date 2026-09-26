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
