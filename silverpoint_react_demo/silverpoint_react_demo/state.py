"""State of the demo app."""

import json
import random
from typing import Any

import reflex as rx
from reflex_silverpoint_react import CHARTS

from .data_tools import initial_datasets, reroll
from .datasets import OPS_HOURLY, VOLVELLE_CHART

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
    ground: str = "silverpoint"
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
    def set_ground(self, value: str):
        self.ground = value

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
    ground: str = "silverpoint"
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
    def set_ground(self, value: str):
        self.ground = value

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
            f"    ground={self.ground!r},\n"
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


class DashboardState(rx.State):
    """The dashboard page: ground settings, layout, live data and the linked value."""

    ground: str = "silverpoint"
    substrate: str = "cream"
    mode: str = "ink"
    lg_columns: str = "4"

    ops: list[dict[str, Any]] = [dict(row) for row in OPS_HOURLY]
    uptime: int = 99
    capacity: int = 64

    # The latest linked value, from on_link_change.
    linked: str = "—"
    link_changes: int = 0
    pair_linked: str = "—"

    @rx.event
    def set_ground(self, value: str):
        self.ground = value

    @rx.event
    def set_substrate(self, value: str):
        self.substrate = value

    @rx.event
    def set_mode(self, value: str):
        self.mode = value

    @rx.event
    def set_lg_columns(self, value: str):
        self.lg_columns = value

    @rx.event
    def on_link(self, link: dict[str, Any] | None):
        self.link_changes += 1
        self.linked = f"{link['key']} = {link['value']}" if link else "— (cleared)"

    @rx.event
    def on_pair_link(self, link: dict[str, Any] | None):
        self.pair_linked = f"{link['key']} = {link['value']}" if link else "— (cleared)"

    @rx.event
    def reroll(self):
        """A new day of traffic, drawn from the backend."""
        rng = random.Random()
        rows = []
        for row in OPS_HOURLY:
            hits = max(5, int(row["hits"] * rng.uniform(0.6, 1.4)))
            p50 = int(row["p50"] * rng.uniform(0.85, 1.15))
            rows.append(
                {
                    "hour": row["hour"],
                    "hits": hits,
                    "errors": max(0, int(hits * rng.uniform(0.03, 0.16))),
                    "p50": p50,
                    "p95": int(p50 * rng.uniform(1.5, 2.3)),
                    "load": min(100, int(hits * rng.uniform(0.9, 1.2))),
                }
            )
        self.ops = rows
        self.uptime = rng.randint(94, 100)
        self.capacity = rng.randint(30, 95)

    @rx.var
    def columns(self) -> dict[str, int]:
        """Columns per breakpoint: one on phones, two on tablets, the chosen number on wide screens."""
        return {"sm": 1, "md": 2, "lg": int(self.lg_columns)}

    @rx.var
    def lg_columns_int(self) -> int:
        return int(self.lg_columns)

    @rx.var
    def total_hits(self) -> int:
        return sum(row["hits"] for row in self.ops)

    @rx.var
    def total_errors(self) -> int:
        return sum(row["errors"] for row in self.ops)


TAGS = ["draft", "review", "silverpoint", "cyanotype"]
RELEASE_STEPS = ["Install", "Import", "Configure", "Publish"]


class UiState(rx.State):
    """The UI components page: controlled components bound to Python, and what they report."""

    # The panel's look, itself set by UI components.
    ground: str = "silverpoint"
    substrate: str = "cream"
    precision: bool = False
    size: str = "md"

    # A settings form: every component controlled from here.
    city: str = "Caracas"
    newsletter: bool = True
    quality: int = 3
    volume: int = 30
    series: str = "hits"
    view: str = "traffic"

    # Components driven by buttons.
    tags: list[str] = list(TAGS)
    alert_open: bool = True
    progress: int = 40
    step: int = 1
    inbox: int = 12

    # What the components reported, latest first, and the last native form submission.
    events: list[str] = []
    submitted: str = "—"

    def _log(self, text: str):
        self.events = [text, *self.events][:8]

    @rx.event
    def set_ground(self, value: str):
        self.ground = value
        self._log(f"radio_group on_change → {value!r}")

    @rx.event
    def set_substrate(self, value: str):
        self.substrate = value
        self._log(f"segmented on_change → {value!r}")

    @rx.event
    def set_precision(self, value: bool):
        self.precision = value
        self._log(f"switch on_change → {value!r}")

    @rx.event
    def set_size(self, value: str):
        self.size = value
        self._log(f"segmented on_change → {value!r}")

    @rx.event
    def set_city(self, value: str):
        self.city = value

    @rx.event
    def set_newsletter(self, value: bool):
        self.newsletter = value
        self._log(f"checkbox on_change → {value!r}")

    @rx.event
    def set_quality(self, value: float):
        self.quality = int(value)
        self._log(f"rate on_change → {int(value)}")

    @rx.event
    def set_volume(self, value: float):
        self.volume = int(value)

    @rx.event
    def set_series(self, value: str):
        self.series = value
        self._log(f"segmented on_change → {value!r}")

    @rx.event
    def set_view(self, value: str):
        self.view = value
        self._log(f"tabs on_change → {value!r}")

    @rx.event
    def remove_tag(self, tag: str):
        self.tags = [t for t in self.tags if t != tag]
        self._log(f"tag on_close → {tag!r}")

    @rx.event
    def reset_tags(self):
        self.tags = list(TAGS)

    @rx.event
    def close_alert(self):
        self.alert_open = False
        self._log("alert on_close")

    @rx.event
    def open_alert(self):
        self.alert_open = True

    @rx.event
    def advance(self):
        self.progress = min(100, self.progress + 20)

    @rx.event
    def restart(self):
        self.progress = 0

    @rx.event
    def next_step(self):
        self.step = min(len(RELEASE_STEPS) - 1, self.step + 1)

    @rx.event
    def previous_step(self):
        self.step = max(0, self.step - 1)

    @rx.event
    def receive(self):
        self.inbox += 1

    @rx.event
    def read_all(self):
        self.inbox = 0

    @rx.event
    def submit(self, form: dict[str, Any]):
        """A native form submit: the components' inputs submit under their ``name``."""
        # Reflex also reports the inputs by their id (``form_city``…); keep what the browser submits.
        native = {key: value for key, value in form.items() if not key.startswith("form_")}
        self.submitted = json.dumps(native, ensure_ascii=False)
        self._log("form on_submit")

    @rx.var
    def mode(self) -> str:
        return "precision" if self.precision else "ink"

    @rx.var
    def city_invalid(self) -> bool:
        return not self.city.strip()

    @rx.var
    def city_message(self) -> str:
        return "Required: pick a city" if not self.city.strip() else f"{len(self.city)} characters"

    @rx.var
    def progress_label(self) -> str:
        return "Done" if self.progress >= 100 else "Upload"

    @rx.var
    def release_items(self) -> list[dict[str, str]]:
        return [{"key": title.lower(), "title": title} for title in RELEASE_STEPS]
