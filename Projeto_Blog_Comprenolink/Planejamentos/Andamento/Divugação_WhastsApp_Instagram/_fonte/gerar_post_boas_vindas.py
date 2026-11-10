# -*- coding: utf-8 -*-
"""Post fixado de boas-vindas do Instagram (1080x1350) + legenda. Gera em 10_POST_BOAS_VINDAS\\.
As categorias vêm do categorias.json do blog (categoria nova = rodar de novo e trocar a imagem do post fixado).
Rodar:  python -X utf8 _fonte\\gerar_post_boas_vindas.py
"""
import json
import os

from PIL import Image, ImageDraw

from gerar_logo import AMARELO, BRANCO, CINZA, ESCURO, K, fonte, horizontal

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, "10_POST_BOAS_VINDAS")
ARVORE = r"D:\Projeto_Blog_Comprenolink\Gestao_Anuncios_Blog\2_DADOS\Blog_WordPress\categorias.json"
CARTAO = (31, 41, 55)


def categorias():
    with open(ARVORE, encoding="utf-8") as f:
        return [c["nome"] for c in json.load(f)["categorias"]]


def imagem(cats):
    W, H = 1080 * K, 1350 * K
    img = Image.new("RGB", (W, H), ESCURO)
    d = ImageDraw.Draw(img)
    logo = horizontal(ESCURO, BRANCO, CINZA).resize((int(W * .80), int(W * .80 * 480 / 1600)), Image.LANCZOS)
    img.paste(logo, (int(W * .10), int(H * .035)))
    y = H * .255
    d.text((W / 2, y), "Bem-vindo ao Compre no Link!", font=fonte("arialbd.ttf", int(W * .062)), fill=AMARELO, anchor="mm")
    y += H * .055
    for linha in ("Os mais vendidos e bem avaliados do Mercado Livre,", "organizados por categoria para você escolher."):
        d.text((W / 2, y), linha, font=fonte("arial.ttf", int(W * .036)), fill=BRANCO, anchor="mm")
        y += H * .033
    # categorias em 2 colunas
    y += H * .025
    d.text((W * .08, y), "CATEGORIAS NO BLOG", font=fonte("arialbd.ttf", int(W * .032)), fill=CINZA, anchor="lm")
    y += H * .035
    lin = (len(cats) + 1) // 2
    alt = H * (.048 if lin <= 4 else .040)  # 9+ categorias: cartões mais baixos para caber
    gap = H * (.011 if lin <= 4 else .008)
    # um tamanho só para todas, o maior que faz o nome mais comprido caber no cartão
    tam = int(W * .031)
    while max(d.textlength(n, font=fonte("arialbd.ttf", tam)) for n in cats) > W * .33:
        tam -= K
    for i, nome in enumerate(cats):
        col, row = divmod(i, lin)
        x0, y0 = W * (.08 + col * .43), y + row * (alt + gap)
        d.rounded_rectangle([x0, y0, x0 + W * .41, y0 + alt], radius=alt * .3, fill=CARTAO)
        d.ellipse([x0 + W * .025, y0 + alt / 2 - W * .009, x0 + W * .043, y0 + alt / 2 + W * .009], fill=AMARELO)
        d.text((x0 + W * .06, y0 + alt / 2), nome, font=fonte("arialbd.ttf", tam), fill=BRANCO, anchor="lm")
    y += lin * (alt + gap) + H * .02
    # como funciona
    d.text((W * .08, y), "COMO FUNCIONA", font=fonte("arialbd.ttf", int(W * .032)), fill=CINZA, anchor="lm")
    y += H * .04
    passos = ("Toque no link da bio e veja os detalhes no blog",
              "Confira o valor do dia direto no Mercado Livre",
              "Quer um link? Comente ou chame no Direct")
    for n, p in enumerate(passos, 1):
        r = W * .028
        d.ellipse([W * .08, y - r, W * .08 + 2 * r, y + r], fill=AMARELO)
        d.text((W * .08 + r, y), str(n), font=fonte("arialbd.ttf", int(W * .032)), fill=ESCURO, anchor="mm")
        d.text((W * .155, y), p, font=fonte("arial.ttf", int(W * .033)), fill=BRANCO, anchor="lm")
        y += H * .048
    # rodapé (abaixo do último passo)
    y0 = max(H * .865, y - H * .01)
    assert y0 + H * .075 < H * .95, "arte sem espaço: diminua os espaçamentos"
    d.rounded_rectangle([W * .08, y0, W * .92, y0 + H * .075], radius=H * .0375, fill=AMARELO)
    d.text((W / 2, y0 + H * .0375), "LINK NA BIO  •  comprenolink.net", font=fonte("arialbd.ttf", int(W * .042)), fill=ESCURO, anchor="mm")
    d.text((W / 2, H * .97), "Link de afiliado: posso ganhar comissão, sem custo extra para você.",
           font=fonte("arial.ttf", int(W * .024)), fill=CINZA, anchor="mm")
    return img.resize((1080, 1350), Image.LANCZOS)


def legenda(cats):
    return "\n".join([
        "👋 Bem-vindo ao Compre no Link!",
        "",
        "Aqui eu reúno os produtos mais vendidos e bem avaliados do Mercado Livre e organizo tudo por categoria no blog comprenolink.net, para você escolher sem perder tempo.",
        "",
        "📂 Categorias: " + ", ".join(cats) + ".",
        "",
        "🔥 Em novembro: Top 10 da Black Friday.",
        "🎄 Em dezembro: presentes de Natal.",
        "",
        "👉 Toque no link da bio, veja os detalhes e confira o valor do dia direto no Mercado Livre.",
        "💬 Quer o link de algum produto? Comente aqui ou chame no WhatsApp (11) 99495-9657.",
        "",
        "Publi: contém link de afiliado. Posso ganhar uma comissão, sem custo extra para você. Preços e estoque podem mudar no Mercado Livre.",
        "",
        "#achadosmercadolivre #mercadolivre #achadinhos #blackfriday #ofertas",
    ])


if __name__ == "__main__":
    os.makedirs(PASTA, exist_ok=True)
    cats = categorias()
    imagem(cats).save(os.path.join(PASTA, "post_boas_vindas.png"))
    with open(os.path.join(PASTA, "legenda_boas_vindas.txt"), "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(legenda(cats))
    print(len(cats), "categorias ->", PASTA)
