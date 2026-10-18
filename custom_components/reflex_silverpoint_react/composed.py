"""Reflex-composed components, level A: native markup drawn on silverpoint surfaces.

Table, pagination, breadcrumb, avatar, statistic, descriptions, a vertical timeline, collapse,
empty and result states, textarea and number input. Their behaviour is native HTML (a ``<table>``,
``<details>``, ``<textarea>``…) or a few lines of JS; their drawing is the ground's own frames,
tones and heightening (see :mod:`.surfaces`).

These components are Reflex-only: silverpoint's React, Vue and Angular adapters do not have them.
Unlike the ``Sp`` components they do not read ``silverpoint_provider``; pass ``ground``,
``substrate`` and ``mode`` explicitly, or wrap them in ``silverpoint_palette`` for colour.

Every builder takes the surface props: ``ground``, ``substrate``, ``mode``, ``size``, ``seed``,
``palette``, ``id``, ``class_name`` and ``style``.
"""

from collections.abc import Callable, Sequence
from typing import Any, Literal

import reflex as rx

from .surfaces import SpInputNumber, SpPagination, sp_glyph, sp_surface

Status = Literal["done", "current", "pending", "error"]
ResultStatus = Literal["success", "info", "warning", "error"]

#: The props every surface accepts, forwarded untouched by the builders.
_SURFACE_KEYS = ("ground", "substrate", "mode", "size", "seed", "palette", "id", "class_name", "style", "key")


def _surface_props(props: dict[str, Any]) -> dict[str, Any]:
    return {key: props.pop(key) for key in _SURFACE_KEYS if key in props}


def _with_style(style: Any, extra: dict[str, Any]) -> Any:
    if style is None:
        return extra
    if isinstance(style, dict):
        return {**extra, **style}
    return [extra, style]


def _items(items: Sequence[Any] | rx.Var, render: Callable[..., rx.Component]) -> list[Any]:
    """Render a static list in Python or a state var with ``rx.foreach``; splat the result."""
    if isinstance(items, rx.Var):
        return [rx.foreach(items, render)]
    return [render(item) for item in items]


# ── Table ───────────────────────────────────────────────────────────────────────────────


def _column(column: dict[str, Any] | str) -> dict[str, Any]:
    return {"key": column, "title": column} if isinstance(column, str) else {"title": column["key"], **column}


def sort_rows(rows: list[dict[str, Any]], key: str | None, order: str | None = "asc") -> list[dict[str, Any]]:
    """Sort table rows on the backend, the usual companion of ``on_sort``.

    ``None`` values sort last; mixed types sort by their string form.

    Args:
        rows: The rows.
        key: The column to sort by; ``None`` keeps the order.
        order: ``asc`` or ``desc``.

    Returns:
        A new, sorted list.
    """
    if not key:
        return list(rows)

    def sort_key(row: dict[str, Any]) -> tuple[int, Any]:
        value = row.get(key)
        if value is None:
            return (1, "")
        return (0, value if isinstance(value, (int, float)) else str(value).lower())

    present = [row for row in rows if row.get(key) is not None]
    missing = [row for row in rows if row.get(key) is None]
    try:
        ordered = sorted(present, key=sort_key, reverse=order == "desc")
    except TypeError:
        ordered = sorted(present, key=lambda row: str(row.get(key)).lower(), reverse=order == "desc")
    return ordered + missing


