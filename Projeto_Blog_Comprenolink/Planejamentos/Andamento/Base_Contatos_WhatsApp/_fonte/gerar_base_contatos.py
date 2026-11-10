# -*- coding: utf-8 -*-
"""Gera Base_Contatos_WhatsApp.xlsx (base de contatos com consentimento, fila de envio e registro de envios).
Uso: python -X utf8 gerar_base_contatos.py   (grava na pasta acima de _fonte)
ATENCAO: gerar de novo SOBRESCREVE a planilha. Se ja houver dados reais, faca copia antes (a pasta _backups guarda uma).
"""
import os, shutil, datetime
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.formatting.rule import FormulaRule
from openpyxl.utils import get_column_letter

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
SAIDA = PASTA + "/Base_Contatos_WhatsApp.xlsx"
LINK_CANAL = "https://whatsapp.com/channel/0029Vb9eTLd3rZZlBFjs8J3A"
N_BASE = 500          # linhas de contatos (5 a 504)
N_ENV = 2000          # linhas de envios (5 a 2004)
B0, B1 = 5, 5 + N_BASE - 1
E0, E1 = 5, 5 + N_ENV - 1

VERDE = "0B3D2E"; VERDE_C = "E8F5EE"; AMARELO = "FFF4C2"; CINZA = "F2F2F2"
f_tit = Font(name="Arial", size=15, bold=True, color=VERDE)
f_cab = Font(name="Arial", size=10, bold=True, color="FFFFFF")
f_txt = Font(name="Arial", size=10)
f_neg = Font(name="Arial", size=10, bold=True)
p_cab = PatternFill("solid", fgColor=VERDE)
p_in = PatternFill("solid", fgColor=AMARELO)
p_auto = PatternFill("solid", fgColor=CINZA)
p_ok = PatternFill("solid", fgColor="C6EFCE")
p_no = PatternFill("solid", fgColor="FFC7CE")
fino = Side(style="thin", color="BBBBBB")
borda = Border(left=fino, right=fino, top=fino, bottom=fino)
cen = Alignment(horizontal="center", vertical="center", wrap_text=True)
esq = Alignment(horizontal="left", vertical="center", wrap_text=True)

wb = Workbook()


def cab(ws, linha, titulos, larguras):
    for i, (t, w) in enumerate(zip(titulos, larguras), start=1):
        c = ws.cell(row=linha, column=i, value=t)
        c.font, c.fill, c.alignment, c.border = f_cab, p_cab, cen, borda
        ws.column_dimensions[get_column_letter(i)].width = w
    ws.row_dimensions[linha].height = 42


def titulo(ws, texto, sub=None):
    ws["A1"] = texto
    ws["A1"].font = f_tit
    if sub:
        ws["A2"] = sub
        ws["A2"].font = Font(name="Arial", size=9, italic=True, color="555555")


# ---------------------------------------------------------------- LEIA-ME
ws = wb.active
ws.title = "LEIA-ME"
titulo(ws, "Base de Contatos WhatsApp - comprenolink.net", "Regra de ouro: só se envia convite para quem aceitou ou conhece o dono, dentro do limite do dia e com a coluna PODE ENVIAR = SIM.")
linhas = [
    ("Para que serve", "Guardar quem pode receber o convite do Canal do WhatsApp, mostrar quem pode receber HOJE e registrar tudo o que foi enviado."),
    ("Abas", "Hoje (fila do dia) | Base (contatos) | Envios (registro) | Canal (seguidores por semana) | Mensagens (textos) | Parametros (limites e listas)."),
    ("Cores", "AMARELO = você digita. CINZA = fórmula, não mexer. VERDE = pode enviar. VERMELHO = não enviar / alerta."),
    ("Rotina diária (5 min)", "1) Abra a aba Hoje.  2) Veja quantos restam.  3) Envie só para quem aparece na lista (botão Abrir conversa).  4) Registre cada envio na aba Envios.  5) Confira se a coluna Conferência está OK."),
    ("Novo contato", "Aba Base: preencha Nome, WhatsApp (só números, com 55 + DDD), Origem, Consentimento e a data. Sem consentimento ou conhecimento pessoal, o contato nunca entra na fila."),
    ("Pediu para sair", "Registre em Envios com Resultado = Pediu para sair. Ele sai da fila para sempre. Responda com a mensagem M4."),
    ("Envio dos convites", "Os convites são enviados SÓ À MÃO pelo dono, pelo celular. O Claude não envia nada: prepara a lista e registra o que o dono informar (Enviado por = Dono). Máximo 9 por dia (5 na 1ª semana). Risco de bloqueio do número: parar 7 dias ao primeiro aviso do WhatsApp."),
    ("Detalhes completos", "Leia o PDF Regras_de_Uso_Base_Contatos_WhatsApp.pdf, que está na mesma pasta."),
]
r = 4
for k, v in linhas:
    ws.cell(row=r, column=1, value=k).font = f_neg
    ws.cell(row=r, column=2, value=v).font = f_txt
    ws.cell(row=r, column=2).alignment = esq
    ws.cell(row=r, column=1).alignment = esq
    ws.row_dimensions[r].height = 46
    r += 1
