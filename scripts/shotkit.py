"""Shot builder: tracked-overlay HyperFrames composition + ElevenLabs SFX mix for one Seedance clip.

A shot module calls build(...) with:
  shot      id, e.g. "B3"
  clip      path to the Seedance mp4
  track     path to the vtrack json (per-frame boxes from Gemini keyframes + optical flow)
  css       shot CSS (fonts/palette/base classes already included)
  hud       HUD markup. Tracking hooks:
              data-follow="obj" data-anchor="c|t|b|l|r|tl|tr|bl|br" [data-dx data-dy]
                 -> element translated to that anchor of the object's box every frame
              data-box="obj" [data-pad="12"]  -> element's left/top/width/height = the box (+pad)
            Elements hold the last known position while their object is not visible.
  js        GSAP entrance/exit tweens on `tl` (driver tween is added automatically)
  sfx       list of (name, prompt, seconds, at_time, volume) -> generated (cached) + mixed.
            If `name` is a path to an existing audio file (music bed, VO) it is mixed as-is, nothing is generated.
  plate_vol volume of Seedance's native ambience
"""
import json
import os
import subprocess
import urllib.error
import urllib.request
from pathlib import Path

import hfkit
import paths

BASE_CSS = r"""
:root{--fg:#eef4e8;--mute:#b9c7b0;--acc:#9bd14a;--warn:#ff5a4f;--panel:rgba(7,13,9,.8);--line:rgba(155,209,74,.6)}
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1920px;height:1080px;overflow:hidden;background:#070b08}
#root{position:relative;width:100%;height:100%;overflow:hidden;font-family:"Assistant",sans-serif;color:var(--fg)}
#plate{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.layer{position:absolute;inset:0}
.mono{font-family:"JetBrains Mono",monospace}
.he{font-family:"Assistant",sans-serif;direction:rtl;unicode-bidi:isolate}
[data-follow]{position:absolute;left:0;top:0;width:0;height:0}
[data-follow].panel{width:max-content;height:auto}
[data-box]{position:absolute}
.panel{background:var(--panel);border-radius:6px}
.tick{position:absolute;width:44px;height:44px;border-color:rgba(238,244,232,.55);border-style:solid}
.tk1{left:48px;top:48px;border-width:2px 0 0 2px}.tk2{right:48px;top:48px;border-width:2px 2px 0 0}
.tk3{left:48px;bottom:48px;border-width:0 0 2px 2px}.tk4{right:48px;bottom:48px;border-width:0 2px 2px 0}
.brk{position:absolute;inset:0}
.brk i{position:absolute;width:26px;height:26px;border-color:var(--acc);border-style:solid}
.brk i:nth-child(1){left:0;top:0;border-width:3px 0 0 3px}.brk i:nth-child(2){right:0;top:0;border-width:3px 3px 0 0}
.brk i:nth-child(3){left:0;bottom:0;border-width:0 0 3px 3px}.brk i:nth-child(4){right:0;bottom:0;border-width:0 3px 3px 0}
"""

DRIVER_JS = r"""
const $ = (s) => document.querySelector(s);
const fi = (t) => Math.max(0, Math.min(D.n - 1, Math.round(t * D.fps)));
function boxAt(name, t) {
  const arr = D.obj[name]; if (!arr) return null;
  let i = fi(t);
  for (let k = i; k >= 0; k--) if (arr[k]) return arr[k];
  for (let k = i; k < arr.length; k++) if (arr[k]) return arr[k];
  return null;
}
function anchor(b, a) {
  const cx = (b[0] + b[2]) / 2, cy = (b[1] + b[3]) / 2;
  return { c: [cx, cy], t: [cx, b[1]], b: [cx, b[3]], l: [b[0], cy], r: [b[2], cy],
           tl: [b[0], b[1]], tr: [b[2], b[1]], bl: [b[0], b[3]], br: [b[2], b[3]] }[a || "c"];
}
const FOL = [...document.querySelectorAll("[data-follow]")];
const BOX = [...document.querySelectorAll("[data-box]")];
function place(t) {
  for (const el of FOL) {
    const b = boxAt(el.dataset.follow, t); if (!b) continue;
    const p = anchor(b, el.dataset.anchor);
    el.style.left = (p[0] + (+el.dataset.dx || 0)) + "px"; el.style.top = (p[1] + (+el.dataset.dy || 0)) + "px";
  }
  for (const el of BOX) {
    const b = boxAt(el.dataset.box, t); if (!b) continue;
    const pad = +el.dataset.pad || 0;
    el.style.left = (b[0] - pad) + "px"; el.style.top = (b[1] - pad) + "px";
    el.style.width = (b[2] - b[0] + 2 * pad) + "px"; el.style.height = (b[3] - b[1] + 2 * pad) + "px";
  }
  if (window.onPlace) window.onPlace(t);
}
const tl = gsap.timeline({ paused: true });
const drv = { t: 0 };
tl.to(drv, { t: DUR, duration: DUR, ease: "none", onUpdate: () => place(drv.t) }, 0);
"""

