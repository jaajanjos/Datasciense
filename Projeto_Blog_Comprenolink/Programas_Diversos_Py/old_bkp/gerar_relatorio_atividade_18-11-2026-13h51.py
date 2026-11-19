# -*- coding: utf-8 -*-
"""RELATÓRIO DE ATIVIDADES do Claude no blog comprenolink.net / Instagram @compre.no.link (formato diário de bordo).
Rodar:  python -X utf8 gerar_relatorio_atividade.py
Saida: D:/Projeto_Blog_Comprenolink/0- Pendencias/4_Relatorio_Ativ_Claude_no_Blog/RELATORIO_ATIVIDADE_CLAUDE_BLOG_DD_MM_AAAA_HHhMM.pdf

REGRA DO DONO (29/10/2026): gerar/atualizar SEMPRE ao fim de cada sessão/agendamento: o que foi EXECUTADO (data e hora),
o que NÃO foi executado, o MOTIVO e a NOVA DATA para reexecutar. Pendência não espera um mês: propor a data mais próxima.
Atualize ATIVIDADES e REEXECUCAO abaixo antes de rodar. Hora só entra quando conhecida (relógio da sessão ou data do arquivo).
"""
import os
import sys
from datetime import date, datetime, timedelta

sys.path.insert(0, r"D:\Projeto_Blog_Comprenolink\0- Pendencias\5_Plano_turbinar_anuncio_instagram")
from gerar_pdf_plano_turbinar import (AMARELO, AZUL_C, CINZA, CLARO, ESCURO, LARANJA, LARANJA_C, S, VERDE,  # noqa: E402
                                      VERDE_C, VERMELHO, VERMELHO_C)
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4, landscape  # noqa: E402
from reportlab.lib.styles import ParagraphStyle  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

AGORA = datetime.now()
SAIDA = rf"D:/Projeto_Blog_Comprenolink/0- Pendencias/4_Relatorio_Ativ_Claude_no_Blog/RELATORIO_ATIVIDADE_CLAUDE_BLOG_{AGORA:%d_%m_%Y_%Hh%M}.pdf"
W, H = landscape(A4)
LARG = W - 3 * cm
AZUL = colors.HexColor("#0369A1")
P = lambda t, e="pq": Paragraph(t, S[e])  # noqa: E731
TXT = ParagraphStyle("txt", fontName="Arial", fontSize=9.6, leading=13.4, textColor=ESCURO)

EX, PA, NE = "EXECUTADO", "PARCIAL", "NÃO EXECUTADO"
COR = {EX: (VERDE, VERDE_C), PA: (LARANJA, LARANJA_C), NE: (VERMELHO, VERMELHO_C)}

