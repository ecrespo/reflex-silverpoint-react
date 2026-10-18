"""Reflex-composed components, level B: overlays on Radix primitives, drawn on silverpoint surfaces.

Modal, drawer, popover, tooltip, select, dropdown menu and toast. Behaviour — focus trapping,
keyboard, dismissal, positioning, ARIA — is Radix's (the unstyled ``@radix-ui/react-*`` primitives,
at the versions Reflex itself already installs). Drawing is silverpoint's: each overlay's content is
an :class:`~.surfaces.SpSurface` with the ground's hand-inked frame; the highlighted option of a
list is heightened, as the current item of an Sp component is.

Overlays render in a portal at the end of ``<body>``, outside any ``silverpoint_palette`` section:
give them ``ground``, ``substrate``, ``mode`` and ``palette`` directly. Like the level A
components they are Reflex-only (not in silverpoint's React/Vue/Angular parity contract).
"""

from collections.abc import Sequence
from typing import Any, Literal

import reflex as rx
from reflex.event import no_args_event_spec, passthrough_event_spec

from .surfaces import sp_glyph, sp_surface

Side = Literal["top", "right", "bottom", "left"]
Align = Literal["start", "center", "end"]
ToastKind = Literal["info", "success", "warning", "error"]
ToastPosition = Literal["bottom-right", "bottom-left", "top-right", "top-left"]

_SURFACE_KEYS = ("ground", "substrate", "mode", "size", "seed", "palette", "class_name", "style")

#: Radix primitive versions: the ones ``@radix-ui/themes`` (installed by Reflex) already pulls in,
#: so the frontend keeps one copy of each.
RADIX_VERSIONS = {
    "dialog": "1.1.23",
    "popover": "1.1.23",
    "tooltip": "1.2.16",
    "select": "2.3.7",
    "dropdown-menu": "2.1.24",
    "toast": "1.2.23",
}


def _surface_props(props: dict[str, Any]) -> dict[str, Any]:
    return {key: props.pop(key) for key in _SURFACE_KEYS if key in props}


# ── Radix primitives ────────────────────────────────────────────────────────────────────


class _Radix(rx.Component):
    """A part of a Radix primitive, imported under a unique alias."""

    # Merge props onto the child instead of rendering an element of its own.
    as_child: rx.Var[bool]


def _radix(package: str, part: str, doc: str, **fields: Any) -> type[_Radix]:
    namespace = {
        "__doc__": doc,
        "__module__": __name__,
        "library": f"@radix-ui/react-{package}@{RADIX_VERSIONS[package]}",
        "tag": part,
        "alias": "SpRadix" + "".join(w.capitalize() for w in package.split("-")) + part,
        "__annotations__": fields,
    }
    return type(f"Radix{''.join(w.capitalize() for w in package.split('-'))}{part}", (_Radix,), namespace)


_open_spec = passthrough_event_spec(bool)
_value_spec = passthrough_event_spec(str)

# Dialog (modal and drawer)
DialogRoot = _radix(
    "dialog",
    "Root",
    "Dialog root.",
    open=rx.Var[bool],
    default_open=rx.Var[bool],
    modal=rx.Var[bool],
    on_open_change=rx.EventHandler[_open_spec],
)
DialogTrigger = _radix("dialog", "Trigger", "Opens the dialog.")
DialogPortal = _radix("dialog", "Portal", "Renders the dialog at the end of body.")
DialogOverlay = _radix("dialog", "Overlay", "The backdrop.")
DialogContent = _radix(
    "dialog",
    "Content",
    "The dialog box.",
    on_escape_key_down=rx.EventHandler[no_args_event_spec],
    on_pointer_down_outside=rx.EventHandler[no_args_event_spec],
)
DialogTitle = _radix("dialog", "Title", "The dialog's accessible name.")
DialogDescription = _radix("dialog", "Description", "The dialog's accessible description.")
DialogClose = _radix("dialog", "Close", "Closes the dialog.")

