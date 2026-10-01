"""The UI components of silverpoint 0.3: the 17 ``Sp`` components, drawn as the charts are.

Buttons, inputs, checkboxes, tabs, cards, alerts… with frames hand-drawn by each ground's own
inker and tone laid as hatching (``silverpoint``) or as the weight of an exact white line
(``cyanotype``). Each one is a native control underneath (a ``<button>``, an ``<input>``, a
``<fieldset>`` of radios), so forms submit, the keyboard follows the WAI-ARIA patterns and
``precision`` mode switches the inking off.

The npm side is the ``/ui`` subpath of ``@silverpoint/react``, plus ``@silverpoint/grounds/ui.css``
(the components' stylesheet, opt-in beside ``styles.css``). These wrappers import both.

Value components are controlled (``value``/``checked`` with ``on_change``) or uncontrolled
(``default_value``/``default_checked``). ``on_change`` receives the new value itself, not a DOM
event: a string, a bool or a number.
"""

from typing import Any, ClassVar, Literal

import reflex as rx
from reflex.event import no_args_event_spec

from .base import SILVERPOINT_STYLESHEETS, GroundName, InkMode, Substrate
from .dashboard import _SubpathComponent

#: The components' stylesheet, opt-in beside ``styles.css``.
SILVERPOINT_UI_STYLESHEET = "@silverpoint/grounds/ui.css"

UiSize = Literal["sm", "md", "lg"]
UiVariant = Literal["default", "primary", "danger"]
UiOrientation = Literal["horizontal", "vertical"]
AlertKind = Literal["info", "success", "warning", "error"]
StepStatus = Literal["wait", "process", "finish", "error"]
UiToneLevel = Literal[1, 2, 3, 4]


def _value_spec(value):
    """The new value of a value component.

    Args:
        value: A string (Input, RadioGroup, Segmented, Tabs), a bool (Checkbox, Switch) or a
            number (Slider, Rate). Never the DOM event.

    Returns:
        The value, forwarded unchanged to the backend handler.
    """
    return (value,)


class SilverpointUi(_SubpathComponent):
    """Props every UI component shares (``CommonUiProps``).

    ``class_name`` is added to the component's root element, after its own classes.
    """

    _subpath: ClassVar[str] = "/ui"

    # Style ground: ``"silverpoint"`` or ``"cyanotype"``, or a ground object. Defaults to the
    # dashboard's, then the provider's, or ``silverpoint``.
    ground: rx.Var[GroundName | str | dict[str, Any]]

    # Prepared substrate within the ground.
    substrate: rx.Var[Substrate]

    # ``ink`` by default; ``precision`` disables inking.
    mode: rx.Var[InkMode]

    # Seed of the frame's hand; overrides ``id`` for the frame variant only.
    seed: rx.Var[int | str]

    # Control size: ``sm``, ``md`` (default) or ``lg``.
    size: rx.Var[UiSize]

    def add_imports(self) -> dict[str, list[str]]:
        """Import the typeface, the grounds and the UI stylesheet next to the component.

        Returns:
            Side-effect imports of the three stylesheets.
        """
        return {"": [*SILVERPOINT_STYLESHEETS, SILVERPOINT_UI_STYLESHEET]}


# ── Actions ─────────────────────────────────────────────────────────────────────────────


class SpButton(SilverpointUi):
    """A native ``<button>``, or an ``<a>`` with ``href``. Its children are its text."""

    tag = "SpButton"

    # ``default``, ``primary`` or ``danger`` (which also draws the exact ✕ glyph).
    variant: rx.Var[UiVariant]

    # ``button`` (default), ``submit`` or ``reset``.
    type: rx.Var[Literal["button", "submit", "reset"]]

    # Not focusable, not submitted; drawn with the disabled tone.
    disabled: rx.Var[bool]

    # Accessible name of an icon-only button.
    label: rx.Var[str]

    # Fills the width of its container.
    block: rx.Var[bool]

    # Renders an ``<a>`` to this address.
    href: rx.Var[str]


# ── Data entry ──────────────────────────────────────────────────────────────────────────


