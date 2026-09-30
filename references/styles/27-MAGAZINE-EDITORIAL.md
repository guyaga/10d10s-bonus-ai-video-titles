# #27 MAGAZINE-EDITORIAL · The flight as a printed spread

> A drone flight through a room becomes an interior-design magazine: a masthead and folios, a circled number pinned on each piece with a leader line to its shopping credit, a price-list column on the left page counting the running total, editor's red-pencil loops and a margin note, halftone and paper grain over the photo, a page that folds open for the pull quote, and a final page that folds in with the whole room totalled.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/magazine-editorial.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E5_luma_drone_through_the_home_BESPOKE.mp4
> Runner: bespoke (`references/recipes/bespoke/E5_home_bespoke.py`, 18 s) · Example: none shipped

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: interiors and furniture brands, "shop the room", home décor, hospitality and boutique hotels, real-estate staging, fashion lookbooks shot in a space.
- Avoid when: the camera doesn't reveal pieces one by one, the room has cuts (tracking and the running total need one take), or the audience expects fast social energy.

## The design method (crafted world)
Ask: **where does this subject's world get printed?** Interiors live in magazines: a masthead, an issue line, folios, product credits keyed by numbers to a price column, a pull quote on its own page, an editor's red pencil marking what's "perfect". So:
1. **The footage is the photo on the spread.** A gutter shadow down the middle, a halftone screen and paper grain over the image, a curled page corner.
2. **Every product title is a magazine credit:** a circled number on the piece, a thin leader with a white halo to a credit strip ("01 · leather armchair · $2,050 · luma.co.il"). The same numbers key the price column.
3. **The running total is typography, not a counter badge:** a printed price-list column bleeding off the left page, rows sliding in as pieces appear, the total rolling up with an ease.
4. **The editor's hand adds life:** red-pencil loops (1.12 turns, wobbling, overshooting their start), a pencil arrow and a handwritten margin note, a torn sticky note on the quote page.
5. **Transitions are page folds** (`rotationY` ±88° with a 2200 px perspective), never wipes.

Worked example (LUMA HOME, issue 05, "the sea room"): masthead → credits 01–04 (armchair, travertine table, hand-woven rug, bouclé sofa) with the price column filling → the quote page folds open: "every piece, with its price. / no surprises. no guessing." + sticky note "perfect. straight to print! — the editor" → the drone flies out; the margin note "the drone leads the tour" with an arrow to it → credits 05–06 (brass lamp, olive tree) → the final page: "the whole room", all six rows, $9,940, "six pieces. one price.", the colophon.

