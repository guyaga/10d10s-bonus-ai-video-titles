"""FLIP-MONTAGE-LOGO: the Marvel-style opener/closer. Frames pulled from the plate itself flip past as 3D pages on an
accelerating clock, tinted progressively towards the brand colour, then the last page falls away to reveal the
wordmark on a colour block, which settles with a light sweep. Frames are extracted with ffmpeg at build time; every
page angle is a pure function of t (deterministic).

Spec keys. Required: clip.
  t          when the montage starts (default: duration - 3.4 s);  dur: montage length before the logo (default 2.2)
  frames     how many plate frames to flip (default 18), sampled evenly (or "from"/"to" seconds of the plate);
             every page gets a seeded punch-in + treatment (mono / saturated / contrast) so one plate still reads as a montage
  logo       {"text": "NORTHLINE", "sub": "WINTER DROP 01", "image": "logo.png" (optional, replaces the text)}
  colors     {"brand": "#e8321f", "text": "#ffffff", "tint": .55}   tint = how red the last pages get
  language   "he" | "en";  pair (Hebrew, default "karantina"; see common.HE_PAIRS); Latin: Oswald 700 + Jost 300
  sfx (true), music, music_vol, plate_vol, name, track (optional)
"""
import subprocess

import paths
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def dur_of(clip):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(clip)],
                                capture_output=True, text=True).stdout.strip())


