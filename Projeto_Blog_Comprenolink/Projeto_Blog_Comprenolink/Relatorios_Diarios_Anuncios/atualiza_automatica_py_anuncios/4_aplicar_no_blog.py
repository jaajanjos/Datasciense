# -*- coding: utf-8 -*-
"""ETAPA 4 - Aplica no guia do blog (WordPress) as substituições validadas em substituicoes_aprovadas.json.

Usa o gerenciar_blog.py (o mesmo das trocas manuais): ele confere a página, mostra o resumo da mudança, faz BACKUP da
página antes de publicar (Gestao_Anuncios_Blog\\2_DADOS\\Blog_WordPress\\backups) e só então publica.
O item é localizado pelo LINK ANTIGO (os números dos itens mudam quando entra/sai produto).
Cada troca é registrada em historico_substituicoes.csv (para a sua validação de link e produto).

Uso:  python 4_aplicar_no_blog.py              (publica no site)
      python 4_aplicar_no_blog.py --simular    (só pré-visualiza: baixa a página e mostra a mudança, NÃO publica)
      python 4_aplicar_no_blog.py --arquivo X.json [--simular]   (usa outro arquivo de substituições)
"""
import csv
import importlib.util
import os
import re
import sys
from datetime import datetime

import comum


def carregar_blog(caminho):
    spec = importlib.util.spec_from_file_location("gerenciar_blog", caminho)
    gb = importlib.util.module_from_spec(spec)
    sys.path.insert(0, os.path.dirname(caminho))
    spec.loader.exec_module(gb)
    return gb


