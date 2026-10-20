"""0.7: palettes, the composed components, the overlays and the timeline, on @silverpoint/react 0.7.0.

Since 0.7.1 every one of them is the npm component itself (silverpoint's parity contract), not a
Reflex-composed copy: these tests assert what each builder hands the npm component.
"""

import warnings

import pytest
import reflex as rx
import reflex_silverpoint_react as sp
from reflex_silverpoint_react.palette import apply_palette, palette_prop, resolve_palette

REACT = f"@silverpoint/react@{sp.SILVERPOINT_VERSION}"


def _props(component: rx.Component) -> dict[str, str]:
    return dict(prop.split(":", 1) for prop in component.render()["props"])


def _paths(component: rx.Component) -> set[tuple[str, str]]:
    return {(var.tag, var.package_path) for var in component._get_all_imports().get(REACT, [])}


class _S(rx.State):
    palette: dict[str, str] = {"ink": "#8A3A24", "ink_secondary": "#6A4A3A"}
    rows: list[dict] = [{"a": 1, "b": "x"}]
    items: list[dict] = [{"label": "Home", "href": "/"}, {"label": "Here", "href": "#"}]
    options: list[dict] = [{"value": "a", "label": "A"}, {"value": "b", "label": "B"}]
    flag: bool = False
    value: str = "a"

    @rx.event
    def pick(self, key: str):
        pass

    @rx.event
    def set_flag(self, value: bool):
        self.flag = value

    @rx.event
    def set_value(self, value: str):
        self.value = value


# ── Version ─────────────────────────────────────────────────────────────────────────────


def test_wraps_silverpoint_0_7_0() -> None:
    assert sp.SILVERPOINT_VERSION == "0.7.0"
    assert sp.SILVERPOINT_LIBRARY == "@silverpoint/react@0.7.0"


# ── Palettes ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("name", list(sp.PALETTES))
def test_every_preset_passes_the_contrast_pairs(name: str) -> None:
    assert sp.check_palette(name) == []


def test_presets_match_the_core_presets() -> None:
    # @silverpoint/core/palettes 0.7.0, field for field.
    assert sp.PALETTES["sanguine"].to_js() == {
        "substrate": "#F2E8DC",
        "ink": "#8A3A24",
        "inkSecondary": "#6A4A3A",
        "heighten": "#FFFFFF",
        "rule": "#9A6450",
        "grid": "#9A6450",
        "text": "#4A2216",
        "textMuted": "#7A3E2C",
    }
    assert resolve_palette("ironGall") is sp.PALETTES["iron_gall"]


def test_check_palette_measures_the_core_pairs() -> None:
    problems = sp.check_palette({"ink": "#cccccc"})
    # ``focus`` defaults to ``ink`` (PALETTE_PAIRS of @silverpoint/core/palettes).
    assert [p.split(" ", 1)[0] for p in problems] == ["ink", "focus"]
    assert problems[0].startswith("ink #cccccc on #EDE7DA")
    outline = sp.check_palette({"ink": "#5A5E65", "heighten": "#6A6E75"})
    assert any(p.startswith("heighten-outline") for p in outline)


def test_contrast_ratio_extremes() -> None:
    assert sp.contrast_ratio("#000", "#fff") == pytest.approx(21)
    assert sp.contrast_ratio("#777777", "#777777") == pytest.approx(1)


def test_resolve_palette_forms() -> None:
    assert resolve_palette("sepia") is sp.PALETTES["sepia"]
    assert resolve_palette({"ink": "#111111"}) == sp.Palette(ink="#111111")
    with pytest.raises(ValueError, match="preset"):
        resolve_palette("nope")
    with pytest.raises(ValueError, match="fields"):
        resolve_palette({"colour": "#111"})
    with pytest.raises(TypeError):
        resolve_palette(42)


