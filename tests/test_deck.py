"""0.9: ``sp_deck``, the npm ``SpDeck`` of ``@silverpoint/react/deck`` (silverpoint 0.9.0).

A Marp/Marpit Markdown deck in the silverpoint style. These tests assert what the builder hands the
npm component: its import path, its npm dependencies (only a page with a deck installs
``@silverpoint/marp``), its stylesheets, its props and its three events.
"""

import importlib
import inspect

import pytest
import reflex as rx
import reflex_silverpoint_react as sp

deck_module = importlib.import_module("reflex_silverpoint_react.deck")

REACT = f"@silverpoint/react@{sp.SILVERPOINT_VERSION}"
MARP = "@silverpoint/marp@0.9.0"
MARKDOWN = "---\npaginate: true\n---\n\n# Title\n\n---\n\n## Two\n\n* a\n* b\n"


def _props(component: rx.Component) -> dict[str, str]:
    return dict(prop.split(":", 1) for prop in component.render()["props"])


def _imports(component: rx.Component) -> dict[str, list]:
    return component._get_all_imports()


class _DeckState(rx.State):
    markdown: str = MARKDOWN
    page: int = 1
    total: int = 0
    step: int = 0
    steps: int = 0
    notes: bool = False

    @rx.event
    def on_page(self, page: int, total: int):
        self.page, self.total = page, total

    @rx.event
    def on_fragment(self, page: int, step: int, steps: int):
        self.step, self.steps = step, steps

    @rx.event
    def on_fragment_short(self, page: int, step: int):
        self.step = step

    @rx.event
    def on_ready(self, total: int):
        self.total = total


# ── Version and import ──────────────────────────────────────────────────────────────────


def test_wraps_silverpoint_0_9_0() -> None:
    assert sp.SILVERPOINT_VERSION == "0.9.0"
    assert sp.SILVERPOINT_LIBRARY == "@silverpoint/react@0.9.0"
    assert sp.MARP_VERSION == "0.9.0"


def test_exported_from_the_root_and_the_deck_module() -> None:
    assert sp.sp_deck is deck_module.sp_deck
    assert sp.SpDeck is deck_module.SpDeck
    # The name the component was designed under; the npm tag is SpDeck.
    assert sp.SilverpointDeck is sp.SpDeck
    for name in ("sp_deck", "SpDeck", "SilverpointDeck", "MARP_VERSION", "DECK_STYLESHEETS"):
        assert name in sp.__all__


def test_imports_spdeck_from_the_deck_subpath() -> None:
    component = sp.sp_deck(MARKDOWN)
    assert component.render()["name"] == "SpDeck"
    tags = {(var.tag, var.package_path) for var in _imports(component)[REACT]}
    assert ("SpDeck", "/deck") in tags


def test_is_server_renderable_not_no_ssr() -> None:
    # SpDeck renders the current slide on the server and attaches its client half after mount,
    # so it needs no NoSSR wrapper (silverpoint's README, "Server rendering").
    assert not isinstance(sp.sp_deck(MARKDOWN), rx.NoSSRComponent)


# ── npm dependencies and stylesheets ────────────────────────────────────────────────────


def test_marp_is_a_dependency_of_the_deck_only() -> None:
    assert MARP in sp.SpDeck.lib_dependencies
    for dependency in ("@silverpoint/core@0.9.0", "@silverpoint/grounds@0.9.0", "@silverpoint/fonts@0.9.0"):
        assert dependency in sp.SpDeck.lib_dependencies
    # Marpit comes with @silverpoint/marp (its dependency); the React deck needs no polyfill.
    assert not [dep for dep in sp.SpDeck.lib_dependencies if dep.startswith("@marp-team/")]
    for component in (sp.bar_chart(), sp.sp_button("Go"), sp.silverpoint_provider()):
        assert MARP not in component._get_dependencies_imports()
        assert not any("marp" in dep for dep in type(component).lib_dependencies)


def test_deck_dependency_reaches_the_page_imports() -> None:
    # Reflex installs the lib_dependencies of the components a page renders.
    assert MARP in rx.el.div(sp.bar_chart(), sp.sp_deck(MARKDOWN))._get_all_imports()
    assert MARP not in rx.el.div(sp.bar_chart(), sp.sp_button("Go"))._get_all_imports()


def test_imports_the_four_stylesheets_in_order() -> None:
    assert sp.DECK_STYLESHEETS == (
        "@silverpoint/fonts/fonts.css",
        "@silverpoint/grounds/styles.css",
        "@silverpoint/grounds/ui.css",
        "@silverpoint/marp/deck.css",
    )
    assert sp.sp_deck(MARKDOWN).add_imports() == {"": list(sp.DECK_STYLESHEETS)}
    assert "@silverpoint/marp/deck.css" not in str(sp.bar_chart().add_imports())


