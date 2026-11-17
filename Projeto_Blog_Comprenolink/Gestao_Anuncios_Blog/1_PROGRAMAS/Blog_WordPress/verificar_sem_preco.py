# -*- coding: utf-8 -*-
"""POLÍTICA DO BLOG (dono): os anúncios NÃO podem exibir preço no comprenolink.net.

Varre TODAS as páginas e posts do WordPress (somente leitura) atrás de:
  - texto com "R$ 123" (nome, título, selo, descrição, benefícios...)
  - caixas de preço dos cartões (…product-price) e campos price/preco no JSON dos blocos
Código de saída 0 = limpo; 1 = achou preço.

Uso:  python verificar_sem_preco.py             (só relata)
      python verificar_sem_preco.py --corrigir  (no GUIA: remove as caixas de preço dos cartões, com backup da
                                                 página; preço dentro de nome/texto você corrige com
                                                 gerenciar_blog.py editar N --nome "..." --aplicar)
As páginas de categoria são geradas do guia (atualizar_categorias_auto.py, a cada 3 h): corrigido o guia, elas
se corrigem sozinhas na próxima geração (ou rode publicar_categorias.py).
"""
import html
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerenciar_blog as gb  # noqa: E402

RE_PRECO = re.compile(r"R\$\s*\d[\d.,]*")
RE_DIV_PRECO = re.compile(r'<div class="[^"]*product-price[^"]*">.*?</div>', re.S)
RE_PROIBIDO = re.compile(r"mais vendid|olha o que eu encontrei|melhor pre|menor pre|melhor|(?<!mercado)l[ií]der|oferta do m[eê]s|"
                         r"garantido|uso di[aá]rio\.?$", re.I)
RE_JSON_PRECO = re.compile(r'"(?:price|preco|preço)"\s*:\s*"?\d')


def conteudos(cfg):
    for tipo in ("pages", "posts"):
        pg = 1
        while True:
            try:
                lote = gb.requisitar(cfg, "GET", f"/wp-json/wp/v2/{tipo}?per_page=100&page={pg}&context=edit&status=any")
            except gb.Erro:
                break
            if not lote:
                break
            for x in lote:
                yield tipo, x
            if len(lote) < 100:
                break
            pg += 1


def main():
    corrigir = "--corrigir" in sys.argv
    cfg = gb.carregar_config()
    achou = 0
    for tipo, x in conteudos(cfg):
        c = x["content"].get("raw", "")
        txt = html.unescape(re.sub(r"<[^>]+>", " ", c))
        textos = RE_PRECO.findall(txt)
        divs = len(RE_DIV_PRECO.findall(c))
        jsons = len(RE_JSON_PRECO.findall(c))
        if textos or divs or jsons:
            achou += 1
            print(f"{tipo[:-1]} {x['id']} '{x['title'].get('raw', '')[:50]}': texto R$={len(textos)} {textos[:4]} "
                  f"| caixas de preço={divs} | json preço={jsons}")
    # política de texto dos cartões do guia (selo, descrição, benefícios, ideal para)
    fora = []
    for i in gb.itens(gb.baixar_pagina(cfg).conteudo):
        for campo in ("nome", "selo", "desc", "beneficios", "ideal"):
            v = i[campo]
            v = " | ".join(v) if isinstance(v, list) else v
            m = RE_PROIBIDO.search(v or "")
            if m:
                fora.append((i["n"], campo, m.group(0)))
    for n, campo, trecho in fora:
        print(f"FORA DA POLÍTICA: item {n}, campo {campo}: {trecho!r} (selo/texto precisa ser reescrito)")
    if not achou and not fora:
        print("OK: nenhum preço em páginas/posts e textos dos cartões dentro da política.")
        return 0
    if not achou:
        return 1
    if corrigir:
        p = gb.baixar_pagina(cfg)
        novo, n = RE_DIV_PRECO.subn("", p.conteudo)
        if n:
            print(f"Guia: removendo {n} caixa(s) de preço (backup antes de publicar).")
            gb.publicar(cfg, p, novo, p.titulo)
        else:
            print("Guia: nenhuma caixa de preço para remover.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
