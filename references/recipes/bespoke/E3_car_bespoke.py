# BESPOKE take of E3_car (AURA EV, night drive). WORLD: the windscreen.
# Everything is an automotive augmented-reality head-up display: graphics are projected onto the road plane in true
# CSS 3D perspective (rotateX 90deg about the near edge, perspective-origin = the shot's vanishing point),
# clipped to the glass in the interior shots. A lane-keep chevron ladder flows up the lane and stops with the car,
# a braking-distance band reaches past the rider and then retracts to a stop line, a soft amber contour hugs the
# rider with a HUD warning strip bolted to it, and the assistant lives INSIDE the speedometer: a split ring whose
# left half is speed (54 -> 0) and whose thin right half is the co-pilot's arc, breathing with the narration and
# turning amber at the hazard. At the hazard a bold amber AEB pictogram (car + cyclist) flashes once on the glass
# and a braking-force g-meter arc swings. Exterior: the car writes on the wet road; the close also lands as light
# projected onto a wet surface, never as a clean overlay.
# Type: Heebo 200/300/500/700 only. Motion: slow fades, projected-light reveals, no stomps, no shakes.
# Sound: soft synthesized UI chimes are pre-mixed into shared/sfx/E3_car_bespoke_vo.mp3.
import json
from pathlib import Path

T = Path(__file__).resolve().parent.parent
FONTS = T.parent / "shared/fonts"

CUT = [0, 5.0417, 8.4167, 12.0, 14.7083, 18.05]

# ---------- road planes: screen y of a point at depth d = vy + h*P/(P+d) ----------
ROADS = {
    # interior (shots 1 & 3): vanishing point where the curb lines meet, near edge hidden under the dash
    "r1": dict(vx=1330, vy=402, h=198, P=700, W=4000, L=16000),
    # POV (shot 2)
    "r2": dict(vx=900, vy=548, h=452, P=900, W=5000, L=16000),
    # exterior (shot 4): the car's own projection on the road in front of it
    "r3": dict(vx=960, vy=700, h=380, P=900, W=5000, L=8000),
    # close (shot 5): a wet surface in the lower-left, the brand lands on it as projected light
    "r4": dict(vx=345, vy=300, h=780, P=900, W=2000, L=4000),
}


def depth(r, y):
    g = ROADS[r]
    return g["P"] * (g["h"] / (y - g["vy"]) - 1)


def road(rid, inner):
    g = ROADS[rid]
    return (f'<div class="r3d" id="{rid}" style="perspective:{g["P"]}px;perspective-origin:{g["vx"]}px {g["vy"]}px">'
            f'<div class="pl" id="{rid}p" style="left:{g["vx"] - g["W"] / 2}px;top:{g["vy"] + g["h"] - g["L"]}px;'
            f'width:{g["W"]}px;height:{g["L"]}px">{inner}</div></div>')


def on(rid, x, d, w, h, cls, extra="", style=""):
    """element on the road plane: lateral x from centre, depth d (px) from the near edge"""
    g = ROADS[rid]
    return (f'<div class="{cls}" {extra} style="left:{g["W"] / 2 + x - w / 2}px;bottom:{d}px;width:{w}px;'
            f'height:{h}px;{style}"></div>')


# interior road content (shots 1 & 3): lane guides, lane-keep chevron ladder, braking band
R1_IN = (on("r1", -345, 0, 7, 16000, "lane", 'id="r1a"')
         + on("r1", 305, 0, 7, 16000, "lane", 'id="r1b"')
         + on("r1", -20, 0, 250, 16000, "chev", 'id="r1d"')
         + on("r1", -20, 0, 470, 10, "bb", 'id="r1bb"'))
# POV road content (shot 2)
R2_IN = (on("r2", -500, 0, 9, 16000, "lane", 'id="r2a"')
         + on("r2", 470, 0, 9, 16000, "lane", 'id="r2b"')
         + on("r2", -15, 0, 300, 16000, "chev", 'id="r2d"')
         + on("r2", -15, 0, 380, 10, "bb amber", 'id="r2bb"')
         + f'<div class="rtxt" id="r2lab" style="left:{ROADS["r2"]["W"] / 2 - 15 - 600}px;width:1200px;text-align:center;bottom:0px">מרחק עצירה <b>21</b> מ׳</div>')
# exterior road content (shot 4): stop line at the bumper, then two lines of text painted by light
_d_stop, _d1, _d2 = depth("r3", 842), depth("r3", 925), depth("r3", 1010)
R3_IN = (on("r3", 0, _d_stop, 1900, 10, "stopln", 'id="r3s"')
         + f'<div class="rword" id="r3w1" style="bottom:{_d1:.0f}px">הוא בסדר.</div>'
         + f'<div class="rword" id="r3w2" style="bottom:{_d2:.0f}px">את בסדר.</div>')
