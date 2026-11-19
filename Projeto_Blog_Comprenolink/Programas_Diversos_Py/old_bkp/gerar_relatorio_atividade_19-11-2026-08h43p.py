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
    ('30/10', '20:47', 'ATENÇÃO: a arte e o vídeo de 28/11 trazem textos que a política do blog evita ("MELHOR CUSTO-BENEFÍCIO" no selo e, no Reels, "Um dos mais vendidos e bem avaliados do Mercado Livre")', 'PARCIAL', 'Agendei mesmo assim porque a rotina foi aprovada pelo dono com estas artes e a publicação só ocorre em 28/11, quase um mês à frente; dá tempo de trocar. Não alterei nenhuma arte sem o OK do dono. Se o dono aprovar, regeno feed.png e reels.mp4 sem esses termos e substituo o agendamento de 28/11 (e de 25/11 e 26/11, que já tinham "Melhor").', 'Aguardando OK do dono', 'assim que o dono responder'),
    ('04/11', '19:17', 'WhatsApp Canal: não publicado', 'NÃO EXECUTADO', 'O pacote de 04/11 não tem bloco 19:20 Canal.', 'Sem bloco 19:20 no pacote', 'Nenhuma'),
    ('04/11', 'noite', 'Segundo administrador no Canal (sócio) e página comprenolink.net/canal; alinhar o 2º chip Claro pré-pago (aparelho dual SIM)', 'NÃO EXECUTADO', 'Combinado com o dono para o dia seguinte.', 'Depende do dono (administrador) e da compra do chip.', 'qui 05/11'),
    ('06/11', '19:17', 'WhatsApp Canal 19:20', 'NÃO EXECUTADO', 'Não publicado.', 'O pacote de hoje não tem o bloco 19:20 (regra: só publica no Canal se houver).', ''),
    ('19/11', '00:59', 'Conferência das tarefas agendadas (conversa nova: BLOG - Execução de atividades e planejamento)', 'EXECUTADO', 'Esta conversa assumiu tudo da "Atividades Claude e Planejamento" (passagem registrada nas anotações). Conferi as tarefas agendadas: as 3 da noite de 18/11 (BF/Natal 2, Pixel, Melhorias M0) terminaram com sucesso; as 5 de hoje (10:06, 10:22, 12:23, 20:00 e 20:30) estão ativas. Nenhuma tarefa cita a conversa antiga.', '', ''),
    ('19/11', '01:15', 'Anúncio Black Friday: decisão do dono ("DE ACORDO") aplicada às tarefas', 'EXECUTADO', 'Plano A: R$ 90 de 20 a 27/11 (≈ R$ 11,25/dia), se até sex 20/11 18:00 o limite da Meta (≥ R$ 90) e a comissão dos 5 itens estiverem resolvidos; senão plano B: R$ 50 de 24 a 27/11. Natal R$ 100 mantido e condicional. Criado 1_Pendencias/DECISAO_ANUNCIO_BF_2026.md e ajustadas 4 tarefas (aviso 20/11 09:00, BF/Natal 4, aviso 23/11 09:00, BF/Natal 5), com cópia em old_bkp. Nada alterado na Meta nem no site.', '', 'Dono: limite da Meta e comissão até sex 20/11 18:00'),
    ('19/11', '01:50', 'Anúncio de Natal alterado pelo dono e aplicado às tarefas', 'EXECUTADO', 'Natal = R$ 150 de 14 a 24/12 (substitui R$ 100 de 03 a 14/12), só se a BF passar; anúncio vai até 24/12. Teto sobe para R$ 290 (acumulado possível R$ 289,67). DECISAO_ANUNCIO_BF_2026.md atualizado; tarefas: BF/Natal 6 (30/11) ajustada, BF/Natal 7 movida para 28/12, Pixel diário estendido até 28/12, criadas natal-preparo-11-12 e natal-parada-17-12. Backups em old_bkp.', '', 'Dono: seg 14/12 subir o limite em + R$ 150 e criar o anúncio (se aprovado)'),
    ('19/11', '02:00', 'Fim do anúncio de Natal antecipado para 22/12 (decisão do dono)', 'EXECUTADO', 'Natal = R$ 150 de 14 a 22/12 (≈ R$ 16,67/dia), mesma verba e mesmo teto (R$ 290). Atualizados DECISAO_ANUNCIO_BF_2026.md, BF/Natal 6 e 7, natal-preparo-11-12, natal-parada-17-12 e este relatório; backups em old_bkp.', '', ''),
    ('19/11', '02:20', 'Página de entrada 752 (rascunho): 5 itens trocados por moda e calçados, de comissão mais alta', 'EXECUTADO', 'A pedido do dono, saíram TV LG, soundbar JBL, Fire TV Stick e fone QCY; entraram Tênis Olympikus Veloz 3 (211), Kit 2 Bermudas Femininas (103), Kit 3 Leggings (36) e Kit 5 Conjuntos Infantil Menino (161); ficou o Kit 4 Bermudas (49). Motivo: nas vendas passadas, moda e calçados pagaram 17% a 21% (Kit 4 Bermudas Jeans 21%, tênis 20%, chinelo 17%), e eletrônicos nunca venderam, então a taxa deles é desconhecida. Os 5 itens estão Ativos (HTTP 200 em 18/11), sem preço e sem termos proibidos; a página continua em RASCUNHO. Backups em paginas_novas/old_bkp (inclui o conteúdo anterior do WP). Tarefas BF/Natal 4 e 5, aviso de 20/11 e DECISAO_ANUNCIO_BF_2026.md atualizados.', 'A comissão real de cada item só aparece no painel do ML Afiliados; os percentuais acima vêm de vendas antigas de itens parecidos.', 'Dono: conferir a comissão até sex 20/11 18:00'),
    ('19/11', '08:00', 'Página de entrada 752 (rascunho): Kit 4 Bermudas Tactel retirado a pedido do dono', 'EXECUTADO', 'A página agora tem 4 itens: Tênis Olympikus Veloz 3, Kit 2 Bermudas Femininas, Kit 3 Leggings e Kit 5 Conjuntos Infantil Menino. Continua em RASCUNHO, sem preço. Tarefas BF/Natal 4 e 5, avisos de 20 e 23/11 e DECISAO_ANUNCIO_BF_2026.md ajustados de 5 para 4 itens; backups em old_bkp.', '', 'Dono: conferir a comissão dos 4 itens até sex 20/11 18:00'),
    ('19/11', '08:23', 'Substituição automática de anúncios (verificação dos 213 anúncios no ML, validação e painel)', 'EXECUTADO', 'Verificação às 08:15: 213 de 213 ativos, 0 precisam de substituto; por isso o passo com o Chrome e o ML Afiliados não rodou e não houve troca nem Reels a reagendar. Regra de maior comissão (ranking dos afiliados, dentro da política) já está no roteiro para a próxima vez. Política do blog: nenhum preço e textos dentro da política. Painel Painel_conversao_performance_2026-11-19_08h21.pdf, planilha e resumo atualizados.', '', ''),
    ('19/11', '08:50', 'Limite de gastos da conta Meta (Compre no Link - Anúncios) subido de R$ 50 para R$ 150', 'EXECUTADO', 'Com o "pode fazer" do dono, abri Faturamento e pagamentos > Limite de gastos da conta > Alterar, digitei 150 e salvei. A Meta confirmou: limite mensal R$ 150,00; gasto R$ 49,67; saldo R$ 100,33; reinicia no dia 1º. Visa final 0442 válida (vence 12/2032). O limite precisava cobrir o gasto de novembro (R$ 49,67) mais o anúncio de R$ 90. Em 14/12 será preciso subir de novo para o Natal. Nada mais foi alterado na Meta.', '', 'Dono: em 14/12, subir o limite para o Natal'),
    ('19/11', '01:18', 'Relatório de atividades: 1ª geração do dia', 'EXECUTADO', 'Regra permanente aplicada: saíram os 8 sucessos de 18/11; ficaram as 15 pendências; plano de reexecução refeito só com ações em aberto; dias sem agendar = 18/12, 21/12 e 23/12.', '', ''),
]

