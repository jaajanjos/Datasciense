# -*- coding: utf-8 -*-
"""Gera o PDF 'Conversão e Performance do Blog' a partir dos relatórios de 21-22/10/2026."""
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                                PageBreak, KeepTogether)
from reportlab.graphics.shapes import Drawing, String
from reportlab.graphics.charts.barcharts import VerticalBarChart
from reportlab.graphics.charts.linecharts import HorizontalLineChart

SAIDA = sys.argv[1]

AZUL = colors.HexColor("#1f4e79")
AZUL_CLARO = colors.HexColor("#dbe7f3")
AMARELO = colors.HexColor("#fff4cc")
VERDE = colors.HexColor("#e2f0d9")
VERMELHO = colors.HexColor("#f8d7da")
CINZA = colors.HexColor("#f2f2f2")

ss = getSampleStyleSheet()
H1 = ParagraphStyle("H1", parent=ss["Title"], fontSize=20, textColor=AZUL, spaceAfter=4)
SUB = ParagraphStyle("SUB", parent=ss["Normal"], fontSize=10, textColor=colors.grey, alignment=1)
H2 = ParagraphStyle("H2", parent=ss["Heading2"], textColor=AZUL, spaceBefore=12, spaceAfter=6)
TX = ParagraphStyle("TX", parent=ss["Normal"], fontSize=10, leading=14, spaceAfter=4)
TXP = ParagraphStyle("TXP", parent=TX, fontSize=8.5, leading=11)
CEL = ParagraphStyle("CEL", parent=ss["Normal"], fontSize=8.5, leading=10.5)
CELB = ParagraphStyle("CELB", parent=CEL, fontName="Helvetica-Bold", fontSize=7.5, leading=9, textColor=colors.white)


def P(t, s=TX):
    return Paragraph(t, s)


def tabela(linhas, larguras, cab=True, zebra=True, extra=None):
    dados = []
    for i, l in enumerate(linhas):
        estilo = CELB if (cab and i == 0) else CEL
        dados.append([Paragraph(str(c), estilo) for c in l])
    t = Table(dados, colWidths=larguras, repeatRows=1 if cab else 0)
    st = [("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b0b0b0")),
          ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if cab:
        st.append(("BACKGROUND", (0, 0), (-1, 0), AZUL))
    if zebra:
        for i in range(1 if cab else 0, len(dados)):
            if i % 2 == 0:
                st.append(("BACKGROUND", (0, i), (-1, i), CINZA))
    if extra:
        st += extra
    t.setStyle(TableStyle(st))
    return t


def caixa(texto, cor):
    t = Table([[Paragraph(texto, TX)]], colWidths=[17 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), cor),
                           ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor("#999999")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def kpis(itens):
    cel = []
    for valor, rotulo in itens:
        cel.append(Paragraph(f'<para align="center"><font size="18" color="#1f4e79"><b>{valor}</b></font>'
                             f'<br/><font size="8">{rotulo}</font></para>', CEL))
    t = Table([cel], colWidths=[17 * cm / len(itens)] * len(itens), rowHeights=[2.0 * cm])
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.6, AZUL), ("INNERGRID", (0, 0), (-1, -1), 0.4, AZUL),
                           ("BACKGROUND", (0, 0), (-1, -1), AZUL_CLARO), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    return t


def grafico_evolucao():
    d = Drawing(17 * cm, 5.6 * cm)
    c = VerticalBarChart()
    c.x, c.y, c.width, c.height = 40, 25, 17 * cm - 70, 5.6 * cm - 55
    c.data = [[22, 31, 33, 34, 38], [4, 5, 5, 6, 6], [3, 11, 11, 12, 12], [1, 3, 3, 3, 3]]
    c.categoryAxis.categoryNames = ["21/10 21:54", "21/10 22:20", "21/10 22:30", "21/10 23:07", "22/10 08:40"]
    c.categoryAxis.labels.fontSize = 7
    c.valueAxis.valueMin, c.valueAxis.valueMax, c.valueAxis.valueStep = 0, 40, 10
    c.valueAxis.labels.fontSize = 7
    cores = [colors.HexColor("#1f4e79"), colors.HexColor("#8faadc"), colors.HexColor("#f4b183"), colors.HexColor("#a9d18e")]
    for i, cor in enumerate(cores):
        c.bars[i].fillColor = cor
        c.bars[i].strokeColor = None
    c.barLabels.fontSize = 6
    c.barLabelFormat = "%d"
    c.barLabels.nudge = 6
    d.add(c)
    leg = ["Visitas", "Visitantes únicos", "Cliques afiliado", "Possíveis compras"]
    x = 45
    for cor, nome in zip(cores, leg):
        from reportlab.graphics.shapes import Rect
        d.add(Rect(x, 5.6 * cm - 14, 8, 8, fillColor=cor, strokeColor=None))
        d.add(String(x + 11, 5.6 * cm - 13, nome, fontSize=7.5))
        x += 105
    return d


