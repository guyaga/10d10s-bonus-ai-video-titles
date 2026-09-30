# #36 SIGNATURE-WRITE-ON · Handwriting and marker notes

> Handwritten notes write themselves on, and red marker circles, boxes, underlines and arrows draw on and ride the tracked features.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/signature-write-on.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_SIGNATURE-WRITE-ON.mp4
> Runner: run_style SIGNATURE-WRITE-ON · Example: examples/signature-write-on

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: real-estate walk-throughs and drone reveals ("the penthouse."), product feature call-outs with a personal touch, coaching and tutorials, recipe tips, travel diaries, "look here" moments.
- Avoid when: corporate or technical tone (use LEADER-CALLOUTS); fast-moving subjects the marks can't hold; long sentences (handwriting slows reading).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` .4 |
| SVG layer `#wo` | 1920×1080 SVG over the plate | all notes and marks |
| Note ink `.hw` | the handwritten text, filled, with a 0 3 6 shadow | revealed by a clip rectangle sweeping in reading direction |
| Note pen outline `.hwo` | the same text as a 2 px stroke drawn with dash-offset | visible only while writing; then only the ink remains |
| Underline | a hand-curved quadratic stroke under the note | optional |
| Mark | a marker circle (wobbly ellipse that overshoots its start by 15%), a hand box, or an underline around a tracked object | `pad` px around the object's box |
| Arrow | a curved stroke from the note to an object or point, plus a 30 px arrowhead that appears when the stroke finishes | `bend` sets the curve |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Note sweep (ink reveal) | `t` | `dur` (default .9 + .045 × characters) | easeOut3 (clip width) | until `until` | cut | none |
| Pen outline | `t` | draws over `dur / 1.2` | linear dash | – | disappears when the note is done | – |
| Ink fill | `t` + .15 × dur | fades in over .5 × dur | linear | – | – | – |
| Underline | `t` + .8 × dur | .45 s | linear dash | – | with the note | – |
| Mark | `mark.t` (default end of the note) | `mark.dur` .8 s | linear dash | follows the tracked object | with the note | – |
| Arrow | `arrow.t` (default note end + .3 s) | `arrow.dur` .6 s | linear dash; head appears at the end | – | with the note | – |
- The signature move: **the pen draws the outline while the ink sweeps in right behind it**, in reading direction, followed by a marker circle that overshoots its start like a real hand. The wobble is seeded, so it's the same on every render.

## Typography
- Latin: Caveat 700 (handwriting), default 100 px (sample 78–130).
- Hebrew: **Karantina 700** as the "hand" (the kit has no Hebrew script face in the approved set). The sweep runs right-to-left and the text anchors at its end. Prices as ש״ח.
- Maximum copy: about 25 characters per note; split longer thoughts into two notes at different times.

## Colour and surface
- Roles: `ink` #ffffff, `marker` #ff3b30, `shadow` rgba(0,0,0,.45). For bright skies, flip to dark ink and a light shadow (the sample: ink #14213d, marker #e5251d, shadow rgba(255,248,235,.75)).
- Brand swap: the marker colour carries the brand; keep the ink near black or white for contrast.
- Marker width `stroke` 7 px, round caps and joins, 0 2 4 shadow.

## Layout and safe zones (1920×1080 canvas)
- A free note: `x`, `y` = the text baseline start (left edge for English, right edge for Hebrew). Defaults 960, 540.
- A pinned note: `follow` + `anchor` + `dx`/`dy`, so the note rides the subject.
- Marks use the tracked object's box; arrows start just under the note and end just above the object.
- Put notes in open sky or on a plain wall, inside the 5% margin.

