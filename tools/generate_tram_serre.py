import random, math, os
from PIL import Image, ImageDraw, ImageFont
W,H=128,192
BK=(12,28,26);D1=(30,58,52);D2=(46,84,70);D3=(78,128,104);GD=(24,104,60);GM=(44,196,98);G=(38,253,117)
Y1=(96,112,104);Y2=(138,156,146);Y3=(184,198,190);WH=(214,224,217);SK=(176,146,120);BR=(112,74,44);BD=(72,46,28)
B4=[[0,8,2,10],[12,4,14,6],[3,11,1,9],[15,7,13,5]]
bay=lambda x,y:(B4[y%4][x%4]+.5)/16
def fnt(sz):
    for p in('/usr/share/fonts/truetype/dejavu/DejaVuSansMono-Bold.ttf','/usr/share/fonts/dejavu/DejaVuSansMono-Bold.ttf'):
        if os.path.exists(p):return ImageFont.truetype(p,sz)
class S:
    def __init__(s,bg=D1):
        s.im=Image.new('RGB',(W,H),bg);s.p=s.im.load();s.d=ImageDraw.Draw(s.im);s.d.fontmode="1"
    def px(s,x,y,c):
        if 0<=x<W and 0<=y<H:s.p[x,y]=c
    def r(s,x0,y0,x1,y1,c):s.d.rectangle((x0,y0,x1,y1),fill=c)
    def grad(s,y0,y1,c1,c2):
        for y in range(y0,y1+1):
            t=(y-y0)/max(1,y1-y0)
            for x in range(W):s.px(x,y,c2 if t>bay(x,y) else c1)
    def halo(s,cx,cy,rad,k=1.0,strong=G):
        for y in range(max(0,cy-rad),min(H,cy+rad+1)):
            for x in range(max(0,cx-rad),min(W,cx+rad+1)):
                t=(1-math.hypot(x-cx,(y-cy)*1.15)/rad)*k
                if t>0 and t**1.2>bay(x,y):s.px(x,y,strong if t>.6 else GM if t>.3 else GD)
    def vines(s,x0,x1,y0,y1):
        for i in range(x0,x1,2):
            ph=random.random()*6
            for y in range(y0,y1):
                s.px(i+int(2*math.sin(y/4+ph)),y,random.choice([GD,GD,GM]))
                if random.random()<.03:s.px(i+1+int(2*math.sin(y/4+ph)),y,G)
    def leaves(s,n,xr,yr,cols=None):
        for _ in range(n):
            x=random.randint(*xr);y=random.randint(*yr);s.d.ellipse((x,y,x+random.randint(3,8),y+random.randint(2,4)),fill=random.choice(cols or (GD,GM,GD)))
    def save(s,name,grain=140):
        for _ in range(grain):
            x,y=random.randrange(W),random.randrange(H);c=s.p[x,y];s.p[x,y]=tuple(max(0,v-6) for v in c)
        s.im.save(f'assets/scenes/{name}.png')
random.seed(7)
def canopy(s,n):
    for _ in range(n):
        x=random.choice([random.randint(0,30),random.randint(98,127)]);y=random.choice([random.randint(0,24),random.randint(150,191)])
        w=random.randint(6,16);h=random.randint(4,9);c=random.choice([GD,GM,GD,GM,G])
        s.d.ellipse((x,y,x+w,y+h),fill=c);s.d.ellipse((x+2,y+1,x+w-2,y+h-3),fill=GD if c!=GD else GM)

