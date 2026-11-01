"""The deck page (0.9): Marp/Marpit decks drawn in silverpoint with ``sp_deck``.

/deck   The showcase deck (assets/decks/showcase.md, read at compile time) driven from Python:
        controlled ``page``, buttons outside the deck, toggles, a live readout and an event log;
        a live Markdown editor beside a second deck; and an authoring cheat sheet.
"""

from pathlib import Path

import reflex as rx
from reflex_silverpoint_react import sp_deck

from .layout import button, card, code, page, select

#: The showcase deck, a file of the demo's assets, read when the app compiles.
SHOWCASE = (Path(__file__).resolve().parent.parent / "assets" / "decks" / "showcase.md").read_text(encoding="utf-8")

FENCE = "`" * 3

#: The editor's starting text: a short deck to change.
DRAFT = f"""---
paginate: true
footer: Edit me
---

<!-- _class: lead -->

# A deck you can edit

Change the Markdown on the left.

---

## Two charts, two fences

* Edit a title below
* Change `bar-chart` to `area-chart`

{FENCE}silverpoint
{{"chart": "bar-chart", "props": {{"title": "Visits by quarter"}}, "height": 300}}
{FENCE}

---

<!-- _ground: cyanotype -->

## On another ground

{FENCE}silverpoint
{{"chart": "gauge-arc", "props": {{"percent": 72, "caption": "Capacity used"}}, "height": 300}}
{FENCE}
"""

MODES = ["ink", "precision"]
LOG_SIZE = 40


class DeckState(rx.State):
    """State of the deck page: the controlled showcase deck, the editor and the event log."""

    page: int = 1
    total: int = 0
    step: int = 0
    steps: int = 0
    show_notes: bool = True
    show_controls: bool = True
    mode: str = "ink"
    draft: str = DRAFT
    draft_page: int = 1
    draft_total: int = 0
    log: list[str] = []

    def _record(self, line: str) -> None:
        self.log = [line, *self.log][:LOG_SIZE]

    # Showcase deck events.

    @rx.event
    def on_page_change(self, page: int, total: int):
        self.page, self.total = page, total
        self._record(f"showcase · page_change(page={page}, total={total})")

    @rx.event
    def on_fragment_change(self, page: int, step: int, steps: int):
        self.step, self.steps = step, steps
        self._record(f"showcase · fragment_change(page={page}, step={step}, steps={steps})")

    @rx.event
    def on_ready(self, total: int):
        self.total = total
        self._record(f"showcase · ready(total={total})")

    # Controls outside the deck.

    @rx.event
    def previous_page(self):
        self.page = max(self.page - 1, 1)

    @rx.event
    def next_page(self):
        self.page = min(self.page + 1, self.total or self.page + 1)

    @rx.event
    def first_page(self):
        self.page = 1

    @rx.event
    def last_page(self):
        self.page = max(self.total, 1)

    @rx.event
    def set_page_from(self, value: str):
        if value.isdigit():
            self.page = min(max(int(value), 1), max(self.total, 1))

    @rx.event
    def set_mode(self, value: str):
        self.mode = value if value in MODES else "ink"

    @rx.event
    def set_show_notes(self, value: str):
        self.show_notes = value == "shown"

    @rx.event
    def set_show_controls(self, value: str):
        self.show_controls = value == "shown"

    @rx.event
    def clear_log(self):
        self.log = []

    # Editor.

    @rx.event
    def set_draft(self, value: str):
        self.draft = value

    @rx.event
    def reset_draft(self):
        self.draft = DRAFT

    @rx.event
    def on_draft_page_change(self, page: int, total: int):
        self.draft_page, self.draft_total = page, total
        self._record(f"editor · page_change(page={page}, total={total})")

    @rx.event
    def on_draft_ready(self, total: int):
        self.draft_total = total
        self._record(f"editor · ready(total={total})")

    @rx.var
    def page_options(self) -> list[str]:
        return [str(n) for n in range(1, max(self.total, 1) + 1)]


DECK_CODE = """from pathlib import Path
from reflex_silverpoint_react import sp_deck   # @silverpoint/marp is installed as its npm dependency

SHOWCASE = Path("assets/decks/showcase.md").read_text()   # read at compile time


class DeckState(rx.State):
    page: int = 1
    total: int = 0

    @rx.event
    def on_page_change(self, page: int, total: int):
        self.page, self.total = page, total


sp_deck(
    SHOWCASE,
    page=DeckState.page,                   # controlled; or default_page=1
    on_page_change=DeckState.on_page_change,
    on_fragment_change=DeckState.on_fragment_change,   # (page, step, steps)
    on_ready=DeckState.on_ready,           # (total,)
    show_notes=True, show_controls=True,
    mode="ink",                            # or "precision"
    hash=True,                             # #<n> deep link
    id="showcase",
)"""

