"""GitHub-style contribution graph with Brio animation and REAL public GitHub day levels.

Local design preview: python scripts/render_contributions.py --preview
Fetch YOUR real calendar: python scripts/render_contributions.py --fetch
Use saved real data: python scripts/render_contributions.py

Default: 185 frames at 200ms per frame (~37 seconds per cycle),
vs previous 59 frames at 110ms (~6.5 seconds).
Adjust --frame-ms and --frames to taste.

A preview is explicitly marked SAMPLE; only --fetch can populate actual counts.
"""
from __future__ import annotations
import argparse, calendar, datetime as dt, json, random, re, urllib.request
from html.parser import HTMLParser
from pathlib import Path
from PIL import Image,ImageDraw
from pixel_font import pixel_text
ROOT=Path(__file__).resolve().parents[1]
DATA=ROOT/'data/contributions.json'
OUT=ROOT/'assets/contribution-brio.gif'
USERNAME='HiroSaito04'

class ContributionsHTML(HTMLParser):
    def __init__(self):super().__init__();self.days=[]
    def handle_starttag(self, tag, attrs):
        if tag not in ('td','rect'):return
        a=dict(attrs)
        if 'data-date' in a and 'data-level' in a:
            try:self.days.append({'date':a['data-date'],'level':min(4,max(0,int(a['data-level'])))})
            except ValueError:pass

def fetch():
    req=urllib.request.Request('https://github.com/users/'+USERNAME+'/contributions',headers={'User-Agent':'Mozilla/5.0 (compatible; pixel-profile-builder/1.0)','Accept':'text/html'})
    errors=[]; days=[]
    try:
        with urllib.request.urlopen(req, timeout=28) as response:html=response.read().decode('utf-8')
        parser=ContributionsHTML();parser.feed(html);days=parser.days
    except Exception as exc:errors.append(str(exc))
    if len(days)<330:
        try:
            api=f'https://github-contributions-api.jogruber.de/v4/{USERNAME}?y=last'
            with urllib.request.urlopen(urllib.request.Request(api,headers={'User-Agent':'pixel-profile-builder/1.0'}), timeout=28) as response:
                data=json.load(response)
            days=[{'date':d['date'],'level':int(d['level'])} for d in data['contributions']]
        except Exception as exc:errors.append(str(exc))
    # Strictly refuse to overwrite cache if the endpoint fails.
    days={d['date']:d for d in days if 0<=d['level']<=4}
    today=dt.date.today()
    within=[v for k,v in days.items() if (today-dt.timedelta(days=366)).isoformat()<=k<=today.isoformat()]
    if len(within)<320:raise RuntimeError('Could not fetch complete contributions calendar. Existing saved data unchanged. '+ ' '.join(errors))
    DATA.parent.mkdir(parents=True,exist_ok=True)
    DATA.write_text(json.dumps({'username':USERNAME,'source':'GitHub public contributions','updated':today.isoformat(),'days':sorted(within,key=lambda x:x['date'])},indent=2),encoding='utf8')
    print('Fetched real public GitHub contribution levels:',len(within))

def levels_for(mode):
    today=dt.date.today()
    sunday=today-dt.timedelta(days=(today.weekday()+1)%7)
    first=sunday-dt.timedelta(weeks=52)
    last=first+dt.timedelta(days=7*53-1)
    # 53 full weeks ending current week, future cells omitted.
    days=[first+dt.timedelta(days=i) for i in range(371)]
    if mode=='sample':
        rng=random.Random(11)
        # sample ONLY, unmistakably labeled; actual data populated by --fetch.
        m={d.isoformat():rng.choices([0,1,2,3,4],[0.70,0.14,0.09,0.05,0.02])[0] for d in days if d<=today}
        return days,m,'SAMPLE PREVIEW — NOT YOUR GITHUB DATA'
    if not DATA.exists():
        return days,{},'RUN GITHUB ACTION TO LOAD REAL CONTRIBUTIONS'
    cached=json.loads(DATA.read_text(encoding='utf8'))
    if cached.get('source')!='GitHub public contributions':
        raise RuntimeError('Unknown contributions cache source; refusing to label as real')
    level={v['date']:int(v['level']) for v in cached['days']}
    if cached.get('snapshot_total_contributions') is not None:
        label='PUBLIC GITHUB SNAPSHOT / '+cached.get('updated','')
    else:
        label='LIVE GITHUB DATA / '+cached.get('updated','')
    return days,level,label

