"""E6_sneaker BESPOKE v2 - "performance lab" language (black / volt, orange only on the shoebox + hot stress).
The shoe is a test specimen on a lab rig:
  * CAD turntable open: the shoe starts as a volt wireframe/edge render in a black CAD viewport (perspective floor grid,
    axis triad) and a render-pass scan wipes it into the real photo.
  * the matted shoe itself is re-rendered through SVG filters (#fWire = edge-detect + mesh + silhouette, #fHeat = banded
    FEA stress map) and masked per frame to the whole shoe, a single layer, or the foam - so the wireframe / heatmap sit
    exactly on the real pixels.
  * data slams are race-timer boards: skewed 7-segment digits that flick through random values and lock ('189 g', '04', '00',
    '87 %'), with the Hebrew word small beside them. No thump/shake hits.
  * exploded assembly: numbered volt balloons on leader lines, each part in turn re-rendered as mesh (foam as FEA map).
  * snap-back: black CAD viewport flash with the whole stack in wireframe.
  * landing: foam heatmap goes blue->red on the 12.72 splash while a force-plate trace (N vs ms) spikes to its peak.
  * end: the end label of an orange GUYAGA shoebox (AERO-01, size run, barcode) with the tagline printed on it.
"""
import random
from pathlib import Path

T = Path(__file__).resolve().parent.parent

K = "#07080A"   # lab black
V = "#D4FF1E"   # volt
O = "#FF5B14"   # box orange / hot
W = "#F2F4EE"

# ------------------------------------------------------------------ 7-segment digits
DW, DH, TH, GP = 100, 180, 18, 3
_h = TH / 2
_xl, _xr, _yt, _ym, _yb = _h, DW - _h, _h, DH / 2, DH - _h


def _hs(x0, x1, y):
    return f"{x0},{y} {x0 + _h},{y - _h} {x1 - _h},{y - _h} {x1},{y} {x1 - _h},{y + _h} {x0 + _h},{y + _h}"


def _vs(x, y0, y1):
    return f"{x},{y0} {x + _h},{y0 + _h} {x + _h},{y1 - _h} {x},{y1} {x - _h},{y1 - _h} {x - _h},{y0 + _h}"


SEG = [_hs(_xl + GP, _xr - GP, _yt), _vs(_xr, _yt + GP, _ym - GP), _vs(_xr, _ym + GP, _yb - GP), _hs(_xl + GP, _xr - GP, _yb),
       _vs(_xl, _ym + GP, _yb - GP), _vs(_xl, _yt + GP, _ym - GP), _hs(_xl + GP, _xr - GP, _ym)]   # a b c d e f g
PITCH = 118


def digits(did, n, scale):
    w, h = (n - 1) * PITCH + DW + 20, DH
    gs = "".join(f'<g class="dg" transform="translate({12 + k * PITCH},0) skewX(-7)">' + "".join(f'<polygon points="{p}"/>' for p in SEG) + "</g>" for k in range(n))
    return f'<svg class="sg" id="{did}" viewBox="0 0 {w} {h}" width="{w * scale:.0f}" height="{h * scale:.0f}" overflow="visible">{gs}</svg>'


# ------------------------------------------------------------------ race-timer boards (data slams)
BOARDS = f'''
<div class="bd" id="bd1" style="left:1496px;top:196px">
  <div class="hd"><span>MASS</span><span>US 9 · SINGLE</span></div>
  <div class="rw">{digits("d1", 3, .86)}<span class="un">g</span></div>
  <div class="he"><b id="w1a">קלה</b> <b id="w1b">כמו</b> <b id="w1c">אוויר</b></div>
</div>
<div class="bd" id="bd2" style="left:34px;top:170px">
  <div class="hd"><span>LAYERS</span><span>STACK TEST</span></div>
  <div class="rw">{digits("d2", 2, .92)}<span class="he2" id="w2a">שכבות</span></div>
  <div class="sep"></div>
  <div class="hd"><span>COMPROMISE</span><span>TOL 0.00</span></div>
  <div class="rw">{digits("d3", 2, .92)}<span class="he2" id="w2b">פשרות</span></div>
</div>
<div class="bd" id="bd3" style="left:1506px;top:262px">
  <div class="hd"><span>ENERGY RETURN</span><span>DROP 10 KG</span></div>
  <div class="rw">{digits("d4", 2, .96)}<span class="un">%</span></div>
  <div class="he">החזר אנרגיה</div>
</div>
'''

# ------------------------------------------------------------------ exploded assembly (balloons + part chips)
PARTS = [(1, "עליון נושם", "KNIT UPPER · 38 g", "r", 450, 236), (2, "קצף תגובתי", "REACTIVE FOAM · 86 g", "l", 1540, 476),
         (3, "לוח קרבון", "CARBON PLATE · 0.9 mm", "l", 1540, 806), (4, "סוליית אחיזה", "WET-GRIP RUBBER · 48 g", "r", 450, 910)]
CHIPS = "".join(
    f'<div class="pc {sd}" id="pc{k}" style="{"left" if sd == "l" else "right"}:{x if sd == "l" else 1920 - x}px;top:{y}px">'
    f'<span class="nm">{nm}</span><span class="sp"><i>{k:02d}</i>{sp}</span>'
    + ('<span class="lg"><em>0.0</em><b></b><em>MPa 2.4</em></span>' if k == 2 else "") + '</div>' for k, nm, sp, sd, x, y in PARTS)
