"""BROADCAST-PACK: a live sports graphics package. A score bug with a running match clock and a score change (flash +
GOAL tab), a LIVE ticker crawling along the bottom, a lower-third that rides the tracked player, a REPLAY bug, and
stinger wipes (a diagonal brand panel sweeping the frame) on chosen cuts. Hebrew mirrors the whole layout (bug on the
right, ticker crawls left-to-right, wipes run the other way).

Spec keys. Required: clip.
  teams      [{"code": "SPA", "color": "#e63b2e", "score": 0}, {"code": "NOR", "color": "#1e6cff", "score": 1}]
  clock      {"start": "88:42", "t": 0}               match clock at t (runs with the video)
  goal       {"team": 0, "t": 11.4, "label": "GOAL"}    score change + flash + tab on the bug
  lower      [{"follow": "player", "anchor": "b", "dx": 0, "dy": 30, "name": "#9 LIOR AVNI", "role": "STRIKER · 3 GOALS",
               "t": .5, "until": 2.5}]
  ticker     {"text": "...", "t": 0, "until": null, "speed": 160, "label": "LIVE"}   speed = px/s crawl; label = the tab text
  bug_t      seconds the score bug slides in (default .3)
  replay     [{"t": 2.6, "until": 11.0, "label": "REPLAY"}]
  wipes      [2.54, 11.125]      cut times: a stinger panel crosses the frame centred on each
  brand      "SPARTA LEAGUE"     text on the wipe panel + bug header
  language   "he" | "en";  pair (Hebrew, default "secular"; see common.HE_PAIRS); Latin: Oswald 700 + Archivo 500
  colors     {"panel": "#0b1f3a", "accent": "#e63b2e", "text": "#ffffff", "gold": "#ffd23f"}
  sfx (true), music, music_vol, vo, plate_vol, name, track
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="BROADCAST-PACK"):
    tp = type_pair(spec, latin=("Oswald", 700, "Archivo", 500), default_pair="secular")
    col = {"panel": "#0b1f3a", "accent": "#e63b2e", "text": "#ffffff", "gold": "#ffd23f", **spec.get("colors", {})}
    rtl = tp["rtl"]
    T = spec.get("teams", [{"code": "HOM", "color": col["accent"], "score": 0}, {"code": "AWY", "color": "#1e6cff", "score": 0}])
    brand = spec.get("brand", "")
    side = "right" if rtl else "left"
    D, Bf = tp["display"], tp["body"]
    teams = "".join(f'<div class="tm"><i style="background:{t["color"]}"></i><b>{e(t["code"])}</b><span class="sc" id="s{k}">{t["score"]}</span></div>'
                    for k, t in enumerate(T))
    h = [f'<div id="bug" style="{side}:70px"><div class="hd">{e(brand)}</div><div class="row">{teams}<div class="clk" id="clk">00:00</div></div>'
         f'<div class="gtab" id="gtab">{e((spec.get("goal") or {}).get("label", "GOAL"))}</div></div>']
    for i, l in enumerate(spec.get("lower", [])):
        h.append(f'<div class="lt" id="lt{i}" data-follow="{e(l["follow"])}" data-anchor="{l.get("anchor", "b")}" data-dx="{l.get("dx", 0)}" data-dy="{l.get("dy", 30)}">'
                 f'<div class="lti"><div class="n">{e(l["name"])}</div><div class="r">{e(l.get("role", ""))}</div><i></i></div></div>')
    for i, r in enumerate(spec.get("replay", [])):
        h.append(f'<div class="rp" id="rp{i}" style="{"left" if rtl else "right"}:70px"><i></i>{e(r.get("label", "REPLAY"))}</div>')
    tk = spec.get("ticker")
    if tk:
        run = e(tk["text"])
        h.append(f'<div id="tk"><div class="lv">{e(tk.get("label", "LIVE"))}</div><div class="cr"><div class="mv" id="mv">'
                 f'<span>{run}</span><span>{run}</span><span>{run}</span></div></div></div>')
    for i, _ in enumerate(spec.get("wipes", [])):
        h.append(f'<div class="wp" id="wp{i}"><div class="band"></div><div class="band b2"></div><div class="wl">{e(brand)}</div></div>')
    css = tp["css"] + f"""
