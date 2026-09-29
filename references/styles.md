# Style catalog

Every style below was built and rendered (source listed). Previews live in `catalog/previews/<id>.mp4`; open
`catalog/index.html` to browse them. The user picks by **ID**; you build from the entry.

How to read an entry
- **Build** says which route runs it. All 22 are runnable from the skill:
  - `run_style` = parametrised builder: `python scripts/run_style.py <ID> --spec spec.json` (7 styles; copy
    `examples/<id>/spec.json`; every key is documented at the top of `scripts/styles/<module>.py`).
  - `adkit` = declarative elements in a spec: `python scripts/run_ad.py <AD> --spec spec.py` (7 styles).
  - `bespoke` = a run_ad spec whose look lives in the `html_front` / `html_behind` / `css` / `js` / `fonts` / `assets`
    hooks (8 styles). The recipe files in `references/recipes/bespoke/` are the originals: they run once their media
    (clip, track, matte, VO, data files) is in place, but a new subject means rewriting them, not swapping the text.
    Only `examples/E8_tower_bespoke.py` ships with its data files.
- **Prompt** is the one line a user pastes. Swap the brand colour and fonts freely; keep the motion recipe.

Two rules from the field:
1. **One bespoke visual language per piece.** Styles are starting points, not a house style. Running every video
   through the same kit made them all look the same (rejected). Mix at most one family per piece, then tailor it to the
   subject's own world: what does this product's industry print, measure, stamp or display?
2. **Premium beats loud.** A single accent colour. Multi-colour comic pop (yellow/pink/cyan bursts) was built and
   rejected as childish; it is still in adkit (`theme` flag `pop`) but do not offer it.

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
- Prompt: `Titles: STOMP-ESCORT - Anton words escorting each tracked item, red index tags + white price stickers, accent #E63B2E, 120 BPM grid.`

### STOMP-BEHIND
Same words, but set **between the plate and a matted subject**, so the model walks in front of her own title.
- Best for: hero reveals, fashion, athletes, anything with a clean silhouette.
- Fonts: Anton + Bodoni Moda. Palette: white words, red shadow/accents.
- Motion: stomp on the beat; the word sits in `html_behind` / `behind: true`; needs `mattes/<AD>_alpha.webm`
  (`npx hyperframes remove-background`). Keep words huge (500-700 px) so the occlusion reads.
- Build: adkit `stomp {behind:true}` or `kine {behind:true}`.
- Source: `D1_stomp_behind_v2.mp4`.
- Prompt: `Titles: STOMP-BEHIND - giant Anton words behind the subject (matte), white with red accent, stomp on the beat.`

### GLASS-CALLOUT
Transparent outlined words (translucent fill + stroke) and smoked-glass price cards; quieter than ESCORT.
- Best for: premium retail, beauty, calm luxury, when the footage must stay the hero.
- Fonts: Anton outline + Bodoni Moda. Palette: white stroke on rgba(0,0,0,.25) fill, glass panels.
- Motion: same beat grid, softer (no hard shadow), cards blur in.
- Build: adkit `stomp {color:"rgba(17,17,17,.38)", stroke:"5px #fff"}` + `tag` (glass panel).
- Source: `D1_stomp_glass_v2.mp4`.
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
- Prompt: `Titles: COUNTDOWN-CTA - flash-sale stack with 15 s live countdown, struck total + sale price, SHOP NOW, accent #E63B2E.`

### KINETIC-HE
Hebrew word-by-word social stomps synced to the voice: Rubik 900 / Karantina 700 words that land blurred->sharp with a
squash, one word in the accent colour, one outlined, hits shake the frame.
- Best for: Hebrew social ads, product launches, anything with a punchy VO.
- Fonts: Rubik 900 + Karantina 700 (big words), Assistant for small lines. Palette: white + one accent.
- Motion: word time = the VO word onset (`word_times.py`); `kine` lines; `hit:true` = shake + thump.
- Build: adkit `kine` (+ `ring`, `callout`, `counter`, `chip`, `lockup`), theme `he_bold`.
- Source: `E6_guyaga_aero_sneaker_HE.mp4`.
- Prompt: `Titles: KINETIC-HE - Hebrew voice-synced word stomps, Rubik 900 + Karantina, one accent word per line, hit shakes.`

### TAPE-HE
Hebrew slogans on highlight-tape strips (ink / accent / light), each strip wipes in right-to-left and slams, slightly
rotated, hard drop shadow; used where plain Hebrew text over footage was unreadable.
- Best for: Hebrew slogans, stats, CTAs over busy footage; readable at phone size.
- Fonts: Rubik 900 / Karantina. Palette: strips in ink + one accent; `tacc` auto-picks legible text colour.
- Motion: strip clip-path wipe 0.28 s, text pops 0.12 s later; optional bottom scrim.
- Build: adkit `tape` (+ `kine`, `counter`), theme `he_bold`.
- Source: `E4_firelink_through_the_smoke_HK.mp4` (all `_HK` renders).
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
- Prompt: `Titles: KINETIC-KARAOKE - voice-synced karaoke captions (accent pill on the spoken word) + punch zooms + tape slogans.`

