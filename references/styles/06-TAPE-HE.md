# #06 TAPE-HE · Hebrew tape strips

> Hebrew slogans printed on slightly rotated highlight-tape strips (ink, accent or light) that wipe in right-to-left and
> slam, one strip per line, readable over any footage.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/tape-he.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E4_firelink_through_the_smoke_HK.mp4
> Runner: run_ad (adkit `tape`, theme `he_bold`) · Example: examples/E4_fire_hk.py

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: Hebrew slogans, claims, stats and CTAs over busy or dark footage (fire, city, night, crowds), phone-first
  social ads; the fix for "Hebrew text over footage is unreadable".
- Avoid when: the piece is premium/quiet (tape is a street/social device); you need more than 3 strips at once (it
  becomes a collage); the footage is already graphic-heavy.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | plate 0.45 in the sample |
| Scrim (optional) | bottom 420 px gradient, transparent → `rgba(0,0,0,.62)` | `scrim: true` on a tape element |
| Tape group | a flex column of strips, 12 px gap, aligned right / left / centre | one element = 1–3 lines |
| Strip | a `span` with a solid fill (ink / accent / light), Karantina 700 text, rotated −2° | 9 px 9 px 0 `rgba(0,0,0,.38)` hard shadow |
| Companions in the sample | kine headlines, counters, box + tag, chip, voice meter, tape lockup | all adkit elements |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Strip j of a tape | line `t`, else element `t` + j × 0.18 s | clip-path `inset(0 0 0 100%)` → `inset(0 0 0 0%)` in 0.28 s (the strip unrolls from the right edge leftward) | expo.out | until element `end` | whole group fades 0.12 s ending at `end` | linear |
| Strip text | strip t + 0.12 | opacity 0 → 1, scale 1.35 → 1 in 0.18 s | power4.out | with strip | with group | — |
| Hit (`hit: true`) | strip t + 0.12 | frame shake, amount 0.5 + thump | — | — | — | — |
| Scrim | element t − 0.1 | opacity → 1 in 0.4 s | default | stays | — | — |
| Tape lockup (end card) | `t` | brand strip wipes 0.3 s, text pops at +0.03, shake 0.45 at +0.12; line strip at +0.3 | expo.out / power4.out | to the end | — | — |

- Stagger: 0.18 s between strips by default; in VO-driven pieces set each line's `t` to its word onset.
- The signature move: **the unroll + slam**. The strip is revealed right-to-left (reading direction) like tape pulled
  off a roll, and its word lands 0.12 s later with a scale-down pop, so each line reads as two micro-hits.

## Typography
- Hebrew: Karantina 700 on every strip (line-height 1.08, padding `.06em .34em .14em`); `font: "big"` → line-height .95,
  padding `.02em .3em .04em` for the loud final strip. Labels around it (counters, tags, chip) in Secular One. Suez One
  only if a strip must feel premium (override with css). RTL: the group has `direction: rtl`; align `r` anchors the
  group's right edge at `x`. Numbers glued to their word ("640 מעלות", "7% חמצן."). Prices ש״ח.
- Sizes: strips 58–96 px (default 64); lockup brand 118 px, line 58 px.
- Max copy: ≤ 4 words per strip, ≤ 3 strips per group; one accent strip per group.

