"""PARTICLE-TEXT: words that form out of embers, sand or smoke and dissolve back into them. The text is rasterised once
into a canvas, sampled into target points, and every particle position is an analytic function of (t, seed): no
simulation state, so any frame can be seeked and rendered identically. Hebrew or English (canvas direction set).

Spec keys. Required: clip, words.
  words      [{"text": "SEA SALT", "mode": "embers|sand|smoke", "t": 7.0, "form": 1.2, "hold_until": 9.6, "out": 1.0,
               "x": 960, "y": 380, "size": 210, "weight": "display|body", "sub": "FLEUR DE SEL", "density": 5}]
             form = seconds to assemble, out = seconds to dissolve (null hold_until = stays to the end)
             density = sampling step in px (smaller = more particles; 4-6); scrim = 0..1 soft dark pool behind the word (light plates)
  palette    {"embers": ["#ffb13b", "#ff5a1f", "#fff1c9"], "sand": ["#f3e3c3", "#d9c29b", "#ffffff"], "smoke": ["#f2efe9", "#cfc8bd", "#ffffff"]}
  language   "he" | "en";  pair (Hebrew, default "suez"; see common.HE_PAIRS); Latin: Jost 700 + Jost 300
  seed;  sfx (true), music, music_vol, plate_vol, name, track (optional)
"""
from styles.common import (JS_UTIL, audio_cues, cue, js, project_dir, res, tracks, type_pair)

PAL = {"embers": ["#ffb13b", "#ff5a1f", "#fff1c9"], "sand": ["#f3e3c3", "#d9c29b", "#ffffff"], "smoke": ["#f4f1ec", "#cfc8bd", "#ffffff"]}


