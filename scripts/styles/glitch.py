"""GLITCH-RGB: digital-glitch titles on the beat. On every hit the plate itself tears (an SVG displacement band filter +
RGB channel split on the video), and the titles split into red/green/blue copies and horizontal slices that jitter,
then snap clean. Between hits everything is still and sharp. Seeded, pure function of t. English or Hebrew.

Spec keys. Required: clip, titles.
  beat       {"bpm": 117.5, "offset": .05}         beat n = offset + n * 60/bpm
  titles     [{"text": "NORTHLINE", "sub": "WINTER DROP 01", "beat": 2, "until": 7, "x": 960, "y": 540, "size": 220,
               "follow": "jacket", "anchor": "r", "dx": 60, "dy": 0, "align": "left|center|right"}]   beats in beat units
  hits       [2, 7, 8, 11, 15, ...]   beats where the frame glitches (default: every title's beat + its until)
  strength   1.0   global glitch amount (tear displacement + split px)
  language   "he" | "en";  pair (Hebrew, default "karantina"; see common.HE_PAIRS); Latin: Oswald 700 + IBM Plex Mono 500
  colors     {"text": "#ffffff", "sub": "#ff5a1f", "r": "#ff2a3c", "g": "#29ff9a", "b": "#2d6bff"}
  seed;  music, music_vol, plate_vol, name, track (for follow titles)
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)

BANDS = 7


def build(spec, base, style="GLITCH-RGB"):
    tp = type_pair(spec, latin=("Oswald", 700, "IBM Plex Mono", 500), default_pair="karantina")
    col = {"text": "#ffffff", "sub": "#ff5a1f", "r": "#ff2a3c", "g": "#29ff9a", "b": "#2d6bff", **spec.get("colors", {})}
    bpm, off = spec.get("beat", {}).get("bpm", 120), spec.get("beat", {}).get("offset", 0)
    B = lambda n: round(off + 60 / bpm * n, 3)  # noqa: E731
    T, h = spec["titles"], []
    hits = spec.get("hits") or sorted({x["beat"] for x in T} | {x["until"] for x in T if x.get("until") is not None})
    for i, x in enumerate(T):
        size = x.get("size", 200)
        al = x.get("align", "center")
        tx = {"center": "-50%", "left": "0", "right": "-100%"}[al]
        pos = (f'data-follow="{e(x["follow"])}" data-anchor="{x.get("anchor", "c")}" data-dx="{x.get("dx", 0)}" data-dy="{x.get("dy", 0)}"'
               if x.get("follow") else f'style="left:{x.get("x", 960)}px;top:{x.get("y", 540)}px"')
        word = e(x["text"])
        A = "data-layout-allow-overlap data-layout-allow-occlusion"
        layers = "".join(f'<span class="ch {c}" {A}>{word}</span>' for c in ("r", "g", "b"))
        slices = "".join(f'<span class="sl" {A} style="clip-path:inset({k * 100 / BANDS:.2f}% 0 {100 - (k + 1) * 100 / BANDS:.2f}% 0)">{word}</span>'
                         for k in range(BANDS))
        sub = f'<div class="sub">{e(x["sub"])}</div>' if x.get("sub") else ""
        h.append(f'<div class="gt" id="t{i}" {pos}><div class="in" style="transform:translate({tx},-50%)">'
                 f'<div class="w" style="font-size:{size}px"><span class="base" {A}>{word}</span>{layers}{slices}</div>{sub}</div></div>')
    css = tp["css"] + f"""
#plate{{filter:url(#tear)}}
.gt{{position:absolute;left:0;top:0;width:0;height:0;opacity:0}}
.in{{position:absolute;left:0;top:0;direction:{tp['dir']};white-space:nowrap}}
.w{{position:relative;font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};line-height:1;letter-spacing:{'0' if tp['rtl'] else '.01em'};text-transform:uppercase}}
.w span{{display:block;color:{col['text']};white-space:nowrap}}
.w .base{{text-shadow:0 10px 40px rgba(0,0,0,.45)}}
.w .ch,.w .sl{{position:absolute;left:0;top:0;opacity:0}}
.w .ch{{mix-blend-mode:screen}}
.w .ch.r{{color:{col['r']}}}.w .ch.g{{color:{col['g']}}}.w .ch.b{{color:{col['b']}}}
.sub{{font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:34px;letter-spacing:{'0' if tp['rtl'] else '.3em'};color:{col['sub']};margin-top:14px;
  text-shadow:0 0 3px rgba(0,0,0,.9),0 2px 14px rgba(0,0,0,.85)}}
