"""Render genuine Tiled TMX layers and animated player route into a GitHub-compatible GIF.
Run: python scripts/render_map.py. Tiled edits to maps/village.tmx are respected.
Now supports editable collectible stars stored directly in the TMX file.
"""
from __future__ import annotations
from pathlib import Path
import xml.etree.ElementTree as ET
import re, math
from PIL import Image, ImageDraw

ROOT = Path(__file__).resolve().parents[1]
MAP = ROOT / 'maps/village.tmx'
OUT = ROOT / 'assets/pathfinder.gif'
ROOT_XML = ET.parse(MAP).getroot()
T = int(ROOT_XML.attrib['tilewidth'])
MW = int(ROOT_XML.attrib['width'])
MH = int(ROOT_XML.attrib['height'])
STAR_ASSET = ROOT / 'source_assets/game/star.png'

class TmxRenderer:
    def __init__(self):
        self.tiles = {}
        self.base = Image.new('RGBA', (MW * T, MH * T), (83, 142, 85, 255))
        for ts in ROOT_XML.findall('tileset'):
            first = int(ts.attrib['firstgid'])
            tsx = ET.parse((MAP.parent / ts.attrib['source']).resolve()).getroot() if 'source' in ts.attrib else ts
            tsxpath = (MAP.parent / ts.attrib['source']).resolve() if 'source' in ts.attrib else MAP
            for tile in tsx.findall('tile'):
                im = tile.find('image')
                if im is None:
                    continue
                p = (tsxpath.parent / im.attrib['source']).resolve()
                if not p.exists():
                    continue
                self.tiles[first + int(tile.attrib['id'])] = Image.open(p).convert('RGBA')
        for layer in ROOT_XML:
            if layer.tag == 'layer' and layer.attrib.get('visible', '1') != '0':
                self.draw_layer(layer)
            elif layer.tag == 'objectgroup' and layer.attrib.get('visible', '1') != '0':
                # do not draw overlay stars as part of the base map; they are animated separately
                if layer.attrib.get('name') == 'Collectible Stars [edit positions]':
                    continue
                self.draw_objects(layer)

    def draw_layer(self, lay):
        data = lay.find('data')
        if data is None or data.attrib.get('encoding') != 'csv':
            return
        values = [int(s) for s in re.findall(r'\d+', data.text or '')]
        w = int(lay.attrib.get('width', MW))
        dx = int(float(lay.attrib.get('offsetx', '0')))
        dy = int(float(lay.attrib.get('offsety', '0')))
        for i, gid in enumerate(values):
            gid &= 0x0FFFFFFF
            if not gid or gid not in self.tiles:
                continue
            tile = self.tiles[gid]
            x = i % w * T + dx
            y = i // w * T + dy
            self.base.alpha_composite(tile, (x, y + T - tile.height))

    def draw_objects(self, lay):
        for obj in lay.findall('object'):
            if obj.attrib.get('visible', '1') == '0':
                continue
            if 'gid' not in obj.attrib:
                continue
            gid = int(obj.attrib['gid']) & 0x0FFFFFFF
            tile = self.tiles.get(gid)
            if tile is None:
                continue
            x = int(float(obj.attrib['x']))
            y = int(float(obj.attrib['y']))
            self.base.alpha_composite(tile, (x, y - tile.height))

def get_route():
    objs = ROOT_XML.find(".//objectgroup[@name='Player Route [edit polyline]']")
    if objs is None:
        raise RuntimeError('Missing route object group in village.tmx')
    route = objs.find("object[@name='Player Walk Path']")
    if route is None or route.find('polyline') is None:
        raise RuntimeError('Missing Player Walk Path polyline')
    ox = float(route.attrib.get('x', 0))
    oy = float(route.attrib.get('y', 0))
    points = [tuple(float(v) for v in pair.split(',')) for pair in route.find('polyline').attrib['points'].split()]
    return [(ox + x, oy + y) for x, y in points]

def get_stars():
    group = ROOT_XML.find(".//objectgroup[@name='Collectible Stars [edit positions]']")
    if group is None:
        return []
    stars = []
    for obj in group.findall('object'):
        if obj.attrib.get('visible', '1') == '0':
            continue
        x = float(obj.attrib.get('x', 0))
        y = float(obj.attrib.get('y', 0))
        w = float(obj.attrib.get('width', 32))
        h = float(obj.attrib.get('height', 32))
        stars.append({'name': obj.attrib.get('name', 'Star'), 'x': x, 'y': y, 'w': w, 'h': h})
    return stars

def frame_sprite(facing, step):
    ix = {'down': (2, 3), 'left': (5, 6), 'right': (8, 9), 'up': (11, 12)}[facing][step % 2]
    return Image.open(ROOT / f'source_assets/sprites/player{ix}.png').convert('RGBA')

def load_star_sprite():
    star = Image.open(STAR_ASSET).convert('RGBA')
    return star

