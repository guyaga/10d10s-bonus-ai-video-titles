"""Source of truth for references/plates.json (the PLATE CONTRACT per style). python references/build_plates.py

Every number is derived from a plate that actually worked (prompts/seedance/*.txt + the renders' vtrack files):
  measured on the source plates: duration, hard cuts (ffmpeg scene > 0.15), and for the primary tracked object the
  fraction of frames it is found (coverage) and the free frame fraction beside it (min over the take).
Field meanings are documented in references/styles.md ("Plate contracts").
"""
import json
from pathlib import Path

CLEAN = "No text, no logos, no signage, no UI, no graphics at any time."


def P(take, max_cuts, dur, subject, framing, space, camera, track, lines, gate, separation=False, beats=False, source=""):
    side, frac = space
    return {"take": take, "max_cuts": max_cuts, "duration_s": dur, "aspect": "16:9", "subject": subject, "framing": framing,
            "negative_space": {"side": side, "min_frac": frac}, "camera": camera, "separation": separation, "track": track,
            "beats": beats, "text_in_frame": False, "seedance_lines": lines,
            "gate": {"max_cuts": gate[0], "min_track_coverage": gate[1], "min_free_margin": gate[2]}, "source": source}


RUNWAY_FORMAT = "FORMAT: One continuous shot, no cuts."
RUNWAY_CAMERA = ("CAMERA: Locked-off at the end of the runway at chest height with an extremely slow push-in. Her full body, head to boots, "
                 "stays inside the frame and centred at all times. FORBIDDEN: cuts, whip-pans, zoom punches, shake.")
RUNWAY_LOCK = "POSITIVE LOCKS: Exactly one model on the runway. Every garment stays identical to the first frame. " + CLEAN

