"""Planar camera tracker: follow anchor points through a clip via chained RANSAC homographies.

Usage:
  python track.py clip.mp4 anchors.json out.json [--canvas 1920x1080] [--preview preview.mp4]

anchors.json: {"points": {"name": [x, y], ...}}  in FRAME-0 pixel coords of the clip
out.json:     {"fps":24, "frames":N, "canvas":[W,H], "points": {"name": [[x,y], ...per frame]}}
              coordinates rescaled to the canvas size (composition pixels).

Good for aerial / planar scenes (map fly-overs, walls, floors). Uses LK optical flow on
Shi-Tomasi corners, re-seeded every frame, homography frame(t-1)->frame(t) accumulated.
"""
import argparse
import json

import cv2
import numpy as np


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("clip")
    ap.add_argument("anchors")
    ap.add_argument("out")
    ap.add_argument("--canvas", default="1920x1080")
    ap.add_argument("--preview")
    ap.add_argument("--mask-top", type=float, default=0.0, help="ignore features in the top fraction (sky)")
    ap.add_argument("--mask-bottom", type=float, default=0.0,
                    help="ignore features in the bottom fraction of frame (e.g. a foreground subject)")
    a = ap.parse_args()

    cw, ch = map(int, a.canvas.split("x"))
    anchors = json.load(open(a.anchors, encoding="utf-8"))["points"]
    names = list(anchors)
    pts0 = np.array([anchors[n] for n in names], np.float32).reshape(-1, 1, 2)

    cap = cv2.VideoCapture(a.clip)
    fps = cap.get(cv2.CAP_PROP_FPS) or 24
    ok, frame = cap.read()
    if not ok:
        raise SystemExit("cannot read clip")
    h, w = frame.shape[:2]
    sx, sy = cw / w, ch / h
    prev = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask = np.full(prev.shape, 255, np.uint8)
    if a.mask_top:
        mask[: int(h * a.mask_top), :] = 0
    if a.mask_bottom:
        mask[int(h * (1 - a.mask_bottom)):, :] = 0

    H = np.eye(3)
    track = {n: [] for n in names}
    writer = None
    if a.preview:
        writer = cv2.VideoWriter(a.preview, cv2.VideoWriter_fourcc(*"mp4v"), fps, (w, h))

    def record(img):
        cur = cv2.perspectiveTransform(pts0, H).reshape(-1, 2)
        for n, (x, y) in zip(names, cur):
            track[n].append([round(float(x * sx), 2), round(float(y * sy), 2)])
        if writer is not None:
            vis = img.copy()
            for n, (x, y) in zip(names, cur):
                cv2.circle(vis, (int(x), int(y)), 7, (80, 255, 140), 2)
                cv2.putText(vis, n, (int(x) + 9, int(y) - 9), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (80, 255, 140), 1)
            writer.write(vis)

    record(frame)
    n_frames, inlier_log = 1, []
    while True:
        ok, frame = cap.read()
        if not ok:
            break
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p0 = cv2.goodFeaturesToTrack(prev, maxCorners=1500, qualityLevel=0.01, minDistance=8, mask=mask)
        step = np.eye(3)
        if p0 is not None and len(p0) >= 8:
            p1, st, _ = cv2.calcOpticalFlowPyrLK(prev, gray, p0, None, winSize=(21, 21), maxLevel=4)
            good0, good1 = p0[st == 1], p1[st == 1]
            if len(good0) >= 8:
                Hs, inl = cv2.findHomography(good0, good1, cv2.RANSAC, 2.0)
                if Hs is not None:
                    step = Hs
                    inlier_log.append(int(inl.sum()))
        H = step @ H
        record(frame)
        prev = gray
        n_frames += 1

    if writer is not None:
        writer.release()
    out = {"fps": fps, "frames": n_frames, "canvas": [cw, ch], "source": [w, h], "points": track}
    json.dump(out, open(a.out, "w", encoding="utf-8"))
    print(f"tracked {len(names)} points over {n_frames} frames @ {fps:.2f}fps; "
          f"median inliers {int(np.median(inlier_log)) if inlier_log else 0}")


if __name__ == "__main__":
    main()
