# -*- coding: utf-8 -*-
"""PDF "PENDENCIAS": o que o dono do blog precisa fazer, em ordem cronológica, passo a passo detalhado.
Edite as listas abaixo e rode:  python -X utf8 gerar_pendencias_detalhado.py
Saída: D:\\mercado_livre\\PENDENCIAS_Passo_a_Passo_<data>.pdf
"""
import os
import sys
from datetime import date

sys.path.insert(0, r"D:\mercado_livre\0- Pendencias\5_Plano_turbinar_anuncio_instagram")
from gerar_pdf_plano_turbinar import (AMARELO, AZUL_C, CINZA, CLARO, ESCURO, LARANJA, LARANJA_C, S, VERDE,  # noqa: E402
                                      VERDE_C, VERMELHO, VERMELHO_C)
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

HOJE = date(2026, 10, 29)
SAIDA = rf"D:/mercado_livre/0- Pendencias/1_Pendencias/0-PENDENCIAS_Passo_a_Passo_{HOJE:%Y-%m-%d}.pdf"
W, H = A4
LARG = W - 3.2 * cm
ROXO, ROXO_C = colors.HexColor("#6D28D9"), colors.HexColor("#EDE9FE")
AZUL = colors.HexColor("#0369A1")

P = lambda t, e="p": Paragraph(t, S[e])  # noqa: E731
CODE = ParagraphStyle("code", fontName="Arial", fontSize=8.6, leading=11.6, textColor=ESCURO)
PASSO = ParagraphStyle("passo", fontName="Arial", fontSize=9.6, leading=13.4, textColor=ESCURO)
NUM = ParagraphStyle("num", fontName="Arial-B", fontSize=12, leading=14, textColor=colors.white, alignment=1)


def caixa_texto(titulo, texto, cor=AZUL_C):
    """Texto pronto para copiar (caixa azul clara)."""
    t = Table([[Paragraph(f"<b>{titulo}</b>", ParagraphStyle("ct", parent=CODE, fontName="Arial-B"))],
               [Paragraph(texto.replace("&", "&amp;").replace("\n", "<br/>"), CODE)]], colWidths=[LARG - 0.4 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), cor), ("BOX", (0, 0), (-1, -1), 0.5, CINZA),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def passos(lista, cor):
    """lista de (título curto, detalhe). Número em quadro colorido + texto."""
    linhas = []
    for i, (tit, det) in enumerate(lista, 1):
        corpo = f"<b>{tit}</b>" + (f"<br/>{det}" if det else "")
        linhas.append([Paragraph(str(i), NUM), Paragraph(corpo, PASSO)])
    t = Table(linhas, colWidths=[0.9 * cm, LARG - 0.9 * cm])
    st = [("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
          ("LINEBELOW", (1, 0), (1, -1), 0.3, colors.HexColor("#D1D5DB"))]
    for r in range(len(linhas)):
        st.append(("BACKGROUND", (0, r), (0, r), cor))
    t.setStyle(TableStyle(st))
    return t


def info(linhas):
    t = Table([[P(f"<b>{a}</b>", "cel"), P(b, "cel")] for a, b in linhas], colWidths=[3.2 * cm, LARG - 3.2 * cm])
    t.setStyle(TableStyle([("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")), ("BACKGROUND", (0, 0), (0, -1), CLARO),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 4),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def faixa(num, titulo, quando, cor):
    t = Table([[Paragraph(f"<font size=22><b>{num}</b></font>",
                          ParagraphStyle("fn", fontName="Arial-B", textColor=colors.white, alignment=1, leading=26)),
                Paragraph(f"<font size=14><b>{titulo}</b></font><br/><font size=10>{quando}</font>",
                          ParagraphStyle("ft", fontName="Arial", textColor=colors.white, leading=18))]],
              colWidths=[1.6 * cm, LARG - 1.6 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), cor), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def bloco(titulo, itens, cor, fundo):
    corpo = [Paragraph(f"<b>{titulo}</b>", ParagraphStyle("bt", fontName="Arial-B", fontSize=10, leading=13, textColor=cor))]
    corpo += [Paragraph("• " + i, PASSO) for i in itens]
    t = Table([[corpo]], colWidths=[LARG])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fundo), ("BOX", (0, 0), (-1, -1), 0.6, cor),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8)]))
    return t


def tabela(cab, linhas, larguras, cor=ESCURO, tam="cel"):
    dados = [[P(f"<b>{c}</b>", "cab") for c in cab]] + [[P(str(c), tam) for c in l] for l in linhas]
    t = Table(dados, colWidths=[LARG * w for w in larguras], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), cor), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    for r in range(2, len(dados), 2):
        st.append(("BACKGROUND", (0, r), (-1, r), CLARO))
    t.setStyle(TableStyle(st))
    return t


def cabecalho_rodape(c, doc):
    c.saveState()
    c.setFillColor(ESCURO)
    c.rect(0, H - 1.5 * cm, W, 1.5 * cm, fill=1, stroke=0)
    c.setFillColor(AMARELO)
    c.rect(0, H - 1.6 * cm, W, 0.1 * cm, fill=1, stroke=0)
    c.setFont("Arial-B", 12)
    c.drawString(1.6 * cm, H - 1.0 * cm, "PENDÊNCIAS – passo a passo")
    c.setFont("Arial", 8.5)
    c.setFillColor(colors.white)
    c.drawRightString(W - 1.6 * cm, H - 1.0 * cm, f"comprenolink.net  •  @compre.no.link  •  gerado em {HOJE:%d/%m/%Y}")
    c.setFillColor(CINZA)
    c.setFont("Arial", 8)
    c.drawString(1.6 * cm, 0.8 * cm, "WhatsApp do blog (11) 99495-9657  •  dúvida? escreva ao Claude com um print da tela")
    c.drawRightString(W - 1.6 * cm, 0.8 * cm, f"Página {doc.page}")
    c.restoreState()


