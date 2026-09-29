"""Check this machine for everything ai-video-titles needs, then say which pipeline steps are available.

python scripts/doctor.py            (no network calls except `npx hyperframes --version`, which may download the CLI once)
"""
import importlib
import os
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
SKILL = HERE.parent
SKILLS = SKILL.parent
if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
sys.path.insert(0, str(HERE))
import paths  # noqa: E402

OK, NO, OPT = "OK  ", "MISS", "opt "
res = {}


def line(tag, name, note=""):
    print(f"  [{tag}] {name}" + (f"  - {note}" if note else ""))


def run(cmd, timeout=180):
    try:
        r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=timeout, encoding="utf-8", errors="replace")
        return r.returncode, (r.stdout or r.stderr or "").strip()
    except Exception as ex:  # noqa: BLE001
        return 1, str(ex)


print("ai-video-titles doctor\n")
print("Python")
v = sys.version_info
res["python"] = v >= (3, 10)
line(OK if res["python"] else NO, f"python {v.major}.{v.minor}.{v.micro}", "" if res["python"] else "needs 3.10+")
for mod, pip, key in (("cv2", "opencv-python", "cv2"), ("numpy", "numpy", "numpy"), ("scipy", "scipy", "scipy"),
                      ("librosa", "librosa", "librosa"), ("google.genai", "google-genai", "genai")):
    try:
        importlib.import_module(mod)
        res[key] = True
        line(OK, pip)
    except Exception:  # noqa: BLE001
        res[key] = False
        line(NO, pip, "pip install -r requirements.txt")

print("\nTools")
res["ffmpeg"] = bool(shutil.which("ffmpeg")) and bool(shutil.which("ffprobe"))
line(OK if res["ffmpeg"] else NO, "ffmpeg + ffprobe", "" if res["ffmpeg"] else "install ffmpeg and put it on PATH")
res["node"] = bool(shutil.which("node")) and bool(shutil.which("npx"))
nv = run("node --version")[1] if res["node"] else ""
line(OK if res["node"] else NO, f"node / npx {nv}", "" if res["node"] else "install Node.js 18+")
res["hf"] = False
if res["node"]:
    code, out = run(f"npx -y {paths.HF} --version", timeout=300)
    res["hf"] = code == 0
    line(OK if res["hf"] else NO, f"npx {paths.HF} --version -> {out.splitlines()[-1] if out else ''}", "" if res["hf"] else out[-200:])

print("\nKeys")


def key(names, required, why):
    have = next((n for n in names if os.environ.get(n)), None)
    line(OK if have else (NO if required else OPT), " / ".join(names), (f"set ({have})" if have else "not set") + f" - {why}")
    return bool(have)


res["gemini"] = key(["GEMINI_API_KEY"], True, "tracking (vtrack.py), AI voice (gemini-tts), QA (qa.py)")
res["eleven"] = key(["ELEVEN_API_KEY", "ELEVENLABS_API_KEY"], False, "music beds + new sound effects (a UI/impact library ships with the kit)")
res["openai"] = key(["OPENAI_API_KEY"], False, "start frames / product stills with GPT Image")
res["kie"] = key(["KIE_API_KEY"], False, "generating the video itself with Seedance 2.5")

print("\nSibling skills (in " + str(SKILLS) + ")")
for s, why in (("hyperframes", "HTML-to-video engine docs"), ("seedance-2-prompt-engineer", "writing the Seedance prompt"),
               ("seedance-make-video", "generating the Seedance plate"), ("gemini-tts", "AI voiceover"), ("elevenlabs", "music / SFX helpers")):
    have = (SKILLS / s / "SKILL.md").exists()
    res["skill_" + s] = have
    line(OK if have else OPT, s, why)

print("\nBundled")
fonts_n = len(list(paths.fonts().glob("*.woff2")))
sfx_n = len(list((SKILL / "assets" / "sfx").glob("*.mp3")))
demo = (SKILL / "examples" / "demo" / "runway_demo_720p.mp4").exists()
line(OK if fonts_n else NO, f"{fonts_n} fonts"); line(OK if sfx_n else NO, f"{sfx_n} UI/impact sounds"); line(OK if demo else NO, "demo clip + track")

core = res["python"] and res["ffmpeg"] and res["node"] and res["hf"] and res["cv2"] and res["numpy"]
steps = [
    ("Render the bundled demo (no keys)", core and demo),
    ("Build + render any catalog style on a clip you already have tracked", core),
    ("Track objects frame by frame (vtrack.py)", core and res["genai"] and res["scipy"] and res["gemini"]),
    ("Planar tracking for maps / facades (track.py)", core),
    ("Beat grid + voice word timing (librosa)", res["librosa"]),
    ("AI voiceover (vo_take2.py via gemini-tts)", res["gemini"] and res["skill_gemini-tts"] and res["ffmpeg"]),
    ("Music beds + new SFX (ElevenLabs)", res["eleven"]),
    ("Gemini QA of a render (qa.py)", res["genai"] and res["gemini"]),
    ("Generate the video plate (Seedance 2.5 via kie)", res["kie"] and res["skill_seedance-make-video"]),
]
print("\nPipeline steps available")
for name, ok in steps:
    line(OK if ok else "----", name)
if not core:
    print("\nCore is missing: fix the MISS lines above first.")
sys.exit(0 if core else 1)
