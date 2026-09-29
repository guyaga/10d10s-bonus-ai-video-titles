"""E9_glasses BESPOKE: the world seen through one Lumen Lens (a traveller's lens, not a HUD).
Devices: the LENS itself frames the film - a real spectacle-lens outline with the tortoiseshell frame edge and
the nose bridge + pad softly visible, edge blur and a chromatic fringe along the glass edge; the assistant is
"Stampy", a sun-faced postage-stamp mascot (blinks, lip-syncs to the VO) who talks in paper speech bubbles;
the sign repainted in Hebrew (homography onto the tracked board) and franked with a red ink "translated" rubber
stamp; the belfry gets a map pin + an airmail postcard / phrasebook entry; the walk is a dotted map line with a
red pin; the order is a paper receipt printed out from the barista's side; the end card is a postcard franked by
Stampy. Type: Varela Round (voice + postcards) + IBM Plex Sans Hebrew (labels) + IBM Plex Mono (receipt Latin).
Palette: navy ink, postal red, airmail blue, cream paper, sun yellow.
"""
import json
from pathlib import Path

T = Path(__file__).resolve().parent.parent
F = T.parent / "shared/fonts"

INK = "#1d2d50"
RED = "#d9482b"
BLUE = "#2b62c0"
PAPER = "#fbf5e6"
SUN = "#ffc94a"

HEB = "U+0590-05FF,U+FB1D-FB4F,U+200C-2010,U+20AA,U+25CC"
LAT = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2199,U+2212,U+2215"
_FACES = [
    ("Varela Round", 400, "varela-round-hebrew-400-normal", HEB),
    ("Varela Round", 400, "varela-round-latin-400-normal", LAT),
    ("PlexHe", 500, "ibm-plex-sans-hebrew-hebrew-500-normal", HEB),
    ("PlexHe", 500, "ibm-plex-sans-hebrew-latin-500-normal", LAT),
    ("PlexHe", 700, "ibm-plex-sans-hebrew-hebrew-700-normal", HEB),
    ("PlexHe", 700, "ibm-plex-sans-hebrew-latin-700-normal", LAT),
    ("PlexMono", 400, "ibm-plex-mono-latin-400-normal", LAT),
    ("PlexMono", 600, "ibm-plex-mono-latin-600-normal", LAT),
]
FONTCSS = "".join(f'@font-face{{font-family:"{fam}";font-weight:{w};src:url(assets/fonts/{stem}.woff2) format("woff2");unicode-range:{ur}}}'
                  for fam, w, stem, ur in _FACES)
ASSETS = {f"fonts/{s}.woff2": str(F / f"{s}.woff2") for _, _, s, _ in _FACES}

# ---------------------------------------------------------------- the lens (frame edge, nose bridge, fringe)
LENS = ("M270,-40 H1690 C1880,-40 1906,40 1906,210 V690 C1906,960 1800,1112 1540,1112 H390 C130,1112 14,990 14,770 V600 "
        "C14,540 70,520 84,440 C96,360 70,250 14,200 V210 C14,40 60,-40 270,-40 Z")
LENS_SVG = (
    '<svg id="lens" width="1920" height="1080" viewBox="0 0 1920 1080" data-layout-allow-overlap data-layout-allow-occlusion>'
    '<defs><filter id="lzSoft" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="13"/></filter>'
    '<filter id="lzFr" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="3.2"/></filter>'
    '<linearGradient id="lzTort" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#2a1a10"/><stop offset=".45" stop-color="#120c08"/>'
    '<stop offset=".7" stop-color="#3a2414"/><stop offset="1" stop-color="#0e0906"/></linearGradient>'
    '<radialGradient id="lzPad" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff" stop-opacity=".55"/><stop offset="1" stop-color="#e8dccb" stop-opacity=".12"/></radialGradient></defs>'
    # frame = everything outside the lens, softly out of focus (it's millimetres from the eye)
    f'<path d="M-60,-60 H1980 V1140 H-60 Z {LENS}" fill="url(#lzTort)" fill-rule="evenodd" opacity=".94" filter="url(#lzSoft)"/>'
    # chromatic fringe hugging the glass edge
    f'<g style="mix-blend-mode:screen" filter="url(#lzFr)" fill="none" stroke-width="7">'
    f'<path d="{LENS}" stroke="#ff3b4e" stroke-opacity=".55" transform="translate(4 3)"/>'
    f'<path d="{LENS}" stroke="#2ee6ff" stroke-opacity=".5" transform="translate(-5 -3) scale(.9975)"/></g>'
    f'<path d="{LENS}" fill="none" stroke="#fff" stroke-opacity=".18" stroke-width="2" transform="translate(960 540) scale(.992) translate(-960 -540)"/>'
    # clear silicone nose pad behind the bridge
    '<g transform="translate(102 520) rotate(14)" filter="url(#lzFr)"><ellipse rx="24" ry="64" fill="url(#lzPad)" stroke="#fff" stroke-opacity=".6" stroke-width="3"/>'
    '<path d="M-6,-48 q-10,40 0,92" stroke="#fff" stroke-opacity=".6" stroke-width="3" fill="none" stroke-linecap="round"/></g>'
    '</svg>'
    '<div id="lzBlur"></div><div id="lzGlare"></div>'
)


