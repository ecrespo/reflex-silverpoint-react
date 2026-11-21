"""#50: an overlay's string trigger follows ``silverpoint_provider``.

A string in ``trigger=`` became ``sp_trigger(...)``, our own button, which reads no provider: under a
cyanotype provider it kept the silverpoint ground (dark text on blue). Since silverpoint 0.11.0
(delta-014) the npm ``SpButton`` keeps the ARIA and the press handlers an overlay clones onto its
trigger, and it reads the provider, so a string trigger is an ``sp_button``. An explicit
``sp_trigger(...)`` is unchanged.
"""

import re

import pytest
import reflex as rx
import reflex_silverpoint_react as sp


class _S(rx.State):
    flag: bool = False
    text: str = "Open"

    @rx.event
    def set_flag(self, value: bool):
        self.flag = value


OVERLAYS = {
    "modal": lambda trigger, **kw: sp.sp_modal("Body", trigger=trigger, title="T", **kw),
    "drawer": lambda trigger, **kw: sp.sp_drawer("Body", trigger=trigger, title="T", **kw),
    "popover": lambda trigger, **kw: sp.sp_popover("Body", trigger=trigger, **kw),
    "tooltip": lambda trigger, **kw: sp.sp_tooltip(trigger, "tip", **kw),
}


def _trigger(overlay: rx.Component) -> tuple[str, set[str]]:
    """The trigger the overlay renders: its tag and the names of the props it is given."""
    props = dict(prop.split(":", 1) for prop in overlay.render()["props"])
    match = re.match(r"\(jsx\((\w+), \(\{(.*?)\}\)", props["trigger"], re.DOTALL)
    assert match, props["trigger"]
    given = set(re.findall(r"(?:^|,)(\w+):", match[2]))
    return match[1], given


@pytest.mark.parametrize("kind", OVERLAYS)
def test_a_string_trigger_is_an_sp_button(kind: str) -> None:
    tag, _ = _trigger(OVERLAYS[kind]("Acknowledge an incident"))
    assert tag == "SpButton"


@pytest.mark.parametrize("kind", OVERLAYS)
def test_a_string_trigger_sets_no_ground_of_its_own(kind: str) -> None:
    """Without ``ground`` / ``palette`` on the overlay, the button leaves them to the provider."""
    _, given = _trigger(OVERLAYS[kind]("Open"))
    assert not {"ground", "substrate", "mode", "palette"} & given


@pytest.mark.parametrize("kind", OVERLAYS)
def test_a_string_trigger_still_takes_the_overlays_common_props(kind: str) -> None:
    """The issue's workaround keeps working: the overlay's own ground and palette reach the button."""
    overlay = OVERLAYS[kind]("Open", ground="cyanotype", palette="sanguine")
    _, given = _trigger(overlay)
    assert {"ground", "palette"} <= given
    assert 'ground:"cyanotype"' in dict(p.split(":", 1) for p in overlay.render()["props"])["trigger"]


def test_a_controlled_modal_with_a_string_trigger_imports_sp_button() -> None:
    """#44 stays fixed: the trigger is an npm import, not custom code of the page."""
    modal = sp.sp_modal("Body", trigger="Edit order", title="T", open=_S.flag, on_open_change=_S.set_flag)
    assert ("SpButton", "/ui") in {
        (var.tag, var.package_path) for var in modal._get_all_imports()[sp.SILVERPOINT_LIBRARY]
    }
    assert not modal._get_all_custom_code()


def test_a_state_var_trigger_is_an_sp_button() -> None:
    assert _trigger(sp.sp_modal("Body", trigger=_S.text, title="T"))[0] == "SpButton"


def test_an_explicit_sp_trigger_is_kept() -> None:
    assert _trigger(sp.sp_modal("Body", trigger=sp.sp_trigger("Edit"), title="T"))[0] == "SilverpointTrigger"
