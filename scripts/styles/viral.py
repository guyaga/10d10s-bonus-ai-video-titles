"""VIRAL-CAPTIONS: Hormozi / MrBeast social captions driven by word timings. 1-3 huge words at a time, the spoken word
bounces in (scale overshoot + tiny tilt), keywords in colour, an emoji pops above the group on chosen words, thick
outline + drop shadow so it reads over anything. Hebrew (RTL) or English.

Spec keys. Required: clip, words.
  words        word-timing JSON: [{"w": "...", "t": 1.23}, ...]  (scripts/word_times.py output, or any transcript)
  language     "he" | "en";  pair: Hebrew pairing (default "secular"; see common.HE_PAIRS)
  keywords     ["אוויר", "AIR", ...]    words drawn in the keyword colour (punctuation ignored)
  emoji        {"אוויר": "🌬️", "קרבון": "⚡"}   an emoji pops above the group when that word is spoken
  max_words    words per caption group (default 3); groups also break on . , ! ?
  hold         seconds a group stays after its last word (default .6, capped by the next group)
  dim          opacity of a group's not-yet-spoken words (default .5; 0 = words appear only when spoken)
  y            caption centre as a fraction of frame height (default .72)
  size         font size px for the spoken words (default 150)
  colors       {"text": "#ffffff", "key": "#ffe14d", "stroke": "#000000", "key2": "#39ff88"}  key2 = every 2nd keyword
  vo           voiceover file (the words' audio), vo_vol;  music, music_vol, plate_vol, name, track (optional)
"""
import json
import urllib.request

import paths
from styles.common import (audio_cues, cue, e, js, project_dir, res, tracks, type_pair)


def twemoji(ch):
    """Colour emoji as a Twemoji SVG (CC-BY 4.0), downloaded once into assets/emoji: headless renders have no emoji font."""
    cp = "-".join(f"{ord(c):x}" for c in ch if ord(c) != 0xFE0F)
    out = paths.SKILL / "assets" / "emoji" / f"{cp}.svg"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        url = f"https://cdn.jsdelivr.net/gh/jdecked/twemoji@15.1.0/assets/svg/{cp}.svg"
        out.write_bytes(urllib.request.urlopen(url, timeout=30).read())
    return out


def clean(w):
    return "".join(ch for ch in w if ch.isalnum() or "֐" <= ch <= "׿").lower()


