# #10 PRESIDENTIAL-SERIF · Premium serif titles

> Few, big serif words (BLOCK, STRIKE, VICTORY) that ease in softly with a red underline, small glass tags on the
> action, one live percent counter, and a restrained one-line lockup. Expensive, never comic.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/presidential-serif.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E2_sparta_spartan_vs_machine.mp4
> Runner: run_ad (adkit theme `sparta` for Latin, `he_premium` for Hebrew) · Example: the spec below (the sample's spec pattern)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: epic brand films, leadership and institutional pieces, battle/sport trailers that must feel expensive,
  launches where restraint signals quality. It was built after a multi-colour comic version was rejected as childish.
- Avoid when: the brief is loud social (use #05/#12); there are many facts to show (3–4 words for the whole film is the
  point); the footage is flat and needs energy from graphics.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's cut | plate 0.45 in the sample |
| Behind word (optional) | the final word behind the hero | `behind: true` + matte |
| Serif words | DM Serif Display, letter-spaced, soft shadow, 140 × 5 px accent underline | `stomp` in a premium theme = the soft entrance |
| Glass tags | numbered tags following tracked objects (HOSTILE · WAR UNIT) | `tag` |
| Brackets, rings | target bracket on the opponent, a ring on a weak point | `box`, `ring` |
| Counter | "SHIELD INTEGRITY 100 → 72 %" | `counter` |
| Chip, voice meter | top-left chip; bottom-right meter driven by a voice envelope | `chip`, `meter` + `env` |
| Lockup | glass bar: brand · accent rule · italic line, bottom centre | premium themes keep this restrained look |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Serif word (premium `stomp`) | `t` | 0.6 s: opacity 0 → 1, scale 1.12 → 1, y 16 → 0, + a small shake (0.25) | expo.out | 1.5–2.7 s (`end`) | 0.12 s fade | linear |
| Glass tag | `t` | 0.35 s clip-path wipe left → right + fade; underline scaleX 0 → 1 in 0.45 s at t + 0.15 | expo.out / power3.out | to `end` | 0.12 s | — |
| Box brackets | `t` | 0.3 s, scale 1.5 → 1; crosshair ticks fade 0.2 s, stagger 0.04 s, at t + 0.15 | power3.out | to `end` | 0.12 s | — |
| Ring | `t` | 0.35 s, scale 1.6 → 1; rings rotate 160 × spin °/s, −110 × spin °/s, ticks 25 × spin °/s | expo.out | to `end` | 0.12 s | — |
| Counter | `t` | stomp from 1.5 (0.16 s) + shake; value cubic-out a → b between t0 and t1; bar grows with it | power4.out | to `end` | 0.12 s | — |
| Chip | `t` | 0.35 s, x −20 → 0 | power3.out | to `end` | — | — |
| Lockup | `t` | stomp from 1.4 | power4.out | to the end | — | — |

- Sample rhythm (25 s trailer): chip and meter at 0.3 s; opponent box 3.3–4.3 s; tag 4.3–7.95 s; BLOCK at 13.0 s with the
  shield counter; ring + WEAK POINT tag 15.9–18 s; STRIKE at 18.15 s; VICTORY behind at 22.3 s; lockup 22.9 s.
- The signature move: **the soft landing**. Words don't stomp; they settle in 0.6 s with an expo ease, a 16 px rise and a
  whisper of shake, then hold long. The 140 × 5 px accent bar under each word is the only colour on screen.

## Typography
- Latin (theme `sparta`): display DM Serif Display 400 (words, tag titles 34 px, counter numbers, lockup 70 px);
  labels Space Grotesk; data Space Mono (tag number 15 px .2em, tag sub 17 px .08em, counter unit 20 px .18em);
  lockup line DM Serif Display italic 40 px. Serif words 240–270 px, letter-spacing .06em.
- Hebrew (theme `he_premium`): Suez One 400 for the serif words, counter numbers and the lockup brand; Secular One for
  tag titles and subs, callouts, counter labels, chip, meter and the lockup line (the theme's RTL css swaps these in);
  no letter-spacing on Hebrew. Numbers LTR in counters,
  glued to their word in text. Prices ש״ח.
- Max copy: 3–4 serif words per film, 1 word each (≤ 8 letters at 260 px); tag title ≤ 20 characters.

## Colour and surface
- Palette (sample): acc `#E63B2E`, ink `#111111`, lt `#F5F3EE` (cream words), panel `rgba(17,17,17,.82)`, sub `#f3c6c1`.
  One accent only. Brand: swap `acc` and keep lt warm white.
- Serif word shadow: `0 10px 50px rgba(0,0,0,.55), 0 2px 6px rgba(0,0,0,.4)` (no offset shadow). Glass panels:
  `var(--panel)`, blur 10 px, saturate 1.15, 1 px `rgba(255,255,255,.22)` border, 14 px accent corner brackets.

## Layout and safe zones (1920×1080 canvas)
- Words centred at x 960, y 175–250 (upper band over sky/smoke); counter at x 90, y 660; chip 84 / 56; meter right 70,
  bottom 112, 300 px wide; lockup bottom 112, centred.
- Tags follow tracked objects (anchor + dx/dy); keep them off faces.
- 9:16: a 260 px word is ~900 px wide for 6 letters; for vertical use 180 px and centre.

## What the footage must give you
- Shoot it like this: planned cut list (max 6), 18–30 s · hero framed off-centre, sky or smoke above · 25 % free at the
  top · cinematic, grounded; push-ins and tracking.
- Tracking: hero and opponent (and any weak point you ring), vtrack objects with clear `desc`.
- Matte: for the final behind-word.
- Good: epic wide shots with haze or sky in the top quarter. Bad: busy top band (text fights detail).

## Build it
### A. With the kit
```bash
python scripts/run_ad.py MY_AD --spec specs/MY_AD.py --render
```
Element keys: `stomp` (text, x, y, size, t, end, behind), `tag` (title, sub, follow, anchor, dx, dy, t, end), `box` (obj,
pad, label, t, end), `ring` (obj, r 180, spin 1, t, end), `counter` (t0, t1, a, b, dec, pre, suf, label, x, y, size 160,
t, end), `chip` (text, sub, t), `meter` (label, t) with spec `env` (per-frame 0–1 voice loudness), `lockup` (brand, line, t).

A minimal spec:
```python
SPEC = {"theme": "sparta",
 "palette": {"acc": "#E63B2E", "ink": "#111111", "lt": "#F5F3EE", "panel": "rgba(17,17,17,.82)", "sub": "#f3c6c1"},
 "clip": "clips/my_film.mp4", "track": "tracks/my_film_vtrack.json", "matte": "mattes/my_film_alpha.webm",
 "music": "shared/sfx/my_score.mp3", "music_vol": 0.5, "plate_vol": 0.45,
 "elements": [
  {"type": "chip", "text": "MY BRAND", "sub": "EST. 1998", "t": 0.3},
  {"type": "tag", "title": "THE CHALLENGE", "sub": "42 KM · 3 000 M CLIMB", "follow": "hero", "anchor": "r", "dx": 40, "t": 3.0, "end": 6.5},
  {"type": "stomp", "text": "RISE", "x": 960, "y": 200, "size": 260, "t": 8.0, "end": 10.5},
  {"type": "counter", "t0": 11.0, "t1": 12.0, "a": 0, "b": 97, "suf": "%", "label": "FINISH RATE", "x": 90, "y": 660, "size": 150, "t": 11.0, "end": 13.5},
  {"type": "stomp", "text": "LEGACY", "x": 960, "y": 250, "size": 270, "behind": True, "t": 15.0},
  {"type": "lockup", "brand": "MY BRAND", "line": "Built to last.", "t": 15.8}]}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```css
.pm{font:400 260px "DM Serif Display";letter-spacing:.06em;color:#F5F3EE;
    text-shadow:0 10px 50px rgba(0,0,0,.55),0 2px 6px rgba(0,0,0,.4);transform:translate(-50%,-50%)}
.pm::after{content:"";position:absolute;left:50%;bottom:-18px;width:140px;height:5px;background:#E63B2E;transform:translateX(-50%)}
```
```js
function shake(at, a = 1) {
  tl.to(["#stage", "#stage2"], {keyframes: [{x: -12*a, y: 5*a, duration: .04}, {x: 9*a, y: -4*a, duration: .04},
        {x: -5*a, y: 2*a, duration: .04}, {x: 0, y: 0, duration: .06}], ease: "none"}, at);
  tl.fromTo("#flash", {opacity: .3*a}, {opacity: 0, duration: .14}, at);
}
function soft(sel, at) {                                   // the premium entrance
  tl.fromTo(sel, {opacity: 0, scale: 1.12, y: 16}, {opacity: 1, scale: 1, y: 0, duration: .6, ease: "expo.out"}, at);
  shake(at, .25);
}
soft("#w1 span", 13.0); tl.to("#w1", {opacity: 0, duration: .12}, 15.7 - .12);
```

## Adapting it to the user's project
- Content: pick the 3–4 words that ARE the story's turns (a challenge, a turn, a result); everything else is tags.
- Language: Hebrew → `he_premium` (Suez One); one Hebrew word per title.
- Brand: one accent; cream words; the lockup line in italic.
- Vertical 9:16: smaller words, centred; drop side tags.
- Longer or shorter clips: ≥ 4 s between serif words; long holds are the style.

## Sound
- Soft thump 0.45 on every stomp/counter/lockup (even the soft words get one); the score carries the piece
  (music 0.5), plate 0.45 so impacts are heard.

## Pitfalls and QA checklist
- [ ] ≤ 4 serif words in the whole piece; no two on screen at once.
- [ ] No comic colours, no hard offset shadows (premium theme handles it; don't add css shadows).
- [ ] Counter and lockup use `stomp` even in premium themes; if that hit feels loud, add css `#lock{...}` or remove the
      counter shake by building a custom soft counter.
- [ ] Tags off faces; frames checked + `scripts/qa.py` "ship".