# ---------------------------------------------------------------- Stampy, the postage-stamp mascot
def stamp_svg(p, w=104, h=128):
    holes = []
    for k in range(9):           # top/bottom perforation
        x = 6 + k * 11.5
        holes += [f'<circle cx="{x:.1f}" cy="0" r="4.6"/>', f'<circle cx="{x:.1f}" cy="{h}" r="4.6"/>']
    for k in range(11):          # left/right perforation
        y = 6 + k * 11.6
        holes += [f'<circle cx="0" cy="{y:.1f}" r="4.6"/>', f'<circle cx="{w}" cy="{y:.1f}" r="4.6"/>']
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" style="overflow:visible">'
            f'<defs><mask id="{p}M"><rect width="{w}" height="{h}" fill="#fff"/><g fill="#000">{"".join(holes)}</g></mask>'
            f'<linearGradient id="{p}S" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8fd3ff"/><stop offset=".62" stop-color="#ffe2b0"/></linearGradient></defs>'
            f'<rect width="{w}" height="{h}" fill="{PAPER}" mask="url(#{p}M)"/>'
            f'<rect x="10" y="10" width="{w - 20}" height="{h - 20}" rx="2" fill="url(#{p}S)"/>'
            f'<path d="M10,{h - 32} q10.5,-7 21,0 t21,0 t21,0 t21,0 V{h - 10} H10 Z" fill="{BLUE}"/>'
            f'<path d="M10,{h - 22} q10.5,-6 21,0 t21,0 t21,0 t21,0" stroke="#fff" stroke-opacity=".7" stroke-width="2.4" fill="none"/>'
            f'<g id="{p}Sun"><circle cx="{w / 2}" cy="{h / 2 - 4}" r="29" fill="{SUN}"/>'
            f'<g stroke="{SUN}" stroke-width="4" stroke-linecap="round">'
            + "".join(f'<path d="M{w / 2},{h / 2 - 41} v-8" transform="rotate({a} {w / 2} {h / 2 - 4})"/>' for a in range(0, 360, 45)) +
            f'</g></g>'
            f'<ellipse id="{p}El" cx="{w / 2 - 10}" cy="{h / 2 - 9}" rx="3.6" ry="5.2" fill="{INK}"/>'
            f'<ellipse id="{p}Er" cx="{w / 2 + 10}" cy="{h / 2 - 9}" rx="3.6" ry="5.2" fill="{INK}"/>'
            f'<circle cx="{w / 2 - 18}" cy="{h / 2 + 1}" r="4.5" fill="#ff8a6b" opacity=".75"/><circle cx="{w / 2 + 18}" cy="{h / 2 + 1}" r="4.5" fill="#ff8a6b" opacity=".75"/>'
            f'<ellipse id="{p}Mo" cx="{w / 2}" cy="{h / 2 + 5}" rx="7" ry="2" fill="{INK}"/>'
            f'<path d="M{w / 2 - 8},{h / 2 + 3} q8,7 16,0" stroke="{INK}" stroke-width="2.6" fill="none" stroke-linecap="round"/>'
            f'<text x="{w - 14}" y="24" text-anchor="end" font-family="PlexMono" font-weight="600" font-size="12" fill="{INK}">LL</text>'
            f'</svg>')


POSTMARK = (f'<svg class="pmk" width="170" height="110" viewBox="0 0 170 110"><g fill="none" stroke="{INK}" stroke-opacity=".55" stroke-width="2.6">'
            '<circle cx="52" cy="55" r="40"/><circle cx="52" cy="55" r="31"/>'
            '<path d="M98 36 q9 -6 18 0 t18 0 t18 0 t18 0"/><path d="M98 55 q9 -6 18 0 t18 0 t18 0 t18 0"/><path d="M98 74 q9 -6 18 0 t18 0 t18 0 t18 0"/></g>'
            f'<text x="52" y="52" text-anchor="middle" font-family="PlexMono" font-weight="600" font-size="12" fill="{INK}" fill-opacity=".6">HVAR</text>'
            f'<text x="52" y="68" text-anchor="middle" font-family="PlexMono" font-size="11" fill="{INK}" fill-opacity=".6">2026</text></svg>')

AIRMAIL = f"repeating-linear-gradient(135deg,{RED} 0 20px,{PAPER} 20px 30px,{BLUE} 30px 50px,{PAPER} 50px 60px)"