# close (shot 5): brand + line projected on the wet surface, a light pool and a stop line under them
_e1, _e2, _es = depth("r4", 868), depth("r4", 992), depth("r4", 884)
R4_IN = (on("r4", 0, _e2 - 60, 1100, _e1 - _e2 + 560, "pool", 'id="r4p"')
         + on("r4", 0, _es, 860, 7, "stopln", 'id="r4s"')
         + f'<div class="rword brandw" id="r4a" style="bottom:{_e1:.0f}px"><span id="lA">AURA</span> <span id="lE">EV</span></div>'
         + f'<div class="rword tagw" id="r4b" style="bottom:{_e2:.0f}px"><span id="lL">רואה ראשונה.</span></div>')


# ---------- the speedometer with the co-pilot living in it (split ring) ----------
def gauge(gid, cx, cy, size):
    return (f'<div id="{gid}" class="gauge" style="left:{cx - size / 2}px;top:{cy - size / 2}px;width:{size}px;height:{size}px">'
            f'<svg viewBox="0 0 240 240" width="{size}" height="{size}">'
            '<path class="gtrk" d="M99.2 217.8 A100 100 0 0 1 99.2 22.2"/>'
            '<path class="gspd" pathLength="100" d="M99.2 217.8 A100 100 0 0 1 99.2 22.2"/>'
            '<path class="atrk" d="M140.8 22.2 A100 100 0 0 1 140.8 217.8"/>'
            '<path class="aarc2" pathLength="100" d="M140.8 22.2 A100 100 0 0 1 140.8 217.8"/>'
            '<g class="tick"><path d="M120 6 V20"/><path d="M120 220 V234"/></g>'
            '</svg>'
            '<div class="gin"><div class="gnum"><span class="spdN">54</span></div><div class="gunit">קמ״ש</div></div></div>')


# braking-force g-meter (shot 3 only)
GMET = ('<div id="gmet" class="gmet" style="left:846px;top:352px">'
        '<svg viewBox="0 0 200 118" width="200" height="118">'
        '<path class="gtrk" d="M22 104 A78 78 0 0 1 178 104"/>'
        '<path class="gfill" pathLength="100" d="M22 104 A78 78 0 0 1 178 104"/>'
        '<g class="gtk"><path d="M22 104 h-10"/><path d="M100 26 v-10"/><path d="M178 104 h10"/></g>'
        '</svg>'
        '<div class="gval"><b id="gV">0.00</b><i>g</i></div>'
        '<div class="glab">כוח בלימה</div></div>')

# AEB pictogram: car + cyclist, bold amber, flashes once on the glass
AEB = ('<div id="aeb"><i class="bloom"></i>'
       '<svg viewBox="0 0 236 150" width="196" height="125">'
       '<rect class="afr" x="4" y="4" width="228" height="142" rx="18"/>'
       '<path class="acar" d="M18 112 V96 Q20 86 32 85 L46 84 L62 66 Q67 61 76 61 L100 61 Q107 61 112 67 L124 84 Q134 86 134 97 V112 Z"/>'
       '<path class="awin" d="M67 70 L57 82 H116 L108 72 Q106 69 101 69 Z"/>'
       '<circle class="awh" cx="42" cy="113" r="11"/><circle class="awh" cx="110" cy="113" r="11"/>'
       '<path class="ahit" d="M142 72 l9 12 -9 12 M152 66 l12 18 -12 18"/>'
       '<g class="acyc"><circle cx="178" cy="112" r="15"/><circle cx="216" cy="112" r="15"/>'
       '<path d="M178 112 L192 90 H210 L216 112 M192 90 L198 112 M186 82 H196 M208 84 L210 90"/>'
       '<path class="arider" d="M197 62 L190 86 L199 96 M195 66 L209 84"/></g>'
       '<circle class="ahead" cx="200" cy="50" r="8.5"/>'
       '</svg><span class="alab">AEB</span></div>')

