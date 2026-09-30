"""PODCAST-TAGS: the video-podcast package. Each host gets a name tag that rides them (tracked); the active speaker's
tag lights up with a live equalizer driven by the real audio, the other dims. An episode chip sits top corner, topic
chapters swap in a lower strip, and a thin waveform bar across the bottom follows the audio. Hebrew mirrors it.

Spec keys. Required: clip, track, hosts.
  hosts     [{"follow": "host_left", "anchor": "b", "dx": 0, "dy": -40, "name": "מאיה", "role": "מגישה"}]
  talk      [{"host": 0, "t": 0, "until": 5.0}, ...]   who is speaking when (drives highlight + equalizer)
  episode   {"no": "042", "title": "...", "t": .4}
  topics    [{"text": "...", "t": 1.0}]                 lower strip, each replaces the previous
  audio     path of the file whose loudness drives the meters (default: the clip's own audio)
  language  "he" | "en";  pair (Hebrew default "suez": Suez One names + Secular One labels)
  colors    {"panel": "rgba(14,12,10,.72)", "accent": "#ffb13b", "text": "#ffffff", "sub": "#d6ccc0"}
  sfx (true), music, music_vol, plate_vol, name
"""
import subprocess

import paths
from styles.common import (JS_UTIL, audio_cues, cue, e, envelope, js, project_dir, res, tracks, type_pair)

NBAR = 5


