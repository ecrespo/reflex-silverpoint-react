"""The composed components of silverpoint 0.7: table, pagination, breadcrumb, avatar, statistic,
descriptions, a vertical timeline, collapse, empty and result states, textarea and number input.

Each one is ``@silverpoint/react``'s own component (``/ui`` subpath, beside the ``Sp`` components):
native markup (a ``<table>``, ``<details>``, ``<textarea>``…) drawn by the core with the ground's
frames, tones and heightening, under silverpoint's parity contract. They read
``silverpoint_provider`` (ground, substrate, mode, locale, palette) as every ``Sp`` component does.

The builders keep the 0.7.0 signatures: positional ``columns``/``data``, ``items`` and ``title``,
static lists or state vars, and every common prop (``ground``, ``substrate``, ``mode``, ``size``,
``seed``, ``palette``, ``id``, ``class_name``, ``style``) as a keyword.
"""

from collections.abc import Sequence
from typing import Any, Literal

import reflex as rx
from reflex.event import passthrough_event_spec

from .surfaces import SpInputNumber, SpPagination, _renamed
from .ui import SilverpointUi

Status = Literal["done", "current", "pending", "error"]
ResultStatus = Literal["success", "info", "warning", "error"]
Align = Literal["start", "center", "end"]
HeadingLevel = Literal[2, 3, 4, 5, 6]

_key_spec = passthrough_event_spec(str)
_open_spec = passthrough_event_spec(bool)
_text_spec = passthrough_event_spec(str)


def _given(**props: Any) -> dict[str, Any]:
    """The arguments that were given: ``None`` leaves the npm default."""
    return {key: value for key, value in props.items() if value is not None}


def _length(value: Any) -> Any:
    """``120`` → ``"120px"``; strings and vars unchanged."""
    return f"{value}px" if isinstance(value, (int, float)) and not isinstance(value, bool) else value


def _slot(children: tuple[Any, ...]) -> Any:
    """Several children as one component prop."""
    if not children:
        return None
    return children[0] if len(children) == 1 else rx.fragment(*children)


# ── Components ──────────────────────────────────────────────────────────────────────────


class SpTable(SilverpointUi):
    """A data table on a card frame: small-caps header, tabular figures, hatched striping."""

    tag = "SpTable"

    # ``[{"key", "title", "align", "sortable", "width"}]``.
    columns: rx.Var[list[dict[str, Any]]]

    # The rows, drawn as given: sort them yourself (see :func:`sort_rows`).
    data: rx.Var[list[dict[str, Any]]]

    # The table's caption, its accessible name.
    caption: rx.Var[str]

    # The column currently sorted, and its order (``asc`` by default).
    sort_key: rx.Var[str]
    sort_order: rx.Var[Literal["asc", "desc"]]

    # Hatches every other row (``False``), the row under the pointer (``True``); draws the card frame (``True``).
    striped: rx.Var[bool]
    hoverable: rx.Var[bool]
    bordered: rx.Var[bool]

    # Shown when there are no rows (``"No data"``).
    empty_text: rx.Var[str]

    # The column whose value keys each row.
    row_key: rx.Var[str]

    # A sortable header was used: the column's key.
    on_sort: rx.EventHandler[_key_spec]


class SpBreadcrumb(SilverpointUi):
    """Where the page sits: links separated by hairline slashes; the last item is the current page."""

    tag = "SpBreadcrumb"

    # ``[{"key", "label", "href"}]``.
    items: rx.Var[list[dict[str, Any]]]

    # Accessible name of the landmark (``"Breadcrumb"``).
    label: rx.Var[str]


class SpAvatar(SilverpointUi):
    """A portrait in a drawn round (or square) frame, or the person's initials."""

    tag = "SpAvatar"

    src: rx.Var[str]
    name: rx.Var[str]
    initials: rx.Var[str]
    alt: rx.Var[str]
    shape: rx.Var[Literal["circle", "square"]]
    pixel_size: rx.Var[int]