PLATES = {
 # ---------------------------------------------------------------- social stomp family
 "STOMP-ESCORT": P("one-take", 0, [10, 30], "one model (or product carrier) whose full body stays in frame; every advertised item visible on her",
    "full body, centred, walks toward camera", ("both", .30), "locked-off or very slow push-in (or a dolly back matching her pace)",
    ["subject full body"],
    [RUNWAY_FORMAT, RUNWAY_CAMERA,
     "She stays in the centre third of the frame for the whole take; the left and right thirds show only runway and audience.",
     RUNWAY_LOCK], (0, .95, .28), beats=True, source="D2_full_runway_720p (30 s) / D1_runway_720p (10 s)"),
 "STOMP-BEHIND": P("one-take", 0, [8, 30], "one person with a clean, readable silhouette against a plain, evenly lit background",
    "full body, centred, walks toward camera; plain wall or backdrop behind the head and shoulders", ("both", .30),
    "slow dolly back matching the walk, or locked-off", ["subject full body"],
    [RUNWAY_FORMAT, RUNWAY_CAMERA.replace("Locked-off at the end of the runway", "Smooth steady dolly backwards").replace(" with an extremely slow push-in", " matching her walking speed"),
     "Behind her upper body there is only a plain, bright back wall: no people, no lights, no motion blur on her outline.",
     RUNWAY_LOCK], (0, .95, .28), separation=True, beats=True, source="D1_runway_720p (10 s) + matte"),
 "GLASS-CALLOUT": P("one-take", 0, [8, 30], "one model with every advertised item visible", "full body, centred, walks toward camera",
    ("both", .30), "slow dolly back matching the walk, or locked-off", ["subject full body", "each advertised item"],
    [RUNWAY_FORMAT, RUNWAY_CAMERA, "She stays in the centre third; the side thirds stay calm and uncluttered.", RUNWAY_LOCK],
    (0, .95, .28), beats=True, source="D1_runway_720p (10 s)"),
 "STICKER-POP": P("one-take", 0, [8, 30], "one model or product carrier, full body in frame, items visible", "full body, centred, walks toward camera",
    ("both", .30), "slow dolly back matching the walk, or locked-off", ["subject full body"],
    [RUNWAY_FORMAT, RUNWAY_CAMERA, "She stays in the centre third; the left and right thirds stay free.", RUNWAY_LOCK],
    (0, .95, .28), beats=True, source="D1_runway_720p (10 s)"),
 "COUNTDOWN-CTA": P("one-take", 0, [20, 30], "one model: walk, one spin, then holds poses for the last 15 seconds (the countdown runs over the hold)",
    "full body, centred; the last 15 s she stands in the centre facing camera", ("both", .30), "locked-off with an extremely slow push-in",
    ["subject full body"],
    [RUNWAY_FORMAT, RUNWAY_CAMERA,
     "Timeline: she walks the full runway toward camera, one full spin only at 12-15s, then holds poses in the centre until the end.",
     RUNWAY_LOCK], (0, .95, .28), beats=True, source="D2/D3 30 s runway takes"),
 "KINETIC-HE": P("cuts-ok", 5, [12, 24], "the product or hero, large and clear; one idea per shot", "subject centred, room above it",
    ("top", .25), "slow orbit or slow push; energy from subject motion, not camera", ["hero object"],
    ["FORMAT: One continuous shot, or hard cuts only at the timecodes listed and nowhere else.",
     "COMPOSITION: The subject stays in the centre and lower two thirds; the upper quarter of the frame is plain background (sky, wall, dark studio).",
     "CAMERA: slow, very smooth. FORBIDDEN: whip-pans, shake. " + CLEAN], (5, .6, .2), source="E6_sneaker_720p (15 s orbit)"),
 "TAPE-HE": P("cuts-ok", 5, [12, 24], "any story footage; one clear subject per shot", "subject off-centre or centred with a calm lower third",
    ("bottom", .25), "steady; cut-blocks welcome", ["subject per shot (optional, for tags)"],
    ["FORMAT: Timestamped cut-blocks. HARD CUTS exactly at the listed timecodes and nowhere else.",
     "COMPOSITION: Keep the lower third of every shot calm and low-detail: floor, table, dark area.",
     "CAMERA: steady. FORBIDDEN: whip-pans, shaky zooms. " + CLEAN], (5, .3, .2), source="E4_fire_720p (20 s, 4 planned cuts)"),
 "KINETIC-KARAOKE": P("cuts-ok", 5, [12, 24], "any footage that carries a voiceover", "subject in the upper two thirds",
    ("bottom", .22), "stabilised; punch-zooms are added in post", [],
    ["FORMAT: One continuous shot, or hard cuts only at the listed timecodes.",
     "COMPOSITION: Nothing important in the bottom fifth of the frame: captions sit there.",
     "CAMERA: stabilised, gentle. FORBIDDEN: cuts elsewhere, shake. " + CLEAN], (5, 0, .18), source="E9_glasses_720p (18 s POV)"),
 "FLASH-CARD": P("cuts-ok", 6, [6, 30], "any footage; the card replaces the frame for 4 frames", "any", ("none", 0),
    "any", [], ["FORMAT: Hard cuts allowed; mark the single biggest beat (the hit the card lands on) in the timeline.", "POSITIVE LOCKS: " + CLEAN],
    (6, 0, 0), beats=True, source="E3_car_720p (card on the braking beat)"),
 "STOMP-SX": P("cut-list", 5, [12, 20], "product or food hero shots, one idea per cut", "subject large, upper quarter free",
    ("top", .25), "energy from cuts and speed ramps", ["hero object per shot (optional)"],
    ["FORMAT: Timestamped cut-blocks. HARD CUTS exactly at the listed timecodes and nowhere else.",
     "COMPOSITION: The upper quarter of each shot stays plain (dark background, wall, steam).",
     "CAMERA: energy from subject motion, cuts and speed ramps. FORBIDDEN: whip-pans, shake. " + CLEAN],
    (5, .3, .2), source="E10_chef_720p (15 s, 4 cuts)"),
 "TRACKED-TAGS": P("cuts-ok", 4, [10, 20], "the product(s) and each labelled part clearly visible and distinct", "subject centred at medium size",
    ("both", .20), "slow orbit, slow glide or locked; no fast moves", ["each labelled object or part"],
    ["FORMAT: One continuous shot preferred; if cutting, HARD CUTS only at the listed timecodes.",
     "COMPOSITION: The product fills at most the centre 60 percent of the frame; plain background on both sides.",
     "CAMERA: slow and very smooth. FORBIDDEN: shake, whip-pans. POSITIVE LOCKS: every labelled part stays identical and visible. " + CLEAN],
    (4, .7, .18), source="E6_sneaker_720p / E7_gold_720p (2 cuts)"),
 "COMIC-POP": P("cuts-ok", 5, [10, 20], "any action footage with one or two big beats", "subject centred, upper area free on the beat shots",
    ("top", .25), "any smooth move", [], ["FORMAT: Hard cuts only at the listed timecodes.",
     "COMPOSITION: On the big-beat shots the upper quarter of the frame is plain.", "CAMERA: smooth. FORBIDDEN: shake. " + CLEAN],
    (5, 0, .2), beats=True, source="E3_car_720p"),
 "SPEED-STAT": P("cut-list", 4, [12, 18], "a measurable action in shots: approach, macro contact, object in flight, celebration",
    "one idea per shot: wide player, extreme close-up on the contact, the object crossing the frame, hero wide", ("left", .30),
    "energy from subject speed and speed ramps", ["athlete", "the object (ball)", "the contact point (boot)"],
    ["FORMAT: Timestamped cut-blocks. HARD CUTS exactly at 3.0s, 8.0s and 11.0s and nowhere else.",
     "CAMERA: energy from subject speed and speed ramps, not camera whips. FORBIDDEN: whip-pans, shaky zooms.",
     "POSITIVE LOCKS: Exactly one ball, exactly one kick. Plain kit with no logos, badges, sponsor text or numbers. " + CLEAN],
    (4, .4, .25), separation=True, source="E1_soccer_720p (15 s, 3 planned cuts)"),
 "PRESIDENTIAL-SERIF": P("cut-list", 6, [18, 30], "an epic story in shots with one hero and one opponent", "hero framed off-centre, sky or smoke above",
    ("top", .25), "cinematic, grounded; push-ins and tracking", ["hero", "opponent"],
    ["FORMAT: Timestamped cut-blocks. HARD CUTS exactly at the listed timecodes and nowhere else.",
     "COMPOSITION: Keep the upper quarter of the wide shots as sky, smoke or haze for the titles.",
     "CAMERA: Cinematic, energy from subject speed and hard cuts. FORBIDDEN: whip-pans, shaky cam.",
     "POSITIVE LOCKS: Exactly one hero and one opponent in focus. " + CLEAN], (6, .5, .2), source="E2_spartan_720p (24 s, 5 cuts)"),
 # ---------------------------------------------------------------- HUD / interface family
 "HUD-HELMET": P("one-take", 0, [15, 30], "one face inside a helmet behind a clear visor", "face close-up, eyes steady and centred, visor edges in frame",
    ("both", .22), "locked-off with a very slow continuous push-in", ["face", "eyes"],
    ["FORMAT: One continuous shot, no cuts.",
     "CAMERA: Locked-off extreme close-up with a very slow continuous push-in over the whole shot. FORBIDDEN: cuts, shake, rotation, zoom punches.",
     "The face stays in the centre third; the left and right quarters show only helmet interior and soft background bokeh.",
     "POSITIVE LOCKS: His face stays identical to the first frame. The visor glass stays completely clean: no displays, no graphics, no text, no UI at any time. Exactly one person."],
    (0, .95, .2), source="B4_helmet_long_720p (24 s)"),
 "HUD-CLEAN": P("one-take", 0, [6, 30], "one face inside a helmet behind a clear visor", "face close-up, eyes steady", ("both", .22),
    "locked-off with a very slight slow push-in", ["face", "eyes"],
    ["FORMAT: One continuous shot, no cuts.", "CAMERA: Locked-off with a very slight slow push-in. FORBIDDEN: shake, rotation, cuts.",
     "POSITIVE LOCKS: The visor glass stays completely clean: no displays, no graphics, no text, no UI at any time. His face stays identical to the first frame."],
    (0, .95, .2), source="B2 (6 s) / B4 (24 s)"),
 "SCIFI-TARGETING": P("one-take", 0, [6, 12], "first-person view: a counted set of targets (2-3) and the shooter's weapon in the foreground",
    "POV; targets spread across the middle, weapon in a lower corner", ("right", .25), "first-person, subtle natural head movement; one short blast shake allowed",
    ["each target", "weapon/launcher"],
    ["FORMAT: One continuous shot, no cuts.", "CAMERA: First-person, subtle natural head movement, one short blast shake at the impact. FORBIDDEN: whip-pans, cuts.",
     "POSITIVE LOCKS: Exactly two robots and one drone. Exactly two rockets, fired once. No text, no reticles, no UI, no logos at any time."],
    (0, .8, .2), source="B3_seedance_720p (8 s)"),
 "ROAD-HUD": P("cut-list", 4, [15, 20], "a driver's view of the road ahead with a hazard that appears, plus exterior and reaction shots",
    "windscreen POV with the road's vanishing point visible; the hazard enters from one side", ("bottom", .30),
    "smooth, steady; no shake", ["hazard (cyclist/pedestrian)", "driver", "car"],
    ["FORMAT: Timestamped cut-blocks. HARD CUTS exactly at the listed timecodes and nowhere else.",
     "COMPOSITION: In the driving shots the road surface ahead fills the lower third and its vanishing point stays visible.",
     "CAMERA: smooth, steady. FORBIDDEN: shaky cam, whip-pans.",
     "POSITIVE LOCKS: exactly one car, one driver, one hazard. The car never hits anything. " + CLEAN], (4, .6, .2), source="E3_car_720p (18 s)"),
 "THERMAL-RESCUE": P("cut-list", 5, [15, 24], "a search in darkness, smoke or fire, then a found person, then an exit to daylight",
    "mid shots and close-ups; the searched object (door, person) clearly readable as a shape", ("none", 0),
    "steady handheld feel, no shake", ["searcher", "door or target", "found person"],
    ["FORMAT: Timestamped cut-blocks. HARD CUTS exactly at the listed timecodes and nowhere else.",
     "LIGHTING: dark interiors lit mainly by fire, so the hottest areas are the brightest (the post filter maps luminance to heat).",
     "CAMERA: steady handheld feel, no shake. FORBIDDEN: whip-pans, zoom punches.",
     "POSITIVE LOCKS: exactly one rescuer and one person rescued. " + CLEAN], (5, .3, 0), source="E4_fire_720p (20 s)"),
 "SPEC-SCAN": P("one-take", 0, [10, 18], "one engineered product floating in a dark studio; its layers separate (exploded view) and rejoin",
    "product centred, fully in frame", ("both", .20), "slow smooth orbit", ["product", "each layer / part"],
    ["FORMAT: One continuous shot, no cuts.", "CAMERA: slow orbit, very smooth. FORBIDDEN: cuts, shake.",
     "Dark plain studio background with rim light so the product's outline is crisp.",
     "POSITIVE LOCKS: exactly one product, always the same design, the stated number of layers when separated. " + CLEAN],
    (0, .9, .18), separation=True, source="E6_sneaker_720p (15 s)"),
 "MAP-FLYOVER": P("one-take", 0, [8, 12], "an aerial over a city/region where every pinned place is visible from the first frame",
    "high aerial, landmarks spread across the frame, horizon or sea as a fixed reference", ("left", .30),
    "smooth drone, constant slow forward push and slight descent; no rotation", ["landmark points (planar, track.py)"],
    ["FORMAT: One continuous shot, no cuts.",
     "CAMERA: Smooth stabilized drone, constant slow speed, gentle forward push and slight descent only. FORBIDDEN: whip-pans, rotation, roll, zoom punches, shake, cuts.",
     "POSITIVE LOCKS: No text, no labels, no map graphics, no UI, no logos appear at any time. The geography stays fixed for the whole shot."],
    (0, 1.0, .25), source="A1_seedance_720p (10 s)"),
 "CAMPUS-AR": P("one-take", 0, [5, 10], "one person walking through a real place; the labelled features (shelves, desks, a skylight) stay visible",
    "medium-wide, person centred, walking toward camera", ("both", .25), "slow steady dolly backwards at chest height matching the walk",
    ["person/head", "each labelled place"],
    ["FORMAT: One continuous shot, no cuts.", "CAMERA: Slow steady dolly backwards at chest height matching his pace. FORBIDDEN: whip-pans, zooms, shake, cuts.",
     "POSITIVE LOCKS: Exactly one person. The room layout stays identical to the first frame. No text, no signs, no UI, no logos."],
    (0, .9, .22), source="C1_seedance_720p (6 s)"),
 "CYBER-DOSSIER": P("one-take", 0, [5, 10], "one character walking toward camera in their setting", "full body, centred, walks toward camera",
    ("both", .35), "low slow dolly backwards matching the walk", ["character", "head"],
    ["FORMAT: One continuous shot, no cuts.", "CAMERA: Low camera at waist height, slow steady dolly backwards matching his pace. FORBIDDEN: whip-pans, rotation, zooms, cuts.",
     "POSITIVE LOCKS: The character's look stays identical to the first frame. No text, no holograms, no UI, no logos appear at any time."],
    (0, .95, .3), source="B1_seedance_720p (6 s)"),
 "ARRIVAL-CARD": P("one-take", 0, [5, 10], "one person arriving in front of the destination (building, entrance)",
    "person walks toward camera, destination facade behind with a blank area for the logo", ("left", .35),
    "slow steady dolly backwards at chest height matching the walk", ["head", "blank facade area"],
    ["FORMAT: One continuous shot, no cuts.", "CAMERA: Slow steady dolly backwards at chest height, matching his walking speed so he stays the same size in frame. FORBIDDEN: whip-pans, zooms, shake, cuts.",
     "POSITIVE LOCKS: Exactly one person in focus. No text, no signs with readable letters, no logos, no UI appear at any time."],
    (0, .95, .3), source="A2_seedance_720p (6 s)"),
 # ---------------------------------------------------------------- crafted worlds
 "HALLMARK-LUXE": P("cuts-ok", 2, [10, 15], "jewellery worn on a hand/wrist on a dark ground, each piece in turn", "macro; the featured piece on one side of the frame",
    ("right", .40), "slow macro glide", ["each piece (watch, bracelet, rings)"],
    ["FORMAT: One continuous shot, or at most two soft cuts between pieces.", "CAMERA: slow macro glide. FORBIDDEN: shake, fast moves.",
     "LIGHTING: a single spotlight on the piece over black velvet; the rest of the frame falls to near-black.",
     "POSITIVE LOCKS: one hand, the same pieces throughout. " + CLEAN], (2, .7, .3), source="E7_gold_720p (12 s, 2 cuts)"),
 "ARCH-DRAWING": P("one-take", 0, [12, 20], "one building rising through the frame; floors/slabs readable, the view it earns at the top",
    "building on the right half, sky and neighbourhood on the left", ("left", .30), "smooth vertical drone rise, constant speed",
    ["building", "floor slabs / balconies"],
    ["FORMAT: One continuous shot, no cuts.", "CAMERA: smooth vertical drone rise, constant speed. FORBIDDEN: cuts, shake, spins.",
     "COMPOSITION: The tower stays in the right half of the frame; the left third is sky and low surroundings.",
     "POSITIVE LOCKS: one tower, the same architecture throughout. " + CLEAN], (0, .9, .25), source="E8_tower_720p (18 s)"),
 "MAGAZINE-EDITORIAL": P("one-take", 0, [15, 20], "one styled room; each priced piece visible in turn", "wide interior, pieces readable, camera travels through the room",
    ("left", .20), "smooth stabilised FPV glide, constant speed", ["each furniture piece"],
    ["FORMAT: ONE SINGLE UNBROKEN CONTINUOUS TAKE. Absolutely no cuts, no dissolves, no fades, no jump in time or position.",
     "CAMERA: smooth stabilised FPV drone, constant graceful speed, gentle banking. FORBIDDEN: cuts, shake, fast whips, collisions.",
     "POSITIVE LOCKS: one continuous camera path, the same room from start to end; no people; every furniture piece stays identical to the first frame. " + CLEAN],
    (0, .7, .15), source="E5_home_v2_720p (18 s; v1 had a cut and was regenerated)"),
 "KITCHEN-TICKET": P("cut-list", 5, [12, 18], "a dish being made in macro steps (fire, slice, sauce, salt, plated hero)", "macro, subject centre-left",
    ("right", .30), "energy from cuts and speed ramps", ["the dish/ingredient per shot"],
    ["FORMAT: Timestamped cut-blocks. HARD CUTS exactly at the listed timecodes and nowhere else.",
     "COMPOSITION: Keep the right third of each shot dark and plain (the order ticket sits there).",
     "CAMERA: energy from cuts and speed ramps. FORBIDDEN: whip-pans, shake. POSITIVE LOCKS: one dish, one plate. " + CLEAN],
    (5, .6, .2), source="E10_chef_720p (15 s, 4 cuts)"),
 "LENS-POSTCARD": P("one-take", 0, [15, 20], "a first-person walk that meets a sign, a landmark and a person to talk to", "POV at eye level, gentle head motion",
    ("bottom", .20), "natural first-person walk, stabilised", ["sign", "landmark", "person/cup"],
    ["FORMAT: One continuous shot, no cuts.", "CAMERA: natural first-person walk, stabilised, gentle head motion. FORBIDDEN: cuts, shake.",
     "POSITIVE LOCKS: the sign keeps abstract unreadable symbols; no readable text anywhere. " + CLEAN],
    (0, .6, .15), source="E9_glasses_720p (18 s)"),
}

