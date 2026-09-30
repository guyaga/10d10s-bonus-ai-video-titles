# #32 GLITCH-RGB · Beat glitch

> On every beat hit the whole frame tears and the words split into red, green and blue copies and jittering slices, then snap back clean.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/glitch-rgb.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_GLITCH-RGB.mp4
> Runner: run_style GLITCH-RGB · Example: examples/glitch-rgb

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: streetwear drops, music releases, gaming, tech launches, nightlife; anything cut to a strong beat.
- Avoid when: calm or premium tone; no music with clear hits; footage that's already shaky or noisy (the energy has to come from the glitch, not the camera); viewers sensitive to flashing (keep `strength` ≤ .6 and hits sparse).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate + tear filter | the user's clip through an SVG filter `#tear` | fractal-noise displacement band (`baseFrequency 0.0008 0.09`) + red/blue channel offsets |
| Title `.gt` | a word at (x, y) or pinned to a tracked object | zero-size anchor, `align` sets the edge |
| Base word | the clean word | soft shadow 0 10 40 rgba(0,0,0,.45); drops to .15 opacity during a burst |
| RGB copies | three copies (r, g, b) blended with `screen` | offset left/centre/right by 18 px × burst, plus jitter |
| Slices | 7 horizontal bands of the word (clip-path) | each band randomly on/off and pushed up to ±80 px sideways during a burst |
| Sub line | small mono line under the word | accent colour, 34 px, heavy dark shadow for legibility |

## Timing and motion
Beat n = `offset + n × 60 / bpm`. Title in/out are in beats.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Title | its `beat` − .04 s | a local burst that fades over .3 s | linear | until `until` | burst over the last .1 s, gone at `until` + .12 s | linear |
| Frame tear | every hit | .28 s burst, decaying from 1 | linear, stuttered at 24 fps | – | – | – |
| RGB split | during a burst | per frame | – | – | – | – |
| Slices | during a burst, each on if hash > .45 | per frame | – | – | – | – |
- Hits: `hits` beats, or by default every title's `beat` and `until`.
- Burst envelope: `(1 − d/.28)` for .28 s after a hit, and each 1/24 s frame is either full or 15% (a hash decides), which gives the stutter.
- Tear amounts at full burst: displacement scale 110, red/blue channel offset ±14 px, all × `strength`.
- The signature move: **stillness between hits**. Everything is sharp and static, then for .28 s the plate tears and the word explodes into RGB slices on the exact beat. Contrast is what sells it.

## Typography
- Latin: Oswald 700, uppercase, tracking .01em, default 200 px (sample: 230 for the brand, 150 for items). Sub line: IBM Plex Mono 500, 34 px, tracking .3em.
- Hebrew: **Karantina 700** display + Secular One sub line (default pair `karantina`). No uppercase or tracking in Hebrew. Prices in the sub line as ש״ח.
- Maximum copy: one word per title (up to about 10 letters at 200 px). The sub line up to about 30 characters.

## Colour and surface
- Roles: `text` #ffffff, `sub` #ff5a1f (the accent), channel colours `r` #ff2a3c, `g` #29ff9a, `b` #2d6bff. Brand swap: change `sub` only; keep the channel colours near RGB or the split stops reading as a glitch.
- Surfaces: none. The sub line gets a 3 px + 14 px dark shadow.

## Layout and safe zones (1920×1080 canvas)
- Free titles: `x`, `y` (default 960, 540). The brand title in the sample sits at y 300 above the subject; the end title at x 90, left-aligned.
- Pinned titles: `follow` the tracked garment, `anchor` "r" + `align` "left" + `dx` 70 (word to the right of the object), or `anchor` "l" + `align` "right" + `dx` −70.
- Keep words within the 5% margin even at full slice offset: slices move up to ±80 px.

## What the footage must give you
- Shoot it like this: cuts OK (max 6) · subject centred, walking or posing; plain walls or sky either side · 25% free on both sides.
- Tracking: optional, only for words pinned to items (vtrack.py, e.g. objects "jacket", "cargo", "sneakers").
- Music: required in practice. Measure the grid with librosa (`beat_track`) and put `bpm` and `offset` in the spec.
- Good: a locked or slow-push shot, graphic negative space, contrasty light. Bad: handheld shake, cluttered backgrounds, soft low-contrast footage.