## What the footage must give you
- Shoot it like this: one take, no cuts · features readable and not moving too fast; open sky or wall on one side for the handwriting · 30% free on the left.
- Tracking: every annotated feature (vtrack.py), e.g. `{"objects": [{"name": "terrace", "desc": "the top-floor terrace"}, {"name": "balcony", "desc": "the balconies on the sea side"}]}`. Coverage should be ≥ 80% of frames.
- Matte: not needed.
- Good: a slow drone climb, a smooth glide, a locked product shot. Bad: spins, fast pans, features that leave the frame while circled.

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/my_clip.mp4 objects.json tracks/my_track.json
python scripts/run_style.py SIGNATURE-WRITE-ON --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| notes | list of notes (keys below) | required |
| notes[].text, x, y, size | the words; position; px | –, 960, 540, 100 |
| notes[].t, dur, until | start; write time; end | –, .9 + .045 × chars, never |
| notes[].follow, anchor, dx, dy | pin the note to a tracked object | –, c, 0, 0 |
| notes[].underline | hand underline after the note | false |
| notes[].mark | `{"obj","shape":"circle|box|underline|none","pad","t","dur"}` | –, circle, 24 (circle) / 20 (box) / 12 (underline), end of note, .8 |
| notes[].arrow | `{"to": object or [x,y], "t", "dur", "bend"}` | –, note end + .3, .6, .25 |
| track | the track file for follow / mark / arrow | – |
| language, pair | "he"/"en"; pair only affects body text | "en"; "secular" |
| colors | `{"ink","marker","shadow"}` | #ffffff, #ff3b30, rgba(0,0,0,.45) |
| stroke | marker width px | 7 |
| seed | wobble seed | 4 |
| sfx | UI tick at each note (.35), soft whoosh at each mark (.3) | true |
| music, music_vol, plate_vol, name | optional | –, .55, .4, style id |
```json
{
 "name": "my-notes", "clip": "clips/my_house.mp4", "track": "tracks/my_house_track.json", "language": "en",
 "colors": {"ink": "#14213d", "marker": "#e5251d", "shadow": "rgba(255,248,235,.75)"},
 "notes": [{"text": "the pool.", "x": 120, "y": 220, "size": 120, "t": 2.0, "underline": true,
            "mark": {"obj": "pool", "shape": "circle", "pad": 26}, "arrow": {"to": "pool", "bend": .3}}]
}
```
### B. The core move (per frame, from onPlace)
```js
// seeded wobble per note (mulberry32 from JS_UTIL), never Math.random
const WOB = N.map((n, i) => { const r = mulberry32(SEED * 97 + i); return Array.from({length: 40}, () => r() - .5); });
function circ(b, pad, i) {                       // a marker circle that overshoots its start by ~15%
  const cx = (b[0] + b[2]) / 2, cy = (b[1] + b[3]) / 2, rx = (b[2] - b[0]) / 2 + pad, ry = (b[3] - b[1]) / 2 + pad;
  let d = ""; for (let k = 0; k <= 48; k++) {
    const a = -2.2 + 1.15 * 2 * Math.PI * k / 48, s = 1 + WOB[i][k % 40] * .06 + (k / 48) * .05;
    d += (k ? " L" : "M") + (cx + Math.cos(a) * rx * s).toFixed(1) + "," + (cy + Math.sin(a) * ry * s).toFixed(1);
  } return d;
}
const draw = (el, u) => { el.style.strokeDasharray = "1"; el.style.strokeDashoffset = String(1 - clamp01(u)); };  // pathLength="1"
// the note: a clip rect grows in reading direction; the outline text is drawn with dash-offset slightly ahead of it
const u = clamp01((t - n.t) / n.dur), w = (bb.width + 40) * easeOut3(u * 1.05);
cr.setAttribute("width", w); cr.setAttribute("x", RTL ? bb.x + bb.width + 20 - w : bb.x - 20);
outline.style.strokeDashoffset = String(1 - clamp01(u * 1.2)); ink.style.opacity = clamp01((u - .15) / .5);
```

## Adapting it to the user's project
- Content: 2–4 notes, each one short, human thought ("sunset, included"), with one circle per note at most.
- Language: Hebrew → Karantina 700, sweeping right to left.
- Brand: marker colour; ink dark on bright skies, white on dark footage.
- Vertical 9:16: notes above or below the subject, size 80–100.
- Longer clips: space notes 3–5 s apart and clear each with `until` before the next.

## Sound
- `ui_tick` at .35 as each note starts (a pen touch), `ar_whoosh` at .3 as each circle draws. Music at .55–.6.

## Pitfalls and QA checklist
- [ ] The circle sits on the right object for its whole life (watch the tracked box, not just one frame).
- [ ] Ink contrast works on the brightest frame (switch to dark ink on skies).
- [ ] Arrows don't cross faces or the note itself (adjust `bend`, sign flips the curve side).
- [ ] Hebrew notes anchor at their right edge (x is the start of the reading direction).