def sp_table(
    columns: Sequence[dict[str, Any] | str],
    data: list[dict[str, Any]] | rx.Var,
    *,
    caption: str | rx.Var | None = None,
    sort_key: str | rx.Var | None = None,
    sort_order: Literal["asc", "desc"] | rx.Var | None = None,
    on_sort: Any = None,
    striped: bool = False,
    hoverable: bool = True,
    bordered: bool = True,
    empty_text: str = "No data",
    **props: Any,
) -> rx.Component:
    """A data table on a card frame: small-caps header, tabular figures, hatched striping.

    Args:
        columns: ``[{"key", "title", "align": "start"|"center"|"end", "sortable", "width"}]`` or
            plain keys.
        data: Rows (dicts), static or a state var.
        caption: The table's caption (its accessible name).
        sort_key: The column currently sorted (draws its arrow and sets ``aria-sort``).
        sort_order: ``asc`` or ``desc``.
        on_sort: Handler called with the column key when a sortable header is clicked; pair it
            with :func:`sort_rows`.
        striped: Hatches every other row.
        hoverable: Hatches the row under the pointer.
        bordered: Draws the card frame around the table.
        empty_text: Shown when there are no rows.
        **props: Surface props.

    Returns:
        The table.
    """
    surface = _surface_props(props)
    cols = [_column(column) for column in columns]

    def header(column: dict[str, Any]) -> rx.Component:
        key = column["key"]
        attrs: dict[str, Any] = {"scope": "col", "data-align": column.get("align", "start")}
        if column.get("width"):
            attrs["style"] = {"width": column["width"]}
        if not column.get("sortable"):
            return rx.el.th(column["title"], custom_attrs=attrs)
        active = sort_key == key if isinstance(sort_key, rx.Var) else rx.Var.create(sort_key == key)
        descending = sort_order == "desc" if isinstance(sort_order, rx.Var) else rx.Var.create(sort_order == "desc")
        attrs["aria-sort"] = rx.cond(active, rx.cond(descending, "descending", "ascending"), "none")
        glyph = rx.cond(active, rx.cond(descending, "sortDown", "sortUp"), "sort")
        button_props: dict[str, Any] = {"type": "button", "class_name": "sp-ui-sort"}
        if on_sort is not None:
            button_props["on_click"] = on_sort(key)
        return rx.el.th(rx.el.button(column["title"], sp_glyph(glyph=glyph), **button_props), custom_attrs=attrs)

    def row(item: Any) -> rx.Component:
        def cell(column: dict[str, Any]) -> Any:
            return item[column["key"]] if isinstance(item, rx.Var) else item.get(column["key"], "")

        return rx.el.tr(*[rx.el.td(cell(c), custom_attrs={"data-align": c.get("align", "start")}) for c in cols])

    empty = rx.el.tr(rx.el.td(empty_text, col_span=len(cols), class_name="sp-ui-table-empty"))
    if isinstance(data, rx.Var):
        body = rx.el.tbody(rx.cond(data.to(list).length() > 0, rx.foreach(data, row), empty))
    else:
        body = rx.el.tbody(*([row(item) for item in data] or [empty]))
    table = rx.el.table(
        *([rx.el.caption(caption)] if caption is not None else []),
        rx.el.thead(rx.el.tr(*[header(c) for c in cols])),
        body,
        class_name="sp-ui-table",
    )
    return sp_surface(
        rx.el.div(table, class_name="sp-ui-table-scroll"),
        name="datatable",
        frame="card" if bordered else None,
        custom_attrs={"data-striped": str(striped).lower(), "data-hoverable": str(hoverable).lower()},
        **surface,
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


# ── Navigation and identity ─────────────────────────────────────────────────────────────


def sp_breadcrumb(items: Sequence[dict[str, Any]] | rx.Var, *, label: str = "Breadcrumb", **props: Any) -> rx.Component:
    """Where the page sits: links separated by hairline slashes; the last item is the current page.

    Args:
        items: ``[{"label", "href"}]``, static or a state var.
        label: Accessible name of the landmark.
        **props: Surface props.

    Returns:
        The breadcrumb.
    """
    surface = _surface_props(props)
    if isinstance(items, rx.Var):
        count = items.to(list).length()

        def crumb(item: Any, index: Any) -> rx.Component:
            return rx.el.li(
                rx.cond(
                    index == count - 1,
                    rx.el.span(item["label"], aria_current="page"),
                    rx.el.a(item["label"], href=item["href"]),
                ),
                class_name="sp-ui-crumb",
            )

        crumbs = [rx.foreach(items, crumb)]
    else:
        last = len(items) - 1
        crumbs = [
            rx.el.li(
                rx.el.span(item["label"], aria_current="page")
                if index == last or not item.get("href")
                else rx.el.a(item["label"], href=item["href"]),
                class_name="sp-ui-crumb",
            )
            for index, item in enumerate(items)
        ]
    return sp_surface(
        rx.el.ol(*crumbs, class_name="sp-ui-crumbs"),
        element="nav",
        name="breadcrumb",
        aria_label=label,
        **surface,
        **props,
    )


def _initials(name: str) -> str:
    parts = [part for part in name.replace("-", " ").split() if part]
    return "".join(part[0] for part in parts[:2]).upper() or "?"


def sp_avatar(
    *,
    src: str | rx.Var | None = None,
    name: str | rx.Var | None = None,
    initials: str | rx.Var | None = None,
    alt: str | rx.Var | None = None,
    shape: Literal["circle", "square"] = "circle",
    pixel_size: int | None = None,
    **props: Any,
) -> rx.Component:
    """A portrait in a drawn round (or square) frame, or the person's initials.

    Args:
        src: Image URL.
        name: The person's name: the accessible name, and the initials when there is no image.
        initials: Explicit initials (overrides those taken from ``name``).
        alt: Image description (``name`` by default).
        shape: ``circle`` or ``square``.
        pixel_size: Exact size in px (``size`` gives sm 28 / md 40 / lg 56).
        **props: Surface props.

    Returns:
        The avatar.
    """
    surface = _surface_props(props)
    if initials is None and isinstance(name, str):
        initials = _initials(name)
    content: list[Any] = []
    if src is not None:
        content.append(
            rx.el.img(src=src, alt=alt if alt is not None else (name or ""), class_name="sp-ui-avatar-image")
        )
    else:
        content.append(
            rx.el.span(
                initials if initials is not None else "?", class_name="sp-ui-avatar-initials", aria_hidden="true"
            )
        )
    if pixel_size:
        surface["style"] = _with_style(surface.get("style"), {"--sp-avatar-size": f"{pixel_size}px"})
    attrs: dict[str, Any] = {"data-shape": shape}
    if src is None:
        attrs["role"] = "img"
        if name is not None:
            attrs["aria-label"] = name
    return sp_surface(
        *content,
        element="span",
        name="avatar",
        frame="round" if shape == "circle" else "box",
        custom_attrs=attrs,
        **surface,
        **props,
    )


def sp_avatar_group(*avatars: rx.Component, label: str | None = None) -> rx.Component:
    """Overlapping avatars.

    Args:
        *avatars: The avatars.
        label: Accessible name of the group.

    Returns:
        The group.
    """
    return rx.el.div(*avatars, class_name="sp-ui-avatar-group", role="group", aria_label=label)


# ── Data display ────────────────────────────────────────────────────────────────────────


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
        **props: Surface props.

    Returns:
        The statistic.
    """
    surface = _surface_props(props)
    value_row = [
        *([rx.el.span(prefix, class_name="sp-ui-statistic-affix")] if prefix is not None else []),
        rx.el.span(value),
        *([rx.el.span(suffix, class_name="sp-ui-statistic-affix")] if suffix is not None else []),
    ]
    children: list[Any] = [
        rx.el.span(title, class_name="sp-ui-statistic-title"),
        rx.el.span(*value_row, class_name="sp-ui-statistic-value"),
    ]
    if trend is not None or delta is not None:
        mark = []
        if isinstance(trend, rx.Var):
            mark = [sp_glyph(glyph=rx.cond(trend == "down", "arrowDown", "arrowUp"))]
        elif trend is not None:
            mark = [sp_glyph(glyph="arrowDown" if trend == "down" else "arrowUp")]
        children.append(rx.el.span(*mark, *([delta] if delta is not None else []), class_name="sp-ui-statistic-trend"))
    return sp_surface(*children, name="statistic", **surface, **props)


def sp_descriptions(
    items: Sequence[dict[str, Any]] | rx.Var,
    *,
    title: str | rx.Var | None = None,
    columns: int = 3,
    bordered: bool = True,
    **props: Any,
) -> rx.Component:
    """Label–value pairs in a grid (a ``<dl>``), optionally on a card frame.

    Args:
        items: ``[{"label", "value"}]``, static or a state var.
        title: Heading above the list.
        columns: Columns of the grid (one column on narrow containers).
        bordered: Draws the card frame.
        **props: Surface props.

    Returns:
        The descriptions.
    """
    surface = _surface_props(props)

    def item(entry: Any) -> rx.Component:
        return rx.el.div(rx.el.dt(entry["label"]), rx.el.dd(entry["value"]), class_name="sp-ui-descriptions-item")

    style = {"--sp-descriptions-columns": str(columns)}
    return sp_surface(
        *([rx.el.h3(title, class_name="sp-ui-descriptions-title")] if title is not None else []),
        rx.el.dl(*_items(items, item), class_name="sp-ui-descriptions-list", style=style),
        element="section",
        name="descriptions",
        frame="card" if bordered else None,
        custom_attrs={"data-bordered": str(bordered).lower()},
        **surface,
        **props,
    )


def _timeline_mark(status: Any) -> rx.Component:
    done = rx.el.span(
        rx.el.span(custom_attrs={"part": "sp-tone", "data-tone": "selected", "data-kind": "round"}, aria_hidden="true"),
        rx.el.span(custom_attrs={"part": "sp-frame", "data-kind": "round"}, aria_hidden="true"),
        class_name="sp-ui-tl-mark",
    )
    current = rx.el.span(
        rx.el.span(custom_attrs={"part": "sp-frame", "data-kind": "round"}, aria_hidden="true"),
        rx.el.span(custom_attrs={"part": "sp-heighten"}, aria_hidden="true"),
        class_name="sp-ui-tl-mark",
    )
    error = rx.el.span(
        rx.el.span(custom_attrs={"part": "sp-frame", "data-kind": "round"}, aria_hidden="true"),
        sp_glyph(glyph="cross"),
        class_name="sp-ui-tl-mark",
    )
    pending = rx.el.span(
        rx.el.span(custom_attrs={"part": "sp-frame", "data-kind": "round"}, aria_hidden="true"),
        class_name="sp-ui-tl-mark",
    )
    if isinstance(status, rx.Var):
        return rx.match(status, ("done", done), ("current", current), ("error", error), pending)
    return {"done": done, "current": current, "error": error}.get(status, pending)


def sp_timeline_list(
    items: Sequence[dict[str, Any]] | rx.Var, *, label: str | None = None, **props: Any
) -> rx.Component:
    """A vertical timeline: a drawn mark per event on a hairline, time, title and description.

    Statuses: ``done`` (hatched mark), ``current`` (heightened, at most one), ``pending`` (empty
    mark, dashed line) and ``error`` (a cross). This is a light list; for a full narrative
    timeline with media and zoom see :func:`sp_timeline` (Knight Lab).

    Args:
        items: ``[{"title", "time", "description", "status"}]``, static or a state var.
        label: Accessible name of the list.
        **props: Surface props.

    Returns:
        The timeline.
    """
    surface = _surface_props(props)

    def entry(item: Any) -> rx.Component:
        if isinstance(items, rx.Var):
            status = item["status"].to(str)
            time, title, description = item["time"], item["title"], item["description"]
            aria_current = rx.cond(status == "current", "step", None)
        else:
            status = item.get("status", "done")
            time, title, description = item.get("time"), item.get("title"), item.get("description")
            aria_current = "step" if status == "current" else None
        body = [
            *([rx.el.span(time, class_name="sp-ui-tl-time")] if time is not None else []),
            rx.el.span(title, class_name="sp-ui-tl-title"),
            *([rx.el.span(description, class_name="sp-ui-tl-description")] if description is not None else []),
        ]
        return rx.el.li(
            _timeline_mark(status),
            rx.el.div(*body, class_name="sp-ui-tl-body"),
            class_name="sp-ui-tl-item",
            custom_attrs={"data-status": status, "aria-current": aria_current},
        )

    return sp_surface(*_items(items, entry), element="ol", name="timeline-list", aria_label=label, **surface, **props)


# ── Disclosure ──────────────────────────────────────────────────────────────────────────


def sp_collapse_item(
    title: str | rx.Component | rx.Var,
    *children: rx.Component | str,
    open: bool | rx.Var = False,
    disabled: bool = False,
    on_toggle: Any = None,
    **props: Any,
) -> rx.Component:
    """One panel of :func:`sp_collapse`: a native ``<details>``.

    Args:
        title: The summary line.
        *children: The panel's content.
        open: Open at first render (or controlled by a var).
        disabled: The panel cannot be toggled.
        on_toggle: Handler of the native ``toggle`` event.
        **props: Extra props for the ``<details>``.

    Returns:
        The panel.
    """
    summary_props: dict[str, Any] = {"class_name": "sp-ui-collapse-summary"}
    attrs: dict[str, Any] = {}
    if disabled:
        summary_props["tab_index"] = -1
        summary_props["aria_disabled"] = "true"
        summary_props["on_click"] = rx.prevent_default
        attrs["data-disabled"] = "true"
    if on_toggle is not None:
        props["on_toggle"] = on_toggle
    return rx.el.details(
        rx.el.summary(sp_glyph(glyph="chevronRight"), title, **summary_props),
        rx.el.div(*children, class_name="sp-ui-collapse-body"),
        open=open,
        class_name="sp-ui-collapse-item",
        custom_attrs=attrs,
        **props,
    )


def sp_collapse(*items: rx.Component, accordion: bool = False, bordered: bool = True, **props: Any) -> rx.Component:
    """Panels that open and close, on a card frame; native ``<details>``, no script.

    Args:
        *items: :func:`sp_collapse_item` panels.
        accordion: Only one panel open at a time (native exclusive ``<details name>``).
        bordered: Draws the card frame.
        **props: Surface props.

    Returns:
        The collapse.
    """
    surface = _surface_props(props)
    if accordion:
        group = f"sp-accordion-{id(items)}"
        for item in items:
            item.custom_attrs["name"] = group
    return sp_surface(*items, name="collapse", frame="card" if bordered else None, **surface, **props)


# ── Feedback ────────────────────────────────────────────────────────────────────────────


def sp_empty(*children: rx.Component, description: str | rx.Var = "No data", **props: Any) -> rx.Component:
    """The empty state: a lightly hatched, drawn tray and a line of italic text.

    Args:
        *children: Actions under the text (e.g. a button).
        description: The text.
        **props: Surface props.

    Returns:
        The empty state.
    """
    surface = _surface_props(props)
    figure = rx.el.span(
        rx.el.span(custom_attrs={"part": "sp-tone", "data-tone": "1", "data-kind": "control"}, aria_hidden="true"),
        rx.el.span(custom_attrs={"part": "sp-frame", "data-kind": "control"}, aria_hidden="true"),
        class_name="sp-ui-empty-figure",
        aria_hidden="true",
    )
    return sp_surface(
        figure,
        rx.el.p(description, class_name="sp-ui-empty-description"),
        *([rx.el.div(*children, class_name="sp-ui-empty-extra")] if children else []),
        name="empty",
        **surface,
        **props,
    )


_RESULT_GLYPHS = {"success": "tick", "info": "info", "warning": "warning", "error": "cross"}


def sp_result(
    *children: rx.Component,
    status: ResultStatus = "info",
    title: str | rx.Var = "",
    subtitle: str | rx.Var | None = None,
    **props: Any,
) -> rx.Component:
    """The outcome of an operation: a drawn round mark (tick, info, warning, cross), title, subtitle.

    Args:
        *children: Actions under the text.
        status: ``success``, ``info``, ``warning`` or ``error``.
        title: The outcome.
        subtitle: Detail.
        **props: Surface props.

    Returns:
        The result.
    """
    surface = _surface_props(props)
    mark = rx.el.span(
        rx.el.span(custom_attrs={"part": "sp-frame", "data-kind": "round"}, aria_hidden="true"),
        sp_glyph(glyph=_RESULT_GLYPHS[status]),
        class_name="sp-ui-result-mark",
    )
    return sp_surface(
        mark,
        rx.el.h3(title, class_name="sp-ui-result-title"),
        *([rx.el.p(subtitle, class_name="sp-ui-result-subtitle")] if subtitle is not None else []),
        *([rx.el.div(*children, class_name="sp-ui-result-extra")] if children else []),
        name="result",
        role="status" if status in ("success", "info") else "alert",
        custom_attrs={"data-status": status},
        **surface,
        **props,
    )


# ── Data entry ──────────────────────────────────────────────────────────────────────────


def sp_textarea(
    *,
    value: str | rx.Var | None = None,
    default_value: str | None = None,
    placeholder: str | rx.Var | None = None,
    rows: int = 3,
    label: str | rx.Var | None = None,
    message: str | rx.Var | None = None,
    invalid: bool | rx.Var = False,
    disabled: bool | rx.Var = False,
    read_only: bool | rx.Var = False,
    max_length: int | None = None,
    show_count: bool = False,
    name: str | None = None,
    textarea_id: str | None = None,
    on_change: Any = None,
    on_blur: Any = None,
    **props: Any,
) -> rx.Component:
    """A multi-line text field on the ``SpInput`` contract: drawn frame, italic placeholder, message.

    ``on_change`` receives the text itself, not a DOM event.

    Args:
        value: The text (controlled).
        default_value: The initial text (uncontrolled).
        placeholder: Placeholder text.
        rows: Visible lines.
        label: Accessible name.
        message: Help or error text under the field.
        invalid: Marks the text as invalid.
        disabled: Disabled.
        read_only: Read-only.
        max_length: Character limit.
        show_count: Prints ``length / max_length`` (needs a controlled ``value``).
        name: Form field name.
        textarea_id: ``id`` of the native ``<textarea>``.
        on_change: Handler receiving the new text.
        on_blur: Handler of the native blur event.
        **props: Surface props.

    Returns:
        The field.
    """
    surface = _surface_props(props)
    message_id = f"{textarea_id}--message" if message is not None and textarea_id else None
    area_props: dict[str, Any] = {
        "class_name": "sp-ui-control",
        "rows": rows,
        "placeholder": placeholder,
        "disabled": disabled,
        "read_only": read_only,
        "name": name,
        "id": textarea_id,
        "max_length": max_length,
        "aria_label": label,
        "aria_invalid": rx.cond(invalid, "true", "false")
        if isinstance(invalid, rx.Var)
        else ("true" if invalid else None),
        "aria_describedby": message_id,
    }
    if value is not None:
        area_props["value"] = value
    elif default_value is not None:
        area_props["default_value"] = default_value
    if on_change is not None:
        # Reflex's own textarea ``on_change`` already hands the handler the text.
        area_props["on_change"] = on_change
    if on_blur is not None:
        area_props["on_blur"] = on_blur
    area_props = {k: v for k, v in area_props.items() if v is not None}
    box = [
        rx.el.span(custom_attrs={"part": "sp-frame", "data-kind": "control"}, aria_hidden="true"),
        rx.el.textarea(**area_props),
    ]
    below: list[Any] = []
    if show_count and value is not None:
        count = value.to(str).length() if isinstance(value, rx.Var) else len(value)
        below.append(rx.el.span(count, f" / {max_length}" if max_length else "", class_name="sp-ui-counter"))
    if message is not None:
        below.append(rx.el.span(message, class_name="sp-ui-message", id=message_id))
    attrs = {
        "data-invalid": rx.cond(invalid, "true", "false")
        if isinstance(invalid, rx.Var)
        else ("true" if invalid else "false")
    }
    surface["style"] = _with_style(surface.get("style"), {"--sp-textarea-rows": str(rows)})
    surface["class_name"] = " ".join(filter(None, ["sp-textarea", surface.get("class_name")]))
    return sp_surface(
        rx.el.span(*box, class_name="sp-ui-box"),
        *below,
        element="span",
        name="input",
        custom_attrs=attrs,
        **surface,
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