#bug{{position:absolute;top:56px;direction:{tp['dir']};opacity:0;transform-origin:{'100%' if rtl else '0'} 0;scale:1.2}}
#bug .hd{{font-family:"{Bf}",sans-serif;font-weight:{tp['bw']};font-size:20px;letter-spacing:{'0' if rtl else '.22em'};color:{col['text']};background:color-mix(in srgb,{col['accent']} 80%,#000);
  padding:5px 14px;width:max-content}}
#bug .row{{display:flex;align-items:stretch;background:{col['panel']};box-shadow:0 10px 30px rgba(0,0,0,.35)}}
.tm{{display:flex;align-items:center;gap:12px;padding:8px 16px;border-inline-end:1px solid rgba(255,255,255,.12)}}
.tm i{{width:8px;height:34px;display:block}}
.tm b{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:36px;color:{col['text']};letter-spacing:.02em}}
.sc{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:40px;color:{col['text']};min-width:30px;text-align:center;display:inline-block}}
.clk{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:34px;color:{col['gold']};padding:8px 18px;display:flex;align-items:center;direction:ltr;font-variant-numeric:tabular-nums}}
.gtab{{position:absolute;{'left' if rtl else 'right'}:-4px;bottom:-46px;background:{col['gold']};color:{col['panel']};font-family:"{D}",sans-serif;font-weight:{tp['dw']};
  font-size:30px;padding:2px 18px;opacity:0;letter-spacing:.06em}}
.lt{{position:absolute;left:0;top:0;width:0;height:0}}
.lti{{position:absolute;left:0;top:0;transform:translateX(-50%);background:{col['panel']};padding:10px 22px 12px;border-top:4px solid {col['accent']};
  direction:{tp['dir']};white-space:nowrap;box-shadow:0 12px 30px rgba(0,0,0,.35);opacity:0}}