ws.column_dimensions["A"].width = 24
ws.column_dimensions["B"].width = 110

# ---------------------------------------------------------------- Parametros
wp = wb.create_sheet("Parametros")
titulo(wp, "Parâmetros e listas", "Células amarelas podem ser mudadas. As fórmulas leem daqui.")
par = [
    ("Limite de envios por dia (todos os contatos)", 9),
    ("Máximo de convites por contato com consentimento = Sim", 2),
    ("Máximo de convites por contato = Conhecido (conhece o dono, sem pedido)", 1),
    ("Dias mínimos entre dois convites ao mesmo contato", 7),
    ("Intervalo mínimo entre uma mensagem e outra (minutos)", 3),
    ("Horário permitido: início (hora)", 9),
    ("Horário permitido: fim (hora)", 20),
]
for i, (k, v) in enumerate(par, start=3):
    wp.cell(row=i, column=1, value=k).font = f_txt
    c = wp.cell(row=i, column=2, value=v)
    c.font, c.fill, c.alignment, c.border = f_neg, p_in, cen, borda
wp.column_dimensions["A"].width = 70
wp.column_dimensions["B"].width = 12
listas = {
    "D": ("Origem", ["Contato pessoal", "Cliente", "Instagram - seguidor", "Instagram - comentou/Direct", "Blog - formulário", "ManyChat", "Indicação", "Outro"]),
    "E": ("Consentimento", ["Sim", "Conhecido", "Não", "Não perguntado"]),
    "F": ("Resultado", ["Enviado", "Entrou no Canal", "Respondeu", "Pediu para sair", "Sem resposta", "Erro"]),
    "G": ("Tipo", ["Convite", "Lembrete", "Agradecimento", "Resposta"]),
    "H": ("Enviado por", ["Dono", "Claude"]),
    "I": ("Sim/Não", ["Sim", "Não"]),
    "J": ("Sim/Não/Não sei", ["Sim", "Não", "Não sei"]),
    "K": ("Mensagem", ["M1", "M2", "M3", "M4"]),
}
for col, (nome, itens) in listas.items():
    c = wp[f"{col}2"]
    c.value = nome
    c.font, c.fill, c.alignment = f_cab, p_cab, cen
    wp.column_dimensions[col].width = 26
    for j, it in enumerate(itens, start=3):
        wp[f"{col}{j}"] = it
        wp[f"{col}{j}"].font = f_txt
wp["A12"] = "Consentimento: Sim = a pessoa pediu ou aceitou receber. Conhecido = conhece o dono pessoalmente, recebe 1 convite só. Não / Não perguntado = nunca entra na fila."
wp["A12"].font = Font(name="Arial", size=9, italic=True)
wp["A12"].alignment = esq
wp.row_dimensions[12].height = 40


def ref_lista(col, n):
    return f"=Parametros!${col}$3:${col}${2 + n}"


