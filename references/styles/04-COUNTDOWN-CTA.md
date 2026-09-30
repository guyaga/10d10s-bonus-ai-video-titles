# #04 COUNTDOWN-CTA · Flash-sale countdown

> The selling end of a video: a FLASH SALE stack slams in beat by beat (label, struck-through total, big sale price,
> discount note), a black OFFER ENDS IN box runs a live 00:15 countdown with a shrinking red rule, item tiles show sale
> prices, and a SHOP NOW button pulses.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/countdown-cta.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/D3_look08_runway_countdown_30s.mp4
> Runner: run_style COUNTDOWN-CTA (`scripts/styles/runway.py`, the `countdown` block) · Example: examples/countdown-cta/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: the last 10–15 s of an e-commerce video: drops, launches, limited offers, bundles; pairs with #01 (the
  same spec can carry both: escort first, countdown at the end).
- Avoid when: there is no real offer (a fake countdown hurts trust); the subject moves a lot during the sale (the stack
  covers the right 40 % of the frame for 15 s); brand films without a price.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | subject should hold still in the centre-left for the sale |
| Rail (optional) | stack of item tiles top-left: image + sale price + struck original | `rail: true` and items with images |
| CTA stack, top-right | pill (FLASH SALE) · italic label · struck total · big sale price · discount note | x = right 80, y = 70, 560 px wide |
| Timer box | OFFER ENDS IN + 00:SS + progress rule | right 80, y 740, 560 px wide |
| SHOP NOW button | accent button, bottom centre | pulses every 2 beats |
| Flash | white flash on each stomp | shared with the stomp family |

## Timing and motion
`CD0 = B(countdown.beat)`; `B(n) = offset + n × 60/bpm`. With 120 BPM one beat = 0.5 s.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Pill FLASH SALE | CD0 | stomp from 2.0, 0.16 s | power4.out | to the end | — | — |
| Timer box | CD0 | stomp from 1.6 | power4.out | to the end | — | — |
| Label "the complete look" | B(cb+1) | 0.18 s, x 30 → 0 | power3.out | — | — | — |
| Struck total | B(cb+1) | 0.15 s, y 20 → 0; strike bar scaleX 0 → 1 in 0.2 s at B(cb+2) | default / power3.out | — | — | — |
| Rail tiles | B(cb+1) | 0.16 s each, x −40 → 0, stagger 0.5 s | back.out(2) | — | — | — |
| Sale price | B(cb+3) | stomp from 2.1 | power4.out | — | — | — |
| Discount note | B(cb+4) | 0.16 s, y 14 → 0 | default | — | — | — |
| SHOP NOW | B(cb+5) | stomp from 1.7 | power4.out | pulses scale 1.08 → 1 in 0.3 s (power2.out) every 2 beats from B(cb+7) | — | — |
| Countdown digits | every frame | text `00:SS`, SS = seconds − floor(t − CD0); rule scaleX = 1 − (t − CD0)/seconds | linear | — | — | — |
| Last `hot_last` seconds (5) | CD0 + sec | digits turn accent; scale 1.25 → 1 in 0.25 s + half-strength shake, once per second | power3.out | — | — | — |

- The signature move: **every piece of the offer is its own hit**, 1 beat apart (pill+timer → label/total → strike →
  price → note → button), then the clock takes over: a tick every second, a pulse + shake every second of the last five.
- Beat sync: put `countdown.beat` on a phrase start of the music; the countdown itself is in real seconds, not beats.

## Typography
- Latin: pill Anton 46 px; label Bodoni Moda italic 40 px; struck total Anton 64 px; sale price Anton 150 px (paper fill,
  3 px ink stroke, 8 px ink shadow); note Archivo 700 26 px .12em; timer label Archivo 700 22 px .2em (150 px wide, wraps
  to 2 lines); digits Anton 120 px; button Anton 60 px; rail price Anton 36 px, original Archivo 700 18 px struck.
- Hebrew: `"fonts": {"display": "Karantina", "serif": "Suez One", "body": "Secular One"}`; pill/price/button in Karantina
  700, the label in Suez One, note/timer label in Secular One. Set `"currency": "ש״ח"` (writes `1,912 ש״ח`), translate
  `pill`, `label`, `note`, `timer_label`, `button`. The clock `00:15` stays LTR digits. Never ₪.
- Max copy: pill ≤ 12 characters, label ≤ 20, note ≤ 32, button ≤ 12; price ≤ 7 characters at 150 px in 560 px.

## Colour and surface
- Roles: `paper` `#f6f1e8` (light boxes, price fill), `ink` `#16130f` (timer box, borders, shadows), `accent` `#ff3d2e`
  (pill, strike bar, rule, button, hot digits). Brand colours via `colors`; the accent must contrast with ink (the
  hot digits sit on the ink timer box).
- Surfaces: every box has a 3–4 px ink (or paper) border and a hard 8 px ink offset shadow on the button; the timer box
  is solid ink with a 4 px paper border; progress rule 12 px, track `rgba(246,241,232,.2)`.

## Layout and safe zones (1920×1080 canvas)
- CTA stack right 80 / top 70 / width 560; timer right 80 / top 740 / width 560; button centred, bottom 40; rail left 70 /
  top 140. So the subject must sit in the centre, clear of x 1280–1840 and of the bottom 140 px.
- 9:16: the kit composes 16:9; for vertical, the stack and timer need re-positioning via a custom spec (they are fixed
  px). Keep the offer inside the centre column x 656–1264 if you plan a centre crop.

