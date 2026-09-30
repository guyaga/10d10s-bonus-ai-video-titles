# #45 DATA-CHARTS · Animated infographic panel

> A frosted glass card slides in on the clean side of the frame, the title unmasks, gridlines draw, bars grow one by one with their values counting up; then the card hands over to a line chart: the line draws with a glowing head, the area fills, and the last point gets a value flag.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/data-charts.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_DATA-CHARTS.mp4
> Runner: run_style DATA-CHARTS · Example: examples/data-charts/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: investor/board updates, quarterly results, SaaS growth stories, annual reports, explainer videos, LinkedIn business content: one clear story told by 4–7 numbers.
- Avoid when: there is no calm half of the frame (the card needs ~40% of the width), the data has more than 7 points, or the message is a single number (use KPI-COUNTERS or KEYNOTE-REVEAL).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#card` | glass card: `rgba(10,13,18,.8)`, blur 18 px + saturate 1.2, 1 px white-18% border, radius 22 px, shadow 0 30 80 | 96 px from the side edge, top 150 px, width `panel.w` (760) |
| `.tw > .tt` | title (48 px), two stacked titles if the line has its own `title` | mask swap between them |
| `.sb` | subtitle (24 px, sub colour) | |
| `.plot .gs` | 5 horizontal gridlines over a 640×330 chart area | each draws with dashoffset |
| `#chb .bar` | bars: 52% of the slot width, radius 8/8/2/2, grow from the bottom | the `hi` bar is accent-coloured with a glow |
| `.bv` / `.bl` | value above each bar (30 px, counts up) / category label under it (22 px) | numbers always LTR |
| `#chl` | line chart: area gradient (accent 45%→0), 5 px accent line, white head dot with accent glow | x labels under it |
| `.flag` | accent pill at the last point with the headline number (e.g. "+312%") | |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| card (fade, x ±60→0, scale .96→1) | panel.t | .70 | expo.out | to until | fade + x ±40 at until−.45, .45 s | power3.in |
| title (yPercent 110→0) | panel.t+.2 | .60 | expo.out | — | swaps to the line title at line.t−.4 (out .4 power3.in, in .6 expo.out at line.t−.05) | — |
| subtitle (fade, y 10→0) | panel.t+.35 | .50 | power3.out | — | — | — |
| gridlines (dashoffset 1→0) | panel.t+.3 | .80 each, stagger .06 | power2.inOut | — | — | — |
| bar k (scaleY 0→1) | bars.t + k×.18 | .90 | expo.out | — | bars fade out + y 20 at line.t−.45, .4 s | power2.in |
| bar value k (fade, y 14→0) | bars.t + k×.18 + .2 | .40 | power3.out | — | — | — |
| bar value count | bars.t + k×.18 | 1.0 | easeOut cubic | — | — | — |
| category labels | bars.t | .40, stagger .10 | — | — | — | — |
| line draw + area wipe | line.t | 1.80 | power2.inOut | — | — | — |
| head dot (scale 0→1) | line.t+1.75 | .40 | back.out(3) | then pulses 1→1.35, 5 yoyo repeats of .5 s | — | — |
| flag (fade, y 16→0, scale .8→1) | line.t+1.95 | .45 | back.out(2.5) | — | — | — |
- Rhythm: the sample shows bars for ~4 s (1.3→5.0), then the line for ~4 s: one idea per chart.
- The signature move: bars growing on an 0.18 s stagger with their numbers counting, then the line drawing to a glowing head and a flag. Numbers are always counted from video time (seek-safe).

## Typography
- Latin: Manrope 700 titles (48 px) and values (30 px, tabular), Manrope 500 subtitle (24 px) and labels (22 px).
- Hebrew: `pair: "secular"` (default): Secular One everywhere. The card becomes RTL; the chart area itself stays LTR geometry, but with `language: "he"` bars and x-labels are ordered right-to-left (first category on the right) and the area wipes from the right. The line is still drawn in data order (oldest first).
- Maximum copy: title ≈ 26 characters, subtitle ≈ 40, category labels ≤ 6 characters (use Q1, ינו׳), flag ≤ 7 characters.

