# #18 CYBER-DOSSIER · Character intro dossier

> A character walks toward camera and the city files them: a scan line sweeps down the frame, a bilingual location card wipes in, a bracket box locks onto the character with an ID tag riding beside them, and three status bars fill.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/cyber-dossier.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/B1_final.mp4
> Runner: bespoke (reference recipe `references/recipes/legacy_shots.py` → `B1`, 6 s) · Example: none shipped (the recipe carries its own paths)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: "meet the hero" openers, game and series trailers, team/speaker intros at tech events ("SPEAKER · 14:30 · HALL B"), athlete walk-outs, a founder walking into their office.
- Avoid when: the subject doesn't walk toward camera, the frame is crowded, or the piece is long (it's a 5–10 s beat, not a whole film).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `.tick` ×4 | corner brackets, 44 px, 48 px from the corners | amber at 70% |
| `#scan` | a 3 px glowing amber line that sweeps top → bottom once | box-shadow 24 px glow |
| `#loc` | location card, left 112 / top 104, 600 px wide, 3 px amber top rule | kicker (mono 18 px, .22em) + big line 54 px/800 + Hebrew line 34 px + two mono data rows 21 px |
| `#pbox .brk` | 4-corner bracket box around the tracked `pilot`, 18 px pad | amber corners 26 px, 3 px |
| `#ptag` | ID tag at the character's top-right (+34, +30) | name 30 px/800; two mono rows 18 px (callsign, suit status with an amber "ONLINE") |
| `#stat` | status panel, right 112 / bottom 112, 420 px | 3 labelled bars (POWER 98%, ARMOR 100%, NEURAL SYNC 99%), 6 px tracks |

## Timing and motion
From `legacy_shots.py` `B1` (6 s plate).
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| scan line | 0.1 | 0.9 (y 0 → 1080, opacity 1 → .2) | power2.inOut | — | ends faded | — |
| corner ticks | 0.15, stagger 0.05 | 0.4 (scale 1.5 → 1) | power3.out | whole clip | — | — |
| location card | 0.7 | 0.7 (clip wipe `inset(0 100% 0 0)` → 0) | expo.out | whole clip | — | — |
| Hebrew line | 1.1 | 0.4 fade | default | — | — | — |
| character brackets | 1.5 | 0.4 (scale 1.4 → 1) | power3.out | whole clip | — | — |
| ID tag | 1.7 | 0.45 (x −20 → 0) | power3.out | rides the character | — | — |
| status panel | 2.9 | 0.5 (y 24 → 0) | power3.out | — | — | — |
| bars | 3.1 / 3.2 / 3.3 | 0.8 (scaleX 0 → .98 / 1 / .99) | power2.out | — | — | — |
- The signature move: the order of discovery. First the world (scan + location), then the person (brackets + ID), then their state (bars). Nothing leaves: the frame ends as a complete dossier page.

## Typography
- Latin: big location and name in **Secular One** 800 (54 / 30 px, letter-spacing .02em); every data row in **JetBrains Mono** (18–21 px, letter-spacing .08–.22em, uppercase).
- Hebrew: the second location line in Secular One 34 px/600, RTL (e.g. "ניאו־תל אביב · גזרה 07"). Keep numbers like "07" inside the Hebrew string; they read correctly within a Hebrew run. Put dates/times in the mono rows.
- Max copy: big line ≈ 20 characters (600 px), ID name ≈ 18, data rows ≈ 34.

## Colour and surface
- The "B palette": accent #ffb547, fg #fff4e2, mute #d9c3a0, warn #ff5046, panels `rgba(12,8,4,.78)` with 6 px radius, bar tracks `rgba(255,244,226,.15)`.
- Amber on night-blue footage is the sample's look; for a brand, swap the accent and keep dark glass panels.

## Layout and safe zones (1920×1080 canvas)
- Location card top-left (112/104), status panel bottom-right (112/112), ID tag riding the character's top-right. The character walks down the centre; the plate contract wants 35% free on both sides.
- 9:16: location card top, ID tag beside the head, status bars bottom; the character fills the middle.

## What the footage must give you
- Shoot it like this: one take, no cuts, 5–10 s · full body, centred, walks toward camera · 35% free on both sides · low slow dolly backwards matching the walk.
- Seedance lines: "FORMAT: One continuous shot, no cuts." / "CAMERA: Low camera at waist height, slow steady dolly backwards matching his pace. FORBIDDEN: whip-pans, rotation, zooms, cuts." / "POSITIVE LOCKS: The character's look stays identical to the first frame. No text, no holograms, no UI, no logos appear at any time."
- Tracking (vtrack.py): `pilot` (the whole character; name it anything and use that name in `data-box` / `data-follow`), optionally `head`. Gate: ≥95% coverage.
- Matte: not needed.

