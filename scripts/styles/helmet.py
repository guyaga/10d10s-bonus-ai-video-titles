"""HUD-HELMET: holographic visor HUD (original design, Iron-Man-like): boot ring, a reticle of counter-rotating rings on
the tracked eyes, a vitals cluster (heart-rate ring + two mini gauges) and a message panel tilted in 3D, radar, compass
tape, data stream, a red alert state, AI assistant line, target lock, confirm prompt and a final word. Hebrew or English.
An optional AI voice file drives a live voice meter (envelope computed from the audio).

Spec keys. Required: clip, track. Every block below is optional; omit it to drop it, or set "t"/"until" to move it.
  eyes / face    tracked object names (default "eyes" / "face"); the reticle sits on eyes, parallax follows face
  language       "he" (RTL, Assistant) | "en"
  colors         {"hud": "#6fe3ff", "text": "#e6fbff", "alert": "#ff4a5a", "ok": "#ffb547"}
  system         short OS tag in the data stream, e.g. "VNG-OS"
  boot           {"title", "sub", "ok", "t": .5, "until": 3.85}
  vitals         {"t": 4.1, "hr_label", "hr_unit", "g1_label", "g1_value", "g2_label", "g2_value",
                  "bpm": [[0,72],[11,72],[15,118],[18,94],[23,102]]}          heart-rate keyframes (t, bpm)
  radar          {"t": 5.2, "label", "contacts": 3, "contacts_at": 11}
  compass        {"t": 1.4, "label", "heading": 72}
  messages       {"t": 7.0, "until": 10.9, "header", "lines": [{"text", "t"}], "cps": 16}
  alert          {"t": 11, "until": 15, "title", "sub"}                      turns the HUD red
  ai             {"t": 15.2, "until": 17.9, "label", "text", "cps": 13}
  lock           {"t": 18.15, "until": 21, "title", "done", "dur": 2.1}
  confirm        {"t": 21.1, "until": 23, "question", "ok", "ok_at": 22.3}
  final          {"t": 23.1, "text"}
  voice          {"file": "ora.mp3", "label": "ORA · VOICE", "vol": 1}      optional AI voice + meter; other sfx duck
  sfx            true (default) = the timed UI sound design;  plate_vol, music, music_vol, name
"""
from styles.common import (audio_cues, cue, e, envelope, fonts, js, project_dir, res, scale_cues, tracks)

