"""SCIFI-TARGETING: first-person targeting HUD. Corner ticks, a centre reticle, bracket boxes + ID tags locked to each
tracked target (ranges count down), a HOSTILE LOCK banner, a FIRE cue, dashed projectile arcs from a launcher to the
locked targets, hit flashes, then a TARGETS NEUTRALIZED banner (optionally bilingual).

Spec keys. Required: clip, track, targets.
  targets    [{"obj": "heavy", "label": "T-01 // HEAVY", "sub": "RANGE {range} m · ARMOR IV", "range": [140, 96],
               "lock": true, "after": "SIGNAL LOST", "t": .5, "anchor": "r"}]    lock=false: tracked but not fired on
  launcher   tracked object the arcs start from (optional; no arcs without it)
  lock       {"t": 2.6, "text": "HOSTILE LOCK · {n} TARGETS"}
  fire       {"t": 3.85, "text": "FIRE"}          impact: seconds (default fire.t + .8)
  banner     {"t": 6.2, "title": "TARGETS NEUTRALIZED", "sub": "המטרות נוטרלו", "detail": "T-01 DOWN · T-02 DOWN"}
  colors     {"hud": "#ffb547", "fg": "#fff4e2", "mute": "#d9c3a0", "alert": "#ff5046"}
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (BRK, TICKS, audio_cues, cue, e, fonts, js, project_dir, res, tracks)


def build(spec, base, style="SCIFI-TARGETING"):
    col = {"hud": "#ffb547", "fg": "#fff4e2", "mute": "#d9c3a0", "alert": "#ff5046", **spec.get("colors", {})}
    T = spec["targets"]
    lock = {"t": 2.6, "text": "HOSTILE LOCK · {n} TARGETS", **(spec.get("lock") or {})}
    fire = {"t": 3.85, "text": "FIRE", **(spec.get("fire") or {})}
    impact = spec.get("impact", fire["t"] + .8)
    banner = spec.get("banner", {"t": impact + 1.5, "title": "TARGETS NEUTRALIZED"})
    n_lock = sum(1 for x in T if x.get("lock", True))
    faces, extra = fonts("Secular One", "JetBrains Mono")
    css = faces + f"""
