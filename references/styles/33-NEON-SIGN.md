# #33 NEON-SIGN · Neon sign on the wall

> Neon tubes mounted on the scene's walls in perspective: a stuttering flicker-on, a coloured glow spilling onto the plate, a soft reflection in the floor.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/neon-sign.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_NEON-SIGN.mp4
> Runner: run_style NEON-SIGN · Example: examples/neon-sign

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: night fashion, bars and restaurants, music and nightlife, streetwear, urban food spots, any "the sign is the brand" moment.
- Avoid when: daylight footage (neon needs darkness to glow); no blank wall or surface to mount a sign on; busy lettered walls (real signs fight the fake ones); anything needing lots of copy.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` .45 |
| Spill | a 1300×900 px radial glow in the first line's colour, `screen` blend | opacity = level × `spill` (.35) |
| Sign `.sg` | 1+ lines of tubes, in a 900 px perspective, turned onto a wall | `rotateY(±angle)` from the wall's edge |
| Outline tube | hollow letters: a white-hot stroke `max(3, size/34)` px with 4 drop-shadow glows (2, 8, 22, 48 px) in the tube colour | display weight by default |
| Solid tube | filled white-hot letters with 4 glows (2, 8, 20, 42 px) | body weight by default |
| Reflection `.rf` | the same sign mirrored (scaleY −1) around the floor line, blurred 4 px, masked to fade, `screen` | opacity = level × `reflect` (.38) |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Sign strike | `t` (default 1 + 2 × sign index) | .9 s stutter (steps below) | stepped | on, humming | cut at `until` | none |
| Hum | after .9 s | per frame | – | brightness .93–1.0 by hash | – | – |
| Buzz dip | random frames (hash > .965) | one frame | – | drops to .35 | – | – |
- Strike steps (seconds from `t` → brightness): 0–.08 → 1, .08–.2 → 0, .2–.26 → .7, .26–.44 → .05, .44–.5 → 1, .5–.58 → .2, .58–.9 → 1. Each step is multiplied by .85–1 per frame.
- Stagger: signs light in turn (their `t`); in the sample, 0.8 s and 4.6 s.
- The signature move: **the classic neon strike**, on-off-half-off-on in the first .9 s with a tick sound on the first and the fifth step, then a steady hum with a rare buzz. The spill and the floor reflection flicker in lockstep, which is what makes the sign feel physically there.

## Typography
- Latin: Tilt Neon 400 (a true tube face) for both roles. Display lines default 150 px, body lines 70 px.
- Hebrew: default pair `karantina-suez`: **Karantina 700** for the big outline tube and **Suez One** for the solid accent line. For a softer sign, `pair: secular`. Prices as ש״ח (not "$" in Hebrew lines).
- Maximum copy: 2 lines per sign, about 10–12 characters for the display line and 22 for the accent line.

## Colour and surface
- Each line has its own `color` (glow). Sample: #ff3da8 pink with a #3de0ff cyan accent, and #ff8a1a orange with #ffe36b yellow. The core is always near-white #fff6fb; the colour lives in the glow.
- Brand swap: use the brand colour for the glow; pair it with one contrasting accent line. Neon reads best in saturated pink, cyan, orange, lime and violet.

## Layout and safe zones (1920×1080 canvas)
- `x`, `y`: the sign's anchor (default 960, 420); `align` which edge sits on it.
- `wall`: "left" (turned right-side-back from its left edge) or "right" (mirror) or "none" (flat, facing camera); `angle` 34° default (55° in the sample for a corridor).
- `floor`: the y where the wall meets the floor (default 650). The reflection is drawn at `2 × floor − y`.
- `vanishing`: the plate's vanishing point (default [960, 540]; sample [960, 470]). Signs are projected towards it, so match it to the footage.
- Safe zone: keep the whole sign inside 5% margins after rotation; wall signs start ~150 px from the edge.

## What the footage must give you
- Shoot it like this: one take, no cuts · symmetrical corridor or street, subject in the centre third, blank walls left and right · 25% free on both sides.
- Tracking: none (the camera must be locked or push very slowly, because the signs are placed, not tracked).
- Matte: not needed.
- Good: night, bare evenly lit walls, a wet or glossy floor, vanishing point near the centre. Bad: daylight, real signage or screens on the walls, handheld or panning camera (the sign would slide).

## Build it
### A. With the kit
```bash
python scripts/run_style.py NEON-SIGN --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| signs | list of signs (keys below) | required |
| signs[].lines | `[{"text","tube","weight","size","color"}]` | – |
| lines[].tube | "outline" or "solid" | outline for display, solid for body |
| lines[].weight | "display" or "body" | display |
| lines[].size | px | 150 display / 70 body |
| lines[].color | glow colour | #ff3da8 |
| signs[].x, y, align | anchor and edge | 960, 420, center |
| signs[].wall, angle | "left" / "right" / "none"; degrees | none, 34 |
| signs[].t, until | on / off (s) | 1 + 2 × index, never |
| signs[].floor, reflect | mirror line y; reflection opacity (0 = none) | 650, .38 |
| signs[].spill | per-sign spill override | spec `spill` |
| spill | spill strength | .35 |
| vanishing | the plate's vanishing point [x, y] | [960, 540] |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "karantina-suez" |
| fonts | override faces | Tilt Neon 400 |
| seed | buzz seed | 5 |
| sfx | tick at strike and at +.44 s | true |
| music, music_vol, plate_vol, name, track | optional | –, .55, .45, style id, – |
```json
{
 "name": "my-neon", "clip": "clips/my_night_alley.mp4", "vanishing": [960, 500],
 "signs": [{"lines": [{"text": "OPEN LATE", "size": 140, "color": "#3de0ff"},
                      {"text": "RAMEN · SINCE 1998", "weight": "body", "size": 56, "color": "#ff3da8"}],
            "x": 180, "y": 600, "align": "left", "wall": "left", "angle": 50, "t": 1.0, "floor": 780, "reflect": .7}]
}
```
### B. The core move (per frame, from onPlace)
```js
// deterministic flicker: a pure function of t (hash1 from JS_UTIL), never Math.random
function level(s, t) {
  const d = t - s.t; if (d < 0 || (s.until != null && t >= s.until)) return 0;
  const fr = Math.floor(t * 24);
  if (d < .9) for (const [a, b, v] of [[0,.08,1],[.08,.2,0],[.2,.26,.7],[.26,.44,.05],[.44,.5,1],[.5,.58,.2],[.58,.9,1]])
    if (d >= a && d < b) return v * (.85 + .15 * hash1(fr + s.i * 7));
  if (hash1(fr * 1.7 + s.i * 31 + SEED) > .965) return .35;      // rare buzz
  return .93 + .07 * hash1(fr + s.i * 3);                          // hum
}
window.onPlace = t => NE.forEach(s => { const v = level(s, t);
  s.pos.style.opacity = v; s.rf.style.opacity = v * s.reflect; s.sp.style.opacity = v * s.spill; });
// CSS: .sg { transform: translate(-50%,-50%) rotateY(55deg); transform-origin: 0 50% }  inside  .pp { perspective: 900px }
// glow: filter: drop-shadow(0 0 2px C) drop-shadow(0 0 8px C) drop-shadow(0 0 22px C) drop-shadow(0 0 48px C)
```

## Adapting it to the user's project
- Content: the display line is the mood ("OPEN LATE", "חורף ברחוב"), the accent line is the fact (name, price, date).
- Language: Hebrew → Karantina 700 tube + Suez One accent; the sign mirrors correctly on a right wall.
- Brand: glow colours from the brand; keep the core white-hot.
- Vertical 9:16: one sign per frame, flat (`wall: none`) above the subject.
- Longer clips: light signs one after another every 3–4 s; use `until` to switch one off before the next strikes.

## Sound
- `lock_tick` at .5 on the strike and at .35 at +.44 s (the second "on"). A low electrical hum from the music bed works too; music at .55.

## Pitfalls and QA checklist
- [ ] `vanishing` matches the footage's real vanishing point, or the wall signs look pasted on.
- [ ] `floor` sits exactly on the wall/floor line; a wrong value floats the reflection.
- [ ] The camera doesn't move sideways (a placed sign slides against the wall).
- [ ] Hebrew prices read "340 ש״ח", not "340$" (the shipped example still shows "340$").
- [ ] The strike isn't too frequent; one sign every few seconds.
