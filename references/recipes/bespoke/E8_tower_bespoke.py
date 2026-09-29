"""E8_tower BESPOKE v3 - "architecture on paper".

World: an architect's drawing table at sunset. Nothing is a UI panel; everything is paper, ink, pencil and wash.
  0-3.3   a translucent VELLUM (tracing paper) sheet slides over the drone footage; the facade is inked on it in thick
          graphite with overshooting construction lines and hatched slab edges (tracked to the building), and the
          headline is hand-lettered on the trace between ruled pencil guidelines.
  3.3-13  the vellum is pulled away; a full-height SEPIA ELEVATION sheet (cream linework) slides in on the left third.
          Floors fill in watercolour-blue wash as the drone climbs; the hero is the SIGHT LINE from the current floor to
          the sea - blocked (terracotta, dashed, x) by the neighbours until you rise, then it clears and a blue view-cone
          wash opens to the sea. Floor numbers ride the real slabs like painted building signage.
          The second line is lettered on a strip of trace laid over the top-right.
  13-15.5 "ואז הנוף." is hand-lettered straight onto the sky with pencil guidelines; gold hairlines trace the penthouse,
          a horizon datum marks the sea.
  15.5-   an estate-agent sales plan: penthouse floor plan in poche walls, the sea-facing wall in gold, and SEAVIEW 24 as
          an embossed brass building plaque.
Palette: vellum cream / graphite / sepia / terracotta / sand / sea-blue / brass. Type: Karantina (hand lettering), Heebo 300 (dims), Bellefair (plaque).
Data (tracks/lines) is precomputed from the footage into tools/E8_tower_bespoke_data.json.
"""
import json
from pathlib import Path

T = Path(__file__).resolve().parent.parent
R = T.parent
W = json.loads((T / "E8_tower_climb.json").read_text())
DATA = json.loads((T / "E8_tower_bespoke_data.json").read_text())
FONTS = R / "shared/fonts"

tracks = []
seen = set()
for tr in DATA["tracks"]:
    if tr["n"] in seen or tr["n"] >= 24 or tr["f0"] < 140:
        continue
    seen.add(tr["n"])
    tracks.append(tr)

INK = "#231c18"      # graphite ink
VEL = "244,237,222"  # vellum rgb
SEP = "#5a3b27"      # sepia paper
CRM = "#f4e6c8"      # cream line
TER = "#c4623a"      # terracotta
SAND = "#e5c79a"
SEA = "#4f93b5"
GOLD = "#d9ab5c"


def _len(l):
    return ((l[2] - l[0]) ** 2 + (l[3] - l[1]) ** 2) ** .5


def ext(l, e=24):
    x0, y0, x1, y1 = l
    L = _len(l) or 1
    ux, uy = (x1 - x0) / L, (y1 - y0) / L
    return [round(x0 - ux * e, 1), round(y0 - uy * e, 1), round(x1 + ux * e, 1), round(y1 + uy * e, 1)], L + 2 * e


# ---------------- facade ink on the vellum (tracked) ----------------
fa, fo, fh = [], [], []
for j, l in enumerate(DATA["lines0"]):
    (x0, y0, x1, y1), L = ext(l, 10)
    fa.append(f'<line class="fl" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" style="stroke-dasharray:{L:.0f};stroke-dashoffset:{L:.0f}"/>')
    (a0, b0, a1, b1), L2 = ext(l, 46)   # construction overshoot
    fo.append(f'<line class="fo" x1="{a0}" y1="{b0}" x2="{a1}" y2="{b1}" style="stroke-dasharray:{L2:.0f};stroke-dashoffset:{L2:.0f}"/>')
    # hatched slab band under long near-horizontal lines
    if _len(l) > 150 and abs(l[3] - l[1]) < .75 * abs(l[2] - l[0]):
        d = 24
        fh.append(f'<path class="fhat" d="M{l[0]},{l[1]} L{l[2]},{l[3]} L{l[2]},{l[3] + d} L{l[0]},{l[1] + d} Z"/>')

# ---------------- penthouse gold linework (end, tracked) ----------------
pt = []
for j, l in enumerate(DATA["linesT"]):
    (x0, y0, x1, y1), L = ext(l, 30)
    pt.append(f'<line class="gl2" x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" style="stroke-dasharray:{L:.0f};stroke-dashoffset:{L:.0f}"/>')
roof = DATA["linesT"][0]
rx, ry = (roof[0], roof[1]) if roof[0] < roof[2] else (roof[2], roof[3])
HZ = (60, 545, 1070, 537)

# ---------------- sepia elevation sheet (left third, full height) ----------------
EW = 640
GY, FH, TX0, TX1 = 790, 25.5, 400, 540
TOP = GY - FH * 24
NB = [(156, 216, 92), (232, 292, 172), (308, 372, 270)]
SX, SYY = 64, GY - 3        # sight target on the sea
el = []
# drawing-table margin line (single, no grid refs)
el.append(f'<rect x="22" y="22" width="{EW - 44}" height="1036" class="e0"/>')
# ground + earth hatch
el.append(f'<line x1="30" y1="{GY}" x2="{EW - 30}" y2="{GY}" class="e3"/>')
el.append('<path class="e0" d="' + "".join(f'M{x},{GY + 3} l-16,16 ' for x in range(170, EW - 34, 12)) + '"/>')
# sea: watercolour wash + wave strokes, sun on the horizon
el.append(f'<path d="M30,{GY - 1} H158 V{GY + 44} H30 Z" class="wash" id="eSeaW"/>')
el.append(f'<path id="eSea" class="e2" d="M32,{GY - 2} ' + " ".join("q8,-7 16,0" for _ in range(8)) + '"/>')
el.append(f'<path class="e1" d="M40,{GY + 14} ' + " ".join("q8,-6 16,0" for _ in range(6)) + f' M52,{GY + 28} ' + " ".join("q8,-6 16,0" for _ in range(5)) + '"/>')
el.append(f'<path d="M58,{GY - 2} a30,30 0 0 1 60,0" class="sun"/>')
el.append(f'<text x="94" y="{GY + 72}" class="elab">הים</text>')
# neighbours (outline + light hatch)
for a, b, h in NB:
    el.append(f'<rect x="{a}" y="{GY - h}" width="{b - a}" height="{h}" class="e1 nb"/>')
    el.append('<path class="e0" d="' + "".join(f'M{a},{GY - h + y} L{min(b, a + y)},{GY - h + y - min(b - a, y)} ' for y in range(14, h, 14)) + '"/>')
