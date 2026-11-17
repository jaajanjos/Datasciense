# -*- coding: utf-8 -*-
"""PDF para divulgar a análise crítica dos anúncios do blog (qualidade, quantidade/equilíbrio e forma de coleta).
Gera D:\\Projeto_Blog_Comprenolink\\Analise_Critica_Anuncios_2026-10-27.pdf.  Rodar:  python -X utf8 gerar_analise_critica.py
"""
import sys

sys.path.insert(0, r"D:\Projeto_Blog_Comprenolink\0- Pendencias\5_Plano_turbinar_anuncio_instagram")
from gerar_pdf_plano_turbinar import (AMARELO, AZUL_C, CINZA, CLARO, ESCURO, LARANJA, LARANJA_C, LARG, S, VERDE,  # noqa: E402
                                      VERDE_C, VERMELHO, VERMELHO_C, caixa, cartoes, tabela)
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

SAIDA = r"D:\Projeto_Blog_Comprenolink\Analise_Critica_Anuncios_2026-10-27.pdf"
CATS = [("Beleza & Saúde", 43), ("Bebê & Maternidade", 43), ("Áudio & TV", 17), ("Tecnologia & Informática", 17),
        ("Esporte & Fitness", 17), ("Casa & Eletrodomésticos", 17), ("Ferramentas & Utilidades", 16),
        ("Moda Infantil & Juvenil", 15), ("Casa, Cama & Decoração", 15)]


def rodape(c, doc):
    c.saveState()
    c.setFillColor(AMARELO)
    c.rect(0, A4[1] - 0.45 * cm, A4[0], 0.45 * cm, fill=1, stroke=0)
    c.setFont("Arial", 8)
    c.setFillColor(CINZA)
    c.drawString(1.8 * cm, 1.1 * cm, "Análise crítica dos anúncios – comprenolink.net  •  27/10/2026")
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


def barras():
    """Barras horizontais simples: categoria, barra proporcional e quantidade/percentual."""
    tot = sum(n for _, n in CATS)
    lb, lmax = LARG * 0.34, LARG * 0.5
    linhas, st = [], [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                      ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    for i, (nome, n) in enumerate(CATS):
        cor = VERMELHO if n >= 40 else (LARANJA if "Moda" in nome else VERDE)
        bar = Table([[""]], colWidths=[max(4, lmax * n / CATS[0][1])], rowHeights=[12])
        bar.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), cor)]))
        linhas.append([Paragraph(nome, S["cel"]), bar, Paragraph(f"<b>{n}</b> ({n / tot:.0%})", S["cel"])])
    t = Table(linhas, colWidths=[lb, lmax + 8, LARG - lb - lmax - 8])
    t.setStyle(TableStyle(st + [("ALIGN", (1, 0), (1, -1), "LEFT")]))
    return t


