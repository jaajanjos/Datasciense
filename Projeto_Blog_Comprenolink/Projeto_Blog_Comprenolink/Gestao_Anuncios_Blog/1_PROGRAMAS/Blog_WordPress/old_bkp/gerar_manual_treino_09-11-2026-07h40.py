# -*- coding: utf-8 -*-
"""Gera Manual_Treino.pdf - um exemplo real de cada opção do menu (1 a 8), rodado em modo treino."""
import html
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

PASTA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(PASTA, "..", ".."))  # pasta Manutenção_Blog
SAIDA = os.path.join(RAIZ, "3_DOCUMENTACAO", "Blog_WordPress", "Manual_Treino.pdf")

AZUL = colors.HexColor("#0B5FA5")
CINZA = colors.HexColor("#444444")
AMARELO = colors.HexColor("#FFF4CC")
VERDE = colors.HexColor("#E6F4EA")
LINHA = colors.HexColor("#D0D7DE")

base = ParagraphStyle("base", fontName="Helvetica", fontSize=11.5, leading=16, textColor=colors.HexColor("#1a1a1a"))
h1 = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=AZUL, spaceAfter=10)
passo_t = ParagraphStyle("passo_t", parent=base, fontName="Helvetica-Bold", fontSize=13.5, leading=17, spaceAfter=3)
peq = ParagraphStyle("peq", parent=base, fontSize=10, leading=13.5, textColor=CINZA)
cod = ParagraphStyle("cod", fontName="Courier", fontSize=9.5, leading=12.5, textColor=colors.HexColor("#E5E7EB"))
capa_t = ParagraphStyle("capa_t", parent=h1, fontSize=28, leading=34, alignment=TA_CENTER)
capa_s = ParagraphStyle("capa_s", parent=base, fontSize=14, leading=20, alignment=TA_CENTER, textColor=CINZA)


def P(t, s=base):
    return Paragraph(t, s)


def lista(itens, s=base):
    return [Paragraph("&bull;&nbsp;&nbsp;" + i, ParagraphStyle("li", parent=s, leftIndent=14, firstLineIndent=-10, spaceAfter=2))
            for i in itens]


def caixa(titulo, linhas, cor):
    conteudo = [P(f"<b>{titulo}</b>", base)] + [P(l, base) for l in linhas]
    t = Table([[conteudo]], colWidths=[16.4 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), cor), ("BOX", (0, 0), (-1, -1), 0.6, LINHA),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t