# ============================================================ CONTEÚDO
RESUMO = [
    ("1", "qui 29/10", "18:55 → 19:30", "Deixar tudo aberto para o Claude agendar o post e o Reels de 27/11", "0 min (só deixar ligado)"),
    ("2", "sex 30/10", "19:00", "Testar a automação BLACK do ManyChat com outra conta", "10 min"),
    ("3", "sex 30/10", "19:30 (depois do teste)", "Ligar a resposta automática no Direct do ManyChat", "15 min"),
    ("4", "sáb 31/10", "10:00", "WhatsApp Business: 2 itens no catálogo + criar o Canal", "30 min"),
    ("5", "seg 02/11 em diante", "19:10 (alarme 18:15)", "Rotina dos Stories com link, nos 27 dias de post", "5 a 10 min por dia"),
    ("6", "qui 05/11", "10:00", "Reunião com o sócio: Turbinar e os 17 anúncios repetidos", "60 min"),
]


def capa():
    st = [Spacer(1, 1.2 * cm), P("PENDÊNCIAS", "capa_t"), Spacer(1, 4),
          P("O que você precisa fazer e como fazer, passo a passo<br/>em ordem de data e horário", "capa_s"), Spacer(1, 10),
          P(f"Atualizado em {HOJE:%d/%m/%Y} (quinta-feira)", "capa_s"), Spacer(1, 14),
          tabela(["Nº", "Quando", "Hora", "O que fazer", "Tempo"], [list(r) for r in RESUMO], [0.06, 0.15, 0.17, 0.46, 0.16]),
          Spacer(1, 10),
          bloco("Como usar este documento", [
              "Siga na ordem dos números: cada tarefa começa numa página nova, com data, hora, o que precisa ter em mãos, os passos, "
              "como saber que deu certo e o que fazer se algo falhar.",
              "No fim de cada tarefa há um quadro <b>\"Avise o Claude\"</b>: é o que você escreve (ou o print que manda) para eu continuar.",
              "Você não precisa mexer em nada do agendamento do Instagram: o Claude cuida dos posts e Reels. Só os itens abaixo dependem de você.",
              "Em qualquer dúvida, tire um print da tela e mande ao Claude: ele diz o próximo clique."], AZUL, AZUL_C), Spacer(1, 8),
          bloco("O que o Claude já fez e continua fazendo (não precisa de você)", [
              "Novembro de 02/11 a 26/11 já está agendado no Instagram (26 de 28 itens). Falta só 27/11, que o Claude agenda hoje, às 19:13.",
              "Dezembro (28/11 a 23/12): o Instagram só aceita agendar 29 dias à frente. O Claude agenda a cada dia que a janela abrir, "
              "a partir de amanhã, 30/10, às 19:00.",
              "Textos do blog dos cartões Philco, LG e Air Fryer já corrigidos e publicados em 29/10."], VERDE, VERDE_C)]
    return st


def t1():
    return [faixa("1", "Deixar tudo aberto para o agendamento de 27/11", "Quinta 29/10, das 18:55 às 19:30 • quase sem trabalho", VERMELHO),
            Spacer(1, 6),
            info([("Por quê", "O Instagram só deixa agendar até 29 dias à frente. O post e o Reels de 27/11 (Power Bank Anker 25.000 mAh 165 W) "
                              "só podem ser marcados a partir das 19:00 de hoje. O Claude faz isso sozinho às <b>19:13</b>."),
                  ("Onde", "No computador (mini PC). Nada no celular."),
                  ("Tempo seu", "Nenhum, só não atrapalhar. Depois, 2 minutos para conferir.")]), Spacer(1, 6),
            P("Passo a passo", "h2"),
            passos([
                ("Mantenha este app (Claude) aberto", "Não feche a janela do aplicativo Claude. Pode minimizar, mas não encerrar."),
                ("Mantenha o Google Chrome aberto com o Instagram", "Aba do Instagram logada em <b>compre.no.link</b>. Não toque em Sair e não feche a aba nem o Chrome. "
                 "Se o Chrome fechar sem querer: abra de novo, entre no Instagram e escreva ao Claude <b>reconectei</b>."),
                ("Deixe o computador ligado e acordado", "Windows → Configurações → Sistema → Energia e bateria → Tela e suspensão. "
                 "Em \"Quando ligado na tomada, colocar o PC no modo de suspensão após\", escolha <b>Nunca</b> (pode voltar ao normal depois das 19:30)."),
                ("Das 19:10 às 19:30, não use o Chrome", "O Claude clica na tela do Instagram. Se você mexer no mouse ou trocar de aba nesse intervalo, um clique pode errar. "
                 "Use outro programa ou o celular."),
                ("Espere o aviso do Claude neste chat", "Ele escreve \"27/11 agendado\" quando terminar (leva cerca de 6 a 8 minutos)."),
                ("Confira (2 minutos)", "No Chrome, abra <b>instagram.com</b> → menu <b>Mais</b> → <b>Conteúdo programado</b> → visão <b>Mensal</b> → novembro. "
                 "No dia <b>27</b> devem aparecer dois itens: <b>19:00</b> e <b>19:05</b>, ambos \"Power Bank Anker\".")], VERMELHO),
            Spacer(1, 6),
            bloco("Se algo falhar", [
                "<b>Passou das 19:40 e o Claude não avisou:</b> escreva <b>agendar 27/11</b> e ele faz na hora.",
                "<b>O Instagram recusou (\"próximos 29 dias\"):</b> o Claude tenta de novo 30 minutos depois, sem você fazer nada.",
                "<b>Chrome desconectado:</b> clique no ícone do Claude (estrela laranja) no Chrome, entre com a mesma conta do app e escreva <b>reconectei</b>."],
                  LARANJA, LARANJA_C), Spacer(1, 6),
            bloco("Avise o Claude", ["Nada, se ele avisar sozinho. Se não avisar até 19:40: <b>agendar 27/11</b>."], VERDE, VERDE_C)]


