from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import math

ROOT = Path('/mnt/data/HiroSaito04')
ASSET_SRC = Path('/mnt/data/_assets_unzip/assets')
OUT = ROOT / 'assets'
OUT.mkdir(exist_ok=True)

# ---------- helpers ----------

def load(p):
    return Image.open(p).convert('RGBA')

def upscale(img, scale=4):
    return img.resize((img.width*scale, img.height*scale), Image.Resampling.NEAREST)

# fallback font (bitmap-like if available, otherwise default)
try:
    FONT_BIG = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 28)
    FONT_MED = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf', 18)
    FONT_SML = ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf', 16)
except:
    FONT_BIG = FONT_MED = FONT_SML = ImageFont.load_default()

PALETTE = {
    'bg': '#80bff2',
    'panel': '#1f2a44',
    'panel2': '#324667',
    'ink': '#102030',
    'cream': '#f9f4da',
    'grass': '#74c365',
    'gold': '#f8cf55',
    'pink': '#ff7ba5',
    'blue': '#68a6ff',
    'shadow': '#00000066'
}

# selected source assets
TREE = load(ASSET_SRC / 'tiles&objects/greeneries/tree.png')
BUSH = load(ASSET_SRC / 'tiles&objects/game/berry_bush.png')
COIN = load(ASSET_SRC / 'tiles&objects/game/coin.png')
STAR = load(ASSET_SRC / 'tiles&objects/game/star.png')
HEART = load(ASSET_SRC / 'tiles&objects/game/heart.png')
PIN = load(ASSET_SRC / 'tiles&objects/game/pin.png')
BOOK = load(ASSET_SRC / 'tiles&objects/game/book.png')
POTION = load(ASSET_SRC / 'tiles&objects/game/potion.png')
CRATE = load(ASSET_SRC / 'tiles&objects/furniture/crate.png')
TABLE = load(ASSET_SRC / 'tiles&objects/furniture/table_wood.png')
HOUSE = load(ASSET_SRC / 'tiles&objects/buildings/Cafe1.png')
HOUSE2 = load(ASSET_SRC / 'tiles&objects/buildings/Red 01.png')
ROAD_H = load(ASSET_SRC / 'tiles&objects/ground/02_road_h.png') if (ASSET_SRC / 'tiles&objects/ground/02_road_h.png').exists() else None
ROAD_V = load(ASSET_SRC / 'tiles&objects/ground/03_road_v.png') if (ASSET_SRC / 'tiles&objects/ground/03_road_v.png').exists() else None
ROAD_NE = load(ASSET_SRC / 'tiles&objects/ground/08_road_ne.png') if (ASSET_SRC / 'tiles&objects/ground/08_road_ne.png').exists() else None
ROAD_NW = load(ASSET_SRC / 'tiles&objects/ground/09_road_nw.png') if (ASSET_SRC / 'tiles&objects/ground/09_road_nw.png').exists() else None
ROAD_SE = load(ASSET_SRC / 'tiles&objects/ground/11_road_se.png')
ROAD_SW = load(ASSET_SRC / 'tiles&objects/ground/10_road_sw.png')
ROAD_C = load(ASSET_SRC / 'tiles&objects/ground/01_road.png') if (ASSET_SRC / 'tiles&objects/ground/01_road.png').exists() else ROAD_SE
PLAYER_R = [load(ASSET_SRC / 'characters/rumi_right0.png'), load(ASSET_SRC / 'characters/rumi_right1.png')]
PLAYER_L = [load(ASSET_SRC / 'characters/rumi_left0.png'), load(ASSET_SRC / 'characters/rumi_left1.png')]
PLAYER_D = [load(ASSET_SRC / 'characters/rumi_down0.png'), load(ASSET_SRC / 'characters/rumi_down1.png')]
PLAYER_U = [load(ASSET_SRC / 'characters/rumi_up0.png'), load(ASSET_SRC / 'characters/rumi_up1.png')]

TILE = 32
SCALE = 4

# ---------- primitive drawings ----------

def rounded_panel(img, xy, fill, outline, radius=16, width=3):
    d = ImageDraw.Draw(img)
    d.rounded_rectangle(xy, radius=radius, fill=fill, outline=outline, width=width)


def text_with_shadow(draw, pos, text, font, fill, shadow=(0,0,0,160), offset=(2,2), anchor=None):
    x,y = pos
    draw.text((x+offset[0], y+offset[1]), text, font=font, fill=shadow, anchor=anchor)
    draw.text((x,y), text, font=font, fill=fill, anchor=anchor)


def paste_scaled(base, sprite, x, y, scale=SCALE):
    base.alpha_composite(upscale(sprite, scale), (x, y))


