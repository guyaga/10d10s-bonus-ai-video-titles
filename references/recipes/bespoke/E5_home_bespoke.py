"""E5_home BESPOKE - "LUMA HOME, issue 05": the drone flight is shot for an interior-design magazine.

Visual language (only this ad uses it):
  * masthead + issue line + page folios, as if the footage were the photo on a printed spread
  * magazine product credits: a circled number pinned on each piece, a thin leader line to a shopping-page credit
    ('01 · כורסת עור · $2,050 · luma.co.il'); the same circled numbers key the price-list column
  * editor's red-pencil loops drawn around pieces, a pencil arrow + handwritten margin note for the drone
  * the running total is a printed price-list COLUMN bleeding off the left page edge (dotted leaders, rules)
  * print texture: halftone screen + paper grain over the photo, a gutter shadow down the spread, a curled page corner
  * a torn sticky note with the editor's comment slapped on the pull-quote page
  * an editorial page folds open on its spine for the pull-quote, a final page folds in for the total + colophon
Type: Frank Ruhl Libre (Hebrew magazine serif) + Heebo Light captions + Amatic SC for the pencil note.
Motion: soft fades, slides and page folds only. No stomps, no shakes, no flashes.
"""
import math
from pathlib import Path

import numpy as np
from PIL import Image

R = Path(__file__).resolve().parent.parent.parent
FONTS = R / "shared/fonts"

HE = "U+0590-05FF,U+FB1D-FB4F,U+200C-2010,U+20AA,U+25CC"
LA = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2199,U+2212,U+2215"
FACES, ASSETS = [], {}
for fam, slug, weights in (("Frank Ruhl Libre", "frank-ruhl-libre", (500, 700, 900)), ("Heebo", "heebo", (300, 400, 500)),
                           ("Amatic SC", "amatic-sc", (700,))):
    for w in weights:
        for sub, ur in (("hebrew", HE), ("latin", LA)):
            stem = f"{slug}-{sub}-{w}-normal"
            ASSETS[f"fonts/{stem}.woff2"] = str(FONTS / f"{stem}.woff2")
            FACES.append(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;'
                         f'src:url(assets/fonts/{stem}.woff2) format("woff2");unicode-range:{ur}}}')

# paper grain tile (deterministic, generated once)
GRAIN = Path(__file__).resolve().parent.parent / "E5_home_grain.png"
if not GRAIN.exists():
    rng = np.random.default_rng(505)
    g = np.abs(rng.normal(0, 1, (512, 512))) * 16 + np.abs(rng.normal(0, 1, (512, 512))).cumsum(1) % 3
    Image.fromarray(np.clip(255 - g, 150, 255).astype(np.uint8), "L").save(GRAIN)
ASSETS["E5_home_grain.png"] = str(GRAIN)

# (id, title, price, obj, marker fx, marker fy, caption dx, caption dy, t, end)
PIECES = [
    ("01", "כורסת עור", 2050, "chair", .30, .22, -150, -170, 0.35, 1.85),
    ("02", "שולחן טרוורטין", 1650, "table", .45, .25, -130, -200, 2.05, 3.62),
    ("03", "שטיח קלוע ביד", 1100, "rug", .62, .62, -120, -160, 3.55, 5.12),
    ("04", "ספת בוקלה", 3900, "sofa", .62, .45, 120, 190, 5.15, 6.5),
    ("05", "מנורת פליז", 950, "lamp", .50, .90, -120, 150, 12.62, 14.35),
    ("06", "עץ זית", 290, "tree", .55, .50, -150, 220, 13.25, 14.35),
]
assert sum(p[2] for p in PIECES) == 9940
money = lambda v: f"${v:,}"  # noqa: E731

# hand-drawn pencil loop in unit space: ~1.12 turns, wobbling radius, drifting outward so the stroke overshoots its start
pts = []
N = 90
for i in range(N + 1):
    u = i / N
    a = -2.2 + u * 2 * math.pi * 1.12
    r = 1 + .035 * math.sin(3 * a + 1.3) + .025 * math.sin(5 * a + .4) + .07 * u
    pts.append((round(math.cos(a) * r, 4), round(math.sin(a) * r, 4)))
LOOP = str(pts).replace("(", "[").replace(")", "]")

