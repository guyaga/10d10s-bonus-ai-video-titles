"""STOMP-ESCORT and COUNTDOWN-CTA: the social stomp runway package.

Escort: per item, a red index tag + giant display word + price sticker slam in ON THE BEAT beside the tracked subject
and ride with it (scaled by the subject's height). Optional big word (behind the subject when a matte is given),
optional finale ("THE LOOK" + item row + total), optional flash-sale countdown stack (COUNTDOWN-CTA).

Spec keys (JSON). Required: clip, track, items (escort) and/or countdown.
  follow        tracked object the escort rides (default "model"); any vtrack object with a full-body box
  beat          {"bpm": 120, "offset": 0.035}  beat n = offset + n * 60/bpm  (measure with librosa on your music)
  brand         {"name": "ATELIER VEYRA", "tag": "AW26", "beat": 1}          optional
  look          {"text": "LOOK 07", "beat": 4, "until": 9}                    optional label over the subject's head
  items         [{"key", "word", "name", "price", "image", "side": "L|R", "beat"}]   image optional
  sticker_min_scale  floor for the price sticker's scale while the subject is small/far (default .62; the word may go to .42)
  big_word      {"text": "AW26", "beat": 24, "until": 29}                   behind the subject when "matte" is set
  finale        {"title": "THE LOOK", "beat": 24, "label": "five pieces"}   optional end card
  countdown     {"beat": 29, "seconds": 15, "discount": 0.2, "pill": "FLASH SALE", "label": "the complete look",
                 "note": "-20% · NEXT 15 SECONDS ONLY", "button": "SHOP NOW →", "rail": true, "hot_last": 5}
  colors        {"paper": "#f6f1e8", "ink": "#16130f", "accent": "#ff3d2e"}
  fonts         {"display": "Anton", "serif": "Bodoni Moda", "body": "Archivo"}
  currency      "$" | "€" | "₪" ...     music, music_vol, plate_vol, matte, name
"""
from styles.common import (STOMP_JS, audio_cues, cue, e, fonts, js, money, project_dir, res, tracks)

DEF_COL = {"paper": "#f6f1e8", "ink": "#16130f", "accent": "#ff3d2e"}
DEF_FONT = {"display": "Anton", "serif": "Bodoni Moda", "body": "Archivo"}