It transfers to:
- **A fashion brand:** a runway or street walk as the editorial photo, credits on each garment, the price column as the "shop the look" page, and a pull quote from the designer.
- **A restaurant or chef:** the kitchen flight as a food-magazine feature: credits on each dish with its price, a menu column instead of the price list, and a critic's red-pencil notes.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#ht` | halftone screen: 1.05 px dots on a 5 px grid, multiply, 16% | over the photo |
| `#gut` | a 120 px gutter shadow at x 900 | the spread's fold |
| `#mast` | "LUMA HOME" masthead (150 px/900 + 60 px .32em), a double rule (760 px), the issue line (25 px) | top centre, lifts away at 1.55 s |
| `.fol` | page folios ("the sea room | 15"), cream chips at the bottom | |
| `#pencil` | the red-pencil loops, arrow and underline, through a graphite displacement filter (scale 3.2) | 5.5 px main stroke + a 2.5 px ghost stroke |
| `#lead` + `.mk` + `.cr` | per piece: a 38 px circled number on the piece, a 1.8 px leader with a 6 px paper halo, a credit strip (number · name 33 px · price 35 px · URL 17 px) | leaders draw from the marker, then the credit slides in |
| `#side` | the left page (500 px): kicker, "the price list" 84 px, sub, rows (circled number + name + dotted leader + price), a double rule, "the room so far" + a rolling total 76 px | clip-wipes in from the left |
| `#note` | the margin note in red pencil (112 px) + a small caps line | top-left |
| `#pg` | the quote page (720 px, right side): kicker, a 230 px quotation mark, the headline 112 px (one word in red), a rule, the deck 62 px, the byline, a folio, a spine shadow, the sticky note | folds open on its left spine |
| `#fin` | the final page (780 px, left): kicker, "the whole room" 128 px, all rows, a double rule, the total 168 px in red, the sub line, the colophon | folds in |
| `#curl`, `#grain` | a curled corner bottom-right; paper grain (multiply, 50%) over everything | |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| masthead name / rule / issue line | 0.15 / 0.35 / 0.6 | 0.8 (y −24 → 0) / 0.7 (scaleX 0 → 1) / 0.6 | power2.out / power2.inOut / power2.out | — | 0.6 (y −40) at 1.55 | power2.in |
| gutter, curl, folios | 0.2 / 0.4 / 0.4 | 0.8 / 0.6 / 0.6 | default | — | 14.3 (curl hides 6.5–11.1) | — |
| price column | 0.25 | 0.9 (clip wipe from the left) | power2.inOut | slides away x −520 at 10.75 (0.7), back at 12.55 | 0.3 at 15.0 | — |
| credit per piece | piece t (0.35, 2.05, 3.55, 5.15, 12.62, 13.25) | marker 0.35 (scale .55 → 1); leader +0.12 over 0.45; credit +0.38 over 0.35 (slides 14 px) | cubic out / smoothstep | to its end (1.85, 3.62, 5.12, 6.5, 14.35, 14.35) | 0.35 | smoothstep |
| price row per piece | piece t + 0.05 | 0.5 (x 26 → 0) | power2.out | — | — | — |
| running total | each piece adds its price over 0.8 s from t + 0.2 | cubic out | — | — | — | — |
| pencil loops | chair 0.35, table 2.05, drone 11.1, lamp 12.85 | 0.7 draw | cubic out | to their end | 0.3 | smoothstep |
| quote page | 6.55 | 0.85 (rotationY −88 → 0) | power3.out | to 10.85 | 0.6 (fold back) + 0.3 fade | power2.in |
| quote mark / words / rule / deck | 6.7 / per word / 8.7 / 9.1 & 10.14 | 0.6 / 0.45 (y 22 → 0) / 0.5 / 0.5 | power2.out | — | — | — |
| sticky note | 8.35 | 0.55 (y −26 → 0, rotation −11 → −5) | power3.out | — | with the page | — |
| margin note words | 11.1, 11.59, 12.07, 12.28 | 0.35 (x 14 → 0) | power2.out | arrow draws 11.3 (0.6), underline 12.35 (0.45) | 0.2 at 12.78 | — |
| final page | 14.3 | 0.9 (rotationY 88 → 0) | power3.out | to end | — | — |
| final title / rows / total / sub / colophon | 14.4 & 14.52 / 14.6 stagger 0.06 / 14.98 / 15.8 / 16.85 | 0.45 / 0.4 / 0.7 (y 30 → 0) / 0.6 / 0.7 | power2.out | — | — | — |
- The signature move: the credit system. One number connects three things (the piece in the photo, its credit, its row in the price column), and the total adds up as you watch.

## Typography
- Magazine serif: **Suez One** for the masthead, credit names and prices, the price column, the quote and the totals (the original used Frank Ruhl Libre 500–900; the kit remaps it).
- Captions, folios, kickers, URLs: **Secular One** (the original Heebo 300–500), small with wide tracking (17–25 px, .06–.2em).
- The editor's hand: **Karantina** 700 (the original Amatic SC; remapped), 112 px for the margin note, 38–66 px on the sticky note.
- RTL: the whole stage is `direction: rtl`; prices, numbers and URLs are `direction: ltr; unicode-bidi: isolate`. The sample priced in $; for shekels write ש״ח (the kit converts ₪).
- Max copy: credit name ≤ 16 characters; the quote 2 lines of ≤ 3 words at 112 px; the margin note ≤ 4 words.

## Colour and surface
- Paper #f5efe4 (and #ece3d3), ink #1f1a15, editor's red #ad3f26 (loops, accent words, the total), grey #6d6358.
- Surfaces are printed matter: halftone, grain, rules (double rules for totals), a spine shadow on each folding page, a curled corner.
- Brand swap: the red pencil can become the brand colour; the masthead becomes the brand's "magazine" name.

## Layout and safe zones (1920×1080 canvas)
- Left page (price column) 500 px; credits are clamped to x 540–1880 and y 40–990 so they never hit it; the quote page covers the right 720 px; the final page the left 780 px.
- The contract asks for 20% free on the left (the column).
- 9:16: the column becomes a bottom strip; credits stack above; pages fold from the bottom edge.

## What the footage must give you
- Shoot it like this: one unbroken take, 15–20 s · a wide interior, pieces readable, the camera travels through the room · 20% free on the left · smooth stabilised FPV glide, constant speed.
- Seedance lines: "FORMAT: ONE SINGLE UNBROKEN CONTINUOUS TAKE. Absolutely no cuts, no dissolves, no fades, no jump in time or position." / "CAMERA: smooth stabilised FPV drone, constant graceful speed, gentle banking. FORBIDDEN: cuts, shake, fast whips, collisions." / "POSITIVE LOCKS: one continuous camera path, the same room from start to end; no people; every furniture piece stays identical to the first frame. No text, no logos, no signage, no UI, no graphics at any time."
- Tracking (vtrack.py): one object per piece (`chair`, `table`, `rug`, `sofa`, `lamp`, `tree`); `drone` if a drone appears in frame (the sample turned that accident into the margin note). Gate: ≥70% coverage.
- Matte: not needed.