HE = dict(
    boot={"title": "מערכת ואנגארד מופעלת", "sub": "סנכרון עצבי", "ok": "כל המערכות תקינות", "t": .5, "until": 3.85},
    vitals={"t": 4.1, "hr_label": "דופק", "hr_unit": "פעימות לדקה", "g1_label": "חמצן", "g1_value": "98%", "g2_label": "חליפה", "g2_value": "100%",
            "bpm": [[0, 72], [11, 72], [15, 118], [18, 94], [21, 94], [23, 102]]},
    radar={"t": 5.2, "label": "מכ״ם · {n} מגעים", "contacts": 3, "contacts_at": 11},
    compass={"t": 1.4, "label": "כיוון", "heading": 72},
    messages={"t": 7.0, "until": 10.9, "header": "הודעה נכנסת · מפקדה", "cps": 16,
              "lines": [{"text": "ואנגארד, כאן מפקדה.", "t": 7.5}, {"text": "זוהתה תנועה חשודה בגזרה 07.", "t": 8.8}, {"text": "המשך בזהירות.", "t": 10.3}]},
    alert={"t": 11, "until": 15, "title": "⚠ אזהרה · 2 עוינים", "sub": "רחפן אחד · טווח 140 מ׳ · כיוון 072°"},
    ai={"t": 15.2, "until": 17.9, "label": "עוזר החליפה", "text": "נשום עמוק. אני איתך.", "cps": 13},
    lock={"t": 18.15, "until": 21, "title": "נעילת מטרה", "done": "המטרה ננעלה", "dur": 2.1},
    confirm={"t": 21.1, "until": 23, "question": "מערכת הנשק זמינה. לאשר?", "ok": "✓ מאושר", "ok_at": 22.3},
    final={"t": 23.1, "text": "יוצאים לדרך"},
)
EN = dict(
    boot={"title": "VANGUARD SYSTEM ONLINE", "sub": "NEURAL SYNC", "ok": "ALL SYSTEMS NOMINAL", "t": .5, "until": 3.85},
    vitals={"t": 4.1, "hr_label": "HEART", "hr_unit": "BPM", "g1_label": "O2", "g1_value": "98%", "g2_label": "SUIT", "g2_value": "100%",
            "bpm": [[0, 72], [11, 72], [15, 118], [18, 94], [21, 94], [23, 102]]},
    radar={"t": 5.2, "label": "RADAR · {n} CONTACTS", "contacts": 3, "contacts_at": 11},
    compass={"t": 1.4, "label": "HEADING", "heading": 72},
    messages={"t": 7.0, "until": 10.9, "header": "INCOMING · COMMAND", "cps": 16,
              "lines": [{"text": "Vanguard, this is command.", "t": 7.5}, {"text": "Movement detected in sector 07.", "t": 8.8}, {"text": "Proceed with caution.", "t": 10.3}]},
    alert={"t": 11, "until": 15, "title": "⚠ WARNING · 2 HOSTILES", "sub": "ONE DRONE · RANGE 140 M · BEARING 072°"},
    ai={"t": 15.2, "until": 17.9, "label": "SUIT ASSISTANT", "text": "Breathe. I'm with you.", "cps": 13},
    lock={"t": 18.15, "until": 21, "title": "TARGET LOCK", "done": "TARGET LOCKED", "dur": 2.1},
    confirm={"t": 21.1, "until": 23, "question": "Weapon system ready. Confirm?", "ok": "✓ CONFIRMED", "ok_at": 22.3},
    final={"t": 23.1, "text": "LET'S GO"},
)
BLOCKS = ["boot", "vitals", "radar", "compass", "messages", "alert", "ai", "lock", "confirm", "final"]


def ring(r, cls, extra="", sw=2):
    return f'<circle class="{cls}" cx="0" cy="0" r="{r}" fill="none" stroke-width="{sw}" {extra}/>'


