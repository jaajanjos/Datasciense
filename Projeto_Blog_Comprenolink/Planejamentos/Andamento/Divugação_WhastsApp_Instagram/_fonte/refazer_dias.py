# -*- coding: utf-8 -*-
"""
Refaz o pacote do dia (textos, feed/story/status e Reels) de datas ESPECÍFICAS, forçando o item do guia.
Uso:  python -X utf8 _fonte\\refazer_dias.py 2026-11-28=14 2026-12-23=35
Criado em 13/11/2026: a troca dos anúncios 14 e 35 deixou os pacotes de 28/11 e 23/12 com o produto antigo.
Não mexe nos outros dias (a fila do calendário muda quando os itens do guia mudam, por isso NÃO usar o gerar_artes_catalogo.py inteiro).
Faça cópia da pasta do dia em _backup_pacotes ANTES de rodar.
"""
import os
import re
import sys
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dados_divulgacao as dd  # noqa: E402
import gerar_artes_catalogo as g  # noqa: E402
import gerar_reels  # noqa: E402


def refaz(dados, cal, dia, n):
    itens = {x["n"]: x for x in dados["itens"]}
    x = itens[n]
    ls = [l for l in cal if l["data"] == dia]
    camp = ls[0]["campanha"]
    t = dd.textos_produto(x, camp, dia)
    t["story"] = re.sub(r"\n\n+", "\n", t["story"])  # selo em branco não deixa linha vazia
    pasta = os.path.join(g.PACOTE, f"{dia:%Y-%m-%d}_{g.DIAS[dia.weekday()]}")
    os.makedirs(pasta, exist_ok=True)
    txt = [f"PACOTE DO DIA {dia:%d/%m/%Y} ({g.DIAS[dia.weekday()]}) – {'Black Friday' if camp == 'black_friday' else 'Natal'}",
           "Ordem: abra cada bloco, copie o texto e publique. Imagens nesta pasta.", ""]
    for formato in ("feed", "story", "status"):
        g.arte(x, camp, formato).save(os.path.join(pasta, f"{formato}.png"))
    for l in ls:
        if not l["item"]:
            raise SystemExit(f"{dia}: linha sem item ({l['formato']}); este script só refaz dias de produto.")
        f = l["formato"]
        if f.startswith("Post no feed"):
            texto, link, img = t["legenda"], "", "feed.png"
        elif f.startswith("Story"):
            texto, link, img = t["story"], t["link_story"], "story.png"
        elif f == "Status":
            texto, link, img = t["wpp"].replace("{LINK}", t["link_wpp"]["status"]), t["link_wpp"]["status"], "status.png"
        elif f == "Canal":
            texto, link, img = t["wpp"].replace("{LINK}", t["link_wpp"]["canal"]), t["link_wpp"]["canal"], "feed.png"
        else:
            raise SystemExit(f"{dia}: formato inesperado: {f}")
        txt += ["=" * 60, f"{l['hora']}  {l['canal']} – {f}", f"Imagem: {img}", "=" * 60, texto, ""]
        if f.startswith("Story"):
            txt += ["Link para o adesivo:", link, ""]
        if l["obs"]:
            txt += ["Obs.: " + l["obs"], ""]
    with open(os.path.join(pasta, "1_TEXTOS_DO_DIA.txt"), "w", encoding="utf-8-sig", newline="\r\n") as fh:
        fh.write("\n".join(txt))
    ok = gerar_reels.gera(pasta)
    print(f"{dia:%d/%m/%Y}: item {n} '{x['nome']}' | reels {'ok' if ok else 'NÃO gerado'} | {pasta}")


def main():
    alvos = {}
    for a in sys.argv[1:]:
        d, n = a.split("=")
        alvos[datetime.strptime(d, "%Y-%m-%d").date()] = int(n)
    if not alvos:
        raise SystemExit(__doc__)
    dados = dd.carrega_produtos()
    dd.carrega_produtos.cache = dados
    cal = dd.calendario(dados)
    for dia, n in sorted(alvos.items()):
        refaz(dados, cal, dia, n)


if __name__ == "__main__":
    main()
