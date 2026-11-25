# -*- coding: utf-8 -*-
r"""VISAO_GERAL_ANUNCIO_PAGO.py  (criado em 24/11/2026 a pedido do dono)

PARA QUE SERVE: registrar, num PDF só, a visão geral de TODO o anúncio pago desde o início
(teste de 11 a 13/11 + anúncio atual bf_26_entrada): quanto foi investido, o que a Meta entregou,
o que chegou de verdade ao blog, quanto custou cada visita e cada clique para o Mercado Livre,
a linha do tempo das decisões, a conclusão e os pontos de atenção.

Ele só LÊ arquivos já gravados (não acessa a Meta nem o site):
  - Meta: LEITURA_ANUNCIO_META_historico*.csv (última leitura de cada campanha)
  - Blog: acessos_*.csv mais novo e compras_atribuidas_*.csv mais novo (Relatorios_Diarios_Anuncios\dados_acessos)
  - Dia a dia do anúncio atual: DADOS_GERENCIAIS_ANUNCIO_META_<nome>.csv
  - Linha do tempo: LINHA_DO_TEMPO_ANUNCIO_PAGO.csv (acrescente uma linha a cada fato novo)

Saídas (pasta 0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog):
  - VISAO_GERAL_ANUNCIO_PAGO_DD_MM_AAAA_HHhMM.pdf  (fica só 1 versão; as antigas vão para old_bkp)
  - VISAO_GERAL_ANUNCIO_PAGO.csv                    (1 linha por campanha + TOTAL, refeito a cada execução)

Roda sozinho no fim do GERA_GRAFICO_ANUNCIO_META.py, ou à parte:
  python -X utf8 "D:\Projeto_Blog_Comprenolink\Programas_Diversos_Py\VISAO_GERAL_ANUNCIO_PAGO.py"
"""
import csv
import datetime as dt
import glob
import io
import os
import re
import shutil
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["text.parse_math"] = False

PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
PASTA_ACESSOS = r"D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\dados_acessos"
TIMELINE = os.path.join(PASTA, "LINHA_DO_TEMPO_ANUNCIO_PAGO.csv")

# Campanhas pagas desde o início (acrescentar aqui a próxima campanha paga)
CAMPANHAS = [
    {"nome": "teste_11a13_11", "utm": "teste_11a13_11", "periodo": "11/11 a 16/11/2026", "verba": 50.0,
     "historico": "LEITURA_ANUNCIO_META_historico.csv", "resultado": "visualização da página",
     "objetivo": "Tráfego"},
    {"nome": "bf_26_entrada", "utm": "bf_26_entrada", "periodo": "20/11 a 22/12/2026", "verba": 240.0,
     "historico": "LEITURA_ANUNCIO_META_historico_120254860764050057.csv", "resultado": "SaidaML (clique para o ML)",
     "objetivo": "Vendas (Pixel)", "por_dia": "DADOS_GERENCIAIS_ANUNCIO_META_bf_26_entrada.csv"},
]
COLS = ["campanha", "periodo", "objetivo", "verba", "gasto", "impressoes", "alcance", "cliques_link", "resultados_meta",
        "tipo_resultado", "visitas_reais", "visitantes_unicos", "cliques_saida", "taxa_saida_pct", "custo_por_visita",
        "custo_por_clique_saida", "compras_atribuidas", "situacao", "ultima_leitura_meta"]


def reais(x):
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def mais_novo(padrao):
    arqs = glob.glob(os.path.join(PASTA_ACESSOS, padrao))
    return max(arqs, key=os.path.getmtime) if arqs else None


def ultima_meta(arquivo):
    """Última linha do histórico da Meta (tolerando ';' dentro da observação)."""
    caminho = os.path.join(PASTA, arquivo)
    if not os.path.exists(caminho):
        return None
    ult = None
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        for n, c in enumerate(csv.reader(f, delimiter=";")):
            if n == 0 or not c or not c[0].strip() or len(c) < 7:
                continue
            ult = c
    if not ult:
        return None
    obs = "; ".join(x for x in ult[7:] if x.strip())
    m = re.search(r"cliques no link (\d+)", obs, re.I)
    return {"quando": f"{ult[0]} {ult[1]}", "gasto": float(ult[2].replace(",", ".")), "impressoes": int(float(ult[3] or 0)),
            "alcance": int(float(ult[4] or 0)), "resultados": int(float(ult[5] or 0)), "status": ult[6],
            "cliques_link": int(m.group(1)) if m else None}


def site(arquivo, utm):
    """Visitas (sessões), visitantes únicos e cliques de saída da campanha no blog."""
    sess, vis, cli = set(), set(), 0
    with open(arquivo, encoding="utf-8-sig", newline="") as f:
        for l in csv.DictReader(f, delimiter=";"):
            if l.get("campanha") != utm:
                continue
            if l.get("tipo") == "visita":
                sess.add(l["sessao"])
                vis.add(l["visitante"])
            elif l.get("tipo") == "clique":
                cli += 1
    return len(sess), len(vis), cli


