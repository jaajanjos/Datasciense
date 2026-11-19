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
    ('29/10',
     '19:03 e 19:16 a 19:20',
     'Tentei agendar com mais de 29 dias à frente pelo Meta Business Suite (para dezembro não esperar 1 mês)',
     NE,
     'Você entrou no Business Suite com o Instagram do blog (sem Facebook). Abri Criar postagem > Agendar e testei o calendário: 28/11 em diante aparece bloqueado, igual ao site do Instagram. Cancelei sem publicar nada.',
     'O limite de 29 dias é do próprio Instagram; o Business Suite não ajuda para contas só de Instagram.',
     'Não há atalho: dezembro abre dia a dia (tabela 4). O Claude agenda a cada dia, sem esperar mais que o necessário.'),
    ('29/10',
     '19:12 a 19:16',
     'Instagram: agendar post (19:00) e Reels (19:05) de 27/11 – Power Bank Anker',
     NE,
     'Cancelei o cron das 19:13 para fazer na hora. Subi feed.png, escrevi a legenda, escolhi 27/11. O Instagram aceitou 18:00 e recusou 18:30, 18:59 e 19:00 ("escolha uma data dentro dos próximos 29 dias"). Descartei o rascunho sem agendar.',
     'A janela real do Instagram fica cerca de 1 hora atrás do relógio: o horário 19:00 de 27/11 só abre perto das 20:00 de hoje (o cálculo anterior, 19:00, estava errado).',
     'Refeito com sucesso às 20:09 a 20:13 (linhas abaixo).'),
    ('29/10',
     '20:04',
     'Instagram: conferi o post de boas-vindas restaurado pelo dono',
     PA,
     'Post voltou com o mesmo endereço (instagram.com/p/DfAUWWGsITn), então a automação BLACK continua ligada a ele. NÃO está fixado: o site não tem a opção Fixar. Comentário "Black" feito pela própria compre.no.link não dispara a automação.',
     'Fixar e testar dependem do celular e de uma segunda conta do dono.',
     'HOJE: dono fixa pelo app (⋯ > Fixar no perfil) e comenta BLACK pela conta pessoal; Claude confere a resposta pública no post.'),
    ('30/10',
     '20:47',
     'ATENÇÃO: a arte e o vídeo de 28/11 trazem textos que a política do blog evita ("MELHOR CUSTO-BENEFÍCIO" no selo e, no Reels, "Um dos mais vendidos e bem avaliados do Mercado Livre")',
     PA,
     'Agendei mesmo assim porque a rotina foi aprovada pelo dono com estas artes e a publicação só ocorre em 28/11, quase um mês à frente; dá tempo de trocar. Não alterei nenhuma arte sem o OK do dono. Se o dono aprovar, regeno feed.png e reels.mp4 sem esses termos e substituo o agendamento de 28/11 (e de 25/11 e 26/11, que já tinham "Melhor").',
     'Aguardando OK do dono',
     'assim que o dono responder'),
    ('31/10',
     '16:56',
     'O gerador deste relatório voltou a uma versão antiga (sem as minhas anotações das 16:31) e o PDF das 00h57 reapareceu na pasta',
     PA,
     'Não sei a causa (possível sincronização com o outro PC). Refiz as anotações. CSV, painel de 16:37 e pacotes novos estavam intactos. Vale o dono conferir se há sincronização automática entre os dois PCs sobrescrevendo Programas_Diversos_Py.',
     'Dono confere a sincronização',
     'assim que puder'),
    ('01/11',
     '11:12',
     'Descobri que a numeração dos itens do blog mudou depois de 31/10 às 16:41 (retirados o item 39 e o 214 antigo; 3 itens novos no fim)',
     PA,
     'Os produtos depois do item 39 subiram uma posição, então os links com #item-N apontavam para o produto vizinho. Não identifiquei quem fez a mudança. Os itens novos 212, 213 e 214 entraram com texto padrão ("Olha o que eu encontrei!", "Uso diário").',
     'Texto dos itens 212 a 214',
     'quando o dono autorizar'),
    ('01/11',
     '11:15',
     'Marcar "Cadastrado = S" na planilha CATALOGO_CATEGORIAS.xlsx',
     PA,
     'Não consegui gravar: o arquivo está aberto no Excel. As 9 categorias já existem no WhatsApp (confirmado pelo dono).',
     'Excel aberto',
     'assim que o dono fechar o Excel e avisar'),
    ('01/11',
     '11:55',
     'Trocar os 10 links no catálogo do WhatsApp Business e apagar o CNL-111',
     PA,
     'SUPERADO: depois, o dono entrou no WhatsApp Web do Chrome do Claude e autorizou; os 16 links foram trocados pelo Claude (ver a entrada de 01/11 12:00). Resta apagar o CNL-111, que o Claude não apaga por ser irreversível.',
     'Apagar o CNL-111',
     'quando o dono puder'),
    ('02/11',
     '21:05 a 21:21',
     'Instagram Story com link agendado no Business Suite: 04/11, 06/11 e 09/11 às 19:10',
     PA,
     'Descobri como agendar o Story com adesivo de link e posicionar o adesivo por script. Faltam 13 (11/11 a 30/11), cerca de 5 min cada; abri uma sessão própria (card "Agendar 13 Stories").',
     'Cada Story leva vários passos no navegador',
     'Sessão própria, assim que o dono iniciar o card'),
    ('02/11',
     '22:05',
     'Instagram: trocar post 19:00 e Reels 19:05 de 13/11, 18/11 e 23/11 (fotos erradas) e agendar os 3 Stories',
     PA,
     'Pedido enviado à sessão dos Stories, que tem o contexto do Chrome: criar os novos, conferir e excluir os antigos errados.',
     'Aguardando a sessão terminar',
     'Hoje, assim que a sessão terminar'),
    ('04/11',
     '19:17',
     'WhatsApp Canal: não publicado',
     NE,
     'O pacote de 04/11 não tem bloco 19:20 Canal.',
     'Sem bloco 19:20 no pacote',
     'Nenhuma'),
    ('04/11',
     'noite',
     'Segundo administrador no Canal (sócio) e página comprenolink.net/canal; alinhar o 2º chip Claro pré-pago (aparelho dual SIM)',
     NE,
     'Combinado com o dono para o dia seguinte.',
     'Depende do dono (administrador) e da compra do chip.',
     'qui 05/11'),
    ('04/11',
     '20:39',
     'Rotina diária de agendamento no Instagram (dia 02/12, cuja janela abriu em 03/11 às ~20:00)',
     NE,
     'Não executei: o Chrome conectado ao Claude está com o Instagram DESLOGADO (abriu a tela de login em instagram.com/scheduled_content). Não digito senha nem faço login pelo dono, e não pude conferir no calendário se 02/12 já tinha sido agendado em 03/11. Também não há dia novo hoje além de 02/12 (a janela de 04/12 só abre em 05/11, ~20:00).',
     'Instagram deslogado no Chrome do Claude',
     'assim que o dono entrar no Instagram (@compre.no.link) neste Chrome e escrever "agendar 02/12"; 04/12 segue em 05/11 ~20:39'),
    ('05/11',
     '10:10',
     'Item 39 do relatório (Kit 3 Formas Antiaderentes): NÃO trocado',
     NE,
     'O item 39 do blog hoje é a Câmera Lâmpada Wi-Fi (ativa); o Kit 3 Formas não existe mais no guia: resíduo do histórico do painel.',
     'Trocar sobrescreveria um item ativo',
     'seg 09/11 (conferir se o painel ainda lista o 39)'),
    ('06/11',
     '19:17',
     'WhatsApp Canal 19:20',
     NE,
     'Não publicado.',
     'O pacote de hoje não tem o bloco 19:20 (regra: só publica no Canal se houver).',
     ''),
    ('09/11',
     '08:06',
     'Criada a rotina de atualização automática dos anúncios (Relatorios_Diarios_Anuncios\\atualiza_automatica_py_anuncios)',
     PA,
     'Menu 0_MENU_ATUALIZA_ANUNCIOS.bat + 0_executar_tudo.py com 5 etapas: verificar no ML + relatório HTML, lista de substitutos, substituição com o Claude (Chrome logado, sem aprovação prévia: o dono valida depois), troca no blog com backup e validação dos links, painel PDF + planilha + resumo. Documentação DOCUMENTACAO_ATUALIZA_ANUNCIOS_09_11_2026.pdf (como executar, riscos e atenção). Testes: simulação completa OK (4 anúncios fora do ar hoje: itens 51, 182, 191, 196), validação da IA OK, troca no blog em pré-visualização OK (nada publicado).',
     'Primeira execução real pendente: o login do Claude Code de terminal está expirado (fazer /login) e o Chrome precisa estar logado no ML Afiliados.',
     '09/11'),
    ('09/11',
     '08:25',
     '1ª execução real da substituição automática CANCELADA pelo dono (consumo alto do plano)',
     NE,
     'Login do Claude Code feito pelo dono (Pro) e Chrome conectado. Etapa 1 concluída (verificação dos 213 anúncios + relatório às 08:22); cancelado durante a etapa 3, antes de qualquer troca: nada publicado no blog, nenhum arquivo de substituição gerado.',
     'Decisão do dono: substituir manualmente. A rotina fica disponível; a opção 3 (relatório + painel, sem Claude) não consome o plano.',
     ''),
    ('13/11',
     '13:40 a 14:02',
     'NÃO feito e ocorrência',
     PA,
     'O dono informou que no WhatsApp só se trabalha com categorias, então não corrigi os 16 links dos produtos do catálogo (8 com número desatualizado; o Smartwatch saiu do blog). Nada foi apagado. Por engano criei D:\\mercado_livre\\0- Pendencias\\99_Programas_PY neste PC (essa raiz antiga não existe aqui); movi o script e apaguei essas pastas, que só tinham o meu arquivo. Depois os arquivos que eu havia criado (PDF, relatório de 13h50 e script) não estavam mais no projeto e foram refeitos.',
     'Decisões do dono',
     'descrições de Contato/Sobre/Privacidade e H1 repetido; apagar os 16 itens de produto do catálogo do WhatsApp; sincronizar a cópia Celular_Whatsapp de 09/12, 11/12 e 14/12 (desatualizada)'),
    ('16/11',
     '20:06 a 20:17',
     'Leitura final do anúncio Meta não concluída (tabela travada) e reagendamentos para 17/11',
     NE,
     "Abri o Gerenciador de Anúncios 4 vezes (período Máximo e este mês; recarreguei a página; esperei até 60 s): o conjunto aparece Ativo, mas gasto, saldo e resultados ficaram em 'Carregando...'. Não gerei PDF nem gráfico para não usar números antigos. Último saldo confirmado: 15/11 20h43, gasto R$ 36,45 e saldo R$ 13,55. Nada alterado na conta de anúncios. A pedido do dono: leitura final reagendada para terça 17/11 às 14:00 e avaliação completa para terça 17/11 às 15:00; rotina noturna ea451579 removida. Dono cancelou a atividade 'decidir a conversa dos prints e a data do guia' (anotação salva).",
     'Lentidão da própria Meta no momento da leitura. Se travar de novo, peço print ao dono.',
     'Terça 17/11 14:00 (leitura final, PDF e gráfico) e 15:00 (avaliação: semáforo, meta 150 visitas e até R$ 0,35, manter R$ 50 ou subir para R$ 100; aumento só com de acordo)'),
    ('17/11',
     '10:00',
     'Gráficos diários do anúncio Meta: sem coleta hoje',
     NE,
     'Abri o Gerenciador de Anúncios (visualização salva) e a tabela demorou a carregar; ao tentar ler os números o Chrome fechou e a extensão ficou sem navegador conectado. Não gerei PDF nem alterei CSVs para não usar números antigos. Campanha teste_11a13_11 aparece como Concluído (encerrada em 16/11); última leitura: 16/11 20h46, gasto R$ 48,32 de R$ 50 (saldo R$ 1,68), 184 resultados. Nada alterado na conta de anúncios.',
     'Chrome precisa estar aberto com a extensão Claude conectada. Como o anúncio terminou em 16/11, a rotina diária já cumpriu seu papel; a leitura final de 16/11 vale como fechamento.',
     'Dono decide se mantém a rotina diária ou a encerra; subir verba só com de acordo'),
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
]

