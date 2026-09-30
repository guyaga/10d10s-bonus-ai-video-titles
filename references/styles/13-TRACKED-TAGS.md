# #13 TRACKED-TAGS · Tracked callout tags

> The clean English fact layer: numbered glass tags and leader-line callouts that ride each tracked object or part frame
> by frame, one stat counter, and a quiet lockup with the price.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/tracked-tags.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E6_guyaga_aero_sneaker.mp4
> Runner: run_ad (adkit `tag` / `callout` / `counter`, theme `guyaga`) · Example: examples/E6_sneaker_sx.py (keep only tag/callout/counter/ring/chip/lockup)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: product films (parts, materials, specs), interiors (each piece + price), jewellery, food (ingredients,
  origin), any footage where the image is the hero and the copy is facts.
- Avoid when: the objects move fast or leave the frame (tags jump); there is no single clear object to point at; the
  brief wants emotion over facts (use #05 / #10).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | 0.35 in the sample |
| Behind word (optional) | brand word behind the product, accent colour | `stomp` + `behind` + matte |
| Ring (optional) | 3 rotating rings on a tracked object | `ring` |
| Leader lines | white 2.5 px path from a point inside the tracked box → elbow → the callout box; 8 px accent dot; pulsing ring | `callout` (drawn in one SVG layer) |
| Callout boxes | glass panels at fixed screen positions (left/right columns) | title + sub |
| Tags | numbered glass tags attached to a tracked object (01, 02 …) | `tag` |
| Counter | big number counting to the stat, with a label and a progress bar | `counter` |
| Chip, lockup | top-left context chip; bottom-centre brand · rule · line | `chip`, `lockup` |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Callout box | `t` | 0.35 s: opacity 0 → 1, y 14 → 0, clip-path reveals top → bottom | expo.out | to `end` | 0.12 s fade | linear |
| Leader line + dot | `t` | appears with the box; redrawn every frame to the tracked point; pulse ring radius 12 → 22 px, opacity 1 → 0, 1.6 cycles/s | — | to `end` | disappears at `end` (see Pitfalls) | — |
| Tag | `t` | 0.35 s: clip-path wipe left → right + fade; accent underline scaleX 0 → 1 in 0.45 s at t + 0.15 | expo.out / power3.out | to `end` | 0.12 s | — |
| Ring | `t` | scale 1.6 → 1 in 0.35 s; rotation 160 × spin, −110 × spin, 25 × spin °/s | expo.out | to `end` | 0.12 s | — |
| Counter | `t` | stomp from 1.5 (0.16 s) + shake; value cubic-out a → b between t0 and t1 | power4.out | to `end` | 0.12 s | — |
| Chip | `t` | 0.35 s, x −20 → 0 | power3.out | to `end` | — | — |
| Lockup | `t` | stomp from 1.4 | power4.out | to end | — | — |

- Stagger: callouts 0.5 s apart (sample: 5.0 / 5.5 / 6.0 / 6.5 s), all out together (9.4 s) while the parts are separated.
- Sync: the window where each part is visible and stable (from the footage, not the music). Tags follow; callouts point.
- The signature move: **the leader line that lives on the object**: the box stays still in a clean column, the line's
  start point is recomputed every frame at (fx, fy) inside the object's tracked box, with a pulsing accent dot on it.

## Typography
- Latin (theme `guyaga`): tag/callout titles in the display face Anton (callout 32 px, tag 34 px; the sample tightens to
  30 px .03em); subs in Space Mono (callout 17 px, tag 17 px .08em; sample 15 px .14em uppercase); tag number Space Mono
  15 px .2em; chip title 40 px; counter number 140 px; lockup brand 70 px. For a softer read use theme `tech` (Michroma
  + Sora) or `travel` (Sora).
- Hebrew: theme `he_bold` or `he_premium` → titles and subs in Secular One (forced by the RTL css), numbers in the
  display face; callouts right-aligned (`text-align:right` in css), prices ש״ח, numbers glued ("38 גרם").
- Max copy: title ≤ 20 characters, sub ≤ 28; box width 330–360 px fixed in the sample.

## Colour and surface
- Palette: acc `#E63B2E`, ink `#111111`, lt `#F5F3EE`, panel `rgba(14,14,14,.78)`, sub `#E4E1DB`.
- Glass: `var(--panel)` + `backdrop-filter: blur(10px) saturate(1.15)` + 1 px `rgba(255,255,255,.22)` border + 14 px
  accent corner brackets. Leader line in `lt`, dot `acc` with `lt` stroke. Sample css removes the white flash and the
  chroma split (`.st span.c{text-shadow:0 18px 70px rgba(0,0,0,.55)!important}`, `#flash{display:none}`).

## Layout and safe zones (1920×1080 canvas)
- Callout boxes in columns: left x −10 (box hangs just inside the edge) and right x 1520–1530; rows y 200 / 430 / 660 /
  800. The line elbows 60 px before the box; the box's vertical anchor is y + 34.
- Tags: `follow` + `anchor` (default `r`), `dx` 24, `side: "l"` to hang left.
- Counter left column (x 90, y 620); lockup bottom 112 centred.
- 9:16: two callouts max, stacked under the product, lines up to it.

## What the footage must give you
- Shoot it like this: cuts OK (max 4), 10–20 s · subject centred at medium size · 20 % free both sides · slow orbit,
  slow glide or locked; no fast moves.
- Tracking: each labelled object or part as its own vtrack object. For moving parts use dedicated small anchor objects
  (the sample tracks `a_upper`, `a_mid`, `a_plate`, `a_out` only inside the window where the layers are separated).
- Matte: only for the behind word.
- Good: product ≤ 60 % of the frame, plain background both sides. Bad: parts that overlap or blur.

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/my_product.mp4 objects.json tracks/my_product_vtrack.json --preview check.mp4
python scripts/run_ad.py MY_AD --spec specs/MY_AD.py --render
```
| Element | Keys | Defaults |
|---|---|---|
| callout | `obj, fx, fy, title, sub, x, y, t, end` | fx/fy 0.5 |
| tag | `title, sub, follow, anchor, dx, dy, side, t, end` | anchor r, dx 24, side r |
| counter | `t0, t1, a, b, dec, pre, suf, label, x, y, size, t, end` | size 160 |
| ring | `obj, r, spin, t, end` | r 180, spin 1 |
| chip / lockup | `text, sub, t` / `brand, line, t` | — |

A minimal spec:
```python
SPEC = {"theme": "guyaga",
 "palette": {"acc": "#E63B2E", "ink": "#111111", "lt": "#F5F3EE", "panel": "rgba(14,14,14,.78)", "sub": "#E4E1DB"},
 "clip": "clips/my_product.mp4", "track": "tracks/my_product_vtrack.json", "music": "shared/sfx/my_music.mp3",
 "css": "#flash{display:none}\n.st span.c{text-shadow:0 18px 70px rgba(0,0,0,.55)!important}\n.co{width:330px;box-sizing:border-box}",
 "elements": [
  {"type": "chip", "text": "INSIDE THE LAMP", "sub": "MY BRAND · 2026", "t": 0.4, "end": 4.0},
  {"type": "callout", "obj": "shade", "fx": 0.5, "fy": 0.4, "title": "HAND-BLOWN GLASS", "sub": "3 mm · amber", "x": -10, "y": 200, "t": 1.0, "end": 6.0},
  {"type": "callout", "obj": "base", "fx": 0.5, "fy": 0.5, "title": "SOLID BRASS", "sub": "brushed finish", "x": 1530, "y": 660, "t": 1.5, "end": 6.0},
  {"type": "counter", "t0": 6.2, "t1": 7.2, "a": 0, "b": 2400, "suf": " K", "label": "WARM LIGHT", "x": 90, "y": 620, "size": 140, "t": 6.2, "end": 8.5},
  {"type": "lockup", "brand": "MY BRAND", "line": "$240", "t": 8.8}]}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// per-frame: redraw every leader from a point inside the tracked box to its fixed box (cy = y + 34; cx = x or x + 400)
window.onPlace = (t) => {
  for (const c of CALLOUTS) {
    const b = boxAt(c.obj, t), L = $("#" + c.id + "L"), D = $("#" + c.id + "D"), R = $("#" + c.id + "R");
    if (!b || t < c.t || t >= c.end) { L.setAttribute("d", ""); D.setAttribute("cx", -50); R.setAttribute("cx", -50); continue; }
    const px = b[0] + (b[2] - b[0]) * c.fx, py = b[1] + (b[3] - b[1]) * c.fy, cy = c.y + 34, cx = c.x > 960 ? c.x : c.x + 400;
    L.setAttribute("d", `M${px},${py} L${cx + (cx > px ? -60 : 60)},${cy} L${cx},${cy}`);
    D.setAttribute("cx", px); D.setAttribute("cy", py);
    R.setAttribute("cx", px); R.setAttribute("cy", py); R.setAttribute("r", 12 + 10 * ((t * 1.6) % 1)); R.setAttribute("opacity", 1 - ((t * 1.6) % 1));
  }
};
for (const c of CALLOUTS) {
  tl.fromTo("#" + c.id, {opacity: 0, y: 14, clipPath: "inset(0 0 100% 0)"}, {opacity: 1, y: 0, clipPath: "inset(0 0 0% 0)", duration: .35, ease: "expo.out"}, c.t);
  tl.to("#" + c.id, {opacity: 0, duration: .12}, c.end - .12);
}
```

## Adapting it to the user's project
- Content: one fact per part: name (title) + measurable proof (sub: material, weight, size, price). 3–5 callouts.
- Language: Hebrew → he themes, right-aligned boxes, ש״ח.
- Brand: `acc` = brand colour (dots, corner brackets, underlines, counter bar); keep the glass dark.
- Vertical 9:16: 2 callouts, stacked.
- Longer or shorter clips: callouts only inside the window where their object is visible and still.

## Sound
- adkit thumps (0.45) on counters, stomps and the lockup only; for tags add a UI pop in the music or via a custom cue.
  Music 0.55, plate 0.35 in the sample.

## Pitfalls and QA checklist
- [ ] Every `obj` exists in the track for the whole `t`–`end` window (a missing box hides the line but leaves the box).
- [ ] The leader line disappears instantly at `end` while the box fades over 0.12 s: the sample adds a css fade on the
      line/dot/ring (`#e2L{animation:coOutS .12s linear <end-0.12>s 1 both}` with `stroke-opacity` keyframes).
- [ ] No white flash / chroma split on a premium product (css above).
- [ ] Boxes inside the frame (x −10 hangs 10 px off-frame by design; check long titles); frames checked + `scripts/qa.py` "ship".
