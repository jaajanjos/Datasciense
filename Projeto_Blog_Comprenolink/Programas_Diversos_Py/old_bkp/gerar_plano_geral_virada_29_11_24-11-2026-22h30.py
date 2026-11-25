# -*- coding: utf-8 -*-
"""Plano geral da virada para o organico (29/11/2026): atividades por conversa, com dia/hora de execucao e entrega.
Gerado pela conversa BLOG - Ajustes no WhatsApp e Instagram. Uma unica versao na pasta (anterior -> old_bkp)."""
import os, shutil, glob
from datetime import datetime
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias"
AGORA = datetime.now()
NOME = "PLANO_GERAL_VIRADA_ORGANICO_29_11_2026_%s.pdf" % AGORA.strftime("%d_%m_%Y_%Hh%M")

CAB = ["Atividade", "Para que serve", "Execução (dia e hora)", "Entrega (dia e hora)", "Situação"]
LARG = [210, 150, 120, 150, 70]

SECOES = [
 ("1. BLOG - Ajustes no WhatsApp e Instagram (dona dos Reels)", [
  ("Receber do dono o caminho da pasta nova dos Reels e confirmar o estilo visual agressivo para os Reels orgânicos",
   "Produzir tudo no lugar certo, sem mexer em nada fora da estrutura", "Qua 25/11, até 20h00 (resposta do dono)", "Qua 25/11, 20h00", "Aguarda o dono"),
  ("Desenhar o estilo visual novo e mostrar 1 Reel de amostra", "O dono aprovar o visual antes de eu gerar em volume",
   "Qua 25/11, 20h00 às 21h30", "Amostra enviada na conversa, qua 25/11 até 21h30; 'sim' do dono até 22h00", "Previsto"),
  ("Gerar o 1º lote: 10 Reels (29/11 e 30/11), 5 por dia, legenda só comprenolink.net, sem hashtag, sem preço e sem 'melhor', 'mais vendido' ou 'líder'",
   "Domingo 29/11 já começar com os 5 Reels", "Qui 26/11, 20h00 às 23h00", "Qui 26/11, 23h00: 10 vídeos e legendas prontos na pasta", "Previsto (depende do 'sim' na amostra)"),
  ("Agendar o lote no Meta Business Suite com o dono (ele escolhe cada arquivo na janela do Windows)",
   "Reels no ar nos horários 11h00, 13h30, 16h00, 18h00 e 20h00", "Sex 27/11, 14h00 às 16h00 (Chrome reservado pela Execução)", "Sex 27/11, até 16h00: 10 Reels agendados e conferidos na lista do Meta", "Confirmado (Chrome)"),
  ("Gerar o lote da semana seguinte (terça a segunda, 5 por dia)", "Estoque sempre de 1 a 2 semanas à frente",
   "Toda sexta, 20h00 às 23h00 (1ª vez: sex 27/11)", "Sexta, 23h00: vídeos prontos na pasta", "Previsto"),
  ("Agendar o lote da semana no Meta com o dono", "Nunca faltar Reel (o Meta trava com muitos vídeos de uma vez)",
   "Toda segunda, 14h00 às 16h00 (1ª vez: seg 30/11)", "Segunda, até 16h00: lote agendado e conferido", "Previsto"),
  ("Conferir só em leitura que os Reels saíram nos horários e com a legenda certa", "Garantir a virada sem falha",
   "Dom 29/11, 11h15 (1º Reel) e 21h00 (5 do dia); depois, dias úteis após as 20h30", "Resultado no PDF e na conversa, no mesmo dia", "Previsto (fim de semana vale por decisão do dono)"),
  ("Revisão semanal dos números do Instagram (alcance, visualizações, cliques) e proposta do que repetir", "Aprender com o orgânico",
   "Toda segunda, 20h00 (1ª vez: seg 30/11)", "Segunda, 21h00: linha enviada à Execução e resumo ao dono", "Previsto"),
  ("Atualizar e enviar o meu PDF diário (evolução e replanejamento)", "O dono acompanha tudo em um lugar só",
   "Todo dia útil, ao fim do trabalho", "Mesmo dia, na conversa", "Rotina"),
 ]),
 ("2. BLOG - Execução de atividades e planejamento (orquestradora)", [
  ("Distribuir as atividades da virada às conversas e cobrar prazos", "Cada conversa fazer só a sua parte, sem sobrecarga",
   "Qua 25/11 (primeira distribuição)", "Qua 25/11: todas as conversas cientes", "Aceito pela conversa"),
  ("Reservar o Chrome para a conversa dos Reels", "Evitar conflito de agenda", "Já feito", "Sex 27/11, 14h00 às 16h00 reservado", "Confirmado"),
  ("Manter só o necessário do anúncio bf_26_entrada, sem esforço extra (checagem das 20h30 e gráfico diário já existentes)",
   "Não gastar mais uso no que se encerra", "Até 27/11, diário", "Registro no relatório geral do dia", "Rotina"),
  ("Perguntar ao dono se mantém a troca de arte de Natal e executar só se ele mantiver", "Evitar mexer no anúncio que fecha em 28/11",
   "Pergunta já feita; troca (se mantida): sex 27/11, 23h30", "Resposta do dono até qui 26/11, 20h00", "Aguarda o dono"),
  ("Ajustar as tarefas que dependem do anúncio ligado (30/11, 17/12, 22/12, 28/12 e Pixel diário), com aprovação do dono",
   "Não rodar checagens de um anúncio pausado", "Seg 30/11, 20h30", "Seg 30/11, 21h30: proposta aprovada ou ajustada", "Previsto"),
  ("Ajustar a rotina de segunda para 5 Reels por dia (hoje agenda 1 Reel às 19h05), com o 'de acordo' do dono",
   "A rotina acompanhar a nova estratégia", "Seg 30/11, 20h00", "Seg 30/11, 21h00: rotina nova registrada", "Previsto"),
  ("Juntar as linhas semanais de cada conversa no relatório geral", "O dono lê um lugar só",
   "Toda segunda, 21h00 (1ª vez: seg 30/11)", "Segunda, 22h00: relatório geral na conversa", "Previsto"),
  ("Melhoria M2: 'Links verificados em DD/MM' nas categorias e no guia", "Mais confiança para comprar pelo link", "Qua 02/12, 20h00 (já agendada)", "Qua 02/12, 21h00", "Agendada"),
  ("Melhoria M6: bloco 'quem somos e como escolhemos' (precisa do texto do dono)", "Mais confiança para comprar pelo link", "Sex 11/12, 20h00 (já agendada)", "Sex 11/12, 21h00 (texto do dono até qui 10/12)", "Agendada"),
  ("Resumo final do anúncio pago (gasto, visitas, cliques, vendas e comissão)", "Fechar o capítulo do anúncio com números", "Seg 28/12, 20h30 (já agendada)", "Seg 28/12, 21h30", "Agendada"),
  ("Replanejar e melhorar as artes dos Reels com os dados do orgânico", "Reels mais fortes em 2027", "Seg 11/01/2027, 20h00 (já agendada)", "Seg 11/01/2027, 21h30: proposta ao dono", "Agendada"),
 ]),
 ("3. 1- PY - Prog gerador gráfico de anúncio META - BLOG", [
  ("Fechamento do anúncio: somar 20/11 a 28/11 e conferir vendas no ML Afiliados; sem venda, só PAUSAR (não editar nada)",
   "Parar de gastar se o anúncio não vende", "Sáb 28/11, 10h00 (tarefa fechamento-anuncio-28-11)", "Sáb 28/11, até 10h30: dono avisado do resultado", "Agendada"),
  ("Publicar a linha de confiança no topo das categorias e do guia: 'Você compra direto no site oficial do Mercado Livre. O CompreNoLink só indica os produtos: o pagamento e a entrega são feitos pelo próprio Mercado Livre.'",
   "Tirar o medo de golpe e fazer comprar pelo link (comissão conta)", "Dom 29/11, 09h00 (tarefa linha-confianca-blog-29-11)", "Dom 29/11, até 09h30: conferida no blog", "Agendada"),
 ]),
 ("4. BLOG- Pendencia e ajustes em programas", [
  ("Sincronizar com a Página do Facebook só os Reels bons que o dono escolher", "Facebook com esforço mínimo, sem apagar a Página",
   "Sugestão: quartas, 20h00, depois do aviso da conversa dos Reels (sem prazo fixo)", "No mesmo dia da escolha do dono", "Previsto"),
  ("Atualizar e enviar o PDF próprio da conversa", "Acompanhamento diário", "Todo dia útil", "Mesmo dia", "Rotina"),
 ]),
 ("5. BLOG- Day by Day e WhatsApp", [
  ("Day by Day: nenhuma atividade da virada, só dúvidas do dono. WhatsApp: fora; só com venda comprovada e evidência, explicado antes ao dono.",
   "Não sobrecarregar", "—", "—", "Sem atividade"),
 ]),
 ("6. O que depende do dono (José)", [
  ("Passar o caminho completo da pasta nova dos Reels e confirmar o estilo visual", "Eu começar a amostra", "Qua 25/11", "Até 20h00", "Aguardado"),
  ("Aprovar (ou pedir ajuste) a amostra do Reel", "Liberar o lote de 29 e 30/11", "Qua 25/11", "Até 22h00", "Aguardado"),
  ("Decidir se mantém a troca de arte de Natal de 27/11 23h30", "Evitar conflito com o fechamento de 28/11", "Qui 26/11", "Até 20h00", "Aguardado"),
  ("Estar no PC para escolher os arquivos dos vídeos no Meta", "Agendar os Reels", "Sex 27/11, 14h00 às 16h00 e toda segunda 14h00", "Mesmo horário", "Combinar"),
  ("Deixar o PC acordado com o app do Claude e o Chrome abertos no fim de semana de 28 e 29/11", "Fechamento, linha de confiança e conferência rodarem", "Sáb 28/11 e dom 29/11", "—", "Combinar"),
 ]),
]

