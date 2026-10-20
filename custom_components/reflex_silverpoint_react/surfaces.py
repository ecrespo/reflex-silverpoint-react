"""The surface and the glyph of silverpoint 0.7, and the two composed controls with a value.

``SpSurface`` is the root contract of ``@silverpoint/grounds/ui.css`` on any element: the ground's
classes and data attributes, an optional hand-inked frame (``<span part="sp-frame">``) and a hatched
tone (``<span part="sp-tone">``). ``SpGlyph`` draws one of the exact 16×16 marks (``UI_GLYPHS``).
Both are ``@silverpoint/react``'s own components (``/ui`` subpath), drawn by the core as every
``Sp`` component is; build your own silverpoint-drawn pieces from them.

``SpPagination`` and ``SpInputNumber`` live here too, beside the other composed components of
:mod:`.composed`, because their value binding (``current`` / ``value`` with ``on_change``) is the
``Sp`` components' own.
"""

import warnings
from typing import Any, Literal

import reflex as rx

from .ui import SilverpointUi

#: The five frame kinds a ground draws (``UI_FRAME_KINDS``).
FrameKind = Literal["control", "pill", "box", "card", "round"]

#: A tone by level (1 lightest … 4 darkest) or by state.
ToneLevel = Literal[1, 2, 3, 4, "1", "2", "3", "4", "selected", "primary", "danger", "disabled"]

#: The glyphs ``UI_GLYPHS`` of ``@silverpoint/core/ui`` draws.
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


def _renamed(props: dict[str, Any], old: str, new: str) -> dict[str, Any]:
    """Move a 0.7.0 argument to its new name, with a deprecation warning."""
    if old in props:
        warnings.warn(f"{old}= is deprecated; use {new}= (0.7.1).", DeprecationWarning, stacklevel=3)
        value = props.pop(old)
        props.setdefault(new, value)
    return props


class SpSurface(SilverpointUi):
    """A silverpoint surface: any element, drawn with a frame and a tone of the ground."""

    tag = "SpSurface"

    # Adds the class ``sp-<name>`` (e.g. ``"card"`` reuses the Sp card's layout).
    name: rx.Var[str]

    # Frame kind drawn over the box: ``control``, ``pill``, ``box``, ``card`` or ``round``.
    frame: rx.Var[FrameKind]

    # Hatched tone laid under the content: 1-4 or ``selected``, ``primary``, ``danger``, ``disabled``.
    tone: rx.Var[ToneLevel]

    @classmethod
    def create(cls, *children, element: str | None = None, **props) -> rx.Component:
        """Create the surface.

        Args:
            *children: Its content.
            element: The HTML element to render, a lowercase tag name (``div`` by default); the npm
                ``as`` prop.
            **props: Its props (``name``, ``frame``, ``tone``, ``ground``, ``palette``…).

        Returns:
            The component.
        """
        if element is not None:
            props["custom_attrs"] = {**(props.get("custom_attrs") or {}), "as": element}
        return super().create(*children, **props)


class SpGlyph(SilverpointUi):
    """A drawn 16×16 mark (``tick``, ``cross``, ``chevronDown``…), stroked with the text colour."""

    tag = "SpGlyph"

    # The glyph's name, a key of ``UI_GLYPHS``.
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


class SpPagination(SilverpointUi):
    """Page navigation: previous/next, the first and last page, a window around the current one.

    Controlled with ``current`` + ``on_change``, or uncontrolled with ``default_current``. The
    current page is heightened, the others are drawn buttons.
    """

    tag = "SpPagination"

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


class SpInputNumber(SilverpointUi):
    """A number field with exact − and + steppers; the value is clamped to ``min``/``max``.

    ``on_change`` receives the number (or ``None`` when the field is emptied), never a DOM event:
    on commit (blur or Enter) for what is typed, at once for the steppers.
    """

    tag = "SpInputNumber"

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

    # Accessible names of the steppers.
    decrement_label: rx.Var[str]
    increment_label: rx.Var[str]

    # The value changed.
    on_change: rx.EventHandler[_number_spec]

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        """Create the field.

        Args:
            *children: Unused.
            **props: Its props. ``input_id`` (0.7.0) is now ``id``: the core derives the native
                input's id from it.

        Returns:
            The component.
        """
        return super().create(*children, **_renamed(props, "input_id", "id"))


sp_surface = SpSurface.create
sp_glyph = SpGlyph.create
sp_pagination = SpPagination.create
sp_input_number = SpInputNumber.create
