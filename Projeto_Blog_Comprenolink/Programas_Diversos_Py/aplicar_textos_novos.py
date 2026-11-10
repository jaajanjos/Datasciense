# -*- coding: utf-8 -*-
"""Aplica no guia do blog os textos de venda dos anúncios novos e os ajustes de política (um único publish, com backup).
Uso:  python -X utf8 aplicar_textos_novos.py            (pré-visualização, nada é publicado)
      python -X utf8 aplicar_textos_novos.py --aplicar  (publica)
Antes de publicar, confere o texto contra as regras do blog (preço, "melhor", "mais vendido", saúde/estética).
"""
import re
import sys
import types

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/Projeto_Blog_Comprenolink/Programas_Diversos_Py")
sys.path.insert(0, "D:/Projeto_Blog_Comprenolink/Gestao_Anuncios_Blog/1_PROGRAMAS/Blog_WordPress")
import gerenciar_blog as g  # noqa: E402
import textos_novos_anuncios_2026_10_30 as T  # noqa: E402

APLICAR = "--aplicar" in sys.argv
PROIBIDO = re.compile(r"R\$|\breais\b|barat|menor pre|melhor pre|desconto|% ?off|promo[cç]|\bmelhor(es)?\b|mais vendid|\bl[ií]der|garantid|"
                      r"\bcura\b|\btrata(r|mento)?\b|emagrec|rejuvenesc|anti-?idade|saud[aá]vel|hidrata[cç][aã]o|oleosa|imunidade", re.I)

todos = {**T.NOVOS}
for n, c in T.AJUSTES_ANTIGOS.items():
    todos[n] = c

erros = []
for n, c in todos.items():
    for campo in ("selo", "desc"):
        if campo in c and PROIBIDO.search(c[campo]):
            erros.append((n, campo, c[campo]))
    for campo in ("beneficios", "ideal"):
        for t in c.get(campo, []):
            if PROIBIDO.search(t):
                erros.append((n, campo, t))
    if "beneficios" in c and len(c["beneficios"]) != 4:
        erros.append((n, "beneficios", "não tem 4 itens"))
    if "ideal" in c and len(c["ideal"]) != 4:
        erros.append((n, "ideal", "não tem 4 itens"))
    if "desc" in c and len(c["desc"]) > 260:
        erros.append((n, "desc", f"{len(c['desc'])} caracteres"))
if erros:
    print("CONFERÊNCIA DE POLÍTICA FALHOU:")
    for e in erros:
        print("  ", e)
    sys.exit(2)
print(f"Conferência de política OK em {len(todos)} itens.")

cfg = g.carregar_config()
p = g.baixar_pagina(cfg, None)
s = p.conteudo
print("Itens na página:", len(g.secoes(s)))
for n in sorted(todos):
    s, avisos = g.editar_item(s, n, todos[n])
    for a in avisos:
        print(f"  ATENÇÃO item {n}: {a}")
s, titulo = g.normalizar(s, p.titulo)
print("Problemas de verificação:", g.verificar(s))
g.efetivar(cfg, types.SimpleNamespace(aplicar=APLICAR, offline=None), p, s, titulo, False)
