# -*- coding: utf-8 -*-
"""Gera processo_crescimento_canal_whatsapp.pdf (v2, 04/11/2026 noite)."""
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
SAIDA = PASTA + "/processo_crescimento_canal_whatsapp.pdf"
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
    c.drawString(1.7 * cm, 1.1 * cm, "comprenolink.net  •  Crescimento seguro do Canal no WhatsApp  •  v2 de 04/11/2026")
    c.drawRightString(A4[0] - 1.7 * cm, 1.1 * cm, f"Página {d.page}")
    c.restoreState()

st = []
st += [Paragraph("Crescimento seguro do Canal no WhatsApp", h1),
       Paragraph("Versão 2, de 04/11/2026 (noite). <b>Substitui</b> o antigo \"Processo de automação de convites\" (v1, guardado em _backups\\obsoleto_automacao). Complementa a planilha <b>Base_Contatos_WhatsApp.xlsx</b> e o PDF <b>Regras_de_Uso_Base_Contatos_WhatsApp.pdf</b>, na mesma pasta.", p),
       Spacer(1, 3),
       caixa("O que mudou e por quê", [
           "<b>A automação de convites foi CANCELADA.</b> Ela nunca foi ligada e nenhuma mensagem automática foi enviada. A conta do WhatsApp do blog continua intacta.",
           "Motivo: enviar convite para muita gente pelo WhatsApp Web, mesmo com limites, pode levar à restrição do número se houver denúncias ou bloqueios, e esse tipo de envio vai contra os termos do WhatsApp. O ganho não compensa o risco de perder o número da loja.",
           "<b>Nova regra fixa:</b> nenhum envio em massa e nenhuma automação de mensagens pelo WhatsApp Web, nem por tarefa agendada. Quem entra no Canal é quem <b>pede para entrar</b> ou quem o dono convida pessoalmente."], VERM_C, VERM),
       Paragraph("1. Análise de risco de cada método", h2),
       tab(["Método", "Risco", "Decisão"], [
           ["Automação de convites pelo WhatsApp Web (blocos, fases 3/6/9)", "ALTO: restrição ou perda do número", "NÃO usar. Cancelada."],
           ["Mensagem em massa para a agenda importada (José e Rosana)", "ALTO: denúncias de quem não conhece a loja", "NÃO enviar. A agenda fica só como cadastro, pendente."],
           ["Convite à mão, pelo celular do dono, só para quem ele conhece, até 9 por dia", "BAIXO, se seguir os cuidados do item 4", "PERMITIDO."],
           ["Link do Canal no Status, na bio, no blog, nos Reels e nas respostas do Direct", "NENHUM: a pessoa entra por conta própria", "USAR todo dia."],
           ["\"Comente CANAL\" no Instagram com resposta automática do ManyChat", "BAIXO: só responde a quem comentou ou escreveu", "USAR. Teste em 11/11."],
           ["E-mail com consentimento (formulário do blog)", "BAIXO: só para quem aceitou; vale a LGPD", "USAR na Black Friday e no Natal."],
           ["WhatsApp Business Platform oficial (envio em massa permitido)", "BAIXO, mas tem custo e aprovação de modelos", "Fora do plano, sem verba por ora."]], [0.46, 0.30, 0.24], cor=VERM),
       Paragraph("2. O plano em 4 frentes", h2),
       tab(["Frente", "O que fazer", "Quem"], [
           ["1. Atrair", "Chamada para o Canal em todo Status (19:12), Stories com link, bio, blog e Reels. Texto: \"Quer a oferta antes de todo mundo? Entre no Canal\".", "Claude (rotina) e dono"],
           ["2. \"Comente CANAL\"", "Reels e posts pedem a palavra CANAL. O ManyChat responde no Direct com o link. Texto pronto até qui 05/11, 10:20 (ação G1).", "Claude escreve, dono cola"],
           ["3. Convite pessoal à mão", "O dono aprova na planilha quem conhece de verdade (Consentimento = Conhecido) e envia pelo seu celular, uma mensagem personalizada por pessoa.", "Dono"],
           ["4. Oferta exclusiva", "Cupom, aviso de preço ou oferta relâmpago só no Canal, principalmente na Black Friday, para dar motivo de entrar.", "Claude propõe, dono aprova"],
           ["Depois da Black Friday", "Telegram e e-mail com consentimento como canais extras.", "Dono decide"]], [0.17, 0.6, 0.23]),
       PageBreak(),
       Paragraph("3. Quem faz o quê", h2),
       tab(["Tarefa", "Claude", "Dono"], [
           ["Postar a divulgação diária (Status, Canal e Story) às 19:12", "Faz (tarefa agendada)", "Mantém PC, Claude e Chrome ligados"],
           ["Preparar a lista do dia e os textos dos convites pessoais", "Faz, só prepara", "Valida"],
           ["<b>Enviar</b> os convites pessoais", "<b>Não envia</b>", "Envia à mão, pelo celular"],
           ["Registrar os envios na aba Envios", "Registra o que o dono informar", "Informa o que enviou"],
           ["Responder dúvidas e propostas", "Sugere o texto", "Responde"],
           ["Ler seguidores do Canal e anotar na aba Canal", "Faz toda segunda", "Revisa a meta"],
           ["Importar inscritos do formulário do blog", "Faz toda segunda (com consentimento marcado)", "Aprova"],
           ["Aprovar contatos pessoais (Conhecido)", "Propõe e cadastra", "Decide quem"]], [0.5, 0.26, 0.24]),
       Paragraph("4. Cuidados do convite pessoal (para não ser bloqueado)", h2),
       caixa("Regras do convite à mão", [
           "Só para quem o dono conhece e que provavelmente responderia a uma mensagem sua. Nunca desconhecidos nem lista copiada.",
           "Máximo <b>9 por dia</b>, entre 9h e 20h, com pelo menos 3 minutos entre uma e outra. Na primeira semana, no máximo <b>5 por dia</b>.",
           "Mensagem pessoal, com o nome da pessoa e saudação diferente. Nunca o mesmo texto copiado para todos, nem preço ou promessa.",
           "Um convite por pessoa. Sem resposta: não insistir.",
           "Quem pedir para sair é marcado como <b>Pediu para sair</b> na hora e nunca mais recebe nada."], VERDE_C, VERDE),
       Paragraph("5. Quando parar", h2),
       tab(["Se acontecer", "O que fazer"], [
           ["O WhatsApp pede verificação ou mostra aviso na conta", "Parar todos os convites por 7 dias e avisar o Claude. Não tentar contornar."],
           ["2 ou mais pessoas pedem para sair, ou 1 denúncia ou bloqueio conhecido", "Parar os convites do dia e rever a lista."],
           ["Pedidos de saída acima de 5% da semana", "Reduzir para metade e rever a lista."],
           ["Aviso do Instagram, do ManyChat ou do Mercado Livre", "Parar a ação que gerou o aviso e avisar o Claude."],
           ["Dúvida se algo é permitido", "Perguntar ao Claude antes. A resposta vem com o risco no começo."]], [0.45, 0.55], cor=VERM),
       Paragraph("6. Agenda diária e semanal", h2),
       tab(["Quando", "Quem", "O que", "Tempo"], [
           ["Todo dia, 10:00", "Dono", "Convites pessoais à mão (até 9; até 5 na 1ª semana), da lista que o Claude prepara", "15 min"],
           ["Todo dia, 19:12", "Claude", "Divulgação: Status, Canal e Story, com a chamada para o Canal", "automático"],
           ["Todo dia, 19:20", "Dono", "Responder quem escreveu (WhatsApp, Instagram)", "5 min"],
           ["Todo dia, 20:30", "Dono", "Fechar o dia: anotar enviados, saídas e entradas", "2 min"],
           ["Segunda, 10:30", "Claude e dono", "Importar o formulário, ler seguidores do Canal e revisar a semana", "15 min"],
           ["Quinta, 10:30", "Dono", "Aprovar contatos pessoais novos (Conhecido)", "5 min"],
           ["Dia 1 do mês, 10:30", "Dono", "Revisar consentimentos e atender exclusões", "20 min"]], [0.2, 0.15, 0.55, 0.1]),
       Paragraph("7. Indicadores semanais (toda segunda)", h2),
       tab(["Indicador", "Meta", "Leitura"], [
           ["Seguidores do Canal", "10 até 10/11 e 20 até 30/11 (estimativa; subir se crescer)", "Se abaixo, reforçar o \"Comente CANAL\" e a chamada no Status"],
           ["Entradas por origem", "Anotar de onde veio (bio, Status, Direct, convite)", "Mostra o que funciona"],
           ["Pedidos para sair", "Até 5% dos convites", "Acima disso, reduzir o ritmo"],
           ["Avisos do WhatsApp", "0", "Qualquer aviso para tudo por 7 dias"]], [0.25, 0.4, 0.35]),
       Paragraph("8. Base de contatos", h2),
       Paragraph("Em 04/11 a base recebeu <b>500 contatos</b> importados dos arquivos do Google Contatos (dono e Rosana), mais 55 na aba Reserva. Todos estão como <b>Não perguntado</b>, ou seja, <b>fora da fila</b>. Só passa a receber convite pessoal quem o dono mudar para <b>Conhecido</b>, em pessoa e consciente. Empresas e serviços ficaram como <b>Não</b>. Nenhuma mensagem foi enviada a esses contatos.", p),
       Paragraph("9. Como o risco é reduzido e o que fazer se houver bloqueio", h2),
       tab(["Como reduzimos o risco", "Detalhe"], [
           ["Sem envio em massa nem automação", "Nada de mensagem automática ou em lote pelo WhatsApp Web. Só convite pessoal, à mão."],
           ["Só quem conhece você", "Convite só para Conhecido aprovado por você. Agenda importada fica fora da fila."],
           ["Volume baixo e gradual", "5 por dia na semana 1, depois até 9. Intervalo de 3 minutos ou mais, das 9h às 20h."],
           ["Mensagem pessoal", "Nome, saudação diferente, sem preço nem promessa, um convite por pessoa."],
           ["Atração em vez de empurrar", "Link do Canal, Comente CANAL, Status, blog e e-mail: quem entra, pediu."],
           ["Parada rápida", "Aviso do WhatsApp, 2 saídas no dia ou denúncia: parar os convites (item 5)."],
           ["Regra permanente", "Antes de cada pedido, o Claude avisa o risco e propõe o caminho seguro."]], [0.3, 0.7], cor=VERDE),
       Spacer(1, 4),
       tab(["Se o WhatsApp restringir ou bloquear", "Solução de contorno"], [
           ["Restrição temporária (horas ou dias)", "Parar tudo, não criar outro número e esperar passar. Continuam a atração, o blog, o Instagram e o e-mail."],
           ["Bloqueio da conta", "Pedir revisão dentro do aplicativo (toque em Solicitar revisão) com o celular e o número do WhatsApp Business. Não tentar contornar com número novo antes da resposta."],
           ["Perder acesso ao Canal", "Prevenir já: adicionar um segundo administrador ao Canal (o sócio), para que o Canal não dependa de um só número."],
           ["Perder o público", "A audiência própria fica fora do WhatsApp: formulário do blog (e-mail com consentimento) e seguidores do Instagram. Dá para avisar todos de onde o Canal está."],
           ["Canal alternativo pronto", "Abrir o canal do Telegram (já previsto para depois da Black Friday) e usar o mesmo texto de chamada."],
           ["Link de entrada único", "Criar no blog uma página curta (por exemplo comprenolink.net/canal) que leva ao Canal. Se o destino mudar, troca-se em um só lugar, sem mexer na bio, no Status e nos Reels."],
           ["Número reserva", "Só depois de analisarmos os termos do WhatsApp Business e com uma conta nova e separada. Não usar para envio em massa."]], [0.3, 0.7], cor=VERM),
       Paragraph("10. Registro", h2),
       tab(["Data", "Evento", "Responsável"], [
           ["04/11/2026", "Processo de automação v1 documentado. Nunca ativado.", "Claude"],
           ["04/11/2026 (noite)", "Automação cancelada por risco de bloqueio. Processo v2 de crescimento seguro. Documentos, checklist e agenda revisados.", "Claude, a pedido do dono"],
           ["", "Primeiro dia de convites pessoais à mão", "Dono"]], [0.2, 0.6, 0.2]),
       Spacer(1, 6),
       Paragraph("Versão 2 - 04/11/2026. Regra permanente: antes de qualquer pedido, o Claude avisa se há risco de bloqueio ou de violar termos e propõe o caminho seguro.", peq)]

doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.7 * cm, rightMargin=1.7 * cm, topMargin=1.6 * cm, bottomMargin=1.8 * cm,
                        title="Crescimento seguro do Canal no WhatsApp", author="comprenolink.net")
doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
print("OK:", SAIDA)
