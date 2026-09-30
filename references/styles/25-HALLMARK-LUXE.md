# #25 HALLMARK-LUXE · A jeweller's bench after hours

> The frame dims to velvet black around the featured piece like a display spotlight; one 10× jeweller's loupe travels from piece to piece showing a stabilised magnified detail with the grade engraved in its ring; each piece is priced on a tiny engraved gold hallmark plate hanging from the loupe; four-point light glints bloom on the metal; thin gold-foil words fade in; it ends on a black card with gold-foil engraving.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/hallmark-luxe.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E7_aurum_gold_on_velvet_BESPOKE.mp4
> Runner: bespoke (`references/recipes/bespoke/E7_gold_bespoke.py` + `E7_gold_bespoke_loupe.py` for the loupe crops, 12 s) · Example: none shipped

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: jewellery and watches, fragrance, fine leather, luxury pens, spirits, anything precious and small that rewards a close look.
- Avoid when: the product is big (the loupe magnifies details), the brand is loud/young, or the footage has no rest moments on each piece (the loupe needs ~1 s per piece).

## The design method (crafted world)
Ask: **how does this subject's world show, grade and price a precious thing?** A jeweller works at a bench under a lamp: they inspect with a loupe, the metal carries a hallmark (750 = 18K), and prices sit on small discreet tags. So:
1. **Light is the layout.** Instead of panels, the frame darkens to velvet black around the featured piece (a radial gradient tracked to the piece), and the words live in that darkness.
2. **The signature is an instrument: the loupe.** One loupe travels the whole take, showing magnified, stabilised crops of the real footage (precomputed as a sprite), with the grade engraved in its ring for each piece.
3. **Prices become objects:** engraved gold hallmark plates (the 750 cartouche, the piece's name, the price) hanging off the loupe, swaying slightly.
4. **Motion is slow:** 1 s fades, blur-to-sharp foil words, a foil sheen that sweeps once. No stomps, no shakes, no paper.
5. **The end is a physical object of the world:** a black card with gold-foil engraving and a blind-embossed frame and hallmark.

Worked example (AURUM ATELIER): "a small ceremony in three moments" → the loupe finds the watch (I · "the hour", 18K · 750 · SAPPHIRE, ₪4,750 → ש״ח on the plate), the bracelet (II · "the light", VS1 · 18K · 3.20 CT), the rings (III · "the touch") → black card "AURUM ATELIER · only yours" with a script signature.

It transfers to:
- **A fragrance house:** the spotlight on the bottle, the loupe becomes a perfumer's blotter strip entering frame with notes engraved (top/heart/base), prices on a glass-stopper tag, the end card is the box's embossed lid.
- **Whisky or wine:** the loupe becomes a tasting glass held to the light (the magnified liquid inside), the hallmark plate becomes the cask/vintage label, the end card is a wax seal.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#spot` | radial darkening centred on the featured piece: clear to 36% of R, 55% alpha at 68%, full alpha at 100% | R and alpha per segment: 1150/.50, 800/.86, 760/.84, 660/.86, 1080/.55 |
| `.gx` glints | four-point star glints (radial core r 46 + a 98 px star + a 45° 44 px star), screen-blended | 8 glints, each tracked to a point on a piece, 0.8–1.1 s |
| `#lead` | a fine gold leader from the magnified detail point to the loupe rim | only when the loupe has to sit off the detail (frame edge) |
| `.hp` hallmark plates | 256 px gold plate: 750 cartouche + "AURUM · I", Hebrew name 40 px, a rule, price 34 px | hangs beside the loupe (±376 px), sways 1.6° |
| `#loupe` | 400 px lens (sprite crop inside) + knurled ring (452 px) + gold rim (428 px) + glass highlight + an engraved ring with the grade text on an arc and "10× ✦ AURUM ATELIER" on top | scale .88 → 1 with visibility |
| `.hw` words | thin gold-foil words: optional roman numeral between hairlines, the word(s), a 320 px gold hairline | centred at x, top y |
| `#card` | black 560 × 316 card, rotated −3°: embossed inner frame, gold frame line, brand caps, ornament rule, Hebrew line 72 px, script signature, a blind 750 hallmark | bottom-left |

## Timing and motion
Loupe on screen 3.05 → 8.72 s (the sprite covers frames 74–211 at 24 fps).
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| spotlight | 0 | 1.2 | sine.inOut | follows the pieces; segments blend over 0.9 s at each boundary | — | — |
| opening words (2 lines) | 0.30 and 1.32 | 1.0 (y 14 → 0) + foil sharpen 1.2 (scaleX 1.16 → 1, blur 7 → 0) + sheen over the whole hold | sine.out / power2.out / sine.inOut | to 2.80 | 0.45 | sine.in |
| glints | 1.20, 1.62, 2.05, … | 0.8–1.1 each: intensity sin(πu)^1.6, rotation 12° → 50° | computed | — | — | — |
| loupe | 3.05 | visibility smoothstep over 0.55; hides when the glass loses its piece (weight < 0.03 → 0.2) | smoothstep | to 8.72 | 0.35 | smoothstep |
| grade engraving / plate per piece | when the piece's loupe weight passes 0.82 | fades over the last 18% of the weight | smoothstep | while centred | as the loupe moves on | — |
| moment words I / II / III | 3.55 / 5.05 / 7.50 (numeral 0.25 earlier) | same as the opening words | — | to 4.40 / 6.25 / 8.78 | 0.45 | sine.in |
| end card | 9.15 | 1.2 (y 26 → 0) | sine.out | to end | — | — |
| brand caps / rule / hallmark | 9.35 / 9.7 / 9.9 | 1.2 (scaleX 1.12 → 1) / 1.0 (scaleX .4 → 1) / 1.0 | power2.out / sine.out | foil sheen 2.6 s | — | — |
| Hebrew line | 10.95 | 0.8 (scale 1.06 → 1, blur 6 → 0) | power2.out | foil sheen 1.9 s | — | — |
| script signature | 11.3 | 0.7 (written on by a clip from the left) | sine.inOut | sheen 1.6 s | — | — |
- Foil: text is clipped to a 300%-wide gold gradient (`#b8903f → #e9cf8a → #fff6da → … `); animating `background-position` 100% → 0% sweeps light across the letters once.
- The signature move: the travelling loupe with real magnified footage inside it and the grade engraved in its ring.

## Typography
- Hebrew words and plate names: **Suez One** (the original used Frank Ruhl Libre 300/500; the kit remaps it). Large (150–176 px) with wide tracking (.12em) for the moment words; 40 px on the plates; 72 px on the card.
- Latin: **Cormorant Garamond** 300–600 for numerals, caps and engraving (letter-spacing .24–.36em); **Pinyon Script** for the signature (44 px).
- Prices: Latin digits inside a `<bdi dir="ltr">`, followed by ש״ח (the kit converts a ₪ glyph automatically because Suez One / Secular One draw ₪ as a stylised "שח").
- Max copy: one word per moment (≤ 6 letters at 176 px); plate name ≤ 12 characters; the card line ≤ 10 characters.

## Colour and surface
- Velvet black `rgba(6,4,2,…)` for the spotlight, gold foil gradient for type, plate gold `#f6e2a6 → #d8b465 → #b58a3c → #e4c67f → #a67c32`, plate ink #3d2809, card black `#1d1811 → #0e0b08 → #070605`.
- No cream paper anywhere; the only surfaces are metal, glass and a black card.
- Brand swap: rose gold or platinum by changing the foil gradient stops; keep the black.

## Layout and safe zones (1920×1080 canvas)
- Words sit in the dark areas the spotlight creates (the sample: the right side for I and II, the left for III); the loupe's centre is clamped to x 270–1650, y 262–818; plates hang ±376 px from the loupe centre; the card sits bottom-left (70/704).
- The contract asks for 40% free on the right (the piece on one side).
- 9:16: the loupe moves above/below the piece; words stack in the dark top area.

## What the footage must give you
- Shoot it like this: cuts OK (max 2), 10–15 s · macro; the featured piece on one side of the frame · 40% free on the right · slow macro glide.
- Seedance lines: "FORMAT: One continuous shot, or at most two soft cuts between pieces." / "CAMERA: slow macro glide. FORBIDDEN: shake, fast moves." / "LIGHTING: a single spotlight on the piece over black velvet; the rest of the frame falls to near-black." / "POSITIVE LOCKS: one hand, the same pieces throughout. No text, no logos, no signage, no UI, no graphics at any time."
- Tracking (vtrack.py): one object per piece (`watchface`, `bracelet`, `ringstack`). Gate: ≥70% coverage.
- The loupe sprite: run `references/recipes/bespoke/E7_gold_bespoke_loupe.py` (edit `CLIP`, `F0`/`F1`, and `SEGS` = (object, detail fx, fy, first frame, last frame) per piece). It writes a tiled JPEG of 420 px stabilised 120 px crops (≈2.3× at 720p) and a JSON with the loupe path and each piece's weight.
- Matte: not needed.

## Build it
### A. With the kit (bespoke route)
```bash
python scripts/vtrack.py clips/jewels.mp4 jewels_objects.json tracks/jewels_vtrack.json
python references/recipes/bespoke/E7_gold_bespoke_loupe.py        # after editing CLIP / SEGS / paths
python scripts/run_ad.py JEWELS --spec specs/jewels_hallmark.py --render
```
| Recipe constant | What it is | Sample value |
|---|---|---|
| `PIECES` | per piece: plate side (±1), plate dy, numeral, Hebrew name, price, grade engraved in the loupe | 3 pieces |
| `WORDS` | hero words: id, lines [(text, size, class)], centre x, top y, in, out, numeral | 4 words |
| `GLINTS` | (object, fx, fy, t, duration, size) | 8 glints |
| `SP` (in the JS) | spotlight segments: [t0, t1, object, fx, fy, radius, alpha] | 5 segments |
| `L_IN, L_OUT` | loupe on/off | 3.05, 8.72 |
| `FONTS` | the faces (Suez One replaces Frank Ruhl via the remap), Cormorant, Pinyon Script | — |
| `SPEC` | theme `he_premium`, palette, `music_vol` .55, `plate_vol` .3, `vo_name`, `assets` (the loupe JPEG) | — |
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
// display spotlight tracked to the featured piece (a radial darkening; words live in the dark)
function spot(t) {
  const b = boxAt("bracelet", t); if (!b) return;
  const x = b[0] + (b[2] - b[0]) * .42, y = b[1] + (b[3] - b[1]) * .42, R = 760, a = .84;
  document.getElementById("spot").style.background =
    `radial-gradient(circle ${R}px at ${x}px ${y}px, rgba(6,4,2,0) 0%, rgba(6,4,2,0) 36%, rgba(6,4,2,${a * .55}) 68%, rgba(6,4,2,${a}) 100%)`;
}
window.onPlace = (t) => {
  spot(t);
  const f = Math.round(t * 24) - LP.f0, i = Math.max(0, Math.min(LP.n - 1, f));      // the loupe shows sprite tile i
  LI.style.backgroundPosition = `${-(i % LP.cols) * LP.size}px ${-Math.floor(i / LP.cols) * LP.size}px`;
  LO.style.left = LP.cx[i] + "px"; LO.style.top = LP.cy[i] + "px";
};
// a foil word: fade up, sharpen out of a wide blur, and one slow sheen across the gold
function word(sel, t0, t1) {
  tl.fromTo(sel, {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: 1.0, ease: "sine.out"}, t0);
  tl.fromTo(sel + " .fo", {scaleX: 1.16, filter: "blur(7px)"}, {scaleX: 1, filter: "blur(0px)", duration: 1.2, ease: "power2.out"}, t0);
  tl.fromTo(sel + " .fo", {backgroundPosition: "100% 0"}, {backgroundPosition: "0% 0", duration: t1 - t0, ease: "sine.inOut"}, t0);
  tl.to(sel, {opacity: 0, duration: .45, ease: "sine.in"}, t1 - .45);
}
word("#hw1", 3.55, 4.40);
```

## Adapting it to the user's project
- Content: 2–3 pieces, each with one grade line (what an expert would engrave), a name and a price; one word per moment (a feeling, not a feature).
- Language: Hebrew words in Suez One; Latin engraving in Cormorant caps; prices ש״ח.
- Brand: the brand name on the loupe ring and the card; the signature in the founder's name.
- No loupe (short on time): keep the spotlight, the glints, the foil words and the hallmark plates tracked to each piece, and the end card.
- 9:16 for Stories: one piece per 3 s, the loupe above it, the plate below.

## Sound
- Slow, sparse: glass_ting on each glint (vol .3–.4), soft_pulse under the loupe arrival, chime on the card (.5); music .55, plate .3.

## Pitfalls and QA checklist
- [ ] The loupe sprite frames match the clip frames (same `F0`; a one-frame shift makes the magnified image lag).
- [ ] The loupe hides when its glass loses the piece (between pieces), rather than showing a blurred nothing.
- [ ] Words sit in the dark, never on a bright piece.
- [ ] Plates hang inside the frame (the loupe is clamped, but check the side for each piece).
- [ ] Prices read "4,750 ש״ח" (digits LTR, currency after).
- [ ] Look at frames at each piece's loupe peak, at a glint peak and at the card; qa.py until "ship".
