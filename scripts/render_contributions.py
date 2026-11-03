
"""Render a compact, pixel-font GitHub contributions GIF with animated Brio.

Commands:
    python scripts/render_contributions.py
    python scripts/render_contributions.py --fetch
    python scripts/render_contributions.py --preview
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import random
import urllib.request
from html.parser import HTMLParser
from pathlib import Path

from PIL import Image, ImageDraw
from pixel_font import pixel_text


# ============================================================
# CONFIGURATION
# ============================================================

ROOT = Path(__file__).resolve().parents[1]

DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "assets" / "contribution-brio.gif"

USERNAME = "HiroSaito04"

WIDTH, HEIGHT = 1198, 222

GRID_X, GRID_Y = 126, 82
CELL, GAP = 13, 17

BACKGROUND = "#0d1117"
BORDER = "#30363d"
TEXT = "#e6edf3"
MUTED = "#8b949e"

COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]


# ============================================================
# FETCH GITHUB CONTRIBUTIONS
# ============================================================

class ContributionsHTML(HTMLParser):
    """Read date/level cells from GitHub's contribution calendar."""

    def __init__(self):
        super().__init__()
        self.days = []

    def handle_starttag(self, tag, attrs):
        if tag not in ("td", "rect"):
            return

        attributes = dict(attrs)

        date = attributes.get("data-date")
        level = attributes.get("data-level")

        if date is None or level is None:
            return

        try:
            self.days.append(
                {
                    "date": date,
                    "level": min(4, max(0, int(level))),
                }
            )
        except ValueError:
            pass


def fetch():
    """Refresh public contributions without overwriting failed fetches."""

    url = (
        f"https://github.com/users/"
        f"{USERNAME}/contributions"
    )

    errors = []
    days = []

    try:
        request = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0",
                "Accept": "text/html",
            },
        )

        with urllib.request.urlopen(
            request,
            timeout=28,
        ) as response:
            parser = ContributionsHTML()
            parser.feed(
                response.read().decode("utf-8")
            )
            days = parser.days

    except Exception as exc:
        errors.append(str(exc))

    if len(days) < 330:
        try:
            api = (
                "https://github-contributions-api.jogruber.de/"
                f"v4/{USERNAME}?y=last"
            )

            request = urllib.request.Request(
                api,
                headers={
                    "User-Agent": "pixel-profile-builder/1.0",
                },
            )

            with urllib.request.urlopen(
                request,
                timeout=28,
            ) as response:
                result = json.load(response)

            days = [
                {
                    "date": item["date"],
                    "level": min(
                        4,
                        max(0, int(item["level"])),
                    ),
                }
                for item in result["contributions"]
            ]

        except Exception as exc:
            errors.append(str(exc))

    unique_days = {
        day["date"]: day
        for day in days
        if 0 <= day["level"] <= 4
    }

    today = dt.date.today()
    start = today - dt.timedelta(days=366)

    within = [
        day
        for date, day in unique_days.items()
        if start.isoformat() <= date <= today.isoformat()
    ]

    if len(within) < 320:
        raise RuntimeError(
            "Could not retrieve enough public contribution data. "
            "The existing cache was not overwritten. "
            + " ".join(errors)
        )

    DATA.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    DATA.write_text(
        json.dumps(
            {
                "username": USERNAME,
                "source": "GitHub public contributions",
                "updated": today.isoformat(),
                "days": sorted(
                    within,
                    key=lambda item: item["date"],
                ),
            },
            indent=2,
        ),
        encoding="utf-8",
    )

    print(
        f"Fetched {len(within)} real GitHub contribution days."
    )


# ============================================================
# LOAD CONTRIBUTION LEVELS
# ============================================================

