# -*- coding: utf-8 -*-
"""RELATÓRIO DE ATIVIDADES do Claude no blog comprenolink.net / Instagram @compre.no.link (formato diário de bordo).
Rodar:  python -X utf8 gerar_relatorio_atividade.py
Saida: D:/Projeto_Blog_Comprenolink/0- Pendencias/4_Relatorio_Ativ_Claude_no_Blog/BLOG - Execução de atividades e planejamento_DD_MM_AAAA_HHhMM.pdf
(nome definido pelo dono em 19/11/2026; antes: RELATORIO_ATIVIDADE_CLAUDE_BLOG_DD_MM_AAAA_HHhMM.pdf)

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
SAIDA = rf"D:/Projeto_Blog_Comprenolink/0- Pendencias/4_Relatorio_Ativ_Claude_no_Blog/BLOG - Execução de atividades e planejamento_{AGORA:%d_%m_%Y_%Hh%M}.pdf"
W, H = landscape(A4)
LARG = W - 3 * cm
AZUL = colors.HexColor("#0369A1")
P = lambda t, e="pq": Paragraph(t, S[e])  # noqa: E731
TXT = ParagraphStyle("txt", fontName="Arial", fontSize=9.6, leading=13.4, textColor=ESCURO)

EX, PA, NE = "EXECUTADO", "PARCIAL", "NÃO EXECUTADO"
COR = {EX: (VERDE, VERDE_C), PA: (LARANJA, LARANJA_C), NE: (VERMELHO, VERMELHO_C)}

# (data, hora, atividade, situação, o que foi feito / evidência, motivo (se não executado), nova data para reexecutar)
ATIVIDADES = [
    ('19/11', '00:59', 'Conferência das tarefas agendadas (conversa nova: BLOG - Execução de atividades e planejamento)', 'EXECUTADO', 'Esta conversa assumiu tudo da "Atividades Claude e Planejamento" (passagem registrada nas anotações). Conferi as tarefas agendadas: as 3 da noite de 18/11 (BF/Natal 2, Pixel, Melhorias M0) terminaram com sucesso; as 5 de hoje (10:06, 10:22, 12:23, 20:00 e 20:30) estão ativas. Nenhuma tarefa cita a conversa antiga.', '', ''),
    ('19/11', '01:15', 'Anúncio Black Friday: decisão do dono ("DE ACORDO") aplicada às tarefas', 'EXECUTADO', 'Plano A: R$ 90 de 20 a 27/11 (≈ R$ 11,25/dia), se até sex 20/11 18:00 o limite da Meta (≥ R$ 90) e a comissão dos 5 itens estiverem resolvidos; senão plano B: R$ 50 de 24 a 27/11. Natal R$ 100 mantido e condicional. Criado 1_Pendencias/DECISAO_ANUNCIO_BF_2026.md e ajustadas 4 tarefas (aviso 20/11 09:00, BF/Natal 4, aviso 23/11 09:00, BF/Natal 5), com cópia em old_bkp. Nada alterado na Meta nem no site.', '', 'Dono: limite da Meta e comissão até sex 20/11 18:00'),
    ('19/11', '01:50', 'Anúncio de Natal alterado pelo dono e aplicado às tarefas', 'EXECUTADO', 'Natal = R$ 150 de 14 a 24/12 (substitui R$ 100 de 03 a 14/12), só se a BF passar; anúncio vai até 24/12. Teto sobe para R$ 290 (acumulado possível R$ 289,67). DECISAO_ANUNCIO_BF_2026.md atualizado; tarefas: BF/Natal 6 (30/11) ajustada, BF/Natal 7 movida para 28/12, Pixel diário estendido até 28/12, criadas natal-preparo-11-12 e natal-parada-17-12. Backups em old_bkp.', '', 'Dono: seg 14/12 subir o limite em + R$ 150 e criar o anúncio (se aprovado)'),
    ('19/11', '02:00', 'Fim do anúncio de Natal antecipado para 22/12 (decisão do dono)', 'EXECUTADO', 'Natal = R$ 150 de 14 a 22/12 (≈ R$ 16,67/dia), mesma verba e mesmo teto (R$ 290). Atualizados DECISAO_ANUNCIO_BF_2026.md, BF/Natal 6 e 7, natal-preparo-11-12, natal-parada-17-12 e este relatório; backups em old_bkp.', '', ''),
    ('19/11', '02:20', 'Página de entrada 752 (rascunho): 5 itens trocados por moda e calçados, de comissão mais alta', 'EXECUTADO', 'A pedido do dono, saíram TV LG, soundbar JBL, Fire TV Stick e fone QCY; entraram Tênis Olympikus Veloz 3 (211), Kit 2 Bermudas Femininas (103), Kit 3 Leggings (36) e Kit 5 Conjuntos Infantil Menino (161); ficou o Kit 4 Bermudas (49). Motivo: nas vendas passadas, moda e calçados pagaram 17% a 21% (Kit 4 Bermudas Jeans 21%, tênis 20%, chinelo 17%), e eletrônicos nunca venderam, então a taxa deles é desconhecida. Os 5 itens estão Ativos (HTTP 200 em 18/11), sem preço e sem termos proibidos; a página continua em RASCUNHO. Backups em paginas_novas/old_bkp (inclui o conteúdo anterior do WP). Tarefas BF/Natal 4 e 5, aviso de 20/11 e DECISAO_ANUNCIO_BF_2026.md atualizados.', 'A comissão real de cada item só aparece no painel do ML Afiliados; os percentuais acima vêm de vendas antigas de itens parecidos.', 'Dono: conferir a comissão até sex 20/11 18:00'),
    ('19/11', '08:00', 'Página de entrada 752 (rascunho): Kit 4 Bermudas Tactel retirado a pedido do dono', 'EXECUTADO', 'A página agora tem 4 itens: Tênis Olympikus Veloz 3, Kit 2 Bermudas Femininas, Kit 3 Leggings e Kit 5 Conjuntos Infantil Menino. Continua em RASCUNHO, sem preço. Tarefas BF/Natal 4 e 5, avisos de 20 e 23/11 e DECISAO_ANUNCIO_BF_2026.md ajustados de 5 para 4 itens; backups em old_bkp.', '', 'Dono: conferir a comissão dos 4 itens até sex 20/11 18:00'),
    ('19/11', '08:23', 'Substituição automática de anúncios (verificação dos 213 anúncios no ML, validação e painel)', 'EXECUTADO', 'Verificação às 08:15: 213 de 213 ativos, 0 precisam de substituto; por isso o passo com o Chrome e o ML Afiliados não rodou e não houve troca nem Reels a reagendar. Regra de maior comissão (ranking dos afiliados, dentro da política) já está no roteiro para a próxima vez. Política do blog: nenhum preço e textos dentro da política. Painel Painel_conversao_performance_2026-11-19_08h21.pdf, planilha e resumo atualizados.', '', ''),
    ('19/11', '08:50', 'Limite de gastos da conta Meta (Compre no Link - Anúncios) subido de R$ 50 para R$ 150', 'EXECUTADO', 'Com o "pode fazer" do dono, abri Faturamento e pagamentos > Limite de gastos da conta > Alterar, digitei 150 e salvei. A Meta confirmou: limite mensal R$ 150,00; gasto R$ 49,67; saldo R$ 100,33; reinicia no dia 1º. Visa final 0442 válida (vence 12/2032). O limite precisava cobrir o gasto de novembro (R$ 49,67) mais o anúncio de R$ 90. Em 14/12 será preciso subir de novo para o Natal. Nada mais foi alterado na Meta.', '', 'Dono: em 14/12, subir o limite para o Natal'),
    ('19/11', '08:55', 'Comissão dos 4 itens da página 752 conferida no ML Afiliados', 'EXECUTADO', 'Com a conta do dono logada, abri a página de cada produto e li a barra Afiliados: Tênis Olympikus Veloz 3, Kit 2 Bermudas Femininas, Kit 3 Leggings e Kit 5 Conjuntos Infantil Menino = GANHOS 16% cada. Para comparar, os itens que saíram: TV LG, soundbar JBL e fone QCY = 5%; Kit 4 Bermudas Tactel = 16%. A troca triplicou a taxa (5% para 16%). Só leitura, nada alterado no ML nem no blog.', 'A taxa mostrada pode mudar com campanhas do ML.', ''),
    ('19/11', '09:55', 'Painel e planilha: origem e data das visitas e dos cliques no ML', 'EXECUTADO', 'A pedido do dono: novo quadro no fim do painel PDF ("De onde vieram as visitas e em que dia" e "Cliques no ML: quando e de onde"), abas novas Origem_Visitas e Visitas_por_Dia e colunas Primeiro dia/Último dia na aba Campanhas; acima de 30 dias só o total. Dados brutos do rastreador, 1 visita = 1 sessão. Planilha recalculada com 0 erros; painel Painel_conversao_performance_2026-11-19_09h54.pdf; cópia de consulta sincronizada. Limpeza do painel agora move para old_bkp e pula arquivo aberto.', '', ''),
    ('19/11', '01:18', 'Relatório de atividades: 1ª geração do dia', 'EXECUTADO', 'Regra permanente aplicada: saíram os 8 sucessos de 18/11; ficaram as 15 pendências; plano de reexecução refeito só com ações em aberto; dias sem agendar = 18/12, 21/12 e 23/12.', '', ''),
    ('19/11', '20:00', 'BF/Natal 3: página de entrada 752 PUBLICADA (plano A antecipado)', 'EXECUTADO', 'Os 4 itens (Tênis Olympikus Veloz 3, Kit 2 Bermudas Femininas, Kit 3 Leggings, Kit 5 Conjuntos Infantil Menino) estavam Ativos/HTTP 200 na verificação de hoje 08:21. Backup do conteúdo anterior em paginas_novas/old_bkp; página 752 passou de rascunho para publicada. Conferido: abre com status 200, sem preço e sem palavras proibidas (o "Melhores Produtos 2026" é só o menu do site); clique de teste com utm_campaign=teste_rastreio disparou o evento SaidaML.', 'O clique de teste conta como 1 saída no rastreador, com a campanha teste_rastreio (fácil de separar).', ''),
    ('19/11', '20:15', 'Material do anúncio entregue: MATERIAL_ANUNCIO_BF_2026-11-19.md', 'EXECUTADO', 'Texto curto sem preço, imagem sugerida (capa Esporte e Fitness; as artes de BF e os slides com preço não servem), link com UTM bf_26_entrada, R$ 90 total de 20/11 00:00 a 27/11 23:59, público amplo e frio e checklist passo a passo. Aviso: SaidaML sem leitura no Events Manager; se a Meta não otimizar por ele, usar visualização da página de destino.', 'Com R$ 90 a Meta dificilmente terá os ~50 eventos/semana para otimizar por SaidaML.', 'Dono: criar e publicar o anúncio hoje à noite'),
    ('19/11', '20:20', 'Gráficos diários: campanha trocada para bf_26_entrada e DECISAO atualizada', 'EXECUTADO', 'CONSTANTE CAMP de gerar_graficos_diarios.py agora é bf_26_entrada (títulos também); sem datas fixas, a rotina graficos-diarios-anuncio-meta não precisa de ajuste. DECISAO_ANUNCIO_BF_2026.md: plano A antecipado registrado. Backups em old_bkp.', '', ''),
    ('19/11', '20:45', 'Reels de 18/12 (Máquina de Cortar Cabelo e Barba Nixzen) AGENDADO antecipadamente', 'EXECUTADO', 'Instagram @compre.no.link: Reels sexta 18/12/2026 às 19:05, corte Original, legenda do 2_LEGENDA_REELS.txt (804/2.200). Conferido no calendário mensal após recarregar: 18/12 tem UM Reels às 19:05. Nada mais alterado; copia temporária do vídeo apagada.', '', ''),
]

FALTA_AGENDAR = [
    ("21/12", "Jogo de Lençol Casal Percal 600 Fios 4 Peças"),
    ("23/12", "Cortina de LED 3x3 m com 300 Luzes e Controle"),
]

# (quando, quem, o que, ganho / observação) – sempre a data mais cedo possível
REEXECUCAO = [
    ("sex 20/11 20:00", "Claude", "BF/Natal 4: só confere o andamento do anúncio (página já publicada em 19/11)", "Tarefa agendada; lê DECISAO_ANUNCIO_BF_2026.md."),
    ("qui 19/11 à noite (anúncio agendado para sex 20/11 00:00)", "Dono", "Criar e publicar o anúncio na Meta (Vendas + SaidaML; R$ 90 de 20/11 00:00 a 27/11 23:59)", "O Claude orienta (MATERIAL_ANUNCIO_BF_2026-11-19.md); publicar e pausar é sempre do dono."),
    ("seg 23/11 20:30", "Claude", "BF/Natal 5: checagem de parada (A) ou publicar a página 752 (B)", "Parar se saída < 3% ou custo por clique de saída > R$ 3."),
    ("seg 30/11 20:00", "Claude", "Agendar os Reels de 21/12 e 23/12 quando a janela abrir", "Rotina de segunda."),
    ("quando puder", "Dono", "\"De acordo\" para corrigir as legendas dos Reels e arquivar os posts repetidos de 11, 13, 16 e 18/11", "Legendas prometem resposta no Direct que não existe."),
    ("quando puder", "Dono", "Validar link e produto dos itens 67 (Suporte de TV) e 181 (Fone Soundcore P30i)", ""),
    ("a decidir", "Dono", "Frase \"dieta e alimentação leve\" na legenda da Air Fryer (11/11) e foto da LG (26/11), que traz \"melhor\" na imagem do fabricante", "Se o dono pedir, o Claude refaz só esse dia."),
    ("sempre que aparecer item em \"Precisam de substituto\"", "Dono + Claude", "Substituir anúncios fora do ar (manual, com o dono logado no ML Afiliados)", "O Claude mostra os substitutos para aprovação e troca no guia."),
]

OBSERVACOES = [
    "As tarefas agendadas só rodam com o PC ligado e sem suspender e o app Claude aberto; as da noite precisam também do Chrome com a extensão e da Meta e do Instagram (@compre.no.link) logados.",
    "Tudo que mexe no blog passa pelo gerenciador com backup antes. Na conta de anúncios Meta, o Claude só altera algo quando o dono pede na conversa (em 20/11: verba R$ 240, fim 22/12 e limite R$ 200). Pausar ou mudar o anúncio é sempre decidido junto com o dono.",
]

# DESTAQUE do topo: o que o dono deve fazer amanhã de manhã para o anúncio (pedido do dono em 19/11/2026)
DESTAQUE_TITULO = "ANÚNCIO BLACK FRIDAY: O QUE VOCÊ AINDA DEVE FAZER (HOJE, qui 19/11, à noite)"
DESTAQUE = [
    ("1", "Hoje à noite, depois das 20:00: criar e publicar o anúncio na Meta com o material que o Claude entrega (Vendas + SaidaML, R$ 90 total, AGENDADO para começar sex 20/11 00:00 e terminar 27/11 23:59)", "qui 19/11 noite", "Claude publica a página 752 às 20:00 e orienta o passo a passo. A Meta revisa o anúncio antes de rodar: criando hoje, ele já roda sexta de manhã"),
]

# PLANO DO ANÚNCIO A e B em ordem cronológica (pedido do dono em 19/11/2026). Plano A = R$ 90 de 20 a 27/11; plano B = R$ 50 de 24 a 27/11
PLANO_ANUNCIO_TITULO = "PLANO DO ANÚNCIO (uma campanha só: Black Friday + Natal, R$ 240, de 20/11 00:00 a 22/12 23:59)"
PLANO_ANUNCIO = [
    ("qui 19/11 20:26", "Anúncio criado e publicado na Meta pelo dono (campanha bf_26_entrada), para levar pessoas à página do blog com 4 produtos de 16% de comissão", "BF", "Dono", "FEITO"),
    ("sex 20/11 00:00", "Anúncio começou a rodar (a Meta aprovou). Para que serve: testar se quem chega pelo anúncio vai do blog para o Mercado Livre, que é o que gera comissão", "BF", "Meta", "FEITO"),
    ("sex 20/11 15:00", "Anúncio emendado com o Natal, a pedido do dono: verba total de R$ 90 para R$ 240 e fim de 27/11 para 22/12 às 23:59, sem pausa entre Black Friday e Natal", "BF+Natal", "Claude, com o pode faça do dono", "FEITO 20/11"),
    ("sex 20/11 15:05", "Limite de gastos mensal da conta Meta subido de R$ 150 para R$ 200 (volta a zero todo dia 1). Para que serve: o anúncio não parar sozinho em dezembro, quando deve gastar cerca de R$ 160", "BF+Natal", "Claude, com o sim do dono", "FEITO 20/11"),
    ("sex 20/11 15:10", "Tarefas agendadas do anúncio ajustadas para a nova data e reescritas em linguagem simples, dizendo para que serve cada uma", "BF+Natal", "Claude, a pedido do dono", "FEITO 20/11"),
    ("sex 20/11 12:30", "Conferido no Gerenciador de Anúncios: campanha e anúncio ATIVOS (aprovados pela Meta), verba R$ 90 então vigente. Para que serve: confirmar que o dinheiro está sendo usado como combinado", "BF", "Claude", "FEITO 20/11"),
    ("sex 20/11 12:45", "Verificação do anunciante enviada à Meta pelo dono (opção Verifique você mesmo, com documento com foto). Para que serve: a Meta pode interromper anúncios de quem não se verificou; com isso o anúncio não corre esse risco até 22/12", "BF+Natal", "Dono", "FEITO 20/11"),
    ("sáb 21/11 a ter 24/11 (Previsto: ter 24/11 09:00)", "Aguardar a resposta da Meta sobre a verificação (costuma levar até 2 dias úteis). Se pedir documento melhor, o Claude orienta; não envia dados pessoais por você", "BF+Natal", "Meta responde; dono envia, se pedirem", "Aguardando"),
    ("sex 20/11 22:32", "Arquivo documento_verificacao_1000px.jpg conferido: já não está mais na pasta Downloads (apagado por você). Para que serve: seu documento não ficar solto no computador", "BF+Natal", "Dono", "FEITO 20/11"),
    ("sex 20/11 23:05", "Rascunho \"Atualizado: Criativo\" do anúncio no Meta DESCARTADO, com o seu OK (foi gerado pelo salvamento automático). Conferido: o anúncio segue ativo. Para que serve: ninguém publicar sem querer uma mudança que ninguém decidiu", "BF+Natal", "Claude, com o OK do dono", "FEITO 20/11"),
    ("seg 23/11 20:30 (Previsto)", "Decidir juntos sobre as 2 sugestões da Meta (vídeo vertical Reels com áudio e música automática). Claude recomenda não aplicar agora: pedem vídeo e hoje o anúncio usa imagem; artes novas ficam para janeiro", "BF+Natal", "Dono e Claude, juntos", "Aguardando"),
    ("sex 20/11 20:35", "Conferência do anúncio feita pelo Claude (só leitura): ativo, R$ 240, gasto de hoje R$ 4,24, alcance de 353 pessoas. A repetição agendada para 21:10 não rodou: o limite de uso do Claude estourou (volta a funcionar a partir de 22:10) e não precisa ser refeita hoje. Para que serve: pegar cedo qualquer problema com o dinheiro", "BF+Natal", "Claude", "FEITO 20/11"),
    ("seg 23/11 09:44", "Mensagem de resumo do anúncio enviada ao dono (rodou às 09:44, atrasada ~44 min porque o app abriu mais tarde): gasto, visitas ao blog e idas ao Mercado Livre de sexta até segunda. Para que serve: saber cedo se o dinheiro está dando resultado", "BF+Natal", "Claude (tarefa agendada)", "FEITO 23/11"),
    ("seg 23/11 09:44", "Conversa aberta com o dono sobre incluir o PDF de gráficos do anúncio nos itens do menu: o Claude apresentou o histórico, as 4 alternativas e recomendou a alternativa 2 (incluir no menu e o Claude registrar a leitura da Meta quando o dono pedir). Para que serve: gerar os relatórios pelo menu, gastando menos do plano", "BF+Natal", "Claude apresentou", "FEITO 23/11"),
    ("seg 23/11 (Previsto: 12:00)", "Decidir a conversa do PDF de gráficos no menu (alternativas 1 a 4) e se a tarefa diária das 10:06 continua ou é desativada. Para que serve: nada ser feito sem o seu de acordo", "BF+Natal", "Dono e Claude, juntos", "Aguardando"),
    ("seg 23/11 (Previsto: 12:00)", "Validar link e produto das 4 trocas feitas em 21/11 no guia: itens 12 (Copo Térmico), 41 (Potes de Vidro), 48 (Fone Bluetooth) e 65 (Soundbar; o nome mudou, saiu \"110 W\"). Para que serve: não mandar visitante a um produto diferente do descrito", "BF+Natal", "Dono", "Aguardando"),
    ("seg 23/11 a ter 22/12, seg a sex 10:06 e 10:22", "Gráficos diários do anúncio e leitura do Pixel. Para que serve: acompanhar todo dia se o dinheiro está trazendo resultado", "BF+Natal", "Claude (tarefa agendada)", "Agendado"),
    ("seg 23/11 20:30", "Checagem: está valendo a pena? Se menos de 3% das visitas forem ao ML ou cada ida custar mais de R$ 3, o Claude avisa com os números. Nada é pausado sozinho: decidimos juntos", "BF+Natal", "Claude avisa, dono e Claude decidem", "Agendado"),
    ("qui 26/11 20:30", "Preparar a arte e o texto de Natal do anúncio. Para que serve: depois de 27/11 a palavra Black Friday fica velha e piora os cliques", "Natal", "Claude prepara, dono aprova", "Agendado"),
    ("sáb 28/11 (Previsto: 10:00)", "Trocar a arte de Black Friday pela de Natal na Meta, só com o de acordo do dono", "Natal", "Dono (ou Claude, se o dono pedir)", "Aguardando"),
    ("seg 30/11 20:30", "Resultado da semana da Black Friday (20 a 27/11) e recomendação: manter, ajustar ou pausar. Decisão junto com o dono", "BF+Natal", "Claude analisa, dono decide", "Agendado"),
    ("qui 17/12 20:00", "Checagem de dezembro: está valendo a pena? Cinco dias antes do fim, os números de dezembro para decidir juntos se vai até 22/12", "Natal", "Claude avisa, dono e Claude decidem", "Agendado"),
    ("ter 22/12 23:59", "Fim do anúncio (data escolhida pelo dono por causa do prazo de entrega do Mercado Livre antes do Natal)", "BF+Natal", "Meta", "Aguardando"),
    ("seg 28/12 20:30", "Resultado final: gasto real, visitas, idas ao ML, custo de cada ida e comissão esperada (o ML paga cerca de 60 dias depois), separando Black Friday e Natal", "BF+Natal", "Claude (tarefa agendada)", "Agendado"),
]

# PREVISÃO do anúncio da Black Friday (opinião do Claude em 19/11/2026, pedido do dono). Estimativa, não garantia.
PREVISAO_TITULO = "PREVISÃO DO ANÚNCIO DA BLACK FRIDAY (R$ 90): OPINIÃO DO CLAUDE EM 19/11 (estimativa, não garantia)"
PREVISAO_BASE = ("<b>Base:</b> 1º teste (11 a 13/11) = R$ 49,67 para 260 visitas (≈ R$ 0,19 por visita) e 0,8% de saída para o ML; "
                 "página do guia, com poucos itens = 14,6% de saída; histórico do painel = 19 vendas e R$ 172 (≈ R$ 9 de comissão por venda). "
                 "Com R$ 90: ≈ 350 a 470 visitas.")
PREVISAO = [
    ("Ruim (igual ao 1º teste, ≈ 1%)", "≈ 4", "0", "R$ 0"),
    ("REALISTA (página curta, 5 a 8%)", "≈ 20 a 35", "0 a 2", "R$ 0 a 20"),
    ("Bom (igual ao guia, ≈ 14%)", "≈ 50 a 65", "1 a 4", "R$ 10 a 40"),
]
PREVISAO_CONCLUSAO = [
    "<b>1.</b> O anúncio quase certamente não se paga na Black Friday: gastar R$ 90 para voltar R$ 0 a 40 é o mais provável.",
    "<b>2.</b> Chance de pelo menos 1 venda: algo como 50% (estimativa). Ajuda: quem entra no ML pelo link e compra outra coisa também gera comissão.",
    "<b>3.</b> O critério do Natal (R$ 150, 14 a 22/12) é difícil: custo por clique de saída abaixo de R$ 1 exige ≈ 19% de saída, mais do que o guia faz hoje. O mais provável é a BF não liberar o Natal, e isso protege o dinheiro.",
    "<b>4.</b> Vira vendas? Pelo anúncio pago, no curto prazo: chance baixa. Pelo blog no Google, no médio prazo: sim, há chance (o guia já leva 14,6% ao ML sem custo).",
    "<b>Valor real do plano:</b> aprender, gastando pouco, se a página curta converte. Saída perto de 8% ou mais em 30/11: repetir esse modelo de página no blog todo, de graça. Perto de 1%: o anúncio pago não serve, e você para sem perder mais.",
]

# ANÁLISE: o anúncio ajuda a divulgar o blog? (opinião do Claude em 19/11/2026, pedido do dono)
DIVULGACAO_TITULO = "O ANÚNCIO AJUDA A DIVULGAR O BLOG? OPINIÃO DO CLAUDE EM 19/11: AJUDA UM POUCO, MAS NÃO É DIVULGAÇÃO DO BLOG"
DIVULGACAO = [
    ("AJUDA", "Gente nova vendo o nome", "≈ 350 a 470 visitas e alguns milhares de pessoas vendo \"Compre no Link\": mais do que o Instagram orgânico traz hoje."),
    ("AJUDA", "O Pixel aprende", "Cada visita fica registrada na Meta; no futuro dá para anunciar só para quem já visitou o blog, o que costuma converter mais e custar menos."),
    ("AJUDA", "Seguidores, talvez alguns", "Se o anúncio sair pela conta @compre.no.link, quem gostar pode seguir."),
    ("NÃO AJUDA", "Visitante cai numa página só", "Ele vai da página 752 para o ML e quase não navega pelo resto do blog: é anúncio de venda, não de divulgação."),
    ("NÃO AJUDA", "Google não melhora com tráfego pago", "O que faz o blog aparecer no Google é conteúdo bom e páginas que as pessoas procuram."),
    ("NÃO AJUDA", "Acabou a verba, acabou a visita", "O efeito some em 27/11."),
    ("DIVULGA DE VERDADE", "1. Google", "Páginas sobre o que as pessoas pesquisam (ex.: presente de Natal por faixa, fone para academia), sem \"melhor\" no texto. É o canal que mais cresce com o tempo, de graça."),
    ("DIVULGA DE VERDADE", "2. Indicação direta", "O dono mandando o link para conhecidos e grupos permitidos."),
    ("DIVULGA DE VERDADE", "3. Instagram corrigido", "Bio e legendas dos Reels levando ao link da bio, sem prometer resposta no Direct."),
]
DIVULGACAO_CONCLUSAO = ("<b>Resumo:</b> o anúncio é um <b>teste de venda</b> com um pequeno efeito de divulgação. A divulgação de verdade vem do Google e das indicações, "
                        "e isso está no plano de melhorias do blog a partir de 01/12.")

# ANÁLISE: o que tudo isso vai refletir (opinião do Claude em 19/11/2026, pedido do dono)
REFLEXO_TITULO = "O QUE TUDO ISSO VAI REFLETIR: OPINIÃO SINCERA DO CLAUDE EM 19/11 (estimativa, não garantia)"
REFLEXO = [
    ("Até 30/11 (Black Friday)", "O mais provável é 0 a 2 vendas e R$ 90 gastos. O ganho real é a resposta: a página curta faz as pessoas irem ao ML ou não? Hoje é palpite; em 30/11 vira número."),
    ("Dezembro", "O Natal (R$ 150, 14 a 22/12) provavelmente não será liberado (critério difícil): economia de R$ 150. As melhorias do blog de 01 a 11/12 (botões, imagens, destaques no topo, confiança) devem melhorar a saída para o ML nas páginas que já recebem visita do Google: é a melhor chance de venda no fim do ano, sem custo."),
    ("Janeiro e fevereiro", "Caem as comissões de novembro e dezembro (≈ 60 dias depois). Deve ser pouco, mas será o primeiro número real do projeto. O replanejamento de janeiro terá dados de verdade para decidir o que manter, o que cortar e onde pôr esforço."),
]
REFLEXO_FUNDO = [
    "<b>1. Se o blog tem futuro como renda:</b> a resposta virá do Google e da taxa de saída das páginas, não do Instagram nem do anúncio.",
    "<b>2. Se vale continuar investindo dinheiro:</b> se a BF der muito abaixo de 8% de saída, a resposta honesta é não colocar mais dinheiro em anúncio, só tempo no blog.",
    "<b>3. Quanto esforço o projeto merece:</b> hoje a estrutura (4 conversas, dezenas de tarefas, relatórios) é grande para o retorno; o resultado de dezembro deve guiar um enxugamento em janeiro.",
    "<b>Expectativa realista:</b> o blog pode virar uma renda pequena e crescente (dezenas de reais por mês no começo) se o Google continuar trazendo visitas e as páginas melhorarem a saída. Com os números atuais, não há caminho para venda grande no curto prazo.",
]

# ANÁLISE GERAL com o Natal de R$ 150 (14 a 24/12) – opinião do Claude em 19/11/2026, pedido do dono
NATAL_TITULO = "ANÁLISE GERAL COM O NATAL DE R$ 150 (14 A 22/12): OPINIÃO DO CLAUDE EM 19/11 (estimativa, não garantia)"
NATAL_ANALISE = [
    ("1. Período", "14 a 22/12 é melhor que 03 a 14/12: é a reta final de compra de presente, quando a pessoa já decidiu comprar. A chance de venda por visita é maior."),
    ("2. Fim em 22/12", "Decisão do dono em 19/11: em 23 e 24/12 muita gente já não compra presente online por causa da entrega. Os mesmos R$ 150 ficam concentrados nos 9 dias bons (≈ R$ 16,67/dia), sem gastar mais."),
    ("3. Condição", "O mais provável, pelo critério atual (saída ≥ 8% e custo por clique de saída < R$ 1), é a Black Friday NÃO liberar o Natal. Se isso acontecer, economia de R$ 150."),
    ("4. Se o Natal rodar", "Algo parecido com a BF, um pouco melhor pela época: ≈ 600 a 800 visitas e, no cenário realista, 1 a 4 vendas, com comissão de ≈ R$ 10 a 40 caindo em fevereiro. Anúncio que se paga sozinho continua improvável."),
    ("5. No geral", "A previsão não muda: o anúncio serve para testar e aprender; a renda que pode crescer vem do Google e das páginas curtas."),
]
NATAL_DONO = ("<b>O que é do dono:</b> sex 20/11 limite da Meta (R$ 90) e comissão dos 4 itens; seg 30/11 decidir o Natal; "
              "seg 14/12, se aprovado, subir o limite em + R$ 150 e criar o anúncio (vai até 22/12). Teto total: R$ 290.")

# PLANO FINAL e análise "vale para testar o blog?" (opinião do Claude em 19/11/2026 ~02:00, pedido do dono)
FINAL_TITULO = "PLANO FINAL FECHADO EM 19/11 E ANÁLISE: VALE PARA TESTAR O BLOG? OPINIÃO DO CLAUDE: SIM, PELO MOTIVO CERTO"
FINAL_PLANO = [
    ("Black Friday (plano A)", "20 a 27/11", "R$ 90", "Limite da Meta e comissão até sex 20/11 18:00"),
    ("Black Friday (plano B)", "24 a 27/11", "R$ 50", "Se o plano A não der tempo"),
    ("Natal", "14 a 22/12", "R$ 150", "Só se a BF passar no critério (avaliação 30/11)"),
    ("TETO", "", "R$ 290", ""),
]
FINAL_ANALISE = [
    "<b>Custo baixo e com freio:</b> no pior caso, ≈ R$ 34 gastos e parada em 23/11; no máximo, R$ 240 ao longo de um mês. O Natal só sai se a BF mostrar resultado.",
    "<b>Resposta que vale dinheiro:</b> \"a página curta leva as pessoas ao ML?\" vai ter resposta com número. Se levar, o modelo vai para o blog todo, de graça, e isso vale mais que os R$ 90.",
    "<b>Medição pronta:</b> Pixel, rastreador do blog, gráficos diários e critérios definidos. Desta vez o teste não termina em \"não sei se funcionou\".",
    "<b>O que não esperar:</b> lucro com o anúncio. O teste mede se o blog converte; não é uma máquina de vendas.",
    "<b>Resumo:</b> teste bem montado, barato e com regra de parada. Seja qual for o resultado, em 30/11 o dono sabe o que fazer com o blog em 2027.",
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
    # ===== FORMATO PADRÃO (dono, 19/11/2026): TODA linha = Atividade | Status | Quem | Data e horário.
    # Status só "Pendente" ou "Concluído"; nunca linha sem data E hora (se ainda não há, "Previsto: dia/hora"). O gerador recusa se faltar.
    import re as _re

    def _hora(d, quem):
        if _re.search(r"\d{1,2}:\d{2}", d) or "Previsto" in d:
            return d
        return f"{d} (Previsto: {'20:00' if 'Claude' in quem else '09:00'})"

    def _chave(d):
        m = _re.search(r"(\d{1,2})/(\d{1,2})", d)
        h = _re.search(r"(\d{1,2}):(\d{2})", d)
        hh = (int(h.group(1)), int(h.group(2)) + (1 if "após" in d else 0)) if h else (99, 0)
        return (int(m.group(2)), int(m.group(1)), hh) if m else (12, 31, hh)

    def _linhas_padrao(itens):
        """itens: (atividade, status, quem, data). Valida e ordena por data."""
        out = []
        for atv, stt, quem, dat in itens:
            assert stt in ("Pendente", "Concluído"), f"Status inválido: {stt!r} ({atv[:40]})"
            assert quem and atv and dat, f"Linha sem campo: {atv[:40]}"
            dat = _hora(dat, quem)
            assert _re.search(r"\d{1,2}:\d{2}", dat), f"Linha sem hora: {atv[:40]}"
            out.append((atv, stt, quem, dat))
        return sorted(out, key=lambda x: _chave(x[3]))

    def quadro(titulo, cor, itens):
        linhas = _linhas_padrao(itens)
        verde = VERDE.hexval().replace("0x", "#")
        dados = [[a_, f'<font color="{verde}"><b>{s_}</b></font>' if s_ == "Concluído" else s_, q_, d_] for a_, s_, q_, d_ in linhas]
        t = tabela(["Atividade", "Status", "Quem", "Data e horário"], dados, [0.52, 0.10, 0.18, 0.20], cor=cor)
        for r_, (_, s_, _, _) in enumerate(linhas, start=1):
            if s_ == "Concluído":
                t.setStyle(TableStyle([("BACKGROUND", (0, r_), (-1, r_), VERDE_C)]))
        faixa = Table([[Paragraph(f"<b>{titulo}</b>", ParagraphStyle("fx", parent=TXT, fontSize=11, leading=14, textColor=colors.white))]],
                      colWidths=[LARG], style=[("BACKGROUND", (0, 0), (-1, -1), cor), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)])
        return [faixa, t]

    # 1) o que o dono ainda deve fazer no anúncio (destaque)
    destaque = [("Aprovar a arte e o texto de Natal do anúncio: APROVADO pelo dono, antecipadamente, em 20/11. O Claude prepara a arte e o texto em qui 26/11 20:30 e a troca na Meta fica para a partir de sáb 28/11. Para que serve: o anúncio continua no ar até 22/12 e a mensagem de Black Friday fica velha depois de 27/11",
                 "Concluído", "Dono", "sex 20/11 23:10")]
    # 2) plano do anúncio: o feito fica em verde
    plano = []
    for dat, atv, pl, quem, stt in PLANO_ANUNCIO:
        feito = stt.upper().startswith("FEITO")
        plano.append((f"[{pl}] {atv}", "Concluído" if feito else "Pendente", quem, dat))
    # 3) demais pendências, cada uma com quem e quando (data prevista quando ainda não há)
    demais = [
        ("Agendar no Instagram o Reels de 21/12 (Jogo de Lençol Percal 600 Fios, 19:05). Para que serve: manter um Reels por dia; a janela de agendamento abre 22/11", "Pendente", "Claude (rotina de segunda)", "seg 23/11 20:00"),
        ("Agendar no Instagram o Reels de 23/12 (Cortina de LED 3x3 m, 19:05); a janela abre 24/11", "Pendente", "Claude (rotina de segunda)", "seg 30/11 20:00 (Previsto)"),
        ("\"De acordo\" do dono para corrigir as legendas dos Reels e arquivar os posts repetidos de 11, 13, 16 e 18/11: APROVADO pelo dono", "Concluído", "Dono", "sex 20/11 15:15"),
        ("Corrigir as legendas dos Reels (trocar \"Comente BLACK... Direct\", que promete uma resposta que ninguém manda, por \"Link na bio para ver o produto\" + hashtags) e arquivar, sem apagar, os posts repetidos de 11, 13, 16 e 18/11. Para que serve: não frustrar quem comenta e deixar o perfil limpo", "Pendente", "Claude (rotina de segunda)", "seg 23/11 20:00"),
        ("Validar link e produto dos itens 67 (Suporte de TV) e 181 (Fone Soundcore P30i). Para que serve: não mandar visitante para anúncio errado", "Pendente", "Dono", "seg 23/11 12:00 (Previsto)"),
        ("Decidir a frase \"dieta e alimentação leve\" da legenda da Air Fryer (11/11) e a foto da LG (26/11), que traz \"melhor\" na imagem do fabricante. Para que serve: seguir a política do blog", "Pendente", "Dono", "ter 24/11 12:00 (Previsto)"),
    ]
    st = quadro("ANÚNCIO: O QUE VOCÊ AINDA DEVE FAZER", VERMELHO, destaque)
    st += [Spacer(1, 10)] + quadro("PLANO DO ANÚNCIO (UMA CAMPANHA SÓ: BLACK FRIDAY + NATAL, R$ 240, DE 20/11 A 22/12), EM ORDEM DE DATA: EM VERDE, O QUE JÁ FOI FEITO", AZUL, plano)
    from reportlab.platypus import KeepTogether
    st += [Spacer(1, 10), KeepTogether(quadro("OUTRAS PENDÊNCIAS, CADA UMA COM QUEM, QUANDO E PARA QUE SERVE", LARANJA, demais))]
    st += [Spacer(1, 10), P("Observações", "h2")]
    for o in OBSERVACOES:
        st += [Paragraph("• " + o, TXT), Spacer(1, 4)]
    doc.build(st, onFirstPage=cab_rod, onLaterPages=cab_rod)
    print("PDF:", SAIDA)
    # REGRA DO DONO (19/11/2026): na pasta fica só a versão mais nova; as anteriores vão para old_bkp (nada é apagado)
    pasta = os.path.dirname(SAIDA)
    bkp = os.path.join(pasta, "old_bkp")
    os.makedirs(bkp, exist_ok=True)
    for nome in os.listdir(pasta):
        if nome.startswith(("BLOG - Execução de atividades e planejamento_", "RELATORIO_ATIVIDADE_CLAUDE_BLOG_")) and nome.endswith(".pdf") and nome != os.path.basename(SAIDA):
            destino = os.path.join(bkp, nome)
            if not os.path.exists(destino):
                try:
                    os.replace(os.path.join(pasta, nome), destino)
                    print("movido para old_bkp:", nome)
                except PermissionError:
                    print("AVISO: não consegui mover (arquivo aberto em outro programa; feche e rode de novo):", nome)


if __name__ == "__main__":
    main()