## What the footage must give you
- Shoot it like this: one take, no cuts, 20–30 s · full body, centred; the last 15 s the subject stands in the centre
  facing camera · 30 % free both sides · locked-off with an extremely slow push-in.
- Tracking: only needed if the same spec also runs escorts (#01) or a `big_word`. A countdown-only spec may omit
  `items` and `track` (the builder then derives a frame clock from the clip's duration).
- Matte: only for a `big_word` behind the subject.
- Good: a calm hold / pose for the sale window. Bad: the subject walking across the right side during the offer.

## Build it
### A. With the kit
```bash
python scripts/run_style.py COUNTDOWN-CTA --spec my_spec.json --render
```
`countdown` block:
| Key | Meaning | Default |
|---|---|---|
| beat | beat index the sale starts on | required |
| seconds | countdown length | 15 |
| discount | fraction off | 0.2 |
| pill / label / note / button / timer_label | copy | "FLASH SALE" / "the complete look" / "−20% · NEXT 15 SECONDS ONLY" / "SHOP NOW →" / "OFFER ENDS IN" |
| was / now | override the totals (else sum of item prices and the discounted sum) | computed |
| rail | show the item tiles (items need images) | true |
| hot_last | last N seconds go hot | 5 |
Other keys: the whole #01 table (items, beat, brand, look, big_word, finale, colors, fonts, currency, music…);
`clip` is required, `track` only when there are items or a big word.

A minimal spec for a generic project:
```json
{
 "name": "my-sale",
 "clip": "clips/my_hold.mp4",
 "track": "tracks/my_hold_vtrack.json",
 "beat": {"bpm": 120, "offset": 0.035},
 "items": [
  {"key": "a", "word": "JACKET", "name": "Signal Puffer", "price": 340, "image": "stills/puffer.png", "side": "L", "beat": 4},
  {"key": "b", "word": "CARGO", "name": "Grid Cargo", "price": 180, "image": "stills/cargo.png", "side": "R", "beat": 8}
 ],
 "countdown": {"beat": 12, "seconds": 15, "discount": 0.25, "pill": "DROP 01", "label": "the full fit", "button": "SHOP NOW →"},
 "colors": {"paper": "#f2f1ec", "ink": "#0e0e10", "accent": "#ff6a13"},
 "music": "shared/sfx/my_music.mp3"
}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
const CD0 = B(CB), SECS = 15, HOT = 5;
window.onCD = (t) => {                                        // called every frame from onPlace
  const rem = Math.max(0, SECS - Math.floor(t - CD0));
  document.getElementById("tt").textContent = "00:" + String(t < CD0 ? SECS : rem).padStart(2, "0");
  document.getElementById("tb").style.transform = `scaleX(${t < CD0 ? 1 : Math.max(0, 1 - (t - CD0) / SECS)})`;
  document.getElementById("timer").classList.toggle("hot", t >= CD0 + SECS - HOT);
};
tl.set(["#cta", "#timer", "#buy"], {opacity: 0}, 0); tl.to(["#cta", "#timer", "#buy"], {opacity: 1, duration: .01}, CD0 - .02);
stomp("#cta .pill", CD0, 2); stomp("#timer", CD0, 1.6);
tl.fromTo("#cta .lbl", {opacity: 0, x: 30}, {opacity: 1, x: 0, duration: .18, ease: "power3.out"}, B(CB + 1));
tl.fromTo("#cta .was", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .15}, B(CB + 1));
tl.fromTo("#cta .was i", {scaleX: 0}, {scaleX: 1, duration: .2, ease: "power3.out"}, B(CB + 2));   // the strike
stomp("#cta .now", B(CB + 3), 2.1);
tl.fromTo("#cta .off", {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: .16}, B(CB + 4));
stomp("#buy", B(CB + 5), 1.7);
for (let k = CB + 7; B(k) < CD0 + SECS; k += 2) tl.fromTo("#buy", {scale: 1.08}, {scale: 1, duration: .3, ease: "power2.out"}, B(k));
for (let s = SECS - HOT; s < SECS; s++) { tl.fromTo("#timer .t", {scale: 1.25}, {scale: 1, duration: .25, ease: "power3.out"}, CD0 + s); shake(CD0 + s, .5); }
```

## Adapting it to the user's project
- Content: a real offer (percent off, bundle price, "ends at midnight"); the seconds are a device, 10–15 s reads best.
- Language: Hebrew copy per the typography notes; keep numbers as digits.
- Brand: accent = the brand's action colour; paper/ink = brand light/dark.
- Vertical 9:16: needs repositioned boxes (custom css); plan the offer in the centre column.
- Longer or shorter clips: the sale window must fit fully in the clip: `B(beat) + seconds ≤ clip length`.

## Sound
- A soft tick (0.22) every second of the countdown, a soft pulse (0.35) instead for the last `hot_last` seconds, a soft
  thump (0.45) on the pill, the price and the button; music 0.75, plate 0.15.

## Pitfalls and QA checklist
- [ ] `B(beat) + seconds` ≤ clip length (else the clock never reaches 00).
- [ ] The subject is clear of the right 560 px and the bottom 140 px during the whole window.
- [ ] Totals are correct (struck = sum of prices, sale = rounded discounted sum) or overridden with `was` / `now`.
- [ ] Rail tiles need item `image`s; without images set `"rail": false`.
- [ ] Hebrew: currency "ש״ח", translated button/labels; frames checked + `scripts/qa.py` "ship".
