# -*- coding: utf-8 -*-
"""nova_pendencias.pdf: o que ainda falta executar (dono e Claude), com passo a passo, o porquê e o benefício.
Estado em 04/11/2026 (concluídos saíram; o histórico está em 0- Pendencias\bkp_drp), depois da análise do Checklist Turbinar (passos 7, 8, 9, 19, 20, 21, 22 e 23 já concluídos).
Rodar:  python -X utf8 gerar_nova_pendencias.py
Saída:  D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/nova_pendencias.pdf
Usa os componentes visuais de gerar_pendencias_detalhado.py (mesma pasta). Caminhos com barra normal.
"""
import os
import sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gerar_pendencias_detalhado as base  # noqa: E402
from gerar_pendencias_detalhado import (AZUL, AZUL_C, LARANJA, LARANJA_C, P, VERDE, VERDE_C, VERMELHO, VERMELHO_C,  # noqa: E402
                                        bloco, faixa, info, passos, tabela)
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import KeepTogether, PageBreak, SimpleDocTemplate, Spacer  # noqa: E402

SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/nova_pendencias.pdf"
base.HOJE = date(2026, 11, 4)
GUIA = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"
BF = "https://comprenolink.net/black-friday/"


DIA_EXEC = {
    "6": "Sex 06/11 às 14:00 e seg 09/11 às 10:15 e 10:45",
    "7": "Todo dia de post às 19:10; datas-chave: 10/11, 11/11, 18 a 26/11, 27/11 e 30/11",
    "8": "Seg 09/11 (só se o item 77 continuar pausado)",
    "11": "Seg 09/11 (pedir) e ter 10/11 (revisar, 30 min); depois toda semana",
    "12": "Conta 13/11; teste 16 a 18/11", "13": "Ter 01/12 (5 min)",
    "14": "Qui 05/11 (10:20 e 10:30); convites à mão a partir de 06/11",
    "15": "Qui 05/11 (10:00) e ao longo da semana; cada item tem o seu dia"}


def atividade(num, titulo, quando, cor, cor_c, quem, tempo, por_que, beneficio, lista, detalhes=None, pronto=None, extra=None):
    """Uma atividade completa: faixa, quadro-resumo, por quê, benefício, passo a passo, detalhes e critério de pronto."""
    topo = KeepTogether([faixa(num, titulo, quando, cor), Spacer(1, 4),
                         info([("Dia de execução", DIA_EXEC.get(str(num), quando)), ("Quem faz", quem), ("Tempo estimado", tempo), ("Por que fazer", por_que), ("Benefício", beneficio)]), Spacer(1, 6),
                         P("Passo a passo", "h2")])
    out = [topo, passos(lista, cor)]
    if extra:
        out += [Spacer(1, 4)] + extra
    fim = []
    if detalhes:
        fim += [Spacer(1, 5), bloco("Detalhes e cuidados", detalhes, cor, cor_c)]
    if pronto:
        fim += [Spacer(1, 4), P(f"<b>Está pronto quando:</b> {pronto}", "p")]
    if fim:
        out += [KeepTogether(fim)]
    out += [Spacer(1, 14)]
    return out


