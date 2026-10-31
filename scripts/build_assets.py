import json, os, textwrap, html
from pathlib import Path

ROOT = Path('/mnt/data/HiroSaito04')
ASSETS = ROOT / 'assets'
DATA = json.loads((ROOT / 'profile.json').read_text(encoding='utf-8'))

ASSETS.mkdir(exist_ok=True)

def esc(s):
    return html.escape(str(s))

def wrap_text(text, width):
    return textwrap.wrap(text, width=width, break_long_words=False, break_on_hyphens=False)

# Theme
bg = '#0b1020'
panel = '#111a33'
panel2 = '#132040'
stroke = '#24345e'
muted = '#a7b6d6'
text = '#eef4ff'
accent = '#5eead4'
accent2 = '#60a5fa'
accent3 = '#c084fc'
accent4 = '#f59e0b'

name = DATA['display_name']
username = DATA['username']
headline = DATA['headline']
subheadline = DATA['subheadline']
tagline = DATA['tagline']
location = DATA['location']
status = DATA['status']
focus = DATA['focus']
frontend = DATA['stack']['frontend']
backend = DATA['stack']['backend']
database = DATA['stack']['database']
design = DATA['stack']['design_media']
tools = DATA['stack']['tools']
workflow = DATA['workflow']


def pill(x, y, label, fill, stroke_color=None, tcolor='#eef4ff', size=16, pad_x=16, height=36):
    stroke_attr = f'stroke="{stroke_color or fill}" stroke-width="1"' if stroke_color is not None else ''
    width = max(120, 18 + len(label) * (size * 0.58))
    return f'''<g transform="translate({x},{y})">
      <rect rx="18" ry="18" width="{width:.0f}" height="{height}" fill="{fill}" {stroke_attr}/>
      <text x="{width/2:.1f}" y="24" text-anchor="middle" font-size="{size}" fill="{tcolor}" font-family="Segoe UI, Inter, Arial">{esc(label)}</text>
    </g>''', width

# HERO SVG
hero_focus = ["WEB APPS", "UI / UX", "MULTIMEDIA", "CREATIVE TECH"]
hero_pills = []
x = 70
for i, item in enumerate(hero_focus):
    g, w = pill(x, 360, item, '#102246', '#27406f', '#dfe9ff', size=16)
    hero_pills.append(g)
    x += w + 14