def montar():
    P = lambda t, e="p": Paragraph(t, S[e])
    st = [Spacer(1, 6.3 * cm),
          Paragraph("Análise Crítica dos Anúncios<br/>do Blog", S["capa_t"]), Spacer(1, 10),
          Paragraph("Qualidade, quantidade de opções e forma de coleta – conclusão e recomendações", S["capa_s"]),
          Spacer(1, 22),
          cartoes([("200", "produtos<br/>no blog"), ("9", "categorias"), ("40", "anúncios novos<br/>em 27/10"),
                   ("~30%", "do blog é<br/>bebê + infantil")]),
          Spacer(1, 18),
          caixa("<b>Em uma frase:</b> a <b>qualidade final</b> do blog está boa (produtos bem escolhidos e textos "
                "reescritos), mas a <b>coleta precisa de foco</b>: o blog ficou concentrado em bebê/infantil e beleza "
                "justamente antes da Black Friday, quando o que mais vende é tecnologia, TV e eletro."),
          Spacer(1, 12),
          tabela([
              ["Item", "Informação"],
              ["Blog", "comprenolink.net (afiliado Mercado Livre)"],
              ["Base da análise", "200 produtos publicados em 27/10/2026, incluindo os 40 anúncios novos (itens 161 a 200)"],
              ["Data", "27/10/2026"],
          ], [0.28, 0.72]),
          PageBreak()]

    # 1. qualidade
    st += [P("1. Qualidade dos anúncios que chegam", "h1"),
           P("<b>Veredito: os produtos são bons, o texto original é fraco.</b> Os itens coletados estão entre os mais "
             "vendidos e bem avaliados do Mercado Livre, com boas fotos e link de afiliado funcionando. Mas o texto que "
             "vem do anúncio não serve para o blog sem reescrita.", "p"),
           tabela([
               ["O que veio no anúncio original (40 novos)", "Quantos", "Problema (explicado)", "Como ficou no blog",
                "O que deve melhorar"],
               ["Selo genérico (\"Mais vendido.\", \"Melhor custo- beneficio\")", "40 de 40 (100%)",
                "<b>Todos os cartões ficam com o mesmo selo</b>, então o visitante não vê o que um produto tem de "
                "diferente do outro. E <b>\"custo-benefício\" é falar de preço</b> de forma indireta – a nossa regra é "
                "não falar de preço, porque o valor muda todo dia no Mercado Livre e a frase pode ficar falsa",
                "Selo com um fato do produto: \"12 Peças\", \"100% Algodão\", \"Toda em Couro\"",
                "<b>Na coleta:</b> preferir anúncio que mostre o diferencial (peças, material, potência, tamanho). "
                "<b>No texto:</b> o selo sempre traz 1 fato, nunca \"mais vendido\" ou \"custo-benefício\""],
               ["\"Ideal para\" vazio (\"Dia a dia!!\", \"Uso diário.\")", "40 de 40 (100%)",
                "Não responde à pergunta do visitante: <b>\"isso serve para mim?\"</b>",
                "Usos reais: \"Batizado\", \"Dias frios\", \"Escola\"",
                "Sempre <b>4 usos reais</b>: ocasião, para quem, época e lugar"],
               ["Sem descrição", "2 de 40", "Cartão incompleto, <b>sem argumento</b> para a pessoa clicar",
                "Descrição criada a partir do anúncio",
                "<b>Na coleta:</b> pular anúncio sem descrição quando houver outro parecido"],
               ["Texto de vendedor ou de preço (\"Olá mamãe!\", \"Barato Premium\")", "vários",
                "Parece <b>cópia do Mercado Livre</b> e fala de preço, o que tira a confiança no blog", "Removido",
                "Filtro automático procura \"preço\", \"barato\" e \"custo-benefício\" a cada rodada"],
               ["Nome longo com código, cor e tamanho repetidos", "vários", "O nome <b>corta no cartão</b>, "
                "principalmente no celular", "Nome de até 60 caracteres",
                "Nome = tipo + marca + diferencial (ex.: \"Tênis Bebê Menino Caramelo\")"],
           ], [0.19, 0.1, 0.27, 0.19, 0.25],
               extra=[("BACKGROUND", (1, 1), (1, 2), VERMELHO_C), ("BACKGROUND", (2, 1), (2, 1), LARANJA_C),
                      ("BACKGROUND", (4, 1), (4, -1), VERDE_C)]),
           Spacer(1, 8),
           caixa("<b>Conclusão da qualidade:</b> a reescrita é <b>obrigatória</b> e está funcionando – todos os 200 "
                 "cartões estão sem preço, sem promessas e com selo e \"Ideal para\" específicos.", VERDE_C, VERDE),
           PageBreak(),  # gráfico e tabela da seção 2 juntos na mesma página
           P("2. Quantidade e equilíbrio das opções", "h1"),
           P("Distribuição dos 200 produtos por categoria (vermelho = concentração alta):", "pq"),
           barras(), Spacer(1, 6),
           tabela([
               ["Ponto", "Situação", "Impacto (divergência do foco)", "Melhor solução"],
               ["Concentração", "Bebê + Moda Infantil = 58 de 200 (~30%); Beleza = 43 (22%)",
                "Bom para chá de bebê e Natal; fraco para Black Friday",
                "<b>Pausar a coleta de bebê/infantil até 01/12</b>; esses itens voltam ao destaque na página de Natal"],
               ["Categorias de Black Friday", "Tecnologia, Áudio & TV e Eletro com 17 cada",
                "Menos da metade de Bebê, justo onde a Black Friday mais vende",
                "<b>Coletar 5 a 10 por categoria até 15/11</b> (antes do teste do Turbinar) em Tecnologia, TV, Eletro e Ferramentas"],
               ["Opções repetidas", "12 sapatinhos, 3 da mesma marca (Bebê Mania)",
                "Muitas opções parecidas dificultam a escolha",
                "<b>Manter os 4 a 5 melhores de cada tipo</b> (mais vendidos e bem avaliados) e retirar os parecidos; o Claude indica quais"],
               ["Kits sortidos", "Vários itens \"cores e estampas sortidas\"",
                "Difícil comparar e mostrar exatamente o que a pessoa recebe",
                "<b>Preferir modelo definido</b>; quando for sortido, o texto deixa claro \"cores sortidas\""],
           ], [0.16, 0.25, 0.25, 0.34], extra=[("BACKGROUND", (3, 1), (3, -1), VERDE_C)]),
           PageBreak()]

    # 3. coleta
    st += [P("3. Forma de coleta", "h1"),
           P("<b>Funciona bem:</b> você coleta no Mercado Livre e o processo automático detecta, classifica, publica e "
             "valida – 40 anúncios numa rodada, com backup, sem quebrar nada e sem mudar produtos antigos de lugar.", "p"),
           tabela([
               ["Ponto fraco", "Por que foge do foco", "Melhor solução"],
               ["A coleta vem por <b>volume</b> (40 de uma vez, quase todos do mesmo nicho), e não por <b>objetivo</b>",
                "Enche o blog do que estava fácil de achar, não do que vende na data",
                "<b>Coletar por uma lista \"o que coletar\"</b> com meta por categoria e prazo (ex.: 10 de Tecnologia até 15/11)"],
               ["Cada rodada exige reescrever 100% dos textos e criar categorias",
                "Muito trabalho de uma vez e risco de erro de classificação",
                "<b>Lotes menores (10 a 15) e de 1 a 2 categorias por vez</b>; o Claude reescreve e publica no mesmo dia"],
               ["Acima de 300 produtos as páginas ficam longas",
                "O visitante se perde e não chega ao botão do Mercado Livre",
                "<b>Teto de cerca de 25 produtos por categoria</b>, subcategorias e um \"Top 5\" no topo de cada página"],
           ], [0.3, 0.3, 0.4], extra=[("BACKGROUND", (0, 0), (0, 0), VERMELHO), ("BACKGROUND", (2, 1), (2, -1), VERDE_C)]),
           P("4. Conclusão", "h1"),
           caixa("A <b>qualidade final do blog está boa</b>: os produtos são bem escolhidos e os textos são reescritos "
                 "dentro da política de venda (sem preço, sem promessas, com aviso de afiliado). Para virar "
                 "<b>venda</b>, porém, a <b>coleta precisa de foco</b>: hoje o blog está forte em bebê/infantil e beleza "
                 "e mais fraco nas categorias que mais vendem na Black Friday.", AZUL_C),
           P("5. Recomendações", "h1"),
           tabela([
               ["#", "Recomendação", "Quando", "Resultado esperado"],
               ["1", "<b>Priorizar Black Friday:</b> novos anúncios de Tecnologia, TV, Eletro e Ferramentas (5 a 10 por categoria)",
                "até 27/11", "Mais opções onde a Black Friday mais vende"],
               ["2", "<b>Pausar bebê e infantil:</b> com 58 itens o nicho está coberto; volta forte no Natal",
                "a partir de já", "Blog mais equilibrado"],
               ["3", "<b>Máximo 5 a 8 opções do mesmo tipo</b>, de marcas e faixas diferentes (ex.: 1 sapatilha, 1 tênis, 1 mocassim)",
                "toda coleta", "Escolha mais fácil para o visitante"],
               ["4", "<b>Preferir anúncio com descrição completa</b> e produto definido; evitar \"kit sortido\"",
                "toda coleta", "Texto mais preciso e fácil de comparar"],
               ["5", "<b>Revisar pelo painel em 30 dias:</b> coletar mais do que tem clique e venda, menos do que não tem",
                "fim de novembro", "Coleta guiada por resultado"],
           ], [0.05, 0.53, 0.15, 0.27]),
           Spacer(1, 10),
           P("Próximo passo sugerido", "h2"),
           P("Preparar uma <b>lista de \"o que coletar\" para a Black Friday</b>, com os tipos de produto que mais faltam em "
             "cada categoria, para orientar a próxima rodada de anúncios (a seção 6 já traz essa lista).", "p"),
           PageBreak()]
    return st + secao_categorias()