# watercolour floor wash (height driven per frame)
el.append(f'<rect id="eWash" x="{TX0}" y="{GY}" width="{TX1 - TX0}" height="0" class="wash"/>')
el.append(f'<rect id="eCur" x="{TX0}" y="{GY - FH}" width="{TX1 - TX0}" height="{FH}" class="wash2"/>')
# tower outline, slabs, parapet, roof garden
el.append(f'<rect x="{TX0}" y="{TOP:.1f}" width="{TX1 - TX0}" height="{FH * 24:.1f}" class="e3 dr"/>')
for f in range(1, 24):
    y = GY - FH * f
    el.append(f'<line x1="{TX0 - 8}" y1="{y:.1f}" x2="{TX1 + 8}" y2="{y:.1f}" class="e1 dr"/>')
el.append(f'<path class="e2 dr" d="M{TX0 - 10},{TOP - 14:.1f} H{TX1 + 10} M{TX0 + 36},{TOP:.1f} V{TOP - 30:.1f} H{TX1 - 20} V{TOP:.1f}"/>')
el.append(f'<path id="ePh" class="gd" d="M{TX0 - 12},{TOP + FH:.1f} H{TX1 + 12} M{TX0 - 12},{TOP - 14:.1f} H{TX1 + 12}"/>')
for f in range(1, 25):
    y = GY - FH * (f - .5)
    el.append(f'<text x="{TX0 - 24}" y="{y + 5:.1f}" class="efn" id="efn{f}">{f}</text>')
# overall height dimension
el.append(f'<g class="dr"><line x1="{TX1 + 44}" y1="{TOP - 14:.1f}" x2="{TX1 + 44}" y2="{GY}" class="e1"/>'
          f'<line x1="{TX1 + 36}" y1="{TOP - 6:.1f}" x2="{TX1 + 52}" y2="{TOP - 22:.1f}" class="e2"/><line x1="{TX1 + 36}" y1="{GY + 8}" x2="{TX1 + 52}" y2="{GY - 8}" class="e2"/>'
          f'<text x="{TX1 + 44}" y="{TOP - 34:.0f}" class="edim">72.00</text></g>')
# view cone + sight line (hero)
el.append(f'<path id="eCone" d="M0,0" class="cone"/>')
el.append('<line id="eSb" x1="0" y1="0" x2="0" y2="0" class="sblk"/>')
el.append('<line id="eSr" x1="0" y1="0" x2="0" y2="0" class="srest"/>')
el.append('<line id="eSc" x1="0" y1="0" x2="0" y2="0" class="sclr"/>')
el.append('<g id="eX"><path d="M-11,-11 L11,11 M11,-11 L-11,11" class="xmk"/></g>')
el.append(f'<g id="eArr"><path d="M0,0 l24,-6 l-5,6 l5,6 Z" class="arr"/></g>')
el.append('<g id="eEye"><circle r="7" class="eye"/><circle r="2.6" class="eye2"/></g>')
el.append('<text id="eSL" class="slab" x="0" y="0">קו מבט לים</text>')
# level marker
el.append('<g id="eLv"><path d="M0,0 l-12,-16 h24 Z" class="lvt"/><line x1="-8" y1="0" x2="60" y2="0" class="lvl"/>'
          '<text x="16" y="-8" class="lvx" id="eLvT">+0.00</text></g>')
el_svg = (f'<svg id="elS" width="{EW}" height="1080" viewBox="0 0 {EW} 1080">'
          '<defs><filter id="wcf" x="-10%" y="-10%" width="120%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.045" numOctaves="3" seed="7" result="n"/>'
          '<feDisplacementMap in="SourceGraphic" in2="n" scale="7" xChannelSelector="R" yChannelSelector="G"/><feGaussianBlur stdDeviation=".7"/></filter>'
          '<filter id="pap" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".75" numOctaves="2" seed="3"/>'
          '<feColorMatrix values="0 0 0 0 .95  0 0 0 0 .86  0 0 0 0 .7  0 0 0 .09 0"/></filter></defs>'
          f'<rect width="{EW}" height="1080" filter="url(#pap)"/>'
          + "".join(el) + '</svg>')
EL_HTML = (f'<div id="el">{el_svg}'
           '<div class="eh"><span class="eh1">חזית מערבית</span><span class="eh2">SEAVIEW 24 · 1:500</span></div>'
           '<div class="ei"><div class="eiF"><span class="eiL">קומה</span><span class="eiN" id="eNum">1</span></div>'
           '<div class="eiP"><span>החל מ־</span><b id="ePr">2.1</b><span>מיליון ₪</span></div></div></div>')

