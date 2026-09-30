# #16 SCIFI-TARGETING · First-person targeting HUD

> A first-person targeting system: corner ticks and a centre reticle boot up, bracket boxes with ID tags lock onto each tracked target while their ranges count down, a HOSTILE LOCK banner, a FIRE cue, dashed projectile arcs fly from the weapon to the targets, hit flashes, then TARGETS NEUTRALIZED.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/scifi-targeting.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/B3_final.mp4
> Runner: run_style SCIFI-TARGETING · Example: examples/scifi-targeting

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: game trailers, sci-fi shorts, drone/defence/robotics tech, sports "target acquired" moments (a goalkeeper, a skier's gate), any POV shot with 2–3 clear subjects.
- Avoid when: the shot is third-person, subjects overlap or leave frame early, the tone is family/lifestyle, or there are more than 3–4 targets (the tags crowd).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `.tick` ×4 | 44×44 px corner brackets 48 px in from each corner | amber at 70% |
| `#ret` | centre reticle: 120 px circle + 180 px split cross-hairs | fixed at 960×540 |
| `#arcs` | one dashed quadratic path per locked target (stroke 4, dash 14/10) | drawn per frame from the `launcher` box to the target |
| `.tgt .brk` | 4-corner bracket box around each target (`data-box`, 10 px pad) | turns red while locked |
| `.tt.panel` | ID tag: label 26 px/800 + sub line 17 px mono with a live `{range}` | follows the target at `anchor` + dx/dy |
| `.hit` | two 4×80 px white crossed bars on the target centre | flash at impact |
| `#lockmsg` | red-bordered banner, 30 px mono, bottom 190 | "HOSTILE LOCK · {n} TARGETS" |
| `#fire` | solid amber block, 44 px, letter-spacing .3em, bottom 180 | the FIRE cue |
| `#banner` | 88 px title between 3 px rules + optional Hebrew 44 px line + 20 px detail | final |

## Timing and motion
Times from the clip start (the sample is 8 s). From `scripts/styles/targeting.py`.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| corner ticks | 0.05, stagger 0.05 | 0.4 (scale 1.5 → 1) | default | whole clip | — | — |
| reticle | 0.2 | 0.5 (scale 2 → 1, rotate −45 → 0) | expo.out | to impact + 0.2 | 0.3 | default |
| target brackets | each target's `t` (default 0.5 + 0.4 × i) | 0.35 (scale 1.5 → 1) | power3.out | — | locked: impact + 0.2; not locked: banner − 0.1 | 0.3 |
| ID tag | `t` + 0.15 | 0.35 (y 10 → 0) | default | — | with its bracket | — |
| range readout | counts `range[0] → range[1]` linearly from 0 to fire.t | per frame | linear | — | switches to `after` text at impact + 0.4 | — |
| lock banner | lock.t 2.6 | 0.25 (scale 1.2 → 1) | power4.out | to fire − 0.1 | 0.15 | default |
| lock state | brackets and tags turn red | per frame | — | lock.t → impact | — | — |
| FIRE | fire.t 3.85 − 0.05 | 0.15 (scale 1.4 → 1) | power4.out | to impact | 0.3 | default |
| arcs | draw from fire.t to impact (default fire + 0.8) | per frame, 24 segments | linear | to impact + 0.5 | cleared | — |
| hit flash | impact | 0.18 (scaleY .2 → 1.3) | power4.out | — | 0.4 at impact + 0.35 | default |
| banner | banner.t (default impact + 1.5) | 0.5 (scaleX 1.3 → 1) | expo.out | to end | — | — |
| banner Hebrew / detail | + 0.25 / + 0.4 | 0.4 | default | — | — | — |
- The signature move: the projectile arcs. Each is a quadratic Bézier from the launcher's top-centre to the target centre with its control point 260 px above the higher end, drawn progressively (`u` from 0 to 1) so it reads as a guided launch.
- Sync the FIRE and impact times to the plate's own action (the sample measured the rocket flash from the plate's luminance: fire 3.85, impact 4.65).

