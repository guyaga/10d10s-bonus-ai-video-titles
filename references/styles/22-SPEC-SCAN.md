# #22 SPEC-SCAN · The product as a lab specimen

> The product is tested on a lab rig: it starts as a volt-green CAD wireframe on a perspective grid and a render-pass scan line wipes it into the real photo; race-timer 7-segment digits flick and lock on its specs; the exploded parts get numbered balloons and are re-rendered as mesh or an FEA heat map right on the real pixels; a force-plate trace spikes on the landing; it ends on the shoebox's end label.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/spec-scan.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E6_guyaga_aero_sneaker_BESPOKE.mp4
> Runner: bespoke (`references/recipes/bespoke/E6_sneaker_bespoke.py`, 15 s) · Example: none shipped (build from the recipe)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: sneakers and sports gear, headphones, phones and hardware, bikes, tools, any engineered product with parts and measurable performance.
- Avoid when: the product has no structure to explode or measure (fashion fabrics, food), the footage has cuts, or the product can't be separated from its background (the wireframe needs a matte).

## The design method (crafted world)
Ask: **how is this product measured and proven where it's made?** A performance shoe is proven in a lab: CAD on a turntable, a scale, stack tests, finite-element stress maps, a force plate, a timing board. So the titles are the lab's readouts, and the product itself is re-rendered by the lab's instruments:
1. **Re-render the real pixels, don't draw on top of them.** The product's matte is passed through SVG filters: `#fWire` (edge detection + a 26 px mesh grid + a volt silhouette ring) and `#fHeat` (luminance banded into a blue → red FEA ramp). Per-frame masks restrict the filter to the whole product, one tracked layer, or a radial spot, so the wireframe and heat map sit exactly on the product.
2. **Data arrives like lab hardware:** 7-segment digits that flick through random values (a seeded hash, 30 fps) and lock on the true value; race-timer boards flip down from a clip.
3. **Label the exploded view like an engineering drawing:** numbered balloons on leader lines, part chips with material and weight.
4. **End on the product's own packaging:** the shoebox end label (model, size run with the size highlighted, barcode, specs), with the slogan printed on it word by word.

Worked example (GUYAGA AERO): CAD turntable θ 0 → 360° while "189 g" locks → scan-wipe into the photo → "04 layers / 00 compromises" → exploded assembly, each part re-rendered (foam as an FEA map) → snap-back flash in the black CAD viewport → the landing: foam heat spikes blue → red with the force-plate peak (2140 N) → "87 % energy return" → shoebox label "runs on air".

It transfers to:
- **Wireless headphones:** the ear cup as a wireframe on a turntable, exploded driver/battery/cushion with balloons, a frequency-response trace instead of the force plate, the box end label with the colourway.
- **A road bike or e-bike:** the frame re-rendered as an FEA stress map on a torque test, balloons on the fork, crank and battery, a power-meter trace on the climb, the spec sticker from the frame tube as the end.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#vp` (behind the matte) | the black CAD viewport: a perspective floor grid (240 px major, 48 px minor, `rotateX(64deg)`), a glowing horizon at 62%, an XYZ axis triad | visible 0 → 1.78 s and again 9.5 → 10.2 s |
| plate + `#matte` | the product cut-out (alpha webm), re-rendered with `#fWire` / `#fHeat` and masked per frame | the core of the style |
| `#scan` | a 4 px volt line with a double glow, sweeping left → right | CAD right of the line, photo left of it |
| `#tt` turntable | an ellipse (rx 560, ry 62) under the product with ticks every 10°, a marker, and "TURNTABLE θ 000° ω 2.5 rev/s" | only the front half of the ticks is drawn |
| `#tm` lab timer | "RUN 0417" + a running 00:SS.cs timer and a blinking red dot | top centre |
| `.bd` race-timer boards | black boards with a 5 px volt top rule, header row, big 7-segment digits + unit, Hebrew word | three boards |
| `#lab` balloons | leader line + dot + volt balloon (r 31) per part, retracting into the part on the snap-back | 4 parts |
| `.pc` part chips | Hebrew part name 46 px + mono spec 19 px with the balloon number | foam chip carries the FEA colour legend 0.0–2.4 MPa |
| `#gap` | live layer-gap readouts "+0.8 mm" beside the separating stack | during the separation |
| `#fp` force plate | 600 × 190 N-vs-ms graph with a filled trace, a cursor, a PEAK marker and a 7-segment peak value | the landing |
| `#bx` shoebox | the orange end label: lid strip, brand + model, slogan, size run (US, 9 highlighted), barcode + spec lines | the ending |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| CAD viewport + wireframe matte | 0 | on | — | to the scan | clipped away by the scan | — |
| turntable | 0.05 | fades 0.3; θ turns 0 → 360° over 2.2 s | cubic out | — | fades 0.2 by 2.05 | — |
| lab timer | 0.1 | 0.3 | default | — | 0.2 at 12.1 | default |
| board 1 (mass) | 0.32 | 0.18 flip (clip down + y −14) | expo.out | digits lock 0.4 + 0.42 | 0.14 at 2.02 | power2.in |
| render-pass scan | 0.95 | 0.8 across the frame | cubic inOut | — | — | — |
| board 2 (layers / compromises) | 2.02 | 0.18 | expo.out | digits lock 2.1 / 3.354 | 0.14 at 4.58 | power2.in |
| full-shoe wireframe | 2.62 | 0.22 | cubic out | — | 0.22 at 4.46 | — |
| layer gaps | 2.9 | 0.25 | cubic out | live values | 0.16 before 4.62 | — |
| balloons 1–4 | 4.9 / 6.1 / 7.3 / 8.25 | leader 0.2, balloon pops 0.26 (overshoot back-ease 2.2) | cubic out / back | — | retract into the part 9.42 → 9.62 | cubic out |
| part chips | balloon + 0.12 | 0.22 (clip from the reading edge) | expo.out | — | 0.12 at 9.4 | default |
| per-part re-render | upper 4.88, foam (heat) 6.08, plate 7.28, outsole 8.23 | 0.15 | — | ~1.1 s each | 0.15 | — |
| snap-back CAD flash | 9.5 | 0.08 | cubic out | — | 0.32 at 9.86 | — |
| board 3 (energy return) | 10.2 | 0.18 | expo.out | digits lock 10.25 + 0.66 | 0.14 at 12.26 | power2.in |
| force plate | 12.24 | 0.22 (clip down) | expo.out | trace draws 12.4 → 13.4 (0 → 250 ms) | — | — |
| landing heat spike | 12.28 | heat 0.3 → 1.05 at 12.6–12.76, settles to .55 over 0.9 | cubic out | — | 0.4 by 14.3 | — |
| peak readout | 12.68 | 0.08, then scale 1.25 → 1 over 0.25 at 12.72 | back.out(3) | — | — | — |
| shoebox label | 13.02 | 0.42 (x 760 → 0, rotateY −28 → 0, perspective 900) | expo.out | to end | — | — |
| model chip / slogan words | 13.136 / 13.75, 14.214, 14.423 | 0.16 | power4.out / expo.out | — | — | — |
- 7-segment "flick and lock": from `t0` to `t0 + dur + 0.05 × digit`, each digit shows a random digit (25% chance of blank) at 30 fps from a seeded hash, then the true value.
- The signature move: the product re-rendered as wireframe and FEA heat, masked exactly to the real product (or one layer of it) by the matte and the tracked boxes.

