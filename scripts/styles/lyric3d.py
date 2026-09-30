"""LYRIC-KINETIC-3D: music-video kinetic lyrics in 3D space. Every word flies in from depth (translateZ + rotation + blur)
exactly on its sung syllable (word timings), big condensed key words and small italic connective words build a layered
composition, chosen words live BEHIND the performer (matte), the front and back planes drift in opposite directions with
the camera for parallax, and each phrase leaves by falling back into depth. English or Hebrew.

Spec keys. Required: clip, words; matte (for any "back" word).
  words      [{"w": "SHADOWS", "t": 1.08, "x": 960, "y": 170, "size": 360, "kind": "big|script|outline", "layer": "front|back",
               "align": "left|center|right", "phrase": 0, "glow": false, "tight": false}, ...]
             tight = this word is set in a deliberate tight lockup with a neighbour (stacked MY / WAY): skips the overlap lint
             x/y = anchor point in 1920x1080 (left/center/right edge per align, top of the word); phrase groups exit together
  exits      {"0": 4.25, "1": null}   phrase -> exit time (null: holds to the end)
  matte      subject matte webm (npx hyperframes remove-background plate.mp4 -o matte.webm)
  drift      degrees of plane rotation over the clip (default 5; front and back turn opposite ways)
  language   "en" | "he";  pair (Hebrew, default "karantina-suez": Karantina display + Suez One script); Latin: Anton + Cormorant Garamond italic
  colors     {"text": "#ffffff", "glow": "#ff3fb4", "outline": "rgba(255,63,180,.85)"}
  sfx (false by default: the song is the soundtrack), plate_vol (default 1), music, music_vol, name
"""
from styles.common import (optional_file, audio_cues, e, fonts, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="LYRIC-KINETIC-3D"):
    tp = type_pair(spec, latin=("Anton", 400, "Cormorant Garamond", 600), default_pair="karantina-suez")
    rtl = tp["rtl"]
    col = {"text": "#ffffff", "glow": "#ff3fb4", "outline": "rgba(255,63,180,.85)", **spec.get("colors", {})}
    W = spec["words"]
    matte = optional_file(base, spec.get("matte"), "matte", "'back' words move to the front layer")
    if not matte:
        W = [{**w, "layer": "front"} for w in W]
    script_style = "normal" if rtl else "italic"
    css = tp["css"] + f"""
.plane{{position:absolute;inset:0;perspective:1500px;perspective-origin:50% 45%}}
.pin{{position:absolute;left:0;top:0;transform-style:preserve-3d}}
.wd{{position:absolute;top:0;white-space:nowrap;will-change:transform,opacity,filter;direction:{tp['dir']};backface-visibility:hidden}}
.wd.left{{left:0}} .wd.center{{left:0;transform:translateX(-50%)}} .wd.right{{right:0}}
.big{{font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};line-height:.9;color:{col['text']};letter-spacing:{'0' if rtl else '.02em'};
  text-transform:uppercase;text-shadow:0 12px 50px rgba(0,0,0,.45)}}
.script{{font-family:"{tp['body']}",serif;font-weight:{tp['bw']};font-style:{script_style};line-height:1;color:{col['text']};text-shadow:0 4px 30px rgba(0,0,0,.6)}}
.outline{{font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};line-height:.9;color:rgba(20,6,24,.12);-webkit-text-stroke:3px {col['outline']};
  letter-spacing:{'0' if rtl else '.08em'};text-transform:uppercase}}
.glow{{color:#fff;text-shadow:0 0 22px {col['glow']},0 0 60px {col['glow']},0 10px 40px rgba(0,0,0,.4)}}
"""
    if rtl:
        css += "\n.big,.outline{text-transform:none}"

    def word_html(i, w):
        cls = f'wd {w.get("align", "left")} {w.get("kind", "big")}' + (" glow" if w.get("glow") else "")
        allow = " data-layout-allow-occlusion data-layout-allow-overlap" if w.get("layer") == "back" else ""   # hidden behind the performer on purpose
        if w.get("tight"):
            allow += " data-layout-allow-overlap"      # a deliberate tight lockup with its neighbour (e.g. "of the" over LIGHT)
        return (f'<div class="pin" style="left:{w["x"]}px;top:{w["y"]}px"><div class="{cls}" id="w{i}" style="font-size:{w.get("size", 200)}px"{allow}>'
                f'{e(w["w"])}</div></div>')

    back = "".join(word_html(i, w) for i, w in enumerate(W) if w.get("layer") == "back")
    front = "".join(word_html(i, w) for i, w in enumerate(W) if w.get("layer", "front") == "front")
    has_back = bool(back)
    hud = (f'<div class="plane" id="pb">{back}</div>' + ("<!--MATTE-->" if has_back else "") + f'<div class="plane" id="pf">{front}</div>')
    exits = {str(k): v for k, v in spec.get("exits", {}).items()}
    J = {"W": [{"i": i, "t": w["t"], "ph": str(w.get("phrase", 0)), "a": w.get("align", "left"), "layer": w.get("layer", "front"),
                "kind": w.get("kind", "big")} for i, w in enumerate(W)], "X": exits, "drift": spec.get("drift", 5), "rtl": rtl}
    j = [f"const K = {js(J)};", r"""
// planes counter-rotate with the camera orbit: front turns one way, back the other (parallax depth)
tl.fromTo("#pf", {rotationY: -K.drift / 2}, {rotationY: K.drift / 2, duration: DUR, ease: "none"}, 0);
tl.fromTo("#pb", {rotationY: K.drift / 2, scale: 1.02}, {rotationY: -K.drift / 2, scale: 1.06, duration: DUR, ease: "none"}, 0);
K.W.forEach((w, n) => {
  const id = "#w" + w.i, cx = w.a === "center" ? -50 : 0, dir = (n % 2 ? 1 : -1) * (K.rtl ? -1 : 1);
  const from = w.kind === "script"
    ? {opacity: 0, z: -520, rotationY: 38 * dir, rotationX: 10, xPercent: cx, filter: "blur(10px)"}
    : {opacity: 0, z: -900, rotationX: 55, rotationY: 12 * dir, xPercent: cx, filter: "blur(14px)"};
  tl.fromTo(id, from, {opacity: 1, z: 0, rotationY: 0, rotationX: 0, xPercent: cx, filter: "blur(0px)", duration: w.kind === "script" ? .5 : .62,
                       ease: w.kind === "script" ? "power3.out" : "expo.out"}, w.t - .06);
  // a tiny settle overshoot on the big words sells the weight
  if (w.kind !== "script") tl.fromTo(id, {scale: 1.06}, {scale: 1, duration: .45, ease: "power2.out"}, w.t + .3);
  const x = K.X[w.ph];
  if (x != null) tl.to(id, {opacity: 0, z: -700, rotationX: -30, filter: "blur(12px)", duration: .45, ease: "power2.in"}, x - .45 + (n % 3) * .04);
});
"""]
    extra = dict(tp["files"])
    if has_back:
        extra["matte.webm"] = matte
    sfx = audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", 1.0), extra=extra)
