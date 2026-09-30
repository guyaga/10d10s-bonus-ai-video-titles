"""GRADIENT-GLASS: the SaaS / tech launch look. A frosted glass card tilts in and settles over a gradient plate, a light
glint travels its border, a shimmering NEW pill, a gradient headline, a subhead, floating glass feature chips, and a cursor
that glides to the call-to-action and clicks it (ripple + press). English by default; Hebrew runs RTL.

Spec keys. Required: clip, title.
  pill       "NEW · v4.0"          title   "Meet Aurora."          sub  "Your whole workflow, one calm workspace."
  cta        "Get early access →"   chips   ["AI summaries", "Realtime sync", "SOC 2 ready"]   (up to 4, placed around the card)
  t          card entrance (default .6);  click  time of the cursor click (default 6.4); cursor true (default)
  language   "en" | "he";  pair (Hebrew, default "secular"); Latin: Sora 800 + Manrope 500
  colors     {"grad": ["#b69cff", "#6fb8ff", "#ff9e7a"], "text": "#ffffff"}
  sfx (true), plate_vol, music, music_vol, name
"""
from styles.common import (audio_cues, cue, e, fonts, js, project_dir, res, tracks, type_pair)

CURSOR = ('<svg viewBox="0 0 32 32" width="44" height="44"><path d="M6 3l19 12.5-8.4 1.7 5.1 9.6-3.9 2-5.1-9.7L6 25z" '
          'fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/></svg>')