# ---------------------------------------------------------------- markup
credits = "".join(
    f'<div class="mk" id="mk{k}">{n}</div>'
    f'<div class="cr" id="cr{k}"><b class="cn">{n}</b><b class="dt">·</b><b class="cq">{title}</b><b class="dt">·</b>'
    f'<b class="cp">{money(price)}</b><b class="dt">·</b><b class="cu">luma.co.il</b></div>'
    for k, (n, title, price, *_rest) in enumerate(PIECES))
leads = "".join(f'<path id="lh{k}" class="lh"/><path id="ld{k}" class="lk"/>' for k in range(len(PIECES)))

rows = "".join(
    f'<div class="row" id="rw{k}"><span class="rn">{n}</span><span class="rt">{title}</span><span class="ld"></span>'
    f'<span class="rp">{money(price)}</span></div>' for k, (n, title, price, *_r) in enumerate(PIECES))
rows_fin = "".join(
    f'<div class="row"><span class="rn">{n}</span><span class="rt">{title}</span><span class="ld"></span>'
    f'<span class="rp">{money(price)}</span></div>' for (n, title, price, *_r) in PIECES)

HTML = f"""
<div id="ht"></div>
<div id="gut"></div>
<div id="mast"><div class="mt">LUMA<span>HOME</span></div><div class="mr"></div>
  <div class="ms"><span>גיליון 05</span><i>·</i><span>סתיו 2026</span><i>·</i><span>מיוחד: חדר הים</span></div></div>
<div id="fol-r" class="fol">חדר הים &nbsp;|&nbsp; 15</div>
<svg id="pencil" viewBox="0 0 1920 1080" width="1920" height="1080">
  <defs><filter id="graph" x="-5%" y="-5%" width="110%" height="110%">
    <feTurbulence type="fractalNoise" baseFrequency=".85" numOctaves="2" seed="7" result="n"/>
    <feDisplacementMap in="SourceGraphic" in2="n" scale="3.2"/></filter></defs>
  <g filter="url(#graph)">
    <path id="c0a" class="pc"/><path id="c0b" class="pc2"/>
    <path id="c1a" class="pc"/><path id="c1b" class="pc2"/>
    <path id="c2a" class="pc"/><path id="c2b" class="pc2"/>
    <path id="c3a" class="pc"/><path id="c3b" class="pc2"/>
    <path id="arw" class="pc"/><path id="arh" class="pc"/><path id="nul" class="pc"/>
  </g>
</svg>
<svg id="lead" viewBox="0 0 1920 1080" width="1920" height="1080">{leads}</svg>
{credits}
<div id="side"><div class="sk">LUMA HOME · עמ׳ 14</div><div class="sh">המחירון</div><div class="ss">חדר הים, פריט אחר פריט</div>
  <div class="rl"></div>{rows}<div class="rl2"></div>
  <div class="tot"><span class="tlab">החדר עד עכשיו</span><span class="tv" id="tv">$0</span></div>
  <div id="fol-l" class="fol">14 &nbsp;|&nbsp; LUMA HOME</div><i class="crule"></i></div>
<div id="note"><span class="nt"><b id="n0">הרחפן</b> <b id="n1">מוביל</b> <b id="n2">את</b> <b id="n3">הסיור</b></span><span class="ns">LUMA DRONE · מדריך הסיור</span></div>
<div id="pg"><div class="pgin">
  <div class="kk">מדור עיצוב · עמ׳ 15</div>
  <div class="qm">”</div>
  <div class="hl"><span id="q0">כל</span> <span id="q1">פריט,</span><br><span id="q2">עם</span> <span id="q3" class="ac">המחיר</span> <span id="q4">שלו.</span></div>
  <div class="hr" id="hrB"></div>
  <div class="dk"><span id="d0">בלי הפתעות.</span><br><span id="d1" class="ac">בלי לנחש.</span></div>
  <div class="by">צילום: LUMA DRONE · טיסה אחת, בלי קאט</div>
  <div class="pf">15</div>
</div><i class="spine"></i>
  <div id="stk"><div class="s1">מושלם.</div><div class="s2">ישר לדפוס!</div><div class="s3">— העורכת</div></div></div>
<div id="fin"><div class="fnin">
  <div class="kk">LUMA HOME · גיליון 05 · עמ׳ 16</div>
  <div class="fh"><span id="f0">כל</span> <span id="f1">החדר</span></div>
  <div class="fl">{rows_fin}</div>
  <div class="dr"></div>
  <div class="ft" id="ftot">$9,940</div>
  <div class="fs" id="fsub">שישה פריטים. מחיר אחד.</div>
  <div class="col" id="col"><div class="cl1">LUMA HOME</div><div class="cl2">קונים את כל החדר</div></div>
</div><i class="spine"></i></div>
<div id="curl"><i class="under"></i><i class="flap"></i></div>
<div id="grain"></div>
"""

