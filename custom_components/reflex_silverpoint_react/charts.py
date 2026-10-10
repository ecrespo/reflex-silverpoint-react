"""The 60 silverpoint charts as Reflex components.

Generated from the silverpoint API reference (``docs/site/generated/props.json``) and then
kept by hand. Every class wraps the client component of the same name exported by
``@silverpoint/react``; every chart also takes the props of :class:`SilverpointChart`.
"""

from typing import Any, Literal

import reflex as rx

from .base import SilverpointChart


class LineChart(SilverpointChart):
    """Spline with an optional dotted baseline series."""

    tag = "LineChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Key of each row in `data` to read.
    secondary_key: rx.Var[str]

    curve: rx.Var[Literal["monotone", "linear", "natural", "step"]]

    # `all` draws the secondary series when there is one; `primary` omits it.
    series: rx.Var[Literal["all", "primary"]]

    # Whether a gap left by a missing value is bridged.
    connect_nulls: rx.Var[bool]


line_chart = LineChart.create


class StepChart(SilverpointChart):
    """A series drawn as steps."""

    tag = "StepChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Where the step sits between two points; `after` by default.
    step: rx.Var[Literal["after", "before", "middle"]]


step_chart = StepChart.create


class SparklineRows(SilverpointChart):
    """One row per series — name, sparkline, readout."""

    tag = "SparklineRows"

    # Rows shown, from the first; all by default.
    rows: rx.Var[int]

    # Key of each row in `data` to read.
    name_key: rx.Var[str]

    # The printed readout; the last value of the series by default.
    readout_key: rx.Var[str]

    # The row's points: an array.
    series_key: rx.Var[str]

    # The value of one point; the point itself when it is a number, else its `value`.
    point_key: rx.Var[str]


sparkline_rows = SparklineRows.create


class KpiCard(SilverpointChart):
    """A metric, its delta, and an area sparkline of the series."""

    tag = "KpiCard"

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # The metric's name, printed under the figure.
    metric: rx.Var[str]

    # Signed change, printed with its sign and a direction mark.
    delta: rx.Var[int | float]

    # Direction of the mark; from the sign of `delta` by default.
    delta_tone: rx.Var[Literal["up", "down", "flat"]]


kpi_card = KpiCard.create


class BarChart(SilverpointChart):
    """Pill bars, as columns or rows, with an optional second series."""

    tag = "BarChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Key of each row in `data` to read.
    secondary_key: rx.Var[str]

    orientation: rx.Var[Literal["columns", "rows"]]


bar_chart = BarChart.create


class StackedBarChart(SilverpointChart):
    """One stacked segment per key."""

    tag = "StackedBarChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    keys: rx.Var[list[str]]

    # Display names of the keys, in order; the keys themselves by default.
    names: rx.Var[list[str]]


stacked_bar_chart = StackedBarChart.create


class ComposedChart(SilverpointChart):
    """Columns and a spline on one value scale."""

    tag = "ComposedChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    bar_key: rx.Var[str]

    # Key of each row in `data` to read.
    line_key: rx.Var[str]

    show_line: rx.Var[bool]


composed_chart = ComposedChart.create


class WaterfallChart(SilverpointChart):
    """Totals from zero and floating deltas from the running total."""

    tag = "WaterfallChart"

    # Key of each row in `data` to read.
    step_key: rx.Var[str]

    # An absolute total: the bar starts at zero and resets the running total.
    base_key: rx.Var[str]

    # A change from the running total.
    delta_key: rx.Var[str]


waterfall_chart = WaterfallChart.create


class FunnelChart(SilverpointChart):
    """Horizontal, centred stages."""

    tag = "FunnelChart"

    # Key of each row in `data` to read.
    stage_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]


funnel_chart = FunnelChart.create


class BulletChart(SilverpointChart):
    """One bar per target, with a marker at the target. Values in 0-100."""

    tag = "BulletChart"

    # Key of each row in `data` to read.
    title_key: rx.Var[str]

    # Key of each row in `data` to read.
    actual_key: rx.Var[str]

    # Key of each row in `data` to read.
    target_key: rx.Var[str]


bullet_chart = BulletChart.create


class PyramidChart(SilverpointChart):
    """Stacked tiers whose width encodes the value (0-100)."""

    tag = "PyramidChart"

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # Key of each row in `data` to read.
    width_key: rx.Var[str]

    # Key of each row in `data` to read.
    tone_key: rx.Var[str]


pyramid_chart = PyramidChart.create


