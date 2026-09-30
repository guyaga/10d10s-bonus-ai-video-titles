# #55 SWISS-GRID · International Typographic Style kinetic type

> A 12-column grid draws itself over the shot, heavy grotesk statements rise line by line out of masks and sit on the columns, a Swiss-red square jumps between grid cells on each new statement, and a counter plus a small caption column keep the rhythm.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/swiss-grid.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_SWISS-GRID.mp4
> Runner: run_style SWISS-GRID · Example: examples/swiss-grid/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: architecture, design studios, furniture, tech brand manifestos, museum/exhibition promos, fashion lookbooks with clean sets: short, confident statements (2–3 words per line).
- Avoid when: the footage is busy or colourful (the style needs a white wall, sky or concrete behind the type), the copy is long, or the brand is playful.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `.gl` / `.gh` | the grid: 13 vertical hairlines (margins 96 px, column width 144 px) + 2 horizontal ones | 1 px, 22% ink (dark) or 30% white (light) |
| `#red` | the red square, one column wide (144×144 px), #e3342f | snaps between cells |
| `.fr .l span` | statement lines, `size` px (190), line-height .98, −.045em, heavy grotesk | each line in its own mask |
| `.cap` | caption column: 3 columns wide, 28 px, 2 px ink rule on top | bottom of the frame |
| `#meta` | top row: running label (24 px, +.06em) and a two-digit counter (01, 02…) | |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| vertical grid lines (scaleY 0→1) | .05 + c×.035 | .90 | power3.inOut | whole clip | — | — |
| horizontal lines (scaleX 0→1) | .10 | 1.00 | power3.inOut | — | — | — |
| meta row (fade, y −10→0) | .35 | .60 | power3.out | — | — | — |
| red square first pop (scale 0→1) | frame 1 t+.5 | .45 | back.out(2) | — | — | — |
| statement line i (yPercent 102→0) | frame t + i×.14 | .75 | expo.out | to until | yPercent −102 at until−.5 + i×.06, .5 s | power3.in |
| caption (fade, y 16→0) | frame t+.5 | .60 | power3.out | — | fade at until−.4, .35 s | — |
| red square to the next cell | next frame t−.1 | .50 | expo.inOut | — | — | — |
| counter roll (yPercent 60→0, fade) | next frame t | .35 | power3.out | — | — | — |
- Each statement is hidden outside its own window (visibility), so no text stacks under the live one.
- The signature move: three heavy lines rising out of masks on a 0.14 s stagger, and the red square snapping to its next cell with a hard expo.inOut: the grid IS the rhythm.