CSS = FONTCSS + f"""
#flash{{display:none}}
.vr{{font-family:"Varela Round",sans-serif;font-weight:400}}
.px{{font-family:"PlexHe",sans-serif;font-weight:500}}
/* lens */
#lens{{position:absolute;left:0;top:0;width:1920px;height:1080px;pointer-events:none}}
#lzBlur{{position:absolute;inset:0;backdrop-filter:blur(5px);-webkit-backdrop-filter:blur(5px);
  -webkit-mask-image:radial-gradient(ellipse 58% 60% at 50% 47%,transparent 78%,#000 100%);mask-image:radial-gradient(ellipse 58% 60% at 50% 47%,transparent 78%,#000 100%)}}
#lzGlare{{position:absolute;left:1180px;top:-420px;width:260px;height:1500px;transform:rotate(28deg);-webkit-mask-image:linear-gradient(180deg,transparent,#000 25%,#000 45%,transparent 70%);mask-image:linear-gradient(180deg,transparent,#000 25%,#000 45%,transparent 70%);
  background:linear-gradient(90deg,rgba(255,255,255,0),rgba(255,255,255,.10) 40%,rgba(255,255,255,.04) 60%,rgba(255,255,255,0));mix-blend-mode:screen}}
#boot{{position:absolute;inset:0;background:radial-gradient(60% 70% at 50% 45%,rgba(255,244,220,0) 35%,rgba(255,236,200,.55) 80%,rgba(255,210,160,.75));opacity:0;pointer-events:none}}
/* Stampy */
#mas{{position:absolute;left:170px;top:890px;width:0;height:0}}
#mas .body{{position:absolute;left:-52px;top:-64px;width:104px;height:128px;filter:drop-shadow(0 10px 14px rgba(20,20,40,.45))}}
/* paper speech bubbles */
.bub{{position:absolute;left:246px;bottom:150px;width:max-content;max-width:900px;direction:rtl;padding:20px 40px 26px;
  background:{PAPER};border-radius:40px;color:{INK};font-family:"Varela Round",sans-serif;font-size:62px;line-height:1.25;
  box-shadow:0 18px 40px rgba(20,20,40,.32),inset 0 0 0 3px rgba(29,45,80,.08);transform-origin:0% 100%}}
.bub .tail{{position:absolute;left:-20px;bottom:18px;width:48px;height:40px;background:{PAPER};clip-path:polygon(100% 0,100% 100%,0 100%)}}
.bub .w,.pin .w,#end .w{{display:inline-block;margin:0 .1em}}
.hl{{color:{RED}}}
/* the repainted sign */
#sign{{position:absolute;left:0;top:0;width:500px;height:660px;transform-origin:0 0;opacity:0}}
#sign .face{{position:absolute;inset:0;border-radius:64px;background:#efe5d0;
  background-image:radial-gradient(120% 90% at 30% 20%,rgba(255,255,255,.35),rgba(0,0,0,0) 60%),radial-gradient(90% 60% at 80% 100%,rgba(120,90,50,.18),rgba(0,0,0,0) 70%);
  box-shadow:0 0 0 3px rgba(29,45,80,.35),0 8px 30px rgba(0,0,0,.25);display:flex;flex-direction:column;align-items:center;justify-content:center;direction:rtl;color:#1f2d4f}}
#sign .yr{{font-family:"PlexHe",sans-serif;font-weight:500;font-size:40px;color:#b8872e;letter-spacing:.04em}}
#sign .big{{font-family:"Varela Round",sans-serif;font-size:176px;line-height:.98}}
#sign .sm{{font-family:"Varela Round",sans-serif;font-size:50px;margin-top:6px}}
#sign svg{{margin:6px 0 4px}}
#sign .scan{{position:absolute;left:-6%;right:-6%;height:8px;top:0;border-radius:6px;background:linear-gradient(90deg,rgba(255,255,255,0),#fff6dc,rgba(255,255,255,0));box-shadow:0 0 24px 6px rgba(255,230,170,.8)}}
#sDet{{border:4px dashed {RED};border-radius:60px;box-shadow:0 0 0 3px rgba(251,245,230,.55)}}
#sPill{{position:absolute;left:0;top:0;width:0;height:0}}
#sPill span{{position:absolute;left:0;top:0;transform:translate(-50%,0) rotate(-7deg);white-space:nowrap;direction:rtl;padding:6px 26px 10px;border-radius:12px;
  border:5px double {RED};background:rgba(251,245,230,.9);color:{RED};font-family:"PlexHe",sans-serif;font-weight:700;font-size:40px;letter-spacing:.02em;
  box-shadow:0 8px 22px rgba(20,20,40,.3)}}
/* belfry: map pin + airmail postcard / phrasebook entry */
.pin{{position:absolute;left:0;top:0;width:0;height:0}}
.pin .mp{{position:absolute;left:-22px;top:-58px;width:44px;height:58px;filter:drop-shadow(0 5px 6px rgba(0,0,0,.4));transform-origin:50% 100%}}
.pin .bx{{position:absolute;left:0;top:26px;transform:translate(-30%,0) rotate(-2.5deg);width:max-content;padding:10px;background:{AIRMAIL};border-radius:10px;
  box-shadow:0 18px 40px rgba(20,20,40,.35);transform-origin:30% 0}}
.pin .in{{display:block;direction:rtl;background:{PAPER};padding:14px 32px 20px;border-radius:4px;color:{INK}}}
.pin .ph{{display:block;direction:ltr;text-align:right;font-family:"PlexMono",monospace;font-size:26px;color:{BLUE};letter-spacing:.04em}}
.pin .ph i{{font-style:normal;color:#8a8373}}
.pin .t1{{display:block;font-family:"Varela Round",sans-serif;font-size:54px;line-height:1.2}}
.pin .t2{{display:block;font-family:"Varela Round",sans-serif;font-size:64px;line-height:1.2}}
.pin .t2 .n{{color:{RED};font-variant-numeric:tabular-nums}}
/* ground path: dotted map line */
#gplane{{position:absolute;left:0;top:0}}
#dest{{position:absolute;left:1660px;top:760px;width:0;height:0}}
#dest .mp{{position:absolute;left:-26px;top:-68px;width:52px;height:68px;filter:drop-shadow(0 6px 6px rgba(0,0,0,.4));transform-origin:50% 100%}}
#dest .bx{{position:absolute;left:0;bottom:84px;transform:translate(-50%,0);width:max-content;direction:rtl;display:flex;align-items:center;gap:16px;padding:12px 26px 14px;
  border-radius:12px;background:{PAPER};color:{INK};box-shadow:0 14px 34px rgba(20,20,40,.35),inset 0 0 0 3px rgba(29,45,80,.12);transform-origin:50% 100%}}
#dest .t{{font-family:"Varela Round",sans-serif;font-size:48px;line-height:1.1}}
#dest .d{{font-family:"PlexHe",sans-serif;font-weight:700;font-size:36px;color:{RED};font-variant-numeric:tabular-nums}}
/* the receipt */
#order{{position:absolute;left:1020px;top:118px;width:650px;filter:drop-shadow(0 22px 30px rgba(20,20,40,.42));transform-origin:50% 0}}
#order .pp{{background:#fffdf7;padding:30px 40px 46px;color:{INK};
  -webkit-mask:conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) 50%/26px 100%;mask:conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) 50%/26px 100%}}
#order .hd{{display:flex;justify-content:center;align-items:center;gap:14px;direction:rtl;font-family:"Varela Round",sans-serif;font-size:42px}}
#order .mt{{text-align:center;font-family:"PlexMono",monospace;font-size:21px;color:#7b7668;letter-spacing:.08em;margin-top:4px}}
#order .rl{{border-top:3px dashed rgba(29,45,80,.35);margin:16px 0}}
#order .lb{{display:flex;align-items:center;gap:10px;direction:rtl;font-family:"PlexHe",sans-serif;font-weight:500;font-size:25px;color:#7b7668}}
#order .he{{direction:rtl;white-space:nowrap;font-family:"Varela Round",sans-serif;font-size:54px;line-height:1.2;margin:2px 0 10px}}
#order .hr{{direction:ltr;text-align:right;font-family:"PlexMono",monospace;font-weight:600;font-size:34px;color:{BLUE};margin-top:4px}}
#order .hr .c{{display:inline-block;white-space:pre}}
#order .it{{display:flex;justify-content:space-between;direction:rtl;font-family:"PlexHe",sans-serif;font-weight:500;font-size:30px}}
#order .it b{{font-family:"PlexMono",monospace;font-weight:600;direction:ltr}}
#order .ty{{text-align:center;font-family:"PlexMono","PlexHe",monospace;font-weight:600;font-size:24px;letter-spacing:.14em;color:{RED};margin-top:12px}}
/* end card: a postcard franked by Stampy */
#end{{position:absolute;left:96px;top:120px;width:max-content;padding:14px;background:{AIRMAIL};border-radius:12px;
  box-shadow:0 30px 70px rgba(10,10,30,.45);transform-origin:0 50%}}
#end .card{{display:flex;gap:36px;direction:ltr;background:{PAPER};padding:34px 40px 34px 48px;border-radius:5px;color:{INK}}}
#end .msg{{display:flex;flex-direction:column}}
#end .lg{{font-family:"Varela Round",sans-serif;font-size:86px;letter-spacing:.02em;line-height:1}}
#end .lg b{{font-weight:400;color:{RED}}}
#end .tgl{{direction:rtl;display:flex;gap:24px;font-family:"Varela Round",sans-serif;font-size:70px;line-height:1.2;margin-top:18px}}
#end .sb{{direction:rtl;font-family:"PlexHe",sans-serif;font-weight:500;font-size:29px;color:#5b6479;margin-top:12px}}
#end .adr{{position:relative;width:170px;border-left:3px solid rgba(29,45,80,.25);padding-left:30px}}
#end .slot{{position:relative;margin-left:auto;width:130px;height:160px}}
#end .slot svg{{width:130px;height:160px}}
#end .pmk{{position:absolute;left:-74px;top:86px;width:170px;height:110px}}
#end .ln{{height:3px;background:rgba(29,45,80,.25);margin-top:28px}}
"""

