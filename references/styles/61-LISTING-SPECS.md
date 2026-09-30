# #61 LISTING-SPECS · Real-estate listing package

> A listing title block (status pill, property title rising out of a mask, address with a drawn rule) sits in the sky, tracked pins with leader labels land on the house and its features, a glass spec bar staggers in with line icons and counting numbers (rooms, baths, built m², plot m²), and the asking price counts up to its figure.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/listing-specs.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_LISTING-SPECS.mp4
> Runner: run_style LISTING-SPECS · Example: examples/listing-specs/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: property listings (villas, apartments, penthouses), Airbnb/holiday rentals, real-estate agency social posts, new-development promos, commercial spaces.
- Avoid when: the footage is an interior walkthrough with no sky or calm area for the title (use MAGAZINE-EDITORIAL or ARCH-DRAWING), or there are more than 5 specs.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#tscrim` | 1000×440 px corner shadow (rgba(10,8,6,.66) → transparent) behind the title block | the title's side |
| `#head` | status pill (accent, dark text, 26 px), title (104 px display, in a mask), address (32 px) with a 90 px accent rule | 110 px from the side, top 80 |
| `.pin` | tracked pin: 22 px white dot with a halo, 110 px leader, dark-glass label (28 px) | rides a tracked object |
| `#bar` | glass spec bar: full width minus 110 px margins, bottom 70, radius 22, blur 14 | up to 5 cells |
| `.cell` | 52 px line icon (accent stroke), counting number (54 px display, tabular, LTR), unit (26 px) | icons: bed, bath, area, plot, pool, car, floors, view |
| `#price` | label (28 px) + price (84 px accent display, counting) + unit (half size) | opposite side to the title, bottom 230 |
| `#agent` | agency name, 34 px display, 90% | opposite top corner |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| title scrim (fade) | .1 | .80 | — | whole clip | — | — |
| status pill (fade, y −12→0, scale .9→1) | .4 | .50 | back.out(2) | — | — | — |
| title (yPercent 105→0) | .6 | .90 | expo.out | — | — | — |
| address rule (scaleX 0→1) | 1.0 | .70 | expo.out | — | — | — |
| address text (fade, x ∓20→0) | 1.1 | .60 | power3.out | — | — | — |
| agent (fade to .9) | 1.2 | .80 | — | — | — | — |
| spec bar (y 60→0, fade) | t_specs−.3 | .70 | power3.out | — | — | — |
| cell i (fade, y 18→0) | t_specs + i×.22 | .50 | power3.out | — | — | — |
| cell number count | t_specs + i×.22 + .1 | .90 | easeOut cubic | — | — | — |
| pin dot (scale 0→1) / leader (scaleX) / label (fade, x ∓16) | pin.t / +.2 / +.45 | .45 each | back.out(3) / power3.out / power3.out | — | — | — |
| price block (fade, y 20→0) | price.t | .70 | power3.out | — | — | — |
| price count | price.t+.1 | 1.30 | easeOut quartic | — | — | — |
- Sample order: title 0.4–1.7 s, specs 2.4 s, pins 3.6 / 4.4 s, price 5.6 s: facts first, the price last.
- The signature move: the spec bar counting up cell by cell and the price rolling to its figure, while pins ride the property.

## Typography
- Latin: DM Serif Display 400 title, numbers and price; Manrope 500 pill, address, units, labels.
- Hebrew: `pair: "suez"` (default) = Suez One title/numbers/price, Secular One text. RTL: the title block defaults to the right corner, cells read right-to-left, numbers stay LTR (`unicode-bidi: isolate`).
- Currency: write the unit in words: "ש״ח" (Suez One / Secular One draw ₪ as a stylised "שח"). Numbers get en-US thousands separators (12,900,000).
- Suez One digits are old-style (low): fine for prices; if you want full-height figures, set a Latin display for numbers.
- Maximum copy: title ≈ 16 characters (104 px), address ≈ 34, unit ≈ 10, pin label ≈ 26.

## Colour and surface
- `colors.accent` #e3b35d (warm gold: pill, rule, icons, price). Dark glass for the bar and labels; white text.
- Brand swap: accent = the agency colour (warm golds and deep greens suit property; avoid neon).

## Layout and safe zones (1920×1080 canvas)
- Title block in the `head_side` corner (default the reading start: right in Hebrew, left in English): keep it in the sky, off the building. Price on the other side, bottom 230; agent in the other top corner; spec bar across the bottom.
- Pins: `anchor` + `dx`/`dy` on the tracked box, leader to the `side` (L/R).
- Industry convention: price last; specs in the order buyers scan them (rooms, baths, built area, plot, extras); the address or area is always on screen with the title.
- 9:16: title top, spec bar as a 2×2 grid (edit CSS) above the platform UI, price under the title.