## Typography
- Data and labels: **Chakra Petch** 500/700 (a squared technical sans), uppercase, letter-spacing .08–.18em; 7-segment digits are drawn as SVG polygons (100 × 180 cell, 18 px strokes, skewX −7°).
- Hebrew: **Karantina** 700 for the part names and board words (the original used Rubik 800/900; the kit remaps Rubik to Karantina). Sizes: board words 40–44 px, part names 46 px, the box slogan 70 px, the force-plate label 30 px.
- RTL: Hebrew words sit right of the digits on the boards (`direction: rtl` on the word span only); units and specs stay LTR mono.
- Max copy: board word ≤ 3 short words; part name ≤ 14 characters; slogan ≤ 3 words.

## Colour and surface
- Lab black #07080A, volt #D4FF1E (every instrument), off-white #F2F4EE, and orange #FF5B14 only on the shoebox and the hottest stress. FEA ramp: #1426A8 → #0A7BFF → #00D8B0 → #C8FF00 → #FF9A00 → #FF2A10.
- Surfaces: boards `rgba(7,8,10,.9)` with faint horizontal scanlines; balloons solid volt; the box label is flat orange with a fibre texture.
- Brand swap: replace volt with the brand's technical accent (keep it high-luminance) and the box orange with the real packaging colour.

## Layout and safe zones (1920×1080 canvas)
- Boards alternate sides (right 1496/196, left 34/170, right 1506/262), the force plate top-left (36/26), the box top-right (right 40/top 28, 740 wide). Balloons park at fixed side positions (x 395 or 1590) with leaders to the tracked parts.
- The product stays centred with 20% free on each side (the contract).
- 9:16: boards above and below the product; balloons alternate left/right.