DIRECTIVES = [
    ("ground", "silverpoint · cyanotype", "silverpoint", "The ground a slide is drawn on; its charts follow."),
    ("substrate", "cream · green · blue · ochre · prussian", "the ground's first", "The prepared paper."),
    ("mode", "ink · precision", "ink", "precision switches the inking off."),
    ("class", "lead · invert · plate · hatched", "—", "A title slide, inverted inks, a plate mark, a hatched band."),
    ("paginate", "true · false", "false", "Page numbers (Marpit)."),
    ("header / footer", "text", "—", "Repeated on each slide (Marpit)."),
    ("backgroundColor / backgroundImage / color", "CSS", "—", "Marpit's own; ![bg right:40%](…) splits a slide."),
    ("size", "16:9 · 4:3", "16:9", "The slide size (Marpit); also the size prop."),
]

FENCE_FIELDS = [
    ("chart", "a catalog slug, e.g. bar-chart", "required"),
    ("props", "the chart's own props, camelCase", "{}"),
    ("data", "the rows the chart reads", "its demo dataset"),
    ("width", "160 .. 1280 canvas px", "the slide's width"),
    ("height", "90 .. 720 canvas px", "360"),
    ("id · ground · substrate · mode · palette", "as on any chart", "the slide's"),
]

CHEAT_MARKDOWN = f"""---
paginate: true
header: My talk
---

<!-- _class: lead -->
# Title slide

---

<!-- _ground: cyanotype -->
## A chart on cyanotype

{FENCE}silverpoint
{{"chart": "bar-chart", "props": {{"title": "Visits"}}, "height": 400}}
{FENCE}

<!-- A presenter note: any comment that is not a directive. -->

---

* fragment one
* fragment two
1) and ordered ones"""

CLI_CODE = """# Marp CLI with the plain theme (fences shown as code, no controller)
npx @marp-team/marp-cli --theme node_modules/@silverpoint/marp/theme.css talk.md

# Marp CLI with silverpoint's engine (directives, backdrops and fences as static SVG)
npx @marp-team/marp-cli --engine @silverpoint/marp/cli talk.md

# VS Code: add the theme to the Marp extension's settings.json
"markdown.marp.themes": ["./node_modules/@silverpoint/marp/theme.css"]"""


def _table(head: list[str], rows: list[tuple[str, ...]]) -> rx.Component:
    return rx.el.table(
        rx.el.thead(rx.el.tr(*[rx.el.th(h) for h in head])),
        rx.el.tbody(*[rx.el.tr(rx.el.td(rx.el.code(row[0])), *[rx.el.td(cell) for cell in row[1:]]) for row in rows]),
        class_name="sp-props",
    )


def _readout() -> rx.Component:
    return rx.el.p(
        "Page ",
        rx.el.strong(DeckState.page, id="deck-readout-page"),
        " / ",
        # @silverpoint/react 0.9.0 never sends the first `ready`, so the total is known from the first move.
        rx.el.strong(rx.cond(DeckState.total > 0, DeckState.total.to_string(), "?"), id="deck-readout-total"),
        " · fragment ",
        rx.el.strong(DeckState.step, id="deck-readout-step"),
        " / ",
        DeckState.steps,
        class_name="deck-readout",
    )


def _controls() -> rx.Component:
    return rx.el.div(
        button("« First", on_click=DeckState.first_page, id="deck-first"),
        button("‹ Previous", on_click=DeckState.previous_page, id="deck-prev"),
        button("Next ›", on_click=DeckState.next_page, id="deck-next"),
        button("Last »", on_click=DeckState.last_page, id="deck-last"),
        rx.el.div(
            rx.el.label("Go to page", html_for="ctl-go-to-page"),
            rx.el.select(
                rx.foreach(DeckState.page_options, lambda option: rx.el.option(option, value=option)),
                id="ctl-go-to-page",
                value=DeckState.page.to_string(),
                on_change=DeckState.set_page_from,
            ),
            class_name="sp-control",
        ),
        select("Mode", DeckState.mode, MODES, DeckState.set_mode),
        select(
            "Notes",
            rx.cond(DeckState.show_notes, "shown", "hidden"),
            ["shown", "hidden"],
            DeckState.set_show_notes,
        ),
        select(
            "Controls",
            rx.cond(DeckState.show_controls, "shown", "hidden"),
            ["shown", "hidden"],
            DeckState.set_show_controls,
        ),
        class_name="sp-controls",
    )