## What the footage must give you
- Shoot it like this: one take, 8–20 s, a slow dolly/drone move toward or along the property at golden hour, sky in the upper corners, a calm bottom strip for the bar.
- Tracking: for pins, vtrack.py on the house and features: `{"name": "villa", "desc": "the villa building"}`, `{"name": "pool", "desc": "the swimming pool"}`.
- Matte: not needed.
- Good footage: exterior hero shots, drone orbits, twilight shots. Bad: interiors with no calm area, fast drone moves (pins swing).

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/villa.mp4 objects.json tracks/villa.json      # only if you use pins
python scripts/run_style.py LISTING-SPECS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| title | property title | required |
| status / address / agent | pill / address line / agency bug | "" / "" / none |
| specs[] | {icon, n, unit} up to 5 | [] |
| t_specs | spec bar start | 2.4 |
| price | {n, unit, label, t} | none |
| pins[] | {obj, anchor, dx, dy, label, t, side} | []; anchor "c", side "R" |
| track | needed for pins | — |
| head_side | "right" / "left" | reading start |
| language / pair | he/en; Hebrew pair | en / "suez" |
| fonts | override | DM Serif Display 400 / Manrope 500 |
| colors | {accent} | #e3b35d |
| sfx | whoosh, tick per cell, pop per pin, chime after the price | true |
| plate_vol, music, music_vol, name | — | .7, none, .5 |
```json
{
 "clip": "clips/house.mp4", "track": "tracks/house.json",
 "status": "FOR SALE · EXCLUSIVE", "title": "Villa Serena", "address": "12 Palm Rd · Malibu",
 "specs": [{"icon": "bed", "n": 5, "unit": "beds"}, {"icon": "bath", "n": 4, "unit": "baths"}, {"icon": "area", "n": 4200, "unit": "sq ft"}, {"icon": "pool", "n": 1, "unit": "pool"}],
 "price": {"n": 8950000, "unit": "USD", "label": "Asking price", "t": 5.6},
 "pins": [{"obj": "house", "anchor": "t", "dx": 160, "dy": 100, "label": "South façade · glass walls", "t": 3.6}],
 "agent": "Coastline Realty"
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const S = [{n: 6, t: 2.4}, {n: 4, t: 2.62}, {n: 480, t: 2.84}], P = {n: 12900000, t: 5.6};
tl.fromTo("#tt span", {yPercent: 105}, {yPercent: 0, duration: .9, ease: "expo.out"}, .6);
tl.fromTo("#ad i", {scaleX: 0}, {scaleX: 1, duration: .7, ease: "expo.out"}, 1.0);
tl.fromTo("#bar", {y: 60, opacity: 0}, {y: 0, opacity: 1, duration: .7, ease: "power3.out"}, S[0].t - .3);
S.forEach((s, i) => tl.fromTo("#c" + i, {opacity: 0, y: 18}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, s.t));
tl.fromTo("#price", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .7, ease: "power3.out"}, P.t);
const fmt = (v) => Math.round(v).toLocaleString("en-US");
window.onPlace = (t) => {                            // counts from time: seek-safe
  S.forEach((s, i) => { const u = Math.max(0, Math.min(1, (t - s.t - .1) / .9)); document.getElementById("cn" + i).textContent = fmt(s.n * (1 - Math.pow(1 - u, 3))); });
  const u = Math.max(0, Math.min(1, (t - P.t - .1) / 1.3)); document.getElementById("pn").textContent = fmt(P.n * (1 - Math.pow(1 - u, 4)));
};
```

## Adapting it to the user's project
- Content: the listing's real data; icons matched to each spec; pins only on features you can see.
- Language: Hebrew → `"language": "he"`; units in Hebrew (חדרים, מ״ר), price unit ש״ח.
- Brand: agency name as `agent`; accent = agency colour.
- Vertical 9:16: see layout.
- Longer clips: add more pins along the move; keep the price for the end.

## Sound
- `ui_whoosh` (.25) at .5, `soft_tick` (.3) per spec cell, `ui_pop` (.25) per pin, `chime` (.25) as the price settles (price.t+1.3).

## Pitfalls and QA checklist
- [ ] The title block sits in the sky, not on the building (set `head_side`).
- [ ] No ₪ in Hebrew (ש״ח); numbers LTR and isolated.
- [ ] Pins sit on the right features in the tracking preview.
- [ ] Spec bar clears the bottom 5% and the price doesn't overlap the pool/house focal point.
- [ ] Numbers are real listing data.
