# -*- coding: utf-8 -*-
"""Gera checklist_execucao_30_dias.xlsx (checklist, comandos, pre-requisitos e plano de 30 dias a partir de 10/11/2026).
ATENCAO: gerar de novo SOBRESCREVE as marcacoes. Se ja houver dados, copie o arquivo antes (a pasta _backups guarda uma copia)."""
import os, shutil, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
SAIDA = PASTA + "/checklist_execucao_30_dias.xlsx"
VERDE = "0B3D2E"
f_tit = Font(name="Arial", size=15, bold=True, color=VERDE)
f_cab = Font(name="Arial", size=10, bold=True, color="FFFFFF")
f_txt = Font(name="Arial", size=10)
f_neg = Font(name="Arial", size=10, bold=True)
p_cab = PatternFill("solid", fgColor=VERDE)
p_in = PatternFill("solid", fgColor="FFF4C2")
p_auto = PatternFill("solid", fgColor="F2F2F2")
p_ok = PatternFill("solid", fgColor="C6EFCE")
p_no = PatternFill("solid", fgColor="FFC7CE")
p_mar = PatternFill("solid", fgColor="DDEBF7")
p_gray = PatternFill("solid", fgColor="D9D9D9")
fino = Side(style="thin", color="BBBBBB")
borda = Border(left=fino, right=fino, top=fino, bottom=fino)
cen = Alignment(horizontal="center", vertical="center", wrap_text=True)
esq = Alignment(horizontal="left", vertical="center", wrap_text=True)
wb = Workbook()


def titulo(ws, t, sub=None):
    ws["A1"] = t
    ws["A1"].font = f_tit
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(name="Arial", size=9, italic=True, color="555555")


def cab(ws, linha, titulos, larguras):
    for i, (t, w) in enumerate(zip(titulos, larguras), start=1):
        c = ws.cell(row=linha, column=i, value=t)
        c.font, c.fill, c.alignment, c.border = f_cab, p_cab, cen, borda
        ws.column_dimensions[chr(64 + i)].width = w
    ws.row_dimensions[linha].height = 34


def corpo(ws, linha, valores, centros=(), entradas=(), altura=None):
    for i, v in enumerate(valores, start=1):
        c = ws.cell(row=linha, column=i, value=v)
        c.font, c.border = f_txt, borda
        c.alignment = cen if i in centros else esq
        if i in entradas:
            c.fill = p_in
    if altura:
        ws.row_dimensions[linha].height = altura


def lista(ws, itens, rango):
    d = DataValidation(type="list", formula1='"' + ",".join(itens) + '"', allow_blank=True, showErrorMessage=True,
                       errorTitle="Valor inválido", error="Escolha um item da lista.")
    ws.add_data_validation(d)
    d.add(rango)


# ------------------------------------------------------------ LEIA-ME
ws = wb.active
ws.title = "LEIA-ME"
titulo(ws, "Checklist de execução: 30 dias a partir de 10/11/2026", "Complementa processo_automatização_whatsapp.pdf, regras_execução.pdf e Base_Contatos_WhatsApp.xlsx (mesma pasta).")
txt = [
    ("Situação", "A automação NÃO está ativada. Só liga depois que o dono escrever o termo do item 6 do processo_automatização_whatsapp.pdf, e só com 9 ou mais contatos aptos. Em 04/11 há 0."),
    ("Como usar", "Pré-requisitos: marque cada item como OK. Plano 30 dias: todo dia às 20:30 preencha V ou X nas 3 validações, o total de envios, alertas, saídas e entraram. O resumo e o balanço se calculam sozinhos."),
    ("Cores", "AMARELO = você preenche. CINZA = fórmula, não digitar por cima. VERDE = OK. VERMELHO = problema ou acima do teto. AZUL = marco do plano."),
    ("Abas", "Pre-requisitos | Rotina diaria | Comandos | Plano 30 dias | Balanco | Nao executar."),
    ("Regra de ouro", "Só se envia para quem aparece com PODE ENVIAR = SIM na aba Hoje da planilha Base_Contatos_WhatsApp, até o teto da fase, entre 9h e 20h. Qualquer problema: escrever pausar automação no chat."),
    ("Datas", "Datas e metas são estimativas e podem ser ajustadas pelo dono nas revisões de segunda. Se a base não tiver 9 aptos até 09/11, o plano desloca para o dia em que houver."),
]
for i, (k, v) in enumerate(txt, start=4):
    ws.cell(row=i, column=1, value=k).font = f_neg
    c = ws.cell(row=i, column=2, value=v)
    c.font, c.alignment = f_txt, esq
    ws.cell(row=i, column=1).alignment = esq
    ws.row_dimensions[i].height = 48
