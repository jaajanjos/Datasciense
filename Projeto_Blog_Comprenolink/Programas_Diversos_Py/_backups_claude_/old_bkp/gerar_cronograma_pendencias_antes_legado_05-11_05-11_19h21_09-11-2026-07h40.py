# -*- coding: utf-8 -*-
"""Cronograma de pendências do blog comprenolink.net (PDF A4 deitado, para imprimir e marcar).
Edite a lista PEND abaixo e rode:  python -X utf8 gerar_cronograma_pendencias.py
"""
import os
import sys
from datetime import date

PASTA = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, r"D:\mercado_livre\plano_turbinar_anuncio_instagram")
from gerar_pdf_plano_turbinar import (AMARELO, AZUL_C, CINZA, CLARO, ESCURO, LARANJA, LARANJA_C, S, VERDE,  # noqa: E402
                                      VERDE_C, VERMELHO, VERMELHO_C)
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4, landscape  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle  # noqa: E402

HOJE = date(2026, 10, 27)
SAIDA = os.path.join(PASTA, f"Cronograma_Pendencias_{HOJE:%Y-%m-%d}.pdf")
W, H = landscape(A4)
LARG = W - 3 * cm
ROXO_C = colors.HexColor("#EDE9FE")
SEM = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]

# grupo, data (date ou None), pendência, quem, como / onde
PEND = [
    ("agora", HOJE, "Fechar o PDF do plano Turbinar no leitor (para eu incluir o quadro-resumo)", "Você",
     "Fechar Plano_Turbinar_Instagram_2026.pdf e avisar \"fechei\""),
    ("agora", HOJE, "Cadastrar 1 item novo no catálogo do WhatsApp Business: Bebê & Maternidade", "Você",
     "06_CATALOGO_WHATSAPP\\CATEGORIAS → CAT-bebe-e-maternidade (foto + texto)"),
    ("semana", date(2026, 11, 1), "WhatsApp Business: perfil, catálogo, respostas rápidas e Canal + enviar link do Canal", "Você",
     "08_PASSO_A_PASSO_WHATSAPP_NO_CELULAR.pdf; mandar o link do Canal ao Claude"),
    ("semana", date(2026, 11, 2), "Início dos posts: 18:45 avisar \"post do dia\"; 19:00 post (Claude); 19:10 story (celular)", "Você + Claude",
     "07_PACOTE_DO_DIA\\2026-11-02_seg • lembrete no calendário do Instagram"),
    ("semana", date(2026, 11, 5), "Reunião com o sócio: aprovar valor máximo do Turbinar e quem paga", "Você + sócio",
     "Plano_Turbinar_Instagram_2026.pdf – página de aprovação"),
    ("semana", date(2026, 11, 5), "Ler os termos do ML Afiliados: anúncio pago é permitido?", "Você",
     "Painel ML Afiliados → termos/regras do programa"),
    ("semana", date(2026, 11, 5), "Republicar o blog das máquinas (Google Sites)", "Você",
     "Manutenção_Blog\\1_PROGRAMAS\\Blog_Maquinas"),
    ("nov", date(2026, 11, 6), "Criar os Destaques do Instagram (Black Friday, Categorias, Como comprar)", "Você (celular)",
     "Pedir o passo a passo ao Claude"),
    ("nov", date(2026, 11, 9), "Decisões: QCY Shopee, nota antiga no painel das máquinas, divulgação de longo prazo", "Você",
     "Conversar com o Claude"),
    ("nov", date(2026, 11, 15), "Criar a conta de anúncios Meta + forma de pagamento (se o Turbinar for aprovado)", "Sócio pagador",
     "Instagram → Turbinar / Central de anúncios"),
    ("nov", date(2026, 11, 16), "Turbinar – TESTE: 3 dias × R$ 10 = R$ 30 (16 a 18/11)", "Sócio pagador",
     "Plano Turbinar – Fase 1"),
    ("nov", date(2026, 11, 19), "Avaliação 1 do Turbinar (semáforo: segue, ajusta ou para)", "Sócios + Claude",
     "Prints dos insights + painel do blog"),
    ("nov", date(2026, 11, 21), "Turbinar – BLACK FRIDAY: 7 dias × R$ 15 = R$ 105 (21 a 27/11), se o teste deu verde", "Sócio pagador",
     "Plano Turbinar – Fase 2"),
    ("nov", date(2026, 11, 30), "Avaliação 2: vendas da Black Friday ≥ gasto? Decide o Natal", "Sócios + Claude",
     "ML Afiliados (exportar CSV) + painel"),
    ("dez", date(2026, 12, 1), "Conferir troca automática para o Natal no blog + pedir indexação de /presentes-de-natal/", "Você + Claude",
     "Search Console → Inspeção de URL"),
    ("dez", date(2026, 12, 1), "Instagram: link 1 da bio → comprenolink.net/presentes-de-natal + bio de dezembro", "Você (link) + Claude (bio)",
     "Editar perfil → Links (celular)"),
    ("dez", date(2026, 12, 5), "Turbinar – NATAL: 10 dias × R$ 10 = R$ 100 (05 a 14/12), se a BF se pagou", "Sócio pagador",
     "Plano Turbinar – Fase 3"),
    ("dez", date(2026, 12, 21), "Relatório final do Turbinar: gasto × vendas × comissão", "Claude",
     "Pasta plano_turbinar_anuncio_instagram"),
    ("dez", date(2026, 12, 26), "Instagram: link 1 da bio volta para comprenolink.net", "Você (celular)",
     "Editar perfil → Links"),
    ("opc", None, "Pedir indexação de /bebe-e-maternidade/ no Search Console", "Você ou Claude", "Opcional – o sitemap já cuida"),
    ("opc", None, "Reels prontos a partir das artes de cada dia", "Claude", "Aguardando seu \"sim\""),
    ("opc", None, "Botão \"Siga no Instagram\" no rodapé e no Contato do blog (com backup)", "Claude", "Aguardando seu \"sim\""),
    ("opc", None, "Outlook com compre.no.link26@gmail.com", "Você + Claude", "Adiado – criar nova senha de app"),
    ("opc", None, "Corrigir no 00_LEIA-ME_WHATSAPP o caminho do OneDrive (C:\\Users\\kkk → E:\\OneDrive)", "Claude",
     "Aguardando confirmar que o OneDrive certo é o E:"),
]
GRUPOS = {
    "agora": ("AGORA (hoje, 27/10)", VERMELHO, VERMELHO_C),
    "semana": ("ESTA SEMANA (até 05/11)", LARANJA, LARANJA_C),
    "nov": ("NOVEMBRO", VERDE, VERDE_C),
    "dez": ("DEZEMBRO", colors.HexColor("#6D28D9"), ROXO_C),
    "opc": ("OPCIONAIS / ADIADOS (sem data)", CINZA, CLARO),
}