def test_palette_css_maps_fields_to_custom_properties() -> None:
    css = sp.palette_css(sp.Palette(ink="#111111", focus="#222222"))
    assert css == {"--sp-ink": "#111111", "--sp-ui-focus-color": "#222222"}


def test_apply_palette_hands_the_native_prop() -> None:
    props = apply_palette({"palette": "indigo", "style": {"width": "10px"}})
    assert props["style"] == {"width": "10px"}
    assert props["palette"]["inkSecondary"] == sp.PALETTES["indigo"].ink_secondary
    assert apply_palette({"palette": None}) == {}


@pytest.mark.parametrize(
    "factory",
    [sp.bar_chart, sp.line_chart, sp.sp_button, sp.sp_card, sp.dashboard, sp.sp_surface, sp.silverpoint_provider],
    ids=["chart", "chart2", "ui", "ui-card", "dashboard", "surface", "provider"],
)
def test_palette_prop_on_every_kind_of_element(factory) -> None:
    props = _props(factory(palette="sanguine"))
    assert "palette" in props and '"textMuted"' in props["palette"]
    assert sp.PALETTES["sanguine"].ink in props["palette"]


def test_palette_from_a_state_var_maps_snake_case_fields() -> None:
    rendered = _props(sp.donut_chart(palette=_S.palette))["palette"]
    assert '["inkSecondary"]' in rendered and '?.["ink_secondary"]' in rendered


def test_section_palette_is_a_provider() -> None:
    section = sp.silverpoint_palette(sp.bar_chart(), palette="verdigris")
    assert section.render()["name"] == "SilverpointProvider"
    assert sp.PALETTES["verdigris"].ink in _props(section)["palette"]
    wrapped = sp.silverpoint_palette(sp.bar_chart(), palette="sepia", id="section")
    assert wrapped.render()["name"] == '"div"'


def test_palette_prop_helper() -> None:
    assert palette_prop(None) is None
    assert palette_prop(sp.Palette(text_muted="#111111")) == {"textMuted": "#111111"}


# ── Surfaces and composed components ────────────────────────────────────────────────────


def test_surface_and_glyph_are_the_npm_components() -> None:
    surface = sp.sp_surface(sp.sp_glyph(glyph="tick"), element="section", name="panel", frame="card", tone=2)
    assert surface.render()["name"] == "SpSurface"
    assert _props(surface)["as"] == '"section"'
    assert {("SpSurface", "/ui"), ("SpGlyph", "/ui")} <= _paths(surface)
    side_effects = {var.tag for var in surface._get_all_imports()[""]}
    assert {"@silverpoint/grounds/styles.css", "@silverpoint/grounds/ui.css"} <= side_effects


def test_sort_rows_follows_ui_sort_rows() -> None:
    rows = [{"n": 2}, {"n": None}, {"n": 1}, {"n": "b"}, {"n": 3}, {"n": "A"}, {}]
    assert [r.get("n") for r in sp.sort_rows(rows, "n")] == [1, 2, 3, "A", "b", None, None]
    assert [r.get("n") for r in sp.sort_rows(rows, "n", "desc")] == ["b", "A", 3, 2, 1, None, None]
    assert sp.sort_rows(rows, None) == rows


