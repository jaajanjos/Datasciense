# -*- coding: utf-8 -*-
"""Plano geral da virada para o organico (29/11/2026): atividades por conversa, com dia/hora de execucao e entrega.
Gerado pela conversa BLOG - Ajustes Instagram. Uma unica versao na pasta (anterior -> old_bkp)."""
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
 ("1. BLOG - Ajustes Instagram (dona dos Reels)", [
  ("MISSÃO DOS REELS: ser a dona de agendar todos os dias de Reels até fechar o ciclo (23/12), o mais cedo possível, em lotes semanais e com as guardas de uso (5h>75% ou semanal>80%)",
   "Uma dona só, sem duplicar; Reels todos os dias", "Contínua, desde 25/11", "Até 23/12/2026", "Em andamento"),
  ("Regra de agendamento: manter o que já está agendado; nos dias com Reel das 19h05, agendar só o novo das 13h30; nos demais, 13h30 e 20h00", "Não duplicar nem apagar sem o de acordo do dono", "Aprovada em 25/11", "—", "Concluído (25/11)"),
  ("Pasta dos Reels novos criada: REELS_NOVO_BLOG (01_AMOSTRA e 02_LOTE_29-11_a_06-12); só esta conversa grava nela", "Tudo no lugar certo", "25/11", "—", "Concluído (25/11)"),
  ("Trocar o link da bio do Instagram com etiqueta de rastreio (utm_medium=bio), com o sim do dono", "Medir os cliques que vêm dos Reels", "Sex 27/11, dentro da janela das 14h00 às 16h00", "Sex 27/11: link trocado e conferido", "Previsto"),
  ("Receber do dono o caminho da pasta nova dos Reels e confirmar o estilo visual agressivo para os Reels orgânicos",
   "Produzir tudo no lugar certo, sem mexer em nada fora da estrutura", "Qua 25/11, até 20h00 (resposta do dono)", "Qua 25/11, 20h00", "Concluído (25/11)"),
  ("Desenhar o estilo visual novo e mostrar 1 Reel de amostra", "O dono aprovar o visual antes de eu gerar em volume",
   "Qua 25/11, 20h00 às 21h30", "Amostra enviada na conversa, qua 25/11 até 21h30; 'sim' do dono até 22h00", "Concluído (25/11)"),
  ("Gerar o 1º lote: 16 Reels (29/11 a 06/12, fase 1: 2 por dia, alternando estilo novo e atual), legenda só comprenolink.net, sem hashtag, sem preço e sem 'melhor', 'mais vendido' ou 'líder'",
   "Domingo 29/11 já começar com os Reels", "Qui 26/11, 20h00 às 23h00", "Qui 26/11, 23h00: 16 vídeos e legendas prontos na pasta", "Concluído (antecipado, 25/11)"),
  ("Agendar o lote no Meta Business Suite com o dono (ele escolhe cada arquivo na janela do Windows)",
   "Reels no ar às 13h30 e 20h00 (fase 1)", "Sex 27/11, 14h00 às 16h00 (Chrome reservado pela Execução)", "Sex 27/11, até 16h00: 16 Reels agendados e conferidos na lista do Meta; uso do plano (%) informado à Execução antes e depois", "Confirmado (Chrome)"),
  ("Gerar o lote da semana seguinte (2 por dia na fase 1; 3 por dia na fase 2 se os critérios forem atendidos)", "Estoque sempre de 1 a 2 semanas à frente",
   "Toda quinta, 20h00 às 23h00 (1ª vez: qui 26/11)", "Quinta, 23h00: vídeos prontos na pasta", "Previsto"),
  ("Agendar o lote da semana no Meta com o dono", "Nunca faltar Reel (o Meta trava com muitos vídeos de uma vez)",
   "Toda sexta, 14h00 às 16h00 (1ª vez: sex 27/11; 2ª: sex 04/12)", "Sexta, até 16h00: lote agendado e conferido", "Previsto"),
  ("Conferir só em leitura que os Reels saíram nos horários e com a legenda certa", "Garantir a virada sem falha",
   "Dom 29/11, 13h45 (1º Reel) e 20h30 (os 2 do dia); depois, dias úteis após as 20h30", "Resultado no PDF e na conversa, no mesmo dia", "Previsto (fim de semana vale por decisão do dono)"),
  ("Leitura dos números do Instagram (alcance, salvamentos, cliques) comparando estilo novo e atual, e proposta do que repetir", "Aprender com o orgânico, sem custo",
   "Seg 30/11, 07/12 e 14/12, 20h00", "Mesma segunda, 21h00: linha enviada à Execução; decisão de continuar ou reduzir em 14/12", "Previsto"),
  ("Atualizar e enviar o meu PDF (evolução e replanejamento)", "O dono acompanha tudo em um lugar só",
   "Só quando houver atividade", "Mesmo dia, na conversa", "Rotina"),
 ]),
 ("2. BLOG - Planejamento e mentoria técnica (orquestradora e mentora)", [
  ("Distribuir as atividades da virada às conversas e cobrar prazos", "Cada conversa fazer só a sua parte, sem sobrecarga",
   "Qua 25/11 (primeira distribuição)", "Qua 25/11: todas as conversas cientes", "Aceito pela conversa"),
  ("Reservar o Chrome para a conversa dos Reels", "Evitar conflito de agenda", "Já feito", "Sex 27/11, 14h00 às 16h00 reservado", "Confirmado"),
  ("Economia: até o fechamento de 28/11 não gastar com o sistema atual (leitura do Pixel, relatório da manhã e ajuste de verba DESATIVADOS; troca de arte de Natal CANCELADA)",
   "Foco total na mudança, sem gastar plano à toa", "Desde 24/11", "Registro no relatório geral", "Feito"),
  ("Autonomia da orquestradora: ajustar o plano e o sucesso das atividades a qualquer momento, alinhando todas as conversas (dono, 24/11), sem prejuízo do objetivo: venda com calma e constância. Sem o dono: anúncio pago (nunca), WhatsApp, gasto de dinheiro, ações irreversíveis, conteúdo fora da política",
   "Replanejar sem esperar, com todos alinhados", "A qualquer momento", "Mensagem curta a todas as conversas e PDF do plano atualizado", "Vigente"),
  ("Leitura parcial do rastreador (a 1-PY, acionada por mim) para decidir a fase 2 de Reels", "Só aumentar o ritmo com evidência",
   "Qui 03/12, 20h35", "Qui 03/12, até 21h: 1 linha; decisão na sex 04/12", "Agendada"),
  ("Ajustar as tarefas que dependem do anúncio ligado (30/11, 17/12, 22/12, 28/12 e Pixel diário), com aprovação do dono",
   "Não rodar checagens de um anúncio pausado", "Seg 30/11, 20h30", "Seg 30/11, 21h30: proposta aprovada ou ajustada", "Previsto"),
  ("Ajustar a rotina de segunda para os Reels em rampa (hoje agenda 1 Reel às 19h05), com o 'de acordo' do dono",
   "A rotina acompanhar a nova estratégia", "Seg 30/11, 20h00", "Seg 30/11, 21h00: rotina nova registrada", "Concluído (25/11): rotina de segunda desativada; Reels com a conversa do Instagram"),
  ("Linha de base: cliques ao ML por dia dos 7 dias anteriores, separando o tráfego do anúncio pago (utm_medium=paid); comparar com 07/12 e 14/12", "Medir se os Reels aumentam os cliques, sem custo",
   "Seg 30/11, 07/12 e 14/12", "Segunda, 22h00, no relatório geral", "Previsto"),
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
 ("4. BLOG - Execução de atividades", [
  ("Sincronizar com a Página do Facebook só os Reels bons que o dono escolher", "Facebook com esforço mínimo, sem apagar a Página",
   "Sugestão: quartas, 20h00, depois do aviso da conversa dos Reels (sem prazo fixo)", "No mesmo dia da escolha do dono", "Previsto"),
  ("Conferir no blog, só em leitura, as melhorias M1+M3+M7 e M2 (01 e 02/12) e o piloto M4 (08/12) e avisar a Execução em 1 linha", "Garantir que nada quebrou", "Qua 02/12 e qua 09/12, 20h30", "Mesmo dia: 1 linha à Execução", "Agendada"),
  ("Atualizar e enviar o PDF próprio da conversa", "Acompanhamento diário", "Todo dia útil", "Mesmo dia", "Rotina"),
 ]),
 ("5. O que depende do dono (José)", [
  ("Passar o caminho completo da pasta nova dos Reels e confirmar o estilo visual", "Eu começar a amostra", "Qua 25/11", "Até 20h00", "Concluído (25/11)"),
  ("Aprovar (ou pedir ajuste) a amostra do Reel", "Liberar o lote de 29 e 30/11", "Qua 25/11", "Até 22h00", "Concluído (25/11)"),
  ("Estar no PC para escolher os arquivos dos vídeos no Meta", "Agendar os Reels", "Sex 27/11, 14h00 às 16h00 e toda sexta no mesmo horário", "Mesmo horário", "Combinar"),
  ("Deixar o PC acordado com o app do Claude e o Chrome abertos no fim de semana de 28 e 29/11", "Fechamento, linha de confiança e conferência rodarem", "Sáb 28/11 e dom 29/11", "—", "Combinar"),
 ]),
]

def tabela(linhas):
    st = getSampleStyleSheet()["BodyText"]; st.fontSize = 8; st.leading = 10
    dados = [[Paragraph("<b>%s</b>" % c, st) for c in CAB]]
    for l in linhas:
        cel = [Paragraph(x, st) for x in l]
        sit = str(l[-1])
        if sit.startswith("Concluído"):
            cel[-1] = Paragraph('<font color="#166534"><b>%s</b></font>' % sit, st)
        elif sit.startswith("Em andamento"):
            cel[-1] = Paragraph('<font color="#A16207"><b>%s</b></font>' % sit, st)
        dados.append(cel)
    t = Table(dados, colWidths=LARG, repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8E8E8")),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                           ("VALIGN", (0, 0), (-1, -1), "TOP")]))
    for r_, l_ in enumerate(linhas, start=1):
        sit = str(l_[-1])
        if sit.startswith("Concluído"):
            t.setStyle(TableStyle([("BACKGROUND", (0, r_), (-1, r_), colors.HexColor("#DCFCE7"))]))
        elif sit.startswith("Em andamento"):
            t.setStyle(TableStyle([("BACKGROUND", (0, r_), (-1, r_), colors.HexColor("#FEF08A"))]))
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
          Paragraph("Gerado em %s às %s. Elaborado pela conversa BLOG - Ajustes Instagram; orquestração: BLOG - Planejamento e mentoria técnica." %
                    (AGORA.strftime("%d/%m/%Y"), AGORA.strftime("%Hh%M")), p), Spacer(1, 6),
          Paragraph("<b>Objetivo:</b> tirar o medo de golpe e fazer o visitante comprar pelo link do blog, para a comissão contar, com persistência e custo zero. "
                    "Nunca mais anúncio pago.", p), Spacer(1, 3),
          Paragraph("<b>Decisões do dono (24/11):</b> o anúncio bf_26_entrada fecha sáb 28/11 às 10h00 (sem venda é pausado). "
                    "O orgânico começa dom 29/11: linha de confiança no blog e Reels no Instagram em RAMPA (ajuste da orquestradora, 24/11): fase 1 (29/11 a 06/12) = 2 por dia, às 13h30 e 20h00; fase 2 (07 a 13/12) = 3 por dia, só se o uso do plano ficar abaixo de 60% e os cliques ao ML estiverem subindo; fase 3 = 5 por dia, só com evidência. Medições seg 30/11, 07/12 e 14/12; decisão de continuar ou reduzir em 14/12. Na fase 1, alternar estilo novo e atual por dia e comparar alcance e salvamentos. "
                    "Facebook só sincroniza os Reels bons; WhatsApp fora.", p), Spacer(1, 3),
          Paragraph("<b>Regras para todas as conversas:</b> legenda só comprenolink.net, sem hashtag, sem preço e sem 'melhor/mais vendido/líder'; "
                    "ninguém mexe no anúncio pago além do fechamento; avisar a Execução antes de usar o Chrome; cópia em old_bkp antes de alterar arquivo do projeto; "
                    "nada muda de lugar sem o 'de acordo' do dono; cada conversa mantém o seu PDF diário com evolução e replanejamento; "
                    "toda segunda cada conversa manda uma linha à Execução (o que fez, o que está pendente, o que precisa do dono).", p)]
    for tit, linhas in SECOES:
        el.append(Paragraph(tit, h2)); el.append(tabela(linhas))
    el += [Spacer(1, 8), Paragraph("<b>Pontos de atenção:</b> (1) sem o lote pronto na quinta 26/11, o domingo começa sem Reels; critério de viabilidade: se o uso do plano passar de 75% (janela de 5h) ou 80% (semanal), parar e reduzir o agendamento; a fase 2 de 07/12 é decidida na sex 04/12 com a leitura parcial; "
           "(2) o Meta trava com muitos vídeos de uma vez, por isso lotes semanais; (3) se o limite de uso das 5 horas não bastar, a tarefa passa para depois da renovação; "
           "(4) 'Previsto' = horário sugerido, vale até o dono mudar; 'Agendada' e 'Confirmado' já estão combinados.", p)]
    doc.build(el)
    print(os.path.join(PASTA, NOME))

main()
