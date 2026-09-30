# #21 THERMAL-RESCUE · The frame is a thermal camera

> The footage itself becomes a thermal-imaging viewfinder: everything turns steel blue-grey and only the hottest tones go amber to white; a crosshair reads spot temperatures, an oxygen gauge drains from 100% to 7%, an ECG line beats, the AI speaks as amber on-screen text, and at the rescue the camera switches off into calm natural colour.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/thermal-rescue.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E4_firelink_through_the_smoke_BESPOKE.mp4
> Runner: bespoke (`references/recipes/bespoke/E4_fire_bespoke.py`, 20 s) · Example: none shipped (build from the recipe)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: firefighting, emergency services, safety equipment, industrial inspection, search and rescue, night-vision/defence products, documentary tension.
- Avoid when: the footage is bright daylight (the luminance-to-heat mapping needs dark scenes where the hottest things are the brightest), or the brand story is light and playful.

## The design method (crafted world)
Ask: **what does this subject's world measure or display?** A firefighter doesn't see the world; they see it through instruments: a thermal imaging camera (TIC), an SCBA air gauge, a PASS alarm, a radio. So:
1. **Turn the plate into the instrument.** An SVG colour-table filter maps luminance to a thermal palette (steel blue for cool, amber → white for hot). The footage stops being "a video with titles" and becomes the TIC's feed.
2. **Every overlay is a real piece of the kit:** the TIC's viewfinder bezel, IRON palette strip and REC clock; the SCBA dial (oxygen 100 → 7%, 300 → 21 bar); the PASS device (green chirp, then a red/amber strobe when air is low); the crew accountability tag (PAR); the radio link.
3. **The voice speaks in the instrument's own type:** single-line on-screen-display text, one monospaced cell per character, typed at 34 characters/s, with a 1 px black outline.
4. **One heartbeat drives everything:** a beat grid (0.52 s, about 115 bpm) pulses the reticle, the heat blobs, the gauge glow and the ECG. At the exit the period becomes 0.95 s and everything calms.
5. **Resolve by switching the instrument off:** a white bloom, natural colour returns, the UI turns white, and the end is a physical badge (the helmet-shield decal).

Worked example (FIRELINK): boot in natural colour → TIC switches on at the cut (3.67) → spot temperature climbs 180 → 640 °C → "second door, on the right" chevrons → heat signature behind the door → the words "one person" themselves appear as a white-hot thermal image on cold blue → the reticle locks on the child (36.8 °C) → exit: bloom, calm, "7% oxygen. enough." → shield.

It transfers to:
- **An EV battery inspection or solar maintenance service:** the drone's thermal view, hot cells glowing, a panel temperature scale, a "cell 14 · 71 °C" tag; the resolve is a green "all cells normal".
- **A hunting/wildlife or night-security camera brand:** the animal as the heat signature, a range finder, a battery gauge instead of oxygen, and the switch-off to dawn colour.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| plate filter `#th` | `feColorMatrix` to luminance → `feComponentTransfer` tables (R/G/B, 11 steps) | applied to the plate only between the TIC cut and the exit |
| `#vig`, `#topfade`, `#scan`, `#band` | vignette, top darkening, 2/4 px scanlines (multiply), a moving 140 px glow band | band moves 520 px/s |
| `.blob` door / kid | screen-blended radial heat signatures on tracked targets | size and opacity pulse with the heartbeat |
| `#bez` | the viewfinder bezel: 26 px rounded frame 44 px in, 56 px amber corners | |
| `#topL` / `#topR` / `#link` | "FIRELINK TIC · IRON 1×", REC dot + running clock, radio link "RX CH3 ORA" | mono 20–24 px |
| `#boot` | "thermal camera · starting" + a progress bar (0.2 → 3.5 s) | natural-colour part |
| `#crew` / `#pass` | PAR crew count; PASS device with two LEDs | |
| `#scale` | 22 × 470 px IRON palette strip, 0–800 °C labels, a marker at the spot temperature | right 84, top 250 |
| `#ret` | crosshair (r 54 dashed ring, ticks, amber corner brackets) + SPOT value + RNG distance + lock label | centre, glides onto the child |
| `#gz` | 300 px SCBA dial: 270° scale 0–100, red 0–30 zone, needle, % and BAR readouts | left 78, top 676 |
| `#ecg` | 560 × 90 live ECG trace of the last 2.4 s + BPM | right side, top 860 |
| `#osd` | the typed voice line under the top bar | amber cells |
| `#m5` | the words as heat: 300 px text with a radial white-hot gradient clipped to the letters | 12.3 → 13.8 |
| `#end` / `#shield` | "7% oxygen. / enough." and the helmet-shield decal | white after the exit |
| `#bloom` / `#blk` | white bloom at the exit; black cover at the TIC cut | |

