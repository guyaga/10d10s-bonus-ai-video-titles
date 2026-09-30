"""LEADER-CALLOUTS: the premium tech product callout. A dot lands on a tracked part (with a ring pulse), a thin leader
line draws out in two segments (angle, then horizontal), and a label unmasks at the end of the line: a small spaced
caption over a big spec value that counts up, with its unit. Everything rides the tracked part. Clean retract on exit.

Spec keys. Required: clip, track, callouts.
  callouts   [{"follow": "lid", "anchor": "t|c|b|l|r|tl|tr|bl|br", "dx": 0, "dy": 0,
               "side": "L|R", "rise": -140 (px up; +down), "run": 260 (horizontal px),
               "label": "ACTIVE NOISE CANCELLING", "value": 42, "prefix": "-", "unit": "dB", "decimals": 0,
               "t": 1.0, "until": 9.5}]
  language   "he" | "en";  pair (Hebrew default "secular"); Latin default Space Grotesk 700 + Space Grotesk 500
  colors     {"line": "#ffffff", "dot": "#ffffff", "accent": "#7cf0ff", "label": "#b8c2cc", "value": "#ffffff"}
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="LEADER-CALLOUTS"):
    tp = type_pair(spec, latin=("Space Grotesk", 700, "Space Grotesk", 500), default_pair="secular")
    rtl = tp["rtl"]
    col = {"line": "#ffffff", "dot": "#ffffff", "accent": "#7cf0ff", "label": "#b8c2cc", "value": "#ffffff", **spec.get("colors", {})}
    D, B = tp["display"], tp["body"]
    h = []
    for i, c in enumerate(spec["callouts"]):
        side = c.get("side", "L")
        sg = -1 if side == "L" else 1
        rise, run = c.get("rise", -140), c.get("run", 260)
        dx1 = sg * abs(rise) * .6
        x2, y2 = dx1 + sg * run, rise
        W, H = 1400, 900
        ox, oy = W / 2, H / 2
        path = f"M{ox} {oy} L{ox + dx1} {oy + rise} L{ox + x2} {oy + y2}"
        lab_pos = (f"left:{ox + x2 + 18}px" if sg > 0 else f"right:{W - (ox + x2) + 18}px") + f";top:{oy + y2}px"
        h.append(f'<div class="co" id="co{i}" data-follow="{e(c["follow"])}" data-anchor="{c.get("anchor", "c")}" data-dx="{c.get("dx", 0)}" data-dy="{c.get("dy", 0)}">'
                 f'<div class="cv" style="left:{-ox}px;top:{-oy}px;width:{W}px;height:{H}px">'
                 f'<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" overflow="visible">'
                 f'<path class="ln" d="{path}" fill="none" stroke="{col["line"]}" stroke-width="2" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
                 f'<circle class="rg" cx="{ox}" cy="{oy}" r="18" fill="none" stroke="{col["accent"]}" stroke-width="2"/>'
                 f'<circle class="dt" cx="{ox}" cy="{oy}" r="7" fill="{col["dot"]}"/>'
                 f'<circle class="end" cx="{ox + x2}" cy="{oy + y2}" r="4" fill="{col["accent"]}"/></svg>'
                 f'<div class="lb {"s" + side}" style="{lab_pos}"><div class="lkw"><div class="lk">{e(c.get("label", ""))}</div></div>'
                 f'<div class="lvw"><div class="lv"><span class="pf">{e(c.get("prefix", ""))}</span><span class="n" id="n{i}">0</span><span class="u">{e(c.get("unit", ""))}</span></div></div>'
                 f'</div></div></div>')
    css = tp["css"] + f"""