# Popover
PopoverRoot = _radix(
    "popover",
    "Root",
    "Popover root.",
    open=rx.Var[bool],
    default_open=rx.Var[bool],
    modal=rx.Var[bool],
    on_open_change=rx.EventHandler[_open_spec],
)
PopoverTrigger = _radix("popover", "Trigger", "Opens the popover.")
PopoverPortal = _radix("popover", "Portal", "Renders the popover at the end of body.")
PopoverContent = _radix(
    "popover",
    "Content",
    "The popover box.",
    side=rx.Var[str],
    align=rx.Var[str],
    side_offset=rx.Var[int],
    collision_padding=rx.Var[int],
)
PopoverClose = _radix("popover", "Close", "Closes the popover.")

# Tooltip
TooltipProvider = _radix("tooltip", "Provider", "Tooltip timing.", delay_duration=rx.Var[int])
TooltipRoot = _radix(
    "tooltip",
    "Root",
    "Tooltip root.",
    open=rx.Var[bool],
    default_open=rx.Var[bool],
    delay_duration=rx.Var[int],
    on_open_change=rx.EventHandler[_open_spec],
)
TooltipTrigger = _radix("tooltip", "Trigger", "The element described.")
TooltipPortal = _radix("tooltip", "Portal", "Renders the tooltip at the end of body.")
TooltipContent = _radix(
    "tooltip", "Content", "The tooltip.", side=rx.Var[str], align=rx.Var[str], side_offset=rx.Var[int]
)

# Select
SelectRoot = _radix(
    "select",
    "Root",
    "Select root.",
    value=rx.Var[str],
    default_value=rx.Var[str],
    open=rx.Var[bool],
    disabled=rx.Var[bool],
    required=rx.Var[bool],
    name=rx.Var[str],
    on_value_change=rx.EventHandler[_value_spec],
    on_open_change=rx.EventHandler[_open_spec],
)
SelectTrigger = _radix("select", "Trigger", "The field.")
SelectValue = _radix("select", "Value", "The chosen option's text.", placeholder=rx.Var[str])
SelectIcon = _radix("select", "Icon", "The field's chevron.")
SelectPortal = _radix("select", "Portal", "Renders the list at the end of body.")
SelectContent = _radix(
    "select", "Content", "The list.", position=rx.Var[str], side_offset=rx.Var[int], side=rx.Var[str]
)
SelectViewport = _radix("select", "Viewport", "The scrolling part of the list.")
SelectItem = _radix("select", "Item", "An option.", value=rx.Var[str], disabled=rx.Var[bool], text_value=rx.Var[str])
SelectItemText = _radix("select", "ItemText", "The option's text.")
SelectItemIndicator = _radix("select", "ItemIndicator", "Shown on the chosen option.")

# Dropdown menu
MenuRoot = _radix(
    "dropdown-menu",
    "Root",
    "Menu root.",
    open=rx.Var[bool],
    default_open=rx.Var[bool],
    modal=rx.Var[bool],
    on_open_change=rx.EventHandler[_open_spec],
)
MenuTrigger = _radix("dropdown-menu", "Trigger", "Opens the menu.")
MenuPortal = _radix("dropdown-menu", "Portal", "Renders the menu at the end of body.")
MenuContent = _radix(
    "dropdown-menu", "Content", "The menu.", side=rx.Var[str], align=rx.Var[str], side_offset=rx.Var[int]
)
MenuItem = _radix(
    "dropdown-menu",
    "Item",
    "A command.",
    disabled=rx.Var[bool],
    text_value=rx.Var[str],
    on_select=rx.EventHandler[no_args_event_spec],
)
MenuLabel = _radix("dropdown-menu", "Label", "A group heading.")
MenuSeparator = _radix("dropdown-menu", "Separator", "A rule between groups.")

