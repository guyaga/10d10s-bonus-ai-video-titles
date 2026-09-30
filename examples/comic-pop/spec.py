"""COMIC-POP (#14) example: multi-colour comic burst words on the biggest beats only, everything else calm.
Runs as-is on the footage bundled with the skill:
    python scripts/run_ad.py COMIC-POP --spec examples/comic-pop/spec.py --root my-comic-pop [--render]
For your clip: set "clip" and "track" (vtrack.py with a "model" object, or change "follow"), your words and beats.
Loud and young: we moved away from it for premium brands (see styles.md). One or two beats, never the whole ad."""
from pathlib import Path

DEMO = Path(__file__).resolve().parent.parent / "demo"
SPEC = {
    "theme": "pop",
    "clip": str(DEMO / "runway_demo_720p.mp4"),
    "track": str(DEMO / "runway_demo_vtrack.json"),
    "music": str(DEMO / "music_demo.mp3"),
    "music_vol": 0.6,
    "plate_vol": 0.3,
    "palette": {"acc": "#ff3d8b", "ink": "#111111", "lt": "#fffdf5", "panel": "rgba(14,14,14,.74)", "sub": "#e4e1db"},
    "elements": [
        {"type": "stomp", "text": "NEW", "follow": "model", "anchor": "l", "dx": -60, "dy": -120, "align": "r", "size": 190, "t": 1.0, "end": 2.6},
        {"type": "stomp", "text": "DROP!", "follow": "model", "anchor": "r", "dx": 60, "dy": 40, "align": "l", "size": 200, "t": 3.0, "end": 5.0},
        {"type": "stomp", "text": "NOW", "x": 960, "y": 540, "size": 260, "t": 5.6, "end": 7.6},
    ],
}
