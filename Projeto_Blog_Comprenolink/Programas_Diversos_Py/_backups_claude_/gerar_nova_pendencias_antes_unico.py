# -*- coding: utf-8 -*-
"""nova_pendencias.pdf: o que ainda falta executar (dono e Claude), com passo a passo, o porquê e o benefício.
Estado em 03/11/2026, depois da análise do Checklist Turbinar (passos 7, 8, 9, 19, 20, 21, 22 e 23 já concluídos).
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
base.HOJE = date(2026, 11, 3)
GUIA = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"
BF = "https://comprenolink.net/black-friday/"


def atividade(num, titulo, quando, cor, cor_c, quem, tempo, por_que, beneficio, lista, detalhes=None, pronto=None, extra=None):
    """Uma atividade completa: faixa, quadro-resumo, por quê, benefício, passo a passo, detalhes e critério de pronto."""
    topo = KeepTogether([faixa(num, titulo, quando, cor), Spacer(1, 4),
                         info([("Quem faz", quem), ("Tempo", tempo), ("Por que fazer", por_que), ("Benefício", beneficio)]), Spacer(1, 6),
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
            "comprenolink.net • Instagram @compre.no.link • WhatsApp (11) 99495-9657 • posição de 03/11/2026", "capa_s"), Spacer(1, 8),
          info([("Como usar", "Cada atividade tem: quem faz, quanto tempo leva, POR QUE fazer, o BENEFÍCIO e o passo a passo. Siga a ordem da tabela abaixo: "
                              "as primeiras são as mais urgentes ou as que destravam as outras."),
                ("Foco", "WhatsApp, Instagram, Mercado Livre e ajustes do blog (TikTok descartado em 03/11)."),
                ("Cores", "Vermelho = urgente. Laranja = importante nesta semana. Azul = planejado com data. Verde = rotina que se repete."),
                ("Se travar", "Escreva ao Claude com um print da tela. Para tudo que exige senha, código de celular ou aceite de termos, o Claude para e avisa: "
                              "essa parte é sempre sua."),
                ("Registro", "Tudo que já foi decidido e feito está em Decisoes_Checklist_Turbinar_03-11-2026.txt (mesma pasta).")]),
          Spacer(1, 8), P("Resumo em ordem de execução", "h2"),
          tabela(["#", "Atividade", "Quem", "Quando", "Tempo"],
                 [["1", "Decisões da reunião com o sócio (REGISTRADAS)", "Feito", "03/11", "concluída"],
                  ["2", "Agenda das rotinas IMPORTADA; falta só abrir a planilha", "Feito", "03/11", "2 min"],
                  ["3", "Ligar a renovação automática do domínio e da hospedagem", "Você", "Esta semana", "10 min"],
                  ["4", "Criar o e-mail alertas@comprenolink.net (aviso das inscrições)", "Você + Claude", "Esta semana", "15 min"],
                  ["5", "Vendas recusadas: conta CONFERIDA; falta só checar os 12 em revisão", "Você", "Esta semana", "5 min"],
                  ["6", "Rotinas: SEO na sexta 06/11 e números na segunda 09/11", "Você (+ Claude)", "06/11 e 09/11", "1 h e 30 min"],
                  ["7", "Calendário de divulgação da Black Friday (WhatsApp e Instagram)", "Você + Claude", "10/11 a 30/11", "10 min por dia"],
                  ["8", "Anúncios: 213 de 214 ativos; 1 pausado (item 77, Colágeno Verisol)", "Você (link novo)", "Quando puder", "10 min"],
                  ["9", "Canal do WhatsApp: link no blog FEITO; falta bio, convites e contagem", "Você", "Esta semana", "10 min + 10/sem"],
                  ["10", "Acabamento do guia: FEITO (\"Não compre se...\", descrição, logotipo)", "Feito", "03/11", "concluída"],
                  ["11", "Uma página nova por semana (fones, TVs, presentes...)", "Claude escreve, você revisa", "Toda semana", "2 h por página"],
                  ["12", "Teste de anúncio pago no Instagram/Facebook (ADIADO: sem verba)", "Você + Claude", "Só com verba liberada", "1 h + R$ 70 a 140"],
                  ["13", "Trocar a bio do Instagram para o Natal", "Você (celular)", "01/12", "5 min"]],
                 [0.05, 0.5, 0.17, 0.16, 0.12], cor=LARANJA), Spacer(1, 4),
          bloco("Foco definido em 03/11: WhatsApp, Instagram, Mercado Livre e ajustes do blog", [
              "TikTok: descartado a pedido do dono. Os 3 vídeos ficam guardados na pasta VIDEOS TIKTOK, sem uso.",
              "Telegram, YouTube/Facebook e Pinterest: fora do foco por enquanto. Só voltam se sobrar tempo depois da Black Friday (peça ao Claude).",
              "Menos canais, feitos com constância, rendem mais do que muitos canais abandonados."], AZUL, AZUL_C), Spacer(1, 8),
          bloco("Já concluído hoje (03/11) – não precisa repetir", [
              "Passo 7: Google Search Console e Bing (site verificado, sitemap enviado, páginas indexadas).",
              "Passo 8: Google Analytics 4 ligado ao site pelo Site Kit; Política de Privacidade atualizada.",
              "Passo 9: velocidade medida (nota 91 no celular).",
              "Passo 19: página Black Friday com contador e seção \"Como saber se o desconto é real\".",
              "Passo 20: página de presentes de Natal publicada antes do prazo e enviada ao Google.",
              "Passo 22: formulário de alertas guardando as inscrições no próprio site (Fluent Forms).",
              "Passos 21 e 23: roteiro, planilha semanal e agenda das rotinas."], VERDE, VERDE_C),
          PageBreak()]

    # 1
    st += atividade("1", "Decisões da reunião com o sócio: REGISTRADAS", "Decidido em 03/11 (falta só a dúvida da conta vinculada)", VERDE, VERDE_C, "Você (feito) + Claude (registrou)", "Concluída",
                    "A reunião sobre o Plano Turbinar e os termos do ML Afiliados estava marcada para hoje às 10:00. O Claude só consegue ajustar o plano "
                    "(verba, produtos, canais) se souber o que foi decidido.",
                    "Evita trabalhar no escuro: o plano de divulgação, os anúncios e as rotinas passam a seguir o que vocês combinaram, e a verba "
                    "do teste pago (atividade 14) fica definida.",
                    [("Anote em poucas linhas", "Escreva no celular ou num papel: (a) vão usar o Turbinar? (b) qual verba por dia e por quantos dias? "
                                                 "(c) quais produtos primeiro? (d) quem publica os Stories e envios quando você não puder?"),
                     ("Anote a dúvida da conta vinculada", "Por que 7 vendas foram recusadas por \"conta vinculada\" (resolvido na atividade 5)? Se o sócio souber, anote a resposta."),
                     ("Mande ao Claude", "Cole as linhas aqui na conversa. O Claude atualiza o plano e registra no arquivo de decisões."),
                     ("Leia os termos do Turbinar", "Antes de qualquer verba: confirme nos termos do ML Afiliados o que é permitido em divulgação paga.")],
                    ["Nunca mande senha ou dados de cartão na conversa.", "Se a reunião foi adiada, escreva \"reunião adiada para DD/MM\" e o Claude move o lembrete."],
                    "o Claude confirmou que registrou as decisões e atualizou o plano.",
                    extra=[bloco("Decisões combinadas e registradas em 03/11/2026", [
                        "Plano Turbinar: vamos usar, na parte gratuita (orgânica), seguindo o foco WhatsApp, Instagram, Mercado Livre e blog.",
                        "Verba paga por dia: nenhuma por enquanto. Só se libera depois de existirem vendas aprovadas (regra de ouro do dinheiro).",
                        "Produtos primeiro: o Top 10 da Black Friday (página /black-friday/).",
                        "Quando você não puder publicar: o sócio direciona o Claude para publicar (comandos e limites na atividade 7).",
                        "Resolvido: as 7 vendas recusadas por \"conta vinculada\" foram compras do próprio dono (atividade 5)."], VERDE, VERDE_C)])

    # 2
    st += atividade("2", "Agenda das rotinas IMPORTADA; falta abrir a planilha", "Agenda feita em 03/11 pelo Claude", VERDE, VERDE_C, "Claude (feito) + Você (abrir a planilha)", "2 minutos",
                    "As rotinas de segunda (números) e de sexta (SEO) só funcionam se virarem hábito. A agenda coloca os lembretes no seu celular nos horários certos.",
                    "Você não precisa lembrar: o celular avisa. Em 10 minutos por semana você enxerga o que está dando resultado e o que deve ser trocado, "
                    "em vez de postar às cegas.",
                    [("Abra a pasta", "D:\\Projeto_Blog_Comprenolink\\0- Pendencias\\1_Pendencias"),
                     ("Importe a agenda", "Dê dois cliques em Agenda_Rotinas_Semanais.ics. Escolha o Google Agenda (ou o calendário do celular) e confirme. "
                                           "Aparecem: segunda 10:45 (reunião dos números), sexta 14:00 (rotina de SEO) e as conferências do guia em 13/11, 26/11 e 11/12."),
                     ("Abra a planilha", "Planilha_Semanal_Turbinar.xlsx. As semanas 1 e 2 já estão preenchidas. Veja como a taxa de clique e a \"leitura automática\" funcionam."),
                     ("Leia o roteiro", "Roteiro_Rotinas_Segunda_e_Sexta.pdf (3 páginas): o passo a passo de cada rotina.")],
                    ["Já existe um lembrete de segunda 10:15 (exportar vendas e rodar o painel). A nova reunião é às 10:45, logo depois: não conflita.",
                     "O contador de visitas do painel inclui testes e as suas próprias visitas. Olhe os visitantes únicos."],
                    "os eventos aparecem no seu calendário e a planilha abre sem erro.")

    # 3
    st += atividade("3", "Ligar a renovação automática do domínio e da hospedagem", "Esta semana", LARANJA, LARANJA_C, "Você", "10 minutos",
                    "Se o domínio comprenolink.net ou a hospedagem vencerem sem renovar, o site sai do ar. Em plena Black Friday isso significaria perder a venda "
                    "da época mais forte do ano. A renovação costuma ser mais cara que o primeiro ano, então vale saber a data.",
                    "Tranquilidade: o site fica no ar sem você precisar lembrar de pagar na hora certa, e você sabe quanto vai custar.",
                    [("Entre na Hostinger", "hpanel.hostinger.com. Se o login estiver bloqueado por tentativas, espere 30 minutos e use \"Esqueceu sua senha?\". "
                                            "Faça o login e a troca de senha no MESMO navegador (no Edge ou no Chrome)."),
                     ("Veja a hospedagem", "Menu Hospedagem > escolha comprenolink.net. Anote a data de renovação e o valor."),
                     ("Veja o domínio", "Menu Domínios > comprenolink.net. Anote a data de vencimento e ative \"Renovação automática\"."),
                     ("Confirme o meio de pagamento", "Em Pagamentos, confirme que o cartão cadastrado está válido e dentro do limite."),
                     ("Avise o Claude", "Escreva as datas e valores. O Claude coloca um lembrete 30 dias antes de cada vencimento na agenda.")],
                    ["Não passe senha nem dados de cartão ao Claude.", "Se a Hostinger pedir código por e-mail ou celular, só você consegue concluir."],
                    "a renovação automática aparece como \"Ativada\" no domínio e na hospedagem, e as datas estão anotadas.")

    # 4
    st += atividade("4", "Criar o e-mail alertas@comprenolink.net (aviso das inscrições)", "Esta semana", LARANJA, LARANJA_C, "Você (cria) + Claude (configura)", "15 minutos",
                    "O formulário de alertas já guarda cada inscrição no painel do WordPress, então nenhum contato se perde. Mas o site ainda não consegue ENVIAR e-mail: "
                    "os avisos de teste não chegaram nem no spam. O Gmail bloqueia o envio em nome dele por um servidor de fora, e o Gmail da compre.no.link26 está "
                    "sem verificação em 2 etapas (por isso não gera senha de app).",
                    "Você passa a receber um aviso a cada nova inscrição, e o site poderá mandar as campanhas (e-mail semanal e o envio diário de 27/11 a 30/11) "
                    "sem cair no spam. O mesmo e-mail também resolve o Outlook que ficou pendente desde 26/10.",
                    [("Entre na Hostinger", "hpanel.hostinger.com (veja a atividade 3 se o login estiver bloqueado)."),
                     ("Abra a área de e-mails", "Escolha o site comprenolink.net > E-mails > Contas de e-mail > Criar conta de e-mail."),
                     ("Crie a conta", "Endereço: alertas@comprenolink.net. Escolha uma senha forte e guarde só para você. NÃO envie a senha ao Claude."),
                     ("Avise o Claude", "Escreva \"criei o e-mail\". O Claude abre o FluentSMTP (já instalado no site), escolhe \"Outro SMTP\" e preenche servidor "
                                        "smtp.hostinger.com, porta 465, usuário alertas@comprenolink.net."),
                     ("Digite a senha no campo", "O Claude para no campo da senha e você mesmo digita. Depois ele envia um e-mail de teste e confere se chegou."),
                     ("Ligue o aviso do formulário", "Com o envio funcionando, o Claude ativa o e-mail de aviso no formulário \"Alertas Black Friday e Natal\".")],
                    ["Se o plano da Hostinger não incluir caixa de e-mail, plano alternativo: no Gmail compre.no.link26, ligar a verificação em 2 etapas "
                     "(precisa do celular) e criar uma senha de app em myaccount.google.com/apppasswords.",
                     "Nunca envie campanha em massa pelo Gmail pessoal: risco de bloqueio da conta. Sempre dar a opção de sair da lista."],
                    "um e-mail de teste do site chega na caixa de entrada e cada inscrição nova gera um aviso.")

    # 5
    st += atividade("5", "Vendas recusadas: CONFERIDO (conta certa; 7 recusas = compra do próprio dono)", "Concluída em 03/11 (falta só conferir os 12 em revisão)", VERDE, VERDE_C,
                    "Claude analisou; você confirmou quem comprou", "5 minutos para a última conferência",
                    "O histórico tem 19 vendas: 12 em revisão (R$ 172,00 de comissão) e 7 recusadas por \"conta vinculada\" (R$ 65,58 de comissão perdida). "
                    "Era preciso saber se o arquivo era da conta certa e por que as 7 foram recusadas.",
                    "O painel passa a dizer a verdade, você sabe que a conta é a do blog, entende a causa das recusas e evita que se repitam, "
                    "protegendo a sua conta de afiliado.",
                    [("Conta do arquivo: CONFERIDA", "A soma das 12 vendas em revisão dá R$ 172,00 de comissão e R$ 793,90 em vendas: é exatamente o total oficial que você digitou do painel do ML em 27/10. "
                                                       "Logo, o CSV é da conta do blog."),
                     ("Causa das 7 recusas: CONFIRMADA por você", "6 compras saíram em 06/10, de 6 lojas diferentes e com pedidos em sequência (um carrinho só), e 1 em 09/10. Você confirmou que foram suas. "
                                                                   "O Mercado Livre não paga comissão quando quem compra é o próprio afiliado ou uma conta vinculada a ele: por isso \"Recusada (conta vinculada)\"."),
                     ("Daqui em diante, não compre pelo link do blog", "Para comprar para você, abra o Mercado Livre direto no aplicativo, sem passar pelo blog nem por links meli.la. "
                                                                         "Ao testar os links do blog, não finalize compra."),
                     ("Confira os 12 em revisão", "No ML Afiliados, veja se alguma das 12 vendas em revisão também foi sua (ou de alguém da sua casa). Se foi, a tendência é virar recusada. "
                                                  "Anote os números dos pedidos e me mande: o Claude marca no painel como \"compra própria\" e tira da previsão de comissão."),
                     ("Avise a família e o sócio", "A regra vale para todos que têm conta vinculada à sua: comprar pelo link do blog não gera comissão e pode atrapalhar a conta.")],
                    ["Compras do próprio afiliado pelos links de afiliado costumam ser proibidas nos termos do programa. Repetir pode colocar a conta em risco; confirme os termos no painel do ML Afiliados.",
                     "A comissão real do blog, até agora, é só o que está \"Em revisão\" e não foi comprado por vocês. A compra de 26/10 (Tampa de micro-ondas, R$ 2,29) foi de um cliente que achou o blog na busca: essa é de verdade.",
                     "O blog não enxerga compras: só o painel do ML Afiliados mostra vendas. Por isso a exportação é toda segunda."],
                    "você conferiu os 12 pedidos em revisão e me mandou quais foram compras suas (se houver).")

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
                     ("Segunda 10:15 – vendas", "Exporte as vendas do ML Afiliados para Relatorios_Diarios_Anuncios\\vendas_afiliados e rode ATUALIZAR_PAINEL.bat."),
                     ("Segunda 10:45 – planilha", "Preencha a linha da semana em Planilha_Semanal_Turbinar.xlsx. Veja o melhor canal na aba Campanhas do painel."),
                     ("Decida UMA coisa", "Canal que mais trouxe cliques ganha o dobro de posts; o que trouxe zero por 2 semanas é trocado.")],
                    ["Roteiro completo: Roteiro_Rotinas_Segunda_e_Sexta.pdf.",
                     "Dados do Google Analytics só aparecem a partir de 06/11 (leva até 48 horas)."],
                    "a planilha tem a linha da semana preenchida e uma decisão anotada.")

    # 7
    datas = tabela(["Data", "O que fazer", "Onde está o material"],
                   [["Todo dia de post", "19:10 Story com link, 19:15 Status do WhatsApp, 19:20 Canal (post e Reels saem sozinhos 19:00 e 19:05)",
                     "Planejamentos\\Andamento\\Divugação_WhastsApp_Instagram\\07_PACOTE_DO_DIA (pasta do dia)"],
                    ["Ter 10/11, 12:00", "Lista da Black Friday nos grupos de WhatsApp que permitem divulgação", "pasta 2026-11-10_ter"],
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
                     ("Dias de lista (12:00)", "Só em grupos onde o administrador permite divulgar: anexe campanha_12h00.png e cole o texto. No máximo 1 mensagem por semana por grupo."),
                     ("Quem comentar BLACK", "O post pede \"Comente BLACK\": o ManyChat responde com o link no Direct. Se algo falhar, peça ao Claude \"texto do Direct de DD/MM\".")],
                    ["Use os textos exatamente como estão em 1_TEXTOS_DO_DIA.txt: sem preço, sem \"mais vendido\" e com o aviso de afiliado.",
                     "Existe uma tarefa agendada diária (19:12) do Claude para o Status e o Canal. Se ela falhar ou o limite de uso do plano do Claude acabar, o plano B é publicar à mão com a pasta do dia.",
                     "O sócio direciona, mas o Claude continua sem digitar senhas, sem burlar captcha e sem aceitar termos: esses passos são sempre de uma pessoa.",
                     "Para o computador agendar, deixe-o ligado e o aplicativo do Claude aberto; o Instagram agenda no Chrome com a conta logada.",
                     "Guia curto para o sócio: Guia_Socio_Como_Pedir_ao_Claude.pdf (mesma pasta, 2 páginas). Mais detalhes: Pendencias_Dono_Passo_a_Passo_2026-10-31.pdf."],
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
    st += atividade("9", "Canal do WhatsApp: link no blog FEITO; faltam Instagram, convites e contagem", "Blog feito em 03/11; o resto é rotina semanal", LARANJA, LARANJA_C, "Você + Claude (link no site)", "30 minutos para montar + 10 minutos por semana",
                    "O Canal já existe e recebe os posts do dia, mas ninguém entra se não souber que ele existe. O WhatsApp é onde o seu público mais responde e o Canal é uma lista sua: "
                    "não depende de algoritmo nem de a pessoa lembrar de abrir o blog.",
                    "Cada oferta chega direto no celular de quem entrou, com o link rastreável (origem whatsapp / canal). Quanto mais seguidores, mais cliques sem gastar nada.",
                    [("Pegue o link do Canal", "WhatsApp Business > Atualizações > seu Canal > Compartilhar link. (O link foi recebido em 31/10; se não achar, peça ao Claude \"link do canal\")."),
                     ("Link no blog: FEITO em 03/11", "O botão \"Entrar no Canal do WhatsApp\" está no Contato, na página inicial, no guia, na Black Friday e no Natal (acima do formulário de alertas), com backup."),
                     ("Coloque no Instagram", "No app: Editar perfil > Links > adicione o convite do Canal (o link 1 continua apontando para a campanha do mês)."),
                     ("Faça um Status de convite por semana", "Uma arte simples \"Entre no Canal e receba os achados do dia\" (o Claude gera). Sem preço e com o aviso de afiliado."),
                     ("Convide pessoas", "10 por semana: família, amigos e clientes, um por um. Não adicione ninguém à força e não faça envio em massa (o WhatsApp bloqueia o número)."),
                     ("Anote toda segunda", "O número de seguidores do Canal na coluna Observações da Planilha_Semanal_Turbinar.xlsx.")],
                    ["Grupos de terceiros: só divulgue onde o administrador permite e no máximo 1 mensagem por semana em cada grupo.",
                     "Nos textos: sem preço, sem \"mais vendido\" e com a frase de link de afiliado."],
                    "o link do Canal está no site, na bio do Instagram e o número de seguidores sobe semana a semana.")

    # 10 Acabamento
    st += atividade("10", "Acabamento do guia: FEITO em 03/11 (\"Não compre se...\", descrição no Google, logotipo)", "Concluída: 17 itens, descrição e logo no ar", VERDE, VERDE_C, "Claude fez (backup de tudo); você só confere", "Concluída",
                    "Faltam três acabamentos do checklist: a linha honesta \"Não compre se...\" nos produtos, a descrição do guia no resultado do Google "
                    "(hoje é o começo do texto, cortado no meio) e o logotipo no topo do site (hoje só aparece o nome).",
                    "\"Não compre se...\" aumenta a confiança (quem avisa o ponto fraco vende mais a longo prazo). A descrição melhor aumenta os cliques vindos do Google. "
                    "O logotipo dá cara de marca e reconhecimento.",
                    [("Peça ao Claude", "Escreva \"fazer o acabamento do guia\"."),
                     ("Defina o escopo", "Com 200 produtos, comece pelo Top 10 da Black Friday e pelos 10 do Natal (20 itens). Os outros entram aos poucos."),
                     ("Aprove os textos", "O Claude mostra as frases \"Não compre se...\" (honestas, sem inventar dados) e a nova descrição do guia. Você aprova ou ajusta."),
                     ("Logotipo", "O Claude coloca o logo (pasta D:\\Projeto_Blog_Comprenolink\\Logo) em Aparência > Personalizar > Identidade do site e confere no celular."),
                     ("Backup e conferência", "O Claude faz backup antes, publica e roda o teste do site.")],
                    ["Os textos seguem a regra: sem preço, sem \"mais vendido\" e sem prometer resultado.",
                     "Mudanças em páginas geradas (categorias e campanhas) vão no categorias.json, não direto no WordPress, senão o gerador desfaz em até 3 horas."],
                    "as páginas mostram o logo, a descrição nova e as linhas \"Não compre se...\" dos itens combinados.")

    # 13
    st += atividade("11", "Uma página nova por semana (fones, TVs, presentes, celulares...)", "Toda semana, a partir de 09/11", AZUL, AZUL_C, "Claude escreve o rascunho; você revisa e dá opinião", "2 horas por página",
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
    st += atividade("12", "Teste de anúncio pago (opcional)", "Só depois de haver vendas aprovadas e verba liberada (hoje: sem verba)", AZUL, AZUL_C, "Você + Claude", "1 hora para montar; R$ 10 a 20 por dia por 7 dias (R$ 70 a 140)",
                    "Com orçamento pequeno dá para descobrir se um produto e um público dão retorno antes de investir mais. Só faz sentido depois de a divulgação gratuita "
                    "ter trazido cliques e de o relatório estar medindo.",
                    "Você sabe quanto custa cada clique e cada venda do anúncio e decide com número, não com palpite.",
                    [("Confirme a verba", "Decidido em 03/11: SEM verba paga por enquanto. Este teste só começa quando você liberar. Regra de ouro: não gaste por mês mais do que a comissão aprovada do mês anterior, exceto este teste."),
                     ("Escolha o que impulsionar", "No Meta Business Suite, o post do Instagram que mais teve cliques orgânicos."),
                     ("Defina o destino", "A página do blog com link rastreável (utm_source=facebook&utm_medium=cpc), nunca direto o link meli.la."),
                     ("Configure", "Público Brasil, 18 a 45 anos, interesses do produto; R$ 10 a 20 por dia por 7 dias."),
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

    # Agenda do Claude
    st += [PageBreak(), faixa("C", "O que o Claude faz (e quando)", "Conferências e tarefas dele, para você saber que estão cobertas", VERDE), Spacer(1, 6),
           P("Estas atividades são do Claude. Você não precisa fazer nada, a não ser responder se ele pedir uma aprovação.", "p"), Spacer(1, 4),
           tabela(["Quando", "O que o Claude faz", "Por quê"],
                  [["06/11 e 09/11", "Conferir se o Google Analytics (Site Kit) já mostra visitantes e se o Bing leu os 2 mapas do site.", "Os dados levam até 48 horas; garante que a medição está ligada."],
                   ["Sexta 06/11", "Rotina de SEO pelo Chrome, se você pedir \"rotina de sexta\".", "Constância no Google."],
                   ["10/11", "Conferir no Search Console se /presentes-de-natal/ foi indexada.", "A página foi antecipada para amadurecer no Google."],
                   ["13/11, 26/11 e 11/12", "Rodar o painel, conferir anúncios e links do guia e só então atualizar a data \"Atualizado em\".", "Não carimbar data sem revisar."],
                   ["A cada 3 horas", "O gerador republica categorias, Black Friday e Natal com backup e cache aquecido.", "Já é automático, sem ação sua."],
                   ["Depois da atividade 4", "Configurar o FluentSMTP, ligar o aviso do formulário e testar.", "Receber aviso por e-mail e poder enviar campanhas."],
                   ["01/12", "Conferir que o menu e a home trocaram para o Natal e que a Black Friday mostra o aviso de fim.", "Troca automática de campanha."],
                   ["Opcional", "Desativar o WPForms (o formulário antigo, sem uso) e corrigir o título H1 duplicado da página inicial.", "Limpeza e leve ganho de velocidade."]],
                  [0.17, 0.5, 0.33], cor=VERDE), Spacer(1, 8),
           bloco("Regras que valem para tudo", [
               "Sem preço, sem \"mais vendido\", \"líder\" ou \"oferta do mês\" e sem promessa de saúde ou estética.",
               "Sempre o aviso de link de afiliado nos textos e nas redes (#publi).",
               "Mudar UMA coisa por semana e olhar o resultado na segunda seguinte.",
               "O Claude nunca digita senhas, não burla captcha e não aceita termos por você: nesses momentos ele para e avisa.",
               "Todo ajuste no site tem backup antes (pasta 2_DADOS\\Blog_WordPress\\backups).",
               "Escreva ao Claude sempre em português e, se travar, mande um print da tela."], VERMELHO, VERMELHO_C)]
    return st


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Pendências abertas (comprenolink.net)", author="comprenolink.net")
    doc.build(conteudo(), onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
