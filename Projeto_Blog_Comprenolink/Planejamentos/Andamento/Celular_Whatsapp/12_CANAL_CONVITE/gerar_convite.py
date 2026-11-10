# -*- coding: utf-8 -*-
from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1920
img = Image.new("RGB", (W, H), (11, 61, 46))
d = ImageDraw.Draw(img)
for y in range(H):
    k = y / H
    d.line([(0, y), (W, y)], fill=(int(11 + 14 * k), int(61 + 50 * k), int(46 + 24 * k)))
F = "C:/Windows/Fonts/seguibl.ttf"; FB = "C:/Windows/Fonts/segoeuib.ttf"
def txt(y, s, f, cor=(255, 255, 255)):
    w = d.textlength(s, font=f)
    d.text(((W - w) / 2, y), s, font=f, fill=cor)
d.ellipse([W/2-150, 330, W/2+150, 630], fill=(37, 211, 102))
txt(440, "💬"[0:0] + "WA", ImageFont.truetype(F, 120), (255, 255, 255))
txt(720, "Entre no nosso", ImageFont.truetype(F, 84))
txt(830, "Canal do WhatsApp", ImageFont.truetype(F, 92), (37, 211, 102))
txt(1020, "Receba os achados do dia", ImageFont.truetype(FB, 62))
txt(1105, "direto no seu celular", ImageFont.truetype(FB, 62))
d.rounded_rectangle([140, 1290, W-140, 1500], 40, fill=(37, 211, 102))
txt(1330, "Toque no link abaixo", ImageFont.truetype(F, 50), (11, 61, 46))
txt(1410, "e entre no Canal", ImageFont.truetype(FB, 52), (11, 61, 46))
txt(1650, "comprenolink.net", ImageFont.truetype(FB, 48), (210, 230, 220))
txt(1730, "Link de afiliado: posso receber comissão, sem custo para você.", ImageFont.truetype(FB, 30), (190, 215, 205))
img.save("convite_canal_status.png")
print("ok")
