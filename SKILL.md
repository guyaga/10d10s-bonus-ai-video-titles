---
name: ai-video-titles
description: After-Effects-style titles, HUD and motion graphics ON TOP of AI-generated video (Seedance 2.5 recommended) - stomp/social titles that ride a tracked subject, text behind the subject, Iron-Man-style HUDs, broadcast stat counters, Hebrew kinetic and tape titles, karaoke captions, flash-sale countdown CTAs, and fully bespoke crafted worlds (thermal camera, jeweller's loupe, architect's drawing, magazine spread, kitchen ticket). Frame-by-frame tracking (Gemini + optical flow), beat/voice sync, SFX + music + AI voice, HyperFrames render, Gemini QA. Ships with a visual style catalog of 29 styles, each with an ID, a copy-paste prompt and a plate contract (references/plates.json: how the video must be shot for that style). Post only: a clip goes in; to generate the video too, use ai-ad-studio. Use when the user wants titles, callouts, HUD, lower-thirds, captions, kinetic typography, motion graphics or "AE-style" text over an AI video / Seedance clip, a shoppable or product-callout video, a Hebrew social ad with big titles, or asks which title style to use.
---

# AI Video Titles

Code-driven motion graphics over AI footage. The video is generated **clean**; every title, HUD and callout is HTML
(HyperFrames) placed from frame-by-frame tracking, timed to the beat and the voice, then rendered to MP4.

```
SKILL=~/.claude/skills/ai-video-titles
catalog      https://ai-video-titles-guyaga.netlify.app   (hosted: send this link when the user picks a style)
             $SKILL/catalog/index.html        the same page locally (serve it, e.g. npx http-server)
style specs  $SKILL/references/styles.md      what each style is, fonts, palette, motion, how to build it
kit          $SKILL/scripts/                  run_style (7 parametrised styles), run_ad (adkit + bespoke specs), vtrack, track,
                                              finalize, qa, music, vo_take2, word_times, doctor
examples     $SKILL/examples/                 one spec per run_style style + 3 adkit/bespoke specs + demo/ (8 s, no keys needed)
recipes      $SKILL/references/recipes/       the original hand-built compositions (reference source for bespoke work)
doctor       python $SKILL/scripts/doctor.py  checks deps/keys/sibling skills, prints which steps are available
```

Everything runs from a **project folder** (cwd, or `--root DIR`, or env `TITLES_ROOT`). Layout is in `scripts/paths.py`:
`clips/ tracks/ mattes/ specs/ shared/sfx/ voice/ videos/ renders/`.

Keys: `GEMINI_API_KEY` (tracking, TTS, QA), `ELEVEN_API_KEY` (music + new SFX; a sound library ships with the kit).
No video-generation key: generation belongs to ai-ad-studio. Tools: Python 3.10+ (`pip install -r requirements.txt`), ffmpeg, Node 18+ (npx hyperframes).
First run on a new machine: `python $SKILL/scripts/doctor.py`. To show the user a result in minutes with no keys and
no Seedance spend: `cd $SKILL/examples/demo && python ../../scripts/run_style.py STOMP-ESCORT --spec spec.json --render`.

---

## Boundaries

