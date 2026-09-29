"""E4_fire BESPOKE - FIRELINK seen through a thermal imaging camera (TIC) + SCBA instruments.

Visual language (only this ad): the frame IS the TIC viewfinder. Luminance -> steel blue-grey, only the hottest
tones (fire, heat signatures) go amber -> white (SVG table map on the plate); ironbow IRON strip, PASS strobe,
crew PAR tag, range-ticked crosshair, scanlines, centre reticle with spot temperature, vertical heat scale,
a round SCBA pressure-gauge dial (oxygen 100 -> 7 %) and a live ECG line; everything pulses on the heartbeat.
ORA speaks as single-line amber OSD text (monospaced Plex Hebrew cells, 1px black outline) under the REC bar; 'אדם אחד' is a white-hot
thermal image of the words on cold blue. At the rescue exit the camera switches off: a calm white bloom, natural colour, the heartbeat slows, UI turns white; ends on a helmet-shield decal.
"""
import json
import math
from pathlib import Path

T = Path(__file__).resolve().parent.parent
_hk = {"__file__": str(T / "specs" / "E4_fire_hk.py")}
exec((T / "specs" / "E4_fire_hk.py").read_text(encoding="utf-8"), _hk)
HK = _hk["SPEC"]

# ---- timing ------------------------------------------------------------------------------------
CUT_TIC, CUT_DOOR, BLACK0, CUT_CHILD, CUT_EXIT, END = 3.667, 9.875, 12.45, 13.875, 17.04, 20.04
P1, T0 = 0.52, 0.03                     # tense heartbeat (~115 bpm), grid lands on the TIC cut
beats = [round(T0 + k * P1, 3) for k in range(0, 60) if T0 + k * P1 < CUT_EXIT - .05]
beats += [round(CUT_EXIT + k * 0.95, 3) for k in range(0, 4)]   # calm (~63 bpm)


def near(t):
    return min(beats, key=lambda b: abs(b - t))


THUMPS = sorted({near(3.667), near(10.1), near(12.35), near(12.9), near(13.4), near(14.2), near(17.04)})

# ---- gauge geometry ------------------------------------------------------------------------------
R = 118


def pol(deg, r):
    a = math.radians(deg - 90)
    return r * math.cos(a), r * math.sin(a)


def arc(d0, d1, r):
    x0, y0 = pol(d0, r)
    x1, y1 = pol(d1, r)
    big = 1 if d1 - d0 > 180 else 0
    return f"M{x0:.1f},{y0:.1f} A{r},{r} 0 {big} 1 {x1:.1f},{y1:.1f}"


ticks = ""
for v in range(0, 101, 5):
    d = -135 + 270 * v / 100
    x0, y0 = pol(d, R - (18 if v % 10 == 0 else 10))
    x1, y1 = pol(d, R)
    ticks += f'<line x1="{x0:.1f}" y1="{y0:.1f}" x2="{x1:.1f}" y2="{y1:.1f}" stroke-width="{3 if v % 10 == 0 else 1.5}"/>'
nums = ""
for v in (25, 50, 75):
    d = -135 + 270 * v / 100
    x, y = pol(d, R - 36)
    nums += f'<text x="{x:.1f}" y="{y + 6:.1f}" text-anchor="middle">{v}</text>'

GAUGE = f'''<div id="gz"><svg viewBox="-150 -150 300 300" width="300" height="300">
<circle r="146" class="gz-bez"/><circle r="134" class="gz-face"/>
<path d="{arc(-135, 135, R + 8)}" class="gz-trk"/>
<path d="{arc(-135, -135 + 270 * .3, R + 8)}" class="gz-red"/>
<path id="gzArc" d="{arc(-135, 135, R + 8)}" class="gz-val" pathLength="100"/>
<g class="gz-tk">{ticks}</g><g class="gz-num">{nums}</g>
<text y="-38" text-anchor="middle" class="gz-o2">O₂</text>
<g id="gzN"><path d="M-5,14 L0,-{R - 6} L5,14 Z" class="gz-ndl"/></g><circle r="13" class="gz-hub"/>
<text id="gzV" y="62" text-anchor="middle" class="gz-v">100%</text>
<text id="gzB" y="88" text-anchor="middle" class="gz-b">300 BAR</text>
</svg><div class="gz-l">חמצן במיכל</div></div>'''

# thermal colour scale (same stops as the plate gradient map)
# ironbow palette strip (the camera's palette indicator)
TSTOPS = "#ffffff 0%,#fff3a6 9%,#ffc53a 22%,#ff7a1a 36%,#e0302c 50%,#9a1f6e 63%,#4a1f86 76%,#1b1a4a 89%,#05060c 100%"


def _cross():
    pts = [(-11, -20), (-46, -100), (0, -80), (46, -100), (11, -20)]
    out = []
    for k in range(4):
        a = math.radians(90 * k)
        for x, y in pts:
            out.append(f"{x * math.cos(a) - y * math.sin(a):.1f},{x * math.sin(a) + y * math.cos(a):.1f}")
    return "M" + " L".join(out) + " Z"