# ---------------- vellum opener ----------------
VEL_HTML = ('<div id="vel"><svg class="vtex" width="1920" height="1080"><defs><filter id="vpap" x="0" y="0" width="100%" height="100%">'
            '<feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="11"/><feColorMatrix values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 .16 0"/></filter></defs>'
            '<rect width="1920" height="1080" filter="url(#vpap)"/></svg>'
            '<svg id="ink" viewBox="0 0 1920 1080" width="1920" height="1080"><defs>'
            '<pattern id="hp" width="9" height="9" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="9" stroke="' + INK + '" stroke-width="2.6"/></pattern>'
            '<filter id="pen" x="-2%" y="-2%" width="104%" height="104%"><feTurbulence type="fractalNoise" baseFrequency=".035" numOctaves="2" seed="5"/>'
            '<feDisplacementMap in="SourceGraphic" scale="3.2" xChannelSelector="R" yChannelSelector="G"/></filter></defs>'
            f'<g id="fa" filter="url(#pen)"><g id="fhs">{"".join(fh)}</g>{"".join(fo)}{"".join(fa)}</g></svg>'
            '<div id="h1" class="lett">'
            '<svg class="gls" width="760" height="420"><g class="gl" id="g1">'
            '<line x1="760" y1="64" x2="0" y2="64"/><line x1="760" y1="168" x2="0" y2="168"/><line x1="760" y1="232" x2="0" y2="232"/><line x1="760" y1="352" x2="0" y2="352"/></g></svg>'
            '<div class="lw" style="top:12px"><span id="hw1">כל</span> <span id="hw2">קומה,</span></div>'
            '<div class="lw" style="top:196px"><span id="hw3">והמחיר</span> <span id="hw4" class="ter">שלה.</span></div></div>'
            '<div id="vnote" class="vn">חזית ראשית · סקיצה 01</div>'
            '</div>')

# ---------------- trace strip for line 2 ----------------
N2_HTML = ('<div id="n2"><svg class="vtex" width="820" height="330"><rect width="820" height="330" filter="url(#vpap)"/></svg>'
           '<svg class="gls" width="820" height="330"><g class="gl" id="g2"><line x1="800" y1="40" x2="20" y2="40"/><line x1="800" y1="148" x2="20" y2="148"/>'
           '<line x1="800" y1="186" x2="20" y2="186"/><line x1="800" y1="296" x2="20" y2="296"/></g></svg>'
           '<div class="lw2" style="top:22px"><span id="n2a">וככל שעולים,</span></div>'
           '<div class="lw2" style="top:168px"><span id="n2b" class="sea">הים נפתח.</span></div></div>')

# ---------------- sky title ----------------
TT_HTML = ('<div id="tt"><svg class="gls" width="900" height="470"><g class="gl" id="g3">'
           '<line x1="900" y1="76" x2="0" y2="76"/><line x1="900" y1="182" x2="0" y2="182"/><line x1="900" y1="265" x2="0" y2="265"/><line x1="900" y1="436" x2="0" y2="436"/></g></svg>'
           '<div class="t1" id="tt1">ואז</div><div class="t2" id="tt2">הנוף.</div></div>')

# ---------------- datum labels + facade signage ----------------
svg_front = ('<svg id="dw" viewBox="0 0 1920 1080" width="1920" height="1080">'
             '<defs><filter id="glw" x="-5%" y="-5%" width="110%" height="110%"><feGaussianBlur stdDeviation="2.4" result="b"/>'
             '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter></defs>'
             + "".join(f'<g id="lv{k}" opacity="0"><line x1="-40" y1="0" x2="600" y2="0" class="lvd" id="lv{k}L"/>'
                       f'<path d="M0,0 l-12,-17 h24 Z" class="lvt2"/>'
                       f'<text x="40" y="-14" class="sign">{tr["n"]}</text><text x="{52 + 40 * len(str(tr["n"]))}" y="-14" class="sign2">קומה</text></g>'
                       for k, tr in enumerate(tracks))
             + f'<g id="pt" filter="url(#glw)">{"".join(pt)}'
             f'<line id="hz" x1="{HZ[0]}" y1="{HZ[1]}" x2="{HZ[2]}" y2="{HZ[3]}" class="hzl"/>'
             f'<g id="rmk" transform="translate({rx + 40},{ry})" opacity="0"><path d="M0,0 l-12,-17 h24 Z" class="gtri"/></g></g>'
             '</svg>')
labels = ('<div id="rmkL" class="dl gold">+72.00 <span>גג הפנטהאוז</span></div>'
          '<div id="hzL" class="dl">±0.00 <span>פני הים</span></div>')

# ---------------- sales plan + brass plaque ----------------
PW, PH = 600, 470
wall = []
# outer walls (poche), sea wall on the left is glazing (gold)
wall.append('<path class="pw" d="M70,40 H560 V430 H70 V330 M70,150 V40" id="pwO"/>')
wall.append('<path class="pwi" d="M300,40 V200 M300,250 V430 M300,260 H400 M450,260 H560 M430,260 V430 M70,250 H180 M230,250 H300"/>')
wall.append('<path class="pdoor" d="M180,250 a50,50 0 0 1 50,-50 M400,260 a50,50 0 0 0 50,50"/>')
wall.append('<path id="pSea" class="psea" d="M70,40 V430"/>')
wall.append('<path id="pSeaG" class="psea2" d="M60,60 V410"/>')
wall.append('<path class="pbal" d="M70,40 H20 V430 H70"/>')
wall.append('<g class="pwav">' + "".join(f'<path d="M-40,{y} q6,-6 12,0 t12,0"/>' for y in (120, 210, 300, 390)) + '</g>')
wall.append('<g id="pArr"><path d="M-8,245 H-70" class="parl"/><path d="M-70,245 l14,-8 v16 Z" class="parh"/></g>')
rooms = [("סלון ופינת אוכל", 185, 150, 32), ("חדר שינה", 185, 340, 30), ("מטבח", 365, 150, 30), ("חדר הורים", 495, 350, 30),
         ("רחצה", 365, 350, 26), ("מרפסת שמש", 45, 470, 26)]
