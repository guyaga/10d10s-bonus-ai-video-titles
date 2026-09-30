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

## Try it in 5 minutes (no keys, no Seedance spend)

An 8-second runway clip, its tracking, music, product images and sounds are bundled in `examples/demo/`.

```bash
cd ~/.claude/skills/ai-video-titles/examples/demo
python ../../scripts/run_style.py STOMP-ESCORT --spec spec.json --render
# -> examples/demo/renders/demo-stomp-escort.mp4  (a few minutes: most of it is the headless-browser render)
```
Then change a name or a price in `spec.json` and render again. That is the whole loop: spec in, video out.

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
| `run_style.py` (parametrised JSON spec) | STOMP-ESCORT, COUNTDOWN-CTA, HUD-HELMET, SCIFI-TARGETING, MAP-FLYOVER, CAMPUS-AR, SPEED-STAT, VIRAL-CAPTIONS, DECODE-TYPE, GLITCH-RGB, NEON-SIGN, KEYNOTE-REVEAL, SPLIT-FLAP, SIGNATURE-WRITE-ON, BROADCAST-PACK, FILM-TITLE-CARD, PARTICLE-TEXT, FLIP-MONTAGE-LOGO, TEXT-ON-PATH | `python scripts/run_style.py HUD-HELMET --spec spec.json [--render]` |
| `run_ad.py` (adkit elements) | STOMP-BEHIND, GLASS-CALLOUT, KINETIC-HE, TAPE-HE, KINETIC-KARAOKE, FLASH-CARD, PRESIDENTIAL-SERIF | `python scripts/run_ad.py AD --spec spec.py [--render]` |
| bespoke (run_ad + html/css/js hooks) | ROAD-HUD, THERMAL-RESCUE, SPEC-SCAN, HALLMARK-LUXE, ARCH-DRAWING, MAGAZINE-EDITORIAL, KITCHEN-TICKET, LENS-POSTCARD | start from `references/recipes/bespoke/` |

Every `run_style` style has a working spec in `examples/<style>/` (plus the `objects.json` to track with).

## Your own video, by hand

From a project folder (layout and overrides in `scripts/paths.py`):
```bash
S=~/.claude/skills/ai-video-titles/scripts
python $S/vtrack.py clips/AD_720p.mp4 tracks/AD_objects.json tracks/AD_vtrack.json --preview tracks/check.mp4
python $S/run_style.py STOMP-ESCORT --spec specs/AD.json --render     # or run_ad.py for adkit / bespoke specs
python $S/qa.py renders/AD.mp4 "what it should show"
```
Inside Claude Code just ask: *"Make a 15 s Seedance 2.5 sneaker ad and add titles in KINETIC-HE with a Hebrew
voiceover."* The skill picks the style with you, generates a clean plate, tracks it, builds, renders and QA-checks it.

Brands in the examples (Atelier Veyra, Firelink, Seaview 24) are fictional demo brands.
