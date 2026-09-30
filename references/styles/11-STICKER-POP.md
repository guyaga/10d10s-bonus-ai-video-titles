# #11 STICKER-POP · Sticker words

> Heavy white sticker words with a thick ink outline and a hard offset shadow slap onto the frame next to each piece on
> the beat, with a red index tag and a tilted white price sticker: the loudest of the runway family that still reads
> premium.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/sticker-pop.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/D1_stomp_sticker_v2.mp4
> Runner: run_style STOMP-ESCORT (the escort builder draws exactly this word style) · Example: examples/stomp-escort/ · per-garment original: references/recipes/legacy_shots.py → `D1S`

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: drops, streetwear, sneakers, merch, anything that should feel like a sticker slapped on the video; short
  10 s product walks.
- Avoid when: luxury/quiet brands (use #03); faces in close-up (stickers next to a face feel like memes); more than one
  word per item.

## How it differs from #01 STOMP-ESCORT
Same word style, different placement. The escort (#01) rides beside the subject's whole-body box and scales with her.
The sticker version (the original `D1S` recipe) pins **each word to its own garment** (coat, bag, boots) with an anchor
and an offset, so the stickers sit on/next to the actual piece. With the kit today you get the #01 placement (one follow
object); for per-garment placement adapt `D1S` (below, section B) or run one escort per garment track.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | plate 0.18 in the sample |
| Sticker group per item | index tag · giant sticker word · price sticker | left groups align right, right groups align left |
| Brand bug | serif brand box + accent tag | 96 / 72 |
| Finale | dim + THE LOOK + image row + total | full frame |
| Flash | white, 0.45 on each stomp | |

## Timing and motion
Beat grid of the sample: `B(i) = 0.51 + 0.5 i` (120 BPM measured on the track). Items on beats 1, 4, 7, 10, 13
(every 1.5 s); finale on beat 16.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Index tag | B(i) − 0.12 | 0.12 s, y 20 → 0 | power3.out | until next item | group: opacity 0, scale 0.85, 0.12 s, 0.14 s before the next item | power2.in |
| Sticker word | B(i) | 0.16 s, scale 1.9 → 1 + shake + flash | power4.out | until next item | with group | — |
| Price sticker | B(i + 1) | 0.18 s, scale 1.5 → 1, y 30 → 0 | back.out(2.2) | with group | with group | — |
| Brand | B(0) | stomp from 1.5 | power4.out | to B(15) − 0.1 | 0.12 s | — |
| Finale | B(16) | dim 0.15 s; THE LOOK stomp from 2.2; images 0.16 s stagger 0.1 at B(17); total stomp from 1.8 at B(18) | power4.out / back.out(2) | to end | — | — |

- Shake: x −14, +11, −6, 0 · y +6, −5, +3, 0 px over 0.04/0.04/0.04/0.06 s; flash 0.45 → 0 in 0.14 s (power2.out).
- The signature move: **the sticker read**: paper fill + 3 px ink stroke + 7 px 7 px 0 ink shadow on a 180 px Anton
  word, and a price sticker tilted −4° (left) / +3° (right) with its own 8 px hard shadow. Everything has an ink outline,
  so it reads on any footage like a physical sticker.

## Typography
- Latin: word Anton 180 px (D1S) / 170 px (escort builder), tracking .01em; index Archivo 700 22 px .14em; product name
  Bodoni Moda italic 32 px; price Archivo 700 34 px.
- Hebrew: word Karantina 700 (`fonts.display`), name Suez One (`fonts.serif`), labels/price Secular One (`fonts.body`);
  `currency: "ש״ח"`. One Hebrew word per sticker.
- Max copy: word ≤ 8 letters; name ≤ 22 characters.

## Colour and surface
- Sample: ivory `#f6f1e8` fill, ink `#16130f`, hot `#ff3d2e`. For pure-white stickers set `"colors": {"paper": "#ffffff"}`.
- Word: fill paper, `-webkit-text-stroke: 3px ink`, `text-shadow: 7px 7px 0 ink`. Price sticker: paper, 3 px ink border,
  `box-shadow: 8px 8px 0 ink`, image 112 × 112 on `#ede6da`. Index tag: hot fill, ink text, 3 px ink border.

## Layout and safe zones (1920×1080 canvas)
- Per-garment anchors in the sample (object, anchor, dx, dy): coat `l` −40, −40 (left) · knit on coat `tr` +40, +120
  (right) · trousers on coat `l` −40, +330 (left) · bag `r` +50, −60 (right) · boots `l` −60, +20 (left). Low garments
  (trousers, boots) anchor the group's bottom edge so it grows upward.
- Keep the subject centred with ≥ 28 % free on both sides; keep stickers off the face.
- 9:16: one sticker at a time, centred under the subject.

## What the footage must give you
- Shoot it like this: one take, no cuts, 8–30 s · full body, centred, walks toward camera · 30 % free both sides · slow
  dolly back matching the walk, or locked-off.
- Tracking: whole body (`model`) for the kit route; for per-garment stickers also each garment (`coat`, `bag`, `boots`)
  in the vtrack objects.
- Matte: no.
- Good: a clear full-body walk, garments distinct in colour. Bad: garments hidden by others, crowds.

## Build it
### A. With the kit
```bash
python scripts/run_style.py STOMP-ESCORT --spec my_spec.json --render
```
All keys as #01 STOMP-ESCORT. A minimal sticker spec (10 s walk, one item every 3 beats like the sample):
```json
{
 "name": "my-stickers",
 "clip": "clips/my_walk.mp4", "track": "tracks/my_walk_vtrack.json", "follow": "model",
 "beat": {"bpm": 120, "offset": 0.51},
 "brand": {"name": "MY BRAND", "tag": "DROP 02", "beat": 0},
 "items": [
  {"key": "hoodie", "word": "HOODIE", "name": "Heavy Hoodie", "price": 120, "image": "stills/hoodie.png", "side": "L", "beat": 1},
  {"key": "cap",    "word": "CAP",    "name": "Six-Panel Cap", "price": 45, "image": "stills/cap.png", "side": "R", "beat": 4},
  {"key": "kicks",  "word": "KICKS",  "name": "Court Low", "price": 150, "image": "stills/kicks.png", "side": "L", "beat": 7}
 ],
 "finale": {"title": "THE FIT", "beat": 10, "label": "three pieces"},
 "colors": {"paper": "#ffffff", "ink": "#111111", "accent": "#ff3d2e"}
}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```html
<!-- one group per garment, driven by the tracker: data-follow / data-anchor / data-dx / data-dy -->
<div class="grp L" id="g-coat" data-follow="coat" data-anchor="l" data-dx="-40" data-dy="-40"><div class="inner">
  <span class="idx">01 / 05</span><span class="word">COAT</span>
  <div class="stk"><img src="assets/items/coat.png"><div><span class="nm">The Camel Overcoat</span><span class="pr">$890</span></div></div>
</div></div>
```
```css
.word{font:180px/1 Anton;color:#f6f1e8;-webkit-text-stroke:3px #16130f;text-shadow:7px 7px 0 #16130f;white-space:nowrap}
.stk{display:flex;gap:16px;margin-top:44px;padding:12px 18px 12px 12px;background:#f6f1e8;border:3px solid #16130f;box-shadow:8px 8px 0 #16130f}
.grp.L .stk{transform:rotate(-4deg)} .grp.R .stk{transform:rotate(3deg)}
.grp.L .inner{right:0;align-items:flex-end} .grp.R .inner{left:0;align-items:flex-start}
```
```js
const B = (i) => +(0.51 + 0.5 * i).toFixed(3);
ITEMS.forEach(([key, bi], k) => {
  const g = `#g-${key}`;
  tl.fromTo(`${g} .idx`, {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .12, ease: "power3.out"}, B(bi) - .12);
  stomp(`${g} .word`, B(bi));                                // scale 1.9 -> 1, .16 s, power4.out + shake
  tl.fromTo(`${g} .stk`, {opacity: 0, scale: 1.5, y: 30}, {opacity: 1, scale: 1, y: 0, duration: .18, ease: "back.out(2.2)"}, B(bi + 1));
  tl.to(`${g} .inner`, {opacity: 0, scale: .85, duration: .12, ease: "power2.in"}, (k < ITEMS.length - 1 ? B(ITEMS[k + 1][1]) : B(15)) - .14);
});
```

## Adapting it to the user's project
- Content: one noun per piece, real name and price; 3–5 pieces in 10 s.
- Language: Hebrew fonts override + ש״ח (see Typography).
- Brand: paper white or cream, ink near-black, accent = brand action colour.
- Vertical 9:16: one centred sticker at a time.
- Longer or shorter clips: 1.5 s per item at 120 BPM; slow music → 2 beats per item.

## Sound
- Soft thump 0.45 on brand, every word, THE LOOK and the total; soft click 0.3 on every price sticker; music 0.75;
  plate 0.18 (sample) / 0.15 (kit default).

## Pitfalls and QA checklist
- [ ] Stickers sit next to their garment (per-garment) or beside the subject (escort), never on the face.
- [ ] Every word lands on a beat; the price sticker a beat later.
- [ ] Low garments' groups grow upward (they must not run off the bottom edge).
- [ ] Prices and total correct; Hebrew ש״ח; frames checked + `scripts/qa.py` "ship".