def build(spec, base, style="STOMP-ESCORT"):
    items = spec.get("items", [])
    cd = spec.get("countdown")
    if style == "COUNTDOWN-CTA" and not cd:
        raise SystemExit("COUNTDOWN-CTA needs a 'countdown' block")
    if not items and not cd:
        raise SystemExit("STOMP-ESCORT needs 'items'")
    col = {**DEF_COL, **spec.get("colors", {})}
    fnt = {**DEF_FONT, **spec.get("fonts", {})}
    cur = spec.get("currency", "$")
    bpm = spec.get("beat", {}).get("bpm", 120)
    off = spec.get("beat", {}).get("offset", 0.0)
    B = lambda i: round(off + 60 / bpm * i, 3)  # noqa: E731
    follow = spec.get("follow", "model")
    brand = spec.get("brand")
    look = spec.get("look")
    big = spec.get("big_word")
    fin = spec.get("finale")
    matte = res(base, spec["matte"]) if spec.get("matte") else None
    n_items = len(items)
    end_beats = [x["beat"] for x in (big, fin, cd) if x]
    end_beat = min(end_beats) if end_beats else (items[-1]["beat"] + 4 if items else 0)
    total = sum(i["price"] for i in items)
    disc = cd.get("discount", .2) if cd else 0
    sale_total = round(total * (1 - disc))

    faces, extra = fonts(fnt["display"], fnt["serif"], fnt["body"])
    D, SF, BD = fnt["display"], fnt["serif"], fnt["body"]
    for it in items:
        if it.get("image"):
            extra[f"items/{it['key']}{res(base, it['image']).suffix}"] = res(base, it["image"])
    img = lambda it: f"assets/items/{it['key']}{res(base, it['image']).suffix}" if it.get("image") else ""  # noqa: E731

    css = faces + f"""
:root{{--paper:{col['paper']};--ink:{col['ink']};--hot:{col['accent']}}}
#root{{font-family:"{BD}",sans-serif}}
#stage,#stage2{{position:absolute;inset:0}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.esc{{position:absolute;left:0;top:0;width:0;height:0}}
.esc .sc{{position:absolute;left:0;top:0;transform-origin:0 0}}
.esc.L .sc{{transform-origin:100% 0}}
.esc .inner{{position:relative;display:flex;flex-direction:column}}
.esc.L .inner{{align-items:flex-end}}
.word{{font-family:"{D}",sans-serif;font-size:170px;line-height:1;color:var(--paper);letter-spacing:.01em;
  text-shadow:7px 7px 0 var(--ink);-webkit-text-stroke:3px var(--ink);white-space:nowrap}}
.idx{{display:inline-block;width:max-content;background:var(--hot);color:var(--ink);font-weight:700;font-size:22px;letter-spacing:.14em;padding:6px 12px;margin-bottom:10px;border:3px solid var(--ink)}}
.stk{{display:flex;align-items:center;gap:16px;margin-top:30px;padding:12px 18px 12px 12px;background:var(--paper);border:3px solid var(--ink);box-shadow:8px 8px 0 var(--ink);width:max-content}}
.esc.L .stk{{transform:rotate(-4deg);transform-origin:100% 0}}.esc.R .stk{{transform:rotate(3deg);transform-origin:0 0}}
.stk img{{width:112px;height:112px;object-fit:contain;background:#ede6da;border:2px solid var(--ink);display:block}}
.stk .nm{{display:block;font-family:"{SF}",serif;font-style:italic;font-size:32px;color:var(--ink);white-space:nowrap}}
.stk .pr{{display:inline-block;margin-top:8px;background:var(--hot);color:var(--ink);font-weight:700;font-size:34px;padding:4px 14px;border:3px solid var(--ink)}}
#brand{{position:absolute;left:96px;top:72px;display:flex;align-items:center;gap:14px}}
#brand .b{{font-family:"{SF}",serif;font-weight:600;font-size:40px;letter-spacing:.22em;color:var(--ink);background:var(--paper);padding:8px 18px;border:3px solid var(--ink)}}
#brand .s{{font-family:"{D}",sans-serif;font-size:40px;color:var(--ink);background:var(--hot);padding:4px 16px;border:3px solid var(--ink)}}
#lk{{position:absolute;left:0;top:0;width:0;height:0}}
#lk span{{position:absolute;left:0;bottom:24px;transform:translateX(-50%);white-space:nowrap;font-family:"{D}",sans-serif;font-size:44px;
  color:var(--ink);background:var(--paper);padding:2px 16px;border:3px solid var(--ink);box-shadow:5px 5px 0 var(--hot)}}
.bw{{position:absolute;left:0;top:0;width:0;height:0}}
.bw span{{position:absolute;left:0;top:0;transform:translate(-50%,0);font-family:"{D}",sans-serif;font-size:520px;line-height:1;color:var(--hot);
  white-space:nowrap;text-shadow:14px 14px 0 var(--ink)}}
#fin{{position:absolute;inset:0}}
#fin .dim{{position:absolute;inset:0;background:rgba(22,19,15,.55)}}
#fin .t{{position:absolute;left:0;right:0;top:150px;text-align:center;font-family:"{D}",sans-serif;font-size:300px;line-height:.9;color:var(--paper);
  text-shadow:10px 10px 0 var(--hot);-webkit-text-stroke:4px var(--ink)}}
#fin .row{{position:absolute;left:0;right:0;top:560px;display:flex;justify-content:center;gap:22px}}
#fin .row img{{width:170px;height:170px;object-fit:contain;background:var(--paper);border:3px solid var(--ink);box-shadow:7px 7px 0 var(--hot)}}
#fin .tot{{position:absolute;left:0;right:0;margin:0 auto;top:800px;width:max-content;display:flex;align-items:center;gap:20px}}
#fin .tot .a{{font-family:"{SF}",serif;font-style:italic;font-size:44px;color:var(--paper)}}
#fin .tot .c{{font-family:"{D}",sans-serif;font-size:96px;color:var(--ink);background:var(--hot);padding:0 24px;border:4px solid var(--paper)}}
#cta{{position:absolute;right:80px;top:70px;width:560px}}
#cta .pill{{display:inline-block;font-family:"{D}",sans-serif;font-size:46px;color:var(--ink);background:var(--hot);padding:2px 18px;border:3px solid var(--ink)}}
#cta .lbl{{display:block;font-family:"{SF}",serif;font-style:italic;font-size:40px;color:var(--ink);margin-top:18px;background:var(--paper);padding:6px 16px;width:max-content;border:3px solid var(--ink)}}
#cta .was{{position:relative;display:block;width:max-content;font-family:"{D}",sans-serif;font-size:64px;line-height:1.2;color:var(--paper);background:var(--ink);padding:0 14px;margin-top:14px;margin-bottom:34px}}
#cta .was i{{position:absolute;left:-6px;right:-6px;top:52%;height:8px;background:var(--hot);transform-origin:0 50%;border:2px solid var(--ink)}}
#cta .now{{display:block;font-family:"{D}",sans-serif;font-size:150px;line-height:1.15;margin-top:6px;margin-bottom:34px;color:var(--paper);text-shadow:8px 8px 0 var(--ink);-webkit-text-stroke:3px var(--ink)}}
#cta .off{{display:block;width:max-content;margin-top:12px;font-weight:700;font-size:26px;letter-spacing:.12em;color:var(--ink);background:var(--paper);padding:6px 14px;border:3px solid var(--ink)}}
#timer{{position:absolute;right:80px;top:740px;width:560px;background:var(--ink);border:4px solid var(--paper);padding:14px 22px 18px;display:flex;flex-wrap:wrap;align-items:center;column-gap:26px}}
#timer .k{{display:block;width:150px;font-weight:700;font-size:22px;line-height:1.3;letter-spacing:.2em;color:var(--paper)}}
#timer .t{{display:block;font-family:"{D}",sans-serif;font-size:120px;line-height:1.2;color:var(--paper)}}
#timer.hot .t{{color:var(--hot)}}
#timer .bar{{flex:0 0 100%;height:12px;background:rgba(246,241,232,.2);margin-top:6px}}
#timer .bar i{{display:block;height:100%;background:var(--hot);transform-origin:0 50%}}
#buy{{position:absolute;left:0;right:0;margin:0 auto;bottom:40px;width:max-content;font-family:"{D}",sans-serif;font-size:60px;color:var(--ink);
  background:var(--hot);padding:6px 44px;border:4px solid var(--ink);box-shadow:8px 8px 0 var(--ink)}}
#rail{{position:absolute;left:70px;top:140px;display:flex;flex-direction:column;gap:14px}}
#rail .it{{display:flex;align-items:center;gap:12px;background:var(--paper);border:3px solid var(--ink);padding:6px 14px 6px 6px;box-shadow:5px 5px 0 var(--ink)}}
#rail img{{width:86px;height:86px;object-fit:contain;background:#ede6da;display:block}}
#rail .p{{display:block;font-family:"{D}",sans-serif;font-size:36px;color:var(--ink)}}
#rail .o{{display:block;font-weight:700;font-size:18px;color:#4a4238;text-decoration:line-through}}
"""
    esc = []
    for k, it in enumerate(items, 1):
        side = it.get("side", "L" if k % 2 else "R")
        it["side"] = side
        sticker = (f'<div class="stk">' + (f'<img src="{img(it)}" alt="{e(it["name"])}">' if it.get("image") else "")
                   + f'<div><span class="nm">{e(it["name"])}</span><span class="pr">{money(it["price"], cur)}</span></div></div>')
        esc.append(f'<div class="esc {side}" id="e-{e(it["key"])}"><div class="sc"><div class="inner">'
                   f'<span class="idx">{k:02d} / {n_items:02d}</span><span class="word">{e(it["word"])}</span>{sticker}</div></div></div>')
    behind = f'<div class="bw" id="bigw" data-follow="{e(follow)}" data-anchor="t" data-dy="-60"><span data-layout-allow-overlap>{e(big["text"])}</span></div>' if big else ""
    front = [f'<div id="lk" data-follow="{e(follow)}" data-anchor="t"><span>{e(look["text"])}</span></div>' if look else "", "".join(esc)]
    if brand:
        front.append(f'<div id="brand"><span class="b">{e(brand["name"])}</span>' + (f'<span class="s">{e(brand["tag"])}</span>' if brand.get("tag") else "") + "</div>")
    if fin:
        row = "".join(f'<img src="{img(i)}" alt="{e(i["name"])}">' for i in items if i.get("image"))
        front.append(f'<div id="fin"><div class="dim"></div><div class="t">{e(fin.get("title", "THE LOOK"))}</div><div class="row">{row}</div>'
                     f'<div class="tot"><span class="a">{e(fin.get("label", f"{n_items} pieces"))}</span><span class="c">{money(total, cur)}</span></div></div>')
    if cd:
        secs = int(cd.get("seconds", 15))
        if cd.get("rail", True) and items:
            rail = "".join(f'<div class="it">' + (f'<img src="{img(i)}" alt="{e(i["name"])}">' if i.get("image") else "")
                           + f'<div><span class="p">{money(round(i["price"] * (1 - disc)), cur)}</span><span class="o">{money(i["price"], cur)}</span></div></div>' for i in items)
            front.append(f'<div id="rail">{rail}</div>')
        note = cd.get("note", f"−{round(disc * 100)}% · NEXT {secs} SECONDS ONLY")
        was = f'<span class="was">{money(cd.get("was", total), cur)}<i></i></span>'
        front.append(f'<div id="cta"><span class="pill">{e(cd.get("pill", "FLASH SALE"))}</span><span class="lbl">{e(cd.get("label", "the complete look"))}</span>'
                     f'{was}<span class="now">{money(cd.get("now", sale_total), cur)}</span><span class="off">{e(note)}</span></div>'
                     f'<div id="timer"><span class="k">{e(cd.get("timer_label", "OFFER ENDS IN"))}</span><span class="t" id="tt">00:{secs:02d}</span><div class="bar"><i id="tb"></i></div></div>'
                     f'<div id="buy">{e(cd.get("button", "SHOP NOW →"))}</div>')
    if matte:
        hud = f'<div id="stage">{behind}</div>\n<!--MATTE-->\n<div id="stage2">{"".join(front)}</div><div id="flash"></div>'
        extra["matte.webm"] = matte
    else:
        hud = f'<div id="stage">{behind}{"".join(front)}</div><div id="flash"></div>'

    ITEMS = [[i["key"], i["side"], i["beat"]] for i in items]
    j = [STOMP_JS, f"const B = (i) => +({off} + {60 / bpm} * i).toFixed(3);",
         f"const ITEMS = {js(ITEMS)}; const FOLLOW = {js(follow)}; const END = B({end_beat}); const STK_MIN = {spec.get('sticker_min_scale', .62)};"]
    j.append(r"""
window.onPlace = (t) => {
  const m = boxAt(FOLLOW, t); if (!m) return;
  const h = m[3] - m[1], s = Math.max(.42, Math.min(1, h / 820));
  for (const [key, side] of ITEMS) {
    const el = document.getElementById("e-" + key), sc = el.firstElementChild;
    el.style.left = (side === "L" ? m[0] - 30 : m[2] + 30) + "px"; el.style.top = (m[1] + h * .18) + "px";
    sc.style.transform = side === "L" ? `translateX(-100%) scale(${s})` : `scale(${s})`;
    // the price sticker must stay legible while the subject is far away: its own floor (STK_MIN) on top of the word's scale
    const stk = el.getElementsByClassName("stk")[0];
    if (stk) stk.style.scale = String(Math.max(STK_MIN, s) / s);
  }
  const lk = document.getElementById("lk"); if (lk) lk.firstElementChild.style.fontSize = (44 * Math.max(.6, s)) + "px";
  if (window.onCD) window.onCD(t);
};
ITEMS.forEach(([key, side, bi], k) => {
  const g = `#e-${key}`;
  tl.set(`${g} .inner`, {opacity: 1}, 0);
  tl.fromTo(`${g} .idx`, {opacity: 0, y: 16}, {opacity: 1, y: 0, duration: .12}, B(bi) - .12);
  stomp(`${g} .word`, B(bi));
  tl.fromTo(`${g} .stk`, {opacity: 0, scale: 1.5, y: 24}, {opacity: 1, scale: 1, y: 0, duration: .18, ease: "back.out(2.2)"}, B(bi + 1));
  tl.to(`${g} .inner`, {opacity: 0, scale: .85, duration: .12, ease: "power2.in"}, (k < ITEMS.length - 1 ? B(ITEMS[k + 1][2]) : END) - .14);
});
tl.set(ITEMS.map(([k]) => `#e-${k} .idx, #e-${k} .word, #e-${k} .stk`).join(",") || "#nothing", {opacity: 0}, 0);
""")
    hits = []
    if brand:
        bb = brand.get("beat", 1)
        j.append(f'stomp("#brand", B({bb}), 1.5); tl.to("#brand", {{opacity: 0, duration: .15}}, END);')
        hits.append(B(bb))
    if look:
        j.append(f'tl.fromTo("#lk span", {{opacity: 0, y: 20}}, {{opacity: 1, y: 0, duration: .2, ease: "back.out(2)"}}, B({look.get("beat", 4)}));'
                 f'tl.to("#lk span", {{opacity: 0, duration: .15}}, B({look.get("until", 9)}) - .1); tl.set("#lk span", {{opacity: 0}}, 0);')
    if big:
        j.append(f'tl.set("#bigw", {{opacity: 0}}, 0); tl.to("#bigw", {{opacity: 1, duration: .01}}, B({big["beat"]}) - .02);'
                 f'stomp("#bigw span", B({big["beat"]}), 2.4); tl.to("#bigw", {{opacity: 0, duration: .25}}, B({big.get("until", big["beat"] + 5)}) - .3);')
        hits.append(B(big["beat"]))
    if fin:
        fb = fin["beat"]
        j.append(f'tl.set("#fin", {{opacity: 0}}, 0); tl.to("#fin", {{opacity: 1, duration: .01}}, B({fb}) - .02);'
                 f'tl.fromTo("#fin .dim", {{opacity: 0}}, {{opacity: 1, duration: .15}}, B({fb}) - .05); stomp("#fin .t", B({fb}), 2.2);'
                 f'tl.fromTo("#fin .row img", {{opacity: 0, scale: 1.6, y: 40}}, {{opacity: 1, scale: 1, y: 0, duration: .16, stagger: .1, ease: "back.out(2)"}}, B({fb + 1}));'
                 f'stomp("#fin .tot", B({fb + 2}), 1.8);')
        hits += [B(fb), B(fb + 2)]
    if cd:
        cb, secs, hot = cd["beat"], int(cd.get("seconds", 15)), int(cd.get("hot_last", 5))
        j.append(f"const CD0 = B({cb}), SECS = {secs}, HOT = {hot};")
        j.append(r"""
window.onCD = (t) => {
  const rem = Math.max(0, SECS - Math.floor(t - CD0));
  document.getElementById("tt").textContent = "00:" + String(t < CD0 ? SECS : rem).padStart(2, "0");
  document.getElementById("tb").style.transform = `scaleX(${t < CD0 ? 1 : Math.max(0, 1 - (t - CD0) / SECS)})`;
  document.getElementById("timer").classList.toggle("hot", t >= CD0 + SECS - HOT);
};
if (!ITEMS.length) window.onPlace = (t) => window.onCD(t);
const CTA = ["#rail", "#cta", "#timer", "#buy"].filter(s => document.querySelector(s));
tl.set(CTA, {opacity: 0}, 0);
tl.to(CTA, {opacity: 1, duration: .01}, CD0 - .02);
stomp("#cta .pill", CD0, 2);
tl.fromTo("#cta .lbl", {opacity: 0, x: 30}, {opacity: 1, x: 0, duration: .18, ease: "power3.out"}, B(__CB__ + 1));
tl.fromTo("#cta .was", {opacity: 0, y: 20}, {opacity: 1, y: 0, duration: .15}, B(__CB__ + 1));
tl.fromTo("#cta .was i", {scaleX: 0}, {scaleX: 1, duration: .2, ease: "power3.out"}, B(__CB__ + 2));
stomp("#cta .now", B(__CB__ + 3), 2.1);
tl.fromTo("#cta .off", {opacity: 0, y: 14}, {opacity: 1, y: 0, duration: .16}, B(__CB__ + 4));
stomp("#timer", CD0, 1.6);
if (document.querySelector("#rail")) tl.fromTo("#rail .it", {opacity: 0, x: -40}, {opacity: 1, x: 0, duration: .16, stagger: .5, ease: "back.out(2)"}, B(__CB__ + 1));
stomp("#buy", B(__CB__ + 5), 1.7);
for (let k = __CB__ + 7; B(k) < CD0 + SECS; k += 2) tl.fromTo("#buy", {scale: 1.08}, {scale: 1, duration: .3, ease: "power2.out"}, B(k));
for (let sec = SECS - HOT; sec < SECS; sec++) { tl.fromTo("#timer .t", {scale: 1.25}, {scale: 1, duration: .25, ease: "power3.out"}, CD0 + sec); shake(CD0 + sec, .5); }
""".replace("__CB__", str(cb)))
        hits += [B(cb), B(cb + 3), B(cb + 5)]

    thumps = spec.get("thumps", True)
    sfx = audio_cues(spec, base, .75)
    if thumps:
        hits += [B(i["beat"]) for i in items]
        sfx += [cue("soft_thump", h - .02, .45) for h in hits]
        sfx += [cue("soft_click", B(i["beat"] + 1) - .02, .3) for i in items]
        if cd:
            c0 = B(cd["beat"])
            sfx += [cue("soft_pulse" if s >= secs - hot else "soft_tick", c0 + s, .35 if s >= secs - hot else .22) for s in range(1, secs + 1)]
    return dict(project=project_dir(spec, style), clip=res(base, spec["clip"]), track=tracks(spec, base), css=css, hud=hud,
                js="\n".join(j), sfx=sfx, plate_vol=spec.get("plate_vol", .15), extra=extra)
