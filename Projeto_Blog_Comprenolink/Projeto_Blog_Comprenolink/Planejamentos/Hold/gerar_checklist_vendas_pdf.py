# -*- coding: utf-8 -*-
"""Gera o PDF "Checklist para turbinar as vendas do blog comprenolink.net".

Uso:  python gerar_checklist_vendas_pdf.py
Saída: Checklist_Turbinar_Vendas_Blog_comprenolink.pdf (nesta mesma pasta)
"""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, Table,
                                TableStyle, PageBreak, KeepTogether)
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

PASTA = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(PASTA, "Checklist_Turbinar_Vendas_Blog_comprenolink.pdf")

FONTES = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Arial", os.path.join(FONTES, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-B", os.path.join(FONTES, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-I", os.path.join(FONTES, "ariali.ttf")))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-B", italic="Arial-I", boldItalic="Arial-B")
pdfmetrics.registerFont(TTFont("Simbolos", os.path.join(FONTES, "seguisym.ttf")))  # para o ✔ dos passos feitos

ATUALIZADO_EM = "21/10/2026"
# Passos do checklist já executados no site em 21/10/2026 (número do passo → o que foi feito)
FEITOS = {
    1: "A página inicial agora é a vitrine \"Início\": título, botão grande para o guia, 6 categorias com links UTM "
       "e aviso de afiliado. O post \"Hello world!\" e o comentário de exemplo foram para a lixeira. A descrição do site "
       "foi preenchida e os blocos \"Recent Posts / Recent Comments\" foram desativados.",
    2: "A página ganhou o título \"Os 21 Melhores Produtos do Mercado Livre em 2026\" (Google e aba do navegador), "
       "e o H1 vazio foi removido. O site já tinha o plugin <b>All in One SEO</b>, que gera a descrição automaticamente: "
       "não é preciso instalar o Rank Math. Falta escrever a descrição à mão no All in One SEO (opcional).",
    3: "O guia mudou de /5-2/ para <b>comprenolink.net/melhores-produtos-mercado-livre-2026/</b>. Os endereços /5-2/ e "
       "/5.2/ redirecionam (301) para o novo <b>mantendo a etiqueta UTM</b>, então os links já divulgados continuam "
       "funcionando e sendo medidos. Menu, página inicial, rodapé, rastreador, relatório, links UTM e os 4 programas .exe "
       "foram atualizados; o relatório continua contando o histórico do endereço antigo.",
    4: "Os 4 cartões extras que não carregavam foram removidos. A mensagem \"Não foi possível buscar os produtos\" "
       "não aparece mais em nenhuma página.",
    5: "Títulos corrigidos: SSD Externo Kingston XS2000, Carregador Duplo para Controle PS5, Kit de Teclas Redragon, "
       "Galaxy A17 5G, iPhone 18 Pro Max e Power Bank Anker. Textos soltos removidos e \"Benefícios\" no lugar certo. "
       "<b>Bônus:</b> os 21 títulos linkavam para a busca do Mercado Livre <b>sem a etiqueta de afiliado</b>; agora "
       "apontam para os seus links meli.la.",
    6: "Publicadas as páginas Sobre, Contato (e-mail compre.no.link26@gmail.com) e Política de Privacidade (LGPD), "
       "com o aviso de afiliado no topo do guia e o menu Início | Melhores Produtos 2026 | Escolha rápida | Sobre | "
       "Contato | Privacidade. Falta o botão de WhatsApp, quando você tiver o número.",
    11: "Tabela \"Escolha rápida\" com 8 categorias e botão \"Ver preço\" logo após a introdução. Cada produto tem "
        "âncora (#item-1 a #item-21) e o menu tem o atalho \"Escolha rápida\".",
    12: "Botão \"Ver preço no Mercado Livre →\" em todos os cartões, aviso \"Preços e estoque podem mudar\" e seção de "
        "Perguntas frequentes no fim. Falta a linha \"Não compre se...\" em cada produto.",
}

AZUL = colors.HexColor("#1F3A68")
AMARELO = colors.HexColor("#FFE600")      # amarelo Mercado Livre
CINZA = colors.HexColor("#F2F4F7")
VERMELHO = colors.HexColor("#C62828")
VERDE = colors.HexColor("#2E7D32")
LARANJA = colors.HexColor("#E65100")

st = {
    "capa_t": ParagraphStyle("capa_t", fontName="Arial-B", fontSize=26, leading=32, textColor=AZUL, alignment=TA_CENTER),
    "capa_s": ParagraphStyle("capa_s", fontName="Arial", fontSize=13, leading=18, alignment=TA_CENTER, textColor=colors.HexColor("#333333")),
    "h1": ParagraphStyle("h1", fontName="Arial-B", fontSize=17, leading=22, textColor=AZUL, spaceBefore=6, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="Arial-B", fontSize=13, leading=17, textColor=AZUL, spaceBefore=10, spaceAfter=5),
    "h3": ParagraphStyle("h3", fontName="Arial-B", fontSize=11, leading=14, spaceBefore=6, spaceAfter=3),
    "p": ParagraphStyle("p", fontName="Arial", fontSize=10, leading=14, spaceAfter=5),
    "pq": ParagraphStyle("pq", fontName="Arial", fontSize=9, leading=12),
    "pqb": ParagraphStyle("pqb", fontName="Arial-B", fontSize=9, leading=12, textColor=colors.white),
    "li": ParagraphStyle("li", fontName="Arial", fontSize=10, leading=14, leftIndent=14, bulletIndent=4, spaceAfter=2),
    "box": ParagraphStyle("box", fontName="Arial", fontSize=10, leading=14),
}


def P(t, s="p"):
    return Paragraph(t, st[s])


def lista(itens):
    return [Paragraph(i, st["li"], bulletText="•") for i in itens]


