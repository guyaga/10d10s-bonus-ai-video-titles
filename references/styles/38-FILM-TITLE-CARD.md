# #38 FILM-TITLE-CARD · Cinema title cards

> Cinema title design in three pieces: a symmetric Wes Anderson chapter card, a Saul Bass cut-paper title that slams in on diagonal colour bars, and a two-column credits roll.
> Watch: https://ai-video-titles-guyaga.netlify.app/previews/film-title-card.mp4 · full sample: https://ai-video-titles-guyaga.netlify.app/full/AE_FILM-TITLE-CARD.mp4
> Runner: run_style FILM-TITLE-CARD · Example: examples/film-title-card

The sample is an EXAMPLE. The user supplies their own footage and content; this document is how to make this look on it.

## When to use it (and when not)
- Best for: brand films, short films, documentaries, chapter openers in long videos, trailers, "a film by" closers, event recap films, premium fashion or architecture pieces.
- Avoid when: a fast social ad (too slow and quiet); product specs (use KEYNOTE-REVEAL); a single continuous shot with no calm wide shot for the card.

## Anatomy (layers, back to front)
| Layer | What it is | Notes |
|---|---|---|
| Plate | the user's clip | `plate_vol` .45 |
| Anderson card | a centred frame (2 px border, 4 corner ornaments, a faint dark fill) holding kicker / title / sub | optional flat colour background (`bg`) instead of over-picture |
| Bass card | three flat shapes on a −8° diagonal (a big bar, a smaller bar, a thin vertical stripe) + the title on them + a sub label in a colour block | palette of 3 colours |
| Credits | two-column rows (role right-aligned, name left-aligned; mirrored in Hebrew) rolling up over a side scrim | gaps between groups with empty rows |

## Timing and motion
| Element | In at | In duration | Ease | Hold | Out | Out ease |
|---|---|---|---|---|---|---|
| Anderson card | `t` | .5 s fade | sine.inOut | still, no movement | .45 s fade ending at `until` | sine.inOut |
| Bass bar 1 | `t` | .32 s from x −1500 | expo.out | – | all pieces slide to x +2400 over .28 s, staggered .04 s, from `until` − .36 | expo.in |
| Bass bar 2 | `t` + .1 | .32 s from x −1500 | expo.out | – | (same) | – |
| Bass stripe | `t` + .22 | .25 s from y −300, opacity 0 | expo.out | – | (same) | – |
| Bass title | `t` + .26 | .12 s fade + .3 s from x −120 | expo.out | – | (same) | – |
| Bass sub | `t` + .45 | .2 s fade | default | – | (same) | – |
| Credits | `t` | .6 s fade in; the roll moves linearly from the bottom edge until fully off the top at `until` (default t + 8) | linear | – | – | – |
- The signature moves: **Anderson = stillness and symmetry** (only a fade, perfectly centred, letter-spaced caps). **Bass = hard diagonal slams** in a quick .1 s cascade, then a hard cut out the other side.
- Honest note: the Bass card is an homage (bars and a title), not a full cut-paper animation with shapes morphing into the title.

## Typography
- Latin: Anderson: Jost 500 title 120 px, tracking .14em, uppercase; kicker Jost 300 30 px tracking .5em; sub 32 px tracking .3em. Bass: Oswald 700 190 px; sub 34 px uppercase on a colour block. Credits: names in the display face, roles at .62 em, tracking .18em.
- Hebrew: default pair `suez`: **Suez One** titles (Anderson and Bass) and **Secular One** kickers, subs and roles. No letter-spacing on Hebrew (the kicker gets only .05em). Credits mirror (role on the right). Prices, if any, as ש״ח.
- Maximum copy: Anderson title about 16 characters at 120 px; Bass title about 9 characters at 190 px; credits rows about 30 characters each side.

## Colour and surface
- Roles: `ink` #f6e7c8 (warm cream text), `frame` #f6e7c8 (card border). Bass palette default ["#d7261e" red, "#111111" black, "#f3e6cf" cream]; the sub block takes the first colour.
- Credits scrim: a gradient from rgba(0,0,0,`scrim`) at the text side to transparent (default .6).
- Brand swap: the Bass palette is the brand's; the Anderson ink stays warm cream or pure white.

