from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'assets'
SRC = ROOT / 'source_assets'

# ---------- helpers ----------
def load(name):
    return Image.open(name).convert('RGBA')

def upscale(img, scale):
    return img.resize((img.width * scale, img.height * scale), Image.Resampling.NEAREST)

try:
    FONT_BIG = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
    FONT_MED = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 20)
    FONT_SML = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 16)
except:
    FONT_BIG = FONT_MED = FONT_SML = ImageFont.load_default()

NAVY = '#1d2d50'
PANEL = '#25385d'
CREAM = '#fff2cf'
GOLD = '#ffd34f'
PINK = '#ffb0c6'
BLUE = '#a3d7ff'
GREEN = '#7ecf6a'
SHADOW = (0,0,0,170)

boy = load(ASSETS / 'boy_down.png')
player = {i: load(SRC / 'sprites' / f'player{i}.png') for i in range(1,13)}
brio = {i: load(SRC / 'sprites' / f'brio{i}.png') for i in range(1,13)}
tree = load(SRC / 'greeneries' / 'tree.png')
shrub = load(SRC / 'greeneries' / 'shrub_01.png')
cafe = load(SRC / 'buildings' / 'Cafe1.png')
red_house = load(SRC / 'buildings' / 'Red 01.png')
blue_house = load(SRC / 'buildings' / 'Blue 01.png')

# user-provided mapping:
# 1 static down, 2/3 moving down, 4 static left, 5/6 moving left,
# 7 static right, 8/9 moving right, 10 static up, 11/12 moving up

def player_frame(direction, step):
    if direction == 'down':
        return player[1] if step is None else player[2 if step % 2 == 0 else 3]
    if direction == 'left':
        return player[4] if step is None else player[5 if step % 2 == 0 else 6]
    if direction == 'right':
        return player[7] if step is None else player[8 if step % 2 == 0 else 9]
    return player[10] if step is None else player[11 if step % 2 == 0 else 12]

def brio_frame(direction, step):
    if direction == 'down':
        return brio[1] if step is None else brio[2 if step % 2 == 0 else 3]
    if direction == 'left':
        return brio[4] if step is None else brio[5 if step % 2 == 0 else 6]
    if direction == 'right':
        return brio[7] if step is None else brio[8 if step % 2 == 0 else 9]
    return brio[10] if step is None else brio[11 if step % 2 == 0 else 12]

def panel(draw, xy, fill=NAVY, outline=CREAM, width=4, radius=16):
    draw.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)

def t(draw, xy, text, font, fill, anchor=None):
    x, y = xy
    draw.text((x+2, y+2), text, font=font, fill=SHADOW, anchor=anchor)
    draw.text((x, y), text, font=font, fill=fill, anchor=anchor)

def paste_scaled(base, sprite, x, y, scale):
    base.alpha_composite(upscale(sprite, scale), (x, y))

def draw_sky(img):
    d = ImageDraw.Draw(img)
    w, h = img.size
    for y in range(h):
        r = int(126 + (40*y/h))
        g = int(181 + (30*y/h))
        b = int(235 + (10*y/h))
        d.line((0,y,w,y), fill=(r,g,b,255))
    # clouds
    for cx, cy in [(120,50),(330,78),(780,62),(1040,48)]:
        for dx,dy,r in [(-20,8,20),(0,0,24),(20,8,18),(42,12,14)]:
            d.ellipse((cx+dx-r, cy+dy-r, cx+dx+r, cy+dy+r), fill=(255,255,255,220))

def make_hero():
    img = Image.new('RGBA', (1200, 360), (0,0,0,0))
    draw_sky(img)
    d = ImageDraw.Draw(img)
    d.rectangle((0,250,1200,360), fill='#6ec25d')
    d.rectangle((0,285,1200,322), fill='#cdb07a')
    d.rectangle((0,322,1200,360), fill='#58ae48')
    panel(d, (24,22,706,175), fill='#1f2f52ee', outline=CREAM, radius=22)
    panel(d, (762,22,1172,175), fill='#1f2f52ee', outline=GOLD, radius=22)
    t(d, (46,48), 'PIXEL PATHFINDER', FONT_BIG, GOLD)
    t(d, (46,86), 'MIKE ANGELO A. RUBIA', FONT_BIG, CREAM)
    t(d, (46,124), 'FULL STACK DEVELOPER', FONT_MED, BLUE)
    t(d, (46,152), '@HiroSaito04', FONT_MED, PINK)
    t(d, (790,48), 'PLAYER PROFILE', FONT_BIG, CREAM)
    t(d, (790,92), 'WORLD:', FONT_MED, GOLD); t(d, (915,92), 'Portfolio Realm', FONT_MED, CREAM)
    t(d, (790,124), 'TYPE:', FONT_MED, GOLD); t(d, (915,124), 'Build • Design • Learn', FONT_MED, CREAM)
    # profile sprite box
    d.rounded_rectangle((1035,60,1145,160), radius=14, fill='#334d7f', outline=CREAM, width=3)
    paste_scaled(img, boy.resize((32,32), Image.Resampling.NEAREST), 1060, 84, 2)
    # scenery
    paste_scaled(img, tree, 36, 186, 2)
    paste_scaled(img, cafe, 790, 176, 1)
    paste_scaled(img, red_house, 952, 172, 1)
    paste_scaled(img, tree, 1060, 214, 2)
    paste_scaled(img, player_frame('right', 0), 625, 220, 3)
    img.save(ASSETS / 'hero.png')

