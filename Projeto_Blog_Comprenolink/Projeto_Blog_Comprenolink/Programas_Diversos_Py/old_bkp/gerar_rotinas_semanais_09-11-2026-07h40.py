# -*- coding: utf-8 -*-
"""Rotinas semanais do Checklist Turbinar (passos 21 e 23), criado em 03/11/2026.
Gera em D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias:
  - Planilha_Semanal_Turbinar.xlsx        (passo 23: números da segunda; semanas 1 e 2 já preenchidas)
  - Roteiro_Rotinas_Segunda_e_Sexta.pdf   (passos 21 e 23: o que fazer, passo a passo)
  - Agenda_Rotinas_Semanais.ics           (segunda 10:45, sexta 14:00 e conferências do guia)
Uso: python -X utf8 gerar_rotinas_semanais.py   (a planilha NÃO é sobrescrita se já existir: gera _nova)
Caminhos com barra normal.
"""
import csv
import os
import sys

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/"
HIST = "D:/Projeto_Blog_Comprenolink/99_Relatorios_Diarios/historico_consolidado/historico_quadros.csv"
VENDAS = "D:/Projeto_Blog_Comprenolink/99_Relatorios_Diarios/vendas_historico/historico_vendas.csv"

SEMANAS = [  # (n, início, fim, rótulo)
    (1, "21/10", "27/10"), (2, "28/10", "03/11"), (3, "04/11", "10/11"), (4, "11/11", "17/11"),
    (5, "18/11", "24/11"), (6, "25/11", "01/12"), (7, "02/12", "08/12"), (8, "09/12", "20/12")]


def dados_historicos():
    """Acumulados do painel (visitas, visitantes, cliques) por dia -> valor no fim de cada semana já fechada."""
    h = {r["dia"]: r for r in csv.DictReader(open(HIST, encoding="utf-8-sig"), delimiter=";")}
    def ate(dia):
        ks = [k for k in h if k <= dia]
        return h[max(ks)] if ks else None
    return ate


def vendas_por_semana():
    v = list(csv.DictReader(open(VENDAS, encoding="utf-8-sig"), delimiter=";"))
    faixas = {1: ("2026-10-21", "2026-10-27"), 2: ("2026-10-28", "2026-11-03")}
    saida = {}
    for n, (a, b) in faixas.items():
        sel = [x for x in v if a <= x["data"][:10] <= b]
        f = lambda s: [float(x["comissao"] or 0) for x in sel if x["status"] == s]
        saida[n] = dict(apr=len(f("Aprovada")), pend=len(f("Pendente")), com_apr=sum(f("Aprovada")), com_pend=sum(f("Pendente")))
    return saida