# ---------------------------------------------------------------- seção 6: categorias (retirar / incluir)
RETIRAR = [  # n, produto, motivo, quem fica no lugar
    (115, "Magnésio Dimalato 250 mg 120 Cápsulas", "3 dimalatos parecidos", "116 Dimalato 350 mg La San Day"),
    (117, "Dimagnésio Malato 1300 mg 60 Comprimidos", "3 dimalatos parecidos", "116 Dimalato 350 mg La San Day"),
    (119, "5 Magnésios Muwiz 120 Cápsulas", "2 produtos \"5 magnésios\" iguais", "118 Maltta 5 Magnésios"),
    (132, "Kit 3 Coenzima Q10 Ubiquinol 100 mg", "5 opções de coenzima Q10", "135 Ubiquinol Ecomev"),
    (136, "Coenzima Q10 200 mg 60 Doses", "5 opções de coenzima Q10", "134 Coenzima Q10 200 mg + Vit. E"),
    (121, "Ômega 3 EPA e DHA Vitafor 60 Cápsulas", "6 opções de ômega 3", "120, 122 e 123"),
    (137, "Licopeno 10 mg Recover Farma 30 Cápsulas", "3 licopenos", "138 Licopeno + Selênio e 139 (120 cáps.)"),
    (141, "Kit 2 Óleo de Semente de Abóbora Zuchetti", "repete o 140 (mesmo produto em dobro)", "140 Zuchetti 120 cáps."),
    (145, "Trocador de Fralda Dobrável Nuvem Azul", "4 trocadores parecidos", "144 Safari e 147 Anatômico"),
    (146, "Trocador de Fralda Portátil Coração Rosa", "4 trocadores parecidos", "144 Safari e 147 Anatômico"),
    (163, "Conjunto Bebê Body Manga Longa e Calça Mijão", "5 kits body + mijão", "161 (12 peças) e 173 (23 peças)"),
    (164, "Kit 6 Peças Bebê Canelado 3 Bodies e 3 Mijões", "5 kits body + mijão", "161 (12 peças) e 173 (23 peças)"),
    (179, "Tênis Bebê Mania Menina 71307", "3 itens da mesma marca", "175 Sapatilha Bebê Mania"),
    (181, "Sapatilha Bebê Mania Vermelha 31607", "3 itens da mesma marca", "175 Sapatilha Bebê Mania"),
    (183, "Tênis Bebê Menina Calce Fácil Rosa", "4 tênis de menina parecidos", "177 Dourado e 182 Sapatênis"),
    (186, "Tênis Bebê Menino Casual 2026", "2 tênis de menino parecidos", "185 Caramelo"),
    (180, "Botina Bebê Caipira Festa Junina", "fora de época (festa junina)", "volta em maio, se quiser"),
]
INCLUIR = [  # categoria, o que coletar, quantos, prioridade/prazo
    ("Tecnologia & Informática", "Tablet, Kindle/leitor digital, notebook intermediário (2 opções), celular Xiaomi ou iPhone, "
     "teclado e mouse sem fio de escritório", "6", "ALTA – até 15/11"),
    ("Áudio & TV", "Smart TV 43\" e 50\" 4K, Fire TV Stick/Chromecast, soundbar de marca, projetor (já existe a tela de "
     "projeção sem projetor)", "5", "ALTA – até 15/11"),
    ("Casa & Eletrodomésticos", "Air fryer grande (5 L ou mais), aspirador vertical ou robô, cafeteira de cápsula, "
     "liquidificador, ventilador (verão), Echo Dot/lâmpada inteligente", "6", "ALTA – até 15/11"),
    ("Ferramentas & Utilidades", "Trena a laser, nível, jogo de chaves, aspirador de pó para carro/casa (Limpeza), "
     "esmerilhadeira", "4", "MÉDIA – até 20/11"),
    ("Esporte & Fitness", "Tênis de corrida, bicicleta/patinete, tapete de yoga, garrafa/bolsa de academia", "4", "MÉDIA – até 20/11"),
    ("Beleza & Saúde", "Perfumes (3 a 4, os mais pedidos no Natal), secador e chapinha, barbeador, aparelho de pressão "
     "e balança (Saúde)", "6", "MÉDIA – até 30/11"),
    ("Casa, Cama & Decoração", "Decoração de Natal (árvore, pisca-pisca, toalha de mesa), kit de toalhas de banho", "3", "MÉDIA – até 30/11"),
    ("Moda Infantil & Juvenil", "Só meninos (hoje só 2 itens): conjuntos e bermudas", "3", "BAIXA – até 30/11"),
    ("Bebê & Maternidade", "Nada novo: pausar até 01/12", "0", "PAUSA"),
]
PANORAMA = [  # categoria, hoje, retirar, incluir
    ("Tecnologia & Informática", 17, 0, 6), ("Áudio & TV", 17, 0, 5), ("Casa & Eletrodomésticos", 17, 0, 6),
    ("Bebê & Maternidade", 43, 9, 0), ("Moda Infantil & Juvenil", 15, 0, 3), ("Casa, Cama & Decoração", 15, 0, 3),
    ("Ferramentas & Utilidades", 16, 0, 4), ("Esporte & Fitness", 17, 0, 4), ("Beleza & Saúde", 43, 8, 6),
]