## Typography
- Latin: tags in **Secular One** 26 px/800; everything numeric and system-like in **JetBrains Mono** (sub lines 17 px, letter-spacing .08em; lock 30 px .14em; FIRE 44 px .3em). Banner 88 px/800, letter-spacing .08em.
- Hebrew: the optional `banner.sub` line is set RTL in Secular One 44 px/700 (e.g. "המטרות נוטרלו"). Tags can be Hebrew too; keep `{range}` and units in the mono sub line so digits stay LTR.
- Max copy: tag label ≈ 18 characters, sub line ≈ 28, banner title ≈ 22 at 88 px.

## Colour and surface
- Roles: `hud` #ffb547 (amber: ticks, brackets, arcs, FIRE), `fg` #fff4e2, `mute` #d9c3a0 (sub lines, detail), `alert` #ff5046 (lock state, lock banner). Panel `rgba(12,8,4,.78)`.
- To rebrand, keep a single warm or cold HUD hue with a clearly different alert red; amber-on-dark reads best over fire and smoke.

## Layout and safe zones (1920×1080 canvas)
- Tags sit at the target's `anchor` (r, tr, c…) + dx 18, dy −20 by default; nudge per target with `dx`/`dy` so no tag covers another target.
- Lock/FIRE banners bottom-centre (190 / 180 px from the bottom); the final banner at top 420.
- Leave the right quarter free for tags (the contract asks for 25% free on the right).
- 9:16: not built in; stack the targets vertically and move banners to the top third.

## What the footage must give you
- Shoot it like this: one take, no cuts, 6–12 s · POV; targets spread across the middle, weapon in a lower corner · 25% free on the right · first-person, subtle natural head movement; one short blast shake allowed.
- Seedance lines: "FORMAT: One continuous shot, no cuts." / "CAMERA: First-person, subtle natural head movement, one short blast shake at the impact. FORBIDDEN: whip-pans, cuts." / "POSITIVE LOCKS: Exactly two robots and one drone. Exactly two rockets, fired once. No text, no reticles, no UI, no logos at any time." (Swap in your own counted targets and weapon.)
- Tracking (vtrack.py): one object per target (describe "not visible once destroyed" so boxes end cleanly) + the `launcher`. See examples/scifi-targeting/objects.json. Gate: ≥80% coverage.
- Matte: not needed.
- Good footage: counted, clearly separated targets, a visible launch moment, a blast. Bad: targets that pass behind each other, a shaky handheld that loses the boxes, AI-generated reticles already in the plate.

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/my_pov.mp4 my_objects.json tracks/my_pov.json
python scripts/run_style.py SCIFI-TARGETING --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip, track | plate + vtrack file | required |
| targets | [{obj, label, sub with {range}, range [from,to], lock, after, t, anchor, dx, dy}] | required; lock true, anchor "r", dx 18, dy −20, t .5 + .4·i |
| launcher | tracked object the arcs start from | none (no arcs) |
| lock | {t, text with {n}} | 2.6, "HOSTILE LOCK · {n} TARGETS" |
| fire | {t, text} | 3.85, "FIRE" |
| impact | seconds | fire.t + 0.8 |
| banner | {t, title, sub (Hebrew line), detail} | impact + 1.5, "TARGETS NEUTRALIZED" |
| colors | {hud, fg, mute, alert} | #ffb547 / #fff4e2 / #d9c3a0 / #ff5046 |
| sfx / music / music_vol / plate_vol / name | sound + levels | true / – / – / .85 |
A minimal spec for a generic project (a drone intercept, two targets, Hebrew banner line):
```json
{
  "name": "intercept",
  "clip": "clips/intercept_720p.mp4",
  "track": "tracks/intercept_vtrack.json",
  "launcher": "turret",
  "targets": [
    {"obj": "drone_a", "label": "UAV-01", "sub": "RANGE {range} m", "range": [420, 180], "t": 0.6},
    {"obj": "drone_b", "label": "UAV-02", "sub": "RANGE {range} m", "range": [510, 240], "t": 1.0, "anchor": "tr"}
  ],
  "lock": {"t": 2.4},
  "fire": {"t": 3.2, "text": "ENGAGE"},
  "impact": 4.0,
  "banner": {"t": 5.4, "title": "AIRSPACE CLEAR", "sub": "המרחב האווירי נקי"}
}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// projectile arc from the launcher to a target, drawn progressively between FIRE and IMPACT (seek-safe)
function arc(el, a, b, u) {
  if (!a || !b || u <= 0) { el.setAttribute("d", ""); return; }
  const x0 = (a[0] + a[2]) / 2, y0 = a[1] + 20, x1 = (b[0] + b[2]) / 2, y1 = (b[1] + b[3]) / 2;
  const cx = (x0 + x1) / 2, cy = Math.min(y0, y1) - 260;
  const P = (s) => [(1-s)*(1-s)*x0 + 2*(1-s)*s*cx + s*s*x1, (1-s)*(1-s)*y0 + 2*(1-s)*s*cy + s*s*y1];
  let d = `M${x0},${y0}`; for (let k = 1; k <= 24; k++) { const p = P(u * k / 24); d += ` L${p[0]},${p[1]}`; }
  el.setAttribute("d", d);
}
window.onPlace = (t) => {
  const u = t < FIRE ? 0 : t < IMPACT ? (t - FIRE) / (IMPACT - FIRE) : (t < IMPACT + .5 ? 1 : 0);
  arc(document.getElementById("arc0"), boxAt("launcher", t), boxAt("heavy", Math.min(t, IMPACT)), u);
  document.getElementById("r0").textContent = Math.round(140 + (96 - 140) * Math.min(1, t / FIRE));
};
tl.fromTo("#lockmsg", {opacity: 0, scale: 1.2}, {opacity: 1, scale: 1, duration: .25, ease: "power4.out"}, LOCK);
tl.fromTo(".hit i", {opacity: 0, scaleY: .2}, {opacity: 1, scaleY: 1.3, duration: .18, ease: "power4.out"}, IMPACT);
```

