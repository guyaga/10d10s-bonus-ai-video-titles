"""CAMPUS-AR: smart-glasses style AR labels on a walking tour. Glass tags (English + Hebrew + mono sub-line) pinned to
tracked places or people, pulse dots, a status chip, optional REC + voice waveform, optional logo end card.

Spec keys. Required: clip, track, tags.
  chip     "ONO AR · CAMPUS TOUR"      top-right status chip (optional)
  tags     [{"follow": "shelves", "anchor": "c", "dx": -70, "dy": 0, "en": "Library", "he": "הספרייה", "sub": "OPEN 08-22",
             "t": 1.0, "until": null, "place": "left|right|above|below", "dot": true}]
           place = which side of the anchor the tag sits on (default right)
  rec      {"t": 3.55, "text": "REC"}        optional
  wave     {"t": 3.6, "until": null}         optional animated voice waveform, bottom centre
  end      {"t": 4.2, "logo": "logo.png", "en": "Welcome to Ono", "he": "ברוכים הבאים לאונו"}   optional end card
  colors   {"accent": "#9bd14a", "fg": "#eef4e8", "mute": "#b9c7b0"}
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (TICKS, audio_cues, cue, e, fonts, js, project_dir, res, tracks)

PLACE = {"right": "translate(0,-50%)", "left": "translate(-100%,-50%)", "above": "translate(-50%,-100%)", "below": "translate(-50%,0)"}


def build(spec, base, style="CAMPUS-AR"):
    col = {"accent": "#9bd14a", "fg": "#eef4e8", "mute": "#b9c7b0", **spec.get("colors", {})}
    tags, end = spec["tags"], spec.get("end")
    faces, extra = fonts("Assistant", "JetBrains Mono")
    css = faces + f"""
:root{{--fg:{col['fg']};--mute:{col['mute']};--acc:{col['accent']};--panel:rgba(7,13,9,.8);--line:color-mix(in srgb,var(--acc) 60%,transparent)}}
.mono{{font-family:"JetBrains Mono",monospace}}
.chip{{position:absolute;right:112px;top:60px;display:flex;align-items:center;gap:12px;font-size:20px;letter-spacing:.14em;padding:10px 16px}}
.chip i{{width:12px;height:12px;border-radius:50%;background:var(--acc);display:block}}
.ar{{padding:14px 20px;white-space:nowrap;border-left:4px solid var(--acc);width:max-content;height:auto}}
.ar .en{{display:block;font-size:40px;font-weight:800;line-height:1.05}}
.ar .he{{display:block;font-size:32px;font-weight:600;color:var(--fg);margin-top:2px;direction:rtl;text-align:left}}
.ar .s{{display:block;font-size:18px;letter-spacing:.1em;color:var(--mute);margin-top:6px}}
.pl{{position:absolute;left:0;top:0;width:max-content}}
.dot{{position:absolute;left:-9px;top:-9px;width:18px;height:18px;border-radius:50%;background:var(--acc);box-shadow:0 0 0 5px rgba(7,13,9,.6),0 0 20px var(--acc)}}
#rec{{position:absolute;left:112px;top:60px;display:flex;align-items:center;gap:12px;padding:10px 16px;font-size:22px;letter-spacing:.14em}}
#rec i{{width:16px;height:16px;border-radius:50%;background:#ff4b3e;display:block}}
#wave{{position:absolute;left:50%;bottom:90px;transform:translateX(-50%);display:flex;align-items:center;gap:6px;height:80px;padding:0 22px}}
#wave b{{display:block;width:7px;border-radius:4px;background:var(--acc)}}
#endg{{position:absolute;left:0;right:0;bottom:0;height:520px;background:linear-gradient(180deg,transparent,rgba(5,9,6,.92) 60%)}}
#end{{position:absolute;left:0;right:0;bottom:120px;display:flex;flex-direction:column;align-items:center}}
#end img{{max-width:380px;max-height:180px;display:block;background:#fff;padding:18px 26px;border-radius:10px;box-sizing:content-box}}
#end .en{{font-size:56px;font-weight:800;margin-top:22px;line-height:1.1}}
#end .he{{font-size:44px;font-weight:700;margin-top:6px;direction:rtl}}
"""
    h = [TICKS]
    if spec.get("chip"):
        h.append(f'<div class="chip panel mono"><i></i>{e(spec["chip"])}</div>')
    for i, g in enumerate(tags):
        pos = f'data-follow="{e(g["follow"])}" data-anchor="{g.get("anchor", "c")}"'
        if g.get("dot", True):
            h.append(f'<div id="d{i}" {pos}><div class="dot"></div></div>')
        body = (f'<span class="en">{e(g.get("en", ""))}</span>' + (f'<span class="he">{e(g["he"])}</span>' if g.get("he") else "")
                + (f'<span class="s mono">{e(g["sub"])}</span>' if g.get("sub") else ""))
        dx = g.get("dx", {"right": 36, "left": -36}.get(g.get("place", "right"), 0))
        dy = g.get("dy", {"above": -30, "below": 30}.get(g.get("place", "right"), 0))
        h.append(f'<div id="p{i}" {pos} data-dx="{dx}" data-dy="{dy}"><div class="pl" style="transform:{PLACE[g.get("place", "right")]}">'
                 f'<div id="g{i}" class="ar panel">{body}</div></div></div>')
    if spec.get("rec"):
        h.append(f'<div id="rec" class="panel mono"><i></i>{e(spec["rec"].get("text", "REC"))}</div>')
    if spec.get("wave"):
        h.append('<div id="wave" class="panel">' + "<b></b>" * 36 + "</div>")
    if end:
        if end.get("logo"):
            lp = res(base, end["logo"])
            extra["end_logo" + lp.suffix] = lp
        h.append('<div id="endg"></div><div id="end">' + (f'<img src="assets/end_logo{res(base, end["logo"]).suffix}" alt="">' if end.get("logo") else "")
                 + f'<span class="en">{e(end.get("en", ""))}</span>' + (f'<span class="he">{e(end["he"])}</span>' if end.get("he") else "") + "</div>")
    G = [{"i": i, "t": g.get("t", .6 + .9 * i), "until": g.get("until"), "dot": g.get("dot", True), "place": g.get("place", "right")} for i, g in enumerate(tags)]
    j = [f"const G = {js(G)}, REC = {js(spec.get('rec'))}, WAVE = {js(spec.get('wave'))}, END = {js(end)};", r"""