rtxt = "".join(f'<text class="prm" x="{x}" y="{y}" font-size="{s}">{n}</text>' for n, x, y, s in rooms)
plan_svg = (f'<svg id="plan" width="{PW}" height="{PH + 40}" viewBox="-90 10 670 500">' + "".join(wall) + rtxt +
            '<text class="plam" x="-50" y="160">לים</text>'
            '<g transform="translate(520,470)"><circle r="16" class="pn"/><path d="M0,-24 L7,6 L0,1 L-7,6 Z" class="pnh"/></g></svg>')
SALE_HTML = ('<div id="sale"><svg class="vtex" width="660" height="880"><rect width="660" height="880" filter="url(#pap2)"/></svg>'
             '<div id="plq"><i class="sc s1"></i><i class="sc s2"></i><i class="sc s3"></i><i class="sc s4"></i>'
             '<div class="pq1">SEAVIEW 24</div><div class="pq2">מגורים מול הים</div></div>'
             '<div class="sh">פנטהאוז · קומה 24</div>' + plan_svg +
             '<div class="sf"><span>210 מ״ר · מרפסת שמש לים</span><b>בתיאום מראש</b></div></div>')
PAP2 = ('<svg width="0" height="0" style="position:absolute"><defs><filter id="pap2" x="0" y="0" width="100%" height="100%">'
        '<feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="2" seed="9"/><feColorMatrix values="0 0 0 0 .55  0 0 0 0 .45  0 0 0 0 .3  0 0 0 .1 0"/></filter></defs></svg>')

HTML_FRONT = PAP2 + svg_front + labels + VEL_HTML + EL_HTML + N2_HTML + TT_HTML + SALE_HTML

# ---------------- fonts ----------------
assets = {}
faces = []
HEB = "U+0590-05FF,U+FB1D-FB4F,U+200C-2010,U+20AA,U+25CC"
LAT = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2199,U+2212,U+2215"
for fam, stem0, ws in (("Heebo", "heebo", (300, 400, 600)), ("Karantina", "karantina", (400, 700)), ("Bellefair", "bellefair", (400,))):
    for w in ws:
        for sub, ur in (("hebrew", HEB), ("latin", LAT)):
            stem = f"{stem0}-{sub}-{w}-normal"
            assets[f"fonts/{stem}.woff2"] = str(FONTS / f"{stem}.woff2")
            faces.append(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;src:url(assets/fonts/{stem}.woff2) format("woff2");unicode-range:{ur}}}')

