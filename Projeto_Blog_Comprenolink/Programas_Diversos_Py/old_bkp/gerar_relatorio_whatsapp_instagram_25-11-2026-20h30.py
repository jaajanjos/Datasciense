# -*- coding: utf-8 -*-
"""Relatorio diario da conversa BLOG - Ajustes Instagram.
REGRA ATUAL (dono, 19/11/2026 noite): o PDF mostra SO pendencias e atividades a realizar.
Concluido sai do relatorio (a lista EXECUTADO abaixo e apenas arquivo interno, nao e impressa). Uma unica versao na pasta (anterior -> old_bkp)."""
import os, re, shutil, glob
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
HOJE = datetime.now()
HOJE_S = HOJE.strftime("%d/%m/%Y")

# (data DD/MM/AAAA, atividade, situacao)  -> aparece so se data == hoje
# EXECUTADO do novo plano (dono, 25/11/2026: o PDF mostra o que executamos e o que falta). (atividade, resultado, quem, data)
EXECUTADO = [
    ("Plano geral da virada para o organico elaborado e distribuido as conversas (Execucao, 1- PY, Pendencia)",
     "Aprovado pelo dono; versoes ajustadas ate a rampa de Reels (2, 3 e 5 por dia).", "Claude + dono", "24/11/2026"),
    ("Regra de agendamento dos Reels definida",
     "Aprovada pelo dono: manter o ja agendado; dias com Reel de 19h05 = so o novo das 13h30; demais 13h30 e 20h00.", "Claude + dono", "25/11/2026"),
    ("Pasta REELS_NOVO_BLOG criada (01_AMOSTRA, 02_LOTE_29-11_a_06-12) e conversas avisadas",
     "Pasta aprovada pelo dono; so esta conversa grava nela.", "Claude", "25/11/2026"),
    ("Estilo visual dos Reels definido (limpo, igual ao blog) e amostra feita",
     "Amostra aprovada pelo dono. Gerador novo: _fonte/gerar_reels_novo.py.", "Claude + dono", "25/11/2026"),
    ("Lote 1 gerado: 16 Reels (29/11 a 06/12), legenda so comprenolink.net, sem hashtag e sem termos proibidos",
     "Aprovado pelo dono ('nota 1000'); antecipado de qui 26/11. Uso do plano antes: 5h=49%, semanal=44%.", "Claude + dono", "25/11/2026"),
    ("Link da bio do Instagram com rastreio (UTM)", "Dono deu o 'sim'; a troca fica para sex 27/11.", "Dono", "25/11/2026"),
    ("PDFs renomeados para o prefixo 'BLOG- Ajustes Instagram' e geradores ajustados", "36 arquivos renomeados; backups em old_bkp.", "Claude", "25/11/2026"),
]

# REGRA (dono): TODA linha tem O QUE E, PARA QUE SERVE, Status, Quem e QUANDO (data + horario). Linguagem simples.
# (o que e, para que serve, status, quem, quando)  -- 'Previsto' = data/hora sugerida, vale ate o dono mudar.
PENDENCIAS = [
    ("MISSAO DOS REELS: ser a dona de agendar todos os dias de Reels ate fechar o ciclo (23/12), o mais cedo possivel, em lotes semanais, com as guardas de uso (5h>75% ou semanal>80% = adiar).",
     "Uma dona so, sem duplicar; Reels todos os dias.",
     "Em andamento", "Claude + dono", "Continua, desde 25/11 ate 23/12/2026"),
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
    """Cores (dono, 25/11): Concluido = linha #DCFCE7 + status verde negrito; Em andamento = #FEF08A + ambar negrito; pendente sem cor."""
    st = getSampleStyleSheet()["BodyText"]; st.fontSize = 9; st.leading = 11
    dados = [[Paragraph("<b>%s</b>" % c, st) for c in cab]]
    cores = []
    for i, l in enumerate(linhas, start=1):
        cel = [Paragraph(x, st) for x in l]
        for k, c in enumerate(cab):
            if c == "Status":
                t_ = re.sub("<[^>]+>", "", str(l[k]))
                if t_.startswith("Concluido") or t_.startswith("Concluído"):
                    cel[k] = Paragraph('<font color="#166534"><b>%s</b></font>' % t_, st); cores.append((i, "#DCFCE7"))
                elif t_.startswith("Em andamento"):
                    cel[k] = Paragraph('<font color="#A16207"><b>%s</b></font>' % t_, st); cores.append((i, "#FEF08A"))
        dados.append(cel)
    t = Table(dados, colWidths=larg, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    for i, c in cores:
        t.setStyle(TableStyle([("BACKGROUND", (0, i), (-1, i), colors.HexColor(c))]))
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
          Paragraph("Gerado em %s as %s. Mostra o que ja executamos e o que falta executar (pedido do dono, 25/11)." % (HOJE_S, HOJE.strftime("%Hh%M")), ss["BodyText"]),
          Spacer(1, 6),
          Paragraph("O que ja executamos", h),
          tabela([(a_, r_, "Concluido", q_, d_) for a_, r_, q_, d_ in EXECUTADO], ["Atividade", "Resultado", "Status", "Quem", "Data"], [170, 165, 58, 70, 62]),
          Paragraph("O que falta executar (em ordem de data)", h)]
    for l in PENDENCIAS:
        if len(l) != 5 or not all(str(x).strip() for x in l):
            raise SystemExit("ERRO: toda linha precisa de o que e, para que serve, status, quem e data+horario: %r" % (l,))
    el.append(tabela([(o, sv, "<b>%s</b>" % st, q, "<b>%s</b>" % qd) for o, sv, st, q, qd in PENDENCIAS],
                     ["Atividade", "Para que serve", "Status", "Quem", "Data e horario"], [165, 110, 62, 80, 108]))
    doc.build(el)
    print(caminho)

if __name__ == "__main__":
    main()