## Build it
### A. With the kit
There's no run_style builder for this look. Build it as a bespoke adkit spec (a .py exposing `SPEC`) and run:
```bash
python scripts/vtrack.py clips/hero.mp4 hero_objects.json tracks/hero_vtrack.json
python scripts/run_ad.py HERO --spec specs/hero_dossier.py --render
```
Bespoke spec keys (adkit):
| Key | Meaning | Default |
|---|---|---|
| clip / track | plate + vtrack (default clips/<AD>_720p.mp4, tracks/<AD>_vtrack.json) | per AD |
| theme / palette | base theme + {acc, ink, lt, panel, sub} | "he_bold" |
| html_front | your HUD markup (can use `data-box`, `data-follow`, `data-anchor`, `data-dx/dy`) | — |
| css / js | styles + GSAP on `tl` (and optional `window.onPlace`) | — |
| fonts / assets | extra font faces / files copied into the project | — |
| elements | kit elements to mix in (usually `[]` for bespoke) | [] |
| music, music_vol, plate_vol, vo / vo_name | audio | – |
A minimal bespoke spec (the dossier on a new character):
```python
TICKS = '<div class="tick tk1"></div><div class="tick tk2"></div><div class="tick tk3"></div><div class="tick tk4"></div>'
BRK = '<div class="brk"><i></i><i></i><i></i><i></i></div>'
SPEC = {
  "theme": "he_bold", "palette": {"acc": "#ffb547", "ink": "#0c0804", "lt": "#fff4e2", "panel": "rgba(12,8,4,.78)", "sub": "#d9c3a0"},
  "elements": [],
  "html_front": f"""{TICKS}<div class="scan" id="scan"></div>
<div id="pbox" data-box="hero" data-pad="18">{BRK}</div>
<div id="ptag" class="panel" data-follow="hero" data-anchor="tr" data-dx="34" data-dy="30">
  <span class="n">SPEAKER · MAYA LEV</span><span class="s mono">CTO · NORTHWIND</span><span class="s mono">KEYNOTE · <b class="ok">14:30</b></span></div>
<div id="loc" class="panel"><span class="kick mono">LOCATION</span><span class="big">HALL B · STAGE 2</span>
  <span class="he">אולם ב׳ · במה 2</span><span class="row mono">TECH SUMMIT 2026 · DAY 1</span></div>""",
  "css": """
:root{--acc:#ffb547;--fg:#fff4e2;--mute:#d9c3a0;--panel:rgba(12,8,4,.78)}
.brk i{border-color:var(--acc)} .tick{border-color:rgba(255,181,71,.7)}
.scan{position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,transparent,var(--acc),transparent);box-shadow:0 0 24px var(--acc)}
#loc{position:absolute;left:112px;top:104px;width:600px;padding:22px 26px;border-top:3px solid var(--acc)}
#loc .kick{font-size:18px;letter-spacing:.22em;color:var(--acc)}
#loc .big{display:block;font-size:54px;font-weight:800;line-height:1.05;margin-top:8px;letter-spacing:.02em}
#loc .he{display:block;font-size:34px;font-weight:600;text-align:left;margin-top:4px}
#loc .row{display:block;font-size:21px;color:var(--mute);margin-top:10px}
#ptag{padding:14px 18px;white-space:nowrap}
#ptag .n{display:block;font-size:30px;font-weight:800}
#ptag .s{display:block;font-size:18px;color:var(--mute);letter-spacing:.08em;margin-top:4px}
#ptag .ok{color:#ffd28a}
""",
  "js": """<the timeline from B below>""",
}
```
The kit's base CSS already defines `.panel`, `.tick`/`.tk1-4` and `.brk`; add the `#stat` bars block from the recipe if you want the status panel.
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
tl.fromTo("#scan", {y: 0, opacity: 1}, {y: 1080, opacity: .2, duration: .9, ease: "power2.inOut"}, .1);
tl.fromTo(".tick", {opacity: 0, scale: 1.5}, {opacity: 1, scale: 1, duration: .4, stagger: .05, ease: "power3.out"}, .15);
tl.fromTo("#loc", {opacity: 0, clipPath: "inset(0 100% 0 0)"}, {opacity: 1, clipPath: "inset(0 0% 0 0)", duration: .7, ease: "expo.out"}, .7);
tl.fromTo("#loc .he", {opacity: 0}, {opacity: 1, duration: .4}, 1.1);
tl.fromTo("#pbox .brk", {opacity: 0, scale: 1.4}, {opacity: 1, scale: 1, duration: .4, ease: "power3.out"}, 1.5);
tl.fromTo("#ptag", {opacity: 0, x: -20}, {opacity: 1, x: 0, duration: .45, ease: "power3.out"}, 1.7);
tl.fromTo("#stat", {opacity: 0, y: 24}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, 2.9);
["#f1", "#f2", "#f3"].forEach((s, i) =>
  tl.fromTo(s, {scaleX: 0}, {scaleX: [.98, 1, .99][i], duration: .8, ease: "power2.out"}, 3.1 + i * .1));
// the tag and brackets follow the tracked box every frame (kit: data-box / data-follow do this for you)
```

## Adapting it to the user's project
- Content: location card = where we are (place + district + date/time + one condition); ID tag = who (name + role + one status); bars = three qualities that define the character/product (for a speaker: EXPERIENCE, ENERGY, HYPE).
- Language: keep the system rows in English mono; put the human line in Hebrew under the big location.
- Brand: accent colour on rules, corners and bars; everything else neutral.
- Longer clips: hold the finished dossier, or re-scan (repeat the scan line) when a second character enters.

## Sound
- B1 cues: hud_boot 0.05 (.7), ui_tick 0.7 (.45), lock_tick 1.5 (.8), data_chatter 1.7 (.35), bass_pulse 2.9 (.6), ui_pop 3.1 (.4). Plate at .7.

## Pitfalls and QA checklist
- [ ] The bracket box hugs the whole character (tight vtrack description: "the whole body, head to shoes").
- [ ] The ID tag never leaves the frame as the character grows; switch `data-anchor` to "tl" if they walk to the right.
- [ ] The location card doesn't sit on the character's head in the first second (they start small and centred).
- [ ] Bars end at believable values (98 / 100 / 99), not all at 100.
- [ ] Look at frames at 1.0, 2.0 and the end; qa.py until "ship".
