"""QUOTE-TESTIMONIAL: the customer-quote card of every testimonial ad. A big quote mark drops in, the quote builds word by
word IN SYNC with the speaker's own voice (word timings), the key phrase gets an accent underline as it is spoken, then the
attribution slides in: a hairline, name, role and a five-star rating that pops star by star. Hebrew or English.

Spec keys. Required: clip, words (or quote + t).
  words      [{"w": "It", "s": 0.67, "e": 0.83}, ...]  word timings (Gemini transcription / word_times.py). The quote text is
             these words in order; punctuation may be attached to a word ("better.").
  quote      "…" + t: use instead of words when there is no speech: the words then build in a stagger from t
  key        [first_word_index, last_word_index]   phrase that gets the accent underline (optional)
  person, role, stars (0-5, default 5), logo (short brand text, optional)   ("name" is the project name)
  side       "left" (default) | "right": the half of the frame the quote lives in (keep it off the face)
  ink        "dark" (default, for bright walls/windows) | "light" (for dark backgrounds; adds a soft scrim)
  language   "he" | "en";  pair (Hebrew, default "suez"); Latin: DM Serif Display + Manrope
  colors     {"accent": "#d9892b", "mark": "#b8651a"}   mark = the big quotation marks
  size       quote font px (default 72), width (default 640), top (default 250)
  sfx (true), plate_vol (default .95: the speaker's voice is the soundtrack), music, music_vol, name
"""
from styles.common import (audio_cues, cue, e, js, project_dir, res, tracks, type_pair)

QM = ('<svg viewBox="0 0 120 90" width="150" height="112"><path fill="currentColor" d="M50 4C24 12 6 32 6 58c0 16 10 28 25 28 13 0 23-10 23-23'
      ' 0-12-9-21-21-22 3-12 12-21 25-26zM114 4C88 12 70 32 70 58c0 16 10 28 25 28 13 0 23-10 23-23 0-12-9-21-21-22 3-12 12-21 25-26z"/></svg>')
STAR = ('<svg viewBox="0 0 24 24" width="38" height="38"><path d="M12 2.6l2.78 6.02 6.6.72-4.93 4.45 1.37 6.5L12 16.97l-5.82 3.32'
        ' 1.37-6.5L2.62 9.34l6.6-.72z" fill="currentColor"/></svg>')


