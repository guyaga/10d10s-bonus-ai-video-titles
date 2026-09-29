"""Shared HyperFrames helpers: Assistant (Hebrew+Latin) @font-face + font install into a project."""
import shutil
from pathlib import Path

import paths
WEIGHTS = [300, 400, 600, 700, 800]


def install_fonts(project: Path):
    dst = project / "assets" / "fonts"
    dst.mkdir(parents=True, exist_ok=True)
    for f in paths.fonts().glob("assistant-*.woff2"):
        shutil.copy2(f, dst / f.name)


def font_css() -> str:
    """@font-face for Assistant: Hebrew + Latin subsets, weights 300-800."""
    rules = []
    for w in WEIGHTS:
        rules.append(
            f'@font-face{{font-family:"Assistant";font-weight:{w};font-display:block;'
            f'src:url(assets/fonts/assistant-latin-{w}.woff2) format("woff2");'
            f'unicode-range:U+0000-00FF,U+0131,U+0152-0153,U+02BB-02BC,U+02C6,U+02DA,U+02DC,U+2000-206F,U+2074,U+20AC,U+2122,U+2190-2199,U+2212,U+2215}}')
        rules.append(
            f'@font-face{{font-family:"Assistant";font-weight:{w};font-display:block;'
            f'src:url(assets/fonts/assistant-hebrew-{w}.woff2) format("woff2");'
            f'unicode-range:U+0307-0308,U+0590-05FF,U+200C-2010,U+20AA,U+25CC,U+FB1D-FB4F}}')
    return "\n".join(rules)


# Hebrew typographic rules used across shots:
#  - Hebrew lines: font-family Assistant, direction:rtl, weights 600 (sub-lines) / 800 (headlines)
#  - gershayim written with the proper character U+05F4 (״) and geresh U+05F3 (׳)
HE_CSS = '.he{font-family:"Assistant",sans-serif;direction:rtl;unicode-bidi:isolate}'