CSS = "".join(FACES) + """
:root{--paper:#f5efe4;--paper2:#ece3d3;--ink:#1f1a15;--pen:#ad3f26;--grey:#6d6358}
#flash{display:none}
.SER{font-family:"Frank Ruhl Libre",serif}
#stage2>*{direction:rtl}
/* spread gutter shading - subtle fold down the middle of the photo */
#gut{position:absolute;left:900px;top:0;width:120px;height:1080px;opacity:0;
  background:linear-gradient(90deg,rgba(40,28,15,0),rgba(40,28,15,.10) 30%,rgba(30,20,10,.34) 49%,rgba(255,250,240,.20) 52%,rgba(40,28,15,.08) 66%,rgba(40,28,15,0))}
/* masthead */
#mast{position:absolute;left:0;right:0;top:34px;display:flex;flex-direction:column;align-items:center;gap:8px}
#mast .mt{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:150px;line-height:.9;color:var(--ink);direction:ltr;letter-spacing:.02em;
  text-shadow:0 0 30px rgba(250,244,232,.55),0 0 8px rgba(250,244,232,.5)}
#mast .mt span{font-weight:500;font-size:60px;letter-spacing:.32em;margin-left:18px;vertical-align:.95em}
#mast .mr{width:760px;height:0;border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding-top:4px;transform-origin:50% 50%}
#mast .ms{display:flex;gap:18px;font-family:"Heebo",sans-serif;font-weight:500;font-size:25px;letter-spacing:.06em;color:var(--ink);
  text-shadow:0 0 10px rgba(250,244,232,.9),0 0 3px rgba(250,244,232,.9)}
#mast .ms i{font-style:normal;color:var(--ink)}
/* folios */
.fol{position:absolute;bottom:34px;background:rgba(245,239,228,.92);padding:6px 14px 5px;font-family:"Heebo",sans-serif;font-weight:500;font-size:22px;letter-spacing:.14em;color:var(--ink);
  text-shadow:0 0 8px rgba(250,244,232,.95),0 0 3px rgba(250,244,232,.95);white-space:nowrap}
#fol-l{direction:ltr}#fol-r{right:180px}
/* pencil */
#pencil{position:absolute;inset:0}
.pc{fill:none;stroke:var(--pen);stroke-width:5.5;stroke-linecap:round;stroke-linejoin:round;opacity:.92}
.pc2{fill:none;stroke:var(--pen);stroke-width:2.5;stroke-linecap:round;opacity:.45}
/* print texture: halftone screen over the photo, paper grain over everything */
#ht{position:absolute;inset:0;opacity:.16;mix-blend-mode:multiply;
  background-image:radial-gradient(circle at 50% 50%,rgba(31,26,21,.9) 0 1.05px,rgba(31,26,21,0) 1.7px);background-size:5px 5px}
#grain{position:absolute;inset:0;background:url(assets/E5_home_grain.png) repeat;background-size:512px 512px;mix-blend-mode:multiply;opacity:.5}
/* curled page corner, bottom right of the spread */
#curl{position:absolute;right:0;bottom:0;width:150px;height:150px;opacity:0}
#curl .under{position:absolute;inset:0;background:#221c16;clip-path:polygon(100% 0,100% 100%,0 100%)}
#curl .flap{position:absolute;inset:0;clip-path:polygon(0 0,100% 0,0 100%);
  background:linear-gradient(135deg,#d8cbb3 0%,#f3ecdf 38%,#fbf7ef 48%,#e1d5bf 100%)}
#curl::before{content:"";position:absolute;left:-20px;top:-20px;width:190px;height:190px;
  background:linear-gradient(135deg,rgba(0,0,0,0) 44%,rgba(25,16,8,.34) 50%,rgba(0,0,0,0) 58%);clip-path:polygon(0 0,100% 0,0 100%)}
/* magazine product credits: circled number on the piece + leader line + shopping-page credit */
#lead{position:absolute;inset:0}
.lk{fill:none;stroke:var(--ink);stroke-width:1.8;stroke-linejoin:round}
.lh{fill:none;stroke:rgba(250,245,235,.8);stroke-width:6;stroke-linecap:round;stroke-linejoin:round}
.mk{position:absolute;left:0;top:0;width:38px;height:38px;margin:-19px 0 0 -19px;border-radius:50%;background:var(--paper);border:2px solid var(--pen);box-sizing:border-box;
  color:#8a2c18;font-family:"Heebo",sans-serif;font-weight:700;font-size:16px;display:flex;align-items:center;justify-content:center;direction:ltr;
  box-shadow:0 0 0 3px rgba(250,245,235,.55),0 3px 10px rgba(30,20,10,.35);opacity:0}
.cr{position:absolute;left:0;top:0;display:block;white-space:nowrap;line-height:1.1;background:rgba(246,241,231,.96);padding:10px 20px 8px;
  color:var(--ink);direction:rtl;border-top:1px solid rgba(31,26,21,.5);border-bottom:2px solid var(--ink);opacity:0;box-shadow:0 6px 18px rgba(30,20,10,.22)}
.cr .cn{font-family:"Heebo",sans-serif;font-weight:700;font-size:17px;color:#8a2c18;letter-spacing:.1em;direction:ltr;unicode-bidi:isolate}
.cr b{display:inline-block;vertical-align:baseline}
.cr .dt{font-weight:400;color:var(--grey);font-family:"Heebo",sans-serif;font-size:20px;margin:0 10px}
.cr .cq{font-family:"Frank Ruhl Libre",serif;font-weight:700;font-size:33px;line-height:1}
.cr .cp{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:35px;line-height:1;direction:ltr;unicode-bidi:isolate}
.cr .cu{font-family:"Heebo",sans-serif;font-weight:500;font-size:17px;letter-spacing:.1em;color:#463d34;direction:ltr;unicode-bidi:isolate}
/* torn sticky note with the editor's comment */
#stk{position:absolute;left:36px;top:650px;width:270px;box-sizing:border-box;padding:40px 22px 26px;background:linear-gradient(170deg,#f6e27e,#efd35e);color:#233a78;text-align:center;
  transform:rotate(-5deg);transform-origin:50% 0;filter:drop-shadow(0 10px 14px rgba(40,30,10,.3));
  clip-path:polygon(0 7%,4% 3%,9% 6%,14% 1%,19% 5%,25% 2%,31% 6%,37% 1%,43% 4%,49% 0,55% 5%,61% 2%,67% 6%,73% 1%,79% 4%,85% 0,91% 5%,96% 2%,100% 6%,100% 100%,0 100%)}
#stk div{font-family:"Amatic SC",sans-serif;font-weight:700;line-height:.95}
#stk .s1{font-size:66px}#stk .s2{font-size:58px}#stk .s3{font-size:38px;margin-top:10px;text-align:left;padding-left:8px}
/* price-list sidebar */
#side{position:absolute;left:0;top:0;width:500px;height:1080px;box-sizing:border-box;padding:64px 44px 0 40px;background:var(--paper);color:var(--ink);
  border-top:14px solid var(--ink);box-shadow:inset -10px 0 18px -10px rgba(60,40,20,.25)}
#side .crule{position:absolute;right:0;top:0;width:3px;height:100%;border-left:1px solid var(--ink);border-right:1px solid var(--ink);box-sizing:border-box}
#side .fol{left:40px;bottom:34px;background:none;padding:0;text-shadow:none}
#side .sk,.kk{font-family:"Heebo",sans-serif;font-weight:400;font-size:17px;letter-spacing:.2em;color:var(--pen)}
#side .sh{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:84px;line-height:1;margin-top:14px}
#side .ss{font-family:"Heebo",sans-serif;font-weight:300;font-size:23px;margin-top:8px;color:var(--grey)}
#side .rl,.dr{height:0;border-top:1px solid var(--ink);margin:18px 0 6px}
#side .rl2{height:0;border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding-top:3px;margin:14px 0 12px}
.row{display:flex;align-items:baseline;gap:12px;height:62px;font-family:"Frank Ruhl Libre",serif}
.row .rn{align-self:center;flex:none;width:30px;height:30px;border-radius:50%;border:1.5px solid var(--pen);box-sizing:border-box;display:flex;align-items:center;justify-content:center;font-family:"Heebo",sans-serif;font-weight:500;font-size:13px;color:var(--pen);direction:ltr}
.row .rt{font-weight:700;font-size:30px;white-space:nowrap}
.row .ld{flex:1;border-bottom:2px dotted rgba(31,26,21,.4);transform:translateY(-6px)}
.row .rp{font-weight:900;font-size:30px;direction:ltr}
#side .tot{display:flex;align-items:baseline;justify-content:space-between}
#side .tlab{font-family:"Heebo",sans-serif;font-weight:400;font-size:21px;color:var(--grey)}
#side .tv{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:76px;line-height:1;direction:ltr;font-variant-numeric:tabular-nums}
/* drone margin note */
#note{position:absolute;left:90px;top:96px;width:660px;display:flex;flex-direction:column;align-items:flex-start}
#note .nt{font-family:"Amatic SC",sans-serif;font-weight:700;font-size:112px;line-height:1;color:var(--pen);white-space:nowrap;
  text-shadow:0 0 14px rgba(252,247,238,.95),0 0 4px rgba(252,247,238,.95)}
#note .nt b{display:inline-block;font-weight:700}
#note .ns{font-family:"Heebo",sans-serif;font-weight:500;font-size:20px;letter-spacing:.16em;color:var(--ink);margin-top:26px;
  text-shadow:0 0 8px rgba(252,247,238,.95),0 0 3px rgba(252,247,238,.95)}
/* editorial page */
#pg,#fin{position:absolute;top:0;height:1080px;background:var(--paper);color:var(--ink)}
#pg{left:1200px;width:720px;transform-origin:0 50%;box-shadow:-18px 0 40px rgba(35,24,12,.3)}
#fin{left:0;width:780px;transform-origin:0 50%;box-shadow:18px 0 40px rgba(35,24,12,.3)}
#pg .spine{position:absolute;left:0;top:0;width:70px;height:100%;background:linear-gradient(90deg,rgba(60,40,20,.28),rgba(60,40,20,0))}
#fin .spine{position:absolute;right:0;top:0;width:70px;height:100%;background:linear-gradient(270deg,rgba(60,40,20,.22),rgba(60,40,20,0))}
.pgin{position:absolute;inset:110px 84px 90px 110px;display:flex;flex-direction:column;align-items:flex-start;text-align:right}
.qm{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:230px;line-height:.6;color:var(--pen);margin-top:40px;height:110px}
.hl{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:112px;line-height:1.08;margin-top:10px}
.hl span,.dk span,.fh span{display:inline-block}
.ac{color:var(--pen)}
.hr{width:120px;height:0;border-top:3px solid var(--ink);margin:44px 0 30px}
.dk{font-family:"Frank Ruhl Libre",serif;font-weight:500;font-size:62px;line-height:1.2}
.by{font-family:"Heebo",sans-serif;font-weight:300;font-size:20px;letter-spacing:.06em;color:var(--grey);margin-top:auto}
.pf{font-family:"Frank Ruhl Libre",serif;font-weight:700;font-size:26px;position:absolute;left:0;bottom:-40px}
.fnin{position:absolute;inset:86px 96px 70px 96px;display:flex;flex-direction:column;align-items:stretch;text-align:right}
.fh{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:128px;line-height:1;margin:18px 0 26px}
.fl .row{height:50px}
.fl .row .rt,.fl .row .rp{font-size:29px}
#fin .dr{border-top:2px solid var(--ink);border-bottom:1px solid var(--ink);padding-top:4px;margin:22px 0 4px}
.ft{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:168px;line-height:1;direction:ltr;text-align:left;color:var(--pen)}
.fs{font-family:"Heebo",sans-serif;font-weight:300;font-size:28px;color:var(--grey);text-align:left;margin-top:2px}
.col{margin-top:auto;width:100%;display:flex;flex-direction:row;align-items:baseline;justify-content:space-between;gap:20px;border-top:1px solid rgba(31,26,21,.4);padding-top:18px}
.cl1,.cl2{white-space:nowrap}
.cl1{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:50px;direction:ltr;letter-spacing:.03em}
.cl2{font-family:"Heebo",sans-serif;font-weight:400;font-size:28px}
"""