def t2():
    return [faixa("2", "Testar a automação BLACK do ManyChat", "Sexta 30/10, às 19:00 • 10 minutos • no celular", LARANJA), Spacer(1, 6),
            info([("Para quê", "Confirmar que quem comenta <b>BLACK</b> no post fixado recebe o link no Direct. A configuração já foi conferida e a sua "
                               "conta pessoal chegou a receber as mensagens uma vez. Este teste é a prova final com outra conta."),
                  ("Conta a usar", "Uma conta que <b>não seja</b> a compre.no.link (ela não dispara a própria automação). Ideal: o Instagram do sócio ou de "
                                   "um amigo. A sua conta pessoal também serve, mas se já testou, apague o comentário antigo antes de comentar de novo."),
                  ("Dispositivo", "Celular, aplicativo do Instagram."),
                  ("Palavras", "BLACK, LINK ou QUERO (maiúsculas ou minúsculas)")]), Spacer(1, 6),
            P("Passo a passo", "h2"),
            passos([
                ("Abra o Instagram com a conta de teste", "Se for a sua conta pessoal, confirme no topo do perfil que não é a compre.no.link."),
                ("Procure o perfil", "Toque na lupa → digite <b>compre.no.link</b> → toque no perfil."),
                ("Abra o post fixado", "É o primeiro da grade, com o ícone de alfinete. É o post de boas-vindas."),
                ("Comente BLACK", "Toque em comentar, digite <b>BLACK</b> e toque em Publicar."),
                ("Espere de 1 a 2 minutos", "Embaixo do seu comentário deve aparecer uma resposta pública como <b>\"Te mandei no Direct!\"</b> "
                 "(ou \"Enviado! Confere sua caixa de mensagens\" / \"Pronto! O link está no seu Direct\")."),
                ("Abra o Direct", "Ícone do avião de papel. Se a mensagem não estiver na lista, toque em <b>Solicitações</b> (mensagens de contas que você não segue)."),
                ("Leia a 1ª mensagem", "\"Oi! Que bom te ver por aqui! Separei os achados mais vendidos e bem avaliados do Mercado Livre pra você...\" com o botão <b>Quero o link</b>. "
                 "Toque no botão."),
                ("Leia a 2ª mensagem", "\"Aqui está: a lista da Black Friday com o Top 10...\" com o botão <b>Ver a lista no blog</b> e o aviso de link de afiliado. Toque no botão."),
                ("Confira a página", "Deve abrir <b>comprenolink.net/black-friday</b> com os produtos. Se abrir, o teste passou."),
                ("Tire dois prints", "Um do comentário com a resposta pública e outro da conversa no Direct. Mande os dois ao Claude.")], LARANJA),
            Spacer(1, 6),
            bloco("Como saber que deu certo", ["Resposta pública no comentário, duas mensagens no Direct e a página da Black Friday abrindo pelo botão."], VERDE, VERDE_C),
            Spacer(1, 6),
            bloco("Se não chegou nada depois de 5 minutos", [
                "Aguarde mais um pouco: às vezes o Instagram demora. Confirme que comentou no <b>post fixado</b> (a automação vale só para ele no plano grátis).",
                "Entre no Instagram com a conta <b>compre.no.link</b> → menu (três riscos) → <b>Configurações e atividade</b> → "
                "<b>Mensagens e respostas a stories</b> → <b>Ferramentas conectadas</b> → ligue <b>Permitir acesso às mensagens</b>. Depois repita o teste.",
                "Se continuar sem chegar, mande o print ao Claude. Ele confere o painel do ManyChat (Edge) com você."], LARANJA, LARANJA_C),
            Spacer(1, 6),
            bloco("Avise o Claude", ["Escreva <b>teste BLACK ok</b> (ou <b>teste BLACK falhou</b>) e anexe os 2 prints."], AZUL, AZUL_C)]


RESPOSTA_PADRAO = ("Oi! Obrigado pela mensagem. Para receber o link dos achados, comente BLACK em qualquer post do perfil @compre.no.link "
                   "que eu te mando aqui no Direct na hora. Se preferir, veja a lista da Black Friday no blog: "
                   "https://comprenolink.net/black-friday/?utm_source=instagram&utm_medium=dm&utm_campaign=black_friday&utm_content=resposta_padrao\n"
                   "(Link de afiliado: posso ganhar comissão, sem custo extra para você.)")


def t3():
    return [faixa("3", "Ligar a resposta automática no Direct (ManyChat)", "Sexta 30/10, por volta das 19:30 • 15 minutos • no computador, Edge", LARANJA),
            Spacer(1, 6),
            info([("Para quê", "Hoje, quem escreve <b>Black</b> direto no Direct não recebe nada (a \"Resposta padrão do Instagram\" está pausada). "
                               "A automação atual só responde a <b>comentários</b>. Esta resposta orienta a pessoa a comentar a palavra ou a abrir o blog."),
                  ("Por que só você", "O ManyChat só abre no Edge com o seu login, e o Claude não tem acesso para editar nesse navegador. "
                                      "O Claude pode guiar cada clique se você mandar prints."),
                  ("Faça depois", "Do teste da tarefa 2 (para não misturar os dois resultados)."),
                  ("Atenção", "Nunca clique em <b>Start Free Trial</b> / \"Experimente 14 dias\" (cobra no cartão). Fique no plano <b>Free</b> e "
                              "não ligue recursos com a etiqueta <b>PRO</b>.")]), Spacer(1, 6),
            P("Passo a passo", "h2"),
            passos([
                ("Abra o Microsoft Edge", "Ícone da onda azul e verde na barra de tarefas. (Não é o Chrome.)"),
                ("Entre no ManyChat", "Digite <b>app.manychat.com</b> na barra de endereço. Se pedir login, use a conta do blog."),
                ("Abra o menu Automação", "Barra lateral esquerda → <b>Automação</b> (Automation)."),
                ("Procure a Resposta padrão", "Na lista, ache <b>Resposta padrão do Instagram</b> (Instagram Default Reply), com o estado <b>Pausado</b>. "
                 "Se o nome estiver um pouco diferente, procure por \"Default Reply\" ou \"Resposta padrão\"."),
                ("Abra para editar", "Clique no nome. O gatilho é \"qualquer mensagem que não ativou outra automação\". Não mude o gatilho."),
                ("Edite o texto da mensagem", "Clique na caixa de texto, apague o que estiver lá e cole o texto sugerido no quadro abaixo."),
                ("Confira o link", "Se usar botão, nome do botão: <b>Ver a lista no blog</b>, com o mesmo link do quadro. Mantenha o aviso de link de afiliado."),
                ("Ative", "Clique no botão <b>Ativar</b> (Set Live) no canto superior direito. O estado deve mudar de Pausado para <b>Ativo</b> (Live)."),
                ("Teste", "Com outra conta, mande <b>oi</b> no Direct do compre.no.link. A resposta deve chegar em segundos. "
                 "Lembrete: o Instagram só permite a resposta automática dentro de 24 h depois da mensagem da pessoa.")], LARANJA),
            Spacer(1, 6),
            caixa_texto("Texto sugerido para a resposta padrão (copie e cole)", RESPOSTA_PADRAO), Spacer(1, 6),
            bloco("Como saber que deu certo", ["No painel, a Resposta padrão aparece como Ativa e a conta de teste recebe o texto ao mandar \"oi\"."], VERDE, VERDE_C),
            Spacer(1, 6),
            bloco("Cuidados", [
                "Em <b>01/12</b>, troque BLACK por <b>NATAL</b> e o link do botão para <b>comprenolink.net/presentes-de-natal</b> (com utm_campaign=natal). "
                "O Claude lembra você nessa data.",
                "Não escreva preço nem \"melhor preço\" na mensagem (regra do blog e do Mercado Livre).",
                "Se a tela estiver diferente do descrito, tire um print e mande ao Claude."], LARANJA, LARANJA_C), Spacer(1, 6),
            bloco("Avise o Claude", ["Escreva <b>resposta padrão ligada</b> (ou mande o print da tela se algo estiver diferente)."], AZUL, AZUL_C)]