def draw_sky(bg, w, h):
    d = ImageDraw.Draw(bg)
    # vertical gradient
    for y in range(h):
        t = y / max(1,h-1)
        r = int(128*(1-t) + 32*t)
        g = int(191*(1-t) + 74*t)
        b = int(242*(1-t) + 98*t)
        d.line((0,y,w,y), fill=(r,g,b,255))
    # clouds
    for cx, cy, s in [(120,80,1.2),(360,60,1.0),(650,90,1.4),(910,55,1.1)]:
        for ox, oy, rr in [(-25,10,28),(0,0,34),(28,8,26),(55,14,20)]:
            d.ellipse((cx+ox*s-rr, cy+oy*s-rr, cx+ox*s+rr, cy+oy*s+rr), fill=(255,255,255,220))


def grass_strip(img, y0):
    d = ImageDraw.Draw(img)
    d.rectangle((0,y0,img.width,img.height), fill='#75c95d')
    d.rectangle((0,y0+18,img.width,img.height), fill='#56a849')
    # tiny grass pixels
    for x in range(0,img.width,8):
        d.line((x,y0+10,x+2,y0+4), fill='#98dc7a')
        d.line((x+4,y0+11,x+6,y0+5), fill='#3f8e3d')

# ---------- compose static assets ----------

def build_hero():
    w,h = 1200,420
    img = Image.new('RGBA',(w,h),(0,0,0,0))
    draw_sky(img,w,h)
    grass_strip(img,270)
    # mountains
    d = ImageDraw.Draw(img)
    d.polygon([(0,280),(120,150),(260,280)], fill='#7d8ccd')
    d.polygon([(180,280),(370,130),(540,280)], fill='#697bc0')
    d.polygon([(450,280),(650,155),(850,280)], fill='#7d8ccd')
    d.polygon([(730,280),(930,135),(1150,280)], fill='#6c80cb')
    # panels
    rounded_panel(img, (28,28,710,200), '#1b2744ee', '#f9f4da', radius=22, width=4)
    rounded_panel(img, (760,28,1168,208), '#1b2744ee', '#f8cf55', radius=22, width=4)
    dd = ImageDraw.Draw(img)
    text_with_shadow(dd,(52,54),'PIXEL PATHFINDER', FONT_BIG, '#f8cf55')
    text_with_shadow(dd,(52,92),'MIKE ANGELO A. RUBIA', FONT_BIG, '#f9f4da')
    text_with_shadow(dd,(52,128),'FULL STACK DEVELOPER', FONT_MED, '#9dd6ff')
    text_with_shadow(dd,(52,160),'@HiroSaito04', FONT_MED, '#ffb0c8')
    # right panel stats
    text_with_shadow(dd,(790,52),'PLAYER CARD', FONT_BIG, '#f9f4da')
    stats=[('CLASS','Developer'),('WORLD','Portfolio Realm'),('QUEST','Build • Design • Learn')]
    yy=96
    for k,v in stats:
        text_with_shadow(dd,(790,yy),f'{k}:', FONT_MED, '#f8cf55')
        text_with_shadow(dd,(905,yy),v, FONT_MED, '#f9f4da')
        yy+=42

    # scenery
    paste_scaled(img,HOUSE,780,200,2)
    paste_scaled(img,HOUSE2,940,185,1)
    paste_scaled(img,TREE,50,210,2)
    paste_scaled(img,TREE,1010,220,2)
    paste_scaled(img,BUSH,310,298,3)
    paste_scaled(img,BUSH,460,304,3)
    for px in [315, 470, 860]:
        paste_scaled(img,COIN,px,250,2)
    paste_scaled(img,STAR,550,40,2)
    paste_scaled(img,HEART,584,36,2)
    # road blocks simplified
    d.rectangle((0,310,w,350), fill='#d0b581')
    d.rectangle((0,350,w,360), fill='#b6925f')
    # player
    paste_scaled(img,PLAYER_R[0],660,254,3)
    img.save(OUT/'hero.png')


def build_save_file():
    w,h=1200,320
    img=Image.new('RGBA',(w,h),(0,0,0,0))
    rounded_panel(img,(16,16,w-16,h-16),'#202d4ccc','#f9f4da',radius=24,width=4)
    d=ImageDraw.Draw(img)
    text_with_shadow(d,(44,42),'SAVE FILE 01', FONT_BIG, '#f8cf55')
    text_with_shadow(d,(44,92),'NAME: Mike Angelo A. Rubia', FONT_MED, '#f9f4da')
    text_with_shadow(d,(44,132),'ROLE: Full Stack Developer', FONT_MED, '#9dd6ff')
    text_with_shadow(d,(44,172),'HANDLE: @HiroSaito04', FONT_MED, '#ffb0c8')
    text_with_shadow(d,(44,212),'MAIN HUB: mr-zhiroark-portfolio.vercel.app', FONT_MED, '#c6f4a5')
    text_with_shadow(d,(44,252),'STATUS: Active • Building • Leveling Up', FONT_MED, '#f9f4da')
    # decorative objects
    paste_scaled(img,BOOK,930,72,3)
    paste_scaled(img,POTION,1020,74,3)
    paste_scaled(img,STAR,1110,74,2)
    paste_scaled(img,CRATE,878,182,3)
    paste_scaled(img,TABLE,972,164,3)
    paste_scaled(img,PLAYER_D[0],850,198,3)
    img.save(OUT/'save-file.png')


