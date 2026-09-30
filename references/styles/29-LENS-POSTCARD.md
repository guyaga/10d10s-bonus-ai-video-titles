# #29 LENS-POSTCARD · The world through one smart-glasses lens

> The film is seen through a real spectacle lens (a tortoiseshell frame edge, the nose pad, a chromatic fringe, a soft glare) and the assistant is "Stampy", a sun-faced postage-stamp mascot who blinks and lip-syncs the voice in paper speech bubbles. A street sign is repainted in Hebrew right on the tracked board and franked with a red "translated" stamp; a landmark gets a map pin and an airmail postcard; the walk becomes a dotted map line; the order prints as a paper receipt; it ends on a postcard franked by Stampy.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/lens-postcard.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E9_lumen_lens_smart_glasses_BESPOKE.mp4
> Runner: bespoke (`references/recipes/bespoke/E9_glasses_bespoke.py`, 17 s) · Example: none shipped

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: AI wearables and translation apps, travel and tourism, city guides, language learning, playful consumer tech, airlines and hotels speaking to travellers.
- Avoid when: the footage isn't first-person, the brand is serious or technical (this world is warm and playful), or there's no sign/landmark/object to interact with.

## The design method (crafted world)
Ask: **what does this subject's world stamp, mail or hand you?** A traveller's world is paper: postcards, postage stamps, franking marks, airmail envelopes, map pins, phrasebooks, receipts. And the device is a lens you look THROUGH, not a screen with a HUD. So:
1. **Frame the film with the object itself:** a real lens outline (with the nose-bridge cut-out), the tortoiseshell frame outside it softly out of focus (it's millimetres from the eye), a red/cyan chromatic fringe on the glass edge, edge blur and a moving glare.
2. **Give the AI a character from the same world:** a postage stamp with a sun face that blinks every 2.7 s, sways, and opens its mouth with the voice's loudness envelope. It speaks in paper speech bubbles whose words pop in on the VO.
3. **Translation happens ON the world:** the sign's board is tracked and a Hebrew version of it is mapped onto it with a 4-point homography (`matrix3d`), then franked with a red double-bordered "translated" stamp.
4. **Every other title is travel paper:** a map pin with an airmail postcard/phrasebook entry for the landmark, a dotted map line with a red destination pin and a distance countdown, a printed receipt for the order, and a postcard end card with a postmark.

Worked example (LUMEN LENS): boot glow → Stampy: "new city. / you've never been here." → "every sign, suddenly in Hebrew." (the bakery board repainted + "translated" stamp) → "that tower?" (pin + postcard entry) → the walk: dotted line, "40 m → you're here!" → "espresso?" (a receipt prints: the Hebrew order, the local-language line, a price) → the postcard end card franked by Stampy.

It transfers to:
- **An airline or travel-insurance brand:** the airplane window as the "lens"; the mascot is a luggage tag; the destination gets a boarding-pass stub; the end card is a stamped passport page.
- **A language-learning app:** the lens of the phone camera; the mascot is a sticky-note character; objects get flash-card labels in two languages; the end is a completed-lesson stamp card.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#lens` | an SVG: everything outside the lens path filled with tortoiseshell (blur 13) at 94%; a red (+4/+3 px) and cyan (−5/−3 px) fringe stroke on the edge (blur 3.2, screen); a thin white inner line; the silicone nose pad | the lens path has the nose-bridge notch on the left |
| `#lzBlur`, `#lzGlare`, `#boot` | a 5 px backdrop blur toward the lens edge; a 260 px diagonal glare drifting ±40 px; a warm boot glow | |
| `#sign` | a 500 × 660 painted board (cream face, Hebrew "big" lines 176 px, small lines 50 px, a year line) mapped onto the tracked sign with `matrix3d` | a scan line reveals it |
| `#sPill` | the "translated" stamp: a 5 px double red border on cream, red text | slams (scale 1.9 → 1) |
| `#pin` | a red map pin that drops + a postcard box (phrasebook entry: Latin + Hebrew lines) | elastic |
| `#gwrap` | 22 navy dots with white rims along a Bézier path (700,1110 → 1645,815), pulsing in sequence, a red start ellipse | the walk |
| `#dest` | the destination pin + "40 מ׳" counting down to "הגעת!" | |
| `#order` | a paper receipt: header with a cup icon, the Hebrew order 54 px, the local-language line (mono, blue), items with prices, a "thank you" line | prints down from the top |
| `.bub` | paper speech bubbles (62 px, radius 40, a tail, soft shadow), words pop in; accent words red | above Stampy |
| `#mas` | Stampy: a 104 × 128 stamp with perforations, a rotating sun, eyes that blink, a mouth driven by the VO | bottom-left, jumps onto the end card |
| `#end` | the postcard: brand 86 px, tagline 70 px, sub line 29 px, a postmark, Stampy franking it | |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| lens + edge blur | 0 | 0.45 | power2.out | whole piece | — | — |
| boot glow | 0.02 | 0.22 (to .85) | power2.out | — | 0.6 at 0.26 | power2.out |
| Stampy | 0.2 | 0.8 (scale 0 → 1, rotation −40 → 0) | elastic.out(1,.45) | sways, blinks, lip-syncs | jumps to the card at 15.1 (0.55, back.inOut(1.4)) | — |
| bubbles | b1 0.45, b2 1.12, b3 4.28, b4 8.48, b5 13.28 | 0.7 (scale .15 → 1, rotation −6 → 0); words pop on the VO | elastic.out(1,.55) | to 3.75 / 3.75 / 8.2 / 11.7 / 15.15 | 0.22 (scale .7) | back.in(2) |
| detection box on the sign | 4.42 | 0.45 (scale 1.15 → 1) | back.out(2.5) | blinks .35 × 4 from 4.7 | 0.2 at 5.3 | — |
| repainted sign | 5.07 | 0.75 (clip opening top → bottom; a scan line 0 → 655) | power1.inOut | big lines elastic from 5.3 (stagger 0.12) | 0.3 at 8.2 | — |
| "translated" stamp | 5.85 | 0.2 (scale 1.9 → 1) + a 5 px jolt at 6.05 | power4.in | — | 0.25 at 8.0 | — |
| map pin + postcard | 8.85 / 9.0 | pin drop 0.28 (y −90 → 0) + squash 0.45; card 0.7 (scale .2 → 1, rotation −14 → −2.5) | power2.in / elastic.out | — | 0.25 at 11.75 | — |
| dotted walk line | 11.98 | dots pop 0.3, stagger 0.035 | back.out(4) | pulse in sequence | 0.3 at 13.45 | — |
| destination pin | 12.3 | 0.32 drop + elastic squash | power2.in / elastic | countdown 12.55 → 13.3 | 0.25 (scale .8) at 13.45 | back.in(2) |
| receipt | 13.72 | 0.55 (clip opening downward, y −60 → 0) + a swing | power2.out / sine.inOut | — | 0.22 (y −40) at 15.0 | power2.in |
| postcard end | 15.42 | 0.55 (scale .3 → 1, rotation −10 → −1.5) | back.out(1.7) | postmark slams 15.78 (0.16, scale 1.5 → 1) | — | — |
- The sign homography: from the tracked sign box, the four corners are inset (7.5% horizontally, 5%/4.5% vertically, a small k skew) and the 500 × 660 board is mapped onto that quad with a `matrix3d` every frame.
- The signature move: looking THROUGH a physical lens, with the translation painted onto the real sign and franked like mail.

## Typography
- Voice, postcards, sign, receipt Hebrew: **Secular One** (the original used Varela Round and IBM Plex Sans Hebrew; the kit remaps both to Secular One). Bubbles 62 px; the sign's big lines 176 px; the postcard brand 86 px and tagline 70 px.
- Latin data (receipt, phrasebook): **IBM Plex Mono** 400/600 (21–34 px).
- RTL: bubbles and the receipt are `direction: rtl`; the local-language lines are LTR mono aligned right. Prices on the receipt: Latin digits + the local currency (the sample's scene is Europe: €), or ש״ח for Israeli prices.
- Max copy: a bubble ≤ 5 words (max-width 900 px); the sign ≤ 3 big words; the postcard tagline ≤ 3 words.

## Colour and surface
- Navy ink #1d2d50, postal red #d9482b (accent words, stamps, pins), airmail blue #2b62c0, cream paper #fbf5e6, sun yellow #ffc94a; the airmail border is a 135° red/cream/blue/cream stripe (20/10/20/10 px).
- Surfaces: paper with soft shadows, a double-bordered rubber stamp, a tortoiseshell frame, glass fringe.
- Brand swap: Stampy can become the brand's own mascot drawn as a stamp; keep the postal palette or recolour the stripe.

## Layout and safe zones (1920×1080 canvas)
- The lens covers x 14–1906, y −40–1112 with the nose notch on the left (around y 440–600). Stampy sits bottom-left (170, 890); bubbles to its right (left 246, bottom 150). The sign follows the tracked board; the pin/postcard sit near the landmark; the receipt top-right.
- The contract asks for 20% free at the bottom (bubbles and Stampy live there).
- 9:16: the lens becomes a tall oval; Stampy and the bubbles move to the bottom band.

## What the footage must give you
- Shoot it like this: one take, no cuts, 15–20 s · a first-person walk at eye level, gentle head motion · 20% free at the bottom · natural first-person walk, stabilised.
- Seedance lines: "FORMAT: One continuous shot, no cuts." / "CAMERA: natural first-person walk, stabilised, gentle head motion. FORBIDDEN: cuts, shake." / "POSITIVE LOCKS: the sign keeps abstract unreadable symbols; no readable text anywhere. No text, no logos, no signage, no UI, no graphics at any time."
- Tracking (vtrack.py): `sign` (the board to repaint), the landmark (for the pin), the person/cup (for the order). Gate: ≥60% coverage.
- VO: the voice's loudness envelope (`env`) for Stampy's mouth, and word timings for the bubble pops.
- Matte: not needed.

## Build it
### A. With the kit (bespoke route)
```bash
python scripts/vtrack.py clips/walk.mp4 walk_objects.json tracks/walk_vtrack.json
python scripts/run_ad.py WALK --spec specs/walk_lens.py --render
```
| Recipe constant | What it is | Sample value |
|---|---|---|
| `LENS` | the lens outline path (with the nose notch) | 1920 × 1080 |
| `INK, RED, BLUE, PAPER, SUN` | the postal palette | see above |
| `BUBS` | speech bubbles: id, [(word, time, highlight)], in, out | 5 bubbles |
| the sign markup + its inset fractions in `sq2q` | the repainted board | 500 × 660 |
| `_P`, `_N` | the dotted walk path (Bézier points) and dot count | 4 points, 22 dots |
| the pin, receipt and postcard markup | the travel paper | Hebrew + local language |
| `SPEC` | theme `he_bold`, palette, `music_vol` .5, `plate_vol` .35, `vo_name`, `env` (loudness per frame), `assets` (fonts) | — |
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// map a W x H board onto any 4-point quad (the tracked sign) with a projective matrix3d
function sq2q(q, W, H) {
  const [x0, y0, x1, y1, x2, y2, x3, y3] = q;
  const dx1 = x1 - x2, dx2 = x3 - x2, dy1 = y1 - y2, dy2 = y3 - y2, sx = x0 - x1 + x2 - x3, sy = y0 - y1 + y2 - y3;
  const det = dx1 * dy2 - dx2 * dy1, g = (sx * dy2 - dx2 * sy) / det, h = (dx1 * sy - sx * dy1) / det;
  const a = x1 - x0 + g * x1, b = x3 - x0 + h * x3, d = y1 - y0 + g * y1, e = y3 - y0 + h * y3;
  return `matrix3d(${a / W},${d / W},0,${g / W},${b / H},${e / H},0,${h / H},0,0,1,0,${x0},${y0},0,1)`;
}
window.onPlace = (t) => {
  const b = boxAt("sign", t);
  if (b) { const w = b[2] - b[0], h = b[3] - b[1], L = b[0] + w * .075, R = b[2] - w * .075, T = b[1] + h * .05, B = b[3] - h * .045, k = h * .012;
    document.getElementById("sign").style.transform = sq2q([L, T, R, T + k, R, B - k, L, B], 500, 660); }
  const ev = ENV[Math.max(0, Math.min(ENV.length - 1, Math.round(t * 24)))] || 0;          // voice loudness
  document.getElementById("msMo").setAttribute("ry", (1.5 + 8 * ev).toFixed(2));               // Stampy's mouth
  const blink = (t % 2.7) < .12 || (t % 7.3) < .1;
  ["msEl", "msEr"].forEach((id) => document.getElementById(id).setAttribute("ry", blink ? "0.8" : "5.2"));
};
tl.fromTo("#b3", {scale: .15, rotation: -6}, {scale: 1, rotation: 0, duration: .7, ease: "elastic.out(1,.55)"}, 4.28);
tl.fromTo("#sPill span", {opacity: 0, scale: 1.9}, {opacity: 1, scale: 1, duration: .2, ease: "power4.in"}, 5.85);   // franking
```

## Adapting it to the user's project
- Content: 4–5 moments the product helps with (arrive, read, discover, navigate, order), each as a bubble + a paper artefact on the world.
- Language: the user's language in the bubbles and the repainted sign; the local language only on the receipt and the phrasebook entry.
- Brand: the postcard end card (brand + tagline) and the mascot; the lens stays generic.
- No sign in the footage: skip the homography; keep the pin, the walk line and the receipt.
- Shorter (8–10 s): bubble 1 → the sign → the postcard.

## Sound
- Paper and post: a soft pop per bubble word (soft_tick, vol .3), a stamp thump on each franking (soft_thump, .6), glass_ting on the pin, a receipt-printer tick train; music .5, plate .35.

## Pitfalls and QA checklist
- [ ] The repainted sign stays glued to the board (check the tracked box against the real board edges; tune the inset fractions).
- [ ] Bubbles never cover the sign or the landmark at their moment.
- [ ] Stampy's mouth moves only while the VO speaks (the env must be computed from the final VO file).
- [ ] The lens frame never hides the action (keep key subjects inside the central 80%).
- [ ] Look at frames at 1.0, 5.9, 9.5, 12.8, 14.3 and 16.5; qa.py until "ship".