## Timing and motion
Key times in the sample: TIC 3.667, door 9.875, black 12.45, child 13.875, exit 17.04, end 20.04.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| bezel | 0.05 | 0.5 (scale 1.04 → 1) | expo.out | whole piece | — | — |
| top bar / link / crew | 0.2, stagger 0.12 | 0.05 (snap on) | default | — | exit | 0.3–0.5 |
| oxygen gauge | 0.9 | 0.5 (scale .6 → 1, rotate −30 → 0) | back.out(1.6) | drains from 4.2 to 17.0 | moves up and scales 1.25 at exit + 0.1 over 0.9 | power3.inOut |
| ECG | 1.1 | 0.4 (x 40 → 0) | power3.out | — | — | — |
| thermal switch-on | 3.667 | plate filter on; black cover .9 → 0 over 0.25; reticle scale 2.2 → 1 over 0.3 | expo.out | to exit | — | — |
| OSD voice lines | per message (0.45, 4.25, 7.25, 10.05, 14.15) | typed 34 chars/s; flickers for the first 0.16 s | — | to each `b` | cut | — |
| chevrons ">>>" | 8.8 | 0.12 each, stagger 0.12, ×3 | steps(1) | to 9.8 | — | — |
| door heat signature | 10.0 | fades in over 0.4 | — | to 12.45 | — | — |
| "one person" as heat | 12.3 | 0.16 (scale 1.25 → 1) on a cold-blue field (0.14) | power4.out | to 13.8 | 0.12 | default |
| reticle lock | 13.875 + 0.15 | glides to the child over 0.5 (cubic out) | — | lock label from 14.2 | at exit | — |
| exit bloom | exit − 0.14 | 0.12 up | power2.in | — | 1.1 down | power2.out |
| end numbers / "enough." | 16.95 / 18.22 | 0.5 | power3.out | — | 0.35 at 19.2 | default |
| shield | 18.95 | 0.38 (scale 1.4 → 1, rotate −10 → −3) | back.out(1.5) | to end | — | — |
- Oxygen: `100 − 93 × u^0.6` with `u` over 4.2 → 17.0 s; below 30% the arc and value turn red and "low oxygen" blinks at 4 Hz.
- Spot temperature: 180 → 640 °C over the search, about 560 °C at the door, 36.8 °C on the child, −2 °C outside; each has a seeded jitter.
- The signature move: the plate itself is re-coloured by the instrument, and at the resolve the instrument switches off.

