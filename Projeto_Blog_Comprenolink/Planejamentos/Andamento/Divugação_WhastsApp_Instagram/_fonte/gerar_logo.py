# -*- coding: utf-8 -*-
"""Logotipo do comprenolink (carrinho + elos de corrente). Gera em 09_LOGO\\:
  logo_perfil_1080.png  (quadrado, cabe no círculo do WhatsApp/Instagram)
  logo_horizontal.png   (fundo escuro, para capas e artes)
  logo_horizontal_fundo_branco.png
  logo_icone_512.png    (só o símbolo)
"""
import os
from PIL import Image, ImageDraw, ImageFont

PASTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "09_LOGO")
F = r"C:\Windows\Fonts"
ESCURO, AMARELO, BRANCO, CINZA = (17, 24, 39), (255, 213, 74), (255, 255, 255), (148, 163, 184)
K = 4  # desenha 4x maior e reduz (bordas suaves)


def simbolo(d, cx, cy, s, cor, cor_elo):
    """Carrinho de compras com dois elos de corrente dentro da cesta. s = largura total."""
    w = max(2, int(s * 0.055))
    # alça
    d.line([(cx - s * .50, cy - s * .36), (cx - s * .36, cy - s * .36), (cx - s * .26, cy - s * .24)], fill=cor, width=w, joint="curve")
    # cesta (trapézio arredondado)
    cesta = [(cx - s * .30, cy - s * .24), (cx + s * .48, cy - s * .24), (cx + s * .36, cy + s * .14), (cx - s * .20, cy + s * .14)]
    d.line(cesta + [cesta[0]], fill=cor, width=w, joint="curve")
    # base e rodas
    d.line([(cx - s * .20, cy + s * .14), (cx - s * .16, cy + s * .26), (cx + s * .38, cy + s * .26)], fill=cor, width=w, joint="curve")
    r = s * .065
    for x in (cx - s * .08, cx + s * .30):
        d.ellipse([x - r, cy + s * .38 - r, x + r, cy + s * .38 + r], fill=cor)
    # dois elos (link) dentro da cesta
    ew, eh, we = s * .25, s * .15, max(2, int(s * .045))
    for dx, dy in ((-s * .05, -s * .07), (s * .14, -s * .02)):
        x0, y0 = cx + dx - ew / 2, cy + dy - eh / 2
        d.rounded_rectangle([x0, y0, x0 + ew, y0 + eh], radius=eh / 2, outline=cor_elo, width=we)


def fonte(nome, tam):
    return ImageFont.truetype(os.path.join(F, nome), tam)


def perfil():
    L = 1080 * K
    img = Image.new("RGB", (L, L), ESCURO)
    d = ImageDraw.Draw(img)
    d.ellipse([L * .07, L * .07, L * .93, L * .93], outline=AMARELO, width=int(L * .018))
    simbolo(d, L * .5, L * .40, L * .46, AMARELO, BRANCO)
    d.text((L * .5, L * .68), "compre no link", font=fonte("arialbd.ttf", int(L * .085)), fill=BRANCO, anchor="mm")
    d.text((L * .5, L * .775), "achados do Mercado Livre", font=fonte("arial.ttf", int(L * .042)), fill=AMARELO, anchor="mm")
    return img.resize((1080, 1080), Image.LANCZOS)


def horizontal(fundo, cor_texto, cor_sub):
    W, H = 1600 * K, 480 * K
    img = Image.new("RGB", (W, H), fundo)
    d = ImageDraw.Draw(img)
    caixa = (ESCURO if fundo == BRANCO else fundo)
    d.rounded_rectangle([H * .12, H * .12, H * .88, H * .88], radius=H * .16, fill=caixa)
    simbolo(d, H * .5, H * .5, H * .58, AMARELO, BRANCO)
    d.text((H * 1.02, H * .44), "compre no link", font=fonte("arialbd.ttf", int(H * .26)), fill=cor_texto, anchor="lm")
    d.text((H * 1.04, H * .72), "comprenolink.net  •  achados do Mercado Livre", font=fonte("arial.ttf", int(H * .085)), fill=cor_sub, anchor="lm")
    return img.resize((1600, 480), Image.LANCZOS)


def icone():
    L = 512 * K
    img = Image.new("RGBA", (L, L), (0, 0, 0, 0))
    d = ImageDraw.Draw(img)
    d.rounded_rectangle([0, 0, L, L], radius=L * .22, fill=ESCURO + (255,))
    simbolo(d, L * .5, L * .5, L * .66, AMARELO, BRANCO)
    return img.resize((512, 512), Image.LANCZOS)


if __name__ == "__main__":
    os.makedirs(PASTA, exist_ok=True)
    perfil().save(os.path.join(PASTA, "logo_perfil_1080.png"))
    horizontal(ESCURO, BRANCO, AMARELO).save(os.path.join(PASTA, "logo_horizontal.png"))
    horizontal(BRANCO, ESCURO, (71, 85, 105)).save(os.path.join(PASTA, "logo_horizontal_fundo_branco.png"))
    icone().save(os.path.join(PASTA, "logo_icone_512.png"))
    print("ok", PASTA)
