"""DECODE-TYPE: terminal decode. Each line types in while every character scrambles through random glyphs (Hebrew
letters for Hebrew, A-Z/0-9 for Latin) and then locks, in reading order (right-to-left for Hebrew), with a blinking
block cursor. Layout never jitters: the final text reserves the space, the scramble is drawn over it. Seeded.

Spec keys. Required: clip, lines.
  lines      [{"text": "גישה מאושרת", "t": 3.0, "until": 7.5, "x": 960, "y": 820, "align": "center|left|right",
               "size": 120, "weight": "display|body", "dur": 1.2, "color": "#e8fff4", "panel": false,
               "follow": "face", "anchor": "r", "dx": 60, "dy": 0}]
             align = which physical edge of the line sits on (x, y) or on the follow anchor (a panel to the right of a
             face: anchor "r", align "left"); dur = seconds from first glyph to the last locked character
  language   "he" | "en";  pair (Hebrew, default "secular"; see common.HE_PAIRS); latin fonts: IBM Plex Mono + JetBrains Mono
  colors     {"text": "#e8fff4", "scramble": "#5cffb0", "cursor": "#5cffb0", "panel": "rgba(4,12,10,.72)"}
  seed       integer (default 7);  track (optional), music, music_vol, plate_vol, name
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)

HE_SET = "אבגדהוזחטיכלמנסעפצקרשת0123456789"
EN_SET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789#%&*+<>/"


def build(spec, base, style="DECODE-TYPE"):
    tp = type_pair(spec, latin=("IBM Plex Mono", 500, "JetBrains Mono", 500), default_pair="secular")
    col = {"text": "#e8fff4", "scramble": "#5cffb0", "cursor": "#5cffb0", "panel": "rgba(4,12,10,.72)", **spec.get("colors", {})}
    L, h = [], []
    for i, ln in enumerate(spec["lines"]):
        size = ln.get("size", 64)
        fam, w = (tp["display"], tp["dw"]) if ln.get("weight", "body") == "display" else (tp["body"], tp["bw"])
        al = ln.get("align", "center")   # physical: which edge of the line sits on (x, y)
        tx = {"center": "-50%", "left": "0", "right": "-100%"}[al]
        # digit runs (98.6%, 07, 2026) are one left-to-right island so bidi never reorders their characters
        import re as _re
        parts, pos_ = [], 0
        for m in _re.finditer(r"[0-9][0-9.,:%/-]*", ln["text"]):
            parts += [(c, False) for c in ln["text"][pos_:m.start()]] + [(m.group(0), True)]
            pos_ = m.end()
        parts += [(c, False) for c in ln["text"][pos_:]]
        cell = lambda ch: f'<span class="c"><i>{e(ch) if ch != " " else "&nbsp;"}</i><b data-layout-allow-overlap></b></span>'  # noqa: E731
        chars = "".join(f'<span class="iso">{"".join(cell(c) for c in p)}</span>' if num else cell(p) for p, num in parts)
        pos = (f'data-follow="{e(ln["follow"])}" data-anchor="{ln.get("anchor", "c")}" data-dx="{ln.get("dx", 0)}" data-dy="{ln.get("dy", 0)}"'
               if ln.get("follow") else f'style="left:{ln.get("x", 960)}px;top:{ln.get("y", 540)}px"')
        h.append(f'<div class="ln" id="l{i}" {pos}><div class="in{" panel" if ln.get("panel") else ""}" style="transform:translate({tx},-50%);'
                 f'font-family:&quot;{fam}&quot;;font-weight:{w};font-size:{size}px;color:{ln.get("color", col["text"])}">{chars}'
                 f'<span class="cur" style="width:{max(6, round(size * .5))}px;height:{round(size * .9)}px"></span></div></div>')
        L.append({"i": i, "t": ln["t"], "until": ln.get("until"), "dur": ln.get("dur", .9 + .045 * len(ln["text"])), "n": len(ln["text"]),
                  "sp": [k for k, ch in enumerate(ln["text"]) if ch == " "]})
    css = tp["css"] + f"""
.ln{{position:absolute;left:0;top:0;width:0;height:0}}
.in{{position:absolute;left:0;top:0;white-space:nowrap;direction:{tp['dir']};line-height:1.15;display:flex;align-items:center}}
.in.panel{{background:{col['panel']};padding:.18em .45em;border-inline-start:3px solid {col['cursor']}}}
.c{{position:relative;display:inline-block}}
.iso{{direction:ltr;unicode-bidi:isolate;display:inline-flex}}
.c i{{font-style:normal;visibility:hidden}}
.c b{{position:absolute;inset:0;font-weight:inherit;text-align:center;white-space:nowrap;clip-path:inset(-60% 0 -60% 0)}}
.c b.s{{color:{col['scramble']};opacity:.85}}
.cur{{position:absolute;top:50%;transform:translateY(-50%);background:{col['cursor']};box-shadow:0 0 18px {col['cursor']}}}
"""
    j = [JS_UTIL, f"const L = {js(L)}, SET = {js(HE_SET if tp['rtl'] else EN_SET)}, SEED = {int(spec.get('seed', 7))};", r"""
const LN = L.map(l => { const el = document.getElementById("l" + l.i); return {...l, el, cs: [...el.getElementsByClassName("c")], cur: el.getElementsByClassName("cur")[0]}; });
window.onPlace = (t) => {
  const fr = Math.floor(t * 12);   // glyphs change 12x per second
  for (const l of LN) {
    const on = t >= l.t && (l.until == null || t < l.until);
    l.el.style.opacity = on ? 1 : 0;
    if (!on) continue;
    const u = (t - l.t) / l.dur;                       // 0..1 over the decode
    l.cs.forEach((c, k) => {
      const b = c.lastChild, fin = c.firstChild.textContent;
      const appear = k / l.n * .55, lock = .35 + k / l.n * .65;   // types in, then locks in reading order
      let s = "", cls = "";
      if (fin.trim() === "") s = " ";
      else if (u >= lock) s = fin;
      else if (u >= appear) { s = SET[Math.floor(hash1(SEED * 131 + l.i * 977 + k * 31 + fr) * SET.length)]; cls = "s"; }
      if (b.textContent !== s) b.textContent = s;
      if (b.className !== cls) b.className = cls;
      c.style.opacity = u >= appear ? 1 : 0;
    });
    const typing = u < 1, blink = Math.floor(t * 2.4) % 2 === 0;
    l.cur.style.opacity = typing || blink ? 1 : 0;
    // cursor sits just past the last character that has appeared (reading direction aware)
    const last = Math.max(0, Math.min(l.n - 1, Math.floor(clamp01(u / .55) * l.n)));
    const c = l.cs[last], rtl = getComputedStyle(l.cur.parentNode).direction === "rtl";
    l.cur.style.left = (rtl ? c.offsetLeft - l.cur.offsetWidth - 4 : c.offsetLeft + c.offsetWidth + 4) + "px";
  }
};
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("data_chatter", ln["t"], .22) for ln in spec["lines"]] + [cue("lock_tick", ln["t"] + L[i]["dur"], .5) for i, ln in enumerate(spec["lines"])]
    sfx += audio_cues(spec, base, .45)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="\n".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .6), extra=tp["files"])