CAT1 = ("NOME:\nBebê & Maternidade (com o emoji de mamadeira no início, como no arquivo de textos)\n\nDESCRIÇÃO:\n"
        "Enxoval, roupinhas, sapatinhos e naninhas. Confira todas as opções da categoria com o valor do dia no Mercado Livre pelo link. "
        "Link de afiliado: posso ganhar comissão, sem custo extra para você.\n\nLINK:\n"
        "https://comprenolink.net/bebe-e-maternidade/?utm_source=whatsapp&utm_medium=catalogo&utm_campaign=categoria&utm_content=cat_bebe-e-maternidade\n\n"
        "CÓDIGO DO ITEM: CAT-bebe-e-maternidade        FOTO: CAT-bebe-e-maternidade.jpg")
CAT2 = ("NOME:\nModa Infantil & Juvenil (com o emoji de camiseta no início, como no arquivo de textos)\n\nDESCRIÇÃO:\n"
        "Conjuntos, moletons e kits para meninas e meninos. Confira todas as opções da categoria com o valor do dia no Mercado Livre pelo link. "
        "Link de afiliado: posso ganhar comissão, sem custo extra para você.\n\nLINK:\n"
        "https://comprenolink.net/moda-infantil-e-juvenil/?utm_source=whatsapp&utm_medium=catalogo&utm_campaign=categoria&utm_content=cat_moda-infantil-e-juvenil\n\n"
        "CÓDIGO DO ITEM: CAT-moda-infantil-e-juvenil        FOTO: CAT-moda-infantil-e-juvenil.jpg")


def t4():
    return [faixa("4", "WhatsApp Business: 2 itens no catálogo e criar o Canal", "Sábado 31/10, às 10:00 • 30 minutos • no celular do número do blog", VERDE),
            Spacer(1, 6),
            info([("Para quê", "Colocar as categorias Bebê & Maternidade e Moda Infantil & Juvenil no catálogo do WhatsApp Business e criar o Canal "
                               "(onde as ofertas do dia serão publicadas)."),
                  ("Dispositivo", "Celular com o WhatsApp Business do número <b>(11) 99495-9657</b>."),
                  ("Tenha em mãos", "O celular com internet; o app <b>OneDrive</b> entrando com a mesma conta Microsoft do computador; o logotipo do blog (pasta 09_LOGO)."),
                  ("Onde estão os arquivos", "Computador: <b>D:\\mercado_livre\\4- Celular_Whatsapp\\06_CATALOGO_WHATSAPP\\CATEGORIAS</b><br/>"
                                             "Celular: OneDrive → Download → Divulgacao_Blog → 06_CATALOGO_WHATSAPP → CATEGORIAS → fotos")]), Spacer(1, 6),
            P("Parte A – Levar as 2 fotos para o celular (3 minutos)", "h2"),
            passos([
                ("Abra o app OneDrive", "Caminho: Download → Divulgacao_Blog → 06_CATALOGO_WHATSAPP → CATEGORIAS → fotos."),
                ("Salve as duas fotos na galeria", "Abra <b>CAT-bebe-e-maternidade.jpg</b> → três pontinhos ou compartilhar → <b>Salvar</b> (ou Baixar). "
                 "Repita com <b>CAT-moda-infantil-e-juvenil.jpg</b>.")], VERDE),
            Spacer(1, 6), P("Parte B – Cadastrar o 1º item: Bebê & Maternidade (8 minutos)", "h2"),
            passos([
                ("Abra o WhatsApp Business", "Ícone verde com a letra B."),
                ("Entre no Catálogo", "Android: três pontinhos (alto) → <b>Ferramentas comerciais</b> → <b>Catálogo</b>. iPhone: <b>Configurações</b> (embaixo) → Ferramentas comerciais → Catálogo."),
                ("Toque em \"Adicionar novo item\"", "Ou no botão <b>+</b>."),
                ("Adicione a foto", "Toque em <b>Adicionar imagens</b> → Galeria → escolha CAT-bebe-e-maternidade."),
                ("Nome do item", "Cole o nome do quadro abaixo (com o emoji)."),
                ("Preço", "<b>Deixe em branco</b>. O valor muda no Mercado Livre e o blog não anuncia preço."),
                ("Descrição", "Cole a descrição do quadro abaixo. Ela já traz o aviso de link de afiliado."),
                ("Mais campos", "Toque em <b>Mais campos</b> (ou Adicionar detalhes). Em <b>Link</b>, cole o link do quadro. Em <b>Código do item</b>, escreva <b>CAT-bebe-e-maternidade</b>."),
                ("Salve", "Toque em <b>Salvar</b>. O item aparece como \"Em revisão\": o WhatsApp leva até 24 horas para aprovar.")], VERDE),
            Spacer(1, 6), caixa_texto("Textos do item 1 (também no arquivo CATALOGO_CATEGORIAS_TEXTOS.txt)", CAT1),
            Spacer(1, 8), P("Parte C – Cadastrar o 2º item: Moda Infantil & Juvenil (6 minutos)", "h2"),
            P("Repita exatamente os mesmos passos da parte B, trocando a foto, o nome, a descrição, o link e o código pelos do quadro abaixo."),
            caixa_texto("Textos do item 2", CAT2), Spacer(1, 8),
            P("Parte D – Criar o Canal do WhatsApp (10 minutos)", "h2"),
            passos([
                ("Abra a aba Atualizações", "Embaixo (iPhone) ou no alto (Android): é a aba de status/atualizações."),
                ("Toque em + ou nos três pontinhos ao lado de \"Canais\"", "Escolha <b>Criar canal</b>. Se não aparecer, atualize o WhatsApp Business na loja de aplicativos e tente de novo."),
                ("Toque em Continuar", "Leia e aceite o aviso de privacidade do Canal."),
                ("Nome do canal", "<b>Compre no Link – Achados do Mercado Livre</b>"),
                ("Descrição do canal", "Cole: <i>Achados do Mercado Livre selecionados pelo blog comprenolink.net: Black Friday, presentes de Natal e os mais vendidos e "
                 "bem avaliados de cada categoria. Links de afiliado, sem custo extra para você.</i>"),
                ("Foto do canal", "Escolha o logotipo do blog (pasta 09_LOGO, salvo na galeria)."),
                ("Toque em Criar canal", "O canal aparece na lista de Atualizações."),
                ("Copie o link do canal", "Abra o canal → toque no nome do canal (no alto) → <b>Compartilhar</b> → <b>Copiar link</b>."),
                ("Mande o link ao Claude", "Cole o link na conversa com o Claude. Ele grava o link nas respostas e nos textos do blog."),
                ("Guarde o link na resposta rápida /canal", "Ferramentas comerciais → <b>Respostas rápidas</b> → abra <b>/canal</b> → troque o trecho <i>[COLE AQUI O LINK DO CANAL]</i> "
                 "pelo link copiado → Salvar.")], VERDE), Spacer(1, 6),
            bloco("Como saber que deu certo", [
                "O Catálogo mostra os 2 itens novos (em revisão ou já aprovados) e o canal aparece em Atualizações com o nome e a foto certos.",
                "Se o WhatsApp recusar algum item na revisão, não insista: apague o item e avise o Claude."], VERDE, VERDE_C), Spacer(1, 6),
            bloco("Cuidados", [
                "Nunca use aplicativos que mandam mensagens em massa e nunca adicione pessoas em grupos sem pedir: o WhatsApp bloqueia o número.",
                "Não coloque preço no catálogo e não escreva \"menor preço\" ou promessas de saúde/estética nos textos.",
                "Se tiver a planilha CATALOGO_CATEGORIAS.xlsx aberta no computador, marque <b>Cadastrado = S</b> nas duas linhas."], LARANJA, LARANJA_C),
            Spacer(1, 6),
            bloco("Avise o Claude", ["Escreva <b>catálogo e canal prontos</b> e cole o <b>link do Canal</b>."], AZUL, AZUL_C)]


