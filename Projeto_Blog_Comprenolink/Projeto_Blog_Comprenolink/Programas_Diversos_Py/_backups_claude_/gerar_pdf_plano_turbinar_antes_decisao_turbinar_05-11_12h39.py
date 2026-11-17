# -*- coding: utf-8 -*-
"""PDF do planejamento de anúncio pago (Turbinar) do Instagram @compre.no.link – Black Friday e Natal 2026.
Rodar:  python -X utf8 gerar_pdf_plano_turbinar.py   → Plano_Turbinar_Instagram_2026.pdf (nesta pasta)
Valores e datas ficam nas listas abaixo: mudou o plano, edite aqui e rode de novo.
"""
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (Image, KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

PASTA = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(PASTA, "Plano_Turbinar_Instagram_2026.pdf")
DATA_DOC = "27/10/2026"

F = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Arial", os.path.join(F, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-B", os.path.join(F, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-I", os.path.join(F, "ariali.ttf")))
pdfmetrics.registerFontFamily("Arial", normal="Arial", bold="Arial-B", italic="Arial-I", boldItalic="Arial-B")

ESCURO = colors.HexColor("#111827")
AMARELO = colors.HexColor("#FFD54A")
CINZA = colors.HexColor("#6B7280")
CLARO = colors.HexColor("#F3F4F6")
VERDE, VERDE_C = colors.HexColor("#15803D"), colors.HexColor("#DCFCE7")
LARANJA, LARANJA_C = colors.HexColor("#B45309"), colors.HexColor("#FEF3C7")
VERMELHO, VERMELHO_C = colors.HexColor("#B91C1C"), colors.HexColor("#FEE2E2")
AZUL_C = colors.HexColor("#E0F2FE")

S = {
    "capa_t": ParagraphStyle("capa_t", fontName="Arial-B", fontSize=26, leading=32, textColor=ESCURO, alignment=TA_CENTER),
    "capa_s": ParagraphStyle("capa_s", fontName="Arial", fontSize=13, leading=18, textColor=CINZA, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="Arial-B", fontSize=17, leading=22, textColor=ESCURO, spaceBefore=4, spaceAfter=8),
    "h2": ParagraphStyle("h2", fontName="Arial-B", fontSize=12.5, leading=16, textColor=ESCURO, spaceBefore=10, spaceAfter=5),
    "p": ParagraphStyle("p", fontName="Arial", fontSize=10.2, leading=14.5, textColor=ESCURO, spaceAfter=5),
    "pq": ParagraphStyle("pq", fontName="Arial", fontSize=8.8, leading=12, textColor=CINZA, spaceAfter=4),
    "cel": ParagraphStyle("cel", fontName="Arial", fontSize=9.2, leading=12.2, textColor=ESCURO),
    "celb": ParagraphStyle("celb", fontName="Arial-B", fontSize=9.2, leading=12.2, textColor=ESCURO),
    "cab": ParagraphStyle("cab", fontName="Arial-B", fontSize=9.2, leading=12, textColor=colors.white),
    "big": ParagraphStyle("big", fontName="Arial-B", fontSize=20, leading=24, textColor=ESCURO, alignment=TA_CENTER),
    "bigl": ParagraphStyle("bigl", fontName="Arial", fontSize=9, leading=12, textColor=CINZA, alignment=TA_CENTER),
}
LARG = A4[0] - 3.6 * cm

# ---------------------------------------------------------------- dados do plano
COMISSAO_MEDIA = 9.05  # R$ 172 de ganho / 19 vendas (ML Afiliados, 180 dias até 27/10/2026)
FASES = [
    # nome, período, dias, R$/dia, post, condição
    ("Fase 1 – Teste", "seg 16/11 a qua 18/11/2026", 3, 10, "O post com melhor resultado gratuito de 02 a 15/11",
     "Só começa se os termos do ML Afiliados permitirem anúncio pago"),
    ("Fase 2 – Black Friday", "sáb 21/11 a sex 27/11/2026", 7, 15, "Top 10 da Black Friday (post ou Reels)",
     "Só se a Fase 1 ficar no VERDE"),
    ("Fase 3 – Natal", "sáb 05/12 a seg 14/12/2026", 10, 10, "Presentes de Natal – Top 10",
     "Só se a Black Friday se pagar (vendas ≥ gasto)"),
]


def brl(v):
    return ("R$ %.2f" % v).replace(".", ",")


def tabela(linhas, larguras, cab=True, zebra=True, extra=None, cab_cor=ESCURO):
    dados = []
    for i, l in enumerate(linhas):
        estilo = S["cab"] if (cab and i == 0) else S["cel"]
        dados.append([c if not isinstance(c, str) else Paragraph(c, estilo) for c in l])
    t = Table(dados, colWidths=[LARG * w for w in larguras], repeatRows=1 if cab else 0)
    st = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
          ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
          ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6)]
    if cab:
        st.append(("BACKGROUND", (0, 0), (-1, 0), cab_cor))
    if zebra:
        for r in range(1 if cab else 0, len(dados)):
            if r % 2 == 0:
                st.append(("BACKGROUND", (0, r), (-1, r), CLARO))
    t.setStyle(TableStyle(st + (extra or [])))
    return t


