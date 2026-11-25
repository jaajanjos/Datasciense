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
    ("<b>Sincronizar com a Pagina do Facebook so os Reels bons que voce escolher</b>, conforme o Plano Geral da Virada Organica (versao 22h20) e o Plano Reformulado, sem aumentar o volume e so apos o aviso da conversa dos Reels. <b>Para que:</b> Facebook com esforco minimo, sem apagar a Pagina e sem gastar uso a toa. Toda segunda mando 1 linha a conversa Execucao (fiz / pendente / preciso do dono).",
     "Pendente", "Eu publico depois que voce escolher os Reels", "Previsto: quartas as 20h00, depois do aviso da conversa dos Reels (1a vez: 25/11/2026 as 20h00); sem prazo fixo"),
    ("<b>Conferir na lista de publicados da Pagina o Reel da Webcam Logitech C270</b> (estava em processamento na Meta em 24/11). <b>Para que:</b> garantir que ele realmente foi publicado so na Pagina; se falhar, eu republico.",
     "Pendente", "Eu (leitura rapida, junto com a sync da quarta)", "Previsto: 25/11/2026 as 20h00"),
    ("<b>Conferir no blog, so em leitura, o resultado das melhorias M1+M3+M7 (01/12) e M2 (02/12).</b> Paginas abrem (200), botoes e imagens sem quebra, sem texto de preco nem 'melhor/mais vendido'. Aviso a Execucao em 1 linha; se achar problema, aviso a Execucao e voce na hora (restauracao pelo backup do gerenciar_blog). <b>Para que:</b> garantir que as melhorias agendadas nao quebraram nada e respeitam a politica do blog.",
     "Pendente", "Eu (so leitura; as melhorias rodam sozinhas)", "Previsto: 02/12/2026 as 20h30"),
    ("<b>Conferir no blog, so em leitura, o piloto M4 (08/12).</b> Mesmos testes: paginas 200, sem quebra, sem preco nem 'melhor/mais vendido'. Aviso a Execucao em 1 linha. <b>Para que:</b> validar o piloto antes de ele valer para o resto do blog.",
     "Pendente", "Eu (so leitura)", "Previsto: 09/12/2026 as 20h30"),
    ("<b>Mandar 1 linha a conversa Execucao toda segunda: o que fiz / o que esta pendente / o que preciso do dono.</b> Regra do plano reformulado: fora isso, so mensagem se eu ficar bloqueado. <b>Para que:</b> a Execucao juntar tudo no relatorio geral sem eu gastar uso a toa.",
     "Pendente", "Eu envio a linha (sem precisar de voce)", "Previsto: toda segunda, 1a vez 30/11/2026 ate 21h00"),
    ("<b>Acompanhar as leituras do plano:</b> 30/11, 07/12 e 14/12 (decisao em 14/12), feitas pela Execucao. Se o plano reduzir o esforco, ajusto a minha sync. <b>Para que:</b> manter so o que gera cliques para o Mercado Livre, com custo zero e dentro do limite do plano Pro (5h abaixo de 75%, semanal abaixo de 80%).",
     "Pendente", "Execucao decide; eu sigo o ajuste", "Previsto: 30/11/2026, 07/12/2026 e 14/12/2026 as 21h00"),
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
    for pref in ("BLOG- Pendencia e ajustes em programas_", "BLOG - Execução de atividades_"):
        for f in glob.glob(os.path.join(PASTA, pref + "*.pdf")):
            shutil.move(f, os.path.join(PASTA, "old_bkp", os.path.basename(f)))
    caminho = os.path.join(PASTA, "BLOG - Execução de atividades_%s.pdf" % HOJE.strftime("%d_%m_%Y_%Hh%M"))
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