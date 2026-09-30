"""DATA-CHARTS: an animated infographic panel on the clean side of the frame. A frosted glass card slides in, the title
unmasks, gridlines draw, bars grow one by one with their values counting up, then the card hands over to a line chart:
the line draws with a glowing head, the area fills under it, and the last point gets a value flag. Numbers are always
LTR; Hebrew mirrors the layout (card on the right if asked, bars ordered right-to-left, labels in Hebrew).

Spec keys. Required: clip, bars and/or line.
  panel     {"side": "L|R", "t": .6, "until": 9.6, "title": "...", "sub": "...", "w": 760}
  bars      {"labels": ["Q1","Q2","Q3","Q4"], "values": [42, 58, 71, 94], "unit": "%", "t": 1.3, "until": 5.2, "hi": 3}
            until = the bars leave (when a line chart follows, they hand over at line.t instead)
            hi = index of the highlighted bar (accent colour)
  line      {"values": [12, 18, 16, 27, 34, 41, 58], "labels": ["ינו", ...], "t": 5.4, "flag": "+312%", "title": "..."}
  language  "he" | "en";  pair (Hebrew default "secular"); Latin default Manrope 700 + Manrope 500
  colors    {"card": "rgba(10,13,18,.8)", "text": "#ffffff", "sub": "#c3ccd6", "bar": "rgba(255,255,255,.28)",
             "accent": "#39d98a", "grid": "rgba(255,255,255,.14)"}
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)

CW, CH = 640, 330   # chart area inside the card


def build(spec, base, style="DATA-CHARTS"):
    tp = type_pair(spec, latin=("Manrope", 700, "Manrope", 500), default_pair="secular")
    rtl = tp["rtl"]
    col = {"card": "rgba(10,13,18,.8)", "text": "#ffffff", "sub": "#c3ccd6", "bar": "rgba(255,255,255,.28)",
           "accent": "#39d98a", "grid": "rgba(255,255,255,.14)", **spec.get("colors", {})}
    D, B = tp["display"], tp["body"]
    P = {"side": "L", "t": .6, "until": None, "title": "", "sub": "", "w": 760, **spec.get("panel", {})}
    bars, line = spec.get("bars"), spec.get("line")
    grid = "".join(f'<line class="gl" x1="0" y1="{CH - CH * k / 4:.0f}" x2="{CW}" y2="{CH - CH * k / 4:.0f}" stroke="{col["grid"]}" stroke-width="1.5" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
                   for k in range(5))
    body = ""
    if bars:
        n = len(bars["values"])
        mx = max(bars["values"]) * 1.12
        slot = CW / n
        bw = slot * .52
        items = ""
        for k, v in enumerate(bars["values"]):
            idx = n - 1 - k if rtl else k
            x = slot * idx + (slot - bw) / 2
            hgt = CH * v / mx
            hi = k == bars.get("hi", n - 1)
            items += (f'<div class="bar{" hi" if hi else ""}" id="b{k}" style="left:{x:.0f}px;width:{bw:.0f}px;height:{hgt:.0f}px"></div>'
                      f'<div class="bv" id="bv{k}" style="left:{x + bw / 2:.0f}px;bottom:{hgt + 10:.0f}px"><span id="bn{k}">0</span>{e(bars.get("unit", ""))}</div>'
                      f'<div class="bl" style="left:{x + bw / 2:.0f}px">{e(bars["labels"][k])}</div>')
        body += f'<div class="ch" id="chb">{items}</div>'
    if line:
        vs = line["values"]
        n = len(vs)
        lo, hi_ = min(vs) * .8, max(vs) * 1.15
        pts = []
        for k, v in enumerate(vs):
            idx = n - 1 - k if rtl else k
            pts.append((CW * idx / (n - 1), CH - CH * (v - lo) / (hi_ - lo)))
        if rtl:
            pts = pts  # still drawn in data order (oldest first) so the line grows toward the newest point
        d = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
        area = d + f" L{pts[-1][0]:.1f} {CH} L{pts[0][0]:.1f} {CH} Z"
        labs = "".join(f'<div class="xl" style="left:{(CW * (n - 1 - k if rtl else k) / (n - 1)):.0f}px">{e(t)}</div>' for k, t in enumerate(line.get("labels", [])))
        fx, fy = pts[-1]
        body += (f'<div class="ch" id="chl"><svg width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" overflow="visible">'
                 f'<defs><linearGradient id="ag" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{col["accent"]}" stop-opacity=".45"/>'
                 f'<stop offset="1" stop-color="{col["accent"]}" stop-opacity="0"/></linearGradient></defs>'
                 f'<path class="ar" d="{area}" fill="url(#ag)"/>'
                 f'<path class="lp" d="{d}" fill="none" stroke="{col["accent"]}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
                 f'<circle class="hd" cx="{fx:.1f}" cy="{fy:.1f}" r="9" fill="#fff"/></svg>{labs}'
                 f'<div class="flag" style="left:{fx:.0f}px;top:{fy:.0f}px">{e(line.get("flag", ""))}</div></div>')
    side = "right" if P["side"] == "R" else "left"
    lt = line.get("title") if line else None
    h = [f'<div id="card" style="{side}:96px;width:{P["w"]}px"><div class="tw"><div class="tt" id="tt1">{e(P["title"])}</div>'
         + (f'<div class="tt" id="tt2">{e(lt)}</div>' if lt else "") + f'</div><div class="sb">{e(P["sub"])}</div>'
         f'<div class="plot"><svg class="gs" width="{CW}" height="{CH}" viewBox="0 0 {CW} {CH}" overflow="visible">{grid}</svg>{body}</div></div>']
    css = tp["css"] + f"""