ws.column_dimensions["A"].width = 18
ws.column_dimensions["B"].width = 120

# ------------------------------------------------------------ Pre-requisitos
wp = wb.create_sheet("Pre-requisitos")
titulo(wp, "Pré-requisitos (marcar até 09/11)", "Para ligar a automação, todos precisam estar OK.")
req = [
    ("Aba Hoje da Base_Contatos_WhatsApp com 9 ou mais contatos com PODE ENVIAR = SIM", "Dono e Claude"),
    ("Números do WhatsApp dos contatos preenchidos na aba Base (55 + DDD + número)", "Dono"),
    ("Consentimento e prova registrados em cada contato (Sim ou Conhecido)", "Claude"),
    ("Limite do dia = 9 na aba Parametros (já ajustado em 04/11)", "Claude"),
    ("Textos M1 e M2 revisados pelo dono na aba Mensagens", "Dono"),
    ("PC ligado, sem suspender nem hibernar, com internet estável (ajustar plano de energia se necessário)", "Dono"),
    ("Aplicativo do Claude aberto neste PC, como já é preciso para a divulgação das 19:12", "Dono"),
    ("Chrome aberto com a extensão Claude conectada e WhatsApp Web logado no WhatsApp Business do blog", "Dono"),
    ("Celular do WhatsApp Business com internet e bateria (o WhatsApp Web depende dele)", "Dono"),
    ("Instagram logado no Chrome (para ler Direct e comentários)", "Dono"),
    ("Microsoft 365 com Excel para computador; planilha fechada quando o importador rodar", "Dono"),
    ("Arquivo agenda_automacao_whatsapp.ics importado na agenda do dono", "Dono"),
    ("Formulário do blog no ar com os campos WhatsApp e consentimento (feito em 04/11)", "Claude"),
    ("Termo de autorização escrito no chat em 10/11, 09:00", "Dono"),
    ("Tarefas agendadas dos blocos 10:00, 14:00 e 18:00 criadas pelo Claude após o termo", "Claude"),
]
cab(wp, 6, ["Nº", "Condição", "Quem", "Status", "Data conferida", "Observações"], [6, 90, 16, 14, 16, 40])
for i, (c, q) in enumerate(req, start=1):
    corpo(wp, 6 + i, [i, c, q, "Pendente", None, None], centros=(1, 3, 4, 5), entradas=(4, 5, 6), altura=32)
    wp.cell(row=6 + i, column=5).number_format = "dd/mm/yyyy"
n0, n1 = 7, 6 + len(req)
wp["A3"] = "Itens OK"
wp["A3"].font = f_neg
wp["B3"] = f'=COUNTIF(D{n0}:D{n1},"OK")&" de {len(req)}"'
wp["B4"] = f'=IF(COUNTIF(D{n0}:D{n1},"OK")={len(req)},"LIBERADO PARA INICIAR","NÃO LIBERADO: faltam "&({len(req)}-COUNTIF(D{n0}:D{n1},"OK"))&" item(ns)")'
for a in ("B3", "B4"):
    wp[a].font, wp[a].fill, wp[a].alignment, wp[a].border = f_neg, p_auto, esq, borda
wp["A4"] = "Situação"
wp["A4"].font = f_neg
wp.conditional_formatting.add(f"D{n0}:D{n1}", FormulaRule(formula=[f'D{n0}="OK"'], fill=p_ok))
wp.conditional_formatting.add(f"D{n0}:D{n1}", FormulaRule(formula=[f'D{n0}="Pendente"'], fill=p_no))
wp.conditional_formatting.add("B4", FormulaRule(formula=['LEFT(B4,3)="LIB"'], fill=p_ok))
wp.conditional_formatting.add("B4", FormulaRule(formula=['LEFT(B4,3)="NÃO"'], fill=p_no))
lista(wp, ["Pendente", "OK"], f"D{n0}:D{n1}")
wp["A{}".format(n1 + 2)] = "Atenção: o sistema pode recusar tarefas agendadas que enviam mensagens sozinhas (já aconteceu com a divulgação diária). Se ocorrer, o envio passa a ser com o dono acompanhando no PC, sem trocar nenhuma regra."
wp["A{}".format(n1 + 2)].font = Font(name="Arial", size=9, italic=True, color="9C0006")
wp.freeze_panes = "A7"

