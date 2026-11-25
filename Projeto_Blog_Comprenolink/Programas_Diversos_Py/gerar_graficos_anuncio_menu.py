# -*- coding: utf-8 -*-
"""gerar_graficos_anuncio_menu.py  (criado em 23/11/2026, alternativa 2 aprovada pelo dono)

Gera o PDF "Graficos_Anuncio_<campanha>_DD-MM-AA_HHhMM.pdf" do anúncio pago. É chamado pelo ATUALIZAR_PAINEL.bat, ou seja,
TODA VEZ que roda o menu principal [1] e [2] e o submenu [6] -> [1], [2], [3] e [7]. Também pode rodar sozinho.

DE ONDE VÊM OS DADOS (só leitura):
  - SITE (visitas e cliques para o Mercado Livre da campanha): o acessos_*.csv MAIS NOVO de Relatorios_Diarios_Anuncios\\dados_acessos.
    Entra sempre atualizado, pois o menu já gerou o relatório antes (1 visita = 1 sessão; dia no fuso de Brasília = UTC-3).
  - META (gasto, alcance, resultados SaidaML): o arquivo LEITURA_META_bf_26_entrada.csv (pasta graficos_diarios),
    com a ÚLTIMA LEITURA registrada, e a data dela aparece escrita no PDF. O programa NÃO lê a Meta sozinho.
    Para atualizar: peça ao Claude "atualize a Meta" (leva cerca de 1 minuto): ele lê o Gerenciador de Anúncios e grava no arquivo.

Se a leitura da Meta for de um dia anterior a hoje, o PDF avisa em vermelho.
Na pasta de saída fica só 1 PDF por dia (o mais novo); os anteriores do mesmo dia vão para old_bkp.
Uso: python -X utf8 gerar_graficos_anuncio_menu.py [--nao-avisar-erro]
"""
import csv
import datetime as dt
import glob
import os
import shutil
import sys
from collections import defaultdict

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Image, Paragraph, SimpleDocTemplate, Table, TableStyle

# ---- configuração do anúncio atual (mudar aqui se vier um anúncio novo, com "de acordo" do dono)
CAMP = "bf_26_entrada"
NOME = "bf_26_entrada"
VERBA = 240.0
INICIO, FIM = "20/11/2026", "22/12/2026"
ALERTA_SAIDA_MIN = 0.03   # alerta se taxa de saída < 3%
ALERTA_CUSTO_MAX = 3.0    # alerta se custo por clique de saída > R$ 3 (só sinal para conversar; decisão é do dono)

BASE = r"D:\Projeto_Blog_Comprenolink"
PASTA = os.path.join(BASE, "0- Pendencias", "1_Pendencias", "graficos_diarios")
CSV_META = os.path.join(PASTA, "LEITURA_META_bf_26_entrada.csv")
PASTA_ACESSOS = os.path.join(BASE, "Relatorios_Diarios_Anuncios", "dados_acessos")
AZ, VD, LA, VM = "#1f4e79", "#16a34a", "#e07b00", "#dc2626"


def d_br(txt):
    return dt.datetime.strptime(txt, "%d/%m/%Y").date()


def ler_meta():
    """Devolve (dias {data: dict}, total dict|None, lido_em str|None)."""
    dias, total, lido = {}, None, None
    if not os.path.exists(CSV_META):
        return dias, total, lido
    with open(CSV_META, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter=";"):
            item = {"gasto": float(r["gasto"]), "saidaml": int(r["saidaml"]), "alcance": int(r["alcance"]),
                    "freq": float(r["frequencia"]), "est": r["estimado"].strip().upper() == "S"}
            lido = r.get("lido_em") or lido
            if r["dia"].strip().upper() == "TOTAL":
                total = item
            else:
                dias[d_br(r["dia"])] = item
    return dias, total, lido


def ler_site():
    """Visitas (sessões distintas) e cliques para o ML por dia, só da campanha. Devolve (visitas, cliques, arquivo)."""
    arqs = sorted(glob.glob(os.path.join(PASTA_ACESSOS, "acessos_*.csv")), key=os.path.getmtime)
    if not arqs:
        return {}, {}, None
    sess_dia, vis = {}, defaultdict(set)
    cli = defaultdict(int)
    with open(arqs[-1], encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))

    def dia(r):
        return (dt.datetime.strptime(r["criado_em"][:19], "%Y-%m-%d %H:%M:%S") - dt.timedelta(hours=3)).date()
    for r in linhas:
        if r.get("tipo") == "visita" and r.get("campanha") == CAMP:
            s = r.get("sessao") or r.get("id")
            if s not in sess_dia:
                sess_dia[s] = dia(r)
            vis[sess_dia[s]].add(s)
    for r in linhas:
        if r.get("tipo") == "clique" and r.get("sessao") in sess_dia:
            cli[sess_dia[r["sessao"]]] += 1
    return {d: len(s) for d, s in vis.items()}, dict(cli), os.path.basename(arqs[-1])


