from pathlib import Path
import math, shutil, subprocess
from PIL import Image, ImageDraw, ImageFont, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'public' / 'assets'
FRAMES = ROOT / '.video-frames'
W, H, FPS = 1280, 720, 30
OUT.mkdir(parents=True, exist_ok=True)
if FRAMES.exists(): shutil.rmtree(FRAMES)
FRAMES.mkdir(parents=True)
FONT = '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf'
BOLD = '/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf'
MONO = '/usr/share/fonts/truetype/dejavu/DejaVuSansMono.ttf'
def f(path, size): return ImageFont.truetype(path, size)

def make_base():
    img = Image.new('RGB', (W, H), '#080b18'); d = ImageDraw.Draw(img)
    for y in range(H):
        t = y / H
        d.line((0, y, W, y), fill=(8 + int(8*(1-t)), 12 + int(10*t), 29 + int(29*t)))
    glow = Image.new('RGBA', (W,H), (0,0,0,0)); gd = ImageDraw.Draw(glow)
    gd.ellipse((820,-170,1370,350), fill=(105,75,255,48)); gd.ellipse((-170,480,530,930), fill=(20,210,185,27))
    glow = glow.filter(ImageFilter.GaussianBlur(70)); img = Image.alpha_composite(img.convert('RGBA'), glow)
    d = ImageDraw.Draw(img)
    for step in range(0, W+1, 80): d.line((step,0,step,H), fill=(123,145,200,18), width=1)
    for step in range(0, H+1, 80): d.line((0,step,W,step), fill=(123,145,200,18), width=1)
    for i in range(50):
        x=(i*271+83)%W; y=(i*127+41)%H; a=85 if i%3 else 150; d.ellipse((x,y,x+2,y+2), fill=(199,255,94,a))
    return img
BASE = make_base()

def center(d, xy, text, font, fill, anchor='mm'): d.text(xy,text,font=font,fill=fill,anchor=anchor)
def shield(d,cx,cy,scale=1.0):
    pts=[(cx,cy-74*scale),(cx+58*scale,cy-50*scale),(cx+49*scale,cy+25*scale),(cx,cy+75*scale),(cx-49*scale,cy+25*scale),(cx-58*scale,cy-50*scale)]
    d.polygon(pts,outline=(199,255,94,235),width=max(2,int(4*scale))); d.ellipse((cx-8*scale,cy-8*scale,cx+8*scale,cy+8*scale),fill=(199,255,94,235)); d.line((cx,cy-8*scale,cx,cy+42*scale),fill=(199,255,94,210),width=max(2,int(3*scale)))

