# #08 FLASH-CARD · Full-screen flash word

> On the single biggest beat the picture is replaced for about 4 frames by a full-screen accent card with one huge
> word ("AURA!", "בולמת!"), then the footage comes straight back.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/flash-card.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E3_aura_night_drive_SX.mp4
> Runner: run_ad (adkit `flash`) · Example: examples/E6_sneaker_sx.py (two flash cards: "אוויר!" and "AERO!")

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: the one moment that must hit: brand name reveal, "GOAL", "SOLD", the product name on the drop beat;
  social edits with strong music.
- Avoid when: used more than twice in a piece (it stops being an event); calm/premium films; photosensitive audiences
  (a full-frame colour flash, keep it to 0.16 s and never repeat rapidly).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate + everything else | the edit | untouched |
| Flash card `.fc` | a full-frame div (`inset: 0`) with a solid background | default background = accent |
| Word | one centred word, Karantina 700, 520 px, rotated −4° | colour default `--tacc` (auto ink/white) |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Card | `t` | instant (opacity set to 1) | — | `dur` (0.16 s ≈ 4 frames at 24 fps) | instant (opacity 0 at t + dur) | — |
| Word | `t` | scale 1.25 → 1 over `dur` | none (linear) | — | with the card | — |

- Beat sync: `t` = the hit (a snare / drop / the stressed syllable of the word), not before it.
- The signature move: **the frame swap**. It's a cut, not a fade: 4 frames of solid colour with the word shrinking
  slightly, so the eye reads a flash of the word and the brain keeps it. Pair it with a punch-zoom on the same beat
  (`punch`) and a VO hit.

## Typography
- Karantina 700, line-height .9, no wrap, 520–600 px (sample: 560 for Hebrew, 600 for Latin).
- Direction is automatic: if the text contains Hebrew the span is `rtl`, else `ltr` (so "AERO!" doesn't render as
  "!AERO").
- Hebrew: Karantina 700 is the only face for this card. Max copy: 1 word + optional "!" (≤ 7 characters at 560 px;
  1920 px width minus rotation margin).

## Colour and surface
- Defaults: background `var(--acc)`, word `var(--tacc)` (ink when the accent is light, white when it's dark).
- Inverse card (sample's second flash): `bg: "#111111"`, `color: "var(--acc)"`.
- Keep to the brand's accent and ink; two different cards in a piece = one normal, one inverse.

## Layout and safe zones (1920×1080 canvas)
- Full frame; the word is centred with flexbox and rotated `rot` (−4° default).
- 9:16: a 560 px word is ~1400 px wide, it will be cropped in a centre crop; for vertical, 2–4 letters or size 300.

## What the footage must give you
- Shoot it like this: cuts OK (max 6), 6–30 s · any framing · no free space needed · any camera · a music beat grid.
- Tracking: none. Matte: none.
- Good: an edit with a clear drop / hit. Bad: nothing, the card hides the footage; just don't hide a key action.

## Build it
### A. With the kit
```bash
python scripts/run_ad.py MY_AD --spec specs/MY_AD.py --render
```
| Key | Meaning | Default |
|---|---|---|
| text | the word | required |
| t | the hit | required |
| dur | time on screen | 0.16 s |
| size | word size | 520 px |
| bg | card background | `var(--acc)` |
| color | word colour | `var(--tacc)` |
| rot | word rotation | −4° |

A minimal spec (add to any adkit spec's elements):
```python
{"type": "flash", "text": "SOLD!", "t": 8.75, "dur": 0.16, "size": 560},
{"type": "flash", "text": "MY BRAND", "t": 15.35, "dur": 0.16, "size": 420, "bg": "#0a0c10", "color": "var(--acc)"},
{"type": "punch", "times": [8.75, 15.35], "amt": 1.1},
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```html
<div class="fc" id="f1" style="background:#4fd1ff"><span style="direction:rtl;font:700 560px/.9 Karantina;color:#0a0c10;transform:rotate(-4deg)">בולמת!</span></div>
```
```css
.fc{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0}
.fc span{white-space:nowrap}
```
```js
const T = 8.75, DUR = .16;
tl.set("#f1", {opacity: 1}, T); tl.set("#f1", {opacity: 0}, T + DUR);
tl.fromTo("#f1 span", {scale: 1.25}, {scale: 1, duration: DUR, ease: "none"}, T);
```

## Adapting it to the user's project
- Content: the brand/product name or the single verb of the ad, with "!".
- Language: Hebrew or English, direction is automatic.
- Brand: accent card for the first flash, inverse card (ink bg, accent word) for the second.
- Vertical 9:16: shorter word or smaller size.
- Longer or shorter clips: 1 card per piece is the rule, 2 is the maximum.

## Sound
- No cue of its own; land it on the music hit and a VO word. A punch-zoom on the same beat sells it.

## Pitfalls and QA checklist
- [ ] ≤ 2 flash cards per piece, ≥ 3 s apart; `dur` ≤ 0.2 s.
- [ ] The card doesn't hide the key action (product reveal, goal) itself: land it right after.
- [ ] Mixed text ("AERO!") renders in the right order (auto direction); frames checked + `scripts/qa.py` "ship".
