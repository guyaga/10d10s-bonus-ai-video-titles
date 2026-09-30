"""LISTING-SPECS: the real-estate listing package. A listing title block (status pill, property title, address rule), tracked
pins with leader labels on the house and its features, a glass spec bar whose cells stagger in with line icons and
count-up numbers (rooms, baths, built m², plot m²), and an asking price that counts up to its figure. Hebrew (RTL) or English.

Spec keys. Required: clip, title.
  status     "למכירה · בלעדי"   title  "וילה בקיסריה"   address  "רחוב הדקל 12 · קיסריה"
  specs      [{"icon": "bed|bath|area|plot|pool|car|floors|view", "n": 6, "unit": "חדרים"}, ...]   up to 5; t_specs (default 2.4)
  price      {"n": 12900000, "unit": "ש״ח", "label": "מחיר מבוקש", "t": 5.4}      (write currency in words for Hebrew)
  pins       [{"obj": "villa", "anchor": "t", "dx": 0, "dy": 60, "label": "חזית דרום · נוף לים", "t": 3.6, "side": "L|R"}]   needs "track"
  agent      "נוף ים נדל״ן"   small brand bug in the corner (optional)
  head_side  "right" | "left"   corner of the title block (default: the reading start). Keep it in the sky, off the house.
  language   "he" | "en";  pair (Hebrew, default "suez"); Latin: DM Serif Display + Manrope
  colors     {"accent": "#e3b35d"}
  sfx (true), plate_vol, music, music_vol, name, track
"""
from styles.common import (audio_cues, cue, e, js, project_dir, res, tracks, type_pair)

ICON = {  # 48x48 line icons, stroke = currentColor
    "bed": '<path d="M5 34V14M5 26h38v8M43 34v-8a6 6 0 0 0-6-6H20v6M11 20a3 3 0 1 0 6 0 3 3 0 1 0-6 0"/>',
    "bath": '<path d="M6 24h36v4a10 10 0 0 1-10 10H16A10 10 0 0 1 6 28zM12 24V12a4 4 0 0 1 8 0M14 38l-2 4M34 38l2 4"/>',
    "area": '<path d="M8 8h32v32H8zM8 16h6M8 24h4M8 32h6M16 8v6M24 8v4M32 8v6"/>',
    "plot": '<path d="M6 36l10-24 16 6 10 18zM16 12l2 10 14-4M18 22l-6 14"/>',
    "pool": '<path d="M6 30c4 3 8 3 12 0s8-3 12 0 8 3 12 0M6 38c4 3 8 3 12 0s8-3 12 0 8 3 12 0M16 26V10a4 4 0 0 1 8 0M30 26V10a4 4 0 0 1 8 0M16 16h14M16 22h14"/>',
    "car": '<path d="M8 30l4-11a4 4 0 0 1 4-3h16a4 4 0 0 1 4 3l4 11v8H8zM8 30h32M14 38v3M34 38v3"/>',
    "floors": '<path d="M24 6L6 15l18 9 18-9zM6 24l18 9 18-9M6 33l18 9 18-9"/>',
    "view": '<path d="M4 34l12-14 8 8 8-12 12 18zM36 10a4 4 0 1 0 0 .1"/>',
}