def grafico_ritmo():
    d = Drawing(17 * cm, 4 * cm)
    c = HorizontalLineChart()
    c.x, c.y, c.width, c.height = 40, 22, 17 * cm - 70, 4 * cm - 42
    c.data = [[20.8, 12.0, 1.6, 0.42]]
    c.categoryAxis.categoryNames = ["21:54-22:20", "22:20-22:30", "22:30-23:07", "23:07-08:40"]
    c.categoryAxis.labels.fontSize = 7
    c.valueAxis.valueMin, c.valueAxis.valueMax, c.valueAxis.valueStep = 0, 25, 5
    c.valueAxis.labels.fontSize = 7
    c.lines[0].strokeColor = colors.HexColor("#c00000")
    c.lines[0].strokeWidth = 2
    c.lineLabelFormat = "%.1f"
    c.lineLabels.fontSize = 7
    d.add(c)
    d.add(String(45, 4 * cm - 12, "Visitas por hora entre um quadro e outro", fontSize=8, fillColor=AZUL))
    return d


def rodape(canv, doc):
    canv.saveState()
    canv.setFont("Helvetica", 7.5)
    canv.setFillColor(colors.grey)
    canv.drawString(2 * cm, 1.2 * cm, "comprenolink.net · Conversão e Performance do Blog · atualizado em 23/10/2026")
    canv.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canv.restoreState()


s = []
# ================= ATUALIZAÇÃO 23/10/2026 (anúncios no ML + dados novos)
s.append(P("Conversão e Performance do Blog", H1))
s.append(P("Atualização de 23/10/2026 · 1 relatório por dia (21/10, 22/10 e 23/10 09:54) · verificação dos anúncios no "
           "Mercado Livre em 23/10 09:44 e 09:51", SUB))
s.append(Spacer(1, 8))
s.append(kpis([("2", "visitantes REAIS (6 testes excluídos)"), ("6", "visitas reais"), ("4", "cliques reais no ML"),
               ("1", "visita de campanha real (TikTok 01)"), ("20 de 23", "anúncios ativos no ML")]))
s.append(P("A. Anúncios fora do ar no Mercado Livre", H2))
s.append(P("Cada link de afiliado do guia foi aberto na página pública do ML. Ela mostra o número do anúncio "
           "e avisos como “Anúncio pausado”. 3 dos 23 produtos levam a anúncios fora do ar:", TX))
s.append(tabela([
    ["Item", "Nº do anúncio", "Catálogo", "Descrição do anúncio", "Situação", "Aviso do ML", "Cliq."],
    ["1", "MLB7142410630", "MLB47526985", "Fone de Ouvido JBL Tune 720BT Sem Fio Bluetooth 5.3 On-Ear Branco com Microfone",
     "Pausado", "“Anúncio pausado”", "5"],
    ["16", "—", "MLB45887282", "Smartphone Motorola Moto G24 256GB 8GB (4GB RAM + 4GB Boost) Câmera 50MP - Rosa",
     "Removido", "Link leva a perfil vazio: “Este perfil ainda está vazio”", "0"],
    ["18", "MLB6928013958", "MLB72985040", "Kit Capa Moto G56 Transparente Anti Impacto + Película de Vidro 3D",
     "Pausado", "“Anúncio pausado”", "0"],
], [0.9 * cm, 2.9 * cm, 2.6 * cm, 4.5 * cm, 1.9 * cm, 3.1 * cm, 1.1 * cm],
    extra=[("BACKGROUND", (4, 1), (4, 3), VERMELHO)]))
