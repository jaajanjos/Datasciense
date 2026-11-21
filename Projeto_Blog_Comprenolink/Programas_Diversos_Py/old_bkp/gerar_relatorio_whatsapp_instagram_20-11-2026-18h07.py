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
    ("Convites do WhatsApp, proximo lote: voce envia a mao o convite do Canal a conhecidos que aprovar; eu monto a lista e registro na planilha.",
     "Aumentar o numero de pessoas que recebem os achados do dia, sem risco de bloqueio do seu numero.",
     "Pendente", "Dono envia; Claude monta a lista e registra", "Previsto: seg 23/11/2026, 20h00 (so se voce aprovar novos contatos)"),
    ("Agendar 5 Reels no Instagram para SAB 21/11: Smart TV LG 32, Power Bank Anker, Moto G24, Mouse Logitech G403 e Churrasqueira Aero Home. Saem as 16h, 17h30, 19h05, 20h30 e 21h30.",
     "O perfil ter 5 Reels no ar no sabado sem voce postar a mao; adianta o calendario inteiro.",
     "Pendente", "Claude agenda; dono escolhe o arquivo de cada video", "Hoje, sex 20/11/2026, apos 15h40 (em andamento)"),
    ("Agendar 5 Reels no Instagram para DOM 22/11: JBL Boombox 4, Perfume Sabah Al Ward, Perfume Asad, Arvore de Natal e Khamrah. Mesmos horarios.",
     "O perfil ter 5 Reels no ar no domingo sem voce postar a mao.",
     "Pendente", "Claude agenda; dono escolhe o arquivo de cada video", "Previsto: sab 21/11/2026, apos 15h40"),
    ("Agendar 5 Reels no Instagram para SEG 23/11: Pisca LED, Pipoqueira Mondial, Maquina de cortar cabelo, Lencol Percal e Cortina de LED. Mesmos horarios.",
     "Fechar os 15 Reels que restam; depois disso nao ha mais Reel pronto e precisaremos criar novos.",
     "Pendente", "Claude agenda; dono escolhe o arquivo de cada video", "Previsto: dom 22/11/2026, apos 15h40"),
    ("Reel e foto agendados para 02/12 (JBL Boombox 4): ainda com as hashtags antigas, pois o Meta nao grava a edicao desses dois. Solucao: apagar os 2 agendamentos e criar de novo so com comprenolink.net e #comprenolinkblog, ou editar logo apos publicarem (pelo Instagram no computador).",
     "Nao divulgar outros sites; sao os unicos 2 posts que ainda tem hashtag de concorrente.",
     "Pendente", "Claude refaz; dono escolhe o arquivo do Reel", "Previsto: dom 22/11/2026, apos 15h40"),
    ("Conferencia final de TODOS os posts (Facebook e Instagram) e do anuncio: lista sem nenhuma hashtag de concorrente. Em 20/11: 9 corrigidos no Facebook/Instagram agendados e 17 publicados no Instagram, conferidos ao vivo.",
     "Garantir que nada divulgue outros sites enquanto voce paga anuncio.",
     "Pendente", "Claude", "Previsto: seg 23/11/2026, apos 15h40"),
    ("Acompanhar o alcance dos Reels na Pagina Comprenolink do Facebook: ver quantas pessoas assistiram.",
     "Saber se vale a pena continuar publicando os Reels na Pagina e quanto isso ajuda o blog.",
     "Pendente", "Claude", "Previsto: seg 23/11/2026, 20h30 (repetir com mais dias de dados; 1a leitura feita em 20/11)"),
    ("Pacotes do outro PC (4_PACOTE_OUTRO_PC.zip, 4_ATUALIZAR_OUTRO_PC.zip e CentralBlog.exe): voce decide 'refazer' ou 'deixar'.",
     "O outro computador usar a versao certa dos programas do blog; sem a sua decisao isso fica parado.",
     "Pendente", "Dono decide", "Previsto: seg 23/11/2026, 20h00"),
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
          Paragraph("Pendencias e atividades a realizar", h)]
    for l in PENDENCIAS:
        if len(l) != 5 or not all(str(x).strip() for x in l):
            raise SystemExit("ERRO: toda linha precisa de o que e, para que serve, status, quem e data+horario: %r" % (l,))
    el.append(tabela(PENDENCIAS, ["O que e", "Para que serve", "Status", "Quem", "Data e horario"], [150, 130, 48, 90, 109]))
    doc.build(el)
    print(caminho)

if __name__ == "__main__":
    main()
