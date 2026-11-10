# -*- coding: utf-8 -*-
"""Gera processo_automatização_whatsapp.pdf (fica ao lado da planilha)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Ar", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("ArB", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFontFamily("Ar", normal="Ar", bold="ArB", italic="Ar", boldItalic="ArB")

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
SAIDA = PASTA + "/processo_automatização_whatsapp.pdf"
VERDE = colors.HexColor("#0B3D2E"); VERDE_C = colors.HexColor("#E8F5EE")
VERM = colors.HexColor("#9C0006"); VERM_C = colors.HexColor("#FFC7CE")
LAR = colors.HexColor("#B45F06"); LAR_C = colors.HexColor("#FFF4C2")
AZUL = colors.HexColor("#1F4E79")

h1 = ParagraphStyle("h1", fontName="ArB", fontSize=17, textColor=VERDE, spaceAfter=4, leading=21)
h2 = ParagraphStyle("h2", fontName="ArB", fontSize=12.5, textColor=VERDE, spaceBefore=10, spaceAfter=4, leading=16)
p = ParagraphStyle("p", fontName="Ar", fontSize=10, leading=14, spaceAfter=3)
pc = ParagraphStyle("pc", fontName="Ar", fontSize=8.8, leading=11.5)
pcb = ParagraphStyle("pcb", fontName="ArB", fontSize=8.8, leading=11.5)
ph = ParagraphStyle("ph", fontName="ArB", fontSize=8.8, leading=11.5, textColor=colors.white)
peq = ParagraphStyle("peq", fontName="Ar", fontSize=8.5, leading=11, textColor=colors.HexColor("#555555"))
W = 17.6 * cm


def tab(cab, linhas, larg, cor=VERDE, negrito_1=True):
    dados = [[Paragraph(c, ph) for c in cab]] + [[Paragraph(str(c), pcb if (i == 0 and negrito_1) else pc) for i, c in enumerate(l)] for l in linhas]
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
    c.drawString(1.7 * cm, 1.1 * cm, "comprenolink.net  •  Processo de automação de convites no WhatsApp  •  v1 de 04/11/2026")
    c.drawRightString(A4[0] - 1.7 * cm, 1.1 * cm, f"Página {d.page}")
    c.restoreState()


st = []
# ------------------------------------------------------------------ 1
st += [Paragraph("Processo de automação de convites no WhatsApp", h1),
       Paragraph("Convite ao Canal \"Compre no Link - Achados do Mercado Livre\" para a base de contatos com consentimento. Complementa a planilha <b>Base_Contatos_WhatsApp.xlsx</b> e o PDF <b>Regras_de_Uso_Base_Contatos_WhatsApp.pdf</b>, na mesma pasta.", p),
       Spacer(1, 3),
       caixa("Situação em 04/11/2026", [
           "<b>Processo documentado. Automação NÃO ATIVADA.</b> Ela só liga depois que o dono escrever, no chat com o Claude, o termo do item 6. Até lá, vale o combinado anterior: o Claude só envia com \"pode enviar\" para cada lote.",
           "O limite do dia passou de 10 para <b>9 envios</b> (planilha e PDF de regras já ajustados).",
           "A base hoje tem 6 contatos, todos já convidados. Sem contatos aptos, a automação envia 0. O teto de 9 por dia só será usado quando a base crescer."], LAR_C, LAR),
       Paragraph("1. Objetivo e princípio", h2),
       Paragraph("Enviar convites de forma regular, dentro de limites seguros, <b>somente</b> para quem a planilha marca com PODE ENVIAR HOJE = SIM. A automação não procura nem inventa contatos: ela executa a fila que a planilha libera. Quem alimenta a base é o dono, o formulário do blog e o Instagram, sempre com consentimento.", p),
       Paragraph("2. Fluxo de ponta a ponta", h2),
       tab(["Etapa", "O que acontece", "Quem", "Onde fica o registro"], [
           ["1. Captação", "Pessoa informa o WhatsApp e aceita (formulário do blog, Direct, comentário, ManyChat) ou o dono indica um conhecido.", "Pessoa / dono", "Formulário, Direct, print"],
           ["2. Entrada na base", "O contato é cadastrado com origem, consentimento e prova. Formulário: importador toda segunda.", "Claude (importa) / dono (aprova)", "Aba Base"],
           ["3. Fila do dia", "A planilha calcula quem pode receber hoje e quantos ainda cabem no limite.", "Planilha", "Aba Hoje"],
           ["4. Validação prévia", "Dono confere a fila e os textos antes do primeiro bloco.", "Dono", "Aba Hoje (visto na lista)"],
           ["5. Envio", "Em 3 blocos, com 5 minutos entre mensagens, no WhatsApp Web.", "Claude", "WhatsApp Web"],
           ["6. Registro", "Cada envio vira uma linha: data, hora, contato, mensagem, enviado por, autorização, resultado.", "Claude", "Aba Envios"],
           ["7. Conferência", "A coluna Conferência precisa mostrar OK em todas as linhas do dia.", "Claude e dono", "Aba Envios"],
           ["8. Respostas", "\"Entrei\" → M3. \"Quero sair\" → M4 e saída permanente. Outras dúvidas vão ao dono.", "Claude / dono", "Aba Envios e Base"],
           ["9. Relatório e validação", "Relatório do dia com enviados, respostas, alertas e saldo. O dono valida.", "Claude / dono", "Chat + planilha"]],
          [0.15, 0.45, 0.2, 0.2]),
       PageBreak()]

# ------------------------------------------------------------------ 3
st += [Paragraph("3. Fórmula de envio", h2),
       tab(["Item", "Regra"], [
           ["Quantidade do dia", "MENOR entre: (a) teto da fase, (b) contatos com PODE ENVIAR = SIM, (c) o que resta do limite de 9 do dia. Nunca mais de 9."],
           ["Teto por fase (subida gradual)", "Semana 1: 3 por dia. Semana 2: 6 por dia. Semana 3 em diante: 9 por dia. Só sobe se a semana anterior fechou sem problema (item 7). Se houver problema, volta à fase anterior."],
           ["Blocos de envio", "Até 3 blocos por dia: 10:00, 14:00 e 18:00. Cada bloco leva até 3 mensagens. O bloco das 18:00 termina até 18:20, para não colidir com a divulgação diária das 19:12."],
           ["Intervalo", "5 minutos entre uma mensagem e outra (o mínimo da planilha é 3)."],
           ["Horário permitido", "Das 9h às 20h. Fora disso, a automação não envia."],
           ["Dias", "Todos os dias. Pausa total em 27/11 (dia D da Black Friday) e a critério do dono em feriados."],
           ["Texto", "M1 (primeiro convite) ou M2 (lembrete, só para Consentimento = Sim, depois de 7 dias, uma vez). Nome do contato trocado e saudação variada, nunca texto idêntico em sequência."],
           ["Quem entra", "Somente PODE ENVIAR = SIM. A automação nunca decide sozinha incluir alguém."],
           ["Registro", "Cada mensagem é lançada em Envios na hora, com Enviado por = Claude e Autorizado = Sim."]], [0.25, 0.75]),
       Paragraph("4. Regras de parada automática", h2),
       tab(["Se acontecer", "A automação faz"], [
           ["O WhatsApp pede verificação, captcha ou mostra aviso de conta", "Para na hora, não tenta contornar, avisa o dono e suspende por 7 dias."],
           ["Erro ao enviar ou conversa não abre", "Registra Resultado = Erro, não repete o envio e segue só com os próximos se for erro isolado."],
           ["Duas ou mais pessoas pedem para sair no mesmo dia", "Para os blocos restantes do dia e avisa o dono."],
           ["Pedidos de saída acima de 5% dos convites da semana", "Volta uma fase de ritmo e pede revisão da lista ao dono."],
           ["Coluna Conferência com ALERTA", "Para, corrige a linha e só então continua."],
           ["PC desligado, Chrome fechado ou WhatsApp Web deslogado", "Não envia. O bloco perdido NÃO é recuperado depois (sem acumular)."],
           ["Dono escreve \"pausar automação\"", "Suspende tudo imediatamente até novo \"ativar\"."]], [0.4, 0.6], cor=VERM),
       Paragraph("5. Quem faz o quê", h2),
       tab(["Tarefa", "Claude", "Dono"], [
           ["Alimentar a base (importar formulário, ler Direct e comentários, propor contatos)", "Faz e registra a prova", "Aprova os contatos pessoais"],
           ["Montar a fila do dia e os textos", "Faz", "Valida às 09:50"],
           ["Enviar nos blocos", "Faz", "Não faz nada, só mantém PC e Chrome prontos"],
           ["Registrar em Envios e conferir", "Faz", "Confere à noite"],
           ["Responder dúvidas e propostas de pessoas", "Avisa e sugere o texto", "Responde"],
           ["Mudar limites, textos, fases ou pausar", "Não muda sozinho", "Decide e escreve no chat"],
           ["Ler seguidores do Canal e atualizar metas", "Faz toda segunda", "Revisa a meta"]], [0.52, 0.24, 0.24]),
       Paragraph("6. Termo de autorização permanente (condição para ligar)", h2),
       Paragraph("A automação só liga quando o dono escrever no chat uma frase com este conteúdo (pode copiar):", p),
       caixa("Texto da autorização", [
           "\"Autorizo o Claude a enviar convites do Canal pelo WhatsApp Web, todos os dias, somente para contatos com PODE ENVIAR = SIM na planilha Base_Contatos_WhatsApp, no máximo 9 por dia, subindo de 3 para 6 e 9 por semana, entre 9h e 20h, com 5 minutos entre mensagens, usando só os textos M1 e M2, parando nas regras do item 4 do documento processo_automatização_whatsapp.pdf. Posso revogar quando quiser escrevendo 'pausar automação'.\""], VERDE_C, VERDE),
       Paragraph("A autorização vale só para este processo. Mudar o limite, o texto, o horário ou a origem dos contatos exige nova autorização. O Claude guarda a data e a frase no registro de execução.", p),
       Spacer(1, 2)]

# ------------------------------------------------------------------ 7+
st += [Paragraph("7. Implantação (datas são estimativas)", h2),
       tab(["Quando", "O que", "Quem", "Pronto quando"], [
           ["Qua 04/11", "Processo, planilha e regras documentados; formulário com WhatsApp e consentimento no ar.", "Claude", "Feito"],
           ["Qui 05/11 a dom 09/11", "Reunir contatos aptos: contatos pessoais aprovados, pedidos do Direct e do formulário.", "Dono e Claude", "Pelo menos 9 contatos com PODE ENVIAR = SIM"],
           ["Seg 09/11, 10:30", "Rodar o importador do formulário e ler os seguidores do Canal. Revisar a lista.", "Claude e dono", "Base atualizada"],
           ["Ter 10/11", "Dono escreve a autorização (item 6). Primeiro dia: fase 1, 3 envios, 1 bloco, acompanhados.", "Dono e Claude", "3 envios com Conferência OK"],
           ["10/11 a 16/11", "Fase 1: 3 por dia.", "Claude", "Semana sem alerta e com até 5% de pedidos de saída"],
           ["17/11 a 23/11", "Fase 2: 6 por dia.", "Claude", "Idem"],
           ["24/11 em diante", "Fase 3: 9 por dia. Pausa em 27/11 (Black Friday). Retoma em 28/11.", "Claude", "Revisão semanal toda segunda"]], [0.17, 0.43, 0.14, 0.26]),
       Paragraph("Se não houver contatos aptos suficientes até 09/11, a primeira fase só começa quando houver. Não se reduz a exigência de consentimento para cumprir a data.", p),
       Paragraph("8. Atribuições do dono no gerenciamento", h2),
       tab(["Atribuição", "Quando", "Tempo", "Como faz", "Onde registra"], [
           ["Garantir que o PC e o Chrome estejam prontos: WhatsApp Web logado, Claude aberto, PC ligado e sem suspensão", "Todo dia, até 09:50", "2 min", "Abrir o Chrome e conferir o WhatsApp Web", "Visto no checklist do item 10"],
           ["Validar a fila do dia e os textos", "Todo dia, 09:50", "3 min", "Abrir a aba Hoje, ver nomes e mensagens. Se algo estiver estranho, escrever \"pausar automação\"", "Checklist do item 10"],
           ["Responder dúvidas de pessoas que escreverem", "Todo dia, 19:20", "5 min", "Responder conversas do WhatsApp e do Instagram", "Aba Envios, Resultado = Respondeu (Claude registra)"],
           ["Validação final do dia", "Todo dia, 20:30", "5 min", "Ler o relatório do Claude e abrir a aba Envios: nenhuma linha com ALERTA, no máximo 9 envios", "Checklist do item 10"],
           ["Aprovar contatos pessoais novos", "Seg e qui, 10:30", "5 min", "Escolher quem pode receber e informar o número ao Claude", "Aba Base (Claude cadastra)"],
           ["Revisar a semana: seguidores do Canal, saídas, taxa de entrada e fase de ritmo", "Seg, 10:30", "15 min", "Ver a aba Canal e o resumo do Claude. Decidir subir, manter ou reduzir", "Aba Canal e este documento"],
           ["Atender verificação do WhatsApp ou aviso de conta", "Quando ocorrer", "5 min", "Resolver no celular e avisar o Claude", "Aba Envios, Observações"],
           ["Revisão mensal de consentimentos e exclusões", "Dia 1 de cada mês, 10:30", "20 min", "Atender pedidos de exclusão, apagar dados e guardar backup", "Aba Base e pasta _backups"]],
          [0.27, 0.14, 0.1, 0.28, 0.21]),
       Spacer(1, 2),
       Paragraph("9. Agenda de execução diária", h2),
       tab(["Horário", "Quem", "O que acontece", "Condição"], [
           ["09:50", "Dono", "Valida a fila e os textos (3 min)", "PC ligado, WhatsApp Web logado"],
           ["10:00", "Claude", "Bloco 1: até 3 envios, 5 min entre eles", "Fila do dia com SIM"],
           ["14:00", "Claude", "Bloco 2: até 3 envios", "Ainda há saldo no limite do dia"],
           ["18:00 a 18:20", "Claude", "Bloco 3: até 3 envios. Termina antes das 19:12", "Idem"],
           ["19:12", "Claude", "Divulgação diária (Status, Canal e Story). Não faz parte deste processo, mas divide o mesmo Chrome", "Tarefa agendada já existente"],
           ["19:20", "Dono", "Responde as pessoas que escreveram (5 min)", "-"],
           ["20:30", "Dono", "Validação final do dia (5 min)", "Relatório do Claude disponível"],
           ["Seg 10:30", "Claude e dono", "Importar formulário, ler seguidores do Canal, revisar semana e fase", "-"]], [0.14, 0.14, 0.5, 0.22]),
       Paragraph("Se o PC estiver desligado ou o Chrome fechado no horário de um bloco, o bloco não acontece e não é recuperado depois. Nada é enviado fora da janela das 9h às 20h.", p),
       Paragraph("10. Validação diária (checklist)", h2),
       Paragraph("Dono marca todos os dias às 20:30. Qualquer \"não\" vira ação no dia seguinte, sem replanejar o processo.", p),
       tab(["Item", "Critério de OK", "Se falhar"], [
           ["1. Fila foi validada às 09:50?", "Nomes e textos conferidos", "Pausar e corrigir a Base"],
           ["2. Total de envios do dia", "Entre 0 e 9, nunca acima do teto da fase", "Pausar e investigar"],
           ["3. Coluna Conferência (aba Envios)", "Todas as linhas do dia com OK", "Corrigir a linha e registrar o motivo"],
           ["4. Todos enviados tinham PODE ENVIAR = SIM?", "Sim, sem exceção", "Pausar a automação e rever as regras"],
           ["5. Pedidos para sair", "Todos registrados e atendidos com M4", "Registrar hoje; se 2 ou mais, parar"],
           ["6. Avisos do WhatsApp (verificação, limite, conta)", "Nenhum", "Parar 7 dias e avisar o Claude"],
           ["7. Novos seguidores do Canal e respostas", "Anotados no relatório", "Pedir ao Claude para anotar"]], [0.38, 0.32, 0.3]),
       Paragraph("11. Quadro de validação (14 dias)", h2),
       Paragraph("Imprimir ou copiar para a planilha. Marque V (validado) ou X (problema) e escreva a ação.", p),
       tab(["Data", "Envios do dia", "Alertas", "Saídas", "Entraram", "Validado V/X", "Ação"],
           [[d, "", "", "", "", "", ""] for d in ["10/11", "11/11", "12/11", "13/11", "14/11", "15/11", "16/11", "17/11", "18/11", "19/11", "20/11", "21/11", "22/11", "23/11"]],
           [0.1, 0.14, 0.1, 0.1, 0.12, 0.14, 0.3]),
       Spacer(1, 2),
       Paragraph("12. Indicadores semanais (toda segunda)", h2),
       tab(["Indicador", "Meta", "Leitura"], [
           ["Envios na semana", "Dentro do teto da fase", "Compara com o que a base permitiu"],
           ["Contatos que entraram no Canal", "Meta de seguidores: 10 até 10/11 e 20 até 30/11 (estimativa)", "Se estiver abaixo, rever origem dos contatos"],
           ["Taxa de entrada", "Acima de 15% dos convites enviados (estimativa)", "Abaixo de 5%: texto ou origem fracos"],
           ["Pedidos para sair", "Até 5% dos convites", "Acima de 5%: reduzir um nível de ritmo"],
           ["Alertas na Conferência e erros", "0", "Qualquer alerta é causa de revisão"]], [0.3, 0.4, 0.3]),
       Paragraph("13. Limites e riscos (leia antes de autorizar)", h2),
       caixa("Honestidade sobre o que a automação é", [
           "O envio é feito pelo WhatsApp Web, controlando o navegador. <b>Não é a API oficial do WhatsApp.</b> Mesmo com os limites, existe risco de o WhatsApp restringir o número se muitas pessoas denunciarem, bloquearem ou ignorarem. Por isso a subida é gradual e há parada automática.",
           "A automação depende do PC ligado, do Chrome aberto e do WhatsApp Web logado. Se um desses faltar, o bloco não acontece.",
           "O ganho é pequeno: a base é feita só de gente que aceitou ou conhece o dono. O crescimento mais forte vem de blog, Instagram, Status e indicação.",
           "Para escalar de verdade e dentro das regras, o caminho é a plataforma oficial (WhatsApp Business Platform, via ManyChat ou similar). Isso tem custo e aprovação de modelos e não faz parte deste processo.",
           "O material não substitui parecer jurídico sobre a LGPD."], LAR_C, LAR),
       Paragraph("14. Registro de execução", h2),
       tab(["Data", "Evento", "Responsável"], [
           ["04/11/2026", "Processo documentado. Limite do dia ajustado de 10 para 9. Automação NÃO ativada.", "Claude"],
           ["", "Autorização permanente do dono (data e frase)", "Dono"],
           ["", "Início da fase 1 (3 por dia)", "Claude"],
           ["", "Início da fase 2 (6 por dia)", "Claude"],
           ["", "Início da fase 3 (9 por dia)", "Claude"]], [0.18, 0.62, 0.2]),
       Spacer(1, 6),
       Paragraph("Versão 1 - 04/11/2026. Complementa: Base_Contatos_WhatsApp.xlsx e Regras_de_Uso_Base_Contatos_WhatsApp.pdf.", peq)]

doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.7 * cm, rightMargin=1.7 * cm, topMargin=1.6 * cm, bottomMargin=1.8 * cm,
                        title="Processo de automação de convites no WhatsApp", author="comprenolink.net")
doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
print("OK:", SAIDA)