#root{{font-family:"Secular One",sans-serif}}
:root{{--acc:{col['hud']};--fg:{col['fg']};--mute:{col['mute']};--warn:{col['alert']};--panel:rgba(12,8,4,.78)}}
.mono{{font-family:"JetBrains Mono",monospace}}
.tick{{border-color:color-mix(in srgb,var(--acc) 70%,transparent)}}
#ret{{position:absolute;left:960px;top:540px;width:0;height:0}}
#ret .c{{position:absolute;left:-60px;top:-60px;width:120px;height:120px;border:2px solid color-mix(in srgb,var(--acc) 80%,transparent);border-radius:50%}}
#ret .h{{position:absolute;left:-90px;top:-1px;width:180px;height:2px;background:linear-gradient(90deg,var(--acc) 0 30%,transparent 30% 70%,var(--acc) 70%)}}
#ret .v{{position:absolute;top:-90px;left:-1px;height:180px;width:2px;background:linear-gradient(180deg,var(--acc) 0 30%,transparent 30% 70%,var(--acc) 70%)}}
.tgt .brk i{{border-color:var(--acc)}}
.tgt.lock .brk i{{border-color:var(--warn)}}
.tt{{padding:10px 14px;white-space:nowrap;width:max-content;height:auto}}
.tt .n{{display:block;font-size:26px;font-weight:800}}
.tt .s{{display:block;font-size:17px;letter-spacing:.08em;color:var(--mute);margin-top:2px}}
.tt.lock{{outline:2px solid var(--warn)}}
#arcs{{position:absolute;inset:0;width:1920px;height:1080px}}
.hit{{position:absolute;left:0;top:0;width:0;height:0}}
.hit i{{position:absolute;left:-2px;top:-40px;width:4px;height:80px;background:#fff;box-shadow:0 0 18px var(--acc)}}
.hit i:nth-child(1){{transform:rotate(45deg)}}.hit i:nth-child(2){{transform:rotate(-45deg)}}
.ctr{{position:absolute;left:0;right:0;margin:0 auto;width:max-content}}
#lockmsg{{bottom:190px;padding:10px 22px;font-size:30px;font-weight:800;letter-spacing:.14em;color:#ffd9d6;border:2px solid var(--warn);background:rgba(40,6,4,.82);white-space:nowrap}}
#fire{{bottom:180px;padding:10px 30px;font-size:44px;font-weight:800;letter-spacing:.3em;color:#1a0d02;background:var(--acc);white-space:nowrap}}
#banner{{position:absolute;left:0;right:0;top:420px;text-align:center}}
#banner .en{{display:inline-block;font-size:88px;font-weight:800;letter-spacing:.08em;padding:10px 40px;background:rgba(12,8,4,.8);border-top:3px solid var(--acc);border-bottom:3px solid var(--acc)}}
#banner .he{{display:block;font-size:44px;font-weight:700;margin-top:14px;text-shadow:0 2px 16px #000;direction:rtl}}
#banner .s{{display:block;font-size:20px;letter-spacing:.14em;color:var(--mute);margin-top:10px}}
"""
    h = [TICKS, '<div id="ret"><div class="c"></div><div class="h"></div><div class="v"></div></div>',
         '<svg id="arcs" viewBox="0 0 1920 1080">' + "".join(f'<path id="arc{i}" fill="none" stroke="{col["hud"]}" stroke-width="4" stroke-dasharray="14 10"/>'
                                                               for i, x in enumerate(T) if x.get("lock", True)) + "</svg>"]
    for i, x in enumerate(T):
        sub = e(x.get("sub", "")).replace("{range}", f'<b id="r{i}">{x.get("range", [0])[0]}</b>')
        h.append(f'<div id="t{i}" class="tgt" data-box="{e(x["obj"])}" data-pad="10">{BRK}</div>')
        h.append(f'<div id="l{i}" class="tt panel" data-follow="{e(x["obj"])}" data-anchor="{x.get("anchor", "r")}" data-dx="{x.get("dx", 18)}" data-dy="{x.get("dy", -20)}">'
                 f'<span class="n">{e(x["label"])}</span><span class="s mono" id="s{i}">{sub}</span></div>')
        if x.get("lock", True):
            h.append(f'<div class="hit" id="h{i}" data-follow="{e(x["obj"])}" data-anchor="c"><i></i><i></i></div>')
    h.append(f'<div id="lockmsg" class="ctr mono">{e(lock["text"].replace("{n}", str(n_lock)))}</div>')
    h.append(f'<div id="fire" class="ctr mono">{e(fire["text"])}</div>')
    if banner:
        h.append(f'<div id="banner"><span class="en">{e(banner["title"])}</span>' + (f'<span class="he">{e(banner["sub"])}</span>' if banner.get("sub") else "")
                 + (f'<span class="s mono">{e(banner["detail"])}</span>' if banner.get("detail") else "") + "</div>")
    TT = [{"i": i, "obj": x["obj"], "lock": x.get("lock", True), "range": x.get("range"), "after": x.get("after"), "t": x.get("t", .5 + .4 * i),
           "sub": x.get("sub", "")} for i, x in enumerate(T)]
    j = [f"const T = {js(TT)}, FIRE = {fire['t']}, IMPACT = {impact}, LOCK = {lock['t']}, LAUNCHER = {js(spec.get('launcher'))}, BANNER = {js(banner.get('t') if banner else None)};",
         r"""
function arc(el, a, b, u) {
  if (!el) return;
  if (!a || !b || u <= 0) { el.setAttribute("d", ""); return; }
  const x0 = (a[0] + a[2]) / 2, y0 = a[1] + 20, x1 = (b[0] + b[2]) / 2, y1 = (b[1] + b[3]) / 2;
  const cx = (x0 + x1) / 2, cy = Math.min(y0, y1) - 260;
  const P = (s) => [(1-s)*(1-s)*x0 + 2*(1-s)*s*cx + s*s*x1, (1-s)*(1-s)*y0 + 2*(1-s)*s*cy + s*s*y1];
  let d = `M${x0},${y0}`; for (let k = 1; k <= 24; k++) { const p = P(u * k / 24); d += ` L${p[0]},${p[1]}`; }
  el.setAttribute("d", d);
}
window.onPlace = (t) => {
  const u = t < FIRE ? 0 : t < IMPACT ? (t - FIRE) / (IMPACT - FIRE) : (t < IMPACT + .5 ? 1 : 0);
  for (const x of T) {
    if (x.range) { const el = document.getElementById("r" + x.i); if (el) el.textContent = Math.round(x.range[0] + (x.range[1] - x.range[0]) * Math.min(1, t / FIRE)); }
    if (x.after && t > IMPACT + .4) { const s = document.getElementById("s" + x.i); if (s.textContent !== x.after) s.textContent = x.after; }
    if (!x.lock) continue;
    const on = t > LOCK && t < IMPACT;
    document.getElementById("t" + x.i).classList.toggle("lock", on);
    document.getElementById("l" + x.i).classList.toggle("lock", on);
    if (LAUNCHER) arc(document.getElementById("arc" + x.i), boxAt(LAUNCHER, t), boxAt(x.obj, Math.min(t, IMPACT)), u);
  }
};
tl.fromTo(".tick", {opacity:0, scale:1.5}, {opacity:1, scale:1, duration:.4, stagger:.05}, .05);
tl.fromTo("#ret", {opacity:0, scale:2, rotation:-45}, {opacity:1, scale:1, rotation:0, duration:.5, ease:"expo.out"}, .2);
for (const x of T) {
  tl.fromTo(`#t${x.i} .brk`, {opacity:0, scale:1.5}, {opacity:1, scale:1, duration:.35, ease:"power3.out"}, x.t);
  tl.fromTo(`#l${x.i}`, {opacity:0, y:10}, {opacity:1, y:0, duration:.35}, x.t + .15);
  if (x.lock) tl.to([`#t${x.i}`, `#l${x.i}`], {opacity:0, duration:.3}, IMPACT + .2);
  else tl.to([`#t${x.i}`, `#l${x.i}`], {opacity:0, duration:.3}, BANNER ? BANNER - .1 : IMPACT + 1.4);
}
tl.fromTo("#lockmsg", {opacity:0, scale:1.2}, {opacity:1, scale:1, duration:.25, ease:"power4.out"}, LOCK);
tl.to("#lockmsg", {opacity:0, duration:.15}, FIRE - .1);
tl.fromTo("#fire", {opacity:0, scale:1.4}, {opacity:1, scale:1, duration:.15, ease:"power4.out"}, FIRE - .05);
tl.to("#fire", {opacity:0, duration:.3}, IMPACT);
if (document.querySelector(".hit")) { tl.fromTo(".hit i", {opacity:0, scaleY:.2}, {opacity:1, scaleY:1.3, duration:.18, ease:"power4.out"}, IMPACT); tl.to(".hit i", {opacity:0, duration:.4}, IMPACT + .35); }
tl.to("#ret", {opacity:0, duration:.3}, IMPACT + .2);
if (BANNER != null) {
  tl.fromTo("#banner .en", {opacity:0, scaleX:1.3}, {opacity:1, scaleX:1, duration:.5, ease:"expo.out"}, BANNER);
  if (document.querySelector("#banner .he")) tl.fromTo("#banner .he", {opacity:0, y:14}, {opacity:1, y:0, duration:.4}, BANNER + .25);
  if (document.querySelector("#banner .s")) tl.fromTo("#banner .s", {opacity:0}, {opacity:1, duration:.4}, BANNER + .4);
}
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("hud_boot", .05, .5), cue("scan_beeps", .5, .5), cue("lock_tone", lock["t"], .7), cue("launch", fire["t"] - .05, .5),
               cue("hit_confirm", impact + .05, .8)] + ([cue("stinger", banner["t"] - .05, .8)] if banner else [])
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud="\n".join(h),
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .85), extra=extra)
