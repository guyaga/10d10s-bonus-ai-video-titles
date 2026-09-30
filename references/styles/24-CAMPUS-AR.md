# #24 CAMPUS-AR · Smart-glasses place labels

> A walking tour seen through smart glasses: small bilingual glass tags pop onto real places and people (a library, a study area, a visitor), each with a pulsing dot on the exact spot; a status chip, an optional REC light and voice waveform, and an optional logo end card.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/campus-ar.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/TEST_C_campus_ar.mp4
> Runner: run_style CAMPUS-AR · Example: examples/campus-ar

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: campus and office tours, museums, hotels and venues, retail stores ("aisle 4 · new arrivals"), factory walk-throughs, onboarding videos, real estate walks.
- Avoid when: the labelled places leave the frame quickly, there are more than 4–5 labels in a short clip, or the piece needs big emotional titles (combine with a title style instead).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `.tick` ×4 | corner brackets | |
| `.chip` | top-right status chip with a blinking dot: "ONO AR · CAMPUS TOUR" | mono 20 px, .14em |
| `.dot` | 18 px accent dot with a dark 5 px ring and a 20 px glow, pinned to the tracked place | optional per tag (`dot: false` for people) |
| `.ar` tag | glass panel with a 4 px accent left border: English 40 px/800, Hebrew 32 px/600 RTL, mono sub 18 px | placed right / left / above / below the anchor |
| `#rec` | REC chip with a red dot, top-left | optional |
| `#wave` | 36-bar animated voice waveform, bottom centre, 80 px tall | optional |
| `#endg` / `#end` | bottom gradient + logo on a white plate (max 380 × 180) + English 56 px + Hebrew 44 px | optional end card |

## Timing and motion
From `scripts/styles/campus.py`.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| corner ticks | 0.05, stagger 0.05 | 0.45 (scale 1.4 → 1) | default | whole clip | — | — |
| chip | 0.2 | 0.4 (x 20 → 0); dot blinks 0.5 × 11 | default / sine.inOut | — | at end − 0.1 | 0.35 |
| dot | tag.t − 0.1 | 0.35 (scale 0 → 1) | back.out(3) | follows the place | with the tag | — |
| tag | tag.t (default 0.6 + 0.9 × i) | 0.5 (slides 16 px from the anchor side + clip opening top → bottom) | expo.out | follows the place | 0.3 at `until` | default |
| REC | rec.t [3.55] | 0.3 (scale 1.2 → 1); dot blinks 0.4 × 6 | power4.out / none | — | — | — |
| waveform | wave.t [3.6] | 0.4 (y 20 → 0); bars ramp in over 0.4 | default | bars move per frame | 0.3 at `until` | default |
| end card | end.t − 0.1: everything else fades 0.35; gradient 0.6 at end.t | logo 0.8 (scale .85 → 1) at +0.15; English +0.5, Hebrew +0.65 (0.5, y 16 → 0) | expo.out / default | to end | — | — |
- The signature move: labels that belong to the place. Each tag is anchored to a tracked object (`data-follow` + anchor + dx/dy) and slides out FROM the place, so it reads as the glasses recognising it.

## Typography
- Latin: **Secular One** 800 (tag name 40 px, line-height 1.05), **JetBrains Mono** for the chip, sub line and REC (18–22 px, letter-spacing .1–.14em).
- Hebrew: Secular One 32 px/600, RTL, left-aligned under the English so the tag keeps one clean edge (the accent border on the left). Hebrew-first: swap the lines.
- Max copy: name ≈ 18 characters, Hebrew line ≈ 18, sub ≈ 24. Tags are short on purpose: glasses show labels, not sentences.

## Colour and surface
- Roles: `accent` #9bd14a, `fg` #eef4e8, `mute` #b9c7b0; glass panels `rgba(7,13,9,.8)`.
- Rebrand with the institution's colour on the dots, borders and chip dot; keep the panels dark.

## Layout and safe zones (1920×1080 canvas)
- Tags sit beside their anchor: `place: right` offsets +36 px, `left` −36, `above` −30, `below` +30 (override with dx/dy). The chip sits right 112 / top 60; REC left 112 / top 60; the waveform bottom 90; the end card bottom 120.
- Keep 25% free on each side of the walking person (the contract) so tags have room.
- 9:16: use `above`/`below` placements; the chip moves under the top safe area.