def compras(arquivo, utm):
    if not arquivo:
        return 0
    with open(arquivo, encoding="utf-8-sig", newline="") as f:
        return sum(1 for l in csv.DictReader(f, delimiter=";") if l.get("campanha") == utm)


def criterio(taxa, custo_cli, gasto):
    if not gasto:
        return "SEM AVALIAÇÃO"
    if taxa >= 8 and custo_cli is not None and custo_cli < 1:
        return "APROVADO"
    if taxa < 3 or custo_cli is None or custo_cli > 3:
        return "ALERTA"
    return "EM OBSERVAÇÃO"


def montar():
    arq_acc, arq_cmp = mais_novo("acessos_*.csv"), mais_novo("compras_atribuidas_*.csv")
    linhas = []
    for c in CAMPANHAS:
        m = ultima_meta(c["historico"]) or {"quando": "-", "gasto": 0.0, "impressoes": 0, "alcance": 0, "resultados": 0,
                                            "status": "sem leitura", "cliques_link": None}
        v, u, s = site(arq_acc, c["utm"])
        g = m["gasto"]
        taxa = s / v * 100 if v else 0.0
        cc = g / s if s else None
        linhas.append({"campanha": c["nome"], "periodo": c["periodo"], "objetivo": c["objetivo"], "verba": c["verba"],
                       "gasto": g, "impressoes": m["impressoes"], "alcance": m["alcance"], "cliques_link": m["cliques_link"],
                       "resultados_meta": m["resultados"], "tipo_resultado": c["resultado"], "visitas_reais": v,
                       "visitantes_unicos": u, "cliques_saida": s, "taxa_saida_pct": taxa,
                       "custo_por_visita": g / v if v else None, "custo_por_clique_saida": cc,
                       "compras_atribuidas": compras(arq_cmp, c["utm"]),
                       "situacao": f"{m['status']} / {criterio(taxa, cc, g)}", "ultima_leitura_meta": m["quando"]})
    t = {k: sum((l[k] or 0) for l in linhas) for k in ("verba", "gasto", "impressoes", "alcance", "visitas_reais",
                                                      "visitantes_unicos", "cliques_saida", "compras_atribuidas")}
    t["cliques_link"] = sum(l["cliques_link"] or 0 for l in linhas)
    t["taxa_saida_pct"] = t["cliques_saida"] / t["visitas_reais"] * 100 if t["visitas_reais"] else 0
    t["custo_por_visita"] = t["gasto"] / t["visitas_reais"] if t["visitas_reais"] else None
    t["custo_por_clique_saida"] = t["gasto"] / t["cliques_saida"] if t["cliques_saida"] else None
    t.update({"campanha": "TOTAL", "periodo": "11/11/2026 até hoje", "objetivo": "", "resultados_meta": "",
              "tipo_resultado": "", "situacao": "", "ultima_leitura_meta": ""})
    return linhas, t, os.path.basename(arq_acc), os.path.basename(arq_cmp) if arq_cmp else "-"


