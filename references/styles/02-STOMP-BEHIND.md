# #02 STOMP-BEHIND · Text behind the subject

> A giant word stomps in on the beat and sits BETWEEN the background and the subject, so the person walks in front of
> their own title.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/stomp-behind.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/D1_stomp_behind_v2.mp4
> Runner: run_ad (adkit `stomp` / `kine` with `behind: true`) · Example: examples/E6_sneaker_sx.py (its "אוויר" word is behind the shoe)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: hero reveals, fashion, athletes, product hero shots, a brand name or one-word promise per beat, any subject
  with a clean silhouette against a plain background.
- Avoid when: the matte can't separate the subject (busy background, motion blur, hair against a similar colour, crowds);
  the subject is small (the occlusion doesn't read); you need to show prices or several facts (use #01 or #13).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` 0.4 (adkit default) |
| `#stage` (behind) | the giant words | everything with `behind: true`, plus `html_behind` |
| Matte | the subject cut out of the same clip (webm with alpha) | composited on top of the words: this is the trick |
| `#stage2` (front) | everything else: tags, price stickers, brand bug, lockup | never covered by the subject |
| Flash | full-frame flash on hits | adkit: 0.3 × amount |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Behind word (`stomp`) | `t` | 0.16 s, scale `from` (2.0) → 1, opacity 0 → 1 | power4.out | until `end` | opacity 0 over 0.12 s ending at `end` | linear |
| Sub line `<i>` (optional) | t + 0.25 | 0.2 s fade | default | with the word | with the word | — |
| Behind word (`kine`, word-by-word) | each word's `t` | 0.14 s, scale 2.3 → 1, blur 14 px → 0 | power4.out, then squash scaleX 1.1 / scaleY 0.82 → 1 in 0.2 s (back.out(3)) | until `end` | slides out 160 px (up/down) or 260 px (left/right) + fade, 0.2 s | power2.in |

- In the reference render (legacy recipe D1B) one word per item landed every 3 beats at 120 BPM (1.5 s), 430 px Anton,
  riding the tracked coat's top edge (anchor `t`, dy −40), and each word faded in 0.1 s just before the next.
- Beat/voice sync: `t` = a beat (librosa on the music) or the VO word onset (`word_times.py`).
- The signature move: **occlusion**. The word is huge and positioned so the subject's head/shoulders pass in front of
  part of it. Every stomp also shakes the frame (x −12, +9, −5, 0 px · y +5, −4, +2, 0 px over 0.04/0.04/0.04/0.06 s)
  and flashes.

## Typography
- Latin: Anton 400 (theme `guyaga`), 430–520 px so the occlusion reads; uppercase; one word, ≤ 7 letters.
- Hebrew: theme `he_bold` → Karantina 700 for the word (or Suez One 400 with theme `he_premium` for a premium piece);
  any small line under it uses Secular One. Hebrew `sub` on a stomp renders in Secular One at 34 % of the word size.
  RTL: words are centred, so nothing mirrors; digits stay glued to their word ("4 שכבות"). Prices as ש״ח.
- Max copy: 1 word behind (2 short words max); anything longer goes in front.

## Colour and surface
- Roles (adkit palette): `lt` = word colour, `acc` = its hard shadow, `ink` = dark text/panels, `panel` = glass,
  `sub` = secondary text. Reference: lt `#f6f1e8` (ivory), shadow `#ff3d2e`, ink `#16130f`.
- Surfaces: word = solid fill + 8 px 8 px 0 accent offset shadow (`shadow_px`, `shadow`); theme `guyaga` adds a 3 px
  red/cyan chroma split. For brand colours set `"color"` (fill) and `"shadow"` per element, or change the palette.

## Layout and safe zones (1920×1080 canvas)
- Place the word where the subject's head/torso will pass: either pinned to the tracked box
  (`follow`, `anchor: "t"`, `dy: -40`) or fixed (`x`, `y`, centred on that point).
- The word may bleed off the frame edges on purpose; keep its vertical centre inside the top 40 % for walking subjects.
- 9:16: centre-crop column is x 656–1264; a centred 430 px word still reads when cropped, the subject must stay centred.

## What the footage must give you
- Shoot it like this: one take, no cuts, 8–30 s · full body, centred, walks toward camera; plain wall or backdrop behind
  the head and shoulders · 30 % free both sides · slow dolly back matching the walk, or locked-off.
- Tracking: optional (only to pin the word to the subject): `{"name": "model", "desc": "the whole body … tight box"}`.
- Matte: **required**. `npx hyperframes@0.8.84 remove-background clips/my.mp4 -o mattes/<AD>_alpha.webm`
  (or set `"matte": "path/to/alpha.webm"` in the spec). Check the matte edges on 3 frames before building.
- Good: plain bright/dark background, crisp outline, subject large. Bad: hair against a busy background, motion blur,
  several people, subject crossing other objects.

## Build it
### A. With the kit
```bash
python scripts/run_ad.py MY_AD --spec specs/MY_AD.py --render
```
Spec keys for this style (adkit):
| Key | Meaning | Default |
|---|---|---|
| theme | font theme: `guyaga` (Anton), `he_bold` (Karantina), `he_premium` (Suez One) | `guyaga` |
| palette | `{acc, ink, lt, panel, sub}` | required |
| elements[].type = `stomp` | `text, t, end, behind, size, from, color, shadow, shadow_px, stroke, x, y` or `follow, anchor, dx, dy`, `align` (c/l/r), `sub` | size 200, from 2.0, color var(--lt), shadow var(--acc), 8 px, align c |
| elements[].type = `kine` | word-by-word version: `x, y, t, end, exit, behind, lines:[[{w, t, size, style, font, hit}]]` | size 180, from 2.3 |
| matte | alpha webm | `mattes/<AD>_alpha.webm` |
| clip, track, music, music_vol, plate_vol | media | `clips/<AD>_720p.mp4`, `tracks/<AD>_vtrack.json`, –, 0.5, 0.4 |

A minimal spec (`specs/MY_AD.py`):
```python
SPEC = {"theme": "guyaga",
 "palette": {"acc": "#ff3d2e", "ink": "#16130f", "lt": "#f6f1e8", "panel": "rgba(22,19,15,.72)", "sub": "#e4e1db"},
 "clip": "clips/my_walk.mp4", "track": "tracks/my_walk_vtrack.json", "matte": "mattes/my_walk_alpha.webm",
 "music": "shared/sfx/my_music.mp3",
 "css": "#flash{display:none}",   # optional: no white flash on a premium cut
 "elements": [
  {"type": "stomp", "text": "BOLD", "follow": "model", "anchor": "t", "dy": -40, "size": 430, "behind": True, "t": 1.01, "end": 2.4},
  {"type": "stomp", "text": "SS27", "x": 960, "y": 300, "size": 520, "behind": True, "t": 2.51, "end": 4.0},
  {"type": "lockup", "brand": "MY BRAND", "line": "the new season", "t": 4.2}]}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```html
<video id="plate" src="clip.mp4" muted></video>
<div id="stage"><div class="st" id="w1"><span>BOLD</span></div></div>          <!-- behind -->
<video id="matte" src="assets/matte.webm" muted></video>                        <!-- subject, alpha -->
<div id="stage2"><!-- front layer --></div><div id="flash"></div>
```
```js
// .st span{font:430px Anton; color:#f6f1e8; text-shadow:8px 8px 0 #ff3d2e; transform:translate(-50%,-50%)}
function shake(at, a = 1) {
  tl.to(["#stage", "#stage2"], {keyframes: [{x: -12*a, y: 5*a, duration: .04}, {x: 9*a, y: -4*a, duration: .04},
        {x: -5*a, y: 2*a, duration: .04}, {x: 0, y: 0, duration: .06}], ease: "none"}, at);
  tl.fromTo("#flash", {opacity: .3*a}, {opacity: 0, duration: .14}, at);
}
tl.set("#w1", {opacity: 0}, 0); tl.set("#w1", {opacity: 1}, T - .01);
tl.fromTo("#w1 span", {opacity: 0, scale: 2}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, T); shake(T);
tl.to("#w1", {opacity: 0, duration: .12}, END - .12);
window.onPlace = (t) => { const b = boxAt("model", t); if (b) Object.assign(document.getElementById("w1").style,
  {left: (b[0] + b[2]) / 2 + "px", top: (b[1] - 40) + "px"}); };   // pin to the head (anchor t, dy -40)
```
The matte video must be seeked with the plate (HyperFrames does this for `<video>` in the composition).

## Adapting it to the user's project
- Content: the one word that is the ad (brand, season, promise). Behind = emotion; facts go in front.
- Language: Hebrew → `he_bold` (Karantina) or `he_premium` (Suez One); keep it to one word.
- Brand: word colour = brand light colour, shadow = brand accent; or no shadow (`shadow_px: 0`) for a cleaner look.
- Vertical 9:16: centre the word on the subject; crop x 656–1264.
- Longer or shorter clips: 1 behind-word per 1.5–3 s at most; a 10 s clip carries 3–5 words.

## Sound
- adkit adds a soft sub thump (0.45) on every `stomp`, `counter`, `lockup` and (0.55) on every `kine` word with
  `hit: true`; music at `music_vol` (0.5), plate at 0.4.

## Pitfalls and QA checklist
- [ ] The matte exists and lines up with the plate (same clip, same length); edges are clean on 3 checked frames.
- [ ] The word is big enough that the occlusion is obvious (≥ 400 px) and the subject actually passes in front of it.
- [ ] The word is still readable with the subject covering part of it (the first and last letters visible).
- [ ] No important text is behind the subject (prices, CTA go in front).
- [ ] Theme `guyaga` adds a chroma split to the shadow; override `.st span.c{text-shadow:…}` in `css` for a clean look.
- [ ] Frames checked + `scripts/qa.py` "ship" (`hyperframes check` may flag overlap: the words carry `data-layout-allow-occlusion`).
