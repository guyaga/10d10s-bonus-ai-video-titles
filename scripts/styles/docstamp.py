"""DOC-LOCATION-STAMP: the documentary place/date stamp. Cinema letterbox bars ease in, a typewriter stamp prints the place
name character by character with a block cursor, a transliteration line follows, the GPS coordinates scramble and lock digit
by digit, then time and date type out. Optionally a crosshair collapses onto a tracked landmark and hangs a small leader
label on it. Hebrew (RTL typing) or English; numbers always stay LTR.

Spec keys. Required: clip, place.
  place      "יפו העתיקה, ישראל"          typed first (display font of the pair)
  translit   "JAFFA · ISRAEL"            optional second line (mono, letter-spaced)
  coords     "32.0543° N   34.7516° E"   optional, scrambles into place
  when       "06:42  ·  14.05.2026"      optional, typed last
  t          start (default .8);  cps  characters per second (default 16);  hold until (default: end)
  corner     "bl" (default) | "br" | "tl" | "tr";  width  text column width px (default 760; keeps the accent bar planted)
  letterbox  2.39 (default) | 0 to disable
  landmark   {"obj": "tower", "label": "מגדל הפעמונים · 1906", "t": 4.6, "side": "L|R"}   needs "track"
  language   "he" | "en";  pair (Hebrew, default "secular"); Latin: Manrope 700 + JetBrains Mono
  colors     {"text": "#ffffff", "accent": "#ffcf6e"}
  sfx (true), plate_vol, music, music_vol, name, track
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, fonts, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="DOC-LOCATION-STAMP"):
    tp = type_pair(spec, latin=("Manrope", 700, "Manrope", 500), default_pair="secular")
    mono_css, mono_files = fonts("JetBrains Mono")
    rtl = tp["rtl"]
    col = {"text": "#ffffff", "accent": "#ffcf6e", **spec.get("colors", {})}
    t0, cps = spec.get("t", .8), spec.get("cps", 16)
    corner = spec.get("corner", "bl")
    lb = spec.get("letterbox", 2.39)
    bar_h = round((1080 - 1920 / lb) / 2) if lb else 0
    pad_y = bar_h + 70
    vx = "left" if corner.endswith("l") else "right"
    vy = "bottom" if corner.startswith("b") else "top"
    lm = spec.get("landmark")
    lines = [("pl", spec["place"], "disp")]
    if spec.get("translit"):
        lines.append(("tr", spec["translit"], "mono"))
    if spec.get("coords"):
        lines.append(("co", spec["coords"], "coord"))
    if spec.get("when"):
        lines.append(("wh", spec["when"], "mono"))
    # schedule: each line starts when the previous one finishes typing (+ a beat)
    sched, t = [], t0
    for key, text, kind in lines:
        dur = len(text) / cps if kind != "coord" else .9
        sched.append({"k": key, "text": text, "kind": kind, "t": round(t, 3), "d": round(dur, 3)})
        t += dur + (.35 if kind == "disp" else .2)
    css = tp["css"] + mono_css + f"""
.lbx{{position:absolute;left:0;right:0;height:{bar_h}px;background:#000}}
#lbt{{top:0;transform-origin:50% 0}} #lbb{{bottom:0;transform-origin:50% 100%}}
#stamp{{position:absolute;{vx}:120px;{vy}:{pad_y}px;display:flex;gap:26px;align-items:stretch;{'flex-direction:row-reverse;' if (rtl and vx == 'left') or (not rtl and vx == 'right') else ''}}}
#stamp .bar{{width:5px;background:{col['accent']};transform-origin:50% 100%}}
#stamp .col{{width:{spec.get('width', 760)}px;display:flex;flex-direction:column;gap:12px;align-items:{'flex-end' if rtl else 'flex-start'}}}
#dscrim{{position:absolute;{vx}:0;{vy}:0;width:1100px;height:560px;background:radial-gradient(ellipse at {'0%' if vx == 'left' else '100%'} {'100%' if vy == 'bottom' else '0%'},rgba(0,0,0,.42),transparent 70%);opacity:0}}
.ln{{white-space:pre;color:{col['text']};text-shadow:0 2px 16px rgba(0,0,0,.7),0 0 2px rgba(0,0,0,.5);min-height:1em}}
.ln.disp{{font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};font-size:62px;line-height:1.1;direction:{tp['dir']}}}
.ln.mono,.ln.coord{{font-family:"JetBrains Mono",monospace;font-weight:500;font-size:28px;letter-spacing:.14em;direction:ltr;color:rgba(255,255,255,.9)}}
.ln.coord{{color:{col['accent']}}}
.cur{{display:inline-block;width:.5em;height:.9em;background:{col['accent']};vertical-align:-.1em;margin-{'right' if rtl else 'left'}:.08em}}
#xh{{position:absolute;left:0;top:0;width:0;height:0;opacity:0}}
#xh .br{{position:absolute;width:34px;height:34px;border:3px solid {col['accent']};filter:drop-shadow(0 0 6px rgba(0,0,0,.6))}}
#xh .b1{{border-width:3px 0 0 3px}} #xh .b2{{border-width:3px 3px 0 0}} #xh .b3{{border-width:0 0 3px 3px}} #xh .b4{{border-width:0 3px 3px 0}}
#xh .dot{{position:absolute;left:-5px;top:-5px;width:10px;height:10px;border-radius:50%;background:{col['accent']};box-shadow:0 0 0 6px rgba(255,207,110,.25)}}
#xh .lead{{position:absolute;top:-1px;height:2px;width:120px;background:rgba(255,255,255,.9);transform-origin:{'100%' if (lm or {}).get('side') == 'L' else '0%'} 50%}}
#xh .lab{{position:absolute;top:-26px;white-space:nowrap;font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:30px;color:#fff;
  padding:6px 14px;background:rgba(10,12,16,.62);border:1px solid rgba(255,255,255,.22);border-radius:4px;direction:{tp['dir']}}}