DIAS = [
    ("02/11", "seg", "Smart TV Samsung 55\" MiniLED 4K + Soundbar", "BLACK"), ("04/11", "qua", "Notebook ASUS Vivobook 15 Ryzen 7 16 GB", "BLACK"),
    ("06/11", "sex", "Caixa de Som JBL Boombox 4 210 W", "BLACK"), ("09/11", "seg", "Samsung Galaxy A17 5G 256GB", "BLACK"),
    ("11/11", "qua", "Air Fryer Mondial 4 L 1500 W", "BLACK"), ("13/11", "sex", "Cama Box Baú Casal com Colchão Gazin Flora", "BLACK"),
    ("16/11", "seg", "Lavadora Vonder LAV 1300 90 bar", "BLACK"), ("18/11", "qua", "Parafusadeira de Impacto Vonder PFV120I", "BLACK"),
    ("20/11", "sex", "Fone JBL Tune 730 Bluetooth", "BLACK"), ("23/11", "seg", "Smartwatch T900 S10 Ultra Pro 49 mm", "BLACK"),
    ("24/11", "ter", "Caixa de Som Aiwa Boombox Plus 200 W", "BLACK"), ("25/11", "qua", "Smart TV Philco 32\"", "BLACK"),
    ("26/11", "qui", "Smart TV LG 32\" webOS", "BLACK"), ("27/11", "sex", "Power Bank Anker 25.000 mAh 165 W", "BLACK"),
    ("28/11", "sáb", "Motorola Moto G24 256GB", "BLACK"), ("29/11", "dom", "Mouse Gamer Logitech G403 HERO", "BLACK"),
    ("30/11", "seg", "Churrasqueira Elétrica Sem Fumaça Aero Home", "BLACK"), ("02/12", "qua", "Caixa de Som JBL Boombox 4 210 W", "NATAL"),
    ("04/12", "sex", "Perfume Árabe Sabah Al Ward 100 ml Feminino", "NATAL"), ("07/12", "seg", "Perfume Árabe Asad 100 ml Masculino", "NATAL"),
    ("09/12", "qua", "Smartwatch T900 S10 Ultra Pro 49 mm", "NATAL"), ("11/12", "sex", "Fone JBL Tune 730 Bluetooth", "NATAL"),
    ("14/12", "seg", "Caixa de Som JBL Go 5 Bluetooth à Prova d'Água", "NATAL"), ("16/12", "qua", "Kit Skincare Vitamina C Dermachem 5 Itens", "NATAL"),
    ("18/12", "sex", "Máquina de Cortar Cabelo e Barba Sem Fio Nixzen", "NATAL"), ("21/12", "seg", "Jogo de Lençol Casal Percal 600 Fios 4 Peças", "NATAL"),
    ("23/12", "qua", "Cortina de LED 3x3 m com 300 Luzes e Controle", "NATAL"),
]


def pasta_do_dia(d, s):
    dd, mm = d.split("/")
    return f"2026-{mm}-{dd}_{s}"


