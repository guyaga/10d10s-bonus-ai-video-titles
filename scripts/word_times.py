"""Word-level timings for a TTS voiceover built with vo_take2.py (one trimmed wav per line).
python word_times.py <AD> <lines.json> [variant] [--root DIR]  -> <root>/tracks/<AD>_<variant>_words.json
Run after vo_take2.py with the same AD/lines/variant (reads <root>/voice/<variant>_<AD>_<id>_t.wav).
Each word's start = its char-proportional position inside the line, snapped to the nearest real
speech onset (librosa onset detection on that line's audio). Good to ~40 ms for punchy reads."""
import json
import re
import sys
from pathlib import Path

import librosa
import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

sys.argv = paths.take_root_arg(sys.argv)
R = paths.root()
ad, lines_f, var = sys.argv[1], sys.argv[2], (sys.argv[3] if len(sys.argv) > 3 else "he")
spec = json.loads(Path(lines_f).read_text(encoding="utf-8"))
out = []
for ln in spec["lines"]:
    wav = R / f"voice/{var}_{ad}_{ln['id']}_t.wav"
    y, sr = librosa.load(str(wav), sr=22050)
    dur = len(y) / sr
    onsets = librosa.onset.onset_detect(y=y, sr=sr, units="time", backtrack=True)
    words = [w for w in re.split(r"\s+", ln["text"].strip()) if w]
    clean = [re.sub(r"[^\w֐-׿%]", "", w) or w for w in words]
    weights = np.array([max(1, len(c)) for c in clean], float)
    starts = np.concatenate([[0], np.cumsum(weights)[:-1]]) / weights.sum() * dur
    snapped = []
    for i, s in enumerate(starts):
        if i == 0:
            snapped.append(0.0)
            continue
        near = onsets[np.abs(onsets - s) < 0.18] if len(onsets) else []
        snapped.append(float(near[np.argmin(np.abs(near - s))]) if len(near) else float(s))
    for w, s in zip(words, snapped):
        out.append({"line": ln["id"], "w": w, "t": round(ln["start"] + s, 3)})
    out[-1]["line_end"] = round(ln["start"] + dur, 3)
dst = R / f"tracks/{ad}_{var}_words.json"
dst.parent.mkdir(exist_ok=True)
dst.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
for o in out:
    print(f'{o["t"]:6.2f}  {o["line"]}  {o["w"]}')
