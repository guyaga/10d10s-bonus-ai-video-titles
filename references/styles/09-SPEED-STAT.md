# #09 SPEED-STAT · Broadcast stat hits

> Sports-broadcast graphics on a fast action cut: a bracket and name tag on the athlete, a giant "9 MS" stat stomp,
> leader-line callouts to the boot, a spinning ring on the ball, a live speed counter and trail, then a giant red
> GOAL (behind the player) and a brand lockup.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/speed-stat.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/E1_guyaga_strike_soccer.mp4
> Runner: run_style SPEED-STAT (`scripts/styles/speedstat.py`) · Example: examples/speed-stat/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: sport (a kick, a sprint, a jump, a swing), slow-motion product proof (a car braking, a racket hit), anything
  with a measurable number in motion; gear ads where the product causes the stat.
- Avoid when: nothing moves fast or nothing can be measured; the footage is one calm take (the package needs
  2–4 distinct shots); soft lifestyle tone.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's action cut | plate 0.4 |
| Big word (behind) | "GOAL", 680 px accent Anton | behind the athlete when `matte` is set |
| Trail | 10 px accent polyline following the tracked object's centre over the last 0.9 s | `trail` |
| Leader lines | white 3 px lines from a point inside a tracked box to each callout, 10 px accent dot | `callouts` |
| Player bracket + tag | 4 accent corner brackets around the athlete + name tag right of the box | `player` |
| Stat | "9 MS" Anton 300 px + mono caption | `stat` |
| Callout panels | dark glass panels with a 3 px accent top border | `callouts` |
| Ring + label | two counter-rotating dashed rings on the tracked object + changing mono label above it | `ring` |
| Speed counter | Anton 220 px number counting up + mono unit line | `counter` |
| Brand bug, lockup | top-left bug; bottom-centre name + line | `brand`, `lockup` |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Brand bug | `brand.t` (0.15) | 0.3 s, x −20 → 0 | default | to `until` | 0.2 s fade | — |
| Player bracket | `player.t` | brackets scale 1.4 → 1, 0.3 s | power3.out | to `until` | 0.05 s | — |
| Player tag | `player.t` + 0.1 | 0.3 s, x −16 → 0 | power3.out | to `until` | 0.05 s | — |
| Stat | `stat.t` | stomp from 2.2 (0.16 s) + shake; caption at +0.25, 0.2 s, y 14 → 0 | power4.out | to `until` | 0.08 s | — |
| Callout i | `c.t` | 0.25 s, x 30 → 0; its leader line draws from the tracked point every frame | power3.out | to `c.until` | 0.08 s | — |
| Ring | `ring.t` | scale 1.5 → 1, 0.3 s; rings rotate +220°/s and −140°/s | power3.out | to `until` | 0.08 s | — |
| Ring label | switches text at each `labels[i][0]` | instant | — | to `label_until` | 0.08 s | — |
| Speed counter | `counter.t` | stomp from 1.8; value = round(value × (1 − (1 − u)^3)), u over `dur` (1.6 s) from t + 0.05 | power4.out / cubic-out | to `until` | 0.08 s | — |
| Trail | `trail.t` | redrawn every frame from the last `len` (0.9 s) of tracked centres, sampled at 1/24 s | — | to `until` | — | — |
| GOAL | `big.t` | stomp from 2.4 + shake | power4.out | to the end | — | — |
| Lockup | `lockup.t` | stomp from 1.6 + shake | power4.out | to the end | — | — |

- Shake (common): x −14, +11, −6, 0 px and y +6, −5, +3, 0 px over 0.04/0.04/0.04/0.06 s; flash 0.4 → 0 in 0.14 s.
- Cut sync: each block's `t`/`until` sits on the shot cuts (sample cuts at 2.54, 7.75, 11.125 s): the player tag
  belongs to shot 1, stat + callouts to the macro shot, counter + trail to the flight shot, GOAL to the hero shot.
- The signature move: **the number that is true to the motion**. The counter counts up while the trail draws behind
  the moving object and the ring spins on it; then a giant word lands on the result.