s.append(Spacer(1, 4))
s.append(P("<b>Motivo:</b> o ML não mostra publicamente por que um anúncio foi pausado ou retirado (só o vendedor vê). "
           "Provável: <b>pausado</b> = vendedor pausou ou acabou o estoque; <b>removido</b> = anúncio finalizado/excluído "
           "pelo vendedor ou retirado pelo ML. Os outros 20 estão ativos.", TXP))
s.append(P("B. O que mudou nos dados desde 22/10", H2))
s.append(P("No total foram 93 visitas e 32 cliques, mas 6 dos 8 visitantes eram testes (computadores Windows e "
           "127.0.0.1, o painel local). Eles foram marcados Ignorar = S em 23/10. Sem eles, o público <b>real</b> é de "
           "<b>2 visitantes, 6 visitas, 4 cliques e 1 possível compra</b>, com 83% das visitas de celular. O principal é o "
           "#57bsbc (Android, veio pelo botão da home, 5 visitas, 4 cliques). Surgiu a <b>1ª visita de campanha real</b>: "
           "vídeo TikTok 01 (fones JBL × QCY), ainda sem clique.", TX))
s.append(P("C. Conclusão da performance e pontos de atenção (23/10/2026)", H2))
s.append(caixa("<b>Conclusão:</b> o blog está em aquecimento. Sem os testes, o público real é de 2 visitantes, que "
               "fizeram 4 cliques no ML e 1 possível compra. O rastreio funciona e a divulgação começou (1 visita do "
               "TikTok), mas a amostra é pequena demais e não há vendas importadas, então a conversão real ainda não "
               "pode ser medida. O risco novo é que <b>3 anúncios do guia estão fora do ar</b>, inclusive o produto "
               "“Mais Vendido” e o tema do vídeo que já está trazendo visita. O JBL pausado já recebeu 5 cliques do blog.", AMARELO))
s.append(Spacer(1, 4))
s.append(tabela([
    ["Prioridade", "Ponto de atenção"],
    ["Urgente", "O vídeo TikTok 01 leva ao JBL, cujo anúncio (MLB7142410630) está PAUSADO. Gere um link de afiliado de "
                "um anúncio ativo do catálogo MLB47526985 e troque no item 1."],
    ["Alta", "Troque os links dos itens 16 (Moto G24, catálogo MLB45887282) e 18 (Capinha Moto G56, catálogo MLB72985040)."],
    ["Feito", "6 acessos de teste marcados Ignorar = S. Ao testar de novo, marque o novo código (coluna Sugestão)."],
    ["Média", "Rode o ATUALIZAR_PAINEL.bat 1 vez por dia: ele verifica os 23 anúncios e mostra o que mudou."],
    ["Média", "Exporte as vendas do ML Afiliados para vendas_afiliados; faltam 35 dias para a Black Friday."],
], [2.3 * cm, 14.7 * cm], extra=[("BACKGROUND", (0, 1), (-1, 2), VERMELHO), ("BACKGROUND", (0, 3), (-1, 3), VERDE),
           ("BACKGROUND", (0, 4), (-1, 5), AMARELO)]))
s.append(PageBreak())

# ================= ANÁLISE ORIGINAL DE 22/10/2026
s.append(P("Análise de 22/10/2026", H1))
s.append(P("comprenolink.net/melhores-produtos-mercado-livre-2026/ · avaliação após as correções de 21/10/2026 · "
           "dados de 5 relatórios (21/10 21:54 a 22/10 08:40) e do Painel de Controle de Acesso.xlsx", SUB))
s.append(Spacer(1, 10))
s.append(kpis([("38", "visitas na página"), ("6", "visitantes únicos"), ("12", "cliques em link de afiliado"),
               ("3", "possíveis compras (estimativa)"), ("0", "vendas confirmadas")]))
s.append(Spacer(1, 10))