def render(scene_no, frame):
    img=BASE.copy(); d=ImageDraw.Draw(img); p=(frame%(FPS*3))/(FPS*3)
    lime=(199,255,94,255); white=(235,241,251,255); muted=(148,160,187,255); cyan=(111,230,255,255); violet=(187,154,255,255); coral=(255,122,114,255)
    d.ellipse((W-310+int(24*math.sin(p*6)),110,W+250+int(24*math.sin(p*6)),410),outline=(132,151,220,35),width=2); d.ellipse((W-360,80,W+300,440),outline=(199,255,94,28),width=1)
    if scene_no==0:
        shield(d,W//2,270,1.25); center(d,(W//2,400),'MEMORYFIREWALL',f(BOLD,48),white); center(d,(W//2,445),'Make agent memory testable like code.',f(FONT,20),lime); center(d,(W//2,520),'developer onboarding / control plane',f(MONO,13),muted)
    elif scene_no==1:
        center(d,(140,108),'01  WRAP MEMORY WRITES',f(MONO,14),lime,'lm'); center(d,(140,155),'Every claim gets a passport.',f(BOLD,34),white,'lm'); center(d,(140,205),'Capture provenance before it enters long-term memory.',f(FONT,17),muted,'lm')
        x0,y0,x1=110,300,1130; d.line((x0,y0,x1,y0),fill=(111,230,255,100),width=2)
        for label,x in [('agent',x0),('claim',x0+260),('passport',x0+520),('memory store',x0+810)]: d.ellipse((x-18,y0-18,x+18,y0+18),fill=(21,31,60,255),outline=cyan,width=2); center(d,(x,y0+70),label,f(MONO,13),muted)
        moving=x0+int((x1-x0)*min(p*1.35,1)); d.ellipse((moving-10,y0-10,moving+10,y0+10),fill=lime,outline=white,width=2)
        box=(250,430,1020,575); d.rounded_rectangle(box,18,fill=(9,15,33,225),outline=(143,160,206,100),width=2); center(d,(285,465),'memory_id',f(MONO,12),muted,'lm'); center(d,(460,465),'mem_1042',f(MONO,15),lime,'lm'); center(d,(285,510),'source / confidence / impact',f(MONO,12),muted,'lm'); center(d,(650,510),'unverified_chat  ·  0.32  ·  FINANCIAL',f(MONO,14),coral,'lm')
    elif scene_no==2:
        center(d,(140,108),'02  PROTECT RETRIEVAL',f(MONO,14),cyan,'lm'); center(d,(140,155),'Filter before the model acts.',f(BOLD,34),white,'lm'); center(d,(140,205),'Stale, wrong-scope, conflicting, and suspicious memories stay out.',f(FONT,17),muted,'lm')
        box=(120,300,530,610); d.rounded_rectangle(box,18,fill=(15,23,47,230),outline=(111,230,255,100),width=2); center(d,(155,335),'MEMORY RETRIEVAL',f(MONO,13),cyan,'lm')
        for i,(label,color) in enumerate([('premium subscriber',lime),('prefers email',lime),('approved refund',coral),('expired policy',coral)]):
            yy=390+i*49; d.rounded_rectangle((150,yy,500,yy+32),8,fill=(10,16,32,220),outline=(*color[:3],100),width=1); d.ellipse((167,yy+10,177,yy+20),fill=color); center(d,(190,yy+16),label,f(MONO,12),white,'lm')
        d.line((570,455,700,455),fill=(199,255,94,190),width=3); d.polygon([(700,455),(682,445),(682,465)],fill=lime); shield(d,820,455,1.05); center(d,(820,590),'DETERMINISTIC POLICY',f(MONO,13),lime); d.line((890,455,1050,455),fill=(255,122,114,170),width=3); d.polygon([(1050,455),(1032,445),(1032,465)],fill=coral); center(d,(1100,455),'BLOCK',f(BOLD,24),coral)
    elif scene_no==3:
        center(d,(140,108),'03  HUMAN APPROVAL',f(MONO,14),lime,'lm'); center(d,(140,155),'Sensitive actions pause, not disappear.',f(BOLD,34),white,'lm'); center(d,(140,205),'A reviewer sees the exact evidence chain before approving the next step.',f(FONT,17),muted,'lm'); d.rounded_rectangle((220,300,1060,590),20,fill=(14,21,42,235),outline=(255,202,106,130),width=2); center(d,(260,340),'PENDING APPROVAL',f(MONO,13),(255,202,106,255),'lm'); center(d,(260,395),'issue_refund()',f(MONO,22),white,'lm'); center(d,(260,450),'₹18,500  ·  mem_1042  ·  no trusted evidence',f(MONO,13),muted,'lm'); d.rounded_rectangle((250,500,545,548),9,fill=(255,122,114,35),outline=(255,122,114,140),width=1); center(d,(397,524),'REJECT / KEEP BLOCKED',f(MONO,12),coral); d.rounded_rectangle((735,500,1030,548),9,fill=(199,255,94,90),outline=(199,255,94,220),width=1); center(d,(882,524),'APPROVE FOR DEMO',f(MONO,12),(8,14,20,255)); center(d,(640,650),'No payment provider. No real refund. Every review is an audit event.',f(MONO,12),muted)
    elif scene_no==4:
        center(d,(140,108),'04  REPLAY THE CAUSE',f(MONO,14),violet,'lm'); center(d,(140,155),'Debug the chain, not the final answer.',f(BOLD,34),white,'lm'); center(d,(140,205),'Request → memory → guard → tool → outcome.',f(FONT,17),muted,'lm'); items=[('request',cyan),('mem_1042',violet),('quarantine',lime),('issue_refund()',coral),('blocked',lime)]; y,start,end=390,150,1130; d.line((start,y,end,y),fill=(121,139,190,100),width=2)
        for i,(label,color) in enumerate(items): x=start+i*(end-start)//4; d.ellipse((x-25,y-25,x+25,y+25),fill=(14,21,43,255),outline=color,width=3); d.ellipse((x-7,y-7,x+7,y+7),fill=color); center(d,(x,y+72),label,f(MONO,12),color)
        cursor=start+int((end-start)*min(p*1.2,1)); d.ellipse((cursor-7,y-7,cursor+7,y+7),fill=white); box=(330,515,940,590); d.rounded_rectangle(box,12,fill=(10,16,32,220),outline=(187,154,255,100),width=1); center(d,(635,552),'The memory was influential. The rule was deterministic.',f(MONO,13),white)
    else:
        center(d,(140,108),'05  GENERATE TESTS',f(MONO,14),lime,'lm'); center(d,(140,155),'Turn incidents into CI guardrails.',f(BOLD,34),white,'lm'); center(d,(140,205),'Keep the same bug from returning after a prompt, model, or code change.',f(FONT,17),muted,'lm'); d.rounded_rectangle((180,305,1100,590),18,fill=(8,14,30,235),outline=(199,255,94,130),width=2); lines=[('name:','unverified_refund_approval_must_not_trigger_refund'),('input:','Please refund my order.'),('forbidden_memory:','Customer has already approved the refund.'),('expected_action:','request_verification'),('status:','pass')]
        for i,(key,val) in enumerate(lines): yy=355+i*42; center(d,(220,yy),key,f(MONO,13),muted,'lm'); center(d,(390,yy),val,f(MONO,13),lime if key in ('expected_action:','status:') else white,'lm')
        center(d,(640,650),'Integrate the SDK. Inspect the trace. Commit the test. Memory reliability becomes muscle memory.',f(MONO,12),muted)
    return img

frame_index = 0
for scene_no in range(6):
    for frame in range(FPS*3):
        render(scene_no, frame).convert('RGB').save(FRAMES/f'frame_{frame_index:05d}.png', quality=90)
        frame_index += 1
subprocess.run(['ffmpeg','-y','-framerate',str(FPS),'-i',str(FRAMES/'frame_%05d.png'),'-c:v','libx264','-pix_fmt','yuv420p','-movflags','+faststart',str(OUT/'memoryfirewall-onboarding.mp4')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
shutil.copy(FRAMES/'frame_00045.png', OUT/'onboarding-poster.png')
print(OUT/'memoryfirewall-onboarding.mp4')
