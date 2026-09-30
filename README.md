# ai-video-titles

**Style hub (live):** https://ai-video-titles-guyaga.netlify.app

After-Effects-style titles, HUDs and motion graphics on top of AI-generated video (Seedance 2.5 recommended), built as
code: frame-by-frame tracking, beat and voice sync, HyperFrames render, Gemini QA. 41 styles, each with a live
preview on the hub, a style ID and a one-line prompt to paste into Claude Code.


## The catalog (61 styles, a database)

Ask Claude for titles and it starts with **"Do you want to see the catalog?"** Pick a card by number or ID on the
hub, and Claude writes the build brief from that style plus your project (brand, language, words, prices, music).

```bash
python scripts/catalog.py list --tag hebrew          # search by use case, or --q news
python scripts/catalog.py show 43                    # one style: look, fonts, samples, how to shoot it, how to build it
python scripts/catalog.py brief 43 "your project"    # style + context → the build brief
python scripts/catalog.py make 43 my_clip.mp4 "your project"   # start a project on your footage (see below)
```
`references/catalog.json` is the same data as the hub: https://ai-video-titles-guyaga.netlify.app

## Install

Paste this into Claude Code:

> Install the ai-video-titles skill from https://github.com/guyaga/10d10s-bonus-ai-video-titles by cloning it to
> ~/.claude/skills/ai-video-titles, running pip install -r requirements.txt in that folder, then run
> python scripts/doctor.py and tell me which pipeline steps are available to me. Finally render the included demo with
> cd examples/demo && python ../../scripts/run_style.py STOMP-ESCORT --spec spec.json --render and show me the result.

Or by hand:
```bash
git clone https://github.com/guyaga/10d10s-bonus-ai-video-titles ~/.claude/skills/ai-video-titles
cd ~/.claude/skills/ai-video-titles
pip install -r requirements.txt
python scripts/doctor.py
```
Needs Python 3.10+, ffmpeg on PATH and Node 18+ (HyperFrames runs through npx, pinned to `hyperframes@0.8.84`).
`doctor.py` checks all of it, plus the keys and the sibling skills, and lists which steps you can run.

| Key | Needed for |
|---|---|
| `GEMINI_API_KEY` | tracking objects in your own clips, AI voiceover, QA of a render |
| `ELEVEN_API_KEY` (or `ELEVENLABS_API_KEY`) | music beds and new sound effects (a UI/impact sound library ships with the kit) |

## What this skill does and doesn't do

Post only: a clip goes in, a titled video comes out. Each style has a **plate contract** in `references/plates.json`
(take, framing, free space for the titles, matte, what must be trackable, and Seedance lines that enforce it), shown on
every hub card as "Shoot it like this". To generate the video and title it end to end, use **ai-ad-studio**, which
plans the Seedance shoot backwards from that contract.

## Try any style in 5 minutes (no keys, no footage)

An 8-second runway clip, its tracking, music, product stills and sounds are bundled in `examples/demo/`. Any of the
41 `run_style` styles previews on it:
```bash
cd ~/.claude/skills/ai-video-titles
python scripts/run_style.py BREAKING-NEWS --demo --render     # → titles-demo/renders/demo-breaking-news.mp4
```
`--demo` loops the clip to the style's own length, derives every tracked object the style rides from the demo's
tracked model (face, feet, torso …) or pins it to a fixed anchor, and swaps in the bundled music. It shows the
style's motion on neutral footage with the example's placeholder words: good for choosing a style, not the final look.

## Hebrew

Hebrew titles use Suez One (premium), Karantina (social stomp) and Secular One (captions, UI), bundled and paired
(`"pair": "suez" | "karantina" | "secular" | "karantina-suez"`). RTL motion, mirrored wipes and number gluing are
built in. Details: *Hebrew typography* in SKILL.md.

## Pick a style