FALTA_AGENDAR = [
    ("18/12", "Máquina de Cortar Cabelo e Barba Sem Fio Nixzen (tarefa hoje 19/11 20:30)"), ("21/12", "Jogo de Lençol Casal Percal 600 Fios 4 Peças"),
    ("23/12", "Cortina de LED 3x3 m com 300 Luzes e Controle"),
]

# (quando, quem, o que, ganho / observação) – sempre a data mais cedo possível
REEXECUCAO = [
    ("sex 20/11 até 18:00", "Dono", "Conferir a comissão dos 4 itens da página 752 no ML (o limite da Meta já foi ajustado para R$ 150)", "Sem isso o plano A (R$ 90, 20 a 27/11) não sai e vale o plano B (R$ 50, 24 a 27/11). Responder \"feito\" para registrar."),
    ("sex 20/11 20:00", "Claude", "BF/Natal 4: plano A publica a página 752 e entrega o material; plano B prepara o anúncio de R$ 50", "Tarefa agendada; lê DECISAO_ANUNCIO_BF_2026.md."),
    ("sex 20/11 após 20:00 (A) ou seg 23/11 até 12:00 (B)", "Dono", "Criar e publicar o anúncio na Meta (Vendas + SaidaML)", "O Claude orienta; publicar e pausar é sempre do dono."),
    ("seg 23/11 20:30", "Claude", "BF/Natal 5: checagem de parada (A) ou publicar a página 752 (B)", "Parar se saída < 3% ou custo por clique de saída > R$ 3."),
    ("qui 19/11 20:30", "Claude", "Agendar o Reels de 18/12 (Nixzen)", "21/12 e 23/12 na rotina de segunda quando a janela abrir."),
    ("quando puder (celular)", "Dono", "Colar o texto novo da bio do Instagram e avisar \"feito\"", "O Instagram no computador recusa salvar; o Claude confere pelo Chrome depois."),
    ("quando puder", "Dono", "\"De acordo\" para corrigir as legendas dos Reels e arquivar os posts repetidos de 11, 13, 16 e 18/11", "Legendas prometem resposta no Direct que não existe."),
    ("quando puder", "Dono", "Validar link e produto dos itens 67 (Suporte de TV) e 181 (Fone Soundcore P30i)", ""),
    ("a decidir", "Dono", "Frase \"dieta e alimentação leve\" na legenda da Air Fryer (11/11) e foto da LG (26/11), que traz \"melhor\" na imagem do fabricante", "Se o dono pedir, o Claude refaz só esse dia."),
    ("sempre que aparecer item em \"Precisam de substituto\"", "Dono + Claude", "Substituir anúncios fora do ar (manual, com o dono logado no ML Afiliados)", "O Claude mostra os substitutos para aprovação e troca no guia."),
]

