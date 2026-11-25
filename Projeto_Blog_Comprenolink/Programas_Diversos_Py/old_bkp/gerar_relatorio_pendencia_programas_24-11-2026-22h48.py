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
    ("<b>Publicados na Pagina 5 Reels que ja estavam no Instagram: Pipoqueira Mondial 12h50, Maquina de Cortar Cabelo 12h51, Jogo de Lencol Percal 12h52, Cortina de LED 3x3 12h53 e Webcam Logitech C270 (em processamento pela Meta, conferir).</b> So na Pagina, legenda terminando em comprenolink.net (sem hashtag). O Smartwatch T900 (IG 23/11 19h05) nao foi repetido porque o mesmo video ja esta na Pagina desde 23/11 11h15. <b>Para que:</b> Pagina em dia com o Instagram.",
     "Concluido", "Eu (adiantado a pedido do dono, sem janela do Windows)", "24/11/2026, das 12h50 as 12h55"),
    ("<b>Sincronizar com a Pagina do Facebook so os Reels bons que voce escolher</b>, conforme o Plano Geral da Virada Organica (versao 22h20). <b>Para que:</b> Facebook com esforco minimo, sem apagar a Pagina e sem gastar uso a toa. Toda segunda mando 1 linha a conversa Execucao (fiz / pendente / preciso do dono).",
     "Pendente", "Eu publico depois que voce escolher os Reels", "Previsto: quartas as 20h00, depois do aviso da conversa dos Reels (1a vez: 25/11/2026 as 20h00); sem prazo fixo"),
    ("<b>Reels sem video localizado</b> (12/11 da caixa JBL e mais 2 do Instagram): se voce achar o arquivo, me diga onde esta. <b>Para que:</b> so com o arquivo eu consigo levar esses Reels para a Pagina; se nao achar, eles ficam de fora e tudo bem, sem pressa.",
     "Pendente", "Voce me diz onde esta o video (opcional)", "Previsto: sem prazo, quando voce achar (leitura de 24/11/2026 12h50 nao conseguiu listar os Reels antigos do Instagram; nomes dos 2 ainda nao identificados)"),
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
    linhas = list(ATIVIDADES)  # concluido do dia fica; sai no dia seguinte (remover a linha)
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
               Paragraph("Gerado em %s as %s. Este quadro mostra o que foi concluido hoje e o que ainda falta; o concluido sai no dia seguinte."
                         % (HOJE.strftime("%d/%m/%Y"), HOJE.strftime("%Hh%M")), ss["BodyText"]), t])
    print(caminho)

if __name__ == "__main__":
    main()