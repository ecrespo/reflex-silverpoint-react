"""The silverpoint catalog: every chart with its family and the reference of its props.

Useful to build galleries, playgrounds and documentation pages; the demo app is built on it.
"""

from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from . import charts as _charts
from .base import SilverpointChart


@dataclass(frozen=True)
class PropDoc:
    """One prop: its Python name, its JS name, its TypeScript type and what it does."""

    name: str
    js: str
    type: str
    doc: str


@dataclass(frozen=True)
class ChartInfo:
    """One chart of the catalog."""

    chart: str
    factory_name: str
    slug: str
    family: str
    summary: str
    props: tuple[PropDoc, ...] = field(default_factory=tuple)

    @property
    def component(self) -> type[SilverpointChart]:
        """The component class."""
        return getattr(_charts, self.chart)

    @property
    def factory(self) -> Callable[..., Any]:
        """The ``create`` factory, e.g. ``line_chart``."""
        return getattr(_charts, self.factory_name)


#: Props every chart takes.
COMMON_PROPS: tuple[PropDoc, ...] = (
    PropDoc("data", "data", "readonly Datum[]", "Rows to draw. If omitted, the demo dataset is rendered (REQ-093)."),
    PropDoc("ground", "ground", "GroundRef", "Style ground. Defaults to the app provider's, or `silverpoint`."),
    PropDoc("substrate", "substrate", "SubstrateName", "Prepared substrate within the ground (REQ-046)."),
    PropDoc("mode", "mode", "InkMode", "`ink` by default; `precision` disables inking (REQ-021)."),
    PropDoc("seed", "seed", "Seed", "Seed. If omitted, it is derived from `id` stably (REQ-003)."),
    PropDoc("id", "id", "string", "Stable identifier. If omitted, it is generated deterministically."),
    PropDoc("height", "height", "number", "Height of the drawing area in px. Width is the container's unless pinned."),
    PropDoc("width", "width", "number", ""),
    PropDoc(
        "chrome", "chrome", "'card' | 'bare'", "`card` draws the full frame; `bare` only the drawing area (REQ-095)."
    ),
    PropDoc("hatch_fill", "hatchFill", "'tile' | 'per-shape'", "How areas are filled (REQ-029)."),
    PropDoc("title", "title", "string", ""),
    PropDoc("badge", "badge", "string", ""),
    PropDoc("value", "value", "string | number", ""),
    PropDoc("unit", "unit", "string", ""),
    PropDoc("footer_left", "footerLeft", "string", ""),
    PropDoc("footer_right", "footerRight", "string", ""),
    PropDoc("label", "label", "string", "Accessible name. If omitted, it is derived from `title` (REQ-120)."),
    PropDoc("description", "description", "string", "Long description for screen readers (REQ-120)."),
    PropDoc(
        "data_table",
        "dataTable",
        "'visible' | 'hidden' | 'none'",
        "Tabular alternative; `hidden` leaves it for assistive technology only (REQ-121).",
    ),
    PropDoc("locale", "locale", "string", ""),
    PropDoc("number_format", "numberFormat", "Intl.NumberFormatOptions", ""),
    PropDoc("class_name", "className", "string", ""),
)

