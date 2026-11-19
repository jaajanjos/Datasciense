# -*- coding: utf-8 -*-
"""Textos de venda dos 3 anúncios que entraram no blog em 31/10/2026 (Forma Tramontina, Projetor Hardline HY320 e Conjunto Moletom Infantil)
e remoção do preço que veio no título de 2 anúncios antigos. Os itens são localizados PELO NOME (a numeração do guia muda quando um item é retirado).
Uso:  python -X utf8 aplicar_textos_212_214.py            (pré-visualização)
      python -X utf8 aplicar_textos_212_214.py --aplicar  (publica, com backup)
Regras do blog: sem preço, sem "melhor/mais vendido", sem promessa de saúde/estética, só fatos do título do anúncio.
"""
import re
import sys
import types

sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, "D:/D:\Projeto_Blog_Comprenolink/Gestao_Anuncios_Blog/1_PROGRAMAS/Blog_WordPress")
import gerenciar_blog as g  # noqa: E402

APLICAR = "--aplicar" in sys.argv
PROIBIDO = re.compile(r"R\$|\breais\b|barat|menor pre|melhor pre|desconto|% ?off|promo[cç]|\bmelhor(es)?\b|mais vendid|\bl[ií]der|garantid|"
                      r"\bcura\b|\btrata(r|mento)?\b|emagrec|rejuvenesc|anti-?idade|saud[aá]vel|hidrata[cç][aã]o|oleosa|imunidade", re.I)

TEXTOS = {
    "Forma Bolo Pudim 24cm": dict(
        nome="Forma de Bolo e Pudim Tramontina Starflon 24 cm",
        selo="Antiaderente Starflon",
        desc="Para bolos e pudins de todo dia: forma Tramontina Starflon com revestimento antiaderente, 24 cm de diâmetro e capacidade de 2,6 litros, na cor grafite.",
        beneficios=["Revestimento antiaderente Starflon", "24 cm de diâmetro", "Capacidade de 2,6 litros", "Cor grafite"],
        ideal=["Bolos caseiros", "Pudins", "Sobremesas", "Cozinha do dia a dia"]),
    "Projetor HY320 Hardline": dict(
        nome="Projetor HY320 Hardline Android Full HD",
        selo="Full HD e Wi-Fi 6",
        desc="Cinema em casa: projetor Hardline HY320 com sistema Android, Wi-Fi 6, 390 ANSI lumens, Full HD e suporte a 4K, para telas de 85 a 200 polegadas.",
        beneficios=["Full HD com suporte a 4K", "390 ANSI lumens", "Android, Wi-Fi 6 e Bluetooth", "Telas de 85 a 200 polegadas"],
        ideal=["Filmes e séries", "Futebol", "Quarto e sala", "Jogos"]),
    "Conjunto Moletom Ny": dict(
        nome="Conjunto de Moletom e Calça Infantil Unissex Ny",
        selo="Unissex Infantil",
        desc="Conjunto infantil com moletom e calça, unissex, disponível em várias cores. Esta opção é no tamanho 16, na cor preta.",
        beneficios=["Moletom e calça no mesmo conjunto", "Modelo unissex", "Várias cores disponíveis", "Opção no tamanho 16, na cor preta"],
        ideal=["Meninos e meninas", "Dias mais frios", "Uso diário", "Passeios"]),
}
LIMPAR_PRECO = ("Lenovo IdeaPad Slim 3", "Fire Tv Stick")  # nomes antigos que trazem "– R$ ..." no título

erros = []
for chave, c in TEXTOS.items():
    for campo in ("nome", "selo", "desc"):
        if PROIBIDO.search(c[campo]):
            erros.append((chave, campo, c[campo]))
    for campo in ("beneficios", "ideal"):
        erros += [(chave, campo, t) for t in c[campo] if PROIBIDO.search(t)]
    if len(c["beneficios"]) != 4 or len(c["ideal"]) != 4 or len(c["desc"]) > 260:
        erros.append((chave, "tamanho", ""))
if erros:
    print("CONFERÊNCIA DE POLÍTICA FALHOU:", erros)
    sys.exit(2)
print("Conferência de política OK.")

cfg = g.carregar_config()
p = g.baixar_pagina(cfg, None)
s = p.conteudo
itens = g.itens(s)
alvos = {}
for x in itens:
    for chave in TEXTOS:
        if chave.lower() in x["nome"].lower():
            alvos[x["n"]] = dict(TEXTOS[chave])
    for chave in LIMPAR_PRECO:
        if chave.lower() in x["nome"].lower() and "R$" in x["nome"]:
            novo = re.sub(r"\s*[–-]\s*R\$\s*[\d\.,]+", "", x["nome"]).strip()
            alvos[x["n"]] = dict(nome=novo)
print("Itens que serão alterados (número atual):")
for n in sorted(alvos):
    print(f"  {n}: {alvos[n]['nome'][:80]}")
if len(alvos) != 5:
    print("ATENÇÃO: esperava 5 itens, achei", len(alvos))
    sys.exit(3)
for n in sorted(alvos):
    s, avisos = g.editar_item(s, n, alvos[n])
    for a in avisos:
        print(f"  ATENÇÃO item {n}: {a}")
s, titulo = g.normalizar(s, p.titulo)
print("Problemas de verificação:", g.verificar(s))
g.efetivar(cfg, types.SimpleNamespace(aplicar=APLICAR, offline=None), p, s, titulo, False)
