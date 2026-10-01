"""The UI catalog: the 17 components of silverpoint 0.3, their declared states and demo props.

``UI_COMPONENTS`` mirrors ``UI_COMPONENTS`` of ``@silverpoint/core/ui`` (17 components, 45 states)
and ``UI_DEMOS`` mirrors ``UI_DEMOS`` of ``@silverpoint/core/ui-demos``: the reference states the
upstream example apps, fixtures and documentation share. :func:`ui_demo` renders one of them.
"""

import inspect
import re
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any, Literal

import reflex as rx

from . import ui as _ui
from .catalog import PropDoc
from .ui import step_item, ui_item

UiGroup = Literal["actions", "data-entry", "navigation", "data-display", "feedback"]

#: The catalog's groups, in the order the documentation lists them.
UI_GROUPS: tuple[tuple[UiGroup, str], ...] = (
    ("actions", "Actions"),
    ("data-entry", "Data entry"),
    ("navigation", "Navigation"),
    ("data-display", "Data display"),
    ("feedback", "Feedback"),
)

#: Components whose ``value`` is bound (controlled or default); a Progress's ``value`` is a plain prop.
UI_VALUE_COMPONENTS = frozenset({"input", "checkbox", "radio-group", "switch", "slider", "rate", "segmented", "tabs"})

#: Components whose bound value is a bool: ``checked`` / ``default_checked``.
_CHECKABLE = frozenset({"checkbox", "switch"})

_FIELD = re.compile(r"^\s+(\w+): rx\.(?:Var|EventHandler)\[")


def _snake_to_camel(name: str) -> str:
    head, *rest = name.split("_")
    return head + "".join(part.title() for part in rest)


def _type_of(cls: type, name: str) -> str:
    annotation = inspect.get_annotations(cls).get(name)
    text = getattr(annotation, "__name__", None) if annotation is not None else None
    text = str(annotation) if text in (None, "Var", "EventHandler") else text
    text = re.sub(r"reflex[\w.]*\.|typing\.|rx\.", "", text).removeprefix("Var[").removesuffix("]")
    return re.sub(r"^Union\[(.*)\]$", lambda m: " | ".join(_split_top(m.group(1))), text)


def _split_top(text: str) -> list[str]:
    """``a, b[c, d]`` → ``["a", "b[c, d]"]``: commas outside brackets."""
    parts, depth, start = [], 0, 0
    for i, ch in enumerate(text):
        depth += ch == "["
        depth -= ch == "]"
        if ch == "," and depth == 0:
            parts.append(text[start:i].strip())
            start = i + 1
    return [*parts, text[start:].strip()]


def _prop_docs(cls: type) -> tuple[PropDoc, ...]:
    """The props a class declares itself, documented by the comment block above each one."""
    docs: list[PropDoc] = []
    comment: list[str] = []
    for line in inspect.getsource(cls).splitlines():
        stripped = line.strip()
        if stripped.startswith("#"):
            comment.append(stripped.lstrip("# ").strip())
            continue
        match = _FIELD.match(line)
        if match:
            name = match.group(1)
            kind = "event" if "rx.EventHandler[" in line else _type_of(cls, name)
            doc = re.sub(r":\w+:`([^`]+)`", r"\1()", " ".join(comment)).replace("``", "")
            docs.append(PropDoc(name, _snake_to_camel(name), kind, doc))
        comment = []
    return tuple(docs)


@dataclass(frozen=True)
class UiComponentInfo:
    """One UI component of the catalog."""

    #: Catalog name, as upstream writes it: ``RadioGroup``.
    name: str
    #: Kebab-case slug: ``radio-group`` (``@silverpoint/react/ui/radio-group``).
    slug: str
    group: UiGroup
    #: Declared states; one demo each in :data:`UI_DEMOS`.
    states: tuple[str, ...]
    summary: str
    props: tuple[PropDoc, ...] = field(default_factory=tuple)

    @property
    def component(self) -> str:
        """The exported name, the same as upstream's: ``SpRadioGroup``."""
        return f"Sp{self.name}"

    @property
    def factory_name(self) -> str:
        """The Python factory: ``sp_radio_group``."""
        return "sp_" + self.slug.replace("-", "_")

    @property
    def component_class(self) -> type[_ui.SilverpointUi]:
        """The component class."""
        return getattr(_ui, self.component)

    @property
    def factory(self) -> Callable[..., Any]:
        """The ``create`` factory."""
        return getattr(_ui, self.factory_name)


def _row(name: str, group: UiGroup, states: list[str], summary: str) -> UiComponentInfo:
    slug = re.sub(r"(?<!^)([A-Z])", r"-\1", name).lower()
    return UiComponentInfo(name, slug, group, tuple(states), summary, _prop_docs(getattr(_ui, f"Sp{name}")))