## What the footage must give you
- Shoot it like this: one take, no cuts, 10–18 s · the product centred, fully in frame · 20% free on both sides · slow smooth orbit · subject matte required.
- Seedance lines: "FORMAT: One continuous shot, no cuts." / "CAMERA: slow orbit, very smooth. FORBIDDEN: cuts, shake." / "Dark plain studio background with rim light so the product's outline is crisp." / "POSITIVE LOCKS: exactly one product, always the same design, the stated number of layers when separated. No text, no logos, no signage, no UI, no graphics at any time."
- Tracking (vtrack.py): `shoe` (the whole product) + one object per part (`upper`, `midsole`, `plate`, `outsole`) + balloon anchor points per part (`a_upper`, `a_mid`, `a_plate`, `a_out`). Gate: ≥90% coverage.
- Matte: required: `npx hyperframes@0.8.84 remove-background clips/product.mp4 -o mattes/product_alpha.webm` (the kit prints this command if it's missing).
- Good footage: a dark, clean background, the product rotating slowly, an exploded view that separates vertically and rejoins, a landing. Bad: busy backgrounds (the edge filter draws them), cuts, parts that overlap in the explode.

## Build it
### A. With the kit (bespoke route)
```bash
npx hyperframes@0.8.84 remove-background clips/product_720p.mp4 -o mattes/product_alpha.webm
python scripts/vtrack.py clips/product_720p.mp4 product_objects.json tracks/product_vtrack.json
python scripts/run_ad.py PRODUCT --spec specs/product_specscan.py --render
```
Start from `references/recipes/bespoke/E6_sneaker_bespoke.py` and change:
| Recipe constant | What it is | Sample value |
|---|---|---|
| `K, V, O, W` | lab black, instrument accent, packaging colour, white | #07080A, #D4FF1E, #FF5B14, #F2F4EE |
| `BOARDS` | the three race-timer boards (header, digits count, unit, Hebrew word) | MASS 189 g, LAYERS 04 / COMPROMISE 00, ENERGY RETURN 87 % |
| `setDig(...)` calls | which value locks on which board and when | "189" at 0.4, "04" at 2.1, "00" at 3.354, "87" at 10.25 |
| `PARTS` / `BALS` | part names, specs, side, chip position; balloon tracked anchor, park position and time | 4 parts, 4.9–8.25 s |
| the `setMatte(...)` schedule | which filter, when, masked to which tracked box | wire / heat per part |
| `FPK` | the force-plate curve (ms, newtons) | peak 2140 N at 80 ms |
| `BOX` | the packaging label: brand, model, slogan, sizes, barcode, spec lines | GUYAGA AERO-01 |
| `SPEC` | theme `he_bold`, palette, fonts (Chakra Petch), `music_vol` .6, `plate_vol` .45, `vo_name`, `html_front`, `html_behind` (the CAD viewport) | — |
Remember `html_behind`: the CAD viewport must sit BEHIND the matte and in front of the plate.
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// <filter id="fWire"> ... edge-detect (feConvolveMatrix -1..8..-1) + tiled 26px volt grid + a dilated silhouette ring ... </filter>
// <filter id="fHeat"> luminance -> feComponentTransfer(discrete) whose tables are rewritten per frame from the FEA ramp </filter>
function setMatte(mode, op, mask) {
  const m = document.getElementById("matte");
  m.style.filter = mode === "wire" ? "url(#fWire)" : mode === "heat" ? "url(#fHeat)" : "none";
  m.style.opacity = mode === "none" ? 1 : op;
  m.style.maskImage = m.style.webkitMaskImage = mode === "none" ? "none" : (mask || "none");
}
const boxMask = (b, p) => `linear-gradient(180deg, transparent ${b[1] - p}px, #000 ${b[1] + p * .2}px, #000 ${b[3] - p * .2}px, transparent ${b[3] + p}px)`;
const hsh = (n) => { const s = Math.sin(n * 12.9898 + 78.233) * 43758.5453; return s - Math.floor(s); };
function lockDigits(str, t, t0, dur, seed) {                 // flick through seeded random digits, then lock (seek-safe)
  const f = Math.floor(t * 30);
  return [...str].map((ch, k) => t < t0 ? " " : t < t0 + dur + k * .05
    ? (hsh(f * 3.1 + k * 17 + seed) < .25 ? " " : String(Math.floor(hsh(f + k * 7 + seed) * 10))) : ch).join("");
}
window.onPlace = (t) => {
  if (t > 4.88 && t < 6.06) setMatte("wire", 1, boxMask(boxAt("upper", t), 30));   // re-render only the upper
  else setMatte("none");
  render7seg("d1", lockDigits("189", t, .4, .42, 1));                                // your 7-seg SVG setter
};
```

## Adapting it to the user's project
- Content: find the product's 3–4 real test numbers (weight, layers, return, peak force, battery hours, dB) and its real parts. Every number must be true.
- Language: Hebrew words on the boards and chips; all specs stay Latin mono (like a real lab).
- Brand: the instrument accent and the packaging colour; the packaging label is the brand moment.
- Products without an explode: keep the CAD open, the boards and the force-plate style graph (swap for the product's own trace), and end on the packaging.
- Shorter clips (8–10 s): CAD open + one board + one re-render + packaging.

## Sound
- The sample uses no thump/shake hits (the lab is precise): soft_tick on each digit lock, lock_tick on each balloon, scan_beeps under the scan wipe, soft_thump on the landing peak, and the VO + music (music .6, plate .45).

## Pitfalls and QA checklist
- [ ] The matte is clean at the edges; the wireframe ring shows any matte noise as a volt halo.
- [ ] Each part mask covers only that part (check `boxMask` padding against the tracked boxes).
- [ ] 7-segment values lock on the true numbers and never on a random digit (the lock time must be before the board leaves).
- [ ] Balloons retract into their parts at the snap-back; none are left floating.
- [ ] The CAD viewport is BEHIND the product (html_behind), never covering it.
- [ ] Look at frames at 0.5, 1.3 (mid-scan), 6.5 (heat), 9.55 (snap-back), 12.8 (peak) and 14.5; qa.py until "ship".