## Build it
### A. With the kit (bespoke route)
```bash
python scripts/vtrack.py clips/room.mp4 room_objects.json tracks/room_vtrack.json
python scripts/run_ad.py ROOM --spec specs/room_magazine.py --render
```
| Recipe constant | What it is | Sample value |
|---|---|---|
| `PIECES` | (number, name, price, object, marker fx, fy, credit dx, dy, in, out) | 6 pieces, total 9,940 (asserted) |
| `CIRC` (JS) | pencil loops: [object, t0, end, scale x, scale y] | 4 loops |
| the masthead / issue line / folios in `HTML` | the magazine identity | LUMA HOME · issue 05 |
| the quote page `#pg` | kicker, quote words, deck, byline, sticky note | Hebrew |
| the final page `#fin` | title, rows, total, sub, colophon | — |
| `money` | the price format | `$2,050` |
| `SPEC` | theme `he_bold`, palette, `music_vol` .55, `plate_vol` .3, `vo_name`, `assets` (fonts + the grain tile) | — |
The recipe generates the paper-grain tile once (numpy) into the tools folder; keep it or point `GRAIN` to any 512 px grain PNG.
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// a magazine credit: circled number on the tracked piece -> leader (with a paper halo) -> credit strip (seek-safe)
const $ = (id) => document.getElementById(id);
const clamp = (v, a, b) => Math.max(a, Math.min(b, v)), eo = (x) => 1 - Math.pow(1 - clamp(x, 0, 1), 3);
const sm = (x) => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
window.onPlace = (t) => {
  PIECES.forEach((P, k) => {
    const [n, name, price, obj, fx, fy, dx, dy, t0, t1] = P, b = boxAt(obj, t), fin = 1 - sm((t - t1 + .05) / .35);
    const mk = $("mk" + k), cr = $("cr" + k), ld = $("ld" + k);
    if (!b || t < t0 || fin <= 0) { mk.style.opacity = cr.style.opacity = 0; ld.setAttribute("d", ""); return; }
    const mx = clamp(b[0] + (b[2] - b[0]) * fx, 560, 1860), my = clamp(b[1] + (b[3] - b[1]) * fy, 60, 1000);
    mk.style.left = mx + "px"; mk.style.top = my + "px"; mk.style.opacity = eo((t - t0) / .35) * fin;
    const ex = mx + dx, ey = my + dy, p = eo((t - t0 - .12) / .45);          // the leader draws toward the credit
    ld.setAttribute("d", `M${mx},${my}L${mx + (ex - mx) * p},${my + (ey - my) * p}`);
    cr.style.left = ex + "px"; cr.style.top = ey + "px"; cr.style.opacity = sm((t - t0 - .38) / .35) * fin;
  });
  let v = 0; PIECES.forEach((P) => { v += P[2] * eo((t - P[8] - .2) / .8); });   // the running total
  $("tv").textContent = "$" + Math.round(v).toLocaleString("en-US");
};
tl.set("#pg", {opacity: 1, transformPerspective: 2200}, 6.55);                  // the quote page folds open on its spine
tl.fromTo("#pg", {rotationY: -88}, {rotationY: 0, duration: .85, ease: "power3.out"}, 6.55);
```

## Adapting it to the user's project
- Content: 4–6 pieces with real prices and a URL; one quote (the brand's promise) and one deck line; the editor's note on something surprising in the footage.
- Language: Hebrew magazine by default; English magazines read left-to-right: mirror the column to the right page and fold pages from the other spine.
- Brand: the masthead is the brand as a publication; the colophon is the CTA ("buy the whole room").
- Without the quote page (shorter clips): masthead → credits with the column → final page.

## Sound
- Printed matter is quiet: soft_tick per credit, a paper page-turn (ui_whoosh at vol .3) on each fold, a soft chime on the total; music .55, plate .3.

## Pitfalls and QA checklist
- [ ] Credits never overlap the price column or each other (the clamp keeps x ≥ 540; check `dx/dy` per piece).
- [ ] The numbers match: marker 03 ↔ credit 03 ↔ row 03, and the rows add up to the printed total.
- [ ] Pencil loops circle the piece, not empty floor (tune the loop scale per piece).
- [ ] Page folds hinge on the spine (transform-origin 0 50%) and the photo stays visible around them.
- [ ] Look at frames at each credit, the quote page, the margin note and the final page; qa.py until "ship".
