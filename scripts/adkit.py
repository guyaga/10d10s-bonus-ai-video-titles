"""Declarative ad builder v2 (high-end HUD): an ad = palette + font theme + list of timed, tracked elements.

Element types (times in s; 'end' optional -> stays to the end):
  stomp   {text, t, end, x, y | follow, anchor, dx, dy, size, behind, color, shadow, align, sub}
  tag     {title, sub, t, end, follow, anchor, dx, dy, side ('r'|'l')}
  box     {obj, t, end, pad, label}
  callout {obj, fx, fy, title, sub, t, end, x, y}
  counter {t0, t1, a, b, dec, pre, suf, label, t, end, x, y, size}
  ring    {obj, t, end, r, spin}
  chip    {text, sub, t}
  lockup  {brand, line, t}
  meter   {label, t, end}
Optional watermark: spec "watermark" = path to a PNG -> small, bottom-centre (omit for none).
Media paths (all optional, defaults follow the layout in paths.py): spec "clip", "track", "matte", "music", "vo".
Also: "punch" {times, amt, dur} zooms the plate+matte, "kine" word-synced social stomps, "tape" RTL highlight strips,
"flash" full-frame word card, "captions" karaoke words from word_times.py (see references/styles.md).
BESPOKE HOOKS (spec keys): "html_front" (raw HUD markup over everything), "html_behind" (raw markup between the plate and the matted subject), "js" (raw GSAP code appended; the timeline is `tl`, per-frame hook window.onPlace(t) may be wrapped, helpers boxAt(name,t)/anchor(b,a)/shake/stomp exist), "css", "fonts" ({"Family":[(file_stem, weight, style)]} with files in the fonts dir, see paths.py), "assets" ({"name.png": "/abs/path"} copied to assets/).
"""
import json
from pathlib import Path

import paths

# family -> [(file stem, weight, style)]
FAM = {
    "Anton": [("anton-latin-400", 400, "normal")],
    "DM Serif Display": [("dm-serif-display-latin-400-normal", 400, "normal"), ("dm-serif-display-latin-400-italic", 400, "italic")],
    "Space Grotesk": [(f"space-grotesk-latin-{w}-normal", w, "normal") for w in (400, 500, 700)],
    "Space Mono": [(f"space-mono-latin-{w}-normal", w, "normal") for w in (400, 700)],
    "Michroma": [("michroma-latin-400-normal", 400, "normal")],
    "Sora": [(f"sora-latin-{w}-normal", w, "normal") for w in (400, 600, 800)],
    "Barlow Condensed": [(f"barlow-condensed-latin-{w}-normal", w, "normal") for w in (600, 700, 800)],
    "Cormorant Garamond": [(f"cormorant-garamond-latin-{w}-normal", w, "normal") for w in (500, 600, 700)]
                          + [(f"cormorant-garamond-latin-{w}-italic", w, "italic") for w in (500, 600)],
    "Manrope": [(f"manrope-latin-{w}-normal", w, "normal") for w in (400, 500, 700)],
    "Assistant": [(f"assistant-{sub}-{w}", w, "normal") for w in (300, 400, 600, 700, 800) for sub in ("hebrew", "latin")],
    "Rubik": [(f"rubik-{sub}-{w}-normal", w, "normal") for w in (300, 400, 500, 700, 800, 900) for sub in ("hebrew", "latin")],
    "Heebo": [(f"heebo-{sub}-{w}-normal", w, "normal") for w in (200, 300, 400, 500, 600, 700, 800, 900) for sub in ("hebrew", "latin")],
    "Amatic SC": [(f"amatic-sc-{sub}-{w}-normal", w, "normal") for w in (400, 700) for sub in ("hebrew", "latin")],
    "Jost": [(f"jost-latin-{w}-normal", w, "normal") for w in (300, 500, 700)],
    "Caveat": [(f"caveat-latin-{w}-normal", w, "normal") for w in (600, 700)],
    "Tilt Neon": [("tilt-neon-latin-400-normal", 400, "normal")],
    "Oswald": [(f"oswald-latin-{w}-normal", w, "normal") for w in (600, 700)],
    "IBM Plex Mono": [("ibm-plex-mono-latin-500-normal", 500, "normal")],
    "Karantina": [(f"karantina-{sub}-{w}-normal", w, "normal") for w in (300, 400, 700) for sub in ("hebrew", "latin")],
    "Suez One": [(f"suez-one-{sub}-400-normal", 400, "normal") for sub in ("hebrew", "latin")],
    "Secular One": [(f"secular-one-{sub}-400-normal", 400, "normal") for sub in ("hebrew", "latin")],
    "Bodoni Moda": [(f"bodoni-moda-latin-{w}", w, "normal") for w in (400, 500, 600, 700)] + [("bodoni-moda-latin-400-italic", 400, "italic")],
    "Archivo": [(f"archivo-latin-{w}", w, "normal") for w in (400, 500, 600, 700)],
    "JetBrains Mono": [(f"jetbrains-mono-latin-{w}-normal", w, "normal") for w in (500, 700)],
    "Fraunces": [(f"fraunces-latin-{w}-normal", w, "normal") for w in (700, 900)] + [(f"fraunces-latin-{w}-italic", w, "italic") for w in (700, 900)],
}
# theme: display (stomps/titles), dstyle (css for display), label, mono, accentfont (taglines)
THEMES = {
    # Hebrew themes use only Guy's three faces: Karantina (loud display), Suez One (premium display), Secular One (labels, captions, UI)
    "he_bold":    dict(display="Karantina", dw=700, ds="normal", label="Secular One", mono="Space Mono", tag="Secular One", tagstyle="normal", chroma=False, rtl=True),
    "he_premium": dict(display="Suez One", dw=400, ds="normal", label="Secular One", mono="Space Mono", tag="Secular One", tagstyle="normal", chroma=False, premium=True, rtl=True),
    "sparta":   dict(display="DM Serif Display", dw=400, ds="normal", label="Space Grotesk", mono="Space Mono", tag="DM Serif Display", tagstyle="italic", chroma=False, premium=True),
    "guyaga":   dict(display="Anton", dw=400, ds="normal", label="Space Grotesk", mono="Space Mono", tag="DM Serif Display", tagstyle="italic", chroma=True),
    "tech":     dict(display="Michroma", dw=400, ds="normal", label="Sora", mono="Space Mono", tag="Sora", tagstyle="normal", chroma=True),
    "tactical": dict(display="Barlow Condensed", dw=800, ds="normal", label="Barlow Condensed", mono="Space Mono", tag="Barlow Condensed", tagstyle="normal", chroma=True),
    "luxe":     dict(display="Cormorant Garamond", dw=600, ds="italic", label="Manrope", mono="Manrope", tag="Cormorant Garamond", tagstyle="italic", chroma=False),
    "chef":     dict(display="Fraunces", dw=900, ds="italic", label="Manrope", mono="Space Mono", tag="Fraunces", tagstyle="italic", chroma=False),
    "travel":   dict(display="Sora", dw=800, ds="normal", label="Sora", mono="Space Mono", tag="Sora", tagstyle="normal", chroma=False),
}