class CandlestickChart(SilverpointChart):
    """OHLC bodies and wicks."""

    tag = "CandlestickChart"

    # Key of each row in `data` to read.
    time_key: rx.Var[str]

    # Key of each row in `data` to read.
    open_key: rx.Var[str]

    # Key of each row in `data` to read.
    high_key: rx.Var[str]

    # Key of each row in `data` to read.
    low_key: rx.Var[str]

    # Key of each row in `data` to read.
    close_key: rx.Var[str]

    # Price bounds of the scale; derived from the data when omitted.
    bounds: rx.Var[list[int | float]]


candlestick_chart = CandlestickChart.create


class AreaChart(SilverpointChart):
    """A curved, toned area under its line."""

    tag = "AreaChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    curve: rx.Var[Literal["monotone", "linear", "natural", "step"]]


area_chart = AreaChart.create


class RangeBandChart(SilverpointChart):
    """The band between a low and a high series."""

    tag = "RangeBandChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    low_key: rx.Var[str]

    # Key of each row in `data` to read.
    high_key: rx.Var[str]


range_band_chart = RangeBandChart.create


class StreamChart(SilverpointChart):
    """Two waves, overlaid or stacked."""

    tag = "StreamChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    keys: rx.Var[list[str]]

    stacked: rx.Var[bool]


stream_chart = StreamChart.create


class ScatterChart(SilverpointChart):
    """Points on two linear scales, optionally sized."""

    tag = "ScatterChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    y_key: rx.Var[str]

    # Key of each row in `data` to read.
    size_key: rx.Var[str]

    # Marker area in px², smallest to largest; `[60, 240]` by default.
    size_range: rx.Var[list[int | float]]


scatter_chart = ScatterChart.create


class BubbleChart(SilverpointChart):
    """Circles whose area encodes `sizeKey`."""

    tag = "BubbleChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    y_key: rx.Var[str]

    # Key of each row in `data` to read.
    size_key: rx.Var[str]

    # Circle area in px², smallest to largest; `[100, 500]` by default.
    size_range: rx.Var[list[int | float]]


bubble_chart = BubbleChart.create


class HeatmapChart(SilverpointChart):
    """Labelled rows of values, normalised against `scaleMax`."""

    tag = "HeatmapChart"

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # Key of each row in `data` to read.
    values_key: rx.Var[str]

    # Value that maps to the darkest tone; 100 by default.
    scale_max: rx.Var[int | float]

    # Names of the columns, in order; missing ones fall back to `#k`.
    column_labels: rx.Var[list[str]]


heatmap_chart = HeatmapChart.create


class TreemapChart(SilverpointChart):
    """Tiles of `cols × rows` cells placed in a `columns × rows` grid."""

    tag = "TreemapChart"

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # Key of each row in `data` to read.
    share_key: rx.Var[str]

    columns: rx.Var[int]

    rows: rx.Var[int]


treemap_chart = TreemapChart.create


class ActivityGrid(SilverpointChart):
    """One cell per day, a column per week."""

    tag = "ActivityGrid"

    # Key of each row in `data` to read.
    date_key: rx.Var[str]

    # Key of each row in `data` to read.
    count_key: rx.Var[str]

    # Key of each row in `data` to read.
    level_key: rx.Var[str]

    # Weeks shown, the most recent last; 26 by default.
    weeks: rx.Var[int]


activity_grid = ActivityGrid.create


class SankeyChart(SilverpointChart):
    """Flow bands between layered nodes."""

    tag = "SankeyChart"

    # Key of each row in `data` to read.
    source_key: rx.Var[str]

    # Key of each row in `data` to read.
    target_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]


sankey_chart = SankeyChart.create


class ChordRing(SilverpointChart):
    """Directed flows between categories around a circle."""

    tag = "ChordRing"

    # Key of each row in `data` to read.
    source_key: rx.Var[str]

    # Key of each row in `data` to read.
    target_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Categories drawn; past it the smallest merge into "Other" (`SP010`). 12 by default.
    max_categories: rx.Var[int]


chord_ring = ChordRing.create


class DonutChart(SilverpointChart):
    """Sectors ∝ value around a central readout."""

    tag = "DonutChart"

    # Key of each row in `data` to read.
    name_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Printed in the centre; the total by default.
    center_value: rx.Var[str | int | float]

    # A line under the centre value.
    center_label: rx.Var[str]

    # Names every sector with its share beside the ring; `true` by default.
    legend: rx.Var[bool]


