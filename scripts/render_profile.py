"""Render and check the profile artwork: python3 scripts/render_profile.py.

Standard library only. Animated terminal graphics with reduced-motion alternatives.
"""
from html import escape
import json
from base64 import b64encode
from math import exp, pi, sin
from pathlib import Path
from random import Random
import re
from xml.etree import ElementTree

ROOT = Path(__file__).resolve().parents[1]
BACKGROUND, TEXT, BORDER = '#000000', '#FFFFFF', '#888888'
CONFIG = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))


def panel(height, title, body):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="960" height="{height}" viewBox="0 0 960 {height}" role="img" aria-labelledby="title">
<title id="title">{escape(title)}</title>
<style>
  svg {{ --ink: {BACKGROUND}; --paper: {TEXT}; }}
  @media (prefers-color-scheme: dark) {{ svg {{ --ink: {TEXT}; --paper: {BACKGROUND}; }} }}
  text {{ font-family: 'JetBrains Mono', Consolas, 'Liberation Mono', monospace; fill: var(--ink); }}
  .headline {{ font-weight: 800; letter-spacing: 2px; }}
  [fill="{TEXT}"] {{ fill: var(--ink); }}
  [stroke="{TEXT}"] {{ stroke: var(--ink); }}
  .bit {{ animation: bit 4s steps(1, end) infinite; }}
  .solve {{ stroke-dasharray: 1; animation: solve 18s linear infinite; }}
  .still {{ display: none; }}
  @keyframes bit {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0; }} }}
  @keyframes solve {{ 0%, 8% {{ stroke-dashoffset: 1; }} 88%, 100% {{ stroke-dashoffset: 0; }} }}
  @media (prefers-reduced-motion: reduce) {{
    .bit, .solve {{ animation: none; }}
    .fx {{ display: none; }}
    .still {{ display: inline; }}
  }}
</style>
<path d="M954 14V{height - 6}H14" fill="none" stroke="{BORDER}" stroke-width="4" shape-rendering="crispEdges"/>
<rect x="8" y="8" width="940" height="{height - 20}" fill="none" stroke="{TEXT}" stroke-width="2" shape-rendering="crispEdges"/>
<path d="M20 20h6m6 0h6m6 0h6" stroke="{TEXT}" stroke-width="6" shape-rendering="crispEdges"/>
<path d="M8 30H948" stroke="{BORDER}"/>
<text x="932" y="23" text-anchor="end" font-size="10" letter-spacing="1">{escape(CONFIG["handle"].upper())} / PIXEL TERMINAL</text>

{body}
</svg>
'''


def maze(cols=29, rows=11):
    rng = Random(27)
    parents = {(0, 0): None}
    stack = [(0, 0)]
    passages = set()
    while stack:
        x, y = stack[-1]
        neighbors = [(x + dx, y + dy) for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1))
                     if 0 <= x + dx < cols and 0 <= y + dy < rows and (x + dx, y + dy) not in parents]
        if not neighbors:
            stack.pop()
            continue
        cell = rng.choice(neighbors)
        parents[cell] = (x, y)
        passages.add(frozenset(((x, y), cell)))
        stack.append(cell)
    route = []
    cell = (cols - 1, rows - 1)
    while cell is not None:
        route.append(cell)
        cell = parents[cell]
    route.reverse()
    assert len(parents) == cols * rows and len(passages) == cols * rows - 1
    assert route[0] == (0, 0) and route[-1] == (cols - 1, rows - 1)
    assert all(frozenset(pair) in passages for pair in zip(route, route[1:]))
    return passages, route


def maze_panel():
    cols, rows, size, left, top = 29, 11, 24, 32, 138
    passages, route = maze(cols, rows)
    walls = []
    for y in range(rows):
        for x in range(cols):
            px, py = left + x * size, top + y * size
            if y == 0:
                walls.append(f'M{px} {py}h{size}')
            if x == 0 and y != 0:
                walls.append(f'M{px} {py}v{size}')
            if (x == cols - 1 and y != rows - 1) or (x < cols - 1 and frozenset(((x, y), (x + 1, y))) not in passages):
                walls.append(f'M{px + size} {py}v{size}')
            if y == rows - 1 or frozenset(((x, y), (x, y + 1))) not in passages:
                walls.append(f'M{px} {py + size}h{size}')
    path = 'M' + ' L'.join(f'{left + x * size + size // 2} {top + y * size + size // 2}' for x, y in route)
    return panel(448, 'A generated maze with an animated solution from entrance to exit', f'''
