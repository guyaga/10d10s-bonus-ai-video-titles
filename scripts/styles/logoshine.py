"""LOGO-SHINE-REVEAL: the premium logo sting. A geometric logomark draws itself on (stroke), then fills with a brushed-metal
gradient; the wordmark opens out of a horizontal light slit; a specular shine crosses the whole lockup in time with the
plate's light sweep and a star glint catches on the mark; a tagline settles underneath; a slow push-in to finish.
Works on any dark surface plate (brushed metal, stone, fabric). Wordmark is Latin; tagline Hebrew or English.

Spec keys. Required: clip, word.
  word       "NOVA"                 wordmark (Latin display, default Michroma)
  mark       "ring" (default) | "hex" | "none"    built-in SVG logomark;  svg: path to your own single-colour SVG (optional)
  tagline    "הטכנולוגיה שמרגישה אנושית"      sub  "NOVA LABS · 2026" (small mono line under the tagline, optional)
  t          start (default .5);  shine  time the shine crosses (default 3.2; sync to the plate's light sweep);  y  lockup centre y (default 470)
  language   "he" | "en" (tagline);  pair (Hebrew, default "secular"); Latin tagline Manrope 500
  colors     {"metal": ["#ffffff", "#aeb6c2", "#e9edf2", "#6d7582"], "accent": "#9fd3ff"}
  sfx (true), plate_vol, music, music_vol, name
"""
from styles.common import (audio_cues, cue, e, fonts, js, project_dir, res, tracks, type_pair)

MARKS = {
    "ring": ('<circle cx="60" cy="60" r="46" /><path d="M28 92 L92 28" />', 400),
    "hex": ('<path d="M60 10 L103 35 L103 85 L60 110 L17 85 L17 35 Z" /><path d="M60 38 L60 82 M41 49 L79 71" />', 460),
}