class SpAvatarGroup(SilverpointUi):
    """Overlapping avatars."""

    tag = "SpAvatarGroup"

    label: rx.Var[str]


class SpStatistic(SilverpointUi):
    """A figure with its title: small-caps label, large tabular number, optional trend."""

    tag = "SpStatistic"

    title: rx.Var[str]
    value: rx.Var[str | int | float]
    prefix: rx.Var[str]
    suffix: rx.Var[str]
    trend: rx.Var[Literal["up", "down"]]
    delta: rx.Var[str]


class SpDescriptions(SilverpointUi):
    """Label–value pairs in a grid (a ``<dl>``), optionally on a card frame."""

    tag = "SpDescriptions"

    items: rx.Var[list[dict[str, Any]]]
    title: rx.Var[str]
    columns: rx.Var[int]
    bordered: rx.Var[bool]
    heading_level: rx.Var[HeadingLevel]


class SpTimelineList(SilverpointUi):
    """A vertical timeline: a drawn mark per event on a hairline, time, title and description."""

    tag = "SpTimelineList"

    items: rx.Var[list[dict[str, Any]]]
    label: rx.Var[str]


class SpCollapse(SilverpointUi):
    """Panels that open and close, on a card frame; native ``<details>``."""

    tag = "SpCollapse"

    accordion: rx.Var[bool]
    bordered: rx.Var[bool]


class SpCollapseItem(SilverpointUi):
    """One panel of :class:`SpCollapse`: a native ``<details>``."""

    tag = "SpCollapseItem"

    title: rx.Var[str]
    disabled: rx.Var[bool]
    open: rx.Var[bool]
    default_open: rx.Var[bool]

    # The panel opened or closed: the new state.
    on_toggle: rx.EventHandler[_open_spec]


class SpEmpty(SilverpointUi):
    """The empty state: a lightly hatched, drawn tray and a line of italic text."""

    tag = "SpEmpty"

    description: rx.Var[str]

    # Actions under the text.
    extra: rx.Var[rx.Component]


class SpResult(SilverpointUi):
    """The outcome of an operation: a drawn round mark, title and subtitle."""

    tag = "SpResult"

    status: rx.Var[ResultStatus]
    title: rx.Var[str]
    subtitle: rx.Var[str]
    heading_level: rx.Var[HeadingLevel]

    # Actions under the text.
    extra: rx.Var[rx.Component]


class SpTextarea(SilverpointUi):
    """A multi-line text field on the ``SpInput`` contract: drawn frame, italic placeholder, message."""

    tag = "SpTextarea"

    value: rx.Var[str]
    default_value: rx.Var[str]
    rows: rx.Var[int]
    placeholder: rx.Var[str]
    label: rx.Var[str]
    message: rx.Var[str]
    invalid: rx.Var[bool]
    disabled: rx.Var[bool]
    read_only: rx.Var[bool]
    max_length: rx.Var[int]
    show_count: rx.Var[bool]
    name: rx.Var[str]

    # The text changed: the new text, not a DOM event.
    on_change: rx.EventHandler[_text_spec]


# ── Builders ────────────────────────────────────────────────────────────────────────────


def _column(column: dict[str, Any] | str) -> dict[str, Any]:
    if isinstance(column, str):
        return {"key": column}
    out = dict(column)
    if "width" in out:
        out["width"] = _length(out["width"])
    return out


def _sort_key(value: Any) -> tuple[int, Any]:
    # ``uiSortRows``: numbers first, by value; anything else by its lower-cased text, by code point.
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return (0, value)
    text = ("true" if value else "false") if isinstance(value, bool) else str(value)
    return (1, text.lower())


