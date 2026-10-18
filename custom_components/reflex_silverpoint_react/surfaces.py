"""The surface: the root every Reflex-composed silverpoint component is built on.

silverpoint's UI stylesheet (``@silverpoint/grounds/ui.css``) does not style components by name
alone. It draws a hand-inked frame and a hatched tone on any element that follows its markup
contract::

    <div class="sp-ui sp-ground-silverpoint" data-substrate="cream" data-mode="ink" data-frame="3">
      <span part="sp-tone" data-tone="1" aria-hidden="true"></span>
      <span part="sp-frame" data-kind="card" aria-hidden="true"></span>
      …content…
    </div>

:class:`SpSurface` renders that contract, resolving ground, substrate, mode and frame variant with
``@silverpoint/core``'s own ``resolveUi`` (so a surface draws exactly as an ``Sp`` component does)
and switching to ``precision`` under ``prefers-contrast: more`` / ``forced-colors: active``.

The tables, overlays and other components of :mod:`.composed` and :mod:`.overlays` are built from
surfaces. They are Reflex-only: not part of silverpoint's React/Vue/Angular parity contract.
"""

import json
from pathlib import Path
from typing import Any, Literal

import reflex as rx
from reflex_base.utils.imports import ImportVar

from .base import SILVERPOINT_STYLESHEETS, SILVERPOINT_VERSION, GroundName, InkMode, Substrate
from .palette import PaletteLike, apply_palette
from .ui import SILVERPOINT_UI_STYLESHEET

_ASSETS = Path(__file__).parent / "assets"

#: Layout of the composed components, injected once into ``<head>`` by the first surface.
SURFACES_CSS = (_ASSETS / "surfaces.css").read_text(encoding="utf-8")

#: The JS components (surface, glyph, pagination, input number), as Reflex custom code.
SURFACES_CODE = f"const SP_REFLEX_CSS = {json.dumps(SURFACES_CSS)};\n" + (_ASSETS / "surface.jsx").read_text(
    encoding="utf-8"
)

#: The five frame kinds a ground draws (``UI_FRAME_KINDS``).
FrameKind = Literal["control", "pill", "box", "card", "round"]

#: A tone by level (1 lightest … 4 darkest) or by state.
ToneLevel = Literal[1, 2, 3, 4, "1", "2", "3", "4", "selected", "primary", "danger", "disabled"]

#: Control size.
SurfaceSize = Literal["sm", "md", "lg"]

#: The glyphs a :class:`SpGlyph` can draw: the Sp components' own, plus a few of ours.
Glyph = Literal[
    "tick",
    "dash",
    "cross",
    "warning",
    "dot",
    "lozenge",
    "info",
    "plus",
    "chevronDown",
    "chevronRight",
    "chevronLeft",
    "arrowUp",
    "arrowDown",
    "sortUp",
    "sortDown",
    "sort",
    "ellipsis",
]

_CORE = f"@silverpoint/core@{SILVERPOINT_VERSION}"


class _SurfaceCode(rx.Component):
    """Imports and custom code shared by every JS component of this module."""

    lib_dependencies: list[str] = [  # noqa: RUF012 - Reflex reads it as a class attribute
        f"@silverpoint/core@{SILVERPOINT_VERSION}",
        f"@silverpoint/grounds@{SILVERPOINT_VERSION}",
        f"@silverpoint/fonts@{SILVERPOINT_VERSION}",
    ]

    def add_imports(self) -> dict[str, Any]:
        """The stylesheets, React hooks and the two ``@silverpoint/core`` helpers the code uses.

        Returns:
            The imports.
        """
        return {
            "": [*SILVERPOINT_STYLESHEETS, SILVERPOINT_UI_STYLESHEET],
            "react": [ImportVar(tag="useEffect"), ImportVar(tag="useState")],
            _CORE: [
                ImportVar(tag="FORCED_PRECISION_QUERY"),
                ImportVar(tag="resolveUi", package_path="/ui"),
                ImportVar(tag="UI_GLYPHS", package_path="/ui"),
            ],
        }

    def add_custom_code(self) -> list[str]:
        """The surface, glyph, pagination and input-number components.

        Returns:
            One code block, identical for every component, so Reflex emits it once per page.
        """
        return [SURFACES_CODE]


class SurfaceProps(_SurfaceCode):
    """Props every surface-based component shares."""

    # Style ground: ``"silverpoint"`` (default) or ``"cyanotype"``. Surfaces do not read
    # ``silverpoint_provider``: pass the ground explicitly.
    ground: rx.Var[GroundName | str]

    # Substrate within the ground.
    substrate: rx.Var[Substrate]

    # ``ink`` (default) or ``precision``.
    mode: rx.Var[InkMode]

    # ``sm``, ``md`` (default) or ``lg``.
    size: rx.Var[SurfaceSize]

    # Seed of the frame's hand (the frame variant); ``id`` is used when omitted.
    seed: rx.Var[int | str]

    @classmethod
    def create(cls, *children, palette: PaletteLike | None = None, **props) -> rx.Component:
        """Create the component.

        Args:
            *children: Its children.
            palette: Colours of this component: a :class:`Palette`, a preset name, a dict or a var.
            **props: Its props.

        Returns:
            The component.
        """
        props = apply_palette({**props, "palette": palette})
        return super().create(*children, **_dom_attributes(cls, props))


