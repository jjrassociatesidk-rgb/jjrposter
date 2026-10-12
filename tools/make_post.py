#!/usr/bin/env python3
"""JJR Associates Instagram FEED POST generator (1080x1350, 4:5) for informational updates.
Usage: python3 tools/make_post.py --chip "GST COUNCIL UPDATE" --heading "57th GST Council" \
  --subtitle "Key takeaways from the meeting of 8 October 2026" --subline "Focus on process reform" \
  --cards "Arrest power removed::Prosecution limit raised to Rs 5 crore|Faster refunds::Acknowledgement in 10 days" \
  --note "Council recommendations - effective only after notification." --out posters/post.jpg
Up to 6 cards ("Headline::detail", separated by |). Headline max ~28 chars; detail max ~85 chars."""
import argparse, os
ap=argparse.ArgumentParser()
ap.add_argument("--chip",required=True); ap.add_argument("--heading",required=True); ap.add_argument("--subtitle",required=True)
ap.add_argument("--subline",default=""); ap.add_argument("--cards",required=True); ap.add_argument("--note",default=""); ap.add_argument("--out",required=True)
a=ap.parse_args()
LOGO=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","assets","ca_logo.png")
from PIL import Image, ImageDraw, ImageFont, ImageFilter
S=2; W,H=1080,1350
navy=(14,42,71); orange=(226,104,24); green=(34,139,76); ink=(52,66,86); mute=(96,112,134)
bg=(246,248,252); card=(255,255,255); line=(222,229,239)
IF="/usr/share/fonts/opentype/inter/"
XB=IF+"InterDisplay-ExtraBold.otf"; BD=IF+"Inter-Bold.otf"; SB=IF+"Inter-SemiBold.otf"; MD=IF+"Inter-Medium.otf"
SER="/usr/share/fonts/truetype/freefont/FreeSerifBold.ttf"; SERR="/usr/share/fonts/truetype/freefont/FreeSerif.ttf"
img=Image.new("RGBA",(W*S,H*S),bg+(255,)); d=ImageDraw.Draw(img)
P=lambda v:int(round(v*S))
def F(p,s): return ImageFont.truetype(p,P(s))
def rr(b,r,fill=None,outline=None,width=1): d.rounded_rectangle([P(b[0]),P(b[1]),P(b[2]),P(b[3])],radius=P(r),fill=fill,outline=outline,width=P(width) if outline else 0)
def rect(b,fill): d.rectangle([P(b[0]),P(b[1]),P(b[2]),P(b[3])],fill=fill)
def ell(b,fill=None,outline=None,width=1): d.ellipse([P(b[0]),P(b[1]),P(b[2]),P(b[3])],fill=fill,outline=outline,width=P(width) if outline else 0)
def tw(t,font,sp=0): return (d.textlength(t,font=font)+P(sp)*(len(t)-1))/S
def text(x,y,t,font,fill,sp=0,anchor="l",maxw=None):
    w=tw(t,font,sp)
    if anchor=="c": x=x-w/2
    elif anchor=="r": x=x-w
    if maxw: assert x+w<=maxw+0.5,(t,x+w)
    if sp==0: d.text((P(x),P(y)),t,font=font,fill=fill)
    else:
        cx=P(x)
        for ch in t:
            d.text((cx,P(y)),ch,font=font,fill=fill); cx+=d.textlength(ch,font=font)+P(sp)
    return w
def shadow(b,r,blur=18,off=10,alpha=60,color=(14,42,71)):
    global img,d
    L=Image.new("RGBA",img.size,(0,0,0,0)); ld=ImageDraw.Draw(L)
    ld.rounded_rectangle([P(b[0]),P(b[1]+off),P(b[2]),P(b[3]+off)],radius=P(r),fill=color+(alpha,))
    L=L.filter(ImageFilter.GaussianBlur(P(blur))); img=Image.alpha_composite(img,L); d=ImageDraw.Draw(img)

# ---------- background decoration ----------
L=Image.new("RGBA",img.size,(0,0,0,0)); ld=ImageDraw.Draw(L)
ld.ellipse([P(640),P(-230),P(1260),P(390)],fill=(222,233,247,255))
ld.ellipse([P(-330),P(650),P(150),P(1130)],fill=(252,236,222,255))
img=Image.alpha_composite(img,L); d=ImageDraw.Draw(img)
# tricolour-inspired top strip (brand colours from the CA logo)
rect((0,0,W,12),navy); rect((0,0,360,12),orange); rect((360,0,720,12),(255,255,255)); rect((720,0,W,12),green)


def wrap(t,font,maxw):
    words=t.split(); lines=[]; cur=""
    for w in words:
        trial=(cur+" "+w).strip()
        if tw(trial,font)<=maxw: cur=trial
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
# ---------- header ----------
def wrap(t,font,maxw):
    words=t.split(); lines=[]; cur=""
    for w in words:
        trial=(cur+" "+w).strip()
        if tw(trial,font)<=maxw: cur=trial
        else: lines.append(cur); cur=w
    lines.append(cur); return lines