WAVES = ('<svg width="230" height="60" viewBox="0 0 230 60"><g fill="none" stroke="#1f2d4f" stroke-width="9" stroke-linecap="round">'
         '<path d="M8 20 q27 -16 54 0 t54 0 t54 0 t54 0"/><path d="M8 46 q27 -16 54 0 t54 0 t54 0 t54 0"/></g></svg>')
MIC = f'<svg width="20" height="26" viewBox="0 0 26 34"><rect x="7" y="2" width="12" height="20" rx="6" fill="#7b7668"/><path d="M3 16a10 10 0 0 0 20 0M13 26v6" stroke="#7b7668" stroke-width="3" fill="none" stroke-linecap="round"/></svg>'
SPK = f'<svg width="26" height="24" viewBox="0 0 34 30"><path d="M3 10h6l8-7v24l-8-7H3z" fill="#7b7668"/><path d="M22 9a8 8 0 0 1 0 12M26 5a13 13 0 0 1 0 20" stroke="#7b7668" stroke-width="3" fill="none" stroke-linecap="round"/></svg>'
CUP = f'<svg width="50" height="42" viewBox="0 0 54 46"><path d="M6 12h32v14a14 14 0 0 1-14 14h-4A14 14 0 0 1 6 26z" fill="{INK}"/><path d="M38 16h4a7 7 0 0 1 0 14h-5" stroke="{INK}" stroke-width="4" fill="none"/><path d="M16 2c-3 4 3 5 0 9M26 2c-3 4 3 5 0 9" stroke="{RED}" stroke-width="3" fill="none" stroke-linecap="round"/></svg>'