def levels_for(mode):
    today = dt.date.today()

    sunday = today - dt.timedelta(
        days=(today.weekday() + 1) % 7
    )

    first_day = sunday - dt.timedelta(weeks=52)

    days = [
        first_day + dt.timedelta(days=index)
        for index in range(371)
    ]

    if mode == "sample":
        rng = random.Random(11)

        levels = {
            day.isoformat(): rng.choices(
                [0, 1, 2, 3, 4],
                weights=[70, 14, 9, 5, 2],
            )[0]
            for day in days
            if day <= today
        }

        return days, levels

    if not DATA.exists():
        raise FileNotFoundError(
            "Missing data/contributions.json. "
            "Run the renderer with --fetch to retrieve "
            "real GitHub contributions."
        )

    cached = json.loads(
        DATA.read_text(encoding="utf-8")
    )

    if cached.get("source") != "GitHub public contributions":
        raise RuntimeError(
            "Unexpected contribution cache source; not using it."
        )

    levels = {
        item["date"]: min(
            4,
            max(0, int(item["level"])),
        )
        for item in cached["days"]
    }

    return days, levels


# ============================================================
# CALENDAR DESIGN
# ============================================================

def calendar_background(days, levels, mode):
    """Create the static calendar using crisp pixel lettering."""

    image = Image.new(
        "RGBA",
        (WIDTH, HEIGHT),
        BACKGROUND,
    )

    draw = ImageDraw.Draw(image)

    draw.rounded_rectangle(
        (1, 1, WIDTH - 2, HEIGHT - 2),
        radius=10,
        fill=BACKGROUND,
        outline=BORDER,
        width=2,
    )

    # --------------------------------------------------------
    # TOP-LEFT TITLE
    # --------------------------------------------------------

    pixel_text(
        image,
        "CONTRIBUTION ACTIVITY",
        26,
        23,
        3,
        TEXT,
    )

    # --------------------------------------------------------
    # TOP-RIGHT LEGEND
    # --------------------------------------------------------

    pixel_text(
        image,
        "LESS",
        WIDTH - 347,
        28,
        2,
        MUTED,
    )

    for level, color in enumerate(COLORS):
        x = WIDTH - 273 + level * 23

        draw.rounded_rectangle(
            (x, 26, x + 14, 40),
            radius=2,
            fill=color,
        )

    pixel_text(
        image,
        "MORE",
        WIDTH - 105,
        28,
        2,
        MUTED,
    )

    # --------------------------------------------------------
    # SAMPLE DISCLAIMER
    # --------------------------------------------------------

    if mode == "sample":
        pixel_text(
            image,
            "SAMPLE - NOT REAL DATA",
            425,
            57,
            1,
            MUTED,
        )

    # --------------------------------------------------------
    # MONTH LABELS
    # --------------------------------------------------------

    for week in range(1, 53):
        current = days[week * 7]
        previous = days[(week - 1) * 7]

        if current.month != previous.month:
            x = GRID_X + week * GAP

            if x < WIDTH - 65:
                pixel_text(
                    image,
                    current.strftime("%b").upper(),
                    x,
                    58,
                    2,
                    MUTED,
                )

    # --------------------------------------------------------
    # WEEKDAY LABELS
    # --------------------------------------------------------

    for row, name in (
        (1, "MON"),
        (3, "WED"),
        (5, "FRI"),
    ):
        pixel_text(
            image,
            name,
            39,
            GRID_Y + row * GAP + 2,
            2,
            MUTED,
        )

    # --------------------------------------------------------
    # CONTRIBUTION CELLS
    # --------------------------------------------------------

    today = dt.date.today()
    lit = set()

    for week in range(53):
        for row in range(7):
            day = days[week * 7 + row]
            date = day.isoformat()

            if day > today or date not in levels:
                continue

            level = levels[date]

            x = GRID_X + week * GAP
            y = GRID_Y + row * GAP

            draw.rounded_rectangle(
                (
                    x,
                    y,
                    x + CELL,
                    y + CELL,
                ),
                radius=2,
                fill=COLORS[level],
            )

            if level > 0:
                lit.add((week, row))

    return image, lit


# ============================================================
# BRIO SPRITES
# ============================================================