@pytest.mark.parametrize(
    ("build", "tag"),
    [
        (lambda: sp.sp_table(["a", "b"], [{"a": 1, "b": 2}], caption="T"), "SpTable"),
        (
            lambda: sp.sp_table(
                [{"key": "a", "sortable": True}], _S.rows, sort_key="a", sort_order="desc", on_sort=_S.pick
            ),
            "SpTable",
        ),
        (lambda: sp.sp_pagination(total=95, current=3), "SpPagination"),
        (lambda: sp.sp_breadcrumb([{"label": "Home", "href": "/"}, {"label": "Here"}]), "SpBreadcrumb"),
        (lambda: sp.sp_breadcrumb(_S.items), "SpBreadcrumb"),
        (lambda: sp.sp_avatar(name="Ada Lovelace"), "SpAvatar"),
        (lambda: sp.sp_avatar(src="a.png", name="Ada", pixel_size=64, shape="square"), "SpAvatar"),
        (lambda: sp.sp_avatar_group(sp.sp_avatar(name="A"), label="Team"), "SpAvatarGroup"),
        (lambda: sp.sp_statistic("Revenue", "1,204", prefix="$", trend="up", delta="+8 %"), "SpStatistic"),
        (lambda: sp.sp_descriptions([{"label": "a", "value": "b"}], title="T", columns=2), "SpDescriptions"),
        (
            lambda: sp.sp_timeline_list([{"title": "x", "status": "current"}, {"title": "y", "status": "pending"}]),
            "SpTimelineList",
        ),
        (lambda: sp.sp_collapse(sp.sp_collapse_item("One", "body", open=True), accordion=True), "SpCollapse"),
        (lambda: sp.sp_empty(description="Nothing"), "SpEmpty"),
        (lambda: sp.sp_result(status="error", title="Failed"), "SpResult"),
        (lambda: sp.sp_textarea(value=_S.value, on_change=_S.set_value, max_length=10, show_count=True), "SpTextarea"),
        (lambda: sp.sp_input_number(value=3, min=0, max=10, step=0.5), "SpInputNumber"),
    ],
)
def test_composed_builders_render_the_npm_component(build, tag: str) -> None:
    component = build()
    assert component.render()["name"] == tag
    assert (tag, "/ui") in _paths(component)


def test_table_columns_and_sort_event() -> None:
    props = _props(sp.sp_table(["a", {"key": "b", "sortable": True, "width": 120}], _S.rows, on_sort=_S.pick))
    assert '"key"' in props["columns"] and '"120px"' in props["columns"]
    assert "pick" in props["onSort"]


def test_collapse_item_open_is_uncontrolled_unless_a_var() -> None:
    assert "defaultOpen" in _props(sp.sp_collapse_item("One", "body", open=True))
    controlled = _props(sp.sp_collapse_item("One", "body", open=_S.flag, on_toggle=_S.set_flag))
    assert "open" in controlled and "onToggle" in controlled


def test_empty_and_result_take_their_actions_as_extra() -> None:
    props = _props(sp.sp_result(sp.sp_button("Retry"), status="error", title="Failed", heading_level=2))
    assert "extra" in props and "SpButton" in props["extra"] and props["headingLevel"] == "2"
    assert "extra" in _props(sp.sp_empty(sp.sp_button("New"), sp.sp_button("Import")))


def test_field_ids_are_the_component_id() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        props = _props(sp.sp_textarea(textarea_id="notes"))
    assert props["id"] == '"notes"' and caught and issubclass(caught[0].category, DeprecationWarning)


def test_textarea_rejects_on_blur() -> None:
    with pytest.raises(TypeError, match="on_blur"):
        sp.sp_textarea(on_blur=_S.set_flag)


# ── Overlays ────────────────────────────────────────────────────────────────────────────


def test_overlays_render_the_npm_components() -> None:
    cases = {
        "SpModal": sp.sp_modal("b", trigger="Open", title="T", open=_S.flag, on_open_change=_S.set_flag),
        "SpDrawer": sp.sp_drawer("b", trigger="D", side="start", size=420),
        "SpPopover": sp.sp_popover("c", trigger="P"),
        "SpTooltip": sp.sp_tooltip("Hover", "tip"),
        "SpSelect": sp.sp_select(["a", "b"], label="Letter"),
        "SpDropdownMenu": sp.sp_dropdown_menu("M", [{"key": "a", "label": "A"}], on_select=_S.pick),
        "SpToaster": sp.sp_toaster(sp.sp_toast("Saved", open=_S.flag, on_open_change=_S.set_flag)),
    }
    for name, component in cases.items():
        assert component.render()["name"] == name
        assert (name, "/ui") in _paths(component)
        assert not any(lib.startswith("@radix-ui/react-") for lib in component._get_all_imports())


