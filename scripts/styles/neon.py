"""NEON-SIGN: neon tubes mounted in the scene. Outline tubes (display weight, hollow stroke) and solid tubes (body weight)
with a white-hot core and a coloured glow, a deterministic flicker-on (the classic stutter, then full), an occasional
buzz later, a warm spill of light on the plate, and a soft mirrored reflection on the floor below (blurred, fading,
rippling). Signs can sit flat or turned onto a wall plane in perspective. Hebrew or English, RTL-correct.

Spec keys. Required: clip, signs.
  signs      [{"lines": [{"text": "חורף ברחוב", "tube": "outline|solid", "weight": "display|body", "size": 150, "color": "#ff3da8"}],
               "x": 400, "y": 420, "align": "center|left|right", "wall": "left|right|none", "angle": 34,
               "t": 1.0, "until": null, "floor": 650, "reflect": .38}]
             floor = the y where the wall meets the floor (the mirror line); reflect = reflection opacity (0 = none)
  spill      .35   strength of the coloured light spill on the plate around each sign
  vanishing  [960, 540]   the plate's vanishing point; wall signs are projected towards it
  language   "he" | "en";  pair (Hebrew, default "karantina-suez"; see common.HE_PAIRS);
             Latin: Tilt Neon 400 + Tilt Neon 400
  seed;  sfx (true), music, music_vol, plate_vol, name, track (optional)
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="NEON-SIGN"):
    tp = type_pair(spec, latin=("Tilt Neon", 400, "Tilt Neon", 400), default_pair="karantina-suez")
    S, h = spec["signs"], []
    for i, s in enumerate(S):
        lines = []
        for ln in s["lines"]:
            c = ln.get("color", "#ff3da8")
            disp = ln.get("weight", "display") == "display"
            fam, w = (tp["display"], tp["dw"]) if disp else (tp["body"], tp["bw"])
            size = ln.get("size", 150 if disp else 70)
            outline = ln.get("tube", "outline" if disp else "solid") == "outline"
            core = "#fff6fb"
            if outline:
                sty = (f"color:rgba(255,246,251,.10);-webkit-text-stroke:{max(3, size // 34)}px {core};"
                       f"filter:drop-shadow(0 0 2px {c}) drop-shadow(0 0 8px {c}) drop-shadow(0 0 22px {c}) drop-shadow(0 0 48px {c})")
            else:
                sty = f"color:{core};filter:drop-shadow(0 0 2px {c}) drop-shadow(0 0 8px {c}) drop-shadow(0 0 20px {c}) drop-shadow(0 0 42px {c})"
            lines.append(f'<div class="tl" data-layout-allow-overlap data-layout-allow-overflow style="font-family:&quot;{fam}&quot;;font-weight:{w};font-size:{size}px;{sty}">{e(ln["text"])}</div>')
        body = "".join(lines)
        al = s.get("align", "center")
        tx = {"center": "-50%", "left": "0", "right": "-100%"}[al]
        wall = s.get("wall", "none")
        ang = s.get("angle", 34)
        rot = {"left": f"rotateY({ang}deg)", "right": f"rotateY(-{ang}deg)", "none": ""}[wall]
        org = {"left": "0 50%", "right": "100% 50%", "none": "50% 50%"}[wall]
        c0 = s["lines"][0].get("color", "#ff3da8")
        y, fl = s.get("y", 420), s.get("floor", 650)
        vx, vy = spec.get("vanishing", [960, 540])   # the plate's vanishing point: wall signs are projected towards it
        ry = 2 * fl - y
        refl = (f'<div class="rf" style="left:{s.get("x", 960)}px;top:{ry}px">'
                f'<div class="pp" style="perspective-origin:{vx - s.get("x", 960)}px {vy - ry}px"><div class="sg" style="transform:translate({tx},-50%) {rot} scaleY(-1);transform-origin:{org}">{body}</div></div></div>') if s.get("reflect", .38) > 0 else ""
        h.append(f'<div class="neon" id="n{i}">'
                 f'<div class="spill" style="left:{s.get("x", 960)}px;top:{y}px;background:radial-gradient(circle,{c0} 0%,transparent 62%)"></div>'
                 f'<div class="pos" style="left:{s.get("x", 960)}px;top:{y}px"><div class="pp" style="perspective-origin:{vx - s.get("x", 960)}px {vy - y}px"><div class="sg" style="transform:translate({tx},-50%) {rot};transform-origin:{org}">{body}</div></div></div>'
                 f'{refl}</div>')
    css = tp["css"] + f"""
.neon{{position:absolute;inset:0}}
.pos,.rf{{position:absolute;width:0;height:0}}
.pp{{position:absolute;left:0;top:0;perspective:900px}}
.sg{{position:absolute;left:0;top:0;direction:{tp['dir']};white-space:nowrap;text-align:center;display:flex;flex-direction:column;align-items:center;gap:.1em}}
.tl{{line-height:1.05;white-space:nowrap}}
.rf{{filter:blur(4px);mix-blend-mode:screen}}
.rf .sg{{-webkit-mask-image:linear-gradient(0deg,#000 10%,transparent 85%);mask-image:linear-gradient(0deg,#000 10%,transparent 85%)}}
.spill{{position:absolute;width:1300px;height:900px;margin:-450px 0 0 -650px;mix-blend-mode:screen;opacity:0}}
"""
    J = [{"i": i, "t": s.get("t", 1 + i * 2), "until": s.get("until"), "spill": s.get("spill", spec.get("spill", .35)), "reflect": s.get("reflect", .38)} for i, s in enumerate(S)]
    j = [JS_UTIL, f"const SG = {js(J)}, SEED = {int(spec.get('seed', 5))};", r"""
const NE = SG.map(s => ({...s, el: document.getElementById("n" + s.i)}));
NE.forEach(s => { s.pos = s.el.getElementsByClassName("pos")[0]; s.rf = s.el.getElementsByClassName("rf")[0]; s.sp = s.el.getElementsByClassName("spill")[0]; });
// brightness 0..1: a stuttering strike during the first .9 s, full after, a rare one-frame buzz dip later
function level(s, t) {
  const d = t - s.t;
  if (d < 0 || (s.until != null && t >= s.until)) return 0;
  const fr = Math.floor(t * 24);
  if (d < .9) {
    const steps = [[0, .08, 1], [.08, .2, 0], [.2, .26, .7], [.26, .44, .05], [.44, .5, 1], [.5, .58, .2], [.58, .9, 1]];
    for (const [a, b, v] of steps) if (d >= a && d < b) return v * (.85 + .15 * hash1(fr + s.i * 7));
  }
  if (hash1(fr * 1.7 + s.i * 31 + SEED) > .965) return .35;           // buzz dip
  return .93 + .07 * hash1(fr + s.i * 3);                                // hum
}
window.onPlace = (t) => {
  for (const s of NE) {
    const v = level(s, t);
    s.pos.style.opacity = v; if (s.rf) s.rf.style.opacity = v * s.reflect;
    s.sp.style.opacity = v * s.spill;
  }
};
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("lock_tick", s.get("t", 1 + i * 2), .5) for i, s in enumerate(S)] + [cue("lock_tick", s.get("t", 1 + i * 2) + .44, .35) for i, s in enumerate(S)]
    sfx += audio_cues(spec, base, .55)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .45), extra=tp["files"])