BAL = "".join(f'<g id="b{k}" opacity="0"><path class="ld"/><circle class="dot" r="7"/><g class="bl"><circle r="31"/><text y="11">{k}</text></g></g>' for k in range(1, 5))

# ------------------------------------------------------------------ force plate
FP = '''<div id="fp">
  <div class="hd"><span>GUYAGA LAB · FORCE PLATE FP-2</span><span class="he3">כוח נחיתה</span></div>
  <svg id="fpg" viewBox="0 0 600 190" width="600" height="190">
    <g class="gr"><path d="M56,20H588M56,52H588M56,84H588M56,116H588M56,148H588"/></g>
    <g class="ax"><path d="M56,12V160H588"/><path d="M56,160v6M162,160v6M269,160v6M375,160v6M482,160v6M588,160v6"/></g>
    <g class="tx"><text x="48" y="25" text-anchor="end">2500</text><text x="48" y="89" text-anchor="end">1250</text><text x="48" y="164" text-anchor="end">0 N</text>
      <text x="56" y="184">0</text><text x="162" y="184" text-anchor="middle">50</text><text x="269" y="184" text-anchor="middle">100</text>
      <text x="375" y="184" text-anchor="middle">150</text><text x="482" y="184" text-anchor="middle">200</text><text x="588" y="184" text-anchor="end">250 ms</text></g>
    <path id="fpf" class="fl"/><path id="fpl" class="tr"/><path id="fpc" class="cur"/>
    <g id="fpk" opacity="0"><path class="pk"/><circle r="7"/></g>
  </svg>
  <div class="pkr" id="fpr"><span class="k">PEAK</span>''' + digits("d5", 4, .3) + '''<span class="u">N</span></div>
</div>'''

# ------------------------------------------------------------------ shoebox end label
random.seed(6)
_bars, _x = [], 0
for _ in range(46):
    w = random.choice((2, 2, 3, 4, 6))
    _bars.append(f'<rect x="{_x}" y="0" width="{w}" height="64"/>')
    _x += w + random.choice((2, 3, 4))
BARCODE = f'<svg class="bc" viewBox="0 0 {_x} 64" width="{_x}" height="64" preserveAspectRatio="none">{"".join(_bars)}</svg>'
SIZES = ["7", "7½", "8", "8½", "9", "9½", "10", "10½", "11", "12"]
BOX = f'''<div id="bx"><div class="lid"></div><div class="end">
  <div class="r1"><span class="br">GUYAGA</span><span class="md" id="bxm">AERO-01</span></div>
  <div class="r2"><span class="tgl"><b id="tg1">רצים</b><b id="tg2">על</b><b id="tg3">אוויר</b></span></div>
  <div class="r3"><span class="us">US</span>{"".join(f'<span class="sz{" on" if s == "9" else ""}">{s}</span>' for s in SIZES)}</div>
  <div class="r4">{BARCODE}<span class="cd"><b class="ty">נעל ריצה · לוח קרבון</b><b>WHT / VOLT</b><b>189 g · 8 mm DROP</b><b>7 290117 604190</b></span></div>
</div></div>'''

# ------------------------------------------------------------------ filters (applied to the matted shoe)
GRID = ("data:image/svg+xml;utf8,%3Csvg xmlns='http://www.w3.org/2000/svg' width='26' height='26'%3E%3Cpath d='M0 .5H26M.5 0V26' "
        "stroke='%23D4FF1E' stroke-width='1.2' fill='none'/%3E%3C/svg%3E")
FILTERS = f'''<svg id="fx" width="0" height="0" style="position:absolute">
<filter id="fWire" filterUnits="userSpaceOnUse" primitiveUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080" color-interpolation-filters="sRGB">
  <feFlood flood-color="#000" result="blk"/>
  <feComposite in="SourceGraphic" in2="blk" operator="over" result="op"/>
  <feColorMatrix in="op" type="matrix" values=".3 .59 .11 0 0  .3 .59 .11 0 0  .3 .59 .11 0 0  0 0 0 0 1" result="gray"/>
  <feGaussianBlur in="gray" stdDeviation="1.1" result="gb"/>
  <feConvolveMatrix in="gb" order="3" kernelMatrix="-1 -1 -1 -1 8 -1 -1 -1 -1" preserveAlpha="true" result="edg"/>
  <feColorMatrix in="edg" type="matrix" values="0 0 0 0 .83  0 0 0 0 1  0 0 0 0 .12  9 0 0 0 0" result="edgV"/>
  <feColorMatrix in="gray" type="matrix" values=".05 0 0 0 .008  .12 0 0 0 .016  .04 0 0 0 .006  0 0 0 0 1" result="body"/>
  <feImage href="{GRID}" x="0" y="0" width="26" height="26" result="cell"/>
  <feTile in="cell" result="grid0"/>
  <feColorMatrix in="grid0" type="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 .38 0" result="grid"/>
  <feMerge result="m"><feMergeNode in="body"/><feMergeNode in="grid"/><feMergeNode in="edgV"/></feMerge>
  <feComposite in="m" in2="SourceAlpha" operator="in" result="cut"/>
  <feMorphology in="SourceAlpha" operator="dilate" radius="3" result="dil"/>
  <feComposite in="dil" in2="SourceAlpha" operator="out" result="ring"/>
  <feFlood flood-color="{V}" result="vf"/>
  <feComposite in="vf" in2="ring" operator="in" result="ringV"/>
  <feMerge><feMergeNode in="cut"/><feMergeNode in="ringV"/></feMerge>
</filter>
<filter id="fHeat" filterUnits="userSpaceOnUse" primitiveUnits="userSpaceOnUse" x="0" y="0" width="1920" height="1080" color-interpolation-filters="sRGB">
  <feColorMatrix type="matrix" values=".3 .59 .11 0 0  .3 .59 .11 0 0  .3 .59 .11 0 0  0 0 0 1 0" result="L"/>
  <feComponentTransfer in="L" result="hm"><feFuncR id="hR" type="discrete" tableValues="0"/><feFuncG id="hG" type="discrete" tableValues="0"/><feFuncB id="hB" type="discrete" tableValues="0"/></feComponentTransfer>
  <feComposite in="hm" in2="SourceAlpha" operator="in"/>
</filter>
</svg>'''

