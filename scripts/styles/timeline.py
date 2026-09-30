"""TIMELINE-HISTORY: the documentary history timeline. A rule with minor ticks draws across the lower third, a playhead
travels it, each year node pops as the playhead arrives, a big year counts up (odometer) to the node's date and a caption
rises above the node. The footage starts in an archival sepia grade and warms into full colour as the timeline reaches
the present. Hebrew timelines run right-to-left (earliest on the right); English left-to-right.

Spec keys. Required: clip, events.
  events     [{"year": 1104, "text": "הצלבנים כובשים את עכו", "t": 1.2}, ...]   in chronological order
  archival   true (default): sepia/grain grade that fades out as the playhead nears the last event
  y          timeline y in px (default 850);  margin (default 170)
  big        {"side": "start" | "end", "y": 430}   where the big counting year sits (default: the reading start side)
  language   "he" | "en";  pair (Hebrew, default "suez"); Latin: DM Serif Display + Manrope
  colors     {"accent": "#f2c46d", "line": "rgba(255,255,255,.75)"}
  sfx (true), plate_vol, music, music_vol, name
"""
from styles.common import (audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def build(spec, base, style="TIMELINE-HISTORY"):
    tp = type_pair(spec, latin=("DM Serif Display", 400, "Manrope", 500), default_pair="suez")
    rtl = tp["rtl"]
    col = {"accent": "#f2c46d", "line": "rgba(255,255,255,.78)", **spec.get("colors", {})}
    E = spec["events"]
    y, mg = spec.get("y", 850), spec.get("margin", 170)
    n = len(E)
    xs = [round(mg + i * (1920 - 2 * mg) / (n - 1)) for i in range(n)]
    if rtl:
        xs = [1920 - x for x in xs]          # earliest on the right
    big = {"side": "start", "y": 430, **spec.get("big", {})}
    big_left = (big["side"] == "start") != rtl   # start side = right in Hebrew
    css = tp["css"] + f"""
#arch{{position:absolute;inset:0;backdrop-filter:sepia(.85) contrast(1.08) brightness(.92) saturate(.8);-webkit-backdrop-filter:sepia(.85) contrast(1.08) brightness(.92) saturate(.8)}}
#vig{{position:absolute;inset:0;background:radial-gradient(ellipse 80% 70% at 50% 45%,transparent 55%,rgba(20,12,4,.55));}}
#band{{position:absolute;left:0;right:0;top:{y - 520}px;height:{1080 - y + 520}px;background:linear-gradient(transparent,rgba(8,6,4,.5) 35%,rgba(8,6,4,.72) 70%,rgba(8,6,4,.82))}}
#rule{{position:absolute;left:{mg - 40}px;right:{mg - 40}px;top:{y}px;height:2px;background:{col['line']};transform-origin:{'100%' if rtl else '0%'} 50%}}
#ticks{{position:absolute;left:{mg - 40}px;right:{mg - 40}px;top:{y + 8}px;height:10px;
  background:repeating-linear-gradient(90deg,rgba(255,255,255,.45) 0 1px,transparent 1px 38px);transform-origin:{'100%' if rtl else '0%'} 50%}}
.nd{{position:absolute;top:{y}px;width:0;height:0}}
.nd .dot{{position:absolute;left:-9px;top:-8px;width:18px;height:18px;border-radius:50%;background:#1a140c;border:3px solid {col['accent']}}}
.nd.on .dot{{background:{col['accent']}}}
.nd .yr{{position:absolute;top:30px;left:-100px;width:200px;text-align:center;font-family:"{tp['display']}",serif;font-size:36px;color:#fff;
  font-variant-numeric:tabular-nums;text-shadow:0 2px 12px rgba(0,0,0,.7)}}
.nd .cp{{position:absolute;bottom:34px;left:-170px;width:340px;text-align:center;font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};
  font-size:30px;line-height:1.25;color:#fff;direction:{tp['dir']};text-shadow:0 2px 14px rgba(0,0,0,.8)}}
.nd .stem{{position:absolute;left:-1px;bottom:12px;width:2px;height:18px;background:{col['accent']};transform-origin:50% 100%}}
#ph{{position:absolute;top:{y}px;left:0;width:0;height:0}}
#ph i{{position:absolute;left:-16px;top:-15px;width:32px;height:32px;border-radius:50%;border:2px solid #fff;box-shadow:0 0 18px rgba(255,255,255,.6)}}
#big{{position:absolute;top:{big['y']}px;{'left' if big_left else 'right'}:{mg - 40}px;font-family:"{tp['display']}",serif;font-weight:{tp['dw']};
  font-size:210px;line-height:1;color:#fff;font-variant-numeric:tabular-nums;text-shadow:0 10px 60px rgba(0,0,0,.45);letter-spacing:-.01em}}
#big small{{display:block;font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:30px;letter-spacing:{'0' if rtl else '.2em'};
  color:#fff;line-height:1.45;padding-bottom:6px;margin-top:34px;padding-top:14px;border-top:3px solid {col['accent']};width:max-content;direction:{tp['dir']};{'margin-left:auto;' if not big_left else ''}}}
"""
    nodes = ""
    for i, (ev, x) in enumerate(zip(E, xs)):
        nodes += (f'<div class="nd" id="n{i}" style="left:{x}px"><i class="stem"></i><div class="cp">{e(ev["text"])}</div>'
                  f'<i class="dot"></i><div class="yr">{ev["year"]}</div></div>')
    arch = spec.get("archival", True)
    hud = (('<div id="arch"></div><div id="vig"></div>' if arch else "") + '<div id="band"></div><div id="rule"></div><div id="ticks"></div>'
           + nodes + f'<div id="ph"><i></i></div><div id="big"><span id="bigy">{E[0]["year"]}</span><small id="bigl">{e(E[0]["text"])}</small></div>')
    J = {"E": [{"y": ev["year"], "t": ev["t"], "x": x, "text": ev["text"]} for ev, x in zip(E, xs)], "arch": arch}
    j = [f"const T = {js(J)};", r"""
const N = T.E.length, x0 = T.E[0].x;
tl.fromTo("#band", {opacity: 0}, {opacity: 1, duration: .8}, 0);
tl.fromTo("#rule", {scaleX: 0}, {scaleX: 1, duration: 1.1, ease: "power3.inOut"}, .15);
tl.fromTo("#ticks", {scaleX: 0}, {scaleX: 1, duration: 1.3, ease: "power3.inOut"}, .25);
tl.fromTo("#big", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .7, ease: "power3.out"}, T.E[0].t - .2);
// the playhead eases node to node; each node pops on arrival, its caption rises, the previous caption dims
T.E.forEach((ev, i) => {
  if (i > 0) tl.to("#ph", {x: ev.x, duration: .9, ease: "power2.inOut"}, ev.t - .9);
  else tl.fromTo("#ph", {x: ev.x, opacity: 0}, {x: ev.x, opacity: 1, duration: .4}, ev.t - .4);
  tl.fromTo(`#n${i} .dot`, {scale: 0}, {scale: 1, duration: .45, ease: "back.out(3)"}, ev.t);
  tl.set(`#n${i}`, {className: "nd on"}, ev.t);
  tl.fromTo(`#n${i} .yr`, {opacity: 0, y: -8}, {opacity: 1, y: 0, duration: .4, ease: "power3.out"}, ev.t + .05);
  tl.fromTo(`#n${i} .stem`, {scaleY: 0}, {scaleY: 1, duration: .3, ease: "power2.out"}, ev.t + .1);
  tl.fromTo(`#n${i} .cp`, {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, ev.t + .15);
  if (i < N - 1) tl.to(`#n${i} .cp`, {opacity: 0, y: -10, duration: .4, ease: "power2.in"}, T.E[i + 1].t - .5);
});
// the big year: an odometer between node dates while the playhead travels, the label swaps on arrival
window.onPlace = (t) => {
  let yv = T.E[0].y, lab = T.E[0].text;
  for (let i = 0; i < N; i++) {
    const ev = T.E[i];
    if (t >= ev.t) { yv = ev.y; lab = ev.text; }
    else if (i > 0 && t >= ev.t - .9) { const u = (t - (ev.t - .9)) / .9, w = u < .5 ? 2 * u * u : 1 - Math.pow(-2 * u + 2, 2) / 2; yv = Math.round(T.E[i - 1].y + (ev.y - T.E[i - 1].y) * w); break; }
    else break;
  }
  const a = document.getElementById("bigy"), b = document.getElementById("bigl");
  if (a.textContent !== String(yv)) a.textContent = String(yv);
  if (b.textContent !== lab) b.textContent = lab;
  // archival grade: full sepia until the second-to-last event, then it warms into full colour for the present
  if (T.arch) {
    const s = T.E[N - 2].t, f = T.E[N - 1].t, u = Math.max(0, Math.min(1, (t - s) / (f - s)));
    document.getElementById("arch").style.opacity = String(1 - u);
    document.getElementById("vig").style.opacity = String(1 - .7 * u);
  }
};
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", .15, .22)] + [cue("soft_tick", ev["t"], .4) for ev in E] + [cue("chime", E[-1]["t"], .25)]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .8), extra=tp["files"])
