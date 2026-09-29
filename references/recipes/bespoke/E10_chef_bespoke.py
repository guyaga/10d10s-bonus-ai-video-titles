"""E10_chef BESPOKE - EMBER, a Tel Aviv kitchen at night.
Visual language (nothing from the stock kine/tape/tag/lockup kit):
  * the order comes in as a THERMAL KITCHEN TICKET that prints line by line under a steel ticket rail (Miriam Libre = Israeli receipt face)
  * every VO line is set in FRANK RUHL LIBRE and condenses out of smoke (per-word SVG turbulence + blur), then drifts away as steam
  * the 260 degree sear is a FLAME-SHAPED HEAT GAUGE that fills from the root
  * the ticket is the SIGNATURE: a big in-focus thermal slip (a third of the frame) on a steel rail, with a masking-tape
    station label (RUBIK DIRT stencil: 'גריל · 2') and a running ticket-rail time strip
  * the chef's notes are GREASE-PENCIL PRINT (AMATIC SC Hebrew, stroked): chalk on the dark shots, wax pencil on porcelain
  * ember sparks rise behind the smoke words; 'באש' is ember-lit orange
  * the KITCHEN owns the ending: the pass printer prints the CTA line, the ticket is torn off, spiked on the rail, and a
    red 'בוצע ✓' rubber stamp lands on it
Shots: flame 0-1.75 | slicing 1.75-4.5 | jus 4.5-6.83 | salt 6.83-10.42 | hero 10.42-15.07
VO: הכול 0.00 מתחיל 0.72 באש 1.28 | 260 2.12 מעלות 2.54 בחוץ 3.03 ורוד 3.42 מבפנים 3.93 |
    רוטב 4.95 שמצטמצם 5.60 6 6.55 שעות 6.69 | מלח 7.62 עד 8.21 הגרגר 8.61 האחרון 9.55 | אמבר 11.00 הערב 11.70 בתל 12.32 אביב 13.00
"""
from pathlib import Path

FONTS = Path(__file__).resolve().parent.parent.parent / "shared/fonts"
HE = "U+0590-05FF,U+FB1D-FB4F,U+200C-2010,U+20AA,U+25CC"
LA = "U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2199,U+2212,U+2215"
FACES = {"Frank Ruhl Libre": ("frank-ruhl-libre", (300, 500, 700, 900)), "Amatic SC": ("amatic-sc", (700,)), "Rubik Dirt": ("rubik-dirt", (400,)),
         "Miriam Libre": ("miriam-libre", (400, 700))}
assets, face_css = {}, []
for fam, (stem, ws) in FACES.items():
    for w in ws:
        for sub, rng in (("hebrew", HE), ("latin", LA)):
            f = f"{stem}-{sub}-{w}-normal.woff2"
            assets[f"fonts/{f}"] = str(FONTS / f)
            face_css.append(f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:normal;'
                            f'src:url(assets/fonts/{f}) format("woff2");unicode-range:{rng}}}')

# ---------------- thermal ticket (prints line by line) ----------------
TK = [  # (html, class, height px, print time)
    ('<b class="logo">EMBER</b>', "c", 66, 0.10),
    ("מטבח · תל אביב", "c sm", 42, 0.22),
    ("", "dash", 28, 0.32),
    ('<span>שולחן 7</span><span class="lt">21:40</span>', "row", 56, 0.42),
    ('<span>סועדים: 2</span><span class="lt">#0417</span>', "row sm", 44, 0.52),
    ("", "dash", 28, 0.60),
    ("1 × אנטריקוט 350 ג׳", "", 56, 0.70),
    ("יישון יבש 28 יום", "ind sm", 44, 0.80),
    ("מדיום-רייר", "ind sm", 44, 0.90),
    ("1 × רוטב יין אדום", "", 56, 1.00),
    ("פתיתי מלח ים", "ind sm", 44, 1.10),
    ("", "dash", 28, 1.18),
    ("*** פייר! ***", "fire", 78, 1.28),
]
tk_html, tk_js, y = [], [], 22
for n, (h, cls, hh, at) in enumerate(TK):
    tk_html.append(f'<div class="tkl {cls}" id="tk{n}" style="height:{hh}px">{h}</div>')
    y += hh
    tk_js.append(f'tl.fromTo("#tk{n}", {{clipPath:"inset(0 0 0 100%)"}}, {{clipPath:"inset(0 0 0 0%)", duration:.14, ease:"steps(7)"}}, {at});')
    tk_js.append(f'tl.to("#tkP", {{height:{y + 30}, duration:.1, ease:"power1.out"}}, {at - .04});')

