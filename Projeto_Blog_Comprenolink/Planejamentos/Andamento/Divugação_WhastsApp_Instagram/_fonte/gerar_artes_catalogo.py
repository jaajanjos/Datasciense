# -*- coding: utf-8 -*-
"""
Gera, a partir dos produtos do blog e do calendário de divulgação:
  06_CATALOGO_WHATSAPP\\  fotos quadradas + CATALOGO_WHATSAPP.xlsx (o que cadastrar no catálogo do WhatsApp Business)
  07_PACOTE_DO_DIA\\AAAA-MM-DD_dia\\  feed.png, story.png, status.png e 1_TEXTOS_DO_DIA.txt (copiar e publicar)
Sem preço nas artes e nos textos. Rodar: python -X utf8 _fonte\\gerar_artes_catalogo.py
"""
import io
import os
import sys
import textwrap
import urllib.request
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dados_divulgacao as dd  # noqa: E402
from PIL import Image, ImageDraw, ImageFont, ImageOps  # noqa: E402

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CACHE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache_fotos")
CATALOGO = os.path.join(PASTA, "06_CATALOGO_WHATSAPP")
PACOTE = os.path.join(PASTA, "07_PACOTE_DO_DIA")
F = r"C:\Windows\Fonts"
fonte = lambda nome, tam: ImageFont.truetype(os.path.join(F, nome), tam)
ESCURO, AMARELO, BRANCO, CINZA = (17, 24, 39), (255, 213, 74), (255, 255, 255), (203, 213, 225)
VERMELHO_NATAL, VERDE_NATAL = (190, 30, 45), (22, 101, 52)
DIAS = ["seg", "ter", "qua", "qui", "sex", "sab", "dom"]


def foto(x):
    os.makedirs(CACHE, exist_ok=True)
    arq = os.path.join(CACHE, f"item{x['n']}.png")
    if not os.path.exists(arq):
        req = urllib.request.Request(x["imagem"], headers={"User-Agent": "Mozilla/5.0"})
        im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert("RGBA")
        fundo = Image.new("RGBA", im.size, BRANCO + (255,))
        Image.alpha_composite(fundo, im).convert("RGB").save(arq)
    return Image.open(arq).convert("RGB")


def quebra(draw, texto, fnt, largura):
    linhas, atual = [], ""
    for p in texto.split():
        t = (atual + " " + p).strip()
        if draw.textlength(t, font=fnt) <= largura:
            atual = t
        else:
            linhas.append(atual)
            atual = p
    return linhas + [atual] if atual else linhas


