"""The overlays of silverpoint 0.7: modal, drawer, popover, tooltip, select, dropdown menu and toast.

Each one is ``@silverpoint/react``'s own component (``/ui`` subpath), on the platform: a native
``<dialog>`` (``showModal()``) for the modal and the drawer, the Popover API for the rest, keyboard
and placement computed by ``@silverpoint/core`` (``uiListKey``, ``uiTypeahead``, ``uiPlace``). The
drawing is the ground's: card frames, the highlighted option heightened. They render in place (the
top layer, not a portal), so they read ``silverpoint_provider`` and ``silverpoint_palette``.

The open state is controlled with ``open`` + ``on_open_change`` or held from ``default_open``. A
``trigger`` is the element that opens the overlay: the npm component clones it with its ARIA and a
click that toggles it, so it must be an element that keeps the props it is given, a native
``rx.el.button`` or :func:`sp_trigger` (strings become one). Sides are logical, ``start``/``end``,
and mirror in right-to-left text; 0.7.0's ``left``/``right`` still work, with a deprecation warning.
"""

import warnings
from collections.abc import Sequence
from pathlib import Path
from typing import Any, Literal

import reflex as rx
from reflex.event import passthrough_event_spec
from reflex_base.utils.imports import ImportVar

from .base import SILVERPOINT_STYLESHEETS, SILVERPOINT_VERSION, GroundName, InkMode, Substrate
from .palette import PaletteLike, apply_palette
from .ui import SILVERPOINT_UI_STYLESHEET, SilverpointUi, UiSize, UiVariant

Side = Literal["top", "end", "bottom", "start"]
Align = Literal["start", "center", "end"]
ToastKind = Literal["info", "success", "warning", "error"]
ToastPosition = Literal["bottom-end", "bottom-start", "top-end", "top-start"]

#: 0.7.0's physical names → the logical ones of silverpoint 0.7 (REQ-523).
_SIDES: dict[str, str] = {"left": "start", "right": "end"}
_POSITIONS: dict[str, str] = {
    "bottom-right": "bottom-end",
    "bottom-left": "bottom-start",
    "top-right": "top-end",
    "top-left": "top-start",
}

_open_spec = passthrough_event_spec(bool)
_key_spec = passthrough_event_spec(str)

_CORE = f"@silverpoint/core@{SILVERPOINT_VERSION}"

#: The trigger component, as Reflex custom code.
TRIGGER_CODE = (Path(__file__).parent / "assets" / "trigger.jsx").read_text(encoding="utf-8")


def _given(**props: Any) -> dict[str, Any]:
    return {key: value for key, value in props.items() if value is not None}


def _length(value: Any) -> Any:
    return f"{value}px" if isinstance(value, (int, float)) and not isinstance(value, bool) else value


def _logical(value: Any, names: dict[str, str], argument: str) -> Any:
    if isinstance(value, str) and value in names:
        warnings.warn(
            f"{argument}={value!r} is deprecated; use {names[value]!r} (logical sides mirror in RTL).",
            DeprecationWarning,
            stacklevel=3,
        )
        return names[value]
    return value


# ── The trigger ─────────────────────────────────────────────────────────────────────────

#: Props every Reflex component understands; anything else given to a trigger is a DOM attribute.
_REFLEX_PROPS = {"style", "key", "id", "class_name", "custom_attrs", "ref", "autofocus", "special_props"}

#: Attribute names React spells differently from their snake_case Python form.
_REACT_NAMES = {
    "tab_index": "tabIndex",
    "html_for": "htmlFor",
    "read_only": "readOnly",
    "auto_complete": "autoComplete",
}


def _dom_attributes(cls: type[rx.Component], props: dict[str, Any]) -> dict[str, Any]:
    """Move attributes the trigger does not declare (``aria_label``, ``tab_index``…) to the DOM."""
    declared = set(cls.get_props()) | set(cls.get_event_triggers()) | _REFLEX_PROPS
    attrs = dict(props.pop("custom_attrs", None) or {})
    for key in [k for k in props if k not in declared]:
        value = props.pop(key)
        if value is None:
            continue
        name = key.replace("_", "-") if key.startswith(("aria_", "data_")) else _REACT_NAMES.get(key, key)
        attrs[name] = value
    if attrs:
        props["custom_attrs"] = attrs
    return props


