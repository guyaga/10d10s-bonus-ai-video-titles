"""APP-UI-POPUPS: phone-style UI floating in the free side of the frame. Notification banners drop in with a spring and
stack (each new one pushes the stack down, older ones scale back and dim), an app card with a progress ring fills up,
and a toast confirms the action. Frosted glass, soft shadows, app-icon gradients drawn in CSS (no logos).
Hebrew: RTL text, the stack sits on the chosen side and aligns to it.

Spec keys. Required: clip, notes.
  notes     [{"app": "Wallet", "icon": "₪" | a letter | digits (glyphs must exist in the chosen font), "grad": ["#34c759", "#0a8f3a"], "title": "...", "body": "...",
              "time": "now", "t": 1.0}]
  card      {"title": "Your order", "sub": "On the way · 12 min", "ring": .72, "t": 5.0, "label": "72%"}   optional
  toast     {"text": "Payment sent", "t": 7.8}                                                    optional
  area      {"side": "R", "x": 1160, "top": 110, "w": 620}     stack position (x = left edge in px)
  until     everything leaves (optional)
  language  "he" | "en";  pair (Hebrew default "secular"); Latin default Manrope 700 + Manrope 500
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="APP-UI-POPUPS"):
    tp = type_pair(spec, latin=("Manrope", 700, "Manrope", 500), default_pair="secular")
    rtl = tp["rtl"]
    D, B = tp["display"], tp["body"]
    A = {"side": "R", "x": 1160, "top": 110, "w": 620, **spec.get("area", {})}
    notes = spec["notes"]
    h = [f'<div id="ui" style="left:{A["x"]}px;top:{A["top"]}px;width:{A["w"]}px">']
    for i, n in enumerate(notes):
        g = n.get("grad", ["#5b8cff", "#3a55d9"])
        h.append(f'<div class="nt" id="n{i}"><div class="ic" style="background:linear-gradient(135deg,{g[0]},{g[1]})">{e(n.get("icon", ""))}</div>'
                 f'<div class="nb"><div class="nh"><span class="na">{e(n.get("app", ""))}</span><span class="tm">{e(n.get("time", "now"))}</span></div>'
                 f'<div class="ntl">{e(n.get("title", ""))}</div><div class="nbd">{e(n.get("body", ""))}</div></div></div>')
    h.append("</div>")
    cd = spec.get("card")
    if cd:
        R = 46
        C = 2 * 3.14159 * R
        h.append(f'<div id="card" style="left:{A["x"]}px;width:{A["w"]}px"><div class="cr"><svg width="120" height="120" viewBox="0 0 120 120">'
                 f'<circle cx="60" cy="60" r="{R}" fill="none" stroke="rgba(255,255,255,.14)" stroke-width="12"/>'
                 f'<circle id="ring" cx="60" cy="60" r="{R}" fill="none" stroke="#35d07f" stroke-width="12" stroke-linecap="round" pathLength="1" '
                 f'stroke-dasharray="1" stroke-dashoffset="1" transform="rotate(-90 60 60)"/></svg><div class="rl" id="rl">0%</div></div>'
                 f'<div class="cb"><div class="ct">{e(cd["title"])}</div><div class="cs">{e(cd.get("sub", ""))}</div><div class="bar"><i id="cbar"></i></div></div></div>')
    ts = spec.get("toast")
    if ts:
        h.append(f'<div id="toast"><i><svg width="22" height="22" viewBox="0 0 24 24"><path d="M4 12.5 9.5 18 20 6.5" fill="none" stroke="#fff" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/></svg></i><span>{e(ts["text"])}</span></div>')
    css = tp["css"] + f"""
#ui{{position:absolute;direction:{tp['dir']}}}
.nt{{position:absolute;left:0;right:0;top:0;display:flex;gap:18px;align-items:flex-start;padding:20px 24px;border-radius:30px;
  background:rgba(246,247,250,.94);backdrop-filter:blur(24px) saturate(1.6);box-shadow:0 18px 50px rgba(0,0,0,.22);transform-origin:50% 0}}
