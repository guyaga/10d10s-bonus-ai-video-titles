"""SWISS-GRID: International Typographic Style kinetic type. A 12-column grid draws itself over the shot, heavy grotesk
statements rise line by line out of masks and snap to the columns, a Swiss-red square jumps between grid cells on the beat,
a counter and a small caption column set the rhythm. Built for clean architecture, design and tech brand films.
English by default; Hebrew statements run RTL from the right edge of the grid.

Spec keys. Required: clip, frames.
  frames     [{"lines": ["FORM", "FOLLOWS", "FUNCTION."], "t": 0.6, "until": 4.9, "col": 1, "red": [9, 2], "caption": "…"}, ...]
             col = start column (0-11) of the lines; red = [col, row] cell of the red square (rows are 120 px from the top margin)
  ink        "dark" (default, for white walls/sky) | "light"
  grid       true (default) — show the column lines;  size (default 190) — statement font size
  label      "ARCHITECTURE" — small running label next to the counter (optional)
  language   "en" | "he";  pair (Hebrew, default "secular"); Latin: Manrope 800 + Manrope 500
  colors     {"red": "#e3342f"}
  sfx (true), plate_vol, music, music_vol, name
"""
from styles.common import (audio_cues, cue, e, js, project_dir, res, tracks, type_pair)

M, COLS = 96, 12
CW = (1920 - 2 * M) / COLS


def cx(c):
    return round(M + c * CW)


