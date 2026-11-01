# Deck

`sp_deck` is the npm `SpDeck` of `@silverpoint/react/deck`: a Marp/Marpit Markdown presentation
drawn in silverpoint. Its engine, `@silverpoint/marp` (which brings `@marp-team/marpit`), is an npm
dependency of this component only, so Reflex installs it when a page uses `sp_deck`. The component
imports its stylesheets itself (`fonts.css`, `styles.css`, `ui.css`, `@silverpoint/marp/deck.css`)
and renders on the server; it needs no `NoSSR` wrapper.

- `markdown` is the deck, a string or a state var. Slides are separated by `---`. The front matter
  sets the deck's directives; `<!-- key: value -->` sets one from that slide on and
  `<!-- _key: value -->` on that slide only. Any other comment is a presenter note.
- Directives: silverpoint's `ground` (`silverpoint`, `cyanotype`), `substrate` and `mode` (`ink`,
  `precision`), plus Marpit's own: `paginate`, `header`, `footer`, `class`, `backgroundColor`,
  `backgroundImage`, `color`, `size`, `headingDivider`, `lang`. Classes: `lead`, `invert`, `plate`,
  `hatched`. Background images keep Marpit's syntax, split ones too (`![bg right:40%](…)`).
- Each list item (`*` or `1)`) is a fragment, revealed a step at a time.
- A fence whose language is `silverpoint` holds one chart as JSON: `chart` (a catalog slug) and,
  optionally, `props` (camelCase, as the npm chart takes them), `data`, `width` (160..1280),
  `height` (90..720, default 360), `id`, `ground`, `substrate`, `mode`, `palette`. A fence that is not
  JSON or names an unknown chart or prop draws a visible error figure and warns `SP026`.
- Raw HTML is shown as text, never rendered; Marpit's `<style>` and `<style scoped>` still apply.
- Controlled: `page` with `on_page_change(page, total)`; uncontrolled: `default_page`.
  `on_fragment_change(page, step, steps)` may take only `(page, step)`; `on_ready(total)`.
- `mode` is `"ink"` or `"precision"`. `palette` is a preset's name (`"iron_gall"` and `"ironGall"`
  both work), not a dict: the deck's charts read only the presets.
- `hash=True` reads and writes a `#<n>` deep link. With focus in the deck, the arrows,
  PageUp/PageDown, Space, Home and End move it; `o` opens the overview, `f` full screen, `n` the notes.
- For Marp CLI or the Marp VS Code extension, use `node_modules/@silverpoint/marp/theme.css` as the
  theme, or `--engine @silverpoint/marp/cli` to draw the fences as static SVG.

```python
import reflex as rx
from reflex_silverpoint_react import sp_deck

FENCE = "`" * 3

TALK = f"""---
paginate: true
footer: Quarterly review
---

<!-- _class: lead -->

# Quarterly review

---

## Visits by quarter

{FENCE}silverpoint
{{"chart": "bar-chart", "props": {{"title": "Visits by quarter"}}, "height": 380}}
{FENCE}

<!-- Point at the third quarter. -->
"""


class State(rx.State):
    page: int = 1
    total: int = 0

    @rx.event
    def on_page_change(self, page: int, total: int):
        self.page, self.total = page, total

    @rx.event
    def next_page(self):
        self.page = min(self.page + 1, self.total or 1)


def talk() -> rx.Component:
    return rx.fragment(
        sp_deck(
            TALK,
            page=State.page,
            on_page_change=State.on_page_change,
            show_notes=True,
            hash=True,
            palette="sepia",
            id="talk",
        ),
        rx.el.button("Next", on_click=State.next_page),
    )
```

## Reference

<!-- generated:deck -->
