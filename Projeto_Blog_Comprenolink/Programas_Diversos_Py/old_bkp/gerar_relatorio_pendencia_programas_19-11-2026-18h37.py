# -*- coding: utf-8 -*-
"""Relatorio diario da conversa BLOG - Pendencia e ajustes em programas.
Regra do dono: executado com sucesso fica SO no dia; no dia seguinte sai.
Pendencias ficam ate a solucao. Uma unica versao na pasta (anterior -> old_bkp)."""
import os, shutil, glob
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
HOJE = datetime.now()
HOJE_S = HOJE.strftime("%d/%m/%Y")

# (data DD/MM/AAAA, atividade, situacao)  -> aparece so se data == hoje
EXECUTADO = [
]

# ficam ate a solucao: (atividade, situacao / quem / quando)
PENDENCIAS = [
    ("Sincronizar Reels do Instagram na Pagina Facebook Comprenolink - hoje: Reels de 06/11 e 09/11",
     "Hoje 19/11 as 20h. Eu tento publicar (autorizado pelo dono); se travar na janela do video, oriento passo a passo."),
    ("Sincronizar os demais Reels (11/11, 13/11, 16/11, 18/11 e os novos do dia a dia)",
     "Max. 2 por dia, a partir de sex 20/11 as 20h, conforme a agenda. Ja publicados: 02/11 e 04/11."),
    ("Reels sem video localizado (12/11 JBL e mais 2 do Instagram)",
     "Aguardando o dono indicar onde esta o video."),
]

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
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    for f in glob.glob(os.path.join(PASTA, "RELATORIO_PENDENCIA_PROGRAMAS_*.pdf")):
        shutil.move(f, os.path.join(PASTA, "old_bkp", os.path.basename(f)))
    nome = "RELATORIO_PENDENCIA_PROGRAMAS_%s.pdf" % HOJE.strftime("%d_%m_%Y_%Hh%M")
    caminho = os.path.join(PASTA, nome)
    ss = getSampleStyleSheet()
    h = ParagraphStyle("h", parent=ss["Heading2"], spaceBefore=10)
    doc = SimpleDocTemplate(caminho, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36,
                            title="Relatorio Pendencia e ajustes em programas")
    el = [Paragraph("Relatorio - BLOG: Pendencia e ajustes em programas", ss["Title"]),
          Paragraph("Gerado em %s as %s. Regra: executado com sucesso fica so no dia e sai no dia seguinte; "
                    "pendencias ficam ate a solucao." % (HOJE_S, HOJE.strftime("%Hh%M")), ss["BodyText"]),
          Paragraph("Executado hoje (%s)" % HOJE_S, h)]
    ex = [(a, s) for d, a, s in EXECUTADO if d == HOJE_S]
    el.append(tabela(ex, ["Atividade", "Situacao"], [200, 327]) if ex else Paragraph("Nada executado hoje ate o momento.", ss["BodyText"]))
    el.append(Paragraph("Pendencias (ficam ate a solucao)", h))
    el.append(tabela(PENDENCIAS, ["Atividade", "Situacao / quem / quando"], [230, 297]))
    doc.build(el)
    print(caminho)

if __name__ == "__main__":
    main()