hero_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="520" viewBox="0 0 1200 520" fill="none">
  <defs>
    <linearGradient id="bggrad" x1="0" y1="0" x2="1200" y2="520" gradientUnits="userSpaceOnUse">
      <stop stop-color="#0B1020"/>
      <stop offset="0.55" stop-color="#111936"/>
      <stop offset="1" stop-color="#0D1430"/>
    </linearGradient>
    <linearGradient id="accentLine" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#5EEAD4"/>
      <stop offset="0.5" stop-color="#60A5FA"/>
      <stop offset="1" stop-color="#C084FC"/>
    </linearGradient>
    <linearGradient id="glass" x1="0" y1="0" x2="1" y2="1">
      <stop stop-color="#152347" stop-opacity="0.95"/>
      <stop offset="1" stop-color="#0D1733" stop-opacity="0.82"/>
    </linearGradient>
    <filter id="blurGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="30" result="blur"/>
    </filter>
  </defs>

  <rect width="1200" height="520" rx="28" fill="url(#bggrad)"/>
  <circle cx="960" cy="115" r="110" fill="#60A5FA" fill-opacity="0.16" filter="url(#blurGlow)"/>
  <circle cx="1080" cy="320" r="95" fill="#C084FC" fill-opacity="0.13" filter="url(#blurGlow)"/>
  <circle cx="760" cy="420" r="120" fill="#5EEAD4" fill-opacity="0.11" filter="url(#blurGlow)"/>

  <g opacity="0.35">
    <path d="M0 120H1200" stroke="#203157"/>
    <path d="M0 200H1200" stroke="#203157"/>
    <path d="M0 280H1200" stroke="#203157"/>
    <path d="M0 360H1200" stroke="#203157"/>
    <path d="M0 440H1200" stroke="#203157"/>
    <path d="M160 0V520" stroke="#203157"/>
    <path d="M320 0V520" stroke="#203157"/>
    <path d="M480 0V520" stroke="#203157"/>
    <path d="M640 0V520" stroke="#203157"/>
    <path d="M800 0V520" stroke="#203157"/>
    <path d="M960 0V520" stroke="#203157"/>
    <path d="M1120 0V520" stroke="#203157"/>
  </g>

  <rect x="50" y="50" width="650" height="420" rx="30" fill="url(#glass)" stroke="#27406F"/>
  <text x="72" y="90" font-size="14" letter-spacing="2" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">PROFILE OVERVIEW</text>
  <text x="72" y="168" font-size="62" font-weight="700" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">{esc(name)}</text>
  <text x="72" y="204" font-size="24" fill="#5EEAD4" font-family="Segoe UI, Inter, Arial">@{esc(username)}</text>
  <text x="72" y="260" font-size="30" font-weight="600" fill="#DCE8FF" font-family="Segoe UI, Inter, Arial">{esc(headline)}</text>
  <text x="72" y="300" font-size="22" fill="#A7B6D6" font-family="Segoe UI, Inter, Arial">{esc(subheadline)}</text>
  <text x="72" y="332" font-size="19" fill="#CCD8F4" font-family="Segoe UI, Inter, Arial">{esc(tagline)}</text>
  {''.join(hero_pills)}
  <text x="72" y="428" font-size="16" letter-spacing="1" fill="#9EB2DA" font-family="Segoe UI, Inter, Arial">STATUS  //  {esc(status)}</text>
  <text x="72" y="455" font-size="16" letter-spacing="1" fill="#9EB2DA" font-family="Segoe UI, Inter, Arial">LOCATION //  {esc(location)}</text>

  <g transform="translate(750,58)">
    <rect width="398" height="404" rx="28" fill="#0E1835" stroke="#27406F"/>
    <text x="28" y="42" font-size="14" letter-spacing="2" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">FOCUS AREAS</text>
    <rect x="26" y="70" width="346" height="88" rx="22" fill="#122348" stroke="#24406E"/>
    <rect x="26" y="176" width="346" height="88" rx="22" fill="#10213F" stroke="#24406E"/>
    <rect x="26" y="282" width="346" height="88" rx="22" fill="#0F1C39" stroke="#24406E"/>

    <circle cx="68" cy="114" r="18" fill="#5EEAD4" fill-opacity="0.18" stroke="#5EEAD4"/>
    <circle cx="68" cy="220" r="18" fill="#60A5FA" fill-opacity="0.18" stroke="#60A5FA"/>
    <circle cx="68" cy="326" r="18" fill="#C084FC" fill-opacity="0.18" stroke="#C084FC"/>

    <text x="100" y="108" font-size="14" letter-spacing="1" fill="#86A4D5" font-family="Segoe UI, Inter, Arial">01</text>
    <text x="100" y="130" font-size="24" font-weight="600" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">{esc(focus[0])}</text>
    <text x="100" y="151" font-size="15" fill="#B8C8E8" font-family="Segoe UI, Inter, Arial">Building practical and responsive user experiences.</text>

    <text x="100" y="214" font-size="14" letter-spacing="1" fill="#86A4D5" font-family="Segoe UI, Inter, Arial">02</text>
    <text x="100" y="236" font-size="24" font-weight="600" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">{esc(focus[1])}</text>
    <text x="100" y="257" font-size="15" fill="#B8C8E8" font-family="Segoe UI, Inter, Arial">Designing clean layouts, interfaces, and visuals.</text>

    <text x="100" y="320" font-size="14" letter-spacing="1" fill="#86A4D5" font-family="Segoe UI, Inter, Arial">03</text>
    <text x="100" y="342" font-size="24" font-weight="600" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">{esc(focus[2])}</text>
    <text x="100" y="363" font-size="15" fill="#B8C8E8" font-family="Segoe UI, Inter, Arial">Producing digital content and creative assets.</text>
  </g>
</svg>'''
(ASSETS / 'hero.svg').write_text(hero_svg, encoding='utf-8')

# STACK SVG
categories = [
    ('FRONTEND', frontend, accent),
    ('BACKEND', backend, accent2),
    ('DATABASE', database, accent3),
    ('DESIGN / MEDIA', design, accent4),
    ('TOOLS', tools, '#34D399'),
]

cards = []
start_y = 62
for idx, (title, items, color) in enumerate(categories):
    y = start_y + idx * 94
    cards.append(f'''<g transform="translate(50,{y})">
      <rect width="1100" height="74" rx="20" fill="#101A35" stroke="#23375F"/>
      <rect x="20" y="18" width="180" height="38" rx="14" fill="{color}" fill-opacity="0.14" stroke="{color}"/>
      <text x="110" y="43" text-anchor="middle" font-size="18" font-weight="600" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">{esc(title)}</text>
      <text x="230" y="44" font-size="20" fill="#CBD9F5" font-family="Segoe UI, Inter, Arial">{esc('  •  '.join(items))}</text>
    </g>''')

stack_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="560" viewBox="0 0 1200 560" fill="none">
  <rect width="1200" height="560" rx="28" fill="#0B1020"/>
  <rect x="26" y="26" width="1148" height="508" rx="26" fill="#0F1730" stroke="#22345C"/>
  <text x="52" y="58" font-size="14" letter-spacing="2" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">TOOLKIT SNAPSHOT</text>
  {''.join(cards)}
</svg>'''
(ASSETS / 'stack.svg').write_text(stack_svg, encoding='utf-8')