def t5():
    return [faixa("5", "Rotina dos Stories com link", "De segunda 02/11 a quarta 23/12, nos 27 dias de post • às 19:10 • 5 a 10 minutos • celular", AZUL), Spacer(1, 6),
            info([("Importante", "Os Stories são nos <b>27 dias de post</b> (tabela no fim desta tarefa), não em todos os dias do calendário. Hoje, 30/10 e 31/10 não há Story. "
                                 "O primeiro é <b>segunda 02/11, às 19:10</b>."),
                  ("Para quê", "O Story com adesivo de link leva os seguidores direto ao produto no blog. O post (19:00) e o Reels (19:05) saem sozinhos, agendados pelo Claude."),
                  ("Dispositivo", "Celular, Instagram da conta <b>compre.no.link</b> e app OneDrive."),
                  ("Lembrete", "O calendário <b>12_CALENDARIO_INSTAGRAM.ics</b> toca um alarme às <b>18:15</b> nos dias de post. "
                               "Se ainda não importou, abra o arquivo no celular (OneDrive → Download) e escolha \"Adicionar ao calendário\".")]), Spacer(1, 6),
            P("Linha do tempo de cada dia de post", "h2"),
            tabela(["Hora", "Quem", "O que acontece"],
                   [["18:15", "Calendário", "Alarme de lembrete. Deixe o celular e o Edge à mão."],
                    ["19:00", "Instagram (agendado)", "O post de foto sai sozinho no feed."],
                    ["19:05", "Instagram (agendado)", "O Reels sai sozinho."],
                    ["<b>19:10</b>", "<b>Você, celular</b>", "<b>Publicar o Story com adesivo de link (passo a passo abaixo).</b>"],
                    ["19:15", "Você, Edge", "Criar a automação do ManyChat para o Reels do dia (plano grátis: 1 automação por publicação)."],
                    ["19:15", "Você, WhatsApp", "Status do WhatsApp com status.png e o texto do bloco \"WhatsApp – Status\"."],
                    ["19:20", "Você, WhatsApp", "Canal: feed.png e o texto do bloco \"WhatsApp – Canal\" (depois da tarefa 4)."],
                    ["até 22:00", "Você", "Responder comentários e mensagens do dia. Onde não houver automação, mande <b>bf</b> (ou <b>natal</b>) no Direct."]],
                   [0.12, 0.22, 0.66]), Spacer(1, 8),
            P("Passo a passo do Story (19:10) – 2 minutos", "h2"),
            passos([
                ("Abra o OneDrive no celular", "Download → Divulgacao_Blog → 07_PACOTE_DO_DIA → pasta do dia (ex.: <b>2026-11-02_seg</b>)."),
                ("Salve a arte", "Abra <b>story.png</b> → compartilhar/três pontinhos → <b>Salvar</b>. Ela vai para a galeria."),
                ("Copie o link do adesivo", "Abra <b>1_TEXTOS_DO_DIA.txt</b> → procure o bloco <b>\"Instagram – Story com adesivo de link\"</b> → pressione o dedo no texto sob "
                 "\"Link para o adesivo\" → Selecionar → <b>Copiar</b>."),
                ("Crie o Story", "No Instagram da compre.no.link: botão <b>+</b> → <b>Story</b> → escolha o <b>story.png</b> da galeria."),
                ("Coloque o adesivo de link", "Toque no ícone do adesivo (carinha quadrada, no alto) → <b>Link</b> → cole o link → no texto do adesivo escreva <b>VER NO BLOG</b> → Concluído."),
                ("Posicione o adesivo", "Arraste o adesivo para cima do retângulo amarelo da arte (\"adesivo VER NO BLOG aqui\")."),
                ("Publique", "Toque em <b>Seu story</b>. Confira no seu perfil que o adesivo abre o blog.")], AZUL), Spacer(1, 6),
            bloco("Como saber que deu certo", ["O Story aparece no seu perfil com o círculo colorido e o adesivo VER NO BLOG abre o blog no produto do dia."], VERDE, VERDE_C),
            Spacer(1, 6),
            bloco("Se algo falhar", [
                "<b>Esqueceu às 19:10:</b> publique assim que lembrar. O link continua valendo.",
                "<b>Não aparece o adesivo de Link:</b> atualize o Instagram na loja de aplicativos. Se ainda faltar, escreva \"Link na bio\" no Story e avise o Claude.",
                "<b>Dia sem pasta:</b> escreva ao Claude. Ele confere se o pacote do dia foi gerado."], LARANJA, LARANJA_C), Spacer(1, 6),
            bloco("Avise o Claude", ["Só em caso de problema. Se tudo correr bem, não precisa avisar."], AZUL, AZUL_C),
            Spacer(1, 8), P("Automação do ManyChat de cada dia (19:15, no Edge)", "h2"),
            passos([
                ("Abra app.manychat.com no Edge", "Menu <b>Automação</b> → <b>+ Nova automação</b> (modelo \"Autoenviar links a partir de comentários\")."),
                ("Publicação", "Escolha \"uma publicação ou Reels específico\" → selecione o <b>Reels do dia</b> → Próximo."),
                ("Palavras", "<b>BLACK, LINK, QUERO</b> (em dezembro: <b>NATAL, LINK, QUERO</b>) e ligue \"interagir com os comentários\"."),
                ("Respostas públicas", "\"Te mandei no Direct!\" • \"Enviado! Confere sua caixa de mensagens\" • \"Pronto! O link está no seu Direct\"."),
                ("DM de boas-vindas", "\"Oi! Que bom te ver por aqui! Separei os achados mais vendidos e bem avaliados do Mercado Livre pra você. Toque no botão abaixo que eu te mando o link agora\" "
                 "• botão <b>Quero o link</b>."),
                ("DM com o link", "Texto com o aviso de link de afiliado • botão <b>Ver a lista no blog</b> com o link "
                 "<b>comprenolink.net/black-friday/?utm_source=instagram&amp;utm_medium=dm&amp;utm_campaign=black_friday&amp;utm_content=manychat</b>."),
                ("Ative", "Deixe desligadas as opções com etiqueta PRO. Clique em <b>Ativar</b>. Nunca clique em \"Start Free Trial\".")], AZUL),
            PageBreak(), P("Os 27 dias de post (Story às 19:10)", "h1"),
            P("A pasta do dia fica em OneDrive → Download → Divulgacao_Blog → 07_PACOTE_DO_DIA. Palavra = o que o seguidor comenta."),
            tabela(["Data", "Dia", "Produto do dia", "Palavra", "Pasta do dia"],
                   [[d, s, prod, pal, pasta_do_dia(d, s)] for d, s, prod, pal in DIAS], [0.09, 0.07, 0.43, 0.09, 0.32], tam="pq")]