FALTA_AGENDAR = [
    ("18/12", "Máquina de Cortar Cabelo e Barba Sem Fio Nixzen"), ("21/12", "Jogo de Lençol Casal Percal 600 Fios 4 Peças"),
    ("23/12", "Cortina de LED 3x3 m com 300 Luzes e Controle"),
]

# (quando, quem, o que, ganho / observação) – sempre a data mais cedo possível
REEXECUCAO = [
    ("qui 05/11 ~20:39", "Claude", "Agendar 04/12 (post 19:00 e Reels 19:05) pela rotina diária: a janela só abre por volta das 20:00 de 05/11", "Precisa: app Claude aberto, Chrome (o conectado ao Claude, \"Browser 1\") logado no Instagram compre.no.link e PC ligado e sem suspender. 02/12 foi agendado em 04/11 depois do login do dono."),
    ("ter 03/11", "Dono ou Claude", "WhatsApp: conferir se as 7 categorias saíram de \"em análise\" (aprovadas e visíveis no catálogo para os clientes)", "Cadastro feito e validado em 02/11. Se alguma for recusada, o WhatsApp mostra o motivo no item; o Claude ajusta o texto ou a foto."),
    ("seg 09/11, 10:00", "Dono + Claude", "Primeira rodada semanal completa (blog, prints de vendas, CSV, painel, catálogo e links)", "Calendário: Calendario_Execucao_Semanal_WhatsApp_Vendas.ics (importar no Google Agenda ou Outlook)."),
    ("31/10 em diante", "Claude", "Agendar dezembro, um dia por vez (04/12 em 05/11, 07/12 em 08/11 e assim por diante)", "A rotina diária expira por volta de 05/11 (7 dias): o Claude recria. Se o PC ou o app forem fechados antes, o dono escreve \"agendar DD/MM\"."),
    ("a decidir", "Dono", "Frase \"dieta e alimentação leve\" na legenda da Air Fryer (11/11) e foto da LG (26/11), que traz \"melhor\" na imagem do fabricante", "Alegações leves que ainda não foram trocadas. Se o dono pedir, o Claude refaz só esse dia."),
    ("dias de post (04/11, 06/11, 09/11...)", "Claude", "Story com link 19:10, Status 19:15 e Canal 19:20 (conforme o pacote do dia)", "Story: Meta Business Suite (pode ser agendado com antecedência). Status e Canal: WhatsApp Web, que precisa estar conectado."),
    ("sempre que aparecer item em \"Precisam de substituto\"", "Dono + Claude", "Substituir anúncios fora do ar: o dono deixa o Chrome com a extensão conectada e logado no ML Afiliados e pede \"substitua os anúncios fora do ar\"", "O Claude mostra os substitutos para aprovação, gera o meli.la, troca no guia e atualiza o relatório e o painel."),
    ("qui 05/11, 10:00", "Dono + sócio", "Reunião Turbinar e os 17 anúncios (os 17 já foram retirados em 30/10; falta só decidir o Turbinar e os termos do ML Afiliados)", "Levar o Plano Turbinar e o resultado da leitura dos termos."),
]