# CAD viewport (behind the matted shoe): black, perspective floor grid, horizon, axis triad
VP = f'''<div id="vp"><div class="fl"></div><div class="hz"></div>
<svg class="ax3" viewBox="-12 -104 124 118" width="160" height="152"><path d="M0,0L80,0" stroke="{O}" stroke-width="4"/><path d="M0,0L0,-80" stroke="{V}" stroke-width="4"/>
<path d="M0,0L-38,34" stroke="#7FA8FF" stroke-width="4" transform="translate(40,0)"/><text x="86" y="6">X</text><text x="-6" y="-84">Y</text></svg></div>'''

SVG = f'''<svg id="lab" viewBox="0 0 1920 1080" data-layout-allow-overlap data-layout-allow-occlusion>
<g id="tt" opacity="0"><ellipse class="pl" cx="960" cy="905" rx="560" ry="62"/><ellipse class="pl2" cx="960" cy="905" rx="600" ry="72"/><g id="ttk"></g>
<path id="ttm" class="mk"/><text id="ttx" class="lb" x="960" y="1010" text-anchor="middle"></text></g>
<g id="gap" opacity="0"><path class="br"/><text class="lb" id="g1"></text><text class="lb" id="g2"></text><text class="lb" id="g3"></text></g>
{BAL}
</svg>'''

TIMER = '<div id="tm"><i id="rec"></i><span class="k">RUN 0417</span><span class="v" id="tmv">00:00.00</span></div>'
SCAN = '<div id="scan"></div>'

HTML_FRONT = FILTERS + SVG + SCAN + TIMER + BOARDS + CHIPS + FP + BOX
HTML_BEHIND = VP