RETIRAR = [
    ("115", "Magnésio Dimalato 250 mg 120 Cápsulas", "3 dimalatos parecidos", "116"), ("117", "Dimagnésio Malato 1300 mg 60 Comprimidos", "3 dimalatos parecidos", "116"),
    ("119", "5 Magnésios Muwiz 120 Cápsulas", "2 produtos \"5 magnésios\" iguais", "118"), ("132", "Kit 3 Coenzima Q10 Ubiquinol 100 mg", "5 opções de coenzima Q10", "135"),
    ("136", "Coenzima Q10 200 mg 60 Doses", "5 opções de coenzima Q10", "134"), ("121", "Ômega 3 EPA e DHA Vitafor 60 Cápsulas", "6 opções de ômega 3", "120, 122 e 123"),
    ("137", "Licopeno 10 mg Recover Farma 30 Cápsulas", "3 licopenos", "138 e 139"), ("141", "Kit 2 Óleo de Semente de Abóbora Zuchetti", "repete o 140", "140"),
    ("145", "Trocador de Fralda Dobrável Nuvem Azul", "4 trocadores parecidos", "144 e 147"), ("146", "Trocador de Fralda Portátil Coração Rosa", "4 trocadores parecidos", "144 e 147"),
    ("163", "Conjunto Bebê Body Manga Longa e Calça Mijão", "5 kits body + mijão", "161 e 173"), ("164", "Kit 6 Peças Bebê Canelado 3 Bodies e 3 Mijões", "5 kits body + mijão", "161 e 173"),
    ("179", "Tênis Bebê Mania Menina 71307", "3 itens da mesma marca", "175"), ("181", "Sapatilha Bebê Mania Vermelha 31607", "3 itens da mesma marca", "175"),
    ("183", "Tênis Bebê Menina Calce Fácil Rosa", "4 tênis de menina parecidos", "177 e 182"), ("186", "Tênis Bebê Menino Casual 2026", "2 tênis de menino parecidos", "185"),
    ("180", "Botina Bebê Caipira Festa Junina", "fora de época (volta em maio)", "–"),
]


def t6():
    return [faixa("6", "Reunião com o sócio: Turbinar e os 17 anúncios repetidos", "Quinta 05/11, às 10:00 • 60 minutos • presencial ou chamada", ROXO), Spacer(1, 6),
            info([("Decisões", "1) Se o blog faz anúncio pago no Instagram (Turbinar), até qual valor e quem paga.<br/>"
                               "2) Se o Claude retira ou não os 17 anúncios repetidos do blog."),
                  ("Tenha em mãos", "<b>Plano_Turbinar_Instagram_2026.pdf</b> (a página final é a de aprovação) e <b>Quadro_Resumo_Turbinar_2026.pdf</b> em "
                                    "D:\\mercado_livre\\plano_turbinar_anuncio_instagram. <b>Analise_Critica_Anuncios_2026-10-27.pdf</b> em D:\\mercado_livre "
                                    "(a seção 6.1 é a lista dos 17)."),
                  ("Prepare antes", "Imprima ou deixe abertos os 3 PDFs e leia os termos do programa ML Afiliados (parte A).")]), Spacer(1, 6),
            P("Parte A – Antes da reunião (qua 04/11, 20 minutos)", "h2"),
            passos([
                ("Leia os termos do ML Afiliados sobre anúncio pago", "Entre no painel do ML Afiliados (conta do blog) → procure <b>Termos e condições</b> / regras do programa. "
                 "Procure os trechos sobre <b>anúncios pagos, mídia paga ou campanhas patrocinadas</b> com o link de afiliado. Anote: é permitido, proibido ou só com condições?"),
                ("Abra o Plano Turbinar", "Leia as páginas 1 a 4 e a página final de aprovação. O resumo está no quadro abaixo."),
                ("Abra a Análise Crítica na seção 6.1", "Veja a lista dos 17 itens (tabela abaixo) e escolha se concorda."),
                ("Combine quem paga", "O pagamento é do sócio pagador, por cartão ou Pix na conta de anúncios da Meta (criada só se o plano for aprovado).")], ROXO),
            Spacer(1, 6), P("Resumo do plano Turbinar", "h2"),
            tabela(["Opção", "Dias com gasto", "Total", "Decide em"],
                   [["1. Gasto mínimo (só teste)", "16, 17 e 18/11 (R$ 10 por dia)", "R$ 30,00", "19/11"],
                    ["2. Teste + Black Friday", "16 a 18/11 e 21 a 27/11 (R$ 15 por dia na Black Friday)", "R$ 135,00", "30/11"],
                    ["3. Plano completo", "as anteriores + 05 a 14/12 (R$ 10 por dia)", "R$ 235,00 (máximo)", "21/12"]],
                   [0.27, 0.45, 0.16, 0.12]), Spacer(1, 4),
            bloco("Números de hoje para a conversa", [
                "160 produtos no blog • 2 seguidores no Instagram • 19 vendas e R$ 172,00 de comissão nos últimos 180 dias • 116 cliques • comissão média de R$ 9,05 por venda.",
                "Risco principal: gastar e não vender. O plano para a cada fase se o resultado não ficar no verde.",
                "O anúncio só leva visitas ao blog. A venda e a entrega são do Mercado Livre."], AZUL, AZUL_C), Spacer(1, 8),
            P("Parte B – Na reunião (10:00)", "h2"),
            passos([
                ("Apresente a situação", "Use o quadro \"Números de hoje\". O Instagram é novo (2 seguidores), então o alcance gratuito no início é pequeno."),
                ("Decida o valor máximo", "Marque no plano (última página) uma opção: R$ 30, R$ 135 ou R$ 235. Pode aprovar só a 1ª fase e decidir as outras depois."),
                ("Decida quem paga", "Escreva o nome do sócio pagador. Ele cria a conta de anúncios Meta até <b>15/11</b> (Instagram → Turbinar / Central de anúncios → forma de pagamento)."),
                ("Condição dos termos", "Só inicie o teste de 16/11 se os termos do ML Afiliados permitirem anúncio pago (resultado da parte A)."),
                ("Decida os 17 anúncios repetidos", "Percorra a tabela abaixo. Aprovar tudo, aprovar alguns ou manter todos. Em caso de dúvida, marque \"manter\"."),
                ("Registre a aprovação", "Assine ou escreva a data na página de aprovação do Plano Turbinar e fotografe a página.")], ROXO), Spacer(1, 8),
            P("Os 17 anúncios sugeridos para retirar (seção 6.1 da Análise Crítica)", "h2"),
            P("Critério: dentro de cada grupo de produtos quase iguais, fica o mais completo ou o de marca mais conhecida. O Claude só retira com a sua aprovação e "
              "faz um <b>backup antes</b>. São 8 de suplementos e 9 de bebê."),
            tabela(["Nº", "Produto a retirar", "Motivo", "Fica no lugar", "Retirar? (S/N)"],
                   [[n, p_, m, f, "[   ]"] for n, p_, m, f in RETIRAR], [0.07, 0.40, 0.25, 0.13, 0.15], tam="pq"), Spacer(1, 8),
            bloco("Depois da reunião", [
                "Envie ao Claude as decisões: <b>valor aprovado</b>, <b>quem paga</b>, <b>retirar os 17 (todos / só alguns / nenhum)</b> e o <b>resultado da leitura dos termos do ML Afiliados</b>.",
                "Se for aprovado: o Claude prepara o anúncio do teste (16 a 18/11) e as datas de avaliação (19/11, 30/11 e 21/12).",
                "Se o Turbinar não for aprovado: o foco fica nos posts, Reels, Stories e WhatsApp, que já estão agendados."], VERDE, VERDE_C), Spacer(1, 6),
            bloco("Avise o Claude", ["Escreva: <b>reunião feita</b> + as 4 decisões acima (valor, quem paga, os 17 anúncios e os termos do ML)."], AZUL, AZUL_C)]


