# #15 HUD-HELMET · Holographic visor HUD

> A holographic head-up display lives inside a helmet visor: counter-rotating rings lock on the eyes, a tilted vitals cluster and message panels float in 3D, the HUD turns red on an alert, and an AI voice speaks with a live meter.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/hud-helmet.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/B4V_helmet_ora_voice_24s.mp4
> Runner: run_style HUD-HELMET · Example: examples/hud-helmet

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: sci-fi and gaming promos, pilots/divers/astronauts, AI-assistant products ("the suit talks to you"), tech launches that want an Iron-Man feeling without copying it, Hebrew or English.
- Avoid when: the face is small in frame or turns away (the reticle must sit on steady eyes), the shot has cuts (one take only), the story needs lots of reading (the HUD carries short system lines, not paragraphs), or the brand is calm/premium (use HUD-CLEAN #17).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#vig` | radial vignette tinted with the HUD colour (10% → 22% at the frame edge) | swaps to the alert colour (14% → 30%) while `alert` is active |
| `#scan` | 1 px scanlines every 4 px, HUD colour at 5% | fades in over 0.6 s at 0.05 s |
| `#boot` ring | a 420 px-radius circle drawn on around the eyes (stroke-dashoffset 2640 → 0) | boot only, gone by 1.75 s |
| `#ret` reticle | 3 rings (r 150 dashed 6/10, r 118 dashed 120/60/30/60 at 4 px, r 92 dotted 2/6 at 6 px) + 4 triangles at r 178–196 | follows the tracked `eyes` box centre every frame |
| `#pxL` → `#lc` vitals | 300 px heart-rate ring (60 ticks, arc r 112) + two 120 px mini gauges | tilted `rotateY(24deg)`, parallax −40 px × head turn |
| `#pxR` → `#rc` message panel | 560 px clipped-corner frame, header + typed lines | `rotateY(-24deg)`, 196 px from the right edge |
| `#warn` | red alert frame, 600 px wide at top 560 | blinks 10× |
| `#meters` | 7 vertical bars, right edge (own 118 px column) | sine-driven, never overlap the message panel |
| `#rad` radar | 230 px circle, conic sweep 140°/s, 3 blips | bottom-left |
| `#cmp` compass tape | 760 px masked tape, a label every 15°, heading from head turn | top centre |
| `#data` | 900 px hex data stream + SYNC %, bottom centre | changes every 0.1 s (seeded hash) |
| Centre messages | `#bootm`, `#ai`, `#lockm`, `#wpn`, `#go` | one at a time, each with a glitch-in |
| `#vox` | AI voice label + 26 bars driven by the voice loudness envelope | only with `voice` |

## Timing and motion
Times in seconds from the clip start (the sample is 24 s). Durations and eases are taken from `scripts/styles/helmet.py`.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| scanlines / vignette | 0.05 | 0.6 / 0.8 | linear | whole clip | — | — |
| boot ring draw | 0.15 | 1.1 | power2.inOut | — | fade 0.4 at 1.35 | linear |
| reticle | 1.1 | 0.6 (scale 1.6 → 1) | expo.out | whole clip | fades with final | — |
| compass | 1.4 (label +0.1) | glitch 0.3 | expo.out | whole clip | — | — |
| data stream / meters | 1.8 / 2.0 | glitch 0.3 | expo.out | — | at final − 0.1, 0.25 | power2.in |
| boot message | 0.5 | glitch 0.35 | expo.out | to 3.85 | 0.25 | power2.in |
| vitals | 4.1 | glitch 0.4; arcs fill 0.8 (staggered +0.4, +0.6) | expo.out / linear | to final | 0.25 | power2.in |
| radar | 5.2 | glitch 0.35 | expo.out | — | at final | — |
| message panel | 7.0 | glitch 0.35; lines type at 16 chars/s from each line's `t` | expo.out | to 10.9 | 0.25 | power2.in |
| alert | 11.0 | glitch 0.25, then opacity .45 yoyo 0.15 × 10 | expo.out / none | to 15.0 | 0.25 | power2.in |
| radar blips | contacts_at 11 | stagger 0.12; scale 1.6 yoyo 0.25 × 8 | sine.inOut | — | — | — |
| AI line | 15.2 | glitch 0.35; types at 13 chars/s from t + 0.2 | expo.out | to 17.9 | 0.25 | power2.in |
| target lock | 18.15 | glitch 0.25; % counts over `dur` 2.1 | expo.out | to 21.0 | 0.25 | power2.in |
| confirm | 21.1 | glitch 0.35; "✓" appears at ok_at 22.3 | expo.out | to 23.0 | 0.25 | power2.in |
| final word | 23.1 | glitch 0.4 | expo.out | to end | — | — |
- Glitch-in (every panel): from `opacity 0, skewX -16, x -24, clipPath inset(46% 0 46% 0)` to clean in `dur`, then 4 opacity flickers (.25/1/.55/1 over 0.16 s).
- Rings spin continuously: A +18°/s, B −34°/s, C +60°/s; ×3 speed during the lock window (lock.t − 0.15 → lock.t + dur + 0.9), and the 4 triangles converge from scale 1.35 → 0.82 over 1.8 s while spinning 90°/s.
- Heart rate follows keyframes `bpm` (t, value) with linear interpolation; the ring arc fills to bpm/140.
- Parallax: `rel = (eyes centre − face centre) / face width`; the side clusters shift `−rel × 40 px`, the compass heading = `heading + rel × 90°`.
- The signature move: the triple counter-rotating reticle locked to the tracked eyes, with the side panels tilted ±24° in 3D so the HUD reads as curved visor glass.

## Typography
- Latin and Hebrew text: **Secular One** everywhere (one face keeps the HUD coherent); digits in **JetBrains Mono** (`.num`, LTR-isolated).
- Sizes at 1920×1080: boot title 46 px, sub 26; heart value 84, label 26; message header 24, lines 32; alert title 40, sub 26; AI label 20, line 44; lock 44 / 30; confirm 40 / 32; final word 120.
- Hebrew: `language: "he"` sets `direction: rtl` on all text blocks; numbers stay in `.num` spans so "07", "140" and "98%" never flip. Keep the ⚠ and ✓ glyphs at the start of the string. No prices here; if you add one, write it as ש״ח.
- Max copy: message lines ≈ 28 characters (the panel is 560 px and wraps inside itself), AI line ≈ 26, final word ≤ 12 characters at 120 px.

## Colour and surface
- Roles: `hud` #6fe3ff (rings, strokes, glow), `text` #e6fbff, `alert` #ff4a5a, `ok` #ffb547 (confirm, amber blip). Swap all four in `colors` for a brand; keep text very light and the alert clearly warmer than the HUD.
- Glass: panels `rgba(2,14,22,.62)`; text glow `0 0 10px hud 85%` plus a ±1.5 px red/cyan chromatic split.
- Frames use a 28 px clipped corner and a 3 px HUD-colour right border.

## Layout and safe zones (1920×1080 canvas)
- Vitals cluster: left 70, top 210, 420 wide. Message panel: right 196, top 190, 560 wide. Alert: right 70, top 560, 600 wide. Meters: right 40, top 300 (118 px column reserved). Radar: left 110, bottom 70. Compass: top 40, centred. Voice meter: right 70, bottom 64, 330 wide. Centre messages: top 150 or bottom 120.
- The face must stay in the centre third; the side panels need about 22% of the width on each side.
- 9:16: not built in. Crop 16:9 → 9:16 only if the face is centred, and move the side clusters above and below the face.

## What the footage must give you
- Shoot it like this: one take, no cuts, 15–30 s · face close-up, eyes steady and centred, visor edges in frame · 22% free on both sides · locked-off with a very slow continuous push-in.
- Seedance lines (from plates.json): "FORMAT: One continuous shot, no cuts." / "CAMERA: Locked-off extreme close-up with a very slow continuous push-in over the whole shot. FORBIDDEN: cuts, shake, rotation, zoom punches." / "The face stays in the centre third; the left and right quarters show only helmet interior and soft background bokeh." / "POSITIVE LOCKS: His face stays identical to the first frame. The visor glass stays completely clean: no displays, no graphics, no text, no UI at any time. Exactly one person."
- Tracking (vtrack.py): objects `face` (forehead to chin, ear to ear), `eyes` (both eyes as one box), optionally `visor`. See examples/hud-helmet/objects.json. The gate wants ≥95% coverage.
- Matte: not needed.
- Good footage: a face lit from the front, eyes clearly visible through clean glass, a slight blink or eye movement. Bad: reflections of real UI on the visor, big head turns, a mask or sunglasses hiding the eyes.

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/my_helmet.mp4 examples/hud-helmet/objects.json tracks/my_helmet.json
python scripts/run_style.py HUD-HELMET --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip, track | the plate and its vtrack file | required |
| eyes / face | tracked object names | "eyes" / "face" |
| language | "he" (RTL) or "en" | "he" |
| colors | {hud, text, alert, ok} | #6fe3ff / #e6fbff / #ff4a5a / #ffb547 |
| system | OS tag in the data stream | "VNG-OS" |
| boot | {title, sub, ok, t, until} | t .5, until 3.85 |
| vitals | {t, hr_label, hr_unit, g1_label, g1_value, g2_label, g2_value, bpm:[[t,v],...]} | t 4.1 |
| radar | {t, label with {n}, contacts, contacts_at} | t 5.2, 3 contacts at 11 |
| compass | {t, label, heading} | t 1.4, heading 72 |
| messages | {t, until, header, lines:[{text,t}], cps} | 7.0 → 10.9, 16 cps |
| alert | {t, until, title, sub} | 11 → 15 |
| ai | {t, until, label, text, cps} | 15.2 → 17.9, 13 cps |
| lock | {t, until, title, done, dur} | 18.15 → 21, dur 2.1 |
| confirm | {t, until, question, ok, ok_at} | 21.1 → 23, ok at 22.3 |
| final | {t, text} | 23.1 |
| voice | {file, label, vol} — AI voice + live meter; other SFX duck to 60% | none |
| sfx / music / music_vol / plate_vol / name | sound design on, music bed, plate level | true / – / – / .7 (.45 with voice) |
Every block merges over the default; set a block to `false` to drop it, or move it with `t` / `until`.
A minimal spec for a generic project (a 15 s English clip, no radar):
```json
{
  "name": "diver-hud",
  "clip": "clips/diver_720p.mp4",
  "track": "tracks/diver_vtrack.json",
  "language": "en",
  "colors": {"hud": "#7df9c8"},
  "system": "ABYSS-OS",
  "radar": false,
  "boot": {"title": "DIVE SYSTEM ONLINE", "sub": "O2 SYNC", "ok": "ALL SEALS NOMINAL"},
  "messages": {"t": 5.0, "until": 8.6, "header": "INCOMING · SURFACE", "lines": [{"text": "Depth 38 m. Hold.", "t": 5.4}, {"text": "Current rising.", "t": 6.8}]},
  "alert": {"t": 9.0, "until": 11.5, "title": "⚠ LOW VISIBILITY", "sub": "RANGE 4 M"},
  "ai": false, "lock": false, "confirm": false,
  "final": {"t": 12.5, "text": "ASCEND"}
}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// tl is the paused master timeline (window.__timelines.main); boxAt(name, t) returns the tracked [x0,y0,x1,y1]
window.onPlace = (t) => {
  const e = boxAt("eyes", t), f = boxAt("face", t);
  const ex = e ? (e[0] + e[2]) / 2 : 960, ey = e ? (e[1] + e[3]) / 2 : 480;
  const rel = e && f ? (ex - (f[0] + f[2]) / 2) / (f[2] - f[0]) : 0;
  ret.style.left = ex + "px"; ret.style.top = ey + "px";
  const lock = t > LOCK_T - .15 && t < LOCK_T + 3, sp = lock ? 3 : 1;
  rA.style.transform = `rotate(${t * 18 * sp}deg)`;    // pure functions of t: seek-safe
  rB.style.transform = `rotate(${-t * 34 * sp}deg)`;
  rC.style.transform = `rotate(${t * 60 * sp}deg)`;
  pxL.style.transform = pxR.style.transform = `translateX(${-rel * 40}px)`;   // head-turn parallax
};
function glitch(sel, at, dur = .3) {
  tl.fromTo(sel, {opacity: 0, skewX: -16, x: -24, clipPath: "inset(46% 0 46% 0)"},
                 {opacity: 1, skewX: 0, x: 0, clipPath: "inset(0% 0 0% 0)", duration: dur, ease: "expo.out"}, at);
  tl.to(sel, {keyframes: [{opacity: .25, duration: .04}, {opacity: 1, duration: .04},
                          {opacity: .55, duration: .03}, {opacity: 1, duration: .05}]}, at + dur);
}
glitch("#lc", 4.1, .4); glitch("#rc", 7.0, .35);
```

## Adapting it to the user's project
- Content: rewrite each block as the story beats of the clip: boot (who/what comes online), vitals (the product's key numbers), message (the mission), alert (the conflict), AI line (the product's voice), lock and confirm (the decision), final word (the CTA or slogan). Drop blocks rather than cram.
- Language: "he" or "en"; mixed is fine inside a block, but keep digits in the data fields so they stay LTR.
- Brand: change `colors`; the whole HUD re-tints, including the vignette and the chromatic glow. `system` becomes the brand's OS tag.
- Vertical 9:16: re-place the clusters above and below the face in CSS (they're positioned absolutely), and keep the reticle.
- Longer or shorter clips: shift every block's `t`/`until`; for under 12 s keep boot, vitals, one message and the final word only.

## Sound
- Built-in cues (bundled in assets/sfx): hud_boot 0.1 (vol .7), data_chatter 0.6 (.25), chime at boot.t + 2.2 (.4), ui_whoosh at vitals (.4), scan_beeps at radar (.25), ui_pop at messages (.5), ui_tick per message line (.3), warn_beep at alert and alert + 1.2 (.75/.5), heartbeat at alert (.5), glass_ting at AI (.5), lock_tone at lock (.55), hit_confirm at lock + 2.25 (.65), charge_up at confirm (.65), hit_confirm at ok_at (.55), stinger at final − 0.05 (.7).
- With `voice`: the voice plays at full level and every other cue is scaled to 60%. Generate the voice with gemini-tts (designed voice) and time the blocks to its lines.

## Pitfalls and QA checklist
- [ ] Tracking coverage ≥95% for `eyes` and `face`; watch the vtrack `--preview` first. A lost eye box parks the reticle at 960×480.
- [ ] The message panel text wraps inside its frame and never runs under the voice meter (the meter has its own 118 px column).
- [ ] Nothing covers the eyes except the reticle rings; panels stay in the outer 22% on each side.
- [ ] Only one centre message at a time (boot / AI / lock / confirm / final never overlap: check `until` values).
- [ ] Hebrew: digits in `.num` read correctly ("07", not "70"); the ⚠/✓ sit at the reading start.
- [ ] The compass tape clips inside its mask (the check allows this overlap on purpose).
- [ ] Look at frames at the longest message line, the alert, and the lock; then run qa.py until "ship".