# (data, hora, atividade, situação, o que foi feito / evidência, motivo (se não executado), nova data para reexecutar)
ATIVIDADES = [
    ('18/11',
     '10:06',
     'Relatório diário de gráficos do anúncio Meta (rotina 10:00): pulado pela regra de saldo; depois refeito por pedido do dono',
     EX,
     'Às 10:06 a rotina aplicou a regra de saldo (anúncio Concluído, saldo R$ 0,33, 260 visitas sem novidade) e não gerou PDF. Por pedido do dono, às ~10:18 foi executado o fluxo completo ignorando a regra: leitura no Gerenciador de Anúncios (Chrome), histórico atualizado e gerado Graficos_Metas_Anuncios_18-11-26_10h18.pdf (5 páginas; cópia no OneDrive). Meta sem mudança desde 16/11: gasto R$ 49,67, 3.335 impressões, 247 cliques no link, Concluído. Dados do site são de 17/11 (último acessos_ disponível).',
     'A Meta mostra aviso: limite de gastos da conta quase atingido (anúncios deixarão de ser exibidos se subir o gasto): é decisão do dono, não alterado. Nada alterado na Meta nem no site.',
     'Todo dia 10:00 (pula se concluído, sem saldo e sem visita nova); pedido do dono "gere Graficos_Metas_Anuncios" força a geração.'),
    ('18/11',
     '10:55 a 11:25',
     'Substituição automática de anúncios fora do normal por itens de Áudio e TV (pedido do dono), com validação, PDFs e painel atualizados',
     EX,
     'Verificação no ML (213 anúncios): 2 pausados (item 67 Cabeceira Queen Dubai e item 181 Aspirador Electrolux Ergorapido). Nenhum estava em pacote do Instagram/WhatsApp, então não houve reel a refazer nem agendamento. Substitutos escolhidos no ranking de mais vendidos de Eletrônicos, Áudio e Vídeo do ML (pulando o que o guia já tinha): item 67 -> Suporte TV Fixo Universal 10 a 100 pol (loja oficial PAROSFLUX, nota 4,8, +250 mil vendas, meli.la/2LCQQT3); item 181 -> Fone Bluetooth Soundcore P30i da Anker (loja oficial, nota 4,9, +10 mil vendas, meli.la/2HTGEdD). Links validados abrindo o meli.la (1º cartão com o produto novo, sem pausado); troca pelo gerenciar_blog (nome, título, foto, descrição, benefícios, Ideal para, selo -, sem preço) com backup da página; verificar_sem_preco OK; categorias atualizadas; historico_substituicoes.csv registrado; 0_executar_tudo --sem-claude regerado: 213 de 213 ativos, 0 pendentes; Painel_conversao_performance_2026-11-18_11h21.pdf gerado e copiado ao OneDrive.',
     'O ranking usado é o geral do ML (não há ranking de afiliados em Áudio e TV: sem vendas de eletrônicos na base). O item 67 é acessório de TV (suporte); comissão exibida 5%. Cache do site pode levar minutos. Validar link e produto (dono).',
     'Nada a reexecutar. Reels: só se um item fora do ar estiver em pacote (não é o caso hoje); próximo dia útil após 20:00 pela rotina.'),
    ('18/11',
     '10:10 a 10:20',
     'Tarefas novas pedidas pelo dono: aviso diário do Pixel (10:22) e relatório das atividades da manhã (12:20); formato da lista com status e responsabilidade',
     EX,
     'Criadas pixel-meta-evolucao-diaria (todo dia, até 15/12; lê PageView e SaidaML do Pixel 1128603339935423, registra em pixel_evolucao.csv) e relatorio-atividades-manha (todo dia, gera este PDF com o que rodou de 06:00 a 12:00). Formato "liste atividades de hoje" passou a trazer hora real, status e responsabilidade (memória atualizada).',
     'O aviso do Pixel de 18/11 ainda não tinha rodado quando este relatório foi gerado (10:22) e dirá "Pixel ainda não ativado": a ativação é hoje às 20:05. Tarefas só rodam com PC, app Claude e Chrome ligados.',
     'Hoje 10:22 aviso do Pixel; 12:20 relatório da manhã; 20:00 conferência da página 752; 20:05 ativação do Pixel; 20:20 baseline de velocidade.'),
    ('18/11',
     '10:22',
     'Aviso diário do Pixel da Meta (rotina 10:22): Pixel ainda não ativado, sem leitura na Meta',
     EX,
     'Rotina rodou com sucesso: o snippet 12 do Pixel está inativo, então não foi aberta a Meta nem gravado nada no pixel_evolucao.csv. Comportamento esperado antes da ativação.',
     'Nada alterado na Meta nem no site. Relatório das 12:10 conferiu as rotinas da manhã (gráficos e Pixel): nenhuma falhou, nada a corrigir.',
     'Ativação hoje às 20:05; aviso do Pixel volta a rodar amanhã 10:22 já com dados.'),
    ('18/11', '13:49', 'Pendência de 13/11 corrigida: descrição da página Política de Privacidade e conferência de Contato, Sobre e da cópia Celular_Whatsapp', EX,
     'Contato e Sobre já tinham descrição própria e um único H1. Privacidade ganhou descrição própria pelo AIOSEO (backup pagina3_privacidade_2026-11-18_13h49_antes_metadesc.json) e já aparece no site. Cópia Celular_Whatsapp de 09/12, 11/12 e 14/12 conferida: idêntica à pasta de divulgação.', '', ''),
]

FALTA_AGENDAR = [
    ("18/12", "Máquina de Cortar Cabelo e Barba Sem Fio Nixzen"), ("21/12", "Jogo de Lençol Casal Percal 600 Fios 4 Peças"),
    ("23/12", "Cortina de LED 3x3 m com 300 Luzes e Controle"),
]

