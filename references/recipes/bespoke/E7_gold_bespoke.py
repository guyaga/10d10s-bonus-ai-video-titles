# E7 AURUM ATELIER - BESPOKE: "a jeweller's bench after hours".
# Visual language (nothing from the stock kine/tape/glass/lockup kit, no paper tags, no handwriting):
#  - a display spotlight: the frame dims to velvet-black around the featured piece (tracked), words live in that darkness
#  - THE LOUPE is the signature: one 10x jeweller's loupe travels watch -> bracelet -> rings (stabilised magnified
#    crops from the clip), a grade engraved into its glass ring per piece (18K . 750 / VS1 . 18K ...)
#  - each piece is priced on a tiny engraved gold hallmark plate hung off the loupe (750 cartouche, Hebrew name, price)
#  - four-point light glints drawn on the metal highlights (tracked, seek-safe, computed from t)
#  - thin Frank Ruhl Libre 300 words in gold foil, wide tracking, slow fades; roman-numeral "moments" I / II / III
#  - end: a black card, gold-foil engraving (Cormorant caps, Frank Ruhl Hebrew, Pinyon Script Latin signature),
#    blind-embossed frame + hallmark, a light sweep across the foil. No cream paper anywhere.
import json
from pathlib import Path

T = Path(__file__).resolve().parent.parent
LP = json.loads((T / "E7_gold_bespoke_loupe.json").read_text())

# Hebrew and Latin subsets are separate families so the Hebrew file is really used for Hebrew glyphs
FONTS = {
    "FRL He": [("frank-ruhl-libre-hebrew-300-normal", 300, "normal"), ("frank-ruhl-libre-hebrew-500-normal", 500, "normal"),
               ("frank-ruhl-libre-hebrew-700-normal", 700, "normal")],
    "FRL La": [("frank-ruhl-libre-latin-300-normal", 300, "normal"), ("frank-ruhl-libre-latin-500-normal", 500, "normal"),
               ("frank-ruhl-libre-latin-700-normal", 700, "normal")],
    "Cormorant Light": [("cormorant-garamond-latin-300-normal", 300, "normal"), ("cormorant-garamond-latin-300-italic", 300, "italic"),
                        ("cormorant-garamond-latin-500-normal", 500, "normal"), ("cormorant-garamond-latin-600-normal", 600, "normal")],
    "Pinyon Script": [("pinyon-script-latin-400-normal", 400, "normal")],
}

GLINT_SVG = ('<svg viewBox="-100 -100 200 200" width="200" height="200">'
             '<defs><radialGradient id="GG{k}"><stop offset="0" stop-color="#fff" stop-opacity=".95"/>'
             '<stop offset=".25" stop-color="#fff3cf" stop-opacity=".55"/><stop offset="1" stop-color="#e8c77a" stop-opacity="0"/></radialGradient></defs>'
             '<circle r="46" fill="url(#GG{k})"/>'
             '<path d="M0,-98 L3.2,-3.2 L98,0 L3.2,3.2 L0,98 L-3.2,3.2 L-98,0 L-3.2,-3.2 Z" fill="#fffaf0"/>'
             '<path d="M0,-44 L1.6,-1.6 L44,0 L1.6,1.6 L0,44 L-1.6,1.6 L-44,0 L-1.6,-1.6 Z" fill="#fff3cf" transform="rotate(45)" opacity=".8"/>'
             '<circle r="5" fill="#fff"/></svg>')

# glints: (obj, fx, fy, t, dur, size)  - the ones under the loupe path were dropped
GLINTS = [
    ("watchface", .50, .22, 1.20, .9, 110), ("bracelet", .62, .26, 1.62, .9, 96), ("ringstack", .60, .22, 2.05, .9, 104),
    ("ringstack", .60, .22, 5.60, .8, 120),
    ("watchface", .45, .20, 9.55, .9, 110), ("bracelet", .55, .25, 9.95, .9, 100), ("ringstack", .62, .20, 10.35, .9, 110),
    ("ringstack", .62, .20, 11.25, 1.1, 140),
]

# the loupe travels watch -> bracelet -> rings; each piece gets an engraved gold hallmark plate + a grade engraved in the glass
PIECES = [  # plate side (+1 right / -1 left), plate dy, numeral, Hebrew name, price, grade engraved in the loupe
    (1, 60, "I", "שעון זהב", "4,750", "18K · 750 · SAPPHIRE"),
    (1, 80, "II", "צמיד טניס", "3,300", "VS1 · 18K · 3.20 CT"),
    (-1, -30, "III", "זוג טבעות", "1,550", "VS1 · F · 18K"),
]
L_IN, L_OUT = 3.05, 8.72   # loupe on screen (sprite covers frames f0 .. f0+n)

