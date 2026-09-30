# #14 COMIC-POP · Comic burst words

> On the biggest beats a word slams in with a comic-book look: bright fill, double hard shadow, thick black outline,
> tilted, on a coloured starburst, cycling through six colour combos.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/comic-pop.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E3_aura_night_drive.mp4
> Runner: run_ad (adkit `stomp` with the theme flag `pop`) · Example: the spec below

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

**Use sparingly.** This look was rejected as childish for premium brands (the SPARTA film was rebuilt as #10
PRESIDENTIAL-SERIF). Offer it only for kids, gaming, toys, deliberately playful brands, and only on one or two beats per
piece, with everything else calm.

## When to use it (and when not)
- Best for: gaming, toys, kids' products, meme-aware brands, a single "BOOM" moment in an otherwise clean edit.
- Avoid when: premium, luxury, institutional, serious topics; more than 2 words in a piece; on faces.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | |
| Starburst | a 22-point star polygon (`clip-path`) behind the word, burst colour | size from the word length |
| Pop word | bright fill, 6 px black stroke, double hard shadow (9 px colour + 16 px black), rotated | cycles 6 combos |
| Everything else | stays calm (tags, counters in the normal theme look) | `plain: true` opts a stomp out of pop |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Word | `t` | 0.16 s, scale `from` (2.0) → 1, opacity 0 → 1, + frame shake (1.0) + flash | power4.out | to `end` | 0.12 s fade | linear |
| Starburst | t + 0.03 | 0.22 s, scale 0.2 → 1, opacity 0 → 0.95 | back.out(2.5) | with the word | with the word | — |

- Shake (adkit): x −12, +9, −5, 0 px · y +5, −4, +2, 0 px over 0.04/0.04/0.04/0.06 s; flash 0.3 → 0 in 0.14 s.
- Combos, in order (fill, offset shadow, burst): `#FFD60A / #FF2D87 / #00E5FF`, `#00E5FF / #FF3D00 / #FFD60A`,
  `#FF2D87 / #FFD60A / #7B2CFF`, `#B6FF00 / #7B2CFF / #FF2D87`, `#FF7A00 / #00E5FF / #FFD60A`, `#FFFFFF / #FF2D87 / #00E5FF`.
- Rotation cycles −4°, 3°, −2°, 4° per pop word; the burst is rotated twice as much.
- The signature move: **the burst behind the slam**: the star pops 0.03 s after the word with an elastic back-ease,
  so the word seems to punch a hole in the frame.

## Typography
- The theme's display face (theme `guyaga` → Anton; the sample used `tech` → Michroma). Anton is the classic comic read.
- Hebrew: Karantina 700 (theme `he_bold`), one short word; the stroke is 6 px, keep size ≥ 160 px so letters stay open.
- Max copy: 1 word, ≤ 8 letters (the burst width = letters × size × 0.56 + size × 0.9).

## Colour and surface
- The six combos above are hard-coded (`adkit.POP`); to use brand colours, edit your own copy of the list in the spec
  (see Build) rather than the kit.
- Word: `-webkit-text-stroke: 6px #111; paint-order: stroke fill; text-shadow: 9px 9px 0 <shadow>, 16px 16px 0 #111`.
  Burst: solid fill, height = size × 1.65.

## Layout and safe zones (1920×1080 canvas)
- Centred on `x, y` (align c), typically x 960, y 200–250 (upper third) on a beat shot where the top is plain.
- The burst extends ~0.45 × size beyond the word on each side: keep x within 96 + burst/2 … 1824 − burst/2.
- 9:16: 1 short word, size ≤ 200 px.

## What the footage must give you
- Shoot it like this: cuts OK (max 5), 10–20 s · subject centred, upper area free on the beat shots · 25 % free at the
  top · any smooth move · no tracking · a music beat grid.
- Tracking: none. Matte: none.
- Good: a clear hit in the music and an empty top third. Bad: faces in the top third.

## Build it
### A. With the kit
The `pop` flag lives on the theme and no stock theme sets it, so switch it on from a `.py` spec (run_ad loads the spec
in the same process as adkit, so this works without editing the kit):
```python
import adkit
adkit.THEMES["pop"] = dict(adkit.THEMES["guyaga"], pop=True)       # Anton + comic pop
# optional brand combos (fill, offset shadow, burst):
# adkit.POP[:] = [("#FFD60A", "#FF2D87", "#00E5FF"), ("#FFFFFF", "#FF2D87", "#00E5FF")]
SPEC = {"theme": "pop",
 "palette": {"acc": "#FF2D87", "ink": "#111111", "lt": "#FFFFFF", "panel": "rgba(10,10,10,.8)", "sub": "#dddddd"},
 "clip": "clips/my_game.mp4", "music": "shared/sfx/my_music.mp3",
 "elements": [
  {"type": "stomp", "text": "BOOM", "x": 960, "y": 230, "size": 200, "t": 4.02, "end": 5.4},
  {"type": "stomp", "text": "LEVEL UP", "x": 960, "y": 220, "size": 170, "t": 9.5, "end": 11.0},
  {"type": "stomp", "text": "MY GAME", "x": 960, "y": 900, "size": 120, "plain": True, "t": 12.0}]}
```
```bash
python scripts/run_ad.py MY_AD --spec specs/MY_AD.py --render
```
| Key (stomp in a pop theme) | Meaning | Default |
|---|---|---|
| text, t, end, x, y, size | the word | size 200 |
| from | entrance scale | 2.0 |
| burst | draw the starburst | true |
| plain | skip the pop look for this word | false |

### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```html
<div class="st" id="p1" style="left:960px;top:230px">
  <div class="bu" style="width:628px;height:330px;background:#00E5FF;clip-path:polygon(50% 0%,58% 22%,78% 6%,72% 30%,98% 24%,80% 44%,100% 56%,76% 62%,90% 86%,64% 76%,58% 100%,48% 80%,34% 98%,32% 74%,8% 86%,20% 62%,0% 50%,22% 40%,4% 18%,30% 26%,26% 2%,44% 20%);transform:translate(-50%,-50%) rotate(-8deg)"></div>
  <span style="font:200px Anton;color:#FFD60A;-webkit-text-stroke:6px #111;paint-order:stroke fill;text-shadow:9px 9px 0 #FF2D87,16px 16px 0 #111;transform:translate(-50%,-50%) rotate(-4deg)">BOOM</span>
</div>
```
```js
tl.fromTo("#p1 span", {opacity: 0, scale: 2}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, T); shake(T);
tl.fromTo("#p1 .bu", {opacity: 0, scale: .2}, {opacity: .95, scale: 1, duration: .22, ease: "back.out(2.5)"}, T + .03);
tl.to("#p1", {opacity: 0, duration: .12}, END - .12);
```

## Adapting it to the user's project
- Content: onomatopoeia or one power word; never a product claim or a price.
- Language: Hebrew → `dict(adkit.THEMES["he_bold"], pop=True)`.
- Brand: replace `adkit.POP` in the spec with 2–3 brand combos.
- Vertical 9:16: smaller, centred.
- Longer or shorter clips: 1–2 pops per piece regardless of length.

## Sound
- Soft sub thump (0.45) on each stomp (adkit); a comic "whoosh" or "boing" belongs in the music/SFX mix, not the kit.

## Pitfalls and QA checklist
- [ ] Confirm the brand is playful; for anything premium propose #10 or #01 instead.
- [ ] ≤ 2 pop words; everything else `plain` or other elements.
- [ ] Burst inside the frame; no pop over a face.
- [ ] The theme flag was set in the spec (otherwise you get plain stomps); frames checked + `scripts/qa.py` "ship".
