# #51 PODCAST-TAGS · Video-podcast package

> Each host gets a name tag that rides them (tracked); the active speaker's tag lights up with a live equalizer driven by the real audio while the other dims; an EP chip with a blinking REC sits top-corner, topic chapters swap in a lower strip, and a thin waveform bar across the bottom follows the voice.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/podcast-tags.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_PODCAST-TAGS.mp4
> Runner: run_style PODCAST-TAGS · Example: examples/podcast-tags/ (spec.json + objects.json)

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: video podcasts, interviews with 2–3 people, panels, livestream highlights, clips cut from long conversations for social.
- Avoid when: there's only one person (use LOWER-THIRD-CORP), the shot cuts between cameras every few seconds (tags jump; use fixed supers per cut), or the audio is music-heavy (the meters stop meaning "who talks").

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#wave` | 96 thin bars across the bottom (120 px side insets, 40 px from the bottom, 30 px tall) | each bar shows the loudness 0.05 s × position ago: a scrolling waveform |
| `#tp` | topic strip, bottom 92 px, centred: accent "TOPIC"/"נושא" cell + dark cell with the topic (34 px) | topics swap vertically |
| `.hg > .tg` | one tag per host, riding the tracked box (anchor "b", dy −40 by default) | dark glass `rgba(14,12,10,.82)`, radius 16, blur 12 |
| `.eq` | 5-bar equalizer (6×40 px bars, accent) | driven by the audio envelope, only for the active host |
| `.nm` / `.rl` | name (40 px display) / role (22 px) | |
| `#ep` | episode chip top-corner: "EP 042" (accent), title, blinking REC dot | EP number and REC always in Manrope (Latin) |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| tags (y 20→0, stagger .12) | hosts_t (.3) | .60 | expo.out | whole clip | — | — |
| active/inactive state | every frame | — | from `talk` | active: opacity 1, scale 1.04; other: opacity .55, scale .96 | — | — |
| equalizer bars | every frame | — | envelope × 1.3 × wobble (0.55–1) | inactive: flat .12 | — | — |
| EP chip (fade, y −24→0) | episode.t | .55 | expo.out | — | — | — |
| REC blink (yoyo, 20 repeats) | episode.t+.5 | .50 | sine.inOut | ≈10 s | — | — |
| topic strip (fade, y 24→0) | first topic t−.1 | .55 | expo.out | — | — | — |
| topic i (yPercent 110→0, fade) | topic.t | .50 | expo.out | until next | yPercent −110 at next t−.3, .35 s | power2.in |
| waveform fade-in | .2 | .80 | — | whole clip | — | — |
- `talk` is the speaker map (who talks when). Get it from a transcript with speaker labels (or by listening); the meters then follow the real audio loudness per frame.
- Industry convention: name supers appear on a host's first line (within ~1 s) and hold ≥ 4 s; in long podcasts, re-show them after each cut or every ~2 minutes; the highlight follows the speaker, never lags more than ~0.3 s.
- The signature move: the tag that "breathes" with the real voice: equalizer + scale-up on the active speaker.

## Typography
- Latin: Manrope 700 names (40 px) and topics (34 px), Manrope 500 roles (22 px, +.12em). EP/REC always Manrope 700.
- Hebrew: `pair: "suez"` (default) = Suez One names and topics, Secular One roles and the TOPIC label ("נושא"). Everything mirrors; the EP chip moves to the right; EP number and REC stay Latin.
- Maximum copy: name ≈ 16 characters, role ≈ 24, topic ≈ 34 (nowrap).

## Colour and surface
- Roles: `panel` rgba(14,12,10,.82), `accent` #ffb13b (equalizer, EP, TOPIC), `text` #ffffff, `sub` #ece4da. REC dot #ff3b30. Waveform white 55%.
- Brand swap: accent = show colour; keep panels dark.

## Layout and safe zones (1920×1080 canvas)
- Tags ride each host's box (`anchor` b/t/c…, `dx`, `dy`; the tag is centred on the anchor and sits above it with `dy` −40). EP chip top 56, 70 px from the side. Topic strip bottom 92, centred. Waveform full-width at the bottom.
- Keep tags on the chest line, never over faces or mics; check the tallest host.
- 9:16: stacked two-shot; move the topic strip up (bottom ≈ 300) and drop the waveform.

