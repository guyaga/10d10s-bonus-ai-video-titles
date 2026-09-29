"""Frame-by-frame object tracking = Gemini vision keyframes + optical-flow in-betweens.

Usage:
  python vtrack.py clip.mp4 objects.json out.json [--kfps 8] [--canvas 1920x1080] [--preview p.mp4]

objects.json:
  {"objects": [{"name": "pilot_head", "desc": "the man's head and face"}, ...],
   "context": "optional one-line description of the shot"}

Pipeline
  1. Sample keyframes at --kfps (default 8/s). Gemini (gemini-3.7-flash) returns a box for every
     named object on every keyframe (box_2d = [ymin, xmin, ymax, xmax] on a 0-1000 grid, or
     visible=false). Batched 8 frames per request, structured JSON output.
  2. Between two keyframes, each box is carried frame by frame with pyramidal Lucas-Kanade
     optical flow on the features inside it (median shift + median scale = "median flow").
  3. Drift correction: the flow path is bent so it lands exactly on the next Gemini box
     (error distributed linearly across the segment).
  4. Light temporal smoothing (Savitzky-Golay) to remove jitter; output in canvas pixels.

out.json: {"fps", "frames", "canvas", "objects": {name: [[x0,y0,x1,y1] | null, ...per frame]}}
"""
import argparse
import json
import os
import sys

import cv2
import numpy as np
from google import genai
from google.genai import types
from scipy.signal import savgol_filter

MODEL = "gemini-3.7-flash"
BATCH = 8


def gemini_boxes(client, frames, idxs, objects, context):
    """frames: list of BGR images; returns {frame_idx: {name: [x0,y0,x1,y1] in px or None}}"""
    names = [o["name"] for o in objects]
    desc = "\n".join(f'- "{o["name"]}": {o["desc"]}' for o in objects)
    h, w = frames[0].shape[:2]
    parts = []
    for i, f in zip(idxs, frames):
        ok, buf = cv2.imencode(".jpg", f, [cv2.IMWRITE_JPEG_QUALITY, 88])
        parts.append(types.Part.from_text(text=f"FRAME {i}"))
        parts.append(types.Part.from_bytes(data=buf.tobytes(), mime_type="image/jpeg"))
    parts.append(types.Part.from_text(text=(
        f"These are {len(idxs)} consecutive keyframes from one continuous video shot. {context}\n"
        f"For EVERY frame, give a tight bounding box for each of these objects:\n{desc}\n"
        "box_2d is [ymin, xmin, ymax, xmax] normalised to 0-1000. Be precise and consistent between "
        "frames (the same physical object). If an object is not visible in a frame, set visible=false.")))
    schema = {
        "type": "OBJECT",
        "properties": {"frames": {"type": "ARRAY", "items": {
            "type": "OBJECT",
            "properties": {
                "frame": {"type": "INTEGER"},
                "objects": {"type": "ARRAY", "items": {
                    "type": "OBJECT",
                    "properties": {
                        "name": {"type": "STRING", "enum": names},
                        "visible": {"type": "BOOLEAN"},
                        "box_2d": {"type": "ARRAY", "items": {"type": "INTEGER"}},
                    },
                    "required": ["name", "visible"]}}},
            "required": ["frame", "objects"]}}},
        "required": ["frames"]}
    for attempt in range(3):
        try:
            r = client.models.generate_content(
                model=MODEL, contents=[types.Content(role="user", parts=parts)],
                config=types.GenerateContentConfig(response_mime_type="application/json",
                                                   response_schema=schema, temperature=0))
            data = json.loads(r.text)
            break
        except Exception as e:  # noqa: BLE001
            print(f"  gemini retry {attempt + 1}: {e}", file=sys.stderr)
    else:
        raise SystemExit("gemini failed")
    out = {}
    for fr in data["frames"]:
        d = {}
        for o in fr["objects"]:
            b = o.get("box_2d")
            if o.get("visible") and b and len(b) == 4:
                y0, x0, y1, x1 = b
                d[o["name"]] = [x0 * w / 1000, y0 * h / 1000, x1 * w / 1000, y1 * h / 1000]
            else:
                d[o["name"]] = None
        out[fr["frame"]] = d
    return out