def rodape(c, doc):
    c.saveState()
    c.setFillColor(ESCURO)
    c.rect(0, H - 1.9 * cm, W, 1.9 * cm, fill=1, stroke=0)
    c.setFillColor(AMARELO)
    c.rect(0, H - 2.02 * cm, W, 0.12 * cm, fill=1, stroke=0)
    c.setFont("Arial-B", 16)
    c.drawString(1.5 * cm, H - 1.2 * cm, "Cronograma de pendências – comprenolink.net")
    c.setFont("Arial", 10)
    c.setFillColor(colors.white)
    c.drawRightString(W - 1.5 * cm, H - 1.2 * cm, f"atualizado em {HOJE:%d/%m/%Y}  •  marque [X] quando concluir")
    c.setFont("Arial", 8)
    c.setFillColor(CINZA)
    c.drawString(1.5 * cm, 0.9 * cm, "Blog comprenolink.net  •  Instagram @compre.no.link  •  WhatsApp (11) 99495-9657")
    c.drawRightString(W - 1.5 * cm, 0.9 * cm, f"Página {doc.page}")
    c.restoreState()


def p(t, est="cel"):
    return Paragraph(t, S[est])


def resumo():
    cont = {g: sum(1 for x in PEND if x[0] == g) for g in GRUPOS}
    cel = []
    for g, (rot, cor, fundo) in GRUPOS.items():
        cel.append(Paragraph(f"<font size=18><b>{cont[g]}</b></font><br/><font size=8>{rot}</font>",
                             S["bigl"].clone("r", textColor=cor, leading=20)))
    t = Table([cel], colWidths=[LARG / len(cel)] * len(cel))
    st = [("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D1D5DB")), ("TOPPADDING", (0, 0), (-1, -1), 8),
          ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]
    for i, (_, _, fundo) in enumerate(GRUPOS.values()):
        st.append(("BACKGROUND", (i, 0), (i, 0), fundo))
    t.setStyle(TableStyle(st))
    return t


def tabela_grupo(g):
    rot, cor, fundo = GRUPOS[g]
    linhas = [[p(f"<b>{rot}</b>", "cab"), "", "", "", "", ""],
              [p("<b>OK</b>"), p("<b>Data</b>"), p("<b>Pendência</b>"), p("<b>Quem</b>"), p("<b>Como / onde</b>"), p("<b>Feito em</b>")]]
    for _, d, txt, quem, como in [x for x in PEND if x[0] == g]:
        quando = f"<b>{d:%d/%m}</b> {SEM[d.weekday()]}" if d else "–"
        linhas.append([p("[   ]"), p(quando), p(txt), p(quem), p(como, "pq"), p("___/___")])
    t = Table(linhas, colWidths=[LARG * w for w in (0.05, 0.09, 0.40, 0.13, 0.25, 0.08)], repeatRows=2)
    st = [("SPAN", (0, 0), (-1, 0)), ("BACKGROUND", (0, 0), (-1, 0), cor), ("BACKGROUND", (0, 1), (-1, 1), fundo),
          ("GRID", (0, 1), (-1, -1), 0.4, colors.HexColor("#D1D5DB")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
          ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5)]
    for r in range(2, len(linhas)):
        if r % 2 == 1:
            st.append(("BACKGROUND", (0, r), (-1, r), CLARO))
    t.setStyle(TableStyle(st))
    return t


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=(W, H), leftMargin=1.5 * cm, rightMargin=1.5 * cm, topMargin=2.5 * cm,
                            bottomMargin=1.5 * cm, title="Cronograma de pendências comprenolink", author="comprenolink.net")
    st = [resumo(), Spacer(1, 8),
          Paragraph("Ordem: primeiro o que vence antes. Itens do Turbinar só acontecem se o plano for aprovado na reunião "
                    "e o resultado da fase anterior ficar no verde. Lembretes do Instagram já estão no "
                    "12_CALENDARIO_INSTAGRAM.ics.", S["pq"]), Spacer(1, 6)]
    for g in GRUPOS:
        st += [tabela_grupo(g), Spacer(1, 10)]
    doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
