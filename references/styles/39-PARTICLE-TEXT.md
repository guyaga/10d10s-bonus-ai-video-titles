# #39 PARTICLE-TEXT · Words from embers, sand or smoke

> Words assemble out of rising embers, blowing sand or gathering smoke, resolve into a crisp glowing word, then dissolve back the same way.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/particle-text.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_PARTICLE-TEXT.mp4
> Runner: run_style PARTICLE-TEXT · Example: examples/particle-text

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: food and fire (grills, bakeries, pizza), spices, salt, coffee and steam, desert and beach travel, perfume and incense, luxury reveals, brand names that should "materialise".
- Avoid when: the footage has no matching element (particles that don't belong look like a plug-in); long copy (1–2 words plus a small line); busy bright areas where the word would form (a light plate needs `scrim`).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` .35 |
| Scrim (optional) | a soft dark radial pool behind the word | `scrim` 0–1; for light plates |
| Particles | small squares on a 1920×1080 canvas, one per sampled pixel of the word (every `density` px) | additive (`lighter`) blend; embers get a faint halo and flicker |
| Solid word | the crisp word drawn over the particles once they've assembled | a glow in the mode's first colour (28 px blur for embers, 16 px otherwise) |
| Sub line | a smaller line under the word | sampled into particles too; drawn at 0.72 × size below |

## Timing and motion
Per word: t0 = `t`, t1 = t0 + `form`, t2 = `hold_until`, t3 = t2 + `out`.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Particle k | t0 + random(0–.45) × form | .6 × form, from its start point to its place in the word | easeOut3, with a shrinking swirl (90 px → 0) | a tiny .8 px shimmer | dissolve starts t2 + random(0–.35) × out, over .65 × out | quadratic (embers rise, sand blows, smoke drifts) |
| Solid word | t1 + .15 | .5 s fade to .92 | linear | until t2 | fades over .35 × out | linear |
| Particles while solid | – | – | – | thin to 30% | back to full to dissolve | – |
- Start points by mode: **embers** rise from below the frame (x within ±750 px of the word, y 1120–1380); **sand** blows in from the reading side (from the left for English, from the right for Hebrew); **smoke** rises from 380–680 px below the word.
- Dissolve by mode: embers float up 220–600 px with a sideways sway; sand blows away 300–1000 px toward the far side and falls; smoke drifts up 160–420 px and swells to 4 × its size.
- The signature move: **the particles become the real word**. After they assemble, a crisp glowing word takes over for reading, then hands back to the particles to dissolve. Every position is an analytic function of (t, seed) with no simulation state, so any frame can be seeked and rendered identically.

## Typography
- Latin: Jost 700 display (default 200 px; sample 170–230), Jost 300 for the sub line (default 26% of the size).
- Hebrew: default pair `suez`: **Suez One** word, **Secular One** sub line. The canvas direction is set to RTL, and sand blows in from the right. For a louder word use `pair: karantina`. Prices as ש״ח.
- Maximum copy: about 10 characters per word at 200 px (particle count grows with area); one sub line about 25 characters.

## Colour and surface
- Palettes (3 colours, picked per particle): embers #ffb13b, #ff5a1f, #fff1c9 · sand #f3e3c3, #d9c29b, #ffffff · smoke #f4f1ec, #cfc8bd, #ffffff. Override per mode with `palette`.
- The solid word is warm white #fff4e0 for embers and white otherwise; its glow uses the mode's first colour.
- Brand swap: a warm brand colour as the embers' first colour; keep sand and smoke near-neutral.

## Layout and safe zones (1920×1080 canvas)
- The word is centred at `x`, `y` (default 960, 420). Place it in the dark, low-detail space above or beside the subject.
- Particles travel outside the word's box on the way in and out; keep at least 200 px around the word clear of faces.

## What the footage must give you
- Shoot it like this: cuts OK (max 5) · subject low or to one side; dark, low-detail space above it · 30% free at the top.
- Tracking: none.
- Matte: not needed.
- Good: a grill with rising sparks (embers), a salt pour or a beach (sand), a steaming cup or plate (smoke), with a dark top third. Bad: bright white plates behind the word (use `scrim` ≥ .5), heavy real smoke that hides the word.

## Build it
### A. With the kit
```bash
python scripts/run_style.py PARTICLE-TEXT --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| words | list of words (keys below) | required |
| words[].text, sub | the word; a small line under it | –, none |
| words[].mode | embers / sand / smoke | embers |
| words[].t, form | start; seconds to assemble | –, 1.2 |
| words[].hold_until, out | when it starts dissolving (null = stays); dissolve seconds | null, 1.0 |
| words[].x, y, size | centre and size | 960, 420, 200 |
| words[].weight | display / body | display |
| words[].subsize | sub line px | 26% of size |
| words[].density | sampling step px (smaller = more particles, 4–6) | 5 |
| words[].scrim | dark pool behind the word, 0–1 | 0 |
| palette | per-mode colour lists | see Colour |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "suez" |
| fonts | override faces | Jost 700 + Jost 300 |
| seed | particle seed | 11 |
| sfx | UI whoosh .35 at each word, soft whoosh .3 at each dissolve | true |
| music, music_vol, plate_vol, name, track | optional | –, .6, .35, style id, – |
```json
{
 "name": "my-particles", "clip": "clips/my_coffee.mp4",
 "words": [
  {"text": "ROASTED", "mode": "smoke", "t": 0.8, "form": 1.4, "hold_until": 4.0, "x": 960, "y": 260, "size": 190, "density": 4},
  {"text": "DAILY", "sub": "SINCE 1987", "mode": "sand", "t": 5.0, "form": 1.3, "x": 960, "y": 240, "size": 200, "scrim": .5}
 ]
}
```
### B. The core move (seeded, per frame from onPlace)
```js
// 1. once: rasterise the word into an offscreen canvas and keep every `step` px pixel as a target point.
//    Each particle gets 5 seeded randoms r[0..4] = mulberry32(SEED * 1000 + wordIndex)()  (never Math.random)
// 2. every frame: position = f(t, r) only, no state carried between frames (seek-safe)
for (const p of P[wi]) {
  const delay = p.r[2] * .45 * w.form, u = easeOut3((t - t0 - delay) / (w.form * .6));
  let x, y, a;
  if (t < t2) {                                   // assemble with a swirl that shrinks to zero
    const sw = (1 - u) * 90;
    x = p.sx + (p.tx - p.sx) * u + Math.sin(t * 3 + p.r[3] * 6.28) * sw;
    y = p.sy + (p.ty - p.sy) * u + Math.cos(t * 2.3 + p.r[0] * 6.28) * sw;
    a = t < t0 + delay ? 0 : Math.min(1, (t - t0 - delay) / .25);
  } else {                                        // dissolve (embers: rise and sway)
    const v = clamp01((t - t2 - p.r[2] * .35 * w.out) / (w.out * .65));
    x = p.tx + (p.r[0] - .5) * 160 * v; y = p.ty - (220 + p.r[1] * 380) * v * v; a = 1 - v;
  }
  const flicker = .55 + .45 * hash1(Math.floor(t * 18) + p.r[4] * 997);   // embers only
  cx.globalAlpha = a * flicker; cx.fillStyle = p.c; cx.fillRect(x - 2, y - 2, 4.2, 4.2);
}
```

## Adapting it to the user's project
- Content: 1–3 words across the clip, each over the shot that contains its material (fire → embers, salt/sand → sand, steam → smoke).
- Language: Hebrew → Suez One; sand blows from the right.
- Brand: the brand name as the last word, formed from smoke or embers over the hero shot, with `hold_until` null so it stays.
- Vertical 9:16: size 150–170, x at 540 of the crop; density 4 keeps it dense.
- Longer clips: one word per shot; avoid two words forming at the same time (particle count doubles).

## Sound
- `ui_whoosh` at .35 as each word forms, `ar_whoosh` at .3 as it dissolves. Diegetic sound (sizzle, wind) helps; music at .6.

## Pitfalls and QA checklist
- [ ] The word is legible for at least 1.5 s between assembly and dissolve.
- [ ] Light plates get a `scrim`; white text on a white plate is unreadable.
- [ ] Density 4–6: finer than 4 gets heavy to render, coarser than 6 looks blocky.
- [ ] The web font is loaded before the canvas samples it (the kit warms it with a hidden DOM copy; a blank word means the font didn't load).
- [ ] Particles never cross the subject's face on the way in.
