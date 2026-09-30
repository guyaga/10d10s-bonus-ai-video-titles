# #20 ROAD-HUD · Automotive AR head-up display

> Everything is projected light on the windscreen: lane guides and a chevron ladder lie flat on the real road in true 3D perspective, a split speed ring counts down as the car brakes, a soft amber contour hugs a cyclist with a warning strip bolted to them, an AEB pictogram flashes once, and the ending is written in light on the wet road.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/road-hud.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E3_aura_night_drive_BESPOKE.mp4
> Runner: bespoke (`references/recipes/bespoke/E3_car_bespoke.py`, 18 s, 5 shots) · Example: none shipped (build from the recipe)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: cars and EVs, driver-assist and safety tech, mobility apps, navigation, e-bikes and scooters, fleet/insurance ("the car saw it first").
- Avoid when: there's no road plane or windscreen view in the footage, the brand wants loud stomp titles (this language is calm), or the clip is a single static shot (the story needs interior → POV → exterior).

## The design method (crafted world)
Ask: **what does this subject's world project, measure or display?** A car's world already has a HUD language: speed, lanes, braking distance, hazard warnings, a stop line. So every title becomes one of those instruments, and every instrument obeys the physics of the scene:
1. **Put type where the world would put it.** Road graphics live ON the road plane (CSS 3D, `rotateX(90deg)` about the near edge, perspective origin at the shot's vanishing point). Glass graphics are clipped to the windscreen polygon.
2. **Drive every number from one model of the event.** One speed profile (54 km/h, braking from 8.6 s to a stop at 11.6 s) drives the speed ring, the distance travelled (integrated per frame), the chevron ladder's flow, the braking-force g-meter (its derivative), and the rider's distance. Nothing is keyframed by hand, so nothing disagrees.
3. **Let the assistant live inside an instrument.** The co-pilot has no avatar: it's the thin right half of the speed ring, breathing with the voice's loudness envelope and turning amber at the hazard.
4. **Keep the motion the world's own:** projected light fades and "paints" in; no stomps, no shakes. The one hard event (AEB) gets one hard flash.

Worked example (this sample, AURA EV at night): conditions line ("night · rain · wet road") → the assistant's "I'm with you" → the rider is contoured long before anyone says so → POV warning strip "rider on the right, in the dark" with distance counting down → AEB flash + "braking." + g-meter → exterior: the car writes "he's fine. / you're fine." on the road → fact "0.8 seconds before you saw him" → brand painted on the wet ground.

It transfers to:
- **A cycling or scooter safety app:** the handlebar is the "windscreen"; lane and hazard graphics on the bike path, the speed ring on the bars, a car contoured in amber.
- **A drone or delivery robot:** the "road plane" is the ground under it; a path ladder flows to the drop-off, obstacles get contours, and the drop point is written on the ground.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `.r3d` road planes (r1…r4) | a 3D plane per shot: `perspective: P px`, `perspective-origin: vx vy`, plane `rotateX(90deg)` | r1 interior (vx 1330, vy 402, h 198, P 700); r2 POV (900, 548, 452, 900); r3 exterior (960, 700, 380, 900); r4 close (345, 300, 780, 900) |
| `.lane` | 7–9 px glowing lane lines, 16 000 px deep | draw with `scaleY 0 → 1` |
| `.chev` | a chevron ladder (SVG background repeat every 260 px), masked to fade with depth | background-position = −distance × 26 (interior) / 60 (POV) |
| `.bb` braking band | a glowing band on the road (cyan; amber in POV) | its depth = braking distance, animated per frame |
| `#ws` | windscreen clip-path polygon | interior HUD exists only inside the glass |
| `.patch` | dark radial "combiner" patches behind glass text | keeps light type readable over city lights |
| `.gauge` split ring | 240-unit SVG: left arc = speed (54 → 0), right thin arc = co-pilot voice | 92–104 px weight-200 digits inside |
| `#gmet` | braking-force g-meter arc + value | amber, shot 3 only |
| `#aeb` | amber AEB pictogram (car + cyclist) with a bloom | one hard flash |
| `#cyc` / `#cycL` / `#cycR` | soft contour on the tracked cyclist + distance label + a bolted-on warning strip | amber, turns cyan when safe |
| `.msg` | glass text blocks (RTL): 24 px label + 54 px row, or 104 px weight-300 "big" row | glow + a faint second reflection |
| `.rword` | words painted on the road plane (200 px, scaleY 1.8) | the exterior "he's fine" lines and the brand |

## Timing and motion
Cuts in the sample: 0, 5.04, 8.42, 12.0, 14.71, 18.05. Durations and eases from the recipe.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| lane guides (r1) | 0.15 | 1.4 (scaleY 0 → 1) | power2.inOut | shot | — | — |
| chevron ladder | 0.7 | 0.8 (to .85) | default | flows with distance | — | — |
| speed ring | 0.3 | 0.7 (blur 6 → 0) | power2.out | whole piece | — | — |
| conditions line | 0.55 | show 0.35 fade | sine.out | to 3.22 | 0.3 | sine.in |
| each word | its VO time | paint 0.45–0.8 | power2.out | — | — | — |
| cyclist contour + label | 2.0 / 2.25 | 0.6 / 0.5 | sine.out | to the cut | 0.15 | sine.in |
| POV warning strip | 5.62 | 0.3 (x 24 → 0) + strip wipe 0.35 | power2.out | to the cut | 0.12 | default |
| braking band (POV) | 6.0 | height 0 → 430 over 0.8 | smoothstep | — | — | — |
| AEB pictogram | 8.45 | 0.14 (scale 1.28 → 1) + bloom fading over 0.55 | power3.out | to 10.9 | 0.4 | sine.in |
| "braking." | 8.6 | paint 0.7 | power2.out | to the cut | 0.25 | sine.in |
| g-meter | 8.62 | 0.3 | sine.out | to the cut | 0.2 | sine.in |
| stop line (exterior) | 12.05 | 0.7 (scaleX 0 → 1) | power2.out | — | — | — |
| road words | 12.3 / 13.44 | paint 0.7 | power2.out | — | — | — |
| fact card | 14.78 | 0.5 | sine.out | to end | — | — |
| brand on the wet surface | pool 15.2 (0.9), stop line 15.3 (0.8), AURA 15.4, EV 16.05, tagline 16.28 | paint 0.45–0.7 | power2.out | to end | — | — |
- **Paint (the signature move):** each word is revealed by a clip from its reading edge while it sharpens from blur(6px) and opacity .2 to crisp: Hebrew from the right (`inset(0 0 0 100%)` → 0), Latin from the left. It reads as light being projected, not as a title appearing.
- Speed: `v(t) = 54` until 8.6 s, then `54 × (1 − u)^1.35` with `u = (t − 8.6)/3`. Distance is integrated per frame; g-force is the derivative, ramped in over 0.35 s.

## Typography
- Hebrew: **Secular One** for all HUD text (the original render used Heebo 200–700; the kit remaps it to Secular One). Use size and opacity for hierarchy: label 24 px dim, row 54 px, big row 104 px, road words 200 px.
- Digits: big light numerals (92–104 px) with `font-variant-numeric: tabular-nums` so the speed doesn't jitter; the brand "AURA EV" is Latin, painted left to right, letter-spacing .2em.
- RTL: glass blocks are `direction: rtl` and right-aligned; the paint reveal runs right → left for Hebrew. Distances in meters use the Hebrew unit "מ׳" after a tabular number.
- Max copy: one short line per glass block (≤ 18 characters at 104 px); road words ≤ 10 characters (they're 200 px and stretched).

## Colour and surface
- Palette: HUD white #e6f8ff, glow `rgba(110,215,255,.55)`, cyan #7fdcff, amber #ffb45c for hazard, AEB amber #ffab1f, dim `rgba(210,240,255,.62)`.
- Surfaces: no panels. Readability comes from light glows (`0 0 16px` glow + a dark `0 2px 18px` shadow + a faint 4/5 px "second reflection") and dark combiner patches behind the glass text.
- Brand swap: change the cyan to the brand's light colour; keep amber for danger (a safety language shouldn't be rebranded red).

## Layout and safe zones (1920×1080 canvas)
- Interior: glass text right-aligned at right 862 px (inside the windscreen polygon), the speed ring at 694×430 (206 px), the g-meter at 846×352, the AEB pictogram at 560×104.
- POV: speed ring bottom-left (250×862, 236 px), the warning strip on the cyclist's top-left.
- Each road plane needs its own vanishing point, measured on the shot's first frame: where the lane lines meet (`vx, vy`), and the screen distance from the vanishing point to the plane's near edge (`h`).
- 9:16: this world depends on a wide windscreen; crop to 9:16 only for the POV and exterior shots.

## What the footage must give you
- Shoot it like this: planned cut list (max 4), 15–20 s · windscreen POV with the road's vanishing point visible; the hazard enters from one side · 30% free at the bottom · smooth, steady, no shake.
- Seedance lines: "FORMAT: Timestamped cut-blocks. HARD CUTS exactly at the listed timecodes and nowhere else." / "COMPOSITION: In the driving shots the road surface ahead fills the lower third and its vanishing point stays visible." / "CAMERA: smooth, steady. FORBIDDEN: shaky cam, whip-pans." / "POSITIVE LOCKS: exactly one car, one driver, one hazard. The car never hits anything. No text, no logos, no signage, no UI, no graphics at any time."
- Tracking (vtrack.py): `cyclist` (or your hazard), optionally `driver`, `car`. Gate: ≥60% coverage (the hazard is only in some shots).
- Voice: an AI co-pilot VO; compute its loudness envelope (`env`) so the ring's right arc breathes.
- Matte: not needed.

## Build it
### A. With the kit (bespoke route)
```bash
python scripts/vtrack.py clips/drive.mp4 drive_objects.json tracks/drive_vtrack.json
python scripts/run_ad.py DRIVE --spec specs/drive_roadhud.py --render
```
Start from `references/recipes/bespoke/E3_car_bespoke.py` and change, in this order:
| Recipe constant | What it is | Sample value |
|---|---|---|
| `CUT` | the shot boundaries in seconds | [0, 5.04, 8.42, 12.0, 14.71, 18.05] |
| `ROADS` | per road plane: vx, vy (vanishing point), h (VP to near edge), P (perspective), W, L | measured on each shot's first frame |
| `R1_IN` … `R4_IN` | what lies on each plane (lanes, chevrons, band, painted words) via `on(rid, x, depth, w, h, cls)` | lateral x from centre, depth in px |
| `spd(t)` | the speed model (drives everything numeric) | 54 → 0 from 8.6 to 11.6 |
| `HTML` glass text | the conditions / assistant / hazard / fact lines | Hebrew |
| `#ws` clip-path | the windscreen polygon in the interior shot | 7 points |
| `SPEC` | theme `he_bold`, palette, `music_vol` .42, `plate_vol` .45, `vo_name`, `env` (voice loudness per frame) | — |
Spec keys (adkit bespoke): `clip`, `track`, `theme`, `palette`, `html_front`, `css`, `js`, `fonts`, `assets`, `elements` ([]), `env`, `vo_name`/`vo`, `music`, `music_vol`, `plate_vol`.
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// a road plane: the container's perspective-origin is the shot's vanishing point; the plane lies flat on the road
// <div class="r3d" style="perspective:900px;perspective-origin:900px 548px">
//   <div class="pl" style="transform-origin:50% 100%;transform:rotateX(90deg);left:..;top:..;width:5000px;height:16000px">...</div></div>
const spd = (t) => t < 8.6 ? 54 : 54 * Math.pow(1 - Math.min(1, (t - 8.6) / 3), 1.35);
const DIST = [0]; for (let f = 1; f <= 460; f++) DIST.push(DIST[f - 1] + spd((f - .5) / 24) / 3.6 / 24);   // metres, per frame
window.onPlace = (t) => {
  const v = spd(t), m = DIST[Math.min(DIST.length - 1, Math.round(t * 24))];
  document.querySelectorAll(".spdN").forEach((n) => n.textContent = Math.round(v));
  document.querySelectorAll(".gspd").forEach((p) => p.style.strokeDasharray = `${(v / 60 * 100).toFixed(2)} 200`);
  document.getElementById("r2d").style.backgroundPosition = `0 ${-(m * 60) % 260}px`;   // chevrons flow at the car's speed
};
// projected-light "paint": Hebrew is revealed from the right edge while it sharpens out of a blur
const paint = (sel, at, dur = .6) => tl.fromTo(sel, {clipPath: "inset(0 0 0 100%)", filter: "blur(6px)", opacity: .2},
  {clipPath: "inset(0 0 0 0%)", filter: "blur(0px)", opacity: 1, duration: dur, ease: "power2.out", immediateRender: false}, at);
paint("#w6", 8.6, .7);
tl.fromTo("#aeb", {opacity: 0, scale: 1.28}, {opacity: 1, scale: 1, duration: .14, ease: "power3.out", immediateRender: false}, 8.45);
```

## Adapting it to the user's project
- Content: map the VO lines onto instruments: conditions → glass line; the assistant → the ring arc; the hazard → contour + strip; the decisive action → pictogram + one big word; the resolution → words on the road; proof → one fact number.
- Language: Hebrew paints right → left, English left → right; don't mix directions within one line.
- Brand: the light colour and the brand line painted on the ground at the end; never a logo sticker over the footage.
- Vehicles without a windscreen: skip `#ws`; keep the road planes.
- Shorter pieces: interior + POV only (about 8 s): conditions, hazard strip, AEB, "braking.", brand on the road.

## Sound
- Soft synthesized UI chimes were pre-mixed into the VO file in the sample (no kit SFX cues). Use soft_tick / soft_pulse / chime from assets/sfx at the paint moments, a single warn_beep at the AEB flash, and keep the rain/road ambience (plate_vol .45, music .42).

## Pitfalls and QA checklist
- [ ] Each road plane's vanishing point matches the footage: lanes must lie ON the road and converge with the real curbs. Check a frame per shot.
- [ ] Glass text stays inside the windscreen polygon and over a dark patch (readability over city lights).
- [ ] Every number comes from the one speed model (speed, distance, g, rider distance agree).
- [ ] The paint direction matches the language (Hebrew from the right).
- [ ] Group visibility switches exactly at the cuts (`tl.set` on the CUT times), so no interior graphic flashes over the exterior shot.
- [ ] Look at frames at each cut ± 2 frames, at the AEB flash and at the brand; qa.py until "ship".