# ------------------------------------------------------------ Rotina diaria
wr = wb.create_sheet("Rotina diaria")
titulo(wr, "Quando executa (rotina diária)")
cab(wr, 3, ["Horário", "Quem", "O que", "Duração"], [16, 18, 100, 12])
rot = [
    ("09:50", "Dono", "Ver PC, Chrome e WhatsApp Web. Validar a fila e os textos na aba Hoje.", "5 min"),
    ("10:00", "Claude", "Bloco 1: até 3 envios, 5 min entre eles.", "-"),
    ("14:00", "Claude", "Bloco 2 (fases 2 e 3): até 3 envios.", "-"),
    ("18:00 a 18:20", "Claude", "Bloco 3 (fase 3): até 3 envios. Termina antes das 19:12.", "-"),
    ("19:12", "Claude", "Divulgação diária (Status, Canal e Story): outro processo, mesmo Chrome.", "-"),
    ("19:20", "Dono", "Responder as pessoas que escreveram.", "5 min"),
    ("20:30", "Dono", "Validação final: Conferência sem ALERTA e no máximo 9 envios. Marcar V ou X na aba Plano 30 dias.", "5 min"),
    ("Segunda, 10:30", "Claude e dono", "Revisão semanal: seguidores do Canal, saídas e ritmo.", "15 min"),
    ("Quinta, 10:30", "Dono", "Aprovar contatos pessoais novos.", "5 min"),
    ("Dia 1, 10:30", "Dono", "Revisão mensal de consentimentos e exclusões.", "20 min"),
]
for i, r in enumerate(rot, start=4):
    corpo(wr, i, list(r), centros=(1, 2, 4), altura=22)

# ------------------------------------------------------------ Comandos
wc = wb.create_sheet("Comandos")
titulo(wc, "Comandos que o dono pode usar", "Escreva no chat com o Claude (convenção combinada em 04/11/2026).")
cab(wc, 4, ["Escreva", "O que acontece", "Quando usar"], [48, 90, 30])
cmd = [
    ("status da automação", "O Claude responde fase atual, teto do dia, aptos hoje, enviados hoje e alertas.", "A qualquer hora"),
    ("pausar automação", "Para tudo imediatamente. Nenhum bloco seguinte envia até você mandar retomar.", "Se algo parecer errado"),
    ("retomar automação", "O Claude confere os pré-requisitos e volta na fase em que estava.", "Depois de pausa, ou em 28/11"),
    ("relatório do dia", "Lista enviados, respostas, saídas, alertas e saldo do limite.", "Às 20:30"),
    ("importar formulário", "O Claude simula a importação e mostra quem entraria. Só grava depois do seu OK.", "Toda segunda"),
    ("ler seguidores do Canal", "Lê o número no WhatsApp Web e anota na aba Canal da Base.", "Toda segunda"),
    ("cadastrar contato: Nome, 55DDDnúmero, origem, consentimento", "Cadastra na aba Base com a data e a prova. Ex.: cadastrar contato: Maria, 5511999998888, Contato pessoal, Conhecido.", "Ao aprovar um contato"),
    ("excluir contato: Nome", "Apaga os dados do contato (pedido de exclusão) e registra a data.", "Quando alguém pedir"),
    ("subir para fase 2 / subir para fase 3 / manter fase / reduzir ritmo", "Registra a sua decisão semanal. O Claude só muda de fase com este comando.", "Segunda, na revisão"),
    ("alterar limite para N", "Muda o limite do dia na aba Parametros. Vale como nova autorização.", "Só se você decidir"),
    ("gerar agenda", "Gera de novo o arquivo .ics com as rotinas.", "Se mudar datas ou horários"),
]
for i, r in enumerate(cmd, start=5):
    corpo(wc, i, list(r), altura=34)
    wc.cell(row=i, column=1).font = f_neg
