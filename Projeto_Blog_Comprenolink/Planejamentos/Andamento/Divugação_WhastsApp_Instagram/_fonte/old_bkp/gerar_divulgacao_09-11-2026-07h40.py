# -*- coding: utf-8 -*-
"""
Gera o pacote de divulgação (Instagram + WhatsApp) em D:\\mercado_livre\\3- DIVULGAÇÃO_WHATSAPP_INSTAGRAM:
  00_LEIA-ME_COMECE_AQUI.txt, 01_GUIA_COMPLETO_DIVULGACAO.pdf, 02_CHECKLISTS_IMPRIMIVEIS.pdf,
  03_TEXTOS_PRONTOS_PARA_COPIAR.txt, 04_CALENDARIO_POSTS_NOV_DEZ.xlsx, 05_LINKS_RASTREAVEIS.txt
Lê os produtos do blog ao vivo (só leitura). Rode de novo quando o Top 10 ou os produtos mudarem:
  python -X utf8 _fonte\\gerar_divulgacao.py
A planilha existente NÃO é sobrescrita se já tiver "Feito" marcado (gera uma cópia _nova).
"""
import os
import sys
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dados_divulgacao as dd  # noqa: E402
from conteudo_celular import CELULAR, RESPOSTAS_RAPIDAS  # noqa: E402
from conteudo_guia import CHECKLISTS, GUIA  # noqa: E402

from reportlab.lib import colors  # noqa: E402
from reportlab.lib.enums import TA_CENTER  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.pdfbase import pdfmetrics  # noqa: E402
from reportlab.pdfbase.ttfonts import TTFont  # noqa: E402
from reportlab.platypus import (KeepTogether, ListFlowable, ListItem, PageBreak, Paragraph,  # noqa: E402
                                SimpleDocTemplate, Spacer, Table, TableStyle)

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONTES = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Arial", os.path.join(FONTES, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Bold", os.path.join(FONTES, "arialbd.ttf")))
pdfmetrics.registerFont(TTFont("Arial-Italic", os.path.join(FONTES, "ariali.ttf")))
from reportlab.pdfbase.pdfmetrics import registerFontFamily  # noqa: E402
registerFontFamily("Arial", normal="Arial", bold="Arial-Bold", italic="Arial-Italic", boldItalic="Arial-Bold")

ESCURO, AMARELO, AZUL, CINZA = colors.HexColor("#111827"), colors.HexColor("#FFD54A"), colors.HexColor("#0B5FA5"), colors.HexColor("#5B6474")
S = {
    "capa": ParagraphStyle("capa", fontName="Arial-Bold", fontSize=26, leading=32, textColor=ESCURO, alignment=TA_CENTER),
    "sub": ParagraphStyle("sub", fontName="Arial", fontSize=13, leading=18, textColor=CINZA, alignment=TA_CENTER),
    "h1": ParagraphStyle("h1", fontName="Arial-Bold", fontSize=17, leading=22, textColor=ESCURO, spaceBefore=10, spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="Arial-Bold", fontSize=12.5, leading=16, textColor=AZUL, spaceBefore=8, spaceAfter=4),
    "p": ParagraphStyle("p", fontName="Arial", fontSize=10.5, leading=14.5, spaceAfter=5),
    "cel": ParagraphStyle("cel", fontName="Arial", fontSize=9, leading=11.5),
    "celb": ParagraphStyle("celb", fontName="Arial-Bold", fontSize=9, leading=11.5, textColor=colors.white),
    "caixa": ParagraphStyle("caixa", fontName="Arial", fontSize=10, leading=13.5),
}


def caixa(texto, cor_fundo, cor_borda, rotulo):
    t = Table([[Paragraph(f"<b>{rotulo}</b> {texto}", S["caixa"])]], colWidths=[17 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), cor_fundo), ("BOX", (0, 0), (-1, -1), 1, cor_borda),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return [Spacer(1, 3), t, Spacer(1, 6)]


def tabela(linhas):
    n = len(linhas[0])
    larg = {2: [6.5 * cm, 10.5 * cm], 3: [4 * cm, 8.5 * cm, 4.5 * cm], 4: [4.6 * cm, 3 * cm, 3 * cm, 6.4 * cm]}[n]
    dados = [[Paragraph(c, S["celb"]) for c in linhas[0]]] + [[Paragraph(c, S["cel"]) for c in l] for l in linhas[1:]]
    t = Table(dados, colWidths=larg, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), ESCURO), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#D5D9E0")),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F7FA")]),
                           ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return [t, Spacer(1, 8)]