# ---- hero ticket: the pass printer prints the CTA
TK2 = [
    ('<b class="logo">EMBER</b>', "c", 64, 10.98),
    ("מטבח · תל אביב", "c sm", 40, 11.14),
    ("", "dash", 26, 11.26),
    ('הערב · <span class="lt">20:30</span>', "", 52, 11.72),
    ("שולחן ל-2 · #0418", "sm", 42, 12.30),
    ("", "dash", 26, 12.46),
    ("הזמינו שולחן · EMBER · תל אביב", "cta", 74, 12.62),
]
tk2_html, tk2_js, y2 = [], [], 22
for n, (h, cls, hh, at) in enumerate(TK2):
    tk2_html.append(f'<div class="tkl {cls}" id="tq{n}" style="height:{hh}px">{h}</div>')
    y2 += hh
    tk2_js.append(f'tl.fromTo("#tq{n}", {{clipPath:"inset(0 0 0 100%)"}}, {{clipPath:"inset(0 0 0 0%)", duration:{.26 if cls == "cta" else .14}, ease:"steps({12 if cls == "cta" else 7})"}}, {at});')
    tk2_js.append(f'tl.to("#tqP", {{height:{y2 + 30}, duration:.1, ease:"power1.out"}}, {at - .04});')

# ember sparks (positions computed per frame from t -> seek-safe)
SPARKS = "".join(f'<i id="sp{i}"></i>' for i in range(46))

FLAME = "M50,148 C20,148 5,126 8,100 C11,76 28,64 29,42 C40,53 44,63 42,74 C53,58 60,34 50,4 C75,25 93,58 93,95 C93,127 77,148 50,148 Z"


def words(ids_words, cls=""):
    return " ".join(f'<span class="w {cls}" id="{i}">{w}</span>' for i, w in ids_words)


HTML = f"""
<svg id="fxdefs" width="0" height="0" style="position:absolute;left:0;top:0"><defs></defs></svg>
<div class="scr" id="sA"></div><div class="scr" id="sB"></div><div class="scr" id="sBt"></div><div class="scr" id="sH"></div>

<div id="sparks">{SPARKS}</div>
<!-- SHOT A : the order prints -->
<div id="rail"><i></i><i class="clip"></i>
  <div id="tstrip"><div id="tsIn">{''.join(f'<span data-t="21:{m:02d}"></span>' for m in range(36, 44))}</div><b id="tsNow"></b></div>
  <div class="tape" id="tapeA">גריל · 2</div>
</div>
<div id="tk"><div id="tkP">{''.join(tk_html)}</div></div>
<div class="blk" id="hA">
  <div class="row1">{words([("a1", "הכול"), ("a2", "מתחיל")])}</div>
  <div class="row2">{words([("a3", "באש.")], "fire")}</div>
</div>

<!-- SHOT B : flame gauge + pink centre -->
<div id="gauge">
  <svg id="gF" width="170" height="255" viewBox="-6 -6 112 166">
    <defs>
      <linearGradient id="gGr" x1="0" y1="1" x2="0" y2="0">
        <stop offset="0" stop-color="#6e1206"/><stop offset=".45" stop-color="#ff4d12"/><stop offset=".8" stop-color="#ffab3d"/><stop offset="1" stop-color="#fff0c2"/>
      </linearGradient>
      <clipPath id="gClip"><path d="{FLAME}"/></clipPath>
    </defs>
    <path d="{FLAME}" fill="rgba(20,8,4,.55)"/>
    <g clip-path="url(#gClip)"><rect id="gLvl" x="-10" y="150" width="120" height="170" fill="url(#gGr)"/></g>
    <path id="gOut" d="{FLAME}" fill="none" stroke="#f6e6cc" stroke-width="2.4"/>
    <g stroke="#f6e6cc" stroke-width="1.6" opacity=".8">
      <line x1="97" y1="148" x2="106" y2="148"/><line x1="97" y1="100" x2="104" y2="100"/><line x1="97" y1="52" x2="104" y2="52"/><line x1="92" y1="16" x2="106" y2="16"/>
    </g>
  </svg>
  <div class="gcol">
    <div class="gnum" id="gN">0<i>°</i></div>
    <div class="glab">{words([("b2", "מעלות"), ("b3", "בחוץ.")])}</div>
  </div>
</div>
<div class="note chalk" id="nB">
  <div id="nB1">יישון יבש · 28 יום</div>
  <svg width="260" height="150" viewBox="0 0 260 150"><path id="arB" class="arr" d="M200,10 C170,70 110,100 30,120 M52,98 L30,120 L58,132"/></svg>
</div>
<div class="blk" id="hB">
  <div class="row1">{words([("b4", "ורוד")], "pink")}</div>
  <div class="row2">{words([("b5", "מבפנים.")])}</div>
</div>

<!-- SHOT C : jus on porcelain -->
<div class="blk ink" id="hC"><div class="row1">{words([("c1", "רוטב")])}</div></div>
<div class="note pencil" id="nC">
  <div><span id="c2">שמצטמצם</span></div>
  <div><span id="c3"><b class="six">6<svg class="ring" width="92" height="92" viewBox="0 0 110 110"><path id="rgC" d="M62,8 C28,4 6,30 10,60 C14,92 52,104 80,90 C104,78 106,40 86,22 C76,13 66,10 52,12"/></svg></b> שעות</span></div>
  <svg class="arw" width="200" height="120" viewBox="0 0 200 120"><path id="arC" class="arr" d="M190,30 C150,20 90,30 30,78 M40,54 L28,80 L56,84"/></svg>
</div>

<!-- SHOT D : salt -->
<div class="blk ink" id="hD1"><div class="row1">{words([("d1", "מלח.")])}</div></div>
<div class="blk ink" id="hD2">
  <div class="row1">{words([("d2", "עד"), ("d3", "הגרגר")])}</div>
  <div class="row2">{words([("d4", "האחרון.")])}</div>
</div>
<div class="note pencil" id="nD">
  <svg width="170" height="150" viewBox="0 0 170 150"><path id="arD" class="arr" d="M30,140 C40,80 80,40 150,20 M122,10 L152,20 L134,44"/></svg>
  <div id="nD1">פתיתי מלח ים, ביד</div>
</div>

<!-- HERO : the pass printer prints the CTA; torn, spiked on the rail, stamped -->
<div id="hrail"><i></i><div class="tape" id="tapeH">פס · מוכן</div></div>
<div id="spike"><i></i></div>
<div id="tk2"><div id="tqP">{''.join(tk2_html)}</div>
  <div id="stamp"><span>בוצע</span><svg width="58" height="50" viewBox="0 0 58 50"><path d="M5,27 L21,43 L53,6"/></svg></div>
</div>
<div id="prn"><div class="slot"></div><b class="led"></b><span>EMBER · PASS</span></div>
<div id="mh">
  <div id="mL"><div>{words([("h1", "הערב,")])}</div><div>{words([("h2", "בתל"), ("h3", "אביב.")])}</div></div>
</div>
"""

