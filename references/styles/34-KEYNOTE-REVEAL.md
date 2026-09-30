# #34 KEYNOTE-REVEAL · Keynote stat reveal

> Apple-keynote pacing: one huge number or word per shot, revealed by a mask wipe, numbers counting up, a small unit and label, a clean blur-out.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/keynote-reveal.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_KEYNOTE-REVEAL.mp4
> Runner: run_style KEYNOTE-REVEAL · Example: examples/keynote-reveal

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: product launches, specs (range, speed, battery, price), company milestones, fundraising and growth numbers, event openers. One strong fact per shot.
- Avoid when: you have no numbers or single strong words; copy-heavy explanations; busy bright centres in every shot (the number lands in the middle).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` .3 |
| Vignette `#vig` | a radial darkening centred on the stat line | opacity from `vignette` .55 in the centre to 35% of that at 60% |
| Beat `.bt` | a full-width row centred at `y` | one visible at a time |
| Number / word `.num` | the hero: gradient-filled text (`background-clip:text`) | tabular figures, tracking −.02em |
| Unit `.unit` | small word after the number (32% of the size) | stays glued to the number on one baseline |
| Label `.lab` | one line below | 20% of the size (min 40 px), light weight |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Vignette | first beat − .4 s | .6 s | default | whole piece | – | – |
| Number/word row | `t` | .7 s mask wipe (+ y 40 → 0 for the "up" wipe) | expo.out | until `until` | .45 s to opacity 0, blur 10 px, scale .97 | power2.in |
| Count-up | `t` + .15 | 1.1 s from `count[0]` to `count[1]` | ease-out quart (1 − (1−u)^4) | final value | – | – |
| Label | `t` + .35 | .6 s from opacity 0, y 16 | power3.out | with the row | with the row | – |
- Wipes: `up` (reveals bottom to top), `center` (opens from the middle), `start` (from the reading start: left for English, **right for Hebrew**).
- Numbers are formatted with thousands commas and `dec` decimals.
- The signature move: **a mask wipe plus a count-up that lands before the label arrives**, with nothing else on screen. Silence around one number is what makes it feel like a keynote.

## Typography
- Latin: Jost 700 for the hero, Jost 300 for unit and label. Hero 300 px for counted numbers, 220 px for words.
- Hebrew: default pair `suez`: **Suez One** for hero words, **Secular One** for unit and label. **Suez One's digits are old-style**, so "620" reads as "62o" at hero size. Whenever the display face is Suez One, the numbers automatically use **Jost 600** (lining figures) while Hebrew words stay in Suez One.
- Prices in Hebrew as "12,900 ש״ח" (the unit carries ש״ח), never ₪.
- Maximum copy: the hero up to 6 characters at 300 px; the label up to about 30 characters.

## Colour and surface
- Roles: `text` #ffffff (units), `grad` ["#ffffff", "#9fd8ff"] top-to-bottom on the hero, `label` #d6dbe3, `vignette` .55. Brand swap: the gradient's bottom colour is the brand tint; keep the top near white.
- Surfaces: no panels. Contrast comes from the vignette and a 0 2 14 rgba(0,0,0,.7) label shadow.

## Layout and safe zones (1920×1080 canvas)
- Rows are full width and centred horizontally at y 540 (`position: center`) or 760 (`position: lower`); any beat can override `y` (the end card in the sample sits at y 900).
- The vignette follows the same centre line.

## What the footage must give you
- Shoot it like this: cuts OK (max 6) · subject off-centre or small; the centre third calm (sky, windscreen, dark interior) · no free space needed.
- Tracking: none.
- Matte: not needed.
- Good: one idea per shot with a low-detail, not-too-bright centre; cuts timed to the stats. Bad: a bright white centre (the gradient disappears) or a face in the centre of every shot.

