"""Build (+ check, + optionally render) one catalog style from a spec file.

python run_style.py STYLE --spec spec.json [--root DIR] [--render [--out NAME] [--sting end.mp4]] [--no-check]
python run_style.py STYLE --demo [--render]      # preview any style on the footage bundled with the skill (no keys)
python run_style.py --list

STYLE is a catalog ID (see references/styles.md), e.g. STOMP-ESCORT, COUNTDOWN-CTA, HUD-HELMET, SCIFI-TARGETING,
MAP-FLYOVER, CAMPUS-AR, SPEED-STAT. The adkit styles (KINETIC-HE, TAPE-HE, ...) run through run_ad.py; the crafted-world
styles are bespoke specs (run_ad.py with html_front/css/js).
The spec is JSON (or a .py exposing SPEC). Relative paths inside it resolve against the spec's folder, then the project
root. Every builder documents its keys at the top of scripts/styles/<module>.py; examples/<style>/ has a working spec.
"""
import importlib
import json
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(HERE))
import paths  # noqa: E402

sys.argv = paths.take_root_arg(sys.argv)
import shotkit  # noqa: E402

STYLES = {  # catalog ID -> module in scripts/styles
    "STOMP-ESCORT": "runway", "COUNTDOWN-CTA": "runway", "HUD-HELMET": "helmet", "HUD-CLEAN": "helmet", "SCIFI-TARGETING": "targeting",
    "MAP-FLYOVER": "mapflyover", "CAMPUS-AR": "campus", "SPEED-STAT": "speedstat",
    # AE classics
    "VIRAL-CAPTIONS": "viral", "DECODE-TYPE": "decode", "GLITCH-RGB": "glitch", "NEON-SIGN": "neon",
    "KEYNOTE-REVEAL": "keynote", "SPLIT-FLAP": "splitflap", "SIGNATURE-WRITE-ON": "writeon", "BROADCAST-PACK": "broadcast",
    "FILM-TITLE-CARD": "filmcard", "PARTICLE-TEXT": "particles", "FLIP-MONTAGE-LOGO": "flipmontage", "TEXT-ON-PATH": "textpath",
    # N20 BEGIN  #42-#61 (Kling plates)
    "LOWER-THIRD-CORP": "lowerthird",
    "BREAKING-NEWS": "breakingnews",
    "LEADER-CALLOUTS": "leadercallouts",
    "DATA-CHARTS": "datacharts",
    "KPI-COUNTERS": "kpicounters",
    "APP-UI-POPUPS": "appui",
    "CHAT-BUBBLES": "chatbubbles",
    "SOCIAL-CTA": "socialcta",
    "END-SCREEN": "endscreen",
    "PODCAST-TAGS": "podcasttags",
    "CHAPTER-MARKERS": "chapters",
    "QUOTE-TESTIMONIAL": "quote",
    "DOC-LOCATION-STAMP": "docstamp",
    "SWISS-GRID": "swissgrid",
    "GRADIENT-GLASS": "glass",
    "BEFORE-AFTER-SPLIT": "beforeafter",
    "LOGO-SHINE-REVEAL": "logoshine",
    "LYRIC-KINETIC-3D": "lyric3d",
    "TIMELINE-HISTORY": "timeline",
    "LISTING-SPECS": "listing",
    # N20 END
}
ADKIT = ["STOMP-BEHIND", "GLASS-CALLOUT", "KINETIC-HE", "TAPE-HE", "KINETIC-KARAOKE", "FLASH-CARD", "PRESIDENTIAL-SERIF"]


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def load(spec_path):
    p = Path(spec_path).resolve()
    if p.suffix == ".py":
        import importlib.util
        sp = importlib.util.spec_from_file_location("spec_mod", p)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m.SPEC, p.parent
    return json.loads(p.read_text(encoding="utf-8")), p.parent


IMPLICIT = {  # objects a builder tracks by default even when the spec does not name them
    "HUD-HELMET": lambda sp: [sp.get("eyes", "eyes"), sp.get("face", "face")],
    "HUD-CLEAN": lambda sp: [sp.get("eyes", "eyes"), sp.get("face", "face")],
    "STOMP-ESCORT": lambda sp: [sp.get("follow", "model")] if sp.get("items") else [],
    "COUNTDOWN-CTA": lambda sp: [sp.get("follow", "model")] if sp.get("items") else [],
}
REQUIRED_FILES = {"VIRAL-CAPTIONS": ("words", "a word-timing JSON: python scripts/word_times.py (from a VO) or any transcript as "
                                              '[{"w": "word", "t": 1.23}, ...]'),
                  "BEFORE-AFTER-SPLIT": ("after", "the second take of the same camera move (the 'after' state)")}


def needed_objects(style, spec):
    from styles.common import spec_objects
    names = spec_objects(spec) + [r for r in spec.get("route", []) if isinstance(r, str)] + IMPLICIT.get(style, lambda sp: [])(spec)
    return list(dict.fromkeys(n for n in names if n))


def objects_template(style, names):
    ex = paths.SKILL / "examples" / style.lower() / "objects.json"
    known = {}
    if ex.exists():
        try:
            known = {o["name"]: o["desc"] for o in json.loads(ex.read_text(encoding="utf-8"))["objects"]}
        except Exception:
            pass
    return {"context": "TODO: one line describing your shot (who/what, action, camera)",
            "objects": [{"name": n, "desc": known.get(n, f"TODO: describe '{n}' in YOUR footage (colour, material, which part)")}
                        for n in names]}


