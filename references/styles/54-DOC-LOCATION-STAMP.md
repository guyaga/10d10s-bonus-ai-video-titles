# #54 DOC-LOCATION-STAMP · Documentary place/date stamp

> Cinema letterbox bars ease in, an accent bar grows, and a typewriter stamp prints the place name character by character with a block cursor; a transliteration line follows, the GPS coordinates scramble and lock digit by digit, then time and date type out. Optionally a crosshair collapses onto a tracked landmark and hangs a small label on it.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/doc-location-stamp.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_DOC-LOCATION-STAMP.mp4
> Runner: run_style DOC-LOCATION-STAMP · Example: examples/doc-location-stamp/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: documentaries, travel films, true-crime/investigative openers, real-estate location intros, news features, brand films that open in a real place.
- Avoid when: the place is fictional or vague, the shot is shorter than ~4 s (typing needs time), or the video is playful social content (it reads as serious cinema).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#lbt` / `#lbb` | black letterbox bars for `letterbox` aspect (2.39 → 138 px each) | grow from the frame edges |
| `#dscrim` | 1100×560 px radial shadow in the stamp's corner (rgba 0,0,0,.42) | keeps white text readable over bright ground |
| `#stamp .bar` | 5 px accent bar beside the text column | grows from the bottom |
| `.ln.disp` | place name, 62 px display face | typed with a block cursor |
| `.ln.mono` | transliteration and time/date: JetBrains Mono 500, 28 px, +.14em | typed |
| `.ln.coord` | coordinates, mono, accent colour | digits scramble then lock left-to-right |
| `.cur` | block cursor (.5em × .9em, accent) | blinks at 2.2 Hz on the last line when done |
| `#xh` | landmark crosshair: 4 corner brackets (34 px, 3 px accent), dot with a halo, 120 px leader line, label on dark glass | rides a tracked object |

## Timing and motion
Lines type one after another: each line starts when the previous finishes (+ .35 s after the place, + .2 s after the others). Typing speed `cps` = 16 characters/s (sample 15); coordinates take .9 s.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| letterbox bars (scaleY 0→1) | .1 | .90 | power3.inOut | whole clip | — | — |
| corner shadow (fade) | t−.4 | .80 | — | — | — | — |
| accent bar (scaleY 0→1) | t−.25 | .60 | expo.out | — | stamp fades + y 12 at until−.5, .5 s | power2.in |
| place (typed) | t | len/cps | linear per character | — | — | — |
| transliteration (typed) | after the place +.35 | len/cps | — | — | — | — |
| coordinates (scramble → lock) | next | .90 | lock index grows linearly | — | — | — |
| time/date (typed, cursor blinks after) | next | len/cps | — | — | — | — |
| crosshair brackets (from ±150 px, fade) | landmark.t | .55 | expo.out | — | — | — |
| crosshair dot (scale 0→1) | landmark.t+.4 | .35 | back.out(3) | — | — | — |
| leader line (scaleX 0→1) | landmark.t+.55 | .45 | power3.out | — | — | — |
| landmark label (fade, x ±20→0) | landmark.t+.8 | .45 | power3.out | — | — | — |
- Typing, scrambling and the cursor are computed per frame from video time (seek-safe); scramble digits come from a seeded hash, never `Math.random`.
- The signature move: the typewriter with the block cursor and the coordinates scrambling into place: the "classified documentary" feel.

## Typography
- Latin: Manrope 700 place (62 px); JetBrains Mono 500 for transliteration, coordinates and time (28 px, +.14em).
- Hebrew: `pair: "secular"` (default): Secular One place name, typed right-to-left; the transliteration, coordinates and date stay LTR mono. The column aligns right and the accent bar goes to the right side of the text.
- Maximum copy: place ≈ 22 characters (one line in 760 px; `width` sets the column, sample 580), transliteration ≈ 30, coordinates in the form `32.0543° N   34.7516° E`.

## Colour and surface
- Roles: `text` #ffffff, `accent` #ffcf6e (bar, cursor, coordinates, crosshair). Text shadow 0 2 16 rgba(0,0,0,.7).
- Brand swap: accent to a brand colour; keep the typewriter white.