def font_faces(theme):
    fams = {theme["display"], theme["label"], theme["mono"], theme["tag"], "Karantina", "Suez One", "Secular One"} if theme.get("rtl") else {theme["display"], theme["label"], theme["mono"], theme["tag"]}
    css, files = [], {}
    for fam in fams:
        for stem, w, st in FAM[fam]:
            ur = (";unicode-range:U+0590-05FF,U+FB1D-FB4F,U+200C-2010,U+20AA,U+25CC" if "-hebrew-" in stem
                  else ";unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+20AC,U+2122,U+2190-2199,U+2212,U+2215" if "-latin-" in stem and any("-hebrew-" in x[0] for x in FAM[fam]) else "")
            wt = "100 900" if len({x[1] for x in FAM[fam]}) == 1 else w   # single-weight faces cover every weight: no faux bold
            css.append(f'@font-face{{font-family:"{fam}";font-weight:{wt};font-style:{st};src:url(assets/fonts/{stem}.woff2) format("woff2"){ur}}}')
            files[f"fonts/{stem}.woff2"] = paths.fonts() / f"{stem}.woff2"
    return "".join(css), files


def _lum(hx):
    hx = hx.lstrip("#")
    r, g, b = (int(hx[i:i + 2], 16) / 255 for i in (0, 2, 4))
    f = lambda c: c / 12.92 if c <= .03928 else ((c + .055) / 1.055) ** 2.4  # noqa: E731
    return .2126 * f(r) + .7152 * f(g) + .0722 * f(b)


