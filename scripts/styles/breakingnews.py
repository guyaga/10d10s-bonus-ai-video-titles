"""BREAKING-NEWS: the rolling-news package. A red BREAKING slab slams in with a white flash and a shine, the headline bar
wipes open beside it and the headline types in word by word, a location/time strap drops under it, a pulsing LIVE chip
and a channel bug with a running clock sit top-corner, and a ticker crawls along the bottom. Headlines can change
(the bar flips to the next one). Hebrew mirrors the layout; the ticker crawls the other way.

Spec keys. Required: clip, headlines.
  slab        "BREAKING NEWS" | "מבזק"       the red label
  headlines   [{"text": "...", "t": 1.0}]     each replaces the previous with a vertical flip
  strap       {"text": "תל אביב · 19:42", "t": 1.8}   small line under the headline
  bug         {"name": "N12", "clock": "19:42:08"}      top corner channel bug; clock runs with the video
  ticker      {"text": "...", "t": .6, "speed": 150, "label": "עוד"}
  live        true                                      LIVE chip next to the bug
  language    "he" | "en";  pair (Hebrew default "karantina": Karantina 700 slab/headline + Secular One labels);
              Latin default Oswald 700 + Archivo 500
  colors      {"red": "#d6001c", "bar": "#ffffff", "ink": "#0b0b0e", "navy": "#0a1a33", "text": "#ffffff"}
  sfx (true), music, music_vol, vo, plate_vol, name
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, fonts, js, project_dir, res, tracks, type_pair, words)


def build(spec, base, style="BREAKING-NEWS"):
    tp = type_pair(spec, latin=("Oswald", 700, "Archivo", 500), default_pair="karantina")
    rtl = tp["rtl"]
    col = {"red": "#d6001c", "bar": "#ffffff", "ink": "#0b0b0e", "navy": "#0a1a33", "text": "#ffffff", **spec.get("colors", {})}
    D, B = tp["display"], tp["body"]
    s_ = "right" if rtl else "left"
    o_ = "left" if rtl else "right"
    heads = spec["headlines"]
    hl = "".join(f'<div class="hl" id="hl{i}">' + "".join(f'<span class="w">{e(w)}</span>' for w in words(h["text"])) + "</div>"
                 for i, h in enumerate(heads))
    strap = spec.get("strap")
    bug = spec.get("bug")
    tk = spec.get("ticker")
    h = ['<div id="flash"></div>',
         f'<div id="lower" style="{s_}:80px"><div id="slab"><span>{e(spec.get("slab", "BREAKING NEWS"))}</span><i class="shine"></i></div>'
         f'<div id="hbar"><div class="hls">{hl}</div></div></div>']
    if strap:
        h.append(f'<div id="strap" style="{s_}:80px"><i></i>{e(strap["text"])}</div>')
    if bug:
        live = '<div class="lv"><i></i>LIVE</div>' if spec.get("live", True) else ""
        h.append(f'<div id="bug" style="{o_}:70px">{live}<div class="bn">{e(bug.get("name", ""))}</div><div class="bc" id="bc">{e(bug.get("clock", ""))}</div></div>')
    if tk:
        run = e(tk["text"])
        h.append(f'<div id="tk"><div class="tl">{e(tk.get("label", "MORE" if not rtl else "עוד"))}</div><div class="cr"><div class="mv" id="mv">'
                 f'<span>{run}</span><span>{run}</span><span>{run}</span></div></div></div>')
    ocss, ofiles = fonts("Oswald")   # the bug clock / LIVE chip are Latin broadcast numerals in both languages
    css = tp["css"] + ocss + f"""
#flash{{position:absolute;inset:0;background:#fff;opacity:0;pointer-events:none}}
#lower{{position:absolute;bottom:170px;display:flex;align-items:stretch;direction:{tp['dir']};filter:drop-shadow(0 14px 28px rgba(0,0,0,.4))}}
#slab{{position:relative;overflow:hidden;background:{col['red']};color:#fff;display:flex;align-items:center;padding:0 30px;
  font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:{82 if rtl else 60}px;letter-spacing:{'0' if rtl else '.04em'};white-space:nowrap;line-height:1.1}}
#slab .shine{{position:absolute;top:0;bottom:0;width:90px;left:0;background:linear-gradient(100deg,transparent,rgba(255,255,255,.55),transparent);transform:skewX(-18deg)}}
#hbar{{background:{col['bar']};min-width:560px;height:120px;overflow:hidden;position:relative;box-shadow:inset 0 -6px 0 {col['red']}}}
.hls{{display:grid}} .hl{{grid-area:1/1;position:relative!important}}
.hls{{position:relative;height:100%}}
.hl{{position:absolute;inset:0;display:flex;align-items:center;gap:{12 if rtl else 16}px;padding:0 34px;white-space:nowrap;direction:{tp['dir']}}}
.hl .w{{display:inline-block;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:{70 if rtl else 58}px;color:{col['ink']};line-height:1.1;letter-spacing:{'0' if rtl else '.005em'};
  text-transform:{'none' if rtl else 'uppercase'}}}
#strap{{position:absolute;bottom:118px;display:flex;align-items:center;gap:12px;background:{col['navy']};color:{col['text']};padding:8px 20px;
  font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:28px;direction:{tp['dir']};letter-spacing:{'0' if rtl else '.06em'}}}