# hero words: id, lines [(text, size, class)], centre x, top y, t in, t out, numeral
WORDS = [
    ("hw0", [("טקס קטן", 150, "a"), ("בשלושה רגעים", 76, "b")], 1480, 70, 0.30, 2.80, ""),
    ("hw1", [("השעה", 176, "a")], 1470, 28, 3.55, 4.40, "I"),
    ("hw2", [("האור", 176, "a")], 1360, 300, 5.05, 6.25, "II"),
    ("hw3", [("המגע", 176, "a")], 560, 90, 7.50, 8.78, "III"),
]


def _html():
    h = ['<div id="spot" data-layout-allow-overlap data-layout-allow-occlusion></div>']
    h.append('<div id="gx">' + "".join(f'<div class="gx" id="gx{k}" data-layout-allow-overlap data-layout-allow-occlusion>{GLINT_SVG.format(k=k)}</div>'
                                        for k in range(len(GLINTS))) + '</div>')
    # fine gold leader from the magnified detail to the loupe when the loupe has to sit off it (frame edge)
    h.append('<svg id="lead" viewBox="0 0 1920 1080" width="1920" height="1080"><path id="ldu" class="ldu"/><path id="ldt" class="ldt"/>'
             '<circle id="ldk" class="ldk" r="7" cx="-40" cy="-40"/></svg>')
    for k, (_s, _dy, num, name, price, _g) in enumerate(PIECES):
        h.append(f'<div class="hp" id="hp{k}" data-layout-allow-overlap data-layout-allow-occlusion><div class="pl">'
                 f'<i class="rv a"></i><i class="rv b"></i>'
                 f'<div class="mk"><span class="c">750</span><span class="au">AURUM &middot; {num}</span></div>'
                 f'<div class="nm">{name}</div><div class="rl"></div>'
                 f'<div class="pr"><bdi dir="ltr">{price}</bdi>&thinsp;₪</div></div></div>')
    arcs = "".join(f'<text class="gr" id="gr{k}"><textPath href="#lparc" startOffset="50%" text-anchor="middle">{g}</textPath></text>'
                   for k, (*_x, g) in enumerate(PIECES))
    h.append('<div id="loupe" data-layout-allow-overlap data-layout-allow-occlusion><div id="lpv"><div id="lpimg"></div></div>'
             '<div class="knurl"></div><div class="rim"></div><div class="glass"></div>'
             '<svg class="eng" viewBox="-200 -200 400 400" width="400" height="400"><defs>'
             '<path id="lparc" d="M -181,0 A 181 181 0 0 0 181,0"/>'
             '<path id="lptop" d="M -181,0 A 181 181 0 0 1 181,0"/></defs>'
             '<circle r="182" class="band"/><circle r="164" class="bi"/><circle r="199" class="bo"/>'
             f'{arcs}<text class="x10"><textPath href="#lptop" startOffset="50%" text-anchor="middle">10&times; &#10022; AURUM ATELIER</textPath></text></svg></div>')
    for (i, lines, x, y, t0, t1, num) in WORDS:
        inner = "".join(f'<div class="ln {c}" style="font-size:{s}px"><span class="fo">{tx}</span></div>' for tx, s, c in lines)
        nm = f'<div class="num"><i></i><span>{num}</span><i></i></div>' if num else ""
        h.append(f'<div class="hw" id="{i}" style="left:{x}px;top:{y}px" data-layout-allow-overlap data-layout-allow-occlusion>{nm}{inner}<div class="hl"></div></div>')
    h.append('<div id="card" data-layout-allow-overlap><div class="cd"><div class="emb"></div><div class="fr"></div>'
             '<div class="br"><span class="foil">AURUM ATELIER</span></div><div class="rule"><i></i><b>&#10022;</b><i></i></div>'
             '<div class="hand" id="hand"><span class="foil">רק שלך</span></div>'
             '<div class="sig" id="sig"><span class="foil">Aurum</span></div>'
             '<div class="hm"><span></span></div></div></div>')
    return "".join(h)