donut_chart = DonutChart.create


class RadarChart(SilverpointChart):
    """One spoke per subject, a closed polygon of values."""

    tag = "RadarChart"

    # Key of each row in `data` to read.
    subject_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # The value range along a spoke; `[0, the largest value]`, niced, by default.
    domain: rx.Var[list[int | float]]


radar_chart = RadarChart.create


class PolarBarChart(SilverpointChart):
    """360° bars out from a hole, length ∝ value."""

    tag = "PolarBarChart"

    # Key of each row in `data` to read.
    name_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]


polar_bar_chart = PolarBarChart.create


class RadialArcGroup(SilverpointChart):
    """Concentric 180° tracks, sweep ∝ value / the largest."""

    tag = "RadialArcGroup"

    # Key of each row in `data` to read.
    name_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]


radial_arc_group = RadialArcGroup.create


class RadialRings(SilverpointChart):
    """Concentric progress rings, sweep ∝ value in 0-100."""

    tag = "RadialRings"

    # Key of each row in `data` to read.
    name_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]


radial_rings = RadialRings.create


class GaugeArc(SilverpointChart):
    """A 240° arc swept to a percent."""

    tag = "GaugeArc"

    # 0 to 100; saturated at the ends outside it.
    percent: rx.Var[int | float]

    # Names the measure under the readout.
    caption: rx.Var[str]

    # Printed in place of the percent.
    readout: rx.Var[str]


gauge_arc = GaugeArc.create


class MeterChart(SilverpointChart):
    """A semicircular meter with a needle at a percent."""

    tag = "MeterChart"

    # 0 to 100; saturated at the ends outside it.
    percent: rx.Var[int | float]

    # Names the measure under the readout.
    caption: rx.Var[str]

    # Printed in place of the percent.
    readout: rx.Var[str]


meter_chart = MeterChart.create


class CoxcombChart(SilverpointChart):
    """Equal angles, sector **area** ∝ value."""

    tag = "CoxcombChart"

    # Key of each row in `data` to read.
    name_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Where the first sector starts, in degrees clockwise from 12 o'clock; 0 by default.
    start_angle: rx.Var[int | float]


coxcomb_chart = CoxcombChart.create


class WindRose(SilverpointChart):
    """Observations of (bearing, speed) binned by compass sector and speed."""

    tag = "WindRose"

    # Where the wind blows from, in degrees clockwise from north.
    bearing_key: rx.Var[str]

    # The wind speed; 0 is a calm, which has no direction.
    value_key: rx.Var[str]

    # Compass sectors: 4, 8, 16 or 32; 16 by default.
    sectors: rx.Var[int]

    # Ascending speed thresholds that split each sector; `[5, 10, 15, 20]` by default.
    bins: rx.Var[list[int | float]]


wind_rose = WindRose.create


class VolvelleChart(SilverpointChart):
    """Concentric categorical rings read against one index."""

    tag = "VolvelleChart"

    # Rings shown, from the inside out; all by default.
    rings: rx.Var[int]

    # The ring whose segment is brought under the index, 0-based; 0 by default.
    index_ring: rx.Var[int]

    # The segment of `indexRing` under the index; its first segment by default.
    index_value: rx.Var[str]


volvelle_chart = VolvelleChart.create


class OrbitChart(SilverpointChart):
    """Nested elliptical orbits with markers along them."""

    tag = "OrbitChart"

    # Orbits shown, from the inside out; all by default.
    orbits: rx.Var[int]

    # A row's markers; `'markers'` by default.
    marker_key: rx.Var[str]

    # A marker's period, 0-1 over the cycle; `'period'` by default.
    period_key: rx.Var[str]


orbit_chart = OrbitChart.create


# ── The second catalog (silverpoint 0.6) ─────────────────────────────────────────────────


def _root_id_spec(node_id):
    """The node a click, Enter or Space asked to draw as root.

    Args:
        node_id: The node's id, or null for the data root.

    Returns:
        The id, forwarded unchanged to the backend handler (annotate it ``str | None``).
    """
    return (node_id,)


class _HierarchyChart(SilverpointChart):
    """Props the hierarchy charts share: one row per node, linked to its parent."""

    # Key of each row in `data` to read.
    id_key: rx.Var[str]

    # The parent's id; `null` for the root.
    parent_key: rx.Var[str]

    # Key of each row in `data` to read.
    label_key: rx.Var[str]