def sort_rows(rows: list[dict[str, Any]], key: str | None, order: str | None = "asc") -> list[dict[str, Any]]:
    """Sort table rows on the backend, the usual companion of ``on_sort``.

    The same order as ``uiSortRows`` of ``@silverpoint/core/ui`` (REQ-474): stable, numbers before
    anything else, which compares by code point after lower-casing; ``None`` and missing values last,
    in input order; ``desc`` reverses the present rows only.

    Args:
        rows: The rows.
        key: The column to sort by; ``None`` keeps the order.
        order: ``asc`` or ``desc``.

    Returns:
        A new, sorted list.
    """
    if not key:
        return list(rows)
    present = [row for row in rows if row.get(key) is not None]
    missing = [row for row in rows if row.get(key) is None]
    return sorted(present, key=lambda row: _sort_key(row[key]), reverse=order == "desc") + missing


def sp_table(
    columns: Sequence[dict[str, Any] | str],
    data: list[dict[str, Any]] | rx.Var,
    *,
    caption: str | rx.Var | None = None,
    sort_key: str | rx.Var | None = None,
    sort_order: Literal["asc", "desc"] | rx.Var | None = None,
    on_sort: Any = None,
    striped: bool | None = None,
    hoverable: bool | None = None,
    bordered: bool | None = None,
    empty_text: str | None = None,
    row_key: str | None = None,
    **props: Any,
) -> rx.Component:
    """A data table on a card frame: small-caps header, tabular figures, hatched striping.

    Args:
        columns: ``[{"key", "title", "align": "start"|"center"|"end", "sortable", "width"}]`` or
            plain keys; an int ``width`` is in px.
        data: Rows (dicts), static or a state var.
        caption: The table's caption (its accessible name).
        sort_key: The column currently sorted (draws its arrow and sets ``aria-sort``).
        sort_order: ``asc`` or ``desc``.
        on_sort: Handler called with the column key when a sortable header is used; pair it with
            :func:`sort_rows`.
        striped: Hatches every other row.
        hoverable: Hatches the row under the pointer.
        bordered: Draws the card frame around the table.
        empty_text: Shown when there are no rows.
        row_key: The column whose value keys each row.
        **props: Common props.

    Returns:
        The table.
    """
    return SpTable.create(
        columns=[_column(column) for column in columns],
        data=data,
        **_given(
            caption=caption,
            sort_key=sort_key,
            sort_order=sort_order,
            on_sort=on_sort,
            striped=striped,
            hoverable=hoverable,
            bordered=bordered,
            empty_text=empty_text,
            row_key=row_key,
        ),
        **props,
    )


def sp_pagination(**props: Any) -> rx.Component:
    """Page navigation; see :class:`~.surfaces.SpPagination` for its props.

    Args:
        **props: ``total``, ``page_size``, ``current``/``default_current``, ``on_change``…

    Returns:
        The pagination.
    """
    return SpPagination.create(**props)


def sp_breadcrumb(items: Sequence[dict[str, Any]] | rx.Var, *, label: str | None = None, **props: Any) -> rx.Component:
    """Where the page sits: links separated by hairline slashes; the last item is the current page.

    Args:
        items: ``[{"label", "href"}]``, static or a state var.
        label: Accessible name of the landmark.
        **props: Common props.

    Returns:
        The breadcrumb.
    """
    return SpBreadcrumb.create(
        items=items if isinstance(items, rx.Var) else list(items), **_given(label=label), **props
    )


def sp_avatar(
    *,
    src: str | rx.Var | None = None,
    name: str | rx.Var | None = None,
    initials: str | rx.Var | None = None,
    alt: str | rx.Var | None = None,
    shape: Literal["circle", "square"] | None = None,
    pixel_size: int | None = None,
    **props: Any,
) -> rx.Component:
    """A portrait in a drawn round (or square) frame, or the person's initials.

    Args:
        src: Image URL.
        name: The person's name: the accessible name, and the initials when there is no image.
        initials: Explicit initials (overrides those taken from ``name``).
        alt: Image description (``name`` by default).
        shape: ``circle`` (default) or ``square``.
        pixel_size: Exact size in px (``size`` gives sm 28 / md 40 / lg 56).
        **props: Common props.

    Returns:
        The avatar.
    """
    return SpAvatar.create(
        **_given(src=src, name=name, initials=initials, alt=alt, shape=shape, pixel_size=pixel_size), **props
    )


