# #17 HUD-CLEAN · Quiet visor HUD

> A calm, flat visor HUD: a heading tape across the top, a thin vitals column on one side, a message panel on the other, one red alert panel that blinks, small brackets on the eyes, and a single bold final word. No rings, no spinning, no voice meter.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/hud-clean.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/B4_helmet_hebrew_24s.mp4
> Runner: reference recipe (`references/recipes/legacy_shots.py` → `B4` Hebrew 24 s, `B2` English 6 s); closest runnable: run_style HUD-HELMET · Example: examples/hud-helmet

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: documentary-feeling sci-fi, pilots, divers, climbers, firefighters, "day in the life" of an operator; anywhere HUD-HELMET (#15) would feel too loud.
- Avoid when: the brief wants spectacle (use #15), the face is small or turning, or the shot has cuts.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#visor` | a container sized to the tracked `visor` box (pad −30 px) | everything below is positioned in % of the visor, so it rides the helmet |
| `#compass` + `#needle` | 40% of the visor width, top 2.5–5%; tape labels every 15° (90 px apart), masked 20%/80% at the edges; an 18 px amber needle under it | heading = 72° + head turn × 90° |
| `#vit` / `#left` | vitals column at left 3%, top 22–24%, width 21–23% | rows: heart, O₂, suit, heading |
| `#msg` / `#right` | message panel at right 3%, top 22%, width 31% | 4 px accent border on the reading edge |
| `#warn` | red-bordered panel at right 3–4%, top 60% | the only saturated red in the frame |
| `#eyebrk` | 4-corner brackets on the tracked `eyes` (18 px corners, 2 px) | turns red during alert and lock |
| centre panels | boot (top 9%), AI line (bottom 9%), lock bar (top 9%, 420 px), confirm (bottom 9%), final word (top 40%, 96 px) | one at a time |

## Timing and motion
From `legacy_shots.py` `B4` (24 s, Hebrew). `B2` compresses the same grammar into 6 s.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| visor layer | 0.1 | 0.3 (fade) | default | whole clip | — | — |
| compass | 0.3 | 0.5 (y −12 → 0) | power3.out | whole clip | — | — |
| needle | 0.5 | 0.3 | default | — | — | — |
| boot panel | 0.4 | 0.5 (scale 1.15 → 1) | expo.out | to 3.9 | 0.4 (y −10) | power2.in |
| eye brackets | 1.2 | 0.4 (scale 1.4 → 1, to .9 opacity) | default | to 23.0 | 0.35 | default |
| vitals column | 4.1 | 0.55 (x −40 → 0) | expo.out | to 23.0 | 0.35 | default |
| vitals rows | 4.3, stagger 0.15 | 0.3 (y 10 → 0) | default | — | — | — |
| message panel | 7.0 | 0.55 (x 40 → 0 + clip wipe from the right) | expo.out | lines type at 16 chars/s | 0.3 at 10.9 | default |
| alert | 11.0 | 0.3 (scale 1.15 → 1) | power4.out | blinks to .4 yoyo 0.2 × 8 from 11.4 | 0.4 at 15.0 | default |
| AI line | 15.2 | 0.5 (y 16 → 0) | power3.out | types at 13 chars/s from 15.4 | 0.4 at 17.9 | default |
| lock bar | 18.2 | 0.3 (scale 1.2 → 1) | power4.out | bar fills over 2.1 s from 18.3 | 0.35 at 21.0 | default |
| confirm | 21.1 | 0.45 (y 16 → 0) | power3.out | "✓" at 22.3 | 0.35 at 23.0 | default |
| final word | 23.1 | 0.5 (scale 1.3 → 1) | expo.out | to end | — | — |
- Heart rate: 72 until 11 s, up to 118 by 15 s, down to 94 by 18 s, holds, then 102 by 23 s (linear segments).
- The signature move: restraint. Every element slides or fades in once, flat (no 3D tilt except B2's ±14° side panels), and only the alert blinks. The eye brackets turning red during the alert are the whole drama.

## Typography
- Hebrew labels and lines: **Secular One** (it replaces the Assistant used in the original B4 render; the kit remaps it automatically). Digits: **JetBrains Mono** in LTR-isolated `.num` spans.
- Sizes at 1920×1080: labels 22 px/600 muted; values 44 px/700 (units 22 px); message header 22/700, lines 30/600; alert title 36/800, sub 26; AI 40/700; lock 36/800; confirm 38/700; final word 96/800.
- English (B2): labels 17 px mono with letter-spacing .16em, values 46 px.
- Max copy: message lines ≈ 26 characters (the panel is 31% of the visor), alert sub ≈ 30.

## Colour and surface
- Roles (the "B palette"): accent #ffb547 (amber), fg #fff4e2, mute #d9c3a0, warn #ff5046; panels `rgba(12,8,4,.8)` with 6 px radius; alert background `rgba(40,6,4,.85)` with a 2 px warn border.
- One accent colour only. For a brand, change the accent and keep the warn red.

## Layout and safe zones (1920×1080 canvas)
- All positions are % of the tracked visor box, so the layout survives a slow push-in. Keep the face in the centre third; side panels use the outer ~25% on each side.
- Top 9% and bottom 9% of the visor host the centre panels; never place two at once.

## What the footage must give you
- Shoot it like this: one take, no cuts, 6–30 s · face close-up, eyes steady · 22% free on both sides · locked-off with a very slight slow push-in.
- Seedance lines: "FORMAT: One continuous shot, no cuts." / "CAMERA: Locked-off with a very slight slow push-in. FORBIDDEN: shake, rotation, cuts." / "POSITIVE LOCKS: The visor glass stays completely clean: no displays, no graphics, no text, no UI at any time. His face stays identical to the first frame."
- Tracking (vtrack.py): `visor` (the whole visor opening), `face`, `eyes` (examples/hud-helmet/objects.json has all three). Gate: ≥95% coverage.
- Matte: not needed.

## Build it
### A. With the kit
The closest runnable route is HUD-HELMET (#15) with the loud blocks switched off:
```bash
python scripts/run_style.py HUD-HELMET --spec my_clean_spec.json --render
```
```json
{
  "name": "clean-hud",
  "clip": "clips/pilot_720p.mp4",
  "track": "tracks/pilot_vtrack.json",
  "language": "he",
  "colors": {"hud": "#ffb547", "text": "#fff4e2", "alert": "#ff5046", "ok": "#ffd28a"},
  "radar": false, "ai": false, "lock": false, "confirm": false,
  "vitals": {"t": 4.1},
  "messages": {"t": 7.0, "until": 10.9, "header": "הודעה נכנסת · מגדל", "lines": [{"text": "מסלול 12 פנוי.", "t": 7.4}, {"text": "רוח צד 14 קשר.", "t": 8.7}]},
  "alert": {"t": 11.0, "until": 14.0, "title": "⚠ רוח חזקה", "sub": "משב 32 קשר"},
  "final": {"t": 15.0, "text": "נחיתה"}
}
```
Honest limitation: helmet.py always draws the boot ring and the triple ring reticle on the eyes (they aren't spec blocks), and its vitals are a ring gauge, not the flat column. For the true clean look, build from the `B4` recipe (B below).
Keys you'll set in the recipe: the visor/face/eyes track names, the texts of boot/vitals/message/alert/AI/lock/confirm/final, each block's in/out time, the heart-rate curve, the accent colour.
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// the visor container rides the tracked visor box (kit: <div id="visor" data-box="visor" data-pad="-30">)
const tape = document.getElementById("tape");
let h = ""; for (let d = 0; d < 720; d += 15) h += `<span>${String(d % 360).padStart(3, "0")}</span>`; tape.innerHTML = h;
window.onPlace = (t) => {
  const e = boxAt("eyes", t), f = boxAt("face", t);
  const rel = e && f ? (((e[0] + e[2]) / 2 - (f[0] + f[2]) / 2) / (f[2] - f[0])) : 0;
  const hdg = 72 + rel * 90;                                   // heading follows the head turn
  tape.style.transform = `translateX(${-(hdg / 15) * 90 + 150}px)`;
  const bpm = t < 11 ? 72 : t < 15 ? 72 + (t - 11) / 4 * 46 : 118;
  document.getElementById("bpm").textContent = Math.round(bpm);
  document.getElementById("eyebrk").classList.toggle("red", (t > 11 && t < 15) || (t > 18 && t < 21));
};
tl.fromTo("#vit", {opacity: 0, x: -40}, {opacity: 1, x: 0, duration: .55, ease: "expo.out"}, 4.1);
tl.fromTo("#vit .row", {opacity: 0, y: 10}, {opacity: 1, y: 0, duration: .3, stagger: .15}, 4.3);
tl.fromTo("#msg", {opacity: 0, x: 40, clipPath: "inset(0 0 0 100%)"}, {opacity: 1, x: 0, clipPath: "inset(0 0 0 0%)", duration: .55, ease: "expo.out"}, 7.0);
tl.fromTo("#warn", {opacity: 0, scale: 1.15}, {opacity: 1, scale: 1, duration: .3, ease: "power4.out"}, 11.0);
tl.to("#warn", {opacity: .4, duration: .2, repeat: 7, yoyo: true, ease: "none"}, 11.4);
```

## Adapting it to the user's project
- Content: 3–4 vitals that matter to the subject (a diver: depth, O₂, time; a climber: altitude, heart, temperature), one message, one alert, one final word. Fewer is better here.
- Language: Hebrew panels are RTL (the reading edge carries the accent border); English uses letter-spaced mono labels.
- Brand: one accent colour; everything else is warm white and dark glass.
- Short clips (6 s, like B2): compass + both side panels at 0.2–0.45, alert at 2.05, final word at 4.1.
- Vertical 9:16: stack the vitals under the face and the message above it.

## Sound
- B4 cues: hud_boot 0.1 (.7), data_chatter 0.6 (.3), chime 2.7 (.45), ui_whoosh 4.05 (.45), ui_pop 7.0 (.6), ui_tick at 7.4/8.7/10.3 (.35), warn_beep 11.0 and 12.2 (.8/.55), heartbeat 11.0 (.55), glass_ting 15.3 (.55), lock_tone 18.2 (.6), hit_confirm 20.4 (.7), charge_up 21.1 (.7), hit_confirm 22.3 (.6), stinger 23.05 (.8). Plate at .7.

## Pitfalls and QA checklist
- [ ] The visor box is tracked tightly; a loose box pushes panels off the glass.
- [ ] Only the alert is red; nothing else competes with it.
- [ ] Digits in `.num` spans (Hebrew): "07", "140", "072°" read correctly.
- [ ] Panels never cover the eyes; brackets are the only thing on the face.
- [ ] If you used the HUD-HELMET route, accept or explain the rings; if the brief says "no rings", build from B4.
- [ ] Look at frames at the message, the alert and the final word; qa.py until "ship".
