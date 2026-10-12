#!/usr/bin/env python3
"""JJR Associates Instagram STORY generator (1080x1920, 9:16) for daily due-date alerts.
Usage: python3 tools/make_story.py --heading "GSTR-1" --title "Outward Supplies Return" \
  --sub "For QRMP (quarterly) filers" --date "13 October 2026" --badge "DUE TOMORROW" \
  --points "Reconcile sales invoices|Avoid late fees|Protect buyers' ITC" --out posters/story.jpg
Keep key content inside y=230..1680 (Instagram story UI covers the top/bottom edges)."""
import argparse, os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ap=argparse.ArgumentParser()
ap.add_argument("--heading",required=True); ap.add_argument("--title",required=True); ap.add_argument("--sub",default="")
ap.add_argument("--date",required=True); ap.add_argument("--badge",default="DUE DATE ALERT"); ap.add_argument("--label",default="LAST DATE TO FILE")
ap.add_argument("--points",default=""); ap.add_argument("--out",required=True)
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
# header (safe zone starts ~y=230)
cf=F(BD,26); cw=tw(a.badge,cf,3)+70
rr((W/2-cw/2,250,W/2+cw/2,304),27,fill=orange); text(W/2,262,a.badge,cf,(255,255,255),sp=3,anchor="c")
text(W/2,340,a.heading,fit(a.heading,XB,210,W-100),navy,anchor="c")
rr((W/2-60,590,W/2+60,598),4,fill=orange)
text(W/2,626,a.title,fit(a.title,BD,56,W-100),navy,anchor="c")
if a.sub: text(W/2,704,a.sub,fit(a.sub,MD,30,W-100),mute,anchor="c")
# due date card
cb=(80,790,1000,1040); shadow(cb,32,blur=22,off=14,alpha=70)
rr(cb,32,fill=orange); rr((cb[0]+14,cb[1],cb[2],cb[3]),32,fill=navy,corners=(False,True,True,False))
ix,iy=cb[0]+60,cb[1]+70
rr((ix,iy,ix+110,iy+110),18,fill=(255,255,255)); rr((ix,iy,ix+110,iy+34),18,fill=orange); rect((ix,iy+18,ix+110,iy+34),orange)
for r_ in range(2):
    for c_ in range(3): rr((ix+16+c_*29,iy+48+r_*30,ix+34+c_*29,iy+64+r_*30),3,fill=navy)
tx=cb[0]+210
text(tx,cb[1]+52,a.label,F(BD,26),(255,196,120),sp=3)
text(tx,cb[1]+100,a.date,fit(a.date,XB,78,cb[2]-tx-24),(255,255,255))
# points
pts=[p for p in a.points.split("|") if p.strip()]
pf=F(SB,34); y0=1120
if pts:
    maxw=max(tw(p,pf) for p in pts)+60; x0=W/2-maxw/2
    assert maxw<W-80,"points too wide"
    for i,p in enumerate(pts[:3]):
        y=y0+i*64
        ell((x0,y+2,x0+42,y+44),fill=green)
        d.line([(P(x0+11),P(y+24)),(P(x0+18),P(y+31)),(P(x0+31),P(y+15))],fill=(255,255,255),width=P(5),joint="curve")
        text(x0+62,y+3,p,pf,ink)
# footer card (inside safe area: ends by y=1680)
fb=(50,1390,1030,1680); shadow(fb,30,blur=18,off=10,alpha=50)
rr(fb,30,fill=card,outline=line,width=2)
rect((fb[0]+30,fb[1],fb[0]+330,fb[1]+6),orange); rect((fb[0]+330,fb[1],fb[0]+660,fb[1]+6),navy); rect((fb[0]+660,fb[1],fb[2]-30,fb[1]+6),green)
logo=Image.open(LOGO); lh=P(104); lw=int(logo.width*lh/logo.height)
img.alpha_composite(logo.resize((lw,lh),Image.LANCZOS),(P(fb[0]+34),P(fb[1]+30))); d=ImageDraw.Draw(img)
nx=fb[0]+34+lw/S+26
text(nx,fb[1]+24,"JJR ASSOCIATES",fit("JJR ASSOCIATES",SER,56,fb[2]-nx-30),navy)
rect((nx,fb[1]+90,fb[2]-34,fb[1]+92),green)
text(nx,fb[1]+100,"CHARTERED ACCOUNTANTS",F(SERR,23),green,sp=2,maxw=fb[2]-20)
text(W/2,fb[1]+152,"www.jjrassociates.co.in",F(BD,27),navy,anchor="c")
rect((fb[0]+34,fb[1]+194,fb[2]-34,fb[1]+196),line)
def pin(x,y):
    ell((x,y,x+20,y+20),fill=orange); d.polygon([(P(x+3),P(y+15)),(P(x+17),P(y+15)),(P(x+10),P(y+30))],fill=orange); ell((x+6,y+6,x+14,y+14),fill=(255,255,255))
def office(x,label,phone):
    pin(x,fb[1]+214); text(x+30,fb[1]+214,label,F(BD,22),navy,sp=1.5)
    text(x+30,fb[1]+244,phone,F(XB,30),green)
office(fb[0]+60,"HEAD OFFICE · NEDUMKANDAM","6282535310")
rect((W/2-1,fb[1]+212,W/2+1,fb[3]-24),line)
office(W/2+34,"BRANCH · MANARCADU","9037776493")
out=img.convert("RGB").resize((W,H),Image.LANCZOS)
os.makedirs(os.path.dirname(os.path.abspath(a.out)),exist_ok=True)
out.save(a.out,quality=92,optimize=True) if a.out.lower().endswith((".jpg",".jpeg")) else out.save(a.out)
print("saved",a.out,out.size)