# Toast
ToastProvider = _radix(
    "toast", "Provider", "Toast timing.", duration=rx.Var[int], swipe_direction=rx.Var[str], label=rx.Var[str]
)
ToastViewport = _radix("toast", "Viewport", "Where toasts stack.", label=rx.Var[str])
ToastRoot = _radix(
    "toast",
    "Root",
    "A toast.",
    open=rx.Var[bool],
    default_open=rx.Var[bool],
    duration=rx.Var[int],
    type=rx.Var[str],
    on_open_change=rx.EventHandler[_open_spec],
)
ToastTitle = _radix("toast", "Title", "The toast's title.")
ToastDescription = _radix("toast", "Description", "The toast's text.")
ToastAction = _radix("toast", "Action", "The toast's action.", alt_text=rx.Var[str])
ToastClose = _radix("toast", "Close", "Dismisses the toast.")


# ── Shared pieces ───────────────────────────────────────────────────────────────────────


def sp_trigger(
    label: str | rx.Var | rx.Component,
    *,
    variant: Literal["default", "primary", "danger"] = "default",
    chevron: bool = False,
    **props: Any,
) -> rx.Component:
    """A drawn button for opening an overlay: the ``SpButton`` look on a surface.

    Unlike :func:`sp_button` (which does not forward Radix's props), it can be an overlay's
    trigger. Strings passed as ``trigger=`` become one of these.

    Args:
        label: Its text (or a component).
        variant: ``default``, ``primary`` (light hatching) or ``danger``.
        chevron: Draws a down chevron after the text.
        **props: Surface props and event triggers.

    Returns:
        The button.
    """
    tone = {"primary": "primary", "danger": "danger"}.get(variant)
    return sp_surface(
        rx.el.span(label, class_name="sp-ui-label sp-ui-plate"),
        *([sp_glyph(glyph="chevronDown")] if chevron else []),
        element="button",
        name="button",
        frame="control",
        tone=tone,
        type="button",
        **props,
    )


def _as_trigger(trigger: Any) -> rx.Component:
    return sp_trigger(trigger) if isinstance(trigger, (str, rx.Var)) else trigger


def _close_button(close: type[_Radix], label: str) -> rx.Component:
    return close.create(
        rx.el.button(sp_glyph(glyph="cross"), type="button", class_name="sp-ui-icon-button", aria_label=label),
        as_child=True,
    )


def _header(title: Any, closable: bool, close: type[_Radix], title_part: type[_Radix], close_label: str) -> list[Any]:
    if title is None and not closable:
        return []
    return [
        rx.el.div(
            title_part.create(rx.el.h2(title, class_name="sp-ui-overlay-title"), as_child=True)
            if title is not None
            else rx.el.span(),
            *([_close_button(close, close_label)] if closable else []),
            class_name="sp-ui-overlay-header",
        ),
        rx.el.span(class_name="sp-ui-overlay-rule", aria_hidden="true"),
    ]


def _open_props(open: Any, default_open: Any, on_open_change: Any) -> dict[str, Any]:
    props = {"open": open, "default_open": default_open, "on_open_change": on_open_change}
    return {key: value for key, value in props.items() if value is not None}


# ── Modal and drawer ────────────────────────────────────────────────────────────────────


def _dialog(
    name: str,
    children: tuple[Any, ...],
    *,
    trigger: Any,
    title: Any,
    description: Any,
    footer: Any,
    open: Any,
    default_open: Any,
    on_open_change: Any,
    closable: bool,
    close_label: str,
    modal: bool,
    extra_attrs: dict[str, Any],
    style: dict[str, Any],
    surface: dict[str, Any],
    props: dict[str, Any],
) -> rx.Component:
    surface_style = surface.pop("style", None)
    content = sp_surface(
        *_header(title, closable, DialogClose, DialogTitle, close_label),
        *(
            [DialogDescription.create(rx.el.p(description, class_name="sp-ui-overlay-description"), as_child=True)]
            if description is not None
            else []
        ),
        rx.el.div(*children, class_name="sp-ui-overlay-body"),
        *([rx.el.div(footer, class_name="sp-ui-overlay-footer")] if footer is not None else []),
        name=name,
        frame="card",
        custom_attrs=extra_attrs,
        style=[style, surface_style] if surface_style is not None else style,
        **surface,
        **props,
    )
    backdrop_surface = {k: v for k, v in surface.items() if k in ("ground", "substrate", "mode", "palette")}
    parts: list[Any] = []
    if trigger is not None:
        parts.append(DialogTrigger.create(_as_trigger(trigger), as_child=True))
    parts.append(
        DialogPortal.create(
            DialogOverlay.create(sp_surface(name="backdrop", tone=1, **backdrop_surface), as_child=True),
            DialogContent.create(content, as_child=True),
        )
    )
    return DialogRoot.create(*parts, modal=modal, **_open_props(open, default_open, on_open_change))


