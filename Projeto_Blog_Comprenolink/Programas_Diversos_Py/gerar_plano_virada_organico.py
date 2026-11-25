# -*- coding: utf-8 -*-
r"""gerar_plano_virada_organico.py  (criado em 24/11/2026 a pedido do dono)

PARA QUE SERVE: gera o PDF "PLANO_VIRADA_ORGANICO_DD_MM_AAAA_HHhMM.pdf" com todas as atividades da virada
do anúncio pago para o orgânico (a partir de dom 29/11/2026), no formato fixo de lista de atividades:
Atividade | Dia e horário | Próximas datas | Quem executa | Conversa de apoio.
Saída: D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias (fica só 1 versão; as antigas vão para old_bkp).
Uso: python -X utf8 "D:\Projeto_Blog_Comprenolink\Programas_Diversos_Py\gerar_plano_virada_organico.py"
"""
import datetime as dt
import glob
import os
import shutil

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias"

DECISOES = [
    "OBJETIVO: buscar VENDA com calma, mas com constância, custo zero em dinheiro. Venda do orgânico é hipótese: medir antes de aumentar o esforço.",
    "Nunca mais anúncio pago (Meta ou outro). Depois do bf_26_entrada, todo o processo fica no orgânico para sempre.",
    "O anúncio bf_26_entrada segue até o fechamento de sáb 28/11 às 10:00. Sem venda vinda do anúncio, é PAUSADO (só pausar; a Meta só cobra o que já foi gasto). Com venda, vai até 22/12 e não renova. A troca da arte para Natal foi CANCELADA.",
    "PLANO REFORMULADO (de acordo do dono em 24/11): Reels em RAMPA, com 2 por dia na fase 1; 3 por dia na fase 2 só com uso do plano Claude abaixo de 60% e cliques subindo; 5 por dia só com evidência.",
    "Medição sem custo pelo rastreador do blog (cliques para o Mercado Livre), em 3 leituras: seg 30/11, 07/12 e 14/12. Decisão de continuar ou reduzir em 14/12, olhando a TENDÊNCIA.",
    "Linha de confiança aprovada: \"Você compra direto no site oficial do Mercado Livre. O CompreNoLink só indica os produtos: o pagamento e a entrega são feitos pelo próprio Mercado Livre.\" Link da bio do Instagram com etiqueta (utm_medium=bio, utm_campaign=organico_reels).",
    "A conversa Execução orquestra e pode ajustar o plano a qualquer momento, alinhando todas as conversas. Só mudam com o dono: anúncio pago (nunca), WhatsApp, gasto de dinheiro, ações irreversíveis, conteúdo fora da política.",
    "Uso do Claude (plano Pro, sem extra): antes de atividade pesada, conferir o uso; acima de 75% da janela de 5 h ou 80% da semana, adiar. Atividades de conversas diferentes com pelo menos 30 min de folga. Coordenação mínima: 1 linha só às segundas.",
]

# Atividade | Dia e horário | Próximas datas | Quem executa | Conversa de apoio | Para que serve
ATIVIDADES = [
    ("Colocar a etiqueta no link da bio do Instagram (utm_source=instagram&utm_medium=bio&utm_campaign=organico_reels)", "até sáb 28/11",
     "-", "Claude (autorizado pelo dono)", "BLOG- Ajustes no WhatsApp e Instagram", "saber exatamente quantas visitas e cliques os Reels trazem"),
    ("Gerar e agendar os Reels da FASE 1: 2 por dia a partir de 29/11, no novo estilo visual", "antes de dom 29/11 (horário pela Execução)",
     "lotes semanais", "Claude + dono (dono escolhe o arquivo)", "BLOG- Ajustes no WhatsApp e Instagram", "começar o orgânico sem sobrecarregar o dono nem o plano"),
    ("FECHAMENTO do anúncio: somar 20/11 a 28/11, conferir vendas no ML Afiliados; 0 venda = PAUSAR. Junto: linha de base do orgânico de 16 a 28/11, sem o anúncio",
     "sáb 28/11 10h00 (tarefa fechamento-anuncio-28-11)", "-", "Claude (automático; dono avisado até 10h30)",
     "1- PY- Prog gerador gráfico de anúncio META - BLOG", "parar de gastar se não vende e ter com o que comparar"),
    ("Publicar a linha de confiança no topo das categorias e do guia", "dom 29/11 09h00 (tarefa linha-confianca-blog-29-11)", "-",
     "Claude (automático; conferida até 09h30)", "1- PY- Prog gerador gráfico de anúncio META - BLOG", "tirar o medo de golpe e fazer comprar pelo link (comissão conta)"),
    ("INÍCIO do orgânico: 2 Reels por dia no Instagram (Facebook só sincronizando os bons; WhatsApp fora)", "dom 29/11", "todos os dias",
     "Meta (agendado)", "BLOG- Ajustes no WhatsApp e Instagram", "mais gente vendo os produtos, sem custo"),
    ("LEITURA 1 do orgânico: cliques para o ML por origem (7 dias x linha de base), sem Meta e sem Chrome", "seg 30/11 20h35 (Execução aciona)",
     "-", "Claude (1 linha para a Execução)", "1- PY- Prog gerador gráfico de anúncio META - BLOG", "ver se os cliques começam a subir"),
    ("Relatório geral da semana e linha de cada conversa (fez / pendente / precisa do dono)", "seg 30/11 21h00", "toda segunda",
     "Claude", "BLOG - Execução de atividades e planejamento", "dono vê tudo num lugar só"),
    ("Ajustar as tarefas que dependem do anúncio ligado (30/11, 17/12, 22/12, 28/12)", "seg 30/11, conforme o fechamento", "-",
     "Claude propõe, dono aprova", "BLOG - Execução de atividades e planejamento", "não rodar checagens de um anúncio pausado"),
    ("Melhoria M2: 'Links verificados em DD/MM' nas categorias e no guia", "qua 02/12 20h00 (já agendada)", "-", "Claude",
     "BLOG - Execução de atividades e planejamento", "mais confiança: mostra que os links são conferidos"),
    ("LEITURA 2 do orgânico + decisão da FASE 2 (3 Reels por dia só se uso < 60% e cliques subindo)", "seg 07/12 20h35 (Execução aciona)", "-",
     "Claude (leitura) / Execução + dono (decisão)", "1- PY- Prog gerador gráfico de anúncio META - BLOG", "aumentar o esforço só com evidência"),
    ("Melhoria M6: bloco 'quem somos e como escolhemos' nas categorias (precisa do texto do dono)", "sex 11/12 20h00 (já agendada)", "-",
     "Claude + texto do dono", "BLOG - Execução de atividades e planejamento", "mais confiança para comprar pelo link"),
    ("LEITURA 3 do orgânico + DECISÃO: continuar, aumentar ou reduzir (olhando a tendência das 3 leituras)", "seg 14/12 20h35 (Execução aciona)", "-",
     "Claude (leitura) / dono decide", "BLOG - Execução de atividades e planejamento", "não gastar esforço em algo que não traz clique nem venda"),
    ("Resumo final do anúncio pago (gasto, visitas, cliques, vendas e comissão)", "seg 28/12 20h30 (tarefa bfnatal-7)", "-", "Claude",
     "BLOG - Execução de atividades e planejamento", "fechar o capítulo do anúncio pago com números"),
    ("Replanejar e melhorar as artes dos Reels com os dados do orgânico", "seg 11/01/2027 20h00 (já agendada)", "-", "Claude propõe, dono aprova",
     "BLOG - Execução de atividades e planejamento", "Reels mais fortes em 2027"),
]

