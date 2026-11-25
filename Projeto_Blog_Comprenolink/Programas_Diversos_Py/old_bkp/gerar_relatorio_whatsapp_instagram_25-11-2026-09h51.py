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
    ("Conferir no Meta (so leitura) se os 5 Reels de ter 24/11 sairam no horario e com a legenda certa (so comprenolink.net, sem #). Ver tambem quais dias ja tem Reel de 19h05 agendado (regra aprovada: nesses dias, so o novo das 13h30). Aviso a Execucao antes e depois de usar o Chrome.",
     "Garantir que os Reels ja agendados estao no ar e saber onde cada novo Reel entra.",
     "Pendente", "Claude (so leitura)", "Qua 25/11/2026, 19h30"),
    ("Agendar o lote 1 (16 Reels, ja gerado e aprovado) no Meta com o dono (ele escolhe os arquivos); informar a % de uso a Execucao antes e depois. Na mesma janela, trocar so o link da bio do Instagram por comprenolink.net/?utm_source=instagram&utm_medium=bio&utm_campaign=organico_reels (dono deu o 'sim'), conferir que abre o blog e registrar antes/depois.",
     "Reels no ar a partir de 29/11; medir os cliques que vem do Instagram.",
     "Previsto (Chrome reservado)", "Claude + dono", "Sex 27/11/2026, 14h00 as 16h00"),
    ("Conferir (so leitura) que os Reels de dom 29/11 sairam no horario, com a legenda certa.",
     "Garantir a virada sem falha.",
     "Previsto", "Claude (so leitura)", "Dom 29/11/2026, 13h45 e 20h30"),
    ("Leitura dos numeros do Instagram (alcance, salvamentos, cliques) e 1 linha a Execucao; decisao de continuar/reduzir em 14/12.",
     "Aprender com o organico, sem custo.",
     "Previsto", "Claude", "Seg 30/11, 07/12 e 14/12/2026, 20h00"),
    ("Gerar o lote 2 (07 a 13/12), conferindo o uso antes (parar se 5h>75% ou semanal>80%); fase 2 (3 por dia) decidida com a leitura parcial de qui 03/12, sem dado claro mantem 2 por dia.",
     "Seguir completando o ciclo com lotes semanais.",
     "Previsto", "Claude", "Qui 03/12/2026, 20h00 as 23h00"),
    ("Agendar o lote 2 no Meta com o dono. Depois, lote 3 (14 a 20/12) e lote 4 (21 a 23/12): gerar toda quinta e agendar toda sexta, ate fechar o ciclo em 23/12.",
     "Completar todos os dias de Reels, o mais cedo possivel, dentro da janela de 29 dias do Instagram.",
     "Previsto", "Claude + dono", "Sex 04/12/2026, 14h00 as 16h00 (e sextas 11/12 e 18/12)"),
    ("Avaliar com o dono as legendas antigas dos Reels agendados com 'Comente X que eu te mando o link no Direct': corrigir os mais proximos ou deixar rodar (sem editar antes do 'de acordo').",
     "Nao contradizer a linha de confianca do blog.",
     "Previsto", "Claude + dono", "Seg 07/12/2026"),
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
          Spacer(1, 6),
          Paragraph("Atividades do novo plano (em ordem de data)", h)]
    for l in PENDENCIAS:
        if len(l) != 5 or not all(str(x).strip() for x in l):
            raise SystemExit("ERRO: toda linha precisa de o que e, para que serve, status, quem e data+horario: %r" % (l,))
    el.append(tabela([(o, sv, "<b>%s</b>" % st, q, "<b>%s</b>" % qd) for o, sv, st, q, qd in PENDENCIAS],
                     ["Atividade", "Para que serve", "Status", "Quem", "Data e horario"], [165, 110, 62, 80, 108]))
    doc.build(el)
    print(caminho)

if __name__ == "__main__":
    main()