SHIELD = f'''<div id="shield"><svg viewBox="0 0 420 500" width="420" height="500">
<defs><path id="shArc" d="M78,196 C112,84 308,84 342,196"/>
<linearGradient id="shG" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#2a211c"/><stop offset="1" stop-color="#0d0a09"/></linearGradient>
<linearGradient id="goldG" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#f7dc8a"/><stop offset=".5" stop-color="#c9922e"/><stop offset="1" stop-color="#f0cf78"/></linearGradient></defs>
<path d="M210,8 C300,8 392,52 404,150 L404,300 C404,392 318,458 210,492 C102,458 16,392 16,300 L16,150 C28,52 120,8 210,8 Z" fill="url(#shG)" stroke="url(#goldG)" stroke-width="10"/>
<path d="M210,30 C290,30 372,68 382,154 L382,298 C382,378 304,436 210,468 C116,436 38,378 38,298 L38,154 C48,68 130,30 210,30 Z" fill="none" stroke="#c9922e" stroke-width="2" stroke-dasharray="6 5" opacity=".8"/>
<text class="sh-arc"><textPath href="#shArc" startOffset="50%" text-anchor="middle">FIRELINK</textPath></text>
<g transform="translate(210,272)"><path d="{_cross()}" fill="#b3201c" stroke="url(#goldG)" stroke-width="5"/>
<circle r="44" fill="#0d0a09" stroke="url(#goldG)" stroke-width="4"/><text y="22" text-anchor="middle" class="sh-n">3</text></g>
</svg><div class="sh-rib"><span>לראות דרך העשן</span></div></div>'''

HTML = f'''
<svg width="0" height="0" style="position:absolute"><defs>
<filter id="th" color-interpolation-filters="sRGB" x="0" y="0" width="100%" height="100%">
<feColorMatrix type="matrix" values=".30 .59 .11 0 0 .30 .59 .11 0 0 .30 .59 .11 0 0 0 0 0 1 0"/>
<feComponentTransfer>
<feFuncR type="table" tableValues=".05 .08 .11 .15 .20 .26 .33 .52 .94 1 1"/>
<feFuncG type="table" tableValues=".07 .11 .15 .20 .26 .33 .40 .38 .60 .90 1"/>
<feFuncB type="table" tableValues=".10 .15 .21 .28 .36 .44 .52 .30 .12 .52 1"/>
</feComponentTransfer></filter></defs></svg>
<div id="tic" class="hot">
  <div id="vig"></div><div id="cold"></div><div id="topfade"></div>
  <div id="blobDoor" class="blob"></div><div id="blobKid" class="blob"></div>
  <div id="scan"></div><div id="band"></div>
  <div id="bez"><i class="c1"></i><i class="c2"></i><i class="c3"></i><i class="c4"></i></div>
  <div id="topL" class="mono">FIRELINK<b>TIC</b><span id="mode">IRON · 1×</span></div>
  <div id="topR"><span class="rec"></span><span class="mono">REC</span><span class="mono" id="clock">00:00:00</span></div>
  <div id="link" class="mono"><span class="sig"><i></i><i></i><i></i><i></i></span>RX CH3<span class="o">ORA</span></div>
  <div id="boot" class="osdt"><div class="bt1">מצלמה תרמית · מאתחלת</div><div class="bt2"><i id="bootP"></i></div></div>
  <div id="crew" class="osdt"><span class="k mono">PAR</span><span id="crewT">צוות 3 · 2 בפנים</span></div>
  <div id="pass"><svg viewBox="0 0 70 46" width="70" height="46"><rect x="3" y="3" width="64" height="40" rx="9" class="pb"/>
    <circle id="pL1" cx="22" cy="23" r="8"/><circle id="pL2" cx="48" cy="23" r="8"/></svg>
    <div class="pt mono"><span>PASS</span><span id="passS">ARMED</span></div></div>
  <div id="scale"><div class="bar"></div><div class="lbs mono"><span>800</span><span>600</span><span>400</span><span>200</span><span>0</span></div>
    <div id="mark"></div><div class="u mono">IRON °C</div></div>
  <div id="ret"><svg viewBox="-130 -130 260 260" width="260" height="260">
    <circle r="54" class="r1"/><path d="M-110,0 H-66 M66,0 H110 M0,-110 V-66 M0,66 V110" class="r2"/>
    <path d="M74,-5 v10 M86,-9 v18 M98,-5 v10 M-74,-5 v10 M-86,-9 v18 M-98,-5 v10 M-5,74 h10 M-9,86 h18 M-5,98 h10 M-5,-74 h10 M-9,-86 h18 M-5,-98 h10" class="r5"/>
    <path d="M-18,-18 h10 M-18,-18 v10 M18,-18 h-10 M18,-18 v10 M-18,18 h10 M-18,18 v-10 M18,18 h-10 M18,18 v-10" class="r3"/>
    <circle r="3" class="r4"/></svg>
    <div id="spot" class="mono"><span class="k">SPOT</span><span id="spotV">---</span></div>
    <div id="dist" class="mono">RNG <span id="distV">--</span> m</div>
    <div id="lock" class="osdt">[ נמצאה · <span class="mono">36.8°C</span> ]</div>
  </div>
  <div id="doorTag" class="osdt tagx"><span class="k mono">HEAT · 37.1°C</span><span class="a">חתימת חום</span></div>
  <div id="chev"><i></i><i></i><i></i></div>
  {GAUGE}
  <div id="ecg"><div class="hd"><span class="mono" id="bpm">118</span><span class="k mono">BPM</span><span class="he">דופק</span></div>
    <svg viewBox="0 0 560 90" width="560" height="90"><path id="ecgP" d=""/><circle id="ecgD" r="5" cx="-20" cy="-20"/></svg></div>
  <div id="warn">חמצן נמוך</div>
  <div id="osd"><span class="px mono" id="osdP">RX›</span><span id="osdT"></span><span id="osdC"></span></div>
  <div id="m5"><div class="tw s" id="m5s">אדם אחד.</div></div>
  <div id="end"><div class="pc"><span class="n mono" id="pct">7%</span><span class="w">חמצן.</span></div><div class="ok" id="okw">מספיק.</div></div>
  {SHIELD}
  <div id="blk"></div><div id="bloom"></div>
</div>'''

