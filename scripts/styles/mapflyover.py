"""MAP-FLYOVER: aerial map explorer. A route line draws through tracked waypoints, pins with bilingual cards stick to
places, a distance readout counts up with the draw, lock brackets mark the destination, optional iris close on it.

Tracking: planar scenes -> scripts/track.py (anchors.json with the pin + route points picked on frame 0) -> points json.
vtrack.py output also works (the centre of each box is used).

Spec keys. Required: clip, track, pins.
  route      ["r0", "r1", ...]   ordered tracked point names the line draws through (optional)
  draw       [2.0, 7.0]           seconds: route draw start / end
  pins       [{"point": "ono", "en": "Ono Academic College", "he": "הקריה האקדמית אונו", "meta": "32.036°N 34.865°E",
               "t": 7.0, "side": "left|right", "below": false, "dim_at": null, "hide_at": null, "main": true}]
             main = lock brackets + iris target
  title      {"kicker": "ROUTE 01 · ARRIVAL", "en": "FROM TLV TO ONO", "he": "מנתב״ג לקריית אונו", "t": .3, "until": 6.3}
  readout    {"label": "BY ROAD", "value": 12.8, "unit": "km", "dec": 1, "left": "≈ 17 min", "right": "straight line 4.0 km",
              "t": 1.9, "until": 8.4}
  chip       "LIVE ROUTE"          top-right status chip (optional)
  iris       {"t": 8.4, "dur": 1.55}    close the frame onto the main pin (optional)
  colors     {"accent": "#9bd14a", "fg": "#eef4e8", "mute": "#b7c6ad"}
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (TICKS, audio_cues, cue, e, fonts, js, project_dir, res, tracks)


def build(spec, base, style="MAP-FLYOVER"):
    col = {"accent": "#9bd14a", "fg": "#eef4e8", "mute": "#b7c6ad", **spec.get("colors", {})}
    pins = spec["pins"]
    draw = spec.get("draw", [2.0, 7.0])
    title, rd, iris = spec.get("title"), spec.get("readout"), spec.get("iris")
    faces, extra = fonts("Secular One", "JetBrains Mono")
    css = faces + f"""