<text class="headline" x="32" y="77" font-size="42">&gt; PATHFINDER_</text>
<text x="928" y="44" text-anchor="end" font-size="14">01 / THE MAZE</text>
<text x="928" y="72" text-anchor="end" font-size="12">ONE PATH. MANY POSSIBILITIES.</text>
<path d="M32 106H928" stroke="{BORDER}"/>
<path d="{' '.join(walls)}" fill="none" stroke="{BORDER}" stroke-width="1" shape-rendering="crispEdges"/>
<path class="solve" d="{path}" pathLength="1" fill="none" stroke="{TEXT}" stroke-width="4" stroke-linejoin="miter"/>
<rect class="fx" x="-5" y="-5" width="10" height="10" fill="{TEXT}">
  <animateMotion path="{path}" dur="18s" keyPoints="0;0;1;1" keyTimes="0;0.08;0.88;1" calcMode="linear" repeatCount="indefinite"/>
</rect>
<rect x="39" y="145" width="10" height="10" fill="{BORDER}"/>
<rect x="711" y="385" width="10" height="10" fill="{BORDER}"/>
<text class="headline" x="769" y="183" font-size="22">01 THINK</text>
<text class="headline" x="769" y="235" font-size="22">02 TRACE</text>
<text class="headline" x="769" y="287" font-size="22">03 SOLVE</text>
<path d="M772 318H926" stroke="{BORDER}" stroke-width="4"/>
<text x="772" y="350" font-size="12">GENERATED MAZE</text>
<text x="772" y="372" font-size="12">SOLUTION PATH</text>
<text x="32" y="428" font-size="12">IN → EXPLORE → OUT</text>
<text x="928" y="428" font-size="12" text-anchor="end">A STUDY IN PROBLEM SOLVING</text>
''')


def terrain(phase):
    mesh = []
    for row in range(17):
        depth = row / 16
        line = []
        for col in range(25):
            u = col / 12 - 1
            height = 95 * exp(-((u + .35) ** 2 * 12 + (depth - .55) ** 2 * 22))
            height += 70 * exp(-((u - .4) ** 2 * 18 + (depth - .7) ** 2 * 28))
            height += 10 * sin(u * 7 + phase) * sin(depth * pi)
            x, y = 480 + u * (110 + 320 * depth), 182 + 190 * depth - height
            assert 32 <= x <= 928 and 115 <= y <= 380
            line.append(f'{x:.1f},{y:.1f}')
        mesh.append(line)
    return ['M' + ' L'.join(line) for line in mesh] + [
        'M' + ' L'.join(line[col] for line in mesh) for col in range(25)
    ]


def landscape_panel():
    frames = [terrain(phase) for phase in (0, pi / 2, pi, 3 * pi / 2, 0)]
    paths = []
    for index, path in enumerate(frames[0]):
        color = TEXT if index % 4 == 0 else BORDER
        values = ';'.join(frame[index] for frame in frames)
        paths.append(f'<path d="{path}" fill="none" stroke="{color}"><animate attributeName="d" values="{values}" dur="10s" repeatCount="indefinite"/></path>')
    still = ''.join(f'<path d="{path}" fill="none" stroke="{BORDER}"/>' for path in frames[0])
    return panel(440, 'Animated wireframe landscape: a grayscale terrain mesh with gently shifting contours', f'''
<text class="headline" x="32" y="77" font-size="38">&gt; TERRAIN / RENDER_</text>
<text x="928" y="50" text-anchor="end" font-size="14">02 / WIREFRAME</text>
<text x="928" y="77" text-anchor="end" font-size="12">PROCEDURAL LANDSCAPE</text>
<path d="M32 106H928" stroke="{BORDER}"/>
<path d="M32 142h16m-8 -8v16 M912 142h16m-8 -8v16 M32 368h16m-8 -8v16 M912 368h16m-8 -8v16" stroke="{BORDER}"/>
<text x="64" y="145" font-size="11">MESH / 25 × 17</text>
<text x="896" y="145" text-anchor="end" font-size="11">X / Y / Z</text>
<g class="fx">{''.join(paths)}</g>
<g class="still">{still}</g>
<path d="M32 394H928" stroke="{BORDER}"/>
<text x="32" y="420" font-size="12">FORM → CONTOUR → SURFACE</text>
<text x="928" y="420" text-anchor="end" font-size="12">GENERATIVE ART / LOOP 10s</text>
''')


def render():
    portrait_bytes = (ROOT / 'assets' / 'subaru.webp').read_bytes()
    assert len(portrait_bytes) < 100_000, 'Resize the embedded portrait before rendering'
    portrait = b64encode(portrait_bytes).decode('ascii')
    hero = panel(370, f'{CONFIG["name_line_1"]} — {CONFIG["role"]}, with pixel portrait artwork', f'''
