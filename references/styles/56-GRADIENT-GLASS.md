# #56 GRADIENT-GLASS · SaaS / tech launch card

> A frosted glass card tilts in and settles over a gradient plate, a light glint travels across it, a shimmering NEW pill, a flowing gradient headline and a subhead appear, floating glass feature chips drift around it, and a cursor glides to the call-to-action button and clicks it (press + double ripple).
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/gradient-glass.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_GRADIENT-GLASS.mp4
> Runner: run_style GRADIENT-GLASS · Example: examples/gradient-glass/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: SaaS product launches, app feature announcements, AI tool promos, waitlist / early-access videos, pricing reveals, conference sponsor loops: the "Linear/Vercel/Apple-glass" look.
- Avoid when: the footage is people or real places (the glass card is centred and covers the middle), the brand is earthy/analog, or you need more than a headline + one line.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#card` | 800×480 px glass card at x 560, y 300 (centred): white 16%→5% gradient, blur 26 px + saturate 1.3, radius 36, big soft shadow, inset top highlight | 3D: `transformPerspective` 1400 |
| `#card::before` | 1.5 px gradient border (white 70% → 8% → 50%) via a mask-composite ring | the "glass edge" |
| `#glint i` | a 120 px diagonal light band inside the card | sweeps once |
| `#pill` | "NEW · v4.0" pill with its own shimmer | 24 px, +.14em |
| `#ttl` | the headline, 112 px, −.035em, gradient-clipped text (3 stops, 200% wide, slowly flowing) | |
| `#sub` | subhead 34 px, 86% white, max 720 px | |
| `#cta` | white button (30 px, weight 600) with a purple shimmer | the cursor clicks it |
| `.chip` | up to 4 floating feature chips (dark glass, 28 px, gradient dot) at fixed spots around the card | (340,330), (1400,280), (1430,700), (300,760) |
| `#cur` / `#rip` | SVG cursor + two ripple rings | |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| card (fade, scale .86→1, rotationX 18→0, y 60→0) | t (.6) | 1.30 | expo.out | whole clip | — | — |
| card breathing tilt (rotationY −3→3) | t | clip end − t | sine.inOut | — | — | — |
| glint sweep (x −400→1100) | t+.9 | 1.40 | power2.inOut | — | — | — |
| pill (fade, y 14→0) + shimmer | t+.5 / t+1.2 | .60 / 1.10 | power3.out / power2.inOut | — | — | — |
| headline (fade, y 30→0, blur 12→0) | t+.7 | 1.00 | expo.out | — | — | — |
| headline gradient flow (background-position 0→100%) | t | clip end − t | linear | — | — | — |
| subhead (fade, y 18→0) | t+1.1 | .80 | power3.out | — | — | — |
| CTA (fade, y 18→0, scale .96→1) + shimmer | t+1.4 / t+2.4 | .70 / 1.00 | back.out(1.8) / power2.inOut | — | — | — |
| chip i (fade, y 40→0, scale .9→1) then float ±14 px | t+1.8 + i×.22 / t+2.6 + i×.22 | .80 / 2.6 yoyo ×2 | back.out(1.6) / sine.inOut | — | — | — |
| cursor enters (1700,1000 → 1500,900) | click−2.0 | .40 | — | — | fades + y +40 at click+1.4, .6 s | power2.in |
| cursor to the CTA centre | click−1.6 | 1.30 | power3.inOut | — | — | — |
| press: cursor .82, CTA .95 (yoyo) | click | .09 ×2 | — | — | — | — |
| ripple rings (scale .2→2.2 / →3, fade) | click+.05 / +.15 | .80 / 1.10 | power2.out | — | — | — |
- The cursor target is measured from layout (`offsetLeft/Top`), not from the animated transform, so it lands where the button settles.
- The signature move: the card tilting up out of perspective with a blur-to-sharp gradient headline, then a slow living tilt and a flowing gradient. Premium calm, never static.

## Typography
- Latin: Sora 800 headline (112 px) and CTA (600, 30 px); Manrope 500 pill, subhead, chips.
- Hebrew: `pair: "secular"` (default): Secular One, RTL card; gradient text works in Hebrew too. Letter-spacing 0.
- Maximum copy: headline ≈ 14 characters (one line in 800 px at 112 px), subhead ≈ 45, CTA ≈ 22, chips ≈ 16 each.

