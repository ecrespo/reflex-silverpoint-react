"""Shared pieces of the silverpoint wrappers: the chart base class and the provider.

silverpoint draws charts in the manner of a Renaissance silverpoint drawing: a fine silver line
on a prepared ground, tone built from hatching, and white heightening on the live value. The
irregularity lives only in the ornament; the data geometry is exact, and every chart has a
``precision`` mode that switches the inking off.

The npm side is ``@silverpoint/react`` (client components), ``@silverpoint/grounds`` (the
stylesheet that colours the strokes, required) and ``@silverpoint/fonts`` (self-hosted
EB Garamond). Both stylesheets are imported once by any page that renders a chart.
"""

from typing import Any, Literal

import reflex as rx

#: The silverpoint npm release these wrappers are written against.
SILVERPOINT_VERSION = "0.1.1"

#: The npm package every chart is imported from (the barrel; it is side-effect free, so the
#: bundler keeps only the charts a page uses).
SILVERPOINT_LIBRARY = f"@silverpoint/react@{SILVERPOINT_VERSION}"

#: Stylesheets every app needs once: the typeface, then the grounds.
SILVERPOINT_STYLESHEETS = (
    "@silverpoint/fonts/fonts.css",
    "@silverpoint/grounds/styles.css",
)

Substrate = Literal["cream", "green", "blue", "ochre"]
InkMode = Literal["ink", "precision"]
Chrome = Literal["card", "bare"]
HatchFill = Literal["tile", "per-shape"]
DataTable = Literal["visible", "hidden", "none"]


class _SilverpointBase(rx.Component):
    """Library, npm dependencies and stylesheet imports shared by every wrapper."""

    library = SILVERPOINT_LIBRARY

    lib_dependencies: list[str] = [  # noqa: RUF012 - Reflex reads it as a class attribute
        f"@silverpoint/core@{SILVERPOINT_VERSION}",
        f"@silverpoint/grounds@{SILVERPOINT_VERSION}",
        f"@silverpoint/fonts@{SILVERPOINT_VERSION}",
    ]

    def add_imports(self) -> dict[str, list[str]]:
        """Import the typeface and the grounds stylesheet next to the component.

        Returns:
            Side-effect imports of the two stylesheets.
        """
        return {"": list(SILVERPOINT_STYLESHEETS)}


def _active_item_spec(item):
    """The item under the pointer or keyboard focus, or ``None`` when it clears.

    Args:
        item: ``{seriesKey, index, datum, value, point: {x, y}}`` from the chart, or null.

    Returns:
        The item, forwarded unchanged to the backend handler (annotate it ``dict | None``).
    """
    return (item,)


def _selected_item_spec(item):
    """The item chosen by click, Enter or Space.

    Args:
        item: ``{seriesKey, index, datum, value, point: {x, y}}`` from the chart.

    Returns:
        The item, forwarded unchanged to the backend handler.
    """
    return (item,)


class SilverpointChart(_SilverpointBase):
    """Props every silverpoint chart shares (API Spec §7, "Props every chart shares").

    Give a chart an ``id`` when you want a stable seed across renders or when you want to use
    :func:`download_svg`, :func:`get_svg` or :func:`get_geometry` on it.
    """

    # Rows to draw. If omitted, the chart renders its own demo dataset.
    data: rx.Var[list[dict[str, Any]]]

    # Style ground, by name (``"silverpoint"``) or as a complete ground object.
    ground: rx.Var[str | dict[str, Any]]

    # Prepared substrate within the ground: cream (default), green, blue or ochre.
    substrate: rx.Var[Substrate]

    # ``ink`` by default; ``precision`` switches inking off and draws exact, even strokes.
    mode: rx.Var[InkMode]

    # Seed of the hand. Same props and seed, same strokes. Derived from ``id`` when omitted.
    seed: rx.Var[int | str]

    # Height of the drawing area in px (160 by default).
    height: rx.Var[int | float]

    # Width in px. The chart takes its container's width unless this pins it.
    width: rx.Var[int | float]

    # ``card`` draws the full frame; ``bare`` only the drawing area.
    chrome: rx.Var[Chrome]

    # How areas are filled: ``tile`` (default) or ``per-shape`` (richer, much heavier).
    hatch_fill: rx.Var[HatchFill]

    # Card title.
    title: rx.Var[str]

    # Small badge printed at the top right of the card.
    badge: rx.Var[str]

    # Headline figure printed on the card.
    value: rx.Var[str | int | float]

    # Unit printed after the headline figure.
    unit: rx.Var[str]

    # Footer text, left.
    footer_left: rx.Var[str]

    # Footer text, right.
    footer_right: rx.Var[str]

    # Accessible name. Derived from ``title`` when omitted.
    label: rx.Var[str]

    # Long description for screen readers.
    description: rx.Var[str]

    # Tabular alternative: ``hidden`` (default, for assistive technology only), ``visible`` or ``none``.
    data_table: rx.Var[DataTable]

    # BCP 47 locale for number formatting, e.g. ``"es-VE"``.
    locale: rx.Var[str]

    # ``Intl.NumberFormatOptions``, e.g. ``{"style": "percent"}``.
    number_format: rx.Var[dict[str, Any]]

    # Replaces the built-in readout: a JS function ``(item, readout) => ReactNode``.
    # Build one from Python with :func:`tooltip_template`.
    tooltip: rx.Var[Any]

    # The active item changed (pointer or keyboard focus), or cleared (``None``).
    on_active_change: rx.EventHandler[_active_item_spec]

    # An item was chosen by click, Enter or Space.
    on_select: rx.EventHandler[_selected_item_spec]


class SilverpointProvider(_SilverpointBase):
    """Sets ground, substrate, mode and locale once for every chart below it.

    A prop on a chart always wins over the provider.
    """

    tag = "SilverpointProvider"

    # Style ground for every chart below.
    ground: rx.Var[str | dict[str, Any]]

    # Substrate for every chart below.
    substrate: rx.Var[Substrate]

    # Inking mode for every chart below.
    mode: rx.Var[InkMode]

    # Locale for every chart below.
    locale: rx.Var[str]


silverpoint_provider = SilverpointProvider.create