SKY1=(118,186,178);SKY2=(196,236,206);GLASS=(150,206,184);GLASS2=(176,224,200);TW=(222,232,226);TG=(170,186,178)
def tram():
    """Station de tram façon Strasbourg : rame claire aux grandes vitres, voie engazonnée, caténaires."""
    random.seed(21)
    global H
    H=202;s=S(D2);s.grad(0,96,SKY1,SKY2)
    for x0,w,h in((0,22,40),(20,16,28),(34,26,46),(58,18,32),(74,24,52),(96,14,30),(108,20,44)):
        s.r(x0,96-h,x0+w,96,D3);[s.r(xx,96-h+5,xx+2,96-h+8,Y3) for xx in range(x0+3,x0+w-2,6) if random.random()<.5]
    for px_ in(8,120):s.r(px_,14,px_+2,150,Y1);s.r(px_-1,14,px_+3,16,Y2)
    s.d.line((0,26,127,22),fill=Y1);s.d.line((0,34,127,34),fill=BK)
    for x in range(14,120,14):s.d.line((x,25,x,34),fill=Y1)
    s.r(0,98,127,140,D3)
    # rame
    s.r(2,60,111,128,TW);s.d.polygon([(111,60),(120,64),(126,76),(127,128),(111,128)],fill=TW)
    s.r(2,57,111,60,TG);s.d.line((52,57,64,40),fill=Y1,width=1);s.d.line((64,40,76,57),fill=Y1);s.d.line((58,40,70,40),fill=Y1);s.d.line((64,40,64,34),fill=Y1)
    s.r(2,66,111,104,BK)
    for x in range(4,108,17):
        s.r(x,67,x+14,103,(30,64,60))
        for y in range(67,104):
            for xx in range(x,x+15):
                if bay(xx,y)<.18:s.px(xx,y,(52,96,90))
        s.d.line((x+2,100,x+10,70),fill=(84,130,122))
    s.d.polygon([(112,66),(119,68),(124,80),(124,104),(112,104)],fill=(30,64,60));s.d.line((114,98,120,74),fill=(84,130,122))
    s.r(2,106,126,109,G);s.r(2,110,126,111,GM)
    s.r(68,64,88,128,TG);s.r(70,66,86,126,(24,52,48));s.r(77,66,78,126,TG)
    s.halo(78,96,16,.75);s.r(72,84,84,92,GD)
    for i,xx in enumerate(range(73,84,2)):s.r(xx,92-[2,5,7,4,6,3][i%6],xx,91,G)
    s.r(2,128,126,131,Y1)
    for bx in(14,46,98):s.d.ellipse((bx-6,128,bx+6,140),fill=BK);s.d.ellipse((bx-3,131,bx+3,137),fill=Y1)
    s.r(0,138,127,140,Y3)
    # quai
    s.r(0,141,127,147,Y2);s.r(0,141,127,141,Y3);s.r(0,147,127,148,Y1)
    for x in range(0,128,8):s.r(x,144,x+3,145,(238,232,140) if x%16==0 else Y2)
    # abri
    s.r(3,86,32,88,Y3);s.r(4,88,5,141,Y1);s.r(30,88,31,141,Y1)
    for y in range(89,140):
        for x in range(6,30):
            if bay(x,y)<.35:s.px(x,y,GLASS2)
    # voie engazonnée au premier plan
    for y in range(149,186):
        for x in range(128):s.px(x,y,GM if bay(x,y)<.42 else GD)
    for _ in range(140):
        x=random.randint(0,127);y=random.randint(150,184);s.d.line((x,y,x+random.choice((-1,0,1)),y-2),fill=random.choice((G,GM,GD)))
    s.r(0,153,127,154,Y3);s.r(0,155,127,155,Y1);s.r(0,175,127,176,Y3);s.r(0,177,127,177,Y1)
    # plaque entre les rails
    s.r(90,159,112,171,Y1);s.r(91,160,111,170,Y2)
    for y in range(161,170,2):s.r(92,y,110,y,Y1)
    s.r(90,159,112,159,Y3);s.px(93,162,GD);s.px(108,168,GD)
    s.r(0,186,127,191,Y1);s.r(0,186,127,186,Y3)
    s.vines(118,124,40,128);s.vines(120,126,14,150);s.vines(6,10,20,150)
    s.leaves(14,(0,14),(150,186),(GD,GM,G));s.leaves(14,(110,127),(130,190));s.leaves(10,(0,40),(120,141))
    s.r(0,186,127,201,Y1);s.r(0,186,127,186,Y3)
    canopy(s,22);s.im=s.im.crop((0,10,128,202));s.p=s.im.load();s.d=ImageDraw.Draw(s.im);H=192;s.save('tram')
def greenhouse():
    """Serre vitrée lumineuse : charpente, allée, bacs de culture, établi et petite estrade pour Noli."""
    random.seed(33)
    s=S(D2)
    s.grad(0,120,SKY2,GLASS)
    for y in range(0,120):
        for x in range(128):
            if bay(x,y)<.10:s.px(x,y,GLASS2)
    s.d.polygon([(0,0),(64,0),(0,26)],fill=GLASS2);s.d.polygon([(127,0),(64,0),(127,26)],fill=GLASS2)
    s.d.line((0,26,64,0),fill=Y1,width=2);s.d.line((64,0,127,26),fill=Y1,width=2)
    for x in range(0,128,16):s.r(x,max(0,26-abs(64-x)*26//64),x+1,120,Y1)
    for y in(44,82):s.r(0,y,127,y+1,Y1)
    s.r(0,118,127,121,Y2)
    for x in range(16,128,32):s.d.line((x,6,x+4,40),fill=GD);s.leaves(6,(x-2,x+8),(36,52),(GD,GM,G))
    for _ in range(22):
        x=random.randint(0,127);s.vines(x,x+2,0,random.randint(10,46))
    # sol et allée en perspective
    s.r(0,122,127,191,(96,84,64))
    s.d.polygon([(50,122),(78,122),(104,191),(24,191)],fill=Y2)
    for y in range(126,191,7):
        t=(y-122)/69;xl=50-26*t;xr=78+26*t;s.d.line((xl,y,xr,y),fill=Y1)
    s.d.line((64,122,64,191),fill=Y1)
    # bacs de culture
    s.d.polygon([(0,132),(42,124),(30,191),(0,191)],fill=BD);s.d.polygon([(0,130),(42,122),(42,126),(0,134)],fill=BR)
    s.d.polygon([(127,132),(86,124),(98,191),(127,191)],fill=BD);s.d.polygon([(127,130),(86,122),(86,126),(127,134)],fill=BR)
    s.leaves(70,(0,34),(110,186),(GD,GM,G,GM));s.leaves(50,(96,127),(150,190),(GD,GM,G,GM))
    for _ in range(40):
        x=random.choice((random.randint(0,30),random.randint(98,127)));y=random.randint(96,130);s.d.line((x,y,x+random.randint(-3,3),y-random.randint(4,12)),fill=random.choice((GM,G,GD)))
    # établi à gauche (la caméra se pose dessus)
    s.r(18,139,54,142,BR);s.r(18,139,54,139,(170,120,72));s.r(20,143,22,160,BD);s.r(50,143,52,160,BD);s.r(20,152,52,153,BD)
    s.r(40,134,46,138,(96,84,64));s.leaves(3,(39,47),(128,134))
    # estrade de Noli à droite
    s.r(74,120,116,124,(170,120,72));s.r(74,124,116,134,BR)
    for x in range(78,116,8):s.r(x,124,x,134,BD)
    s.halo(95,98,26,.45,GM)
    s.r(108,100,112,124,Y1);s.d.rectangle((105,96,115,101),fill=BK);s.r(107,97,113,100,GD)
    canopy(s,20);s.save('greenhouse')
tram();greenhouse()