# ── Props ───────────────────────────────────────────────────────────────────────────────


def test_markdown_is_required() -> None:
    markdown = inspect.signature(sp.sp_deck).parameters["markdown"]
    assert markdown.default is inspect.Parameter.empty
    assert markdown.kind is inspect.Parameter.POSITIONAL_OR_KEYWORD


def test_props_render_camel_case() -> None:
    props = _props(
        sp.sp_deck(
            MARKDOWN,
            default_page=2,
            theme="silverpoint",
            ground="cyanotype",
            substrate="prussian",
            mode="precision",
            size="4:3",
            show_notes=True,
            show_controls=False,
            keyboard=False,
            swipe=False,
            hash=True,
            interactive=False,
            label="Talk",
            id="talk",
        )
    )
    assert props["markdown"] == '"---\\npaginate: true\\n---\\n\\n# Title\\n\\n---\\n\\n## Two\\n\\n* a\\n* b\\n"'
    assert props["defaultPage"] == "2"
    assert props["theme"] == '"silverpoint"'
    assert props["ground"] == '"cyanotype"'
    assert props["substrate"] == '"prussian"'
    assert props["mode"] == '"precision"'
    assert props["size"] == '"4:3"'
    assert props["showNotes"] == "true"
    assert props["showControls"] == "false"
    assert props["keyboard"] == "false"
    assert props["swipe"] == "false"
    assert props["hash"] == "true"
    assert props["interactive"] == "false"
    assert props["label"] == '"Talk"'
    assert props["id"] == '"talk"'


def test_unset_props_are_left_to_the_npm_defaults() -> None:
    props = _props(sp.sp_deck(MARKDOWN))
    assert set(props) == {"markdown"}


def test_state_vars_bind_markdown_page_and_toggles() -> None:
    props = _props(
        sp.sp_deck(
            _DeckState.markdown, page=_DeckState.page, show_notes=_DeckState.notes, on_page_change=_DeckState.on_page
        )
    )
    assert "markdown" in props["markdown"]
    assert "page" in props["page"]
    assert "notes" in props["showNotes"]


@pytest.mark.parametrize(("given", "sent"), [("iron_gall", "ironGall"), ("ironGall", "ironGall"), ("sepia", "sepia")])
def test_palette_is_a_preset_name_in_js_spelling(given: str, sent: str) -> None:
    assert _props(sp.sp_deck(MARKDOWN, palette=given))["palette"] == f'"{sent}"'


def test_palette_object_of_a_preset_is_sent_by_name() -> None:
    assert _props(sp.sp_deck(MARKDOWN, palette=sp.PALETTES["iron_gall"]))["palette"] == '"ironGall"'


def test_palette_must_be_a_preset() -> None:
    with pytest.raises(ValueError, match="preset"):
        sp.sp_deck(MARKDOWN, palette="crimson")
    with pytest.raises(ValueError, match="preset"):
        sp.sp_deck(MARKDOWN, palette={"ink": "#000000"})


def test_mode_rejects_a_value_outside_the_literal() -> None:
    with pytest.raises(TypeError, match="mode"):
        sp.sp_deck(MARKDOWN, mode="silverpoint")  # type: ignore[arg-type]


# ── Events ──────────────────────────────────────────────────────────────────────────────


def test_events_unpack_the_payload_into_ints() -> None:
    component = sp.sp_deck(
        MARKDOWN,
        on_page_change=_DeckState.on_page,
        on_fragment_change=_DeckState.on_fragment,
        on_ready=_DeckState.on_ready,
    )
    props = _props(component)
    page_change = props["onPageChange"]
    assert '?.["page"]' in page_change or '["page"]' in page_change
    assert '["total"]' in page_change
    assert all(f'["{key}"]' in props["onFragmentChange"] for key in ("page", "step", "steps"))
    assert '["total"]' in props["onReady"]
    assert "on_page" in page_change


def test_a_handler_may_take_fewer_arguments() -> None:
    # A handler of (page, step) ignores the third value, `steps`.
    props = _props(sp.sp_deck(MARKDOWN, on_fragment_change=_DeckState.on_fragment_short))
    assert "on_fragment_short" in props["onFragmentChange"]


def test_event_specs_are_typed_ints() -> None:
    for name, arity in (("on_page_change", 2), ("on_fragment_change", 3), ("on_ready", 1)):
        spec = sp.SpDeck.get_event_triggers()[name]
        payload = rx.Var("payload").to(dict)
        values = spec(payload)
        assert len(values) == arity, name
        assert all(value._var_type is int for value in values), name
