"""END-SCREEN: the YouTube-style end card over the last seconds. A dark scrim wipes across the free side with an angled
edge, a WATCH NEXT heading unmasks, two video tiles flip up (thumbnails pulled from any clips at chosen times, with a
slow Ken Burns, a duration badge and a title), and a round channel avatar pops inside a dashed ring that draws and
spins, with a SUBSCRIBE label. The presenter stays on the other side of the frame.

Spec keys. Required: clip, tiles.
  t          start of the end card (default 5.6)
  side       "L" | "R"   the side the card covers (default L)
  heading    "WATCH NEXT"
  tile_w     tile width px (default 460)
  tiles      [{"src": "clips/podcast.mp4", "at": 4.0, "title": "...", "dur": "12:48"}]   two work best
  avatar     {"src": "clips/talking-head.mp4", "at": 1.0, "x": .58, "y": .26, "zoom": 3.2, "label": "SUBSCRIBE"}
             x/y = the face centre in the frame (0-1); zoom = crop factor
  language   "he" | "en";  pair (Hebrew default "secular"); Latin default Manrope 700 + Manrope 500
  colors     {"scrim": "#0b0d12", "accent": "#ff0033", "text": "#ffffff", "sub": "#aab3bf"}
  sfx (true), music, music_vol, plate_vol, name
"""
import subprocess

import paths
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def frame(src, at, out):
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", str(at), "-i", str(src), "-frames:v", "1", "-vf", "scale=960:-2", "-q:v", "3", str(out)], check=True)
    return out


