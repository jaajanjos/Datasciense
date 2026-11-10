# -*- coding: utf-8 -*-
"""PDF "Pendencias_WhatsApp": passo a passo do que o dono precisa fechar no WhatsApp Business (e a exportação de vendas).
Rodar:  python -X utf8 gerar_pendencias_whatsapp.py
Saída:  D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Pendencias_WhatsApp.pdf
Usa os componentes visuais de gerar_pendencias_detalhado.py (mesma pasta). Caminhos com barra normal.
"""
import os
import sys
from datetime import date, timedelta

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gerar_pendencias_detalhado as base  # noqa: E402
from gerar_pendencias_detalhado import (AZUL, AZUL_C, LARANJA, LARANJA_C, P, VERDE, VERDE_C, VERMELHO, VERMELHO_C,  # noqa: E402
                                        bloco, caixa_texto, faixa, info, passos, tabela)
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer  # noqa: E402

SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Pendencias_WhatsApp.pdf"
base.HOJE = date(2026, 11, 1)

MODA = ("NOME:\n(emoji de camiseta) Moda Infantil & Juvenil\n\nDESCRIÇÃO:\n"
        "Conjuntos, moletons e kits para meninas e meninos. Confira todas as opções da categoria com o valor do dia no Mercado Livre "
        "pelo link. Link de afiliado: posso ganhar comissão, sem custo extra para você.\n\nLINK:\n"
        "https://comprenolink.net/moda-infantil-e-juvenil/?utm_source=whatsapp&utm_medium=catalogo&utm_campaign=categoria&utm_content=cat_moda-infantil-e-juvenil\n\n"
        "CÓDIGO DO ITEM: CAT-moda-infantil-e-juvenil\nFOTO: CAT-moda-infantil-e-juvenil.jpg\nPREÇO: deixar em branco")


