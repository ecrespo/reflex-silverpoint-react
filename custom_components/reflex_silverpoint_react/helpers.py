"""Python helpers for what the React API does with functions and refs.

* :func:`tooltip_template` builds the ``tooltip`` render function from a Python format string.
* :func:`download_svg`, :func:`get_svg` and :func:`get_geometry` reach the chart's imperative
  handle (``ChartHandle``: ``toSVGString()`` and ``getGeometry()``) through the Reflex ref that a
  component with an ``id`` gets.
"""

import json
import re
from typing import Any

import reflex as rx

_PLACEHOLDER = re.compile(r"\{([A-Za-z_][\w.]*)\}")

#: Placeholders :func:`tooltip_template` understands, besides ``{datum.<field>}``.
TOOLTIP_FIELDS = {
    "heading": "r.heading",
    "text": "r.text",
    "announcement": "r.announcement",
    "value": "item.value",
    "index": "item.index",
    "series": "item.seriesKey",
}


def _escape_template_literal(text: str) -> str:
    return text.replace("\\", "\\\\").replace("`", "\\`").replace("${", "\\${")


def tooltip_template(template: str) -> rx.Var:
    """Build a ``tooltip`` renderer from a format string.

    The result is a JS function ``(item, readout) => string``, which silverpoint prints in place
    of its built-in readout.

    Placeholders: ``{heading}`` and ``{text}`` (the built-in readout's two lines),
    ``{announcement}``, ``{value}``, ``{index}``, ``{series}`` and ``{datum.<field>}`` for any
    field of the active row. Double the braces for a literal brace: ``{{`` and ``}}``.

    Example:
        ``line_chart(tooltip=tooltip_template("{datum.hour} h · {value} hits"))``

    Args:
        template: The text to print, with placeholders.

    Returns:
        A Var holding the JS function.

    Raises:
        ValueError: If a placeholder is not one of the known names.
    """
    open_mark, close_mark = "\x00", "\x01"
    source = template.replace("{{", open_mark).replace("}}", close_mark)
    parts: list[str] = []
    last = 0
    for match in _PLACEHOLDER.finditer(source):
        parts.append(_escape_template_literal(source[last : match.start()]))
        name = match.group(1)
        if name in TOOLTIP_FIELDS:
            expression = TOOLTIP_FIELDS[name]
        elif name.startswith("datum.") and len(name) > len("datum."):
            path = "".join(f"?.[{json.dumps(key)}]" for key in name.split(".")[1:])
            expression = f"item.datum{path}"
        else:
            msg = f"Unknown tooltip placeholder {{{name}}}. Use one of {sorted(TOOLTIP_FIELDS)} or datum.<field>."
            raise ValueError(msg)
        parts.append(f"${{{expression} ?? ''}}")
        last = match.end()
    parts.append(_escape_template_literal(source[last:]))
    body = "".join(parts).replace(open_mark, "{").replace(close_mark, "}")
    return rx.Var(f"((item, r) => `{body}`)")


def chart_ref(chart_id: str) -> str:
    """The name of the Reflex ref of the chart whose ``id`` is ``chart_id``.

    Args:
        chart_id: The ``id`` given to the chart.

    Returns:
        The ref name, as Reflex registers it in ``refs``.
    """
    return "ref_" + re.sub(r"[^\w]+", "_", chart_id)


def _handle(chart_id: str) -> str:
    return f"refs[{json.dumps(chart_ref(chart_id))}]?.current"


def download_svg(chart_id: str, filename: str = "silverpoint-chart.svg") -> rx.event.EventSpec:
    """Download the chart as a standalone SVG file, entirely in the browser.

    The SVG carries its own ground colours, so it renders the same outside the app.

    Args:
        chart_id: The ``id`` given to the chart.
        filename: Name of the downloaded file.

    Returns:
        An event to use as a trigger, e.g. ``rx.button(on_click=download_svg("sales"))``.
    """
    script = f"""(() => {{
  const handle = {_handle(chart_id)};
  if (!handle || typeof handle.toSVGString !== "function") {{
    console.warn("silverpoint: no chart with id {chart_id}");
    return null;
  }}
  const svg = handle.toSVGString();
  const url = URL.createObjectURL(new Blob([svg], {{ type: "image/svg+xml" }}));
  const link = document.createElement("a");
  link.href = url;
  link.download = {json.dumps(filename)};
  document.body.appendChild(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 1000);
  return svg.length;
}})()"""
    return rx.call_script(script)


def get_svg(chart_id: str, callback: Any) -> rx.event.EventSpec:
    """Send the chart's standalone SVG markup to a backend event handler.

    Args:
        chart_id: The ``id`` given to the chart.
        callback: Event handler that receives the SVG string (or ``None``).

    Returns:
        An event that runs the script and calls ``callback`` with the result.
    """
    return rx.call_script(f"{_handle(chart_id)}?.toSVGString?.() ?? null", callback=callback)


def get_geometry(chart_id: str, callback: Any) -> rx.event.EventSpec:
    """Send the chart's computed geometry (scales, hit areas…) to a backend event handler.

    Args:
        chart_id: The ``id`` given to the chart.
        callback: Event handler that receives the geometry as a dict (or ``None``).

    Returns:
        An event that runs the script and calls ``callback`` with the result.
    """
    script = f"(() => {{ const g = {_handle(chart_id)}?.getGeometry?.(); return g ? JSON.parse(JSON.stringify(g)) : null; }})()"
    return rx.call_script(script, callback=callback)