def sp_avatar_group(*avatars: rx.Component, label: str | None = None, **props: Any) -> rx.Component:
    """Overlapping avatars.

    Args:
        *avatars: The avatars.
        label: Accessible name of the group.
        **props: Common props.

    Returns:
        The group.
    """
    return SpAvatarGroup.create(*avatars, **_given(label=label), **props)


def sp_statistic(
    title: str | rx.Var,
    value: Any,
    *,
    prefix: str | rx.Var | None = None,
    suffix: str | rx.Var | None = None,
    trend: Literal["up", "down"] | rx.Var | None = None,
    delta: str | rx.Var | None = None,
    **props: Any,
) -> rx.Component:
    """A figure with its title: small-caps label, large tabular number, optional trend.

    Args:
        title: What the figure measures.
        value: The figure (format it before passing; it is printed as is).
        prefix: Printed before the value, small (``"$"``).
        suffix: Printed after the value, small (``"%"``, ``"kg"``).
        trend: ``up`` or ``down`` draws an arrow before ``delta``.
        delta: The change, as text (``"+8.2 %"``).
        **props: Common props.

    Returns:
        The statistic.
    """
    return SpStatistic.create(
        title=title, value=value, **_given(prefix=prefix, suffix=suffix, trend=trend, delta=delta), **props
    )


def sp_descriptions(
    items: Sequence[dict[str, Any]] | rx.Var,
    *,
    title: str | rx.Var | None = None,
    columns: int | None = None,
    bordered: bool | None = None,
    heading_level: int | None = None,
    **props: Any,
) -> rx.Component:
    """Label–value pairs in a grid (a ``<dl>``), optionally on a card frame.

    Args:
        items: ``[{"label", "value"}]``, static or a state var.
        title: Heading above the list.
        columns: Columns of the grid, 1 to 6 (3 by default; one column on narrow containers).
        bordered: Draws the card frame (default).
        heading_level: Level of the title heading, 2 to 6 (3 by default).
        **props: Common props.

    Returns:
        The descriptions.
    """
    return SpDescriptions.create(
        items=items if isinstance(items, rx.Var) else list(items),
        **_given(title=title, columns=columns, bordered=bordered, heading_level=heading_level),
        **props,
    )


def sp_timeline_list(
    items: Sequence[dict[str, Any]] | rx.Var, *, label: str | None = None, **props: Any
) -> rx.Component:
    """A vertical timeline: a drawn mark per event on a hairline, time, title and description.

    Statuses: ``done`` (hatched mark, the default), ``current`` (heightened, at most one),
    ``pending`` (empty mark, dashed line) and ``error`` (a cross). For a full narrative timeline
    with media and zoom see :func:`sp_timeline` (Knight Lab).

    Args:
        items: ``[{"title", "time", "description", "status"}]``, static or a state var.
        label: Accessible name of the list.
        **props: Common props.

    Returns:
        The timeline.
    """
    return SpTimelineList.create(
        items=items if isinstance(items, rx.Var) else list(items), **_given(label=label), **props
    )


def sp_collapse_item(
    title: str | rx.Var,
    *children: rx.Component | str,
    open: bool | rx.Var | None = None,
    disabled: bool | None = None,
    on_toggle: Any = None,
    **props: Any,
) -> rx.Component:
    """One panel of :func:`sp_collapse`: a native ``<details>``.

    Args:
        title: The summary line.
        *children: The panel's content.
        open: A bool opens it at first render (``default_open``); a state var controls it.
        disabled: The panel cannot be toggled.
        on_toggle: Handler receiving the new open state (a bool).
        **props: Common props.

    Returns:
        The panel.
    """
    state = {"open": open} if isinstance(open, rx.Var) else {"default_open": open}
    return SpCollapseItem.create(
        *children, title=title, **_given(**state, disabled=disabled, on_toggle=on_toggle), **props
    )


