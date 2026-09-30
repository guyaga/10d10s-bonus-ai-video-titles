# #23 MAP-FLYOVER · Aerial map explorer

> An aerial shot becomes a live map: a glowing route draws through tracked waypoints on the ground, pins pop up with bilingual cards stuck to real places, a distance readout counts up with the draw, lock brackets mark the destination, and an iris closes onto it.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/map-flyover.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/TEST_A_map_to_ono.mp4
> Runner: run_style MAP-FLYOVER · Example: examples/map-flyover

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: "how to get here" for campuses, hotels, venues and real estate; travel routes; delivery/logistics coverage; event arrivals; city guides. Pairs with ARRIVAL-CARD (#19) as the next shot.
- Avoid when: the camera rotates or tilts a lot (planar tracking breaks), the pinned places aren't visible from the first frame, or the geography is fictional but must look real (facts on cards must be true).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#iris` | a full-frame radial mask centred on the main pin; radius 2400 → 0 at the end | optional |
| `#route` SVG | a dotted ghost polyline (the whole route, fg at 35%, dash 4/12) + the drawn route (6 px accent, round joins, 6 px glow) + a route head (r 10) | points = tracked waypoints every frame |
| `.pin` | dot (22 px accent, dark 5 px ring, 24 px glow) + a pulse ring (60 px) + a 70 px stem + a card | `minor` pins are muted grey-green |
| `.card` | min 260 px, accent top rule; English 36 px/700, Hebrew 28 px/600 RTL, mono meta 18 px | card sits above the stem (or below with `below`), left or right |
| `#lock` | 4 corner brackets (34 px, 3 px) around the main pin, 140 px box | pulse 4× |
| `#title` | kicker chip (mono 20 px) + English 84 px/800 + Hebrew 44 px + a 120 × 3 px accent bar | top-left (112/96) |
| `#readout` | distance panel 560 px, bottom-left (112/104): label, big value + unit, two small facts, a 4 px progress bar | value counts with the route draw |
| `#chip` | "LIVE ROUTE" status chip with a blinking dot, top-right | optional |
| `.tick` ×4 | corner brackets | |

## Timing and motion
From `scripts/styles/mapflyover.py`; sample values in brackets.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| corner ticks | 0.1, stagger 0.05 | 0.5 (scale 1.4 → 1) | power3.out | whole clip | — | — |
| chip | 0.3 | 0.45 (x 24 → 0); dot blinks 0.5 × 18 | default / sine.inOut | — | at iris | 0.4 |
| title kicker | title.t [0.3] | 0.4 (y 12 → 0) | default | to `until` [6.3] | 0.5 (y −16) | power2.in |
| title English | t + 0.15 | 0.7 (y 40 → 0, clip wipe left → right) | expo.out | — | — | — |
| title Hebrew / bar | t + 0.45 / t + 0.5 | 0.5 / 0.6 (scaleX 0 → 1) | default / power3.inOut | — | — | — |
| each pin | pin.t [0.8, 1.5, 7.0] (default 0.8 + 0.7·i) | dot 0.35 (back.out(3)); ring 0.9 scale .3 → 1.6 fading; stem +0.15, 0.35; card +0.3, 0.5 (clip rising) | back.out / power2.out / power3.out / expo.out | — | dim_at → .55 over 0.6; hide_at → 0 over 0.4 | — |
| route draw | draw [2.0 → 7.0] | per frame, eased power2.inOut along the path length | — | — | — | — |
| readout | readout.t [1.9] | 0.5 (y 24 → 0) | power3.out | value = value × draw progress | 0.4 at `until` [8.4] | default |
| lock brackets | main pin t + 0.05, stagger 0.04 | 0.45 (scale 2.2 → 1) | power3.out | pulse to .35 yoyo 0.3 × 4 | — | — |
| iris | iris.t [8.4] | dur [1.55] radius 2400 → 0 | power2.inOut | — | — | — |
- The signature move: the route draws ON the ground. The polyline is rebuilt every frame from planar-tracked points, so as the drone moves, the line stays glued to the streets, and its head leads the distance counter.

## Typography
- Latin: **Secular One** 800 for the title (84 px, letter-spacing −.01em) and card names (36 px/700); **JetBrains Mono** for the kicker, meta, readout and chip (18–44 px).
- Hebrew: card lines 28 px/600 and the title's second line 44 px, `direction: rtl`, left-aligned under the English so both share the card's edge. Hebrew-first: put the Hebrew in `en` (it's just the main line) and the English in `he`.
- Max copy: title ≈ 20 characters at 84 px (900 px box, no wrap); card name ≈ 22; meta ≈ 34.

## Colour and surface
- Roles: `accent` #9bd14a, `fg` #eef4e8, `mute` #b7c6ad; panels `rgba(7,13,9,.78)` (radius 4–6 px).
- The route glow is the accent through a 6 px Gaussian blur merged over the line; for a brand, change `accent` (keep it saturated so it reads over city lights).

## Layout and safe zones (1920×1080 canvas)
- Title top-left, readout bottom-left, chip top-right: the left 30% must stay calm (the contract asks for 30% free on the left). Pins can be anywhere; choose `side` and `below` so cards don't collide with the title or readout.
- 9:16: title top, readout bottom, the route in the middle; drop the chip.

## What the footage must give you
- Shoot it like this: one take, no cuts, 8–12 s · high aerial, landmarks spread across the frame, the horizon or sea as a fixed reference · 30% free on the left · smooth drone, constant slow forward push and slight descent, no rotation.
- Seedance lines: "FORMAT: One continuous shot, no cuts." / "CAMERA: Smooth stabilized drone, constant slow speed, gentle forward push and slight descent only. FORBIDDEN: whip-pans, rotation, roll, zoom punches, shake, cuts." / "POSITIVE LOCKS: No text, no labels, no map graphics, no UI, no logos appear at any time. The geography stays fixed for the whole shot."
- Tracking: planar, with `scripts/track.py`. Pick the pin points and the route waypoints on frame 0 of the clip (pixel coordinates in the clip's own resolution) in `anchors.json`: `{"points": {"airport": [1040, 400], "r0": [1040, 400], "r1": [930, 455], ...}}`. vtrack.py output also works (box centres). Gate: 100% coverage.
- Matte: not needed.

## Build it
### A. With the kit
```bash
python scripts/track.py clips/aerial_720p.mp4 anchors.json tracks/aerial_points.json --preview check.mp4
python scripts/run_style.py MAP-FLYOVER --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip, track | plate + points json (track.py) or vtrack json | required |
| route | ordered tracked point names the line draws through | [] (no line) |
| draw | [start, end] seconds of the route draw | [2.0, 7.0] |
| pins | [{point, en, he, meta, t, side "left/right", below, dim_at, hide_at, main}] | required; main = lock + iris target (default the last pin) |
| title | {kicker, en, he, t, until} | none |
| readout | {label, value, unit, dec, left, right, t, until} | none |
| chip | status chip text | none |
| iris | {t, dur} close onto the main pin | none |
| colors | {accent, fg, mute} | #9bd14a / #eef4e8 / #b7c6ad |
| sfx / music / music_vol / plate_vol / name | sound + levels | true / – / – / .55 |
A minimal spec for a generic project (a hotel on the coast):
```json
{
  "name": "to-the-hotel",
  "clip": "clips/coast_aerial.mp4",
  "track": "tracks/coast_points.json",
  "route": ["r0", "r1", "r2", "r3"],
  "draw": [1.6, 6.0],
  "pins": [
    {"point": "station", "en": "Train station", "he": "תחנת הרכבת", "t": 0.8, "side": "right", "hide_at": 7.5},
    {"point": "hotel", "en": "Villa Ha'Galim", "he": "וילה הגלים", "meta": "32.500°N 34.890°E", "t": 6.2, "main": true}
  ],
  "title": {"kicker": "ROUTE · 8 MIN", "en": "STATION TO SEA", "he": "מהרכבת אל הים", "t": 0.3, "until": 5.6},
  "readout": {"label": "BY CAR", "value": 3.4, "unit": "km", "dec": 1, "left": "≈ 8 min", "right": "free parking", "t": 1.5, "until": 7.8},
  "colors": {"accent": "#4fc3d9"},
  "iris": {"t": 8.0, "dur": 1.4}
}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
const c = (n, t) => { const b = boxAt(n, t); return b ? [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2] : null; };
const ease = gsap.parseEase("power2.inOut");
function partial(pts, u) {                        // the first u (0..1) of the polyline by length
  const seg = []; let L = 0;
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0] - pts[i-1][0], pts[i][1] - pts[i-1][1]); seg.push(d); L += d; }
  let want = L * u; const out = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    if (want >= seg[i-1]) { out.push(pts[i]); want -= seg[i-1]; continue; }
    const f = seg[i-1] ? want / seg[i-1] : 0;
    out.push([pts[i-1][0] + (pts[i][0] - pts[i-1][0]) * f, pts[i-1][1] + (pts[i][1] - pts[i-1][1]) * f]); break;
  }
  return out;
}
window.onPlace = (t) => {
  const pts = ROUTE.map((r) => c(r, t)).filter(Boolean);            // re-read the tracked points every frame
  const u = ease(Math.max(0, Math.min(1, (t - DRAW[0]) / (DRAW[1] - DRAW[0]))));
  document.getElementById("rl").setAttribute("points", (u > 0 ? partial(pts, u) : []).map((p) => p.join(",")).join(" "));
  document.getElementById("km").textContent = (12.8 * u).toFixed(1);   // the counter rides the same u
};
```

## Adapting it to the user's project
- Content: 2–4 pins (start, landmarks, destination); one title (the journey in 3–4 words); one readout (a true distance and time).
- Language: bilingual cards by default; the facts (coordinates, km, minutes) stay in mono.
- Brand: `accent`; keep the dark panels so cards read over any city.
- No route: omit `route` and keep pins + title (a "places near you" map).
- Longer drones: pins with `dim_at`/`hide_at` let the map breathe as places pass by.

## Sound
- Cues: ui_whoosh 0.25 (.45), glass_ting at each pin (.55), scan_beeps at the draw start (.2), chime at the draw end (.5), logo_hit at the iris (.6). Plate .55.

## Pitfalls and QA checklist
- [ ] Anchor points are picked on frame 0 in the clip's own pixels; check the track.py `--preview`: the dots must stay on the streets for the whole clip.
- [ ] Use `--mask-top` in track.py if the sky/horizon has no features, or tracking drifts.
- [ ] Every fact on the cards is real (coordinates, distance by road, time).
- [ ] Cards don't cover the title, readout or each other: set `side` / `below`.
- [ ] The main pin is visible when the iris closes.
- [ ] Look at frames at the title, mid-draw, the main pin and the iris; qa.py until "ship".