def MAPPIN(w, h):
    return (f'<svg class="mp" width="{w}" height="{h}" viewBox="0 0 44 58"><path d="M22 57 C22 57 3 34 3 21 A19 19 0 0 1 41 21 C41 34 22 57 22 57Z" fill="{RED}" stroke="#fff" stroke-width="3"/>'
            f'<circle cx="22" cy="21" r="7.5" fill="#fff"/></svg>')


# chat bubbles: id, [(word, t, highlight)], in, out
BUBS = [
    ("b1", [("עיר", .6, 0), ("חדשה.", .948, 1)], .45, 3.75),
    ("b2", [("אף", 1.273, 0), ("פעם", 1.691, 0), ("לא", 1.97, 0), ("היית", 2.133, 0), ("כאן.", 2.527, 0)], 1.12, 3.75),
    ("b3", [("כל", 4.4, 0), ("שלט,", 4.655, 0), ("פתאום", 5.073, 0), ("בעברית.", 5.816, 1)], 4.28, 8.2),
    ("b4", [("המגדל", 8.6, 0), ("הזה?", 9.439, 1)], 8.48, 11.7),
    ("b5", [("אספרסו?", 13.4, 1)], 13.28, 15.15),
]

html, js = [], []
H = html.append
J = js.append


def pop(sel, t, dur=.5, frm=.5, ease="back.out(3)", y=16):
    J(f'tl.fromTo("{sel}", {{opacity:0, scale:{frm}, y:{y}}}, {{opacity:1, scale:1, y:0, duration:{dur}, ease:"{ease}"}}, {t});')


# ---- lens first (everything else is "projected" inside it)
H(LENS_SVG)
J('tl.fromTo(["#lens","#lzBlur"], {opacity:0}, {opacity:1, duration:.45, ease:"power2.out"}, 0);')
H('<div id="boot"></div>')
J('tl.fromTo("#boot", {opacity:0}, {opacity:.85, duration:.22, ease:"power2.out"}, 0.02); tl.to("#boot", {opacity:0, duration:.6, ease:"power2.out"}, .26);')


# ---- ground path (12.0-13.7): dotted map line + red pin
def _bz(u, P):
    return tuple((1 - u) ** 3 * P[0][k] + 3 * (1 - u) ** 2 * u * P[1][k] + 3 * (1 - u) * u * u * P[2][k] + u ** 3 * P[3][k] for k in (0, 1))


_P = [(700, 1110), (860, 880), (1330, 990), (1645, 815)]
_N = 22
_dots = []
for _k in range(_N):
    _x, _y = _bz(_k / (_N - 1), _P)
    _dots.append(f'<circle class="gd" id="gd{_k}" cx="{_x:.0f}" cy="{_y:.0f}" r="{15 - 8.5 * _k / (_N - 1):.1f}"/>')
H('<svg id="gwrap" width="1920" height="1080" viewBox="0 0 1920 1080" style="position:absolute;left:0;top:0" data-layout-allow-overlap data-layout-allow-occlusion>'
  f'<g fill="{INK}" stroke="#fff" stroke-width="4.5" style="filter:drop-shadow(0 3px 4px rgba(0,0,0,.35))">' + "".join(_dots) + '</g>'
  f'<g id="gStart" transform="translate(700 1110)"><ellipse rx="40" ry="16" fill="none" stroke="{RED}" stroke-width="5"/></g></svg>')
