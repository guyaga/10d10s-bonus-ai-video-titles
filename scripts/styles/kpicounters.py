"""KPI-COUNTERS: a results dashboard. Frosted tiles cascade in; in each a caption rises, a big number counts up
(prefix / suffix / decimals, thousands separators), a delta chip pops with an arrow, and a sparkline draws under it with
a glowing end dot. A thin progress rule sweeps across each tile as it counts. Numbers stay LTR in Hebrew.

Spec keys. Required: clip, tiles.
  tiles     [{"label": "ACTIVE USERS", "value": 2.4, "decimals": 1, "prefix": "", "suffix": "M", "delta": "+38%",
              "down": false, "spark": [3, 4, 4, 6, 7, 9, 12], "t": 1.0}]
  layout    {"side": "L|R", "cols": 1, "top": 150, "w": 560, "gap": 22}   a column (cols 1) or a grid (cols 2)
  heading   {"text": "Q3 · RESULTS", "t": .6}   optional small heading above the tiles
  until     time all tiles leave (optional)
  language  "he" | "en";  pair (Hebrew default "secular"); Latin default Space Grotesk 700 + Space Grotesk 500
  colors    {"card": "rgba(8,11,16,.76)", "text": "#ffffff", "sub": "#d2d9e1", "up": "#3ddc84", "down": "#ff5a5a", "accent": "#7cc8ff"}
  sfx (true), music, music_vol, plate_vol, name
"""
from styles.common import (JS_UTIL, audio_cues, cue, e, js, project_dir, res, tracks, type_pair)

SW, SH = 200, 56