class SpInput(SilverpointUi):
    """A native ``<input>`` in a framed box, with an optional message and affixes."""

    tag = "SpInput"

    # Native input type: ``text`` (default), ``search``, ``email``, ``url``, ``tel``, ``password``, ``number``.
    type: rx.Var[Literal["text", "search", "email", "url", "tel", "password", "number"]]

    # Hint shown while empty; not a substitute for the accessible name.
    placeholder: rx.Var[str]

    # Form field name; the native input submits under it.
    name: rx.Var[str]

    # Not focusable and not submitted.
    disabled: rx.Var[bool]

    # Focusable and submitted, but not editable.
    read_only: rx.Var[bool]

    # Sets ``aria-invalid`` and draws the exact ⚠ glyph.
    invalid: rx.Var[bool]

    # Help or error text under the control, referenced by ``aria-describedby``.
    message: rx.Var[str]

    # Accessible name, when no ``<label for>`` names the control.
    label: rx.Var[str]

    # Controlled value.
    value: rx.Var[str]

    # Initial value of an uncontrolled input.
    default_value: rx.Var[str]

    # Content before the text, inside the box.
    prefix: rx.Var[rx.Component]

    # Content after the text, inside the box.
    suffix: rx.Var[rx.Component]

    # The new value (a string), not the DOM event.
    on_change: rx.EventHandler[_value_spec]


class SpCheckbox(SilverpointUi):
    """A native checkbox, hidden for sight, in its ``<label>``."""

    tag = "SpCheckbox"

    # The visible text and accessible name. Required.
    label: rx.Var[str]

    # Form field name; submitted as ``on`` when checked.
    name: rx.Var[str]

    # Not focusable and not submitted.
    disabled: rx.Var[bool]

    # Draws the exact dash and sets the native ``indeterminate`` state.
    indeterminate: rx.Var[bool]

    # Controlled state.
    checked: rx.Var[bool]

    # Initial state of an uncontrolled checkbox.
    default_checked: rx.Var[bool]

    # The new state (a bool).
    on_change: rx.EventHandler[_value_spec]


class SpSwitch(SilverpointUi):
    """A native checkbox with ``role="switch"``."""

    tag = "SpSwitch"

    # The visible text and accessible name. Required.
    label: rx.Var[str]

    # Form field name; submitted as ``on`` when on.
    name: rx.Var[str]

    # Not focusable and not submitted.
    disabled: rx.Var[bool]

    # Controlled state.
    checked: rx.Var[bool]

    # Initial state of an uncontrolled switch.
    default_checked: rx.Var[bool]

    # The new state (a bool).
    on_change: rx.EventHandler[_value_spec]


class SpRadioGroup(SilverpointUi):
    """A ``<fieldset>`` of native radios; the arrows move and select."""

    tag = "SpRadioGroup"

    # The choices, ``[{key, label, disabled?}]``; build them with :func:`ui_item`. Keys are unique.
    items: rx.Var[list[dict[str, Any]]]

    # Form field name the radios submit under. Required.
    name: rx.Var[str]

    # The group's name, its ``<legend>``. Required.
    label: rx.Var[str]

    # ``vertical`` (default) or ``horizontal``.
    orientation: rx.Var[UiOrientation]

    # Controlled key; ``None`` checks none.
    value: rx.Var[str | None]

    # Initial key of an uncontrolled group.
    default_value: rx.Var[str | None]

    # The key checked (a string).
    on_change: rx.EventHandler[_value_spec]


class SpSlider(SilverpointUi):
    """A native range over the exact drawing of its rail, with optional labelled marks."""

    tag = "SpSlider"

    # Accessible name of the range. Required.
    label: rx.Var[str]

    # Lowest value (0 by default).
    min: rx.Var[int | float]

    # Highest value (100 by default).
    max: rx.Var[int | float]

    # Step (1 by default).
    step: rx.Var[int | float]

    # Form field name; the native input submits under it.
    name: rx.Var[str]

    # Not focusable and not submitted.
    disabled: rx.Var[bool]

    # Values on the rail that get a labelled mark.
    marks: rx.Var[list[int | float]]

    # Controlled value.
    value: rx.Var[int | float]

    # Initial value of an uncontrolled slider (``min`` by default).
    default_value: rx.Var[int | float]

    # The new value (a number).
    on_change: rx.EventHandler[_value_spec]


