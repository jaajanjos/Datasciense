# -*- coding: utf-8 -*-
"""Gera regras_execução.pdf: registro do resumo cronológico, do resumo do processo de automação (atribuições) e das datas de início."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Ar", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("ArB", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFontFamily("Ar", normal="Ar", bold="ArB", italic="Ar", boldItalic="ArB")

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
SAIDA = PASTA + "/regras_execução.pdf"
VERDE = colors.HexColor("#0B3D2E"); VERDE_C = colors.HexColor("#E8F5EE")
VERM = colors.HexColor("#9C0006"); VERM_C = colors.HexColor("#FFC7CE")
LAR = colors.HexColor("#B45F06"); LAR_C = colors.HexColor("#FFF4C2")
h1 = ParagraphStyle("h1", fontName="ArB", fontSize=17, textColor=VERDE, spaceAfter=4, leading=21)
h2 = ParagraphStyle("h2", fontName="ArB", fontSize=12.5, textColor=VERDE, spaceBefore=10, spaceAfter=4, leading=16)
p = ParagraphStyle("p", fontName="Ar", fontSize=10, leading=14, spaceAfter=3)
pc = ParagraphStyle("pc", fontName="Ar", fontSize=8.8, leading=11.5)
pcb = ParagraphStyle("pcb", fontName="ArB", fontSize=8.8, leading=11.5)
ph = ParagraphStyle("ph", fontName="ArB", fontSize=8.8, leading=11.5, textColor=colors.white)
peq = ParagraphStyle("peq", fontName="Ar", fontSize=8.5, leading=11, textColor=colors.HexColor("#555555"))
W = 17.6 * cm


def tab(cab, linhas, larg, cor=VERDE):
    dados = [[Paragraph(c, ph) for c in cab]] + [[Paragraph(str(c), pcb if i == 0 else pc) for i, c in enumerate(l)] for l in linhas]
    t = Table(dados, colWidths=[w * W for w in larg], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), cor), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F7F7")]),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def caixa(titulo, itens, fundo, borda):
    corpo = [Paragraph(f"<b>{titulo}</b>", p)] + [Paragraph("• " + i, p) for i in itens]
    t = Table([[corpo]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fundo), ("BOX", (0, 0), (-1, -1), 1, borda),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def rodape(c, d):
    c.saveState()
    c.setFont("Ar", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(1.7 * cm, 1.1 * cm, "comprenolink.net  •  Regras de execução  •  registro de 04/11/2026")
    c.drawRightString(A4[0] - 1.7 * cm, 1.1 * cm, f"Página {d.page}")
    c.restoreState()

st = [Paragraph("Regras de execução", h1),
      Paragraph("Registro, em 04/11/2026, do que foi feito sobre a atividade 9 (Canal do WhatsApp) e a base de contatos, e do plano que vale <b>depois da revisão da noite</b>. Detalhes: <b>processo_crescimento_canal_whatsapp.pdf</b> e <b>Regras_de_Uso_Base_Contatos_WhatsApp.pdf</b> (mesma pasta).", p),
      Spacer(1, 3),
      caixa("Situação em 04/11/2026 (noite)", [
          "<b>A automação de convites foi cancelada</b> por risco de bloqueio do número do WhatsApp. Ela nunca foi ligada e nenhuma mensagem automática foi enviada.",
          "<b>Regra fixa:</b> nenhum envio em massa e nenhuma automação de mensagens pelo WhatsApp Web. Convites só à mão, pelo celular do dono, para quem ele conhece.",
          "A base tem 500 contatos importados (mais 55 na aba Reserva), todos <b>pendentes</b> e fora da fila. Aptos para convite: 0."], VERM_C, VERM),
      Paragraph("1. O que foi feito, em ordem cronológica (04/11/2026)", h2),
      tab(["Nº", "O que foi feito"], [
          ["1", "<b>Anexo I do nova_pendencias.pdf.</b> Tabela de adequação e quadro do que falta, com datas e horários."],
          ["2", "<b>Atividade 9 (Canal do WhatsApp).</b> Conferi que não estava concluída (faltava o link na bio) e criei a arte do Status de convite."],
          ["3", "<b>Status de convite</b> postado às 15:58, com legenda e link do Canal. O Canal tinha 2 seguidores."],
          ["4", "<b>Link na bio.</b> O dono criou o 3º link \"Canal do WhatsApp\" no celular, guiado passo a passo, e eu conferi pelo PC."],
          ["5", "<b>PDF e planilha semanal atualizados</b> (atividade 9, Anexos H e I, 2 seguidores e 7 convites)."],
          ["6", "<b>Base de dados.</b> Sem lista comprada. Criei a pasta 12_Base_Contatos_WhatsApp com a planilha Excel, o PDF de regras de uso e o importador do formulário."],
          ["7", "<b>Formulário do blog</b> com campo WhatsApp e caixa de consentimento, com backup antes."],
          ["8", "<b>Limite do dia</b> passou de 10 para 9 na planilha e no PDF de regras."],
          ["9", "<b>Documentos de automação v1</b> (processo, agenda, checklist de 30 dias e guia do gerador). Depois substituídos, ver itens 12 a 14."],
          ["10", "<b>Limpeza do nova_pendencias.pdf</b> (só pendências; histórico em bkp_drp) e atualização da agenda no Google Agenda: série antiga apagada, concluídos apagados, sem duplicados."],
          ["11", "<b>Importação dos contatos.</b> O dono exportou dois arquivos CSV do Google Contatos (dele e da sócia Rosana). Importei: 6 números preenchidos, 28 contatos do dono e 466 da Rosana na Base, 55 na aba Reserva. Todos como pendentes."],
          ["12", "<b>Análise de risco.</b> O dono questionou a segurança. Concluí que o envio automatizado pelo WhatsApp Web arrisca a conta e que eu devia ter avisado antes."],
          ["13", "<b>Decisão do dono:</b> cancelar a automação e adotar o crescimento por atração e convite à mão. Regra gravada na memória: avaliar o risco de bloqueio antes de qualquer pedido."],
          ["14", "<b>Revisão completa.</b> Reescrevi o processo (processo_crescimento_canal_whatsapp.pdf), as regras de uso, este documento, o guia, o checklist, a planilha, as agendas e o nova_pendencias.pdf. Versões antigas em _backups\\obsoleto_automacao."]], [0.06, 0.94]),
      Paragraph("2. Plano atual, resumido", h2),
      tab(["Frente", "O que acontece", "Quem"], [
          ["Atrair", "Link do Canal em Status, bio, blog, Stories e Reels, com a chamada \"Entre no Canal\".", "Claude e dono"],
          ["\"Comente CANAL\"", "ManyChat responde no Direct com o link a quem comentou. Texto até qui 05/11, 10:20; teste em 11/11.", "Claude escreve, dono cola"],
          ["Convite pessoal", "O dono aprova quem conhece (Conhecido) e envia à mão, até 9 por dia (5 na 1ª semana), mensagem personalizada.", "Dono"],
          ["Oferta exclusiva", "Cupom ou oferta só no Canal, principalmente na Black Friday.", "Claude propõe, dono aprova"]], [0.2, 0.58, 0.22]),
      Paragraph("<b>O Claude não envia convites em massa.</b> Ele prepara a lista e o texto, registra o que o dono informar, lê os seguidores do Canal e faz o relatório. A divulgação das 19:12 continua automática (Status, Canal e Story), porque é publicação no próprio perfil e não mensagem para terceiros.", p),
      Paragraph("3. O que o dono gerencia", h2),
      tab(["Quando", "O que", "Tempo"], [
          ["Todo dia, 10:00", "Convites pessoais à mão, da lista preparada pelo Claude.", "15 min"],
          ["Todo dia, 19:20", "Responder as pessoas que escreveram.", "5 min"],
          ["Todo dia, 20:30", "Fechar o dia: anotar enviados, saídas e entradas.", "2 min"],
          ["Quinta, 10:30", "Aprovar contatos pessoais (Conhecido).", "5 min"],
          ["Segunda, 10:30", "Revisar a semana: seguidores do Canal, saídas e ritmo.", "15 min"],
          ["Dia 1 de cada mês", "Revisar consentimentos e atender exclusões.", "20 min"],
          ["Quando ocorrer", "Resolver verificação ou aviso do WhatsApp no celular e parar convites por 7 dias.", "5 min"]], [0.24, 0.62, 0.14]),
      Spacer(1, 4),
      caixa("Regras de parada", [
          "Aviso ou verificação do WhatsApp: parar os convites por 7 dias.",
          "2 ou mais pedidos de saída no dia, ou 1 denúncia: parar os convites do dia.",
          "Dúvida se algo é permitido: perguntar ao Claude antes."], VERDE_C, VERDE),
      Paragraph("4. Quando inicia", h2),
      Paragraph("<b>Início dos convites à mão: assim que você aprovar os primeiros contatos como Conhecido</b>, na quinta 05/11, 10:30. Não há data fixa nem mínimo de contatos: se houver poucos, convida poucos. A atração (Status, bio, \"Comente CANAL\") já está valendo.", p),
      tab(["Quando", "O que acontece", "Quem"], [
          ["Qui 05/11, 10:20", "Texto do \"Comente CANAL\" e da resposta do ManyChat pronto; dono cola (G1).", "Claude e dono"],
          ["Qui 05/11, 10:30", "Dono aprova os primeiros Conhecidos na planilha.", "Dono"],
          ["Sex 06/11 em diante", "Convites à mão, até 5 por dia na 1ª semana e até 9 depois.", "Dono"],
          ["Seg 09/11, 10:30", "Primeira revisão semanal: seguidores, saídas e importação do formulário.", "Claude e dono"],
          ["Qua 11/11", "Teste do ManyChat com outra conta.", "Dono"]], [0.2, 0.58, 0.22]),
      Spacer(1, 6),
      Paragraph("Registro de 04/11/2026 (noite). Complementa: processo_crescimento_canal_whatsapp.pdf, Regras_de_Uso_Base_Contatos_WhatsApp.pdf e Base_Contatos_WhatsApp.xlsx.", peq)]

doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.7 * cm, rightMargin=1.7 * cm, topMargin=1.6 * cm, bottomMargin=1.8 * cm,
                        title="Regras de execução", author="comprenolink.net")
doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
print("OK:", SAIDA)
