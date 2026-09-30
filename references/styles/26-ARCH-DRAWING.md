# #26 ARCH-DRAWING · Architecture on paper

> The drone footage is drawn on: a translucent vellum sheet slides over the shot with the facade inked on it in graphite and a hand-lettered headline; then a sepia elevation sheet slides in where floors fill with watercolour wash as the drone climbs and the sight line to the sea clears; floor numbers ride the real slabs like painted signage; the sky gets a hand-lettered line; it ends on an estate-agent floor plan and a brass building plaque.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/arch-drawing.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E8_seaview24_tower_arrival_BESPOKE.mp4
> Runner: bespoke (`references/recipes/bespoke/E8_tower_bespoke.py`, 18 s) · Example: examples/E8_tower_bespoke.py (+ E8_tower_bespoke_data.json, E8_tower_climb.json: runs standalone)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: real-estate developments and towers, architecture studios, hotels and resorts, urban renewal, anything sold "from the plan".
- Avoid when: there's no building to trace (lines need real edges), the camera orbits wildly, or the brand is tech/fast (this world is slow, hand-made paper).

## The design method (crafted world)
Ask: **what does this subject's world draw, print or stamp before it exists?** A building is born on an architect's table: tracing paper over a site photo, elevations in sepia, floor plans with poché walls, dimension lines, level markers, and finally a brass plaque on the finished lobby. So:
1. **Every title is a drawing artefact:** a headline hand-lettered between ruled pencil guidelines, floor numbers as painted signage, heights as level markers ("+72.00"), the price as an annotation on the elevation.
2. **Tie the drawing to the footage:** the facade lines are extracted from the first frames and carried by a per-frame homography (the drawing sits ON the building); the floor signage rides tracked slab points; the elevation's current floor is driven by the drone's climb (measured from the footage), so the wash rises with the real camera.
3. **The hero is a diagram, not a word:** the sight line from the current floor to the sea: blocked (terracotta, dashed, ×) by the neighbouring buildings until you rise, then it clears and a blue view-cone wash opens to the sea. The selling point, "the higher you are, the more sea you see", is shown, not written.
4. **Materials, not panels:** vellum (60% translucent cream with paper grain), sepia paper, watercolour wash with a turbulence edge, graphite with a pen-wobble displacement, brass.

Worked example (SEAVIEW 24): vellum over the facade "every floor, and its price." → the sepia west elevation with floors 1 → 24 filling, "from 2.1 → 4.8 million", the sight line clearing → trace strip "and as you rise, the sea opens." → "then, the view." lettered on the sky, gold hairlines on the penthouse, a sea-level datum → the penthouse plan with the sea wall in gold and the SEAVIEW 24 brass plaque.