s.append(P("1. Veredito", H2))
s.append(caixa("<b>As correções funcionaram do ponto de vista técnico</b>: a home agora leva visitas para o guia "
               "(campanhas <i>botao_home</i> registrando), o endereço novo recebe os acessos, os cliques nos links "
               "meli.la estão sendo contados e o painel de possíveis compras está ativo.<br/><br/>"
               "<b>Ainda não é possível medir conversão real.</b> Quase todo o tráfego tem cara de teste (computador "
               "Windows, muitas recargas, horários das correções), nenhuma das 7 campanhas de divulgação configuradas "
               "(TikTok, Instagram, WhatsApp) recebeu visita e o relatório de vendas do ML Afiliados não foi importado. "
               "Os números de hoje medem o <b>funcionamento do rastreio</b>, não o desempenho de vendas.", AMARELO))

s.append(P("2. Evolução quadro a quadro", H2))
s.append(grafico_evolucao())
s.append(tabela([
    ["Nº", "Data/hora", "Visitas", "Únicos", "Vindas de link", "Cliques", "% c/ clique", "Poss. compras", "Visitas/h"],
    ["1", "21/10 21:54", "22", "4", "13 (59%)", "3", "29%", "1", "—"],
    ["2", "21/10 22:20", "31", "5", "16 (52%)", "11", "50%", "3", "20,8"],
    ["3", "21/10 22:30", "33", "5", "16 (48%)", "11", "43%", "3", "12,0"],
    ["4", "21/10 23:07", "34", "6", "17 (50%)", "12", "47%", "3", "1,6"],
    ["5", "22/10 08:40", "38", "6", "17 (45%)", "12", "37%", "3", "0,4"],
], [1.3 * cm, 2.2 * cm, 1.5 * cm, 1.8 * cm, 2.1 * cm, 1.5 * cm, 2.4 * cm, 2.3 * cm, 1.9 * cm]))
s.append(Spacer(1, 6))
s.append(grafico_ritmo())
s.append(P("<b>Leitura:</b> o pico (≈21 visitas/hora) coincide com a sessão de correções e testes. Da noite até 08:40 "
           "o ritmo caiu para 0,4 visita/hora: +4 visitas, <b>nenhum visitante novo e nenhum clique novo</b>. "
           "As 4 visitas da madrugada são todas do mesmo visitante (#196e9e, Edge), que já estava ativo nos testes.", TX))

s.append(P("3. Funil de conversão (último quadro)", H2))
s.append(tabela([
    ["Etapa", "Quantidade", "Taxa", "Comentário"],
    ["Acessos a outras páginas do site (home etc.)", "154", "—", "+8 desde o 1º quadro"],
    ["Visitas no guia", "38", "—", "inclui recargas da mesma pessoa"],
    ["Visitantes únicos no guia", "6", "—", "base real é pequena demais para estatística"],
    ["Visitantes que clicaram em produto", "5 de 6", "83%", "inflado por testes de clique"],
    ["Cliques em link de afiliado", "12", "32% das visitas · 2 por visitante", "75% dos cliques na 'Escolha rápida'"],
    ["Possíveis compras (pontuação ≥ 70)", "3", "25% dos cliques", "os 3 são visitantes de computador Windows"],
    ["Vendas aprovadas / pendentes", "—", "—", "vendas_afiliados está vazia"],
], [5.4 * cm, 2.2 * cm, 3.8 * cm, 5.6 * cm]))
s.append(Spacer(1, 6))
s.append(P("Referência de mercado (aproximada) para blogs de afiliado: 5% a 15% dos visitantes clicam para a loja e "
           "1% a 5% dos cliques viram compra. As taxas atuais (32% a 83%) estão muito acima disso, o que é mais um "
           "sinal de que o tráfego é de teste e não de público.", TXP))

s.append(P("4. Origem do tráfego e desempenho por campanha", H2))
s.append(tabela([
    ["Origem / campanha", "Visitas", "Únicos", "Cliques", "Taxa", "Poss. compras", "Avaliação"],
    ["site · botao_home / botao_rodape", "10", "2", "1", "50%", "—", "link interno"],
    ["site · botao_home / cat_presentes", "3", "1", "1", "50%", "1", "link interno"],
    ["site · botao_home / botao_principal", "3", "1", "2", "100%", "1", "link interno"],
    ["tiktok · teste_instalacao", "1", "1", "1", "100%", "—", "teste de 29/09"],
    ["Direto / desconhecido", "21", "3", "7", "20%", "1", "provável acesso próprio"],
    ["7 campanhas configuradas (TikTok vídeos 01-03, bios TikTok/IG, WhatsApp, TikTok Ads)", "0", "0", "0", "—", "—", "sem divulgação ainda"],
], [6.2 * cm, 1.4 * cm, 1.7 * cm, 1.4 * cm, 1.3 * cm, 2.0 * cm, 3.0 * cm],
    extra=[("BACKGROUND", (0, 6), (-1, 6), VERMELHO)]))