CSS = "".join(face_css) + """
:root{--cream:#f6e9d2;--ink:#24130c;--ember:#ff8a3d}
.scr{position:absolute;inset:0;opacity:0;pointer-events:none}
#sA{background:linear-gradient(20deg,rgba(8,4,2,.82) 0%,rgba(8,4,2,.45) 32%,transparent 58%)}
#sB{background:radial-gradient(ellipse 900px 520px at 0% 100%,rgba(12,6,3,.8),rgba(12,6,3,.35) 55%,transparent 80%)}
#sBt{background:radial-gradient(ellipse 1100px 640px at 100% 0%,rgba(8,4,2,.9),rgba(8,4,2,.55) 50%,transparent 80%)}
#sH{background:radial-gradient(ellipse 1300px 620px at 50% 18%,rgba(6,3,2,.55),transparent 70%)}
.w{display:inline-block;white-space:nowrap}
.blk{position:absolute;direction:rtl;font-family:"Frank Ruhl Libre",serif;color:var(--cream);opacity:0;
  text-shadow:0 4px 30px rgba(0,0,0,.75),0 1px 4px rgba(0,0,0,.6)}
.blk .row1,.blk .row2{white-space:nowrap}
.blk.ink{color:#150a05;text-shadow:0 1px 14px rgba(255,255,255,.35)}
/* A */
#hA{left:96px;bottom:118px;text-align:right}
#hA .row1{font-size:92px;font-weight:500;line-height:1.05}
#hA .row2{font-size:250px;font-weight:900;line-height:.92;margin-top:4px}
.w.fire{color:#ff7a22;text-shadow:0 0 38px rgba(255,90,10,.8),0 0 90px rgba(255,60,0,.5),0 6px 30px rgba(0,0,0,.6)}
#sparks{position:absolute;inset:0;pointer-events:none}
#sparks i{position:absolute;left:0;top:0;width:4px;height:9px;border-radius:50%;opacity:0;
  background:radial-gradient(#fff4c8,#ffb040 45%,#ff5a0a 80%);box-shadow:0 0 8px 2px rgba(255,120,20,.75),0 0 18px 4px rgba(255,70,0,.35)}
#rail{position:absolute;left:880px;top:30px;width:1040px;height:30px;opacity:0;z-index:3}
#rail>i{position:absolute;inset:0;border-radius:4px;background:linear-gradient(180deg,#e9edf0,#9aa3a9 45%,#5b6368 55%,#c5ccd1);box-shadow:0 6px 16px rgba(0,0,0,.6)}
#rail>i.clip{left:680px;right:auto;width:60px;top:-7px;bottom:-12px;border-radius:3px;background:linear-gradient(90deg,#7c858b,#dfe4e7,#7c858b)}
.tape{position:absolute;direction:rtl;font-family:"Rubik Dirt","Rubik",sans-serif;font-weight:400;color:#1c1a18;white-space:nowrap;
  background:linear-gradient(180deg,rgba(236,222,178,.97),rgba(222,204,156,.97));padding:6px 22px 4px;box-shadow:0 3px 8px rgba(0,0,0,.45);
  -webkit-mask:linear-gradient(90deg,transparent 0,#000 5px calc(100% - 5px),transparent 100%);mask:linear-gradient(90deg,transparent 0,#000 5px calc(100% - 5px),transparent 100%)}
#tapeA{left:60px;top:-10px;font-size:40px;line-height:44px;transform:rotate(-3deg)}
#tstrip{position:absolute;left:14px;top:50px;width:360px;height:34px;overflow:hidden;background:#f3efe4;box-shadow:0 4px 10px rgba(0,0,0,.5);
  border-top:2px solid #cfc7b4}
#tsIn{position:absolute;left:0;top:0;display:flex;height:34px;white-space:nowrap;
  background:repeating-linear-gradient(90deg,#2b2621 0 2px,transparent 2px 22px) 0 0/100% 8px no-repeat}
#tsIn span::before{content:attr(data-t)}
#tsIn span{display:block;width:110px;flex:none;box-sizing:border-box;font-family:"Space Mono",monospace;font-weight:700;font-size:17px;line-height:40px;color:#2b2621;padding-left:6px;
  border-left:2px solid #2b2621}
#tsNow{position:absolute;left:168px;top:0;bottom:0;width:3px;background:#e23b12;box-shadow:0 0 6px rgba(226,59,18,.8)}
#tk{position:absolute;left:1270px;top:52px;width:620px;opacity:0;filter:drop-shadow(0 22px 30px rgba(0,0,0,.6));z-index:2;transform-origin:50% 0}
#tkP,#tqP{height:0;overflow:hidden;background:linear-gradient(180deg,#fbf8f1,#f1ece0);padding:0 34px;box-sizing:border-box;
  -webkit-mask:linear-gradient(#000 0 0) top/100% calc(100% - 13px) no-repeat,conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) bottom/22px 13px repeat-x;
  mask:linear-gradient(#000 0 0) top/100% calc(100% - 13px) no-repeat,conic-gradient(from -45deg at bottom,#0000,#000 1deg 89deg,#0000 90deg) bottom/22px 13px repeat-x}
#tkP::before,#tqP::before{content:"";display:block;height:22px}
.tkl{direction:rtl;font-family:"Miriam Libre","Space Mono",monospace;font-weight:700;font-size:39px;line-height:56px;color:#26221e;
  white-space:nowrap;clip-path:inset(0 0 0 100%);letter-spacing:.01em}
.tkl .lt{font-family:"Space Mono",monospace;font-weight:700}
.tkl.c{text-align:center}
.tkl.sm{font-size:31px;font-weight:400;line-height:44px;color:#4a443d}
.tkl.ind{padding-right:46px}
.tkl.row{display:flex;justify-content:space-between}
.tkl.dash{background:repeating-linear-gradient(90deg,#3a342e 0 11px,transparent 11px 20px) 0 50%/100% 3px no-repeat}
.tkl .logo{display:inline-block;font-family:"Miriam Libre",monospace;font-weight:700;font-size:54px;letter-spacing:.04em;line-height:66px}
.tkl.fire{text-align:center;background:#1d1a17;color:#fbf8f1;font-size:44px;line-height:78px;margin-top:4px}
/* B */
#gauge{position:absolute;left:78px;top:772px;display:flex;align-items:flex-end;gap:14px;opacity:0;direction:ltr}
#gF{overflow:visible;filter:drop-shadow(0 0 22px rgba(255,90,20,.35))}
.gcol{display:flex;flex-direction:column;align-items:flex-start;padding-bottom:10px}
.gnum{font-family:"Frank Ruhl Libre",serif;font-weight:900;font-size:180px;line-height:.86;color:var(--cream);font-variant-numeric:tabular-nums;
  text-shadow:0 4px 30px rgba(0,0,0,.75)}
.gnum i{font-style:normal;color:var(--ember);font-weight:500}
.glab{direction:rtl;font-family:"Frank Ruhl Libre",serif;font-weight:500;font-size:58px;line-height:1.1;color:var(--cream);text-shadow:0 3px 20px rgba(0,0,0,.8)}
#hB{right:110px;top:70px;text-align:right}
#hB .row1{font-size:230px;font-weight:900;line-height:.95}
#hB .row2{font-size:96px;font-weight:500;line-height:1.05;margin-top:-6px}
.w.pink{color:#f7b2b7;text-shadow:0 0 50px rgba(247,120,140,.35),0 4px 30px rgba(0,0,0,.7)}
.note{position:absolute;direction:rtl;font-family:"Amatic SC",sans-serif;font-weight:700;opacity:0;letter-spacing:.02em;-webkit-text-stroke:1.6px currentColor}
.note.chalk{color:#f3efe6;text-shadow:0 0 1px rgba(255,255,255,.9),0 0 10px rgba(255,255,255,.18),0 3px 16px rgba(0,0,0,.85)}
.note.chalk>*{filter:url(#chalkF)}
.note.pencil{color:#2a1208;text-shadow:0 1px 0 rgba(255,255,255,.4)}
.arr{fill:none;stroke-linecap:round;stroke-linejoin:round;stroke-width:5}
.chalk .arr{stroke:#f3efe6}.pencil .arr{stroke:#3a1d10}
#nB{right:120px;top:90px;font-size:86px;line-height:1;text-align:right}
#nB svg{display:block;margin:4px 120px 0 auto;overflow:visible}
/* C */
#hC{right:110px;top:250px}
#hC .row1{font-size:250px;font-weight:900;line-height:1}
#nC{right:120px;top:560px;font-size:96px;line-height:1.05;text-align:right}
#nC>div>span{display:inline-block;line-height:1.28}
#nC .six{position:relative;display:inline-block;font-weight:700;padding:0 6px;color:#8e2412}
#nC .ring{position:absolute;left:50%;top:50%;transform:translate(-60%,-46%);overflow:visible}
#nC .ring path{fill:none;stroke:#b3311a;stroke-width:5;stroke-linecap:round}
#nC .arw{position:absolute;left:-210px;top:10px;overflow:visible}
/* D */
#hD1{right:100px;top:30px}
#hD1 .row1{font-size:240px;font-weight:900;line-height:1}
#hD2{right:110px;top:790px;text-align:right}
#hD2 .row1{font-size:96px;font-weight:500;line-height:1.05}
#hD2 .row2{font-size:120px;font-weight:900;line-height:1}
#nD{left:70px;top:720px;font-size:84px;line-height:1}
#nD svg{display:block;margin-left:260px;overflow:visible}
/* HERO : the pass */
#hrail{position:absolute;left:560px;top:22px;width:880px;height:30px;opacity:0;z-index:3}
#hrail>i{position:absolute;inset:0;border-radius:4px;background:linear-gradient(180deg,#e9edf0,#9aa3a9 45%,#5b6368 55%,#c5ccd1);box-shadow:0 6px 16px rgba(0,0,0,.6)}
#tapeH{left:-14px;top:-6px;font-size:36px;line-height:40px;transform:rotate(2.5deg)}
#spike{position:absolute;left:754px;top:30px;width:12px;height:92px;opacity:0;z-index:6}
#spike i{position:absolute;left:3px;top:0;width:6px;height:100%;background:linear-gradient(90deg,#6b737a,#eef1f3 45%,#7d868c);
  clip-path:polygon(0 0,100% 0,100% 82%,50% 100%,0 82%)}
#prn{position:absolute;left:1270px;top:-6px;width:640px;height:66px;opacity:0;z-index:5;border-radius:0 0 10px 10px;
  background:linear-gradient(180deg,#2c2c2e,#161617 70%,#0c0c0d);box-shadow:0 10px 24px rgba(0,0,0,.7),inset 0 -2px 0 rgba(255,255,255,.08)}
#prn .slot{position:absolute;left:24px;right:24px;bottom:10px;height:7px;border-radius:4px;background:#000;box-shadow:inset 0 2px 3px rgba(0,0,0,.9),0 1px 0 rgba(255,255,255,.12)}
#prn .led{position:absolute;right:26px;top:16px;width:10px;height:10px;border-radius:50%;background:#3dff7a;box-shadow:0 0 10px #3dff7a}
#prn span{position:absolute;left:26px;top:12px;font-family:"Space Mono",monospace;font-weight:700;font-size:15px;letter-spacing:.2em;color:#8d8d90}
#tk2{position:absolute;left:1280px;top:48px;width:620px;opacity:0;filter:drop-shadow(0 22px 30px rgba(0,0,0,.6));z-index:4;transform-origin:50% 0}
.tkl.cta{text-align:center;background:#1d1a17;color:#fbf8f1;font-size:35px;line-height:74px;margin:0 -12px}
#stamp{position:absolute;left:30px;top:130px;display:flex;align-items:center;gap:10px;direction:rtl;padding:2px 20px 0 16px;opacity:0;
  border:6px solid #c9231a;border-radius:14px;color:#c9231a;font-family:"Rubik Dirt","Rubik",sans-serif;font-size:70px;line-height:88px;
  transform:rotate(-11deg);mix-blend-mode:multiply}
#stamp svg{overflow:visible}#stamp path{fill:none;stroke:#c9231a;stroke-width:9;stroke-linecap:round;stroke-linejoin:round}
#mh{position:absolute;left:84px;top:96px;direction:rtl}
#mL{direction:rtl;font-family:"Frank Ruhl Libre",serif;font-weight:700;font-size:118px;line-height:1.08;color:var(--cream);text-align:right;white-space:nowrap;
  text-shadow:0 4px 30px rgba(0,0,0,.85),0 1px 4px rgba(0,0,0,.6)}
#mL .w{opacity:0}
#wm{z-index:5}
"""

