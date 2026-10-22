# Timeline

`sp_timeline` is the npm `SpTimeline` of `@silverpoint/react/timeline`: Knight Lab TimelineJS drawn
in silverpoint. TimelineJS (`@knight-lab/timelinejs` 3.9.13) is an npm dependency of the component,
so Reflex installs it when a page uses `sp_timeline`; no Python extra is needed
(`timeline_available()` is always `True`, kept for old code). If TimelineJS cannot be loaded, the
component warns `SP025` and renders `fallback`.

It works in two layers. The **skin** replaces TimelineJS's colours, type and rules with the ground's:
substrate, inks, EB Garamond, hairline rules, eras hatched by density, the current marker
heightened. The **hand** lays the ground's own hand-inked frames and tone tiles on the markers, eras
and menubar; `inked_frames=False` keeps the skin only, and `precision`, `cyanotype` and forced
colours fall back to exact rules by themselves.

- `data` is TimelineJS's own JSON: `{"title", "events", "eras", "scale"}`, a state var, or any
  object with `to_dict()`. Each event has a `start_date` (`{"year": …}`) and `text`
  (`{"headline", "text"}`), and may carry a `unique_id`.
- `options` are TimelineJS's options; `font` and `theme` are ignored, because the skin sets both.
- `height` is the whole timeline's (600 px by default), in px or a CSS length.
- `on_change` receives the `unique_id` of the slide shown; the navigation events take no argument.
- `ground`, `substrate`, `mode`, `palette` and `id` work as on any component, and the provider's
  apply.
- TimelineJS requests its icon font from a relative path; the Reflex dev server answers it with
  HTML, so the browser logs font-decoding warnings. They come from TimelineJS.

```python
import reflex as rx
from reflex_silverpoint_react import sp_timeline

HISTORY = {
    "title": {"text": {"headline": "Silverpoint", "text": "A stylus on a prepared ground."}},
    "events": [
        {
            "start_date": {"year": 1390},
            "text": {"headline": "Cennini", "text": "Il libro dell'arte describes the ground."},
            "unique_id": "cennini",
        },
        {
            "start_date": {"year": 1484},
            "text": {"headline": "Dürer at thirteen", "text": "A self-portrait that admits no correction."},
            "unique_id": "durer",
        },
    ],
}


class State(rx.State):
    current: str = "title"

    @rx.event
    def on_change(self, unique_id: str):
        self.current = unique_id


def history() -> rx.Component:
    return sp_timeline(
        HISTORY,
        height=560,
        ground="silverpoint",
        substrate="cream",
        palette="sepia",
        inked_frames=True,
        on_change=State.on_change,
        id="history",
    )
```

## Reference

<!-- generated:timeline -->