r0 = 5 + len(cmd) + 1
wc.cell(row=r0, column=1, value="No terminal (pasta D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Base_Contatos_WhatsApp\\_fonte)").font = f_neg
cab(wc, r0 + 1, ["Comando", "Para que serve", "Cuidado"], [48, 90, 30])
term = [
    ("python -X utf8 importar_leads_formulario.py", "Simula a importação do formulário do blog. Não grava nada.", "Seguro"),
    ("python -X utf8 importar_leads_formulario.py --gravar", "Grava na Base quem informou o WhatsApp e marcou a caixa. Faz backup antes.", "Feche o Excel antes"),
    ("python -X utf8 gerar_agenda_automacao.py", "Regenera o agenda_automacao_whatsapp.ics.", "Seguro"),
    ("python -X utf8 gerar_base_contatos.py", "Recria a planilha Base do zero e APAGA os dados.", "Só com cópia feita antes"),
]
for i, r in enumerate(term, start=r0 + 2):
    corpo(wc, i, list(r), altura=26)
    wc.cell(row=i, column=1).font = Font(name="Consolas", size=9)
wc.cell(row=r0 + 5, column=3).fill = p_no

# ------------------------------------------------------------ Plano 30 dias
wl = wb.create_sheet("Plano 30 dias")
titulo(wl, "Plano de 30 dias (10/11/2026 a 09/12/2026)", "Fase 1: 3/dia (10 a 16/11) | Fase 2: 6/dia (17 a 23/11) | Fase 3: 9/dia (a partir de 24/11). Cada fase só começa com a decisão do dono na segunda anterior.")
tit = ["Data", "Dia", "Fase", "Teto do dia", "Claude (blocos)", "Dono: além da rotina e marcos", "09:50 fila validada", "19:20 respostas", "20:30 validação final", "Envios do dia", "Alertas", "Pediram para sair", "Entraram no Canal", "Resultado do dia", "Observações"]
lar = [12, 6, 8, 9, 26, 56, 11, 11, 11, 10, 9, 10, 10, 18, 40]
for i, (t, w) in enumerate(zip(tit, lar), start=1):
    c = wl.cell(row=14, column=i, value=t)
    c.font, c.fill, c.alignment, c.border = f_cab, p_cab, cen, borda
    wl.column_dimensions[chr(64 + i)].width = w
wl.row_dimensions[14].height = 44
dias = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
D = datetime.date
extras = {
    D(2026, 11, 10): "09:00 escrever a autorização no chat. Primeiro dia: 3 envios acompanhados. INÍCIO DA FASE 1",
    D(2026, 11, 16): "10:30 revisão da semana 1. Decidir: subir para fase 2, manter ou reduzir. Aprovar contatos",
    D(2026, 11, 17): "INÍCIO DA FASE 2 (se aprovada)",
    D(2026, 11, 23): "10:30 revisão da semana 2. Decidir: subir para fase 3, manter ou reduzir. Aprovar contatos",
    D(2026, 11, 24): "INÍCIO DA FASE 3 (se aprovada)",
    D(2026, 11, 26): "Já existe lembrete às 20:00 da Black Friday (outra pendência)",
    D(2026, 11, 27): "PAUSA: dia D da Black Friday. Sem convites automáticos",
    D(2026, 11, 28): "09:00 conferir o relatório de 27/11 e escrever retomar automação",
    D(2026, 11, 30): "10:30 revisão semanal. Conferir meta do Canal (20 seguidores, estimativa) e definir a meta nova. Aprovar contatos",
    D(2026, 12, 1): "10:30 revisão mensal de consentimentos e exclusões (20 min)",
    D(2026, 12, 7): "10:30 revisão semanal. Rever textos M1 e M2 para o Natal. Aprovar contatos",
    D(2026, 12, 9): "BALANÇO DOS 30 DIAS (aba Balanco). Decidir: continuar, ajustar ou migrar para plataforma oficial",
}
P0 = 15
for i in range(30):
    r = P0 + i
    d = D(2026, 11, 10) + datetime.timedelta(days=i)
    if d < D(2026, 11, 17):
        fase, teto, claude = "F1", 3, "10:00 (3 envios)"
    elif d < D(2026, 11, 24):
        fase, teto, claude = "F2", 6, "10:00 (3) + 14:00 (3)"
    else:
        fase, teto, claude = "F3", 9, "10:00, 14:00 e 18:00 (3 cada)"
    if d == D(2026, 11, 27):
        fase, teto, claude = "PAUSA", 0, "nenhum envio"
    dono = extras.get(d, "")
    if not dono and d.weekday() == 0:
        dono = "10:30 revisão semanal e aprovar contatos (15 min)"
    if not dono and d.weekday() == 3:
        dono = "10:30 aprovar contatos pessoais novos (5 min)"
    corpo(wl, r, [d, dias[d.weekday()], fase, teto, claude, dono or "só a rotina diária", None, None, None, None, None, None, None, None, None],
          centros=(1, 2, 3, 4, 7, 8, 9, 10, 11, 12, 13, 14), entradas=(7, 8, 9, 10, 11, 12, 13, 15), altura=30)
    wl.cell(row=r, column=1).number_format = "dd/mm/yyyy"
    wl.cell(row=r, column=14, value=f'=IF(COUNTA(G{r}:J{r})=0,"",IF(J{r}>D{r},"ACIMA DO TETO",IF(AND(G{r}="V",H{r}="V",I{r}="V"),"OK","VER")))').fill = p_auto
    wl.cell(row=r, column=14).font = f_neg
    if d in extras and any(k in extras[d] for k in ("INÍCIO", "BALANÇO", "PAUSA", "revisão", "retomar")):
        for col in (1, 2, 3, 4, 5, 6):
            wl.cell(row=r, column=col).fill = p_gray if d == D(2026, 11, 27) else p_mar
