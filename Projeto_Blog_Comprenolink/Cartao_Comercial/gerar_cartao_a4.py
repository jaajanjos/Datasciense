"""Cartão comercial Compre no Link: folha A4 com 10 cartões 90x50 mm (frente e verso) + marcas de corte."""
import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib.colors import HexColor, white
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.barcode.qr import QrCodeWidget
from reportlab.graphics.shapes import Drawing
from reportlab.graphics import renderPDF

AQUI = os.path.dirname(os.path.abspath(__file__))
LOGO = r"D:\mercado_livre\3- DIVULGAÇÃO_WHATSAPP_INSTAGRAM\09_LOGO\logo_horizontal.png"
pdfmetrics.registerFont(TTFont("Arial", r"C:\Windows\Fonts\arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-Bold", r"C:\Windows\Fonts\arialbd.ttf"))

AZUL, AMARELO, CLARO = HexColor("#111827"), HexColor("#FFD23F"), HexColor("#CBD5E1")
SITE, SITE_URL, INSTA = "comprenolink.net", "https://comprenolink.net", "@compre.no.link"
LARG, ALT = 90 * mm, 50 * mm
COLS, LINS = 2, 5
MX = (A4[0] - COLS * LARG) / 2
MY = (A4[1] - LINS * ALT) / 2


def frente(c, x, y):
    c.setFillColor(AZUL); c.rect(x, y, LARG, ALT, stroke=0, fill=1)
    c.setFillColor(AMARELO); c.rect(x, y, LARG, 2.2 * mm, stroke=0, fill=1)
    lw = 66 * mm
    c.drawImage(LOGO, x + (LARG - lw) / 2, y + ALT - 24 * mm, lw, lw * 480 / 1600, mask="auto")
    c.setFillColor(AMARELO); c.setFont("Arial-Bold", 10.5)
    c.drawCentredString(x + LARG / 2, y + 19 * mm, "Achados do Mercado Livre por categoria")
    c.setFillColor(white); c.setFont("Arial", 8.5)
    c.drawCentredString(x + LARG / 2, y + 13.2 * mm, "Black Friday, ofertas e lançamentos selecionados")
    c.setFont("Arial-Bold", 9.5)
    c.drawCentredString(x + LARG / 2, y + 6.4 * mm, f"{SITE}   •   {INSTA}")


def verso(c, x, y):
    c.setFillColor(AMARELO); c.rect(x, y, LARG, ALT, stroke=0, fill=1)
    c.setFillColor(AZUL); c.rect(x, y, LARG, 2.2 * mm, stroke=0, fill=1)
    q = 30 * mm
    c.setFillColor(white); c.roundRect(x + 7 * mm, y + (ALT - q) / 2, q, q, 2 * mm, stroke=0, fill=1)
    w = QrCodeWidget(SITE_URL); b = w.getBounds()
    s = (q - 4 * mm) / (b[2] - b[0])
    d = Drawing(q - 4 * mm, q - 4 * mm, transform=[s, 0, 0, s, 0, 0]); d.add(w)
    renderPDF.draw(d, c, x + 9 * mm, y + (ALT - q) / 2 + 2 * mm)
    tx = x + 7 * mm + q + 6 * mm
    c.setFillColor(AZUL)
    c.setFont("Arial-Bold", 12.5); c.drawString(tx, y + 35 * mm, "Quer o link?")
    c.setFont("Arial-Bold", 10); c.drawString(tx, y + 28.5 * mm, "Comente BLACK")
    c.setFont("Arial", 8.3)
    c.drawString(tx, y + 23.3 * mm, "no post que eu te mando")
    c.drawString(tx, y + 19.3 * mm, "no Direct, ou aponte a")
    c.drawString(tx, y + 15.3 * mm, "câmera para o QR Code.")
    c.setFont("Arial-Bold", 9); c.drawString(tx, y + 8 * mm, INSTA)
    c.setFont("Arial", 5.8); c.drawString(x + 7 * mm, y + 4.2 * mm, "Publi: contém link de afiliado. Preços e estoque podem mudar no Mercado Livre.")


def marcas(c):
    c.setStrokeColor(HexColor("#888888")); c.setLineWidth(0.3)
    for i in range(COLS + 1):
        x = MX + i * LARG
        c.line(x, MY - 6 * mm, x, MY - 1.5 * mm); c.line(x, MY + LINS * ALT + 1.5 * mm, x, MY + LINS * ALT + 6 * mm)
    for j in range(LINS + 1):
        y = MY + j * ALT
        c.line(MX - 6 * mm, y, MX - 1.5 * mm, y); c.line(MX + COLS * LARG + 1.5 * mm, y, MX + COLS * LARG + 6 * mm, y)


def pagina(c, desenhar, titulo, espelhar):
    for j in range(LINS):
        for i in range(COLS):
            ii = (COLS - 1 - i) if espelhar else i  # verso espelhado para casar na impressão frente e verso
            desenhar(c, MX + ii * LARG, MY + j * ALT)
    marcas(c)
    c.setFillColor(HexColor("#888888")); c.setFont("Arial", 7)
    c.drawCentredString(A4[0] / 2, 8 * mm, titulo)
    c.showPage()


def main():
    saida = os.path.join(AQUI, "Cartao_Comercial_A4_ComprenoLink.pdf")
    c = canvas.Canvas(saida, pagesize=A4)
    c.setTitle("Cartão comercial Compre no Link (A4, 10 por folha)")
    pagina(c, frente, "FRENTE  |  10 cartões 90 x 50 mm  |  cortar nas marcas  |  imprimir em 100% (sem ajustar à página)", False)
    pagina(c, verso, "VERSO  |  imprimir frente e verso com 'virar na borda longa'  |  100% (sem ajustar à página)", True)
    c.save(); print(saida)


if __name__ == "__main__":
    main()
