# Grounds and palettes

**Contents:** [Grounds](#grounds) · [Palettes](#palettes) · [Presets](#presets)

## Grounds

- `ground="silverpoint"` (the default): a fine line on a prepared paper, tone built from hatch
  density, white heightening on the live value. Substrates: `cream` (default), `green`, `blue`,
  `ochre`.
- `ground="cyanotype"`: a white line on Prussian blue, tone as the weight of an exact line; nothing
  is hatched. Its one substrate is `prussian`, whatever substrate a chart names.
- `mode="precision"` turns the hand-inking off (`ink` is the default). `prefers-contrast: more` and
  `forced-colors: active` force it, and no prop overrides that.
- `hatch_fill="per-shape"` hatches each shape on its own: much heavier markup. Keep the default
  `tile`, except for a single hero chart.

Set them on a chart, on a dashboard, or once for a subtree with `silverpoint_provider(...)`. The
provider's props can be state vars, so one control can re-ground a whole page:

```python
import reflex as rx
from reflex_silverpoint_react import bar_chart, donut_chart, silverpoint_provider


class State(rx.State):
    ground: str = "silverpoint"

    @rx.event
    def set_ground(self, value: str):
        self.ground = value


def section() -> rx.Component:
    return silverpoint_provider(
        bar_chart(title="Units sold", id="units"),
        donut_chart(title="Sales by channel", id="channels"),
        ground=State.ground,
        substrate="green",
        locale="en-GB",
    )
```

## Palettes

silverpoint writes no colour into its drawing: every stroke and fill is painted by CSS through the
ground's `--sp-` custom properties, and a palette sets them, so it re-colours without re-rendering.

- `palette=` takes a preset's **name** (`"sanguine"`), a `Palette`, a dict of fields (snake_case,
  `{"ink": "#2C6355"}`) or a state var holding one. It works on every chart, component, dashboard,
  the timeline and the provider. (The JavaScript API takes palette objects, never names; Python is
  the exception.)
- Fields: `substrate`, `ink`, `ink_secondary`, `heighten`, `rule`, `grid`, `text`, `text_muted` and
  `focus` (the UI focus ring). Unset fields keep the ground's own.
- Palettes merge field by field, element → dashboard → provider: an element's own field wins.
- **Monochrome by design:** a chart has two inks, `ink` for the main series and `ink_secondary` for
  the second. Categories differ by hatch density, never by a colour per series.
- `check_palette(palette)` lists the contrast pairs that fail (`[]` when every one passes), against
  the core's thresholds; `contrast_ratio(a, b)` measures one pair. `palette_css(palette)` returns the
  `--sp-` declarations as a style dict, for your own markup.
- `silverpoint_palette(*children, palette=...)` colours a whole section: it is a provider with a
  palette.

```python
import reflex as rx
from reflex_silverpoint_react import Palette, bar_chart, check_palette, silverpoint_palette, sp_button

MINE = Palette(substrate="#F2E8DC", ink="#8A3A24", ink_secondary="#6A4A3A", text="#4A2216")
PROBLEMS = check_palette(MINE)


class State(rx.State):
    palette: dict[str, str] = {"ink": "#2C6355"}


def coloured() -> rx.Component:
    return rx.el.div(
        bar_chart(title="Orders", palette="sanguine", id="orders"),
        sp_button("Save", variant="primary", palette=State.palette),
        silverpoint_palette(bar_chart(title="Returns", id="returns"), palette=MINE),
    )
```

## Presets

Six presets named after drawing media, `PALETTES[name]` (fields by their Python names):

<!-- generated:palette-presets -->
