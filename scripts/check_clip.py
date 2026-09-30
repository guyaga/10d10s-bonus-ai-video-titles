"""Will this footage carry this title style? Two stages, one tool.

PLANNING (no footage yet): how to shoot or prompt the footage for a style
    python check_clip.py plan <n|STYLE-ID> ["project context"]
    → the style's shooting requirements + ready-to-paste lines for a Seedance / Kling / Veo prompt or a shot list,
      and the objects.json to track afterwards.

POST-PRODUCTION (footage exists): check the clip against the style before building titles
    python check_clip.py check <n|STYLE-ID> clip.mp4 [--objects objects.json | --track track.json]
                               [--context "..."] [--no-gemini] [--out report.json]
    → PASS / PASS WITH WARNINGS / FAIL, what to fix (trim points, reframing, a better-suited style),
      and the list of catalog styles this clip already fits.

Checks (calibrated on real AI plates):
  cuts        motion continuity (~300 corners tracked frame to frame; a cut = most points lost AND a luma-histogram jump).
              ffmpeg's scene score misses soft same-room AI cuts (0.06 vs 0.03 on a clean take); this doesn't.
  tracking    vtrack.py coverage per object (what the titles will ride)
  title space median free margin beside the main subject, on the side the style needs
  edge crop   full-body styles: how often the subject touches the top/bottom edge (feet or head cut)
  second look Gemini watches the clip against the style: text/logos in frame, subject, framing, camera, one take
"""
import argparse
import json
import os
import statistics
import subprocess
import sys
import time
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SKILL = Path(__file__).resolve().parent.parent
PLATES = SKILL / "references" / "plates.json"
CATALOG = SKILL / "references" / "catalog.json"


def load(p):
    return json.loads(Path(p).read_text(encoding="utf-8"))


def resolve(key):
    """'#43' / '43' / 'breaking-news' → ('BREAKING-NEWS', contract, catalog entry)"""
    plates = load(PLATES)
    cat = {s["id"]: s for s in load(CATALOG)["styles"]} if CATALOG.is_file() else {}
    k = key.strip().lstrip("#").upper()
    if k.isdigit():
        k = next((sid for sid, s in cat.items() if s.get("n") == int(k)), k)
    if k not in plates:
        sys.exit(f"unknown style '{key}' (no shooting requirements in references/plates.json)")
    return k, plates[k], cat.get(k, {})


# ─────────────────────────── measurements ───────────────────────────
def count_cuts(clip):
    import cv2
    cap = cv2.VideoCapture(str(clip))
    fps, prev, n, cuts = cap.get(cv2.CAP_PROP_FPS) or 24, None, 0, []
    while True:
        ok, fr = cap.read()
        if not ok:
            break
        g = cv2.cvtColor(cv2.resize(fr, (320, 180)), cv2.COLOR_BGR2GRAY)
        if prev is not None:
            lost = 1.0
            p0 = cv2.goodFeaturesToTrack(prev, 300, 0.01, 6)
            if p0 is not None:
                _, st, err = cv2.calcOpticalFlowPyrLK(prev, g, p0, None, winSize=(21, 21), maxLevel=3)
                lost = 1 - ((st.ravel() == 1) & (err.ravel() < 12)).mean()
            hd = cv2.compareHist(cv2.calcHist([prev], [0], None, [32], [0, 256]),
                                 cv2.calcHist([g], [0], None, [32], [0, 256]), cv2.HISTCMP_BHATTACHARYYA)
            if (lost >= 0.65 and hd >= 0.08) or hd >= 0.25:
                cuts.append(round(n / fps, 2))
        prev, n = g, n + 1
    return cuts, round(n / fps, 2)


def gemini_check(clip, style, contract, context):
    from google import genai
    from google.genai import types
    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    f = client.files.upload(file=str(clip))
    while f.state.name == "PROCESSING":
        time.sleep(3)
        f = client.files.get(name=f.name)
    ask = f"""You check footage for a motion-graphics pipeline. The title style {style} will be added on top in post, so
the footage must suit it. Style requirements: {json.dumps(contract, ensure_ascii=False)}. Project context: {context or 'n/a'}.
Return JSON only: {{"text_or_logos_visible": bool, "subject_ok": bool, "framing_ok": bool, "camera_ok": bool,
"single_unbroken_take": bool, "issues": [short strings with MM:SS], "fix": "one or two lines: how to reshoot/re-prompt or trim"}}"""
    r = client.models.generate_content(model="gemini-3.7-flash", contents=[f, ask],
                                       config=types.GenerateContentConfig(response_mime_type="application/json"))
    try:
        client.files.delete(name=f.name)
    except Exception:
        pass
    return json.loads(r.text)


