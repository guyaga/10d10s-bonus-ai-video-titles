# #07 KINETIC-KARAOKE · Karaoke captions

> Voice-synced captions at the bottom, 2–3 words at a time, the word being spoken lighting up in an accent pill; on top,
> kinetic headlines and punch-zooms on the key words.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/kinetic-karaoke.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E9_lumen_lens_smart_glasses_SX.mp4
> Runner: run_ad (adkit `captions` + `punch` + `kine`/`tape`) · Example: examples/E6_sneaker_sx.py (it has all three)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: VO- or talk-driven reels, explainers, creator content, accessibility (sound-off viewing), Hebrew social.
- Avoid when: there is no speech (use #05/#06); the bottom fifth of the frame holds the important action; premium
  brand films (captions read as social content).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate + punch | the clip, scaled 1.1 → 1 on key words | `punch` scales `#plate` and `#matte` together |
| Kinetic headlines | `kine` word stomps, top/middle | see #05 |
| Tape lines | `tape` strips for the claim of each section | see #06 |
| Caption bar | `#cap`, centred, 150 px from the bottom, RTL | one caption group visible at a time |
| Caption group | 1–3 words, Secular One 66 px, white with a 9 px black stroke | the active word gets the accent pill |
| Flash cards (optional) | full-frame word on the biggest beats | see #08 |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Caption group | its first word's onset | shows instantly; y 30 → 0 and scale 0.9 → 1 in 0.14 s | back.out(2.5) | until min(next group − 0.02 s, last word + 1.0 s, element `end`) | cut (instant) | — |
| Active word pill | the word's onset | class `cw on` (accent pill); scale 1.28 → 1 in 0.16 s | back.out(3) | until the next word's onset (or the group's end) | back to plain white | — |
| Punch zoom | each time in `times` | scale `amt` (1.1) → 1 in `dur` (0.35 s) on plate + matte | power3.out | — | — | — |
| Kine / tape companions | see #05 / #06 | | | | | |

- Grouping rules (in the builder): a group closes at `max` words (default 3) or after a word ending in `.` `,` `?` `!`;
  a number is never the last word of a group (it is glued to the next word, so "6 שעות" stays together); a group never
  lingers more than 1.0 s after its last word.
- Voice sync: the words list comes straight from `scripts/word_times.py` (`[{w, t}]`).
- The signature move: **the moving pill**. Only one word is highlighted at a time and it pops (1.28 → 1) the instant
  it's spoken; the rest of the group stays white-on-black-stroke, so the eye follows the voice.

## Typography
- Captions: Secular One 400, 66 px, line-height 1.1, gap .28em between words, white fill with a 9 px black stroke
  (`paint-order: stroke fill`) and a 0 6px 18px 60 % black shadow. The active word: accent background, text `--tacc`
  (ink or white by the accent's luminance), no stroke, padding 0 .14em, radius 6 px, 6 px 6 px 0 45 % black shadow.
- Hebrew: the caption bar is `direction: rtl`; the same bar works for English (Secular One has Latin). Headlines in
  Karantina 700 (see #05); strips in Karantina (see #06). Prices ש״ח.
- Max copy: 3 words per group, ~24 characters; long words (> 10 letters) should be their own group (`max: 2` or
  punctuation).

## Colour and surface
- Palette of the sample (E9): acc `#2ec4a6`, ink `#0d1b1e`, lt `#ffffff`, panel `rgba(10,22,24,.88)`, sub `#d6f8f0`.
  The accent is the pill; choose an accent that contrasts with both black stroke text and the footage.

## Layout and safe zones (1920×1080 canvas)
- `#cap` spans the width, bottom 150 px, groups centred; the bottom 22 % of the frame must stay calm.
- Headlines in the top/middle band away from the captions; punch-zooms need 10 % extra image around the frame edges
  (the plate scales up, so keep key detail away from the edges at those moments).
- 9:16: captions centred at the bottom survive a centre crop if a group is ≤ 600 px (3 short words).

## What the footage must give you
- Shoot it like this: cuts OK (max 5), 12–24 s · subject in the upper two thirds · 22 % free at the bottom ·
  stabilised; punch-zooms are added in post · no tracking needed.
- Tracking: none for captions (only for companion tags/boxes).
- Matte: no (punch scales the matte too if one exists).
- Good: talking head or subject high in frame. Bad: hands/product at the very bottom during speech.

## Build it
### A. With the kit
```bash
python scripts/vo_take2.py MY_AD specs/MY_AD_lines.json he     # VO (or bring a recorded one)
python scripts/word_times.py MY_AD specs/MY_AD_lines.json he   # -> tools/MY_AD_he_words.json [{w, t}]
python scripts/run_ad.py MY_AD --spec specs/MY_AD.py --render
```
| Key | Meaning | Default |
|---|---|---|
| `captions.words` | `[{w, t}]` from word_times.py | required |
| `captions.max` | words per group | 3 |
| `captions.t`, `captions.end` | first/last moment captions may show | 0 / 999 |
| `punch.times`, `punch.amt`, `punch.dur` | zoom hits | –, 1.1, 0.35 s |
| theme, palette, vo / vo_name, music, css | see #05 | |

A minimal spec:
```python
import json
from pathlib import Path
WORDS = json.loads(Path("tools/MY_AD_he_words.json").read_text(encoding="utf-8"))
SPEC = {"theme": "he_bold",
 "palette": {"acc": "#2ec4a6", "ink": "#0d1b1e", "lt": "#ffffff", "panel": "rgba(10,22,24,.88)", "sub": "#d6f8f0"},
 "clip": "clips/my_talk.mp4", "vo": "shared/sfx/MY_AD_he_vo.mp3", "css": "#flash{display:none}",
 "elements": [
  {"type": "captions", "words": [{"w": x["w"], "t": x["t"]} for x in WORDS], "max": 3, "t": 0.3, "end": 15.0},
  {"type": "punch", "times": [0.95, 5.8], "amt": 1.1}]}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```css
#cap{position:absolute;left:0;right:0;bottom:150px;display:flex;justify-content:center;direction:rtl}
.cg{position:absolute;display:flex;gap:.28em;font:400 66px/1.1 "Secular One";opacity:0}
.cw{display:inline-block;color:#fff;-webkit-text-stroke:9px #000;paint-order:stroke fill;text-shadow:0 6px 18px rgba(0,0,0,.6)}
.cw.on{color:#0d1b1e;background:#2ec4a6;-webkit-text-stroke:0;padding:0 .14em;border-radius:6px;box-shadow:6px 6px 0 rgba(0,0,0,.45)}
```
```js
GROUPS.forEach((g, gi) => {                                  // g = [{w, t}], built by the grouping rules above
  const id = `#g${gi}`, start = g[0].t;
  const end = Math.min(gi + 1 < GROUPS.length ? GROUPS[gi + 1][0].t - .02 : 999, g[g.length - 1].t + 1.0);
  tl.set(id, {opacity: 1}, start); tl.set(id, {opacity: 0}, end);
  tl.fromTo(id, {y: 30, scale: .9}, {y: 0, scale: 1, duration: .14, ease: "back.out(2.5)", immediateRender: false}, start);
  g.forEach((w, wi) => {
    const nxt = wi + 1 < g.length ? g[wi + 1].t : end;
    tl.set(`${id}w${wi}`, {className: "cw on"}, w.t); tl.set(`${id}w${wi}`, {className: "cw"}, nxt);
    tl.fromTo(`${id}w${wi}`, {scale: 1.28}, {scale: 1, duration: .16, ease: "back.out(3)", immediateRender: false}, w.t);
  });
});
PUNCH.forEach((pt) => tl.fromTo(["#plate", "#matte"], {scale: 1.1}, {scale: 1, duration: .35, ease: "power3.out", immediateRender: false}, pt));
```

## Adapting it to the user's project
- Content: the words are the real VO transcript; fix word_times onsets by ear on 2–3 words before rendering.
- Language: Hebrew and English both work with Secular One; for English-only you may swap the caption font in css.
- Brand: the pill colour = brand accent; stroke stays black.
- Vertical 9:16: `max: 2` for narrow groups.
- Longer or shorter clips: captions scale with the VO; punches 1 per 2–3 s at most.

## Sound
- No sound cues of its own; the VO carries it. Kine hits add thumps (0.55); music under VO around 0.45–0.6.

## Pitfalls and QA checklist
- [ ] Onsets match the VO (a pill that lights before the word is spoken reads as a bug).
- [ ] Numbers never end a group ("6" alone on screen); the builder glues them, check the render.
- [ ] Groups vanish ≤ 1 s after their last word (no stale captions over silence).
- [ ] Nothing important in the bottom 22 %; punch-zooms don't crop a face at the frame edge.
- [ ] Frames checked + `scripts/qa.py` "ship".
