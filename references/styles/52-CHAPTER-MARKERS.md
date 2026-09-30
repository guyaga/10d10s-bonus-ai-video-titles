# #52 CHAPTER-MARKERS · Documentary / YouTube chapter card

> A big chapter numeral draws as an outline and then fills, a hairline rule draws beside the kicker ("CHAPTER"/"פרק"), the chapter title rises out of a mask and a subtitle blurs up; then the card folds into a small chapter chip in the corner while a segmented chapter bar (the YouTube scrub-bar idiom) fills along the bottom.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/chapter-markers.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_CHAPTER-MARKERS.mp4
> Runner: run_style CHAPTER-MARKERS · Example: examples/chapter-markers/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: documentaries, long YouTube videos with chapters, course modules, brand films in parts, travel series, podcasts cut into segments.
- Avoid when: the video has no real structure (a chapter card for a 30 s ad is pretentious), or the establishing shot has no calm half.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#scrim` | a side gradient (rgba(4,8,14) at `scrim` 0.5 → 0 by 72% of the width) | fades to .35 after the card leaves |
| `#card` | 760 px column, 110 px from the side edge, top 250 px | text aligned to the reading start |
| `#num .o` / `.f` | 300 px numeral: an outline copy (2.5 px white stroke, almost transparent fill) and a solid copy on top | the solid fill wipes across the outline |
| `#kick` | kicker word (34 px body, +.32em Latin) with a 260×2 px accent rule | the rule draws from the reading start |
| `#ttl span` | chapter title, 104 px display, in a mask | |
| `#sub` | subtitle 38 px body, 88% white | |
| `#chip` | corner chip: numeral (accent) · divider · title, dark glass pill | appears as the card leaves |
| `#bar` | segmented chapter bar: one segment per chapter, 6 px tracks, labels under them (24 px) | past chapters full, the current one fills over the shot (accent) |

## Timing and motion
t0 = chapter.t, t1 = chapter.until.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| scrim (fade) | max(0, t0−.4) | 1.10 | power2.out | — | to .35 at t1−.4, .8 s | — |
| kicker rule (scaleX 0→1) | t0 | .90 | expo.out | — | kicker fades at t1−.45, .4 s | — |
| kicker word (fade, x ∓30→0) | t0+.15 | .70 | power3.out | — | — | — |
| numeral outline (fade, scale 1.08→1) | t0+.1 | .90 | power3.out | — | numeral fades + scale .96 + blur 8 at t1−.55, .6 s | power2.in |
| numeral fill (clip-path wipe) | t0+.75 | 1.10 | power2.inOut | — | — | — |
| numeral drift (x → ∓18) | t0 | t1−t0 | linear | — | — | — |
| title (yPercent 105→0) | t0+1.05 | 1.00 | expo.out | — | yPercent −105 at t1−.6, .6 s | power3.in |
| subtitle (fade, y 22→0, blur 6→0) | t0+1.5 | .80 | power3.out | — | fade + y −12 at t1−.65, .45 s | power2.in |
| chip (fade, y −16→0, scale .96→1) | t1−.1 | .60 | back.out(1.6) | to the end | — | — |
| bar (fade, y 20→0) | bar.t | .70 | power3.out | — | — | — |
| current segment fill (scaleX 0→1) | bar.t+.2 | clip duration − bar.t − .3 | linear | — | — | — |
- The card lives ~6 s (sample .6 → 6.8); the chip then holds for the rest of the chapter.
- The signature move: outline numeral → solid fill wipe, with a slow drift; the title rising out of a hard mask. Calm, editorial, expensive.

## Typography
- Latin: DM Serif Display 400 numeral (300 px), title (104 px), chip numeral (40 px); Manrope 500 kicker (34 px, +.32em, uppercase), subtitle (38 px), labels (24 px).
- Hebrew: `pair: "suez"` (default) = Suez One numeral and title, Secular One kicker/sub/labels. Everything runs right-to-left (rule, fill wipe, drift, bar fill). Suez One's digits sit low (old-style): for a big numeral that must look full-height, set `fonts: {"display": "DM Serif Display"}` only for the numeral via CSS, or use Karantina (`pair: "karantina-suez"`).
- Maximum copy: title ≈ 18 characters per line (760 px column; it wraps to 2 lines max), subtitle ≈ 36, bar labels ≈ 14.

## Colour and surface
- Roles: `text` #ffffff, `accent` #e8c27a (rule, chip numeral, current segment), `scrim` 0.5 (opacity of the side gradient).
- Brand swap: accent = brand colour (a warm gold or the channel colour); raise `scrim` to .6–.7 over bright footage.

