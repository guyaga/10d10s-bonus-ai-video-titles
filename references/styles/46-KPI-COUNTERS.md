# #46 KPI-COUNTERS · Results dashboard tiles

> Frosted tiles cascade in on one side; in each, a caption rises, a big number counts up with its prefix/suffix, a thin progress rule sweeps across the tile, a sparkline draws to a glowing dot and a green/red delta chip pops.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/kpi-counters.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_KPI-COUNTERS.mp4
> Runner: run_style KPI-COUNTERS · Example: examples/kpi-counters/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: company results, SaaS metrics, campaign results, fundraising updates, "year in numbers", sports season stats, impact reports: 2–4 headline numbers with direction.
- Avoid when: the numbers need comparison over categories (use DATA-CHARTS), there's no clean third of the frame, or there are more than 4 KPIs at once.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#kpi` | the group, 96 px from the chosen side, `layout.top` px from the top | width = w × cols + gaps |
| `#kh` | optional heading chip (22 px, +.3em, accent colour on dark) | e.g. "Q3 · RESULTS" |
| `.kt` | a tile: `rgba(8,11,16,.76)`, blur 16 px + saturate 1.25, 1 px white-16% border, radius 18 px, padding 22/28/24 | grid of `cols` columns |
| `.kl` | caption, 20 px, +.22em | |
| `.kv` | the number, 84 px display, tabular, −.02em; suffix 52 px in accent | always LTR, en-US thousands separators |
| `.sp` | 200×56 sparkline (3.5 px, green or red), end dot | draws with dashoffset |
| `.kd` | delta pill with ▲/▼, tinted 22% green or red | |
| `.pr` | 3 px accent rule along the tile bottom | sweeps with the count, then fades |

## Timing and motion
Per tile, from its `t`:
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| heading (fade, y 12→0) | heading.t | .50 | power3.out | — | — | — |
| tile (fade, x ±50→0, rotateY ±12→0) | t | .70 | expo.out | to `until` | fade + x ±40, .4 s, stagger .08, at until−.6 | power3.in |
| caption (fade, y 10→0) | t+.15 | .45 | power3.out | — | — | — |
| number count 0→value | t+.35 | 1.60 | easeOut cubic | — | — | — |
| progress rule (scaleX 0→1) | t+.35 | 1.60 | power2.out | fades at t+2.0 (.4 s) | — | — |
| sparkline draw | t+.40 | 1.40 | power2.inOut | — | — | — |
| spark end dot (scale 0→1) | t+1.75 | .35 | back.out(3) | — | — | — |
| delta pill (fade, scale .6→1) | t+1.90 | .40 | back.out(2.5) | — | — | — |
- Stagger: 0.7 s between tiles in the sample (1.0, 1.7, 2.4): a cascade, not a wall.
- The signature move: the count, the progress rule and the sparkline all finish together (~t+2.0), then the delta pill "stamps" the result.

## Typography
- Latin: Space Grotesk 700 number (84 px) and delta (22 px), Space Grotesk 500 caption (20 px, +.22em) and heading (22 px, +.3em).
- Hebrew: `pair: "secular"` (default): Secular One captions and heading, tracking 0; the number row and the delta stay LTR. The progress rule sweeps from the right.
- Maximum copy: caption ≈ 20 characters; number ≤ 7 characters including separators and suffix (tile width 560–600 px also has to fit the 200 px sparkline).

## Colour and surface
- Roles: `card` rgba(8,11,16,.76), `text` #ffffff, `sub` #d2d9e1, `up` #3ddc84, `down` #ff5a5a, `accent` #7cc8ff (suffix, heading, progress rule).
- Brand swap: accent = brand colour; keep up/down semantic (green/red). For a light look: `card: "rgba(255,255,255,.82)"`, `text: "#0d1117"`, `sub: "#4b5563"`.

## Layout and safe zones (1920×1080 canvas)
- `layout`: side L/R, cols 1 (column) or 2 (grid), top 150, w 560, gap 22. Group starts 96 px from the side edge (5% safe).
- A 1-column stack of 3 tiles is ~720 px tall: keep `top` ≤ 160 so the last tile clears the bottom safe area.
- Industry convention: biggest/most important KPI first; the delta explains the number's direction; units belong in the suffix, not the caption.
- 9:16: cols 1, w ≈ 900, top ≈ 380, max 3 tiles.