## Adapting it to the user's project
- Content: labels are the target's identity (a code + a class), sub lines carry a live measurement (range, speed, altitude); `after` replaces the sub line after impact ("SIGNAL LOST", "SAVED").
- Language: English system language reads most "military"; put the human line in Hebrew in `banner.sub`.
- Brand: change `colors`; cold cyan for tech/defence, amber for fire/war, lime for sport.
- Non-violent uses: sport ("TARGET: TOP CORNER" → "GOAL"), wildlife camera ("SUBJECT LOCKED" → "CAPTURED"), product demos (targets = product features, launcher = a hand pointing).
- Longer clips: add targets with later `t`; move lock/fire/impact to the plate's real action.

## Sound
- Cues (assets/sfx): hud_boot 0.05 (vol .5), scan_beeps 0.5 (.5), lock_tone at lock.t (.7), launch at fire − 0.05 (.5), hit_confirm at impact + 0.05 (.8), stinger at banner − 0.05 (.8). Keep the plate's own explosion audio (plate_vol .85).

## Pitfalls and QA checklist
- [ ] Every target's box disappears when the target is destroyed or hidden (describe that in objects.json); otherwise brackets hang in the smoke.
- [ ] fire/impact match the plate's action to the frame (scrub the plate; a late flash looks fake).
- [ ] Tags never cover another target or each other: adjust `anchor`, `dx`, `dy`.
- [ ] Arcs start from the launcher, not from mid-air: check the launcher box exists at fire.t.
- [ ] The banner doesn't sit on top of the burning targets: move `banner.t` or its top position.
- [ ] Look at frames at lock, fire, impact and banner; run qa.py until "ship".
