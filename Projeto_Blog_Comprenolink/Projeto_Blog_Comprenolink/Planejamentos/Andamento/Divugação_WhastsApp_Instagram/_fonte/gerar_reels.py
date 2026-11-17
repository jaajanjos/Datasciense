# -*- coding: utf-8 -*-
"""Reels (vídeo 9:16, 12 s, sem preço) a partir do pacote do dia: usa o story.png (foto e nome do produto) e os
benefícios (✅) da legenda do feed. Gera reels.mp4 + reels_capa.jpg + 2_LEGENDA_REELS.txt na pasta do dia.
Rodar:  python -X utf8 _fonte\\gerar_reels.py 2026-11-02     (ou --todos)
Roda sozinho no fim do gerar_artes_catalogo.py (pacote do dia novo = Reels novos).
Precisa do ffmpeg (PATH ou instalado pelo winget). Música: adicionar no app do Instagram (opcional).
"""
import glob
import os
import re
import shutil
import subprocess
import sys
import tempfile

from PIL import Image, ImageDraw

from gerar_logo import AMARELO, BRANCO, CINZA, ESCURO, fonte, horizontal

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACOTE = os.path.join(RAIZ, "07_PACOTE_DO_DIA")
W, H, FPS = 1080, 1920, 30
CENAS = (4.0, 4.0, 4.0)  # segundos de cada cena; transição de 0,5 s entre elas
PALAVRA = {"Black Friday": "BLACK", "Natal": "NATAL"}
FFMPEG = shutil.which("ffmpeg") or next(iter(sorted(glob.glob(os.path.expandvars(
    r"%LOCALAPPDATA%\Microsoft\WinGet\Packages\Gyan.FFmpeg*\*\bin\ffmpeg.exe")))), None)


def ler_dia(pasta):
    with open(os.path.join(pasta, "1_TEXTOS_DO_DIA.txt"), encoding="utf-8-sig") as f:
        txt = f.read()
    m = re.search(r"Instagram – Post no feed.*?\n=+\n(.*?)\n=+", txt, re.S)
    if not m:
        return None
    legenda = m.group(1).strip()
    legenda = re.sub(r"\n+Obs\.:.*$", "", legenda, flags=re.S).strip()
    beneficios = [l[1:].strip() for l in legenda.splitlines() if l.startswith("✅")][:4]
    campanha = "Natal" if "#natal" in legenda or "NATAL" in legenda else "Black Friday"
    return legenda, beneficios, campanha


def texto_centro(d, y, t, fnt, cor, larg=W - 140):
    """Escreve centralizado quebrando linhas; devolve o y final."""
    palavras, linha, linhas = t.split(), "", []
    for p in palavras:
        teste = (linha + " " + p).strip()
        if d.textlength(teste, font=fnt) <= larg:
            linha = teste
        else:
            linhas.append(linha)
            linha = p
    linhas.append(linha)
    alt = fnt.size * 1.25
    for l in linhas:
        d.text((W / 2, y), l, font=fnt, fill=cor, anchor="mt")
        y += alt
    return y


def cena1(story):
    """Faixa da campanha + foto + nome do produto (topo do story), com chamada própria do Reels embaixo."""
    img = story.copy()
    d = ImageDraw.Draw(img)
    d.rectangle([0, 1420, W, H], fill=ESCURO)
    texto_centro(d, 1500, "Veja os detalhes no Mercado Livre", fonte("arial.ttf", 46), BRANCO)
    d.text((W / 2, 1760), "veja os detalhes »", font=fonte("arialbd.ttf", 44), fill=AMARELO, anchor="mm")
    return img


