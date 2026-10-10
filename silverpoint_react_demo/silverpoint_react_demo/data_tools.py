"""Generated and re-rolled data for the demo: the activity grid, and fresh values for every chart."""

import copy
import datetime as dt
import random
from typing import Any

from .datasets import DATASETS, Rows

#: Fields that are positions, sizes of tiles or identifiers, never re-rolled.
_FIXED_FIELDS = {"period", "cols", "rows", "bearing", "level", "month", "season", "year"}

#: Charts whose ``x`` and ``y`` are grid positions, never re-rolled.
_GRID_CHARTS = {"vector-field-chart"}

#: Charts whose values are read on a 0-100 scale.
_PERCENT_CHARTS = {"bullet-chart", "pyramid-chart", "heatmap-chart", "radial-rings"}


def activity_grid(seed: int = 1592, end: dt.date = dt.date(2026, 6, 30), weeks: int = 26) -> Rows:
    """Daily activity counts with their quantised level, as silverpoint's own demo builds them.

    Args:
        seed: Seed of the generator.
        end: Last day shown.
        weeks: Weeks of data.

    Returns:
        One row per day: ``{date, count, level}``.
    """
    rng = random.Random(seed)
    days = weeks * 7
    first = end - dt.timedelta(days=days - 1)
    rows: Rows = []
    for offset in range(days):
        day = first + dt.timedelta(days=offset)
        weekend = day.weekday() >= 5
        r = rng.random()
        count = int(r * r * (5 if weekend else 14))
        level = 0 if count == 0 else 1 if count <= 2 else 2 if count <= 5 else 3 if count <= 9 else 4
        rows.append({"date": day.isoformat(), "count": count, "level": level})
    return rows


def initial_datasets() -> dict[str, Rows]:
    """Every chart's dataset, by slug, ready to go into state.

    Returns:
        A deep copy of the demo datasets plus the generated activity grid.
    """
    data = copy.deepcopy(DATASETS)
    data["activity-grid"] = activity_grid()
    return data


def _jitter(value: Any, rng: random.Random, ceiling: float | None) -> Any:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return value
    if value == 0:
        return value
    factor = rng.uniform(0.7, 1.3)
    new = value * factor
    if ceiling is not None:
        new = min(new, ceiling)
    if isinstance(value, int):
        return max(1, round(new)) if value > 0 else min(-1, round(new))
    return round(new, 2)


def _candles(rng: random.Random, labels: list[str]) -> Rows:
    price = rng.uniform(95, 110)
    rows: Rows = []
    for label in labels:
        open_ = price
        close = max(50.0, open_ + rng.uniform(-6, 6))
        high = max(open_, close) + rng.uniform(0.5, 4)
        low = min(open_, close) - rng.uniform(0.5, 4)
        rows.append(
            {"time": label, "open": round(open_), "high": round(high), "low": round(low), "close": round(close)}
        )
        price = close
    return rows


def _waterfall(rng: random.Random, rows: Rows) -> Rows:
    running = 0.0
    out: Rows = []
    for index, row in enumerate(rows):
        if "base" in row and index == 0:
            running = round(row["base"] * rng.uniform(0.8, 1.2))
            out.append({"step": row["step"], "base": running})
        elif "base" in row:
            out.append({"step": row["step"], "base": round(running)})
        else:
            delta = _jitter(row["delta"], rng, None)
            running += delta
            out.append({"step": row["step"], "delta": delta})
    return out


def reroll(slug: str, rows: Rows, rng: random.Random) -> Rows:
    """Fresh values for one chart, keeping its shape and labels.

    Args:
        slug: The chart's slug.
        rows: Its current rows.
        rng: Random generator.

    Returns:
        New rows.
    """
    if slug == "activity-grid":
        return activity_grid(seed=rng.randrange(1, 10_000))
    if slug == "candlestick-chart":
        return _candles(rng, [row["time"] for row in rows])
    if slug == "waterfall-chart":
        return _waterfall(rng, rows)
    if slug == "wind-rose":
        return [{"bearing": row["bearing"], "speed": _jitter(row["speed"], rng, None)} for row in rows]
    if slug == "volvelle-chart":
        return copy.deepcopy(rows)
    ceiling = 100 if slug in _PERCENT_CHARTS else None
    fixed = _FIXED_FIELDS | {"x", "y"} if slug in _GRID_CHARTS else _FIXED_FIELDS
    fresh: Rows = []
    for row in rows:
        new: dict[str, Any] = {}
        for key, value in row.items():
            if key in fixed:
                new[key] = value
            elif isinstance(value, list):
                new[key] = [
                    {k: v if k in _FIXED_FIELDS else _jitter(v, rng, ceiling) for k, v in item.items()}
                    if isinstance(item, dict)
                    else _jitter(item, rng, ceiling)
                    for item in value
                ]
            else:
                new[key] = _jitter(value, rng, ceiling)
        fresh.append(new)
    if slug == "range-band-chart":
        for row in fresh:
            row["low"], row["high"] = min(row["low"], row["high"]), max(row["low"], row["high"])
    if slug == "error-bar-chart":
        for row in fresh:
            row["low"], row["effect"], row["high"] = sorted((row["low"], row["effect"], row["high"]))
    return fresh


def drill_path(rows: Rows, node_id: str | None) -> list[str]:
    """The names from the root of a hierarchy down to one node: the breadcrumb of a drill-down.

    Args:
        rows: The hierarchy, one row per node with ``id``, ``parent`` and ``name``.
        node_id: The node drawn as root; ``None`` (or an unknown id) for the data root.

    Returns:
        The names, the data root first.
    """
    by_id = {row["id"]: row for row in rows}
    names: list[str] = []
    row = by_id.get(node_id) if node_id is not None else None
    while row is not None:
        names.append(row["name"])
        row = by_id.get(row["parent"]) if row["parent"] is not None else None
    if not names:
        names = [next(row["name"] for row in rows if row["parent"] is None)]
    return names[::-1]
