"""Feature-005 (silverpoint): the Reflex catalog export, ``reflex-catalog.json`` (Data Model §2.30).

``scripts/export_catalog.py`` builds it from the package itself; silverpoint's agent catalog joins
it by slug and JS prop name, and marks every Reflex entry stale when ``wraps`` is not its version.
"""

import importlib.metadata
import importlib.util
import json
import warnings
from pathlib import Path

import pytest
import reflex_silverpoint_react as sp

ROOT = Path(__file__).resolve().parent.parent
FIXTURES = Path(__file__).parent / "fixtures"


def _load(name: str):
    spec = importlib.util.spec_from_file_location(name, ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


export_catalog = _load("export_catalog")


@pytest.fixture(scope="module")
def catalog() -> dict:
    return export_catalog.build()


def _builders(catalog: dict) -> set[str]:
    return {c["builder"] for c in catalog["charts"]} | {c["builder"] for c in catalog["components"]}


def test_req553_catalog_header(catalog):
    assert catalog["schema"] == 1
    assert catalog["package"] == "reflex-silverpoint-react"
    assert catalog["version"] == importlib.metadata.version("reflex-silverpoint-react")
    assert list(catalog) == ["schema", "package", "version", "wraps", "common", "charts", "components", "helpers"]


def test_req556_wraps_is_silverpoint_version(catalog):
    assert catalog["wraps"] == sp.SILVERPOINT_VERSION


def test_req556_export_is_not_a_derived_pin(catalog):
    # `derived` marks silverpoint's interim pin; the wrapper's own export never carries it.
    assert "derived" not in catalog


def test_req553_every_builder_in_all_is_present(catalog):
    named = _builders(catalog) | set(catalog["helpers"]) | {"sp_trigger"}
    lowercase = {name for name in sp.__all__ if name[0].islower()}
    assert lowercase == named
    assert {info.factory_name for info in sp.CHARTS} <= _builders(catalog)
    assert {f"sp_{info.slug.replace('-', '_')}" for info in sp.UI_COMPONENTS} <= _builders(catalog)
    assert not {name for name in catalog["helpers"] if name.startswith("sp_")}


def test_req553_chart_slugs_match_silverpoint(catalog):
    silverpoint = json.loads((FIXTURES / "silverpoint-slugs.json").read_text())
    slugs = [c["slug"] for c in catalog["charts"]]
    # The same 60 slugs; the order is each catalog's own (by family here, by phase there).
    assert len(slugs) == len(set(slugs)) == 60
    assert set(slugs) == set(silverpoint["charts"])


def test_req553_component_slugs_match_silverpoint(catalog):
    silverpoint = json.loads((FIXTURES / "silverpoint-slugs.json").read_text())
    # Besides silverpoint's 38 components: the dashboard and the timeline (catalog entries of their
    # own there) and the parts a component is built from, which Reflex exposes as builders.
    parts = {"dashboard", "timeline", "avatar-group", "collapse-item", "tab-panel", "toaster"}
    assert {c["slug"] for c in catalog["components"]} == set(silverpoint["components"]) | parts


def test_req553_props_carry_python_and_js_names(catalog):
    for entry in [*catalog["charts"], *catalog["components"]]:
        names = [p["name"] for p in entry["props"]]
        assert len(names) == len(set(names)), entry["slug"]
        for prop in entry["props"]:
            assert set(prop) == {"name", "js", "type"}
            assert prop["name"] == prop["name"].lower(), prop
    line = next(c for c in catalog["charts"] if c["slug"] == "line-chart")
    assert {"name": "x_key", "js": "xKey", "type": "Accessor<string | number>"} in line["props"]
    assert [p["name"] for p in catalog["common"]["chart"]][:2] == ["data", "ground"]
    assert "palette" in {p["name"] for p in catalog["common"]["ui"]}


def test_req553_drillable_charts_list_on_root_change(catalog):
    # Declared on a private base class, so only the chart's PropDocs can name it.
    event = {"name": "on_root_change", "js": "onRootChange", "type": "(id: string | null) => void"}
    for slug in ("squarified-treemap", "sunburst-chart"):
        chart = next(c for c in catalog["charts"] if c["slug"] == slug)
        assert event in chart["props"], slug


def test_req553_deprecated_arguments_are_listed(catalog):
    deprecated = {c["builder"]: c["deprecated"] for c in catalog["components"] if c["deprecated"]}
    assert deprecated == {
        "sp_drawer": {"size": "extent"},
        "sp_input_number": {"input_id": "id"},
        "sp_popover": {"side_offset": "offset"},
        "sp_textarea": {"textarea_id": "id"},
        "sp_toast": {"action_alt": ""},
        "sp_tooltip": {"side_offset": "offset"},
    }


#: What each builder needs besides the argument under test, and a value for it.
_REQUIRED: dict[str, tuple[tuple, dict]] = {
    "sp_popover": (("Body",), {"trigger": "Open"}),
    "sp_tooltip": (("Hover", "Tip"), {}),
    "sp_toast": (("Saved",), {}),
}
_VALUES = {"extent": 320, "id": "field", "offset": 9}


@pytest.mark.parametrize(
    ("builder", "old", "new"),
    [(builder, old, new) for builder, names in export_catalog.DEPRECATED.items() for old, new in names.items()],
)
def test_req553_deprecated_arguments_still_mean_their_new_name(builder, old, new):
    build = getattr(sp, builder)
    args, kwargs = _REQUIRED.get(builder, ((), {}))
    with warnings.catch_warnings():
        warnings.simplefilter("ignore", DeprecationWarning)
        if not new:  # ignored: the build is the same as without it
            assert str(build(*args, **kwargs, **{old: "x"}).render()) == str(build(*args, **kwargs).render())
            return
        value = _VALUES[new]
        old_render = build(*args, **kwargs, **{old: value}).render()
        assert str(old_render) == str(build(*args, **kwargs, **{new: value}).render())


def test_req553_export_equals_silverpoint_derived_pin(catalog):
    """While the two agree: silverpoint's interim pin, read from this repository with ``ast``.

    The pin (tests/fixtures/reflex-catalog.derived.json, silverpoint v0.8.0) was derived from 0.7.1
    wrapping 0.7.0; its reader cannot see a builder's deprecated arguments, and its chart props came
    from the PropDocs before they named the drill-down event.
    """
    pin = json.loads((FIXTURES / "reflex-catalog.derived.json").read_text())
    derived = pin.pop("derived")
    assert derived
    ours = json.loads(json.dumps(catalog))
    for entry in ours["components"]:
        entry["deprecated"] = {}
    for entry in ours["charts"]:
        entry["props"] = [p for p in entry["props"] if p["name"] != "on_root_change"]
    for key in ("version", "wraps"):
        pin.pop(key)
        ours.pop(key)
    assert ours == pin


def test_req553_committed_catalog_is_current(catalog):
    committed = (ROOT / "reflex-catalog.json").read_text()
    assert committed == export_catalog.dumps(catalog), "run: uv run python scripts/export_catalog.py"