def gravar_csv(linhas, total):
    fmt = lambda v: f"{v:.2f}" if isinstance(v, float) else ("" if v is None else v)
    with open(os.path.join(PASTA, "VISAO_GERAL_ANUNCIO_PAGO.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(COLS)
        for l in linhas + [total]:
            w.writerow([fmt(l.get(k)) for k in COLS])


def ler_timeline():
    if not os.path.exists(TIMELINE):
        return []
    with open(TIMELINE, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def ler_por_dia():
    for c in CAMPANHAS:
        if c.get("por_dia") and os.path.exists(os.path.join(PASTA, c["por_dia"])):
            with open(os.path.join(PASTA, c["por_dia"]), encoding="utf-8-sig", newline="") as f:
                return c["nome"], list(csv.DictReader(f, delimiter=";"))
    return None, []


def grafico(linhas):
    fig, ax = plt.subplots(1, 3, figsize=(11, 3.2))
    nomes = [l["campanha"] for l in linhas]
    cores = ["#9ca3af", "#2563eb"]
    for i, (k, tit, fmt) in enumerate([("gasto", "Investido (R$)", "{:.2f}"), ("custo_por_visita", "Custo por visita real (R$)", "{:.2f}"),
                                       ("taxa_saida_pct", "Visitas que clicaram p/ o ML (%)", "{:.1f}")]):
        vals = [l[k] or 0 for l in linhas]
        b = ax[i].bar(nomes, vals, color=cores[:len(vals)])
        for r in b:
            ax[i].text(r.get_x() + r.get_width() / 2, r.get_height(), fmt.format(r.get_height()), ha="center", va="bottom", fontsize=9)
        ax[i].set_title(tit, fontsize=10)
        ax[i].tick_params(labelsize=8)
    ax[1].axhline(0.35, color="#dc2626", linestyle="--", linewidth=1)
    ax[2].axhline(8, color="#16a34a", linestyle="--", linewidth=1)
    fig.tight_layout()
    buf = io.BytesIO()
    fig.savefig(buf, format="png", dpi=150)
    plt.close(fig)
    buf.seek(0)
    return buf


def conclusao(linhas, t):
    a = linhas[-1]
    txt = [f"Desde 11/11/2026 foram investidos <b>{reais(t['gasto'])}</b> de {reais(t['verba'])} autorizados "
           f"({t['gasto'] / t['verba'] * 100:.0f}%). O anúncio pago trouxe <b>{t['visitas_reais']} visitas reais</b> ao blog "
           f"({t['visitantes_unicos']} pessoas) e <b>{t['cliques_saida']} cliques para o Mercado Livre</b>; "
           f"compras atribuídas até agora: <b>{t['compras_atribuidas']}</b>."]
    if len(linhas) > 1:
        tst = linhas[0]
        txt.append(f"O teste trouxe visita barata ({reais(tst['custo_por_visita'] or 0)} por visita), mas quase ninguém clicou "
                   f"para o ML ({tst['taxa_saida_pct']:.1f}%). O anúncio atual ({a['campanha']}) inverte isso: visita mais cara "
                   f"({reais(a['custo_por_visita'] or 0)}), porém {a['taxa_saida_pct']:.1f}% das visitas clicam para o ML, "
                   f"o que é o que gera comissão.")
    cc = a["custo_por_clique_saida"]
    txt.append(f"Situação atual: <b>{a['situacao']}</b>. Custo por clique de saída {reais(cc) if cc else '-'} "
               f"(meta: abaixo de R$ 1; alerta acima de R$ 3). Os critérios são só alerta: qualquer mudança no anúncio é decidida junto com o dono.")
    att = ["Nenhuma compra atribuída ao anúncio até agora. A venda no ML Afiliados só é paga cerca de 60 dias depois e parte pode não confirmar.",
           "A Meta conta menos cliques de saída (SaidaML) do que o blog, porque o Pixel só funciona para quem aceita o aviso de cookies; o número do blog é o mais fiel.",
           "Sem a chave da API da Meta, a leitura da Meta é feita à mão no Gerenciador; nos dias em que a Meta não abriu dia a dia, o valor ficou somado no último dia lido.",
           "Arte e texto do anúncio ainda são de Black Friday: trocar para Natal por volta de 28/11 (decidir junto).",
           f"Limite de gastos da conta: R$ 200/mês (reinicia dia 1). Saldo da verba do anúncio atual: {reais(max(a['verba'] - a['gasto'], 0))}."]
    return txt, att


def gerar_pdf(agora=None):
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Image, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    agora = agora or dt.datetime.now()
    linhas, t, arq_acc, arq_cmp = montar()
    gravar_csv(linhas, t)
    antigos = glob.glob(os.path.join(PASTA, "VISAO_GERAL_ANUNCIO_PAGO_*.pdf"))
    if antigos:
        os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
        for x in antigos:
            shutil.move(x, os.path.join(PASTA, "old_bkp", os.path.basename(x)))
    saida = os.path.join(PASTA, f"VISAO_GERAL_ANUNCIO_PAGO_{agora:%d_%m_%Y_%Hh%M}.pdf")

    s = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=s["Title"], fontSize=18)
    h2 = ParagraphStyle("h2", parent=s["Heading2"], fontSize=12.5, spaceBefore=8, textColor=colors.HexColor("#1f2937"))
    p = ParagraphStyle("p", parent=s["BodyText"], fontSize=9.5, leading=13)
    pc = ParagraphStyle("pc", parent=s["BodyText"], fontSize=8, leading=10)
    doc = SimpleDocTemplate(saida, pagesize=landscape(A4), leftMargin=1.4 * cm, rightMargin=1.4 * cm,
                            topMargin=1.2 * cm, bottomMargin=1.2 * cm, title="Visão geral do anúncio pago")

    pcab = ParagraphStyle("pcab", parent=s["BodyText"], fontSize=7.5, leading=9, textColor=colors.white)

    def tabela(dados, larg, cab="#1f2937"):
        dados = [[Paragraph(str(x), pcab) for x in dados[0]]] + dados[1:]
        tb = Table(dados, colWidths=larg, repeatRows=1)
        tb.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor(cab)), ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
                                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("FONTSIZE", (0, 0), (-1, -1), 8),
                                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("PADDING", (0, 0), (-1, -1), 3),
                                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")])]))
        return tb

    r = lambda v: reais(v) if isinstance(v, float) else "-"
    e = [Paragraph("Visão geral do anúncio pago (Meta) – desde o início", h1),
         Paragraph(f"Gerado em {agora:%d/%m/%Y às %Hh%M}. Para que serve: registrar num lugar só tudo o que o anúncio pago "
                   f"já custou e trouxe ao blog, desde o teste de 11/11, para decidir com números reais.", p),
         Paragraph("Resumo geral", h2)]
    resumo = [["Investido", "Verba autorizada", "Impressões", "Visitas reais", "Pessoas", "Cliques p/ o ML", "% que clicou",
               "Custo/visita", "Custo/clique p/ ML", "Compras"],
              [reais(t["gasto"]), reais(t["verba"]), f"{t['impressoes']:,}".replace(",", "."), t["visitas_reais"],
               t["visitantes_unicos"], t["cliques_saida"], f"{t['taxa_saida_pct']:.1f}%", r(t["custo_por_visita"]),
               r(t["custo_por_clique_saida"]), t["compras_atribuidas"]]]
    e += [tabela(resumo, [2.5 * cm] * 10, "#2563eb"), Spacer(1, 6), Paragraph("Por campanha", h2)]
    cab = ["Campanha", "Período", "Objetivo", "Verba", "Gasto", "Impressões", "Alcance", "Cliques no link", "Resultado Meta",
           "Visitas reais", "Pessoas", "Cliques p/ ML", "% clicou", "Custo/visita", "Custo/clique ML", "Situação"]
    dados = [cab] + [[l["campanha"], Paragraph(l["periodo"], pc), l["objetivo"], reais(l["verba"]), reais(l["gasto"]),
                      l["impressoes"], l["alcance"], l["cliques_link"] if l["cliques_link"] is not None else "-",
                      Paragraph(f"{l['resultados_meta']} ({l['tipo_resultado']})", pc), l["visitas_reais"],
                      l["visitantes_unicos"], l["cliques_saida"], f"{l['taxa_saida_pct']:.1f}%", r(l["custo_por_visita"]),
                      r(l["custo_por_clique_saida"]), Paragraph(l["situacao"], pc)] for l in linhas]
    e.append(tabela(dados, [2.4*cm, 1.9*cm, 1.8*cm, 1.4*cm, 1.4*cm, 1.5*cm, 1.3*cm, 1.4*cm, 2.4*cm, 1.4*cm, 1.2*cm, 1.3*cm,
                            1.2*cm, 1.4*cm, 1.5*cm, 2.3*cm]))
    e += [Spacer(1, 6), Image(grafico(linhas), width=25 * cm, height=7.3 * cm),
          Paragraph("Linha tracejada vermelha = meta de custo por visita (R$ 0,35). Linha verde = meta de 8% das visitas clicando para o ML.", pc)]

    txt, att = conclusao(linhas, t)
    e += [PageBreak(), Paragraph("Conclusão de performance", h2)] + [Paragraph(x, p) for x in txt]
    e += [Paragraph("Pontos de atenção", h2)] + [Paragraph("• " + x, p) for x in att]

    nome, dias = ler_por_dia()
    if dias:
        e.append(Paragraph(f"Dia a dia do anúncio atual ({nome})", h2))
        d = [["Data", "Gasto no dia", "Gasto acumulado", "Impressões", "Resultado Meta", "Visitas reais", "Pessoas", "Cliques p/ ML"]]
        d += [[x["data"], reais(float(x["gasto_dia"] or 0)), reais(float(x["gasto_acumulado"] or 0)), x["impressoes"],
               x.get("resultados_meta", ""), x["visitas_reais"], x["visitantes_unicos"], x["cliques_saida"]] for x in dias]
        e.append(tabela(d, [2.6 * cm, 2.6 * cm, 3 * cm, 2.4 * cm, 2.6 * cm, 2.4 * cm, 2 * cm, 2.4 * cm]))

    tl = ler_timeline()
    if tl:
        e.append(Paragraph("Linha do tempo (decisões e leituras)", h2))
        d = [["Data", "Campanha", "O que aconteceu"]] + [[x["data"], x["campanha"], Paragraph(x["evento"], pc)] for x in tl]
        e.append(tabela(d, [2.4 * cm, 3.2 * cm, 20.5 * cm]))
    e += [Spacer(1, 6), Paragraph(f"Fontes: histórico de leituras da Meta, {arq_acc} (visitas e cliques do blog), {arq_cmp} "
                                  f"(compras). Visita = sessão no blog com a etiqueta da campanha.", pc)]
    doc.build(e)
    return saida


if __name__ == "__main__":
    print("VISAO GERAL:", gerar_pdf())
    sys.exit(0)