"""
    svg = ('<svg width="0" height="0" style="position:absolute"><filter id="tear" x="-5%" y="-5%" width="110%" height="110%" color-interpolation-filters="sRGB">'
           '<feTurbulence id="tb" type="fractalNoise" baseFrequency="0.0008 0.09" numOctaves="1" seed="1" result="n"/>'
           '<feDisplacementMap id="dm" in="SourceGraphic" in2="n" scale="0" xChannelSelector="R" yChannelSelector="A" result="d"/>'
           '<feColorMatrix in="d" type="matrix" values="1 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 1 0" result="R"/>'
           '<feOffset id="or" in="R" dx="0" result="R2"/>'
           '<feColorMatrix in="d" type="matrix" values="0 0 0 0 0  0 1 0 0 0  0 0 0 0 0  0 0 0 1 0" result="G"/>'
           '<feColorMatrix in="d" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 1 0 0  0 0 0 1 0" result="Bc"/>'
           '<feOffset id="ob" in="Bc" dx="0" result="B2"/>'
           '<feBlend in="R2" in2="G" mode="screen" result="RG"/><feBlend in="RG" in2="B2" mode="screen"/></filter></svg>')
    TJ = [{"i": i, "on": B(x["beat"]), "off": B(x["until"]) if x.get("until") is not None else None} for i, x in enumerate(T)]
    j = [JS_UTIL, f"const TT = {js(TJ)}, HITS = {js([B(n) for n in hits])}, K = {spec.get('strength', 1.0)}, SEED = {int(spec.get('seed', 9))};", r"""
const TE = TT.map(x => { const el = document.getElementById("t" + x.i); return {...x, el, ch: [...el.getElementsByClassName("ch")], sl: [...el.getElementsByClassName("sl")], base: el.getElementsByClassName("base")[0]}; });
const tb = document.getElementById("tb"), dm = document.getElementById("dm"), orr = document.getElementById("or"), ob = document.getElementById("ob");
// glitch envelope: a sharp 0.28 s burst after every hit, stuttering (on/off at 24 fps by hash)
function env(t) {
  let a = 0;
  for (const h of HITS) { const d = t - h; if (d >= -0.04 && d < .28) a = Math.max(a, (1 - d / .28) * (hash1(Math.floor(t * 24) * 7.3 + h) > .25 ? 1 : .15)); }
  return a;
}
window.onPlace = (t) => {
  const a = env(t) * K, fr = Math.floor(t * 24);
  dm.setAttribute("scale", (a * 110).toFixed(1));
  tb.setAttribute("seed", String(1 + (fr % 97)));
  orr.setAttribute("dx", (a * 14).toFixed(1)); ob.setAttribute("dx", (-a * 14).toFixed(1));
  for (const x of TE) {
    const vis = t >= x.on - .04 && (x.off == null || t < x.off + .12);
    x.el.style.opacity = vis ? 1 : 0;
    if (!vis) continue;
    // local burst: stronger at the title's own in/out
    const loc = Math.max(a, (t < x.on + .3 ? 1 - (t - x.on) / .3 : 0), (x.off != null && t > x.off - .1 ? (t - x.off + .1) / .22 : 0));
    const g = Math.max(0, Math.min(1, loc)) * K;
    x.base.style.opacity = g > .05 ? .15 : 1;
    x.ch.forEach((c, k) => { c.style.opacity = g > .05 ? 1 : 0; c.style.transform = `translate(${((k - 1) * 18 + (hash1(fr * 3 + k + x.i * 11) - .5) * 20) * g}px,${(hash1(fr + k * 5) - .5) * 8 * g}px)`; });
    x.sl.forEach((s, k) => { const on = g > .05 && hash1(fr * 13 + k * 7 + x.i) > .45; s.style.opacity = on ? 1 : 0;
      s.style.transform = `translateX(${(hash1(fr * 17 + k * 29 + SEED) - .5) * 160 * g}px)`; });
  }
};
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("lock_tick", B(n), .45) for n in hits] + [cue("data_chatter", B(n), .18) for n in hits[::2]]
    sfx += audio_cues(spec, base, .6)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud=svg + "".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .3), extra=tp["files"])