## What the footage must give you
- Shoot it like this: one take, 8–30 s, two hosts at mics, both in frame, chests visible for the tags; the bottom 15% calm; locked-off.
- Tracking: vtrack.py with one object per host: `{"name": "host_left", "desc": "the woman on the left: head and upper body (tight box)"}`, `{"name": "host_right", ...}`.
- Audio: the clip's own audio drives the meters, or pass `audio` (e.g. the clean podcast mix).
- Matte: not needed.
- Good footage: two-shot podcast set. Bad: cuts every few seconds, hosts leaving frame, mics covering the chests.

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/podcast.mp4 objects.json tracks/podcast.json
python scripts/run_style.py PODCAST-TAGS --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip, track | video + vtrack JSON | required |
| hosts[] | {follow, anchor, dx, dy, name, role} | required; anchor "b", dx 0, dy −40 |
| talk[] | {host index, t, until}: who speaks when | [] (all dim) |
| episode | {no, title, t} | none; t .4 |
| topics[] | {text, t} | [] |
| audio | file whose loudness drives the meters | the clip's audio |
| hosts_t | when the tags appear | .3 |
| language / pair | he/en; Hebrew pair | en / "suez" |
| fonts | override | Manrope 700 / 500 |
| colors | {panel, accent, text, sub} | see above |
| sfx | REC beep + whoosh per topic | true |
| music, music_vol, plate_vol, name | — | none, .5, .9 |
```json
{
 "clip": "clips/ep42.mp4", "track": "tracks/ep42.json",
 "hosts": [{"follow": "host_left", "name": "Maya Levin", "role": "HOST"}, {"follow": "host_right", "name": "Dan Oren", "role": "GUEST · AI RESEARCHER"}],
 "talk": [{"host": 0, "t": 0, "until": 6.2}, {"host": 1, "t": 6.2, "until": 14.0}],
 "episode": {"no": "042", "title": "AI in everyday life", "t": 0.4},
 "topics": [{"text": "Why everyone talks about agents", "t": 1.2}, {"text": "What it means for work", "t": 7.0}]
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
// env = per-frame loudness 0..1 (24 fps) computed offline from the audio; talk = speaker map
const env = window.ENV, talk = [{host: 0, t: 0, until: 6.2}, {host: 1, t: 6.2, until: 14}];
const envAt = (t) => env[Math.max(0, Math.min(env.length - 1, Math.round(t * 24)))] || 0;
const who = (t) => (talk.find((s) => t >= s.t && t < s.until) || {host: -1}).host;
window.onPlace = (t) => {                       // state = f(time): seek-safe
  const a = who(t), lv = envAt(t);
  [0, 1].forEach((i) => {
    const tag = document.getElementById("h" + i), on = i === a;
    tag.style.opacity = on ? 1 : .55; tag.style.scale = on ? 1.04 : .96;
    [...document.getElementById("eq" + i).children].forEach((b, k) =>
      b.style.transform = `scaleY(${on ? Math.max(.12, Math.min(1, lv * 1.3 * (.55 + .45 * Math.sin(t * 17 + k * 1.9 + i)))) : .12})`);
  });
};
tl.set(".tg", {xPercent: -50, yPercent: -100}, 0);   // centre on the anchor with xPercent/yPercent (GSAP owns transform)
tl.fromTo(".tg", {y: 20}, {y: 0, duration: .6, ease: "expo.out", stagger: .12}, .3);
```

## Adapting it to the user's project
- Content: real names/roles; topics = the chapters of the conversation.
- Language: Hebrew → `"language": "he"`, pair suez; EP number stays Latin.
- Brand: accent = show colour; EP number from the user.
- Vertical 9:16: see layout.
- Longer clips: REC blinks ~10 s (20 repeats); extend `repeat` for long clips; add topics every 20–60 s.

## Sound
- `rec_beep` (.35) at the EP chip, `ui_whoosh` (.3) per topic change. The podcast audio stays on top (`plate_vol` .9).

## Pitfalls and QA checklist
- [ ] `talk` matches who actually speaks (highlight never on the silent host).
- [ ] Tags on chests, not faces/mics; tracking preview checked.
- [ ] Tag centring uses `xPercent/yPercent` in the same GSAP timeline (a CSS translate would be overwritten).
- [ ] Topic strip ≤ 34 characters.
- [ ] EP/REC in Latin even in Hebrew.
