
"""5x7 pixel lettering, compatible with formatted card-renderer.js."""

from __future__ import annotations

import re
from pathlib import Path

from PIL import ImageDraw

SOURCE = Path(__file__).resolve().with_name("card-renderer.js")

# Support single/double quotes, optional whitespace,
# unquoted JavaScript keys, and multiline arrays.
GLYPH_PATTERN = re.compile(
    r"(?P<key>'[^']+'|\"[^\"]+\"|[A-Za-z_$][\w$]*)\s*:\s*"
    r"\[(?P<rows>(?:\s*['\"][01]{5}['\"]\s*,?){7})\s*\]",
    re.MULTILINE,
)

ROW_PATTERN = re.compile(r"['\"]([01]{5})['\"]")


def load_glyphs():
    text = SOURCE.read_text(encoding="utf-8")
    glyphs = {}

    for match in GLYPH_PATTERN.finditer(text):
        key = match.group("key").strip("'\"")
        rows = ROW_PATTERN.findall(match.group("rows"))

        if len(rows) == 7:
            glyphs[key.upper()] = rows

    if len(glyphs) < 26 or "?" not in glyphs:
        raise RuntimeError(
            "Could not load pixel glyphs from "
            "scripts/card-renderer.js. "
            "Check that the FONT object still "
            "contains 5x7 glyph rows."
        )

    glyphs.setdefault(" ", ["00000"] * 7)
    return glyphs


FONT = load_glyphs()


def pixel_text(image, text, x, y, scale=2, color="#d0e9d0"):
    """Render crisp, unantialiased pixel glyphs."""

    draw = ImageDraw.Draw(image)

    scale = max(1, round(scale))
    x, y = round(x), round(y)

    for character in str(text).upper():
        glyph = FONT.get(character, FONT["?"])

        for row_index, bits in enumerate(glyph):
            for col_index, bit in enumerate(bits):
                if bit == "1":
                    left = x + col_index * scale
                    top = y + row_index * scale

                    draw.rectangle(
                        (
                            left,
                            top,
                            left + scale - 1,
                            top + scale - 1,
                        ),
                        fill=color,
                    )

        x += 6 * scale