def caixa(texto, fundo=AZUL_C, borda=colors.HexColor("#0284C7")):
    t = Table([[Paragraph(texto, S["p"])]], colWidths=[LARG])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fundo), ("BOX", (0, 0), (-1, -1), 1, borda),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def cartoes(itens):
    """Linha de 'cartões' com número grande + legenda."""
    cel = [[Paragraph(v, S["big"]), Paragraph(l, S["bigl"])] for v, l in itens]
    t = Table([[Table([[a], [b]], colWidths=[LARG / len(itens) - 8]) for a, b in cel]],
              colWidths=[LARG / len(itens)] * len(itens))
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), CLARO), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")),
                           ("LINEAFTER", (0, 0), (-2, -1), 0.5, colors.white), ("TOPPADDING", (0, 0), (-1, -1), 8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def rodape(c, doc):
    c.saveState()
    c.setFillColor(AMARELO)
    c.rect(0, A4[1] - 0.45 * cm, A4[0], 0.45 * cm, fill=1, stroke=0)
    c.setFont("Arial", 8)
    c.setFillColor(CINZA)
    c.drawString(1.8 * cm, 1.1 * cm, f"Plano Turbinar Instagram @compre.no.link – Black Friday e Natal 2026  •  {DATA_DOC}")
    c.drawRightString(A4[0] - 1.8 * cm, 1.1 * cm, f"Página {doc.page}")
    c.restoreState()


def capa(c, doc):
    c.saveState()
    c.setFillColor(ESCURO)
    c.rect(0, A4[1] - 7 * cm, A4[0], 7 * cm, fill=1, stroke=0)
    c.setFillColor(AMARELO)
    c.rect(0, A4[1] - 7.25 * cm, A4[0], 0.25 * cm, fill=1, stroke=0)
    c.setFont("Arial-B", 30)
    c.drawCentredString(A4[0] / 2, A4[1] - 3.3 * cm, "compre no link")
    c.setFillColor(colors.white)
    c.setFont("Arial", 12)
    c.drawCentredString(A4[0] / 2, A4[1] - 4.3 * cm, "comprenolink.net  •  @compre.no.link  •  achados do Mercado Livre")
    c.restoreState()
    rodape(c, doc)


def montar():
    st = [Spacer(1, 6.3 * cm),
          Paragraph("Planejamento de Anúncio Pago<br/>no Instagram (Turbinar)", S["capa_t"]), Spacer(1, 10),
          Paragraph("Black Friday e Natal 2026 – documento para reunião de sócios", S["capa_s"]), Spacer(1, 26)]
    tot = sum(d * v for _, _, d, v, _, _ in FASES)
    st.append(cartoes([("R$ 30", "gasto mínimo<br/>(só o teste)"), ("R$ 135", "teste +<br/>Black Friday"),
                       (brl(tot).replace(",00", ""), "plano completo<br/>(valor máximo)"), ("16/11", "início do 1º<br/>anúncio")]))
    st += [Spacer(1, 22), tabela([
        ["Item", "Informação"],
        ["Empresa / perfil", "Blog comprenolink.net (afiliado Mercado Livre) – Instagram @compre.no.link"],
        ["Assunto", "Quanto investir, quando e como medir o anúncio pago (botão <b>Turbinar</b>) do Instagram"],
        ["Período do plano", "02/11/2026 a 14/12/2026 (preparação, teste, Black Friday e Natal)"],
        ["Data do documento", DATA_DOC],
        ["Decisão pedida aos sócios", "Aprovar (ou não) o <b>valor máximo</b> e quem paga – ver a página final de aprovação"],
    ], [0.3, 0.7]), Spacer(1, 18),
        caixa("<b>Em uma frase:</b> começamos com um <b>teste de R$ 30</b> em 16/11, medimos o custo de cada visita e "
              "<b>só investimos mais</b> (Black Friday e Natal) se os números ficarem no verde. O gasto máximo é de "
              f"<b>{brl(tot)}</b> e pode parar a qualquer momento."),
        PageBreak()]

    # ---------------- quadro-resumo (imagem gerada por gerar_quadro_resumo.py)
    png = os.path.join(PASTA, "Quadro_Resumo_Turbinar_2026.png")
    if os.path.exists(png):
        from PIL import Image as PILImage
        with PILImage.open(png) as im:
            prop = im.height / im.width
        st += [Paragraph("Quadro-resumo: quando fazer e quanto custa", S["h1"]),
               Paragraph("Cada faixa colorida é uma opção de investimento. As barras mostram os dias com gasto; os pontos "
                         "embaixo são as datas de preparação e avaliação (sem gasto).", S["p"]),
               Image(png, width=LARG, height=LARG * prop), Spacer(1, 10),
               tabela([
                   ["Opção", "Mês / dias com gasto", "Total", "Decide em"],
                   ["<b>1. Gasto mínimo</b>", "Novembro: 16, 17 e 18", "<b>R$ 30,00</b>", "19/11 (avaliação 1)"],
                   ["<b>2. Teste + Black Friday</b>", "Novembro: 16 a 18 + 21 a 27", "<b>R$ 135,00</b>", "30/11 (avaliação 2)"],
                   ["<b>3. Plano completo</b>", "Novembro: 16 a 18 + 21 a 27 • Dezembro: 05 a 14", f"<b>{brl(tot)}</b>", "21/12 (relatório final)"],
               ], [0.27, 0.37, 0.14, 0.22],
                   extra=[("BACKGROUND", (0, 1), (-1, 1), VERDE_C), ("BACKGROUND", (0, 2), (-1, 2), LARANJA_C),
                          ("BACKGROUND", (0, 3), (-1, 3), colors.HexColor("#EDE9FE"))]),
               PageBreak()]

    # ---------------- 1. resumo executivo
    st += [Paragraph("1. Resumo para a reunião", S["h1"]),
           Paragraph("O Instagram do blog foi configurado em 27/10/2026 (perfil profissional, bio, links, post de "
                     "boas-vindas fixado e respostas automáticas do Direct). A partir de 02/11 entram os posts "
                     "diários da Black Friday. Como o perfil é <b>novo</b>, o alcance gratuito no início é pequeno. "
                     "O <b>Turbinar</b> é o anúncio pago do próprio Instagram: pagamos um valor por dia e ele mostra "
                     "o post para pessoas que ainda não seguem o perfil.", S["p"]),
           tabela([
               ["Pergunta", "Resposta curta"],
               ["O que é?", "Pagar para o Instagram mostrar um post nosso a mais pessoas (fora dos seguidores)."],
               ["Para quê?", "Levar visitas ao blog na época que mais vende: Black Friday (até 27/11) e Natal."],
               ["Quanto?", f"De <b>R$ 30</b> (só teste) até <b>{brl(tot)}</b> (plano completo). Nunca passa disso sem nova reunião."],
               ["Quando?", "Teste 16 a 18/11 • Black Friday 21 a 27/11 • Natal 05 a 14/12."],
               ["Como saber se valeu?", "Custo por clique (Instagram), visitas pagas (painel do blog) e vendas (ML Afiliados)."],
               ["Risco principal", "Gastar e não vender. Por isso o plano tem <b>pontos de parada</b> após cada fase."],
               ["Quem paga?", "Um dos sócios, pelo cartão ou Pix na conta de anúncios da Meta (definir na aprovação)."],
           ], [0.26, 0.74]),
           Paragraph("2. Onde estamos hoje (números reais)", S["h2"]),
           tabela([
               ["Indicador", "Valor", "Fonte / observação"],
               ["Produtos no blog", "160", "Guia comprenolink.net, 8 categorias"],
               ["Seguidores no Instagram", "2", "Perfil criado/configurado em 27/10/2026"],
               ["Vendas registradas", "19", "ML Afiliados, últimos 180 dias"],
               ["Ganho (comissão)", "R$ 172,00", "ML Afiliados, últimos 180 dias"],
               ["Comissão média por venda", brl(COMISSAO_MEDIA), "R$ 172 ÷ 19 vendas (base para as contas deste plano)"],
               ["Cliques no link de afiliado", "116", "ML Afiliados, últimos 180 dias"],
           ], [0.34, 0.18, 0.48]),
           Paragraph("Valores do ML Afiliados digitados em 27/10/2026. A comissão varia por produto: é uma média para "
                     "estimar, não uma garantia.", S["pq"]),
           PageBreak()]

    # ---------------- 3. como funciona
    st += [Paragraph("3. Como funciona (do anúncio até a comissão)", S["h1"]),
           tabela([
               ["Passo", "O que acontece", "Onde"],
               ["1", "A pessoa vê o post turbinado (marcado como \"Patrocinado\")", "Instagram"],
               ["2", "Toca em <b>Visitar site</b> → abre a página da Black Friday ou do Natal", "Instagram → blog"],
               ["3", "Vê os produtos, detalhes e \"Ideal para\"", "comprenolink.net"],
               ["4", "Toca em \"Ver no Mercado Livre\" (nosso link de afiliado)", "blog → Mercado Livre"],
               ["5", "Compra e paga no Mercado Livre", "Mercado Livre"],
               ["6", "O Mercado Livre paga a comissão ao afiliado", "Painel ML Afiliados"],
           ], [0.1, 0.62, 0.28]),
           Spacer(1, 6),
           caixa("<b>Importante:</b> não vendemos, não entregamos e não recebemos dinheiro do cliente. O anúncio "
                 "só serve para <b>levar visitas</b>. A venda e a entrega são do Mercado Livre."),
           Paragraph("Como o dinheiro é gasto", S["h2"]),
           tabela([
               ["Configuração no Turbinar", "O que escolher", "Por quê"],
               ["Objetivo", "<b>Mais visitas ao site</b>", "Queremos cliques no blog, não curtidas"],
               ["Destino (link)", "Página da campanha com rastreio <b>utm_medium=pago</b>", "Separar visita paga da gratuita no painel"],
               ["Público", "Brasil, 25 a 55 anos, interesses: compras online, ofertas, Mercado Livre, tecnologia", "Quem já compra pela internet"],
               ["Orçamento", "Valor por dia + número de dias (tabela da seção 5)", "O Instagram nunca gasta mais que o total escolhido"],
               ["Pagamento", "Cartão de crédito ou Pix na conta de anúncios Meta", "Cobrança automática conforme o gasto"],
           ], [0.24, 0.44, 0.32]),
           Paragraph("Links que vão no anúncio (com rastreio)", S["h2"]),
           tabela([
               ["Fase", "Link do botão \"Visitar site\""],
               ["Teste", "comprenolink.net/black-friday/?utm_source=instagram&amp;utm_medium=pago&amp;utm_campaign=black_friday&amp;utm_content=teste"],
               ["Black Friday", "comprenolink.net/black-friday/?utm_source=instagram&amp;utm_medium=pago&amp;utm_campaign=black_friday&amp;utm_content=top10"],
               ["Natal", "comprenolink.net/presentes-de-natal/?utm_source=instagram&amp;utm_medium=pago&amp;utm_campaign=natal&amp;utm_content=top10"],
           ], [0.18, 0.82]),
           PageBreak()]

    # ---------------- 4. cronograma
    st += [Paragraph("4. Cronograma completo (datas e responsáveis)", S["h1"]),
           Paragraph("Cores: <font color='#15803D'><b>verde</b></font> = gasto de dinheiro • cinza = preparação/avaliação, sem gasto.", S["pq"])]
    crono = [
        ["Data", "Etapa", "O que fazer", "Responsável", "Gasto"],
        ["até 05/11 (qui)", "Preparação", "Ler os termos do ML Afiliados: anúncio pago é permitido? Pode usar o nome \"Mercado Livre\"?", "Sócio", "R$ 0"],
        ["02/11 a 15/11", "Preparação", "Postar todo dia do calendário (conteúdo gratuito) para o perfil ter o que mostrar", "Sócio + Claude", "R$ 0"],
        ["até 15/11 (dom)", "Preparação", "Criar a conta de anúncios Meta e cadastrar cartão/Pix", "Sócio (pagador)", "R$ 0"],
        ["15/11 (dom)", "Escolha", "Escolher o post com mais salvamentos/comentários para o teste", "Claude analisa, sócios decidem", "R$ 0"],
        ["16/11 a 18/11", "Fase 1 – Teste", "Turbinar 3 dias a R$ 10/dia", "Sócio (pagador)", "R$ 30"],
        ["19/11 (qui)", "Avaliação 1", "Comparar resultados com o semáforo (seção 6) e decidir", "Sócios + Claude", "R$ 0"],
        ["21/11 a 27/11", "Fase 2 – Black Friday", "Turbinar 7 dias a R$ 15/dia (se o teste deu verde)", "Sócio (pagador)", "R$ 105"],
        ["30/11 (seg)", "Avaliação 2", "Vendas da Black Friday ≥ gasto? Decide o Natal", "Sócios + Claude", "R$ 0"],
        ["05/12 a 14/12", "Fase 3 – Natal", "Turbinar 10 dias a R$ 10/dia (se a BF se pagou)", "Sócio (pagador)", "R$ 100"],
        ["até 21/12 (seg)", "Fechamento", "Relatório final: gasto x vendas x comissão; lição para 2027", "Claude prepara, sócios analisam", "R$ 0"],
    ]
    verdes = [i for i, l in enumerate(crono) if l[4] not in ("Gasto", "R$ 0")]
    st.append(tabela(crono, [0.15, 0.15, 0.42, 0.17, 0.11], zebra=False,
                     extra=[("BACKGROUND", (0, r), (-1, r), VERDE_C) for r in verdes] +
                           [("BACKGROUND", (0, r), (-1, r), CLARO) for r in range(1, len(crono)) if r not in verdes]))
    st += [Spacer(1, 8), caixa("<b>Por que não turbinar já em 02/11?</b> Um perfil com poucos posts desperdiça o dinheiro: "
                                "a pessoa visita, vê pouco conteúdo e vai embora. As duas primeiras semanas gratuitas "
                                "também mostram qual post o público prefere – esse é o que vale a pena turbinar.",
                                LARANJA_C, LARANJA),
           PageBreak()]

    # ---------------- 5. orçamento
    linhas = [["Fase", "Período", "Dias", "Valor por dia", "Total da fase", "Vendas para empatar*"]]
    acum = 0
    for nome, per, d, v, _, _ in FASES:
        acum += d * v
        linhas.append([f"<b>{nome}</b>", per, str(d), brl(v), f"<b>{brl(d * v)}</b>", f"≈ {round(d * v / COMISSAO_MEDIA + 0.4999)}"])
    linhas.append(["<b>TOTAL MÁXIMO</b>", "16/11 a 14/12/2026", str(sum(f[2] for f in FASES)), "–", f"<b>{brl(acum)}</b>",
                   f"<b>≈ {round(acum / COMISSAO_MEDIA + 0.4999)}</b>"])
    st += [Paragraph("5. Orçamento", S["h1"]),
           tabela(linhas, [0.22, 0.24, 0.07, 0.13, 0.14, 0.2],
                  extra=[("BACKGROUND", (0, len(linhas) - 1), (-1, len(linhas) - 1), AMARELO)]),
           Paragraph(f"* Vendas para empatar = total da fase ÷ comissão média de {brl(COMISSAO_MEDIA)}, arredondado para cima.", S["pq"]),
           Paragraph("Cenários de gasto (o que pode acontecer)", S["h2"]),
           tabela([
               ["Cenário", "O que aconteceu", "Gasto total", "Vendas para empatar"],
               ["A – Parar no teste", "Teste ficou no vermelho: paramos e seguimos só no gratuito", "<b>R$ 30,00</b>", "≈ 4"],
               ["B – Teste + Black Friday", "Teste verde, mas a Black Friday não se pagou: não fazemos o Natal", "<b>R$ 135,00</b>", "≈ 15"],
               ["C – Plano completo", "Tudo no verde: fazemos as 3 fases", f"<b>{brl(acum)}</b>", f"≈ {round(acum / COMISSAO_MEDIA + 0.4999)}"],
           ], [0.24, 0.44, 0.14, 0.18],
               extra=[("BACKGROUND", (0, 1), (-1, 1), VERDE_C), ("BACKGROUND", (0, 2), (-1, 2), LARANJA_C),
                      ("BACKGROUND", (0, 3), (-1, 3), AZUL_C)]),
           Paragraph("Estimativa de visitas (para ter uma ideia)", S["h2"]),
           tabela([
               ["Fase", "Gasto", "Se cada clique custar R$ 0,30", "Se custar R$ 0,50", "Se custar R$ 1,00"],
               ["Teste", "R$ 30", "≈ 100 visitas", "≈ 60 visitas", "≈ 30 visitas"],
               ["Black Friday", "R$ 105", "≈ 350 visitas", "≈ 210 visitas", "≈ 105 visitas"],
               ["Natal", "R$ 100", "≈ 333 visitas", "≈ 200 visitas", "≈ 100 visitas"],
           ], [0.2, 0.14, 0.24, 0.21, 0.21]),
           Paragraph("Estimativas matemáticas. O custo real por clique só é conhecido depois do teste – é exatamente "
                     "para isso que serve a Fase 1.", S["pq"]),
           PageBreak()]

    # ---------------- 6. decisão
    st += [Paragraph("6. Como decidir: o semáforo", S["h1"]),
           Paragraph("Depois de cada fase olhamos 3 números. A regra abaixo evita decidir no \"achismo\".", S["p"]),
           tabela([
               ["Sinal", "Custo por clique (Instagram)", "Visitas pagas no painel do blog", "Decisão"],
               ["VERDE", "até R$ 0,50", "aparecem visitas com utm_medium=pago e cliques no Mercado Livre", "<b>Segue para a próxima fase</b>"],
               ["AMARELO", "de R$ 0,50 a R$ 1,00", "poucas visitas ou quase nenhum clique no Mercado Livre", "<b>Troca o post ou o público</b> e testa mais 2 dias (R$ 20)"],
               ["VERMELHO", "acima de R$ 1,00", "nenhum clique no Mercado Livre", "<b>Para</b> e fica só no gratuito"],
           ], [0.13, 0.22, 0.38, 0.27],
               extra=[("BACKGROUND", (0, 1), (-1, 1), VERDE_C), ("TEXTCOLOR", (0, 1), (0, 1), VERDE),
                      ("BACKGROUND", (0, 2), (-1, 2), LARANJA_C), ("BACKGROUND", (0, 3), (-1, 3), VERMELHO_C)]),
           Paragraph("Regra extra para o Natal", S["h2"]),
           tabela([
               ["Resultado da Black Friday", "Decisão para o Natal"],
               ["Comissão das vendas da BF <b>maior ou igual</b> ao gasto (R$ 105)", "Fazer a Fase 3 (R$ 100)"],
               ["Comissão menor que o gasto, mas custo por clique no verde", "Fazer o Natal pela metade: 5 dias (R$ 50)"],
               ["Comissão muito menor e cliques no amarelo/vermelho", "Não fazer o Natal pago"],
           ], [0.6, 0.4]),
           Paragraph("7. Onde ver cada número", S["h1"]),
           tabela([
               ["Número", "Onde ver", "Quem olha"],
               ["Alcance, cliques e custo por clique", "Instagram → post turbinado → <b>Ver insights</b> / Central de anúncios", "Sócio pagador (print para o Claude)"],
               ["Visitas pagas no blog", "Painel do blog (ATUALIZAR_PAINEL.bat) – linhas com utm_medium=pago", "Claude"],
               ["Vendas e comissão", "Painel <b>ML Afiliados</b> (exportar CSV para a pasta vendas_afiliados)", "Sócio + Claude"],
               ["Gasto real", "Conta de anúncios Meta → Cobrança", "Sócio pagador"],
           ], [0.28, 0.48, 0.24]),
           PageBreak()]

    # ---------------- 8. riscos
    st += [Paragraph("8. Riscos e cuidados", S["h1"]),
           tabela([
               ["Risco", "Impacto", "Como evitamos"],
               ["Termos do ML Afiliados proibirem anúncio pago ou o uso da marca", "Conta de afiliado suspensa", "Ler os termos ANTES (até 05/11). Se proibir, não turbinar."],
               ["Gastar e não vender", "Prejuízo", "Teste pequeno, semáforo e parada após cada fase"],
               ["Anúncio recusado pela Meta", "Atraso", "Texto sem preço, sem \"menor preço\", sem promessas; aviso de afiliado"],
               ["Gasto maior que o combinado", "Prejuízo", "Orçamento total fixo no Turbinar; o Instagram não passa do valor escolhido"],
               ["Clique cai em página errada", "Visita perdida", "Usar só os links da seção 3; o Claude confere antes"],
               ["Preço do produto mudar no Mercado Livre", "Cliente frustrado", "Nunca colocar preço no anúncio (\"confira o valor do dia\")"],
           ], [0.36, 0.18, 0.46]),
           Paragraph("Regras fixas do texto do anúncio", S["h2"]),
           tabela([
               ["Pode", "Não pode"],
               ["\"Os mais vendidos e bem avaliados do Mercado Livre\"", "Preço, \"menor preço\", \"melhor preço\""],
               ["\"Confira o valor do dia no Mercado Livre\"", "Promessas de saúde ou estética"],
               ["\"Link de afiliado: posso ganhar comissão, sem custo extra para você\"", "Dizer que somos o Mercado Livre ou loja oficial"],
           ], [0.5, 0.5], extra=[("BACKGROUND", (0, 0), (0, 0), VERDE), ("BACKGROUND", (1, 0), (1, 0), VERMELHO)]),
           Paragraph("9. Glossário rápido", S["h1"]),
           tabela([
               ["Termo", "O que significa"],
               ["Turbinar", "Botão do Instagram para pagar e mostrar um post a mais pessoas"],
               ["Alcance", "Quantas pessoas diferentes viram o post"],
               ["Custo por clique (CPC)", "Quanto pagamos, em média, por cada pessoa que tocou em \"Visitar site\""],
               ["UTM (utm_medium=pago)", "Etiqueta no link que mostra no painel do blog que a visita veio do anúncio"],
               ["Ponto de equilíbrio", "Número de vendas cuja comissão paga o anúncio"],
               ["Reels", "Vídeo curto em pé; costuma ter custo por clique menor que post de foto"],
           ], [0.28, 0.72]),
           PageBreak()]

    # ---------------- 10. aprovação
    lin = "_______________________________"
    st += [Paragraph("10. Checklist e aprovação dos sócios", S["h1"]),
           tabela([
               ["[   ]", "Item para decidir na reunião"],
               ["[   ]", "Os termos do ML Afiliados permitem anúncio pago? (quem verifica e até quando)"],
               ["[   ]", f"Valor máximo aprovado: ( ) R$ 30 só teste   ( ) R$ 135 teste + BF   ( ) {brl(acum)} completo   ( ) outro: R$ ______"],
               ["[   ]", "Quem paga (cartão/Pix) e em nome de quem fica a conta de anúncios"],
               ["[   ]", "Quem olha os números e manda os prints nas datas de avaliação (19/11, 30/11, 21/12)"],
               ["[   ]", "Como dividir o resultado (comissão) e o custo do anúncio entre os sócios"],
           ], [0.06, 0.94], zebra=False),
           Spacer(1, 26),
           KeepTogether([tabela([
               ["", "Sócio 1", "Sócio 2"],
               ["Nome", lin, lin],
               ["Decisão", "( ) Aprovo   ( ) Não aprovo", "( ) Aprovo   ( ) Não aprovo"],
               ["Valor máximo", "R$ ________", "R$ ________"],
               ["Data", "____/____/2026", "____/____/2026"],
               ["Assinatura", lin, lin],
           ], [0.2, 0.4, 0.4], zebra=False,
               extra=[("TOPPADDING", (0, 1), (-1, -1), 12), ("BOTTOMPADDING", (0, 1), (-1, -1), 12)])]),
           Spacer(1, 20),
           caixa("<b>Próximo passo após a aprovação:</b> avisar o Claude com o valor aprovado. Ele coloca as datas no "
                 "calendário (.ics), prepara os textos e links de cada fase e analisa os números em 19/11, 30/11 e 21/12. "
                 "O pagamento e a confirmação no Instagram são sempre feitos pelo sócio pagador.", VERDE_C, VERDE)]
    return st


if __name__ == "__main__":
    import gerar_quadro_resumo  # refaz o quadro (PDF + PNG) com os mesmos valores antes de montar o plano
    gerar_quadro_resumo.main()
    doc =SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm,
                            bottomMargin=1.8 * cm, title="Plano Turbinar Instagram 2026", author="comprenolink.net")
    doc.build(montar(), onFirstPage=capa, onLaterPages=rodape)
    print("PDF:", SAIDA)
