"""FILM-TITLE-CARD: cinema title design. Two card modes plus a credits roll.
  anderson  centred and symmetric: small letter-spaced kicker, the title, a sub line, a thin frame with corner ornaments,
            gentle fades, no movement (Wes Anderson). Optional flat colour card (bg) instead of over-picture.
  bass      cut-paper graphics: flat colour bars and blocks slam in on diagonals, the title set on them, a little
            rotation, hard cuts (Saul Bass).
  credits   a classic two-column roll (role | name), linear crawl, optional scrim; columns mirror for Hebrew.

Spec keys. Required: clip, cards and/or credits.
  cards      [{"mode": "anderson|bass", "t": 3.3, "until": 7.6, "kicker": "CHAPTER ONE", "title": "THE MACHINE", "sub": "...",
               "y": 860, "bg": null, "palette": ["#d7261e", "#111111", "#f3e6cf"]}]
  credits    {"t": 19.6, "until": 24, "x": 480, "lines": [["DIRECTED BY", "GUY AGA"], ["", ""], ...], "scrim": .6, "size": 40}
  language   "he" | "en";  pair (Hebrew, default "suez"; see common.HE_PAIRS); Latin: Jost 500 (anderson) / Oswald 700 (bass) + Jost 300
  colors     {"ink": "#f6e7c8", "frame": "#f6e7c8"}
  sfx (true), music, music_vol, plate_vol, name, track (optional)
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, fonts, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="FILM-TITLE-CARD"):
    tp = type_pair(spec, latin=("Jost", 500, "Jost", 300), default_pair="suez")
    rtl = tp["rtl"]
    bass_font = ("Oswald", 700) if not rtl else (tp["display"], tp["dw"])
    fc, ff = fonts("Oswald") if not rtl else ("", {})
    col = {"ink": "#f6e7c8", "frame": "#f6e7c8", **spec.get("colors", {})}
    h, C = [], []
    for i, c in enumerate(spec.get("cards", [])):
        mode = c.get("mode", "anderson")
        C.append({"i": i, "mode": mode, "t": c["t"], "until": c.get("until")})
        if mode == "anderson":
            bg = f"background:{c['bg']};" if c.get("bg") else ""
            h.append(f'<div class="card an" id="c{i}" style="{bg}"><div class="an-in" style="top:{c.get("y", 540)}px">'
                     f'<i class="cn tl"></i><i class="cn tr"></i><i class="cn bl"></i><i class="cn br"></i>'
                     + (f'<div class="k">{e(c["kicker"])}</div>' if c.get("kicker") else "")
                     + f'<div class="tt">{e(c["title"])}</div>' + (f'<div class="sb">{e(c["sub"])}</div>' if c.get("sub") else "") + "</div></div>")
        else:
            p = c.get("palette", ["#d7261e", "#111111", "#f3e6cf"])
            h.append(f'<div class="card bs" id="c{i}">'
                     # GSAP only moves the .mv wrappers; the rotation lives on the inner shapes (no transform fights)
                     f'<div class="mv m1"><div class="sh s1" style="background:{p[0]}"></div></div><div class="mv m2"><div class="sh s2" style="background:{p[1]}"></div></div>'
                     f'<div class="mv m3"><div class="sh s3" style="background:{p[2]}"></div></div>'
                     f'<div class="mv m4"><div class="bt" style="top:{c.get("y", 520)}px"><div class="tt" data-layout-allow-overlap>{e(c["title"])}</div>'   # rotated: AABBs always intersect
                     + (f'<div class="sb" data-layout-allow-overlap style="background:{p[0]}">{e(c["sub"])}</div>' if c.get("sub") else "") + "</div></div></div>")
    cr = spec.get("credits")
    if cr:
        rows = "".join(f'<div class="cr-row"><span class="rl">{e(a)}</span><span class="nm">{e(b)}</span></div>' if (a or b) else '<div class="cr-gap"></div>'
                       for a, b in cr["lines"])
        h.append(f'<div id="crs"><div id="crsc" style="background:linear-gradient({"270deg" if rtl else "90deg"},rgba(0,0,0,{cr.get("scrim", .6)}),rgba(0,0,0,{cr.get("scrim", .6) * .6}) 70%,transparent)"></div>'
                 f'<div id="crm" style="left:{cr.get("x", 480)}px;font-size:{cr.get("size", 40)}px">{rows}</div></div>')
    D, Bf = tp["display"], tp["body"]
    css = tp["css"] + fc + f"""
.card{{position:absolute;inset:0;opacity:0}}
.an-in{{position:absolute;left:50%;transform:translate(-50%,-50%);padding:34px 80px 38px;text-align:center;direction:{tp['dir']};border:2px solid {col['frame']};
  background:rgba(20,14,8,.28);box-shadow:0 0 0 8px rgba(20,14,8,.12)}}
