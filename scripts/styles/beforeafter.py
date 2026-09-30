"""BEFORE-AFTER-SPLIT: the renovation / retouch / product-upgrade comparison. Two takes of the SAME camera move (the before
plate and the after clip) are stacked; a divider with a round handle sweeps across revealing the after, swings back, and
settles on a split. Big label chips name each side, a bottom stat bar lands at the end. The after clip rides in the kit's
second video slot (the matte layer), masked with a clip-path, so nothing else in the kit changes.

Make the pair with Kling/Seedance: one start frame (text_to_image), its "before" edit (image_to_image, same camera), then
image_to_video on BOTH with an identical camera-move prompt.

Spec keys. Required: clip (the BEFORE plate), after (the AFTER clip).
  labels     {"before": "לפני", "after": "אחרי"}
  after_side "start" (default: the after reveals from the reading-start side, i.e. right in Hebrew, left in English) | "end"
  moves      [[t, pos], ...]  divider keyframes, pos 0..1 of the frame width measured from the after side
             (default [[0.9, 0], [2.9, .78], [4.6, .3], [6.0, .5]]). Two generated takes drift apart over time: keep the
             split moves early and end on 1.0 (full AFTER) if the seam starts to show.
  NOTE       write currency in words for Hebrew (ש״ח): Suez One / Secular One draw ₪ as a stylised "שח"; write ש״ח
  stat       "שיפוץ מלא · 42 ימי עבודה · 186,000 ש״ח"  bottom bar text (optional), stat_t (default 6.6)
  language   "he" | "en";  pair (Hebrew, default "karantina": Karantina labels + Secular One stat); Latin: Oswald + Manrope
  colors     {"accent": "#ffd23f"}
  sfx (true), plate_vol, music, music_vol, name
"""
import subprocess

from styles.common import (audio_cues, cue, e, js, project_dir, res, tracks, type_pair)
import paths


def webm(src, name):
    out = paths.root() / "mattes" / f"{name}_after.webm"
    out.parent.mkdir(parents=True, exist_ok=True)
    if not out.exists() or out.stat().st_mtime < src.stat().st_mtime:
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", str(src), "-an", "-c:v", "libvpx-vp9", "-b:v", "0", "-crf", "28",
                        "-row-mt", "1", "-deadline", "good", "-cpu-used", "4", "-pix_fmt", "yuv420p", str(out)], check=True)
    return out