<rect x="32" y="36" width="292" height="26" fill="{TEXT}"/>
<text x="42" y="54" font-size="14" letter-spacing="2" style="fill:var(--paper)">~/profile $ whoami</text>
<text x="32" y="224" font-size="16" letter-spacing="2">{escape(CONFIG["role"])}</text>
<text class="headline" x="28" y="128" font-size="68">{escape(CONFIG["name_line_1"])}</text>
<rect class="bit" x="340" y="114" width="18" height="14" fill="{TEXT}"/>
<text class="headline" x="30" y="183" font-size="43">{escape(CONFIG["name_line_2"])}</text>
<text x="32" y="261" font-size="15">{escape(CONFIG["tagline"])}</text>
<path d="M32 328H928" stroke="{BORDER}"/>
<text x="32" y="350" font-size="12">{escape(CONFIG["footer"])}</text>
<text x="928" y="350" text-anchor="end" font-size="12">{escape(CONFIG["location"])}</text>
<path d="M932 54V322H662" stroke="{BORDER}" stroke-width="4" fill="none"/>
<rect x="656" y="48" width="272" height="268" fill="none" stroke="{TEXT}" stroke-width="2"/>
<image x="660" y="50" width="264" height="264" preserveAspectRatio="xMidYMid meet" style="image-rendering:pixelated" href="data:image/webp;base64,{portrait}"/>
''')
    steps = []
    for index, label in enumerate(('UNDERSTAND', 'PLAN', 'BUILD', 'TEST', 'IMPROVE')):
        x = index * 192
        steps.append(f'''
<path d="M{max(8, x)} 32V96" stroke="{BORDER}"/>
<text class="headline" x="{x + 20}" y="57" font-size="25">0{index + 1}</text>
<rect class="bit" x="{x + 155}" y="40" width="14" height="14" fill="{TEXT}" style="animation-delay:-{index * .8}s"/>
<text x="{x + 20}" y="88" font-size="17">{label}</text>''')
    return {
        'profile.svg': hero,
        'workflow.svg': panel(112, 'Understand → Plan → Build → Test → Improve', ''.join(steps)),
        'maze.svg': maze_panel(),
        'landscape.svg': landscape_panel(),
    }


def check(artwork):
    for svg in artwork.values():
        root = ElementTree.fromstring(svg)
        assert root.find('{http://www.w3.org/2000/svg}title').text
        assert 'prefers-reduced-motion: reduce' in svg
        assert 'prefers-color-scheme: dark' in svg
        assert not any(node.get('width') == '960' and node.get('height') == root.get('height')
                       for node in root.findall('{http://www.w3.org/2000/svg}rect'))
        assert set(re.findall(r'#[0-9A-Fa-f]{6}\b', svg)) <= {BACKGROUND, TEXT, BORDER}
        for node in root.iter():
            for attr in ('fill', 'stroke'):
                assert node.get(attr, 'none') in {BACKGROUND, TEXT, BORDER, 'none'}
    assert len(maze(1, 1)[1]) == 1
    maze(2, 3)
    assert len(terrain(0)) == 42
    assert terrain(0) != terrain(pi / 2)
    portrait = ElementTree.fromstring(artwork['profile.svg']).find('{http://www.w3.org/2000/svg}image')
    assert portrait.get('width') == portrait.get('height')
    assert portrait.get('preserveAspectRatio') == 'xMidYMid meet'
    assert 'image-rendering:pixelated' in portrait.get('style')


if __name__ == '__main__':
    artwork = render()
    check(artwork)
    (ROOT / 'assets').mkdir(exist_ok=True)
    for name, svg in artwork.items():
        (ROOT / 'assets' / name).write_text(svg, encoding='utf-8')
    print('Generated 4 animated panels. Maze, terrain, SVG markup, and grayscale palette checked.')
