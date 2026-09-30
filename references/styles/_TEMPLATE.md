# #NN STYLE-ID · Human name

> One sentence: what the viewer sees.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/style-id.mp4 · full sample: <full render URL from catalog.json>
> Runner: run_style STYLE-ID | run_ad (adkit) | bespoke · Example: examples/...

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: … (real use cases)
- Avoid when: … (wrong footage, too much copy, wrong tone)

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| … | … | … |

## Timing and motion
Times in seconds from the element's start (or on beats). Durations and eases are taken from the builder code.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| … | … | … | … | … | … | … |
- Stagger: …
- Beat/voice sync: …
- The signature move (the one thing that makes this look this look): …

## Typography
- Latin: family, weight, size at 1920×1080, tracking, case
- Hebrew: Suez One / Karantina 700 / Secular One only (which one for which role), RTL rules (mirrored motion, digits glued
  to their word, prices as ש״ח, never ₪)
- Maximum copy length per element before it breaks the layout

## Colour and surface
- Palette roles (accent / ink / paper) with the sample's hex values, and how to swap in brand colours
- Surfaces: glass, blur, stroke, shadow values

## Layout and safe zones (1920×1080 canvas)
- Positions and sizes in px (or % of frame); the relation to the tracked subject; 5% safe margin; 9:16 notes

## What the footage must give you
- Shoot it like this: … (from plates.json)
- Tracking: which objects (vtrack.py objects.json example) / planar (track.py) / none
- Matte: needed or not
- Good vs bad footage for this style

## Build it
### A. With the kit
```bash
python scripts/run_style.py STYLE-ID --spec my_spec.json --render      # or run_ad / bespoke route
```
Every spec key, what it does, and its default:
| Key | Meaning | Default |
|---|---|---|
A minimal spec for a generic project (the user's clip, the user's words):
```json
{ }
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// ≤ 30 lines, simplified from the builder: the signature animation, seek-safe (tl on window.__timelines, no Math.random)
```

## Adapting it to the user's project
- Content: …
- Language: …
- Brand: …
- Vertical 9:16: …
- Longer or shorter clips: …

## Sound
- Cues (whoosh, tick, hit…), where they land, and volume

## Pitfalls and QA checklist
- [ ] …
