# -*- coding: utf-8 -*-
"""
Catálogo do WhatsApp Business POR CATEGORIA (um item por categoria do blog, link para a página da categoria).
Gera 06_CATALOGO_WHATSAPP\\CATEGORIAS\\: fotos\\CAT-<slug>.jpg (1º produto da categoria), CATALOGO_CATEGORIAS.xlsx
e CATALOGO_CATEGORIAS_TEXTOS.txt. Categoria nova no blog = só 1 item novo para cadastrar no WhatsApp.
Rodar:  python -X utf8 _fonte\\gerar_catalogo_categorias.py   (depois: _fonte\\sincronizar_copias.py)
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dados_divulgacao as dd  # noqa: E402
from gerar_artes_catalogo import cartao_foto, foto  # noqa: E402

PASTA = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "06_CATALOGO_WHATSAPP", "CATEGORIAS")


def main():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    dados = dd.carrega_produtos()
    os.makedirs(os.path.join(PASTA, "fotos"), exist_ok=True)
    minimo = dados["arvore"].get("minimo_para_publicar", 3)
    linhas = []
    for cat in dados["arvore"]["categorias"]:
        xs = [x for x in dados["itens"] if x.get("cat") is cat]
        if len(xs) < minimo:
            continue  # sem página própria no blog ainda
        c, _ = cartao_foto(foto(xs[0]), 1080)
        arq = f"CAT-{cat['slug']}.jpg"
        c.save(os.path.join(PASTA, "fotos", arq), quality=90)
        chamada = (cat.get("chamada") or cat["intro"]).rstrip(".")
        desc = (f"{chamada[0].upper() + chamada[1:]}. Confira todas as opções da categoria com o valor do dia no Mercado Livre "
                "pelo link. Link de afiliado: posso ganhar comissão, sem custo extra para você.")
        link = dd.utm(f"{dd.SITE}/{cat['slug']}/", "whatsapp", "catalogo", "categoria", f"cat_{cat['slug']}")
        linhas.append([f"CAT-{cat['slug']}", f"{cat['emoji']} {cat['nome']}", "(deixe em branco)", desc, link, arq, len(xs)])
    wb = Workbook()
    ws = wb.active
    ws.title = "Categorias"
    ws.append(["Código do item", "Nome do item", "Preço", "Descrição", "Link do site", "Foto (pasta fotos)", "Produtos hoje", "Cadastrado (S/N)"])
    for l in linhas:
        ws.append(l + ["N"])
    for c in ws[1]:
        c.fill, c.font = PatternFill("solid", fgColor="111827"), Font(bold=True, color="FFFFFF")
    for i, w in enumerate([30, 30, 16, 70, 70, 36, 12, 14], 1):
        ws.column_dimensions[chr(64 + i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    wb.save(os.path.join(PASTA, "CATALOGO_CATEGORIAS.xlsx"))
    txt = ["TEXTOS DO CATÁLOGO POR CATEGORIA – WhatsApp Business (copiar e colar no celular)",
           f"São {len(linhas)} itens fixos: um por categoria do blog. Cadastre uma vez só — quando o blog",
           "ganhar novos anúncios, não precisa voltar aqui, o link da categoria já mostra tudo.",
           "Categoria nova no blog = cadastrar só o item novo.",
           "Para cada categoria: Adicionar novo item → foto (pasta fotos) → NOME → Preço EM BRANCO",
           "→ DESCRIÇÃO → Mais campos: LINK e CÓDIGO.", ""]
    for cod, nome, _, desc, link, arq, n in linhas:
        txt += ["=" * 60, f"CÓDIGO: {cod}      FOTO: {arq}      PRODUTOS HOJE: {n}", "=" * 60,
                "NOME:", nome, "", "DESCRIÇÃO:", desc, "", "LINK:", link, ""]
    with open(os.path.join(PASTA, "CATALOGO_CATEGORIAS_TEXTOS.txt"), "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write("\n".join(txt))
    print(f"{len(linhas)} categorias:", ", ".join(l[0] for l in linhas))


if __name__ == "__main__":
    main()