## Typography
- Latin: Anton for every big thing (stat 300 px, callout titles 36 px, counter 220 px, GOAL 680 px, lockup 76/48 px,
  brand 40 px .06em, player name 34 px); JetBrains Mono for data lines (stat caption 26 px .14em, callout subs 18 px,
  ring label 24 px, unit 26 px .2em, tag 18 px .14em); Archivo is the fallback body.
- Hebrew: the builder's fonts are Latin; for Hebrew copy override in a css block of a custom spec or use Karantina 700 for
  the big words and Secular One for the data lines (numbers stay LTR, glued to their unit: "121 קמ״ש").
- Max copy: stat ≤ 5 characters ("9 MS"); callout title ≤ 20, sub ≤ 26; unit ≤ 26; GOAL ≤ 5 letters at 680 px.

## Colour and surface
- `colors`: white `#ffffff`, accent `#E63B2E`, ink `#0b0b0d`. Panels = ink at 82 % (`color-mix`), callouts with a 3 px
  accent top border, player tag with a 4 px accent left border; sub lines `#ffd2cf`.
- Hard shadows: stat and counter 8 px 8 px 0 accent; GOAL accent fill, 6 px ink stroke, 14 px 14 px 0 ink shadow.
- Brand colours: accent = team/brand colour; keep white and near-black.

## Layout and safe zones (1920×1080 canvas)
- Brand 84 / 64; stat at (`x` 90, `y` 520), vertically centred on y; callouts right column x 1260, y 130 + 200 × i;
  counter bottom-left (x 96, bottom 90); GOAL top-centre y 60; lockup bottom-centre 70 px up; ring 520 px square on
  the object; ring label 60 px above the object.
- The action should happen centre/right so the left third holds the stat and counter (30 % free on the left).
- 9:16: not designed for vertical (left/right columns); re-lay out stat above and counter below the action.

## What the footage must give you
- Shoot it like this: planned cut list (max 4), 12–18 s · one idea per shot: wide athlete, extreme close-up of the
  contact, the object crossing the frame, hero wide · 30 % free on the left · energy from subject speed and speed
  ramps · matte for the hero shot.
- Tracking: vtrack objects per the sample:
  ```json
  {"context": "A 15-second football commercial with hard cuts: run-up, macro of the boot hitting the ball, ball flight, celebration.",
   "objects": [{"name": "player", "desc": "the athlete's whole visible body"}, {"name": "ball", "desc": "the ball"},
               {"name": "boot", "desc": "the kicking boot (close shots only)"}]}
  ```
- Matte: for GOAL behind the athlete (`npx hyperframes@0.8.84 remove-background …`).
- Good: clean shots with one object each. Bad: logos/numbers on kits (the plate prompt bans them), shaky whip-pans.

## Build it
### A. With the kit
```bash
python scripts/run_style.py SPEED-STAT --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip, track | media (required) | — |
| brand | `{name, tag, t, until}` | none |
| player | `{obj, title, sub, t, until}` | none |
| stat | `{text, sub, x, y, t, until}` | x 90, y 520 |
| callouts | `[{title, sub, obj, fx, fy, x, y, t, until}]` (leader from point fx/fy inside obj's box) | fx/fy .5, x 1260, y 130 + 200 i |
| ring | `{obj, t, until, labels: [[t, text]], label_until}` | none |
| counter | `{t, until, value, dur, unit, x, bottom}` | dur 1.6, x 96, bottom 90 |
| trail | `{obj, t, until, len}` | len 0.9 s |
| big | `{text, t, size}` (behind with `matte`) | size 680 |
| lockup | `{name, line, t}` | none |
| colors | `{white, accent, ink}` | `#ffffff / #E63B2E / #0b0b0d` |
| sfx, music, music_vol, vo, plate_vol, matte, name | mix / media | true, –, 0.55, –, 0.4, –, speed-stat |