"""
    col_html = "".join(f'<div class="ln {s["kind"]}" id="{s["k"]}"></div>' for s in sched)
    hud = (f'<div class="lbx" id="lbt"></div><div class="lbx" id="lbb"></div>' if lb else "")
    hud += '<div id="dscrim"></div>'
    hud += f'<div id="stamp"><div class="bar"></div><div class="col">{col_html}</div></div>'
    if lm:
        L = lm.get("side", "R") == "L"
        hud += ('<div id="xh"><i class="br b1"></i><i class="br b2"></i><i class="br b3"></i><i class="br b4"></i><i class="dot"></i>'
                f'<i class="lead" style="{"right:18px" if L else "left:18px"}"></i>'
                f'<div class="lab" style="{"right:150px" if L else "left:150px"}">{e(lm["label"])}</div></div>')
    J = {"S": sched, "rtl": rtl, "lb": bool(lb), "lm": lm, "t0": t0, "until": spec.get("until")}
    j = [JS_UTIL, f"const P = {js(J)};", r"""
const GLY = "0123456789";
if (P.lb) { tl.fromTo("#lbt", {scaleY: 0}, {scaleY: 1, duration: .9, ease: "power3.inOut"}, 0.1); tl.fromTo("#lbb", {scaleY: 0}, {scaleY: 1, duration: .9, ease: "power3.inOut"}, 0.1); }
tl.fromTo("#dscrim", {opacity: 0}, {opacity: 1, duration: .8}, P.t0 - .4);
tl.fromTo("#stamp .bar", {scaleY: 0}, {scaleY: 1, duration: .6, ease: "expo.out"}, P.t0 - .25);
const lastEnd = P.S[P.S.length - 1].t + P.S[P.S.length - 1].d;
window.onPlace = (t) => {
  for (const s of P.S) {
    const el = document.getElementById(s.k);
    let txt = "", cur = false;
    if (t >= s.t) {
      if (s.kind === "coord") {                       // digits scramble, then lock left to right
        const u = Math.min(1, (t - s.t) / s.d), lock = Math.floor(u * s.text.length), f = Math.floor(t * 24);
        txt = [...s.text].map((ch, i) => (i < lock || !/\d/.test(ch)) ? ch : GLY[Math.floor(hash1(f * 31 + i) * 10)]).join("");
      } else {
        const n = Math.min(s.text.length, Math.floor((t - s.t) * s.text.length / s.d + 1e-6));
        txt = [...s.text].slice(0, n).join("");
        cur = n < s.text.length || (s === P.S[P.S.length - 1] && Math.floor(t * 2.2) % 2 === 0);
      }
    }
    const html = txt.replace(/&/g, "&amp;").replace(/</g, "&lt;") + (cur ? '<i class="cur"></i>' : "");
    if (el.innerHTML !== html) el.innerHTML = html;
  }
};
if (P.until) tl.to("#stamp", {opacity: 0, y: 12, duration: .5, ease: "power2.in"}, P.until - .5);
if (P.lm) {
  const t = P.lm.t;
  tl.set("#xh", {opacity: 1}, t);
  // the brackets start wide and collapse onto the landmark, the dot pings, the leader draws, the label slides out
  const W = 150;
  [["b1", -W, -W, -34, -34], ["b2", W, -W, 0, -34], ["b3", -W, W, -34, 0], ["b4", W, W, 0, 0]].forEach(([c, x0, y0, x1, y1]) =>
    tl.fromTo("#xh ." + c, {x: x0, y: y0, opacity: 0}, {x: x1 - 17 + 17, y: y1 - 17 + 17, opacity: 1, duration: .55, ease: "expo.out"}, t));
  tl.fromTo("#xh .dot", {scale: 0}, {scale: 1, duration: .35, ease: "back.out(3)"}, t + .4);
  tl.fromTo("#xh .lead", {scaleX: 0}, {scaleX: 1, duration: .45, ease: "power3.out"}, t + .55);
  tl.fromTo("#xh .lab", {opacity: 0, x: P.lm.side === "L" ? 20 : -20}, {opacity: 1, x: 0, duration: .45, ease: "power3.out"}, t + .8);
}
"""]
    if lm:
        hud = hud.replace('<div id="xh">', f'<div id="xh" data-follow="{lm["obj"]}" data-anchor="{lm.get("anchor", "c")}" data-dx="{lm.get("dx", 0)}" data-dy="{lm.get("dy", 0)}">')
    sfx = []
    if spec.get("sfx", True):
        for s in sched:
            n = max(1, int(s["d"] * 7))
            if s["kind"] != "coord":
                sfx += [cue("soft_tick", s["t"] + i * s["d"] / n, .18) for i in range(n)]
            else:
                sfx.append(cue("data_chatter", s["t"], .12))
        if lm:
            sfx += [cue("lock_tick", lm["t"] + .4, .35)]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .8), extra={**tp["files"], **mono_files})
