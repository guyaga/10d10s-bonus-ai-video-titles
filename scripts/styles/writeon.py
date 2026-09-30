"""SIGNATURE-WRITE-ON: handwriting and marker annotations that draw themselves over the shot. Notes write on (the
outline draws while a sweep reveals the ink in reading direction: right-to-left for Hebrew), hand circles (wobbly,
overshooting ellipses), boxes, underlines and arrows draw on with stroke-dashoffset, and shapes can be pinned to
tracked objects so they ride the footage. Seeded wobble, pure function of t.

Spec keys. Required: clip, notes.
  notes      [{"text": "the penthouse.", "x": 560, "y": 210, "size": 110, "t": 12.6, "dur": 1.1, "until": null,
               "follow": "terrace", "anchor": "t", "dx": -300, "dy": -160,          (optional: pin the note to an object)
               "underline": true,
               "mark": {"obj": "terrace", "shape": "circle|box|underline|none", "pad": 24, "t": 13.3, "dur": .8},
               "arrow": {"to": "terrace" | [x, y], "t": 13.8, "dur": .6, "bend": .25}}]
  language   "he" | "en";  hand font: Caveat 700 (Latin) / Karantina 700 (Hebrew); pair only sets the Hebrew body
  colors     {"ink": "#ffffff", "marker": "#ff3b30", "shadow": "rgba(0,0,0,.45)"}   bright skies: dark ink + light shadow
  stroke     marker width px (default 7);  seed;  sfx (true), music, music_vol, plate_vol, name, track
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, fonts, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="SIGNATURE-WRITE-ON"):
    tp = type_pair(spec, latin=("Caveat", 700, "Caveat", 600), default_pair="secular")
    hand = "Karantina" if tp["rtl"] else "Caveat"   # Hebrew hand: Karantina (Guy's Hebrew system)
    fc, ff = fonts(hand)
    col = {"ink": "#ffffff", "marker": "#ff3b30", "shadow": "rgba(0,0,0,.45)", **spec.get("colors", {})}
    N, h = spec["notes"], []
    for i, n in enumerate(N):
        size = n.get("size", 100)
        anchor = "end" if tp["rtl"] else "start"
        h.append(f'<g id="n{i}" opacity="0"><clipPath id="cp{i}"><rect id="cr{i}" x="0" y="0" width="0" height="1080"/></clipPath>'
                 f'<g clip-path="url(#cp{i})"><text id="tx{i}" class="hw" font-size="{size}" text-anchor="{anchor}" direction="{tp["dir"]}">{e(n["text"])}</text>'
                 f'<text id="to{i}" class="hwo" font-size="{size}" text-anchor="{anchor}" direction="{tp["dir"]}" pathLength="1">{e(n["text"])}</text></g>'
                 f'<path id="u{i}" class="mk" pathLength="1"/><path id="m{i}" class="mk" pathLength="1"/><path id="a{i}" class="mk" pathLength="1"/>'
                 f'<path id="ah{i}" class="mk"/></g>')
    css = tp["css"] + fc + f"""
#wo{{position:absolute;left:0;top:0;width:1920px;height:1080px;overflow:visible}}
.hw{{font-family:"{hand}",cursive;font-weight:700;fill:{col['ink']};filter:drop-shadow(0 3px 6px {col['shadow']})}}
.hwo{{font-family:"{hand}",cursive;font-weight:700;fill:none;stroke:{col['ink']};stroke-width:2;stroke-dasharray:1;stroke-dashoffset:1}}
.mk{{fill:none;stroke:{col['marker']};stroke-width:{spec.get('stroke', 7)};stroke-linecap:round;stroke-linejoin:round;filter:drop-shadow(0 2px 4px {col['shadow']})}}
"""
    J = [{"i": i, "t": n["t"], "dur": n.get("dur", .9 + .045 * len(n["text"])), "until": n.get("until"), "x": n.get("x", 960), "y": n.get("y", 540),
          "follow": n.get("follow"), "anchor": n.get("anchor", "c"), "dx": n.get("dx", 0), "dy": n.get("dy", 0), "ul": bool(n.get("underline")),
          "mark": n.get("mark"), "arrow": n.get("arrow")} for i, n in enumerate(N)]
    j = [JS_UTIL, f"const N = {js(J)}, RTL = {js(tp['rtl'])}, SEED = {int(spec.get('seed', 4))};", r"""