Browse the hub (https://ai-video-titles-guyaga.netlify.app), filter by use case, press **Copy** on a style and paste
the line into Claude Code. The same page runs locally:
`npx http-server ~/.claude/skills/ai-video-titles/catalog -p 8790`. Full specs per style: `references/styles.md`.

## How the styles run

| Route | Styles | Command |
|---|---|---|
| `run_style.py` (parametrised JSON spec, 41 styles) | STOMP-ESCORT, COUNTDOWN-CTA, HUD-HELMET, SCIFI-TARGETING, MAP-FLYOVER, CAMPUS-AR, SPEED-STAT, VIRAL-CAPTIONS, DECODE-TYPE, GLITCH-RGB, NEON-SIGN, KEYNOTE-REVEAL, SPLIT-FLAP, SIGNATURE-WRITE-ON, BROADCAST-PACK, FILM-TITLE-CARD, PARTICLE-TEXT, FLIP-MONTAGE-LOGO, TEXT-ON-PATH, LOWER-THIRD-CORP, BREAKING-NEWS, LEADER-CALLOUTS, DATA-CHARTS, KPI-COUNTERS, APP-UI-POPUPS, CHAT-BUBBLES, SOCIAL-CTA, END-SCREEN, PODCAST-TAGS, CHAPTER-MARKERS, QUOTE-TESTIMONIAL, DOC-LOCATION-STAMP, SWISS-GRID, GRADIENT-GLASS, BEFORE-AFTER-SPLIT, LOGO-SHINE-REVEAL, LYRIC-KINETIC-3D, TIMELINE-HISTORY, LISTING-SPECS | `python scripts/run_style.py <ID> --spec spec.json [--render]` |
| `run_ad.py` (adkit elements) | STOMP-BEHIND, GLASS-CALLOUT, KINETIC-HE, TAPE-HE, KINETIC-KARAOKE, FLASH-CARD, PRESIDENTIAL-SERIF, STOMP-SX, TRACKED-TAGS, COMIC-POP | `python scripts/run_ad.py AD --spec spec.py [--render]` |
| bespoke (run_ad + html/css/js hooks) | ROAD-HUD, THERMAL-RESCUE, SPEC-SCAN, HALLMARK-LUXE, ARCH-DRAWING, MAGAZINE-EDITORIAL, KITCHEN-TICKET, LENS-POSTCARD | start from `references/recipes/bespoke/` |

Every `run_style` style has a spec in `examples/<style>/` showing every key (the builder documents them at the top of
`scripts/styles/<module>.py`). Those specs point at the plates the hub samples were made on, which are not shipped:
your footage goes in through `catalog.py make` below. `catalog.py show <n>` prints a style's **tier**:
- **one-command**: needs only your clip and your words
- **track-first**: the titles ride objects in the frame, so they get tracked first (vtrack.py, GEMINI_API_KEY)
- **bespoke-rewrite**: a crafted world; the recipe is the reference and Claude rewrites it for your subject

## Planning a shoot (no footage yet)

```bash
python scripts/check_clip.py plan 43 "rolling news package for a city marathon, Hebrew"
```
Prints what the footage must contain for that style (one take or cuts, framing, free space for the titles, what must
be trackable) and ready-to-paste lines for a Seedance / Kling / Veo prompt or a shot list, plus the objects to track
afterwards. To generate the footage and title it end to end, use the **ai-ad-studio** skill.

## Use it on your own footage

```bash
S=~/.claude/skills/ai-video-titles/scripts
python $S/catalog.py make 43 ~/Videos/marathon.mp4 "rolling news for the Tel Aviv marathon, Hebrew, brand red #d6001c"
```
`make` creates `breaking-news-project/` with your clip in `clips/`, a starter `spec.json` (the style's example with
your clip swapped in, your context saved in `_context`, every content field listed in `_todo`), an `objects.json`
when the style rides tracked objects, then runs the clip check and prints the verdict and the next commands:

1. **Check**: `check_clip.py check` measures cuts, tracking coverage, title space and edge crop (plus a Gemini
   second look when `GEMINI_API_KEY` is set). FAIL → trim or reframe as printed, or pick a style it lists as fitting.
2. **Track** (track-first styles): describe each object in `objects.json` as it looks in *your* clip, then
   `python $S/vtrack.py clips/marathon.mp4 objects.json tracks/track.json --preview tracks/check.mp4` and watch the preview.
   (`make ... --track` does this for you once the descriptions are filled in.)
3. **Edit** `spec.json`: your words, names, prices, language (`"language": "he"` + a Hebrew `pair`), brand colours,
   the music bed and its beat grid. Keys you don't need can go; missing music, voice or matte only warn.
4. **Build**: `python $S/run_style.py BREAKING-NEWS --spec breaking-news-project/spec.json --root breaking-news-project`
   (a missing input stops with the exact fix).
5. **Render**: the same command with `--render` → `breaking-news-project/renders/`.
6. **Review**: `python $S/qa.py breaking-news-project/renders/breaking-news.mp4 --root breaking-news-project`, and look
   at 4–6 frames yourself.

Inside Claude Code just ask for titles: the skill offers the catalog, asks whether you have footage, and runs
these steps with you.

## Testing

`python scripts/selftest.py` builds every `run_style` style on the bundled footage (`--demo`, with hyperframes'
lint / runtime / layout / motion checks), runs the clip checker's planning stage for all 61 styles and its post stage
on the demo clip. Results of the last clean-install run are in `TESTING.md`.

Brands in the examples (Atelier Veyra, Firelink, Seaview 24) are fictional demo brands.