def secao_categorias():
    P = lambda t, e="p": Paragraph(t, S[e])
    assert sum(1 for r in RETIRAR if r[0] >= 143) == 9 and sum(1 for r in RETIRAR if r[0] < 143) == 8
    linhas = [["Categoria", "Hoje", "Retirar", "Incluir", "Fica com", "Avaliação"]]
    extra = []
    for i, (c, hoje, r, inc) in enumerate(PANORAMA, 1):
        fim = hoje - r + inc
        aval = "Excesso – enxugar" if r else ("Pausar coleta" if c.startswith("Bebê") else
                                             ("Reforçar para a Black Friday" if inc >= 5 else "Completar"))
        linhas.append([f"<b>{c}</b>", str(hoje), f"-{r}" if r else "–", f"+{inc}" if inc else "–", f"<b>{fim}</b>", aval])
        if r:
            extra.append(("BACKGROUND", (2, i), (2, i), VERMELHO_C))
        if inc >= 5:
            extra.append(("BACKGROUND", (3, i), (3, i), VERDE_C))
    tot = (sum(p[1] for p in PANORAMA), sum(p[2] for p in PANORAMA), sum(p[3] for p in PANORAMA))
    linhas.append(["<b>TOTAL</b>", f"<b>{tot[0]}</b>", f"<b>-{tot[1]}</b>", f"<b>+{tot[2]}</b>",
                   f"<b>{tot[0] - tot[1] + tot[2]}</b>", "Blog mais equilibrado"])
    extra.append(("BACKGROUND", (0, len(linhas) - 1), (-1, len(linhas) - 1), AMARELO))
    st = [P("6. Categorias: quantidade, o que retirar e o que incluir", "h1"),
          P("<b>Minha opinião:</b> a <b>quantidade de categorias (9) está certa</b> – não precisa criar nem apagar "
            "categoria. O ajuste necessário é <b>dentro</b> delas: Bebê e Beleza & Saúde têm produtos repetidos demais, "
            "e as categorias que mais vendem na Black Friday têm de menos.", "p"),
          tabela(linhas, [0.27, 0.09, 0.1, 0.1, 0.11, 0.33], extra=extra),
          Spacer(1, 6),
          caixa("<b>Por que retirar?</b> Com 5 coenzimas Q10, 6 ômegas 3, 7 magnésios ou 12 sapatinhos, o visitante não "
                "consegue escolher e desiste. Ficando com os <b>2 a 3 melhores de cada tipo</b>, a página fica mais curta "
                "e cada produto recebe mais cliques. Nada se perde: o anúncio retirado continua no backup e pode voltar.",
                LARANJA_C, LARANJA),
          P("Subcategorias fracas (1 ou 2 produtos)", "h2"),
          tabela([
              ["Subcategoria", "Produtos", "Melhor solução"],
              ["Áudio & TV › Projeção", "1 (só a tela)", "<b>Incluir um projetor</b>; se não houver, juntar com TVs"],
              ["Casa & Eletro › Automação & Segurança", "1", "<b>Incluir</b> Echo Dot e lâmpada inteligente"],
              ["Ferramentas › Reparos & Vedação", "1", "<b>Juntar</b> com Ferramentas Manuais"],
              ["Ferramentas › Limpeza", "1", "<b>Incluir</b> aspirador (casa/carro)"],
              ["Esporte › Esportes & Lazer", "1", "<b>Incluir</b> bicicleta/patinete e tênis de corrida"],
              ["Esporte › Proteção & Suporte", "2", "Manter (completa com joelheira e tornozeleira)"],
              ["Beleza › Perfumes", "2", "<b>Incluir 3 a 4 perfumes</b> – é presente forte de Natal"],
              ["Beleza › Saúde", "1", "<b>Incluir</b> aparelho de pressão e balança, ou juntar com Cuidados Pessoais"],
              ["Moda Infantil › Meninos", "2", "<b>Incluir 3</b> itens de menino"],
          ], [0.38, 0.14, 0.48], extra=[("BACKGROUND", (2, 1), (2, -1), VERDE_C)]),
          PageBreak(),
          P(f"6.1 Sugestão de anúncios para retirar ({len(RETIRAR)} itens)", "h2"),
          P("Critério: dentro de cada grupo de produtos quase iguais, fica o mais completo ou o de marca mais conhecida. "
            "<b>Só retiro com a sua aprovação</b>, com backup antes.", "pq"),
          tabela([["Nº", "Produto a retirar", "Motivo", "Fica no lugar"]] +
                 [[str(n), nome, mot, fica] for n, nome, mot, fica in RETIRAR],
                 [0.07, 0.38, 0.27, 0.28], extra=[("BACKGROUND", (0, 1), (0, -1), VERMELHO_C)]),
          PageBreak(),
          P("6.2 O que incluir (lista \"o que coletar\")", "h2"),
          P("Ordem de prioridade: primeiro o que vende na Black Friday (até 15/11, antes do teste do Turbinar).", "pq"),
          tabela([["Categoria", "O que coletar", "Qtd.", "Prioridade / prazo"]] + [list(r) for r in INCLUIR],
                 [0.22, 0.5, 0.07, 0.21],
                 extra=[("BACKGROUND", (3, 1), (3, 3), VERDE_C), ("BACKGROUND", (3, 9), (3, 9), LARANJA_C)]),
          Spacer(1, 8),
          P("Opinião final sobre as categorias", "h2"),
          caixa("<b>1.</b> Manter as <b>9 categorias</b>. <b>2.</b> Retirar os <b>17 repetidos</b> (8 de suplementos e 9 de "
                "bebê). <b>3.</b> Incluir cerca de <b>37 anúncios</b>, 17 deles de Tecnologia, TV e Eletro até 15/11. "
                "<b>4.</b> Resultado: o blog vai de 200 para cerca de <b>220 produtos</b>, Bebê cai de 43 para 34 e todas "
                "as categorias de Black Friday passam de 20 opções.", VERDE_C, VERDE),
          Spacer(1, 6),
          P("Observação: <b>Beleza & Saúde</b> tem hoje 32 suplementos (vitaminas + magnésio). Se depois da limpeza ainda "
            "passar de 30, vale separar em duas categorias: \"Beleza & Perfumes\" e \"Vitaminas & Suplementos\".", "pq"),
          PageBreak()]
    return st + secao_sucesso()