# ---------------------------------------------------------------- Base
wsb = wb.create_sheet("Base")
titulo(wsb, "Base de contatos", "Amarelo = você digita | Cinza = automático. O contato só entra na fila se PODE ENVIAR HOJE = SIM.")
tit_b = ["ID", "Nome", "WhatsApp (55 + DDD + número, só números)", "Origem", "Data do cadastro", "Consentimento", "Data do consentimento", "Como consentiu / prova", "Entrou no Canal?", "Pediu para sair?", "Convites enviados", "Último envio", "Dias desde o último", "PODE ENVIAR HOJE?", "Fila", "Observações"]
larg_b = [8, 26, 20, 24, 14, 16, 14, 34, 12, 12, 11, 13, 12, 28, 7, 40]
cab(wsb, 4, tit_b, larg_b)
for i in range(N_BASE):
    r = B0 + i
    wsb.cell(row=r, column=1, value=f"C{i + 1:03d}")
    for col in range(1, 17):
        c = wsb.cell(row=r, column=col)
        c.font, c.border = f_txt, borda
        c.alignment = esq if col in (2, 8, 14, 16) else cen
        if col in (2, 3, 4, 5, 6, 7, 8, 9, 10, 16):
            c.fill = p_in
        else:
            c.fill = p_auto
    wsb.cell(row=r, column=3).number_format = "0"
    for col in (5, 7, 12):
        wsb.cell(row=r, column=col).number_format = "dd/mm/yyyy"
    env_id = f"Envios!$C${E0}:$C${E1}"
    env_res = f"Envios!$I${E0}:$I${E1}"
    env_dt = f"Envios!$A${E0}:$A${E1}"
    wsb.cell(row=r, column=11, value=f'=IF(B{r}="","",COUNTIFS({env_id},A{r},{env_res},"<>Erro",{env_res},"<>"))')
    wsb.cell(row=r, column=12, value=f'=IF(OR(B{r}="",K{r}=0),"",_xlfn.MAXIFS({env_dt},{env_id},A{r},{env_res},"<>Erro",{env_res},"<>"))')
    wsb.cell(row=r, column=13, value=f'=IF(L{r}="","",TODAY()-L{r})')
    sair = f'OR(J{r}="Sim",COUNTIFS({env_id},A{r},{env_res},"Pediu para sair")>0)'
    entrou = f'OR(I{r}="Sim",COUNTIFS({env_id},A{r},{env_res},"Entrou no Canal")>0)'
    maxc = f'IF(F{r}="Sim",Parametros!$B$4,Parametros!$B$5)'
    num_ok = f'AND(ISNUMBER(C{r}),OR(LEN(C{r})=12,LEN(C{r})=13),LEFT(C{r},2)="55")'
    wsb.cell(row=r, column=14, value=(
        f'=IF(B{r}="","",IF({sair},"NÃO: pediu para sair",IF({entrou},"NÃO: já entrou no Canal",'
        f'IF(NOT(OR(F{r}="Sim",F{r}="Conhecido")),"NÃO: sem consentimento",'
        f'IF(K{r}>={maxc},"NÃO: limite de convites",'
        f'IF(AND(M{r}<>"",M{r}<Parametros!$B$6),"NÃO: aguardar "&(Parametros!$B$6-M{r})&" dia(s)",'
        f'IF(NOT({num_ok}),"NÃO: número inválido","SIM")))))))'))
    wsb.cell(row=r, column=15, value=f'=IF(N{r}="SIM",COUNTIF($N${B0}:N{r},"SIM"),"")')
    wsb.cell(row=r, column=14).font = f_neg
wsb.freeze_panes = "C5"
wsb.auto_filter.ref = f"A4:P{B1}"
rng_n = f"N{B0}:N{B1}"
wsb.conditional_formatting.add(rng_n, FormulaRule(formula=[f'N{B0}="SIM"'], fill=p_ok))
wsb.conditional_formatting.add(rng_n, FormulaRule(formula=[f'LEFT(N{B0},3)="NÃO"'], fill=p_no))
wsb.conditional_formatting.add(f"G{B0}:G{B1}", FormulaRule(formula=[f'AND(OR(F{B0}="Sim"),G{B0}="")'], fill=p_no))


def dv_lista(ws, formula, rango, msg=None):
    d = DataValidation(type="list", formula1=formula, allow_blank=True, showErrorMessage=True,
                       errorTitle="Valor inválido", error=msg or "Escolha um item da lista.")
    ws.add_data_validation(d)
    d.add(rango)


dv_lista(wsb, ref_lista("D", 8), f"D{B0}:D{B1}")
dv_lista(wsb, ref_lista("E", 4), f"F{B0}:F{B1}")
dv_lista(wsb, ref_lista("J", 3), f"I{B0}:I{B1}")
dv_lista(wsb, ref_lista("I", 2), f"J{B0}:J{B1}")
dn = DataValidation(type="custom", formula1=f'=AND(ISNUMBER(C{B0}),OR(LEN(C{B0})=12,LEN(C{B0})=13),LEFT(C{B0},2)="55")',
                    allow_blank=True, showErrorMessage=True, errorTitle="Número inválido",
                    error="Digite só números, começando com 55 + DDD + número (12 ou 13 dígitos). Ex.: 5511999998888")
