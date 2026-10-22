# Overlays

**Contents:** [Triggers](#triggers) · [Open state](#open-state) · [Examples](#examples) · [Reference](#reference)

`sp_modal`, `sp_drawer`, `sp_popover`, `sp_tooltip`, `sp_select`, `sp_dropdown_menu`, `sp_toast` and
`sp_toaster`: the npm overlays of `@silverpoint/react/ui`. Behaviour is the platform's: `showModal()`
for the modal and the drawer (focus stays inside; Escape and the backdrop close them unless
`dismissible=False`), the Popover API for the rest (light dismiss), keyboard and placement from
`@silverpoint/core`. They render in place, in the top layer with no portal, so a section's palette
reaches them, and they read `silverpoint_provider`.

## Triggers

An overlay clones its `trigger` with its ARIA (`aria-expanded`, `aria-controls`) and a toggling
click, so the trigger must keep the props it is given:

- `trigger="Open"`: a string becomes `sp_trigger("Open")`, the drawn button made for this.
- `trigger=sp_trigger("Open", variant="primary")`: the same, with its own props.
- `trigger=rx.el.button("Open", type="button")`: a native button.
- **Never `trigger=sp_button(...)`**: `SpButton` drops the props it is given, so the overlay loses its
  ARIA and its click (silverpoint REQ-547, delta-014).

`sp_trigger` does not read the provider: pass it `ground`, `substrate`, `mode` and `palette` when the
section sets them. `sp_tooltip(trigger, content)` takes its trigger first and text only; for markup,
use `sp_popover`. `sp_dropdown_menu("Actions", items)` draws its own button from a string.

Sides are logical (`side="start"`/`"end"`, `position="bottom-end"`) and mirror in right-to-left
text; `left` and `right` still work with a `DeprecationWarning`.

## Open state

Uncontrolled, an overlay opens from its trigger and closes itself. Controlled, `open=State.flag` with
`on_open_change=State.set_flag` (it receives the new state, a bool); close it from Python by setting
the field. `default_open=True` opens it once, uncontrolled.

## Examples

A modal controlled from state, whose footer confirms:

```python
import reflex as rx
from reflex_silverpoint_react import sp_modal, sp_trigger


class State(rx.State):
    modal_open: bool = False
    applied: int = 0

    @rx.event
    def set_modal_open(self, value: bool):
        self.modal_open = value

    @rx.event
    def confirm(self):
        self.applied += 1
        self.modal_open = False


def apply_dialog() -> rx.Component:
    return sp_modal(
        rx.el.p("Apply the new ground to every chart of the dashboard?"),
        trigger="Apply changes",
        title="Apply changes",
        description="The drawing is re-inked; the data does not change.",
        footer=rx.el.div(
            sp_trigger("Cancel", on_click=State.set_modal_open(False)),
            sp_trigger("Apply", variant="primary", on_click=State.confirm),
        ),
        open=State.modal_open,
        on_open_change=State.set_modal_open,
        id="apply-modal",
    )
```

A drawer, a popover and a tooltip, uncontrolled:

```python
import reflex as rx
from reflex_silverpoint_react import sp_drawer, sp_popover, sp_tooltip, sp_trigger


def panels() -> rx.Component:
    return rx.el.div(
        sp_drawer(rx.el.p("Settings go here."), trigger="Settings", title="Settings", side="end", id="settings"),
        sp_popover(
            rx.el.p("Silverpoint cannot be erased."),
            trigger=sp_trigger("A note"),
            title="A note",
            closable=True,
            id="note",
        ),
        sp_tooltip(rx.el.button("Hover or focus me", type="button"), "Tooltips use the control frame"),
    )
```

A select, a menu and a toast:

```python
import reflex as rx
from reflex_silverpoint_react import sp_dropdown_menu, sp_select, sp_toast, sp_toaster

MENU = [
    {"key": "edit", "label": "Edit", "shortcut": "E"},
    {"type": "separator"},
    {"key": "delete", "label": "Delete", "danger": True},
]


class State(rx.State):
    region: str = "North"
    toast_open: bool = False
    last: str = ""

    @rx.event
    def set_region(self, value: str):
        self.region = value
        self.toast_open = True

    @rx.event
    def set_toast_open(self, value: bool):
        self.toast_open = value

    @rx.event
    def menu(self, key: str):
        self.last = key


def controls() -> rx.Component:
    return rx.el.div(
        sp_select(["North", "East", "South", "West"], value=State.region, on_change=State.set_region, label="Region"),
        sp_dropdown_menu("Actions", MENU, on_select=State.menu),
        sp_toaster(
            sp_toast(
                "Saved",
                "Region changed.",
                kind="success",
                open=State.toast_open,
                on_open_change=State.set_toast_open,
            )
        ),
    )
```

## Reference

<!-- generated:overlays -->
