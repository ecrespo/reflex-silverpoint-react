"""Regressions for #44 (a controlled overlay with a text trigger) and #45 (the exported SVG has no colours)."""

import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest
import reflex as rx
import reflex_silverpoint_react as sp
from reflex_silverpoint_react import helpers

ROOT = Path(__file__).parent.parent
TRIGGER_SOURCE = Path(sp.__file__).parent / "assets" / "trigger.jsx"


class _S(rx.State):
    flag: bool = False

    @rx.event
    def set_flag(self, value: bool):
        self.flag = value


# ── #44: sp_trigger is a module, not custom code ────────────────────────────────────────


def _imports_trigger(component: rx.Component) -> bool:
    library = sp.SpTrigger.create("x").library
    return any(var.tag == "SilverpointTrigger" for var in component._get_all_imports().get(library, []))


def test_trigger_is_a_module_of_its_own_not_custom_code() -> None:
    trigger = sp.sp_trigger("Go")
    # Reflex writes custom code into the page module only; a module is imported wherever it renders.
    assert trigger.library is not None and trigger.library.startswith("$/public/")
    assert trigger.library.endswith("trigger.jsx")
    assert _imports_trigger(trigger)
    assert not trigger._get_all_custom_code()


def test_trigger_module_exports_the_component_and_imports_what_it_uses() -> None:
    source = TRIGGER_SOURCE.read_text(encoding="utf-8")
    assert re.search(r"^export const SilverpointTrigger\b", source, re.MULTILINE)
    imported = {
        name.strip()
        for names in re.findall(r"^import \{([^}]+)\} from ", source, re.MULTILINE)
        for name in names.split(",")
    }
    used = {
        "createElement",
        "forwardRef",
        "useEffect",
        "useState",
        "FORCED_PRECISION_QUERY",
        "resolveUi",
        "uiButtonView",
        "UI_GLYPHS",
    }
    assert used <= imported
    assert re.search(r'from "@silverpoint/core/ui";', source) and re.search(r'from "react";', source)


@pytest.mark.parametrize("trigger", ["Edit order", "builder"])
def test_a_controlled_overlay_imports_its_text_trigger(trigger: str) -> None:
    given = sp.sp_trigger("Edit order") if trigger == "builder" else trigger
    modal = sp.sp_modal("Body", title="Edit order", trigger=given, open=_S.flag, on_open_change=_S.set_flag)
    assert _imports_trigger(modal)
    assert not modal._get_all_custom_code()


def _load_checker():
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "check_compiled_trigger", ROOT / "scripts" / "check_compiled_trigger.py"
    )
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


IMPORT = 'import {SilverpointTrigger} from "$/public/external/reflex_silverpoint_react/assets/trigger.jsx"\n'
RENDER = 'jsx(SpModal,{trigger:(jsx(SilverpointTrigger, ({}), "Edit order"))})\n'


def _web(tmp_path: Path, files: dict[str, str]) -> Path:
    for name, text in files.items():
        path = tmp_path / ".web" / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text)
    return tmp_path / ".web"


def test_compiled_check_passes_when_every_module_imports_the_trigger(tmp_path: Path) -> None:
    """What CI runs on the compiled demo: the repro of #44 is a stateful module under app_components/."""
    web = _web(tmp_path, {"app/routes/_index.jsx": IMPORT + RENDER, "app_components/demo/pages.jsx": IMPORT + RENDER})
    assert _load_checker().check(web) == []


def test_compiled_check_names_the_module_that_renders_an_undefined_trigger(tmp_path: Path) -> None:
    files = {
        # 0.9.1: the page defined the trigger as custom code; the stateful module only rendered it.
        "app/routes/_index.jsx": "const SilverpointTrigger = forwardRef(function SilverpointTrigger() {});\n" + RENDER,
        "app_components/demo/pages.jsx": RENDER,
        "node_modules/x/index.jsx": RENDER,
    }
    problems = _load_checker().check(_web(tmp_path, files))
    assert len(problems) == 2 and all("does not import SilverpointTrigger" in p for p in problems)
    assert any("app_components/demo/pages.jsx" in p for p in problems) and not any(
        "node_modules" in p for p in problems
    )