#root{{font-family:"Secular One",sans-serif}}
:root{{--fg:{col['fg']};--mute:{col['mute']};--acc:{col['accent']};--panel:rgba(7,13,9,.78);--line:color-mix(in srgb,var(--acc) 55%,transparent)}}
.mono{{font-family:"JetBrains Mono",monospace}}
#chip{{position:absolute;right:112px;top:60px;display:flex;align-items:center;gap:12px;font-size:20px;letter-spacing:.14em;color:var(--fg);background:var(--panel);padding:10px 16px;border-radius:4px}}
#chipdot{{width:12px;height:12px;border-radius:50%;background:var(--acc)}}
#title{{position:absolute;left:112px;top:96px;width:900px}}
#kicker{{font-size:20px;letter-spacing:.2em;color:var(--acc);display:inline-block;background:var(--panel);padding:8px 12px;border-radius:4px}}
#h1{{white-space:nowrap;font-size:84px;font-weight:800;line-height:1;letter-spacing:-.01em;margin-top:14px;display:block;text-shadow:0 4px 30px rgba(0,0,0,.6)}}
#h1he{{font-size:44px;font-weight:600;direction:rtl;text-align:left;margin-top:12px;display:block;text-shadow:0 3px 20px rgba(0,0,0,.7)}}
#titlebar{{height:3px;width:120px;background:var(--acc);margin-top:22px}}
.pin{{position:absolute;left:0;top:0;width:0;height:0}}
.pin .dot{{position:absolute;left:-11px;top:-11px;width:22px;height:22px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 5px rgba(7,13,9,.7),0 0 24px var(--acc)}}
.pin .ring{{position:absolute;left:-30px;top:-30px;width:60px;height:60px;border-radius:50%;border:2px solid var(--acc)}}
.pin .stem{{position:absolute;left:-1px;bottom:18px;width:2px;height:70px;background:var(--line);transform-origin:50% 100%}}
.pin .card{{position:absolute;left:-24px;bottom:92px;width:max-content;min-width:260px;background:var(--panel);padding:16px 20px 16px 22px;border-radius:6px;border-top:2px solid var(--acc)}}
.pin.right .card{{left:auto;right:-24px}}
.pin.below .card{{bottom:auto;top:34px}}.pin.below .stem{{display:none}}
.pin.minor .dot{{background:var(--mute);box-shadow:0 0 0 5px rgba(7,13,9,.7)}}.pin.minor .ring{{border-color:var(--mute)}}.pin.minor .card{{border-top-color:var(--mute);min-width:200px}}
.card .en{{font-size:36px;font-weight:700;line-height:1.1;display:block;white-space:nowrap}}
.card .he{{font-size:28px;font-weight:600;direction:rtl;text-align:left;display:block;color:var(--mute);margin-top:4px;white-space:nowrap}}
.card .meta{{font-size:18px;letter-spacing:.08em;color:var(--acc);display:block;margin-top:8px;white-space:nowrap}}
#lock{{position:absolute;left:0;top:0;width:0;height:0}}
.br{{position:absolute;width:34px;height:34px;border-color:var(--acc);border-style:solid}}
#b1{{left:-70px;top:-70px;border-width:3px 0 0 3px}}#b2{{left:36px;top:-70px;border-width:3px 3px 0 0}}
#b3{{left:-70px;top:36px;border-width:0 0 3px 3px}}#b4{{left:36px;top:36px;border-width:0 3px 3px 0}}
#route{{position:absolute;inset:0;width:1920px;height:1080px;overflow:visible}}
#readout{{position:absolute;left:112px;bottom:104px;background:var(--panel);padding:20px 26px;border-radius:6px;width:560px}}
.row{{display:flex;justify-content:space-between;align-items:baseline;gap:20px}}
.lab{{font-size:18px;letter-spacing:.16em;color:var(--mute)}}
.val{{font-size:44px;font-weight:700;color:var(--fg)}}
.small{{font-size:20px;color:var(--mute)}}
#bar{{height:4px;background:rgba(238,244,232,.15);margin-top:14px;border-radius:2px;overflow:hidden}}
#barfill{{height:100%;width:100%;background:var(--acc);transform-origin:0 50%}}
#iris{{position:absolute;inset:0;background:radial-gradient(circle at var(--ix,960px) var(--iy,540px),transparent 0,transparent var(--ir,2400px),#050805 calc(var(--ir,2400px) + 2px))}}
"""
    h = ['<div id="iris"></div>',
         '<svg id="route" viewBox="0 0 1920 1080"><defs><filter id="glow" x="-20%" y="-20%" width="140%" height="140%"><feGaussianBlur stdDeviation="6" result="b"/>'
         '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
         f'<polyline id="rg" fill="none" stroke="{col["fg"]}" stroke-opacity=".35" stroke-width="3" stroke-dasharray="4 12" stroke-linecap="round" points=""/>'
         f'<polyline id="rl" fill="none" stroke="{col["accent"]}" stroke-width="6" stroke-linecap="round" stroke-linejoin="round" filter="url(#glow)" points=""/>'
         f'<circle id="rh" r="10" fill="{col["fg"]}" stroke="{col["accent"]}" stroke-width="4" cx="-50" cy="-50"/></svg>']
    main = next((p for p in pins if p.get("main")), pins[-1])
    for i, p in enumerate(pins):
        cls = " ".join(x for x in ["pin", "right" if p.get("side") == "right" else "", "below" if p.get("below") else "", "" if p is main or p.get("major") else "minor"] if x)
        card = (f'<span class="en">{e(p.get("en", ""))}</span>' + (f'<span class="he">{e(p["he"])}</span>' if p.get("he") else "")
                + (f'<span class="meta mono">{e(p["meta"])}</span>' if p.get("meta") else ""))
        h.append(f'<div id="pin{i}" class="{cls}" data-follow="{e(p["point"])}" data-anchor="c"><div class="stem"></div><div class="ring"></div><div class="dot"></div><div class="card">{card}</div></div>')
    h.append(f'<div id="lock" data-follow="{e(main["point"])}" data-anchor="c"><div class="br" id="b1"></div><div class="br" id="b2"></div><div class="br" id="b3"></div><div class="br" id="b4"></div></div>')
    if title:
        h.append(f'<div id="title"><span id="kicker" class="mono">{e(title.get("kicker", ""))}</span><span id="h1">{e(title["en"])}</span>'
                 + (f'<span id="h1he">{e(title["he"])}</span>' if title.get("he") else "") + '<div id="titlebar"></div></div>')
    if rd:
        h.append(f'<div id="readout"><div class="row"><span class="lab mono">{e(rd.get("label", ""))}</span><span class="val mono"><span id="km">0</span> {e(rd.get("unit", ""))}</span></div>'
                 f'<div class="row" style="margin-top:6px"><span class="small mono">{e(rd.get("left", ""))}</span><span class="small mono">{e(rd.get("right", ""))}</span></div>'
                 '<div id="bar"><div id="barfill"></div></div></div>')
    h.append(TICKS)
    if spec.get("chip"):
        h.append(f'<div id="chip" class="mono"><div id="chipdot"></div>{e(spec["chip"])}</div>')
    P = [{"i": i, "t": p.get("t", .8 + .7 * i), "dim": p.get("dim_at"), "hide": p.get("hide_at")} for i, p in enumerate(pins)]
    j = [f"const ROUTE = {js(spec.get('route', []))}, DRAW = {js(draw)}, MAIN = {js(main['point'])}, MAINI = {pins.index(main)}, PINS = {js(P)};",
         f"const RD = {js(rd)}, IRIS = {js(iris)}, TITLE = {js(title)};", r"""