def planilha():
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
    from openpyxl.utils import get_column_letter
    ate = dados_historicos()
    vs = vendas_por_semana()
    wb = Workbook()
    ws = wb.active
    ws.title = "Semanal"
    azul, amar, cinza = "1F2A44", "FFE600", "F2F4F8"
    borda = Border(*(Side(style="thin", color="C8CDD6"),) * 4)
    ws["A1"] = "Planilha semanal de acompanhamento - comprenolink.net (Checklist Turbinar, parte 7)"
    ws["A1"].font = Font(bold=True, size=14, color=azul)
    ws["A2"] = ("Preencha toda SEGUNDA com os números do Painel (99_Relatorios_Diarios) e do painel de Afiliados do ML. "
                "Colunas amarelas = você digita; as demais calculam sozinhas. 'Acumulado' = valor do painel no fim da semana.")
    ws["A2"].alignment = Alignment(wrap_text=True, vertical="top")
    ws.merge_cells("A2:P2"); ws.row_dimensions[2].height = 34
    cab = ["Semana", "Período", "Visitas (acumulado)", "Visitantes únicos (acum.)", "Cliques meli.la (acum.)",
           "Visitas na semana", "Cliques na semana", "Taxa de clique", "Vendas aprovadas", "Vendas pendentes",
           "Comissão aprovada R$", "Comissão pendente R$", "Melhor canal", "Decisão da semana", "Leitura automática", "Observações"]
    for j, t in enumerate(cab, 1):
        c = ws.cell(row=4, column=j, value=t)
        c.font = Font(bold=True, color="FFFFFF"); c.fill = PatternFill("solid", fgColor=azul)
        c.alignment = Alignment(wrap_text=True, vertical="center", horizontal="center"); c.border = borda
    ws.row_dimensions[4].height = 44
    # linha base (início do acompanhamento no painel): 21/10
    base = ate("2026-10-21")
    r0 = 5
    ws.cell(row=r0, column=1, value="Base"); ws.cell(row=r0, column=2, value="21/10 (início do painel)")
    ws.cell(row=r0, column=3, value=int(base["visitas"])); ws.cell(row=r0, column=4, value=int(base["visitantes"]))
    ws.cell(row=r0, column=5, value=int(base["cliques"]))
    ws.cell(row=r0, column=16, value="Ponto de partida. A página inicial era 'Hello world' até 21/10.")
    fim = {1: "2026-10-27", 2: "2026-11-03"}
    notas = {1: "Maioria das visitas = testes e o próprio dono. Compra orgânica de 26/10 (Tampa, em revisão) veio de busca na internet.",
             2: "Medição ligada em 03/11 (Search Console, Bing, GA4). Black Friday e Natal publicadas; formulário de alertas no ar."}
    decisoes = {2: "Semana de arrumar a base: medição + páginas de campanha. Próximo: publicar e medir o canal Instagram/WhatsApp."}
    for i, (n, a, b) in enumerate(SEMANAS):
        r = r0 + 1 + i
        ws.cell(row=r, column=1, value=n); ws.cell(row=r, column=2, value=f"{a} a {b}")
        if n in fim:
            d = ate(fim[n])
            ws.cell(row=r, column=3, value=int(d["visitas"])); ws.cell(row=r, column=4, value=int(d["visitantes"]))
            ws.cell(row=r, column=5, value=int(d["cliques"]))
            s = vs[n]
            ws.cell(row=r, column=9, value=s["apr"]); ws.cell(row=r, column=10, value=s["pend"])
            ws.cell(row=r, column=11, value=round(s["com_apr"], 2)); ws.cell(row=r, column=12, value=round(s["com_pend"], 2))
            ws.cell(row=r, column=16, value=notas[n])
            if n in decisoes:
                ws.cell(row=r, column=14, value=decisoes[n])
        prev = r - 1
        ws.cell(row=r, column=6, value=f'=IF(C{r}="","",C{r}-C{prev})')
        ws.cell(row=r, column=7, value=f'=IF(E{r}="","",E{r}-E{prev})')
        ws.cell(row=r, column=8, value=f'=IF(OR(F{r}="",F{r}=0),"",G{r}/F{r})')
        ws.cell(row=r, column=15, value=(
            f'=IF(F{r}="","",IF(F{r}<50,"Poucas visitas: o problema é divulgação",'
            f'IF(H{r}<0.1,"Taxa de clique < 10%: revisar página/tabela do topo",'
            f'IF(AND(G{r}>=20,I{r}=0),"Muitos cliques, sem venda: trocar produto/ver vendedor","Ok: repetir o que funcionou"))))'))
    ult = r0 + len(SEMANAS)
    for r in range(r0, ult + 1):
        for j in range(1, 17):
            c = ws.cell(row=r, column=j); c.border = borda
            c.alignment = Alignment(wrap_text=True, vertical="top")
            if j in (3, 4, 5, 9, 10, 11, 12, 13, 14, 16) and r > r0:
                c.fill = PatternFill("solid", fgColor=amar if j in (3, 4, 5, 9, 10, 11, 12, 13, 14) else cinza)
        ws.cell(row=r, column=8).number_format = "0.0%"
        ws.cell(row=r, column=11).number_format = 'R$ #,##0.00'; ws.cell(row=r, column=12).number_format = 'R$ #,##0.00'
    for col, w in zip("ABCDEFGHIJKLMNOP", (8, 22, 12, 12, 12, 11, 11, 10, 11, 11, 13, 13, 16, 38, 34, 48)):
        ws.column_dimensions[col].width = w
    ws.freeze_panes = "C5"

    m = wb.create_sheet("Metas e regras")
    linhas = [("Metas (Checklist Turbinar, parte 3)", ""),
              ("Até 10/11", "300 visitas reais na página de produtos e 1a venda aprovada"),
              ("Até 30/11 (Black Friday)", "1.500 visitas no mes e taxa de clique >= 15%"),
              ("Até 31/12", "3.000+ visitas/mes e 10+ vendas no mes"), ("", ""),
              ("Como ler os números (parte 7)", ""),
              ("Muitas visitas e poucos cliques (taxa < 10%)", "O problema é a página: reveja a tabela do topo, os botões e se o produto bate com o título."),
              ("Muitos cliques e nenhuma venda em 2 semanas", "Produto caro, vendedor com reputação ruim ou frete alto: troque por um semelhante."),
              ("Poucas visitas", "O problema é divulgação: aumente a frequência no canal que mais trouxe visitas."),
              ("Um post trouxe muito mais visitas que os outros", "Faça mais 3 variações dele na mesma semana."), ("", ""),
              ("Regra da segunda-feira", "O canal/post que mais trouxe CLIQUES ganha o dobro de posts; o que trouxe zero por 2 semanas é trocado. Produtos mais clicados sobem na 'Escolha rápida'."),
              ("Atenção com os números", "O contador de 'visitas' do painel inclui testes e o próprio dono. Prefira 'visitantes únicos' e, a partir de 06/11, os dados do Google Analytics (Site Kit).")]
    for i, (a, b) in enumerate(linhas, 1):
        m.cell(row=i, column=1, value=a).font = Font(bold=bool(a and not b), color=azul if a and not b else "000000")
        m.cell(row=i, column=2, value=b).alignment = Alignment(wrap_text=True, vertical="top")
    m.column_dimensions["A"].width = 46; m.column_dimensions["B"].width = 100
    destino = SAIDA + "Planilha_Semanal_Turbinar.xlsx"
    if os.path.exists(destino):
        destino = SAIDA + "Planilha_Semanal_Turbinar_nova.xlsx"
    wb.save(destino)
    print("Planilha:", destino)


