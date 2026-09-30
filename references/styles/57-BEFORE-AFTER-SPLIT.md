# #57 BEFORE-AFTER-SPLIT · Comparison wipe

> Two takes of the same camera move are stacked; a white divider with a round handle sweeps across revealing the AFTER, swings back, and settles on a split (or on the full after). Big label chips name each side, and a stat bar lands at the end.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/before-after-split.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_BEFORE-AFTER-SPLIT.mp4
> Runner: run_style BEFORE-AFTER-SPLIT · Example: examples/before-after-split/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: renovations and interior design, retouching/editing tools, skincare/fitness results, cleaning products, product upgrades (v1 vs v2), AI restyling apps, real estate staging.
- Avoid when: you don't have two matching takes (same framing and camera move), or the change is too small to see at a glance.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| the plate (`clip`) | the BEFORE video | bottom |
| `#matte` | the AFTER video (the kit's second video slot), masked with `clip-path: inset()` | converted to webm automatically |
| `#div .ln` | 4 px white divider with shadow | follows the reveal position |
| `#div .hd` | 88 px white handle with two arrow triangles, at y 496 | pops in, bumps at each move |
| `.chip` | label chips top 80 px, 80 px from the sides: BEFORE (dark glass) / AFTER (accent #ffd23f, dark text), 84 px display | |
| `#stat` | bottom bar (pill, dark glass, 36 px body, accent dot), centred, bottom 74 px | |

## Timing and motion
The reveal is a list of keyframes `moves` = [[time, position], …]; position 0..1 of the frame width measured from the AFTER side. Between keyframes it eases with a cubic in-out; mask, divider and handle are recomputed every frame from video time.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| BEFORE chip (fade, y −20→0) | .3 | .60 | back.out(1.8) | — | fades (y −12) at last move −.4 if the last position ≥ .99 | power2.in |
| AFTER chip (fade, y −20→0, scale .9→1) | moves[1].time − 1.2 | .60 | back.out(2.2) | — | — | — |
| handle (scale 0→1) | moves[0].time + .1 | .50 | back.out(2.4) | — | — | — |
| handle bump at each move (scale 1.15→1) | move time − .05 | .50 | power2.out | — | — | — |
| divider position | per `moves` | between keyframes | cubic in-out | — | hidden at 0 and 1 | — |
| stat bar (fade, y 30→0) | stat_t (6.6) | .70 | power3.out | — | — | — |
- Default moves: [[0.9, 0], [2.9, .78], [4.6, .3], [6.0, .5]]: reveal most, swing back, settle in the middle. Sample: [[.9,0],[2.8,.8],[4.3,.28],[5.6,.5],[7.3,1.0]].
- The signature move: the handle-led sweep that overshoots, comes back, and settles: it mimics a person dragging a comparison slider.

## Typography
- Latin: Oswald 700 chips (84 px, +.04em), Manrope 500 stat (36 px).
- Hebrew: `pair: "karantina"` (default) = Karantina 700 chips "לפני" / "אחרי", Secular One stat. By default the AFTER reveals from the reading-start side (right in Hebrew, left in English).
- Currency: Suez One / Secular One draw ₪ as a stylised "שח": write "186,000 ש״ח". (The builder's docstring example still shows "₪"; don't copy it.)
- Maximum copy: chips ≤ 8 characters, stat ≈ 50 characters.

## Colour and surface
- `colors.accent` #ffd23f (AFTER chip, stat dot); BEFORE chip dark glass rgba(10,10,12,.62); stat bar rgba(10,10,12,.72).
- Brand swap: accent = brand colour (keep it light enough for dark text on the AFTER chip).

## Layout and safe zones (1920×1080 canvas)
- Chips at the top corners (80 px in, 80 px down): BEFORE on the before side, AFTER on the after side. Handle vertically centred (top 496). Stat bar centred, bottom 74.
- Industry convention: BEFORE on the left and AFTER on the right in LTR markets (the eye reads the change); RTL mirrors it.
- 9:16: works as is on a vertical canvas (vertical divider); move chips below the platform UI.

## What the footage must give you
- Two clips with the SAME framing and camera move: the before (`clip`) and the after (`after`).
- How to make the pair with AI: 1) one start frame of the AFTER state (text_to_image); 2) the BEFORE version of that exact frame (image_to_image: "same room, same camera, dated furniture…"); 3) image_to_video on BOTH with one identical camera-move prompt (slow dolly, 10 s).
- Two generated takes drift apart after ~6 s: do the split moves early and end on 1.0 (full AFTER) if the seam starts to show (the sample does exactly this at 7.3 s).
- Real footage: a locked-off or motion-controlled camera, or a tripod mark for both shoots.
- Tracking: none. Matte: the AFTER clip is used as the second layer (converted to webm by the builder).

