# Recipes: the original hand-built compositions

These files are the source the catalog styles were distilled from. Use them as **reference** when a style has to be
rebuilt for a new subject (the *bespoke-rewrite* tier) or when you want to see how a finished piece was assembled.
The runnable, parametrised versions live in `scripts/styles/` (`run_style.py`) and in the adkit examples (`run_ad.py`).

## Runs as-is vs reference only

| File | Status | Why |
|---|---|---|
| `bespoke/E4_fire_bespoke.py` (THERMAL-RESCUE) | runs with its own plate + track | needs only the clip/track/VO of the piece it is written for |
| `bespoke/E6_sneaker_bespoke.py` (SPEC-SCAN) | runs with its own plate + track | idem |
| `bespoke/E10_chef_bespoke.py` (KITCHEN-TICKET) | runs with its own plate + track | reads its sound from `shared/sfx` (generated on first run) |
| `bespoke/E5_home_bespoke.py` (MAGAZINE-EDITORIAL) | runs with its own plate + track + two product stills | the stills are not shipped: pass your own PNGs |
| `examples/E8_tower_bespoke.py` (ARCH-DRAWING) | **runs**: ships with its data files | the only bespoke recipe patched to load standalone |
| `bespoke/E8_tower_bespoke.py` | reference | the original; the standalone copy is the one above |
| `bespoke/E3_car_bespoke.py` (ROAD-HUD) | **reference only** | reads an environment JSON produced in the original project |
| `bespoke/E7_gold_bespoke.py` + `E7_gold_bespoke_loupe.py` (HALLMARK-LUXE) | **reference only** | the loupe sprite generator reads project paths (`tools/…`) and a tracked jewellery JSON |
| `bespoke/E9_glasses_bespoke.py` (LENS-POSTCARD) | **reference only** | reads a sign/translation JSON from the original project |
| `legacy_shots.py` | **reference only** | the very first shots (A1–C3, B1–B4, D1–D3). Project paths are hardcoded, and its Hebrew is set in Assistant. |

**Hebrew fonts in `legacy_shots.py`:** adkit remaps old Hebrew faces (Assistant, Rubik, Heebo …) to Suez One /
Karantina / Secular One at build time (`adkit.HE_REMAP`), but these legacy shots go straight through `shotkit`, which
does not remap. If you lift code from them, replace `"Assistant"` with `"Secular One"` (labels, HUD, captions) or
`"Karantina"` / `"Suez One"` (display), or build the shot with its `run_style` successor instead: HUD-HELMET / HUD-CLEAN
(B2, B4), SCIFI-TARGETING (B3), MAP-FLYOVER (A1), CAMPUS-AR (C1–C3), STOMP-ESCORT / COUNTDOWN-CTA (D1–D3).
CYBER-DOSSIER (B1) and ARRIVAL-CARD (A2) have no parametrised builder yet: rewrite from the recipe.

`EDIT-DOCTRINE-example.md` is the edit plan that shaped the first batch of ads (edit-director skill).