def build(spec, base, style="PODCAST-TAGS"):
    tp = type_pair(spec, latin=("Manrope", 700, "Manrope", 500), default_pair="suez")
    rtl = tp["rtl"]
    col = {"panel": "rgba(14,12,10,.82)", "accent": "#ffb13b", "text": "#ffffff", "sub": "#ece4da", **spec.get("colors", {})}
    D, B = tp["display"], tp["body"]
    clip = res(base, spec["clip"])
    src = res(base, spec["audio"]) if spec.get("audio") else clip
    wav = paths.root() / "tmp" / (spec.get("name", "podcast") + "_env.wav")
    wav.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-vn", "-ac", "1", "-ar", "22050", str(wav)], check=True)
    env = envelope(wav)
    h = []
    for i, ho in enumerate(spec["hosts"]):
        eq = "".join("<i></i>" for _ in range(NBAR))
        h.append(f'<div class="hg" data-follow="{e(ho["follow"])}" data-anchor="{ho.get("anchor", "b")}" data-dx="{ho.get("dx", 0)}" data-dy="{ho.get("dy", -40)}">'
                 f'<div class="tg" id="h{i}"><div class="eq" id="eq{i}">{eq}</div><div><div class="nm">{e(ho["name"])}</div>'
                 f'<div class="rl">{e(ho.get("role", ""))}</div></div></div></div>')
    ep = spec.get("episode")
    if ep:
        h.append(f'<div id="ep"><span class="no">EP {e(ep["no"])}</span><span class="et">{e(ep.get("title", ""))}</span><span class="rec"><i></i>REC</span></div>')
    tops = spec.get("topics", [])
    if tops:
        h.append('<div id="tp"><div class="tk">' + ("נושא" if rtl else "TOPIC") + '</div><div class="tw">'
                 + "".join(f'<div class="tx" id="tp{i}">{e(x["text"])}</div>' for i, x in enumerate(tops)) + '</div></div>')
    h.append('<div id="wave">' + "".join("<i></i>" for _ in range(96)) + '</div>')
    css = tp["css"] + f"""
.hg{{position:absolute;left:0;top:0;width:0;height:0}}
.tg{{position:absolute;left:0;top:0;display:flex;align-items:center;gap:16px;padding:14px 24px 14px 18px;
  background:{col['panel']};backdrop-filter:blur(12px);border-radius:16px;border:1px solid rgba(255,255,255,.12);white-space:nowrap;direction:{tp['dir']};
  box-shadow:0 14px 34px rgba(0,0,0,.35)}}
.eq{{display:flex;align-items:flex-end;gap:4px;height:40px;direction:ltr}}
.eq i{{width:6px;height:40px;border-radius:3px;background:{col['accent']};transform-origin:50% 100%;display:block}}
.nm{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:40px;color:{col['text']};line-height:1.2}}
.rl{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:22px;color:{col['sub']};letter-spacing:{'0' if rtl else '.12em'}}}
#ep{{position:absolute;top:56px;{'right' if rtl else 'left'}:70px;display:flex;align-items:center;gap:0;direction:{tp['dir']};box-shadow:0 12px 30px rgba(0,0,0,.3)}}
#ep .no{{background:{col['accent']};color:#1a1208;font-family:"Manrope",sans-serif;font-weight:700;font-size:26px;padding:10px 18px;letter-spacing:.08em;direction:ltr}}
#ep .et{{background:{col['panel']};color:#fff;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:30px;padding:8px 22px}}
#ep .rec{{display:flex;align-items:center;gap:8px;background:rgba(0,0,0,.55);color:#fff;font-family:"Manrope",sans-serif;font-weight:700;font-size:20px;padding:13px 16px;direction:ltr}}
#ep .rec i{{width:12px;height:12px;border-radius:50%;background:#ff3b30;display:block}}
#tp{{position:absolute;bottom:92px;left:50%;display:flex;align-items:stretch;direction:{tp['dir']};box-shadow:0 14px 34px rgba(0,0,0,.35)}}
#tp .tk{{background:{col['accent']};color:#1a1208;font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:24px;padding:10px 18px;display:flex;align-items:center;
  letter-spacing:{'0' if rtl else '.16em'}}}
#tp .tw{{position:relative;background:{col['panel']};overflow:hidden;display:grid}}
#tp .tx{{grid-area:1/1;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:34px;color:#fff;padding:8px 28px;white-space:nowrap;line-height:1.3}}
#wave{{position:absolute;left:120px;right:120px;bottom:40px;height:30px;display:flex;align-items:center;gap:6px}}
#wave i{{flex:1;height:30px;border-radius:3px;background:rgba(255,255,255,.55);transform-origin:50% 50%;display:block}}
"""
    ocss, ofiles = "", {}
    if rtl:   # EP number / REC are Latin numerals in both languages
        from styles.common import fonts
        ocss, ofiles = fonts("Manrope")
    css = ocss + css
    J = {"env": env, "fps": 24, "talk": spec.get("talk", []), "n": len(spec["hosts"]), "ep": ep and ep.get("t", .4),
         "tops": [x["t"] for x in tops], "hosts_t": spec.get("hosts_t", .3)}
    j = [JS_UTIL, f"const J = {js(J)};", r"""
const $$ = (id) => document.getElementById(id);
const envAt = (t) => { const i = Math.max(0, Math.min(J.env.length - 1, Math.round(t * J.fps))); return J.env[i] || 0; };
const WAVE = [...document.querySelectorAll("#wave i")];
const who = (t) => { for (const s of J.talk) if (t >= s.t && t < s.until) return s.host; return -1; };
window.onPlace = (t) => {
  const a = who(t), lv = envAt(t);
  for (let i = 0; i < J.n; i++) {
    const on = i === a;
    $$("h" + i).style.opacity = t < J.hosts_t ? 0 : (on ? 1 : .55);
    $$("h" + i).style.scale = on ? 1.04 : .96;
    [...$$("eq" + i).children].forEach((b, k) => {
      const wob = .55 + .45 * Math.sin(t * 17 + k * 1.9 + i);
      b.style.transform = `scaleY(${on ? Math.max(.12, Math.min(1, lv * 1.3 * wob)) : .12})`;
    });
  }
  WAVE.forEach((b, k) => {
    const back = envAt(t - (WAVE.length - k) * 0.05);
    b.style.transform = `scaleY(${Math.max(.08, Math.min(1, back * 1.2))})`;
  });
};
tl.set(".tg", {xPercent: -50, yPercent: -100}, 0);
tl.fromTo(".tg", {y: 20}, {y: 0, duration: .6, ease: "expo.out", stagger: .12}, J.hosts_t);
if (J.ep != null) {
  tl.fromTo("#ep", {opacity: 0, y: -24}, {opacity: 1, y: 0, duration: .55, ease: "expo.out"}, J.ep);
  tl.to("#ep .rec i", {opacity: .15, duration: .5, yoyo: true, repeat: 20, ease: "sine.inOut"}, J.ep + .5);
}
J.tops.forEach((t0, i) => {
  if (i === 0) tl.fromTo("#tp", {opacity: 0, y: 24, xPercent: -50}, {opacity: 1, y: 0, xPercent: -50, duration: .55, ease: "expo.out"}, t0 - .1);
  tl.fromTo(`#tp${i}`, {yPercent: 110, opacity: 0}, {yPercent: 0, opacity: 1, duration: .5, ease: "expo.out"}, t0);
  if (i > 0) tl.to(`#tp${i - 1}`, {yPercent: -110, opacity: 0, duration: .35, ease: "power2.in"}, t0 - .3);
});
tl.fromTo("#wave", {opacity: 0}, {opacity: 1, duration: .8}, .2);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("rec_beep", ep.get("t", .4) if ep else .4, .35)] + [cue("ui_whoosh", t0, .3) for t0 in J["tops"]]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=clip, track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .9), extra={**tp["files"], **ofiles})
