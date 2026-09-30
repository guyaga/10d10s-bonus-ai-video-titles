"""TEXT-ON-PATH: words that ride a tracked road, river or trail. Every frame the path is rebuilt through the tracked
points (smoothed Catmull-Rom), the route optionally draws on as a glowing line, and each text line slides along it
(SVG textPath startOffset) so the letters bend with the road as the camera moves. Text rides an upright copy of the
route (always laid left-to-right on screen), so letters never stand on their heads; Hebrew works on it because Chrome's
bidi orders the Hebrew runs (never set direction="rtl" on a textPath: Chrome drops the text).

Spec keys. Required: clip, track, route, lines.
  route      ["r0", "r1", "r2", ...]   tracked point/box names in order (track.py points or vtrack boxes: centre used)
  draw       {"t": 1.5, "dur": 2.0, "width": 10, "color": "#9bd14a", "glow": true}   route line draw-on (null = no line)
  lines      [{"text": "TLV → ONO · 12.8 KM", "t": 2.0, "until": 9.0, "from": 0.0, "to": .55, "size": 44, "dy": -18,
               "weight": "display|body", "color": "#ffffff"}]
             from/to = where along the path (0..1) the line's start travels between t and until; dy = offset from the road
  language   "he" | "en";  pair (Hebrew, default "secular"; see common.HE_PAIRS); Latin: Oswald 700 + Jost 500
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="TEXT-ON-PATH"):
    tp = type_pair(spec, latin=("Oswald", 700, "Jost", 500), default_pair="secular")
    rtl = tp["rtl"]
    dr = spec.get("draw", {"t": 1.5, "dur": 2.0})
    dr = None if dr is None else {"t": 1.5, "dur": 2.0, "width": 10, "color": "#9bd14a", "glow": True, **dr}
    L = spec["lines"]
    txt = []
    for i, l in enumerate(L):
        disp = l.get("weight", "display") == "display"
        fam, w = (tp["display"], tp["dw"]) if disp else (tp["body"], tp["bw"])
        txt.append(f'<text id="t{i}" class="rt" dy="{l.get("dy", -18)}" style="font-family:&quot;{fam}&quot;;font-weight:{w};font-size:{l.get("size", 44)}px;'
                   f'fill:{l.get("color", "#ffffff")}"><textPath id="tp{i}" href="#rpu" startOffset="0%">{e(l["text"])}</textPath></text>')
    line = ""
    if dr:
        glow = f'<path id="rg" fill="none" stroke="{dr["color"]}" stroke-opacity=".45" stroke-width="{dr["width"] * 2.6}" stroke-linecap="round" filter="url(#bl)" pathLength="1"/>' if dr["glow"] else ""
        line = glow + f'<path id="rl" fill="none" stroke="{dr["color"]}" stroke-width="{dr["width"]}" stroke-linecap="round" stroke-linejoin="round" pathLength="1"/>'
    svg = (f'<svg id="tpv" viewBox="0 0 1920 1080"><defs><filter id="bl" x="-10%" y="-10%" width="120%" height="120%"><feGaussianBlur stdDeviation="8"/></filter>'
           f'<path id="rpu"/></defs>{line}{"".join(txt)}</svg>')
    css = tp["css"] + """
#tpv{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}
.rt{paint-order:stroke fill;stroke:rgba(0,0,0,.55);stroke-width:5px;stroke-linejoin:round;letter-spacing:.04em}
"""
    J = [{"i": i, "t": l["t"], "until": l.get("until"), "from": l.get("from", 0), "to": l.get("to", .6)} for i, l in enumerate(L)]
    j = [JS_UTIL, f"const ROUTE = {js(spec['route'])}, DR = {js(dr)}, LN = {js(J)}, RTL = {js(rtl)};", r"""
const ctr = (n, t) => { const b = boxAt(n, t); return b ? [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2] : null; };
function catmull(P) {   // smooth path through all points
  if (P.length < 2) return "";
  let d = `M${P[0][0].toFixed(1)},${P[0][1].toFixed(1)}`;
  for (let i = 0; i < P.length - 1; i++) {
    const p0 = P[i - 1] || P[i], p1 = P[i], p2 = P[i + 1], p3 = P[i + 2] || P[i + 1];
    const c1 = [p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6], c2 = [p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6];
    d += ` C${c1[0].toFixed(1)},${c1[1].toFixed(1)} ${c2[0].toFixed(1)},${c2[1].toFixed(1)} ${p2[0].toFixed(1)},${p2[1].toFixed(1)}`;
  }
  return d;
}
window.onPlace = (t) => {
  const P = ROUTE.map(r => ctr(r, t)).filter(Boolean);
  const d = catmull(P);
  // text rides an upright copy of the route: always laid left-to-right on screen so glyphs never stand on their heads.
  // (Chrome drops textPath text that carries direction="rtl"; without it, bidi still orders Hebrew runs correctly.)
  const up = P.length > 1 && P[P.length - 1][0] < P[0][0] ? catmull([...P].reverse()) : d;
  document.getElementById("rpu").setAttribute("d", up);
  if (DR) {
    const u = easeInOut((t - DR.t) / DR.dur);
    for (const id of ["rl", "rg"]) { const el = document.getElementById(id); if (!el) continue; el.setAttribute("d", d);
      el.style.strokeDasharray = "1"; el.style.strokeDashoffset = String(1 - u); el.style.opacity = u > 0 ? 1 : 0; }
  }
  for (const l of LN) {
    const el = document.getElementById("t" + l.i), on = t >= l.t && (l.until == null || t < l.until);
    const fade = Math.min(clamp01((t - l.t) / .4), l.until == null ? 1 : clamp01((l.until - t) / .4));
    el.style.opacity = on ? fade : 0;
    const u = easeInOut((t - l.t) / ((l.until ?? l.t + 6) - l.t));
    document.getElementById("tp" + l.i).setAttribute("startOffset", ((l.from + (l.to - l.from) * u) * 100).toFixed(2) + "%");
  }
};
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = ([cue("scan_beeps", dr["t"], .25)] if dr else []) + [cue("ar_whoosh", l["t"], .4) for l in L]
    sfx += audio_cues(spec, base, .55)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud=svg, js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .5), extra=tp["files"])
