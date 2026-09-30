"""The style catalog as a database: every hub style with its number, look, use cases, fonts, samples, plate contract
and how to build it. The hub (catalog/index.html) is the visual face; references/catalog.json is the same data for
Claude.

    python catalog.py build                          # regenerate references/catalog.json from the hub + plates.json
    python catalog.py list [--tag hebrew] [--q news] # search: id / number / one-liner / tags / fonts
    python catalog.py show 43 | BREAKING-NEWS        # one style card, including samples and the shooting requirements
    python catalog.py brief 43 "context..."          # the build brief: style + the user's project context + commands

Numbers are stable (#01..#61...): never renumbered, new styles are appended.
"""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
SKILL = Path(__file__).resolve().parent.parent
HUB = "https://ai-video-titles-guyaga.netlify.app"
DB = SKILL / "references" / "catalog.json"


def hub_data():
    """Evaluate the hub's data block (from `const RENDERS` to `/*END N20*/`) with node and return it as JSON."""
    html = (SKILL / "catalog" / "index.html").read_text(encoding="utf-8")
    a = html.index("const RENDERS")
    end = html.find("/*END N20*/")
    b = end if end > 0 else html.index("const $ =")
    js = html[a:b] + "\nprocess.stdout.write(JSON.stringify({S, NUM, FAMS, MAIN, MORE, SHOOT: typeof SHOOT === 'undefined' ? {} : SHOOT," \
                      " names: Object.fromEntries(RENDERS.map(r => [r, label(r)]))}));"
    r = subprocess.run(["node", "-"], input=js, capture_output=True, text=True, encoding="utf-8")  # stdin: Windows caps argv length
    if r.returncode:
        sys.exit("could not read the hub data block:\n" + r.stderr[-1500:])
    return json.loads(r.stdout)


def runner_of(sid):
    rs = (SKILL / "scripts" / "run_style.py").read_text(encoding="utf-8")
    block = rs[rs.index("STYLES"):rs.index("}", rs.index("STYLES"))]
    if f'"{sid}"' in block:
        return "run_style"
    for m in re.finditer(r'"([A-Z0-9-]+)"', rs[rs.index("}", rs.index("STYLES")):]):
        if m.group(1) == sid:
            return "run_ad"
    return "bespoke"


# styles that are built through another style's builder or an adkit example, not a module of their own
SX = "examples/E6_sneaker_sx.py"
OVERRIDE = {
    "HUD-CLEAN": ("run_style", "python scripts/run_style.py HUD-HELMET --spec <spec.json> --render  (leave out the reticle, radar and voice blocks)", "examples/hud-helmet"),
    "STICKER-POP": ("run_style", "python scripts/run_style.py STOMP-ESCORT --spec <spec.json> --render  (word style: white fill + ink stroke + hard shadow)", "examples/stomp-escort"),
    "STOMP-SX": ("run_ad", "python scripts/run_ad.py <AD> --spec <spec.py> --render", SX),
    "TRACKED-TAGS": ("run_ad", "python scripts/run_ad.py <AD> --spec <spec.py> --render  (keep only tag / callout / counter elements)", SX),
    "COMIC-POP": ("run_ad", "python scripts/run_ad.py <AD> --spec <spec.py> --render  (theme flag pop on the big stomp words only)", SX),
    "KINETIC-HE": ("run_ad", None, SX), "KINETIC-KARAOKE": ("run_ad", None, SX), "FLASH-CARD": ("run_ad", None, SX),
    "TAPE-HE": ("run_ad", None, "examples/E4_fire_hk.py"), "PRESIDENTIAL-SERIF": ("run_ad", None, SX),
    "STOMP-BEHIND": ("run_ad", None, SX), "GLASS-CALLOUT": ("run_ad", None, SX),
    "ARCH-DRAWING": ("bespoke", None, "examples/E8_tower_bespoke.py"),
}