## Colour and surface
- Roles: `card` rgba(10,13,18,.8), `text` #ffffff, `sub` #c3ccd6, `bar` rgba(255,255,255,.28), `accent` #39d98a (highlight bar, line, area, flag), `grid` rgba(255,255,255,.14).
- Brand swap: accent = brand colour; keep non-highlight bars neutral (the highlight is the story). Flag text is dark (#07150d); if the accent is dark, change the flag text colour in CSS.

## Layout and safe zones (1920×1080 canvas)
- Card at x = 96 px from the chosen `side`, top 150 px, width 760 px (≈ 40% of the frame); chart area 640×330 px.
- Industry convention: one chart per card, 4–7 data points, the highlighted value is the last/biggest one and matches the voiceover.
- 9:16: card width ≈ 900 px centred in the upper half; reduce to 4 bars.

## What the footage must give you
- Shoot it like this: one take, 8–20 s, people on one side, the other ~42% of the frame soft, bright, out-of-focus space; slow dolly or locked-off.
- Tracking: none.
- Matte: not needed.
- Good footage: office b-roll with shallow focus, a founder at a desk on one side, a lab, a warehouse aisle. Bad: whiteboards/screens/walls with writing (AI lettering behind a data card looks broken: the sample's first plate was rejected for exactly this).

## Build it
### A. With the kit
```bash
python scripts/run_style.py DATA-CHARTS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| panel | {side L/R, t, until, title, sub, w} | L, .6, none, "", "", 760 |
| bars | {labels, values, unit, t, hi} | none; hi = last bar |
| line | {values, labels, t, flag, title} | none |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Manrope 700 / 500 |
| colors | {card, text, sub, bar, accent, grid} | see above |
| sfx | whoosh, tick per bar, data chatter + chime on the line | true |
| music, music_vol, plate_vol, name | — | none, .5, .6 |
At least one of `bars` / `line` is required. `bars.until` is accepted but not used: the bars leave only when the line takes over.
```json
{
 "clip": "clips/founder.mp4",
 "panel": {"side": "R", "t": 0.6, "until": 11.5, "title": "Revenue growth", "sub": "2026 · by quarter"},
 "bars": {"labels": ["Q1", "Q2", "Q3", "Q4"], "values": [1.2, 1.9, 2.6, 4.1], "unit": "M", "t": 1.3, "hi": 3},
 "line": {"values": [3, 5, 4, 8, 11, 15, 22], "labels": ["Jan","Feb","Mar","Apr","May","Jun","Jul"], "t": 6.0, "flag": "+640%", "title": "Active teams"}
}
```
Note: values count up as integers (`Math.round`); for decimals like 1.2 M, scale the numbers (12 with unit "00K") or edit the rounding.
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const B = {t: 1.3, v: [42, 58, 71, 94]}, L = {t: 5.4};
tl.fromTo("#card", {opacity: 0, x: -60, scale: .96}, {opacity: 1, x: 0, scale: 1, duration: .7, ease: "expo.out"}, .6);
tl.fromTo(".gl", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: .8, ease: "power2.inOut", stagger: .06}, .9);
B.v.forEach((v, k) => tl.fromTo(`#b${k}`, {scaleY: 0}, {scaleY: 1, duration: .9, ease: "expo.out"}, B.t + k * .18));
tl.to("#chb", {opacity: 0, y: 20, duration: .4, ease: "power2.in"}, L.t - .45);
tl.fromTo(".lp", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: 1.8, ease: "power2.inOut"}, L.t);
tl.fromTo(".ar", {clipPath: "inset(0 100% 0 0)"}, {clipPath: "inset(0 0% 0 0%)", duration: 1.8, ease: "power2.inOut"}, L.t);
tl.fromTo(".flag", {opacity: 0, y: 16, scale: .8}, {opacity: 1, y: 0, scale: 1, duration: .45, ease: "back.out(2.5)"}, L.t + 1.95);
// counts are pure functions of time
const easeOut3 = (u) => 1 - Math.pow(1 - Math.min(1, Math.max(0, u)), 3);
window.onPlace = (t) => B.v.forEach((v, k) => document.getElementById("bn" + k).textContent = Math.round(v * easeOut3((t - (B.t + k * .18)) / 1)));
```

## Adapting it to the user's project
- Content: the user's real numbers; the highlighted bar and the flag carry the headline the voiceover says.
- Language: Hebrew → `"language": "he"`; month labels abbreviated (ינו׳, פבר׳); numbers stay LTR.
- Brand: accent only; card stays dark glass for contrast.
- Vertical 9:16: see layout.
- Longer clips: bars-then-line fills ~10 s; for more, render a second card later with a new spec entry (or a second pass).

## Sound
- `ui_whoosh` (.45) at the card, `soft_tick` (.3) per bar, `data_chatter` (.25) while the line draws, `chime` (.45) when the flag lands.

## Pitfalls and QA checklist
- [ ] No readable text or screens in the footage behind the card.
- [ ] The highlighted bar and the flag match the narration.
- [ ] Integers only in bar counters (or adapt the rounding).
- [ ] Hebrew: first category on the right; numbers LTR; area wipes from the right.
- [ ] Contrast: frames mid-exit may flag in QA; held frames must pass.
- [ ] The card never overlaps a face; check the widest frame of any camera move.
