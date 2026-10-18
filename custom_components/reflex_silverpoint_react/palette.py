"""Colour for every chart, UI component and dashboard: palettes over the ``--sp-`` custom properties.

silverpoint never writes a colour into its SVG: every stroke and fill is painted by CSS through the
``--sp-`` custom properties of the ground (REQ-041, REQ-042). Re-colouring is therefore one thing
done the same way everywhere: setting those properties on the element that declares them, which
re-themes without re-rendering.

* ``palette=`` on any chart, UI component or dashboard colours that one element.
* :func:`silverpoint_palette` colours a whole section (every silverpoint element inside it).
* :data:`PALETTES` holds presets named after historical drawing media; :func:`check_palette`
  verifies a palette against the contrast thresholds of the silverpoint data model (§3.2).

A palette is monochrome by design. Tone is built from hatch density (Art. 6), so a chart has two
inks, ``ink`` for the main series and ``ink_secondary`` for the second, never a colour per series.
``precision`` mode and the system's high-contrast modes still apply on top of any palette.
"""

from dataclasses import asdict, dataclass, fields, replace
from typing import Any

import reflex as rx

#: Palette field → the ``--sp-`` custom property it sets.
PALETTE_PROPERTIES: dict[str, str] = {
    "substrate": "--sp-substrate",
    "ink": "--sp-ink",
    "ink_secondary": "--sp-ink-secondary",
    "heighten": "--sp-heighten",
    "rule": "--sp-rule",
    "grid": "--sp-grid",
    "text": "--sp-text",
    "text_muted": "--sp-text-muted",
    "focus": "--sp-ui-focus-color",
}

#: Minimum contrast of each field against the substrate (Data Model §3.2): 4.5 for anything read
#: as text or as a series, 3.0 for rules, grid and the focus ring. ``heighten`` is exempt: it is
#: always outlined (§3.3).
CONTRAST_THRESHOLDS: dict[str, float] = {
    "ink": 4.5,
    "ink_secondary": 4.5,
    "text": 4.5,
    "text_muted": 4.5,
    "rule": 3.0,
    "grid": 3.0,
    "focus": 3.0,
}

#: The cream substrate of the silverpoint ground: what a palette without ``substrate`` sits on.
DEFAULT_SUBSTRATE = "#EDE7DA"


@dataclass(frozen=True)
class Palette:
    """The colours of one ground's inks. Every field is optional: unset fields keep the ground's own.

    Values are any CSS colour (``"#8A3A24"``, ``"rgb(…)"``, ``"var(--brand)"``);
    :func:`check_palette` can only measure hex values.
    """

    # The prepared ground the drawing sits on.
    substrate: str | None = None
    # The main series and the frames of UI components.
    ink: str | None = None
    # The second series.
    ink_secondary: str | None = None
    # White heightening on the live value (always outlined with ``ink``).
    heighten: str | None = None
    # Rules and baselines.
    rule: str | None = None
    # Grid lines.
    grid: str | None = None
    # Large figures and primary labels.
    text: str | None = None
    # Axis labels and secondary text.
    text_muted: str | None = None
    # Focus ring of UI components (``ink`` by default).
    focus: str | None = None

    def to_dict(self) -> dict[str, str]:
        """The set fields only.

        Returns:
            ``{field: colour}``.
        """
        return {key: value for key, value in asdict(self).items() if value is not None}

    def to_css(self) -> dict[str, str]:
        """The ``--sp-`` custom properties this palette sets.

        Returns:
            ``{"--sp-ink": "#…", …}``.
        """
        return {PALETTE_PROPERTIES[key]: value for key, value in self.to_dict().items()}

    def merged(self, **changes: str | None) -> "Palette":
        """A copy with some fields changed.

        Args:
            **changes: Fields to set (``None`` clears one).

        Returns:
            The new palette.
        """
        return replace(self, **changes)

    @classmethod
    def from_dict(cls, values: dict[str, Any]) -> "Palette":
        """Build a palette from a dict, rejecting unknown fields.

        Args:
            values: ``{field: colour}``.

        Returns:
            The palette.

        Raises:
            ValueError: On a field that is not a palette field.
        """
        known = {f.name for f in fields(cls)}
        unknown = set(values) - known
        if unknown:
            msg = f"Unknown palette fields {sorted(unknown)}; use {sorted(known)}."
            raise ValueError(msg)
        return cls(**{key: value for key, value in values.items() if value is not None})