def pixel_button(text, color_fill, color_outline, outname, width=500):
    h=80
    img=Image.new('RGBA',(width,h),(0,0,0,0))
    rounded_panel(img,(4,4,width-4,h-4),color_fill,color_outline,radius=16,width=4)
    d=ImageDraw.Draw(img)
    text_with_shadow(d,(width//2,24),text,FONT_BIG,'#f9f4da',anchor='ma')
    img.save(OUT/outname)

# ---------- animated assets ----------

def build_pathfinder_gif():
    tile = 32*3
    cols, rows = 10, 6
    w, h = cols*tile + 340, rows*tile + 80
    path = [(0,4),(1,4),(2,4),(2,3),(3,3),(4,3),(5,3),(5,2),(6,2),(7,2),(7,3),(8,3)]
    points = {
        (0,4): ('START','Portfolio', PALETTE['blue']),
        (5,3): ('PATHFINDER','Skills / Questline', PALETTE['gold']),
        (8,3): ('CONTRIB','Contribution Zone', PALETTE['pink']),
    }
    frames=[]
    # movement positions between path cells
    positions=[]
    for i in range(len(path)-1):
        x1,y1=path[i]; x2,y2=path[i+1]
        for t in [0.0,0.5]:
            positions.append((x1+(x2-x1)*t, y1+(y2-y1)*t, x2-x1, y2-y1, i))
    positions.append((path[-1][0], path[-1][1], 0,0,len(path)-1))

    for idx,(px,py,dx,dy,seg) in enumerate(positions):
        img=Image.new('RGBA',(w,h),(0,0,0,0))
        draw_sky(img,w,h)
        grass_strip(img, rows*tile+10)
        rounded_panel(img,(16,16,w-16,h-16),'#1b2744e8','#f9f4da',radius=18,width=4)
        d=ImageDraw.Draw(img)
        text_with_shadow(d,(28,24),'PATHFINDER // QUEST MAP', FONT_BIG, '#f8cf55')
        # map board
        bx, by = 28, 64
        d.rounded_rectangle((bx,by,bx+cols*tile+20,by+rows*tile+20), radius=18, fill='#6bb15a', outline='#f9f4da', width=3)
        mx, my = bx+10, by+10
        # tiles
        for r in range(rows):
            for c in range(cols):
                d.rectangle((mx+c*tile, my+r*tile, mx+(c+1)*tile, my+(r+1)*tile), fill='#74c365', outline='#64a64f')
        # path drawn
        for c,r in path:
            d.rectangle((mx+c*tile+10,my+r*tile+10,mx+(c+1)*tile-10,my+(r+1)*tile-10), fill='#d8b47e', outline='#b78755')
        # decor
        paste_scaled(img,TREE,mx+tile*8+10,my+tile*0+4,1)
        paste_scaled(img,TREE,mx+tile*8+8,my+tile*4+4,1)
        paste_scaled(img,BUSH,mx+tile*1,my+tile*1,2)
        paste_scaled(img,BUSH,mx+tile*3,my+tile*5-18,2)
        paste_scaled(img,HOUSE, mx+tile*0-10,my+tile*3-70,1)
        paste_scaled(img,HOUSE2, mx+tile*4-20,my+tile*1-54,1)
        # markers
        for (c,r),(title,sub,color) in points.items():
            cx=mx+c*tile+tile//2; cy=my+r*tile+tile//2
            d.ellipse((cx-12,cy-12,cx+12,cy+12), fill=color, outline='#fff', width=2)
        # side legend
        rounded_panel(img,(cols*tile+70,78,w-36,h-36),'#243558dd','#f8cf55',radius=18,width=3)
        text_with_shadow(d,(cols*tile+92,96),'QUEST TARGETS', FONT_MED, '#f9f4da')
        yy=132
        lines=[
            '01  Portfolio Gate',
            '02  Pathfinder Board',
            '03  Contribution Zone',
            '',
            'Follow the sprite',
            'to explore the profile.'
        ]
        for line in lines:
            if line:
                text_with_shadow(d,(cols*tile+92,yy),line,FONT_SML,'#dff2ff')
            yy+=26
        # player orientation
        if abs(dx) > 0:
            sprites = PLAYER_R if dx>0 else PLAYER_L
        elif dy>0:
            sprites = PLAYER_D
        else:
            sprites = PLAYER_U
        sprite = sprites[idx % 2]
        sx = int(mx + px*tile + tile//2 - (32*SCALE)//2)
        sy = int(my + py*tile + tile//2 - (32*SCALE)//2 + 8)
        paste_scaled(img, sprite, sx+18, sy+26, 2)
        # prompt text near destination
        if seg >= 5:
            text_with_shadow(d,(cols*tile+92,262),'Current objective:', FONT_SML, '#f8cf55')
            current = 'Pathfinder' if seg < len(path)-1 else 'Contribution'
            text_with_shadow(d,(cols*tile+92,288),current, FONT_MED, '#ffb0c8')
        frames.append(img.convert('P', palette=Image.Palette.ADAPTIVE))
    frames[0].save(OUT/'pathfinder.gif', save_all=True, append_images=frames[1:], duration=180, loop=0, disposal=2)


def build_contrib_gif():
    cols, rows = 16, 7
    cell=42
    w,h=1200,360
    frames=[]
    positions=[]
    # sprite moves along top then snakes down rows
    for r in range(rows):
        range_cols = range(cols) if r % 2 == 0 else range(cols-1,-1,-1)
        for c in range_cols:
            positions.append((c,r))
    positions = positions[::2]  # reduce frames
    for idx,(pc,pr) in enumerate(positions):
        img=Image.new('RGBA',(w,h),(0,0,0,0))
        rounded_panel(img,(16,16,w-16,h-16),'#1b2744ee','#f9f4da',radius=18,width=4)
        d=ImageDraw.Draw(img)
        text_with_shadow(d,(30,28),'CONTRIBUTION FIELD // SPRITE RUN', FONT_BIG, '#f8cf55')
        # grid area
        gx, gy = 42, 86
        for r in range(rows):
            for c in range(cols):
                color = ['#2b364f','#315c3d','#418c47','#53b95c'][(c+r)%4]
                d.rounded_rectangle((gx+c*cell, gy+r*cell, gx+c*cell+32, gy+r*cell+32), radius=6, fill=color, outline='#0d1725')
        # decorative icons and labels
        text_with_shadow(d,(780,98),'REAL CONTRIBUTION SNAKE BELOW', FONT_MED, '#f9f4da')
        text_with_shadow(d,(780,136),'This mini-scene is a pixel', FONT_SML, '#dff2ff')
        text_with_shadow(d,(780,160),'intro where the sprite', FONT_SML, '#dff2ff')
        text_with_shadow(d,(780,184),'runs across the contribution', FONT_SML, '#dff2ff')
        text_with_shadow(d,(780,208),'field before the actual', FONT_SML, '#dff2ff')
        text_with_shadow(d,(780,232),'GitHub snake animation.', FONT_SML, '#dff2ff')
        paste_scaled(img,COIN,790,258,3)
        paste_scaled(img,STAR,860,258,3)
        paste_scaled(img,HEART,930,258,3)
        # player
        next_c,next_r = positions[min(idx+1,len(positions)-1)]
        dx = next_c-pc
        if dx>0: sprites=PLAYER_R
        elif dx<0: sprites=PLAYER_L
        else: sprites=PLAYER_D if next_r>pr else PLAYER_U
        sprite=sprites[idx%2]
        x = gx + pc*cell - 8
        y = gy + pr*cell - 10
        paste_scaled(img, sprite, x, y, 2)
        # title tags
        d.rounded_rectangle((774,36,1148,74), radius=14, fill='#243558', outline='#f8cf55', width=2)
        text_with_shadow(d,(961,46),'LVL UP THROUGH COMMITS', FONT_MED, '#ffb0c8', anchor='ma')
        frames.append(img.convert('P', palette=Image.Palette.ADAPTIVE))
    frames[0].save(OUT/'contribution-run.gif', save_all=True, append_images=frames[1:], duration=120, loop=0, disposal=2)


def build_footer():
    w,h=1200,96
    img=Image.new('RGBA',(w,h),(0,0,0,0))
    rounded_panel(img,(8,8,w-8,h-8),'#202d4cee','#f8cf55',radius=16,width=3)
    d=ImageDraw.Draw(img)
    text_with_shadow(d,(w//2,32),'SAVE PROGRESS • KEEP BUILDING • SEE YOU IN THE NEXT QUEST', FONT_MED, '#f9f4da', anchor='ma')
    img.save(OUT/'footer.png')


if __name__ == '__main__':
    build_hero()
    build_save_file()
    pixel_button('OPEN PORTFOLIO', '#2a4468dd', '#9dd6ff', 'button-portfolio.png')
    pixel_button('OPEN GITHUB', '#59324ddd', '#ffb0c8', 'button-github.png')
    build_pathfinder_gif()
    build_contrib_gif()
    build_footer()
    print('built pathfinder assets')
