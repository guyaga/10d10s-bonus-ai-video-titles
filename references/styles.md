# Style catalog

Every style below was built and rendered (source listed). Previews live in `catalog/previews/<id>.mp4`; open
`catalog/index.html` to browse them. The user picks by **ID**; you build from the entry.

How to read an entry
- **Build** says which route runs it. 39 of the 41 run from the skill (STICKER-POP and HUD-CLEAN through the
  STOMP-ESCORT and HUD-HELMET builders); CYBER-DOSSIER and ARRIVAL-CARD are still reference recipes
  (`references/recipes/legacy_shots.py` B1 / A2) to port into a spec. Routes:
  - `run_style` = parametrised builder: `python scripts/run_style.py <ID> --spec spec.json` (STOMP-ESCORT, COUNTDOWN-CTA, HUD-HELMET,
    SCIFI-TARGETING, MAP-FLYOVER, CAMPUS-AR, SPEED-STAT and the 12 AE classics in section D; copy `examples/<id>/spec.json`; every key is documented at the top of `scripts/styles/<module>.py`).
  - `adkit` = declarative elements in a spec: `python scripts/run_ad.py <AD> --spec spec.py`.
  - `bespoke` = a run_ad spec whose look lives in the `html_front` / `html_behind` / `css` / `js` / `fonts` / `assets`
    hooks. The recipe files in `references/recipes/bespoke/` are the originals: they run once their media
    (clip, track, matte, VO, data files) is in place, but a new subject means rewriting them, not swapping the text.
    Only `examples/E8_tower_bespoke.py` ships with its data files.
- **Prompt** is the one line a user pastes. Swap the brand colour and fonts freely; keep the motion recipe.

Two rules from the field:
1. **One bespoke visual language per piece.** Styles are starting points, not a house style. Running every video
   through the same kit made them all look the same (rejected). Mix at most one family per piece, then tailor it to the
   subject's own world: what does this product's industry print, measure, stamp or display?
2. **Premium beats loud.** A single accent colour. Multi-colour comic pop (yellow/pink/cyan bursts) was built and
   rejected as childish; it is still in adkit (`theme` flag `pop`) but do not offer it.


## Hebrew typography

Hebrew titles use three Google faces, bundled in `assets/fonts` with Hebrew + Latin unicode-ranges:

| Face | Character | Use it for |
|---|---|---|
| **Suez One** | serif display, weighty and editorial | premium, luxury, film, real estate |
| **Karantina** (700) | condensed display, loud | social stomp, sport, food, loud drops |
| **Secular One** | bold rounded-geometric, very legible | captions, HUD labels, tech, clean UI |

Pairings (`"pair"` in any run_style spec; defined in `scripts/styles/common.py` HE_PAIRS):
- `suez`: Suez One display + Secular One body/labels (premium)
- `karantina`: Karantina 700 display + Secular One body/labels (punchy social)
- `secular`: Secular One alone (captions, UI)
- `karantina-suez`: Karantina display + a Suez One accent word or line

Rules: Hebrew titles never use Anton, Bodoni or any Latin-only face (`type_pair` refuses them). `dir=rtl`; wipes and
motion mirror; numbers stay glued to the word they belong to (`words()` in common.py) and digit runs stay one
left-to-right island. Assistant remains only inside styles shipped before this system: HUD-HELMET, SCIFI-TARGETING,
MAP-FLYOVER and CAMPUS-AR (Hebrew HUD and label text) and the adkit themes `he_bold` / `he_premium` (KINETIC-HE,
TAPE-HE, KINETIC-KARAOKE, STOMP-SX), whose shipped renders it matches. New work uses the three faces above.

## Plate contracts

Every style also has a **plate contract** in `references/plates.json`: what the AI video must contain for the style to
work. This skill is post only; the contract is what a generator (ai-ad-studio) plans the shoot backwards from.
- `take` one-take | cuts-ok | cut-list, `max_cuts`, `duration_s` [min, max], `aspect` (the kit renders 1920x1080, so 16:9)
- `subject`, `framing`, `camera`: what must be in frame and how it is shot
- `negative_space` {side, min_frac}: the free fraction of frame width (left/right/both) or height (top/bottom) the titles need
- `separation`: the style needs a matte (text behind the subject); `track`: what must be trackable; `beats`: lands on a music grid
- `text_in_frame`: always false. `seedance_lines`: 2-4 lines to paste into a Seedance 2.5 prompt that enforce the contract
- `gate` {max_cuts, min_track_coverage, min_free_margin}: plate-checker thresholds. Cuts: count hard cuts with
  ffmpeg `select='gt(scene,0.15)'` (0.35 and 0.25 both missed a real cut in the football plate; 0.15 caught every
  cut with no false ones on the one-takes). A match cut that keeps the colours (the first interior plate) scores
  below any threshold: for one-take styles also ask Gemini "is this one unbroken take?". Coverage: fraction of frames vtrack finds the
  first `track` object (for cut-list styles, over the whole take). Free margin: the minimum over the take of the free
  frame fraction on the `negative_space` side of that object's box.
Numbers are derived from the plate behind each style's source render (`source` names it): durations and cuts as
measured, free margins and coverage from its vtrack file, rounded down to leave room. Regenerate with
`python references/build_plates.py`. Each style below carries a one-line `Plate:` summary.

---

## A. Social stomp family (fashion, product, drops)

### STOMP-ESCORT
Giant Anton word per item that slams in beside the tracked garment and rides with it ("escorts" it), a red `01 / 05`
index tag with a rule, and a white sticker card (thumbnail, italic Bodoni name, red price chip). Brand bug top-left.
- Best for: fashion runway, shoppable lookbooks, product line-ups, any "piece by piece" reveal.
- Fonts: Anton (words) + Bodoni Moda italic (names) + Archivo (labels).
- Palette: ivory `#f6f1e8`, ink `#16130f`, hot red `#ff3d2e`.
- Motion: words land on a beat grid (120 BPM: one item every 1.5-2 s); scale 2.3 -> 1 with blur, overshoot, soft sub
  thump; tag wipes in, card drops 0.3 s later; exit blur-out. Tracking: vtrack box per garment, anchor + side offset.
