---
paginate: true
header: silverpoint · slide decks
footer: reflex-silverpoint-react 0.9.1
ground: silverpoint
substrate: cream
---

<!-- _class: lead -->
<!-- _paginate: false -->

# Charts drawn like silverpoint

Marp decks in Reflex, from Markdown

<!-- Welcome. This deck is plain Marp Markdown, read by sp_deck at compile time. Press n to hide these notes. -->

---

## What a deck is made of

* Slides separated by `---`, directives in comments
* Lists that reveal one item at a time
* `silverpoint` fences that become live charts
* Presenter notes from any other comment

<!-- Each bullet is a fragment: the arrows reveal them before the next slide. -->

---

## Visits by quarter

```silverpoint
{"chart": "bar-chart", "props": {"title": "Visits by quarter", "xKey": "quarter", "valueKey": "visits"}, "data": [{"quarter": "Q1", "visits": 412}, {"quarter": "Q2", "visits": 538}, {"quarter": "Q3", "visits": 611}, {"quarter": "Q4", "visits": 574}], "height": 380}
```

<!-- A bar chart with its own rows. Hover a bar: the chart is hydrated, not a picture. -->

---

## How a slide is drawn

1) Marpit parses the Markdown and the directives
2) The silverpoint theme lays it on the ground
3) Each fence is drawn as static SVG
4) In the browser, the chart is hydrated in place

---

<!-- _ground: cyanotype -->
<!-- _substrate: prussian -->

## The cyanotype ground

```silverpoint
{"chart": "line-chart", "props": {"title": "Visits over the year"}, "height": 380}
```

<!-- One directive moves this slide to the cyanotype ground; its chart follows. -->

---

<!-- _mode: precision -->

## Precision mode

```silverpoint
{"chart": "radar-chart", "props": {"title": "Skills, with exact strokes"}, "height": 400}
```

<!-- mode: precision switches the inking off: even, exact lines for a reading slide. -->

---

![bg right:40%](/decks/paper.svg)

## Prepared paper

A ground is the paper a chart is drawn on: its substrate, its inks and its rules.

Marpit's backgrounds still work: this one is split to the right.

---

<style scoped>
h2 { letter-spacing: 0.08em; text-transform: uppercase; }
p { font-style: italic; }
</style>

## Share by channel

```silverpoint
{"chart": "donut-chart", "props": {"title": "Share by channel", "legend": true}, "height": 300}
```

A `<style scoped>` block restyles this slide only.

---

<!-- _substrate: ochre -->

## When a fence is wrong

```silverpoint
{"chart": "pie-chart", "props": {"title": "There is no pie chart"}}
```

The rest of the deck renders as usual.

<!-- This block names an unknown chart on purpose: it draws an error figure with the closest names (SP026). -->

---

<!-- _class: lead -->

# Thank you

`pip install reflex-silverpoint-react`
