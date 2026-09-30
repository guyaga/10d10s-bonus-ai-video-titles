"""Build (+ check, + optionally render) one catalog style from a spec file.

python run_style.py STYLE --spec spec.json [--root DIR] [--render [--out NAME] [--sting end.mp4]] [--no-check]
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
    "STOMP-ESCORT": "runway", "COUNTDOWN-CTA": "runway", "HUD-HELMET": "helmet", "SCIFI-TARGETING": "targeting",
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


def main():
    if "--list" in sys.argv or len(sys.argv) < 2:
        print("run_style.py styles:", ", ".join(STYLES))
        print("run_ad.py (adkit spec) styles:", ", ".join(ADKIT))
        return
    style = sys.argv[1].upper()
    if style not in STYLES:
        raise SystemExit(f"unknown style {style}. run_style.py handles: {', '.join(STYLES)}"
                         + (f"\n{style} is an adkit style: python run_ad.py <AD> --spec your_spec.py" if style in ADKIT else ""))
    spec, base = load(arg("--spec") or sys.exit("--spec is required"))
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
        r = subprocess.run(f"npx -y {paths.HF} check", cwd=project, shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
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