CSS = r'''
#flash{display:none}
:root{--k:#07080A;--v:#D4FF1E;--o:#FF5B14;--w:#F2F4EE}
#hud2 #wm{z-index:5}
/* ---- 7-seg */
.sg polygon{fill:rgba(212,255,30,.07)}
.sg polygon.on{fill:var(--v)}
.sg{filter:drop-shadow(0 0 10px rgba(212,255,30,.45))}
/* ---- race-timer boards */
.bd{position:absolute;padding:12px 18px 16px;background:rgba(7,8,10,.9);border-top:5px solid var(--v);opacity:0;
    background-image:repeating-linear-gradient(0deg,rgba(255,255,255,.028) 0 2px,transparent 2px 5px)}
.bd .hd{display:flex;justify-content:space-between;gap:22px;font-family:"Chakra",monospace;font-weight:700;font-size:17px;letter-spacing:.16em;color:var(--v);margin-bottom:10px;direction:ltr;white-space:nowrap}
.bd .hd span:last-child{color:rgba(242,244,238,.55)}
.bd .rw{display:flex;align-items:flex-end;gap:10px;direction:ltr}
.bd .un{font-family:"Chakra",monospace;font-weight:700;font-size:62px;line-height:1;color:var(--v);padding-bottom:4px}
.bd .he{margin-top:12px;font-family:"Rubik",sans-serif;font-weight:800;font-size:44px;line-height:1.05;color:var(--w);direction:rtl;text-align:right;white-space:nowrap}
.bd .he b,.bd .he2{font-weight:800}
.bd .he b{display:inline-block}
.bd .he2{font-family:"Rubik",sans-serif;font-size:40px;line-height:1;color:var(--w);direction:rtl;padding-bottom:6px;margin-left:8px;white-space:nowrap}
.bd .sep{height:2px;background:rgba(212,255,30,.25);margin:16px 0 12px}
/* ---- turntable + gap readouts */
#lab{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}
#lab .pl{fill:none;stroke:var(--v);stroke-width:2.5}
#lab .pl2{fill:none;stroke:rgba(212,255,30,.35);stroke-width:1.5;stroke-dasharray:3 9}
#ttk line{stroke:var(--v);stroke-width:2}
#lab .mk{fill:var(--o)}
#lab .lb{font-family:"Chakra",monospace;font-weight:700;font-size:24px;letter-spacing:.08em;fill:var(--v);paint-order:stroke;stroke:rgba(7,8,10,.92);stroke-width:7px;stroke-linejoin:round}
#gap .br{fill:none;stroke:var(--v);stroke-width:2.5}
#lab .ld{fill:none;stroke:var(--v);stroke-width:2.5}
#lab .dot{fill:var(--k);stroke:var(--v);stroke-width:3}
#lab .bl circle{fill:var(--v);stroke:var(--k);stroke-width:3}
#lab .bl text{font-family:"Chakra",monospace;font-weight:700;font-size:32px;fill:var(--k);text-anchor:middle}
/* ---- part chips */
.pc{position:absolute;display:flex;flex-direction:column;gap:4px;padding:10px 16px 12px;background:rgba(7,8,10,.86);opacity:0}
.pc.l{border-left:5px solid var(--v);align-items:flex-start}
.pc.r{border-right:5px solid var(--v);align-items:flex-end}
.pc .nm{font-family:"Rubik",sans-serif;font-weight:800;font-size:46px;line-height:1.05;color:var(--w);direction:rtl;white-space:nowrap}
.pc .sp{font-family:"Chakra",monospace;font-weight:500;font-size:19px;letter-spacing:.1em;color:rgba(242,244,238,.8);direction:ltr;white-space:nowrap}
.pc .sp i{font-style:normal;font-weight:700;color:var(--v);margin-right:10px}
.pc .lg{display:flex;align-items:center;gap:8px;margin-top:4px;direction:ltr;font-family:"Chakra",monospace;font-weight:700;font-size:14px;color:rgba(242,244,238,.75)}
.pc .lg em{font-style:normal}
.pc .lg b{display:block;width:170px;height:10px;background:linear-gradient(90deg,#1426A8,#0A7BFF,#00D8B0,#C8FF00,#FF9A00,#FF2A10)}
/* ---- CAD viewport (behind the shoe) */
#vp{position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 50% 45%,#11140F,#050605 75%);opacity:0;overflow:hidden}
#vp .fl{position:absolute;left:-40%;width:180%;top:62%;height:90%;transform-origin:50% 0;transform:perspective(620px) rotateX(64deg);
  background-image:linear-gradient(rgba(212,255,30,.55) 2px,transparent 2px),linear-gradient(90deg,rgba(212,255,30,.55) 2px,transparent 2px),
                   linear-gradient(rgba(212,255,30,.2) 1px,transparent 1px),linear-gradient(90deg,rgba(212,255,30,.2) 1px,transparent 1px);
  background-size:240px 240px,240px 240px,48px 48px,48px 48px;background-position:center top}
#vp .hz{position:absolute;left:0;right:0;top:62%;height:2px;background:rgba(212,255,30,.6);box-shadow:0 0 24px rgba(212,255,30,.5)}
#vp .ax3{position:absolute;left:70px;bottom:70px}
#vp .ax3 text{font-family:"Chakra",monospace;font-weight:700;font-size:16px;fill:var(--w)}
/* render-pass scan line */
#scan{position:absolute;top:0;bottom:0;left:0;width:4px;background:var(--v);box-shadow:0 0 18px 4px rgba(212,255,30,.8),0 0 60px 10px rgba(212,255,30,.3);opacity:0}
/* ---- lab timer */
#tm{position:absolute;left:0;right:0;margin:0 auto;top:22px;width:max-content;display:flex;align-items:center;gap:14px;padding:6px 16px;background:rgba(7,8,10,.85);
    font-family:"Chakra",monospace;font-weight:700;direction:ltr;opacity:0}
#tm i{display:block;width:12px;height:12px;border-radius:50%;background:var(--o)}
#tm .k{font-size:16px;letter-spacing:.18em;color:rgba(242,244,238,.7)}
#tm .v{font-size:24px;letter-spacing:.06em;color:var(--v);font-variant-numeric:tabular-nums;min-width:124px}
/* ---- force plate */
#fp{position:absolute;left:36px;top:26px;width:640px;padding:12px 18px 12px;background:rgba(7,8,10,.9);border-top:5px solid var(--v);opacity:0}
#fp .hd{display:flex;justify-content:space-between;align-items:baseline;font-family:"Chakra",monospace;font-weight:700;font-size:16px;letter-spacing:.14em;color:var(--v);direction:ltr}
#fp .he3{font-family:"Rubik",sans-serif;font-weight:800;font-size:30px;letter-spacing:0;color:var(--w);direction:rtl}
#fpg{display:block;margin-top:4px;overflow:visible}
#fpg .gr path{stroke:rgba(212,255,30,.12);stroke-width:1}
#fpg .ax path{fill:none;stroke:rgba(242,244,238,.6);stroke-width:1.5}
#fpg .tx text{font-family:"Chakra",monospace;font-weight:500;font-size:14px;fill:rgba(242,244,238,.7)}
#fpg .tr{fill:none;stroke:var(--v);stroke-width:3.5;stroke-linejoin:round}
#fpg .fl{fill:rgba(212,255,30,.12)}
#fpg .cur{stroke:rgba(242,244,238,.5);stroke-width:1.5}
#fpk circle{fill:var(--o);stroke:var(--k);stroke-width:2}
#fpk .pk{stroke:var(--o);stroke-width:1.5;stroke-dasharray:4 4}
#fp .pkr{position:absolute;right:28px;top:52px;display:flex;align-items:flex-end;gap:6px;direction:ltr;opacity:0;background:rgba(7,8,10,.8);padding:4px 8px}
#fp .pkr .k{font-family:"Chakra",monospace;font-weight:700;font-size:15px;letter-spacing:.16em;color:var(--o);padding-bottom:4px;margin-right:6px}
#fp .pkr .u{font-family:"Chakra",monospace;font-weight:700;font-size:22px;color:var(--v)}
#fp .pkr .sg{filter:drop-shadow(0 0 6px rgba(212,255,30,.5))}
/* ---- shoebox end label */
#bx{position:absolute;right:40px;top:28px;width:740px;opacity:0;transform-origin:100% 50%}
#bx .lid{height:22px;background:linear-gradient(180deg,#B83C08,#D9480C);border-radius:2px 2px 0 0;box-shadow:inset 0 -3px 0 rgba(0,0,0,.25)}
#bx .end{position:relative;padding:12px 20px 16px;background:#FF5B14;color:#0B0B0B;box-shadow:0 22px 60px rgba(0,0,0,.6);
  background-image:repeating-linear-gradient(90deg,rgba(0,0,0,.025) 0 3px,transparent 3px 7px),linear-gradient(180deg,rgba(255,255,255,.08),rgba(0,0,0,.12))}
#bx .r1{display:flex;justify-content:space-between;align-items:flex-end;border-bottom:4px solid #0B0B0B;padding-bottom:4px}
#bx .br{font-family:"Rubik",sans-serif;font-weight:900;font-size:78px;line-height:.9;letter-spacing:-.01em;transform:skewX(-8deg);transform-origin:0 100%}
#bx .md{font-family:"Chakra",monospace;font-weight:700;font-size:46px;line-height:1;letter-spacing:.04em;background:#0B0B0B;color:#FF5B14;padding:4px 12px 2px}
#bx .r2{display:flex;justify-content:flex-start;direction:rtl;padding:6px 0 8px}
#bx .tgl{display:flex;gap:.26em;direction:rtl;font-family:"Rubik",sans-serif;font-weight:900;font-size:70px;line-height:1.05;white-space:nowrap}
#bx .tgl b{display:inline-block;font-weight:900}
#bx .cd .ty{font-family:"Rubik",sans-serif;font-weight:800;font-size:22px;letter-spacing:0;direction:rtl;text-align:left}
#bx .r3{display:flex;align-items:stretch;border:2.5px solid #0B0B0B;direction:ltr}
#bx .r3 span{flex:1;text-align:center;font-family:"Chakra",monospace;font-weight:700;font-size:20px;padding:3px 0;border-left:2px solid #0B0B0B}
#bx .r3 span:first-child{border-left:0;background:#0B0B0B;color:#FF5B14;flex:.9}
#bx .r3 span.on{background:#0B0B0B;color:#FF5B14}
#bx .r4{display:flex;align-items:center;gap:18px;margin-top:10px;direction:ltr}
#bx .bc{display:block;height:64px;width:250px;fill:#0B0B0B}
#bx .cd{display:flex;flex-direction:column;font-family:"Chakra",monospace;font-weight:700;font-size:17px;letter-spacing:.08em;line-height:1.3}
#matte{will-change:filter}
'''

