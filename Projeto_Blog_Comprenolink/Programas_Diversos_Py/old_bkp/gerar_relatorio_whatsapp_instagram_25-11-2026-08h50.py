# -*- coding: utf-8 -*-
"""Relatorio diario da conversa BLOG - Ajustes Instagram.
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
    ("Conferir no Meta (so leitura) se os 5 Reels de ter 24/11 (11h00, 13h30, 16h00, 18h00 e 20h00) sairam no horario e com a legenda certa (so comprenolink.net, sem #). Nao foi feita na terca a noite; passa para quarta, sem impacto no plano.",
     "Garantir que os Reels ja agendados estao no ar e sem erro.",
     "Pendente (adiada)", "Claude (so leitura)", "Qua 25/11/2026, 19h30 (aviso a Execucao antes e depois de usar o Chrome)"),
    ("Receber do dono o caminho da pasta nova dos Reels e a confirmacao do estilo visual agressivo para os Reels organicos.",
     "Produzir tudo no lugar certo, sem mexer fora da estrutura. Sem resposta, salvo a amostra na estrutura atual e o dono move depois.",
     "Aguarda o dono", "Dono", "Qua 25/11/2026, ate 20h00"),
    ("Desenhar o estilo visual novo e mostrar 1 Reel de amostra.",
     "O dono aprovar o visual antes de gerar em volume.",
     "Previsto", "Claude; aprovacao do dono ate 22h00", "Qua 25/11/2026, 20h00 as 21h30"),
    ("Gerar o 1o lote: 16 Reels (29/11 a 06/12, 2 por dia, alternando estilo novo e atual), legenda so comprenolink.net, sem preco e sem 'melhor/mais vendido/lider'. Antes, conferir o uso do plano (parar se 5h>75% ou semanal>80%).",
     "Domingo 29/11 comecar com Reels no ar (fase 1 da rampa).",
     "Previsto (depende do 'sim' na amostra)", "Claude", "Qui 26/11/2026, 20h00 as 23h00"),
    ("Agendar o lote no Meta Business Suite com o dono (ele escolhe os arquivos); informar a % de uso a Execucao antes e depois. Na mesma janela, trocar so o link da bio do Instagram por comprenolink.net/?utm_source=instagram&utm_medium=bio&utm_campaign=organico_reels, conferir que abre o blog e registrar antes/depois (aguarda o 'sim' do dono nesta conversa).",
     "Reels no ar as 13h30 e 20h00; medir os cliques que vem do Instagram.",
     "Previsto (Chrome reservado)", "Claude + dono", "Sex 27/11/2026, 14h00 as 16h00"),
    ("Conferir (so leitura) que os Reels de dom 29/11 sairam as 13h30 e 20h00, com a legenda certa.",
     "Garantir a virada sem falha.",
     "Previsto", "Claude (so leitura)", "Dom 29/11/2026, 13h45 e 20h30 (fim de semana vale por decisao do dono)"),
    ("Leitura dos numeros do Instagram (alcance, salvamentos, cliques), estilo novo x atual, com 1 linha a Execucao; decisao de continuar/reduzir em 14/12.",
     "Aprender com o organico, sem custo.",
     "Previsto", "Claude", "Seg 30/11, 07/12 e 14/12/2026, 20h00"),
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
    corpo = [Paragraph("<b>VIRADA PARA O ORGANICO EM DOMINGO 29/11. PROXIMO PASSO: QUARTA 25/11.</b>", st),
             Spacer(1, 4),
             Paragraph("<b>Plano vigente (orquestracao: Execucao):</b> Reels em rampa, 2 por dia na fase 1 (29/11 a 06/12), 3 na fase 2 so se uso do plano < 60% e cliques subindo, 5 so com evidencia. "
                       "Gerar toda quinta, agendar toda sexta 14h00 as 16h00. Plano geral: 0- Pendencias/1_Pendencias/PLANO_GERAL_VIRADA_ORGANICO_29_11_2026_*.pdf", st),
             Spacer(1, 4),
             Paragraph("<b>Anuncio pago:</b> nunca mais; nada e alterado nele por esta conversa. WhatsApp fora; so com venda comprovada e evidencia.", st)]
    t = Table([[topo], [corpo]], colWidths=[525])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), verm),
                           ("BACKGROUND", (0, 1), (-1, 1), colors.HexColor("#FDE7E9")),
                           ("BOX", (0, 0), (-1, -1), 2.5, verm),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def main():
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    for padrao in ("BLOG- Ajustes no WhatsApp e Instagram_*.pdf", "BLOG- Ajustes Instagram_*.pdf", "RELATORIO_WHATSAPP_INSTAGRAM_*.pdf"):
        for f in glob.glob(os.path.join(PASTA, padrao)):
            shutil.copy2(f, os.path.join(PASTA, "old_bkp", os.path.basename(f)))
            try:
                os.remove(f)
            except PermissionError:
                print("AVISO: feche o PDF anterior para ele sair da pasta (copia ja esta em old_bkp):", os.path.basename(f))
    nome = "BLOG- Ajustes Instagram_%s.pdf" % HOJE.strftime("%d_%m_%Y_%Hh%M")
    caminho = os.path.join(PASTA, nome)
    ss = getSampleStyleSheet()
    h = ParagraphStyle("h", parent=ss["Heading2"], spaceBefore=10)
    doc = SimpleDocTemplate(caminho, pagesize=A4, leftMargin=36, rightMargin=36, topMargin=36, bottomMargin=36,
                            title="Relatorio WhatsApp e Instagram")
    el = [Paragraph("Relatorio - BLOG: Ajustes Instagram", ss["Title"]),
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