def build(spec, base, style="END-SCREEN"):
    tp = type_pair(spec, latin=("Manrope", 700, "Manrope", 500), default_pair="secular")
    rtl = tp["rtl"]
    col = {"scrim": "#0b0d12", "accent": "#ff0033", "text": "#ffffff", "sub": "#aab3bf", **spec.get("colors", {})}
    D, B = tp["display"], tp["body"]
    t0 = spec.get("t", 5.6)
    side = spec.get("side", "L")
    name = spec.get("name", "end-screen")
    tmp = paths.root() / "tmp" / name
    extra = dict(tp["files"])
    tiles = spec["tiles"]
    TW = spec.get("tile_w", 460)
    th = []
    for i, tl_ in enumerate(tiles):
        f = frame(res(base, tl_["src"]), tl_.get("at", 2), tmp / f"tile{i}.jpg")
        extra[f"es/tile{i}.jpg"] = f
        th.append(f'<div class="tile" id="t{i}"><div class="th"><img src="assets/es/tile{i}.jpg" alt=""><span class="du">{e(tl_.get("dur", ""))}</span>'
                  f'<i class="pl"></i></div><div class="tt">{e(tl_["title"])}</div></div>')
    av = spec.get("avatar")
    avh = ""
    if av:
        f = frame(res(base, av["src"]), av.get("at", 1), tmp / "avatar.jpg")
        extra["es/avatar.jpg"] = f
        z = av.get("zoom", 3)
        avh = (f'<div id="av"><svg class="ring" width="236" height="236" viewBox="0 0 236 236"><circle cx="118" cy="118" r="110" fill="none" stroke="{col["accent"]}" '
               f'stroke-width="5" stroke-dasharray="14 10" pathLength="1000"/></svg><div class="ph"><img src="assets/es/avatar.jpg" alt="" '
               f'style="width:{z * 100}%;left:{50 - av.get("x", .5) * z * 100}%;top:{50 - av.get("y", .5) * z * 100 * 9 / 16}%"></div>'
               f'<div class="al">{e(av.get("label", "SUBSCRIBE" if not rtl else "הירשמו"))}</div></div>')
    edge = "polygon(0 0,100% 0,86% 100%,0 100%)" if side == "L" else "polygon(14% 0,100% 0,100% 100%,0 100%)"
    h = [f'<div id="scrim" style="{"left" if side == "L" else "right"}:0;clip-path:{edge}"></div>'
         f'<div id="es" class="{side}"><div class="hw"><div id="hd">{e(spec.get("heading", "WATCH NEXT" if not rtl else "הסרטון הבא"))}</div></div>'
         f'<div class="tiles">{"".join(th)}</div>{avh}</div>']
    css = tp["css"] + f"""
#scrim{{position:absolute;top:0;bottom:0;width:1140px;background:linear-gradient(100deg,{col['scrim']} 55%,color-mix(in srgb,{col['scrim']} 85%,transparent))}}
#es{{position:absolute;top:120px;width:980px;direction:{tp['dir']}}}
#es.L{{left:110px}} #es.R{{right:110px}}
.hw{{overflow:hidden;margin-bottom:34px}}
#hd{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:54px;letter-spacing:{'0' if rtl else '.18em'};color:{col['text']};line-height:1.25}}
.tiles{{display:flex;gap:34px;perspective:1400px}}
.tile{{width:{TW}px;transform-origin:50% 100%}}
.th{{position:relative;width:{TW}px;height:{round(TW * 9 / 16)}px;border-radius:16px;overflow:hidden;box-shadow:0 20px 50px rgba(0,0,0,.5);border:2px solid rgba(255,255,255,.14)}}
.th img{{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}}
.du{{position:absolute;bottom:12px;{'left' if rtl else 'right'}:12px;background:rgba(0,0,0,.8);color:#fff;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:20px;
  padding:3px 9px;border-radius:6px;direction:ltr}}
.pl{{position:absolute;left:50%;top:50%;width:70px;height:70px;margin:-35px;border-radius:50%;background:rgba(0,0,0,.55);border:3px solid rgba(255,255,255,.85)}}
.pl::after{{content:"";position:absolute;left:26px;top:19px;border-left:24px solid #fff;border-top:15px solid transparent;border-bottom:15px solid transparent}}
.tt{{margin-top:16px;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:30px;line-height:1.3;color:{col['text']}}}
#av{{position:absolute;top:650px;{'right' if rtl else 'left'}:0;display:flex;align-items:center;gap:28px}}
#av .ring{{position:absolute;left:-8px;top:-8px}}
#av .ph{{position:relative;width:220px;height:220px;border-radius:50%;overflow:hidden;background:#222}}
#av .ph img{{position:absolute;max-width:none}}
.al{{margin-{'right' if rtl else 'left'}:10px;background:{col['accent']};color:#fff;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:32px;padding:14px 30px;
  border-radius:999px;letter-spacing:{'0' if rtl else '.06em'}}}
"""
    J = {"t": t0, "side": side, "n": len(tiles), "av": bool(av)}
    j = [JS_UTIL, f"const J = {js(J)};", r"""
const T = J.t, L = J.side === "L";
tl.set("#es, #scrim", {autoAlpha: 0}, 0); tl.set("#es, #scrim", {autoAlpha: 1}, T - .01);
tl.fromTo("#scrim", {clipPath: L ? "polygon(0 0,0% 0,0% 100%,0 100%)" : "polygon(100% 0,100% 0,100% 100%,100% 100%)"},
  {clipPath: L ? "polygon(0 0,100% 0,86% 100%,0 100%)" : "polygon(14% 0,100% 0,100% 100%,0 100%)", duration: .7, ease: "expo.inOut"}, T);
tl.fromTo("#hd", {yPercent: 110}, {yPercent: 0, duration: .6, ease: "expo.out"}, T + .35);
for (let i = 0; i < J.n; i++) {
  tl.fromTo(`#t${i}`, {rotateX: 75, opacity: 0, y: 60}, {rotateX: 0, opacity: 1, y: 0, duration: .8, ease: "expo.out"}, T + .5 + i * .14);
  tl.fromTo(`#t${i} img`, {scale: 1.0}, {scale: 1.12, duration: 5, ease: "none"}, T + .5);
  tl.fromTo(`#t${i} .pl`, {scale: 0}, {scale: 1, duration: .4, ease: "back.out(2.5)"}, T + 1.0 + i * .14);
  tl.to(`#t${i}`, {y: -8, duration: 1.4, yoyo: true, repeat: 2, ease: "sine.inOut"}, T + 1.4 + i * .3);
}
if (J.av) {
  tl.fromTo("#av .ph", {scale: 0}, {scale: 1, duration: .6, ease: "back.out(2.2)"}, T + .9);
  // the ring draws only once the avatar is there (an empty dashed circle reads as a stray graphic)
  // a dashed stroke can't be drawn on with dashoffset (the pattern repeats), so the ring scales + fades in instead
  tl.set("#av .ring", {opacity: 0, transformOrigin: "50% 50%"}, 0);
  tl.fromTo("#av .ring", {opacity: 0, scale: .7}, {opacity: 1, scale: 1, duration: .6, ease: "back.out(2)", immediateRender: false}, T + 1.3);
  tl.fromTo("#av .ring", {rotate: 0}, {rotate: 120, duration: 5, ease: "none", transformOrigin: "50% 50%"}, T + 1.35);
  tl.fromTo(".al", {opacity: 0, x: L ? -20 : 20}, {opacity: 1, x: 0, duration: .45, ease: "power3.out"}, T + 1.3);
}
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", t0, .5), cue("logo_hit", t0 + .5, .4)] + ([cue("ui_pop", t0 + .9, .4)] if av else [])
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .85), extra=extra)
