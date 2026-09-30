# #41 TEXT-ON-PATH · Words riding the road

> Words ride a tracked road, river or trail: the route draws on as a glowing line, and the text slides along it, bending with the road as the camera moves.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/text-on-path.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_TEXT-ON-PATH.mp4
> Runner: run_style TEXT-ON-PATH · Example: examples/text-on-path (spec.json English, spec_he.json Hebrew)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: travel and tourism ("from the airport to the beach"), real-estate location films ("12 minutes to the city"), delivery and logistics, running and cycling routes, road trips, event directions.
- Avoid when: the route is hidden behind buildings or trees for part of the shot; the camera rotates or rolls (the route jumps); ground-level footage where the road is foreshortened to a sliver.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's aerial clip | `plate_vol` .5 |
| Route glow | the route drawn wide (2.6 × width) at .45 opacity, blurred 8 px | optional (`glow`) |
| Route line | the route drawn on with dash-offset | `width` 10 px, round caps, `color` #9bd14a |
| Text line | an SVG `<text>` on a `<textPath>` following an upright copy of the route | a .55 black stroke under the fill for legibility |
The path is rebuilt every frame as a smooth Catmull-Rom curve through the tracked route points, in order.

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Route line | `draw.t` (1.5 s) | `draw.dur` (2.0 s) dash-offset 1 → 0 | easeInOut | stays drawn | – | – |
| Text line | `t` | .4 s fade in | linear | slides from `from` to `to` along the path until `until` (default t + 6) | .4 s fade out before `until` | linear |
| Slide | `t` | `until − t` | easeInOut on startOffset | – | – | – |
- The signature move: **the words physically ride the road**. Because the path is rebuilt from tracked points every frame and the text's start offset travels along it, the letters bend around the curves and stay glued to the road as the drone moves.

## Typography
- Latin: Oswald 700 (display), 44 px default (sample 40 px), tracking .04em; Jost 500 for body-weight lines.
- Hebrew: default pair `secular`: **Secular One** (clean and legible along a curve). Karantina 700 (`pair: karantina`) for a bolder line.
- **Chrome's Hebrew-on-a-path bug.** Never set `direction="rtl"` on a `<textPath>`: Chrome drops the text entirely. The kit lays the text on an **upright copy of the route** (the path is reversed whenever it runs right-to-left on screen, so letters never stand on their heads) and lets Chrome's bidi algorithm order the Hebrew runs. The shipped Hebrew sample reads correctly right-to-left this way.
- Units in Hebrew lines: "12.8 ק״מ", prices as ש״ח.
- Maximum copy: the line must fit the path length between `from` and `to` plus its slide; about 30 characters at 40–44 px on a route crossing half the frame.

## Colour and surface
- Roles: route `color` #9bd14a (lime), text `color` #ffffff, legibility stroke rgba(0,0,0,.55) 5 px.
- Brand swap: the route colour is the brand accent; keep the text white with its dark stroke.

## Layout and safe zones (1920×1080 canvas)
- Everything follows the route. `from`/`to` (0–1) choose which stretch of the path the line's start travels; `dy` (default −18) lifts the text above the road line (negative = above).
- Keep route points inside the frame for the whole shot; points that leave the frame bend the path to the edge.

## What the footage must give you
- Shoot it like this: one take, no cuts · the route clearly visible and roughly flat to camera, not hidden behind buildings · no free space needed.
- Tracking: route points with the planar tracker. Pick 5–7 points along the road on frame 0 (`{"points": {"r0": [x, y], ...}}` in the clip's frame-0 pixels), then `track.py` follows them through the shot with chained homographies. Tracked boxes from vtrack.py also work (their centres are used). Coverage must be 100%.
- Matte: not needed.
- Good: a high drone shot with a slow forward push and slight descent, the road visible throughout. Bad: rotation, roll, fast pans, cuts, a road that disappears under trees.

## Build it
### A. With the kit
```bash
python scripts/track.py clips/my_aerial.mp4 anchors.json tracks/my_route.json [--mask-top 0.2]   # ignore sky features
python scripts/run_style.py TEXT-ON-PATH --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| track | the route point file (track.py or vtrack.py) | required |
| route | point/box names in order along the road | required |
| draw | `{"t","dur","width","color","glow"}`; null = no line | {"t": 1.5, "dur": 2.0, "width": 10, "color": "#9bd14a", "glow": true} |
| lines | list of lines (keys below) | required |
| lines[].text | the words | required |
| lines[].t, until | in / out | –, t + 6 |
| lines[].from, to | where on the path (0–1) the line's start travels | 0, .6 |
| lines[].size, dy | px; offset from the road (negative = above) | 44, −18 |
| lines[].weight, color | display/body; fill colour | display, #ffffff |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "secular" |
| fonts | override faces | Oswald 700 + Jost 500 |
| sfx | scan beeps .25 as the route draws, soft whoosh .4 per line | true |
| music, music_vol, plate_vol, name | optional | –, .55, .5, style id |
```json
{
 "name": "my-route", "clip": "clips/my_aerial.mp4", "track": "tracks/my_route.json",
 "route": ["r0", "r1", "r2", "r3", "r4", "r5"],
 "draw": {"t": 1.0, "dur": 2.0, "width": 8, "color": "#ffb13b"},
 "lines": [{"text": "BEACH · 6 MIN", "t": 1.8, "until": 8.5, "from": 0.05, "to": 0.4, "size": 42, "dy": -16}]
}
```
### B. The core move (per frame, from onPlace)
```js
const P = ROUTE.map(r => { const b = boxAt(r, t); return b && [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2]; }).filter(Boolean);
const d = catmull(P);                                            // smooth path through the tracked points
// upright copy: if the route runs right-to-left on screen, reverse it so the glyphs aren't upside down.
// NEVER put direction="rtl" on the <textPath>: Chrome drops the text. Bidi orders Hebrew runs by itself.
const up = P[P.length - 1][0] < P[0][0] ? catmull([...P].reverse()) : d;
document.getElementById("rpu").setAttribute("d", up);            // <textPath href="#rpu">
const u = easeInOut((t - DR.t) / DR.dur);                        // route draw-on (pathLength="1")
rl.setAttribute("d", d); rl.style.strokeDasharray = "1"; rl.style.strokeDashoffset = String(1 - u);
for (const l of LN) {                                            // slide each line along the road
  const v = easeInOut((t - l.t) / ((l.until ?? l.t + 6) - l.t));
  document.getElementById("tp" + l.i).setAttribute("startOffset", ((l.from + (l.to - l.from) * v) * 100).toFixed(2) + "%");
}
```

## Adapting it to the user's project
- Content: a destination and a distance or time ("OLD PORT · 4 MIN"); one line per road segment.
- Language: Hebrew → Secular One; don't touch the path direction yourself, the kit handles it.
- Brand: the route colour.
- Vertical 9:16: pick route points inside the crop; size 36–40.
- Longer clips: several lines on successive stretches (`from`/`to` 0–.3, .35–.65, .7–1).

## Sound
- `scan_beeps` at .25 as the route draws, `ar_whoosh` at .4 as each line appears. Music at .55.

## Pitfalls and QA checklist
- [ ] Watch the tracker preview: the points stay on the road for the whole shot.
- [ ] The text never renders upside down (the route may flip direction mid-shot; the upright copy handles it).
- [ ] Hebrew lines are present and read right-to-left (if the text vanished, something set `direction="rtl"` on the path).
- [ ] The line fits between `from` and `to` without running off the end of the path.
- [ ] The text is large enough to read over the aerial (the sample's 40 px is on the small side; 44–52 px is safer).