def build(spec, base, style="LISTING-SPECS"):
    tp = type_pair(spec, latin=("DM Serif Display", 400, "Manrope", 500), default_pair="suez")
    rtl = tp["rtl"]
    col = {"accent": "#e3b35d", **spec.get("colors", {})}
    specs = spec.get("specs", [])[:5]
    ts = spec.get("t_specs", 2.4)
    price = spec.get("price")
    pins = spec.get("pins", [])
    side = spec.get("head_side", "right" if rtl else "left")      # the title block's corner (keep it in the sky, off the building)
    other = "left" if side == "right" else "right"
    css = tp["css"] + f"""
#tscrim{{position:absolute;{side}:0;top:0;width:1000px;height:440px;background:radial-gradient(ellipse at {'100%' if side == 'right' else '0%'} 0%,rgba(10,8,6,.66),rgba(10,8,6,.3) 45%,transparent 72%)}}
#head{{position:absolute;top:80px;{side}:110px;direction:{tp['dir']};display:flex;flex-direction:column;align-items:flex-start}}
#st{{display:inline-block;padding:8px 20px;border-radius:30px;background:{col['accent']};color:#1a1408;font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:26px}}
#tt{{margin-top:14px;font-family:"{tp['display']}",serif;font-weight:{tp['dw']};font-size:104px;line-height:1.05;color:#fff;text-shadow:0 6px 34px rgba(0,0,0,.5);overflow:hidden}}
#tt span{{display:block}}
#ad{{margin-top:10px;display:flex;align-items:center;gap:18px;font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:32px;color:#fff;
  text-shadow:0 2px 10px rgba(0,0,0,.85),0 0 24px rgba(0,0,0,.5)}}
#ad i{{width:90px;height:2px;background:{col['accent']};transform-origin:{'100%' if rtl else '0%'} 50%}}
#bar{{position:absolute;left:110px;right:110px;bottom:70px;display:flex;direction:{tp['dir']};border-radius:22px;overflow:hidden;
  background:rgba(12,14,18,.7);border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(14px);-webkit-backdrop-filter:blur(14px)}}
.cell{{flex:1;display:flex;align-items:center;gap:18px;padding:24px 30px;{('border-left' if rtl else 'border-right')}:1px solid rgba(255,255,255,.14);opacity:0}}
.cell:last-child{{{('border-left' if rtl else 'border-right')}:none}}
.cell svg{{width:52px;height:52px;flex:none;stroke:{col['accent']};fill:none;stroke-width:2.2;stroke-linecap:round;stroke-linejoin:round}}
.cell b{{font-family:"{tp['display']}",serif;font-weight:{tp['dw']};font-size:54px;line-height:1;color:#fff;font-variant-numeric:tabular-nums;direction:ltr;unicode-bidi:isolate}}
.cell span{{font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:26px;color:#fff;line-height:1.2}}
#price{{position:absolute;{other}:110px;bottom:230px;direction:{tp['dir']};text-align:{other};opacity:0}}
#price small{{display:block;margin-bottom:22px;line-height:1.3;font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:28px;color:rgba(255,255,255,.88);text-shadow:0 2px 12px rgba(0,0,0,.7)}}
#price div{{font-family:"{tp['display']}",serif;font-weight:{tp['dw']};font-size:84px;line-height:1.1;color:{col['accent']};text-shadow:0 4px 26px rgba(0,0,0,.55);white-space:nowrap}}
#price div b{{font-weight:inherit;font-variant-numeric:tabular-nums;direction:ltr;unicode-bidi:isolate}}
#price div span{{font-size:.5em;color:#fff;margin-{'right' if rtl else 'left'}:.3em}}
.pin{{position:absolute;left:0;top:0;width:0;height:0;opacity:0}}
.pin .dot{{position:absolute;left:-11px;top:-11px;width:22px;height:22px;border-radius:50%;background:#fff;box-shadow:0 0 0 7px rgba(255,255,255,.28),0 4px 14px rgba(0,0,0,.4)}}
.pin .ld{{position:absolute;top:-1px;height:2px;width:110px;background:#fff}}
.pin .lb{{position:absolute;top:-28px;white-space:nowrap;padding:10px 20px;border-radius:12px;background:rgba(12,14,18,.62);border:1px solid rgba(255,255,255,.22);
  backdrop-filter:blur(10px);font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:28px;color:#fff;direction:{tp['dir']}}}
#agent{{position:absolute;{other}:110px;top:84px;font-family:"{tp['display']}",serif;font-size:34px;color:#fff;opacity:.9;text-shadow:0 2px 14px rgba(0,0,0,.6)}}
"""
    cells = "".join(f'<div class="cell" id="c{i}"><svg viewBox="0 0 48 48">{ICON.get(s.get("icon", "area"), ICON["area"])}</svg>'
                    f'<div><b id="cn{i}">0</b><span> {e(s.get("unit", ""))}</span></div></div>' for i, s in enumerate(specs))
    pins_html = ""
    for i, p in enumerate(pins):
        L = p.get("side", "R") == "L"
        pins_html += (f'<div class="pin" id="p{i}" data-follow="{e(p["obj"])}" data-anchor="{p.get("anchor", "c")}" data-dx="{p.get("dx", 0)}" data-dy="{p.get("dy", 0)}">'
                      f'<i class="ld" style="{"right" if L else "left"}:12px"></i><i class="dot"></i>'
                      f'<div class="lb" style="{"right" if L else "left"}:130px">{e(p["label"])}</div></div>')
    hud = ('<div id="tscrim"></div>'
           f'<div id="head"><div id="st">{e(spec.get("status", ""))}</div><div id="tt"><span>{e(spec["title"])}</span></div>'
           f'<div id="ad"><i></i><span>{e(spec.get("address", ""))}</span></div></div>'
           + pins_html
           + (f'<div id="price"><small>{e(price.get("label", ""))}</small><div><b id="pn">0</b><span>{e(price.get("unit", ""))}</span></div></div>' if price else "")
           + (f'<div id="bar">{cells}</div>' if specs else "")
           + (f'<div id="agent">{e(spec["agent"])}</div>' if spec.get("agent") else ""))
    J = {"S": [{"n": s["n"], "t": ts + i * .22} for i, s in enumerate(specs)], "P": price, "pins": [{"t": p["t"], "L": p.get("side", "R") == "L"} for p in pins],
         "rtl": rtl, "agent": bool(spec.get("agent"))}
    j = [f"const R = {js(J)};", r"""
const fmt = (v) => Math.round(v).toLocaleString("en-US");
tl.fromTo("#tscrim", {opacity: 0}, {opacity: 1, duration: .8}, .1);
tl.fromTo("#st", {opacity: 0, y: -12, scale: .9}, {opacity: 1, y: 0, scale: 1, duration: .5, ease: "back.out(2)"}, .4);
tl.fromTo("#tt span", {yPercent: 105}, {yPercent: 0, duration: .9, ease: "expo.out"}, .6);
tl.fromTo("#ad i", {scaleX: 0}, {scaleX: 1, duration: .7, ease: "expo.out"}, 1.0);
tl.fromTo("#ad span", {opacity: 0, x: R.rtl ? 20 : -20}, {opacity: 1, x: 0, duration: .6, ease: "power3.out"}, 1.1);
if (R.agent) tl.fromTo("#agent", {opacity: 0}, {opacity: .9, duration: .8}, 1.2);
if (R.S.length) tl.fromTo("#bar", {y: 60, opacity: 0}, {y: 0, opacity: 1, duration: .7, ease: "power3.out"}, R.S[0].t - .3);
R.S.forEach((s, i) => tl.fromTo("#c" + i, {opacity: 0, y: 18}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, s.t));
R.pins.forEach((p, i) => {
  tl.set("#p" + i, {opacity: 1}, p.t);
  tl.fromTo(`#p${i} .dot`, {scale: 0}, {scale: 1, duration: .45, ease: "back.out(3)"}, p.t);
  tl.fromTo(`#p${i} .ld`, {scaleX: 0}, {scaleX: 1, duration: .45, ease: "power3.out", transformOrigin: p.L ? "100% 50%" : "0% 50%"}, p.t + .2);
  tl.fromTo(`#p${i} .lb`, {opacity: 0, x: p.L ? 16 : -16}, {opacity: 1, x: 0, duration: .45, ease: "power3.out"}, p.t + .45);
});
if (R.P) tl.fromTo("#price", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .7, ease: "power3.out"}, R.P.t);
window.onPlace = (t) => {
  R.S.forEach((s, i) => { const u = Math.max(0, Math.min(1, (t - s.t - .1) / .9)), v = s.n * (1 - Math.pow(1 - u, 3));
    const el = document.getElementById("cn" + i), txt = fmt(v); if (el.textContent !== txt) el.textContent = txt; });
  if (R.P) { const u = Math.max(0, Math.min(1, (t - R.P.t - .1) / 1.3)), v = R.P.n * (1 - Math.pow(1 - u, 4));
    const el = document.getElementById("pn"), txt = fmt(v); if (el.textContent !== txt) el.textContent = txt; }
};
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", .5, .25)] + [cue("soft_tick", ts + i * .22, .3) for i in range(len(specs))] + [cue("ui_pop", p["t"], .25) for p in pins]
        if price:
            sfx.append(cue("chime", price.get("t", 5.4) + 1.3, .25))
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .7), extra=tp["files"])