.co{{position:absolute;left:0;top:0;width:0;height:0}}
.cv{{position:absolute;pointer-events:none}}
.cv svg{{position:absolute;left:0;top:0;filter:drop-shadow(0 0 6px rgba(0,0,0,.45))}}
.dt,.rg,.end{{transform-box:fill-box;transform-origin:center}}
.lb{{position:absolute;transform:translateY(-100%);padding-bottom:12px;white-space:nowrap;direction:{tp['dir']}}}
.lk,.lv{{clip-path:none}} .lkw,.lvw{{overflow:hidden}}
.lb.sR{{text-align:left}} .lb.sL{{text-align:right}}
.lk{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:21px;letter-spacing:{'0' if rtl else '.24em'};color:{col['label']};text-transform:uppercase;line-height:1.3}}
.lv{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};color:{col['value']};line-height:1;margin-top:6px;direction:ltr;display:inline-flex;align-items:baseline;gap:6px}}
.lv .n,.lv .pf{{font-size:84px;letter-spacing:-.02em;font-variant-numeric:tabular-nums}}
.lv .u{{font-size:34px;color:{col['accent']};font-weight:{tp['bw']}}}
"""
    J = [{"t": c["t"], "until": c.get("until"), "v": c.get("value", 0), "d": c.get("decimals", 0), "side": c.get("side", "L")} for c in spec["callouts"]]
    j = [JS_UTIL, f"const J = {js(J)};", r"""
const $$ = (id) => document.getElementById(id);
window.onPlace = (t) => {
  J.forEach((c, i) => {
    const u = easeOut3((t - (c.t + .75)) / 1.1);
    $$("n" + i).textContent = (c.v * u).toFixed(c.d);
  });
};
// SVG circles animate their radius (attr r), never a CSS/GSAP transform: transform origins on SVG drift
tl.set(".dt, .end", {attr: {r: 0}}, 0); tl.set(".rg", {attr: {r: 0}, opacity: 0}, 0);
J.forEach((c, i) => {
  const g = `#co${i}`;
  tl.fromTo(`${g} .dt`, {attr: {r: 0}}, {attr: {r: 7}, duration: .35, ease: "back.out(3)", immediateRender: false}, c.t);
  tl.fromTo(`${g} .rg`, {attr: {r: 6}, opacity: 1}, {attr: {r: 40}, opacity: 0, duration: .9, ease: "power2.out", immediateRender: false}, c.t);
  tl.fromTo(`${g} .rg`, {attr: {r: 6}, opacity: .8}, {attr: {r: 40}, opacity: 0, duration: .9, ease: "power2.out", immediateRender: false}, c.t + 2.2);
  tl.fromTo(`${g} .ln`, {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: .6, ease: "power3.inOut"}, c.t + .15);
  tl.fromTo(`${g} .end`, {attr: {r: 0}}, {attr: {r: 4}, duration: .25, ease: "back.out(3)", immediateRender: false}, c.t + .7);
  // labels rise into a fixed mask (never a sideways wipe: half-revealed words read as truncated text)
  tl.fromTo(`${g} .lk`, {yPercent: 110}, {yPercent: 0, duration: .5, ease: "expo.out"}, c.t + .7);
  tl.fromTo(`${g} .lv`, {yPercent: 110}, {yPercent: 0, duration: .55, ease: "expo.out"}, c.t + .78);
  if (c.until != null) {
    // one exit: the label wipes back into the line end while the line retracts toward the dot, then the dot closes
    tl.to(`${g} .lk, ${g} .lv`, {yPercent: -110, duration: .3, ease: "power3.in", stagger: .04}, c.until - .6);
    tl.to(`${g} .end`, {attr: {r: 0}, duration: .15, ease: "power2.in"}, c.until - .6);
    tl.to(`${g} .ln`, {attr: {"stroke-dashoffset": 1}, duration: .4, ease: "power3.in"}, c.until - .6);
    tl.to(`${g} .dt`, {attr: {r: 0}, duration: .2, ease: "power2.in"}, c.until - .22);
  }
});
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_pop", c["t"], .35) for c in spec["callouts"]] + [cue("ui_tick", c["t"] + .75, .25) for c in spec["callouts"]]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .6), extra=tp["files"])