#: Props every UI component takes.
UI_COMMON_PROPS: tuple[PropDoc, ...] = (
    PropDoc("id", "id", "str", "The frame variant and every related id derive from it."),
    *_prop_docs(_ui.SilverpointUi),
    PropDoc("class_name", "className", "str", "Added to the component's root element, after its own classes."),
)

#: The 17 components of silverpoint 0.3 and their 45 declared states.
UI_COMPONENTS: tuple[UiComponentInfo, ...] = (
    _row("Button", "actions", ["default", "primary", "danger", "disabled"], "A native button, or a link with href."),
    _row("Input", "data-entry", ["empty", "filled", "invalid", "disabled"], "A native text input in a framed box."),
    _row(
        "Checkbox",
        "data-entry",
        ["unchecked", "checked", "indeterminate", "disabled"],
        "A native checkbox with an exact tick or dash.",
    ),
    _row("RadioGroup", "data-entry", ["selected", "disabled-item"], "A fieldset of native radios."),
    _row("Switch", "data-entry", ["off", "on", "disabled"], "A native checkbox with role switch."),
    _row("Slider", "data-entry", ["marks", "disabled"], "A native range over an exact rail, with marks."),
    _row("Rate", "data-entry", ["three", "read-only"], "Native radios 1..count, each an exact lozenge."),
    _row("Segmented", "data-entry", ["first", "middle"], "Native radios in one frame."),
    _row("Tabs", "navigation", ["first", "disabled-tab"], "A tablist of native buttons, with tab panels."),
    _row("Steps", "navigation", ["current", "error"], "An ordered list of steps with their status."),
    _row("Card", "data-display", ["plain", "titled"], "A framed card with header, body and footer."),
    _row("Tag", "data-display", ["tone-1", "closable"], "A framed, toned label; closable."),
    _row("Badge", "data-display", ["count", "dot", "overflow"], "A count or a dot beside its content."),
    _row("Divider", "data-display", ["plain", "text"], "A rule, optionally captioned."),
    _row("Progress", "feedback", ["line", "circle", "indeterminate"], "A progressbar, a line or a circle."),
    _row("Alert", "feedback", ["info", "success", "warning", "error"], "An alert or a status by kind; closable."),
    _row("Skeleton", "feedback", ["paragraph", "avatar"], "A loading placeholder."),
)

_PERIODS = [ui_item("day", "Day"), ui_item("week", "Week"), ui_item("month", "Month"), ui_item("year", "Year")]
_GROUNDS = [ui_item("silverpoint", "silverpoint"), ui_item("cyanotype", "cyanotype")]
_TABS = [ui_item("overview", "Overview"), ui_item("traffic", "Traffic"), ui_item("errors", "Errors")]
_STEPS = [step_item("install", "Install"), step_item("import", "Import"), step_item("configure", "Configure")]
_STEPS.append(step_item("publish", "Publish"))