def conteudo():
    st = [Spacer(1, 0.4 * cm), P("PENDÊNCIAS DO WHATSAPP", "capa_t"), Spacer(1, 4),
          P("Passo a passo do WhatsApp Business e das vendas<br/>ATUALIZADO em 01/11/2026: o que foi concluído, o que falta e a rotina semanal", "capa_s"),
          Spacer(1, 8),
          info([("Tempo estimado", "20 a 30 minutos, no celular do número (11) 99495-9657."),
                ("Tenha em mãos", "O celular com internet, o WhatsApp Business aberto e, para a parte 2, a foto <b>CAT-moda-infantil-e-juvenil.jpg</b> "
                                  "(onde achar: veja a parte 1)."),
                ("Fonte dos arquivos", "D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Celular_Whatsapp (06_CATALOGO_WHATSAPP\\CATEGORIAS)."),
                ("Situação em 01/11", "As partes 2 a 5 abaixo foram concluídas em 31/10. A parte 1 está PARCIAL: o Claude conferiu o WhatsApp Web em 01/11 e só 2 das 9 categorias estão no catálogo. "
                                      "Elas ficam aqui como consulta. A parte 6 traz a rotina semanal e o calendário de execução.")]),
          Spacer(1, 8), P("O que o relatório técnico já confirma como FEITO", "h2"),
          tabela(["Item", "Situação"],
                 [["WhatsApp Business no número, perfil comercial, saudação, ausência, etiquetas", "Feito"],
                  ["Catálogo por produto: 17 itens", "Feito"],
                  ["Catálogo por categoria: 8 itens (Bebê & Maternidade estava em análise)", "Feito. Conferir a aprovação"],
                  ["Canal \"Compre no Link – Achados do Mercado Livre\"", "Feito (um duplicado foi removido)"],
                  ["7 respostas rápidas: /bf /natal /link /preco /pedido /canal /obrigado", "Feito"]],
                 [0.78, 0.22], cor=VERDE), Spacer(1, 6),
          P("Situação das 5 pendências (atualizado em 01/11/2026)", "h2"),
          tabela(["Nº", "Pendência", "Situação"],
                 [["1", "Conferir o catálogo: Bebê aprovado? Moda Infantil existe?", "PARCIAL. Conferido no WhatsApp Web em 01/11: o catálogo tem 17 produtos e só 2 categorias (Moda Infantil e Bebê). Faltam 7 categorias"],
                  ["2", "Cadastrar o item Moda Infantil & Juvenil, se faltar", "CONCLUÍDO. A Moda Infantil & Juvenil está no catálogo"],
                  ["3", "Copiar o link do Canal que já existe (NÃO criar outro)", "CONCLUÍDO em 31/10. Link recebido às 17:04 e registrado"],
                  ["4", "Colar o link na resposta rápida /canal e avisar o Claude", "CONCLUÍDO em 31/10, segundo o dono"],
                  ["5", "Exportar as vendas do ML Afiliados (conta do blog)", "CONCLUÍDO em 31/10. 19 vendas, comissão pendente R$ 172,00 (vendas_ml_2026-10-31.csv)"]],
                 [0.06, 0.5, 0.44], cor=VERDE), Spacer(1, 6),
          P("Ainda em aberto (validação do Claude em 01/11). Já feito em 01/11: planilha das categorias marcada \"Cadastrado = S\" e painel atualizado (19 vendas, 0 fórmulas com erro).", "h2"),
          tabela(["Pendência", "O que fazer"],
                 [["Cadastrar 7 categorias no catálogo", "Faltam: Tecnologia, Áudio & TV, Casa & Eletrodomésticos, Casa Cama & Decoração, Ferramentas, Esporte & Fitness e Beleza & Saúde. "
                                                         "Textos prontos em CATALOGO_CATEGORIAS_TEXTOS.txt. O campo Link do WhatsApp aceita só 75 caracteres: use o link curto, por exemplo https://comprenolink.net/audio-e-tv/."],
                  ["Apagar o CNL-111 (Kit Skincare)", "Produto que saiu do Mercado Livre. WhatsApp Business → Catálogo → item → Excluir. Eu não apago itens: não tem volta."],
                  ["Links do catálogo por produto", "FEITO em 01/11: os 16 links foram trocados por links curtos com o número certo (o campo cortava os antigos em 75 caracteres)."],
                  ["Bebê & Maternidade", "Está no catálogo. Conferir se saiu de \"em análise\" (mais de 24 h pode ser recusa silenciosa)."]],
                 [0.3, 0.7], cor=LARANJA), Spacer(1, 6),
          bloco("Regras de ouro (sempre, em todo texto do WhatsApp)", [
              "Sem preço e sem \"menor/melhor preço\": use \"confira o valor do dia no Mercado Livre\".",
              "Sem promessa de saúde ou estética.",
              "Sempre o aviso de link de afiliado (já está nos textos prontos).",
              "Nada de aplicativos de envio em massa e não adicione pessoas em grupos sem pedir: o WhatsApp bloqueia o número."],
                VERMELHO, VERMELHO_C)]

    # ---------------- Parte 1
    st += [PageBreak(), faixa("1", "Conferir o catálogo e levar a foto para o celular", "Primeiro passo • PARCIAL: faltam 7 categorias no catálogo • 3 a 5 minutos", AZUL),
           Spacer(1, 6),
           P("A) Conferir o que já existe no catálogo", "h2"),
           passos([
               ("Abra o WhatsApp Business", "Ícone verde com a letra B."),
               ("Entre no catálogo", "Android: três pontinhos → <b>Ferramentas comerciais</b> → <b>Catálogo</b>. iPhone: <b>Configurações</b> → Ferramentas comerciais → Catálogo."),
               ("Conte os itens de categoria", "Devem existir 8 itens com nome de categoria: Tecnologia & Informática, Áudio & TV, Casa & Eletrodomésticos, Bebê & Maternidade, "
                "Casa Cama & Decoração, Ferramentas & Utilidades, Esporte & Fitness e Beleza & Saúde."),
               ("Procure Moda Infantil & Juvenil", "Se aparecer, <b>pule a parte 2</b>. Se não aparecer, faça a parte 2."),
               ("Veja o Bebê & Maternidade", "Se ainda estiver \"em análise\", aguarde (até 24 h). Se foi recusado, apague o item e me avise."),
               ("Anote", "Quantos itens de categoria existem e se a Moda Infantil estava lá. Você vai me contar na parte 4.")], AZUL),
           Spacer(1, 6),
           P("B) Levar a foto da Moda Infantil para o celular (só se for cadastrar)", "h2"),
           P("A pasta <b>Divulgacao_Blog</b> do OneDrive não existe mais, então use um destes jeitos, o que for mais fácil para você:"),
           passos([
               ("Opção 1: WhatsApp Web (mais rápido)", "No computador, abra web.whatsapp.com com o número do blog, abra a conversa com você mesmo (\"Você\"), anexe "
                "<b>D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Celular_Whatsapp\\06_CATALOGO_WHATSAPP\\CATEGORIAS\\fotos\\CAT-moda-infantil-e-juvenil.jpg</b> e envie. "
                "No celular, abra a imagem e salve na galeria."),
               ("Opção 2: e-mail ou cabo", "Mande a foto para o seu e-mail e baixe no celular, ou copie por cabo USB."),
               ("Opção 3: pedir ao Claude", "Se você me disser uma pasta do OneDrive que o celular já enxerga, eu copio a foto e os textos para lá (peço antes de criar pasta nova).")], AZUL)]

    # ---------------- Parte 2
    st += [PageBreak(), faixa("2", "Cadastrar o item Moda Infantil & Juvenil (só se faltar)", "Segundo passo • CONCLUÍDO (a Moda Infantil já está no catálogo) • 6 minutos", VERDE), Spacer(1, 6),
           passos([
               ("Abra o catálogo e toque em +", "Ferramentas comerciais → Catálogo → botão <b>+</b> (Adicionar novo item)."),
               ("Foto", "Toque em <b>Adicionar imagens</b> → Galeria → escolha <b>CAT-moda-infantil-e-juvenil</b>."),
               ("Nome do item", "Digite o emoji de camiseta e o nome do quadro abaixo."),
               ("Preço", "<b>Deixe em branco.</b> O valor muda no Mercado Livre e o blog não anuncia preço."),
               ("Descrição", "Copie do quadro abaixo. O texto já tem o aviso de link de afiliado e cabe no limite de 300 caracteres."),
               ("Mais campos", "Toque em <b>Mais campos</b> (ou Adicionar detalhes). Em <b>Link</b>, cole o link do quadro. Em <b>Código do item</b>, escreva <b>CAT-moda-infantil-e-juvenil</b>."),
               ("Salve", "Toque em <b>Salvar</b>. O item fica \"em análise\" por até 24 horas, o que é normal.")], VERDE),
           Spacer(1, 6), caixa_texto("Textos do item (copie do arquivo CATALOGO_CATEGORIAS_TEXTOS.txt ou deste quadro)", MODA), Spacer(1, 6),
           bloco("Como saber que deu certo", ["O catálogo passa a mostrar 9 itens de categoria, com a Moda Infantil em análise ou aprovada."], VERDE, VERDE_C),
           Spacer(1, 6),
           bloco("Se o WhatsApp recusar o item", [
               "Não insista: apague o item e me avise. Produtos de roupa infantil às vezes passam por revisão manual.",
               "Se a descrição der erro de tamanho, apague a última frase e deixe só: \"Conjuntos, moletons e kits para meninas e meninos. Confira as opções pelo link.\" "
               "(mantenha o aviso de afiliado no link da página)."], LARANJA, LARANJA_C)]

    # ---------------- Parte 3 e 4
    st += [PageBreak(), faixa("3", "Copiar o link do Canal que já existe", "Terceiro passo • CONCLUÍDO em 31/10 • NÃO criar outro canal", VERMELHO), Spacer(1, 6),
           bloco("Atenção", ["O relatório mostra que um canal duplicado já foi criado e removido uma vez. Não crie outro: copie o link do que já existe."],
                 VERMELHO, VERMELHO_C), Spacer(1, 6),
           passos([
               ("Abra a aba Atualizações", "Embaixo (iPhone) ou no alto (Android)."),
               ("Abra o canal", "Procure <b>Compre no Link – Achados do Mercado Livre</b> na lista \"Canais\". Se houver dois canais com esse nome, avise antes de seguir."),
               ("Toque no nome do canal", "No alto da tela do canal."),
               ("Compartilhar → Copiar link", "O link tem a forma <b>whatsapp.com/channel/...</b>. Ele fica copiado na área de transferência."),
               ("Confira o canal", "Foto com o logotipo, nome certo e descrição \"Achados do Mercado Livre selecionados pelo blog comprenolink.net...\".")], VERMELHO),
           Spacer(1, 10),
           faixa("4", "Colar o link na resposta rápida /canal e avisar o Claude", "Quarto passo • CONCLUÍDO em 31/10 • 5 minutos", AZUL), Spacer(1, 6),
           passos([
               ("Abra as respostas rápidas", "Ferramentas comerciais → <b>Respostas rápidas</b>."),
               ("Abra a /canal", "Toque no atalho <b>/canal</b> para editar."),
               ("Troque o trecho do link", "O texto é: \"📣 Siga o meu canal de achados no WhatsApp (sem grupo, sem conversa): [COLE AQUI O LINK DO CANAL]\". "
                "Apague <b>[COLE AQUI O LINK DO CANAL]</b> e cole o link copiado."),
               ("Salve", "Toque em <b>Salvar</b>."),
               ("Teste", "Em qualquer conversa (pode ser a de \"Você\"), digite <b>/</b> e escolha <b>canal</b>. O texto com o link deve aparecer pronto.")], AZUL),
           Spacer(1, 6),
           caixa_texto("Mensagem pronta para me enviar depois (troque o que for diferente)",
                       "WhatsApp: catálogo com ___ itens de categoria; Moda Infantil: [já existia / cadastrei hoje]; Bebê: [aprovado / em análise].\n"
                       "Link do Canal: [cole aqui]\n/canal atualizada: sim")]

    # ---------------- Parte 5
    st += [PageBreak(), faixa("5", "Exportar as vendas do ML Afiliados", "Quinto passo • CONCLUÍDO em 31/10 • 10 minutos • no computador, Chrome", LARANJA), Spacer(1, 6),
           bloco("Como ficou resolvido (01/11)", [
               "A conta certa é a que mostra ganho estimado perto de R$ 172 nos últimos 180 dias. Em 30/10 o Chrome estava na conta pessoal (R$ 15,27).",
               "Nessa conta do blog não existe botão de exportar. Em 31/10 você tirou prints da tabela de Vendas e o CSV foi montado a partir deles: "
               "19 vendas (12 pendentes e 7 recusadas por conta vinculada).",
               "O painel já usa esse CSV. Daqui para frente, repita toda segunda-feira (parte 6)."], VERDE, VERDE_C), Spacer(1, 6),
           passos([
               ("Entre na conta certa", "No Chrome, abra mercadolivre.com.br/afiliados/dashboard. Clique no nome no alto, à direita. Se não for a conta do blog, saia e entre com ela."),
               ("Escolha o período", "Em <b>Métricas → Período</b>, escolha <b>Últimos 180 dias</b>."),
               ("Procure o botão de baixar", "Nessa conta ele não existe (confirmado em 31/10). Use os prints do passo abaixo."),
               ("Tire prints da tabela Vendas", "Em Vendas, abra o filtro Status e marque as 4 opções (Aprovada, Em revisão, Recusada, Cancelada). Print de cada página da tabela, sem pular nenhuma. "
                "Mande ao Claude, que monta o CSV no formato que o painel lê."),
               ("O CSV fica na pasta certa", "<b>D:\\Projeto_Blog_Comprenolink\\Relatorios_Diarios_Anuncios\\vendas_afiliados</b>. Nome: vendas_ml_AAAA-MM-DD.csv. Confira se o número de linhas bate com o de resultados da tela."),
               ("Rode o painel", "Feche o Excel. O Claude roda o <b>Relatorios_Diarios_Anuncios\\ATUALIZAR_PAINEL.bat</b> (ou você dá dois cliques). O log fica em log_painel.txt.")], LARANJA)]

    # ---------------- Fim
    st += [Spacer(1, 10), P("Lista de conferência (atualizada em 01/11/2026)", "h2"),
           tabela(["OK", "Tarefa", "Feito em"],
                  [["[ X ]", "1. Conferi o catálogo (itens de categoria e status do Bebê)", "31/10 (faltam 7 categorias: conferido em 01/11)"],
                   ["[ X ]", "2. Cadastrei a Moda Infantil & Juvenil (ou ela já existia)", "31/10"],
                   ["[ X ]", "3. Copiei o link do canal já existente (sem criar outro)", "31/10 17:04"],
                   ["[ X ]", "4. Atualizei a resposta rápida /canal e mandei o link ao Claude", "31/10"],
                   ["[ X ]", "5. Exportei as vendas da conta do blog para vendas_afiliados", "31/10 (CSV de prints)"]],
                  [0.08, 0.62, 0.3], cor=VERDE), Spacer(1, 6)]

    # ---------------- Parte 6: rotina semanal
    segundas = [date(2026, 11, 2) + timedelta(weeks=i) for i in range(9)]
    st += [PageBreak(), faixa("6", "Rotina semanal e calendário de execução", "Toda segunda-feira • primeira rodada completa em 09/11", AZUL), Spacer(1, 6),
           P("O que se repete toda semana (detalhes no PROCESSO_SEMANAL_VENDAS_WHATSAPP.pdf):", "p"),
           tabela(["Hora", "Quem", "Etapa"],
                  [["10:00", "Você + Claude", "Blog: se cadastrou ou retirou anúncios, pedir \"gerar as categorias\""],
                   ["10:15", "Você", "ML Afiliados: prints da tabela de Vendas (as 4 situações) e envio ao Claude"],
                   ["10:45", "Claude (você fecha o Excel)", "CSV em vendas_afiliados e ATUALIZAR_PAINEL.bat"],
                   ["11:15", "Você", "Conferir o PDF novo do painel: vendas, comissão pendente, conversão, anúncios fora do ar"],
                   ["11:30", "Você + Claude", "Catálogo do WhatsApp: categoria nova? item \"em análise\" há mais de 24 h? Numeração e links ainda certos?"]],
                  [0.1, 0.25, 0.65], cor=AZUL), Spacer(1, 6),
           P("Datas das próximas rodadas", "h2"),
           tabela(["Segunda", "Situação"],
                  [[f"{s:%d/%m}", "Rodada 0 (opcional): vendas atualizadas em 31/10" if i == 0 else "PRIMEIRA RODADA COMPLETA" if i == 1 else "Rodada normal"]
                   for i, s in enumerate(segundas)], [0.2, 0.8], cor=AZUL), Spacer(1, 6),
           bloco("Arquivos de agenda e de validação", [
               "Calendario_Execucao_Semanal_WhatsApp_Vendas.ics (esta pasta): 45 eventos, 02/11 a 28/12, com aviso 15 minutos antes.",
               "Validacao_WhatsApp_Vendas_Calendario_2026-11-01.pdf (esta pasta): o que foi validado, o que ainda falta e a tabela de links do catálogo por produto.",
               "Se algo travar, tire um print e mande ao Claude."], VERDE, VERDE_C)]
    return st


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Pendências do WhatsApp (comprenolink.net)", author="comprenolink.net")
    doc.build(conteudo(), onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