def conteudo():
    st = [Spacer(1, 0.3 * cm), P("PENDÊNCIAS ABERTAS", "capa_t"), Spacer(1, 4),
          P("O que ainda falta executar, com passo a passo, o porquê e o benefício<br/>"
            "comprenolink.net • Instagram @compre.no.link • WhatsApp (11) 99495-9657 • posição de 04/11/2026", "capa_s"), Spacer(1, 8),
          info([("Como usar", "Cada atividade tem: quem faz, quanto tempo leva, POR QUE fazer, o BENEFÍCIO e o passo a passo. Siga a ordem da tabela abaixo: "
                              "as primeiras são as mais urgentes ou as que destravam as outras."),
                ("Foco", "WhatsApp, Instagram, Mercado Livre e ajustes do blog (TikTok descartado em 03/11)."),
                ("Cores", "Vermelho = urgente. Laranja = importante nesta semana. Azul = planejado com data. Verde = rotina que se repete."),
                ("Se travar", "Escreva ao Claude com um print da tela. Para tudo que exige senha, código de celular ou aceite de termos, o Claude para e avisa: "
                              "essa parte é sempre sua."),
                ("Controle", "ESTE É O ÚNICO ARQUIVO DE PENDÊNCIAS. Toda pendência nova entra aqui e, quando concluída, sai da lista (o histórico fica na pasta bkp_drp, em 0- Pendencias). Os números das atividades não mudam, porque a agenda aponta para eles. Nenhuma pendência fica em outro arquivo, para você não perder o controle.")]),
          Spacer(1, 8), P("Resumo em ordem de execução", "h2"),
          tabela(["#", "Atividade", "Quem", "Dia", "Tempo"],
                 [["14", "Crescimento seguro do Canal no WhatsApp: atração e convites à mão (sem automação)", "Você + Claude", "Qui 05/11 em diante", "20 min por dia"],
                  ["6", "Rotinas: SEO na sexta e números na segunda", "Você (+ Claude)", "Sex 06/11 e seg 09/11", "60 min e 45 min"],
                  ["7", "Calendário de divulgação da Black Friday (WhatsApp e Instagram)", "Você + Claude", "Todo dia, 19:10", "10 min por dia"],
                  ["8", "Anúncios: 213 de 214 ativos; 1 pausado (item 77, Colágeno Verisol)", "Você (link novo)", "Seg 09/11, se continuar", "10 min"],
                  ["11", "Uma página nova por semana (fones, TVs, presentes...)", "Claude escreve, você revisa", "Seg 09/11 e toda semana", "30 min seus"],
                  ["12", "Teste de anúncio pago no Instagram/Facebook (decidido em 05/11)", "Você + sócio pagador + Claude", "Conta Meta até 13/11; teste de 16 a 18/11", "1 h + R$ 50 de teste"],
                  ["13", "Trocar a bio do Instagram para o Natal", "Você (celular)", "Ter 01/12", "5 min"],
                  ["15", "Pendências herdadas das outras conversas (catálogo, segurança, vendas, medição, dezembro)", "Você + Claude", "Qui 05/11 em diante", "30 min na semana"]],
                 [0.05, 0.36, 0.17, 0.19, 0.23], cor=LARANJA), Spacer(1, 4),
          bloco("Foco definido em 03/11: WhatsApp, Instagram, Mercado Livre e ajustes do blog", [
              "TikTok: descartado a pedido do dono. Os 3 vídeos ficam guardados na pasta VIDEOS TIKTOK, sem uso.",
              "Telegram, YouTube/Facebook e Pinterest: fora do foco por enquanto. Só voltam se sobrar tempo depois da Black Friday (peça ao Claude).",
              "Menos canais, feitos com constância, rendem mais do que muitos canais abandonados."], AZUL, AZUL_C), Spacer(1, 8),
          Spacer(1, 6), P("Plano de execução por dia (equilibrado, sem passar o dia inteiro)", "h2"),
          tabela(["Dia", "O que fazer", "Tempo extra"],
                 [["Qui 05/11", "10:00 republicar o blog das máquinas (Google Sites), 10:20 colar o convite do Canal nas respostas (G1) e 10:30 aprovar contatos pessoais para o Canal (atividade 14). A agenda foi revisada em 04/11 (importar de novo o agenda_crescimento_canal_whatsapp.ics)", "40 min"],
                  ["Sex 06/11", "Rotina de SEO às 14:00 (atividade 6). Se pedir \"rotina de sexta\" ao Claude, ele faz a maior parte e leva uns 20 min", "20 a 60 min"],
                  ["Sáb 07/11", "Destaques do Instagram, no celular", "30 min"],
                  ["Seg 09/11", "10:15 vendas por prints (15 min), 10:30 revisão semanal do Canal: formulário e seguidores (15 min, atividade 14), 10:45 números (30 min) e decisões do dia 09/11 (15 min). Pedir a primeira página nova da semana", "75 min"],
                  ["Ter 10/11", "Catálogo do WhatsApp: Moda Infantil (15 min). Revisar a página nova (30 min)", "55 min"],
                  ["A partir de 06/11", "Rotina diária da atividade 14: 10:00 convites à mão (15 min), 19:20 responder as pessoas (5 min) e 20:30 fechar o dia (2 min)", "20 min por dia"],
                  ["Qua 11/11", "Dia do 11.11 (rotina do dia) e confirmar os testes do ManyChat (5 min)", "5 min"],
                  ["Qui 12/11", "Ver se os dois computadores sincronizam a pasta de scripts", "10 min"],
                  ["Sex 13/11", "Rotina de SEO com a conferência do guia, tudo na mesma hora", "20 a 60 min"],
                  ["16 a 20/11", "Segunda: números (45 min). Terça: revisar a página nova (30 min). Sexta: SEO. Sem nada além disso", "45 + 30 + 20 a 60"],
                  ["23 a 30/11 (Black Friday)", "Nenhuma tarefa extra. Só a rotina do dia (10 min), a rotina da atividade 14 (20 min, sem convites em 27/11), o lembrete de 26/11 às 20:00, o dia D 27/11 (08:00, 12:00 e 19:00) e a segunda 30/11. A Rotina de SEO de 27/11 passa para 30/11", "só a rotina"],
                  ["Ter 01/12", "Trocar a bio do Instagram para o Natal (celular)", "5 min"]],
                 [0.17, 0.66, 0.17], cor=VERDE), Spacer(1, 4),
          bloco("Como o equilíbrio funciona", [
              "Todo dia de post existe a rotina fixa de 10 minutos (Story 19:10, Status 19:15, Canal 19:20). Quando você não puder, o sócio direciona o Claude.",
              "Fora essa rotina, nenhum dia passa de cerca de 30 minutos. Só segunda e sexta chegam a 60, porque são as rotinas fixas dos números e do SEO.",
              "Tudo que pode ser feito pelo Claude (páginas novas, SEO, trocas no blog, textos) fica com ele; você só aprova.",
              "Se algum dia ficar pesado, avise: o Claude move a tarefa para o dia mais leve."], AZUL, AZUL_C),
          PageBreak()]

    # 6
    st += atividade("6", "Rotinas: SEO na sexta 06/11 e números na segunda 09/11", "06/11 (sexta 14:00) e 09/11 (segunda 10:15 e 10:45)", AZUL, AZUL_C,
                    "Você (o Claude ajuda se pedir: \"rotina de sexta\")", "1 hora na sexta e 30 minutos na segunda",
                    "O Google leva de 4 a 12 semanas para dar posição boa; quem cuida do site toda semana ganha. E sem olhar os números você continua fazendo o que não funciona.",
                    "Sexta: o Google passa a mostrar suas páginas para mais pesquisas. Segunda: você descobre qual canal traz cliques e dobra o que funciona, "
                    "troca o que não traz nada.",
                    [("Sexta 14:00 – Search Console", "search.google.com/search-console (conta compre.no.link26@gmail.com). Desempenho > Consultas: procure pesquisas "
                                                      "com muitas impressões e poucos cliques."),
                     ("Melhore o título e a descrição", "No WordPress, abra a página > All in One SEO e escreva algo que responda à pesquisa. Sem preço e sem \"mais vendido\"."),
                     ("Peça indexação do que for novo", "Search Console > Inspeção de URL > Solicitar indexação."),
                     ("Segunda 10:15 – vendas", "A sua conta do ML Afiliados não tem botão de exportar: tire os prints da tabela de Vendas e mande ao Claude, que atualiza o arquivo de vendas. Depois rode ATUALIZAR_PAINEL.bat. Passo a passo no Anexo A."),
                     ("Segunda 10:45 – planilha", "Preencha a linha da semana em Planilha_Semanal_Turbinar.xlsx. Veja o melhor canal na aba Campanhas do painel."),
                     ("Decida UMA coisa", "Canal que mais trouxe cliques ganha o dobro de posts; o que trouxe zero por 2 semanas é trocado.")],
                    ["Roteiro completo: Roteiro_Rotinas_Segunda_e_Sexta.pdf.",
                     "Dados do Google Analytics só aparecem a partir de 06/11 (leva até 48 horas)."],
                    "a planilha tem a linha da semana preenchida e uma decisão anotada.")

    # 7
    datas = tabela(["Data", "O que fazer", "Onde está o material"],
                   [["Todo dia de post", "19:10 Story com link, 19:15 Status do WhatsApp, 19:20 Canal (post e Reels saem sozinhos 19:00 e 19:05)",
                     "Planejamentos\\Andamento\\Divugação_WhastsApp_Instagram\\07_PACOTE_DO_DIA (pasta do dia)"],
                    ["Qua 11/11", "11.11: post, Reels, Story e Status do dia (Air Fryer Mondial)", "pasta 2026-11-11_qua"],
                    ["18/11 a 26/11", "Esquenta da Black Friday: 2 a 3 envios por dia", "pastas de cada dia"],
                    ["Qui 26/11, 20:00", "Lembrete forte: \"amanhã é Black Friday\"", "pasta 2026-11-26_qui (bloco das 20:00)"],
                    ["Sex 27/11", "Dia D: disparos às 08:00, 12:00 e 19:00 (a cada 2 a 3 horas se der)", "pasta 2026-11-27_sex"],
                    ["Seg 30/11", "Cyber Monday: último dia da campanha", "pasta 2026-11-30_seg"],
                    ["Ter 01/12", "A página de Natal assume o menu e a home sozinha (confira no celular)", "comprenolink.net"]],
                   [0.17, 0.5, 0.33], cor=AZUL)
    st += atividade("7", "Calendário de divulgação da Black Friday", "10/11 a 30/11 (a Black Friday é 27/11)", AZUL, AZUL_C, "Você publica; quando você não puder, o sócio direciona o Claude a publicar; o Claude agenda post e Reels", "10 a 20 minutos por dia",
                    "A Black Friday é a época em que mais se compra. As pessoas começam a pesquisar semanas antes; quem aparece com constância colhe o resultado.",
                    "Cada envio com link rastreável mostra, na segunda seguinte, qual dia e qual produto trouxe visitas e cliques: você repete o que deu certo.",
                    [("Se o sócio for direcionar o Claude", "O sócio escreve ao Claude, em português e com a data. Exemplos: \"agendar DD/MM\" (post e Reels no Instagram), ""\"publicar o Status e o Canal de hoje\", \"publicar o Story de hoje\" e \"texto do Direct de DD/MM\". O Claude usa a pasta do dia (07_PACOTE_DO_DIA) e os textos já revisados."),
                     ("O que precisa estar pronto para o Claude publicar", "Computador do blog ligado e sem suspender, aplicativo do Claude aberto, Chrome aberto com o Instagram @compre.no.link e o WhatsApp Web (número do blog) já logados e a extensão do Claude conectada. Se uma conta pedir senha ou código, o Claude para e avisa: aí é preciso você (ou quem tem a senha) entrar."),
                     ("Antes de começar", "Na véspera ou de manhã, leve story.png, status.png e feed.png da pasta do dia para o celular (WhatsApp Web para você mesmo é o jeito mais rápido)."),
                     ("19:10 – Story", "Instagram @compre.no.link: + > Story > story.png > adesivo Link (cole o link do arquivo 1_TEXTOS_DO_DIA.txt) > Seu story."),
                     ("19:15 – Status", "WhatsApp Business > Status > status.png > cole a legenda do bloco das 19:15 > enviar."),
                     ("19:20 – Canal (só nos dias marcados)", "Aba Atualizações > Canal > anexe feed.png > cole a legenda do bloco das 19:20."),
                     ("Quem comentar BLACK", "O post pede \"Comente BLACK\": o ManyChat responde com o link no Direct. Se algo falhar, peça ao Claude \"texto do Direct de DD/MM\".")],
                    ["Use os textos exatamente como estão em 1_TEXTOS_DO_DIA.txt: sem preço, sem \"mais vendido\" e com o aviso de afiliado.",
                     "Existe uma tarefa agendada diária (19:12) do Claude para o Status e o Canal. Se ela falhar ou o limite de uso do plano do Claude acabar, o plano B é publicar à mão com a pasta do dia.",
                     "O sócio direciona, mas o Claude continua sem digitar senhas, sem burlar captcha e sem aceitar termos: esses passos são sempre de uma pessoa.",
                     "Para o computador agendar, deixe-o ligado e o aplicativo do Claude aberto; o Instagram agenda no Chrome com a conta logada.",
                     "Guia curto para o sócio: Guia_Socio_Como_Pedir_ao_Claude.pdf (mesma pasta, 2 páginas). Os passos de cada envio estão também no Guia do sócio e no Anexo A."],
                    "todos os dias do calendário foram publicados e as visitas aparecem no relatório por origem.", extra=[datas])

    # 8 Anúncios fora do ar (Mercado Livre)
    st += atividade("8", "Anúncios fora do ar: 213 de 214 ativos; 1 pausado (item 77, fora do Top 10)", "Verificado em 03/11 às 12h12. O resto já foi tratado em 30/10", LARANJA, LARANJA_C,
                    "Você gera o link no ML Afiliados; o Claude troca no blog", "15 minutos por semana",
                    "Situação em 03/11 (12h12): 213 ativos e 1 pausado, o item 77 (Colágeno Verisol Bodyaction 200 g, fora do Top 10), possivelmente sem estoque. Pode ser temporário: espere uns dias e, se continuar pausado, gere um novo link do mesmo produto (catálogo MLB23792428). O resto já foi tratado. Os anúncios repetidos saíram em 30/10, as trocas foram feitas e a última checagem (02/11, 20h52) encontrou os 214 itens ativos. Esta atividade só vira trabalho se o painel voltar a avisar algum item. Por que existe: quando um anúncio é pausado ou removido no Mercado Livre, quem clica cai em \"Anúncio pausado\" ou num perfil vazio. A pessoa perde a confiança no blog "
                    "e você perde a comissão. O painel já avisa quais itens estão fora do ar, mas o link novo só você consegue gerar (o Claude não entra no ML sem login e não burla captcha).",
                    "Cada clique vira chance de compra: o guia nunca mostra produto quebrado, a taxa de clique para compra sobe e o Google valoriza páginas sem links com problema.",
                    [("Rode o painel", "Dois cliques em D:\\Projeto_Blog_Comprenolink\\Relatorios_Diarios_Anuncios\\ATUALIZAR_PAINEL.bat (ele verifica os anúncios se a última checagem passou de 12 horas)."),
                     ("Veja o quadro \"Anúncios fora do ar\"", "No PDF mais recente do painel: número do item, nome e motivo (pausado ou removido). Há também o quadro \"Substituição\" com os requisitos do produto novo."),
                     ("Escolha o substituto", "Mesmo tipo de produto, vendedor com boa reputação e a MELHOR política de venda (garantia, devolução, frete). O mais barato nem sempre é o melhor."),
                     ("Gere o link no ML Afiliados", "Abra o anúncio escolhido no Mercado Livre, use a opção de compartilhar/gerar link de afiliado e copie o link curto (meli.la)."),
                     ("Mande ao Claude", "Escreva: \"trocar item N por [link novo]\". O Claude troca no guia com backup, ajusta título, imagem e texto (sem preço), atualiza as categorias e aquece o cache."),
                     ("Confira no celular", "Abra o guia, procure o item e toque em \"Ver preço no Mercado Livre\": deve abrir o produto novo.")],
                    ["Não deixe anúncio fora do ar por mais de uma semana.",
                     "O Claude não usa a API do ML (exige token) nem páginas com verificação de conta: o link novo é sempre gerado por você.",
                     "Depois da troca, o painel registra a mudança no histórico de anúncios."],
                    "o quadro \"Anúncios fora do ar\" do painel está vazio (hoje já está).")

    # 9 Canal do WhatsApp
    st += atividade("14", "Crescimento seguro do Canal no WhatsApp: atração e convites à mão (sem automação)", "05/11 em diante", LARANJA, LARANJA_C, "Você (aprovar e enviar à mão) + Claude (lista, registro e relatório)", "20 minutos por dia",
                    "O Canal só cresce se mais gente souber dele. Automação de convites foi cancelada em 04/11 por risco de bloqueio do número do WhatsApp. Crescer por atração (Status, bio, Reels, Comente CANAL) e por convite pessoal à mão, só para quem você conhece.",
                    "Canal crescendo toda semana sem arriscar o WhatsApp do blog. Entra quem pede para entrar ou quem você convida pessoalmente.",
                    [("Texto do Comente CANAL (qui 05/11, 10:20)", "O Claude deixa pronto o convite do Canal e a resposta do ManyChat (ação G1). Você cola nas respostas do Direct e do ManyChat."),
                     ("Aprove contatos (qui 05/11, 10:30)", "Na aba Base, mude para Conhecido só quem você conhece de verdade. Os 500 contatos importados estão como Não perguntado e fora da fila."),
                     ("Convites à mão (a partir de 06/11, 10:00)", "Abra a aba Hoje, envie pelo celular, até 5 por dia na 1ª semana e até 9 depois, 3 minutos entre eles, mensagem personalizada. Depois escreva ao Claude: enviei Nome1, Nome2."),
                     ("Fechar o dia (20:30)", "Marque V ou X no Plano 30 dias do checklist_execucao_30_dias.xlsx e anote enviados, saídas e entradas."),
                     ("Revisão semanal (seg 09/11, 10:30)", "O Claude importa o formulário, lê os seguidores do Canal e mostra os indicadores. Você decide manter ou reduzir o ritmo."),
                     ("Pré-requisitos", "checklist_execucao_30_dias.xlsx > aba Pre-requisitos: 11 itens. Todo detalhe no processo_crescimento_canal_whatsapp.pdf e no guia_utilização_gerador_excel.pdf.")],
                    ["Nada de envio em massa nem de automação de mensagens pelo WhatsApp Web: há risco de restrição do número. Convite só à mão, só para quem você conhece.",
                     "Ao primeiro aviso do WhatsApp, pare os convites por 7 dias e avise o Claude. Com 2 pedidos de saída no dia ou 1 denúncia, pare os convites do dia.",
                     "Sem contatos aprovados, os convites esperam; a atração continua. Sem convites em 27/11 (Black Friday)."],
                    "a primeira semana de convites à mão fechou sem aviso do WhatsApp e o Canal chegou a 10 seguidores (meta estimada até 10/11).",
                    extra=[bloco("Situação de hoje (04/11/2026, noite)", [
                        "Base de contatos: 500 contatos importados do Google Contatos (você e a sócia Rosana), mais 55 na aba Reserva. Todos pendentes e fora da fila. Aptos hoje: 0.",
                        "Canal do WhatsApp: 2 seguidores. Formulário do blog com WhatsApp e consentimento: no ar, 0 inscrições.",
                        "Automação: CANCELADA. Nunca foi ligada. Tarefas agendadas: só a divulgação das 19:12.",
                        "Arquivos na pasta Planejamentos\\Andamento\\Base_Contatos_WhatsApp: 2 planilhas, 4 PDFs e a agenda agenda_crescimento_canal_whatsapp.ics. Versões antigas em _backups\\obsoleto_automacao."], AZUL, AZUL_C)])

    # 13
    st += atividade("11", "Uma página nova por semana (fones, TVs, presentes, celulares...)", "Toda semana, a partir de 09/11", AZUL, AZUL_C, "Claude escreve o rascunho; você revisa e dá opinião", "30 minutos seus (revisão); o Claude escreve o rascunho",
                    "Quem pesquisa no Google digita \"melhor fone bluetooth até 300 reais\", não \"21 produtos\". Páginas específicas aparecem melhor e convertem mais.",
                    "Cada página nova é mais uma porta de entrada no Google que trabalha por você por meses.",
                    [("Escolha o tema da semana", "Ordem sugerida: fones Bluetooth; Smart TV 32\"; presentes de Natal; celulares; \"JBL Tune vale a pena?\"; QCY x JBL."),
                     ("Peça o rascunho", "Escreva ao Claude \"página da semana: fones\". Ele monta 800 a 1.500 palavras, tabela no topo, 3 a 7 produtos, prós e contras e perguntas frequentes."),
                     ("Revise e acrescente opinião", "Texto genérico não rankeia. Acrescente o que você sabe e fotos suas, se tiver. Tire qualquer preço ou promessa."),
                     ("Publique e peça indexação", "O Claude publica com backup, liga a página ao guia e pede indexação no Search Console.")],
                    ["Cada página precisa de links UTM próprios para o relatório diferenciar a origem.",
                     "Não mude o endereço de uma página já indexada sem redirecionamento 301."],
                    "pelo menos 1 página nova publicada por semana.")

    # 12 anúncio
    st += atividade("12", "Teste de anúncio pago (decidido em 05/11)", "Conta Meta até 13/11; teste de R$ 50 de 16 a 18/11; Black Friday e Natal só se o semáforo ficar verde", AZUL, AZUL_C, "Você + Claude", "1 hora para montar; R$ 50 de orçamento total em 3 dias (cerca de R$ 16,67 por dia)",
                    "Com orçamento pequeno dá para descobrir se um produto e um público dão retorno antes de investir mais. Só faz sentido depois de a divulgação gratuita "
                    "ter trazido cliques e de o relatório estar medindo.",
                    "Você sabe quanto custa cada clique e cada venda do anúncio e decide com número, não com palpite.",
                    [("Confirme a verba", "Decidido em 05/11: o sócio pagador cria a conta Meta até 13/11. Teste de R$ 50 (16 a 18/11), Black Friday de R$ 105 e Natal de R$ 100, estes dois só se o semáforo ficar verde. Total máximo R$ 255; acima disso, só com nova reunião."),
                     ("Escolha o que impulsionar", "No Meta Business Suite, o post do Instagram que mais teve cliques orgânicos."),
                     ("Defina o destino", "A página do blog com link rastreável (utm_source=facebook&utm_medium=cpc), nunca direto o link meli.la."),
                     ("Configure", "Público Brasil, 18 a 45 anos, interesses do produto; orçamento total de R$ 50 até 18/11 (cerca de R$ 16,67 por dia)."),
                     ("Compare depois", "Na segunda seguinte: comissão gerada x valor gasto. Se não cobrir em 2 testes, volte ao orgânico.")],
                    ["Leia os termos do ML Afiliados antes: em geral é proibido usar a marca Mercado Livre em anúncios de busca e mandar o anúncio direto para o link de afiliado.",
                     "O TikTok Ads tem mínimo maior (cerca de R$ 50 por dia): deixe para depois."],
                    "você sabe o custo por clique e por venda do anúncio.")

    # 15
    st += atividade("13", "Trocar a bio do Instagram para o Natal", "01/12", AZUL, AZUL_C, "Você (celular)", "5 minutos",
                    "A bio hoje fala de Black Friday e o link 1 aponta para /black-friday. A campanha acaba em 30/11 e a página de Natal assume o menu e a home sozinha.",
                    "Quem entrar no perfil em dezembro vê o assunto certo e cai direto na página de presentes, que já está pronta.",
                    [("Abra o app do Instagram", "Perfil @compre.no.link > Editar perfil."),
                     ("Troque o link 1", "Links > o primeiro link vira comprenolink.net/presentes-de-natal."),
                     ("Troque a bio", "Peça ao Claude \"bio de Natal\": ele escreve a versão sem preço e com chamada para comentar a palavra do post."),
                     ("Confira", "Abra o link pelo celular e veja se a página de Natal carrega.")],
                    ["Links da bio só se editam no app do celular, não no computador."],
                    "o link da bio abre a página de Natal e a bio está atualizada.")

    # 15 consolidado das outras conversas
    st += atividade("15", "Pendências herdadas das outras conversas (consolidado em 04/11/2026, noite)", "05/11 em diante", LARANJA, LARANJA_C, "Você (decidir, apagar, trocar senha) + Claude (conferir e executar o que você aprovar)", "30 minutos na semana, em partes de 5 a 10 minutos",
                    "As conversas 001, 002 e 003 passaram o que ficou em aberto para esta conversa, e você decidiu trabalhar só nela. Aqui fica tudo num lugar só, para nada se perder.",
                    "Catálogo do WhatsApp certo, segurança do pacote em dia, vendas e medição conferidas e dezembro agendado sem surpresa.",
                    [("Qui 05/11, 10:00: reunião Turbinar com o sócio", "Feita em 05/11. Decidido: conta Meta em 13/11, teste de R$ 50 (16 a 18/11), BF R$ 105 e Natal R$ 100 mantidos (total máximo R$ 255). Termos do ML Afiliados: o Claude confere a regra antes de qualquer anúncio com link de afiliado."),
                     ("Catálogo do WhatsApp (celular)", "Regra decidida em 06/11: o catálogo é SÓ POR CATEGORIA, sem produtos individuais. Os 17 produtos antigos saem aos poucos (você apaga no celular; o Claude não apaga; comece pelos 10 com link antigo). Conferir se as categorias saíram de \"em análise\"."),
                     ("Frases leves (decidir)", "\"Dieta e alimentação leve\" na Air Fryer (11/11) e a foto da LG (26/11), com \"melhor\" na imagem do fabricante. Se você pedir, o Claude refaz só esse dia."),
                     ("Segurança do pacote do outro PC", "Se o zip 4_PACOTE_OUTRO_PC.zip de 29/10 (07:08) saiu deste PC, apague a cópia e troque a senha de aplicativo \"Painel Blog\". O Claude nunca digita senha. Teste o ATUALIZAR_AQUI.bat no outro PC; se algum .py mudou desde 29/10, rode antes o GERAR_EXE.bat. Nunca use o painel do WordPress nos dois PCs ao mesmo tempo."),
                     ("Vendas do ML Afiliados", "Mandar prints novos (o último lote é de 31/10), conferir se algum dos 12 \"em revisão\" foi compra própria e acompanhar a aprovação da Tampa para Micro-ondas."),
                     ("Medição (seg 09/11, junto da rodada semanal)", "Não entrou nenhuma visita rastreada de Instagram, WhatsApp ou ManyChat desde 31/10, e o painel mede só o guia. O Claude confere os UTM dos links da divulgação das 19:12 e propõe o ajuste do rastreio; você aprova antes de mexer."),
                     ("Dezembro (Claude, com seu OK)", "Conferir a foto dos pacotes de 09/12, 14/12 e 18/12, que foram refeitos, e agendar os Stories de dezembro. O post e o Reels do dia seguem o cron das 20:39.")],
                    ["Para não duplicar: só uma conversa agenda post e Reels no Instagram. A partir de 04/11 é esta. O Instagram só fica logado no Chrome \"Browser 1\".",
                     "Nada que apaga, troca senha ou mexe no site é feito sem a sua palavra."],
                    "o catálogo está limpo, a senha foi trocada (se for o caso), as vendas conferidas e dezembro agendado.")

    # Agenda do Claude
    st += [PageBreak(), faixa("C", "O que o Claude faz (e quando)", "Conferências e tarefas dele, para você saber que estão cobertas", VERDE), Spacer(1, 6),
           P("Estas atividades são do Claude. Você não precisa fazer nada, a não ser responder se ele pedir uma aprovação.", "p"), Spacer(1, 4),
           tabela(["Quando", "O que o Claude faz", "Por quê"],
                  [["Todo dia, ~20:39", "Agendar no Instagram o post (19:00) e o Reels (19:05) do dia que a janela de 29 dias acabou de abrir (04/12 em 05/11, 07/12 em 08/11...).", "O Instagram só aceita 29 dias à frente. Um cron só, nesta conversa, para não duplicar."],
                   ["Todo dia, 19:10 e 20:30", "Conferir que o Story saiu e marcar Feito=S na planilha 04_CALENDARIO_POSTS_NOV_DEZ.xlsx do que foi publicado.", "A planilha só vale se for marcada na hora."],
                   ["06/11 e 09/11", "Conferir se o Google Analytics (Site Kit) já mostra visitantes e se o Bing leu os 2 mapas do site.", "Os dados levam até 48 horas; garante que a medição está ligada."],
                   ["Sexta 06/11", "Rotina de SEO pelo Chrome, se você pedir \"rotina de sexta\".", "Constância no Google."],
                   ["10/11", "Conferir no Search Console se /presentes-de-natal/ foi indexada.", "A página foi antecipada para amadurecer no Google."],
                   ["13/11, 26/11 e 11/12", "Rodar o painel, conferir anúncios e links do guia e só então atualizar a data \"Atualizado em\".", "Não carimbar data sem revisar."],
                   ["A cada 3 horas", "O gerador republica categorias, Black Friday e Natal com backup e cache aquecido.", "Já é automático, sem ação sua."],
                   ["Seg 10:00 e sex 12:00", "Conferir o uso do plano do Claude e se a tarefa das 19:12 continua ativa", "Para não parar a publicação no meio da Black Friday."],
                   ["20:00 em 05, 08, 10, 12, 15, 17, 19, 22 e 24/11", "Quando a janela de 29 dias do Instagram abre, você escreve agendar DD/MM e o Claude agenda post e Reels do dia", "O Instagram só aceita 29 dias à frente; a agenda lembra você a cada noite."],
                   ["03/10/2027", "Desligar a renovação automática do e-mail grátis (teste de 12 meses) ou decidir mantê-lo.", "Evitar cobrança do plano pago depois do teste."],
                   ["01/12", "Conferir que o menu e a home trocaram para o Natal e que a Black Friday mostra o aviso de fim.", "Troca automática de campanha."],
                   ["Seg 09/11, 10:30", "Importar o formulário do blog, ler os seguidores do Canal e fazer o relatório da semana.", "Acompanhar o crescimento do Canal."],
                   ["Todo dia, até 10:00", "Preparar a lista de convites do dia e os textos. O Claude só prepara; você envia à mão.", "Convite pessoal sem automação, para não arriscar o WhatsApp."],
                   ["Opcional", "Desativar o WPForms (o formulário antigo, sem uso) e corrigir o título H1 duplicado da página inicial.", "Limpeza e leve ganho de velocidade."]],
                  [0.17, 0.5, 0.33], cor=VERDE), Spacer(1, 8),
           bloco("Regras que valem para tudo", [
               "Sem preço, sem \"mais vendido\", \"líder\" ou \"oferta do mês\" e sem promessa de saúde ou estética.",
               "Sempre o aviso de link de afiliado nos textos e nas redes (#publi).",
               "Mudar UMA coisa por semana e olhar o resultado na segunda seguinte.",
               "O Claude nunca digita senhas, não burla captcha e não aceita termos por você: nesses momentos ele para e avisa.",
               "Todo ajuste no site tem backup antes (pasta 2_DADOS\\Blog_WordPress\\backups).",
               "Se der problema que o Claude consiga resolver, ele procura a solução e executa (tenta outros caminhos antes de avisar). Não se replaneja: a tarefa continua no mesmo dia.",
               "Escreva ao Claude sempre em português e, se travar, mande um print da tela."], VERMELHO, VERMELHO_C)]

    st += [PageBreak(), faixa("A", "Anexo A: processo semanal de vendas (ML Afiliados) e catálogo do WhatsApp", "Toda segunda, 10:15 (lembrete na agenda) • herdado do documento de 31/10", LARANJA), Spacer(1, 6),
           info([("Por que existe", "O blog não enxerga compras: só o painel do ML Afiliados mostra as vendas. E a conta do blog não tem botão para exportar a lista, então o caminho é por prints."),
                 ("Benefício", "O painel de conversão passa a mostrar vendas reais por produto e por origem, e você decide o que repetir."),
                 ("Tempo", "15 minutos por semana")]), Spacer(1, 6),
           passos([("Entre na conta certa", "No Chrome, abra mercadolivre.com.br/afiliados/dashboard. A conta certa é a que mostra ganho estimado perto de R$ 172 nos últimos 180 dias (é a que criou os links do blog). Se não bater, troque de conta."),
                   ("Escolha o período", "Métricas > Período > Últimos 180 dias."),
                   ("Abra Vendas e marque os 4 status", "Aba Vendas > filtro Status: Aprovada, Em revisão, Recusada e Cancelada (marcar todas dá o quadro completo)."),
                   ("Tire os prints", "Um print de cada trecho da tabela, rolando a página inteira. Se houver mais de uma página (\"1 2\" no rodapé), um print de cada página. Não pule nenhuma."),
                   ("Mande ao Claude", "Envie os prints em sequência, avisando que são da tabela de Vendas. O Claude lê as vendas e atualiza o arquivo vendas_ml_AAAA-MM-DD.csv em Relatorios_Diarios_Anuncios\\vendas_afiliados."),
                   ("Confira o total", "O número de linhas do arquivo deve bater com o \"N resultados\" que a tela do ML mostra."),
                   ("Rode o painel", "Feche o Excel se estiver aberto e dê dois cliques em Relatorios_Diarios_Anuncios\\ATUALIZAR_PAINEL.bat. Ele verifica os anúncios, processa as vendas e abre a planilha. Se mostrar erro, tire um print e mande ao Claude.")], LARANJA),
           Spacer(1, 6),
           bloco("Catálogo do WhatsApp (só quando o blog ganhar categoria nova)", [
               "O catálogo é por categoria. Hoje o blog tem 9 categorias; a que falta cadastrar é Moda Infantil & Juvenil, sugestão: ter 10/11, 15 min (item CAT-moda-infantil-e-juvenil, com foto e texto prontos em 06_CATALOGO_WHATSAPP).",
               "Como: WhatsApp Business > Ferramentas comerciais > Catálogo > adicionar item.",
               "O histórico de vendas nunca duplica: reenviar uma venda só atualiza o status (por exemplo, de Em revisão para Aprovada)."], AZUL, AZUL_C),
           Spacer(1, 12),
           faixa("B", "Anexo B: outras pendências dos documentos antigos", "Com data ou sem data • nada foi perdido ao juntar tudo em um arquivo", AZUL), Spacer(1, 6),
           tabela(["Quando", "Pendência", "Quem", "Observação"],
                  [["05/11 (qui)", "Republicar o blog das máquinas (Google Sites)", "Você", "Pasta Gestao_Anuncios_Blog\\1_PROGRAMAS\\Blog_Maquinas. Peça o passo a passo ao Claude."],
                   ["07/11 (sáb)", "Criar os Destaques do Instagram (Black Friday, Categorias, Como comprar)", "Você (celular)", "Os Destaques só se criam no celular; o Claude gera as capas se você pedir."],
                   ["09/11 (seg)", "Decisões: QCY Shopee, nota antiga no painel das máquinas e divulgação de longo prazo", "Você + Claude", "Conversa de 15 minutos."],
                   ["11/11 (qua)", "Confirmar o teste da automação BLACK do ManyChat com outra conta e a resposta automática no Direct", "Você", "Eram tarefas de 30/10. Se já foram feitas, avise para dar baixa."],
                   ["12/11 (qui)", "Confirmar se os dois computadores sincronizam a pasta de scripts (um arquivo voltou à versão antiga em 31/10)", "Você", "Veja se há tarefa de cópia entre este PC e o outro (lenovo) e me diga a direção."],
                   ["13/11 (sex)", "Turbinar pago: conta de anúncios Meta JÁ CRIADA em 05/11 (cartão Visa do dono e limite de gastos R$ 50). Teste de R$ 50 em 16 a 18/11 (orçamento total, cerca de R$ 16,67 por dia), avaliação em 19/11",
                    "Você (cartão de crédito)", "Decidido na reunião de 05/11 (substitui o ADIADO de 03/11). Limite de gastos mensal: R$ 50 agora; subir para R$ 155 em 20/11 (só se o teste ficou no verde) e para R$ 100 em 04/12 (só se a Black Friday se pagou). Black Friday de R$ 105 (21 a 27/11) e Natal de R$ 100 (05 a 14/12) seguem o semáforo: só se a fase anterior ficar no verde. Avaliações em 19/11 e 30/11 e relatório final em 21/12 (o Claude faz). Total máximo R$ 255; nunca passa disso sem nova reunião."],
                   ["Sem data", "Outlook com compre.no.link26@gmail.com", "Você + Claude", "Adiado: depende de ligar a verificação em 2 etapas ou do e-mail da atividade 4."],
                   ["26/12 (sáb)", "Instagram: o link 1 da bio volta para comprenolink.net", "Você (celular)", "Depois do Natal."],
],
                  [0.12, 0.38, 0.14, 0.36], cor=AZUL), Spacer(1, 8),
           bloco("Sobre os arquivos antigos de pendências", [
               "Este documento é o único arquivo de pendências a partir de 03/11/2026.",
               "Os documentos antigos de pendências (cronograma de 27/10, listas de 29/10 e 31/10, processo semanal de 31/10) e o registro de decisões tiveram o que estava aberto passado para cá e foram removidos. Se precisar de algum, ele está na Lixeira do Windows.",
               "Os geradores deles continuam em Programas_Diversos_Py, se um dia for preciso refazer algum."], VERDE, VERDE_C)]
    st += [PageBreak(), faixa("G", "Anexo G: crescimento do Instagram e do WhatsApp (o que ainda não fazemos)", "Grátis primeiro; o pago só entra com verba liberada pelos sócios", AZUL), Spacer(1, 6),
           info([("Por que existe", "O conteúdo sai todo dia, mas faltam as ações que fazem mais gente chegar e voltar. Esta tabela lista cada uma, o que precisa ser feito, quem faz, quando e o que o PAGO acrescentaria."),
                 ("Já fazemos", "Reels e post todos os dias, Story com link, Status e Canal diários, ManyChat (BLACK e NATAL), botões do Canal e do Instagram no blog, Canal e link do WhatsApp na bio."),
                 ("Regra do plano", "Turbinar pago liberado em 05/11 (teste R$ 50, Black Friday R$ 105, Natal R$ 100). As demais ferramentas pagas seguem sem verba. Os valores da última coluna são de REFERÊNCIA para vocês decidirem; preços de ferramentas mudam: confirme no site antes de contratar.")]), Spacer(1, 6),
           tabela(["#", "Ação", "Situação hoje", "O que fazer", "Quem e quando", "Pago que turbina e custo por mês"],
                  [["G1", "Convite do Canal nas respostas automáticas", "Respostas salvas só trazem o WhatsApp, sem o Canal", "Acrescentar frase e link do Canal no Direct e no ManyChat", "Claude escreve, você cola. Qui 05/11, 10 min", "ManyChat Pro (mais contatos e fluxos): a partir de cerca de US$ 15 (estimativa). O grátis basta por ora: R$ 0"],
                   ["G2", "Destaques do Instagram", "Não existem", "Criar Black Friday, Categorias, Como comprar e Canal do WhatsApp", "Você no celular, Claude faz as capas. Sáb 07/11, 30 min", "Nenhum. Canva Pro só se quiserem mais modelos: cerca de R$ 35 (estimativa). Padrão: R$ 0"],
                   ["G3", "Responder comentários na 1ª hora", "Não é sistemático", "Reservar 5 min depois das 19:00 na rotina das 19:10", "Você ou o sócio. Hoje, 5 min por dia", "Nenhum: R$ 0"],
                   ["G4", "Catálogo do WhatsApp completo", "8 de 9 categorias; falta Moda Infantil", "Cadastrar com foto e texto prontos", "Você no celular. Ter 10/11, 15 min", "Nenhum: R$ 0"],
                   ["G5", "Saudação, ausência e etiquetas do WhatsApp Business", "Textos prontos; não confirmado no app", "Conferir no app e aplicar o que faltar", "Você no celular. Sáb 07/11, 10 min", "Nenhum: R$ 0"],
                                      ["G7", "Gancho de 2 segundos nos Reels", "Sem padrão de abertura", "Ajustar o texto de abertura no gerador de vídeos", "Claude. Até qui 05/11, 30 min (vale a partir do dia 04/12)", "Edição profissional de vídeo (ex.: CapCut Pro) cerca de R$ 40 (estimativa). Padrão: R$ 0"],
                   ["G8", "Hashtags certas", "9 em todo post", "Testar 5 bem ligadas ao produto", "Claude. A partir do dia 04/12", "Nenhum: R$ 0"],
                   ["G9", "Áudio em alta nos Reels", "Vídeos sem música", "Testar em 3 Reels (contas comerciais têm biblioteca limitada)", "Claude. Teste a partir do dia 04/12", "Nenhum: R$ 0"],
                   ["G10", "Enquete ou caixa de perguntas nos Stories", "Stories só com link", "Testar no Business Suite; senão, pelo celular 2 vezes por semana", "Claude ou você. Teste sex 06/11, 2 min", "Nenhum: R$ 0"],
                   ["G11", "Escolher o post campeão e repetir o formato", "A reunião de segunda só olha números", "Incluir \"qual post teve mais alcance e salvamentos\" no roteiro", "Claude ajusta. Seg 09/11", "Impulsionar o post campeão no Instagram: referência R$ 100 a R$ 300 por mês (ver abaixo)"]],
                  [0.07, 0.16, 0.17, 0.2, 0.18, 0.22], cor=AZUL), Spacer(1, 8),
           P("O que o PAGO turbinaria mais (referência mensal)", "h2"),
           tabela(["Opção paga", "O que faz", "Custo por mês (referência)", "Observação"],
                  [["Anúncio de tráfego para o Canal do WhatsApp (Meta Ads)", "Leva gente nova direto para o Canal e para o blog", "R$ 100 a R$ 300", "Decidido em 05/11: novembro com R$ 50 de teste + R$ 105 da Black Friday = R$ 155. Dezembro: R$ 100 (Natal). Total máximo R$ 255"],
                   ["Impulsionar o post ou Reels campeão", "Mostra o melhor conteúdo para mais perfis parecidos com os seguidores", "R$ 100 a R$ 300", "Só depois de saber qual post é o campeão (G11) e com vendas aprovadas"],
                   ["ManyChat Pro", "Mais contatos e automações no Direct", "cerca de US$ 15 (estimativa)", "Só se o plano grátis estourar o limite de contatos"],
                   ["Canva Pro ou CapCut Pro", "Mais modelos de arte e edição de vídeo", "R$ 35 a R$ 40 (estimativa)", "Não é essencial: as artes e os vídeos já saem dos nossos geradores"]],
                  [0.3, 0.3, 0.17, 0.23], cor=LARANJA), Spacer(1, 6),
           bloco("Leitura rápida", [
               "As 10 ações da tabela são gratuitas. O pago só acelera quando já houver um post campeão e vendas aprovadas.",
               "Reserva de referência, se os sócios liberarem: de R$ 100 a R$ 300 por mês em anúncios, mais, se quiserem, cerca de R$ 35 a R$ 55 em ferramentas.",
               "Estes valores não foram contratados nem aprovados. Nada pago acontece sem a decisão dos sócios."], VERMELHO, VERMELHO_C)]
    st += [PageBreak(), faixa("H", "Anexo H: diagnóstico de 04/11 - estamos aplicando?", "Conferido no Instagram e no Meta Business Suite (somente leitura)", VERMELHO), Spacer(1, 6),
           info([("Resultado", "Das ações abertas do Anexo G, 1 está parcial, 2 não deu para conferir e 7 NÃO estão aplicadas. O que já estava aplicado (link do WhatsApp na bio) e a divergência do Canal fora da bio, corrigida em 04/11, saíram desta lista."),
                 ("Como foi conferido", "Perfil @compre.no.link aberto no Instagram, Meta Business Suite (Percepções, últimos 28 dias: 07/10 a 03/11) e os arquivos do projeto. Nada foi alterado.")]), Spacer(1, 6),
           P("Números reais do Instagram (últimos 28 dias)", "h2"),
           tabela(["Indicador", "Valor", "O que significa"],
                  [["Seguidores / seguindo", "12 / 73", "Conta nova: segue mais gente do que tem seguidores"],
                   ["Publicações no perfil", "3", "Os posts agendados ainda não saíram; só 3 estão publicados"],
                   ["Visualizações", "49", "Pouco alcance, como esperado para uma conta com 12 seguidores"],
                   ["Contas alcançadas", "14", "Quase só seguidores e conhecidos"],
                   ["Interações com o conteúdo", "17", "Curtidas, comentários e salvamentos"],
                   ["Visitas ao perfil", "47", "Há curiosidade: quem chega ao perfil olha"],
                   ["Cliques em links", "1", "Gargalo principal: quase ninguém sai do Instagram para o blog ou para o Canal"]],
                  [0.3, 0.14, 0.56], cor=VERMELHO), Spacer(1, 6),
           P("Anexo G: o que está aplicado de verdade", "h2"),
           tabela(["#", "Ação", "Aplicando?", "Evidência", "Próximo passo"],
                  [["G1", "Convite do Canal nas respostas automáticas", "NÃO", "As respostas salvas só trazem o WhatsApp; ManyChat não conferido", "Qui 05/11: Claude escreve, você cola"],
                   ["G2", "Destaques do Instagram", "NÃO", "O perfil só mostra o botão Novo, sem nenhum Destaque", "Sáb 07/11"],
                   ["G3", "Responder comentários na 1ª hora", "NÃO CONFERIDO", "Sem registro; há 7 comentários e 5 seguidores novos nas notificações", "Rotina das 19:10"],
                   ["G4", "Catálogo do WhatsApp", "PARCIAL", "8 de 9 categorias nos arquivos; app não conferido", "Ter 10/11: Moda Infantil"],
                   ["G5", "Saudação, ausência e etiquetas", "NÃO CONFERIDO", "Textos prontos; só o celular mostra se foram aplicados", "Sáb 07/11"],
                                      ["G7", "Gancho de 2 segundos nos Reels", "NÃO", "Os Reels agendados não têm esse padrão", "Até qui 05/11"],
                   ["G8", "Hashtags certas", "NÃO", "Os posts usam 9 hashtags", "A partir do dia 04/12"],
                   ["G9", "Áudio em alta nos Reels", "NÃO", "Os vídeos saem sem música", "Teste a partir do dia 04/12"],
                   ["G10", "Enquete nos Stories", "NÃO", "Os Stories só têm o link", "Teste sex 06/11"],
                   ["G11", "Escolher o post campeão", "NÃO", "A reunião de segunda só olha números", "Seg 09/11"]],
                  [0.07, 0.2, 0.14, 0.34, 0.25], cor=AZUL), Spacer(1, 6),
           P("Os 3 fatores críticos (texto que você enviou) e se aplicamos", "h2"),
           tabela(["Fator", "Aplicamos?", "Como estamos", "Próximo passo"],
                  [
                                     ["2. Cookie de 24 h e venda indireta", "PARCIAL", "Postamos e usamos Status e Canal todos os dias, o que gera cliques no mesmo dia. Não medimos vendas indiretas. A regra das 24 h é a informação do texto que você enviou; não a conferi nas regras do ML Afiliados", "Na segunda, ao ler as vendas por prints, separar o que foi comprado fora do produto do link"],
                   ["3. Distribuição multicanal (Telegram e WhatsApp)", "PARCIAL", "WhatsApp Canal e Status: sim. Telegram: NÃO, fora do foco por decisão de 03/11", "Decisão sua: reavaliar o Telegram depois da Black Friday, ou criar o canal já (custo R$ 0)"]],
                  [0.2, 0.12, 0.4, 0.28], cor=LARANJA), Spacer(1, 6),
           bloco("Leitura final", [
               "O que fazemos todo dia (post, Reels, Story, Status, Canal) está rodando. O que falta é fazer o tráfego sair do Instagram: 1 clique em link em 28 dias.",
               "Prioridade 1: convite do Canal nas respostas e Destaques (05 a 07/11). Prioridade 2: atração e convites à mão para o Canal (atividade 14, início 06/11). Prioridade 3: gancho, hashtags e áudio nos Reels do dia 04/12 em diante.",
               "Só depois de ter post campeão e dados, faz sentido discutir o pago (Anexo G)."], AZUL, AZUL_C)]
    st += [PageBreak(), faixa("I", "Anexo I: quanto % estamos adequados e quando fecha o que falta", "Conferido em 04/11 • regra: SIM = 1 ponto, PARCIAL = meio ponto, NÃO ou NÃO CONFERIDO = 0", VERMELHO), Spacer(1, 6),
           tabela(["Bloco", "Itens", "Pontos", "Adequado", "Falta"],
                  [["Instagram (G2, G3, G6 a G11 e Canal na bio)", "9", "2 de 9", "22%", "78%"],
                   ["WhatsApp e Canal (G1, G4, G5)", "3", "0,5 de 3", "17%", "83%"],
                   ["Fatores de operação (links/estoque, cookie, multicanal)", "3", "2 de 3", "67%", "33%"],
                   ["<b>TOTAL</b>", "<b>15</b>", "<b>4,5 de 15</b>", "<b>30%</b>", "<b>70%</b>"]],
                  [0.46, 0.1, 0.16, 0.14, 0.14], cor=VERMELHO), Spacer(1, 4),
           P("Os 30% (com o Canal na bio, feito em 04/11) usam pesos iguais para todos os itens e contam como zero o que não deu para conferir (G3 e G5). Se esses dois já estiverem em uso, o total sobe um pouco. O que está pronto e funcionando todo dia (post, Reels, Story, Status, Canal) não entra na conta: ela mede só o que ainda impulsiona o alcance.", "p"), Spacer(1, 8),
           P("O que falta, quando será feito (dia e horário)", "h2"),
           tabela(["Quando", "O que falta", "Quem", "Tempo", "Faz subir"],
                  [["Todo dia, 19:20", "Responder comentários e Direct logo depois do post das 19:00 (G3)", "Você ou o sócio", "5 min por dia", "Instagram"],
                   ["Qui 05/11, 10:20", "Convite do Canal nas respostas automáticas do Direct e do ManyChat (G1)", "Claude escreve, você cola", "10 min", "WhatsApp"],
                   ["Qui 05/11, 11:00", "Padrão de gancho de 2 segundos nos Reels, no gerador de vídeos (G7)", "Claude", "30 min", "Instagram"],
                   ["Sex 06/11, 19:10", "Teste de enquete ou caixa de perguntas no Story (G10)", "Claude ou você", "2 min", "Instagram"],
                   ["Qui 05/11, 20:00", "Agendar o dia 04/12 já com 5 hashtags e áudio de teste (G8 e G9)", "Claude (você escreve agendar 04/12)", "15 min", "Instagram"],
                   ["Sáb 07/11, 10:00", "Criar os Destaques: Black Friday, Categorias, Como comprar e Canal (G2)", "Você no celular; Claude faz as capas", "30 min", "Instagram"],
                   ["Sáb 07/11, 10:40", "Conferir e aplicar saudação, ausência e etiquetas no WhatsApp Business (G5)", "Você no celular", "10 min", "WhatsApp"],
                   ["Seg 09/11, 10:15", "Ler as vendas por prints separando as indiretas (compra de outro produto em até 24 h)", "Você + Claude", "dentro dos 15 min", "Fatores"],
                   ["Seg 09/11, 10:45", "Reunião: incluir o post com mais alcance e salvamentos e repetir o formato (G11)", "Você + Claude", "dentro dos 30 min", "Instagram"],
                   ["Seg 09/11, 11:15", "Decidir o Telegram: criar o canal agora (custo R$ 0) ou depois da Black Friday", "Você", "5 min", "Fatores"],
                   ["Seg 09/11, 11:45", "Item 77 (Colágeno): se continuar pausado, trocar o link", "Você traz o link, Claude troca", "10 min", "Fatores"],
                   ["Ter 10/11, 14:00", "Cadastrar Moda Infantil no catálogo do WhatsApp (G4)", "Você no celular", "15 min", "WhatsApp"]],
                  [0.2, 0.36, 0.18, 0.13, 0.13], cor=AZUL), Spacer(1, 6),
           bloco("Meta realista", [
               "Se tudo isso for feito até 10/11, passamos de 30% para cerca de 85% (13 de 15 itens). O restante é teste e depende de dados: áudio em alta (conta comercial pode ter biblioteca limitada) e Telegram.",
               "Nenhum horário cai às 16h, e cada dia fica com 30 minutos ou menos fora a rotina das 19:10.",
               "Estes horários são propostas. Eles só entram na agenda se você disser, para não contrariar a agenda já importada."], VERDE, VERDE_C)]
    return st


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Pendências abertas (comprenolink.net)", author="comprenolink.net")
    doc.build(conteudo(), onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