def test_overlay_props_follow_the_api_spec() -> None:
    modal = _props(sp.sp_modal("b", trigger="Open", width=600, dismissible=False))
    assert modal["width"] == '"600px"' and modal["dismissible"] == "false"
    assert "SilverpointTrigger" in modal["trigger"]
    drawer = _props(sp.sp_drawer("b", side="start", size=420))
    assert drawer["side"] == '"start"' and drawer["extent"] == '"420px"'
    popover = _props(sp.sp_popover("c", trigger="P", side_offset=10, width=280))
    assert popover["offset"] == "10" and popover["width"] == '"280px"'
    assert _props(sp.sp_tooltip("Hover", "tip"))["text"] == '"tip"'


def test_physical_sides_map_to_logical_ones() -> None:
    with warnings.catch_warnings(record=True) as caught:
        warnings.simplefilter("always")
        drawer = _props(sp.sp_drawer("b", side="left"))
        toaster = _props(sp.sp_toaster(position="top-right"))
    assert drawer["side"] == '"start"' and toaster["position"] == '"top-end"'
    assert all(issubclass(w.category, DeprecationWarning) for w in caught) and len(caught) == 2


def test_select_items_take_value_as_key() -> None:
    items = ["a", {"value": "b", "label": "B", "disabled": True}]
    props = _props(sp.sp_select(items, value=_S.value, on_change=_S.set_value))
    # Without a label, the placeholder names the combobox (JSON-escaped in the render).
    assert '["key"] : "b"' in props["items"] and props["label"] == '"Select\\u2026"'
    var_items = _props(sp.sp_select(_S.options, default_value="a", label="Letter"))["items"]
    assert "key" in var_items and "value" in var_items


def test_menu_with_a_text_trigger_draws_its_own_button() -> None:
    props = _props(sp.sp_dropdown_menu("Actions", [{"key": "a", "label": "A"}]))
    assert props["label"] == '"Actions"' and "trigger" not in props


def test_menu_separators_and_labels_get_keys() -> None:
    items = [{"key": "a", "label": "A"}, {"type": "separator"}, {"type": "label", "label": "Zone"}]
    rendered = _props(sp.sp_dropdown_menu("M", items))["items"]
    assert '"separator-1"' in rendered and '"label-2"' in rendered


def test_trigger_forwards_what_an_overlay_clones_onto_it() -> None:
    trigger = sp.sp_trigger("Go", variant="primary", chevron=True, aria_label="Go now", tab_index=-1)
    props = _props(trigger)
    assert trigger.render()["name"] == "SilverpointTrigger"
    assert props['"aria-label"'] == '"Go now"' and props["tabIndex"] == "-1" and props["variant"] == '"primary"'
    assert len(rx.el.div(trigger, sp.sp_trigger("x"))._get_all_custom_code()) == 1


# ── Timeline ────────────────────────────────────────────────────────────────────────────


def test_timeline_is_the_npm_sp_timeline() -> None:
    data = {"events": [{"start_date": {"year": 1500}, "text": {"headline": "x"}}]}
    component = sp.sp_timeline(data, {"font": "x", "start_at_end": True}, height=500, palette="sepia", label="Years")
    props = _props(component)
    assert component.render()["name"] == "SpTimeline"
    assert ("SpTimeline", "/timeline") in _paths(component)
    assert '"font"' not in props["options"] and "start_at_end" in props["options"]
    assert props["height"] == '"500px"' and props["label"] == '"Years"'
    imports = component._get_all_imports()
    assert "@knight-lab/timelinejs@3.9.13" in imports
    css = [var.tag for var in imports[""]]
    assert css.index("@knight-lab/timelinejs/dist/css/timeline.css") < css.index("@silverpoint/grounds/timeline.css")


def test_timeline_needs_no_python_extra() -> None:
    assert sp.timeline_available()
