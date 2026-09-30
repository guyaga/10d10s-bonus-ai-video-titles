"""--demo mode: run any run_style style on the footage that ships with the skill (examples/demo), no plates, no keys.

The catalog examples were built on plates that are not in git (Seedance/Kling clips). demo.prepare() rewrites a copy of
the style's example spec so it builds anywhere:
  * clip / after / video tiles  -> the bundled 8 s runway clip, looped to the style's own length (so its timing survives)
  * track                       -> a synthetic track: the demo's tracked "model" box, plus every object name the spec
                                   refers to, derived from it (face/eyes = head, boots = feet, jacket = torso, host_right =
                                   mirrored model ...) or, for places/points, a fixed documented anchor on screen
  * music                       -> the bundled demo bed;  vo / matte are dropped (the builders degrade gracefully)
  * words (word-timing files)   -> a placeholder line timed at a natural speaking pace
  * missing images              -> a bundled product still
The result shows the style's motion on neutral footage. It is a preview of the grammar, not the look on your subject.
"""
import json
import subprocess
from pathlib import Path

import paths

DEMO = paths.SKILL / "examples" / "demo"
CLIP = DEMO / "runway_demo_720p.mp4"
TRACK = DEMO / "runway_demo_vtrack.json"
MUSIC = DEMO / "music_demo.mp3"
IMAGE = next(iter(sorted((DEMO / "items").glob("*.webp"))), None) if (DEMO / "items").is_dir() else None
VIDEO_EXT = (".mp4", ".mov", ".webm", ".m4v")
IMAGE_EXT = (".png", ".jpg", ".jpeg", ".webp", ".svg")
TIME_KEYS = {"t", "at", "until", "end", "start", "s", "e", "t0", "t1", "time", "impact", "lock", "fire", "hold_until"}
PLACEHOLDER = {"he": "זה הדמו של הכתוביות שלך בסגנון שבחרת, על הסרטון שלך זה ייראה מדויק",
               "en": "This is a preview of the style you picked, on your own footage it will fit your words"}
# fixed anchors for tracked places/points the demo clip does not contain (documented in TESTING.md)
# two rows, 650 px apart: a label beside one anchor never reaches the next
ANCHORS = [(250, 330), (900, 330), (1550, 330), (250, 760), (900, 760), (1550, 760), (575, 545), (1225, 545)]


def _walk(o, key=None):
    if isinstance(o, dict):
        for k, v in o.items():
            yield from _walk(v, k)
    elif isinstance(o, list):
        for v in o:
            yield from _walk(v, key)
    else:
        yield key, o


def est_duration(spec):
    """The style's own length: the latest time the spec schedules anything (+ a tail), clamped to 8..30 s."""
    top = 0.0
    bpm = (spec.get("beat") or {}).get("bpm") if isinstance(spec.get("beat"), dict) else None
    off = (spec.get("beat") or {}).get("offset", 0) if isinstance(spec.get("beat"), dict) else 0
    for k, v in _walk(spec):
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            if k in TIME_KEYS:
                top = max(top, float(v))
            elif k == "beat" and bpm:
                top = max(top, off + 60 / bpm * v)
    return max(8.0, min(30.0, round(top + 2.5)))


def _region(name, B, idx, route):
    x0, y0, x1, y1 = B
    w, h = x1 - x0, y1 - y0
    n = name.lower()
    has = lambda *ks: any(k in n for k in ks)  # noqa: E731
    if name in route:                                  # a road/route: points spread along an arc across the frame
        i, m = route.index(name), max(1, len(route) - 1)
        u = i / m
        cx, cy = 200 + 1520 * u, 860 - 560 * u + 180 * (4 * u * (1 - u))
        return [cx - 40, cy - 30, cx + 40, cy + 30], False
    if has("eye"):
        return [x0 + .33 * w, y0 + .05 * h, x1 - .33 * w, y0 + .09 * h], False
    if has("face", "head"):
        return [x0 + .28 * w, y0, x1 - .28 * w, y0 + .13 * h], False
    if has("boot", "shoe", "sneaker", "feet", "foot"):
        return [x0 + .2 * w, y1 - .07 * h, x1 - .2 * w, y1], False
    if has("leg", "trouser", "pant", "cargo", "skirt", "jean"):
        return [x0 + .15 * w, y0 + .5 * h, x1 - .15 * w, y1 - .08 * h], False
    if has("bag", "tote", "bud", "case", "phone", "hand", "cup", "bottle", "ball"):
        return [x1 - .25 * w, y0 + .45 * h, x1, y0 + .6 * h], False
    if has("jacket", "coat", "top", "shirt", "knit", "torso", "chest", "trench", "dress"):
        return [x0, y0 + .15 * h, x1, y0 + .5 * h], False
    if has("right", "_2", "second", "guest"):         # the second person: the model shifted to the right third
        cx = (x0 + x1) / 2
        return [x0 - cx + 1340, y0, x1 - cx + 1340, y1], False
    if has("left", "_1", "first"):                    # the first person: the model shifted to the left third
        cx = (x0 + x1) / 2
        return [x0 - cx + 580, y0, x1 - cx + 580, y1], False
    if has("model", "player", "host", "person", "subject", "singer", "speaker", "talent", "athlete"):
        return list(B), False
    cx, cy = ANCHORS[idx % len(ANCHORS)]
    return [cx - 60, cy - 45, cx + 60, cy + 45], True   # static anchor


