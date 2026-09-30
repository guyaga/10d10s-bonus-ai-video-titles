"""Shared helpers for the catalog style builders (scripts/styles/*.py).

A style builder is `build(spec: dict, base: Path) -> dict(project, clip, track, css, hud, js, sfx, plate_vol, extra)`,
the exact keyword set shotkit.build() takes. `base` is the folder relative paths in the spec resolve against
(the spec file's folder). Composition space is 1920x1080; track files must be in that canvas (vtrack.py default).
"""
import html
import json
from pathlib import Path

import adkit
import paths

# ---- sound: bundled library (assets/sfx/<name>.mp3), generated with ElevenLabs only if missing ----------------------
SFX = {
    "ui_whoosh": ("Clean cinematic UI whoosh swelling in, airy, modern tech interface, no music", 1.2),
    "ui_tick": ("Fast soft digital typing ticks for text appearing on screen, subtle futuristic UI", 1.0),
    "ui_pop": ("Single short soft digital pop, glassy click with small bubbly tail, UI sound", 0.6),
    "chime": ("Warm soft arrival chime, two gentle bell tones, positive, clean UI notification", 1.2),
    "logo_hit": ("Soft cinematic logo reveal: low thump followed by a bright airy shimmer, elegant", 1.8),
    "hud_boot": ("Sci-fi helmet HUD booting up, rising electronic sweep with small digital chirps, clean", 1.6),
    "data_chatter": ("Quiet fast computer data chatter, tiny electronic blips and clicks, sci-fi interface", 2.0),
    "lock_tick": ("Short sharp electronic target-acquired tick, sci-fi, clean", 0.5),
    "bass_pulse": ("Deep low cinematic bass pulse, single hit, tense sci-fi", 1.5),
    "heartbeat": ("Muffled heartbeat inside a helmet speeding up from calm to fast, tense", 5.0),
    "warn_beep": ("Urgent sci-fi warning double beep, two short high electronic alarm tones", 0.8),
    "charge_up": ("Weapon system charging up, rising electric whine ending with a confident click, sci-fi", 1.6),
    "scan_beeps": ("Targeting computer scanning, quick repeating electronic beeps accelerating, sci-fi", 2.0),
    "lock_tone": ("Missile lock-on tone, steady high electronic beep, sci-fi, clean", 1.0),
    "launch": ("Heavy mechanical launcher firing two rockets, metallic ka-chunk and whoosh", 1.2),
    "hit_confirm": ("Two quick electronic hit-confirm blips, satisfying, sci-fi HUD", 0.8),
    "stinger": ("Short triumphant sci-fi UI stinger, bright synth hit with shimmer tail", 1.6),
    "glass_ting": ("Delicate soft glass ting, AR smart-glasses notification, airy and clean", 0.7),
    "ar_whoosh": ("Very soft airy UI whoosh for an AR label sliding in, subtle", 0.8),
    "rec_beep": ("Single short studio record-start beep, clean", 0.5),
    "mic_click": ("Soft microphone check tick, subtle", 0.5),
    "soft_thump": ("Deep soft round sub thump, clean and warm, subtle impact, no whoosh, no noise, no distortion", 0.6),
    "soft_click": ("Soft subtle clean click, quiet and elegant, like a camera shutter in the distance", 0.5),
    "soft_tick": ("Single soft clean clock tick, quiet, warm", 0.5),
    "soft_pulse": ("Short soft low electronic pulse beep, round and warm, not harsh", 0.5),
}


def cue(name, at, vol=0.8):
    p, secs = SFX[name]
    return (name, p, secs, round(float(at), 3), vol)


def audio_cues(spec, base, default_vol=.6):
    """Music bed / voiceover files from the spec: {"music": path, "music_vol": .6, "vo": path, "vo_vol": 1}."""
    out = []
    for key, vk, dv in (("music", "music_vol", default_vol), ("vo", "vo_vol", 1.0)):
        if spec.get(key):
            f = res(base, spec[key])
            if not f.exists():
                raise SystemExit(f"{key} file not found: {f}")
            out.append((str(f), key, 30, float(spec.get(key + "_at", 0)), spec.get(vk, dv)))
    return out


