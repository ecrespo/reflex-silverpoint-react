"""The demo's data: every chart has a dataset its key props can read, and a re-roll keeps it valid."""

import random
import sys
from pathlib import Path

import pytest
import reflex_silverpoint_react as sp

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "silverpoint_react_demo"))

from silverpoint_react_demo.data_tools import initial_datasets, reroll
from silverpoint_react_demo.datasets import KEY_PROPS

#: Charts fed from scalar state instead of rows.
SCALAR_CHARTS = {"gauge-arc", "meter-chart"}

#: The slugs of the charts new in silverpoint 0.6.
NEW_IN_0_6 = [
    "histogram-chart", "ecdf-chart", "box-plot-chart", "violin-chart", "ridgeline-chart", "beeswarm-chart",
    "lollipop-chart", "dumbbell-chart", "slope-chart", "bump-chart", "error-bar-chart", "interval-chart",
    "diverging-bar-chart", "connected-scatter-chart", "waffle-chart", "marimekko-chart", "squarified-treemap",
    "sunburst-chart", "tree-chart", "parallel-coordinates-chart", "polar-line-chart", "polar-scatter-chart",
    "density-bin-chart", "contour-chart", "delaunay-chart", "vector-field-chart", "network-chart",
]  # fmt: skip


def test_every_chart_has_a_dataset() -> None:
    datasets = initial_datasets()
    missing = {info.slug for info in sp.CHARTS} - SCALAR_CHARTS - set(datasets)
    assert not missing


@pytest.mark.parametrize("slug", NEW_IN_0_6)
def test_new_charts_name_fields_their_rows_have(slug: str) -> None:
    rows = initial_datasets()[slug]
    keys = KEY_PROPS[slug]
    assert rows, slug
    fields = set().union(*(row.keys() for row in rows))
    for prop, value in keys.items():
        if prop.endswith("_key"):
            assert value in fields, f"{slug}: {prop}={value!r} not in its rows"
    for column in [*keys.get("levels", []), *keys.get("dimensions", [])]:
        assert column in fields, f"{slug}: column {column!r} not in its rows"


def test_new_charts_render_with_their_dataset() -> None:
    datasets = initial_datasets()
    for slug in NEW_IN_0_6:
        info = sp.chart_by_slug(slug)
        component = info.factory(data=datasets[slug], **KEY_PROPS[slug])
        assert component.render()["name"] == info.chart


@pytest.mark.parametrize("seed", range(5))
def test_reroll_keeps_the_0_6_invariants(seed: int) -> None:
    rng = random.Random(seed)
    data = {slug: reroll(slug, rows, rng) for slug, rows in initial_datasets().items()}
    original = initial_datasets()

    for row in data["interval-chart"]:
        assert row["from"] <= row["to"]
    for row in data["error-bar-chart"]:
        assert row["low"] <= row["effect"] <= row["high"]
    for slug in ("squarified-treemap", "sunburst-chart", "tree-chart"):
        assert [(r["id"], r["parent"]) for r in data[slug]] == [(r["id"], r["parent"]) for r in original[slug]]
    assert [(r["x"], r["y"]) for r in data["vector-field-chart"]] == [
        (r["x"], r["y"]) for r in original["vector-field-chart"]
    ]
    for slug, field in (("polar-line-chart", "month"), ("bump-chart", "season"), ("connected-scatter-chart", "year")):
        assert [r[field] for r in data[slug]] == [r[field] for r in original[slug]], slug


def test_drill_path_names_the_nodes_from_the_root() -> None:
    from silverpoint_react_demo.data_tools import drill_path
    from silverpoint_react_demo.datasets import BUDGET

    root = next(row for row in BUDGET if row["parent"] is None)
    leaf = next(row for row in BUDGET if row.get("amount") is not None)
    parent = next(row for row in BUDGET if row["id"] == leaf["parent"])

    assert drill_path(BUDGET, None) == [root["name"]]
    assert drill_path(BUDGET, parent["id"])[-1] == parent["name"]
    assert drill_path(BUDGET, parent["id"])[0] == root["name"]
    assert drill_path(BUDGET, "no-such-node") == [root["name"]]