def _event_log() -> rx.Component:
    return card(
        rx.el.div(
            rx.el.p("Event log", class_name="demo-card-title"),
            button("Clear", on_click=DeckState.clear_log, id="deck-log-clear"),
            class_name="deck-log-head",
        ),
        rx.cond(
            DeckState.log.length() > 0,
            rx.el.ol(rx.foreach(DeckState.log, lambda line: rx.el.li(rx.el.code(line))), class_name="deck-log"),
            rx.el.p("No events yet: move the deck.", class_name="sp-note"),
        ),
        id="deck-event-log",
    )


def deck_page() -> rx.Component:
    return page(
        rx.el.h1("Slide decks"),
        rx.el.p(
            "Marp/Marpit Markdown presentations drawn in silverpoint: the npm SpDeck of silverpoint 0.9 "
            "(@silverpoint/react/deck). Slides are separated by ---, comments set directives or hold presenter "
            "notes, list items are revealed one at a time, and silverpoint fences become live charts.",
            class_name="sp-lede",
        ),
        rx.el.h2("Showcase, driven from Python"),
        rx.el.p(
            "assets/decks/showcase.md, read when the app compiles. The page is controlled: the buttons below "
            "and the deck's own controls and keys (focus it, then use the arrows, Space, Home/End; o overview, "
            "f full screen, n notes) both move it, and every event lands in the log. The URL keeps a #<n> "
            "deep link: reload on #5 to open the fifth slide."
        ),
        _controls(),
        _readout(),
        rx.el.div(
            sp_deck(
                SHOWCASE,
                page=DeckState.page,
                show_notes=DeckState.show_notes,
                show_controls=DeckState.show_controls,
                mode=DeckState.mode,
                hash=True,
                on_page_change=DeckState.on_page_change,
                on_fragment_change=DeckState.on_fragment_change,
                on_ready=DeckState.on_ready,
                id="showcase",
            ),
            class_name="deck-stage",
        ),
        _event_log(),
        code(DECK_CODE),
        rx.el.h2("Live editor"),
        rx.el.p(
            "The Markdown on the left is state; the deck on the right re-renders from it half a second after "
            "you stop typing, and its charts are mounted again."
        ),
        rx.el.div(
            rx.el.div(
                rx.text_area(
                    value=DeckState.draft,
                    on_change=DeckState.set_draft,
                    debounce_timeout=500,
                    rows="24",
                    spell_check=False,
                    id="deck-editor",
                    class_name="deck-editor",
                ),
                rx.el.p(
                    button("Reset the draft", on_click=DeckState.reset_draft, id="deck-editor-reset"),
                    " Page ",
                    DeckState.draft_page,
                    " / ",
                    rx.cond(DeckState.draft_total > 0, DeckState.draft_total.to_string(), "?"),
                ),
            ),
            rx.el.div(
                sp_deck(
                    DeckState.draft,
                    default_page=1,
                    on_page_change=DeckState.on_draft_page_change,
                    on_ready=DeckState.on_draft_ready,
                    id="editor",
                ),
                class_name="deck-stage",
            ),
            class_name="deck-split",
        ),
        rx.el.h2("Authoring cheat sheet"),
        rx.el.h3("Directives"),
        rx.el.p(
            "In the front matter for the whole deck, as <!-- key: value --> from a slide on, or as "
            "<!-- _key: value --> for one slide only. Any other comment is a presenter note."
        ),
        _table(["Directive", "Values", "Default", "Effect"], DIRECTIVES),
        rx.el.h3("The chart fence"),
        rx.el.p(
            "A fenced block whose language is silverpoint holds one chart as JSON. A block that is not JSON, "
            "names an unknown chart or prop, or asks for a size out of range draws an error figure in its place "
            "(SP026); the rest of the deck renders as usual. Raw HTML is shown as text; <style scoped> still "
            "restyles one slide."
        ),
        _table(["Field", "Value", "Default"], FENCE_FIELDS),
        code(CHEAT_MARKDOWN),
        rx.el.h3("Marp CLI and VS Code"),
        rx.el.p(
            "@silverpoint/marp/theme.css carries both grounds as a plain Marp theme. There, backdrops are not "
            "generated and fences are shown as code; with silverpoint's engine, Marp CLI draws them as static SVG."
        ),
        code(CLI_CODE),
    )