JS = r"""
const PIECES = __PIECES__;
const LOOP = __LOOP__;
const CIRC = [  // pencil loops: [obj, t0, end, sx, sy]
  ["chair", .35, 1.85, 1.1, 1.08], ["table", 2.05, 3.62, 1.14, 1.35], ["lamp", 12.85, 14.35, 1.25, 1.5], ["drone", 11.1, 12.95, 1.25, 1.6]];
const clamp = (v, a, b) => Math.max(a, Math.min(b, v));
const sm = (x) => { x = clamp(x, 0, 1); return x * x * (3 - 2 * x); };
const eo = (x) => 1 - Math.pow(1 - clamp(x, 0, 1), 3);
const fmt = (v) => "$" + Math.round(v).toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
function loopPath(b, sx, sy, p, off) {
  const cx = (b[0] + b[2]) / 2, cy = (b[1] + b[3]) / 2, rx = (b[2] - b[0]) / 2 * sx, ry = (b[3] - b[1]) / 2 * sy;
  const n = Math.max(2, Math.round((LOOP.length - 1) * p) + 1);
  let d = "";
  for (let i = 0; i < n; i++) { const q = LOOP[i]; d += (i ? "L" : "M") + (cx + q[0] * rx + off).toFixed(1) + "," + (cy + q[1] * ry + off * .6).toFixed(1); }
  return p <= 0 ? "" : d;
}
const _p0 = window.onPlace;
window.onPlace = (t) => {
  _p0 && _p0(t);
  // magazine credits: circled number on the piece, leader line drawn out to a shopping-page credit
  PIECES.forEach((P, k) => {
    const mk = document.getElementById("mk" + k), cr = document.getElementById("cr" + k);
    const ld = document.getElementById("ld" + k), lh = document.getElementById("lh" + k);
    const t0 = P[8], t1 = P[9], fin = 1 - sm((t - t1 + .05) / .35), b = boxAt(P[3], t);
    if (!b || t < t0 || fin <= 0) { mk.style.opacity = 0; cr.style.opacity = 0; ld.setAttribute("d", ""); lh.setAttribute("d", ""); return; }
    const mx = clamp(b[0] + (b[2] - b[0]) * P[4], 560, 1860), my = clamp(b[1] + (b[3] - b[1]) * P[5], 60, 1000);
    const pm = eo((t - t0) / .35);
    mk.style.left = mx.toFixed(1) + "px"; mk.style.top = my.toFixed(1) + "px";
    mk.style.opacity = pm * fin; mk.style.transform = `scale(${(.55 + .45 * pm).toFixed(3)})`;
    const w = cr.offsetWidth, h = cr.offsetHeight, neg = P[6] < 0;
    const ax = mx + P[6], ay = my + P[7];
    const L = clamp(neg ? ax - w : ax, 540, 1880 - w), T = clamp(ay - h / 2, 40, 990 - h);
    const ex = neg ? L + w : L, ey = T + h / 2, kx = ex + (neg ? 40 : -40), ky = ey;
    const dx0 = kx - mx, dy0 = ky - my, d0 = Math.hypot(dx0, dy0) || 1;
    const sx = mx + dx0 / d0 * 21, sy = my + dy0 / d0 * 21;
    const l1 = Math.hypot(kx - sx, ky - sy), l2 = Math.abs(ex - kx), pl = eo((t - t0 - .12) / .45) * (l1 + l2);
    let d = "";
    if (pl > 0) {
      d = `M${sx.toFixed(1)},${sy.toFixed(1)}`;
      if (pl <= l1) { const f = pl / l1; d += `L${(sx + (kx - sx) * f).toFixed(1)},${(sy + (ky - sy) * f).toFixed(1)}`; }
      else { d += `L${kx.toFixed(1)},${ky.toFixed(1)}L${(kx + (ex - kx) * (pl - l1) / (l2 || 1)).toFixed(1)},${ey.toFixed(1)}`; }
    }
    ld.setAttribute("d", d); lh.setAttribute("d", d); ld.style.opacity = lh.style.opacity = fin;
    const pc = sm((t - t0 - .38) / .35);
    cr.style.left = L.toFixed(1) + "px"; cr.style.top = T.toFixed(1) + "px";
    cr.style.opacity = pc * fin; cr.style.transform = `translateX(${((neg ? 14 : -14) * (1 - pc)).toFixed(1)}px)`;
  });
  // editor's red-pencil loops
  CIRC.forEach((C, k) => {
    const a = document.getElementById("c" + k + "a"), bb = document.getElementById("c" + k + "b");
    const b = boxAt(C[0], t), p = eo((t - C[1]) / .7), fade = 1 - sm((t - C[2] + .05) / .3);
    if (!b || t < C[1] || fade <= 0) { a.setAttribute("d", ""); bb.setAttribute("d", ""); return; }
    a.setAttribute("d", loopPath(b, C[3], C[4], p, 0)); bb.setAttribute("d", loopPath(b, C[3] * 1.03, C[4] * 1.04, p * .96, 3));
    a.style.opacity = bb.style.opacity = fade;
  });
  // pencil arrow from the margin note to the drone
  const arw = document.getElementById("arw"), arh = document.getElementById("arh"), nul = document.getElementById("nul");
  const db = boxAt("drone", t), af = 1 - sm((t - 12.72) / .25);
  if (db && t > 11.3 && af > 0) {
    const sx = 470, sy = 300, ex = (db[0] + db[2]) / 2 + 20, ey = db[1] - (db[3] - db[1]) * .4;
    const cx = (sx + ex) / 2 - 170, cy = (sy + ey) / 2 + 20, p = eo((t - 11.3) / .6);
    let d = "", lx = sx, ly = sy, px = sx, py = sy;
    for (let i = 0; i <= 40; i++) { const s = p * i / 40, m = 1 - s;
      const X = m * m * sx + 2 * m * s * cx + s * s * ex, Y = m * m * sy + 2 * m * s * cy + s * s * ey;
      d += (i ? "L" : "M") + X.toFixed(1) + "," + Y.toFixed(1); px = lx; py = ly; lx = X; ly = Y; }
    arw.setAttribute("d", d);
    if (p > .97) { const an = Math.atan2(ly - py, lx - px), L = 30;
      arh.setAttribute("d", `M${(lx - L * Math.cos(an - .5)).toFixed(1)},${(ly - L * Math.sin(an - .5)).toFixed(1)}L${lx.toFixed(1)},${ly.toFixed(1)}L${(lx - L * Math.cos(an + .5)).toFixed(1)},${(ly - L * Math.sin(an + .5)).toFixed(1)}`);
    } else arh.setAttribute("d", "");
    arw.style.opacity = arh.style.opacity = af;
  } else { arw.setAttribute("d", ""); arh.setAttribute("d", ""); }
  // pencil underline under the note
  const up = eo((t - 12.35) / .45), uf = 1 - sm((t - 12.72) / .25);
  if (t > 12.35 && uf > 0) {
    const x0 = 745, x1 = 745 - 520 * up;
    nul.setAttribute("d", `M${x0},222 Q${(x0 + x1) / 2},${232} ${x1.toFixed(1)},${(220 + 6 * up).toFixed(1)}`); nul.style.opacity = uf;
  } else nul.setAttribute("d", "");
  // running total in the price-list sidebar
  let v = 0;
  PIECES.forEach((P) => { v += P[2] * eo((t - P[8] - .2) / .8); });
  document.getElementById("tv").textContent = fmt(v);
};
// ---- soft, printed-matter motion (timeline) ----
const E = "power2.out";
tl.set(["#mast", ".fol", "#side", "#note", "#pg", "#fin", "#gut", "#stk"], {opacity: 0}, 0);
// masthead: lifts in, rule draws, lifts away as the camera tilts down
tl.fromTo("#mast .mt", {opacity: 0, y: -24}, {opacity: 1, y: 0, duration: .8, ease: E}, .15);
tl.set("#mast", {opacity: 1}, .14);
tl.fromTo("#mast .mr", {scaleX: 0}, {scaleX: 1, duration: .7, ease: "power2.inOut"}, .35);
tl.fromTo("#mast .ms", {opacity: 0, y: 10}, {opacity: 1, y: 0, duration: .6, ease: E}, .6);
tl.to("#mast", {opacity: 0, y: -40, duration: .6, ease: "power2.in"}, 1.55);
tl.to("#gut", {opacity: 1, duration: .8}, .2);
tl.to("#gut", {opacity: 0, duration: .4}, 14.3);
tl.to("#curl", {opacity: 1, duration: .6}, .4);
tl.to("#curl", {opacity: 0, duration: .3}, 6.5);
tl.to("#curl", {opacity: 1, duration: .4}, 11.1);
tl.to(".fol", {opacity: 1, duration: .6}, .4);
tl.to(".fol", {opacity: 0, duration: .4}, 14.3);
// sidebar slides in like a printed column; rows ink in as each piece is named
tl.set("#side", {opacity: 1}, .25);
tl.fromTo("#side", {clipPath: "inset(0% 100% 0% 0%)"}, {clipPath: "inset(0% 0% 0% 0%)", duration: .9, ease: "power2.inOut"}, .25);
PIECES.forEach((P, k) => tl.fromTo(["#rw" + k + " .rt", "#rw" + k + " .rp"], {opacity: 0, x: 26}, {opacity: 1, x: 0, duration: .5, ease: E}, P[8] + .05));
tl.to("#side", {x: -520, duration: .7, ease: "power2.inOut"}, 10.75);
tl.to("#side", {x: 0, duration: .7, ease: "power2.inOut"}, 12.55);
tl.to("#side", {opacity: 0, duration: .3}, 15.0);
// editorial page folds open on its spine for the pull-quote, folds shut before the drone
tl.set("#pg", {opacity: 1, transformPerspective: 2200}, 6.55);
tl.fromTo("#pg", {rotationY: -88}, {rotationY: 0, duration: .85, ease: "power3.out"}, 6.55);
tl.to("#fol-r", {opacity: 0, duration: .3}, 6.5);
tl.to("#fol-r", {opacity: 1, duration: .4}, 11.4);
tl.fromTo(".qm", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .6, ease: E}, 6.7);
[["#q0", 6.8], ["#q1", 7.03], ["#q2", 7.36], ["#q3", 7.57], ["#q4", 7.98]].forEach(([s, at]) =>
  tl.fromTo(s, {opacity: 0, y: 22}, {opacity: 1, y: 0, duration: .45, ease: E}, at));
tl.fromTo("#hrB", {scaleX: 0, transformOrigin: "100% 50%"}, {scaleX: 1, duration: .5, ease: "power2.inOut"}, 8.7);
tl.fromTo("#d0", {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .5, ease: E}, 9.1);
tl.fromTo("#d1", {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .5, ease: E}, 10.14);
tl.fromTo([".by", ".pf"], {opacity: 0}, {opacity: 1, duration: .6}, 7.2);
// the editor slaps a torn sticky note on the page
tl.fromTo("#stk", {opacity: 0, y: -26, rotation: -11}, {opacity: 1, y: 0, rotation: -5, duration: .55, ease: "power3.out"}, 8.35);
tl.to("#pg", {rotationY: -88, duration: .6, ease: "power2.in"}, 10.85);
tl.to("#pg", {opacity: 0, duration: .3, ease: "power1.in"}, 11.15);
// margin note in red pencil, word by word
tl.set("#note", {opacity: 1}, 11.05);
[["#n0", 11.1], ["#n1", 11.59], ["#n2", 12.07], ["#n3", 12.28]].forEach(([s, at]) =>
  tl.fromTo(s, {opacity: 0, x: 14}, {opacity: 1, x: 0, duration: .35, ease: E}, at));
tl.fromTo("#note .ns", {opacity: 0}, {opacity: 1, duration: .5}, 11.4);
tl.to("#note", {opacity: 0, duration: .2}, 12.78);
// closing page folds in over the photo: the whole room, totalled, and the colophon
tl.set("#fin", {opacity: 1, transformPerspective: 2200}, 14.3);
tl.fromTo("#fin", {rotationY: 88}, {rotationY: 0, duration: .9, ease: "power3.out"}, 14.3);
tl.fromTo("#f0", {opacity: 0, y: 24}, {opacity: 1, y: 0, duration: .45, ease: E}, 14.4);
tl.fromTo("#f1", {opacity: 0, y: 24}, {opacity: 1, y: 0, duration: .45, ease: E}, 14.52);
tl.fromTo("#fin .kk", {opacity: 0}, {opacity: 1, duration: .5}, 14.5);
tl.fromTo("#fin .fl .row", {opacity: 0, x: 20}, {opacity: 1, x: 0, duration: .4, stagger: .06, ease: E}, 14.6);
tl.fromTo("#fin .dr", {scaleX: 0, transformOrigin: "100% 50%"}, {scaleX: 1, duration: .5, ease: "power2.inOut"}, 14.8);
tl.fromTo("#ftot", {opacity: 0, y: 30}, {opacity: 1, y: 0, duration: .7, ease: E}, 14.98);
tl.fromTo("#fsub", {opacity: 0}, {opacity: 1, duration: .6}, 15.8);
tl.fromTo("#col", {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .7, ease: E}, 16.85);
"""
JS = JS.replace("__PIECES__", str([list(p) for p in PIECES]).replace("'", '"')).replace("__LOOP__", LOOP)

SPEC = {
    "theme": "he_bold",
    "palette": {"acc": "#ad3f26", "ink": "#1f1a15", "lt": "#f5efe4", "panel": "rgba(245,239,228,.95)", "sub": "#6d6358"},
    "music_vol": 0.55,
    "plate_vol": 0.3,
    "elements": [],
    "css": CSS,
    "html_front": HTML,
    "js": JS,
    "assets": ASSETS,
    "vo_name": "E5_home_he_vo",
}
