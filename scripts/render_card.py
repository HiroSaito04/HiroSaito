"""Generate the Pixel Pathfinder GitHub profile card from the user's actual boy_down.png.

Typography is rasterized at small sizes, binarized, then enlarged with NEAREST
sampling. This results in visibly pixelated letterforms without shipping any font.
Run: python scripts/render_card.py
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'assets'/'profile-card.png'
W,H=1440,600
C={
    'dark':(10,17,17), 'base':(14,23,21), 'ink':(8,14,13),
    'line':(134,214,92), 'lime':(146,224,87), 'light':(246,247,234),
    'muted':(175,190,178),'forest':(38,75,38), 'forest2':(54,104,45),
}

def rgba(c,a=255): return (*c,a)

def pixel_font(text, size=13, scale=2, color=(245,248,236), tracking=1):
    """Render monochrome pixel font as a transparent image."""
    # These local fonts are rendering inputs only, never distributed.
    font_candidates=[
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf',
        '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf',
    ]
    font=None
    for p in font_candidates:
        if Path(p).exists(): font=ImageFont.truetype(p,size); break
    font=font or ImageFont.load_default()
    # Small bitmap glyphs converted to integer-nearest pixel blocks.
    bits=[]
    for ch in text:
        bbox=font.getbbox(ch)
        advance=max(3, int(math.ceil(font.getlength(ch))))
        tile=Image.new('L',(advance+6,size+8),0)
        d=ImageDraw.Draw(tile)
        d.text((3-bbox[0],3-bbox[1]),ch,font=font,fill=255)
        # Avoid anti-aliased edge pixels: binary black/white pixels only.
        tile=tile.point(lambda v:255 if v>=104 else 0)
        bits.append(tile.crop((0,0,advance+tracking+2,tile.height)))
    bw=sum(b.width for b in bits)+4
    bh=size+9
    mask=Image.new('L',(bw,bh),0)
    xx=0
    for bit in bits:
        mask.paste(bit,(xx,0))
        xx+=bit.width
    mask=mask.crop((0,0,max(xx,1),mask.height))
    scaled=mask.resize((mask.width*scale,mask.height*scale),Image.Resampling.NEAREST)
    out=Image.new('RGBA',scaled.size,(0,0,0,0))
    out.paste((*color,255),(0,0,scaled.width,scaled.height),scaled)
    return out

def word(base,text,x,y,size=13,scale=2,color=None,tracking=1,max_w=None):
    color=color or C['light']
    stamp=pixel_font(text,size,scale,color,tracking)
    if max_w and stamp.width>max_w:
        # preserve nearest-neighbor pixels even if text needs to fit
        factor=max_w/stamp.width
        stamp=stamp.resize((max_w,max(1,round(stamp.height*factor))),Image.Resampling.NEAREST)
    base.alpha_composite(stamp,(int(x),int(y)))
    return stamp.size

def box_steps(draw,rect,rad,color,width=5):
    x1,y1,x2,y2=rect
    # blocky chamfer outlines, non-antialiased, retro pixel shape
    pts=[(x1+rad,y1),(x2-rad,y1),(x2-rad,y1+4),(x2-8,y1+4),
         (x2-8,y1+rad),(x2,y1+rad),(x2,y2-rad),
         (x2-8,y2-rad),(x2-8,y2-4),(x2-rad,y2-4),(x2-rad,y2),
         (x1+rad,y2),(x1+rad,y2-4),(x1+8,y2-4),(x1+8,y2-rad),
         (x1,y2-rad),(x1,y1+rad),(x1+8,y1+rad),(x1+8,y1+4),(x1+rad,y1+4)]
    draw.line(pts+[pts[0]],fill=color,width=width,joint='curve')
    return pts

def fill_step(draw,rect,rad,color):
    x1,y1,x2,y2=rect
    draw.polygon([(x1+rad,y1),(x2-rad,y1),(x2-8,y1+8),(x2,y1+rad),
       (x2,y2-rad),(x2-8,y2-8),(x2-rad,y2),
       (x1+rad,y2),(x1+8,y2-8),(x1,y2-rad),(x1,y1+rad),(x1+8,y1+8)],fill=color)

def draw_tree(draw,x,y,h,base_color):
    # pixel pine silhouettes with block foliage strips and trunk
    w=h*.75; h=int(h); w=int(w)
    draw.rectangle((x-5,y-h//4,x+4,y),fill=base_color)
    for i,frac in enumerate([0.18,0.32,0.45,0.57,0.72,0.87]):
        yy=int(y-h+(i+1)*h/7)
        half=int(w*frac*.5)
        draw.rectangle((x-half,yy,x+half,yy+int(h/7)+3),fill=base_color)

def make():
    im=Image.new('RGBA',(W,H),rgba(C['ink']))
    d=ImageDraw.Draw(im)
    # subtle charcoal-green gradient
    for y in range(H):
        for_chunk=1-y/H
        r=int(10+4*(1-for_chunk))
        g=int(18+9*(1-for_chunk))
        b=int(16+5*(1-for_chunk))
        d.line((0,y,W,y),fill=(r,g,b,255))
    # subtle tile pixels/particles
    for gx in range(0,W,24):
        for gy in range(0,H,24):
            if ((gx*13+gy*19)//24)%53==0:
                d.rectangle((gx,gy,gx+2,gy+2),fill=(41,72,44,155))

    # Main frame, soft halo separate from crisp outer edge
    overlay=Image.new('RGBA',(W,H),(0,0,0,0)); g=ImageDraw.Draw(overlay)
    box_steps(g,(48,46,1391,549),30,(119,213,80,180),8)
    blur=overlay.filter(ImageFilter.GaussianBlur(14))
    blur.putalpha(blur.getchannel('A').point(lambda a:int(a*.22)))
    im.alpha_composite(blur)
    d=ImageDraw.Draw(im)
    fill_step(d,(48,46,1391,549),32,(16,27,23,246))
    box_steps(d,(48,46,1391,549),30,rgba(C['line']),5)
    box_steps(d,(58,56,1381,539),28,(39,76,37,255),2)

    # right-side forest pixels, gradual parallax behind content
    for x,h,color in [(1010,38,(27,52,31,255)),(1085,53,(31,65,34,255)),(1166,80,(38,74,37,255)),
        (1250,105,(41,81,39,255)),(1330,72,(31,62,33,255))]:
        draw_tree(d,x,527,h,color)
    for xx in range(930,1375,12):
        yy=528 - int(13*math.sin(xx*.035)+8*math.cos(xx*.07))
        d.rectangle((xx,min(yy,535),xx+10,max(yy,535)), fill=(44,87,40,255))
    # pixel floating crosses and corners
    for x,y,s in [(1220,122,8),(1293,421,7),(1147,470,5),(1268,255,5),(1150,104,5)]:
        col=(101,194,72,205)
        d.rectangle((x-s//2,y-3*s//2,x+s//2,y+3*s//2),fill=col)
        d.rectangle((x-3*s//2,y-s//2,x+3*s//2,y+s//2),fill=col)
    for (x,y,s) in [(1327,83,18),(1345,101,18),(1363,119,18)]:
        d.rectangle((x,y,x+s-2,y+s-2),fill=(37,70,39,255))

    # portrait panel -- stepped silhouette, no pseudo-vector filtering on sprite
    fill_step(d,(111,114,471,491),46,(32,62,32,255))
    box_steps(d,(111,114,471,491),46,(110,198,68,255),6)
    fill_step(d,(124,127,459,479),38,(40,76,36,255))
    # panels are shaded by geometric strips, not blur
    for i in range(8):
        y=135+i*40
        d.rectangle((140,y,443,y+11),fill=(44+i*2,84+i*2,42+i,45))
    sprite=Image.open(ROOT/'assets'/'boy_down.png').convert('RGBA')
    a=sprite.getchannel('A')
    # crop away black transparent borders only; keep exact pixel sprite
    bbox=a.getbbox()
    if bbox:sprite=sprite.crop(bbox)
    # crisp nearest-neighbor 3.25x approx; fits green portrait container
    target_height=315
    sc=target_height/max(sprite.height,1)
    target=(max(1,round(sprite.width*sc)),target_height)
    sprite=sprite.resize(target,Image.Resampling.NEAREST)
    im.alpha_composite(sprite,(int(292-target[0]/2),int(307-target[1]/2)))

    # identity right -- all text drawn using pixelated glyph masks
    fill_step(d,(525,116,815,176),17,(13,22,19,255))
    box_steps(d,(525,116,815,176),17,(71,125,51,255),4)
    word(im, '>_ HIROSAITO04',546,130,13,2,C['light'],0,max_w=262)
    word(im,'MIKE RUBIA',525,206,21,3,C['light'],0,max_w=782)
    word(im,'SOFTWARE DEVELOPER  •  MOBILE AND WEB',528,284,14,2,C['lime'],0,max_w=800)

    # progress-style accent
    d.rectangle((529,337,1280,344),fill=(35,68,36,255))
    d.rectangle((529,337,650,344),fill=rgba(C['lime']))
    d.rectangle((529,347,650,351),fill=(33,67,32,255))
    word(im, 'Building thoughtful digital experiences.',528,372,12,2,C['muted'],0,max_w=746)

    # GitHub pill
    fill_step(d,(525,432,1020,490),20,(12,22,18,255))
    box_steps(d,(525,432,1020,490),20,(81,142,59,255),4)
    # terminal prompt pixel glyph left
    word(im,'>_',545,448,13,2,C['lime'],0)
    word(im,'HIRO SAITO',603,446,12,2,C['light'],0,max_w=386)

    im.convert('RGB').save(OUT,optimize=True)
    print('Generated:',OUT)

if __name__ == '__main__': make()
