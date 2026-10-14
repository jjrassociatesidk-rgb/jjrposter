#!/usr/bin/env python3
"""Tax audit decision-tree flowchart page (1080x1350) with the standard JJR footer. Edit the layout in this file. JJR Associates Instagram FEED POST generator (1080x1350, 4:5) for informational updates.
Usage: python3 tools/make_post.py --chip "GST COUNCIL UPDATE" --heading "57th GST Council" \
  --subtitle "Key takeaways from the meeting of 8 October 2026" --subline "Focus on process reform" \
  --cards "Arrest power removed::Prosecution limit raised to Rs 5 crore|Faster refunds::Acknowledgement in 10 days" \
  --note "Council recommendations - effective only after notification." --out posters/post.jpg
Up to 6 cards ("Headline::detail", separated by |). Headline max ~28 chars; detail max ~85 chars."""
import argparse, os
ap=argparse.ArgumentParser()
ap.add_argument("--chip",default="TAX AUDIT · 3 OF 4"); ap.add_argument("--heading",default="Do You Need a Tax Audit?"); ap.add_argument("--subtitle",default="Section 44AB · FY 2025-26 (AY 2026-27)")
ap.add_argument("--subline",default=""); ap.add_argument("--cards",default=""); ap.add_argument("--note",default=""); ap.add_argument("--out",required=True)
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
cf=F(BD,22); cw=tw(a.chip,cf,3)+56
rr((W/2-cw/2,34,W/2+cw/2,76),21,fill=navy); text(W/2,43,a.chip,cf,(255,255,255),sp=3,anchor="c")
text(W/2,82,a.heading,fit(a.heading,XB,66,W-70),navy,anchor="c")
rr((W/2-50,166,W/2+50,172),3,fill=orange)
text(W/2,182,a.subtitle,fit(a.subtitle,BD,23,W-80),mute,anchor="c")

LINE=(70,86,110)
def arrow_v(x,y0,y1,lab=None,lab_side="r"):
    d.line([(P(x),P(y0)),(P(x),P(y1-8))],fill=LINE,width=P(3))
    d.polygon([(P(x-8),P(y1-12)),(P(x+8),P(y1-12)),(P(x),P(y1))],fill=LINE)
    if lab:
        lw=tw(lab,F(XB,18),1)
        text(x+10 if lab_side=="r" else x-10-lw,(y0+y1)/2-12,lab,F(XB,18),green,sp=1)
def arrow_h(x0,x1,y,lab):
    d.line([(P(x0),P(y)),(P(x1-8),P(y))],fill=LINE,width=P(3))
    d.polygon([(P(x1-12),P(y-8)),(P(x1-12),P(y+8)),(P(x1),P(y))],fill=LINE)
    lw=tw(lab,F(XB,18),1); text((x0+x1)/2-lw/2,y-26,lab,F(XB,18),(190,60,40),sp=1)
def box(b,t,size=22,kind="q"):
    fills={"q":(card,navy,navy),"ok":((226,243,233),green,(20,100,55)),"req":((253,236,222),orange,(160,70,10)),"note":((238,243,250),line,ink)}
    f,o,c=fills[kind]
    shadow(b,16,blur=8,off=5,alpha=26) if kind=="q" else None
    rr(b,16,fill=f,outline=o,width=2)
    fnt=F(BD if kind!="note" else MD,size)
    while True:
        lines=wrap(t,fnt,b[2]-b[0]-22)
        lh=size*1.22
        if len(lines)*lh<=b[3]-b[1]-10 or size<=15: break
        size-=1; fnt=F(BD if kind!="note" else MD,size)
    y=(b[1]+b[3])/2-len(lines)*lh/2
    for ln in lines:
        text((b[0]+b[2])/2,y-1,ln,fnt,c,anchor="c"); y+=lh
