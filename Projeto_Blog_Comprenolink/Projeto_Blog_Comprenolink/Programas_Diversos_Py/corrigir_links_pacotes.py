# -*- coding: utf-8 -*-
"""Corrige só o número #item-N dos links nos 1_TEXTOS_DO_DIA.txt dos pacotes do dia (a numeração do guia muda quando um anúncio sai).
Acha o número certo pelo NOME do produto do dia, comparando com o guia ao vivo. Não regera artes nem textos.
Uso:  python -X utf8 corrigir_links_pacotes.py            (só mostra o que mudaria)
      python -X utf8 corrigir_links_pacotes.py --aplicar  (grava; antes copia o original para old_bkp\\ da mesma pasta como nome_DD-MM-AAAA-HHhMM.txt)
      --desde=AAAA-MM-DD  (padrão: hoje)
"""
import html
import os
import re
import shutil
import sys
import urllib.request
from datetime import date, datetime

APLICAR = "--aplicar" in sys.argv
m = re.search(r"--desde=(\d{4})-(\d{2})-(\d{2})", " ".join(sys.argv))
DESDE = date(int(m[1]), int(m[2]), int(m[3])) if m else date.today()
RAIZ = "D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento"
PASTAS = [RAIZ + "/Divugação_WhastsApp_Instagram/07_PACOTE_DO_DIA", RAIZ + "/Celular_Whatsapp/07_PACOTE_DO_DIA"]
GUIA = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"


def norm(t):
    t = html.unescape(t or "").replace("″", '"').replace("×", "x").replace("’", "'").replace("–", "-").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", t).strip().lower()


req = urllib.request.Request(GUIA + f"?v={int(datetime.now().timestamp())}", headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"})
pagina = urllib.request.urlopen(req, timeout=90).read().decode("utf-8", "ignore")
ITENS = [(int(a), norm(n)) for a, b, n in re.findall(r'<h2 id="item-(\d+)"[^>]*>(\d+)\.<a[^>]*>([^<]+)</a>', pagina)]
print(f"guia ao vivo: {len(ITENS)} itens")


def titulo(txt):
    p = txt.split("Post no feed", 1)
    if len(p) > 1:
        a = re.search(r"[🔥🎄]\s*([^\n]+)", p[1])
        if a:
            return a.group(1).strip()
    a = re.search(r"[🔥🎄]\s*\*?(?:Black Friday|Natal|Presentes de Natal)\s*[:\-–]\s*([^\n*]+)", txt)
    return a.group(1).strip() if a else None


def numero(nome):
    n = norm(nome)
    for i, t in ITENS:
        if t[:28] == n[:28]:
            return i
    return None


resumo = []
for raiz in PASTAS:
    if not os.path.isdir(raiz):
        print("pasta não existe:", raiz)
        continue
    for pasta in sorted(os.listdir(raiz)):
        mm = re.match(r"(\d{4})-(\d{2})-(\d{2})_", pasta)
        arq = os.path.join(raiz, pasta, "1_TEXTOS_DO_DIA.txt")
        if not mm or not os.path.exists(arq):
            continue
        dia = date(int(mm[1]), int(mm[2]), int(mm[3]))
        if dia < DESDE:
            continue
        bruto = open(arq, "rb").read()
        bom = bruto.startswith(b"\xef\xbb\xbf")
        txt = bruto.decode("utf-8-sig")
        usados = sorted({int(x) for x in re.findall(r"#item-(\d+)", txt)})
        if not usados:
            resumo.append((dia, raiz.split("/")[-2][:14], "-", "-", "sem link de produto (dia de lista)"))
            continue
        nome = titulo(txt)
        certo = numero(nome) if nome else None
        if certo is None:
            resumo.append((dia, raiz.split("/")[-2][:14], nome, usados, "PRODUTO NÃO ACHADO NO GUIA: conferir"))
            continue
        if usados == [certo]:
            resumo.append((dia, raiz.split("/")[-2][:14], nome, usados, "ok"))
            continue
        resumo.append((dia, raiz.split("/")[-2][:14], nome, usados, f"trocar para #item-{certo}"))
        if APLICAR:
            bk = os.path.join(raiz, pasta, "old_bkp")
            os.makedirs(bk, exist_ok=True)
            shutil.copy2(arq, os.path.join(bk, f"1_TEXTOS_DO_DIA_{datetime.now():%d-%m-%Y-%Hh%M}.txt"))
            novo = re.sub(r"#item-\d+", f"#item-{certo}", txt)
            open(arq, "wb").write((b"\xef\xbb\xbf" if bom else b"") + novo.encode("utf-8"))
for d, o, nome, u, a in resumo:
    print(f"{d:%d/%m} {o:14} {str(nome)[:38]:38} link={str(u):8} -> {a}")
print("MODO:", "APLICADO" if APLICAR else "só visualização")
