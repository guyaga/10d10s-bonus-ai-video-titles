"""E7 bespoke: builds the jeweller's-loupe sprite - ONE loupe that travels watch -> bracelet -> rings (3.08s-8.75s).
Magnified, stabilised crops follow a detail point on each piece; between pieces the source point glides (so the glass
shows whatever passes under it, like a real loupe). The loupe's on-screen centre is the detail point clamped to a safe
area (a fine leader line joins them when they differ).
Writes tools/E7_gold_bespoke_loupe.jpg (tiled) + tools/E7_gold_bespoke_loupe.json (frame range, source + display centres, piece weights)."""
import json
import subprocess
from pathlib import Path

import numpy as np
from PIL import Image, ImageFilter

T = Path(__file__).resolve().parent
CLIP = T.parent / "E_ads/clips/E7_gold_720p.mp4"
F0, F1 = 74, 211
# (obj, fx, fy, first frame, last frame) - glides fill the gaps
SEGS = [("watchface", .50, .52, 74, 104), ("bracelet", .47, .24, 113, 136), ("ringstack", .54, .34, 154, 210)]
CROP = 120                 # source px (1280x720) -> ~2.3x at 420 px
OUT = 420
COLS = 8
SAFE = (270, 1650, 262, 818)   # display-centre clamp (x0, x1, y0, y1) in 1920x1080

trk = json.loads((T / "E7_gold_vtrack.json").read_text())["objects"]


def pt(obj, fx, fy, f):
    b = trk[obj][f]
    if not b:
        return None
    return b[0] + (b[2] - b[0]) * fx, b[1] + (b[3] - b[1]) * fy


def sm(u):
    u = min(max(u, 0), 1)
    return u * u * (3 - 2 * u)


K = 7
pad = lambda a: np.pad(np.array(a, float), (K // 2, K // 2), mode="edge")  # noqa: E731
smooth = lambda a: np.convolve(pad(a), np.ones(K) / K, mode="valid")  # noqa: E731

# smooth each piece's detail track on its own (so smoothing never leaks across a glide), then blend
TR = []
for (o, fx, fy, a0, b0) in SEGS:
    pts = [pt(o, fx, fy, f) for f in range(F0, F1)]
    last = next(p for p in pts if p)
    fill = []
    for p in pts:
        last = p or last
        fill.append(last)
    TR.append((smooth([p[0] for p in fill]), smooth([p[1] for p in fill])))

sx, sy, wts = [], [], []
for i, f in enumerate(range(F0, F1)):
    w = [0.0, 0.0, 0.0]
    for k, (o, fx, fy, a0, b0) in enumerate(SEGS):
        if a0 <= f <= b0:
            w[k] = 1
            break
    else:
        k = next(j for j in range(len(SEGS) - 1) if SEGS[j][4] < f < SEGS[j + 1][3])
        u = sm((f - SEGS[k][4]) / (SEGS[k + 1][3] - SEGS[k][4]))
        w[k], w[k + 1] = 1 - u, u
    sx.append(sum(w[k] * TR[k][0][i] for k in range(3)))
    sy.append(sum(w[k] * TR[k][1][i] for k in range(3)))
    wts.append([round(v, 3) for v in w])
sx, sy = np.array(sx), np.array(sy)
dx = smooth(np.clip(sx, SAFE[0], SAFE[1]))
dy = smooth(np.clip(sy, SAFE[2], SAFE[3]))

raw = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", str(CLIP), "-f", "rawvideo", "-pix_fmt", "rgb24", "-"], capture_output=True, check=True).stdout
frames = np.frombuffer(raw, np.uint8).reshape(-1, 720, 1280, 3)
n = F1 - F0
rows = (n + COLS - 1) // COLS
sheet = Image.new("RGB", (COLS * OUT, rows * OUT))
for i, f in enumerate(range(F0, F1)):
    im = Image.fromarray(frames[f])
    x, y = sx[i] / 1.5, sy[i] / 1.5
    x = min(max(x, CROP / 2), 1280 - CROP / 2)
    y = min(max(y, CROP / 2), 720 - CROP / 2)
    c = im.crop((int(x - CROP / 2), int(y - CROP / 2), int(x - CROP / 2) + CROP, int(y - CROP / 2) + CROP))
    c = c.resize((OUT, OUT), Image.LANCZOS).filter(ImageFilter.UnsharpMask(radius=2, percent=70, threshold=2))
    sheet.paste(c, ((i % COLS) * OUT, (i // COLS) * OUT))
sheet.save(T / "E7_gold_bespoke_loupe.jpg", quality=86)
(T / "E7_gold_bespoke_loupe.json").write_text(json.dumps({
    "f0": F0, "n": n, "cols": COLS, "size": OUT, "rows": rows,
    "sx": [round(v, 1) for v in sx], "sy": [round(v, 1) for v in sy],
    "cx": [round(v, 1) for v in dx], "cy": [round(v, 1) for v in dy], "w": wts}))
print("sprite", sheet.size, n)