ATENCAO = [
    "Os Reels de 29/11 em diante ainda precisam ser gerados e agendados com o dono antes de domingo; sem isso, o orgânico começa sem Reels.",
    "No começo os números são pequenos (poucos cliques por semana): uma semana ruim isolada não decide; vale a tendência das 3 leituras (30/11, 07/12, 14/12).",
    "Venda do ML Afiliados aparece com atraso de 1 a 2 dias e é paga cerca de 60 dias depois; parte pode não confirmar.",
    "Sábado 28/11 e domingo 29/11 têm tarefas automáticas: deixar o PC acordado e o app do Claude e o Chrome abertos.",
    "Até o fechamento de 28/11, nenhuma conversa gasta tokens com o sistema do anúncio pago (leituras da Meta, gráficos extras, checagens).",
]


def main():
    agora = dt.datetime.now()
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    for a in glob.glob(os.path.join(PASTA, "PLANO_VIRADA_ORGANICO_*.pdf")):
        shutil.move(a, os.path.join(PASTA, "old_bkp", os.path.basename(a)))
    saida = os.path.join(PASTA, f"PLANO_VIRADA_ORGANICO_{agora:%d_%m_%Y_%Hh%M}.pdf")
    s = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=s["Title"], fontSize=17)
    h2 = ParagraphStyle("h2", parent=s["Heading2"], fontSize=12, spaceBefore=8)
    p = ParagraphStyle("p", parent=s["BodyText"], fontSize=9.5, leading=13)
    c = ParagraphStyle("c", parent=s["BodyText"], fontSize=8, leading=10)
    cb = ParagraphStyle("cb", parent=c, textColor=colors.white)
    doc = SimpleDocTemplate(saida, pagesize=landscape(A4), leftMargin=1.2 * cm, rightMargin=1.2 * cm,
                            topMargin=1.2 * cm, bottomMargin=1.2 * cm, title="Plano da virada para o orgânico")
    cab = ["Atividade", "Dia e horário", "Próximas datas", "Quem executa", "Conversa de apoio", "Para que serve"]
    dados = [[Paragraph(x, cb) for x in cab]] + [[Paragraph(x, c) for x in linha] for linha in ATIVIDADES]
    t = Table(dados, colWidths=[7.6 * cm, 4.2 * cm, 2.8 * cm, 3.4 * cm, 4.2 * cm, 4.9 * cm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")), ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("PADDING", (0, 0), (-1, -1), 3),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")])]))
    e = [Paragraph("Plano da virada: do anúncio pago para o orgânico (a partir de 29/11/2026) – plano reformulado", h1),
         Paragraph(f"Gerado em {agora:%d/%m/%Y às %Hh%M}. Para que serve: mostrar, em ordem, tudo o que precisa acontecer para a "
                   f"estratégia orgânica começar no domingo 29/11, quem faz cada coisa e para quê.", p),
         Paragraph("Decisões do dono e plano vigente (24/11/2026)", h2)] + [Paragraph("• " + d, p) for d in DECISOES]
    e += [Paragraph("Atividades da virada", h2), t, Spacer(1, 6), Paragraph("Pontos de atenção", h2)]
    for x in ATENCAO:
        e.append(Paragraph("• " + x, p))
    doc.build(e)
    print("PLANO:", saida)


if __name__ == "__main__":
    main()
