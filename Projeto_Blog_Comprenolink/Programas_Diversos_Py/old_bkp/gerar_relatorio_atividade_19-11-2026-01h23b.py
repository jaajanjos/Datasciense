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
    ('29/10', '19:03 e 19:16 a 19:20', 'Tentei agendar com mais de 29 dias à frente pelo Meta Business Suite (para dezembro não esperar 1 mês)', 'NÃO EXECUTADO', 'Você entrou no Business Suite com o Instagram do blog (sem Facebook). Abri Criar postagem > Agendar e testei o calendário: 28/11 em diante aparece bloqueado, igual ao site do Instagram. Cancelei sem publicar nada.', 'O limite de 29 dias é do próprio Instagram; o Business Suite não ajuda para contas só de Instagram.', 'Não há atalho: dezembro abre dia a dia (tabela 4). O Claude agenda a cada dia, sem esperar mais que o necessário.'),
    ('29/10', '19:12 a 19:16', 'Instagram: agendar post (19:00) e Reels (19:05) de 27/11 – Power Bank Anker', 'NÃO EXECUTADO', 'Cancelei o cron das 19:13 para fazer na hora. Subi feed.png, escrevi a legenda, escolhi 27/11. O Instagram aceitou 18:00 e recusou 18:30, 18:59 e 19:00 ("escolha uma data dentro dos próximos 29 dias"). Descartei o rascunho sem agendar.', 'A janela real do Instagram fica cerca de 1 hora atrás do relógio: o horário 19:00 de 27/11 só abre perto das 20:00 de hoje (o cálculo anterior, 19:00, estava errado).', 'Refeito com sucesso às 20:09 a 20:13 (linhas abaixo).'),
    ('29/10', '20:04', 'Instagram: conferi o post de boas-vindas restaurado pelo dono', 'PARCIAL', 'Post voltou com o mesmo endereço (instagram.com/p/DfAUWWGsITn), então a automação BLACK continua ligada a ele. NÃO está fixado: o site não tem a opção Fixar. Comentário "Black" feito pela própria compre.no.link não dispara a automação.', 'Fixar e testar dependem do celular e de uma segunda conta do dono.', 'HOJE: dono fixa pelo app (⋯ > Fixar no perfil) e comenta BLACK pela conta pessoal; Claude confere a resposta pública no post.'),
    ('30/10', '20:47', 'ATENÇÃO: a arte e o vídeo de 28/11 trazem textos que a política do blog evita ("MELHOR CUSTO-BENEFÍCIO" no selo e, no Reels, "Um dos mais vendidos e bem avaliados do Mercado Livre")', 'PARCIAL', 'Agendei mesmo assim porque a rotina foi aprovada pelo dono com estas artes e a publicação só ocorre em 28/11, quase um mês à frente; dá tempo de trocar. Não alterei nenhuma arte sem o OK do dono. Se o dono aprovar, regeno feed.png e reels.mp4 sem esses termos e substituo o agendamento de 28/11 (e de 25/11 e 26/11, que já tinham "Melhor").', 'Aguardando OK do dono', 'assim que o dono responder'),
    ('31/10', '16:56', 'O gerador deste relatório voltou a uma versão antiga (sem as minhas anotações das 16:31) e o PDF das 00h57 reapareceu na pasta', 'PARCIAL', 'Não sei a causa (possível sincronização com o outro PC). Refiz as anotações. CSV, painel de 16:37 e pacotes novos estavam intactos. Vale o dono conferir se há sincronização automática entre os dois PCs sobrescrevendo Programas_Diversos_Py.', 'Dono confere a sincronização', 'assim que puder'),
    ('01/11', '11:15', 'Marcar "Cadastrado = S" na planilha CATALOGO_CATEGORIAS.xlsx', 'PARCIAL', 'Não consegui gravar: o arquivo está aberto no Excel. As 9 categorias já existem no WhatsApp (confirmado pelo dono).', 'Excel aberto', 'assim que o dono fechar o Excel e avisar'),
    ('02/11', '21:05 a 21:21', 'Instagram Story com link agendado no Business Suite: 04/11, 06/11 e 09/11 às 19:10', 'PARCIAL', 'Descobri como agendar o Story com adesivo de link e posicionar o adesivo por script. Faltam 13 (11/11 a 30/11), cerca de 5 min cada; abri uma sessão própria (card "Agendar 13 Stories").', 'Cada Story leva vários passos no navegador', 'Sessão própria, assim que o dono iniciar o card'),
    ('02/11', '22:05', 'Instagram: trocar post 19:00 e Reels 19:05 de 13/11, 18/11 e 23/11 (fotos erradas) e agendar os 3 Stories', 'PARCIAL', 'Pedido enviado à sessão dos Stories, que tem o contexto do Chrome: criar os novos, conferir e excluir os antigos errados.', 'Aguardando a sessão terminar', 'Hoje, assim que a sessão terminar'),
    ('04/11', '19:17', 'WhatsApp Canal: não publicado', 'NÃO EXECUTADO', 'O pacote de 04/11 não tem bloco 19:20 Canal.', 'Sem bloco 19:20 no pacote', 'Nenhuma'),
    ('04/11', '20:39', 'Rotina diária de agendamento no Instagram (dia 02/12, cuja janela abriu em 03/11 às ~20:00)', 'NÃO EXECUTADO', 'Não executei: o Chrome conectado ao Claude está com o Instagram DESLOGADO (abriu a tela de login em instagram.com/scheduled_content). Não digito senha nem faço login pelo dono, e não pude conferir no calendário se 02/12 já tinha sido agendado em 03/11. Também não há dia novo hoje além de 02/12 (a janela de 04/12 só abre em 05/11, ~20:00).', 'Instagram deslogado no Chrome do Claude', 'assim que o dono entrar no Instagram (@compre.no.link) neste Chrome e escrever "agendar 02/12"; 04/12 segue em 05/11 ~20:39'),
    ('04/11', 'noite', 'Segundo administrador no Canal (sócio) e página comprenolink.net/canal; alinhar o 2º chip Claro pré-pago (aparelho dual SIM)', 'NÃO EXECUTADO', 'Combinado com o dono para o dia seguinte.', 'Depende do dono (administrador) e da compra do chip.', 'qui 05/11'),
    ('05/11', '10:10', 'Item 39 do relatório (Kit 3 Formas Antiaderentes): NÃO trocado', 'NÃO EXECUTADO', 'O item 39 do blog hoje é a Câmera Lâmpada Wi-Fi (ativa); o Kit 3 Formas não existe mais no guia: resíduo do histórico do painel.', 'Trocar sobrescreveria um item ativo', 'seg 09/11 (conferir se o painel ainda lista o 39)'),
    ('06/11', '19:17', 'WhatsApp Canal 19:20', 'NÃO EXECUTADO', 'Não publicado.', 'O pacote de hoje não tem o bloco 19:20 (regra: só publica no Canal se houver).', ''),
    ('09/11', '08:06', 'Criada a rotina de atualização automática dos anúncios (Relatorios_Diarios_Anuncios\\atualiza_automatica_py_anuncios)', 'PARCIAL', 'Menu 0_MENU_ATUALIZA_ANUNCIOS.bat + 0_executar_tudo.py com 5 etapas: verificar no ML + relatório HTML, lista de substitutos, substituição com o Claude (Chrome logado, sem aprovação prévia: o dono valida depois), troca no blog com backup e validação dos links, painel PDF + planilha + resumo. Documentação DOCUMENTACAO_ATUALIZA_ANUNCIOS_09_11_2026.pdf (como executar, riscos e atenção). Testes: simulação completa OK (4 anúncios fora do ar hoje: itens 51, 182, 191, 196), validação da IA OK, troca no blog em pré-visualização OK (nada publicado).', 'Primeira execução real pendente: o login do Claude Code de terminal está expirado (fazer /login) e o Chrome precisa estar logado no ML Afiliados.', '09/11'),
    ('09/11', '08:25', '1ª execução real da substituição automática CANCELADA pelo dono (consumo alto do plano)', 'NÃO EXECUTADO', 'Login do Claude Code feito pelo dono (Pro) e Chrome conectado. Etapa 1 concluída (verificação dos 213 anúncios + relatório às 08:22); cancelado durante a etapa 3, antes de qualquer troca: nada publicado no blog, nenhum arquivo de substituição gerado.', 'Decisão do dono: substituir manualmente. A rotina fica disponível; a opção 3 (relatório + painel, sem Claude) não consome o plano.', ''),
    ('19/11', '00:59', 'Conferência das tarefas agendadas (conversa nova: BLOG - Execução de atividades e planejamento)', 'EXECUTADO', 'Esta conversa assumiu tudo da "Atividades Claude e Planejamento" (passagem registrada nas anotações). Conferi as tarefas agendadas: as 3 da noite de 18/11 (BF/Natal 2, Pixel, Melhorias M0) terminaram com sucesso; as 5 de hoje (10:06, 10:22, 12:23, 20:00 e 20:30) estão ativas. Nenhuma tarefa cita a conversa antiga.', '', ''),
    ('19/11', '01:15', 'Anúncio Black Friday: decisão do dono ("DE ACORDO") aplicada às tarefas', 'EXECUTADO', 'Plano A: R$ 90 de 20 a 27/11 (≈ R$ 11,25/dia), se até sex 20/11 18:00 o limite da Meta (≥ R$ 90) e a comissão dos 5 itens estiverem resolvidos; senão plano B: R$ 50 de 24 a 27/11. Natal R$ 100 mantido e condicional. Criado 1_Pendencias/DECISAO_ANUNCIO_BF_2026.md e ajustadas 4 tarefas (aviso 20/11 09:00, BF/Natal 4, aviso 23/11 09:00, BF/Natal 5), com cópia em old_bkp. Nada alterado na Meta nem no site.', '', 'Dono: limite da Meta e comissão até sex 20/11 18:00'),
    ('19/11', '01:18', 'Relatório de atividades: 1ª geração do dia', 'EXECUTADO', 'Regra permanente aplicada: saíram os 8 sucessos de 18/11; ficaram as 15 pendências; plano de reexecução refeito só com ações em aberto; dias sem agendar = 18/12, 21/12 e 23/12.', '', ''),
]

