# #50 END-SCREEN · YouTube-style end card

> Over the last seconds, a dark scrim wipes across the free side with an angled edge, a WATCH NEXT heading unmasks, two video tiles flip up with a slow Ken Burns, play buttons and duration badges, and a round channel avatar pops inside a spinning dashed ring with a SUBSCRIBE label. The presenter stays visible on the other side.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/end-screen.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_END-SCREEN.mp4
> Runner: run_style END-SCREEN · Example: examples/end-screen/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: YouTube video endings, course lessons ("next lesson"), podcast episode outros, series episodes, any "watch next" hand-off with the host still on screen.
- Avoid when: the last shot has no free side (the scrim covers ~60% of the frame), or the platform has no clickable end elements and you need the viewer to act (then a single SOCIAL-CTA is stronger).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#scrim` | 1140 px wide dark panel (`scrim` #0b0d12 → 85% at the edge), angled edge `polygon(0 0,100% 0,86% 100%,0 100%)` | on `side` L or R |
| `#hd` | heading "WATCH NEXT" / "הסרטון הבא", 54 px, +.18em, in a mask line | at top 120 px |
| `.tile` | a video tile: thumbnail (`tile_w` px wide, 16:9, radius 16, 2 px white-14% border, shadow), duration badge, round play button, 30 px title | thumbnails are frames extracted with ffmpeg from any clip at `at` s |
| `#av` | 220 px round avatar cropped from a frame (`x`, `y` = face centre 0–1, `zoom`), dashed accent ring (236 px), SUBSCRIBE pill | at top 650 px |

## Timing and motion
T = `t` (start of the end card).
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| scrim wipe (clip-path polygon) | T | .70 | expo.inOut | to the end | — | — |
| heading (yPercent 110→0) | T+.35 | .60 | expo.out | — | — | — |
| tile i flip up (rotateX 75→0, y 60→0, fade) | T+.5 + i×.14 | .80 | expo.out | — | — | — |
| thumbnail Ken Burns (scale 1→1.12) | T+.5 | 5.0 | linear | — | — | — |
| play button (scale 0→1) | T+1.0 + i×.14 | .40 | back.out(2.5) | — | — | — |
| tile float (y −8, yoyo, 2 repeats) | T+1.4 + i×.3 | 1.4 each | sine.inOut | — | — | — |
| avatar (scale 0→1) | T+.9 | .60 | back.out(2.2) | — | — | — |
| ring (fade + scale .7→1), then spin 120° | T+1.3 / T+1.35 | .60 / 5.0 | back.out(2) / linear | — | — | — |
| SUBSCRIBE label (fade, x ∓20→0) | T+1.3 | .45 | power3.out | — | — | — |
- The ring appears only after the avatar (an empty dashed circle first reads as a stray graphic). A dashed stroke can't be drawn on with dashoffset (the dash pattern repeats), so it fades/scales in, then spins.
- The signature move: the angled scrim wipe and the tiles flipping up in perspective, then floating: alive but calm.

## Typography
- Latin: Manrope 700 heading (54 px, +.18em), tile titles (30 px), badges, label (32 px).
- Hebrew: `pair: "secular"` (default): Secular One. Heading "הסרטון הבא", label "הירשמו". The card is RTL; duration badges sit bottom-left and stay LTR.
- Maximum copy: tile titles ≈ 30 characters (two lines max at 380–460 px).

## Colour and surface
- Roles: `scrim` #0b0d12, `accent` #ff0033 (ring, label), `text` #ffffff, `sub` #aab3bf.
- Brand swap: accent = brand colour; keep the scrim near-black so thumbnails pop.

## Layout and safe zones (1920×1080 canvas)
- Content block: 110 px from the side, top 120, width 980; tiles `tile_w` (460 default; sample 380) with 34 px gap; avatar at top 650.
- Industry convention (YouTube): end-screen elements can only be added in the last 5–20 s of a video, and the creator places them in YouTube Studio over the picture: video/playlist tiles are 16:9, the subscribe element is a round channel icon. Start this card ≥ 5 s before the end (sample: last 4.8 s of a 10 s clip, as a demo), and after upload put YouTube's real elements exactly over these tiles and the avatar so the design and the clickable areas match. Keep the presenter's face out of the element zone.
- 9:16 (Shorts): YouTube Shorts have no end screens; use SOCIAL-CTA instead.

