"""SPEED-STAT: sports-broadcast stat hits. Player bracket + tag, a giant stat stomp ("9 MS"), leader-line callouts to
tracked points, a spinning ring + label on a tracked object, a live speed counter, a motion trail, a giant end word
("GOAL", behind the subject when a matte is given) and a brand lockup.

Spec keys. Required: clip, track. Every block is optional.
  brand      {"name": "GUYAGA STRIKE", "tag": "FG · 2026", "until": 11.1}
  player     {"obj": "player", "title": "THE STRIKER", "sub": "RUN-UP 31 KM/H", "t": .5, "until": 2.5}
  stat       {"text": "9 MS", "sub": "CONTACT TIME", "x": 90, "y": 520, "t": 2.74, "until": 7.67}
  callouts   [{"title": "CARBON STRIKE PLATE", "sub": "+14% energy return", "obj": "boot", "fx": .5, "fy": .45,
               "x": 1260, "y": 130, "t": 4.3, "until": 7.67}]         leader line from a point inside obj's box
  ring       {"obj": "ball", "t": 3.6, "until": 11.05, "labels": [[3.6, "BALL COMPRESSION 18%"], [7.75, "SPIN 9.8 RPS"]], "label_until": 7.67}
  counter    {"t": 7.87, "until": 11.05, "value": 121, "dur": 1.6, "unit": "KM/H · SPIN 9.8 RPS", "x": 96, "bottom": 90}
  trail      {"obj": "ball", "t": 7.75, "until": 11.125, "len": .9}
  big        {"text": "GOAL", "t": 11.4, "size": 680}             behind the subject when "matte" is set
  lockup     {"name": "GUYAGA STRIKE", "line": "MAKE IT COUNT", "t": 13.0}
  colors     {"white": "#ffffff", "accent": "#E63B2E", "ink": "#0b0b0d"}
  sfx (true), music, music_vol, vo, plate_vol, matte, name
"""
from styles.common import (BRK, STOMP_JS, audio_cues, cue, e, fonts, js, project_dir, res, tracks)


