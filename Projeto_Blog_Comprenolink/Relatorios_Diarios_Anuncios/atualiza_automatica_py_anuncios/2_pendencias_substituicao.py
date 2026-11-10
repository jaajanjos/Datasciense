# -*- coding: utf-8 -*-
"""ETAPA 2 - Monta a lista de anúncios que precisam de substituto (pausados, removidos e outras situações fora do
normal) a partir da última verificação, com os requisitos de cada um. Grava pendencias_substituicao.json.

Usa a mesma regra do quadro "Precisam de substituto" do relatório (função situacao_anuncios do 3_).
Uso:  python 2_pendencias_substituicao.py
"""
import importlib
import sys
from datetime import datetime

import comum


def main():
    c = comum.cfg()
    comum.abrir_log("atualiza")
    comum.titulo("ETAPA 2 - Lista de anúncios que precisam de substituto")
    sys.path.insert(0, c["pasta_fontes_painel"])
    rel = importlib.import_module(c["programa_relatorio"][:-3])
    info = rel.situacao_anuncios()
    if info is None:
        comum.log("ERRO: não há verificação dos anúncios gravada. Rode a etapa 1 primeiro.")
        return 1
    faixa = float(c.get("faixa_preco", 0.20))
    pend = []
    for x in info["pendentes"]:
        preco = x.get("preco")
        pend.append({
            "item": int(x["item"]) if str(x["item"]).isdigit() else x["item"],
            "nome_no_blog": x["nome"],
            "titulo_no_ml": x["titulo"],
            "categoria": x["categoria"],
            "situacao_ml": x["status"],
            "aviso_ml": x["aviso"],
            "fora_do_ar_desde": x["desde"],
            "link_antigo": x["link"],
            "catalogo_mlb": x["catalogo"],
            "anuncio_mlb": x["anuncio"],
            "preco_antes": preco,
            "preco_min": round(preco * (1 - faixa), 2) if preco else None,
            "preco_max": round(preco * (1 + faixa), 2) if preco else None,
            "busca_mesmo_produto": f"https://www.mercadolivre.com.br/p/{x['catalogo']}/s" if x["catalogo"] else "",
            "busca_mesmo_tipo": f"https://lista.mercadolivre.com.br/{rel.slug_busca(x['titulo'] or x['nome'])}",
        })
    dados = {
        "gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "ultima_verificacao_ml": info["ultima"],
        "anuncios_ativos": info["ativos"],
        "anuncios_total": info["total"],
        "requisitos_substituto": [rel.re.sub(r"<[^>]+>", "", r) for r in rel.REQUISITOS_SUBSTITUTO],
        "pendentes": pend,
    }
    comum.gravar_json(comum.ARQ_PENDENCIAS, dados)
    comum.log(f"Última verificação no ML: {info['ultima']} · {info['ativos']} de {info['total']} ativos")
    if not pend:
        comum.log("Nenhum anúncio precisa de substituto agora.")
    for p in pend:
        faixa_txt = (f"R$ {p['preco_min']:.2f} a R$ {p['preco_max']:.2f}" if p["preco_antes"] else "preço não disponível")
        comum.log(f"  item {p['item']:>3} · {p['situacao_ml']:<10} · {p['nome_no_blog'][:55]} · {faixa_txt}")
    comum.log(f"{len(pend)} pendente(s) gravado(s) em {comum.ARQ_PENDENCIAS}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