OSDF = '"Plex He","JetBrains Mono",monospace'
OUTL = "1px 0 0 #000,-1px 0 0 #000,0 1px 0 #000,0 -1px 0 #000,1px 1px 0 #000,-1px -1px 0 #000,0 0 7px rgba(0,0,0,.9)"
CSS = '''
#tic{position:absolute;inset:0;--amb:#ffb21a;--hot:#ff4a1c;--ui:#e8eef5;--osd:rgba(6,5,5,.8);--ice:#eaf4ff}
#tic.calm{--amb:#ffffff;--hot:#ffffff;--ui:#ffffff}
#tic .mono{font-family:"JetBrains Mono",monospace;font-weight:700;letter-spacing:.06em}
.osdt{font-family:__OSDF__;font-weight:500;color:var(--amb);text-shadow:__OUTL__}
#vig{position:absolute;inset:0;background:radial-gradient(ellipse 72% 70% at 50% 50%,transparent 58%,rgba(0,0,0,.55) 100%)}
#topfade{position:absolute;left:0;right:0;top:0;height:230px;background:linear-gradient(180deg,rgba(0,0,0,.42),rgba(0,0,0,0))}
#cold{position:absolute;inset:0;opacity:0;background:radial-gradient(ellipse 60% 55% at 50% 48%,#2c5a8c 0%,#17325a 45%,#0a1428 100%)}
#scan{position:absolute;inset:0;background:repeating-linear-gradient(0deg,rgba(0,0,0,.22) 0 2px,transparent 2px 4px);mix-blend-mode:multiply;opacity:0}
#band{position:absolute;left:0;right:0;height:140px;top:-200px;background:linear-gradient(180deg,transparent,rgba(200,225,255,.06),transparent)}
.blob{position:absolute;left:0;top:0;width:10px;height:10px;border-radius:50%;opacity:0;mix-blend-mode:screen;
 background:radial-gradient(circle,rgba(255,255,255,.95) 0%,rgba(255,236,140,.85) 18%,rgba(255,168,26,.6) 38%,rgba(255,70,20,.28) 58%,transparent 72%)}
#bez{position:absolute;left:44px;top:44px;right:44px;bottom:44px;border:2px solid rgba(220,232,245,.22);border-radius:26px}
#bez i{position:absolute;width:56px;height:56px;border:0 solid var(--amb)}
#bez .c1{left:-2px;top:-2px;border-width:5px 0 0 5px;border-top-left-radius:26px}
#bez .c2{right:-2px;top:-2px;border-width:5px 5px 0 0;border-top-right-radius:26px}
#bez .c3{left:-2px;bottom:-2px;border-width:0 0 5px 5px;border-bottom-left-radius:26px}
#bez .c4{right:-2px;bottom:-2px;border-width:0 5px 5px 0;border-bottom-right-radius:26px}
#topL{position:absolute;left:84px;top:70px;display:flex;gap:14px;align-items:center;font-size:24px;color:var(--ui);text-shadow:0 1px 6px #000}
#topL b{background:var(--amb);color:#111;padding:2px 8px;font-weight:700}
#topL #mode{font-size:18px;opacity:.8;font-weight:500}
#topR{position:absolute;right:84px;top:70px;display:flex;gap:12px;align-items:center;font-size:22px;color:var(--ui);text-shadow:0 1px 6px #000}
.rec{width:14px;height:14px;border-radius:50%;background:var(--hot)}
#link{position:absolute;left:0;right:0;margin:0 auto;top:70px;width:max-content;display:flex;gap:12px;align-items:center;font-size:20px;color:var(--ui);text-shadow:__OUTL__}
#link .o{color:var(--amb)}
#link .sig{display:flex;gap:3px;align-items:flex-end;height:18px}#link .sig i{display:block;width:5px;background:var(--amb);outline:1px solid #000}
#link .sig i:nth-child(1){height:5px}#link .sig i:nth-child(2){height:9px}#link .sig i:nth-child(3){height:13px}#link .sig i:nth-child(4){height:18px}
#boot{position:absolute;left:84px;top:108px;direction:rtl;width:340px}
#boot .bt1{font-size:30px;line-height:1.2;text-align:right}
#boot .bt2{height:4px;background:rgba(255,255,255,.25);margin-top:6px;outline:1px solid #000}#boot .bt2 i{display:block;height:100%;background:var(--amb);width:0}
#crew{position:absolute;right:84px;top:106px;display:flex;gap:12px;align-items:baseline;direction:rtl;font-size:32px}
#crew .k{font-size:17px;color:var(--ui);direction:ltr}
#pass{position:absolute;left:84px;top:176px;display:flex;gap:10px;align-items:center}
#pass .pb{fill:rgba(10,12,16,.75);stroke:var(--ui);stroke-width:2}
#pass circle{fill:#2a2f36;stroke:#000;stroke-width:1.5}
#pass .pt{display:flex;flex-direction:column;font-size:16px;line-height:1.15;color:var(--ui);text-shadow:__OUTL__}
#pass #passS{color:#7dffb0}
#scale{position:absolute;right:84px;top:250px;width:90px;height:470px}
#scale .bar{position:absolute;right:0;top:0;width:22px;height:100%;background:linear-gradient(180deg,__TSTOPS__);border:1px solid rgba(255,255,255,.4)}
#scale .lbs{position:absolute;right:32px;top:-10px;height:calc(100% + 20px);display:flex;flex-direction:column;justify-content:space-between;
 font-size:17px;color:var(--ui);text-align:right;text-shadow:0 1px 4px #000}
#scale .u{position:absolute;right:0;top:-34px;font-size:18px;color:var(--ui);white-space:nowrap;text-shadow:0 1px 4px #000}
#mark{position:absolute;right:24px;top:0;width:0;height:0;border-top:10px solid transparent;border-bottom:10px solid transparent;border-right:16px solid var(--ui);transform:translateY(-10px)}
#ret{position:absolute;left:0;top:0;width:0;height:0}
#ret svg{position:absolute;left:-130px;top:-130px;overflow:visible}
#ret .r1{fill:none;stroke:var(--ui);stroke-width:2.5;stroke-dasharray:20 8;opacity:.9}
#ret .r2{stroke:var(--ui);stroke-width:2.5;opacity:.85}#ret .r5{stroke:var(--ui);stroke-width:2;opacity:.8}
#ret .r3{stroke:var(--amb);stroke-width:3;fill:none}#ret .r4{fill:var(--amb)}
#spot{position:absolute;left:72px;top:-92px;display:flex;flex-direction:column;color:var(--ui);white-space:nowrap;text-shadow:__OUTL__}
#spot .k{font-size:15px;opacity:.8}#spot #spotV{font-size:34px;color:var(--amb)}
#dist{position:absolute;left:18px;top:112px;font-size:17px;color:var(--ui);white-space:nowrap;text-shadow:__OUTL__}
#dist #distV{color:var(--amb);font-size:22px}
#lock{position:absolute;left:-200px;top:162px;width:400px;text-align:center;direction:rtl;font-size:40px;font-weight:700;opacity:0;white-space:nowrap}
#lock .mono{font-size:26px}
.tagx{position:absolute;left:0;top:0;display:flex;flex-direction:column;align-items:flex-end;direction:rtl;padding:2px 14px;opacity:0;border-right:3px solid var(--amb)}
.tagx .k{font-size:17px;color:var(--ui);direction:ltr}.tagx .a{font-size:46px;line-height:1.1;font-weight:700}
#chev{position:absolute;left:1380px;top:470px;display:flex;gap:6px;opacity:0}
#chev i{display:block;width:60px;height:110px;background:var(--amb);clip-path:polygon(0 0,45% 0,100% 50%,45% 100%,0 100%,55% 50%)}
#gz{position:absolute;left:78px;top:676px;width:300px;height:300px}
#gz svg{overflow:visible}
.gz-bez{fill:rgba(10,12,16,.82);stroke:rgba(230,238,248,.35);stroke-width:3}.gz-face{fill:none;stroke:rgba(255,255,255,.12);stroke-width:1}
.gz-trk{fill:none;stroke:rgba(255,255,255,.14);stroke-width:12}.gz-red{fill:none;stroke:#ff3a1c;stroke-width:12;opacity:.85}
.gz-val{fill:none;stroke:var(--amb);stroke-width:12;stroke-dasharray:100 100}
.gz-tk line{stroke:var(--ui)}.gz-num text{font:700 17px "JetBrains Mono",monospace;fill:var(--ui);opacity:.8}
.gz-o2{font:700 26px "JetBrains Mono",monospace;fill:var(--ui);opacity:.75}
.gz-ndl{fill:var(--hot);stroke:#000;stroke-width:1}.gz-hub{fill:#16161a;stroke:var(--ui);stroke-width:3}
.gz-v{font:700 44px "JetBrains Mono",monospace;fill:var(--ui)}.gz-b{font:500 17px "JetBrains Mono",monospace;fill:var(--ui);opacity:.7}
.gz-l{position:absolute;left:0;right:0;top:-44px;text-align:center;direction:rtl;font-family:"Karantina",sans-serif;font-weight:700;font-size:40px;color:var(--ui);text-shadow:0 2px 8px #000}
#ecg{position:absolute;left:1276px;top:860px;width:560px;background:rgba(8,10,14,.6);padding:8px 0 4px}
#ecg .hd{display:flex;align-items:baseline;gap:10px;padding:0 14px;color:var(--ui)}
#ecg #bpm{font-size:34px;color:var(--hot)}#ecg .k{font-size:15px;opacity:.7}#ecg .he{margin-left:auto;font-family:"Karantina",sans-serif;font-weight:700;font-size:34px;direction:rtl}
#ecgP{fill:none;stroke:var(--hot);stroke-width:3.5;stroke-linejoin:round}#ecgD{fill:#fff}
#warn{position:absolute;left:78px;top:556px;width:300px;text-align:center;direction:rtl;font-family:"Karantina",sans-serif;font-weight:700;font-size:50px;color:#fff;background:#d8241a;opacity:0}
#osd{position:absolute;left:0;right:0;top:112px;height:60px;display:flex;justify-content:center;align-items:center;gap:14px;direction:rtl;opacity:0}
#osd .px{font-size:20px;color:var(--ui);direction:ltr;text-shadow:__OUTL__}
#osdT{display:flex;direction:rtl}
#osdT i{display:block;font-style:normal;width:27px;text-align:center;font-size:46px;line-height:60px;font-family:__OSDF__;font-weight:500;color:var(--amb);text-shadow:__OUTL__}
#osdT i.sp{width:34px}
#osdC{display:block;width:16px;height:38px;background:var(--amb);outline:1px solid #000}
#m5{position:absolute;left:0;right:0;top:250px;height:400px;opacity:0}
#m5 .tw{position:absolute;left:0;right:0;top:0;text-align:center;direction:rtl;font-family:"Karantina",sans-serif;font-weight:700;font-size:300px;line-height:1.2;white-space:nowrap}
#m5 .s{background:radial-gradient(ellipse 50% 60% at 50% 55%,#ffffff 0%,#fffbe6 38%,#ffe27a 62%,#ffa21a 84%,#ff5a14 100%);-webkit-background-clip:text;background-clip:text;color:transparent;
 filter:drop-shadow(0 0 5px #ffe27a) drop-shadow(0 0 20px #ff8a1a) drop-shadow(0 0 56px rgba(255,74,20,.85))}
#end{position:absolute;left:430px;top:680px;direction:rtl;display:flex;flex-direction:column;align-items:flex-start;opacity:0}
#end .pc{display:flex;align-items:baseline;gap:18px;direction:rtl;color:#fff;background:rgba(8,10,14,.66);padding:0 24px;border-right:5px solid #fff}
#end .n{font-size:110px;font-weight:700;direction:ltr}#end .w{font-family:"Karantina",sans-serif;font-weight:700;font-size:100px}
#end .ok{font-family:"Karantina",sans-serif;font-weight:700;font-size:170px;line-height:1;color:#fff;text-shadow:0 6px 30px rgba(0,0,0,.6);margin-top:6px}
#shield{position:absolute;right:170px;top:96px;width:420px;height:500px;opacity:0;filter:drop-shadow(0 18px 30px rgba(0,0,0,.55))}
#shield svg{position:absolute;left:0;top:0}
.sh-arc{font:900 52px "Fraunces",serif;fill:url(#goldG);letter-spacing:.06em}
.sh-n{font:900 64px "Fraunces",serif;fill:#f7dc8a}
.sh-sm{font:700 15px "JetBrains Mono",monospace;fill:#c9922e;letter-spacing:.2em}
.sh-rib{position:absolute;left:30px;right:30px;top:382px;height:66px;background:#b3201c;border:3px solid #c9922e;
 clip-path:polygon(0 0,100% 0,94% 50%,100% 100%,0 100%,6% 50%);display:flex;align-items:center;justify-content:center}
.sh-rib span{font-family:"Rubik",sans-serif;font-weight:800;font-size:38px;color:#fff7e6;direction:rtl;line-height:1}
#bloom{position:absolute;inset:0;background:radial-gradient(circle at 50% 45%,#fff 0%,#fff 40%,rgba(235,244,255,.9) 100%);opacity:0}
#blk{position:absolute;inset:0;background:#000;opacity:0}
.kn{display:none!important}
'''.replace("__OSDF__", OSDF).replace("__OUTL__", OUTL).replace("__TSTOPS__", TSTOPS)