.ic{{flex:none;width:64px;height:64px;border-radius:16px;display:grid;place-items:center;color:#fff;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:32px}}
.nb{{flex:1;min-width:0}}
.nh{{display:flex;justify-content:space-between;align-items:center;font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:20px;color:#4b5563}}
.na{{letter-spacing:{'0' if rtl else '.04em'};text-transform:{'none' if rtl else 'uppercase'}}}
.ntl{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:30px;color:#0d1117;line-height:1.25;margin-top:2px}}
.nbd{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:25px;color:#30363d;line-height:1.3}}
#card{{position:absolute;top:620px;display:flex;gap:26px;align-items:center;padding:26px 30px;border-radius:32px;background:rgba(12,14,20,.72);
  backdrop-filter:blur(20px);box-shadow:0 24px 60px rgba(0,0,0,.3);direction:{tp['dir']}}}
.cr{{position:relative;width:120px;height:120px;flex:none}}
.rl{{position:absolute;inset:0;display:grid;place-items:center;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:30px;color:#fff;direction:ltr}}
.cb{{flex:1}}
.ct{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:34px;color:#fff;line-height:1.25}}
.cs{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:24px;color:#b9c1cc;margin-top:4px}}
.bar{{height:8px;border-radius:8px;background:rgba(255,255,255,.14);margin-top:16px;overflow:hidden}}
.bar i{{display:block;height:100%;background:#35d07f;border-radius:8px;transform-origin:{'100%' if rtl else '0'} 50%}}
#toast{{position:absolute;left:{A['x'] + A['w'] / 2}px;top:920px;display:flex;gap:14px;align-items:center;padding:16px 30px;
  border-radius:999px;background:#0d1117;color:#fff;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:30px;white-space:nowrap;direction:{tp['dir']};
  box-shadow:0 16px 40px rgba(0,0,0,.35)}}
#toast i{{font-style:normal;width:40px;height:40px;border-radius:50%;background:#35d07f;display:grid;place-items:center;font-size:24px}}
"""
    J = {"n": [n["t"] for n in notes], "card": cd and {"t": cd["t"], "ring": cd.get("ring", .7)}, "toast": ts and ts["t"], "until": spec.get("until")}
    j = [JS_UTIL, f"const J = {js(J)};", r"""
const $$ = (id) => document.getElementById(id);
// each banner drops in with a spring; older banners slide down one slot, scale back and dim (the iOS stack)
const SLOT = 150;
J.n.forEach((t0, i) => {
  tl.fromTo(`#n${i}`, {y: -170, opacity: 0, scale: .92}, {y: 0, opacity: 1, scale: 1, duration: .75, ease: "back.out(1.4)"}, t0);
  for (let k = 0; k < i; k++) {
    const depth = i - k;
    tl.to(`#n${k}`, {y: depth * SLOT * .82, scale: 1 - depth * .05, opacity: depth >= 3 ? 0 : 1, duration: .6, ease: "power3.out"}, t0);
  }
});
if (J.card) {
  const c = J.card;
  tl.fromTo("#card", {opacity: 0, y: 40, scale: .95}, {opacity: 1, y: 0, scale: 1, duration: .7, ease: "expo.out"}, c.t);
  tl.fromTo("#ring", {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 1 - c.ring}, duration: 1.8, ease: "power2.inOut"}, c.t + .3);
  tl.fromTo("#cbar", {scaleX: 0}, {scaleX: c.ring, duration: 1.8, ease: "power2.inOut"}, c.t + .3);
  window.onPlace = (t) => { $$("rl").textContent = Math.round(100 * c.ring * easeInOut((t - (c.t + .3)) / 1.8)) + "%"; };
}
if (J.toast != null) tl.fromTo("#toast", {opacity: 0, y: 30, scale: .8, xPercent: -50}, {opacity: 1, y: 0, scale: 1, xPercent: -50, duration: .5, ease: "back.out(2.2)"}, J.toast);
if (J.until != null) tl.to("#ui, #card, #toast", {opacity: 0, y: -20, duration: .4, ease: "power2.in", stagger: .05}, J.until - .5);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("glass_ting", t, .5) for t in J["n"]]
        if cd:
            sfx.append(cue("ui_whoosh", cd["t"], .35))
        if ts:
            sfx.append(cue("chime", ts["t"], .5))
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .6), extra=tp["files"])
