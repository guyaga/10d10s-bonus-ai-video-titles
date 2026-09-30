# #43 BREAKING-NEWS · Rolling-news package

> A red BREAKING slab slams in with a white flash and a shine, the white headline bar wipes open and the headline types in word by word, a strap drops under it, a channel bug with a LIVE chip and a running clock sits top-corner, and a ticker crawls along the bottom. Headlines flip to the next one.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/breaking-news.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_BREAKING-NEWS.mp4
> Runner: run_style BREAKING-NEWS · Example: examples/breaking-news/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: news-style social clips, "breaking" product announcements, internal-comms parodies, event coverage, local-news-look promos, sports/transfer news.
- Avoid when: the subject is a face in close-up (the package covers the lower 30%), the footage already has burned-in text or signs with words, or the tone is premium/luxury (it reads as urgent TV).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#flash` | full-frame white | one 0.25 s pop at the slam |
| `#tk` | ticker: 70 px navy band at the very bottom, red label cell + crawling text | the crawl is driven per frame from video time |
| `#strap` | navy strap with a 10 px red square, 28 px body face | sits 118 px from the bottom, under the headline |
| `#lower` | the headline group, 170 px from the bottom, 80 px from the start edge, drop shadow 0 14 px 28 px | contains slab + headline bar |
| `#slab` | red label ("BREAKING NEWS" / "מבזק") with a skewed white `.shine` | 60 px Latin / 82 px Hebrew display |
| `#hbar` | white bar, 120 px tall, min 560 px wide, 6 px red inset underline | holds all headlines stacked; only one visible |
| `.hl .w` | headline words | each word is its own span (typed in) |
| `#bug` | top corner (opposite side to the headline): LIVE chip (pulsing dot) + channel name + clock | always LTR; clock in Oswald numerals |

## Timing and motion
T0 = the first headline's `t`.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| bug (opacity, y −20→0) | max(.2, T0−.8) | .45 | power3.out | whole clip | — | — |
| slab slam (scale 1.6→1, fade) | T0−.45 | .22 | power4.out | whole clip | — | — |
| white flash (.55→0) | T0−.45 | .25 | power2.out | — | — | — |
| headline bar wipe (clip-path) | T0−.25 | .50 | expo.out | whole clip | — | — |
| shine sweep (x −130→520) | T0−.2 and again T0+3.2 | .70 | power2.inOut | — | — | — |
| headline words (yPercent 105→0, fade) | each headline's t | .32 each, stagger .07 | expo.out | until next headline | yPercent −105, .25 s, stagger .03, starting next t−.28 | power2.in |
| strap (opacity, y −24→0) | strap.t | .40 | power3.out | — | — | — |
| ticker band (y 70→0) | ticker.t | .45 | power3.out | — | — | — |
| ticker crawl | from ticker.t | `speed` px/s (150) | linear | loops over 3 copies | — | — |
| LIVE dot pulse | 0 | .5 per half-cycle, 30 repeats | sine.inOut | ≈15 s | — | — |
| clock | every frame | `clock` + floor(video time) | — | — | — | — |
- Beat/voice sync: slam on a musical hit or the anchor's first word; a new headline every 4–6 s.
- The signature move: the slam (scale from 1.6 in 0.22 s) with the white flash and the shine, then words typing into a hard white bar.

## Typography
- Latin: Oswald 700 slab (60 px, +.04em) and headline (58 px, UPPERCASE); Archivo 500 strap/ticker (28/30 px). Bug clock and LIVE: Oswald (always, even in Hebrew: broadcast numerals).
- Hebrew: `pair: "karantina"` (default) = Karantina 700 slab 82 px + headline 70 px, Secular One strap and ticker. No uppercase, no tracking. Layout mirrors: headline group on the right, bug on the left, ticker crawls left-to-right.
- Maximum copy: headline ≈ 30 Latin / 34 Hebrew characters (nowrap; the bar grows to fit but must not cross the bug column). Strap ≈ 45 characters. Ticker: any length (it loops).

## Colour and surface
- Roles: `red` #d6001c (slab, underline, ticker label, LIVE), `bar` #ffffff, `ink` #0b0b0e (headline text), `navy` #0a1a33 (strap, bug name, ticker band), `text` #ffffff.
- Brand swap: a channel colour replaces `navy`; keep `red` for urgency (or brand accent for non-news parodies). Keep the headline bar light and the ink dark: it's the readability anchor.

## Layout and safe zones (1920×1080 canvas)
- Headline group: bottom 170 px, 80 px from the start edge. Strap: bottom 118 px. Ticker: full-width 70 px at the bottom (below title-safe, like real channels). Bug: top 60 px, 70 px from the other edge.
- Industry conventions: tickers crawl at ~120–180 px/s at 1080p (150 default; faster reads as panic); headlines stay on screen ≥ 4 s; the bug sits in the top corner opposite the headline so both corners are never loaded at once.
- 9:16: raise `#lower` above the platform UI (≈ bottom 360 px) and drop the ticker or set speed ≈ 110.

