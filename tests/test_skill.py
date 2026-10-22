"""Feature-005 (silverpoint): the `reflex-silverpoint` skill (T-246) and its examples check (T-247).

``scripts/make_skill.py`` writes ``skills/reflex-silverpoint/`` from the hand-written templates and
``reflex-catalog.json``. Every ``python`` fence of the skill is imported and the components it builds
are rendered (REQ-557); every other fence is prose.
"""

import ast
import importlib.util
import inspect
import json
import re
import sys
from pathlib import Path

import pytest
import reflex as rx

ROOT = Path(__file__).resolve().parent.parent
SKILL = ROOT / "skills" / "reflex-silverpoint"
FIXTURES = Path(__file__).parent / "fixtures"

_spec = importlib.util.spec_from_file_location("make_skill", ROOT / "scripts" / "make_skill.py")
make_skill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(make_skill)

CATALOG = json.loads((ROOT / "reflex-catalog.json").read_text())
DESCRIPTION = (
    "Build silverpoint charts, dashboards and UI in Python with Reflex through reflex-silverpoint-react. "
    "Use whenever code imports reflex_silverpoint_react or the user wants silverpoint in Reflex."
)


def _files() -> dict[str, str]:
    return {str(p.relative_to(SKILL)): p.read_text() for p in sorted(SKILL.rglob("*.md")) if "templates" not in p.parts}


# ── Layout and contents ─────────────────────────────────────────────────────────────────


def test_req553_skill_is_current():
    assert make_skill.render() == _files(), "run: uv run python scripts/make_skill.py"


def test_req553_skill_layout():
    families = [f["slug"] for f in json.loads((FIXTURES / "silverpoint-slugs.json").read_text())["families"]]
    expected = {"SKILL.md", *(f"references/charts/{slug}.md" for slug in families)}
    expected |= {
        f"references/{name}.md"
        for name in ("components", "overlays", "timeline", "dashboard", "palettes", "state-and-events")
    }
    assert set(_files()) == expected


def test_req554_skill_md_frontmatter_and_length():
    text = (SKILL / "SKILL.md").read_text()
    assert text.startswith(f"---\nname: reflex-silverpoint\ndescription: {DESCRIPTION}\n---\n")
    assert len(text.splitlines()) < 500


def test_req554_every_file_names_the_version_it_describes():
    stamp = f"reflex-silverpoint-react {CATALOG['version']}"
    for path, text in _files().items():
        assert stamp in text, path
        assert f"silverpoint {CATALOG['wraps']}" in text, path


def test_req554_skill_prefers_the_mcp_tools():
    text = (SKILL / "SKILL.md").read_text()
    assert "## Prefer the silverpoint MCP tools when they are connected" in text
    assert "https://silverpointweb.vercel.app/mcp" in text


def test_req553_every_builder_and_helper_is_documented():
    text = "\n".join(_files().values())
    for name in [c["builder"] for c in CATALOG["charts"] + CATALOG["components"]] + CATALOG["helpers"]:
        assert f"`{name}`" in text, name


def test_req553_chart_props_tables_list_python_and_js_names():
    lines = (SKILL / "references" / "charts" / "lines.md").read_text()
    assert "| `x_key` | `xKey` | `Accessor<string \\| number>` |" in lines
    assert "<!-- generated:family -->" in lines and "<!-- /generated:family -->" in lines


def test_req547_overlay_triggers_are_never_sp_button():
    # The prose names the mistake; no example may make it.
    for name, code in make_skill.extract_examples(_files()):
        assert not re.search(r"trigger\s*=\s*sp_button", code), name
    assert "Never `trigger=sp_button(...)`" in (SKILL / "SKILL.md").read_text()


# ── Examples (REQ-557) ──────────────────────────────────────────────────────────────────


def test_req557_extract_refuses_a_fence_that_is_neither_python_nor_prose():
    with pytest.raises(ValueError, match="tsx"):
        make_skill.extract_examples({"x.md": "```tsx\n<LineChart />\n```\n"})
    with pytest.raises(ValueError, match="language"):
        make_skill.extract_examples({"x.md": "```\nplain\n```\n"})
    assert make_skill.extract_examples({"x.md": "```sh\npip install x\n```\n```json\n[]\n```\n"}) == []
    found = make_skill.extract_examples({"a/b.md": "```python\nx = 1\n```\n"})
    assert found == [("a-b-1", "x = 1\n")]


EXAMPLES = make_skill.extract_examples(_files())


def test_req557_the_skill_has_python_examples():
    assert len(EXAMPLES) >= 60 + 10


def _components(module) -> list[rx.Component]:
    """Every component the example builds: module-level ones, and what its views return."""
    found = [v for v in vars(module).values() if isinstance(v, rx.Component)]
    for fn in vars(module).values():
        is_view = inspect.isfunction(fn) and fn.__module__ == module.__name__ and not fn.__name__.startswith("_")
        if is_view and all(p.default is not p.empty for p in inspect.signature(fn).parameters.values()):
            result = fn()
            if isinstance(result, rx.Component):
                found.append(result)
    return found


#: Props Reflex gives every component, besides those the catalog lists.
_REFLEX_PROPS = {"id", "class_name", "style", "key", "custom_attrs", "on_click"}


def _allowed() -> dict[str, set[str]]:
    chart = {p["name"] for p in CATALOG["common"]["chart"]} | _REFLEX_PROPS
    ui = {p["name"] for p in CATALOG["common"]["ui"]} | _REFLEX_PROPS
    allowed = {c["builder"]: {p["name"] for p in c["props"]} | chart for c in CATALOG["charts"]}
    allowed |= {c["builder"]: {p["name"] for p in c["props"]} | ui for c in CATALOG["components"]}
    return allowed


@pytest.mark.parametrize(("name", "code"), EXAMPLES, ids=[name for name, _ in EXAMPLES])
def test_req557_python_example_names_only_catalog_props(name, code):
    # Reflex passes an unknown keyword through to the npm component without a word, so rendering
    # alone does not catch a misspelt prop: every keyword of a builder call must be in the catalog.
    allowed = _allowed()
    tree = ast.parse(code)
    imported = {
        alias.asname or alias.name: alias.name
        for node in ast.walk(tree)
        if isinstance(node, ast.ImportFrom) and node.module == "reflex_silverpoint_react"
        for alias in node.names
    }
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and imported.get(node.func.id) in allowed:
            builder = imported[node.func.id]
            for keyword in node.keywords:
                assert keyword.arg is None or keyword.arg in allowed[builder], f"{builder} takes no {keyword.arg}"


@pytest.mark.parametrize(("name", "code"), EXAMPLES, ids=[name for name, _ in EXAMPLES])
def test_req557_python_example_imports_and_renders(name, code, tmp_path):
    path = tmp_path / f"skill_{name.replace('-', '_')}.py"
    path.write_text(code)
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[path.stem] = module
    try:
        spec.loader.exec_module(module)
        components = _components(module)
        assert components, f"{name} builds no component"
        for component in components:
            assert component.render()
    finally:
        sys.modules.pop(path.stem, None)