def sp_modal(
    *children: Any,
    trigger: Any = None,
    title: Any = None,
    description: Any = None,
    footer: Any = None,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    closable: bool = True,
    close_label: str = "Close",
    width: int | str | None = None,
    **props: Any,
) -> rx.Component:
    """A modal dialog on a card frame, over a hatched backdrop. Focus is trapped while it is open.

    Controlled with ``open`` + ``on_open_change``, or uncontrolled with a ``trigger``.

    Args:
        *children: The body.
        trigger: What opens it: a string (becomes :func:`sp_trigger`) or a component that forwards
            its props (``rx.el.button``, :func:`sp_trigger`).
        title: The heading and accessible name.
        description: A line under the title (the accessible description).
        footer: Actions, aligned to the end.
        open: Open state (controlled).
        default_open: Initial open state (uncontrolled).
        on_open_change: Handler receiving the new open state.
        closable: Draws the close cross.
        close_label: Accessible name of the cross.
        width: Width (px or CSS length); 520 px by default.
        **props: Surface props (``ground``, ``substrate``, ``mode``, ``palette``…).

    Returns:
        The dialog.
    """
    surface = _surface_props(props)
    style = {"--sp-modal-width": f"{width}px" if isinstance(width, int) else width} if width is not None else {}
    return _dialog(
        "modal",
        children,
        trigger=trigger,
        title=title,
        description=description,
        footer=footer,
        open=open,
        default_open=default_open,
        on_open_change=on_open_change,
        closable=closable,
        close_label=close_label,
        modal=True,
        extra_attrs={},
        style=style,
        surface=surface,
        props=props,
    )


def sp_drawer(
    *children: Any,
    trigger: Any = None,
    title: Any = None,
    description: Any = None,
    footer: Any = None,
    side: Side = "right",
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    closable: bool = True,
    close_label: str = "Close",
    size: int | str | None = None,
    modal: bool = True,
    **props: Any,
) -> rx.Component:
    """A panel that slides from an edge of the window, on a card frame.

    Args:
        *children: The body.
        trigger: What opens it (see :func:`sp_modal`).
        title: The heading and accessible name.
        description: A line under the title.
        footer: Actions.
        side: ``right`` (default), ``left``, ``top`` or ``bottom``.
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        closable: Draws the close cross.
        close_label: Accessible name of the cross.
        size: Width (left/right) or height (top/bottom), px or CSS length.
        modal: Traps focus and blocks the page behind (default).
        **props: Surface props.

    Returns:
        The drawer.
    """
    surface = _surface_props(props)
    style = {"--sp-drawer-size": f"{size}px" if isinstance(size, int) else size} if size is not None else {}
    return _dialog(
        "drawer",
        children,
        trigger=trigger,
        title=title,
        description=description,
        footer=footer,
        open=open,
        default_open=default_open,
        on_open_change=on_open_change,
        closable=closable,
        close_label=close_label,
        modal=modal,
        extra_attrs={"data-side": side},
        style=style,
        surface=surface,
        props=props,
    )


# ── Popover and tooltip ─────────────────────────────────────────────────────────────────