HTML = f'''
<div id="g1" class="grp" data-layout-allow-overlap data-layout-allow-occlusion>
  <div id="ws">{road("r1", R1_IN)}</div>
  <div class="patch" style="left:520px;top:52px;width:660px;height:260px"></div>
  <div class="patch" style="left:520px;top:300px;width:560px;height:290px"></div>
  {gauge("spdA", 694, 430, 206)}
  {GMET}
  {AEB}
  <div id="m1" class="msg" style="right:862px;top:112px">
    <span class="k">תנאי דרך</span>
    <span class="row"><span id="w1">לילה</span><i class="sep" id="s1"></i><span id="w2">גשם</span><i class="sep" id="s2"></i><span id="w3">כביש רטוב</span></span>
  </div>
  <div id="m2" class="msg big" style="right:862px;top:104px">
    <span class="k">עוזרת נהיגה · פעילה</span>
    <span class="row"><span id="w4">אני</span> <span id="w5">איתך.</span></span>
  </div>
  <div id="m4" class="msg big" style="right:862px;top:98px">
    <span class="k" id="m4k">בלימת חירום אוטונומית</span>
    <span class="row"><span id="w6">בולמת.</span></span>
  </div>
  <div id="m4b" class="msg" style="right:862px;top:282px"><span class="row small"><span>עצירה מלאה · לפני הרוכב</span></span></div>
</div>
<div id="g2" class="grp" data-layout-allow-overlap data-layout-allow-occlusion>
  {road("r2", R2_IN)}
  <div class="patch" style="left:40px;top:700px;width:460px;height:340px"></div>
  {gauge("spdB", 250, 862, 236)}
</div>
<div id="g3" class="grp" data-layout-allow-overlap data-layout-allow-occlusion>
  {road("r3", R3_IN)}
</div>
<div id="g4" class="grp" data-layout-allow-overlap data-layout-allow-occlusion>
  <div class="patch" style="left:1440px;top:300px;width:520px;height:420px"></div>
  <div class="patch" style="left:0px;top:700px;width:720px;height:400px"></div>
  <div id="fact" class="msg" style="right:74px;top:356px">
    <span class="k">זיהוי מוקדם</span>
    <span class="fnum"><b>0.8</b> שניות</span>
    <span class="row small"><span>לפני שראית אותו</span></span>
  </div>
  <div id="aLock">{road("r4", R4_IN)}</div>
</div>
<div id="cyc" data-box="cyclist" data-pad="10" data-layout-allow-overlap data-layout-allow-occlusion><i class="halo"></i><i class="edge"></i></div>
<div id="cycL" data-follow="cyclist" data-anchor="tl" data-dx="-14" data-dy="4" data-layout-allow-overlap>
  <div class="cl"><span class="cn">רוכב</span><span class="cd"><b class="cycD">38</b> מ׳</span></div>
</div>
<div id="cycR" data-follow="cyclist" data-anchor="tl" data-dx="-6" data-dy="-2" data-layout-allow-overlap>
  <div class="wstrip">
    <span class="wrow"><svg class="wico" viewBox="0 0 40 36" width="40" height="36"><path d="M20 3 L38 33 H2 Z"/><path class="wx" d="M20 13 V23 M20 27.5 V28.5"/></svg><b id="w7">רוכב מימין</b><i class="wdot"></i><span id="w8">בחושך</span></span>
    <span class="wsub"><span class="wd"><b class="cycD">21</b> מ׳</span><span class="wk">מתקרב · צד ימין</span></span>
  </div>
</div>
'''

FACES = "".join(
    f'@font-face{{font-family:"Heebo";font-weight:{w};font-style:normal;src:url(assets/fonts/heebo-{s}-{w}-normal.woff2) format("woff2");'
    f'unicode-range:{"U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F" if s == "hebrew" else "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2191,U+2193,U+2212,U+2215"}}}'
    for w in (200, 300, 500, 700) for s in ("hebrew", "latin"))

CHEV = ("url(\"data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='260' viewBox='0 0 300 260'%3E"
        "%3Cpolyline points='34,214 150,128 266,214' fill='none' stroke='%23b8ecff' stroke-width='24' stroke-linecap='round' stroke-linejoin='round'/%3E%3C/svg%3E\")")

