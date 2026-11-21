"""0.11: wraps silverpoint 0.11.0 — no builder or prop change, the release line follows the library.

The pyproject and ``.claude-plugin/*.json`` versions are tied to each other by ``test_plugin.py``;
this file pins pyproject itself on the line.
"""

import json
import re
import tomllib
from pathlib import Path

import reflex_silverpoint_react as sp

ROOT = Path(__file__).resolve().parent.parent
LINE = "0.11.0"
NPM_PIN = re.compile(r"^(@silverpoint/[a-z-]+)@(.+)$")


def _silverpoint_pins(dependencies: list[str]) -> dict[str, str]:
    """Every ``@silverpoint/*`` npm pin of a list, as ``{package: version}``."""
    return {m[1]: m[2] for m in map(NPM_PIN.match, dependencies) if m}


def test_wraps_silverpoint_0_11_0() -> None:
    assert sp.SILVERPOINT_VERSION == LINE
    assert sp.MARP_VERSION == LINE
    assert sp.SILVERPOINT_LIBRARY == f"@silverpoint/react@{LINE}"


def test_every_provider_npm_pin_is_on_0_11_0() -> None:
    pins = _silverpoint_pins(sp.SilverpointProvider.lib_dependencies)
    assert set(pins) == {"@silverpoint/core", "@silverpoint/grounds", "@silverpoint/fonts"}
    assert set(pins.values()) == {LINE}


def test_the_deck_pins_marp_on_0_11_0() -> None:
    pins = _silverpoint_pins(sp.SpDeck.lib_dependencies)
    assert pins["@silverpoint/marp"] == LINE
    assert set(pins.values()) == {LINE}


def test_reflex_catalog_is_on_0_11_0() -> None:
    catalog = json.loads((ROOT / "reflex-catalog.json").read_text())
    assert (catalog["version"], catalog["wraps"]) == (LINE, LINE)


def test_package_version_is_0_11_0() -> None:
    """``test_plugin.py`` ties both ``.claude-plugin/*.json`` versions to this one."""
    assert tomllib.loads((ROOT / "pyproject.toml").read_text())["project"]["version"] == LINE


def test_readme_tells_this_package_from_the_silverpoint_python_package() -> None:
    readme = (ROOT / "README.md").read_text()
    [paragraph] = [p for p in readme.split("\n\n") if "https://github.com/ecrespo/silverpoint-python" in p]
    paragraph = " ".join(paragraph.split())
    assert "[`silverpoint`](https://github.com/ecrespo/silverpoint-python) is a different Python package" in paragraph
