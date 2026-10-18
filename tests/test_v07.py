"""0.7: palettes, the Reflex-composed components (levels A and B) and the Knight Lab timeline."""

import pytest
import reflex as rx
import reflex_silverpoint_react as sp
from reflex_silverpoint_react.palette import apply_palette, resolve_palette


def _props(component: rx.Component) -> dict[str, str]:
    return dict(prop.split(":", 1) for prop in component.render()["props"])


class _S(rx.State):
    palette: dict[str, str] = {"ink": "#8A3A24"}
    rows: list[dict] = [{"a": 1, "b": "x"}]
    items: list[dict] = [{"label": "Home", "href": "/"}, {"label": "Here", "href": "#"}]
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


# ── Palettes ────────────────────────────────────────────────────────────────────────────


@pytest.mark.parametrize("name", list(sp.PALETTES))
def test_every_preset_passes_the_contrast_thresholds(name: str) -> None:
    assert sp.check_palette(name) == []


def test_check_palette_reports_low_contrast() -> None:
    problems = sp.check_palette({"ink": "#cccccc"})
    assert len(problems) == 1 and problems[0].startswith("ink #cccccc")


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


def test_apply_palette_nests_under_doubled_class() -> None:
    props = apply_palette({"palette": "indigo", "style": {"width": "10px"}})
    assert "palette" not in props
    assert props["style"]["width"] == "10px"
    assert props["style"]["&&"]["--sp-ink"] == sp.PALETTES["indigo"].ink


@pytest.mark.parametrize(
    "factory",
    [sp.bar_chart, sp.line_chart, sp.sp_button, sp.sp_card, sp.dashboard, sp.sp_surface],
    ids=["chart", "chart2", "ui", "ui-card", "dashboard", "surface"],
)
def test_palette_prop_on_every_kind_of_element(factory) -> None:
    rendered = str(factory(palette="sanguine").render())
    assert '["&&"]' in rendered and sp.PALETTES["sanguine"].ink in rendered


def test_palette_from_a_state_var() -> None:
    rendered = str(sp.donut_chart(palette=_S.palette).render())
    assert '?.["ink"]' in rendered and "--sp-text-muted" in rendered


def test_section_palette_targets_the_declaring_elements() -> None:
    rendered = str(sp.silverpoint_palette(sp.bar_chart(), palette="verdigris").render())
    assert "display" in rendered and ":where(.sp-root, .sp-ui, .sp-dashboard, .sp-surface)" in rendered


def test_provider_has_no_palette() -> None:
    with pytest.raises(TypeError, match="silverpoint_palette"):
        sp.silverpoint_provider(palette="sepia")


# ── Surfaces and level A ────────────────────────────────────────────────────────────────


def test_surface_imports_core_ui_helpers_and_stylesheets() -> None:
    imports = sp.sp_surface(frame="card")._get_all_imports()
    core = imports[f"@silverpoint/core@{sp.SILVERPOINT_VERSION}"]
    tags = {(var.tag, var.package_path) for var in core}
    assert ("resolveUi", "/ui") in tags and ("FORCED_PRECISION_QUERY", "/") in tags
    side_effects = {var.tag for var in imports[""]}
    assert {"@silverpoint/grounds/styles.css", "@silverpoint/grounds/ui.css"} <= side_effects


def test_surface_code_is_emitted_once() -> None:
    tree = rx.el.div(sp.sp_surface(), sp.sp_glyph(glyph="tick"), sp.sp_pagination(total=10))
    assert len(tree._get_all_custom_code()) == 1


def test_sort_rows() -> None:
    rows = [{"n": 2}, {"n": None}, {"n": 1}, {"n": 3}]
    assert [r["n"] for r in sp.sort_rows(rows, "n")] == [1, 2, 3, None]
    assert [r["n"] for r in sp.sort_rows(rows, "n", "desc")] == [3, 2, 1, None]
    assert sp.sort_rows(rows, None) == rows


@pytest.mark.parametrize(
    "build",
    [
        lambda: sp.sp_table(["a", "b"], [{"a": 1, "b": 2}], caption="T"),
        lambda: sp.sp_table(
            [{"key": "a", "sortable": True}], _S.rows, sort_key="a", sort_order="desc", on_sort=_S.pick
        ),
        lambda: sp.sp_pagination(total=95, current=3),
        lambda: sp.sp_breadcrumb([{"label": "Home", "href": "/"}, {"label": "Here"}]),
        lambda: sp.sp_breadcrumb(_S.items),
        lambda: sp.sp_avatar(name="Ada Lovelace"),
        lambda: sp.sp_avatar(src="a.png", name="Ada", pixel_size=64, shape="square"),
        lambda: sp.sp_statistic("Revenue", "1,204", prefix="$", trend="up", delta="+8 %"),
        lambda: sp.sp_descriptions([{"label": "a", "value": "b"}], title="T", columns=2),
        lambda: sp.sp_timeline_list([{"title": "x", "status": "current"}, {"title": "y", "status": "pending"}]),
        lambda: sp.sp_collapse(sp.sp_collapse_item("One", "body", open=True), accordion=True),
        lambda: sp.sp_empty(description="Nothing"),
        lambda: sp.sp_result(status="error", title="Failed"),
        lambda: sp.sp_textarea(value=_S.value, on_change=_S.set_value, max_length=10, show_count=True),
        lambda: sp.sp_input_number(value=3, min=0, max=10, step=0.5),
    ],
)
def test_level_a_builders_render(build) -> None:
    rendered = build().render()
    assert rendered["name"] in ("SilverpointSurface", "SilverpointPagination", "SilverpointInputNumber")