class SpRate(SilverpointUi):
    """Native radios valued 1..count, each an exact lozenge."""

    tag = "SpRate"

    # The group's name, its ``<legend>``. Required.
    label: rx.Var[str]

    # Number of marks, 1..10 (5 by default).
    count: rx.Var[int]

    # Form field name; the native radios submit under it.
    name: rx.Var[str]

    # Not focusable and not submitted.
    disabled: rx.Var[bool]

    # Shows the value; the keyboard and the pointer do not change it.
    read_only: rx.Var[bool]

    # Controlled value.
    value: rx.Var[int]

    # Initial value of an uncontrolled rate (0 by default).
    default_value: rx.Var[int]

    # The new value (a number).
    on_change: rx.EventHandler[_value_spec]


class SpSegmented(SilverpointUi):
    """Native radios in one frame; the arrows move and select."""

    tag = "SpSegmented"

    # The options, ``[{key, label, disabled?}]``; build them with :func:`ui_item`.
    items: rx.Var[list[dict[str, Any]]]

    # The control's name, its ``<legend>``. Required.
    label: rx.Var[str]

    # Form field name; the native radios submit under it.
    name: rx.Var[str]

    # Fills the width of its container.
    block: rx.Var[bool]

    # Controlled key; an unknown one shows the first enabled segment.
    value: rx.Var[str]

    # Initial key of an uncontrolled control.
    default_value: rx.Var[str]

    # The key selected (a string).
    on_change: rx.EventHandler[_value_spec]


# ── Navigation ──────────────────────────────────────────────────────────────────────────


class SpTabs(SilverpointUi):
    """A tablist of native buttons, one tab stop; its children are :class:`SpTabPanel`."""

    tag = "SpTabs"

    # The tabs, ``[{key, label, disabled?}]``; a disabled one is skipped by the arrows.
    items: rx.Var[list[dict[str, Any]]]

    # Accessible name of the tab list.
    label: rx.Var[str]

    # ``horizontal`` (default) or ``vertical``.
    orientation: rx.Var[UiOrientation]

    # ``automatic`` (default): a tab is selected as focus reaches it; ``manual``: on Enter or Space.
    activation: rx.Var[Literal["automatic", "manual"]]

    # Controlled key; an unknown one shows the first enabled tab.
    value: rx.Var[str]

    # Initial key of uncontrolled tabs.
    default_value: rx.Var[str]

    # The key selected (a string).
    on_change: rx.EventHandler[_value_spec]


class SpTabPanel(_SubpathComponent):
    """A ``tabpanel`` labelled by its tab, hidden unless its tab is selected."""

    tag = "SpTabPanel"
    _subpath: ClassVar[str] = "/ui"

    # The key of the tab that shows this panel. Required.
    value: rx.Var[str]


class SpSteps(SilverpointUi):
    """An ordered list of steps; their status is derived from ``current`` unless set."""

    tag = "SpSteps"

    # The steps, ``[{key, title, description?, status?}]``; build them with :func:`step_item`.
    items: rx.Var[list[dict[str, Any]]]

    # The current step, 0-based. Required.
    current: rx.Var[int]

    # ``horizontal`` (default) or ``vertical``.
    orientation: rx.Var[UiOrientation]

    # Accessible name of the list.
    label: rx.Var[str]


# ── Data display ────────────────────────────────────────────────────────────────────────


class SpCard(SilverpointUi):
    """A framed card; its children are its body. Without ``title`` it is a plain container."""

    tag = "SpCard"

    # Heading of the card.
    title: rx.Var[str]

    # Level of the heading, 2 to 6 (3 by default).
    heading_level: rx.Var[Literal[2, 3, 4, 5, 6]]

    # Content at the end of the header, e.g. a period or a tag.
    extra: rx.Var[rx.Component | str]

    # Content of the footer.
    footer: rx.Var[rx.Component | str]


class SpTag(SilverpointUi):
    """A framed, toned label; its children are its text."""

    tag = "SpTag"

    # Tonal level 1 to 4 (1 by default).
    tone: rx.Var[UiToneLevel]

    # Adds a native close button, which fires ``on_close``.
    closable: rx.Var[bool]

    # Accessible name of the close button (``Remove <text>`` by default).
    close_label: rx.Var[str]

    # The close button was clicked.
    on_close: rx.EventHandler[no_args_event_spec]