def rodape(canvas, doc, titulo):
    canvas.saveState()
    canvas.setFillColor(AMARELO)
    canvas.rect(0, A4[1] - 0.35 * cm, A4[0], 0.35 * cm, fill=1, stroke=0)
    canvas.setFont("Arial", 8)
    canvas.setFillColor(CINZA)
    canvas.drawString(2 * cm, 1.2 * cm, f"comprenolink.net – {titulo}")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"página {doc.page}")
    canvas.restoreState()


def capa(titulo, subtitulo):
    return [Spacer(1, 6 * cm), Paragraph(titulo, S["capa"]), Spacer(1, 0.6 * cm), Paragraph(subtitulo, S["sub"]),
            Spacer(1, 0.4 * cm), Paragraph(f"Atualizado em {datetime.now():%d/%m/%Y}", S["sub"]), PageBreak()]


def gera_guia(dados, arq, blocos=GUIA, titulo="Guia de Divulgação<br/>Instagram e WhatsApp",
              subtitulo="Passo a passo para qualquer pessoa divulgar o blog comprenolink.net<br/>e levar visitas às ofertas do Mercado Livre",
              rotulo="Guia de divulgação"):
    hist = capa(titulo, subtitulo)
    top = dados["top"]
    for bloco in blocos:
        tipo = bloco[0]
        if tipo == "quebra":
            hist.append(PageBreak())
        elif tipo in ("h1", "h2", "p"):
            hist.append(Paragraph(bloco[1], S[tipo]))
        elif tipo in ("passos", "lista"):
            itens = [ListItem(Paragraph(t, S["p"]), leftIndent=14) for t in bloco[1]]
            hist.append(ListFlowable(itens, bulletType="1" if tipo == "passos" else "bullet", start="1",
                                     bulletFontName="Arial-Bold", bulletFontSize=10, leftIndent=16))
        elif tipo == "dica":
            hist += caixa(bloco[1], colors.HexColor("#EAF4FF"), AZUL, "Dica:")
        elif tipo == "alerta":
            hist += caixa(bloco[1], colors.HexColor("#FFF4D6"), colors.HexColor("#C98A00"), "Atenção:")
        elif tipo == "tabela":
            hist += tabela(bloco[1])
    if blocos is GUIA:
        hist.append(PageBreak())
        hist.append(Paragraph("13. Produtos em destaque nesta campanha (lidos do blog)", S["h1"]))
        for camp, nome in (("black_friday", "Top 10 da Black Friday"), ("natal", "Top 10 presentes de Natal")):
            hist.append(Paragraph(nome, S["h2"]))
            hist += tabela([["#", "Produto (nome no blog)", "Selo"]] +
                           [[str(k), x["nome"], x["selo"]] for k, x in enumerate(top[camp], 1)])
    doc = SimpleDocTemplate(arq, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm,
                            title=titulo.replace("<br/>", " – "), author="comprenolink.net")
    doc.build(hist, onFirstPage=lambda c, d: None, onLaterPages=lambda c, d: rodape(c, d, rotulo))


def gera_checklists(arq):
    hist = capa("Checklists de Divulgação", "Imprima e marque com X cada tarefa concluída")
    for titulo, itens in CHECKLISTS:
        linhas = [[Paragraph("<b>Feito</b>", S["celb"]), Paragraph("<b>Tarefa</b>", S["celb"]), Paragraph("<b>Data</b>", S["celb"])]]
        linhas += [["", Paragraph(t, S["cel"]), ""] for t in itens]
        t = Table(linhas, colWidths=[1.5 * cm, 12.5 * cm, 3 * cm], repeatRows=1, rowHeights=[None] + [0.85 * cm] * len(itens))
        estilo = [("BACKGROUND", (0, 0), (-1, 0), ESCURO), ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#B9C0CB")),
                  ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]
        t.setStyle(TableStyle(estilo))
        hist += [Paragraph(titulo, S["h1"]), t, Spacer(1, 14)]
        hist.append(KeepTogether([Paragraph("Observações:", S["p"]), Spacer(1, 1.2 * cm)]))
        hist.append(PageBreak())
    doc = SimpleDocTemplate(arq, pagesize=A4, leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.8 * cm, bottomMargin=2 * cm,
                            title="Checklists de Divulgação", author="comprenolink.net")
    doc.build(hist, onFirstPage=lambda c, d: None, onLaterPages=lambda c, d: rodape(c, d, "Checklists de divulgação"))