def longest_clean(cuts, dur):
    edges = [0.0, *cuts, dur]
    segs = [(edges[i], edges[i + 1]) for i in range(len(edges) - 1)]
    return max(segs, key=lambda s: s[1] - s[0])


# ─────────────────────────── plan ───────────────────────────
def cmd_plan(a):
    sid, c, cat = resolve(a.style)
    ns = c.get("negative_space", {})
    lines = c.get("seedance_lines", [])
    print(f"""# Shooting plan · #{cat.get('n', '?')} {sid}
{cat.get('one', '')}
Project: {a.context or '(add your project context)'}

## The footage this style needs
- Take: {c.get('take')} (max cuts {c.get('max_cuts', 0)}) · length {c.get('duration_s')} s · aspect {c.get('aspect')}
- Subject: {c.get('subject')}
- Framing: {c.get('framing')}
- Free space for the titles: {ns.get('side', 'none')} side(s), at least {int(ns.get('min_frac', 0) * 100)}% of the frame
- Camera: {c.get('camera')}
- Needs a subject cut-out (matte): {'yes' if c.get('separation') else 'no'} · lands on a beat grid: {'yes' if c.get('beats') else 'no'}
- Must stay trackable: {', '.join(c.get('track', [])) or 'nothing (static layout)'}
- No text, logos or signage in frame, ever: the titles bring all the words.

## Paste into your video prompt (Seedance / Kling / Veo), adapting the nouns to your scene
""" + "\n".join(f"  {l}" for l in lines) + f"""

## Filming it yourself
Shoot the same rules: {c.get('take')}, {c.get('framing')}, keep the {ns.get('side', 'frame')} clear, {c.get('camera')}.

## After you have the clip
  python scripts/check_clip.py check {sid} your_clip.mp4 --objects objects.json
  (objects.json lists what to track: {', '.join(c.get('track', [])) or 'none needed'})""")


# ─────────────────────────── check ───────────────────────────
def fits(meas):
    """catalog styles whose requirements this clip already meets (measured checks only)"""
    out = []
    for sid, c in load(PLATES).items():
        g = c.get("gate", {})
        if len(meas["cuts"]) > g.get("max_cuts", c.get("max_cuts", 0)):
            continue
        side = c.get("negative_space", {}).get("side", "none")
        fm = meas.get("free_margin")
        if fm and side in ("left", "right", "both"):
            have = {"left": fm["left"], "right": fm["right"], "both": min(fm["left"], fm["right"])}[side]
            if have < g.get("min_free_margin", 0):
                continue
        lo, hi = c.get("duration_s", [0, 999])
        if meas["duration"] < lo * 0.6:
            continue
        out.append(sid)
    return out


