# Example specs (real, rendered)

| file | style | notes |
|---|---|---|
| `E6_sneaker_sx.py` | KINETIC-HE + KINETIC-KARAOKE + FLASH-CARD + punch (SX = social dynamic stomp) | smoke-tested: builds and passes `hyperframes check` |
| `E4_fire_hk.py` | TAPE-HE + counters + tracked box/tag (HK = Hebrew kinetic) | voice envelope inlined as `env` |
| `E8_tower_bespoke.py` | ARCH-DRAWING, fully bespoke via `html_front` / `css` / `js` / `fonts` | data files alongside |

To run one: copy it to `<project>/specs/<AD>.py` and provide `clips/<AD>_720p.mp4` + `tracks/<AD>_vtrack.json`
(+ `mattes/<AD>_alpha.webm` when an element uses `behind`), then `python run_ad.py <AD>`. The object names in the
spec (`shoe`, `door`, ...) must exist in your vtrack json.
