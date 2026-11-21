"""0.10: the provider on its own subpath, the dashboard under a provider (the version lives in test_v011)."""

import reflex as rx
import reflex_silverpoint_react as sp
from reflex.compiler.utils import compile_imports

RED = sp.Palette(ink="#8a3324")


def _modules(component: rx.Component) -> dict[str, list[str]]:
    """The silverpoint modules a component imports, each with its named imports."""
    return {
        entry["lib"]: sorted(entry["rest"])
        for entry in compile_imports(component._get_all_imports())
        if entry["lib"].startswith("@silverpoint/react")
    }


def test_provider_is_imported_from_its_own_subpath() -> None:
    """silverpoint#21: ``@silverpoint/react/provider`` keeps the root barrel out of a page with no chart."""
    assert _modules(sp.silverpoint_provider(sp.sp_button("Go"))) == {
        "@silverpoint/react/provider": ["SilverpointProvider"],
        "@silverpoint/react/ui": ["SpButton"],
    }


def test_a_palette_section_is_imported_from_the_provider_subpath() -> None:
    section = sp.silverpoint_palette(sp.sp_button("Go"), palette=RED)
    assert _modules(section)["@silverpoint/react/provider"] == ["SilverpointProvider"]
    assert "@silverpoint/react" not in _modules(section)


def test_provider_keeps_the_version_pin_and_the_stylesheets() -> None:
    provider = sp.silverpoint_provider()
    assert provider.library == sp.SILVERPOINT_LIBRARY
    imports = provider._get_all_imports()
    assert [(var.tag, var.package_path) for var in imports[sp.SILVERPOINT_LIBRARY]] == [
        ("SilverpointProvider", "/provider")
    ]
    assert {var.tag for var in imports[""]} >= set(sp.SILVERPOINT_STYLESHEETS)


def test_a_chart_still_comes_from_the_root_entry() -> None:
    modules = _modules(sp.silverpoint_provider(sp.bar_chart()))
    assert modules["@silverpoint/react"] == ["BarChart"]
    assert modules["@silverpoint/react/provider"] == ["SilverpointProvider"]
