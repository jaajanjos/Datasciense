# -*- coding: utf-8 -*-
"""Reels do NOVO BLOG (25/11/2026): estilo LIMPO (fundo claro, cartao branco, botao amarelo), sem 'Comente X',
com a linha de confianca. Grava em REELS_NOVO_BLOG\\<subpasta>. Legenda termina SO com comprenolink.net (sem hashtag).
Uso:  python -X utf8 _fonte\\gerar_reels_novo.py 01_AMOSTRA 1          (subpasta, item do guia)
"""
import io
import os
import re
import sys
import tempfile
import urllib.request

from PIL import Image, ImageDraw

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dados_divulgacao as dd  # noqa: E402
import gerar_reels as gr  # noqa: E402
from gerar_logo import ESCURO, AMARELO, fonte, horizontal  # noqa: E402

W, H = gr.W, gr.H
RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "REELS_NOVO_BLOG")
FUNDO, CARTAO, TEXTO, SUAVE, BORDA = (244, 245, 247), (255, 255, 255), (31, 41, 55), (107, 114, 128), (229, 231, 235)
LINHA_CONFIANCA = "Você compra direto no site oficial do Mercado Livre. O CompreNoLink só indica os produtos."


def foto(x):
    req = urllib.request.Request(x["imagem"], headers={"User-Agent": "Mozilla/5.0"})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert("RGBA")
    fundo = Image.new("RGBA", im.size, (255, 255, 255, 255))
    return Image.alpha_composite(fundo, im).convert("RGB")


def topo(img):
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 190], fill=CARTAO)
    d.line([0, 190, W, 190], fill=BORDA, width=3)
    logo = horizontal(CARTAO, ESCURO, SUAVE).resize((560, 168), Image.LANCZOS)
    img.paste(logo, (60, 12))
    return d


def cena1(x, im):
    img = Image.new("RGB", (W, H), FUNDO)
    d = topo(img)
    d.rounded_rectangle([60, 260, W - 60, 1420], radius=40, fill=CARTAO, outline=BORDA, width=3)
    lado = 820
    f = im.copy()
    f.thumbnail((lado, lado), Image.LANCZOS)
    img.paste(f, ((W - f.width) // 2, 300 + (lado - f.height) // 2))
    y = gr.texto_centro(d, 1150, x["nome"], fonte("arialbd.ttf", 64), TEXTO, larg=W - 220)
    d.rounded_rectangle([W // 2 - 220, y + 20, W // 2 + 220, y + 90], radius=35, fill=(255, 244, 191))
    d.text((W // 2, y + 55), x["selo"], font=fonte("arialbd.ttf", 34), fill=TEXTO, anchor="mm")
    d.rounded_rectangle([170, 1530, W - 170, 1690], radius=80, fill=AMARELO)
    d.text((W / 2, 1610), "Veja no Mercado Livre", font=fonte("arialbd.ttf", 60), fill=ESCURO, anchor="mm")
    return img


def cena2(x, im):
    img = Image.new("RGB", (W, H), FUNDO)
    d = topo(img)
    d.text((W / 2, 330), "Por que olhar", font=fonte("arial.ttf", 48), fill=SUAVE, anchor="mm")
    y = gr.texto_centro(d, 380, x["nome"], fonte("arialbd.ttf", 62), TEXTO, larg=W - 200) + 50
    for b in x["beneficios"][:4]:
        d.rounded_rectangle([70, y, W - 70, y + 190], radius=34, fill=CARTAO, outline=BORDA, width=3)
        d.ellipse([110, y + 60, 180, y + 130], fill=AMARELO)
        d.text((145, y + 95), "✓", font=fonte("seguisym.ttf", 44), fill=ESCURO, anchor="mm")
        fnt = fonte("arialbd.ttf", 46)
        while d.textlength(b, font=fnt) > W - 330 and fnt.size > 30:
            fnt = fonte("arialbd.ttf", fnt.size - 2)
        d.text((215, y + 95), b, font=fnt, fill=TEXTO, anchor="lm")
        y += 220
    return img


def cena3():
    img = Image.new("RGB", (W, H), FUNDO)
    d = topo(img)
    d.rounded_rectangle([60, 330, W - 60, 1500], radius=40, fill=CARTAO, outline=BORDA, width=3)
    d.text((W / 2, 520), "Quer ver o produto?", font=fonte("arialbd.ttf", 76), fill=TEXTO, anchor="mm")
    d.rounded_rectangle([140, 640, W - 140, 840], radius=100, fill=AMARELO)
    d.text((W / 2, 740), "Link na bio", font=fonte("arialbd.ttf", 80), fill=ESCURO, anchor="mm")
    d.text((W / 2, 930), "e confira direto no Mercado Livre", font=fonte("arial.ttf", 46), fill=TEXTO, anchor="mm")
    d.line([140, 1030, W - 140, 1030], fill=BORDA, width=3)
    gr.texto_centro(d, 1090, LINHA_CONFIANCA, fonte("arial.ttf", 44), SUAVE, larg=W - 260)
    d.text((W / 2, 1780), "Link de afiliado: posso ganhar comissão, sem custo extra para você.",
           font=fonte("arial.ttf", 30), fill=SUAVE, anchor="mm")
    return img


def legenda(x):
    bens = "\n".join(f"✅ {b}" for b in x["beneficios"][:4])
    return (f"{x['nome']}\n\n{x['desc']}\n\n{bens}\n\n"
            f"👉 Link na bio para ver o produto.\n\n{dd.AVISO}\n\ncomprenolink.net")


TROCAS = (("perfeito para o café da manhã e a dieta", "prático para o café da manhã"),
          ("Ótimo para", "Bom para"), ("Ótima opção", "Boa opção"), ("ideal para", "bom para"))


def limpa(x):
    """Termos simples e seguros pela politica do blog (sem superlativo, sem promessa)."""
    def t(s):
        for a, b in TROCAS:
            s = s.replace(a, b)
        return s
    x = dict(x)
    x["desc"] = t(x["desc"])
    x["beneficios"] = [t(b) for b in x["beneficios"]]
    return x


def gera(sub, n, prefixo=""):
    dados = dd.carrega_produtos()
    x = limpa(next(i for i in dados["itens"] if i["n"] == n))
    pasta = os.path.join(DESTINO, sub, f"{prefixo}item{n}_{dd.slug(x['nome'])[:24]}")
    os.makedirs(pasta, exist_ok=True)
    im = foto(x)
    c1 = cena1(x, im)
    gr.video([c1, cena2(x, im), cena3()], os.path.join(pasta, "reels.mp4"))
    c1.save(os.path.join(pasta, "reels_capa.jpg"), quality=90)
    with open(os.path.join(pasta, "2_LEGENDA_REELS.txt"), "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(f"REEL item {n} do guia: {x['nome']}\n" + "=" * 40 + "\n" + legenda(x) + "\n")
    return pasta


if __name__ == "__main__":
    print(gera(sys.argv[1], int(sys.argv[2])))