## Build it
### A. With the kit
```bash
python scripts/run_style.py BEFORE-AFTER-SPLIT --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the BEFORE video | required |
| after | the AFTER video (same framing, same length) | required |
| labels | {before, after} | BEFORE/AFTER, לפני/אחרי |
| after_side | "start" (reading-start side) or "end" | "start" |
| moves | [[t, pos 0..1], …] divider keyframes | [[0.9,0],[2.9,.78],[4.6,.3],[6.0,.5]] |
| stat / stat_t | bottom bar text / time | none / 6.6 |
| language / pair | he/en; Hebrew pair | en / "karantina" |
| fonts | override | Oswald 700 / Manrope 500 |
| colors | {accent} | #ffd23f |
| sfx | pop, whoosh per move, chime with the stat | true |
| plate_vol, music, music_vol, name | — | .6, none, .5 |
```json
{
 "clip": "clips/kitchen_before.mp4", "after": "clips/kitchen_after.mp4",
 "moves": [[0.9, 0], [2.8, 0.8], [4.3, 0.28], [5.6, 0.5], [7.3, 1.0]],
 "stat": "Full renovation · 6 weeks · $42,000", "stat_t": 7.5
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const kf = [[0.9, 0], [2.8, .8], [4.3, .28], [5.6, .5], [7.3, 1]], W = 1920, fromLeft = true;
const ease = (u) => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const posAt = (t) => {
  if (t <= kf[0][0]) return kf[0][1];
  for (let i = 1; i < kf.length; i++) if (t <= kf[i][0]) { const [a, p] = kf[i - 1], [b, q] = kf[i]; return p + (q - p) * ease((t - a) / (b - a)); }
  return kf[kf.length - 1][1];
};
window.onPlace = (t) => {                          // mask + divider = f(time): seek-safe
  const p = posAt(t), x = fromLeft ? W * p : W * (1 - p);
  document.getElementById("matte").style.clipPath = fromLeft ? `inset(0 ${W - x}px 0 0)` : `inset(0 0 0 ${x}px)`;
  const d = document.getElementById("div"); d.style.transform = `translateX(${x}px)`; d.style.opacity = p > .002 && p < .998 ? 1 : 0;
};
tl.fromTo("#div .hd", {scale: 0}, {scale: 1, duration: .5, ease: "back.out(2.4)"}, kf[0][0] + .1);
for (let i = 1; i < kf.length; i++) tl.fromTo("#div .hd", {scale: 1.15}, {scale: 1, duration: .5, ease: "power2.out"}, kf[i][0] - .05);
```

## Adapting it to the user's project
- Content: the real result, a real stat (time, cost, % improvement).
- Language: Hebrew → `"language": "he"`; prices in ש״ח.
- Brand: accent on the AFTER chip.
- Vertical 9:16: see layout.
- Longer clips: add more keyframes; end on 1.0 when the takes drift.

## Sound
- `ui_pop` (.25) at .3, `ar_whoosh` (.35) with each divider move, `chime` (.22) with the stat.

## Pitfalls and QA checklist
- [ ] The two clips line up at the start frame (check a 50/50 frame for a visible seam).
- [ ] End on full AFTER if the takes drift.
- [ ] No ₪ in Hebrew text (ש״ח).
- [ ] The stat bar is centred with a CSS translate that GSAP also animates (y): if it jumps sideways, centre it with `xPercent: -50` inside the tween instead.
- [ ] The divider hides at 0 and 1 (no stray line at the edge).
