# #01 STOMP-ESCORT · Escort stomp

> Each advertised item gets a giant sticker word that slams in beside the walking subject on the beat and rides with her,
> with a red `01 / 05` index tag above it and a white price sticker below it.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/stomp-escort.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/D2_runway_full_countdown_30s.mp4
> Runner: run_style STOMP-ESCORT (`scripts/styles/runway.py`) · Example: examples/stomp-escort/ (runnable demo: examples/demo/)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: runway / catwalk walks, "piece by piece" product reveals on a person (outfit, gear kit, uniform), shoppable
  lookbooks, any one-take shot of one subject walking toward camera.
- Avoid when: the subject is small or off-centre the whole time (the escort scales down to 42 % and gets lost); there are
  cuts (the tracking box jumps and the words teleport); more than ~6 items (each item needs ~1.5–3 s); quiet premium
  tone (use #03 GLASS-CALLOUT or #10 PRESIDENTIAL-SERIF).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | audio at `plate_vol` 0.15 by default |
| Big word (optional) | 520 px accent word pinned above the subject's head | behind the subject when a `matte` is given (see #02) |
| Look label (optional) | small `LOOK 07` sticker riding the top of the subject's box | 44 px, scales with the subject (min 60 %) |
| Escort group, one per item | index tag + giant word + price sticker, stacked | rides beside the tracked box: left side ends 30 px left of the box, right side starts 30 px right of it |
| Brand bug (optional) | serif brand box + accent tag, top-left | x 96, y 72 |
| Finale (optional) | dim + 300 px title + product image row + total | full frame |
| Flash | full-frame white layer | 0.4 × amount opacity on every hit |

## Timing and motion
All times are on a beat grid: `B(n) = offset + n × 60 / bpm` (defaults bpm 120, offset 0). Measure `bpm` and `offset`
from the user's music with librosa (`beat_track`) and put them in the spec.

| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Index tag `01 / 05` | B(item.beat) − 0.12 s | 0.12 s, y 16 → 0, opacity 0 → 1 | GSAP default (power1.out) | until the next item | with the group | — |
| Giant word | B(item.beat) | 0.16 s, scale 1.9 → 1, opacity 0 → 1 | power4.out | until the next item | group: opacity 0, scale 0.85, 0.12 s, starting 0.14 s before the next item's beat | power2.in |
| Price sticker | B(item.beat + 1) (one beat later) | 0.18 s, scale 1.5 → 1, y 24 → 0 | back.out(2.2) | with the group | with the group | — |
| Brand bug | B(brand.beat) (default beat 1) | stomp from 1.5 | power4.out | until END | opacity 0, 0.15 s at END | — |
| Look label | B(look.beat) (default 4) | 0.2 s, y 20 → 0 | back.out(2) | until B(look.until) (default 9) | 0.15 s fade | — |
| Big word | B(big.beat) | stomp from 2.4 | power4.out | until B(big.until) | 0.25 s fade | — |
| Finale | B(finale.beat) | dim 0.15 s; title stomp from 2.2; images 0.16 s each, stagger 0.1 s, from B(beat+1); total stomp from 1.8 at B(beat+2) | power4.out / back.out(2) | to the end | — | — |

`END` = the earliest of big_word / finale / countdown beats, else the last item's beat + 4.

- Stagger: one item per N beats. The sample uses 3 beats (1.5 s) at 120 BPM; the example spec uses 6 beats (3 s) so a
  30 s walk is covered. Rule: each item must be on screen ≥ 1.5 s.
- Beat/voice sync: every word lands ON a beat; the sticker lands one beat later (a two-hit rhythm: word, then price).
- The signature move: **the stomp + shake**. On every hit the whole overlay layer shakes (x −14, +11, −6, 0 px; y +6, −5,
  +3, 0 px over 0.04 + 0.04 + 0.04 + 0.06 s) and a white flash drops from 0.4 → 0 in 0.14 s. The word itself scales down
  from 1.9 × in 0.16 s. Then **the escort**: every frame the group is re-placed beside the subject's tracked box and
  scaled by the subject's height: `s = clamp(h / 820, 0.42, 1)`; the price sticker has its own floor
  (`sticker_min_scale`, default 0.62) so the price stays legible while she is far away.

## Typography
- Latin: word Anton 400, 170 px at scale 1 (fills ~1.5 × its width at scale 1.9 when landing), tracking .01em, uppercase
  copy; index tag Archivo 700 22 px, tracking .14em; sticker name Bodoni Moda italic 32 px; price Archivo 700 34 px;
  brand Bodoni Moda 600 40 px tracking .22em + Anton 40 px tag.
- Hebrew: this builder's word font is Latin (Anton); for Hebrew copy set `"fonts": {"display": "Karantina", "serif":
  "Suez One", "body": "Secular One"}` (Karantina 700 is the word, Suez One the product name, Secular One labels/price).
  Keep words to one Hebrew word; do not mirror the layout (sides are physical left/right of the subject). Prices: set
  `"currency": "ש״ח"` (the money helper writes `890 ש״ח` after the number); never `₪` (none of the three faces has it).
- Max copy: word ≤ 8 characters (CASHMERE is the longest that works at full scale); sticker name ≤ 22 characters;
  index tag is automatic.

## Colour and surface
- Roles: `paper` (word fill, sticker background) `#f6f1e8`, `ink` (outlines, shadows, text) `#16130f`, `accent` (index tag,
  price chip) `#ff3d2e`. Brand colours: set `"colors": {"paper", "ink", "accent"}`; keep paper light and ink dark, the
  word is readable on any footage only because of the ink stroke + hard shadow.
