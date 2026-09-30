# #53 QUOTE-TESTIMONIAL · Customer quote in sync with the voice

> A big quote mark drops in, the quote builds word by word in sync with the speaker's own voice, the key phrase gets an accent underline as it is spoken, then the attribution slides in: a hairline, the name, the role and five stars that pop one by one.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/quote-testimonial.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_QUOTE-TESTIMONIAL.mp4
> Runner: run_style QUOTE-TESTIMONIAL · Example: examples/quote-testimonial/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: testimonial ads, case studies, reviews, UGC with real customers, social proof in landing-page videos, B2B client stories.
- Avoid when: the speaker's quote is longer than ~15 words (split it), the face fills the frame (the quote needs ~35% of the width), or the claim can't be attributed to a real person (don't invent quotes or names).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#scrim` | side gradient rgba(0,0,0,.5) → transparent at 62% | only with `ink: "light"` (over dark backgrounds) |
| `#qm` | 150×112 px SVG quote mark in `mark` colour (#b8651a) | mirrored (scaleX −1) in Hebrew |
| `#txt .w` | the quote, one span per word, `size` px display face | words start invisible and rise on their spoken time |
| `.w.k::after` | accent underline behind the key phrase (14% of the font size, 50% opacity) | grows per word with a CSS variable `--u` |
| `#att` | 120×2 px accent hairline, name (40 px, 700), role (30 px), stars (38 px SVG, accent), optional brand text | |

## Timing and motion
Word times `s` come from the speaker's audio. `last` = last word's s + .5.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| quote mark (fade, scale 1.6→1, rotate −8→0, y −30→0) | first word −.45 | .80 | back.out(1.7) | to the end | — | — |
| word i (fade, y 26→0, blur 6→0) | s_i − .04 | .42 | power3.out | to the end | — | — |
| key-phrase underline per word (--u 0→1) | s_i | until the next word (≥ .18 s) | linear | — | — | — |
| whole quote settle (y 0→−8) | 0 | clip duration | sine.inOut | — | — | — |
| hairline (scaleX 0→1) | last | .70 | expo.out | — | — | — |
| name / role (fade, x ∓24→0) | last+.15 / +.30 | .60 | power3.out | — | — | — |
| star i (fade, scale .2→1, rotate −40→0) | last+.55 + i×.09 | .45 | back.out(2.6) | — | — | — |
| brand text (fade) | last+1.2 | .60 | — | — | — | — |
- Voice sync is the whole trick: each word appears exactly as it's said (a lift + blur-to-sharp, never a pop), and the underline sweeps across the key phrase at speaking speed.
- Without speech: pass `quote` + `t` and the words build on a .16 s stagger.

## Typography
- Latin: DM Serif Display 400 quote (72 px default; sample 74), Manrope 700 name (40 px), Manrope 500 role (30 px, +.04em), brand text 24 px +.28em.
- Hebrew: `pair: "suez"` (default) = Suez One quote, Secular One attribution. RTL: text right-aligned, the mark mirrored, underline and hairline grow from the right, name/role slide from the right. Stars stay LTR.
- Maximum copy: ~15 words at 72 px in a 640 px column (≈ 5 lines). Longer quotes: lower `size` to 60 or shorten.

## Colour and surface
- `ink: "dark"` (default): text #1c1712, sub rgba(28,23,18,.72): for bright walls/windows behind the quote. `ink: "light"`: white text + the scrim, for dark backgrounds.
- `colors.accent` #d9892b (underline, hairline, stars), `colors.mark` #b8651a (quote mark).
- No card or panel: the quote sits directly on the footage, which is what makes it feel editorial. If the background is busy, use `ink: "light"` (with scrim) rather than adding a box.

## Layout and safe zones (1920×1080 canvas)
- `side` left → x 120; right → x 1920−120−width. `width` 640, `top` 250 (sample 300). The mark sits 140 px above the text.
- Industry convention: the quote goes on the side the person is NOT on, at eye level or just below; name and role are always shown with a customer quote.
- 9:16: width ≈ 900, size ≈ 64, top in the upper third above the face or in the lower third below the chin.

## What the footage must give you
- Shoot it like this: one take (or the quote's full sentence without cuts), the speaker medium close-up on one side, a calm bright wall/window (for dark ink) or dark background (light ink) on the other ~35%; locked-off; clean audio of the quote.
- Word timings: `python scripts/word_times.py` (for TTS lines) or a Gemini transcription with word timestamps for real speech (the sample's timings came from Gemini). Each word: `{"w": "really", "s": 1.03, "e": 1.48}` (`e` is optional, unused).
- Tracking: none. Matte: not needed.
- Good footage: customer by a window, soft light, looking just off camera. Bad: the speaker centred in a tight close-up, a patterned wall behind the text.

## Build it
### A. With the kit
```bash
python scripts/run_style.py QUOTE-TESTIMONIAL --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| words | [{w, s, e}] word timings; the quote text is these words | required unless `quote` |
| quote + t | text + start time, when there is no speech | —, .8 |
| key | [first word index, last word index] for the underline | none |
| person / role | attribution | "" |
| stars | 0–5 | 5 |
| logo | short brand text under the stars | none |
| side | "left" or "right" | "left" |
| ink | "dark" or "light" | "dark" |
| size / width / top | quote px / column px / top px | 72 / 640 / 250 |
| language / pair | he/en; Hebrew pair | en / "suez" |
| fonts | override | DM Serif Display 400 / Manrope 500 |
| colors | {accent, mark} | #d9892b, #b8651a |
| sfx | soft thump on the mark, click on the hairline, tiny pops per star | true |
| plate_vol | the speaker's voice is the soundtrack | .95 |
| music, music_vol, name | — | none, .35 |
```json
{
 "clip": "clips/dana.mp4",
 "words": [{"w": "We", "s": 0.6}, {"w": "cut", "s": 0.8}, {"w": "our", "s": 1.05}, {"w": "support", "s": 1.25}, {"w": "time", "s": 1.7}, {"w": "in", "s": 1.95}, {"w": "half.", "s": 2.1}],
 "key": [3, 6], "person": "Dana Cohen", "role": "Head of Support · Acme", "side": "right", "ink": "dark"
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const W = [0.67, 0.83, 1.03, 1.52, 2.15, 2.48, 3.0], KEY = [3, 6], last = W[W.length - 1] + .5;
tl.fromTo("#qm", {opacity: 0, scale: 1.6, rotation: -8, y: -30}, {opacity: 1, scale: 1, rotation: 0, y: 0, duration: .8, ease: "back.out(1.7)"}, W[0] - .45);
W.forEach((s, i) => tl.fromTo("#w" + i, {opacity: 0, y: 26, filter: "blur(6px)"},
  {opacity: 1, y: 0, filter: "blur(0px)", duration: .42, ease: "power3.out"}, s - .04));   // each word on its spoken time
for (let i = KEY[0]; i <= KEY[1]; i++) {                                                    // underline at speaking speed
  const nxt = i + 1 < W.length ? W[i + 1] : W[i] + .4;
  tl.fromTo("#w" + i, {"--u": 0}, {"--u": 1, duration: Math.max(.18, nxt - W[i]), ease: "none"}, W[i]);
}
tl.fromTo("#att .ln", {scaleX: 0}, {scaleX: 1, duration: .7, ease: "expo.out"}, last);
for (let i = 0; i < 5; i++) tl.fromTo(`#stars span:nth-child(${i + 1})`, {opacity: 0, scale: .2, rotation: -40},
  {opacity: 1, scale: 1, rotation: 0, duration: .45, ease: "back.out(2.6)"}, last + .55 + i * .09);
// CSS: .w.k::after { transform: scaleX(var(--u, 0)); transform-origin: 0 50% }
```

## Adapting it to the user's project
- Content: the customer's exact words (verbatim from the audio), a real name and role; stars only if they're a real rating.
- Language: Hebrew → `"language": "he"`; Hebrew word timings from the transcription.
- Brand: accent = brand colour; `logo` = the brand name in text.
- Vertical 9:16: see layout.
- Longer testimonials: one quote card per sentence, each on its own clip section.

## Sound
- `soft_thump` (.35) as the mark drops, `soft_click` (.3) on the hairline, `ui_pop` (.12) per star. Keep music low (.35): the voice is the soundtrack.

## Pitfalls and QA checklist
- [ ] Word times match the audio (± 50 ms): scrub a few words.
- [ ] The quote never overlaps the face; side chosen accordingly.
- [ ] Ink matches the background (dark on bright, light + scrim on dark).
- [ ] The quote is verbatim and attributed to a real person.
- [ ] Hebrew: right-aligned, mark mirrored, underline grows from the right.
