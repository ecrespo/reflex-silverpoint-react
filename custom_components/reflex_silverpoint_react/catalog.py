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
    PropDoc(
        "data",
        "data",
        "readonly Datum[]",
        "Rows to draw. If omitted, the demo dataset is rendered (REQ-093) and the accessor props (`…_key`, `keys`, `names`) are ignored.",
    ),
    PropDoc(
        "ground",
        "ground",
        "GroundRef",
        "Style ground: `silverpoint` or `cyanotype`, or a ground object. Defaults to the app provider's, or `silverpoint`.",
    ),
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

#: The 60 charts, in catalog order: the 33 of the first catalog, then the 27 of silverpoint 0.6.
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
    ChartInfo(
        chart="HistogramChart",
        factory_name="histogram_chart",
        slug="histogram-chart",
        family="Distributions & comparisons",
        summary="Raw observations binned in the core.",
        props=(
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "bins",
                "bins",
                "number | readonly number[]",
                "A number asks for that many equal-width bins over the niced extent; an array gives the thresholds, increasing. Freedman–Diaconis by default, Sturges when the IQR is 0.",
            ),
            PropDoc("cumulative", "cumulative", "boolean", "Turns the counts into a running total."),
            PropDoc("orientation", "orientation", "ChartOrientation", ""),
        ),
    ),
    ChartInfo(
        chart="EcdfChart",
        factory_name="ecdf_chart",
        slug="ecdf-chart",
        family="Distributions & comparisons",
        summary="The empirical cumulative distribution as a step function.",
        props=(
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("group_key", "groupKey", "Accessor<string | null | undefined>", "Two groups at most are drawn."),
            PropDoc("markers", "markers", "readonly number[]", "Quantiles, in 0-1, drawn as rules."),
        ),
    ),
    ChartInfo(
        chart="BoxPlotChart",
        factory_name="box_plot_chart",
        slug="box-plot-chart",
        family="Distributions & comparisons",
        summary="Quartiles, median, Tukey whiskers and outliers per group.",
        props=(
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("group_key", "groupKey", "Accessor<string | null | undefined>", ""),
            PropDoc("whisker", "whisker", "number", "Whisker reach as a multiple of the IQR; 1.5 by default."),
            PropDoc("outliers", "outliers", "boolean", "Draws the observations past the whiskers; `true` by default."),
            PropDoc("orientation", "orientation", "ChartOrientation", ""),
        ),
    ),
    ChartInfo(
        chart="ViolinChart",
        factory_name="violin_chart",
        slug="violin-chart",
        family="Distributions & comparisons",
        summary="A mirrored kernel density per group.",
        props=(
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("group_key", "groupKey", "Accessor<string | null | undefined>", ""),
            PropDoc(
                "bandwidth",
                "bandwidth",
                "number",
                "Kernel bandwidth in data units, shared by every group; Silverman's rule by default.",
            ),
            PropDoc("quartiles", "quartiles", "boolean", "Marks the quartiles inside each violin; `true` by default."),
            PropDoc("orientation", "orientation", "ChartOrientation", ""),
        ),
    ),
    ChartInfo(
        chart="RidgelineChart",
        factory_name="ridgeline_chart",
        slug="ridgeline-chart",
        family="Distributions & comparisons",
        summary="A kernel density per group on overlapping baselines.",
        props=(
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "group_key",
                "groupKey",
                "Accessor<string | null | undefined>",
                "The group of an observation; one ridge per group.",
            ),
            PropDoc(
                "bandwidth",
                "bandwidth",
                "number",
                "Kernel bandwidth in data units, shared by every group; Silverman's rule by default.",
            ),
            PropDoc(
                "overlap", "overlap", "number", "How far a ridge reaches into the one behind it, 0-1; 0.5 by default."
            ),
        ),
    ),
    ChartInfo(
        chart="BeeswarmChart",
        factory_name="beeswarm_chart",
        slug="beeswarm-chart",
        family="Distributions & comparisons",
        summary="One point per observation, packed without overlap.",
        props=(
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("group_key", "groupKey", "Accessor<string | null | undefined>", ""),
            PropDoc(
                "label_key",
                "labelKey",
                "Accessor<string | null | undefined>",
                "Names the point in the readout and the table.",
            ),
            PropDoc("radius", "radius", "number", "Point radius in px; 3 by default."),
        ),
    ),
    ChartInfo(
        chart="LollipopChart",
        factory_name="lollipop_chart",
        slug="lollipop-chart",
        family="Distributions & comparisons",
        summary="A stem from the baseline and a head at the value.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("orientation", "orientation", "ChartOrientation", ""),
            PropDoc(
                "sort",
                "sort",
                "'none' | 'ascending' | 'descending'",
                "Order of the categories; `none` keeps the data order.",
            ),
        ),
    ),
    ChartInfo(
        chart="DumbbellChart",
        factory_name="dumbbell_chart",
        slug="dumbbell-chart",
        family="Distributions & comparisons",
        summary="Two values per category joined by a segment.",
        props=(
            PropDoc("label_key", "labelKey", "Accessor<string>", ""),
            PropDoc("start_key", "startKey", "Accessor<number | null | undefined>", ""),
            PropDoc("end_key", "endKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "names",
                "names",
                "readonly [string, string]",
                "Titles of the two values; `['start', 'end']` by default.",
            ),
            PropDoc(
                "end_marker",
                "endMarker",
                "'dot' | 'arrow'",
                "`arrow` encodes the direction from the first value to the second.",
            ),
            PropDoc(
                "orientation", "orientation", "ChartOrientation", "`rows` by default: long category names read across."
            ),
        ),
    ),
    ChartInfo(
        chart="SlopeChart",
        factory_name="slope_chart",
        slug="slope-chart",
        family="Distributions & comparisons",
        summary="Two period axes, one segment per category.",
        props=(
            PropDoc("label_key", "labelKey", "Accessor<string>", ""),
            PropDoc("start_key", "startKey", "Accessor<number | null | undefined>", ""),
            PropDoc("end_key", "endKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "names",
                "names",
                "readonly [string, string]",
                "Titles of the two periods; `['start', 'end']` by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="BumpChart",
        factory_name="bump_chart",
        slug="bump-chart",
        family="Distributions & comparisons",
        summary="The rank of each series at each x.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<string | number>", ""),
            PropDoc("series_key", "seriesKey", "Accessor<string>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "order",
                "order",
                "'descending' | 'ascending'",
                "`descending` gives rank 1 to the highest value (the default).",
            ),
            PropDoc("series", "series", "number", "Series drawn, the best-ranked first; all by default."),
        ),
    ),
    ChartInfo(
        chart="ErrorBarChart",
        factory_name="error_bar_chart",
        slug="error-bar-chart",
        family="Distributions & comparisons",
        summary="A point estimate with its interval per category.",
        props=(
            PropDoc("label_key", "labelKey", "Accessor<string>", ""),
            PropDoc("estimate_key", "estimateKey", "Accessor<number | null | undefined>", ""),
            PropDoc("low_key", "lowKey", "Accessor<number | null | undefined>", ""),
            PropDoc("high_key", "highKey", "Accessor<number | null | undefined>", ""),
            PropDoc("reference", "reference", "number", "A reference value drawn as a dotted rule."),
            PropDoc("orientation", "orientation", "ChartOrientation", "`rows` by default, as a forest plot reads."),
        ),
    ),
    ChartInfo(
        chart="IntervalChart",
        factory_name="interval_chart",
        slug="interval-chart",
        family="Distributions & comparisons",
        summary="Floating bars from start to end on lanes.",
        props=(
            PropDoc("lane_key", "laneKey", "Accessor<string>", ""),
            PropDoc("start_key", "startKey", "Accessor<number | string | null | undefined>", ""),
            PropDoc("end_key", "endKey", "Accessor<number | string | null | undefined>", ""),
            PropDoc("label_key", "labelKey", "Accessor<string | null | undefined>", ""),
            PropDoc(
                "axis", "axis", "'number' | 'date'", "`date` reads ISO `YYYY-MM-DD` days in UTC; `number` by default."
            ),
        ),
    ),
    ChartInfo(
        chart="DivergingBarChart",
        factory_name="diverging_bar_chart",
        slug="diverging-bar-chart",
        family="Distributions & comparisons",
        summary="Ordered levels stacked on both sides of a neutral centre.",
        props=(
            PropDoc("label_key", "labelKey", "Accessor<string>", ""),
            PropDoc("levels", "levels", "readonly string[]", "The level columns, most negative first."),
            PropDoc(
                "neutral",
                "neutral",
                "number | null",
                "Index of the neutral level, split across the centre; `null` for none. The middle one by default.",
            ),
            PropDoc("percent", "percent", "boolean", "Normalises each row to 100 %; `true` by default."),
        ),
    ),
    ChartInfo(
        chart="ConnectedScatterChart",
        factory_name="connected_scatter_chart",
        slug="connected-scatter-chart",
        family="Distributions & comparisons",
        summary="An ordered path through x-y points.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<number | null | undefined>", ""),
            PropDoc("y_key", "yKey", "Accessor<number | null | undefined>", ""),
            PropDoc("label_key", "labelKey", "Accessor<string | null | undefined>", ""),
            PropDoc("arrows", "arrows", "boolean", "Draws direction marks along the path; `true` by default."),
        ),
    ),
    ChartInfo(
        chart="WaffleChart",
        factory_name="waffle_chart",
        slug="waffle-chart",
        family="Hierarchies & dimensions",
        summary="A unit grid filled in reading order by category.",
        props=(
            PropDoc("name_key", "nameKey", "Accessor<string | number>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("cells", "cells", "number", "Cells in the grid; 100 by default."),
            PropDoc("columns", "columns", "number", "Cells per row; 10 by default."),
        ),
    ),
    ChartInfo(
        chart="MarimekkoChart",
        factory_name="marimekko_chart",
        slug="marimekko-chart",
        family="Hierarchies & dimensions",
        summary="Column width by total, segment height by share.",
        props=(
            PropDoc("column_key", "columnKey", "Accessor<string>", ""),
            PropDoc("segment_key", "segmentKey", "Accessor<string>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
        ),
    ),
    ChartInfo(
        chart="SquarifiedTreemap",
        factory_name="squarified_treemap",
        slug="squarified-treemap",
        family="Hierarchies & dimensions",
        summary="Nested rectangles, area by value, drillable through `rootId` and `onRootChange`.",
        props=(
            PropDoc("id_key", "idKey", "Accessor<string>", ""),
            PropDoc("parent_key", "parentKey", "Accessor<string | null | undefined>", "`null` for the root."),
            PropDoc("label_key", "labelKey", "Accessor<string | null | undefined>", ""),
            PropDoc(
                "value_key",
                "valueKey",
                "Accessor<number | null | undefined>",
                "Read on leaves; an internal node is the sum of its children.",
            ),
            PropDoc("depth", "depth", "number", "Levels drawn below the root; all by default."),
            PropDoc(
                "root_id", "rootId", "string | null", "The node drawn as root, controlled; the data root by default."
            ),
            PropDoc(
                "on_root_change",
                "onRootChange",
                "(id: string | null) => void",
                "A node asked to be drawn as root (`None`: back to the top); pass it back as `root_id`.",
            ),
        ),
    ),
    ChartInfo(
        chart="SunburstChart",
        factory_name="sunburst_chart",
        slug="sunburst-chart",
        family="Hierarchies & dimensions",
        summary="A hierarchy as rings of arcs, drillable through `rootId` and `onRootChange`.",
        props=(
            PropDoc("id_key", "idKey", "Accessor<string>", ""),
            PropDoc("parent_key", "parentKey", "Accessor<string | null | undefined>", "`null` for the root."),
            PropDoc("label_key", "labelKey", "Accessor<string | null | undefined>", ""),
            PropDoc(
                "value_key",
                "valueKey",
                "Accessor<number | null | undefined>",
                "Read on leaves; an internal node is the sum of its children.",
            ),
            PropDoc("depth", "depth", "number", "Rings drawn below the root; all by default."),
            PropDoc(
                "root_id", "rootId", "string | null", "The node drawn as root, controlled; the data root by default."
            ),
            PropDoc(
                "on_root_change",
                "onRootChange",
                "(id: string | null) => void",
                "A node asked to be drawn as root (`None`: back to the top); pass it back as `root_id`.",
            ),
        ),
    ),
    ChartInfo(
        chart="TreeChart",
        factory_name="tree_chart",
        slug="tree-chart",
        family="Hierarchies & dimensions",
        summary="A tidy node-link tree.",
        props=(
            PropDoc("id_key", "idKey", "Accessor<string>", ""),
            PropDoc("parent_key", "parentKey", "Accessor<string | null | undefined>", "`null` for the root."),
            PropDoc("label_key", "labelKey", "Accessor<string | null | undefined>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", ""),
            PropDoc("orientation", "orientation", "'horizontal' | 'vertical'", ""),
        ),
    ),
    ChartInfo(
        chart="ParallelCoordinatesChart",
        factory_name="parallel_coordinates_chart",
        slug="parallel-coordinates-chart",
        family="Hierarchies & dimensions",
        summary="One polyline per row across parallel axes.",
        props=(
            PropDoc("label_key", "labelKey", "Accessor<string | null | undefined>", ""),
            PropDoc("dimensions", "dimensions", "readonly string[]", "The dimension columns, in axis order."),
            PropDoc(
                "domains",
                "domains",
                "Readonly<Record<string, readonly [number, number]>>",
                "Axis domains by dimension; derived from the data when omitted.",
            ),
        ),
    ),
    ChartInfo(
        chart="PolarLineChart",
        factory_name="polar_line_chart",
        slug="polar-line-chart",
        family="Hierarchies & dimensions",
        summary="A line over angle and radius.",
        props=(
            PropDoc("angle_key", "angleKey", "Accessor<number | null | undefined>", "In the units of `period`."),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", "The radius, `≥ 0`."),
            PropDoc("period", "period", "number", "One turn, in the units of the angle; when set, the line closes."),
            PropDoc(
                "start_angle",
                "startAngle",
                "number",
                "Where the angle 0 sits, in degrees clockwise from 12 o'clock; 0 by default.",
            ),
        ),
    ),
    ChartInfo(
        chart="PolarScatterChart",
        factory_name="polar_scatter_chart",
        slug="polar-scatter-chart",
        family="Hierarchies & dimensions",
        summary="Points over angle and radius.",
        props=(
            PropDoc("angle_key", "angleKey", "Accessor<number | null | undefined>", "In the units of `period`."),
            PropDoc("radius_key", "radiusKey", "Accessor<number | null | undefined>", "The radius, `≥ 0`."),
            PropDoc("size_key", "sizeKey", "Accessor<number | null | undefined>", ""),
            PropDoc("period", "period", "number", "One turn, in the units of the angle; 360 by default."),
        ),
    ),
    ChartInfo(
        chart="DensityBinChart",
        factory_name="density_bin_chart",
        slug="density-bin-chart",
        family="Fields & networks",
        summary="X-y points counted in two-dimensional bins.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<number | null | undefined>", ""),
            PropDoc("y_key", "yKey", "Accessor<number | null | undefined>", ""),
            PropDoc("bin_shape", "binShape", "'hexagon' | 'rect'", ""),
            PropDoc("bin_size", "binSize", "number", "Bin size in px; 14 by default."),
        ),
    ),
    ChartInfo(
        chart="ContourChart",
        factory_name="contour_chart",
        slug="contour-chart",
        family="Fields & networks",
        summary="Iso-lines and filled bands of a density or a grid.",
        props=(
            PropDoc(
                "source",
                "source",
                "'points' | 'grid'",
                "`points` estimates a density from a point cloud; `grid` reads a regular grid of values.",
            ),
            PropDoc("x_key", "xKey", "Accessor<number | null | undefined>", ""),
            PropDoc("y_key", "yKey", "Accessor<number | null | undefined>", ""),
            PropDoc(
                "value_key", "valueKey", "Accessor<number | null | undefined>", "The grid value (`source: 'grid'`)."
            ),
            PropDoc(
                "levels",
                "levels",
                "number | readonly number[]",
                "A count of levels, or the thresholds, increasing: in the grid's values, or as shares of the density's peak.",
            ),
            PropDoc("filled", "filled", "boolean", "Fills the bands between levels; `true` by default."),
        ),
    ),
    ChartInfo(
        chart="DelaunayChart",
        factory_name="delaunay_chart",
        slug="delaunay-chart",
        family="Fields & networks",
        summary="The triangulation of x-y points, or its Voronoi cells.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<number | null | undefined>", ""),
            PropDoc("y_key", "yKey", "Accessor<number | null | undefined>", ""),
            PropDoc("label_key", "labelKey", "Accessor<string | null | undefined>", ""),
            PropDoc("mesh", "mesh", "'delaunay' | 'voronoi'", ""),
        ),
    ),
    ChartInfo(
        chart="VectorFieldChart",
        factory_name="vector_field_chart",
        slug="vector-field-chart",
        family="Fields & networks",
        summary="An arrow per grid point.",
        props=(
            PropDoc("x_key", "xKey", "Accessor<number | null | undefined>", ""),
            PropDoc("y_key", "yKey", "Accessor<number | null | undefined>", ""),
            PropDoc("u_key", "uKey", "Accessor<number | null | undefined>", ""),
            PropDoc("v_key", "vKey", "Accessor<number | null | undefined>", ""),
            PropDoc("scale", "scale", "number", "Arrow length per unit of magnitude; fitted to the grid by default."),
        ),
    ),
    ChartInfo(
        chart="NetworkChart",
        factory_name="network_chart",
        slug="network-chart",
        family="Fields & networks",
        summary="A node-link graph.",
        props=(
            PropDoc("source_key", "sourceKey", "Accessor<string>", ""),
            PropDoc("target_key", "targetKey", "Accessor<string>", ""),
            PropDoc("value_key", "valueKey", "Accessor<number | null | undefined>", "1 by default."),
            PropDoc(
                "nodes",
                "nodes",
                "readonly NetworkNode[]",
                "The nodes, as data; the distinct ends of the links by default.",
            ),
            PropDoc("iterations", "iterations", "number", "Layout iterations; 300 by default."),
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
