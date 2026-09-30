"""SOCIAL-CTA: the YouTube / social call to action. A channel chip (avatar + handle + follower count) slides in; later a
red SUBSCRIBE pill pops, a cursor glides in and clicks it (press + ripple), the pill flips to a grey SUBSCRIBED with a
check, the bell rings with sparkles, and a like button pops with a count-up. Everything is drawn in CSS/SVG, no platform
logos. Hebrew mirrors the layout and uses Hebrew button labels.

Spec keys. Required: clip.
  channel   {"name": "סטודיו נורת׳", "handle": "@studio.north", "subs": 128400, "initial": "N", "t": .8, "until": 4.6}
  cta       {"t": 6.2, "click": 7.2, "label": "הירשמו", "done": "נרשמתם", "bell": true, "like": 12400}
  pos       {"x": 150, "y": 760}   where the CTA row sits (left edge / top in px)
  language  "he" | "en";  pair (Hebrew default "secular"); Latin default Manrope 700 + Manrope 500
  colors    {"red": "#ff0033", "done": "#3a3f47", "panel": "rgba(12,14,18,.72)"}
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)

BELL = ('<svg width="44" height="44" viewBox="0 0 24 24"><path d="M12 22a2.5 2.5 0 0 0 2.4-2h-4.8A2.5 2.5 0 0 0 12 22Zm7-6V11a7 7 0 0 0-5.5-6.8V3.5a1.5 1.5 0 0 0-3 0v.7'
        'A7 7 0 0 0 5 11v5l-2 2v1h18v-1l-2-2Z" fill="#fff"/></svg>')
THUMB = ('<svg width="40" height="40" viewBox="0 0 24 24"><path d="M2 21h4V9H2v12Zm20-11a2 2 0 0 0-2-2h-6.3l1-4.6v-.3a1.5 1.5 0 0 0-.5-1.1L13.2 1 6.6 7.6A2 2 0 0 0 6 9v10a2 2 0 0 0 2 2h9'
         'a2 2 0 0 0 1.8-1.2l3-7.1c.1-.2.2-.5.2-.7v-2Z" fill="#fff"/></svg>')
CHECK = ('<svg width="30" height="30" viewBox="0 0 24 24"><path d="M4 12.5 9.5 18 20 6.5" fill="none" stroke="#fff" stroke-width="3.2" '
         'stroke-linecap="round" stroke-linejoin="round"/></svg>')
CURSOR = ('<svg width="54" height="54" viewBox="0 0 24 24"><path d="M5 2.5v17.2l4.6-4.3 2.9 6.6 2.7-1.2-2.9-6.5 6.3-.4Z" fill="#fff" stroke="#111" stroke-width="1.3" '
          'stroke-linejoin="round"/></svg>')


def build(spec, base, style="SOCIAL-CTA"):
    tp = type_pair(spec, latin=("Manrope", 700, "Manrope", 500), default_pair="secular")
    rtl = tp["rtl"]
    col = {"red": "#ff0033", "done": "#3a3f47", "panel": "rgba(12,14,18,.72)", **spec.get("colors", {})}
    D, B = tp["display"], tp["body"]
    ch = spec.get("channel")
    cta = {"t": 6.2, "click": 7.2, "label": "SUBSCRIBE" if not rtl else "הירשמו", "done": "SUBSCRIBED" if not rtl else "נרשמתם", "bell": True, "like": None,
           **spec.get("cta", {})}
    P = {"x": 150, "y": 760, **spec.get("pos", {})}
    h = []
    if ch:
        h.append(f'<div id="chip" style="left:{P["x"]}px;top:{P["y"] - 150}px"><div class="av">{e(ch.get("initial", ch["name"][:1]))}</div>'
                 f'<div><div class="cn">{e(ch["name"])}</div><div class="ch2"><span>{e(ch.get("handle", ""))}</span><span class="dot">·</span>'
                 f'<span class="subs"><b id="subs">0</b> {"מנויים" if rtl else "subscribers"}</span></div></div></div>')
    like = f'<div id="like"><div class="lk">{THUMB}</div><b id="lkn">0</b></div>' if cta.get("like") else ""
    bell = f'<div id="bell"><div class="bi">{BELL}</div><i class="sp s1"></i><i class="sp s2"></i><i class="sp s3"></i></div>' if cta.get("bell") else ""
    h.append(f'<div id="row" style="left:{P["x"]}px;top:{P["y"]}px"><div id="sub"><span class="l1">{e(cta["label"])}</span>'
             f'<span class="l2">{CHECK}&nbsp;{e(cta["done"])}</span><i id="rip"></i></div>{bell}{like}</div>'
             f'<div id="cur">{CURSOR}</div>')
    css = tp["css"] + f"""