class SpTrigger(rx.Component):
    """A native ``<button>`` drawn as ``SpButton`` that keeps every prop an overlay clones onto it."""

    tag = "SilverpointTrigger"

    lib_dependencies: list[str] = [  # noqa: RUF012 - Reflex reads it as a class attribute
        f"@silverpoint/core@{SILVERPOINT_VERSION}",
        f"@silverpoint/grounds@{SILVERPOINT_VERSION}",
        f"@silverpoint/fonts@{SILVERPOINT_VERSION}",
    ]

    ground: rx.Var[GroundName | str]
    substrate: rx.Var[Substrate]
    mode: rx.Var[InkMode]
    size: rx.Var[UiSize]
    seed: rx.Var[int | str]
    palette: rx.Var[dict[str, str]]

    # ``default``, ``primary`` (light hatching) or ``danger``.
    variant: rx.Var[UiVariant]

    # Draws a down chevron after the text.
    chevron: rx.Var[bool]

    # Not focusable; drawn with the disabled tone.
    disabled: rx.Var[bool]

    # Accessible name of a trigger without text.
    label: rx.Var[str]

    def add_imports(self) -> dict[str, Any]:
        """The stylesheets, React and the ``@silverpoint/core`` functions the trigger draws with.

        Returns:
            The imports.
        """
        return {
            "": [*SILVERPOINT_STYLESHEETS, SILVERPOINT_UI_STYLESHEET],
            "react": [
                ImportVar(tag="createElement"),
                ImportVar(tag="forwardRef"),
                ImportVar(tag="useEffect"),
                ImportVar(tag="useState"),
            ],
            _CORE: [
                ImportVar(tag="FORCED_PRECISION_QUERY"),
                ImportVar(tag="resolveUi", package_path="/ui"),
                ImportVar(tag="uiButtonView", package_path="/ui"),
                ImportVar(tag="UI_GLYPHS", package_path="/ui"),
            ],
        }

    def add_custom_code(self) -> list[str]:
        """The trigger component.

        Returns:
            One code block, identical for every trigger, so Reflex emits it once per page.
        """
        return [TRIGGER_CODE]

    @classmethod
    def create(cls, *children, palette: PaletteLike | None = None, **props) -> rx.Component:
        """Create the trigger.

        Args:
            *children: Its text.
            palette: Its colours.
            **props: Its props; any other attribute (``aria_label``, ``on_click``…) goes to the button.

        Returns:
            The component.
        """
        props = apply_palette({**props, "palette": palette})
        return super().create(*children, **_dom_attributes(cls, props))


def sp_trigger(
    label: str | rx.Var | rx.Component,
    *,
    variant: Literal["default", "primary", "danger"] | None = None,
    chevron: bool | None = None,
    **props: Any,
) -> rx.Component:
    """A drawn button for opening an overlay: ``SpButton``'s drawing on a button that keeps its props.

    Unlike :func:`sp_button` it can be an overlay's ``trigger``: the overlay's ARIA and toggle land
    on the native button. Strings passed as ``trigger=`` become one of these. It does not read
    ``silverpoint_provider``; pass ``ground``, ``substrate``, ``mode`` and ``palette`` directly.

    Args:
        label: Its text (or a component).
        variant: ``default``, ``primary`` (light hatching) or ``danger``.
        chevron: Draws a down chevron after the text.
        **props: ``ground``, ``substrate``, ``mode``, ``size``, ``seed``, ``palette``, ``disabled``,
            event triggers and DOM attributes.

    Returns:
        The button.
    """
    return SpTrigger.create(label, **_given(variant=variant, chevron=chevron), **props)


def _as_trigger(trigger: Any, **props: Any) -> Any:
    if trigger is None:
        return None
    return sp_trigger(trigger, **props) if isinstance(trigger, (str, rx.Var)) else trigger


