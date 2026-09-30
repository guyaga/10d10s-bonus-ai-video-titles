# #49 SOCIAL-CTA · Subscribe / follow call to action

> A channel chip (avatar, name, handle, counting subscriber number) slides in; later a red SUBSCRIBE pill pops with a bell and a like button, a cursor glides in and clicks it (press + ripple), the pill flips to a grey SUBSCRIBED with a check, the bell rings with sparkles and the like count climbs.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/social-cta.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_SOCIAL-CTA.mp4
> Runner: run_style SOCIAL-CTA · Example: examples/social-cta/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: YouTube intros/outros, creator clips, podcast promos, Instagram/TikTok "follow for more" moments, course and newsletter sign-up asks.
- Avoid when: the creator is not on screen or not talking to camera (the ask feels detached), or the platform has its own end screen in that time window (see END-SCREEN).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#chip` | pill: dark glass `rgba(12,14,18,.72)` + blur 16 px, 78 px gradient avatar (initial), name 36 px, handle · counted subscribers 23 px | 150 px above the CTA row |
| `#row` | the CTA row at `pos` (x, y), always LTR | pill + bell + like |
| `#sub` | 96 px tall red pill (min 330 px), two stacked labels: SUBSCRIBE and ✓ SUBSCRIBED (grey #3a3f47) | the check is an inline SVG |
| `#rip` | white ripple circle | scales ×9 on the click |
| `#bell` | 96 px dark glass circle, SVG bell, three yellow sparkles | rings with rotate keyframes |
| `#like` | dark glass pill with an SVG thumb and a counted number | |
| `#cur` | an SVG arrow cursor with drop shadow | glides, clicks, leaves |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| chip (fade, x ∓60→0) | channel.t | .70 | expo.out | to channel.until | fade + x ∓40 at until−.4, .4 s | power3.in |
| avatar (scale .4→1, rotate −30→0) | channel.t+.1 | .60 | back.out(2.4) | — | — | — |
| subscriber count | channel.t+.4 | 1.40 | easeOut cubic (+1 after the click) | — | — | — |
| subscribe pill (scale 0→1) | cta.t | .55 | back.out(2.2) | — | — | — |
| bell (scale 0→1) | cta.t+.15 | .50 | back.out(2.4) | — | — | — |
| like (scale 0→1) | cta.t+.30 | .50 | back.out(2.4) | — | — | — |
| cursor glide in (from +260,+260) | click−.9 | .50 | power2.out | — | — | — |
| cursor onto button | click−.4 | .35 | power3.inOut | — | exits +150,+160 at click+.7, .6 s | power2.in |
| click: cursor .82, pill .93 (yoyo) | click | .08 ×2 | — | — | — | — |
| ripple (scale 0→9, fade) | click | .60 | power2.out | — | — | — |
| label flip SUBSCRIBE → ✓ SUBSCRIBED | click+.08 | .15 / .20 | — | — | — | — |
| bell ring (rotate 22, −20, 14, −8, 0) + sparkles | click+.45 / +.5 | .5 total / .6 stagger .06 | power2.out | — | — | — |
| like thumb bump (scale 1.35, rotate −14 → 1) + count | click+1.0 | .14 + .25 / 1.2 | back.out(3) / easeOut cubic | — | — | — |
- Timing: ask about 1 s before the click (cta.t → click ≈ 1.1–1.2 s); if the creator points at the button, put `click` on the point.
- The signature move: a real-feeling click: cursor ease-in, a press (both cursor and pill shrink for 80 ms), the ripple, and the label flip.

## Typography
- Latin: Manrope 700 name/button/counts, Manrope 500 handle line. Button 40 px, +.06em.
- Hebrew: `pair: "secular"` (default): Secular One. Labels default to "הירשמו" / "נרשמתם". The chip mirrors (slides from the right); the button row stays LTR. The @handle is bidi-isolated (`direction:ltr; unicode-bidi:isolate`): without it "@studio.north" rendered as "studio.north@".
- Numbers are formatted 128.4K / 1.2M, always LTR.
- Maximum copy: channel name ≈ 18 characters, button label ≈ 12.

## Colour and surface
- Roles: `red` #ff0033 (button + glow), `done` #3a3f47 (subscribed), `panel` rgba(12,14,18,.72) (chip, bell, like). Avatar gradient #ff8a3d→#ff2e63, sparkles #ffd23f.
- No platform logos: the red pill and the bell read as "subscribe" by convention. For Instagram-style: `red: "#0095f6"`, labels "Follow" / "Following".

## Layout and safe zones (1920×1080 canvas)
- `pos`: x 150, y 760 (top-left of the CTA row); chip at y−150. The cursor targets x+165, y+60 (the pill centre for the default width): if you change the label length a lot, check the cursor lands on the pill.
- Industry convention: subscribe asks sit in the lower third on the side opposite the face, early (0:05–0:30) or at the end before the end screen.
- 9:16: pos ≈ {x: 90, y: 1300} on a vertical canvas; keep clear of the platform's right-side button rail and bottom caption.

## What the footage must give you
- Shoot it like this: one take, 6–20 s, a creator talking to camera, centred or to one side, the lower-left (or lower-right) calm; tripod.
- Tracking: none. Matte: not needed.
- Good footage: talking head at a desk, a creator pointing down to where the button lands. Bad: the creator's hands or a mic in the CTA zone.

## Build it
### A. With the kit
```bash
python scripts/run_style.py SOCIAL-CTA --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| channel | {name, handle, subs, initial, t, until} | none; t .8 |
| cta | {t, click, label, done, bell, like} | 6.2, 7.2, SUBSCRIBE/הירשמו, SUBSCRIBED/נרשמתם, true, none |
| pos | {x, y} of the CTA row | 150, 760 |
| language / pair | he/en; Hebrew pair | en / "secular" |
| fonts | override | Manrope 700 / 500 |
| colors | {red, done, panel} | see above |
| sfx | pop, click, chime (+ pop for like, whoosh for chip) | true |
| music, music_vol, plate_vol, name | — | none, .5, .85 |
```json
{
 "clip": "clips/creator.mp4",
 "channel": {"name": "Acme Labs", "handle": "@acmelabs", "subs": 48200, "initial": "A", "t": 0.8, "until": 4.6},
 "cta": {"t": 6.0, "click": 7.2, "bell": true, "like": 3100},
 "pos": {"x": 150, "y": 780}
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const T = 6.0, CLICK = 7.2, bx = 150 + 165, by = 780 + 60;
tl.fromTo("#sub", {scale: 0, opacity: 0}, {scale: 1, opacity: 1, duration: .55, ease: "back.out(2.2)"}, T);
tl.fromTo("#cur", {x: bx + 260, y: by + 260, opacity: 0}, {x: bx + 60, y: by + 30, opacity: 1, duration: .5, ease: "power2.out"}, CLICK - .9);
tl.to("#cur", {x: bx, y: by, duration: .35, ease: "power3.inOut"}, CLICK - .4);
tl.to("#cur", {scale: .82, duration: .08, yoyo: true, repeat: 1}, CLICK);       // press
tl.to("#sub", {scale: .93, duration: .08, yoyo: true, repeat: 1}, CLICK);
tl.fromTo("#rip", {scale: 0, opacity: .8}, {scale: 9, opacity: 0, duration: .6, ease: "power2.out"}, CLICK);
tl.to("#sub .l1", {opacity: 0, duration: .15}, CLICK + .08);
tl.to("#sub .l2", {opacity: 1, duration: .2}, CLICK + .08);                     // ✓ SUBSCRIBED (SVG check)
tl.to("#bell .bi", {keyframes: [{rotate: 22, duration: .08}, {rotate: -20, duration: .1}, {rotate: 14, duration: .1}, {rotate: -8, duration: .1}, {rotate: 0, duration: .12}]}, CLICK + .45);
tl.to("#cur", {x: bx + 150, y: by + 160, opacity: 0, duration: .6, ease: "power2.in"}, CLICK + .7);
```

## Adapting it to the user's project
- Content: the user's real channel name, handle and subscriber count; `like` optional.
- Language: Hebrew → `"language": "he"`; isolate the handle; numbers LTR.
- Brand: avatar initial + brand colour in `red` (or keep platform red for recognition).
- Vertical 9:16: see layout.
- Longer clips: put the chip early and the click near the creator's verbal ask.

## Sound
- `ui_pop` (.5) when the pill appears, `soft_click` (.8) on the click, `chime` (.5) with the bell, `ui_pop` (.4) on the like, `ui_whoosh` (.35) with the chip.

## Pitfalls and QA checklist
- [ ] The cursor tip lands on the pill (re-check if the label is much longer/shorter than default).
- [ ] @handle bidi-isolated in Hebrew; counts LTR.
- [ ] No ✓ character in Hebrew fonts: the check is SVG.
- [ ] CTA row clear of hands, mic and the face.
- [ ] Not inside the last 5–20 s if the video will get a YouTube end screen (their elements cover it).