s.append(Spacer(1, 4))
s.append(P("O indicador “Visitas vindas de anúncio/link (45%)” está superestimado: 16 das 17 visitas “de link” "
           "são cliques internos na própria home (utm_source=site). Tráfego de divulgação externa real = 0.", TX))

s.append(P("5. Produtos clicados", H2))
s.append(tabela([
    ["Produto", "Cliques", "Origem"],
    ["“Escolha rápida: o melhor de cada categoria” (tabela #escolha-rapida)", "9", "direto 5 · botao_home 4"],
    ["Smart TV 32\" Philco Roku P32CRA", "1", "direto"],
    ["Fone JBL Tune 720BT Bluetooth 5.3", "1", "direto"],
    ["1. Fone JBL Bluetooth On-Ear", "1", "tiktok teste"],
], [10.5 * cm, 1.8 * cm, 4.7 * cm]))
s.append(Spacer(1, 4))
s.append(P("A tabela “Escolha rápida” concentra 75% dos cliques — é o bloco que mais atrai atenção. Porém o rastreio "
           "grava o título da seção, não o produto, então não se sabe <b>qual</b> item foi clicado.", TX))

s.append(KeepTogether([P("6. Perfil dos visitantes", H2), tabela([
    ["ID", "Período", "Origem", "Aparelho", "Visitas", "Cliques", "Intenção", "Diagnóstico"],
    ["#idawt7", "21/10 17:44 → 22:08*", "direto", "Windows · Chrome", "19", "3", "Alta", "provável dono / teste"],
    ["#196e9e", "21/10 22:00 → 23:23*", "direto", "Windows · Edge", "13", "5", "Alta", "provável teste"],
    ["#s5vfvo", "21/10 17:48 → 20:45*", "botao_home", "Windows · Chrome", "3", "2", "Alta", "provável teste"],
    ["#2oo3cg", "21/10 17:14*", "direto", "Windows · Chrome", "1", "0", "—", "indefinido"],
    ["#57bsbc", "21/10 22:34*", "botao_home", "Android · Chrome", "1", "1", "Média", "<b>único candidato a visitante real</b>"],
    ["#acao01", "29/09", "tiktok teste", "Android · Chrome", "1", "1", "Média", "teste de instalação"],
], [1.6 * cm, 3.0 * cm, 1.9 * cm, 2.5 * cm, 1.3 * cm, 1.3 * cm, 1.4 * cm, 4.0 * cm],
    extra=[("BACKGROUND", (0, 5), (-1, 5), VERDE)])]))
s.append(P("* horário convertido para Brasília (o relatório mostra os eventos em UTC, 3 h à frente).", TXP))
s.append(P("95% das visitas vêm de computador Windows. Em tráfego real vindo de TikTok/Instagram/WhatsApp o "
           "esperado é o oposto: 80% a 90% celular. As 3 “possíveis compras” são desses computadores e devem ser "
           "tratadas como falso positivo até prova em contrário.", TX))

s.append(P("7. Problemas de medição encontrados", H2))
s.append(tabela([
    ["#", "Problema", "Efeito no relatório", "Correção sugerida"],
    ["1", "Acessos próprios (dono e testes) entram na contagem", "infla visitas, cliques e possíveis compras",
     "marcar o navegador do dono (ex.: ?nao_contar=1 grava cookie) e ignorar no relatório"],
    ["2", "Links internos da home usam UTM (utm_source=site)", "aparecem como “Divulgação”; % de anúncio falso",
     "classificar source=site como “Interno” e separar de divulgação externa"],
    ["3", "Horários em UTC", "“Visitas por dia/horário” deslocados 3 h; atividade de 21/10 aparece em 22/10",
     "converter para America/Sao_Paulo no relatório"],
    ["4", "Cliques da Escolha rápida sem nome do produto", "não dá para saber qual item converte",
     "data-produto em cada link da tabela"],
    ["5", "Vendas não importadas", "conversão real desconhecida",
     "exportar vendas/ganhos do painel ML Afiliados para D:\\mercado_livre\\vendas_afiliados"],
    ["6", "Planilha: coluna “Intervalo” mostra número serial (46316,91…) e o quadro 5 está como texto",
     "gráfico de evolução e intervalos difíceis de ler", "formatar como data/hora dd/mm hh:mm"],
    ["7", "“Visitas que clicaram em produto” usa visitas (com recargas)", "taxa cai quando a mesma pessoa recarrega",
     "usar visitantes que clicaram ÷ visitantes únicos"],
], [0.6 * cm, 4.8 * cm, 5.2 * cm, 6.4 * cm]))

