#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
ESBOÇO LOCAL da nova arquitetura de categorias do blog (NÃO publica nada: só lê o guia).

Lê os produtos do guia (página 5), aplica a árvore e as tags de 2_DADOS\\Blog_WordPress\\categorias.json
e gera em 5_ESBOCO_CATEGORIAS\\:
  index.html .................... simulação da Início com o menu "Categorias"
  categoria-<slug>.html ......... uma página (hub) por Categoria Pai, com subcategorias e cartões
  tag-<tag>.html ................ páginas de tags sazonais (ex.: tag-black-friday.html)
  escolha-rapida.html ........... tabela "o melhor de cada subcategoria" na nova árvore
  matriz_mapeamento.csv/.html ... Matriz de Mapeamento (produto -> Pai -> Sub -> tags -> destino)
  RELATORIO.txt ................. resumo, categorias fracas (poucos itens), regra dos 3 cliques
Uso: python gerar_esboco_categorias.py
"""
import csv
import html
import json
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerenciar_blog as gb  # noqa: E402
from gerar_categorias import nome_curto  # noqa: E402

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
SAIDA = os.path.join(RAIZ, "5_ESBOCO_CATEGORIAS")
ARQ_CATEGORIAS = os.path.join(gb.PASTA_DADOS, "categorias.json")
SITE = "https://comprenolink.net"
GUIA = SITE + "/melhores-produtos-mercado-livre-2026/"
e = lambda t: html.escape(str(t or ""), quote=True)

CSS = """
:root{--azul:#0B5FA5;--tinta:#1a2230;--cinza:#5b6474;--borda:#e3e6ea;--fundo:#f5f6f7;--amarelo:#ffe600}
*{box-sizing:border-box}body{margin:0;font-family:"Segoe UI",system-ui,sans-serif;color:var(--tinta);background:var(--fundo);line-height:1.55}
.faixa{background:#fff3cd;border-bottom:1px solid #f1d27a;padding:8px 16px;font-size:13px;text-align:center}
header{background:#fff;border-bottom:3px solid var(--amarelo)}
.topo{max-width:1080px;margin:auto;padding:12px 16px;display:flex;flex-wrap:wrap;gap:12px;align-items:center;justify-content:space-between}
.logo{font-weight:800;font-size:20px;color:var(--tinta);text-decoration:none}
nav ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:4px 14px}
nav a{color:var(--tinta);text-decoration:none;font-weight:600;font-size:14px}
nav li.menu{position:relative}nav li.menu>ul{display:none;position:absolute;background:#fff;border:1px solid var(--borda);border-radius:8px;padding:8px;min-width:240px;z-index:5;flex-direction:column}
nav li.menu:hover>ul,nav li.menu:focus-within>ul{display:flex}
main{max-width:1080px;margin:auto;padding:20px 16px 48px}
.migalhas{font-size:13px;color:var(--cinza);margin-bottom:8px}.migalhas a{color:var(--azul)}
h1{font-size:28px;margin:.2em 0}.intro{font-size:17px;color:var(--cinza);max-width:760px}
h2{font-size:21px;margin:28px 0 12px;padding-top:8px;border-top:1px solid var(--borda)}
.grade{display:grid;grid-template-columns:repeat(auto-fill,minmax(230px,1fr));gap:14px}
.card{background:#fff;border:1px solid var(--borda);border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:6px}
.card img{width:100%;height:150px;object-fit:contain}
.card h3{font-size:15px;margin:0}.selo{font-size:12px;font-weight:700;color:#8a5a00;background:#fff4d6;border-radius:999px;padding:2px 8px;align-self:flex-start}
.card p{font-size:13px;color:var(--cinza);margin:0;flex:1}
.botoes{display:flex;gap:8px;flex-wrap:wrap}.btn{font-size:13px;font-weight:700;border-radius:10px;padding:8px 12px;text-decoration:none}
.btn.preco{background:var(--azul);color:#fff}.btn.det{border:1px solid var(--borda);color:var(--tinta)}
.tags{font-size:11px;color:var(--cinza)}.cat{display:block;background:#fff;border:1px solid var(--borda);border-radius:14px;padding:16px;text-decoration:none;color:var(--tinta)}
.cat b{font-size:17px}.cat span{display:block;font-size:13px;color:var(--cinza);margin-top:4px}
.aviso{background:#fdecea;border:1px solid #f3c6c1;color:#a33;border-radius:10px;padding:10px 12px;font-size:13px}
table{border-collapse:collapse;width:100%;background:#fff;font-size:14px}td,th{border:1px solid var(--borda);padding:8px;text-align:left;vertical-align:top}th{background:#eef1f4}
"""


def carrega_arvore():
    with open(ARQ_CATEGORIAS, encoding="utf-8") as f:
        return json.load(f)


def tem(nome, palavras):
    # a palavra precisa começar uma palavra do nome ("fone" não vale dentro de "microfone"; "halter" vale em "halteres")
    return any(re.search(r"(?<!\w)" + re.escape(p), nome) for p in palavras)


def classifica(item, arvore):
    nome = item["nome"].lower()
    for cat in arvore["categorias"]:
        for sub in cat["subcategorias"]:
            if tem(nome, sub["palavras"]):
                return cat, sub
    return None, None


def tags_do(item, arvore):
    nome = item["nome"].lower()
    return [t["tag"] for t in arvore["tags"] if tem(nome, t["palavras"])]


def pagina(titulo, corpo, cats, ativo=""):
    menu_cats = "".join(f'<li><a href="categoria-{c["slug"]}.html">{e(c["emoji"])} {e(c["nome"])}</a></li>' for c in cats)
    return f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(titulo)} - ESBOÇO comprenolink.net</title><link rel="stylesheet" href="estilo.css"></head><body>
<div class="faixa">ESBOÇO LOCAL — nada disto está publicado. Gerado em {datetime.now():%d/%m/%Y %H:%M}.</div>
<header><div class="topo"><a class="logo" href="index.html">🛒 comprenolink.net</a><nav><ul>
<li><a href="index.html">Início</a></li><li class="menu"><a href="#" aria-haspopup="true">Categorias ▾</a><ul>{menu_cats}</ul></li>
<li><a href="tag-black-friday.html">🔥 Black Friday</a></li><li><a href="{GUIA}" target="_blank">Lista completa 2026</a></li>
<li><a href="escolha-rapida.html">Escolha rápida</a></li><li><a href="matriz_mapeamento.html">Matriz</a></li></ul></nav></div></header>
<main>{corpo}</main></body></html>"""


def cartao(x, info):
    img = f'<img src="{e(x["imagem"])}" alt="{e(x["nome"])}" loading="lazy">' if x["imagem"] else ""
    selo = f'<span class="selo">⭐ {e(x["selo"])}</span>' if x["selo"] else ""
    desc = x["desc"] if len(x["desc"]) <= 140 else x["desc"][:137].rsplit(" ", 1)[0] + "…"
    return (f'<div class="card">{img}{selo}<h3>{e(x["nome"])}</h3><p>{e(desc)}</p>'
            f'<div class="tags">{" · ".join("#" + t for t in info["tags"])}</div><div class="botoes">'
            f'<a class="btn preco" href="{e(x["link"])}" target="_blank" rel="sponsored nofollow noopener">Ver preço</a>'
            f'<a class="btn det" href="{GUIA}#item-{x["n"]}" target="_blank">Ver detalhes</a></div></div>')


def main():
    arvore = carrega_arvore()
    cats = arvore["categorias"]
    minimo = arvore.get("minimo_para_publicar", 3)
    guia = gb.baixar_pagina(gb.carregar_config())
    itens = gb.itens(guia.conteudo)
    os.makedirs(SAIDA, exist_ok=True)
    with open(os.path.join(SAIDA, "estilo.css"), "w", encoding="utf-8") as f:
        f.write(CSS)

    info, sem_categoria = {}, []
    for x in itens:
        cat, sub = classifica(x, arvore)
        if not cat:
            sem_categoria.append(x)
        info[x["n"]] = {"cat": cat, "sub": sub, "tags": tags_do(x, arvore)}

    def da_cat(c):
        return [x for x in itens if info[x["n"]]["cat"] is c]

    # Páginas de categoria (hubs)
    for c in cats:
        xs = da_cat(c)
        blocos = ""
        for s in c["subcategorias"]:
            ys = [x for x in xs if info[x["n"]]["sub"] is s]
            if ys:
                ancora = re.sub(r"[^a-z0-9]+", "-", s["nome"].lower().encode("ascii", "ignore").decode()).strip("-")
                blocos += f'<h2 id="{ancora}">{e(s["nome"])} <small>({len(ys)})</small></h2><div class="grade">' + \
                          "".join(cartao(y, info[y["n"]]) for y in ys) + "</div>"
        aviso = "" if len(xs) >= minimo else (f'<p class="aviso">Só {len(xs)} produto(s): página fraca para o Google. '
                                              f'Recomendado publicar com {minimo} ou mais.</p>')
        corpo = (f'<div class="migalhas"><a href="index.html">Início</a> › {e(c["nome"])}</div><h1>{e(c["emoji"])} {e(c["nome"])}</h1>'
                 f'<p class="intro">{e(c["intro"])}</p>{aviso}' + (blocos or "<p>Nenhum produto ainda.</p>"))
        with open(os.path.join(SAIDA, f'categoria-{c["slug"]}.html'), "w", encoding="utf-8") as f:
            f.write(pagina(c["nome"], corpo, cats))

    # Páginas de tags
    for t in arvore["tags"]:
        ys = [x for x in itens if t["tag"] in info[x["n"]]["tags"]]
        corpo = (f'<div class="migalhas"><a href="index.html">Início</a> › #{e(t["tag"])}</div><h1>{e(t["titulo"])}</h1>'
                 f'<p class="intro">Seleção para {e(t["quando"])}: os produtos mais vendidos e bem avaliados do Mercado Livre.</p>'
                 f'<div class="grade">{"".join(cartao(y, info[y["n"]]) for y in ys)}</div>')
        with open(os.path.join(SAIDA, f'tag-{t["tag"]}.html'), "w", encoding="utf-8") as f:
            f.write(pagina(t["titulo"], corpo, cats))

    # Início simulada
    cards_cat = "".join(
        f'<a class="cat" href="categoria-{c["slug"]}.html"><b>{e(c["emoji"])} {e(c["nome"])}</b>'
        f'<span>{" · ".join(e(s["nome"]) for s in c["subcategorias"] if any(info[x["n"]]["sub"] is s for x in itens))}</span>'
        f'<span>{len(da_cat(c))} {"produto" if len(da_cat(c)) == 1 else "produtos"}</span></a>' for c in cats if da_cat(c))
    tags_links = " · ".join(f'<a href="tag-{t["tag"]}.html">#{e(t["tag"])}</a>' for t in arvore["tags"])
    corpo = ('<h1>Achados do Mercado Livre com o melhor custo-benefício</h1><p class="intro">Escolha uma categoria: em até 3 cliques você '
             'chega à oferta no Mercado Livre.</p><h2>Escolha por categoria</h2><div class="grade">' + cards_cat +
             f'</div><h2>Seleções especiais</h2><p>{tags_links}</p>')
    with open(os.path.join(SAIDA, "index.html"), "w", encoding="utf-8") as f:
        f.write(pagina("Início", corpo, cats))

    # Escolha rápida na nova árvore (melhor = 1º do ranking em cada subcategoria)
    linhas = ""
    for c in cats:
        for s in c["subcategorias"]:
            ys = [x for x in itens if info[x["n"]]["sub"] is s]
            if ys:
                y = ys[0]
                linhas += (f'<tr><td>{e(c["emoji"])} {e(c["nome"])}</td><td>{e(s["nome"])}</td><td><a href="{GUIA}#item-{y["n"]}" target="_blank">'
                           f'{e(nome_curto(y["nome"]))}</a></td><td><a href="{e(y["link"])}" target="_blank">Ver preço</a></td></tr>')
    corpo = ('<h1>Escolha rápida: o melhor de cada subcategoria</h1><p class="intro">Melhor = o produto mais acima no ranking do guia.</p>'
             f'<table><tr><th>Categoria</th><th>Subcategoria</th><th>Nossa escolha</th><th>Oferta</th></tr>{linhas}</table>')
    with open(os.path.join(SAIDA, "escolha-rapida.html"), "w", encoding="utf-8") as f:
        f.write(pagina("Escolha rápida", corpo, cats))

    # Matriz de mapeamento
    cab = ["Nº no guia", "Produto", "Categoria Pai", "Subcategoria", "Tags", "Destino (página de categoria a criar)", "Detalhes no guia", "Link de afiliado"]
    reg = []
    for x in itens:
        i = info[x["n"]]
        reg.append([x["n"], x["nome"], i["cat"]["nome"] if i["cat"] else "SEM CATEGORIA", i["sub"]["nome"] if i["sub"] else "-",
                    ", ".join(i["tags"]), f'{SITE}/{i["cat"]["slug"]}/#item-{x["n"]}' if i["cat"] else "-",
                    f"{GUIA}#item-{x['n']}", x["link"]])
    with open(os.path.join(SAIDA, "matriz_mapeamento.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(cab)
        w.writerows(reg)
    corpo = ('<h1>Matriz de Mapeamento</h1><p class="intro">Produto → Categoria Pai → Subcategoria → Tags → Destino. '
             'Também em matriz_mapeamento.csv (abre no Excel).</p><table><tr>' + "".join(f"<th>{e(h)}</th>" for h in cab[:6]) + "</tr>" +
             "".join("<tr>" + "".join(f"<td>{e(v)}</td>" for v in r[:6]) + "</tr>" for r in reg) + "</table>")
    with open(os.path.join(SAIDA, "matriz_mapeamento.html"), "w", encoding="utf-8") as f:
        f.write(pagina("Matriz de Mapeamento", corpo, cats))

    # Relatório
    rel = [f"ESBOÇO DE CATEGORIAS - gerado em {datetime.now():%d/%m/%Y %H:%M} (NADA FOI PUBLICADO)",
           f"Produtos lidos do guia: {len(itens)} (página modificada em {guia.modificado})", "",
           "ÁRVORE (Categoria Pai > Subcategoria: produtos)"]
    for c in cats:
        xs = da_cat(c)
        rel.append(f"  {c['nome']} ({len(xs)}){'   <- FRACA: menos de ' + str(minimo) + ' produtos' if 0 < len(xs) < minimo else ''}"
                   f"{'   (vazia - não criar ainda)' if not xs else ''}")
        for s in c["subcategorias"]:
            ys = [x["n"] for x in xs if info[x["n"]]["sub"] is s]
            rel.append(f"     > {s['nome']}: {ys if ys else '(vazia)'}")
    rel += ["", "TAGS"] + [f"  #{t['tag']} ({t['quando']}): {[x['n'] for x in itens if t['tag'] in info[x['n']]['tags']]}" for t in arvore["tags"]]
    rel += ["", "SEM CATEGORIA: " + (", ".join(f"{x['n']} {x['nome']}" for x in sem_categoria) or "nenhum"),
            "", "REGRA DOS 3 CLIQUES: Início (menu Categorias) > página da Categoria Pai > oferta no Mercado Livre = 2 cliques;",
            "  pelo cartão 'Escolha por categoria' da Início também 2 cliques. Nenhum produto passa de 3. OK.",
            "", "Arquivos: index.html, categoria-*.html, tag-*.html, escolha-rapida.html, matriz_mapeamento.csv/.html"]
    with open(os.path.join(SAIDA, "RELATORIO.txt"), "w", encoding="utf-8") as f:
        f.write("\n".join(rel) + "\n")
    print("\n".join(rel))
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    sys.exit(main())