def _common(props: dict[str, Any]) -> dict[str, Any]:
    """The common props a string trigger inherits from its overlay."""
    return {key: props[key] for key in ("ground", "substrate", "mode", "size", "palette") if key in props}


# ── Components ──────────────────────────────────────────────────────────────────────────


class _Overlay(SilverpointUi):
    """The open state every overlay binds (REQ-500)."""

    # Open state (controlled), and the initial one (uncontrolled).
    open: rx.Var[bool]
    default_open: rx.Var[bool]

    # The overlay opened or closed: the new state.
    on_open_change: rx.EventHandler[_open_spec]


class SpModal(_Overlay):
    """A modal ``<dialog>`` on a card frame, over a hatched backdrop."""

    tag = "SpModal"

    title: rx.Var[str]
    description: rx.Var[str]
    label: rx.Var[str]
    closable: rx.Var[bool]
    close_label: rx.Var[str]
    width: rx.Var[str]
    dismissible: rx.Var[bool]
    trigger: rx.Var[rx.Component]
    footer: rx.Var[rx.Component]


class SpDrawer(_Overlay):
    """A ``<dialog>`` against one side of the window."""

    tag = "SpDrawer"

    title: rx.Var[str]
    description: rx.Var[str]
    label: rx.Var[str]
    closable: rx.Var[bool]
    close_label: rx.Var[str]
    dismissible: rx.Var[bool]
    side: rx.Var[Literal["start", "end", "top", "bottom"]]
    extent: rx.Var[str]
    modal: rx.Var[bool]
    trigger: rx.Var[rx.Component]
    footer: rx.Var[rx.Component]


class SpPopover(_Overlay):
    """A card anchored to its trigger (Popover API)."""

    tag = "SpPopover"

    title: rx.Var[str]
    label: rx.Var[str]
    side: rx.Var[Side]
    align: rx.Var[Align]
    offset: rx.Var[int]
    closable: rx.Var[bool]
    close_label: rx.Var[str]
    width: rx.Var[str]
    trigger: rx.Var[rx.Component]


class SpTooltip(_Overlay):
    """A short description shown on hover and focus of its trigger."""

    tag = "SpTooltip"

    text: rx.Var[str]
    side: rx.Var[Side]
    align: rx.Var[Align]
    offset: rx.Var[int]
    delay: rx.Var[int]
    trigger: rx.Var[rx.Component]


class SpSelect(_Overlay):
    """A drawn field opening a list of options (APG combobox + listbox)."""

    tag = "SpSelect"

    items: rx.Var[list[str | dict[str, Any]]]
    placeholder: rx.Var[str]
    label: rx.Var[str]
    disabled: rx.Var[bool]
    required: rx.Var[bool]
    name: rx.Var[str]
    width: rx.Var[str]
    value: rx.Var[str | None]
    default_value: rx.Var[str | None]

    # An option was chosen: its key.
    on_change: rx.EventHandler[_key_spec]


class SpDropdownMenu(_Overlay):
    """A menu of commands (APG menu button)."""

    tag = "SpDropdownMenu"

    items: rx.Var[list[dict[str, Any]]]
    label: rx.Var[str]
    side: rx.Var[Side]
    align: rx.Var[Align]
    trigger: rx.Var[rx.Component]

    # A command was chosen: its key.
    on_select: rx.EventHandler[_key_spec]


class SpToast(_Overlay):
    """A notice in the toaster; it closes itself after ``duration``."""

    tag = "SpToast"

    title: rx.Var[str]
    description: rx.Var[str]
    kind: rx.Var[ToastKind]
    duration: rx.Var[int | float]
    close_label: rx.Var[str]
    action: rx.Var[rx.Component]


class SpToaster(SilverpointUi):
    """The notification region (F8 focuses it); its children are the toasts."""

    tag = "SpToaster"

    position: rx.Var[ToastPosition]
    duration: rx.Var[int]
    label: rx.Var[str]


# ── Builders ────────────────────────────────────────────────────────────────────────────


