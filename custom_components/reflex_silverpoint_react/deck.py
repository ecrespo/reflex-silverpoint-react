"""Marp/Marpit slide decks drawn in silverpoint: ``sp_deck``, the npm ``SpDeck``.

``@silverpoint/react/deck`` (silverpoint 0.9.0) renders a Marp Markdown presentation in the
silverpoint style: the ``silverpoint`` Marpit theme on the library's grounds and substrates, the
``ground`` / ``substrate`` / ``mode`` directives per slide, fragmented lists, presenter notes, and
```` ```silverpoint ```` code fences that become real, hydrated charts inside a slide.

The engine lives in ``@silverpoint/marp`` (which brings ``@marp-team/marpit`` as its own
dependency). It is an optional peer of ``@silverpoint/react``, so it is a ``lib_dependencies`` entry
of this component only: Reflex installs it when a page renders ``sp_deck`` and never otherwise.

The component renders the current slide on the server and attaches its client half (scaling, keys,
swipe, fragments, chart hydration) after mount, so it needs no ``NoSSR`` wrapper. Every prop is a
string, number or boolean, and every event carries one plain object, which the event specs below
unpack into ints.
"""

from typing import Any, Literal

import reflex as rx
from reflex.vars import ObjectVar

from .base import SILVERPOINT_STYLESHEETS, SILVERPOINT_VERSION, GroundName, InkMode, Substrate
from .dashboard import _SubpathComponent
from .palette import PALETTES, Palette
from .ui import SILVERPOINT_UI_STYLESHEET

#: The ``@silverpoint/marp`` release the deck is written against: the engine, theme and controller.
MARP_VERSION = SILVERPOINT_VERSION

#: The stylesheets a deck needs, in the order silverpoint documents: the typeface, the grounds, the
#: UI components (the deck's controls) and the deck's own (the slide box, controls, overview, print).
DECK_STYLESHEETS = (*SILVERPOINT_STYLESHEETS, SILVERPOINT_UI_STYLESHEET, "@silverpoint/marp/deck.css")

#: The slide sizes the ``silverpoint`` theme declares.
DeckSize = Literal["16:9", "4:3"]


def _page_change_spec(payload: ObjectVar[dict[str, int]]) -> tuple[rx.Var[int], rx.Var[int]]:
    """``{page, total}`` → ``(page, total)``.

    Args:
        payload: The npm ``pageChange`` payload.

    Returns:
        The current page (1-based) and the number of pages.
    """
    return (payload["page"].to(int), payload["total"].to(int))


def _fragment_change_spec(payload: ObjectVar[dict[str, int]]) -> tuple[rx.Var[int], rx.Var[int], rx.Var[int]]:
    """``{page, step, steps}`` → ``(page, step, steps)``.

    Args:
        payload: The npm ``fragmentChange`` payload.

    Returns:
        The page, the fragments shown on it and its fragment count.
    """
    return (payload["page"].to(int), payload["step"].to(int), payload["steps"].to(int))


def _ready_spec(payload: ObjectVar[dict[str, int]]) -> tuple[rx.Var[int]]:
    """``{total}`` → ``(total,)``.

    Args:
        payload: The npm ``ready`` payload.

    Returns:
        The number of pages.
    """
    return (payload["total"].to(int),)


class SpDeck(_SubpathComponent):
    """A Marp/Marpit Markdown slide deck drawn in silverpoint (the npm ``SpDeck``).

    Slides are separated by ``---``; the front matter and ``<!-- key: value -->`` comments set the
    directives (Marpit's own plus ``ground``, ``substrate`` and ``mode``); any other comment is a
    presenter note; each list item is a fragment; a ```` ```silverpoint ```` fence holding
    ``{"chart": "<slug>", "props": {…}}`` draws a chart. Use it controlled (``page`` with
    ``on_page_change``) or uncontrolled (``default_page``).
    """

    tag = "SpDeck"
    _subpath = "/deck"

    lib_dependencies: list[str] = [  # noqa: RUF012 - Reflex reads it as a class attribute
        *_SubpathComponent.lib_dependencies,
        f"@silverpoint/marp@{MARP_VERSION}",
    ]

    # The Marp Markdown: front matter, ``---`` between slides, ``silverpoint`` fences for charts.
    markdown: rx.Var[str]

    # Controlled current page (1-based); pair it with ``on_page_change``.
    page: rx.Var[int]

    # Uncontrolled initial page (1-based). Default ``1``.
    default_page: rx.Var[int]

    # Accessible name of the deck region; the first heading of slide 1 by default.
    label: rx.Var[str]

    # The Marpit theme. Default ``"silverpoint"``.
    theme: rx.Var[str]

    # The deck's ground, which a ``ground`` directive overrides per slide. Default: the provider's, or ``silverpoint``.
    ground: rx.Var[GroundName | str]

    # The deck's substrate; the ground's first by default.
    substrate: rx.Var[Substrate | str]

    # ``ink`` (default) or ``precision``, which a ``mode`` directive overrides per slide.
    mode: rx.Var[InkMode]

    # A palette preset's name (``"sepia"``, ``"ironGall"``…) for the fence charts.
    palette: rx.Var[str]

    # The slide size: ``"16:9"`` (default) or ``"4:3"``.
    size: rx.Var[DeckSize]

    # Show the current slide's presenter notes (Marpit comments). Default ``False``.
    show_notes: rx.Var[bool]

    # Show the controls: previous, next, overview, notes, full screen. Default ``True``.
    show_controls: rx.Var[bool]

    # Handle the arrow, PageUp/PageDown, Space, Home/End, ``o``, ``f`` and ``n`` keys while focus is in the deck.
    keyboard: rx.Var[bool]

    # A horizontal swipe moves the deck. Default ``True``.
    swipe: rx.Var[bool]

    # Read and write a ``#<n>`` deep link in the URL. Default ``False``.
    hash: rx.Var[bool]

    # Hydrate the fence charts (``True``); ``False`` keeps them static SVG.
    interactive: rx.Var[bool]

    # The current page changed, by the reader or by a re-render that clamped it: ``(page, total)``.
    on_page_change: rx.EventHandler[_page_change_spec]

    # A fragment of the current slide was revealed or hidden: ``(page, step, steps)``.
    on_fragment_change: rx.EventHandler[_fragment_change_spec]

    # The deck rendered with a new slide count: ``(total,)``.
    on_ready: rx.EventHandler[_ready_spec]

    def add_imports(self) -> dict[str, list[str]]:
        """The typeface, the grounds, ``ui.css`` and ``@silverpoint/marp/deck.css``, in that order.

        Returns:
            Side-effect imports of the four stylesheets.
        """
        return {"": list(DECK_STYLESHEETS)}