wsb.add_data_validation(dn)
dn.add(f"C{B0}:C{B1}")
dd = DataValidation(type="date", operator="greaterThanOrEqual", formula1="46023", allow_blank=True, showErrorMessage=True,
                    errorTitle="Data inválida", error="Digite uma data válida (dd/mm/aaaa) a partir de 2026.")
wsb.add_data_validation(dd)
dd.add(f"E{B0}:E{B1}")
dd.add(f"G{B0}:G{B1}")

# ---------------------------------------------------------------- Envios
wse = wb.create_sheet("Envios")
titulo(wse, "Registro de envios", "Registre CADA mensagem enviada (feita pelo dono ou pelo Claude). A Base lê esta aba para contar convites e datas.")
tit_e = ["Data", "Hora", "ID do contato", "Nome (automático)", "Mensagem", "Tipo", "Enviado por", "Autorizado pelo dono?", "Resultado", "Lote", "Observações", "Conferência (automática)"]
larg_e = [13, 9, 12, 26, 11, 15, 12, 14, 18, 12, 42, 40]
cab(wse, 4, tit_e, larg_e)
for i in range(N_ENV):
    r = E0 + i
    for col in range(1, 13):
        c = wse.cell(row=r, column=col)
        c.font, c.border = f_txt, borda
        c.alignment = esq if col in (4, 11, 12) else cen
        c.fill = p_auto if col in (4, 12) else p_in
    wse.cell(row=r, column=1).number_format = "dd/mm/yyyy"
    wse.cell(row=r, column=2).number_format = "hh:mm"
    wse.cell(row=r, column=4, value=f'=IF(C{r}="","",IFERROR(INDEX(Base!$B${B0}:$B${B1},MATCH(C{r},Base!$A${B0}:$A${B1},0)),"ID não existe"))')
    cons = f'IFERROR(INDEX(Base!$F${B0}:$F${B1},MATCH(C{r},Base!$A${B0}:$A${B1},0)),"")'
    wse.cell(row=r, column=12, value=(
        f'=IF(C{r}="","",IF(D{r}="ID não existe","ALERTA: ID não existe na Base",'
        f'IF(H{r}<>"Sim","ALERTA: sem autorização do dono",'
        f'IF(AND(E{r}<>"M4",NOT(OR({cons}="Sim",{cons}="Conhecido"))),"ALERTA: contato sem consentimento",'
        f'IF(OR(B{r}<TIME(Parametros!$B$8,0,0),B{r}>TIME(Parametros!$B$9,0,0)),"ALERTA: fora do horário permitido",'
        f'IF(COUNTIFS($A${E0}:$A${E1},A{r},$I${E0}:$I${E1},"<>Erro",$C${E0}:$C${E1},"<>")>Parametros!$B$3,"ALERTA: passou do limite do dia","OK"))))))'))
wse.freeze_panes = "D5"
wse.auto_filter.ref = f"A4:L{E1}"
wse.conditional_formatting.add(f"L{E0}:L{E1}", FormulaRule(formula=[f'LEFT(L{E0},6)="ALERTA"'], fill=p_no))
wse.conditional_formatting.add(f"L{E0}:L{E1}", FormulaRule(formula=[f'L{E0}="OK"'], fill=p_ok))
dv_lista(wse, f"=Base!$A${B0}:$A${B1}", f"C{E0}:C{E1}", "Use um ID que exista na aba Base (ex.: C001).")
dv_lista(wse, ref_lista("K", 4), f"E{E0}:E{E1}")
dv_lista(wse, ref_lista("G", 4), f"F{E0}:F{E1}")
dv_lista(wse, ref_lista("H", 2), f"G{E0}:G{E1}")
dv_lista(wse, ref_lista("I", 2), f"H{E0}:H{E1}")
dv_lista(wse, ref_lista("F", 6), f"I{E0}:I{E1}")
d2 = DataValidation(type="date", operator="greaterThanOrEqual", formula1="46023", allow_blank=True, showErrorMessage=True,
                    errorTitle="Data inválida", error="Digite uma data válida (dd/mm/aaaa).")
