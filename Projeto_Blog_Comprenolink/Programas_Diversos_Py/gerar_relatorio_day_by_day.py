# -*- coding: utf-8 -*-
"""Relatorio da conversa BLOG - Day by Day pontuais duvidas soltas.
Regra do dono (19/11/2026): o PDF traz SO pendencias e atividades a realizar.
Concluido e retirado. Toda linha tem Status, Quem e Data e horario
(se nao houver data: 'Previsto: dia/hora'). Uma unica versao na pasta (anterior -> old_bkp)."""
import os, shutil, glob, sys
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
HOJE = datetime.now()
HOJE_S = HOJE.strftime("%d/%m/%Y")

# (atividade, status 'Pendente', quem, data e horario)  -> so pendencias / a realizar
PENDENCIAS = []

def tabela(linhas, cab, larg):
    st = getSampleStyleSheet()["BodyText"]; st.fontSize = 9; st.leading = 11
    dados = [[Paragraph("<b>%s</b>" % c, st) for c in cab]]
    for l in linhas:
        dados.append([Paragraph(x, st) for x in l])
    t = Table(dados, colWidths=larg, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t

def main():
    for l in PENDENCIAS:
        if len(l) != 4 or not all(str(x).strip() for x in l):
            sys.exit("Linha incompleta (precisa Atividade, Status, Quem, Data e horario): %r" % (l,))
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    for pad in ("BLOG- Day by Day pontuais duvidas soltas_*.pdf", "BLOG- Day by Day_*.pdf", "RELATORIO_DAY_BY_DAY_*.pdf"):
        for f in glob.glob(os.path.join(PASTA, pad)):
            shutil.move(f, os.path.join(PASTA, "old_bkp", os.path.basename(f)))
    nome = "BLOG- Day by Day pontuais duvidas soltas_%s.pdf" % HOJE.strftime("%d_%m_%Y_%Hh%M")
    caminho = os.path.join(PASTA, nome)
    ss = getSampleStyleSheet()
    h = ParagraphStyle("h", parent=ss["Heading2"], spaceBefore=10)
    doc = SimpleDocTemplate(caminho, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36,
                            title="BLOG- Day by Day pontuais duvidas soltas")
    el = [Paragraph("BLOG- Day by Day pontuais duvidas soltas", ss["Title"]),
          Paragraph("Gerado em %s as %s. So pendencias e atividades a realizar; concluido e retirado."
                    % (HOJE_S, HOJE.strftime("%Hh%M")), ss["BodyText"]),
          Paragraph("Pendencias e atividades a realizar", h)]
    el.append(tabela(PENDENCIAS, ["Atividade", "Status", "Quem", "Data e horario"], [210, 70, 90, 157]) if PENDENCIAS
              else Paragraph("Nenhuma pendencia no momento.", ss["BodyText"]))
    doc.build(el)
    print(caminho)

if __name__ == "__main__":
    main()