def test_initials_and_frames() -> None:
    avatar = str(sp.sp_avatar(name="Cennino Cennini").render())
    assert '"CC"' in avatar and 'frame:"round"' in avatar
    assert 'frame:"box"' in str(sp.sp_avatar(name="x", shape="square").render())


def test_table_sort_header_has_aria_sort_and_handler() -> None:
    rendered = str(sp.sp_table([{"key": "a", "sortable": True}], _S.rows, sort_key="a", on_sort=_S.pick).render())
    assert "aria-sort" in rendered and "pick" in rendered


def test_frame_markup_uses_the_part_attribute() -> None:
    rendered = str(sp.sp_result(status="success", title="ok").render())
    assert 'part:"sp-frame"' in rendered and 'role:"status"' in rendered


def test_unknown_surface_props_become_dom_attributes() -> None:
    props = _props(sp.sp_trigger("Go", aria_label="Go now", disabled=True, tab_index=-1))
    assert props['"aria-label"'] == '"Go now"' and props["disabled"] == "true" and props["tabIndex"] == "-1"
    assert "css" not in props


# ── Level B ─────────────────────────────────────────────────────────────────────────────


def test_overlays_render_on_radix_primitives() -> None:
    cases = {
        "SpRadixDialogRoot": sp.sp_modal("b", trigger="Open", title="T", open=_S.flag, on_open_change=_S.set_flag),
        "SpRadixPopoverRoot": sp.sp_popover("c", trigger="P"),
        "SpRadixTooltipProvider": sp.sp_tooltip("Hover", "tip"),
        "SpRadixDropdownMenuRoot": sp.sp_dropdown_menu("M", [{"key": "a", "label": "A"}], on_select=_S.pick),
        "SpRadixToastProvider": sp.sp_toaster(sp.sp_toast("Saved", open=_S.flag, on_open_change=_S.set_flag)),
    }
    for name, component in cases.items():
        assert component.render()["name"] == name
    drawer = str(sp.sp_drawer("b", trigger="D", side="left", size=420).render())
    assert '"data-side"' in drawer or "data-side" in drawer


def test_radix_versions_match_the_ones_reflex_installs() -> None:
    imports = sp.sp_modal("b", trigger="x")._get_all_imports()
    assert "@radix-ui/react-dialog@1.1.23" in imports


def test_select_static_and_var_items() -> None:
    assert sp.sp_select(["a", {"value": "b", "label": "B", "disabled": True}], value=_S.value, on_change=_S.set_value)
    assert sp.sp_select(_S.rows, default_value="a")


def test_trigger_is_a_drawn_button() -> None:
    rendered = str(sp.sp_trigger("Go", variant="primary").render())
    assert 'element:"button"' in rendered and 'frame:"control"' in rendered and 'tone:"primary"' in rendered


# ── Timeline ────────────────────────────────────────────────────────────────────────────


def test_timeline_available_in_dev() -> None:
    assert sp.timeline_available()


def test_timeline_wraps_knightlab_in_a_surface() -> None:
    data = {"events": [{"start_date": {"year": 1500}, "text": {"headline": "x"}}]}
    component = sp.sp_timeline(
        data, {"font": "x", "start_at_end": True}, height=500, palette="sepia", ground="cyanotype"
    )
    rendered = str(component.render())
    assert component.render()["name"] == "SilverpointSurface"
    assert "SilverpointTimelineInk" in rendered and "KnightLabTimeline" in rendered
    assert '"font"' not in rendered and "start_at_end" in rendered
    assert 'name:"kl-timeline"' in rendered and "500px" in rendered


def test_timeline_code_carries_the_skin() -> None:
    from reflex_silverpoint_react.timeline import TIMELINE_CODE

    assert "SP_TIMELINE_CSS" in TIMELINE_CODE and ".tl-timemarker" in TIMELINE_CODE


def test_assets_ship_in_the_package() -> None:
    from importlib.resources import files

    assets = files("reflex_silverpoint_react") / "assets"
    for name in ("surface.jsx", "surfaces.css", "timeline.jsx", "timeline.css"):
        assert (assets / name).is_file()