def build(spec, base, style="BEFORE-AFTER-SPLIT"):
    tp = type_pair(spec, latin=("Oswald", 700, "Manrope", 500), default_pair="karantina")
    rtl = tp["rtl"]
    col = {"accent": "#ffd23f", **spec.get("colors", {})}
    lab = {"before": "לפני" if rtl else "BEFORE", "after": "אחרי" if rtl else "AFTER", **spec.get("labels", {})}
    # the after side: reading start (right in Hebrew, left in English) unless told otherwise
    start_is_right = rtl if spec.get("after_side", "start") == "start" else not rtl
    moves = spec.get("moves", [[0.9, 0], [2.9, .78], [4.6, .3], [6.0, .5]])
    name = spec.get("name", style.lower())
    after = webm(res(base, spec["after"]), name)
    css = tp["css"] + f"""
#matte{{clip-path:inset(0 0 0 0)}}
#div{{position:absolute;top:0;bottom:0;left:0;width:0}}
#div .ln{{position:absolute;top:0;bottom:0;left:-2px;width:4px;background:#fff;box-shadow:0 0 18px rgba(0,0,0,.45),0 0 2px rgba(0,0,0,.6)}}
#div .hd{{position:absolute;left:-44px;top:496px;width:88px;height:88px;border-radius:50%;background:rgba(255,255,255,.96);box-shadow:0 8px 30px rgba(0,0,0,.35);
  display:flex;align-items:center;justify-content:center;gap:10px}}
#div .hd i{{width:0;height:0;border-top:11px solid transparent;border-bottom:11px solid transparent}}
#div .hd .a{{border-right:14px solid #111}} #div .hd .b{{border-left:14px solid #111}}
.chip{{position:absolute;top:80px;padding:10px 30px 14px;background:rgba(10,10,12,.62);border:1px solid rgba(255,255,255,.2);border-radius:14px;
  font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};font-size:84px;line-height:1;color:#fff;letter-spacing:{'0' if rtl else '.04em'};backdrop-filter:blur(6px)}}
.chip.after{{background:{col['accent']};color:#111;border-color:transparent}}
#cb{{{'right' if not start_is_right else 'left'}:80px}} #ca{{{'right' if start_is_right else 'left'}:80px}}
#stat{{position:absolute;left:50%;bottom:74px;display:flex;align-items:center;gap:22px;padding:18px 34px;
  background:rgba(10,10,12,.72);border-radius:60px;border:1px solid rgba(255,255,255,.18);backdrop-filter:blur(8px);white-space:nowrap;
  font-family:"{tp['body']}",sans-serif;font-weight:{tp['bw']};font-size:36px;color:#fff;direction:{tp['dir']}}}
#stat i{{width:14px;height:14px;border-radius:50%;background:{col['accent']};flex:none}}
"""
    hud_top = (f'<div id="div"><i class="ln"></i><div class="hd"><i class="a"></i><i class="b"></i></div></div>'
               f'<div class="chip" id="cb">{e(lab["before"])}</div><div class="chip after" id="ca">{e(lab["after"])}</div>'
               + (f'<div id="stat"><i></i><span>{e(spec["stat"])}</span></div>' if spec.get("stat") else ""))
    hud = "<!--MATTE-->" + hud_top
    J = {"moves": moves, "right": start_is_right, "stat": bool(spec.get("stat")), "st": spec.get("stat_t", 6.6)}
    j = [f"const B = {js(J)};", r"""
// the reveal position p (0..1 from the after side) drives the mask, the divider and the handle, every frame
const kf = B.moves;
const ease = (u) => u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2;
function posAt(t) {
  if (t <= kf[0][0]) return kf[0][1];
  for (let i = 1; i < kf.length; i++) if (t <= kf[i][0]) {
    const [t0, p0] = kf[i - 1], [t1, p1] = kf[i], u = ease((t - t0) / (t1 - t0));
    return p0 + (p1 - p0) * u;
  }
  return kf[kf.length - 1][1];
}
window.onPlace = (t) => {
  const p = posAt(t), W = 1920, x = B.right ? W * (1 - p) : W * p;
  const m = document.getElementById("matte");
  // after shows on its side of the divider
  const clip = B.right ? `inset(0 0 0 ${x.toFixed(1)}px)` : `inset(0 ${(W - x).toFixed(1)}px 0 0)`;
  if (m && m.style.clipPath !== clip) m.style.clipPath = clip;
  const d = document.getElementById("div"); d.style.transform = `translateX(${x.toFixed(1)}px)`;
  d.style.opacity = (p > .002 && p < .998) ? 1 : 0;
};
tl.fromTo("#cb", {opacity: 0, y: -20}, {opacity: 1, y: 0, duration: .6, ease: "back.out(1.8)"}, .3);
tl.fromTo("#ca", {opacity: 0, y: -20, scale: .9}, {opacity: 1, y: 0, scale: 1, duration: .6, ease: "back.out(2.2)"}, kf[1][0] - 1.2);
tl.fromTo("#div .hd", {scale: 0}, {scale: 1, duration: .5, ease: "back.out(2.4)"}, kf[0][0] + .1);
for (let i = 1; i < kf.length; i++) tl.fromTo("#div .hd", {scale: 1.15}, {scale: 1, duration: .5, ease: "power2.out"}, kf[i][0] - .05);
const lk = kf[kf.length - 1];
if (lk[1] >= .99) tl.to("#cb", {opacity: 0, y: -12, duration: .45, ease: "power2.in"}, lk[0] - .4);
if (B.stat) { tl.set("#stat", {xPercent: -50}, 0); tl.fromTo("#stat", {opacity: 0, y: 30}, {opacity: 1, y: 0, xPercent: -50, duration: .7, ease: "power3.out"}, B.st); }
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_pop", .3, .25)] + [cue("ar_whoosh", moves[i - 1][0] + .1, .35) for i in range(1, len(moves))]
        if spec.get("stat"):
            sfx.append(cue("chime", spec.get("stat_t", 6.6), .22))
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .6), extra={**tp["files"], "matte.webm": after})