OBSERVACOES = [
    "As tarefas agendadas só rodam com o PC ligado e sem suspender e o app Claude aberto; as da noite precisam também do Chrome com a extensão e da Meta e do Instagram (@compre.no.link) logados.",
    "Tudo que mexe no blog passa pelo gerenciador com backup antes; nada é alterado na conta de anúncios Meta (criar, publicar, pausar e verba são do dono).",
]

# DESTAQUE do topo: o que o dono deve fazer amanhã de manhã para o anúncio (pedido do dono em 19/11/2026)
DESTAQUE_TITULO = "ANÚNCIO BLACK FRIDAY: O QUE VOCÊ DEVE FAZER AMANHÃ DE MANHÃ (sex 20/11, prazo 18:00)"
DESTAQUE = [
    ("1", "Conferir no painel do ML Afiliados a comissão dos 4 itens NOVOS da página de entrada, já trocados por moda e calçados: Tênis Olympikus Veloz 3, Kit 2 Bermudas Femininas, Kit 3 Leggings e Kit 5 Conjuntos Infantil Menino", "até 18:00", "Nas vendas passadas, esses tipos pagaram 17% a 21% (eletrônicos nunca venderam, taxa desconhecida). Item de comissão baixa: dizer qual trocar"),
    ("2", "Responder ao Claude: \"feito comissão\" (ou o item a trocar). O limite da Meta já foi ajustado", "até 18:00", "É isso que libera o plano A na tarefa das 20:00"),
    ("3", "À noite, depois das 20:00: criar e publicar o anúncio na Meta com o material que o Claude entrega (Vendas + SaidaML, R$ 90 total, término 27/11)", "sex 20/11 noite", "Claude publica a página 752 às 20:00 e orienta o passo a passo"),
]

