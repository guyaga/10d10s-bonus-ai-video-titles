"""CHAPTER-MARKERS: documentary / YouTube chapter card. A big chapter numeral draws as an outline and then fills, a hairline
rule draws in, the chapter title rises out of a mask, a subtitle fades up, then the card folds into a persistent chapter
chip while a segmented chapter bar (the YouTube scrub-bar idiom) fills along the bottom. Hebrew (RTL: rules and wipes
run right-to-left) or English.

Spec keys. Required: clip, chapter.
  chapter    {"num": "01", "kicker": "פרק", "title": "העיר שמעל הים", "sub": "נמל עתיק · 3,000 שנות היסטוריה",
              "t": 0.6, "until": 6.6}
  bar        {"labels": ["העיר שמעל הים", "הנמל", "הכנסייה", "השוק", "הלילה"], "current": 0, "t": 0.3}   optional
  chip       true (default): after "until" the card collapses into a small chip "01 · title" in the top corner
  side       "left" (default) | "right": which half of the frame holds the card (keep it off the subject)
  language   "he" | "en";  pair (Hebrew, default "suez"); Latin: DM Serif Display + Manrope
  colors     {"text": "#ffffff", "accent": "#e8c27a", "scrim": .5}
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="CHAPTER-MARKERS"):
    tp = type_pair(spec, latin=("DM Serif Display", 400, "Manrope", 500), default_pair="suez")
    rtl = tp["rtl"]
    col = {"text": "#ffffff", "accent": "#e8c27a", "scrim": .5, **spec.get("colors", {})}
    ch = spec["chapter"]
    t0, t1 = ch.get("t", .6), ch.get("until", 6.6)
    side = spec.get("side", "left")
    bar = spec.get("bar")
    chip = spec.get("chip", True)
    # the card column: anchored to the outer edge of its half, text aligned to the reading start
    x = 110 if side == "left" else 1920 - 110 - 760
    align = "right" if rtl else "left"
    grad_dir = "to right" if side == "left" else "to left"

    css = tp["css"] + f"""
#scrim{{position:absolute;inset:0;background:linear-gradient({grad_dir},rgba(4,8,14,{col['scrim']}) 0%,rgba(4,8,14,{col['scrim'] * .8}) 38%,rgba(4,8,14,{col['scrim'] * .35}) 56%,transparent 72%);opacity:0}}
#card{{position:absolute;left:{x}px;top:250px;width:760px;direction:{tp['dir']};text-align:{align}}}
#head{{display:flex;align-items:flex-end;gap:34px;justify-content:flex-start}}
#kick{{display:flex;flex-direction:column;align-items:flex-start;gap:16px;margin-bottom:46px;font-family:"{tp['body']}",sans-serif;
  font-weight:{tp['bw']};font-size:34px;letter-spacing:{'.02em' if rtl else '.32em'};color:#fff;text-shadow:0 2px 14px rgba(0,0,0,.7);text-transform:uppercase}}
#kick i{{display:block;height:2px;width:260px;background:{col['accent']};transform-origin:{'100%' if rtl else '0%'} 50%}}
#num{{position:relative;line-height:0}}
#num span{{display:inline-block;font-family:"{tp['display']}",serif;font-weight:{tp['dw']};font-size:300px;line-height:.86;
  letter-spacing:-.02em;font-variant-numeric:lining-nums}}
#num .o{{position:absolute;{'right' if rtl else 'left'}:0;top:0;color:rgba(10,14,20,.18);-webkit-text-stroke:2.5px rgba(255,255,255,.95)}}
#num .f{{color:{col['text']};text-shadow:0 10px 60px rgba(0,0,0,.35)}}
#ttl{{overflow:hidden;padding-bottom:.08em;margin-top:34px}}
#ttl span{{display:block;font-family:"{tp['display']}",serif;font-weight:{tp['dw']};font-size:104px;line-height:1.05;color:{col['text']};
  text-shadow:0 6px 40px rgba(0,0,0,.45)}}
#sub{{margin-top:22px;font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:38px;color:rgba(255,255,255,.88);
  text-shadow:0 2px 18px rgba(0,0,0,.55)}}
#chip{{position:absolute;top:70px;{'right' if rtl else 'left'}:80px;display:flex;align-items:center;gap:16px;direction:{tp['dir']};
  padding:14px 26px 14px 22px;background:rgba(8,12,18,.55);border:1px solid rgba(255,255,255,.18);border-radius:40px;backdrop-filter:blur(10px);opacity:0}}