# (quando, quem, o que, ganho / observação) – sempre a data mais cedo possível
REEXECUCAO = [
    ('hoje 18/11, 20:00', 'Claude', 'BF/Natal 2: conferir o rascunho 752 (Áudio e TV + Kit Bermudas) e os 5 links, sem publicar', 'Tarefa agendada; precisa de PC, app Claude e Chrome ligados'),
    ('hoje 18/11, 20:05', 'Claude', 'Ativar o Pixel da Meta (snippet 12), testar PageView e SaidaML e registrar', 'Sem Pixel ativo a Meta não aprende; teste no Gerenciador de Eventos'),
    ('hoje 18/11, 20:20', 'Claude', 'Baseline de saída por página e PageSpeed (só leitura)', 'Linha de base das melhorias do blog'),
    ('hoje 18/11', 'Dono', 'Validar link e produto dos itens 67 (Suporte de TV) e 181 (Fone Soundcore P30i)', 'Troca feita e conferida pelo Claude; falta o OK do dono'),
    ('até sex 20/11', 'Dono', 'Limite de gastos da conta Meta (quase atingido) e comissão dos 5 itens da página 752 no painel do ML', 'Sem o limite ajustado o anúncio pago não roda; aviso automático 20/11 09:00'),
    ('até seg 23/11, 12:00', 'Dono', 'Decidir o anúncio da Black Friday (campanha Vendas + SaidaML; o dono publica)', 'Aviso automático 23/11 09:00'),
    ('sem data (quando puder)', 'Dono', 'Apagar os 16 itens de produto do catálogo do WhatsApp Business (o catálogo é só de categorias)', 'Exige o login do dono no WhatsApp Business; o Claude não entra. Avise quando apagar'),
    ('a decidir', 'Dono', 'Frase "dieta e alimentação leve" na legenda da Air Fryer (11/11) e foto da LG (26/11), que traz "melhor" na imagem do fabricante', 'Alegações leves que ainda não foram decididas (política de anúncios)'),
]

OBSERVACOES = [
    "As tarefas agendadas só rodam com o PC, o app Claude e o Chrome ligados.",
]