def sp_popover(
    *children: Any,
    trigger: Any,
    title: Any = None,
    side: Side = "bottom",
    align: Align = "center",
    side_offset: int = 6,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    closable: bool = False,
    close_label: str = "Close",
    width: int | None = None,
    **props: Any,
) -> rx.Component:
    """Rich content anchored to a trigger, on a card frame; dismissed by Escape or a click outside.

    Args:
        *children: The content.
        trigger: What opens it (see :func:`sp_modal`).
        title: A heading.
        side: Preferred side of the trigger.
        align: Alignment along that side.
        side_offset: Gap to the trigger, px.
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        closable: Draws a close cross.
        close_label: Accessible name of the cross.
        width: Maximum width, px (320 by default).
        **props: Surface props.

    Returns:
        The popover.
    """
    surface = _surface_props(props)
    style = {"--sp-popover-width": f"{width}px"} if width else {}
    extra_style = surface.pop("style", None)
    content = sp_surface(
        *(_header(title, closable, PopoverClose, _NoPart, close_label) if (title is not None or closable) else []),
        *children,
        name="popover",
        frame="card",
        style=[style, extra_style] if extra_style is not None else style,
        **surface,
        **props,
    )
    return PopoverRoot.create(
        PopoverTrigger.create(_as_trigger(trigger), as_child=True),
        PopoverPortal.create(
            PopoverContent.create(
                content, as_child=True, side=side, align=align, side_offset=side_offset, collision_padding=8
            )
        ),
        **_open_props(open, default_open, on_open_change),
    )


class _NoPart:
    """Stands in for a Radix part that a component does not have (a popover has no Title)."""

    @staticmethod
    def create(child: Any, **_: Any) -> Any:
        return child


def sp_tooltip(
    trigger: Any,
    content: Any,
    *,
    side: Side = "top",
    align: Align = "center",
    side_offset: int = 6,
    delay: int = 300,
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    **props: Any,
) -> rx.Component:
    """A short label shown on hover or keyboard focus, on a drawn box frame.

    Args:
        trigger: The element described (a string becomes :func:`sp_trigger`).
        content: The text.
        side: Preferred side.
        align: Alignment along that side.
        side_offset: Gap, px.
        delay: Hover delay before showing, ms.
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        **props: Surface props.

    Returns:
        The tooltip.
    """
    surface = _surface_props(props)
    box = sp_surface(content, name="tooltip", frame="control", size="sm", **surface, **props)
    return TooltipProvider.create(
        TooltipRoot.create(
            TooltipTrigger.create(_as_trigger(trigger), as_child=True),
            TooltipPortal.create(
                TooltipContent.create(box, as_child=True, side=side, align=align, side_offset=side_offset)
            ),
            **_open_props(open, default_open, on_open_change),
        ),
        delay_duration=delay,
    )


# ── Select and dropdown menu ────────────────────────────────────────────────────────────


def _option(item: Any) -> dict[str, Any]:
    if isinstance(item, str):
        return {"value": item, "label": item}
    return {"label": item.get("value"), **item}


