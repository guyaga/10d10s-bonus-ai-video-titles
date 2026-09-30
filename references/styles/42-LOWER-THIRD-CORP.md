# #42 LOWER-THIRD-CORP · Corporate name super

> An accent bar grows up, a dark glass plate wipes open, the person's name rises out of a mask line, a rule draws under it and the title slides in; one glint sweeps the frame, then everything exits through the same masks.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/lower-third-corp.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_LOWER-THIRD-CORP.mp4
> Runner: run_style LOWER-THIRD-CORP · Example: examples/lower-third-corp/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: interviews, CEO/founder talking heads, YouTube creators, conference talks, podcast clips, news interviews: any time a speaking person needs a name and a role on screen. Also episode/segment titles (the `tag` chip).
- Avoid when: there is no person on screen (use CHAPTER-MARKERS or DOC-LOCATION-STAMP), the name + title is longer than one line each, or the bottom of the frame is busy (hands, a desk full of objects, a logo on a shirt right where the plate lands).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#glint` | full-height 260 px white-gradient band (10% white) | sweeps once across the whole frame on the FIRST super only |
| `.bar` | 14 px wide accent bar, full plate height | grows from the bottom (`transform-origin:50% 100%`); always on the block's outer edge |
| `.mk` | optional 58×58 accent square with a letter (`logo`) | pinned to the top of the bar |
| `.tx` | the plate: `rgba(10,12,16,.82)` + `backdrop-filter:blur(6px)`, padding 20/36/22 px, min-width 360 px | opens with a `clip-path: inset()` wipe from the bar side |
| `.tg` | optional chip (`tag`) in the accent colour | e.g. "LIVE", "EP 12", "פרק 12" |
| `.nm` inside `.nmw` | the name, 60 px display face | `.nmw` is `overflow:hidden`: the mask line the name rises out of |
| `.rl` | 2 px rule, 55% opacity | draws from the bar side (`scaleX 0→1`) |
| `.tt` inside `.ttw` | the title/role, 30 px body face | second mask line |

## Timing and motion
Times in seconds from the super's `t`. Exit is anchored to `until`.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| bar (scaleY 0→1) | t | .32 | expo.out | to until | scaleY→0 at until−.10, .25 s | power2.in |
| plate wipe (clip-path) | t+.12 | .55 | expo.out | to until | closes at until−.35, .40 s | expo.in |
| tag chip (opacity, y 10→0) | t+.30 | .30 | power3.out | — | — | — |
| name (yPercent 110→0) | t+.28 | .60 | expo.out | to until | yPercent −110 at until−.5, .35 s (stagger .05 with title) | power3.in |
| rule (scaleX 0→1) | t+.42 | .60 | power3.inOut | — | — | — |
| title (yPercent 110→0 + fade) | t+.50 | .55 | expo.out | to until | with the name | power3.in |
| glint (x across frame) | t+.35 | 1.30 | power2.inOut | — | — | first super only |
- Stagger: bar → plate → name → tag → rule → title, all within 0.5 s: reads as one confident build, never as five separate animations.
- Beat/voice sync: land `t` on the first syllable of the person's first sentence (or just after they're in frame); give it at least 3.5 s of hold. Two supers need ≥ 0.6 s gap (sample: 0.6→4.7, 5.3→9.7).
- The signature move: text rising out of a hard mask line (yPercent 110→0 inside an `overflow:hidden` wrapper), with a clip-path plate wipe. No fades on the name: it is revealed, not dissolved.

## Typography
- Latin: Manrope 700 name (60 px, −.01em), Manrope 500 title (30 px, +.02em), tag 18 px +.18em caps.
- Hebrew: `pair: "suez"` (default) = Suez One name + Secular One title. `secular` for a plainer, more UI look. Letter-spacing is forced to 0 in Hebrew. Everything mirrors: bar on the right, plate wipes right-to-left, glint travels right-to-left.
- Maximum copy: name ≈ 22 Latin / 18 Hebrew characters, title ≈ 40 characters, one line each (`white-space:nowrap`: longer copy runs off the plate, it does not wrap). Split a long role into the title and the `tag`.

## Colour and surface
- Palette roles: `bar` accent `#cc2419` (also the tag and logo square), `panel` `rgba(10,12,16,.82)`, `text` `#ffffff`, `sub` `#c9d2de`, `rule` `#ffffff`.
- Brand swap: put the brand colour in `bar` only; keep the panel near-black (it is what guarantees contrast over any footage). For a light brand look use `panel: "rgba(250,250,248,.9)"`, `text: "#111"`, `sub: "#444"`.
- Surface: blur 6 px glass, no stroke, no shadow. The glint is the only highlight.

## Layout and safe zones (1920×1080 canvas)
- Fixed supers: 96 px from the side edge (5% safe margin), baseline at `y` × 1080 (default .8 = 864 px; sample .86). The plate grows upward from that baseline.
- Following supers (`follow`): the block centres on the tracked box's anchor (`anchor` default "b" = bottom) plus `dx`, `dy` (default +40 px below).
- Industry convention: name supers live in the lower third, outside the 5% title-safe margin, on the side OPPOSITE the speaker's gaze/gesturing hand; keep them clear of the chin line.
- 9:16: set `y` ≈ .72 (above platform UI) and keep names ≤ 14 characters.