## Layout and safe zones (1920×1080 canvas)
- `side` left → card at x 110; right → x 1050. Top 250. Chip top 70, 80 px from the reading-start corner. Bar: 120 px side insets, bottom 70.
- Industry convention: YouTube chapters come from timestamps in the description; this bar mirrors them visually (use the same chapter names). A chapter card should hold 4–6 s and sit on an establishing shot.
- 9:16: card in the upper third, numeral ≈ 200 px, skip the bar.

## What the footage must give you
- Shoot it like this: one take, 6–30 s, a calm establishing shot of the chapter's place: subject in one half, the other ~40% open (sea, sky, wall); slow steady glide, level horizon.
- Tracking: none. Matte: not needed.
- Good footage: aerials, wide landscapes, an empty stage, an exterior. Bad: busy crowds on the card side, fast moves, cuts.

## Build it
### A. With the kit
```bash
python scripts/run_style.py CHAPTER-MARKERS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| chapter | {num, kicker, title, sub, t, until} | required; t .6, until 6.6 |
| bar | {labels [...], current index, t} | none; current 0, t .3 |
| chip | collapse into a corner chip | true |
| side | "left" or "right" | "left" |
| language / pair | he/en; Hebrew pair | en / "suez" |
| fonts | override | DM Serif Display 400 / Manrope 500 |
| colors | {text, accent, scrim} | #fff, #e8c27a, .5 |
| sfx | whoosh, thump on the fill, whoosh on the title, click on the chip | true |
| music, music_vol, plate_vol, name | — | none, .5, .7 |
```json
{
 "clip": "clips/harbour.mp4", "side": "left",
 "chapter": {"num": "02", "kicker": "CHAPTER", "title": "The Harbour", "sub": "Where the city began, 1291", "t": 0.6, "until": 6.6},
 "bar": {"labels": ["The City", "The Harbour", "The Market", "Night"], "current": 1, "t": 0.3}
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const t0 = .6, t1 = 6.6;
tl.fromTo("#kick i", {scaleX: 0}, {scaleX: 1, duration: .9, ease: "expo.out"}, t0);
tl.fromTo("#num .o", {opacity: 0, scale: 1.08}, {opacity: 1, scale: 1, duration: .9, ease: "power3.out"}, t0 + .1);   // outline
tl.fromTo("#num .f", {clipPath: "inset(0 100% 0 0)"}, {clipPath: "inset(0 0% 0 0%)", duration: 1.1, ease: "power2.inOut"}, t0 + .75); // fill wipe
tl.fromTo("#num", {x: 0}, {x: -18, duration: t1 - t0, ease: "none"}, t0);                                                // slow drift
tl.fromTo("#ttl span", {yPercent: 105}, {yPercent: 0, duration: 1.0, ease: "expo.out"}, t0 + 1.05);
tl.fromTo("#sub", {opacity: 0, y: 22, filter: "blur(6px)"}, {opacity: 1, y: 0, filter: "blur(0px)", duration: .8, ease: "power3.out"}, t0 + 1.5);
tl.to("#ttl span", {yPercent: -105, duration: .6, ease: "power3.in"}, t1 - .6);
tl.to("#num", {opacity: 0, scale: .96, filter: "blur(8px)", duration: .6, ease: "power2.in"}, t1 - .55);
tl.fromTo("#chip", {opacity: 0, y: -16, scale: .96}, {opacity: 1, y: 0, scale: 1, duration: .6, ease: "back.out(1.6)"}, t1 - .1);
```

## Adapting it to the user's project
- Content: the user's real chapter list; the bar labels = their YouTube chapter titles.
- Language: Hebrew → `"language": "he"`; kicker "פרק".
- Brand: accent = channel colour.
- Vertical 9:16: see layout.
- Longer clips: the current segment fills over the whole clip; for one card per chapter, render a card at each chapter start (one spec per chapter clip).

## Sound
- `ar_whoosh` (.35) at t0, `soft_thump` (.5) on the numeral fill (t0+.75), `ui_whoosh` (.25) on the title, `soft_click` (.35) as the chip lands.

## Pitfalls and QA checklist
- [ ] The card sits on the calm half (set `side`).
- [ ] Hebrew: all wipes/drifts/bar fills run right-to-left.
- [ ] Big Suez One numerals look low (old-style digits): check it reads as intended.
- [ ] Bar labels match the video's real chapters.
- [ ] Contrast over bright skies: raise `scrim`.
