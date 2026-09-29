"""Render a HyperFrames project at 24 fps, optionally append an end sting, loudness-normalise to -16 LUFS.

python finalize.py <project_dir> <out_name> [--sting sting.mp4] [--root DIR]
-> <root>/renders/<out_name>.mp4 (+ renders/preview/<out_name>_preview.mp4 when the master is over 29 MB, for chat apps)
"""
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import paths  # noqa: E402


def run(cmd, **kw):
    return subprocess.run(cmd, check=True, **kw)


def main(project, name, sting=None):
    project = Path(project)
    R = paths.root()
    (R / "renders").mkdir(exist_ok=True)
    pj = project / "package.json"
    if pj.exists():
        pj.write_text(re.sub(r"hyperframes@\d+\.\d+\.\d+", paths.HF, pj.read_text(encoding="utf-8")), encoding="utf-8")
    raw = R / f"renders/_{name}_raw.mp4"
    r = subprocess.run(f'npx -y {paths.HF} render --fps 24 --workers 4 -o "{raw}"', cwd=project, shell=True,
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0 or not raw.exists():
        log = ((r.stdout or "") + (r.stderr or "")).replace("\r", "\n")
        tail = [ln for ln in log.splitlines() if ln.strip()][-12:]
        raise SystemExit("hyperframes render failed:\n" + "\n".join(tail))
    out = R / f"renders/{name}.mp4"
    if sting:
        fc = ("[0:v]fps=24,scale=1920:1080,setsar=1[v0];[1:v]fps=24,scale=1920:1080,setsar=1[v1];"
              "[0:a]aresample=48000,aformat=channel_layouts=stereo[a0];[v0][a0][v1][2:a]concat=n=2:v=1:a=1[v][a];"
              "[a]loudnorm=I=-16:TP=-1.5:LRA=11[an]")
        ins = ["-i", str(raw), "-i", str(sting), "-f", "lavfi", "-t", "1.5", "-i", "anullsrc=r=48000:cl=stereo"]
        maps = ["-map", "[v]", "-map", "[an]"]
    else:
        fc = "[0:a]loudnorm=I=-16:TP=-1.5:LRA=11[an]"
        ins = ["-i", str(raw)]
        maps = ["-map", "0:v", "-map", "[an]"]
    run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", fc, *maps,
         "-c:v", "libx264", "-crf", "17", "-preset", "slow", "-pix_fmt", "yuv420p",
         "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-movflags", "+faststart", str(out)])
    raw.unlink(missing_ok=True)
    mb = out.stat().st_size / 1e6
    if mb > 29:
        prev = R / f"renders/preview/{name}_preview.mp4"
        prev.parent.mkdir(exist_ok=True)
        run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(out), "-c:v", "libx264", "-b:v", "7000k", "-maxrate", "8000k",
             "-bufsize", "12M", "-preset", "slow", "-c:a", "copy", "-movflags", "+faststart", str(prev)])
        print(f"{out} ({mb:.1f} MB) + preview {prev}")
    else:
        print(f"{out} ({mb:.1f} MB)")


if __name__ == "__main__":
    argv = paths.take_root_arg(sys.argv)
    st = argv[argv.index("--sting") + 1] if "--sting" in argv else None
    main(argv[1], argv[2], st)
