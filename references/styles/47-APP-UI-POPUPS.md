# #47 APP-UI-POPUPS · Floating phone UI

> Phone-style notification banners drop in with a spring and stack like iOS (each new one pushes the older ones down, smaller and dimmer), an app card fills a progress ring, and a toast with a check confirms the action. Frosted glass, soft shadows, app icons drawn in CSS gradients.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/app-ui-popups.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_APP-UI-POPUPS.mp4
> Runner: run_style APP-UI-POPUPS · Example: examples/app-ui-popups/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: app and fintech ads, delivery/booking flows, "a day with our app" stories, SaaS feature promos, UGC-style ads where the phone screen isn't shown: the UI floats beside the person instead.
- Avoid when: the real phone screen is visible (the floating UI then contradicts it), or you need the actual product UI (use screen recordings).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#ui` | the stack area at `area.x`, `area.top`, width `area.w` | banners are absolutely stacked at top 0 |
| `.nt` | a banner: `rgba(246,247,250,.94)`, blur 24 px + saturate 1.6, radius 30 px, shadow 0 18 50 | `transform-origin: 50% 0` |
| `.ic` | 64 px rounded-square icon, CSS gradient `grad`, a letter/digits/symbol inside | no logos: use a letter |
| `.nh` | header row: app name (20 px, caps in Latin) + time ("now") | |
| `.ntl` / `.nbd` | title (30 px, dark) / body (25 px) | |
| `#card` | dark glass app card `rgba(12,14,20,.72)` at top 620 px, radius 32 px: 120 px progress ring + title/sub + 8 px bar | optional |
| `#toast` | black pill, green check circle (inline SVG), 30 px text, centred under the stack at top 920 px | optional |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| banner i (y −170→0, fade, scale .92→1) | note.t | .75 | back.out(1.4) | stays in the stack | all leave at until−.5 (fade, y −20, .4 s, stagger .05) | power2.in |
| older banners (push down) | each new note.t | .60 | power3.out | — | depth ≥ 3 → fade to 0 | — |
| card (fade, y 40→0, scale .95→1) | card.t | .70 | expo.out | — | with the stack | — |
| ring + bar fill to `ring` | card.t+.3 | 1.80 | power2.inOut | — | — | — |
| ring % label | card.t+.3 | 1.80 | easeInOut (time-driven) | — | — | — |
| toast (fade, y 30→0, scale .8→1) | toast.t | .50 | back.out(2.2) | — | with the stack | — |
- The stack: slot 150 px; an older banner moves to y = depth × 150 × .82 and scales 1 − depth × .05; the 3rd-oldest fades out.
- Beat: one banner every ~1.4–1.6 s (sample 1.0, 2.6, 4.0), card at ~5.6, toast at ~8.2.
- The signature move: the spring drop with the stack pushing back and dimming: instantly reads as "phone".

## Typography
- Latin: Manrope 700 title/card/toast, Manrope 500 app name (caps, +.04em), time and body.
- Hebrew: `pair: "secular"` (default): Secular One throughout, RTL, no caps. Percentages and the ring label stay LTR.
- Glyph lesson: the icon, ✓ and ₪ must exist in the chosen font. None of Suez One / Karantina / Secular One has ₪ or ✓: write amounts as "240 ש״ח"; the kit draws the toast check as an inline SVG path, not a character. Use a Hebrew letter or digits as the icon.
- Maximum copy: title ≈ 28 characters, body ≈ 40 (one line looks right; two lines push the stack), toast ≈ 24.

