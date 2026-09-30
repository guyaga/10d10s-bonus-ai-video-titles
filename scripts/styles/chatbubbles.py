"""CHAT-BUBBLES: a messenger conversation told over the shot. A contact header slides in, messages pop from their tail
corner with a spring, the other side shows a bouncing typing indicator first, sent messages get double ticks that turn
blue when read, timestamps fade in, and the thread scrolls up as it grows. Messenger-style colours drawn in CSS, no logos.
Hebrew: outgoing ("me") bubbles sit on the LEFT, as in RTL messengers.

Spec keys. Required: clip, messages.
  contact   {"name": "Noa", "status": "online", "initial": "N", "t": .5}
  messages  [{"from": "them" | "me", "text": "...", "t": 1.2, "time": "20:41"}]   'them' shows typing .9 s before t
  area      {"x": 1120, "top": 90, "w": 680, "bottom": 1000}
  read      seconds after a 'me' message that its ticks turn blue (default 1.2)
  until     everything leaves (optional)
  language  "he" | "en";  pair (Hebrew default "secular"); Latin default Manrope 700 + Manrope 500
  colors    {"panel": "rgba(233,226,216,.62)", "me": "#d9fdd3", "them": "#ffffff", "text": "#111b21", "tick": "#53bdeb", "head": "#f0f2f5"}
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="CHAT-BUBBLES"):
    tp = type_pair(spec, latin=("Manrope", 700, "Manrope", 500), default_pair="secular")
    rtl = tp["rtl"]
    col = {"panel": "rgba(233,226,216,.62)", "me": "#d9fdd3", "them": "#ffffff", "text": "#111b21", "tick": "#53bdeb", "head": "#f0f2f5", **spec.get("colors", {})}
    D, B = tp["display"], tp["body"]
    A = {"x": 1120, "top": 90, "w": 680, "bottom": 1000, **spec.get("area", {})}
    ct = spec.get("contact", {"name": "", "t": .4})
    msgs = spec["messages"]
    # physical side of each bubble: outgoing = end side (right in LTR, left in RTL)
    me_side, them_side = ("left", "right") if rtl else ("right", "left")
    rows = []
    for i, m in enumerate(msgs):
        me = m["from"] == "me"
        side = me_side if me else them_side
        ticks = '<span class="tk" id="tk{0}"><svg width="30" height="18" viewBox="0 0 30 18"><path d="M2 9 L7 14 L16 3 M11 14 L13 16 L26 3" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/></svg></span>'.format(i) if me else ""
        rows.append(f'<div class="rw {side}" id="r{i}"><div class="bb {"me" if me else "them"} {side}" id="b{i}"><div class="bt">{e(m["text"])}</div>'
                    f'<div class="meta"><span class="tm">{e(m.get("time", ""))}</span>{ticks}</div></div></div>')
        if not me:
            rows.append(f'<div class="rw {side} ty" id="ty{i}"><div class="bb them {side} typing"><i></i><i></i><i></i></div></div>')
    h = [f'<div id="chat" style="left:{A["x"]}px;top:{A["top"]}px;width:{A["w"]}px;height:{A["bottom"] - A["top"]}px">'
         f'<div id="hd"><div class="av">{e(ct.get("initial", ct.get("name", "?")[:1]))}</div><div><div class="cn">{e(ct.get("name", ""))}</div>'
         f'<div class="cs">{e(ct.get("status", ""))}</div></div></div><div id="thread"><div id="list">{"".join(rows)}</div></div></div>']
    css = tp["css"] + f"""
#chat{{position:absolute;display:flex;flex-direction:column;border-radius:34px;overflow:hidden;background:{col['panel']};backdrop-filter:blur(22px) saturate(1.3);
  box-shadow:0 30px 80px rgba(0,0,0,.35);border:1px solid rgba(255,255,255,.14);direction:{tp['dir']}}}
