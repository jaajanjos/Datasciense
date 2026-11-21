# -*- coding: utf-8 -*-
"""Relatorio da conversa BLOG - Pendencia e ajustes em programas.
Regra do dono (19/11/2026): so PENDENCIAS e atividades a realizar; concluida e RETIRADA.
Toda linha: Atividade | Status | Quem | Data e horario (nunca sem data/hora; sem data = "Previsto: dia/hora").
Uma unica versao na pasta (anterior -> old_bkp)."""
import os, re, sys, shutil, glob
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
HOJE = datetime.now()

# (atividade, status, quem, data e horario)   status: Pendente | Concluido (concluido nao entra no PDF)
ATIVIDADES = [
    ("<b>Corrigir a legenda da foto do Fone JBL Tune 730 (Instagram, 19h00 de 20/11).</b> Ela ainda termina com 9 hashtags genericas; o padrao e so comprenolink.net e #comprenolinkblog. <b>Para que:</b> nao divulgar outros sites e marcas e levar o trafego so para o blog.",
     "Pendente", "Voce edita pelo app do celular, ou me pede para excluir e publicar de novo", "Previsto: 20/11/2026 as 20h"),
    ("<b>Publicar na Pagina o Reel de 13/11 (e o novo de 23/11).</b> Mesma rotina acima. <b>Para que:</b> manter a Pagina em dia com o Instagram, ate completar todos os Reels.",
     "Pendente", "Voce escolhe o video; eu publico", "23/11/2026 as 20h"),
    ("<b>Publicar na Pagina o Reel de 16/11 (e o novo de 24/11).</b> <b>Para que:</b> mesma finalidade: Pagina sempre com conteudo novo.",
     "Pendente", "Voce escolhe o video; eu publico", "24/11/2026 as 20h"),
    ("<b>Publicar na Pagina o Reel de 18/11 (e o novo de 25/11).</b> <b>Para que:</b> completar os Reels que ficaram para tras.",
     "Pendente", "Voce escolhe o video; eu publico", "25/11/2026 as 20h"),
    ("<b>Publicar na Pagina os Reels novos seguintes (no maximo 2 por dia).</b> <b>Para que:</b> a Pagina acompanhar o Instagram dia a dia ate o fim de dezembro, sem acumular atraso.",
     "Pendente", "Voce escolhe o video; eu publico", "Previsto: de 26/11/2026 a 23/12/2026, sempre as 20h"),
    ("<b>Reels sem video localizado</b> (12/11 da caixa JBL e mais 2 do Instagram): preciso saber onde esta o arquivo do video. <b>Para que:</b> sem o video nao da para levar esses Reels para a Pagina, e ela ficaria com buracos.",
     "Pendente", "Voce me diz onde esta o video", "Previsto: 20/11/2026 as 20h"),
]

def validar():
    for a in ATIVIDADES:
        if len(a) != 4 or not all(str(x).strip() for x in a):
            sys.exit("RECUSADO: linha com campo vazio: %r" % (a,))
        if a[1] not in ("Pendente", "Concluido"):
            sys.exit("RECUSADO: status invalido: %r" % (a,))
        if not re.search(r"\d{1,2}/\d{1,2}", a[3]) or not re.search(r"\d{1,2}\s*h", a[3]):
            sys.exit("RECUSADO: falta data e horario: %r" % (a,))

def main():
    validar()
    linhas = [a for a in ATIVIDADES if a[1] == "Pendente"]
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    for f in glob.glob(os.path.join(PASTA, "BLOG- Pendencia e ajustes em programas_*.pdf")):
        shutil.move(f, os.path.join(PASTA, "old_bkp", os.path.basename(f)))
    caminho = os.path.join(PASTA, "BLOG- Pendencia e ajustes em programas_%s.pdf" % HOJE.strftime("%d_%m_%Y_%Hh%M"))
    ss = getSampleStyleSheet()
    st = ParagraphStyle("c", parent=ss["BodyText"], fontSize=9, leading=11)
    dados = [[Paragraph("<b>%s</b>" % c, st) for c in ("Atividade", "Status", "Quem", "Data e horario")]]
    for l in linhas:
        dados.append([Paragraph(x, st) for x in l])
    t = Table(dados, colWidths=[250, 50, 125, 102], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey), ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    doc = SimpleDocTemplate(caminho, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36,
                            title="BLOG - Pendencia e ajustes em programas")
    doc.build([Paragraph("BLOG: Pendencia e ajustes em programas", ss["Title"]),
               Paragraph("Gerado em %s as %s. Este quadro mostra so o que ainda falta fazer, para voce acompanhar o que esta pendente; o que for concluido sai daqui."
                         % (HOJE.strftime("%d/%m/%Y"), HOJE.strftime("%Hh%M")), ss["BodyText"]), t])
    print(caminho)

if __name__ == "__main__":
    main()