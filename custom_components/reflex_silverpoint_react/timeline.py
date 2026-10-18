"""Knight Lab TimelineJS drawn in silverpoint: ``sp_timeline``.

Wraps `reflex-knightlab-timeline <https://github.com/ecrespo/reflex-knightlab-timeline>`_ (an
optional dependency: ``pip install "reflex-silverpoint-react[timeline]"``) in a silverpoint
surface, in two layers:

1. **Skin** — TimelineJS's colours, type and rules are replaced by the ground's ``--sp-`` custom
   properties: the substrate, the inks, EB Garamond, hairline rules, eras hatched by density, the
   current marker heightened. Substrates, palettes, ``cyanotype`` and ``precision`` all apply.
2. **Hand** — the ground's own hand-inked frames and tone tiles (the CSS masks of
   ``@silverpoint/grounds/ui.css``) are read from hidden probes and laid on TimelineJS's markers,
   eras and menubar, so they are drawn with exactly the same pieces as the ``Sp`` components.
   ``inked_frames=False`` keeps the skin only; ``precision`` mode and forced colours switch the
   hand off by themselves.
"""

import json
from pathlib import Path
from typing import Any

import reflex as rx
from reflex_base.utils.imports import ImportVar

from .surfaces import sp_surface

_ASSETS = Path(__file__).parent / "assets"

#: The skin, injected once into ``<head>`` by the first timeline.
TIMELINE_CSS = (_ASSETS / "timeline.css").read_text(encoding="utf-8")

#: The probe component, as Reflex custom code.
TIMELINE_CODE = f"const SP_TIMELINE_CSS = {json.dumps(TIMELINE_CSS)};\n" + (_ASSETS / "timeline.jsx").read_text(
    encoding="utf-8"
)

_MISSING = (
    "sp_timeline needs reflex-knightlab-timeline. Install it with "
    '`pip install "reflex-silverpoint-react[timeline]"` (or `pip install reflex-knightlab-timeline`).'
)


class SpTimelineInk(rx.Component):
    """Publishes the ground's frame and tone masks to the timeline around it (phase 2)."""

    tag = "SilverpointTimelineInk"

    # Lays the hand-inked frames; ``False`` keeps the skin only.
    inked: rx.Var[bool]

    def add_imports(self) -> dict[str, Any]:
        """React hooks used by the probe.

        Returns:
            The imports.
        """
        return {"react": [ImportVar(tag="useEffect"), ImportVar(tag="useRef")]}

    def add_custom_code(self) -> list[str]:
        """The skin and the probe component.

        Returns:
            One code block.
        """
        return [TIMELINE_CODE]


def timeline_available() -> bool:
    """Whether the optional ``reflex-knightlab-timeline`` dependency is installed.

    Returns:
        ``True`` when :func:`sp_timeline` can be used.
    """
    try:
        import reflex_knightlab_timeline  # noqa: F401
    except ImportError:
        return False
    return True


def sp_timeline(
    data: Any = None,
    options: Any = None,
    *,
    height: int | str = 600,
    inked_frames: bool = True,
    card: bool = True,
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
        data: The TimelineJS data (``{"title", "events", "eras", "scale"}``), a ``TimelineData`` of
            reflex-knightlab-timeline, or a state var.
        options: TimelineJS options (dict or ``TimelineOptions``). ``font`` and ``theme`` are
            ignored: the skin sets both.
        height: Height of the whole timeline (px or CSS length).
        inked_frames: Lays the ground's hand-drawn frames and tone tiles (phase 2).
        card: Frames the whole timeline as a card.
        on_change: Handler receiving the ``unique_id`` of the slide shown.
        on_loaded: Handler receiving TimelineJS's ``loaded`` payload.
        on_nav_next: The next arrow was used.
        on_nav_previous: The previous arrow was used.
        on_zoom_in: Zoomed in.
        on_zoom_out: Zoomed out.
        on_back_to_start: The "back to start" button was used.
        **props: Surface props: ``ground``, ``substrate``, ``mode``, ``palette``, ``seed``,
            ``id``, ``class_name``, ``style``.

    Returns:
        The timeline.

    Raises:
        ImportError: If reflex-knightlab-timeline is not installed.
    """
    try:
        from reflex_knightlab_timeline import timeline as knightlab_timeline
    except ImportError as error:  # pragma: no cover - depends on the environment
        raise ImportError(_MISSING) from error

    if options is not None and not isinstance(options, (dict, rx.Var)) and hasattr(options, "to_dict"):
        options = options.to_dict()
    if isinstance(options, dict):
        options = {key: value for key, value in options.items() if key not in ("font", "theme")}
    events = {
        "on_change": on_change,
        "on_loaded": on_loaded,
        "on_nav_next": on_nav_next,
        "on_nav_previous": on_nav_previous,
        "on_zoom_in": on_zoom_in,
        "on_zoom_out": on_zoom_out,
        "on_back_to_start": on_back_to_start,
    }
    inner = knightlab_timeline(
        data=data,
        options=options if options is not None else {},
        style={"width": "100%", "height": "100%"},
        **{key: value for key, value in events.items() if value is not None},
    )
    length = f"{height}px" if isinstance(height, int) else height
    style = {"height": length}
    user_style = props.pop("style", None)
    return sp_surface(
        SpTimelineInk.create(inked=inked_frames),
        inner,
        name="kl-timeline",
        frame="card" if card else None,
        style=[style, user_style] if user_style is not None else style,
        custom_attrs={"data-kl-card": "true" if card else "false", "data-kl-inked": "false"},
        **props,
    )