def _open(open: Any, default_open: Any, on_open_change: Any) -> dict[str, Any]:
    return _given(open=open, default_open=default_open, on_open_change=on_open_change)


def sp_modal(
    *children: Any,
    trigger: Any = None,
    title: Any = None,
    description: Any = None,
    footer: Any = None,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    closable: bool | None = None,
    close_label: str | None = None,
    width: int | str | None = None,
    label: str | None = None,
    dismissible: bool | None = None,
    **props: Any,
) -> rx.Component:
    """A modal dialog on a card frame, over a hatched backdrop. Focus stays in it while it is open.

    Args:
        *children: The body.
        trigger: What opens it: a string (becomes :func:`sp_trigger`) or an element that keeps the
            props it is given (``rx.el.button``, :func:`sp_trigger`).
        title: The heading and accessible name.
        description: A line under the title (the accessible description).
        footer: Actions, aligned to the end.
        open: Open state (controlled).
        default_open: Initial open state (uncontrolled).
        on_open_change: Handler receiving the new open state.
        closable: Draws the close cross (default).
        close_label: Accessible name of the cross.
        width: Width (px or CSS length); 520 px by default.
        label: Accessible name when there is no title.
        dismissible: Escape and a backdrop click close it (default).
        **props: Common props (``ground``, ``substrate``, ``mode``, ``palette``…).

    Returns:
        The dialog.
    """
    return SpModal.create(
        *children,
        **_given(
            trigger=_as_trigger(trigger, **_common(props)),
            title=title,
            description=description,
            footer=footer,
            closable=closable,
            close_label=close_label,
            width=_length(width),
            label=label,
            dismissible=dismissible,
        ),
        **_open(open, default_open, on_open_change),
        **props,
    )


def sp_drawer(
    *children: Any,
    trigger: Any = None,
    title: Any = None,
    description: Any = None,
    footer: Any = None,
    side: str | None = None,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    closable: bool | None = None,
    close_label: str | None = None,
    size: int | str | None = None,
    modal: bool | None = None,
    extent: int | str | None = None,
    label: str | None = None,
    dismissible: bool | None = None,
    **props: Any,
) -> rx.Component:
    """A panel against one side of the window, on a card frame.

    Args:
        *children: The body.
        trigger: What opens it (see :func:`sp_modal`).
        title: The heading and accessible name.
        description: A line under the title.
        footer: Actions.
        side: ``end`` (default), ``start``, ``top`` or ``bottom``.
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        closable: Draws the close cross (default).
        close_label: Accessible name of the cross.
        size: 0.7.0's name of ``extent``.
        modal: Blocks the page behind (default); ``False`` opens it with ``show()``.
        extent: Width (start/end) or height (top/bottom), px or CSS length.
        label: Accessible name when there is no title.
        dismissible: Escape and a backdrop click close it (default).
        **props: Common props.

    Returns:
        The drawer.
    """
    return SpDrawer.create(
        *children,
        **_given(
            trigger=_as_trigger(trigger, **_common(props)),
            title=title,
            description=description,
            footer=footer,
            side=_logical(side, _SIDES, "side"),
            closable=closable,
            close_label=close_label,
            extent=_length(extent if extent is not None else size),
            modal=modal,
            label=label,
            dismissible=dismissible,
        ),
        **_open(open, default_open, on_open_change),
        **props,
    )


def sp_popover(
    *children: Any,
    trigger: Any,
    title: Any = None,
    side: str | None = None,
    align: Align | None = None,
    side_offset: int | None = None,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    closable: bool | None = None,
    close_label: str | None = None,
    width: int | str | None = None,
    offset: int | None = None,
    label: str | None = None,
    **props: Any,
) -> rx.Component:
    """A card anchored to its trigger; it closes on Escape or a click outside.

    Args:
        *children: The body.
        trigger: What opens it (see :func:`sp_modal`).
        title: A heading that names it.
        side: Preferred side of the trigger: ``bottom`` (default), ``top``, ``start`` or ``end``.
        align: Alignment along that side (``center``).
        side_offset: 0.7.0's name of ``offset``.
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        closable: Draws a close cross.
        close_label: Accessible name of the cross.
        width: Width, px or CSS length (320 px by default).
        offset: Gap to the trigger, px (6).
        label: Accessible name when there is no title.
        **props: Common props.

    Returns:
        The popover.
    """
    return SpPopover.create(
        *children,
        trigger=_as_trigger(trigger, **_common(props)),
        **_given(
            title=title,
            side=_logical(side, _SIDES, "side"),
            align=align,
            offset=offset if offset is not None else side_offset,
            closable=closable,
            close_label=close_label,
            width=_length(width),
            label=label,
        ),
        **_open(open, default_open, on_open_change),
        **props,
    )