## What the footage must give you
- Shoot it like this: one take, 6–30 s, chest-up, the person centre or to one side; the lower-left or lower-right quarter calm; 18% of frame height free at the bottom; tripod or very slow push.
- Tracking: none for fixed supers (a clock is derived from the clip). Only if a super must ride a moving person: vtrack.py with `{"name": "host", "desc": "the speaking person's head and shoulders"}`.
- Matte: not needed.
- Good footage: seated interview, desk talk, stage talk with a clean floor. Bad: handheld walk-and-talk (the plate floats over a moving world), a busy desk under the plate, a speaker at the frame edge where the plate should go.

## Build it
### A. With the kit
```bash
python scripts/run_style.py LOWER-THIRD-CORP --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| supers | list of supers (below) | required |
| supers[].name / title | the two lines | name required, title "" |
| supers[].t / until | in time / exit time (s); omit `until` to hold to the end | t required |
| supers[].side | "L" or "R" | "L" (Hebrew: "R") |
| supers[].tag | small chip above the name | none |
| supers[].follow / anchor / dx / dy | ride a tracked object | none / "b" / 0 / 40 |
| language | "he" or "en" | "en" |
| pair | Hebrew pair: suez, secular, karantina, karantina-suez | "suez" |
| fonts | {display, dw, body, bw} override | Manrope 700 / 500 |
| y | baseline of fixed supers (fraction of height) | .8 |
| colors | {bar, panel, text, sub, rule} | see above |
| logo | a letter in a square on the bar | none |
| sfx | whoosh + click per super | true |
| music, music_vol, vo, vo_vol | audio beds | none, .5, none, 1 |
| plate_vol | the clip's own audio | .7 |
| track | only needed with `follow` | derived clock |
| name | project folder name | lower-third-corp |
```json
{
 "name": "acme-interview",
 "clip": "clips/interview.mp4",
 "language": "en",
 "logo": "A",
 "colors": {"bar": "#0057ff"},
 "supers": [
  {"name": "Maya Stein", "title": "CEO, Acme Robotics", "t": 0.8, "until": 5.0},
  {"tag": "PART 2", "name": "Why robots need hands", "title": "Three lessons from the factory floor", "t": 12.0, "until": 16.5}
 ]
}
```
### B. The core move in HyperFrames/GSAP
```js
// markup: .lt > .in > .bar + .tx > (.nmw > .nm) + .rl + (.ttw > .tt) ; .nmw,.ttw {overflow:hidden}
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const t = 0.8, until = 5.0, fromLeft = true;
const shut = fromLeft ? "inset(0 100% 0 0)" : "inset(0 0 0 100%)";
tl.set(".bar", {scaleY: 0}, 0);
tl.fromTo(".bar", {scaleY: 0}, {scaleY: 1, duration: .32, ease: "expo.out"}, t);
tl.fromTo(".tx", {clipPath: shut}, {clipPath: "inset(0 0% 0 0%)", duration: .55, ease: "expo.out"}, t + .12);
tl.fromTo(".nm", {yPercent: 110}, {yPercent: 0, duration: .6, ease: "expo.out"}, t + .28);
tl.fromTo(".rl", {scaleX: 0}, {scaleX: 1, duration: .6, ease: "power3.inOut"}, t + .42);
tl.fromTo(".tt", {yPercent: 110, opacity: 0}, {yPercent: 0, opacity: 1, duration: .55, ease: "expo.out"}, t + .5);
tl.fromTo("#glint", {x: -300}, {x: 1980, duration: 1.3, ease: "power2.inOut"}, t + .35);
// exit through the same masks
tl.to(".nm, .tt", {yPercent: -110, duration: .35, ease: "power3.in", stagger: .05}, until - .5);
tl.to(".tx", {clipPath: shut, duration: .4, ease: "expo.in"}, until - .35);
tl.to(".bar", {scaleY: 0, duration: .25, ease: "power2.in"}, until - .1);
```

## Adapting it to the user's project
- Content: one super per new speaker; a second super later can carry a segment title with a `tag`.
- Language: Hebrew → `"language": "he"`, default pair suez; everything mirrors automatically. Use real names and roles from the user; don't invent.
- Brand: accent to `bar`, optional `logo` letter; keep the panel dark.
- Vertical 9:16: `y` ≈ .72, short names, consider `side` on the open side of the speaker.
- Longer or shorter clips: holds under 3 s feel like a glitch; for a 60 s interview show the super once at the start and again (shorter) after a cut.

## Sound
- `ar_whoosh` at t (vol .5) and `soft_click` at t+.3 (vol .35) per super. Keep it under the voice; switch off with `"sfx": false` for serious or news content.

## Pitfalls and QA checklist
- [ ] Name and title fit on one line each (nowrap): nothing runs past the plate.
- [ ] The plate never covers the chin or a gesturing hand.
- [ ] Hebrew: plate wipes from the right, bar on the right, glint right-to-left.
- [ ] Animate masks with yPercent inside overflow:hidden wrappers; never animate `left/top` (fails the HyperFrames pixel-snap check); for offsets on elements GSAP also moves use xPercent/yPercent, not a CSS transform GSAP will overwrite.
- [ ] Contrast: the first ~0.5 s of the wipe may flag in QA; the held frame must pass.
- [ ] ≥ 3.5 s hold; ≥ 0.6 s between supers.
