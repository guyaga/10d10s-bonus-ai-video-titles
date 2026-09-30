# #44 LEADER-CALLOUTS · Premium tech product callouts

> A white dot lands on a part of the product with a ring pulse, a thin leader line draws out (angled segment, then horizontal), and at its end a spaced caption and a big spec number rise out of a mask while the number counts up. Everything rides the tracked part.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/leader-callouts.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_LEADER-CALLOUTS.mp4
> Runner: run_style LEADER-CALLOUTS · Example: examples/leader-callouts/ (spec.json + objects.json)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: product launch films (earbuds, phones, watches, cameras, sneakers, appliances, cars), feature explainers, e-commerce hero videos: anywhere 2–5 facts belong to specific parts.
- Avoid when: the product is small in frame or moves fast (the lines swing wildly), the facts are not numbers (use TRACKED-TAGS), or there are more than 5 facts at once.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `.co` | a zero-size anchor that follows the tracked part every frame | `data-follow`, `data-anchor`, `dx/dy` |
| `svg .ln` | the leader: 2 px path, 2 segments: angled (60% of the rise horizontally), then horizontal `run` px | drawn with `stroke-dashoffset` 1→0 (`pathLength=1`) |
| `svg .rg` | the ring pulse around the dot, accent colour | radius 6→40, fading; fires at t and t+2.2 |
| `svg .dt` | the 7 px dot on the part | radius 0→7 with back.out |
| `svg .end` | 4 px accent dot at the line end | pops when the line arrives |
| `.lk` | the caption: 21 px, +.24em, uppercase, grey | rises out of an `overflow:hidden` wrapper |
| `.lv` | the value: prefix + counting number (84 px) + unit (34 px, accent) | tabular numerals, always LTR |

## Timing and motion
Per callout, from its `t`:
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| dot (r 0→7) | t | .35 | back.out(3) | to until | r→0 at until−.22, .2 s | power2.in |
| ring pulse (r 6→40, fade) | t, again t+2.2 | .90 | power2.out | — | — | — |
| line draw (dashoffset 1→0) | t+.15 | .60 | power3.inOut | to until | retracts at until−.6, .4 s | power3.in |
| end dot (r 0→4) | t+.70 | .25 | back.out(3) | — | r→0 at until−.6, .15 s | power2.in |
| caption (yPercent 110→0) | t+.70 | .50 | expo.out | to until | yPercent −110 at until−.6, .3 s | power3.in |
| value (yPercent 110→0) | t+.78 | .55 | expo.out | to until | with caption (stagger .04) | power3.in |
| number count 0→value | t+.75 | 1.10 | easeOut cubic | — | — | — |
- Stagger: 1.2 s between callouts in the sample (1.0, 2.2, 3.4, 4.6): each one lands, then the next.
- Beat sync: put each `t` on a beat or a turntable "facing" moment.
- The signature move: the two-segment leader drawing out of a dot, and the number counting up at its end. Precise, thin, lots of air.

## Typography
- Latin: Space Grotesk 700 value (84 px, −.02em, tabular), Space Grotesk 500 caption (21 px, +.24em, uppercase), unit 34 px.
- Hebrew: `pair: "secular"` (default): Secular One caption and value. The value block stays LTR (numbers and units); only the caption is RTL. Caption tracking 0.
- Maximum copy: caption ≈ 26 characters (nowrap), value ≤ 5 digits + a 3-letter unit.

## Colour and surface
- Roles: `line` #ffffff, `dot` #ffffff, `accent` #7cf0ff (ring, end dot, unit), `label` #b8c2cc, `value` #ffffff.
- Brand swap: put the brand colour in `accent` only. On light product sets use `line/dot/value: "#111"` and `label: "#555"`.
- Surface: no panels. A soft `drop-shadow(0 0 6px rgba(0,0,0,.45))` keeps thin lines readable over detail.

## Layout and safe zones (1920×1080 canvas)
- Each callout anchors to its tracked box (`anchor`: t/c/b/l/r/tl/tr/bl/br + dx/dy). `rise` is vertical (negative = up), `run` horizontal px, `side` L/R which way the line goes.
- Keep every label end ≥ 96 px (5%) from the frame edge over the whole clip: check the extreme frames of the orbit.
- Industry convention: callouts point at the part they describe, labels on the outside of the product, never crossing each other; left-side lines for left-side parts.
- 9:16: use `rise` for most of the distance (vertical stacks) and short `run` (≤ 120).