## Colour and surface
- Strip styles: `ink` = `var(--ink)` fill + `var(--lt)` text; `acc` = `var(--acc)` fill + auto text colour
  (`--tacc` = ink when the accent's luminance > 0.22, else white); `lt` = light fill + ink text.
- Sample palette: acc `#ff7a1a`, ink `#0c0806`, lt `#fff4ea`, panel `rgba(12,8,6,.82)`, sub `#ffd3b0`. Brand: set
  `acc` to the brand colour; the auto text colour keeps it legible.
- Rotation −2° by default (`rot` per element or per line); hard shadow 9 px 9 px 0 at 38 % black.

## Layout and safe zones (1920×1080 canvas)
- `x`, `y` = the group's anchor: align `r` → right edge at x (sample 1840 = 80 px from the edge); `c` → centred on x;
  `l` → left edge at x. `y` is the top of the group.
- Keep groups in the lower third (y 600–800) over a calm area, or top band; never across a face.
- 9:16: centre-aligned groups (`align: "c"`, x 960) with strips ≤ 560 px survive the centre crop.

## What the footage must give you
- Shoot it like this: cuts OK (max 5), 12–24 s · subject off-centre or centred with a calm lower third · 25 % free at the
  bottom · steady; cut-blocks welcome.
- Tracking: optional (only for tags/boxes on subjects).
- Matte: no (only for a behind-word companion).
- Good: dark or mid-tone lower third. Bad: nothing, tape reads over almost anything; just keep it off faces.

## Build it
### A. With the kit
```bash
python scripts/run_ad.py MY_AD --spec specs/MY_AD.py --render
```
| Key (tape element) | Meaning | Default |
|---|---|---|
| x, y | anchor (see Layout) | required |
| align | `r` / `l` / `c` | `r` |
| t, end | start / end of the group | 0 / to the end |
| rot | rotation of every strip in degrees | −2 |
| scrim | fade in the bottom gradient | false |
| lines | `[{text, style ink/acc/lt, size, t, rot, w 700, font big, hit}]` | style ink, size 64 |
Other keys: theme `he_bold`, palette, clip, track, music, vo, css (see #05).

A minimal spec:
```python
SPEC = {"theme": "he_bold",
 "palette": {"acc": "#ff7a1a", "ink": "#0c0806", "lt": "#fff4ea", "panel": "rgba(12,8,6,.82)", "sub": "#ffd3b0"},
 "clip": "clips/my_clip.mp4", "music": "shared/sfx/my_music.mp3",
 "elements": [
  {"type": "tape", "x": 960, "y": 760, "align": "c", "t": 1.0, "end": 4.0, "scrim": True,
   "lines": [{"text": "קפה אמיתי", "style": "ink", "size": 62}, {"text": "מ-6 בבוקר", "style": "acc", "size": 74, "hit": True}]},
  {"type": "tape", "x": 1840, "y": 470, "align": "r", "t": 5.0,
   "lines": [{"text": "דיזנגוף 120", "style": "lt", "size": 64}, {"text": "בואו.", "style": "acc", "size": 96, "font": "big", "hit": True}]},
  {"type": "lockup", "brand": "MY CAFE", "line": "פתוח עכשיו", "t": 6.5}]}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```css
.tp{position:absolute;display:flex;flex-direction:column;gap:12px;direction:rtl;align-items:flex-end}
.tl{display:block;width:max-content;padding:.06em .34em .14em;font:700 64px/1.08 Karantina;box-shadow:9px 9px 0 rgba(0,0,0,.38);transform:rotate(-2deg)}
.tl.ink{background:#0c0806;color:#fff4ea} .tl.acc{background:#ff7a1a;color:#0c0806}
.tl b{display:inline-block;font-weight:inherit}
```
```js
LINES.forEach(([id, t, hit], j) => {                       // t = element t + j * .18, or the line's own t
  tl.fromTo(`#${id}`, {clipPath: "inset(0 0 0 100%)"}, {clipPath: "inset(0 0 0 0%)", duration: .28, ease: "expo.out"}, t);
  tl.fromTo(`#${id} b`, {opacity: 0, scale: 1.35}, {opacity: 1, scale: 1, duration: .18, ease: "power4.out"}, t + .12);
  if (hit) shake(t + .12, .5);
});
tl.to("#scrim", {opacity: 1, duration: .4}, T0 - .1);        // optional bottom gradient
tl.to("#grp", {opacity: 0, duration: .12}, END - .12);
```

## Adapting it to the user's project
- Content: split the slogan into 2 strips: a neutral set-up (ink) and the punch (accent). One number per strip max.
- Language: Hebrew-first; for English copy use the same element (Karantina has Latin) or override the font in css.
- Brand: `acc` = brand colour, `ink` = brand dark; keep one accent strip per group.
- Vertical 9:16: centre-aligned groups, strips ≤ 560 px, y in the lower third.
- Longer or shorter clips: 1 tape group per 2–4 s; the lockup takes the last 1.5–2 s.

## Sound
- A soft thump on hit strips is not automatic for `tape` (adkit thumps fire on stomp/counter/lockup and kine hits);
  the shake still fires. Add a thump by using a `kine` companion with `hit: true`, or mix one in the music. Lockup gets a
  thump (0.45).

## Pitfalls and QA checklist
- [ ] Strips never cross a face or the product's key detail.
- [ ] Accent-strip text colour is legible (auto `--tacc`; check light accents like yellow).
- [ ] The wipe runs right-to-left for Hebrew (default); for English left-aligned groups consider `inset(0 100% 0 0)` in a css/js override.
- [ ] Numbers glued ("640 מעלות"), prices ש״ח; frames checked + `scripts/qa.py` "ship".