# PLANO DO ANÚNCIO A e B em ordem cronológica (pedido do dono em 19/11/2026). Plano A = R$ 90 de 20 a 27/11; plano B = R$ 50 de 24 a 27/11
PLANO_ANUNCIO_TITULO = "PLANO DO ANÚNCIO (A = R$ 90 de 20 a 27/11  |  B = R$ 50 de 24 a 27/11  |  NATAL = R$ 150 de 14 a 22/12): TODAS AS ATIVIDADES EM ORDEM CRONOLÓGICA"
PLANO_ANUNCIO = [
    ("qui 19/11 01:15", "Decisão: plano A com recuo automático para o B; Natal R$ 100 condicional", "A e B", "Dono", "FEITO"),
    ("sex 20/11 09:00", "Aviso urgente: limite da Meta e comissão até 18:00", "A e B", "Claude (tarefa agendada)", "Agendado"),
    ("sex 20/11 até 18:00", "Limite de gastos da Meta subido para R$ 150 (gasto R$ 49,67; saldo R$ 100,33); forma de pagamento Visa 0442 válida", "A", "Claude, com o de acordo do dono", "FEITO 19/11"),
    ("sex 20/11 até 18:00", "Conferir a comissão dos 4 itens NOVOS da página 752 (moda e calçados) no ML Afiliados (dizer se algum sai)", "A e B", "Dono", "PENDENTE"),
    ("sex 20/11 até 18:00", "Responder ao Claude: \"feito limite\" e \"feito comissão\"", "A", "Dono", "PENDENTE"),
    ("sex 20/11 20:00", "BF/Natal 4. Plano A: reverifica os 4 links, publica a página 752, entrega o material de R$ 90 e troca a campanha no relatório. Plano B: entrega o material de R$ 50", "A ou B", "Claude (tarefa agendada)", "Agendado"),
    ("sex 20/11 após 20:00", "Criar e publicar o anúncio na Meta: Vendas + SaidaML, R$ 90 total, término 27/11 23:59", "A", "Dono (Claude orienta)", "Aguardando"),
    ("sáb 21 a sex 27/11", "Mandar a página 752 à mão para conhecidos e grupos permitidos", "A e B", "Dono", "Aguardando"),
    ("todo dia 10:06 e 10:22", "Gráficos do anúncio, Pixel (PageView e SaidaML) e conferência dos 4 links", "A (desde 21/11) e B (desde 24/11)", "Claude (tarefa agendada)", "Agendado"),
    ("seg 23/11 09:00", "Aviso. Plano A: números do anúncio no ar. Plano B: ÚLTIMO DIA, decisão até 12:00", "A ou B", "Claude (tarefa agendada)", "Agendado"),
    ("seg 23/11 até 12:00", "Liberar o limite da Meta (pelo menos R$ 50), confirmar a comissão e decidir se o anúncio sai", "B", "Dono", "Só se for B"),
    ("seg 23/11 20:30", "BF/Natal 5. Plano A: checagem de parada (pausar se saída < 3% ou custo por clique de saída > R$ 3). Plano B: publica a página 752, troca a campanha e entrega o checklist", "A ou B", "Claude (tarefa agendada)", "Agendado"),
    ("seg 23/11 noite", "Plano A: pausar se o Claude recomendar. Plano B: criar e publicar o anúncio de R$ 50 (início 24/11 00:00)", "A ou B", "Dono", "Aguardando"),
    ("ter 24/11 00:00", "Início do anúncio do plano B", "B", "Meta", "Só se for B"),
    ("qua 25/11 10:06", "Checagem de parada do plano B (mesma regra: saída < 3% ou custo por clique de saída > R$ 3); o Claude avisa e o dono pausa", "B", "Claude avisa, dono pausa", "Só se for B"),
    ("sex 27/11 23:59", "Fim do anúncio da Black Friday", "A e B", "Meta", "Aguardando"),
    ("seg 30/11 20:30", "BF/Natal 6: avaliar a Black Friday (aprova se saída ≥ 8% e custo por clique de saída < R$ 1) e recomendar o Natal", "A e B", "Claude analisa, dono decide", "Agendado"),
    ("qui 19/11 01:45", "Natal alterado pelo dono: R$ 150 de 14 a 24/12 (substitui R$ 100 de 03 a 14/12); teto sobe para R$ 290", "Natal", "Dono", "FEITO"),
    ("sex 11/12 20:30", "Natal: se aprovado, material final, links conferidos e aviso para segunda", "Natal", "Claude (tarefa agendada)", "Agendado"),
    ("seg 14/12", "Subir o limite da Meta em + R$ 150 e criar/publicar o anúncio de Natal (R$ 150, 14/12 00:00 a 22/12 23:59, ≈ R$ 16,67/dia)", "Natal", "Dono (Claude orienta)", "Só se aprovado"),
    ("14 a 22/12, 10:06 e 10:22", "Acompanhamento diário do Natal (gráficos, Pixel e links)", "Natal", "Claude (tarefa agendada)", "Só se aprovado"),
    ("qui 17/12 20:00", "Checagem de parada do Natal (pausar se saída < 3% ou custo por clique de saída > R$ 3)", "Natal", "Claude avisa, dono pausa", "Agendado"),
    ("ter 22/12 23:59", "Fim do anúncio de Natal (antecipado de 24/12 pelo prazo de entrega do ML; decisão do dono)", "Natal", "Meta", "Só se aprovado"),
    ("seg 28/12 20:30", "BF/Natal 7: fechamento (resultado, custo total, vendas e o que aprendemos; comissão do ML cai em ~60 dias). Movido de 14/12", "A, B e Natal", "Claude (tarefa agendada)", "Agendado"),
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
    nao = [a for a in ATIVIDADES if a[3] in (NE, PA)]
    dest = Table([[Paragraph(f"<b>{DESTAQUE_TITULO}</b>", ParagraphStyle("dt", parent=TXT, fontSize=12, leading=15, textColor=colors.white))]],
                 colWidths=[LARG])
    dest.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), VERMELHO), ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    st = [dest, tabela(["#", "O que fazer", "Prazo", "Por quê"], [list(d) for d in DESTAQUE], [0.04, 0.56, 0.12, 0.28], cor=VERMELHO),
          Spacer(1, 10), Table([[Paragraph(f"<b>{PLANO_ANUNCIO_TITULO}</b>", ParagraphStyle("pa", parent=TXT, fontSize=11, leading=14, textColor=colors.white))]],
                               colWidths=[LARG], style=[("BACKGROUND", (0, 0), (-1, -1), AZUL), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]),
          tabela(["Data e hora", "Atividade", "Plano", "Quem executa", "Situação"], [list(p_) for p_ in PLANO_ANUNCIO], [0.13, 0.50, 0.12, 0.15, 0.10], cor=AZUL),
          Spacer(1, 10), Table([[Paragraph(f"<b>{PREVISAO_TITULO}</b>", ParagraphStyle("pv", parent=TXT, fontSize=11, leading=14, textColor=colors.white))]],
                               colWidths=[LARG], style=[("BACKGROUND", (0, 0), (-1, -1), LARANJA), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]),
          Spacer(1, 4), Paragraph(PREVISAO_BASE, TXT), Spacer(1, 4),
          tabela(["Cenário (saída para o ML)", "Pessoas que vão ao ML", "Vendas prováveis", "Comissão estimada"], [list(p_) for p_ in PREVISAO], [0.40, 0.20, 0.20, 0.20], cor=LARANJA),
          Spacer(1, 6)] + [x for c_ in PREVISAO_CONCLUSAO for x in (Paragraph(c_, TXT), Spacer(1, 3))] + [
          Spacer(1, 10), Table([[Paragraph(f"<b>{DIVULGACAO_TITULO}</b>", ParagraphStyle("dv", parent=TXT, fontSize=11, leading=14, textColor=colors.white))]],
                               colWidths=[LARG], style=[("BACKGROUND", (0, 0), (-1, -1), VERDE), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]),
          tabela(["Efeito", "Ponto", "Explicação"], [list(d_) for d_ in DIVULGACAO], [0.16, 0.22, 0.62], cor=VERDE),
          Spacer(1, 6), Paragraph(DIVULGACAO_CONCLUSAO, TXT),
          Spacer(1, 10), Table([[Paragraph(f"<b>{REFLEXO_TITULO}</b>", ParagraphStyle("rf", parent=TXT, fontSize=11, leading=14, textColor=colors.white))]],
                               colWidths=[LARG], style=[("BACKGROUND", (0, 0), (-1, -1), ESCURO), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]),
          tabela(["Quando", "O que deve acontecer"], [list(r_) for r_ in REFLEXO], [0.18, 0.82], cor=ESCURO),
          Spacer(1, 6), Paragraph("<b>O que tudo isso vai refletir, no fundo:</b>", TXT), Spacer(1, 3)] + [x for r_ in REFLEXO_FUNDO for x in (Paragraph(r_, TXT), Spacer(1, 3))] + [
          Spacer(1, 10), Table([[Paragraph(f"<b>{NATAL_TITULO}</b>", ParagraphStyle("nt", parent=TXT, fontSize=11, leading=14, textColor=colors.white))]],
                               colWidths=[LARG], style=[("BACKGROUND", (0, 0), (-1, -1), VERMELHO), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]),
          tabela(["Ponto", "Análise"], [list(n_) for n_ in NATAL_ANALISE], [0.18, 0.82], cor=VERMELHO),
          Spacer(1, 6), Paragraph(NATAL_DONO, TXT),
          Spacer(1, 10), Table([[Paragraph(f"<b>{FINAL_TITULO}</b>", ParagraphStyle("fn", parent=TXT, fontSize=11, leading=14, textColor=colors.white))]],
                               colWidths=[LARG], style=[("BACKGROUND", (0, 0), (-1, -1), VERDE), ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]),
          tabela(["Etapa", "Período", "Verba", "Condição"], [list(x_) for x_ in FINAL_PLANO], [0.25, 0.15, 0.12, 0.48], cor=VERDE),
          Spacer(1, 6)] + [x for a_ in FINAL_ANALISE for x in (Paragraph(a_, TXT), Spacer(1, 3))] + [
          PageBreak(), painel(), Spacer(1, 8),
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
                     "o que não foi, o motivo e a nova data. Gerador: D:\\Projeto_Blog_Comprenolink\\Programas_Diversos_Py\\gerar_relatorio_atividade.py.", TXT)]
    doc.build(st, onFirstPage=cab_rod, onLaterPages=cab_rod)
    print("PDF:", SAIDA)
    # REGRA DO DONO (19/11/2026): na pasta fica só a versão mais nova; as anteriores vão para old_bkp (nada é apagado)
    pasta = os.path.dirname(SAIDA)
    bkp = os.path.join(pasta, "old_bkp")
    os.makedirs(bkp, exist_ok=True)
    for nome in os.listdir(pasta):
        if nome.startswith("RELATORIO_ATIVIDADE_CLAUDE_BLOG_") and nome.endswith(".pdf") and nome != os.path.basename(SAIDA):
            destino = os.path.join(bkp, nome)
            if not os.path.exists(destino):
                try:
                    os.replace(os.path.join(pasta, nome), destino)
                    print("movido para old_bkp:", nome)
                except PermissionError:
                    print("AVISO: não consegui mover (arquivo aberto em outro programa; feche e rode de novo):", nome)


if __name__ == "__main__":
    main()
