"""Where everything lives. Every script resolves paths through here, so the kit works in any project folder.

ROOT   the title project (default: current working directory; override with env TITLES_ROOT or a script's --root)
FONTS  woff2 font library (default: this skill's assets/fonts; override with env TITLES_FONTS)

Project layout convention under ROOT (each can also be overridden per spec):
  clips/<AD>_720p.mp4          the Seedance plate            spec["clip"]
  tracks/<AD>_vtrack.json      vtrack.py output              spec["track"]
  mattes/<AD>_alpha.webm       subject matte (text-behind)   spec["matte"]
  specs/<AD>[_<variant>].py    SPEC dicts for run_ad.py
  shared/sfx/                  audio cache: generated SFX, <AD>_music.mp3, <AD>[_<variant>]_vo.mp3
  voice/                       per-line TTS wavs (vo_take2.py / word_times.py)
  videos/<ad>[-<variant>]/     generated HyperFrames projects
  renders/                     finished mp4s
"""
import os
from pathlib import Path

SKILL = Path(__file__).resolve().parent.parent


def root() -> Path:
    return Path(os.environ.get("TITLES_ROOT") or os.getcwd()).resolve()


def fonts() -> Path:
    return Path(os.environ.get("TITLES_FONTS") or SKILL / "assets" / "fonts")


def sfx_cache() -> Path:
    p = root() / "shared" / "sfx"
    p.mkdir(parents=True, exist_ok=True)
    return p


def take_root_arg(argv):
    """Strip a `--root DIR` pair from argv and export it as TITLES_ROOT. Returns the cleaned argv."""
    if "--root" in argv:
        i = argv.index("--root")
        os.environ["TITLES_ROOT"] = str(Path(argv[i + 1]).resolve())
        argv = argv[:i] + argv[i + 2:]
    return argv


HF = "hyperframes@0.8.84"   # pinned: 0.8.85 was announced but never published to npm (ETARGET)