def roteiro_pdf():
    import gerar_pendencias_detalhado as base
    from gerar_pendencias_detalhado import (AZUL, AZUL_C, LARANJA, LARANJA_C, P, VERDE, VERDE_C, VERMELHO, VERMELHO_C,
                                            bloco, faixa, info, passos, tabela)
    from datetime import date
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer
    base.HOJE = date(2026, 11, 3)
    st = [Spacer(1, 0.4 * cm), P("ROTINAS DA SEMANA", "capa_t"), Spacer(1, 4),
          P("Segunda: os números (passo 23) | Sexta: SEO (passo 21)<br/>comprenolink.net - Checklist Turbinar", "capa_s"), Spacer(1, 8),
          info([("Em uma frase", "Segunda 30 minutos olhando os números e decidindo UMA coisa. Sexta 1 hora cuidando do Google."),
                ("Quando", "Segunda 10:15 (vendas do ML por prints e rodar o painel, lembrete que já existe) e 10:45 (reunião dos números). "
                           "Sexta 14:00. Tudo está na agenda única: agenda_nova_pendencias.ics."),
                ("Onde registrar", "Planilha_Semanal_Turbinar.xlsx (mesma pasta deste PDF). Semanas 1 e 2 já estão preenchidas."),
                ("Quer ajuda?", "Escreva ao Claude: \"rotina de segunda\" ou \"rotina de sexta\". Ele faz a parte que dá para fazer pelo computador.")]),
          Spacer(1, 8),
          bloco("Regras de ouro", [
              "Mude UMA coisa por semana e olhe o resultado na segunda seguinte (Parte 8 do checklist).",
              "Sem preço, sem \"mais vendido\" e sem promessa nos textos. Sempre o aviso de link de afiliado.",
              "Não gaste com anúncio pago sem comissão que pague (regra de ouro do dinheiro do checklist)."], VERMELHO, VERMELHO_C),
          PageBreak(),
          faixa("23", "Segunda-feira: os números (30 min)", "10:15 e 10:45 - toda segunda", AZUL), Spacer(1, 6),
          passos([
              ("10:15 - Vendas do ML Afiliados", "A conta não tem botão de exportar: abra a aba Vendas (Últimos 180 dias, os 4 status marcados), tire um print de cada trecho/página da tabela e mande ao Claude, que atualiza o arquivo de vendas em D:\\Projeto_Blog_Comprenolink\\99_Relatorios_Diarios\\vendas_afiliados. Passo a passo no Anexo A do nova_pendencias.pdf."),
              ("Rodar o painel", "Dois cliques em D:\\Projeto_Blog_Comprenolink\\99_Relatorios_Diarios\\ATUALIZAR_PAINEL.bat. Abra o PDF mais recente (Painel_conversao_performance_...)."),
              ("10:45 - Preencher a planilha", "Abra Planilha_Semanal_Turbinar.xlsx. Na linha da semana digite: Visitas, Visitantes únicos e Cliques (acumulados do painel), "
               "vendas aprovadas e pendentes e as comissões. A taxa de clique e a 'leitura automática' calculam sozinhas."),
              ("Descobrir o melhor canal", "No painel (aba Campanhas) veja a origem que mais trouxe CLIQUES: instagram, whatsapp, tiktok... Escreva na coluna 'Melhor canal'."),
              ("Olhar o Google", "A partir de 06/11: Site Kit (WordPress) mostra visitantes do Google Analytics; Search Console mostra as pesquisas. Anote o que chamar atenção."),
              ("Decidir UMA coisa", "Canal que mais trouxe cliques ganha o dobro de posts; o que trouxe zero por 2 semanas é trocado; os produtos mais clicados sobem na "
               "'Escolha rápida'. Escreva a decisão na coluna 'Decisão da semana'.")], AZUL),
          Spacer(1, 6),
          tabela(["O que a leitura automática diz", "O que fazer"],
                 [["Poucas visitas (menos de 50 na semana)", "O problema é divulgação: aumente a frequência no canal que mais trouxe visitas."],
                  ["Taxa de clique abaixo de 10%", "O problema é a página: reveja a tabela do topo, os botões e se o produto bate com o título."],
                  ["Muitos cliques e nenhuma venda em 2 semanas", "Produto caro, vendedor ruim ou frete alto: troque por um semelhante."],
                  ["Ok: repetir o que funcionou", "Faça mais 3 variações do post que mais trouxe visitas, na mesma semana."]],
                 [0.4, 0.6], cor=AZUL),
          Spacer(1, 6),
          bloco("Cuidado com os números", [
              "O contador de 'visitas' do painel inclui testes e o próprio dono (hoje 470 visitas, mas só 15 visitantes únicos).",
              "Por isso, olhe sempre 'visitantes únicos' e, quando houver dados, o Google Analytics.",
              "Venda aprovada só aparece no painel do ML Afiliados: o blog não enxerga compras."], LARANJA, LARANJA_C),
          PageBreak(),
          faixa("21", "Sexta-feira: SEO (1 hora)", "14:00 - toda sexta", VERDE), Spacer(1, 6),
          passos([
              ("Search Console - Desempenho", "search.google.com/search-console (conta compre.no.link26@gmail.com). Abra Desempenho > Consultas. Procure pesquisas com MUITAS impressões e POUCOS cliques."),
              ("Melhorar o título/descrição dessas páginas", "No WordPress: abra a página > All in One SEO > título e descrição. Escreva algo que responda a pesquisa. Os textos seguem as regras de ouro."),
              ("Ligar páginas entre si", "Toda página nova deve ter link para o guia e para a Black Friday/Natal, e receber link de alguma página antiga. As categorias já se ligam sozinhas."),
              ("Checar a saúde do site", "Dois cliques em D:\\Projeto_Blog_Comprenolink\\2-Verificar_Erros_Blog\\testar_site_de_novo.bat e, se quiser, D:\\Projeto_Blog_Comprenolink\\1- Gera_Relatorio\\4_test_blog_seo.exe."),
              ("Pedir indexação do que for novo", "Search Console > Inspeção de URL > cole o endereço > Solicitar indexação (páginas novas ou muito alteradas)."),
              ("Guia: data de atualização a cada 15 dias", "Datas: 13/11, 26/11 e 11/12. Só troque o 'Atualizado em' depois de conferir anúncios e links (o painel verifica os anúncios). "
               "Comando: gerenciar_blog.py substituir \"Atualizado em 01/11/2026\" \"Atualizado em DD/MM/2026\" --aplicar (ou peça ao Claude).")], VERDE),
          Spacer(1, 6),
          bloco("Meta da rotina", [
              "1 página nova por semana (passo 13: fones, TVs, presentes, celulares, reviews, comparativos).",
              "Guia atualizado a cada 15 dias. O Google leva de 4 a 12 semanas para dar posições boas: constância ganha.",
              "Não troque endereço (slug) de página já indexada sem redirecionamento 301."], VERDE, VERDE_C)]
    nome = "Roteiro_Rotinas_Segunda_e_Sexta.pdf"
    doc = SimpleDocTemplate(SAIDA + nome, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Rotinas da semana - comprenolink.net", author="comprenolink.net")
    doc.build(st, onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA + nome)


def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def dobra(linha):
    b = linha.encode("utf-8"); partes = []
    while len(b) > 74:
        corte = 74
        while (b[corte] & 0xC0) == 0x80:
            corte -= 1
        partes.append(b[:corte]); b = b[corte:]
    partes.append(b)
    return "\r\n ".join(p.decode("utf-8") for p in partes)


def agenda():
    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Claude//Rotinas Semanais//PT", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
         "X-WR-CALNAME:Rotinas Turbinar - comprenolink"]

    def ev(uid, ini, fim, título, desc, rrule=None, alarme=10):
        L.extend(["BEGIN:VEVENT", f"UID:{uid}@rotinas-turbinar", "DTSTAMP:20261103T140000Z", f"DTSTART:{ini}", f"DTEND:{fim}",
                  f"SUMMARY:{esc(título)}", f"DESCRIPTION:{esc(desc)}"])
        if rrule:
            L.append("RRULE:" + rrule)
        L.extend(["BEGIN:VALARM", f"TRIGGER:-PT{alarme}M", "ACTION:DISPLAY", f"DESCRIPTION:{esc(título)}", "END:VALARM", "END:VEVENT"])
    ev("segunda-números", "20261109T104500", "20261109T111500", "Reunião com os números (30 min)",
       "Abra a Planilha_Semanal_Turbinar.xlsx e o Painel. Preencha a semana, ache o melhor canal e decida UMA coisa. "
       "Roteiro: 0- Pendencias/1_Pendencias/Roteiro_Rotinas_Segunda_e_Sexta.pdf",
       rrule="FREQ=WEEKLY;BYDAY=MO;UNTIL=20261221T235959")
    ev("sexta-seo", "20261106T140000", "20261106T150000", "Rotina de SEO (1 h)",
       "Search Console > Desempenho: consultas com muitas impressões e poucos cliques. Melhore títulos/descrições, ligue páginas, "
       "rode testar_site_de_novo.bat e peça indexação do que for novo. Roteiro no PDF Roteiro_Rotinas_Segunda_e_Sexta.pdf",
       rrule="FREQ=WEEKLY;BYDAY=FR;UNTIL=20261218T235959")
    for dia, nome in (("20261113", "13/11"), ("20261126", "26/11"), ("20261211", "11/12")):
        ev("guia-" + dia, dia + "T143000", dia + "T150000", f"Guia: conferir anúncios e atualizar a data ({nome})",
           "A cada 15 dias: rodar o painel (verifica anúncios fora do ar), conferir links e só entao trocar 'Atualizado em' no guia. "
           "Peça ao Claude: 'atualizar a data do guia'.")
    L.append("END:VCALENDAR")
    with open(SAIDA + "Agenda_Rotinas_Semanais.ics", "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(dobra(x) for x in L) + "\r\n")
    print("ICS:", SAIDA + "Agenda_Rotinas_Semanais.ics")


if __name__ == "__main__":
    planilha()
    roteiro_pdf()
    # a agenda agora é única: gerar_agenda_nova_pendencias.py