## Typography
- Latin: Manrope 700 statements (190 px, −.045em, uppercase copy recommended), Manrope 500 caption (28 px) and label (24 px). (The code sets the statement weight to 700; the docstring's "Manrope 800" is not used.)
- Hebrew: `pair: "secular"` (default): statements run RTL from the right edge of the grid (the start column counts from the right). The statement CSS forces weight 700; Secular One only has 400, so the browser fakes the bold. For Hebrew prefer `pair: "karantina"` (Karantina 700 is real heavy) or set `fonts: {"display": "Karantina", "dw": 700}`.
- Maximum copy: ≈ 9 characters per line at 190 px starting at column 1 (the lines are `nowrap`), 3 lines per frame; caption ≈ 50 characters.

## Colour and surface
- `ink: "dark"` (default): #111 type and grid on white walls/sky. `ink: "light"`: white type for dark concrete or night.
- `colors.red` #e3342f: the only colour. Swap to the brand colour only if it's a strong primary; the style depends on one hard accent.
- No panels, no shadows.

## Layout and safe zones (1920×1080 canvas)
- Grid: margin M = 96 px, 12 columns of 144 px. Statements start at column `col` (0–11), top at M+150 = 246 px. Red square cell `[col, row]` = (96 + col×144, 246 + row×120).
- Caption at column `cap_col` (default 9), bottom M+30; meta row at the top margin.
- Industry convention (Swiss style): flush-left ragged-right text, strict grid alignment, one accent colour, lots of white space, numbered sequence.
- 9:16: size ≈ 130, col 0, 2 lines per frame; keep the red square in the right columns.

## What the footage must give you
- Shoot it like this: one take, 6–30 s, clean architecture or a plain set, large flat bright (or uniformly dark) areas where the type sits; slow slider move.
- Tracking: none. Matte: not needed.
- Good footage: white concrete, gallery walls, minimal interiors, sky. Bad: texture or colour behind the type, busy crowds.

## Build it
### A. With the kit
```bash
python scripts/run_style.py SWISS-GRID --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| frames[] | {lines [...], t, until, col, red [col,row], caption, cap_col} | required; col 1, red [9,2], cap_col 9 |
| ink | "dark" / "light" | "dark" |
| grid | show the grid lines | true |
| size | statement px | 190 |
| label | running label next to the counter | "" |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Manrope 700 / 500 |
| colors | {red} | #e3342f |
| sfx | whoosh, click per line, thump on each red move | true |
| plate_vol, music, music_vol, name | — | .5, none, .5 |
```json
{
 "clip": "clips/gallery.mp4", "ink": "dark", "label": "NORD MUSEUM · 2026",
 "frames": [
  {"lines": ["LIGHT", "IS A", "MATERIAL."], "t": 0.7, "until": 5.0, "col": 1, "red": [10, 0], "caption": "The new north wing opens in May."},
  {"lines": ["SEE IT", "IN", "PERSON."], "t": 5.4, "col": 1, "red": [7, 1], "caption": "Tickets from 1 April."}
 ]
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const M = 96, CW = (1920 - 2 * M) / 12, cell = (c, r) => [M + c * CW, M + 150 + r * 120];
for (let c = 0; c <= 12; c++) tl.fromTo("#g" + c, {scaleY: 0}, {scaleY: 1, duration: .9, ease: "power3.inOut"}, .05 + c * .035);
const F = [{t: .7, until: 5.0, n: 3, red: [10, 0]}, {t: 5.4, n: 3, red: [7, 1]}];
const r0 = cell(...F[0].red);
tl.fromTo("#red", {x: r0[0], y: r0[1], scale: 0}, {scale: 1, duration: .45, ease: "back.out(2)"}, F[0].t + .5);
F.forEach((f, k) => {
  for (let i = 0; i < f.n; i++)
    tl.fromTo(`#f${k} .l:nth-child(${i + 1}) span`, {yPercent: 102}, {yPercent: 0, duration: .75, ease: "expo.out"}, f.t + i * .14);
  if (k > 0) { const r = cell(...f.red); tl.to("#red", {x: r[0], y: r[1], duration: .5, ease: "expo.inOut"}, f.t - .1); }
  if (f.until != null) for (let i = 0; i < f.n; i++)
    tl.to(`#f${k} .l:nth-child(${i + 1}) span`, {yPercent: -102, duration: .5, ease: "power3.in"}, f.until - .5 + i * .06);
});
```

## Adapting it to the user's project
- Content: 2–3 statements of 1–3 words per line; the caption carries the plain-language fact.
- Language: Hebrew → `"language": "he"` with a real heavy face (`pair: "karantina"`).
- Brand: the red square can be the brand colour; keep the rest ink.
- Vertical 9:16: see layout.
- Longer clips: one frame every 4–5 s; the counter numbers them.

## Sound
- `ui_whoosh` (.2) as the grid draws, `soft_click` (.28) per line, `soft_thump` (.35) as the red square lands/moves.

## Pitfalls and QA checklist
- [ ] Lines fit (nowrap): nothing crosses the right margin.
- [ ] The type sits on a flat bright (or dark) area for the whole frame duration.
- [ ] Hebrew uses a real bold (Karantina 700), not a faked Secular One bold.
- [ ] The red square never lands on a face or the key subject.
- [ ] Each statement exists only inside its window (no stacked hidden text).