def load_sprites():
    folder = ROOT / "source_assets" / "sprites"
    sprites = {}

    for number in range(1, 13):
        path = folder / f"brio{number}.png"

        if not path.exists():
            raise FileNotFoundError(
                f"Missing Brio sprite: {path}"
            )

        with Image.open(path) as sprite:
            sprites[number] = sprite.convert("RGBA")

    return sprites


# ============================================================
# MOVEMENT HELPERS
# ============================================================

def manhattan(a, b):
    return (
        abs(a[0] - b[0])
        + abs(a[1] - b[1])
    )


def direction_for(a, b):
    if b[0] > a[0]:
        return "right"

    if b[0] < a[0]:
        return "left"

    if b[1] > a[1]:
        return "down"

    return "up"


def route_cells(start, target):
    """Move one cell at a time without diagonal movement."""

    col, row = start

    target_col, target_row = target

    path = []

    horizontal_first = (
        abs(target_col - col)
        >= abs(target_row - row)
    )

    if horizontal_first:
        while col != target_col:
            col += 1 if target_col > col else -1
            path.append((col, row))

        while row != target_row:
            row += 1 if target_row > row else -1
            path.append((col, row))

    else:
        while row != target_row:
            row += 1 if target_row > row else -1
            path.append((col, row))

        while col != target_col:
            col += 1 if target_col > col else -1
            path.append((col, row))

    return path


def center(cell):
    col, row = cell

    return (
        GRID_X + col * GAP + CELL / 2,
        GRID_Y + row * GAP + CELL / 2,
    )


# ============================================================
# CONSISTENT GIF PALETTE
# ============================================================

def gif_palette():
    """Preserve exact calendar and text colors across GIF frames."""

    palette = [
        (13, 17, 23),
        (48, 54, 61),
        (230, 237, 243),
        (139, 148, 158),
        (22, 27, 34),
        (14, 68, 41),
        (0, 109, 50),
        (38, 166, 65),
        (57, 211, 83),
    ]

    for red in range(0, 256, 51):
        for green in range(0, 256, 51):
            for blue in range(0, 256, 51):
                rgb = (red, green, blue)

                if rgb not in palette:
                    palette.append(rgb)

    palette = palette[:256]

    palette.extend(
        [(0, 0, 0)] * (256 - len(palette))
    )

    sample = Image.new(
        "P",
        (1, 1),
    )

    sample.putpalette(
        [
            channel
            for rgb in palette
            for channel in rgb
        ]
    )

    return sample


# ============================================================
# RENDER ANIMATION
# ============================================================

