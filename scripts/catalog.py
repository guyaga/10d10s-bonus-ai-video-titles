"""The style catalog as a database: every hub style with its number, look, use cases, fonts, samples, plate contract
and how to build it. The hub (catalog/index.html) is the visual face; references/catalog.json is the same data for
Claude.

    python catalog.py build                          # regenerate references/catalog.json from the hub + plates.json
    python catalog.py list [--tag hebrew] [--q news] # search: id / number / one-liner / tags / fonts
    python catalog.py show 43 | BREAKING-NEWS        # one style card, including samples and the shooting requirements
    python catalog.py brief 43 "context..."          # the build brief: style + the user's project context + commands
    python catalog.py make 43 my_clip.mp4 "context" [--out DIR] [--track] [--no-gemini]
                                                     # start a project on YOUR footage: starter spec, objects.json,
                                                     # tracking, the clip check, then the exact build commands

Tiers (catalog.json "tier"):
  one-command      the style needs only your clip (+ your words): make → edit spec → build
  track-first      the titles ride objects in the frame: make → describe the objects → vtrack.py → build
  bespoke-rewrite  a crafted world: the recipe is the reference; Claude rewrites it for your subject

Numbers are stable (#01..#61...): never renumbered, new styles are appended.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SKILL = Path(__file__).resolve().parent.parent
HUB = "https://ai-video-titles-guyaga.netlify.app"
DB = SKILL / "references" / "catalog.json"


def hub_data():
    """Evaluate the hub's data block (from `const RENDERS` to `/*END N20*/`) with node and return it as JSON."""
    html = (SKILL / "catalog" / "index.html").read_text(encoding="utf-8")
    a = html.index("const RENDERS")
    end = html.find("/*END N20*/")
    b = end if end > 0 else html.index("const $ =")
    js = html[a:b] + "\nprocess.stdout.write(JSON.stringify({S, NUM, FAMS, MAIN, MORE, SHOOT: typeof SHOOT === 'undefined' ? {} : SHOOT," \
                      " names: Object.fromEntries(RENDERS.map(r => [r, label(r)]))}));"
    r = subprocess.run(["node", "-"], input=js, capture_output=True, text=True, encoding="utf-8")  # stdin: Windows caps argv length
    if r.returncode:
        sys.exit("could not read the hub data block:\n" + r.stderr[-1500:])
    return json.loads(r.stdout)


def runner_of(sid):
    rs = (SKILL / "scripts" / "run_style.py").read_text(encoding="utf-8")
    block = rs[rs.index("STYLES"):rs.index("}", rs.index("STYLES"))]
    if f'"{sid}"' in block:
        return "run_style"
    for m in re.finditer(r'"([A-Z0-9-]+)"', rs[rs.index("}", rs.index("STYLES")):]):
        if m.group(1) == sid:
            return "run_ad"
    return "bespoke"


# styles that are built through another style's builder or an adkit example, not a module of their own
SX = "examples/E6_sneaker_sx.py"
OVERRIDE = {
    "HUD-CLEAN": ("run_style", "python scripts/run_style.py HUD-CLEAN --spec <spec.json> --render  (HUD-HELMET with boot/reticle/radar/voice off)", "examples/hud-clean"),
    "STICKER-POP": ("run_style", "python scripts/run_style.py STOMP-ESCORT --spec <spec.json> --render  (word style: white fill + ink stroke + hard shadow)", "examples/stomp-escort"),
    "STOMP-SX": ("run_ad", "python scripts/run_ad.py <AD> --spec <spec.py> --render", SX),
    "TRACKED-TAGS": ("run_ad", "python scripts/run_ad.py <AD> --spec <spec.py> --render  (keep only tag / callout / counter elements)", SX),
    "COMIC-POP": ("run_ad", "python scripts/run_ad.py COMIC-POP --spec <spec.py> --render  (\"theme\": \"pop\")", "examples/comic-pop/spec.py"),
    "KINETIC-HE": ("run_ad", None, SX), "KINETIC-KARAOKE": ("run_ad", None, SX), "FLASH-CARD": ("run_ad", None, SX),
    "TAPE-HE": ("run_ad", None, "examples/E4_fire_hk.py"), "PRESIDENTIAL-SERIF": ("run_ad", None, SX),
    "STOMP-BEHIND": ("run_ad", None, SX), "GLASS-CALLOUT": ("run_ad", None, SX),
    "ARCH-DRAWING": ("bespoke", None, "examples/E8_tower_bespoke.py"),
}