#: Props every Reflex component understands; anything else given to a surface is a DOM attribute.
_REFLEX_PROPS = {"style", "key", "id", "class_name", "custom_attrs", "ref", "autofocus", "special_props"}

#: Attribute names React spells differently from their snake_case Python form.
_REACT_NAMES = {
    "tab_index": "tabIndex",
    "html_for": "htmlFor",
    "read_only": "readOnly",
    "auto_complete": "autoComplete",
}


def _dom_attributes(cls: type[rx.Component], props: dict[str, Any]) -> dict[str, Any]:
    """Move attributes a surface does not declare (``role``, ``aria_label``, ``type``…) to the DOM.

    Reflex turns unknown props of a component into CSS; on a surface they are meant for the
    rendered element, so they go to ``custom_attrs`` (``aria_label`` → ``aria-label``).
    """
    declared = set(cls.get_props()) | set(cls.get_event_triggers()) | _REFLEX_PROPS
    attrs = dict(props.pop("custom_attrs", None) or {})
    for key in [k for k in props if k not in declared]:
        value = props.pop(key)
        if value is None:
            continue
        if key.startswith(("aria_", "data_")):
            name = key.replace("_", "-")
        else:
            name = _REACT_NAMES.get(key, key)
        attrs[name] = value
    if attrs:
        props["custom_attrs"] = attrs
    return props


class SpSurface(SurfaceProps):
    """A silverpoint surface: any element, drawn with a frame and a tone of the ground."""

    tag = "SilverpointSurface"

    # The HTML element to render (``div`` by default).
    element: rx.Var[str]

    # Adds the class ``sp-<name>`` (e.g. ``"card"`` reuses the Sp card's layout).
    name: rx.Var[str]

    # Frame kind drawn over the box: ``control``, ``pill``, ``box``, ``card`` or ``round``.
    frame: rx.Var[FrameKind]

    # Hatched tone laid under the content: 1-4 or ``selected``, ``primary``, ``danger``, ``disabled``.
    tone: rx.Var[ToneLevel]


class SpGlyph(_SurfaceCode):
    """A drawn 16×16 mark (``tick``, ``cross``, ``chevronDown``…), stroked with the text colour."""

    tag = "SilverpointGlyph"

    # The glyph's name.
    glyph: rx.Var[Glyph]


def _page_spec(page):
    """The page chosen.

    Args:
        page: The new page, 1-based.

    Returns:
        The page, forwarded to the handler.
    """
    return (page,)


def _number_spec(value):
    """The new number.

    Args:
        value: A number, or null when the field was emptied.

    Returns:
        The value, forwarded to the handler (annotate it ``float | None``).
    """
    return (value,)


class SpPagination(SurfaceProps):
    """Page navigation: previous/next, the first and last page, a window around the current one.

    Controlled with ``current`` + ``on_change``, or uncontrolled with ``default_current``. The
    current page is heightened, the others are drawn buttons.
    """

    tag = "SilverpointPagination"

    # Number of items in all pages.
    total: rx.Var[int]

    # Items per page (10 by default).
    page_size: rx.Var[int]

    # The current page, 1-based (controlled).
    current: rx.Var[int]

    # The initial page (uncontrolled).
    default_current: rx.Var[int]

    # Pages shown on each side of the current one (1 by default).
    siblings: rx.Var[int]

    # Prints "start–end of total" before the pages.
    show_total: rx.Var[bool]

    # The summary's text: ``{start}``, ``{end}`` and ``{total}`` are replaced.
    total_template: rx.Var[str]

    # Accessible name of the navigation landmark.
    label: rx.Var[str]

    # Accessible names of the arrows and of each page ("Page 3").
    previous_label: rx.Var[str]
    next_label: rx.Var[str]
    page_label: rx.Var[str]

    # Disables every page.
    disabled: rx.Var[bool]

    # A page was chosen.
    on_change: rx.EventHandler[_page_spec]


class SpInputNumber(SurfaceProps):
    """A number field with exact − and + steppers; the value is clamped to ``min``/``max``.

    ``on_change`` receives the number (or ``None`` when the field is emptied), never a DOM event.
    """

    tag = "SilverpointInputNumber"

    # The value (controlled).
    value: rx.Var[int | float | None]

    # The initial value (uncontrolled).
    default_value: rx.Var[int | float]

    # Bounds and step (1 by default).
    min: rx.Var[int | float]
    max: rx.Var[int | float]
    step: rx.Var[int | float]

    # Decimals the value is rounded to.
    precision: rx.Var[int]

    # Placeholder text.
    placeholder: rx.Var[str]

    # Accessible name of the field.
    label: rx.Var[str]

    # Help or error text under the field.
    message: rx.Var[str]

    # Marks the value as invalid.
    invalid: rx.Var[bool]

    # Disabled or read-only.
    disabled: rx.Var[bool]
    read_only: rx.Var[bool]

    # Form field name.
    name: rx.Var[str]

    # ``id`` of the native input (the surface's own ``id`` stays on the root).
    input_id: rx.Var[str]

    # Accessible names of the steppers.
    decrement_label: rx.Var[str]
    increment_label: rx.Var[str]

    # The value changed.
    on_change: rx.EventHandler[_number_spec]


sp_surface = SpSurface.create
sp_glyph = SpGlyph.create
sp_pagination = SpPagination.create
sp_input_number = SpInputNumber.create
