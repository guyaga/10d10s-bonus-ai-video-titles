# #37 BROADCAST-PACK · Live sports package

> A live sports graphics package: a score bug with a running match clock, a goal flash, a crawling LIVE ticker, a lower-third that rides the player, a REPLAY bug and stinger wipes on the cuts.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/broadcast-pack.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_BROADCAST-PACK.mp4
> Runner: run_style BROADCAST-PACK · Example: examples/broadcast-pack

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: sports highlights, amateur league and school games, esports, sponsor activations, sports-brand ads that borrow the TV look, "match day" social clips.
- Avoid when: non-sport content (use LOWER-THIRD-CORP or BREAKING-NEWS); footage with real scoreboards, sponsor boards or kit logos in frame (they clash); a single continuous shot with no replay moment (wipes need cuts).

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` .5 |
| Score bug `#bug` | brand header strip + one cell per team (colour bar, 3-letter code, score) + match clock | top-left 56/70 px (top-right in Hebrew), scaled 1.2 |
| Goal tab | a gold "GOAL" tab under the bug | appears on the goal |
| Lower-third `.lt` | name + role card pinned under the tracked player, with a small accent pointer | panel colour, 4 px accent top border |
| REPLAY bug `.rp` | top-right (top-left in Hebrew) label with a play triangle | pulses while the replay runs |
| Ticker `#tk` | 64 px bottom bar: accent "LIVE" block + crawling text | crawls left (right in Hebrew) |
| Stinger `.wp` | two skewed bands (accent, then panel) plus the brand name crossing the frame | centred on each cut |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Score bug | `bug_t` (.3 s) | .45 s from x −30 (x +30 in Hebrew) | power3.out | whole piece | – | – |
| Clock | – | ticks every second from `clock.start` at `clock.t` | – | – | – | – |
| Ticker | `ticker.t` | .4 s from y +64 | power3.out | crawls at `speed` px/s (160) | .3 s at `until` | default |
| Lower-third | `lower[].t` | .4 s clip-path open from the centre | expo.out | rides the player | .15 s fade before `until` | default |
| REPLAY bug | `replay[].t` | .3 s from x ±20 | default | pulses to .35 opacity every 1 s | .2 s at `until` | sine.inOut pulse |
| Goal | `goal.t` | score scales 1 → 1.6 → 1 (.15 s yoyo); bug row flashes gold 3 times (.08 s); tab drops in at +.1 s (.3 s) | power2.out / back.out(2) | – | – | – |
| Stinger | cut − .28 s | .56 s; two bands cross the frame, the second slightly delayed | easeInOut | – | – | – |
- The signature move: **the stinger wipe centred on the cut**. The accent band covers the frame at the exact cut frame, so the cut into and out of the replay is hidden behind the brand, just like a TV replay transition.

## Typography
- Latin: Oswald 700 (codes 36 px, scores 40 px, clock 34 px, lower-third name 40 px, stinger 110 px), Archivo 500 (header 20 px, role 22 px, ticker 28 px), tracking .1–.22em on labels.
- Hebrew: default pair `secular`: **Secular One** throughout; for a louder look use `pair: karantina` (Karantina 700 names and codes). The clock stays left-to-right with tabular digits. The layout mirrors: bug right, REPLAY left, ticker crawls right, wipes run the other way.
- Maximum copy: team codes 3 letters; name about 18 characters; role about 30; the ticker is unlimited (it loops three copies).

## Colour and surface
- Roles: `panel` #0b1f3a (navy), `accent` #e63b2e (red), `text` #ffffff, `gold` #ffd23f (clock, goal tab and flash). Team colour bars from `teams[].color`.
- Brand swap: `panel` = the league's dark colour, `accent` = its highlight. Keep `gold` for the clock (readability).
- Surfaces: flat panels with 0 10 30 / 0 12 30 rgba(0,0,0,.35) shadows; no gradients.

## Layout and safe zones (1920×1080 canvas)
- Bug: 70 px from the side, 56 px from the top. REPLAY: 70 px from the other side, 60 px from the top. Ticker: full width, bottom 64 px.
- Lower-third: centred under the player's box, `anchor` "b", `dy` 30 by default (the sample uses −160/−150 to sit over the player's legs in close shots).
- Leave the top corners and the bottom band free of key action in the footage.

