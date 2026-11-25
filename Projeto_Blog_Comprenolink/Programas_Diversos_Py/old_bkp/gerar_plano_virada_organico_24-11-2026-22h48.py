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
    "Nunca mais anúncio pago (Meta ou outro). Depois do bf_26_entrada, todo o processo fica no orgânico para sempre.",
    "O anúncio bf_26_entrada segue até o fechamento de sáb 28/11 às 10:00. Sem venda vinda do anúncio, é PAUSADO (só pausar; a Meta só cobra o que já foi gasto). Com venda, vai até 22/12 e não renova.",
    "A estratégia orgânica começa dom 29/11, de qualquer jeito: (1) linha de confiança no blog; (2) 5 Reels por dia, persistente; (3) sem gastar nada.",
    "Texto aprovado da linha de confiança: \"🔒 Você compra direto no site oficial do Mercado Livre. O CompreNoLink só indica os produtos: o pagamento e a entrega são feitos pelo próprio Mercado Livre.\"",
]

# Atividade | Dia e horário | Próximas datas | Quem executa | Conversa de apoio | Para que serve
ATIVIDADES = [
    ("Gerar os Reels de 29/11 em diante (5 por dia, itens do guia ainda não usados, legenda só com comprenolink.net) e agendar no Meta Business Suite",
     "sex 27/11 14h00 (horário a confirmar com o dono)", "depois, lotes semanais (seg 14h00)", "Claude + dono (dono escolhe o arquivo do vídeo)",
     "BLOG- Ajustes no WhatsApp e Instagram", "ter Reels prontos no ar já no domingo 29/11"),
    ("Trocar a arte e o texto do anúncio para Natal", "sex 27/11 23h30 (tarefa natal-troca-criativo-27-11)", "-", "Claude",
     "BLOG - Execução de atividades e planejamento", "anúncio de Natal no ar se ele continuar depois de 28/11"),
    ("FECHAMENTO do anúncio: somar 20/11 a 28/11, conferir vendas no ML Afiliados; 0 venda = PAUSAR", "sáb 28/11 10h00 (tarefa fechamento-anuncio-28-11)",
     "-", "Claude (automático; avisa o dono)", "1- PY- Prog gerador gráfico de anúncio META - BLOG", "parar de gastar se o anúncio não vende"),
    ("Publicar a linha de confiança no topo das categorias e do guia", "dom 29/11 09h00 (tarefa linha-confianca-blog-29-11)", "-",
     "Claude (automático)", "1- PY- Prog gerador gráfico de anúncio META - BLOG", "tirar o medo de golpe e fazer comprar pelo link (comissão conta)"),
    ("INÍCIO: 5 Reels por dia no Instagram (11h00, 13h30, 16h00, 18h00, 20h00)", "dom 29/11, a partir das 11h00", "todos os dias", "Meta (agendado)",
     "BLOG- Ajustes no WhatsApp e Instagram", "mais gente vendo os produtos, sem custo"),
    ("Rotina de segunda: agendar o lote da semana com 5 Reels por dia (hoje agenda só 1 Reels às 19h05)", "seg 30/11 20h00 (tarefa divulgacao-diaria-whatsapp-story)",
     "toda segunda", "Claude + dono", "BLOG - Execução de atividades e planejamento (ajustar a rotina com o de acordo do dono)", "nunca faltar Reels"),
    ("Ajustar as tarefas que dependem do anúncio ligado (30/11, 17/12, 22/12, 28/12 e Pixel diário)", "seg 30/11, junto da checagem das 20h30",
     "-", "Claude propõe, dono aprova", "BLOG - Execução de atividades e planejamento", "não rodar checagens de um anúncio pausado"),
    ("Melhoria M2: 'Links verificados em DD/MM' nas categorias e no guia", "qua 02/12 20h00 (já agendada)", "-", "Claude",
     "BLOG - Execução de atividades e planejamento", "mais confiança: mostra que os links são conferidos"),
    ("Melhoria M6: bloco 'quem somos e como escolhemos' nas categorias (precisa do texto do dono)", "sex 11/12 20h00 (já agendada)", "-",
     "Claude + texto do dono", "BLOG - Execução de atividades e planejamento", "mais confiança para comprar pelo link"),
    ("Resumo final do anúncio pago (gasto, visitas, cliques, vendas e comissão)", "seg 28/12 20h30 (tarefa bfnatal-7)", "-", "Claude",
     "BLOG - Execução de atividades e planejamento", "fechar o capítulo do anúncio pago com números"),
    ("Replanejar e melhorar as artes dos Reels com os dados do orgânico", "seg 11/01/2027 20h00 (já agendada)", "-", "Claude propõe, dono aprova",
     "BLOG - Execução de atividades e planejamento", "Reels mais fortes em 2027"),
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
    e = [Paragraph("Plano da virada: do anúncio pago para o orgânico (a partir de 29/11/2026)", h1),
         Paragraph(f"Gerado em {agora:%d/%m/%Y às %Hh%M}. Para que serve: mostrar, em ordem, tudo o que precisa acontecer para a "
                   f"estratégia orgânica começar no domingo 29/11, quem faz cada coisa e para quê.", p),
         Paragraph("Decisões do dono (24/11/2026)", h2)] + [Paragraph("• " + d, p) for d in DECISOES]
    e += [Paragraph("Atividades da virada", h2), t, Spacer(1, 6), Paragraph("Pontos de atenção", h2)]
    for x in ["Os Reels depois de 27/11 ainda não existem: sem o agendamento de sexta 27/11 com o dono, o domingo 29/11 começa sem os 5 Reels.",
              "O agendamento no Meta precisa do dono escolhendo cada arquivo de vídeo; o Meta trava se muitos vídeos forem enviados de uma vez (lotes semanais).",
              "Sábado e domingo eram dias sem atividade; 28/11 e 29/11 valem por decisão do dono. Deixar o PC acordado e o app do Claude e o Chrome abertos.",
              "Orgânico é persistência: os números do acompanhamento semanal mostram o que repetir; resultado de venda pode levar semanas.",
              "Nenhuma atividade da virada mexe na verba nem no pagamento da Meta; a única ação no anúncio é PAUSAR em 28/11 se não houver venda."]:
        e.append(Paragraph("• " + x, p))
    doc.build(e)
    print("PLANO:", saida)


if __name__ == "__main__":
    main()
