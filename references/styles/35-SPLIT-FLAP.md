# #35 SPLIT-FLAP · Departure board

> A real split-flap board: every cell riffles through random letters with a falling leaf before landing on its character, row by row; a status re-flips later.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/split-flap.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_SPLIT-FLAP.mp4
> Runner: run_style SPLIT-FLAP · Example: examples/split-flap

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: travel, airlines, hotels, tours, trains, event line-ups ("stage · time · artist"), launch schedules, menus and price lists, sports fixtures. Anything tabular with a "status changed" moment.
- Avoid when: a single slogan (use KEYNOTE-REVEAL or KINETIC); long names (cells are fixed width); fast footage with no calm top band.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` .5 |
| Board `#board` | a dark rounded panel | rgba(12,12,12,.86), padding 22/24/26 px, radius 10 px, shadow 0 30 70 rgba(0,0,0,.45) |
| Title | static header line | body face, 0.8 × cell px |
| Header row | one label per column, **spanning exactly its column's width** and centred on it | body face, 0.56 × cell px, label colour |
| Cells | `w` cells per column, each `cell` px wide × 1.42 × cell tall | a top half, a bottom half and a falling leaf in a CSS 3D perspective of 8 × cell |
| Leaf | the half-card that falls during a flip | rotates on its hinge; a 2/6 px shadow |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Board | earliest row `t` − .6 s | .5 s from opacity 0, y −20 | power3.out | – | .5 s fade at `until` (optional) | default |
| A cell's riffle | row `t` + .03 × (k + 3 × column) | 5–13 flips (3 when clearing to a space), each `flip` .055 s | linear leaf | lands on its character | – | – |
| A flip | – | .055 s: top-leaf 0→−90° in the first half, bottom-leaf 90°→0 in the second | linear | – | – | – |
| Change | `changes[].t` + .03 × k | a new riffle from the current glyph to the new text | – | – | – | – |
- Stagger: within a row, cells start .03 s apart and each column adds a .09 s offset (3 × .03), so the riffle ripples across the board.
- Digits riffle through 0–9, letters through the alphabet (Hebrew letters on a Hebrew board).
- The signature move: **each cell riffles a random number of flips (5–13) before landing**, so a row settles unevenly, letter by letter, exactly like a station board; then one cell group re-flips later ("on time" → "departed").

## Typography
- Latin: Oswald 700 in the cells (0.95 × cell px), Jost 300 for title and labels.
- Hebrew: default pair `karantina`: **Karantina 700** in the cells, **Secular One** for the title and labels.
- Directions per column: Hebrew names fill right-to-left; times, gates and numbers use `"dir": "ltr"` so "08:40" keeps its order.
- **Headers must span their own column.** A header is exactly `w × cell + (w − 1) × 4` px wide and centred on its column. Without that, labels drift to the shared edge between an LTR and an RTL column and read as swapped ("שעה" over the destination).
- Maximum copy: each column's `w` in characters; longer text is cut. Plan the widest value per column.

## Colour and surface
- Roles: `board` rgba(12,12,12,.86), `cell` #1d1d1d, `text` #f4f1e8, `label` #b9b3a8; a column `color` overrides its text (the sample's status column is #ffd23f yellow). Brand swap: the status column colour.
- Surfaces: the board shadow; a 1 px dark seam across the middle of every cell.

## Layout and safe zones (1920×1080 canvas)
- `board.x`, `board.y` are the aligned top corner: Hebrew default x 1860, right-aligned; English default x 60, left-aligned; y 90.
- `cell` 58 px default (sample 44 px for a 23-cell board). Board width ≈ Σw × (cell + 4) + gaps of cell × .5 between columns + 48 px padding. Keep it inside 5% margins.
- Sits in the top band; the subject walks in the lower two thirds.

## What the footage must give you
- Shoot it like this: cuts OK (max 4) · subject in the lower two thirds; the top band free for the board · 30% free at the top.
- Tracking: none.
- Matte: not needed.
- Good: a travel walk, a terminal, a street with sky or a calm facade above. Bad: bright sky blowing out behind a translucent board (raise `board` opacity), a busy top third.