def draw(mode, frame_ms=200, frame_count=185):
    days,levels,label=levels_for(mode)
    # GitHub calendar composition: no fake side panels, no second grid.
    W,H=1198,300
    margin=20
    gap=17;cell=13
    gx=126;gy=82
    month_months=[]
    for week in range(53):
        d=days[week*7]
        if week==0 or d.month!=days[(week-1)*7].month:
            month_months.append((week, d.strftime('%b').upper()))
    # correct 0-4 GitHub dark palette
    colors=['#161b22','#0e4429','#006d32','#26a641','#39d353']
    base=Image.new('RGBA',(W,H),'#0d1117')
    dr=ImageDraw.Draw(base)
    dr.rounded_rectangle((1,1,W-2,H-2), radius=12, fill='#0d1117',outline='#30363d',width=2)
    pixel_text(base,'CONTRIBUTION ACTIVITY',26,23,3,'#e6edf3')
    pixel_text(base,label,540,28,1.5,'#8b949e')
    for week,month in month_months:
        if week==0:continue
        x=gx+week*gap
        if x<1100:pixel_text(base,month,x,58,2,'#8b949e')
    for r,label_day in [(1,'MON'),(3,'WED'),(5,'FRI')]:
        pixel_text(base,label_day,39,gy+r*gap+2,2,'#8b949e')
    for week in range(53):
        for row in range(7):
            day=days[week*7+row]
            if day>dt.date.today():continue
            if mode!='sample' and day.isoformat() not in levels:
                continue # No invented data for days not covered by the archived snapshot.
            col=colors[levels.get(day.isoformat(),0)]
            x=gx+week*gap;y=gy+row*gap
            dr.rounded_rectangle((x,y,x+cell,y+cell),radius=2,fill=col)
    pixel_text(base,'LESS',W-294,253,2,'#8b949e')
    for level,color in enumerate(colors):
        x=W-223+level*23
        dr.rounded_rectangle((x,249,x+14,263), radius=2,fill=color)
    pixel_text(base,'MORE',W-87,253,2,'#8b949e')
    pixel_text(base,'VIEW LIVE GRID AT GITHUB.COM/HIROSAITO04',30,259,2,'#7f8b99')
    frames=[]
    # Traverse the same real calendar cells, serpentining naturally through each week.
    route=[]
    for week in range(53):
        rows=range(7) if week%2==0 else range(6,-1,-1)
        for row in rows:
            day=days[week*7+row]
            if day<=dt.date.today():route.append((week,row))
    # More frames + longer durations = slower, less jumpy walk across the calendar.
    # Never false-fill cells; Brio is rendered over the actual GitHub levels.
    selected=[route[round(i*(len(route)-1)/(frame_count-1))] for i in range(frame_count)]
    spritebase=ROOT/'source_assets/sprites'
    spritecache={n:Image.open(spritebase/f'brio{n}.png').convert('RGBA') for n in range(1,13)}
    for i,(week,row) in enumerate(selected):
        frame=base.copy()
        nweek,nrow=selected[min(i+1,len(selected)-1)]
        if nweek>week: direction='right'
        elif nrow>row: direction='down'
        elif nrow<row: direction='up'
        else:direction='left'
        frame_ix={'right':(8,9),'left':(5,6),'up':(11,12),'down':(2,3)}[direction][i%2]
        spr=spritecache[frame_ix]
        # 32px Brio sprite occupies 2 columns; feet stay on the calendar.
        px=gx+week*gap-9;py=gy+row*gap-18
        frame.alpha_composite(spr,(px,py))
        frames.append(frame.convert('P',palette=Image.Palette.ADAPTIVE,colors=64))
    OUT.parent.mkdir(parents=True,exist_ok=True)
    frames[0].save(OUT,save_all=True,append_images=frames[1:],duration=frame_ms,loop=0,optimize=True,disposal=2)
    base.convert('RGB').save(ROOT/'assets/contribution-preview.png')
    print(f'Contribution: {len(frames)} frames x {frame_ms} ms = {len(frames)*frame_ms/1000:.1f} sec/cycle, {OUT.stat().st_size/1e6:.2f} MB, mode={mode}')

if __name__=='__main__':
    p=argparse.ArgumentParser()
    p.add_argument('--fetch',action='store_true',help='Fetch real GitHub data, fail safely on network errors')
    p.add_argument('--preview',action='store_true',help='Use clearly marked sample values for a design review')
    p.add_argument('--frame-ms', type=int, default=200, help='Duration of each sprite frame in ms (default: 200)')
    p.add_argument('--frames', type=int, default=185, help='Number of sprite frames in a full loop (default: 185)')
    args=p.parse_args()
    if args.fetch and args.preview:
        p.error('--fetch and --preview cannot be combined')
    if not (60 <= args.frame_ms <= 1000):
        p.error('--frame-ms must be between 60 and 1000')
    if not (25 <= args.frames <= 400):
        p.error('--frames must be between 25 and 400')
    if args.fetch:fetch()
    draw('sample' if args.preview else 'live', args.frame_ms, args.frames)
