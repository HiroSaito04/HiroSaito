"""Generate original pixel-art GitHub README assets with a self-contained 5x7 pixel font.

No external fonts, APIs, sprite packs, or copyrighted game imagery required.
Run: python scripts/build_pixel_assets.py
"""
from __future__ import annotations

import html
import json
import math
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'assets'
OUT.mkdir(parents=True, exist_ok=True)
D = json.loads((ROOT / 'profile.json').read_text('utf-8'))

C = {
    'night':'#121631', 'night2':'#1d2446', 'panel':'#202948',
    'deep':'#0b1025', 'outline':'#070d25', 'light':'#f9f0d1',
    'cream':'#fff4d9', 'muted':'#bcc6df', 'purple':'#786cc0',
    'purple2':'#514c91', 'blue':'#80b7eb', 'cyan':'#8de6d9',
    'mint':'#81d9a5', 'grass':'#47745b', 'grass2':'#6ca77a',
    'pink':'#ee94ac', 'berry':'#b65785', 'gold':'#ffd573',
    'darkgold':'#b8864d', 'brown':'#895f4e', 'skin':'#e8b18a',
    'hair':'#29304c', 'white':'#ffffff',
}

# Built-in bitmap alphabet: every headline is real pixel art, not a system-font approximation.
FONT = {
'A':["01110","10001","10001","11111","10001","10001","10001"],
'B':["11110","10001","10001","11110","10001","10001","11110"],
'C':["01111","10000","10000","10000","10000","10000","01111"],
'D':["11110","10001","10001","10001","10001","10001","11110"],
'E':["11111","10000","10000","11110","10000","10000","11111"],
'F':["11111","10000","10000","11110","10000","10000","10000"],
'G':["01111","10000","10000","10111","10001","10001","01111"],
'H':["10001","10001","10001","11111","10001","10001","10001"],
'I':["11111","00100","00100","00100","00100","00100","11111"],
'J':["00111","00010","00010","00010","10010","10010","01100"],
'K':["10001","10010","10100","11000","10100","10010","10001"],
'L':["10000","10000","10000","10000","10000","10000","11111"],
'M':["10001","11011","10101","10101","10001","10001","10001"],
'N':["10001","11001","10101","10011","10001","10001","10001"],
'O':["01110","10001","10001","10001","10001","10001","01110"],
'P':["11110","10001","10001","11110","10000","10000","10000"],
'Q':["01110","10001","10001","10001","10101","10010","01101"],
'R':["11110","10001","10001","11110","10100","10010","10001"],
'S':["01111","10000","10000","01110","00001","00001","11110"],
'T':["11111","00100","00100","00100","00100","00100","00100"],
'U':["10001","10001","10001","10001","10001","10001","01110"],
'V':["10001","10001","10001","10001","10001","01010","00100"],
'W':["10001","10001","10001","10101","10101","10101","01010"],
'X':["10001","10001","01010","00100","01010","10001","10001"],
'Y':["10001","10001","01010","00100","00100","00100","00100"],
'Z':["11111","00001","00010","00100","01000","10000","11111"],
'0':["01110","10011","10101","10101","11001","10001","01110"],
'1':["00100","01100","00100","00100","00100","00100","01110"],
'2':["01110","10001","00001","00010","00100","01000","11111"],
'3':["11110","00001","00001","01110","00001","00001","11110"],
'4':["00010","00110","01010","10010","11111","00010","00010"],
'5':["11111","10000","10000","11110","00001","00001","11110"],
'6':["01111","10000","10000","11110","10001","10001","01110"],
'7':["11111","00001","00010","00100","01000","01000","01000"],
'8':["01110","10001","10001","01110","10001","10001","01110"],
'9':["01110","10001","10001","01111","00001","00001","11110"],
'.':["00000","00000","00000","00000","00000","01100","01100"],
':':["00000","01100","01100","00000","01100","01100","00000"],
'-':["00000","00000","00000","11111","00000","00000","00000"],
'/':["00001","00001","00010","00100","01000","10000","10000"],
'>':["10000","01000","00100","00010","00100","01000","10000"],
'<':["00001","00010","00100","01000","00100","00010","00001"],
'!':["00100","00100","00100","00100","00100","00000","00100"],
'?':["01110","10001","00001","00010","00100","00000","00100"],
'+':["00000","00100","00100","11111","00100","00100","00000"],
'@':["01110","10001","10111","10101","10111","10000","01110"],
'&':["01100","10010","10100","01000","10101","10010","01101"],
'_':["00000","00000","00000","00000","00000","00000","11111"],
' ':["00000"]*7,
}