KA = '"Karantina",sans-serif'
CSS = "".join(faces) + f"""
#dw{{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}}
.vtex{{position:absolute;left:0;top:0;pointer-events:none}}
/* ---- vellum ---- */
#vel{{position:absolute;left:170px;top:-20px;width:1790px;height:1120px;background:rgba({VEL},.60);
  box-shadow:-6px 0 22px rgba(40,25,10,.28), inset 1px 0 0 rgba(255,255,255,.7);transform:rotate(-.6deg);transform-origin:0 50%}}
#ink{{position:absolute;left:-170px;top:20px;overflow:visible}}
.fl{{fill:none;stroke:{INK};stroke-width:4.8;stroke-linecap:round}}
.fo{{fill:none;stroke:rgba(35,28,24,.55);stroke-width:1.3;stroke-linecap:round}}
.fhat{{fill:url(#hp);stroke:none;opacity:0}}
.lett{{position:absolute;direction:rtl}}
#h1{{left:40px;top:640px;width:760px;height:420px}}
.gls{{position:absolute;left:0;top:0;overflow:visible}}
.gl line{{stroke:rgba(35,28,24,.45);stroke-width:1.2}}
#g3 line,#g2 line{{stroke:rgba(35,28,24,.5)}}
.lw{{position:absolute;right:20px;font-family:{KA};font-weight:700;font-size:196px;line-height:1;color:{INK};white-space:nowrap;letter-spacing:.01em}}
.lw span,.lw2 span{{display:inline-block}}
.ter{{color:{TER}}}
.vn{{position:absolute;right:120px;bottom:70px;font-family:{KA};font-weight:400;font-size:44px;color:rgba(35,28,24,.8);direction:rtl;
  border-top:2px solid rgba(35,28,24,.6);padding-top:4px}}
/* ---- sepia elevation ---- */
#el{{position:absolute;left:0;top:0;width:{EW}px;height:1080px;background:linear-gradient(170deg,#6a4630 0%,{SEP} 55%,#4b2f1f 100%);
  box-shadow:10px 0 34px rgba(20,10,4,.55);direction:rtl;font-family:"Heebo",sans-serif;color:{CRM}}}
#elS{{position:absolute;left:0;top:0}}
.e0{{fill:none;stroke:rgba(244,230,200,.35);stroke-width:1}}
.e1{{fill:none;stroke:rgba(244,230,200,.75);stroke-width:1.4}}
.e2{{fill:none;stroke:{CRM};stroke-width:2}}
.e3{{fill:none;stroke:{CRM};stroke-width:3}}
.wash{{fill:{SEA};fill-opacity:.62;filter:url(#wcf)}}
.wash2{{fill:#7cc0e0;fill-opacity:.85;filter:url(#wcf)}}
.sun{{fill:{TER};fill-opacity:.85;stroke:{SAND};stroke-width:1.5}}
.gd{{fill:none;stroke:{GOLD};stroke-width:3}}
.efn{{font-family:"Heebo",sans-serif;font-weight:400;font-size:15px;fill:{CRM};text-anchor:end}}
.edim{{font-family:"Heebo",sans-serif;font-weight:300;font-size:16px;fill:rgba(244,230,200,.85);text-anchor:middle}}
.elab{{font-family:{KA};font-weight:700;font-size:40px;fill:{CRM};text-anchor:middle}}
.cone{{fill:#8fcbe6;fill-opacity:0;filter:url(#wcf)}}
.sblk{{stroke:{TER};stroke-width:3.2;stroke-dasharray:10 8;stroke-linecap:round}}
.srest{{stroke:rgba(244,230,200,.4);stroke-width:1.4;stroke-dasharray:2 7}}
.sclr{{stroke:#bfe6f7;stroke-width:5;stroke-linecap:round}}
.xmk{{fill:none;stroke:{TER};stroke-width:4;stroke-linecap:round}}
.arr{{fill:#bfe6f7}}
.eye{{fill:{SEP};stroke:{CRM};stroke-width:2.4}}.eye2{{fill:{CRM}}}
.slab{{font-family:{KA};font-weight:700;font-size:40px;fill:{CRM};text-anchor:middle}}
.lvt{{fill:{SAND}}}.lvl{{stroke:{SAND};stroke-width:2}}
.lvx{{font-family:"Heebo",sans-serif;font-weight:600;font-size:20px;fill:{SAND};direction:ltr}}
#el .eh{{position:absolute;left:44px;right:44px;top:40px;display:flex;justify-content:space-between;align-items:baseline;border-bottom:2px solid rgba(244,230,200,.6);padding-bottom:6px}}
.eh1{{font-family:{KA};font-weight:700;font-size:70px;line-height:1}}
.eh2{{font-weight:300;font-size:17px;letter-spacing:.14em;direction:ltr;color:{SAND}}}
#el .ei{{position:absolute;left:44px;right:44px;top:866px;border-top:2px solid rgba(244,230,200,.6);padding-top:2px}}
.eiF{{display:flex;align-items:baseline;gap:18px;height:126px}}
.eiL{{font-family:{KA};font-weight:700;font-size:74px;color:{SAND}}}
.eiN{{font-family:{KA};font-weight:700;font-size:134px;line-height:.9;color:{CRM};font-variant-numeric:tabular-nums}}
.eiP{{display:flex;align-items:baseline;gap:12px;white-space:nowrap;font-family:{KA};font-weight:700;font-size:54px;color:{SAND}}}
.eiP b{{font-size:66px;color:#f0b48f;direction:ltr}}
/* ---- trace strip ---- */
#n2{{position:absolute;left:1060px;top:44px;width:820px;height:330px;background:rgba({VEL},.80);box-shadow:0 8px 26px rgba(40,25,10,.3);transform:rotate(.8deg);direction:rtl}}
.lw2{{position:absolute;right:26px;font-family:{KA};font-weight:700;font-size:150px;line-height:1;color:{INK};white-space:nowrap}}
.sea{{color:#2d6f93}}
/* ---- sky title ---- */
#tt{{position:absolute;left:90px;top:40px;width:900px;height:470px;direction:rtl;text-align:right}}
#tt .t1,#tt .t2{{position:absolute;right:20px;font-family:{KA};font-weight:700;color:{INK};line-height:1;white-space:nowrap;text-shadow:0 0 40px rgba({VEL},.55)}}
#tt .t1{{top:30px;font-size:180px}}
#tt .t2{{top:196px;font-size:280px}}
/* ---- facade signage ---- */
.lvd{{stroke:{CRM};stroke-width:2.6;stroke-dasharray:30 7 5 7;filter:drop-shadow(0 0 2px rgba(30,15,5,.95))}}
.lvt2{{fill:{TER};stroke:{CRM};stroke-width:2}}
.sign{{font-family:{KA};font-weight:700;font-size:92px;fill:{CRM};stroke:rgba(40,22,10,.85);stroke-width:5;paint-order:stroke;direction:ltr}}
.sign2{{font-family:{KA};font-weight:700;font-size:44px;fill:{SAND};stroke:rgba(40,22,10,.85);stroke-width:4;paint-order:stroke}}
.gl2{{fill:none;stroke:{GOLD};stroke-width:2.6;stroke-linecap:round}}
.hzl{{stroke:{CRM};stroke-width:2.4;stroke-dasharray:34 8 6 8;filter:drop-shadow(0 0 3px rgba(30,15,5,.8))}}
.gtri{{fill:{GOLD};stroke:{CRM};stroke-width:1.5}}
.dl{{position:absolute;left:0;top:0;font-family:{KA};font-weight:700;font-size:50px;color:{CRM};direction:ltr;white-space:nowrap;opacity:0;
  text-shadow:0 0 3px rgba(30,15,5,.95),0 2px 10px rgba(30,15,5,.7)}}
.dl span{{margin-left:10px}}
.dl.gold{{color:#f3cf8c}}
#hzL{{color:{INK};text-shadow:0 0 6px rgba({VEL},.95),0 0 18px rgba({VEL},.8)}}
/* ---- sales plan ---- */
#sale{{position:absolute;left:1220px;top:70px;width:660px;height:880px;background:#f3ead7;box-shadow:0 18px 50px rgba(20,10,4,.5);direction:rtl}}
#plq{{position:absolute;left:40px;right:40px;top:34px;height:150px;border-radius:6px;
  background:linear-gradient(160deg,#8a5e2c 0%,#d9b270 22%,#f1d9a0 40%,#b98a47 62%,#e6c688 80%,#8f6431 100%);
  box-shadow:inset 0 2px 1px rgba(255,245,215,.8),inset 0 -3px 2px rgba(70,40,10,.55),0 6px 14px rgba(40,20,5,.45);text-align:center}}
.sc{{position:absolute;width:12px;height:12px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff1c9,#9a6f36 70%)}}
.s1{{left:14px;top:14px}}.s2{{right:14px;top:14px}}.s3{{left:14px;bottom:14px}}.s4{{right:14px;bottom:14px}}
.pq1{{font-family:"Bellefair",serif;font-size:84px;line-height:1;padding-top:16px;letter-spacing:.12em;color:#6e4a1e;direction:ltr;
  text-shadow:0 -1px 0 rgba(60,35,8,.9),0 2px 1px rgba(255,240,200,.9)}}
.pq2{{font-family:"Bellefair",serif;font-size:32px;color:#6e4a1e;text-shadow:0 -1px 0 rgba(60,35,8,.6),0 1px 1px rgba(255,240,200,.9)}}
#sale .sh{{position:absolute;right:44px;top:204px;font-family:{KA};font-weight:700;font-size:64px;color:{INK}}}
#plan{{position:absolute;left:30px;top:290px;overflow:visible}}
.pw{{fill:none;stroke:{INK};stroke-width:14;stroke-linejoin:miter}}
.pwi{{fill:none;stroke:{INK};stroke-width:6}}
.pdoor{{fill:none;stroke:rgba(35,28,24,.6);stroke-width:1.5}}
.psea{{fill:none;stroke:{GOLD};stroke-width:16}}
.psea2{{fill:none;stroke:{GOLD};stroke-width:2;stroke-dasharray:14 6}}
.pbal{{fill:none;stroke:rgba(35,28,24,.55);stroke-width:2;stroke-dasharray:6 5}}
.pwav path{{fill:none;stroke:{SEA};stroke-width:3}}
.parl{{stroke:{TER};stroke-width:4}}.parh{{fill:{TER}}}
.plam{{font-family:{KA};font-weight:700;font-size:44px;fill:{TER};text-anchor:middle}}
.prm{{font-family:{KA};font-weight:700;fill:{INK};text-anchor:middle}}
.pn{{fill:none;stroke:{INK};stroke-width:1.5}}.pnh{{fill:{INK}}}
#sale .sf{{position:absolute;left:44px;right:44px;bottom:26px;display:flex;justify-content:space-between;align-items:baseline;border-top:2px solid {INK};padding-top:6px;
  font-family:{KA};font-weight:700;color:{INK}}}
#sale .sf span{{font-size:44px}}#sale .sf b{{font-size:44px;color:{TER}}}
#wm{{z-index:5}}
"""