wse.add_data_validation(d2)
d2.add(f"A{E0}:A{E1}")

# ---------------------------------------------------------------- Hoje
wh = wb.create_sheet("Hoje", 1)
titulo(wh, "Fila de hoje", "Envie SÓ para quem está na lista abaixo, até o limite do dia. Depois registre cada envio na aba Envios.")
env_a = f"Envios!$A${E0}:$A${E1}"
env_c = f"Envios!$C${E0}:$C${E1}"
env_i = f"Envios!$I${E0}:$I${E1}"
resumo = [
    ("Data de hoje", "=TODAY()", "dd/mm/yyyy"),
    ("Limite de envios por dia", "=Parametros!B3", "0"),
    ("Já enviados hoje", f'=COUNTIFS({env_a},TODAY(),{env_c},"<>",{env_i},"<>Erro")', "0"),
    ("Restam hoje", "=MAX(0,B5-B6)", "0"),
    ("Contatos aptos hoje (PODE ENVIAR = SIM)", f'=COUNTIF(Base!$N${B0}:$N${B1},"SIM")', "0"),
    ("Podem receber neste lote", "=MIN(B7,B8)", "0"),
]
for i, (k, f, nf) in enumerate(resumo, start=4):
    wh.cell(row=i, column=1, value=k).font = f_neg
    c = wh.cell(row=i, column=2, value=f)
    c.font, c.fill, c.alignment, c.border, c.number_format = f_neg, p_auto, cen, borda, nf
wh["D4"] = "Horário permitido"
wh["D4"].font = f_neg
wh["E4"] = '=TEXT(Parametros!B8,"00")&"h às "&TEXT(Parametros!B9,"00")&"h"'
wh["D5"] = "Intervalo entre mensagens"
wh["D5"].font = f_neg
wh["E5"] = '=Parametros!B7&" min ou mais"'
wh["D7"] = "Contatos na base"
wh["D7"].font = f_neg
wh["E7"] = f'=COUNTA(Base!$B${B0}:$B${B1})'
wh["D8"] = "Com consentimento ou conhecidos"
wh["D8"].font = f_neg
wh["E8"] = f'=COUNTIF(Base!$F${B0}:$F${B1},"Sim")+COUNTIF(Base!$F${B0}:$F${B1},"Conhecido")'
wh["D9"] = "Convites enviados (total)"
wh["D9"].font = f_neg
wh["E9"] = f'=COUNTIFS({env_c},"<>",{env_i},"<>Erro")'
wh["D10"] = "Entraram no Canal (registrados)"
wh["D10"].font = f_neg
wh["E10"] = f'=COUNTIF({env_i},"Entrou no Canal")'
for a in ("E4", "E5", "E7", "E8", "E9", "E10"):
    wh[a].font, wh[a].alignment, wh[a].border, wh[a].fill = f_neg, cen, borda, p_auto
wh.conditional_formatting.add("B7", FormulaRule(formula=["B7=0"], fill=p_no))
wh.conditional_formatting.add("B7", FormulaRule(formula=["B7>0"], fill=p_ok))
tit_h = ["Nº", "ID", "Nome", "WhatsApp", "Mensagem a usar", "Abrir conversa (clique)", "Já enviou? (marque na aba Envios)"]
larg_h = [44, 10, 28, 18, 22, 24, 34]
cab(wh, 13, tit_h, larg_h)
wh.column_dimensions["A"].width = 44
wh.column_dimensions["D"].width = 30
wh.column_dimensions["E"].width = 22
for k in range(1, 21):
    r = 13 + k
    wh.cell(row=r, column=1, value=k)
    idx = f'MATCH({k},Base!$O${B0}:$O${B1},0)'
    wh.cell(row=r, column=2, value=f'=IF({k}>$B$9,"",INDEX(Base!$A${B0}:$A${B1},{idx}))')
    wh.cell(row=r, column=3, value=f'=IF(B{r}="","",INDEX(Base!$B${B0}:$B${B1},{idx}))')
    wh.cell(row=r, column=4, value=f'=IF(B{r}="","",INDEX(Base!$C${B0}:$C${B1},{idx}))')
    wh.cell(row=r, column=5, value=f'=IF(B{r}="","",IF(INDEX(Base!$K${B0}:$K${B1},{idx})=0,"M1 - convite","M2 - lembrete"))')
    wh.cell(row=r, column=6, value=f'=IF(B{r}="","",HYPERLINK("https://wa.me/"&D{r},"Abrir conversa"))')
    wh.cell(row=r, column=7, value=f'=IF(B{r}="","",IF(COUNTIFS({env_c},B{r},{env_a},TODAY())>0,"Registrado hoje","Falta registrar"))')
    for col in range(1, 8):
        c = wh.cell(row=r, column=col)
        c.font, c.border, c.fill = f_txt, borda, p_auto
        c.alignment = cen if col != 3 else esq
        if col == 4:
            c.number_format = "0"
