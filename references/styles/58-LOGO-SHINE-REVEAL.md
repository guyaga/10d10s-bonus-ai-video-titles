# #58 LOGO-SHINE-REVEAL · Premium logo sting

> A geometric logomark draws itself on as a thin stroke while rotating in, then fills with a brushed-metal gradient; the wordmark opens out of a horizontal light slit; a specular shine crosses the lockup in time with the plate's own light sweep and a star glint catches on the mark; a tagline settles underneath while everything slowly pushes in.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/logo-shine-reveal.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_LOGO-SHINE-REVEAL.mp4
> Runner: run_style LOGO-SHINE-REVEAL · Example: examples/logo-shine-reveal/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: brand stings at the end (or start) of ads, product launch end cards, app intros, tech/automotive/luxury brands, conference openers.
- Avoid when: the brand is colourful and playful (brushed metal reads premium-tech), the logo is complex/multi-colour (the kit draws a simple geometric mark + text wordmark), or the plate is bright.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#vig` | radial vignette centred on the lockup (transparent → 45% black) | focuses the eye |
| `#mk` | 150 px SVG mark: `ring` (circle + diagonal) or `hex` (hexagon + Y), or `none` | a 5 px white stroke copy draws on, a 13 px metal-gradient copy fades in |
| `#wm` | wordmark: 140 px, +.14em, metal gradient text (7 stops, 220% wide, slowly drifting) + drop shadow | default face Michroma (`word_font`) |
| `#shw` | a second copy of the wordmark with a narrow white highlight band | visible only while the shine crosses |
| `#star` | 90 px star glint (radial + cross lines) | pinned to the mark's upper right |
| `#tag` | tagline 46 px, #eef3f8, heavy text shadow | Hebrew or English |
| `#sub` | small mono line (JetBrains Mono 24 px, +.34em) on a dark pill | e.g. "NOVA LABS · 2026" |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| mark stroke draw (dashoffset → 0, stagger .18 per path) | t (.5) | 1.10 | power2.inOut | — | stroke fades at t+1.3, .6 s | — |
| mark rotate/scale (−90°→0, .8→1) | t | 1.40 | expo.out | — | — | — |
| mark metal fill (fade in) | t+1.0 | .70 | power2.out | — | — | — |
| wordmark slit (clip-path inset 48%→0, fade) | t+.8 | .90 | expo.inOut | — | — | — |
| wordmark scaleX 1.12→1 | t+.8 | 1.40 | expo.out | — | — | — |
| metal drift (background-position 0→100%) | t | clip end − t | linear | — | — | — |
| shine band crosses (140% → −40%) | shine (3.2) | 1.20 | power2.inOut | visible shine−.02 → shine+1.25 | — | — |
| star glint (fade, scale .2→1, rotate −30→15) | shine−.15 | .35 | power2.out | — | fade, scale .4, rotate 45 at shine+.2, .6 s | power2.in |
| tagline (fade, y 18→0, blur 8→0) | shine+.6 | .90 | power3.out | — | — | — |
| sub line (fade to .9) | shine+1.1 | .80 | — | — | — | — |
| lockup push-in (scale 1→1.035) | t | clip end − t | sine.inOut | — | — | — |
- `shine` must match the moment the plate's own light sweeps across (scrub the plate and read the time): the fake shine and the real light moving together is what sells it.
- The signature move: draw-on → metal fill → slit open → the synced specular pass.

## Typography
- Wordmark: Latin display, default Michroma (wide, techy); `word_font` can name any font in the kit's font table (e.g. "Space Grotesk", "Sora", "Anton").
- Tagline: Latin Manrope 500 (46 px); Hebrew `pair: "secular"` (default): Secular One, RTL.
- Sub line: JetBrains Mono, always LTR.
- Maximum copy: wordmark ≤ 7 characters at 140 px (wide faces), tagline ≈ 32 characters.