## What the footage must give you
- Shoot it like this: one take, no cuts, 5–10 s · medium-wide, the person centred and walking toward camera · 25% free on both sides · slow steady dolly backwards at chest height matching the walk.
- Seedance lines: "FORMAT: One continuous shot, no cuts." / "CAMERA: Slow steady dolly backwards at chest height matching his pace. FORBIDDEN: whip-pans, zooms, shake, cuts." / "POSITIVE LOCKS: Exactly one person. The room layout stays identical to the first frame. No text, no signs, no UI, no logos."
- Tracking (vtrack.py): the person (`man` / `head`) and each labelled place (`shelves`, `desks`, …). See examples/campus-ar/objects.json. Gate: ≥90% coverage.
- Matte: not needed.

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/tour.mp4 tour_objects.json tracks/tour_vtrack.json
python scripts/run_style.py CAMPUS-AR --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip, track | plate + vtrack file | required |
| chip | top-right status chip | none |
| tags | [{follow, anchor, dx, dy, en, he, sub, t, until, place, dot}] | required; anchor "c", place "right", dot true, t .6 + .9·i |
| rec | {t, text} | none |
| wave | {t, until} voice waveform | none |
| end | {t, logo, en, he} end card | none |
| colors | {accent, fg, mute} | #9bd14a / #eef4e8 / #b9c7b0 |
| sfx / music / music_vol / plate_vol / name | sound + levels | true / – / – / .7 |
A minimal spec for a generic project (an office tour with an end card):
```json
{
  "name": "office-tour",
  "clip": "clips/office_walk.mp4",
  "track": "tracks/office_walk.json",
  "chip": "NORTHWIND · OPEN DAY",
  "tags": [
    {"follow": "kitchen", "place": "left", "en": "Kitchen", "he": "מטבח", "sub": "COFFEE ALL DAY", "t": 0.8},
    {"follow": "screens", "place": "above", "en": "Dev floor", "he": "קומת הפיתוח", "t": 2.2},
    {"follow": "head", "anchor": "r", "dx": 40, "en": "Dana", "he": "מנהלת הצוות", "sub": "HOST", "t": 3.6, "dot": false}
  ],
  "end": {"t": 5.4, "logo": "brand/logo.png", "en": "Come build with us", "he": "בואו לבנות איתנו"}
}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// markup: <div id="p0" data-follow="shelves" data-anchor="c" data-dx="-70"><div class="pl" style="transform:translate(-100%,-50%)">
//           <div id="g0" class="ar panel"><span class="en">Library</span><span class="he">הספרייה</span></div></div></div>
// the kit moves [data-follow] to the tracked anchor every frame; the tag itself only animates its entrance
const FROM = {right: {x: -16}, left: {x: 16}, above: {y: 16}, below: {y: -16}};
function tag(i, place, at, until) {
  tl.set(`#g${i}`, {opacity: 0}, 0);
  tl.fromTo(`#d${i} .dot`, {scale: 0}, {scale: 1, duration: .35, ease: "back.out(3)"}, at - .1);
  tl.fromTo(`#g${i}`, {opacity: 0, ...FROM[place], clipPath: "inset(0 0 100% 0)"},
                      {opacity: 1, x: 0, y: 0, clipPath: "inset(0 0 0% 0)", duration: .5, ease: "expo.out"}, at);
  if (until != null) tl.to([`#g${i}`, `#d${i}`], {opacity: 0, duration: .3}, until);
}
tag(0, "left", 1.0); tag(1, "above", 2.5); tag(2, "right", 3.9);
window.onPlace = (t) => {                                  // waveform: pure function of t (seek-safe)
  document.querySelectorAll("#wave b").forEach((b, i) =>
    b.style.height = (6 + Math.abs(Math.sin(t * 9 + i * .7) * Math.sin(t * 3.1 + i * .31)) * 60) + "px");
};
```

## Adapting it to the user's project
- Content: label what a visitor needs (the name of the place, one fact: hours, capacity, a feature); name people only with permission.
- Language: bilingual; for a Hebrew-only audience set `en` to the Hebrew text and leave `he` empty.
- Brand: the accent + the end card logo and line.
- With a narrator: add `rec` and `wave` with the VO start time so it feels like live-streamed glasses.
- Longer walks: give each tag an `until` so only 2–3 are on screen at once.

## Sound
- Cues: ar_whoosh 0.1 (.5), glass_ting 0.05 s before each tag (.6), rec_beep at REC (.7), logo_hit at the end card + 0.1 (.8). Plate .7.

## Pitfalls and QA checklist
- [ ] Each tag's anchor object is tracked for the whole time the tag is on screen (a lost box parks the tag).
- [ ] Tags never cover the walking person's face.
- [ ] Places that leave the frame get an `until` before they exit.
- [ ] The end-card logo has transparent padding cropped (it sits on a white plate).
- [ ] Look at a frame for each tag's first full second and at the end card; qa.py until "ship".
