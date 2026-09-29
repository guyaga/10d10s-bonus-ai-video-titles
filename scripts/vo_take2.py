"""Generate + mix a timed voiceover from per-line TTS. python vo_take2.py <AD> <lines.json> [variant] [--root DIR]
lines.json: {"voice": "ora|trailer|Charon|Sulafat|Leda|Algenib|Kore|Puck|Orus|... or a designed alias",
             "lines": [{"id": "l1", "start": 0.5, "text": "...", "style": "..."}], "total": 18.0}
Writes <root>/voice/<variant>_<AD>_<id>_t.wav and <root>/shared/sfx/<AD>_<variant>_vo.mp3; prints each line's end time and any overlap.
Needs the gemini-tts skill (override its script path with env GEMINI_TTS_SCRIPT)."""
import os
import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402

sys.argv = paths.take_root_arg(sys.argv)
R = paths.root()
V = R / "voice"
V.mkdir(exist_ok=True)
TTS = os.environ.get("GEMINI_TTS_SCRIPT") or str(Path.home() / ".claude/skills/gemini-tts/scripts/gemini_tts.py")
TRIM = ("silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.02,areverse,"
        "silenceremove=start_periods=1:start_threshold=-45dB:start_silence=0.05,areverse")


def dur(p):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(p)],
                                capture_output=True, text=True).stdout.strip())


ad, spec = sys.argv[1], json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
VAR = sys.argv[3] if len(sys.argv) > 3 else "t2"
ins, fil, lab, ends = [], [], [], []
for i, ln in enumerate(spec["lines"]):
    w, tw = V / f"{VAR}_{ad}_{ln['id']}.wav", V / f"{VAR}_{ad}_{ln['id']}_t.wav"
    subprocess.run([sys.executable, TTS, "speak", ln["text"], "--voice", spec["voice"], "--style", ln.get("style", "natural"), "-o", str(w)],
                   capture_output=True, text=True, check=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(w), "-af", TRIM, str(tw)], check=True)
    d = dur(tw)
    ends.append((ln["id"], ln["start"], ln["start"] + d))
    ins += ["-i", str(tw)]
    fil.append(f"[{i}]adelay={int(ln['start'] * 1000)}:all=1[a{i}]")
    lab.append(f"[a{i}]")
total = spec["total"]
fil.append(f"{''.join(lab)}amix=inputs={len(lab)}:normalize=0,highpass=f=60,acompressor=threshold=-18dB:ratio=3:attack=5:release=90,"
           f"volume=1.5,alimiter=limit=0.95,apad=whole_dur={total + .5},atrim=0:{total + .5}")
out = paths.sfx_cache() / f"{ad}_{VAR}_vo.mp3"
subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fil), "-ar", "48000", "-ac", "2", "-b:a", "256k", str(out)], check=True)
for (a, s, e), nxt in zip(ends, ends[1:] + [(None, total, None)]):
    flag = "  OVERLAP" if e > nxt[1] else ""
    print(f"{a}: {s:.2f} -> {e:.2f}{flag}")
print("wrote", out)
