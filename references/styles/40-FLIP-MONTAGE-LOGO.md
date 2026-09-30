# #40 FLIP-MONTAGE-LOGO · Flip montage into the logo

> A Marvel-style closer: frames of the film flip past as 3D pages, faster and faster and more tinted toward the brand colour, then the last page falls away to reveal the wordmark on a colour block with a light sweep.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/flip-montage-logo.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_FLIP-MONTAGE-LOGO.mp4
> Runner: run_style FLIP-MONTAGE-LOGO · Example: examples/flip-montage-logo

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: the last 3–4 seconds of any brand film, trailer, event recap, collection drop or channel intro; any piece that should end on a logo with energy.
- Avoid when: a quiet premium ending (use LOGO-SHINE-REVEAL or FILM-TITLE-CARD); very short clips under 6 s (the montage replaces the last ~3.4 s of the plate); a plate with almost no visual variety (the pages all look alike).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip, until the montage starts | `plate_vol` .35 |
| Montage `#fm` | a black stage with a 2200 px perspective, scaling from 1.28 to 1 | covers the plate from `t` |
| Pages `.pg` | `frames` stills pulled from the plate by ffmpeg at build time, stacked, each hinged on its left edge (right edge in Hebrew) | each page has its own seeded punch-in (1.15–2.25×, off-centre origin) and treatment: mono + contrast, saturated, or contrast + brightness, in rotation |
| Page tint | a brand-colour multiply layer on each page | stronger on later pages (up to `tint`), plus 15% while the page flips |
| Logo block `#blk` | the wordmark (text or image) on a brand-colour block | scales 1.5 → 1 as it lands |
| Light sweep `#sw` | a white diagonal gradient crossing the block | after the block settles |
| Sub line | a small letter-spaced line under the block | fades and rises in |

## Timing and motion
T0 = `t` (default clip length − 3.4 s), MD = `dur` (2.2 s), N = `frames` (18). Page k flips from `T0 + MD × (1 − (1 − k/N)^1.9)` to the next page's start, so the flips accelerate.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Montage stage | T0 − .02 s | cut in; zooms 1.28 → 1 over MD + .6 s | easeInOut | – | – | – |
| Page k flip | its start | the slice until the next start (min .05 s): rotateY 0 → −105° (+105° in Hebrew) | easeInOut | – | hidden after its slice | – |
| Logo block | T0 + MD − .15 s | .7 s from scale 1.5 | easeOut3 | to the end | – | – |
| Light sweep | T0 + MD + .35 s | .8 s across the block | linear | – | – | – |
| Sub line | T0 + MD + .4 s | .5 s fade + y 20 → 0 | linear | to the end | – | – |
- The signature move: **acceleration plus variety**. The page interval shrinks on a 1.9-power curve, each page gets a different punch-in and treatment, and the tint climbs toward the brand colour, so one plate reads as a whole montage and the energy peaks exactly as the logo lands.

## Typography
- Latin: Oswald 700 wordmark, 230 px, tracking .01em; Jost 300 sub line, 46 px, tracking .4em.
- Hebrew: default pair `karantina`: **Karantina 700** wordmark and **Secular One** sub line; pages hinge on the right and flip the other way. For a premium logo use `pair: suez`. Prices, if any, as ש״ח.
- A real logo file: `logo.image` replaces the text (max 1200×300 px on the block).
- Maximum copy: the wordmark about 10 characters at 230 px; the sub line about 25.

## Colour and surface
- Roles: `brand` #e8321f (the block and the page tint; the sample uses #ff5a1f), `text` #ffffff, `tint` .55.
- Surfaces: pages cast a 60 px dark shadow; the block is flat colour; the sweep is a 100° white gradient at .55.
- Brand swap: `brand` = the primary brand colour; the text stays white (or the logo image).

## Layout and safe zones (1920×1080 canvas)
- Pages are full frame. The block is centred; with the sub line, the group is centred vertically.
- Keep the logo image inside 1200×300 so it stays within the safe margin at scale 1.

