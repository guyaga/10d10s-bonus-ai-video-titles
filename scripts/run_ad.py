"""Build (+ check, + optionally render) one titled video from a declarative spec.

python run_ad.py <AD> [--variant NAME] [--spec path/to/spec.py] [--root DIR] [--render [--sting sting.mp4] [--out NAME]]

  <AD>        id of the piece, e.g. E6_sneaker. Media defaults: clips/<AD>_720p.mp4, tracks/<AD>_vtrack.json (see paths.py)
  --spec      spec file (a module exposing SPEC). Default: <root>/specs/<AD>.py or <root>/specs/<AD>_<variant>.py
  --variant   builds videos/<ad>-<variant>, voice defaults to shared/sfx/<AD>_<variant>_vo.mp3
  --render    render 24 fps + optional end sting + loudnorm -16 LUFS via finalize.py -> renders/<out>.mp4
"""
import importlib.util
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")   # Hebrew + check symbols on Windows consoles
sys.path.insert(0, str(HERE))
import paths  # noqa: E402

sys.argv = paths.take_root_arg(sys.argv)
import adkit  # noqa: E402
import shotkit  # noqa: E402


def arg(name, default=None):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def load_spec(ad, variant=None, spec_path=None):
    f = Path(spec_path) if spec_path else paths.root() / "specs" / (f"{ad}_{variant}.py" if variant else f"{ad}.py")
    if not f.exists():
        raise SystemExit(f"spec not found: {f}")
    sp = importlib.util.spec_from_file_location(f"spec_{ad}", f)
    m = importlib.util.module_from_spec(sp)
    sp.loader.exec_module(m)
    return m.SPEC


def main():
    ad = sys.argv[1]
    var = arg("--variant")
    spec = load_spec(ad, var, arg("--spec"))
    if var:
        spec.setdefault("vo_name", f"{ad}_{var}_vo")
        spec.setdefault("project_suffix", f"-{var}")
    cfg = adkit.build(ad, spec)
    shotkit.build(ad, **cfg)
    pj = cfg["project"] / "package.json"
    if pj.exists():   # keep the pin: a fresh init may write a newer, unpublished version
        import re
        pj.write_text(re.sub(r"hyperframes@\d+\.\d+\.\d+", paths.HF, pj.read_text(encoding="utf-8")), encoding="utf-8")
    r = subprocess.run(f"npx -y {paths.HF} check", cwd=cfg["project"], shell=True, capture_output=True, text=True, encoding="utf-8", errors="replace")
    lines = [ln.strip()[:220] for ln in ((r.stdout or "") + (r.stderr or "")).splitlines() if "✗" in ln or "Check " in ln]
    print(f"[{ad}] project: {cfg['project']}")
    print("\n".join(lines[:15]) or "(check printed no summary lines; run `npx hyperframes check` in the project)")
    if "--render" in sys.argv:
        out = arg("--out", ad + (f"_{var.upper()}" if var else ""))
        cmd = [sys.executable, str(HERE / "finalize.py"), str(cfg["project"]), out]
        if arg("--sting"):
            cmd += ["--sting", arg("--sting")]
        subprocess.run(cmd, check=True)


if __name__ == "__main__":
    main()