def fit(t,path,start,maxw):
    sz=start
    while sz>20 and tw(t,F(path,sz))>maxw: sz-=2
    return F(path,sz)
cf=F(BD,23); cw=tw(a.chip,cf,3)+60
rr((W/2-cw/2,44,W/2+cw/2,90),23,fill=navy); text(W/2,54,a.chip,cf,(255,255,255),sp=3,anchor="c")
text(W/2,100,a.heading,fit(a.heading,XB,104,W-80),navy,anchor="c")
rr((W/2-60,222,W/2+60,230),4,fill=orange)
text(W/2,246,a.subtitle,fit(a.subtitle,BD,34,W-80),navy,anchor="c")
if a.subline: text(W/2,298,a.subline,fit(a.subline,MD,26,W-80),mute,anchor="c")
items=[tuple(c.split("::",1)) for c in a.cards.split("|") if "::" in c][:6]
n=len(items); rows=(n+1)//2
cw_=478; gap=12; avail=900-344; ch_=min(178,(avail-gap*(rows-1))//rows); gx0=(W-2*cw_-24)/2
hf=F(BD,27); df=F(MD,22)
for i,(h,t) in enumerate(items):
    r,c=divmod(i,2); x=gx0+c*(cw_+24); y=344+r*(ch_+gap)
    shadow((x,y,x+cw_,y+ch_),22,blur=12,off=7,alpha=34)
    rr((x,y,x+cw_,y+ch_),22,fill=card,outline=line,width=2)
    rr((x,y+22,x+6,y+62),3,fill=orange)
    ell((x+24,y+20,x+68,y+64),fill=navy); text(x+46,y+27,str(i+1),F(XB,27),(255,255,255),anchor="c")
    text(x+84,y+28,h.strip(),fit(h.strip(),BD,27,cw_-100),navy)
    lines=wrap(t.strip(),df,cw_-48)
    assert len(lines)<=3,("detail too long",t)
    for k,ln in enumerate(lines): text(x+24,y+78+k*30,ln,df,ink)
if a.note:
    rr((50,914,W-50,954),20,fill=(253,238,224))
    text(W/2,923,a.note,fit(a.note,SB,21,W-110),(150,70,10),anchor="c")

# ---------- footer ----------
FT=972
shadow((0,FT,W,H+40),0,blur=16,off=-6,alpha=45)
rect((0,FT,W,H),card); rect((0,FT,W,FT+5),navy); rect((0,FT,300,FT+5),orange); rect((780,FT,W,FT+5),green)
logo=Image.open(LOGO); lh=P(126); lw=int(logo.width*lh/logo.height)
lg=logo.resize((lw,lh),Image.LANCZOS); img.alpha_composite(lg,(P(46),P(FT+26))); d=ImageDraw.Draw(img)
nx=46+lw/S+34
text(nx,FT+18,"JJR ASSOCIATES",F(SER,66),navy,maxw=W-30)
rect((nx,FT+98,W-46,FT+100),green)
text(nx,FT+110,"CHARTERED ACCOUNTANTS",F(SERR,27),green,sp=2.2,maxw=W-30)
wf=F(BD,27); ww=tw("www.jjrassociates.co.in",wf)
rr((nx,FT+150,nx+ww+86,FT+194),22,fill=navy)
gx,gy=nx+28,FT+172                                         # globe icon
ell((gx-12,gy-12,gx+12,gy+12),outline=(255,255,255),width=2); ell((gx-5,gy-12,gx+5,gy+12),outline=(255,255,255),width=2)
d.line([(P(gx-12),P(gy)),(P(gx+12),P(gy))],fill=(255,255,255),width=P(2))
text(nx+52,FT+158,"www.jjrassociates.co.in",wf,(255,255,255))
rect((46,FT+218,W-46,FT+220),line)
def pin(x,y):
    ell((x,y,x+22,y+22),fill=orange); d.polygon([(P(x+3),P(y+16)),(P(x+19),P(y+16)),(P(x+11),P(y+34))],fill=orange); ell((x+7,y+7,x+15,y+15),fill=(255,255,255))
def office(x,label,name,l1,l2,phone):
    pin(x,FT+238)
    text(x+34,FT+238,label,F(BD,22),navy,sp=2)
    pf2=F(XB,29); text(x+448,FT+233,phone,pf2,green,anchor="r")
    text(x,FT+270,name,F(XB,26),navy)
    text(x,FT+302,l1,F(MD,24),ink,maxw=x+470); text(x,FT+330,l2,F(MD,24),ink,maxw=x+470)
office(46,"HEAD OFFICE","CA Justin Scaria","Central Junction,","Nedumkandam, Idukki","6282535310")
rect((W/2-1,FT+238,W/2+1,FT+356),line)
office(586,"BRANCH","CA Rohan Jose","Chavacheril Building, KK Road,","Manarcadu, Kottayam","9037776493")
out=img.convert("RGB").resize((W,H),Image.LANCZOS); os.makedirs(os.path.dirname(os.path.abspath(a.out)),exist_ok=True); out.save(a.out,quality=92,optimize=True) if a.out.lower().endswith((".jpg",".jpeg")) else out.save(a.out); print(out.size)