SIDE = {"both": "both sides", "left": "left", "right": "right", "top": "top", "bottom": "bottom"}


def shoot_line(v):
    """The hub card's 'Shoot it like this' line: take · framing · space."""
    take = {"one-take": "One take, no cuts", "cuts-ok": f"Cuts OK (max {v['max_cuts']})", "cut-list": f"Planned cuts (max {v['max_cuts']})"}[v["take"]]
    ns = v["negative_space"]
    space = "no free space needed" if ns["side"] == "none" else f"{round(ns['min_frac'] * 100)}% free {SIDE[ns['side']]}"
    extra = " · subject matte" if v["separation"] else ""
    return f"{take} · {v['framing']} · {space}{extra}"


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    out = here / "plates.json"
    out.write_text(json.dumps(PLATES, ensure_ascii=False, indent=1), encoding="utf-8")
    print(len(PLATES), "contracts ->", out)
    hub = here.parent / "catalog" / "index.html"
    h = hub.read_text(encoding="utf-8")
    block = "/*PLATES*/const SHOOT = " + json.dumps({k: shoot_line(v) for k, v in PLATES.items()}, ensure_ascii=False) + ";/*END PLATES*/"
    if "/*PLATES*/" in h:
        i, j = h.index("/*PLATES*/"), h.index("/*END PLATES*/") + len("/*END PLATES*/")
        h = h[:i] + block + h[j:]
    else:
        h = h.replace("const S = [", block + chr(10) + "const S = [", 1)
    hub.write_text(h, encoding="utf-8")
    print("hub 'Shoot it like this' lines ->", hub)