## Build it
### A. With the kit
```bash
python scripts/run_style.py SPLIT-FLAP --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| columns | `[{"w", "dir", "label", "color"}]` | required |
| columns[].w | cells in the column | required |
| columns[].dir | "ltr" / "rtl" | the language direction |
| columns[].label, color | header text; text colour | "", colors.text |
| rows | `[{"cols": [...], "t"}]` | required |
| changes | `[{"row", "col", "text", "t"}]` re-flip one cell group | [] |
| title | static header line | none |
| board | `{"x","y","align","cell"}` | he: 1860, 90, right, 58 · en: 60, 90, left, 58 |
| until | fade the board out (s) | never |
| flip | seconds per flip | .055 |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "karantina" |
| fonts | override faces | Oswald 700 + Jost 300 |
| colors | `{"board","cell","text","label"}` | rgba(12,12,12,.86), #1d1d1d, #f4f1e8, #b9b3a8 |
| seed | riffle seed | 3 |
| sfx | data chatter (.35) + UI tick (.3) at each row and change | true |
| music, music_vol, plate_vol, name, track | optional | –, .5, .5, style id, – |
```json
{
 "name": "my-board", "clip": "clips/my_walk.mp4", "title": "TONIGHT · LINE-UP",
 "board": {"x": 60, "y": 70, "align": "left", "cell": 48},
 "columns": [{"w": 5, "label": "TIME"}, {"w": 10, "label": "ARTIST"}, {"w": 7, "label": "STAGE", "color": "#ffd23f"}],
 "rows": [{"cols": ["21:00", "NOVA", "MAIN"], "t": 0.8}, {"cols": ["22:30", "ECHOLAND", "TENT"], "t": 1.4}],
 "changes": [{"row": 0, "col": 2, "text": "LIVE", "t": 7.0}]
}
```
### B. The core move (per frame, from onPlace)
```js
// seq = [[t0, fromChar, toChar], ...] built once from seeded hashes: n = 5 + floor(hash1(...) * 9) flips per landing
window.onPlace = (t) => CL.forEach(c => {
  let k = -1; for (let i = 0; i < c.seq.length; i++) if (t >= c.seq[i][0]) k = i; else break;
  if (k < 0) { c.top.textContent = c.bot.textContent = " "; c.leaf.style.display = "none"; return; }
  const [t0, from, to] = c.seq[k], p = Math.min(1, (t - t0) / FLIP);
  if (p >= 1) { c.top.textContent = c.bot.textContent = to; c.leaf.style.display = "none"; return; }
  c.top.textContent = to; c.bot.textContent = from; c.leaf.style.display = "block";   // new on top, old below
  if (p < .5) { c.leaf.className = "leaf t"; c.lspan.textContent = from; c.leaf.style.transform = `rotateX(${-180 * p}deg)`; }
  else        { c.leaf.className = "leaf b"; c.lspan.textContent = to;   c.leaf.style.transform = `rotateX(${180 * (1 - p)}deg)`; }
});
// a header spans its column: width = w * cell + (w - 1) * 4 px, text centred
```

## Adapting it to the user's project
- Content: 3–5 rows; one column is the "status" that changes later, which is the story beat.
- Language: Hebrew names right-to-left, times and codes `"dir": "ltr"`. Prices in a Hebrew column as ש״ח.
- Brand: the board colour and the status colour.
- Vertical 9:16: fewer, narrower columns (2–3), cell 40 px, board centred (`align: center`).
- Longer clips: add `changes` every few seconds; they keep the board alive.

## Sound
- `data_chatter` at .35 at every row start and change, `ui_tick` at .3 a quarter-second later. Music at .5–.55.

## Pitfalls and QA checklist
- [ ] Every header sits over its own column (check an LTR column next to an RTL one).
- [ ] No text is cut: count characters per column against `w`.
- [ ] Times and codes in a Hebrew board keep their order ("08:40", "B4").
- [ ] The board stays inside the safe margin at its widest.
- [ ] Automated QA may misread flipping Hebrew mid-riffle as "backwards"; zoom a settled frame to confirm before changing anything.