LEVEL = """
// ---- smoke condense / steam dissolve (per-element SVG turbulence, fully tl-driven) ----
const SVGNS = "http://www.w3.org/2000/svg", FXD = document.querySelector("#fxdefs defs");
let _fx = 0;
(function(){ const f = document.createElementNS(SVGNS, "filter"); f.setAttribute("id", "chalkF");
  f.innerHTML = '<feTurbulence type="fractalNoise" baseFrequency="1.1" numOctaves="1" seed="4" result="n"/>' +
    '<feColorMatrix in="n" type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  -2.2 0 0 0 1.95" result="m"/>' +
    '<feComposite in="SourceGraphic" in2="m" operator="in"/>'; FXD.appendChild(f); })();
function smokeF(el) {
  const id = "sm" + (_fx++), f = document.createElementNS(SVGNS, "filter");
  f.setAttribute("id", id); f.setAttribute("x", "-25%"); f.setAttribute("y", "-60%"); f.setAttribute("width", "150%"); f.setAttribute("height", "220%");
  f.innerHTML = '<feTurbulence type="fractalNoise" baseFrequency="0.009 0.028" numOctaves="2" seed="' + (3 + _fx * 11) + '" result="n"/>' +
    '<feDisplacementMap in="SourceGraphic" in2="n" scale="0" xChannelSelector="R" yChannelSelector="G" result="d"/>' +
    '<feGaussianBlur in="d" stdDeviation="0"/>';
  FXD.appendChild(f);
  el.style.filter = "url(#" + id + ")";
  return { d: f.querySelector("feDisplacementMap"), b: f.querySelector("feGaussianBlur") };
}
function smokeIn(sel, at, dur = 0.85, rise = 26, amt = 130) {
  document.querySelectorAll(sel).forEach((el) => {
    const s = el._sm || (el._sm = smokeF(el));
    tl.fromTo(el, { opacity: 0, y: rise }, { opacity: 1, y: 0, duration: dur, ease: "sine.out", immediateRender: false }, at);
    tl.fromTo(s.d, { attr: { scale: amt } }, { attr: { scale: 0 }, duration: dur * 1.15, ease: "sine.out", immediateRender: false }, at);
    tl.fromTo(s.b, { attr: { stdDeviation: Math.min(16, amt / 6) } }, { attr: { stdDeviation: 0 }, duration: dur, ease: "sine.out", immediateRender: false }, at);
  });
}
function smokeOut(sel, at, dur = 0.6) {
  document.querySelectorAll(sel).forEach((el) => {
    const s = el._sm || (el._sm = smokeF(el));
    tl.fromTo(el, { opacity: 1, y: 0 }, { opacity: 0, y: -34, duration: dur, ease: "sine.in", immediateRender: false }, at);
    tl.fromTo(s.d, { attr: { scale: 0 } }, { attr: { scale: 140 }, duration: dur, ease: "sine.in", immediateRender: false }, at);
    tl.fromTo(s.b, { attr: { stdDeviation: 0 } }, { attr: { stdDeviation: 14 }, duration: dur, ease: "sine.in", immediateRender: false }, at);
  });
}
function draw(sel, at, dur) {
  document.querySelectorAll(sel).forEach((p) => { const L = p.getTotalLength ? p.getTotalLength() : 600;
    p.style.strokeDasharray = L; p.style.strokeDashoffset = L;
    tl.fromTo(p, { strokeDashoffset: L }, { strokeDashoffset: 0, duration: dur, ease: "sine.inOut", immediateRender: false }, at); });
}
function show(sel, at, dur = .5) { tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: dur, ease: "sine.out", immediateRender: false }, at); }
function hide(sel, at, dur = .4) { tl.fromTo(sel, { opacity: 1 }, { opacity: 0, duration: dur, ease: "sine.in", immediateRender: false }, at); }
function wordsOf(parent) { return [...document.querySelectorAll(parent + " .w")].map(e => "#" + e.id); }

// block containers are always visible; their words carry the fades
["#hA", "#hB", "#hC", "#hD1", "#hD2"].forEach(b => tl.set(b, { opacity: 1 }, 0));
document.querySelectorAll(".blk .w, #mL .w, #c2, #c3").forEach(w => { w.style.opacity = 0; });

// ================= SHOT A 0-1.75 : the ticket prints, "everything starts in fire" =================
show("#sA", 0, .4);
show("#rail", 0, .3);
tl.set("#tk", { opacity: 1 }, .06);
""" + "\n".join(tk_js) + """
tl.fromTo("#tk", { rotation: 0 }, { rotation: -1.2, duration: 1.4, ease: "sine.inOut", immediateRender: false }, .3);
smokeIn("#a1", 0.02, .7); smokeIn("#a2", 0.72, .7);
smokeIn("#a3", 1.22, .42, 18);
smokeOut("#tk", 1.5, .3); smokeOut("#a1,#a2", 1.5, .3); smokeOut("#a3", 1.9, .35);
hide("#rail", 1.55, .2); hide("#sA", 1.62, .13);

// ================= SHOT B 1.75-4.5 : the flame gauge, pink inside =================
show("#sB", 1.75, .3); show("#sBt", 1.75, .3);
smokeIn("#gauge", 2.0, .5, 20);
smokeIn("#b2", 2.54, .6); smokeIn("#b3", 3.03, .6);
// chef's chalk note on the dark top-right, then the pink centre takes its place
smokeIn("#nB", 2.15, .6, 14); draw("#arB", 2.4, .6);
smokeOut("#nB", 3.12, .35);
smokeIn("#b4", 3.4, .6); smokeIn("#b5", 3.9, .36);
smokeOut("#gauge,#b4,#b5", 4.3, .2);
hide("#sB,#sBt", 4.38, .12);

// ================= SHOT C 4.5-6.83 : jus, written on porcelain =================
smokeIn("#c1", 4.9, .9, 20);
show("#nC", 5.5, .01);
smokeIn("#c2", 5.56, .55, 10); draw("#arC", 5.8, .55);
smokeIn("#c3", 6.2, .3, 10); draw("#rgC", 6.3, .35);
smokeOut("#c1", 6.45, .3); hide("#nC", 6.76, .06);

// ================= SHOT D 6.83-10.42 : salt =================
smokeIn("#d1", 7.58, .8, 20);
smokeIn("#d2", 8.18, .55); smokeIn("#d3", 8.58, .6); smokeIn("#d4", 9.5, .45);
smokeIn("#nD", 8.1, .6, 10); draw("#arD", 8.35, .6);
smokeOut("#d1,#d2,#d3,#d4,#nD", 10.18, .23);

// ================= HERO 10.42-15.07 : the pass printer prints the CTA; tear, spike, stamp =================
show("#sH", 10.42, .6);
show("#hrail,#spike", 10.45, .3);
tl.fromTo("#prn", { opacity: 0, y: -60 }, { opacity: 1, y: 0, duration: .35, ease: "power2.out", immediateRender: false }, 10.45);
tl.set("#tk2", { opacity: 1 }, 10.9);
""" + "\n".join(tk2_js) + """
smokeIn("#h1", 11.66, .7); smokeIn("#h2", 12.3, .6); smokeIn("#h3", 12.97, .6);
// torn off the printer...
tl.to("#tk2", { y: 16, rotation: 2.4, duration: .1, ease: "power4.out" }, 13.3);
// ...carried along the rail...
tl.to("#tk2", { x: -590, y: 2, rotation: -1.6, duration: .42, ease: "power3.inOut" }, 13.42);
// ...and spiked
tl.to("#tk2", { y: 20, rotation: -2.2, duration: .12, ease: "power2.in" }, 13.84);
tl.to("#tk2", { y: 17, duration: .12, ease: "sine.out" }, 13.96);
// 'done' rubber stamp slams down
tl.fromTo("#stamp", { opacity: 0, scale: 2.3, rotation: -4 }, { opacity: .92, scale: 1, rotation: -11, duration: .13, ease: "power4.in", immediateRender: false }, 14.05);
tl.to("#tk2", { y: 22, duration: .05, ease: "power2.out" }, 14.18);
tl.to("#tk2", { y: 17, duration: .18, ease: "sine.out" }, 14.23);

// ---- per-frame: gauge level + count, a gentle flicker on the fire word and the gauge ----
const _pp = window.onPlace;
window.onPlace = (t) => {
  _pp && _pp(t);
  const u = Math.max(0, Math.min(1, (t - 2.12) / (3.1 - 2.12))), w = 1 - Math.pow(1 - u, 3);
  document.getElementById("gN").firstChild.nodeValue = String(Math.round(260 * w));
  const lvl = 150 - 146 * w + 2.5 * Math.sin(t * 9.1) * w;
  document.getElementById("gLvl").setAttribute("y", lvl.toFixed(2));
  const fl = 1 + 0.018 * Math.sin(t * 13.7) + 0.012 * Math.sin(t * 7.3 + 1.1);
  document.getElementById("gF").style.transform = `scale(${fl.toFixed(4)},${(2 - fl).toFixed(4)})`;
  // ticket-rail time strip scrolls, the order timer runs
  document.getElementById("tsIn").style.transform = `translateX(${(-(t * 48)).toFixed(2)}px)`;
  // ember sparks rising behind the smoke words (pure function of t -> seek-safe)
  const R = (i, k) => { const v = Math.sin(i * 127.1 + k * 311.7) * 43758.5453; return v - Math.floor(v); };
  const ss = (a, b, x) => { const u = Math.max(0, Math.min(1, (x - a) / (b - a))); return u * u * (3 - 2 * u); };
  const inA = ss(0, .3, t) * (1 - ss(1.45, 1.75, t)), inH = ss(10.6, 11.2, t) * (1 - ss(14.85, 15.07, t));
  const reg = inA >= inH ? { e: inA, x0: 70, x1: 820, yb: 1070, h: 560 } : { e: inH, x0: 60, x1: 760, yb: 520, h: 420 };
  for (let i = 0; i < 46; i++) {
    const el = document.getElementById("sp" + i);
    if (reg.e <= 0.001) { el.style.opacity = 0; continue; }
    const L = .9 + .9 * R(i, 1), age = ((t / L) + R(i, 2)) % 1;
    const x = reg.x0 + (reg.x1 - reg.x0) * R(i, 3) + 34 * Math.sin(t * (1.3 + R(i, 4) * 2.2) + i) + age * 60 * (R(i, 5) - .3);
    const y = reg.yb - age * reg.h * (.55 + .45 * R(i, 6));
    const fl = .65 + .35 * Math.sin(t * (17 + 9 * R(i, 7)) + i * 3.1);
    const op = reg.e * Math.pow(Math.sin(Math.PI * age), .7) * (.45 + .55 * R(i, 8)) * fl;
    const sc = .6 + 1.1 * R(i, 9);
    el.style.opacity = op.toFixed(3);
    el.style.transform = `translate(${x.toFixed(1)}px,${y.toFixed(1)}px) rotate(${(12 * Math.sin(t * 2 + i)).toFixed(1)}deg) scale(${sc.toFixed(2)})`;
  }
  const a3 = document.getElementById("a3");
  a3.style.textShadow = `0 0 ${(34 + 10 * Math.sin(t * 11.3)).toFixed(1)}px rgba(255,90,10,.8),0 0 ${(80 + 20 * Math.sin(t * 6.1)).toFixed(1)}px rgba(255,70,0,.45),0 6px 30px rgba(0,0,0,.6)`;
};
"""

SPEC = {
    "theme": "he_bold",
    "palette": {"acc": "#ff8a3d", "ink": "#24130c", "lt": "#f6e9d2", "panel": "rgba(20,13,10,.8)", "sub": "#e9d6b8"},
    "music_vol": 0.5,
    "plate_vol": 0.45,
    "vo_name": "E10_chef_he_vo",
    "elements": [],
    "assets": assets,
    "css": CSS,
    "html_front": HTML,
    "js": LEVEL,
}