def make_savefile():
    img = Image.new('RGBA', (1200, 320), (0,0,0,0))
    d = ImageDraw.Draw(img)
    panel(d, (16,16,1184,304), fill='#24375dee', outline=CREAM, radius=22)
    t(d, (42, 42), 'SAVE FILE 01', FONT_BIG, GOLD)
    t(d, (42, 92), 'NAME: Mike Angelo A. Rubia', FONT_MED, CREAM)
    t(d, (42, 132), 'ROLE: Full Stack Developer', FONT_MED, BLUE)
    t(d, (42, 172), 'HANDLE: @HiroSaito04', FONT_MED, PINK)
    t(d, (42, 212), 'PORTFOLIO: mr-zhiroark-portfolio.vercel.app', FONT_MED, '#d8f4a2')
    t(d, (42, 252), 'STATUS: Active • Building • Exploring', FONT_MED, CREAM)
    # avatar frame
    d.rounded_rectangle((886,52,1128,268), radius=20, fill='#314a7a', outline=GOLD, width=4)
    t(d, (1008, 70), 'PROFILE', FONT_MED, CREAM, anchor='ma')
    scaled = boy.resize((48,48), Image.Resampling.NEAREST)
    paste_scaled(img, scaled, 956, 104, 2)
    t(d, (1008, 230), 'boy_down.png', FONT_SML, PINK, anchor='ma')
    img.save(ASSETS / 'save-file.png')

def make_buttons():
    for fn, text, fill, outline in [
        ('button-portfolio.png','OPEN PORTFOLIO','#2c4670ee',BLUE),
        ('button-github.png','OPEN GITHUB','#533353ee',PINK),
    ]:
        img = Image.new('RGBA', (500, 84), (0,0,0,0))
        d = ImageDraw.Draw(img)
        panel(d, (4,4,496,80), fill=fill, outline=outline, radius=16)
        t(d, (250, 28), text, FONT_BIG, CREAM, anchor='ma')
        img.save(ASSETS / fn)