## Typography
- Hebrew OSD text: **Secular One** in fixed-width cells (27 px per character, 34 px per space, 46 px size), amber with a 1 px black outline. The original used IBM Plex Sans Hebrew; the kit remaps it to Secular One.
- Big Hebrew words (the gauge label, "low oxygen", "one person", "enough."): **Karantina 700** (40 / 50 / 300 / 170 px).
- Digits and system text: **JetBrains Mono** 700 (letter-spacing .06em).
- The shield: Latin "FIRELINK" on an arc in a heavy serif, a Hebrew ribbon line in Karantina.
- RTL: OSD lines type right → left inside an RTL flex row; temperatures and percentages stay in mono LTR spans.
- Max copy: one OSD line ≈ 22 characters (it's one row across the top); a heat word ≤ 10 characters at 300 px.

## Colour and surface
- Instrument colours: amber #ffb21a (UI accent, OSD), hot #ff4a1c (needle, ECG, REC), UI white #e8eef5, ice #eaf4ff; after the exit every UI colour becomes #ffffff.
- The thermal table (R/G/B tableValues from the recipe) is what makes it look like a TIC; keep it as-is and change only the UI accent for a brand.
- Surfaces: no glass panels; black outlines and dark translucent backings (`rgba(8,10,14,.6–.82)`) like real camera UI.

## Layout and safe zones (1920×1080 canvas)
- Top bar at 70 px (left brand, centre link, right REC), OSD at 112, gauge bottom-left, ECG bottom-right, heat scale right edge, crosshair centre. The contract needs no free space: the UI frames the picture, like a real viewfinder.
- 9:16: stack the gauge and ECG at the bottom; the scale moves to the left edge.

## What the footage must give you
- Shoot it like this: planned cut list (max 5), 15–24 s · mid shots and close-ups; the searched object (door, person) clearly readable as a shape · no free space needed · steady handheld feel, no shake.
- Seedance lines: "FORMAT: Timestamped cut-blocks. HARD CUTS exactly at the listed timecodes and nowhere else." / "LIGHTING: dark interiors lit mainly by fire, so the hottest areas are the brightest (the post filter maps luminance to heat)." / "CAMERA: steady handheld feel, no shake. FORBIDDEN: whip-pans, zoom punches." / "POSITIVE LOCKS: exactly one rescuer and one person rescued. No text, no logos, no signage, no UI, no graphics at any time."
- Tracking (vtrack.py): `door` (the target of the search) and `child` (the found person); optionally the searcher. Gate: ≥30% coverage (targets appear only in some shots).
- Matte: not needed.

## Build it
### A. With the kit (bespoke route)
```bash
python scripts/vtrack.py clips/rescue.mp4 rescue_objects.json tracks/rescue_vtrack.json
python scripts/run_ad.py RESCUE --spec specs/rescue_thermal.py --render
```
Start from `references/recipes/bespoke/E4_fire_bespoke.py` and change:
| Recipe constant | What it is | Sample value |
|---|---|---|
| `CUT_TIC, CUT_DOOR, BLACK0, CUT_CHILD, CUT_EXIT, END` | when the TIC switches on, the key shots, the exit | 3.667, 9.875, 12.45, 13.875, 17.04, 20.04 |
| `P1, T0` | heartbeat period and phase (0.52 s ≈ 115 bpm; calm 0.95 s after the exit) | 0.52, 0.03 |
| `MSG` | the OSD voice lines: {a, b, prefix, [(start, text)]} | 5 messages |
| `o2At`, `spotAt` | the oxygen and temperature models | see the recipe |
| `GAUGE`, `SHIELD` | the instrument dial and the end badge | SVG builders |
| the `#th` table values | the thermal palette | keep |
Note: the recipe loads the sample's Hebrew tape spec (`specs/E4_fire_hk.py`) only for its audio levels and voice; replace those three lines with your own `music_vol`, `plate_vol` and `vo_name`.
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// 1) the thermal plate: luminance -> table-mapped heat colours (SVG filter), applied only while the camera is "on"
// <filter id="th" color-interpolation-filters="sRGB"><feColorMatrix type="matrix" values=".30 .59 .11 0 0 .30 .59 .11 0 0 .30 .59 .11 0 0 0 0 0 1 0"/>
//  <feComponentTransfer><feFuncR type="table" tableValues=".05 .08 .11 .15 .20 .26 .33 .52 .94 1 1"/>
//  <feFuncG type="table" tableValues=".07 .11 .15 .20 .26 .33 .40 .38 .60 .90 1"/>
//  <feFuncB type="table" tableValues=".10 .15 .21 .28 .36 .44 .52 .30 .12 .52 1"/></feComponentTransfer></filter>
const BEATS = []; for (let k = 0; .03 + k * .52 < EXIT; k++) BEATS.push(.03 + k * .52);
const lastBeat = (t) => { let b = -9; for (const x of BEATS) { if (x <= t) b = x; else break; } return b; };
window.onPlace = (t) => {
  const hot = t >= TIC && t < EXIT;
  document.getElementById("plate").style.filter = hot ? "url(#th) contrast(1.08)" : "none";
  const pulse = Math.exp(-Math.max(0, t - lastBeat(t)) * 7);           // every beat: a decaying pulse
  document.getElementById("ret").style.transform = `translate(960px,540px) scale(${1 + .05 * pulse})`;
  const u = Math.max(0, Math.min(1, (t - 4.2) / 12.8)), o2 = 100 - 93 * Math.pow(u, .6);
  document.getElementById("gzN").setAttribute("transform", `rotate(${-135 + 270 * o2 / 100})`);
  document.getElementById("gzV").textContent = Math.round(o2) + "%";
};
tl.fromTo("#bloom", {opacity: 0}, {opacity: 1, duration: .12, ease: "power2.in"}, EXIT - .14);   // the camera switches off
tl.to("#bloom", {opacity: 0, duration: 1.1, ease: "power2.out"}, EXIT - .02);
```

## Adapting it to the user's project
- Content: list the real instruments of the user's world (what they carry, what beeps) and give each one a job in the story; the voice speaks through the one that talks (radio, OSD).
- Language: Hebrew OSD in fixed cells works; keep technical labels in English mono like real equipment.
- Brand: the amber UI accent and the end badge; never a floating logo.
- Different endings: the switch-off can be a door opening to daylight, a helmet coming off, a thermal image fading into colour.

## Sound
- The sample drops soft sub-thumps on key heartbeat beats (hidden `kine` elements hitting at `THUMPS`: the TIC cut, the door, "one person", the child, the exit) under the VO and music. Add warn_beep for the PASS alarm, heartbeat.mp3 under the search, and let the fire roar from the plate carry the rest.

## Pitfalls and QA checklist
- [ ] Only the plate is filtered, never the UI (apply the filter to `#plate`, not the whole root).
- [ ] The scene is dark enough that fire maps to amber-white and people to warm, not everything to white. Adjust the table values or add `contrast()` if the whole frame blows out.
- [ ] Heat blobs sit on the tracked target and disappear when it's not tracked.
- [ ] OSD lines fit on one row (count the cells).
- [ ] The exit bloom lands exactly on the cut to daylight.
- [ ] Look at frames before the TIC cut, in the search, at "one person", at the lock and after the exit; qa.py until "ship".