def draw(
    mode,
    frame_ms=200,
    pixels_per_frame=12.0,
    frame_budget=None,
):
    days, levels = levels_for(mode)

    base, lit = calendar_background(
        days,
        levels,
        mode,
    )

    sprites = load_sprites()
    palette = gif_palette()

    remaining = set(lit)
    consumed = set()

    current = (-1, 3)
    facing = "right"

    tick = 0
    frames = []

    poses = {
        "down": (1, 2, 3),
        "left": (4, 5, 6),
        "right": (7, 8, 9),
        "up": (10, 11, 12),
    }

    # --------------------------------------------------------
    # DRAW EACH ANIMATION FRAME
    # --------------------------------------------------------

    def frame_at(point, direction, standing=False):
        nonlocal tick

        picture = base.copy()
        painter = ImageDraw.Draw(picture)

        for week, row in consumed:
            x = GRID_X + week * GAP
            y = GRID_Y + row * GAP

            painter.rounded_rectangle(
                (
                    x,
                    y,
                    x + CELL,
                    y + CELL,
                ),
                radius=2,
                fill=COLORS[0],
            )

        animation = poses[direction]

        number = (
            animation[0]
            if standing
            else animation[1 + tick % 2]
        )

        sprite = sprites[number]

        px = round(
            point[0] - sprite.width / 2
        )

        py = round(
            point[1]
            - sprite.height
            + CELL / 2
            + 2
        )

        picture.alpha_composite(
            sprite,
            (px, py),
        )

        # The same palette is used for every frame.
        indexed = picture.convert("RGB").quantize(
            palette=palette,
            dither=Image.Dither.NONE,
        )

        frames.append(indexed)
        tick += 1

    # --------------------------------------------------------
    # OPTIONAL FRAME BUDGET
    # --------------------------------------------------------

    if remaining and frame_budget:
        position = current
        targets = set(remaining)
        total_distance = 0

        while targets:
            nearest = min(
                targets,
                key=lambda cell: (
                    manhattan(position, cell),
                    cell,
                ),
            )

            total_distance += (
                manhattan(position, nearest) * GAP
            )

            position = nearest
            targets.remove(nearest)

        pixels_per_frame = max(
            pixels_per_frame,
            total_distance
            / max(
                1,
                frame_budget - len(remaining),
            ),
        )

    # --------------------------------------------------------
    # INITIAL FRAME
    # --------------------------------------------------------

    frame_at(
        center(current),
        facing,
        standing=True,
    )

    # --------------------------------------------------------
    # COLLECT NEAREST ILLUMINATED CELLS
    # --------------------------------------------------------

    while remaining:
        target = min(
            remaining,
            key=lambda cell: (
                manhattan(current, cell),
                cell,
            ),
        )

        for next_cell in route_cells(current, target):
            start = center(current)
            end = center(next_cell)

            facing = direction_for(
                current,
                next_cell,
            )

            steps = max(
                1,
                math.ceil(
                    math.dist(start, end)
                    / pixels_per_frame
                ),
            )

            for step in range(1, steps + 1):
                blend = step / steps

                point = (
                    start[0]
                    + (end[0] - start[0]) * blend,
                    start[1]
                    + (end[1] - start[1]) * blend,
                )

                if (
                    step == steps
                    and next_cell in remaining
                ):
                    remaining.remove(next_cell)
                    consumed.add(next_cell)

                frame_at(
                    point,
                    facing,
                    standing=(step == steps),
                )

            current = next_cell

    # --------------------------------------------------------
    # LOOP PAUSE
    # --------------------------------------------------------

    for _ in range(6):
        frame_at(
            center(current),
            facing,
            standing=True,
        )

    # --------------------------------------------------------
    # EXPORT GIF
    # --------------------------------------------------------

    OUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    frames[0].save(
        OUT,
        format="GIF",
        save_all=True,
        append_images=frames[1:],
        duration=frame_ms,
        loop=0,
        optimize=False,
        disposal=2,
    )

    print(
        f"Brio: {len(lit)} contributions collected | "
        f"{len(frames)} frames | "
        f"{len(frames) * frame_ms / 1000:.1f}s | "
        f"{OUT.stat().st_size / 1_000_000:.2f} MB"
    )


# ============================================================
# COMMAND LINE
# ============================================================

def main():
    parser = argparse.ArgumentParser(
        description=__doc__
    )

    parser.add_argument(
        "--fetch",
        action="store_true",
    )

    parser.add_argument(
        "--preview",
        action="store_true",
    )

    parser.add_argument(
        "--frame-ms",
        type=int,
        default=200,
    )

    parser.add_argument(
        "--pixels-per-frame",
        type=float,
        default=12.0,
    )

    parser.add_argument(
        "--frames",
        type=int,
        default=None,
    )

    args = parser.parse_args()

    if args.fetch and args.preview:
        parser.error(
            "--fetch and --preview cannot be combined"
        )

    if not 60 <= args.frame_ms <= 1000:
        parser.error(
            "--frame-ms must be between 60 and 1000"
        )

    if not 1 <= args.pixels_per_frame <= 50:
        parser.error(
            "--pixels-per-frame must be between 1 and 50"
        )

    if (
        args.frames is not None
        and not 25 <= args.frames <= 800
    ):
        parser.error(
            "--frames must be between 25 and 800"
        )

    if args.fetch:
        fetch()

    draw(
        mode="sample" if args.preview else "live",
        frame_ms=args.frame_ms,
        pixels_per_frame=args.pixels_per_frame,
        frame_budget=args.frames,
    )


if __name__ == "__main__":
    main()