def cmd_check(a):
    sid, c, cat = resolve(a.style)
    g = c.get("gate", {})
    clip = Path(a.clip)
    if not clip.is_file():
        sys.exit(f"clip not found: {clip}")
    rep = {"style": sid, "clip": str(clip), "checks": {}, "fails": [], "warns": [], "fix": []}

    cuts, dur = count_cuts(clip)
    rep["checks"].update(cuts=cuts, duration=dur)
    allowed = g.get("max_cuts", c.get("max_cuts", 0))
    if len(cuts) > allowed:
        s0, s1 = longest_clean(cuts, dur)
        rep["fails"].append(f"{len(cuts)} cut(s) at {cuts} s; {sid} allows {allowed}")
        rep["fix"].append(f"trim to the longest clean segment {s0:.2f}–{s1:.2f} s "
                          f"(ffmpeg -ss {s0:.2f} -to {s1:.2f} -i {clip.name} -c:v libx264 -crf 18 trimmed.mp4), or regenerate as one take")

    track = Path(a.track) if a.track else None
    if a.objects and not track:
        track = clip.with_suffix(".track.json")
        if not track.is_file():
            subprocess.run([sys.executable, str(SKILL / "scripts" / "vtrack.py"), str(clip), a.objects, str(track),
                            "--canvas", "1920x1080"], check=True)
    if track and track.is_file():
        tr = load(track)
        W, H = tr["canvas"]
        cov = {k: round(sum(1 for b in v if b) / max(1, len(v)), 3) for k, v in tr["objects"].items()}
        rep["checks"]["track_coverage"] = cov
        need = g.get("min_track_coverage", 0.8)
        for k, v in cov.items():
            if v < need:
                rep["fails"].append(f"'{k}' tracked in only {v:.0%} of frames (needs {need:.0%})")
                rep["fix"].append(f"make '{k}' more specific in objects.json (colour, material, which part), or pick a "
                                  f"style that doesn't ride '{k}'")
        main = next(iter(tr["objects"]))
        boxes = [b for b in tr["objects"][main] if b]
        if boxes:
            left = statistics.median(b[0] / W for b in boxes)
            right = statistics.median((W - b[2]) / W for b in boxes)
            rep["checks"]["free_margin"] = {"left": round(left, 3), "right": round(right, 3), "object": main}
            side = c.get("negative_space", {}).get("side", "none")
            need_m = g.get("min_free_margin", c.get("negative_space", {}).get("min_frac", 0))
            have = {"left": left, "right": right, "both": min(left, right)}.get(side)
            if have is not None and have < need_m:
                rep["fails"].append(f"title space ({side}): {have:.0%} free, needs {need_m:.0%}")
                rep["fix"].append("reframe wider / scale the plate down with a blurred fill, or pick a style that "
                                  "needs the other side (see 'fits' below)")
            if "full body" in c.get("framing", ""):
                edge = sum(1 for b in boxes if b[1] <= H * .005 or b[3] >= H * .995) / len(boxes)
                rep["checks"]["body_touches_edge"] = round(edge, 3)
                if edge > .40:
                    rep["fails"].append(f"subject cropped at the frame edge in {edge:.0%} of frames")
                elif edge > .05:
                    rep["warns"].append(f"subject touches the frame edge in {edge:.0%} of frames (feet/head cropped)")
    elif c.get("track"):
        rep["warns"].append(f"tracking not checked: pass --objects objects.json (this style rides: {', '.join(c['track'])})")

    if not a.no_gemini and os.environ.get("GEMINI_API_KEY"):
        gm = gemini_check(clip, sid, c, a.context)
        rep["checks"]["second_look"] = gm
        if gm.get("text_or_logos_visible"):
            rep["fails"].append("text or logos visible in the footage (they will fight the titles)")
        if gm.get("subject_ok") is False:
            rep["fails"].append("the subject doesn't match what this style needs")
        if c.get("take") == "one-take" and gm.get("single_unbroken_take") is False and not cuts:
            rep["warns"].append("the second look sees a cut the motion check didn't: scrub the clip")
        for k in ("framing_ok", "camera_ok"):
            if gm.get(k) is False:
                rep["warns"].append(f"{k.replace('_ok', '')}: {'; '.join(gm.get('issues', []))[:200]}")
        if gm.get("fix"):
            rep["fix"].append(gm["fix"])

    rep["fits"] = fits(rep["checks"])
    rep["verdict"] = "FAIL" if rep["fails"] else ("PASS WITH WARNINGS" if rep["warns"] else "PASS")
    if a.out:
        Path(a.out).write_text(json.dumps(rep, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"{rep['verdict']} · {sid} on {clip.name} ({dur} s, {len(cuts)} cut(s))")
    for x in rep["fails"]:
        print("  ✗", x)
    for x in rep["warns"]:
        print("  !", x)
    for x in rep["fix"]:
        print("  → fix:", x)
    print(f"  technically fits (cuts, title space, length; judge the subject yourself) ({len(rep['fits'])}): {', '.join(rep['fits'][:14])}{' …' if len(rep['fits']) > 14 else ''}")
    sys.exit(3 if rep["fails"] else 0)


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("plan"); p.add_argument("style"); p.add_argument("context", nargs="?", default="")
    p.set_defaults(f=cmd_plan)
    p = sub.add_parser("check"); p.add_argument("style"); p.add_argument("clip")
    p.add_argument("--objects"); p.add_argument("--track"); p.add_argument("--context", default="")
    p.add_argument("--no-gemini", action="store_true"); p.add_argument("--out")
    p.set_defaults(f=cmd_check)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