def build(spec, base, style="LOGO-SHINE-REVEAL"):
    tp = type_pair(spec, latin=("Manrope", 500, "Manrope", 500), default_pair="secular")
    wm_css, wm_files = fonts(spec.get("word_font", "Michroma"))
    rtl = tp["rtl"]
    col = {"metal": ["#ffffff", "#aeb6c2", "#e9edf2", "#6d7582"], "accent": "#9fd3ff", **spec.get("colors", {})}
    m0, m1, m2, m3 = col["metal"]
    t0, shine, y = spec.get("t", .5), spec.get("shine", 3.2), spec.get("y", 470)
    mark = spec.get("mark", "ring")
    paths_svg, plen = MARKS.get(mark, ("", 0))
    metal = f"linear-gradient(100deg,{m3} 0%,{m1} 18%,{m0} 34%,{m2} 50%,{m1} 66%,{m0} 80%,{m3} 100%)"
    css = tp["css"] + wm_css + f"""
#vig{{position:absolute;inset:0;background:radial-gradient(ellipse 60% 55% at 50% {round(y / 10.8)}%,rgba(0,0,0,.0),rgba(0,0,0,.45) 100%)}}
#lock{{position:absolute;left:0;right:0;top:{y}px;transform:translateY(-50%);display:flex;flex-direction:column;align-items:center}}
#row{{display:flex;align-items:center;gap:44px}}
#mk{{width:150px;height:150px;overflow:visible}}
#mk svg{{width:150px;height:150px;overflow:visible}}
#mk .st{{fill:none;stroke:{m0};stroke-width:5;stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 0 6px rgba(255,255,255,.35))}}
#mk .fl{{fill:none;stroke:url(#mg);stroke-width:13;stroke-linecap:round;stroke-linejoin:round;opacity:0}}
#wm{{position:relative;font-family:"{spec.get('word_font', 'Michroma')}",sans-serif;font-size:140px;line-height:1;letter-spacing:.14em;padding-left:.14em;
  background:{metal};background-size:220% 100%;background-position:0% 50%;-webkit-background-clip:text;background-clip:text;color:transparent;
  filter:drop-shadow(0 8px 30px rgba(0,0,0,.55))}}
#wmw{{position:relative}}
#shw{{position:absolute;left:0;top:0;font-family:"{spec.get('word_font', 'Michroma')}",sans-serif;font-size:140px;line-height:1;letter-spacing:.14em;padding-left:.14em;
  background:linear-gradient(100deg,transparent 40%,rgba(255,255,255,1) 50%,transparent 60%);background-size:260% 100%;background-position:140% 50%;
  -webkit-background-clip:text;background-clip:text;color:transparent;pointer-events:none}}
#star{{position:absolute;width:90px;height:90px;left:0;top:0;opacity:0;background:
  radial-gradient(circle,rgba(255,255,255,1) 0 6%,rgba(255,255,255,.0) 22%),
  linear-gradient(90deg,transparent 48%,rgba(255,255,255,.95) 50%,transparent 52%),linear-gradient(0deg,transparent 48%,rgba(255,255,255,.95) 50%,transparent 52%)}}
#tag{{margin-top:46px;font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};font-size:46px;color:#eef3f8;direction:{tp['dir']};
  text-shadow:0 2px 10px rgba(0,0,0,.85),0 0 30px rgba(0,0,0,.6);letter-spacing:{'0' if rtl else '.02em'}}}
#sub{{margin-top:18px;padding:8px 10px 8px 20px;border-radius:24px;background:rgba(6,9,14,.55);font-family:"JetBrains Mono",monospace;font-size:24px;letter-spacing:.34em;color:#e8f3ff;opacity:.95;direction:ltr;text-shadow:0 1px 8px rgba(0,0,0,.95),0 0 22px rgba(0,0,0,.7)}}
"""
    mono_css, mono_files = fonts("JetBrains Mono") if spec.get("sub") else ("", {})
    css += mono_css
    svg = ""
    if paths_svg:
        svg = (f'<svg viewBox="0 0 120 120"><defs><linearGradient id="mg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{m3}"/>'
               f'<stop offset=".35" stop-color="{m0}"/><stop offset=".6" stop-color="{m1}"/><stop offset="1" stop-color="{m0}"/></linearGradient></defs>'
               f'<g class="fl">{paths_svg}</g><g class="st">{paths_svg}</g></svg>')
    hud = ('<div id="vig"></div><div id="lock"><div id="row">' + (f'<div id="mk">{svg}</div>' if svg else "")
           + f'<div id="wmw"><div id="wm">{e(spec["word"])}</div><div id="shw">{e(spec["word"])}</div></div></div>'
           + (f'<div id="tag">{e(spec["tagline"])}</div>' if spec.get("tagline") else "")
           + (f'<div id="sub">{e(spec["sub"])}</div>' if spec.get("sub") else "") + '</div><div id="star"></div>')
    J = {"t0": t0, "shine": shine, "plen": plen, "mark": bool(svg), "tag": bool(spec.get("tagline")), "sub": bool(spec.get("sub"))}
    j = [f"const L = {js(J)};", r"""
if (L.mark) {
  const st = document.querySelectorAll("#mk .st *");
  st.forEach((p) => { const n = p.getTotalLength ? p.getTotalLength() : 400; p.style.strokeDasharray = n; p.style.strokeDashoffset = n; });
  tl.to("#mk .st *", {strokeDashoffset: 0, duration: 1.1, ease: "power2.inOut", stagger: .18}, L.t0);
  tl.fromTo("#mk .fl", {opacity: 0}, {opacity: 1, duration: .7, ease: "power2.out"}, L.t0 + 1.0);
  tl.to("#mk .st", {opacity: .0, duration: .6}, L.t0 + 1.3);
  tl.fromTo("#mk", {rotation: -90, scale: .8}, {rotation: 0, scale: 1, duration: 1.4, ease: "expo.out"}, L.t0);
}
// wordmark opens from a horizontal light slit, the metal gradient keeps drifting (brushed-metal life)
tl.fromTo("#wmw", {clipPath: "inset(48% 0 48% 0)", opacity: 0}, {clipPath: "inset(0% 0 0% 0)", opacity: 1, duration: .9, ease: "expo.inOut"}, L.t0 + .8);
tl.fromTo("#wmw", {scaleX: 1.12}, {scaleX: 1, duration: 1.4, ease: "expo.out"}, L.t0 + .8);
tl.fromTo("#wm", {backgroundPosition: "0% 50%"}, {backgroundPosition: "100% 50%", duration: DUR - L.t0, ease: "none"}, L.t0);
// the specular shine crosses in sync with the plate's light sweep, a star glint catches on the mark
tl.set("#shw", {visibility: "hidden"}, 0);
tl.set("#shw", {visibility: "visible"}, L.shine - .02);
tl.set("#shw", {visibility: "hidden"}, L.shine + 1.25);
tl.fromTo("#shw", {backgroundPosition: "140% 50%"}, {backgroundPosition: "-40% 50%", duration: 1.2, ease: "power2.inOut"}, L.shine);
if (L.mark) {
  const r = document.getElementById("mk").getBoundingClientRect(), cx = r.left + r.width / 2, cy = r.top + r.height / 2;  // centre ignores the entrance rotate/scale
  tl.set("#star", {x: cx + 150 * .28 - 45, y: cy - 150 * .3 - 45}, 0);
  tl.fromTo("#star", {opacity: 0, scale: .2, rotation: -30}, {opacity: 1, scale: 1, rotation: 15, duration: .35, ease: "power2.out"}, L.shine - .15);
  tl.to("#star", {opacity: 0, scale: .4, rotation: 45, duration: .6, ease: "power2.in"}, L.shine + .2);
}
if (L.tag) tl.fromTo("#tag", {opacity: 0, y: 18, filter: "blur(8px)"}, {opacity: 1, y: 0, filter: "blur(0px)", duration: .9, ease: "power3.out"}, L.shine + .6);
if (L.sub) tl.fromTo("#sub", {opacity: 0}, {opacity: .9, duration: .8}, L.shine + 1.1);
tl.fromTo("#lock", {scale: 1}, {scale: 1.035, duration: DUR - L.t0, ease: "sine.inOut"}, L.t0);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ar_whoosh", t0, .3), cue("logo_hit", t0 + .8, .55), cue("glass_ting", shine, .3)]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .5), extra={**tp["files"], **wm_files, **mono_files})