FALTA_AGENDAR = [
    ("18/12", "Máquina de Cortar Cabelo e Barba Sem Fio Nixzen (tarefa hoje 19/11 20:30)"), ("21/12", "Jogo de Lençol Casal Percal 600 Fios 4 Peças"),
    ("23/12", "Cortina de LED 3x3 m com 300 Luzes e Controle"),
]

# (quando, quem, o que, ganho / observação) – sempre a data mais cedo possível
REEXECUCAO = [
    ("sex 20/11 até 18:00", "Dono", "Liberar o limite de gastos da conta Meta (≥ R$ 90) e conferir a comissão dos 5 itens da página 752 no ML", "Sem isso o plano A (R$ 90, 20 a 27/11) não sai e vale o plano B (R$ 50, 24 a 27/11). Responder \"feito\" para registrar."),
    ("sex 20/11 20:00", "Claude", "BF/Natal 4: plano A publica a página 752 e entrega o material; plano B prepara o anúncio de R$ 50", "Tarefa agendada; lê DECISAO_ANUNCIO_BF_2026.md."),
    ("sex 20/11 após 20:00 (A) ou seg 23/11 até 12:00 (B)", "Dono", "Criar e publicar o anúncio na Meta (Vendas + SaidaML)", "O Claude orienta; publicar e pausar é sempre do dono."),
    ("seg 23/11 20:30", "Claude", "BF/Natal 5: checagem de parada (A) ou publicar a página 752 (B)", "Parar se saída < 3% ou custo por clique de saída > R$ 3."),
    ("qui 19/11 20:30", "Claude", "Agendar o Reels de 18/12 (Nixzen)", "21/12 e 23/12 na rotina de segunda quando a janela abrir."),
    ("quando puder (celular)", "Dono", "Colar o texto novo da bio do Instagram e avisar \"feito\"", "O Instagram no computador recusa salvar; o Claude confere pelo Chrome depois."),
    ("quando puder", "Dono", "\"De acordo\" para corrigir as legendas dos Reels e arquivar os posts repetidos de 11, 13, 16 e 18/11", "Legendas prometem resposta no Direct que não existe."),
    ("quando puder", "Dono", "Validar link e produto dos itens 67 (Suporte de TV) e 181 (Fone Soundcore P30i)", ""),
    ("quando puder", "Dono", "\"De acordo\" para refazer 4_PACOTE_OUTRO_PC.zip, 4_ATUALIZAR_OUTRO_PC.zip e CentralBlog.exe; responder se roda \"gerar as categorias\" (itens 14, 35, 47)", "3 avisos do validador."),
    ("a decidir", "Dono", "Frase \"dieta e alimentação leve\" na legenda da Air Fryer (11/11) e foto da LG (26/11), que traz \"melhor\" na imagem do fabricante", "Se o dono pedir, o Claude refaz só esse dia."),
    ("sempre que aparecer item em \"Precisam de substituto\"", "Dono + Claude", "Substituir anúncios fora do ar (manual, com o dono logado no ML Afiliados)", "O Claude mostra os substitutos para aprovação e troca no guia."),
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

# DESTAQUE do topo: o que o dono deve fazer amanhã de manhã para o anúncio (pedido do dono em 19/11/2026)
DESTAQUE_TITULO = "ANÚNCIO BLACK FRIDAY: O QUE VOCÊ DEVE FAZER AMANHÃ DE MANHÃ (sex 20/11, prazo 18:00)"
DESTAQUE = [
    ("1", "Liberar o limite de gastos da conta Meta (Compre no Link - Anúncios): pelo menos R$ 90 e forma de pagamento OK", "até 18:00", "Sem isso o anúncio de R$ 90 (20 a 27/11) não roda; volta ao plano B (R$ 50, 24 a 27/11)"),
    ("2", "Conferir no painel do ML Afiliados a comissão dos 5 itens da página de entrada (Smart TV LG QNED 55\", Soundbar JBL SB595, Fire TV Stick 4K, Fone QCY HT08, Kit 4 Bermudas)", "até 18:00", "Item de comissão baixa: dizer qual trocar; o Claude troca antes de publicar"),
    ("3", "Responder ao Claude: \"feito limite\" e \"feito comissão\" (ou o item a trocar)", "até 18:00", "É isso que libera o plano A na tarefa das 20:00"),
    ("4", "À noite, depois das 20:00: criar e publicar o anúncio na Meta com o material que o Claude entrega (Vendas + SaidaML, R$ 90 total, término 27/11)", "sex 20/11 noite", "Claude publica a página 752 às 20:00 e orienta o passo a passo"),
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
          Spacer(1, 10), painel(), Spacer(1, 8),
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


if __name__ == "__main__":
    main()