#: The name this component was designed under; the npm tag is ``SpDeck``.
SilverpointDeck = SpDeck

#: Python preset name → the JS name the deck reads (``iron_gall`` → ``ironGall``).
_PRESET_JS = {name: name.split("_")[0] + "".join(p.title() for p in name.split("_")[1:]) for name in PALETTES}


def _palette_name(palette: Any) -> Any:
    """A preset name in its JS spelling, or the var unchanged.

    Args:
        palette: A preset name (either spelling), a preset :class:`Palette`, or a state var.

    Returns:
        The name the npm deck reads.

    Raises:
        ValueError: On anything that is not one of the presets.
    """
    if isinstance(palette, rx.Var):
        return palette
    if isinstance(palette, Palette):
        names = [name for name, preset in PALETTES.items() if preset == palette]
        if names:
            return _PRESET_JS[names[0]]
    elif isinstance(palette, str):
        if palette in _PRESET_JS:
            return _PRESET_JS[palette]
        if palette in _PRESET_JS.values():
            return palette
    msg = (
        f"sp_deck takes a palette preset by name ({', '.join(sorted(_PRESET_JS))}), not {palette!r}: "
        "the deck's charts read only the presets."
    )
    raise ValueError(msg)


def sp_deck(
    markdown: str | rx.Var,
    *,
    page: int | rx.Var | None = None,
    default_page: int | rx.Var | None = None,
    theme: str | rx.Var | None = None,
    ground: GroundName | str | rx.Var | None = None,
    substrate: Substrate | str | rx.Var | None = None,
    mode: InkMode | rx.Var | None = None,
    palette: str | Palette | rx.Var | None = None,
    size: DeckSize | rx.Var | None = None,
    show_notes: bool | rx.Var | None = None,
    show_controls: bool | rx.Var | None = None,
    keyboard: bool | rx.Var | None = None,
    swipe: bool | rx.Var | None = None,
    hash: bool | rx.Var | None = None,
    interactive: bool | rx.Var | None = None,
    label: str | rx.Var | None = None,
    on_page_change: Any = None,
    on_fragment_change: Any = None,
    on_ready: Any = None,
    **props: Any,
) -> rx.Component:
    """A Marp/Marpit Markdown slide deck drawn in silverpoint.

    Args:
        markdown: The Marp Markdown (a string or a state var): front matter, ``---`` between slides,
            ``<!-- directive: value -->`` comments, presenter notes and ``silverpoint`` chart fences.
        page: Controlled current page (1-based); pair it with ``on_page_change``.
        default_page: Uncontrolled initial page (1-based; default 1).
        theme: The Marpit theme (default ``"silverpoint"``).
        ground: The deck's ground (``silverpoint`` or ``cyanotype``); a ``ground`` directive overrides it per slide.
        substrate: The deck's substrate; the ground's first by default.
        mode: ``"ink"`` (default) or ``"precision"``; a ``mode`` directive overrides it per slide.
        palette: A palette preset for the fence charts: its name (``"iron_gall"`` or ``"ironGall"``),
            the preset :class:`Palette` itself, or a state var holding a JS preset name.
        size: ``"16:9"`` (default) or ``"4:3"``.
        show_notes: Show the current slide's presenter notes (default ``False``).
        show_controls: Show the previous / next / overview / notes / full-screen controls (default ``True``).
        keyboard: Handle the keys while focus is in the deck (default ``True``).
        swipe: A horizontal swipe moves the deck (default ``True``).
        hash: Read and write a ``#<n>`` deep link (default ``False``).
        interactive: Hydrate the fence charts (default ``True``); ``False`` keeps static SVG.
        label: Accessible name of the deck region; the first heading of slide 1 by default.
        on_page_change: Handler receiving ``(page: int, total: int)``.
        on_fragment_change: Handler receiving ``(page: int, step: int, steps: int)``; it may take
            only the first two.
        on_ready: Handler receiving ``(total: int)`` when the deck renders with a new slide count.
        **props: ``id``, ``class_name``, ``style`` and other common props.

    Returns:
        The deck.
    """
    given = {
        "markdown": markdown,
        "page": page,
        "default_page": default_page,
        "theme": theme,
        "ground": ground,
        "substrate": substrate,
        "mode": mode,
        "palette": None if palette is None else _palette_name(palette),
        "size": size,
        "show_notes": show_notes,
        "show_controls": show_controls,
        "keyboard": keyboard,
        "swipe": swipe,
        "hash": hash,
        "interactive": interactive,
        "label": label,
        "on_page_change": on_page_change,
        "on_fragment_change": on_fragment_change,
        "on_ready": on_ready,
    }
    return SpDeck.create(**{key: value for key, value in given.items() if value is not None}, **props)