# JOURNEY SVG
steps = [
    ('DISCOVER', workflow[0], accent),
    ('DESIGN', workflow[1], accent2),
    ('BUILD', workflow[2], accent3),
    ('REFINE', workflow[3], '#34D399'),
    ('SHIP', workflow[4], accent4),
]
parts = []
for i, (title, desc, color) in enumerate(steps):
    x = 50 + i * 220
    connector = ''
    if i < len(steps)-1:
        connector = f'<path d="M{x+150} 190 H {x+214}" stroke="#355487" stroke-width="3" stroke-linecap="round" stroke-dasharray="10 10"/>'
    lines = wrap_text(desc, 26)
    text_lines = ''.join([f'<text x="{x+26}" y="{238 + j*18}" font-size="14" fill="#CBD9F5" font-family="Segoe UI, Inter, Arial">{esc(line)}</text>' for j,line in enumerate(lines)])
    parts.append(f'''<g>
      <rect x="{x}" y="110" width="170" height="170" rx="22" fill="#101A35" stroke="#23375F"/>
      <circle cx="{x+42}" cy="150" r="16" fill="{color}" fill-opacity="0.17" stroke="{color}"/>
      <text x="{x+42}" y="155" text-anchor="middle" font-size="14" font-weight="700" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">{i+1}</text>
      <text x="{x+72}" y="145" font-size="15" letter-spacing="1" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">STEP</text>
      <text x="{x+26}" y="188" font-size="24" font-weight="600" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">{esc(title)}</text>
      {text_lines}
    </g>
    {connector}''')

journey_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="360" viewBox="0 0 1200 360" fill="none">
  <rect width="1200" height="360" rx="28" fill="#0B1020"/>
  <rect x="26" y="26" width="1148" height="308" rx="26" fill="#0F1730" stroke="#22345C"/>
  <text x="52" y="58" font-size="14" letter-spacing="2" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">WORKFLOW MAP</text>
  {''.join(parts)}
</svg>'''
(ASSETS / 'journey.svg').write_text(journey_svg, encoding='utf-8')

# FOCUS / CARDS SVG
left_lines = wrap_text("I enjoy building responsive interfaces, shaping cleaner user experiences, and blending development with multimedia creativity.", 42)
left_text = ''.join([f'<text x="74" y="{135 + i*24}" font-size="22" fill="#DCE8FF" font-family="Segoe UI, Inter, Arial">{esc(line)}</text>' for i,line in enumerate(left_lines)])

pill_groups = []
pill_items = [
    ('MERN STACK', '#112448', '#5EEAD4'),
    ('RESPONSIVE UI', '#12213F', '#60A5FA'),
    ('VIDEO EDITING', '#101D3A', '#C084FC'),
    ('BRANDING', '#10203C', '#F59E0B'),
    ('CONTENT CREATION', '#112448', '#34D399'),
    ('PROBLEM SOLVING', '#12213F', '#F472B6'),
]
x_positions = [72, 285, 524, 72, 316, 570]
y_positions = [248, 248, 248, 302, 302, 302]
for (label, fillc, scol), x, y in zip(pill_items, x_positions, y_positions):
    pill_groups.append(f'<rect x="{x}" y="{y}" width="190" height="38" rx="18" fill="{fillc}" stroke="{scol}"/>\n<text x="{x+95}" y="{y+24}" text-anchor="middle" font-size="15" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">{esc(label)}</text>')

focus_svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="420" viewBox="0 0 1200 420" fill="none">
  <rect width="1200" height="420" rx="28" fill="#0B1020"/>
  <rect x="30" y="30" width="720" height="360" rx="28" fill="#101A35" stroke="#23375F"/>
  <rect x="780" y="30" width="390" height="360" rx="28" fill="#0F1730" stroke="#23375F"/>
  <text x="70" y="74" font-size="14" letter-spacing="2" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">ABOUT / NOW</text>
  <text x="70" y="112" font-size="34" font-weight="700" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">Creating with code, design, and media.</text>
  {left_text}
  {''.join(pill_groups)}
  <text x="810" y="74" font-size="14" letter-spacing="2" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">CURRENTLY</text>
  <rect x="810" y="96" width="330" height="74" rx="20" fill="#122348" stroke="#24406E"/>
  <rect x="810" y="182" width="330" height="74" rx="20" fill="#10213F" stroke="#24406E"/>
  <rect x="810" y="268" width="330" height="74" rx="20" fill="#0F1C39" stroke="#24406E"/>
  <text x="834" y="124" font-size="14" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">BUILDING</text>
  <text x="834" y="148" font-size="22" font-weight="600" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">Developer portfolio & practice projects</text>
  <text x="834" y="210" font-size="14" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">LEARNING</text>
  <text x="834" y="234" font-size="22" font-weight="600" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">Full-stack development & UI thinking</text>
  <text x="834" y="296" font-size="14" fill="#8AA5D6" font-family="Segoe UI, Inter, Arial">GOAL</text>
  <text x="834" y="320" font-size="22" font-weight="600" fill="#EEF4FF" font-family="Segoe UI, Inter, Arial">Meaningful, polished digital experiences</text>
</svg>'''
(ASSETS / 'focus.svg').write_text(focus_svg, encoding='utf-8')

print('Assets generated successfully.')
