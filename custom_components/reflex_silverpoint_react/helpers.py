"""Python helpers for what the React API does with functions and refs.

* :func:`tooltip_template` builds the ``tooltip`` render function from a Python format string.
* :func:`download_svg`, :func:`get_svg` and :func:`get_geometry` reach the chart's imperative
  handle (``ChartHandle``: ``toSVGString()`` and ``getGeometry()``) through the Reflex ref that a
  component with an ``id`` gets. The two SVG helpers put the page's silverpoint stylesheet inside
  the markup, so the file paints itself outside the app.
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


#: A JS function ``(svg) => svg``: the markup of ``toSVGString()`` with the page's silverpoint
#: stylesheet inside it. ``toSVGString()`` returns the canonical markup, whose strokes and fills are
#: painted by ``@silverpoint/grounds`` through ``--sp-*`` properties; opened on its own it is black
#: (#45, silverpoint#14). The rules are read from the page (``document.styleSheets``), so the file
#: carries exactly what the app paints with, its own overrides included: every rule that names a
#: ``.sp-`` class or a ``--sp-`` property, also inside ``@media``/``@supports``/``@layer`` groups.
#: They go in CDATA as the first child of the root ``<svg>``: the stylesheet may hold ``<`` and the
#: file must stay XML. A value that is not SVG markup, or a page with no such rule, is returned as
#: it came. A stylesheet from another origin cannot be read and is skipped.
STANDALONE_SVG_JS = """((svg) => {
  if (typeof svg !== "string") return svg ?? null;
  const open = /^<svg(?:[^>"']|"[^"]*"|'[^']*')*>/.exec(svg)?.[0];
  if (!open) return svg;
  const ours = (text) => /(?:\\.|--)sp-/.test(text);
  const collect = (rules) => {
    const out = [];
    for (const rule of rules) {
      if (!ours(rule.cssText)) continue;
      // A group (@media, @supports, @layer) keeps only our rules; a style rule is kept whole.
      if (!rule.selectorText && rule.cssRules && rule.cssRules.length > 0) {
        const inner = collect(rule.cssRules);
        if (inner.length > 0) out.push(rule.cssText.slice(0, rule.cssText.indexOf("{") + 1) + inner.join("\\n") + "}");
      } else {
        out.push(rule.cssText);
      }
    }
    return out;
  };
  const css = [];
  for (const sheet of document.styleSheets) {
    let rules;
    try {
      rules = sheet.cssRules;
    } catch {
      continue;
    }
    css.push(...collect(rules));
  }
  if (css.length === 0) return svg;
  const style = "<style><![CDATA[" + css.join("\\n").replaceAll("]]>", "]]]]><![CDATA[>") + "]]></style>";
  return open + style + svg.slice(open.length);
})"""


def download_svg(chart_id: str, filename: str = "silverpoint-chart.svg") -> rx.event.EventSpec:
    """Download the chart as a standalone SVG file, entirely in the browser.

    The file holds the chart's markup and, inside it, the page's silverpoint stylesheet, so it
    renders with the same ground, substrate and palette outside the app. The typeface is not
    embedded: a viewer without EB Garamond falls back to its own serif.

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
  const svg = {STANDALONE_SVG_JS}(handle.toSVGString());
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

    As with :func:`download_svg`, the markup holds the page's silverpoint stylesheet, so it paints
    itself when saved or sent elsewhere.

    Args:
        chart_id: The ``id`` given to the chart.
        callback: Event handler that receives the SVG string (or ``None``).

    Returns:
        An event that runs the script and calls ``callback`` with the result.
    """
    return rx.call_script(f"{STANDALONE_SVG_JS}({_handle(chart_id)}?.toSVGString?.() ?? null)", callback=callback)


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
