"""Deterministically render the entry locally (requires Pillow, not at runtime)."""
from pathlib import Path
import hashlib
import random
from PIL import Image, ImageDraw, ImageFont

S = 3
PAPER = '#f2ead9'
INK = '#252a2b'
RED = '#b4332b'
MUTED = '#bfb8a9'
LIGHT = '#ddd4c2'
im = Image.new('RGB', (1024*S, 1024*S), PAPER)
d = ImageDraw.Draw(im)
FONTS = Path('/usr/share/fonts/truetype/dejavu')
def font(size, bold=False):
    return ImageFont.truetype(str(FONTS / ('DejaVuSans-Bold.ttf' if bold else 'DejaVuSans.ttf')), round(size*S))
def poly(points, fill=INK):
    d.polygon([(round(x*S),round(y*S)) for x,y in points], fill=fill)
def rect(box, fill=INK, outline=None, width=1):
    d.rectangle(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=width*S)
def ellipse(box, fill=INK, outline=None, width=1):
    d.ellipse(tuple(round(v*S) for v in box), fill=fill, outline=outline, width=width*S)
def line(points, fill=INK, width=2):
    d.line([(round(x*S),round(y*S)) for x,y in points], fill=fill, width=width*S, joint='curve')
def text(x,y,value,size=12,bold=False,fill=INK,center=False):
    f=font(size,bold)
    box=d.textbbox((0,0),value,font=f)
    w=box[2]-box[0]
    if center: x-=w/(2*S)
    d.text((round(x*S)-box[0],round(y*S)-box[1]),value,font=f,fill=fill)
    return w/S

# Newspaper masthead and rigid six-cell grid.
text(36,29,'SUNDAY EDITION',12,True)
w=text(0,-100,'WORLD BULLETIN',12,True)
text(988-w,29,'WORLD BULLETIN',12,True)
text(512,61,'22 NOVEMBER 2026',65,True,center=True)
line([(36,143),(988,143)],width=5)
line([(36,153),(988,153)],width=1)
for y in (428,702,976): line([(36,y),(988,y)],width=2)
line([(512,166),(512,963)],width=2)

# All art uses the same 420 x 170 stage, relative to its cell.
def art_origin(col,row): return (64+col*476,170+row*274)
def panel(col,row,headline,draw_art):
    x,y=art_origin(col,row)
    draw_art(x,y)
    for i,wordline in enumerate(headline):
        f=font(30,True)
        bb=d.textbbox((0,0),wordline,font=f)
        assert bb[2]-bb[0] <= 420*S
        text(x,y+181+i*35,wordline,30,True)
    text(x+396,y+239,'NOV 22',10,True,RED,True)

def base(x,y):
    line([(x,y+158),(x+420,y+158)],width=2)
    rect((x+12,y+118,x+156,y+156),INK)
    poly([(x,y+118),(x+83,y+83),(x+169,y+118)])
    for a in (25,66,107): rect((x+a,y+130,x+a+24,y+156),PAPER)
    rect((x+179,y+97,x+206,y+156),INK)
    rect((x+173,y+83,x+213,y+101),INK)
    rect((x+185,y+88,x+201,y+94),PAPER)
    line([(x+193,y+83),(x+193,y+56)],width=3)
    poly([(x+268,y+156),(x+248,y+132),(x+271,y+132),(x+250,y+103),(x+280,y+112),(x+282,y+76),(x+302,y+107),(x+329,y+85),(x+321,y+119),(x+356,y+113),(x+335,y+137),(x+364,y+156)],RED)
    line([(x+383,y+12),(x+326,y+49),(x+294,y+93)],RED,5)
    line([(x+351,y+12),(x+313,y+35)],RED,2)
    poly([(x+294,y+93),(x+297,y+74),(x+309,y+82)],RED)

def tax(x,y):
    rect((x+199,y+39,x+317,y+142),INK)
    for a in range(211,310,19):
        rect((x+a,y+25,x+a+6,y+39),INK)
        rect((x+a,y+142,x+a+6,y+156),INK)
    for a in range(51,140,19):
        rect((x+185,y+a,x+199,y+a+6),INK)
        rect((x+317,y+a,x+331,y+a+6),INK)
    rect((x+214,y+54,x+302,y+127),PAPER)
    text(x+258,y+66,'%',56,True,RED,True)
    for a in (142,132,122): ellipse((x+53,y+a-30,x+167,y+a),MUTED,INK,2)
    ellipse((x+47,y+30,x+170,y+144),PAPER,INK,4)
    ellipse((x+57,y+40,x+160,y+134),None,INK,1)
    text(x+108,y+53,'€',69,True,INK,True)

