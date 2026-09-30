# #05 KINETIC-HE · Hebrew kinetic titles

> Big Hebrew words stomp in on the voiceover: a Karantina headline lands with a shake, a smaller Secular One line
> answers under it, and one word per piece sits behind the product in the accent colour.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/kinetic-he.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E6_guyaga_aero_sneaker_HE.mp4
> Runner: run_ad (adkit, theme `he_bold`) · Example: examples/E6_sneaker_sx.py (word-by-word `kine` version); the rendered sample's spec pattern is below

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: Hebrew social ads and product launches with a punchy voiceover; one strong phrase every 2–3 s; spec numbers
  that deserve a stomp ("4 שכבות", "189 גרם").
- Avoid when: there is no voice or music to hit (the stomps then feel random); the copy is sentences (use #06 TAPE-HE
  or #07 KINETIC-KARAOKE); the brand is quiet luxury (use theme `he_premium`, Suez One, see #10).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | plate 0.35 in the sample |
| Behind word (optional) | one huge accent word between plate and the matted product | `behind: true`, needs a matte (see #02) |
| Front stomp | Karantina headline, centred on `x, y` | size 190–230 px |
| Sub line | Secular One line under the headline | 34 % of the headline size, 55 % of the size below its centre |
| Support HUD (optional) | ring on the product, glass callouts, counters, chip | adkit `ring`, `callout`, `counter`, `chip` |
| Lockup | Hebrew tape lockup: brand strip + accent line strip | he_bold default |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Stomp headline | `t` = VO onset of the key word | 0.16 s, scale `from` (2.0) → 1, opacity 0 → 1, + frame shake + flash | power4.out | until `end` (2–2.5 s) | opacity 0 in 0.12 s ending at `end` | linear |
| Sub line | t + 0.25 | 0.2 s fade | default | with headline | with headline | — |
| Behind word | `t` | same stomp, `from` 1.4 (a gentler landing for a huge word) | power4.out | ~1.6 s | 0.12 s fade | — |
| Counter (Hebrew label) | `t` | stomp from 1.5; value eases cubic-out from `a` to `b` between `t0` and `t1`; bar scaleX 0 → 1 alongside | power4.out / cubic | until `end` | 0.12 s fade | — |
| Tape lockup | `t` | brand strip wipes right → left in 0.3 s (clip-path), text pops 1.3 → 1 in 0.18 s at +0.03; shake 0.45 at +0.12; line strip same at +0.3 | expo.out / power4.out | to the end | — | — |
| Word-by-word variant (`kine`) | each word's `t` | 0.14 s, scale 2.3 → 1 + blur 14 → 0; squash 1.1/0.82 → 1 in 0.2 s | power4.out, back.out(3) | until `end` | exit 160 px up/down or 260 px left/right + fade, 0.2 s | power2.in |

- Shake (adkit): x −12, +9, −5, 0 px and y +5, −4, +2, 0 px over 0.04 / 0.04 / 0.04 / 0.06 s; flash 0.3 × amount → 0 in
  0.14 s. `hit: true` on a kine word = shake at that word (amount `amt`, default 0.8).
- Voice sync: generate the VO (`scripts/vo_take2.py`), then `scripts/word_times.py` gives each word's onset; the headline
  lands on the stressed word, not the first word of the phrase.
- The signature move: **headline + answer**. A loud Karantina phrase stomps, a quiet Secular One line answers a quarter
  second later ("4 שכבות" → "אפס פשרות"), and every few phrases one word goes BEHIND the product.

## Typography
- Hebrew (this style): Karantina 700 for every headline, behind-word and counter number (condensed, loud); Secular One
  400 for sub lines, tag/callout titles and text, counter labels, chip (the theme's RTL css forces these);
  Suez One only if you switch to `he_premium`. Never Rubik/Heebo/Assistant/Anton for
  Hebrew (the kit remaps old names to these three automatically).
- RTL: the theme sets `direction: rtl` on stomps, tags, callouts, chip, lockup and meter; letter-spacing 0 on Hebrew;
  digits are glued to their word ("4 שכבות", "0.9 מ״מ") so a number never stands alone; counters keep the value LTR.
  Prices as ש״ח (the kit replaces ₪ automatically, none of the three faces has it).
- Sizes: headline 190–230 px front, 400–420 px behind; sub = 34 % of the headline; counter values 120 px.
- Max copy: headline ≤ 2 words (≤ 12 letters); sub ≤ 4 words; behind word 1 word.

## Colour and surface
- adkit palette roles: `lt` headline colour `#F5F3EE`, `acc` accent word / behind word `#E63B2E`, `ink` `#111111`,
  `panel` glass `rgba(14,14,14,.74)`, `sub` secondary text `#E4E1DB`. Swap in brand colours in `palette`.
- Shadow: theme default is an 8 px 8 px 0 accent offset; the sample overrides it with a soft depth shadow
  (`.st span.c{text-shadow:0 18px 70px rgba(0,0,0,.55)!important}`) and gives the Hebrew sub a heavy halo so it reads
  over bright footage.

## Layout and safe zones (1920×1080 canvas)
- Headlines centred at x 960, y 118–215 (top band) while the product sits centre/lower; behind-words where the product
  will cover them (sample: x 1210 y 138 at 400 px).
- Callouts fixed at the frame sides (x −10 or 1520; the glass box is 360 px wide), their leader lines run to the tracked
  point. Counters at x 70 / 1590, y 300 / 560.
- 9:16: keep headlines ≤ 600 px wide and centred (x 656–1264 survives a centre crop); drop the side callouts.

## What the footage must give you
- Shoot it like this: cuts OK (max 5), 12–24 s · subject centred, room above it · 25 % free at the top · slow orbit or
  slow push; energy from the subject, not the camera.
- Tracking: the hero object (`shoe`, `bottle`…) for rings and callouts; parts as separate objects if you call them out.
- Matte: only for behind-words.
- Good: product centred low with an empty top quarter. Bad: busy top of frame (sky with signs, crowds) under the headline.

## Build it
### A. With the kit
```bash
python scripts/vo_take2.py MY_AD specs/MY_AD_he_lines.json he        # optional: Hebrew VO
python scripts/word_times.py MY_AD specs/MY_AD_he_lines.json he      # word onsets for the stomps
python scripts/run_ad.py MY_AD --spec specs/MY_AD.py --render
```
| Key | Meaning | Default |
|---|---|---|
| theme | `he_bold` (Karantina) / `he_premium` (Suez One) | `guyaga` |
| palette | `{acc, ink, lt, panel, sub}` | required |
| `stomp` | `text, sub, t, end, x, y, size, from, behind, color` | size 200, from 2.0 |
| `kine` | `x, y, t, end, exit, behind, lines:[[{w, t, size, style fill/accent/outline, font big, hit, amt}]]` | size 180 |
| `counter` | `t0, t1, a, b, dec, pre, suf, label, x, y, size, t, end` | size 160 |
| `lockup` | `brand, line, t, size, line_size` | 118 / 58 px (tape look in Hebrew themes) |
| vo_name / vo, music, music_vol, plate_vol, css | media and overrides | `<AD>_vo`, –, 0.5, 0.4 |

A minimal spec (`specs/MY_AD.py`):
```python
SPEC = {"theme": "he_bold",
 "palette": {"acc": "#E63B2E", "ink": "#111111", "lt": "#F5F3EE", "panel": "rgba(14,14,14,.74)", "sub": "#E4E1DB"},
 "clip": "clips/my_product.mp4", "track": "tracks/my_product_vtrack.json", "vo": "shared/sfx/MY_AD_he_vo.mp3",
 "css": ".st span.c{text-shadow:0 18px 70px rgba(0,0,0,.55)!important}",
 "elements": [
  {"type": "stomp", "text": "קלה במיוחד", "sub": "רק 189 גרם", "x": 960, "y": 150, "size": 230, "t": 0.62, "end": 2.6},
  {"type": "stomp", "text": "4 שכבות", "sub": "אפס פשרות", "x": 960, "y": 150, "size": 230, "t": 2.9, "end": 5.2},
  {"type": "counter", "t0": 5.4, "t1": 6.4, "a": 0, "b": 189, "label": "גרם · משקל", "x": 70, "y": 300, "size": 120, "t": 5.4, "end": 7.6},
  {"type": "lockup", "brand": "MY BRAND", "line": "רצים על אוויר", "t": 8.0}]}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```css
.st span{font:700 230px Karantina;direction:rtl;letter-spacing:0;color:#F5F3EE;transform:translate(-50%,-50%)}
.st i.he{font:400 78px "Secular One";direction:rtl;transform:translate(-50%,126px);text-shadow:0 4px 24px rgba(0,0,0,.6)}
```
```js
function shake(at, a = 1) {
  tl.to(["#stage", "#stage2"], {keyframes: [{x: -12*a, y: 5*a, duration: .04}, {x: 9*a, y: -4*a, duration: .04},
        {x: -5*a, y: 2*a, duration: .04}, {x: 0, y: 0, duration: .06}], ease: "none"}, at);
  tl.fromTo("#flash", {opacity: .3*a}, {opacity: 0, duration: .14}, at);
}
for (const [id, t, end] of LINES) {                        // t = word onset from word_times.py
  tl.set(`#${id}`, {opacity: 1}, t - .01);
  tl.fromTo(`#${id} span`, {opacity: 0, scale: 2}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, t); shake(t);
  tl.fromTo(`#${id} i`, {opacity: 0}, {opacity: 1, duration: .2}, t + .25);   // the answer line
  tl.to(`#${id}`, {opacity: 0, duration: .12}, end - .12);
}
```

## Adapting it to the user's project
- Content: write the VO first, 2–4 words per phrase; pick the stressed word of each phrase as the headline; put the
  proof (number, material) in the sub line or a counter.
- Language: this style is Hebrew-first; for English use theme `guyaga` (Anton) with the same structure.
- Brand: `acc` = brand colour (used on behind-words, accent words, counter bars, tape line).
- Vertical 9:16: headlines ≤ 600 px, centred; no side callouts.
- Longer or shorter clips: one headline per VO phrase; leave ≥ 0.3 s between a headline's `end` and the next `t`.

## Sound
- Soft sub thump 0.45 on every stomp, counter and lockup (0.55 on kine hits); VO at 1.0, music `music_vol` (sample 0.6),
  plate `plate_vol` (sample 0.35).

## Pitfalls and QA checklist
- [ ] Every headline lands on a VO word onset (check with the waveform), not on silence.
- [ ] No Latin-only face touches Hebrew (the kit remaps; check the rendered frame anyway).
- [ ] Numbers glued to their word; counters LTR; prices ש״ח.
- [ ] The flash layer: adkit's flash starts at 0.3 until the first hit on some specs. Add `#flash{display:none}` in
      `css` if the plate looks milky at the start.
- [ ] Sub lines readable over bright frames (halo shadow); frames checked + `scripts/qa.py` "ship".