GOLD = "linear-gradient(100deg,#b8903f 0%,#e9cf8a 22%,#fff6da 38%,#f1d99b 50%,#c49a4a 66%,#ecd18c 84%,#b8903f 100%)"
CSS = r'''
#stage2{direction:ltr}
#spot{position:absolute;inset:0;pointer-events:none}
#gx{position:absolute;inset:0}
.gx{position:absolute;left:0;top:0;width:200px;height:200px;margin:-100px 0 0 -100px;opacity:0;mix-blend-mode:screen}
.gx svg{display:block}
#lead{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}
.ldu{fill:none;stroke:rgba(10,6,2,.6);stroke-width:3.4px}
.ldt{fill:none;stroke:#e6cf97;stroke-width:1.3px}
.ldk{fill:none;stroke:#f2dc9f;stroke-width:1.6px}
/* engraved gold hallmark plate */
.hp{position:absolute;left:0;top:0;width:0;height:0;opacity:0}
.pl{position:absolute;left:-128px;top:-92px;width:256px;box-sizing:border-box;padding:20px 20px 16px;
  background:linear-gradient(158deg,#f6e2a6 0%,#d8b465 30%,#b58a3c 55%,#e4c67f 78%,#a67c32 100%);
  border-radius:4px;box-shadow:0 22px 40px rgba(0,0,0,.6),0 3px 8px rgba(0,0,0,.45),inset 0 1px 0 rgba(255,248,220,.85),inset 0 -2px 3px rgba(80,50,10,.55);
  display:flex;flex-direction:column;align-items:center;gap:4px;direction:rtl;color:#4a3210}
.pl::before{content:"";position:absolute;inset:7px;border:1px solid rgba(90,60,18,.55);border-radius:2px;box-shadow:0 1px 0 rgba(255,244,210,.45),inset 0 1px 0 rgba(255,244,210,.35)}
.pl .rv{position:absolute;top:50%;width:8px;height:8px;margin-top:-4px;border-radius:50%;background:radial-gradient(circle at 35% 35%,#fff1c6,#9c7430 70%);box-shadow:0 1px 1px rgba(0,0,0,.5)}
.pl .rv.a{left:-2px;display:none}.pl .rv.b{right:-2px;display:none}
.pl .mk{display:flex;align-items:center;gap:10px;direction:ltr;margin-bottom:10px}
.pl .mk .c{font-family:"Cormorant Light",serif;font-weight:600;font-size:17px;letter-spacing:.08em;padding:0 9px;height:22px;line-height:22px;border:1.5px solid rgba(74,50,16,.8);border-radius:11px;
  color:#4a3210;text-shadow:0 1px 0 rgba(255,244,210,.7)}
.pl .mk .au{font-family:"Cormorant Light",serif;font-weight:600;font-size:15px;letter-spacing:.32em;color:#4a3210;text-shadow:0 1px 0 rgba(255,244,210,.7)}
.pl .nm{font-family:"FRL He","FRL La",serif;font-weight:500;font-size:40px;line-height:1.1;color:#3d2809;
  text-shadow:0 1px 0 rgba(255,246,214,.8),0 -1px 0 rgba(60,36,6,.45)}
.pl .rl{width:70px;height:1px;background:rgba(74,50,16,.6);box-shadow:0 1px 0 rgba(255,244,210,.6);margin:2px 0 4px}
.pl .pr{font-family:"FRL He","FRL La",serif;font-weight:500;font-size:34px;line-height:1.05;color:#3d2809;
  text-shadow:0 1px 0 rgba(255,246,214,.8),0 -1px 0 rgba(60,36,6,.45)}
/* the loupe */
#loupe{position:absolute;left:0;top:0;width:0;height:0;opacity:0}
#lpv{position:absolute;left:-200px;top:-200px;width:400px;height:400px;border-radius:50%;overflow:hidden;background:#000}
#lpimg{position:absolute;left:-10px;top:-10px;width:420px;height:420px;background-image:url(assets/E7_gold_loupe.jpg);background-repeat:no-repeat;
  background-size:__BGS__}
#loupe .knurl{position:absolute;left:-226px;top:-226px;width:452px;height:452px;border-radius:50%;
  background:repeating-conic-gradient(#6b5021 0deg 2deg,#caa75e 2deg 4deg);
  -webkit-mask:radial-gradient(circle,transparent 213px,#000 214px,#000 225px,transparent 226px);mask:radial-gradient(circle,transparent 213px,#000 214px,#000 225px,transparent 226px);
  filter:drop-shadow(0 20px 40px rgba(0,0,0,.6))}
#loupe .rim{position:absolute;left:-214px;top:-214px;width:428px;height:428px;border-radius:50%;
  border:14px solid transparent;background:conic-gradient(from 200deg,#f7e2a6,#8a6524,#f3d98f,#6e4f1b,#e9cd85,#f7e2a6) border-box;
  -webkit-mask:radial-gradient(circle,transparent 199px,#000 200px);mask:radial-gradient(circle,transparent 199px,#000 200px);box-sizing:border-box}
#loupe .glass{position:absolute;left:-200px;top:-200px;width:400px;height:400px;border-radius:50%;
  background:radial-gradient(ellipse 60% 34% at 34% 18%,rgba(255,255,255,.22),rgba(255,255,255,0) 70%),
             radial-gradient(circle at 50% 50%,rgba(0,0,0,0) 72%,rgba(0,0,0,.45) 100%);box-shadow:inset 0 0 18px rgba(0,0,0,.5)}
#loupe .eng{position:absolute;left:-200px;top:-200px;width:400px;height:400px;overflow:visible}
.eng .band{fill:none;stroke:rgba(10,7,3,.74);stroke-width:34px}
.eng .bi{fill:none;stroke:rgba(226,196,126,.55);stroke-width:1px}
.eng .bo{fill:none;stroke:rgba(226,196,126,.35);stroke-width:1px}
.eng text{font-family:"Cormorant Light",serif;font-weight:600;font-size:21px;letter-spacing:.24em;fill:#ecd395;dominant-baseline:middle}
.eng .x10{font-size:15px;letter-spacing:.34em;fill:#cdb074;font-weight:500}
.eng .gr{opacity:0}
/* thin gold words */
.hw{position:absolute;width:0;height:0;direction:rtl}
.hw>div{position:absolute;left:0;white-space:nowrap;text-align:center}
.hw .num{top:0;display:flex;align-items:center;gap:18px;direction:ltr;font-family:"Cormorant Light",serif;font-weight:300;font-size:30px;letter-spacing:.3em;color:#e3c983;
  filter:drop-shadow(0 2px 10px rgba(0,0,0,.95))}
.hw .num i{display:block;width:54px;height:1px;background:linear-gradient(90deg,transparent,#d8b86c)}
.hw .num i:last-child{background:linear-gradient(270deg,transparent,#d8b86c)}
.hw .ln{filter:drop-shadow(0 3px 16px rgba(0,0,0,.95)) drop-shadow(0 0 3px rgba(0,0,0,.6))}
.hw .fo{display:inline-block;font-family:"FRL He","FRL La",serif;font-weight:300;line-height:1.05;letter-spacing:.12em;padding:0 .06em;
  background:linear-gradient(100deg,#d2ad63 0%,#f3dea4 24%,#fffaf0 40%,#f6e3ae 52%,#d6b168 70%,#efd594 86%,#d2ad63 100%);background-size:300% 100%;
  background-position:100% 0;-webkit-background-clip:text;background-clip:text;color:transparent;-webkit-text-fill-color:transparent}
.hw .hl{height:1px;width:320px;background:linear-gradient(90deg,transparent,#d9b96d 30%,#f5e3b0 50%,#d9b96d 70%,transparent)}
#hw0 .a{top:0}#hw0 .b{top:176px}#hw0 .hl{top:292px}
#hw0 .b .fo{letter-spacing:.2em}
#hw1 .num,#hw2 .num,#hw3 .num{top:0}
#hw1 .a,#hw2 .a,#hw3 .a{top:40px}
#hw1 .hl,#hw2 .hl,#hw3 .hl{top:238px}
/* the end card: black card, gold foil + blind emboss */
#card{position:absolute;left:70px;top:704px;width:560px;height:316px;opacity:0}
#card .cd{position:absolute;inset:0;transform:rotate(-3deg);
  background:radial-gradient(ellipse 80% 70% at 30% 20%,#1d1811 0%,#0e0b08 55%,#070605 100%);
  box-shadow:0 30px 60px rgba(0,0,0,.75),0 4px 10px rgba(0,0,0,.6),0 0 0 1px rgba(214,178,100,.55),inset 0 1px 0 rgba(255,236,190,.12);border-radius:3px}
#card .emb{position:absolute;inset:14px;border-radius:2px;box-shadow:inset 1px 1px 0 rgba(0,0,0,.9),inset -1px -1px 0 rgba(255,240,210,.09),1px 1px 0 rgba(255,240,210,.08),-1px -1px 0 rgba(0,0,0,.8)}
#card .fr{position:absolute;inset:24px;border:1px solid rgba(214,178,100,.7)}
#card .foil{display:inline-block;padding:0 .14em;background:__GOLD__;background-size:300% 100%;background-position:100% 0;
  -webkit-background-clip:text;background-clip:text;color:#dcbc70;-webkit-text-fill-color:transparent;filter:drop-shadow(0 1px 0 rgba(0,0,0,.9))}
#card .br{position:absolute;left:0;right:0;top:48px;text-align:center;font-family:"Cormorant Light",serif;font-weight:500;font-size:32px;letter-spacing:.36em;padding-left:.36em}
#card .rule{position:absolute;left:0;right:0;top:94px;display:flex;align-items:center;justify-content:center;gap:14px;color:#d6b264;font-size:14px}
#card .rule i{display:block;width:92px;height:1px;background:linear-gradient(90deg,transparent,#c9a354,transparent)}
#card .hand{position:absolute;left:0;right:0;top:140px;text-align:center;direction:rtl;font-family:"FRL He","FRL La",serif;font-weight:500;font-size:72px;line-height:1.1;letter-spacing:.04em}
#card .sig{position:absolute;left:62px;bottom:30px;font-family:"Pinyon Script",cursive;font-size:44px;line-height:1.25;transform:rotate(-4deg)}
#card .hm{position:absolute;right:52px;bottom:40px;height:30px;padding:0 12px;border-radius:15px;
  box-shadow:inset 1px 1px 0 rgba(0,0,0,.9),inset -1px -1px 0 rgba(255,240,210,.1);display:flex;align-items:center}
#card .hm span::after{content:"750";font-family:"Cormorant Light",serif;font-weight:600;font-size:19px;letter-spacing:.14em;color:#0f0c09;text-shadow:-1px -1px 0 rgba(0,0,0,.9),1px 1px 0 rgba(255,240,210,.13)}
'''.replace("__GOLD__", GOLD).replace("__BGS__", f"{LP['cols'] * LP['size']}px {LP['rows'] * LP['size']}px")


