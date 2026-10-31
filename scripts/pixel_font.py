"""Shared 5x7 pixel font glyphs from the code-built profile card. No font installation required."""
from pathlib import Path
import re
from PIL import ImageDraw
SOURCE=Path(__file__).resolve().parent/'card-renderer.js'
raw=SOURCE.read_text(encoding='utf-8')
FONT={}
for key,block in re.findall(r"'([^']+)':\[([^\]]+)\]",raw):
    pattern=re.findall(r"'([01]{5})'",block)
    if len(pattern)==7: FONT[key]=pattern
FONT.setdefault(' ',['00000']*7)
def pixel_text(img,text,x,y,scale=2,color='#d0e9d0'):
    d=ImageDraw.Draw(img)
    scale=max(1,round(scale))
    for c in str(text).upper():
        grid=FONT.get(c,FONT.get('?',FONT[' ']))
        for yy,row in enumerate(grid):
            for xx,v in enumerate(row):
                if v=='1':d.rectangle((x+xx*scale,y+yy*scale,x+(xx+1)*scale-1,y+(yy+1)*scale-1),fill=color)
        x+=6*scale