## Build it
### A. With the kit
```bash
python scripts/run_style.py KEYNOTE-REVEAL --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| beats | list of beats (keys below) | required |
| beats[].text | the number or word | required |
| beats[].count, dec | [from, to] count-up; decimals | none (word reveal); 0 |
| beats[].unit, label | small word after the number; line below | none |
| beats[].t, until | in / out in seconds | –, never |
| beats[].wipe | up / start / center | up |
| beats[].size, y | hero size px; vertical position override | 300 (count) / 220 (word); from `position` |
| position | "center" (540) or "lower" (760) | center |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "suez" |
| fonts | override faces | Jost 700 + Jost 300 |
| colors | `{"text","grad":[top,bottom],"label","vignette"}` | #ffffff, [#ffffff, #9fd8ff], #d6dbe3, .55 |
| sfx | UI whoosh .28 just before every beat | true |
| music, music_vol, plate_vol, name, track | optional | –, .55, .3, style id, – |
```json
{
 "name": "my-keynote", "clip": "clips/my_launch.mp4", "language": "en",
 "beats": [
  {"text": "10", "count": [0, 10], "unit": "hrs", "label": "battery life", "t": 1.0, "until": 4.2},
  {"text": "2.4", "count": [0, 2.4], "dec": 1, "unit": "M", "label": "people on the waitlist", "t": 4.6, "until": 8.0, "wipe": "start"},
  {"text": "NOVA", "label": "Available today.", "t": 8.4, "wipe": "center", "size": 240}
 ]
}
```
### B. The core move in HyperFrames/GSAP
```js
const MASK = {up: ["inset(100% 0 0 0)", "inset(0% 0 0 0)"], center: ["inset(0 50% 0 50%)", "inset(0 0% 0 0%)"],
  start: RTL ? ["inset(0 0 0 100%)", "inset(0 0 0 0%)"] : ["inset(0 100% 0 0)", "inset(0 0% 0 0)"]};
for (const b of B) {
  const id = "#b" + b.i, m = MASK[b.wipe];
  tl.set(id, {opacity: 1}, b.t);
  tl.fromTo(id + " .row", {clipPath: m[0], y: b.wipe === "up" ? 40 : 0}, {clipPath: m[1], y: 0, duration: .7, ease: "expo.out"}, b.t);
  tl.fromTo(id + " .lab", {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .6, ease: "power3.out"}, b.t + .35);
  if (b.until != null) tl.to(id, {opacity: 0, filter: "blur(10px)", scale: .97, duration: .45, ease: "power2.in"}, b.until - .45);
}
// the count-up is a pure function of t, set every frame in onPlace:
window.onPlace = t => B.filter(b => b.count).forEach(b => {
  const u = Math.max(0, Math.min(1, (t - b.t - .15) / 1.1)), w = 1 - Math.pow(1 - u, 4);
  document.getElementById("n" + b.i).textContent = (b.count[0] + (b.count[1] - b.count[0]) * w).toFixed(b.dec);
});
```

## Adapting it to the user's project
- Content: 3–5 facts, each a number + unit + one short label; end on the product name as a word reveal.
- Language: Hebrew → Suez One words, Secular One labels, Jost digits (automatic). The "start" wipe runs right to left.
- Brand: the gradient's lower colour; the vignette strength for bright footage (up to .7).
- Vertical 9:16: sizes down to about 220 (numbers) and 160 (words); labels still centred.
- Longer clips: one beat per shot; leave at least .4 s of clean plate between `until` and the next `t`.

## Sound
- `ui_whoosh` at .28 just before each beat (−.05 s). Music bed at .55–.6.

## Pitfalls and QA checklist
- [ ] Numbers use lining digits (no "62o"): check any Suez One project.
- [ ] Each beat sits inside its own shot (cut points vs `t`/`until`).
- [ ] The gradient hero stays readable on the brightest frame; raise `vignette` if not.
- [ ] Units stay glued to their number in Hebrew (same row, same baseline).