def sp_collapse(
    *items: rx.Component, accordion: bool | None = None, bordered: bool | None = None, **props: Any
) -> rx.Component:
    """Panels that open and close, on a card frame; native ``<details>``.

    Args:
        *items: :func:`sp_collapse_item` panels.
        accordion: Only one panel open at a time (native exclusive ``<details name>``).
        bordered: Draws the card frame (default).
        **props: Common props.

    Returns:
        The collapse.
    """
    return SpCollapse.create(*items, **_given(accordion=accordion, bordered=bordered), **props)


def sp_empty(*children: rx.Component, description: str | rx.Var | None = None, **props: Any) -> rx.Component:
    """The empty state: a lightly hatched, drawn tray and a line of italic text.

    Args:
        *children: Actions under the text (e.g. a button).
        description: The text (``"No data"``).
        **props: Common props.

    Returns:
        The empty state.
    """
    return SpEmpty.create(**_given(description=description, extra=_slot(children)), **props)


def sp_result(
    *children: rx.Component,
    status: ResultStatus | None = None,
    title: str | rx.Var = "",
    subtitle: str | rx.Var | None = None,
    heading_level: int | None = None,
    **props: Any,
) -> rx.Component:
    """The outcome of an operation: a drawn round mark (tick, info, warning, cross), title, subtitle.

    Args:
        *children: Actions under the text.
        status: ``success``, ``info`` (default), ``warning`` or ``error``.
        title: The outcome.
        subtitle: Detail.
        heading_level: Level of the title heading, 2 to 6 (3 by default).
        **props: Common props.

    Returns:
        The result.
    """
    return SpResult.create(
        title=title,
        **_given(status=status, subtitle=subtitle, heading_level=heading_level, extra=_slot(children)),
        **props,
    )


def sp_textarea(
    *,
    value: str | rx.Var | None = None,
    default_value: str | None = None,
    placeholder: str | rx.Var | None = None,
    rows: int | None = None,
    label: str | rx.Var | None = None,
    message: str | rx.Var | None = None,
    invalid: bool | rx.Var | None = None,
    disabled: bool | rx.Var | None = None,
    read_only: bool | rx.Var | None = None,
    max_length: int | None = None,
    show_count: bool | None = None,
    name: str | None = None,
    on_change: Any = None,
    **props: Any,
) -> rx.Component:
    """A multi-line text field on the ``SpInput`` contract: drawn frame, italic placeholder, message.

    ``on_change`` receives the text itself, not a DOM event.

    Args:
        value: The text (controlled).
        default_value: The initial text (uncontrolled).
        placeholder: Placeholder text.
        rows: Visible lines (3 by default).
        label: Accessible name.
        message: Help or error text under the field.
        invalid: Marks the text as invalid.
        disabled: Disabled.
        read_only: Read-only.
        max_length: Character limit.
        show_count: Prints ``length / max_length``.
        name: Form field name.
        on_change: Handler receiving the new text.
        **props: Common props. ``textarea_id`` (0.7.0) is now ``id``: the core derives the native
            textarea's id from it.

    Returns:
        The field.

    Raises:
        TypeError: On ``on_blur``, which ``SpTextarea`` does not expose.
    """
    if "on_blur" in props:
        msg = "sp_textarea has no on_blur in silverpoint 0.7.0: use on_change, which reports every edit."
        raise TypeError(msg)
    props = _renamed(props, "textarea_id", "id")
    return SpTextarea.create(
        **_given(
            value=value,
            default_value=default_value,
            placeholder=placeholder,
            rows=rows,
            label=label,
            message=message,
            invalid=invalid,
            disabled=disabled,
            read_only=read_only,
            max_length=max_length,
            show_count=show_count,
            name=name,
            on_change=on_change,
        ),
        **props,
    )


def sp_input_number(**props: Any) -> rx.Component:
    """A number field with exact − / + steppers; see :class:`~.surfaces.SpInputNumber`.

    Args:
        **props: ``value``/``default_value``, ``min``, ``max``, ``step``, ``precision``, ``on_change``…

    Returns:
        The field.
    """
    return SpInputNumber.create(**props)
