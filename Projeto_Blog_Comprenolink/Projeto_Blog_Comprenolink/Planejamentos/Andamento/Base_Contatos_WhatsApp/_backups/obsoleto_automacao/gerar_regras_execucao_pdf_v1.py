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
      Paragraph("Registro, em 04/11/2026, de três respostas dadas ao dono sobre a atividade 9 (Canal do WhatsApp) e o processo de automação de convites: (1) resumo cronológico do que foi feito, (2) resumo do processo com as atribuições do Claude e do dono, (3) datas de início. Detalhes completos: <b>processo_automatização_whatsapp.pdf</b> e <b>Regras_de_Uso_Base_Contatos_WhatsApp.pdf</b> (mesma pasta).", p),
      Spacer(1, 3),
      caixa("Situação em 04/11/2026", [
          "A automação de convites <b>NÃO está ativada</b>. Só liga depois que o dono escrever o termo de autorização do item 6 do processo_automatização_whatsapp.pdf.",
          "Hoje a base tem 6 contatos, todos já convidados. Sem contatos aptos (PODE ENVIAR = SIM), o envio automático é 0."], LAR_C, LAR),
      Paragraph("1. O que foi feito, em ordem cronológica (04/11/2026)", h2),
      tab(["Nº", "O que foi feito"], [
          ["1", "<b>Anexo I do nova_pendencias.pdf.</b> Tabela de adequação (23% adequados, 77% faltando) e quadro do que falta, com datas e horários."],
          ["2", "<b>Atividade 9 (Canal do WhatsApp).</b> O dono perguntou se estava concluída. Conferi e vi que não: o link na bio do Instagram não existia. Corrigi o texto no PDF e criei a arte do Status de convite."],
          ["3", "<b>Status de convite.</b> Postado às 15:58 no WhatsApp Web, com legenda e link do Canal. Li 2 seguidores no Canal."],
          ["4", "<b>Link na bio.</b> O Instagram só permite editar links no celular. Guiei o dono passo a passo e conferi pelo PC: o 3º link \"Canal do WhatsApp\" está na bio."],
          ["5", "<b>PDF atualizado.</b> Atividade 9 e Anexos H e I, com a adequação em 30%."],
          ["6", "<b>Planilha semanal.</b> Anotei 2 seguidores e 7 convites enviados."],
          ["7", "<b>Base de dados.</b> Discutimos que 10 por dia não tinha insumo e que lista comprada não é permitida. O dono autorizou criar uma base própria."],
          ["8", "<b>Pasta Planejamentos\\Andamento\\Base_Contatos_WhatsApp</b> (criada como Base_Contatos_WhatsApp e renomeada pelo dono). Criei a planilha Excel (Hoje, Base, Envios, Canal, Mensagens e Parametros), testada no Excel deste PC, o PDF de regras de uso e o importador de inscrições do formulário."],
          ["9", "<b>Formulário do blog.</b> Adicionei o campo opcional WhatsApp e a caixa de consentimento, com backup antes. Já aparece na página da Black Friday."],
          ["10", "<b>Limite do dia.</b> Passou de 10 para 9, na planilha e no PDF de regras."],
          ["11", "<b>processo_automatização_whatsapp.pdf.</b> Documentei o processo de envio automatizado, com as atribuições do dono, a agenda e o checklist diário. Automação não ativada."],
          ["12", "<b>agenda_automacao_whatsapp.ics.</b> Gerei o arquivo com as rotinas e marcos do dono: validações às 09:50 e 20:30, respostas às 19:20, revisão de segunda, fases 2 e 3 e pausa na Black Friday."],
          ["13", "<b>Registros.</b> Atualizei as notas de memória e a estrutura de pastas."]], [0.06, 0.94]),
      Paragraph("<b>Pendente:</b> o dono importar o .ics na agenda; preencher os números dos 6 contatos já convidados; reunir pelo menos 9 contatos aptos até 09/11; o relatório de atividades do dia; regenerar a listagem Nova_Estrutura_diretorio…txt.", p),
      Paragraph("2. Processo de automação, resumido", h2),
      Paragraph("<b>Como funciona (depois que a base estiver alimentada)</b>", p),
      tab(["Passo", "O que acontece"], [
          ["1", "A planilha mostra quem pode receber hoje (aba Hoje)."],
          ["2", "Em 3 blocos (10:00, 14:00 e 18:00), o Claude envia até 3 convites por bloco. Teto de 9 por dia, 5 minutos entre as mensagens, das 9h às 20h."],
          ["3", "O Claude registra cada envio na aba Envios e confere se há alertas."],
          ["4", "O Claude responde quem entrou (M3) e quem pediu para sair (M4)."],
          ["5", "O Claude envia o relatório do dia."]], [0.1, 0.9]),
      Paragraph("O ritmo sobe aos poucos: 3 por dia na semana 1, 6 na semana 2 e 9 a partir da semana 3. Pausa em 27/11 (Black Friday).", p),
      Paragraph("<b>Atribuições do Claude</b>", p),
      tab(["Atribuição"], [
          ["Alimentar a base: importar o formulário, ler Direct e comentários e propor contatos. Só entra quem tem consentimento."],
          ["Montar a fila do dia e os textos."],
          ["Enviar nos blocos e registrar."],
          ["Parar sozinho nas situações de risco: aviso do WhatsApp, 2 pedidos de saída no dia ou alerta na Conferência."],
          ["Ler os seguidores do Canal toda segunda e fazer o relatório."]], [1.0]),
      Paragraph("3. O que o dono gerencia", h2),
      tab(["Quando", "O que", "Tempo"], [
          ["Todo dia, 09:50", "PC ligado, Chrome aberto e WhatsApp Web logado. Validar a fila e os textos na aba Hoje.", "5 min"],
          ["Todo dia, 19:20", "Responder as pessoas que escreveram.", "5 min"],
          ["Todo dia, 20:30", "Validação final: nenhum ALERTA, no máximo 9 envios. Marcar V ou X no quadro.", "5 min"],
          ["Segunda e quinta, 10:30", "Aprovar contatos pessoais novos.", "5 min"],
          ["Segunda, 10:30", "Revisar a semana: seguidores, saídas e ritmo. Decidir subir, manter ou reduzir.", "15 min"],
          ["Dia 1 de cada mês", "Revisar consentimentos e atender exclusões.", "20 min"],
          ["Quando ocorrer", "Resolver verificação ou aviso do WhatsApp no celular.", "5 min"]], [0.24, 0.62, 0.14]),
      Spacer(1, 4),
      caixa("Comandos do dono no chat", [
          "<b>Ligar:</b> escrever o termo de autorização do item 6 do processo_automatização_whatsapp.pdf. Só vale com pelo menos 9 contatos aptos.",
          "<b>Parar:</b> escrever \"pausar automação\", a qualquer hora."], VERDE_C, VERDE),
      Paragraph("<b>Atenção:</b> se o PC ou o Chrome estiverem fechados no horário, o bloco não acontece e não é recuperado. Hoje a base tem 6 contatos, todos já convidados: sem contatos aptos, o Claude envia 0.", p),
      Paragraph("4. Quando inicia", h2),
      Paragraph("<b>Início previsto: terça, 10/11/2026, às 10:00</b> (primeiro bloco, com 3 convites). Só vale se a base tiver pelo menos <b>9 contatos aptos</b> até segunda 09/11. Hoje há 0.", p),
      tab(["Quando", "O que acontece", "Quem"], [
          ["Qui 05/11, 10:30", "Começa a alimentação da base: o dono escolhe os contatos pessoais que podem receber e passa nomes e números.", "Dono"],
          ["05/11 a 09/11", "O Claude lê os pedidos do Direct e dos comentários e importa o formulário. Cada contato entra com a prova de consentimento.", "Claude"],
          ["Seg 09/11, 10:30", "Revisão: contagem dos contatos com SIM na aba Hoje. Com 9 ou mais, a data de 10/11 está confirmada.", "Claude e dono"],
          ["Ter 10/11, 09:00", "O dono escreve o termo de autorização no chat.", "Dono"],
          ["Ter 10/11, 10:00", "Primeiro bloco, com 3 envios, acompanhado pelo Claude.", "Claude"],
          ["Ter 17/11", "Fase 2, com 6 por dia, se a semana 1 fechou sem problema.", "Claude, com decisão do dono"],
          ["Ter 24/11", "Fase 3, com 9 por dia, se a semana 2 fechou sem problema.", "Claude, com decisão do dono"],
          ["Sex 27/11", "Pausa na Black Friday. Retoma em 28/11.", "Claude"]], [0.2, 0.58, 0.22]),
      Paragraph("Se faltar gente até 09/11, o início passa para o dia em que houver 9 aptos. A exigência de consentimento não é reduzida para cumprir a data. Para os lembretes tocarem a partir de 05/11, o dono importa o arquivo <b>agenda_automacao_whatsapp.ics</b> na agenda dele.", p),
      Spacer(1, 6),
      Paragraph("Registro de 04/11/2026. Complementa: processo_automatização_whatsapp.pdf, Regras_de_Uso_Base_Contatos_WhatsApp.pdf e Base_Contatos_WhatsApp.xlsx.", peq)]

doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.7 * cm, rightMargin=1.7 * cm, topMargin=1.6 * cm, bottomMargin=1.8 * cm,
                        title="Regras de execução", author="comprenolink.net")
doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
print("OK:", SAIDA)