def synth_track(names, route, frames, out):
    src = json.loads(TRACK.read_text(encoding="utf-8"))
    model = src["objects"]["model"]
    n_src = len(model)
    objs, static = {}, []
    for idx, name in enumerate(dict.fromkeys(["model", *names])):
        seq = []
        for f in range(frames):
            B = model[f % n_src] or next(b for b in model if b)
            r, st = _region(name, B, idx, route)
            seq.append([round(v, 1) for v in r])
        objs[name] = seq
        if st:
            static.append(name)
    out.write_text(json.dumps({"fps": 24.0, "frames": frames, "canvas": [1920, 1080], "objects": objs}), encoding="utf-8")
    return static


def loop_clip(dur, out):
    if not out.exists():
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-stream_loop", "-1", "-i", str(CLIP), "-t", f"{dur:.2f}",
                        "-c:v", "libx264", "-preset", "veryfast", "-crf", "22", "-pix_fmt", "yuv420p", "-r", "24",
                        "-c:a", "aac", "-b:a", "128k", str(out)], check=True)
    return out


def placeholder_words(lang, out, start=.6):
    t, W = start, []
    for w in PLACEHOLDER.get(lang, PLACEHOLDER["en"]).split():
        W.append({"w": w, "t": round(t, 2), "s": round(t, 2), "e": round(t + .3, 2)})
        t += .38 if len(w) > 3 else .3
    out.write_text(json.dumps(W, ensure_ascii=False), encoding="utf-8")
    return out


def prepare(style, spec, base, needed):
    """Return (demo_spec, notes). All paths in demo_spec are absolute."""
    from styles.common import res
    work = paths.root() / "demo_assets" / style.lower()
    work.mkdir(parents=True, exist_ok=True)
    spec = json.loads(json.dumps(spec))            # deep copy
    dur = est_duration(spec)
    clip = loop_clip(dur, work / f"demo_{int(dur)}s.mp4")
    notes = [f"demo footage: the bundled runway clip looped to {dur:.0f} s (the style's own length)"]
    spec["clip"] = str(clip)
    spec["name"] = f"demo-{style.lower()}"
    if "after" in spec:
        spec["after"] = str(clip)
    for k in ("vo", "matte", "audio"):
        if spec.pop(k, None):
            notes.append(f"{k} dropped for the demo")
    if spec.get("music"):
        spec["music"] = str(MUSIC)
    if isinstance(spec.get("words"), str):          # a word-timing file (viral captions): a placeholder line
        spec["words"] = str(placeholder_words(spec.get("language", "en"), work / "words.json"))
        notes.append("words: a placeholder line (use scripts/word_times.py or a transcript for real timings)")

    def fix_media(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if isinstance(v, str) and v.lower().endswith(VIDEO_EXT + IMAGE_EXT) and k not in ("clip", "after", "track", "words"):
                    if not res(base, v).exists():
                        o[k] = str(clip) if v.lower().endswith(VIDEO_EXT) else (str(IMAGE) if IMAGE else v)
                else:
                    fix_media(v)
        elif isinstance(o, list):
            for v in o:
                fix_media(v)
    fix_media(spec)
    route = [r for r in spec.get("route", []) if isinstance(r, str)]
    if needed or spec.get("track"):
        tr = work / "track.json"
        static = synth_track(needed, route, int(round(dur * 24)), tr)
        spec["track"] = str(tr)
        derived = [n for n in needed if n not in static and n != "model"]
        if derived:
            notes.append(f"tracked objects derived from the demo model box: {', '.join(derived)}")
        if static:
            notes.append(f"tracked places pinned to fixed demo anchors: {', '.join(static)}")
    return spec, notes