P1 = P0 + 29
lista(wl, ["V", "X"], f"G{P0}:I{P1}")
dn = DataValidation(type="custom", formula1=f"=AND(ISNUMBER(J{P0}),J{P0}>=0,J{P0}<=D{P0})", allow_blank=True, showErrorMessage=True,
                    errorTitle="Acima do teto", error="O total de envios não pode passar do teto do dia. Se passou, registre o problema na observação e avise o Claude.")
wl.add_data_validation(dn)
dn.add(f"J{P0}:J{P1}")
dnum = DataValidation(type="whole", operator="greaterThanOrEqual", formula1="0", allow_blank=True, showErrorMessage=True, errorTitle="Valor inválido", error="Digite um número inteiro, 0 ou maior.")
wl.add_data_validation(dnum)
dnum.add(f"K{P0}:M{P1}")
wl.conditional_formatting.add(f"G{P0}:I{P1}", FormulaRule(formula=[f'G{P0}="V"'], fill=p_ok))
wl.conditional_formatting.add(f"G{P0}:I{P1}", FormulaRule(formula=[f'G{P0}="X"'], fill=p_no))
wl.conditional_formatting.add(f"N{P0}:N{P1}", FormulaRule(formula=[f'N{P0}="OK"'], fill=p_ok))
wl.conditional_formatting.add(f"N{P0}:N{P1}", FormulaRule(formula=[f'OR(N{P0}="VER",N{P0}="ACIMA DO TETO")'], fill=p_no))
wl.conditional_formatting.add(f"J{P0}:J{P1}", FormulaRule(formula=[f'AND(ISNUMBER(J{P0}),J{P0}>D{P0})'], fill=p_no))
# resumo (topo)
resumo = [
    ("Dias com resultado OK", f'=COUNTIF(N{P0}:N{P1},"OK")'),
    ("Dias com problema (VER ou acima do teto)", f'=COUNTIF(N{P0}:N{P1},"VER")+COUNTIF(N{P0}:N{P1},"ACIMA DO TETO")'),
    ("Total de envios", f'=SUM(J{P0}:J{P1})'),
    ("Entraram no Canal", f'=SUM(M{P0}:M{P1})'),
    ("Pediram para sair", f'=SUM(L{P0}:L{P1})'),
    ("Alertas", f'=SUM(K{P0}:K{P1})'),
]
for i, (k, f) in enumerate(resumo, start=4):
    wl.cell(row=i, column=1, value=k).font = f_neg
    wl.merge_cells(start_row=i, start_column=1, end_row=i, end_column=3)
    c = wl.cell(row=i, column=4, value=f)
    c.font, c.fill, c.alignment, c.border = f_neg, p_auto, cen, borda
wl.freeze_panes = f"C{P0}"

