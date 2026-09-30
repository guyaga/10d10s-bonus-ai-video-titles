# #03 GLASS-CALLOUT · Glass callout

> The quiet-luxury version of the escort: transparent outlined words and smoked-glass price cards that blur in on the
> beat beside the product, with no hard shadows.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/glass-callout.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/D1_stomp_glass_v2.mp4
> Runner: run_ad (adkit `stomp` + `tag`) · Example: examples/E6_sneaker_sx.py (adapt: outlined stomps + tags) · original recipe: references/recipes/legacy_shots.py → `D1G`

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: premium retail, beauty, jewellery on a person, calm luxury fashion, any piece where the footage must stay
  the hero and the graphics should feel like etched glass.
- Avoid when: the background is very bright and busy (translucent fills vanish), the piece needs energy (use #01 / #11),
  or the copy is long (glass cards hold a name + price, not sentences).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | plate 0.18 in the reference |
| Outlined word | translucent dark fill + near-white stroke + soft dark glow | the word lets the footage show through |
| Glass index tag | `01 / 05` on smoked glass | 1.5 px light border, 10 px backdrop blur |
| Glass price card | image + italic name + light price chip on smoked glass | 16 px blur, 14 px radius, no rotation, no shadow |
| Brand bug | glass brand box + light tag chip | top-left |
| Flash | ivory (not white) flash on hits | softer than the stomp family |

## Timing and motion
Identical rhythm to #01 (same builder in the reference): items on a 120 BPM grid, one every 3 beats.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Index tag | beat − 0.12 s | 0.12 s, y 20 → 0 | power3.out | until next item | group fade 0.12 s, scale 0.85 | power2.in |
| Outlined word | beat | 0.16 s, scale 1.9 → 1 | power4.out | until next item | with group | — |
| Glass card | beat + 1 | 0.18 s, scale 1.5 → 1, y 30 → 0 | back.out(2.2) | with group | with group | — |
| adkit `tag` (runnable route) | `t` | 0.35 s clip-path wipe left → right + fade; underline scaleX 0 → 1 in 0.45 s at t + 0.15 | expo.out / power3.out | until `end` | 0.12 s fade | linear |

- Stagger: 1.5 s per item (3 beats at 120 BPM) in the reference; never faster than 1.2 s, glass needs a beat to be read.
- The signature move: **the outlined word over the moving footage**: fill `rgba(22,19,15,.46)`, stroke
  `4px rgba(246,241,232,.98)`, glow `0 0 36px rgba(22,19,15,.55)`. The stroke carries legibility, the fill tints the
  footage without hiding it. The shake still fires on each stomp but the flash is ivory, so it reads as a light bloom.

## Typography
- Latin: word Anton 180 px (outline only), index tag Archivo 700 22 px .14em, card name Bodoni Moda italic 32 px, price
  Archivo 700 34 px, brand Bodoni Moda 600 40 px .22em.
- Hebrew: word in Suez One (premium; theme `he_premium`) or Karantina 700 (`he_bold`), card text Secular One. Outline
  strokes on Hebrew: keep ≤ 4 px at 180 px or the counters of ה/ם close up. Prices ש״ח, never ₪.
- Max copy: word ≤ 8 letters; card name ≤ 22 characters; price ≤ 7 characters.

## Colour and surface
- Palette (reference): ivory `#f6f1e8`, ink `#16130f`; accent is barely used (only the glass corner brackets in the adkit
  tag). Brand colours: keep the glass neutral (ink at 42–55 % alpha) and put the brand colour on the price chip only.
- Glass: `background: rgba(22,19,15,.42); border: 1.5px solid rgba(246,241,232,.75); backdrop-filter: blur(16px)
  saturate(1.2); border-radius: 14px; box-shadow: none`. Image tile ivory at 90 %, radius 8. Price chip ivory 92 %,
  radius 6, ink text. adkit `.gl` panels: `var(--panel)` background, `blur(10px) saturate(1.15)`, 1 px
  `rgba(255,255,255,.22)` border, 14 px accent corner brackets top-left/bottom-right.

## Layout and safe zones (1920×1080 canvas)
- Per item the group rides a tracked object with an anchor and an offset (reference: coat left edge dx −40; bag right
  edge dx +50; boots left edge dx −60), left groups align right, right groups align left.
- With adkit: `tag` follows `follow` at `anchor` (default `r`) + `dx` 24 / `dy` 0; `side: "l"` flips it to the left of
  the anchor. Keep cards inside x 96–1824, y 54–1026.
- 9:16: the cards won't fit beside a centred subject; stack one card under the subject (anchor `b`, dy +40).

## What the footage must give you
- Shoot it like this: one take, no cuts, 8–30 s · full body, centred, walks toward camera · 30 % free both sides · slow
  dolly back matching the walk, or locked-off.
- Tracking: the subject's full body plus each advertised item (vtrack objects `model`, `coat`, `bag`, `boots` …, one box
  per item, `desc` naming colour and part).
