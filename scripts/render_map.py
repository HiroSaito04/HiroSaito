"""READ-ONLY Tiled -> PixSims renderer.

Edit maps/village.tmx ONLY in Tiled. This script reads its layers, tile object
alignment, player polyline, and star objects; it never writes to a TMX/TSX file.
It writes assets/pixsims.gif and assets/village-map-full.png.

Usage:
    python scripts/render_map.py
    python scripts/render_map.py --camera follow
    python scripts/render_map.py --camera overview
    python scripts/render_map.py --map maps/village.tmx
"""

from __future__ import annotations

import argparse
import base64
import gzip
import math
import re
import struct
import xml.etree.ElementTree as ET
import zlib
from dataclasses import dataclass
from pathlib import Path

from PIL import Image, ImageDraw

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

FLIP_H = 0x80000000
FLIP_V = 0x40000000
FLIP_D = 0x20000000
GID_MASK = 0x0FFFFFFF
ALIGN = {
    "topleft": (0, 0),
    "top": (0.5, 0),
    "topright": (1, 0),
    "left": (0, 0.5),
    "center": (0.5, 0.5),
    "right": (1, 0.5),
    "bottomleft": (0, 1),
    "bottom": (0.5, 1),
    "bottomright": (1, 1),
}
ROUTE_GROUP = "Player Route [edit polyline]"
STARS_GROUP = "Collectible Stars [edit positions]"


def read_properties(el):
    properties = {}
    if el is None:
        return properties
    for prop in el.findall("./properties/property"):
        raw = prop.attrib.get("value", prop.text or "")
        kind = prop.attrib.get("type", "string")
        if kind in ("int", "float"):
            try:
                raw = float(raw) if kind == "float" else int(raw)
            except ValueError:
                pass
        if kind == "bool":
            raw = str(raw).lower() == "true"
        properties[prop.attrib["name"]] = raw
    return properties


def visible(el):
    return el.attrib.get("visible", "1") != "0"


def get_float(el, attr, default=0):
    return float(el.attrib.get(attr, default))


@dataclass
class Tile:
    image: Image.Image
    alignment: str = "bottomleft"
    tileoffset: tuple[float, float] = (0.0, 0.0)