def test_compiled_check_fails_when_no_stateful_module_renders_the_trigger(tmp_path: Path) -> None:
    # The demo must keep an overlay controlled from state with a text trigger, or the check proves nothing.
    web = _web(tmp_path, {"app/routes/_index.jsx": IMPORT + RENDER})
    assert any("app_components" in p for p in _load_checker().check(web))


# ── #45: the exported SVG paints itself ─────────────────────────────────────────────────


def test_export_scripts_embed_the_page_stylesheet_in_the_svg() -> None:
    for spec in (sp.download_svg("hits", "hits.svg"), sp.get_svg("hits", _S.set_flag)):
        script = str(spec.args[0][1])
        assert "toSVGString" in script
        assert "document.styleSheets" in script
        assert "<style><![CDATA[" in script and "]]></style>" in script


NODE = shutil.which("node")

HARNESS = """
const sheets = %(sheets)s;
globalThis.document = {
  styleSheets: sheets.map((rules) =>
    rules === null
      ? { get cssRules() { throw new Error("SecurityError"); } }
      : { cssRules: rules.map(function rule(r) { return typeof r === "string" ? { cssText: r } : { cssText: r.text, cssRules: r.rules.map(rule) }; }) }),
};
const standalone = %(standalone)s;
console.log(JSON.stringify(standalone(%(svg)s)));
"""


def _standalone(svg: object, sheets: list) -> object:
    script = HARNESS % {"sheets": json.dumps(sheets), "standalone": helpers.STANDALONE_SVG_JS, "svg": json.dumps(svg)}
    done = subprocess.run([NODE, "-e", script], capture_output=True, text=True, timeout=60, check=True)
    return json.loads(done.stdout)


SVG = '<svg class="sp-chart sp-ground-silverpoint" aria-label="a > b"><path class="sp-line"/></svg>'


@pytest.mark.skipif(NODE is None, reason="needs node to run the browser script")
def test_standalone_svg_carries_the_silverpoint_rules_in_cdata() -> None:
    sheets = [
        [
            ":where(.sp-ground-silverpoint) { --sp-ink: #303030; }",
            ".sp-line { stroke: var(--sp-ink); }",
            "body { margin: 0; }",
            {
                "text": "@media (forced-colors: active) { .sp-line { stroke: CanvasText; } .other { color: red; } }",
                "rules": [".sp-line { stroke: CanvasText; }", ".other { color: red; }"],
            },
            {"text": "@media print { .other { color: red; } }", "rules": [".other { color: red; }"]},
        ],
        None,  # a cross-origin stylesheet: reading its rules throws
        ['.sp-x::after { content: "]]>"; }'],
    ]
    out = _standalone(SVG, sheets)
    assert isinstance(out, str)
    # First child of the root; the ">" inside the root's quoted attribute does not end its tag.
    head = '<svg class="sp-chart sp-ground-silverpoint" aria-label="a > b"><style><![CDATA['
    assert out.startswith(head) and out.endswith(']]></style><path class="sp-line"/></svg>')
    css = out[len(head) : out.index("]]></style>")]
    assert "--sp-ink: #303030" in css and ".sp-line { stroke: var(--sp-ink); }" in css
    # Only silverpoint's rules, also inside a conditional group; the app's own rules stay out.
    assert "body" not in css and ".other" not in css and "print" not in css
    assert "@media (forced-colors: active) {.sp-line { stroke: CanvasText; }}" in css.replace("\n", "")
    # A CDATA terminator inside the stylesheet cannot close the section early.
    assert 'content: "]]]]><![CDATA[>"' in out


@pytest.mark.skipif(NODE is None, reason="needs node to run the browser script")
def test_standalone_svg_leaves_other_values_alone() -> None:
    assert _standalone(None, [[".sp-line { stroke: red; }"]]) is None
    assert _standalone("<div></div>", [[".sp-line { stroke: red; }"]]) == "<div></div>"
    # No silverpoint rule on the page: nothing to add.
    assert _standalone(SVG, [["body { margin: 0; }"]]) == SVG


def test_docstrings_say_where_the_colours_come_from() -> None:
    assert "carries its own ground colours" not in (sp.download_svg.__doc__ or "")
    for function in (sp.download_svg, sp.get_svg):
        assert "stylesheet" in (function.__doc__ or "")
