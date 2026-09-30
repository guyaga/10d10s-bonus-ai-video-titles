"""LOWER-THIRD-CORP: the corporate / interview name super. An accent bar grows from the edge, the name rises out of a mask
line, the title slides in a beat later, a thin rule draws under it and a glint sweeps once across the plate. Clean
masked exit. Any number of entries; each can sit at a fixed side or ride a tracked person (follow).
Hebrew mirrors everything (bar grows from the right, text right-aligned, wipes run right-to-left).

Spec keys. Required: clip, supers.
  supers     [{"name": "דנה לוי", "title": "מנכ״לית, NORTH LABS", "t": .6, "until": 5.2,
               "side": "L|R" (default L; RTL default R), "follow": "host", "anchor": "b", "dx": 0, "dy": 40,
               "tag": "LIVE" (optional small chip above the name)}]
  language   "he" | "en";  pair (Hebrew, default "suez": Suez One name + Secular One title);
             Latin default Manrope 700 + Manrope 500 (override with fonts {display, dw, body, bw})
  y          baseline of fixed supers as a fraction of frame height (default .8)
  colors     {"bar": "#cc2419", "panel": "rgba(10,12,16,.82)", "text": "#ffffff", "sub": "#c9d2de", "rule": "#ffffff"}
  logo       optional small square mark text (e.g. "N") on the bar
  sfx (true), music, music_vol, vo, plate_vol, name, track (needed only for follow)
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="LOWER-THIRD-CORP"):
    tp = type_pair(spec, latin=("Manrope", 700, "Manrope", 500), default_pair="suez")
    rtl = tp["rtl"]
    col = {"bar": "#cc2419", "panel": "rgba(10,12,16,.82)", "text": "#ffffff", "sub": "#c9d2de", "rule": "#ffffff", **spec.get("colors", {})}
    D, B = tp["display"], tp["body"]
    y = spec.get("y", .8)
    logo = spec.get("logo")
    h = ['<div id="glint"></div>']
    for i, s in enumerate(spec["supers"]):
        side = s.get("side", "R" if rtl else "L")
        pos = (f'data-follow="{e(s["follow"])}" data-anchor="{s.get("anchor", "b")}" data-dx="{s.get("dx", 0)}" data-dy="{s.get("dy", 40)}"'
               if s.get("follow") else f'style="{"right" if side == "R" else "left"}:96px;top:{int(1080 * y)}px"')
        tag = f'<div class="tg">{e(s["tag"])}</div>' if s.get("tag") else ""
        mark = f'<div class="mk">{e(logo)}</div>' if logo else ""
        rev = (side == "R") != rtl   # the accent bar always sits on the block's outer edge
        h.append(f'<div class="lt {side}{" fol" if s.get("follow") else ""}{" rev" if rev else ""}" id="lt{i}" {pos}><div class="in">'
                 f'<div class="bar">{mark}</div><div class="tx">{tag}<div class="nmw"><div class="nm">{e(s["name"])}</div></div>'
                 f'<div class="rl"></div><div class="ttw"><div class="tt">{e(s.get("title", ""))}</div></div></div></div></div>')
    css = tp["css"] + f"""
#glint{{position:absolute;top:0;bottom:0;width:260px;left:0;background:linear-gradient(100deg,transparent,rgba(255,255,255,.10),transparent);opacity:0;pointer-events:none}}
.lt{{position:absolute;direction:{tp['dir']}}}
.lt.fol{{width:0;height:0}}
.lt .in{{position:absolute;bottom:0;display:flex;align-items:stretch;gap:0}}
.lt.L .in{{left:0}} .lt.R .in{{right:0}} .lt.rev .in{{flex-direction:row-reverse}}
.lt.fol .in{{bottom:auto;top:0;transform:translateX(-50%)}}
.bar{{width:14px;background:{col['bar']};transform-origin:50% 100%;position:relative;flex:none}}
.mk{{position:absolute;top:0;{'right' if rtl else 'left'}:0;width:58px;height:58px;background:{col['bar']};color:#fff;display:grid;place-items:center;
  font-family:"{D}",sans-serif;font-size:34px}}