## What the footage must give you
- Shoot it like this: cuts OK (max 6) · variety across the shot (close-ups, wides, details) makes the flip read · no free space needed.
- Tracking: none.
- Matte: not needed.
- The last ~3.4 s of the plate is replaced, so plan the story to end before that. Frames are sampled evenly between `from` (.2 s) and `to` (length − .2 s).
- Good: a clip with different framings over its length. Bad: one static framing for the whole clip (use `from`/`to` to sample the most varied part).

## Build it
### A. With the kit
```bash
python scripts/run_style.py FLIP-MONTAGE-LOGO --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| t | when the montage starts (s) | clip length − 3.4 |
| dur | montage length before the logo lands | 2.2 |
| frames | pages to flip | 18 |
| from, to | the plate range to sample pages from | .2, length − .2 |
| logo | `{"text", "sub", "image"}` (image replaces text) | {"text": "LOGO"} |
| colors | `{"brand","text","tint"}` | #e8321f, #ffffff, .55 |
| seed | page punch-in seed | 21 |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "karantina" |
| fonts | override faces | Oswald 700 + Jost 300 |
| sfx | tick .25 on every 2nd flip, whoosh .5 at the start, logo hit .9 as it lands | true |
| music, music_vol, plate_vol, name, track | optional | –, .6, .35, style id, – |
```json
{
 "name": "my-closer", "clip": "clips/my_recap.mp4", "frames": 20,
 "logo": {"text": "SUMMIT 26", "sub": "SEE YOU NEXT YEAR"}, "colors": {"brand": "#1e6cff", "tint": .5},
 "music": "shared/sfx/my_bed.mp3", "music_vol": 0.6
}
```
### B. The core move (per frame, from onPlace)
```js
const start = (k) => T0 + MD * (1 - Math.pow(1 - k / N, 1.9));     // accelerating flip clock
window.onPlace = (t) => {
  document.getElementById("stk").style.transform = `scale(${1.28 - .28 * easeInOut((t - T0) / (MD + .6))})`;
  PG.forEach((p, k) => {
    const s = start(k), e = start(k + 1), u = clamp01((t - s) / Math.max(.05, e - s));
    p.style.zIndex = String(N - k); p.style.display = t > e + .02 ? "none" : "block";
    p.style.transform = `rotateY(${(RTL ? 1 : -1) * 105 * easeInOut(u)}deg)`;     // hinge: transform-origin 0 50%
    p.lastChild.style.opacity = TINT * (k / N) + .15 * u;                        // brand tint climbs
  });
  const L = T0 + MD, v = easeOut3((t - L + .15) / .7);
  blk.style.transform = `scale(${1.5 - .5 * v})`;
  sw.style.left = (-45 + 190 * clamp01((t - L - .35) / .8)) + "%";
};
// page variety is fixed at build time from a seeded RNG: scale 1.15-2.25, origin 20-80% / 15-85%, filter in rotation
```

## Adapting it to the user's project
- Content: the brand or campaign name plus one sub line ("OUT NOW", the date, the URL).
- Language: Hebrew → Karantina wordmark, pages flip right-to-left.
- Brand: `brand` colour, or a logo image on the block.
- Vertical 9:16: pages still full frame; wordmark about 150 px so it fits the crop.
- Longer clips: nothing changes; `t` defaults to the last 3.4 s. For an opener instead of a closer, set `t` to .3 and `from`/`to` over the whole clip.

## Sound
- `ui_whoosh` at .5 just before the montage, `ui_tick` at .25 on every second flip (the ticks speed up with the flips), `logo_hit` at .9 as the block lands. Music at .6–.65, ideally with a hit at T0 + MD.

## Pitfalls and QA checklist
- [ ] The story ends before `t`; nothing important is hidden by the montage.
- [ ] The pages look different from each other (if not, narrow `from`/`to` to the most varied part or raise `frames`).
- [ ] The logo lands on a music hit.
- [ ] The logo image has a transparent background and fits within 1200×300.
