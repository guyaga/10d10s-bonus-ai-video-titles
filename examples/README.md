# Example specs (real, rendered)

| file | style | notes |
|---|---|---|
| `E6_sneaker_sx.py` | KINETIC-HE + KINETIC-KARAOKE + FLASH-CARD + punch (SX = social dynamic stomp) | smoke-tested: builds and passes `hyperframes check` |
| `E4_fire_hk.py` | TAPE-HE + counters + tracked box/tag (HK = Hebrew kinetic) | voice envelope inlined as `env` |
| `E8_tower_bespoke.py` | ARCH-DRAWING, fully bespoke via `html_front` / `css` / `js` / `fonts` | data files alongside |

To run one: copy it to `<project>/specs/<AD>.py` and provide `clips/<AD>_720p.mp4` + `tracks/<AD>_vtrack.json`
(+ `mattes/<AD>_alpha.webm` when an element uses `behind`), then `python run_ad.py <AD>`. The object names in the
spec (`shoe`, `door`, ...) must exist in your vtrack json.

## #42-#61: the Kling 3.0 examples (one folder per style, `spec.json`)

These run through `run_style.py STYLE --spec examples/<style>/spec.json --root <project>`. Small data (vtrack json)
sits next to each spec; the plates are not in the repo. Put them in `<project>/clips/` (and the one large matte in
`<project>/mattes/`). Every plate was made with Kling 3.0 (`kling-video-v3_0`, 720p, 16:9, 10 s); its full prompt is
the `.txt` of the same name next to the original in `G_studio/kling_plates/`.

| plate (`clips/…`) | styles | notes |
|---|---|---|
| `talking-head.mp4` | LOWER-THIRD-CORP, SOCIAL-CTA, END-SCREEN | creator to camera, bright home studio |
| `podcast.mp4` | PODCAST-TAGS | two hosts at mics; track `tracks/podcast_vtrack.json` (in the example folder) |
| `phone-hands.mp4` | APP-UI-POPUPS, CHAT-BUBBLES | person on a sofa scrolling, screen never visible |
| `product-macro.mp4` | LEADER-CALLOUTS | gadget rotating on a dark plinth; track `tracks/product_vtrack.json` |
| `city-news.mp4` | BREAKING-NEWS | city street at dusk, emergency lights far away |
| `office-b-roll.mp4` | DATA-CHARTS, KPI-COUNTERS | open office, screens out of focus |
| `aerial_doc.mp4` | CHAPTER-MARKERS, DOC-LOCATION-STAMP, TIMELINE-HISTORY | slow drone over an old port; `aerial_track.json` |
| `portrait_testimonial.mp4` | QUOTE-TESTIMONIAL | medium close-up, window light |
| `minimal_architecture.mp4` | SWISS-GRID | slow push along white concrete |
| `gradient_glass.mp4` | GRADIENT-GLASS | abstract glass / gradient surface |
| `logo_metal.mp4` | LOGO-SHINE-REVEAL | dark brushed metal with a light sweep |
| `singer.mp4` + `mattes/singer_alpha.webm` | LYRIC-KINETIC-3D | matte: `npx hyperframes remove-background singer.mp4 -o mattes/singer_alpha.webm` (2.9 MB, not committed) |
| `property_villa.mp4` | LISTING-SPECS | dolly toward a villa at golden hour; `villa_track.json` |
| `ba_before.mp4` + `ba_after.mp4` | BEFORE-AFTER-SPLIT | same camera move twice: start frames from Kling `text_to_image` / `image_to_image`, then `image_to_video` |