OBSERVACOES = [
    "Quando o dono sai do computador, o agendamento de 28/11 às 20:39 depende de 3 coisas ligadas: o app Claude, o Chrome (com a extensão do Claude e o Instagram compre.no.link logado) e o PC sem suspender. O cron é de sessão e só dispara com o app aberto.",
    "Em 29/10 abri uma vez a conversa do Direct da conta pessoal do dono para conferir o teste, o que marcou as mensagens como vistas; avisei na hora e não repeti.",
    "A rede do PC falhou por poucos segundos às 18:4x (erro de DNS ao chamar o blog) e voltou sozinha; nenhuma alteração foi perdida.",
    "Os agendamentos dependem do aplicativo Claude, do Chrome com a extensão e do Instagram logado ficarem abertos. O cron é de sessão: se o aplicativo for fechado, ele se perde "
    "e o dono escreve \"agendar DD/MM\".",
    "Tudo que mexe no blog passa pelo gerenciador com backup antes (pasta backups). Nada foi apagado do blog nesta sessão.",
    "Horários \"não registrado\" ou \"manhã/tarde\" vêm do resumo das sessões anteriores. Histórico completo: "
    r"C:\Users\SVR_RYZEN_JAA\.claude\projects\C--Users-SVR-RYZEN-JAA\d759a442-1d58-4e20-94e0-f2e7cc22f60c.jsonl.",
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