## What the footage must give you
- Shoot it like this: one take, 6–20 s, subject on one side, the other ~35% calm soft background; slow dolly or locked-off.
- Tracking: none. Matte: not needed.
- Good footage: office b-roll, a product on a desk, a team at work, a stadium, a warehouse. Bad: screens or walls with readable text behind the tiles, a face on the tile side.

## Build it
### A. With the kit
```bash
python scripts/run_style.py KPI-COUNTERS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| tiles | list (below) | required |
| tiles[].label | caption | required |
| tiles[].value, decimals | number to count to | required, 0 |
| tiles[].prefix / suffix | e.g. "$" / "M" | "" / "" |
| tiles[].delta, down | pill text, red ▼ if true | "", false |
| tiles[].spark | sparkline values (≥ 2) | none |
| tiles[].t | tile in time | required |
| layout | {side, cols, top, w, gap} | L, 1, 150, 560, 22 |
| heading | {text, t} | none |
| until | all tiles leave | none |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Space Grotesk 700 / 500 |
| colors | {card, text, sub, up, down, accent} | see above |
| sfx | whoosh per tile, pulse per delta | true |
| music, music_vol, plate_vol, name | — | none, .5, .6 |
```json
{
 "clip": "clips/team.mp4",
 "layout": {"side": "R", "top": 150, "w": 580},
 "heading": {"text": "2026 · IN NUMBERS", "t": 0.5},
 "tiles": [
  {"label": "CUSTOMERS", "value": 12400, "delta": "+62%", "spark": [2, 3, 5, 6, 9, 12], "t": 1.0},
  {"label": "ARR", "value": 8.4, "decimals": 1, "prefix": "$", "suffix": "M", "delta": "+41%", "spark": [3, 4, 5, 6, 7, 8], "t": 1.7},
  {"label": "CHURN", "value": 1.9, "decimals": 1, "suffix": "%", "delta": "-0.4 PTS", "down": false, "spark": [4, 3.5, 3, 2.4, 2.1, 1.9], "t": 2.4}
 ],
 "until": 11.5
}
```
Note: `down` colours the pill and sparkline red; for "churn went down" (good news) keep `down: false` and write the negative in `delta`.
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const K = [{t: 1.0, v: 2.4, d: 1}, {t: 1.7, v: 18.6, d: 1}];
K.forEach((k, i) => {
  const g = `#k${i}`;
  tl.fromTo(g, {opacity: 0, x: -50, rotateY: 12}, {opacity: 1, x: 0, rotateY: 0, duration: .7, ease: "expo.out"}, k.t);
  tl.fromTo(`${g} .pr`, {scaleX: 0}, {scaleX: 1, duration: 1.6, ease: "power2.out"}, k.t + .35);
  tl.to(`${g} .pr`, {opacity: 0, duration: .4}, k.t + 2.0);
  tl.fromTo(`${g} .spl`, {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: 1.4, ease: "power2.inOut"}, k.t + .4);
  tl.fromTo(`${g} .kd`, {opacity: 0, scale: .6}, {opacity: 1, scale: 1, duration: .4, ease: "back.out(2.5)"}, k.t + 1.9);
});
const easeOut3 = (u) => 1 - Math.pow(1 - Math.min(1, Math.max(0, u)), 3);
const fmt = (v, d) => v.toLocaleString("en-US", {minimumFractionDigits: d, maximumFractionDigits: d});
window.onPlace = (t) => K.forEach((k, i) => document.getElementById("kn" + i).textContent = fmt(k.v * easeOut3((t - (k.t + .35)) / 1.6), k.d));
```

## Adapting it to the user's project
- Content: 2–4 real KPIs from the user, each with a direction.
- Language: Hebrew → `"language": "he"`; captions in Hebrew, numbers and deltas LTR.
- Brand: accent = brand colour; up/down stay semantic.
- Vertical 9:16: see layout.
- Longer clips: set `until` and start a second set later in another pass.

## Sound
- `ui_whoosh` (.35) per tile at t, `soft_pulse` (.35) when each delta pops (t+1.9).

## Pitfalls and QA checklist
- [ ] Numbers fit the tile with the sparkline (≤ 7 characters).
- [ ] Deltas are colour-honest (green = good for the viewer).
- [ ] Tiles clear the bottom 5% on the last frame of the cascade.
- [ ] Counts are computed from video time in `onPlace` (seek-safe).
- [ ] Contrast: first ~0.5 s of each tile fade may flag in QA; held frames must pass.