BIO = ("🛒 Achados do Mercado Livre comparados pra você\n"
       "🔥 Black Friday: Top 10 + ofertas por categoria\n"
       "💬 Comente BLACK e receba o link\n"
       "👇 Lista no blog")
TEXTOS_FIXOS = [
    ("BIO DO INSTAGRAM (até 150 caracteres)", BIO),
    ("BIO DO INSTAGRAM – DEZEMBRO", BIO.replace("🔥 Black Friday: Top 10 + ofertas por categoria", "🎄 Presentes de Natal: Top 10 que agradam")
     .replace("BLACK", "NATAL")),
    ("DESCRIÇÃO DO PERFIL COMERCIAL (WhatsApp Business)",
     "Blog comprenolink.net: comparamos os produtos mais vendidos e bem avaliados do Mercado Livre. "
     "Peça o link de qualquer produto por aqui. Links de afiliado, sem custo extra para você."),
    ("MENSAGEM DE SAUDAÇÃO (WhatsApp Business)",
     "Olá! 👋 Aqui é o Compre no Link. Me diga qual produto você procura que eu te mando o link do blog "
     "com os detalhes e o valor do dia no Mercado Livre. Quer receber as ofertas? Salve este número e responda OFERTAS."),
    ("MENSAGEM DE AUSÊNCIA (WhatsApp Business)",
     "Oi! Agora estou fora, mas respondo assim que voltar. Enquanto isso, a lista completa está em: https://comprenolink.net"),
    ("DESCRIÇÃO DO CANAL (WhatsApp)",
     "Achados do Mercado Livre selecionados pelo blog comprenolink.net: Black Friday, presentes de Natal e "
     "os mais vendidos e bem avaliados de cada categoria. Links de afiliado, sem custo extra para você."),
    ("CONVITE PARA O CANAL (Status / grupos)",
     "📣 Criei um canal no WhatsApp com os achados do Mercado Livre (Black Friday e Natal). "
     "É só tocar e seguir, sem grupo e sem conversa: [COLE AQUI O LINK DO CANAL]"),
    ("RESPOSTA PADRÃO NO DIRECT (quando não citar produto)",
     "Oi! Tudo bem? 😊 A lista completa está aqui: " + dd.utm(dd.PAG["black_friday"], "instagram", "dm", "black_friday", "resposta_padrao") +
     "\nLá você vê os detalhes e confere o valor do dia no Mercado Livre. (Link de afiliado: posso ganhar comissão, sem custo extra para você.)"),
    ("RESPOSTA QUANDO PERGUNTAM O PREÇO",
     "O valor muda todo dia no Mercado Livre 😊 Pelo link você vê o preço de hoje direto no anúncio oficial."),
    ("RESPOSTA NO COMENTÁRIO",
     "Te mandei no Direct! 📩"),
    ("WHATSAPP DO BLOG (para bio, perfil e quem pedir contato)",
     f"WhatsApp: {dd.WHATSAPP}\nLink que abre a conversa: {dd.WHATSAPP_LINK}"),
    ("CONVITE PARA FALAR NO WHATSAPP (story / legenda)",
     f"💬 Quer o link de algum produto ou tem dúvida? Chama no WhatsApp {dd.WHATSAPP} (link na bio) que eu te ajudo."),
]


