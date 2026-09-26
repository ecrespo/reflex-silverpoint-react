"""State of the demo app."""

import json
import random
from typing import Any

import reflex as rx
from reflex_silverpoint_react import CHARTS

from .data_tools import initial_datasets, reroll
from .datasets import VOLVELLE_CHART

SIZES: dict[str, tuple[int, int]] = {"sm": (240, 120), "md": (320, 150), "lg": (640, 300)}


def _describe(item: dict[str, Any] | None) -> str:
    if not item:
        return "—"
    datum = item.get("datum") or {}
    fields = ", ".join(f"{key}: {value}" for key, value in datum.items() if not isinstance(value, (list, dict)))
    return f"{item.get('seriesKey', '')} #{item.get('index', 0)} = {item.get('value')}  ({fields})"


class DemoState(rx.State):
    """Controls shared by the gallery, the playground and the interaction page."""

    # Ground settings applied through silverpoint_provider.
    substrate: str = "cream"
    mode: str = "ink"
    hatch_fill: str = "tile"

    # Where the gallery takes its data from: the charts' own demo datasets, or Python state.
    use_state_data: bool = False
    datasets: dict[str, list[dict[str, Any]]] = initial_datasets()
    rolls: int = 0

    # Scalar charts.
    gauge_percent: int = 72
    meter_percent: int = 58
    kpi_delta: float = 8.2

    @rx.event
    def set_substrate(self, value: str):
        self.substrate = value

    @rx.event
    def set_mode(self, value: str):
        self.mode = value

    @rx.event
    def set_hatch_fill(self, value: str):
        self.hatch_fill = value

    @rx.event
    def set_use_state_data(self, value: bool):
        self.use_state_data = value

    @rx.event
    def reroll_all(self):
        """Fresh values for every chart; switches the gallery to state data."""
        rng = random.Random()
        self.datasets = {slug: reroll(slug, rows, rng) for slug, rows in self.datasets.items()}
        self.gauge_percent = rng.randint(5, 98)
        self.meter_percent = rng.randint(5, 98)
        self.kpi_delta = round(rng.uniform(-12, 12), 1)
        self.use_state_data = True
        self.rolls += 1

    @rx.event
    def reset_data(self):
        self.datasets = initial_datasets()
        self.gauge_percent = 72
        self.meter_percent = 58
        self.kpi_delta = 8.2
        self.rolls = 0

    @rx.event
    def set_gauge_percent(self, value: list[int | float]):
        self.gauge_percent = int(value[0])

    @rx.event
    def set_meter_percent(self, value: list[int | float]):
        self.meter_percent = int(value[0])


class InteractionState(rx.State):
    """Events coming back from the charts."""

    active: str = "—"
    selections: list[str] = []
    svg_report: str = "Not exported yet."
    geometry_report: str = "Not read yet."

    # Volvelle: which ring and segment sit under the index.
    volvelle_ring: int = 0
    volvelle_value: str = "Mon"

    # A live KPI series.
    kpi_series: list[dict[str, Any]] = [
        {"value": v} for v in (118, 124, 121, 132, 140, 136, 129, 142, 151, 147, 155, 162, 158, 171)
    ]

    @rx.event
    def on_active(self, item: dict[str, Any] | None):
        self.active = _describe(item)

    @rx.event
    def on_select(self, item: dict[str, Any]):
        self.selections = [_describe(item), *self.selections][:6]

    @rx.event
    def clear_selections(self):
        self.selections = []

    @rx.event
    def receive_svg(self, svg: str | None):
        if not svg:
            self.svg_report = "No chart answered (is the id right?)."
            return
        self.svg_report = f"Received {len(svg):,} characters of standalone SVG; it starts with {svg[:48]!r}…"

    @rx.event
    def receive_geometry(self, geometry: dict[str, Any] | None):
        if not geometry:
            self.geometry_report = "No geometry."
            return
        summary = {
            key: (f"{len(value)} items" if isinstance(value, list) else "…" if isinstance(value, dict) else value)
            for key, value in geometry.items()
        }
        self.geometry_report = json.dumps(summary)[:400]

    @rx.event
    def volvelle_select(self, item: dict[str, Any]):
        datum = item.get("datum") or {}
        labels = [row["label"] for row in VOLVELLE_CHART]
        ring = datum.get("ring")
        if ring in labels:
            self.volvelle_ring = labels.index(ring)
            self.volvelle_value = str(datum.get("segment", ""))

    @rx.event
    def tick_kpi(self):
        last = self.kpi_series[-1]["value"]
        self.kpi_series = [*self.kpi_series[1:], {"value": max(60, last + random.randint(-14, 16))}]

    @rx.var
    def kpi_delta(self) -> float:
        first, last = self.kpi_series[0]["value"], self.kpi_series[-1]["value"]
        return round((last - first) / first * 100, 1)


class PlaygroundState(rx.State):
    """The ground playground: one chart, every rendering choice."""

    chart: str = "LineChart"
    substrate: str = "cream"
    mode: str = "ink"
    hatch_fill: str = "tile"
    chrome: str = "card"
    data_table: str = "hidden"
    size: str = "md"
    seed: int = 1592

    @rx.event
    def set_chart(self, value: str):
        self.chart = value

    @rx.event
    def set_substrate(self, value: str):
        self.substrate = value

    @rx.event
    def set_mode(self, value: str):
        self.mode = value

    @rx.event
    def set_hatch_fill(self, value: str):
        self.hatch_fill = value

    @rx.event
    def set_chrome(self, value: str):
        self.chrome = value

    @rx.event
    def set_data_table(self, value: str):
        self.data_table = value

    @rx.event
    def set_size(self, value: str):
        self.size = value

    @rx.event
    def set_seed(self, value: float | str):
        try:
            self.seed = int(float(value))
        except ValueError:
            self.seed = 0

    @rx.event
    def new_seed(self):
        self.seed = random.randint(1, 99_999)

    @rx.var
    def width(self) -> int:
        return SIZES.get(self.size, SIZES["md"])[0]

    @rx.var
    def height(self) -> int:
        return SIZES.get(self.size, SIZES["md"])[1]

    @rx.var
    def code(self) -> str:
        info = next((c for c in CHARTS if c.chart == self.chart), CHARTS[0])
        width, height = SIZES.get(self.size, SIZES["md"])
        return (
            f"from reflex_silverpoint_react import {info.factory_name}\n\n"
            f"{info.factory_name}(\n"
            f"    title={info.chart!r},\n"
            f"    substrate={self.substrate!r},\n"
            f"    mode={self.mode!r},\n"
            f"    hatch_fill={self.hatch_fill!r},\n"
            f"    chrome={self.chrome!r},\n"
            f"    data_table={self.data_table!r},\n"
            f"    seed={self.seed},\n"
            f"    width={width},\n"
            f"    height={height},\n"
            f"    # data=...  (omitted: the chart draws its demo dataset)\n"
            f")"
        )
