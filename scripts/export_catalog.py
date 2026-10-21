"""Export the Reflex catalog, `reflex-catalog.json` (silverpoint Data Model §2.30, T-230).

silverpoint's agent catalog joins it by slug and JS prop name, so an agent sees the snake_case
builders and props beside the React names; every entry is marked stale when `wraps` is not the
silverpoint version the agent catalog describes (REQ-556). It is built from the package itself:
`CHARTS` and their `PropDoc`s, `COMMON_PROPS`, the builders of `__all__` with their signatures, and
the props each component class declares. Type names are the annotations as the source writes them.

    uv run python scripts/export_catalog.py            # writes reflex-catalog.json
    uv run python scripts/export_catalog.py --check    # fails when the committed file is stale
"""

import ast
import importlib.metadata
import inspect
import json
import sys
import textwrap
from pathlib import Path
from typing import Any

import reflex_silverpoint_react as sp

OUT = Path(__file__).resolve().parent.parent / "reflex-catalog.json"

#: Arguments a builder still accepts from an earlier version: old name → its replacement ("" when
#: it is ignored). tests/test_agent_catalog.py checks that each one still means its replacement.
DEPRECATED: dict[str, dict[str, str]] = {
    "sp_drawer": {"size": "extent"},
    "sp_input_number": {"input_id": "id"},
    "sp_popover": {"side_offset": "offset"},
    "sp_textarea": {"textarea_id": "id"},
    "sp_toast": {"action_alt": ""},
    "sp_tooltip": {"side_offset": "offset"},
}

#: Props a builder takes that are not a component's own: its body and the common props.
_NOT_PROPS = {"children", "props"}


def _camel(name: str) -> str:
    head, *rest = name.split("_")
    return head + "".join(part.title() for part in rest)


def _prop(name: str, kind: str) -> dict[str, str]:
    return {"name": name, "js": _camel(name), "type": kind}


def _parsed(obj: Any) -> tuple[ast.AST, str]:
    source = textwrap.dedent(inspect.getsource(obj))
    return ast.parse(source).body[0], source


def class_props(cls: type) -> list[dict[str, str]]:
    """The props a class declares in its own body: `rx.Var[int]` is `int`, an event handler `event`."""
    node, source = _parsed(cls)
    out = []
    for stmt in node.body:
        if not (isinstance(stmt, ast.AnnAssign) and isinstance(stmt.target, ast.Name)):
            continue
        if stmt.target.id.startswith("_") or not isinstance(stmt.annotation, ast.Subscript):
            continue
        head = ast.get_source_segment(source, stmt.annotation.value)
        if head in ("rx.Var", "Var"):
            out.append(_prop(stmt.target.id, ast.get_source_segment(source, stmt.annotation.slice)))
        elif head in ("rx.EventHandler", "EventHandler"):
            out.append(_prop(stmt.target.id, "event"))
    return out


def builder_props(fn: Any) -> tuple[list[dict[str, str]], list[str]]:
    """A builder function's named arguments as props, and those that can be passed by position."""
    node, source = _parsed(fn)
    args = node.args
    positional = [a.arg for a in args.posonlyargs + args.args]
    named = args.posonlyargs + args.args + args.kwonlyargs

    def kind(arg: ast.arg) -> str:
        return ast.get_source_segment(source, arg.annotation) if arg.annotation else "Any"

    return [_prop(a.arg, kind(a)) for a in named], positional


def _component(builder: str) -> dict[str, Any]:
    obj = getattr(sp, builder)
    if inspect.ismethod(obj) and obj.__name__ == "create":
        cls: type | None = obj.__self__
        props, positional = class_props(cls), []
    else:
        props, positional = builder_props(obj)
        # A builder over the component class of the same name also takes that class's props.
        cls = getattr(sp, "Sp" + "".join(part.title() for part in builder.removeprefix("sp_").split("_")), None)
        if cls is not None:
            given = {p["name"] for p in props}
            props += [p for p in class_props(cls) if p["name"] not in given]
    return {
        "slug": builder.removeprefix("sp_").replace("_", "-"),
        "builder": builder,
        "cls": cls.__name__ if cls is not None else "",
        "props": [p for p in props if p["name"] not in _NOT_PROPS],
        "positional": positional,
        "deprecated": DEPRECATED.get(builder, {}),
    }


def build() -> dict[str, Any]:
    """The catalog, as `reflex-catalog.json` holds it."""
    charts = [
        {
            "slug": info.slug,
            "builder": info.factory_name,
            "cls": info.chart,
            "family": info.family,
            "summary": info.summary,
            "props": [{"name": p.name, "js": p.js, "type": p.type} for p in info.props],
        }
        for info in sp.CHARTS
    ]
    common_chart = [{"name": p.name, "js": p.js, "type": p.type} for p in sp.COMMON_PROPS]
    # `COMMON_PROPS` documents the shared chart props; the chart base class declares the rest
    # (`palette`, `tooltip`, the events).
    documented = {p["name"] for p in common_chart}
    common_chart += [p for p in class_props(sp.SilverpointChart) if p["name"] not in documented]

    lowercase = sorted(name for name in sp.__all__ if name[0].islower())
    chart_builders = {c["builder"] for c in charts}
    components = [
        _component(name)
        for name in lowercase
        if (name.startswith("sp_") or name == "dashboard") and name != "sp_trigger"
    ]
    named = chart_builders | {c["builder"] for c in components} | {"sp_trigger"}
    helpers = [name for name in lowercase if name not in named and not name.startswith("sp_")]

    return {
        "schema": 1,
        "package": "reflex-silverpoint-react",
        "version": importlib.metadata.version("reflex-silverpoint-react"),
        "wraps": sp.SILVERPOINT_VERSION,
        "common": {"chart": common_chart, "ui": class_props(sp.SilverpointUi)},
        "charts": charts,
        "components": components,
        "helpers": helpers,
    }


def dumps(catalog: dict[str, Any]) -> str:
    return json.dumps(catalog, indent=2, ensure_ascii=False) + "\n"


def main(argv: list[str]) -> int:
    text = dumps(build())
    if "--check" in argv:
        if not OUT.exists() or OUT.read_text(encoding="utf-8") != text:
            print(f"{OUT.name} is stale: run `uv run python scripts/export_catalog.py`", file=sys.stderr)
            return 1
        return 0
    OUT.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