class _DrillableChart(_HierarchyChart):
    """A hierarchy chart drilled down under your control, through ``root_id`` and ``on_root_change``."""

    # A node was activated: the id to draw as root, ``None`` for the data root. The chart keeps no
    # root of its own: store the id in state and pass it back as ``root_id``.
    on_root_change: rx.EventHandler[_root_id_spec]


class HistogramChart(SilverpointChart):
    """Raw observations binned in the core."""

    tag = "HistogramChart"

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # A number asks for that many equal-width bins over the niced extent; an array gives the thresholds, increasing.
    # Freedman–Diaconis by default, Sturges when the IQR is 0.
    bins: rx.Var[int | list[int | float]]

    # Turns the counts into a running total.
    cumulative: rx.Var[bool]

    orientation: rx.Var[Literal["columns", "rows"]]


histogram_chart = HistogramChart.create


class EcdfChart(SilverpointChart):
    """The empirical cumulative distribution as a step function."""

    tag = "EcdfChart"

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Two groups at most are drawn.
    group_key: rx.Var[str]

    # Quantiles, in 0-1, drawn as rules.
    markers: rx.Var[list[int | float]]


ecdf_chart = EcdfChart.create


class BoxPlotChart(SilverpointChart):
    """Quartiles, median, Tukey whiskers and outliers per group."""

    tag = "BoxPlotChart"

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Key of each row in `data` to read.
    group_key: rx.Var[str]

    # Whisker reach as a multiple of the IQR; 1.5 by default.
    whisker: rx.Var[int | float]

    # Draws the observations past the whiskers; `true` by default.
    outliers: rx.Var[bool]

    orientation: rx.Var[Literal["columns", "rows"]]


box_plot_chart = BoxPlotChart.create


class ViolinChart(SilverpointChart):
    """A mirrored kernel density per group."""

    tag = "ViolinChart"

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Key of each row in `data` to read.
    group_key: rx.Var[str]

    # Kernel bandwidth in data units, shared by every group; Silverman's rule by default.
    bandwidth: rx.Var[int | float]

    # Marks the quartiles inside each violin; `true` by default.
    quartiles: rx.Var[bool]

    orientation: rx.Var[Literal["columns", "rows"]]


violin_chart = ViolinChart.create


class RidgelineChart(SilverpointChart):
    """A kernel density per group on overlapping baselines."""

    tag = "RidgelineChart"

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # The group of an observation; one ridge per group.
    group_key: rx.Var[str]

    # Kernel bandwidth in data units, shared by every group; Silverman's rule by default.
    bandwidth: rx.Var[int | float]

    # How far a ridge reaches into the one behind it, 0-1; 0.5 by default.
    overlap: rx.Var[int | float]


ridgeline_chart = RidgelineChart.create


class BeeswarmChart(SilverpointChart):
    """One point per observation, packed without overlap."""

    tag = "BeeswarmChart"

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Key of each row in `data` to read.
    group_key: rx.Var[str]

    # Names the point in the readout and the table.
    label_key: rx.Var[str]

    # Point radius in px; 3 by default.
    radius: rx.Var[int | float]


beeswarm_chart = BeeswarmChart.create


class LollipopChart(SilverpointChart):
    """A stem from the baseline and a head at the value."""

    tag = "LollipopChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    orientation: rx.Var[Literal["columns", "rows"]]

    # Order of the categories; `none` keeps the data order.
    sort: rx.Var[Literal["none", "ascending", "descending"]]


lollipop_chart = LollipopChart.create


class DumbbellChart(SilverpointChart):
    """Two values per category joined by a segment."""

    tag = "DumbbellChart"

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # Key of each row in `data` to read.
    start_key: rx.Var[str]

    # Key of each row in `data` to read.
    end_key: rx.Var[str]

    # Titles of the two values; `['start', 'end']` by default.
    names: rx.Var[list[str]]

    # `arrow` encodes the direction from the first value to the second.
    end_marker: rx.Var[Literal["dot", "arrow"]]

    # `rows` by default: long category names read across.
    orientation: rx.Var[Literal["columns", "rows"]]


dumbbell_chart = DumbbellChart.create


class SlopeChart(SilverpointChart):
    """Two period axes, one segment per category."""

    tag = "SlopeChart"

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # Key of each row in `data` to read.
    start_key: rx.Var[str]

    # Key of each row in `data` to read.
    end_key: rx.Var[str]

    # Titles of the two periods; `['start', 'end']` by default.
    names: rx.Var[list[str]]


slope_chart = SlopeChart.create