It transfers to:
- **A hotel or resort:** the vellum traces the hotel from the drone; the elevation shows which floors face the sea and the room price per floor; the end is a room plan with the balcony in gold and a key-card instead of a plaque.
- **A product designed by industrial designers (a chair, a car):** a vellum sketch over the product shot, a sepia orthographic sheet with dimensions that fill as the camera orbits, and a patent-style drawing as the end card.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#dw` signage SVG | per tracked floor slab: a level triangle + a long datum line + the floor number (92 px) and "קומה" (44 px) painted with a dark stroke | shown only when the slab is tracked and not under a sheet; one per 110 px vertically |
| `#pt` gold linework | penthouse lines (from the footage, carried by a homography) + a horizon datum + a roof level marker | gold #d9ab5c with a soft glow |
| `#vel` vellum | 1790 × 1120 cream sheet at 60% with paper grain, sliding over the shot | the facade in graphite (`.fl` lines, `.fo` construction overshoots, `.fhat` hatched slab bands) with a pen-wobble filter |
| `#h1` lettering | 196 px Karantina hand lettering between four ruled pencil guidelines, one word terracotta | words clip in from the right (RTL) |
| `#el` elevation | a 640 px sepia sheet (left third): margin line, ground + earth hatch, the sea with waves and a sun, 3 neighbour blocks, the tower's 24 floors, floor numbers, a 72.00 m dimension, the watercolour floor wash, the current-floor band, a level marker, the sight line (blocked / rest / clear), the view cone, an eye | header "west elevation · SEAVIEW 24 · 1:500"; footer: floor number 134 px + price |
| `#n2` trace strip | an 820 × 330 vellum strip with its own guidelines, dropped top-right | second line, 150 px lettering |
| `#tt` sky title | ruled guidelines + "ואז" 180 px + "הנוף." 280 px lettered on the sky | |
| `#sale` sales sheet | a 660 × 880 paper sheet: brass plaque (SEAVIEW 24, 84 px), "penthouse · floor 24", the floor plan (poché walls, doors, room names, the sea wall in gold, sea waves, a north arrow), a facts line | slides in from the right |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| vellum sheet | 0 | 1.0 (x 1800 → 0) | power2.out | to 3.05 | 0.95 (x → 1900) | power2.in |
| construction overshoots / facade lines | 0.45 / 0.7 | 0.9 / 1.0 draw (dash offset), stagger 0.05 / 0.06 | power1.inOut / power2.inOut | — | with the sheet | — |
| hatched slab bands | 1.7, stagger 0.08 | 0.8 (to .95) | default | — | — | — |
| pencil guidelines | 0.7, stagger 0.08 | 0.7 (x2 760 → 0) | power1.inOut | — | — | — |
| headline words | 1.0, 1.209, 1.69, 2.416 (on the VO) | 0.42 each (clip `inset(-20% 0 -30% 100%)` → 0%) | power1.out | — | — | — |
| elevation sheet | 3.25 | 1.0 (x −700 → 0) | power2.out | to 12.6 | 0.9 (x → −700) | power2.in |
| elevation linework | 3.7, stagger 0.015 | 1.5 draw | power1.inOut | — | — | — |
| neighbours | 4.0, stagger 0.15 | 1.0 draw | power1.inOut | — | — | — |
| header / footer | 3.9, stagger 0.2 | 0.6 | default | — | — | — |
| floor wash | per frame: floors 1 → 12 over 3.2–5.95 s, 12 → 24 over 6.8–11.0 s (half time, half the drone's measured climb) | — | — | — | — | — |
| trace strip | 5.75 | 0.8 (y −360 → 0) | power2.out | lines at 6.15 (0.8) and 7.8 (0.7) | 0.8 (y → −380) at 9.2 | power2.in |
| sky title | 13.1 (guides) / 13.25 / 13.95 | 0.7 / 0.5 / 0.8 | power1.inOut / power1.out | — | — | — |
| penthouse gold lines | 14.5, stagger 0.06 | 1.0 draw | power2.inOut | — | — | — |
| horizon datum | 14.4 | 1.4 | power2.inOut | — | — | — |
| sales sheet | 15.3 | 0.9 (x 760 → 0) | power2.out | to end | — | — |
| plaque / heading / plan walls | 15.65 / 16.0 / 15.9 | 0.6 (scale .96 → 1) / 0.5 / 1.3 draw, stagger 0.1 | power1.out / default / power1.inOut | — | — | — |
| sea wall (gold) / labels | 17.0 / 17.3 | 0.7 draw / 0.5, stagger 0.08 | power2.out | — | — | — |
- The signature move: the sight-line diagram on the elevation, recomputed every frame from the current floor: blocked by a neighbour (terracotta dashed + ×) until the line clears the rooftops, then it turns sea-blue and the view cone opens.

## Typography
- Hand lettering and big labels: **Karantina** 700 (headline 196 px, trace strip 150 px, sky 180/280 px, floor signage 92 px, floor number 134 px, price 54–66 px).
- Small drawing text (dimension numbers, level values, floor ticks): **Secular One** (the original used Heebo 300–600; the kit remaps it).
- The brass plaque: **Suez One** (the original Bellefair; remapped).
- RTL: every lettering line clips in from the right; numbers like "+72.00", "1:500" and prices are LTR spans. Prices: write "מיליון ש״ח" (the kit converts ₪).
- Max copy: headline 2 lines of ≤ 2 words at 196 px; the sky title 2 words.

## Colour and surface
- Graphite ink #231c18, vellum rgb(244,237,222) at 60%, sepia #5a3b27 (sheet gradient #6a4630 → #5a3b27 → #4b2f1f), cream line #f4e6c8, terracotta #c4623a (blocked sight line, accent word), sand #e5c79a, sea blue #4f93b5, brass/gold #d9ab5c.
- Surfaces: paper grain (feTurbulence at baseFrequency .75–.9), watercolour wash with a displacement edge (scale 7), pen wobble (scale 3.2).
- Brand swap: the terracotta and sea-blue are the story colours; change the brass plaque's name and the sheet's title block, not the palette.

## Layout and safe zones (1920×1080 canvas)
- The elevation sheet owns the left third (640 px); the building must be in the right half of the frame (the contract asks for 30% free on the left). The trace strip sits top-right, the sales sheet on the right (660 px).
- 9:16: the elevation becomes a bottom band; the lettering goes to the sky above the tower.

## What the footage must give you
- Shoot it like this: one take, no cuts, 12–20 s · the building on the right half, sky and neighbourhood on the left · 30% free on the left · smooth vertical drone rise, constant speed.
- Seedance lines: "FORMAT: One continuous shot, no cuts." / "CAMERA: smooth vertical drone rise, constant speed. FORBIDDEN: cuts, shake, spins." / "COMPOSITION: The tower stays in the right half of the frame; the left third is sky and low surroundings." / "POSITIVE LOCKS: one tower, the same architecture throughout. No text, no logos, no signage, no UI, no graphics at any time."
- Data precomputed from the footage (the recipe reads it from `E8_tower_bespoke_data.json` and `E8_tower_climb.json`):
  - `lines0`: facade line segments on the first frame (e.g. OpenCV Canny + HoughLinesP on frame 0, kept to the building);
  - `start` / `top`: per-frame homographies (frame index → 3×3 matrix, row-major, first 6 used) carrying those lines, from `scripts/track.py`-style feature tracking on the facade;
  - `linesT` + `top`: the penthouse lines on a late frame and their homographies;
  - `tracks`: per floor slab {n (floor number), f0 (first frame), p [[x,y] per frame]} (vtrack or track.py points on each slab edge);
  - `E8_tower_climb.json`: the drone's vertical progress per frame (0 → 1), used to pace the floor wash.
  There's no generator script in the kit for these; build them once per building with track.py/vtrack.py and a few lines of OpenCV.
- Matte: not needed.

## Build it
### A. With the kit (bespoke route)
```bash
python scripts/run_ad.py TOWER --spec examples/E8_tower_bespoke.py --render    # the shipped example, as-is
python scripts/run_ad.py MYTOWER --spec specs/mytower_arch.py --render          # your adapted copy
```
| Recipe constant | What it is | Sample value |
|---|---|---|
| `DATA`, `W` | the precomputed facade lines, homographies, slab tracks and climb curve | the two JSON files |
| `GY, FH, TX0, TX1` | the elevation's ground line, floor height, tower x-range | 790, 25.5, 400, 540 |
| `NB` | neighbour blocks on the elevation: (x0, x1, height) | 3 blocks |
| `LEGS` (JS) | which floors the wash climbs through, when | [3.2, 5.95, 1→12], [6.8, 11.0, 12→24] |
| price formula (JS) | `2.1 + (floor − 1) × 2.7 / 23` million | per project |
| `VEL_HTML`, `N2_HTML`, `TT_HTML` | the three hand-lettered lines | Hebrew |
| `rooms`, `wall` | the floor plan and room names | penthouse |
| `SALE_HTML` | plaque name + subtitle, plan heading, facts line | SEAVIEW 24 |
| `SPEC` | theme, palette, fonts, `music_vol`, `plate_vol`, `vo_name`, `html_front`, `css`, `js` | — |
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// the sight line from the current floor to the sea, recomputed every frame; blocked by neighbours until it clears
const $ = (id) => document.getElementById(id);
const line = (id, a, b, c, d) => { const e = $(id); e.setAttribute("x1", a); e.setAttribute("y1", b); e.setAttribute("x2", c); e.setAttribute("y2", d); };
window.onPlace = (t) => {
  const F = floorAt(t), yF = GY - FH * (F - .5);                 // current floor from the drone climb
  const ex = TX0 - 3, ey = yF, yAt = (x) => ey + (SEA_Y - ey) * (ex - x) / (ex - SEA_X);
  let margin = 1e9, hit = null;
  for (let k = NB.length - 1; k >= 0; k--) {                       // nearest neighbour first
    const [a, b, h] = NB[k], m = (GY - h) - yAt(a); margin = Math.min(margin, m);
    if (m < 0 && !hit) hit = yAt(b) > GY - h ? [b, yAt(b)] : [ex - (GY - h - ey) * (ex - SEA_X) / (SEA_Y - ey), GY - h];
  }
  const clear = Math.max(0, Math.min(1, margin / 22));             // 0 = blocked, 1 = open view
  line("eSb", ex, ey, ...(hit || [ex, ey]));  $("eSb").style.opacity = hit ? 1 : 0;   // terracotta dashed
  $("eCone").style.fillOpacity = (.5 * clear).toFixed(3);          // the blue view cone opens
  $("eWash").setAttribute("y", GY - FH * F); $("eWash").setAttribute("height", FH * F);
};
// hand lettering: each word revealed from its reading edge between the ruled guidelines
[["#hw1", 1.0], ["#hw2", 1.209], ["#hw3", 1.69], ["#hw4", 2.416]].forEach(([s, t]) =>
  tl.fromTo(s, {opacity: 0, clipPath: "inset(-20% 0 -30% 100%)"}, {opacity: 1, clipPath: "inset(-20% 0 -30% 0%)", duration: .42, ease: "power1.out"}, t - .06));
tl.fromTo("#vel", {x: 1800}, {x: 0, duration: 1.0, ease: "power2.out"}, 0);
```

## Adapting it to the user's project
- Content: the three lettered lines carry the pitch (what, how it grows, the payoff); the elevation carries the facts (floors, heights, price per floor); the plan carries the product (the unit being sold).
- Language: Hebrew lettering in Karantina reads as hand-drawn; English works too (letter left → right).
- Brand: the plaque and the sheet title block; the palette is the paper world, keep it.
- Without the precomputed facade lines: drop the vellum ink and keep the lettering on a plain vellum sheet; keep the elevation (it's pure drawing, driven only by the climb).
- Low-rise buildings: fewer floors in the elevation (set `FH` larger), the sight line to a park or skyline instead of the sea.

## Sound
- Paper and pencil: soft_tick for each word, a paper slide (ui_whoosh at vol .3) for each sheet, chime when the sight line clears; music .5–.55, plate .3.

## Pitfalls and QA checklist
- [ ] The inked facade stays on the building for the whole vellum part (check the homographies at 0.5, 1.5 and 3.0 s).
- [ ] Floor signage never appears under a sheet or stacked closer than 110 px (the recipe hides both cases).
- [ ] The wash reaches the top floor when the drone reaches the top (tune `LEGS` to the climb).
- [ ] The sight line visibly flips from blocked to clear during the climb (that's the story).
- [ ] Prices and heights are real.
- [ ] Look at frames at 1.5, 5.0, 9.0, 13.8 and 17.5; qa.py until "ship".