def caixa(texto, cor=AMARELO, borda=AZUL):
    t = Table([[Paragraph(texto, st["box"])]], colWidths=[17 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), cor), ("BOX", (0, 0), (-1, -1), 1, borda),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def tabela(cab, linhas, larg, zebra=True):
    dados = [[Paragraph(c, st["pqb"]) for c in cab]] + [[Paragraph(str(c), st["pq"]) for c in l] for l in linhas]
    t = Table(dados, colWidths=[w * cm for w in larg], repeatRows=1)
    estilo = [("BACKGROUND", (0, 0), (-1, 0), AZUL), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B0B7C3")),
              ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if zebra:
        for i in range(2, len(dados), 2):
            estilo.append(("BACKGROUND", (0, i), (-1, i), CINZA))
    t.setStyle(TableStyle(estilo))
    return t


def passo(num, titulo, quando, tempo, custo, porque, como, pronto=None):
    """Um item do checklist: caixinha para marcar (já marcada se está em FEITOS) + detalhes."""
    feito = FEITOS.get(num)
    marca = Paragraph("<font name='Simbolos' color='white'>✔</font>", st["box"]) if feito else ""
    rotulo = f"<b>{num}. {titulo}</b>" + ("  <font color='#2E7D32'><b>FEITO</b></font>" if feito else "")
    cab = Table([[marca, Paragraph(rotulo, st["box"])]], colWidths=[0.7 * cm, 16.3 * cm])
    cab.setStyle(TableStyle([("BOX", (0, 0), (0, 0), 1.2, VERDE if feito else AZUL),
                             ("BACKGROUND", (0, 0), (0, 0), VERDE if feito else colors.white),
                             ("BACKGROUND", (1, 0), (1, 0), colors.HexColor("#E8F5E9") if feito else CINZA),
                             ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (1, 0), (1, 0), 6),
                             ("LEFTPADDING", (0, 0), (0, 0), 3)]))
    meta = Table([[Paragraph(f"<b>Quando:</b> {quando}", st["pq"]), Paragraph(f"<b>Tempo:</b> {tempo}", st["pq"]),
                   Paragraph(f"<b>Custo estimado:</b> {custo}", st["pq"])]], colWidths=[6 * cm, 4.5 * cm, 6.5 * cm])
    meta.setStyle(TableStyle([("LEFTPADDING", (0, 0), (-1, -1), 2), ("TOPPADDING", (0, 0), (-1, -1), 2)]))
    corpo = [cab, meta]
    if feito:
        corpo.append(caixa(f"<b>Feito em {ATUALIZADO_EM}:</b> {feito}", colors.HexColor("#E8F5E9"), VERDE))
        corpo.append(Spacer(1, 4))
    corpo += [P(f"<b>Por que:</b> {porque}"), P("<b>Como fazer</b> (para refazer ou conferir):" if feito else "<b>Como fazer:</b>")]
    corpo += [Paragraph(c, st["li"], bulletText=f"{i}.") for i, c in enumerate(como, 1)]
    if pronto:
        corpo.append(P(f"<font color='#2E7D32'><b>Está pronto quando:</b></font> {pronto}"))
    corpo.append(Spacer(1, 6))
    return [KeepTogether(corpo)]


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFillColor(AMARELO)
    canvas.rect(0, A4[1] - 0.5 * cm, A4[0], 0.5 * cm, fill=1, stroke=0)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(colors.HexColor("#555555"))
    canvas.drawString(2 * cm, 1.1 * cm, f"Checklist para turbinar as vendas  |  comprenolink.net  |  versão 2 – atualizado em {ATUALIZADO_EM}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.1 * cm, f"Página {doc.page}")
    canvas.restoreState()


H = []  # história (conteúdo do PDF)

# ------------------------------------------------------------------ CAPA
H += [Spacer(1, 4 * cm), P("Checklist Passo a Passo para<br/>Turbinar as Vendas do Blog", "capa_t"), Spacer(1, 0.6 * cm),
      P("comprenolink.net/melhores-produtos-mercado-livre-2026/  •  Afiliado Mercado Livre", "capa_s"), Spacer(1, 1.2 * cm),
      P("Análise de tudo o que foi feito até 21/10/2026 • Diagnóstico da página • Checklist cronológico com custo "
        "estimado de cada etapa • Calendário até o Natal (Black Friday em 27/11/2026)", "capa_s"),
      Spacer(1, 0.8 * cm),
      P(f"<b>Versão 2 — atualizada em {ATUALIZADO_EM}</b> com as correções já feitas no site (Parte 0). "
        "Os passos concluídos aparecem marcados com ✔ e a etiqueta FEITO.".replace("✔", "<font name='Simbolos'>✔</font>"),
        "capa_s"),
      Spacer(1, 2 * cm),
      caixa("<b>Como usar este documento:</b> imprima ou deixe aberto no celular. Faça os passos <b>na ordem</b> — "
            "cada fase prepara a seguinte. Marque a caixinha □ ao lado de cada passo quando terminar. "
            "Os valores em R$ são <b>estimativas de outubro/2026</b> e podem mudar; confira o preço na hora de contratar. "
            "Tudo que está marcado como <b>R$ 0</b> pode ser feito sem gastar nada."),
      PageBreak()]

# ------------------------------------------------------------------ RESUMO
H += [P("Resumo em 1 página (leia primeiro)", "h1"),
      P("O blog <b>não está com problema de anúncio ruim — está com problema de visitante que não chega ao anúncio</b>. "
        "Os seus próprios dados mostram isso:"),
      tabela(["O que os dados mostram (29/09 a 20/10/2026)", "Número"], [
          ["Visitas registradas no site inteiro", "110 (107 visitantes)"],
          ["Visitas que caíram na página inicial (comprenolink.net/)", "<b>105 (95%)</b>"],
          ["Visitas reais na página dos 21 produtos (/5-2/)", "<b>0</b> (a única registrada foi o seu teste de instalação)"],
          ["Visitas vindas dos links UTM do TikTok / Instagram / WhatsApp", "0 (fora o teste)"],
          ["Cliques em link de afiliado (meli.la)", "1 (o teste)"],
          ["Vendas aprovadas importadas no relatório", "nenhum arquivo de vendas importado ainda"],
      ], [12, 5]),
      Spacer(1, 6),
      P("Até 21/10/2026, a página inicial, onde 95% das pessoas chegavam, mostrava o post padrão do WordPress "
        "<b>\"Hello world!\"</b>, sem nenhum link para os produtos: as pessoas entravam, viam um site vazio e iam embora."),
      caixa(f"<b>Situação em {ATUALIZADO_EM}:</b> a Fase 0 inteira foi feita no site (passos 1 a 6) e também os passos "
            "11 e 12. A página inicial virou vitrine, a página dos produtos não mostra mais erros, os títulos foram "
            "corrigidos e todos os links de afiliado funcionam. O que falta agora é <b>trazer visitantes</b>. "
            "Veja a Parte 0.", colors.HexColor("#E8F5E9"), VERDE),
      P("As 5 ações que mais trazem resultado, em ordem:", "h2")]
H += lista([
    "<font color='#2E7D32'><b>FEITO em 21/10:</b></font> página inicial transformada em vitrine e \"Hello world!\" apagado (Fase 0, passo 1).",
    "<font color='#2E7D32'><b>FEITO em 21/10:</b></font> título de verdade na página dos produtos e erros do plugin corrigidos (Fase 0).",
    "<b>Esta semana:</b> publicar de fato os 3 vídeos do TikTok e os posts do Instagram que já estão prontos, usando os links UTM — eles existem mas não geraram nenhuma visita (Fase 3). R$ 0.",
    "<b>Até 10/11:</b> criar a página \"Black Friday 2026\" — é a época do ano em que mais se compra (Fase 4). R$ 0.",
    "<b>Toda semana:</b> rodar o relatório, importar as vendas do painel de Afiliados e repetir o que funcionou (Fase 7). R$ 0.",
])
H += [Spacer(1, 6),
      caixa("<b>Custo total possível:</b> dá para fazer <b>todo o essencial com R$ 0</b> (só tempo: ~1 a 2 h por dia). "
            "Um plano \"econômico\" com ferramentas pagas fica em <b>~R$ 70 a 150/mês</b>, e um \"acelerado\" com anúncios "
            "pagos em <b>~R$ 450 a 900/mês</b>. Detalhes na Parte 6.", colors.HexColor("#E8F5E9"), VERDE),
      PageBreak()]

# ------------------------------------------------------------------ PARTE 0 — CORREÇÕES JÁ FEITAS
H += [P(f"Parte 0 — Correções já feitas no site em {ATUALIZADO_EM}", "h1"),
      P("Tudo abaixo foi feito pelo painel do WordPress, com você logado, e conferido no computador e no celular. "
        "A última coluna diz como desfazer, caso precise."),
      tabela(["O que foi feito", "Onde fica no WordPress", "Como desfazer"], [
          ["<b>Página inicial nova</b> (\"Achados do Mercado Livre com o melhor custo-benefício\"): botão para o guia, "
           "6 categorias com links UTM (utm_source=site&amp;utm_medium=home) e aviso de afiliado.",
           "Páginas → Início; Configurações → Leitura (página estática)", "Configurações → Leitura → \"Seus posts mais recentes\""],
          ["<b>\"Hello world!\" e comentário de exemplo</b> enviados para a lixeira (o endereço agora dá 404).",
           "Posts → Lixeira", "Restaurar na lixeira"],
          ["<b>Descrição do site</b>: \"Os melhores achados do Mercado Livre, comparados e com o preço de hoje\".",
           "Configurações → Geral", "Apagar o texto"],
          ["<b>Página dos 21 produtos</b>: título novo, 4 cartões com erro removidos, títulos que não batiam corrigidos, "
           "textos soltos removidos, Benefícios/Ideal para como subtítulos.",
           "Páginas → Os 21 Melhores Produtos...", "Editor da página → Revisões"],
          ["<b>Links de afiliado</b>: os 21 títulos levavam para lista.mercadolivre.com.br <b>sem etiqueta de afiliado</b> "
           "(venda sem comissão). Agora levam para os seus links meli.la.",
           "Mesma página", "Revisões"],
          ["<b>Tabela \"Escolha rápida\"</b> (8 categorias com botão \"Ver preço\"), aviso de afiliado com data, "
           "Perguntas frequentes que abrem ao tocar.", "Mesma página", "Revisões"],
          ["<b>Páginas Sobre, Contato e Política de Privacidade</b> publicadas. Contato usa o e-mail "
           "compre.no.link26@gmail.com.", "Páginas", "Mover para a lixeira"],
          ["<b>Endereço novo do guia</b>: comprenolink.net/melhores-produtos-mercado-livre-2026/ (antes /5-2/). "
           "Links antigos redirecionam mantendo o UTM; configs, relatório e os .exe atualizados (os antigos ficaram em "
           "_exe_antigos_2026-09).", "Página → Link/URL; Snippets id 6; config_rastreio.json", "Voltar o slug para 5-2"],
          ["<b>Menu do topo</b>: Início, Melhores Produtos 2026, Escolha rápida, Sobre, Contato, Privacidade "
           "(tirou o aviso \"ADICIONAR AO MENU\").", "Aparência → Menus → Menu principal", "Excluir o menu"],
          ["<b>Visual moderno em todas as páginas</b>: fonte Inter, cabeçalho fixo, título centralizado com barra amarela, "
           "conteúdo em cartão branco, cartões de produto com botão azul \"Ver preço no Mercado Livre →\", "
           "busca e página \"não encontrada\" no mesmo padrão.", "Aparência → Personalizar → CSS adicional",
           "Apagar o CSS (classes cnl-*)"],
          ["<b>Widgets padrão</b> (Pesquisar, Recent Posts, Recent Comments) desativados.",
           "Aparência → Widgets → Widgets inativos", "Arrastar de volta"],
          ["<b>Regra \"Cache curto e redirecionamentos\"</b>: cache das páginas de 7 dias para 10 minutos; "
           "/5-2/ e /5.2/ → endereço novo do guia (mantendo o UTM); páginas de autor e categoria vazia → início; rodapé próprio no lugar de "
           "\"Orgulhosamente mantido com WordPress\".", "Snippets (plugin Code Snippets), id 6", "Desativar o snippet"],
      ], [7.6, 5, 4.4]),
      Spacer(1, 8),
      P("Teste automático do site", "h2"),
      P("Dê dois cliques em <b>D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Verificar_Erros_Blog\\testar_site_de_novo.bat</b>. Em cerca de 1 minuto ele testa as "
        "5 páginas, os endereços antigos e os 26 links, procura textos indevidos (\"Hello world\", erros do plugin, "
        "rodapé antigo) e abre um relatório HTML, que fica salvo em D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Hold\\Dados_Tiktok. Rode depois de qualquer "
        "mudança no site."),
      tabela(["Resultado do teste de 21/10/2026", "Situação"], [
          ["5 páginas públicas", "Todas abrem (código 200)"],
          ["26 links (21 de afiliado + internos)", "Todos funcionam; os meli.la levam ao Mercado Livre"],
          ["Textos indevidos (Hello world, erro do plugin, Recent Posts, ADICIONAR AO MENU, rodapé antigo)", "Nenhum"],
          ["Cache das páginas no navegador", "10 minutos (antes: 7 dias)"],
          ["Endereços antigos /5.2/, autor e categoria", "Redirecionam para a página certa"],
      ], [10, 7]),
      Spacer(1, 8),
      P("O que ainda falta (em ordem)", "h2")]
H += lista([
    "<b>Botão de WhatsApp Business</b> na página Contato, quando você tiver o número dedicado.",
    "<b>Fase 1</b>: Google Search Console, Bing, Analytics e velocidade (passos 7 a 10).",
    "<b>Fase 3</b>: publicar os vídeos e posts que já estão prontos. É isso que traz visitantes (passos 14 a 18).",
    "<b>Fase 4</b>: página da Black Friday até 10/11 (passo 19).",
    "<b>Linha \"Não compre se...\"</b> em cada produto e descrição escrita à mão no All in One SEO (passos 2 e 12).",
    "<b>Logotipo</b>: hoje o topo mostra só o nome do site com o ícone 🛒 do CSS.".replace("🛒 ", ""),
])
H += [Spacer(1, 4),
      caixa("<b>Se a página antiga ainda aparecer em algum celular:</b> é uma cópia guardada no navegador de quem visitou "
            "antes de 21/10 (o cache era de 7 dias). Ela some sozinha até 28/10. Para ver na hora, use uma aba anônima "
            "ou aperte Ctrl+F5 no computador.", colors.HexColor("#FFF3E0"), LARANJA),
      PageBreak()]

# ------------------------------------------------------------------ PARTE 1 — ANÁLISE DO QUE FOI FEITO
H += [P("Parte 1 — Análise de tudo o que foi realizado até agora", "h1"),
      P("Levantamento feito na pasta D:\\Projeto_Blog_Comprenolink e no site publicado em 21/10/2026.")]
H += [tabela(["O que já existe", "Situação", "Avaliação"], [
    ["Blog WordPress na Hostinger (tema Futurio) com a página /5-2/ e 21 produtos", "No ar",
     "<font color='#2E7D32'><b>Bom.</b></font> Conteúdo com benefícios e \"ideal para\" em cada produto; ~1.900 palavras; links com "
     "rel=\"sponsored\" (correto para o Google)."],
    ["21 links curtos de afiliado meli.la (relatorio_anuncios_blog.html)", "Todos ativos (HTTP 200)",
     "<font color='#2E7D32'><b>Bom.</b></font> Nenhum link quebrado."],
    ["Rastreador próprio (snippet PHP + relatório .exe por UTM, LGPD)", "Instalado e funcionando",
     "<font color='#2E7D32'><b>Muito bom.</b></font> Já registrou 110 visitas. É ele que revelou o problema da página inicial."],
    ["Gerador de links UTM (links_anuncios_*.csv/html)", "7 links criados (TikTok, Instagram, WhatsApp, TikTok Ads)",
     "<font color='#E65100'><b>Pronto mas não usado:</b></font> nenhum desses links trouxe visita real."],
    ["3 vídeos do TikTok (fones JBL x QCY, Alexa, TVs Philco x LG) + guia de publicação", "Vídeos prontos",
     "<font color='#E65100'><b>Atenção:</b></font> não aparece nenhuma visita vinda do TikTok além do teste → "
     "provavelmente não foram publicados, ou o link da bio está sem UTM / sem link."],
    ["Automação Instagram (calendário de 20 posts, artes PNG, lembretes .ics, manual PDF)", "Gerado em 29/09",
     "<font color='#E65100'><b>Atenção:</b></font> nenhuma visita do Instagram registrada → o calendário não foi executado."],
    ["Mensagens prontas para WhatsApp/Telegram/Pinterest (docx)", "Prontas",
     "<font color='#E65100'><b>Atenção:</b></font> o texto usa o link sem UTM, então mesmo que tenha sido enviado, "
     "não dá para medir. Trocar pelo link etiquetado."],
    ["Pasta vendas_afiliados (vendas do painel ML)", "Vazia",
     "<font color='#C62828'><b>Falta:</b></font> sem exportar as vendas não se sabe o que vendeu."],
    ["Página inicial do site", "Era \"Hello world!\" padrão",
     "<font color='#C62828'><b>Era crítico:</b></font> recebia 95% das visitas e não levava a nenhum produto. "
     "<font color='#2E7D32'><b>Corrigido em 21/10/2026</b></font> (Parte 0)."],
], [5.5, 3.6, 7.9])]
H += [P("Conclusão da análise", "h2"),
      P("A parte técnica (blog, links, rastreio, materiais de divulgação) está <b>acima da média</b> para quem está "
        "começando. O que faltou foi a <b>execução da divulgação</b> e o <b>acabamento do site</b>. A boa notícia: quase "
        "tudo o que falta é gratuito e boa parte do material já está pronto — só precisa ser publicado."),
      PageBreak()]

# ------------------------------------------------------------------ PARTE 2 — DIAGNÓSTICO
OK = "<font color='#2E7D32'><b>Corrigido</b></font>"
PARC = "<font color='#E65100'><b>Em parte</b></font>"
PEND = "<font color='#C62828'><b>Pendente</b></font>"
H += [P("Parte 2 — Diagnóstico da página e do site (21/10/2026)", "h1"),
      P(f"A coluna <b>Situação</b> mostra o que já foi resolvido em {ATUALIZADO_EM}."),
      tabela(["#", "Problema encontrado", "Gravidade", "Efeito nas vendas", "Situação"], [
          ["1", "Página inicial (comprenolink.net/) mostra \"Hello world!\", \"Recent Posts\", comentário de exemplo e nenhum link para os produtos.", "<font color='#C62828'><b>Crítica</b></font>", "95% das visitas se perdem.", OK],
          ["2", "Título da página /5-2/ está vazio: no Google e na aba do navegador aparece só \"- comprenolink.net\". Há também um H1 vazio antes do título.", "<font color='#C62828'><b>Crítica</b></font>", "Quase impossível aparecer no Google.", OK],
          ["3", "Endereço /5-2/ não diz nada (não tem palavra-chave) e alguém já digitou /5.2/ errado.", "Alta", "Pior posição no Google; difícil de lembrar/divulgar.", OK + ": agora /melhores-produtos-mercado-livre-2026/"],
          ["4", "Mensagens de erro visíveis para o visitante: \"Não foi possível buscar os produtos no banco de dados e/ou na API\" (aparece nos itens 8, 10 e 15).", "Alta", "Passa imagem de site quebrado → menos confiança e menos cliques.", OK],
          ["5", "Título do item diferente do produto mostrado: \"Galaxy A15\" mostra A17; \"Controle DualSense\" mostra um carregador; \"Teclado Mecânico\" mostra só um jogo de teclas; \"SSD 480GB/1TB\" mostra SSD externo; texto solto \"Samsung Galaxy M55\" no item do iPhone; \"Benefícios\" fora do lugar no item 18.", "Alta", "Visitante desconfia; Mercado Livre pode não converter (produto não é o que ele queria).", OK],
          ["5b", "<b>Encontrado depois:</b> os 21 títulos de produto linkavam para a busca do Mercado Livre sem a etiqueta de afiliado.", "<font color='#C62828'><b>Crítica</b></font>", "Venda pelo título não gerava comissão.", OK],
          ["6", "Não existe aviso de afiliado (\"este site recebe comissão\"), nem páginas Sobre, Contato e Política de Privacidade (/sobre/ dá erro 404).", "Média", "Menos confiança; exigido por boas práticas (CONAR/Google) e por plataformas de anúncio.", OK],
          ["7", "Meta descrição é só o começo do texto, cortada no meio da frase.", "Média", "Menos cliques no resultado do Google.", PEND + ": escrever no All in One SEO"],
          ["8", "Página pesada (42 imagens, 85 links de produto; carregamento medido de vários segundos).", "Média", "No celular, parte das pessoas desiste antes de carregar.", PARC + ": 4 cartões a menos; falta o passo 9"],
          ["9", "Sem tabela-resumo no topo: o visitante precisa rolar 21 produtos para achar o que quer.", "Média", "Menos cliques; quem chega procurando \"fone\" vai embora.", OK],
          ["10", "Preços fixos no texto (ex.: R$ 319,00) — o Mercado Livre muda preços todo dia.", "Baixa", "Se o preço do ML for maior, a pessoa se frustra.", PARC + ": aviso de preço adicionado"],
          ["11", "<b>Encontrado depois:</b> os navegadores guardavam as páginas por 7 dias.", "Média", "Mudanças (preços, Black Friday) demoravam até 1 semana para aparecer.", OK + ": agora 10 min"],
      ], [0.8, 6.6, 1.8, 4.4, 3.4]),
      PageBreak()]

# ------------------------------------------------------------------ PARTE 3 — FUNIL
H += [P("Parte 3 — Entenda a conta: por que o foco é tráfego", "h1"),
      P("Venda de afiliado é um funil. Cada etapa perde gente. Exemplo <b>ilustrativo</b> (os números reais você verá no seu relatório):"),
      tabela(["Etapa", "Exemplo", "Onde melhorar"], [
          ["Pessoas que visitam a página", "1.000 visitas/mês", "Fases 3, 4, 5 e 6 (divulgação, SEO, datas)"],
          ["Clicam em algum produto (taxa de clique)", "20% → 200 cliques", "Fases 0 e 2 (página clara, tabela no topo)"],
          ["Compram no Mercado Livre (conversão)", "3% → 6 compras", "Escolher produtos com bom preço e boa reputação"],
          ["Valor médio da compra", "R$ 300", "Misturar itens baratos (recompra) com caros"],
          ["Comissão (varia por categoria — veja no painel)", "ex.: 5% → R$ 90/mês", "Priorizar categorias de comissão maior"],
      ], [5.5, 4.5, 7]),
      Spacer(1, 6),
      P("Repare: com 1 visita real em 3 semanas, nenhum ajuste de texto resolve. <b>Primeiro trazer gente, depois "
        "melhorar a taxa de clique.</b> Também vale saber que o Mercado Livre costuma pagar comissão sobre "
        "<b>qualquer produto</b> comprado na sessão aberta pelo seu link (confirme as regras atuais no painel de Afiliados) — "
        "por isso tráfego qualificado vale mais que um anúncio perfeito."),
      caixa("<b>Metas sugeridas (realistas para quem está começando):</b><br/>"
            "• Até 10/11: 300 visitas reais na página de produtos e 1ª venda aprovada.<br/>"
            "• Até 30/11 (Black Friday): 1.500 visitas no mês e taxa de clique ≥ 15%.<br/>"
            "• Até 31/12: 3.000+ visitas/mês e 10+ vendas no mês."),
      PageBreak()]

# ------------------------------------------------------------------ PARTE 4 — CHECKLIST
H += [P("Parte 4 — Checklist cronológico passo a passo", "h1"),
      P("Hoje é quarta-feira, 21/10/2026. As datas abaixo partem de hoje. Se atrasar, mantenha a <b>ordem</b>.")]

H += [P("FASE 0 — Emergência: arrumar a vitrine (Dias 1 e 2: 21 e 22/10)", "h2")]
H += passo(1, "Transformar a página inicial numa vitrine que leva ao guia", "21/10 (hoje)", "1 a 2 h", "R$ 0",
           "95% das suas visitas chegam em comprenolink.net/ e encontram o \"Hello world!\".",
           ["Entre em <b>hpanel.hostinger.com</b> → Sites → comprenolink.net → <b>Painel do WordPress</b> (ou acesse comprenolink.net/wp-admin).",
            "Vá em <b>Posts</b> → passe o mouse em \"Hello world!\" → <b>Lixeira</b>. Vá em <b>Comentários</b> e mande o comentário de exemplo para a lixeira.",
            "Vá em <b>Páginas → Adicionar nova</b>. Título: \"Achados do Mercado Livre com o melhor custo-benefício\".",
            "No editor, adicione: (a) uma frase de boas-vindas curta; (b) um <b>Botão</b> grande \"Ver os 21 melhores produtos de 2026\" apontando para https://comprenolink.net/5-2/?utm_source=site&amp;utm_medium=home&amp;utm_campaign=botao_home; (c) 4 a 6 blocos de categoria (Fones, TVs, Celulares, Games, Acessórios) cada um com imagem e link para a âncora correspondente do guia.",
            "Publique. Depois vá em <b>Configurações → Leitura</b> → \"Sua página inicial exibe\": <b>Uma página estática</b> → Página inicial = a página que você criou → Salvar.",
            "Em <b>Configurações → Geral</b>, preencha a <b>Descrição</b> (slogan), ex.: \"Os melhores achados do Mercado Livre, testados e comparados\". Isso tira o \"comprenolink.net -\" do título.",
            "Abra o site no celular (aba anônima) e confira se o botão leva ao guia."],
           "quem entra em comprenolink.net vê produtos e um botão para o guia. No próximo relatório, \"site / home\" passa a aparecer como origem.")
H += passo(2, "Dar título e descrição de verdade à página /5-2/ (SEO básico)", "21/10", "40 min", "R$ 0 (plugin gratuito)",
           "Sem título, o Google não sabe do que a página trata; hoje ela aparece como \"- comprenolink.net\".",
           ["Em <b>Plugins → Adicionar novo</b>, procure <b>Rank Math SEO</b> (ou Yoast SEO), instale e ative. Siga o assistente no modo \"Fácil\".",
            "Abra a página /5-2/ em <b>Páginas → Editar</b>. No campo de título da página (topo do editor) escreva: \"Os 21 Melhores Produtos do Mercado Livre em 2026\". Se o título já estiver como bloco de texto dentro do conteúdo, mantenha só um dos dois para não duplicar.",
            "Remova o bloco de título/H1 vazio que aparece antes do texto (bloco \"Título\" sem conteúdo).",
            "No quadro do Rank Math: <b>Título SEO</b> \"21 Melhores Produtos do Mercado Livre em 2026 (Guia + Preços)\"; <b>Descrição</b> (até 155 caracteres): \"Comparamos fones, TVs, celulares, games e acessórios mais vendidos do Mercado Livre. Veja prós, para quem é e o link com o melhor preço.\"; <b>Palavra-chave foco</b>: \"melhores produtos mercado livre 2026\".",
            "Atualize a página. Teste no Google: digite <i>site:comprenolink.net</i> alguns dias depois."],
           "a aba do navegador mostra o título novo e o Rank Math dá nota verde/amarela.")
H += passo(3, "Endereço da página: manter /5-2/ ou trocar?", "21/10", "15 min", "R$ 0",
           "Um endereço com palavra-chave ajuda no Google, mas trocar quebra os links já distribuídos e o seu rastreador, que hoje olha só para /5-2/.",
           ["<b>Recomendação:</b> como ainda não houve tráfego real, é o melhor momento para trocar. Em Editar página → painel lateral → <b>Link/URL</b>, mude o slug para <b>melhores-produtos-mercado-livre-2026</b>.",
            "No Rank Math → <b>Redirecionamentos</b> → Adicionar: de <i>5-2</i> e <i>5.2</i> para o endereço novo (tipo <b>301</b>). Assim nenhum link antigo quebra.",
            "Atualize <b>pagina_blog</b> em D:\\Projeto_Blog_Comprenolink\\Relatorios_Diarios_Anuncios\\programas_fontes_python\\config_rastreio.json (e em Planejamentos\\Andamento\\Rastreamento_anuncios\\config_rastreio.json) para o endereço novo e gere os links UTM de novo com gerar_links_anuncios.exe.",
            "Se preferir não mexer agora, pule este passo — os passos 1 e 2 são mais importantes."],
           "o endereço novo abre a página, e /5-2/ redireciona sozinho para ele.")
H += passo(4, "Eliminar as mensagens de erro do plugin", "22/10", "30 min a 1 h", "R$ 0",
           "\"Não foi possível buscar os produtos no banco de dados e/ou na API\" aparece para o visitante nos itens 8, 10 e 15 e passa a imagem de site quebrado.",
           ["Edite a página e localize os blocos do <b>Hostinger Affiliate</b> logo abaixo dos produtos 8, 10 e 15 (são blocos extras, vazios).",
            "Apague esses blocos extras (o produto principal de cada item continua). Se a mensagem estiver no bloco principal, refaça o bloco colando o link do produto de novo.",
            "No painel do plugin (menu lateral <b>Hostinger → Affiliate</b>), confira se a conexão com o Mercado Livre está ativa.",
            "Atualize e confira a página no celular procurando a frase de erro (Ctrl+F no computador)."],
           "a frase de erro não aparece em lugar nenhum da página.")
H += passo(5, "Corrigir títulos que não batem com o produto mostrado", "22/10", "1 h", "R$ 0",
           "Quem clica em \"Controle DualSense\" e cai num carregador não compra — e perde confiança no resto da lista.",
           ["Item 10: troque o título para \"Carregador duplo para controle PS5\" <b>ou</b> troque o produto por um controle DualSense de verdade (gere o link no painel de Afiliados).",
            "Item 13: \"Teclado Mecânico\" → coloque um teclado mecânico completo (ex.: Redragon Kumara) no lugar do jogo de teclas.",
            "Item 14: título \"Galaxy A15\" mas o produto é A17 → mude o título para \"Samsung Galaxy A17 5G\".",
            "Item 8: \"SSD Kingston 480GB/1TB\" mas o produto é SSD externo → ajuste o título ou o produto.",
            "Item 17: apague o texto solto \"Samsung Galaxy M55\" e o nome do iPhone repetido. Item 18: mova \"Benefícios\" para baixo do produto.",
            "Atualize também os mesmos nomes em Automação_Instagram\\produtos.json para as artes ficarem iguais ao site."],
           "cada título descreve exatamente o produto do botão \"Compre agora\".")
H += passo(6, "Criar páginas de confiança: Aviso de afiliado, Sobre, Contato, Privacidade", "22/10", "1 h", "R$ 0",
           "Gente compra mais de site que parece ter alguém por trás. É também pré-requisito para anúncios pagos e boa prática do CONAR.",
           ["No topo do guia, coloque um parágrafo pequeno: \"<i>Este site participa do programa de Afiliados do Mercado Livre. Ao comprar pelos nossos links, podemos receber uma comissão, sem custo extra para você.</i>\"",
            "Crie a página <b>Sobre</b> (quem é você, por que indica produtos, como escolhe).",
            "Crie <b>Contato</b> (e-mail ou WhatsApp Business) e <b>Política de Privacidade</b> (WordPress já tem modelo em Configurações → Privacidade).",
            "Em <b>Aparência → Menus</b>, monte o menu: Início | Melhores Produtos 2026 | Black Friday (depois) | Sobre | Contato."],
           "o menu aparece em todas as páginas e o aviso está visível no topo do guia.")

H += [P("FASE 1 — Medir tudo (Dias 3 a 5: 23 a 25/10)", "h2")]
H += passo(7, "Cadastrar o site no Google Search Console e no Bing", "23/10", "40 min", "R$ 0",
           "É assim que o Google descobre a página e mostra quais pesquisas trazem você.",
           ["Acesse <b>search.google.com/search-console</b> com sua conta Google → Adicionar propriedade → <b>Domínio</b> comprenolink.net.",
            "Copie o registro TXT. No hPanel → <b>Domínios → DNS / Nameservers</b> → Adicionar registro TXT → cole → salvar. Volte e clique Verificar (pode levar até algumas horas).",
            "Em <b>Sitemaps</b>, envie o endereço que o Rank Math mostra (normalmente sitemap_index.xml).",
            "Em <b>Inspeção de URL</b>, cole o endereço do guia → <b>Solicitar indexação</b>. Faça o mesmo com a página inicial.",
            "Repita no <b>Bing Webmaster Tools</b> (bing.com/webmasters) — dá para importar do Google com 1 clique."],
           "o Search Console mostra a página como \"indexada\".")
H += passo(8, "Instalar o Google Analytics 4 (Site Kit)", "23/10", "30 min", "R$ 0",
           "O seu rastreador mostra visitas e cliques por anúncio; o GA4 complementa com tempo na página e rolagem.",
           ["Plugins → Adicionar novo → <b>Site Kit by Google</b> → ativar → conectar com a mesma conta do Search Console.",
            "Ative Analytics. Em 48 h os dados começam a aparecer."],
           "o painel do Site Kit mostra visitantes do dia.")
H += passo(9, "Medir a velocidade e acelerar o site", "24/10", "1 h", "R$ 0",
           "No celular, cada segundo a mais de carregamento faz parte das pessoas desistir.",
           ["Teste em <b>pagespeed.web.dev</b> com o endereço do guia (aba Celular). Anote a nota.",
            "No WordPress, instale <b>LiteSpeed Cache</b> (a Hostinger usa servidor LiteSpeed; o plugin pode já estar lá). Ative: Cache, Otimização de imagens (WebP) e <b>Lazy load</b> de imagens.",
            "No hPanel, ative o <b>CDN</b> da Hostinger se o seu plano tiver (planos Business/Cloud). Alternativa gratuita: Cloudflare (plano Free).",
            "Teste de novo e compare. Meta: nota de celular acima de 60."],
           "a nota do PageSpeed no celular subiu e a página abre em poucos segundos no 4G.")
H += passo(10, "Ligar as vendas do Mercado Livre ao seu relatório", "25/10 e toda segunda-feira", "15 min", "R$ 0",
           "Hoje a pasta vendas_afiliados está vazia; sem ela o relatório não mostra quais anúncios vendem.",
           ["Entre no painel <b>Mercado Livre Afiliados</b> → Relatórios/Ganhos → exporte o período (CSV ou Excel).",
            "Salve o arquivo em <b>D:\\Projeto_Blog_Comprenolink\\Relatorios_Diarios_Anuncios\\vendas_afiliados</b>.",
            "Rode <b>relatorio_acessos_anuncios.exe</b> e abra o HTML gerado.",
            "No painel de Afiliados, crie também <b>etiquetas (IDs) diferentes por canal</b> se o programa permitir (ex.: blog, tiktok, insta) e preencha \"etiqueta_afiliado\" no config_rastreio.json."],
           "o relatório mostra vendas aprovadas/pendentes ao lado das visitas.")

H += [P("FASE 2 — Página que converte (Semana 2: 26/10 a 01/11)", "h2")]
H += passo(11, "Colocar uma tabela \"Escolha rápida\" no topo do guia", "26/10", "1 h", "R$ 0",
           "A maioria das pessoas no celular não rola 21 produtos. Uma tabela no topo leva direto ao que ela quer.",
           ["Logo após a introdução, adicione um bloco <b>Tabela</b> com 3 colunas: Categoria | Melhor escolha | Botão.",
            "Linhas sugeridas: Melhor fone barato (QCY) • Melhor fone (JBL) • Melhor TV barata (Philco) • Melhor TV (LG) • Celular custo-benefício (Moto G24) • Presente até R$ 200 • Para gamers (PS5).",
            "Na coluna Botão, use o mesmo link meli.la do produto, com texto \"Ver preço hoje\".",
            "Adicione também um <b>Índice</b> (bloco \"Table of Contents\" do Rank Math) com âncoras para cada categoria."],
           "na primeira tela do celular aparece a tabela com botões.")
H += passo(12, "Melhorar botões, preços e chamadas", "27/10", "1 h", "R$ 0",
           "Pequenos detalhes de botão e texto costumam aumentar bastante a taxa de clique.",
           ["Troque \"Compre agora\" por textos como <b>\"Ver preço e frete no Mercado Livre\"</b> ou \"Ver oferta de hoje\" (cor forte: amarelo ML ou verde).",
            "Onde o preço é fixo, adicione \"<i>preço consultado em DD/MM; pode mudar</i>\" ou deixe o plugin buscar o preço automaticamente.",
            "Em cada produto, acrescente 1 linha \"<b>Não compre se...</b>\" (honestidade aumenta a confiança).",
            "Acrescente no fim uma seção <b>Perguntas frequentes</b> (\"É seguro comprar no Mercado Livre?\", \"Como saber se o vendedor é confiável?\", \"Tem garantia?\")."],
           "cada produto tem botão claro e a página tem FAQ.")
H += passo(13, "Quebrar o guia em páginas por nicho (uma por semana)", "a partir de 28/10", "2 a 3 h por página", "R$ 0 (ou R$ 40 a 120 por texto se contratar redator)",
           "Quem pesquisa no Google digita \"melhor fone bluetooth até 300 reais\", não \"21 produtos\". Páginas específicas aparecem melhor e convertem mais.",
           ["Ordem sugerida: (1) Melhores fones Bluetooth 2026; (2) Melhor Smart TV 32\" custo-benefício; (3) Melhores presentes até R$ 100 / R$ 200 (ótimo para Natal); (4) Melhores celulares até R$ 1.500; (5) JBL Tune 720BT vale a pena? (review); (6) QCY vs JBL (comparativo).",
            "Cada página: 800–1.500 palavras, tabela no topo, 3 a 7 produtos, prós/contras, FAQ, link para o guia principal e vice-versa.",
            "Pode usar IA (ChatGPT/Claude/Gemini) como rascunho, mas <b>revise, inclua opinião própria e fotos</b> — texto genérico não ranqueia.",
            "Se contratar redator (Workana, 99Freelas): estimativa de R$ 40 a 120 por artigo de 1.000 palavras."],
           "pelo menos 1 página nova publicada por semana, cada uma com links UTM próprios.")

H += [P("FASE 3 — Colocar a divulgação que já está pronta no ar (começa em 23/10 e segue todo dia)", "h2")]
H += passo(14, "Publicar os 3 vídeos do TikTok com o link certo", "23 a 25/10 (1 por dia)", "30 min por vídeo", "R$ 0 (CapCut Pro opcional ~R$ 30 a 60/mês)",
           "Os vídeos estão em D:\\Projeto_Blog_Comprenolink\\Logo\\Videos_TikTok, mas nenhuma visita veio do TikTok.",
           ["Mude a conta para <b>Conta comercial</b> (Configurações → Conta) — é grátis.",
            "No campo <b>Site</b> do perfil coloque o link UTM da bio (está em links_anuncios_2026-10-20_13h41.csv, linha \"tiktok;bio\"). Se o campo Site ainda não estiver liberado, use um Linktree/Bio Link grátis com os links UTM de cada vídeo.",
            "Publique 1 vídeo por dia entre 18h e 21h, seguindo o guia .docx da pasta. Na legenda: \"link na bio, item 1 do guia\".",
            "Responda todos os comentários nas primeiras 2 horas (o TikTok entrega mais vídeos com conversa).",
            "Depois dos 3, grave <b>1 vídeo novo por dia</b> (15–30 s): \"3 achados até R$ 100 no Mercado Livre\", \"não compre este fone antes de ver isso\", unboxing, comparativos."],
           "o relatório mostra visitas com origem tiktok / video / nome do vídeo.")
H += passo(15, "Executar o calendário do Instagram (20 posts já prontos)", "a partir de 26/10", "20 a 30 min por dia", "R$ 0 (Canva Pro opcional ~R$ 35/mês; ManyChat grátis até certo limite)",
           "As artes e legendas foram geradas em Automação_Instagram\\saida, mas não foram publicadas.",
           ["Abra Automação_Instagram\\saida\\calendario_instagram_*.html. Se as datas já passaram, mude \"data_inicio\" em config_instagram.json para 26/10/2026 e rode 1_gerar_calendario.py e 2_gerar_artes.py de novo.",
            "Importe o arquivo .ics no Google Agenda do celular para receber os lembretes.",
            "Agende os posts no <b>Meta Business Suite</b> (grátis) — dá para agendar uma semana inteira de uma vez.",
            "Use a estratégia \"comenta FONE que eu te mando o link\" e responda no Direct com o link UTM do post. ManyChat (oficial da Meta) automatiza isso.",
            "Mantenha o link da bio com o UTM da semana (semana1, semana2...)."],
           "o relatório mostra origem instagram (bio / stories / dm).")
H += passo(16, "Criar seu Canal no WhatsApp e um canal no Telegram", "27/10", "1 h para montar; 15 min/dia", "R$ 0 (chip dedicado opcional ~R$ 15 a 30/mês)",
           "Canal próprio é audiência sua: cada nova oferta chega direto no celular das pessoas, sem depender de algoritmo.",
           ["No <b>WhatsApp Business</b>, aba Atualizações → Canais → Criar canal \"Achados Compre no Link\". No Telegram, crie um canal com o mesmo nome.",
            "Atualize as mensagens do arquivo \"Como Executar a Estratégia de Divulgação do Blog.docx\" para usar o link UTM \"whatsapp;social;grupos\" (crie outro para telegram no gerar_links_anuncios).",
            "Poste 2 a 3 ofertas por dia (manhã, almoço, noite). Formato: foto + preço + 1 benefício + link.",
            "Convide amigos/família e coloque o link do canal no site, na bio do Instagram e no TikTok.",
            "Grupos de terceiros: só poste onde o administrador permite divulgação. Mandar link em grupo sem autorização gera denúncia e bloqueio."],
           "canal criado, link no site e primeiras visitas com origem whatsapp/telegram no relatório.")
H += passo(17, "Pinterest: pins que trazem visita por meses", "28/10", "1 h para montar; 15 min/dia", "R$ 0",
           "No Pinterest os pins continuam trazendo cliques por muito tempo e o link é clicável direto no pin.",
           ["Crie uma conta <b>Empresa</b> em business.pinterest.com e confirme o site comprenolink.net (meta tag via Rank Math → Configurações gerais → Webmaster Tools).",
            "Crie pastas: Fones, Casa Inteligente, TVs, Games, Presentes de Natal, Black Friday.",
            "Reaproveite as artes do Instagram (formato vertical 1000×1500 é o ideal) — 3 a 5 pins por dia, cada um com título com palavra-chave e o link UTM do blog (origem pinterest)."],
           "pins publicados e visitas com origem pinterest no relatório.")
H += passo(18, "YouTube Shorts e Facebook com os mesmos vídeos", "a partir de 29/10", "10 min por vídeo", "R$ 0",
           "O mesmo vídeo do TikTok publicado em mais 2 redes multiplica o alcance sem trabalho extra.",
           ["Baixe o vídeo <b>sem marca d'água</b> (salve o arquivo original do CapCut).",
            "Publique como Short no YouTube e como Reels no Facebook/Instagram. No YouTube, coloque o link UTM na descrição do canal e num comentário fixado.",
            "Use o mesmo título com palavra-chave (\"Melhor fone até R$ 300 em 2026\")."],
           "visitas com origem youtube/facebook no relatório.")

H += [P("FASE 4 — Datas que vendem: 11.11, Black Friday e Natal (preparar até 10/11)", "h2")]
H += passo(19, "Criar a página \"Black Friday 2026 Mercado Livre\"", "02 a 10/11", "3 a 4 h", "R$ 0",
           "A Black Friday é 27/11/2026 (Cyber Monday 30/11). As pessoas pesquisam semanas antes — a página precisa estar no Google cedo.",
           ["Crie a página <b>/black-friday-mercado-livre-2026/</b> com: contagem regressiva, \"como saber se o desconto é real\", tabela de produtos com preço antes x agora, e seção que você atualiza todo dia.",
            "Peça indexação no Search Console no mesmo dia.",
            "Anote os preços atuais dos 21 produtos <b>agora</b> (planilha): na Black Friday você mostra \"caiu de X para Y\" com prova.",
            "Prepare 10 artes/vídeos \"esquenta Black Friday\" para 18 a 26/11 e um roteiro para o dia 27/11 (postar a cada 2–3 horas)."],
           "página publicada até 10/11 e linkada no menu e na home.")
H += passo(20, "Aproveitar o 11.11 e montar o guia de presentes de Natal", "11/11 e 01 a 20/12", "2 h cada", "R$ 0",
           "11/11 é dia de promoções grandes no Mercado Livre; dezembro é o mês dos presentes.",
           ["Em 10 e 11/11: posts e mensagens no canal com as melhores ofertas do dia.",
            "Até 01/12: publicar \"Presentes de Natal até R$ 50 / R$ 100 / R$ 200\" (aproveita os itens baratos: capinha, película, microSD, mouse, carregador).",
            "Lembrar a data-limite de entrega para o Natal nas postagens (\"compre até dia X para chegar antes do Natal\" — confira os prazos no ML)."],
           "páginas e posts sazonais publicados antes de cada data.")

H += [P("FASE 5 — SEO contínuo (Semanas 3 a 8 em diante)", "h2")]
H += passo(21, "Rotina de SEO semanal", "toda sexta-feira", "1 h", "R$ 0",
           "O Google leva de 4 a 12 semanas para dar posições boas; quem publica com regularidade ganha.",
           ["No Search Console → <b>Desempenho</b>: veja as pesquisas com muitas impressões e poucos cliques e melhore o título/descrição dessas páginas.",
            "Ligue cada página nova às antigas (links internos) e ao guia principal.",
            "Atualize a data e os preços do guia a cada 15 dias (\"atualizado em DD/MM/2026\").",
            "Use o test_blog_seo.exe que já existe na pasta Relatorios_Diarios_Anuncios\\programas_fontes_python para checar a página depois de cada mudança."],
           "1 página nova por semana e o guia atualizado a cada 15 dias.")

H += [P("FASE 6 — Lista própria de contatos (a partir da Semana 4)", "h2")]
H += passo(22, "Capturar e-mails / WhatsApp de quem visita", "04/11", "1 a 2 h", "R$ 0 (Brevo ou MailerLite no plano grátis)",
           "Quem visitou e não comprou hoje pode comprar na Black Friday — se você tiver como avisar.",
           ["Crie conta grátis no <b>Brevo</b> ou <b>MailerLite</b> e instale o plugin deles no WordPress.",
            "Adicione um formulário simples: \"Receba os alertas de preço da Black Friday\" (nome + e-mail) no guia e na home. Mencione a Política de Privacidade (LGPD).",
            "Mande 1 e-mail por semana com 5 achados e, na Black Friday, 1 por dia (27/11 a 30/11)."],
           "formulário no ar e primeiros inscritos.")

H += [P("FASE 7 — Medir, decidir e repetir (toda segunda-feira)", "h2")]
H += passo(23, "Reunião de 30 minutos com os seus números", "toda segunda-feira", "30 min", "R$ 0",
           "Sem olhar os números você continua fazendo o que não funciona.",
           ["Exporte vendas do painel de Afiliados → vendas_afiliados → rode relatorio_acessos_anuncios.exe.",
            "Preencha a planilha semanal: visitas, cliques, taxa de clique, vendas, comissão por canal (veja Parte 7).",
            "Regra simples: o canal/post que mais trouxe <b>cliques</b> ganha o dobro de posts na semana; o que trouxe zero por 2 semanas é trocado.",
            "Os produtos mais clicados vão para o topo da tabela \"Escolha rápida\"."],
           "planilha preenchida e uma decisão anotada por semana.")

H += [P("FASE 8 — Opcional e pago: anúncios (só depois das Fases 0 a 3 prontas)", "h2"),
      caixa("<b>Só pague anúncio quando:</b> a página inicial e o guia estiverem arrumados, o relatório estiver medindo, e "
            "a divulgação gratuita já tiver trazido algum clique. Anúncio em página com problema é dinheiro jogado fora. "
            "Leia antes os <b>termos do programa de Afiliados do Mercado Livre</b>: em geral é proibido usar a marca "
            "\"Mercado Livre\" em anúncios de busca e mandar o anúncio direto para o link de afiliado.",
            colors.HexColor("#FFF3E0"), LARANJA), Spacer(1, 6)]
H += passo(24, "Teste pequeno de anúncio no Instagram/Facebook ou Pinterest", "a partir de 11/11 (esquenta Black Friday)", "1 h para montar", "R$ 10 a 20 por dia, por 7 dias = ~R$ 70 a 140 por teste",
           "Com orçamento pequeno dá para descobrir se um produto/público dá retorno antes de investir mais.",
           ["No Meta Business Suite → <b>Impulsionar</b> o post que mais teve cliques orgânicos (já provou que funciona).",
            "Destino: a página do blog com link UTM (origem facebook, meio cpc). Público: Brasil, 18–45, interesses do produto.",
            "Orçamento: R$ 10 a 20/dia por 7 dias. Depois compare: comissão gerada x valor gasto.",
            "Se a comissão não cobrir o gasto em 2 testes, volte ao orgânico — no começo isso é normal.",
            "TikTok Ads já tem link criado (tiktok_ads_teste); o mínimo costuma ser maior (~R$ 50/dia por campanha) — deixe para depois."],
           "você sabe quanto custou cada clique e cada venda do anúncio.")
H += [PageBreak()]

# ------------------------------------------------------------------ PARTE 5 — CALENDÁRIO
H += [P("Parte 5 — Calendário semana a semana (21/10 a 20/12/2026)", "h1"),
      tabela(["Semana", "Datas", "O que fazer (passos)", "Custo"], [
          ["1", "21 a 27/10", "<font color='#2E7D32'><b>Fase 0 (passos 1–6) e passos 11–12: FEITOS em 21/10</b></font> • Fase 1 (7–10) • começar TikTok (14) • criar canal WhatsApp/Telegram (16)", "R$ 0"],
          ["2", "28/10 a 03/11", "Tabela no topo e botões (11–12) • 1ª página de nicho: fones (13) • Instagram diário (15) • Pinterest (17) • Shorts (18) • começar página Black Friday (19)", "R$ 0 (opc. Canva/CapCut ~R$ 65–95/mês)"],
          ["3", "04 a 10/11", "Publicar Black Friday e pedir indexação (19) • formulário de e-mail (22) • 2ª página de nicho: TVs • rotina SEO (21)", "R$ 0"],
          ["4", "11 a 17/11", "11.11: ofertas do dia (20) • 3ª página: presentes até R$ 100/200 • 1º teste de anúncio, opcional (24)", "R$ 0 (opc. anúncio ~R$ 70–140)"],
          ["5", "18 a 24/11", "Esquenta Black Friday: 2–3 posts/dia, e-mail semanal, atualizar preços diariamente", "R$ 0"],
          ["6", "25/11 a 01/12", "<b>Black Friday 27/11 e Cyber Monday 30/11</b>: postar a cada 2–3 h, e-mail diário, atualizar a página de manhã e à tarde", "R$ 0 (opc. anúncio ~R$ 100–200)"],
          ["7", "02 a 08/12", "Analisar resultados da BF • guia de presentes de Natal no topo da home • 4ª página: celulares", "R$ 0"],
          ["8", "09 a 20/12", "Natal: \"compre até dia X para chegar\" • reforçar itens baratos • preparar janeiro (volta às aulas, liquidações)", "R$ 0"],
      ], [1.4, 2.6, 10.2, 2.8]),
      Spacer(1, 8),
      P("Rotina diária sugerida (1 a 2 horas)", "h2"),
      tabela(["Horário", "Tarefa", "Tempo"], [
          ["Manhã", "Ver ofertas do dia no Mercado Livre; postar 1 oferta no canal WhatsApp/Telegram; 3 pins", "20 min"],
          ["Almoço", "Responder comentários e Directs (TikTok/Instagram) com o link UTM", "15 min"],
          ["Noite (18–21h)", "Publicar 1 vídeo curto (TikTok → Shorts → Reels) + 1 story com link; 1 oferta no canal", "40 min"],
          ["Fim de semana", "Escrever/revisar 1 página de nicho; gravar vídeos da semana em lote", "2 a 3 h"],
      ], [3, 11.5, 2.5]),
      PageBreak()]

# ------------------------------------------------------------------ PARTE 6 — CUSTOS
H += [P("Parte 6 — Resumo de custos (estimativas de outubro/2026)", "h1"),
      tabela(["Item", "Obrigatório?", "Custo estimado", "Observação"], [
          ["Hospedagem Hostinger", "Sim (já contratado)", "Já pago", "Confira a data de renovação no hPanel; a renovação costuma ser mais cara que o 1º ano."],
          ["Domínio comprenolink.net", "Sim", "~R$ 50 a 90 por ano", "Às vezes vem grátis no 1º ano do plano. Ative a renovação automática para não perder o site."],
          ["Plugins WordPress (Rank Math, Site Kit, LiteSpeed Cache)", "Sim", "R$ 0", "Versões gratuitas bastam."],
          ["Google Search Console, GA4, Bing Webmaster, PageSpeed", "Sim", "R$ 0", ""],
          ["TikTok, Instagram, Pinterest, YouTube, WhatsApp/Telegram, Meta Business Suite", "Sim", "R$ 0", ""],
          ["Brevo / MailerLite (e-mail)", "Recomendado", "R$ 0", "Grátis até um limite de contatos/envios; pago só se a lista crescer muito."],
          ["Canva Pro", "Opcional", "~R$ 35/mês", "A versão grátis + as artes que o script já gera resolvem no começo."],
          ["CapCut Pro", "Opcional", "~R$ 30 a 60/mês", "A versão grátis edita bem vídeos curtos."],
          ["ManyChat (resposta automática no Direct)", "Opcional", "R$ 0 no início; ~R$ 75/mês (≈US$ 15) no Pro", ""],
          ["Chip de celular só para o canal", "Opcional", "~R$ 15 a 30/mês", "Separa o pessoal do trabalho."],
          ["Tripé + ring light para vídeos", "Opcional", "~R$ 50 a 150 (uma vez)", ""],
          ["Redator freelancer", "Opcional", "~R$ 40 a 120 por artigo", "Ou escreva você com ajuda de IA e revise."],
          ["Anúncios Meta/Pinterest", "Opcional", "~R$ 10 a 20/dia por teste", "Só depois das Fases 0–3."],
      ], [5, 2.6, 3.6, 5.8]),
      Spacer(1, 8),
      P("Três cenários de investimento mensal", "h2"),
      tabela(["Cenário", "O que inclui", "Custo por mês", "Para quem"], [
          ["<b>Zero</b>", "Todos os passos gratuitos (Fases 0 a 7)", "<b>R$ 0</b> + ~1 a 2 h/dia", "Começar agora, sem risco. <b>Recomendado até a Black Friday.</b>"],
          ["<b>Econômico</b>", "Zero + Canva Pro + CapCut Pro + chip", "~R$ 70 a 150", "Quando já estiver postando todo dia e quiser ganhar tempo."],
          ["<b>Acelerado</b>", "Econômico + 2 redatores/mês + anúncios R$ 10–20/dia", "~R$ 450 a 900", "Só quando o relatório provar que um canal vende e a comissão paga o anúncio."],
      ], [2.6, 6, 3.4, 5]),
      Spacer(1, 6),
      caixa("<b>Regra de ouro do dinheiro:</b> não gaste por mês mais do que a comissão aprovada do mês anterior, "
            "exceto o teste pequeno de anúncio. Comece no cenário Zero; suba de cenário só quando os números pedirem.",
            colors.HexColor("#E8F5E9"), VERDE),
      PageBreak()]

# ------------------------------------------------------------------ PARTE 7 — PLANILHA SEMANAL
H += [P("Parte 7 — Planilha semanal de acompanhamento", "h1"),
      P("Copie esta tabela num caderno ou no Excel e preencha toda segunda-feira com os números do relatório e do painel de Afiliados."),
      tabela(["Semana", "Visitas no guia", "Cliques meli.la", "Taxa de clique", "Vendas aprov.", "Comissão R$", "Melhor canal", "Decisão da semana"],
             [[str(i), "", "", "", "", "", "", ""] for i in range(1, 9)], [1.3, 2, 2, 1.9, 1.8, 1.9, 2.4, 3.7], zebra=False),
      Spacer(1, 8),
      P("Como ler os números", "h2")]
H += lista([
    "<b>Muitas visitas e poucos cliques</b> (taxa &lt; 10%): o problema é a página — reveja tabela do topo, botões e se o produto bate com o título.",
    "<b>Muitos cliques e nenhuma venda</b> em 2 semanas: o produto está caro, o vendedor tem reputação ruim ou o frete é alto — troque o produto por outro semelhante.",
    "<b>Poucas visitas</b>: o problema é divulgação — aumente a frequência no canal que mais trouxe visitas.",
    "<b>Um post trouxe muito mais visitas que os outros</b>: faça mais 3 variações dele na mesma semana.",
])
H += [Spacer(1, 6), P("Parte 8 — O que NÃO fazer", "h1")]
H += lista([
    "Não usar robôs de seguir/curtir nem comprar seguidores — as redes derrubam o alcance ou a conta.",
    "Não mandar link em grupos sem permissão do administrador nem fazer spam no privado de desconhecidos.",
    "Não usar a marca \"Mercado Livre\" como palavra-chave em anúncios de busca e não mandar anúncio pago direto para o link meli.la — confira sempre os termos do programa de Afiliados.",
    "Não prometer preço (\"R$ 319 garantido\"): o preço é do vendedor e muda; diga \"preço consultado em...\".",
    "Não esconder que é link de afiliado — avise no site e use #publi / \"link de afiliado\" nas redes.",
    "Não mudar 10 coisas ao mesmo tempo: mude uma, espere uma semana, olhe o relatório.",
])
H += [Spacer(1, 8), P("Glossário rápido", "h2"),
      tabela(["Termo", "O que significa"], [
          ["UTM", "Etiqueta no fim do link (?utm_source=tiktok...) que diz ao seu relatório de onde veio a visita."],
          ["Taxa de clique (CTR)", "De cada 100 visitas, quantas clicaram em algum produto."],
          ["Conversão", "De cada 100 cliques no Mercado Livre, quantos viraram compra."],
          ["SEO", "Ajustes para a página aparecer nas pesquisas do Google."],
          ["Indexar", "O Google guardar a sua página para mostrá-la nas pesquisas."],
          ["Slug", "A parte final do endereço da página (ex.: /5-2/)."],
          ["Redirecionamento 301", "Aviso permanente de que uma página mudou de endereço; leva o visitante e o Google para o endereço novo."],
          ["Home / página inicial", "O endereço principal comprenolink.net/."],
      ], [4, 13]),
      Spacer(1, 10),
      P("<i>Documento gerado em 21/10/2026 a partir dos dados do rastreador (110 eventos de 29/09 a 20/10/2026) e da "
        "análise da página publicada. Para regerar: python D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Hold\\Dados_Tiktok\\gerar_checklist_vendas_pdf.py</i>", "pq")]


def main():
    doc = BaseDocTemplate(SAIDA, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=1.8 * cm,
                          title="Checklist para turbinar as vendas do blog comprenolink.net", author="comprenolink.net")
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="f")
    doc.addPageTemplates([PageTemplate(id="p", frames=[frame], onPage=rodape)])
    doc.build(H)
    print("PDF gerado:", SAIDA)


if __name__ == "__main__":
    main()