#card{{position:absolute;top:150px;padding:40px 48px 56px;background:{col['card']};backdrop-filter:blur(18px) saturate(1.2);border:1px solid rgba(255,255,255,.18);
  border-radius:22px;box-shadow:0 30px 80px rgba(0,0,0,.35);direction:{tp['dir']}}}
.tw{{position:relative;overflow:hidden;height:70px}}
.tt{{position:absolute;inset:0;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:48px;color:{col['text']};line-height:1.35;white-space:nowrap}}
.sb{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:24px;color:{col['sub']};margin:4px 0 30px}}
.plot{{position:relative;width:{CW}px;height:{CH}px;direction:ltr}}
.gs{{position:absolute;left:0;top:0}}
.ch{{position:absolute;inset:0}}
.bar{{position:absolute;bottom:0;background:{col['bar']};border-radius:8px 8px 2px 2px;transform-origin:50% 100%}}
.bar.hi{{background:{col['accent']};box-shadow:0 0 30px color-mix(in srgb,{col['accent']} 55%,transparent)}}
.bv{{position:absolute;transform:translateX(-50%);text-shadow:0 2px 8px rgba(0,0,0,.6);font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:30px;color:{col['text']};font-variant-numeric:tabular-nums;white-space:nowrap}}
.bl,.xl{{position:absolute;top:{CH + 14}px;transform:translateX(-50%);font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:22px;color:{col['sub']};white-space:nowrap}}
#chl svg{{position:absolute;left:0;top:0;overflow:visible}}
.hd{{transform-box:fill-box;transform-origin:center;filter:drop-shadow(0 0 10px {col['accent']})}}
.flag{{position:absolute;transform:translate(-100%,-150%);background:{col['accent']};color:#07150d;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:30px;
  padding:6px 14px;border-radius:8px;white-space:nowrap;direction:ltr}}
"""
    J = {"P": P, "bars": ({"t": bars["t"], "until": bars.get("until"), "v": bars["values"]} if bars else None),
         "line": ({"t": line["t"]} if line else None), "rtl": rtl}
    j = [JS_UTIL, f"const J = {js(J)};", r"""