def cartel(x,y):
    poly([(x+49,y+11),(x+231,y+20),(x+222,y+165),(x+40,y+156)],LIGHT)
    rect((x+58,y+13,x+224,y+156),PAPER,INK,3)
    text(x+141,y+26,'WANTED',25,True,center=True)
    line([(x+72,y+61),(x+210,y+61)],width=2)
    ellipse((x+118,y+76,x+165,y+119),INK)
    poly([(x+93,y+143),(x+101,y+121),(x+141,y+106),(x+180,y+121),(x+188,y+143)])
    for a,b in ((271,111),(355,117)):
        ellipse((x+a-29,y+b-34,x+a+29,y+b+27),INK)
        ellipse((x+a-19,y+b-24,x+a+19,y+b+17),PAPER)
        rect((x+a-12,y+b-39,x+a+12,y+b-29),RED)
    line([(x+283,y+75),(x+299,y+56),(x+322,y+56),(x+343,y+80)],INK,8)
    ellipse((x+301,y+47,x+320,y+66),PAPER,INK,4)

def quake(x,y):
    poly([(x+7,y+154),(x+106,y+21),(x+163,y+103),(x+218,y+47),(x+310,y+154)],INK)
    poly([(x+78,y+59),(x+106,y+21),(x+141,y+71),(x+114,y+61),(x+101,y+72)],PAPER)
    poly([(x+192,y+79),(x+218,y+47),(x+247,y+82),(x+219,y+72),(x+207,y+86)],PAPER)
    text(x+352,y+38,'6.9',46,True,center=True)
    line([(x,y+133),(x+108,y+133),(x+126,y+117),(x+144,y+152),(x+169,y+106),(x+190,y+158),(x+212,y+126),(x+230,y+133),(x+420,y+133)],PAPER,9)
    line([(x,y+133),(x+108,y+133),(x+126,y+117),(x+144,y+152),(x+169,y+106),(x+190,y+158),(x+212,y+126),(x+230,y+133),(x+420,y+133)],RED,4)

def border(x,y):
    rect((x+39,y+17,x+53,y+159),INK)
    rect((x+365,y+17,x+379,y+159),INK)
    for a in range(67,360,25): rect((x+a,y+40,x+a+7,y+156),INK)
    line([(x+53,y+55),(x+365,y+55)],width=6)
    line([(x+53,y+139),(x+365,y+139)],width=6)
    rect((x+201,y+38,x+216,y+159),INK)
    ellipse((x+162,y+57,x+255,y+150),PAPER,RED,9)
    line([(x+178,y+73),(x+239,y+134)],RED,9)
    line([(x+18,y+159),(x+401,y+159)],width=3)

def deal(x,y):
    # US flag, podium and signed-page silhouette.
    rect((x+39,y+10,x+43,y+160),INK)
    rect((x+43,y+13,x+153,y+81),PAPER,INK,1)
    for a in range(13,81,10): rect((x+44,y+a,x+153,y+a+4),RED)
    rect((x+44,y+13,x+94,y+49),INK)
    for a in range(51,91,11):
        for b in range(20,47,11): ellipse((x+a,y+b,x+a+3,y+b+3),PAPER)
    poly([(x+121,y+97),(x+256,y+97),(x+241,y+158),(x+137,y+158)],INK)
    rect((x+112,y+87,x+264,y+98),INK)
    ellipse((x+175,y+109,x+203,y+137),PAPER)
    line([(x+192,y+86),(x+203,y+63),(x+221,y+63)],width=3)
    ellipse((x+219,y+59,x+229,y+66),INK)
    rect((x+288,y+16,x+391,y+151),PAPER,INK,3)
    poly([(x+364,y+16),(x+364,y+43),(x+391,y+43)],LIGHT)
    for b in (59,72,85): line([(x+303,y+b),(x+374,y+b)],width=2)
    line([(x+304,y+121),(x+317,y+132),(x+352,y+101)],RED,6)

panel(0,0,['IRAN HITS','US BASE'],base)
panel(1,0,['EU DIGITAL TAX'],tax)
panel(0,1,['CARTEL BOSS','CAUGHT'],cartel)
panel(1,1,['PERU QUAKE 6.9'],quake)
panel(0,2,['ESTONIA CLOSES','BORDER'],border)
panel(1,2,['PERMANENT','DEAL VOW'],deal)
im=im.resize((1024,1024),Image.Resampling.LANCZOS)
# A fixed seed gives a fine paper grain without changing repeat renders.
rng=random.Random(22112026)
pixels=bytearray(im.tobytes())
for i in range(0,len(pixels),3):
    grain=rng.choices((-1,0,1),weights=(1,8,1))[0]
    for j in range(3): pixels[i+j]=max(0,min(255,pixels[i+j]+grain))
im=Image.frombytes('RGB',im.size,bytes(pixels))
path=Path(__file__).with_name('entry.png')
im.save(path,optimize=True,compress_level=9)
print(hashlib.sha256(path.read_bytes()).hexdigest())