### FLASH-CARD
A 4-frame full-screen word card (accent background, huge Karantina word) cut into the edit on the biggest beat.
- Best for: the one moment that must hit (brand name, "GOAL", "SOLD").
- Fonts: Karantina 700 (auto RTL/LTR by script). Palette: accent bg + ink word, or inverse.
- Motion: on for `dur` 0.16 s, scale 1.25 -> 1. Use once or twice per piece, never more.
- Build: adkit `flash`.
- Source: `E3_aura_night_drive_SX.mp4` ("AURA!").
- Prompt: `Titles: FLASH-CARD - one 4-frame full-screen word card on the biggest beat, accent background.`

### SPEED-STAT
Sports broadcast stat hits: a giant "9 MS" contact-time stomp, callout leaders to the boot, a live ball-speed counter
riding the tracked ball, then a giant red GOAL with a brand lockup.
- Best for: sport, slow-motion product proof, anything measurable in motion.
- Fonts: Anton + Archivo. Palette: white / red `#E63B2E` / black panels.
- Motion: counter eases 0 -> value while following the tracked object; GOAL 680 px stomp with shake.
- Build: run_style `SPEED-STAT` (`scripts/styles/speedstat.py`; example `examples/speed-stat/`).
- Source: `E1_guyaga_strike_soccer.mp4`.
- Prompt: `Titles: SPEED-STAT - broadcast stat hits: huge Anton numbers, live counter on the tracked ball, giant GOAL finish.`

### PRESIDENTIAL-SERIF
Restrained, premium: soft-in DM Serif Display words (BLOCK, VICTORY) with an accent underline, small glass tags,
a percent counter, few titles. Built after the comic version was rejected as childish.
- Best for: epic/brand films, leadership, battle or sport trailers that must feel expensive.
- Fonts: DM Serif Display (+ italic tagline) + Space Grotesk / Space Mono labels. Palette: cream + one red accent.
- Motion: `soft` = opacity + 1.12 -> 1 + small rise over 0.6 s, tiny shake; long holds.
- Build: adkit theme `sparta` (premium) with `stomp`, `tag`, `counter`, `lockup`, `meter`.
- Source: `E2_sparta_spartan_vs_machine.mp4`.
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
- Prompt: `Titles: STICKER-POP - heavy white Anton sticker words with a hard ink shadow, red index tag, white price sticker, stomp on the beat.`

