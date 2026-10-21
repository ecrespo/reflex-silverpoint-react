"""Knight Lab TimelineJS drawn in silverpoint: ``sp_timeline``, the npm ``SpTimeline``.

``@silverpoint/react/timeline`` (silverpoint 0.7.0) builds TimelineJS 3.9.13 on the client, in a
section on a card frame, in two layers:

1. **Skin** — ``@silverpoint/grounds/timeline.css`` replaces TimelineJS's colours, type and rules with
   the ground's ``--sp-`` custom properties: the substrate, the inks, EB Garamond, hairline rules,
   eras hatched by density, the current marker heightened. Substrates, palettes, ``cyanotype`` and
   ``precision`` all apply.
2. **Hand** — the ground's own hand-inked frames and tone tiles are read from hidden probes and laid
   on TimelineJS's markers, eras and menubar. ``inked_frames=False`` keeps the skin only.

TimelineJS is an npm dependency of this component only (``@knight-lab/timelinejs``, installed when
a page uses ``sp_timeline``); no Python extra is needed any more. If it cannot be loaded the
component warns ``SP025`` and renders its ``fallback``.
"""

from typing import Any

import reflex as rx
from reflex.event import no_args_event_spec, passthrough_event_spec

from .base import SILVERPOINT_STYLESHEETS
from .ui import SILVERPOINT_UI_STYLESHEET, SilverpointUi

#: The TimelineJS release silverpoint 0.7.0 skins (its optional peer).
TIMELINEJS_VERSION = "3.9.13"

#: TimelineJS's own stylesheet, then the silverpoint skin over it (API Spec §1.3).
TIMELINE_STYLESHEETS = (
    "@knight-lab/timelinejs/dist/css/timeline.css",
    "@silverpoint/grounds/timeline.css",
)

_id_spec = passthrough_event_spec(str)
_payload_spec = passthrough_event_spec(dict)


class SpTimeline(SilverpointUi):
    """A Knight Lab TimelineJS timeline drawn in silverpoint."""

    tag = "SpTimeline"
    _subpath = "/timeline"

    lib_dependencies: list[str] = [  # noqa: RUF012 - Reflex reads it as a class attribute
        *SilverpointUi.lib_dependencies,
        f"@knight-lab/timelinejs@{TIMELINEJS_VERSION}",
    ]

    # TimelineJS data: ``{"title", "events", "eras", "scale"}``.
    data: rx.Var[dict[str, Any]]

    # TimelineJS options; ``font`` and ``theme`` are ignored (the skin sets both).
    options: rx.Var[dict[str, Any]]

    # Height of the whole timeline, a CSS length (``"600px"``).
    height: rx.Var[str]

    # Lays the ground's hand-drawn frames and tone tiles (``True``).
    inked_frames: rx.Var[bool]

    # Frames the whole timeline as a card (``True``).
    card: rx.Var[bool]

    # Accessible name of the region.
    label: rx.Var[str]

    # Shown when TimelineJS could not be loaded.
    fallback: rx.Var[rx.Component]

    # The slide shown changed: its ``unique_id``.
    on_change: rx.EventHandler[_id_spec]

    # TimelineJS finished loading: its payload.
    on_loaded: rx.EventHandler[_payload_spec]

    on_nav_next: rx.EventHandler[no_args_event_spec]
    on_nav_previous: rx.EventHandler[no_args_event_spec]
    on_zoom_in: rx.EventHandler[no_args_event_spec]
    on_zoom_out: rx.EventHandler[no_args_event_spec]
    on_back_to_start: rx.EventHandler[no_args_event_spec]

    def add_imports(self) -> dict[str, list[str]]:
        """The typeface, the grounds, ``ui.css``, TimelineJS's stylesheet and the skin, in that order.

        Returns:
            Side-effect imports of the stylesheets.
        """
        return {"": [*SILVERPOINT_STYLESHEETS, SILVERPOINT_UI_STYLESHEET, *TIMELINE_STYLESHEETS]}


def timeline_available() -> bool:
    """Whether :func:`sp_timeline` can be used.

    Kept for 0.7.0 code: since 0.7.1 the timeline needs no Python extra, so this is always ``True``.

    Returns:
        ``True``.
    """
    return True


def _plain(value: Any) -> Any:
    """A ``TimelineData`` / ``TimelineOptions`` of reflex-knightlab-timeline → its dict."""
    if value is not None and not isinstance(value, (dict, rx.Var)) and hasattr(value, "to_dict"):
        return value.to_dict()
    return value


def sp_timeline(
    data: Any = None,
    options: Any = None,
    *,
    height: int | str | None = None,
    inked_frames: bool | None = None,
    card: bool | None = None,
    label: str | rx.Var | None = None,
    fallback: rx.Component | None = None,
    on_change: Any = None,
    on_loaded: Any = None,
    on_nav_next: Any = None,
    on_nav_previous: Any = None,
    on_zoom_in: Any = None,
    on_zoom_out: Any = None,
    on_back_to_start: Any = None,
    **props: Any,
) -> rx.Component:
    """A Knight Lab TimelineJS timeline drawn in silverpoint.

    Args:
        data: The TimelineJS data (``{"title", "events", "eras", "scale"}``), an object with
            ``to_dict()`` (reflex-knightlab-timeline's ``TimelineData``), or a state var.
        options: TimelineJS options (dict, ``to_dict()`` object or var). ``font`` and ``theme`` are
            ignored: the skin sets both.
        height: Height of the whole timeline (px or CSS length; 600 px by default).
        inked_frames: Lays the ground's hand-drawn frames and tone tiles (default).
        card: Frames the whole timeline as a card (default).
        label: Accessible name of the region.
        fallback: Shown if TimelineJS cannot be loaded.
        on_change: Handler receiving the ``unique_id`` of the slide shown.
        on_loaded: Handler receiving TimelineJS's ``loaded`` payload.
        on_nav_next: The next arrow was used.
        on_nav_previous: The previous arrow was used.
        on_zoom_in: Zoomed in.
        on_zoom_out: Zoomed out.
        on_back_to_start: The "back to start" button was used.
        **props: Common props: ``ground``, ``substrate``, ``mode``, ``palette``, ``seed``, ``id``,
            ``class_name``, ``style``.

    Returns:
        The timeline.
    """
    options = _plain(options)
    if isinstance(options, dict):
        options = {key: value for key, value in options.items() if key not in ("font", "theme")}
    given = {
        "data": _plain(data),
        "options": options,
        "height": f"{height}px" if isinstance(height, (int, float)) and not isinstance(height, bool) else height,
        "inked_frames": inked_frames,
        "card": card,
        "label": label,
        "fallback": fallback,
        "on_change": on_change,
        "on_loaded": on_loaded,
        "on_nav_next": on_nav_next,
        "on_nav_previous": on_nav_previous,
        "on_zoom_in": on_zoom_in,
        "on_zoom_out": on_zoom_out,
        "on_back_to_start": on_back_to_start,
    }
    return SpTimeline.create(**{key: value for key, value in given.items() if value is not None}, **props)