#strap i{{width:10px;height:10px;background:{col['red']};display:block}}
#bug{{position:absolute;top:60px;display:flex;align-items:stretch;gap:0;direction:ltr;filter:drop-shadow(0 8px 20px rgba(0,0,0,.35))}}
#bug .lv{{display:flex;align-items:center;gap:8px;background:{col['red']};color:#fff;font-family:"Oswald",sans-serif;font-weight:700;font-size:26px;padding:6px 14px;letter-spacing:.08em}}
#bug .lv i{{width:12px;height:12px;border-radius:50%;background:#fff;display:block}}
#bug .bn{{background:{col['navy']};color:#fff;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:32px;padding:4px 16px;display:flex;align-items:center}}
#bug .bc{{background:rgba(10,26,51,.72);color:#fff;font-family:"Oswald",sans-serif;font-weight:600;font-size:26px;padding:6px 14px;display:flex;align-items:center;font-variant-numeric:tabular-nums}}
#tk{{position:absolute;left:0;right:0;bottom:0;height:70px;display:flex;background:{col['navy']};direction:{tp['dir']}}}
#tk .tl{{background:{col['red']};color:#fff;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:36px;display:flex;align-items:center;padding:0 26px;z-index:2}}
#tk .cr{{position:relative;flex:1;overflow:hidden}}
#tk .mv{{position:absolute;top:0;height:70px;display:flex;align-items:center;white-space:nowrap;{s_}:0}}
#tk .mv span{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:30px;color:#fff;padding:0 70px}}
"""
    J = {"heads": [{"t": x["t"], "n": len(words(x["text"]))} for x in heads], "strap": strap, "ticker": tk,
         "clock": (bug or {}).get("clock"), "live": bool(bug) and spec.get("live", True), "t0": heads[0]["t"]}
    j = [JS_UTIL, f"const J = {js(J)}, RTL = {js(rtl)};", r"""
const $$ = (id) => document.getElementById(id);
let c0 = null; if (J.clock) { const p = J.clock.split(":").map(Number); c0 = p[0] * 3600 + p[1] * 60 + (p[2] || 0); }
window.onPlace = (t) => {
  if (c0 != null) { const s = c0 + Math.floor(t), p2 = (n) => String(n).padStart(2, "0");
    $$("bc").textContent = p2(Math.floor(s / 3600) % 24) + ":" + p2(Math.floor(s / 60) % 60) + ":" + p2(s % 60); }
  if (J.ticker) { const mv = $$("mv"), w = mv.scrollWidth / 3, x = (Math.max(0, t - J.ticker.t) * (J.ticker.speed || 150)) % w;
    mv.style.transform = `translateX(${RTL ? x : -x}px)`; }
};
const T0 = J.t0;
// slab slam + flash + shine
tl.fromTo("#slab", {scale: 1.6, opacity: 0}, {scale: 1, opacity: 1, duration: .22, ease: "power4.out"}, T0 - .45);
tl.fromTo("#flash", {opacity: .55}, {opacity: 0, duration: .25, ease: "power2.out"}, T0 - .45);
tl.fromTo("#slab .shine", {x: -130}, {x: 520, duration: .7, ease: "power2.inOut", immediateRender: true}, T0 - .2);
tl.fromTo("#slab .shine", {x: -130}, {x: 520, duration: .7, ease: "power2.inOut", immediateRender: false}, T0 + 3.2);
tl.fromTo("#hbar", {clipPath: RTL ? "inset(0 0 0 100%)" : "inset(0 100% 0 0)"}, {clipPath: "inset(0 0% 0 0%)", duration: .5, ease: "expo.out"}, T0 - .25);
J.heads.forEach((hd, i) => {
  tl.set(`#hl${i}`, {opacity: 1}, hd.t - .01);
  tl.fromTo(`#hl${i} .w`, {yPercent: 105, opacity: 0}, {yPercent: 0, opacity: 1, duration: .32, ease: "expo.out", stagger: .07}, hd.t);
  if (i > 0) tl.to(`#hl${i - 1} .w`, {yPercent: -105, opacity: 0, duration: .25, ease: "power2.in", stagger: .03}, hd.t - .28);
});
tl.set(J.heads.map((_, i) => `#hl${i} .w`).join(","), {opacity: 0}, 0);
if (J.strap) tl.fromTo("#strap", {opacity: 0, y: -24}, {opacity: 1, y: 0, duration: .4, ease: "power3.out"}, J.strap.t);
tl.fromTo("#bug", {opacity: 0, y: -20}, {opacity: 1, y: 0, duration: .45, ease: "power3.out"}, Math.max(.2, T0 - .8));
if (J.live) tl.to("#bug .lv i", {opacity: .15, duration: .5, repeat: 30, yoyo: true, ease: "sine.inOut"}, 0);
if (J.ticker) tl.fromTo("#tk", {y: 70}, {y: 0, duration: .45, ease: "power3.out"}, J.ticker.t);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("bass_pulse", J["t0"] - .45, .7), cue("stinger", J["t0"] - .45, .55)] + [cue("ui_tick", x["t"], .3) for x in heads]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .6), extra={**tp["files"], **ofiles})