#chip{{position:absolute;display:flex;gap:18px;align-items:center;padding:14px 26px 14px 14px;border-radius:999px;background:{col['panel']};
  backdrop-filter:blur(16px);box-shadow:0 16px 40px rgba(0,0,0,.3);direction:{tp['dir']}}}
.av{{width:78px;height:78px;border-radius:50%;background:linear-gradient(135deg,#ff8a3d,#ff2e63);display:grid;place-items:center;color:#fff;
  font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:38px;box-shadow:0 0 0 4px rgba(255,255,255,.9)}}
.cn{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:36px;color:#fff;line-height:1.2}}
.ch2{{display:flex;gap:10px;font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:23px;color:#c8ced6}}
.ch2 span:first-child{{direction:ltr;unicode-bidi:isolate}}
.ch2 b{{font-weight:inherit;color:#fff;direction:ltr;display:inline-block}}
#row{{position:absolute;display:flex;gap:18px;align-items:center;direction:ltr}}
#sub span{{direction:{tp['dir']}}}
#sub{{position:relative;overflow:hidden;height:96px;min-width:330px;border-radius:999px;background:{col['red']};display:grid;box-shadow:0 18px 40px rgba(255,0,51,.35)}}
#sub span{{grid-area:1/1;display:flex;align-items:center;justify-content:center;padding:0 46px;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:40px;color:#fff;
  letter-spacing:{'0' if rtl else '.06em'};white-space:nowrap}}
#sub .l2{{background:{col['done']};opacity:0}}
#rip{{position:absolute;left:50%;top:50%;width:40px;height:40px;margin:-20px;border-radius:50%;background:rgba(255,255,255,.55);opacity:0}}
#bell{{position:relative;width:96px;height:96px;border-radius:50%;background:{col['panel']};display:grid;place-items:center;backdrop-filter:blur(12px)}}
.bi{{transform-origin:50% 12%;display:grid}}
.sp{{position:absolute;width:10px;height:10px;border-radius:50%;background:#ffd23f;opacity:0}}
.s1{{left:6px;top:14px}} .s2{{right:4px;top:10px}} .s3{{right:14px;bottom:6px}}
#like{{display:flex;align-items:center;gap:12px;height:96px;padding:0 30px;border-radius:999px;background:{col['panel']};backdrop-filter:blur(12px)}}
#like b{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:36px;color:#fff;direction:ltr;font-variant-numeric:tabular-nums}}
.lk{{display:grid;transform-origin:30% 80%}}
#cur{{position:absolute;left:0;top:0;filter:drop-shadow(0 6px 10px rgba(0,0,0,.4))}}
"""
    J = {"ch": ch and {"t": ch.get("t", .8), "until": ch.get("until"), "subs": ch.get("subs", 0)}, "cta": cta, "P": P, "rtl": rtl}
    j = [JS_UTIL, f"const J = {js(J)};", r"""
const $$ = (id) => document.getElementById(id);
const C = J.cta, P = J.P;
const fmt = (n) => n >= 1e6 ? (n / 1e6).toFixed(1) + "M" : n >= 1e3 ? (n / 1e3).toFixed(1) + "K" : String(Math.round(n));
window.onPlace = (t) => {
  if (J.ch) $$("subs").textContent = fmt(J.ch.subs * easeOut3((t - (J.ch.t + .4)) / 1.4) + (t > C.click ? 1 : 0));
  if (C.like) $$("lkn").textContent = fmt(C.like * easeOut3((t - (C.click + 1.0)) / 1.2));
};
if (J.ch) {
  tl.fromTo("#chip", {opacity: 0, x: J.rtl ? 60 : -60}, {opacity: 1, x: 0, duration: .7, ease: "expo.out"}, J.ch.t);
  tl.fromTo("#chip .av", {scale: .4, rotate: -30}, {scale: 1, rotate: 0, duration: .6, ease: "back.out(2.4)"}, J.ch.t + .1);
  if (J.ch.until != null) tl.to("#chip", {opacity: 0, x: J.rtl ? 40 : -40, duration: .4, ease: "power3.in"}, J.ch.until - .4);
}
tl.fromTo("#sub", {scale: 0, opacity: 0}, {scale: 1, opacity: 1, duration: .55, ease: "back.out(2.2)"}, C.t);
if (C.bell) tl.fromTo("#bell", {scale: 0}, {scale: 1, duration: .5, ease: "back.out(2.4)"}, C.t + .15);
if (C.like) tl.fromTo("#like", {scale: 0}, {scale: 1, duration: .5, ease: "back.out(2.4)"}, C.t + .3);
// cursor: glides in from below, eases onto the button, clicks
const bx = P.x + 165, by = P.y + 60;
tl.fromTo("#cur", {x: bx + 260, y: by + 260, opacity: 0}, {x: bx + 60, y: by + 30, opacity: 1, duration: .5, ease: "power2.out"}, C.click - .9);
tl.to("#cur", {x: bx, y: by, duration: .35, ease: "power3.inOut"}, C.click - .4);
tl.to("#cur", {scale: .82, duration: .08, yoyo: true, repeat: 1}, C.click);
tl.to("#sub", {scale: .93, duration: .08, yoyo: true, repeat: 1}, C.click);
tl.fromTo("#rip", {scale: 0, opacity: .8}, {scale: 9, opacity: 0, duration: .6, ease: "power2.out"}, C.click);
tl.to("#sub .l1", {opacity: 0, duration: .15}, C.click + .08);
tl.to("#sub .l2", {opacity: 1, duration: .2}, C.click + .08);
tl.to("#sub", {boxShadow: "0 18px 40px rgba(0,0,0,.25)", duration: .3}, C.click + .08);
tl.to("#cur", {x: bx + 150, y: by + 160, opacity: 0, duration: .6, ease: "power2.in"}, C.click + .7);
if (C.bell) {
  tl.to("#bell .bi", {keyframes: [{rotate: 22, duration: .08}, {rotate: -20, duration: .1}, {rotate: 14, duration: .1}, {rotate: -8, duration: .1}, {rotate: 0, duration: .12}]}, C.click + .45);
  tl.fromTo("#bell .sp", {scale: 0, opacity: 1}, {scale: 1.6, opacity: 0, duration: .6, ease: "power2.out", stagger: .06}, C.click + .5);
}
if (C.like) tl.to("#like .lk", {keyframes: [{scale: 1.35, rotate: -14, duration: .14}, {scale: 1, rotate: 0, duration: .25, ease: "back.out(3)"}]}, C.click + 1.0);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_pop", cta["t"], .5), cue("soft_click", cta["click"], .8), cue("chime", cta["click"] + .45, .5)]
        if ch:
            sfx.append(cue("ui_whoosh", ch.get("t", .8), .35))
        if cta.get("like"):
            sfx.append(cue("ui_pop", cta["click"] + 1.0, .4))
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .85), extra=tp["files"])
