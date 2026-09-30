# #28 KITCHEN-TICKET · A restaurant kitchen at night

> The order comes in as a thermal kitchen ticket printing line by line under a steel rail; the voice-over words condense out of smoke and drift away as steam; the sear temperature fills a flame-shaped gauge to 260°; the chef's notes appear in grease pencil on the dark and on the porcelain; and the kitchen owns the ending: the pass printer prints the booking line, the ticket is torn off, carried along the rail, spiked, and stamped "done ✓".
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/kitchen-ticket.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E10_ember_chefs_pass_BESPOKE.mp4
> Runner: bespoke (`references/recipes/bespoke/E10_chef_bespoke.py`, 15 s, 5 shots) · Example: none shipped

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: restaurants and chefs, food delivery, bakeries and bars, cooking classes, food products (sauce, spices, meat).
- Avoid when: the footage is bright and white everywhere (smoke words need dark areas), the piece is a menu with many prices (use MAGAZINE-EDITORIAL #27), or the brand is fast-food loud (use STOMP-SX #12).

## The design method (crafted world)
Ask: **what does this subject's world print, measure and stamp?** A professional kitchen runs on paper and heat: thermal order tickets on a steel rail, a station label on masking tape, a grill thermometer, the chef's grease-pencil notes, the pass printer, a spike for finished tickets, a "done" stamp. So:
1. **The order IS the opening title.** A thermal ticket prints line by line (each line revealed in 7 steps, like a thermal head), with the restaurant name, table, covers and the dishes. It's big (a third of the frame) and in focus: it's the signature.
2. **The voice is made of the kitchen's air:** each VO word condenses out of smoke (per-word SVG turbulence + blur resolving to sharp, rising 26 px) and later leaves as steam (the reverse, drifting 34 px up).
3. **Measure with the world's instruments:** the sear temperature fills a flame-shaped gauge from the root to 260°, with a slight flicker; ember sparks rise behind the words.
4. **Notes by hand:** grease pencil, chalk-textured on the dark shots, wax on the porcelain, with drawn arrows and a circle around "6".
5. **The ending is a kitchen action,** not a logo card: print the CTA line on the pass printer, tear, carry along the rail, spike, stamp.

Worked example (EMBER, Tel Aviv): the ticket "table 7 · 21:40 · 1 × entrecôte 350 g, dry-aged 28 days, medium-rare · red-wine jus · sea-salt flakes · *** fire! ***" + "everything starts in fire." → the flame gauge 0 → 260° "outside", "pink inside" → "jus" on the porcelain with the note "reducing · 6 hours" → "salt. to the last grain." → the pass printer: "tonight · 20:30 · table for 2 · book a table · EMBER · Tel Aviv" → tear, spike, stamp "בוצע ✓".

It transfers to:
- **A bakery:** the ticket becomes the morning bake list, the flame gauge becomes the oven's proof/temperature dial, notes in flour-dusted chalk, the ending: a paper bag label stamped "fresh".
- **A cocktail bar:** the ticket is the bar tab, the gauge a jigger filling, notes on a napkin, the ending: the tab spiked and stamped "cheers".

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `.scr` scrims | per-shot dark gradients (bottom-left, top-right, top) under the words | only where words sit |
| `#sparks` | 46 ember sparks (4 × 9 px), rising and flickering | computed per frame from t (seeded) |
| `#rail` | a 1040 × 30 px steel rail (metal gradient) with a clip, top-right | shot A |
| `#tstrip` + `.tape` | a scrolling ticket-rail time strip (21:36…21:43) + a masking-tape station label "גריל · 2" | |
| `#tk` ticket | a 620 px thermal slip with a torn zig-zag bottom (CSS mask), lines 39 px (sm 31 px), dashed separators, the logo 54 px, "*** fire! ***" inverted | its height grows as each line prints |
| `.blk` words | VO words, right-aligned blocks: row1 92–250 px, row2 96–250 px | cream on dark, ink on porcelain; "באש" ember-lit |
| `#gauge` | a 170 × 255 flame outline with a gradient fill rising from the root, tick marks, "260°" 180 px | |
| `.note` | grease-pencil notes (stroked text) with drawn arrows and a circle | chalk texture filter on dark shots |
| hero: `#hrail`, `#spike`, `#prn`, `#tk2`, `#stamp` | a second rail, a steel spike, the pass printer with a green LED, the CTA ticket (the CTA line inverted), the red rubber stamp | ending |

## Timing and motion
Shots: flame 0–1.75 | slicing 1.75–4.5 | jus 4.5–6.83 | salt 6.83–10.42 | hero 10.42–15.07.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| rail / scrim A | 0 | 0.3 / 0.4 | sine.out | shot A | 0.2 at 1.55 | sine.in |
| ticket lines | 0.10 → 1.28 (13 lines, about 0.1 apart) | 0.14 per line, `steps(7)` clip from the right; the slip grows 0.1 s before each line | steps / power1.out | sways to −1.2° over 1.4 s | steam-out 0.3 at 1.5 | sine.in |
| VO words | on the VO (0.02, 0.72, 1.22 …) | smoke-in 0.36–0.9 (turbulence scale 130 → 0 over 1.15 × dur, blur ≤16 → 0, y 26 → 0) | sine.out | to the shot end | steam-out 0.2–0.6 (scale 0 → 140, blur 0 → 14, y −34) | sine.in |
| flame gauge | 2.0 (smoke-in 0.5) | the number counts 0 → 260 over 2.12–3.1 (cubic out); the level rises with it | — | flickers ±1.8% | 0.2 at 4.3 | — |
| chef's notes | 2.15 / 5.5 / 8.1 | smoke-in 0.6; arrows draw 0.55–0.6 (dash offset) | sine.inOut | — | with the shot | — |
| the circle around "6" | 6.3 | 0.35 draw | sine.inOut | — | — | — |
| hero rail + spike / printer | 10.45 | 0.3 / 0.35 (y −60 → 0) | power2.out | — | — | — |
| CTA ticket lines | 10.98 → 12.62 | 0.14 steps(7); the CTA line 0.26 steps(12) | steps | — | — | — |
| tear | 13.3 | 0.1 (y 16, rotation 2.4°) | power4.out | — | — | — |
| carry along the rail | 13.42 | 0.42 (x −590, rotation −1.6°) | power3.inOut | — | — | — |
| spike | 13.84 / 13.96 | 0.12 down (y 20) / 0.12 settle (y 17) | power2.in / sine.out | — | — | — |
| stamp | 14.05 | 0.13 (scale 2.3 → 1, rotation −4 → −11°, opacity .92) | power4.in | the ticket jolts y 22 → 17 (0.05 + 0.18) | — | — |
- The signature move: the thermal ticket. It prints like real hardware (stepped reveals, the paper growing, a torn edge), and at the end it's physically handled: torn, carried, spiked, stamped.

## Typography
- VO words: **Suez One** (the original Frank Ruhl Libre 300–900; remapped), very large (row1 up to 250 px, 900 weight originally → Suez One's single weight; use size for hierarchy).
- Ticket: **Secular One** for Hebrew receipt lines (the original Miriam Libre; remapped) + **Space Mono** 700 for times and numbers.
- Grease pencil and the station tape: **Karantina** 700 (the original Amatic SC / Rubik Dirt; remapped), stroked 1.6 px so it looks drawn.
- The stamp: Karantina 700, 70 px, red, in a 6 px rounded border.
- RTL: word blocks are right-aligned RTL; ticket rows use `justify-content: space-between` with Latin times on the left. Prices (if any) as ש״ח.
- Max copy: 1–3 words per VO block; ticket lines ≤ 24 characters (620 px slip at 39 px).

## Colour and surface
- Cream #f6e9d2 (words), ink #24130c (words on porcelain), ember #ff8a3d, thermal paper #fbf8f1 → #f1ece0 with ink #26221e, steel gradients (#e9edf0 → #9aa3a9 → #5b6368 → #c5ccd1), stamp red #c9231a, printer LED #3dff7a.
- Surfaces are real materials: thermal paper with a zig-zag torn edge (CSS mask), brushed steel, masking tape, chalk (an SVG noise mask), porcelain.
- Brand swap: the restaurant name on the ticket and the stamp word; keep the kitchen materials.

## Layout and safe zones (1920×1080 canvas)
- The ticket and rail live top-right (rail x 880–1920, ticket x 1270, 620 wide); words sit bottom-left or top-left over scrims; the gauge bottom-left (78/772). In the hero, the printer is top-right and the spike at x 754.
- The contract keeps the right third of each shot dark and plain (the ticket sits there).
- 9:16: the rail across the top, the ticket hanging down the right half, words in the bottom half.

## What the footage must give you
- Shoot it like this: planned cut list (max 5), 12–18 s · macro, subject centre-left · 30% free on the right · energy from cuts and speed ramps.
- Seedance lines: "FORMAT: Timestamped cut-blocks. HARD CUTS exactly at the listed timecodes and nowhere else." / "COMPOSITION: Keep the right third of each shot dark and plain (the order ticket sits there)." / "CAMERA: energy from cuts and speed ramps. FORBIDDEN: whip-pans, shake. POSITIVE LOCKS: one dish, one plate. No text, no logos, no signage, no UI, no graphics at any time."
- Tracking (vtrack.py): the dish or ingredient per shot if a note must point at it (the sample places notes by hand per shot). Gate: ≥60% coverage.
- VO: word timings (scripts/word_times.py) so each word condenses exactly when it's spoken.
- Matte: not needed.

## Build it
### A. With the kit (bespoke route)
```bash
python scripts/word_times.py CHEF specs/chef_lines.json he        # word-level timings for the smoke-in
python scripts/run_ad.py CHEF --spec specs/chef_ticket.py --render
```
| Recipe constant | What it is | Sample value |
|---|---|---|
| `TK` | the order ticket: (html, class, height, print time) per line | 13 lines, 0.10 → 1.28 |
| `TK2` | the CTA ticket printed at the pass | 7 lines, 10.98 → 12.62 |
| the word blocks in `HTML` (`words([...])`) | each VO word with an id, grouped in blocks per shot | hA … hD2 |
| `smokeIn(sel, at, dur, rise, amt)` / `smokeOut(...)` calls | when each word appears and leaves | on the VO timings |
| the gauge formula (JS) | 0 → 260 over 2.12 → 3.1 s | sear temperature |
| the notes `#nB`, `#nC`, `#nD` | chef's grease-pencil notes + arrows | Hebrew |
| the tear/carry/spike/stamp tweens | the ending choreography | 13.3 → 14.23 |
| `SPEC` | theme `he_bold`, palette, `music_vol` .5, `plate_vol` .45, `vo_name`, `assets` (fonts) | — |
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// 1) a thermal ticket line prints: stepped reveal from the right edge, the paper grows just before it
function printLine(sel, at, paperHeight) {
  tl.to("#tkP", {height: paperHeight, duration: .1, ease: "power1.out"}, at - .04);
  tl.fromTo(sel, {clipPath: "inset(0 0 0 100%)"}, {clipPath: "inset(0 0 0 0%)", duration: .14, ease: "steps(7)"}, at);
}
// 2) a word condenses out of smoke: its own SVG filter (turbulence displacement + blur), both driven by the timeline
function smokeIn(el, at, dur = .85, rise = 26, amt = 130) {
  const f = document.createElementNS("http://www.w3.org/2000/svg", "filter"), id = "sm" + el.id;
  f.id = id; f.innerHTML = '<feTurbulence type="fractalNoise" baseFrequency="0.009 0.028" numOctaves="2" seed="7" result="n"/>' +
    '<feDisplacementMap in="SourceGraphic" in2="n" scale="0"/><feGaussianBlur stdDeviation="0"/>';
  document.querySelector("#fxdefs defs").appendChild(f); el.style.filter = `url(#${id})`;
  tl.fromTo(el, {opacity: 0, y: rise}, {opacity: 1, y: 0, duration: dur, ease: "sine.out", immediateRender: false}, at);
  tl.fromTo(f.querySelector("feDisplacementMap"), {attr: {scale: amt}}, {attr: {scale: 0}, duration: dur * 1.15, ease: "sine.out", immediateRender: false}, at);
  tl.fromTo(f.querySelector("feGaussianBlur"), {attr: {stdDeviation: Math.min(16, amt / 6)}}, {attr: {stdDeviation: 0}, duration: dur, ease: "sine.out", immediateRender: false}, at);
}
// 3) the ending: tear, carry, spike, stamp
tl.to("#tk2", {y: 16, rotation: 2.4, duration: .1, ease: "power4.out"}, 13.3);
tl.to("#tk2", {x: -590, y: 2, rotation: -1.6, duration: .42, ease: "power3.inOut"}, 13.42);
tl.to("#tk2", {y: 20, rotation: -2.2, duration: .12, ease: "power2.in"}, 13.84);
tl.fromTo("#stamp", {opacity: 0, scale: 2.3, rotation: -4}, {opacity: .92, scale: 1, rotation: -11, duration: .13, ease: "power4.in", immediateRender: false}, 14.05);
```

## Adapting it to the user's project
- Content: the order ticket is the dish's truth (weight, ageing, doneness); the VO is the chef's philosophy in 3–4 short lines; the ending ticket is the CTA (book, order, visit) with a real time and place.
- Language: Hebrew kitchens read right to left, times stay LTR mono.
- Brand: the restaurant name on the ticket logo, the station tape and the stamp word.
- Delivery apps: the ending ticket becomes the courier label, spiked as "on its way".

## Sound
- Ticket print: soft_tick trains at each line (vol .3); the stamp: a single soft_thump (.8); sizzling and knife sounds from the plate (plate .45), music .5.

## Pitfalls and QA checklist
- [ ] Smoke words sit on dark scrims or porcelain, never on a bright flame where they vanish.
- [ ] Each word condenses on its spoken syllable (word_times.py), not on a guessed grid.
- [ ] Ticket lines fit the slip width (no overflow at 39 px).
- [ ] The ticket lands exactly on the spike (x −590 from its start must meet the spike at x 754).
- [ ] Sparks are computed from t (no Math.random), so seeking is stable.
- [ ] Look at frames at 1.3, 3.2, 6.4, 9.6, 12.7 and 14.3; qa.py until "ship".