def _js():
    glints = json.dumps([list(g) for g in GLINTS])
    pieces = json.dumps([[p[0], p[1]] for p in PIECES])
    js = r'''
const GL = __GL__, PC = __PC__, LPD = __LP__, L_IN = __LIN__, L_OUT = __LOUT__;
const clamp01 = (v) => Math.max(0, Math.min(1, v));
const sm = (v) => { v = clamp01(v); return v * v * (3 - 2 * v); };
// display spotlight: [t0, t1, obj, fx, fy, radius, alpha]; the camera move 3.0-8.85 is one take, so neighbours blend
const SP = [[0, 2.95, "bracelet", .75, .62, 1150, .50], [2.95, 4.40, "watchface", .55, .95, 800, .86],
            [4.40, 6.30, "bracelet", .42, .42, 760, .84], [6.30, 8.87, "ringstack", .45, .45, 660, .86], [8.87, 13, "ringstack", -.6, .3, 1080, .55]];
function spAt(k, t) { const s = SP[k], b = boxAt(s[2], t); if (!b) return null;
  return [b[0] + (b[2] - b[0]) * s[3], b[1] + (b[3] - b[1]) * s[4], s[5], s[6]]; }
const spot = document.getElementById("spot");
function spotAt(t) {
  let k = SP.findIndex((s) => t < s[1]); if (k < 0) k = SP.length - 1;
  let p = spAt(k, t); const W = .9;
  for (const bd of [1, 2]) {
    const B = SP[bd][1];
    if (Math.abs(t - B) < W / 2) { const a = spAt(bd, t), c = spAt(bd + 1, t), u = sm((t - (B - W / 2)) / W); if (a && c) p = a.map((v, j) => v + (c[j] - v) * u); }
  }
  if (!p) return;
  const [x, y, R, a] = p;
  spot.style.background = `radial-gradient(circle ${R.toFixed(0)}px at ${x.toFixed(1)}px ${y.toFixed(1)}px, rgba(6,4,2,0) 0%, rgba(6,4,2,0) 36%, rgba(6,4,2,${(a * .55).toFixed(3)}) 68%, rgba(6,4,2,${a.toFixed(3)}) 100%)`;
}
const GX = GL.map((g, k) => document.getElementById("gx" + k));
const LO = document.getElementById("loupe"), LI = document.getElementById("lpimg");
const HP = PC.map((p, k) => document.getElementById("hp" + k)), GR = PC.map((p, k) => document.getElementById("gr" + k));
const LDU = document.getElementById("ldu"), LDT = document.getElementById("ldt"), LDK = document.getElementById("ldk");
// sub-frame interpolation of the precomputed loupe path (seek-safe: pure function of t)
function lpAt(key, t) { const x = t * 24 - LPD.f0, i = Math.max(0, Math.min(LPD.n - 1, Math.floor(x))), j = Math.min(LPD.n - 1, i + 1), u = clamp01(x - i);
  return LPD[key][i] + (LPD[key][j] - LPD[key][i]) * u; }
const _p = window.onPlace;
window.onPlace = (t) => {
  _p && _p(t);
  spotAt(t);
  GL.forEach((g, k) => {
    const el = GX[k], u = (t - g[3]) / g[4];
    if (u <= 0 || u >= 1) { el.style.opacity = 0; return; }
    const b = boxAt(g[0], t); if (!b) { el.style.opacity = 0; return; }
    const x = b[0] + (b[2] - b[0]) * g[1], y = b[1] + (b[3] - b[1]) * g[2];
    const I = Math.pow(Math.sin(Math.PI * u), 1.6), s = g[5] / 200 * (.25 + .95 * I);
    el.style.opacity = I.toFixed(3);
    el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) rotate(${(12 + 38 * u).toFixed(2)}deg) scale(${s.toFixed(3)})`;
  });
  // the travelling loupe
  const lv = sm((t - L_IN) / .55) * (1 - sm((t - (L_OUT - .35)) / .35));
  const f = Math.round(t * 24) - LPD.f0, i = Math.max(0, Math.min(LPD.n - 1, f));
  const cx = lpAt("cx", t), cy = lpAt("cy", t), sx = lpAt("sx", t), sy = lpAt("sy", t);
  LO.style.left = cx.toFixed(1) + "px"; LO.style.top = cy.toFixed(1) + "px";
  LI.style.backgroundPosition = `${-(i % LPD.cols) * LPD.size}px ${-Math.floor(i / LPD.cols) * LPD.size}px`;
  const W = LPD.w[i];
  const gl = 1 - Math.max(...W);
  LI.style.filter = `blur(${(8 * gl).toFixed(2)}px)`;
  LO.style.opacity = (lv * (1 - sm((gl - .03) / .17))).toFixed(3);
  LO.style.transform = `scale(${((.88 + .12 * lv) * (1 - .22 * sm(gl / .35))).toFixed(4)})`;
  PC.forEach((p, k) => {
    const w = sm((W[k] - .82) / .18) * lv;
    GR[k].style.opacity = w.toFixed(3);
    const el = HP[k];
    if (w <= 0.001) { el.style.opacity = 0; return; }
    const sway = 1.6 * Math.sin(1.3 * t + k * 2.1);
    el.style.opacity = w.toFixed(3);
    el.style.left = (cx + p[0] * (226 + 150)).toFixed(1) + "px";
    el.style.top = (cy + p[1]).toFixed(1) + "px";
    el.style.transform = `translateY(${(10 * (1 - w)).toFixed(1)}px) rotate(${(p[0] * -2.2 + sway).toFixed(2)}deg)`;
  });
  // leader from the magnified detail to the rim when the loupe sits off the detail
  const dx = sx - cx, dy = sy - cy, d = Math.hypot(dx, dy), lo = sm((d - 236) / 50) * lv;
  if (lo > 0.01) {
    const ex = cx + dx / d * 228, ey = cy + dy / d * 228, px = sx - dx / d * 9, py = sy - dy / d * 9;
    const path = `M${ex.toFixed(1)},${ey.toFixed(1)} L${px.toFixed(1)},${py.toFixed(1)}`;
    LDU.setAttribute("d", path); LDT.setAttribute("d", path); LDK.setAttribute("cx", sx.toFixed(1)); LDK.setAttribute("cy", sy.toFixed(1));
    LDU.style.opacity = LDT.style.opacity = LDK.style.opacity = lo.toFixed(3);
  } else { LDU.setAttribute("d", ""); LDT.setAttribute("d", ""); LDK.setAttribute("cx", -40); }
};
// --- timeline: slow fades only ---
tl.fromTo("#spot", {opacity: 0}, {opacity: 1, duration: 1.2, ease: "sine.inOut"}, 0);
function word(id, t0, t1) {
  const lines = document.querySelectorAll("#" + id + " .ln");
  tl.set("#" + id, {opacity: 1}, 0);
  tl.set("#" + id + ">div", {xPercent: -50}, 0);
  lines.forEach((ln, j) => {
    const at = t0 + j * (id === "hw0" ? 1.02 : 0);
    tl.fromTo(ln, {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: 1.0, ease: "sine.out"}, at);
    tl.fromTo(ln.querySelector(".fo"), {scaleX: 1.16, filter: "blur(7px)"}, {scaleX: 1, filter: "blur(0px)", duration: 1.2, ease: "power2.out"}, at);
    tl.fromTo(ln.querySelector(".fo"), {backgroundPosition: "100% 0"}, {backgroundPosition: "0% 0", duration: Math.max(1.2, t1 - at), ease: "sine.inOut"}, at);
  });
  const n = document.querySelector("#" + id + " .num");
  if (n) tl.fromTo(n, {opacity: 0}, {opacity: 1, duration: .8, ease: "sine.out"}, t0 - .25);
  tl.fromTo("#" + id + " .hl", {scaleX: 0, opacity: 0}, {scaleX: 1, opacity: 1, duration: 1.1, ease: "power2.out"}, t0 + .3);
  tl.to("#" + id, {opacity: 0, duration: .45, ease: "sine.in"}, t1 - .45);
}
__WORDS__
// end card: black card rises, foil is stamped (blur->sharp), a light sweep crosses the foil
tl.fromTo("#card", {opacity: 0, y: 26}, {opacity: 1, y: 0, duration: 1.2, ease: "sine.out"}, 9.15);
tl.fromTo("#card .br", {opacity: 0, scaleX: 1.12}, {opacity: 1, scaleX: 1, duration: 1.2, ease: "power2.out"}, 9.35);
tl.fromTo("#card .rule", {opacity: 0, scaleX: .4}, {opacity: 1, scaleX: 1, duration: 1.0, ease: "power2.out"}, 9.7);
tl.fromTo("#card .hm", {opacity: 0}, {opacity: 1, duration: 1.0, ease: "sine.out"}, 9.9);
tl.fromTo("#hand", {opacity: 0, scale: 1.06, filter: "blur(6px)"}, {opacity: 1, scale: 1, filter: "blur(0px)", duration: .8, ease: "power2.out"}, 10.95);
tl.fromTo("#sig", {clipPath: "inset(0 100% 0 0)"}, {clipPath: "inset(0 0% 0 0)", duration: .7, ease: "sine.inOut"}, 11.3);
tl.fromTo("#card .br .foil", {backgroundPosition: "100% 0"}, {backgroundPosition: "0% 0", duration: 2.6, ease: "sine.inOut"}, 9.35);
tl.fromTo("#hand .foil", {backgroundPosition: "100% 0"}, {backgroundPosition: "0% 0", duration: 1.9, ease: "sine.inOut"}, 10.95);
tl.fromTo("#sig .foil", {backgroundPosition: "100% 0"}, {backgroundPosition: "0% 0", duration: 1.6, ease: "sine.inOut"}, 11.3);
'''
    wl = "\n".join(f'word("{w[0]}", {w[4]}, {w[5]});' for w in WORDS)
    return (js.replace("__GL__", glints).replace("__PC__", pieces).replace("__LP__", json.dumps(LP)).replace("__WORDS__", wl)
            .replace("__LIN__", str(L_IN)).replace("__LOUT__", str(L_OUT)))


SPEC = {
    'theme': 'he_premium',
    'palette': {'acc': '#d4af37', 'ink': '#0b0b0b', 'lt': '#fff8e7', 'panel': 'rgba(10,9,8,.6)', 'sub': '#e9dcb8'},
    'music_vol': 0.55,
    'plate_vol': 0.3,
    'elements': [],
    'html_front': _html(),
    'css': CSS,
    'js': _js(),
    'fonts': FONTS,
    'assets': {'E7_gold_loupe.jpg': str(T / 'E7_gold_bespoke_loupe.jpg')},
    'vo_name': 'E7_gold_he_vo',
}