wh.conditional_formatting.add("G14:G33", FormulaRule(formula=['G14="Registrado hoje"'], fill=p_ok))
wh.conditional_formatting.add("G14:G33", FormulaRule(formula=['G14="Falta registrar"'], fill=PatternFill("solid", fgColor="FFEB9C")))
wh["A35"] = "Se a lista estiver vazia: não há contato apto. Cadastre contatos com consentimento na aba Base. Nunca envie para quem não está aqui."
wh["A35"].font = Font(name="Arial", size=9, italic=True, color="9C0006")

# ---------------------------------------------------------------- Canal
wc = wb.create_sheet("Canal")
titulo(wc, "Seguidores do Canal por semana", "Toda segunda: abra WhatsApp Web > Canais > Compre no Link e anote o número de seguidores.")
cab(wc, 4, ["Data da leitura", "Seguidores do Canal", "Novos desde a leitura anterior", "De onde vieram (se souber)", "Observações"], [16, 18, 22, 40, 50])
for i in range(60):
    r = 5 + i
    for col in range(1, 6):
        c = wc.cell(row=r, column=col)
        c.font, c.border, c.alignment = f_txt, borda, cen if col < 4 else esq
        c.fill = p_auto if col == 3 else p_in
    wc.cell(row=r, column=1).number_format = "dd/mm/yyyy"
    if i > 0:
        wc.cell(row=r, column=3, value=f'=IF(AND(ISNUMBER(B{r}),ISNUMBER(B{r - 1})),B{r}-B{r - 1},"")')
wc["A5"] = datetime.date(2026, 11, 4)
wc["B5"] = 2
wc["D5"] = "Ponto de partida"
wc["E5"] = "Leitura no WhatsApp Web. Canal na bio do Instagram e Status de convite feitos neste dia."
wc["G4"] = "Metas (estimativa, rever toda segunda)"
wc["G4"].font = f_neg
metas = [("10/11/2026", 10), ("30/11/2026", 20)]
wc["G5"], wc["H5"] = "Até 10/11/2026", 10
wc["G6"], wc["H6"] = "Até 30/11/2026", 20
wc["G7"] = "Seguidores hoje (última leitura)"
wc["H7"] = "=LOOKUP(9.99E+307,B5:B64)"
wc["G8"] = "Falta para a meta de 10/11"
wc["H8"] = "=MAX(0,H5-H7)"
wc["G9"] = "Falta para a meta de 30/11"
wc["H9"] = "=MAX(0,H6-H7)"
for r in range(5, 10):
    wc[f"G{r}"].font = f_neg
    wc[f"H{r}"].font, wc[f"H{r}"].alignment, wc[f"H{r}"].border = f_neg, cen, borda
    wc[f"H{r}"].fill = p_in if r in (5, 6) else p_auto
wc.column_dimensions["G"].width = 34
wc.column_dimensions["H"].width = 12
dc = DataValidation(type="date", operator="greaterThanOrEqual", formula1="46023", allow_blank=True, showErrorMessage=True,
                    errorTitle="Data inválida", error="Digite uma data válida.")
wc.add_data_validation(dc)
dc.add("A5:A64")