#: Presets named after historical drawing media, each verified by :func:`check_palette`.
PALETTES: dict[str, Palette] = {
    # The silverpoint ground's own inks on cream: what a chart draws with no palette.
    "silverpoint": Palette(
        substrate="#EDE7DA",
        ink="#5A5E65",
        ink_secondary="#685C4D",
        heighten="#FFFFFF",
        rule="#737A82",
        grid="#737A82",
        text="#3F4348",
        text_muted="#5A5E65",
    ),
    # Red chalk (sanguine), as in Leonardo's and Andrea del Sarto's studies.
    "sanguine": Palette(
        substrate="#F2E8DC",
        ink="#8A3A24",
        ink_secondary="#6A4A3A",
        heighten="#FFFFFF",
        rule="#9A6450",
        grid="#9A6450",
        text="#4A2216",
        text_muted="#7A3E2C",
    ),
    # Sepia wash and bistre.
    "sepia": Palette(
        substrate="#F0E6D2",
        ink="#6B4C2C",
        ink_secondary="#5A5148",
        heighten="#FFFFFF",
        rule="#8A6E52",
        grid="#8A6E52",
        text="#3B2A18",
        text_muted="#6B4C2C",
    ),
    # Iron-gall ink: the blue-black of manuscripts.
    "iron_gall": Palette(
        substrate="#EEEAE0",
        ink="#3C4858",
        ink_secondary="#6A4E36",
        heighten="#FFFFFF",
        rule="#6C7584",
        grid="#6C7584",
        text="#232B36",
        text_muted="#4A5566",
    ),
    # Verdigris, the copper green of illuminators.
    "verdigris": Palette(
        substrate="#E7EDE6",
        ink="#2C6355",
        ink_secondary="#65563F",
        heighten="#FFFFFF",
        rule="#5C7B71",
        grid="#5C7B71",
        text="#1F3D36",
        text_muted="#3E6A5E",
    ),
    # Indigo, the dyers' and printers' blue.
    "indigo": Palette(
        substrate="#E9EAF1",
        ink="#3A4884",
        ink_secondary="#675641",
        heighten="#FFFFFF",
        rule="#68709A",
        grid="#68709A",
        text="#232C52",
        text_muted="#4A5590",
    ),
}

#: What ``palette=`` accepts: a :class:`Palette`, a preset name, a dict of fields, or a state var
#: holding a dict of fields.
PaletteLike = Palette | str | dict[str, Any] | rx.Var


def _relative_luminance(hex_colour: str) -> float:
    value = hex_colour.lstrip("#")
    if len(value) == 3:
        value = "".join(c * 2 for c in value)
    channels = [int(value[i : i + 2], 16) / 255 for i in (0, 2, 4)]
    linear = [c / 12.92 if c <= 0.03928 else ((c + 0.055) / 1.055) ** 2.4 for c in channels]
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2]


def contrast_ratio(foreground: str, background: str) -> float:
    """WCAG contrast ratio between two hex colours.

    Args:
        foreground: ``#rgb`` or ``#rrggbb``.
        background: ``#rgb`` or ``#rrggbb``.

    Returns:
        The ratio, from 1 to 21.
    """
    lighter, darker = sorted((_relative_luminance(foreground), _relative_luminance(background)), reverse=True)
    return (lighter + 0.05) / (darker + 0.05)


def _is_hex(value: str) -> bool:
    value = value.lstrip("#")
    return len(value) in (3, 6) and all(c in "0123456789abcdefABCDEF" for c in value)


