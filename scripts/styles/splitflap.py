"""SPLIT-FLAP: a departure board. Every cell is a real split flap (top/bottom halves + a leaf that falls in CSS 3D)
that riffles through random characters before landing on its letter, staggered in reading order; rows can re-flip
later (a status change). Columns carry their own direction, so Hebrew destinations fill right-to-left while times
stay left-to-right. Pure function of t (seeded).

Spec keys. Required: clip, columns, rows.
  columns    [{"w": 5, "dir": "ltr", "label": "שעה"}, {"w": 9, "label": "יעד"}, {"w": 9, "label": "סטטוס", "color": "#ffd23f"}]
             w = cells in the column; dir defaults to the language direction; color = text colour for that column
  rows       [{"cols": ["08:40", "רומא", "עלייה"], "t": 1.0}, ...]    t = when the row starts flipping
  changes    [{"row": 1, "col": 2, "text": "המריא", "t": 9.0}]       re-flip one cell group later
  title      "יציאות · DEPARTURES"  (static header, body weight)
  board      {"x": 1860, "y": 90, "align": "right", "cell": 58}     position (x,y of the aligned top corner) and cell width px
  language   "he" | "en";  pair (Hebrew, default "karantina"; see common.HE_PAIRS); Latin: Oswald 700 + Jost 300
  colors     {"board": "rgba(12,12,12,.86)", "cell": "#1d1d1d", "text": "#f4f1e8", "label": "#b9b3a8"}
  flip       seconds per flip (default .055);  seed;  sfx (true), music, music_vol, plate_vol, name, track (optional)
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)

HE_SET = "אבגדהוזחטיכלמנסעפצקרשת"
EN_SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIG = "0123456789"


def build(spec, base, style="SPLIT-FLAP"):
    tp = type_pair(spec, latin=("Oswald", 700, "Jost", 300), default_pair="karantina")
    col = {"board": "rgba(12,12,12,.86)", "cell": "#1d1d1d", "text": "#f4f1e8", "label": "#b9b3a8", **spec.get("colors", {})}
    C, R = spec["columns"], spec["rows"]
    bd = {"x": 1860 if tp["rtl"] else 60, "y": 90, "align": "right" if tp["rtl"] else "left", "cell": 58, **spec.get("board", {})}
    cw = bd["cell"]
    chh = round(cw * 1.42)
    cells, h = [], []
    # a header spans exactly its column (w cells + the 4 px gaps between them) and is centred on it, so it reads as
    # belonging to that column whatever the column's own direction (LTR times sit next to RTL names on a Hebrew board)
    head = "".join(f'<div class="col lab" style="width:{c["w"] * cw + (c["w"] - 1) * 4}px;direction:{tp["dir"]}">{e(c.get("label", ""))}</div>' for c in C)
    rows_html = []
    for ri, r in enumerate(R):
        cols_html = []
        for ci, c in enumerate(C):
            txt = str(r["cols"][ci]) if ci < len(r["cols"]) else ""
            d = c.get("dir", tp["dir"])
            ids = []
            for k in range(c["w"]):
                cid = f"c{ri}_{ci}_{k}"
                A = "data-layout-allow-overflow data-layout-allow-occlusion data-layout-allow-overlap"   # half-glyph clipping IS the flap
                ids.append(f'<div class="cell" id="{cid}"><div class="h t"><span {A}></span></div><div class="h b"><span {A}></span></div>'
                           f'<div class="leaf"><span {A}></span></div></div>')
                cells.append({"id": cid, "r": ri, "c": ci, "k": k, "segs": [[r["t"] + .03 * (k + 3 * ci), txt[k] if k < len(txt) else " "]],
                              "num": (txt[k] if k < len(txt) else " ") in DIG + ":.-", "color": c.get("color")})
            cols_html.append(f'<div class="col" style="direction:{d}">{"".join(ids)}</div>')
        rows_html.append('<div class="row">' + "".join(cols_html) + "</div>")
    for ch in spec.get("changes", []):
        txt = str(ch["text"])
        for cl in cells:
            if cl["r"] == ch["row"] and cl["c"] == ch["col"]:
                cl["segs"].append([ch["t"] + .03 * cl["k"], txt[cl["k"]] if cl["k"] < len(txt) else " "])
    tx = {"left": "0", "right": "-100%", "center": "-50%"}[bd["align"]]
    title = f'<div class="ttl">{e(spec["title"])}</div>' if spec.get("title") else ""
    h.append(f'<div id="board" style="left:{bd["x"]}px;top:{bd["y"]}px;transform:translateX({tx})">{title}<div class="row hd">{head}</div>{"".join(rows_html)}</div>')
    fs = round(cw * .95)
    css = tp["css"] + f"""
