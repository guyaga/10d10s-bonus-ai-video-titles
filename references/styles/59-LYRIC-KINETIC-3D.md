# #59 LYRIC-KINETIC-3D · Music-video lyrics in 3D space

> Every lyric word flies in from depth (translateZ + rotation + blur) exactly on its sung syllable; big condensed key words and small italic connective words build a layered composition, chosen words live behind the performer, the front and back planes drift in opposite directions for parallax, and each phrase leaves by falling back into depth.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/lyric-kinetic-3d.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_LYRIC-KINETIC-3D.mp4
> Runner: run_style LYRIC-KINETIC-3D · Example: examples/lyric-kinetic-3d/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: lyric videos, music promos, artist social clips, spoken-word/poetry, emotional brand anthems, trailer taglines sung or spoken with rhythm.
- Avoid when: the words are dense speech (use KINETIC-KARAOKE or VIRAL-CAPTIONS), there are no clean timings, or the performer fills the frame so no word can sit off the face.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#pb` (back plane) | words with `layer: "back"` | behind the performer (needs a matte) |
| matte | the performer cut out (webm with alpha) | laid over the back plane |
| `#pf` (front plane) | all other words | in front of everything |
| `.big` | condensed display words (Anton, uppercase), text shadow | key words, 200–400 px |
| `.script` | small italic serif connective words (Cormorant Garamond 600 italic) | "in", "the", "of the" |
| `.outline` | stroked display words (3 px glow-colour stroke, near-transparent fill) | echoes, repeated words |
| `.glow` | neon glow (#ff3fb4, 22 px + 60 px) added to any word | one or two per clip |
Both planes have `perspective: 1500px`; each word sits in a `.pin` at its (x, y) anchor.

## Timing and motion
Each word's `t` is its sung onset.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| big/outline word (z −900→0, rotateX 55→0, rotateY ±12→0, blur 14→0, fade) | t−.06 | .62 | expo.out | to the phrase exit | z −700, rotateX −30, blur 12, fade, at exit−.45 (+ n%3 × .04 jitter) | power2.in |
| big word settle (scale 1.06→1) | t+.30 | .45 | power2.out | — | — | — |
| script word (z −520→0, rotateY ±38→0, rotateX 10→0, blur 10→0) | t−.06 | .50 | power3.out | — | same exit | — |
| front plane drift (rotationY −drift/2 → +drift/2) | 0 | clip duration | linear | — | — | — |
| back plane drift (rotationY +drift/2 → −drift/2, scale 1.02→1.06) | 0 | clip duration | linear | — | — | — |
- Words alternate their entry direction (odd/even), mirrored in Hebrew.
- `exits` groups words by `phrase`: all words of a phrase fall back together (null = hold to the end).
- The signature move: words arriving from deep space on the syllable, with a tiny scale overshoot on the heavy words, and a key word hidden behind the singer (depth).

## Typography
- Latin: Anton 400 (big/outline, uppercase, +.02em), Cormorant Garamond 600 italic (script).
- Hebrew: `pair: "karantina-suez"` (default) = Karantina 700 big words + Suez One script words (upright, no italic; no uppercase transform).
- Sizes are set per word (`size` px). Typical: big 250–400, script 90–120. One or two words per line of the song on screen at once.

## Colour and surface
- `colors`: text #ffffff, glow #ff3fb4, outline rgba(255,63,180,.85). Match the glow to the stage lighting (magenta, cyan, amber).
- No panels. Readability comes from size, shadow and placing words on calm areas.

## Layout and safe zones (1920×1080 canvas)
- Every word is placed by hand: `x`, `y` (top of the word) and `align` (left/center/right edge at x). Build a composition per phrase: one big word, two or three small connective words around it.
- Keep front words in the free columns left/right and across the chest; never on the face. Back words can cross behind the head (that's the point).
- `tight: true` marks deliberate tight lockups (e.g. "of the" stacked over LIGHT) so the overlap check allows them.
- Industry convention: lyric words land on the vocal onset (not the beat) and leave before the next line starts; the hook word gets the biggest size and the glow.
- 9:16: stack vertically above and below the face; sizes ≈ 70%.

## What the footage must give you
- Shoot it like this: one take, a performer singing to camera, medium shot, moody stage light, free columns left and right; slow orbit or push (the planes drift with it).
- Word timings: transcribe the vocal with word timestamps (Gemini transcription, or word_times.py for TTS); the sample's came from a Gemini transcription of the clip's own singing.
- Matte (for back words): `npx hyperframes remove-background plate.mp4 -o mattes/singer_alpha.webm`. Without a matte, back words automatically move to the front.
- Good footage: a singer in front of a dark stage, a rapper in a clean room, a speaker with dramatic light. Bad: busy crowds behind, fast cuts, the face in the middle of every free space.

## Build it
### A. With the kit
```bash
npx hyperframes remove-background clips/singer.mp4 -o mattes/singer_alpha.webm
python scripts/run_style.py LYRIC-KINETIC-3D --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| words[] | {w, t, x, y, size, kind big/script/outline, layer front/back, align, phrase, glow, tight} | required; size 200, kind big, layer front, align left, phrase 0 |
| exits | {"phrase": exit time or null} | {} (hold) |
| matte | subject matte webm | needed for back words |
| drift | plane rotation over the clip (degrees) | 5 |
| language / pair | he/en; Hebrew pair | en / "karantina-suez" |
| fonts | override | Anton 400 / Cormorant Garamond 600 |
| colors | {text, glow, outline} | see above |
| plate_vol | the song | 1.0 |
| music, music_vol, name | — | none, .5 |
There are no built-in sound effects: the song is the soundtrack.
```json
{
 "clip": "clips/verse.mp4", "matte": "mattes/verse_alpha.webm", "drift": 6,
 "words": [
  {"w": "Hold", "t": 0.5, "x": 120, "y": 420, "size": 110, "kind": "script", "phrase": 0},
  {"w": "ON", "t": 0.9, "x": 960, "y": 120, "size": 380, "kind": "big", "align": "center", "layer": "back", "phrase": 0},
  {"w": "TONIGHT", "t": 1.8, "x": 1820, "y": 620, "size": 230, "kind": "big", "align": "right", "glow": true, "phrase": 0}
 ],
 "exits": {"0": 4.2}
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const DUR = 10, drift = 6, W = [{i: 0, t: .5, kind: "script", center: false}, {i: 1, t: .9, kind: "big", center: true}], EXIT = 4.2;
tl.fromTo("#pf", {rotationY: -drift / 2}, {rotationY: drift / 2, duration: DUR, ease: "none"}, 0);               // parallax planes
tl.fromTo("#pb", {rotationY: drift / 2, scale: 1.02}, {rotationY: -drift / 2, scale: 1.06, duration: DUR, ease: "none"}, 0);
W.forEach((w, n) => {
  const id = "#w" + w.i, cx = w.center ? -50 : 0, dir = n % 2 ? 1 : -1;   // centre with xPercent INSIDE the tween
  const from = w.kind === "script"
    ? {opacity: 0, z: -520, rotationY: 38 * dir, rotationX: 10, xPercent: cx, filter: "blur(10px)"}
    : {opacity: 0, z: -900, rotationX: 55, rotationY: 12 * dir, xPercent: cx, filter: "blur(14px)"};
  tl.fromTo(id, from, {opacity: 1, z: 0, rotationX: 0, rotationY: 0, xPercent: cx, filter: "blur(0px)",
    duration: w.kind === "script" ? .5 : .62, ease: w.kind === "script" ? "power3.out" : "expo.out"}, w.t - .06);
  if (w.kind !== "script") tl.fromTo(id, {scale: 1.06}, {scale: 1, duration: .45, ease: "power2.out"}, w.t + .3);
  tl.to(id, {opacity: 0, z: -700, rotationX: -30, filter: "blur(12px)", duration: .45, ease: "power2.in"}, EXIT - .45 + (n % 3) * .04);
});
```

## Adapting it to the user's project
- Content: the real lyric, exact timings; the hook word big and glowing.
- Language: Hebrew → `"language": "he"` (Karantina + Suez One, entry directions mirror).
- Brand: glow colour from the stage light or the artist's palette.
- Vertical 9:16: see layout.
- Longer clips: one phrase group per line; set each phrase's exit before the next line.

## Sound
- None added: the song carries it (`plate_vol` 1.0). Add a subtle `music` bed only if the plate has no song.

## Pitfalls and QA checklist
- [ ] Every word lands on its syllable (± 60 ms).
- [ ] No front word on the face; back words only with a clean matte.
- [ ] Centred words use `xPercent: -50` inside the GSAP tween (a CSS translate would be overwritten by GSAP's 3D transform).
- [ ] Phrase exits clear the screen before the next line.
- [ ] Deliberate overlaps are marked `tight` (so the layout check passes only for intended lockups).