JS_DATA = ("const E8D=" + json.dumps({"s": DATA["start"], "p": DATA["top"], "tr": tracks, "W": W, "roof": [rx, ry], "hz": HZ, "nb": NB},
                                     separators=(",", ":")) + ";\n")

JS = JS_DATA + f"const GY={GY},FH={FH},TX0={TX0},TX1={TX1},SX={SX},SYY={SYY};\n" + r"""
(function(){
const S=E8D, $i=(id)=>document.getElementById(id);
const wa=(t)=>S.W[Math.max(0,Math.min(S.W.length-1,Math.round(t*24)))];
const LEGS=[[3.2,5.95,1,12],[6.8,11.0,12,24]];
function FLf(t){for(const[a,b,x,y]of LEGS){if(t<a)return x;if(t<=b){const lin=(t-a)/(b-a);const wn=(wa(t)-wa(a))/Math.max(1e-6,wa(b)-wa(a));const u=Math.min(1,Math.max(0,.5*lin+.5*wn));return x+(y-x)*u;}}return 24;}
function mat(ch,fr){const keys=Object.keys(ch).map(Number);const lo=Math.min(...keys),hi=Math.max(...keys);const k=Math.max(lo,Math.min(hi,fr));return ch[String(k)];}
function app(m,x,y){return [m[0]*x+m[1]*y+m[2], m[3]*x+m[4]*y+m[5]];}
function svgm(m){return `matrix(${m[0]},${m[3]},${m[1]},${m[4]},${m[2]},${m[5]})`;}
const place=(el,x,y)=>{el.style.transform=`translate(${x}px,${y}px)`;};
const L=(id,a,b,c,d)=>{const e=$i(id);e.setAttribute("x1",a.toFixed(1));e.setAttribute("y1",b.toFixed(1));e.setAttribute("x2",c.toFixed(1));e.setAttribute("y2",d.toFixed(1));};
const _p=window.onPlace;
window.onPlace=(t)=>{ _p&&_p(t);
  const fr=Math.round(t*24);
  $i("fa").setAttribute("transform",svgm(mat(S.s,fr)));
  const mt=mat(S.p,fr); $i("pt").setAttribute("transform",svgm(mt));
  const r=app(mt,S.roof[0]+40,S.roof[1]); const rl=$i("rmkL"); place(rl,r[0]-rl.offsetWidth/2,r[1]-rl.offsetHeight-30);
  const h=app(mt,S.hz[0]+330,S.hz[1]); const hl=$i("hzL"); place(hl,h[0],h[1]+14);
  // elevation: watercolour floors
  const F=FLf(t), fi=Math.max(1,Math.min(24,Math.round(F)));
  const top=GY-FH*Math.min(24,F); const w=$i("eWash"); w.setAttribute("y",top.toFixed(1)); w.setAttribute("height",(GY-top).toFixed(1));
  $i("eCur").setAttribute("y",(GY-FH*fi).toFixed(1));
  for(let f=1;f<=24;f++){const e=$i("efn"+f); e.style.fill=f===fi?"#ffffff":(f===24?"#f0c476":"#f4e6c8"); e.style.fontWeight=f===fi?600:400; e.style.fontSize=f===fi?"20px":"15px";}
  const yF=GY-FH*(F-.5);
  $i("eLv").setAttribute("transform",`translate(${TX1+4},${yF.toFixed(2)})`);
  $i("eLvT").textContent="+"+((F-1)*3).toFixed(2);
  $i("eNum").textContent=String(fi);
  $i("ePr").textContent=(2.1+(fi-1)*2.7/23).toFixed(1);
  // sight line (hero)
  const ex=TX0-3, ey=yF, yAt=(x)=>ey+(SYY-ey)*(ex-x)/(ex-SX);
  let margin=1e9, hit=null;
  for(let k=S.nb.length-1;k>=0;k--){const [a,b,hh]=S.nb[k]; const m=(GY-hh)-yAt(a); margin=Math.min(margin,m);
    if(m<0&&!hit){ // first obstruction seen from the tower
      if(yAt(b)>GY-hh){hit=[b,yAt(b)];} else {const x=ex-(GY-hh-ey)*(ex-SX)/(SYY-ey); hit=[x,GY-hh];}}}
  const c=Math.max(0,Math.min(1,margin/22));
  $i("eEye").setAttribute("transform",`translate(${ex},${ey.toFixed(1)})`);
  if(hit){L("eSb",ex,ey,hit[0],hit[1]); L("eSr",hit[0],hit[1],SX,SYY); $i("eX").setAttribute("transform",`translate(${hit[0].toFixed(1)},${hit[1].toFixed(1)})`);}
  $i("eSb").style.opacity=hit?1:0; $i("eSr").style.opacity=hit?1:0; $i("eX").style.opacity=hit?1:0;
  L("eSc",ex,ey,ex-(ex-SX-22)*c,ey+(SYY-ey)*(ex-(ex-(ex-SX-22)*c))/(ex-SX)); $i("eSc").style.opacity=c>0?1:0;
  const ang=Math.atan2(SYY-ey,SX-ex)*180/Math.PI;
  $i("eArr").setAttribute("transform",`translate(${SX+2},${SYY})rotate(${(ang+180).toFixed(2)})`); $i("eArr").style.opacity=c;
  $i("eCone").setAttribute("d",`M${ex},${ey.toFixed(1)} L32,${GY-2} L158,${GY-2} Z`); $i("eCone").style.fillOpacity=(.5*c).toFixed(3);
  const mx=(ex+SX)/2, my=(ey+SYY)/2; const sl=$i("eSL");
  sl.setAttribute("transform",`translate(${mx.toFixed(1)},${my.toFixed(1)})rotate(${(ang+180).toFixed(2)})translate(0,-24)`);
  sl.style.fill=c>.5?"#bfe6f7":"#f4e6c8";
  $i("eSea").style.stroke=c>.5?"#bfe6f7":"#f4e6c8"; $i("eSeaW").style.fillOpacity=(.35+.5*c).toFixed(3);
  // facade signage riding tracked slab points
  const shown=[];
  S.tr.forEach((tr,k)=>{const g=$i("lv"+k); const i=fr-tr.f0, n=tr.p.length;
    if(i<0||i>=n){g.setAttribute("opacity",0); return;}
    const [x,y]=tr.p[i]; let op=Math.max(0,Math.min(1,i/8,(n-1-i)/8,(1010-y)/60));
    const VW={el:[3.3,13.3,0,0,660,1080],n2:[6.0,9.4,1050,30,1900,390]};
    for(const key in VW){const [a,b,x0,y0,x1,y1]=VW[key]; if(t<a||t>b) continue;
      if(x+250>x0&&x-40<x1&&y-110<y1&&y+10>y0){op=0;}}
    if(op>0){ if(shown.some(q=>Math.abs(q-y)<110)) op=0; else shown.push(y); }
    g.setAttribute("opacity",op.toFixed(3)); g.setAttribute("transform",`translate(${x},${y})`);
    $i("lv"+k+"L").setAttribute("x2",(-40+640*Math.min(1,i/14)).toFixed(1));});
};
})();
// ---------------- timeline: slow, steady, drawn on ----------------
tl.set(["#n2","#tt","#sale","#rmkL","#hzL","#rmk","#hz"],{opacity:0},0);
// vellum slides over the footage
tl.fromTo("#vel",{x:1800},{x:0,duration:1.0,ease:"power2.out"},0);
tl.to("#fa .fo",{strokeDashoffset:0,duration:.9,ease:"power1.inOut",stagger:.05},0.45);
tl.to("#fa .fl",{strokeDashoffset:0,duration:1.0,ease:"power2.inOut",stagger:.06},0.7);
tl.to("#fa .fhat",{opacity:.95,duration:.8,stagger:.08},1.7);
tl.fromTo("#g1 line",{attr:{x2:760}},{attr:{x2:0},duration:.7,ease:"power1.inOut",stagger:.08},0.7);
[["#hw1",1.0],["#hw2",1.209],["#hw3",1.69],["#hw4",2.416]].forEach(([s,t])=>tl.fromTo(s,{opacity:0,clipPath:"inset(-20% 0 -30% 100%)"},{opacity:1,clipPath:"inset(-20% 0 -30% 0%)",duration:.42,ease:"power1.out"},t-.06));
tl.fromTo("#vnote",{opacity:0},{opacity:1,duration:.6},1.6);
tl.to("#vel",{x:1900,duration:.95,ease:"power2.in"},3.05);
// sepia elevation sheet
tl.fromTo("#el",{x:-700},{x:0,duration:1.0,ease:"power2.out"},3.25);
tl.fromTo("#elS .dr,#elS .e3,#elS .e2,#elS .gd",{strokeDasharray:1600,strokeDashoffset:1600},{strokeDashoffset:0,duration:1.5,ease:"power1.inOut",stagger:.015},3.7);
tl.fromTo("#elS .nb",{strokeDasharray:800,strokeDashoffset:800},{strokeDashoffset:0,duration:1.0,ease:"power1.inOut",stagger:.15},4.0);
tl.fromTo(["#el .eh","#el .ei"],{opacity:0},{opacity:1,duration:.6,stagger:.2},3.9);
tl.fromTo("#ePh",{strokeWidth:3},{strokeWidth:5,duration:.6},11.0);
tl.to("#el",{x:-700,duration:.9,ease:"power2.in"},12.6);
// trace strip, line 2
tl.fromTo("#n2",{opacity:0,y:-360},{opacity:1,y:0,duration:.8,ease:"power2.out"},5.75);
tl.fromTo("#g2 line",{attr:{x2:800}},{attr:{x2:20},duration:.6,ease:"power1.inOut",stagger:.08},6.0);
tl.fromTo("#n2a",{opacity:0,clipPath:"inset(-20% 0 -30% 100%)"},{opacity:1,clipPath:"inset(-20% 0 -30% 0%)",duration:.8,ease:"power1.out"},6.15);
tl.fromTo("#n2b",{opacity:0,clipPath:"inset(-20% 0 -30% 100%)"},{opacity:1,clipPath:"inset(-20% 0 -30% 0%)",duration:.7,ease:"power1.out"},7.8);
tl.to("#n2",{y:-380,duration:.8,ease:"power2.in"},9.2);
tl.set("#n2",{opacity:0},10.01);
// sky title
tl.set("#tt",{opacity:1},13.1);
tl.fromTo("#g3 line",{attr:{x2:900}},{attr:{x2:0},duration:.7,ease:"power1.inOut",stagger:.08},13.1);
tl.fromTo("#tt1",{opacity:0,clipPath:"inset(-20% 0 -30% 100%)"},{opacity:1,clipPath:"inset(-20% 0 -30% 0%)",duration:.5,ease:"power1.out"},13.25);
tl.fromTo("#tt2",{opacity:0,clipPath:"inset(-20% 0 -30% 100%)"},{opacity:1,clipPath:"inset(-20% 0 -30% 0%)",duration:.8,ease:"power1.out"},13.95);
// penthouse gold + horizon datum
tl.to("#pt .gl2",{strokeDashoffset:0,duration:1.0,ease:"power2.inOut",stagger:.06},14.5);
tl.fromTo("#hz",{opacity:0,attr:{x2:60}},{opacity:1,attr:{x2:S_HZX2},duration:1.4,ease:"power2.inOut"},14.4);
tl.to("#hzL",{opacity:1,duration:.6},15.0);
tl.to(["#rmk","#rmkL"],{opacity:1,duration:.6},15.2);
tl.to("#rmkL",{opacity:0,duration:.4},15.9);
// sales plan + plaque (VO: SEAVIEW 24 at 15.7)
tl.fromTo("#sale",{opacity:1,x:760},{opacity:1,x:0,duration:.9,ease:"power2.out"},15.3);
tl.fromTo("#plq",{opacity:0,scale:.96},{opacity:1,scale:1,duration:.6,ease:"power1.out"},15.65);
tl.fromTo("#sale .sh",{opacity:0},{opacity:1,duration:.5},16.0);
tl.fromTo("#plan .pw,#plan .pwi",{strokeDasharray:2400,strokeDashoffset:2400},{strokeDashoffset:0,duration:1.3,ease:"power1.inOut",stagger:.1},15.9);
tl.fromTo("#plan .pdoor,#plan .pbal",{opacity:0},{opacity:1,duration:.4},16.8);
tl.fromTo("#plan .prm",{opacity:0},{opacity:1,duration:.4,stagger:.08},16.6);
tl.fromTo("#pSea",{strokeDasharray:400,strokeDashoffset:400},{strokeDashoffset:0,duration:.7,ease:"power2.out"},17.0);
tl.fromTo(["#pSeaG","#plan .pwav","#pArr","#plan .plam"],{opacity:0},{opacity:1,duration:.5,stagger:.08},17.3);
tl.fromTo("#sale .sf",{opacity:0},{opacity:1,duration:.5},17.1);
""".replace("S_HZX2", str(HZ[2]))

SPEC = {'theme': 'he_premium',
        'palette': {'acc': GOLD, 'ink': INK, 'lt': CRM, 'panel': 'rgba(90,59,39,.8)', 'sub': SAND},
        'music_vol': 0.55,
        'plate_vol': 0.3,
        'vo_name': 'E8_tower_he_vo',
        'elements': [],
        'html_front': HTML_FRONT,
        'css': CSS,
        'js': JS,
        'assets': assets}