def build(spec, base, style="SPEED-STAT"):
    col = {"white": "#ffffff", "accent": "#E63B2E", "ink": "#0b0b0d", **spec.get("colors", {})}
    brand, player, stat, co, ring, cnt, trail, big, lock = (spec.get(k) for k in ("brand", "player", "stat", "callouts", "ring", "counter", "trail", "big", "lockup"))
    co = co or []
    matte = res(base, spec["matte"]) if spec.get("matte") else None
    faces, extra = fonts("Anton", "Archivo", "JetBrains Mono")
    css = faces + f"""
:root{{--w:{col['white']};--red:{col['accent']};--k:{col['ink']};--panel:color-mix(in srgb,var(--k) 82%,transparent)}}
#root{{font-family:"Archivo","Secular One",sans-serif}}
#stage,#stage2{{position:absolute;inset:0}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0}}
#brand{{position:absolute;left:84px;top:64px;display:flex;align-items:center;gap:12px}}
#brand .b{{font-family:"Anton",sans-serif;font-size:40px;letter-spacing:.06em;color:var(--w);background:var(--k);padding:2px 16px}}
#brand .s{{font-family:"JetBrains Mono",monospace;font-size:18px;letter-spacing:.14em;color:var(--k);background:var(--red);padding:6px 10px}}
#pbox .brk i{{border-color:var(--red)}}
#ptag{{padding:10px 16px;background:var(--panel);border-left:4px solid var(--red);white-space:nowrap;width:max-content;height:auto}}
#ptag .n{{display:block;font-family:"Anton",sans-serif;font-size:34px;color:var(--w)}}
#ptag .s{{display:block;font-family:"JetBrains Mono",monospace;font-size:18px;color:#ffd2cf}}
#ms{{position:absolute;width:0;height:0}}
#ms span{{position:absolute;left:0;top:0;white-space:nowrap;font-family:"Anton",sans-serif;font-size:300px;color:var(--w);text-shadow:8px 8px 0 var(--red);transform:translate(0,-50%)}}
#ms small{{position:absolute;left:8px;top:150px;white-space:nowrap;font-family:"JetBrains Mono",monospace;font-size:26px;letter-spacing:.14em;color:var(--w);background:var(--k);padding:6px 12px}}
#lines,#trail{{position:absolute;inset:0;width:1920px;height:1080px}}
.co{{position:absolute;padding:12px 18px;background:var(--panel);border-top:3px solid var(--red);white-space:nowrap}}
.co .t{{display:block;font-family:"Anton",sans-serif;font-size:36px;color:var(--w)}}
.co .s{{display:block;font-family:"JetBrains Mono",monospace;font-size:18px;color:#ffd2cf;margin-top:2px}}
#ring{{position:absolute;left:0;top:0;width:0;height:0}}
#ring svg{{position:absolute;left:-260px;top:-260px}}
#ringl{{position:absolute;left:0;top:0;width:0;height:0}}
#ringl span{{position:absolute;left:0;top:0;white-space:nowrap;font-family:"JetBrains Mono",monospace;font-size:24px;color:var(--w);background:var(--k);padding:6px 12px;transform:translateX(-50%)}}
#spd{{position:absolute}}
#spd .v{{display:block;font-family:"Anton",sans-serif;font-size:220px;line-height:1.15;margin-bottom:22px;color:var(--w);text-shadow:8px 8px 0 var(--red)}}
#spd .u{{display:block;font-family:"JetBrains Mono",monospace;font-size:26px;letter-spacing:.2em;color:var(--w);background:var(--k);padding:6px 12px;width:max-content}}
#goal{{position:absolute;left:0;right:0;top:60px;text-align:center}}
#goal span{{display:inline-block;font-family:"Anton",sans-serif;line-height:1;color:var(--red);-webkit-text-stroke:6px var(--k);text-shadow:14px 14px 0 var(--k)}}
#lock{{position:absolute;left:0;right:0;margin:0 auto;bottom:70px;width:max-content;display:flex;align-items:center;gap:20px}}
#lock .b{{font-family:"Anton",sans-serif;font-size:76px;color:var(--w);background:var(--k);padding:0 24px}}
#lock .s{{font-family:"Anton",sans-serif;font-size:48px;color:var(--k);background:var(--red);padding:4px 20px}}
"""
    back = f'<div id="goal"><span style="font-size:{big.get("size", 680)}px" data-layout-allow-overlap data-layout-allow-occlusion>{e(big["text"])}</span></div>' if big else ""
    f = []
    if trail:
        f.append(f'<svg id="trail" viewBox="0 0 1920 1080"><polyline id="tr" fill="none" stroke="{col["accent"]}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" points=""/></svg>')
    f.append('<svg id="lines" viewBox="0 0 1920 1080">' + "".join(
        f'<path id="l{i}" fill="none" stroke="{col["white"]}" stroke-width="3"/><circle id="d{i}" r="10" fill="{col["accent"]}" stroke="{col["white"]}" stroke-width="3" cx="-50" cy="-50"/>'
        for i in range(len(co))) + "</svg>")
    if player:
        f.append(f'<div id="pbox" data-box="{e(player["obj"])}" data-pad="16">{BRK}</div>'
                 f'<div id="ptag" data-follow="{e(player["obj"])}" data-anchor="r" data-dx="26" data-dy="-120"><span class="n">{e(player["title"])}</span>'
                 + (f'<span class="s">{e(player["sub"])}</span>' if player.get("sub") else "") + "</div>")
    if stat:
        f.append(f'<div id="ms" style="left:{stat.get("x", 90)}px;top:{stat.get("y", 520)}px"><span data-layout-allow-overlap>{e(stat["text"])}</span>'
                 + (f'<small>{e(stat["sub"])}</small>' if stat.get("sub") else "") + "</div>")
    for i, c in enumerate(co):
        f.append(f'<div class="co" id="co{i}" style="left:{c.get("x", 1260)}px;top:{c.get("y", 130 + 200 * i)}px"><span class="t">{e(c["title"])}</span>'
                 + (f'<span class="s">{e(c["sub"])}</span>' if c.get("sub") else "") + "</div>")
    if ring:
        f.append(f'<div id="ring" data-follow="{e(ring["obj"])}" data-anchor="c"><svg width="520" height="520" viewBox="-260 -260 520 520">'
                 f'<g id="rg1"><circle r="200" fill="none" stroke="{col["white"]}" stroke-width="4" stroke-dasharray="40 22"/></g>'
                 f'<g id="rg2"><circle r="232" fill="none" stroke="{col["accent"]}" stroke-width="3" stroke-dasharray="6 14"/></g></svg></div>')
        if ring.get("labels"):
            f.append(f'<div id="ringl" data-follow="{e(ring["obj"])}" data-anchor="t" data-dy="-60"><span id="rl"></span></div>')
    if cnt:
        f.append(f'<div id="spd" style="left:{cnt.get("x", 96)}px;bottom:{cnt.get("bottom", 90)}px"><span class="v" id="kmh">0</span><span class="u">{e(cnt.get("unit", ""))}</span></div>')
    if brand:
        f.append(f'<div id="brand"><span class="b">{e(brand["name"])}</span>' + (f'<span class="s">{e(brand["tag"])}</span>' if brand.get("tag") else "") + "</div>")
    if lock:
        f.append(f'<div id="lock"><span class="b">{e(lock["name"])}</span>' + (f'<span class="s">{e(lock["line"])}</span>' if lock.get("line") else "") + "</div>")
    if matte:
        hud = f'<div id="stage">{back}</div>\n<!--MATTE-->\n<div id="stage2">{"".join(f)}</div><div id="flash"></div>'
        extra["matte.webm"] = matte
    else:
        hud = f'<div id="stage">{back}{"".join(f)}</div><div id="flash"></div>'
    CO = [{"i": i, "obj": c["obj"], "fx": c.get("fx", .5), "fy": c.get("fy", .5), "x": c.get("x", 1260), "y": c.get("y", 130 + 200 * i) + 45,
           "t": c["t"], "until": c.get("until")} for i, c in enumerate(co)]
    j = [STOMP_JS, "const S = " + js({"brand": brand, "player": player, "stat": stat, "ring": ring, "cnt": cnt, "trail": trail, "big": big, "lock": lock}) + ";",
         f"const CO = {js(CO)};", r"""
const $$ = (id) => document.getElementById(id);
const win = (b, t) => b && t >= b.t && (b.until == null || t < b.until);
window.onPlace = (t) => {
  for (const c of CO) {
    const l = $$("l" + c.i), d = $$("d" + c.i), b = boxAt(c.obj, t);
    if (!b || !win(c, t)) { l.setAttribute("d", ""); d.setAttribute("cx", -50); continue; }
    const p = [b[0] + (b[2] - b[0]) * c.fx, b[1] + (b[3] - b[1]) * c.fy];
    l.setAttribute("d", `M${p[0]},${p[1]} L${c.x - 40},${c.y} L${c.x},${c.y}`); d.setAttribute("cx", p[0]); d.setAttribute("cy", p[1]);
  }
  if (S.ring) {
    $$("rg1").setAttribute("transform", `rotate(${t * 220})`); $$("rg2").setAttribute("transform", `rotate(${-t * 140})`);
    if (S.ring.labels) { let s = ""; for (const [lt, txt] of S.ring.labels) if (t >= lt) s = txt; if ($$("rl").textContent !== s) $$("rl").textContent = s; }
  }
  if (S.cnt) { const u = Math.max(0, Math.min(1, (t - S.cnt.t - .05) / (S.cnt.dur || 1.6))); $$("kmh").textContent = String(Math.round(S.cnt.value * (1 - Math.pow(1 - u, 3)))); }
  if (S.trail) {
    if (win(S.trail, t) && boxAt(S.trail.obj, t)) {
      const pts = []; for (let s = Math.max(S.trail.t, t - (S.trail.len || .9)); s <= t; s += 1 / 24) { const b = boxAt(S.trail.obj, s); if (b) pts.push([(b[0] + b[2]) / 2, (b[1] + b[3]) / 2]); }
      $$("tr").setAttribute("points", pts.map(p => p.join(",")).join(" "));
    } else $$("tr").setAttribute("points", "");
  }
};
const hide = (sel) => { const L = [].concat(sel).filter(s => document.querySelector(s)); if (L.length) tl.set(L, {opacity: 0}, 0); };
hide(["#ms", ".co", "#ring", "#ringl", "#spd", "#goal", "#lock", "#pbox", "#ptag"]);
const out = (sel, at, d = .08) => { if (at != null && document.querySelector(sel)) tl.to(sel, {opacity: 0, duration: d}, at - d); };
if (S.brand) { tl.fromTo("#brand", {opacity: 0, x: -20}, {opacity: 1, x: 0, duration: .3}, S.brand.t ?? .15); out("#brand", S.brand.until, .2); }
if (S.player) {
  tl.to(["#pbox", "#ptag"], {opacity: 1, duration: .01}, S.player.t);
  tl.fromTo("#pbox .brk", {scale: 1.4}, {scale: 1, duration: .3, ease: "power3.out"}, S.player.t);
  tl.fromTo("#ptag", {x: -16}, {x: 0, duration: .3, ease: "power3.out"}, S.player.t + .1);
  if (S.player.until != null) tl.to(["#pbox", "#ptag"], {opacity: 0, duration: .05}, S.player.until - .05);
}
if (S.stat) {
  tl.to("#ms", {opacity: 1, duration: .01}, S.stat.t - .05); stomp("#ms span", S.stat.t, 2.2);
  if (document.querySelector("#ms small")) tl.fromTo("#ms small", {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: .2}, S.stat.t + .25);
  out("#ms", S.stat.until);
}
if (S.ring) {
  tl.to(["#ring", "#ringl"].filter(s => document.querySelector(s)), {opacity: 1, duration: .01}, S.ring.t);
  tl.fromTo("#ring svg", {scale: 1.5, opacity: 0}, {scale: 1, opacity: 1, duration: .3, ease: "power3.out"}, S.ring.t);
  out("#ring", S.ring.until); out("#ringl", S.ring.label_until ?? S.ring.until);
}
for (const c of CO) { tl.to(`#co${c.i}`, {opacity: 1, duration: .01}, c.t); tl.fromTo(`#co${c.i}`, {x: 30}, {x: 0, duration: .25, ease: "power3.out"}, c.t); out(`#co${c.i}`, c.until); }
if (S.cnt) { tl.to("#spd", {opacity: 1, duration: .01}, S.cnt.t - .02); stomp("#spd", S.cnt.t, 1.8); out("#spd", S.cnt.until); }
if (S.big) { tl.to("#goal", {opacity: 1, duration: .01}, S.big.t - .03); stomp("#goal span", S.big.t, 2.4); }
if (S.lock) { tl.to("#lock", {opacity: 1, duration: .01}, S.lock.t - .02); stomp("#lock", S.lock.t, 1.6); }
"""]
    sfx = []
    if spec.get("sfx", True):
        hits = [x["t"] for x in (stat, cnt, big, lock) if x]
        sfx = [cue("soft_thump", h - .02, .5) for h in hits] + [cue("ui_pop", c["t"], .35) for c in co]
        if ring:
            sfx.append(cue("ui_whoosh", ring["t"] - .05, .3))
    sfx += audio_cues(spec, base, .55)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .4), extra=extra)
