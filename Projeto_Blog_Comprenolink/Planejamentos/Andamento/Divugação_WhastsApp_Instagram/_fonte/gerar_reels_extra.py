# -*- coding: utf-8 -*-
"""Reels EXTRAS (20/11/2026, aprovados pelo dono): 20 produtos do guia do blog que ainda nao viraram Reel,
para 24 a 27/11 (5 por dia: 11h00, 13h30, 16h00, 18h00, 20h00).
Gera, para cada item, uma pasta em 07_PACOTE_DO_DIA\\EXTRA_REELS_24-27nov\\ com story/feed/status.png,
1_TEXTOS_DO_DIA.txt (legenda so com comprenolink.net e #comprenolinkblog) e reels.mp4 + 2_LEGENDA_REELS.txt.
NAO mexe nas pastas dos dias normais (24/11 a 27/11 ficam como estao).
Uso:  python -X utf8 _fonte\\gerar_reels_extra.py            (todos)
      python -X utf8 _fonte\\gerar_reels_extra.py 59 78      (so esses itens)
"""
import os
import re
import sys
from datetime import date

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dados_divulgacao as dd  # noqa: E402
import gerar_artes_catalogo as g  # noqa: E402
import gerar_reels  # noqa: E402

# (dia, hora, numero do item no guia)
LISTA = [
    ("2026-11-24", "11h00", 59), ("2026-11-24", "13h30", 78), ("2026-11-24", "16h00", 80),
    ("2026-11-24", "18h00", 77), ("2026-11-24", "20h00", 48),
    ("2026-11-25", "11h00", 61), ("2026-11-25", "13h30", 60), ("2026-11-25", "16h00", 43),
    ("2026-11-25", "18h00", 55), ("2026-11-25", "20h00", 28),
    ("2026-11-26", "11h00", 57), ("2026-11-26", "13h30", 38), ("2026-11-26", "16h00", 27),
    ("2026-11-26", "18h00", 73), ("2026-11-26", "20h00", 72),
    ("2026-11-27", "11h00", 19), ("2026-11-27", "13h30", 20), ("2026-11-27", "16h00", 53),
    ("2026-11-27", "18h00", 33), ("2026-11-27", "20h00", 32),
]
CAMP = "black_friday"
RAIZ_EXTRA = os.path.join(g.PACOTE, "EXTRA_REELS_24-27nov")
CACHE_EXTRA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "cache_fotos_extra")


def foto_fresca(x):
    """Sempre baixa a foto ATUAL do item (o cache antigo guarda fotos de quando os numeros do guia eram outros)."""
    import io
    import urllib.request
    from PIL import Image
    os.makedirs(CACHE_EXTRA, exist_ok=True)
    arq = os.path.join(CACHE_EXTRA, f"item{x['n']}.png")
    req = urllib.request.Request(x["imagem"], headers={"User-Agent": "Mozilla/5.0"})
    im = Image.open(io.BytesIO(urllib.request.urlopen(req, timeout=60).read())).convert("RGBA")
    fundo = Image.new("RGBA", im.size, (255, 255, 255, 255))
    Image.alpha_composite(fundo, im).convert("RGB").save(arq)
    return Image.open(arq).convert("RGB")


g.foto = foto_fresca


def main():
    so = {int(a) for a in sys.argv[1:]}
    dados = dd.carrega_produtos()
    dd.carrega_produtos.cache = dados
    itens = {x["n"]: x for x in dados["itens"]}
    os.makedirs(RAIZ_EXTRA, exist_ok=True)
    for i, (dia_s, hora, n) in enumerate(LISTA, 1):
        if so and n not in so:
            continue
        dia = date.fromisoformat(dia_s)
        x = itens[n]
        t = dd.textos_produto(x, CAMP, dia)
        pasta = os.path.join(RAIZ_EXTRA, f"{dia:%d-%m}_{hora}_item{n}_{dd.slug(x['nome'])[:22]}")
        os.makedirs(pasta, exist_ok=True)
        for formato in ("feed", "story", "status"):
            g.arte(x, CAMP, formato).save(os.path.join(pasta, f"{formato}.png"))
        txt = [f"REEL EXTRA {dia:%d/%m/%Y} as {hora} - item {n} do guia: {x['nome']}", "",
               "=" * 60, f"{hora}  Instagram – Post no feed (foto/carrossel)", "Imagem: feed.png", "=" * 60,
               t["legenda"], "", "=" * 60, ""]
        with open(os.path.join(pasta, "1_TEXTOS_DO_DIA.txt"), "w", encoding="utf-8-sig", newline="\r\n") as fh:
            fh.write("\n".join(txt))
        ok = gerar_reels.gera(pasta)
        print(f"{i:02d}. {dia:%d/%m} {hora} item {n} '{x['nome'][:45]}' | reels {'ok' if ok else 'NAO gerado'}")


if __name__ == "__main__":
    main()