def make_pathfinder():
    # animated map inspired by village.tmx layout
    W, H = 1200, 520
    tile = 48
    origin_x, origin_y = 36, 90
    path = [(1,8),(2,8),(3,8),(4,8),(5,8),(6,8),(6,7),(6,6),(6,5),(7,5),(8,5),(9,5),(10,5),(10,6),(10,7),(11,7),(12,7),(13,7)]
    # densify frames
    moves=[]
    for i in range(len(path)-1):
        x1,y1 = path[i]; x2,y2 = path[i+1]
        direction='right' if x2>x1 else 'left' if x2<x1 else 'down' if y2>y1 else 'up'
        moves.append((x1,y1,direction,0))
        moves.append(((x1+x2)/2,(y1+y2)/2,direction,1))
    moves.append((path[-1][0], path[-1][1], 'right', None))
    frames=[]
    for px,py,direction,step in moves:
        img=Image.new('RGBA',(W,H),(0,0,0,0))
        draw_sky(img)
        d = ImageDraw.Draw(img)
        d.rectangle((0,70,W,H), fill='#6fbe5f')
        panel(d,(18,18,W-18,H-18), fill='#213154ee', outline=CREAM, radius=20)
        t(d,(28,28),'PATHFINDER // VILLAGE MAP', FONT_BIG, GOLD)
        # map board
        d.rounded_rectangle((32,72,930,486), radius=18, fill='#72c162', outline=CREAM, width=3)
        # subtle grid
        for c in range(0, 18):
            x = origin_x + c*tile
            d.line((x,74,x,484), fill='#67aa57')
        for r in range(0, 9):
            y = origin_y + r*tile
            d.line((34,y,928,y), fill='#67aa57')
        # road/path
        for c,r in path:
            d.rounded_rectangle((origin_x+c*tile+6, origin_y+r*tile+6, origin_x+(c+1)*tile-6, origin_y+(r+1)*tile-6), radius=8, fill='#d4b37e', outline='#b88f5a')
        # buildings/props inspired by village.tmx
        paste_scaled(img, cafe, 44, 188, 1)
        paste_scaled(img, blue_house, 290, 148, 1)
        paste_scaled(img, red_house, 500, 100, 1)
        paste_scaled(img, tree, 152, 106, 2)
        paste_scaled(img, tree, 702, 108, 2)
        paste_scaled(img, tree, 790, 316, 2)
        paste_scaled(img, shrub, 264, 332, 2)
        paste_scaled(img, shrub, 638, 372, 2)
        # signposts / legend
        for pos, label, color in [((1,8),'START',PINK),((6,5),'PORTFOLIO',BLUE),((10,7),'PROFILE',GOLD),((13,7),'GOAL',CREAM)]:
            c,r=pos
            cx=origin_x+c*tile+24; cy=origin_y+r*tile-8
            d.rounded_rectangle((cx-30,cy-16,cx+30,cy+8), radius=8, fill='#2c4670', outline=color, width=2)
            t(d,(cx,cy-10),label,FONT_SML,color,anchor='ma')
        # right info panel
        panel(d,(952,84,1164,472), fill='#2b3f69ee', outline=GOLD, radius=18)
        t(d,(972,108),'QUEST LOG', FONT_MED, CREAM)
        info=[
            '01  Start at the village gate',
            '02  Walk the main road',
            '03  Reach the portfolio zone',
            '04  View the profile save file',
            '05  Continue to contribution'
        ]
        y=148
        for line in info:
            t(d,(972,y),line,FONT_SML,'#e6f3ff'); y += 38
        t(d,(972,370),'PLAYER SPRITE:', FONT_SML, GOLD)
        paste_scaled(img, player_frame(direction, step), 1030, 396, 2)
        # moving player on map
        sx = int(origin_x + px*tile + 6)
        sy = int(origin_y + py*tile - 6)
        paste_scaled(img, player_frame(direction, step), sx, sy, 2)
        frames.append(img.convert('P', palette=Image.Palette.ADAPTIVE))
    frames[0].save(ASSETS / 'pathfinder.gif', save_all=True, append_images=frames[1:], duration=170, loop=0, disposal=2)

def make_contribution():
    W,H = 1200, 360
    cell = 42
    gx, gy = 44, 94
    cols, rows = 16, 6
    positions=[]
    for r in range(rows):
        c_range = range(cols) if r % 2 == 0 else range(cols-1,-1,-1)
        for c in c_range:
            positions.append((c,r))
    frames=[]
    for idx,(pc,pr) in enumerate(positions[::2]):
        img=Image.new('RGBA',(W,H),(0,0,0,0))
        d = ImageDraw.Draw(img)
        panel(d,(16,16,W-16,H-16), fill='#203152ee', outline=CREAM, radius=20)
        t(d,(30,30),'CONTRIBUTION ACTIVITY', FONT_BIG, GOLD)
        # original centered contribution design feeling
        for r in range(rows):
            for c in range(cols):
                palette = ['#2d3d61','#315c3c','#3f8c4a','#62c85d']
                color = palette[(c+r) % 4]
                d.rounded_rectangle((gx+c*cell, gy+r*cell, gx+c*cell+32, gy+r*cell+32), radius=6, fill=color, outline='#0f1728')
        # section note at right
        panel(d,(760,78,1148,308), fill='#2b3f69ee', outline=GOLD, radius=18)
        t(d,(784,102),'BRIO REPLACES THE SNAKE', FONT_MED, CREAM)
        notes=[
            'Original contribution section style',
            'is kept, but the animated player',
            'for this activity is Brio.',
            '',
            'Sprite set used: brio1..12',
            'Character moves across the',
            'contribution grid instead of',
            'the old snake animation.'
        ]
        y=138
        for line in notes:
            if line:
                t(d,(784,y),line,FONT_SML,'#e7f2ff')
            y += 22
        # move brio across contributions
        next_c,next_r = positions[min((idx+1)*2, len(positions)-1)]
        direction = 'right' if next_c>pc else 'left' if next_c<pc else 'down'
        frame = brio_frame(direction, idx)
        x = gx + pc*cell - 10
        y = gy + pr*cell - 4
        paste_scaled(img, frame, x, y, 2)
        paste_scaled(img, brio_frame(direction, idx), 926, 236, 2)
        t(d,(938,214),'BRIO', FONT_SML, PINK, anchor='ma')
        frames.append(img.convert('P', palette=Image.Palette.ADAPTIVE))
    frames[0].save(ASSETS / 'contribution-brio.gif', save_all=True, append_images=frames[1:], duration=120, loop=0, disposal=2)


def main():
    ASSETS.mkdir(exist_ok=True)
    make_hero()
    make_savefile()
    make_buttons()
    make_pathfinder()
    make_contribution()

if __name__ == '__main__':
    main()