def css_for(p, th):
    D, L, M, G = th["display"], th["label"], th["mono"], th["tag"]
    tacc = p["ink"] if p["acc"].startswith("#") and _lum(p["acc"]) > .22 else "#ffffff"
    rtl = """
.st span,.tg,.co,#chip,#lock,#meter{{direction:rtl}}
.st span{{letter-spacing:0!important}}
.st i.he{{font-family:"Secular One",sans-serif;font-weight:400;letter-spacing:0;background:none;padding:0;color:var(--lt);text-shadow:0 4px 24px rgba(0,0,0,.6);direction:rtl}}
.tg .a,.co .a,#chip .a{{font-family:"Secular One",sans-serif;font-weight:400}}
.tg .b,.co .b,#chip .b,#meter .k,.ct .u{{font-family:"Secular One",sans-serif;font-weight:400;letter-spacing:0;font-size:22px}}
.tg .n{{font-family:"Space Mono",monospace}}
#lock .b{{font-family:"Secular One",sans-serif;font-weight:400}}
""".replace("{{", "{").replace("}}", "}") if th.get("rtl") else ""
    chroma = "-3px 0 rgba(255,40,80,.55),3px 0 rgba(40,220,255,.45)," if (th["chroma"] and not th.get("pop")) else ""
    return f"""
:root{{--tacc:{tacc};--acc:{p['acc']};--ink:{p['ink']};--lt:{p['lt']};--panel:{p['panel']};--sub:{p['sub']};--line:rgba(255,255,255,.22)}}
#root{{font-family:"{L}",sans-serif}}
#stage,#stage2{{position:absolute;inset:0}}
#flash{{position:absolute;inset:0;background:#fff;opacity:0}}
.D{{font-family:"{D}",sans-serif;font-weight:{th['dw']};font-style:{th['ds']}}}
.M{{font-family:"{M}",monospace}}
/* stomp */
.st{{position:absolute;left:0;top:0;width:0;height:0}}
.st span{{position:absolute;left:0;top:0;white-space:nowrap;line-height:1.05;font-family:"{D}",sans-serif;font-weight:{th['dw']};font-style:{th['ds']}}}
.st span.c{{text-shadow:{chroma}var(--sh)}}
.st i{{position:absolute;left:0;top:0;white-space:nowrap;font-family:"{M}",monospace;font-style:normal;font-size:22px;letter-spacing:.22em;color:var(--lt);background:var(--ink);padding:6px 12px}}
.st .bu{{position:absolute;left:0;top:0;transform:translate(-50%,-50%)}}
.st span.p{{-webkit-text-stroke:6px #111;paint-order:stroke fill}}
.st span.pm{{letter-spacing:.06em;text-shadow:0 10px 50px rgba(0,0,0,.55),0 2px 6px rgba(0,0,0,.4)}}
.st span.pm::after{{content:"";position:absolute;left:50%;bottom:-18px;width:140px;height:5px;background:var(--acc);transform:translateX(-50%)}}
/* kinetic social stomps */
.kn{{position:absolute;display:flex;flex-direction:column;align-items:center;direction:rtl}}
.kr{{display:flex;gap:0;align-items:baseline;direction:rtl;white-space:nowrap}}
.kw{{margin:0 .11em}}
.kw{{display:inline-block;font-family:"Karantina",sans-serif;font-weight:700;line-height:.98;color:var(--lt);text-shadow:0 16px 60px rgba(0,0,0,.55),0 2px 6px rgba(0,0,0,.35)}}
.kw.accent{{color:var(--acc)}}
.kw.outline{{color:rgba(17,17,17,.38);-webkit-text-stroke:5px var(--lt);paint-order:stroke fill;text-shadow:none}}
.kw.big{{font-family:"Karantina",sans-serif;font-weight:700;line-height:.86}}
.kw.light{{font-weight:700;opacity:.92}}
/* tape slogans (social highlight strips) */
.tp{{position:absolute;display:flex;flex-direction:column;gap:12px;direction:rtl}}
.tp.al-r{{align-items:flex-end}}.tp.al-l{{align-items:flex-start}}.tp.al-c{{align-items:center}}
.tl{{display:block;width:max-content;padding:.06em .34em .14em;font-family:"Karantina",sans-serif;font-weight:700;line-height:1.08;box-shadow:9px 9px 0 rgba(0,0,0,.38)}}
.tl.w7{{font-weight:700}}
.tl.acc{{background:var(--acc);color:var(--tacc,#fff)}}
.tl.ink{{background:var(--ink);color:var(--lt)}}
.tl.lt{{background:var(--lt);color:var(--ink)}}
.tl.big{{font-family:"Karantina",sans-serif;font-weight:700;line-height:.95;padding:.02em .3em .04em}}
.tl b{{display:inline-block;font-weight:inherit}}
#scrim{{position:absolute;left:0;right:0;bottom:0;height:420px;background:linear-gradient(180deg,transparent,rgba(0,0,0,.62));opacity:0}}
/* social: flash cards + karaoke captions */
.fc{{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;opacity:0}}
.fc span{{font-family:"Karantina",sans-serif;font-weight:700;line-height:.9;direction:rtl;white-space:nowrap}}
#cap{{position:absolute;left:0;right:0;bottom:150px;display:flex;justify-content:center;direction:rtl}}
.cg{{position:absolute;display:flex;gap:.28em;direction:rtl;white-space:nowrap;font-family:"Secular One",sans-serif;font-weight:400;font-size:66px;line-height:1.1;opacity:0}}
.cw{{display:inline-block;color:#fff;-webkit-text-stroke:9px #000;paint-order:stroke fill;text-shadow:0 6px 18px rgba(0,0,0,.6)}}
.cw.on{{color:var(--tacc);background:var(--acc);-webkit-text-stroke:0;padding:0 .14em;border-radius:6px;text-shadow:none;box-shadow:6px 6px 0 rgba(0,0,0,.45)}}
/* glass panel shared */
.gl{{background:var(--panel);backdrop-filter:blur(10px) saturate(1.15);border:1px solid var(--line);position:relative}}
.gl::before,.gl::after{{content:"";position:absolute;width:14px;height:14px;border-color:var(--acc);border-style:solid}}
.gl::before{{left:-1px;top:-1px;border-width:2px 0 0 2px}}
.gl::after{{right:-1px;bottom:-1px;border-width:0 2px 2px 0}}
/* tag */
.tg{{position:absolute;width:max-content;padding:12px 18px 12px 16px}}
[data-follow].tg{{height:auto}}
.tg.l{{transform:translateX(-100%)}}
.tg .n{{display:block;font-family:"{M}",monospace;font-size:15px;letter-spacing:.2em;color:var(--sub);margin-bottom:4px}}
.tg .a{{display:block;font-family:"{D}",sans-serif;font-weight:{th['dw']};font-style:{th['ds']};font-size:34px;line-height:1.15;color:var(--lt)}}
.tg .b{{display:block;font-family:"{M}",monospace;font-size:17px;letter-spacing:.08em;color:var(--sub);margin-top:6px}}
.tg .u{{display:block;height:2px;background:var(--acc);margin-top:10px;transform-origin:0 50%}}
/* box */
.bx .brk i{{border-color:var(--acc);width:30px;height:30px}}
.bx .lb{{position:absolute;left:0;top:-38px;font-family:"{M}",monospace;font-size:15px;letter-spacing:.2em;color:var(--ink);background:var(--acc);padding:5px 9px;white-space:nowrap}}
.bx .xh{{position:absolute;background:var(--acc)}}
.bx .x1{{left:50%;top:-12px;width:2px;height:12px}}.bx .x2{{left:50%;bottom:-12px;width:2px;height:12px}}
.bx .x3{{top:50%;left:-12px;height:2px;width:12px}}.bx .x4{{top:50%;right:-12px;height:2px;width:12px}}
/* callout */
.co{{position:absolute;padding:12px 18px 12px 16px;white-space:nowrap}}
.co .a{{display:block;font-family:"{D}",sans-serif;font-weight:{th['dw']};font-style:{th['ds']};font-size:32px;line-height:1.15;color:var(--lt)}}
.co .b{{display:block;font-family:"{M}",monospace;font-size:17px;color:var(--sub);margin-top:6px}}
#lines{{position:absolute;inset:0;width:1920px;height:1080px}}
/* counter */
.ct{{position:absolute;display:flex;flex-direction:column;gap:14px;padding:16px 20px}}
.ct .v{{display:block;font-family:"{D}",sans-serif;font-weight:{th['dw']};font-style:{th['ds']};line-height:1.1;color:var(--lt);font-variant-numeric:tabular-nums}}
.ct .u{{display:block;width:max-content;font-family:"{M}",monospace;font-size:20px;letter-spacing:.18em;color:var(--sub)}}
.ct .pb{{display:block;height:4px;background:rgba(255,255,255,.18)}}
.ct .pb b{{display:block;height:100%;background:var(--acc);transform-origin:0 50%}}
.rg{{position:absolute;left:0;top:0;width:0;height:0}}
/* chip */
#chip{{position:absolute;left:84px;top:56px;display:flex;flex-direction:column;gap:6px;padding:12px 18px 14px}}
#chip .b{{font-family:"{M}",monospace;font-size:16px;letter-spacing:.26em;color:var(--sub)}}
#chip .a{{font-family:"{D}",sans-serif;font-weight:{th['dw']};font-style:{th['ds']};font-size:40px;line-height:1.1;color:var(--lt);text-shadow:0 2px 18px rgba(0,0,0,.55)}}
/* lockup */
#lock{{position:absolute;left:0;right:0;margin:0 auto;bottom:112px;width:max-content;display:flex;align-items:center;gap:22px;padding:14px 26px}}
#lock .a{{font-family:"{D}",sans-serif;font-weight:{th['dw']};font-style:{th['ds']};font-size:70px;line-height:1.1;color:var(--lt)}}
#lock .s{{width:2px;height:54px;background:var(--acc)}}
#lock .b{{font-family:"{G}",serif;font-style:{th['tagstyle']};font-size:40px;line-height:1.2;color:var(--sub)}}
/* voice meter */
#meter{{position:absolute;right:70px;bottom:112px;width:300px;padding:12px 16px}}
#meter .k{{display:block;font-family:"{M}",monospace;font-size:15px;letter-spacing:.2em;color:var(--sub)}}
#meter .w{{display:flex;align-items:center;gap:5px;height:44px;margin-top:6px}}
#meter .w b{{display:block;width:6px;border-radius:3px;background:var(--lt)}}
/* watermark */"""  + rtl + f"""
#wm{{position:absolute;left:0;right:0;margin:0 auto;bottom:26px;height:44px;width:auto;opacity:.92;filter:drop-shadow(0 1px 6px rgba(0,0,0,.6))}}
"""


