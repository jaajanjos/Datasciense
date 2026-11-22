# -*- coding: utf-8 -*-
"""Criativo novo (PROPOSTA, 21/11/2026) para o anuncio bf_26_entrada_v1: a imagem atual sai CORTADA no feed
("compre no li..."). Esta versao deixa a marca INTEIRA, centralizada e com margem segura nas bordas, em 3 formatos:
  1080x1350 (4:5)  feed do Instagram e do Facebook
  1080x1920 (9:16) Stories e Reels
  1080x1080 (1:1)  quadrado (feed/Facebook/outros)
Mesmo texto do criativo atual: marca + "comprenolink.net  •  achados do Mercado Livre".
NAO publica nada: so gera os PNG nesta pasta. Trocar no anuncio so com o 'sim' do dono (e da conversa Execucao).
Uso:  python -X utf8 gerar_criativo_v2.py
"""
import os
import sys

FONTE = r"D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Divugação_WhastsApp_Instagram\_fonte"
sys.path.insert(0, FONTE)
from PIL import Image, ImageDraw  # noqa: E402
from gerar_logo import BRANCO, CINZA, ESCURO, AMARELO, fonte, horizontal  # noqa: E402

AQUI = os.path.dirname(os.path.abspath(__file__))
FORMATOS = {"1080x1350": (1080, 1350), "1080x1920": (1080, 1920), "1080x1080": (1080, 1080), "1200x628": (1200, 628)}


def criativo_horizontal(w, h):
    """1,91:1 (feed horizontal/coluna direita do Facebook): marca a esquerda, botao a direita, margem segura."""
    img = Image.new("RGB", (w, h), ESCURO)
    d = ImageDraw.Draw(img)
    mx, my = int(w * 0.07), int(h * 0.12)
    logo = horizontal(ESCURO, BRANCO, CINZA)
    lw = int(w * 0.52)
    lh = int(lw * logo.height / logo.width)
    img.paste(logo.resize((lw, lh), Image.LANCZOS), (mx, h // 2 - lh // 2 - int(h * 0.04)))
    bx0 = mx + lw + int(w * 0.05)
    bw, bh = w - mx - bx0, int(h * 0.26)
    by = h // 2 - bh // 2 - int(h * 0.04)
    d.rounded_rectangle([bx0, by, bx0 + bw, by + bh], radius=bh // 2, fill=AMARELO)
    d.text((bx0 + bw / 2, by + bh / 2), "Veja no site", font=fonte("arialbd.ttf", int(h * 0.09)), fill=ESCURO, anchor="mm")
    d.text((w / 2, h - my), "Publicidade · Link de afiliado", font=fonte("arial.ttf", int(h * 0.05)), fill=CINZA, anchor="mm")
    return img


def criativo(w, h):
    if w / h > 1.5:
        return criativo_horizontal(w, h)
    img = Image.new("RGB", (w, h), ESCURO)
    d = ImageDraw.Draw(img)
    seguro = int(w * 0.14)                       # margem segura: nada importante encostado na borda
    larg = w - 2 * seguro                        # largura util da marca
    logo = horizontal(ESCURO, BRANCO, CINZA)
    alt = int(larg * logo.height / logo.width)
    logo = logo.resize((larg, alt), Image.LANCZOS)
    # a marca ja traz "comprenolink.net - achados do Mercado Livre" dentro dela: sem texto repetido
    y_logo = int(h * 0.36) - alt // 2
    img.paste(logo, (seguro, y_logo))
    # botao: sempre abaixo da marca e com folga ate o rodape
    y_bot = int(h * 0.62)
    alt_bot = int(w * 0.15)
    d.rounded_rectangle([seguro, y_bot, w - seguro, y_bot + alt_bot], radius=alt_bot // 2, fill=AMARELO)
    d.text((w / 2, y_bot + alt_bot / 2), "Veja no site", font=fonte("arialbd.ttf", int(w * 0.058)), fill=ESCURO, anchor="mm")
    d.text((w / 2, int(h * 0.86)), "Publicidade · Link de afiliado", font=fonte("arial.ttf", int(w * 0.032)), fill=CINZA, anchor="mm")
    return img


def main():
    for nome, (w, h) in FORMATOS.items():
        arq = os.path.join(AQUI, f"criativo_v2_{nome}.png")
        criativo(w, h).save(arq)
        print(arq)


if __name__ == "__main__":
    main()