def build(spec, base, style="KPI-COUNTERS"):
    tp = type_pair(spec, latin=("Space Grotesk", 700, "Space Grotesk", 500), default_pair="secular")
    rtl = tp["rtl"]
    col = {"card": "rgba(8,11,16,.76)", "text": "#ffffff", "sub": "#d2d9e1", "up": "#3ddc84", "down": "#ff5a5a", "accent": "#7cc8ff", **spec.get("colors", {})}
    D, B = tp["display"], tp["body"]
    L = {"side": "L", "cols": 1, "top": 150, "w": 560, "gap": 22, **spec.get("layout", {})}
    tiles = spec["tiles"]
    items = []
    for i, k in enumerate(tiles):
        sp = k.get("spark", [])
        path = ""
        if len(sp) > 1:
            lo, hi = min(sp), max(sp)
            pts = [(SW * n / (len(sp) - 1), SH - (SH - 8) * (v - lo) / ((hi - lo) or 1) - 4) for n, v in enumerate(sp)]
            path = "M" + " L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
            ex, ey = pts[-1]
        dn = k.get("down", False)
        spark = (f'<svg class="sp" width="{SW}" height="{SH}" viewBox="0 0 {SW} {SH}" overflow="visible"><path class="spl" d="{path}" fill="none" '
                 f'stroke="{col["down"] if dn else col["up"]}" stroke-width="3.5" stroke-linecap="round" stroke-linejoin="round" pathLength="1" stroke-dasharray="1" stroke-dashoffset="1"/>'
                 f'<circle class="spd" cx="{ex:.1f}" cy="{ey:.1f}" r="6" fill="{col["down"] if dn else col["up"]}"/></svg>') if path else ""
        arrow = "▼" if dn else "▲"
        items.append(f'<div class="kt" id="k{i}"><div class="kl">{e(k["label"])}</div>'
                     f'<div class="kr"><div class="kv"><span>{e(k.get("prefix", ""))}</span><span id="kn{i}">0</span><span class="sf">{e(k.get("suffix", ""))}</span></div>'
                     f'{spark}</div><div class="kd {"dn" if dn else "up"}">{arrow} {e(k.get("delta", ""))}</div><i class="pr"></i></div>')
    side = "right" if L["side"] == "R" else "left"
    hd = spec.get("heading")
    head = f'<div id="kh">{e(hd["text"])}</div>' if hd else ""
    h = [f'<div id="kpi" style="{side}:96px;top:{L["top"]}px;width:{L["w"] * L["cols"] + L["gap"] * (L["cols"] - 1)}px">{head}'
         f'<div class="grid">{"".join(items)}</div></div>']
    css = tp["css"] + f"""
#kpi{{position:absolute;direction:{tp['dir']}}}
#kh{{display:inline-block;background:rgba(8,11,16,.82);padding:8px 16px;border-radius:8px;font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:22px;letter-spacing:{'0' if rtl else '.3em'};color:{col['accent']};margin-bottom:16px}}
.grid{{display:grid;grid-template-columns:repeat({L['cols']},{L['w']}px);gap:{L['gap']}px}}
.kt{{position:relative;overflow:hidden;background:{col['card']};backdrop-filter:blur(16px) saturate(1.25);border:1px solid rgba(255,255,255,.16);
  border-radius:18px;padding:22px 28px 24px;box-shadow:0 20px 50px rgba(0,0,0,.28)}}
.kl{{font-family:"{B}",sans-serif;font-weight:{tp['bw']};font-size:20px;letter-spacing:{'0' if rtl else '.22em'};color:{col['sub']}}}
.kr{{display:flex;align-items:flex-end;justify-content:space-between;gap:18px;margin-top:14px;direction:ltr}}
.kv{{font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:84px;line-height:1.12;color:{col['text']};font-variant-numeric:tabular-nums;letter-spacing:-.02em;white-space:nowrap}}
.kv .sf{{font-size:52px;margin-left:4px;color:{col['accent']}}}
.sp{{flex:none;margin-bottom:10px}}
.spd{{transform-box:fill-box;transform-origin:center}}
.kd{{display:inline-block;margin-top:10px;padding:4px 12px;border-radius:999px;font-family:"{D}",sans-serif;font-weight:{tp['dw']};font-size:22px;direction:ltr}}
.kd.up{{background:color-mix(in srgb,{col['up']} 22%,transparent);color:{col['up']}}}
.kd.dn{{background:color-mix(in srgb,{col['down']} 22%,transparent);color:{col['down']}}}
.pr{{position:absolute;left:0;right:0;bottom:0;height:3px;background:{col['accent']};transform-origin:{'100%' if rtl else '0'} 50%;display:block}}
"""
    J = {"k": [{"t": k["t"], "v": k["value"], "d": k.get("decimals", 0)} for k in tiles], "hd": hd, "until": spec.get("until"), "side": L["side"]}
    j = [JS_UTIL, f"const J = {js(J)};", r"""
const $$ = (id) => document.getElementById(id);
const fmt = (v, d) => v.toLocaleString("en-US", {minimumFractionDigits: d, maximumFractionDigits: d});
window.onPlace = (t) => { J.k.forEach((k, i) => { const u = easeOut3((t - (k.t + .35)) / 1.6); $$("kn" + i).textContent = fmt(k.v * u, k.d); }); };
tl.set(".spd", {transformOrigin: "50% 50%"}, 0);
if (J.hd) tl.fromTo("#kh", {opacity: 0, y: 12}, {opacity: 1, y: 0, duration: .5, ease: "power3.out"}, J.hd.t);
J.k.forEach((k, i) => {
  const g = `#k${i}`;
  tl.fromTo(g, {opacity: 0, x: J.side === "R" ? 50 : -50, rotateY: J.side === "R" ? -12 : 12}, {opacity: 1, x: 0, rotateY: 0, duration: .7, ease: "expo.out"}, k.t);
  tl.fromTo(`${g} .kl`, {opacity: 0, y: 10}, {opacity: 1, y: 0, duration: .45, ease: "power3.out"}, k.t + .15);
  tl.fromTo(`${g} .pr`, {scaleX: 0}, {scaleX: 1, duration: 1.6, ease: "power2.out"}, k.t + .35);
  tl.to(`${g} .pr`, {opacity: 0, duration: .4}, k.t + 2.0);
  tl.fromTo(`${g} .spl`, {attr: {"stroke-dashoffset": 1}}, {attr: {"stroke-dashoffset": 0}, duration: 1.4, ease: "power2.inOut"}, k.t + .4);
  tl.fromTo(`${g} .spd`, {scale: 0}, {scale: 1, duration: .35, ease: "back.out(3)"}, k.t + 1.75);
  tl.fromTo(`${g} .kd`, {opacity: 0, scale: .6}, {opacity: 1, scale: 1, duration: .4, ease: "back.out(2.5)"}, k.t + 1.9);
});
if (J.until != null) tl.to(".kt", {opacity: 0, x: J.side === "R" ? 40 : -40, duration: .4, ease: "power3.in", stagger: .08}, J.until - .6);
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_whoosh", k["t"], .35) for k in tiles] + [cue("soft_pulse", k["t"] + 1.9, .35) for k in tiles]
    sfx += audio_cues(spec, base, .5)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud="".join(h), js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .6), extra=tp["files"])