def cena2(story, beneficios, nome):
    img = Image.new("RGB", (W, H), ESCURO)
    d = ImageDraw.Draw(img)
    foto = story.crop((130, 280, 950, 1100)).resize((560, 560), Image.LANCZOS)
    img.paste(foto, ((W - 560) // 2, 150))
    y = texto_centro(d, 770, nome, fonte("arialbd.ttf", 54), BRANCO)
    y += 40
    for b in beneficios:
        d.rounded_rectangle([90, y, W - 90, y + 150], radius=28, fill=(31, 41, 55))
        d.ellipse([125, y + 50, 175, y + 100], fill=AMARELO)
        d.text((150, y + 75), "✓", font=fonte("seguisym.ttf", 36), fill=ESCURO, anchor="mm")
        fnt = fonte("arial.ttf", 40)
        while d.textlength(b, font=fnt) > W - 330 and fnt.size > 30:
            fnt = fonte("arial.ttf", fnt.size - 2)
        d.text((210, y + 75), b, font=fnt, fill=BRANCO, anchor="lm")
        y += 175
    return img


def cena3(campanha):
    img = Image.new("RGB", (W, H), ESCURO)
    d = ImageDraw.Draw(img)
    logo = horizontal(ESCURO, BRANCO, CINZA).resize((900, 270), Image.LANCZOS)
    img.paste(logo, (90, 260))
    d.text((W / 2, 760), "Quer o link?", font=fonte("arialbd.ttf", 84), fill=BRANCO, anchor="mm")
    d.rounded_rectangle([170, 880, W - 170, 1080], radius=100, fill=AMARELO)  # margem: o zoom corta ~3% das bordas
    d.text((W / 2, 980), f"Comente {PALAVRA[campanha]}", font=fonte("arialbd.ttf", 74), fill=ESCURO, anchor="mm")
    d.text((W / 2, 1170), "que eu te mando no Direct", font=fonte("arial.ttf", 54), fill=BRANCO, anchor="mm")
    d.text((W / 2, 1330), "ou toque no link da bio", font=fonte("arialbd.ttf", 54), fill=AMARELO, anchor="mm")
    d.text((W / 2, 1480), "Confira o valor do dia direto no Mercado Livre", font=fonte("arial.ttf", 40), fill=CINZA, anchor="mm")
    d.text((W / 2, 1780), "Link de afiliado: posso ganhar comissão, sem custo extra para você.",
           font=fonte("arial.ttf", 30), fill=CINZA, anchor="mm")
    return img


def video(cenas, saida):
    with tempfile.TemporaryDirectory() as tmp:
        entradas, filtros = [], []
        for i, (im, seg) in enumerate(zip(cenas, CENAS)):
            arq = os.path.join(tmp, f"c{i}.png")
            im.save(arq)
            entradas += ["-i", arq]  # 1 quadro só: o zoompan gera os n quadros da cena
            n = int(seg * FPS)
            # zoom lento (1,00 → 1,06) para dar movimento
            filtros.append(f"[{i}:v]scale={W * 2}:{H * 2},zoompan=z='1+0.06*on/{n}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
                           f":d={n}:s={W}x{H}:fps={FPS},setsar=1[v{i}]")
        off = CENAS[0] - 0.5
        filtros.append(f"[v0][v1]xfade=transition=fade:duration=0.5:offset={off}[x1]")
        off += CENAS[1] - 0.5
        filtros.append(f"[x1][v2]xfade=transition=fade:duration=0.5:offset={off},format=yuv420p[out]")
        cmd = [FFMPEG, "-y", "-loglevel", "error"] + entradas + [
            "-filter_complex", ";".join(filtros), "-map", "[out]", "-r", str(FPS), "-c:v", "libx264",
            "-preset", "medium", "-crf", "20", "-movflags", "+faststart", saida]
        subprocess.run(cmd, check=True)


def gera(pasta):
    dados = ler_dia(pasta)
    if not dados:
        return False
    legenda, beneficios, campanha = dados
    story = Image.open(os.path.join(pasta, "story.png")).convert("RGB")
    nome = re.sub(r"^\W+", "", legenda.splitlines()[0]).strip()
    c1 = cena1(story)
    video([c1, cena2(story, beneficios, nome), cena3(campanha)], os.path.join(pasta, "reels.mp4"))
    c1.save(os.path.join(pasta, "reels_capa.jpg"), quality=90)
    with open(os.path.join(pasta, "2_LEGENDA_REELS.txt"), "w", encoding="utf-8-sig", newline="\r\n") as f:
        f.write("LEGENDA DO REELS (mesma do post do feed)\n" + "=" * 40 + "\n" + legenda + "\n")
    return True


def todos(prefixo=""):
    """Gera os Reels dos dias com post no Instagram; devolve as pastas feitas (vazio se não houver ffmpeg)."""
    if not FFMPEG:
        print("Reels: ffmpeg não encontrado – pulei (instale com: winget install Gyan.FFmpeg)")
        return []
    return [p for p in sorted(os.listdir(PACOTE)) if p.startswith(prefixo) and gera(os.path.join(PACOTE, p))]


if __name__ == "__main__":
    alvo = sys.argv[1] if len(sys.argv) > 1 else "--todos"
    feitos = todos("" if alvo == "--todos" else alvo)
    print(len(feitos), "Reels:", ", ".join(feitos))