class TiledMap:
    def __init__(self, filename: Path):
        self.filename = filename.resolve()
        self.root = ET.parse(self.filename).getroot()
        if self.root.attrib.get("orientation") != "orthogonal":
            raise ValueError(
                "This renderer currently supports orthogonal Tiled maps only."
            )
        self.tile_w = int(self.root.attrib["tilewidth"])
        self.tile_h = int(self.root.attrib["tileheight"])
        self.cols = int(self.root.attrib["width"])
        self.rows = int(self.root.attrib["height"])
        self.width = self.cols * self.tile_w
        self.height = self.rows * self.tile_h
        self.properties = read_properties(self.root)
        self.tile_dict = {}
        self.missing_gids = set()
        self._load_tilesets()
        self.image = Image.new("RGBA", (self.width, self.height), (56, 129, 68, 255))
        self._paint_children(self.root, (0, 0), 1.0)

    def _load_tilesets(self):
        for ref in self.root.findall("tileset"):
            first = int(ref.attrib["firstgid"])
            tsx_file = (
                (self.filename.parent / ref.attrib["source"]).resolve()
                if "source" in ref.attrib
                else self.filename
            )
            ts = ET.parse(tsx_file).getroot() if "source" in ref.attrib else ref
            align = ts.attrib.get("objectalignment", "bottomleft")
            offset = ts.find("tileoffset")
            tileoffset = (
                (get_float(offset, "x"), get_float(offset, "y"))
                if offset is not None
                else (0.0, 0.0)
            )
            image_cache = {}
            for tile in ts.findall("tile"):
                im = tile.find("image")
                if im is None:
                    continue
                source = (tsx_file.parent / im.attrib["source"]).resolve()
                if not source.is_file():
                    raise FileNotFoundError(
                        f"Tiled image missing: {source}\nKeep the TMX, TSX, and referenced image folders together."
                    )
                if source not in image_cache:
                    image_cache[source] = Image.open(source).convert("RGBA")
                self.tile_dict[first + int(tile.attrib["id"])] = Tile(
                    image_cache[source], align, tileoffset
                )
            # simple atlas tilesets are supported too
            atlas = ts.find("image")
            if atlas is not None:
                source = (tsx_file.parent / atlas.attrib["source"]).resolve()
                im = Image.open(source).convert("RGBA")
                tw = int(ts.attrib["tilewidth"])
                th = int(ts.attrib["tileheight"])
                columns = int(ts.attrib["columns"])
                count = int(ts.attrib["tilecount"])
                spacing = int(ts.attrib.get("spacing", 0))
                margin = int(ts.attrib.get("margin", 0))
                for tile_id in range(count):
                    x = margin + (tile_id % columns) * (tw + spacing)
                    y = margin + (tile_id // columns) * (th + spacing)
                    self.tile_dict[first + tile_id] = Tile(
                        im.crop((x, y, x + tw, y + th)), align, tileoffset
                    )

    @staticmethod
    def _decode_gid(raw_gid):
        return int(raw_gid) & GID_MASK

    def _tile_image(self, raw_gid):
        raw = int(raw_gid)
        tile = self.tile_dict.get(raw & GID_MASK)
        if tile is None:
            if raw & GID_MASK:
                self.missing_gids.add(raw & GID_MASK)
            return None, None
        img = tile.image
        if raw & FLIP_D:
            img = img.transpose(Image.Transpose.TRANSPOSE)
        if raw & FLIP_H:
            img = img.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        if raw & FLIP_V:
            img = img.transpose(Image.Transpose.FLIP_TOP_BOTTOM)
        return img, tile

    def _paint_children(self, parent, offset, opacity):
        for el in parent:
            if el.tag not in ("layer", "objectgroup", "group") or not visible(el):
                continue
            origin = (
                offset[0] + get_float(el, "offsetx"),
                offset[1] + get_float(el, "offsety"),
            )
            alpha = opacity * get_float(el, "opacity", 1.0)
            if el.tag == "group":
                self._paint_children(el, origin, alpha)
                continue
            if el.attrib.get("name") in (ROUTE_GROUP, STARS_GROUP):
                continue  # overlay objects, not part of static map
            overlay = Image.new("RGBA", self.image.size)
            if el.tag == "layer":
                self._paint_tile_layer(overlay, el, origin)
            else:
                self._paint_object_layer(overlay, el, origin)
            if alpha < 1:
                overlay.putalpha(
                    overlay.getchannel("A").point(lambda a: round(a * alpha))
                )
            self.image.alpha_composite(overlay)

    def _read_layer_gids(self, layer):
        data = layer.find("data")
        if data is None:
            return []
        encoding = data.attrib.get("encoding", "xml")
        if encoding == "csv":
            return [int(s) for s in re.findall(r"\d+", data.text or "")]
        if encoding == "base64":
            raw = base64.b64decode((data.text or "").strip())
            compression = data.attrib.get("compression", "")
            if compression == "zlib":
                raw = zlib.decompress(raw)
            elif compression == "gzip":
                raw = gzip.decompress(raw)
            elif compression:
                raise ValueError(
                    f"Unsupported compression: {compression}; save as CSV in Tiled"
                )
            return [x[0] for x in struct.iter_unpack("<I", raw)]
        if encoding == "xml":
            return [int(tile.attrib.get("gid", 0)) for tile in data.findall("tile")]
        raise ValueError(f"Unknown TMX encoding: {encoding}")

    def _paint_tile_layer(self, layer_image, layer, offset):
        gids = self._read_layer_gids(layer)
        width = int(layer.attrib.get("width", self.cols))
        for index, raw_gid in enumerate(gids):
            if not raw_gid:
                continue
            img, tile = self._tile_image(raw_gid)
            if img is None:
                continue
            col, row = index % width, index // width
            x = round(col * self.tile_w + offset[0] + tile.tileoffset[0])
            y = round(
                row * self.tile_h
                + offset[1]
                + self.tile_h
                - img.height
                + tile.tileoffset[1]
            )
            layer_image.alpha_composite(img, (x, y))

    def _paint_object_layer(self, layer_image, layer, offset):
        for obj in layer.findall("object"):
            if not visible(obj) or "gid" not in obj.attrib:
                continue
            img, tile = self._tile_image(int(obj.attrib["gid"]))
            if img is None:
                continue
            width = max(1, round(get_float(obj, "width", img.width)))
            height = max(1, round(get_float(obj, "height", img.height)))
            if (width, height) != img.size:
                img = img.resize((width, height), Image.Resampling.NEAREST)
            ax, ay = ALIGN.get(tile.alignment, (0, 1))
            px = get_float(obj, "x") + offset[0] + tile.tileoffset[0]
            py = get_float(obj, "y") + offset[1] + tile.tileoffset[1]
            # handle simple object rotations around its anchor point
            angle = get_float(obj, "rotation")
            if angle:
                pad = max(width, height) * 2
                canvas = Image.new("RGBA", (width + 2 * pad, height + 2 * pad))
                canvas.alpha_composite(img, (pad, pad))
                pivot = (pad + ax * width, pad + ay * height)
                img = canvas.rotate(
                    -angle,
                    resample=Image.Resampling.NEAREST,
                    center=pivot,
                    expand=False,
                )
                px -= pivot[0]
                py -= pivot[1]
            else:
                px -= ax * width
                py -= ay * height
            layer_image.alpha_composite(img, (round(px), round(py)))

    def object_group(self, name):
        return self.root.find(f".//objectgroup[@name='{name}']")

    def route(self):
        group = self.object_group(ROUTE_GROUP)
        obj = (
            group.find("object[@name='Player Walk Path']")
            if group is not None
            else None
        )
        if obj is None or obj.find("polyline") is None:
            raise ValueError(
                f"Missing '{ROUTE_GROUP}' / 'Player Walk Path'. Draw a polyline in Tiled first. See TILED_MAP_GUIDE.md."
            )
        # include Tiled object group's offsets
        ox = get_float(group, "offsetx") + get_float(obj, "x")
        oy = get_float(group, "offsety") + get_float(obj, "y")
        pts = []
        for pair in obj.find("polyline").attrib.get("points", "").split():
            sx, sy = map(float, pair.split(","))
            pts.append((ox + sx, oy + sy))
        if len(pts) < 2:
            raise ValueError("Player Walk Path must contain at least two points.")
        return pts

    def stars(self):
        group = self.object_group(STARS_GROUP)
        if group is None:
            return []
        stars = []
        for obj in group.findall("object"):
            if not visible(obj):
                continue
            x = get_float(obj, "x") + get_float(group, "offsetx")
            y = get_float(obj, "y") + get_float(group, "offsety")
            w = get_float(obj, "width", 32)
            h = get_float(obj, "height", 32)
            icon = None
            if (
                "gid" in obj
            ):  # Tiled tile object: anchor follows tileset TSX objectalignment
                raw_gid = int(obj.attrib["gid"])
                tile = self.tile_dict.get(raw_gid & GID_MASK)
                ax, ay = ALIGN.get(tile.alignment if tile else "bottomleft", (0, 1))
                x -= ax * w
                y -= ay * h
                icon, _ = self._tile_image(raw_gid)
            props = read_properties(obj)
            stars.append(
                dict(
                    name=obj.attrib.get("name", "Star"),
                    x=x,
                    y=y,
                    w=w,
                    h=h,
                    radius=float(props.get("pickup_radius", 32)),
                    icon=icon,
                )
            )
        return stars


def sprite(root, facing, number):
    names = {"down": (2, 3), "left": (5, 6), "right": (8, 9), "up": (11, 12)}
    frame = names[facing][number % 2]
    file = root / f"source_assets/sprites/player{frame}.png"
    if not file.exists():
        raise FileNotFoundError(f"Missing player sprite: {file}")
    return Image.open(file).convert("RGBA")


def nearest_point_distance(point, a, b):
    """Distance of a star center to a movement segment (prevents missed pickups)."""
    dx, dy = b[0] - a[0], b[1] - a[1]
    if dx * dx + dy * dy == 0:
        return math.dist(point, a)
    t = max(
        0.0,
        min(
            1.0, ((point[0] - a[0]) * dx + (point[1] - a[1]) * dy) / (dx * dx + dy * dy)
        ),
    )
    return math.dist(point, (a[0] + t * dx, a[1] + t * dy))


def steps_along_route(points, speed=18, max_frames=96):
    route = []
    for a, b in zip(points, points[1:]):
        dist = math.dist(a, b)
        count = max(1, math.ceil(dist / max(1, speed)))
        facing = (
            ("right" if b[0] > a[0] else "left")
            if abs(b[0] - a[0]) >= abs(b[1] - a[1])
            else ("down" if b[1] > a[1] else "up")
        )
        for i in range(count):
            alpha = i / count
            route.append(
                (a[0] + alpha * (b[0] - a[0]), a[1] + alpha * (b[1] - a[1]), facing)
            )
    route.append((*points[-1], "down"))
    if len(route) > max_frames:
        route = [
            route[round(i * (len(route) - 1) / (max_frames - 1))]
            for i in range(max_frames)
        ]
    return route


def generate(filename, camera="follow", duration_ms=None, max_frames=96, zoom=1.17):
    """Create a full-bleed PixSims game view with a bounded, gentle camera.

    The TMX file is read-only. The view crops *within* the map bounds and
    scales the crop to fill the viewport, so there are no side gutters or
    exposed map edges when the camera follows the player.
    """
    from pixel_font import pixel_text

    tiled = TiledMap(filename)
    points = tiled.route()
    stars = tiled.stars()
    mode = tiled.properties.get("camera_mode", "follow") if camera == "auto" else camera
    if mode not in ("overview", "follow"):
        raise ValueError("camera_mode must be overview or follow")
    ms = int(duration_ms or tiled.properties.get("frame_duration_ms", 135))
    speed = float(tiled.properties.get("walk_pixels_per_frame", 18))
    steps = steps_along_route(points, speed=speed, max_frames=max_frames)
    if tiled.missing_gids:
        print("NOTE: TMX references missing tile IDs:", sorted(tiled.missing_gids))
    star_file = ROOT / "source_assets/game/star.png"
    star_icon = Image.open(star_file).convert("RGBA") if star_file.exists() else None
    if star_icon is None and stars:
        raise FileNotFoundError(f"Missing collectible graphic: {star_file}")
    map_image = tiled.image
    cache = {}

    # Full-width game view. Only 14px side borders: no extra empty canvas.
    W, H = 1152, 652
    vx, vy, vw, vh = 16, 72, 1120, 561

    # Source window maintains the display aspect ratio, staying within the map.
    # Moderate zoom ~1.17x gives context around the player, never a close-up.
    zoom = max(1.0, min(2.0, float(zoom)))
    source_w = min(map_image.width, max(16, round(vw / zoom)))
    source_h = max(16, round(source_w * vh / vw))
    if source_h > map_image.height:
        source_h = map_image.height
        source_w = max(16, min(map_image.width, round(source_h * vw / vh)))
    scale_x = vw / source_w
    scale_y = vh / source_h
    cam_max_x = max(0, map_image.width - source_w)
    cam_max_y = max(0, map_image.height - source_h)

    def clamp(n, lo, hi):
        return max(lo, min(hi, n))

    camx = clamp(steps[0][0] - source_w * 0.5, 0, cam_max_x)
    camy = clamp(steps[0][1] - source_h * 0.53, 0, cam_max_y)
    collected = set()
    frames = []
    prev = None

    for i, (x, y, facing) in enumerate(steps):
        for j, star in enumerate(stars):
            if j in collected:
                continue
            center = (star["x"] + star["w"] / 2, star["y"] + star["h"] / 2)
            if nearest_point_distance(center, prev or (x, y), (x, y)) <= star["radius"]:
                collected.add(j)

        if mode == "follow":
            tx = clamp(x - source_w * 0.5, 0, cam_max_x)
            ty = clamp(y - source_h * 0.53, 0, cam_max_y)
            # Responsive but non-jittery camera that moves with the route.
            camx += (tx - camx) * 0.28
            camy += (ty - camy) * 0.28
        else:
            # Explicit overview fills the view with map art (no gutters).
            camx, camy = cam_max_x * 0.5, cam_max_y * 0.5
        left = round(clamp(camx, 0, cam_max_x))
        top = round(clamp(camy, 0, cam_max_y))

        # Draw moving objects into the viewport crop before pasting onto frame;
        # player/stars cannot bleed outside the frame even at map boundaries.
        scene = map_image.crop((left, top, left + source_w, top + source_h))
        scene = scene.resize((vw, vh), Image.Resampling.NEAREST)

        def onscreen(px, py):
            return round((px - left) * scale_x), round((py - top) * scale_y)

        if star_icon is not None:
            for j, star in enumerate(stars):
                if j in collected:
                    continue
                sx, sy = onscreen(star["x"], star["y"])
                source = star["icon"] if star["icon"] is not None else star_icon
                icon = source.resize(
                    (
                        max(8, round(star["w"] * scale_x)),
                        max(8, round(star["h"] * scale_y)),
                    ),
                    Image.Resampling.NEAREST,
                )
                # Skip fully offscreen stars, and clip partial sprites to scene.
                if sx + icon.width > 0 and sx < vw and sy + icon.height > 0 and sy < vh:
                    scene.alpha_composite(
                        icon, (sx, round(sy + math.sin((i + j) / 5) * 2))
                    )

        key = facing, i % 2
        if key not in cache:
            cache[key] = sprite(ROOT, facing, i % 2)
        player_img = cache[key]
        size = max(26, round(48 * (scale_x + scale_y) * 0.5))
        player_img = player_img.resize((size, size), Image.Resampling.NEAREST)
        cx, cy = onscreen(x, y)
        scene.alpha_composite(
            player_img, (round(cx - size / 2), round(cy - size * 0.85))
        )

        # Minimal pixel HUD: fills nearly the entire GIF with actual village.
        frame = Image.new("RGBA", (W, H), "#0a1410")
        dr = ImageDraw.Draw(frame)
        dr.rectangle((0, 0, W - 1, H - 1), outline="#315e3f", width=3)
        dr.rectangle((6, 7, W - 7, 58), fill="#0b1713")
        dr.line((14, 61, W - 15, 61), fill="#466d4d", width=2)
        # pixel-corner details
        for bx in (12, W - 24):
            dr.rectangle((bx, 12, bx + 11, 15), fill="#5caa6c")
        frame.alpha_composite(scene, (vx, vy))
        dr.rectangle(
            (vx - 2, vy - 2, vx + vw + 1, vy + vh + 1), outline="#477854", width=2
        )
        pixel_text(frame, "PIXSIMS", 28, 23, 3, "#d9efdc")
        pixel_text(frame, "VILLAGE WORLD", 324, 27, 2, "#93b99e")
        pixel_text(frame, "STAR QUEST", 754, 26, 2, "#f5ce54")
        pixel_text(
            frame, f"{len(collected):02d}/{len(stars):02d}", 1014, 23, 3, "#f8f0c7"
        )
        frames.append(frame.convert("P", palette=Image.Palette.ADAPTIVE, colors=128))
        prev = (x, y)

    frames.extend([frames[-1].copy()] * 6)
    output = ROOT / "assets/pixsims.gif"
    output.parent.mkdir(exist_ok=True, parents=True)
    frames[0].save(
        output,
        save_all=True,
        append_images=frames[1:],
        duration=ms,
        loop=0,
        optimize=True,
        disposal=2,
    )
    map_image.save(ROOT / "assets/village-map-full.png")
    print(
        f"RENDERED {output} | camera={mode} | zoom={zoom:.2f} "
        f"| crop={source_w}x{source_h} | frames={len(frames)} "
        f"| stars={len(collected)}/{len(stars)} "
        f"| {output.stat().st_size/1048576:.1f} MiB"
    )
    if len(collected) < len(stars):
        print(
            "TIP: Uncollected stars were away from Player Walk Path. Edit the route in Tiled."
        )
    print("Tiled TMX was read only and was not modified.")


def main():
    parser = argparse.ArgumentParser(
        description="Render your saved Tiled village into a player + collectible stars animation; no TMX edits."
    )
    parser.add_argument(
        "--map",
        default=str(ROOT / "maps/village.tmx"),
        help="Any Tiled .tmx map with the Player Route and Stars layers",
    )
    parser.add_argument(
        "--camera",
        choices=["auto", "overview", "follow"],
        default="follow",
        help="Default follows the player; auto reads the TMX camera_mode property",
    )
    parser.add_argument(
        "--frame-ms", type=int, default=None, help="Frame duration; optional override"
    )
    parser.add_argument(
        "--max-frames", type=int, default=96, help="Upper bound on GIF frames"
    )
    parser.add_argument(
        "--zoom",
        type=float,
        default=1.17,
        help="Camera zoom, 1.0 to 2.0; default is wide 1.17",
    )
    opts = parser.parse_args()
    generate(
        Path(opts.map),
        camera=opts.camera,
        duration_ms=opts.frame_ms,
        max_frames=max(10, opts.max_frames),
        zoom=opts.zoom,
    )


if __name__ == "__main__":
    main()