CSS = FACES + r"""
#flash{display:none}
:root{--hud:#e6f8ff;--glow:rgba(110,215,255,.55);--cy:#7fdcff;--amb:#ffb45c;--aeb:#ffab1f;--dim:rgba(210,240,255,.62)}
.grp{position:absolute;inset:0;opacity:0}
.grp,.grp *,#cycR *{font-family:"Heebo",sans-serif}
/* windscreen glass: the interior HUD only exists inside the glass */
#ws{position:absolute;inset:0;clip-path:polygon(402px 86px,1100px 30px,1920px 0px,1920px 594px,1500px 580px,1000px 568px,690px 560px)}
.r3d{position:absolute;inset:0}
.pl{position:absolute;transform-origin:50% 100%;transform:rotateX(90deg)}
.pl>div{position:absolute}
.lane{background:linear-gradient(to top,rgba(140,225,255,.95) 0%,rgba(140,225,255,.75) 18%,rgba(140,225,255,0) 70%);box-shadow:0 0 18px rgba(110,215,255,.6);transform-origin:50% 100%}
/* lane-keep chevron ladder, world-anchored, flows with the car */
.chev{background-image:""" + CHEV + r""";background-size:100% 260px;background-repeat:repeat-y;opacity:.85;
  -webkit-mask-image:linear-gradient(to top,transparent 0%,#000 4%,#000 14%,transparent 52%);mask-image:linear-gradient(to top,transparent 0%,#000 4%,#000 14%,transparent 52%)}
.bb{background:linear-gradient(to top,rgba(127,220,255,.16),rgba(127,220,255,.5));border-top:18px solid rgba(160,232,255,.95);box-shadow:0 0 30px rgba(110,215,255,.45)}
.bb.amber{background:linear-gradient(to top,rgba(255,180,92,.10),rgba(255,180,92,.34));border-top-color:rgba(255,196,120,.98);box-shadow:0 0 30px rgba(255,170,80,.45)}
.stopln{background:rgba(170,236,255,.95);box-shadow:0 0 40px rgba(110,215,255,.9),0 0 90px rgba(110,215,255,.5)}
.rtxt{position:absolute;transform:scaleY(1.8);transform-origin:50% 100%;white-space:nowrap;direction:rtl;font-weight:500;font-size:64px;color:#ffd9a8;text-shadow:0 0 20px rgba(255,170,80,.6)}
.rtxt b{font-weight:700}
.rword{position:absolute;left:0;transform:scaleY(1.8);transform-origin:50% 100%;width:5000px;text-align:center;direction:rtl;white-space:nowrap;font-weight:700;font-size:200px;line-height:1;color:#f2fbff;
  text-shadow:0 0 30px rgba(120,220,255,.95),0 0 90px rgba(80,200,255,.6)}
/* end card: the brand written in light on a wet surface */
#r4 .rword{width:2000px;transform:scaleY(2.1)}
#r4 .rword span{display:inline-block}
#r4 .brandw{direction:ltr;font-size:128px;font-weight:300;letter-spacing:.2em;padding-left:.2em;color:#eefaff}
#r4 .brandw #lE{font-weight:700;color:#9fe6ff}
#r4 .tagw{font-size:84px;font-weight:500;color:#e6f8ff;text-shadow:0 0 22px rgba(120,220,255,.9),0 0 60px rgba(80,200,255,.5)}
#r4 .pool{background:radial-gradient(ellipse closest-side,rgba(110,205,255,.26),rgba(90,190,255,.10) 50%,rgba(90,190,255,0) 100%);filter:blur(10px)}
#r4 .stopln{height:5px}
/* dark combiner patches keep the projected type readable over city lights */
.patch{position:absolute;background:radial-gradient(closest-side,rgba(2,6,12,.62),rgba(2,6,12,.34) 60%,rgba(2,6,12,0));pointer-events:none}
/* HUD type: glow + a faint second reflection, like light on laminated glass */
.msg,.gauge,.gmet,#fact,.cl{color:var(--hud);text-shadow:0 0 16px var(--glow),0 2px 18px rgba(0,0,0,.75),4px 5px 0 rgba(170,230,255,.10)}
.msg{position:absolute;display:flex;flex-direction:column;align-items:flex-end;direction:rtl;opacity:0}
.msg .k{font-size:24px;font-weight:300;color:var(--dim);letter-spacing:.02em;padding-bottom:10px;margin-bottom:10px;border-bottom:1px solid rgba(170,230,255,.45);width:100%;text-align:right}
.msg .row{font-size:54px;font-weight:500;line-height:1.08;white-space:nowrap;display:flex;align-items:center;gap:.3em}
.msg.big .row{font-size:104px;font-weight:300;line-height:1.02}
.msg .row.small{font-size:34px;font-weight:300;color:var(--dim)}
.sep{display:inline-block;width:8px;height:8px;border-radius:50%;background:var(--cy);box-shadow:0 0 10px var(--cy)}
/* split-ring speedometer: left = speed, right = the co-pilot's thin arc */
.gauge{position:absolute}
.gauge svg{position:absolute;inset:0;overflow:visible}
.gauge path{fill:none}
.gtrk{stroke:rgba(200,240,255,.16);stroke-width:9}
.gspd{stroke:var(--cy);stroke-width:9;stroke-linecap:butt;filter:drop-shadow(0 0 6px rgba(127,220,255,.9))}
.atrk{stroke:rgba(200,240,255,.14);stroke-width:2}
.aarc2{stroke:#dff6ff;stroke-width:2.5;stroke-linecap:round;filter:drop-shadow(0 0 5px rgba(127,220,255,.95))}
.gauge.haz .aarc2{stroke:var(--amb);filter:drop-shadow(0 0 6px rgba(255,170,80,.95))}
.tick path{stroke:rgba(220,245,255,.5);stroke-width:2}
.gin{position:absolute;inset:0;display:flex;flex-direction:column;align-items:center;justify-content:center}
.gnum{font-size:92px;font-weight:200;line-height:.9;font-variant-numeric:tabular-nums;letter-spacing:-.01em;margin-top:6px}
.gunit{font-size:22px;font-weight:300;color:var(--dim);direction:rtl;margin-top:6px}
#spdB .gnum{font-size:104px}
/* braking-force g-meter */
.gmet{position:absolute;width:200px;height:170px;opacity:0}
.gmet svg{position:absolute;left:0;top:0;overflow:visible}
.gmet path{fill:none}
.gmet .gfill{stroke:var(--amb);stroke-width:9;filter:drop-shadow(0 0 7px rgba(255,170,80,.9))}
.gmet .gtk path{stroke:rgba(220,245,255,.5);stroke-width:2}
.gval{position:absolute;left:0;width:200px;top:56px;text-align:center;direction:ltr;white-space:nowrap}
.gval b{font-size:50px;font-weight:300;font-variant-numeric:tabular-nums}
.gval i{font-style:normal;font-size:26px;font-weight:300;color:var(--dim);margin-left:4px}
.glab{position:absolute;left:0;width:200px;top:124px;text-align:center;direction:rtl;font-size:24px;font-weight:500;color:#ffe2bd}
/* AEB pictogram */
#aeb{position:absolute;left:560px;top:104px;width:196px;height:165px;opacity:0;transform-origin:50% 40%}
#aeb svg{position:absolute;left:0;top:0;overflow:visible;filter:drop-shadow(0 0 10px rgba(255,160,40,.85)) drop-shadow(0 0 30px rgba(255,140,20,.5))}
#aeb .afr{fill:rgba(40,18,0,.42);stroke:var(--aeb);stroke-width:7}
#aeb .acar{fill:var(--aeb)}
#aeb .awin{fill:rgba(40,18,0,.85)}
#aeb .awh{fill:rgba(40,18,0,.95);stroke:var(--aeb);stroke-width:6}
#aeb .ahit{fill:none;stroke:var(--aeb);stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
#aeb .acyc circle,#aeb .acyc path{fill:none;stroke:var(--aeb);stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
#aeb .ahead{fill:var(--aeb)}
#aeb .alab{position:absolute;left:0;width:196px;top:130px;text-align:center;font-size:30px;font-weight:700;letter-spacing:.34em;padding-left:.34em;color:var(--aeb);text-shadow:0 0 14px rgba(255,160,40,.9)}
#aeb .bloom{position:absolute;left:-90px;top:-80px;width:376px;height:300px;border-radius:50%;background:radial-gradient(closest-side,rgba(255,190,90,.75),rgba(255,160,40,.25) 55%,rgba(255,160,40,0));opacity:0}
/* rider contour: soft amber light that hugs the tracked silhouette */
#cyc{opacity:0}
#cyc i{position:absolute;inset:0;border-radius:46% 46% 40% 40% / 30% 30% 22% 22%}
#cyc .halo{inset:-16px;background:radial-gradient(closest-side,rgba(255,180,92,0) 62%,rgba(255,180,92,.28) 84%,rgba(255,180,92,0));filter:blur(6px)}
#cyc .edge{border:2px solid rgba(255,200,130,.95);box-shadow:0 0 14px rgba(255,170,80,.85),0 0 40px rgba(255,170,80,.45),inset 0 0 22px rgba(255,170,80,.35)}
#cyc.safe .edge{border-color:rgba(170,236,255,.95);box-shadow:0 0 14px rgba(110,215,255,.85),0 0 40px rgba(110,215,255,.45),inset 0 0 22px rgba(110,215,255,.3)}
#cyc.safe .halo{background:radial-gradient(closest-side,rgba(110,215,255,0) 62%,rgba(110,215,255,.28) 84%,rgba(110,215,255,0))}
#cycL,#cycR{opacity:0}
.cl{position:absolute;right:0;top:0;display:flex;flex-direction:column;align-items:flex-end;direction:rtl;white-space:nowrap;font-family:"Heebo",sans-serif;
  padding:8px 14px 10px;background:linear-gradient(270deg,rgba(2,6,12,.62),rgba(2,6,12,.2));border-right:2px solid var(--amb)}
.cl .cn{font-size:26px;font-weight:500;color:#ffe2bd}
.cl .cd{font-size:38px;font-weight:300;font-variant-numeric:tabular-nums}
/* POV hazard: a HUD warning strip bolted to the rider's contour */
.wstrip{position:absolute;right:0;top:0;display:flex;flex-direction:column;align-items:flex-end;direction:rtl;white-space:nowrap}
.wrow{display:flex;align-items:center;gap:14px;padding:8px 18px 10px 22px;background:linear-gradient(270deg,rgba(255,171,31,.96),rgba(255,150,30,.9));color:#1c0e00;
  font-size:40px;font-weight:700;line-height:1.1;box-shadow:0 0 26px rgba(255,160,40,.55)}
.wrow #w8{font-weight:300}
.wdot{display:inline-block;width:8px;height:8px;border-radius:50%;background:#1c0e00}
.wico path{fill:#1c0e00}
.wico .wx{fill:none;stroke:#ffab1f;stroke-width:4.5;stroke-linecap:round}
.wsub{display:flex;align-items:baseline;gap:16px;margin-top:6px;padding:4px 14px 6px;background:linear-gradient(270deg,rgba(2,6,12,.72),rgba(2,6,12,.25));border-right:3px solid var(--aeb);color:var(--hud);
  text-shadow:0 0 12px var(--glow)}
.wsub .wd{font-size:36px;font-weight:300;font-variant-numeric:tabular-nums}
.wsub .wk{font-size:24px;font-weight:300;color:#ffe2bd}
/* end card */
#fact{align-items:flex-end}
#fact .fnum{margin-top:22px;margin-bottom:34px!important;display:flex;align-items:baseline;gap:14px;font-size:44px;font-weight:300;line-height:1.1;direction:rtl;white-space:nowrap;margin-bottom:10px}
#fact .fnum b{font-size:150px;font-weight:200;line-height:1;direction:ltr;display:inline-block}
#aLock{position:absolute;inset:0;opacity:0}
"""

