"""
Gera as ARTES prontas para postar (PNG) a partir do config_instagram.json:
  - Carrossel: slides 1080x1350 (capa, 1 slide por produto/dica, slide final com CTA)
  - Reels: capa 1080x1920 (use como "capa" ao publicar o Reels)
  - Story: 1080x1920 com espaço livre para o adesivo de LINK

Foto opcional do produto: coloque em fotos_produtos\\<id>.jpg ou .png
(o id está em produtos.json — ex.: fotos_produtos\\fone_jbl.png). Sem foto, a arte sai só com texto.

Uso:
    python 2_gerar_artes.py            # todos os posts
    python 2_gerar_artes.py --post 3   # só o post #03
"""
import argparse
import json
import os
import sys

from PIL import Image, ImageDraw, ImageFont

PASTA = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
CONFIG_IG = os.path.join(PASTA, "config_instagram.json")
PRODUTOS = os.path.join(PASTA, "produtos.json")
FOTOS = os.path.join(PASTA, "fotos_produtos")
PASTA_ARTES = os.path.join(PASTA, "saida", "artes")

AMARELO, AZUL, BRANCO, CINZA = (255, 230, 0), (45, 50, 119), (255, 255, 255), (225, 228, 240)
FONTES = os.path.join(os.environ.get("WINDIR", r"C:\Windows"), "Fonts")


def fonte(tam, negrito=True):
    for nome in (["segoeuib.ttf", "arialbd.ttf"] if negrito else ["segoeui.ttf", "arial.ttf"]):
        try:
            return ImageFont.truetype(os.path.join(FONTES, nome), tam)
        except OSError:
            pass
    return ImageFont.load_default(tam)


def quebrar(draw, texto, f, largura):
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if draw.textlength(teste, font=f) <= largura:
            atual = teste
        else:
            if atual:
                linhas.append(atual)
            atual = palavra
    if atual:
        linhas.append(atual)
    return linhas


def texto_bloco(draw, texto, y, tam, cor, largura, x=90, negrito=True, centro=False, W=1080, max_linhas=6):
    # reduz a fonte até caber no máximo de linhas
    while True:
        f = fonte(tam, negrito)
        linhas = quebrar(draw, texto, f, largura)
        if len(linhas) <= max_linhas or tam <= 30:
            break
        tam -= 6
    for ln in linhas:
        lx = (W - draw.textlength(ln, font=f)) / 2 if centro else x
        draw.text((lx, y), ln, font=f, fill=cor)
        y += int(tam * 1.22)
    return y