const $$ = (id) => document.getElementById(id);
// seeded hand wobble: a closed ellipse that overshoots its start by ~15% like a real marker circle
const WOB = N.map((n, i) => { const r = mulberry32(SEED * 97 + i); return Array.from({length: 40}, () => (r() - .5)); });
function circ(b, pad, i, u) {
  const cx = (b[0] + b[2]) / 2, cy = (b[1] + b[3]) / 2, rx = (b[2] - b[0]) / 2 + pad, ry = (b[3] - b[1]) / 2 + pad, w = WOB[i];
  let d = ""; const K = 48, turns = 1.15, a0 = -2.2;
  for (let k = 0; k <= K; k++) {
    const a = a0 + turns * 2 * Math.PI * k / K, n = 1 + w[k % 40] * .06 + (k / K) * .05;
    d += (k ? " L" : "M") + (cx + Math.cos(a) * rx * n).toFixed(1) + "," + (cy + Math.sin(a) * ry * n).toFixed(1);
  }
  return d;
}
function boxp(b, pad, i) {
  const w = WOB[i], j = (k) => w[k] * 10, x0 = b[0] - pad, y0 = b[1] - pad, x1 = b[2] + pad, y1 = b[3] + pad;
  return `M${x0 + j(1)},${y0 + j(2)} L${x1 + j(3)},${y0 + j(4)} L${x1 + j(5)},${y1 + j(6)} L${x0 + j(7)},${y1 + j(8)} L${x0 + j(9)},${y0 + j(10) + 14}`;
}
function under(x0, x1, y, i) { const w = WOB[i]; return `M${x0},${y + w[3] * 6} Q${(x0 + x1) / 2},${y + 14 + w[5] * 8} ${x1},${y - 6 + w[7] * 6}`; }
const draw = (el, u) => { el.style.strokeDasharray = "1"; el.style.strokeDashoffset = String(1 - clamp01(u)); el.style.opacity = u > 0 ? 1 : 0; };
window.onPlace = (t) => {
  for (const n of N) {
    const g = $$("n" + n.i), on = t >= n.t && (n.until == null || t < n.until);
    g.setAttribute("opacity", on ? "1" : "0");
    if (!on) continue;
    let x = n.x, y = n.y;
    if (n.follow) { const b = boxAt(n.follow, t); if (b) { const p = anchor(b, n.anchor); x = p[0] + n.dx; y = p[1] + n.dy; } }
    const tx = $$("tx" + n.i), to = $$("to" + n.i);
    for (const el of [tx, to]) { el.setAttribute("x", x); el.setAttribute("y", y); }
    const bb = tx.getBBox(), u = clamp01((t - n.t) / n.dur);
    // sweep reveal in reading direction + outline draw
    const cr = $$("cr" + n.i), wdt = (bb.width + 40) * easeOut3(u * 1.05);
    cr.setAttribute("y", bb.y - 40); cr.setAttribute("height", bb.height + 80); cr.setAttribute("width", wdt);
    cr.setAttribute("x", RTL ? bb.x + bb.width + 20 - wdt : bb.x - 20);
    to.style.strokeDashoffset = String(1 - clamp01(u * 1.2)); tx.style.opacity = clamp01((u - .15) / .5);
    to.style.opacity = u < 1 ? 1 : 0;   // the outline is only the pen drawing; the ink stays
    const ue = $$("u" + n.i);
    if (n.ul) { ue.setAttribute("d", under(bb.x - 10, bb.x + bb.width + 10, bb.y + bb.height + 6, n.i)); draw(ue, (t - n.t - n.dur * .8) / .45); }
    const m = n.mark, me = $$("m" + n.i);
    if (m && m.obj) {
      const b = boxAt(m.obj, t), mu = (t - (m.t ?? n.t + n.dur)) / (m.dur ?? .8);
      if (b) { me.setAttribute("d", m.shape === "box" ? boxp(b, m.pad ?? 20, n.i) : m.shape === "underline" ? under(b[0], b[2], b[3] + (m.pad ?? 12), n.i) : circ(b, m.pad ?? 24, n.i, mu)); draw(me, mu); }
      else me.style.opacity = 0;
    }
    const a = n.arrow, ae = $$("a" + n.i), ah = $$("ah" + n.i);
    if (a) {
      let tgt = Array.isArray(a.to) ? a.to : null;
      if (!tgt) { const b = boxAt(a.to, t); if (b) { const c = [(b[0] + b[2]) / 2, (b[1] + b[3]) / 2]; tgt = [c[0] - (c[0] - (bb.x + bb.width / 2)) * .08, b[1] - 10]; } }
      if (tgt) {
        const s = [bb.x + bb.width / 2 + (tgt[0] > bb.x + bb.width / 2 ? bb.width * .35 : -bb.width * .35), bb.y + bb.height + 18];
        const mx = (s[0] + tgt[0]) / 2 + (tgt[1] - s[1]) * (a.bend ?? .25), my = (s[1] + tgt[1]) / 2 - (tgt[0] - s[0]) * (a.bend ?? .25);
        ae.setAttribute("d", `M${s[0]},${s[1]} Q${mx},${my} ${tgt[0]},${tgt[1]}`);
        const au = (t - (a.t ?? n.t + n.dur + .3)) / (a.dur ?? .6);
        draw(ae, au);
        const ang = Math.atan2(tgt[1] - my, tgt[0] - mx), L = 30;
        ah.setAttribute("d", `M${tgt[0] - L * Math.cos(ang - .5)},${tgt[1] - L * Math.sin(ang - .5)} L${tgt[0]},${tgt[1]} L${tgt[0] - L * Math.cos(ang + .5)},${tgt[1] - L * Math.sin(ang + .5)}`);
        ah.style.opacity = au >= 1 ? 1 : 0;
      }
    }
  }
};
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_tick", n["t"], .35) for n in N] + [cue("ar_whoosh", (n.get("mark") or {}).get("t", n["t"] + 1), .3) for n in N if n.get("mark")]
    sfx += audio_cues(spec, base, .55)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud=f'<svg id="wo" viewBox="0 0 1920 1080">{"".join(h)}</svg>', js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .4),
                extra={**tp["files"], **ff})
