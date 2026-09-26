"""Page frame and small building blocks of the demo."""

from collections.abc import Callable
from typing import Any

import reflex as rx

NAV = [
    ("/", "Start"),
    ("/gallery", "Gallery"),
    ("/playground", "Playground"),
    ("/interaction", "Interaction"),
    ("/dashboard", "Dashboard"),
    ("/chart/line-chart", "Chart reference"),
]


def page(*children: rx.Component) -> rx.Component:
    """The frame every page shares.

    Args:
        *children: The page content.

    Returns:
        The page.
    """
    return rx.el.div(
        rx.el.header(
            rx.el.p(
                rx.el.a("silverpoint", href="/"),
                rx.el.small("for Reflex"),
                class_name="sp-brand",
            ),
            rx.el.nav(*[rx.el.a(label, href=href) for href, label in NAV], class_name="sp-nav"),
            class_name="sp-header",
        ),
        rx.el.main(*children, class_name="sp-main"),
        rx.el.footer(
            rx.el.p(
                "reflex-silverpoint-react wraps ",
                rx.el.a("@silverpoint/react", href="https://github.com/ecrespo/silverpoint"),
                ". MIT · Typeface: EB Garamond, SIL Open Font License.",
            ),
            class_name="sp-footer",
        ),
        class_name="sp-demo",
    )


def card(*children: rx.Component, **props: Any) -> rx.Component:
    """A white card on the paper.

    Args:
        *children: Content.
        **props: Extra props.

    Returns:
        The card.
    """
    class_name = " ".join(filter(None, ["sp-card", props.pop("class_name", "")]))
    return rx.el.div(*children, class_name=class_name, **props)


def code(text: str | rx.Var) -> rx.Component:
    """A block of code.

    Args:
        text: The code.

    Returns:
        The block.
    """
    return rx.el.pre(rx.el.code(text), class_name="sp-code")


def select(label: str, value: rx.Var, options: list[str], on_change: Callable[..., Any]) -> rx.Component:
    """A labelled native select.

    Args:
        label: Its label.
        value: The current value.
        options: The choices.
        on_change: Handler receiving the new value.

    Returns:
        The control.
    """
    control_id = "ctl-" + label.lower().replace(" ", "-")
    return rx.el.div(
        rx.el.label(label, html_for=control_id),
        rx.el.select(
            *[rx.el.option(option, value=option) for option in options],
            id=control_id,
            value=value,
            on_change=on_change,
        ),
        class_name="sp-control",
    )


def button(text: str, **props: Any) -> rx.Component:
    """A plain button in the page's style.

    Args:
        text: Its label.
        **props: Event triggers and other props.

    Returns:
        The button.
    """
    return rx.el.button(text, class_name="sp-button", type="button", **props)