## Colour and surface
- `colors.metal` 4 stops (#ffffff, #aeb6c2, #e9edf2, #6d7582): the brushed-metal gradient for the wordmark and mark fill. Gold: ["#fff6d8", "#c9a45c", "#f1dfae", "#7a5a23"]. Copper, rose gold: same pattern.
- `colors.accent` #9fd3ff (reserved; the sample doesn't use it visibly).
- Needs a DARK plate: metal text on a bright background disappears.

## Layout and safe zones (1920×1080 canvas)
- The lockup (mark + wordmark in a row, tagline and sub centred under it) is centred horizontally at `y` (470 default; sample 380).
- Industry convention: logo stings last 3–5 s, end on a held frame of the lockup for ≥ 1 s, and the sound hit lands with the wordmark.
- 9:16: works centred; lower the wordmark size by editing the builder CSS if the word is long.

## What the footage must give you
- Shoot it like this: one take, 5–12 s, a dark surface (brushed metal, stone, fabric, water at night) with ONE soft light sweep crossing it; the centre calm.
- Generate it: "dark brushed metal surface, extreme close-up, a single soft band of light sweeps slowly from left to right at 3 seconds, no text, no logos".
- Tracking: none. Matte: not needed.

## Build it
### A. With the kit
```bash
python scripts/run_style.py LOGO-SHINE-REVEAL --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| word | wordmark text | required |
| word_font | wordmark font family | "Michroma" |
| mark | "ring", "hex" or "none" | "ring" |
| tagline / sub | tagline / small mono line | none |
| t | start | .5 |
| shine | time the shine crosses (sync to the plate's light) | 3.2 |
| y | lockup centre y (px) | 470 |
| language / pair | tagline language; Hebrew pair | en / "secular" |
| colors | {metal [4], accent} | see above |
| sfx | whoosh, logo hit with the wordmark, glass ting with the shine | true |
| plate_vol, music, music_vol, name | — | .5, none, .5 |
The builder docstring mentions an `svg` key for a custom logomark: it is not implemented. To use a real logo, add its single-colour paths to `MARKS` in `scripts/styles/logoshine.py` (viewBox 0 0 120 120) and pass its name as `mark`.
```json
{
 "clip": "clips/metal.mp4",
 "word": "ACME", "mark": "hex",
 "tagline": "Built to last.", "sub": "ACME ROBOTICS · 2026",
 "t": 0.5, "shine": 3.1, "y": 450,
 "colors": {"metal": ["#fff6d8", "#c9a45c", "#f1dfae", "#7a5a23"]}
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const T = .5, SHINE = 3.2, DUR = 8;
document.querySelectorAll("#mk .st *").forEach((p) => { const n = p.getTotalLength(); p.style.strokeDasharray = n; p.style.strokeDashoffset = n; });
tl.to("#mk .st *", {strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut", stagger: .18}, T);          // draw-on
tl.fromTo("#mk", {rotation: -90, scale: .8}, {rotation: 0, scale: 1, duration: 1.4, ease: "expo.out"}, T);
tl.fromTo("#mk .fl", {opacity: 0}, {opacity: 1, duration: .7, ease: "power2.out"}, T + 1.0);              // metal fill
tl.fromTo("#wmw", {clipPath: "inset(48% 0 48% 0)", opacity: 0}, {clipPath: "inset(0% 0 0% 0)", opacity: 1, duration: .9, ease: "expo.inOut"}, T + .8);
tl.fromTo("#wm", {backgroundPosition: "0% 50%"}, {backgroundPosition: "100% 50%", duration: DUR - T, ease: "none"}, T); // brushed-metal drift
tl.set("#shw", {visibility: "hidden"}, 0); tl.set("#shw", {visibility: "visible"}, SHINE - .02); tl.set("#shw", {visibility: "hidden"}, SHINE + 1.25);
tl.fromTo("#shw", {backgroundPosition: "140% 50%"}, {backgroundPosition: "-40% 50%", duration: 1.2, ease: "power2.inOut"}, SHINE);
tl.fromTo("#lock", {scale: 1}, {scale: 1.035, duration: DUR - T, ease: "sine.inOut"}, T);
```

## Adapting it to the user's project
- Content: brand name as the wordmark, the real tagline and a small sub line (company · year or URL).
- Language: Hebrew tagline → `"language": "he"`; the wordmark stays Latin (the brand name).
- Brand: pick the metal (silver, gold) that suits the brand; `word_font` close to the brand's logotype.
- Vertical 9:16: centred works.
- Longer clips: the push-in and metal drift stretch; hold ≥ 1 s on the full lockup.

## Sound
- `ar_whoosh` (.3) at t, `logo_hit` (.55) with the wordmark (t+.8), `glass_ting` (.3) with the shine.

## Pitfalls and QA checklist
- [ ] `shine` matches the plate's light sweep (scrub and read the time).
- [ ] The plate is dark enough for the metal text to read.
- [ ] Gradient text (`background-clip:text`) renders in the MP4: check the held frame.
- [ ] The star glint sits on the mark's upper right (it is placed from the mark's layout box).
- [ ] Hold the final lockup ≥ 1 s.
