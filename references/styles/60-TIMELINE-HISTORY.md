# #60 TIMELINE-HISTORY · Documentary history timeline

> A ruled timeline with minor ticks draws across the lower third, a glowing playhead eases from node to node, each year node pops as it arrives, a big year counts like an odometer to the node's date and a caption rises above the node. The footage starts in an archival sepia grade and warms into full colour as the timeline reaches the present.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/timeline-history.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/N20_TIMELINE-HISTORY.mp4
> Runner: run_style TIMELINE-HISTORY · Example: examples/timeline-history/

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: documentaries, heritage and city films, company histories ("since 1952"), museum pieces, anniversary videos, product evolution (v1 → today).
- Avoid when: there are more than 6 events in 10 s, the dates are not chronological, or the footage has no calm lower third.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| `#arch` | archival grade as a backdrop filter: sepia .85, contrast 1.08, brightness .92, saturate .8 | fades out between the 2nd-to-last and last event |
| `#vig` | warm vignette (rgba(20,12,4,.55) at the edges) | fades to 30% with the grade |
| `#band` | dark gradient band from 520 px above the rule to the bottom | readability for the lower third |
| `#rule` / `#ticks` | 2 px rule at `y` (850) + minor ticks every 38 px | draw from the start side |
| `.nd` | node: 18 px dot (accent ring, fills when reached), year label (36 px), stem, caption above (30 px, 340 px wide) | spaced evenly between margins |
| `#ph` | playhead: 32 px white ring with glow | eases node to node |
| `#big` | the big year (210 px display, tabular) + the current event label under an accent rule | odometer count between dates |

## Timing and motion
Each event has a time `t`; the playhead arrives exactly at `t`.
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| band (fade) | 0 | .80 | — | whole clip | — | — |
| rule (scaleX 0→1) | .15 | 1.10 | power3.inOut | — | — | — |
| ticks (scaleX 0→1) | .25 | 1.30 | power3.inOut | — | — | — |
| big year block (fade, y 20→0) | first t−.2 | .70 | power3.out | — | — | — |
| playhead appear / travel to node i | first t−.4 / t_i−.9 | .40 / .90 | power2.inOut | — | — | — |
| node dot (scale 0→1, fills) | t_i | .45 | back.out(3) | — | — | — |
| node year (fade, y −8→0) | t_i+.05 | .40 | power3.out | — | — | — |
| stem (scaleY 0→1) | t_i+.1 | .30 | power2.out | — | — | — |
| caption (fade, y 16→0) | t_i+.15 | .50 | power3.out | until next | fade + y −10 at next t−.5, .4 s | power2.in |
| big year odometer | t_i−.9 → t_i | .90 | quad in-out | — | — | — |
| sepia → colour | t(N−2) → t(N−1) | linear | — | — | — | — |
- Event spacing in the sample: 1.8 s (1.2, 3.0, 4.8, 6.6, 8.4).
- The signature move: the odometer year rolling while the playhead travels, and the archival grade warming into colour at "today".

## Typography
- Latin: DM Serif Display 400 years (36 px nodes, 210 px big), Manrope 500 captions (30 px) and the big label (30 px, +.2em).
- Hebrew: `pair: "suez"` (default) = Suez One years, Secular One captions. The timeline runs right-to-left (earliest on the right), rule and ticks draw from the right, the big year sits on the reading-start side (right) unless `big.side: "end"`.
- Suez One's digits are old-style (they sit low): for a big "1948" that must look full-height, use a Latin display for the numerals (e.g. `fonts: {"display": "DM Serif Display"}`) while captions stay in Secular One.
- Maximum copy: caption ≈ 26 characters (2 lines in 340 px), 3–6 events.

## Colour and surface
- `colors.accent` #f2c46d (node rings/fills, stems, big-year rule), `colors.line` rgba(255,255,255,.78).
- `archival: false` to keep the footage in colour throughout (e.g. modern company timelines).

## Layout and safe zones (1920×1080 canvas)
- Rule at `y` (850) between `margin` (170) on each side; nodes evenly spaced. Captions sit above the nodes (≤ 120 px); the big year at `big.y` (430) on its side.
- Industry convention: time runs in the reading direction (left→right in LTR, right→left in RTL); "today" is the last node and the one in full colour.
- 9:16: 3–4 events, margin ≈ 90, rule y ≈ 1500 on a vertical canvas.

