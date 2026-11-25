# -*- coding: utf-8 -*-
"""Relatorio diario da conversa BLOG - Ajustes no WhatsApp e Instagram.
REGRA ATUAL (dono, 19/11/2026 noite): o PDF mostra SO pendencias e atividades a realizar.
Concluido sai do relatorio (a lista EXECUTADO abaixo e apenas arquivo interno, nao e impressa). Uma unica versao na pasta (anterior -> old_bkp)."""
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
    ("19/11/2026", "Reels do Instagram de 02/11 e 04/11 publicados na Pagina Facebook Comprenolink",
     "Feito por mim (dono escolheu o video). Depois disso a sincronizacao dos demais Reels passou para a conversa 'Pendencia e ajustes em programas'."),
    ("19/11/2026", "Conferencia da planilha Base_Contatos_WhatsApp (abas Envios e Hoje)",
     "Feito por mim, so leitura. Ultimo lote de convites: L5 em 12/11 (8 envios). Total 37 convites, 1 entrada no Canal."),
    ("19/11/2026", "Corrigir na Base C007 (empresa), C331 (Lur) e C383 (Mercia): nao convidar",
     "Feito por mim, com o 'de acordo' do dono. Consentimento mudado para Nao; os 3 sairam da fila (PODE ENVIAR = NAO). Backup em old_bkp da pasta da Base (19-11-2026-11h10)."),
    ("19/11/2026", "Corrigir na Base o C010 (Baterias Moura, empresa): nao convidar",
     "Feito por mim, de acordo do dono. Consentimento mudado para Nao; saiu da fila. Backup em old_bkp da pasta da Base (19-11-2026-18h45). Fila de hoje: C011 liberado e C009 aguardando aprovacao."),
    ("19/11/2026", "Refazer a lista da aba Hoje da Base (N 1 a 9 estavam sem formula desde a limpeza de 12/11)",
     "Feito por mim, com o dono fechando o Excel. A lista agora mostra C009 e C011 com o texto M1. Backup em old_bkp da pasta da Base (19-11-2026-18h47)."),
    ("19/11/2026", "Convites do WhatsApp de hoje (lote L6-19/11): C009 Basilio e C011 Bruno",
     "Enviados a mao pelo dono; registrados por mim na aba Envios (18h48 e 18h51, horario aproximado, conferencia OK). Total de convites: 39. Backup em old_bkp da pasta da Base (19-11-2026-18h53)."),
]

# REGRA (dono): TODA linha tem O QUE E, PARA QUE SERVE, Status, Quem e QUANDO (data + horario). Linguagem simples.
# (o que e, para que serve, status, quem, quando)  -- 'Previsto' = data/hora sugerida, vale ate o dono mudar.
PENDENCIAS = [
    ("Nenhuma atividade pendente de hoje (seg 23/11). Os 20 Reels de 24, 25, 26 e 27/11 estao agendados no Meta e conferidos (dia, hora e legenda so com comprenolink.net, sem #). Nada foi tocado no anuncio pago. Abas do Chrome fechadas.",
     "Instagram com 5 Reels por dia durante a semana da Black Friday.",
     "Concluido hoje", "Claude", "Seg 23/11/2026, feito"),
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

def banner_urgente(ss):
    """Faixa de destaque (dono, 20/11/2026): execucao obrigatoria, urgente e o que impacta."""
    verm = colors.HexColor("#C00000")
    st = ParagraphStyle("urg", parent=ss["BodyText"], fontSize=10.5, leading=14, textColor=verm)
    tit = ParagraphStyle("urgt", parent=ss["Heading2"], textColor=colors.white, alignment=1, spaceAfter=0, spaceBefore=0)
    topo = Paragraph("ATENCAO: EXECUCAO OBRIGATORIA E URGENTE", tit)
    corpo = [Paragraph("<b>ESTAS ATIVIDADES TEM QUE SER EXECUTADAS HOJE, SEGUNDA 23/11, das 14h00 as 15h30.</b>", st),
             Spacer(1, 4),
             Paragraph("<b>O QUE IMPACTA se nao forem feitas:</b> o Instagram fica SEM REEL a partir de terca 24/11, na semana da Black Friday, "
                       "justamente quando voce paga anuncio e quem clica nele pode entrar pelo perfil e pelo blog. "
                       "<b>Os Reels de terca 24/11 as 11h00 e 13h30 so podem ser agendados na SEGUNDA</b> (na terca, as 14h00, esses horarios ja passaram).", st),
             Spacer(1, 4),
             Paragraph("<b>Anuncios pagos:</b> o anuncio em si nao usa os Reels, e nada sera publicado nem alterado nele nas janelas; so leitura.", st)]
    t = Table([[topo], [corpo]], colWidths=[525])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), verm),
                           ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FDE7E9")),
                           ("BOX", (0, 0), (-1, -1), 2.5, verm),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def main():
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    for padrao in ("BLOG- Ajustes no WhatsApp e Instagram_*.pdf", "RELATORIO_WHATSAPP_INSTAGRAM_*.pdf"):
        for f in glob.glob(os.path.join(PASTA, padrao)):
            shutil.copy2(f, os.path.join(PASTA, "old_bkp", os.path.basename(f)))
            try:
                os.remove(f)
            except PermissionError:
                print("AVISO: feche o PDF anterior para ele sair da pasta (copia ja esta em old_bkp):", os.path.basename(f))
    nome = "BLOG- Ajustes no WhatsApp e Instagram_%s.pdf" % HOJE.strftime("%d_%m_%Y_%Hh%M")
    caminho = os.path.join(PASTA, nome)
    ss = getSampleStyleSheet()
    h = ParagraphStyle("h", parent=ss["Heading2"], spaceBefore=10)
    doc = SimpleDocTemplate(caminho, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36,
                            title="Relatorio WhatsApp e Instagram")
    el = [Paragraph("Relatorio - BLOG: Ajustes no WhatsApp e Instagram", ss["Title"]),
          Paragraph("Gerado em %s as %s. Mostra so pendencias e atividades a realizar; o que foi concluido sai." % (HOJE_S, HOJE.strftime("%Hh%M")), ss["BodyText"]),
          Spacer(1, 6), banner_urgente(ss),
          Paragraph("Pendencias e atividades a realizar", h)]
    for l in PENDENCIAS:
        if len(l) != 5 or not all(str(x).strip() for x in l):
            raise SystemExit("ERRO: toda linha precisa de o que e, para que serve, status, quem e data+horario: %r" % (l,))
    destaque = []
    for o_que, serve, status, quem, quando in PENDENCIAS:
        destaque.append(('<font color="#C00000"><b>URGENTE - EXECUCAO OBRIGATORIA</b></font><br/><font color="#C00000">' + o_que + '</font>',
                         serve, '<font color="#C00000"><b>' + status + '</b></font>', quem,
                         '<font color="#C00000"><b>' + quando + '</b></font>'))
    el.append(tabela(destaque, ["O que e", "Para que serve", "Status", "Quem", "Data e horario"], [148, 120, 58, 90, 109]))
    doc.build(el)
    print(caminho)

if __name__ == "__main__":
    main()

