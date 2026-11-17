# -*- coding: utf-8 -*-
"""Gera Regras_de_Uso_Base_Contatos_WhatsApp.pdf (fica ao lado da planilha)."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Ar", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("ArB", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFontFamily("Ar", normal="Ar", bold="ArB", italic="Ar", boldItalic="ArB")

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
SAIDA = PASTA + "/Regras_de_Uso_Base_Contatos_WhatsApp.pdf"
VERDE = colors.HexColor("#0B3D2E"); VERDE_C = colors.HexColor("#E8F5EE")
VERM = colors.HexColor("#9C0006"); VERM_C = colors.HexColor("#FFC7CE")
AMAR_C = colors.HexColor("#FFF4C2")

h1 = ParagraphStyle("h1", fontName="ArB", fontSize=17, textColor=VERDE, spaceAfter=4, leading=21)
h2 = ParagraphStyle("h2", fontName="ArB", fontSize=12.5, textColor=VERDE, spaceBefore=10, spaceAfter=4, leading=16)
p = ParagraphStyle("p", fontName="Ar", fontSize=10, leading=14, spaceAfter=3)
pc = ParagraphStyle("pc", fontName="Ar", fontSize=9, leading=12)
pcb = ParagraphStyle("pcb", fontName="ArB", fontSize=9, leading=12)
ph = ParagraphStyle("ph", fontName="ArB", fontSize=9, leading=12, textColor=colors.white)
peq = ParagraphStyle("peq", fontName="Ar", fontSize=8.5, leading=11, textColor=colors.HexColor("#555555"))


def tab(cab, linhas, larg, cor=VERDE):
    dados = [[Paragraph(c, ph) for c in cab]] + [[Paragraph(str(c), pcb if i == 0 else pc) for i, c in enumerate(l)] for l in linhas]
    t = Table(dados, colWidths=[w * 17.6 * cm for w in larg], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), cor), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F7F7")]),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def caixa(titulo, itens, fundo, borda):
    corpo = [Paragraph(f"<b>{titulo}</b>", p)] + [Paragraph("• " + i, p) for i in itens]
    t = Table([[corpo]], colWidths=[17.6 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fundo), ("BOX", (0, 0), (-1, -1), 1, borda),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def rodape(c, d):
    c.saveState()
    c.setFont("Ar", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(1.7 * cm, 1.1 * cm, "comprenolink.net  •  Base de Contatos WhatsApp  •  regras de uso")
    c.drawRightString(A4[0] - 1.7 * cm, 1.1 * cm, f"Página {d.page}")
    c.restoreState()


st = []
st += [Paragraph("Base de Contatos WhatsApp: regras de uso", h1),
       Paragraph("Planilha <b>Base_Contatos_WhatsApp.xlsx</b> (nesta mesma pasta). Versão 1, criada em 04/11/2026. Este documento explica o que a planilha faz, quem pode receber o convite do Canal e como usar todo dia.", p),
       Spacer(1, 4),
       caixa("Regra de ouro", [
           "Só recebe convite quem <b>aceitou receber</b> ou quem <b>conhece o dono pessoalmente</b>. Nunca estranhos, nunca lista comprada ou copiada.",
           "Só se envia para quem aparece na aba <b>Hoje</b> (coluna PODE ENVIAR = SIM), até o <b>limite do dia (9)</b>, entre <b>9h e 20h</b>, com intervalo mínimo de <b>3 minutos</b> entre mensagens.",
           "Todo envio é <b>registrado</b> na aba Envios. Sem registro, a planilha não sabe e a regra não protege."], VERDE_C, VERDE),
       Paragraph("1. Objetivo", h2),
       Paragraph("Criar uma base própria, pequena e permitida, para convidar pessoas ao Canal do WhatsApp (Compre no Link - Achados do Mercado Livre) sem arriscar o número da loja. O convite pessoal tem um teto: a base cresce principalmente por quem chega pelo blog, pelo Instagram e pelo Status e aceita receber.", p),
       Paragraph("2. O que tem na pasta", h2),
       tab(["Arquivo / pasta", "Para que serve"], [
           ["Base_Contatos_WhatsApp.xlsx", "A planilha: Hoje, Base, Envios, Canal, Mensagens e Parametros."],
           ["Regras_de_Uso_Base_Contatos_WhatsApp.pdf", "Este documento."],
           ["_fonte\\gerar_base_contatos.py", "Gera a planilha do zero (apaga os dados: usar só se a planilha estragar; antes, copie o arquivo)."],
           ["_fonte\\importar_leads_formulario.py", "Traz para a Base quem se inscreveu no formulário do blog com WhatsApp e consentimento."],
           ["_fonte\\gerar_regras_pdf.py", "Gera este PDF."],
           ["_backups", "Cópias automáticas feitas antes de qualquer gravação pelos scripts."]], [0.47, 0.53]),
       Paragraph("3. As abas da planilha", h2),
       tab(["Aba", "O que é", "Quem mexe"], [
           ["Hoje", "Resumo do dia (quantos já foram, quantos restam) e a fila: quem pode receber agora, qual mensagem usar e botão Abrir conversa.", "Só lê. Tudo é automático."],
           ["Base", "Um contato por linha: nome, WhatsApp, origem, consentimento, se entrou no Canal, se pediu para sair. A coluna PODE ENVIAR HOJE? decide sozinha.", "Dono ou Claude, nas colunas amarelas."],
           ["Envios", "Um envio por linha: data, hora, contato, mensagem, quem enviou, autorização e resultado. Tem a coluna Conferência com alertas.", "Dono ou Claude, nas colunas amarelas."],
           ["Canal", "Número de seguidores do Canal em cada segunda e as metas.", "Dono ou Claude, toda segunda."],
           ["Mensagens", "Os 4 textos prontos (M1 convite, M2 lembrete, M3 agradecimento, M4 resposta a quem pede para sair).", "Só lê. Para mudar o texto, falar com o Claude."],
           ["Parametros", "Limites (9 por dia, 2 e 1 convite por contato, 7 dias entre convites, horário 9h a 20h) e as listas de escolha.", "Só o dono muda."]],
          [0.16, 0.56, 0.28]),
       Paragraph("Cores: <b>amarelo</b> = você digita; <b>cinza</b> = fórmula, não digitar por cima; <b>verde</b> = pode; <b>vermelho</b> = não enviar ou alerta.", p),
       PageBreak(),
       Paragraph("4. Quem pode receber (consentimento)", h2),
       tab(["Valor na coluna Consentimento", "Significa", "Quantos convites"], [
           ["Sim", "A pessoa pediu ou aceitou receber (formulário do blog com a caixa marcada, respondeu \"quero\" no Instagram ou no Direct, pediu pessoalmente).", "Até 2 (convite + 1 lembrete depois de 7 dias)."],
           ["Conhecido", "Conhece o dono pessoalmente (família, amigo, cliente), mas não pediu. Convite de cortesia.", "Só 1. Se a pessoa responder positivo, mude para Sim."],
           ["Não", "Recusou ou não quer.", "Nenhum."],
           ["Não perguntado", "Entrou na base sem nenhuma relação nem aceite.", "Nenhum. Nunca entra na fila."]], [0.22, 0.5, 0.28]),
       Paragraph("Registre sempre, na coluna <b>Como consentiu</b>, a prova: \"respondeu quero no Direct em 05/11\", \"formulário do blog, entrada nº 12\", \"cliente que comprou em ...\". Se não houver prova, o consentimento não vale.", p),
       Paragraph("5. Como a planilha decide \"PODE ENVIAR HOJE?\"", h2),
       Paragraph("A coluna olha as condições nesta ordem e para na primeira que falhar. Só aparece <b>SIM</b> se passar em todas.", p),
       tab(["Resultado", "Motivo"], [
           ["NÃO: pediu para sair", "Marcado na Base ou registrado em Envios como Pediu para sair. Permanente."],
           ["NÃO: já entrou no Canal", "Marcado na Base ou registrado como Entrou no Canal. Não precisa de convite."],
           ["NÃO: sem consentimento", "Consentimento diferente de Sim ou Conhecido."],
           ["NÃO: limite de convites", "Já recebeu o máximo (2 para Sim, 1 para Conhecido)."],
           ["NÃO: aguardar N dia(s)", "O último envio foi há menos de 7 dias."],
           ["NÃO: número inválido", "O WhatsApp deve ter só números, começar com 55 e ter 12 ou 13 dígitos (55 + DDD + número)."],
           ["SIM", "Pode entrar na fila de hoje, se ainda houver vaga no limite do dia."]], [0.3, 0.7]),
       Paragraph("6. Rotina diária (5 a 10 minutos)", h2),
       tab(["Passo", "O que fazer"], [
           ["1", "Abra a planilha e vá na aba <b>Hoje</b>. Veja \"Restam hoje\" e \"Podem receber neste lote\"."],
           ["2", "Para cada nome da lista: clique em <b>Abrir conversa</b>, copie a mensagem da aba Mensagens (troque {nome}) e envie. Espere pelo menos 3 minutos entre um envio e outro."],
           ["3", "Logo depois de cada envio, registre uma linha em <b>Envios</b>: data, hora, ID, mensagem (M1 ou M2), tipo, enviado por, Autorizado = Sim, Resultado = Enviado."],
           ["4", "Confira a coluna <b>Conferência</b>: tem de estar OK. ALERTA = corrigir antes de continuar."],
           ["5", "Quando alguém responder: \"entrou\" → Resultado = Entrou no Canal e envie M3. \"Quero sair\" → Resultado = Pediu para sair e envie M4."],
           ["6", "Se a lista da aba Hoje estiver vazia, não há quem convidar: cadastre novos contatos permitidos (item 7) e pare por hoje."]], [0.1, 0.9]),
       PageBreak(),
       Paragraph("7. Como cadastrar contatos (somente fontes permitidas)", h2),
       tab(["Origem", "Como entra na Base", "Consentimento"], [
           ["Formulário do blog", "Pessoa preenche o WhatsApp e marca a caixa \"Aceito receber o convite do Canal e ofertas no WhatsApp\". O script importar_leads_formulario.py traz para a Base toda segunda. Sem a caixa marcada, não entra.", "Sim"],
           ["Instagram: comentou ou chamou no Direct", "Quem comenta BLACK ou pede o link e informa o número. Registrar print ou data.", "Sim"],
           ["ManyChat", "Quem aceitou a conversa automática e pediu o link.", "Sim"],
           ["Cliente", "Quem já conversou ou comprou com a loja e pediu contato.", "Sim ou Conhecido"],
           ["Contato pessoal", "Família, amigos e colegas que você conhece. Você decide quem.", "Conhecido"],
           ["Indicação", "Quem o dono ou um seguidor indicou e <b>a pessoa indicada aceitou</b>.", "Sim só depois do aceite"]], [0.22, 0.6, 0.18]),
       Spacer(1, 4),
       caixa("Nunca fazer", [
           "Comprar, baixar ou usar lista de números. Não copiar membros de grupos, seguidores de outros perfis ou números de sites.",
           "Enviar para quem não está na aba Hoje, ou acima de 9 por dia, ou fora das 9h às 20h.",
           "Enviar o mesmo texto idêntico para todos de uma vez. Trocar o nome e variar a saudação.",
           "Insistir com quem não respondeu: máximo 1 lembrete, só para Sim, depois de 7 dias.",
           "Usar preço, \"mais vendido\" ou promessa nos convites."], VERM_C, VERM),
       Paragraph("8. Envios feitos pelo Claude", h2),
       Paragraph("O Claude só envia quando o dono autoriza <b>expressamente cada lote</b>. A autorização de um dia não vale para o outro.", p),
       tab(["Etapa", "O que acontece"], [
           ["1", "O Claude abre a aba Hoje e monta o lote com <b>no máximo o que ainda resta no dia</b> (nunca mais de 9)."],
           ["2", "Mostra ao dono a <b>lista de nomes</b> e o <b>texto final de cada um</b>."],
           ["3", "O dono responde \"pode enviar\" para aquele lote. Sem essa frase, nada é enviado."],
           ["4", "O Claude envia pelo WhatsApp Web, com <b>3 minutos ou mais</b> entre as mensagens, dentro do horário."],
           ["5", "Registra cada envio em Envios com Enviado por = Claude e Autorizado = Sim, e confere a coluna Conferência."],
           ["6", "Informa ao dono o que foi enviado e as respostas. Se a conta pedir verificação ou der erro, <b>para na hora</b> e avisa."]], [0.1, 0.9]),
       Paragraph("9. Contagem do Canal toda segunda", h2),
       Paragraph("Na segunda-feira: abrir WhatsApp Web &gt; Canais &gt; Compre no Link e anotar na aba <b>Canal</b> a data e o número de seguidores. A planilha calcula quantos entraram desde a leitura anterior e quanto falta para a meta (estimativa: 10 até 10/11/2026 e 20 até 30/11/2026, a rever com os números). Se o Canal crescer mais do que isso, as metas sobem.", p),
       PageBreak(),
       Paragraph("10. Captação pelo blog (formulário)", h2),
       Paragraph("O formulário \"Alertas Black Friday e Natal\" (form 4) ganhou em 04/11/2026 dois campos <b>opcionais</b>: <b>WhatsApp (opcional)</b> e a caixa <b>\"Aceito receber o convite do Canal e ofertas no WhatsApp\"</b>. Ele já aparece na página da Black Friday. Backup do formulário antes da mudança: <i>9_Manutenção_Blog\\2_DADOS\\Blog_WordPress\\backups\\fluentform4_antes_whatsapp_2026-11-04_16h34.json</i>.", p),
       tab(["Situação do inscrito", "O que acontece"], [
           ["Preencheu WhatsApp e marcou a caixa", "Entra na Base como Consentimento = Sim, origem Blog - formulário, e passa a aparecer na fila."],
           ["Preencheu o número e não marcou a caixa", "Não entra. Sem aceite explícito, não há convite."],
           ["Só e-mail", "Continua recebendo só os alertas por e-mail, como antes."]], [0.47, 0.53]),
       Paragraph("Para importar: feche o Excel, abra o terminal e rode <b>python -X utf8 importar_leads_formulario.py</b> (só simula) e depois <b>python -X utf8 importar_leads_formulario.py --gravar</b>. O script ignora número repetido e faz backup da planilha antes de gravar. Nesta data o formulário ainda não tinha nenhuma inscrição.", p),
       Paragraph("11. Cuidados com a lei e com o WhatsApp", h2),
       Paragraph("• Guarde só o necessário (nome, número, origem, consentimento e prova). Não compartilhe a planilha com terceiros.<br/>"
                 "• A pessoa pode pedir a saída ou a exclusão dos dados a qualquer momento: marcar Pediu para sair e, se pedir exclusão, apagar a linha da Base e os dados pessoais dos registros.<br/>"
                 "• Muitas denúncias ou bloqueios podem restringir o número da loja. Se notar que muitas pessoas não respondem ou bloqueiam, reduza o ritmo.<br/>"
                 "• Este material é orientação prática do projeto e não substitui parecer jurídico.", p),
       Paragraph("12. Se algo der errado", h2),
       tab(["Problema", "O que fazer"], [
           ["Fórmula mostra #NOME?", "O Excel é antigo. A planilha precisa do Microsoft Excel 2019 ou 365 (função MAXIFS). Testada no Excel instalado neste PC em 04/11/2026."],
           ["Planilha estragou ou apagou fórmulas", "Copiar o último arquivo de _backups e voltar. Em último caso, gerar de novo com gerar_base_contatos.py (os dados serão recriados do zero)."],
           ["Importador não grava", "Fechar o Excel e rodar de novo. O arquivo aberto no Excel fica bloqueado."],
           ["Conferência com ALERTA", "Corrigir a linha (autorização, horário, limite do dia ou contato sem consentimento) e não repetir o erro."],
           ["WhatsApp avisou ou limitou o número", "Parar todos os envios por 7 dias e avisar o Claude. Não tentar contornar."]], [0.35, 0.65]),
       Spacer(1, 6),
       Paragraph("Versão 1 - 04/11/2026. Dados já lançados: 7 envios de convite feitos pelo dono em 04/11 (6 contatos conhecidos), 2 seguidores no Canal.", peq)]

doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.7 * cm, rightMargin=1.7 * cm, topMargin=1.6 * cm, bottomMargin=1.8 * cm,
                        title="Base de Contatos WhatsApp: regras de uso", author="comprenolink.net")
doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
print("OK:", SAIDA)