## What the footage must give you
- Shoot it like this: one take, 6–30 s, a calm establishing shot of the place/company, the lower third quiet; slow steady move.
- Tracking: none. Matte: not needed.
- Good footage: aerials of old towns, a factory exterior, a museum hall, a product on a plinth. Bad: busy lower third, cuts (the sepia→colour story needs one continuous shot).

## Build it
### A. With the kit
```bash
python scripts/run_style.py TIMELINE-HISTORY --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | video | required |
| events[] | {year, text, t} in chronological order (≥ 2) | required |
| archival | sepia grade that warms into colour | true |
| y / margin | rule y px / side margin px | 850 / 170 |
| big | {side "start"/"end", y} | start, 430 |
| language / pair | he/en; Hebrew pair | en / "suez" |
| fonts | override | DM Serif Display 400 / Manrope 500 |
| colors | {accent, line} | #f2c46d, rgba(255,255,255,.78) |
| sfx | whoosh, tick per node, chime at the last | true |
| plate_vol, music, music_vol, name | — | .8, none, .5 |
```json
{
 "clip": "clips/factory.mp4",
 "events": [{"year": 1952, "text": "The first workshop opens", "t": 1.2}, {"year": 1978, "text": "Our first export", "t": 3.2},
            {"year": 2004, "text": "The new plant in Haifa", "t": 5.2}, {"year": 2026, "text": "Today · 40 countries", "t": 7.2}],
 "archival": true, "big": {"side": "start", "y": 420}
}
```
### B. The core move in HyperFrames/GSAP
```js
const tl = gsap.timeline({paused: true}); window.__timelines = {main: tl};
const E = [{y: 1952, t: 1.2, x: 170}, {y: 1978, t: 3.2, x: 697}, {y: 2004, t: 5.2, x: 1223}, {y: 2026, t: 7.2, x: 1750}];
tl.fromTo("#rule", {scaleX: 0}, {scaleX: 1, duration: 1.1, ease: "power3.inOut"}, .15);
E.forEach((ev, i) => {
  if (i > 0) tl.to("#ph", {x: ev.x, duration: .9, ease: "power2.inOut"}, ev.t - .9);
  else tl.fromTo("#ph", {x: ev.x, opacity: 0}, {x: ev.x, opacity: 1, duration: .4}, ev.t - .4);
  tl.fromTo(`#n${i} .dot`, {scale: 0}, {scale: 1, duration: .45, ease: "back.out(3)"}, ev.t);
  tl.fromTo(`#n${i} .cp`, {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, ev.t + .15);
});
window.onPlace = (t) => {                 // odometer + grade from time (seek-safe)
  let yv = E[0].y;
  for (let i = 0; i < E.length; i++) { if (t >= E[i].t) yv = E[i].y; else if (i && t >= E[i].t - .9) {
    const u = (t - (E[i].t - .9)) / .9, w = u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; yv = Math.round(E[i - 1].y + (E[i].y - E[i - 1].y) * w); break; } else break; }
  document.getElementById("bigy").textContent = yv;
  const u = Math.max(0, Math.min(1, (t - E[2].t) / (E[3].t - E[2].t)));
  document.getElementById("arch").style.opacity = 1 - u;                 // sepia → colour at "today"
};
```

## Adapting it to the user's project
- Content: 3–6 real dated milestones; the last one = today.
- Language: Hebrew → `"language": "he"`; runs right-to-left.
- Brand: accent = brand colour; `archival: false` for modern brands.
- Vertical 9:16: see layout.
- Longer clips: space events ~2–4 s apart.

## Sound
- `ui_whoosh` (.22) as the rule draws, `soft_tick` (.4) at each node, `chime` (.25) at the last.

## Pitfalls and QA checklist
- [ ] Events in chronological order; captions fit 2 lines.
- [ ] Hebrew: earliest on the right, rule draws from the right.
- [ ] Big year readable (full-height digits if Suez One looks too low).
- [ ] The grade warms exactly as the playhead reaches "today".
- [ ] The lower third of the footage stays calm behind the band.