const $$ = (id) => document.getElementById(id);
const P = J.P, BR = J.bars, LN = J.line;
window.onPlace = (t) => {
  if (BR) BR.v.forEach((v, k) => { const u = easeOut3((t - (BR.t + k * .18)) / 1.0); $$("bn" + k).textContent = Math.round(v * u); });
};
tl.fromTo("#card", {opacity: 0, x: P.side === "R" ? 60 : -60, scale: .96}, {opacity: 1, x: 0, scale: 1, duration: .7, ease: "expo.out"}, P.t);
tl.fromTo("#tt1", {yPercent: 110}, {yPercent: 0, duration: .6, ease: "expo.out"}, P.t + .2);
tl.fromTo(".sb", {opacity: 0, y: 10}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, P.t + .35);
tl.fromTo(".gl", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: .8, ease: "power2.inOut", stagger: .06}, P.t + .3);
if (BR) {
  BR.v.forEach((v, k) => {
    tl.fromTo(`#b${k}`, {scaleY: 0}, {scaleY: 1, duration: .9, ease: "expo.out"}, BR.t + k * .18);
    tl.fromTo(`#bv${k}`, {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: .4, ease: "power3.out"}, BR.t + k * .18 + .2);
  });
  tl.fromTo(".bl", {opacity: 0}, {opacity: 1, duration: .4, stagger: .1}, BR.t);
  if (LN) tl.to("#chb", {opacity: 0, y: 20, duration: .4, ease: "power2.in"}, LN.t - .45);
  else if (BR.until != null) tl.to("#chb", {opacity: 0, y: 20, duration: .4, ease: "power2.in"}, BR.until - .4);
}
if (LN) {
  tl.set("#chl", {opacity: 1}, LN.t - .01);
  if (document.getElementById("tt2")) { tl.to("#tt1", {yPercent: -110, duration: .4, ease: "power3.in"}, LN.t - .4); tl.fromTo("#tt2", {yPercent: 110}, {yPercent: 0, duration: .6, ease: "expo.out"}, LN.t - .05); }
  tl.fromTo(".lp", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: 1.8, ease: "power2.inOut"}, LN.t);
  tl.fromTo(".ar", {clipPath: J.rtl ? "inset(0 0 0 100%)" : "inset(0 100% 0 0)"}, {clipPath: "inset(0 0% 0 0%)", duration: 1.8, ease: "power2.inOut"}, LN.t);
  tl.fromTo(".xl", {opacity: 0}, {opacity: 1, duration: .4, stagger: .08}, LN.t);
  tl.fromTo(".hd", {scale: 0}, {scale: 1, duration: .4, ease: "back.out(3)"}, LN.t + 1.75);
  tl.fromTo(".flag", {opacity: 0, y: 16, scale: .8}, {opacity: 1, y: 0, scale: 1, duration: .45, ease: "back.out(2.5)"}, LN.t + 1.95);
  tl.to(".hd", {scale: 1.35, duration: .5, yoyo: true, repeat: 5, ease: "sine.inOut"}, LN.t + 2.2);
}
if (document.getElementById("tt2")) tl.set("#tt2", {yPercent: 110}, 0);
if (LN) { tl.set("#chl", {opacity: 0}, 0); tl.set(".hd", {transformOrigin: "50% 50%"}, 0); }
if (P.until != null) tl.to("#card", {opacity: 0, x: P.side === "R" ? 40 : -40, duration: .45, ease: "power3.in"}, P.until - .45);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", P["t"], .45)]
        if bars:
            sfx += [cue("soft_tick", bars["t"] + k * .18, .3) for k in range(len(bars["values"]))]
        if line:
            sfx += [cue("data_chatter", line["t"], .25), cue("chime", line["t"] + 1.95, .45)]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .6), extra=tp["files"])