# adkit (run_ad) styles whose titles ride tracked objects
AD_TRACKED = {"STOMP-BEHIND", "GLASS-CALLOUT", "TRACKED-TAGS"}


def tier_of(sid, runner, example):
    if runner == "bespoke":
        return "bespoke-rewrite"
    if runner == "run_ad":
        return "track-first" if sid in AD_TRACKED else "one-command"
    sys.path.insert(0, str(SKILL / "scripts"))
    from run_style import needed_objects
    ex = SKILL / (example or "") / "spec.json"
    if not ex.is_file():
        return "one-command"
    spec = json.loads(ex.read_text(encoding="utf-8"))
    return "track-first" if needed_objects(sid, spec) else "one-command"


def cmd_build(_):
    d = hub_data()
    plates = json.loads((SKILL / "references" / "plates.json").read_text(encoding="utf-8"))
    fams = {f[0]: f[1] for f in d["FAMS"]}
    styles = []
    for s in d["S"]:
        sid = s["id"]
        main = d["MAIN"].get(sid)
        renders = [r for r in [main, *d["MORE"].get(sid, [])] if r]
        ex = SKILL / "examples" / sid.lower()
        runner = runner_of(sid)
        o_run, o_how, o_ex = OVERRIDE.get(sid, (None, None, None))
        runner = o_run or runner
        how = o_how or {"run_style": f"python scripts/run_style.py {sid} --spec <spec.json> --render",
               "run_ad": "python scripts/run_ad.py <AD> --spec <spec.py> --render   (adkit spec; see examples/*_sx.py, *_hk.py)",
               "bespoke": "bespoke recipe: references/recipes/ (rewrite for the new subject; see styles.md)"}[runner]
        example = o_ex or (str(ex.relative_to(SKILL)).replace("\\", "/") if ex.is_dir() else None)
        styles.append({
            "n": d["NUM"].get(sid), "id": sid, "family": fams.get(s.get("f"), s.get("f")), "one": s.get("one", ""),
            "tags": s.get("tags", []), "fonts": s.get("fonts", ""), "palette": s.get("pal", []), "sample": s.get("src", ""),
            "kling": bool(s.get("kling")), "prompt": s.get("p", ""), "shoot_it_like_this": d["SHOOT"].get(sid, ""),
            "recipe": f"references/styles/{d['NUM'].get(sid, 0):02d}-{sid}.md",
            "recipe_url": f"https://github.com/guyaga/10d10s-bonus-ai-video-titles/blob/master/references/styles/{d['NUM'].get(sid, 0):02d}-{sid}.md",
            "plate_contract": plates.get(sid), "runner": runner, "tier": tier_of(sid, runner, example), "build": how,
            "example": example,
            "preview": f"{HUB}/previews/{sid.lower()}.mp4",
            "renders": [{"label": d["names"].get(r, r), "url": f"{HUB}/full/{r}.mp4"} for r in renders],
        })
    styles.sort(key=lambda x: x["n"] or 999)
    DB.write_text(json.dumps({"hub": HUB, "count": len(styles), "styles": styles}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {DB.relative_to(SKILL)}: {len(styles)} styles "
          f"({sum(s['runner'] == 'run_style' for s in styles)} run_style, {sum(s['runner'] == 'run_ad' for s in styles)} run_ad, "
          f"{sum(s['runner'] == 'bespoke' for s in styles)} bespoke; tiers: "
          + ", ".join(f"{t} {sum(s['tier'] == t for s in styles)}" for t in ("one-command", "track-first", "bespoke-rewrite")) + ")")


def db():
    if not DB.is_file():
        sys.exit("references/catalog.json missing: run `python scripts/catalog.py build`")
    return json.loads(DB.read_text(encoding="utf-8"))["styles"]


def find(key):
    k = key.strip().lstrip("#").upper()
    for s in db():
        if s["id"] == k or (k.isdigit() and s["n"] == int(k)):
            return s
    sys.exit(f"no style '{key}'. Try: python catalog.py list --q {key.lower()}")


def cmd_list(a):
    q = (a.q or "").lower()
    for s in db():
        if a.tag and a.tag.lower() not in [t.lower() for t in s["tags"]]:
            continue
        hay = " ".join([s["id"], s["one"], " ".join(s["tags"]), s["fonts"], s["family"]]).lower()
        if q and q not in hay:
            continue
        print(f"#{s['n']:02d}  {s['id']:<20} {s['family']:<22} {', '.join(s['tags'])}\n      {s['one']}")


def cmd_show(a):
    s = find(a.key)
    print(f"#{s['n']:02d} {s['id']}  ·  {s['family']}{'  ·  Kling sample' if s['kling'] else ''}\n{s['one']}\n")
    print(f"Use for:  {', '.join(s['tags'])}\nFonts:    {s['fonts']}\nPalette:  {' '.join(s['palette'])}")
    print(f"Shoot it: {s['shoot_it_like_this']}\nTier:     {s.get('tier', '?')}\nBuild:    {s['build']}\nExample:  {s['example']}")
    print(f"Recipe:   {s.get('recipe')}  (read it before building)")
    print(f"Watch:    {s['preview']}")
    for r in s["renders"]:
        print(f"          {r['label']}: {r['url']}")
    print(f"\nPrompt:   {s['prompt']}")


def cmd_brief(a):
    s = find(a.key)
    pc = s["plate_contract"] or {}
    print(f"""# Title brief · #{s['n']:02d} {s['id']}

## Project context (from the user)
{a.context}

## Read the recipe first
{s.get('recipe')}: anatomy, timing and eases, typography, layout in px, what the footage must give, every spec key,
the core GSAP move, 9:16, sound, and the QA checklist. Follow it; the summary below is only the headline.

## Style
{s['prompt']}
- Look: {s['one']}
- Fonts: {s['fonts']}  (Hebrew text: Suez One / Karantina / Secular One only; prices as ש״ח)
- Palette: {' '.join(s['palette'])}; swap to the project's brand colours if it has them
- Reference renders: {', '.join(r['url'] for r in s['renders'][:2])}

## The footage this style needs
{s['shoot_it_like_this']}
- Take: {pc.get('take', '?')} · framing: {pc.get('framing', '?')} · free space: {pc.get('negative_space', '?')}
- Gate: {pc.get('gate', '?')}
- No footage yet? Generate it with ai-ad-studio, which writes these shooting lines into the prompt: {pc.get('seedance_lines', [])}

## Build ({s.get('tier', '?')})
1. Footage in hand: `python scripts/catalog.py make {s['id']} <clip.mp4> "<context>"` sets up the project, the objects to
   track and runs the clip check. No footage yet: `python scripts/check_clip.py plan {s['id']} "<context>"`.
2. Edit the starter spec: the words, names, prices, language, brand colours and the beat grid of the music are yours;
   the example `{s['example'] or 'references/recipes/ (bespoke: rewrite for this subject)'}` shows every key.
3. {s['build']}
4. Check 4-6 frames yourself, then scripts/qa.py until "ship".""")


MEDIA_KEYS = ("music", "vo", "matte", "audio", "words", "after")


def cmd_make(a):
    """Start a title project on the user's own footage."""
    import os
    import shutil
    s = find(a.key)
    sid = s["id"]
    clip_src = Path(a.clip).resolve()
    if not clip_src.is_file():
        sys.exit(f"clip not found: {a.clip}")
    out = Path(a.out or f"{sid.lower()}-project").resolve()
    for d in ("clips", "tracks", "renders"):
        (out / d).mkdir(parents=True, exist_ok=True)
    clip = out / "clips" / clip_src.name
    if not clip.exists():
        shutil.copy2(clip_src, clip)
    rel_clip = f"clips/{clip.name}"
    py = sys.executable
    S = SKILL / "scripts"
    he = any("֐" <= ch <= "׿" for ch in a.context)
    print(f"#{s['n']:02d} {sid} · tier: {s.get('tier')} · project: {out}")

    if s["runner"] != "run_style":
        # adkit / bespoke styles: the example is a python SPEC or a recipe; copy it as the starting point
        ex = SKILL / (s["example"] or "references/recipes")
        dst = out / "specs"
        dst.mkdir(exist_ok=True)
        if ex.is_file():
            shutil.copy2(ex, dst / ex.name)
            start = dst / ex.name
        else:
            start = ex
        (out / "CONTEXT.md").write_text(f"# {sid}\n\n{a.context}\n\nClip: {rel_clip}\n", encoding="utf-8")
        print(f"  starting point: {start}\n  context saved: {out / 'CONTEXT.md'}")
        run_check(py, S, sid, clip, None, a)
        print(f"\nNext:\n  1. adapt {start} to your clip, words and brand (styles.md → {sid} lists every element)\n"
              f"  2. {s['build']}   (add --root {out})\n  3. python {S / 'qa.py'} renders/<name>.mp4 --root {out}")
        return

    ex_dir = SKILL / s["example"]
    spec = json.loads((ex_dir / "spec.json").read_text(encoding="utf-8"))
    spec = {k: v for k, v in spec.items() if not k.startswith("_")}
    todo = []
    for k in MEDIA_KEYS:
        v = spec.get(k)
        if isinstance(v, str) and not (ex_dir / v).exists():
            spec.pop(k)
            todo.append({"music": "music: your music bed (mp3), + music_vol",
                         "vo": "vo: your voiceover (mp3), + vo_vol",
                         "matte": "matte: npx hyperframes@0.8.84 remove-background " + rel_clip + " -o mattes/subject_alpha.webm (only for text behind the subject)",
                         "audio": "audio: the dialogue track (defaults to the clip's own sound)",
                         "words": "words: word timings of your VO (python scripts/word_times.py …) or a transcript [{\"w\", \"t\"}]",
                         "after": "after: the second take (the 'after' state)"}[k])
    spec["clip"] = rel_clip
    spec["name"] = sid.lower()
    if he:
        spec["language"] = "he"
    sys.path.insert(0, str(S))
    from run_style import needed_objects, objects_template
    need = needed_objects(sid, spec)
    track = None
    if need:
        objs = out / "objects.json"
        if not objs.exists():
            tpl = objects_template(sid, need)
            if a.context and "TODO" in tpl.get("context", ""):
                # the user's project context is the best shot description we have: use it so --track can run
                tpl["context"] = a.context
            objs.write_text(json.dumps(tpl, ensure_ascii=False, indent=1), encoding="utf-8")
        track = out / "tracks" / "track.json"
        spec["track"] = "tracks/track.json"
        has_todo = "TODO" in objs.read_text(encoding="utf-8")
        if a.track and os.environ.get("GEMINI_API_KEY") and not has_todo and not track.exists():
            print("  tracking (vtrack.py, a few minutes) …")
            subprocess.run([py, str(S / "vtrack.py"), str(clip), str(objs), str(track), "--preview", str(out / "tracks" / "check.mp4")],
                           check=True)
        elif not track.exists():
            todo.insert(0, f"track: describe {', '.join(need)} in objects.json, then run "
                           f"python {S / 'vtrack.py'} {rel_clip} objects.json tracks/track.json --preview tracks/check.mp4 (cwd {out})")
    else:
        spec.pop("track", None)
    todo.append("content: replace the example's words, names, prices and colours with yours (see _context)")
    spec = {"_style": f"#{s['n']:02d} {sid}", "_context": a.context, "_todo": todo, **spec}
    (out / "spec.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"  starter spec: {out / 'spec.json'} (from {s['example']}; keys documented in scripts/styles/)")
    run_check(py, S, sid, clip, track if track and track.exists() else None, a)
    print("\nNext:")
    for i, t in enumerate(todo, 1):
        print(f"  {i}. {t}")
    n = len(todo)
    print(f"  {n + 1}. build + check:  python {S / 'run_style.py'} {sid} --spec {out / 'spec.json'} --root {out}\n"
          f"  {n + 2}. render:         add --render (→ {out / 'renders'})\n"
          f"  {n + 3}. review:         python {S / 'qa.py'} {out / 'renders'}/{sid.lower()}.mp4 --root {out}   (and look at 4-6 frames)")


def run_check(py, S, sid, clip, track, a):
    """The coordinator's clip check (cuts, tracking coverage, title space, edge crop, Gemini second look)."""
    cmd = [py, str(S / "check_clip.py"), "check", sid, str(clip), "--context", a.context]
    if track:
        cmd += ["--track", str(track)]
    if a.no_gemini:
        cmd.append("--no-gemini")
    print("\nClip check (check_clip.py):")
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    print("  " + ((r.stdout or "") + (r.stderr or "")).strip().replace("\n", "\n  "))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build").set_defaults(f=cmd_build)
    p = sub.add_parser("list"); p.add_argument("--tag"); p.add_argument("--q"); p.set_defaults(f=cmd_list)
    p = sub.add_parser("show"); p.add_argument("key"); p.set_defaults(f=cmd_show)
    p = sub.add_parser("brief"); p.add_argument("key"); p.add_argument("context"); p.set_defaults(f=cmd_brief)
    p = sub.add_parser("make"); p.add_argument("key"); p.add_argument("clip"); p.add_argument("context", nargs="?", default="")
    p.add_argument("--out"); p.add_argument("--track", action="store_true"); p.add_argument("--no-gemini", action="store_true")
    p.set_defaults(f=cmd_make)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
