# #31 DECODE-TYPE · Terminal decode

> Lines type in while every character scrambles through random glyphs and locks, in reading order, behind a blinking block cursor.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/decode-type.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_DECODE-TYPE.mp4
> Runner: run_style DECODE-TYPE · Example: examples/decode-type

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: tech, AI, cyber-security, sci-fi, data products, "access granted" moments, status readouts beside a face or a machine, launch teasers.
- Avoid when: warm or organic brands (food, fashion, family); long sentences (a decode over 30+ characters feels slow); footage without a calm side for the lines.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` .6 |
| Line `.ln` | one text line, placed at (x, y) or pinned to a tracked object | zero-size anchor; the text is offset by `align` |
| Optional panel | dark glass strip behind a line | `rgba(4,12,10,.72)`, a 3 px accent border on the reading-start side |
| Character cell `.c` | each character twice: the final glyph (invisible, reserves the width) and a drawn glyph on top | the layout never jitters because the final text reserves the space |
| Scramble glyph | a random glyph from the set, drawn in the scramble colour at .85 opacity | Hebrew set: א–ת + 0–9; Latin set: A–Z, 0–9, #%&*+<>/ |
| Cursor `.cur` | a solid block, `size × .5` wide, `size × .9` tall, glowing | sits just past the last character that has appeared |

## Timing and motion
All times per line, from the line's `t`. `u` = (time − t) / dur.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Line | `t` | `dur` (default .9 + .045 × characters) | linear per character | until `until` | cut at `until` | none |
| Character k appears | u = k/n × .55 | instant | – | scrambles until lock | – | – |
| Character k locks | u = .35 + k/n × .65 | instant | – | final glyph | – | – |
| Scramble rate | – | glyph changes 12 × per second | – | – | – | – |
| Cursor | with the line | – | – | solid while typing, then blinks at 2.4 Hz | with the line | – |
- Stagger: characters appear over the first 55% of `dur` and lock over the last 65%, in reading order (right to left for Hebrew).
- The signature move: **a fixed-width reveal**. The final text reserves the layout, and the scramble is drawn over it, so nothing shifts while letters flicker and lock one by one.
- Deterministic: every glyph is `hash1(seed×131 + line×977 + char×31 + frame)`, so scrubbing or re-rendering gives identical frames.

## Typography
- Latin: IBM Plex Mono 500 (display) + JetBrains Mono 500 (body). Default size 64 px; the sample headline uses 150 px.
- Hebrew: **Secular One** (default pair `secular`) for status lines and headlines. Karantina 700 (`pair: karantina`) for a louder headline. Suez One doesn't suit this style (its digits are old-style).
- **Keep number runs together.** A run like `98.6%`, `07` or `2026` is wrapped in a left-to-right isolate (`direction:ltr; unicode-bidi:isolate`). Without it, the bidi algorithm reorders characters and "98.6%" can render as "6.89%" inside Hebrew.
- Maximum copy: about 24 characters for a status line at 46 px beside a face; about 14 characters for a 150 px headline.

## Colour and surface
- Roles: `text` #e8fff4, `scramble` #5cffb0, `cursor` #5cffb0 (with an 18 px glow), `panel` rgba(4,12,10,.72). Brand swap: put the brand's accent in `scramble` and `cursor`; keep `text` near white.
- Surfaces: optional panel (`"panel": true`) with padding .18em .45em.

## Layout and safe zones (1920×1080 canvas)
- A free line: `x`, `y` in px (default 960, 540); `align` says which physical edge sits on the point (`center`, `left`, `right`).
- A pinned line: `follow` a tracked object and `anchor` (c|t|b|l|r|tl|tr|bl|br) plus `dx`, `dy`. Status lines to the right of a face: `"anchor": "r", "align": "left", "dx": 70`, stacked by `dy` −150 / −80 / −10.
- Keep lines inside the 5% safe margin (96 px left/right, 54 px top/bottom).

## What the footage must give you
- Shoot it like this: cuts OK (max 4) · subject centred or off-centre, calm space on one side for the status lines · 22% free on the right.
- Tracking: optional. Pin lines to a face or subject with vtrack.py, e.g. `{"context": "a man's face in a helmet", "objects": [{"name": "face", "desc": "the man's face"}]}`.
- Matte: not needed.
- Good: a locked or slow-push close-up with dark bokeh beside it. Bad: bright busy backgrounds where thin mono text vanishes.

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/my_clip.mp4 objects.json tracks/my_track.json      # only if lines follow something
python scripts/run_style.py DECODE-TYPE --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| lines | list of lines (keys below) | required |
| lines[].text | the text | required |
| lines[].t / until | start / end in seconds | – / never |
| lines[].x, y | position in px (free line) | 960, 540 |
| lines[].align | center / left / right | center |
| lines[].size | font size px | 64 |
| lines[].weight | "display" or "body" face | body |
| lines[].dur | seconds from first glyph to last lock | .9 + .045 × characters |
| lines[].color | text colour | colors.text |
| lines[].panel | glass strip behind the line | false |
| lines[].follow, anchor, dx, dy | pin to a tracked object | –, c, 0, 0 |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "secular" |
| fonts | override faces | IBM Plex Mono 500 + JetBrains Mono 500 |
| colors | `{"text","scramble","cursor","panel"}` | #e8fff4, #5cffb0, #5cffb0, rgba(4,12,10,.72) |
| seed | scramble seed | 7 |
| sfx | data chatter at each line start (.22), lock tick at each lock (.5) | true |
| track, music, music_vol, plate_vol, name | optional | –, –, .45, .6, style id |
```json
{
 "name": "my-decode", "clip": "clips/my_clip.mp4", "language": "en",
 "lines": [
  {"text": "IDENTITY CONFIRMED", "t": 1.0, "until": 6.0, "x": 1500, "y": 300, "align": "left", "size": 46, "panel": true},
  {"text": "ACCESS GRANTED", "t": 3.0, "until": 6.0, "x": 960, "y": 900, "size": 140, "weight": "display", "dur": 1.4}
 ]
}
```
### B. The core move (per frame, from onPlace)
```js
const fr = Math.floor(t * 12);                          // 12 glyph changes per second
cells.forEach((c, k) => {
  const u = (t - line.t) / line.dur, appear = k / n * .55, lock = .35 + k / n * .65;
  const fin = c.firstChild.textContent, b = c.lastChild;   // <i> reserves width, <b> is drawn on top
  let s = "", cls = "";
  if (fin.trim() === "") s = " ";
  else if (u >= lock) s = fin;
  else if (u >= appear) { s = SET[Math.floor(hash1(SEED * 131 + line.i * 977 + k * 31 + fr) * SET.length)]; cls = "s"; }
  b.textContent = s; b.className = cls; c.style.opacity = u >= appear ? 1 : 0;
});
cursor.style.opacity = (u < 1 || Math.floor(t * 2.4) % 2 === 0) ? 1 : 0;
```

## Adapting it to the user's project
- Content: 2–4 short status lines plus one headline. Numbers make it feel real ("98.6%", "ID 0472").
- Language: Hebrew uses the Hebrew glyph set for the scramble automatically.
- Brand: the scramble and cursor colour carry the brand; keep the rest cool and minimal.
- Vertical 9:16: stack the lines centred (`align: center`) below the subject instead of beside it.
- Longer clips: stagger more lines, and set `until` so old lines clear before new ones arrive.

## Sound
- `data_chatter` at .22 at each line's start; `lock_tick` at .5 when each line finishes locking. Music bed at .45 if used.

## Pitfalls and QA checklist
- [ ] Number runs read correctly inside Hebrew lines (check "98.6%" didn't flip).
- [ ] Pinned lines don't drift onto the face; check `dx`/`dy` at the frame where the subject is largest.
- [ ] `dur` isn't so short that nobody sees the scramble (under .6 s for 10+ characters reads as a glitch).
- [ ] Lines stay inside the safe margin when the tracked subject moves.