## What the footage must give you
- Shoot it like this: one take, 8–20 s, one product centred in the middle third on a plain dark set, large empty dark space left and right (30%), slow orbit or turntable with a gentle push-in.
- Tracking: vtrack.py on 2–4 parts, e.g. `{"context": "...", "objects": [{"name": "case", "desc": "the whole charging case"}, {"name": "buds", "desc": "the two earbuds inside (one box)"}]}`. The gate wants ≥ 90% coverage.
- Matte: not needed.
- Good footage: turntable product shots, slow macro orbits. Bad: hands covering the product, fast spins, busy backgrounds.

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/product.mp4 objects.json tracks/product.json
python scripts/run_style.py LEADER-CALLOUTS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip, track | video + vtrack JSON | required |
| callouts[].follow | tracked object name | required |
| callouts[].anchor, dx, dy | where on its box the dot sits | "c", 0, 0 |
| callouts[].side | line direction L/R | "L" |
| callouts[].rise / run | vertical / horizontal line length (px) | −140 / 260 |
| callouts[].label | caption | "" |
| callouts[].value, prefix, unit, decimals | the counting number | 0, "", "", 0 |
| callouts[].t / until | in / exit (s) | t required, no exit |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Space Grotesk 700 / 500 |
| colors | {line, dot, accent, label, value} | see above |
| sfx | pop per dot + tick per count | true |
| music, music_vol, plate_vol, name | — | none, .5, .6 |
```json
{
 "clip": "clips/watch.mp4", "track": "tracks/watch.json",
 "callouts": [
  {"follow": "bezel", "anchor": "tr", "side": "R", "rise": -160, "run": 220, "label": "Sapphire crystal", "value": 9, "unit": "H", "t": 1.0, "until": 9.5},
  {"follow": "strap", "anchor": "l", "side": "L", "rise": 140, "run": 200, "label": "Battery", "value": 72, "unit": "HRS", "t": 2.2, "until": 9.5}
 ]
}
```
### B. The core move in HyperFrames/GSAP
```js
// <path class="ln" d="M0 0 L-84 -140 L-344 -140" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const t = 1.0, until = 9.5;
tl.set(".dt, .end", {attr: {r: 0}}, 0);
tl.fromTo(".dt", {attr: {r: 0}}, {attr: {r: 7}, duration: .35, ease: "back.out(3)", immediateRender: false}, t);
tl.fromTo(".rg", {attr: {r: 6}, opacity: 1}, {attr: {r: 40}, opacity: 0, duration: .9, ease: "power2.out", immediateRender: false}, t);
tl.fromTo(".ln", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: .6, ease: "power3.inOut"}, t + .15);
tl.fromTo(".lk", {yPercent: 110}, {yPercent: 0, duration: .5, ease: "expo.out"}, t + .7);
tl.fromTo(".lv", {yPercent: 110}, {yPercent: 0, duration: .55, ease: "expo.out"}, t + .78);
tl.to(".lk, .lv", {yPercent: -110, duration: .3, ease: "power3.in", stagger: .04}, until - .6);
tl.to(".ln", {attr: {"stroke-dashoffset": 1}, duration: .4, ease: "power3.in"}, until - .6);
// the count is a function of time (seek-safe): value * easeOutCubic((t - (t0 + .75)) / 1.1)
window.onPlace = (now) => { const u = Math.min(1, Math.max(0, (now - (t + .75)) / 1.1));
  document.getElementById("n0").textContent = (42 * (1 - Math.pow(1 - u, 3))).toFixed(0); };
```

## Adapting it to the user's project
- Content: one fact per part; real specs from the user; units short and in the accent colour.
- Language: Hebrew → `"language": "he"`; captions RTL, values stay LTR.
- Brand: accent colour only; keep lines white or ink.
- Vertical 9:16: vertical rises, short runs.
- Longer clips: add callouts in waves; don't hold more than 4 at once.

## Sound
- `ui_pop` (.35) at each dot, `ui_tick` (.25) when the count starts (t+.75). Subtle: the product's own sound design should lead.

## Pitfalls and QA checklist
- [ ] Each dot sits ON the part it describes on every frame (watch the tracking preview first).
- [ ] No two lines cross; labels stay inside the 5% margin at the orbit extremes.
- [ ] Animate SVG circles by `attr: {r}`, never with GSAP scale/transform (transform origins on SVG drift to the frame corner).
- [ ] Labels rise into a mask; never wipe them sideways (half-revealed words read as truncated text).
- [ ] The exit is one synchronized retract (labels, line, then dot), not four separate fades.