J('tl.set("#gwrap", {opacity:0}, 0); tl.set("#gwrap", {opacity:1}, 11.95);')
J('tl.fromTo("#gwrap .gd", {opacity:0, scale:0, transformOrigin:"50% 50%"}, {opacity:1, scale:1, duration:.3, ease:"back.out(4)", stagger:.035}, 11.98);')
J('tl.to("#gwrap", {opacity:0, duration:.3}, 13.45);')
H(f'<div id="dest">{MAPPIN(52, 68)}<div class="bx">{CUP}<span class="t">בית הקפה</span><span class="d" id="destD">40 מ׳</span></div></div>')
J('tl.set("#dest", {opacity:0}, 0); tl.set("#dest", {opacity:1}, 12.3);')
J('tl.fromTo("#dest .mp", {opacity:0, y:-120, scaleY:1}, {opacity:1, y:0, duration:.32, ease:"power2.in"}, 12.3);')
J('tl.fromTo("#dest .mp", {scaleY:.72}, {scaleY:1, duration:.45, ease:"elastic.out(1,.4)", immediateRender:false}, 12.62);')
pop("#dest .bx", 12.55, .6, .3, "elastic.out(1,.5)", 20)
J('tl.to("#dest", {opacity:0, scale:.8, duration:.25, ease:"back.in(2)"}, 13.45);')

# ---- the sign, repainted in Hebrew (tracked homography) + rubber stamp
H('<div id="sDet" data-box="sign" data-pad="6"></div>')
J('tl.set("#sDet", {opacity:0}, 0);')
J('tl.fromTo("#sDet", {opacity:0, scale:1.15}, {opacity:1, scale:1, duration:.45, ease:"back.out(2.5)"}, 4.42);')
J('tl.to("#sDet", {opacity:.35, duration:.15, repeat:3, yoyo:true, ease:"sine.inOut"}, 4.7);')
J('tl.to("#sDet", {opacity:0, duration:.2}, 5.3);')
H('<div id="sign"><div class="face"><span class="yr">מאז 1952</span><span class="big">שער</span><span class="big">הים</span>'
  + WAVES + '<span class="sm">מאפייה ובית קפה</span></div><div class="scan"></div></div>')
J('tl.set("#sign", {opacity:1}, 5.05);')
J('tl.fromTo("#sign .face", {clipPath:"inset(0 0 100% 0 round 64px)"}, {clipPath:"inset(0 0 0% 0 round 64px)", duration:.75, ease:"power1.inOut"}, 5.07);')
J('tl.fromTo("#sign .scan", {y:0, opacity:1}, {y:655, duration:.75, ease:"power1.inOut"}, 5.07); tl.to("#sign .scan", {opacity:0, duration:.2}, 5.82);')
J('tl.fromTo("#sign .big", {scale:.6}, {scale:1, duration:.7, ease:"elastic.out(1,.45)", stagger:.12, immediateRender:false}, 5.3);')
J('tl.to("#sign", {opacity:0, duration:.3}, 8.2);')
H('<div id="sPill" data-follow="sign" data-anchor="b" data-dx="0" data-dy="18"><span>תורגם לעברית ✓</span></div>')
J('tl.set("#sPill", {opacity:0}, 0); tl.set("#sPill", {opacity:1}, 5.85);')
J('tl.fromTo("#sPill span", {opacity:0, scale:1.9}, {opacity:1, scale:1, duration:.2, ease:"power4.in"}, 5.85);')
J('tl.fromTo("#sPill span", {y:0}, {keyframes:[{y:5, duration:.05},{y:0, duration:.12}], ease:"none", immediateRender:false}, 6.05);')
J('tl.to("#sPill", {opacity:0, duration:.25}, 8.0);')

# ---- belfry: pin + airmail postcard / phrasebook entry
H('<div class="pin" id="pin" data-follow="belfry" data-anchor="b" data-dx="0" data-dy="8">' + MAPPIN(44, 58) + '<div class="bx"><span class="in">'
  '<span class="ph">zvonik <i>(n.)</i></span>'
  '<span class="t1"><span class="w">מגדל</span><span class="w">הפעמונים</span></span>'
  '<span class="t2" id="pinF"><span class="w">בן</span><span class="w n" id="pinN">500</span><span class="w">שנה</span></span></span></div></div>')
J('tl.set("#pin", {opacity:0}, 0); tl.set("#pin", {opacity:1}, 8.85);')
J('tl.fromTo("#pin .mp", {opacity:0, y:-90}, {opacity:1, y:0, duration:.28, ease:"power2.in"}, 8.85);')
J('tl.fromTo("#pin .mp", {scaleY:.7}, {scaleY:1, duration:.45, ease:"elastic.out(1,.4)", immediateRender:false}, 9.13);')
J('tl.fromTo("#pin .bx", {opacity:0, scale:.2, rotation:-14}, {opacity:1, scale:1, rotation:-2.5, duration:.7, ease:"elastic.out(1,.55)"}, 9.0);')
J('tl.fromTo("#pinF", {opacity:0}, {opacity:1, duration:.01}, 9.95);')
pop("#pinF .w", 9.97, .5, .4, "back.out(3.2)", 14)
J('tl.fromTo("#pinN", {scale:1.6}, {scale:1, duration:.6, ease:"elastic.out(1,.4)", immediateRender:false}, 10.37);')
J('tl.to("#pin", {opacity:0, duration:.25}, 11.75);')