def scale_cues(cues, k):
    return [(n, p, s, at, round(v * k, 3)) for (n, p, s, at, v) in cues]


# ---- paths --------------------------------------------------------------------------------------------------------
def res(base, p):
    """Resolve a spec path: absolute, or relative to the spec's folder, or relative to the project root."""
    if p is None:
        return None
    p = Path(p)
    if p.is_absolute():
        return p
    for b in (Path(base), paths.root()):
        if (b / p).exists():
            return (b / p).resolve()
    return (Path(base) / p).resolve()


def project_dir(spec, style):
    return paths.root() / "videos" / spec.get("name", style.lower())


def tracks(spec, base):
    """The spec's track file(s). Styles that track nothing may omit "track": a frame clock is derived from the clip."""
    if not spec.get("track"):
        import subprocess
        clip = res(base, spec["clip"])
        d = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(clip)],
                                 capture_output=True, text=True).stdout.strip())
        n = int(round(d * 24))
        out = paths.root() / "tracks" / f"_{spec.get('name', 'clip')}_clock.json"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps({"fps": 24.0, "frames": n, "canvas": [1920, 1080], "objects": {}}), encoding="utf-8")
        return out
    t = spec["track"]
    return [res(base, x) for x in t] if isinstance(t, list) else res(base, t)


# ---- fonts --------------------------------------------------------------------------------------------------------
def fonts(*families):
    """@font-face css + {asset_path: file} for families in adkit.FAM (Hebrew/Latin subsets handled)."""
    css, files = "", {}
    for fam in dict.fromkeys(families):
        c, f = adkit.font_faces({"display": fam, "label": fam, "mono": fam, "tag": fam})
        css += c
        files.update(f)
    return css, files


# ---- markup helpers -----------------------------------------------------------------------------------------------
def e(s):
    return html.escape(str(s), quote=True)


def is_he(s):
    return any("֐" <= ch <= "׿" for ch in str(s))


def money(v, cur="$"):
    return f"{cur}{v:,.0f}" if cur in ("$", "€", "£") else f"{v:,.0f} {cur}"


def js(obj):
    return json.dumps(obj, ensure_ascii=False)


TICKS = '<div class="tick tk1"></div><div class="tick tk2"></div><div class="tick tk3"></div><div class="tick tk4"></div>'
BRK = '<div class="brk"><i></i><i></i><i></i><i></i></div>'

# stomp + shake: the social hit used by the stomp family (targets #stage/#stage2 when present, flashes #flash)
STOMP_JS = r"""
function shake(at, amt = 1) {
  const L = ["#stage", "#stage2"].filter(s => document.querySelector(s));
  if (L.length) tl.to(L, {keyframes: [{x: -14 * amt, y: 6 * amt, duration: .04}, {x: 11 * amt, y: -5 * amt, duration: .04}, {x: -6 * amt, y: 3 * amt, duration: .04}, {x: 0, y: 0, duration: .06}], ease: "none"}, at);
  if (document.querySelector("#flash")) tl.fromTo("#flash", {opacity: .4 * amt}, {opacity: 0, duration: .14, ease: "power2.out"}, at);
}
function stomp(sel, at, from = 1.9, amt = 1) {
  tl.fromTo(sel, {opacity: 0, scale: from}, {opacity: 1, scale: 1, duration: .16, ease: "power4.out"}, at);
  if (amt) shake(at, amt);
}
"""


def envelope(audio, fps=24):
    """Per-frame 0..1 loudness envelope of a voice file (drives HUD voice meters). Needs librosa."""
    import librosa
    import numpy as np
    y, sr = librosa.load(str(audio), sr=22050, mono=True)
    hop = int(sr / fps)
    rms = librosa.feature.rms(y=y, frame_length=hop * 2, hop_length=hop)[0]
    rms = rms / (np.percentile(rms, 98) + 1e-9)
    return [round(float(min(1, v)), 3) for v in rms]