# ---- GSAP + per-frame -----------------------------------------------------------------------------
JS = r'''
const BEATS = __BEATS__;
const CUTS = {tic:__TIC__, door:__DOOR__, black:__BLACK__, child:__CHILD__, exit:__EXIT__};
const hsh = (n) => { const s = Math.sin(n * 12.9898) * 43758.5453; return s - Math.floor(s); };
function lastBeat(t){ let b = -9; for (const x of BEATS){ if (x <= t) b = x; else break; } return b; }
function ecgV(dt, p){ // one PQRST complex, dt seconds after the beat
  const g = (m, s, a) => a * Math.exp(-((dt - m) * (dt - m)) / (2 * s * s));
  return g(-.12*p/.52, .025, .12) + g(-.02, .008, -.18) + g(0, .011, 1) + g(.025, .01, -.32) + g(.2*p/.52, .045, .26);
}
function periodAt(t){ return t < CUTS.exit ? .52 : .95; }
function o2At(t){ const u = Math.max(0, Math.min(1, (t - 4.2) / (17.0 - 4.2))); return 100 - 93 * Math.pow(u, .6); }
function spotAt(t, n){
  if (t < CUTS.tic) return null;
  if (t < CUTS.door) { const u = Math.min(1, (t - CUTS.tic) / 5.4); return 180 + 460 * (1 - Math.pow(1 - u, 2)) + (hsh(n) - .5) * 14; }
  if (t < CUTS.black) return 560 + (hsh(n) - .5) * 20;
  if (t < CUTS.child) return null;
  if (t < CUTS.exit) return 36.8 + (hsh(n) - .5) * .2;
  return -2 + (hsh(n) - .5) * .4;
}
const E = (id) => document.getElementById(id);
const OSD = {last: null};
const MSG = [
  {a: .45, b: 3.45, p: "RX›", s: [[.45, "אני איתך."], [1.33, " המסכה אטומה."]]},
  {a: 4.25, b: 7.05, p: "RX›", s: [[4.25, "תישאר נמוך."], [5.53, " תמשיך לזוז."]]},
  {a: 7.25, b: 9.7, p: "NAV›", s: [[7.25, "הדלת השנייה, מימין."]]},
  {a: 10.05, b: 12.3, p: "SCAN›", s: [[10.05, "יש חום מאחורי הדלת."]]},
  {a: 14.15, b: 16.85, p: "RX›", s: [[14.15, "הנה."], [14.66, " היא אצלך."]]},
];
const plate = E("plate"), TIC = E("tic");
const _p = window.onPlace;
window.onPlace = (t) => {
  _p && _p(t);
  const n = Math.round(t * 24);
  const hot = t >= CUTS.tic && t < CUTS.exit;
  if (plate) plate.style.filter = hot ? "url(#th) contrast(1.08)" : (t >= CUTS.exit ? "saturate(.8) brightness(1.06)" : "none");
  TIC.classList.toggle("calm", t >= CUTS.exit);
  const lb = lastBeat(t), P = periodAt(t), pulse = Math.exp(-Math.max(0, t - lb) * 7);
  // scan band + flicker
  E("band").style.top = (((t * 520) % 1400) - 200) + "px";
  const fl = .78 + .22 * hsh(n);
  // reticle: centre, locks onto the child
  let rx = 960, ry = 540, lk = 0;
  const cb = boxAt("child", t);
  if (t >= CUTS.child && t < CUTS.exit && cb) {
    const c = anchor(cb, "c"), u = Math.min(1, (t - CUTS.child - .15) / .5), e = u <= 0 ? 0 : 1 - Math.pow(1 - u, 3);
    rx = 960 + (c[0] - 960) * e; ry = 540 + (c[1] - 540) * e; lk = t >= 14.2 ? 1 : 0;
  }
  const rs = 1 + .05 * pulse * (t < CUTS.exit ? 1 : .4);
  E("ret").style.transform = `translate(${rx}px,${ry}px) scale(${rs})`;
  E("ret").style.opacity = (t < CUTS.tic - .1 ? 0 : t >= CUTS.exit ? Math.max(0, 1 - (t - CUTS.exit) / .5) : (t >= CUTS.black && t < CUTS.child ? .55 : 1));
  E("lock").style.opacity = lk * (t < 16.9 ? 1 : 0);
  const sv = spotAt(t, n);
  E("spotV").textContent = sv === null ? "---" : (Math.abs(sv) < 100 ? sv.toFixed(1) : Math.round(sv)) + "°C";
  E("spot").style.opacity = (t >= CUTS.black - .1 && t < CUTS.child) ? 0 : fl;
  // heat scale marker
  const mk = sv === null ? 0 : Math.max(0, Math.min(1, sv / 800));
  E("mark").style.top = (470 * (1 - mk)) + "px";
  // door heat signature (behind the door)
  const db = boxAt("door", t), BD = E("blobDoor");
  if (t >= 10.0 && t < CUTS.black && db) {
    const c = anchor(db, "c"), s = 520 * (1 + .14 * pulse), a = Math.min(1, (t - 10.0) / .4) * (.55 + .45 * pulse);
    BD.style.width = BD.style.height = s + "px"; BD.style.left = (c[0] - s / 2 + 40) + "px"; BD.style.top = (c[1] - s / 2 - 40) + "px"; BD.style.opacity = a;
    const TG = E("doorTag"); TG.style.left = (c[0] - 340) + "px"; TG.style.top = (c[1] + 170) + "px";
    TG.style.opacity = Math.min(1, (t - 10.25) / .2) * fl;
  } else { BD.style.opacity = 0; E("doorTag").style.opacity = 0; }
  // child heat signature
  const BK = E("blobKid");
  if (t >= CUTS.child && t < CUTS.exit && cb) {
    const c = anchor(cb, "c"), s = Math.max(cb[2] - cb[0], cb[3] - cb[1]) * 1.9 * (1 + .12 * pulse);
    BK.style.width = BK.style.height = s + "px"; BK.style.left = (c[0] - s / 2) + "px"; BK.style.top = (c[1] - s / 2) + "px";
    BK.style.opacity = Math.min(1, (t - CUTS.child) / .3) * (.5 + .4 * pulse);
  } else BK.style.opacity = 0;
  // oxygen gauge
  const o2 = o2At(t), deg = -135 + 270 * o2 / 100;
  E("gzN").setAttribute("transform", `rotate(${deg + (t < CUTS.exit ? (hsh(n + 7) - .5) * 1.6 : 0)})`);
  E("gzArc").style.strokeDasharray = `${o2} 100`;
  E("gzV").textContent = Math.round(o2) + "%";
  E("gzB").textContent = Math.round(3 * o2) + " BAR";
  const low = o2 < 30 && t < CUTS.exit;
  E("gzArc").style.stroke = low ? "#ff3a1c" : "";
  E("gzV").style.fill = low ? "#ff5a3a" : "";
  E("warn").style.opacity = (low && t > 11.6 && t < 16.9) ? ((Math.floor(t * 4) % 2) ? 1 : .15) : 0;
  E("gz").style.filter = `drop-shadow(0 0 ${6 + 22 * pulse}px ${low ? "rgba(255,50,20,.7)" : "rgba(255,170,40,.35)"})`;
  // ECG trace: last 2.4 s
  const W = 560, H = 90, span = 2.4; let d = "";
  for (let k = 0; k <= 140; k++) {
    const x = W * k / 140, tau = t - span + span * k / 140, b = lastBeat(tau), nb = BEATS.find((q) => q > tau);
    let v = b > -9 ? ecgV(tau - b, periodAt(tau)) : 0;
    if (nb !== undefined) v += ecgV(tau - nb, periodAt(tau));
    d += (k ? "L" : "M") + x.toFixed(1) + "," + (H * .66 - v * 52).toFixed(1);
  }
  E("ecgP").setAttribute("d", d);
  const vl = lastBeat(t) > -9 ? ecgV(t - lastBeat(t), P) : 0;
  E("ecgD").setAttribute("cx", W); E("ecgD").setAttribute("cy", H * .66 - vl * 52);
  E("bpm").textContent = t < CUTS.exit ? (114 + Math.round(hsh(Math.floor(t / .52)) * 8)) : Math.max(64, Math.round(118 - (t - CUTS.exit) * 30));
  E("clock").textContent = "00:00:" + String(Math.floor(t)).padStart(2, "0") + ":" + String(n % 24).padStart(2, "0");
  E("bootP").style.width = Math.min(100, Math.max(0, (t - .2) / 3.3 * 100)) + "%";
  // range to target (crosshair distance ticks)
  let rng = null;
  if (t >= CUTS.tic && t < CUTS.door) rng = 12 - 6.5 * Math.min(1, (t - CUTS.tic) / 6);
  else if (t >= CUTS.door && t < CUTS.black) rng = 4.2 - 1.6 * Math.min(1, (t - CUTS.door) / 2.5);
  else if (t >= CUTS.child && t < CUTS.exit) rng = Math.max(.6, 1.6 - (t - CUTS.child) * .6);
  E("distV").textContent = rng === null ? "--" : rng.toFixed(1);
  E("dist").style.opacity = (t >= CUTS.black - .1 && t < CUTS.child) ? 0 : fl;
  // PASS device: green chirp while moving, amber/red strobe when air is low
  const alarm = t > 11.6 && t < CUTS.exit, ph = (n % 12);
  E("pL1").style.fill = alarm ? (n % 4 < 2 ? "#ff3a1c" : "#2a2f36") : (ph < 2 ? "#7dffb0" : "#2a2f36");
  E("pL2").style.fill = alarm ? (n % 4 >= 2 ? "#ffb21a" : "#2a2f36") : (ph >= 6 && ph < 8 ? "#7dffb0" : "#2a2f36");
  E("passS").textContent = alarm ? "ALERT" : (t >= CUTS.exit ? "OFF" : "ARMED");
  E("passS").style.color = alarm ? "#ff5a3a" : (t >= CUTS.exit ? "#fff" : "#7dffb0");
  E("pass").style.filter = alarm && n % 4 < 2 ? "drop-shadow(0 0 14px rgba(255,60,20,.9))" : "none";
  // crew accountability
  const ct = t >= CUTS.exit + .3 ? "צוות 3 · כולם בחוץ" : "צוות 3 · 2 בפנים";
  if (E("crewT").textContent !== ct) E("crewT").textContent = ct;
  // camera OSD line (single row, monospaced cells, typed)
  let m = null;
  for (const q of MSG) if (t >= q.a && t < q.b) m = q;
  let str = "";
  if (m) for (const [st, tx] of m.s) if (t >= st) str += tx.slice(0, Math.min(tx.length, Math.floor((t - st) * 34) + 1));
  if (str !== OSD.last) { OSD.last = str; E("osdT").innerHTML = [...str].map((c) => (c === " " ? '<i class="sp">&nbsp;</i>' : "<i>" + c + "</i>")).join(""); }
  if (m && E("osdP").textContent !== m.p) E("osdP").textContent = m.p;
  E("osd").style.opacity = m ? (t - m.a < .16 ? ((n % 2) ? 1 : .35) : 1) : 0;
  E("osdC").style.opacity = (Math.floor(t * 3) % 2) ? 0 : 1;
  // thermal words: heat shimmer on the glow layers
  if (t > 12.2 && t < 14) {
    const gl = 16 + 10 * pulse + 5 * hsh(n);
    E("m5s").style.filter = `drop-shadow(0 0 5px #ffe27a) drop-shadow(0 0 ${gl}px #ff8a1a) drop-shadow(0 0 ${gl * 3}px rgba(255,74,20,.85))`;
  }
};

// ---------- timeline ----------
// boot (natural colour mask shot)
tl.fromTo("#bez", {opacity: 0, scale: 1.04}, {opacity: 1, scale: 1, duration: .5, ease: "expo.out"}, .05);
tl.fromTo(["#topL", "#topR", "#link", "#crew"], {opacity: 0}, {opacity: 1, duration: .05, stagger: .12}, .2);
tl.fromTo("#pass", {opacity: 0}, {opacity: 1, duration: .05}, .9);
tl.fromTo("#scan", {opacity: 0}, {opacity: .6, duration: .3}, .1);
tl.set("#boot", {opacity: 1}, 0); tl.to("#boot", {opacity: 0, duration: .1}, CUTS.tic - .15);
tl.fromTo("#gz", {opacity: 0, scale: .6, rotation: -30}, {opacity: 1, scale: 1, rotation: 0, duration: .5, ease: "back.out(1.6)"}, .9);
tl.fromTo("#ecg", {opacity: 0, x: 40}, {opacity: 1, x: 0, duration: .4, ease: "power3.out"}, 1.1);
tl.fromTo("#scale", {opacity: 0}, {opacity: 1, duration: .05}, CUTS.tic);
tl.fromTo("#ret svg", {scale: 2.2, opacity: 0}, {scale: 1, opacity: 1, duration: .3, ease: "expo.out"}, CUTS.tic);
tl.fromTo("#blk", {opacity: .9}, {opacity: 0, duration: .25, immediateRender: false}, CUTS.tic - .02);
// second door on the right: chevrons
tl.set("#chev", {opacity: 1}, 8.8); tl.set("#chev", {opacity: 0}, 9.8);
tl.fromTo("#chev i", {opacity: .15}, {opacity: 1, duration: .12, stagger: .12, repeat: 2, repeatDelay: .0, ease: "steps(1)"}, 8.8);
// one person: the words themselves seen as heat (white-hot on cold blue)
tl.fromTo("#cold", {opacity: 0}, {opacity: .9, duration: .14}, 12.3); tl.to("#cold", {opacity: 0, duration: .12}, 13.8);
tl.fromTo("#m5", {opacity: 0, scale: 1.25}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, 12.3); tl.to("#m5", {opacity: 0, duration: .12}, 13.8);
tl.fromTo("#scan", {opacity: .6}, {opacity: .35, duration: .2}, 12.4); tl.to("#scan", {opacity: .6, duration: .2}, 13.87);
// exit: calm white light, TIC switches off
tl.fromTo("#bloom", {opacity: 0}, {opacity: 1, duration: .12, ease: "power2.in"}, CUTS.exit - .14);
tl.to("#bloom", {opacity: 0, duration: 1.1, ease: "power2.out"}, CUTS.exit - .02);
tl.to(["#scan", "#band", "#scale", "#topL", "#topR", "#vig", "#topfade", "#pass"], {opacity: 0, duration: .5}, CUTS.exit);
tl.to("#link", {opacity: 0, duration: .3}, CUTS.exit);
tl.to("#gz", {x: 30, y: -300, scale: 1.25, duration: .9, ease: "power3.inOut"}, CUTS.exit + .1);
tl.to("#ecg", {opacity: .85, duration: .3}, CUTS.exit);
tl.fromTo("#end", {opacity: 0, x: -30}, {opacity: 1, x: 0, duration: .5, ease: "power3.out"}, 16.95);
tl.fromTo("#okw", {opacity: 0, y: 30}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, 18.22);
tl.to("#end", {opacity: 0, x: -20, duration: .35}, 19.2);
tl.to("#crew", {opacity: 0, duration: .25}, 18.4);
tl.fromTo("#shield", {opacity: 0, scale: 1.4, rotation: -10}, {opacity: 1, scale: 1, rotation: -3, duration: .38, ease: "back.out(1.5)"}, 18.95);
'''
JS = (JS.replace("__BEATS__", json.dumps(beats)).replace("__TIC__", str(CUT_TIC)).replace("__DOOR__", str(CUT_DOOR))
      .replace("__BLACK__", str(BLACK0)).replace("__CHILD__", str(CUT_CHILD)).replace("__EXIT__", str(CUT_EXIT)))