def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def main():
    agora = dt.datetime.now()
    meta, total, lido = ler_meta()
    vis, cli, arq_site = ler_site()
    ini, fim = d_br(INICIO), d_br(FIM)
    dias = sorted({d for d in list(meta) + list(vis) if ini <= d <= fim})
    if not dias:
        print("AVISO: ainda não há dados da campanha para o PDF.")
        return 0
    rot = [d.strftime("%d/%m") for d in dias]
    gasto_dia = [meta.get(d, {}).get("gasto", 0) for d in dias]
    alc_dia = [meta.get(d, {}).get("alcance", 0) for d in dias]
    vis_dia = [vis.get(d, 0) for d in dias]
    cli_dia = [cli.get(d, 0) for d in dias]
    sml_dia = [meta.get(d, {}).get("saidaml", 0) for d in dias]
    gasto = total["gasto"] if total else sum(gasto_dia)
    alcance = total["alcance"] if total else sum(alc_dia)
    sml = total["saidaml"] if total else sum(sml_dia)
    est = (total or {}).get("est", False)
    v_tot, c_tot = sum(vis_dia), sum(cli_dia)
    taxa = c_tot / v_tot if v_tot else 0.0
    custo_cli = gasto / c_tot if c_tot else 0.0
    desatualizada = True
    if lido:
        try:
            desatualizada = dt.datetime.strptime(lido.split()[0], "%d/%m/%Y").date() < agora.date()
        except ValueError:
            pass

    fig, ax = plt.subplots(2, 2, figsize=(10, 7.2))
    fig.suptitle(f"Anúncio {NOME} (verba {brl(VERBA)}): gráficos de {agora:%d/%m/%Y}", fontweight="bold")
    b = ax[0][0].bar(rot, gasto_dia, color=AZ); ax[0][0].set_title("Gasto por dia (R$)")
    for x, v in zip(b, gasto_dia):
        ax[0][0].text(x.get_x() + x.get_width() / 2, v, f"{v:.2f}", ha="center", va="bottom", fontsize=8)
    b = ax[0][1].bar(rot, alc_dia, color=LA); ax[0][1].set_title("Pessoas alcançadas por dia (Meta)")
    for x, v in zip(b, alc_dia):
        ax[0][1].text(x.get_x() + x.get_width() / 2, v, str(v), ha="center", va="bottom", fontsize=8)
    xs = list(range(len(rot)))
    ax[1][0].bar([x - 0.2 for x in xs], vis_dia, 0.4, color=VD, label="Visitas no blog")
    ax[1][0].bar([x + 0.2 for x in xs], cli_dia, 0.4, color=AZ, label="Cliques para o ML")
    ax[1][0].set_xticks(xs); ax[1][0].set_xticklabels(rot); ax[1][0].legend(fontsize=7)
    ax[1][0].set_title("Site: visitas e cliques para o Mercado Livre")
    b = ax[1][1].bar(rot, sml_dia, color=VD); ax[1][1].set_title("SaidaML contado pela Meta (Pixel)")
    for x, v in zip(b, sml_dia):
        ax[1][1].text(x.get_x() + x.get_width() / 2, v, str(v), ha="center", va="bottom", fontsize=8)
    for a in ax.flat:
        a.tick_params(axis="x", labelsize=7)
    fig.tight_layout(rect=(0, 0, 1, 0.95))
    png = os.path.join(PASTA, "_grafico_tmp.png")
    fig.savefig(png, dpi=110); plt.close(fig)

    s = getSampleStyleSheet()
    T = ParagraphStyle("t", parent=s["Title"], fontSize=17, leading=21)
    H = ParagraphStyle("h", parent=s["Heading2"], fontSize=12, spaceBefore=10, textColor=colors.HexColor(AZ))
    P = ParagraphStyle("p", parent=s["BodyText"], fontSize=10, leading=14)
    C = ParagraphStyle("c", parent=P, fontSize=9.5, leading=13)
    CW = ParagraphStyle("cw", parent=C, textColor=colors.white)
    AV = ParagraphStyle("av", parent=P, textColor=colors.HexColor(VM))

    def tab(linhas, larg, cab):
        d = [[Paragraph(f"<b>{x}</b>", CW) for x in cab]] + [[Paragraph(x, C) for x in l] for l in linhas]
        t = Table(d, colWidths=larg, repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(AZ)), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                               ("VALIGN", (0, 0), (-1, -1), "TOP"), ("PADDING", (0, 0), (-1, -1), 5),
                               ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")])]))
        return t

    nome_pdf = f"Graficos_Anuncio_{NOME}_{agora:%d-%m-%y_%Hh%M}.pdf"
    destino = os.path.join(PASTA, nome_pdf)
    doc = SimpleDocTemplate(destino, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.5 * cm,
                            bottomMargin=1.5 * cm, title=f"Gráficos do anúncio {NOME}", author="comprenolink.net")
    e = [Paragraph(f"Gráficos do anúncio pago: {NOME}", T),
         Paragraph(f"Gerado em {agora:%d/%m/%Y às %Hh%M}. Campanha de {INICIO} a {FIM}. Só leitura: nada é alterado na Meta nem no site.", P),
         Paragraph(f"<b>Dados do site:</b> {arq_site or 'sem arquivo'} (1 visita = 1 sessão). "
                   f"<b>Dados da Meta:</b> última leitura registrada em {lido or 'nenhuma'}.", P)]
    if desatualizada:
        e.append(Paragraph("<b>ATENÇÃO: a leitura da Meta é de um dia anterior a hoje.</b> Para atualizar, peça ao Claude: \"atualize a Meta\".", AV))
    e += [Image(png, width=17 * cm, height=17 * cm * 7.2 / 10), Paragraph("Resumo em números", H)]
    e.append(tab([
        ["Gasto", f"<b>{brl(gasto)}</b> de {brl(VERBA)} ({gasto / VERBA * 100:.1f}%){' (estimado)' if est else ''}", "Dinheiro já usado, segundo a última leitura da Meta."],
        ["Pessoas alcançadas", f"<b>{alcance:,}</b>".replace(",", "."), "Quantas pessoas viram o anúncio (Meta)."],
        ["SaidaML na Meta (Pixel)", f"<b>{sml}</b>" + (f" ({brl(gasto / sml)} cada)" if sml else ""), "Idas ao Mercado Livre que o Pixel contou (só quem aceitou o aviso de cookies)."],
        ["Visitas no blog (site)", f"<b>{v_tot}</b>", "Gente que chegou pelo anúncio (campanha " + CAMP + ")."],
        ["Cliques para o ML (site)", f"<b>{c_tot}</b>", "Clique de saída = foi do blog ao Mercado Livre, o que gera comissão."],
        ["Taxa de saída (site)", f"<b>{taxa * 100:.1f}%</b> ({c_tot} de {v_tot})", f"Sinal de alerta: abaixo de {ALERTA_SAIDA_MIN * 100:.0f}%."],
        ["Custo por clique de saída", f"<b>{brl(custo_cli)}</b>" if c_tot else "não calculável", f"Sinal de alerta: acima de {brl(ALERTA_CUSTO_MAX)}."]],
        [4.6 * cm, 5.6 * cm, 7.2 * cm], ("Item", "Valor", "O que significa")))
    sinais = []
    if v_tot and taxa < ALERTA_SAIDA_MIN:
        sinais.append("a taxa de saída está abaixo do alerta")
    if c_tot and custo_cli > ALERTA_CUSTO_MAX:
        sinais.append("o custo por clique de saída está acima do alerta")
    e += [Paragraph("Leitura", H),
          Paragraph(("Sinal de alerta: " + " e ".join(sinais) + ". " if sinais else "Nenhum sinal de alerta nos números acima. ")
                    + "Os alertas são só um sinal para conversar; <b>a decisão de manter, ajustar ou pausar é do dono e do Claude, juntos.</b> "
                      "Amostra pequena: poucos cliques, concentrados em poucos dias.", P)]
    doc.build(e)
    os.remove(png)
    # só 1 PDF por dia na pasta: os anteriores do mesmo dia vão para old_bkp
    prefixo = f"Graficos_Anuncio_{NOME}_{agora:%d-%m-%y}_"
    bkp = os.path.join(PASTA, "old_bkp")
    for nome in os.listdir(PASTA):
        if nome.startswith(prefixo) and nome.endswith(".pdf") and nome != nome_pdf:
            os.makedirs(bkp, exist_ok=True)
            try:
                os.replace(os.path.join(PASTA, nome), os.path.join(bkp, nome))
            except OSError:
                pass
    print("PDF DE GRAFICOS DO ANUNCIO:", destino)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # o menu nunca pode parar por causa deste PDF
        print("AVISO: não foi possível gerar o PDF de gráficos do anúncio:", exc)
        sys.exit(0 if "--nao-avisar-erro" in sys.argv else 1)