def cmd_build(_):
    d = hub_data()
    plates = json.loads((SKILL / "references" / "plates.json").read_text(encoding="utf-8"))
    fams = {f[0]: f[1] for f in d["FAMS"]}
    styles = []
    for s in d["S"]:
        sid = s["id"]
        main = d["MAIN"].get(sid)
        renders = [r for r in [main, *d["MORE"].get(sid, [])] if r]
        ex = SKILL / "examples" / sid.lower()
        runner = runner_of(sid)
        o_run, o_how, o_ex = OVERRIDE.get(sid, (None, None, None))
        runner = o_run or runner
        how = o_how or {"run_style": f"python scripts/run_style.py {sid} --spec <spec.json> --render",
               "run_ad": "python scripts/run_ad.py <AD> --spec <spec.py> --render   (adkit spec; see examples/*_sx.py, *_hk.py)",
               "bespoke": "bespoke recipe: references/recipes/ (rewrite for the new subject; see styles.md)"}[runner]
        example = o_ex or (str(ex.relative_to(SKILL)).replace("\\", "/") if ex.is_dir() else None)
        styles.append({
            "n": d["NUM"].get(sid), "id": sid, "family": fams.get(s.get("f"), s.get("f")), "one": s.get("one", ""),
            "tags": s.get("tags", []), "fonts": s.get("fonts", ""), "palette": s.get("pal", []), "sample": s.get("src", ""),
            "kling": bool(s.get("kling")), "prompt": s.get("p", ""), "shoot_it_like_this": d["SHOOT"].get(sid, ""),
            "plate_contract": plates.get(sid), "runner": runner, "build": how,
            "example": example,
            "preview": f"{HUB}/previews/{sid.lower()}.mp4",
            "renders": [{"label": d["names"].get(r, r), "url": f"{HUB}/full/{r}.mp4"} for r in renders],
        })
    styles.sort(key=lambda x: x["n"] or 999)
    DB.write_text(json.dumps({"hub": HUB, "count": len(styles), "styles": styles}, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"wrote {DB.relative_to(SKILL)}: {len(styles)} styles "
          f"({sum(s['runner'] == 'run_style' for s in styles)} run_style, {sum(s['runner'] == 'run_ad' for s in styles)} run_ad, "
          f"{sum(s['runner'] == 'bespoke' for s in styles)} bespoke)")


def db():
    if not DB.is_file():
        sys.exit("references/catalog.json missing: run `python scripts/catalog.py build`")
    return json.loads(DB.read_text(encoding="utf-8"))["styles"]


def find(key):
    k = key.strip().lstrip("#").upper()
    for s in db():
        if s["id"] == k or (k.isdigit() and s["n"] == int(k)):
            return s
    sys.exit(f"no style '{key}'. Try: python catalog.py list --q {key.lower()}")


def cmd_list(a):
    q = (a.q or "").lower()
    for s in db():
        if a.tag and a.tag.lower() not in [t.lower() for t in s["tags"]]:
            continue
        hay = " ".join([s["id"], s["one"], " ".join(s["tags"]), s["fonts"], s["family"]]).lower()
        if q and q not in hay:
            continue
        print(f"#{s['n']:02d}  {s['id']:<20} {s['family']:<22} {', '.join(s['tags'])}\n      {s['one']}")


def cmd_show(a):
    s = find(a.key)
    print(f"#{s['n']:02d} {s['id']}  ·  {s['family']}{'  ·  Kling sample' if s['kling'] else ''}\n{s['one']}\n")
    print(f"Use for:  {', '.join(s['tags'])}\nFonts:    {s['fonts']}\nPalette:  {' '.join(s['palette'])}")
    print(f"Shoot it: {s['shoot_it_like_this']}\nBuild:    {s['build']}\nExample:  {s['example']}")
    print(f"Watch:    {s['preview']}")
    for r in s["renders"]:
        print(f"          {r['label']}: {r['url']}")
    print(f"\nPrompt:   {s['prompt']}")


def cmd_brief(a):
    s = find(a.key)
    pc = s["plate_contract"] or {}
    print(f"""# Title brief · #{s['n']:02d} {s['id']}

## Project context (from the user)
{a.context}

## Style
{s['prompt']}
- Look: {s['one']}
- Fonts: {s['fonts']}  (Hebrew text: Suez One / Karantina / Secular One only; prices as ש״ח)
- Palette: {' '.join(s['palette'])}; swap to the project's brand colours if it has them
- Reference renders: {', '.join(r['url'] for r in s['renders'][:2])}

## The footage this style needs
{s['shoot_it_like_this']}
- Take: {pc.get('take', '?')} · framing: {pc.get('framing', '?')} · free space: {pc.get('negative_space', '?')}
- Gate: {pc.get('gate', '?')}
- No footage yet? Generate it with ai-ad-studio, which writes these shooting lines into the prompt: {pc.get('seedance_lines', [])}

## Build
1. Adapt `{s['example'] or 'references/recipes/ (bespoke: rewrite for this subject)'}` to the project: its words, prices, names, language, brand colours, the beat grid of its music.
2. {s['build']}
3. Check 4-6 frames yourself, then scripts/qa.py until "ship".""")


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("build").set_defaults(f=cmd_build)
    p = sub.add_parser("list"); p.add_argument("--tag"); p.add_argument("--q"); p.set_defaults(f=cmd_list)
    p = sub.add_parser("show"); p.add_argument("key"); p.set_defaults(f=cmd_show)
    p = sub.add_parser("brief"); p.add_argument("key"); p.add_argument("context"); p.set_defaults(f=cmd_brief)
    a = ap.parse_args()
    a.f(a)


if __name__ == "__main__":
    main()
