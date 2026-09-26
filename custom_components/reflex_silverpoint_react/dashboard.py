"""The dashboard of silverpoint 0.2: a declarative grid of cards, optionally linked.

``Dashboard`` lays its children out from a data-only layout (columns, spans and row height per
breakpoint), gives each chart the size of its cell, and titles the whole grid. With ``link`` its
charts share one linked value: the item under the pointer in one chart marks every item with
the same ``link.key`` in the others.

The npm side lives in two subpath modules of ``@silverpoint/react``: ``/dashboard`` (``Dashboard``
and ``DashboardCell``) and ``/dashboard-link`` (``DashboardLink``, the client boundary of the
linked value). Neither is in the package barrel, so these wrappers import them by subpath.
"""

from typing import Any, ClassVar, Literal

import reflex as rx
from reflex_base.utils.imports import ImportVar

from .base import GroundName, InkMode, Substrate, _SilverpointBase

Breakpoint = Literal["sm", "md", "lg"]
HeadingLevel = Literal[2, 3, 4, 5, 6]

#: A value for every breakpoint, or only some of them: ``2`` or ``{"md": 2, "lg": 3}``.
PerBreakpoint = int | dict[Breakpoint, int]

#: Defaults of ``@silverpoint/core`` (``DASHBOARD_DEFAULTS``).
DASHBOARD_DEFAULTS: dict[str, Any] = {
    "columns": {"sm": 1, "md": 2, "lg": 4},
    "row_height": 240,
    "gap": 16,
    "span": 1,
    "heading_level": 2,
    "ssr_width": 1200,
}


def _link_spec(link):
    """The linked value changed, or cleared.

    Args:
        link: ``{key, value}`` from the dashboard, or null when the source cleared.

    Returns:
        The link, forwarded unchanged to the backend handler (annotate it ``dict | None``).
    """
    return (link,)


def _as_link(link: Any) -> Any:
    """Accept ``link="hour"`` as a shorthand for ``link={"key": "hour"}``."""
    return {"key": link} if isinstance(link, str) else link


class _SubpathComponent(_SilverpointBase):
    """A component imported from a subpath module of ``@silverpoint/react``."""

    # The module inside the package, e.g. ``/dashboard``.
    _subpath: ClassVar[str] = ""

    @property
    def import_var(self) -> ImportVar:
        """Import the tag from ``@silverpoint/react<subpath>``, keeping the version pin.

        Returns:
            The import var.
        """
        return ImportVar(tag=self.tag, package_path=self._subpath)


class Dashboard(_SubpathComponent):
    """A grid of cards laid out from a data-only ``layout``.

    Its children are charts, each optionally wrapped in :class:`DashboardCell` to place it in a
    named layout cell; unmarked children follow the named cells, in source order, span 1 (they never take a
    named cell, and a layout cell no child names is dropped). Charts
    placed directly (or in a ``DashboardCell``) are sized to their cell.

    It needs ``id`` and one of ``title`` or ``label``. It is not a chart: ``ground``,
    ``substrate``, ``mode`` and ``locale`` apply to every chart inside, as with the provider.
    """

    tag = "Dashboard"
    _subpath = "/dashboard"

    # Heading printed above the grid; also its accessible name.
    title: rx.Var[str]

    # Accessible name when there is no visible title.
    label: rx.Var[str]

    # Paragraph printed under the title, and the grid's accessible description.
    description: rx.Var[str]

    # ``{columns, rowHeight, gap, cells: [{id, colSpan, rowSpan}]}``. Build it with :func:`dashboard_layout`.
    layout: rx.Var[dict[str, Any]]

    # Level of the title heading, 2 to 6 (2 by default).
    heading_level: rx.Var[HeadingLevel]

    # Width in px the grid is laid out for before the browser measures it (1200 by default).
    ssr_width: rx.Var[int | float]

    # ``{"key": "hour"}`` links the charts on that datum field; a plain string works too.
    link: rx.Var[dict[str, str]]

    # Style ground for every chart inside.
    ground: rx.Var[GroundName | str | dict[str, Any]]

    # Substrate of the dashboard's paper and of every chart inside.
    substrate: rx.Var[Substrate]

    # Inking mode for every chart inside.
    mode: rx.Var[InkMode]

    # Locale for every chart inside.
    locale: rx.Var[str]

    # The linked value changed (``{key, value}``) or cleared (``None``). Only with ``link``.
    on_link_change: rx.EventHandler[_link_spec]

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        """Create the dashboard.

        Args:
            *children: The charts, optionally wrapped in :func:`dashboard_cell`.
            **props: The dashboard's props.

        Returns:
            The component.
        """
        if "link" in props:
            props["link"] = _as_link(props["link"])
        return super().create(*children, **props)


