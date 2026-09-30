# #12 STOMP-SX · Dynamic Hebrew social stomp

> The high-energy Hebrew social cut: coloured Karantina headline words stomp in word by word on the voice (blur,
> squash, shake), ink tape strips carry the second line, glass tags ride the product, counters tick, a flash card hits
> the biggest beat, and a closing tape slogan lands with one accent word.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/stomp-sx.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E10_ember_chefs_pass_SX.mp4
> Runner: run_ad (adkit, theme `he_bold`) · Example: examples/E6_sneaker_sx.py (the template)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: Hebrew food, product, travel and brand ads for Reels/TikTok that need energy; VO-driven cuts of 12–20 s
  with 4–6 shots.
- Avoid when: premium tone (#10), long one-take shots (the rhythm wants cuts), no VO or music hits to stomp on.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate + punch | the cut, scale 1.1 → 1 on key words | `punch` |
| Behind words (optional) | a huge accent word behind the matted subject | `kine`/`stomp` with `behind` |
| Kinetic headline | `kine`: 1–2 rows of words; one word `accent`, `font: big`, `hit: true` | the voice's key words |
| Tape strips | `tape`: ink strip + accent strip under/next to the headline | the second line / proof |
| Tags / counters | glass tags on tracked food/product parts; counters for numbers (°C, days, grams) | `tag`, `counter` |
| Captions | karaoke bar at the bottom | `captions` (see #07) |
| Flash card | 1–2 full-frame words on the biggest beats | `flash` (see #08) |
| Tape lockup | brand strip + line strip, bottom-right | `lockup` in a Hebrew theme |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Kine word | its `t` (VO onset) | 0.14 s: opacity 0 → 1, scale 2.3 → 1, blur 14 px → 0; then squash scaleX 1.1 / scaleY 0.82 → 1 in 0.2 s | power4.out; back.out(3) | to element `end` (1.1–2.8 s) | whole block slides 160 px up/down or 260 px left/right + fades in 0.2 s, starting at `end` − 0.2 | power2.in |
| Hit word | its `t` | + frame shake (amount `amt`, 0.8) + thump 0.55 | — | — | — | — |
| Tape strip | its `t` (or element t + 0.18 j) | clip-path wipe right → left 0.28 s; text pop 1.35 → 1 at +0.12 | expo.out / power4.out | to `end` | 0.12 s fade | — |
| Counter | `t` | stomp from 1.5; value cubic-out t0 → t1 | power4.out | to `end` | 0.12 s | — |
| Tag | `t` | 0.35 s wipe + underline 0.45 s | expo.out | to `end` | 0.12 s | — |
| Punch | each time | plate scale 1.1 → 1, 0.35 s | power3.out | — | — | — |
| Flash | `t` | 0.16 s full frame | — | — | — | — |
| Tape lockup | `t` | strips wipe 0.3 s, shake 0.45 | expo.out | to end | — | — |

- Sample rhythm (E10, 15 s): headline "הכול מתחיל באש" 0.05–1.75 s (באש at 1.28 big/accent/hit) · counter 260 °C
  2.12–3.1 · "ורוד מבפנים" 3.42 · "רוטב" 4.95 + tape "שמצטמצם / 6 שעות" · "מלח" 7.62 + tape "עד הגרגר / האחרון." ·
  "EMBER" 11.0 · lockup 13.5; punches at 1.28, 3.42, 4.95, 6.55, 7.62, 9.55, 11.0; flashes "באש!" 1.5 and "EMBER!" 11.3.
- The signature move: **the word-by-word stomp with squash**: each word appears exactly on its spoken syllable,
  blurred and 2.3× big, snaps sharp in 0.14 s, then squashes (wider, shorter) and springs back, while the frame
  punches in on the accent word.

## Typography
- Hebrew: Karantina 700 for every headline word (line-height .98; `font: big` → .86), strips and lockup; Secular One for
  tags, counter labels, captions. Sizes: set-up words 100–150 px, the accent word 260–400 px. Words in a row keep a
  .11em margin (so they never collide). RTL rows; numbers glued ("6 שעות"); prices ש״ח.
- Styles per word: `fill` (light), `accent` (accent colour), `outline` (dark translucent fill + 5 px light stroke),
  `big` (tighter line height).
- Max copy: 2 rows, ≤ 3 words per row; one accent word per block; strips ≤ 4 words.

## Colour and surface
- Sample palette: acc `#ff7a3d`, ink `#120c0a`, lt `#fff6ec`, panel `rgba(20,13,10,.8)`, sub `#f3c9a8`. Swap `acc` to
  the brand colour. Word shadow: `0 16px 60px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.35)` (sample strengthens it to
  `.7`/`.55` for bright plates).
- On very bright shots (white plates in the sample) the headline flips to ink words with an accent word
  (`#e5 .kw{color:var(--ink)}`) via `css`.

## Layout and safe zones (1920×1080 canvas)
- `kine` blocks are centred on `x, y` (translate −50 %/−50 %); put them in the empty quarter of each shot (sample:
  x 1450–1640 when the food is left, x 280 when it's right).
- Tapes align right at x 1840 (80 px from the edge) or centred; counters top-left (84, 64); lockup bottom-right.
- 9:16: blocks centred at x 960, ≤ 560 px wide; accent word ≤ 300 px size.

## What the footage must give you
- Shoot it like this: planned cut list (max 5), 12–20 s · subject large, upper quarter free · 25 % free at the top ·
  energy from cuts and speed ramps.
- Tracking: optional, per shot, for tags (e.g. `steak_s`, `sauce_s`).
- Matte: only for behind-words.
- Good: bold, simple shots with one hero each and an empty corner. Bad: cluttered frames with no free quarter.

## Build it
### A. With the kit
```bash
python scripts/vo_take2.py MY_AD specs/MY_AD_lines.json sx
python scripts/word_times.py MY_AD specs/MY_AD_lines.json sx    # onsets for every kine word + captions
python scripts/run_ad.py MY_AD --spec specs/MY_AD_sx.py --render
```
`kine` keys: `x, y, t, end, exit (up/down/left/right), behind, lines: [[{w, t, size, style, font, hit, amt}]]`.
Other elements: `tape` (#06), `captions` + `punch` (#07), `flash` (#08), `counter`, `tag`, `lockup` (#05).

A minimal spec (`specs/MY_AD_sx.py`):
```python
SPEC = {"theme": "he_bold",
 "palette": {"acc": "#ff7a3d", "ink": "#120c0a", "lt": "#fff6ec", "panel": "rgba(20,13,10,.8)", "sub": "#f3c9a8"},
 "clip": "clips/my_food.mp4", "vo_name": "MY_AD_sx_vo", "css": ".kw{text-shadow:0 18px 70px rgba(0,0,0,.7),0 3px 10px rgba(0,0,0,.55)}",
 "elements": [
  {"type": "kine", "x": 1450, "y": 330, "t": 0.05, "end": 1.75, "exit": "up",
   "lines": [[{"w": "הכול", "t": 0.05, "size": 120}, {"w": "מתחיל", "t": 0.72, "size": 120}],
             [{"w": "באש", "t": 1.28, "size": 380, "style": "accent", "font": "big", "hit": True}]]},
  {"type": "tape", "x": 1840, "y": 400, "align": "r", "t": 2.2, "end": 3.6,
   "lines": [{"text": "יישון יבש", "style": "ink", "size": 60}, {"text": "28 יום", "style": "acc", "size": 84, "hit": True}]},
  {"type": "punch", "times": [1.28, 2.5], "amt": 1.1},
  {"type": "flash", "text": "באש!", "t": 1.5, "dur": 0.16, "size": 580},
  {"type": "lockup", "brand": "MY PLACE", "line": "הערב · הזמינו שולחן", "t": 4.0}]}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```css
.kn{position:absolute;display:flex;flex-direction:column;align-items:center;direction:rtl}
.kr{display:flex;align-items:baseline;direction:rtl;white-space:nowrap}
.kw{display:inline-block;margin:0 .11em;font:700 180px/.98 Karantina;color:#fff6ec;text-shadow:0 16px 60px rgba(0,0,0,.55),0 2px 6px rgba(0,0,0,.35)}
.kw.accent{color:#ff7a3d} .kw.big{line-height:.86}
```
```js
tl.set("#k1", {xPercent: -50, yPercent: -50}, 0);
for (const [id, t, hit] of WORDS) {                         // t = the VO onset of each word
  tl.fromTo(`#${id}`, {opacity: 0, scale: 2.3, filter: "blur(14px)"}, {opacity: 1, scale: 1, filter: "blur(0px)", duration: .14, ease: "power4.out"}, t);
  tl.fromTo(`#${id}`, {scaleX: 1.1, scaleY: .82}, {scaleX: 1, scaleY: 1, duration: .2, ease: "back.out(3)", immediateRender: false}, t + .14);
  if (hit) { shake(t, .8); tl.fromTo(["#plate", "#matte"], {scale: 1.1}, {scale: 1, duration: .35, ease: "power3.out", immediateRender: false}, t); }
}
tl.to("#k1", {x: 0, y: -160, opacity: 0, duration: .2, ease: "power2.in"}, END - .2);   // exit "up"
```

## Adapting it to the user's project
- Content: write the VO as 2–4 word phrases; one accent word per phrase; the proof (number/material/time) goes on a tape
  strip or a counter.
- Language: Hebrew-first; for English the same kit works (Karantina has Latin) but #01/#05 English themes read better.
- Brand: `acc` = brand colour; one flash card in the accent, one inverse.
- Vertical 9:16: centred blocks, smaller accent words.
- Longer or shorter clips: one block per shot; each block 1–3 s; don't stack two blocks at once.

## Sound
- Thump 0.55 on every `hit` word, 0.45 on counters and the lockup; VO 1.0; music around 0.45–0.6; plate low (0.35).

## Pitfalls and QA checklist
- [ ] Every word lands on its spoken onset (word_times + ear check).
- [ ] Words never collide (.11em margins; check the widest row at its biggest size stays inside x 96–1824).
- [ ] Blocks exit before the next block enters; nothing covers faces or the hero food/product.
- [ ] Numbers glued, ש״ח; `#flash{display:none}` if the start looks milky; frames checked + `scripts/qa.py` "ship".