BRK = '<div class="brk"><i></i><i></i><i></i><i></i></div>'
# comic pop combos: (fill, offset shadow, burst)
POP = [("#FFD60A", "#FF2D87", "#00E5FF"), ("#00E5FF", "#FF3D00", "#FFD60A"), ("#FF2D87", "#FFD60A", "#7B2CFF"),
       ("#B6FF00", "#7B2CFF", "#FF2D87"), ("#FF7A00", "#00E5FF", "#FFD60A"), ("#FFFFFF", "#FF2D87", "#00E5FF")]
STAR = "polygon(50% 0%,58% 22%,78% 6%,72% 30%,98% 24%,80% 44%,100% 56%,76% 62%,90% 86%,64% 76%,58% 100%,48% 80%,34% 98%,32% 74%,8% 86%,20% 62%,0% 50%,22% 40%,4% 18%,30% 26%,26% 2%,44% 20%)"


# Old Hebrew families -> Guy's three faces. Applied to every Hebrew spec (css, markup, js), so specs written before the
# switch render with the new system without being rewritten. A spec may override or extend it with "he_fonts".
HE_REMAP = {
    "Assistant": "Secular One", "Heebo": "Secular One", "Miriam Libre": "Secular One", "IBM Plex Sans Hebrew": "Secular One",
    "Plex He": "Secular One", "PlexHe": "Secular One", "Varela Round": "Secular One",
    "Rubik": "Karantina", "Rubik Dirt": "Karantina", "Amatic SC": "Karantina",
    "Frank Ruhl Libre": "Suez One", "FRL He": "Suez One", "Bellefair": "Suez One",
}


def he_remap(css, hud, js, extra, remap):
    import re as _re
    for old, new in sorted(remap.items(), key=lambda kv: -len(kv[0])):
        q = _re.escape(old)
        css = _re.sub(r"@font-face\{font-family:\s*[\"']" + q + r"[\"'][^}]*\}", "", css)          # drop the old faces
        for text in ("css", "hud", "js"):
            v = {"css": css, "hud": hud, "js": js}[text]
            v = _re.sub(r"([\"'])" + q + r"\1", lambda m: m.group(1) + new + m.group(1), v)
            v = _re.sub(r"&quot;" + q + r"&quot;", "&quot;" + new + "&quot;", v)
            v = _re.sub(r"(font-family:\s*)" + q + r"(?=\s*[,;}])", lambda m: m.group(1) + '"' + new + '"', v)
            if text == "css":
                css = v
            elif text == "hud":
                hud = v
            else:
                js = v
    faces, files = font_faces({"display": "Karantina", "label": "Suez One", "mono": "Secular One", "tag": "Secular One"})
    extra.update(files)
    return faces + css, hud, js


