# -*- coding: utf-8 -*-
"""Quadro-resumo de 1 página (A4 deitado) do plano Turbinar: linha do tempo nov–dez 2026 com as 3 opções.
Gera Quadro_Resumo_Turbinar_2026.pdf e .png nesta pasta.  Rodar:  python -X utf8 gerar_quadro_resumo.py
"""
import os
from datetime import date, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from gerar_pdf_plano_turbinar import (AMARELO, AZUL_C, CINZA, CLARO, COMISSAO_MEDIA, ESCURO, LARANJA, LARANJA_C,
                                      VERDE, VERDE_C, brl)

PASTA = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(PASTA, "Quadro_Resumo_Turbinar_2026.pdf")
W, H = landscape(A4)
INI, FIM = date(2026, 11, 2), date(2026, 12, 21)
ROXO, ROXO_C = colors.HexColor("#6D28D9"), colors.HexColor("#EDE9FE")

# (rótulo, início, fim, R$/dia, cor)
TESTE = ("Teste", date(2026, 11, 16), date(2026, 11, 18), 10, VERDE)
BF = ("Black Friday", date(2026, 11, 21), date(2026, 11, 27), 15, LARANJA)
NATAL = ("Natal", date(2026, 12, 5), date(2026, 12, 14), 10, ROXO)
OPCOES = [("1. Gasto mínimo", [TESTE], VERDE_C), ("2. Teste + Black Friday", [TESTE, BF], LARANJA_C),
          ("3. Plano completo", [TESTE, BF, NATAL], ROXO_C)]
MARCOS = [(date(2026, 11, 5), "Termos ML"), (date(2026, 11, 15), "Conta de anúncios"), (date(2026, 11, 19), "Avaliação 1"),
          (date(2026, 11, 30), "Avaliação 2"), (date(2026, 12, 21), "Relatório final")]


def total(fases):
    return sum(((f - i).days + 1) * v for _, i, f, v, _ in fases)