def build(spec, base, style="VIRAL-CAPTIONS"):
    W = json.loads(res(base, spec["words"]).read_text(encoding="utf-8"))
    W = [{"w": x["w"], "t": float(x["t"])} for x in W]
    tp = type_pair(spec, latin=("Rubik", 900, "Rubik", 400), default_pair="secular")
    col = {"text": "#ffffff", "key": "#ffe14d", "key2": "#39ff88", "stroke": "#000000", **spec.get("colors", {})}
    keys = {clean(k) for k in spec.get("keywords", [])}
    emoji = {clean(k): v for k, v in spec.get("emoji", {}).items()}
    mx, hold = spec.get("max_words", 3), spec.get("hold", .6)
    # digits glue to the next word (adkit rule): merge a numeric token with the word after it
    merged, i = [], 0
    while i < len(W):
        w = W[i]
        if clean(w["w"]).isdigit() and i + 1 < len(W):
            merged.append({"w": w["w"] + " " + W[i + 1]["w"], "t": w["t"]})
            i += 2
        else:
            merged.append(w)
            i += 1
    groups, cur = [], []
    for w in merged:
        cur.append(w)
        if len(cur) >= mx or w["w"].rstrip().endswith((".", ",", "!", "?", "…")):
            groups.append(cur)
            cur = []
    if cur:
        groups.append(cur)
    G, html, nk, extra_files = [], [], 0, {}
    for gi, g in enumerate(groups):
        end = min(g[-1]["t"] + hold + .35, groups[gi + 1][0]["t"] - .02 if gi + 1 < len(groups) else 1e9)
        ws = []
        for wi, w in enumerate(g):
            k = clean(w["w"].split()[-1]) in keys or clean(w["w"]) in keys
            cls = "w"
            if k:
                cls += " k2" if nk % 2 else " k"
                nk += 1
            ws.append(f'<span class="{cls}" id="g{gi}w{wi}">{e(w["w"].strip(".,!?…"))}</span>')
            em = emoji.get(clean(w["w"])) or emoji.get(clean(w["w"].split()[-1]))
            if em:
                svg = twemoji(em)
                extra_files[f"emoji/{svg.name}"] = svg
                html.append(f'<div class="em" id="g{gi}e{wi}"><img src="assets/emoji/{svg.name}" alt=""></div>')
        html.append(f'<div class="grp" id="g{gi}">' + "".join(ws) + "</div>")
        G.append({"t": [w["t"] for w in g], "end": round(end, 3), "em": [bool(emoji.get(clean(w["w"])) or emoji.get(clean(w["w"].split()[-1]))) for w in g]})
    y, size = spec.get("y", .72), spec.get("size", 150)
    css = tp["css"] + f"""
#cap{{position:absolute;inset:0}}
.grp{{position:absolute;left:0;right:0;top:{round(y * 1080)}px;transform:translateY(-50%);display:flex;justify-content:center;flex-wrap:wrap;gap:0 .26em;
  direction:{tp['dir']};font-family:"{tp['display']}",sans-serif;font-weight:{tp['dw']};font-size:{size}px;line-height:1.02;padding:0 120px;opacity:0}}
.w{{display:inline-block;color:{col['text']};-webkit-text-stroke:{max(8, size // 12)}px {col['stroke']};paint-order:stroke fill;
  text-shadow:0 {size // 18}px 0 {col['stroke']},0 {size // 9}px {size // 5}px rgba(0,0,0,.45);opacity:0;white-space:nowrap}}
.w.k{{color:{col['key']}}}.w.k2{{color:{col['key2']}}}
.em{{position:absolute;left:50%;top:{round(y * 1080 - size * 1.2)}px;width:{round(size * 1.25)}px;height:{round(size * 1.25)}px;margin:-{round(size * .625)}px 0 0 -{round(size * .625)}px;opacity:0;
  filter:drop-shadow(0 8px 14px rgba(0,0,0,.45))}}
.em img{{width:100%;height:100%;display:block}}
"""
    j = [f"const G = {js(G)}, DIR = {js(tp['dir'])}, DIM = {spec.get('dim', .5)};", r"""
// each emoji sits above its own word (measured from the laid-out caption, so RTL and wrapping are handled)
window.onPlace = () => {
  G.forEach((g, gi) => g.em.forEach((has, wi) => {
    if (!has) return;
    const w = document.getElementById("g" + gi + "w" + wi), m = document.getElementById("g" + gi + "e" + wi);
    if (w && m) m.style.left = (w.offsetLeft + w.offsetWidth / 2) + "px";
  }));
};
G.forEach((g, gi) => {
  tl.set(`#g${gi}`, {opacity: 1}, g.t[0] - .02); tl.set(`#g${gi}`, {opacity: 0}, g.end);
  tl.fromTo(`#g${gi}`, {scale: .9, y: 30}, {scale: 1, y: 0, duration: .16, ease: "back.out(2.6)", immediateRender: false}, g.t[0]);
  g.t.forEach((t, wi) => {
    const s = `#g${gi}w${wi}`, tilt = (wi % 2 ? 1 : -1) * 3 * (DIR === "rtl" ? -1 : 1);
    // the whole group is up from its first word (unspoken words dimmed), each word pops to full when spoken
    tl.set(s, {opacity: DIM}, g.t[0] - .02); tl.set(s, {opacity: 1}, t);
    tl.fromTo(s, {scale: 1.55, rotation: tilt, y: 18}, {scale: 1, rotation: 0, y: 0, duration: .22, ease: "back.out(3.4)", immediateRender: false}, t);
    // syllable pulse: a second smaller bounce half-way through the word
    const nxt = wi + 1 < g.t.length ? g.t[wi + 1] : t + .45;
    if (nxt - t > .34) tl.fromTo(s, {scale: 1.12}, {scale: 1, duration: .14, ease: "power2.out", immediateRender: false}, t + (nxt - t) * .55);
    if (g.em[wi]) {
      const m = `#g${gi}e${wi}`;
      tl.set(m, {opacity: 1}, t); tl.set(m, {opacity: 0}, Math.min(g.end, t + 1.1));
      tl.fromTo(m, {scale: 0, rotation: -25}, {scale: 1, rotation: 0, duration: .32, ease: "back.out(3)", immediateRender: false}, t);
      tl.to(m, {y: -24, duration: .5, ease: "sine.out"}, t + .3);
    }
  });
});
"""]
    sfx = []
    if spec.get("sfx", True):
        sfx = [cue("ui_pop", g["t"][i], .28) for g in G for i in range(len(g["t"])) if g["em"][i]]
    sfx += audio_cues(spec, base, .35)
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css,
                hud='<div id="cap">' + "".join(html) + "</div>", js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .25), extra={**tp["files"], **extra_files})
