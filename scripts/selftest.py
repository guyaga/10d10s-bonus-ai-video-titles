"""Self-test: does every style build on footage the skill ships with? Run after any change, and after a fresh install.

    python scripts/selftest.py [--styles A,B] [--jobs 3] [--md TESTING_table.md] [--root DIR]

1. run_style.py STYLE --demo (build + hyperframes check: lint, runtime, layout, motion) for every run_style style
2. check_clip.py plan <style> for every catalog style (the planning stage)
3. check_clip.py check <style> <demo clip> --no-gemini for every catalog style (the post stage; PASS/FAIL are both
   valid answers, a crash is not)
No keys, no network except npx fetching the pinned hyperframes once. Exit 0 only when everything passes.
"""
import argparse
import json
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
sys.path.insert(0, str(HERE))
ADKIT_EXAMPLES = {"COMIC-POP": "examples/comic-pop/spec.py"}


def run(cmd, env=None, timeout=900):
    t = time.time()
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or ""), time.time() - t
    except subprocess.TimeoutExpired:
        return 124, "timeout", time.time() - t


def demo_build(style, root):
    env = {**os.environ, "TITLES_ROOT": str(root)}
    code, out, secs = run([sys.executable, str(HERE / "run_style.py"), style, "--demo"], env)
    lines = [ln.strip() for ln in out.splitlines()]
    note = next((ln for ln in lines if "Traceback" in ln or "Error" in ln or ln.startswith("✗")), "")
    if code and not note:
        note = next((ln for ln in reversed(lines) if ln), "")[:160]
    return style, code == 0, round(secs), note[:160]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--styles")
    ap.add_argument("--jobs", type=int, default=3)
    ap.add_argument("--md")
    ap.add_argument("--root")
    a = ap.parse_args()
    from run_style import STYLES
    styles = a.styles.split(",") if a.styles else list(STYLES)
    root = Path(a.root or tempfile.mkdtemp(prefix="titles-selftest-")).resolve()
    print(f"selftest root: {root}\n")

    # 1. demo builds
    with ThreadPoolExecutor(a.jobs) as ex:
        builds = list(ex.map(lambda s: demo_build(s, root), styles))
    # adkit examples that run as-is on the bundled footage (run_ad.py)
    for sid, spec in ADKIT_EXAMPLES.items():
        env = {**os.environ, "TITLES_ROOT": str(root)}
        code, out, secs = run([sys.executable, str(HERE / "run_ad.py"), sid, "--spec", str(SKILL / spec)], env)
        note = next((ln.strip() for ln in out.splitlines() if "Traceback" in ln or ln.strip().startswith("✗")), "")
        builds.append((sid + " (run_ad)", code == 0 and "Check passed" in out, round(secs), note[:160]))
    ok_b = sum(b[1] for b in builds)
    print(f"{'style':<22}{'demo build + check':<20}{'s':>5}  note")
    for s, ok, secs, note in builds:
        print(f"{s:<22}{'PASS' if ok else 'FAIL':<20}{secs:>5}  {note}")

    # 2 + 3. the clip checker, planning and post
    cat = json.loads((SKILL / "references" / "catalog.json").read_text(encoding="utf-8"))["styles"]
    demo = SKILL / "examples" / "demo" / "runway_demo_720p.mp4"
    plan_fail, check_fail, verdicts = [], [], {}
    for st in cat:
        c, out, _ = run([sys.executable, str(HERE / "check_clip.py"), "plan", st["id"], "selftest"], timeout=120)
        if c != 0:
            plan_fail.append(f"{st['id']}: {out.strip().splitlines()[-1][:120] if out.strip() else c}")
        c, out, _ = run([sys.executable, str(HERE / "check_clip.py"), "check", st["id"], str(demo), "--no-gemini"], timeout=300)
        first = out.strip().splitlines()[0] if out.strip() else ""
        if c not in (0, 3) or "Traceback" in out:
            check_fail.append(f"{st['id']}: {out.strip().splitlines()[-1][:120] if out.strip() else c}")
        verdicts[st["id"]] = first.split(" · ")[0]
    print(f"\ncheck_clip plan : {len(cat) - len(plan_fail)}/{len(cat)} ok" + ("".join(f"\n  FAIL {x}" for x in plan_fail)))
    print(f"check_clip check: {len(cat) - len(check_fail)}/{len(cat)} ran on the demo clip" + ("".join(f"\n  FAIL {x}" for x in check_fail)))
    vc = {}
    for v in verdicts.values():
        vc[v] = vc.get(v, 0) + 1
    print("  verdicts on the demo clip:", ", ".join(f"{k} {n}" for k, n in sorted(vc.items())))

    total_ok = ok_b == len(builds) and not plan_fail and not check_fail
    print(f"\nRESULT: demo builds {ok_b}/{len(builds)} · plan {len(cat) - len(plan_fail)}/{len(cat)} · "
          f"check {len(cat) - len(check_fail)}/{len(cat)} → {'ALL PASS' if total_ok else 'FAILURES'}")
    if a.md:
        rows = "\n".join(f"| {s} | {'PASS' if ok else 'FAIL'} | {secs} s | {note.replace('|', '/')} |" for s, ok, secs, note in builds)
        Path(a.md).write_text(f"| Style | `--demo` build + check | Time | Note |\n|---|---|---|---|\n{rows}\n\n"
                              f"check_clip.py plan: {len(cat) - len(plan_fail)}/{len(cat)} · check on the demo clip: "
                              f"{len(cat) - len(check_fail)}/{len(cat)} (verdicts: {', '.join(f'{k} {n}' for k, n in sorted(vc.items()))})\n",
                              encoding="utf-8")
    sys.exit(0 if total_ok else 1)


if __name__ == "__main__":
    main()