#: The 33 charts, in catalog order.
CHARTS: tuple[ChartInfo, ...] = (
    ChartInfo(
        chart="LineChart",
        factory_name="line_chart",
        slug="line-chart",
        family="Lines",
        summary="Spline with an optional dotted baseline series.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("secondary_key", "secondaryKey", "Accessor<number | null | undefined>", ""),
            PropDoc("curve", "curve", "LineCurve", ""),
            PropDoc(
                "series",
                "series",
                "'all' | 'primary'",
                "`all` draws the secondary series when there is one; `primary` omits it.",
            ),
            PropDoc(
                "connect_nulls",
                "connectNulls",
                "boolean",
                "Whether a gap left by a missing value is bridged (REQ-008).",
            ),
        ),
    ),
    ChartInfo(
        chart="StepChart",
        factory_name="step_chart",
        slug="step-chart",
        family="Lines",
        summary="A series drawn as steps.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "step",
                "step",
                "'after' | 'before' | 'middle'",
                "Where the step sits between two points; `after` by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="SparklineRows",
        factory_name="sparkline_rows",
        slug="sparkline-rows",
        family="Lines",
        summary="One row per series — name, sparkline, readout.",
        props=(
            PropDoc("rows", "rows", "number", "Rows shown, from the first; all by default."),
            PropDoc("name_key", "nameKey", "Accessor<string>", ""),
            PropDoc(
                "readout_key",
                "readoutKey",
                "Accessor<string | number | null | undefined>",
                "The printed readout; the last value of the series by default.",
            ),
            PropDoc(
                "series_key",
                "seriesKey",
                "Accessor<readonly unknown[] | null | undefined>",
                "The row's points: an array.",
            ),
            PropDoc(
                "point_key",
                "pointKey",
                "Accessor<number | null | undefined>",
                "The value of one point; the point itself when it is a number, else its `value`.",
            ),
        ),
    ),
    ChartInfo(
        chart="KpiCard",
        factory_name="kpi_card",
        slug="kpi-card",
        family="Lines",
        summary="A metric, its delta, and an area sparkline of the series.",
        props=(
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("metric", "metric", "string", "The metric's name, printed under the figure."),
            PropDoc("delta", "delta", "number", "Signed change, printed with its sign and a direction mark."),
            PropDoc(
                "delta_tone",
                "deltaTone",
                "'up' | 'down' | 'flat'",
                "Direction of the mark; from the sign of `delta` by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="BarChart",
        factory_name="bar_chart",
        slug="bar-chart",
        family="Bars",
        summary="Pill bars, as columns or rows, with an optional second series.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("secondary_key", "secondaryKey", "Accessor<number | null | undefined>", ""),
            PropDoc("orientation", "orientation", "'columns' | 'rows'", ""),
        ),
    ),
    ChartInfo(
        chart="StackedBarChart",
        factory_name="stacked_bar_chart",
        slug="stacked-bar-chart",
        family="Bars",
        summary="One stacked segment per key.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("keys", "keys", "readonly string[]", ""),
            PropDoc(
                "names",
                "names",
                "readonly string[]",
                "Display names of the keys, in order; the keys themselves by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="ComposedChart",
        factory_name="composed_chart",
        slug="composed-chart",
        family="Bars",
        summary="Columns and a spline on one value scale.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("bar_key", "barKey", "Accessor<number | null | undefined>", ""),
            PropDoc("line_key", "lineKey", "Accessor<number | null | undefined>", ""),
            PropDoc("show_line", "showLine", "boolean", ""),
        ),
    ),
    ChartInfo(
        chart="WaterfallChart",
        factory_name="waterfall_chart",
        slug="waterfall-chart",
        family="Bars",
        summary="Totals from zero and floating deltas from the running total.",
        props=(
            PropDoc("step_key", "stepKey", "Accessor<string>", ""),
            PropDoc(
                "base_key",
                "baseKey",
                "Accessor<number | null | undefined>",
                "An absolute total: the bar starts at zero and resets the running total.",
            ),
            PropDoc("delta_key", "deltaKey", "Accessor<number | null | undefined>", "A change from the running total."),
        ),
    ),
    ChartInfo(
        chart="FunnelChart",
        factory_name="funnel_chart",
        slug="funnel-chart",
        family="Bars",
        summary="Horizontal, centred stages.",
        props=(
            PropDoc("stage_key", "stageKey", "Accessor<string>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
        ),
    ),
    ChartInfo(
        chart="BulletChart",
        factory_name="bullet_chart",
        slug="bullet-chart",
        family="Bars",
        summary="One bar per target, with a marker at the target. Values in 0-100.",
        props=(
            PropDoc("title_key", "titleKey", "Accessor<string>", ""),
            PropDoc("actual_key", "actualKey", "Accessor<number | null | undefined>", ""),
            PropDoc("target_key", "targetKey", "Accessor<number | null | undefined>", ""),
        ),
    ),
    ChartInfo(
        chart="PyramidChart",
        factory_name="pyramid_chart",
        slug="pyramid-chart",
        family="Bars",
        summary="Stacked tiers whose width encodes the value (0-100).",
        props=(
            PropDoc("label_key", "labelKey", "Accessor<string>", ""),
            PropDoc("width_key", "widthKey", "Accessor<number | null | undefined>", ""),
            PropDoc("tone_key", "toneKey", "Accessor<number | null | undefined>", ""),
        ),
    ),
    ChartInfo(
        chart="CandlestickChart",
        factory_name="candlestick_chart",
        slug="candlestick-chart",
        family="Bars",
        summary="OHLC bodies and wicks.",
        props=(
            PropDoc("time_key", "timeKey", "Accessor<string | number>", ""),
            PropDoc("open_key", "openKey", "Accessor<number | null | undefined>", ""),
            PropDoc("high_key", "highKey", "Accessor<number | null | undefined>", ""),
            PropDoc("low_key", "lowKey", "Accessor<number | null | undefined>", ""),
            PropDoc("close_key", "closeKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "bounds",
                "bounds",
                "readonly [number, number]",
                "Price bounds of the scale; derived from the data when omitted (REQ-097).",
            ),
        ),
    ),
    ChartInfo(
        chart="AreaChart",
        factory_name="area_chart",
        slug="area-chart",
        family="Areas",
        summary="A curved, toned area under its line.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("curve", "curve", "LineCurve", ""),
        ),
    ),
    ChartInfo(
        chart="RangeBandChart",
        factory_name="range_band_chart",
        slug="range-band-chart",
        family="Areas",
        summary="The band between a low and a high series.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("low_key", "lowKey", "Accessor<number | null | undefined>", ""),
            PropDoc("high_key", "highKey", "Accessor<number | null | undefined>", ""),
        ),
    ),
    ChartInfo(
        chart="StreamChart",
        factory_name="stream_chart",
        slug="stream-chart",
        family="Areas",
        summary="Two waves, overlaid or stacked.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("keys", "keys", "readonly string[]", ""),
            PropDoc("stacked", "stacked", "boolean", ""),
        ),
    ),
    ChartInfo(
        chart="ScatterChart",
        factory_name="scatter_chart",
        slug="scatter-chart",
        family="Points & grids",
        summary="Points on two linear scales, optionally sized.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<number | null | undefined>", ""),
            PropDoc("y_key", "yKey", "Accessor<number | null | undefined>", ""),
            PropDoc("size_key", "sizeKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "size_range",
                "sizeRange",
                "readonly [number, number]",
                "Marker area in px², smallest to largest; `[60, 240]` by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="BubbleChart",
        factory_name="bubble_chart",
        slug="bubble-chart",
        family="Points & grids",
        summary="Circles whose area encodes `sizeKey`.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<number | null | undefined>", ""),
            PropDoc("y_key", "yKey", "Accessor<number | null | undefined>", ""),
            PropDoc("size_key", "sizeKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "size_range",
                "sizeRange",
                "readonly [number, number]",
                "Circle area in px², smallest to largest; `[100, 500]` by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="HeatmapChart",
        factory_name="heatmap_chart",
        slug="heatmap-chart",
        family="Points & grids",
        summary="Labelled rows of values, normalised against `scaleMax`.",
        props=(
            PropDoc("label_key", "labelKey", "Accessor<string>", ""),
            PropDoc("values_key", "valuesKey", "Accessor<readonly (number | null)[] | null | undefined>", ""),
            PropDoc("scale_max", "scaleMax", "number", "Value that maps to the darkest tone; 100 by default."),
            PropDoc(
                "column_labels",
                "columnLabels",
                "readonly string[]",
                "Names of the columns, in order; missing ones fall back to `#k` (delta-006).",
            ),
        ),
    ),
    ChartInfo(
        chart="TreemapChart",
        factory_name="treemap_chart",
        slug="treemap-chart",
        family="Points & grids",
        summary="Tiles of `cols × rows` cells placed in a `columns × rows` grid.",
        props=(
            PropDoc("label_key", "labelKey", "Accessor<string>", ""),
            PropDoc("share_key", "shareKey", "Accessor<number | null | undefined>", ""),
            PropDoc("columns", "columns", "number", ""),
            PropDoc("rows", "rows", "number", ""),
        ),
    ),
    ChartInfo(
        chart="ActivityGrid",
        factory_name="activity_grid",
        slug="activity-grid",
        family="Points & grids",
        summary="One cell per day, a column per week.",
        props=(
            PropDoc("date_key", "dateKey", "Accessor<string>", ""),
            PropDoc("count_key", "countKey", "Accessor<number | null | undefined>", ""),
            PropDoc("level_key", "levelKey", "Accessor<number | null | undefined>", ""),
            PropDoc("weeks", "weeks", "number", "Weeks shown, the most recent last; 26 by default."),
        ),
    ),
    ChartInfo(
        chart="SankeyChart",
        factory_name="sankey_chart",
        slug="sankey-chart",
        family="Flows",
        summary="Flow bands between layered nodes.",
        props=(
            PropDoc("source_key", "sourceKey", "Accessor<string>", ""),
            PropDoc("target_key", "targetKey", "Accessor<string>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
        ),
    ),
    ChartInfo(
        chart="ChordRing",
        factory_name="chord_ring",
        slug="chord-ring",
        family="Flows",
        summary="Directed flows between categories around a circle.",
        props=(
            PropDoc("source_key", "sourceKey", "Accessor<string | number>", ""),
            PropDoc("target_key", "targetKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "max_categories",
                "maxCategories",
                "number",
                'Categories drawn; past it the smallest merge into "Other" (`SP010`). 12 by default.',
            ),
        ),
    ),
    ChartInfo(
        chart="DonutChart",
        factory_name="donut_chart",
        slug="donut-chart",
        family="Radial",
        summary="Sectors ∝ value around a central readout.",
        props=(
            PropDoc("name_key", "nameKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("center_value", "centerValue", "string | number", "Printed in the centre; the total by default."),
            PropDoc("center_label", "centerLabel", "string", "A line under the centre value."),
            PropDoc(
                "legend", "legend", "boolean", "Names every sector with its share beside the ring; `true` by default."
            ),
        ),
    ),
    ChartInfo(
        chart="RadarChart",
        factory_name="radar_chart",
        slug="radar-chart",
        family="Radial",
        summary="One spoke per subject, a closed polygon of values.",
        props=(
            PropDoc("subject_key", "subjectKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "domain",
                "domain",
                "readonly [number, number]",
                "The value range along a spoke; `[0, the largest value]`, niced, by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="PolarBarChart",
        factory_name="polar_bar_chart",
        slug="polar-bar-chart",
        family="Radial",
        summary="360° bars out from a hole, length ∝ value.",
        props=(
            PropDoc("name_key", "nameKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
        ),
    ),
    ChartInfo(
        chart="RadialArcGroup",
        factory_name="radial_arc_group",
        slug="radial-arc-group",
        family="Radial",
        summary="Concentric 180° tracks, sweep ∝ value / the largest.",
        props=(
            PropDoc("name_key", "nameKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
        ),
    ),
    ChartInfo(
        chart="RadialRings",
        factory_name="radial_rings",
        slug="radial-rings",
        family="Radial",
        summary="Concentric progress rings, sweep ∝ value in 0-100.",
        props=(
            PropDoc("name_key", "nameKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
        ),
    ),
    ChartInfo(
        chart="GaugeArc",
        factory_name="gauge_arc",
        slug="gauge-arc",
        family="Radial",
        summary="A 240° arc swept to a percent.",
        props=(
            PropDoc("percent", "percent", "number", "0 to 100; saturated at the ends outside it."),
            PropDoc("caption", "caption", "string", "Names the measure under the readout."),
            PropDoc("readout", "readout", "string", "Printed in place of the percent."),
        ),
    ),
    ChartInfo(
        chart="MeterChart",
        factory_name="meter_chart",
        slug="meter-chart",
        family="Radial",
        summary="A semicircular meter with a needle at a percent.",
        props=(
            PropDoc("percent", "percent", "number", "0 to 100; saturated at the ends outside it."),
            PropDoc("caption", "caption", "string", "Names the measure under the readout."),
            PropDoc("readout", "readout", "string", "Printed in place of the percent."),
        ),
    ),
    ChartInfo(
        chart="CoxcombChart",
        factory_name="coxcomb_chart",
        slug="coxcomb-chart",
        family="Radial",
        summary="Equal angles, sector **area** ∝ value.",
        props=(
            PropDoc("name_key", "nameKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "start_angle",
                "startAngle",
                "number",
                "Where the first sector starts, in degrees clockwise from 12 o'clock; 0 by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="WindRose",
        factory_name="wind_rose",
        slug="wind-rose",
        family="Radial",
        summary="Observations of (bearing, speed) binned by compass sector and speed.",
        props=(
            PropDoc(
                "bearing_key",
                "bearingKey",
                "Accessor<number | null | undefined>",
                "Where the wind blows from, in degrees clockwise from north.",
            ),
            PropDoc(
                "value_key",
                "valueKey",
                "Accessor<number | null | undefined>",
                "The wind speed; 0 is a calm, which has no direction.",
            ),
            PropDoc("sectors", "sectors", "number", "Compass sectors: 4, 8, 16 or 32; 16 by default."),
            PropDoc(
                "bins",
                "bins",
                "readonly number[]",
                "Ascending speed thresholds that split each sector; `[5, 10, 15, 20]` by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="VolvelleChart",
        factory_name="volvelle_chart",
        slug="volvelle-chart",
        family="Radial",
        summary="Concentric categorical rings read against one index.",
        props=(
            PropDoc("rings", "rings", "number", "Rings shown, from the inside out; all by default."),
            PropDoc(
                "index_ring",
                "indexRing",
                "number",
                "The ring whose segment is brought under the index, 0-based; 0 by default.",
            ),
            PropDoc(
                "index_value",
                "indexValue",
                "string",
                "The segment of `indexRing` under the index; its first segment by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="OrbitChart",
        factory_name="orbit_chart",
        slug="orbit-chart",
        family="Radial",
        summary="Nested elliptical orbits with markers along them.",
        props=(
            PropDoc("orbits", "orbits", "number", "Orbits shown, from the inside out; all by default."),
            PropDoc(
                "marker_key",
                "markerKey",
                "Accessor<readonly unknown[] | null | undefined>",
                "A row's markers; `'markers'` by default.",
            ),
            PropDoc(
                "period_key",
                "periodKey",
                "Accessor<number | null | undefined>",
                "A marker's period, 0-1 over the cycle; `'period'` by default.",
            ),
        ),
    ),
)

#: Families, in catalog order.
FAMILIES: tuple[str, ...] = tuple(dict.fromkeys(info.family for info in CHARTS))


def chart_by_slug(slug: str) -> ChartInfo | None:
    """Look a chart up by its kebab-case slug (``"line-chart"``).

    Args:
        slug: The slug.

    Returns:
        The chart, or ``None``.
    """
    return next((info for info in CHARTS if info.slug == slug), None)


def chart_by_name(name: str) -> ChartInfo | None:
    """Look a chart up by its component name (``"LineChart"``).

    Args:
        name: The component name.

    Returns:
        The chart, or ``None``.
    """
    return next((info for info in CHARTS if info.chart == name), None)