# ---- order: a paper receipt printed out on the barista's side
H('<div id="order"><div class="pp">'
  f'<div class="hd">{CUP}<span>שער הים</span></div>'
  '<div class="mt">RACUN 0417 · 10:42</div><div class="rl"></div>'
  f'<div class="lb">{MIC}<span>אמרת</span></div>'
  '<div class="he" id="oHe">אספרסו אחד, בבקשה</div>'
  f'<div class="lb">{SPK}<span>הבריסטה שומעת</span></div>'
  '<div class="hr" id="oHr">' + "".join(f'<span class="c">{c}</span>' for c in "Jedan espresso, molim.") + '</div>'
  '<div class="rl"></div><div class="it"><span>1 × אספרסו</span><b>€2.00</b></div>'
  '<div class="ty">HVALA · <span style="letter-spacing:0;font-family:PlexHe">תודה</span></div></div></div>')
J('tl.set("#order", {opacity:0}, 0); tl.set("#order", {opacity:1}, 13.72);')
J('tl.fromTo("#order", {clipPath:"inset(0 0 100% 0)", y:-60}, {clipPath:"inset(0 0 -10% 0)", y:0, duration:.55, ease:"power2.out"}, 13.72);')
J('tl.fromTo("#order", {rotation:0}, {keyframes:[{rotation:-2.2, duration:.18},{rotation:1, duration:.2},{rotation:-.6, duration:.25}], ease:"sine.inOut", immediateRender:false}, 14.2);')
J('tl.fromTo("#oHr .c", {opacity:0}, {opacity:1, duration:.01, stagger:.022}, 14.15);')
J('tl.to("#order", {opacity:0, y:-40, duration:.22, ease:"power2.in"}, 15.0);')

# ---- paper speech bubbles from Stampy
for bid, words, tin, tout in BUBS:
    ws = "".join(f'<span class="w{" hl" if h else ""}" id="{bid}w{k}">{w}</span>' for k, (w, _, h) in enumerate(words))
    H(f'<div class="bub" id="{bid}"><span class="tail"></span>{ws}</div>')
    J(f'tl.set("#{bid}", {{opacity:0}}, 0); tl.set("#{bid}", {{opacity:1}}, {tin});')
    J(f'tl.fromTo("#{bid}", {{scale:.15, rotation:-6}}, {{scale:1, rotation:0, duration:.7, ease:"elastic.out(1,.55)"}}, {tin});')
    for k, (w, t, h) in enumerate(words):
        pop(f"#{bid}w{k}", t, .45, .5 if not h else .3, "back.out(3.4)", 18)
    J(f'tl.to("#{bid}", {{opacity:0, scale:.7, duration:.22, ease:"back.in(2)"}}, {tout});')
J('tl.to("#b1", {y:-128, duration:.5, ease:"back.out(2.2)"}, 1.12); tl.to("#b1 .tail", {opacity:0, duration:.15}, 1.12);')

# ---- end card: postcard (Stampy flies up and becomes its stamp)
H('<div id="end"><div class="card"><div class="msg"><span class="lg">LUMEN <b>LENS</b></span>'
  '<div class="tgl"><span class="w" id="t0">העולם,</span><span class="w" id="t1">בשפה</span><span class="w hl" id="t2">שלך.</span></div>'
  '<div class="sb" id="esb">משקפיים חכמים · מתרגמים את העולם בזמן אמת</div></div>'
  '<div class="adr"><div class="slot" id="eSlot"><span id="eSt">' + stamp_svg("es", 104, 128).replace('width="104" height="128"', 'width="150" height="185"', 1) + '</span>'
  + POSTMARK + '</div><div class="ln"></div><div class="ln"></div></div></div></div>')
J('tl.set("#end", {opacity:0}, 0); tl.set("#end", {opacity:1}, 15.42);')
J('tl.fromTo("#end", {scale:.3, rotation:-10, opacity:0}, {scale:1, rotation:-1.5, opacity:1, duration:.55, ease:"back.out(1.7)"}, 15.42);')
J('tl.set("#eSt", {opacity:0}, 0); tl.set("#eSt", {opacity:1}, 15.66);')
J('tl.fromTo("#end .pmk", {opacity:0, scale:1.5}, {opacity:1, scale:1, duration:.16, ease:"power4.in"}, 15.78);')
pop("#end .lg", 15.56, .5, .6, "back.out(2.6)", 0)
pop("#t0", 15.72, .5, .4, "back.out(3.2)", 20)
pop("#t1", 16.23, .5, .4, "back.out(3.2)", 20)
pop("#t2", 16.88, .6, .25, "back.out(3.6)", 20)
J('tl.fromTo("#esb", {opacity:0, y:12}, {opacity:1, y:0, duration:.4, ease:"power2.out"}, 17.1);')