.tx{{background:{col['panel']};padding:20px 36px 22px;backdrop-filter:blur(6px);clip-path:inset(0 0 0 0);min-width:360px}}
.tg{{display:inline-block;background:{col['bar']};color:#fff;font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:18px;letter-spacing:{'0' if rtl else '.18em'};
  padding:3px 10px;margin-bottom:10px}}
.nmw,.ttw{{overflow:hidden;padding-bottom:4px}}
.nm{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:60px;line-height:1.12;color:{col['text']};white-space:nowrap;letter-spacing:{'0' if rtl else '-.01em'}}}
.rl{{height:2px;background:{col['rule']};opacity:.55;margin:8px 0 10px;transform-origin:{'100%' if rtl else '0'} 50%}}
.tt{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:30px;line-height:1.25;color:{col['sub']};white-space:nowrap;letter-spacing:{'0' if rtl else '.02em'}}}
"""
    J = [{"t": s["t"], "until": s.get("until"), "side": s.get("side", "R" if rtl else "L")} for s in spec["supers"]]
    j = [JS_UTIL, f"const J = {js(J)}, RTL = {js(rtl)};", r"""
J.forEach((s, i) => {
  const g = `#lt${i}`, from = (s.side === "R") ? 1 : -1;
  tl.set(`${g} .in`, {opacity: 1}, 0);
  tl.fromTo(`${g} .bar`, {scaleY: 0}, {scaleY: 1, duration: .32, ease: "expo.out"}, s.t);
  tl.fromTo(`${g} .tx`, {clipPath: from < 0 ? "inset(0 100% 0 0)" : "inset(0 0 0 100%)"}, {clipPath: "inset(0 0% 0 0%)", duration: .55, ease: "expo.out"}, s.t + .12);
  tl.fromTo(`${g} .tg`, {opacity: 0, y: 10}, {opacity: 1, y: 0, duration: .3, ease: "power3.out"}, s.t + .3);
  tl.fromTo(`${g} .nm`, {yPercent: 110}, {yPercent: 0, duration: .6, ease: "expo.out"}, s.t + .28);
  tl.fromTo(`${g} .rl`, {scaleX: 0}, {scaleX: 1, duration: .6, ease: "power3.inOut"}, s.t + .42);
  tl.fromTo(`${g} .tt`, {yPercent: 110, opacity: 0}, {yPercent: 0, opacity: 1, duration: .55, ease: "expo.out"}, s.t + .5);
  if (i === 0) tl.fromTo("#glint", {x: RTL ? 1980 : -300, opacity: 1}, {x: RTL ? -300 : 1980, opacity: 1, duration: 1.3, ease: "power2.inOut"}, s.t + .35);
  if (s.until != null) {
    tl.to(`${g} .nm, ${g} .tt`, {yPercent: -110, duration: .35, ease: "power3.in", stagger: .05}, s.until - .5);
    tl.to(`${g} .tx`, {clipPath: from < 0 ? "inset(0 100% 0 0)" : "inset(0 0 0 100%)", duration: .4, ease: "expo.in"}, s.until - .35);
    tl.to(`${g} .bar`, {scaleY: 0, duration: .25, ease: "power2.in"}, s.until - .1);
  }
});
tl.set(J.map((_, i) => `#lt${i} .bar`).join(","), {scaleY: 0}, 0);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ar_whoosh", s["t"], .5) for s in spec["supers"]] + [cue("soft_click", s["t"] + .3, .35) for s in spec["supers"]]
    sfx += audio_cues(spec, base, .5)
    need_track = any(s.get("follow") for s in spec["supers"])
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec if need_track or spec.get("track") else {**spec, "track": None}, base),
                css=css, hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .7), extra=tp["files"])