def tela(linhas):
    conteudo = [P(html.escape(l).replace(" ", "&nbsp;") or "&nbsp;", cod) for l in linhas]
    t = Table([[conteudo]], colWidths=[16.4 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#111827")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def digitar(linhas):
    dados = [[P("<b>O programa pede</b>", peq), P("<b>Você digita</b>", peq)]] + [[P(a, peq), P(b, peq)] for a, b in linhas]
    t = Table(dados, colWidths=[8.6 * cm, 7.8 * cm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F0FA")), ("GRID", (0, 0), (-1, -1), 0.5, LINHA),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def opcao(n, titulo, resumo, miolo):
    tag = Table([[P(f"<font color='white'><b>Opção {n}</b></font>", ParagraphStyle("tag", parent=base, fontSize=12, alignment=TA_CENTER))]],
               colWidths=[2.8 * cm], rowHeights=[0.9 * cm])
    tag.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), AZUL), ("VALIGN", (0, 0), (-1, -1), "MIDDLE")]))
    linha = Table([[tag, P(titulo, passo_t)]], colWidths=[3 * cm, 13.4 * cm])
    linha.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("LEFTPADDING", (0, 0), (-1, -1), 0)]))
    conteudo = [linha, Spacer(1, 4), P(resumo, base), Spacer(1, 6)] + miolo
    return [KeepTogether(conteudo), Spacer(1, 16)]


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(CINZA)
    canvas.drawString(2 * cm, 1.2 * cm, "Manual de Treino - GerenciarBlog.exe")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def montar():
    s = []
    s += [Spacer(1, 5 * cm), P("Manual de Treino", capa_t), Spacer(1, 6),
          P("Um exemplo real de cada opção do menu", capa_s), Spacer(1, 4),
          P("GerenciarBlog.exe &mdash; modo offline (TREINAR.bat)", capa_s), Spacer(1, 2.5 * cm),
          caixa("O que é o modo treino",
                ["Ao abrir pelo <b>TREINAR.bat</b>, o programa mostra <b>[MODO OFFLINE]</b> no título do menu e usa uma "
                 "cópia do guia salva em <b>treino\\pagina_exemplo.html</b>. Mesmo respondendo <b>s</b> para \"Aplicar no site "
                 "AGORA?\", <b>nada é enviado ao comprenolink.net</b> &mdash; o resultado fica só no arquivo "
                 "<b>saida_offline.html</b>, na mesma pasta."],
                VERDE), Spacer(1, 8),
          caixa("Como foram geradas as telas deste manual",
                ["Cada página abaixo mostra a tela <b>real</b> do programa, rodando no mesmo modo treino que você vai usar &mdash; "
                 "não são imagens ilustrativas, é a saída de verdade de cada opção."], AMARELO),
          PageBreak()]

    s += [P("As 8 opções do menu", h1)]
    s.append(tela([' 1) Testar conexão          5) Adicionar anúncio', ' 2) Listar anúncios         6) Buscar e substituir texto',
                   ' 3) Editar anúncio          7) Fazer backup agora', ' 4) Remover anúncio         8) Restaurar um backup',
                   ' 0) Sair']))
    s += [Spacer(1, 16)]

    # ---------------------------------------------------------------- opção 1
    s += opcao(1, "Testar conexão",
               "Confirma se o login e a senha de aplicativo estão corretos, e quantos itens a página tem. "
               "Esta é a <b>única opção que sempre tenta acessar o site de verdade</b>, mesmo em modo treino "
               "&mdash; por isso é normal ela dar erro enquanto o arquivo <b>wp_credenciais.json</b> ainda não existe:",
               [digitar([("Escolha:", "<b>1</b>")]), Spacer(1, 4),
                tela(["ERRO: Faltam as credenciais. Copie wp_credenciais.exemplo.json para",
                      "wp_credenciais.json e preencha 'usuario' e 'senha_aplicativo'",
                      "(veja o LEIA-ME)."]), Spacer(1, 4),
                P("Depois de preencher <b>wp_credenciais.json</b> com a senha de aplicativo de verdade e rodar "
                  "<b>sem</b> o modo treino (GerenciarBlog.exe normal), esta mesma opção mostra: "
                  "<font face='Courier'>Conectado como: ...  pode editar páginas: SIM</font>.", peq)])

    # ---------------------------------------------------------------- opção 2
    s += opcao(2, "Listar anúncios",
               "Mostra todos os anúncios do guia: número, nome, selo, preço e link. Use o número para as opções 3 e 4.",
               [digitar([("Escolha:", "<b>2</b>")]), Spacer(1, 4),
                tela(["Os 21 Melhores Produtos do Mercado Livre em 2026  (21 itens)",
                      "",
                      " 1. Fone JBL Bluetooth On-Ear  [Mais Vendido]  R$ 319,00",
                      "      https://meli.la/1XdTgfZ",
                      " 2. Fone In-Ear QCY  [Melhor Custo-Benefício]  R$ 319,00",
                      "      https://meli.la/2Lwv4FH",
                      " 3. Caixa de Som Bluetooth  [Preferida para Uso Externo]  R$ 1.379,90",
                      "      https://meli.la/1JyNNjn",
                      "      (... segue até o item 21 ...)"])])

    # ---------------------------------------------------------------- opção 3
    s += opcao(3, "Editar anúncio",
               "Exemplo: o Echo Dot (item 4) baixou de preço. Nos campos que você não quer mudar, é só apertar ENTER.",
               [digitar([("Escolha:", "<b>3</b>"), ("Número do anúncio a editar:", "<b>4</b>"),
                         ("Novo nome / selo / descrição / benefícios / ideal para / título do anúncio / imagem:", "(ENTER em cada um)"),
                         ("Novo link meli.la:", "<b>https://meli.la/EXEMPLO4</b>"),
                         ("Novo preço (ex.: R$ 299,90):", "<b>R$ 279,00</b>"),
                         ("Aplicar no site AGORA? (s/N):", "<b>s</b>")]), Spacer(1, 4),
                tela(["=== RESUMO DA MUDANÇA (leia antes de confirmar) ===",
                      "  Item 4 (Amazon Echo Dot 5a Geracao) - link:",
                      "    https://meli.la/1AXvaMV  ->  https://meli.la/EXEMPLO4",
                      "  Item 4 (Amazon Echo Dot 5a Geracao) - preco: R$ 449,00  ->  R$ 279,00",
                      "",
                      "[offline] resultado gravado em ...\\saida_offline.html",
                      "(nada foi enviado ao site)."])])

    s.append(PageBreak())

    # ---------------------------------------------------------------- opção 4
    s += opcao(4, "Remover anúncio",
               "Exemplo: a Soundbar (item 7) saiu de estoque. Os itens seguintes são renumerados sozinhos.",
               [digitar([("Escolha:", "<b>4</b>"), ("Número do anúncio a REMOVER:", "<b>7</b>"),
                         ("Aplicar no site AGORA? (s/N):", "<b>s</b>")]), Spacer(1, 4),
                tela(["Removendo o item 7: Soundbar  (https://meli.la/1Qeyqb3)",
                      "Os itens seguintes foram renumerados; agora são 20 itens.",
                      "",
                      "=== RESUMO DA MUDANÇA (leia antes de confirmar) ===",
                      "  REMOVIDO:   item 7 - Soundbar",
                      "  14 anúncio(s) mantido(s) foram renumerados automaticamente.",
                      "  Texto 'reunimos N modelos': 21  ->  20",
                      "  Data 'Atualizado em': 21/10/2026  ->  22/10/2026"])])

    # ---------------------------------------------------------------- opção 5
    s += opcao(5, "Adicionar anúncio",
               "Exemplo: incluir o JBL Tune 520BT na 2ª posição, já com uma linha na tabela \"Escolha rápida\". "
               "Só <b>nome</b> e <b>link</b> são obrigatórios; listas usam o sinal | entre os itens.",
               [digitar([("Escolha:", "<b>5</b>"), ("Nome curto do produto:", "<b>JBL Tune 520BT</b>"),
                         ("Link meli.la do produto:", "<b>https://meli.la/EXEMPLO520</b>"),
                         ("Selo:", "<b>Oferta Black Friday</b>"), ("Preço:", "<b>R$ 199,90</b>"),
                         ("Benefícios:", "<b>Som JBL Pure Bass|Bateria de longa duração|Leve</b>"),
                         ("Posição:", "<b>2</b>"), ("Categoria p/ tabela 'Escolha rápida':", "<b>Fone JBL em oferta</b>"),
                         ("Aplicar no site AGORA? (s/N):", "<b>s</b>")]), Spacer(1, 4),
                tela(["Novo item entrará na posição 2; agora são 22 itens.", "",
                      "=== RESUMO DA MUDANÇA (leia antes de confirmar) ===",
                      "  ADICIONADO: item 2 - JBL Tune 520BT  [Oferta Black Friday]  R$ 199,90",
                      "  20 anúncio(s) mantido(s) foram renumerados automaticamente.",
                      "  Tabela 'Escolha rápida': 7 -> 8 linha(s)"])])

    s.append(PageBreak())

    # ---------------------------------------------------------------- opção 6
    s += opcao(6, "Buscar e substituir texto",
               "Útil para corrigir um texto que se repete na página. Exemplo: corrigir a data do aviso de atualização.",
               [digitar([("Escolha:", "<b>6</b>"), ("Texto a procurar:", "<b>Atualizado em 21/10/2026</b>"),
                         ("Trocar por:", "<b>Atualizado em 22/10/2026</b>"), ("Aplicar no site AGORA? (s/N):", "<b>s</b>")]),
                Spacer(1, 4),
                tela(["1 ocorrência(s) de 'Atualizado em 21/10/2026' na página.", "",
                      "=== RESUMO DA MUDANÇA (leia antes de confirmar) ===",
                      "  Data 'Atualizado em': 21/10/2026  ->  22/10/2026"]), Spacer(1, 4),
                P("Se o texto não existir mais na página, o programa avisa <font face='Courier'>0 ocorrência(s)</font> "
                  "e não faz nada.", peq)])

    # ---------------------------------------------------------------- opção 7
    s += opcao(7, "Fazer backup agora",
               "Salva uma cópia da página atual na pasta <b>backups</b>, sem perguntar nada. Útil antes de uma edição "
               "grande, mesmo fora do fluxo normal (toda publicação já faz isso sozinha).",
               [digitar([("Escolha:", "<b>7</b>")]), Spacer(1, 4),
                tela(["Backup salvo em: ...\\backups\\pagina_2026-10-22_10h5421.html"])])

    # ---------------------------------------------------------------- opção 8
    s += opcao(8, "Restaurar um backup",
               "Mostra a lista de backups salvos; escolha o número para voltar o site àquela versão.",
               [digitar([("Escolha:", "<b>8</b>"), ("(lista de backups aparece)", ""),
                         ("Número do backup a restaurar:", "<b>1</b>")]), Spacer(1, 4),
                tela(["  1) pagina_2026-10-22_10h5421.html", "Número do backup a restaurar: ",
                      "Nenhuma mudança a aplicar."]), Spacer(1, 4),
                P("Neste exemplo o backup é idêntico à página atual (foi salvo um instante antes, sem nenhuma edição "
                  "no meio), por isso o programa avisa que não há nada para mudar &mdash; ele <b>nunca publica igual ao igual</b>. "
                  "No uso real, cada opção 3/4/5/6 confirmada já grava um backup sozinha antes de publicar; se uma dessas "
                  "mudanças sair errada, escolha o backup <b>de antes dela</b> na lista para desfazer.", peq)])

    s += [caixa("Pronto para usar de verdade?",
                ["O roteiro é idêntico fora do modo treino: abra <b>GERENCIAR_BLOG.bat</b> (ou GerenciarBlog.exe) em vez do "
                 "TREINAR.bat, com o <b>wp_credenciais.json</b> preenchido. As mesmas 8 opções, os mesmos resumos &mdash; só que "
                 "respondendo <b>s</b> a mudança vai para o site de verdade."], VERDE)]
    return s


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=2.3 * cm, rightMargin=2.3 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                            title="Manual de Treino - GerenciarBlog.exe", author="Blog comprenolink.net")
    doc.build(montar(), onFirstPage=lambda c, d: None, onLaterPages=rodape)
    # O pacote do outro PC leva só os painéis do navegador; este manual (menu/treino) fica só aqui
    print("PDF gerado:", SAIDA)


if __name__ == "__main__":
    main()