#: The reference states of the 17 components, ``slug → state → props`` (Python names). Besides the
#: component's own props, ``value`` is the bound value of a value component and ``content`` /
#: ``extra`` the text it holds. Every state carries its id, ``<slug>--<state>``.
UI_DEMOS: dict[str, dict[str, dict[str, Any]]] = {
    "button": {
        "default": {"content": "Default"},
        "primary": {"content": "Primary", "variant": "primary"},
        "danger": {"content": "Delete", "variant": "danger"},
        "disabled": {"content": "Disabled", "disabled": True},
    },
    "input": {
        "empty": {
            "label": "Search charts",
            "placeholder": "Search charts…",
            "type": "search",
            "name": "q",
            "value": "",
        },
        "filled": {"label": "City", "name": "city", "value": "Caracas"},
        "invalid": {
            "label": "City",
            "name": "city",
            "value": "Caracas",
            "invalid": True,
            "message": "Required: pick a city",
        },
        "disabled": {"label": "City", "name": "city", "value": "Caracas", "disabled": True},
    },
    "checkbox": {
        "unchecked": {"label": "Legend", "name": "legend", "value": False},
        "checked": {"label": "Baseline", "name": "baseline", "value": True},
        "indeterminate": {"label": "All series", "name": "all", "value": False, "indeterminate": True},
        "disabled": {"label": "Baseline", "name": "baseline", "value": True, "disabled": True},
    },
    "radio-group": {
        "selected": {
            "label": "Ground",
            "name": "ground",
            "items": _GROUNDS,
            "value": "silverpoint",
            "orientation": "horizontal",
        },
        "disabled-item": {
            "label": "Ground",
            "name": "ground",
            "items": [_GROUNDS[0], {**_GROUNDS[1], "disabled": True}],
            "value": "silverpoint",
            "orientation": "horizontal",
        },
    },
    "switch": {
        "off": {"label": "Linked hover", "name": "linked", "value": False},
        "on": {"label": "Precision", "name": "precision", "value": True},
        "disabled": {"label": "Precision", "name": "precision", "value": True, "disabled": True},
    },
    "slider": {
        "marks": {"label": "Volume", "name": "volume", "value": 30, "marks": [0, 25, 50, 75, 100]},
        "disabled": {"label": "Volume", "name": "volume", "value": 30, "disabled": True},
    },
    "rate": {
        "three": {"label": "Quality", "name": "quality", "value": 3, "count": 5},
        "read-only": {"label": "Quality", "name": "quality", "value": 3, "count": 5, "read_only": True},
    },
    "segmented": {
        "first": {"label": "Period", "name": "period", "items": _PERIODS, "value": "day"},
        "middle": {"label": "Period", "name": "period", "items": _PERIODS, "value": "week"},
    },
    "tabs": {
        "first": {"label": "Views", "items": [*_TABS, ui_item("settings", "Settings")], "value": "overview"},
        "disabled-tab": {
            "label": "Views",
            "items": [*_TABS, ui_item("settings", "Settings", disabled=True)],
            "value": "traffic",
        },
    },
    "steps": {
        "current": {"label": "Release", "items": _STEPS, "current": 2},
        "error": {
            "label": "Release",
            "items": [{**s, "status": "error"} if s["key"] == "configure" else s for s in _STEPS],
            "current": 2,
        },
    },
    "card": {
        "plain": {"content": "Hits per hour rose through the afternoon and eased at night."},
        "titled": {"title": "Revenue", "extra": "Q3", "content": "128 thousands, up 6.4 on the quarter."},
    },
    "tag": {
        "tone-1": {"content": "draft", "tone": 1},
        "closable": {"content": "review", "tone": 3, "closable": True},
    },
    "badge": {
        "count": {"content": "Inbox", "count": 12},
        "dot": {"content": "Alerts", "dot": True},
        "overflow": {"content": "Mentions", "count": 120, "max": 99},
    },
    "divider": {
        "plain": {},
        "text": {"text": "or"},
    },
    "progress": {
        "line": {"label": "Upload", "value": 40},
        "circle": {"label": "Coverage", "value": 72, "shape": "circle"},
        "indeterminate": {"label": "Loading"},
    },
    "alert": {
        "info": {"kind": "info", "title": "New ground available", "content": "cyanotype ships in 0.2.0."},
        "success": {"kind": "success", "title": "Published", "content": "Every package reached npm."},
        "warning": {"kind": "warning", "title": "Contrast check", "content": "One ink is close to 4.5:1 on ochre."},
        "error": {"kind": "error", "title": "Build failed", "content": "ui.css is over its 24 KB budget."},
    },
    "skeleton": {
        "paragraph": {"lines": 3},
        "avatar": {"lines": 3, "avatar": True},
    },
}
for _slug, _states in UI_DEMOS.items():
    for _state, _props in _states.items():
        _props["id"] = f"{_slug}--{_state}"


def ui_component_by_slug(slug: str) -> UiComponentInfo | None:
    """The UI component with this slug, e.g. ``radio-group``.

    Args:
        slug: Kebab-case slug.

    Returns:
        The component, or ``None``.
    """
    return next((info for info in UI_COMPONENTS if info.slug == slug), None)


def ui_demo(slug: str, state: str, *children: rx.Component, controlled: bool = False, **overrides: Any) -> rx.Component:
    """Render one reference state of :data:`UI_DEMOS`.

    The demo's ``value`` becomes ``default_value`` (or ``default_checked``), so the component is
    uncontrolled, as a consumer writes it; with ``controlled=True`` it becomes ``value`` (or
    ``checked``), and ``overrides`` should then carry an ``on_change``.

    Args:
        slug: The component's slug, e.g. ``"radio-group"``.
        state: One of its declared states, e.g. ``"selected"``.
        *children: Replace the demo's text content (e.g. ``sp_tab_panel`` elements for tabs).
        controlled: Bind ``value`` instead of the default value.
        **overrides: Props that win over the demo's: ``ground``, ``substrate``, ``mode``, ``id``…

    Returns:
        The component.

    Raises:
        KeyError: If the component or the state is unknown.
    """
    info = ui_component_by_slug(slug)
    if info is None:
        raise KeyError(f"Unknown UI component {slug!r}")
    props = dict(UI_DEMOS[slug][state])
    content = props.pop("content", None)
    if "value" in props and slug in UI_VALUE_COMPONENTS:
        value = props.pop("value")
        if slug in _CHECKABLE:
            props["checked" if controlled else "default_checked"] = value
        else:
            props["value" if controlled else "default_value"] = value
    props.update(overrides)
    if not children and content is not None:
        children = (content,)
    return info.factory(*children, **props)