def build(ad, spec):
    p, th = spec["palette"], THEMES[spec.get("theme", "guyaga")]
    els = spec["elements"]
    behind, front, lines, js, hide = [], [], [], [], []
    ntag = 0
    npop = 0
    for n, e in enumerate(els, 1):
        i = f"e{n}"
        t, end, k = e.get("t", 0), e.get("end"), e["type"]
        if k == "stomp":
            pos = (f'data-follow="{e["follow"]}" data-anchor="{e.get("anchor", "c")}" data-dx="{e.get("dx", 0)}" data-dy="{e.get("dy", 0)}"'
                   if "follow" in e else f'style="left:{e["x"]}px;top:{e["y"]}px"')
            tr = {"c": "translate(-50%,-50%)", "l": "translate(0,-50%)", "r": "translate(-100%,-50%)"}[e.get("align", "c")]
            shp = e.get("shadow_px", 8)
            st = (f'font-size:{e.get("size", 200)}px;color:{e.get("color", "var(--lt)")};transform:{tr};'
                  f'--sh:{shp}px {shp}px 0 {e.get("shadow", "var(--acc)")};' + (f'-webkit-text-stroke:{e["stroke"]};' if e.get("stroke") else ""))
            if th.get("rtl") and e.get("sub"):
                sub = f'<i class="he" style="font-size:{int(e.get("size", 200) * .34)}px;transform:translate(-50%,{int(e.get("size", 200) * .55)}px)">{e["sub"]}</i>'
            else:
                sub = (f'<i style="transform:translate(-50%,{int(e.get("size", 200) * .62)}px)">{e["sub"]}</i>' if e.get("sub") else "")
            burst = ""
            if th.get("pop") and not e.get("plain"):
                fill, sh2, bc = POP[npop % len(POP)]
                rot = (-4, 3, -2, 4)[npop % 4]
                npop += 1
                sz = e.get("size", 200)
                bw, bh = int(len(e["text"]) * sz * .56 + sz * .9), int(sz * 1.65)
                burst = (f'<div class="bu" style="width:{bw}px;height:{bh}px;background:{bc};clip-path:{STAR};'
                         f'transform:translate(-50%,-50%) rotate({rot * 2}deg)"></div>') if e.get("burst", True) else ""
                st = (f'font-size:{sz}px;color:{fill};transform:{tr} rotate({rot}deg);'
                      f'--sh:9px 9px 0 {sh2},16px 16px 0 #111;')
                h = f'<div class="st" id="{i}" {pos}>{burst}<span class="p c" style="{st}" data-layout-allow-overlap data-layout-allow-occlusion>{e["text"]}</span>{sub}</div>'
            elif th.get("premium"):
                st = f'font-size:{e.get("size", 200)}px;color:{e.get("color", "var(--lt)")};transform:{tr};'
                h = f'<div class="st" id="{i}" {pos}><span class="pm" style="{st}" data-layout-allow-overlap data-layout-allow-occlusion>{e["text"]}</span>{sub}</div>'
            else:
                h = f'<div class="st" id="{i}" {pos}><span class="c" style="{st}" data-layout-allow-overlap data-layout-allow-occlusion>{e["text"]}</span>{sub}</div>'
            (behind if e.get("behind") else front).append(h)
            js.append(f'soft("#{i} span", {t});' if th.get("premium") else f'stomp("#{i} span", {t}, {e.get("from", 2.0)});')
            if burst:
                js.append(f'tl.fromTo("#{i} .bu", {{opacity:0, scale:.2}}, {{opacity:.95, scale:1, duration:.22, ease:"back.out(2.5)"}}, {t + .03});')
            if e.get("sub"):
                js.append(f'tl.fromTo("#{i} i", {{opacity:0}}, {{opacity:1, duration:.2}}, {t + .25});')
        elif k == "kine":
            rows = []
            for row in e["lines"]:
                ws = []
                for j, wd in enumerate(row):
                    cls = " ".join(x for x in [wd.get("style", "fill"), "big" if wd.get("font") == "big" else ""] if x and x != "fill")
                    ws.append(f'<span class="kw {cls}" id="{i}w{len(rows)}_{j}" style="font-size:{wd.get("size", 180)}px" data-layout-allow-overlap data-layout-allow-occlusion>{wd["w"]}</span>')
                    wid = f"{i}w{len(rows)}_{j}"
                    js.append(f'tl.fromTo("#{wid}", {{opacity:0, scale:{wd.get("from", 2.3)}, filter:"blur(14px)"}}, {{opacity:1, scale:1, filter:"blur(0px)", duration:.14, ease:"power4.out"}}, {wd["t"]});')
                    js.append(f'tl.fromTo("#{wid}", {{scaleX:1.1, scaleY:.82}}, {{scaleX:1, scaleY:1, duration:.2, ease:"back.out(3)", immediateRender:false}}, {wd["t"] + .14});')
                    if wd.get("hit"):
                        js.append(f'shake({wd["t"]}, {wd.get("amt", .8)});')
                rows.append('<div class="kr">' + "".join(ws) + "</div>")
            h = f'<div class="kn" id="{i}" style="left:{e["x"]}px;top:{e["y"]}px">' + "".join(rows) + "</div>"
            (behind if e.get("behind") else front).append(h)
            js.append(f'tl.set("#{i}", {{xPercent:-50, yPercent:-50}}, 0);')
            if end is not None:
                dx, dy = {"up": (0, -160), "down": (0, 160), "left": (-260, 0), "right": (260, 0)}.get(e.get("exit", "up"), (0, -160))
                js.append(f'tl.to("#{i}", {{x:{dx}, y:{dy}, opacity:0, duration:.2, ease:"power2.in"}}, {end - .2});')
                end = None
        elif k == "tape":
            al = e.get("align", "r")
            rows = []
            for j, ln in enumerate(e["lines"]):
                lid = f"{i}t{j}"
                cls = " ".join(x for x in [ln.get("style", "ink"), "w7" if ln.get("w") == 700 else "", "big" if ln.get("font") == "big" else ""] if x)
                rows.append(f'<span class="tl {cls}" id="{lid}" style="font-size:{ln.get("size", 64)}px;transform:rotate({ln.get("rot", e.get("rot", -2))}deg)"><b>{ln["text"]}</b></span>')
                lt = ln.get("t", t + j * .18)
                js.append(f'tl.fromTo("#{lid}", {{clipPath:"inset(0 0 0 100%)"}}, {{clipPath:"inset(0 0 0 0%)", duration:.28, ease:"expo.out"}}, {lt});')
                js.append(f'tl.fromTo("#{lid} b", {{opacity:0, scale:1.35}}, {{opacity:1, scale:1, duration:.18, ease:"power4.out"}}, {lt + .12});')
                if ln.get("hit"):
                    js.append(f'shake({lt + .12}, .5);')
            anchor = {"r": "left:auto;right:%dpx" % (1920 - e["x"]), "l": "left:%dpx" % e["x"], "c": "left:%dpx" % e["x"]}[al]
            front.append(f'<div class="tp al-{al}" id="{i}" style="{anchor};top:{e["y"]}px">' + "".join(rows) + "</div>")
            if al == "c":
                js.append(f'tl.set("#{i}", {{xPercent:-50}}, 0);')
            if e.get("scrim"):
                js.append(f'tl.to("#scrim", {{opacity:1, duration:.4}}, {t - .1});')
        elif k == "punch":
            for pt in e["times"]:
                amt = e.get("amt", 1.1)
                js.append(f'tl.fromTo(["#plate", "#matte"], {{scale:{amt}}}, {{scale:1, duration:{e.get("dur", .35)}, ease:"power3.out", immediateRender:false}}, {pt});')
            i = None
        elif k == "flash":
            bg = e.get("bg", "var(--acc)")
            col = e.get("color", "var(--tacc)")
            import re as _re
            fdir = "rtl" if _re.search(r"[֐-׿]", e["text"]) else "ltr"
            front.append(f'<div class="fc" id="{i}" style="background:{bg}"><span style="direction:{fdir};font-size:{e.get("size", 520)}px;color:{col};transform:rotate({e.get("rot", -4)}deg)" data-layout-allow-overlap>{e["text"]}</span></div>')
            js.append(f'tl.set("#{i}", {{opacity:1}}, {t}); tl.set("#{i}", {{opacity:0}}, {t + e.get("dur", .16)});')
            js.append(f'tl.fromTo("#{i} span", {{scale:1.25}}, {{scale:1, duration:{e.get("dur", .16)}, ease:"none"}}, {t});')
            e["_noshow"] = True
        elif k == "captions":
            words = e["words"]  # [{w, t}] from word_times.py
            groups, cur = [], []
            for wi_, wd in enumerate(words):
                cur.append(wd)
                glue = wd["w"].strip().replace(".", "").replace(",", "").isdigit() and wi_ + 1 < len(words)
                if not glue and (len(cur) >= e.get("max", 3) or wd["w"].endswith((".", ",", "?", "!"))):
                    groups.append(cur); cur = []
            if cur:
                groups.append(cur)
            gh = []
            for gi, g in enumerate(groups):
                gid = f"{i}g{gi}"
                ws = "".join(f'<span class="cw" id="{gid}w{wi}">{wd["w"]}</span>' for wi, wd in enumerate(g))
                gh.append(f'<div class="cg" id="{gid}">{ws}</div>')
                g_end = min(groups[gi + 1][0]["t"] - .02 if gi + 1 < len(groups) else 999, g[-1]["t"] + 1.0, e.get("end", 999))
                js.append(f'tl.set("#{gid}", {{opacity:1}}, {g[0]["t"]}); tl.set("#{gid}", {{opacity:0}}, {g_end});')
                js.append(f'tl.fromTo("#{gid}", {{y:30, scale:.9}}, {{y:0, scale:1, duration:.14, ease:"back.out(2.5)", immediateRender:false}}, {g[0]["t"]});')
                for wi, wd in enumerate(g):
                    nxt = g[wi + 1]["t"] if wi + 1 < len(g) else g_end
                    js.append(f'tl.set("#{gid}w{wi}", {{className:"cw on"}}, {wd["t"]}); tl.set("#{gid}w{wi}", {{className:"cw"}}, {nxt});')
                    js.append(f'tl.fromTo("#{gid}w{wi}", {{scale:1.28}}, {{scale:1, duration:.16, ease:"back.out(3)", immediateRender:false}}, {wd["t"]});')
            front.append('<div id="cap">' + "".join(gh) + "</div>")
            i = "cap"
        elif k == "tag":
            ntag += 1
            front.append(f'<div class="tg gl {e.get("side", "r")}" id="{i}" data-follow="{e["follow"]}" data-anchor="{e.get("anchor", "r")}" '
                         f'data-dx="{e.get("dx", 24)}" data-dy="{e.get("dy", 0)}"><span class="n">{ntag:02d}</span><span class="a">{e["title"]}</span>'
                         + (f'<span class="b">{e["sub"]}</span>' if e.get("sub") else "") + '<span class="u"></span></div>')
            js.append(f'tl.fromTo("#{i}", {{opacity:0, clipPath:"inset(0 100% 0 0)"}}, {{opacity:1, clipPath:"inset(0 0% 0 0)", duration:.35, ease:"expo.out"}}, {t});')
            js.append(f'tl.fromTo("#{i} .u", {{scaleX:0}}, {{scaleX:1, duration:.45, ease:"power3.out"}}, {t + .15});')
        elif k == "box":
            lb = f'<span class="lb">{e["label"]}</span>' if e.get("label") else ""
            front.append(f'<div class="bx" id="{i}" data-box="{e["obj"]}" data-pad="{e.get("pad", 14)}">{BRK}'
                         f'<i class="xh x1"></i><i class="xh x2"></i><i class="xh x3"></i><i class="xh x4"></i>{lb}</div>')
            js.append(f'tl.fromTo("#{i} .brk", {{opacity:0, scale:1.5}}, {{opacity:1, scale:1, duration:.3, ease:"power3.out"}}, {t});')
            js.append(f'tl.fromTo("#{i} .xh", {{opacity:0}}, {{opacity:1, duration:.2, stagger:.04}}, {t + .15});')
        elif k == "callout":
            front.append(f'<div class="co gl" id="{i}" style="left:{e["x"]}px;top:{e["y"]}px"><span class="a">{e["title"]}</span>'
                         + (f'<span class="b">{e["sub"]}</span>' if e.get("sub") else "") + "</div>")
            lines.append(f'<path id="{i}L" fill="none" stroke="{p["lt"]}" stroke-width="2.5"/><circle id="{i}R" r="16" fill="none" stroke="{p["acc"]}" stroke-width="2" cx="-50" cy="-50"/>'
                         f'<circle id="{i}D" r="8" fill="{p["acc"]}" stroke="{p["lt"]}" stroke-width="2.5" cx="-50" cy="-50"/>')
            js.append(f'tl.fromTo("#{i}", {{opacity:0, y:14, clipPath:"inset(0 0 100% 0)"}}, {{opacity:1, y:0, clipPath:"inset(0 0 0% 0)", duration:.35, ease:"expo.out"}}, {t});')
        elif k == "counter":
            front.append(f'<div class="ct gl" id="{i}" style="left:{e["x"]}px;top:{e["y"]}px"><span class="v" id="{i}V" style="font-size:{e.get("size", 160)}px">'
                         f'{e.get("pre", "")}{e["a"]}{e.get("suf", "")}</span>' + (f'<span class="u">{e["label"]}</span>' if e.get("label") else "")
                         + f'<i class="pb"><b id="{i}P"></b></i></div>')
            js.append(f'stomp("#{i}", {t}, 1.5);')
        elif k == "ring":
            r = e.get("r", 180)
            ticks = "".join(f'<line x1="0" y1="-{r + 44}" x2="0" y2="-{r + (56 if j % 6 == 0 else 50)}" transform="rotate({j * 10})"/>' for j in range(36))
            sz = 2 * r + 140
            front.append(f'<div class="rg" id="{i}" data-follow="{e["obj"]}" data-anchor="c"><svg width="{sz}" height="{sz}" viewBox="{-sz // 2} {-sz // 2} {sz} {sz}" '
                         f'style="position:absolute;left:{-sz // 2}px;top:{-sz // 2}px">'
                         f'<g id="{i}A"><circle r="{r}" fill="none" stroke="{p["lt"]}" stroke-width="3" stroke-dasharray="44 18"/></g>'
                         f'<g id="{i}B"><circle r="{r + 24}" fill="none" stroke="{p["acc"]}" stroke-width="2" stroke-dasharray="4 10"/>'
                         f'<path d="M{r + 24},0 A{r + 24},{r + 24} 0 0 1 0,{r + 24}" fill="none" stroke="{p["acc"]}" stroke-width="5"/></g>'
                         f'<g id="{i}C" stroke="{p["lt"]}" stroke-width="2" opacity=".55">{ticks}</g></svg></div>')
            js.append(f'tl.fromTo("#{i} svg", {{opacity:0, scale:1.6}}, {{opacity:1, scale:1, duration:.35, ease:"expo.out"}}, {t});')
        elif k == "chip":
            i = "chip"
            front.append(f'<div id="chip" class="gl"><span class="b">{e.get("sub", "")}</span><span class="a">{e["text"]}</span></div>')
            js.append(f'tl.fromTo("#chip", {{opacity:0, x:-20}}, {{opacity:1, x:0, duration:.35, ease:"power3.out"}}, {t});')
        elif k == "lockup" and e.get("look", "tape" if th.get("rtl") and (not th.get("premium") or "#lockA" in spec.get("css", "")) else "plain") == "tape":
            # Hebrew tape lock (Karantina strips). Premium themes keep the restrained one-line lock unless the spec styles #lockA
            i = "lock"
            rows = [f'<span class="tl ink big" id="lockA" style="font-size:{e.get("size", 118)}px;transform:rotate(-2deg)"><b>{e["brand"]}</b></span>']
            if e.get("line"):
                rows.append(f'<span class="tl acc" id="lockB" style="font-size:{e.get("line_size", 58)}px;transform:rotate(-2deg)"><b>{e["line"]}</b></span>')
            front.append('<div class="tp al-r" id="lock" style="left:auto;right:96px;top:auto;bottom:118px">' + "".join(rows) + "</div>")
            js.append(f'tl.to("#scrim", {{opacity:1, duration:.4}}, {t - .1});')
            if any(x["type"] == "meter" for x in els):
                js.append(f'tl.to("#meter", {{opacity:0, duration:.2}}, {t - .2});')
            js.append(f'tl.fromTo("#lockA", {{clipPath:"inset(0 0 0 100%)"}}, {{clipPath:"inset(0 0 0 0%)", duration:.3, ease:"expo.out"}}, {t});')
            js.append(f'tl.fromTo("#lockA b", {{opacity:0, scale:1.3}}, {{opacity:1, scale:1, duration:.18, ease:"power4.out"}}, {t + .03});')   # word lands with the strip: never an empty bar
            js.append(f'shake({t + .12}, .45);')
            if e.get("line"):
                js.append(f'tl.fromTo("#lockB", {{clipPath:"inset(0 0 0 100%)"}}, {{clipPath:"inset(0 0 0 0%)", duration:.3, ease:"expo.out"}}, {t + .3});')
                js.append(f'tl.fromTo("#lockB b", {{opacity:0, scale:1.3}}, {{opacity:1, scale:1, duration:.18, ease:"power4.out"}}, {t + .33});')
        elif k == "lockup":
            i = "lock"
            front.append(f'<div id="lock" class="gl"><span class="a">{e["brand"]}</span>' + (f'<span class="s"></span><span class="b">{e["line"]}</span>' if e.get("line") else "") + "</div>")
            js.append(f'stomp("#lock", {t}, 1.4);')
        elif k == "meter":
            i = "meter"
            front.append(f'<div id="meter" class="gl"><span class="k">{e["label"]}</span><div class="w">' + "<b></b>" * 24 + "</div></div>")
            js.append(f'tl.fromTo("#meter", {{opacity:0, y:16}}, {{opacity:1, y:0, duration:.3}}, {t});')
        e["_id"] = i
        if i is None or e.get("_noshow"):
            continue
        hide.append(i)
        if end is not None:
            js.append(f'tl.to("#{i}", {{opacity:0, duration:.12}}, {end - .12});')
    behind += [spec.get("html_behind", "")]
    front += [spec.get("html_front", "")]
    js.append(spec.get("js", ""))
    has_matte = any(e.get("behind") for e in els) or bool(spec.get("html_behind"))
    wm = '<img id="wm" src="assets/watermark.png" alt="">' if spec.get("watermark") else ""  # optional brand mark
    hud = ("<div id=\"stage\">" + "".join(behind) + "</div>\n<!--MATTE-->\n" if has_matte else "<div id=\"stage\"></div>") + \
          "<div id=\"scrim\"></div><div id=\"stage2\"><svg id=\"lines\" viewBox=\"0 0 1920 1080\">" + "".join(lines) + "</svg>" + "".join(front) + "</div>" + wm + "<div id=\"flash\"></div>"
    env = spec.get("env")
    live = []
    for e in els:
        i = e["_id"]
        if e["type"] == "callout":
            fx, fy = e.get("fx", .5), e.get("fy", .5)
            cy, left = e["y"] + 34, e["x"] > 960
            cx = e["x"] if left else e["x"] + 400
            live.append(f'''{{const b=boxAt("{e["obj"]}",t),L=document.getElementById("{i}L"),D=document.getElementById("{i}D"),Rr=document.getElementById("{i}R");
  if(b&&t>={e.get("t", 0)}&&t<{e.get("end", 999)}){{const px=b[0]+(b[2]-b[0])*{fx},py=b[1]+(b[3]-b[1])*{fy};
  L.setAttribute("d",`M${{px}},${{py}} L${{{cx}+({cx}>px?-60:60)}},{cy} L{cx},{cy}`);D.setAttribute("cx",px);D.setAttribute("cy",py);
  Rr.setAttribute("cx",px);Rr.setAttribute("cy",py);Rr.setAttribute("r",12+10*((t*1.6)%1));Rr.setAttribute("opacity",1-((t*1.6)%1));}}
  else{{L.setAttribute("d","");D.setAttribute("cx",-50);Rr.setAttribute("cx",-50);}}}}''')
        if e["type"] == "counter":
            # keep the panel inside the 5% safe frame at its FINAL width (a wider suffix like ש״ח must not run off the edge)
            fin = f'{e.get("pre", "")}{e["b"]:,.{e.get("dec", 0)}f}{e.get("suf", "")}'
            live.append(f'''{{const u=Math.max(0,Math.min(1,(t-{e["t0"]})/({e["t1"]}-{e["t0"]}))),w=1-Math.pow(1-u,3),v={e["a"]}+({e["b"]}-{e["a"]})*w;
  document.getElementById("{i}V").textContent="{e.get("pre", "")}"+v.toFixed({e.get("dec", 0)}).replace(/\\B(?=(\\d{{3}})+(?!\\d))/g,",")+"{e.get("suf", "")}";
  document.getElementById("{i}P").style.transform=`scaleX(${{w}})`;
  const C=document.getElementById("{i}"),V=document.getElementById("{i}V");
  if(!C.dataset.fx&&document.fonts.status==="loaded"){{const s=V.textContent;V.textContent={json.dumps(fin, ensure_ascii=False)};
    const over=C.offsetLeft+C.offsetWidth-1824;if(over>0)C.style.left=(C.offsetLeft-over)+"px";C.dataset.fx=1;V.textContent=s;}}}}''')
        if e["type"] == "ring":
            sp = e.get("spin", 1)
            live.append(f'document.getElementById("{i}A").setAttribute("transform",`rotate(${{t*160*{sp}}})`);'
                        f'document.getElementById("{i}B").setAttribute("transform",`rotate(${{-t*110*{sp}}})`);'
                        f'document.getElementById("{i}C").setAttribute("transform",`rotate(${{t*25*{sp}}})`);')
        if e["type"] == "meter" and env:
            live.append('{const ev=ENV[Math.max(0,Math.min(ENV.length-1,Math.round(t*24)))]||0;'
                        'document.querySelectorAll("#meter .w b").forEach((b,k)=>{b.style.height=(4+38*ev*(.35+.65*Math.abs(Math.sin(k*1.7+t*7))))+"px";});}')
    jsall = ("const ENV = " + json.dumps(env) + ";\n" if env else "") + "window.onPlace = (t) => {\n" + "\n".join(live) + "\n};\n" + r"""
function shake(at, amt = 1) {
  tl.to(["#stage", "#stage2"], {keyframes: [{x: -12 * amt, y: 5 * amt, duration: .04}, {x: 9 * amt, y: -4 * amt, duration: .04}, {x: -5 * amt, y: 2 * amt, duration: .04}, {x: 0, y: 0, duration: .06}], ease: "none"}, at);
  tl.fromTo("#flash", {opacity: .3 * amt}, {opacity: 0, duration: .14}, at);
}
function soft(sel, at) { tl.fromTo(sel, {opacity: 0, scale: 1.12, y: 16}, {opacity: 1, scale: 1, y: 0, duration: .6, ease: "expo.out"}, at); shake(at, .25); }
function stomp(sel, at, from = 2) { tl.fromTo(sel, {opacity: 0, scale: from}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, at); shake(at); }
if (document.querySelector("#wm")) tl.fromTo("#wm", {opacity: 0}, {opacity: .92, duration: .6}, .2);
""" + "tl.set([" + ",".join(f'"#{h}"' for h in hide) + "], {opacity: 0}, 0);\n" + \
        "\n".join(f'tl.set("#{e["_id"]}", {{opacity: 1}}, {max(0, e.get("t", 0) - .01)});' for e in els if e.get("_id") and not e.get("_noshow")) + "\n" + "\n".join(js)
    faces, extra = font_faces(th)
    for fam, stems in spec.get("fonts", {}).items():   # bespoke fonts: {"Family": [(stem, weight, style), ...]} files in the fonts dir (paths.fonts())
        for stem, w, st in stems:
            faces += f'@font-face{{font-family:"{fam}";font-weight:{w};font-style:{st};src:url(assets/fonts/{stem}.woff2) format("woff2")}}'
            extra[f"fonts/{stem}.woff2"] = paths.fonts() / f"{stem}.woff2"
    for name, src in spec.get("assets", {}).items():    # bespoke images/files -> assets/<name>
        extra[name] = Path(src)
    R = paths.root()
    if spec.get("watermark"):
        extra["watermark.png"] = Path(spec["watermark"])
    if has_matte:
        extra["matte.webm"] = Path(spec.get("matte") or R / f"mattes/{ad}_alpha.webm")
    thump = ("soft_thump", "Deep soft round sub thump, clean and warm, subtle impact, no whoosh, no noise, no distortion", 0.6)
    # music bed + voiceover are plain files (make them with music.py / vo_take2.py); skipped when absent
    cache = paths.sfx_cache()
    music = Path(spec.get("music") or cache / f"{ad}_music.mp3")
    vo = Path(spec.get("vo") or cache / f'{spec.get("vo_name", f"{ad}_vo")}.mp3')
    sfx = [(str(f), "", 30, 0.0, v) for f, v in ((music, spec.get("music_vol", .5)), (vo, 1.0)) if f.exists()]
    if spec.get("thumps", True):   # a soft sub thump under every stomp / counter / lockup / kinetic hit (ElevenLabs SFX, cached)
        sfx += [(*thump, e["t"], .45) for e in els if e["type"] in ("stomp", "counter", "lockup")]
        sfx += [(*thump, wd["t"], .55) for e in els if e["type"] == "kine" for row in e["lines"] for wd in row if wd.get("hit")]
    css_all = faces + css_for(p, th) + spec.get("css", "")
    blob = css_all + hud + json.dumps(spec.get("elements", []), ensure_ascii=False)
    if th.get("rtl") or spec.get("he_fonts") or any("֐" <= ch <= "׿" for ch in blob):
        css_all, hud, jsall = he_remap(css_all, hud, jsall, extra, {**HE_REMAP, **spec.get("he_fonts", {})})
        # none of the three Hebrew faces has a shekel sign (Chrome falls back to a stray face): write it out
        hud, jsall = (x.replace("₪", "ש״ח") for x in (hud, jsall))
    return dict(project=R / f"videos/{ad.lower().replace('_', '-')}{spec.get('project_suffix', '')}", clip=Path(spec.get("clip") or R / f"clips/{ad}_720p.mp4"),
                track=Path(spec.get("track") or R / f"tracks/{ad}_vtrack.json"), css=css_all, hud=hud, js=jsall, sfx=sfx,
                plate_vol=spec.get("plate_vol", .4), extra=extra)
