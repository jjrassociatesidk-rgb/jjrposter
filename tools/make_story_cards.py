#!/usr/bin/env python3
"""JJR Associates Instagram STORY generator for multi-point INFORMATIONAL updates (1080x1920).
Use one slide per 3 cards (so 6 points = 2 story slides). Example:
python3 tools/make_story_cards.py --chip "GST COUNCIL UPDATE" --heading "57th GST Council" --part "Key takeaways \u00b7 1 of 2" \
  --note "Council recommendations - effective only after notification." \
  --cards "Headline::detail|Headline::detail|Headline::detail" --first 1 --out posters/slide1.jpg
--first = number shown on the first card (use 4 for the second slide). Max 3 cards per slide; headline ~28 chars; detail ~110 chars."""
import argparse, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ap=argparse.ArgumentParser()
ap.add_argument("--chip",required=True); ap.add_argument("--heading",required=True); ap.add_argument("--part",default="")
ap.add_argument("--note",default=""); ap.add_argument("--cards",required=True); ap.add_argument("--first",type=int,default=1); ap.add_argument("--out",required=True)
a=ap.parse_args()
HERE=os.path.dirname(os.path.abspath(__file__)); LOGO=os.path.join(HERE,"..","assets","ca_logo.png")
S=2; W,H=1080,1920
navy=(14,42,71); orange=(226,104,24); green=(34,139,76); ink=(52,66,86); mute=(96,112,134); bg=(246,248,252); card=(255,255,255); line=(222,229,239)
def pick(*c):
    for p in c:
        if os.path.exists(p): return p
    raise SystemExit("font missing: "+c[0])
IF="/usr/share/fonts/opentype/inter/"; DJ="/usr/share/fonts/truetype/dejavu/"; FR="/usr/share/fonts/truetype/freefont/"
XB=pick(IF+"InterDisplay-ExtraBold.otf",DJ+"DejaVuSans-Bold.ttf"); BD=pick(IF+"Inter-Bold.otf",DJ+"DejaVuSans-Bold.ttf")
SB=pick(IF+"Inter-SemiBold.otf",DJ+"DejaVuSans-Bold.ttf"); MD=pick(IF+"Inter-Medium.otf",DJ+"DejaVuSans.ttf")
SER=pick(FR+"FreeSerifBold.ttf",DJ+"DejaVuSerif-Bold.ttf"); SERR=pick(FR+"FreeSerif.ttf",DJ+"DejaVuSerif.ttf")
img=Image.new("RGBA",(W*S,H*S),bg+(255,)); d=ImageDraw.Draw(img)
P=lambda v:int(round(v*S))
F=lambda p,s: ImageFont.truetype(p,P(s))
def rr(b,r,fill=None,outline=None,width=1,corners=None):
    d.rounded_rectangle([P(b[0]),P(b[1]),P(b[2]),P(b[3])],radius=P(r),fill=fill,outline=outline,width=P(width) if outline else 0,corners=corners)
def rect(b,fill): d.rectangle([P(b[0]),P(b[1]),P(b[2]),P(b[3])],fill=fill)
def ell(b,fill=None,outline=None,width=1): d.ellipse([P(b[0]),P(b[1]),P(b[2]),P(b[3])],fill=fill,outline=outline,width=P(width) if outline else 0)
def tw(t,font,sp=0): return (d.textlength(t,font=font)+P(sp)*(len(t)-1))/S
def text(x,y,t,font,fill,sp=0,anchor="l",maxw=None):
    w=tw(t,font,sp)
    if anchor=="c": x=x-w/2
    elif anchor=="r": x=x-w
    if maxw: assert x+w<=maxw+0.5,("too wide",t,x+w)
    if sp==0: d.text((P(x),P(y)),t,font=font,fill=fill)
    else:
        cx=P(x)
        for ch in t: d.text((cx,P(y)),ch,font=font,fill=fill); cx+=d.textlength(ch,font=font)+P(sp)
    return w
def shadow(b,r,blur=18,off=10,alpha=60,color=(14,42,71)):
    global img,d
    L=Image.new("RGBA",img.size,(0,0,0,0)); ld=ImageDraw.Draw(L)
    ld.rounded_rectangle([P(b[0]),P(b[1]+off),P(b[2]),P(b[3]+off)],radius=P(r),fill=color+(alpha,))
    img=Image.alpha_composite(img,L.filter(ImageFilter.GaussianBlur(P(blur)))); d=ImageDraw.Draw(img)
def fit(t,path,start,maxw):
    s=start
    while s>20 and tw(t,F(path,s))>maxw: s-=2
    return F(path,s)
# background
L=Image.new("RGBA",img.size,(0,0,0,0)); ld=ImageDraw.Draw(L)
ld.ellipse([P(600),P(-300),P(1320),P(420)],fill=(222,233,247,255)); ld.ellipse([P(-380),P(1000),P(260),P(1640)],fill=(252,236,222,255))
img=Image.alpha_composite(img,L); d=ImageDraw.Draw(img)
rect((0,0,W,12),navy); rect((0,0,360,12),orange); rect((360,0,720,12),(255,255,255)); rect((720,0,W,12),green)
def wrap(t,font,maxw):
    words=t.split(); lines=[]; cur=""
    for w in words:
        trial=(cur+" "+w).strip()
        if tw(trial,font)<=maxw: cur=trial
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
# layout: up to 3 cards = roomy; 4-6 cards = compact single-story layout
items=[tuple(c.split("::",1)) for c in a.cards.split("|") if "::" in c][:6]
n=len(items); compact=n>3
cf=F(BD,24 if compact else 26); cw=tw(a.chip,cf,3)+(60 if compact else 70)
cy0,cy1=(236,282) if compact else (250,304)
rr((W/2-cw/2,cy0,W/2+cw/2,cy1),(cy1-cy0)/2,fill=orange); text(W/2,cy0+(10 if compact else 12),a.chip,cf,(255,255,255),sp=3,anchor="c")
if compact:
    text(W/2,296,a.heading,fit(a.heading,XB,100,W-80),navy,anchor="c")
    if a.part: text(W/2,406,a.part,fit(a.part,BD,32,W-80),navy,anchor="c")
    cx0,cx1=60,1020; ch=138; gap=8; y0=462; hf_s,df_s,step,bd=30,25,32,44
