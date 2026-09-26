"""The 33 silverpoint charts as Reflex components.

Generated from the silverpoint API reference (``docs/site/generated/props.json``) and then
kept by hand. Every class wraps the client component of the same name exported by
``@silverpoint/react``; every chart also takes the props of :class:`SilverpointChart`.
"""

from typing import Literal

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