def sp_select(
    items: Sequence[Any] | rx.Var,
    *,
    value: str | rx.Var | None = None,
    default_value: str | None = None,
    on_change: Any = None,
    placeholder: str = "Select…",
    label: str | rx.Var | None = None,
    disabled: bool | rx.Var = False,
    name: str | None = None,
    required: bool = False,
    width: int | None = None,
    **props: Any,
) -> rx.Component:
    """A single-choice list with full keyboard support, drawn as a control frame and a card list.

    ``on_change`` receives the chosen value (a string). The chosen option carries a drawn tick; the
    highlighted one is heightened.

    Args:
        items: ``["a", "b"]`` or ``[{"value", "label", "disabled"}]``, static or a state var of dicts.
        value: The chosen value (controlled).
        default_value: The initial value (uncontrolled).
        on_change: Handler receiving the new value.
        placeholder: Shown, in italics, while nothing is chosen.
        label: Accessible name of the field.
        disabled: Disables the field.
        name: Form field name (a hidden native select is submitted).
        required: Required in a form.
        width: Minimum width of the field, px (180 by default).
        **props: Surface props, applied to the field and the list.

    Returns:
        The select.
    """
    surface = _surface_props(props)
    list_surface = {k: v for k, v in surface.items() if k in ("ground", "substrate", "mode", "palette", "seed")}

    def option(item: Any) -> rx.Component:
        entry = item if isinstance(item, rx.Var) else _option(item)
        return SelectItem.create(
            SelectItemIndicator.create(sp_glyph(glyph="tick"), class_name="sp-ui-option-indicator"),
            SelectItemText.create(entry["label"]),
            value=entry["value"],
            disabled=entry["disabled"].to(bool) if isinstance(entry, rx.Var) else entry.get("disabled", False),
            class_name="sp-ui-option",
        )

    options = rx.foreach(items, option) if isinstance(items, rx.Var) else [option(item) for item in items]
    style = {"--sp-select-width": f"{width}px"} if width else None
    field = sp_trigger(
        SelectValue.create(placeholder=placeholder, class_name="sp-ui-select-value"),
        chevron=True,
        class_name="sp-ui-select-trigger",
        aria_label=label,
        disabled=disabled,
        **({"style": style} if style else {}),
        **{k: v for k, v in surface.items() if k not in ("class_name", "style")},
    )
    root_props: dict[str, Any] = {"disabled": disabled, "required": required}
    if value is not None:
        root_props["value"] = value
    if default_value is not None:
        root_props["default_value"] = default_value
    if on_change is not None:
        root_props["on_value_change"] = on_change
    if name is not None:
        root_props["name"] = name
    return rx.el.span(
        SelectRoot.create(
            SelectTrigger.create(field, as_child=True),
            SelectPortal.create(
                SelectContent.create(
                    sp_surface(
                        SelectViewport.create(*options)
                        if isinstance(options, list)
                        else SelectViewport.create(options),
                        name="select-content",
                        frame="card",
                        **list_surface,
                    ),
                    as_child=True,
                    position="popper",
                    side_offset=4,
                )
            ),
            **root_props,
        ),
        class_name=" ".join(filter(None, ["sp-select", surface.get("class_name")])),
        **props,
    )


def sp_dropdown_menu(
    trigger: Any,
    items: Sequence[dict[str, Any]] | rx.Var,
    *,
    on_select: Any = None,
    side: Side = "bottom",
    align: Align = "start",
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    **props: Any,
) -> rx.Component:
    """A menu of commands opened from a trigger; full keyboard support, typeahead, heightened focus.

    Items are ``{"key", "label", "shortcut", "disabled", "danger"}``; in a static list,
    ``{"type": "separator"}`` draws a rule and ``{"type": "label", "label": …}`` a group heading.

    Args:
        trigger: What opens it (a string becomes :func:`sp_trigger` with a chevron).
        items: The commands, static or a state var of dicts.
        on_select: Handler called with the chosen item's ``key``.
        side: Preferred side.
        align: Alignment along that side.
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        **props: Surface props.

    Returns:
        The menu.
    """
    surface = _surface_props(props)

    def entry(item: Any) -> rx.Component:
        if isinstance(item, dict) and item.get("type") == "separator":
            return MenuSeparator.create(class_name="sp-ui-menu-separator")
        if isinstance(item, dict) and item.get("type") == "label":
            return MenuLabel.create(item["label"], class_name="sp-ui-menu-label")
        key = item["key"]
        item_props: dict[str, Any] = {"class_name": "sp-ui-menu-item"}
        if isinstance(item, rx.Var):
            item_props["disabled"] = item["disabled"].to(bool)
            item_props["custom_attrs"] = {"data-danger": rx.cond(item["danger"].to(bool), "true", "false")}
            shortcut = rx.cond(
                item["shortcut"], rx.el.span(item["shortcut"], class_name="sp-ui-shortcut"), rx.fragment()
            )
        else:
            item_props["disabled"] = item.get("disabled", False)
            item_props["custom_attrs"] = {"data-danger": "true" if item.get("danger") else "false"}
            shortcut = (
                rx.el.span(item["shortcut"], class_name="sp-ui-shortcut") if item.get("shortcut") else rx.fragment()
            )
        if on_select is not None:
            item_props["on_select"] = on_select(key)
        return MenuItem.create(item["label"], shortcut, **item_props)

    entries = rx.foreach(items, entry) if isinstance(items, rx.Var) else [entry(item) for item in items]
    content = sp_surface(
        *(entries if isinstance(entries, list) else [entries]),
        name="menu",
        frame="card",
        **surface,
        **props,
    )
    return MenuRoot.create(
        MenuTrigger.create(
            sp_trigger(trigger, chevron=True) if isinstance(trigger, (str, rx.Var)) else trigger, as_child=True
        ),
        MenuPortal.create(MenuContent.create(content, as_child=True, side=side, align=align, side_offset=6)),
        **_open_props(open, default_open, on_open_change),
    )


