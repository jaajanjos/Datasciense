# -*- coding: utf-8 -*-
r"""Lê o histórico diário do anúncio Meta (CSV) e gera o PDF do dia com a tabela acumulada.
Uso: python -X utf8 LEITURA_ANUNCIO_META.py   (gera LEITURA_ANUNCIO_META_DD_MM_AAAA_HHhMM_DIARIO.pdf)
CSV: ...\4_Relatorio_Ativ_Claude_no_Blog\LEITURA_ANUNCIO_META_historico.csv
Colunas: data;hora;gasto;impressoes;alcance;resultados;status;observacao   (gasto em reais, ponto decimal)"""
import csv, datetime, os
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
CSV = os.path.join(PASTA, "LEITURA_ANUNCIO_META_historico.csv")
ORC = 50.0
def f(x): return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
linhas = list(csv.DictReader(open(CSV, encoding="utf-8-sig"), delimiter=";"))
agora = datetime.datetime.now()
saida = os.path.join(PASTA, f"LEITURA_ANUNCIO_META_{agora:%d_%m_%Y_%Hh%M}_DIARIO.pdf")
s = getSampleStyleSheet()
h = ParagraphStyle("h", parent=s["Title"], fontSize=17)
h2 = ParagraphStyle("h2", parent=s["Heading2"], fontSize=12, spaceBefore=10)
p = ParagraphStyle("p", parent=s["BodyText"], fontSize=10, leading=14)
doc = SimpleDocTemplate(saida, pagesize=landscape(A4), leftMargin=1.5*cm, rightMargin=1.5*cm, topMargin=1.5*cm, bottomMargin=1.5*cm,
                        title="Acompanhamento diário do anúncio Meta")
dados = [["Data", "Hora", "Gasto", "% da verba", "Impressões", "Alcance", "Visualiz. da página", "Custo/visualiz.", "Status", "Observação"]]
ant = None
for l in linhas:
    g, r = float(l["gasto"]), int(l["resultados"])
    dados.append([l["data"], l["hora"], f(g), f"{g/ORC*100:.1f}%", l["impressoes"], l["alcance"], str(r), f(g/r) if r else "-", l["status"], l["observacao"]])
u = linhas[-1]; g = float(u["gasto"]); r = int(u["resultados"])
t = Table(dados, repeatRows=1)
t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,0),colors.HexColor("#1f2937")),("TEXTCOLOR",(0,0),(-1,0),colors.white),
    ("GRID",(0,0),(-1,-1),0.5,colors.grey),("FONTSIZE",(0,0),(-1,-1),8.5),("VALIGN",(0,0),(-1,-1),"MIDDLE"),
    ("ROWBACKGROUNDS",(0,1),(-1,-1),[colors.white,colors.HexColor("#f3f4f6")]),("PADDING",(0,0),(-1,-1),4)]))
e = [Paragraph("Acompanhamento diário do anúncio Meta – teste_11a13_11_anuncio", h),
     Paragraph(f"Gerado em {agora:%d/%m/%Y às %Hh%M}. Verba total: {f(ORC)} (vitalício). Dados lidos no Gerenciador de Anúncios da Meta.", p),
     Paragraph("Situação atual", h2),
     Paragraph(f"Gasto: <b>{f(g)}</b> de {f(ORC)} (<b>{g/ORC*100:.1f}%</b>) · saldo restante: <b>{f(ORC-g)}</b> · {u['resultados']} visualizações da página"
               f"{' · custo por visualização ' + f(g/r) if r else ''}.", p),
     Paragraph("Dia a dia (acumulado)", h2), t, Spacer(1, 8),
     Paragraph("Observação: o custo por visualização usa as visualizações da página que a Meta conta (cliques em 7 dias ou visualização em 1 dia); "
               "confirmar as visitas reais no Google Analytics (utm do anúncio).", p)]
doc.build(e)
print(saida)