def main():
    c = canvas.Canvas(SAIDA, pagesize=(W, H))
    c.setTitle("Quadro-resumo Turbinar 2026")
    # cabeçalho
    c.setFillColor(ESCURO)
    c.rect(0, H - 2.4 * cm, W, 2.4 * cm, fill=1, stroke=0)
    c.setFillColor(AMARELO)
    c.rect(0, H - 2.55 * cm, W, 0.15 * cm, fill=1, stroke=0)
    c.setFont("Arial-B", 19)
    c.drawString(1.5 * cm, H - 1.45 * cm, "Quadro-resumo: Turbinar Instagram 2026")
    c.setFillColor(colors.white)
    c.setFont("Arial", 10.5)
    c.drawRightString(W - 1.5 * cm, H - 1.45 * cm, "@compre.no.link  •  quando fazer e quanto custa cada opção")

    # linha do tempo
    x0, x1 = 6.3 * cm, W - 1.2 * cm
    ndias = (FIM - INI).days + 1
    px = (x1 - x0) / ndias
    X = lambda d: x0 + (d - INI).days * px
    topo = H - 3.4 * cm
    # meses
    for nome, a, b in (("NOVEMBRO 2026", INI, date(2026, 11, 30)), ("DEZEMBRO 2026", date(2026, 12, 1), FIM)):
        c.setFillColor(ESCURO)
        c.rect(X(a), topo - 0.55 * cm, X(b) + px - X(a) - 2, 0.55 * cm, fill=1, stroke=0)
        c.setFillColor(colors.white)
        c.setFont("Arial-B", 9)
        c.drawCentredString((X(a) + X(b) + px) / 2, topo - 0.4 * cm, nome)
    # dias
    yd = topo - 1.05 * cm
    sem = "STQQSSD"
    for k in range(ndias):
        d = INI + timedelta(days=k)
        c.setFillColor(CLARO if d.weekday() < 5 else colors.HexColor("#E5E7EB"))
        c.rect(X(d), yd - 0.05 * cm, px - 1, 0.5 * cm, fill=1, stroke=0)
        c.setFillColor(ESCURO if d.weekday() < 5 else CINZA)
        c.setFont("Arial-B" if d.day in (1, 16, 21, 27, 5, 14) else "Arial", 6.5)
        c.drawCentredString(X(d) + px / 2, yd + 0.13 * cm, str(d.day))
        c.setFont("Arial", 5.5)
        c.setFillColor(CINZA)
        c.drawCentredString(X(d) + px / 2, yd - 0.3 * cm, sem[d.weekday()])
    # linhas das opções
    alt, y = 2.55 * cm, yd - 0.75 * cm
    for nome, fases, fundo in OPCOES:
        y -= alt
        c.setFillColor(fundo)
        c.roundRect(0.9 * cm, y, x1 - 0.9 * cm + 0.2 * cm, alt - 0.2 * cm, 6, fill=1, stroke=0)
        c.setFillColor(ESCURO)
        c.setFont("Arial-B", 10.5)
        c.drawString(1.2 * cm, y + alt - 0.9 * cm, nome)
        c.setFont("Arial-B", 17)
        c.drawString(1.2 * cm, y + 0.45 * cm, brl(total(fases)))
        for rot, i, f, v, cor in fases:
            c.setFillColor(cor)
            c.roundRect(X(i), y + 0.25 * cm, X(f) + px - X(i) - 2, alt - 0.7 * cm, 4, fill=1, stroke=0)
            c.setFillColor(colors.white)
            dias = (f - i).days + 1
            c.setFont("Arial-B", 8)
            c.drawCentredString((X(i) + X(f) + px) / 2, y + alt - 1.05 * cm, rot)
            c.setFont("Arial", 7)
            leg = f"{dias} dias × {brl(v).replace(',00', '')}" if dias >= 5 else brl(dias * v).replace(',00', '')  # barra estreita: só o total
            c.drawCentredString((X(i) + X(f) + px) / 2, y + 0.55 * cm, leg)
    # marcos (sem gasto)
    ym = y - 0.25 * cm
    for k, (d, rot) in enumerate(MARCOS):
        xm = X(d) + px / 2
        dy = 0.38 * cm if k % 2 == 0 else 0.78 * cm  # alterna a altura para os rótulos não se encostarem
        c.setStrokeColor(CINZA)
        c.setDash(2, 2)
        c.line(xm, ym, xm, yd - 0.45 * cm)
        c.setDash()
        c.setFillColor(ESCURO)
        c.circle(xm, ym, 3, fill=1, stroke=0)
        c.setFont("Arial", 6.8)
        c.drawCentredString(min(xm, x1 - 1.3 * cm), ym - dy, f"{d.day:02d}/{d.month:02d} {rot}")

    # tabela comparativa
    ty = ym - 1.7 * cm
    cols = [("Opção", 5.3), ("Quando há gasto", 6.2), ("Dias pagos", 2.4), ("Total", 2.9), ("Vendas p/ empatar*", 3.5),
            ("Condição para acontecer", 6.9)]
    linhas = [("1. Gasto mínimo", "16 a 18/nov", "3", "R$ 30,00", "≈ 4", "Termos do ML permitirem anúncio pago"),
              ("2. Teste + Black Friday", "16/nov a 27/nov", "10", "R$ 135,00", "≈ 15", "Teste no VERDE em 19/11"),
              ("3. Plano completo", "16/nov a 14/dez", "20", "R$ 235,00", "≈ 26", "Black Friday se pagar (avaliação 30/11)")]
    fundos = [VERDE_C, LARANJA_C, ROXO_C]
    rh, xs = 0.75 * cm, 0.9 * cm
    c.setFillColor(ESCURO)
    c.rect(xs, ty, sum(w for _, w in cols) * cm, rh, fill=1, stroke=0)
    x = xs
    c.setFont("Arial-B", 8.5)
    c.setFillColor(colors.white)
    for t, w in cols:
        c.drawString(x + 0.15 * cm, ty + 0.2 * cm, t)
        x += w * cm
    for k, l in enumerate(linhas):
        yy = ty - (k + 1) * rh
        c.setFillColor(fundos[k])
        c.rect(xs, yy, sum(w for _, w in cols) * cm, rh, fill=1, stroke=0)
        x = xs
        for j, (t, w) in enumerate(zip(l, [w for _, w in cols])):
            c.setFillColor(ESCURO)
            c.setFont("Arial-B" if j in (0, 3) else "Arial", 8.5)
            c.drawString(x + 0.15 * cm, yy + 0.26 * cm, t)
            x += w * cm
    c.setFont("Arial", 7.5)
    c.setFillColor(CINZA)
    nota = (f"* comissão média {brl(COMISSAO_MEDIA)} por venda (R$ 172 ÷ 19 vendas, ML Afiliados). Barras coloridas = dias com gasto; "
            "pontos = datas sem gasto (preparação e avaliações). Sem preço no anúncio • pagamento sempre feito pelo sócio pagador.")
    c.drawString(xs, ty - 4 * rh - 0.15 * cm, nota)
    c.drawRightString(W - 1.2 * cm, 0.7 * cm, "Detalhes completos: Plano_Turbinar_Instagram_2026.pdf  •  27/10/2026")
    c.showPage()
    c.save()
    import pypdfium2 as p
    p.PdfDocument(SAIDA)[0].render(scale=2.2).to_pil().save(SAIDA[:-4] + ".png")
    print("Quadro:", SAIDA)


if __name__ == "__main__":
    main()
