# -*- coding: utf-8 -*-
"""GERA_GRAFICO_ANUNCIO_META.py  (criado em 21/11/2026 a pedido do dono)

Gera o gráfico de 4 quadros do anúncio da Meta (o mesmo modelo de GRAFICO_ANUNCIO_META_16_11_2026_20h50.png):
  1) Gasto acumulado (linha) com a verba total (linha tracejada)
  2) Visitas reais vindas do anúncio, por dia (site)
  3) Meta (visualizações) x blog (visitas reais), total
  4) Custo por visita real, custo por visualização da Meta e a meta de custo

DE ONDE VÊM OS DADOS (só leitura, nada é alterado):
  - Gasto, alcance e visualizações: LEITURA_ANUNCIO_META_historico.csv  (pasta 4_Relatorio_Ativ_Claude_no_Blog)
  - Visitas reais por dia: o arquivo acessos_*.csv MAIS NOVO de Relatorios_Diarios_Anuncios\\dados_acessos
    (1 visita = 1 sessão; dia no fuso de Brasília = horário do arquivo - 3 h)

USO (na pasta Programas_Diversos_Py):
  python -X utf8 GERA_GRAFICO_ANUNCIO_META.py
      -> gráfico do teste de 11 a 13/11 (padrão, igual ao de 16/11)
  python -X utf8 GERA_GRAFICO_ANUNCIO_META.py --campanha bf_26_entrada --nome "bf_26_entrada" --verba 240 --meta-custo 0.35
      -> gráfico do anúncio da Black Friday + Natal (a coluna de gasto do CSV precisa ter as leituras dessa campanha)
  Opções: --csv CAMINHO  --acessos CAMINHO  --saida PASTA

O PNG é gravado em 0- Pendencias\\4_Relatorio_Ativ_Claude_no_Blog com o nome GRAFICO_ANUNCIO_META_DD_MM_AAAA_HHhMM.png
(a versão anterior continua na pasta; mova para old_bkp se quiser manter só uma).
"""
import argparse
import csv
import datetime as dt
import glob
import os
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

PASTA_REL = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
PASTA_ACESSOS = r"D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\dados_acessos"
CSV_PADRAO = os.path.join(PASTA_REL, "LEITURA_ANUNCIO_META_historico.csv")

AZUL, VERDE, CINZA, VERMELHO = "#2563eb", "#16a34a", "#9ca3af", "#dc2626"


def ler_leituras(caminho):
    """Linhas do histórico: data;hora;gasto;impressoes;alcance;resultados;status;observacao. Ignora linhas vazias."""
    out = []
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        for l in csv.DictReader(f, delimiter=";"):
            if not l.get("data") or not l.get("gasto"):
                continue
            out.append({
                "data": l["data"].strip(), "hora": l["hora"].strip(),
                "gasto": float(l["gasto"].replace(",", ".")),
                "resultados": int(float(l["resultados"] or 0)),
            })
    return out


def visitas_por_dia(caminho, campanha):
    """Conta sessões distintas por dia (Brasília) da campanha. Só linhas tipo 'visita'."""
    sess = {}
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        for l in csv.DictReader(f, delimiter=";"):
            if l.get("tipo") != "visita" or l.get("campanha") != campanha:
                continue
            t = dt.datetime.strptime(l["criado_em"], "%Y-%m-%d %H:%M:%S") - dt.timedelta(hours=3)
            sess.setdefault(t.date(), set()).add(l["sessao"])
    return {d: len(s) for d, s in sorted(sess.items())}


def rotulos(ax, barras, fmt="{:.0f}"):
    for b in barras:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), fmt.format(b.get_height()), ha="center", va="bottom", fontsize=9)