def fim():
    return [PageBreak(), P("Lista de conferência (marque conforme concluir)", "h1"),
            tabela(["OK", "Data e hora", "Tarefa", "Feito em"],
                   [["[   ]", "qui 29/10, 19:13", "Deixar tudo aberto e conferir 27/11 no calendário do Instagram", "___/___"],
                    ["[   ]", "sex 30/10, 19:00", "Testar a automação BLACK do ManyChat com outra conta", "___/___"],
                    ["[   ]", "sex 30/10, 19:30", "Ligar a resposta automática no Direct (ManyChat)", "___/___"],
                    ["[   ]", "sáb 31/10, 10:00", "WhatsApp Business: 2 itens no catálogo e criar o Canal (mandar o link ao Claude)", "___/___"],
                    ["[   ]", "seg 02/11, 19:10", "1º Story com link (e todos os 27 dias de post)", "___/___"],
                    ["[   ]", "qui 05/11, 10:00", "Reunião com o sócio e envio das decisões ao Claude", "___/___"]],
                   [0.07, 0.2, 0.60, 0.13]), Spacer(1, 10),
            P("Outras datas já previstas (para você não esquecer)", "h2"),
            tabela(["Data", "O que", "Quem"],
                   [["sex 06/11", "Criar os Destaques do Instagram (Black Friday, Categorias, Como comprar). Peça o passo a passo ao Claude.", "Você, celular"],
                    ["seg 09/11", "Decisões: QCY Shopee, nota antiga no painel das máquinas e divulgação de longo prazo.", "Você"],
                    ["até dom 15/11", "Conta de anúncios Meta com forma de pagamento (só se o Turbinar for aprovado).", "Sócio pagador"],
                    ["seg 16/11", "Início do Turbinar de teste (só se aprovado): R$ 30 em 3 dias.", "Sócio pagador"],
                    ["ter 01/12", "Bio de Natal, link 1 da bio para presentes-de-natal, automações com NATAL.", "Você + Claude"]],
                   [0.17, 0.63, 0.20]), Spacer(1, 10),
            bloco("Regras de ouro (sempre)", [
                "Sempre: aviso de link de afiliado nos textos • \"Confira o valor do dia no Mercado Livre\" • responder comentários e Direct no mesmo dia.",
                "Nunca: preço, \"menor preço\" ou \"melhor preço\" • promessas de saúde ou estética • comprar seguidores ou seguir/deixar de seguir em massa • "
                "robôs de mensagem em massa no WhatsApp • clicar em \"Start Free Trial\" do ManyChat.",
                "Nunca envie senha, código de verificação ou número de cartão ao Claude ou por mensagem. Se uma tela pedir algo assim, faça você mesmo."],
                  VERMELHO, VERMELHO_C), Spacer(1, 8),
            P("Onde estão os arquivos", "h2"),
            tabela(["O quê", "No computador", "No celular (OneDrive)"],
                   [["Pacote de cada dia (post, story, Reels, textos)", "D:\\mercado_livre\\4- Celular_Whatsapp\\07_PACOTE_DO_DIA", "Download → Divulgacao_Blog → 07_PACOTE_DO_DIA"],
                    ["Catálogo do WhatsApp", "D:\\mercado_livre\\4- Celular_Whatsapp\\06_CATALOGO_WHATSAPP", "Download → Divulgacao_Blog → 06_CATALOGO_WHATSAPP"],
                    ["Passo a passo do WhatsApp", "...\\08_PASSO_A_PASSO_WHATSAPP_NO_CELULAR.pdf", "Download → Divulgacao_Blog"],
                    ["Plano Turbinar", "D:\\mercado_livre\\plano_turbinar_anuncio_instagram", "–"],
                    ["Análise Crítica dos anúncios", "D:\\mercado_livre\\Analise_Critica_Anuncios_2026-10-27.pdf", "–"],
                    ["Guia Passo a Passo do Instagram", "D:\\mercado_livre\\Guia_Passo_a_Passo_Instagram_2026.pdf", "–"],
                    ["Este documento", SAIDA, "–"]],
                   [0.30, 0.42, 0.28], tam="pq")]


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Pendências – passo a passo (comprenolink.net)", author="comprenolink.net")
    st = capa()
    for f in (t1, t2, t3, t4, t5, t6):
        st += [PageBreak()] + f()
    st += fim()
    doc.build(st, onFirstPage=cabecalho_rodape, onLaterPages=cabecalho_rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
