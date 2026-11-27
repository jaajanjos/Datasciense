# -*- coding: utf-8 -*-
"""RELATÓRIO DE ATIVIDADES do Claude no blog comprenolink.net / Instagram @compre.no.link (formato diário de bordo).
Rodar:  python -X utf8 gerar_relatorio_atividade.py
Saida: D:/Projeto_Blog_Comprenolink/0- Pendencias/4_Relatorio_Ativ_Claude_no_Blog/BLOG - Planejamento e mentoria tecnica_DD_MM_AAAA_HHhMM.pdf
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
SAIDA = rf"D:/Projeto_Blog_Comprenolink/0- Pendencias/4_Relatorio_Ativ_Claude_no_Blog/BLOG - Planejamento e mentoria tecnica_{AGORA:%d_%m_%Y_%Hh%M}.pdf"
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
    ('23/11', '20:20', 'Reels de 21/12 (Jogo de Lençol Casal Percal 600 Fios) AGENDADO; ficaram os demais dias já agendados', 'EXECUTADO', 'Instagram @compre.no.link: Reels seg 21/12/2026 às 19:05, corte Original, legenda sem a promessa de Direct (Link na bio) e terminando só em comprenolink.net (617/2.200). Conferido no calendário mensal após recarregar: 21/12 tem UM Reels às 19:05; 24/11 a 18/12 já estavam agendados. Cópia temporária apagada. Atenção: a ARTE do vídeo desse dia ainda diz Comente NATAL e te mando no Direct.', '', ''),
    ('23/11', '20:25', 'TAREFA EXTRA (trocar legendas Comente BLACK/NATAL e arquivar posts repetidos de 11, 13, 16 e 18/11)', 'PENDENTE', 'Confirmei que o Instagram permite editar a legenda de item agendado (botão Guardar), mas são ~30 itens e o texto precisa ser redigitado um a um; não foi feito nesta rodada para não arriscar legendas erradas. Nada foi alterado nem arquivado. O bloco da tarefa continua ativo.', 'Volume alto de edições manuais + conflito: tarefa pede hashtags, regra de 23/11 pede só comprenolink.net.', 'Dono decide as hashtags; depois executar em lotes por noite'),
    ('24/11', '20:30', 'Proposta de troca do criativo da campanha bf_26_entrada (Black Friday para Natal) PREPARADA', 'EXECUTADO', 'Arquivo 1_Pendencias/PROPOSTA_TROCA_CRIATIVO_NATAL_2026-11-24.md: texto sem preço e sem promessa, imagens existentes (capas Esporte e Fitness / Moda Infantil), passos da troca. Conferido: página 752 abre (200), o texto dela não cita Black Friday (só o item Black Friday do menu do site) e os 2 links meli.la abrem. Nada alterado na Meta nem no site; a CAMP dos gráficos continua bf_26_entrada.', 'Reverificação completa dos 213 anúncios não rodada agora; fazer na sex 27/11 antes da troca.', 'Dono: dar o de acordo para trocar a partir de sáb 28/11'),
]

FALTA_AGENDAR = [
    ("23/12", "Cortina de LED 3x3 m com 300 Luzes e Controle"),
]

# (quando, quem, o que, ganho / observação) – sempre a data mais cedo possível
REEXECUCAO = [
    ("sex 20/11 20:00", "Claude", "BF/Natal 4: só confere o andamento do anúncio (página já publicada em 19/11)", "Tarefa agendada; lê DECISAO_ANUNCIO_BF_2026.md."),
    ("qui 19/11 à noite (anúncio agendado para sex 20/11 00:00)", "Dono", "Criar e publicar o anúncio na Meta (Vendas + SaidaML; R$ 90 de 20/11 00:00 a 27/11 23:59)", "O Claude orienta (MATERIAL_ANUNCIO_BF_2026-11-19.md); publicar e pausar é sempre do dono."),
    ("seg 23/11 20:30", "Claude", "BF/Natal 5: checagem de parada (A) ou publicar a página 752 (B)", "Parar se saída < 3% ou custo por clique de saída > R$ 3."),
    ("seg 30/11 20:00", "Claude", "Agendar o Reels de 21/12 (o de 23/12 já foi agendado em 24/11) quando a janela abrir", "Rotina de segunda."),
    ("quando puder", "Dono", "\"De acordo\" para corrigir as legendas dos Reels e arquivar os posts repetidos de 11, 13, 16 e 18/11", "Legendas prometem resposta no Direct que não existe."),
    ("quando puder", "Dono", "Validar link e produto dos itens 67 (Suporte de TV) e 181 (Fone Soundcore P30i)", ""),
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
    ("seg 23/11 10:08", "Verificação do anunciante na Meta: pendência CONCLUÍDA a pedido do dono em 23/11. O Claude não conferiu a resposta da Meta; se ela pedir um documento melhor ou outra informação, o Claude orienta (não envia dados pessoais por você). Para que serve: o anúncio não ser interrompido por falta de verificação", "BF+Natal", "Dono", "FEITO 23/11"),
    ("sex 20/11 22:32", "Arquivo documento_verificacao_1000px.jpg conferido: já não está mais na pasta Downloads (apagado por você). Para que serve: seu documento não ficar solto no computador", "BF+Natal", "Dono", "FEITO 20/11"),
    ("sex 20/11 23:05", "Rascunho \"Atualizado: Criativo\" do anúncio no Meta DESCARTADO, com o seu OK (foi gerado pelo salvamento automático). Conferido: o anúncio segue ativo. Para que serve: ninguém publicar sem querer uma mudança que ninguém decidiu", "BF+Natal", "Claude, com o OK do dono", "FEITO 20/11"),
    ("seg 23/11 20:30 (Previsto)", "Decidir juntos sobre as 2 sugestões da Meta (vídeo vertical Reels com áudio e música automática). Claude recomenda não aplicar agora: pedem vídeo e hoje o anúncio usa imagem; artes novas ficam para janeiro", "BF+Natal", "Dono e Claude, juntos", "Aguardando"),
    ("sex 20/11 20:35", "Conferência do anúncio feita pelo Claude (só leitura): ativo, R$ 240, gasto de hoje R$ 4,24, alcance de 353 pessoas. A repetição agendada para 21:10 não rodou: o limite de uso do Claude estourou (volta a funcionar a partir de 22:10) e não precisa ser refeita hoje. Para que serve: pegar cedo qualquer problema com o dinheiro", "BF+Natal", "Claude", "FEITO 20/11"),
    ("seg 23/11 09:44", "Mensagem de resumo do anúncio enviada ao dono (rodou às 09:44, atrasada ~44 min porque o app abriu mais tarde): gasto, visitas ao blog e idas ao Mercado Livre de sexta até segunda. Para que serve: saber cedo se o dinheiro está dando resultado", "BF+Natal", "Claude (tarefa agendada)", "FEITO 23/11"),
    ("seg 23/11 09:44", "Conversa aberta com o dono sobre incluir o PDF de gráficos do anúncio nos itens do menu: o Claude apresentou o histórico, as 4 alternativas e recomendou a alternativa 2 (incluir no menu e o Claude registrar a leitura da Meta quando o dono pedir). Para que serve: gerar os relatórios pelo menu, gastando menos do plano", "BF+Natal", "Claude apresentou", "FEITO 23/11"),
    ("seg 23/11 09:55", "Leitura da Meta e do Pixel feita pelo Claude (só leitura) e 2 PDFs gerados na pasta graficos_diarios (1_Pendencias): Gráficos do anúncio bf_26_entrada (gasto R$ 20,07 até 22/11, 1.071 pessoas alcançadas, 8 cliques para o ML pelo site) e Evolução do Pixel (ativo, PageView 64, SaidaML 19). Para que serve: acompanhar se o dinheiro do anúncio está dando resultado", "BF+Natal", "Claude", "FEITO 23/11"),
    ("seg 23/11 10:12", "Tarefa Gráficos diários do anúncio Meta: DECIDIDO pelo dono, opção 1 (deixar como está). Hoje ela rodou às 10:05 e pulou a coleta, porque ainda olha o teste antigo de R$ 50 (concluído); não acompanha o anúncio atual. Para que serve: registrar a escolha; o Claude não mexe na tarefa", "BF+Natal", "Dono e Claude, juntos", "FEITO 23/11"),
    ("seg 23/11 10:22", "Tarefa Evolução do Pixel da Meta rodou sozinha (com o Chrome conectado): Pixel ATIVO, PageView 64 e SaidaML 19 (totais), eventos por dia 25 em 18/11, 9 em 19/11 e 42 em 20/11. A Meta mostra 1 diagnóstico no Pixel, ainda não aberto. Para que serve: ver se a Meta recebe as visitas e idas ao ML do blog", "BF+Natal", "Claude (tarefa agendada)", "FEITO 23/11"),
    ("seg 23/11 10:11", "PDF de gráficos do anúncio no menu: DECIDIDO pelo dono (alternativa 2) e IMPLEMENTADO pelo Claude. Agora o PDF Graficos_Anuncio_bf_26_entrada sai sozinho, com o site de hoje e a última leitura da Meta (data escrita no PDF), toda vez que roda o menu principal [1] e [2] e o submenu [6] -> [1], [2], [3] e [7]. Testado pelo .bat do painel. Para atualizar a Meta, basta pedir ao Claude: atualize a Meta. Para que serve: gerar o relatório pelo menu, gastando menos do plano", "BF+Natal", "Dono e Claude, juntos", "FEITO 23/11"),
    ("seg 23/11 10:35", "Fone do guia (item 48, Coolmusic, comissão 9%): comparados 7 fones no Mercado Livre (só leitura); nenhum paga mais de 9% (marcas conhecidas pagam 5%; o QCY HT05 também paga 9%). DECIDIDO pelo dono: alternativa A, manter o Coolmusic. Para que serve: ganhar o máximo de comissão sem trocar à toa", "BF+Natal", "Dono e Claude, juntos", "FEITO 23/11"),
    ("seg 23/11 15:22", "Hashtag das legendas: testada no Instagram (tocando num post do perfil, a #comprenolinkblog leva a posts aleatórios, não aos seus). DECISÃO FINAL do dono, confirmada aqui: sim, sem hashtag; as legendas terminam só com comprenolink.net. Posts já publicados e Reels já agendados ficam como estão. Para que serve: não levar o seguidor a conteúdo de outros", "BF+Natal", "Dono e Claude, juntos", "FEITO 23/11"),
    ("seg 23/11 10:50", "Legenda do Reels do fone (item 48, terça 24/11 20:00) CORRIGIDA a pedido do dono (vamos fazer agora): tiradas as frases que o anúncio não comprova, entrou bateria de 6 h, estojo e IPX4, Comente BLACK virou Link na bio, hashtag mantida. Feito pelo Claude nos 2 arquivos de texto, com backup. A conversa do Instagram foi avisada e agenda o Reels hoje das 14:00 às 15:30. As artes seguem com Comente BLACK até janeiro. Para que serve: não publicar frase que o anúncio do ML não comprova", "BF+Natal", "Dono e Claude, juntos", "FEITO 23/11"),
    ("seg 23/11 11:16", "Sync de Reels na Página do Facebook (Comprenolink) feita pela conversa BLOG- Pendencia e ajustes em programas: 8 Reels publicados só na Página: 5 das 11:11 às 11:16 (13/11 Cama Box Baú, 16/11 Lavadora Vonder, 18/11 Parafusadeira Vonder, Smartwatch T900 e Caixa de Som Aiwa Boombox) e mais 3 por volta das 11:26 (Árvore de Natal, Khamrah e Pisca Led Natal, que já tinham saído no Instagram; os vídeos vieram dos pacotes de 09/12, 11/12 e 14/12). O Claude conferiu só o arquivo de registro; a publicação foi informada pela outra conversa. Faltam 3 Reels sem vídeo localizado (JBL Go 5 e mais 2). Para que serve: a Página do Facebook ter os mesmos Reels do Instagram", "BF+Natal", "Conversa Pendência/programas (com o dono)", "FEITO 23/11"),
    ("seg 23/11 19:25", "Leitura da Meta atualizada a pedido do dono (só leitura, nada alterado na conta): 20 a 23/11 gastou R$ 28,34 de R$ 240; 5 idas ao Mercado Livre (SaidaML: 1, 3, 1 e 0 hoje); 1.202 pessoas alcançadas; 55 cliques no link; custo por ida ao ML R$ 5,67 (acima do alerta de R$ 3). Gasto de hoje agora é o real (R$ 8,27), não mais estimado. PDF Graficos_Anuncio_bf_26_entrada_23-11-26_19h24 gerado em graficos_diarios. Para que serve: chegar à checagem das 20:30 com números de hoje", "BF+Natal", "Claude (a pedido do dono)", "FEITO 23/11"),
    ("ter 24/11 ~17:00", "REGRA DO DONO sobre o WhatsApp registrada e avisada às 3 outras conversas: sem esforço no WhatsApp (só gerou custo); melhoria ou ajuste só se gerar aumento de venda COMPROVADO, com fato real e evidência (sem hipótese), explicado ao dono antes. A melhoria M5 (canal do WhatsApp no rodapé das categorias, 04/12) foi APAGADA a pedido do dono; memórias duplicadas do WhatsApp unificadas em uma. Para que serve: concentrar o esforço no que gera venda", "Regra geral", "Claude", "FEITO 24/11"),
    ("ter 24/11 20:10", "Reels de 23/12 (Cortina de LED 3x3 m, 19:05) AGENDADO no Instagram (adiantado da rotina de segunda 30/11, pois a janela de 29 dias abriu hoje; opção B, só o Reels) e CONFERIDO no calendário mensal: 23/12 tem UM Reels às 19:05, sem duplicidade. Legenda do pacote corrigida (com backup): saiu \"Comente NATAL... Direct\" e a hashtag; termina só com comprenolink.net. ATENÇÃO: o vídeo em si traz na arte final \"Comente NATAL / que eu te mando no Direct\"; só dá para trocar recriando a arte (previsto para janeiro). Nada alterado na Meta. Para que serve: manter um Reels por dia sem esperar a rotina de segunda", "Instagram", "Claude", "FEITO 24/11"),
    ("qua 25/11 20:15", "Ajustar a verba de R$ 240 e a campanha bf_26_entrada nos programas de leitura e gráficos do anúncio (hoje ainda com R$ 50 do teste antigo); só arquivos locais, com backup e teste, sem Chrome e sem mexer na Meta. CANCELADO a pedido do dono (nunca mais anúncio pago; foco no orgânico). Para que serve: gráficos e leituras com a verba certa", "BF+Natal", "Claude", "CANCELADO 24/11"),
    ("ter 24/11 ~22:00", "VIRADA PARA O ORGÂNICO: o dono decidiu nunca mais anúncio pago; o anúncio bf_26_entrada segue até o fechamento de sáb 28/11 10:00 (sem venda = só pausar); dom 29/11 09:00 linha de confiança no blog; a partir de 29/11, 5 Reels por dia, sem gastar. O dono CONFIRMOU esta conversa como ORQUESTRADORA do plano geral (PDF 22h20): distribui as atividades às 3 conversas a partir de qua 25/11, cobra prazos e junta toda segunda o resumo. Determinação do dono: todas executam o plano na íntegra, obedecem a ajustes e opinam com soluções. Para que serve: tirar o medo de golpe e fazer comprar pelo link, com custo zero", "Virada orgânica", "Claude (orquestra) e todas as conversas", "FEITO 24/11"),
    ("ter 24/11 ~22:30", "ECONOMIA DE TOKENS por ordem do dono: até o fechamento de 28/11 não gastar com o sistema atual (anúncio). DESATIVADAS (não apagadas): leitura do Pixel 10:22, relatório da manhã 12:23, ajuste de verba R$ 240; troca de Natal do anúncio CANCELADA. Equilíbrio do uso do plano Pro combinado com as 4 conversas (leitura: 5h 45%, semanal 32%; adiar se 5h>75% ou semanal>80%; 30 min entre conversas). Critério de viabilidade: orgânico é hipótese, mede-se cliques ao ML pelo rastreador na seg 30/11 e 07/12; 2 semanas sem aumento = reduzir esforço. Para que serve: não estourar o limite e focar no que pode vender", "Virada orgânica", "Claude e dono", "FEITO 24/11"),
    ("ter 24/11 ~23:00", "WhatsApp: sem esforço; só com venda comprovada e evidência real (REGRA); melhoria M5 apagada. Etiqueta de rastreio no link da bio do Instagram AUTORIZADA pelo dono (utm_medium=bio), a ser feita pela conversa do Instagram na sex 27/11 14h–16h. Acionamentos da leitura do rastreador agendados para seg 30/11 e seg 07/12 às 20:35. Para que serve: medir de onde vêm os cliques ao Mercado Livre", "Virada orgânica", "Claude", "Agendado"),
    ("ter 24/11 ~23:30", "PLANO REFORMULADO e APROVADO pelo dono (de acordo): Reels em rampa (fase 1, de 29/11 a 06/12: 2 por dia às 13h30 e 20h00; fase 2 a partir de 07/12: 3 por dia só se o uso do plano estiver abaixo de 60% e os cliques ao ML subirem; 5 por dia só com evidência); coordenação mínima entre conversas (só segundas, 1 linha); leituras do rastreador seg 30/11, 07/12 e 14/12 (3 semanas, tendência), mais leitura parcial qui 03/12 para decidir a fase 2 na sex 04/12; decisão de continuar ou reduzir em 14/12. O dono deu autonomia à orquestradora para ajustar o plano a qualquer momento, alinhando todas as conversas, sem prejuízo do objetivo (venda com calma e constância). Limites sem o dono: anúncio pago (nunca), WhatsApp, gasto de dinheiro, ações irreversíveis, conteúdo fora da política. Para que serve: buscar venda com custo zero e sem estourar o plano", "Virada orgânica", "Claude (orquestra) e todas as conversas", "FEITO 24/11"),
    ("qui 03/12 20:35", "Acionar a conversa 1-PY para a leitura parcial do rastreador (sem Chrome): cliques ao ML por origem e % de uso, para decidir na sex 04/12 se o lote da fase 2 (3 Reels por dia) vale. Sem dado claro, mantém 2 por dia. Para que serve: não aumentar o ritmo sem evidência", "Virada orgânica", "Claude e 1-PY", "Agendado 03/12"),
    ("seg 14/12 20:35", "Acionar a 1-PY para a terceira leitura do rastreador (3 semanas): tendência de cliques ao ML e decisão de continuar, reduzir ou aumentar o ritmo de Reels. Para que serve: decidir com fato, não com hipótese", "Virada orgânica", "Claude e 1-PY", "Agendado 14/12"),
    ("qua 25/11 20:30", "Orquestração: distribuir às 3 conversas as atividades do plano geral da virada orgânica e cobrar prazos (sem Chrome). Chrome: qua 20h–21h Pendência/programas (sync de Reels bons no Facebook); sex 27/11 14h–16h Instagram (agendar Reels). Para que serve: cada conversa saber o que fazer e quando, sem conflito", "Virada orgânica", "Claude (orquestradora)", "FEITO 25/11"),
    ("seg 30/11 21:04 (toda segunda)", "Relatório geral semanal da virada orgânica: junta uma linha de cada conversa (fez, pendente, precisa do dono) e a % de uso do plano; seg 30/11 20:35 e 07/12 20:35 a 1-PY lê o rastreador do blog (linha de base 16–28/11). Para que serve: acompanhar a evolução e decidir se continua", "Virada orgânica", "Claude (orquestradora)", "Agendado"),
    ("ter 24/11 ~20:50", "Conferência do Claude no Meta e no Instagram: Reels das 18:00 (Notebook) e das 20:00 (fone) PUBLICADOS; Reels de 23/12 (Cortina de LED) agendado UMA vez às 19:05, legenda só com comprenolink.net; proposta de Natal do anúncio conferida (sem preço e sem mais vendido/melhor/líder). O dono APROVOU a troca (Sim, trocar 28/11). Como sábado não é dia de trabalho do Claude, a troca foi agendada para sex 27/11 23:30, mas o dono CANCELOU a troca à noite (fechamento do anúncio em 28/11 e foco no orgânico). Para que serve: anúncio de Natal no ar logo após a Black Friday", "BF+Natal", "Claude e dono, juntos", "FEITO 24/11 (troca CANCELADA depois)"),
    ("ter 24/11 ~16:45", "ORDEM do dono: aviso aqui quando o Reels das 18:00 concluir (tarefa de leitura às 18:20) e, como a noite de hoje estava livre, ADIANTAR atividades aprovadas para hoje. Replanejado e agendado: 20:10 Reels de 23/12 no Instagram (era seg 30/11); 20:45 preparo da arte e do texto de Natal do anúncio (era qui 26/11 20:30; a troca na Meta continua só a partir de 28/11 e com de acordo do dono). Regra permanente: dia vago = replanejar e registrar. Para que serve: usar a noite livre e adiantar as pendências", "BF+Natal / Instagram", "Claude", "Agendado 24/11"),
    ("ter 24/11 16:00", "Atividade das 16:00 CONCLUÍDA COM SUCESSO, informada pelo dono: Reels do Instagram de hoje no horário das 16:00 publicado. Registrado pelo Claude (o dono não precisa digitar nada). Falta hoje: os Reels das 18:00 e das 20:00 (fone, item 48), já agendados. Para que serve: manter o ritmo de divulgação do blog", "Instagram", "Dono (informou) e Claude (registrou)", "FEITO 24/11"),
    ("ter 24/11 ~14:00", "Reverificação dos 4 links da página 752 (achados-selecionados) feita: a página responde 200 e os 4 links do Mercado Livre (2 curtos meli.la e 2 de lista) respondem 200, sem aviso de indisponível (só leitura; nada alterado). Limite: o ML carrega os produtos por script, então o 200 mostra que os links estão no ar, não item por item. Para que serve: garantir que quem clica no anúncio chega a uma página que funciona", "BF+Natal", "Claude", "FEITO 24/11"),
    ("ter 24/11 ~13:15", "Sync de 5 Reels do Instagram para a Página do Facebook (Pipoqueira, Máquina de Cortar Cabelo, Lençol, Cortina de LED e Webcam), feita pela conversa Pendência/programas às 12h50–12h55 (adiantada a pedido do dono) e CONFERIDA pelo Claude na lista de publicados do Meta Business Suite (só leitura): os 5 estão na Página, uma vez cada, sem duplicidade (a Webcam de 11:00 é do Instagram, outro perfil); legenda termina só em comprenolink.net. Anúncio e agendamentos não tocados. A leitura Instagram x Página foi feita 12h45–12h55 e a tarefa das 15h foi desativada. Próxima sync: qua 25/11 11h (Reels de 24/11). Para que serve: a Página ter os mesmos Reels do Instagram", "BF+Natal", "Conversa Pendência/programas (com o dono); conferido pelo Claude", "FEITO 24/11"),
    ("ter 24/11 10:23", "Leitura do Pixel rodou sozinha (10:22) com sucesso: Pixel ATIVO; PageView 68 (era 64, +4); SaidaML 19 (igual a ontem); eventos por dia 18/11=25, 19/11=9, 20/11=42, 21/11=5, 22/11=5. Linha de 24/11 gravada no pixel_evolucao.csv (cópia em old_bkp). Para que serve: ver se o Pixel continua contando as idas ao Mercado Livre", "BF+Natal", "Claude (tarefa agendada)", "FEITO 24/11"),
    ("ter 24/11 ~11:00", "Aviso de diagnóstico do Pixel aberto e lido (só leitura, aba fechada): pede para confirmar o domínio comprenolink.net na lista de permissões (detectado em 23/11). Parecer do Claude: deixar como está, pois adicionar à lista pode bloquear eventos de outros domínios; o Pixel segue ativo. Para que serve: não arriscar um Pixel que está funcionando", "BF+Natal", "Claude (a pedido do dono)", "FEITO 24/11"),
    ("ter 24/11 ~10:00", "Tarefa agendada \"Gráficos diários do anúncio Meta\" (10:06) RETIRADA da agenda a pedido do dono: desativada, não apagada. Para que serve: gráficos só pelo menu ou com \"atualize a Meta\", gastando menos do plano", "BF+Natal", "Dono decidiu, Claude desativou", "FEITO 24/11"),
    ("ter 24/11 12:23", "Relatório da manhã (12:10): Pixel rodou 10:22 com sucesso; Gráficos das 10:06 não rodaram por decisão do dono (tarefa desativada, só pelo menu); nenhuma falha a corrigir. Para que serve: conferir que a manhã foi cumprida", "BF+Natal", "Claude (tarefa agendada)", "FEITO 24/11"),
    ("ter 24/11 ~10:30", "Alinhamento de agenda com a conversa Pendência/programas: ela usa o Chrome hoje às 15h só para ler Reels do Instagram x Página do Facebook (sem mexer no anúncio nem em agendamentos); sem conflito com a agenda do Claude; o OK final é do dono dentro da conversa dela. Para que serve: não haver choque de Chrome", "BF+Natal", "Dono e Claude, juntos", "FEITO 24/11"),
    ("seg 23/11 11:10", "Agenda de hoje à noite conferida e mantida pelo Claude com o dono: o Reels do fone (24/11 20:00) é agendado só pela conversa do Instagram (para não duplicar), a rotina de Reels de segunda às 20:00 leva só 4 a 6 minutos e a checagem do anúncio às 20:30 começa depois, sem disputar o Chrome; agendar Reels não mexe no anúncio pago. Para que serve: não duplicar Reels e não atrapalhar o anúncio nem as vendas", "BF+Natal", "Dono e Claude, juntos", "FEITO 23/11"),
    ("seg 23/11 11:45", "Reels do fone (item 48, terça 24/11 20:00) AGENDADO pela conversa do Instagram e CONFERIDO pelo Claude na lista de agendados do Meta Business Suite (só leitura): legenda corrigida (6 h de bateria, estojo, IPX4, Link na bio), termina só em comprenolink.net, sem hashtag; só no Instagram. Também agendados 5 Reels de 24/11, 5 de 25/11 e 2 de 26/11; faltam 3 de 26/11 (16:00, 18:00 e 20:00), porque o Meta travou o envio de vídeo e a conversa tenta de novo hoje. Para que serve: o texto correto sair no ar", "BF+Natal", "Conversa BLOG- Ajustes no WhatsApp e Instagram", "FEITO 23/11"),
    ("seg 23/11 15:06", "Os 3 Reels que faltavam de quinta 26/11 (16:00 espelho, 18:00 kit parafusadeira, 20:00 caixa de ferramentas) foram AGENDADOS pela conversa do Instagram e CONFERIDOS pelo Claude na lista de agendados do Meta (só leitura): quinta 26/11 tem os 5 horários (11:00, 13:30, 16:00, 18:00, 20:00). Total agendado hoje por ela: 15 Reels (5 de terça 24/11, 5 de quarta 25/11, 5 de quinta 26/11). Legendas só com comprenolink.net. O anúncio pago não foi tocado. Para que serve: manter um Reels por dia", "BF+Natal", "Conversa BLOG- Ajustes no WhatsApp e Instagram", "FEITO 23/11"),
    ("seg 23/11 15:14", "Reels de sexta 27/11 (Black Friday) AGENDADOS pela conversa do Instagram (11:00 halteres, 13:30 barra fixa, 16:00 kit 20 itens, 18:00 skincare, 20:00 inalador) e CONFERIDOS pelo Claude na lista de agendados do Meta (só leitura): os 5 horários existem. Total agendado hoje por ela: 20 Reels (24, 25, 26 e 27/11, 5 por dia). Chrome liberado antes das 20:00. Anúncio pago não tocado. ATENÇÃO: várias legendas agendadas (ex.: o inalador) ainda dizem Comente BLACK que eu te mando o link no Direct; só a do fone (item 48) foi corrigida. Para que serve: manter a fila de Reels e liberar o Chrome para a noite", "BF+Natal", "Conversa BLOG- Ajustes no WhatsApp e Instagram", "FEITO 23/11"),
    ("seg 23/11 15:20", "Legendas dos Reels agendados de 24 a 27/11 com Comente BLACK que eu te mando o link no Direct: DECIDIDO pelo dono, opção B (deixar como está, conforme a decisão anterior de manter os já agendados até 02/12). Só a do fone (item 48) foi corrigida. Nada alterado. Para que serve: registrar a escolha e não mexer em Reels já agendados", "BF+Natal", "Dono e Claude, juntos", "FEITO 23/11"),
    ("seg 23/11 11:00", "Diagnóstico do Pixel lido pelo Claude (só leitura): a Meta avisa que o domínio comprenolink.net começou a enviar dados e pede para confirmar que é seu, adicionando-o à lista de permissões. Para que serve: saber o que o aviso significa", "BF+Natal", "Claude", "FEITO 23/11"),
    ("seg 23/11 11:00", "Aviso do Pixel sobre o domínio comprenolink.net: DECIDIDO pelo dono, opção 1 (deixar como está). O Claude não criou a lista de permissões, porque ela bloqueia todo domínio que não esteja nela e a Meta diz que nenhuma ação é necessária; nada foi alterado na Meta. Para que serve: não correr o risco de parar a contagem de visitas do anúncio", "BF+Natal", "Dono e Claude, juntos", "FEITO 23/11"),
    ("seg 23/11 10:20", "Validação das 4 trocas de 21/11 no guia, feita pelo Claude com o dono (só leitura no Mercado Livre): item 12 OK sem mudanças (comissão 21%); item 41 corrigido (tiradas as frases forno e 4 travas, que o anúncio não confirma; comissão 12%); item 48 corrigido (texto agora com bateria de 6 h, estojo e proteção IPX4; comissão 9%); item 65 corrigido (frete grátis com texto prudente). Política sem preço continua OK. Para que serve: não mandar visitante a um produto diferente do descrito", "BF+Natal", "Dono e Claude, juntos", "FEITO 23/11"),
    ("seg 23/11 a ter 22/12, seg a sex 10:22", "Leitura do Pixel (a tarefa dos gráficos diários das 10:06 foi RETIRADA da agenda a pedido do dono em 24/11; gráficos só pelo menu ou com \"atualize a Meta\"). Para que serve: acompanhar todo dia se o dinheiro está trazendo resultado", "BF+Natal", "Claude (tarefa agendada)", "Agendado"),
    ("seg 23/11 20:30", "Checagem do anúncio RODOU com sucesso (nada alterado na Meta): gasto R$ 28,34; 5 idas ao ML pelo Pixel (cerca de 8 pelo rastreador); taxa de saída boa (acima de 3% das visitas); custo por ida R$ 5,67 (Pixel) ou cerca de R$ 3,54 (rastreador), acima de R$ 3, com poucos dados (menos de 50 visitas). DECISÃO do dono e do Claude juntos: manter o anúncio e voltar ao assunto na segunda 30/11 às 20:30 com a semana inteira da Black Friday. Pendência da checagem: reverificar os 4 links do blog (o verificador estourou o tempo; a página 752 responde 200), refeita pela rotina das 10:00. Para que serve: decidir com dados, sem pausar cedo demais", "BF+Natal", "Claude e dono, juntos", "FEITO 23/11"),
    ("qui 26/11 20:30", "Preparar a arte e o texto de Natal do anúncio. Para que serve: depois de 27/11 a palavra Black Friday fica velha e piora os cliques", "Natal", "Claude prepara, dono aprova", "Agendado"),
    ("sáb 28/11 (Previsto: 10:00)", "Trocar a arte de Black Friday pela de Natal na Meta, só com o de acordo do dono", "Natal", "Dono (ou Claude, se o dono pedir)", "Aguardando"),
    ("seg 30/11 20:30", "Resultado da semana da Black Friday (20 a 27/11) e recomendação: manter, ajustar ou pausar. Decisão junto com o dono", "BF+Natal", "Claude analisa, dono decide", "Agendado"),
    ("qui 17/12 20:00", "Checagem de dezembro: está valendo a pena? Cinco dias antes do fim, os números de dezembro para decidir juntos se vai até 22/12", "Natal", "Claude avisa, dono e Claude decidem", "Agendado"),
    ("ter 22/12 20:00 (ou quando o anúncio parar antes, por qualquer motivo)", "MUDANÇA DE ESTRATÉGIA (assunto importante pré-definido): quando o anúncio pago terminar (22/12 23:59) ou parar antes, entra 5 Reels por dia, orgânico puro, Instagram primeiro, depois Facebook, WhatsApp fora. AGENDADO: tarefa nova em 22/12 às 20:00 e aviso acrescentado nas tarefas de 17/12, 30/11 e 28/12; o Claude abre o aviso com a frase MUDANÇA DE ESTRATÉGIA e força o assunto. A conversa dos Reels prepara o 1º lote a partir de ~14/12. Facebook: esforço mínimo, sem apagar a Página. Para que serve: não perder o ritmo de divulgação quando o anúncio acabar", "BF+Natal", "Claude avisa e força; dono decide", "Agendado"),
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
            assert stt in ("Pendente", "Concluído", "Em andamento"), f"Status inválido: {stt!r} ({atv[:40]})"
            assert quem and atv and dat, f"Linha sem campo: {atv[:40]}"
            dat = _hora(dat, quem)
            assert _re.search(r"\d{1,2}:\d{2}", dat), f"Linha sem hora: {atv[:40]}"
            out.append((atv, stt, quem, dat))
        return sorted(out, key=lambda x: _chave(x[3]))

    def quadro(titulo, cor, itens):
        linhas = _linhas_padrao(itens)
        verde = VERDE.hexval().replace("0x", "#")
        dados = [[a_, f'<font color="{verde}"><b>{s_}</b></font>' if s_ == "Concluído" else (f'<font color="#A16207"><b>{s_}</b></font>' if s_ == "Em andamento" else s_), q_, d_] for a_, s_, q_, d_ in linhas]
        t = tabela(["Atividade", "Status", "Quem", "Data e horário"], dados, [0.52, 0.10, 0.18, 0.20], cor=cor)
        for r_, (_, s_, _, _) in enumerate(linhas, start=1):
            if s_ == "Concluído":
                t.setStyle(TableStyle([("BACKGROUND", (0, r_), (-1, r_), VERDE_C)]))
            elif s_ == "Em andamento":
                t.setStyle(TableStyle([("BACKGROUND", (0, r_), (-1, r_), colors.HexColor("#FEF08A"))]))
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
        ("\"De acordo\" do dono para corrigir as legendas dos Reels e arquivar os posts repetidos de 11, 13, 16 e 18/11: APROVADO pelo dono", "Concluído", "Dono", "sex 20/11 15:15"),
        ("Corrigir as legendas dos Reels (trocar \"Comente BLACK... Direct\", que promete uma resposta que ninguém manda, por \"Link na bio para ver o produto\" + hashtags) e arquivar, sem apagar, os posts repetidos de 11, 13, 16 e 18/11. Para que serve: não frustrar quem comenta e deixar o perfil limpo", "Pendente", "Claude (rotina de segunda)", "seg 23/11 20:00"),
        ("Validar link e produto dos itens 67 (Suporte de TV) e 181 (Fone Soundcore P30i): VALIDADOS pelo Claude com o dono em 23/11 (só leitura no Mercado Livre). Item 67: 10 a 100 polegadas, até 80 kg, 3 cm da parede, kit completo e aço carbono, tudo confirmado; comissão 5%. Item 181: Bluetooth 5.4, conexão dupla, cancelamento de ruído adaptativo, modo 3D pelo app, estojo 2 em 1 com suporte para celular e 45 h, tudo confirmado; comissão 5%. Nenhuma mudança no guia. Para que serve: não mandar visitante a produto errado", "Concluído", "Dono e Claude, juntos", "seg 23/11 11:05"),
        ("Air Fryer (frase \"dieta e alimentação leve\") e foto da LG (\"melhor\" na imagem do fabricante): SOLUCIONADO, informado pelo dono em 24/11. Para que serve: seguir a política do blog", "Concluído", "Dono", "ter 24/11"),
    ]
    novo = [
        ('Conferência (só leitura) dos Reels de terça 24/11: saíram os 5 (11:00, 13:30, 16:00, 18:00 e 20:01), com métricas; calendário mensal conferido (sem risco de duplicar)', 'Concluído', 'B | BLOG- Ajustes Instagram', 'qua 25/11 20:10'),
        ('Backup das conversas: rodízio mudou para 1 por dia nos últimos 31 dias (programa novo testado) e backup de hoje feito', 'Concluído', 'JOSE + C | BLOG - Planejamento e mentoria técnica', 'qua 25/11 08:13'),
        ('Nomes dos PDFs de todas as conversas ajustados para os nomes novos (A, B e C)', 'Concluído', 'A/B/C | todas as conversas', 'qua 25/11 08:45'),
        ('Pasta dos Reels novos definida e aprovada: REELS_NOVO_BLOG (01_AMOSTRA e 02_LOTE_29-11_a_06-12)', 'Concluído', 'B | JOSE + BLOG- Ajustes Instagram', 'qua 25/11 09:20'),
        ('Visual novo dos Reels: amostra aprovada por você (estilo limpo, identidade própria do blog)', 'Concluído', 'B | JOSE + BLOG- Ajustes Instagram', 'qua 25/11 09:30'),
        ('1º lote de 16 Reels (2 por dia, 29/11 a 06/12) gerado e aprovado por você', 'Concluído', 'B | BLOG- Ajustes Instagram', 'qua 25/11 09:40'),
        ('MENTORIA TÉCNICA da Execução: orienta as conversas e revisa resultados quando pedirem; coordena Chrome e uso do plano (uma atividade por vez). Para que serve: cada conversa executar sem sobrecarregar ninguém', "Em andamento", 'C | BLOG - Planejamento e mentoria técnica', 'qua 25/11 09:00 (contínuo)'),
        ('MISSÃO DOS REELS: a conversa do Instagram é a dona de todos os dias de Reels que faltam para completar o ciclo, o mais cedo possível, em lotes semanais. Você fala direto com ela e acompanha. Para que serve: uma dona só, sem duplicar', "Em andamento", 'B | JOSE + BLOG- Ajustes Instagram', 'qua 25/11 09:00 (contínuo)'),
        ('Sync dos Reels bons do Instagram para a Página do Facebook, com os vídeos que você escolher. Para que serve: aproveitar o que já funciona, sem gastar à toa', "Pendente", 'A | JOSE + BLOG - Execução de atividades', 'sex 27/11 15:20 a 16:00 (replanejada: na quarta você não escolheu os vídeos)'),
        ('Distribuir as atividades às 3 conversas e cobrar prazos. Para que serve: cada uma fazer só a sua parte, sem conflito de Chrome. Todas confirmaram', "Concluído", 'C | BLOG - Planejamento e mentoria técnica', 'qua 25/11 20:37'),
        ('Agendar 12 Reels do 1º lote no Meta Business Suite com você presente (você escolhe os arquivos na janela do Windows) e trocar o link da bio com UTM, conferindo que abre o blog. Datas: 13h30 só em 29/11, 30/11, 02/12 e 04/12; 13h30 e 20h00 em 01/12, 03/12, 05/12 e 06/12. Informa o % de uso antes e depois; para sozinho se passar de 75% (5h) ou 80% (semana). Para que serve: Reels no ar e medir de onde vêm os cliques', "Pendente", 'B | JOSE + BLOG- Ajustes Instagram', 'sex 27/11 14:00 a 15:15 (janela até 16:00)'),
        ('Fechamento do anúncio bf_26_entrada: sem venda, só pausar. A resposta começa com PAUSEI ou NÃO pausei. Para que serve: parar de gastar sem resultado', "Pendente", 'D | 1- PY- Prog gerador gráfico de anúncio META - BLOG', 'sáb 28/11 10:00'),
        ('Conferir a pausa do anúncio na Meta (se a resposta disser NÃO CONSEGUI PAUSAR, pausar você mesmo). Para que serve: garantir que não gasta mais', "Pendente", 'JOSE (só lê a 1ª linha da resposta da 1- PY, sem conversar)', 'sáb 28/11 10:30'),
        ('Linha de confiança no blog: "Você compra direto no site oficial do Mercado Livre...". Para que serve: tirar o medo de golpe e fazer comprar pelo link', "Pendente", 'D | 1- PY- Prog gerador gráfico de anúncio META - BLOG', 'dom 29/11 09:00'),
        ('Começam os Reels do orgânico (2 por dia), conferidos só em leitura às 20:30. Para que serve: constância na divulgação, custo zero', "Pendente", 'B | BLOG- Ajustes Instagram', 'dom 29/11 13:30 (e 20:00)'),
        ('Leitura do rastreador (cliques ao ML por origem) contra a linha de base de 16 a 28/11, acionada pela Execução. Para que serve: saber se o orgânico traz cliques', "Pendente", 'D | 1- PY- Prog gerador gráfico de anúncio META - BLOG', 'seg 30/11 20:35'),
        ('Relatório geral semanal: 1 linha de cada conversa e % de uso do plano. Para que serve: você ler um lugar só', "Pendente", 'C | BLOG - Planejamento e mentoria técnica', 'seg 30/11 21:04 (toda segunda)'),
        ('Melhorias M1+M3+M7 no blog: botão único, imagens com tamanho fixo, rótulo "Ver preço" trocado (roda sozinha, com backup). Para que serve: mais cliques ao Mercado Livre', "Pendente", 'Tarefa agendada (executa)', 'ter 01/12 20:00'),
        ('Melhoria M2: "Links verificados em DD/MM" nas categorias e no guia (roda sozinha, com backup)', "Pendente", 'Tarefa agendada (executa)', 'qua 02/12 20:00'),
        ('Conferir no blog as melhorias M1+M3+M7 e M2 (só leitura) e avisar a Execução em 1 linha. Para que serve: garantir que nada quebrou', "Pendente", 'A | BLOG - Execução de atividades', 'qua 02/12 20:30'),
        ('Gerar o 2º lote de Reels (14, fase 1)', "Pendente", 'B | BLOG- Ajustes Instagram', 'qui 03/12 20:00'),
        ('Leitura parcial do rastreador, acionada pela Execução. Para que serve: decidir a fase 2 sem hipótese', "Pendente", 'D | 1- PY- Prog gerador gráfico de anúncio META - BLOG', 'qui 03/12 20:35'),
        ('Agendar o 2º lote com você e decidir a fase 2 (3 Reels por dia só se o uso do plano estiver abaixo de 60% e os cliques subirem)', "Pendente", 'B | JOSE + BLOG- Ajustes Instagram', 'sex 04/12 14:00 a 16:00'),
        ('Agendar os 4 Reels que sobraram do 1º lote (junto com o 2º lote); pode adiantar para 07/12 em diante na janela de 27/11 só com o seu OK', "Pendente", 'B | JOSE + BLOG- Ajustes Instagram', 'sex 04/12 14:00 a 16:00'),
        ('Avaliar com você as legendas antigas que prometem Direct nos Reels já agendados (corrigir os mais próximos ou deixar rodar)', "Pendente", 'B | JOSE + BLOG- Ajustes Instagram', 'seg 07/12 20:00'),
        ('2ª leitura do rastreador, acionada pela Execução', "Pendente", 'D | 1- PY- Prog gerador gráfico de anúncio META - BLOG', 'seg 07/12 20:35'),
        ('Melhoria M4: piloto de 3 a 5 destaques em Áudio e TV (roda sozinha; publica só com a sua prévia)', "Pendente", 'JOSE, na tarefa M4 (ela abre sozinha e pede a prévia)', 'ter 08/12 20:00'),
        ('Conferir o piloto M4 no blog (só leitura) e avisar a Execução em 1 linha', "Pendente", 'A | BLOG - Execução de atividades', 'qua 09/12 20:30'),
        ('Seu texto de "quem somos e como escolhemos" para a melhoria M6', "Pendente", 'C | JOSE + BLOG - Planejamento e mentoria técnica', 'qui 10/12 20:00'),
        ('Gerar e agendar o 3º lote de Reels com você', "Pendente", 'B | JOSE + BLOG- Ajustes Instagram', 'sex 11/12 14:00 a 16:00'),
        ('Melhoria M6: bloco de confiança nas categorias, com o seu texto (roda sozinha, com backup)', "Pendente", 'Tarefa agendada (executa)', 'sex 11/12 20:00'),
        ('3ª leitura do rastreador (3 semanas, tendência), acionada pela Execução', "Pendente", 'D | 1- PY- Prog gerador gráfico de anúncio META - BLOG', 'seg 14/12 20:35'),
        ('Decidir com você: continuar, reduzir ou ampliar o ritmo de Reels, com os números de 3 semanas. Para que serve: decidir com fato, não com hipótese', "Pendente", 'C | JOSE + BLOG - Planejamento e mentoria técnica', 'seg 14/12 21:00'),
        ('Black Friday no blog (home, menu, página própria e "alertas"): trocar por Natal, sem apagar a página, com backup. APROVADO por você em 26/11. Para que serve: promoção vencida perde a confiança e a Amazon proíbe', "Pendente", 'Tarefa agendada (executa) | C valida', 'seg 30/11 20:05'),
        ('Guia do blog: padronizar os 639 links que estão sem "nofollow" (junto da melhoria M2, com backup). Para que serve: cumprir a regra de link patrocinado antes da Amazon', "Pendente", 'A | BLOG - Execução de atividades', 'qua 02/12 20:00 (com a M2)'),
        ('Decisão da Amazon (4 condições, conferidas com o Guia de Conformidade) e, se aprovada, você cria a conta só quando o blog estiver pronto (o prazo de 180 dias para 3 vendas começa no cadastro) e cadastra os canais (site, Instagram, Facebook). Para que serve: venda de canal não cadastrado não conta', "Pendente", 'C | JOSE + BLOG - Planejamento e mentoria técnica', 'ter 22/12 (decisão); jan/2027 (conta)'),
        ('AMAZON, janeiro/2027: frase "Como Associado da Amazon, eu ganho com compras qualificadas." no rodapé; parágrafo na Política e no Sobre; só links amzn.to ou amazon.com.br com tag; sem preço; nunca Amazon em e-mail/WhatsApp; evento SaidaAmazon; teste de 5 a 10 produtos. Para que serve: entrar na Amazon dentro das regras', "Pendente", 'A + D | com seu de acordo', 'jan/2027 (depois de 22/12)'),
        ('REGRAS DE OURO da Amazon (Guia de Conformidade): nenhuma compra sua, de familiares ou da mesma rede pelos links (invalida e bloqueia); só contam 3 vendas de clientes reais em 180 dias; sem preço digitado (preço só pela API, em até 24h); sem imagem baixada do site da Amazon (foto própria, do fabricante ou da API); links só amzn.to ou amazon.com.br com tag; nada em WhatsApp, Direct, SMS ou e-mail; botões Amazon e ML podem ficar lado a lado com texto limpo. Para que serve: não perder a conta por erro simples', "Em andamento", 'C | JOSE + BLOG - Planejamento e mentoria técnica', 'contínuo até jan/2027'),
    ]
    st = quadro("NOVO PLANO (VIRADA PARA O ORGÂNICO, 29/11), EM ORDEM DE DATA. A = BLOG - Execução de atividades; B = BLOG- Ajustes Instagram; C = BLOG - Planejamento e mentoria técnica; D = 1- PY- Prog gerador gráfico de anúncio META - BLOG", AZUL, novo)
    doc.build(st, onFirstPage=cab_rod, onLaterPages=cab_rod)
    print("PDF:", SAIDA)
    # REGRA DO DONO (19/11/2026): na pasta fica só a versão mais nova; as anteriores vão para old_bkp (nada é apagado)
    pasta = os.path.dirname(SAIDA)
    bkp = os.path.join(pasta, "old_bkp")
    os.makedirs(bkp, exist_ok=True)
    for nome in os.listdir(pasta):
        if nome.startswith(("BLOG - Planejamento e mentoria tecnica_", "BLOG - Execução de atividades e planejamento_", "RELATORIO_ATIVIDADE_CLAUDE_BLOG_")) and nome.endswith(".pdf") and nome != os.path.basename(SAIDA):
            destino = os.path.join(bkp, nome)
            if not os.path.exists(destino):
                try:
                    os.replace(os.path.join(pasta, nome), destino)
                    print("movido para old_bkp:", nome)
                except PermissionError:
                    print("AVISO: não consegui mover (arquivo aberto em outro programa; feche e rode de novo):", nome)


if __name__ == "__main__":
    main()