def pilula(draw, texto, x, y, tam=34, fundo=AMARELO, cor=AZUL):
    f = fonte(tam)
    w = draw.textlength(texto, font=f)
    draw.rounded_rectangle((x, y, x + w + 44, y + tam + 26), radius=(tam + 26) // 2, fill=fundo)
    draw.text((x + 22, y + 9), texto, font=f, fill=cor)
    return y + tam + 26


def rodape(draw, cfg, W, H):
    f = fonte(30, False)
    t = f"{cfg['perfil']}  ·  link na bio  ·  {cfg['site']}"
    draw.text(((W - draw.textlength(t, font=f)) / 2, H - 80), t, font=f, fill=CINZA)


def colar_foto(img, pid, caixa):
    for ext in (".png", ".jpg", ".jpeg", ".webp"):
        cam = os.path.join(FOTOS, pid + ext)
        if os.path.exists(cam):
            foto = Image.open(cam).convert("RGBA")
            x0, y0, x1, y1 = caixa
            foto.thumbnail((x1 - x0, y1 - y0))
            bg = Image.new("RGBA", (x1 - x0, y1 - y0), BRANCO + (255,))
            bg.alpha_composite(foto, ((x1 - x0 - foto.width) // 2, (y1 - y0 - foto.height) // 2))
            mask = Image.new("L", bg.size, 0)
            ImageDraw.Draw(mask).rounded_rectangle((0, 0, *bg.size), radius=36, fill=255)
            img.paste(bg.convert("RGB"), (x0, y0), mask)
            return True
    return False


def base(W, H, fundo=AZUL):
    img = Image.new("RGB", (W, H), fundo)
    d = ImageDraw.Draw(img)
    d.rectangle((0, 0, W, 18), fill=AMARELO)
    return img, d


def slide_capa(cfg, pauta, W=1080, H=1350, reels=False):
    img, d = base(W, H)
    y = 180 if not reels else 420
    y = pilula(d, pauta["pilar"].upper(), 90, y) + 50
    y = texto_bloco(d, pauta["titulo"], y, 96, BRANCO, W - 180, max_linhas=5) + 40
    if not reels:
        pilula(d, "ARRASTA PRO LADO  →", 90, H - 230, 36)
    else:
        pilula(d, f"Comenta {pauta['palavra']} e receba o link", 90, y + 20, 40)
    rodape(d, cfg, W, H)
    return img


def slide_produto(cfg, p, i, total, W=1080, H=1350):
    img, d = base(W, H)
    d.text((90, 70), f"{i}/{total}", font=fonte(34, False), fill=CINZA)
    tem_foto = colar_foto(img, p["id"], (140, 150, W - 140, 690))
    y = 740 if tem_foto else 260
    y = pilula(d, p["selo"].upper(), 90, y, 32) + 36
    y = texto_bloco(d, p["nome"], y, 76 if tem_foto else 96, BRANCO, W - 180, max_linhas=3) + 30
    d.text((90, y), "a partir de", font=fonte(34, False), fill=CINZA)
    d.text((90, y + 44), f"R$ {p['preco']}", font=fonte(92), fill=AMARELO)
    d.text((90, H - 150), "*preço pode mudar no Mercado Livre", font=fonte(26, False), fill=CINZA)
    rodape(d, cfg, W, H)
    return img


def slide_topico(cfg, texto, i, total, W=1080, H=1350):
    img, d = base(W, H)
    d.text((90, 70), f"{i}/{total}", font=fonte(34, False), fill=CINZA)
    d.text((90, 260), f"{i:02d}", font=fonte(220), fill=AMARELO)
    texto_bloco(d, texto, 560, 80, BRANCO, W - 180, max_linhas=6)
    rodape(d, cfg, W, H)
    return img


def slide_final(cfg, pauta, W=1080, H=1350):
    img, d = base(W, H, AMARELO)
    y = texto_bloco(d, "Gostou?", 260, 110, AZUL, W - 180, centro=True)
    y = texto_bloco(d, f"Comenta {pauta['palavra']}", y + 40, 96, AZUL, W - 180, centro=True)
    y = texto_bloco(d, "que eu te mando o link no direct", y + 10, 52, AZUL, W - 180, negrito=False, centro=True)
    y = texto_bloco(d, "Salva pra não perder  ·  Manda pra quem precisa", y + 80, 40, AZUL, W - 180, negrito=False, centro=True)
    f = fonte(30, False)
    t = f"{cfg['perfil']}  ·  lista completa: link na bio"
    d.text(((W - d.textlength(t, font=f)) / 2, H - 80), t, font=f, fill=AZUL)
    return img


def story_link(cfg, pauta, prods, W=1080, H=1920):
    img, d = base(W, H)
    y = pilula(d, "NOVO POST NO FEED", 90, 260) + 50
    y = texto_bloco(d, pauta["titulo"], y, 92, BRANCO, W - 180, max_linhas=5) + 30
    if prods:
        colar_foto(img, prods[0]["id"], (190, y + 20, W - 190, y + 620))
    # área reservada para o adesivo de LINK (Instagram > adesivos > Link)
    d.rounded_rectangle((190, H - 560, W - 190, H - 400), radius=40, outline=AMARELO, width=6)
    f = fonte(38)
    t = "cole o adesivo de LINK aqui"
    d.text(((W - d.textlength(t, font=f)) / 2, H - 500), t, font=f, fill=AMARELO)
    rodape(d, cfg, W, H)
    return img


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Gera as artes PNG do Instagram")
    ap.add_argument("--post", type=int, help="número do post (1, 2, 3...)")
    args = ap.parse_args()

    with open(CONFIG_IG, encoding="utf-8") as f:
        cfg = json.load(f)
    with open(PRODUTOS, encoding="utf-8") as f:
        produtos = {p["id"]: p for p in json.load(f)["produtos"]}

    for n, pauta in enumerate(cfg["pautas"], 1):
        if args.post and n != args.post:
            continue
        prods = [produtos[i] for i in pauta["produtos"]]
        pasta = os.path.join(PASTA_ARTES, f"ig{n:02d}_{pauta['palavra'].lower()}")
        os.makedirs(pasta, exist_ok=True)
        arquivos = []
        if pauta["formato"] == "carrossel":
            slides = [slide_capa(cfg, pauta)]
            itens = pauta.get("topicos", [])
            total = len(itens) + len(prods)
            slides += [slide_topico(cfg, t, i, total) for i, t in enumerate(itens, 1)]
            slides += [slide_produto(cfg, p, len(itens) + i, total) for i, p in enumerate(prods, 1)]
            slides.append(slide_final(cfg, pauta))
            slides = slides[:20]  # limite do Instagram: 20 imagens por carrossel
            for i, s in enumerate(slides, 1):
                arquivos.append(f"slide_{i:02d}.png")
                s.save(os.path.join(pasta, arquivos[-1]))
        else:
            slide_capa(cfg, pauta, 1080, 1920, reels=True).save(os.path.join(pasta, "capa_reels.png"))
            arquivos.append("capa_reels.png")
        story_link(cfg, pauta, prods).save(os.path.join(pasta, "story_link.png"))
        arquivos.append("story_link.png")
        print(f"🎨 #{n:02d} {pauta['formato']:<9} {pauta['titulo'][:48]:<48} → {len(arquivos)} arquivos")
    print(f"\n✅ Artes em: {PASTA_ARTES}")
    sem_foto = sorted({i for pa in cfg["pautas"] for i in pa["produtos"]}
                      - {os.path.splitext(a)[0] for a in os.listdir(FOTOS)} if os.path.isdir(FOTOS) else [])
    if sem_foto:
        print(f"ℹ️  {len(sem_foto)} produtos sem foto em fotos_produtos\\ (a arte sai só com texto): {', '.join(sem_foto[:8])}...")


if __name__ == "__main__":
    main()
