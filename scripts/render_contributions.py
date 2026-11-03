"""GitHub contribution calendar with Brio's four-direction animation.

Commands:
    python scripts/render_contributions.py
    python scripts/render_contributions.py --fetch
    python scripts/render_contributions.py --preview

Features:
- Compact calendar with no unnecessary bottom space
- Contribution legend aligned with the top-right heading
- No live-data/date label
- Real GitHub contribution levels
- Brio moves only up, down, left, and right
- Brio moves one calendar block at a time
- Nearest illuminated contribution targeting
- Visited illuminated contributions turn dark
- Automatic looping GIF
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

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "contributions.json"
OUT = ROOT / "assets" / "contribution-brio.gif"

USERNAME = "HiroSaito04"

# Canvas and calendar dimensions
W, H = 1198, 222
GAP = 17
CELL = 13
GX, GY = 126, 82

COLORS = [
    "#161b22",
    "#0e4429",
    "#006d32",
    "#26a641",
    "#39d353",
]


class ContributionsHTML(HTMLParser):
    def __init__(self):
        super().__init__()
        self.days = []

    def handle_starttag(self, tag, attrs):
        if tag not in ("td", "rect"):
            return

        attributes = dict(attrs)

        if "data-date" not in attributes:
            return

        if "data-level" not in attributes:
            return

        try:
            level = int(attributes["data-level"])
            self.days.append(
                {
                    "date": attributes["data-date"],
                    "level": min(4, max(0, level)),
                }
            )
        except ValueError:
            pass


def fetch():
    url = f"https://github.com/users/" f"{USERNAME}/contributions"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "Mozilla/5.0",
            "Accept": "text/html",
        },
    )

    errors = []
    days = []

    try:
        with urllib.request.urlopen(
            request,
            timeout=28,
        ) as response:
            html = response.read().decode("utf-8")

        parser = ContributionsHTML()
        parser.feed(html)
        days = parser.days

    except Exception as exc:
        errors.append(str(exc))

    if len(days) < 330:
        try:
            api = (
                "https://github-contributions-api.jogruber.de/" f"v4/{USERNAME}?y=last"
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
                    "level": int(item["level"]),
                }
                for item in result["contributions"]
            ]

        except Exception as exc:
            errors.append(str(exc))

    # Preserve the existing cache if fetching fails.
    valid_days = {item["date"]: item for item in days if 0 <= item["level"] <= 4}

    today = dt.date.today()
    earliest = today - dt.timedelta(days=366)

    within = [
        value
        for date, value in valid_days.items()
        if earliest.isoformat() <= date <= today.isoformat()
    ]

    if len(within) < 320:
        raise RuntimeError(
            "Could not fetch the complete contribution "
            "calendar. Existing data was preserved. " + " ".join(errors)
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
        "Fetched real GitHub contributions:",
        len(within),
    )


def levels_for(mode):
    today = dt.date.today()

    sunday = today - dt.timedelta(days=(today.weekday() + 1) % 7)

    first = sunday - dt.timedelta(weeks=52)

    days = [first + dt.timedelta(days=i) for i in range(371)]

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

        return (
            days,
            levels,
            "SAMPLE PREVIEW - NOT REAL DATA",
        )

    if not DATA.exists():
        return (
            days,
            {},
            "RUN GITHUB ACTION TO LOAD CONTRIBUTIONS",
        )

    cached = json.loads(DATA.read_text(encoding="utf-8"))

    if cached.get("source") != "GitHub public contributions":
        raise RuntimeError("Unknown contribution data source.")

    levels = {item["date"]: int(item["level"]) for item in cached["days"]}

    return days, levels, ""


def draw(
    mode,
    frame_ms=200,
    pixels_per_frame=12.0,
    frame_budget=None,
):
    days, levels, label = levels_for(mode)

    today = dt.date.today()

    # --------------------------------------------------
    # BASE CANVAS
    # --------------------------------------------------

    base = Image.new(
        "RGBA",
        (W, H),
        "#0d1117",
    )

    dr = ImageDraw.Draw(base)

    dr.rounded_rectangle(
        (1, 1, W - 2, H - 2),
        radius=10,
        fill="#0d1117",
        outline="#30363d",
        width=2,
    )

    # --------------------------------------------------
    # HEADER
    # --------------------------------------------------

    pixel_text(
        base,
        "CONTRIBUTION ACTIVITY",
        26,
        23,
        3,
        "#e6edf3",
    )

    # Only show warnings for sample or missing data.
    # No LIVE GITHUB DATA / DATE label.
    if mode == "sample" or not DATA.exists():
        pixel_text(
            base,
            label,
            480,
            53,
            1.5,
            "#8b949e",
        )

    # --------------------------------------------------
    # TOP-RIGHT CONTRIBUTION LEGEND
    # --------------------------------------------------

    legend_y = 28

    pixel_text(
        base,
        "LESS",
        W - 347,
        legend_y,
        2,
        "#8b949e",
    )

    for level, color in enumerate(COLORS):
        x = W - 273 + level * 23

        dr.rounded_rectangle(
            (
                x,
                legend_y - 2,
                x + 14,
                legend_y + 12,
            ),
            radius=2,
            fill=color,
        )

    pixel_text(
        base,
        "MORE",
        W - 105,
        legend_y,
        2,
        "#8b949e",
    )

    # --------------------------------------------------
    # MONTH LABELS
    # --------------------------------------------------

    for week in range(53):
        day = days[week * 7]

        if week == 0:
            continue

        previous = days[(week - 1) * 7]

        if day.month != previous.month:
            x = GX + week * GAP

            if x < 1100:
                pixel_text(
                    base,
                    day.strftime("%b").upper(),
                    x,
                    58,
                    2,
                    "#8b949e",
                )

    # --------------------------------------------------
    # WEEKDAY LABELS
    # --------------------------------------------------

    for row, weekday in [
        (1, "MON"),
        (3, "WED"),
        (5, "FRI"),
    ]:
        pixel_text(
            base,
            weekday,
            39,
            GY + row * GAP + 2,
            2,
            "#8b949e",
        )

    # --------------------------------------------------
    # CONTRIBUTION GRID
    # --------------------------------------------------

    lit = {}

    for week in range(53):
        for row in range(7):
            day = days[week * 7 + row]

            if day > today:
                continue

            date = day.isoformat()

            if mode != "sample" and date not in levels:
                continue

            level = min(
                4,
                max(0, int(levels.get(date, 0))),
            )

            x = GX + week * GAP
            y = GY + row * GAP

            dr.rounded_rectangle(
                (x, y, x + CELL, y + CELL),
                radius=2,
                fill=COLORS[level],
            )

            if level > 0:
                lit[(week, row)] = (
                    x + CELL / 2,
                    y + CELL / 2,
                )

    # --------------------------------------------------
    # BRIO SPRITES
    # --------------------------------------------------

    spritebase = ROOT / "source_assets" / "sprites"

    spritecache = {
        number: Image.open(spritebase / f"brio{number}.png").convert("RGBA")
        for number in range(1, 13)
    }

    frames = []
    remaining = set(lit)
    consumed = set()

    # Brio begins just left of the contribution grid.
    current_cell = (-1, 3)

    tick = 0

    def cell_center(position):
        col, row = position

        return (
            GX + col * GAP + CELL / 2,
            GY + row * GAP + CELL / 2,
        )

    def direction_for(start, end):
        dc = end[0] - start[0]
        dr = end[1] - start[1]

        if dc > 0:
            return "right"

        if dc < 0:
            return "left"

        if dr > 0:
            return "down"

        return "up"

    def manhattan(start, end):
        return abs(start[0] - end[0]) + abs(start[1] - end[1])

    # --------------------------------------------------
    # FRAME RENDERING
    # --------------------------------------------------

    def paint(point, direction, standing=False):
        nonlocal tick

        frame = base.copy()
        draw = ImageDraw.Draw(frame)

        # Turn visited illuminated cells dark.
        for week, row in consumed:
            x = GX + week * GAP
            y = GY + row * GAP

            draw.rounded_rectangle(
                (x, y, x + CELL, y + CELL),
                radius=2,
                fill=COLORS[0],
            )

        animations = {
            "down": (1, 2, 3),
            "left": (4, 5, 6),
            "right": (7, 8, 9),
            "up": (10, 11, 12),
        }

        sprites = animations[direction]

        if standing:
            index = sprites[0]
        else:
            index = sprites[1 + tick % 2]

        sprite = spritecache[index]

        px = round(point[0] - sprite.width / 2)

        py = round(point[1] - sprite.height + CELL / 2 + 2)

        frame.alpha_composite(
            sprite,
            (px, py),
        )

        frames.append(
            frame.convert(
                "P",
                palette=Image.Palette.ADAPTIVE,
                colors=64,
            )
        )

        tick += 1

    # --------------------------------------------------
    # ORTHOGONAL GRID MOVEMENT
    # --------------------------------------------------

    def route_cells(start, target):
        """Move exactly one block at a time.

        Only four directions are allowed:
        up, down, left, and right.
        """

        path = []

        col, row = start
        target_col, target_row = target

        horizontal = abs(target_col - col)
        vertical = abs(target_row - row)

        # Move along the longer axis first.
        if horizontal >= vertical:

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

    # --------------------------------------------------
    # OPTIONAL FRAME BUDGET
    # --------------------------------------------------

    if remaining and frame_budget:
        mock = current_cell
        targets = set(remaining)
        total_distance = 0

        while targets:
            target = min(
                targets,
                key=lambda position: (
                    manhattan(mock, position),
                    position[0],
                    position[1],
                ),
            )

            total_distance += manhattan(mock, target) * GAP

            mock = target
            targets.remove(target)

        pixels_per_frame = max(
            pixels_per_frame,
            total_distance
            / max(
                1,
                frame_budget - len(remaining),
            ),
        )

    # --------------------------------------------------
    # ANIMATE BRIO
    # --------------------------------------------------

    current_point = cell_center(current_cell)
    facing = "right"

    paint(
        current_point,
        facing,
        standing=True,
    )

    while remaining:

        # Find nearest illuminated contribution.
        target = min(
            remaining,
            key=lambda position: (
                manhattan(current_cell, position),
                position[0],
                position[1],
            ),
        )

        path = route_cells(
            current_cell,
            target,
        )

        for next_cell in path:

            start = cell_center(current_cell)
            destination = cell_center(next_cell)

            facing = direction_for(
                current_cell,
                next_cell,
            )

            distance = math.dist(
                start,
                destination,
            )

            count = max(
                1,
                math.ceil(distance / max(1.0, pixels_per_frame)),
            )

            for step in range(1, count + 1):

                progress = step / count

                point = (
                    start[0] + (destination[0] - start[0]) * progress,
                    start[1] + (destination[1] - start[1]) * progress,
                )

                # Collect the light on arrival.
                if step == count and next_cell in remaining:
                    remaining.remove(next_cell)
                    consumed.add(next_cell)

                paint(
                    point,
                    facing,
                    standing=(step == count),
                )

            current_cell = next_cell

    # Brief pause before looping.
    for _ in range(6):
        paint(
            cell_center(current_cell),
            facing,
            standing=True,
        )

    # --------------------------------------------------
    # SAVE ANIMATION
    # --------------------------------------------------

    OUT.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    frames[0].save(
        OUT,
        save_all=True,
        append_images=frames[1:],
        duration=frame_ms,
        loop=0,
        optimize=True,
        disposal=2,
    )

    print(
        f"Brio: {len(lit)} contributions collected | "
        f"{len(frames)} frames | "
        f"{len(frames) * frame_ms / 1000:.1f}s | "
        f"{OUT.stat().st_size / 1e6:.2f} MB"
    )


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--fetch",
        action="store_true",
        help="Fetch real GitHub contribution data",
    )

    parser.add_argument(
        "--preview",
        action="store_true",
        help="Generate a sample contribution calendar",
    )

    parser.add_argument(
        "--frame-ms",
        type=int,
        default=200,
        help="Milliseconds per frame",
    )

    parser.add_argument(
        "--pixels-per-frame",
        type=float,
        default=12,
        help="Brio movement speed",
    )

    parser.add_argument(
        "--frames",
        type=int,
        default=None,
        help="Optional approximate frame budget",
    )

    args = parser.parse_args()

    if args.fetch and args.preview:
        parser.error("--fetch and --preview cannot be combined")

    if not 60 <= args.frame_ms <= 1000:
        parser.error("--frame-ms must be between 60 and 1000")

    if not 1 <= args.pixels_per_frame <= 50:
        parser.error("--pixels-per-frame must be between 1 and 50")

    if args.frames is not None and not 25 <= args.frames <= 800:
        parser.error("--frames must be between 25 and 800")

    if args.fetch:
        fetch()

    draw(
        "sample" if args.preview else "live",
        args.frame_ms,
        args.pixels_per_frame,
        args.frames,
    )


if __name__ == "__main__":
    main()