def registrar(linha):
    novo = not os.path.exists(comum.ARQ_HISTORICO)
    if not novo:
        comum.old_bkp(comum.ARQ_HISTORICO)
    with open(comum.ARQ_HISTORICO, "a", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        if novo:
            w.writerow(["data", "modo", "item", "nome_antigo", "link_antigo", "nome_novo", "link_novo", "preco",
                        "anuncio_mlb", "vendedor", "politica", "resultado", "conferir"])
        w.writerow(linha)


def main():
    simular = "--simular" in sys.argv
    arq = sys.argv[sys.argv.index("--arquivo") + 1] if "--arquivo" in sys.argv else comum.ARQ_SUBSTITUICOES
    c = comum.cfg()
    comum.abrir_log("atualiza")
    comum.titulo("ETAPA 4 - Trocar os anúncios no guia do blog" + (" [SIMULAÇÃO: nada será publicado]" if simular else ""))
    dados = comum.ler_json(arq)
    if not dados:
        comum.log(f"Nada a aplicar: {arq} não existe (a etapa 3 não gerou substituições).")
        return 0
    subs = dados.get("substituicoes") or []
    if not subs:
        comum.log("Nenhuma substituição válida para aplicar.")
        return 0

    gb = carregar_blog(c["gerenciar_blog"])
    cfg_wp = gb.carregar_config()
    pagina = gb.baixar_pagina(cfg_wp)
    itens = gb.itens(pagina.conteudo)
    falhas = 0
    for s in subs:
        alvo = next((i for i in itens if i["link"] == s["link_antigo"]), None)
        quando = datetime.now().strftime("%Y-%m-%d %H:%M")
        if alvo is None:
            comum.log(f"  item {s['item']}: o link antigo {s['link_antigo']} não está mais no guia. Pulado.")
            registrar([quando, "simulação" if simular else "real", s["item"], "", s["link_antigo"], s["nome"], s["link"],
                       s["preco"], s.get("anuncio_mlb", ""), s.get("vendedor", ""), s.get("politica", ""),
                       "PULADO: link antigo não encontrado", ""])
            continue
        n = alvo["n"]
        if str(n) != str(s["item"]):
            comum.log(f"  Atenção: o produto mudou de número no guia (era {s['item']}, agora é {n}). Usando {n}.")
        if any(i["link"] == s["link"] for i in itens):
            comum.log(f"  item {n}: o link novo {s['link']} JÁ existe em outro item do guia. Pulado (evita duplicar).")
            registrar([quando, "simulação" if simular else "real", n, alvo["nome"], s["link_antigo"], s["nome"],
                       s["link"], s["preco"], s.get("anuncio_mlb", ""), s.get("vendedor", ""), s.get("politica", ""),
                       "PULADO: link novo já existe no guia", ""])
            continue
        cmd = [sys.executable, "-X", "utf8", c["gerenciar_blog"], "editar", str(n),
               "--nome", s["nome"], "--link", s["link"], "--titulo-anuncio", s["titulo_anuncio"],
               "--imagem", s["imagem"]]   # sem --preco: o blog não mostra preço (política do dono)
        # selo em branco é permitido (decisão do dono 12/11/2026): "-" limpa o selo do produto anterior
        if s.get("selo"):
            cmd += ["--selo", s["selo"]]
        elif alvo.get("selo"):
            cmd += ["--selo", "-"]
        if s.get("desc"):
            cmd += ["--desc", s["desc"]]
        for campo, opcao in (("beneficios", "--beneficios"), ("ideal", "--ideal")):
            if s.get(campo):
                cmd += [opcao, " | ".join(s[campo]) if isinstance(s[campo], list) else s[campo]]
        if not simular:
            cmd.append("--aplicar")
        comum.log(f"  item {n}: {alvo['nome']}  ->  {s['nome']} ({s['link']})")
        codigo = comum.rodar(cmd, cwd=os.path.dirname(c["gerenciar_blog"]), tempo_limite=600)
        conferir = []
        if alvo.get("preco_auto"):
            conferir.append("cartão do plugin Hostinger: confira foto/título/preço do cartão no site")
        conferir.append("validar link e produto (dono)")
        validacao = ""
        if codigo == 0 and not simular:
            # VALIDAÇÃO: relê o guia publicado e prova que a troca ficou lá
            pagina = gb.baixar_pagina(cfg_wp)
            itens = gb.itens(pagina.conteudo)
            problemas = []
            novos = [i for i in itens if i["link"] == s["link"]]
            if len(novos) != 1:
                problemas.append(f"link novo aparece {len(novos)}x no guia (esperado 1)")
            elif novos[0]["nome"].strip().lower() != s["nome"].strip().lower():
                problemas.append(f"nome no guia diferente do esperado ({novos[0]['nome']!r})")
            if any(i["link"] == s["link_antigo"] for i in itens):
                problemas.append("link antigo ainda está no guia")
            if novos:   # política: o guia não pode mostrar preço
                for campo in ("nome", "titulo_anuncio", "selo", "desc"):
                    if re.search(r"R\$\s*\d", novos[0][campo] or ""):
                        problemas.append(f"PREÇO no campo {campo} do guia (proibido pela política do blog)")
            validacao = "VALIDADO no guia (link novo presente, link antigo removido)" if not problemas                 else "FALHOU na validação: " + "; ".join(problemas)
            comum.log(f"  item {n}: {validacao}")
            if problemas:
                falhas += 1
        if codigo != 0:
            falhas += 1
            resultado = "ERRO ao aplicar (veja o log)"
        elif simular:
            resultado = "pré-visualizado (simulação)"
        else:
            resultado = "publicado" if validacao.startswith("VALIDADO") else "publicado, mas " + validacao
        if validacao:
            conferir.insert(0, validacao)
        registrar([quando, "simulação" if simular else "real", n, alvo["nome"], s["link_antigo"], s["nome"], s["link"],
                   s["preco"], s.get("anuncio_mlb", ""), s.get("vendedor", ""), s.get("politica", ""), resultado,
                   "; ".join(conferir)])
    comum.log(f"Histórico das trocas (para você validar): {comum.ARQ_HISTORICO}")
    return 1 if falhas else 0


if __name__ == "__main__":
    sys.exit(main())