# ---- Stampy (above bubbles & card)
H('<div id="mas"><div class="body" id="masB">' + stamp_svg("ms") + '</div></div>')
J('tl.set("#mas", {opacity:0}, 0); tl.set("#mas", {opacity:1}, .2);')
J('tl.fromTo("#masB", {scale:0, rotation:-40}, {scale:1, rotation:0, duration:.8, ease:"elastic.out(1,.45)"}, .2);')
J('tl.to("#mas", {x:__DX__, y:__DY__, scale:1.25, duration:.55, ease:"back.inOut(1.4)"}, 15.1);')
J('tl.to("#mas", {opacity:0, duration:.06}, 15.66);')

J(r"""
function sq2q(q, W, H) {
  const [x0,y0,x1,y1,x2,y2,x3,y3] = q;
  const dx1=x1-x2, dx2=x3-x2, dy1=y1-y2, dy2=y3-y2, sx=x0-x1+x2-x3, sy=y0-y1+y2-y3;
  const det = dx1*dy2 - dx2*dy1;
  const g = (sx*dy2 - dx2*sy)/det, h = (dx1*sy - sx*dy1)/det;
  const a = x1-x0+g*x1, b = x3-x0+h*x3, d = y1-y0+g*y1, e = y3-y0+h*y3;
  return `matrix3d(${a/W},${d/W},0,${g/W},${b/H},${e/H},0,${h/H},0,0,1,0,${x0},${y0},0,1)`;
}
const _p = window.onPlace;
window.onPlace = (t) => {
  _p && _p(t);
  const b = boxAt("sign", t);
  if (b) {
    const w = b[2]-b[0], h = b[3]-b[1];
    const L = b[0]+w*.075, R = b[2]-w*.075, T0 = b[1]+h*.05, B0 = b[3]-h*.045, k = h*.012;
    document.getElementById("sign").style.transform = sq2q([L,T0, R,T0+k, R,B0-k, L,B0], 500, 660);
  }
  const ev = (typeof ENV !== "undefined") ? (ENV[Math.max(0, Math.min(ENV.length-1, Math.round(t*24)))] || 0) : 0;
  // Stampy: idle sway, VO lip-sync, blink every 2.7s
  const live = t > 1.0 && t < 15.1;
  const body = document.getElementById("masB");
  if (live) body.style.transform = `translateY(${(3.5*Math.sin(t*3.0)).toFixed(2)}px) rotate(${(4*Math.sin(t*2.1)).toFixed(2)}deg) scale(${(1 + .07*ev).toFixed(3)})`;
  const talk = t < 15.1 ? ev : 0;
  document.getElementById("msMo").setAttribute("ry", (1.5 + 8*talk).toFixed(2));
  document.getElementById("msMo").setAttribute("rx", (6 + 2*talk).toFixed(2));
  const bl = (t % 2.7) < .12 || (t % 7.3) < .1;
  for (const id of ["msEl","msEr","esEl","esEr"]) document.getElementById(id).setAttribute("ry", bl ? "0.8" : "5.2");
  document.getElementById("msSun").setAttribute("transform", `rotate(${(t*14)%360} 52 60)`);
  document.getElementById("esSun").setAttribute("transform", `rotate(${(t*14)%360} 52 60)`);
  if (t > 12.6) for (let k = 0; k < 22; k++) { const ph = ((t*1.4 - k/11) % 1 + 1) % 1; document.getElementById("gd"+k).style.fillOpacity = (0.55 + 0.45*Math.pow(1-ph, 3)).toFixed(3); }
  const u = Math.max(0, Math.min(1, (t-12.55)/(13.3-12.55))), m = Math.round(40*(1-u*u*(3-2*u)));
  document.getElementById("destD").textContent = m > 0 ? m + " מ׳" : "הגעת!";
  document.getElementById("lzGlare").style.transform = `translateX(${(-40*Math.sin(t*.35)).toFixed(1)}px) rotate(28deg)`;
};
""")

SPEC_JS = "\n".join(js)

SPEC = {
    "theme": "he_bold",
    "palette": {"acc": BLUE, "ink": INK, "lt": "#ffffff", "panel": PAPER, "sub": "#5b6479"},
    "music_vol": 0.5,
    "plate_vol": 0.35,
    "vo_name": "E9_glasses_hk_vo",
    "project_suffix": "-bespoke",
    "elements": [],
    "css": CSS,
    "html_front": "".join(html),
    "js": SPEC_JS.replace("__DX__", "763").replace("__DY__", "-665"),
    "assets": ASSETS,
}
SPEC["env"] = json.loads((T / "E9_glasses_hk_env.json").read_text())