## What the footage must give you
- Shoot it like this: one take for the last 6–20 s, the presenter on one side (the side not covered), still enough to hold ~5 s; tripod.
- Tracking: none. Matte: not needed.
- Thumbnails: any of the user's other videos or clips (`src` + `at` second); the avatar is a frame from any clip with the face (`x`, `y` = the face centre as a fraction of the frame, `zoom` ≈ 3–3.5 for a medium shot).
- Good footage: presenter pointing or glancing to the card side. Bad: the presenter walking into the card side; a cut in the last 5 s.

## Build it
### A. With the kit
```bash
python scripts/run_style.py END-SCREEN --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| tiles[] | {src, at, title, dur} (two work best) | required; at 2 |
| t | end-card start (s) | 5.6 |
| side | which side the card covers | "L" |
| heading | heading text | "WATCH NEXT" / "הסרטון הבא" |
| tile_w | tile width px | 460 |
| avatar | {src, at, x, y, zoom, label} | none; at 1, x .5, y .5, zoom 3, label SUBSCRIBE/הירשמו |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Manrope 700 / 500 |
| colors | {scrim, accent, text, sub} | see above |
| sfx | whoosh + logo hit (+ pop for the avatar) | true |
| music, music_vol, plate_vol, name | — | none, .5, .85 |
```json
{
 "clip": "clips/outro.mp4",
 "t": 12.0, "side": "L", "tile_w": 420,
 "tiles": [{"src": "clips/ep41.mp4", "at": 30, "title": "Ep. 41 · Building in public", "dur": "38:05"},
           {"src": "clips/ep40.mp4", "at": 12, "title": "Ep. 40 · The first hire", "dur": "41:22"}],
 "avatar": {"src": "clips/outro.mp4", "at": 2, "x": 0.66, "y": 0.28, "zoom": 3.2}
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const T = 12.0;
tl.set("#es, #scrim", {autoAlpha: 0}, 0); tl.set("#es, #scrim", {autoAlpha: 1}, T - .01);
tl.fromTo("#scrim", {clipPath: "polygon(0 0,0% 0,0% 100%,0 100%)"}, {clipPath: "polygon(0 0,100% 0,86% 100%,0 100%)", duration: .7, ease: "expo.inOut"}, T);
tl.fromTo("#hd", {yPercent: 110}, {yPercent: 0, duration: .6, ease: "expo.out"}, T + .35);
[0, 1].forEach((i) => {
  tl.fromTo(`#t${i}`, {rotateX: 75, opacity: 0, y: 60}, {rotateX: 0, opacity: 1, y: 0, duration: .8, ease: "expo.out"}, T + .5 + i * .14); // parent has perspective
  tl.fromTo(`#t${i} img`, {scale: 1}, {scale: 1.12, duration: 5, ease: "none"}, T + .5);
});
tl.fromTo("#av .ph", {scale: 0}, {scale: 1, duration: .6, ease: "back.out(2.2)"}, T + .9);
tl.set("#av .ring", {opacity: 0, transformOrigin: "50% 50%"}, 0);
tl.fromTo("#av .ring", {opacity: 0, scale: .7}, {opacity: 1, scale: 1, duration: .6, ease: "back.out(2)", immediateRender: false}, T + 1.3);
tl.fromTo("#av .ring", {rotate: 0}, {rotate: 120, duration: 5, ease: "none"}, T + 1.35);
```

## Adapting it to the user's project
- Content: their two best next videos; real titles and durations.
- Language: Hebrew → `"language": "he"`; default Hebrew heading/label.
- Brand: accent = brand colour.
- Vertical 9:16: not applicable to Shorts (see layout).
- Longer clips: set `t` to (end − 5…20 s).

## Sound
- `ui_whoosh` (.5) at T, `logo_hit` (.4) at T+.5, `ui_pop` (.4) when the avatar pops. Duck or fade the presenter's voice at the end.

## Pitfalls and QA checklist
- [ ] The card starts ≥ 5 s before the end (YouTube end-screen window).
- [ ] The presenter's audio doesn't end mid-word at the last frame: the kit can't fade plate audio, so fade the last ~1.2 s after rendering (`ffmpeg -af afade=t=out:st=<end-1.2>:d=1.2`), or end the clip on a finished sentence.
- [ ] Avatar crop is centred on the face (`x`, `y`, `zoom`).
- [ ] Dashed ring appears after the avatar and spins; never drawn with dashoffset.
- [ ] Tiles and avatar don't overlap the presenter's face.