LX0,LX1=40,340; RX0,RX1=560,860; LA=(LX0+LX1)/2; RA=(RX0+RX1)/2
# column pills
rr((LA-110,226,LA+110,262),18,fill=navy); text(LA,232,"BUSINESS",F(XB,21),(255,255,255),sp=2,anchor="c")
rr((RA-120,226,RA+120,262),18,fill=orange); text(RA,232,"PROFESSION",F(XB,21),(255,255,255),sp=2,anchor="c")
rows=[(290,362),(434,514),(592,686)]
# business column
L=["Turnover above ₹1 crore?","Cash receipts and payments each 5% or less?","Turnover above ₹10 crore?"]
R=["Gross receipts above ₹50 lakh?","Opted for presumptive Sec 44ADA?","Receipts up to ₹75 lakh and cash receipts 5% or less?"]
for (y0,y1),lt,rt in zip(rows,L,R):
    box((LX0,y0,LX1,y1),lt,23); box((RX0,y0,RX1,y1),rt,23)
for k in range(2):
    arrow_v(LA,rows[k][1],rows[k+1][0],"YES"); arrow_v(RA,rows[k][1],rows[k+1][0],"YES")
# side results
SL=(384,522); SR=(904,1042)
def side(x0,x1,row,t,kind):
    y0,y1=rows[row]; yc=(y0+y1)/2
    arrow_h(LX1 if x0<500 else RX1,x0,yc,"NO")
    box((x0,yc-34,x1,yc+34),t,19,kind)
side(*SL,0,"Audit not required","ok"); side(*SL,1,"Audit required (₹1 crore limit)","req"); side(*SL,2,"Audit not required","ok")
side(*SR,0,"Audit not required","ok"); side(*SR,1,"Audit required (₹50 lakh limit)","req"); side(*SR,2,"Audit required (₹50 lakh limit)","req")
# final results under third questions
arrow_v(LA,rows[2][1],752,"YES"); box((LX0,752,LX1,806),"Audit required (₹10 crore limit)",20,"req")
arrow_v(RA,rows[2][1],752,"YES"); box((RX0,752,RX1,806),"Audit not required (Sec 44ADA)",20,"ok")
# presumptive notes
box((LX0,826,522,892),"Up to ₹2 crore (₹3 crore if cash is 5% or less)? Opt for 44AD and declare 8% (6% digital): no audit.",18,"note")
box((RX0,826,1042,892),"Up to ₹50 lakh (₹75 lakh if cash is 5% or less)? Opt for 44ADA and declare 50%: no audit.",18,"note")
rr((40,912,W-40,956),21,fill=(253,238,224))
note="Declaring less than the presumptive profit can bring an audit. Other laws may need audit separately."
text(W/2,919,note,fit(note,SB,21,W-100),(150,70,10),anchor="c")

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
rect((46,FT+200,W-46,FT+202),line)
def pin(x,y):
    ell((x,y,x+22,y+22),fill=orange); d.polygon([(P(x+3),P(y+16)),(P(x+19),P(y+16)),(P(x+11),P(y+34))],fill=orange); ell((x+7,y+7,x+15,y+15),fill=(255,255,255))
def phone_icon(x,y):
    rr((x,y,x+15,y+26),4,fill=green); rr((x+3,y+4,x+12,y+19),1,fill=(255,255,255)); ell((x+5.5,y+20.5,x+9.5,y+24.5),fill=(255,255,255))
def person_icon(x,y):
    ell((x+4,y,x+17,y+13),fill=orange); d.pieslice([P(x),P(y+15),P(x+21),P(y+39)],180,360,fill=orange)
def office(x,label,name,l1,l2,phone):
    person_icon(x,FT+226); text(x+34,FT+224,name,F(XB,28),navy)
    text(x+34,FT+262,l1,F(MD,25),ink,maxw=x+470); text(x+34,FT+290,l2,F(MD,25),ink,maxw=x+470)
    phone_icon(x+4,FT+330); text(x+34,FT+328,phone,F(XB,28),green)
office(46,"","CA Justin Scaria","Central Junction,","Nedumkandam, Idukki","+91 62825 35310")
rect((W/2-1,FT+222,W/2+1,FT+346),line)
office(586,"","CA Rohan Jose","Chavacheril Building, KK Road,","Manarcadu, Kottayam","+91 90377 76493")
out=img.convert("RGB").resize((W,H),Image.LANCZOS); os.makedirs(os.path.dirname(os.path.abspath(a.out)),exist_ok=True); out.save(a.out,quality=92,optimize=True) if a.out.lower().endswith((".jpg",".jpeg")) else out.save(a.out); print(out.size)