#chip b{{font-family:"{tp['display']}",serif;font-weight:{tp['dw']};font-size:40px;color:{col['accent']};line-height:1}}
#chip span{{font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:30px;color:#fff;line-height:1}}
#chip i{{width:1px;height:30px;background:rgba(255,255,255,.35)}}
#bar{{position:absolute;left:120px;right:120px;bottom:70px;display:flex;gap:10px;direction:{tp['dir']};opacity:0}}
.seg{{flex:1;position:relative}}
.seg .tr{{height:6px;border-radius:3px;background:rgba(255,255,255,.28);overflow:hidden}}
.seg .fl{{height:100%;width:100%;background:#fff;transform:scaleX(0);transform-origin:{'100%' if rtl else '0%'} 50%}}
.seg.cur .fl{{background:{col['accent']}}}
.seg .lb{{margin-top:14px;font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:24px;color:rgba(255,255,255,.62);white-space:nowrap;
  text-shadow:0 2px 10px rgba(0,0,0,.6)}}
.seg.cur .lb{{color:#fff}}
"""
    segs = ""
    if bar:
        for i, lb in enumerate(bar["labels"]):
            segs += f'<div class="seg{" cur" if i == bar.get("current", 0) else ""}" id="s{i}"><div class="tr"><div class="fl"></div></div><div class="lb">{e(lb)}</div></div>'
    hud = ('<div id="scrim"></div>'
           f'<div id="card"><div id="head"><div id="num"><span class="f">{e(ch["num"])}</span><span class="o">{e(ch["num"])}</span></div>'
           f'<div id="kick"><span>{e(ch.get("kicker", ""))}</span><i></i></div></div>'
           f'<div id="ttl"><span>{e(ch["title"])}</span></div><div id="sub">{e(ch.get("sub", ""))}</div></div>'
           + (f'<div id="chip"><b>{e(ch["num"])}</b><i></i><span>{e(ch["title"])}</span></div>' if chip else "")
           + (f'<div id="bar">{segs}</div>' if bar else ""))
    cur = bar.get("current", 0) if bar else 0
    J = {"t0": t0, "t1": t1, "rtl": rtl, "cur": cur, "bt": bar.get("t", .3) if bar else 0, "chip": chip, "nseg": len(bar["labels"]) if bar else 0}
    j = [f"const C = {js(J)};", r"""
const FILL_FROM = C.rtl ? "inset(0 0 0 100%)" : "inset(0 100% 0 0)";
tl.fromTo("#scrim", {opacity: 0}, {opacity: 1, duration: 1.1, ease: "power2.out"}, Math.max(0, C.t0 - .4));
// kicker: the rule draws from the reading start, the word slides in beside it
tl.fromTo("#kick i", {scaleX: 0}, {scaleX: 1, duration: .9, ease: "expo.out"}, C.t0);
tl.fromTo("#kick span", {opacity: 0, x: C.rtl ? 30 : -30}, {opacity: 1, x: 0, duration: .7, ease: "power3.out"}, C.t0 + .15);
// numeral: outline first, then the solid fill wipes across it; a slow parallax drift keeps it alive
tl.fromTo("#num .o", {opacity: 0, scale: 1.08}, {opacity: 1, scale: 1, duration: .9, ease: "power3.out"}, C.t0 + .1);
tl.fromTo("#num .f", {clipPath: FILL_FROM}, {clipPath: "inset(0 0% 0 0%)", duration: 1.1, ease: "power2.inOut"}, C.t0 + .75);
tl.fromTo("#num", {x: 0}, {x: C.rtl ? 18 : -18, duration: C.t1 - C.t0, ease: "none"}, C.t0);
// title rises out of its mask, subtitle follows
tl.fromTo("#ttl span", {yPercent: 105}, {yPercent: 0, duration: 1.0, ease: "expo.out"}, C.t0 + 1.05);
tl.fromTo("#sub", {opacity: 0, y: 22, filter: "blur(6px)"}, {opacity: 1, y: 0, filter: "blur(0px)", duration: .8, ease: "power3.out"}, C.t0 + 1.5);
// chapter bar: segments before the current one are full, the current one fills over the shot
if (C.nseg) {
  tl.fromTo("#bar", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .7, ease: "power3.out"}, C.bt);
  for (let i = 0; i < C.nseg; i++) {
    if (i < C.cur) tl.set(`#s${i} .fl`, {scaleX: 1}, 0);
    if (i === C.cur) tl.fromTo(`#s${i} .fl`, {scaleX: 0}, {scaleX: 1, duration: DUR - C.bt - .3, ease: "none"}, C.bt + .2);
  }
}
// exit: the card folds away (title back into its mask, numeral fades), the chip takes over in the corner
tl.to("#ttl span", {yPercent: -105, duration: .6, ease: "power3.in"}, C.t1 - .6);
tl.to("#sub", {opacity: 0, y: -12, duration: .45, ease: "power2.in"}, C.t1 - .65);
tl.to("#num", {opacity: 0, scale: .96, filter: "blur(8px)", duration: .6, ease: "power2.in"}, C.t1 - .55);
tl.to("#kick", {opacity: 0, duration: .4}, C.t1 - .45);
tl.to("#scrim", {opacity: .35, duration: .8}, C.t1 - .4);
if (C.chip) tl.fromTo("#chip", {opacity: 0, y: -16, scale: .96}, {opacity: 1, y: 0, scale: 1, duration: .6, ease: "back.out(1.6)"}, C.t1 - .1);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ar_whoosh", t0, .35), cue("soft_thump", t0 + .75, .5), cue("ui_whoosh", t0 + 1.05, .25), cue("soft_click", t1 - .05, .35)]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .7), extra=tp["files"])