def tabela(linhas):
    st = getSampleStyleSheet()["BodyText"]; st.fontSize = 8; st.leading = 10
    dados = [[Paragraph("<b>%s</b>" % c, st) for c in CAB]]
    for l in linhas:
        dados.append([Paragraph(x, st) for x in l])
    t = Table(dados, colWidths=LARG, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    return t

def main():
    os.makedirs(PASTA, exist_ok=True)
    bkp = os.path.join(PASTA, "old_bkp"); os.makedirs(bkp, exist_ok=True)
    for f in glob.glob(os.path.join(PASTA, "PLANO_GERAL_VIRADA_ORGANICO_29_11_2026_*.pdf")):
        shutil.move(f, os.path.join(bkp, os.path.basename(f)))
    ss = getSampleStyleSheet()
    doc = SimpleDocTemplate(os.path.join(PASTA, NOME), pagesize=landscape(A4), leftMargin=24, rightMargin=24, topMargin=24, bottomMargin=24,
                            title="Plano geral da virada para o orgânico - 29/11/2026")
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontSize=15)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontSize=11, spaceBefore=8, spaceAfter=4)
    p = ParagraphStyle("p", parent=ss["BodyText"], fontSize=9, leading=12)
    el = [Paragraph("Plano geral da virada para o orgânico (domingo 29/11/2026)", h1),
          Paragraph("Gerado em %s às %s. Elaborado pela conversa BLOG - Ajustes no WhatsApp e Instagram; orquestração: BLOG - Execução de atividades e planejamento." %
                    (AGORA.strftime("%d/%m/%Y"), AGORA.strftime("%Hh%M")), p), Spacer(1, 6),
          Paragraph("<b>Objetivo:</b> tirar o medo de golpe e fazer o visitante comprar pelo link do blog, para a comissão contar, com persistência e custo zero. "
                    "Nunca mais anúncio pago.", p), Spacer(1, 3),
          Paragraph("<b>Decisões do dono (24/11):</b> o anúncio bf_26_entrada fecha sáb 28/11 às 10h00 (sem venda é pausado). "
                    "O orgânico começa dom 29/11: linha de confiança no blog e 5 Reels por dia no Instagram (11h00, 13h30, 16h00, 18h00 e 20h00). "
                    "Facebook só sincroniza os Reels bons; WhatsApp fora.", p), Spacer(1, 3),
          Paragraph("<b>Regras para todas as conversas:</b> legenda só comprenolink.net, sem hashtag, sem preço e sem 'melhor/mais vendido/líder'; "
                    "ninguém mexe no anúncio pago além do fechamento; avisar a Execução antes de usar o Chrome; cópia em old_bkp antes de alterar arquivo do projeto; "
                    "nada muda de lugar sem o 'de acordo' do dono; cada conversa mantém o seu PDF diário com evolução e replanejamento; "
                    "toda segunda cada conversa manda uma linha à Execução (o que fez, o que está pendente, o que precisa do dono).", p)]
    for tit, linhas in SECOES:
        el.append(Paragraph(tit, h2)); el.append(tabela(linhas))
    el += [Spacer(1, 8), Paragraph("<b>Pontos de atenção:</b> (1) sem o lote pronto na quinta 26/11, o domingo começa sem os 5 Reels; "
           "(2) o Meta trava com muitos vídeos de uma vez, por isso lotes semanais; (3) se o limite de uso das 5 horas não bastar, a tarefa passa para depois da renovação; "
           "(4) 'Previsto' = horário sugerido, vale até o dono mudar; 'Agendada' e 'Confirmado' já estão combinados.", p)]
    doc.build(el)
    print(os.path.join(PASTA, NOME))

main()