# invisible elements only to drop the soft sub-thump (heartbeat) into the sfx mix on key beats; hidden via .kn css
THUMP_ELS = [{"type": "kine", "x": 960, "y": 540, "t": b, "lines": [[{"w": "·", "t": b, "hit": True, "amt": 0}]]} for b in THUMPS]

SPEC = {
    "theme": "he_bold",
    "palette": {"acc": "#ffb21a", "ink": "#060505", "lt": "#fff3e2", "panel": "rgba(6,5,5,.8)", "sub": "#ffd9a8"},
    "music_vol": HK["music_vol"],
    "plate_vol": HK["plate_vol"],
    "vo_name": HK["vo_name"],
    "project_suffix": "-bespoke",
    "elements": THUMP_ELS,
    "fonts": {"Plex He": [("ibm-plex-sans-hebrew-hebrew-500-normal", 500, "normal"), ("ibm-plex-sans-hebrew-hebrew-700-normal", 700, "normal")],
              "Fraunces": [("fraunces-latin-900-normal", 900, "normal")],
              "JetBrains Mono": [("jetbrains-mono-latin-500-normal", 500, "normal"), ("jetbrains-mono-latin-700-normal", 700, "normal")]},
    "html_front": HTML,
    "css": CSS,
    "js": JS,
}