JS = r'''
const cl_ = (v, a, b) => Math.max(a, Math.min(b, v));
const rp = (t, a, d) => cl_((t - a) / d, 0, 1);
const eo = (u) => 1 - Math.pow(1 - u, 3);
const eio = (u) => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
const bo = (u) => { const c1 = 2.2, c3 = c1 + 1; return 1 + c3 * Math.pow(u - 1, 3) + c1 * Math.pow(u - 1, 2); };
const vis = (t, a, b, din = .25, dout = .16) => eo(rp(t, a, din)) * (1 - rp(t, b - dout, dout));
const G = (id) => document.getElementById(id);
const hsh = (n) => { const s = Math.sin(n * 12.9898 + 78.233) * 43758.5453; return s - Math.floor(s); };
// ---------- 7-seg
const MAP = {"0": "abcdef", "1": "bc", "2": "abged", "3": "abgcd", "4": "fgbc", "5": "afgcd", "6": "afgedc", "7": "abc", "8": "abcdefg", "9": "abcdfg", " ": ""};
function setDig(svgId, str, t, t0, dur, seed) {
  const gs = G(svgId).querySelectorAll(".dg");
  const f = Math.floor(t * 30);
  gs.forEach((g, k) => {
    let ch = str[k], on = null;
    if (t < t0) ch = " ";
    else if (t < t0 + dur + k * .05) {
      const r = hsh(f * 3.1 + k * 17 + seed);
      if (r < .25) ch = " "; else ch = String(Math.floor(hsh(f + k * 7 + seed) * 10));
    }
    const segs = MAP[ch] || "";
    g.querySelectorAll("polygon").forEach((p, j) => p.classList.toggle("on", segs.includes("abcdefg"[j])));
  });
}
// ---------- heat ramp (banded FEA)
const HS = [[0, [20, 38, 168]], [.22, [10, 123, 255]], [.42, [0, 216, 176]], [.6, [200, 255, 0]], [.78, [255, 154, 0]], [1, [255, 42, 16]]];
function ramp(v) {
  v = cl_(v, 0, 1);
  for (let i = 1; i < HS.length; i++) if (v <= HS[i][0]) {
    const [a, ca] = HS[i - 1], [b, cb] = HS[i], u = (v - a) / (b - a);
    return ca.map((c, j) => (c + (cb[j] - c) * u) / 255);
  }
  return HS[HS.length - 1][1].map(c => c / 255);
}
let _lastS = -1;
function setHeat(s) {
  s = Math.round(s * 100) / 100; if (s === _lastS) return; _lastS = s;
  const n = 10, R = [], Gc = [], B = [];
  for (let k = 0; k < n; k++) { const v = ((k + .5) / n) * s * 1.1, c = ramp(v); R.push(c[0].toFixed(3)); Gc.push(c[1].toFixed(3)); B.push(c[2].toFixed(3)); }
  G("hR").setAttribute("tableValues", R.join(" ")); G("hG").setAttribute("tableValues", Gc.join(" ")); G("hB").setAttribute("tableValues", B.join(" "));
}
// ---------- matte re-render state
function setMatte(mode, op, mask) {
  const m = G("matte"); if (!m) return;
  m.style.filter = mode === "wire" ? "url(#fWire)" : mode === "heat" ? "url(#fHeat)" : "none";
  m.style.opacity = mode === "none" ? 1 : op;
  const mi = mode === "none" ? "none" : (mask || "none");
  m.style.webkitMaskImage = mi; m.style.maskImage = mi;
}
const boxMask = (b, p) => `linear-gradient(180deg, transparent ${b[1] - p}px, #000 ${b[1] + p * .2}px, #000 ${b[3] - p * .2}px, transparent ${b[3] + p}px)`;
const radMask = (cx, cy, rx, ry) => `radial-gradient(ellipse ${rx}px ${ry}px at ${cx}px ${cy}px, #000 55%, transparent 100%)`;
// ---------- force plate trace
const FPK = [[0, 0], [40, 20], [62, 140], [72, 900], [80, 2140], [88, 1500], [100, 1120], [125, 1380], [155, 1640], [185, 1300], [215, 620], [238, 160], [250, 0]];
function force(ms) {
  if (ms <= 0) return 0;
  for (let i = 1; i < FPK.length; i++) if (ms <= FPK[i][0]) {
    const [a, fa] = FPK[i - 1], [b, fb] = FPK[i], u = (ms - a) / (b - a), s = (1 - Math.cos(Math.PI * u)) / 2;
    return fa + (fb - fa) * s;
  }
  return 0;
}
const fx = (ms) => 56 + ms / 250 * 532, fy = (F) => 160 - F / 2500 * 140;
const BALS = [[1, "a_upper", 395, 178, 4.9], [2, "a_mid", 1590, 424, 6.1], [3, "a_plate", 1590, 754, 7.3], [4, "a_out", 395, 860, 8.25]];
const _p0 = window.onPlace;
window.onPlace = (t) => {
  _p0 && _p0(t);
  const sh = boxAt("shoe", t);
  // ---- lab timer
  { const cs = Math.floor(t * 100), s = Math.floor(cs / 100), c = cs % 100;
    G("tmv").textContent = `00:${String(s).padStart(2, "0")}.${String(c).padStart(2, "0")}`;
    G("rec").style.opacity = Math.floor(t * 2.5) % 2 ? .25 : 1; }
  // ---- render-pass scan (0.95-1.75): CAD right of the line, photo left of it
  const X = t < .95 ? -40 : 1980 * eio(rp(t, .95, .8));
  G("scan").style.transform = `translateX(${X}px)`;
  G("scan").style.opacity = t > .93 && t < 1.78 ? 1 : 0;
  { const vp = G("vp");
    let o = 0, clip = "none";
    if (t < 1.78) { o = 1; clip = t < .95 ? "none" : `inset(0 0 0 ${X}px)`; }
    else if (t > 9.5 && t < 10.2) o = t < 9.58 ? eo(rp(t, 9.5, .08)) : 1 - eo(rp(t, 9.86, .32));
    vp.style.opacity = o; vp.style.clipPath = clip; }
  // ---- matte: wireframe / FEA re-render
  {
    const mid = boxAt("midsole", t);
    if (t < 1.78) setMatte("wire", 1, t < .95 ? "linear-gradient(#000,#000)" : `linear-gradient(90deg, transparent ${X}px, #000 ${X + 3}px)`);
    else if (t > 2.62 && t < 4.7) setMatte("wire", eo(rp(t, 2.62, .22)) * (1 - rp(t, 4.46, .22)), "linear-gradient(#000,#000)");
    else if (t > 4.88 && t < 6.06) setMatte("wire", vis(t, 4.88, 6.06, .15, .15), boxMask(boxAt("upper", t), 30));
    else if (t > 6.08 && t < 7.26) { setHeat(.34 + .28 * Math.sin(Math.PI * rp(t, 6.2, .9))); setMatte("heat", vis(t, 6.08, 7.26, .15, .15), boxMask(boxAt("midsole", t), 18)); }
    else if (t > 7.28 && t < 8.22) setMatte("wire", vis(t, 7.28, 8.22, .15, .15), boxMask(boxAt("plate", t), 18));
    else if (t > 8.23 && t < 9.46) setMatte("wire", vis(t, 8.23, 9.46, .15, .15), boxMask(boxAt("outsole", t), 26));
    else if (t > 9.5 && t < 10.2) setMatte("wire", t < 9.58 ? 1 : 1 - eo(rp(t, 9.86, .32)), "linear-gradient(#000,#000)");
    else if (t > 12.28 && t < 14.3) {
      const s = t < 12.6 ? .3 : t < 12.76 ? .3 + .75 * eo(rp(t, 12.6, .16)) : 1.05 - .5 * eo(rp(t, 12.76, .9));
      setHeat(s);
      const cx = (mid[0] + mid[2]) / 2, cy = mid[1] + (mid[3] - mid[1]) * .38;
      setMatte("heat", vis(t, 12.28, 14.3, .18, .4) * .95, radMask(cx, cy, (mid[2] - mid[0]) * .58, (mid[3] - mid[1]) * .58));
    }
    else setMatte("none");
  }
  // ---- turntable under the spinning shoe
  {
    const f = vis(t, .05, 2.05, .3, .2), g = G("tt");
    g.setAttribute("opacity", f);
    if (f > 0) {
      const th = 360 * eo(rp(t, .1, 2.2));
      let d = "";
      for (let k = 0; k < 36; k++) {
        const a = (k * 10 + th) * Math.PI / 180, x = 960 + 560 * Math.cos(a), y = 905 + 62 * Math.sin(a);
        if (Math.sin(a) < -.2) continue;
        const L = k % 9 === 0 ? 22 : 10;
        d += `<line x1="${x}" y1="${y}" x2="${x}" y2="${y + L}"/>`;
      }
      G("ttk").innerHTML = d;
      const a = (th + 90) * Math.PI / 180, mx = 960 + 560 * Math.cos(a), my = 905 + 62 * Math.sin(a);
      G("ttm").setAttribute("d", `M${mx},${my - 4}L${mx - 12},${my + 18}L${mx + 12},${my + 18}Z`);
      G("ttx").textContent = `TURNTABLE  θ ${String(Math.round(th)).padStart(3, "0")}°   ω 2.5 rev/s`;
    }
  }
  // ---- 7-seg boards
  setDig("d1", "189", t, .4, .42, 1);
  setDig("d2", "04", t, 2.1, .38, 2);
  setDig("d3", "00", t, 3.354, .3, 3);
  setDig("d4", "87", t, 10.25, .66, 4);
  setDig("d5", String(Math.round(Math.max(...[0, 20, 40, 60, 70, 76, 80].map(m => m <= (t - 12.4) * 250 ? force(m) : 0)))).padStart(4, " "), t, 12.66, 0, 5);
  // ---- live layer gaps during the separation
  {
    const f = vis(t, 2.9, 4.62, .25, .16), g = G("gap");
    g.setAttribute("opacity", f);
    if (f > 0) {
      const Ls = ["upper", "midsole", "plate", "outsole"].map(n => boxAt(n, t));
      const Xr = Math.max(...Ls.map(b => b[2])) + 34, Y = Ls.map(b => (b[1] + b[3]) / 2);
      const Y0 = ["upper", "midsole", "plate", "outsole"].map(n => { const b = boxAt(n, 2.6); return (b[1] + b[3]) / 2; }), base = [0, 1, 2].map(k => Y0[k + 1] - Y0[k]);
      g.children[0].setAttribute("d", Y.map((y, k) => `M${Xr - 14},${y}H${Xr}` + (k < 3 ? `V${Y[k + 1] - 6}M${Xr},${Y[k + 1] - 6}` : "")).join(""));
      for (let k = 0; k < 3; k++) {
        const el = G("g" + (k + 1)), gap = Math.max(0, (Y[k + 1] - Y[k]) - base[k]) * .21 + .4;
        el.textContent = `+${gap.toFixed(1)} mm`;
        el.setAttribute("x", Xr + 14); el.setAttribute("y", (Y[k] + Y[k + 1]) / 2 + 8);
      }
    }
  }
  // ---- exploded-assembly balloons (retract into the part on the snap-back)
  for (const [k, nm, bx, by, t0] of BALS) {
    const g = G("b" + k);
    if (t < t0 - .02 || t > 9.64) { g.setAttribute("opacity", 0); continue; }
    g.setAttribute("opacity", 1);
    const a = anchor(boxAt(nm, t), "c"), r = eo(rp(t, 9.42, .2));
    const Xb = bx + (a[0] - bx) * r, Yb = by + (a[1] - by) * r;
    const p = eo(rp(t, t0, .2)), ex = a[0] + (Xb - a[0]) * p, ey = a[1] + (Yb - a[1]) * p;
    const L = Math.hypot(ex - a[0], ey - a[1]) || 1, stop = Math.max(0, L - 31 * (1 - r));
    const [ld, dot, bl] = g.children;
    ld.setAttribute("d", `M${a[0]},${a[1]}L${a[0] + (ex - a[0]) * stop / L},${a[1] + (ey - a[1]) * stop / L}`);
    dot.setAttribute("cx", a[0]); dot.setAttribute("cy", a[1]); dot.setAttribute("r", 7 * (1 - r));
    const s = Math.max(0, bo(rp(t, t0 + .08, .26))) * (1 - r);
    bl.setAttribute("transform", `translate(${Xb},${Yb}) scale(${s})`);
  }
  // ---- force plate trace (t 12.40 -> 13.40 = 0 -> 250 ms)
  {
    const ms = cl_((t - 12.4) * 250, 0, 250);
    let d = `M${fx(0)},${fy(force(0))}`;
    for (let m = 2; m <= ms; m += 2) d += `L${fx(m)},${fy(force(m))}`;
    d += `L${fx(ms)},${fy(force(ms))}`;
    G("fpl").setAttribute("d", d);
    G("fpf").setAttribute("d", d + `L${fx(ms)},160L56,160Z`);
    G("fpc").setAttribute("d", ms > 0 && ms < 250 ? `M${fx(ms)},12V160` : "");
    const pk = G("fpk");
    pk.setAttribute("opacity", ms >= 80 ? 1 : 0);
    pk.children[0].setAttribute("d", `M${fx(80)},${fy(2140)}H588`);
    pk.children[1].setAttribute("cx", fx(80)); pk.children[1].setAttribute("cy", fy(2140));
  }
};
// ---------------- GSAP entrances / exits (race-board flip: clip down + slight skew settle)
function board(sel, t0, t1) {
  tl.fromTo(sel, {opacity: 0, clipPath: "inset(0 0 100% 0)", y: -14}, {opacity: 1, clipPath: "inset(0 0 0% 0)", y: 0, duration: .18, ease: "expo.out"}, t0);
  if (t1) tl.to(sel, {opacity: 0, clipPath: "inset(0 0 100% 0)", duration: .14, ease: "power2.in"}, t1 - .14);
}
function word(sel, at) { tl.fromTo(sel, {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .16, ease: "expo.out"}, at); }
tl.fromTo("#tm", {opacity: 0}, {opacity: 1, duration: .3}, .1);
tl.to("#tm", {opacity: 0, duration: .2}, 12.1);
board("#bd1", .32, 2.02);
word("#w1a", .4); word("#w1b", .609); word("#w1c", .98);
board("#bd2", 2.02, 4.58);
tl.set(["#w2a", "#w2b"], {opacity: 0}, 0);
word("#w2a", 2.704); word("#w2b", 3.656);
board("#bd3", 10.2, 12.26);
''' + "\n".join(
    f'tl.fromTo("#pc{k}", {{opacity:0, clipPath:"inset(0 {"0 0 100%" if sd == "r" else "100% 0 0"})"}}, {{opacity:1, clipPath:"inset(0 0 0 0%)", duration:.22, ease:"expo.out"}}, {t0 + .12});'
    f'tl.to("#pc{k}", {{opacity:0, duration:.12}}, 9.4);'
    for (k, nm, sp, sd, x, y), t0 in zip(PARTS, (4.9, 6.1, 7.3, 8.25))) + r'''
// force plate + peak
tl.fromTo("#fp", {opacity: 0, clipPath: "inset(0 0 100% 0)"}, {opacity: 1, clipPath: "inset(0 0 0% 0)", duration: .22, ease: "expo.out"}, 12.24);
tl.fromTo("#fp .pkr", {opacity: 0}, {opacity: 1, duration: .08}, 12.68);
tl.fromTo("#fp .pkr", {scale: 1.25}, {scale: 1, duration: .25, ease: "back.out(3)", immediateRender: false}, 12.72);
// shoebox end label slides in from the shelf; tagline printed word by word
tl.fromTo("#bx", {opacity: 0, x: 760, rotateY: -28, transformPerspective: 900}, {opacity: 1, x: 0, rotateY: 0, duration: .42, ease: "expo.out"}, 13.02);
tl.set(["#tg1", "#tg2", "#tg3"], {opacity: 0}, 0);
tl.fromTo("#bxm", {opacity: 0, scale: 1.3}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, 13.136);
word("#tg1", 13.75); word("#tg2", 14.214); word("#tg3", 14.423);
'''

SPEC = {
    "theme": "he_bold",
    "palette": {"acc": V, "ink": K, "lt": W, "panel": "rgba(7,8,10,.86)", "sub": "#C9CFC0"},
    "music_vol": 0.6,
    "plate_vol": 0.45,
    "vo_name": "E6_sneaker_he_vo",
    "fonts": {"Chakra": [("chakra-petch-latin-500-normal", 500, "normal"), ("chakra-petch-latin-700-normal", 700, "normal")]},
    "css": CSS,
    "html_front": HTML_FRONT,
    "html_behind": HTML_BEHIND,
    "js": JS,
    "elements": [],
}