- Build: run_style `STOMP-ESCORT` (`scripts/styles/runway.py`; example `examples/stomp-escort/`, runnable demo `examples/demo/`).
- Source: `D2_runway_full_countdown_30s.mp4` (and `D1_stomp_sticker_v2.mp4`, same family).
- Plate: one take, no cuts, 10-30 s · full body, centred, walks toward camera · 30% free both sides · locked-off or very slow push-in (or a dolly back matching her pace) · track: subject full body · music beat grid.
- Prompt: `Titles: STOMP-ESCORT - Anton words escorting each tracked item, red index tags + white price stickers, accent #E63B2E, 120 BPM grid.`

### STOMP-BEHIND
Same words, but set **between the plate and a matted subject**, so the model walks in front of her own title.
- Best for: hero reveals, fashion, athletes, anything with a clean silhouette.
- Fonts: Anton + Bodoni Moda. Palette: white words, red shadow/accents.
- Motion: stomp on the beat; the word sits in `html_behind` / `behind: true`; needs `mattes/<AD>_alpha.webm`
  (`npx hyperframes remove-background`). Keep words huge (500-700 px) so the occlusion reads.
- Build: adkit `stomp {behind:true}` or `kine {behind:true}`.
- Source: `D1_stomp_behind_v2.mp4`.
- Plate: one take, no cuts, 8-30 s · full body, centred, walks toward camera; plain wall or backdrop behind the head and shoulders · 30% free both sides · slow dolly back matching the walk, or locked-off · track: subject full body · matte (subject separable), music beat grid.
- Prompt: `Titles: STOMP-BEHIND - giant Anton words behind the subject (matte), white with red accent, stomp on the beat.`

### GLASS-CALLOUT
Transparent outlined words (translucent fill + stroke) and smoked-glass price cards; quieter than ESCORT.
- Best for: premium retail, beauty, calm luxury, when the footage must stay the hero.
- Fonts: Anton outline + Bodoni Moda. Palette: white stroke on rgba(0,0,0,.25) fill, glass panels.
- Motion: same beat grid, softer (no hard shadow), cards blur in.
- Build: adkit `stomp {color:"rgba(17,17,17,.38)", stroke:"5px #fff"}` + `tag` (glass panel).
- Source: `D1_stomp_glass_v2.mp4`.
- Plate: one take, no cuts, 8-30 s · full body, centred, walks toward camera · 30% free both sides · slow dolly back matching the walk, or locked-off · track: subject full body, each advertised item · music beat grid.
- Prompt: `Titles: GLASS-CALLOUT - transparent outlined Anton words + smoked-glass price cards, restrained, no hard shadows.`

### COUNTDOWN-CTA
The selling end: FLASH SALE tag, italic "the complete look" box, struck-through total, big sale price, a black
OFFER ENDS IN box with a live 00:15 countdown and red progress rule, a stack of item tiles at sale prices, SHOP NOW
button with a hard offset shadow.
- Best for: e-commerce drops, launches, limited offers; pairs with STOMP-ESCORT.
- Fonts: Anton (numbers, button) + Bodoni Moda italic + Archivo. Palette: red `#E63B2E` / ink / white.
- Motion: elements slam in staggered 0.12 s; digits punch each second (scale 1.25 + red flash); rule shrinks linearly.
- Build: run_style `COUNTDOWN-CTA` (`scripts/styles/runway.py`, `countdown` block; example `examples/countdown-cta/`).
- Source: `D3_look08_runway_countdown_30s.mp4` (also `D2_...`).
- Plate: one take, no cuts, 20-30 s · full body, centred; the last 15 s she stands in the centre facing camera · 30% free both sides · locked-off with an extremely slow push-in · track: subject full body · music beat grid.
- Prompt: `Titles: COUNTDOWN-CTA - flash-sale stack with 15 s live countdown, struck total + sale price, SHOP NOW, accent #E63B2E.`

### KINETIC-HE
Hebrew word-by-word social stomps synced to the voice: Rubik 900 / Karantina 700 words that land blurred->sharp with a
squash, one word in the accent colour, one outlined, hits shake the frame.
- Best for: Hebrew social ads, product launches, anything with a punchy VO.
- Fonts: Rubik 900 + Karantina 700 (big words), Assistant for small lines. Palette: white + one accent.
- Motion: word time = the VO word onset (`word_times.py`); `kine` lines; `hit:true` = shake + thump.
- Build: adkit `kine` (+ `ring`, `callout`, `counter`, `chip`, `lockup`), theme `he_bold`.
- Source: `E6_guyaga_aero_sneaker_HE.mp4`.
- Plate: cuts OK (max 5), 12-24 s · subject centred, room above it · 25% free top · slow orbit or slow push; energy from subject motion, not camera · track: hero object.
- Prompt: `Titles: KINETIC-HE - Hebrew voice-synced word stomps, Rubik 900 + Karantina, one accent word per line, hit shakes.`

### TAPE-HE
Hebrew slogans on highlight-tape strips (ink / accent / light), each strip wipes in right-to-left and slams, slightly
rotated, hard drop shadow; used where plain Hebrew text over footage was unreadable.
- Best for: Hebrew slogans, stats, CTAs over busy footage; readable at phone size.
- Fonts: Rubik 900 / Karantina. Palette: strips in ink + one accent; `tacc` auto-picks legible text colour.
- Motion: strip clip-path wipe 0.28 s, text pops 0.12 s later; optional bottom scrim.
- Build: adkit `tape` (+ `kine`, `counter`), theme `he_bold`.
- Source: `E4_firelink_through_the_smoke_HK.mp4` (all `_HK` renders).
- Plate: cuts OK (max 5), 12-24 s · subject off-centre or centred with a calm lower third · 25% free bottom · steady; cut-blocks welcome · track: subject per shot (optional, for tags).
- Prompt: `Titles: TAPE-HE - Hebrew slogans on rotated highlight-tape strips (ink + accent), RTL wipe + slam, readable over anything.`

### KINETIC-KARAOKE
TAPE/KINETIC plus karaoke captions: 2-3 word groups at the bottom, the spoken word highlighted in an accent pill, plus
punch-zooms on the plate.
- Best for: talking/VO-driven social cuts, reels, accessibility.
- Fonts: Rubik 900 with a thick black stroke. Palette: white words, accent pill.
- Motion: groups break on punctuation or 3 words; digits glue to the next word ("6 שעות"); a group holds <= 1 s after
  its last word; `punch` zooms 1.1 -> 1 on key beats.