const c = (n, t) => { const b = boxAt(n, t); return b ? [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2] : null; };
const ease = gsap.parseEase("power2.inOut");
function partial(pts, u) {
  const seg = []; let L = 0;
  for (let i = 1; i < pts.length; i++) { const d = Math.hypot(pts[i][0]-pts[i-1][0], pts[i][1]-pts[i-1][1]); seg.push(d); L += d; }
  let want = L * u; const out = [pts[0]];
  for (let i = 1; i < pts.length; i++) {
    if (want >= seg[i-1]) { out.push(pts[i]); want -= seg[i-1]; continue; }
    const f = seg[i-1] ? want / seg[i-1] : 0;
    out.push([pts[i-1][0] + (pts[i][0]-pts[i-1][0]) * f, pts[i-1][1] + (pts[i][1]-pts[i-1][1]) * f]); break;
  }
  return out;
}
window.onPlace = (t) => {
  const pts = ROUTE.map((r) => c(r, t)).filter(Boolean);
  const u = ease(Math.max(0, Math.min(1, (t - DRAW[0]) / (DRAW[1] - DRAW[0]))));
  document.getElementById("rg").setAttribute("points", pts.map((p) => p.join(",")).join(" "));
  const part = u > 0 && pts.length > 1 ? partial(pts, u) : [];
  document.getElementById("rl").setAttribute("points", part.map((p) => p.join(",")).join(" "));
  const head = part.length ? part[part.length - 1] : [-50, -50];
  document.getElementById("rh").setAttribute("cx", head[0]); document.getElementById("rh").setAttribute("cy", head[1]);
  if (RD) { document.getElementById("km").textContent = (RD.value * u).toFixed(RD.dec ?? 1); document.getElementById("barfill").style.transform = `scaleX(${u})`; }
  const o = c(MAIN, t) || [960, 540];
  const ir = !IRIS || t < IRIS.t ? 2400 : 2400 * (1 - ease(Math.min(1, (t - IRIS.t) / (IRIS.dur || 1.55))));
  const R = document.getElementById("root"); R.style.setProperty("--ix", o[0] + "px"); R.style.setProperty("--iy", o[1] + "px"); R.style.setProperty("--ir", ir + "px");
};
tl.fromTo(".tick", {opacity: 0, scale: 1.4}, {opacity: 1, scale: 1, duration: .5, stagger: .05, ease: "power3.out"}, .1);
if (document.querySelector("#chip")) { tl.fromTo("#chip", {opacity: 0, x: 24}, {opacity: 1, x: 0, duration: .45}, .3); tl.fromTo("#chipdot", {opacity: 1}, {opacity: .25, duration: .5, repeat: 17, yoyo: true, ease: "sine.inOut"}, .4); }
if (TITLE) {
  const t0 = TITLE.t ?? .3;
  tl.fromTo("#kicker", {opacity: 0, y: 12}, {opacity: 1, y: 0, duration: .4}, t0);
  tl.fromTo("#h1", {opacity: 0, y: 40, clipPath: "inset(0 100% 0 0)"}, {opacity: 1, y: 0, clipPath: "inset(0 0% 0 0)", duration: .7, ease: "expo.out"}, t0 + .15);
  if (document.querySelector("#h1he")) tl.fromTo("#h1he", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .5}, t0 + .45);
  tl.fromTo("#titlebar", {scaleX: 0, transformOrigin: "0 50%"}, {scaleX: 1, duration: .6, ease: "power3.inOut"}, t0 + .5);
  if (TITLE.until) tl.to("#title", {opacity: 0, y: -16, duration: .5, ease: "power2.in"}, TITLE.until);
}
function pop(id, at) {
  tl.fromTo(`${id} .dot`, {scale: 0}, {scale: 1, duration: .35, ease: "back.out(3)"}, at);
  tl.fromTo(`${id} .ring`, {scale: .3, opacity: .9}, {scale: 1.6, opacity: 0, duration: .9, ease: "power2.out"}, at + .05);
  tl.fromTo(`${id} .stem`, {scaleY: 0}, {scaleY: 1, duration: .35, ease: "power3.out"}, at + .15);
  tl.fromTo(`${id} .card`, {opacity: 0, y: 18, clipPath: "inset(100% 0 0 0)"}, {opacity: 1, y: 0, clipPath: "inset(0% 0 0 0)", duration: .5, ease: "expo.out"}, at + .3);
}
tl.set(".pin .dot, .pin .card, #lock .br", {opacity: 0}, 0);
for (const p of PINS) {
  tl.set(`#pin${p.i} .dot, #pin${p.i} .card`, {opacity: 1}, p.t);
  pop(`#pin${p.i}`, p.t);
  if (p.dim != null) tl.to(`#pin${p.i}`, {opacity: .55, duration: .6}, p.dim);
  if (p.hide != null) tl.to(`#pin${p.i}`, {opacity: 0, duration: .4}, p.hide);
}
const mt = PINS[MAINI].t;
tl.fromTo("#lock .br", {opacity: 0, scale: 2.2}, {opacity: 1, scale: 1, duration: .45, stagger: .04, ease: "power3.out"}, mt + .05);
tl.to("#lock .br", {opacity: .35, duration: .3, repeat: 3, yoyo: true, ease: "sine.inOut"}, mt + .6);
if (RD) {
  tl.fromTo("#readout", {opacity: 0, y: 24}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, RD.t ?? 1.9);
  if (RD.until) tl.to("#readout", {opacity: 0, duration: .4}, RD.until);
}
if (IRIS) tl.to(["#chip", ".pin.minor", ".pin .card"].filter(s => document.querySelector(s)), {opacity: 0, duration: .4}, IRIS.t);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", .25, .45)] + [cue("glass_ting", p["t"], .55) for p in P] + [cue("scan_beeps", draw[0], .2), cue("chime", draw[1], .5)]
        if iris:
            sfx.append(cue("logo_hit", iris["t"], .6))
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud="\n".join(h),
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .55), extra=extra)