class BumpChart(SilverpointChart):
    """The rank of each series at each x."""

    tag = "BumpChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    series_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # `descending` gives rank 1 to the highest value (the default).
    order: rx.Var[Literal["descending", "ascending"]]

    # Series drawn, the best-ranked first; all by default.
    series: rx.Var[int]


bump_chart = BumpChart.create


class ErrorBarChart(SilverpointChart):
    """A point estimate with its interval per category."""

    tag = "ErrorBarChart"

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # Key of each row in `data` to read.
    estimate_key: rx.Var[str]

    # Key of each row in `data` to read.
    low_key: rx.Var[str]

    # Key of each row in `data` to read.
    high_key: rx.Var[str]

    # A reference value drawn as a dotted rule.
    reference: rx.Var[int | float]

    # `rows` by default, as a forest plot reads.
    orientation: rx.Var[Literal["columns", "rows"]]


error_bar_chart = ErrorBarChart.create


class IntervalChart(SilverpointChart):
    """Floating bars from start to end on lanes."""

    tag = "IntervalChart"

    # Key of each row in `data` to read.
    lane_key: rx.Var[str]

    # Key of each row in `data` to read.
    start_key: rx.Var[str]

    # Key of each row in `data` to read.
    end_key: rx.Var[str]

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # `date` reads ISO `YYYY-MM-DD` days in UTC; `number` by default.
    axis: rx.Var[Literal["number", "date"]]


interval_chart = IntervalChart.create


class DivergingBarChart(SilverpointChart):
    """Ordered levels stacked on both sides of a neutral centre."""

    tag = "DivergingBarChart"

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # The level columns, most negative first.
    levels: rx.Var[list[str]]

    # Index of the neutral level, split across the centre; `null` for none. The middle one by default.
    neutral: rx.Var[int | None]

    # Normalises each row to 100 %; `true` by default.
    percent: rx.Var[bool]


diverging_bar_chart = DivergingBarChart.create


class ConnectedScatterChart(SilverpointChart):
    """An ordered path through x-y points."""

    tag = "ConnectedScatterChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    y_key: rx.Var[str]

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # Draws direction marks along the path; `true` by default.
    arrows: rx.Var[bool]


connected_scatter_chart = ConnectedScatterChart.create


class WaffleChart(SilverpointChart):
    """A unit grid filled in reading order by category."""

    tag = "WaffleChart"

    # Key of each row in `data` to read.
    name_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    # Cells in the grid; 100 by default.
    cells: rx.Var[int]

    # Cells per row; 10 by default.
    columns: rx.Var[int]


waffle_chart = WaffleChart.create


class MarimekkoChart(SilverpointChart):
    """Column width by total, segment height by share."""

    tag = "MarimekkoChart"

    # Key of each row in `data` to read.
    column_key: rx.Var[str]

    # Key of each row in `data` to read.
    segment_key: rx.Var[str]

    # Key of each row in `data` to read.
    value_key: rx.Var[str]


marimekko_chart = MarimekkoChart.create


class SquarifiedTreemap(_DrillableChart):
    """Nested rectangles, area by value, drillable through `rootId` and `onRootChange`."""

    tag = "SquarifiedTreemap"

    # Read on leaves; an internal node is the sum of its children.
    value_key: rx.Var[str]

    # Levels drawn below the root; all by default.
    depth: rx.Var[int]

    # The node drawn as root, controlled; the data root by default.
    root_id: rx.Var[str | None]


squarified_treemap = SquarifiedTreemap.create


class SunburstChart(_DrillableChart):
    """A hierarchy as rings of arcs, drillable through `rootId` and `onRootChange`."""

    tag = "SunburstChart"

    # Read on leaves; an internal node is the sum of its children.
    value_key: rx.Var[str]

    # Rings drawn below the root; all by default.
    depth: rx.Var[int]

    # The node drawn as root, controlled; the data root by default.
    root_id: rx.Var[str | None]


sunburst_chart = SunburstChart.create


class TreeChart(_HierarchyChart):
    """A tidy node-link tree."""

    tag = "TreeChart"

    # Key of each row in `data` to read.
    value_key: rx.Var[str]

    orientation: rx.Var[Literal["horizontal", "vertical"]]


tree_chart = TreeChart.create


class ParallelCoordinatesChart(SilverpointChart):
    """One polyline per row across parallel axes."""

    tag = "ParallelCoordinatesChart"

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    # The dimension columns, in axis order.
    dimensions: rx.Var[list[str]]

    # Axis domains by dimension; derived from the data when omitted.
    domains: rx.Var[dict[str, list[int | float]]]