## Layout and safe zones (1920×1080 canvas)
- Anderson: centred horizontally, its centre at `y` (default 540; the sample puts it low, at 860, over a wide shot's floor).
- Bass: bars span the left two thirds on a −8° angle; the title block sits at 6% from the left (6% from the right in Hebrew) at `y` (default 520).
- Credits: the columns' centre at `x` (default 480); the scrim darkens that side.

## What the footage must give you
- Shoot it like this: planned cuts (max 6) · wide establishing shots with dust, sky or floor space; hero off-centre in the last shot · 25% free at the bottom.
- Tracking: none.
- Matte: not needed.
- Good: a wide calm shot for the chapter card, a strong graphic shot for the Bass title, a final hero shot with open space on one side for credits. Bad: busy close-ups everywhere.

## Build it
### A. With the kit
```bash
python scripts/run_style.py FILM-TITLE-CARD --spec my_spec.json --render
```
| Key | Meaning | Default |
|---|---|---|
| clip | the user's video | required |
| cards | list of cards (keys below) | cards and/or credits required |
| cards[].mode | "anderson" or "bass" | anderson |
| cards[].t, until | in / out | –, never |
| cards[].kicker, title, sub | text (kicker: Anderson only) | –, required, – |
| cards[].y | vertical centre | 540 (anderson) / 520 (bass) |
| cards[].bg | Anderson flat background colour | none (over picture) |
| cards[].palette | Bass colours [bar, bar 2, stripe] | ["#d7261e", "#111111", "#f3e6cf"] |
| credits | `{"t","until","x","lines":[[role,name],...],"scrim","size"}` | until t + 8, x 480, scrim .6, size 40 |
| language, pair | "he"/"en"; Hebrew pairing | "en"; "suez" |
| fonts | override faces | Jost 500 + Jost 300 (Bass: Oswald 700) |
| colors | `{"ink","frame"}` | #f6e7c8, #f6e7c8 |
| sfx | logo hit (.55) per Anderson card, stinger (.55) per Bass card | true |
| music, music_vol, plate_vol, name, track | optional | –, .6, .45, style id, – |
```json
{
 "name": "my-film", "clip": "clips/my_brand_film.mp4",
 "cards": [
  {"mode": "anderson", "t": 1.2, "until": 5.0, "kicker": "CHAPTER ONE", "title": "The Workshop", "sub": "where it all begins", "y": 820},
  {"mode": "bass", "t": 6.0, "until": 9.0, "title": "MAKERS", "sub": "a short film", "palette": ["#1e6cff", "#111111", "#f3e6cf"]}
 ],
 "credits": {"t": 12.0, "until": 18.0, "x": 520, "lines": [["DIRECTED BY", "DANA LEVI"], ["", ""], ["MUSIC", "NOVA"]]}
}
```
### B. The core move in HyperFrames/GSAP
```js
// Saul Bass: GSAP moves the .mv wrappers only; the -8deg rotation lives on the inner shapes (no transform fights)
tl.set(id, {opacity: 1}, c.t);
tl.fromTo(id + " .m1", {x: -1500}, {x: 0, duration: .32, ease: "expo.out"}, c.t);
tl.fromTo(id + " .m2", {x: -1500}, {x: 0, duration: .32, ease: "expo.out"}, c.t + .1);
tl.fromTo(id + " .m3", {opacity: 0, y: -300}, {opacity: 1, y: 0, duration: .25, ease: "expo.out"}, c.t + .22);
tl.fromTo(id + " .tt", {opacity: 0}, {opacity: 1, duration: .12}, c.t + .26);
tl.fromTo(id + " .m4", {x: -120}, {x: 0, duration: .3, ease: "expo.out"}, c.t + .26);
tl.to([id + " .m1", id + " .m2", id + " .m3", id + " .m4"], {x: 2400, duration: .28, ease: "expo.in", stagger: .04}, c.until - .36);
tl.set(id, {opacity: 0}, c.until);
// Anderson: fade only.  tl.fromTo(id, {opacity: 0}, {opacity: 1, duration: .5, ease: "sine.inOut"}, c.t)
// Credits: a pure function of t in onPlace:  top = 1080 - (1080 + H) * clamp01((t - CR.t) / (CR.until - CR.t))
```

## Adapting it to the user's project
- Content: a chapter card per section ("CHAPTER TWO · The Road"), one Bass title for the brand or film name, real credits at the end.
- Language: Hebrew → Suez One titles, Secular One kickers and roles; credits mirror.
- Brand: the Bass palette and the Anderson ink.
- Vertical 9:16: Anderson title down to about 80 px; Bass bars still diagonal, title about 130 px; credits single-column (put the role above the name).
- Longer clips: one card per chapter, never two cards on screen at once.

## Sound
- `logo_hit` at .55 on each Anderson card, `stinger` at .55 on each Bass card. Music at .6; let the credits ride the music.

## Pitfalls and QA checklist
- [ ] The Anderson card sits over a calm part of the shot (it has a light fill, not a solid panel).
- [ ] The Bass card's bars clear the frame completely on the way out (no stuck bar on the next shot).
- [ ] Credits finish rolling before the clip ends (`until` ≤ clip length).
- [ ] Hebrew titles have no letter-spacing; English Anderson titles do.