def sp_tooltip(
    trigger: Any,
    content: str | rx.Var,
    *,
    side: str | None = None,
    align: Align | None = None,
    side_offset: int | None = None,
    delay: int | None = None,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    offset: int | None = None,
    **props: Any,
) -> rx.Component:
    """A short description of its trigger, shown on hover and on focus; Escape dismisses it.

    Args:
        trigger: The element described (a string becomes :func:`sp_trigger`).
        content: The text (the npm ``text``): the trigger's accessible description.
        side: Preferred side (``top``).
        align: Alignment along that side (``center``).
        side_offset: 0.7.0's name of ``offset``.
        delay: Hover delay before showing, ms (300).
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        offset: Gap, px (6).
        **props: Common props.

    Returns:
        The tooltip.

    Raises:
        TypeError: When ``content`` is a component: a tooltip holds text only.
    """
    if isinstance(content, rx.Component):
        msg = "sp_tooltip's content is text (silverpoint 0.7.0 SpTooltip.text); use sp_popover for markup."
        raise TypeError(msg)
    return SpTooltip.create(
        trigger=_as_trigger(trigger, **_common(props)),
        text=content,
        **_given(
            side=_logical(side, _SIDES, "side"),
            align=align,
            offset=offset if offset is not None else side_offset,
            delay=delay,
        ),
        **_open(open, default_open, on_open_change),
        **props,
    )


def _option(item: Any) -> Any:
    """``{"value", "label", "disabled"}`` (0.7.0) or ``{"key", …}`` → ``UiItem``; a string is its own key."""
    if isinstance(item, str):
        return item
    out = {key: value for key, value in item.items() if key != "value"}
    out.setdefault("key", item.get("value"))
    out.setdefault("label", str(out["key"]))
    return out


def _options(items: Sequence[Any] | rx.Var) -> Any:
    if not isinstance(items, rx.Var):
        return [_option(item) for item in items]
    # A state var of dicts may still name the key ``value``: map it in the browser.
    expression = (
        f"({items}).map((item) => (typeof item === 'string' ? item : "
        "({ ...item, key: item.key ?? item.value, label: item.label ?? String(item.key ?? item.value) })))"
    )
    return rx.Var(_js_expr=expression, _var_type=list, _var_data=items._get_all_var_data())


def sp_select(
    items: Sequence[Any] | rx.Var,
    *,
    value: str | rx.Var | None = None,
    default_value: str | None = None,
    on_change: Any = None,
    placeholder: str | None = None,
    label: str | rx.Var | None = None,
    disabled: bool | rx.Var | None = None,
    name: str | None = None,
    required: bool | None = None,
    width: int | str | None = None,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    **props: Any,
) -> rx.Component:
    """A drawn field that opens a list of options; the chosen one is ticked.

    Args:
        items: ``["a", "b"]`` or ``[{"key", "label", "disabled"}]`` (0.7.0's ``value`` still names
            the key), static or a state var.
        value: The chosen key (controlled).
        default_value: The initial key (uncontrolled).
        on_change: Handler receiving the chosen key.
        placeholder: Shown, in italics, while nothing is chosen (``"Select…"``).
        label: Accessible name of the field; the placeholder when omitted.
        disabled: Disables the field.
        name: Form field name (a hidden input submits the key).
        required: Required in a form.
        width: Width of the field, px or CSS length (180 px by default).
        open: Open state of the list (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        **props: Common props.

    Returns:
        The select.
    """
    return SpSelect.create(
        items=_options(items),
        label=label if label is not None else (placeholder or "Select…"),
        **_given(
            value=value,
            default_value=default_value,
            on_change=on_change,
            placeholder=placeholder,
            disabled=disabled,
            name=name,
            required=required,
            width=_length(width),
        ),
        **_open(open, default_open, on_open_change),
        **props,
    )