else:
    text(W/2,330,a.heading,fit(a.heading,XB,120,W-80),navy,anchor="c")
    rr((W/2-60,486,W/2+60,494),4,fill=orange)
    if a.part: text(W/2,512,a.part,fit(a.part,BD,38,W-80),navy,anchor="c")
    cx0,cx1=60,1020; ch=218; gap=18; y0=584; hf_s,df_s,step,bd=34,28,37,54
def wrap(t,font,maxw):
    words=t.split(); lines=[]; cur=""
    for w in words:
        trial=(cur+" "+w).strip()
        if tw(trial,font)<=maxw: cur=trial
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
hf=F(BD,hf_s); df=F(MD,df_s)
for i,(h,t) in enumerate(items):
    y=y0+i*(ch+gap)
    shadow((cx0,y,cx1,y+ch),22,blur=10 if compact else 14,off=6 if compact else 8,alpha=34)
    rr((cx0,y,cx1,y+ch),22,fill=card,outline=line,width=2)
    rr((cx0,y+(20 if compact else 28),cx0+7,y+(60 if compact else 78)),3,fill=orange)
    by=y+(14 if compact else 24)
    ell((cx0+28,by,cx0+28+bd,by+bd),fill=navy); text(cx0+28+bd/2,by+(bd-hf_s)/2-2,str(a.first+i),F(XB,hf_s),(255,255,255),anchor="c")
    text(cx0+28+bd+20,by+(bd-hf_s)/2-2,h.strip(),fit(h.strip(),BD,hf_s,cx1-cx0-28-bd-40),navy)
    lines=wrap(t.strip(),df,cx1-cx0-60); assert len(lines)<=(2 if compact else 4),("detail too long",t,len(lines))
    for k,ln in enumerate(lines): text(cx0+30,by+bd+(4 if compact else 22)+k*step,ln,df,ink)
if a.note:
    ny=y0+n*ch+(n-1)*gap+(10 if compact else 20); nh=38 if compact else 50
    rr((cx0,ny,cx1,ny+nh),22,fill=(253,238,224)); text(W/2,ny+(nh-23)/2-3,a.note,fit(a.note,SB,23,cx1-cx0-30),(150,70,10),anchor="c")
# footer card (inside safe area: ends by y=1680)
fb=(50,1390,1030,1716); shadow(fb,30,blur=18,off=10,alpha=50)
rr(fb,30,fill=card,outline=line,width=2)
rect((fb[0]+30,fb[1],fb[0]+330,fb[1]+6),orange); rect((fb[0]+330,fb[1],fb[0]+660,fb[1]+6),navy); rect((fb[0]+660,fb[1],fb[2]-30,fb[1]+6),green)
logo=Image.open(LOGO); lh=P(104); lw=int(logo.width*lh/logo.height)
img.alpha_composite(logo.resize((lw,lh),Image.LANCZOS),(P(fb[0]+34),P(fb[1]+30))); d=ImageDraw.Draw(img)
nx=fb[0]+34+lw/S+26
text(nx,fb[1]+24,"JJR ASSOCIATES",fit("JJR ASSOCIATES",SER,56,fb[2]-nx-30),navy)
rect((nx,fb[1]+90,fb[2]-34,fb[1]+92),green)
text(nx,fb[1]+100,"CHARTERED ACCOUNTANTS",F(SERR,23),green,sp=2,maxw=fb[2]-20)
text(W/2,fb[1]+146,"www.jjrassociates.co.in",F(BD,27),navy,anchor="c")
rect((fb[0]+34,fb[1]+186,fb[2]-34,fb[1]+188),line)
def pin(x,y):
    ell((x,y,x+20,y+20),fill=orange); d.polygon([(P(x+3),P(y+15)),(P(x+17),P(y+15)),(P(x+10),P(y+30))],fill=orange); ell((x+6,y+6,x+14,y+14),fill=(255,255,255))
def office(x,label,name,phone):
    pin(x,fb[1]+202); text(x+30,fb[1]+202,label,F(BD,22),navy,sp=1.5)
    text(x+30,fb[1]+234,name,F(XB,27),navy)
    text(x+30,fb[1]+268,phone,F(XB,30),green)
office(fb[0]+60,"HEAD OFFICE · NEDUMKANDAM","CA JUSTIN SCARIA","6282535310")
rect((W/2-1,fb[1]+200,W/2+1,fb[3]-22),line)
office(W/2+34,"BRANCH · MANARCADU","CA ROHAN JOSE","9037776493")
out=img.convert("RGB").resize((W,H),Image.LANCZOS)
os.makedirs(os.path.dirname(os.path.abspath(a.out)),exist_ok=True)
out.save(a.out,quality=92,optimize=True) if a.out.lower().endswith((".jpg",".jpeg")) else out.save(a.out)
print("saved",a.out,out.size)