def check_palette(palette: PaletteLike) -> list[str]:
    """Check a palette against the contrast thresholds of the silverpoint data model.

    Only hex colours can be measured; other values are skipped. A palette without ``substrate``
    is measured against the cream substrate.

    Args:
        palette: The palette, a preset name or a dict.

    Returns:
        One message per field below its threshold; empty when the palette passes.
    """
    resolved = resolve_palette(palette)
    if not isinstance(resolved, Palette):
        return []
    values = resolved.to_dict()
    substrate = values.get("substrate", DEFAULT_SUBSTRATE)
    if not _is_hex(substrate):
        return []
    problems = []
    for key, threshold in CONTRAST_THRESHOLDS.items():
        colour = values.get(key)
        if colour is None or not _is_hex(colour):
            continue
        ratio = contrast_ratio(colour, substrate)
        if ratio < threshold:
            problems.append(f"{key} {colour} on {substrate}: {ratio:.2f}:1, below {threshold}:1")
    return problems


def resolve_palette(palette: PaletteLike | None) -> Palette | rx.Var | None:
    """Normalise what ``palette=`` accepts.

    Args:
        palette: A :class:`Palette`, a preset name, a dict of fields, a state var or ``None``.

    Returns:
        A :class:`Palette`, the var unchanged, or ``None``.

    Raises:
        ValueError: On an unknown preset name or field.
        TypeError: On any other type.
    """
    if palette is None or isinstance(palette, (Palette, rx.Var)):
        return palette
    if isinstance(palette, str):
        if palette not in PALETTES:
            msg = f"Unknown palette preset {palette!r}; use one of {sorted(PALETTES)}."
            raise ValueError(msg)
        return PALETTES[palette]
    if isinstance(palette, dict):
        return Palette.from_dict(palette)
    msg = f"palette must be a Palette, a preset name, a dict or a Var, not {type(palette).__name__}."
    raise TypeError(msg)


def palette_css(palette: PaletteLike | None) -> dict[str, Any]:
    """The ``--sp-`` declarations of a palette, as a style dict.

    For a state var holding a dict, every field is read from the var at runtime; fields the dict
    does not have stay unset (the ground's own colour).

    Args:
        palette: What ``palette=`` accepts.

    Returns:
        ``{"--sp-ink": …, …}``; empty for ``None``.
    """
    resolved = resolve_palette(palette)
    if resolved is None:
        return {}
    if isinstance(resolved, rx.Var):
        mapping = resolved.to(dict)
        return {prop: mapping[key] for key, prop in PALETTE_PROPERTIES.items()}
    return resolved.to_css()


def _merge_style(style: Any, extra: dict[str, Any]) -> Any:
    if not extra:
        return style
    if style is None:
        return extra
    if isinstance(style, dict):
        return {**style, **extra}
    if isinstance(style, (list, tuple)):
        return [*style, extra]
    return [style, extra]


def apply_palette(props: dict[str, Any]) -> dict[str, Any]:
    """Turn a ``palette`` prop into style on the element itself.

    The declarations go under ``&&`` (the element's emotion class, doubled): that outweighs both
    the ground's zero-specificity defaults and a surrounding :func:`silverpoint_palette`, so an
    element's own palette always wins over its section's.

    Args:
        props: The props passed to ``create``; ``palette`` is popped.

    Returns:
        The props, with the palette merged into ``style``.
    """
    palette = props.pop("palette", None)
    declarations = palette_css(palette)
    if declarations:
        props["style"] = _merge_style(props.get("style"), {"&&": declarations})
    return props


#: The elements that declare the ``--sp-`` properties: a chart root, a UI component root and a
#: dashboard section (a chart's inner ``<svg>`` inherits from its root and declares nothing).
_GROUND_ELEMENTS = ":where(.sp-root, .sp-ui, .sp-dashboard, .sp-surface)"


def silverpoint_palette(*children: rx.Component, palette: PaletteLike, **props: Any) -> rx.Component:
    """Colour every chart, UI component and dashboard inside a section.

    The wrapper is ``display: contents``, so it takes no layout space. An element's own
    ``palette=`` still wins over the section's.

    Args:
        *children: The section.
        palette: A :class:`Palette`, a preset name, a dict of fields or a state var.
        **props: Extra props for the wrapper ``div``.

    Returns:
        The wrapper.
    """
    declarations = palette_css(palette)
    style = {"display": "contents", f"& {_GROUND_ELEMENTS}": declarations}
    props["style"] = _merge_style(props.get("style"), style) if props.get("style") else style
    return rx.el.div(*children, **props)