# ---------------------------------------------------------------- seção 7: análise sincera de sucesso
def secao_sucesso():
    P = lambda t, e="p": Paragraph(t, S[e])
    return [
        P("7. Análise sincera: o blog vai ter sucesso?", "h1"),
        caixa("<b>Resposta direta:</b> o blog <b>pode</b> dar certo – a estrutura está acima da média dos blogs de "
              "afiliado. Mas <b>com a dinâmica de hoje, não vai</b>: o problema não é produto nem texto, é "
              "<b>falta de visitantes</b>. Hoje quase todo o esforço vai para colocar anúncio, e quase nada para trazer "
              "gente. É preciso inverter essa conta.", LARANJA_C, LARANJA),
        P("Os números reais até hoje", "h2"),
        tabela([
            ["Indicador", "Valor", "O que significa"],
            ["Ganho no ML Afiliados (180 dias)", "R$ 172,00", "cerca de R$ 29 por mês"],
            ["Vendas registradas (180 dias)", "19", "cerca de 3 por mês"],
            ["Cliques no link de afiliado (180 dias)", "116", "menos de 1 por dia"],
            ["Comissão média por venda", "R$ 9,05", "cada venda paga pouco: é preciso volume"],
            ["Visitas externas ao blog (painel de 22/10)", "quase zero", "o tráfego medido era quase todo de teste"],
            ["Seguidores no Instagram", "4", "perfil recém-criado (27/10)"],
            ["Venda vinda de busca no Google", "1 (26/10)", "<b>o Google já trouxe comprador sozinho</b> – é o melhor sinal"],
        ], [0.38, 0.17, 0.45]),
        Spacer(1, 6),
        P("Pontos fortes e pontos fracos (sem enfeite)", "h2"),
        tabela([
            ["Pontos fortes", "Pontos fracos"],
            ["200 produtos selecionados, textos dentro da política, 9 categorias e validação automática",
             "Tráfego quase nulo: sem visita, nenhum texto bom vende"],
            ["Automação pronta: categorias, Reels, posts, respostas no Direct e calendário",
             "Tempo gasto mais em cadastrar anúncio do que em divulgar"],
            ["Rastreio de cliques (UTM) e painel para medir o resultado",
             "Instagram e WhatsApp começando do zero (4 seguidores)"],
            ["Google já indexando (Search Console ligado em 27/10) e 1 venda orgânica",
             "Comissão baixa por venda (média R$ 9): precisa de muitas vendas"],
        ], [0.5, 0.5], extra=[("BACKGROUND", (0, 0), (0, 0), VERDE), ("BACKGROUND", (1, 0), (1, 0), VERMELHO)]),
        Spacer(1, 6),
        P("A conta que mostra o tamanho do desafio", "h2"),
        P("Estimativa simples para chegar a <b>R$ 1.000 por mês</b> de comissão (são suposições para dar a ordem de "
          "grandeza, não promessa):", "p"),
        tabela([
            ["Etapa", "Conta", "Resultado"],
            ["Vendas necessárias", "R$ 1.000 ÷ R$ 9 por venda", "<b>cerca de 110 vendas/mês</b>"],
            ["Cliques no Mercado Livre", "supondo que 3 a 5% dos cliques viram compra", "<b>2.200 a 3.700 cliques/mês</b>"],
            ["Visitas no blog", "supondo que 30% dos visitantes clicam em um produto", "<b>7.000 a 12.000 visitas/mês</b>"],
            ["Hoje", "116 cliques em 6 meses", "<b>precisamos de mais de 100 vezes os cliques de hoje</b>"],
        ], [0.25, 0.45, 0.3], extra=[("BACKGROUND", (2, 4), (2, 4), VERMELHO_C)]),
        PageBreak(),
        P("O que mudar na dinâmica (a nova regra 80/20)", "h2"),
        P("<b>80% do tempo em trazer visitantes, 20% em cadastrar produtos.</b> O catálogo já é grande o suficiente.", "p"),
        tabela([
            ["#", "Mudança", "Por que", "Meta"],
            ["1", "<b>Parar de coletar em volume</b>: só os ~37 da lista da seção 6.2 até 30/11",
             "200 produtos já bastam; o gargalo é tráfego", "Catálogo estável"],
            ["2", "<b>Artigos de comparação para o Google</b> (\"melhor air fryer 2026\", \"fone até X\") – o Claude escreve",
             "A única venda orgânica veio de busca; o Google traz visita todo dia, de graça", "2 artigos por semana"],
            ["3", "<b>Reels todo dia de post</b> + story, sem falhar", "É o que leva o perfil a quem não segue", "27 Reels até 23/12"],
            ["4", "<b>WhatsApp: Canal + Status</b> todo dia de post; grupos só onde é permitido", "Público próximo compra mais rápido",
             "100 seguidores no Canal até 31/12"],
            ["5", "<b>Turbinar só como teste</b> (R$ 30) e só se os números ficarem no verde", "Evita gastar sem retorno", "Decidir em 19/11"],
            ["6", "<b>Olhar o painel toda segunda</b> (15 min): visitas, cliques e vendas por origem", "Fazer mais do que funciona",
             "1 conversa por semana com o Claude"],
        ], [0.05, 0.43, 0.32, 0.2]),
        Spacer(1, 6),
        P("Metas para saber se está dando certo", "h2"),
        tabela([
            ["Mês", "Visitas externas", "Cliques no ML", "Vendas", "Se não bater"],
            ["Novembro 2026", "1.000", "300", "15", "Revisar Instagram e artigos"],
            ["Dezembro 2026", "2.000", "600", "30", "Rever o foco das categorias"],
            ["Janeiro 2027", "3.000", "900", "45", "<b>Reunião de decisão</b>: continuar, mudar ou pausar"],
        ], [0.18, 0.18, 0.16, 0.12, 0.36]),
        P("Metas sugeridas como referência de crescimento, não previsão. "
          "Os números do painel e do ML Afiliados dizem se estamos no caminho.", "pq"),
        Spacer(1, 6),
        P("Conclusão sincera", "h2"),
        caixa("O blog tem <b>uma base sólida</b>: bons produtos, textos corretos e muita coisa automatizada. Isso é o que a "
              "maioria dos blogs de afiliado não tem. Mas sucesso em blog de afiliado depende de <b>tráfego constante</b>, "
              "e hoje ele quase não existe. <b>Vamos conseguir se mudarmos a dinâmica</b>: menos cadastro de produto, "
              "mais divulgação todo dia (Google, Reels e WhatsApp), metas mensais e decisão com base nos números em "
              "janeiro de 2027. Se seguirmos assim por 90 dias, teremos uma resposta clara – com dados, não com achismo.",
              VERDE_C, VERDE),
        PageBreak()] + secao_investimento()


