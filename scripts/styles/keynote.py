"""KEYNOTE-REVEAL: Apple-keynote style. One huge number or word per beat, revealed by a mask wipe, numbers count up,
a small label and the unit sit with it, clean fade-and-blur exits, a soft vignette keeps contrast. Hebrew or English;
Hebrew wipes run right-to-left and the unit stays glued to its number.

Spec keys. Required: clip, beats.
  beats      [{"text": "3.2", "count": [0, 3.2], "dec": 1, "unit": "שניות", "label": "מ-0 ל-100", "t": 1.0, "until": 4.6,
               "wipe": "up|start|center", "size": 300, "y": 540}]   y overrides the position for that beat
             text without "count" = a word reveal; "count" [from, to] = number counting up over 1.1 s (dec decimals)
  language   "he" | "en";  pair (Hebrew, default "suez"; see common.HE_PAIRS); Latin: Jost 700 + Jost 300
  colors     {"text": "#ffffff", "grad": ["#ffffff", "#9fd8ff"], "label": "#d6dbe3", "vignette": .55}
  position   "center" (default) | "lower"   where the beat sits
  sfx (true), music, music_vol, plate_vol, name, track (optional)
"""
from styles.common import (audio_cues, cue, e, fonts, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="KEYNOTE-REVEAL"):
    tp = type_pair(spec, latin=("Jost", 700, "Jost", 300), default_pair="suez")
    numfam, numw = f'"{tp["display"]}"', tp["dw"]
    if tp["display"] == "Suez One":            # Suez One ships old-style figures ('620' reads '62o'); hero stats need lining digits
        c, f = fonts("Jost")
        tp["css"] += c
        tp["files"].update(f)
        numfam, numw = '"Jost","Suez One"', 600
    col = {"text": "#ffffff", "grad": ["#ffffff", "#9fd8ff"], "label": "#d6dbe3", "vignette": .55, **spec.get("colors", {})}
    B, h = spec["beats"], []
    top = {"center": 540, "lower": 760}[spec.get("position", "center")]
    for i, b in enumerate(B):
        size = b.get("size", 300 if b.get("count") else 220)
        main = f'<span class="num" id="n{i}">{e(b["text"])}</span>'
        unit = f'<span class="unit" style="font-size:{round(size * .32)}px">{e(b["unit"])}</span>' if b.get("unit") else ""
        lab = f'<div class="lab" style="font-size:{round(max(40, size * .2))}px">{e(b["label"])}</div>' if b.get("label") else ""
        h.append(f'<div class="bt" id="b{i}" style="top:{b.get("y", top)}px"><div class="row" style="font-size:{size}px">{main}{unit}</div>{lab}</div>')
    g0, g1 = col["grad"]
    css = tp["css"] + f"""
#vig{{position:absolute;inset:0;background:radial-gradient(ellipse 70% 60% at 50% {round(top / 10.8)}%,rgba(0,0,0,{col['vignette']}),rgba(0,0,0,{col['vignette'] * .35}) 60%,transparent 100%);opacity:0}}
.bt{{position:absolute;left:0;right:0;transform:translateY(-50%);display:flex;flex-direction:column;align-items:center;direction:{tp['dir']};opacity:0}}
.row{{display:flex;align-items:baseline;gap:.12em;line-height:1;white-space:nowrap}}
.num{{font-family:{numfam},sans-serif;font-weight:{numw};letter-spacing:-.02em;background:linear-gradient(180deg,{g0},{g1});
  -webkit-background-clip:text;background-clip:text;color:transparent;font-variant-numeric:tabular-nums;padding:0 .04em}}
.unit{{font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};color:{col['text']}}}
.lab{{font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};color:{col['label']};text-shadow:0 2px 14px rgba(0,0,0,.7);letter-spacing:{'0' if tp['rtl'] else '.08em'};margin-top:.35em}}
"""
    J = [{"i": i, "t": b["t"], "until": b.get("until"), "count": b.get("count"), "dec": b.get("dec", 0), "wipe": b.get("wipe", "up")} for i, b in enumerate(B)]
    j = [f"const B = {js(J)}, RTL = {js(tp['rtl'])};", r"""
const fmt = (v, d) => v.toFixed(d).replace(/\B(?=(\d{3})+(?!\d))/g, ",");
window.onPlace = (t) => {
  for (const b of B) {
    if (!b.count) continue;
    const u = Math.max(0, Math.min(1, (t - b.t - .15) / 1.1)), w = 1 - Math.pow(1 - u, 4);
    const el = document.getElementById("n" + b.i), s = fmt(b.count[0] + (b.count[1] - b.count[0]) * w, b.dec);
    if (el.textContent !== s) el.textContent = s;
  }
};
const MASK = {up: ["inset(100% 0 0 0)", "inset(0% 0 0 0)"], center: ["inset(0 50% 0 50%)", "inset(0 0% 0 0%)"],
  start: RTL ? ["inset(0 0 0 100%)", "inset(0 0 0 0%)"] : ["inset(0 100% 0 0)", "inset(0 0% 0 0)"]};
tl.fromTo("#vig", {opacity: 0}, {opacity: 1, duration: .6}, Math.max(0, B[0].t - .4));
for (const b of B) {
  const id = "#b" + b.i, m = MASK[b.wipe] || MASK.up;
  tl.set(id, {opacity: 1}, b.t);
  tl.fromTo(id + " .row", {clipPath: m[0], y: b.wipe === "up" ? 40 : 0}, {clipPath: m[1], y: 0, duration: .7, ease: "expo.out"}, b.t);
  if (document.querySelector(id + " .lab")) tl.fromTo(id + " .lab", {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .6, ease: "power3.out"}, b.t + .35);
  if (b.until != null) tl.to(id, {opacity: 0, filter: "blur(10px)", scale: .97, duration: .45, ease: "power2.in"}, b.until - .45);
}
"""]
    sfx = [cue("ui_whoosh", b["t"] - .05, .28) for b in B] if spec.get("sfx", True) else []
    sfx += audio_cues(spec, base, .55)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud='<div id="vig"></div>' + "".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .3), extra=tp["files"])