def main():
    ap = argparse.ArgumentParser(description="Gera o gráfico de 4 quadros do anúncio da Meta.")
    ap.add_argument("--csv", default=CSV_PADRAO)
    ap.add_argument("--acessos", default=None, help="acessos_*.csv (padrão: o mais novo da pasta dados_acessos)")
    ap.add_argument("--campanha", default="teste_11a13_11", help="utm_campaign usada para contar as visitas")
    ap.add_argument("--nome", default="teste_11a13_11", help="nome mostrado no título")
    ap.add_argument("--verba", type=float, default=50.0, help="verba total em reais (linha tracejada)")
    ap.add_argument("--meta-custo", type=float, default=0.35, help="meta de custo por visita (R$)")
    ap.add_argument("--desde", default=None, help="só leituras a partir desta data DD/MM/AAAA")
    ap.add_argument("--saida", default=PASTA_REL)
    a = ap.parse_args()

    leituras = ler_leituras(a.csv)
    if a.desde:
        d0 = dt.datetime.strptime(a.desde, "%d/%m/%Y").date()
        leituras = [l for l in leituras if dt.datetime.strptime(l["data"], "%d/%m/%Y").date() >= d0]
    if not leituras:
        print("ERRO: nenhuma leitura no CSV para essa seleção:", a.csv)
        return 1

    arq = a.acessos or max(glob.glob(os.path.join(PASTA_ACESSOS, "acessos_*.csv")), key=os.path.getmtime)
    vis = visitas_por_dia(arq, a.campanha)
    if not vis:
        print(f"AVISO: nenhuma visita da campanha '{a.campanha}' em {os.path.basename(arq)}; o quadro 2 ficará vazio.")

    ultimo = leituras[-1]
    gasto = ultimo["gasto"]
    visualiz = ultimo["resultados"]
    total_vis = sum(vis.values())
    custo_vis = gasto / total_vis if total_vis else 0
    custo_meta = gasto / visualiz if visualiz else 0

    agora = dt.datetime.now()
    fig, ax = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(f"Anuncio Meta {a.nome} x visitas reais do blog ({agora:%d/%m/%Y})", fontsize=15, fontweight="bold")

    x = [f"{l['data'][:5]} {l['hora']}" for l in leituras]
    ax[0][0].plot(x, [l["gasto"] for l in leituras], marker="o", color=AZUL)
    ax[0][0].axhline(a.verba, color=VERMELHO, linestyle="--")
    ax[0][0].set_title(f"Gasto acumulado (verba R$ {a.verba:g})")
    ax[0][0].tick_params(axis="x", rotation=60, labelsize=8)

    dias = [d.strftime("%d/%m") for d in vis]
    b = ax[0][1].bar(dias, list(vis.values()), color=VERDE)
    rotulos(ax[0][1], b)
    ax[0][1].set_title("Visitas reais vindas do anuncio por dia (site)")

    b = ax[1][0].bar(["Meta: visualizacoes", "Site: visitas reais"], [visualiz, total_vis], color=[AZUL, VERDE])
    rotulos(ax[1][0], b)
    ax[1][0].set_title("Meta x blog (total)")

    b = ax[1][1].bar(["Custo/visita real", "Custo/visualiz. Meta", "Meta de custo"], [custo_vis, custo_meta, a.meta_custo], color=[VERDE, AZUL, CINZA])
    rotulos(ax[1][1], b, "{:.2f}")
    ax[1][1].set_title("Custo por visita (R$)")

    fig.tight_layout(rect=(0, 0, 1, 0.95))
    os.makedirs(a.saida, exist_ok=True)
    saida = os.path.join(a.saida, f"GRAFICO_ANUNCIO_META_{agora:%d_%m_%Y_%Hh%M}.png")
    fig.savefig(saida, dpi=120)
    print("GRAFICO:", saida)
    print(f"Gasto R$ {gasto:.2f} | visualizacoes Meta {visualiz} | visitas reais {total_vis} | custo/visita R$ {custo_vis:.2f} | arquivo de acessos: {os.path.basename(arq)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