# ---------------------------------------------------------------- seção 8: investimento mensal estimado
def secao_investimento():
    P = lambda t, e="p": Paragraph(t, S[e])
    return [
        P("8. Investimento mensal estimado para melhorar a performance", "h1"),
        P("A maior parte do que melhora a performance é <b>gratuita</b> (Google, Reels, WhatsApp, artigos). O único "
          "gasto em dinheiro recomendado agora é o <b>anúncio pago (Turbinar)</b>, e só se os números ficarem no verde.", "p"),
        tabela([
            ["Item", "Por quê", "Para quê", "Quando", "Custo estimado"],
            ["<b>Turbinar – teste</b>", "Perfil novo alcança pouca gente sozinho",
             "Descobrir quanto custa cada visita vinda do Instagram", "seg 16/11 a qua 18/11/2026", "<b>R$ 30</b>"],
            ["<b>Turbinar – Black Friday</b>", "Semana em que as pessoas mais compram",
             "Levar visitas à página Black Friday (Top 10)", "sáb 21/11 a sex 27/11/2026<br/>(só se o teste der verde)",
             "<b>R$ 105</b>"],
            ["<b>Turbinar – Natal</b>", "Segunda maior época de compras",
             "Levar visitas à página Presentes de Natal", "sáb 05/12 a seg 14/12/2026<br/>(só se a BF se pagar)", "<b>R$ 100</b>"],
            ["Artigos de comparação para o Google", "O Google já trouxe 1 comprador sozinho",
             "Visitas todos os dias, sem pagar anúncio", "2 por semana, a partir de 02/11", "R$ 0 (o Claude escreve)"],
            ["Reels, posts e stories", "Alcance de quem ainda não segue o perfil",
             "Crescer seguidores e cliques no link da bio", "todo dia de post, 02/11 a 23/12", "R$ 0 (já prontos)"],
            ["WhatsApp Business (Canal e Status)", "Quem já conhece compra mais rápido",
             "Divulgar ofertas para contatos e seguidores do Canal", "todo dia de post", "R$ 0"],
            ["ManyChat (resposta automática no Direct)", "Responder \"BLACK\" na hora, sem esforço",
             "Entregar o link para quem comenta", "já ativo", "R$ 0 (plano Free)"],
            ["Search Console e painel do blog", "Medir o que funciona", "Decidir com números", "toda segunda",
             "R$ 0"],
            ["Hospedagem e domínio (Hostinger)", "Manter o blog no ar", "Site funcionando",
             "conferir a data de renovação no painel Hostinger", "já existente (não é gasto novo)"],
        ], [0.2, 0.21, 0.23, 0.2, 0.16],
            extra=[("BACKGROUND", (4, 1), (4, 3), LARANJA_C), ("BACKGROUND", (4, 4), (4, 8), VERDE_C)]),
        Spacer(1, 8),
        KeepTogether([  # resumo inteiro numa página só
        P("Resumo por mês", "h2"),
            tabela([
                ["Mês", "O que é pago", "Mínimo", "Máximo", "Decisão"],
                ["Outubro 2026", "nada", "R$ 0", "R$ 0", "–"],
                ["Novembro 2026", "Teste (R$ 30) + Black Friday (R$ 105)", "R$ 30", "R$ 135", "qui 19/11 – segue ou para"],
                ["Dezembro 2026", "Natal (R$ 100)", "R$ 0", "R$ 100", "seg 30/11 – faz ou não o Natal"],
                ["Janeiro 2027", "nada previsto", "R$ 0", "R$ 0", "reunião de decisão com os números"],
                ["<b>TOTAL</b>", "", "<b>R$ 30</b>", "<b>R$ 235</b>", "nunca passa disso sem nova reunião"],
            ], [0.16, 0.34, 0.12, 0.12, 0.26], extra=[("BACKGROUND", (0, 5), (-1, 5), AMARELO)])]),
        Spacer(1, 8),
        P("O que NÃO recomendo pagar agora", "h2"),
        tabela([
            ["Item", "Custo", "Por que não agora"],
            ["ManyChat Pro (automação em qualquer post)", "US$ 149/mês (valor mostrado na tela do ManyChat)",
             "Caro para o resultado atual; o plano Free + respostas salvas resolvem"],
            ["Google Ads (anúncio no Google)", "variável", "Comissão média de R$ 9 por venda não paga o clique"],
            ["Comprar seguidores ou curtidas", "–", "Proibido pelo Instagram e derruba o alcance"],
            ["Ferramentas de design ou de SEO pagas", "–", "As artes e os textos já são gerados; o Search Console é grátis"],
        ], [0.34, 0.26, 0.4], extra=[("BACKGROUND", (0, 0), (-1, 0), VERMELHO)]),
        Spacer(1, 8),
        caixa("<b>Conclusão do investimento:</b> o plano custa de <b>R$ 30 a R$ 235 no total</b>, entre novembro e "
              "dezembro de 2026, e cada etapa só acontece se a anterior der resultado. O investimento principal é "
              "<b>tempo e constância</b> (cerca de 10 minutos por dia de post + 15 minutos às segundas), não dinheiro.",
              VERDE_C, VERDE),
        P("Valores do Turbinar conforme o Plano Turbinar Instagram 2026. O preço do ManyChat Pro é o que apareceu na "
          "tela de cadastro em 27/10/2026 e pode mudar.", "pq")]


if __name__ == "__main__":
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm,
                            bottomMargin=1.8 * cm, title="Análise crítica dos anúncios – comprenolink", author="comprenolink.net")
    doc.build(montar(), onFirstPage=capa, onLaterPages=rodape)
    print("PDF:", SAIDA)