def build(spec, base, style="HUD-HELMET"):
    lang = spec.get("language", "he")
    DEF = HE if lang == "he" else EN
    C = {}
    for b in BLOCKS:   # spec value: dict merges over the default, false/None drops the block, missing = default
        v = spec.get(b, DEF[b])
        C[b] = None if not v else {**DEF[b], **v}
    col = {"hud": "#6fe3ff", "text": "#e6fbff", "alert": "#ff4a5a", "ok": "#ffb547", **spec.get("colors", {})}
    rtl = lang == "he"
    faces, extra = fonts("Assistant", "JetBrains Mono")
    sysname = spec.get("system", "VNG-OS")

    css = faces + f"""
:root{{--cy:{col['hud']};--txt:{col['text']};--red:{col['alert']};--amb:{col['ok']};--bk:rgba(2,14,22,.62)}}
#root{{font-family:"Assistant",sans-serif}}
.he{{direction:{'rtl' if rtl else 'ltr'}}}
.g{{color:var(--txt);text-shadow:0 0 10px color-mix(in srgb,var(--cy) 85%,transparent),-1.5px 0 rgba(255,60,120,.4),1.5px 0 rgba(60,200,255,.4)}}
.num{{font-family:"JetBrains Mono",monospace;direction:ltr;unicode-bidi:isolate;display:inline-block}}
svg{{overflow:visible}}
.rs{{stroke:var(--cy)}}.rs.dim{{stroke:color-mix(in srgb,var(--cy) 35%,transparent)}}
.rot{{transform-box:fill-box;transform-origin:center}}
#vig{{position:absolute;inset:0;background:radial-gradient(ellipse 62% 70% at 50% 48%,transparent 55%,color-mix(in srgb,var(--cy) 10%,transparent) 78%,color-mix(in srgb,var(--cy) 22%,transparent) 100%)}}
#vig.red{{background:radial-gradient(ellipse 62% 70% at 50% 48%,transparent 55%,color-mix(in srgb,var(--red) 14%,transparent) 78%,color-mix(in srgb,var(--red) 30%,transparent) 100%)}}
#scan{{position:absolute;inset:0;background:repeating-linear-gradient(0deg,color-mix(in srgb,var(--cy) 5%,transparent) 0 1px,transparent 1px 4px)}}
#boot{{position:absolute;left:0;top:0;width:0;height:0}}
#boot svg{{position:absolute;left:-450px;top:-450px}}
.px{{position:absolute;inset:0}}
#ret{{position:absolute;left:0;top:0;width:0;height:0}}
#ret svg{{position:absolute;left:-220px;top:-220px}}
#ret.red .rs{{stroke:var(--red)}}
#lc{{position:absolute;left:70px;top:210px;width:420px;perspective:1000px}}
#lci{{transform:rotateY(24deg);transform-origin:0 50%}}
#hr{{position:relative;width:300px;height:300px}}
#hr svg{{position:absolute;left:0;top:0}}
#hr .c,.mg .c{{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}}
#hr .k{{font-size:26px;font-weight:600}}#hr .v{{font-size:84px;line-height:1}}#hr .u{{font-size:18px;font-weight:600;opacity:.85}}
.mini{{display:flex;gap:26px;margin-top:10px;margin-inline-start:20px}}
.mg{{position:relative;width:120px;height:120px}}.mg svg{{position:absolute;left:0;top:0}}
.mg .v{{font-size:30px}}.mg .k{{font-size:18px;font-weight:600}}
#rc{{position:absolute;right:70px;top:190px;width:600px;perspective:1000px}}
#rci{{transform:rotateY(-24deg);transform-origin:100% 50%}}
.frame{{position:relative;padding:22px 30px 24px;background:var(--bk);clip-path:polygon(0 0,calc(100% - 28px) 0,100% 28px,100% 100%,28px 100%,0 calc(100% - 28px));border-right:3px solid var(--cy)}}
.frame .h{{display:block;font-size:24px;font-weight:700;color:var(--cy)}}
.frame .l{{display:block;font-size:32px;font-weight:600;line-height:1.4;min-height:1.4em}}
#warn{{position:absolute;right:70px;top:560px;width:600px;perspective:1000px}}
#warn .frame{{border-right-color:var(--red);background:rgba(40,4,10,.72)}}
#warn .t{{display:block;font-size:40px;font-weight:800;color:#ffe3e6;text-shadow:0 0 12px var(--red)}}
#warn .s{{display:block;font-size:26px;font-weight:600;color:#ffd0d5;margin-top:4px}}
#rad{{position:absolute;left:110px;bottom:70px;width:230px;height:230px;border-radius:50%;background:rgba(2,14,22,.5)}}
#rad svg{{position:absolute;left:0;top:0}}
#sweep{{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,color-mix(in srgb,var(--cy) 55%,transparent),transparent 70deg,transparent 360deg)}}
.blip{{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:var(--red);box-shadow:0 0 14px var(--red)}}
.blip.a{{background:var(--amb);box-shadow:0 0 14px var(--amb)}}
#radl{{position:absolute;left:-40px;right:-40px;top:238px;text-align:center;font-size:20px;font-weight:600}}
#cmp{{position:absolute;left:0;right:0;margin:0 auto;top:40px;width:760px;height:60px;overflow:hidden;direction:ltr;background:rgba(2,14,22,.72);
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 22%,#000 78%,transparent)}}
#tape{{position:absolute;left:0;top:10px;white-space:nowrap;font-size:20px}}
#tape span{{display:inline-block;width:80px;text-align:center;border-left:1px solid color-mix(in srgb,var(--cy) 45%,transparent)}}
#cmpn{{position:absolute;left:0;right:0;margin:0 auto;top:104px;width:max-content;font-size:22px;font-weight:600;background:rgba(2,14,22,.72);padding:2px 14px}}
#data{{position:absolute;left:0;right:0;margin:0 auto;bottom:34px;width:900px;text-align:center;font-size:16px;letter-spacing:.14em;opacity:.8;direction:ltr}}
#meters{{position:absolute;right:40px;top:300px;display:flex;gap:8px;align-items:flex-end;height:220px}}
#meters i{{display:block;width:10px;background:linear-gradient(180deg,var(--cy),color-mix(in srgb,var(--cy) 20%,transparent));transform-origin:50% 100%}}
.ctr{{position:absolute;left:0;right:0;margin:0 auto;width:max-content;max-width:1500px;text-align:center}}
#bootm{{top:150px}}#bootm .t{{display:block;font-size:46px;font-weight:800}}#bootm .s{{display:block;font-size:26px;font-weight:600;margin-top:4px}}
#ai{{bottom:120px;padding:14px 34px;background:var(--bk)}}#ai .k{{display:block;font-size:20px;font-weight:700;color:var(--cy)}}#ai .q{{display:block;font-size:44px;font-weight:700;min-height:1.2em}}
#lockm{{top:150px}}#lockm .t{{display:block;font-size:44px;font-weight:800;color:#ffe3e6;text-shadow:0 0 14px var(--red)}}#lockm .p{{display:block;font-size:30px;color:#ffd0d5}}
#wpn{{bottom:120px;padding:14px 34px;background:var(--bk)}}#wpn .q{{display:block;font-size:40px;font-weight:700}}
#wpn .ok{{display:block;font-size:32px;font-weight:800;color:var(--amb);text-shadow:0 0 12px var(--amb);min-height:1.2em}}
#go{{top:440px;font-size:120px;font-weight:800;letter-spacing:.02em;padding:0 40px;background:rgba(2,14,22,.55)}}
#vox{{position:absolute;right:70px;bottom:64px;width:330px;padding:12px 18px;background:var(--bk);border-right:3px solid var(--cy)}}
#vox .k{{display:block;font-size:22px;font-weight:700;color:var(--cy)}}
#vox .w{{display:flex;align-items:center;gap:5px;height:56px;margin-top:6px;direction:ltr}}
#vox .w b{{display:block;width:6px;border-radius:3px;background:var(--cy);box-shadow:0 0 8px var(--cy)}}
"""
    ticks = "".join(f'<line x1="0" y1="-132" x2="0" y2="-{132 + (14 if k % 5 == 0 else 7)}" transform="rotate({k * 6})" />' for k in range(60))
    h = ['<div id="vig"></div><div id="scan"></div>',
         f'<div class="px" id="pxA"><div id="boot"><svg width="900" height="900" viewBox="-450 -450 900 900">{ring(420, "rs", "id=\"bootring\" stroke-dasharray=\"2640\" stroke-dashoffset=\"2640\"", 3)}</svg></div>'
         f'<div id="ret"><svg width="440" height="440" viewBox="-220 -220 440 440"><g class="rot" id="rA">{ring(150, "rs dim", "stroke-dasharray=\"6 10\"", 2)}</g>'
         f'<g class="rot" id="rB">{ring(118, "rs", "stroke-dasharray=\"120 60 30 60\"", 4)}</g><g class="rot" id="rC">{ring(92, "rs dim", "stroke-dasharray=\"2 6\"", 6)}</g>'
         '<g id="tri"><path class="rs" d="M0,-178 L-10,-196 L10,-196 Z" fill="none" stroke-width="2"/><path class="rs" d="M0,178 L-10,196 L10,196 Z" fill="none" stroke-width="2"/>'
         '<path class="rs" d="M-178,0 L-196,-10 L-196,10 Z" fill="none" stroke-width="2"/><path class="rs" d="M178,0 L196,-10 L196,10 Z" fill="none" stroke-width="2"/></g></svg></div></div>']
    v = C["vitals"]
    if v:
        mg = lambda i, lab, val: (f'<div class="mg"><svg width="120" height="120" viewBox="-60 -60 120 120">{ring(50, "rs dim", "", 6)}'  # noqa: E731
                                  f'<circle id="g{i}Arc" cx="0" cy="0" r="50" fill="none" stroke="{col["hud"]}" stroke-width="6" stroke-dasharray="314" stroke-dashoffset="314" transform="rotate(-90)"/></svg>'
                                  f'<div class="c g he"><span class="v num">{e(val)}</span><span class="k">{e(lab)}</span></div></div>')
        h.append(f'<div class="px" id="pxL"><div id="lc"><div id="lci"><div id="hr"><svg width="300" height="300" viewBox="-150 -150 300 300">'
                 f'<g class="rot" id="hrT" stroke="{col["hud"]}" stroke-opacity=".55" stroke-width="2">{ticks}</g>{ring(112, "rs dim", "", 10)}'
                 f'<circle id="hrArc" cx="0" cy="0" r="112" fill="none" stroke="{col["hud"]}" stroke-width="10" stroke-linecap="round" stroke-dasharray="703.7" stroke-dashoffset="703.7" transform="rotate(-90)"/></svg>'
                 f'<div class="c g he"><span class="k">{e(v["hr_label"])}</span><span class="v num" id="bpm">72</span><span class="u">{e(v["hr_unit"])}</span></div></div>'
                 f'<div class="mini">{mg(1, v["g1_label"], v["g1_value"])}{mg(2, v["g2_label"], v["g2_value"])}</div></div></div></div>')
    right = []
    if C["messages"]:
        m = C["messages"]
        right.append(f'<div id="rc"><div id="rci"><div class="frame g he" id="msg"><span class="h">{e(m["header"])}</span>'
                     + "".join(f'<span class="l" id="m{i}"></span>' for i in range(len(m["lines"]))) + "</div></div></div>")
    if C["alert"]:
        a = C["alert"]
        right.append(f'<div id="warn"><div style="transform:rotateY(-24deg);transform-origin:100% 50%"><div class="frame he">'
                     f'<span class="t">{e(a["title"])}</span><span class="s">{e(a.get("sub", ""))}</span></div></div></div>')
    right.append('<div id="meters">' + "<i></i>" * 7 + "</div>")
    h.append('<div class="px" id="pxR">' + "".join(right) + "</div>")
    if C["radar"]:
        r = C["radar"]
        lab = e(r["label"]).replace("{n}", '<span class="num" id="radc">0</span>')
        h.append(f'<div id="rad"><div id="sweep"></div><svg width="230" height="230" viewBox="-115 -115 230 230">{ring(110, "rs dim", "", 1)}{ring(75, "rs dim", "", 1)}{ring(40, "rs dim", "", 1)}'
                 f'<line x1="-110" y1="0" x2="110" y2="0" stroke="{col["hud"]}" stroke-opacity=".3"/><line x1="0" y1="-110" x2="0" y2="110" stroke="{col["hud"]}" stroke-opacity=".3"/></svg>'
                 '<div class="blip" style="left:170px;top:70px"></div><div class="blip" style="left:185px;top:105px"></div><div class="blip a" style="left:150px;top:50px"></div>'
                 f'<div id="radl" class="g he">{lab}</div></div>')
    if C["compass"]:
        h.append(f'<div id="cmp" class="g"><div id="tape" class="num"></div></div><div id="cmpn" class="g he">{e(C["compass"]["label"])} <span class="num" id="hdg">072°</span></div>')
    h.append('<div id="data" class="g num"></div>')
    if C["boot"]:
        b = C["boot"]
        h.append(f'<div id="bootm" class="ctr g he"><span class="t">{e(b["title"])}</span><span class="s">{e(b["sub"])} <span class="num" id="sync">0%</span> · <span id="allok"></span></span></div>')
    if C["ai"]:
        h.append(f'<div id="ai" class="ctr g he"><span class="k">{e(C["ai"]["label"])}</span><span class="q" id="aiq"></span></div>')
    if C["lock"]:
        h.append('<div id="lockm" class="ctr he"><span class="t" id="lockt"></span><span class="p num" id="lockp">0%</span></div>')
    if C["confirm"]:
        h.append(f'<div id="wpn" class="ctr g he"><span class="q">{e(C["confirm"]["question"])}</span><span class="ok" id="wok"></span></div>')
    if C["final"]:
        h.append(f'<div id="go" class="ctr g he">{e(C["final"]["text"])}</div>')
    vo = spec.get("voice")
    env = None
    if vo:
        vf = res(base, vo["file"])
        env = envelope(vf)
        h.append(f'<div id="vox" class="g he"><span class="k">{e(vo.get("label", "AI · VOICE"))}</span><div class="w">' + "<b></b>" * 26 + "</div></div>")

    j = ["const C = " + js({k: v for k, v in C.items()}) + ";",
         f"const EYES = {js(spec.get('eyes', 'eyes'))}, FACE = {js(spec.get('face', 'face'))}, SYS = {js(sysname)};",
         "const ENV = " + js(env) + ";", r"""
const $$ = (id) => document.getElementById(id);
const has = (id) => !!document.getElementById(id);
const txt = (id, s) => { const el = $$(id); if (el && el.textContent !== s) el.textContent = s; };
const type = (id, full, t0, t, cps) => { const n = Math.max(0, Math.min([...full].length, Math.floor((t - t0) * cps))); txt(id, [...full].slice(0, n).join("")); };
const lerp = (a, b, u) => a + (b - a) * Math.max(0, Math.min(1, u));
const inW = (b, t) => b && t >= b.t && t < (b.until ?? 1e9);
if (has("tape")) { let th = ""; for (let d = 0; d < 720; d += 15) th += `<span data-layout-allow-occlusion>${String(d % 360).padStart(3, "0")}</span>`; $$("tape").innerHTML = th; }
const HEX = "0123456789ABCDEF";
const hash = (n) => { let x = Math.sin(n * 12.9898) * 43758.5453; return x - Math.floor(x); };
const METERS = [...document.querySelectorAll("#meters i")];
const VB = [...document.querySelectorAll("#vox .w b")];
function bpmAt(t) {
  const K = C.vitals ? C.vitals.bpm : [[0, 72]];
  if (t <= K[0][0]) return K[0][1];
  for (let i = 1; i < K.length; i++) if (t < K[i][0]) return lerp(K[i - 1][1], K[i][1], (t - K[i - 1][0]) / (K[i][0] - K[i - 1][0]));
  return K[K.length - 1][1];
}
window.onPlace = (t) => {
  const ey = boxAt(EYES, t), f = boxAt(FACE, t);
  const ex = ey ? (ey[0] + ey[2]) / 2 : 960, eyy = ey ? (ey[1] + ey[3]) / 2 : 480;
  const rel = (ey && f) ? ((ex - (f[0] + f[2]) / 2) / (f[2] - f[0])) : 0;
  $$("ret").style.left = ex + "px"; $$("ret").style.top = eyy + "px";
  $$("boot").style.left = ex + "px"; $$("boot").style.top = eyy + "px";
  if (has("pxL")) $$("pxL").style.transform = `translateX(${-rel * 40}px)`;
  $$("pxR").style.transform = `translateX(${-rel * 40}px)`;
  const lock = C.lock && t > C.lock.t - .15 && t < C.lock.t + C.lock.dur + .9, warn = inW(C.alert, t);
  const sp = lock ? 3 : 1;
  $$("rA").style.transform = `rotate(${t * 18 * sp}deg)`; $$("rB").style.transform = `rotate(${-t * 34 * sp}deg)`; $$("rC").style.transform = `rotate(${t * 60 * sp}deg)`;
  const conv = lock ? lerp(1.35, .82, (t - C.lock.t) / 1.8) : 1;
  $$("tri").style.transform = `scale(${conv}) rotate(${lock ? (t - C.lock.t) * 90 : 0}deg)`;
  $$("ret").classList.toggle("red", !!(lock || warn));
  $$("vig").classList.toggle("red", !!warn);
  if (C.vitals) {
    const bpm = bpmAt(t), v0 = C.vitals.t + .1;
    $$("hrT").style.transform = `rotate(${t * 12}deg)`;
    txt("bpm", String(Math.round(bpm)));
    $$("hrArc").style.strokeDashoffset = 703.7 * (1 - Math.min(1, lerp(0, 1, (t - v0) / .8) * bpm / 140));
    $$("g1Arc").style.strokeDashoffset = 314 * (1 - lerp(0, .98, (t - v0 - .4) / .8));
    $$("g2Arc").style.strokeDashoffset = 314 * (1 - lerp(0, 1, (t - v0 - .6) / .8));
  }
  if (C.radar) { $$("sweep").style.transform = `rotate(${t * 140}deg)`; txt("radc", t > C.radar.contacts_at ? String(C.radar.contacts) : "0"); }
  if (C.compass) {
    const hdg = C.compass.heading + rel * 90;
    $$("tape").style.transform = `translateX(${-(hdg / 15) * 80 + 340}px)`;
    txt("hdg", String(Math.round((hdg + 360) % 360)).padStart(3, "0") + "°");
  }
  const k = Math.floor(t * 10); let row = "";
  for (let i = 0; i < 38; i++) row += HEX[Math.floor(hash(k * 41 + i) * 16)] + (i % 4 === 3 ? " " : "");
  const sync = Math.round(lerp(0, 99, (t - .6) / 1.8));
  txt("data", SYS + "  " + row + " SYNC " + String(sync).padStart(2, "0"));
  METERS.forEach((m, i) => { m.style.height = (40 + 170 * (.5 + .5 * Math.sin(t * (2 + i * .7) + i))) + "px"; });
  if (C.boot) { txt("sync", sync + "%"); txt("allok", t > C.boot.t + 2.2 ? C.boot.ok : ""); }
  if (C.messages) C.messages.lines.forEach((l, i) => type("m" + i, l.text, l.t, t, C.messages.cps));
  if (C.ai) type("aiq", C.ai.text, C.ai.t + .2, t, C.ai.cps);
  if (C.lock) { const lk = Math.max(0, Math.min(1, (t - C.lock.t - .15) / C.lock.dur)); txt("lockp", Math.round(lk * 100) + "%"); txt("lockt", lk >= 1 ? C.lock.done : C.lock.title); }
  if (C.confirm) txt("wok", t > C.confirm.ok_at ? C.confirm.ok : "");
  if (ENV && VB.length) { const ev = ENV[Math.max(0, Math.min(ENV.length - 1, Math.round(t * 24)))] || 0;
    VB.forEach((b, i) => { const sh = .35 + .65 * Math.abs(Math.sin(i * 1.7 + t * 7)); b.style.height = (4 + 50 * ev * sh) + "px"; }); }
};
function glitch(sel, at, dur = .3) {
  if (!document.querySelector(sel)) return;
  tl.fromTo(sel, {opacity: 0, skewX: -16, x: -24, clipPath: "inset(46% 0 46% 0)"}, {opacity: 1, skewX: 0, x: 0, clipPath: "inset(0% 0 0% 0)", duration: dur, ease: "expo.out"}, at);
  tl.to(sel, {keyframes: [{opacity: .25, duration: .04}, {opacity: 1, duration: .04}, {opacity: .55, duration: .03}, {opacity: 1, duration: .05}]}, at + dur);
}
const outAt = (sel, at) => { const L = [].concat(sel).filter(s => document.querySelector(s)); if (L.length && at != null) tl.to(L, {opacity: 0, duration: .25, ease: "power2.in"}, at); };
tl.set(["#ret", "#lc", "#rc", "#warn", "#rad", "#cmp", "#cmpn", "#data", "#meters", "#bootm", "#ai", "#lockm", "#wpn", "#go", ".blip", "#vox"].filter(s => document.querySelector(s)), {opacity: 0}, 0);
tl.fromTo("#scan", {opacity: 0}, {opacity: 1, duration: .6}, .05);
tl.fromTo("#vig", {opacity: 0}, {opacity: 1, duration: .8}, .05);
tl.fromTo("#bootring", {strokeDashoffset: 2640}, {strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut"}, .15);
tl.to("#boot", {opacity: 0, duration: .4}, 1.35);
tl.fromTo("#ret", {opacity: 0, scale: 1.6}, {opacity: 1, scale: 1, duration: .6, ease: "expo.out"}, 1.1);
glitch("#data", 1.8); glitch("#meters", 2.0);
if (C.boot) { glitch("#bootm", C.boot.t, .35); outAt("#bootm", C.boot.until); }
if (C.compass) { glitch("#cmp", C.compass.t); glitch("#cmpn", C.compass.t + .1); }
if (C.vitals) glitch("#lc", C.vitals.t, .4);
if (C.radar) glitch("#rad", C.radar.t, .35);
if (C.messages) { glitch("#rc", C.messages.t, .35); outAt("#rc", C.messages.until); }
if (C.radar && C.alert) { tl.to(".blip", {opacity: 1, duration: .05, stagger: .12}, C.radar.contacts_at); tl.to(".blip", {scale: 1.6, duration: .25, repeat: 7, yoyo: true, ease: "sine.inOut"}, C.radar.contacts_at + .1); }
if (C.alert) { glitch("#warn", C.alert.t, .25); tl.to("#warn", {opacity: .45, duration: .15, repeat: 9, yoyo: true, ease: "none"}, C.alert.t + .4); outAt("#warn", C.alert.until); }
if (C.ai) { glitch("#ai", C.ai.t, .35); outAt("#ai", C.ai.until); }
if (C.lock) { glitch("#lockm", C.lock.t, .25); outAt("#lockm", C.lock.until); }
if (C.confirm) { glitch("#wpn", C.confirm.t, .35); outAt("#wpn", C.confirm.until); }
if (C.final) { outAt(["#lc", "#rad", "#meters", "#data", "#vox"], C.final.t - .1); glitch("#go", C.final.t, .4); }
glitch("#vox", .15, .3);
"""]
    sfx = []
    if spec.get("sfx", True):
        def at(b, k="t", d=0):
            return C[b][k] + d if C[b] else None
        raw = [("hud_boot", .1, .7), ("data_chatter", .6, .25), ("chime", at("boot", d=2.2), .4), ("ui_whoosh", at("vitals", d=-.05), .4),
               ("scan_beeps", at("radar"), .25), ("ui_pop", at("messages"), .5)]
        if C["messages"]:
            raw += [("ui_tick", ln["t"], .3) for ln in C["messages"]["lines"]]
        raw += [("warn_beep", at("alert"), .75), ("warn_beep", at("alert", d=1.2), .5), ("heartbeat", at("alert"), .5),
                ("glass_ting", at("ai", d=.1), .5), ("lock_tone", at("lock"), .55), ("hit_confirm", at("lock", d=2.25), .65),
                ("charge_up", at("confirm"), .65), ("hit_confirm", at("confirm", "ok_at"), .55), ("stinger", at("final", d=-.05), .7)]
        sfx = [cue(n, a, v) for n, a, v in raw if a is not None]
    if vo:
        sfx = [(str(res(base, vo["file"])), "voice", 30, float(vo.get("at", 0)), vo.get("vol", 1.0))] + scale_cues(sfx, .6)
    sfx += audio_cues(spec, base, .4)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="\n".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .45 if vo else .7), extra=extra)