def build(spec, base, style="GRADIENT-GLASS"):
    tp = type_pair(spec, latin=("Sora", 800, "Manrope", 500), default_pair="secular")
    rtl = tp["rtl"]
    col = {"grad": ["#b69cff", "#6fb8ff", "#ff9e7a"], "text": "#ffffff", **spec.get("colors", {})}
    g0, g1, g2 = col["grad"]
    t0, click = spec.get("t", .6), spec.get("click", 6.4)
    chips = spec.get("chips", [])[:4]
    # chip anchor points around the card (card spans x 560-1360, y 300-780)
    spots = [(340, 330), (1400, 280), (1430, 700), (300, 760)]
    css = tp["css"] + f"""
#card{{position:absolute;left:560px;top:300px;width:800px;height:480px;border-radius:36px;background:linear-gradient(160deg,rgba(255,255,255,.16),rgba(255,255,255,.05));
  backdrop-filter:blur(26px) saturate(1.3);-webkit-backdrop-filter:blur(26px) saturate(1.3);box-shadow:0 40px 120px rgba(8,4,40,.45),inset 0 1px 0 rgba(255,255,255,.35);
  display:flex;flex-direction:column;align-items:center;justify-content:center;gap:22px;direction:{tp['dir']};transform-style:preserve-3d}}
#card::before{{content:"";position:absolute;inset:0;border-radius:36px;padding:1.5px;background:linear-gradient(135deg,rgba(255,255,255,.7),rgba(255,255,255,.08) 40%,rgba(255,255,255,.08) 60%,rgba(255,255,255,.5));
  -webkit-mask:linear-gradient(#000 0 0) content-box,linear-gradient(#000 0 0);-webkit-mask-composite:xor;mask-composite:exclude}}
#glint{{position:absolute;inset:0;border-radius:36px;overflow:hidden;pointer-events:none}}
#glint i{{position:absolute;top:-40%;left:0;width:120px;height:180%;background:linear-gradient(90deg,transparent,rgba(255,255,255,.35),transparent);transform:rotate(20deg) translateX(-400px)}}
#pill{{position:relative;padding:10px 22px;border-radius:40px;font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:24px;letter-spacing:{'0' if rtl else '.14em'};
  color:#fff;background:rgba(255,255,255,.1);border:1px solid rgba(255,255,255,.35);overflow:hidden}}
#pill b{{position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%,rgba(255,255,255,.45) 50%,transparent 70%);transform:translateX(-120%)}}
#ttl{{font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};font-size:112px;line-height:1.02;letter-spacing:{'0' if rtl else '-.035em'};text-align:center;
  background:linear-gradient(100deg,{g0},{g1} 50%,{g2});background-size:200% 100%;-webkit-background-clip:text;background-clip:text;color:transparent;padding:0 .05em .06em}}
#sub{{font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:34px;color:rgba(255,255,255,.86);text-align:center;max-width:720px}}
#cta{{position:relative;margin-top:8px;padding:20px 40px;border-radius:40px;background:#fff;color:#141024;font-family:"{tp['display']}",sans-serif;font-weight:600;font-size:30px;white-space:nowrap;box-shadow:0 12px 40px rgba(111,184,255,.35)}}
#cta .sh{{position:absolute;inset:0;border-radius:40px;overflow:hidden}}
#cta b{{position:absolute;inset:0;background:linear-gradient(100deg,transparent 30%,rgba(182,156,255,.55) 50%,transparent 70%);transform:translateX(-120%)}}
#rip{{position:absolute;left:0;top:0;width:0;height:0}}
#rip i{{position:absolute;left:-60px;top:-60px;width:120px;height:120px;border-radius:50%;border:3px solid rgba(255,255,255,.9);opacity:0}}
#cur{{position:absolute;left:0;top:0;filter:drop-shadow(0 6px 10px rgba(0,0,0,.35))}}
.chip{{position:absolute;padding:14px 24px;border-radius:22px;background:rgba(20,14,48,.46);border:1px solid rgba(255,255,255,.3);backdrop-filter:blur(16px);
  -webkit-backdrop-filter:blur(16px);font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:28px;color:#fff;white-space:nowrap;direction:{tp['dir']};
  box-shadow:0 18px 50px rgba(8,4,40,.35)}}
.chip i{{display:inline-block;width:12px;height:12px;border-radius:50%;background:linear-gradient(135deg,{g0},{g2});margin-{'left' if rtl else 'right'}:12px;vertical-align:.06em}}
"""
    chips_html = "".join(f'<div class="chip" id="k{i}" style="left:{x}px;top:{y}px"><i></i>{e(c)}</div>' for i, (c, (x, y)) in enumerate(zip(chips, spots)))
    hud = (f'<div id="card"><div id="glint"><i></i></div>'
           + (f'<div id="pill"><b></b>{e(spec["pill"])}</div>' if spec.get("pill") else "")
           + f'<div id="ttl">{e(spec["title"])}</div>'
           + (f'<div id="sub">{e(spec["sub"])}</div>' if spec.get("sub") else "")
           + (f'<div id="cta"><span class="sh"><b></b></span>{e(spec["cta"])}</div>' if spec.get("cta") else "")
           + '</div>' + chips_html
           + ('<div id="rip"><i></i><i></i></div><div id="cur">' + CURSOR + '</div>' if spec.get("cursor", True) and spec.get("cta") else ""))
    J = {"t0": t0, "click": click, "n": len(chips), "cur": bool(spec.get("cursor", True) and spec.get("cta")), "pill": bool(spec.get("pill")),
         "sub": bool(spec.get("sub")), "cta": bool(spec.get("cta"))}
    j = [f"const S = {js(J)};", r"""
gsap.set("#card", {transformPerspective: 1400});
tl.fromTo("#card", {opacity: 0, scale: .86, rotationX: 18, y: 60}, {opacity: 1, scale: 1, rotationX: 0, y: 0, duration: 1.3, ease: "expo.out"}, S.t0);
tl.fromTo("#card", {rotationY: -3}, {rotationY: 3, duration: DUR - S.t0, ease: "sine.inOut"}, S.t0);   // a breathing tilt keeps the glass alive
tl.fromTo("#glint i", {x: -400}, {x: 1100, duration: 1.4, ease: "power2.inOut"}, S.t0 + .9);
if (S.pill) { tl.fromTo("#pill", {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: .6, ease: "power3.out"}, S.t0 + .5);
              tl.fromTo("#pill b", {xPercent: -120}, {xPercent: 120, duration: 1.1, ease: "power2.inOut"}, S.t0 + 1.2); }
tl.fromTo("#ttl", {opacity: 0, y: 30, filter: "blur(12px)"}, {opacity: 1, y: 0, filter: "blur(0px)", duration: 1.0, ease: "expo.out"}, S.t0 + .7);
tl.fromTo("#ttl", {backgroundPosition: "0% 50%"}, {backgroundPosition: "100% 50%", duration: DUR - S.t0, ease: "none"}, S.t0);
if (S.sub) tl.fromTo("#sub", {opacity: 0, y: 18}, {opacity: 1, y: 0, duration: .8, ease: "power3.out"}, S.t0 + 1.1);
if (S.cta) { tl.fromTo("#cta", {opacity: 0, y: 18, scale: .96}, {opacity: 1, y: 0, scale: 1, duration: .7, ease: "back.out(1.8)"}, S.t0 + 1.4);
             tl.fromTo("#cta b", {xPercent: -120}, {xPercent: 120, duration: 1.0, ease: "power2.inOut"}, S.t0 + 2.4); }
for (let i = 0; i < S.n; i++) {
  tl.fromTo("#k" + i, {opacity: 0, y: 40, scale: .9}, {opacity: 1, y: 0, scale: 1, duration: .8, ease: "back.out(1.6)"}, S.t0 + 1.8 + i * .22);
  tl.to("#k" + i, {y: (i % 2 ? 14 : -14), duration: 2.6, ease: "sine.inOut", yoyo: true, repeat: Math.max(0, Math.ceil((DUR - S.t0 - 2.6 - i * .22) / 2.6) - 1)}, S.t0 + 2.6 + i * .22);
}
if (S.cur) {
  // the cursor enters from the lower right, glides to the CTA centre, presses it, the ripple rings out
  // measure from layout (offsets), not the animated transform, so the target is where the button settles
  const cd = document.getElementById("card"), ct = document.getElementById("cta");
  const cxp = cd.offsetLeft + ct.offsetLeft + ct.offsetWidth / 2, cyp = cd.offsetTop + ct.offsetTop + ct.offsetHeight / 2;
  tl.fromTo("#cur", {x: 1700, y: 1000, opacity: 0}, {x: 1500, y: 900, opacity: 1, duration: .4}, S.click - 2.0);
  tl.to("#cur", {x: cxp - 8, y: cyp - 6, duration: 1.3, ease: "power3.inOut"}, S.click - 1.6);
  tl.to("#cur", {scale: .82, duration: .09, yoyo: true, repeat: 1, transformOrigin: "10% 10%"}, S.click);
  tl.to("#cta", {scale: .95, duration: .09, yoyo: true, repeat: 1}, S.click);
  tl.set("#rip", {x: cxp, y: cyp}, 0);
  tl.to("#cur", {opacity: 0, y: "+=40", duration: .6, ease: "power2.in"}, S.click + 1.4);
  tl.fromTo("#rip i:nth-child(1)", {opacity: .9, scale: .2}, {opacity: 0, scale: 2.2, duration: .8, ease: "power2.out", immediateRender: false}, S.click + .05);
  tl.fromTo("#rip i:nth-child(2)", {opacity: .6, scale: .2}, {opacity: 0, scale: 3, duration: 1.1, ease: "power2.out", immediateRender: false}, S.click + .15);
}
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", t0, .3), cue("glass_ting", t0 + 1.0, .3)] + [cue("ui_pop", t0 + 1.8 + i * .22, .15) for i in range(len(chips))]
        if J["cur"]:
            sfx.append(cue("soft_click", click, .5))
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .4), extra=tp["files"])