#board{{position:absolute;background:{col['board']};padding:22px 24px 26px;border-radius:10px;box-shadow:0 30px 70px rgba(0,0,0,.45);direction:{tp['dir']}}}
.ttl{{font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:{round(cw * .8)}px;color:{col['text']};letter-spacing:{'0' if tp['rtl'] else '.18em'};margin:0 4px 12px}}
.row{{display:flex;gap:{round(cw * .5)}px;margin-top:6px}}
.row.hd{{margin:0 0 4px}}
.col{{display:flex;gap:4px}}
.col.lab{{font-family:"{tp['body']}",sans-serif;font-weight:{max(400, tp['bw'])};font-size:{round(cw * .56)}px;color:{col['label']};letter-spacing:{'0' if tp['rtl'] else '.14em'};justify-content:center;box-sizing:border-box;padding:0 4px}}
.cell{{position:relative;width:{cw}px;height:{chh}px;perspective:{cw * 8}px}}
.h,.leaf{{position:absolute;left:0;width:100%;height:50%;overflow:hidden;background:{col['cell']};border-radius:4px}}
.h.t,.leaf.t{{top:0;border-bottom:1px solid rgba(0,0,0,.65)}}
.h.b,.leaf.b{{top:50%;border-top:1px solid rgba(255,255,255,.04)}}
.h span,.leaf span{{position:absolute;left:0;width:100%;height:{chh}px;line-height:{chh}px;text-align:center;font-family:"{tp['display']}",sans-serif;
  font-weight:{tp['dw']};font-size:{fs}px;color:{col['text']}}}
.h.b span,.leaf.b span{{top:-{chh // 2}px}}
.h.t span,.leaf.t span{{top:0}}
.leaf{{transform-origin:50% 100%;backface-visibility:hidden;box-shadow:0 2px 6px rgba(0,0,0,.35)}}
.leaf.b{{transform-origin:50% 0}}
"""
    J = [{"id": c["id"], "segs": c["segs"], "num": c["num"], "color": c["color"]} for c in cells]
    j = [JS_UTIL, f"const CELLS = {js(J)}, SET = {js(HE_SET if tp['rtl'] else EN_SET)}, DIG = {js(DIG)}, FLIP = {spec.get('flip', .055)}, SEED = {int(spec.get('seed', 3))};", r"""
// each segment: riffle through n random chars from the previous glyph to the target, one flip every FLIP seconds
const CL = CELLS.map((c, i) => {
  const el = document.getElementById(c.id);
  const q = (s) => el.querySelector(s + " span");
  const seq = [];   // [[t0, fromChar, toChar], ...] one entry per flip
  let cur = " ";
  c.segs.forEach(([t0, target], si) => {
    if (target === cur) return;
    const n = target === " " ? 3 : 5 + Math.floor(hash1(SEED * 71 + i * 13 + si * 7) * 9);
    const pool = c.num ? DIG : SET;
    for (let k = 0; k < n; k++) {
      const nxt = k === n - 1 ? target : pool[Math.floor(hash1(SEED * 3 + i * 101 + si * 37 + k * 17) * pool.length)];
      seq.push([t0 + k * FLIP, cur, nxt]); cur = nxt;
    }
  });
  if (c.color) el.querySelectorAll("span").forEach(s => s.style.color = c.color);
  return {seq, top: q(".h.t"), bot: q(".h.b"), leaf: el.querySelector(".leaf"), lspan: q(".leaf")};
});
const put = (s, v) => { if (s.textContent !== v) s.textContent = v; };
window.onPlace = (t) => {
  for (const c of CL) {
    let k = -1;
    for (let i = 0; i < c.seq.length; i++) if (t >= c.seq[i][0]) k = i; else break;
    if (k < 0) { put(c.top, " "); put(c.bot, " "); c.leaf.style.display = "none"; continue; }
    const [t0, from, to] = c.seq[k], p = Math.min(1, (t - t0) / FLIP);
    if (p >= 1) { put(c.top, to); put(c.bot, to); c.leaf.style.display = "none"; continue; }
    // top half already shows the next char; bottom still the old one; the leaf falls
    put(c.top, to); put(c.bot, from); c.leaf.style.display = "block";
    if (p < .5) { c.leaf.className = "leaf t"; put(c.lspan, from); c.leaf.style.transform = `rotateX(${-180 * p}deg)`; }
    else { c.leaf.className = "leaf b"; put(c.lspan, to); c.leaf.style.transform = `rotateX(${180 * (1 - p)}deg)`; }
  }
};
tl.fromTo("#board", {opacity: 0, y: -20}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, Math.max(0, Math.min(...CELLS.map(c => c.segs[0][0])) - .6));
"""]
    if spec.get("until") is not None:
        j.append(f'tl.to("#board", {{opacity: 0, duration: .5}}, {spec["until"]});')
    sfx = []
    if spec.get("sfx", True):
        starts = sorted({round(r["t"], 2) for r in R} | {round(c["t"], 2) for c in spec.get("changes", [])})
        sfx = [cue("data_chatter", t0, .35) for t0 in starts] + [cue("ui_tick", t0 + .25, .3) for t0 in starts]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="\n".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .5), extra=tp["files"])