parallel_coordinates_chart = ParallelCoordinatesChart.create


class PolarLineChart(SilverpointChart):
    """A line over angle and radius."""

    tag = "PolarLineChart"

    # In the units of `period`.
    angle_key: rx.Var[str]

    # The radius, `≥ 0`.
    value_key: rx.Var[str]

    # One turn, in the units of the angle; when set, the line closes.
    period: rx.Var[int | float]

    # Where the angle 0 sits, in degrees clockwise from 12 o'clock; 0 by default.
    start_angle: rx.Var[int | float]


polar_line_chart = PolarLineChart.create


class PolarScatterChart(SilverpointChart):
    """Points over angle and radius."""

    tag = "PolarScatterChart"

    # In the units of `period`.
    angle_key: rx.Var[str]

    # The radius, `≥ 0`.
    radius_key: rx.Var[str]

    # Key of each row in `data` to read.
    size_key: rx.Var[str]

    # One turn, in the units of the angle; 360 by default.
    period: rx.Var[int | float]


polar_scatter_chart = PolarScatterChart.create


class DensityBinChart(SilverpointChart):
    """X-y points counted in two-dimensional bins."""

    tag = "DensityBinChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    y_key: rx.Var[str]

    bin_shape: rx.Var[Literal["hexagon", "rect"]]

    # Bin size in px; 14 by default.
    bin_size: rx.Var[int | float]


density_bin_chart = DensityBinChart.create


class ContourChart(SilverpointChart):
    """Iso-lines and filled bands of a density or a grid."""

    tag = "ContourChart"

    # `points` estimates a density from a point cloud; `grid` reads a regular grid of values.
    source: rx.Var[Literal["points", "grid"]]

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    y_key: rx.Var[str]

    # The grid value (`source: 'grid'`).
    value_key: rx.Var[str]

    # A count of levels, or the thresholds, increasing: in the grid's values, or as shares of the density's peak.
    levels: rx.Var[int | list[int | float]]

    # Fills the bands between levels; `true` by default.
    filled: rx.Var[bool]


contour_chart = ContourChart.create


class DelaunayChart(SilverpointChart):
    """The triangulation of x-y points, or its Voronoi cells."""

    tag = "DelaunayChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    y_key: rx.Var[str]

    # Key of each row in `data` to read.
    label_key: rx.Var[str]

    mesh: rx.Var[Literal["delaunay", "voronoi"]]


delaunay_chart = DelaunayChart.create


class VectorFieldChart(SilverpointChart):
    """An arrow per grid point."""

    tag = "VectorFieldChart"

    # Key of each row in `data` to read.
    x_key: rx.Var[str]

    # Key of each row in `data` to read.
    y_key: rx.Var[str]

    # Key of each row in `data` to read.
    u_key: rx.Var[str]

    # Key of each row in `data` to read.
    v_key: rx.Var[str]

    # Arrow length per unit of magnitude; fitted to the grid by default.
    scale: rx.Var[int | float]


vector_field_chart = VectorFieldChart.create


class NetworkChart(SilverpointChart):
    """A node-link graph."""

    tag = "NetworkChart"

    # Key of each row in `data` to read.
    source_key: rx.Var[str]

    # Key of each row in `data` to read.
    target_key: rx.Var[str]

    # 1 by default.
    value_key: rx.Var[str]

    # The nodes, as data; the distinct ends of the links by default.
    nodes: rx.Var[list[dict[str, Any]]]

    # Layout iterations; 300 by default.
    iterations: rx.Var[int]


network_chart = NetworkChart.create


def network_node(
    node_id: str,
    *,
    label: str | None = None,
    group: str | None = None,
    x: float | None = None,
    y: float | None = None,
) -> dict[str, Any]:
    """One node of :func:`network_chart`'s ``nodes``.

    With a finite ``x`` and ``y`` on every node the chart draws them there and runs no layout.

    Args:
        node_id: The id the links name in ``source_key`` and ``target_key``.
        label: Printed name; the id by default.
        group: Groups nodes into tones.
        x: Fixed position, in the chart's units.
        y: Fixed position, in the chart's units.

    Returns:
        The node, with only the fields given.
    """
    node: dict[str, Any] = {"id": node_id, "label": label, "group": group, "x": x, "y": y}
    return {key: value for key, value in node.items() if value is not None}