## Layout and safe zones (1920×1080 canvas)
- `corner`: bl (default), br, tl, tr. The stamp sits 120 px from the side and (letterbox bar + 70 px) from the top/bottom: inside the picture, never on the black bars.
- `letterbox`: 2.39 (cinema scope) or 0 to disable. It changes the image: use it only if the whole piece is letterboxed.
- Landmark label: the leader goes left (`side: "L"`) or right from the crosshair.
- Industry convention: location/date stamps appear at the start of a scene, in a lower corner, hold 3–5 s after typing, and never move with the camera (only the landmark marker tracks).
- 9:16: corner "bl", `letterbox: 0`, width ≈ 900.

## What the footage must give you
- Shoot it like this: one take, 6–30 s, an establishing shot of the real place, the stamp's corner calm (sea, sky, road, shadow); slow steady glide.
- Tracking: only for the landmark crosshair: vtrack.py with the landmark, e.g. `{"name": "tower", "desc": "the bell tower of the church"}`.
- Matte: not needed.
- Good footage: aerials, wide exteriors, a street at dawn. Bad: the stamp corner full of detail, handheld shake (the crosshair jitters).

## Build it
### A. With the kit
```bash
python scripts/run_style.py DOC-LOCATION-STAMP --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| place | first line (display face) | required |
| translit / coords / when | optional lines | none |
| t | typing start | .8 |
| cps | characters per second | 16 |
| until | the stamp leaves | none (holds) |
| corner | bl, br, tl, tr | "bl" |
| width | text column px | 760 |
| letterbox | aspect of the bars, 0 = none | 2.39 |
| landmark | {obj, anchor, dx, dy, label, t, side} | none; anchor "c", side "R" |
| track | needed only with landmark | — |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Manrope 700 / 500 (+ JetBrains Mono) |
| colors | {text, accent} | #fff, #ffcf6e |
| sfx | soft ticks while typing, data chatter on coords, lock tick on the landmark | true |
| plate_vol, music, music_vol, name | — | .8, none, .5 |
```json
{
 "clip": "clips/lisbon.mp4",
 "place": "Alfama, Lisbon",
 "translit": "PORTUGAL · OLD TOWN",
 "coords": "38.7118° N   9.1300° W",
 "when": "07:15  ·  02.03.2026",
 "t": 0.9, "corner": "bl", "letterbox": 2.39
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const hash1 = (n) => { const x = Math.sin(n * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); };
const S = [{k: "pl", text: "Alfama, Lisbon", t: .9, d: 14 / 16}, {k: "co", text: "38.7118° N   9.1300° W", t: 2.1, d: .9, coord: true}];
tl.fromTo("#lbt, #lbb", {scaleY: 0}, {scaleY: 1, duration: .9, ease: "power3.inOut"}, .1);
tl.fromTo("#stamp .bar", {scaleY: 0}, {scaleY: 1, duration: .6, ease: "expo.out"}, .65);
window.onPlace = (t) => S.forEach((s) => {           // typing is state derived from time: seek-safe
  let txt = "";
  if (t >= s.t) {
    if (s.coord) { const lock = Math.floor(Math.min(1, (t - s.t) / s.d) * s.text.length), f = Math.floor(t * 24);
      txt = [...s.text].map((c, i) => (i < lock || !/\d/.test(c)) ? c : "0123456789"[Math.floor(hash1(f * 31 + i) * 10)]).join("");
    } else txt = [...s.text].slice(0, Math.floor((t - s.t) * s.text.length / s.d)).join("");
  }
  document.getElementById(s.k).textContent = txt;
});
```

## Adapting it to the user's project
- Content: the real place, real coordinates (from a map), the real date/time of the shoot.
- Language: Hebrew → `"language": "he"`; the place types RTL; everything numeric stays LTR.
- Brand: accent colour only.
- Vertical 9:16: see layout.
- Longer clips: set `until` so the stamp leaves before the next scene.

## Sound
- `soft_tick` (.18) about 7 times per second while typing, `data_chatter` (.12) under the coordinates, `lock_tick` (.35) when the crosshair dot lands.

## Pitfalls and QA checklist
- [ ] Coordinates are real and formatted with ° N/E (or S/W).
- [ ] The stamp sits inside the picture, above the letterbox bar.
- [ ] Hebrew place types right-to-left; numbers LTR.
- [ ] Scramble uses a seeded hash (no Math.random): renders are identical every time.
- [ ] The crosshair sits on the landmark in the tracking preview before rendering.