def build(spec, base, style="SWISS-GRID"):
    tp = type_pair(spec, latin=("Manrope", 700, "Manrope", 500), default_pair="secular")
    rtl = tp["rtl"]
    col = {"red": "#e3342f", **spec.get("colors", {})}
    dark = spec.get("ink", "dark") == "dark"
    ink = "#111111" if dark else "#ffffff"
    line = "rgba(17,17,17,.22)" if dark else "rgba(255,255,255,.3)"
    size = spec.get("size", 190)
    F = spec["frames"]
    css = tp["css"] + f"""
.gl{{position:absolute;top:{M}px;bottom:{M}px;width:1px;background:{line};transform-origin:50% 0}}
.gh{{position:absolute;left:{M}px;right:{M}px;height:1px;background:{line};transform-origin:0 50%}}
.fr{{position:absolute;top:{M + 150}px;direction:{tp['dir']}}}
.fr .l{{overflow:hidden;height:{round(size * .98)}px}}
.fr .l span{{display:block;font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};font-size:{size}px;line-height:{round(size * .98)}px;
  letter-spacing:{'0' if rtl else '-.045em'};color:{ink};white-space:nowrap}}
#red{{position:absolute;left:0;top:0;width:{round(CW)}px;height:{round(CW)}px;background:{col['red']}}}
#meta{{position:absolute;top:{M + 24}px;left:{cx(0)}px;right:{M}px;display:flex;justify-content:space-between;align-items:baseline;
  font-family:"{tp['body']}",sans-serif;font-weight:500;font-size:24px;letter-spacing:.06em;color:{ink};direction:{tp['dir']}}}
#meta b{{font-weight:{400 if tp['rtl'] else 700};font-variant-numeric:tabular-nums;letter-spacing:0}}
.cap{{position:absolute;bottom:{M + 30}px;width:{round(CW * 3)}px;font-family:"{tp['body']}",sans-serif;font-weight:500;font-size:28px;line-height:1.3;color:{ink};
  direction:{tp['dir']};border-top:2px solid {ink};padding-top:14px}}
"""
    grid = ""
    if spec.get("grid", True):
        grid = "".join(f'<i class="gl" id="g{c}" style="left:{cx(c)}px"></i>' for c in range(COLS + 1))
        grid += f'<i class="gh" id="gh0" style="top:{M}px"></i><i class="gh" id="gh1" style="top:{1080 - M}px"></i>'
    frames = ""
    for k, fr in enumerate(F):
        c0 = fr.get("col", 1)
        pos = f"right:{1920 - cx(COLS - c0)}px" if rtl else f"left:{cx(c0)}px"
        ls = "".join(f'<div class="l"><span>{e(t)}</span></div>' for t in fr["lines"])
        frames += f'<div class="fr" id="f{k}" style="{pos}">{ls}</div>'
        if fr.get("caption"):
            cc = fr.get("cap_col", 9)
            frames += f'<div class="cap" id="c{k}" style="left:{cx(cc)}px">{e(fr["caption"])}</div>'
    label = spec.get("label", "")
    hud = grid + '<div id="red"></div>' + frames + f'<div id="meta"><span>{e(label)}</span><b id="cnt">01</b></div>'
    J = {"F": [{"t": f["t"], "until": f.get("until"), "n": len(f["lines"]), "red": f.get("red", [9, 2]), "cap": bool(f.get("caption"))} for f in F],
         "M": M, "CW": CW, "grid": spec.get("grid", True), "cols": COLS}
    j = [f"const G = {js(J)};", r"""
if (G.grid) {
  for (let c = 0; c <= G.cols; c++) tl.fromTo("#g" + c, {scaleY: 0}, {scaleY: 1, duration: .9, ease: "power3.inOut"}, .05 + c * .035);
  tl.fromTo("#gh0,#gh1", {scaleX: 0}, {scaleX: 1, duration: 1.0, ease: "power3.inOut"}, .1);
}
tl.fromTo("#meta", {opacity: 0, y: -10}, {opacity: 1, y: 0, duration: .6, ease: "power3.out"}, .35);
const cell = (r) => [G.M + r[0] * G.CW, G.M + 150 + r[1] * 120];
// the red square: pops into its first cell, then snaps cell to cell with a hard ease (the grid is the rhythm)
const r0 = cell(G.F[0].red);
tl.fromTo("#red", {x: r0[0], y: r0[1], scale: 0}, {scale: 1, duration: .45, ease: "back.out(2)"}, G.F[0].t + .5);
window.onPlace = (t) => {
  let k = 0; G.F.forEach((f, i) => { if (t >= f.t - .1) k = i; });
  const s = String(k + 1).padStart(2, "0"), el = document.getElementById("cnt");
  if (el.textContent !== s) el.textContent = s;
};
G.F.forEach((f, k) => {
  const id = "#f" + k;
  // each statement exists only inside its own window (no hidden text stacked under the live one)
  tl.set(id, {visibility: "hidden"}, 0);
  tl.set(id, {visibility: "visible"}, f.t - .02);
  if (f.until != null) tl.set(id, {visibility: "hidden"}, f.until + .05);
  for (let i = 0; i < f.n; i++)
    tl.fromTo(`${id} .l:nth-child(${i + 1}) span`, {yPercent: 102}, {yPercent: 0, duration: .75, ease: "expo.out"}, f.t + i * .14);
  if (f.cap) tl.fromTo("#c" + k, {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .6, ease: "power3.out"}, f.t + .5);
  if (k > 0) {
    const r = cell(f.red);
    tl.to("#red", {x: r[0], y: r[1], duration: .5, ease: "expo.inOut"}, f.t - .1);
    tl.fromTo("#cnt", {yPercent: 60, opacity: 0}, {yPercent: 0, opacity: 1, duration: .35, ease: "power3.out"}, f.t);
  }
  if (f.until != null) {
    for (let i = 0; i < f.n; i++)
      tl.to(`${id} .l:nth-child(${i + 1}) span`, {yPercent: -102, duration: .5, ease: "power3.in"}, f.until - .5 + i * .06);
    if (f.cap) tl.to("#c" + k, {opacity: 0, duration: .35}, f.until - .4);
  }
});
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", .05, .2)]
        for f in F:
            sfx += [cue("soft_click", f["t"] + i * .14, .28) for i in range(len(f["lines"]))]
            sfx.append(cue("soft_thump", f["t"] + .5 if f is F[0] else f["t"] - .1, .35))
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .5), extra=tp["files"])