## Colour and surface
- `colors.grad` 3 stops (#b69cff, #6fb8ff, #ff9e7a): headline gradient and chip dots; `colors.text` #ffffff. CTA shimmer uses rgba(182,156,255,.55), CTA text #141024.
- Brand swap: set `grad` to the brand's 3-stop gradient; the plate should share its hues.
- Surfaces: glass (blur 26 on the card, 16 on the chips), gradient borders, soft purple-black shadows.

## Layout and safe zones (1920×1080 canvas)
- Card fixed at the centre (x 560–1360, y 300–780); chips at the four fixed spots; the cursor comes from the lower right.
- Industry convention: one product name, one promise, one action. The CTA text matches the landing page button.
- 9:16: the card is 800 px wide: fits a vertical frame if you move it (edit left/top in the builder CSS) and drop to 2 chips.

## What the footage must give you
- Shoot it like this: one take, 6–20 s, an abstract gradient/glass/liquid plate with movement at the edges and a calm centre; no people, no text.
- Generate it (Kling/Seedance): "abstract frosted glass shapes and soft gradient light in [brand hues], slow drifting motion around the edges, the centre calm and softly lit, no text, no logos".
- Tracking: none. Matte: not needed.
- Good footage: abstract 3D glass, soft gradients, product render backgrounds. Bad: busy centre, people, readable screens.

## Build it
### A. With the kit
```bash
python scripts/run_style.py GRADIENT-GLASS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| title | headline | required |
| pill / sub / cta | pill text / subhead / button text | none |
| chips | up to 4 feature chips | [] |
| t | card entrance | .6 |
| click | cursor click time | 6.4 |
| cursor | show the cursor (needs `cta`) | true |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Sora 800 / Manrope 500 |
| colors | {grad [3], text} | see above |
| sfx | whoosh, glass ting, pop per chip, click | true |
| plate_vol, music, music_vol, name | — | .4, none, .5 |
```json
{
 "clip": "clips/abstract.mp4",
 "pill": "NEW · 2.0", "title": "Meet Lumen.", "sub": "Notes that write themselves.",
 "cta": "Start free  →", "chips": ["AI summaries", "Offline", "Team spaces"],
 "t": 0.6, "click": 6.4,
 "colors": {"grad": ["#9dfcd3", "#5ab7ff", "#b69cff"]}
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const T = .6, DUR = 10, CLICK = 6.4;
gsap.set("#card", {transformPerspective: 1400});
tl.fromTo("#card", {opacity: 0, scale: .86, rotationX: 18, y: 60}, {opacity: 1, scale: 1, rotationX: 0, y: 0, duration: 1.3, ease: "expo.out"}, T);
tl.fromTo("#card", {rotationY: -3}, {rotationY: 3, duration: DUR - T, ease: "sine.inOut"}, T);          // living tilt
tl.fromTo("#ttl", {opacity: 0, y: 30, filter: "blur(12px)"}, {opacity: 1, y: 0, filter: "blur(0px)", duration: 1, ease: "expo.out"}, T + .7);
tl.fromTo("#ttl", {backgroundPosition: "0% 50%"}, {backgroundPosition: "100% 50%", duration: DUR - T, ease: "none"}, T); // gradient flow
tl.fromTo("#glint i", {x: -400}, {x: 1100, duration: 1.4, ease: "power2.inOut"}, T + .9);
const cd = document.getElementById("card"), ct = document.getElementById("cta");                      // layout, not transforms
const cx = cd.offsetLeft + ct.offsetLeft + ct.offsetWidth / 2, cy = cd.offsetTop + ct.offsetTop + ct.offsetHeight / 2;
tl.fromTo("#cur", {x: 1700, y: 1000, opacity: 0}, {x: 1500, y: 900, opacity: 1, duration: .4}, CLICK - 2);
tl.to("#cur", {x: cx - 8, y: cy - 6, duration: 1.3, ease: "power3.inOut"}, CLICK - 1.6);
tl.to("#cta", {scale: .95, duration: .09, yoyo: true, repeat: 1}, CLICK);
```

## Adapting it to the user's project
- Content: product name, one-line promise, the real CTA text.
- Language: Hebrew → `"language": "he"`.
- Brand: `grad` = brand gradient; generate the plate in the same hues.
- Vertical 9:16: see layout.
- Longer clips: the tilt and gradient flow stretch over the whole clip; chips float 3 cycles (≈ 7.8 s).

## Sound
- `ui_whoosh` (.3) at the card, `glass_ting` (.3) at t+1, `ui_pop` (.15) per chip, `soft_click` (.5) on the click.

## Pitfalls and QA checklist
- [ ] The headline fits one line (≈ 14 characters).
- [ ] The cursor tip lands on the button centre.
- [ ] The plate's centre stays calm behind the card.
- [ ] Gradient text renders in the final MP4 (background-clip:text): check a frame.
- [ ] Chips don't collide with plate highlights or leave the frame.
