# -*- coding: utf-8 -*-
"""Relatorio diario da conversa BLOG - Day by Day pontuais duvidas soltas.
Regra do dono: executado com sucesso fica SO no dia; no dia seguinte sai.
Pendencias ficam ate a solucao. Uma unica versao na pasta (anterior -> old_bkp)."""
import os, shutil, glob
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
HOJE = datetime.now()
HOJE_S = HOJE.strftime("%d/%m/%Y")

# (data DD/MM/AAAA, atividade, situacao)  -> aparece so se data == hoje
EXECUTADO = [
    ("19/11/2026", "Regra do relatorio (so executados de hoje + pendencias abertas)",
     "Registrada na memoria e repassada as conversas Atividades Claude e Planejamento, WhatsApp e Instagram e Pendencia e ajustes em programas."),
    ("19/11/2026", "Instagram compre.no.link conferido (so leitura, no Chrome)",
     "Perfil publico, aparece no Google e 'Mostrar sugestoes de contas nos perfis' ligado. Nada foi alterado."),
    ("19/11/2026", "Regra 'resposta completa de uma vez' registrada",
     "Feita por mim na memoria do projeto."),
]

# ficam ate a solucao: (atividade, situacao / quem / quando)
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
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    for pad in ("BLOG- Day by Day pontuais duvidas soltas_*.pdf", "BLOG- Day by Day_*.pdf", "RELATORIO_DAY_BY_DAY_*.pdf"):
        for f in glob.glob(os.path.join(PASTA, pad)):
            shutil.move(f, os.path.join(PASTA, "old_bkp", os.path.basename(f)))
    nome = "BLOG- Day by Day pontuais duvidas soltas_%s.pdf" % HOJE.strftime("%d_%m_%Y_%Hh%M")
    caminho = os.path.join(PASTA, nome)
    ss = getSampleStyleSheet()
    h = ParagraphStyle("h", parent=ss["Heading2"], spaceBefore=10)
    doc = SimpleDocTemplate(caminho, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36,
                            title="Relatorio Day by Day")
    el = [Paragraph("Relatorio - BLOG: Day by Day (duvidas pontuais)", ss["Title"]),
          Paragraph("Gerado em %s as %s. Regra: executado com sucesso fica so no dia e sai no dia seguinte; "
                    "pendencias ficam ate a solucao." % (HOJE_S, HOJE.strftime("%Hh%M")), ss["BodyText"]),
          Paragraph("Executado hoje (%s)" % HOJE_S, h)]
    ex = [(a, s) for d, a, s in EXECUTADO if d == HOJE_S]
    el.append(tabela(ex, ["Atividade", "Situacao"], [200, 327]) if ex else Paragraph("Nada executado hoje.", ss["BodyText"]))
    el.append(Paragraph("Pendencias (ficam ate a solucao)", h))
    el.append(tabela(PENDENCIAS, ["Atividade", "Situacao / quem / quando"], [230, 297]) if PENDENCIAS
              else Paragraph("Nenhuma pendencia.", ss["BodyText"]))
    doc.build(el)
    print(caminho)

if __name__ == "__main__":
    main()