- Build: adkit `captions` (words from `word_times.py`) + `punch` + `kine`/`tape`.
- Source: `E9_lumen_lens_smart_glasses_SX.mp4` (all `_SX` renders).
- Plate: cuts OK (max 5), 12-24 s · subject in the upper two thirds · 22% free bottom · stabilised; punch-zooms are added in post · no tracking.
- Prompt: `Titles: KINETIC-KARAOKE - voice-synced karaoke captions (accent pill on the spoken word) + punch zooms + tape slogans.`

### FLASH-CARD
A 4-frame full-screen word card (accent background, huge Karantina word) cut into the edit on the biggest beat.
- Best for: the one moment that must hit (brand name, "GOAL", "SOLD").
- Fonts: Karantina 700 (auto RTL/LTR by script). Palette: accent bg + ink word, or inverse.
- Motion: on for `dur` 0.16 s, scale 1.25 -> 1. Use once or twice per piece, never more.
- Build: adkit `flash`.
- Source: `E3_aura_night_drive_SX.mp4` ("AURA!").
- Plate: cuts OK (max 6), 6-30 s · any · no free space needed · any · no tracking · music beat grid.
- Prompt: `Titles: FLASH-CARD - one 4-frame full-screen word card on the biggest beat, accent background.`

### SPEED-STAT
Sports broadcast stat hits: a giant "9 MS" contact-time stomp, callout leaders to the boot, a live ball-speed counter
riding the tracked ball, then a giant red GOAL with a brand lockup.
- Best for: sport, slow-motion product proof, anything measurable in motion.
- Fonts: Anton + Archivo. Palette: white / red `#E63B2E` / black panels.
- Motion: counter eases 0 -> value while following the tracked object; GOAL 680 px stomp with shake.
- Build: run_style `SPEED-STAT` (`scripts/styles/speedstat.py`; example `examples/speed-stat/`).
- Source: `E1_guyaga_strike_soccer.mp4`.
- Plate: planned cut list (max 4), 12-18 s · one idea per shot: wide player, extreme close-up on the contact, the object crossing the frame, hero wide · 30% free left · energy from subject speed and speed ramps · track: athlete, the object (ball), the contact point (boot) · matte (subject separable).
- Prompt: `Titles: SPEED-STAT - broadcast stat hits: huge Anton numbers, live counter on the tracked ball, giant GOAL finish.`

### PRESIDENTIAL-SERIF
Restrained, premium: soft-in DM Serif Display words (BLOCK, VICTORY) with an accent underline, small glass tags,
a percent counter, few titles. Built after the comic version was rejected as childish.
- Best for: epic/brand films, leadership, battle or sport trailers that must feel expensive.
- Fonts: DM Serif Display (+ italic tagline) + Space Grotesk / Space Mono labels. Palette: cream + one red accent.
- Motion: `soft` = opacity + 1.12 -> 1 + small rise over 0.6 s, tiny shake; long holds.
- Build: adkit theme `sparta` (premium) with `stomp`, `tag`, `counter`, `lockup`, `meter`.
- Source: `E2_sparta_spartan_vs_machine.mp4`.
- Plate: planned cut list (max 6), 18-30 s · hero framed off-centre, sky or smoke above · 25% free top · cinematic, grounded; push-ins and tracking · track: hero, opponent.
- Prompt: `Titles: PRESIDENTIAL-SERIF - few, big DM Serif words that ease in with an accent underline, glass tags, no comic colours.`

### STICKER-POP
Heavy white sticker words (solid white fill, thick ink stroke, hard offset shadow) with a red index tag and a white
price sticker. The loudest of the runway family that still reads premium.
- Best for: drops, streetwear, sneakers, anything that should feel like a sticker slapped on the frame.
- Fonts: Anton + Bodoni Moda italic. Palette: #ffffff, #16130f, accent #ff3d2e.
- Motion: same 120 BPM grid as ESCORT; words slam from 1.6x with a hard shadow snap.
- Build: reference recipe `references/recipes/legacy_shots.py` → `D1S` (the sticker shot). Closest runnable:
  `run_style.py STOMP-ESCORT` with the word style set to white fill + ink stroke.
- Source: `D1_stomp_sticker_v2.mp4` (v1: `D1_stomp_sticker.mp4`).
- Plate: one take, no cuts, 8-30 s · full body, centred, walks toward camera · 30% free both sides · slow dolly back matching the walk, or locked-off · track: subject full body · music beat grid.
- Prompt: `Titles: STICKER-POP - heavy white Anton sticker words with a hard ink shadow, red index tag, white price sticker, stomp on the beat.`