def preflight(style, spec, base):
    """Stop early, with the exact fix, when an input the style cannot live without is missing."""
    from styles.common import res
    probs = []
    clip = res(base, spec.get("clip")) if spec.get("clip") else None
    if not clip or not clip.exists():
        probs.append(f"your footage is missing: spec \"clip\" = {spec.get('clip')!r}\n"
                     f"    put your video there (any mp4; 16:9 renders at 1920x1080) or edit \"clip\" in the spec.\n"
                     f"    To just see the style: python scripts/run_style.py {style} --demo")
    if style in REQUIRED_FILES:
        key, what = REQUIRED_FILES[style]
        v = spec.get(key)
        if isinstance(v, str) and not res(base, v).exists():
            probs.append(f"{style} needs \"{key}\": {what}. Not found: {v}")
    need = needed_objects(style, spec)
    if need:
        tr = spec.get("track")
        files = [res(base, x) for x in (tr if isinstance(tr, list) else [tr])] if tr else []
        have = set()
        for f in files:
            if f and f.exists():
                have |= set(json.loads(f.read_text(encoding="utf-8")).get("objects", {}))
        missing = [n for n in need if n not in have]
        if missing:
            obj_path = Path(base) / "objects.json"
            if not obj_path.exists():
                obj_path.write_text(json.dumps(objects_template(style, need), ensure_ascii=False, indent=1), encoding="utf-8")
            clip_s = spec.get("clip", "clips/your_clip.mp4")
            tr_s = tr if isinstance(tr, str) else "tracks/your_track.json"
            step3 = ("build again" if isinstance(tr, str) else f'set "track": "{tr_s}" in the spec, then build again')
            probs.append(f"{style} rides tracked objects your track does not have: {', '.join(missing)}\n"
                         f"    1. edit {obj_path} (one entry per object; describe it as it looks in YOUR footage)\n"
                         f"    2. python {paths.SKILL / 'scripts' / 'vtrack.py'} {clip_s} {obj_path.name} {tr_s} --preview tracks/check.mp4\n"
                         f"       (needs GEMINI_API_KEY; map/facade points: scripts/track.py)\n"
                         f"    3. watch tracks/check.mp4 (the boxes must sit on the objects), then {step3}.\n"
                         f"    Or rename the spec's follow/obj names to objects your track already has: {sorted(have) or 'none'}")
    if probs:
        raise SystemExit("\n".join(f"[{style}] {p}" for p in probs))


def main():
    if "--list" in sys.argv or len(sys.argv) < 2:
        print("run_style.py styles:", ", ".join(STYLES))
        print("run_ad.py (adkit spec) styles:", ", ".join(ADKIT))
        return
    style = sys.argv[1].upper()
    if style not in STYLES:
        raise SystemExit(f"unknown style {style}. run_style.py handles: {', '.join(STYLES)}"
                         + (f"\n{style} is an adkit style: python run_ad.py <AD> --spec your_spec.py" if style in ADKIT else ""))
    demo = "--demo" in sys.argv
    if demo:
        import os
        if not os.environ.get("TITLES_ROOT"):
            os.environ["TITLES_ROOT"] = str(Path.cwd() / "titles-demo")
        spec_path = arg("--spec") or paths.SKILL / "examples" / style.lower() / "spec.json"
    else:
        spec_path = arg("--spec") or sys.exit("--spec is required (or --demo to preview the style on bundled footage)")
    spec, base = load(spec_path)
    if demo:
        import demo as demo_mod
        spec, notes = demo_mod.prepare(style, spec, base, needed_objects(style, spec))
        print(f"[{style}] DEMO: " + "; ".join(notes))
    else:
        preflight(style, spec, base)
    mod = importlib.import_module(f"styles.{STYLES[style]}")
    cfg = mod.build(spec, base, style)
    name = spec.get("name", style.lower())
    shotkit.build(name, **cfg)
    project = Path(cfg["project"])
    pj = project / "package.json"
    if pj.exists():
        pj.write_text(re.sub(r"hyperframes@\d+\.\d+\.\d+", paths.HF, pj.read_text(encoding="utf-8")), encoding="utf-8")
    ok = True
    if "--no-check" not in sys.argv:
        # --demo: the bundled footage is bright and neutral, so contrast verdicts there say nothing about the style;
        # the structural passes (lint, runtime, layout, motion) still run. Real builds keep the WCAG contrast pass.
        flags = " --no-contrast" if (demo or "--no-contrast" in sys.argv) else ""
        r = subprocess.run(f"npx -y {paths.HF} check{flags}", cwd=project, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
        out = (r.stdout or "") + (r.stderr or "")
        lines = [ln.strip()[:220] for ln in out.splitlines() if "✗" in ln or "Check " in ln or "error" in ln.lower()]
        print(f"[{style}] project: {project}")
        print("\n".join(lines[:20]) or out[-800:])
        ok = r.returncode == 0
    if "--render" in sys.argv:
        cmd = [sys.executable, str(HERE / "finalize.py"), str(project), arg("--out", name)]
        if arg("--sting"):
            cmd += ["--sting", arg("--sting")]
        subprocess.run(cmd, check=True)
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