TEMPLATE = """<!doctype html>
<html lang="en">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=1920, height=1080" />
<script src="https://cdn.jsdelivr.net/npm/gsap@3.14.2/dist/gsap.min.js"></script>
<style>
__FONTS__
__BASE__
__CSS__
</style>
</head>
<body>
<div id="root" data-composition-id="main" data-start="0" data-duration="__DUR__" data-width="1920" data-height="1080">
  <video id="plate" class="clip" src="assets/plate.mp4" data-start="0" data-duration="__DUR__" data-track-index="0" muted playsinline></video>
  <audio id="plate-audio" src="assets/plate.mp4" data-start="0" data-duration="__DUR__" data-track-index="10" data-volume="__PVOL__"></audio>
  <audio id="sfx" src="assets/sfx.wav" data-start="0" data-duration="__DUR__" data-track-index="11" data-volume="1"></audio>
__HUDBLOCK__
</div>
<script>
const D = __DATA__;
const DUR = __DUR__;
__DRIVER__
__JS__
place(0);
window.__timelines["main"] = tl;
</script>
</body>
</html>
"""


def eleven_sfx(name, prompt, seconds):
    """ElevenLabs sound-generation with a disk cache (<root>/shared/sfx/<name>.mp3) and 429 back-off."""
    if Path(str(name)).suffix and Path(name).exists():
        return Path(name)
    out = paths.sfx_cache() / f"{name}.mp3"
    if out.exists():
        return out
    bundled = paths.SKILL / "assets" / "sfx" / f"{name}.mp3"   # the kit ships its UI/impact library: no API call needed
    if bundled.exists():
        return bundled
    if not os.environ.get("ELEVEN_API_KEY") and os.environ.get("ELEVENLABS_API_KEY"):
        os.environ["ELEVEN_API_KEY"] = os.environ["ELEVENLABS_API_KEY"]
    if not os.environ.get("ELEVEN_API_KEY"):
        raise SystemExit(f"sfx '{name}' is not cached or bundled and ELEVEN_API_KEY is not set")
    body = json.dumps({"text": prompt, "duration_seconds": seconds, "prompt_influence": 0.6}).encode()
    for attempt in range(4):
        req = urllib.request.Request("https://api.elevenlabs.io/v1/sound-generation", data=body, method="POST",
                                     headers={"xi-api-key": os.environ["ELEVEN_API_KEY"], "Content-Type": "application/json"})
        try:
            out.write_bytes(urllib.request.urlopen(req, timeout=120).read())
            return out
        except urllib.error.HTTPError as e:
            if e.code == 429:
                import time
                time.sleep(4 * (attempt + 1))
                continue
            raise
    raise SystemExit(f"sfx failed: {name}")


def mix_sfx(cues, dur, out):
    ins, fil, labels = [], [], []
    for i, (name, prompt, secs, at, vol) in enumerate(cues):
        f = eleven_sfx(name, prompt, secs)
        ins += ["-i", str(f)]
        fil.append(f"[{i}]adelay={int(at * 1000)}:all=1,volume={vol}[a{i}]")
        labels.append(f"[a{i}]")
    fil.append(f"{''.join(labels)}amix=inputs={len(cues)}:normalize=0,alimiter=limit=0.9,apad=whole_dur={dur + 0.5},atrim=0:{dur + 0.5}")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", *ins, "-filter_complex", ";".join(fil),
                    "-ar", "48000", "-ac", "2", str(out)], check=True)


def has_audio(media):
    r = subprocess.run(["ffprobe", "-v", "error", "-select_streams", "a", "-show_entries", "stream=index", "-of", "csv=p=0", str(media)],
                       capture_output=True, text=True)
    return bool(r.stdout.strip())


