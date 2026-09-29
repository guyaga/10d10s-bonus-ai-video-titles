# REFERENCE SOURCE - not runnable as-is. The hand-built compositions behind STOMP-ESCORT, STOMP-BEHIND, GLASS-CALLOUT,
# COUNTDOWN-CTA (D1S/D1G/D1B/D2/D3), HUD-HELMET (B4X/B4V), SCIFI-TARGETING (B3), MAP-FLYOVER (A1/A2), CAMPUS-AR (C1-C3)
# and SPEED-STAT (E1). Copy the css/hud/js blocks of the function you need into a spec (html_front/css/js) or a
# shotkit.build() call; its paths (ROOT/shared/..., E_ads/...) belong to the original project.
"""All test-shot overlay designs. python shots.py A2 B1 ...  (builds + checks each project)

Timing facts come from frame-by-frame analysis of each Seedance clip:
  B3: launch flash 3.85s, impacts 4.65s, fireball peak ~5.0s (luminance analysis)
  C2: headphones on at ~3.5s; only two microphone heads are clearly visible (Gemini)
"""
import subprocess
import sys
from pathlib import Path

import shotkit

R = Path(__file__).resolve().parent.parent
LOGO = Path("D:/Ono video/right at home storyboard/campus/OnoAcademic.svg.png")

TICKS = '<div class="tick tk1"></div><div class="tick tk2"></div><div class="tick tk3"></div><div class="tick tk4"></div>'
BRK = '<div class="brk"><i></i><i></i><i></i><i></i></div>'

# shared SFX prompts (cached by name)
S = {
    "ui_whoosh": ("Clean cinematic UI whoosh swelling in, airy, modern tech interface, no music", 1.2),
    "ui_tick": ("Fast soft digital typing ticks for text appearing on screen, subtle futuristic UI", 1.0),
    "ui_pop": ("Single short soft digital pop, glassy click with small bubbly tail, UI sound", 0.6),
    "chime": ("Warm soft arrival chime, two gentle bell tones, positive, clean UI notification", 1.2),
    "logo_hit": ("Soft cinematic logo reveal: low thump followed by a bright airy shimmer, elegant", 1.8),
    "hud_boot": ("Sci-fi helmet HUD booting up, rising electronic sweep with small digital chirps, clean", 1.6),
    "data_chatter": ("Quiet fast computer data chatter, tiny electronic blips and clicks, sci-fi interface", 2.0),
    "lock_tick": ("Short sharp electronic target-acquired tick, sci-fi, clean", 0.5),
    "bass_pulse": ("Deep low cinematic bass pulse, single hit, tense sci-fi", 1.5),
    "heartbeat": ("Muffled heartbeat inside a helmet speeding up from calm to fast, tense", 5.0),
    "warn_beep": ("Urgent sci-fi warning double beep, two short high electronic alarm tones", 0.8),
    "charge_up": ("Weapon system charging up, rising electric whine ending with a confident click, sci-fi", 1.6),
    "scan_beeps": ("Targeting computer scanning, quick repeating electronic beeps accelerating, sci-fi", 2.0),
    "lock_tone": ("Missile lock-on tone, steady high electronic beep, sci-fi, clean", 1.0),
    "launch": ("Heavy mechanical launcher firing two rockets, metallic ka-chunk and whoosh", 1.2),
    "hit_confirm": ("Two quick electronic hit-confirm blips, satisfying, sci-fi HUD", 0.8),
    "stinger": ("Short triumphant sci-fi UI stinger, bright synth hit with shimmer tail", 1.6),
    "glass_ting": ("Delicate soft glass ting, AR smart-glasses notification, airy and clean", 0.7),
    "ar_whoosh": ("Very soft airy UI whoosh for an AR label sliding in, subtle", 0.8),
    "rec_beep": ("Single short studio record-start beep, clean", 0.5),
    "mic_click": ("Soft microphone check tick, subtle", 0.5),
}


def cue(name, at, vol=0.8):
    p, secs = S[name]
    return (name, p, secs, at, vol)