- Surfaces: word = paper fill, 3 px ink stroke, 7 px 7 px 0 ink hard shadow. Index tag = accent fill + 3 px ink border.
  Sticker = paper, 3 px ink border, 8 px 8 px 0 ink shadow, rotated −4° (left side) / +3° (right side); image 112 × 112
  on `#ede6da` with 2 px ink border.

## Layout and safe zones (1920×1080 canvas)
- Group anchor: left side → x = box.left − 30, right side → x = box.right + 30; y = box.top + 18 % of the box height.
  Left groups align right (they grow away from the subject), right groups align left.
- Keep the subject centred with ≥ 28 % free width on both sides (the plate gate) so a full-scale group (≈ 520 px wide)
  fits. 5 % safe margin = 96 px left/right, 54 px top/bottom: brand bug sits at 96 / 72.
- 9:16: the kit composes 1920 × 1080. For a vertical delivery, the subject must be centred and you crop the centre
  608 px column; escorts will not fit beside her, so switch to one word stacked above the head (`big_word`) or use
  #05 KINETIC-HE for vertical.

## What the footage must give you
- Shoot it like this: one take, no cuts, 10–30 s · full body, centred, walks toward camera · 30 % free on both sides ·
  locked-off or very slow push-in (or a dolly back matching her pace).
- Tracking: one full-body box (`follow`, default `"model"`), vtrack.py:
  ```json
  {"context": "One continuous take: a model walks toward the camera wearing …",
   "objects": [{"name": "model", "desc": "the whole body of the single model, head to feet (tight box)"}]}
  ```
  Run `python scripts/vtrack.py clip.mp4 objects.json tracks/my_vtrack.json --preview check.mp4` and watch the preview.
- Matte: not needed (only for `big_word` behind the subject).
- Good: steady camera, one subject, clean side space, feet in frame. Bad: crowd behind her, cuts, subject hugging an edge,
  feet cropped for long stretches (the box height then shrinks the escort).

## Build it
### A. With the kit
```bash
python scripts/run_style.py STOMP-ESCORT --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| track | vtrack JSON (1920×1080 canvas) | required |
| follow | tracked object the escorts ride | `"model"` |
| items | `[{key, word, name, price, image?, side "L"/"R", beat}]` | required (or `countdown`) |
| beat | `{"bpm", "offset"}` | 120, 0.0 |
| brand | `{"name", "tag", "beat"}` | none (beat 1) |
| look | `{"text", "beat", "until"}` | none (4, 9) |
| sticker_min_scale | price sticker scale floor | 0.62 |
| big_word | `{"text", "beat", "until"}` (behind when `matte`) | none (until = beat + 5) |
| finale | `{"title", "beat", "label"}` | none ("THE LOOK", "N pieces") |
| countdown | the sale block, see #04 | none |
| colors | `{"paper", "ink", "accent"}` | `#f6f1e8 / #16130f / #ff3d2e` |
| fonts | `{"display", "serif", "body"}` | Anton / Bodoni Moda / Archivo |
| currency | `"$"`, `"€"`, `"£"` (prefix) or any text (suffix) | `"$"` |
| music, music_vol, plate_vol, matte, name, thumps | media and mix | –, 0.75, 0.15, –, "stomp-escort", true |