def build(spec, base, style="PARTICLE-TEXT"):
    tp = type_pair(spec, latin=("Jost", 700, "Jost", 300), default_pair="suez")
    pal = {**PAL, **spec.get("palette", {})}
    W = []
    for w in spec["words"]:
        disp = w.get("weight", "display") == "display"
        W.append({"text": w["text"], "mode": w.get("mode", "embers"), "t": w["t"], "form": w.get("form", 1.2), "hold": w.get("hold_until"),
                  "out": w.get("out", 1.0), "x": w.get("x", 960), "y": w.get("y", 420), "size": w.get("size", 200),
                  "fam": tp["display"] if disp else tp["body"], "wt": tp["dw"] if disp else tp["bw"], "sub": w.get("sub"),
                  "subsize": w.get("subsize", round(w.get("size", 200) * .26)), "step": w.get("density", 5), "scrim": w.get("scrim", 0)})
    css = tp["css"] + "#pc{position:absolute;left:0;top:0;width:1920px;height:1080px}\n"
    # a hidden DOM copy of each word makes sure the webfont is requested before the canvas samples it
    warm = "".join(f'<span style="position:absolute;left:-4000px;top:0;font-family:&quot;{w["fam"]}&quot;;font-weight:{w["wt"]};font-size:40px">{w["text"]}</span>' for w in W)
    j = [JS_UTIL, f"const W = {js(W)}, PAL = {js(pal)}, RTL = {js(tp['rtl'])}, BODY = {js(tp['body'])}, BW = {tp['bw']}, SEED = {int(spec.get('seed', 11))};", r"""
const cv = document.getElementById("pc"), cx = cv.getContext("2d");
let P = null;   // per word: array of particles {tx, ty, sx, sy, r1..r4, c}
function sample() {
  const off = document.createElement("canvas"); off.width = 1920; off.height = 1080;
  const o = off.getContext("2d", {willReadFrequently: true});
  return W.map((w, wi) => {
    o.clearRect(0, 0, 1920, 1080); o.fillStyle = "#fff"; o.textAlign = "center"; o.textBaseline = "middle"; o.direction = RTL ? "rtl" : "ltr";
    o.font = `${w.wt} ${w.size}px "${w.fam}"`; o.fillText(w.text, w.x, w.y);
    if (w.sub) { o.font = `${BW} ${w.subsize}px "${BODY}"`; o.fillText(w.sub, w.x, w.y + w.size * .72); }
    const d = o.getImageData(0, 0, 1920, 1080).data, rnd = mulberry32(SEED * 1000 + wi), out = [];
    for (let y = 0; y < 1080; y += w.step) for (let x = 0; x < 1920; x += w.step) {
      if (d[(y * 1920 + x) * 4 + 3] < 128) continue;
      const r = [rnd(), rnd(), rnd(), rnd(), rnd()];
      let sx, sy;
      if (w.mode === "embers") { sx = w.x + (r[0] - .5) * 1500; sy = 1120 + r[1] * 260; }          // rise from the fire below
      else if (w.mode === "sand") { sx = (RTL ? 1980 + r[0] * 500 : -60 - r[0] * 500); sy = w.y + (r[1] - .5) * 700; }   // blown in from the reading side
      else { sx = w.x + (r[0] - .5) * 500; sy = w.y + 380 + r[1] * 300; }                        // smoke rises and gathers
      out.push({tx: x, ty: y, sx, sy, r, c: PAL[w.mode][Math.floor(r[4] * 3)]});
    }
    return out;
  });
}
function draw(t) {
  cx.clearRect(0, 0, 1920, 1080);
  if (!P) {
    if (!W.every(w => document.fonts.check(`${w.wt} ${w.size}px "${w.fam}"`))) return;
    P = sample();
  }
  W.forEach((w, wi) => {
    cx.globalCompositeOperation = "lighter";
    const t0 = w.t, t1 = w.t + w.form, t2 = w.hold == null ? 1e9 : w.hold, t3 = t2 + w.out;
    if (t < t0 || t > t3) return;
    // the assembled particles resolve into the crisp word (legible), which hands back to particles to dissolve
    const solid = clamp01((t - t1 - .15) / .5) * (t < t2 ? 1 : 1 - clamp01((t - t2) / (w.out * .35)));
    if (w.scrim) {   // soft dark pool behind the word on light plates
      const life = clamp01((t - t0) / .4) * (t < t2 ? 1 : 1 - clamp01((t - t2) / w.out));
      const g = cx.createRadialGradient(w.x, w.y + w.size * .2, 0, w.x, w.y + w.size * .2, w.size * 3.4);
      g.addColorStop(0, `rgba(10,8,6,${w.scrim * life})`); g.addColorStop(1, "rgba(10,8,6,0)");
      cx.globalCompositeOperation = "source-over"; cx.globalAlpha = 1; cx.fillStyle = g;
      cx.fillRect(w.x - w.size * 3.4, w.y - w.size * 3.2, w.size * 6.8, w.size * 6.8);
    }
    if (solid > 0) {
      cx.globalCompositeOperation = "source-over"; cx.globalAlpha = solid * .92;
      cx.textAlign = "center"; cx.textBaseline = "middle"; cx.direction = RTL ? "rtl" : "ltr";
      cx.shadowColor = PAL[w.mode][0]; cx.shadowBlur = w.mode === "embers" ? 28 : 16;
      cx.fillStyle = w.mode === "embers" ? "#fff4e0" : "#ffffff";
      cx.font = `${w.wt} ${w.size}px "${w.fam}"`; cx.fillText(w.text, w.x, w.y);
      if (w.sub) { cx.font = `${BW} ${w.subsize}px "${BODY}"`; cx.fillText(w.sub, w.x, w.y + w.size * .72); }
      cx.shadowBlur = 0; cx.globalCompositeOperation = "lighter";
    }
    const pa = 1 - solid * .7;   // particles thin out while the solid word is up
    for (const p of P[wi]) {
      const delay = p.r[2] * .45 * w.form, u = easeOut3((t - t0 - delay) / (w.form * .6));
      let x, y, a, s;
      if (t < t2) {                                   // assemble (+ a small living shimmer while holding)
        const sw = (1 - u) * 90;
        x = p.sx + (p.tx - p.sx) * u + Math.sin(t * 3 + p.r[3] * 6.28) * sw;
        y = p.sy + (p.ty - p.sy) * u + Math.cos(t * 2.3 + p.r[0] * 6.28) * sw;
        x += Math.sin(t * 5 + p.r[1] * 40) * .8; y += Math.cos(t * 4 + p.r[2] * 40) * .8;
        a = t < t0 + delay ? 0 : Math.min(1, (t - t0 - delay) / .25); s = 1;
      } else {                                        // dissolve
        const v = clamp01((t - t2 - p.r[2] * .35 * w.out) / (w.out * .65)), v2 = v * v;
        if (w.mode === "embers") { x = p.tx + (p.r[0] - .5) * 160 * v + Math.sin(t * 4 + p.r[3] * 9) * 20 * v; y = p.ty - (220 + p.r[1] * 380) * v2; }
        else if (w.mode === "sand") { x = p.tx + (RTL ? -1 : 1) * (300 + p.r[0] * 700) * v2; y = p.ty + (120 + p.r[1] * 300) * v2; }
        else { x = p.tx + Math.sin(p.r[0] * 6.28 + t) * 120 * v; y = p.ty - (160 + p.r[1] * 260) * v; }
        a = 1 - v; s = 1 + v * (w.mode === "smoke" ? 3 : .5);
      }
      if (a <= 0.01) continue;
      const fl = w.mode === "embers" ? .55 + .45 * hash1(Math.floor(t * 18) + p.r[4] * 997) : 1;
      cx.globalAlpha = a * fl * pa * (w.mode === "smoke" ? .55 : .95);
      cx.fillStyle = p.c;
      const sz = (w.mode === "smoke" ? 4.4 : w.mode === "sand" ? 3.6 : 4.2) * s * (w.step / 5);
      cx.fillRect(x - sz / 2, y - sz / 2, sz, sz);
      if (w.mode === "embers") { cx.globalAlpha *= .35; cx.fillRect(x - sz * 1.4, y - sz * 1.4, sz * 2.8, sz * 2.8); }   // ember halo
    }
  });
  cx.globalAlpha = 1; cx.globalCompositeOperation = "source-over";
}
window.onPlace = draw;
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", w["t"], .35) for w in W] + [cue("ar_whoosh", w["hold"], .3) for w in W if w["hold"] is not None]
    sfx += audio_cues(spec, base, .6)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud=f'<canvas id="pc" width="1920" height="1080"></canvas><div style="position:absolute;opacity:0">{warm}</div>',
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .35), extra=tp["files"])
