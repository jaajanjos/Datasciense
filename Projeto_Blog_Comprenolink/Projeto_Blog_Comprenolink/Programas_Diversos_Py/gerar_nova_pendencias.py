# -*- coding: utf-8 -*-
"""nova_pendencias.pdf: o que ainda falta executar (dono e Claude), com passo a passo, o porquê e o benefício.
Estado em 11/11/2026 (concluídos saíram; versões anteriores em 0- Pendencias\\1_Pendencias\\old_bkp e o gerador antigo em Programas_Diversos_Py\\old_bkp).
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
base.HOJE = date(2026, 11, 11)
POSICAO = "11/11/2026"
ANUNCIO = "0- Pendencias\\5_Plano_turbinar_anuncio_instagram\\Teste_Antecipado_11a13_11"

DIA_EXEC = {
    "12": "Qua 11/11 (publicar), qui 12 e sex 13/11 no ar; seg 16/11 20:40 avaliação",
    "14": "Convites à mão entre 18:00 e 19:30, até 9 por dia; registro pelo Claude depois do seu aviso",
    "16": "Qua 11/11 (você, 15:35) e qua 11/11 após 20:00 (Claude: capas)",
    "11": "Página de presentes: conferir indexação (atrasado desde 10/11); página nova: toda semana",
    "6": "Sex 13/11 a partir das 20:00 (SEO + guia) e seg 16/11 (números)",
    "7": "Story, Status e Canal: você, pelo celular. Instagram em lote: Claude, toda segunda 20:00",
    "13": "Ter 01/12 (5 min)",
    "15": "Ao longo da semana; cada item tem o seu dia"}


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
            f"comprenolink.net • Instagram @compre.no.link • WhatsApp (11) 99495-9657 • posição de {POSICAO}", "capa_s"), Spacer(1, 8),
          info([("Como usar", "Cada atividade tem: quem faz, quanto tempo leva, POR QUE fazer, o BENEFÍCIO e o passo a passo. Siga a ordem da tabela abaixo: "
                              "as primeiras são as mais urgentes ou as que destravam as outras."),
                ("Foco", "Blog, Instagram, WhatsApp e Mercado Livre. WhatsApp é SÓ POR CATEGORIA (sem produto individual e sem preço). Instagram segue por produto; "
                         "dias novos (a partir de 07/12) só com Reels às 19:05. TikTok foi abandonado em 09/11."),
                ("Quando o Claude trabalha", "Segunda a sexta, sempre a partir das 20:00. Sábado e domingo não há atividade. "
                                             "O Claude faz primeiro tudo o que puder; o que não puder, passa o passo a passo e confere pela tela."),
                ("Cores", "Vermelho = urgente. Laranja = importante nesta semana. Azul = planejado com data. Verde = rotina que se repete."),
                ("Se travar", "Escreva ao Claude com um print da tela. Senha, código de celular, cartão, aceite de termos e o botão Publicar são sempre seus."),
                ("Controle", "ESTE É O ÚNICO ARQUIVO DE PENDÊNCIAS. Toda pendência nova entra aqui e, quando concluída, sai da lista (versões anteriores em 1_Pendencias\\old_bkp). "
                             "Os números das atividades não mudam, porque a agenda aponta para eles.")]),
          Spacer(1, 8), P("Resumo em ordem de execução", "h2"),
          tabela(["#", "Atividade", "Quem", "Dia", "Tempo"],
                 [["12", "Teste de anúncio pago (R$ 50, antecipado para 11 a 13/11)", "Você publica; Claude confere pela tela", "Qua 11/11 → avaliação seg 16/11", "1 h + R$ 50"],
                  ["16", "Ajustes do Instagram de 11/11 (Bem-vindo, post repetido, capas dos Destaques)", "Você + Claude", "Qua 11/11", "15 min seus"],
                  ["14", "Canal do WhatsApp: convites à mão (lote L3) e registro", "Você envia; Claude registra", "Qua 11/11, 18:00–19:30", "20 min"],
                  ["11", "Página de presentes de Natal (indexação) e página nova da semana", "Claude (você revisa)", "Atrasado desde 10/11", "30 min seus"],
                  ["6", "Rotinas: SEO na sexta e números na segunda", "Claude (você aprova)", "Sex 13/11 e seg 16/11, 20:00", "30 a 60 min"],
                  ["7", "Calendário da Black Friday (Story, Status, Canal e Reels)", "Você + Claude", "Até 30/11", "10 min por dia"],
                  ["15", "Pendências herdadas (segurança, vendas, medição, ManyChat, sincronização)", "Você + Claude", "Esta semana", "30 min na semana"],
                  ["13", "Trocar a bio do Instagram para o Natal", "Você (celular)", "Ter 01/12", "5 min"]],
                 [0.05, 0.38, 0.2, 0.2, 0.17], cor=LARANJA), Spacer(1, 4),
          bloco(f"O que saiu da lista desde 04/11 (concluído)", [
              "Troca dos anúncios fora do ar 51, 182, 191 e 196 (09 e 11/11) e 93, 110, 163 e 198 (11/11, no mesmo número); guia com 214 itens e âncoras dos pacotes corrigidas.",
              "Catálogo do WhatsApp: 9 de 9 categorias, conferido em 10/11 (só categorias; os produtos individuais saíram).",
              "Reunião Turbinar (05/11), conta de anúncios Meta criada (cartão e limite R$ 50) e material do anúncio pronto (09/11).",
              "Pendência e anúncio do Colágeno Verisol retirados (09/11). Tudo o que era TikTok foi apagado (09/11).",
              "Post Bem-vindo novo publicado (10/11). 3 posts do feed repetidos apagados e Reels de 3 pacotes adiantados (09 a 12/11).",
              "Renovação automática do domínio comprenolink.eu desligada (09/11); o comprenolink.net segue com renovação automática."], VERDE, VERDE_C), Spacer(1, 8),
          P("Plano por dia (esta semana e as próximas)", "h2"),
          tabela(["Dia", "O que fazer", "Quem"],
                 [["Qua 11/11", "~12:00 publicar o anúncio de teste (passo a passo pronto). 15:35 Instagram: fixar o Bem-vindo novo, apagar o antigo e o post só imagem do Galaxy A17. 18:00–19:30 convites do lote L3. Após 20:00: capas dos Destaques.", "Você + Claude"],
                  ["Qui 12/11", "Após 15:30: usar as capas e criar os Destaques no celular. Ver se os dois computadores sincronizam a pasta de scripts.", "Você"],
                  ["Sex 13/11", "Após 20:00: rotina de SEO com a conferência do guia (painel, anúncios e links). Print dos resultados do anúncio à noite.", "Claude + você"],
                  ["Seg 16/11", "20:00 rotina do Instagram (Reels em lote). 20:40 avaliação do anúncio e semáforo da Black Friday.", "Claude"],
                  ["Sex 20/11", "Subir o limite da conta de anúncios para R$ 155, SÓ se o semáforo ficar verde.", "Você"],
                  ["21 a 27/11", "Anúncio da Black Friday (R$ 105), só com semáforo verde. Dia D 27/11: sem convites; só a rotina do dia.", "Meta + você"],
                  ["Até 30/11", "3 pacotes novos de Reels (09/12, 11/12 e 14/12), um por noite, produtos diferentes dos já usados e do anúncio.", "Claude"],
                  ["Ter 01/12", "Trocar a bio do Instagram para o Natal.", "Você (celular)"]],
                 [0.14, 0.68, 0.18], cor=VERDE), Spacer(1, 4),
          bloco("Conversas do Claude por tema (desde 09/11)", [
              "BLOG- Pendência e ajustes em programas: este arquivo, pendências do blog e programas da pasta D:\\Projeto_Blog_Comprenolink.",
              "BLOG- Ajustes no WhatsApp e Instagram: convites, Canal, Status, catálogo e Instagram.",
              "BLOG- Atividades Claude e Planejamento: agenda, rotinas do Claude e anúncio pago.",
              "BLOG- Day by Day: dúvidas pontuais do dia a dia."], AZUL, AZUL_C),
          PageBreak()]

    # 12 anúncio
    st += atividade("12", "Teste de anúncio pago (antecipado para 11 a 13/11)", "Publicar qua 11/11; avaliação seg 16/11 20:40", VERMELHO, VERMELHO_C,
                    "Você (login, cartão e Publicar) + Claude (material pronto, conferência pela tela e avaliação)", "1 hora para montar; R$ 50 de orçamento TOTAL",
                    "Com orçamento pequeno dá para descobrir se o anúncio traz cliques baratos antes de gastar na Black Friday. A data foi antecipada (era 16 a 18/11) para sobrar tempo de decidir.",
                    "Você decide a Black Friday (R$ 105) com número na mão, não com palpite.",
                    [("Abra o passo a passo", f"{ANUNCIO}\\PASSO_A_PASSO_DONO_11_11.txt. Textos, link com UTM e artes já estão prontos na mesma pasta."),
                     ("Entre no Gerenciador de Anúncios", "adsmanager.facebook.com, conta \"Compre no Link - Anúncios\". Em 10/11 o Chrome do Claude caiu na tela de login: o login é seu."),
                     ("Monte a campanha", "Tráfego; orçamento TOTAL R$ 50; de agora até 13/11 23:59; Brasil 18 a 55; só Instagram Feed e Stories; destino a página de Tecnologia com UTM."),
                     ("Mande o print do resumo", "Antes de publicar. O Claude confere: sem \"Mercado Livre/ML\", sem preço, aviso de afiliado visível."),
                     ("Publique", "O clique em Publicar e a confirmação de pagamento são seus. Avise o sócio da nova data."),
                     ("13/11 à noite", "Print dos resultados (alcance, cliques, custo por clique). Seg 16/11 20:40 o Claude dá o semáforo.")],
                    ["Termos do ML Afiliados (cláusula 4.4) conferidos em 09/11: mídia paga permitida em Instagram/Facebook Ads, sem usar as marcas Mercado Livre, Mercado Pago, Meli ou ML.",
                     "Destino escolhido: página de categoria Tecnologia (o endereço do guia tem \"mercado-livre\" no nome).",
                     "Depois: limite R$ 155 em 20/11 e Black Friday 21 a 27/11 só com semáforo verde; Natal R$ 100 (05 a 14/12) só se a Black Friday se pagar. Total máximo R$ 255."],
                    "o anúncio está aprovado pela Meta e no ar até 13/11, com o print dos resultados guardado.")

    # 16 Instagram 11/11
    st += atividade("16", "Ajustes do Instagram de 11/11", "Qua 11/11", LARANJA, LARANJA_C,
                    "Você (fixar e apagar, no app) + Claude (capas dos Destaques)", "15 minutos seus",
                    "O perfil está com dois \"Bem-vindo\" e um post do Galaxy A17 repetido (imagem + Reels). Perfil limpo passa mais confiança a quem chega pelo anúncio.",
                    "Quem visita o perfil vê uma apresentação só, sem repetição, e os Destaques organizados por categoria.",
                    [("Fixar o Bem-vindo novo", "O que diz \"Produtos selecionados do Mercado Livre\": 3 pontinhos > Fixar no seu perfil."),
                     ("Apagar o Bem-vindo antigo", "O que diz \"Os mais vendidos e bem avaliados\": 3 pontinhos > Eliminar."),
                     ("Apagar o post só imagem do Galaxy A17", "O que tem \"Link na bio - Comente BLACK\". O Reels do A17 (com símbolo de vídeo) FICA."),
                     ("Capas dos Destaques (Claude, após 20:00)", "Pasta nova DESTAQUES_CAPAS: 9 categorias + Black Friday + Natal + Como funciona."),
                     ("Criar os Destaques (você, qui 12/11 após 15:30)", "No celular, com as capas da pasta.")],
                    ["Passo a passo detalhado: 0- Pendencias\\1_Pendencias\\PASSO_A_PASSO_DONO_11_11_15h35.txt.",
                     "Assunto da conversa BLOG- Ajustes no WhatsApp e Instagram."],
                    "um Bem-vindo fixado, o Reels do A17 mantido e os Destaques criados.")

    # 14 Canal do WhatsApp
    st += atividade("14", "Canal do WhatsApp: convites à mão (sem automação)", "Lote L3 em 11/11", LARANJA, LARANJA_C,
                    "Você (envia à mão) + Claude (prepara a lista e registra)", "20 minutos no dia do lote",
                    "O Canal só cresce se mais gente souber dele. A automação foi cancelada em 04/11 por risco de bloqueio do número; o caminho é convite pessoal à mão.",
                    "Canal crescendo sem arriscar o WhatsApp do blog.",
                    [("Pegue o lote L3", "Planejamentos\\Andamento\\Base_Contatos_WhatsApp\\LOTE_L3_10-11_mensagens.txt (mensagens prontas)."),
                     ("Envie à mão", "Entre 18:00 e 19:30, um contato por vez, 3 minutos ou mais entre eles, conferindo nome e foto. Lur (C331) e Mercia (C383) não têm WhatsApp: pule."),
                     ("Avise o Claude", "Escreva \"L3 feito\" e quantos enviou. O Claude registra na aba Envios (cópia em old_bkp antes)."),
                     ("Novos contatos", "Depois do L3 a fila de aprovados acaba. Para continuar, marque como Conhecido na aba Base só quem você conhece de verdade.")],
                    ["Limite: 9 por dia, horário das 09:00 às 20:00. Ao primeiro aviso do WhatsApp, pare por 7 dias e avise o Claude.",
                     "Sem convites em 27/11 (Black Friday). Canal com 10 seguidores em 10/11.",
                     "Lotes já registrados: L0 (04/11), L1 (06/11) e L2 (09/11)."],
                    "o L3 está registrado e não houve aviso do WhatsApp.")

    # 11 páginas
    st += atividade("11", "Página de presentes de Natal e uma página nova por semana", "Atrasado desde 10/11", LARANJA, LARANJA_C,
                    "Claude (confere, escreve e publica com backup); você revisa", "30 minutos seus por semana",
                    "Quem pesquisa no Google digita \"fone bluetooth bom\", não \"21 produtos\". Páginas específicas aparecem melhor; e página não indexada não aparece.",
                    "Cada página nova é mais uma porta de entrada no Google que trabalha por meses.",
                    [("Conferir a indexação de /presentes-de-natal/", "Search Console > Inspeção de URL (Chrome lilás, conta compre.no.link26). Se não estiver indexada, Solicitar indexação."),
                     ("Revisar a página nova da semana", "Você lê e acrescenta opinião; tire qualquer preço ou promessa."),
                     ("Próximo tema", "Ordem sugerida: fones Bluetooth; Smart TV 32\"; celulares; \"JBL Tune vale a pena?\"; QCY x JBL."),
                     ("Publicar", "O Claude publica com backup, liga a página ao guia e pede indexação.")],
                    ["Cada página precisa de links UTM próprios.", "Não mude o endereço de página já indexada sem redirecionamento 301."],
                    "a página de Natal está indexada e há 1 página nova publicada por semana.")

    # 6 rotinas
    st += atividade("6", "Rotinas: SEO na sexta e números na segunda", "Sex 13/11 e seg 16/11, a partir das 20:00", AZUL, AZUL_C,
                    "Claude (executa); você aprova as mudanças", "30 a 60 minutos do Claude",
                    "O Google leva de 4 a 12 semanas para dar posição boa; quem cuida do site toda semana ganha. Sem olhar os números, continua-se fazendo o que não funciona.",
                    "Sexta: mais pesquisas mostram suas páginas. Segunda: você sabe qual canal traz cliques.",
                    [("Sexta – Search Console", "Pesquisas com muitas impressões e poucos cliques: melhorar título e descrição (All in One SEO), sem preço e sem \"mais vendido\"."),
                     ("Sexta – conferência do guia", "Rodar o painel (0_executar_tudo.py --sem-claude), conferir anúncios e links do guia e só então atualizar \"Atualizado em\"."),
                     ("Segunda – vendas", "Prints da tabela de Vendas do ML Afiliados (sem botão de exportar). O Claude atualiza o arquivo de vendas (Anexo A)."),
                     ("Decida UMA coisa", "O canal que mais trouxe cliques ganha mais posts; o que trouxe zero por 2 semanas é trocado.")],
                    ["Roteiro completo: Roteiro_Rotinas_Segunda_e_Sexta.pdf (atualizado em 11/11)."],
                    "a planilha tem a linha da semana preenchida e uma decisão anotada.")

    # 7 calendário
    st += atividade("7", "Calendário de divulgação da Black Friday", "Até 30/11 (a Black Friday é 27/11)", AZUL, AZUL_C,
                    "Você (Story, Status e Canal pelo celular) + Claude (Reels em lote toda segunda 20:00)", "10 minutos por dia",
                    "A Black Friday é a época em que mais se compra; quem aparece com constância colhe o resultado.",
                    "Cada envio com link rastreável mostra, na segunda seguinte, qual dia e produto trouxe visitas.",
                    [("Todo dia de post", "19:10 Story com link, 19:15 Status, 19:20 Canal (só por categoria). Material na pasta do dia em 07_PACOTE_DO_DIA."),
                     ("Instagram", "Os posts e Reels já agendados saem sozinhos. Dias novos (a partir de 07/12) recebem só o Reels das 19:05."),
                     ("26/11 20:00 e 27/11", "Lembrete forte na véspera; no dia D, disparos às 08:00, 12:00 e 19:00."),
                     ("30/11", "Cyber Monday: último dia da campanha. Em 01/12 a página de Natal assume o menu e a home sozinha.")],
                    ["Textos exatamente como em 1_TEXTOS_DO_DIA.txt: sem preço, sem \"mais vendido\"/\"líder\" e com o aviso de afiliado.",
                     "A rotina do Claude é só segunda 20:00 (modo econômico); a publicação diária é sua, pelo celular."],
                    "todos os dias do calendário foram publicados e as visitas aparecem no relatório por origem.")

    # 15 herdadas
    st += atividade("15", "Pendências herdadas (atualizado em 11/11)", "Esta semana", AZUL, AZUL_C,
                    "Você (decidir, trocar senha) + Claude (conferir e executar o que você aprovar)", "30 minutos na semana, em partes de 5 a 10 minutos",
                    "São itens de outras conversas que continuam abertos; ficam aqui para nada se perder.",
                    "Segurança em dia, vendas e medição conferidas e dezembro sem surpresa.",
                    [("ManyChat (qua 11/11)", "Confirmar com outra conta o teste da palavra BLACK e a resposta automática no Direct. Se já fez, avise para dar baixa."),
                     ("Sincronização (qui 12/11)", "Ver se os dois computadores sincronizam a pasta de scripts (um arquivo voltou à versão antiga em 31/10) e dizer a direção."),
                     ("Segurança do pacote do outro PC", "Se o 4_PACOTE_OUTRO_PC.zip (29/10) saiu deste PC, apague a cópia e troque a senha de aplicativo \"Painel Blog\". O Claude nunca digita senha."),
                     ("Vendas do ML Afiliados", "Mandar prints novos (o último lote é de 31/10) e conferir se algum \"em revisão\" foi compra própria."),
                     ("Medição", "Conferir se já entram visitas rastreadas de Instagram, WhatsApp e ManyChat; o anúncio usa utm_campaign=teste_11a13_11.")],
                    ["Nada que apaga, troca senha ou mexe no site é feito sem a sua palavra."],
                    "as vendas foram conferidas, a senha trocada (se for o caso) e a sincronização confirmada.")

    # 13 bio
    st += atividade("13", "Trocar a bio do Instagram para o Natal", "01/12", AZUL, AZUL_C, "Você (celular)", "5 minutos",
                    "A bio fala de Black Friday e o link 1 aponta para /black-friday. A campanha acaba em 30/11.",
                    "Quem entrar no perfil em dezembro cai direto na página de presentes, que já está pronta.",
                    [("Abra o app do Instagram", "Perfil @compre.no.link > Editar perfil."),
                     ("Troque o link 1", "Vira comprenolink.net/presentes-de-natal."),
                     ("Troque a bio", "Peça ao Claude \"bio de Natal\": versão sem preço."),
                     ("Confira", "Abra o link pelo celular e veja se a página de Natal carrega.")],
                    ["Links da bio só se editam no app do celular. Em 26/12 o link 1 volta para comprenolink.net."],
                    "o link da bio abre a página de Natal.")

    # Agenda do Claude
    st += [PageBreak(), faixa("C", "O que o Claude faz (e quando)", "Sempre de segunda a sexta, a partir das 20:00", VERDE), Spacer(1, 6),
           P("Estas atividades são do Claude. Você só responde se ele pedir uma aprovação.", "p"), Spacer(1, 4),
           tabela(["Quando", "O que o Claude faz", "Por quê"],
                  [["Toda segunda, 20:00", "Agendar no Instagram, em lote, o Reels (19:05) de todos os dias cuja janela de 29 dias já abriu, conferindo o calendário antes.", "O Instagram só aceita 29 dias à frente; modo econômico."],
                   ["Qua 11/11, após 20:00", "Capas dos Destaques (pasta DESTAQUES_CAPAS).", "Você cria os Destaques em 12/11."],
                   ["Sex 13/11, após 20:00", "Rotina de SEO e conferência do guia (painel, anúncios e links).", "Constância no Google e guia sem link quebrado."],
                   ["Seg 16/11, 20:40", "Avaliar o teste do anúncio e dar o semáforo da Black Friday (tarefa agendada).", "Decidir com número."],
                   ["Até 30/11", "3 pacotes novos de Reels (09/12, 11/12, 14/12), um por noite.", "Dezembro sem buraco no calendário."],
                   ["Depois do seu aviso", "Registrar os convites do WhatsApp na aba Envios.", "A planilha só vale se for registrada."],
                   ["A cada 3 horas", "O gerador republica categorias, Black Friday e Natal com backup.", "Já é automático."],
                   ["01/12", "Conferir que o menu e a home trocaram para o Natal.", "Troca automática de campanha."],
                   ["03/10/2027", "Lembrar de desligar a renovação do e-mail grátis (teste de 12 meses) ou mantê-lo.", "Evitar cobrança depois do teste."]],
                  [0.2, 0.5, 0.3], cor=VERDE), Spacer(1, 8),
           bloco("Regras que valem para tudo", [
               "Sem preço, sem \"mais vendido\", \"líder\", \"melhor\" ou \"garantido\" e sem promessa de saúde ou estética.",
               "Sempre o aviso de link de afiliado nos textos e nas redes (#publi).",
               "Antes de mexer em qualquer arquivo: cópia em old_bkp (nome_DD-MM-AAAA-HHhMM). Nada muda de lugar sem o seu \"de acordo\".",
               "O Claude informa o uso estimado (BAIXO, MÉDIO ou ALTO) antes de cada atividade.",
               "O Claude nunca digita senhas, não burla captcha e não aceita termos por você. Se travar, passa o passo a passo e confere pela tela.",
               "Se der problema que o Claude consiga resolver, ele corrige e conclui no mesmo dia, sem replanejar."], VERMELHO, VERMELHO_C)]

    st += [PageBreak(), faixa("A", "Anexo A: processo semanal de vendas (ML Afiliados)", "Toda segunda • 15 minutos", LARANJA), Spacer(1, 6),
           info([("Por que existe", "O blog não enxerga compras: só o painel do ML Afiliados mostra as vendas, e a conta não tem botão de exportar. O caminho é por prints."),
                 ("Benefício", "O painel passa a mostrar vendas reais por produto e por origem.")]), Spacer(1, 6),
           passos([("Entre na conta certa", "mercadolivre.com.br/afiliados/dashboard: a que criou os links do blog."),
                   ("Escolha o período", "Métricas > Período > Últimos 180 dias."),
                   ("Abra Vendas e marque os 4 status", "Aprovada, Em revisão, Recusada e Cancelada."),
                   ("Tire os prints", "A tabela inteira, todas as páginas."),
                   ("Mande ao Claude", "Ele atualiza vendas_ml_AAAA-MM-DD.csv em Relatorios_Diarios_Anuncios\\vendas_afiliados."),
                   ("Rode o painel", "Feche o Excel e rode Relatorios_Diarios_Anuncios\\ATUALIZAR_PAINEL.bat. Erro: print ao Claude.")], LARANJA),
           Spacer(1, 6),
           bloco("Catálogo do WhatsApp", [
               "Só por categoria: 9 de 9 cadastradas e conferidas em 10/11. Produto individual não entra.",
               "Categoria nova no blog: cadastrar com foto e texto prontos (06_CATALOGO_WHATSAPP\\CATEGORIAS)."], AZUL, AZUL_C),
           Spacer(1, 12),
           faixa("B", "Anexo B: outras pendências com ou sem data", "Nada foi perdido ao juntar tudo em um arquivo", AZUL), Spacer(1, 6),
           tabela(["Quando", "Pendência", "Quem", "Observação"],
                  [["Sem data", "Outlook com compre.no.link26@gmail.com", "Você + Claude", "Adiado: depende da verificação em 2 etapas."],
                   ["Sem data", "Desativar o WPForms (sem uso) e corrigir o título H1 duplicado da página inicial", "Claude, com seu OK", "Limpeza e leve ganho de velocidade."],
                   ["Depois da BF", "Reavaliar Telegram, Pinterest e YouTube", "Você", "Fora do foco até a Black Friday passar."],
                   ["Sem data", "Atualizar o Relatório Mestre e o Mapa Operacional de 07/11 (citam a rotina das 19:12 e D:\\mercado_livre)", "Claude, quando você pedir", "Estão desatualizados."],
                   ["26/12 (sáb)", "Instagram: o link 1 da bio volta para comprenolink.net", "Você (celular)", "Depois do Natal."]],
                  [0.12, 0.4, 0.16, 0.32], cor=AZUL), Spacer(1, 8),
           bloco("Sobre esta versão", [
               f"Posição de {POSICAO}. Os anexos de diagnóstico de 04/11 (G, H e I: crescimento, \"estamos aplicando?\" e % de adequação) saíram desta versão porque descreviam a situação daquele dia; continuam na versão anterior em 1_Pendencias\\old_bkp.",
               "Este é o único arquivo de pendências. Os geradores ficam em Programas_Diversos_Py."], VERDE, VERDE_C)]
    return st


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Pendências abertas (comprenolink.net)", author="comprenolink.net")
    doc.build(conteudo(), onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