#hd{{display:flex;align-items:center;gap:18px;padding:22px 26px;background:rgba(240,242,245,.92)}}
.av{{width:62px;height:62px;border-radius:50%;background:linear-gradient(135deg,#d9531e,#b0144f);color:#fff;display:grid;place-items:center;
  font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:30px}}
.cn{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:32px;color:#111b21;line-height:1.2}}
.cs{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:21px;color:#0b6b35}}
#thread{{position:relative;flex:1;overflow:hidden}}
#list{{position:absolute;left:0;right:0;bottom:0;padding:18px 22px 26px;display:flex;flex-direction:column;gap:14px}}
.rw{{display:flex;direction:ltr}} .rw.right{{justify-content:flex-end}} .rw.left{{justify-content:flex-start}}
.bb{{direction:{tp['dir']}}}
.bb{{position:relative;max-width:78%;padding:14px 20px 10px;border-radius:22px;box-shadow:0 2px 3px rgba(0,0,0,.12)}}
.bb.me{{background:{col['me']}}} .bb.them{{background:{col['them']}}}
.bb.right{{border-top-right-radius:6px;transform-origin:100% 0}} .bb.left{{border-top-left-radius:6px;transform-origin:0 0}}
.bt{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:29px;line-height:1.35;color:{col['text']}}}
.meta{{display:flex;justify-content:flex-end;align-items:center;gap:6px;margin-top:2px;direction:ltr}}
.tm{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:17px;color:#4a5a63}}
.tk{{color:#8696a0;display:inline-flex}}
.typing{{display:flex;gap:8px;padding:20px 22px}}
.typing i{{width:12px;height:12px;border-radius:50%;background:#8696a0;display:block}}
.ty{{position:absolute;bottom:26px;{them_side}:22px}}
"""
    # every row's height is unknown until layout, so the thread offset is measured in onPlace from the real DOM
    J = {"m": [{"t": m["t"], "me": m["from"] == "me"} for m in msgs], "ct": ct.get("t", .4), "read": spec.get("read", 1.2), "until": spec.get("until"),
         "tick": col["tick"]}
    j = [JS_UTIL, f"const J = {js(J)};", r"""
const $$ = (id) => document.getElementById(id);
const rows = J.m.map((_, i) => $$("r" + i));
window.onPlace = (t) => {
  // show rows whose time has come; the list is bottom-anchored, so hidden (display none) rows take no space
  J.m.forEach((m, i) => { rows[i].style.display = t >= m.t ? "flex" : "none"; });
  J.m.forEach((m, i) => { if (!m.me) { const ty = $$("ty" + i); ty.style.display = (t >= m.t - .9 && t < m.t) ? "flex" : "none"; } });
  J.m.forEach((m, i) => { if (m.me) $$("tk" + i).style.color = t >= m.t + J.read ? J.tick : "#8696a0"; });
};
tl.fromTo("#chat", {opacity: 0, y: 40, scale: .96}, {opacity: 1, y: 0, scale: 1, duration: .7, ease: "expo.out"}, J.ct);
J.m.forEach((m, i) => {
  tl.fromTo(`#b${i}`, {scale: .3, opacity: 0}, {scale: 1, opacity: 1, duration: .5, ease: "back.out(2)"}, m.t);
  tl.fromTo(`#b${i} .meta`, {opacity: 0}, {opacity: 1, duration: .3}, m.t + .35);
  if (!m.me) tl.to(`#ty${i} i`, {y: -8, duration: .22, yoyo: true, repeat: 3, ease: "sine.inOut", stagger: .1}, m.t - .9);
});
if (J.until != null) tl.to("#chat", {opacity: 0, y: -30, duration: .45, ease: "power3.in"}, J.until - .45);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_pop" if m["from"] == "me" else "glass_ting", m["t"], .45) for m in msgs] + [cue("ui_whoosh", ct.get("t", .4), .3)]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .6), extra=tp["files"])