### STOMP-SX
The dynamic Hebrew social version: coloured Karantina headline words that stomp in, ink tape lines for the
secondary copy, and a closing slogan with one accent word. Busier and faster than TAPE-HE.
- Best for: food, product, travel and brand social ads in Hebrew that need energy.
- Fonts: Karantina + Rubik 900. Palette: brand accent (e.g. #ff7a1a), ink, white.
- Motion: word-synced `kine` stomps (blur + scale + squash), hit shakes, `tape` strips wiping RTL.
- Build: adkit via `run_ad.py` with an SX spec. `examples/E6_sneaker_sx.py` is the template.
- Source: `E10_ember_chefs_pass_SX.mp4` (also E3, E5, E6, E9 `_SX`).
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
- Prompt: `Titles: TRACKED-TAGS - numbered glass tags tracked to each object, one stat panel, price total, English, restrained motion.`

### COMIC-POP
Multi-colour comic burst words (yellow, pink, cyan) with a starburst backing on the biggest beats.
- **Use sparingly.** It was rejected as childish for premium brands, and SPARTA was rebuilt as PRESIDENTIAL-SERIF.
  Offer it only for kids, gaming or deliberately playful brands, and only on one or two beats.
- Build: adkit theme flag `pop` on the big `stomp` words.
- Source: `E3_aura_night_drive.mp4` ("BRAKING").
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
- Prompt: `Titles: HUD-HELMET - holographic visor HUD, rotating rings + tick scales, cyan with red alerts, AI voice with live meter, Hebrew.`

### SCIFI-TARGETING
First-person targeting: brackets and ID tags locked to each robot (`T-01 // HEAVY`), a HOSTILE LOCK banner, FIRE,
then TARGETS NEUTRALIZED.
- Best for: action, gaming, defence/tech demos.
- Fonts: JetBrains Mono + Assistant. Palette: amber `#ffb547`, warn red, dark panels.
- Motion: box brackets snap to tracked boxes (`data-box`), tags follow, banners wipe.
- Build: run_style `SCIFI-TARGETING` (`scripts/styles/targeting.py`; example `examples/scifi-targeting/`).
- Source: `B3_final.mp4`.
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
- Prompt: `Titles: SPEC-SCAN - lab/CAD language: wireframe scan-in, exploded parts with numbered balloons, FEA heat map, 7-segment stats.`

### MAP-FLYOVER
Aerial map explorer: a route line draws across a planar-tracked city, pins with bilingual labels stick to places,
a distance counter runs, then a landing card on arrival.
- Best for: travel, real estate location, campus/venue arrival, logistics.
- Fonts: Assistant + JetBrains Mono. Palette: dark glass panels, lime/acc route.
- Motion: pins ride `track.py` (planar homography) points; route draws with stroke-dashoffset.
- Build: run_style `MAP-FLYOVER` (`scripts/styles/mapflyover.py`; points from `track.py`; example `examples/map-flyover/`).
- Source: `TEST_A_map_to_ono.mp4`.
- Prompt: `Titles: MAP-FLYOVER - route drawing over a tracked aerial, pinned bilingual place labels, distance counter, arrival card.`

### CAMPUS-AR
AR place labels on a walking tour: small glass tags pinned to real features (Library, Study area, Podcast studio,
Skylight), a voice waveform, a person tag, an end logo card.
- Best for: campus/venue/office tours, museums, retail wayfinding.
- Fonts: Assistant + mono. Palette: dark glass, thin accent rule.
- Motion: tags clip-wipe in, ride tracked anchors, fade on exit.
- Build: run_style `CAMPUS-AR` (`scripts/styles/campus.py`; example `examples/campus-ar/`).
- Source: `TEST_C_campus_ar.mp4`.
- Prompt: `Titles: CAMPUS-AR - small bilingual AR tags pinned to real places along a walk, glass panels, waveform for voice.`

### HUD-CLEAN
The first, quieter visor HUD: a thin vitals column, a heading tick scale, and one red alert panel. No rings, no voice.
- Best for: when HUD-HELMET is too much; documentary-feeling sci-fi, pilots, divers, climbers.
- Fonts: Assistant + JetBrains Mono. Palette: pale cyan-white, amber, alert red.
- Build: `run_style.py HUD-HELMET` with the reticle, radar and voice blocks left out of the spec (every block is optional).
  The original recipe is `legacy_shots.py` → `B4` (Hebrew) / `B2` (English).
- Source: `B4_helmet_hebrew_24s.mp4` (also `B2_final.mp4`, `TEST_B_scifi_pilot.mp4`).
- Prompt: `Titles: HUD-CLEAN - quiet visor HUD: thin vitals column, heading tick scale, one red alert panel, no rings.`

### CYBER-DOSSIER
A character intro as a city dossier: a bilingual location card, a pilot ID panel, and suit status bars.
- Best for: game trailers, character reveals, sci-fi shorts, "meet the hero" openers.
- Fonts: JetBrains Mono + Assistant. Palette: amber #ffb547 on near-black glass.
- Build: reference recipe `legacy_shots.py` → `B1`.
- Source: `B1_final.mp4`.
- Prompt: `Titles: CYBER-DOSSIER - character intro dossier: bilingual location card, pilot ID panel, suit status bars, amber mono type.`

### ARRIVAL-CARD
A destination lower-third: the place name in two languages, coordinates and a distance line, and a green ARRIVED chip.
- Best for: travel, campus and real-estate arrivals; the last shot of a MAP-FLYOVER.
- Fonts: Assistant + JetBrains Mono. Palette: green #9bd14a, dark glass, off-white.
- Build: reference recipe `legacy_shots.py` → `A2`. It pairs with `run_style.py MAP-FLYOVER` as the next shot.
- Source: `A2_final.mp4`.
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
- Prompt: `Titles: LENS-POSTCARD - seen through a glasses lens: stamp mascot speech bubbles, translated sign, airmail postcards, receipt.`

---

## Proposed, not yet built
Ideas that fit the kit but have no render yet. Offer them as "new", and budget a bespoke build.
- **SCOREBUG-LIVE** (proposed, not yet built): live sports-broadcast package - score bug, player lower-thirds riding the
  tracked player, replay wipe. Builds on SPEED-STAT + `tag` follow.
- **SPLIT-FLAP** (proposed, not yet built): departure-board letters that flip into place for travel/airline/hotel copy.
- **MARKER-WRITE-ON** (proposed, not yet built): hand-drawn marker circles/arrows and handwriting that writes on
  (stroke-dashoffset on SVG paths) for tutorials, coaching, real-estate walk-throughs.

## Not offered
- Comic multi-colour pop as the main language of a premium ad (see COMIC-POP: beats only, playful brands only).
- "Security camera" face-recognition boxes on fashion: rejected; use STOMP-ESCORT or GLASS-CALLOUT.