def draw_star(base, star, sx, sy, scale=1, glow=False):
    sprite = star.resize((int(star.width * scale), int(star.height * scale)), Image.Resampling.NEAREST)
    if glow:
        g = Image.new('RGBA', (sprite.width + 16, sprite.height + 16), (0, 0, 0, 0))
        gd = ImageDraw.Draw(g)
        gd.ellipse((4, 4, g.width - 4, g.height - 4), fill=(255, 232, 105, 60))
        base.alpha_composite(g, (sx - 8, sy - 8))
    base.alpha_composite(sprite, (sx, sy))

def generate():
    r = TmxRenderer()
    pts = get_route()
    stars = get_stars()
    star_sprite = load_star_sprite()

    steps = []
    for (x1, y1), (x2, y2) in zip(pts, pts[1:]):
        dist = math.hypot(x2 - x1, y2 - y1)
        n = max(2, round(dist / 22))
        facing = (
            'right' if abs(x2 - x1) >= abs(y2 - y1) and x2 > x1 else
            'left' if abs(x2 - x1) >= abs(y2 - y1) else
            'down' if y2 > y1 else 'up'
        )
        for i in range(n):
            a = i / n
            steps.append((x1 + (x2 - x1) * a, y1 + (y2 - y1) * a, facing))
    steps.append((*pts[-1], 'down'))
    if len(steps) > 72:
        steps = [steps[round(i * (len(steps) - 1) / 71)] for i in range(72)]

    W, H = 1152, 634
    visible_w, visible_h = 1040, 520
    from pixel_font import pixel_text
    composed = []
    static = r.base
    collected = set()
    flash = None

    for i, (x, y, facing) in enumerate(steps):
        # update collection state before drawing frame
        for idx, s in enumerate(stars):
            if idx in collected:
                continue
            cx = s['x'] + s['w'] / 2
            cy = s['y'] + s['h'] / 2
            if math.hypot(cx - x, cy - y) < 34:
                collected.add(idx)
                flash = (cx, cy, 4)
                break

        camera_x = round(min(max(0, x - visible_w * .5), static.width - visible_w))
        camera_y = round(min(max(0, y - visible_h * .5), static.height - visible_h))
        crop = static.crop((camera_x, camera_y, camera_x + visible_w, camera_y + visible_h))
        frame = Image.new('RGBA', (W, H), '#0d1117')
        d = ImageDraw.Draw(frame)
        d.rounded_rectangle((12, 12, W - 12, H - 12), radius=18, fill='#111b17', outline='#355c40', width=3)
        d.rounded_rectangle((24, 74, W - 24, H - 25), radius=10, fill='#09120c', outline='#486a4f', width=2)
        frame.alpha_composite(crop, (56, 90))

        # draw currently uncollected stars on top of map
        for idx, s in enumerate(stars):
            if idx in collected:
                continue
            sx = round(56 + s['x'] - camera_x)
            sy = round(90 + s['y'] - camera_y)
            bob = math.sin((i + idx) * 0.55) * 2.5
            draw_star(frame, star_sprite, sx, round(sy + bob), scale=1, glow=True)

        # sparkle at recent collection spot
        if flash is not None and flash[2] > 0:
            fx, fy, n = flash
            cx = round(56 + fx - camera_x)
            cy = round(90 + fy - camera_y)
            for r0 in [6 + (4 - n) * 3, 13 + (4 - n) * 4]:
                d.ellipse((cx - r0, cy - r0, cx + r0, cy + r0), outline=(255, 230, 90, 150), width=2)
            pixel_text(frame, '+1', cx + 16, cy - 24, 1.8, '#f8dd63')
            flash = (fx, fy, n - 1)
            if flash[2] <= 0:
                flash = None

        spr = frame_sprite(facing, i).resize((64, 64), Image.Resampling.NEAREST)
        px = round(56 + x - camera_x - 32)
        py = round(90 + y - camera_y - 54)
        frame.alpha_composite(spr, (px, py))

        # HUD
        pixel_text(frame, 'WORLD / PATHFINDER', 44, 29, 2.5, '#daf6dd')
        pixel_text(frame, 'COLLECT THE STARS', 650, 29, 2.15, '#facc15')
        pixel_text(frame, f'STARS {len(collected):02d}/{len(stars):02d}', 872, 29, 2.0, '#daf6dd')
        composed.append(frame.convert('P', palette=Image.Palette.ADAPTIVE, colors=128))

    OUT.parent.mkdir(exist_ok=True, parents=True)
    composed[0].save(OUT, save_all=True, append_images=composed[1:], duration=115, loop=0, optimize=True, disposal=2)
    static.thumbnail((1152, 960), Image.Resampling.NEAREST)
    static.save(ROOT / 'assets/village-map-full.png')
    print(f'Pathfinder: {len(composed)} frames; stars={len(stars)}; file={OUT.stat().st_size/1e6:.2f} MB')

if __name__ == '__main__':
    generate()