- **Post only.** A clip goes in, a titled video comes out. This skill owns the style knowledge (the catalog, the
  builders, and each style's plate contract in `references/plates.json`). It does not generate video.
- **To generate video and title it end to end, use ai-ad-studio.** It picks the style, reads `references/plates.json`
  to plan the shoot backwards from it (take, framing, free space, matte, tracking, Seedance lines), generates through
  seedance-2-prompt-engineer + seedance-make-video, gates the plate, then calls this skill for the titles.
- A plate that breaks its style's contract (a cut in a one-take style, no room for the titles, text in frame) is sent
  back for regeneration, not fixed in post.

## STEP 0 - Pick the style with the user (always first)

1. Open or describe the catalog. Ask with **AskUserQuestion**: 2-4 style IDs that fit the subject, the first marked
   "(Recommended)", each with its one-line description. Users can also paste a catalog prompt line
   (`Titles: STOMP-ESCORT - ...`). If a clip already exists, only offer styles whose plate contract it can meet.
   Map subject -> family:
   - fashion / drops / e-commerce -> STOMP-ESCORT, STOMP-BEHIND, GLASS-CALLOUT, COUNTDOWN-CTA
   - Hebrew social ad -> KINETIC-HE, TAPE-HE, KINETIC-KARAOKE, FLASH-CARD
   - sport / measurable action -> SPEED-STAT; epic brand film -> PRESIDENTIAL-SERIF
   - sci-fi / tech / AI assistant -> HUD-HELMET, SCIFI-TARGETING; automotive -> ROAD-HUD; emergency -> THERMAL-RESCUE
   - product engineering -> SPEC-SCAN; luxury -> HALLMARK-LUXE; real estate -> ARCH-DRAWING, MAP-FLYOVER
   - interiors -> MAGAZINE-EDITORIAL; food -> KITCHEN-TICKET; travel / wearables -> LENS-POSTCARD; venues -> CAMPUS-AR
2. **Decide the piece's own visual language.** The catalog is a starting point, not a house style. The lesson that
   cost a full rebuild: running eight different ads through one kit made them all look the same. For every piece ask
   "what does this subject's world print, measure, stamp or display?" (a kitchen prints tickets, a jeweller uses a
   loupe, an architect draws on vellum) and build that. One accent colour. Few, big, meaningful titles.
3. Decide **the ending first** (the last title / CTA) and the **device** (the one structural idea). For multi-ad
   batches write an `EDIT-DOCTRINE.md` with the edit-director skill (example in `references/recipes/`).

## STEP 1 - Check the plate against the style's contract

The clip comes in from outside (the user, or ai-ad-studio). Read the chosen style's entry in
`references/plates.json` and check the clip before any post work:
- **Cuts**: `ffmpeg -i clip.mp4 -vf "select='gt(scene,0.15)',showinfo" -an -f null -` and count `pts_time` hits
  against `gate.max_cuts`. For one-take styles also ask Gemini "is this one unbroken take?" (match cuts score low).
- **Duration / aspect**: inside `duration_s`; the kit renders 1920x1080, so a 9:16 clip needs reframing first.
- **Tracking + space**: after STEP 2, the first `track` object must be found on at least `gate.min_track_coverage`
  of frames, with at least `gate.min_free_margin` of the frame free on the `negative_space` side.
- **Clean frame**: no readable text, logos or UI in the plate (`text_in_frame` is always false).
- **Matte**: if `separation` is true, the subject must cut out cleanly (STEP 2 matte).
If the clip fails, say which rule and how much, and recommend regenerating with the contract's `seedance_lines`
through ai-ad-studio. Do not paper over a failed plate with titles.

## STEP 2 - Analyse the plate frame by frame

```bash
cd <project>
# 1. object tracking: Gemini boxes at 8 keyframes/s + LK optical flow between them + drift correction + Savitzky-Golay
python $SKILL/scripts/vtrack.py clips/AD_720p.mp4 tracks/AD_objects.json tracks/AD_vtrack.json --kfps 8 --preview tracks/AD_check.mp4
#    objects.json: {"context": "one line about the shot", "objects": [{"name": "shoe", "desc": "the white running shoe"}, ...]}
#    ALWAYS watch the --preview: boxes must sit on the objects before you design anything.
# 2. planar scenes (maps, facades, floors): chained RANSAC homographies from anchor points
python $SKILL/scripts/track.py clips/AD_720p.mp4 anchors.json tracks/AD_points.json --preview tracks/AD_pts.mp4
# 3. text-behind-subject matte (webm with alpha)
npx hyperframes@0.8.84 remove-background clips/AD_720p.mp4 -o mattes/AD_alpha.webm
# 4. beats / hits: librosa beat_track + onset_detect on the music bed; put title entrances ON beats
```
Also look at a contact sheet (ffmpeg `fps=2,tile`) and note the timecode of every moment a title must land.

## STEP 3 - Build the titles

Three routes, by style (references/styles.md says which one each style uses):

**A. Parametrised styles - `run_style.py`** (STOMP-ESCORT, COUNTDOWN-CTA, HUD-HELMET, SCIFI-TARGETING, MAP-FLYOVER,
CAMPUS-AR, SPEED-STAT). Copy `examples/<style>/spec.json`, edit texts / items / prices / times / colours, point `clip`
and `track` at your files, then:
```bash
python $SKILL/scripts/run_style.py STOMP-ESCORT --spec specs/runway.json            # build + hyperframes check
python $SKILL/scripts/run_style.py STOMP-ESCORT --spec specs/runway.json --render   # -> renders/<name>.mp4
```
Each builder documents every key at the top of `scripts/styles/<module>.py`. Relative paths in a spec resolve against
the spec's folder, then the project root. The kit's UI/impact sounds are bundled, so these styles need no ElevenLabs key.

**B. adkit styles - `run_ad.py`** (STOMP-BEHIND, GLASS-CALLOUT, KINETIC-HE, TAPE-HE, KINETIC-KARAOKE, FLASH-CARD,
PRESIDENTIAL-SERIF). Write `specs/AD.py` exposing `SPEC` (below), then `python $SKILL/scripts/run_ad.py AD [--spec file.py]`.

**C. Crafted worlds - bespoke** (ROAD-HUD, THERMAL-RESCUE, SPEC-SCAN, HALLMARK-LUXE, ARCH-DRAWING, MAGAZINE-EDITORIAL,
KITCHEN-TICKET, LENS-POSTCARD). A run_ad spec whose look lives entirely in the hooks (`html_front`, `css`, `js`, `fonts`,
`assets`); start from `references/recipes/bespoke/<AD>_bespoke.py` and rewrite it for the new subject - these are
tailor-made by definition, never a template with the text swapped.

```python
SPEC = {"theme": "he_bold",            # he_bold | he_premium | sparta | guyaga | tech | tactical | luxe | chef | travel
        "palette": {"acc": "#E63B2E", "ink": "#111111", "lt": "#F5F3EE", "panel": "rgba(17,17,17,.82)", "sub": "#f3c6c1"},
        "music_vol": .5, "plate_vol": .4,  # music = shared/sfx/AD_music.mp3, VO = shared/sfx/AD_vo.mp3 (both optional)
        "watermark": None,                 # optional path to a small PNG, bottom-centre
        "elements": [
          {"type": "kine", "x": 960, "y": 300, "t": 4.3, "end": 8.9, "exit": "up",
           "lines": [[{"w": "לתוך", "t": 4.3, "size": 180}, {"w": "האש", "t": 4.86, "size": 300, "font": "big", "style": "accent", "hit": True}]]},
          {"type": "tape", "x": 960, "y": 760, "align": "c", "t": 4.95, "end": 8.9,
           "lines": [{"text": "אפס ראות", "style": "ink", "size": 62}, {"text": "640 מעלות", "style": "acc", "size": 74, "hit": True}]},
          {"type": "counter", "t0": 4.2, "t1": 17.2, "a": 100, "b": 7, "suf": "%", "label": "חמצן במיכל", "x": 90, "y": 690, "t": .5},
          {"type": "tag", "title": "חתימת חום", "sub": "אדם 1", "follow": "door", "anchor": "c", "dx": -170, "t": 10.25, "end": 12.2},
        ]}
```
Elements: `stomp` `kine` `tape` `flash` `punch` `captions` `tag` `box` `callout` `counter` `ring` `chip` `lockup` `meter`
(field list at the top of `scripts/adkit.py`; each catalog entry names the ones it uses). Anything the kit does not do
goes through the bespoke hooks: `html_front`, `html_behind` (between plate and matte), `css`, `js` (GSAP on `tl`,
per-frame `window.onPlace(t)`, helpers `boxAt(name,t)` / `anchor(b,a)`), `fonts`, `assets`. Crafted-world styles are
100% hooks - start from the matching file in `references/recipes/bespoke/` or `examples/E8_tower_bespoke.py`.

Tracking in markup: `data-follow="obj" data-anchor="c|t|b|l|r|tl|tr|bl|br" data-dx data-dy` pins an element to a
box anchor every frame; `data-box="obj" data-pad` sizes it to the box. Put `<!--MATTE-->` in raw HUD to split
behind/front around the matte. Everything must be seek-safe: drive motion from `t`, never from wall-clock time.

**Typography.** Hebrew: Assistant 300-800 for UI and sub-lines, Rubik 900 and Karantina 700 for big social words,
Frank Ruhl Libre for editorial/luxury, Heebo for calm tech; write gershayim/geresh with the real characters (״ ׳).
Latin pairings in the kit (`FAM` in adkit.py): Anton + Bodoni Moda, DM Serif Display + Space Grotesk, Michroma +
Sora, Barlow Condensed, Cormorant Garamond + Manrope, Fraunces. Fonts ship in `assets/fonts` (override `TITLES_FONTS`).
**Readability over footage** (thin text over video failed every time): tape strips, a bottom scrim, glass panels
with a blur, or a hard 1-2 px outline; accent-coloured text only on ink/strip backgrounds (`tacc` auto-contrast).

## STEP 4 - Sound

- Music bed: `python $SKILL/scripts/music.py AD 18 "<genre, instruments, mood; hits at the title timestamps>"` (ElevenLabs
  Music, instrumental, retries on 429). Write the hits you need at the times your titles land.
- VO: lines JSON `{"voice": "Charon|Sulafat|<designed alias>", "lines": [{"id", "start", "text", "style"}], "total"}` ->
  `python $SKILL/scripts/vo_take2.py AD lines.json he` (gemini-tts skill; designed voices via its `design` command;
  one voice per character, e.g. a Hebrew AI woman for a suit assistant). It prints overlaps - fix the starts, not the text.
- Word timing for karaoke / voice-synced kine: `python $SKILL/scripts/word_times.py AD lines.json he` ->
  `tracks/AD_he_words.json`, feed it to a `captions` element or copy the times into `kine` words.
- SFX: generated + cached per name (ElevenLabs sound-generation) - a soft sub thump is added under every stomp/hit
  (`"thumps": False` to disable). Keep it clean: early noisy trailer music was rejected; prefer elegant beds + soft hits.

## STEP 5 - Render, QA, fix

```bash
python $SKILL/scripts/run_ad.py AD --render [--sting end_logo.mp4]     # 24 fps, loudnorm -16 LUFS -> renders/AD.mp4
python $SKILL/scripts/qa.py renders/AD.mp4 "<what it should show, in order>"   # {"verdict": "ship"|"fix", "issues": [...]}
```
Fix every issue, re-render, repeat until `ship`. Then watch it yourself at phone size. Optional outside eye:
`scripts/creative.py` asks Gemini for an alternative title/narration take.

### Gotchas (each one cost a render)
- `hyperframes check` contrast failures: accent text on dark plates -> put it on a strip/panel or let `tacc` pick.
- Zero-size SVG canvases are not painted -> give the SVG a real size and a centred viewBox.
- Tracked panels collapse to 0x0 -> `[data-follow].panel{width:max-content;height:auto}`.
- Tweening `letterSpacing` snaps between frames -> animate `scale` instead.
- Hebrew: `direction:rtl` on the container, keep digits glued to the next word in captions ("6 שעות"),
  flash cards auto-pick RTL/LTR by script (a Latin word in an RTL box renders "!AERO").
- Captions linger -> each group holds at most 1 s after its last word.
- Outline-only words fail "text_not_painted" -> translucent dark fill + stroke.
- Kinetic words collide -> `.kw{margin:0 .11em}`.
- `hyperframes init` refuses a non-empty folder -> init first, copy assets after (shotkit does this).
- npm ETARGET on a new HyperFrames version -> keep the pin `hyperframes@0.8.84` (paths.HF).
- Windows consoles choke on Hebrew/check symbols -> `PYTHONIOENCODING=utf-8` (run_ad reconfigures stdout).
- Generated takes sometimes cut mid-shot: regenerate the plate before designing, tracking cannot bridge a cut.

## Deliver
Send the render (and `renders/preview/*_preview.mp4` under 29 MB for chat apps). For a batch, a contact sheet or a
simple gallery page. Name styles by catalog ID so the user can ask for "the same in TAPE-HE".