## Build it
### A. With the kit
```bash
python scripts/run_style.py GLITCH-RGB --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| titles | list of titles (keys below) | required |
| titles[].text, sub | the word and the small line under it | –, none |
| titles[].beat, until | in/out in beats | –, never |
| titles[].x, y, size, align | free position, size, anchor edge | 960, 540, 200, center |
| titles[].follow, anchor, dx, dy | pin to a tracked object | –, c, 0, 0 |
| beat | `{"bpm", "offset"}` | 120, 0 |
| hits | beats where the frame glitches | every title's beat + until |
| strength | global glitch amount | 1.0 |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "karantina" |
| fonts | override faces | Oswald 700 + IBM Plex Mono 500 |
| colors | `{"text","sub","r","g","b"}` | #ffffff, #ff5a1f, #ff2a3c, #29ff9a, #2d6bff |
| seed | slice-offset seed | 9 |
| sfx | lock tick on every hit (.45), data chatter on every 2nd hit (.18) | true |
| music, music_vol, plate_vol, name, track | optional | –, .6, .3, style id, – |
```json
{
 "name": "my-glitch", "clip": "clips/my_clip.mp4", "beat": {"bpm": 124, "offset": 0.08},
 "titles": [
  {"text": "LAUNCH", "sub": "APP 2.0 · OUT NOW", "beat": 2, "until": 8, "x": 960, "y": 320, "size": 220},
  {"text": "FASTER", "sub": "2× SPEED", "beat": 9, "until": 13, "x": 1500, "y": 540, "size": 160, "align": "right"}
 ],
 "music": "shared/sfx/my_track.mp3", "music_vol": 0.65
}
```
### B. The core move (seeded, per frame from onPlace)
```js
// hash1(n): deterministic 0..1 from a number (JS_UTIL). Never Math.random: every frame is a pure function of t.
function env(t) {                                 // .28 s stuttering burst after each hit
  let a = 0;
  for (const h of HITS) { const d = t - h;
    if (d >= -0.04 && d < .28) a = Math.max(a, (1 - d / .28) * (hash1(Math.floor(t * 24) * 7.3 + h) > .25 ? 1 : .15)); }
  return a;
}
window.onPlace = (t) => {
  const a = env(t) * K, fr = Math.floor(t * 24);
  dm.setAttribute("scale", (a * 110).toFixed(1));          // plate tear (feDisplacementMap)
  tb.setAttribute("seed", String(1 + fr % 97));            // new noise band every frame
  orr.setAttribute("dx", (a * 14).toFixed(1)); ob.setAttribute("dx", (-a * 14).toFixed(1));  // R/B split
  rgb.forEach((c, k) => c.style.transform =
    `translate(${((k - 1) * 18 + (hash1(fr * 3 + k) - .5) * 20) * a}px,${(hash1(fr + k * 5) - .5) * 8 * a}px)`);
  slices.forEach((s, k) => { s.style.opacity = a > .05 && hash1(fr * 13 + k * 7) > .45 ? 1 : 0;
    s.style.transform = `translateX(${(hash1(fr * 17 + k * 29 + SEED) - .5) * 160 * a}px)`; });
};
```

## Adapting it to the user's project
- Content: one word per beat section; the sub line carries the name and price.
- Language: Hebrew → Karantina 700; the RGB copies and slices work the same.
- Brand: the sub colour is the brand accent.
- Vertical 9:16: stack titles top and bottom of the subject; reduce `size` to 150.
- Longer clips: add titles and let `hits` default; for a long quiet stretch, add hits only on downbeats.

## Sound
- `lock_tick` at .45 on every hit and `data_chatter` at .18 on every second hit. The music bed at .6–.65 is the real driver.

## Pitfalls and QA checklist
- [ ] Hits land on audible beats: scrub 3 hits against the waveform.
- [ ] Between hits the titles are perfectly clean (no leftover slice or RGB offset).
- [ ] The sub line stays readable over the plate (its shadow is on).
- [ ] Not too many hits: more than about 1 every 2 s turns into noise and a flashing risk.
- [ ] Slices don't push words outside the frame.
