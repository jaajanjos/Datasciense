#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Gera a tabela "Escolha rápida: o melhor de cada categoria" (guia, página 5) e a lista
"Escolha por categoria" (Início, página 14) a partir dos produtos que estão no guia.

  * Cada produto vai para uma categoria pelas palavras do nome (CATEGORIAS, na ordem).
  * "O melhor" de cada categoria = o produto mais acima no ranking do guia.
  * Os links da Início levam direto ao 1º produto da categoria (#item-N), com o rastreio UTM.

Uso:
  python gerar_categorias.py              -> só gera a prévia (nada é publicado)
  python gerar_categorias.py --publicar   -> publica as duas páginas (backup antes de cada uma)
Prévia: 3_DOCUMENTACAO\\Blog_WordPress\\previa_categorias.html
"""
import html
import os
import re
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerenciar_blog as gb  # noqa: E402

PAGINA_INICIO = 14
GUIA = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"
UTM = "?utm_source=site&amp;utm_medium=home&amp;utm_campaign=botao_home&amp;utm_content="
RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PREVIA = os.path.join(RAIZ, "3_DOCUMENTACAO", "Blog_WordPress", "previa_categorias.html")

# (emoji + nome, palavras do nome do produto, utm_content, frase da Início, texto do link) — a ordem decide empates
CATEGORIAS = [
    ("🎮 Games e PC", ["gamer", "teclas", "teclado", "headset", "playstation", "console", "ssd"], "cat_games",
     "periféricos para jogar com mais precisão e conforto:", "Ver games e PC"),
    ("💪 Fitness e suplementos", ["creatina", "whey", "halter", "barra fixa", "academia", "musculação"], "cat_fitness",
     "para treinar em casa e manter a suplementação em dia:", "Ver fitness"),
    ("🍳 Cozinha", ["copo", "pote", "cozedor", "tempero", "micro-ondas", "mixer", "churrasqueira", "assadeira",
                   "panela", "airfryer", "liquidificador"], "cat_cozinha",
     "praticidade e organização para o dia a dia:", "Ver cozinha"),
    ("📱 Celulares e acessórios", ["motorola", "moto g", "galaxy", "iphone", "smartphone", "celular", "power bank",
                                  "carregador"], "cat_celular",
     "do primeiro celular aos acessórios que não podem faltar:", "Ver celulares"),
    ("🎧 Fones e caixas de som", ["fone", "caixa de som", "soundbar"], "cat_audio",
     "som de qualidade para música, filmes e chamadas:", "Ver fones e caixas"),
    ("📺 Smart TVs", ["smart tv", " tv "], "cat_tv",
     "imagem de qualidade e streaming na sala:", "Ver TVs"),
    ("🧹 Casa, limpeza e decoração", ["mop", "lavadora", "espelho", "aspirador", "echo dot", "alexa"], "cat_casa",
     "casa limpa, bonita e mais prática:", "Ver casa"),
    ("🌸 Beleza e perfumaria", ["perfume", "maquiagem", "secador", "chapinha"], "cat_beleza",
     "para se sentir bem e presentear:", "Ver beleza"),
]
OUTROS = ("🛍️ Outros achados", [], "cat_outros", "mais ofertas selecionadas:", "Ver outros achados")


def categoria(nome):
    n = f" {nome.lower()} "
    for cat in CATEGORIAS:
        if any(p in n for p in cat[1]):
            return cat
    return OUTROS


def agrupar(itens):
    grupos = {}
    for x in itens:
        grupos.setdefault(categoria(x["nome"])[0], []).append(x)
    ordem = [c for c in CATEGORIAS + [OUTROS] if c[0] in grupos]
    # categorias na ordem em que aparecem no guia (a do 1º produto primeiro)
    ordem.sort(key=lambda c: min(x["n"] for x in grupos[c[0]]))
    return [(c, sorted(grupos[c[0]], key=lambda x: x["n"])) for c in ordem]


MAX_NOMES = 3  # produtos citados por categoria na Início; os demais viram "e mais N opções"


def nome_curto(nome):
    """Versão enxuta do nome para as listas: corta o complemento depois de ' – ' e, se ainda
    ficar longo, o trecho a partir de ' com ' / ' para '."""
    n = nome.split(" – ")[0].strip()
    if len(n) > 32:
        for corte in (" com ", " para "):
            if corte in n and n.index(corte) >= 12:
                n = n[:n.index(corte)]
                break
    return n


def lista_nomes(xs):
    nomes = [html.escape(nome_curto(x["nome"]), quote=False) for x in xs[:MAX_NOMES]]
    resto = len(xs) - len(nomes)
    if resto:
        return ", ".join(nomes) + f" e mais {resto} {'opção' if resto == 1 else 'opções'}"
    return nomes[0] if len(nomes) == 1 else ", ".join(nomes[:-1]) + " e " + nomes[-1]


def tabela(grupos):
    linhas = "".join(
        f'<tr><td>{html.escape(c[0], quote=False)}</td><td><a href="#item-{xs[0]["n"]}">{html.escape(nome_curto(xs[0]["nome"]), quote=False)}</a></td>'
        f'<td><a href="{html.escape(xs[0]["link"])}" target="_blank" rel="sponsored nofollow noopener">Ver preço</a></td></tr>'
        for c, xs in grupos)
    return ('<!-- wp:table {"className":"cnl-escolha"} -->\n<figure class="wp-block-table cnl-escolha"><table class="has-fixed-layout">'
            '<thead><tr><th>Categoria</th><th>Nossa escolha</th><th>Oferta</th></tr></thead>'
            f'<tbody>{linhas}</tbody></table></figure>\n<!-- /wp:table -->')


def lista_inicio(grupos):
    itens = "\n\n".join(
        f'<!-- wp:list-item -->\n<li><strong>{html.escape(c[0], quote=False)}</strong> – {c[3]} {lista_nomes(xs)}. '
        f'<a href="{GUIA}{UTM}{c[2]}#item-{xs[0]["n"]}">{c[4]}</a></li>\n<!-- /wp:list-item -->'
        for c, xs in grupos)
    return f'<!-- wp:list -->\n<ul class="wp-block-list">{itens}</ul>\n<!-- /wp:list -->'


def troca_tabela(conteudo, nova):
    i = conteudo.find('id="escolha-rapida"')
    a = conteudo.find('<!-- wp:table', i)
    b = conteudo.find('<!-- /wp:table -->', a) + len('<!-- /wp:table -->')
    if i < 0 or a < 0 or b < len('<!-- /wp:table -->'):
        raise gb.Erro("Tabela 'Escolha rápida' não encontrada no guia.")
    return conteudo[:a] + nova + conteudo[b:]


def troca_lista(conteudo, nova):
    i = conteudo.find('>Escolha por categoria</h2>')
    a = conteudo.find('<!-- wp:list -->', i)
    b = conteudo.find('<!-- /wp:list -->', a) + len('<!-- /wp:list -->')
    if i < 0 or a < 0 or b < len('<!-- /wp:list -->'):
        raise gb.Erro("Lista 'Escolha por categoria' não encontrada na Início.")
    return conteudo[:a] + nova + conteudo[b:]


def main():
    publicar = "--publicar" in sys.argv
    cfg = gb.carregar_config()
    guia = gb.baixar_pagina(cfg)
    itens = gb.itens(guia.conteudo)
    grupos = agrupar(itens)
    nova_tab, nova_lista = tabela(grupos), lista_inicio(grupos)
    novo_guia = troca_tabela(guia.conteudo, nova_tab)
    d = gb.requisitar(cfg, "GET", f"/wp-json/wp/v2/pages/{PAGINA_INICIO}?context=edit")
    novo_inicio = troca_lista(d["content"]["raw"], nova_lista)

    print(f"{len(itens)} produtos em {len(grupos)} categorias:")
    for c, xs in grupos:
        print(f"  {c[0]:30} melhor: #{xs[0]['n']} {xs[0]['nome'][:40]:40} | todos: {[x['n'] for x in xs]}")
    os.makedirs(os.path.dirname(PREVIA), exist_ok=True)
    with open(PREVIA, "w", encoding="utf-8") as f:
        f.write('<!doctype html><meta charset="utf-8"><title>Prévia das categorias</title>'
                '<style>body{font-family:Segoe UI,sans-serif;max-width:860px;margin:24px auto;padding:0 16px;color:#1a2230}'
                'table{border-collapse:collapse;width:100%}td,th{border:1px solid #ddd;padding:8px;text-align:left}'
                'th{background:#f3f4f6}li{margin:8px 0}h1{font-size:20px}.n{color:#666;font-size:13px}</style>'
                f'<h1>Prévia gerada em {datetime.now():%d/%m/%Y %H:%M} (ainda NÃO publicada)</h1>'
                '<h2>Guia — Escolha rápida: o melhor de cada categoria</h2>' + nova_tab +
                '<h2>Início — Escolha por categoria</h2>' + nova_lista)
    print("prévia:", PREVIA)
    if not publicar:
        print("Nada foi publicado. Para publicar: python gerar_categorias.py --publicar")
        return 0
    if gb.verificar(novo_guia):
        raise gb.Erro("Guia ficaria inconsistente: " + "; ".join(gb.verificar(novo_guia)))
    gb.publicar(cfg, guia, novo_guia, guia.titulo)
    base = os.path.join(gb.PASTA_BACKUP, f"pagina14_inicio_{datetime.now():%Y-%m-%d_%Hh%M%S}.html")
    with open(base, "w", encoding="utf-8", newline="") as f:
        f.write(d["content"]["raw"])
    print("Backup da Início salvo em:", base)
    gb.requisitar(cfg, "POST", f"/wp-json/wp/v2/pages/{PAGINA_INICIO}", {"content": novo_inicio})
    print("Início publicada.")
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    try:
        sys.exit(main())
    except gb.Erro as e:
        print("ERRO:", e)
        sys.exit(1)