## What the footage must give you
- Shoot it like this: planned cuts (max 4) · player readable in the intro and result shots; top corners and the bottom band free · 15% free at the top.
- Tracking: the player (vtrack.py), e.g. `{"objects": [{"name": "player", "desc": "the striker in the red kit, whole body"}]}`.
- Cut times: measure them (ai-ad-studio's cut detector, or scene detection) and put them in `wipes`.
- Good: intro shot → action in slow motion → result shot. Bad: real scoreboards, sponsor logos, numbers on kits.

## Build it
### A. With the kit
```bash
python scripts/vtrack.py clips/my_match.mp4 objects.json tracks/my_match_track.json
python scripts/run_style.py BROADCAST-PACK --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| teams | `[{"code","color","score"}]` | HOM (accent) 0 · AWY (#1e6cff) 0 |
| clock | `{"start": "MM:SS", "t"}` the match clock at video time t | {"start": "00:00", "t": 0} |
| goal | `{"team", "t", "label"}` | none |
| lower | `[{"follow","anchor","dx","dy","name","role","t","until"}]` | anchor b, dx 0, dy 30 |
| replay | `[{"t","until","label"}]` | label "REPLAY" |
| ticker | `{"text","t","until","speed","label"}` | speed 160, label "LIVE" |
| wipes | cut times for stingers | [] |
| brand | league name on the bug header and the stinger | "" |
| bug_t | when the score bug slides in | .3 |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "secular" |
| fonts | override faces | Oswald 700 + Archivo 500 |
| colors | `{"panel","accent","text","gold"}` | #0b1f3a, #e63b2e, #ffffff, #ffd23f |
| sfx | whoosh .6 before each wipe, pop .4 on each lower-third, stinger .7 on the goal | true |
| music, music_vol, vo, plate_vol, name, track | optional | –, .5, –, .5, style id, – |
```json
{
 "name": "my-match", "clip": "clips/my_match.mp4", "track": "tracks/my_match_track.json", "brand": "CITY CUP",
 "teams": [{"code": "RED", "color": "#e63b2e", "score": 0}, {"code": "BLU", "color": "#1e6cff", "score": 0}],
 "clock": {"start": "73:10", "t": 0}, "goal": {"team": 0, "t": 9.6},
 "lower": [{"follow": "player", "name": "#10 DANA LEVI", "role": "MIDFIELD", "t": 0.6, "until": 3.0}],
 "replay": [{"t": 3.4, "until": 9.2}], "wipes": [3.2, 9.4],
 "ticker": {"text": "LIVE · CITY CUP FINAL · RED 0-0 BLU", "t": 0.4}
}
```
### B. The core move (per frame, from onPlace)
```js
// stinger: two skewed bands cross the frame in .56 s, centred on the cut (easeInOut from JS_UTIL)
J.wipes.forEach((cut, i) => {
  const u = (t - (cut - .28)) / .56, el = $$("wp" + i);
  if (u < 0 || u > 1) { el.style.display = "none"; return; } el.style.display = "block";
  const p = 120 - 260 * easeInOut(u), q = 120 - 260 * easeInOut(clamp01(u * 1.15 - .08));   // band 2 lags
  const [a, b] = el.getElementsByClassName("band");
  a.style.left = (RTL ? 100 - p - 62 : p) + "%"; b.style.left = (RTL ? 100 - q - 30 : q + 18) + "%";
});
// match clock and ticker are pure functions of t
const sec = m0 * 60 + s0 + Math.floor(t - J.clock.t);
$$("clk").textContent = String(Math.floor(sec / 60)).padStart(2, "0") + ":" + String(sec % 60).padStart(2, "0");
const x = ((t - J.ticker.t) * J.ticker.speed) % (mv.scrollWidth / 3); mv.style.transform = `translateX(${RTL ? x : -x}px)`;
// CSS: .band { transform: skewX(-18deg); width: 62% }  .b2 { width: 30% }
```

## Adapting it to the user's project
- Content: real team codes, the real score before and after, the scorer's name and a stat in the role line.
- Language: Hebrew mirrors the whole package; team codes can stay Latin.
- Brand: league colours in `panel`/`accent`, league name in `brand`.
- Vertical 9:16: the bug and REPLAY stack at the top, the ticker at the bottom; the lower-third can stay pinned.
- Longer clips: more lower-thirds and replays; a wipe on every cut into and out of a replay.

## Sound
- `ui_whoosh` at .6 just before each stinger (−.3 s), `ui_pop` at .4 on each lower-third, `stinger` at .7 on the goal. Crowd and music at .5–.55.

## Pitfalls and QA checklist
- [ ] Each wipe's centre sits on the real cut frame.
- [ ] The lower-third never covers the player's face; adjust `dy`.
- [ ] The score changes exactly at the goal frame, and the clock runs forward only.
- [ ] Nothing real in the plate (kit numbers, sponsor boards) competes with the graphics.