# ── Toast ───────────────────────────────────────────────────────────────────────────────

_TOAST_GLYPHS = {"info": "info", "success": "tick", "warning": "warning", "error": "cross"}


def sp_toast(
    title: Any,
    description: Any = None,
    *,
    kind: ToastKind = "info",
    action: rx.Component | None = None,
    action_alt: str = "",
    open: bool | rx.Var | None = None,
    default_open: bool | None = None,
    on_open_change: Any = None,
    duration: int | None = None,
    close_label: str = "Dismiss",
    **props: Any,
) -> rx.Component:
    """A brief notice that stacks in the corner and dismisses itself; place it inside :func:`sp_toaster`.

    Show it by setting ``open`` from state; it calls ``on_open_change(False)`` when it closes
    (timeout, swipe, the cross or Escape).

    Args:
        title: The notice.
        description: Detail.
        kind: ``info``, ``success``, ``warning`` or ``error`` (its drawn mark; ``error`` and
            ``warning`` are announced assertively).
        action: A button for the notice's action.
        action_alt: How to perform the action without the toast (required by Radix for ``action``).
        open: Open state (controlled).
        default_open: Initial open state.
        on_open_change: Handler receiving the new open state.
        duration: Time on screen, ms (the toaster's by default).
        close_label: Accessible name of the cross.
        **props: Surface props.

    Returns:
        The toast.
    """
    surface = _surface_props(props)
    body = sp_surface(
        sp_glyph(glyph=_TOAST_GLYPHS[kind]),
        ToastTitle.create(rx.el.p(title, class_name="sp-ui-toast-title"), as_child=True),
        ToastClose.create(
            rx.el.button(
                sp_glyph(glyph="cross"), type="button", class_name="sp-ui-icon-button", aria_label=close_label
            ),
            as_child=True,
        ),
        *(
            [ToastDescription.create(rx.el.p(description, class_name="sp-ui-toast-description"), as_child=True)]
            if description is not None
            else []
        ),
        *(
            [
                ToastAction.create(
                    rx.el.div(action, class_name="sp-ui-toast-action"), as_child=True, alt_text=action_alt or "Action"
                )
            ]
            if action is not None
            else []
        ),
        element="li",
        name="toast",
        frame="card",
        custom_attrs={"data-kind": kind},
        **surface,
        **props,
    )
    root_props = _open_props(open, default_open, on_open_change)
    if duration is not None:
        root_props["duration"] = duration
    root_props["type"] = "foreground" if kind in ("error", "warning") else "background"
    return ToastRoot.create(body, as_child=True, **root_props)


def sp_toaster(
    *toasts: rx.Component,
    position: ToastPosition = "bottom-right",
    duration: int = 5000,
    label: str = "Notifications",
) -> rx.Component:
    """The place toasts stack: wrap every :func:`sp_toast` of the page in one toaster.

    Args:
        *toasts: The toasts.
        position: Corner of the window.
        duration: Default time on screen, ms.
        label: Accessible name of the notification region (F8 focuses it).

    Returns:
        The toaster.
    """
    swipe = "right" if position.endswith("right") else "left"
    return ToastProvider.create(
        *toasts,
        ToastViewport.create(class_name="sp-toast-viewport", custom_attrs={"data-position": position}, label=label),
        duration=duration,
        swipe_direction=swipe,
        label=label,
    )