def flow_step(g0, g1, box):
    """Move/scale box from gray g0 to g1 by median flow of features inside it."""
    x0, y0, x1, y1 = box
    h, w = g0.shape
    m = np.zeros_like(g0)
    xa, ya, xb, yb = map(int, [max(0, x0), max(0, y0), min(w - 1, x1), min(h - 1, y1)])
    if xb - xa < 4 or yb - ya < 4:
        return box
    m[ya:yb, xa:xb] = 255
    p0 = cv2.goodFeaturesToTrack(g0, 200, 0.01, 4, mask=m)
    if p0 is None or len(p0) < 4:
        return box
    p1, st, _ = cv2.calcOpticalFlowPyrLK(g0, g1, p0, None, winSize=(21, 21), maxLevel=3)
    a, b = p0[st == 1].reshape(-1, 2), p1[st == 1].reshape(-1, 2)
    if len(a) < 4:
        return box
    d = np.median(b - a, axis=0)
    ca, cb = a.mean(0), b.mean(0)
    da, db = np.linalg.norm(a - ca, axis=1), np.linalg.norm(b - cb, axis=1)
    s = float(np.median(db[da > 1] / da[da > 1])) if (da > 1).sum() > 3 else 1.0
    s = float(np.clip(s, 0.9, 1.1))
    cx, cy = (x0 + x1) / 2 + d[0], (y0 + y1) / 2 + d[1]
    hw, hh = (x1 - x0) / 2 * s, (y1 - y0) / 2 * s
    return [cx - hw, cy - hh, cx + hw, cy + hh]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("objects")
    ap.add_argument("out")
    ap.add_argument("--kfps", type=float, default=8)
    ap.add_argument("--canvas", default="1920x1080")
    ap.add_argument("--preview")
    a = ap.parse_args()
    spec = json.load(open(a.objects, encoding="utf-8"))
    objects, context = spec["objects"], spec.get("context", "")
    names = [o["name"] for o in objects]
    cw, ch = map(int, a.canvas.split("x"))

    cap = cv2.VideoCapture(a.clip)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    frames = []
    while True:
        ok, f = cap.read()
        if not ok:
            break
        frames.append(f)
    n = len(frames)
    h, w = frames[0].shape[:2]
    step = max(1, round(fps / a.kfps))
    keys = list(range(0, n, step))
    if keys[-1] != n - 1:
        keys.append(n - 1)
    print(f"{n} frames @ {fps}fps, {len(keys)} keyframes, {len(names)} objects")

    client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
    det = {}
    for i in range(0, len(keys), BATCH):
        ks = keys[i:i + BATCH]
        det.update(gemini_boxes(client, [frames[k] for k in ks], ks, objects, context))
        print(f"  gemini keyframes {ks[0]}-{ks[-1]} done")

    gray = [cv2.cvtColor(f, cv2.COLOR_BGR2GRAY) for f in frames]
    res = {nm: [None] * n for nm in names}
    for nm in names:
        for ka, kb in zip(keys[:-1], keys[1:]):
            A = det.get(ka, {}).get(nm)
            B = det.get(kb, {}).get(nm)
            if A is None:
                continue
            path = [A]
            for t in range(ka, kb):
                path.append(flow_step(gray[t], gray[t + 1], path[-1]))
            if B is not None:  # drift-correct onto next keyframe
                err = np.array(B) - np.array(path[-1])
                L = kb - ka
                path = [list(np.array(p) + err * (j / L)) for j, p in enumerate(path)]
            for j, p in enumerate(path[:-1] if B is not None else path):
                res[nm][ka + j] = p
        last = det.get(keys[-1], {}).get(nm)
        if last is not None:
            res[nm][keys[-1]] = last
        # smoothing over visible runs
        arr = res[nm]
        i = 0
        while i < n:
            if arr[i] is None:
                i += 1
                continue
            j = i
            while j < n and arr[j] is not None:
                j += 1
            run = np.array(arr[i:j], float)
            if len(run) >= 9:
                run = savgol_filter(run, 9, 2, axis=0)
            for k2 in range(i, j):
                arr[k2] = run[k2 - i].tolist()
            i = j

    sx, sy = cw / w, ch / h
    out = {"fps": fps, "frames": n, "canvas": [cw, ch], "source": [w, h], "objects": {
        nm: [None if b is None else [round(b[0] * sx, 1), round(b[1] * sy, 1), round(b[2] * sx, 1), round(b[3] * sy, 1)]
             for b in res[nm]] for nm in names},
        "keyframes": {str(k): det.get(k, {}) for k in keys}}
    json.dump(out, open(a.out, "w", encoding="utf-8"))
    if a.preview:
        vw = cv2.VideoWriter(a.preview, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))
        cols = [(80, 255, 140), (255, 180, 60), (60, 120, 255), (255, 80, 200), (200, 255, 60)]
        for t, f in enumerate(frames):
            v = f.copy()
            for c, nm in enumerate(names):
                b = res[nm][t]
                if b is None:
                    continue
                cv2.rectangle(v, (int(b[0]), int(b[1])), (int(b[2]), int(b[3])), cols[c % 5], 2)
                cv2.putText(v, nm, (int(b[0]), int(b[1]) - 6), cv2.FONT_HERSHEY_SIMPLEX, 0.5, cols[c % 5], 1)
            if t in keys:
                cv2.putText(v, "KEY", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2)
            vw.write(v)
        vw.release()
    vis = {nm: sum(b is not None for b in out["objects"][nm]) for nm in names}
    print("visible frames per object:", vis)


if __name__ == "__main__":
    main()