def cartao_foto(im, lado):
    im = ImageOps.contain(im, (lado - 60, lado - 60))
    c = Image.new("RGB", (lado, lado), BRANCO)
    c.paste(im, ((lado - im.width) // 2, (lado - im.height) // 2))
    m = Image.new("L", (lado, lado), 0)
    ImageDraw.Draw(m).rounded_rectangle([0, 0, lado, lado], 40, fill=255)
    return c, m


def arte(x, campanha, formato):
    W, H = (1080, 1920) if formato in ("story", "status") else (1080, 1350)
    natal = campanha == "natal"
    img = Image.new("RGB", (W, H), ESCURO)
    d = ImageDraw.Draw(img)
    # faixa do topo
    faixa = 190 if H > 1400 else 150
    d.rectangle([0, 0, W, faixa], fill=VERMELHO_NATAL if natal else AMARELO)
    titulo = "PRESENTES DE NATAL" if natal else "BLACK FRIDAY 2026"
    ft = fonte("ariblk.ttf", 78 if H > 1400 else 70)
    d.text((W / 2, faixa / 2), titulo, font=ft, fill=BRANCO if natal else ESCURO, anchor="mm")
    # foto
    lado = 820 if H > 1400 else 600
    c, m = cartao_foto(foto(x), lado)
    y = faixa + (90 if H > 1400 else 50)
    img.paste(c, ((W - lado) // 2, y), m)
    y += lado + (60 if H > 1400 else 35)
    # selo
    fs = fonte("arialbd.ttf", 40)
    selo = x["selo"].upper()
    tw = d.textlength(selo, font=fs)
    d.rounded_rectangle([(W - tw) / 2 - 30, y, (W + tw) / 2 + 30, y + 70], 35, fill=VERDE_NATAL if natal else AMARELO)
    d.text((W / 2, y + 35), selo, font=fs, fill=BRANCO if natal else ESCURO, anchor="mm")
    y += 100
    # nome
    fn = fonte("arialbd.ttf", 64 if H > 1400 else 56)
    for linha in quebra(d, x["nome"], fn, W - 120)[:3]:
        d.text((W / 2, y), linha, font=fn, fill=BRANCO, anchor="ma")
        y += fn.size + 12
    # chamada
    chamada = {"feed": "Link na bio  •  Comente " + dd.PALAVRA[campanha],
               "story": "Toque no link abaixo", "status": "Link na mensagem"}[formato]
    fc = fonte("arialbd.ttf", 46)
    yb = max(y + 50, H - (440 if formato == "story" else 190))
    d.text((W / 2, yb), chamada, font=fc, fill=AMARELO, anchor="mm")
    d.text((W / 2, yb + 70), "Confira o valor do dia no Mercado Livre", font=fonte("arial.ttf", 34), fill=CINZA, anchor="mm")
    d.text((W / 2, H - 60), "comprenolink.net  •  link de afiliado", font=fonte("arial.ttf", 30), fill=CINZA, anchor="mm")
    if formato == "story":  # espaço para o adesivo de link
        d.rounded_rectangle([W / 2 - 230, H - 250, W / 2 + 230, H - 150], 50, outline=AMARELO, width=4)
        d.text((W / 2, H - 200), "adesivo VER NO BLOG aqui", font=fonte("arial.ttf", 30), fill=CINZA, anchor="mm")
    return img


def arte_campanha(campanha, texto_grande, texto_pequeno):
    W, H = 1080, 1920
    natal = campanha == "natal"
    img = Image.new("RGB", (W, H), ESCURO)
    d = ImageDraw.Draw(img)
    d.rectangle([0, 0, W, 260], fill=VERMELHO_NATAL if natal else AMARELO)
    d.text((W / 2, 130), "PRESENTES DE NATAL" if natal else "BLACK FRIDAY 2026", font=fonte("ariblk.ttf", 80),
           fill=BRANCO if natal else ESCURO, anchor="mm")
    y = 420
    fg = fonte("ariblk.ttf", 92)
    for linha in quebra(d, texto_grande, fg, W - 120):
        d.text((W / 2, y), linha, font=fg, fill=BRANCO, anchor="ma")
        y += 110
    y += 40
    ff = fonte("arialbd.ttf", 48)
    for linha in quebra(d, texto_pequeno, ff, W - 160):
        d.text((W / 2, y), linha, font=ff, fill=AMARELO, anchor="ma")
        y += 64
    top = dd.carrega_produtos.cache["top"][campanha][:4] if hasattr(dd.carrega_produtos, "cache") else []
    lado, x0, ytop = 440, 70, y + 80
    for k, x in enumerate(top):
        c, m = cartao_foto(foto(x), lado)
        img.paste(c, (x0 + (k % 2) * (lado + 60), ytop + (k // 2) * (lado + 40)), m)
    d.text((W / 2, H - 60), "comprenolink.net  •  link de afiliado", font=fonte("arial.ttf", 30), fill=CINZA, anchor="mm")
    return img


def gera_catalogo(dados):
    from openpyxl import Workbook
    from openpyxl.styles import Alignment, Font, PatternFill
    os.makedirs(os.path.join(CATALOGO, "fotos"), exist_ok=True)
    vistos, linhas = set(), []
    for camp in ("black_friday", "natal"):
        for x in dados["top"][camp]:
            colecao = "Black Friday" if camp == "black_friday" else "Presentes de Natal"
            if x["n"] in vistos:
                for l in linhas:
                    if l[0] == f"CNL-{x['n']:03d}":
                        l[6] += " + " + colecao
                continue
            vistos.add(x["n"])
            c, m = cartao_foto(foto(x), 1080)
            arq = f"CNL-{x['n']:03d}_{dd.slug(x['nome'])}.jpg"
            c.save(os.path.join(CATALOGO, "fotos", arq), quality=90)
            desc = x["desc"] + "\n\n" + "\n".join(f"✅ {b}" for b in x["beneficios"][:4]) + \
                "\n\nConfira o valor do dia no Mercado Livre pelo link. Link de afiliado: posso ganhar comissão, sem custo extra para você."
            link = dd.utm(dd.GUIA, "whatsapp", "catalogo", camp, f"cnl_{x['n']:03d}", f"#item-{x['n']}")
            linhas.append([f"CNL-{x['n']:03d}", x["nome"], "(deixe em branco)", desc, link, arq, colecao])
    wb = Workbook()
    ws = wb.active
    ws.title = "Catálogo"
    ws.append(["Código do item", "Nome do item", "Preço", "Descrição", "Link do site", "Foto (pasta fotos)", "Coleção", "Cadastrado (S/N)"])
    for l in linhas:
        ws.append(l + ["N"])
    for c in ws[1]:
        c.fill, c.font = PatternFill("solid", fgColor="111827"), Font(bold=True, color="FFFFFF")
    for i, w in enumerate([12, 40, 16, 70, 60, 40, 28, 12], 1):
        ws.column_dimensions[chr(64 + i)].width = w
    for row in ws.iter_rows(min_row=2):
        for c in row:
            c.alignment = Alignment(wrap_text=True, vertical="top")
    ws.freeze_panes = "A2"
    wb.save(os.path.join(CATALOGO, "CATALOGO_WHATSAPP.xlsx"))
    txt = ["TEXTOS DO CATÁLOGO DO WHATSAPP BUSINESS – copiar e colar no celular",
           "Para cada produto: Adicionar novo item → foto (pasta fotos) → NOME → Preço EM BRANCO → DESCRIÇÃO → Mais campos: LINK e CÓDIGO.", ""]
    for cod, nome, _, desc, link, arq, colecao in linhas:
        txt += ["=" * 60, f"CÓDIGO: {cod}      FOTO: {arq}      COLEÇÃO: {colecao}", "=" * 60,
                "NOME:", nome, "", "DESCRIÇÃO:", desc, "", "LINK:", link, ""]
    with open(os.path.join(CATALOGO, "CATALOGO_TEXTOS.txt"), "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write("\n".join(txt))
    return len(linhas)


def gera_pacotes(dados):
    por_dia = defaultdict(list)
    for l in dd.calendario(dados):
        por_dia[l["data"]].append(l)
    itens = {x["n"]: x for x in dados["itens"]}
    feitas = 0
    for dia, ls in sorted(por_dia.items()):
        pasta = os.path.join(PACOTE, f"{dia:%Y-%m-%d}_{DIAS[dia.weekday()]}")
        os.makedirs(pasta, exist_ok=True)
        camp = ls[0]["campanha"]
        txt = [f"PACOTE DO DIA {dia:%d/%m/%Y} ({DIAS[dia.weekday()]}) – {'Black Friday' if camp == 'black_friday' else 'Natal'}",
               "Ordem: abra cada bloco, copie o texto e publique. Imagens nesta pasta.", ""]
        produto = next((itens[l["item"]] for l in ls if l["item"]), None)
        if produto:
            for formato in ("feed", "story", "status"):
                arte(produto, camp, formato).save(os.path.join(pasta, f"{formato}.png"))
                feitas += 1
        for l in ls:
            if not l["item"] and l["formato"] != "Conferência":
                grande = {"Lembrete forte": "AMANHÃ É BLACK FRIDAY", "Disparo do dia D": "É HOJE!", "Cyber Monday": "ÚLTIMO DIA"}.get(
                    l["formato"], "LISTA PRONTA" if camp == "black_friday" else "IDEIAS DE PRESENTE")
                nome = f"campanha_{l['hora'].replace(':', 'h')}.png"
                arte_campanha(camp, grande, "Top 10 e ofertas por categoria no blog").save(os.path.join(pasta, nome))
                feitas += 1
            imagem = {"Post no feed (foto/carrossel)": "feed.png", "Story com adesivo de link": "story.png", "Status": "status.png",
                      "Canal": "feed.png"}.get(l["formato"], f"campanha_{l['hora'].replace(':', 'h')}.png" if not l["item"] else "")
            if l["formato"] == "Conferência":
                imagem = "-"
            txt += ["=" * 60, f"{l['hora']}  {l['canal']} – {l['formato']}", f"Imagem: {imagem}", "=" * 60, l["texto"], ""]
            if l["link"].startswith("http") and l["formato"] in ("Story com adesivo de link",):
                txt += ["Link para o adesivo:", l["link"], ""]
            if l["obs"]:
                txt += ["Obs.: " + l["obs"], ""]
        with open(os.path.join(pasta, "1_TEXTOS_DO_DIA.txt"), "w", encoding="utf-8-sig", newline="\r\n") as f:
            f.write("\n".join(txt))
    return len(por_dia), feitas


def main():
    dados = dd.carrega_produtos()
    dd.carrega_produtos.cache = dados
    n = gera_catalogo(dados)
    dias, artes = gera_pacotes(dados)
    print(f"Catálogo: {n} produtos | Pacote do dia: {dias} dias, {artes} artes")
    import gerar_reels  # Reels saem junto com o pacote do dia
    print(f"Reels: {len(gerar_reels.todos())} vídeos")


if __name__ == "__main__":
    main()