def tabela(cab, linhas, larguras, cor=ESCURO, col_situacao=None):
    dados = [[P(f"<b>{c}</b>", "cab") for c in cab]] + [[P(str(c)) for c in l] for l in linhas]
    t = Table(dados, colWidths=[LARG * w for w in larguras], repeatRows=1)
    st = [("BACKGROUND", (0, 0), (-1, 0), cor), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#D1D5DB")),
          ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    for r in range(2, len(dados), 2):
        st.append(("BACKGROUND", (0, r), (-1, r), CLARO))
    if col_situacao is not None:
        for r, l in enumerate(linhas, 1):
            st.append(("BACKGROUND", (col_situacao, r), (col_situacao, r), COR[l[col_situacao]][1]))
    t.setStyle(TableStyle(st))
    return t


def cab_rod(c, doc):
    c.saveState()
    c.setFillColor(ESCURO)
    c.rect(0, H - 1.7 * cm, W, 1.7 * cm, fill=1, stroke=0)
    c.setFillColor(AMARELO)
    c.rect(0, H - 1.82 * cm, W, 0.12 * cm, fill=1, stroke=0)
    c.setFont("Arial-B", 15)
    c.drawString(1.5 * cm, H - 1.1 * cm, "Relatório de atividades do Claude (diário de bordo) – blog comprenolink.net")
    c.setFont("Arial", 9.5)
    c.setFillColor(colors.white)
    c.drawRightString(W - 1.5 * cm, H - 1.1 * cm, f"atualizado em {AGORA:%d/%m/%Y} às {AGORA:%H:%M}")
    c.setFont("Arial", 8)
    c.setFillColor(CINZA)
    c.drawString(1.5 * cm, 0.8 * cm, "Blog comprenolink.net  •  Instagram @compre.no.link  •  WhatsApp (11) 99495-9657")
    c.drawRightString(W - 1.5 * cm, 0.8 * cm, f"Página {doc.page}")
    c.restoreState()


def painel():
    n = {k: sum(1 for a in ATIVIDADES if a[3] == k) for k in COR}

    def c(v, rot, cor):
        return Paragraph(f"<font size=20><b>{v}</b></font><br/><font size=9>{rot}</font>",
                         ParagraphStyle("pn", parent=TXT, alignment=1, textColor=cor, leading=22))
    t = Table([[c(n[EX], "executadas", VERDE), c(n[PA], "parciais", LARANJA), c(n[NE], "não executadas", VERMELHO),
                c(len(FALTA_AGENDAR), "dias ainda sem agendar", AZUL)]], colWidths=[LARG / 4] * 4)
    t.setStyle(TableStyle([("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")), ("INNERGRID", (0, 0), (-1, -1), 0.3, colors.HexColor("#D1D5DB")),
                           ("BACKGROUND", (0, 0), (0, 0), VERDE_C), ("BACKGROUND", (1, 0), (1, 0), LARANJA_C), ("BACKGROUND", (2, 0), (2, 0), VERMELHO_C),
                           ("BACKGROUND", (3, 0), (3, 0), AZUL_C), ("TOPPADDING", (0, 0), (-1, -1), 8), ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def abre(d):
    dd, mm = d.split("/")
    j = date(2026, int(mm), int(dd)) - timedelta(days=29)
    return f"{j:%d/%m} ~20:00"


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=(W, H), leftMargin=1.5 * cm, rightMargin=1.5 * cm, topMargin=2.4 * cm, bottomMargin=1.5 * cm,
                            title="Relatório de atividades do Claude – blog", author="comprenolink.net")
    nao = [a for a in ATIVIDADES if a[3] in (NE, PA)]
    st = [painel(), Spacer(1, 8),
          Paragraph("<b>Como ler.</b> Cada linha é uma atividade em ordem de data e hora. A coluna <b>Situação</b> diz se foi executada, parcial ou não executada; "
                    "quando não foi, o <b>motivo</b> e a <b>nova data</b> aparecem na mesma linha. Nada espera um mês: a seção 3 mostra a data mais próxima possível "
                    "de cada reexecução.", TXT),
          Spacer(1, 8), P("1. Diário de bordo (cronológico)", "h2"),
          tabela(["Data", "Hora", "Atividade", "Situação", "O que foi feito / evidência", "Motivo (se não executado)", "Reexecução"],
                 [list(a) for a in ATIVIDADES], [0.05, 0.08, 0.20, 0.09, 0.25, 0.20, 0.13], col_situacao=3),
          PageBreak(), P("2. O que não foi executado (ou ficou parcial): motivo e nova data", "h2"),
          tabela(["Data", "Atividade", "Situação", "Motivo", "Nova data para reexecutar"],
                 [[a[0], a[2], a[3], a[5], a[6]] for a in nao], [0.05, 0.28, 0.09, 0.32, 0.26], cor=VERMELHO, col_situacao=2),
          PageBreak(), P("3. Plano de reexecução: a data mais cedo possível", "h2"),
          tabela(["Quando", "Quem", "O que", "Ganho / observação"], [list(r) for r in REEXECUCAO], [0.17, 0.10, 0.38, 0.35], cor=LARANJA),
          Spacer(1, 10), P("4. Dias de post sem agendamento: quando o Instagram libera (limite de 29 dias, vale também para o Business Suite)", "h2"),
          Paragraph("O Business Suite tem o mesmo limite de 29 dias, então este é o caminho. Cada dia abre cerca de 1 hora depois das 19:00 do dia indicado (testado em 29/10: aceitou 18:00 e recusou 18:30 às 19:15); o Reels de 19:05 abre 5 minutos depois.", TXT),
          Spacer(1, 4),
          tabela(["Dia de post", "Produto", "Pode agendar a partir de", "Situação"],
                 [[d, p_, abre(d), "pendente"] for d, p_ in FALTA_AGENDAR], [0.12, 0.46, 0.2, 0.22], cor=AZUL),
          PageBreak(), P("5. Observações e riscos", "h2")]
    for o in OBSERVACOES:
        st += [Paragraph("• " + o, TXT), Spacer(1, 4)]
    st += [Spacer(1, 6), P("6. Regra permanente", "h2"),
           Paragraph("Por pedido do dono (29/10/2026), o Claude atualiza este relatório sempre que concluir uma sessão de trabalho ou de agendamento, "
                     "com o nome <b>RELATORIO_ATIVIDADE_CLAUDE_BLOG_DD_MM_AAAA_HHhMM.pdf</b> em <b>D:\\Projeto_Blog_Comprenolink</b>: o que foi executado (data e hora), "
                     "o que não foi, o motivo e a nova data. Gerador: D:\\Projeto_Blog_Comprenolink\\0- Pendencias\\gerar_relatorio_atividade.py.", TXT)]
    doc.build(st, onFirstPage=cab_rod, onLaterPages=cab_rod)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