## Colour and surface
- Banners: light iOS glass (#f6f7fa at 94%) with dark text #0d1117 / #30363d / #4b5563. Card: dark glass with white text. Ring/bar/check: #35d07f.
- Brand swap: set each note's `grad` to the app's colours (two stops); change #35d07f in the builder CSS if the brand needs another success colour.

## Layout and safe zones (1920×1080 canvas)
- `area`: x 1160 (left edge of the stack, px), top 110, w 620. The card is fixed at top 620 px, the toast at top 920 px, centred on the stack. With three banners + card + toast the right side is full: check the bottom 5%.
- The stack sits wherever `x` puts it. `area.side` is accepted but does not move the stack; for a left-side stack set `x` ≈ 96.
- Industry convention: phone notifications come from the top and stack downward; confirmation toasts sit low and centred.
- 9:16: x ≈ 60, w ≈ 960, top ≈ 260; skip the card.

## What the footage must give you
- Shoot it like this: one take, 6–20 s, a person using a phone in the left third (screen never visible), right two thirds soft and empty; locked-off, shallow depth of field.
- Tracking: none. Matte: not needed.
- Good footage: someone on a sofa/café/street glancing at their phone, a hand holding a phone out of focus. Bad: the screen facing the camera, busy backgrounds on the UI side.

## Build it
### A. With the kit
```bash
python scripts/run_style.py APP-UI-POPUPS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| notes[] | {app, icon, grad [2 colours], title, body, time, t} | required; grad #5b8cff→#3a55d9, time "now" |
| card | {title, sub, ring 0–1, t} | none; ring .7 |
| toast | {text, t} | none |
| area | {side, x, top, w} | R, 1160, 110, 620 (side unused) |
| until | everything leaves | none |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Manrope 700 / 500 |
| sfx | glass ting per banner, whoosh on card, chime on toast | true |
| music, music_vol, plate_vol, name | — | none, .5, .6 |
```json
{
 "clip": "clips/phone.mp4",
 "area": {"x": 1180, "top": 100, "w": 600},
 "notes": [
  {"app": "Wallet", "icon": "W", "grad": ["#34c759", "#0a8f3a"], "title": "Payment received", "body": "Noa sent you $40 · Friday dinner", "t": 1.0},
  {"app": "Rides", "icon": "R", "grad": ["#111827", "#374151"], "title": "Your driver is here", "body": "Grey sedan · 2 min", "t": 2.6}
 ],
 "card": {"title": "Your order is on the way", "sub": "12 min · 2.4 km", "ring": 0.72, "t": 5.0},
 "toast": {"text": "Payment approved", "t": 7.8}
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const N = [1.0, 2.6, 4.0], SLOT = 150;
N.forEach((t0, i) => {
  tl.fromTo(`#n${i}`, {y: -170, opacity: 0, scale: .92}, {y: 0, opacity: 1, scale: 1, duration: .75, ease: "back.out(1.4)"}, t0);
  for (let k = 0; k < i; k++) {           // push the older banners down, smaller, dimmer
    const d = i - k;
    tl.to(`#n${k}`, {y: d * SLOT * .82, scale: 1 - d * .05, opacity: d >= 3 ? 0 : 1, duration: .6, ease: "power3.out"}, t0);
  }
});
tl.fromTo("#ring", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 1 - .72}, duration: 1.8, ease: "power2.inOut"}, 5.9);
// centre the toast with xPercent in the SAME tween: a CSS translate(-50%) would be overwritten by GSAP's y/scale
tl.fromTo("#toast", {opacity: 0, y: 30, scale: .8, xPercent: -50}, {opacity: 1, y: 0, scale: 1, xPercent: -50, duration: .5, ease: "back.out(2.2)"}, 8.2);
```

## Adapting it to the user's project
- Content: the user's real app flow in 3 steps (trigger → progress → success). Keep each banner to one idea.
- Language: Hebrew → `"language": "he"`; amounts as ש״ח; Hebrew letter icons.
- Brand: `grad` per app; the card colour stays dark glass.
- Vertical 9:16: see layout.
- Longer clips: more notes (only 3 stay visible); set `until` before the end card.

## Sound
- `glass_ting` (.5) per banner, `ui_whoosh` (.35) on the card, `chime` (.5) on the toast.

## Pitfalls and QA checklist
- [ ] The phone screen is not visible in the footage.
- [ ] No ₪ or ✓ characters in Secular One/Suez One/Karantina text (ש״ח; SVG check).
- [ ] Toast centred with xPercent inside the GSAP tween (a CSS transform on it gets overwritten).
- [ ] The stack, card and toast clear the bottom 5% and don't overlap the person.
- [ ] Icons are letters/digits, never real brand logos.