def build(spec, base, style="FLIP-MONTAGE-LOGO"):
    tp = type_pair(spec, latin=("Oswald", 700, "Jost", 300), default_pair="karantina")
    col = {"brand": "#e8321f", "text": "#ffffff", "tint": .55, **spec.get("colors", {})}
    clip = res(base, spec["clip"])
    D = dur_of(clip)
    t0 = spec.get("t", max(0, D - 3.4))
    md = spec.get("dur", 2.2)
    n = spec.get("frames", 18)
    a, b = spec.get("from", .2), spec.get("to", D - .2)
    name = spec.get("name", "flip")
    fdir = paths.root() / "tracks" / f"_{name}_frames"
    fdir.mkdir(parents=True, exist_ok=True)
    extra = dict(tp["files"])
    imgs = []
    for k in range(n):
        ts = a + (b - a) * k / max(1, n - 1)
        out = fdir / f"f{k:02d}.jpg"
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", f"{ts:.3f}", "-i", str(clip), "-frames:v", "1",
                        "-vf", "scale=1280:-2", "-q:v", "4", str(out)], check=True)
        extra[f"flip/f{k:02d}.jpg"] = out
        imgs.append(f"assets/flip/f{k:02d}.jpg")
    logo = spec.get("logo", {"text": "LOGO"})
    if logo.get("image"):
        li = res(base, logo["image"])
        extra["flip/logo" + li.suffix] = li
        mark = f'<img class="lgi" src="assets/flip/logo{li.suffix}" alt="">'
    else:
        mark = f'<div class="lgt">{e(logo["text"])}</div>'
    sub = f'<div class="lgs">{e(logo["sub"])}</div>' if logo.get("sub") else ""
    # variety is what makes the montage read: every page gets its own seeded punch-in and treatment
    import random as _r
    rnd = _r.Random(spec.get("seed", 21))
    looks = []
    for k in range(n):
        z = 1.15 + rnd.random() * 1.1
        ox, oy = 20 + rnd.random() * 60, 15 + rnd.random() * 70
        flt = ["grayscale(1) contrast(1.35)", "saturate(1.4) contrast(1.15)", "contrast(1.25) brightness(1.05)"][k % 3]
        looks.append(f"transform:scale({z:.2f});transform-origin:{ox:.0f}% {oy:.0f}%;filter:{flt}")
    pages = "".join(f'<div class="pg" id="p{k}"><img src="{src}" alt="" style="{looks[k]}"><i></i></div>' for k, src in enumerate(imgs))
    rtl = tp["rtl"]
    css = tp["css"] + f"""
#fm{{position:absolute;inset:0;opacity:0;background:#000;perspective:2200px;overflow:hidden}}
#stk{{position:absolute;inset:0;transform-style:preserve-3d}}
.pg{{position:absolute;inset:0;overflow:hidden;transform-origin:{'100%' if rtl else '0'} 50%;backface-visibility:hidden;box-shadow:0 0 60px rgba(0,0,0,.6)}}
.pg img{{width:100%;height:100%;object-fit:cover;display:block}}
.pg i{{position:absolute;inset:0;background:{col['brand']};mix-blend-mode:multiply;opacity:0}}
#lg{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center;opacity:0}}
#blk{{position:relative;background:{col['brand']};padding:.08em .32em .02em;overflow:hidden;font-size:230px}}
.lgt{{font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};font-size:230px;line-height:1.1;color:{col['text']};letter-spacing:{'0' if rtl else '.01em'};direction:{tp['dir']};white-space:nowrap}}
.lgi{{display:block;max-width:1200px;max-height:300px}}
#sw{{position:absolute;top:0;bottom:0;width:40%;left:-45%;background:linear-gradient(100deg,transparent,rgba(255,255,255,.55),transparent)}}
.lgs{{font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:46px;color:#fff;letter-spacing:{'0' if rtl else '.4em'};margin-top:26px;direction:{tp['dir']}}}
"""
    hud = f'<div id="fm"><div id="stk">{pages}</div><div id="lg"><div id="blk">{mark}<div id="sw"></div></div>{sub}</div></div>'
    j = [JS_UTIL, f"const T0 = {t0}, MD = {md}, N = {n}, RTL = {js(rtl)}, TINT = {col['tint']};", r"""
// flip k starts at T0 + MD * f(k/N), f = accelerating curve; each flip lasts a shrinking slice of time
const start = (k) => T0 + MD * (1 - Math.pow(1 - k / N, 1.9));
const PG = [...document.getElementsByClassName("pg")];
window.onPlace = (t) => {
  const on = t >= T0 - .02;
  document.getElementById("fm").style.opacity = on ? 1 : 0;
  if (!on) return;
  const zoom = 1.28 - .28 * easeInOut((t - T0) / (MD + .6));
  document.getElementById("stk").style.transform = `scale(${zoom})`;
  PG.forEach((p, k) => {
    const s = start(k), e = start(k + 1), d = Math.max(.05, e - s);
    const u = clamp01((t - s) / d);
    p.style.zIndex = String(N - k);
    p.style.display = t > e + .02 ? "none" : "block";
    p.style.transform = `rotateY(${(RTL ? 1 : -1) * 105 * easeInOut(u)}deg)`;
    p.lastChild.style.opacity = TINT * (k / N) + (u > 0 ? .15 * u : 0);
  });
  const L = T0 + MD;   // the last page has fallen: the logo block is underneath
  const lg = document.getElementById("lg"), blk = document.getElementById("blk");
  lg.style.opacity = t >= L - .15 ? 1 : 0;
  const v = easeOut3((t - L + .15) / .7);
  blk.style.transform = `scale(${1.5 - .5 * v})`;
  document.getElementById("sw").style.left = (-45 + 190 * clamp01((t - L - .35) / .8)) + "%";
  const sb = document.querySelector(".lgs"); if (sb) { sb.style.opacity = clamp01((t - L - .4) / .5); sb.style.transform = `translateY(${20 * (1 - clamp01((t - L - .4) / .5))}px)`; }
};
"""]
    sfx = []
    if spec.get("sfx", True):
        starts = [t0 + md * (1 - (1 - k / n) ** 1.9) for k in range(0, n, 2)]
        sfx = [cue("ui_tick", s_, .25) for s_ in starts] + [cue("ui_whoosh", t0 - .1, .5), cue("logo_hit", t0 + md - .05, .9)]
    sfx += audio_cues(spec, base, .6)
    return dict(project=project_dir(spec, style), clip=clip, track=tracks(spec, base), css=css, hud=hud, js="\n".join(j), sfx=sfx,
                plate_vol=spec.get("plate_vol", .35), extra=extra)