- Matte: not needed.
- Good: mid-tone or dark background behind the cards (glass reads). Bad: blown-out white backdrop (use #01 instead).

## Build it
### A. With the kit
```bash
python scripts/run_ad.py MY_AD --spec specs/MY_AD.py --render
```
| Key | Meaning | Default |
|---|---|---|
| theme | `luxe` (Cormorant italic display, Manrope labels), `guyaga` (Anton), `he_premium` / `he_bold` | `guyaga` |
| palette | `{acc, ink, lt, panel, sub}`; `panel` is the glass colour | required |
| `stomp` | `text, t, end, follow/anchor/dx/dy or x/y, size, color, stroke, shadow_px, from` | see #02 |
| `tag` | `title, sub, t, end, follow, anchor, dx, dy, side` | anchor r, dx 24, side r |
| css | overrides (glass values, glow instead of hard shadow) | — |

A minimal spec:
```python
SPEC = {"theme": "guyaga",
 "palette": {"acc": "#d8ccb8", "ink": "#16130f", "lt": "#f6f1e8", "panel": "rgba(22,19,15,.42)", "sub": "#e8e1d4"},
 "clip": "clips/my_walk.mp4", "track": "tracks/my_walk_vtrack.json", "music": "shared/sfx/my_music.mp3",
 "css": """#flash{background:#f6f1e8}
.st span.c{text-shadow:0 0 36px rgba(22,19,15,.55)!important}
.gl{backdrop-filter:blur(16px) saturate(1.2);border:1.5px solid rgba(246,241,232,.75);border-radius:14px}""",
 "elements": [
  {"type": "stomp", "text": "COAT", "follow": "coat", "anchor": "l", "dx": -40, "align": "r", "size": 180,
   "color": "rgba(22,19,15,.46)", "stroke": "4px rgba(246,241,232,.98)", "shadow_px": 0, "t": 1.01, "end": 2.37},
  {"type": "tag", "title": "The Camel Overcoat", "sub": "$890", "follow": "coat", "anchor": "l", "side": "l", "dx": -40, "dy": 150, "t": 1.51, "end": 2.37}]}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```css
.word{font:180px Anton;color:rgba(22,19,15,.46);-webkit-text-stroke:4px rgba(246,241,232,.98);text-shadow:0 0 36px rgba(22,19,15,.55)}
.card{background:rgba(22,19,15,.42);border:1.5px solid rgba(246,241,232,.75);backdrop-filter:blur(16px) saturate(1.2);border-radius:14px}
#flash{background:#f6f1e8}
```
```js
const B = (i) => +(0.51 + 0.5 * i).toFixed(3);       // measured beat grid of the reference
ITEMS.forEach(([key, bi], k) => {
  const g = `#g-${key}`;
  tl.fromTo(`${g} .idx`, {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .12, ease: "power3.out"}, B(bi) - .12);
  tl.fromTo(`${g} .word`, {opacity: 0, scale: 1.9}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, B(bi)); shake(B(bi));
  tl.fromTo(`${g} .card`, {opacity: 0, scale: 1.5, y: 30}, {opacity: 1, scale: 1, y: 0, duration: .18, ease: "back.out(2.2)"}, B(bi + 1));
  const out = k < ITEMS.length - 1 ? B(ITEMS[k + 1][1]) - .14 : B(15) - .1;
  tl.to(`${g} .inner`, {opacity: 0, scale: .85, duration: .12, ease: "power2.in"}, out);
});
// groups ride data-follow="coat" data-anchor="l" data-dx="-40" (the per-frame driver moves them)
```

## Adapting it to the user's project
- Content: product noun + product name + price, one item per 1.5 s; 3–5 items per clip.
- Language: Hebrew → theme `he_premium` (Suez One word) and Secular One cards; sides stay physical left/right.
- Brand: keep glass neutral; brand colour on price chips and the brand tag only.
- Vertical 9:16: one card under the subject at a time.
- Longer or shorter clips: same rule as #01, item spacing = usable walk time / items.

## Sound
- Reference mix: soft sub thump 0.45 on each word and finale hit, soft click 0.3 on each card, music 0.75, plate 0.18.
  With adkit, thumps fire on `stomp` / `counter` / `lockup` (`"thumps": false` to mute).

## Pitfalls and QA checklist
- [ ] The outlined word is readable on the brightest frame behind it (raise fill alpha to .55 or the glow if not).
- [ ] Glass over a very bright background → contrast check fails: darken `panel` or move the card.
- [ ] Theme `guyaga` adds a chroma split to stomp shadows: override `.st span.c{text-shadow:…}` (above).
- [ ] Cards never cover the face; the group exits before the next item.
- [ ] Hebrew prices read ש״ח; frames checked + `scripts/qa.py` "ship".