# ---- Hebrew typography --------------------------------------------------------------------------------------------
# Hebrew titles use three Google faces only (Guy's system). Hebrew titles NEVER use Anton / Bodoni / any Latin-only face.
#   Suez One     serif display: premium, luxury, film, real estate
#   Karantina    condensed display: social stomp, sport, food, loud drops
#   Secular One  bold rounded-geometric: captions, HUD labels, tech, clean UI
# Pairings (display, weight, body/accent, weight):
HE_PAIRS = {
    "suez": ("Suez One", 400, "Secular One", 400),          # premium display + clean labels
    "karantina": ("Karantina", 700, "Secular One", 400),    # punchy social stomp + clean labels
    "secular": ("Secular One", 400, "Secular One", 400),    # captions, HUD, UI
    "karantina-suez": ("Karantina", 700, "Suez One", 400),  # condensed display + a Suez One accent word/line
}


def type_pair(spec, latin=("Oswald", 700, "Archivo", 400), default_pair="secular"):
    """Resolve the spec's typography. Returns dict(css, files, display, dw, body, bw, rtl, lang, dir).
    spec: "language": "he" | "en";  "pair": one of HE_PAIRS (Hebrew) ;  "fonts": {"display", "dw", "body", "bw"} (override)."""
    lang = spec.get("language", "en")
    rtl = lang == "he"
    if rtl:
        pair = spec.get("pair", default_pair)
        if pair not in HE_PAIRS:
            raise SystemExit(f"unknown Hebrew pair '{pair}'. Use one of: {', '.join(HE_PAIRS)}")
        d, dw, b, bw = HE_PAIRS[pair]
    else:
        d, dw, b, bw = latin
    f = spec.get("fonts", {})
    d, dw, b, bw = f.get("display", d), f.get("dw", dw), f.get("body", b), f.get("bw", bw)
    if rtl:
        for fam in (d, b):
            if not any("-hebrew-" in st for st, _, _ in adkit.FAM.get(fam, [])):
                raise SystemExit(f"'{fam}' has no Hebrew glyphs; Hebrew titles use Suez One, Karantina or Secular One (see HE_PAIRS)")
    css, files = fonts(d, b)
    return dict(css=css, files=files, display=d, dw=dw, body=b, bw=bw, rtl=rtl, lang=lang, dir="rtl" if rtl else "ltr")


def words(text):
    """Split a line into display words. A token made only of digits/%/./, is glued to the NEXT word
    ('6 שעות', '24 מ׳', '100 %') so numbers never stand alone on a caption or a stomp (adkit rule)."""
    toks = [t for t in str(text).split() if t]
    out, i = [], 0
    while i < len(toks):
        t = toks[i]
        core = t.strip(".,%₪$€")
        if core.replace(".", "").replace(",", "").isdigit() and i + 1 < len(toks):
            j = i + 1
            while j + 1 < len(toks) and not any(ch.isalpha() for ch in toks[j]):   # "100 % כותנה": glue the symbol too
                j += 1
            out.append(" ".join(toks[i:j + 1]))
            i = j + 1
        else:
            out.append(t)
            i += 1
    return out


# deterministic helpers for canvas / procedural styles: never Math.random, everything a pure function of t + seed
JS_UTIL = r"""
const mulberry32 = (a) => () => { a |= 0; a = a + 0x6D2B79F5 | 0; let t = Math.imul(a ^ a >>> 15, 1 | a); t = t + Math.imul(t ^ t >>> 7, 61 | t) ^ t; return ((t ^ t >>> 14) >>> 0) / 4294967296; };
const hash1 = (n) => { const x = Math.sin(n * 12.9898 + 78.233) * 43758.5453; return x - Math.floor(x); };
const clamp01 = (u) => Math.max(0, Math.min(1, u));
const easeOut3 = (u) => 1 - Math.pow(1 - clamp01(u), 3);
const easeInOut = (u) => { u = clamp01(u); return u < .5 ? 4 * u * u * u : 1 - Math.pow(-2 * u + 2, 3) / 2; };
"""