s.append(P("8. Plano de ação para medir conversão de verdade", H2))
acoes = [
    ["Prioridade", "Ação", "Meta"],
    ["Hoje", "Parar de clicar nos próprios links de afiliado (cliques/compras próprias podem violar as regras do "
             "programa e sujam os dados) e ativar a exclusão do acesso próprio", "base limpa"],
    ["Hoje", "Publicar os 3 vídeos TikTok prontos com os links UTM já gerados (fones, Echo Dot, Smart TV) e "
             "colocar o link na bio do TikTok e Instagram", "primeiras visitas externas"],
    ["Esta semana", "Divulgar em 2-3 grupos de WhatsApp/Telegram com o link “whatsapp/grupos”", "50+ visitantes reais"],
    ["Esta semana", "Corrigir os itens 2, 3 e 4 da seção 7 no script do relatório", "relatório confiável"],
    ["Em 7 dias", "Importar o relatório de vendas do ML Afiliados e comparar cliques do ML × cliques do blog",
     "1ª taxa de conversão real"],
    ["Até 27/11", "Preparar página/seção Black Friday com os produtos mais clicados", "pico de vendas"],
]
s.append(tabela(acoes, [2.3 * cm, 11.2 * cm, 3.5 * cm]))
s.append(Spacer(1, 6))
s.append(P("<b>Estimativa de volume necessário:</b> com 10% dos visitantes clicando e 2% a 3% dos cliques comprando, "
           "a 1ª venda tende a aparecer entre 170 e 500 visitantes reais. Com 6 visitantes (quase todos de teste) "
           "a ausência de vendas é esperada e não indica falha do blog.", TX))

s.append(PageBreak())
s.append(P("9. Painel de controle dinâmico (Excel)", H2))
s.append(P("A planilha <b>Painel de  Controle de Acesso.xlsx</b> foi refeita como painel de conversão e performance. "
           "Ela é remontada a partir de <b>todos</b> os relatorio_acessos_anuncios_*.html da pasta e das vendas exportadas do "
           "ML Afiliados, com fórmulas, conclusão automática, pontos de atenção e 10 gráficos.", TX))
s.append(tabela([
    ["Aba", "Conteúdo"],
    ["Painel", "16 KPIs, conclusão automática, pontos de atenção automáticos, análise do especialista (editável) e 10 gráficos"],
    ["Quadros", "1 linha por relatório: visitas, cliques, Δ, horas entre relatórios, visitas/hora, cliques por visitante, Observação"],
    ["Campanhas", "visitas, cliques e taxa por campanha + classificação automática (Externo, Interno, Teste, Direto)"],
    ["Produtos / Visitantes", "produtos mais clicados; visitantes com horário convertido para Brasília, sugestão de teste e coluna Ignorar"],
    ["Diario / Perfil", "visitas por dia com média móvel 7 dias; dispositivo, sistema, canal e horário"],
    ["Vendas", "importação automática de CSV/Excel do ML Afiliados + linhas digitadas à mão (Fonte = manual)"],
    ["Metas", "fuso, meta de clique, meta de conversão, comissão média, meta semanal, Black Friday, % celular esperado"],
], [3.5 * cm, 13.5 * cm]))
s.append(Spacer(1, 6))
s.append(P("<b>Como atualizar:</b> salve o novo relatório HTML em 99_LOG_RELATORIOS (e as vendas em vendas_afiliados), feche a "
           "planilha e dê dois cliques em <b>ATUALIZAR_PAINEL.bat</b>. O .bat monta a planilha, recalcula no Excel, exporta o PDF "
           "do painel (Painel_conversao_performance_AAAA-MM-DD_HHhMM.pdf) e abre a planilha. Cada versão anterior vai para "
           "_backup_painel (últimas 15).", TX))