.lti .n{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:40px;color:{col['text']};line-height:1.25}}
.lti .r{{margin-top:4px;line-height:1.3;font-family:"{Bf}",sans-serif;font-weight:{tp['bw']};font-size:22px;color:#cfd8e6;letter-spacing:{'0' if rtl else '.12em'}}}
.lti i{{position:absolute;left:50%;top:-14px;width:0;height:0;border:10px solid transparent;border-bottom-color:{col['accent']};transform:translateX(-50%) translateY(-14px)}}
.rp{{position:absolute;top:60px;display:flex;align-items:center;gap:12px;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:34px;color:{col['text']};
  background:{col['panel']};padding:8px 18px;opacity:0;letter-spacing:.08em;direction:{tp['dir']}}}
.rp i{{width:0;height:0;border-top:12px solid transparent;border-bottom:12px solid transparent;border-{'right' if rtl else 'left'}:18px solid {col['accent']}}}
#tk{{position:absolute;left:0;right:0;bottom:0;height:64px;display:flex;background:{col['panel']};direction:{tp['dir']};opacity:0}}
#tk .lv{{background:{col['accent']};color:#fff;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:30px;display:flex;align-items:center;padding:0 22px;letter-spacing:.1em;z-index:2}}
#tk .cr{{position:relative;flex:1;overflow:hidden}}
#tk .mv{{position:absolute;top:0;height:64px;display:flex;align-items:center;white-space:nowrap;{'right' if rtl else 'left'}:0}}
#tk .mv span{{font-family:"{Bf}",sans-serif;font-weight:{max(400, tp['bw'])};font-size:28px;color:{col['text']};padding:0 60px}}
.wp{{position:absolute;inset:0;pointer-events:none;overflow:hidden}}
.wp .band{{position:absolute;top:-20%;height:140%;width:62%;background:{col['accent']};transform:skewX(-18deg);left:120%}}
.wp .b2{{background:{col['panel']};width:30%}}
.wp .wl{{position:absolute;top:50%;left:120%;transform:translate(-50%,-50%);font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:110px;color:#fff;white-space:nowrap;letter-spacing:.04em}}
"""
    J = {"clock": spec.get("clock", {"start": "00:00", "t": 0}), "goal": spec.get("goal"), "lower": [{"t": l["t"], "until": l.get("until")} for l in spec.get("lower", [])],
         "replay": spec.get("replay", []), "ticker": tk, "wipes": spec.get("wipes", []), "scores": [t["score"] for t in T], "bug_t": spec.get("bug_t", .3)}
    j = [JS_UTIL, f"const J = {js(J)}, RTL = {js(rtl)};", r"""
const $$ = (id) => document.getElementById(id);
const [m0, s0] = J.clock.start.split(":").map(Number);
window.onPlace = (t) => {
  const sec = Math.max(0, m0 * 60 + s0 + Math.floor(t - (J.clock.t || 0)));
  $$("clk").textContent = String(Math.floor(sec / 60)).padStart(2, "0") + ":" + String(sec % 60).padStart(2, "0");
  if (J.goal) { const g = t >= J.goal.t; J.scores.forEach((s, k) => { const v = String(s + (g && k === J.goal.team ? 1 : 0)); if ($$("s" + k).textContent !== v) $$("s" + k).textContent = v; }); }
  if (J.ticker) { const mv = $$("mv"), w = mv.scrollWidth / 3, x = ((t - J.ticker.t) * (J.ticker.speed || 160)) % w;
    mv.style.transform = `translateX(${RTL ? x : -x}px)`; }
  // stinger wipes: a double skewed band crosses the frame in .5 s centred on the cut
  J.wipes.forEach((c, i) => {
    const u = (t - (c - .28)) / .56, el = $$("wp" + i);
    if (u < 0 || u > 1) { el.style.display = "none"; return; }
    el.style.display = "block";
    const p = 120 - 260 * easeInOut(u), q = 120 - 260 * easeInOut(clamp01(u * 1.15 - .08));
    const [a, b] = el.getElementsByClassName("band");
    a.style.left = (RTL ? 100 - p - 62 : p) + "%"; b.style.left = (RTL ? 100 - q - 30 : q + 18) + "%";
    el.getElementsByClassName("wl")[0].style.left = (RTL ? 100 - p - 31 + 62 : p + 31) + "%";
  });
};
tl.fromTo("#bug", {opacity: 0, x: RTL ? 30 : -30}, {opacity: 1, x: 0, duration: .45, ease: "power3.out"}, J.bug_t);
if (J.ticker) { tl.fromTo("#tk", {opacity: 0, y: 64}, {opacity: 1, y: 0, duration: .4, ease: "power3.out"}, J.ticker.t);
  if (J.ticker.until != null) tl.to("#tk", {opacity: 0, y: 64, duration: .3}, J.ticker.until); }
J.lower.forEach((l, i) => {
  tl.fromTo(`#lt${i} .lti`, {opacity: 0, clipPath: "inset(0 50% 0 50%)"}, {opacity: 1, clipPath: "inset(0 0% 0 0%)", duration: .4, ease: "expo.out"}, l.t);
  if (l.until != null) tl.to(`#lt${i} .lti`, {opacity: 0, duration: .15}, l.until - .15);
});
J.replay.forEach((r, i) => { tl.fromTo(`#rp${i}`, {opacity: 0, x: RTL ? -20 : 20}, {opacity: 1, x: 0, duration: .3}, r.t);
  tl.to(`#rp${i}`, {opacity: .35, duration: .5, repeat: Math.max(1, Math.floor((r.until - r.t) / 1)), yoyo: true, ease: "sine.inOut"}, r.t + .3);
  tl.to(`#rp${i}`, {opacity: 0, duration: .2}, r.until); });
if (J.goal) {
  tl.fromTo(".sc", {scale: 1}, {scale: 1.6, duration: .15, yoyo: true, repeat: 1, ease: "power2.out"}, J.goal.t);
  tl.fromTo("#gtab", {opacity: 0, y: -20}, {opacity: 1, y: 0, duration: .3, ease: "back.out(2)"}, J.goal.t + .1);
  tl.to("#bug .row", {backgroundColor: "#ffd23f", duration: .08, yoyo: true, repeat: 5}, J.goal.t);
}
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", c - .3, .6) for c in spec.get("wipes", [])] + [cue("ui_pop", l["t"], .4) for l in spec.get("lower", [])]
        if spec.get("goal"):
            sfx += [cue("stinger", spec["goal"]["t"], .7)]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .5), extra=tp["files"])