A minimal spec for a generic project:
```json
{
 "name": "my-escort",
 "clip": "clips/my_walk.mp4",
 "track": "tracks/my_walk_vtrack.json",
 "follow": "model",
 "beat": {"bpm": 118, "offset": 0.21},
 "brand": {"name": "MY BRAND", "tag": "SS27", "beat": 1},
 "items": [
  {"key": "jacket", "word": "JACKET", "name": "Signal Puffer", "price": 340, "side": "L", "beat": 5},
  {"key": "pants",  "word": "CARGO",  "name": "Grid Cargo Pant", "price": 180, "side": "R", "beat": 9},
  {"key": "shoes",  "word": "RUNNER", "name": "Low Runner", "price": 210, "side": "L", "beat": 13}
 ],
 "finale": {"title": "DROP 01", "beat": 16, "label": "three pieces"},
 "colors": {"paper": "#f2f1ec", "ink": "#0e0e10", "accent": "#ff6a13"},
 "music": "shared/sfx/my_music.mp3"
}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// tl = window.__timelines["main"] (paused); boxAt(name, t) -> [x0,y0,x1,y1] from the track; onPlace(t) runs every frame
const B = (i) => +(OFFSET + (60 / BPM) * i).toFixed(3);
function shake(at, a = 1) {
  tl.to(["#stage", "#stage2"], {keyframes: [{x: -14*a, y: 6*a, duration: .04}, {x: 11*a, y: -5*a, duration: .04},
        {x: -6*a, y: 3*a, duration: .04}, {x: 0, y: 0, duration: .06}], ease: "none"}, at);
  tl.fromTo("#flash", {opacity: .4*a}, {opacity: 0, duration: .14, ease: "power2.out"}, at);
}
function stomp(sel, at, from = 1.9) { tl.fromTo(sel, {opacity: 0, scale: from}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, at); shake(at); }
window.onPlace = (t) => {                                  // the escort: re-place and re-scale every frame
  const m = boxAt("model", t); if (!m) return;
  const h = m[3] - m[1], s = Math.max(.42, Math.min(1, h / 820));
  for (const [key, side] of ITEMS) {
    const el = document.getElementById("e-" + key), sc = el.firstElementChild;
    el.style.left = (side === "L" ? m[0] - 30 : m[2] + 30) + "px"; el.style.top = (m[1] + h * .18) + "px";
    sc.style.transform = side === "L" ? `translateX(-100%) scale(${s})` : `scale(${s})`;
    el.querySelector(".stk").style.scale = String(Math.max(.62, s) / s);   // sticker never below 62 %
  }
};
ITEMS.forEach(([key, side, bi], k) => {
  tl.fromTo(`#e-${key} .idx`, {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .12}, B(bi) - .12);
  stomp(`#e-${key} .word`, B(bi));
  tl.fromTo(`#e-${key} .stk`, {opacity: 0, scale: 1.5, y: 24}, {opacity: 1, scale: 1, y: 0, duration: .18, ease: "back.out(2.2)"}, B(bi + 1));
  tl.to(`#e-${key} .inner`, {opacity: 0, scale: .85, duration: .12, ease: "power2.in"}, (k < ITEMS.length - 1 ? B(ITEMS[k+1][2]) : END) - .14);
});
```

## Adapting it to the user's project
- Content: one short noun per item (what the piece IS: COAT, CARGO, RUNNER), the real product name, the real price.
  Order items top-to-bottom or in the order the camera shows them best; alternate sides L/R.
- Language: Hebrew → fonts override above, one Hebrew word per escort, `currency` "ש״ח".
- Brand: 3 colours via `colors`; the brand bug takes the brand name and a season/drop tag.
- Vertical 9:16: see Layout; for vertical-first social use #05/#12.
- Longer or shorter clips: fit the item spacing to the walk: `(last usable second − first readable second) / items`,
  converted to beats. Start items only once the subject is big enough (box height ≥ ~350 px, i.e. scale ≥ 0.42).

## Sound
- Soft sub thump (0.45) 0.02 s before every word and on brand / big word / finale / total; soft click (0.3) on every
  sticker; music bed at 0.75, plate audio at 0.15. Turn thumps off with `"thumps": false`.

## Pitfalls and QA checklist
- [ ] Track canvas is 1920 × 1080 (the kit rescales a smaller canvas with a warning; a missing canvas fails).
- [ ] Watch the vtrack preview: the model box must hug her body on every frame; a box that jumps = words jump.
- [ ] No word covers the face: if a side group overlaps her head, move that item to the other side or a later beat.
- [ ] The price is legible at the moment it lands (sticker floor 0.62; raise `sticker_min_scale` if she is far).
- [ ] The group exits before the next item stomps (automatic) and nothing hangs after END.
- [ ] Prices add up in the finale total; Hebrew prices read `ש״ח`, not `₪`.
- [ ] Frames checked at 4–6 moments + `scripts/qa.py` says "ship".
