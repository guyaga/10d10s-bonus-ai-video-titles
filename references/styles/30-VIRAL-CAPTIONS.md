# #30 VIRAL-CAPTIONS · Viral word-by-word captions

> Huge 1–3-word captions that bounce in on every spoken word, keywords in colour, an emoji popping above the key word.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/viral-captions.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_VIRAL-CAPTIONS.mp4
> Runner: run_style VIRAL-CAPTIONS · Example: examples/viral-captions

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: talking-head reels, product explainers with a voiceover, founder videos, UGC ads, podcast clips cut for social. Anything where the **voice carries the message** and the viewer watches muted half the time.
- Avoid when: there is no voice (use KINETIC-HE or STOMP-ESCORT instead); premium or luxury tone (too loud, use PRESIDENTIAL-SERIF or QUOTE-TESTIMONIAL); long dense sentences with no natural 1–3-word chunks; footage whose bottom quarter is busy (the captions sit there).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` default .25 (the VO carries the sound) |
| Caption group `.grp` | 1–3 words centred on one line, `top = y × 1080` | one group visible at a time; wraps with 120 px side padding |
| Word `.w` | each word a separate span | white fill, thick black stroke (`paint-order: stroke fill`), a hard drop 1/18 of the size plus a soft shadow |
| Keyword `.k` / `.k2` | a word listed in `keywords` | alternates `key` (yellow) and `key2` (green) colours in order of appearance |
| Emoji `.em` | a Twemoji SVG above its own word | 1.25 × the font size, positioned from the laid-out word (so RTL and wrapping work) |

## Timing and motion
Times come from the word-timing file (`t` = when each word is spoken).
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Group | first word − .02 s (set visible) | .16 s from scale .9, y 30 | back.out(2.6) | until last word + `hold` (.6) + .35, capped at next group − .02 | cut (set opacity 0) | none |
| Unspoken words | group start | set | none | at `dim` opacity (.5) | – | – |
| Spoken word | its `t` | .22 s from scale 1.55, tilt ±3°, y 18 | back.out(3.4) | full opacity | with group | – |
| Syllable pulse | `t + (next − t) × .55` (only if the gap > .34 s) | .14 s from scale 1.12 | power2.out | – | – | – |
| Emoji | its word's `t` | .32 s from scale 0, rotation −25° | back.out(3) | min(group end, t + 1.1) | cut | – |
| Emoji float | t + .3 | .5 s to y −24 | sine.out | – | – | – |
- Stagger: none. Words land on the voice, so the voice is the stagger.
- Tilt alternates by word index (even −3°, odd +3°) and is mirrored for RTL.
- Grouping: `max_words` per group (3), and a group also ends on a word ending with . , ! ? …
- Numbers: a digit-only token is glued to the next word ("6 שעות", "100 %") so a number never stands alone.
- The signature move: the **1.55 → 1 overshoot bounce with a 3° tilt on each spoken word**, while the rest of the group waits at 50% opacity so the reader sees the whole phrase and the beat together.

## Typography
- Latin: Rubik 900 (display), 150 px default, as written (no forced case). Stroke width `max(8, size/12)` px.
- Hebrew: **Secular One** (default pair `secular`). For a louder, condensed look use `"pair": "karantina"` (Karantina 700). Suez One only for a premium, quieter caption. RTL is set on the group; tilt and emoji positions follow it. Prices as ש״ח, never ₪.
- Maximum copy: 3 words per group at 150 px fits 1920 − 240 px. Words over ~12 characters need `max_words: 2` or `size: 120`.

## Colour and surface
- Roles: `text` #ffffff, `key` #ffe14d (yellow), `key2` #39ff88 (green), `stroke` #000000. Brand swap: keep `text` white and `stroke` black for legibility and put the brand colours in `key`/`key2`.
- Surfaces: no panel. Readability comes from the stroke plus a 0 / size/18 hard shadow and a 0 / size/9 / size/5 rgba(0,0,0,.45) soft shadow.

## Layout and safe zones (1920×1080 canvas)
- Caption centre at `y` × 1080 (default .72 → 778 px; the sample uses .86 → 929 px). Side padding 120 px.
- Emoji centre at caption top − 1.2 × size.
- Keep the caption clear of faces: if the speaker's chin is below 70% of the frame, raise nothing, push `y` to .86 and reduce `size`.
- 9:16: the canvas is 1920×1080; for a vertical deliverable, crop the render and set `y` ≈ .66 and `size` ≈ 110 so 2 words fit the crop width.

## What the footage must give you
- Shoot it like this: cuts OK (max 6) · subject in the upper two thirds · 25% free at the bottom.
- Tracking: none. Timing comes from the word file (`scripts/word_times.py` on the voiceover, or any transcript with per-word start times).
- Matte: not needed.
- Good: a person or product in the top two thirds, a table, floor or dark studio below. Bad: busy lower thirds, burned-in subtitles, fast strobing footage.

## Build it
### A. With the kit
```bash
python scripts/word_times.py <AD> lines.json he        # or: supply your own [{"w","t"}] JSON
python scripts/run_style.py VIRAL-CAPTIONS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| words | word-timing JSON `[{"w": "...", "t": 1.23}]` | required |
| language | "he" or "en" | "en" |
| pair | Hebrew pairing (suez, karantina, secular, karantina-suez) | "secular" |
| fonts | override `{"display","dw","body","bw"}` | Rubik 900 (Latin) |
| keywords | words drawn in the keyword colours (punctuation ignored) | [] |
| emoji | `{"word": "🔥"}` emoji popped above that word (Twemoji SVG, downloaded once) | {} |
| max_words | words per group | 3 |
| hold | seconds a group stays after its last word | .6 |
| dim | opacity of not-yet-spoken words (0 = appear only when spoken) | .5 |
| y | caption centre, fraction of frame height | .72 |
| size | font size in px | 150 |
| colors | `{"text","key","key2","stroke"}` | #ffffff / #ffe14d / #39ff88 / #000000 |
| sfx | UI pop at each emoji (.28 volume) | true |
| vo, vo_vol | voiceover file and volume | –, 1 |
| music, music_vol | music bed | –, .35 |
| plate_vol | clip audio | .25 |
| name, track | project name; optional track | style id; frame clock from the clip |
```json
{
 "name": "my-captions", "clip": "clips/my_clip.mp4", "words": "tracks/my_words.json",
 "language": "en", "keywords": ["FREE", "today"], "emoji": {"today": "🔥"},
 "vo": "voice/my_vo.mp3", "music": "shared/sfx/my_bed.mp3", "music_vol": 0.3, "y": 0.84
}
```
### B. The core move in HyperFrames/GSAP
```js
// G = [{t:[word times], end}], built from the word file; tl is the paused timeline on window.__timelines["main"]
G.forEach((g, gi) => {
  tl.set(`#g${gi}`, {opacity: 1}, g.t[0] - .02); tl.set(`#g${gi}`, {opacity: 0}, g.end);
  tl.fromTo(`#g${gi}`, {scale: .9, y: 30}, {scale: 1, y: 0, duration: .16, ease: "back.out(2.6)", immediateRender: false}, g.t[0]);
  g.t.forEach((t, wi) => {
    const s = `#g${gi}w${wi}`, tilt = (wi % 2 ? 1 : -1) * 3 * (RTL ? -1 : 1);
    tl.set(s, {opacity: .5}, g.t[0] - .02); tl.set(s, {opacity: 1}, t);
    tl.fromTo(s, {scale: 1.55, rotation: tilt, y: 18}, {scale: 1, rotation: 0, y: 0, duration: .22, ease: "back.out(3.4)", immediateRender: false}, t);
    const nxt = g.t[wi + 1] ?? t + .45;
    if (nxt - t > .34) tl.fromTo(s, {scale: 1.12}, {scale: 1, duration: .14, ease: "power2.out", immediateRender: false}, t + (nxt - t) * .55);
  });
});
```

## Adapting it to the user's project
- Content: record or generate the voiceover first, then run `word_times.py`. Choose 4–6 keywords (the product name, the benefit, the number) and 2–4 emoji at most.
- Language: Hebrew → `"language": "he"`, Secular One. Put numbers as digits with their unit; the kit glues them.
- Brand: brand colours into `key` / `key2`; keep text white and stroke black.
- Vertical 9:16: see Layout; fewer words per group.
- Longer clips: nothing changes, groups are generated from the words. For very fast speech, set `max_words: 2` and `hold: .3`.

## Sound
- `ui_pop` at .28 on every emoji. The voiceover is the main track (`vo_vol` 1); a music bed at .3–.35; plate at .2–.25.

## Pitfalls and QA checklist
- [ ] Word timings match the audio (scrub 3 random words); a late word looks like a bug.
- [ ] No group overlaps a face; lower `y` or `size` if it does.
- [ ] Emoji download needs internet once (Twemoji CDN); after that it's cached in assets/emoji.
- [ ] Emoji keys match the spoken word after punctuation is stripped ("אוויר." = "אוויר").
- [ ] Hebrew digits stay glued to their word and read in the right order.
- [ ] Not more than one emoji per group; more reads as spam.
