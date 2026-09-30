# #19 ARRIVAL-CARD · Destination lower-third

> A person arrives in front of the destination: brackets lock on their head with a green "ARRIVED ✓ · הגעת" chip, a bilingual destination card rises from the bottom-left with coordinates, a route line slides in under it, and the destination's logo lands on a blank patch of the facade.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/arrival-card.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/A2_final.mp4
> Runner: bespoke (reference recipe `references/recipes/legacy_shots.py` → `A2`, 6 s) · pairs with run_style MAP-FLYOVER (#23) as the next shot · Example: none shipped

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: travel and campus films, hotel/venue arrivals, real-estate "you're home" moments, event openers, the landing shot after a MAP-FLYOVER.
- Avoid when: there's no clear destination in frame, the person is too small to bracket, or there's no clean facade area for the logo (drop the logo then).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `.tick` ×4 | corner brackets | green-tinted |
| `#head-brk` | 4-corner brackets on the tracked `head`, 22 px pad | accent corners |
| `#arr` | chip centred above the head (anchor t, dy −40): "ARRIVED ✓" 30 px/800 green + Hebrew "הגעת" 28 px/700 | `translate(-50%,-100%)` |
| `#loc` | destination card, left 112 / bottom 112, 620 px, 3 px green top rule | kicker mono 18 px .2em; English 52 px/800; Hebrew 40 px/600; mono sub 22 px (place + coordinates) |
| `#route` | route strip, left 112 / bottom 56, mono 20 px .08em | "TLV → ONO · 12.8 km by road · ≈17 min" |
| `#logo` | the brand logo (330 px wide, light drop shadow) centred on the tracked `facade_blank` | lands with a brightness flash |

## Timing and motion
From `legacy_shots.py` `A2` (6 s plate).
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| corner ticks | 0.05, stagger 0.05 | 0.5 (scale 1.4 → 1) | power3.out | whole clip | — | — |
| head brackets | 0.3 | 0.45 (scale 1.6 → 1) | power3.out | to 3.6 | 0.35 | default |
| ARRIVED chip | 0.45 | 0.45 (y 14 → 0) | back.out(2) | to 3.6 | 0.35 | default |
| destination card | 1.0 | 0.6 (y 30 → 0 + clip rising from the bottom) | expo.out | to end | — | — |
| Hebrew line | 1.35 | 0.45 (x −16 → 0) | power2.out | — | — | — |
| route strip | 2.5 | 0.45 (x −24 → 0) | power2.out | to end | — | — |
| logo | 4.2 | 0.9 (scale .82 → 1, brightness 3 → 1) | expo.out | to end | — | — |
- The signature move: the logo "lands" on the real building: it's placed on a tracked blank area of the facade and flashes from brightness 3 down to 1, like a sign switching on.

## Typography
- Latin: **Secular One** 800 for the destination and chip; **JetBrains Mono** for the kicker, coordinates and route (uppercase, letter-spaced).
- Hebrew: Secular One 40 px (destination) and 28 px/700 (chip). The sample keeps the Hebrew line left-aligned under the English (`text-align:left`) so both lines share one edge; for a Hebrew-first piece, put Hebrew on top and right-align the card.
- Max copy: destination ≈ 22 characters at 52 px (620 px card); route strip ≈ 50.

## Colour and surface
- The "A palette" (shared with MAP-FLYOVER and CAMPUS-AR): accent #9bd14a (green), fg #eef4e8, mute #b7c6ad, panel `rgba(7,13,9,.78)`, radius 6 px.
- Rebrand with the destination's colour on the chip, the card rule and the brackets.

## Layout and safe zones (1920×1080 canvas)
- Card bottom-left (112/112), route under it (112/56), chip above the head, logo on the facade (the contract asks for 35% free on the left for the card).
- 9:16: the card becomes a full-width strip at the bottom; the chip stays above the head.

## What the footage must give you
- Shoot it like this: one take, no cuts, 5–10 s · the person walks toward camera, the destination facade behind with a blank area for the logo · 35% free on the left · slow steady dolly backwards at chest height matching the walk.
- Seedance lines: "FORMAT: One continuous shot, no cuts." / "CAMERA: Slow steady dolly backwards at chest height, matching his walking speed so he stays the same size in frame. FORBIDDEN: whip-pans, zooms, shake, cuts." / "POSITIVE LOCKS: Exactly one person in focus. No text, no signs with readable letters, no logos, no UI appear at any time."
- Tracking (vtrack.py): `head` (head and face only) and `facade_blank` (a plain wall area of the building where a sign could hang). Gate: ≥95% coverage.
- Matte: not needed.
- Good footage: a recognisable entrance, a person arriving calmly, a blank facade panel. Bad: AI-generated signage with fake letters (it fights your logo), crowds.

## Build it
### A. With the kit
No run_style builder; build it as a bespoke adkit spec and run:
```bash
python scripts/vtrack.py clips/arrive.mp4 arrive_objects.json tracks/arrive_vtrack.json
python scripts/run_ad.py ARRIVE --spec specs/arrive_card.py --render
```
Bespoke spec keys: `clip`, `track`, `theme`, `palette` {acc, ink, lt, panel, sub}, `html_front`, `css`, `js`, `fonts`, `assets` (put the logo here: `{"logo.png": "path/to/logo.png"}` → `assets/logo.png`), `elements` ([]), `music`, `music_vol`, `plate_vol`.
A minimal spec (a hotel arrival):
```python
TICKS = '<div class="tick tk1"></div><div class="tick tk2"></div><div class="tick tk3"></div><div class="tick tk4"></div>'
BRK = '<div class="brk"><i></i><i></i><i></i><i></i></div>'
SPEC = {
  "theme": "he_bold", "palette": {"acc": "#9bd14a", "ink": "#070d09", "lt": "#eef4e8", "panel": "rgba(7,13,9,.78)", "sub": "#b7c6ad"},
  "elements": [], "assets": {"logo.png": "brand/hotel_logo.png"}, "plate_vol": .6,
  "html_front": f"""{TICKS}
<div id="head-brk" data-box="head" data-pad="22">{BRK}</div>
<div id="arr" class="panel tag" data-follow="head" data-anchor="t" data-dy="-40"><span class="en">CHECKED IN ✓</span><span class="he">הגעתם</span></div>
<div id="loc" class="panel"><span class="kick mono">DESTINATION</span>
  <span class="en">Villa Ha'Galim</span><span class="he">וילה הגלים</span>
  <span class="sub mono">Caesarea · 32.500°N 34.890°E</span></div>
<div id="route" class="panel mono">TLV → CAESAREA · 58 km · ≈45 min</div>
<div id="logo" data-follow="facade_blank" data-anchor="c"><img src="assets/logo.png" alt=""></div>""",
  "css": "<the A2 css from the recipe: .tag, #arr, #head-brk, #loc, #route, #logo>",
  "js": "<the timeline in B below>",
}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
tl.fromTo(".tick", {opacity: 0, scale: 1.4}, {opacity: 1, scale: 1, duration: .5, stagger: .05, ease: "power3.out"}, .05);
tl.fromTo("#head-brk .brk", {opacity: 0, scale: 1.6}, {opacity: 1, scale: 1, duration: .45, ease: "power3.out"}, .3);
tl.fromTo("#arr", {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: .45, ease: "back.out(2)"}, .45);
tl.fromTo("#loc", {opacity: 0, y: 30, clipPath: "inset(100% 0 0 0)"},
                  {opacity: 1, y: 0, clipPath: "inset(0% 0 0 0)", duration: .6, ease: "expo.out"}, 1.0);
tl.fromTo("#loc .he", {opacity: 0, x: -16}, {opacity: 1, x: 0, duration: .45, ease: "power2.out"}, 1.35);
tl.fromTo("#route", {opacity: 0, x: -24}, {opacity: 1, x: 0, duration: .45, ease: "power2.out"}, 2.5);
tl.to(["#arr", "#head-brk .brk"], {opacity: 0, duration: .35}, 3.6);
// the sign switches on: bright flash settling to normal (filter keeps the drop shadow)
tl.fromTo("#logo img", {opacity: 0, scale: .82, filter: "brightness(3) drop-shadow(0 2px 6px rgba(0,0,0,.25))"},
  {opacity: 1, scale: 1, filter: "brightness(1) drop-shadow(0 2px 6px rgba(0,0,0,.25))", duration: .9, ease: "expo.out"}, 4.2);
```

## Adapting it to the user's project
- Content: the chip is the emotion ("ARRIVED", "WELCOME HOME", "CHECKED IN"), the card is the fact (place name in two languages + coordinates), the route is the journey (distance + time). All facts must be real: check the coordinates and distances.
- Language: bilingual by design; Hebrew-first projects swap the order.
- Brand: logo on the facade + the accent colour.
- As the second shot of a MAP-FLYOVER: reuse the same card text and colours so the map's last card "becomes" this card.

## Sound
- A2 cues: chime 0.35 (.7), ui_whoosh 0.95 (.6), ui_tick 1.3 (.4), ui_pop 2.5 (.6), logo_hit 4.15 (.8). Plate at .6.

## Pitfalls and QA checklist
- [ ] The logo sits on a truly blank wall in every frame (the facade_blank box must be stable; a jittery box makes the logo swim).
- [ ] The chip clears the top of the frame as the person gets closer (dy −40 from the head's top).
- [ ] The card never covers the person (they should be centre/right; the card lives in the left 35%).
- [ ] Coordinates and distances are real.
- [ ] Look at frames at 1.2, 3.0 and 5.5; qa.py until "ship".