JS = r"""
const CUT = %s;
const FPS = 24;
// speed profile (km/h): cruise 54, the car brakes from 8.6 s, full stop at 11.6 s
function spd(t) { if (t < 8.6) return 54; const u = Math.min(1, (t - 8.6) / 3.0); return 54 * Math.pow(1 - u, 1.35); }
// distance travelled (m), integrated per frame (deterministic, seek-safe)
const DIST = [0]; for (let f = 1; f <= 460; f++) DIST.push(DIST[f - 1] + spd((f - .5) / FPS) / 3.6 / FPS);
const dist = (t) => DIST[Math.max(0, Math.min(DIST.length - 1, Math.round(t * FPS)))];
const lerp = (a, b, u) => a + (b - a) * Math.max(0, Math.min(1, u));
const ease = (u) => { u = Math.max(0, Math.min(1, u)); return u * u * (3 - 2 * u); };
const envAt = (t) => (typeof ENV !== "undefined" ? (ENV[Math.max(0, Math.min(ENV.length - 1, Math.round(t * FPS)))] || 0) : 0);
const q = (s) => document.getElementById(s);
const N = [...document.querySelectorAll(".spdN")];
const GS = [...document.querySelectorAll(".gspd")], GA = [...document.querySelectorAll(".aarc2")], GG = [...document.querySelectorAll(".gauge")];
// braking force in g: derivative of the speed profile, with a short brake-pressure build-up
function gforce(t) {
  if (t < 8.6 || t > 11.6) return 0;
  const u = (t - 8.6) / 3.0, dv = 54 * 1.35 * Math.pow(Math.max(0, 1 - u), .35) / 3.0; // km/h per s
  return dv / 3.6 / 9.81 * ease((t - 8.6) / .35);
}
window.onPlace = ((_p) => (t) => {
  _p && _p(t);
  const v = spd(t);
  N.forEach((n) => n.textContent = Math.round(v));
  GS.forEach((p) => p.style.strokeDasharray = `${(v / 60 * 100).toFixed(2)} 200`);
  // the co-pilot's arc breathes with the narration and turns amber from the hazard until the stop
  const e = envAt(t), haz = t >= 5.6 && t < 11.3;
  GG.forEach((g) => g.classList.toggle("haz", haz));
  GA.forEach((p) => { p.style.opacity = (.45 + .55 * Math.min(1, e * 1.4)).toFixed(3); p.style.strokeWidth = (2.2 + 5 * e).toFixed(2); });
  const g = gforce(t);
  q("gV").textContent = g.toFixed(2);
  q("gmet").querySelector(".gfill").style.strokeDasharray = `${(g / 1.0 * 100).toFixed(2)} 200`;
  // world-anchored chevron ladder flows toward us at the car's speed and stops when it stops
  const m = dist(t);
  q("r1d").style.backgroundPosition = `0 ${-(m * 26) %% 260}px`;
  q("r2d").style.backgroundPosition = `0 ${-(m * 60) %% 260}px`;
  // braking band: interior shot 3 retracts from past the rider to a stop line at his wheel
  q("r1bb").style.height = lerp(420, %.1f, ease((t - 8.6) / 3.0)) + "px";
  // POV: the band reaches past the rider (not safe yet)
  q("r2bb").style.height = lerp(0, 430, ease((t - 6.0) / .8)) + "px";
  q("r2lab").style.bottom = lerp(0, 452, ease((t - 6.0) / .8)) + "px";
  // rider distance
  let d = t < CUT[1] ? lerp(38, 29, (t - 2.0) / 3.0) : t < CUT[2] ? lerp(21, 14, (t - 6.0) / 2.4) : lerp(9, 2.4, ease((t - 8.6) / 3.0));
  document.querySelectorAll(".cycD").forEach((x) => x.textContent = d.toFixed(1));
  const cy = q("cyc"); cy.classList.toggle("safe", t >= 11.3);
  const pul = .5 + .5 * Math.sin(t * 5.2);
  cy.querySelector(".halo").style.opacity = .55 + .45 * pul;
  q("cycL").querySelector(".cl").style.borderRightColor = t >= 11.3 ? "#7fdcff" : "#ffb45c";
})(window.onPlace);
const show = (sel, a, b, fin = .35, fout = .3) => {
  tl.fromTo(sel, {opacity: 0}, {opacity: 1, duration: fin, ease: "sine.out", immediateRender: false}, a);
  if (b != null) tl.to(sel, {opacity: 0, duration: fout, ease: "sine.in"}, b - fout);
};
// projected-light reveal: the line is painted in from the right edge (reading direction) and settles out of a slight blur
const paint = (sel, at, dur = .6) => tl.fromTo(sel, {clipPath: "inset(0 0 0 100%%)", filter: "blur(6px)", opacity: .2},
  {clipPath: "inset(0 0 0 0%%)", filter: "blur(0px)", opacity: 1, duration: dur, ease: "power2.out", immediateRender: false}, at);
// Latin reads left to right: painted from the left edge
const paintL = (sel, at, dur = .6) => tl.fromTo(sel, {clipPath: "inset(0 100%% 0 0)", filter: "blur(6px)", opacity: .2},
  {clipPath: "inset(0 0%% 0 0)", filter: "blur(0px)", opacity: 1, duration: dur, ease: "power2.out", immediateRender: false}, at);
tl.set(".grp,#cyc,#cycL,#cycR,.msg,#aLock,#gmet,#aeb", {opacity: 0}, 0);
// ---------- groups follow the cuts ----------
tl.set("#g1", {opacity: 1}, 0); tl.set("#g1", {opacity: 0}, CUT[1]); tl.set("#g1", {opacity: 1}, CUT[2]); tl.set("#g1", {opacity: 0}, CUT[3]);
tl.set("#g2", {opacity: 1}, CUT[1]); tl.set("#g2", {opacity: 0}, CUT[2]);
tl.set("#g3", {opacity: 1}, CUT[3]); tl.set("#g3", {opacity: 0}, CUT[4]);
tl.set("#g4", {opacity: 1}, CUT[4]);
// ---------- shot 1: HUD boots, road guides draw forward ----------
tl.fromTo(["#r1a", "#r1b"], {scaleY: 0}, {scaleY: 1, duration: 1.4, ease: "power2.inOut"}, .15);
tl.fromTo("#r1d", {opacity: 0}, {opacity: .85, duration: .8}, .7);
tl.set("#r1bb", {opacity: 0}, 0);
tl.fromTo("#spdA", {opacity: 0, filter: "blur(6px)"}, {opacity: 1, filter: "blur(0px)", duration: .7, ease: "power2.out"}, .3);
tl.fromTo("#spdA .gtrk,#spdA .atrk,#spdA .tick", {opacity: 0}, {opacity: 1, duration: .6}, .3);
show("#m1", .55, 3.22);
paint("#w1", .6); tl.fromTo("#s1", {scale: 0, opacity: 0}, {scale: 1, opacity: 1, duration: .3, immediateRender: false}, 1.45); paint("#w2", 1.506, .45);
tl.fromTo("#s2", {scale: 0, opacity: 0}, {scale: 1, opacity: 1, duration: .3, immediateRender: false}, 1.70); paint("#w3", 1.738, .8);
show("#m2", 3.24, CUT[1]);
paint("#w4", 3.27, .5); paint("#w5", 3.966, .6);
// the car sees the rider long before anyone says so
show("#cyc", 2.0, CUT[1], .6, .15); show("#cycL", 2.25, CUT[1], .5, .15);
// ---------- shot 2: POV, the hazard strip bolts onto the rider ----------
tl.fromTo(["#r2a", "#r2b"], {scaleY: .2}, {scaleY: 1, duration: .8, ease: "power2.out", immediateRender: false}, CUT[1]);
show("#cyc", 5.5, CUT[2], .35, .12);
tl.fromTo("#cycR", {opacity: 0, x: 24}, {opacity: 1, x: 0, duration: .3, ease: "power2.out", immediateRender: false}, 5.62);
tl.to("#cycR", {opacity: 0, duration: .12}, CUT[2] - .12);
tl.fromTo("#cycR .wrow", {clipPath: "inset(0 0 0 100%%)"}, {clipPath: "inset(0 0 0 0%%)", duration: .35, ease: "power2.out", immediateRender: false}, 5.62);
paint("#w7", 5.7, .5); paint("#w8", 6.838, .5);
tl.fromTo("#cycR .wsub", {opacity: 0, y: -8}, {opacity: 1, y: 0, duration: .35, immediateRender: false}, 6.1);
// ---------- shot 3: the car brakes ----------
tl.set("#r1bb", {opacity: 1}, CUT[2]);
tl.fromTo("#r1bb", {opacity: 0}, {opacity: 1, duration: .3, immediateRender: false}, 8.45);
// AEB pictogram: one hard flash on the glass, holds while the car bites, then steps back
tl.fromTo("#aeb", {opacity: 0, scale: 1.28}, {opacity: 1, scale: 1, duration: .14, ease: "power3.out", immediateRender: false}, 8.45);
tl.fromTo("#aeb .bloom", {opacity: 1}, {opacity: 0, duration: .55, ease: "power2.out", immediateRender: false}, 8.45);
tl.to("#aeb", {opacity: 0, duration: .4, ease: "sine.in"}, 10.9);
show("#m4", 8.56, CUT[3], .3, .25);
paint("#w6", 8.6, .7);
show("#m4b", 11.6, CUT[3], .4, .2);
show("#gmet", 8.62, CUT[3], .3, .2);
show("#cyc", 8.72, CUT[3], .35, .15); show("#cycL", 8.8, CUT[3], .35, .15);
// ---------- shot 4: the car writes on the road ----------
tl.fromTo("#r3s", {scaleX: 0, opacity: 0}, {scaleX: 1, opacity: 1, duration: .7, ease: "power2.out", immediateRender: false}, 12.05);
tl.set(["#r3w1", "#r3w2"], {opacity: 0}, 0);
paint("#r3w1", 12.3, .7); paint("#r3w2", 13.438, .7);
// ---------- shot 5: fact, then the brand lands as projected light on the wet surface ----------
show("#fact", 14.78, null, .5);
show("#aLock", 15.2, null, .01);
tl.fromTo("#r4p", {opacity: 0}, {opacity: 1, duration: .9, ease: "sine.out", immediateRender: false}, 15.2);
tl.fromTo("#r4s", {scaleX: 0, opacity: 0}, {scaleX: 1, opacity: 1, duration: .8, ease: "power2.out", immediateRender: false}, 15.3);
paintL("#lA", 15.4, .6); paintL("#lE", 16.05, .45);
paint("#lL", 16.279, .7);
tl.set(["#lE", "#lA", "#lL", "#r4p", "#r4s", "#w1", "#w2", "#w3", "#w4", "#w5", "#w6", "#w7", "#w8", "#s1", "#s2"], {opacity: 0}, 0);
""" % (json.dumps(CUT), depth("r1", 574))

SPEC = {
    "theme": "he_bold",
    "palette": {"acc": "#7fdcff", "ink": "#02060c", "lt": "#e6f8ff", "panel": "rgba(2,6,12,.6)", "sub": "#bfe9ff"},
    "music_vol": 0.42,
    "plate_vol": 0.45,
    "vo_name": "E3_car_bespoke_vo",
    "elements": [],
    "css": CSS,
    "html_front": HTML,
    "js": JS,
    "assets": {f"fonts/heebo-{s}-{w}-normal.woff2": str(FONTS / f"heebo-{s}-{w}-normal.woff2")
               for w in (200, 300, 500, 700) for s in ("hebrew", "latin")},
}
SPEC["env"] = json.loads((T / "E3_car_he_env.json").read_text())
