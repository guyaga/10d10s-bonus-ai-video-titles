# Testing

**Last clean-install run: 2026-09-30.** A fresh `git clone` of commit `b445668` into an empty folder, Windows 11,
Python 3.13, Node 22, `hyperframes@0.8.84`. No project files, no plates, no keys used.

```bash
python scripts/doctor.py      # deps, keys, sibling skills, bundled assets
python scripts/selftest.py    # everything below, ~10 min with --jobs 4
```

## 1. Every style builds on the footage bundled with the skill

`run_style.py <ID> --demo` builds each style on `examples/demo/` (the 8 s runway clip looped to the style's own length,
a synthetic track carrying every object the style rides, placeholder words where a style needs word timings), then
runs `hyperframes check`: lint, runtime, layout (overlaps, overflow) and motion. The WCAG contrast pass is off in demo
mode only: the bright neutral demo footage says nothing about how a style reads on the footage it is designed for.
Real builds keep it on.

| Style | `--demo` build + check | Time | Note |
|---|---|---|---|
| STOMP-ESCORT | PASS | 72 s |  |
| COUNTDOWN-CTA | PASS | 76 s |  |
| HUD-HELMET | PASS | 71 s |  |
| HUD-CLEAN | PASS | 47 s |  |
| SCIFI-TARGETING | PASS | 28 s |  |
| MAP-FLYOVER | PASS | 35 s |  |
| CAMPUS-AR | PASS | 32 s |  |
| SPEED-STAT | PASS | 38 s |  |
| VIRAL-CAPTIONS | PASS | 32 s |  |
| DECODE-TYPE | PASS | 41 s |  |
| GLITCH-RGB | PASS | 44 s |  |
| NEON-SIGN | PASS | 33 s |  |
| KEYNOTE-REVEAL | PASS | 40 s |  |
| SPLIT-FLAP | PASS | 37 s |  |
| SIGNATURE-WRITE-ON | PASS | 45 s |  |
| BROADCAST-PACK | PASS | 43 s |  |
| FILM-TITLE-CARD | PASS | 54 s |  |
| PARTICLE-TEXT | PASS | 28 s |  |
| FLIP-MONTAGE-LOGO | PASS | 25 s |  |
| TEXT-ON-PATH | PASS | 24 s |  |
| LOWER-THIRD-CORP | PASS | 27 s |  |
| BREAKING-NEWS | PASS | 25 s |  |
| LEADER-CALLOUTS | PASS | 28 s |  |
| DATA-CHARTS | PASS | 26 s |  |
| KPI-COUNTERS | PASS | 27 s |  |
| APP-UI-POPUPS | PASS | 26 s |  |
| CHAT-BUBBLES | PASS | 25 s |  |
| SOCIAL-CTA | PASS | 23 s |  |
| END-SCREEN | PASS | 33 s |  |
| PODCAST-TAGS | PASS | 34 s |  |
| CHAPTER-MARKERS | PASS | 29 s |  |
| QUOTE-TESTIMONIAL | PASS | 29 s |  |
| DOC-LOCATION-STAMP | PASS | 30 s |  |
| SWISS-GRID | PASS | 31 s |  |
| GRADIENT-GLASS | PASS | 32 s |  |
| BEFORE-AFTER-SPLIT | PASS | 33 s |  |
| LOGO-SHINE-REVEAL | PASS | 24 s |  |
| LYRIC-KINETIC-3D | PASS | 30 s |  |
| TIMELINE-HISTORY | PASS | 30 s |  |
| LISTING-SPECS | PASS | 28 s |  |
| COMIC-POP (run_ad) | PASS | 22 s |  |

check_clip.py plan: 61/61 · check on the demo clip: 61/61 (verdicts: PASS 25, PASS WITH WARNINGS 36)

40 `run_style` styles + COMIC-POP through `run_ad.py` = 41. STICKER-POP is a variant of STOMP-ESCORT's word style and
has no builder of its own; the 10 bespoke crafted worlds and the other adkit styles are built from their specs/recipes
(see `references/recipes/README.md` for which ones run as-is).

**Demo anchors.** Objects the demo clip does not contain are derived from its tracked model: face/eyes = head,
boots/shoes = feet, cargo/trousers/skirt = legs, jacket/coat/knit = torso, bag/buds/case/ball = the right hand,
*_left / *_right = the model shifted to the left / right third. Places and points (airport, tower, pool …) sit on fixed
anchors: two rows at y 330 and 760, x 250 / 900 / 1550, then (575, 545), (1225, 545). Route points lie on an arc
across the frame. See `scripts/demo.py`.

## 2. The clip checker (`check_clip.py`)

- `plan <style>`: 61/61 styles print their shooting requirements and prompt lines.
- `check <style> examples/demo/runway_demo_720p.mp4 --no-gemini`: 61/61 run to a verdict (PASS 25, PASS WITH
  WARNINGS 36, FAIL 0; the warnings are "tracking not checked" for styles that ride objects, as expected without
  `--objects`).

## 3. Real renders (from the clean clone)

| Style | Render | What the frames show |
|---|---|---|
| BREAKING-NEWS | `titles-demo/renders/demo-breaking-news.mp4` (13 s) | LIVE bug with a running clock, red slab, headline bar types then flips to the second headline, strap, ticker; Hebrew RTL correct |
| GLITCH-RGB | `demo-glitch-rgb.mp4` (18 s) | title, RGB tear on the beat with CARGO riding the derived legs, clean recovery; red sub-lines are low-contrast on the bright demo plate (fine on the dark plates it is designed for) |
| VIRAL-CAPTIONS | `demo-viral-captions.mp4` (8 s) | Hebrew placeholder line in Secular One, 1-3 words per group, stroke + shadow, readable over the runway |
| PODCAST-TAGS | `demo-podcast-tags.mp4` (14 s) | two host tags on the left / right thirds, never overlapping (collision avoidance stacks them if they meet), REC bug, episode chip and topic strap running to the end |
| HUD-CLEAN | `demo-hud-clean.mp4` (14 s) | no boot ring, no reticle: vitals cluster, heading tape, message panel, the red alert state |

## 4. `catalog.py make` on a clip that is not the example's

`make 31 examples/demo/runway_demo_720p.mp4 "…Hebrew context…"` → project folder, starter spec (`language: he`,
context saved, TODOs listed), `objects.json` for `face`, the clip check verdict, the next commands. Building before
tracking stops with the exact vtrack command instead of a stack trace.

## Found and fixed by this test

- SPEED-STAT used "Secular One" in CSS without loading it (every real render failed the font check).
- adkit loaded the Hebrew fallback faces only for Hebrew themes, so English adkit ads (TRACKED-TAGS, STOMP-BEHIND,
  GLASS-CALLOUT, COMIC-POP) failed the font check.
- A missing music / voice / matte / image stopped the build; now it warns and builds without it.
- The speed counter's digits touched its unit tag; PODCAST-TAGS tags overlapped when the hosts were close.
- LIVE pulse, REC blink and glass chip float stopped early on clips longer than the example; they now follow the clip.