class DashboardCell(_SubpathComponent):
    """Places its chart in the layout cell named ``cell``.

    Give it a single chart: the dashboard hands that chart its cell's id, size and settings.
    """

    tag = "DashboardCell"
    _subpath = "/dashboard"

    # Id of the layout cell this child fills. Omitted: the next cell in source order, span 1.
    cell: rx.Var[str]


class DashboardLink(_SubpathComponent):
    """Links any charts below it on one datum field, outside a :class:`Dashboard` grid.

    A ``Dashboard`` with ``link`` already renders one; use this to link charts you lay out
    yourself. It adds no element of its own.
    """

    tag = "DashboardLink"
    _subpath = "/dashboard-link"

    # ``{"key": "hour"}``: the datum field the charts are linked on; a plain string works too.
    link: rx.Var[dict[str, str]]

    # The linked value changed (``{key, value}``) or cleared (``None``).
    on_link_change: rx.EventHandler[_link_spec]

    @classmethod
    def create(cls, *children, **props) -> rx.Component:
        """Create the link boundary.

        Args:
            *children: The linked charts, anywhere below.
            **props: ``link`` and ``on_link_change``.

        Returns:
            The component.
        """
        if "link" in props:
            props["link"] = _as_link(props["link"])
        return super().create(*children, **props)


def dashboard_cell_layout(
    cell_id: str,
    col_span: PerBreakpoint | None = None,
    row_span: PerBreakpoint | None = None,
) -> dict[str, Any]:
    """One cell of a dashboard layout.

    Args:
        cell_id: The id a :func:`dashboard_cell` refers to with ``cell``.
        col_span: Columns it spans, for every breakpoint or per breakpoint (``{"md": 2, "lg": 3}``).
        row_span: Rows it spans, likewise.

    Returns:
        The cell, with the camelCase keys the dashboard reads.
    """
    cell: dict[str, Any] = {"id": cell_id}
    if col_span is not None:
        cell["colSpan"] = col_span
    if row_span is not None:
        cell["rowSpan"] = row_span
    return cell


def dashboard_layout(
    cells: list[dict[str, Any] | str] | None = None,
    columns: PerBreakpoint | None = None,
    row_height: int | None = None,
    gap: int | None = None,
) -> dict[str, Any]:
    """A dashboard layout, from Python names.

    Example:
        ``dashboard_layout(["revenue", "orders", dashboard_cell_layout("trend", col_span={"md": 2, "lg": 4})])``

    Args:
        cells: The cells in order; a string is a cell of span 1.
        columns: Columns of the grid, for every breakpoint or per breakpoint (``sm``/``md``/``lg``:
            1/2/4 by default; the breakpoints are the dashboard's own width, 640 and 1024 px).
        row_height: Height of one row in px (240 by default).
        gap: Space between cells in px (16 by default).

    Returns:
        The layout, with the camelCase keys the dashboard reads.
    """
    layout: dict[str, Any] = {}
    if columns is not None:
        layout["columns"] = columns
    if row_height is not None:
        layout["rowHeight"] = row_height
    if gap is not None:
        layout["gap"] = gap
    if cells is not None:
        layout["cells"] = [dashboard_cell_layout(c) if isinstance(c, str) else c for c in cells]
    return layout


dashboard = Dashboard.create
dashboard_cell = DashboardCell.create
dashboard_link = DashboardLink.create