def gera_textos(dados, arq):
    L = ["TEXTOS PRONTOS PARA COPIAR – comprenolink.net", f"Gerado em {datetime.now():%d/%m/%Y %H:%M} a partir dos produtos do blog.",
         "Regras: sem preço, sem promessa de saúde/estética, sempre com o aviso de afiliado.",
         "Dica: no celular, abra este arquivo no app do OneDrive/Arquivos, segure o dedo no texto e copie.", ""]
    for titulo, texto in TEXTOS_FIXOS:
        L += ["=" * 70, titulo, "=" * 70, texto, ""]
    L += ["#" * 70, "RESPOSTAS RÁPIDAS (WhatsApp Business → Ferramentas comerciais → Respostas rápidas)", "#" * 70]
    troca = {"{BF}": dd.utm(dd.PAG["black_friday"], "whatsapp", "conversa", "black_friday", "resposta_rapida"),
             "{NATAL}": dd.utm(dd.PAG["natal"], "whatsapp", "conversa", "natal", "resposta_rapida"),
             "{SITE}": dd.utm(dd.GUIA, "whatsapp", "conversa", "perfil", "resposta_rapida")}
    for atalho, texto in RESPOSTAS_RAPIDAS:
        for k, v in troca.items():
            texto = texto.replace(k, v)
        L += [f"--- Atalho: {atalho}   (na conversa, digite /{atalho}) ---", texto, ""]
    for camp, nome in (("black_friday", "BLACK FRIDAY – TOP 10"), ("natal", "NATAL – TOP 10")):
        L += ["#" * 70, f"MENSAGENS DE {nome.split(' –')[0]} (grupos, lembretes)", "#" * 70]
        L += ["--- Mensagem semanal para grupos ---", dd.MSG_GRUPO[camp].replace("{LINK}", dd.utm(dd.PAG[camp], "whatsapp", "grupos", camp, "mensagem")), ""]
        if camp == "black_friday":
            L += ["--- Lembrete (26/11) ---", dd.MSG_LEMBRETE.replace("{LINK}", dd.utm(dd.PAG[camp], "whatsapp", "grupos", camp, "lembrete")), "",
                  "--- Dia D (27/11) ---", dd.MSG_DIA_D.replace("{LINK}", dd.utm(dd.PAG[camp], "whatsapp", "grupos", camp, "dia_d")), "",
                  "--- Cyber Monday (30/11) ---", dd.MSG_CYBER.replace("{LINK}", dd.utm(dd.PAG[camp], "whatsapp", "grupos", camp, "cyber")), ""]
        L += ["#" * 70, f"PRODUTOS {nome}", "#" * 70, ""]
        for k, x in enumerate(dados["top"][camp], 1):
            t = dd.textos_produto(x, camp, date.today())
            L += ["=" * 70, f"{k}. {x['nome']}  (item {x['n']} do guia)", "=" * 70,
                  "--- LEGENDA DO FEED ---", t["legenda"], "",
                  "--- TEXTO DO STORY (link no adesivo: ver planilha ou abaixo) ---", t["story"], "Link do story: " + t["link_story"], "",
                  "--- RESPOSTA NO DIRECT ---", t["dm"], "",
                  "--- WHATSAPP (Status/Canal) ---", t["wpp"].replace("{LINK}", t["link_wpp"]["status"]), ""]
    L += ["=" * 70, "HASHTAGS POR CATEGORIA", "=" * 70]
    L += [f"{k}: {' '.join(v)}" for k, v in dd.TAGS_CAT.items()]
    L += [f"Black Friday: {' '.join(dd.TAGS_CAMPANHA['black_friday'])}", f"Natal: {' '.join(dd.TAGS_CAMPANHA['natal'])}",
          f"Sempre: {' '.join(dd.TAGS_BASE)}", ""]
    with open(arq, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write("\n".join(L))


def gera_links(arq):
    L = ["LINKS RASTREÁVEIS – comprenolink.net", "Use SEMPRE estes links (com utm). Não apague o pedaço depois do \"?\".", ""]
    for nome, link in dd.LINKS_FIXOS:
        L += [nome, "   " + link, ""]
    L += ["Links de cada post (story, Direct, Status, Canal): planilha 04_CALENDARIO_POSTS_NOV_DEZ.xlsx, coluna Link.", ""]
    with open(arq, "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write("\n".join(L))


def gera_planilha(dados, arq):
    from openpyxl import Workbook, load_workbook
    from openpyxl.formatting.rule import FormulaRule
    from openpyxl.styles import Alignment, Font, PatternFill
    from openpyxl.worksheet.datavalidation import DataValidation
    if os.path.exists(arq):  # não perde o que a pessoa já marcou
        ws = load_workbook(arq)["Calendário"]
        if any(str(ws.cell(r, 10).value or "").upper() == "S" for r in range(2, ws.max_row + 1)):
            arq = arq.replace(".xlsx", f"_nova_{datetime.now():%Y%m%d}.xlsx")
    wb = Workbook()
    cab_fill, cab_font = PatternFill("solid", fgColor="111827"), Font(bold=True, color="FFFFFF")
    dias = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

    ws = wb.active
    ws.title = "Calendário"
    cab = ["Data", "Dia", "Hora", "Canal", "Formato", "Campanha", "Produto", "Item", "Texto pronto (copiar)", "Feito (S/N)", "Link (com utm)", "Observações"]
    ws.append(cab)
    for l in dd.calendario(dados):
        ws.append([l["data"], dias[l["data"].weekday()], l["hora"], l["canal"], l["formato"],
                   "Black Friday" if l["campanha"] == "black_friday" else "Natal", l["produto"], l["item"], l["texto"], "N", l["link"], l["obs"]])
    for c in ws[1]:
        c.fill, c.font = cab_fill, cab_font
    larg = [11, 5, 6, 14, 22, 12, 34, 6, 70, 9, 60, 34]
    for i, w in enumerate(larg, 1):
        ws.column_dimensions[chr(64 + i)].width = w
    for row in ws.iter_rows(min_row=2):
        row[0].number_format = "DD/MM/YYYY"
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    dv = DataValidation(type="list", formula1='"S,N"', allow_blank=False)
    ws.add_data_validation(dv)
    dv.add(f"J2:J{ws.max_row}")
    ws.conditional_formatting.add(f"A2:L{ws.max_row}", FormulaRule(formula=['$J2="S"'], fill=PatternFill("solid", fgColor="D9F2D9")))
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = f"A1:L{ws.max_row}"

    wl = wb.create_sheet("Links")
    wl.append(["Onde usar", "Link (com utm)"])
    for nome, link in dd.LINKS_FIXOS:
        wl.append([nome, link])
    for c in wl[1]:
        c.fill, c.font = cab_fill, cab_font
    wl.column_dimensions["A"].width, wl.column_dimensions["B"].width = 45, 120

    wr = wb.create_sheet("Resultados semanais")
    wr.append(["Semana (início)", "Seguidores IG", "Contas alcançadas IG", "Toques no link IG", "Seguidores Canal WPP",
               "Visitas blog – Instagram", "Visitas blog – WhatsApp", "Cliques Mercado Livre", "Vendas", "Comissão (R$)", "O que funcionou / o que mudar"])
    for d in ["02/11/2026", "09/11/2026", "16/11/2026", "23/11/2026", "30/11/2026", "07/12/2026", "14/12/2026", "21/12/2026"]:
        wr.append([d] + [None] * 10)
    for c in wr[1]:
        c.fill, c.font = cab_fill, cab_font
        c.alignment = Alignment(wrap_text=True, vertical="top")
    for i, w in enumerate([14, 12, 14, 12, 14, 14, 14, 14, 9, 12, 50], 1):
        wr.column_dimensions[chr(64 + i)].width = w

    wc = wb.create_sheet("Como usar")
    for linha in ["COMO USAR ESTA PLANILHA",
                  "1. Aba Calendário: cada linha é uma tarefa com data, hora, canal, texto pronto e link.",
                  "2. Copie o 'Texto pronto' e cole no Instagram/WhatsApp. Use o 'Link' no adesivo do story, no Status ou no Canal.",
                  "3. Depois de fazer, mude 'Feito' para S: a linha fica verde.",
                  "4. Use o filtro da coluna Data ou Canal para ver só o dia/canal que quer.",
                  "5. Aba Links: links fixos (bio, grupos, canal, lista).",
                  "6. Aba Resultados semanais: preencha toda sexta (veja o capítulo 10 do guia).",
                  "Regras: sem preço, sem promessas de saúde/estética, sempre o aviso de afiliado (o texto pronto já tem)."]:
        wc.append([linha])
    wc["A1"].font = Font(bold=True, size=13)
    wc.column_dimensions["A"].width = 120
    wb.save(arq)
    return arq


LEIA_ME = """COMECE AQUI – DIVULGAÇÃO DO BLOG NO INSTAGRAM E WHATSAPP
==========================================================
Blog: https://comprenolink.net      Atualizado em {data}

ORDEM PARA COMEÇAR
  1. Leia o 01_GUIA_COMPLETO_DIVULGACAO.pdf (capítulos 1 a 3: como funciona e regras).
  2. Faça a PREPARAÇÃO (capítulo 4 do guia) usando o checklist A do 02_CHECKLISTS_IMPRIMIVEIS.pdf.
  3. Abra a 04_CALENDARIO_POSTS_NOV_DEZ.xlsx: cada linha diz o que postar, quando, com texto e link.
  4. Copie textos do 03_TEXTOS_PRONTOS_PARA_COPIAR.txt (bio, saudação, legendas, mensagens).
  5. Links fixos (bio, grupos, canal): 05_LINKS_RASTREAVEIS.txt.

ARQUIVOS
  00_LEIA-ME_COMECE_AQUI.txt ........ este arquivo
  01_GUIA_COMPLETO_DIVULGACAO.pdf ... passo a passo completo (Instagram, WhatsApp, Canva, métricas)
  02_CHECKLISTS_IMPRIMIVEIS.pdf ..... preparação, antes de publicar, diário, semanal, Black Friday, Natal, mês
  03_TEXTOS_PRONTOS_PARA_COPIAR.txt . bio, mensagens do WhatsApp Business, legendas e Direct do Top 10
  04_CALENDARIO_POSTS_NOV_DEZ.xlsx .. {n} tarefas de 02/11 a 23/12, coluna Feito (S/N), resultados
  05_LINKS_RASTREAVEIS.txt .......... links com utm para cada canal
  06_CATALOGO_WHATSAPP\\ ............. fotos + textos dos 17 produtos para o catálogo do WhatsApp Business
  07_PACOTE_DO_DIA\\ .................. uma pasta por dia: feed.png, story.png, status.png e 1_TEXTOS_DO_DIA.txt
  08_PASSO_A_PASSO_WHATSAPP_NO_CELULAR.pdf  o que fazer no celular, tela por tela
  Cópia para o celular: E:\\OneDrive\\Download\\Divulgacao_Blog (abrir pelo app OneDrive)
  ARTES_PRONTAS\\ ..................... (crie) as artes do Canva com nome AAAAMMDD_produto_feed.png
  _fonte\\ ............................ programa que gera tudo (pedir ao Claude para atualizar)

REGRAS DE OURO
  - Nunca escrever preço nem "menor/melhor preço" (use "confira o valor do dia").
  - Nunca prometer saúde/estética. Falar só de composição, tamanho, quantidade.
  - Sempre o aviso "Publi: contém link de afiliado".
  - WhatsApp só para quem aceitou (Canal, Status, grupos com permissão, lista de quem salvou o número).
  - Sem robôs, compra de seguidores ou mensagens em massa para desconhecidos.

AGENDA
  Os horários batem com a agenda E:\\OneDrive\\Download\\calendario_blog_2026.ics
  (posts 19:00 seg/qua/sex; semana da Black Friday todo dia; grupos terça 12:00).

ATUALIZAR ESTE PACOTE
  Quando mudarem os produtos do Top 10 ou entrar campanha nova, peça ao Claude:
  "gerar o pacote de divulgação de novo". A planilha com tarefas marcadas não é apagada
  (sai uma cópia _nova).
"""


def main():
    dados = dd.carrega_produtos()
    gera_guia(dados, os.path.join(PASTA, "01_GUIA_COMPLETO_DIVULGACAO.pdf"))
    gera_checklists(os.path.join(PASTA, "02_CHECKLISTS_IMPRIMIVEIS.pdf"))
    gera_textos(dados, os.path.join(PASTA, "03_TEXTOS_PRONTOS_PARA_COPIAR.txt"))
    planilha = gera_planilha(dados, os.path.join(PASTA, "04_CALENDARIO_POSTS_NOV_DEZ.xlsx"))
    gera_links(os.path.join(PASTA, "05_LINKS_RASTREAVEIS.txt"))
    gera_guia(dados, os.path.join(PASTA, "08_PASSO_A_PASSO_WHATSAPP_NO_CELULAR.pdf"), CELULAR,
              "Passo a passo no celular<br/>WhatsApp Business", "Instalação, perfil, catálogo, respostas rápidas,<br/>Canal e a rotina de cada dia",
              "Passo a passo no celular")
    with open(os.path.join(PASTA, "00_LEIA-ME_COMECE_AQUI.txt"), "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write(LEIA_ME.format(data=f"{datetime.now():%d/%m/%Y}", n=len(dd.calendario(dados))))
    print("Pacote gerado em", PASTA, "| planilha:", os.path.basename(planilha))


if __name__ == "__main__":
    main()