# ---------------------------------------------------------------- Mensagens
wm = wb.create_sheet("Mensagens")
titulo(wm, "Mensagens prontas", "Troque {nome} pelo nome do contato. Não use preço, 'mais vendido' ou promessa. O link do Canal é sempre o mesmo.")
cab(wm, 4, ["ID", "Nome", "Quando usar", "Texto (copiar e colar)", "Regras"], [8, 22, 34, 90, 46])
msgs = [
    ("M1", "Convite", "Primeiro contato. Só para quem aparece na fila.",
     "Oi, {nome}! Criei um canal no WhatsApp com os achados do dia do Mercado Livre. Se quiser receber, é só entrar: " + LINK_CANAL + " . Sem compromisso, pode sair quando quiser.",
     "Uma vez por contato. Varie a saudação para não enviar texto idêntico a todos."),
    ("M2", "Lembrete", "Só para Consentimento = Sim, sem resposta há 7 dias ou mais, e 1 única vez.",
     "Oi, {nome}! Passando só para lembrar do canal com os achados do dia: " + LINK_CANAL + " . Se não quiser receber, é só me avisar.",
     "Nunca para quem é 'Conhecido'. Nunca depois de 'Pediu para sair'."),
    ("M3", "Agradecimento", "Quando a pessoa entrar no Canal.",
     "Que bom que você entrou, {nome}! Se gostar, repasse o link para 2 amigos: " + LINK_CANAL,
     "Registrar Resultado = Entrou no Canal na aba Envios."),
    ("M4", "Resposta a quem pede para sair", "Quando alguém disser que não quer receber.",
     "Tudo bem, {nome}! Não vou mais te enviar convites. Obrigado pelo retorno.",
     "Registrar Resultado = Pediu para sair. A pessoa sai da fila para sempre."),
]
for i, m in enumerate(msgs, start=5):
    for col, v in enumerate(m, start=1):
        c = wm.cell(row=i, column=col, value=v)
        c.font, c.border, c.alignment = f_txt, borda, esq
    wm.row_dimensions[i].height = 70

# ---------------------------------------------------------------- dados iniciais (envios de 04/11/2026)
sem = [("Joyce", "Contato pessoal"), ("Augusto Genro", "Contato pessoal"), ("Rosana", "Contato pessoal"),
       ("Erico", "Contato pessoal"), ("José Anjos (POCO PHONE X6)", "Contato pessoal"), ("Juliana", "Contato pessoal")]
for i, (nome, orig) in enumerate(sem):
    r = B0 + i
    wsb.cell(row=r, column=2, value=nome)
    wsb.cell(row=r, column=4, value=orig)
    wsb.cell(row=r, column=5, value=datetime.date(2026, 11, 4))
    wsb.cell(row=r, column=6, value="Conhecido")
    wsb.cell(row=r, column=7, value=datetime.date(2026, 11, 4))
    wsb.cell(row=r, column=8, value="Conhece o dono; convite único feito pelo dono em 04/11/2026")
    wsb.cell(row=r, column=9, value="Não sei")
    wsb.cell(row=r, column=10, value="Não")
    wsb.cell(row=r, column=16, value="Preencher o número do WhatsApp quando for conferir.")
wsb.cell(row=B0 + 4, column=16, value="Preencher o número. Havia 2 conversas com este nome em 04/11 (confirmar se é um número do próprio dono).")
env = [(1, "15:18"), (2, "15:18"), (3, "15:18"), (4, "15:18"), (5, "15:18"), (5, "15:18"), (6, "15:24")]
for i, (idc, hr) in enumerate(env):
    r = E0 + i
    wse.cell(row=r, column=1, value=datetime.date(2026, 11, 4))
    h, m = hr.split(":")
    wse.cell(row=r, column=2, value=datetime.time(int(h), int(m)))
    wse.cell(row=r, column=3, value=f"C{idc:03d}")
    wse.cell(row=r, column=5, value="M1")
    wse.cell(row=r, column=6, value="Convite")
    wse.cell(row=r, column=7, value="Dono")
    wse.cell(row=r, column=8, value="Sim")
    wse.cell(row=r, column=9, value="Enviado")
    wse.cell(row=r, column=10, value="L0-04/11")
    wse.cell(row=r, column=11, value="Lançamento inicial: envio feito pelo dono antes da planilha existir.")

for w in wb.worksheets:
    w.sheet_view.showGridLines = False
    w.sheet_properties.tabColor = VERDE if w.title in ("Hoje", "Base", "Envios") else "999999"
wb.active = 1

if os.path.exists(SAIDA):
    os.makedirs(PASTA + "/_backups", exist_ok=True)
    shutil.copy2(SAIDA, PASTA + "/_backups/Base_Contatos_WhatsApp_" + datetime.datetime.now().strftime("%d-%m-%Y_%Hh%M") + ".xlsx")
wb.save(SAIDA)
print("OK:", SAIDA)