## What the footage must give you
- Shoot it like this: one take, 6–30 s, wide, key action in the upper two thirds, the bottom 30% road/ground with no important detail; locked-off or a very slow push from an elevated position.
- Tracking: none.
- Matte: not needed.
- Good footage: street scenes, crowds, a building exterior, a stadium, a launch event from the back. Bad: signs/billboards with readable words (fake news graphics next to real text look broken), close faces, fast handheld.

## Build it
### A. With the kit
```bash
python scripts/run_style.py BREAKING-NEWS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| headlines | [{text, t}] each flips in, replacing the previous | required |
| slab | the red label text | "BREAKING NEWS" |
| strap | {text, t} small line under the headline | none |
| bug | {name, clock "HH:MM:SS"}: clock runs with the video | none |
| live | LIVE chip on the bug | true |
| ticker | {text, t, speed, label} | none; speed 150; label "MORE"/"עוד" |
| language / pair | he/en; Hebrew pair | en / "karantina" |
| fonts | override {display, dw, body, bw} | Oswald 700 / Archivo 500 |
| colors | {red, bar, ink, navy, text} | see above |
| sfx | bass pulse + stinger at the slam, tick per headline | true |
| music, music_vol, vo, vo_vol | audio | none, .5, none, 1 |
| plate_vol | clip audio | .6 |
| name | project folder | breaking-news |
```json
{
 "name": "launch-news",
 "clip": "clips/event.mp4",
 "slab": "BREAKING",
 "headlines": [{"text": "Acme unveils its first humanoid", "t": 1.0}, {"text": "Preorders open tonight", "t": 5.5}],
 "strap": {"text": "BERLIN · LIVE FROM THE KEYNOTE", "t": 1.9},
 "bug": {"name": "ACME TV", "clock": "20:15:00"},
 "ticker": {"text": "Price from €2,900  ·  Ships in spring  ·  Five colours", "t": 0.6}
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const T0 = 1.0;
tl.fromTo("#slab", {scale: 1.6, opacity: 0}, {scale: 1, opacity: 1, duration: .22, ease: "power4.out"}, T0 - .45);
tl.fromTo("#flash", {opacity: .55}, {opacity: 0, duration: .25, ease: "power2.out"}, T0 - .45);
tl.fromTo("#slab .shine", {x: -130}, {x: 520, duration: .7, ease: "power2.inOut"}, T0 - .2);
tl.fromTo("#hbar", {clipPath: "inset(0 100% 0 0)"}, {clipPath: "inset(0 0% 0 0%)", duration: .5, ease: "expo.out"}, T0 - .25);
tl.fromTo("#hl0 .w", {yPercent: 105, opacity: 0}, {yPercent: 0, opacity: 1, duration: .32, ease: "expo.out", stagger: .07}, T0);
tl.to("#hl0 .w", {yPercent: -105, opacity: 0, duration: .25, ease: "power2.in", stagger: .03}, 5.5 - .28); // next headline at 5.5
tl.fromTo("#hl1 .w", {yPercent: 105, opacity: 0}, {yPercent: 0, opacity: 1, duration: .32, ease: "expo.out", stagger: .07}, 5.5);
// ticker + clock are functions of video time (seek-safe), not tweens:
window.onPlace = (t) => {
  const mv = document.getElementById("mv"), w = mv.scrollWidth / 3;   // text repeated 3x
  mv.style.transform = `translateX(${-((Math.max(0, t - .6) * 150) % w)}px)`;
};
```

## Adapting it to the user's project
- Content: short, verb-first headlines; real place/time on the strap; the ticker carries the secondary facts.
- Language: Hebrew → `"language": "he"`, slab "מבזק"; mirrors automatically; clock stays Latin digits.
- Brand: channel name in the bug; `navy` → brand colour.
- Vertical 9:16: see layout; keep one headline.
- Longer clips: the LIVE pulse stops after ≈15 s (30 repeats × 0.5 s); for longer clips extend `repeat`, or accept a solid dot.

## Sound
- `bass_pulse` (.7) + `stinger` (.55) at T0−.45 (the slam); `ui_tick` (.3) at each headline. Real news packages also use a short "sting" of music: add `music` at low volume.

## Pitfalls and QA checklist
- [ ] Headline fits in the bar without touching the bug side.
- [ ] No readable real-world text in the footage behind the package.
- [ ] Ticker speed 120–180 px/s; loop seam invisible (three copies of the text).
- [ ] Clock format "HH:MM:SS"; it starts at the given value at t=0.
- [ ] Hebrew: slab on the right, ticker crawls left-to-right, bug on the left.
- [ ] Crawl and clock are computed from video time in `onPlace` (seek-safe); never animate `left`.