def load_track(track):
    """vtrack.py output ({objects: {name: [box|None per frame]}}) or track.py output ({points: {name: [[x,y] per frame]}}).
    Points become zero-size boxes so data-follow / boxAt work the same for both. Both files may be merged by passing a list."""
    tracks = track if isinstance(track, (list, tuple)) else [track]
    out = None
    for tr in tracks:
        T = json.loads(Path(tr).read_text(encoding="utf-8"))
        if "points" in T and "objects" not in T:
            T["objects"] = {k: [[p[0], p[1], p[0], p[1]] if p else None for p in v] for k, v in T.pop("points").items()}
        if out is None:
            out = T
        else:
            out["objects"].update(T["objects"])
    return out


def build(shot, project, clip, track, css, hud, js, sfx, plate_vol=0.6, extra=None):
    project = Path(project)
    missing = [f"  {name} <- {src}" for name, src in (extra or {}).items() if not Path(src).exists()]
    if not Path(clip).exists():
        missing.insert(0, f"  plate <- {clip}")
    if missing:
        hint = ("\n  (text-behind-subject needs a matte: npx " + paths.HF + " remove-background clips/<AD>_720p.mp4 -o mattes/<AD>_alpha.webm)"
                if any("matte" in m for m in missing) else "")
        raise SystemExit(f"[{shot}] missing input files:\n" + "\n".join(missing) + hint)
    if not (project / "hyperframes.json").exists():
        # init refuses a non-empty dir: init first, copy assets after
        subprocess.run(["npx", "-y", paths.HF, "init", str(project), "--non-interactive",
                        "--example=blank", "--skill=general-video"], check=True, shell=True,
                       stdout=subprocess.DEVNULL)
    assets = project / "assets"
    assets.mkdir(exist_ok=True)
    hfkit.install_fonts(project)
    import shutil
    shutil.copy2(clip, assets / "plate.mp4")
    for name, src in (extra or {}).items():
        (assets / name).parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, assets / name)
    T = load_track(track)
    n, fps = T["frames"], T["fps"]
    dur = round(n / fps, 3)
    if sfx:
        mix_sfx(sfx, dur, assets / "sfx.wav")
    else:   # silent bed so the <audio> element always has a source
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "lavfi", "-t", str(dur + .5), "-i", "anullsrc=r=48000:cl=stereo", str(assets / "sfx.wav")], check=True)
    data = {"fps": fps, "n": n, "obj": T["objects"]}
    if "<!--MATTE-->" in hud:
        h1, h2 = hud.split("<!--MATTE-->", 1)
        NL = chr(10)
        block = ('  <div id="hud" class="clip layer" data-start="0" data-duration="__DUR__" data-track-index="1">' + NL + h1 + NL + '  </div>' + NL
                 + '  <video id="matte" class="clip" src="assets/matte.webm" data-start="0" data-duration="__DUR__" data-track-index="2" muted playsinline '
                 + 'style="position:absolute;inset:0;width:100%;height:100%;object-fit:cover"></video>' + NL
                 + '  <div id="hud2" class="clip layer" data-start="0" data-duration="__DUR__" data-track-index="3">' + NL + h2 + NL + '  </div>')
    else:
        block = ('  <div id="hud" class="clip layer" data-start="0" data-duration="__DUR__" data-track-index="1">' + chr(10) + hud + chr(10) + '  </div>')
    html = (TEMPLATE.replace("__HUDBLOCK__", block).replace("__FONTS__", hfkit.font_css()).replace("__BASE__", BASE_CSS)
            .replace("__CSS__", css).replace("__DRIVER__", DRIVER_JS)
            .replace("__JS__", js).replace("__DATA__", json.dumps(data, separators=(",", ":")))
            .replace("__DUR__", str(dur)).replace("__PVOL__", str(plate_vol)))
    if plate_vol <= 0 or not has_audio(assets / "plate.mp4"):   # a silent plate must not be authored as an audio source
        html = "\n".join(ln for ln in html.split("\n") if 'id="plate-audio"' not in ln)
    (project / "index.html").write_text(html, encoding="utf-8")
    print(f"[{shot}] index.html: {n} frames @ {fps} = {dur}s, {len(sfx)} sfx cues")
    return dur
