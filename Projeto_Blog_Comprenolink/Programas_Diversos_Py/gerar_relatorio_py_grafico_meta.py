# -*- coding: utf-8 -*-
r"""gerar_relatorio_py_grafico_meta.py  (criado em 24/11/2026 por ordem do dono, via conversa Execução)

PARA QUE SERVE: gera o PDF diário da conversa "1- PY- Prog gerador gráfico de anúncio META - BLOG" mostrando
APENAS as atividades que esta conversa vai executar no NOVO PLANO (virada para o orgânico), em ordem de data:
Atividade (com "para que serve") | Status | Quem | Data e horário.
Regras: sem histórico do anúncio antigo; atividade concluída SAI da lista (mude o status para "Concluída" e ela
some na próxima geração); atividade nova ENTRA conforme o plano ou replanejamento. Só gerar quando houver atividade.
Uma versão só na pasta; as anteriores vão para old_bkp.
Saída: D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog\
       1- PY- Prog gerador grafico de anuncio META - BLOG_DD_MM_AAAA_HHhMM.pdf
Uso: python -X utf8 "D:\Projeto_Blog_Comprenolink\Programas_Diversos_Py\gerar_relatorio_py_grafico_meta.py"
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

PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
PREFIXO = "1- PY- Prog gerador grafico de anuncio META - BLOG"

# (data de ordenação AAAA-MM-DD HH:MM, atividade, para que serve, status, quem, data e horário)
# Status: "Pendente", "Em andamento" ou "Concluída" (concluída não aparece no PDF).
ATIVIDADES = [
    ("2026-11-28 10:00", "Fechamento do anúncio bf_26_entrada: somar 20/11 a 28/11 e conferir vendas no ML Afiliados; sem venda vinda do anúncio, só PAUSAR (sem mexer em verba nem pagamento). Resultado ao dono até 10h30 e 1 linha à Execução",
     "parar de gastar sem resultado", "Pendente", "Claude (1-PY), tarefa automática", "sáb 28/11 10:00"),
    ("2026-11-28 10:01", "Linha de base do orgânico de 16 a 28/11 (sem anúncio e sem teste), por origem, no mesmo download do fechamento: LINHA_BASE_ORGANICO_16_28_11.csv",
     "ter com o que comparar nas leituras de segunda", "Pendente", "Claude (1-PY), tarefa automática", "sáb 28/11 10:00"),
    ("2026-11-29 09:00", "Linha de confiança no topo das categorias e do guia: \"Você compra direto no site oficial do Mercado Livre...\" (no gerador, com backup e conferência)",
     "tirar o medo de golpe e fazer comprar pelo link", "Pendente", "Claude (1-PY), tarefa automática", "dom 29/11 09:00 (conferida até 09:30)"),
    ("2026-11-30 20:35", "Leitura 1 do rastreador: cliques para o ML por origem (7 dias x linha de base), contando à parte o Instagram com etiqueta da bio; resultado em 1 linha à Execução",
     "saber se o orgânico traz cliques", "Pendente", "Claude (1-PY), acionada pela Execução", "seg 30/11 20:35"),
    ("2026-11-30 21:00", "Linha semanal à Execução: o que fez, o que está pendente, o que precisa do dono",
     "o dono ler tudo num lugar só", "Pendente", "Claude (1-PY)", "toda segunda, antes das 21:00"),
    ("2026-12-03 20:35", "Leitura parcial do rastreador (meio da semana)",
     "acompanhar a tendência antes da decisão da fase 2", "Pendente", "Claude (1-PY), acionada pela Execução", "qui 03/12"),
    ("2026-12-07 20:35", "Leitura 2 do rastreador (para a decisão da fase 2: 3 Reels por dia só com uso < 60% e cliques subindo)",
     "aumentar o esforço só com evidência", "Pendente", "Claude (1-PY), acionada pela Execução", "seg 07/12 20:35"),
    ("2026-12-14 20:35", "Leitura 3 do rastreador (tendência das 3 leituras para a decisão continuar, aumentar ou reduzir)",
     "decidir com fato, não com hipótese", "Pendente", "Claude (1-PY), acionada pela Execução", "seg 14/12 20:35"),
]


def main():
    agora = dt.datetime.now()
    ativas = sorted([a for a in ATIVIDADES if a[3] != "Concluída"], key=lambda a: a[0])
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    for x in glob.glob(os.path.join(PASTA, PREFIXO + "_*.pdf")):
        shutil.move(x, os.path.join(PASTA, "old_bkp", os.path.basename(x)))
    saida = os.path.join(PASTA, f"{PREFIXO}_{agora:%d_%m_%Y_%Hh%M}.pdf")

    s = getSampleStyleSheet()
    h1 = ParagraphStyle("h1", parent=s["Title"], fontSize=16)
    h2 = ParagraphStyle("h2", parent=s["Heading2"], fontSize=12)
    p = ParagraphStyle("p", parent=s["BodyText"], fontSize=9.5, leading=13)
    c = ParagraphStyle("c", parent=s["BodyText"], fontSize=8.5, leading=11)
    cb = ParagraphStyle("cb", parent=c, textColor=colors.white)
    doc = SimpleDocTemplate(saida, pagesize=landscape(A4), leftMargin=1.4 * cm, rightMargin=1.4 * cm,
                            topMargin=1.3 * cm, bottomMargin=1.3 * cm, title="Atividades da conversa 1-PY no novo plano")
    dados = [[Paragraph(x, cb) for x in ("Atividade", "Status", "Quem", "Data e horário")]]
    for _, atv, para, st, quem, quando in ativas:
        dados.append([Paragraph(f"{atv}. <b>Para que serve:</b> {para}", c), Paragraph(st, c), Paragraph(quem, c), Paragraph(quando, c)])
    t = Table(dados, colWidths=[15.5 * cm, 2.4 * cm, 4.6 * cm, 4.4 * cm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")), ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("PADDING", (0, 0), (-1, -1), 4),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")])]))
    e = [Paragraph("Atividades da conversa 1- PY- Prog gerador gráfico de anúncio META - BLOG", h1),
         Paragraph(f"Atualizado em {agora:%d/%m/%Y às %H:%M}. Só as atividades que esta conversa vai executar no NOVO PLANO "
                   f"(virada para o orgânico, 29/11), em ordem de data. Concluída sai; nova entra conforme o plano ou replanejamento.", p),
         Spacer(1, 6), Paragraph("Atividades em ordem de data", h2), t]
    doc.build(e)
    print("PDF:", saida)


if __name__ == "__main__":
    main()