class SpBadge(SilverpointUi):
    """A count (or a dot) beside its children; the count is text, in the accessible name."""

    tag = "SpBadge"

    # The number shown, up to ``max``.
    count: rx.Var[int]

    # Above it the badge reads ``99+`` (99 by default).
    max: rx.Var[int]

    # A dot with no number.
    dot: rx.Var[bool]

    # Accessible text of the badge, e.g. ``unread messages``.
    label: rx.Var[str]


class SpDivider(SilverpointUi):
    """A rule, optionally with a caption set in it."""

    tag = "SpDivider"

    # ``horizontal`` (default) or ``vertical``.
    orientation: rx.Var[UiOrientation]

    # A caption set in the rule.
    text: rx.Var[str]

    # Where the caption sits: ``start``, ``center`` (default) or ``end``.
    align: rx.Var[Literal["start", "center", "end"]]


# ── Feedback ────────────────────────────────────────────────────────────────────────────


class SpProgress(SilverpointUi):
    """A ``progressbar``, a line or a circle; without ``value``, indeterminate."""

    tag = "SpProgress"

    # 0..100; omitted, the progress is indeterminate.
    value: rx.Var[int | float]

    # ``line`` (default) or ``circle``.
    shape: rx.Var[Literal["line", "circle"]]

    # Accessible name. Required.
    label: rx.Var[str]

    # Prints the value (true by default).
    show_value: rx.Var[bool]


class SpAlert(SilverpointUi):
    """An ``alert`` or a ``status`` by kind; its children are its body."""

    tag = "SpAlert"

    # ``info`` (default), ``success``, ``warning`` or ``error``.
    kind: rx.Var[AlertKind]

    # Bold first line of the alert.
    title: rx.Var[str]

    # Adds a native close button, which fires ``on_close``.
    closable: rx.Var[bool]

    # Accessible name of the close button (``Close`` by default).
    close_label: rx.Var[str]

    # The close button was clicked.
    on_close: rx.EventHandler[no_args_event_spec]


class SpSkeleton(SilverpointUi):
    """A loading placeholder: ``aria-busy``, a hidden label, hidden toned lines."""

    tag = "SpSkeleton"

    # Number of lines, 1..8 (3 by default).
    lines: rx.Var[int]

    # Draws an avatar placeholder before the lines.
    avatar: rx.Var[bool]

    # Accessible label (``Loading`` by default).
    label: rx.Var[str]


# ── Items ───────────────────────────────────────────────────────────────────────────────


def ui_item(key: str, label: str, disabled: bool = False) -> dict[str, Any]:
    """One item of :func:`sp_tabs`, :func:`sp_segmented` or :func:`sp_radio_group`.

    Args:
        key: Its key, unique in the list; the value ``on_change`` reports.
        label: Its visible text.
        disabled: Skipped by the arrows, not selectable.

    Returns:
        The item.
    """
    item: dict[str, Any] = {"key": key, "label": label}
    if disabled:
        item["disabled"] = True
    return item


def step_item(key: str, title: str, description: str | None = None, status: StepStatus | None = None) -> dict[str, Any]:
    """One step of :func:`sp_steps`.

    Args:
        key: Its key, unique in the list.
        title: Its title.
        description: A line under the title.
        status: ``wait``, ``process``, ``finish`` or ``error``; derived from ``current`` when
            omitted (``error`` must be explicit).

    Returns:
        The step.
    """
    item: dict[str, Any] = {"key": key, "title": title}
    if description is not None:
        item["description"] = description
    if status is not None:
        item["status"] = status
    return item


sp_button = SpButton.create
sp_input = SpInput.create
sp_checkbox = SpCheckbox.create
sp_switch = SpSwitch.create
sp_radio_group = SpRadioGroup.create
sp_slider = SpSlider.create
sp_rate = SpRate.create
sp_segmented = SpSegmented.create
sp_tabs = SpTabs.create
sp_tab_panel = SpTabPanel.create
sp_steps = SpSteps.create
sp_card = SpCard.create
sp_tag = SpTag.create
sp_badge = SpBadge.create
sp_divider = SpDivider.create
sp_progress = SpProgress.create
sp_alert = SpAlert.create
sp_skeleton = SpSkeleton.create