### STOMP-SX
The dynamic Hebrew social version: coloured Karantina headline words that stomp in, ink tape lines for the
secondary copy, and a closing slogan with one accent word. Busier and faster than TAPE-HE.
- Best for: food, product, travel and brand social ads in Hebrew that need energy.
- Fonts: Karantina + Rubik 900. Palette: brand accent (e.g. #ff7a1a), ink, white.
- Motion: word-synced `kine` stomps (blur + scale + squash), hit shakes, `tape` strips wiping RTL.
- Build: adkit via `run_ad.py` with an SX spec. `examples/E6_sneaker_sx.py` is the template.
- Source: `E10_ember_chefs_pass_SX.mp4` (also E3, E5, E6, E9 `_SX`).
- Plate: planned cut list (max 5), 12-20 s · subject large, upper quarter free · 25% free top · energy from cuts and speed ramps · track: hero object per shot (optional).
- Prompt: `Titles: STOMP-SX - dynamic Hebrew social stomp, coloured Karantina headline words, ink tape lines, closing slogan with one accent word.`

### TRACKED-TAGS
The clean English callout layer: numbered glass tags tracked to each object, one stat panel, a price total.
The original version of every ad before the Hebrew and bespoke passes.
- Best for: product, interior, jewellery, food; any time the footage is the hero and the copy is facts.
- Fonts: Space Grotesk + Space Mono (+ DM Serif for prices). Palette: warm white, ink, one accent.
- Motion: tags draw a leader line and fade in on their object, follow it frame by frame, fade out.
- Build: adkit `tag` / `callout` / `counter` elements via `run_ad.py`. Start from `examples/E6_sneaker_sx.py`
  and keep only `tag`, `callout` and `counter` (drop `kine`, `tape` and `flash`).
- Source: `E6_guyaga_aero_sneaker.mp4` (also the plain E4, E5, E7, E8, E9, E10 renders).
- Plate: cuts OK (max 4), 10-20 s · subject centred at medium size · 20% free both sides · slow orbit, slow glide or locked; no fast moves · track: each labelled object or part.
- Prompt: `Titles: TRACKED-TAGS - numbered glass tags tracked to each object, one stat panel, price total, English, restrained motion.`

### COMIC-POP
Multi-colour comic burst words (yellow, pink, cyan) with a starburst backing on the biggest beats.
- **Use sparingly.** It was rejected as childish for premium brands, and SPARTA was rebuilt as PRESIDENTIAL-SERIF.
  Offer it only for kids, gaming or deliberately playful brands, and only on one or two beats.
- Build: adkit theme flag `pop` on the big `stomp` words.
- Source: `E3_aura_night_drive.mp4` ("BRAKING").
- Plate: cuts OK (max 5), 10-20 s · subject centred, upper area free on the beat shots · 25% free top · any smooth move · no tracking · music beat grid.
- Prompt: `Titles: COMIC-POP - multi-colour comic burst words on the biggest beats only, starburst backing, keep everything else calm.`

## B. HUD / interface family

### HUD-HELMET
Iron-Man-style (original design) holographic visor HUD in Hebrew: rotating dashed rings and tick scales, a cyan glass
visor overlay, threat panels that go red on alert, a heart-rate ring, and the suit AI "Ora" speaking (Gemini TTS
designed voice) with a voice meter driven by the real audio envelope.
- Best for: sci-fi, gaming, tech launches, "AI assistant" stories.
- Fonts: Assistant 300-800 (Hebrew) + JetBrains Mono. Palette: cyan `#6fe3ff`, text `#e6fbff`, red `#ff4a5a`, amber.
- Motion: rings rotate continuously (seek-safe: angle = f(t)); alert = red wash + panel shake; perspective tilt.
- Build: run_style `HUD-HELMET` (`scripts/styles/helmet.py`, `language` he/en, optional `voice` file drives the meter; example `examples/hud-helmet/`).
- Source: `B4V_helmet_ora_voice_24s.mp4`.
- Plate: one take, no cuts, 15-30 s · face close-up, eyes steady and centred, visor edges in frame · 22% free both sides · locked-off with a very slow continuous push-in · track: face, eyes.
- Prompt: `Titles: HUD-HELMET - holographic visor HUD, rotating rings + tick scales, cyan with red alerts, AI voice with live meter, Hebrew.`

### SCIFI-TARGETING
First-person targeting: brackets and ID tags locked to each robot (`T-01 // HEAVY`), a HOSTILE LOCK banner, FIRE,
then TARGETS NEUTRALIZED.
- Best for: action, gaming, defence/tech demos.
- Fonts: JetBrains Mono + Assistant. Palette: amber `#ffb547`, warn red, dark panels.
- Motion: box brackets snap to tracked boxes (`data-box`), tags follow, banners wipe.
- Build: run_style `SCIFI-TARGETING` (`scripts/styles/targeting.py`; example `examples/scifi-targeting/`).
- Source: `B3_final.mp4`.
- Plate: one take, no cuts, 6-12 s · POV; targets spread across the middle, weapon in a lower corner · 25% free right · first-person, subtle natural head movement; one short blast shake allowed · track: each target, weapon/launcher.
- Prompt: `Titles: SCIFI-TARGETING - tracked target brackets + ID tags, HOSTILE LOCK banner, amber military HUD.`

### ROAD-HUD
Automotive AR head-up display projected onto the road in true CSS 3D perspective: lane-keep chevrons, braking-distance
band, amber contour on the cyclist with a warning strip, a split speed ring (54 -> 0) that doubles as the co-pilot's
voice arc, an AEB pictogram flash, and an end line written as light on the wet road.
- Best for: automotive, mobility, safety tech.
- Fonts: Heebo 200/300/500/700 only. Palette: cool white, cyan, amber for hazards.
- Motion: slow fades and projected-light reveals; no stomps, no shakes.
- Build: bespoke (`references/recipes/bespoke/E3_car_bespoke.py`).
- Source: `E3_aura_night_drive_BESPOKE.mp4`.
- Plate: planned cut list (max 4), 15-20 s · windscreen POV with the road's vanishing point visible; the hazard enters from one side · 30% free bottom · smooth, steady; no shake · track: hazard (cyclist/pedestrian), driver, car.
- Prompt: `Titles: ROAD-HUD - AR head-up display projected on the road in 3D perspective, speed ring + hazard contour, calm fades.`

### THERMAL-RESCUE
The frame becomes a thermal-imaging viewfinder: steel-blue luminance map with only the hottest tones amber->white,
ironbow strip, crosshair with spot temperature, SCBA pressure-gauge dial (100 -> 7 %), live ECG line; the AI speaks as
amber OSD text; the camera switches off to natural colour at the rescue.
- Best for: emergency services, safety equipment, industrial, documentary tension.
- Fonts: IBM Plex Sans Hebrew / Mono. Palette: steel blue, amber, white-hot.
- Motion: everything pulses on the heartbeat; switch-off bloom at the resolve.
- Build: bespoke (`E4_fire_bespoke.py`; SVG colour-table filter on the plate).
- Source: `E4_firelink_through_the_smoke_BESPOKE.mp4`.
- Plate: planned cut list (max 5), 15-24 s · mid shots and close-ups; the searched object (door, person) clearly readable as a shape · no free space needed · steady handheld feel, no shake · track: searcher, door or target, found person.
- Prompt: `Titles: THERMAL-RESCUE - the frame is a thermal camera: blue-grey map, white-hot fire, gauge dial + ECG, amber OSD voice.`

### SPEC-SCAN
Performance-lab language: the product starts as a volt CAD wireframe on a grid and scan-wipes into the photo; exploded
assembly with numbered balloons, parts re-rendered as mesh / FEA heat maps masked to the real pixels, race-timer
7-segment digits that flick and lock, a force-plate trace on the landing, end on a shoebox label.
- Best for: sneakers, gear, hardware, any engineered product.
- Fonts: Chakra Petch + Rubik (Hebrew). Palette: black + volt, orange only on the box and hot stress.
- Motion: scan wipes, digit flicker-and-lock, no thump/shake.
- Build: bespoke (`E6_sneaker_bespoke.py`, SVG filters `#fWire` / `#fHeat` over the matte).
- Source: `E6_guyaga_aero_sneaker_BESPOKE.mp4`.
- Plate: one take, no cuts, 10-18 s · product centred, fully in frame · 20% free both sides · slow smooth orbit · track: product, each layer / part · matte (subject separable).
- Prompt: `Titles: SPEC-SCAN - lab/CAD language: wireframe scan-in, exploded parts with numbered balloons, FEA heat map, 7-segment stats.`

### MAP-FLYOVER
Aerial map explorer: a route line draws across a planar-tracked city, pins with bilingual labels stick to places,
a distance counter runs, then a landing card on arrival.
- Best for: travel, real estate location, campus/venue arrival, logistics.
- Fonts: Assistant + JetBrains Mono. Palette: dark glass panels, lime/acc route.
- Motion: pins ride `track.py` (planar homography) points; route draws with stroke-dashoffset.
- Build: run_style `MAP-FLYOVER` (`scripts/styles/mapflyover.py`; points from `track.py`; example `examples/map-flyover/`).
- Source: `TEST_A_map_to_ono.mp4`.
- Plate: one take, no cuts, 8-12 s · high aerial, landmarks spread across the frame, horizon or sea as a fixed reference · 30% free left · smooth drone, constant slow forward push and slight descent; no rotation · track: landmark points (planar, track.py).
- Prompt: `Titles: MAP-FLYOVER - route drawing over a tracked aerial, pinned bilingual place labels, distance counter, arrival card.`

### CAMPUS-AR
AR place labels on a walking tour: small glass tags pinned to real features (Library, Study area, Podcast studio,
Skylight), a voice waveform, a person tag, an end logo card.
- Best for: campus/venue/office tours, museums, retail wayfinding.
- Fonts: Assistant + mono. Palette: dark glass, thin accent rule.
- Motion: tags clip-wipe in, ride tracked anchors, fade on exit.
- Build: run_style `CAMPUS-AR` (`scripts/styles/campus.py`; example `examples/campus-ar/`).
- Source: `TEST_C_campus_ar.mp4`.
- Plate: one take, no cuts, 5-10 s · medium-wide, person centred, walking toward camera · 25% free both sides · slow steady dolly backwards at chest height matching the walk · track: person/head, each labelled place.
- Prompt: `Titles: CAMPUS-AR - small bilingual AR tags pinned to real places along a walk, glass panels, waveform for voice.`

### HUD-CLEAN
The first, quieter visor HUD: a thin vitals column, a heading tick scale, and one red alert panel. No rings, no voice.
- Best for: when HUD-HELMET is too much; documentary-feeling sci-fi, pilots, divers, climbers.
- Fonts: Assistant + JetBrains Mono. Palette: pale cyan-white, amber, alert red.
- Build: `run_style.py HUD-HELMET` with the reticle, radar and voice blocks left out of the spec (every block is optional).
  The original recipe is `legacy_shots.py` → `B4` (Hebrew) / `B2` (English).
- Source: `B4_helmet_hebrew_24s.mp4` (also `B2_final.mp4`, `TEST_B_scifi_pilot.mp4`).
- Plate: one take, no cuts, 6-30 s · face close-up, eyes steady · 22% free both sides · locked-off with a very slight slow push-in · track: face, eyes.
- Prompt: `Titles: HUD-CLEAN - quiet visor HUD: thin vitals column, heading tick scale, one red alert panel, no rings.`

### CYBER-DOSSIER
A character intro as a city dossier: a bilingual location card, a pilot ID panel, and suit status bars.
- Best for: game trailers, character reveals, sci-fi shorts, "meet the hero" openers.
- Fonts: JetBrains Mono + Assistant. Palette: amber #ffb547 on near-black glass.
- Build: reference recipe `legacy_shots.py` → `B1`.
- Source: `B1_final.mp4`.
- Plate: one take, no cuts, 5-10 s · full body, centred, walks toward camera · 35% free both sides · low slow dolly backwards matching the walk · track: character, head.
- Prompt: `Titles: CYBER-DOSSIER - character intro dossier: bilingual location card, pilot ID panel, suit status bars, amber mono type.`

### ARRIVAL-CARD
A destination lower-third: the place name in two languages, coordinates and a distance line, and a green ARRIVED chip.
- Best for: travel, campus and real-estate arrivals; the last shot of a MAP-FLYOVER.
- Fonts: Assistant + JetBrains Mono. Palette: green #9bd14a, dark glass, off-white.
- Build: reference recipe `legacy_shots.py` → `A2`. It pairs with `run_style.py MAP-FLYOVER` as the next shot.
- Source: `A2_final.mp4`.
- Plate: one take, no cuts, 5-10 s · person walks toward camera, destination facade behind with a blank area for the logo · 35% free left · slow steady dolly backwards at chest height matching the walk · track: head, blank facade area.
- Prompt: `Titles: ARRIVAL-CARD - destination lower-third, bilingual place name, coordinates + distance line, green ARRIVED chip.`

## C. Editorial / crafted-world family (fully bespoke)

### HALLMARK-LUXE
A jeweller's bench after hours: the frame dims to velvet-black around the featured piece, a 10x loupe travels between
pieces showing stabilised magnified crops with the grade engraved in its ring, prices on tiny gold hallmark plates,
four-point glints on the metal, thin gold-foil words, an embossed black end card.
- Best for: jewellery, watches, fragrance, any luxury object.
- Fonts: Frank Ruhl Libre 300 (Hebrew), Cormorant caps, Pinyon Script. Palette: velvet black + gold foil.
- Motion: slow fades only; glints computed from t.
- Build: bespoke (`E7_gold_bespoke.py` + `E7_gold_bespoke_loupe.py` for the loupe crops).
- Source: `E7_aurum_gold_on_velvet_BESPOKE.mp4`.
- Plate: cuts OK (max 2), 10-15 s · macro; the featured piece on one side of the frame · 40% free right · slow macro glide · track: each piece (watch, bracelet, rings).
- Prompt: `Titles: HALLMARK-LUXE - spotlight on velvet black, a travelling jeweller's loupe, gold hallmark price plates, foil type.`

### ARCH-DRAWING
Architecture on paper: a vellum sheet slides over the drone shot with the facade inked on it, then a sepia elevation
sheet where floors fill with watercolour wash as the drone climbs and the sight line to the sea clears; ends on an
estate-agent floor plan and a brass building plaque.
- Best for: real estate, architecture, developments, hotels.
- Fonts: Karantina (hand lettering) + Heebo 300. Palette: vellum cream, graphite, sepia, terracotta, sea blue, brass.
- Motion: sheet slides, line draws, wash fills tied to tracked slabs.
- Build: bespoke (`E8_tower_bespoke.py`; runnable example in `examples/`).
- Source: `E8_seaview24_tower_arrival_BESPOKE.mp4`.
- Plate: one take, no cuts, 12-20 s · building on the right half, sky and neighbourhood on the left · 30% free left · smooth vertical drone rise, constant speed · track: building, floor slabs / balconies.
- Prompt: `Titles: ARCH-DRAWING - vellum + sepia elevation sheets over the footage, floors fill with wash, hand-lettered lines, floor plan end.`

### MAGAZINE-EDITORIAL
The drone flight as an interior-design magazine spread: masthead and folios, circled numbers pinned on each piece with
shopping credits, a running price-list column, red-pencil loops and margin notes, halftone + paper grain, a page that
folds open for the pull quote and folds in for the total.
- Best for: interiors, furniture, home, hospitality, shoppable rooms.
- Fonts: Frank Ruhl Libre + Heebo Light + Amatic SC (pencil). Palette: paper cream, ink, editor red.
- Motion: soft fades, slides, page folds only.
- Build: bespoke (`E5_home_bespoke.py`).
- Source: `E5_luma_drone_through_the_home_BESPOKE.mp4`.
- Plate: one take, no cuts, 15-20 s · wide interior, pieces readable, camera travels through the room · 20% free left · smooth stabilised FPV glide, constant speed · track: each furniture piece.
- Prompt: `Titles: MAGAZINE-EDITORIAL - the video as a printed spread: masthead, numbered product credits, price column, red-pencil notes, page folds.`

### KITCHEN-TICKET
A restaurant kitchen at night: the order prints line by line as a thermal ticket under a steel rail, the VO words
condense out of smoke and drift off as steam, a flame-shaped heat gauge fills to 260 degrees, grease-pencil notes on
the plate, and the ending is the ticket torn, spiked and stamped DONE.
- Best for: restaurants, food, delivery, chefs.
- Fonts: Frank Ruhl Libre (VO words), Miriam Libre (receipt), Amatic SC (grease pencil), Rubik Dirt (station label).
- Palette: steel, ember orange, receipt white, stamp red.
- Motion: print-in, smoke condense (SVG turbulence), stamp slam at the end only.
- Build: bespoke (`E10_chef_bespoke.py`).
- Source: `E10_ember_chefs_pass_BESPOKE.mp4`.
- Plate: planned cut list (max 5), 12-18 s · macro, subject centre-left · 30% free right · energy from cuts and speed ramps · track: the dish/ingredient per shot.
- Prompt: `Titles: KITCHEN-TICKET - thermal order ticket printing on a steel rail, smoke-formed words, flame heat gauge, stamped finish.`

### LENS-POSTCARD
The world seen through one smart-glasses lens: a real lens outline with frame edge and chromatic fringe, a
postage-stamp mascot who lip-syncs the VO in paper speech bubbles, a sign repainted in Hebrew by homography and
franked "translated", an airmail postcard for the landmark, a printed receipt, a postcard end card.
- Best for: travel, translation/AI wearables, tourism, playful consumer tech.
- Fonts: Varela Round + IBM Plex Sans Hebrew + IBM Plex Mono. Palette: navy ink, postal red, airmail blue, cream, sun yellow.
- Motion: paper pops, stamp franking, dotted map line.
- Build: bespoke (`E9_glasses_bespoke.py`).
- Source: `E9_lumen_lens_smart_glasses_BESPOKE.mp4`.
- Plate: one take, no cuts, 15-20 s · POV at eye level, gentle head motion · 20% free bottom · natural first-person walk, stabilised · track: sign, landmark, person/cup.
- Prompt: `Titles: LENS-POSTCARD - seen through a glasses lens: stamp mascot speech bubbles, translated sign, airmail postcards, receipt.`

---

## D. AE classics (famous After Effects looks, all parametrised)

Twelve title looks people ask for by name. Each is one `run_style.py` builder (`scripts/styles/<module>.py`, every key
documented at its top) with a working example in `examples/<id>/`. Everything is seek-safe: canvas and procedural
effects are pure functions of time and a seed, never `Math.random`.

### VIRAL-CAPTIONS
Hormozi / MrBeast social captions driven by word timings: 1-3 huge words at a time in the lower band, the group
appears with unspoken words dimmed, each word pops to full and bounces as it is spoken (a second smaller bounce on
long words), keywords in colour, and a colour emoji (Twemoji, fetched once and cached) pops above its own word.
- Best for: talking-head and VO-driven social ads, reels, product explainers; Hebrew or English.
- Fonts: Hebrew Secular One (captions); Latin Rubik 900. Palette: white, black stroke, keyword yellow/green.
- Motion: group in with a back-ease, word pop 1.55 -> 1 with tilt, syllable pulse; digits glue to their word.
- Build: run_style `VIRAL-CAPTIONS` (`scripts/styles/viral.py`; words from `word_times.py`; example `examples/viral-captions/`).
- Source: `AE_VIRAL-CAPTIONS` (GUYAGA AERO sneaker, Hebrew VO).
- Plate: cuts OK (max 6), 8-30 s · subject in the upper two thirds · 25% free bottom · any smooth move; cuts on the voice's phrases · no tracking.
- Prompt: `Titles: VIRAL-CAPTIONS - huge word-by-word captions from the VO timings, keywords in colour, emoji pops, bounce on every word.`

### DECODE-TYPE
Terminal decode: each line types in while every character scrambles through random glyphs (Hebrew letters for Hebrew,
A-Z/0-9 for Latin) and locks in reading order, with a blinking block cursor. The final text reserves its space so
nothing jitters; digit runs stay one left-to-right island, so "98.6%" never reorders inside Hebrew.
- Best for: tech, security, sci-fi, data reveals, AI assistants.
- Fonts: Hebrew Secular One; Latin IBM Plex Mono + JetBrains Mono. Palette: mint text + green cursor on dark glass.
- Motion: glyphs change 12x/s, lock at 35-100% of the decode; lines can pin beside a tracked face.
- Build: run_style `DECODE-TYPE` (`scripts/styles/decode.py`; example `examples/decode-type/`).
- Source: `AE_DECODE-TYPE` (helmet close-up, Hebrew).
- Plate: cuts OK (max 4), 6-20 s · subject centred or off-centre, calm space on one side for the status lines · 22% free right · locked or very slow push · track: face or subject (optional, to pin lines to it).
- Prompt: `Titles: DECODE-TYPE - terminal decode: scrambling glyphs lock into the words with a blinking cursor, status lines beside the face.`

### GLITCH-RGB
On every beat the plate itself tears (an SVG displacement band filter plus an RGB channel split on the video) and the
titles split into red/green/blue copies and jittering slices, then snap clean. Between hits everything is still.
- Best for: streetwear, music, gaming, tech drops.
- Fonts: Latin Oswald 700 + IBM Plex Mono; Hebrew Karantina + Secular One. Palette: white titles, orange sub, RGB split.
- Motion: 0.28 s stuttering bursts on a measured beat grid; item words ride tracked garments.
- Build: run_style `GLITCH-RGB` (`scripts/styles/glitch.py`; example `examples/glitch-rgb/`).
- Source: `AE_GLITCH-RGB` (NORTHLINE underpass walk).
- Plate: cuts OK (max 6), 6-20 s · subject centred, walking or posing; plain walls or sky either side · 25% free both sides · locked or slow push; hits come from the music · track: items/garments (optional, for pinned words) · music beat grid.
- Prompt: `Titles: GLITCH-RGB - on each beat the frame tears and the words split into RGB slices, then snap clean.`

### NEON-SIGN
Neon tubes mounted in the scene: outline tubes (hollow stroke) and solid tubes with a white-hot core and coloured
glow, a real stutter on strike and a rare buzz later, a coloured light spill on the plate, signs turned onto the wall
plane in perspective towards the plate's vanishing point, and a mirrored reflection on the wet floor.
- Best for: nightlife, streetwear, bars and restaurants, city launches.
- Fonts: Hebrew Karantina 700 tubes + a Suez One accent line; Latin Tilt Neon. Palette: per-tube colour (pink, cyan, orange, yellow).
- Motion: deterministic flicker-on, hum, buzz dips; reflection follows the sign's level.
- Build: run_style `NEON-SIGN` (`scripts/styles/neon.py`; example `examples/neon-sign/`).
- Source: `AE_NEON-SIGN` (NORTHLINE underpass, Hebrew).
- Plate: one take, no cuts, 6-20 s · symmetrical corridor or street, subject in the centre third, blank walls left and right · 25% free both sides · locked-off or very slow push · no tracking.
- Prompt: `Titles: NEON-SIGN - neon tubes mounted on the walls in perspective, flicker-on, glow spill and a wet-floor reflection.`

### KEYNOTE-REVEAL
Apple-keynote pacing: one huge number or word per shot, a mask-wipe reveal (right-to-left for Hebrew), numbers count
up with their unit glued on, a small label beneath, a clean fade-and-blur exit and a soft vignette for contrast.
- Best for: product specs, EV and tech launches, fundraising and results decks as video.
- Fonts: Hebrew Suez One + Secular One; Latin Jost 700 + 300. Palette: white-to-ice gradient numbers, grey labels.
- Build: run_style `KEYNOTE-REVEAL` (`scripts/styles/keynote.py`; example `examples/keynote-reveal/`).
- Source: `AE_KEYNOTE-REVEAL` (AURA EV night drive, Hebrew).
- Plate: cuts OK (max 6), 8-24 s · subject off-centre or small; the centre third calm (sky, windscreen, dark interior) · no free space needed · slow, smooth, steady · no tracking.
- Prompt: `Titles: KEYNOTE-REVEAL - one huge counting number per shot, mask-wipe reveal, unit + small label, clean fades.`

### SPLIT-FLAP
A departure board: every cell is a real split flap (top/bottom halves and a falling leaf in CSS 3D) that riffles
through characters before landing, staggered in reading order; cells can re-flip later (a status change). Each column
carries its own direction, so Hebrew destinations fill right-to-left while times stay left-to-right.
- Best for: travel, airlines, hotels, events, launch schedules.
- Fonts: Hebrew Karantina 700 cells + Secular One labels; Latin Oswald 700 + Jost 300. Palette: charcoal cells, cream letters, yellow status.
- Build: run_style `SPLIT-FLAP` (`scripts/styles/splitflap.py`; example `examples/split-flap/`). Replaces the proposed SPLIT-FLAP.
- Source: `AE_SPLIT-FLAP` (first-person travel walk, Hebrew).
- Plate: cuts OK (max 4), 8-24 s · subject in the lower two thirds; the top band free for the board · 30% free top · gentle walk or glide · no tracking.
- Prompt: `Titles: SPLIT-FLAP - departure board, every cell flips through letters and lands; a status re-flips later.`

### SIGNATURE-WRITE-ON
Handwriting and marker annotations that draw themselves: notes write on (the outline draws while a sweep reveals the
ink in reading direction), wobbly hand circles, boxes, underlines and arrows draw on with stroke-dashoffset, pinned to
tracked objects so they ride the footage. Merges the proposed MARKER-WRITE-ON.
- Best for: real estate, tutorials, coaching, product walkthroughs, anything "look here".
- Fonts: Latin Caveat 700 hand; Hebrew hand Karantina + Secular One. Palette: ink (dark on bright skies, white on dark) + red marker.
- Build: run_style `SIGNATURE-WRITE-ON` (`scripts/styles/writeon.py`; example `examples/signature-write-on/`).
- Source: `AE_SIGNATURE-WRITE-ON` (SEAVIEW 24 drone climb).
- Plate: one take, no cuts, 8-20 s · features readable and not moving too fast; open sky or wall on one side for the handwriting · 30% free left · smooth drone climb, slow glide or locked · track: each annotated feature.
- Prompt: `Titles: SIGNATURE-WRITE-ON - handwritten notes write on, red hand circles and arrows pinned to the tracked features.`

### BROADCAST-PACK
A live sports package: score bug with a running match clock and a score change (flash + GOAL tab), a LIVE ticker, a
lower-third riding the tracked player, a REPLAY bug and stinger wipes across the cuts. Hebrew mirrors the layout.
Replaces the proposed SCOREBUG-LIVE.
- Best for: sport, esports, live events, "match day" promos.
- Fonts: Latin Oswald 700 + Archivo 500; Hebrew Secular One. Palette: navy panels, red accent, gold clock/goal.
- Build: run_style `BROADCAST-PACK` (`scripts/styles/broadcast.py`; example `examples/broadcast-pack/`).
- Source: `AE_BROADCAST-PACK` (football spot).
- Plate: planned cut list (max 4), 10-20 s · player readable in the intro and result shots; top corners and the bottom band free · 15% free top · broadcast-style: tracking, slow motion on the replay · track: player.
- Prompt: `Titles: BROADCAST-PACK - live score bug with running clock, ticker, lower-third on the tracked player, stinger wipes, goal update.`

### FILM-TITLE-CARD
Cinema title design in two card modes plus a credits roll: `anderson` (centred, symmetric, letter-spaced kicker, thin
frame with corner ornaments, gentle fades) and `bass` (Saul Bass cut-paper bars slamming in on diagonals with the
title set on them), then a two-column credits roll that mirrors for Hebrew.
- Best for: trailers, brand films, short films, chapter openers, end credits.
- Fonts: Latin Jost (Anderson) / Oswald 700 (Bass); Hebrew Suez One + Secular One. Palette: cream ink; Bass red/black/cream.
- Build: run_style `FILM-TITLE-CARD` (`scripts/styles/filmcard.py`; example `examples/film-title-card/`).
- Source: `AE_FILM-TITLE-CARD` (SPARTA battle).
- Plate: planned cut list (max 6), 12-30 s · wide establishing shots with dust, sky or floor space; hero off-centre in the last shot · 25% free bottom · cinematic, grounded; no whips · no tracking.
- Prompt: `Titles: FILM-TITLE-CARD - a Wes Anderson chapter card, a Saul Bass cut-paper title and a two-column credits roll.`

### PARTICLE-TEXT
Words that form out of embers, sand or smoke, resolve into the crisp word, and dissolve back. The text is rasterised
into points once; every particle position is an analytic function of (t, seed), so any frame renders identically.
An optional soft dark pool keeps the word legible on light plates.
- Best for: food, fire, beauty, fragrance, elemental brand words.
- Fonts: Latin Jost 700 + 300; Hebrew Suez One + Secular One (canvas direction set for RTL). Palette per mode (ember, sand, smoke).
- Build: run_style `PARTICLE-TEXT` (`scripts/styles/particles.py`; example `examples/particle-text/`).
- Source: `AE_PARTICLE-TEXT` (EMBER kitchen).
- Plate: cuts OK (max 5), 8-20 s · subject low or to one side; dark, low-detail space above it · 30% free top · slow push or locked; cuts on the recipe steps · no tracking.
- Prompt: `Titles: PARTICLE-TEXT - words assemble from embers / sand / steam, resolve crisp, then dissolve back.`

### FLIP-MONTAGE-LOGO
The Marvel-style closer: frames pulled from the plate itself flip past as 3D pages on an accelerating clock, each with
its own punch-in and treatment and a growing brand tint, then the last page falls away to the wordmark on a colour
block with a light sweep. Frames are extracted with ffmpeg at build time.
- Best for: brand closers and openers, drops, trailers.
- Fonts: Latin Oswald 700 + Jost 300; Hebrew Karantina + Secular One. Palette: brand colour block, white wordmark.
- Build: run_style `FLIP-MONTAGE-LOGO` (`scripts/styles/flipmontage.py`; example `examples/flip-montage-logo/`).
- Source: `AE_FLIP-MONTAGE-LOGO` (NORTHLINE).
- Plate: cuts OK (max 6), 6-30 s · variety across the shot (close-ups, wides, details) makes the flip read · no free space needed · any · no tracking.
- Prompt: `Titles: FLIP-MONTAGE-LOGO - pages of the film flip faster and faster, then resolve into the logo on a colour block.`

### TEXT-ON-PATH
Words riding a tracked road, river or trail: the path is rebuilt every frame through the tracked points (smoothed
Catmull-Rom), the route draws on as a glowing line, and each line slides along it (SVG textPath) bending with the road.
The text rides an upright copy of the route, so letters never stand on their heads; Hebrew works because Chrome's bidi
orders it (never put direction="rtl" on a textPath: Chrome drops the text).
- Best for: travel, logistics, real-estate location, sport routes (runs, rides).
- Fonts: Latin Oswald 700 + Jost 500; Hebrew Secular One. Palette: route green glow, white text with dark outline.
- Build: run_style `TEXT-ON-PATH` (`scripts/styles/textpath.py`; points from `track.py`; examples `examples/text-on-path/`, Hebrew `spec_he.json`).
- Source: `AE_TEXT-ON-PATH` (coastal aerial).
- Plate: one take, no cuts, 8-15 s · the route clearly visible and roughly flat to camera, not hidden behind buildings · no free space needed · smooth drone, constant slow push and slight descent; no rotation · track: route points (planar, track.py).
- Prompt: `Titles: TEXT-ON-PATH - the words ride the tracked road as a glowing route draws on.`

## Not offered
- Comic multi-colour pop as the main language of a premium ad (see COMIC-POP: beats only, playful brands only).
- "Security camera" face-recognition boxes on fashion: rejected; use STOMP-ESCORT or GLASS-CALLOUT.