def R(x,y,w,h,fill,opacity=None):
    o='' if opacity is None else f' opacity="{opacity}"'
    return f'<rect x="{int(x)}" y="{int(y)}" width="{int(w)}" height="{int(h)}" fill="{fill}"{o}/>'

def pixel_text(msg, x, y, scale=4, color=None, max_width=None, tracking=1):
    msg=msg.upper()
    # max_width, if provided, scales down with integer pixel scale
    if max_width:
        scale=min(scale, max(1, int(max_width//((len(msg)*(5+tracking)-tracking)))))
    out=[]
    color=color or C['cream']
    for ci,ch in enumerate(msg):
        for row,line in enumerate(FONT.get(ch,FONT['?'])):
            for col,p in enumerate(line):
                if p=='1': out.append(R(x+(ci*(5+tracking)+col)*scale,y+row*scale,scale,scale,color))
    return ''.join(out)

def tx(msg,x,y,size=20,fill=None,weight='normal',anchor=None,ls=None):
    a=f' text-anchor="{anchor}"' if anchor else ''
    l=f' letter-spacing="{ls}"' if ls else ''
    return f'<text x="{x}" y="{y}" font-family="Verdana,Arial,sans-serif" font-size="{size}" font-weight="{weight}" fill="{fill or C["cream"]}"{a}{l}>{html.escape(msg)}</text>'

def svg(body,w,h):
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" shape-rendering="crispEdges" role="img">
    <title>Original pixel-game developer profile art</title>
    {body}
    </svg>'''

def frame(x,y,w,h,fill=None,accent=None,shadow=10):
    fill=fill or C['panel'];accent=accent or C['gold']
    return ''.join([
      R(x+shadow,y+shadow,w,h,C['outline']),
      R(x,y,w,h,accent),R(x+5,y+5,w-10,h-10,C['outline']),
      R(x+10,y+10,w-20,h-20,fill),
      R(x+18,y+18,w-36,4,C['purple2']),
      R(x+18,y+h-24,w-36,4,C['purple2']),
      R(x+18,y+18,5,5,accent),R(x+w-23,y+18,5,5,accent),
      R(x+18,y+h-23,5,5,accent),R(x+w-23,y+h-23,5,5,accent),
    ])

# Original, intentionally abstract, 16 x 22 RPG-style developer character sprite.
# Each ASCII position is one chunky pixel. No claim of depicting the real person's likeness.
SPRITE = [
"................",
".....kkkkkk.....",
"....kkkkkkkk....",
"...kkkknkkkkk...",
"...kkssSSsskk...",
"...kSSSSSSSSk...",
"...kSxSSSSxSk...",
"...kSSSssSSSk...",
"....kssssssk....",
".....ksssskk....",
"...bbpbbbbpbb...",
"..bbbbbbbbbbbb..",
"..bsbbbbbbbbsb..",
"..bsbppbbppbsb..",
"..bsbbbbbbbbsb..",
"...bbbbbbbbbb...",
"...bbbbbbbbbb...",
"....vvbbbbvv....",
"....vv....vv....",
"....vv....vv....",
"...dddd..dddd...",
"..ddddd..ddddd..",
]
SPR_COLORS={
 'k':C['hair'], 'n':'#465577','s':C['skin'],'S':'#ffd6a3',
 'x':C['night'],'b':C['blue'],'p':C['pink'],
 'v':'#5b608a','d':'#302a4e',
}

def sprite(x,y,p=8):
    out=[]
    # transparent space
    for j,row in enumerate(SPRITE):
        for i,ch in enumerate(row):
            if ch!='.':out.append(R(x+i*p,y+j*p,p,p,SPR_COLORS[ch]))
    return ''.join(out)

def coin(x,y,p=6):
    pattern=["..yyy..",".yyyyy.","yyyyyyy","yykyyyy","yykyyyy",".yyyyy.","..yyy.."]
    return ''.join(R(x+i*p,y+j*p,p,p,C['gold'] if ch=='y' else C['darkgold']) for j,row in enumerate(pattern) for i,ch in enumerate(row) if ch!='.')

def heart(x,y,p=6):
    pattern=[".rr.rr.","rrrrrrr","rrrrrrr",".rrrrr.","..rrr..","...r..."]
    return ''.join(R(x+i*p,y+j*p,p,p,C['pink']) for j,row in enumerate(pattern) for i,ch in enumerate(row) if ch!='.')

def star(x,y,p=4,color=None):
    return ''.join([R(x+p,y,p,p,color or C['gold']),R(x,y+p,3*p,p,color or C['gold']),R(x+p,y+2*p,p,p,color or C['gold'])])

def tree(x,base,s=8):
    rows=["....g....","...ggg...","..ggggg..",".ggggggg.","ggggggggg","...ggg...","..ggggg..",".ggggggg.","ggggggggg","....t....","....t...."]
    o=[]
    for y,row in enumerate(rows):
        for xi,ch in enumerate(row):
            if ch=='g':o.append(R(x+xi*s,base+y*s,s,s,C['grass2'] if (xi+y)%4 else C['grass']))
            if ch=='t':o.append(R(x+xi*s,base+y*s,s,s,C['brown']))
    return ''.join(o)

def clouds(x,y,s=10):
    rows=["...wwwww....","..wwwwwwwww.",".wwwwwwwwwww","wwwwwwwwwwww"]
    return ''.join(R(x+i*s,y+j*s,s,s,'#c0b8e1' if j==0 else '#8f8bc0') for j,row in enumerate(rows) for i,ch in enumerate(row) if ch=='w')

def mosaic_bg(w,h,base=None):
    rng=random.Random(17)
    o=[R(0,0,w,h,base or C['night'])]
    for j in range(0,h,32):
      for i in range(0,w,32):
        if rng.random()<.11:o.append(R(i,j,32,32,C['night2'],.6))
    for _ in range(int(w*h//18000)):
      x=rng.randrange(8,w-8,8);y=rng.randrange(8,h-8,8)
      o.append(R(x,y,4,4,C['cream'],.6 if rng.random()<.55 else .25))
    return ''.join(o)

# Hero: side-scroller world / game HUD
W,H=1200,560
B=[mosaic_bg(W,H)]
B += [R(0,0,W,16,C['outline']),R(0,H-16,W,16,C['outline']),R(0,0,16,H,C['outline']),R(W-16,0,16,H,C['outline'])]
B += [R(18,18,W-36,8,C['purple']),R(18,H-26,W-36,8,C['purple'])]
B += [R(18,27,6,H-54,C['purple']),R(W-24,27,6,H-54,C['purple'])]
B += [clouds(760,82,9),clouds(1010,42,7),star(970,190,7),star(1100,130,5),star(810,50,4)]
# Distant pixel mountains
for x in range(0,W,28):
    height=140+int(55*abs(math.sin(x*.010)) + 45*abs(math.cos(x*.016)))
    B.append(R(x,H-90-height,28,height,C['purple2']))
for x in range(0,W,28):
    height=90+int(35*abs(math.sin(x*.015)) + 24*abs(math.cos(x*.023)))
    B.append(R(x,H-90-height,28,height,C['grass']))
B += [R(24,H-105,W-48,20,C['grass2']),R(24,H-85,W-48,65,C['brown'])]
for x in range(30,W-30,24):B.append(R(x,H-84,14,8,C['darkgold']))
B += [tree(790,330,9),tree(1080,337,8),tree(995,354,6)]
B += [frame(43,52,730,420,fill=C['deep'],accent=C['gold'],shadow=10)]
B += [pixel_text('PLAYER ONE',80,87,3,C['mint'])]
B += [R(80,122,650,7,C['purple2'])]
B += [pixel_text('MIKE ANGELO',80,158,6,C['cream'])]
B += [pixel_text('A. RUBIA',80,218,6,C['gold'])]
B += [R(80,285,570,58,C['night2']),R(80,285,8,58,C['cyan'])]
B += [pixel_text('FULL STACK DEVELOPER',100,302,4,C['cyan'])]
B += [pixel_text('GITHUB / HIROSAITO04',80,366,3,C['muted'])]
B += [pixel_text('PRESS START > PORTFOLIO',80,416,3,C['mint'])]
# Character shadow and plinth
B += [R(870,486,222,10,C['outline']),R(891,474,176,12,C['darkgold']),R(910,462,138,12,C['gold'])]
B += [sprite(900,265,10)]
B += [R(865,215,254,48,C['outline']),R(871,221,242,36,C['cream'])]
B += [pixel_text('DEV HERO',894,228,3,C['night'])]
B += [coin(1050,177,6),heart(820,195,5)]
(OUT/'hero.svg').write_text(svg(''.join(B),W,H),'utf-8')

# Character standalone for source code reuse
W,H=240,280
B=[R(0,0,W,H,C['night']),frame(12,12,W-24,H-24,C['night2'],C['purple']),sprite(59,29,8)]
B += [pixel_text('PLAYER',48,220,4,C['cream']),pixel_text('01',97,247,3,C['cyan'])]
(OUT/'character.svg').write_text(svg(''.join(B),W,H),'utf-8')

# Status UI built from sourced data
W,H=1200,355
B=[mosaic_bg(W,H),frame(20,20,1160,315,C['deep'],C['mint'])]
B += [pixel_text('SAVE FILE / PROFILE',56,53,4,C['gold'])]
B += [R(58,103,1080,5,C['purple2'])]
B += [pixel_text('NAME',58,130,3,C['cyan']),pixel_text(D['name'],292,128,3,C['cream'])]
B += [pixel_text('CLASS',58,185,3,C['cyan']),pixel_text(D['role'],292,183,3,C['cream'])]
B += [pixel_text('PLAYER ID',58,240,3,C['cyan']),pixel_text('@'+D['username'],292,238,3,C['cream'])]
B += [R(58,292,1080,4,C['purple2'])]
B += [coin(1000,220,6)]
(OUT/'save-file.svg').write_text(svg(''.join(B),W,H),'utf-8')

# Quest Board: no invented project names; destinations are actual links in README
W,H=1200,420
B=[mosaic_bg(W,H),frame(22,20,1156,380,C['deep'],C['gold'])]
B += [pixel_text('QUEST BOARD',55,52,5,C['gold'])]
B += [pixel_text('SELECT YOUR DESTINATION',55,112,3,C['muted'])]
items=[
 ('01','OPEN PORTFOLIO','VISIT THE LIVE SITE',C['mint']),
 ('02','EXPLORE GITHUB','BROWSE PUBLIC WORK',C['blue']),
 ('03','CONTRIBUTION QUEST','FOLLOW THE SNAKE',C['pink']),
]
for i,(num,label,sub,color) in enumerate(items):
    y=160+i*69
    B.extend([R(58,y,1080,58,C['panel']),R(58,y,10,58,color),R(70,y+53,1054,5,C['purple2']),
              pixel_text('>'+num,93,y+13,4,color),pixel_text(label,255,y+13,4,C['cream']),pixel_text(sub,850,y+16,2,C['muted'])])
(OUT/'quest-board.svg').write_text(svg(''.join(B),W,H),'utf-8')

# Tiny retro RPG footer panorama
W,H=1200,215
B=[mosaic_bg(W,H),R(0,157,1200,12,C['grass2']),R(0,169,1200,46,C['brown'])]
for x in [38,170,318,930,1065]:B.append(tree(x,53,10))
B += [star(86,30,5),star(766,29,4),star(1100,27,5)]
B += [frame(300,28,600,112,C['deep'],C['pink']),pixel_text('THANKS FOR VISITING',330,55,4,C['cream']),pixel_text('SAVE PROGRESS / KEEP BUILDING',330,97,2,C['mint'])]
(OUT/'footer.svg').write_text(svg(''.join(B),W,H),'utf-8')

# Bare dividers / sprites for reuse
W,H=1200,96
B=[R(0,0,W,H,C['night'])]
for x in range(0,W,48):
 B.extend([R(x,40,24,14,C['purple2']),R(x+24,47,24,7,C['purple'])])
B += [star(530,20,6),heart(585,20,6),star(650,20,6)]
(OUT/'divider.svg').write_text(svg(''.join(B),W,H),'utf-8')

# Link button sprites for the GitHub README. Click behavior comes from the HTML anchors.
for filename, label, color in [
    ('button-portfolio.svg','VISIT PORTFOLIO', C['mint']),
    ('button-github.svg','OPEN GITHUB',C['blue']),
]:
    W,H=530,96
    B=[R(8,12,512,78,C['outline']),R(0,0,512,78,color),
       R(6,6,500,66,C['deep']),R(14,14,484,50,C['panel']),
       R(18,18,7,42,color),pixel_text('>',39,26,4,color),pixel_text(label,85,24,4,C['cream'])]
    (OUT/filename).write_text(svg(''.join(B),W,H),'utf-8')

print('Built:',', '.join(p.name for p in sorted(OUT.glob('*.svg'))))
