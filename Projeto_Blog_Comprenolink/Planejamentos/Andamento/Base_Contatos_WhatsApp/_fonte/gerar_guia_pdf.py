# -*- coding: utf-8 -*-
"""Gera guia_utilização_gerador_excel.pdf: passo a passo de cada recurso criado em 04/11/2026."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

pdfmetrics.registerFont(TTFont("Ar", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("ArB", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Co", "C:/Windows/Fonts/consola.ttf"))
pdfmetrics.registerFontFamily("Ar", normal="Ar", bold="ArB", italic="Ar", boldItalic="ArB")

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
SAIDA = PASTA + "/guia_utilização_gerador_excel.pdf"
VERDE = colors.HexColor("#0B3D2E"); VERDE_C = colors.HexColor("#E8F5EE")
VERM = colors.HexColor("#9C0006"); VERM_C = colors.HexColor("#FFC7CE")
LAR = colors.HexColor("#B45F06"); LAR_C = colors.HexColor("#FFF4C2")
h1 = ParagraphStyle("h1", fontName="ArB", fontSize=17, textColor=VERDE, spaceAfter=4, leading=21)
h2 = ParagraphStyle("h2", fontName="ArB", fontSize=12.5, textColor=VERDE, spaceBefore=10, spaceAfter=4, leading=16)
h3 = ParagraphStyle("h3", fontName="ArB", fontSize=10.5, textColor=colors.HexColor("#1F4E79"), spaceBefore=6, spaceAfter=2, leading=13)
p = ParagraphStyle("p", fontName="Ar", fontSize=10, leading=14, spaceAfter=3)
pc = ParagraphStyle("pc", fontName="Ar", fontSize=8.8, leading=11.5)
pcb = ParagraphStyle("pcb", fontName="ArB", fontSize=8.8, leading=11.5)
pco = ParagraphStyle("pco", fontName="Co", fontSize=8.3, leading=11)
ph = ParagraphStyle("ph", fontName="ArB", fontSize=8.8, leading=11.5, textColor=colors.white)
peq = ParagraphStyle("peq", fontName="Ar", fontSize=8.5, leading=11, textColor=colors.HexColor("#555555"))
W = 17.6 * cm


def tab(cab, linhas, larg, cor=VERDE):
    dados = [[Paragraph(c, ph) for c in cab]] + [[Paragraph(str(c), pcb if i == 0 else pc) for i, c in enumerate(l)] for l in linhas]
    t = Table(dados, colWidths=[w * W for w in larg], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), cor), ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#BBBBBB")),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F7F7F7")]),
                           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def passos(lista):
    return tab(["Passo", "O que fazer"], [[str(i), t] for i, t in enumerate(lista, start=1)], [0.08, 0.92])


def cod(txt):
    t = Table([[Paragraph(txt.replace("\n", "<br/>"), pco)]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#F2F2F2")), ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#999999")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)]))
    return t


def caixa(titulo, itens, fundo, borda):
    corpo = [Paragraph(f"<b>{titulo}</b>", p)] + [Paragraph("• " + i, p) for i in itens]
    t = Table([[corpo]], colWidths=[W])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), fundo), ("BOX", (0, 0), (-1, -1), 1, borda),
                           ("LEFTPADDING", (0, 0), (-1, -1), 8), ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                           ("TOPPADDING", (0, 0), (-1, -1), 6), ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    return t


def rodape(c, d):
    c.saveState()
    c.setFont("Ar", 8)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(1.7 * cm, 1.1 * cm, "comprenolink.net  •  Guia de utilização dos geradores e planilhas  •  v1 de 04/11/2026")
    c.drawRightString(A4[0] - 1.7 * cm, 1.1 * cm, f"Página {d.page}")
    c.restoreState()


PS = 'cd "D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Base_Contatos_WhatsApp\\_fonte"'
st = [Paragraph("Guia de utilização: geradores, planilhas e recursos", h1),
      Paragraph("Passo a passo de tudo o que foi criado em 04/11/2026 na pasta <b>D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Base_Contatos_WhatsApp</b>. Para cada recurso: para que serve, quando usar, como usar e o que cuidar. As regras de envio estão em <b>Regras_de_Uso_Base_Contatos_WhatsApp.pdf</b> e o plano seguro de crescimento do Canal em <b>processo_crescimento_canal_whatsapp.pdf</b>. Versão 2, revisada em 04/11/2026 (noite).", p),
      Spacer(1, 3),
      caixa("Antes de tudo", [
          "A automação de convites foi <b>CANCELADA</b> por risco de bloqueio do WhatsApp. Não existe envio automático nem em massa: convites só à mão, pelo celular do dono, para quem ele conhece.",
          "A Base já tem <b>500 contatos importados</b> do Google Contatos (pendentes, fora da fila). O gerador gerar_base_contatos.py apagaria todos eles: não rode sem antes copiar o arquivo.",
          "Os arquivos .xlsx são para <b>preencher</b>. Os arquivos .py (pasta _fonte) são <b>geradores</b>: recriam o arquivo do zero e apagam o que foi digitado. Use-os só nas situações descritas aqui.",
          "Sempre que um gerador sobrescreve um arquivo existente, ele guarda uma cópia na pasta <b>_backups</b> antes."], LAR_C, LAR),
      Paragraph("1. O que existe na pasta", h2),
      tab(["Arquivo", "Tipo", "Para que serve"], [
          ["Base_Contatos_WhatsApp.xlsx", "Planilha de uso diário", "Contatos, fila do dia, registro de envios, seguidores do Canal, mensagens e parâmetros."],
          ["checklist_execucao_30_dias.xlsx", "Planilha de uso diário", "Pré-requisitos, rotina, comandos, plano de 30 dias a partir de 06/11 e balanço."],
          ["agenda_crescimento_canal_whatsapp.ics", "Agenda", "Lembretes das suas rotinas (convites à mão, respostas, fechar o dia, revisões), para importar no calendário."],
          ["Regras_de_Uso_Base_Contatos_WhatsApp.pdf", "Documento", "Regras de quem pode receber e como a planilha decide."],
          ["processo_crescimento_canal_whatsapp.pdf", "Documento", "Análise de risco, plano de atração e convite à mão, cuidados, paradas e contingência."],
          ["regras_execução.pdf", "Documento", "Resumo cronológico, atribuições e datas de início."],
          ["guia_utilização_gerador_excel.pdf", "Documento", "Este guia."],
          ["_fonte", "Pasta", "Os geradores (.py) e o importador do formulário."],
          ["_backups", "Pasta", "Cópias de segurança automáticas antes de qualquer sobrescrita ou gravação."]], [0.38, 0.17, 0.45]),
      Paragraph("2. Primeiro uso (ordem sugerida)", h2),
      passos([
          "Abra <b>checklist_execucao_30_dias.xlsx</b> > aba <b>Pre-requisitos</b> e veja o que falta.",
          "Abra <b>Base_Contatos_WhatsApp.xlsx</b> > aba <b>Base</b>. Os 6 contatos já convidados já têm número. Os 500 importados estão como Não perguntado (fora da fila).",
          "Na quinta, 10:30, mude para <b>Conhecido</b> só quem você conhece de verdade (item 3.2). Quem estiver como Conhecido, com número, aparece na aba Hoje.",
          "Importe o <b>agenda_crescimento_canal_whatsapp.ics</b> na sua agenda (item 7).",
          "Toda segunda, peça ao Claude: <b>importar formulário</b> e <b>ler seguidores do Canal</b> (itens 5 e 3.5).",
          "A partir de 06/11, envie à mão, pelo celular, até 5 convites por dia na 1ª semana e até 9 depois. O Claude só prepara a lista e registra o que você informar."]),
      PageBreak(),
      Paragraph("3. Base_Contatos_WhatsApp.xlsx", h2),
      Paragraph("Use o Excel para computador (Microsoft 365). Amarelo = você digita. Cinza = fórmula, nunca digite por cima. Verde = pode. Vermelho = não enviar ou alerta.", p),
      Paragraph("3.1 Aba Hoje (a fila do dia)", h3),
      Paragraph("Só leitura. Mostra a data, o limite (9), quantos já foram hoje, quantos restam, quantos estão aptos e quantos podem receber neste lote. A tabela lista até 20 pessoas com o ID, o nome, o número, a mensagem a usar (M1 ou M2) e o botão <b>Abrir conversa</b>.", p),
      passos([
          "Abra a aba <b>Hoje</b> e leia \"Podem receber neste lote\".",
          "Se for 0, não há ninguém para convidar hoje: cadastre contatos novos na aba Base e pare por hoje.",
          "Para cada nome, clique em <b>Abrir conversa</b> (abre o WhatsApp Web naquele número, sem enviar nada).",
          "Copie o texto da aba Mensagens, troque {nome}, envie e <b>registre na aba Envios</b>. A coluna \"Já enviou?\" muda para \"Registrado hoje\" quando o registro existe."]),
      Paragraph("3.2 Aba Base (os contatos)", h3),
      tab(["Coluna", "O que digitar", "Regra"], [
          ["B Nome", "Nome do contato", "Obrigatório. Sem nome a linha não conta."],
          ["C WhatsApp", "Somente números, com 55 + DDD + número. Ex.: 5511999998888", "12 ou 13 dígitos começando com 55. Outro formato é recusado."],
          ["D Origem", "Escolha na lista", "Contato pessoal, Cliente, Instagram, Blog - formulário, ManyChat, Indicação, Outro."],
          ["E Data do cadastro", "dd/mm/aaaa", "Data a partir de 2026."],
          ["F Consentimento", "Escolha na lista", "Sim, Conhecido, Não ou Não perguntado. Só Sim e Conhecido entram na fila."],
          ["G Data / H Como consentiu", "Data e a prova", "Ex.: \"respondeu quero no Direct em 05/11\". Sem prova, não vale."],
          ["I Entrou no Canal? / J Pediu para sair?", "Sim, Não ou Não sei", "Sim em qualquer um dos dois tira a pessoa da fila."],
          ["K, L, M, N, O (cinza)", "Automático", "Convites enviados, último envio, dias desde o último, PODE ENVIAR HOJE? e posição na fila."],
          ["P Observações", "Livre", "Anote o que for útil."]], [0.26, 0.38, 0.36]),
      passos([
          "Vá à primeira linha livre (o ID já vem preenchido: C001, C002...). São 500 linhas.",
          "Preencha nome, WhatsApp, origem, data do cadastro, consentimento, data do consentimento e a prova.",
          "Olhe a coluna <b>N (PODE ENVIAR HOJE?)</b>: SIM ou NÃO com o motivo (sem consentimento, limite de convites, aguardar N dia(s), número inválido, já entrou, pediu para sair).",
          "Para achar alguém, use o filtro do cabeçalho (seta nas colunas). Para voltar, limpe o filtro."]),
      Paragraph("3.3 Aba Envios (o registro de cada mensagem)", h3),
      passos([
          "Logo após cada mensagem enviada, preencha uma linha: <b>Data, Hora, ID do contato</b> (escolha na lista), <b>Mensagem</b> (M1 a M4), <b>Tipo</b>, <b>Enviado por</b> (Dono: os convites são enviados só por você), <b>Autorizado pelo dono?</b> e <b>Resultado</b>.",
          "O nome aparece sozinho na coluna D. Se aparecer \"ID não existe\", o ID não está na Base.",
          "Confira a coluna <b>L (Conferência)</b>: OK em verde. ALERTA em vermelho significa: sem autorização, contato sem consentimento, fora das 9h às 20h, passou do limite do dia ou ID inexistente. Corrija antes de continuar.",
          "Resultados: Enviado, Entrou no Canal, Respondeu, Pediu para sair, Sem resposta ou Erro. \"Pediu para sair\" e \"Entrou no Canal\" tiram a pessoa da fila automaticamente. \"Erro\" não conta como convite.",
          "Na coluna Lote, escreva o código do grupo de envios (ex.: L1-10/11). Em Observações, o que for útil."]),
      Paragraph("3.4 Aba Mensagens", h3),
      Paragraph("Quatro textos prontos: <b>M1</b> convite, <b>M2</b> lembrete (só para consentimento Sim, depois de 7 dias, uma vez), <b>M3</b> agradecimento e <b>M4</b> resposta a quem pede para sair. Copie o texto, troque {nome} pelo nome e varie a saudação para não enviar texto idêntico em sequência. Para mudar um texto, peça ao Claude (é um dos textos autorizados).", p),
      Paragraph("3.5 Aba Canal (seguidores por semana)", h3),
      passos([
          "Toda segunda: abra o WhatsApp Web > Canais > Compre no Link e veja o número de seguidores (ou escreva <b>ler seguidores do Canal</b> no chat).",
          "Na próxima linha livre da aba Canal, digite a data e o número. A coluna \"Novos desde a leitura anterior\" se calcula.",
          "Confira à direita: seguidores hoje e o que falta para as metas de 10/11 e 30/11 (estimativas, editáveis em H5 e H6)."]),
      Paragraph("3.6 Aba Parametros (limites)", h3),
      tab(["Célula", "Parâmetro", "Valor atual"], [
          ["B3", "Limite de envios por dia", "9"],
          ["B4", "Máximo de convites por contato com consentimento Sim", "2"],
          ["B5", "Máximo de convites por contato Conhecido", "1"],
          ["B6", "Dias mínimos entre dois convites ao mesmo contato", "7"],
          ["B7", "Intervalo mínimo entre mensagens (minutos)", "3"],
          ["B8 e B9", "Horário permitido (início e fim, em horas)", "9 e 20"]], [0.15, 0.65, 0.2]),
      Paragraph("Mudar o limite ou o horário vale como nova autorização: escreva <b>alterar limite para N</b> no chat e peça ao Claude para conferir os documentos. As colunas D a K à direita guardam as listas de escolha; não apague.", p),
      PageBreak(),
      Paragraph("4. checklist_execucao_30_dias.xlsx", h2),
      tab(["Aba", "Como usar"], [
          ["LEIA-ME", "Leia a situação e as cores. Não precisa preencher."],
          ["Pre-requisitos", "Na coluna Status de cada um dos 15 itens, escolha <b>OK</b> quando estiver pronto e anote a data conferida. No topo aparece \"x de 15\" e \"LIBERADO PARA INICIAR\" só quando todos estão OK."],
          ["Rotina diaria", "Só leitura. Lista horário, quem faz e o que fazer. Use como lembrete."],
          ["Comandos", "Só leitura. Os comandos do chat e do terminal, com o cuidado de cada um."],
          ["Plano 30 dias", "Uma linha por dia, de 10/11 a 09/12. Veja item 4.1."],
          ["Balanco", "Calcula sozinho os indicadores a partir do Plano. Preencha só o amarelo (seguidores em 09/12, decisão e observações)."],
          ["Nao executar", "Só leitura. Quando NÃO executar e o que fazer."]], [0.2, 0.8]),
      Paragraph("4.1 Aba Plano 30 dias, todo dia às 20:30", h3),
      passos([
          "Ache a linha do dia (a coluna Data mostra o dia e a coluna Fase mostra o teto: S1 = 5 (semana 1), S2+ = 9, PAUSA = 0 em 27/11).",
          "Escolha <b>V</b> ou <b>X</b> nas três colunas: 10:00 convites feitos, 19:20 respostas, 20:30 dia fechado.",
          "Digite o total de <b>Envios do dia</b>. O Excel recusa um valor acima do teto do dia.",
          "Digite <b>Alertas</b>, <b>Pediram para sair</b> e <b>Entraram no Canal</b> (números inteiros, 0 ou mais).",
          "Leia <b>Resultado do dia</b>: OK (3 V e dentro do teto), VER (algum X) ou ACIMA DO TETO. Escreva o motivo em Observações quando houver X.",
          "No topo da aba, veja o resumo: dias OK, dias com problema, total de envios, entraram, saídas e alertas."]),
      Paragraph("Linhas azuis são marcos (início, revisões e balanço). A linha cinza de 27/11 é a pausa nos convites na Black Friday. Só passe de 5 para 9 convites por dia se a semana 1 fechou sem aviso do WhatsApp e com até 5% de pedidos de saída.", p),
      Paragraph("4.2 Aba Balanco (09/12)", h3),
      passos([
          "Em 09/12, abra a aba <b>Balanco</b>. Os resultados já vêm do Plano.",
          "Veja a coluna Situação: OK ou REVISAR / ACIMA DE 5%. A taxa de entrada boa é acima de 15% (estimativa); abaixo de 5%, revise texto e origem.",
          "Digite os seguidores do Canal em 09/12.",
          "Escolha na lista a sua decisão: Continuar como está, Ajustar (nova autorização) ou Migrar para plataforma oficial. Escreva observações."]),
      Paragraph("5. Importador do formulário do blog", h2),
      Paragraph("O formulário \"Alertas Black Friday e Natal\" tem os campos opcionais WhatsApp e a caixa de consentimento. O importador lê as inscrições e coloca na Base apenas quem informou o número <b>e marcou a caixa</b>. Ignora números repetidos e inscrições sem consentimento.", p),
      passos([
          "<b>Feche o Excel</b> (o arquivo aberto fica bloqueado). Abra o terminal (PowerShell).",
          "Entre na pasta dos geradores e rode a simulação, que não grava nada:",
      ]),
      cod(PS + "\npython -X utf8 importar_leads_formulario.py"),
      Paragraph("O resultado mostra quantas inscrições foram lidas, quantas entram e os nomes. Se estiver certo, grave:", p),
      cod("python -X utf8 importar_leads_formulario.py --gravar"),
      Paragraph("Ele faz um backup em _backups, grava os contatos com Consentimento = Sim, origem \"Blog - formulário\" e a prova \"Formulário do blog, entrada nº ...\". Ou, mais simples: escreva <b>importar formulário</b> no chat e o Claude faz e mostra o resultado. Em 04/11 o formulário ainda não tinha inscrições.", p),
      PageBreak(),
      Paragraph("6. Os geradores (.py): quando e como usar", h2),
      caixa("Importante", [
          "Um gerador cria o arquivo de novo e <b>apaga tudo o que foi digitado</b>. Use só para recriar um arquivo estragado ou depois de uma mudança estrutural combinada com o Claude.",
          "Antes de sobrescrever, o gerador copia o arquivo antigo para a pasta _backups com data e hora. Para recuperar, copie o backup de volta para a pasta principal."], VERM_C, VERM),
      tab(["Gerador", "Cria", "Quando usar"], [
          ["gerar_base_contatos.py", "Base_Contatos_WhatsApp.xlsx", "Planilha estragada ou mudança de estrutura. Apaga contatos e envios."],
          ["gerar_checklist_xlsx.py", "checklist_execucao_30_dias.xlsx", "Se estragar ou se as datas do plano mudarem. Apaga as marcações."],
          ["gerar_agenda_crescimento.py", "agenda_crescimento_canal_whatsapp.ics", "Quando mudar horários ou datas das rotinas."],
          ["gerar_regras_pdf.py", "Regras_de_Uso_Base_Contatos_WhatsApp.pdf", "Quando o texto das regras mudar."],
          ["gerar_processo_pdf.py", "processo_crescimento_canal_whatsapp.pdf", "Quando o processo mudar."],
          ["gerar_regras_execucao_pdf.py", "regras_execução.pdf", "Quando o resumo mudar."],
          ["gerar_guia_pdf.py", "guia_utilização_gerador_excel.pdf", "Quando este guia mudar."]], [0.3, 0.35, 0.35]),
      Paragraph("Como rodar qualquer gerador (exemplo com a agenda, que não apaga dados digitados):", p),
      cod(PS + "\npython -X utf8 gerar_agenda_crescimento.py"),
      passos([
          "Para mudar um horário ou texto, peça ao Claude. Ele altera o gerador, roda e confere o resultado.",
          "Se for rodar você mesmo: <b>feche</b> o arquivo no Excel ou no leitor de PDF antes, senão o Windows bloqueia a gravação (erro Permission denied).",
          "Depois de gerar, abra o arquivo novo e confira. O gerador mostra \"OK:\" e o caminho quando termina.",
          "Se algo sair errado, restaure a cópia mais recente da pasta _backups."]),
      Paragraph("7. Agenda (.ics)", h2),
      passos([
          "Abra o arquivo <b>agenda_crescimento_canal_whatsapp.ics</b>. Ele tem 6 eventos: convites à mão 10:00, respostas 19:20 e fechar o dia 20:30 (diários), revisão de segunda 10:30, aprovar contatos às quintas e revisão mensal no dia 1.",
          "<b>Outlook:</b> Arquivo > Abrir e Exportar > Importar/Exportar > Importar um arquivo iCalendar (.ics). <b>Google Agenda:</b> Configurações > Importar e exportar > selecionar o arquivo > escolher a agenda de destino > Importar.",
          "Os eventos têm identificador fixo: importar de novo atualiza e não duplica. Mesmo assim, importe uma vez só e apague o arquivo da agenda se importou o errado.",
          "Os convites das 10:00 e o fechar o dia das 20:30 começam em 06/11; as respostas das 19:20, em 05/11. Os eventos antigos da automação (validar fila 09:50, autorização, fases e pausa) foram apagados do Google Agenda."]),
      Paragraph("8. Comandos do chat", h2),
      Paragraph("Escreva no chat com o Claude. A lista completa, com exemplos, está na aba <b>Comandos</b> do checklist.", p),
      tab(["Escreva", "Resultado"], [
          ["preparar lista de hoje", "Lista do dia com o texto de cada pessoa. Você envia à mão."],
          ["enviei: Nome1, Nome2", "Registra os envios na aba Envios (Enviado por = Dono)."],
          ["relatório do dia", "Enviados, respostas, saídas, avisos e saldo do limite."],
          ["importar formulário", "Simula e, com o seu OK, grava as inscrições na Base."],
          ["ler seguidores do Canal", "Lê e anota na aba Canal."],
          ["aprovar contatos: Nome1, Nome2", "Muda para Conhecido quem você conhece."],
          ["cadastrar contato: Nome, 55DDDnúmero, origem, consentimento", "Cadastra na Base com a data e a prova."],
          ["excluir contato: Nome", "Apaga os dados do contato e registra."],
          ["parar convites", "Registra a parada de 7 dias."],
          ["reduzir ritmo / manter ritmo", "Registra a decisão semanal sobre o teto (5 ou 9)."],
          ["gerar agenda", "Gera de novo o arquivo .ics."]], [0.5, 0.5]),
      Paragraph("9. Formulário do blog (campos WhatsApp)", h2),
      passos([
          "O formulário \"Alertas Black Friday e Natal\" ganhou em 04/11 o campo opcional <b>WhatsApp</b> e a caixa <b>\"Aceito receber o convite do Canal e ofertas no WhatsApp\"</b>. Aparece na página da Black Friday.",
          "Quem preenche o número e marca a caixa pode entrar na Base. Quem só preenche o número, sem marcar, não entra.",
          "Para ver as inscrições: painel do WordPress > Fluent Forms > Entradas. O aviso por e-mail ao admin já inclui o WhatsApp.",
          "Para voltar ao formulário antigo (sem WhatsApp), peça ao Claude: ele usa o backup <i>Gestao_Anuncios_Blog\\2_DADOS\\Blog_WordPress\\backups\\fluentform4_antes_whatsapp_2026-11-04_16h34.json</i>."]),
      Paragraph("10. Problemas comuns", h2),
      tab(["Problema", "Causa e solução"], [
          ["Permission denied ao gerar ou importar", "O arquivo está aberto no Excel ou no leitor de PDF. Feche e rode de novo."],
          ["#NOME? em fórmula", "Excel antigo. É preciso Microsoft 365 ou Excel 2019 (função MAXIFS)."],
          ["WhatsApp recusado ao digitar", "Digite só números, começando com 55, com 12 ou 13 dígitos (55 + DDD + número)."],
          ["Contato com SIM não aparece na aba Hoje", "Já atingiu o limite do dia (9) ou há outro motivo. Veja a coluna N da Base e o \"Restam hoje\"."],
          ["Conferência com ALERTA", "Corrija a linha em Envios (autorização, horário, limite do dia ou consentimento) antes de continuar."],
          ["Apaguei uma fórmula sem querer", "Desfaça (Ctrl+Z). Se já salvou, restaure a cópia de _backups."],
          ["Planilha estragou", "Copie o backup mais recente de _backups. Em último caso, rode o gerador (apaga os dados)."]], [0.38, 0.62]),
      Spacer(1, 6),
      Paragraph("Versão 1 - 04/11/2026. Este guia descreve os recursos existentes nesta data; quando algo mudar, o Claude atualiza o gerador e o guia.", peq)]

doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.7 * cm, rightMargin=1.7 * cm, topMargin=1.6 * cm, bottomMargin=1.8 * cm,
                        title="Guia de utilização: geradores, planilhas e recursos", author="comprenolink.net")
doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
print("OK:", SAIDA)