.an .cn{{position:absolute;width:14px;height:14px;border:2px solid {col['frame']};background:rgba(20,14,8,.3)}}
.an .cn.tl{{left:-9px;top:-9px}}.an .cn.tr{{right:-9px;top:-9px}}.an .cn.bl{{left:-9px;bottom:-9px}}.an .cn.br{{right:-9px;bottom:-9px}}
.an .k{{font-family:"{Bf}",sans-serif;font-weight:{max(400, tp['bw'])};font-size:30px;letter-spacing:{'.05em' if rtl else '.5em'};color:{col['ink']};margin-bottom:26px;line-height:1.2}}
.an .tt{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:120px;line-height:1;letter-spacing:{'0' if rtl else '.14em'};color:{col['ink']};text-transform:uppercase;
  text-shadow:0 3px 20px rgba(0,0,0,.45);white-space:nowrap}}
.an .sb{{font-family:"{Bf}",sans-serif;font-weight:{tp['bw']};font-size:32px;letter-spacing:{'0' if rtl else '.3em'};color:{col['ink']};margin-top:18px;text-transform:uppercase}}
.bs .mv{{position:absolute;inset:0}}
.bs .sh{{position:absolute}}
.bs .s1{{left:-10%;top:50%;width:66%;height:400px;transform:translateY(-50%) rotate(-8deg)}}
.bs .s2{{left:-5%;top:50%;width:52%;height:230px;transform:translateY(-50%) rotate(-8deg)}}
.bs .s3{{left:8%;top:22%;width:14px;height:60%;transform:rotate(-8deg)}}
.bs .bt{{position:absolute;left:{'auto' if rtl else '6%'};right:{'6%' if rtl else 'auto'};transform:translateY(-50%) rotate(-8deg);direction:{tp['dir']}}}
.bs .tt{{font-family:"{bass_font[0]}",sans-serif;font-weight:{bass_font[1]};font-size:190px;line-height:1.05;color:#fff;letter-spacing:.02em;white-space:nowrap}}
.bs .sb{{display:inline-block;font-family:"{Bf}",sans-serif;font-weight:{max(400, tp['bw'])};font-size:34px;color:#111;padding:6px 16px;margin-top:34px;letter-spacing:{'0' if rtl else '.2em'};text-transform:uppercase}}
#crs{{position:absolute;inset:0;opacity:0}}
#crsc{{position:absolute;inset:0}}
#crm{{position:absolute;top:0;transform:translateX(-50%);direction:{tp['dir']}}}
.cr-row{{display:grid;grid-template-columns:1fr 1.5fr;column-gap:.8em;min-width:1000px;margin-bottom:.35em}}
.cr-row .nm{{white-space:nowrap}}
.cr-row .rl{{text-align:end;font-family:"{Bf}",sans-serif;font-weight:{tp['bw']};font-size:.62em;letter-spacing:{'0' if rtl else '.18em'};color:#d9cfbd;padding-top:.3em}}
.cr-row .nm{{text-align:start;font-family:"{D}",sans-serif;font-weight:{tp['dw']};color:#fff;letter-spacing:{'0' if rtl else '.06em'}}}
.cr-gap{{height:1.1em}}
"""
    j = [JS_UTIL, f"const C = {js(C)}, CR = {js(cr)};", r"""
for (const c of C) {
  const id = "#c" + c.i;
  if (c.mode === "anderson") {
    tl.fromTo(id, {opacity: 0}, {opacity: 1, duration: .5, ease: "sine.inOut"}, c.t);
    if (c.until != null) tl.to(id, {opacity: 0, duration: .45, ease: "sine.inOut"}, c.until - .45);
  } else {
    tl.set(id, {opacity: 1}, c.t);
    tl.fromTo(id + " .m1", {x: -1500}, {x: 0, duration: .32, ease: "expo.out"}, c.t);
    tl.fromTo(id + " .m2", {x: -1500}, {x: 0, duration: .32, ease: "expo.out"}, c.t + .1);
    tl.fromTo(id + " .m3", {opacity: 0, y: -300}, {opacity: 1, y: 0, duration: .25, ease: "expo.out"}, c.t + .22);
    tl.fromTo(id + " .tt", {opacity: 0}, {opacity: 1, duration: .12}, c.t + .26);
    tl.fromTo(id + " .m4", {x: -120}, {x: 0, duration: .3, ease: "expo.out"}, c.t + .26);
    if (document.querySelector(id + " .sb")) tl.fromTo(id + " .sb", {opacity: 0}, {opacity: 1, duration: .2}, c.t + .45);
    if (c.until != null) { tl.to([id + " .m1", id + " .m2", id + " .m3", id + " .m4"], {x: 2400, duration: .28, ease: "expo.in", stagger: .04}, c.until - .36); tl.set(id, {opacity: 0}, c.until); }
  }
}
if (CR) {
  tl.fromTo("#crs", {opacity: 0}, {opacity: 1, duration: .6}, CR.t);
  window.onPlace = (t) => {
    const el = document.getElementById("crm"), H = el.offsetHeight, D = (CR.until ?? CR.t + 8) - CR.t;
    const u = clamp01((t - CR.t) / D);
    el.style.top = (1080 - (1080 + H) * u) + "px";
  };
}
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("logo_hit" if c.get("mode", "anderson") == "anderson" else "stinger", c["t"], .55) for c in spec.get("cards", [])]
    sfx += audio_cues(spec, base, .6)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .45), extra={**tp["files"], **ff})