# ---------------------------------------------------------------- A2 arrival
def A2():
    css = r"""
.tag{padding:10px 16px;white-space:nowrap}
#arr{transform:translate(-50%,-100%)}
#arr .en{font-size:30px;font-weight:800;letter-spacing:.06em;color:var(--acc)}
#arr .he{font-size:28px;font-weight:700;margin-left:12px}
#head-brk{--c:var(--acc)}
#loc{position:absolute;left:112px;bottom:112px;width:620px;padding:24px 28px;border-top:3px solid var(--acc)}
#loc .kick{font-size:18px;letter-spacing:.2em;color:var(--acc)}
#loc .en{display:block;font-size:52px;font-weight:800;line-height:1.05;margin-top:10px}
#loc .he{display:block;font-size:40px;font-weight:600;color:var(--fg);margin-top:4px;text-align:left}
#loc .sub{display:block;font-size:22px;color:var(--mute);margin-top:10px}
#route{position:absolute;left:112px;bottom:56px;padding:10px 16px;font-size:20px;letter-spacing:.08em}
#logo{transform:translate(-50%,-50%)}
#logo img{width:330px;display:block;filter:drop-shadow(0 2px 6px rgba(0,0,0,.25))}
"""
    hud = f"""
{TICKS}
<div id="head-brk" data-box="head" data-pad="22">{BRK}</div>
<div id="arr" class="panel tag" data-follow="head" data-anchor="t" data-dy="-40"><span class="en">ARRIVED ✓</span><span class="he">הגעת</span></div>
<div id="loc" class="panel"><span class="kick mono">DESTINATION</span>
  <span class="en">Ono Academic College</span><span class="he">הקריה האקדמית אונו</span>
  <span class="sub mono">Kiryat Ono campus · 32.036°N 34.865°E</span></div>
<div id="route" class="panel mono">TLV → ONO · 12.8 km by road · ≈17 min</div>
<div id="logo" data-follow="facade_blank" data-anchor="c"><img src="assets/ono_logo.png" alt="Ono Academic College"></div>
"""
    js = r"""
tl.fromTo(".tick", {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:.5, stagger:.05, ease:"power3.out"}, .05);
tl.fromTo("#head-brk .brk", {opacity:0, scale:1.6}, {opacity:1, scale:1, duration:.45, ease:"power3.out"}, .3);
tl.fromTo("#arr", {opacity:0, y:14}, {opacity:1, y:0, duration:.45, ease:"back.out(2)"}, .45);
tl.fromTo("#loc", {opacity:0, y:30, clipPath:"inset(100% 0 0 0)"}, {opacity:1, y:0, clipPath:"inset(0% 0 0 0)", duration:.6, ease:"expo.out"}, 1.0);
tl.fromTo("#loc .he", {opacity:0, x:-16}, {opacity:1, x:0, duration:.45, ease:"power2.out"}, 1.35);
tl.fromTo("#route", {opacity:0, x:-24}, {opacity:1, x:0, duration:.45, ease:"power2.out"}, 2.5);
tl.to(["#arr", "#head-brk .brk"], {opacity:0, duration:.35}, 3.6);
tl.fromTo("#logo img", {opacity:0, scale:.82, filter:"brightness(3) drop-shadow(0 2px 6px rgba(0,0,0,.25))"}, {opacity:1, scale:1, filter:"brightness(1) drop-shadow(0 2px 6px rgba(0,0,0,.25))", duration:.9, ease:"expo.out"}, 4.2);
"""
    sfx = [cue("chime", .35, .7), cue("ui_whoosh", .95, .6), cue("ui_tick", 1.3, .4), cue("ui_pop", 2.5, .6), cue("logo_hit", 4.15, .8)]
    return dict(extra={"ono_logo.png": LOGO}, project=R / "videos/a2-arrival", clip=R / "A_map_ono/clips/A2_seedance_720p.mp4",
                track=R / "tools/A2_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.6)


# ---------------------------------------------------------------- B palette
B_CSS = r"""
:root{--acc:#ffb547;--fg:#fff4e2;--mute:#d9c3a0;--warn:#ff5046;--panel:rgba(12,8,4,.78);--line:rgba(255,181,71,.6)}
.brk i{border-color:var(--acc)}
.tick{border-color:rgba(255,181,71,.7)}
.scan{position:absolute;left:0;right:0;top:0;height:3px;background:linear-gradient(90deg,transparent,var(--acc),transparent);box-shadow:0 0 24px var(--acc)}
"""


# ---------------------------------------------------------------- B1 wide walk
def B1():
    css = B_CSS + r"""
#loc{position:absolute;left:112px;top:104px;width:600px;padding:22px 26px;border-left:0;border-top:3px solid var(--acc)}
#loc .kick{font-size:18px;letter-spacing:.22em;color:var(--acc)}
#loc .big{display:block;font-size:54px;font-weight:800;line-height:1.05;margin-top:8px;letter-spacing:.02em}
#loc .he{display:block;font-size:34px;font-weight:600;text-align:left;margin-top:4px}
#loc .row{display:block;font-size:21px;color:var(--mute);margin-top:10px}
#pbox{}
#ptag{padding:14px 18px;white-space:nowrap}
#ptag .n{display:block;font-size:30px;font-weight:800}
#ptag .s{display:block;font-size:18px;color:var(--mute);letter-spacing:.08em;margin-top:4px}
#ptag .ok{color:#ffd28a}
#stat{position:absolute;right:112px;bottom:112px;width:420px;padding:20px 24px}
.bar{margin-top:12px}.bar .l{display:flex;justify-content:space-between;font-size:18px;letter-spacing:.12em;color:var(--mute)}
.bar .t{height:6px;background:rgba(255,244,226,.15);margin-top:6px;border-radius:3px;overflow:hidden}
.bar .f{height:100%;background:var(--acc);transform-origin:0 50%}
"""
    hud = f"""
{TICKS}<div class="scan" id="scan"></div>
<div id="pbox" data-box="pilot" data-pad="18">{BRK}</div>
<div id="ptag" class="panel" data-follow="pilot" data-anchor="tr" data-dx="34" data-dy="30">
  <span class="n">PILOT · G. AGA</span><span class="s mono">CALLSIGN: VANGUARD</span><span class="s mono">SUIT MK-VII · <b class="ok">ONLINE</b></span></div>
<div id="loc" class="panel"><span class="kick mono">LOCATION</span><span class="big">NEO-TLV · SECTOR 07</span>
  <span class="he">ניאו־תל אביב · גזרה 07</span>
  <span class="row mono">DISTRICT: NOMAD · 2089-10-04 · 23:41</span><span class="row mono">RAIN 12 mm/h · VIS 340 m</span></div>
<div id="stat" class="panel">
  <div class="bar"><div class="l mono"><span>POWER</span><span>98%</span></div><div class="t"><div class="f" id="f1"></div></div></div>
  <div class="bar"><div class="l mono"><span>ARMOR</span><span>100%</span></div><div class="t"><div class="f" id="f2"></div></div></div>
  <div class="bar"><div class="l mono"><span>NEURAL SYNC</span><span>99%</span></div><div class="t"><div class="f" id="f3"></div></div></div></div>
"""
    js = r"""
tl.fromTo("#scan", {y:0, opacity:1}, {y:1080, opacity:.2, duration:.9, ease:"power2.inOut"}, .1);
tl.fromTo(".tick", {opacity:0, scale:1.5}, {opacity:1, scale:1, duration:.4, stagger:.05, ease:"power3.out"}, .15);
tl.fromTo("#loc", {opacity:0, clipPath:"inset(0 100% 0 0)"}, {opacity:1, clipPath:"inset(0 0% 0 0)", duration:.7, ease:"expo.out"}, .7);
tl.fromTo("#loc .he", {opacity:0}, {opacity:1, duration:.4}, 1.1);
tl.fromTo("#pbox .brk", {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:.4, ease:"power3.out"}, 1.5);
tl.fromTo("#ptag", {opacity:0, x:-20}, {opacity:1, x:0, duration:.45, ease:"power3.out"}, 1.7);
tl.fromTo("#stat", {opacity:0, y:24}, {opacity:1, y:0, duration:.5, ease:"power3.out"}, 2.9);
tl.fromTo("#f1", {scaleX:0}, {scaleX:.98, duration:.8, ease:"power2.out"}, 3.1);
tl.fromTo("#f2", {scaleX:0}, {scaleX:1, duration:.8, ease:"power2.out"}, 3.2);
tl.fromTo("#f3", {scaleX:0}, {scaleX:.99, duration:.8, ease:"power2.out"}, 3.3);
"""
    sfx = [cue("hud_boot", .05, .7), cue("ui_tick", .7, .45), cue("lock_tick", 1.5, .8), cue("data_chatter", 1.7, .35),
           cue("bass_pulse", 2.9, .6), cue("ui_pop", 3.1, .4)]
    return dict(project=R / "videos/b1-wide", clip=R / "B_scifi/clips/B1_seedance_720p.mp4",
                track=R / "tools/B1_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.7)


# ---------------------------------------------------------------- B2 helmet HUD
def B2():
    css = B_CSS + r"""
#visor{overflow:visible}
#vin{position:absolute;inset:0;perspective:900px}
.side{position:absolute;top:22%;width:23%;padding:14px 16px}
#left{left:3%;transform:rotateY(14deg);transform-origin:0 50%}
#right{right:3%;transform:rotateY(-14deg);transform-origin:100% 50%;text-align:right}
.lab{display:block;font-size:17px;line-height:1.3;letter-spacing:.16em;color:var(--mute);margin-bottom:6px}
.val{display:block;font-size:46px;font-weight:700;line-height:1.15;margin-bottom:4px}
.unit{font-size:20px;color:var(--mute);margin-left:4px}
#compass{position:absolute;left:25%;right:25%;top:5%;height:40px;overflow:hidden;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 20%,#000 80%,transparent)}
#tape{position:absolute;left:0;top:0;white-space:nowrap;font-size:18px;letter-spacing:.1em;color:var(--fg)}
#tape span{display:inline-block;width:90px;text-align:center;border-left:1px solid rgba(255,244,226,.35)}
#needle{position:absolute;left:50%;top:calc(5% + 44px);width:0;height:0;margin-left:-9px;border-left:9px solid transparent;border-right:9px solid transparent;border-bottom:14px solid var(--acc)}
#warn{position:absolute;right:4%;top:60%;padding:14px 18px;border:2px solid var(--warn);background:rgba(40,6,4,.8);white-space:nowrap}
#warn .t{display:block;font-size:30px;font-weight:800;color:#ffd9d6}
#warn .s{display:block;font-size:18px;color:#ffb3ad;letter-spacing:.08em;margin-top:4px}
#wf{position:absolute;left:0;right:0;margin:0 auto;width:max-content;bottom:8%;padding:10px 22px;font-size:30px;font-weight:800;
  letter-spacing:.18em;color:var(--acc);border:2px solid var(--acc);background:rgba(12,8,4,.78);white-space:nowrap}
#eyebrk .brk i{width:18px;height:18px;border-width:2px}
"""
    hud = f"""
<div id="visor" data-box="visor" data-pad="-30"><div id="vin">
  <div id="compass"><div id="tape" class="mono"></div></div><div id="needle"></div>
  <div id="left" class="side panel"><span class="lab mono">HEART</span><span class="val mono"><span id="bpm">88</span><span class="unit">BPM</span></span>
     <span class="lab mono" style="margin-top:12px">O₂</span><span class="val mono">97<span class="unit">%</span></span></div>
  <div id="right" class="side panel"><span class="lab mono">SUIT INTEGRITY</span><span class="val mono">100<span class="unit">%</span></span>
     <span class="lab mono" style="margin-top:12px">HEADING</span><span class="val mono"><span id="hdg">072</span><span class="unit">°</span></span></div>
  <div id="warn"><span class="t">⚠ 2 HOSTILES · 1 DRONE</span><span class="s mono">140 m · BEARING 072°</span></div>
  <div id="wf">WEAPONS FREE</div>
</div></div>
<div id="eyebrk" data-box="eyes" data-pad="10">{BRK}</div>
"""
    js = r"""
const tape = document.getElementById("tape");
let h = ""; for (let d = 0; d < 720; d += 15) h += `<span>${String(d % 360).padStart(3, "0")}</span>`; tape.innerHTML = h;
window.onPlace = (t) => {
  const e = boxAt("eyes", t), f = boxAt("face", t);
  const rel = (e && f) ? (((e[0] + e[2]) / 2 - (f[0] + f[2]) / 2) / (f[2] - f[0])) : 0;
  const hdg = 72 + rel * 90;
  tape.style.transform = `translateX(${-(hdg / 15) * 90 + 200}px)`;
  document.getElementById("hdg").textContent = String(Math.round((hdg + 360) % 360)).padStart(3, "0");
  const bpm = t < 2 ? 88 : t < 3.6 ? 88 + (t - 2) / 1.6 * 24 : 112;
  document.getElementById("bpm").textContent = Math.round(bpm);
};
tl.fromTo("#vin", {opacity:0}, {opacity:1, duration:.25}, .1);
tl.fromTo("#compass", {opacity:0, y:-12}, {opacity:1, y:0, duration:.5, ease:"power3.out"}, .2);
tl.fromTo("#needle", {scaleY:0}, {scaleY:1, duration:.4}, .3);
tl.fromTo("#left", {opacity:0, x:-40}, {opacity:1, x:0, duration:.55, ease:"expo.out"}, .35);
tl.fromTo("#right", {opacity:0, x:40}, {opacity:1, x:0, duration:.55, ease:"expo.out"}, .45);
tl.fromTo("#eyebrk .brk", {opacity:0, scale:1.3}, {opacity:.9, scale:1, duration:.4}, .6);
tl.fromTo("#warn", {opacity:0, scale:1.15}, {opacity:1, scale:1, duration:.3, ease:"power4.out"}, 2.05);
tl.to("#warn", {opacity:.35, duration:.18, repeat:5, yoyo:true, ease:"none"}, 2.4);
tl.fromTo("#wf", {opacity:0, scale:1.35}, {opacity:1, scale:1, duration:.6, ease:"expo.out"}, 4.1);
"""
    sfx = [cue("hud_boot", .05, .6), cue("heartbeat", .6, .5), cue("warn_beep", 2.05, .8), cue("warn_beep", 2.8, .5),
           cue("charge_up", 3.95, .75)]
    return dict(project=R / "videos/b2-helmet", clip=R / "B_scifi/clips/B2_seedance_720p.mp4",
                track=R / "tools/B2_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.7)


# ---------------------------------------------------------------- B3 POV targeting
def B3():
    css = B_CSS + r"""
#ret{position:absolute;left:960px;top:540px;width:0;height:0}
#ret .c{position:absolute;left:-60px;top:-60px;width:120px;height:120px;border:2px solid rgba(255,181,71,.8);border-radius:50%}
#ret .h{position:absolute;left:-90px;top:-1px;width:180px;height:2px;background:linear-gradient(90deg,var(--acc) 0 30%,transparent 30% 70%,var(--acc) 70%)}
#ret .v{position:absolute;top:-90px;left:-1px;height:180px;width:2px;background:linear-gradient(180deg,var(--acc) 0 30%,transparent 30% 70%,var(--acc) 70%)}
.tgt .brk i{border-color:var(--acc)}
.tgt.lock .brk i{border-color:var(--warn)}
.tt{padding:10px 14px;white-space:nowrap}
.tt .n{display:block;font-size:26px;font-weight:800}
.tt .s{display:block;font-size:17px;letter-spacing:.08em;color:var(--mute);margin-top:2px}
.tt.lock{border:2px solid var(--warn)}
#arcs{position:absolute;inset:0;width:1920px;height:1080px}
.hit{position:absolute;left:0;top:0;width:0;height:0}
.hit i{position:absolute;left:-2px;top:-40px;width:4px;height:80px;background:#fff;box-shadow:0 0 18px var(--acc)}
.hit i:nth-child(1){transform:rotate(45deg)}.hit i:nth-child(2){transform:rotate(-45deg)}
#lockmsg{position:absolute;left:50%;top:auto;bottom:190px;transform:translateX(-50%);padding:10px 22px;font-size:30px;font-weight:800;letter-spacing:.14em;color:#ffd9d6;border:2px solid var(--warn);background:rgba(40,6,4,.82);white-space:nowrap}
#fire{position:absolute;left:50%;top:auto;bottom:180px;transform:translateX(-50%);padding:10px 30px;font-size:44px;font-weight:800;letter-spacing:.3em;color:#1a0d02;background:var(--acc);white-space:nowrap}
#banner{position:absolute;left:0;right:0;top:420px;text-align:center}
#banner .en{display:inline-block;font-size:88px;font-weight:800;letter-spacing:.08em;padding:10px 40px;background:rgba(12,8,4,.8);border-top:3px solid var(--acc);border-bottom:3px solid var(--acc)}
#banner .he{display:block;font-size:44px;font-weight:700;margin-top:14px;text-align:center;text-shadow:0 2px 16px #000}
#banner .s{display:block;font-size:20px;letter-spacing:.14em;color:var(--mute);margin-top:10px}
"""
    hud = f"""
{TICKS}
<div id="ret"><div class="c"></div><div class="h"></div><div class="v"></div></div>
<svg id="arcs" viewBox="0 0 1920 1080"><path id="arc1" fill="none" stroke="#ffb547" stroke-width="4" stroke-dasharray="14 10"/><path id="arc2" fill="none" stroke="#ffb547" stroke-width="4" stroke-dasharray="14 10"/></svg>
<div id="t1" class="tgt" data-box="heavy" data-pad="10">{BRK}</div>
<div id="t2" class="tgt" data-box="striker" data-pad="10">{BRK}</div>
<div id="t3" class="tgt" data-box="drone" data-pad="12">{BRK}</div>
<div id="l1" class="tt panel" data-follow="heavy" data-anchor="r" data-dx="18" data-dy="-20"><span class="n">T-01 // HEAVY</span><span class="s mono">RANGE <b id="r1">140</b> m · ARMOR IV</span></div>
<div id="l2" class="tt panel" data-follow="striker" data-anchor="tr" data-dx="18" data-dy="-10"><span class="n">T-02 // STRIKER</span><span class="s mono">RANGE <b id="r2">152</b> m · FAST</span></div>
<div id="l3" class="tt panel" data-follow="drone" data-anchor="r" data-dx="26" data-dy="-26"><span class="n">D-01 // RECON</span><span class="s mono" id="d1s">ALT 38 m · TRACKING</span></div>
<div class="hit" id="h1" data-follow="heavy" data-anchor="c"><i></i><i></i></div>
<div class="hit" id="h2" data-follow="striker" data-anchor="c"><i></i><i></i></div>
<div id="lockmsg" class="mono">HOSTILE LOCK · 2 TARGETS</div>
<div id="fire" class="mono">FIRE</div>
<div id="banner"><span class="en">TARGETS NEUTRALIZED</span><span class="he">המטרות נוטרלו</span><span class="s mono">T-01 DOWN · T-02 DOWN · D-01 SIGNAL LOST</span></div>
"""
    js = r"""
const FIRE = 3.85, IMPACT = 4.65;
function arc(el, a, b, u) {
  if (!a || !b || u <= 0) { el.setAttribute("d", ""); return; }
  const x0 = (a[0] + a[2]) / 2, y0 = a[1] + 20, x1 = (b[0] + b[2]) / 2, y1 = (b[1] + b[3]) / 2;
  const cx = (x0 + x1) / 2, cy = Math.min(y0, y1) - 260;
  const P = (s) => [(1-s)*(1-s)*x0 + 2*(1-s)*s*cx + s*s*x1, (1-s)*(1-s)*y0 + 2*(1-s)*s*cy + s*s*y1];
  let d = `M${x0},${y0}`; for (let k = 1; k <= 24; k++) { const p = P(u * k / 24); d += ` L${p[0]},${p[1]}`; }
  el.setAttribute("d", d);
}
window.onPlace = (t) => {
  const r = (v0, v1) => Math.round(v0 + (v1 - v0) * Math.min(1, t / 3.8));
  document.getElementById("r1").textContent = r(140, 96);
  document.getElementById("r2").textContent = r(152, 118);
  const u = t < FIRE ? 0 : t < IMPACT ? (t - FIRE) / (IMPACT - FIRE) : (t < IMPACT + .5 ? 1 : 0);
  arc(document.getElementById("arc1"), boxAt("launcher", t), boxAt("heavy", Math.min(t, IMPACT)), u);
  arc(document.getElementById("arc2"), boxAt("launcher", t), boxAt("striker", Math.min(t, IMPACT)), u);
  document.getElementById("t1").classList.toggle("lock", t > 2.6 && t < IMPACT);
  document.getElementById("t2").classList.toggle("lock", t > 2.6 && t < IMPACT);
  document.getElementById("l1").classList.toggle("lock", t > 2.6 && t < IMPACT);
  document.getElementById("l2").classList.toggle("lock", t > 2.6 && t < IMPACT);
  document.getElementById("d1s").textContent = t < IMPACT + .4 ? "ALT 38 m · TRACKING" : "SIGNAL LOST";
};
tl.fromTo(".tick", {opacity:0, scale:1.5}, {opacity:1, scale:1, duration:.4, stagger:.05}, .05);
tl.fromTo("#ret", {opacity:0, scale:2, rotation:-45}, {opacity:1, scale:1, rotation:0, duration:.5, ease:"expo.out"}, .2);
tl.fromTo("#t1 .brk", {opacity:0, scale:1.5}, {opacity:1, scale:1, duration:.35, ease:"power3.out"}, .5);
tl.fromTo("#l1", {opacity:0, y:10}, {opacity:1, y:0, duration:.35}, .65);
tl.fromTo("#t2 .brk", {opacity:0, scale:1.5}, {opacity:1, scale:1, duration:.35, ease:"power3.out"}, .9);
tl.fromTo("#l2", {opacity:0, y:10}, {opacity:1, y:0, duration:.35}, 1.05);
tl.fromTo("#t3 .brk", {opacity:0, scale:1.5}, {opacity:1, scale:1, duration:.35, ease:"power3.out"}, 1.3);
tl.fromTo("#l3", {opacity:0, y:10}, {opacity:1, y:0, duration:.35}, 1.45);
tl.fromTo("#lockmsg", {opacity:0, scale:1.2}, {opacity:1, scale:1, duration:.25, ease:"power4.out"}, 2.6);
tl.to("#lockmsg", {opacity:0, duration:.15}, 3.75);
tl.fromTo("#fire", {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:.15, ease:"power4.out"}, FIRE - .05);
tl.to("#fire", {opacity:0, duration:.3}, IMPACT);
tl.fromTo(".hit i", {opacity:0, scaleY:.2}, {opacity:1, scaleY:1.3, duration:.18, ease:"power4.out"}, IMPACT);
tl.to(".hit i", {opacity:0, duration:.4}, IMPACT + .35);
tl.to(["#t1", "#t2", "#l1", "#l2", "#ret"], {opacity:0, duration:.3}, IMPACT + .2);
tl.to(["#t3", "#l3"], {opacity:0, duration:.3}, 6.1);
tl.fromTo("#banner .en", {opacity:0, scaleX:1.3}, {opacity:1, scaleX:1, duration:.5, ease:"expo.out"}, 6.2);
tl.fromTo("#banner .he", {opacity:0, y:14}, {opacity:1, y:0, duration:.4}, 6.45);
tl.fromTo("#banner .s", {opacity:0}, {opacity:1, duration:.4}, 6.6);
"""
    sfx = [cue("hud_boot", .05, .5), cue("scan_beeps", .5, .5), cue("lock_tone", 2.6, .7), cue("launch", 3.8, .5),
           cue("hit_confirm", 4.7, .8), cue("stinger", 6.15, .8)]
    return dict(project=R / "videos/b3-pov", clip=R / "B_scifi/clips/B3_seedance_720p.mp4",
                track=R / "tools/B3_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.85)


# ---------------------------------------------------------------- C palette (Ono green AR)
C_CSS = r"""
.chip{position:absolute;right:112px;top:60px;display:flex;align-items:center;gap:12px;font-size:20px;letter-spacing:.14em;padding:10px 16px}
.chip i{width:12px;height:12px;border-radius:50%;background:var(--acc);display:block}
.ar{padding:14px 20px;white-space:nowrap;border-left:4px solid var(--acc)}
.ar .en{display:block;font-size:40px;font-weight:800;line-height:1.05}
.ar .he{display:block;font-size:32px;font-weight:600;color:var(--fg);margin-top:2px;text-align:left}
.ar .s{display:block;font-size:18px;letter-spacing:.1em;color:var(--mute);margin-top:6px}
.pinline{position:absolute;width:2px;background:var(--line)}
.dot{position:absolute;left:-9px;top:-9px;width:18px;height:18px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 5px rgba(7,13,9,.6),0 0 20px var(--acc)}
"""


def C1():
    css = C_CSS + r"""
#tagS{transform:translate(-100%,-50%)}
#tagD{transform:translate(0,-100%)}
#tagG{transform:translate(0,-50%)}
#tagG .en{font-size:30px}
"""
    hud = f"""
{TICKS}<div class="chip panel mono"><i></i>ONO AR · CAMPUS TOUR</div>
<div data-follow="shelves" data-anchor="c" data-dx="-40"><div class="dot"></div></div>
<div id="tagS" class="ar panel" data-follow="shelves" data-anchor="c" data-dx="-70"><span class="en">Library</span><span class="he">הספרייה</span></div>
<div data-follow="desks" data-anchor="c"><div class="dot"></div></div>
<div id="tagD" class="ar panel" data-follow="desks" data-anchor="c" data-dx="-40" data-dy="-30"><span class="en">Study area</span><span class="he">אזור למידה</span></div>
<div id="tagG" class="ar panel" data-follow="head" data-anchor="r" data-dx="40"><span class="en">Guy Aga</span><span class="he">אורח בקמפוס</span><span class="s mono">GUEST · VISITOR PASS</span></div>
"""
    js = r"""
tl.fromTo(".tick", {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:.45, stagger:.05}, .05);
tl.fromTo(".chip", {opacity:0, x:20}, {opacity:1, x:0, duration:.4}, .2);
tl.to(".chip i", {opacity:.25, duration:.5, repeat:10, yoyo:true, ease:"sine.inOut"}, .6);
const dots = document.querySelectorAll(".dot");
tl.fromTo(dots[0], {scale:0}, {scale:1, duration:.35, ease:"back.out(3)"}, .9);
tl.fromTo("#tagS", {opacity:0, clipPath:"inset(0 0 0 100%)"}, {opacity:1, clipPath:"inset(0 0 0 0%)", duration:.5, ease:"expo.out"}, 1.0);
tl.fromTo(dots[1], {scale:0}, {scale:1, duration:.35, ease:"back.out(3)"}, 2.4);
tl.fromTo("#tagD", {opacity:0, y:16}, {opacity:1, y:0, duration:.5, ease:"expo.out"}, 2.5);
tl.fromTo("#tagG", {opacity:0, x:-16}, {opacity:1, x:0, duration:.45, ease:"power3.out"}, 3.9);
"""
    sfx = [cue("ar_whoosh", .1, .5), cue("glass_ting", .95, .7), cue("glass_ting", 2.45, .6), cue("glass_ting", 3.9, .55)]
    return dict(project=R / "videos/c1-library", clip=R / "C_campus_hud/clips/C1_seedance_720p.mp4",
                track=R / "tools/C1_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.7)


def C2():
    css = C_CSS + r"""
#tagW{transform:translate(-50%,-100%)}
.mic{transform:translate(-50%,0)}
.mic .m{position:absolute;left:0;top:0;transform:translate(-50%,-50%);width:54px;height:54px;border:2px solid var(--acc);border-radius:50%}
.mic .l{position:absolute;left:36px;top:-14px;font-size:18px;letter-spacing:.12em;white-space:nowrap;padding:4px 8px}
#rec{position:absolute;left:112px;top:60px;display:flex;align-items:center;gap:12px;padding:10px 16px;font-size:22px;letter-spacing:.14em}
#rec i{width:16px;height:16px;border-radius:50%;background:#ff4b3e;display:block}
#wave{position:absolute;left:50%;bottom:90px;transform:translateX(-50%);display:flex;align-items:center;gap:6px;height:80px;padding:0 22px}
#wave b{display:block;width:7px;border-radius:4px;background:var(--acc)}
"""
    bars = "".join("<b></b>" for _ in range(36))
    hud = f"""
{TICKS}<div class="chip panel mono"><i></i>ONO AR · CAMPUS TOUR</div>
<div id="tagW" class="ar panel" data-follow="wall" data-anchor="t" data-dx="-330" data-dy="150"><span class="en">Podcast studio</span><span class="he">אולפן הפודקאסט</span></div>
<div class="mic" id="mA" data-follow="mic_near_left" data-anchor="c"><div class="m"></div><div class="l panel mono">MIC A</div></div>
<div class="mic" id="mB" data-follow="mic_near_right" data-anchor="c"><div class="m"></div><div class="l panel mono">MIC B</div></div>
<div id="rec" class="panel mono"><i></i>REC</div>
<div id="wave" class="panel">{bars}</div>
"""
    js = r"""
const W = [...document.querySelectorAll("#wave b")];
window.onPlace = (t) => {
  const on = t > 3.6 ? Math.min(1, (t - 3.6) / .4) : 0;
  W.forEach((b, i) => {
    const v = Math.abs(Math.sin(t * 9 + i * .7) * Math.sin(t * 3.1 + i * .31));
    b.style.height = (6 + on * v * 60) + "px";
  });
};
tl.fromTo(".tick", {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:.45, stagger:.05}, .05);
tl.fromTo(".chip", {opacity:0, x:20}, {opacity:1, x:0, duration:.4}, .2);
tl.fromTo("#tagW", {opacity:0, y:16}, {opacity:1, y:0, duration:.5, ease:"expo.out"}, .6);
tl.fromTo("#mA .m", {scale:0}, {scale:1, duration:.35, ease:"back.out(3)"}, 1.5);
tl.fromTo("#mA .l", {opacity:0, x:-8}, {opacity:1, x:0, duration:.3}, 1.6);
tl.fromTo("#mB .m", {scale:0}, {scale:1, duration:.35, ease:"back.out(3)"}, 1.8);
tl.fromTo("#mB .l", {opacity:0, x:-8}, {opacity:1, x:0, duration:.3}, 1.9);
tl.fromTo("#rec", {opacity:0, scale:1.2}, {opacity:1, scale:1, duration:.3, ease:"power4.out"}, 3.55);
tl.to("#rec i", {opacity:.2, duration:.4, repeat:5, yoyo:true, ease:"none"}, 3.9);
tl.fromTo("#wave", {opacity:0, y:20}, {opacity:1, y:0, duration:.4}, 3.6);
"""
    sfx = [cue("ar_whoosh", .1, .5), cue("glass_ting", .6, .65), cue("mic_click", 1.5, .6), cue("mic_click", 1.8, .5), cue("rec_beep", 3.55, .7)]
    return dict(project=R / "videos/c2-podcast", clip=R / "C_campus_hud/clips/C2_seedance_720p.mp4",
                track=R / "tools/C2_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.7)


def C3():
    css = C_CSS + r"""
#tagA{transform:translate(-100%,0)}
#tagK{transform:translate(0,-50%)}
#tagG{transform:translate(-100%,-50%)}
#tagG .en{font-size:30px}
#endg{position:absolute;left:0;right:0;bottom:0;height:520px;background:linear-gradient(180deg,transparent,rgba(5,9,6,.92) 60%)}
#end{position:absolute;left:0;right:0;bottom:120px;display:flex;flex-direction:column;align-items:center}
#end img{width:380px;display:block;background:#fff;padding:18px 26px;border-radius:10px;box-sizing:content-box}
#end .en{font-size:56px;font-weight:800;margin-top:22px;line-height:1.1}
#end .he{font-size:44px;font-weight:700;margin-top:6px;text-align:center}
"""
    hud = f"""
{TICKS}<div class="chip panel mono"><i></i>ONO AR · CAMPUS TOUR</div>
<div id="tagA" class="ar panel" data-follow="stairs" data-anchor="l" data-dx="-30" data-dy="40"><span class="en">Central atrium</span><span class="he">האטריום המרכזי</span></div>
<div data-follow="skylight" data-anchor="r" data-dx="10"><div class="dot"></div></div>
<div id="tagK" class="ar panel" data-follow="skylight" data-anchor="r" data-dx="40"><span class="en">Skylight</span><span class="he">חלון הגג</span></div>
<div id="tagG" class="ar panel" data-follow="head" data-anchor="l" data-dx="-36"><span class="en">Guy Aga</span><span class="he">אורח בקמפוס</span></div>
<div id="endg"></div>
<div id="end"><img src="assets/ono_logo.png" alt="Ono Academic College"><span class="en">Welcome to Ono</span><span class="he">ברוכים הבאים לאונו</span></div>
"""
    js = r"""
tl.fromTo(".tick", {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:.45, stagger:.05}, .05);
tl.fromTo(".chip", {opacity:0, x:20}, {opacity:1, x:0, duration:.4}, .2);
tl.fromTo("#tagA", {opacity:0, clipPath:"inset(0 0 0 100%)"}, {opacity:1, clipPath:"inset(0 0 0 0%)", duration:.5, ease:"expo.out"}, .5);
tl.fromTo("#tagG", {opacity:0, x:-16}, {opacity:1, x:0, duration:.45, ease:"power3.out"}, 1.6);
tl.to("#tagG", {opacity:0, duration:.3}, 3.6);
tl.fromTo(".dot", {scale:0}, {scale:1, duration:.35, ease:"back.out(3)"}, 2.3);
tl.fromTo("#tagK", {opacity:0, x:-16}, {opacity:1, x:0, duration:.45, ease:"power3.out"}, 2.4);
tl.to(["#tagA", "#tagK", ".dot", ".chip"], {opacity:0, duration:.35}, 4.1);
tl.fromTo("#endg", {opacity:0}, {opacity:1, duration:.6}, 4.2);
tl.fromTo("#end img", {opacity:0, scale:.85}, {opacity:1, scale:1, duration:.8, ease:"expo.out"}, 4.35);
tl.fromTo("#end .en", {opacity:0, y:16}, {opacity:1, y:0, duration:.5, ease:"power3.out"}, 4.7);
tl.fromTo("#end .he", {opacity:0, y:16}, {opacity:1, y:0, duration:.5, ease:"power3.out"}, 4.85);
"""
    sfx = [cue("ar_whoosh", .1, .5), cue("glass_ting", .5, .6), cue("glass_ting", 1.6, .5), cue("glass_ting", 2.35, .55), cue("logo_hit", 4.3, .8)]
    return dict(extra={"ono_logo.png": LOGO}, project=R / "videos/c3-atrium", clip=R / "C_campus_hud/clips/C3_seedance_720p.mp4",
                track=R / "tools/C3_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.7)


# ---------------------------------------------------------------- B4 long helmet HUD, Hebrew
def B4():
    css = B_CSS + r"""
#visor{overflow:visible}
#vin{position:absolute;inset:0;direction:rtl;font-family:"Assistant",sans-serif}
#vin .num{font-family:"JetBrains Mono",monospace;direction:ltr;unicode-bidi:isolate;display:inline-block}
.pn{position:absolute;padding:16px 20px;background:rgba(12,8,4,.8);border-radius:6px}
.k{display:block;font-size:22px;font-weight:600;color:var(--mute)}
.v{display:block;font-size:44px;font-weight:700;line-height:1.1;color:var(--fg)}
.v small{font-size:22px;font-weight:600;color:var(--mute);margin-inline-start:6px}
#boot{left:0;right:0;margin:0 auto;top:9%;width:max-content;text-align:center;border-top:3px solid var(--acc)}
#boot .t{display:block;font-size:40px;font-weight:800}
#boot .s{display:block;font-size:24px;font-weight:600;color:var(--mute);margin-top:4px}
#boot .ok{color:#ffd28a}
#vit{left:3%;top:24%;width:21%}
#vit .row{margin-bottom:10px}
#msg{right:3%;top:22%;width:31%;border-right:4px solid var(--acc)}
#msg .h{display:block;font-size:22px;font-weight:700;color:#ffd28a;letter-spacing:.02em}
#msg .l{display:block;font-size:30px;font-weight:600;line-height:1.35;min-height:1.35em;color:var(--fg)}
#warn{right:3%;top:60%;width:31%;border:2px solid var(--warn);background:rgba(40,6,4,.85)}
#warn .t{display:block;font-size:36px;font-weight:800;color:#ffd9d6}
#warn .s{display:block;font-size:26px;font-weight:600;color:#ffc2bc;margin-top:4px}
#ai{left:0;right:0;margin:0 auto;bottom:9%;width:max-content;text-align:center;border-bottom:3px solid var(--acc)}
#ai .k{font-size:20px}
#ai .q{display:block;font-size:40px;font-weight:700;color:var(--fg)}
#lockp{left:0;right:0;margin:0 auto;top:9%;width:420px;text-align:center;border:2px solid var(--warn)}
#lockp .t{display:block;font-size:36px;font-weight:800;color:#ffd9d6}
#lockp .bar{height:8px;background:rgba(255,244,226,.15);border-radius:4px;margin-top:10px;overflow:hidden;direction:ltr}
#lockp .f{height:100%;background:var(--warn);transform-origin:100% 50%}
#wpn{left:0;right:0;margin:0 auto;bottom:9%;width:max-content;text-align:center;border:2px solid var(--acc)}
#wpn .q{display:block;font-size:38px;font-weight:700}
#wpn .ok{display:block;font-size:30px;font-weight:800;color:#ffd28a;margin-top:6px}
#go{left:0;right:0;margin:0 auto;top:40%;width:max-content;font-size:96px;font-weight:800;padding:10px 44px;
  background:rgba(12,8,4,.72);border-top:3px solid var(--acc);border-bottom:3px solid var(--acc)}
#compass{position:absolute;left:30%;right:30%;top:2.5%;height:36px;overflow:hidden;direction:ltr;
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 20%,#000 80%,transparent)}
#tape{position:absolute;left:0;top:0;white-space:nowrap;font-size:18px;color:var(--fg)}
#tape span{display:inline-block;width:90px;text-align:center;border-left:1px solid rgba(255,244,226,.35)}
#needle{position:absolute;left:50%;top:calc(2.5% + 40px);width:0;height:0;margin-left:-9px;border-left:9px solid transparent;border-right:9px solid transparent;border-bottom:14px solid var(--acc)}
#eyebrk .brk i{width:18px;height:18px;border-width:2px}
#eyebrk.red .brk i{border-color:var(--warn)}
"""
    hud = f"""
<div id="visor" data-box="visor" data-pad="-30"><div id="vin">
  <div id="compass"><div id="tape" class="mono"></div></div><div id="needle"></div>
  <div id="boot" class="pn"><span class="t">מערכת ואנגארד מופעלת</span>
    <span class="s">סנכרון עצבי <span class="num" id="sync">0%</span> · <span class="ok" id="allok"></span></span></div>
  <div id="vit" class="pn">
    <div class="row"><span class="k">דופק</span><span class="v"><span class="num" id="bpm">72</span><small>פעימות/דקה</small></span></div>
    <div class="row"><span class="k">חמצן בדם</span><span class="v"><span class="num">98%</span></span></div>
    <div class="row"><span class="k">שלמות החליפה</span><span class="v"><span class="num">100%</span></span></div>
    <div class="row"><span class="k">כיוון</span><span class="v"><span class="num" id="hdg">072°</span></span></div></div>
  <div id="msg" class="pn"><span class="h">הודעה נכנסת · מפקדה</span>
    <span class="l" id="m1"></span><span class="l" id="m2"></span><span class="l" id="m3"></span></div>
  <div id="warn" class="pn"><span class="t">⚠ אזהרה</span><span class="s">2 עוינים · רחפן אחד</span>
    <span class="s">טווח <span class="num">140</span> מ׳ · כיוון <span class="num">072°</span></span></div>
  <div id="ai" class="pn"><span class="k">עוזר החליפה</span><span class="q" id="aiq"></span></div>
  <div id="lockp" class="pn"><span class="t" id="lockt">נעילת מטרה…</span><div class="bar"><div class="f" id="lockf"></div></div></div>
  <div id="wpn" class="pn"><span class="q">מערכת הנשק זמינה. לאשר?</span><span class="ok" id="wok"></span></div>
  <div id="go" class="pn">יוצאים לדרך</div>
</div></div>
<div id="eyebrk" data-box="eyes" data-pad="12">{BRK}</div>
"""
    js = r"""
const tape = document.getElementById("tape");
let th = ""; for (let d = 0; d < 720; d += 15) th += `<span>${String(d % 360).padStart(3, "0")}</span>`; tape.innerHTML = th;
const txt = (id, s) => { const e = document.getElementById(id); if (e.textContent !== s) e.textContent = s; };
const type = (id, full, t0, t, cps) => { const n = Math.max(0, Math.min(full.length, Math.floor((t - t0) * cps))); txt(id, [...full].slice(0, n).join("")); };
const lerp = (a, b, u) => a + (b - a) * Math.max(0, Math.min(1, u));
window.onPlace = (t) => {
  const e = boxAt("eyes", t), f = boxAt("face", t);
  const rel = (e && f) ? (((e[0] + e[2]) / 2 - (f[0] + f[2]) / 2) / (f[2] - f[0])) : 0;
  const hdg = 72 + rel * 90;
  tape.style.transform = `translateX(${-(hdg / 15) * 90 + 150}px)`;
  txt("hdg", String(Math.round((hdg + 360) % 360)).padStart(3, "0") + "°");
  txt("sync", Math.round(lerp(0, 99, (t - .6) / 1.8)) + "%");
  txt("allok", t > 2.7 ? "כל המערכות תקינות" : "");
  const bpm = t < 11 ? 72 : t < 15 ? lerp(72, 118, (t - 11) / 4) : t < 18 ? lerp(118, 94, (t - 15) / 3) : t < 21 ? 94 : lerp(94, 102, (t - 21) / 2);
  txt("bpm", String(Math.round(bpm)));
  type("m1", "ואנגארד, כאן מפקדה.", 7.4, t, 16);
  type("m2", "זוהתה תנועה חשודה בגזרה 07.", 8.7, t, 16);
  type("m3", "המשך בזהירות.", 10.3, t, 16);
  type("aiq", "נשום עמוק. אני איתך.", 15.4, t, 13);
  const lk = (t - 18.3) / 2.1;
  document.getElementById("lockf").style.transform = `scaleX(${Math.max(0, Math.min(1, lk))})`;
  txt("lockt", lk >= 1 ? "המטרה ננעלה" : "נעילת מטרה…");
  document.getElementById("eyebrk").classList.toggle("red", t > 11 && t < 15 || t > 18 && t < 21);
  txt("wok", t > 22.3 ? "✓ מאושר" : "");
};
// 0-4 boot
tl.fromTo("#vin", {opacity:0}, {opacity:1, duration:.3}, .1);
tl.fromTo("#compass", {opacity:0, y:-12}, {opacity:1, y:0, duration:.5, ease:"power3.out"}, .3);
tl.fromTo("#needle", {opacity:0}, {opacity:1, duration:.3}, .5);
tl.fromTo("#boot", {opacity:0, scale:1.15}, {opacity:1, scale:1, duration:.5, ease:"expo.out"}, .4);
tl.to("#boot", {opacity:0, y:-10, duration:.4, ease:"power2.in"}, 3.9);
tl.fromTo("#eyebrk .brk", {opacity:0, scale:1.4}, {opacity:.9, scale:1, duration:.4}, 1.2);
// 4-7 vitals
tl.fromTo("#vit", {opacity:0, x:-40}, {opacity:1, x:0, duration:.55, ease:"expo.out"}, 4.1);
tl.fromTo("#vit .row", {opacity:0, y:10}, {opacity:1, y:0, duration:.3, stagger:.15}, 4.3);
// 7-11 message
tl.fromTo("#msg", {opacity:0, x:40, clipPath:"inset(0 0 0 100%)"}, {opacity:1, x:0, clipPath:"inset(0 0 0 0%)", duration:.55, ease:"expo.out"}, 7.0);
tl.to("#msg", {opacity:0, duration:.3}, 10.9);
// 11-15 warning
tl.fromTo("#warn", {opacity:0, scale:1.15}, {opacity:1, scale:1, duration:.3, ease:"power4.out"}, 11.0);
tl.to("#warn", {opacity:.4, duration:.2, repeat:7, yoyo:true, ease:"none"}, 11.4);
tl.to("#warn", {opacity:0, duration:.4}, 15.0);
// 15-18 breathe
tl.fromTo("#ai", {opacity:0, y:16}, {opacity:1, y:0, duration:.5, ease:"power3.out"}, 15.2);
tl.to("#ai", {opacity:0, duration:.4}, 17.9);
// 18-21 lock
tl.fromTo("#lockp", {opacity:0, scale:1.2}, {opacity:1, scale:1, duration:.3, ease:"power4.out"}, 18.2);
tl.to("#lockp", {opacity:0, duration:.35}, 21.0);
// 21-24 weapons + go
tl.fromTo("#wpn", {opacity:0, y:16}, {opacity:1, y:0, duration:.45, ease:"power3.out"}, 21.1);
tl.to(["#wpn", "#vit", "#eyebrk"], {opacity:0, duration:.35}, 23.0);
tl.fromTo("#go", {opacity:0, scale:1.3}, {opacity:1, scale:1, duration:.5, ease:"expo.out"}, 23.1);
"""
    ticks = [cue("ui_tick", x, .35) for x in (7.4, 8.7, 10.3)]
    sfx = [cue("hud_boot", .1, .7), cue("data_chatter", .6, .3), cue("chime", 2.7, .45), cue("ui_whoosh", 4.05, .45),
           cue("ui_pop", 7.0, .6), *ticks, cue("warn_beep", 11.0, .8), cue("warn_beep", 12.2, .55), cue("heartbeat", 11.0, .55),
           cue("glass_ting", 15.3, .55), cue("lock_tone", 18.2, .6), cue("hit_confirm", 20.4, .7),
           cue("charge_up", 21.1, .7), cue("hit_confirm", 22.3, .6), cue("stinger", 23.05, .8)]
    return dict(project=R / "videos/b4-helmet-he", clip=R / "B_scifi/clips/B4_helmet_long_720p.mp4",
                track=R / "tools/B4_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.7)


# ---------------------------------------------------------------- D1 runway, shoppable callouts (English)
D_ITEMS = [  # key, tracked obj, anchor, side, slot_y, t0, index, name, material, price
    ("coat", "coat", "l:35:-70", "L", 210, 1.0, "01", "The Camel Overcoat", "Double-faced wool", 890),
    ("knit", "knit", "c", "R", 240, 2.1, "02", "Silk Rib Turtleneck", "Silk & merino", 240),
    ("trousers", "trousers", "b:-18:-110", "L", 500, 3.2, "03", "Pleated Wide Trouser", "Italian wool crepe", 360),
    ("bag", "bag", "c", "R", 540, 4.3, "04", "Mini Frame Bag", "Calf leather", 520),
    ("boots", "boots", "c", "L", 790, 5.4, "05", "Pointed Ankle Boot", "Polished calf", 410),
]


def D1():
    fonts = "".join(
        f'@font-face{{font-family:"Bodoni Moda";font-weight:{w};src:url(assets/fonts/bodoni-moda-latin-{w}.woff2) format("woff2")}}'
        for w in (400, 500, 600, 700))
    fonts += '@font-face{font-family:"Bodoni Moda";font-style:italic;font-weight:400;src:url(assets/fonts/bodoni-moda-latin-400-italic.woff2) format("woff2")}'
    fonts += "".join(
        f'@font-face{{font-family:"Archivo";font-weight:{w};src:url(assets/fonts/archivo-latin-{w}.woff2) format("woff2")}}'
        for w in (400, 500, 600, 700))
    total = sum(i[9] for i in D_ITEMS)
    css = fonts + r"""
:root{--ivory:#f4efe6;--ink:#16130f;--sand:#d8ccb8;--mute:#5d544a}
#root{font-family:"Archivo",sans-serif}
.serif{font-family:"Bodoni Moda",serif}
#brand{position:absolute;left:110px;top:64px;padding:16px 22px;background:rgba(244,239,230,.92);border:1px solid var(--ink)}
#brand .b{display:block;font-family:"Bodoni Moda",serif;font-size:40px;font-weight:600;letter-spacing:.24em;color:var(--ink)}
#brand .s{display:block;font-size:15px;font-weight:600;letter-spacing:.28em;color:var(--mute);margin-top:6px}
#lines{position:absolute;inset:0;width:1920px;height:1080px}
.gdot{position:absolute;left:0;top:0;width:0;height:0}
.gdot i{position:absolute;left:-8px;top:-8px;width:16px;height:16px;border-radius:50%;background:var(--ink);box-shadow:0 0 0 4px var(--ivory)}
.card{position:absolute;width:420px;display:flex;gap:18px;align-items:center;padding:14px;background:var(--ivory);border:1px solid var(--ink)}
.card.L{left:110px}.card.R{left:1390px}
.badge{width:104px;height:104px;flex:0 0 104px;background:#ede6da;overflow:hidden;border:1px solid rgba(22,19,15,.25)}
.badge img{width:100%;height:100%;object-fit:contain;display:block}
.info{flex:1;min-width:0}
.idx{display:block;font-size:14px;font-weight:600;letter-spacing:.24em;color:var(--mute)}
.nm{display:block;font-family:"Bodoni Moda",serif;font-size:27px;font-weight:500;line-height:1.1;color:var(--ink);margin-top:4px}
.mt{display:block;font-size:14px;font-weight:500;letter-spacing:.18em;text-transform:uppercase;color:var(--mute);margin-top:6px}
.pr{display:block;font-size:24px;font-weight:700;color:var(--ink);margin-top:6px}
#shop{position:absolute;right:110px;bottom:64px;width:max-content;display:flex;align-items:center;gap:26px;
  padding:16px 30px;background:var(--ink);color:var(--ivory)}
#shop .a{font-family:"Bodoni Moda",serif;font-style:italic;font-size:32px}
#shop .b{font-size:16px;font-weight:600;letter-spacing:.26em}
#shop .c{font-size:30px;font-weight:700}
#shop i{display:block;width:1px;height:30px;background:rgba(244,239,230,.4)}
"""
    cards, dots = [], []
    for key, obj, anc, side, y, t0, idx, name, mat, price in D_ITEMS:
        cards.append(f'<div class="card {side}" id="c-{key}" style="top:{y}px"><div class="badge"><img src="assets/items/{key}.png" alt="{name}"></div>'
                     f'<div class="info"><span class="idx">{idx}</span><span class="nm">{name}</span><span class="mt">{mat}</span>'
                     f'<span class="pr">${price:,}</span></div></div>')
        a, dx, dy = (anc.split(":") + ["0", "0"])[:3]
        dots.append(f'<div class="gdot" id="d-{key}" data-follow="{obj}" data-anchor="{a}" data-dx="{dx}" data-dy="{dy}"><i></i></div>')
    paths = "".join(f'<path id="p-{i[0]}" fill="none" stroke="#16130f" stroke-width="2"/>' for i in D_ITEMS)
    hud = f"""
<svg id="lines" viewBox="0 0 1920 1080">{paths}</svg>
{''.join(dots)}
{''.join(cards)}
<div id="brand"><span class="b">ATELIER VEYRA</span><span class="s">AUTUMN / WINTER 2026 · LOOK 07</span></div>
<div id="shop"><span class="a">Shop the look</span><i></i><span class="b">5 PIECES</span><i></i><span class="c">${total:,}</span></div>
"""
    items_js = ",".join(f'["{i[0]}","{i[1]}","{i[2]}","{i[3]}",{i[4]},{i[5]}]' for i in D_ITEMS)
    js = r"""
const ITEMS = [__ITEMS__];
const CARD_H = 134;
window.onPlace = (t) => {
  for (const [key, obj, anc, side, y, t0] of ITEMS) {
    const b = boxAt(obj, t), p = document.getElementById("p-" + key);
    if (!b) continue;
    const [an, dx, dy] = (anc + ":0:0").split(":");
    const a0 = anchor(b, an), a = [a0[0] + (+dx), a0[1] + (+dy)];
    const u = Math.max(0, Math.min(1, (t - t0) / .45));
    const ex = side === "L" ? 110 + 420 : 1390, ey = y + CARD_H / 2;
    const mx = side === "L" ? Math.min(a[0] - 60, ex + 120) : Math.max(a[0] + 60, ex - 120);
    const pts = [[a[0], a[1]], [mx, ey], [ex, ey]];
    // partial polyline by length
    const segs = [Math.hypot(pts[1][0]-pts[0][0], pts[1][1]-pts[0][1]), Math.hypot(pts[2][0]-pts[1][0], pts[2][1]-pts[1][1])];
    let want = (segs[0] + segs[1]) * u, d = `M${pts[0][0]},${pts[0][1]}`;
    for (let i = 0; i < 2 && want > 0; i++) {
      const f = Math.min(1, want / segs[i]);
      d += ` L${pts[i][0] + (pts[i+1][0]-pts[i][0]) * f},${pts[i][1] + (pts[i+1][1]-pts[i][1]) * f}`;
      want -= segs[i];
    }
    p.setAttribute("d", u > 0 ? d : "");
  }
};
tl.fromTo("#brand", {opacity:0, y:-14}, {opacity:1, y:0, duration:.6, ease:"power3.out"}, .2);
for (const [key, , , side, , t0] of ITEMS) {
  tl.fromTo(`#d-${key} i`, {scale:0}, {scale:1, duration:.3, ease:"back.out(3)"}, t0 - .15);
  tl.fromTo(`#c-${key}`, {opacity:0, x: side === "L" ? -24 : 24, clipPath: side === "L" ? "inset(0 0 0 100%)" : "inset(0 100% 0 0)"},
            {opacity:1, x:0, clipPath:"inset(0 0 0 0%)", duration:.55, ease:"expo.out"}, t0 + .38);
  tl.fromTo(`#c-${key} .badge img`, {scale:1.25}, {scale:1, duration:.8, ease:"power3.out"}, t0 + .38);
}
tl.fromTo("#shop", {opacity:0, y:24}, {opacity:1, y:0, duration:.6, ease:"expo.out"}, 7.4);
""".replace("__ITEMS__", items_js)
    sfx = [cue("ui_whoosh", .15, .35)] + [cue("ui_pop", i[5] - .15, .55) for i in D_ITEMS] + [cue("chime", 7.4, .5)]
    extra = {f"items/{i[0]}.png": R / f"D_runway/stills/items/{i[0]}.png" for i in D_ITEMS}
    for f in (R / "shared/fonts").glob("bodoni-moda-*.woff2"):
        extra[f"fonts/{f.name}"] = f
    for f in (R / "shared/fonts").glob("archivo-*.woff2"):
        extra[f"fonts/{f.name}"] = f
    return dict(extra=extra, project=R / "videos/d1-runway", clip=R / "D_runway/clips/D1_runway_720p.mp4",
                track=R / "tools/D1_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.8)


# ---------------------------------------------------------------- D1S runway, social "stomp" style
# Beat grid measured with librosa from shared/sfx/runway_beat.mp3: 120.2 BPM, kicks at 0.51 + 0.5*n s
BEAT0, BEAT = 0.51, 0.5
D_STOMP = [  # key, word, follow obj, anchor, dx, dy, side, beat index of word, name, price
    ("coat", "COAT", "coat", "l", -40, -40, "L", 1, "The Camel Overcoat", 890),
    ("knit", "KNIT", "coat", "tr", 40, 120, "R", 4, "Silk Rib Turtleneck", 240),
    ("trousers", "TROUSER", "coat", "l", -40, 330, "L", 7, "Pleated Wide Trouser", 360),
    ("bag", "BAG", "bag", "r", 50, -60, "R", 10, "Mini Frame Bag", 520),
    ("boots", "BOOTS", "boots", "l", -60, 20, "L", 13, "Pointed Ankle Boot", 410),
]


def D1S():
    b = lambda i: round(BEAT0 + BEAT * i, 3)  # noqa: E731
    fonts = '@font-face{font-family:"Anton";font-weight:400;src:url(assets/fonts/anton-latin-400.woff2) format("woff2")}'
    fonts += '@font-face{font-family:"Bodoni Moda";font-style:italic;font-weight:400;src:url(assets/fonts/bodoni-moda-latin-400-italic.woff2) format("woff2")}'
    fonts += '@font-face{font-family:"Bodoni Moda";font-weight:600;src:url(assets/fonts/bodoni-moda-latin-600.woff2) format("woff2")}'
    fonts += "".join(f'@font-face{{font-family:"Archivo";font-weight:{w};src:url(assets/fonts/archivo-latin-{w}.woff2) format("woff2")}}' for w in (500, 700))
    total = sum(i[9] for i in D_STOMP)
    css = fonts + r"""
:root{--ivory:#f6f1e8;--ink:#16130f;--hot:#ff3d2e}
#root{font-family:"Archivo",sans-serif}
#stage{position:absolute;inset:0}
#flash{position:absolute;inset:0;background:#fff;opacity:0}
.grp{position:absolute;left:0;top:0;width:0;height:0}
.inner{position:absolute;top:0;display:flex;flex-direction:column}
.grp.L .inner{right:0;align-items:flex-end}
.grp.R .inner{left:0;align-items:flex-start}
.word{font-family:"Anton",sans-serif;font-size:180px;line-height:1;color:var(--ivory);letter-spacing:.01em;
  text-shadow:7px 7px 0 var(--ink);-webkit-text-stroke:3px var(--ink);white-space:nowrap}
.idx{display:inline-block;background:var(--hot);color:var(--ink);font-weight:700;font-size:22px;letter-spacing:.14em;padding:6px 12px;margin-bottom:10px;border:3px solid var(--ink)}
.stk{display:flex;align-items:center;gap:16px;margin-top:44px;padding:12px 18px 12px 12px;background:var(--ivory);border:3px solid var(--ink);box-shadow:8px 8px 0 var(--ink)}
#g-trousers .inner,#g-boots .inner{top:auto;bottom:0}
.grp.L .stk{transform:rotate(-4deg)}.grp.R .stk{transform:rotate(3deg)}
.stk img{width:112px;height:112px;object-fit:contain;background:#ede6da;border:2px solid var(--ink);display:block}
.stk .nm{display:block;font-family:"Bodoni Moda",serif;font-style:italic;font-size:32px;color:var(--ink);white-space:nowrap}
.stk .pr{display:inline-block;margin-top:8px;background:var(--hot);color:var(--ink);font-weight:700;font-size:34px;padding:4px 14px;border:3px solid var(--ink)}
#brand{position:absolute;left:96px;top:72px;display:flex;align-items:center;gap:14px}
#brand .b{font-family:"Bodoni Moda",serif;font-weight:600;font-size:40px;letter-spacing:.22em;color:var(--ink);background:var(--ivory);padding:8px 18px;border:3px solid var(--ink)}
#brand .s{font-family:"Anton",sans-serif;font-size:40px;color:var(--ink);background:var(--hot);padding:4px 16px;border:3px solid var(--ink)}
#fin{position:absolute;inset:0}
#fin .dim{position:absolute;inset:0;background:rgba(22,19,15,.55)}
#fin .t{position:absolute;left:0;right:0;top:150px;text-align:center;font-family:"Anton",sans-serif;font-size:300px;line-height:.9;color:var(--ivory);
  text-shadow:10px 10px 0 var(--hot);-webkit-text-stroke:4px var(--ink)}
#fin .row{position:absolute;left:0;right:0;top:560px;display:flex;justify-content:center;gap:22px}
#fin .row img{width:170px;height:170px;object-fit:contain;background:var(--ivory);border:3px solid var(--ink);box-shadow:7px 7px 0 var(--hot)}
#fin .tot{position:absolute;left:0;right:0;margin:0 auto;top:800px;width:max-content;display:flex;align-items:center;gap:20px}
#fin .tot .a{font-family:"Bodoni Moda",serif;font-style:italic;font-size:44px;color:var(--ivory)}
#fin .tot .c{font-family:"Anton",sans-serif;font-size:96px;color:var(--ink);background:var(--hot);padding:0 24px;border:4px solid var(--ivory)}
"""
    grps = []
    for key, word, obj, anc, dx, dy, side, bi, name, price in D_STOMP:
        n = D_STOMP.index(next(x for x in D_STOMP if x[0] == key)) + 1
        grps.append(f'<div class="grp {side}" id="g-{key}" data-follow="{obj}" data-anchor="{anc}" data-dx="{dx}" data-dy="{dy}"><div class="inner">'
                    f'<span class="idx">{n:02d} / 05</span><span class="word">{word}</span>'
                    f'<div class="stk"><img src="assets/items/{key}.png" alt="{name}"><div><span class="nm">{name}</span>'
                    f'<span class="pr">${price:,}</span></div></div></div></div>')
    row = "".join(f'<img src="assets/items/{i[0]}.png" alt="{i[8]}">' for i in D_STOMP)
    hud = f"""
<div id="stage">
{''.join(grps)}
<div id="brand"><span class="b">ATELIER VEYRA</span><span class="s">AW26</span></div>
<div id="fin"><div class="dim"></div><div class="t">THE LOOK</div><div class="row">{row}</div>
  <div class="tot"><span class="a">five pieces</span><span class="c">${total:,}</span></div></div>
</div>
<div id="flash"></div>
"""
    beats = [b(x) for x in range(21)]
    js = r"""
const B = (i) => +(0.51 + 0.5 * i).toFixed(3);
function shake(at) {
  tl.to("#stage", {keyframes: [{x: -14, y: 6, duration: .04}, {x: 11, y: -5, duration: .04}, {x: -6, y: 3, duration: .04}, {x: 0, y: 0, duration: .06}], ease: "none"}, at);
  tl.fromTo("#flash", {opacity: .45}, {opacity: 0, duration: .14, ease: "power2.out"}, at);
}
function stomp(sel, at, from = 1.9) {
  tl.fromTo(sel, {opacity: 0, scale: from}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, at);
  shake(at);
}
tl.set("#fin", {opacity: 0}, 0);
stomp("#brand", B(0), 1.5);
const ITEMS = __ITEMS__;
ITEMS.forEach(([key, bi], k) => {
  const g = `#g-${key}`;
  tl.fromTo(`${g} .idx`, {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .12, ease: "power3.out"}, B(bi) - .12);
  stomp(`${g} .word`, B(bi));
  tl.fromTo(`${g} .stk`, {opacity: 0, scale: 1.5, y: 30}, {opacity: 1, scale: 1, y: 0, duration: .18, ease: "back.out(2.2)"}, B(bi + 1));
  const out = k < ITEMS.length - 1 ? B(ITEMS[k + 1][1]) - .14 : B(15) - .1;
  tl.to(`${g} .inner`, {opacity: 0, scale: .85, duration: .12, ease: "power2.in"}, out);
});
tl.to("#brand", {opacity: 0, duration: .12}, B(15) - .1);
tl.to("#fin", {opacity: 1, duration: .01}, B(16) - .02);
tl.fromTo("#fin .dim", {opacity: 0}, {opacity: 1, duration: .15}, B(16) - .05);
stomp("#fin .t", B(16), 2.2);
tl.fromTo("#fin .row img", {opacity: 0, scale: 1.6, y: 40}, {opacity: 1, scale: 1, y: 0, duration: .16, stagger: .1, ease: "back.out(2)"}, B(17));
stomp("#fin .tot", B(18), 1.8);
""".replace("__ITEMS__", "[" + ",".join(f'["{i[0]}",{i[7]}]' for i in D_STOMP) + "]")
    stomp_sfx = ("soft_thump", "Deep soft round sub thump, clean and warm, subtle impact, no whoosh, no noise, no distortion", 0.6)
    pop_sfx = ("soft_click", "Soft subtle clean click, quiet and elegant, like a camera shutter in the distance", 0.5)
    sfx = [("fashion_elegant_11000", "music", 11, 0.0, 0.75)]
    hits = [b(0)] + [b(i[7]) for i in D_STOMP] + [b(16), b(18)]
    sfx += [(stomp_sfx[0], stomp_sfx[1], stomp_sfx[2], h - .02, .45) for h in hits]
    sfx += [(pop_sfx[0], pop_sfx[1], pop_sfx[2], b(i[7] + 1) - .02, .3) for i in D_STOMP]
    extra = {f"items/{i[0]}.png": R / f"D_runway/stills/items/{i[0]}.png" for i in D_STOMP}
    for pat in ("anton-*.woff2", "bodoni-moda-*.woff2", "archivo-*.woff2"):
        for f in (R / "shared/fonts").glob(pat):
            extra[f"fonts/{f.name}"] = f
    return dict(extra=extra, project=R / "videos/d1-runway-stomp", clip=R / "D_runway/clips/D1_runway_720p.mp4",
                track=R / "tools/D1_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.18)


def D1G():
    """Stomp, 'glass' variant: transparent outlined titles + smoked-glass price cards."""
    cfg = D1S()
    cfg["css"] += r"""
.word{color:rgba(22,19,15,.46);-webkit-text-stroke:4px rgba(246,241,232,.98);text-shadow:0 0 36px rgba(22,19,15,.55)}
.idx{background:rgba(22,19,15,.55);color:var(--ivory);border:1.5px solid rgba(246,241,232,.8);backdrop-filter:blur(10px)}
.stk{background:rgba(22,19,15,.42);border:1.5px solid rgba(246,241,232,.75);box-shadow:none;backdrop-filter:blur(16px) saturate(1.2);border-radius:14px}
.grp.L .stk,.grp.R .stk{transform:none}
.stk img{background:rgba(246,241,232,.9);border:0;border-radius:8px}
.stk .nm{color:var(--ivory)}
.stk .pr{background:rgba(246,241,232,.92);color:var(--ink);border:0;border-radius:6px}
#brand .b{background:rgba(22,19,15,.45);color:var(--ivory);border:1.5px solid rgba(246,241,232,.8);backdrop-filter:blur(12px)}
#brand .s{background:rgba(246,241,232,.9);color:var(--ink);border:0}
#fin .dim{background:rgba(22,19,15,.35);backdrop-filter:blur(8px)}
#fin .t{color:rgba(246,241,232,.12);-webkit-text-stroke:4px var(--ivory);text-shadow:none}
#fin .row img{background:rgba(246,241,232,.9);border:0;border-radius:12px;box-shadow:none}
#fin .tot .c{background:rgba(246,241,232,.92);color:var(--ink);border:0;border-radius:8px}
#flash{background:rgba(246,241,232,1)}
"""
    cfg["project"] = R / "videos/d1-runway-glass"
    return cfg


def D1B():
    """Stomp, 'behind the model' variant: giant words sit between the plate and a matted model."""
    cfg = D1S()
    words = "".join(f'<div class="bw" id="w-{i[0]}" data-follow="coat" data-anchor="t" data-dy="{-40 if i[0] != "boots" else 120}">'
                    f'<span data-layout-allow-overlap>{i[1]}</span></div>' for i in D_STOMP)
    stickers = []
    BDY = {"coat": 110, "knit": 270, "trousers": 150, "bag": 90, "boots": -190}
    for key, word, obj, anc, dx, dy, side, bi, name, price in D_STOMP:
        n = [x[0] for x in D_STOMP].index(key) + 1
        stickers.append(f'<div class="grp {side}" id="g-{key}" data-follow="{obj}" data-anchor="{anc}" data-dx="{dx}" data-dy="{BDY[key]}"><div class="inner">'
                        f'<span class="idx">{n:02d} / 05</span>'
                        f'<div class="stk"><img src="assets/items/{key}.png" alt="{name}"><div><span class="nm">{name}</span>'
                        f'<span class="pr">${price:,}</span></div></div></div></div>')
    row = "".join(f'<img src="assets/items/{i[0]}.png" alt="{i[8]}">' for i in D_STOMP)
    total = sum(i[9] for i in D_STOMP)
    cfg["hud"] = f"""
<div id="stage">{words}<div id="fint" class="bw"><span data-layout-allow-overlap>THE LOOK</span></div></div>
<!--MATTE-->
<div id="stage2">
{''.join(stickers)}
<div id="brand"><span class="b">ATELIER VEYRA</span><span class="s">AW26</span></div>
<div id="fin"><div class="row">{row}</div><div class="tot"><span class="a">five pieces</span><span class="c">${total:,}</span></div></div>
</div>
<div id="flash"></div>
"""
    cfg["css"] += r"""
#stage2{position:absolute;inset:0}
#g-trousers .inner,#g-boots .inner{top:0;bottom:auto}
.bw{position:absolute;left:0;top:0;width:0;height:0}
.bw span{position:absolute;left:0;top:0;transform:translate(-50%,0);font-family:"Anton",sans-serif;font-size:430px;line-height:1;
  color:var(--ivory);white-space:nowrap;text-shadow:12px 12px 0 var(--hot)}
#fint{left:960px;top:40px}
#fint span{font-size:340px;color:var(--hot);text-shadow:12px 12px 0 var(--ink)}
.stk{margin-top:14px}
#fin .row{top:700px}
#fin .tot{top:900px}
"""
    js = cfg["js"]
    js = js.replace('tl.to("#stage", {keyframes:', 'tl.to(["#stage", "#stage2"], {keyframes:')
    js = js.replace('stomp(`${g} .word`, B(bi));', 'stomp(`#w-${key} span`, B(bi));\n  tl.to(`#w-${key} span`, {opacity: 0, duration: .1}, (k < ITEMS.length - 1 ? B(ITEMS[k + 1][1]) : B(15)) - .12);')
    js = js.replace('tl.set("#fin", {opacity: 0}, 0);', 'tl.set(["#fin", "#fint"], {opacity: 0}, 0);')
    js = js.replace('tl.fromTo("#fin .dim", {opacity: 0}, {opacity: 1, duration: .15}, B(16) - .05);\nstomp("#fin .t", B(16), 2.2);',
                    'tl.to("#fint", {opacity: 1, duration: .01}, B(16) - .02);\nstomp("#fint span", B(16), 2.2);')
    cfg["js"] = js
    cfg["extra"]["matte.webm"] = R / "D_runway/matte/D1_model_alpha.webm"
    cfg["project"] = R / "videos/d1-runway-behind"
    return cfg


# ---------------------------------------------------------------- D2 full runway: walk (escort) -> spin -> 15s sale countdown
# Music: shared/sfx/runway_music_30s.mp3 (ElevenLabs Music), librosa: 120.2 BPM, beat 0 at 0.035s
D2_ITEMS = [  # key, word, side, beat, name, price
    ("coat", "COAT", "L", 10, "The Camel Overcoat", 890),
    ("knit", "KNIT", "R", 13, "Silk Rib Turtleneck", 240),
    ("trousers", "TROUSER", "L", 16, "Pleated Wide Trouser", 360),
    ("bag", "BAG", "R", 19, "Mini Frame Bag", 520),
    ("boots", "BOOTS", "L", 22, "Pointed Ankle Boot", 410),
]
SALE = 0.20


def D2(items=None, look="07", items_dir="items", proj="d2-runway-full", clip="D2_full_runway_720p.mp4", track="D2_vtrack.json", matte="D2_model_alpha.webm"):
    items = items or D2_ITEMS
    base = D1S()
    total = sum(i[5] for i in items)
    sale_total = round(total * (1 - SALE))
    css = base["css"] + r"""
#stage2{position:absolute;inset:0}
.esc{position:absolute;left:0;top:0;width:0;height:0}
.esc .sc{position:absolute;left:0;top:0;transform-origin:0 0}
.esc.L .sc{transform-origin:100% 0}
.esc .inner{position:relative;display:flex;flex-direction:column}
.esc.L .inner{align-items:flex-end}
.esc .word{font-size:170px}
.esc .stk{margin-top:30px}
#lk{position:absolute;left:0;top:0;width:0;height:0}
#lk span{position:absolute;left:0;bottom:24px;transform:translateX(-50%);white-space:nowrap;font-family:"Anton",sans-serif;font-size:44px;
  color:var(--ink);background:var(--ivory);padding:2px 16px;border:3px solid var(--ink);box-shadow:5px 5px 0 var(--hot)}
.bw{position:absolute;left:0;top:0;width:0;height:0}
.bw span{position:absolute;left:0;top:0;transform:translate(-50%,0);font-family:"Anton",sans-serif;font-size:520px;line-height:1;color:var(--hot);
  white-space:nowrap;text-shadow:14px 14px 0 var(--ink)}
#cta{position:absolute;right:80px;top:70px;width:560px}
#cta .pill{display:inline-block;font-family:"Anton",sans-serif;font-size:46px;color:var(--ink);background:var(--hot);padding:2px 18px;border:3px solid var(--ink)}
#cta .lbl{display:block;font-family:"Bodoni Moda",serif;font-style:italic;font-size:40px;color:var(--ink);margin-top:18px;background:var(--ivory);padding:6px 16px;width:max-content;border:3px solid var(--ink)}
#cta .was{position:relative;display:block;width:max-content;font-family:"Anton",sans-serif;font-size:64px;line-height:1.2;color:var(--ivory);background:var(--ink);padding:0 14px;margin-top:14px;margin-bottom:34px;text-shadow:4px 4px 0 var(--ink)}
#cta .was i{position:absolute;left:-6px;right:-6px;top:52%;height:8px;background:var(--hot);transform-origin:0 50%;border:2px solid var(--ink)}
#cta .now{display:block;font-family:"Anton",sans-serif;font-size:150px;line-height:1.15;margin-top:6px;margin-bottom:34px;color:var(--ivory);text-shadow:8px 8px 0 var(--ink);-webkit-text-stroke:3px var(--ink)}
#cta .off{display:block;width:max-content;margin-top:12px;font-weight:700;font-size:26px;letter-spacing:.12em;color:var(--ink);background:var(--ivory);padding:6px 14px;border:3px solid var(--ink)}
#timer{position:absolute;right:80px;top:740px;width:560px;background:var(--ink);border:4px solid var(--ivory);padding:14px 22px 18px;display:flex;flex-wrap:wrap;align-items:center;column-gap:26px}
#timer .bar{flex:0 0 100%}
#timer .k{display:block;width:150px;font-weight:700;font-size:22px;line-height:1.3;letter-spacing:.2em;color:var(--ivory)}
#timer .t{display:block;font-family:"Anton",sans-serif;font-size:120px;line-height:1.2;color:var(--ivory)}
#timer.hot .t{color:var(--hot)}
#timer .bar{height:12px;background:rgba(246,241,232,.2);margin-top:6px}
#timer .bar i{display:block;height:100%;background:var(--hot);transform-origin:0 50%}
#buy{position:absolute;left:0;right:0;margin:0 auto;bottom:40px;width:max-content;font-family:"Anton",sans-serif;font-size:60px;color:var(--ink);
  background:var(--hot);padding:6px 44px;border:4px solid var(--ink);box-shadow:8px 8px 0 var(--ink)}
#rail{position:absolute;left:70px;top:140px;display:flex;flex-direction:column;gap:14px}
#rail .it{display:flex;align-items:center;gap:12px;background:var(--ivory);border:3px solid var(--ink);padding:6px 14px 6px 6px;box-shadow:5px 5px 0 var(--ink)}
#rail img{width:86px;height:86px;object-fit:contain;background:#ede6da;display:block}
#rail .p{display:block;font-family:"Anton",sans-serif;font-size:36px;color:var(--ink)}
#rail .o{display:block;font-weight:700;font-size:18px;color:#4a4238;text-decoration:line-through}
"""
    esc = []
    for key, word, side, bi, name, price in items:
        n = [x[0] for x in items].index(key) + 1
        esc.append(f'<div class="esc {side}" id="e-{key}"><div class="sc"><div class="inner">'
                   f'<span class="idx">{n:02d} / 05</span><span class="word">{word}</span>'
                   f'<div class="stk"><img src="assets/items/{key}.png" alt="{name}"><div><span class="nm">{name}</span>'
                   f'<span class="pr">${price:,}</span></div></div></div></div></div>')
    rail = "".join(f'<div class="it"><img src="assets/items/{i[0]}.png" alt="{i[4]}"><div><span class="p">${round(i[5] * (1 - SALE)):,}</span>'
                   f'<span class="o">${i[5]:,}</span></div></div>' for i in items)
    hud = f"""
<div id="stage"><div class="bw" id="spinw" data-follow="model" data-anchor="t" data-dy="-60"><span data-layout-allow-overlap>AW26</span></div></div>
<!--MATTE-->
<div id="stage2">
<div id="lk" data-follow="model" data-anchor="t"><span>LOOK {look}</span></div>
{''.join(esc)}
<div id="brand"><span class="b">ATELIER VEYRA</span><span class="s">AW26</span></div>
<div id="rail">{rail}</div>
<div id="cta"><span class="pill">FLASH SALE</span><span class="lbl">the complete look</span>
  <span class="was">${total:,}<i></i></span><span class="now">${sale_total:,}</span><span class="off">−20% · NEXT 15 SECONDS ONLY</span></div>
<div id="timer"><span class="k">OFFER ENDS IN</span><span class="t" id="tt">00:15</span><div class="bar"><i id="tb"></i></div></div>
<div id="buy">SHOP NOW →</div>
</div>
<div id="flash"></div>
"""
    items_js = "[" + ",".join(f'["{i[0]}","{i[2]}",{i[3]}]' for i in items) + "]"
    js = r"""
const B = (i) => +(0.035 + 0.5 * i).toFixed(3);
const CD0 = B(29);  // countdown starts at 15 on this beat, hits 00 fifteen seconds later
function shake(at, amt = 1) {
  tl.to(["#stage", "#stage2"], {keyframes: [{x: -14 * amt, y: 6 * amt, duration: .04}, {x: 11 * amt, y: -5 * amt, duration: .04}, {x: -6 * amt, y: 3 * amt, duration: .04}, {x: 0, y: 0, duration: .06}], ease: "none"}, at);
  tl.fromTo("#flash", {opacity: .4 * amt}, {opacity: 0, duration: .14, ease: "power2.out"}, at);
}
function stomp(sel, at, from = 1.9) {
  tl.fromTo(sel, {opacity: 0, scale: from}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, at);
  shake(at);
}
const ITEMS = __ITEMS__;
window.onPlace = (t) => {
  const m = boxAt("model", t); if (!m) return;
  const h = m[3] - m[1], s = Math.max(.42, Math.min(1, h / 820));
  for (const [key, side] of ITEMS) {
    const e = document.getElementById("e-" + key), sc = e.firstElementChild;
    const x = side === "L" ? m[0] - 30 : m[2] + 30, y = m[1] + h * .18;
    e.style.left = x + "px"; e.style.top = y + "px";
    sc.style.transform = side === "L" ? `translateX(-100%) scale(${s})` : `scale(${s})`;
  }
  document.getElementById("lk").firstElementChild.style.fontSize = (44 * Math.max(.6, s)) + "px";
  const rem = Math.max(0, 15 - Math.floor(t - CD0));
  document.getElementById("tt").textContent = t < CD0 ? "00:15" : "00:" + String(rem).padStart(2, "0");
  document.getElementById("tb").style.transform = `scaleX(${t < CD0 ? 1 : Math.max(0, 1 - (t - CD0) / 15)})`;
  document.getElementById("timer").classList.toggle("hot", t >= CD0 + 10);
};
tl.set(["#spinw", "#rail", "#cta", "#timer", "#buy"], {opacity: 0}, 0);
stomp("#brand", B(1), 1.5);
tl.fromTo("#lk span", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .2, ease: "back.out(2)"}, B(4));
tl.to("#lk span", {opacity: 0, duration: .15}, B(9) - .1);
ITEMS.forEach(([key, side, bi], k) => {
  const g = `#e-${key}`;
  tl.fromTo(`${g} .idx`, {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .12}, B(bi) - .12);
  stomp(`${g} .word`, B(bi));
  tl.fromTo(`${g} .stk`, {opacity: 0, scale: 1.5, y: 24}, {opacity: 1, scale: 1, y: 0, duration: .18, ease: "back.out(2.2)"}, B(bi + 1));
  tl.to(`${g} .inner`, {opacity: 0, scale: .85, duration: .12, ease: "power2.in"}, (k < ITEMS.length - 1 ? B(ITEMS[k + 1][2]) : B(24)) - .14);
});
tl.to("#spinw", {opacity: 1, duration: .01}, B(24) - .02);
stomp("#spinw span", B(24), 2.4);
tl.to("#spinw", {opacity: 0, duration: .25}, B(29) - .3);
tl.to("#brand", {opacity: 0, duration: .15}, B(24));
// CTA
tl.to(["#rail", "#cta", "#timer", "#buy"], {opacity: 1, duration: .01}, B(29) - .02);
stomp("#cta .pill", B(29), 2);
tl.fromTo("#cta .lbl", {opacity: 0, x: 30}, {opacity: 1, x: 0, duration: .18, ease: "power3.out"}, B(30));
tl.fromTo("#cta .was", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .15}, B(30));
tl.fromTo("#cta .was i", {scaleX: 0}, {scaleX: 1, duration: .2, ease: "power3.out"}, B(31));
stomp("#cta .now", B(32), 2.1);
tl.fromTo("#cta .off", {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: .16}, B(33));
stomp("#timer", B(29), 1.6);
tl.fromTo("#rail .it", {opacity: 0, x: -40}, {opacity: 1, x: 0, duration: .16, stagger: .5, ease: "back.out(2)"}, B(30));
stomp("#buy", B(34), 1.7);
for (let k = 36; k < 60; k += 2) tl.fromTo("#buy", {scale: 1.08}, {scale: 1, duration: .3, ease: "power2.out"}, B(k));
for (let sec = 10; sec < 15; sec++) { tl.fromTo("#timer .t", {scale: 1.25}, {scale: 1, duration: .25, ease: "power3.out"}, CD0 + sec); shake(CD0 + sec, .5); }
""".replace("__ITEMS__", items_js)
    sfx = [("fashion_elegant_30000", "music", 30, 0.0, .75)]
    st = ("soft_thump", "Deep soft round sub thump, clean and warm, subtle impact, no whoosh, no noise, no distortion", 0.6)
    pop = ("soft_click", "Soft subtle clean click, quiet and elegant, like a camera shutter in the distance", 0.5)
    tick = ("soft_tick", "Single soft clean clock tick, quiet, warm", 0.5)
    tick_hot = ("soft_pulse", "Short soft low electronic pulse beep, round and warm, not harsh", 0.5)
    b = lambda i: round(0.035 + 0.5 * i, 3)  # noqa: E731
    hits = [b(1)] + [b(i[3]) for i in items] + [b(24), b(29), b(32), b(34)]
    sfx += [(*st, h - .02, .45) for h in hits]
    sfx += [(*pop, b(i[3] + 1) - .02, .3) for i in items]
    cd0 = b(29)
    sfx += [(*(tick_hot if s >= 10 else tick), cd0 + s, .35 if s >= 10 else .22) for s in range(1, 16)]
    extra = {k: v for k, v in base["extra"].items() if not k.startswith("items/")}
    extra.update({f"items/{i[0]}.png": R / f"D_runway/stills/{items_dir}/{i[0]}.png" for i in items})
    extra["matte.webm"] = R / f"D_runway/matte/{matte}"
    return dict(extra=extra, project=R / f"videos/{proj}", clip=R / f"D_runway/clips/{clip}",
                track=R / f"tools/{track}", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.15)


# ---------------------------------------------------------------- B4X long helmet, cinematic holographic HUD (Hebrew)
D3_ITEMS = [  # Look 08
    ("trench", "TRENCH", "L", 10, "The Ivory Trench", 780),
    ("knit", "CASHMERE", "R", 13, "Cashmere Rib Knit", 320),
    ("skirt", "SATIN", "L", 16, "Satin Midi Skirt", 290),
    ("tote", "TOTE", "R", 19, "Suede Tote", 460),
    ("boots", "BOOTS", "L", 22, "Knee Boot", 540),
]


def D3():
    return D2(items=D3_ITEMS, look="08", items_dir="items08", proj="d3-runway-look08",
              clip="D3_look08_runway_720p.mp4", track="D3_vtrack.json", matte="D3_model_alpha.webm")


def B4X():
    ring = lambda r, cls, dash="", sw=2: f'<circle class="{cls}" cx="0" cy="0" r="{r}" fill="none" stroke-width="{sw}" {dash}/>'  # noqa: E731
    css = r"""
:root{--cy:#6fe3ff;--txt:#e6fbff;--red:#ff4a5a;--amb:#ffb547;--bk:rgba(2,14,22,.62)}
#root{font-family:"Assistant",sans-serif}
.he{direction:rtl}
.g{color:var(--txt);text-shadow:0 0 10px rgba(90,220,255,.85),-1.5px 0 rgba(255,60,120,.4),1.5px 0 rgba(60,200,255,.4)}
.num{font-family:"JetBrains Mono",monospace;direction:ltr;unicode-bidi:isolate;display:inline-block}
svg{overflow:visible}
.rs{stroke:var(--cy)}.rs.dim{stroke:rgba(111,227,255,.35)}
.rot{transform-box:fill-box;transform-origin:center}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse 62% 70% at 50% 48%,transparent 55%,rgba(111,227,255,.10) 78%,rgba(111,227,255,.22) 100%)}
#vig.red{background:radial-gradient(ellipse 62% 70% at 50% 48%,transparent 55%,rgba(255,74,90,.14) 78%,rgba(255,74,90,.3) 100%)}
#scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(111,227,255,.05) 0 1px,transparent 1px 4px)}
#boot{position:absolute;left:0;top:0;width:0;height:0}
#boot svg{position:absolute;left:-450px;top:-450px}
.px{position:absolute;inset:0}
/* reticle on eyes */
#ret{position:absolute;left:0;top:0;width:0;height:0}
#ret svg{position:absolute;left:-220px;top:-220px}
#ret.red .rs{stroke:var(--red)}
/* left vitals cluster */
#lc{position:absolute;left:70px;top:210px;width:420px;perspective:1000px}
#lci{transform:rotateY(24deg);transform-origin:0 50%}
#hr{position:relative;width:300px;height:300px}
#hr svg{position:absolute;left:0;top:0}
#hr .c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
#hr .k{font-size:26px;font-weight:600}
#hr .v{font-size:84px;line-height:1}
#hr .u{font-size:18px;font-weight:600;opacity:.85}
.mini{display:flex;gap:26px;margin-top:10px;margin-inline-start:20px}
.mg{position:relative;width:120px;height:120px}
.mg svg{position:absolute;left:0;top:0}
.mg .c{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.mg .v{font-size:30px}.mg .k{font-size:18px;font-weight:600}
/* right message panel */
#rc{position:absolute;right:70px;top:190px;width:600px;perspective:1000px}
#rci{transform:rotateY(-24deg);transform-origin:100% 50%}
.frame{position:relative;padding:22px 30px 24px;background:var(--bk);clip-path:polygon(0 0,calc(100% - 28px) 0,100% 28px,100% 100%,28px 100%,0 calc(100% - 28px));
  border-right:3px solid var(--cy)}
.frame .h{display:block;font-size:24px;font-weight:700;color:var(--cy)}
.frame .l{display:block;font-size:32px;font-weight:600;line-height:1.4;min-height:1.4em}
#warn{position:absolute;right:70px;top:560px;width:600px;perspective:1000px}
#warn .frame{border-right-color:var(--red);background:rgba(40,4,10,.72)}
#warn .t{display:block;font-size:40px;font-weight:800;color:#ffe3e6;text-shadow:0 0 12px rgba(255,74,90,.9)}
#warn .s{display:block;font-size:26px;font-weight:600;color:#ffd0d5;margin-top:4px}
/* radar */
#rad{position:absolute;left:110px;bottom:70px;width:230px;height:230px;border-radius:50%;background:rgba(2,14,22,.5)}
#rad svg{position:absolute;left:0;top:0}
#sweep{position:absolute;inset:0;border-radius:50%;background:conic-gradient(from 0deg,rgba(111,227,255,.55),rgba(111,227,255,0) 70deg,transparent 360deg)}
.blip{position:absolute;width:14px;height:14px;margin:-7px 0 0 -7px;border-radius:50%;background:var(--red);box-shadow:0 0 14px var(--red)}
.blip.a{background:var(--amb);box-shadow:0 0 14px var(--amb)}
#radl{position:absolute;left:0;right:0;top:238px;text-align:center;font-size:20px;font-weight:600}
/* compass */
#cmp{position:absolute;left:0;right:0;margin:0 auto;top:40px;width:760px;height:60px;overflow:hidden;direction:ltr;background:rgba(2,14,22,.72);
  -webkit-mask-image:linear-gradient(90deg,transparent,#000 22%,#000 78%,transparent)}
#tape{position:absolute;left:0;top:10px;white-space:nowrap;font-size:20px}
#tape span{display:inline-block;width:80px;text-align:center;border-left:1px solid rgba(111,227,255,.45)}
#cmpn{position:absolute;left:0;right:0;margin:0 auto;top:104px;width:max-content;font-size:22px;font-weight:600;background:rgba(2,14,22,.72);padding:2px 14px}
/* data stream + meters */
#data{position:absolute;left:0;right:0;margin:0 auto;bottom:34px;width:900px;text-align:center;font-size:16px;letter-spacing:.14em;opacity:.8;direction:ltr}
#meters{position:absolute;right:40px;top:300px;display:flex;gap:8px;align-items:flex-end;height:220px}
#meters i{display:block;width:10px;background:linear-gradient(180deg,var(--cy),rgba(111,227,255,.2));transform-origin:50% 100%}
/* center messages */
.ctr{position:absolute;left:0;right:0;margin:0 auto;width:max-content;text-align:center}
#bootm{top:150px}
#bootm .t{display:block;font-size:46px;font-weight:800}
#bootm .s{display:block;font-size:26px;font-weight:600;margin-top:4px}
#ai{bottom:120px;padding:14px 34px;background:var(--bk)}
#ai .k{display:block;font-size:20px;font-weight:700;color:var(--cy)}
#ai .q{display:block;font-size:44px;font-weight:700}
#lockm{top:150px}
#lockm .t{display:block;font-size:44px;font-weight:800;color:#ffe3e6;text-shadow:0 0 14px rgba(255,74,90,.95)}
#lockm .p{display:block;font-size:30px;color:#ffd0d5}
#wpn{bottom:120px;padding:14px 34px;background:var(--bk)}
#wpn .q{display:block;font-size:40px;font-weight:700}
#wpn .ok{display:block;font-size:32px;font-weight:800;color:var(--amb);text-shadow:0 0 12px rgba(255,181,71,.9)}
#go{top:440px;font-size:120px;font-weight:800;letter-spacing:.02em;padding:0 40px;background:rgba(2,14,22,.55)}
"""
    ticks = "".join(f'<line x1="0" y1="-{r0}" x2="0" y2="-{r0 + (14 if k % 5 == 0 else 7)}" transform="rotate({k * 6})" />'
                    for k in range(60) for r0 in [132])
    hud = f"""
<div id="vig"></div><div id="scan"></div>
<div class="px" id="pxA">
  <div id="boot"><svg width="900" height="900" viewBox="-450 -450 900 900">{ring(420, "rs", 'id="bootring" stroke-dasharray="2640" stroke-dashoffset="2640"', 3)}</svg></div>
  <div id="ret"><svg width="440" height="440" viewBox="-220 -220 440 440">
    <g class="rot" id="rA">{ring(150, "rs dim", 'stroke-dasharray="6 10"', 2)}</g>
    <g class="rot" id="rB">{ring(118, "rs", 'stroke-dasharray="120 60 30 60"', 4)}</g>
    <g class="rot" id="rC">{ring(92, "rs dim", 'stroke-dasharray="2 6"', 6)}</g>
    <g id="tri"><path class="rs" d="M0,-178 L-10,-196 L10,-196 Z" fill="none" stroke-width="2"/><path class="rs" d="M0,178 L-10,196 L10,196 Z" fill="none" stroke-width="2"/>
       <path class="rs" d="M-178,0 L-196,-10 L-196,10 Z" fill="none" stroke-width="2"/><path class="rs" d="M178,0 L196,-10 L196,10 Z" fill="none" stroke-width="2"/></g>
  </svg></div>
</div>
<div class="px" id="pxL"><div id="lc"><div id="lci">
  <div id="hr"><svg width="300" height="300" viewBox="-150 -150 300 300">
      <g class="rot" id="hrT" stroke="rgba(111,227,255,.55)" stroke-width="2">{ticks}</g>
      {ring(112, "rs dim", "", 10)}
      <circle id="hrArc" cx="0" cy="0" r="112" fill="none" stroke="#6fe3ff" stroke-width="10" stroke-linecap="round" stroke-dasharray="703.7" stroke-dashoffset="703.7" transform="rotate(-90)"/>
    </svg>
    <div class="c g he"><span class="k">דופק</span><span class="v num" id="bpm">72</span><span class="u">פעימות לדקה</span></div></div>
  <div class="mini">
    <div class="mg"><svg width="120" height="120" viewBox="-60 -60 120 120">{ring(50, "rs dim", "", 6)}<circle id="o2Arc" cx="0" cy="0" r="50" fill="none" stroke="#6fe3ff" stroke-width="6" stroke-dasharray="314" stroke-dashoffset="314" transform="rotate(-90)"/></svg>
      <div class="c g he"><span class="v num">98%</span><span class="k">חמצן</span></div></div>
    <div class="mg"><svg width="120" height="120" viewBox="-60 -60 120 120">{ring(50, "rs dim", "", 6)}<circle id="suArc" cx="0" cy="0" r="50" fill="none" stroke="#6fe3ff" stroke-width="6" stroke-dasharray="314" stroke-dashoffset="314" transform="rotate(-90)"/></svg>
      <div class="c g he"><span class="v num">100%</span><span class="k">חליפה</span></div></div>
  </div>
</div></div></div>
<div class="px" id="pxR">
  <div id="rc"><div id="rci"><div class="frame g he" id="msg"><span class="h">הודעה נכנסת · מפקדה</span>
    <span class="l" id="m1"></span><span class="l" id="m2"></span><span class="l" id="m3"></span></div></div></div>
  <div id="warn"><div id="wi" style="transform:rotateY(-24deg);transform-origin:100% 50%"><div class="frame he">
    <span class="t">⚠ אזהרה · 2 עוינים</span><span class="s">רחפן אחד · טווח <span class="num">140</span> מ׳ · כיוון <span class="num">072°</span></span></div></div></div>
  <div id="meters">{''.join('<i></i>' for _ in range(7))}</div>
</div>
<div id="rad"><div id="sweep"></div><svg width="230" height="230" viewBox="-115 -115 230 230">{ring(110, "rs dim", "", 1)}{ring(75, "rs dim", "", 1)}{ring(40, "rs dim", "", 1)}
  <line x1="-110" y1="0" x2="110" y2="0" stroke="rgba(111,227,255,.3)"/><line x1="0" y1="-110" x2="0" y2="110" stroke="rgba(111,227,255,.3)"/></svg>
  <div class="blip" id="bl1" style="left:170px;top:70px"></div><div class="blip" id="bl2" style="left:185px;top:105px"></div><div class="blip a" id="bl3" style="left:150px;top:50px"></div>
  <div id="radl" class="g he">מכ״ם · <span class="num" id="radc">0</span> מגעים</div></div>
<div id="cmp" class="g"><div id="tape" class="num"></div></div><div id="cmpn" class="g he">כיוון <span class="num" id="hdg">072°</span></div>
<div id="data" class="g num"></div>
<div id="bootm" class="ctr g he"><span class="t">מערכת ואנגארד מופעלת</span><span class="s">סנכרון עצבי <span class="num" id="sync">0%</span> · <span id="allok"></span></span></div>
<div id="ai" class="ctr g he"><span class="k">עוזר החליפה</span><span class="q" id="aiq"></span></div>
<div id="lockm" class="ctr he"><span class="t" id="lockt">נעילת מטרה</span><span class="p num" id="lockp">0%</span></div>
<div id="wpn" class="ctr g he"><span class="q">מערכת הנשק זמינה. לאשר?</span><span class="ok" id="wok"></span></div>
<div id="go" class="ctr g he">יוצאים לדרך</div>
"""
    js = r"""
const $$ = (id) => document.getElementById(id);
const txt = (id, s) => { const e = $$(id); if (e.textContent !== s) e.textContent = s; };
const type = (id, full, t0, t, cps) => { const n = Math.max(0, Math.min(full.length, Math.floor((t - t0) * cps))); txt(id, [...full].slice(0, n).join("")); };
const lerp = (a, b, u) => a + (b - a) * Math.max(0, Math.min(1, u));
const tape = $$("tape"); let th = ""; for (let d = 0; d < 720; d += 15) th += `<span>${String(d % 360).padStart(3, "0")}</span>`; tape.innerHTML = th;
const HEX = "0123456789ABCDEF";
const hash = (n) => { let x = Math.sin(n * 12.9898) * 43758.5453; return x - Math.floor(x); };
const METERS = [...document.querySelectorAll("#meters i")];
window.onPlace = (t) => {
  const e = boxAt("eyes", t), f = boxAt("face", t);
  const ex = e ? (e[0] + e[2]) / 2 : 960, ey = e ? (e[1] + e[3]) / 2 : 480;
  const rel = (e && f) ? ((ex - (f[0] + f[2]) / 2) / (f[2] - f[0])) : 0;
  $$("ret").style.left = ex + "px"; $$("ret").style.top = ey + "px";
  $$("boot").style.left = ex + "px"; $$("boot").style.top = ey + "px";
  $$("pxL").style.transform = `translateX(${-rel * 40}px)`; $$("pxR").style.transform = `translateX(${-rel * 40}px)`;
  const lock = t > 18 && t < 21.2, warn = t > 11 && t < 15;
  const sp = lock ? 3 : 1;
  $$("rA").style.transform = `rotate(${t * 18 * sp}deg)`;
  $$("rB").style.transform = `rotate(${-t * 34 * sp}deg)`;
  $$("rC").style.transform = `rotate(${t * 60 * sp}deg)`;
  const conv = lock ? lerp(1.35, .82, (t - 18.2) / 1.8) : 1;
  $$("tri").style.transform = `scale(${conv}) rotate(${lock ? (t - 18) * 90 : 0}deg)`;
  $$("ret").classList.toggle("red", lock || warn);
  $$("vig").classList.toggle("red", warn);
  $$("hrT").style.transform = `rotate(${t * 12}deg)`;
  const bpm = t < 11 ? 72 : t < 15 ? lerp(72, 118, (t - 11) / 4) : t < 18 ? lerp(118, 94, (t - 15) / 3) : t < 21 ? 94 : lerp(94, 102, (t - 21) / 2);
  txt("bpm", String(Math.round(bpm)));
  $$("hrArc").style.strokeDashoffset = 703.7 * (1 - Math.min(1, (t > 4.2 ? lerp(0, 1, (t - 4.2) / .8) : 0) * bpm / 140));
  $$("o2Arc").style.strokeDashoffset = 314 * (1 - lerp(0, .98, (t - 4.6) / .8));
  $$("suArc").style.strokeDashoffset = 314 * (1 - lerp(0, 1, (t - 4.8) / .8));
  $$("sweep").style.transform = `rotate(${t * 140}deg)`;
  txt("radc", t > 11 ? "3" : "0");
  const hdg = 72 + rel * 90;
  tape.style.transform = `translateX(${-(hdg / 15) * 80 + 340}px)`;
  txt("hdg", String(Math.round((hdg + 360) % 360)).padStart(3, "0") + "°");
  const k = Math.floor(t * 10); let row = "";
  for (let i = 0; i < 38; i++) row += HEX[Math.floor(hash(k * 41 + i) * 16)] + (i % 4 === 3 ? " " : "");
  txt("data", "VNG-OS  " + row + " SYNC " + String(Math.round(lerp(0, 99, (t - .6) / 1.8))).padStart(2, "0"));
  METERS.forEach((m, i) => { m.style.height = (40 + 170 * (.5 + .5 * Math.sin(t * (2 + i * .7) + i))) + "px"; });
  txt("sync", Math.round(lerp(0, 99, (t - .6) / 1.8)) + "%");
  txt("allok", t > 2.7 ? "כל המערכות תקינות" : "");
  type("m1", "ואנגארד, כאן מפקדה.", 7.5, t, 16);
  type("m2", "זוהתה תנועה חשודה בגזרה 07.", 8.8, t, 16);
  type("m3", "המשך בזהירות.", 10.3, t, 16);
  type("aiq", "נשום עמוק. אני איתך.", 15.4, t, 13);
  const lk = Math.max(0, Math.min(1, (t - 18.3) / 2.1));
  txt("lockp", Math.round(lk * 100) + "%");
  txt("lockt", lk >= 1 ? "המטרה ננעלה" : "נעילת מטרה");
  txt("wok", t > 22.3 ? "✓ מאושר" : "");
};
function glitch(sel, at, dur = .3) {
  tl.fromTo(sel, {opacity: 0, skewX: -16, x: -24, clipPath: "inset(46% 0 46% 0)"},
                 {opacity: 1, skewX: 0, x: 0, clipPath: "inset(0% 0 0% 0)", duration: dur, ease: "expo.out"}, at);
  tl.to(sel, {keyframes: [{opacity: .25, duration: .04}, {opacity: 1, duration: .04}, {opacity: .55, duration: .03}, {opacity: 1, duration: .05}]}, at + dur);
}
const outAt = (sel, at) => tl.to(sel, {opacity: 0, duration: .25, ease: "power2.in"}, at);
tl.set(["#ret", "#lc", "#rc", "#warn", "#rad", "#cmp", "#cmpn", "#data", "#meters", "#bootm", "#ai", "#lockm", "#wpn", "#go", ".blip"], {opacity: 0}, 0);
tl.fromTo("#scan", {opacity: 0}, {opacity: 1, duration: .6}, .05);
tl.fromTo("#vig", {opacity: 0}, {opacity: 1, duration: .8}, .05);
tl.fromTo("#bootring", {strokeDashoffset: 2640}, {strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut"}, .15);
tl.to("#boot", {opacity: 0, duration: .4}, 1.35);
glitch("#bootm", .5, .35); outAt("#bootm", 3.85);
tl.fromTo("#ret", {opacity: 0, scale: 1.6}, {opacity: 1, scale: 1, duration: .6, ease: "expo.out"}, 1.1);
glitch("#cmp", 1.4); glitch("#cmpn", 1.5);
glitch("#data", 1.8); glitch("#meters", 2.0);
glitch("#lc", 4.1, .4);
glitch("#rad", 5.2, .35);
glitch("#rc", 7.0, .35); outAt("#rc", 10.9);
tl.to(".blip", {opacity: 1, duration: .05, stagger: .12}, 11.0);
tl.to(".blip", {scale: 1.6, duration: .25, repeat: 7, yoyo: true, ease: "sine.inOut"}, 11.1);
glitch("#warn", 11.0, .25); tl.to("#warn", {opacity: .45, duration: .15, repeat: 9, yoyo: true, ease: "none"}, 11.4); outAt("#warn", 15.0);
glitch("#ai", 15.2, .35); outAt("#ai", 17.9);
glitch("#lockm", 18.15, .25); outAt("#lockm", 21.0);
glitch("#wpn", 21.1, .35);
outAt(["#wpn", "#lc", "#rad", "#meters", "#data"], 23.0);
glitch("#go", 23.1, .4);
"""
    ticks_sfx = [cue("ui_tick", x, .3) for x in (7.5, 8.8, 10.3)]
    sfx = [cue("hud_boot", .1, .7), cue("data_chatter", .6, .25), cue("chime", 2.7, .4), cue("ui_whoosh", 4.05, .4),
           cue("scan_beeps", 5.2, .25), cue("ui_pop", 7.0, .5), *ticks_sfx, cue("warn_beep", 11.0, .75),
           cue("warn_beep", 12.2, .5), cue("heartbeat", 11.0, .5), cue("glass_ting", 15.3, .5), cue("lock_tone", 18.2, .55),
           cue("hit_confirm", 20.4, .65), cue("charge_up", 21.1, .65), cue("hit_confirm", 22.3, .55), cue("stinger", 23.05, .7)]
    return dict(project=R / "videos/b4x-helmet-holo", clip=R / "B_scifi/clips/B4_helmet_long_720p.mp4",
                track=R / "tools/B4_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.7)


def B4V():
    """B4X + 'Ora' suit-AI voice (Gemini TTS designed voice), HUD voice indicator driven by the real voice envelope."""
    import json as _json
    cfg = B4X()
    env = _json.loads((R / "B_scifi/voice/ora_b4_env.json").read_text())
    cfg["css"] += r"""
#vox{position:absolute;right:70px;bottom:64px;width:330px;padding:12px 18px;background:var(--bk);border-right:3px solid var(--cy)}
#vox .k{display:block;font-size:22px;font-weight:700;color:var(--cy)}
#vox .w{display:flex;align-items:center;gap:5px;height:56px;margin-top:6px;direction:ltr}
#vox .w b{display:block;width:6px;border-radius:3px;background:var(--cy);box-shadow:0 0 8px rgba(111,227,255,.8)}
"""
    cfg["hud"] += '<div id="vox" class="g he"><span class="k">אורה · ערוץ קולי</span><div class="w">' + "<b></b>" * 26 + "</div></div>"
    cfg["js"] = cfg["js"].replace("window.onPlace = (t) => {", "const ENV = " + _json.dumps(env) + ";\nconst VB = [...document.querySelectorAll('#vox .w b')];\nwindow.onPlace = (t) => {\n  const ev = ENV[Math.max(0, Math.min(ENV.length - 1, Math.round(t * 24)))] || 0;\n  VB.forEach((b, i) => { const sh = .35 + .65 * Math.abs(Math.sin(i * 1.7 + t * 7)); b.style.height = (4 + 50 * ev * sh) + 'px'; });", 1)
    cfg["js"] += '\nglitch("#vox", .15, .3);\n'
    # voice on top, HUD sfx ducked under it
    cfg["sfx"] = [("ora_b4_voice", "voice", 25, 0.0, 1.0)] + [(n, p, s, at, round(v * .6, 2)) for (n, p, s, at, v) in cfg["sfx"]]
    cfg["plate_vol"] = .45
    cfg["project"] = R / "videos/b4v-helmet-voice"
    return cfg


# ---------------------------------------------------------------- E1 soccer "The Strike" (fictional brand VANTA STRIKE)
# Cuts measured with ffmpeg scene detection: 2.54s (run-up -> macro), 7.75s (-> ball flight), 11.125s (-> goal wide)
def E1():
    fonts = '@font-face{font-family:"Anton";font-weight:400;src:url(assets/fonts/anton-latin-400.woff2) format("woff2")}'
    fonts += "".join(f'@font-face{{font-family:"Archivo";font-weight:{w};src:url(assets/fonts/archivo-latin-{w}.woff2) format("woff2")}}' for w in (400, 500, 600, 700))
    css = fonts + r"""
:root{--w:#ffffff;--red:#E63B2E;--k:#0b0b0d;--panel:rgba(11,11,13,.82)}
#root{font-family:"Archivo","Assistant",sans-serif}
.an{font-family:"Anton",sans-serif}
#stage,#stage2{position:absolute;inset:0}
#flash{position:absolute;inset:0;background:#fff;opacity:0}
#brand{position:absolute;left:84px;top:64px;display:flex;align-items:center;gap:12px}
#brand .b{font-family:"Anton",sans-serif;font-size:40px;letter-spacing:.06em;color:var(--w);background:var(--k);padding:2px 16px}
#brand .s{font-family:"JetBrains Mono",monospace;font-size:18px;letter-spacing:.14em;color:var(--k);background:var(--red);padding:6px 10px}
#pbox .brk i{border-color:var(--red)}
#ptag{padding:10px 16px;background:var(--panel);border-left:4px solid var(--red);white-space:nowrap}
#ptag .n{display:block;font-family:"Anton",sans-serif;font-size:34px;color:var(--w)}
#ptag .s{display:block;font-family:"JetBrains Mono",monospace;font-size:18px;color:#ffd2cf}
.big{position:absolute;left:0;top:0;width:0;height:0}
.big span{position:absolute;left:0;top:0;white-space:nowrap;font-family:"Anton",sans-serif;color:var(--w);text-shadow:8px 8px 0 var(--red)}
#ms span{font-size:300px;transform:translate(0,-50%)}
#ms small{position:absolute;left:8px;top:150px;white-space:nowrap;font-family:"JetBrains Mono",monospace;font-size:26px;letter-spacing:.14em;color:var(--w);background:var(--k);padding:6px 12px}
#lines{position:absolute;inset:0;width:1920px;height:1080px}
.co{position:absolute;padding:12px 18px;background:var(--panel);border-top:3px solid var(--red);white-space:nowrap}
.co .t{display:block;font-family:"Anton",sans-serif;font-size:36px;color:var(--w)}
.co .s{display:block;font-family:"JetBrains Mono",monospace;font-size:18px;color:#ffd2cf;margin-top:2px}
#co1{left:1260px;top:130px}#co2{left:1260px;top:330px}
#ring{position:absolute;left:0;top:0;width:0;height:0}
#ring svg{position:absolute;left:-260px;top:-260px}
#ringl{position:absolute;left:0;top:0;width:0;height:0}
#ringl span{position:absolute;left:0;top:0;white-space:nowrap;font-family:"JetBrains Mono",monospace;font-size:24px;color:var(--w);background:var(--k);padding:6px 12px}
#spd{position:absolute;left:96px;bottom:90px}
#spd .v{display:block;font-family:"Anton",sans-serif;font-size:220px;line-height:1.15;margin-bottom:22px;color:var(--w);text-shadow:8px 8px 0 var(--red)}
#spd .u{display:block;font-family:"JetBrains Mono",monospace;font-size:26px;letter-spacing:.2em;color:var(--w);background:var(--k);padding:6px 12px;width:max-content}
#trail{position:absolute;inset:0;width:1920px;height:1080px}
#goal{position:absolute;left:0;right:0;top:60px;text-align:center}
#goal span{font-family:"Anton",sans-serif;font-size:680px;line-height:1;color:var(--red);-webkit-text-stroke:6px var(--k);text-shadow:14px 14px 0 var(--k)}
#lock{position:absolute;left:0;right:0;margin:0 auto;bottom:70px;width:max-content;display:flex;align-items:center;gap:20px}
#lock .b{font-family:"Anton",sans-serif;font-size:76px;color:var(--w);background:var(--k);padding:0 24px}
#lock .s{font-family:"Anton",sans-serif;font-size:48px;color:var(--k);background:var(--red);padding:4px 20px}
"""
    ring = ('<svg width="520" height="520" viewBox="-260 -260 520 520">'
            '<g id="rg1"><circle r="200" fill="none" stroke="#ffffff" stroke-width="4" stroke-dasharray="40 22"/></g>'
            '<g id="rg2"><circle r="232" fill="none" stroke="#E63B2E" stroke-width="3" stroke-dasharray="6 14"/></g></svg>')
    hud = f"""
<div id="stage"><div id="goal"><span data-layout-allow-overlap data-layout-allow-occlusion>GOAL</span></div></div>
<!--MATTE-->
<div id="stage2">
<svg id="trail" viewBox="0 0 1920 1080"><polyline id="tr" fill="none" stroke="#E63B2E" stroke-width="10" stroke-linecap="round" stroke-linejoin="round" points=""/></svg>
<svg id="lines" viewBox="0 0 1920 1080"><path id="l1" fill="none" stroke="#fff" stroke-width="3"/><path id="l2" fill="none" stroke="#fff" stroke-width="3"/>
  <circle id="d1" r="10" fill="#E63B2E" stroke="#fff" stroke-width="3" cx="-50" cy="-50"/><circle id="d2" r="10" fill="#E63B2E" stroke="#fff" stroke-width="3" cx="-50" cy="-50"/></svg>
<div id="pbox" data-box="player" data-pad="16">{BRK}</div>
<div id="ptag" data-follow="player" data-anchor="r" data-dx="26" data-dy="-120"><span class="n">THE STRIKER</span><span class="s">RUN-UP 31 KM/H</span></div>
<div class="big" id="ms" style="left:90px;top:520px"><span data-layout-allow-overlap>9 MS</span><small>CONTACT TIME</small></div>
<div class="co" id="co1"><span class="t">CARBON STRIKE PLATE</span><span class="s">+14% energy return</span></div>
<div class="co" id="co2"><span class="t">3D GRIP ZONE</span><span class="s">spin control on contact</span></div>
<div id="ring" data-follow="ball" data-anchor="c">{ring}</div>
<div id="ringl" data-follow="ball" data-anchor="t" data-dy="-60"><span id="rl" style="transform:translateX(-50%)">BALL COMPRESSION 18%</span></div>
<div id="spd"><span class="v" id="kmh">0</span><span class="u">KM/H · SPIN 9.8 RPS</span></div>
<div id="brand"><span class="b">GUYAGA STRIKE</span><span class="s">FG · 2026</span></div>
<div id="lock"><span class="b">GUYAGA STRIKE</span><span class="s">MAKE IT COUNT</span></div>
</div>
<div id="flash"></div>
"""
    js = r"""
const C1 = 2.54, C2 = 7.75, C3 = 11.125;
const hist = [];
window.onPlace = (t) => {
  const bt = boxAt("boot", t), bl = boxAt("ball", t);
  const inMacro = t >= C1 && t < C2;
  const link = (lid, did, from, to) => {
    const l = document.getElementById(lid), d = document.getElementById(did);
    if (!from || !inMacro) { l.setAttribute("d", ""); d.setAttribute("cx", -50); return; }
    l.setAttribute("d", `M${from[0]},${from[1]} L${to[0] - 40},${to[1]} L${to[0]},${to[1]}`);
    d.setAttribute("cx", from[0]); d.setAttribute("cy", from[1]);
  };
  const bootPt = bt ? [(bt[0] + bt[2]) / 2, bt[1] + (bt[3] - bt[1]) * .45] : null;
  const gripPt = bt ? [bt[2] - (bt[2] - bt[0]) * .2, bt[1] + (bt[3] - bt[1]) * .7] : null;
  link("l1", "d1", t > 4.2 ? bootPt : null, [1260, 175]);
  link("l2", "d2", t > 5.0 ? gripPt : null, [1260, 375]);
  const r = t < C2 ? 0 : t < C3 ? (t - C2) * 60 : 0;
  document.getElementById("rg1").setAttribute("transform", `rotate(${t * 220})`);
  document.getElementById("rg2").setAttribute("transform", `rotate(${-t * 140})`);
  document.getElementById("rl").textContent = t < C2 ? "BALL COMPRESSION 18%" : "SPIN 9.8 RPS";
  const u = Math.max(0, Math.min(1, (t - C2 - .15) / 1.6));
  document.getElementById("kmh").textContent = String(Math.round(121 * (1 - Math.pow(1 - u, 3))));
  // ball trail during flight: deterministic from track history
  if (t >= C2 && t < C3 && bl) {
    let pts = []; for (let s = Math.max(C2, t - .9); s <= t; s += 1 / 24) { const b = boxAt("ball", s); if (b) pts.push([(b[0] + b[2]) / 2, (b[1] + b[3]) / 2]); }
    document.getElementById("tr").setAttribute("points", pts.map(p => p.join(",")).join(" "));
  } else document.getElementById("tr").setAttribute("points", "");
};
function shake(at, amt = 1) {
  tl.to(["#stage", "#stage2"], {keyframes: [{x: -14 * amt, y: 6 * amt, duration: .04}, {x: 11 * amt, y: -5 * amt, duration: .04}, {x: -6 * amt, y: 3 * amt, duration: .04}, {x: 0, y: 0, duration: .06}], ease: "none"}, at);
  tl.fromTo("#flash", {opacity: .45 * amt}, {opacity: 0, duration: .14}, at);
}
function stomp(sel, at, from = 1.9) { tl.fromTo(sel, {opacity: 0, scale: from}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, at); shake(at); }
tl.set(["#ms", "#co1", "#co2", "#ring", "#ringl", "#spd", "#goal", "#lock", "#pbox", "#ptag"], {opacity: 0}, 0);
// shot 1 run-up
tl.fromTo("#brand", {opacity: 0, x: -20}, {opacity: 1, x: 0, duration: .3}, .15);
tl.to(["#pbox", "#ptag"], {opacity: 1, duration: .01}, .5);
tl.fromTo("#pbox .brk", {scale: 1.4}, {scale: 1, duration: .3, ease: "power3.out"}, .5);
tl.fromTo("#ptag", {x: -16}, {x: 0, duration: .3, ease: "power3.out"}, .6);
tl.to(["#pbox", "#ptag"], {opacity: 0, duration: .05}, C1 - .05);
// shot 2 macro contact
tl.to("#ms", {opacity: 1, duration: .01}, C1 + .15);
stomp("#ms span", C1 + .2, 2.2);
tl.fromTo("#ms small", {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: .2}, C1 + .45);
tl.to(["#ring", "#ringl"], {opacity: 1, duration: .01}, 3.6);
tl.fromTo("#ring svg", {scale: 1.5, opacity: 0}, {scale: 1, opacity: 1, duration: .3, ease: "power3.out"}, 3.6);
tl.to("#co1", {opacity: 1, duration: .01}, 4.3); tl.fromTo("#co1", {x: 30}, {x: 0, duration: .25, ease: "power3.out"}, 4.3);
tl.to("#co2", {opacity: 1, duration: .01}, 5.1); tl.fromTo("#co2", {x: 30}, {x: 0, duration: .25, ease: "power3.out"}, 5.1);
tl.to(["#ms", "#co1", "#co2", "#ringl"], {opacity: 0, duration: .08}, C2 - .08);
// shot 3 ball flight
tl.to("#spd", {opacity: 1, duration: .01}, C2 + .1);
stomp("#spd", C2 + .12, 1.8);
tl.to(["#spd", "#ring"], {opacity: 0, duration: .08}, C3 - .08);
// shot 4 goal
tl.to("#goal", {opacity: 1, duration: .01}, C3 + .25);
stomp("#goal span", C3 + .28, 2.4);
tl.to("#brand", {opacity: 0, duration: .2}, C3);
tl.to("#lock", {opacity: 1, duration: .01}, 13.0);
stomp("#lock", 13.02, 1.6);
"""
    sfx = [("E1_music", "music", 16, 0.0, .55), ("E1_vo", "vo", 16, 0.0, 1.0)]
    st = ("soft_thump", "Deep soft round sub thump, clean and warm, subtle impact, no whoosh, no noise, no distortion", 0.6)
    sfx += [(*st, h, .5) for h in (2.72, 7.85, 11.39, 13.0)]
    sfx += [cue("ui_pop", 4.3, .35), cue("ui_pop", 5.1, .35), cue("ui_whoosh", 3.55, .3)]
    extra = {}
    for pat in ("anton-*.woff2", "archivo-*.woff2"):
        for f in (R / "shared/fonts").glob(pat):
            extra[f"fonts/{f.name}"] = f
    extra["matte.webm"] = R / "E_ads/matte/E1_alpha.webm"
    return dict(extra=extra, project=R / "videos/e1-soccer", clip=R / "E_ads/clips/E1_soccer_720p.mp4",
                track=R / "tools/E1_vtrack.json", css=css, hud=hud, js=js, sfx=sfx, plate_vol=.4)


SHOTS = {"E1": E1, "A2": A2, "B1": B1, "B2": B2, "B3": B3, "C1": C1, "C2": C2, "C3": C3, "B4": B4, "D1": D1, "D1S": D1S,
         "D1G": D1G, "D1B": D1B, "D2": D2, "B4X": B4X, "B4V": B4V, "D3": D3}

if __name__ == "__main__":
    for k in sys.argv[1:]:
        cfg = SHOTS[k]()
        shotkit.build(k, **cfg)
        r = subprocess.run("npx hyperframes check", cwd=cfg["project"], shell=True, capture_output=True, text=True)
        bad = [ln for ln in (r.stdout + r.stderr).splitlines() if "✗" in ln or "Check" in ln]
        print(f"[{k}] " + " | ".join(bad[:8]))
