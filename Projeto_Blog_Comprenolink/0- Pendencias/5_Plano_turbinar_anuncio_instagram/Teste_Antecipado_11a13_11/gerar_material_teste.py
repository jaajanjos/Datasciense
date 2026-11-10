import re, sys, os
from PIL import Image, ImageDraw, ImageFont
sys.stdout.reconfigure(encoding="utf-8")
PASTA = os.path.dirname(os.path.abspath(__file__))
LOGO = r"D:\Projeto_Blog_Comprenolink\Logo\logo_horizontal.png"
AM, AZ, BR, CZ = (255,230,0),(45,50,119),(255,255,255),(225,228,240)
F = r"C:\Windows\Fonts"
def f(t, b=True): return ImageFont.truetype(os.path.join(F,"segoeuib.ttf" if b else "segoeui.ttf"), t)
def quebrar(d, txt, fn, larg):
    ls, cur = [], ""
    for p in txt.split():
        t = (cur+" "+p).strip()
        if d.textlength(t, font=fn) <= larg: cur = t
        else: ls.append(cur); cur = p
    return ls+[cur]
def arte(w, h, nome, titulo, sub, cta):
    im = Image.new("RGB",(w,h),AZ); d = ImageDraw.Draw(im)
    d.rectangle([0,0,w,18],fill=AM); d.rectangle([0,h-18,w,h],fill=AM)
    m="compre no link"; d.text(((w-d.textlength(m,font=f(78)))//2,int(h*0.07)),m,font=f(78),fill=AM)
    u="comprenolink.net"; d.text(((w-d.textlength(u,font=f(38,False)))//2,int(h*0.07)+100),u,font=f(38,False),fill=CZ)
    y = int(h*0.30)
    for l in quebrar(d,titulo,f(88),w-160):
        d.text(((w-d.textlength(l,font=f(88)))//2,y),l,font=f(88),fill=BR); y+=110
    y+=30
    for l in quebrar(d,sub,f(46,False),w-200):
        d.text(((w-d.textlength(l,font=f(46,False)))//2,y),l,font=f(46,False),fill=CZ); y+=64
    bw,bh = 640,120; by = int(h*0.74)
    d.rounded_rectangle([(w-bw)//2,by,(w+bw)//2,by+bh],radius=60,fill=AM)
    d.text(((w-d.textlength(cta,font=f(54)))//2,by+28),cta,font=f(54),fill=AZ)
    av = "Publicidade · Link de afiliado"
    d.text(((w-d.textlength(av,font=f(32,False)))//2,h-120),av,font=f(32,False),fill=CZ)
    im.save(os.path.join(PASTA,nome)); print("ok",nome,im.size)
T = "Tecnologia sem complicação"
S = "Fones, caixas de som, TVs e acessórios organizados por categoria para você comparar com calma."
arte(1080,1350,"anuncio_1080x1350.png",T,S,"Veja no site")
arte(1080,1920,"anuncio_1080x1920.png",T,S,"Veja no site")