def sp_dropdown_menu(
    trigger: Any,
    items: Sequence[dict[str, Any]] | rx.Var,
    *,
    on_select: Any = None,
    side: str | None = None,
    align: Align | None = None,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    label: str | rx.Var | None = None,
    **props: Any,
) -> rx.Component:
    """A menu of commands under a drawn button.

    Items are ``{"key", "label", "shortcut", "disabled", "danger"}``, ``{"type": "separator", "key"}``
    or ``{"type": "label", "key", "label"}``; a static separator or label without a key gets one.

    Args:
        trigger: Its button: a string is the menu's own drawn button with that text (and the menu's
            accessible name); a component is cloned as the trigger.
        items: The commands, static or a state var of dicts.
        on_select: Handler called with the chosen item's ``key``.
        side: Preferred side (``bottom``).
        align: Alignment along that side (``start``).
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        label: The menu's accessible name; the trigger's text when it is a string.
        **props: Common props.

    Returns:
        The menu.
    """
    text_trigger = isinstance(trigger, (str, rx.Var))
    if not isinstance(items, rx.Var):
        # Keys are unique (REQ-325); 0.7.0 let separators and labels go without one.
        items = [
            item if "key" in item else {**item, "key": f"{item.get('type', 'item')}-{index}"}
            for index, item in enumerate(items)
        ]
    if label is None:
        label = trigger if text_trigger else "Menu"
    return SpDropdownMenu.create(
        items=items,
        label=label,
        **_given(
            trigger=None if text_trigger else trigger,
            on_select=on_select,
            side=_logical(side, _SIDES, "side"),
            align=align,
        ),
        **_open(open, default_open, on_open_change),
        **props,
    )


def sp_toast(
    title: Any,
    description: Any = None,
    *,
    kind: ToastKind | None = None,
    action: rx.Component | None = None,
    action_alt: str | None = None,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    duration: int | None = None,
    close_label: str | None = None,
    **props: Any,
) -> rx.Component:
    """A notice; put it in :func:`sp_toaster`. ``error`` and ``warning`` are announced assertively.

    Args:
        title: The notice.
        description: Detail.
        kind: ``info`` (default), ``success``, ``warning`` or ``error`` (its drawn mark).
        action: A button for the notice's action.
        action_alt: 0.7.0 (Radix) only; ignored, with a deprecation warning.
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        duration: Time on screen, ms, at least 1000 (the toaster's by default).
        close_label: Accessible name of the cross.
        **props: Common props.

    Returns:
        The toast.
    """
    if action_alt is not None:
        warnings.warn(
            "sp_toast(action_alt=) is ignored since 0.7.1 (it was Radix's).", DeprecationWarning, stacklevel=2
        )
    return SpToast.create(
        title=title,
        **_given(description=description, kind=kind, action=action, duration=duration, close_label=close_label),
        **_open(open, default_open, on_open_change),
        **props,
    )


def sp_toaster(
    *toasts: rx.Component,
    position: str | None = None,
    duration: int | None = None,
    label: str | None = None,
    **props: Any,
) -> rx.Component:
    """The notification region: where toasts stack. Toasts pause while hovered or focused.

    Args:
        *toasts: The :func:`sp_toast` notices.
        position: ``bottom-end`` (default), ``bottom-start``, ``top-end`` or ``top-start``.
        duration: Default time on screen, ms (5000).
        label: Accessible name of the region (F8 focuses it).
        **props: Common props.

    Returns:
        The toaster.
    """
    return SpToaster.create(
        *toasts,
        **_given(position=_logical(position, _POSITIONS, "position"), duration=duration, label=label),
        **props,
    )