A minimal spec:
```json
{
 "name": "my-stat",
 "clip": "clips/my_action.mp4", "track": "tracks/my_action_vtrack.json", "matte": "mattes/my_action_alpha.webm",
 "stat": {"text": "0.3 S", "sub": "REACTION TIME", "t": 2.7, "until": 6.0},
 "callouts": [{"title": "CARBON FRAME", "sub": "-22% weight", "obj": "racket", "fx": 0.5, "fy": 0.3, "t": 3.4, "until": 6.0}],
 "ring": {"obj": "ball", "t": 6.1, "until": 9.0, "labels": [[6.1, "SPIN 42 RPS"]]},
 "counter": {"t": 6.2, "until": 9.0, "value": 187, "unit": "KM/H · SERVE SPEED"},
 "trail": {"obj": "ball", "t": 6.1, "until": 9.0},
 "big": {"text": "ACE", "t": 9.3},
 "lockup": {"name": "MY BRAND", "line": "SERVE HARDER", "t": 11.0},
 "colors": {"accent": "#00c2ff"}
}
```
### B. The core move in HyperFrames/GSAP (to build it without the kit or to customise it)
```js
window.onPlace = (t) => {                                   // runs every frame; boxAt from the track
  for (const c of CO) {                                     // leader lines from a point inside the tracked box
    const l = $$("l" + c.i), d = $$("d" + c.i), b = boxAt(c.obj, t);
    if (!b || t < c.t || t >= c.until) { l.setAttribute("d", ""); d.setAttribute("cx", -50); continue; }
    const p = [b[0] + (b[2] - b[0]) * c.fx, b[1] + (b[3] - b[1]) * c.fy];
    l.setAttribute("d", `M${p[0]},${p[1]} L${c.x - 40},${c.y} L${c.x},${c.y}`); d.setAttribute("cx", p[0]); d.setAttribute("cy", p[1]);
  }
  $$("rg1").setAttribute("transform", `rotate(${t * 220})`); $$("rg2").setAttribute("transform", `rotate(${-t * 140})`);
  const u = Math.max(0, Math.min(1, (t - CNT.t - .05) / CNT.dur));
  $$("kmh").textContent = String(Math.round(CNT.value * (1 - Math.pow(1 - u, 3))));   // cubic-out count
  const pts = []; for (let s = Math.max(TR.t, t - .9); s <= t; s += 1 / 24) { const b = boxAt("ball", s); if (b) pts.push([(b[0] + b[2]) / 2, (b[1] + b[3]) / 2]); }
  $$("tr").setAttribute("points", t >= TR.t && t < TR.until ? pts.map(p => p.join(",")).join(" ") : "");
};
stomp("#ms span", STAT.t, 2.2); stomp("#spd", CNT.t, 1.8); stomp("#goal span", BIG.t, 2.4); stomp("#lock", LOCK.t, 1.6);
```

## Adapting it to the user's project
- Content: one hero number per shot, and it must be true or clearly illustrative (contact time, speed, height, weight).
  Callouts name the product features that caused it.
- Language: English broadcast style is the default; Hebrew per the typography note.
- Brand: accent = brand colour; brand bug and lockup carry the name and tagline.
- Vertical 9:16: re-lay out (see Layout).
- Longer or shorter clips: one package per action; ~4 s per shot minimum so each stat is read.

## Sound
- Soft thump (0.5) on the stat, counter, big word and lockup; a UI pop (0.35) per callout; a UI whoosh (0.3) as the ring
  comes in; music `music_vol` 0.55; plate 0.4. `"sfx": false` mutes the cues.

## Pitfalls and QA checklist
- [ ] Every block's `t`/`until` matches the shot it belongs to (no callout pointing at a boot that's no longer on screen).
- [ ] Tracked objects exist in those shots (a leader line to a missing box is hidden, but the callout panel stays).
- [ ] Counter value and unit are consistent; the trail follows the object, not a jump across a cut (`trail.t` after the cut).
- [ ] GOAL behind the athlete only with a clean matte; frames checked + `scripts/qa.py` "ship".