s.append(P("10. Teste de funcionalidade (22/10/2026)", H2))
s.append(tabela([
    ["#", "Teste", "Resultado"],
    ["1", "Leitura dos 5 relatórios HTML e montagem da planilha", "OK: 5 quadros, valores iguais aos relatórios"],
    ["2", "Relatório duplicado (mesma data/hora com outro nome)", "OK: ignorado, continua com 5 quadros"],
    ["3", "Recalcular no Excel (todas as fórmulas)", "OK: 0 fórmulas com erro"],
    ["4", "Importar CSV de vendas (separador ;, R$ 999,90, datas dd/mm/aaaa)", "OK: 2 vendas, 1 aprovada + 1 pendente"],
    ["5", "Arquivo de vendas com colunas desconhecidas", "OK: ignorado com aviso na aba Vendas e no .bat"],
    ["6", "Preservar edições: Ignorar = S, Observação, venda manual, meta, análise", "OK: tudo mantido após atualizar"],
    ["7", "Visitantes reais após marcar 5 testes", "OK: 6 → 1 visitante real; KPIs e funil recalculados"],
    ["8", "Conclusão e alertas mudam com os dados", "OK: passa de 'RASTREIO OK, SEM PÚBLICO' para 'RESULTADO' com vendas"],
    ["9", "Horário UTC → Brasília (-3 h)", "OK: ex.: 22/10 01:08 UTC = 21/10 22:08"],
    ["10", "ATUALIZAR_PAINEL.bat de ponta a ponta", "OK: planilha + PDF do painel gerados, backup criado"],
    ["11", "Bug encontrado e corrigido", "'Data da venda' era lida como valor; erro de congelamento na aba Metas impedia o Excel de abrir"],
], [0.8 * cm, 8.4 * cm, 7.8 * cm]))
s.append(P("Os testes 4 a 8 foram feitos numa cópia da pasta com vendas fictícias; a planilha real não recebeu dados de teste.", TXP))

s.append(PageBreak())
s.append(P("11. Conclusão da performance e pontos de atenção", H2))
s.append(tabela([
    ["Prioridade", "Ponto de atenção"],
    ["Alta", "Tráfego externo real = 0: nenhuma das 7 campanhas (TikTok, Instagram, WhatsApp) recebeu visita."],
    ["Alta", "95% das visitas são de computador Windows: os números atuais são de testes. Marque Ignorar = S na aba Visitantes."],
    ["Alta", "Sem vendas importadas: a conversão real não pode ser medida até exportar o relatório do ML Afiliados."],
    ["Média", "75% dos cliques vêm da 'Escolha rápida' sem nome do produto: não se sabe qual item atrai."],
    ["Média", "Links internos da home contam como 'Divulgação' no relatório HTML (o painel já corrige isso)."],
    ["Média", "Faltam 36 dias para a Black Friday (27/11): é preciso gerar tráfego antes para ter histórico."],
], [2.3 * cm, 14.7 * cm], extra=[("BACKGROUND", (0, 1), (-1, 3), VERMELHO), ("BACKGROUND", (0, 4), (-1, 6), AMARELO)]))
s.append(Spacer(1, 8))
s.append(caixa("O blog está <b>pronto para receber tráfego</b>: estrutura corrigida, links de afiliado corretos e "
               "rastreio funcionando de ponta a ponta. O gargalo agora não é a página, é a <b>falta de visitantes "
               "reais</b>. Próximo marco de avaliação: repetir este relatório após 7 dias de divulgação, com o acesso "
               "próprio excluído e as vendas do ML Afiliados importadas.", VERDE))

doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.6 * cm,
                        bottomMargin=1.8 * cm, title="Conversão e Performance do Blog",
                        author="comprenolink.net", subject="Avaliação após correções de 21/10/2026")
doc.build(s, onFirstPage=rodape, onLaterPages=rodape)
print("OK", SAIDA)
