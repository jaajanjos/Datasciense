#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Atualização automática das categorias (roda pelo Agendador do Windows, a cada 3 horas).

Quando o guia (anúncios novos, removidos ou editados), o categorias.json ou a fase da campanha
(Black Friday até 30/11 -> Natal de 01/12 a 25/12 -> nenhuma) mudam, roda
"publicar_categorias.py --publicar": páginas de categoria, Black Friday/Natal, Escolha rápida,
Início e menu. Se nada mudou, não publica nada (não enche o WordPress de revisões).

Produto sem categoria: não publica, anota no log e tenta de novo na próxima rodada
(é só incluir a palavra no categorias.json ou pedir "gerar as categorias").
Os textos de venda dos anúncios novos continuam sendo feitos no "gerar as categorias";
o log lista os itens novos que ainda precisam desse capricho.

Log: 2_DADOS\\Blog_WordPress\\atualizar_categorias.log      Forçar: --forcar
"""
import contextlib
import hashlib
import io
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerenciar_blog as gb  # noqa: E402
import publicar_categorias as pc  # noqa: E402
from gerar_esboco_categorias import ARQ_CATEGORIAS, carrega_arvore  # noqa: E402

LOG = os.path.join(gb.PASTA_DADOS, "atualizar_categorias.log")
ESTADO = os.path.join(gb.PASTA_DADOS, "atualizar_categorias_estado.json")


def anota(*linhas):
    with open(LOG, "a", encoding="utf-8") as f:
        for linha in linhas:
            f.write(f"{datetime.now():%d/%m/%Y %H:%M} {linha}\n")
    with open(LOG, encoding="utf-8") as f:  # guarda só as últimas 2000 linhas
        todas = f.readlines()
    if len(todas) > 2000:
        with open(LOG, "w", encoding="utf-8") as f:
            f.writelines(todas[-2000:])


def fase(arvore):
    dia = pc.hoje()
    tag = {t["tag"]: t for t in arvore["tags"]}
    bf, natal = tag["black-friday"], tag.get("natal-presentes")
    camp = next((t["tag"] for t in (bf, natal) if t and pc.valendo(t, dia)), "nenhuma")
    return f"destaque={camp}|natal_no_ar={bool(natal and pc.tem_pagina(natal, dia))}"


def chave(cfg):
    guia = gb.baixar_pagina(cfg)
    with open(ARQ_CATEGORIAS, "rb") as f:
        arv = f.read()
    h = hashlib.sha256(guia.conteudo.encode("utf-8") + arv + fase(carrega_arvore()).encode()).hexdigest()
    return h, [x["link"] for x in gb.itens(guia.conteudo)], {x["link"]: f'{x["n"]} {x["nome"]}' for x in gb.itens(guia.conteudo)}


def main():
    cfg = gb.carregar_config()
    antes = {}
    if os.path.exists(ESTADO):
        with open(ESTADO, encoding="utf-8") as f:
            antes = json.load(f)
    h, links, nomes = chave(cfg)
    if h == antes.get("chave") and "--forcar" not in sys.argv:
        anota(f"sem mudanças ({len(links)} produtos, {fase(carrega_arvore())})")
        return 0
    novos = [nomes[k] for k in links if antes.get("links") and k not in antes["links"]]
    saiu = io.StringIO()
    sys.argv = [sys.argv[0], "--publicar"]
    try:
        with contextlib.redirect_stdout(saiu):
            pc.main()
    except gb.Erro as erro:
        anota(f"ERRO, nada publicado: {erro}")
        return 1
    h, links, _ = chave(cfg)  # depois de publicar (a Escolha rápida mexe no guia)
    with open(ESTADO, "w", encoding="utf-8") as f:
        json.dump({"chave": h, "links": links, "quando": f"{datetime.now():%d/%m/%Y %H:%M}"}, f, ensure_ascii=False, indent=2)
    resumo = [l.strip() for l in saiu.getvalue().splitlines() if l.strip() and "backup" not in l]
    anota(f"PUBLICADO ({len(links)} produtos, {fase(carrega_arvore())})", *[f"   {l}" for l in resumo])
    if novos:
        anota("   anúncios novos (pedir 'gerar as categorias' para os textos de venda): " + "; ".join(novos))
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as erro:  # noqa: BLE001 - no agendador não há tela: tudo vai para o log
        anota(f"ERRO inesperado: {erro!r}")
        sys.exit(1)