const W = [...document.querySelectorAll("#wave b")];
window.onPlace = (t) => {
  if (!WAVE) return;
  const on = t > WAVE.t && (WAVE.until == null || t < WAVE.until) ? Math.min(1, (t - WAVE.t) / .4) : 0;
  W.forEach((b, i) => { const v = Math.abs(Math.sin(t * 9 + i * .7) * Math.sin(t * 3.1 + i * .31)); b.style.height = (6 + on * v * 60) + "px"; });
};
tl.fromTo(".tick", {opacity: 0, scale: 1.4}, {opacity: 1, scale: 1, duration: .45, stagger: .05}, .05);
if (document.querySelector(".chip")) { tl.fromTo(".chip", {opacity: 0, x: 20}, {opacity: 1, x: 0, duration: .4}, .2); tl.to(".chip i", {opacity: .25, duration: .5, repeat: 10, yoyo: true, ease: "sine.inOut"}, .6); }
const FROM = {right: {x: -16}, left: {x: 16}, above: {y: 16}, below: {y: -16}};
for (const g of G) {
  tl.set(`#g${g.i}`, {opacity: 0}, 0);
  if (g.dot) { tl.set(`#d${g.i} .dot`, {scale: 0}, 0); tl.fromTo(`#d${g.i} .dot`, {scale: 0}, {scale: 1, duration: .35, ease: "back.out(3)"}, g.t - .1); }
  tl.fromTo(`#g${g.i}`, {opacity: 0, ...FROM[g.place], clipPath: "inset(0 0 100% 0)"}, {opacity: 1, x: 0, y: 0, clipPath: "inset(0 0 0% 0)", duration: .5, ease: "expo.out"}, g.t);
  if (g.until != null) tl.to([`#g${g.i}`, `#d${g.i}`].filter(s => document.querySelector(s)), {opacity: 0, duration: .3}, g.until);
}
if (REC) { tl.fromTo("#rec", {opacity: 0, scale: 1.2}, {opacity: 1, scale: 1, duration: .3, ease: "power4.out"}, REC.t); tl.to("#rec i", {opacity: .2, duration: .4, repeat: 5, yoyo: true, ease: "none"}, REC.t + .35); }
if (WAVE) { tl.fromTo("#wave", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .4}, WAVE.t); if (WAVE.until != null) tl.to("#wave", {opacity: 0, duration: .3}, WAVE.until); }
if (END) {
  tl.to([".ar", ".dot", ".chip", "#wave", "#rec"].filter(s => document.querySelector(s)), {opacity: 0, duration: .35}, END.t - .1);
  tl.fromTo("#endg", {opacity: 0}, {opacity: 1, duration: .6}, END.t);
  if (document.querySelector("#end img")) tl.fromTo("#end img", {opacity: 0, scale: .85}, {opacity: 1, scale: 1, duration: .8, ease: "expo.out"}, END.t + .15);
  tl.fromTo("#end .en", {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .5}, END.t + .5);
  if (document.querySelector("#end .he")) tl.fromTo("#end .he", {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .5}, END.t + .65);
}
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ar_whoosh", .1, .5)] + [cue("glass_ting", g["t"] - .05, .6) for g in G]
        if spec.get("rec"):
            sfx.append(cue("rec_beep", spec["rec"]["t"], .7))
        if end:
            sfx.append(cue("logo_hit", end["t"] + .1, .8))
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud="\n".join(h),
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .7), extra=extra)