# ------------------------------------------------------------ Balanco
wbl = wb.create_sheet("Balanco")
titulo(wbl, "Balanço dos 30 dias (09/12/2026)", "Os resultados vêm da aba Plano 30 dias. Preencha só o amarelo.")
cab(wbl, 4, ["Indicador", "Resultado", "Meta ou regra", "Situação"], [46, 16, 62, 22])
PL = "'Plano 30 dias'!"
bal = [
    ("Envios no total", f"={PL}D6", "Dentro do teto de cada fase", None),
    ("Contatos que entraram no Canal", f"={PL}D7", "Meta da semana revista a cada segunda", None),
    ("Taxa de entrada (entraram ÷ convites)", f'=IF(B5=0,"",B6/B5)', "Acima de 15% (estimativa); abaixo de 5% revisar texto e origem", '=IF(B7="","",IF(B7>=0.15,"OK",IF(B7<0.05,"REVISAR","ATENÇÃO")))'),
    ("Pedidos para sair (% dos convites)", f'=IF(B5=0,"",{PL}D8/B5)', "Até 5% dos convites", '=IF(B8="","",IF(B8<=0.05,"OK","ACIMA DE 5%"))'),
    ("Alertas na Conferência e erros", f"={PL}D9", "0", '=IF(B9=0,"OK","REVISAR")'),
    ("Dias fechados com OK", f"={PL}D4", "Todos, menos os dias sem PC ligado", None),
    ("Dias com problema", f"={PL}D5", "0", '=IF(B11=0,"OK","REVISAR")'),
    ("Seguidores do Canal em 09/12", None, "A nova meta definida em 30/11", None),
]
for i, (k, f, m, s) in enumerate(bal, start=5):
    corpo(wbl, i, [k, f, m, s], centros=(2, 4), altura=26)
    wbl.cell(row=i, column=1).font = f_neg
    wbl.cell(row=i, column=2).fill = p_auto
    wbl.cell(row=i, column=4).fill = p_auto
wbl.cell(row=12, column=2).fill = p_in
wbl["B7"].number_format = "0.0%"
wbl["B8"].number_format = "0.0%"
wbl.conditional_formatting.add("D5:D12", FormulaRule(formula=['D5="OK"'], fill=p_ok))
wbl.conditional_formatting.add("D5:D12", FormulaRule(formula=['AND(D5<>"",D5<>"OK")'], fill=p_no))
wbl["A14"] = "Decisão do dono em 09/12"
wbl["A14"].font = f_neg
wbl["B14"].fill, wbl["B14"].border, wbl["B14"].alignment = p_in, borda, cen
wbl.merge_cells("B14:C14")
lista(wbl, ["Continuar como está", "Ajustar (nova autorização)", "Migrar para plataforma oficial"], "B14")
wbl["A15"] = "Observações"
wbl["A15"].font = f_neg
wbl.merge_cells("B15:D15")
wbl["B15"].fill, wbl["B15"].border = p_in, borda
wbl.row_dimensions[15].height = 60
wbl["B15"].alignment = esq

# ------------------------------------------------------------ Nao executar
wn = wb.create_sheet("Nao executar")
titulo(wn, "Quando NÃO executar")
cab(wn, 3, ["Situação", "O que fazer"], [60, 90])
nao = [
    ("Menos de 9 aptos em 09/11", "Adiar o início para o dia em que houver. Não reduzir o consentimento."),
    ("Termo de autorização não escrito", "Não enviar nada. Vale só o \"pode enviar\" por lote."),
    ("PC desligado, Chrome fechado ou WhatsApp Web deslogado", "O bloco não acontece. Não recuperar depois."),
    ("Aviso, verificação ou limite do WhatsApp", "Parar por 7 dias e avisar o Claude. Não contornar."),
    ("2 ou mais pedidos de saída no mesmo dia", "Parar os blocos restantes do dia e rever a lista."),
    ("Conferência com ALERTA na planilha Base_Contatos_WhatsApp", "Corrigir a linha antes de qualquer novo envio."),
    ("Fora das 9h às 20h ou em 27/11", "Nenhum envio."),
]
for i, r in enumerate(nao, start=4):
    corpo(wn, i, list(r), altura=26)
    wn.cell(row=i, column=1).font = f_neg

for w in wb.worksheets:
    w.sheet_view.showGridLines = False
    w.sheet_properties.tabColor = VERDE if w.title in ("Plano 30 dias", "Pre-requisitos", "Balanco") else "999999"
wb.active = 3
if os.path.exists(SAIDA):
    os.makedirs(PASTA + "/_backups", exist_ok=True)
    shutil.copy2(SAIDA, PASTA + "/_backups/checklist_execucao_30_dias_" + datetime.datetime.now().strftime("%d-%m-%Y_%Hh%M") + ".xlsx")
wb.save(SAIDA)
print("OK:", SAIDA)