def build(spec, base, style="QUOTE-TESTIMONIAL"):
    tp = type_pair(spec, latin=("DM Serif Display", 400, "Manrope", 500), default_pair="suez")
    rtl = tp["rtl"]
    col = {"accent": "#d9892b", "mark": "#b8651a", **spec.get("colors", {})}
    dark = spec.get("ink", "dark") == "dark"
    ink, sub = ("#1c1712", "rgba(28,23,18,.72)") if dark else ("#ffffff", "rgba(255,255,255,.8)")
    size, width, top = spec.get("size", 72), spec.get("width", 640), spec.get("top", 250)
    side = spec.get("side", "left")
    x = 120 if side == "left" else 1920 - 120 - width
    if spec.get("words"):
        W = [dict(w=w["w"], s=float(w["s"])) for w in spec["words"]]
    else:
        t0 = spec.get("t", .8)
        W = [dict(w=w, s=round(t0 + i * .16, 3)) for i, w in enumerate(spec["quote"].split())]
    k0, k1 = spec.get("key", [-1, -2])
    spans = []
    for i, w in enumerate(W):
        cls = ("w k" + (" kl" if i == k1 else "")) if k0 <= i <= k1 else "w"
        spans.append(f'<span class="{cls}" id="w{i}">{e(w["w"])}</span>')
    stars = spec.get("stars", 5)
    last = W[-1]["s"] + .5
    css = tp["css"] + f"""
#scrim{{position:absolute;inset:0;background:linear-gradient({'to right' if side == 'left' else 'to left'},rgba(0,0,0,.5),rgba(0,0,0,.18) 45%,transparent 62%);opacity:{0 if dark else 1}}}
#q{{position:absolute;left:{x}px;top:{top}px;width:{width}px;direction:{tp['dir']};text-align:{'right' if rtl else 'left'}}}
#qm{{position:absolute;{'right' if rtl else 'left'}:-4px;top:-140px;color:{col['mark']};transform-origin:50% 60%;{'transform:scaleX(-1);' if rtl else ''}}}
#txt{{position:relative;font-family:"{tp['display']}",serif;font-weight:{tp['dw']};font-size:{size}px;line-height:1.13;color:{ink};letter-spacing:{'0' if rtl else '-.005em'}}}
.w{{display:inline-block;isolation:isolate;margin-{'left' if rtl else 'right'}:.24em;opacity:.0;position:relative}}
.w.k::after{{content:"";position:absolute;{'right:-.04em;left:-.28em' if rtl else 'left:-.04em;right:-.28em'};bottom:.02em;height:.14em;background:{col['accent']};opacity:.5;z-index:-1;
  transform:scaleX(var(--u,0));transform-origin:{'100%' if rtl else '0%'} 50%}}
.w.kl::after{{{'left' if rtl else 'right'}:-.04em}}
#att{{margin-top:44px;display:flex;flex-direction:column;align-items:flex-start;gap:10px}}
#att .ln{{width:120px;height:2px;background:{col['accent']};transform-origin:{'100%' if rtl else '0%'} 50%}}
#att .nm{{font-family:"{tp['body']}",sans-serif;font-weight:700;font-size:40px;color:{ink};margin-top:12px}}
#att .rl{{font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:30px;color:{sub};{'letter-spacing:.04em;' if not rtl else ''}}}
#stars{{display:flex;gap:6px;margin-top:10px;color:{col['accent']};direction:ltr}}
#stars span{{display:block;opacity:0}}
#logo{{margin-top:18px;font-family:"{tp['body']}",sans-serif;font-weight:700;font-size:24px;letter-spacing:.28em;color:{sub};opacity:0}}
"""
    hud = ('<div id="scrim"></div>'
           f'<div id="q"><div id="qm">{QM}</div><div id="txt">{"".join(spans)}</div>'
           f'<div id="att"><i class="ln"></i><div class="nm">{e(spec.get("person", ""))}</div><div class="rl">{e(spec.get("role", ""))}</div>'
           f'<div id="stars">{"".join(f"<span>{STAR}</span>" for _ in range(stars))}</div>'
           + (f'<div id="logo">{e(spec["logo"])}</div>' if spec.get("logo") else "") + '</div></div>')
    J = {"W": [w["s"] for w in W], "k": [k0, k1], "last": last, "rtl": rtl, "stars": stars}
    j = [f"const Q = {js(J)};", r"""
tl.fromTo("#qm", {opacity: 0, scale: 1.6, rotation: -8, y: -30}, {opacity: 1, scale: 1, rotation: 0, y: 0, duration: .8, ease: "back.out(1.7)"}, Math.max(0, Q.W[0] - .45));
// each word rises in on its own spoken beat: a small lift + blur-to-sharp, never a pop
Q.W.forEach((s, i) => tl.fromTo("#w" + i, {opacity: 0, y: 26, filter: "blur(6px)"}, {opacity: 1, y: 0, filter: "blur(0px)", duration: .42, ease: "power3.out"}, s - .04));
// the key phrase underline sweeps while it is being said
if (Q.k[0] >= 0) for (let i = Q.k[0]; i <= Q.k[1]; i++) {
  const s = Q.W[i], nxt = i + 1 < Q.W.length ? Q.W[i + 1] : s + .4;
  tl.fromTo("#w" + i, {"--u": 0}, {"--u": 1, duration: Math.max(.18, nxt - s), ease: "none"}, s);
}
// a gentle settle of the whole quote so it never feels frozen
tl.fromTo("#txt", {y: 0}, {y: -8, duration: DUR, ease: "sine.inOut"}, 0);
tl.fromTo("#att .ln", {scaleX: 0}, {scaleX: 1, duration: .7, ease: "expo.out"}, Q.last);
tl.fromTo("#att .nm", {opacity: 0, x: Q.rtl ? 24 : -24}, {opacity: 1, x: 0, duration: .6, ease: "power3.out"}, Q.last + .15);
tl.fromTo("#att .rl", {opacity: 0, x: Q.rtl ? 24 : -24}, {opacity: 1, x: 0, duration: .6, ease: "power3.out"}, Q.last + .3);
for (let i = 0; i < Q.stars; i++) tl.fromTo(`#stars span:nth-child(${i + 1})`, {opacity: 0, scale: .2, rotation: -40}, {opacity: 1, scale: 1, rotation: 0, duration: .45, ease: "back.out(2.6)"}, Q.last + .55 + i * .09);
if (document.querySelector("#logo")) tl.fromTo("#logo", {opacity: 0}, {opacity: 1, duration: .6}, Q.last + 1.2);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("soft_thump", max(0, W[0]["s"] - .45), .35), cue("soft_click", last, .3)] + [cue("ui_pop", last + .55 + i * .09, .12) for i in range(stars)]
    sfx += audio_cues(spec, base, .35)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .95), extra=tp["files"])
