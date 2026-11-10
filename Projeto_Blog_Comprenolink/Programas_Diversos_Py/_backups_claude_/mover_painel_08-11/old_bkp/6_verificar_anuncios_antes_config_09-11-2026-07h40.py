# -*- coding: utf-8 -*-
"""
Verifica a situação dos anúncios do guia no Mercado Livre (ativo, pausado, removido...).

Como funciona
  1. Lê a página pública do guia e pega cada produto (nº, nome no blog, título do card, link de afiliado).
  2. Abre cada link de afiliado (meli.la ou mercadolivre.com.br/social/...). Essa página pública do ML
     mostra no 1º card o anúncio para onde o link leva: número do anúncio (MLB...), código do catálogo,
     título, preço e avisos como "Anúncio pausado".
  3. Grava o resultado em Relatorios_Diarios_Anuncios\\anuncios_status\\status_anuncios_AAAA-MM-DD_HHhMM.csv
     e acrescenta no historico_status_anuncios.csv (é isso que o painel lê).

Limites (importante)
  - A API do ML exige login de desenvolvedor e a página do produto pede verificação de robô.
    Este script NÃO tenta burlar isso: se o ML pedir verificação, o anúncio fica "Não verificado".
  - O ML não mostra publicamente o MOTIVO de um anúncio estar pausado ou removido (isso só aparece
    para o vendedor). O script registra o aviso que o ML mostra e uma causa PROVÁVEL.

Uso:  python 6_verificar_anuncios.py  [--pausa 2]
"""
import csv
import html
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime

RELAT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # Relatorios_Diarios_Anuncios
BASE = os.path.dirname(RELAT)  # D:/mercado_livre
PASTA = os.path.join(RELAT, "anuncios_status")
HISTORICO = os.path.join(PASTA, "historico_status_anuncios.csv")
CONFIG = os.path.join(BASE, "1- Gera_Relatorio", "config_rastreio.json")
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/130.0 Safari/537.36")
COLUNAS = ["verificado_em", "item", "nome_no_blog", "titulo_card", "link_afiliado", "status", "aviso_ml",
           "motivo_provavel", "acao_sugerida", "anuncio_mlb", "catalogo_mlb", "catalogo_no_blog", "titulo_ml", "preco_ml",
           "url_anuncio", "http", "url_final"]

MOTIVOS = {
    "Ativo": ("", ""),
    "Pausado": ("Pausado pelo vendedor ou sem estoque. O ML não mostra o motivo exato para afiliados.",
                "Gerar novo link de afiliado de um anúncio ATIVO do mesmo produto (catálogo) e trocar no blog."),
    "Removido / indisponível": ("Anúncio finalizado ou excluído pelo vendedor, ou retirado pelo ML (ex.: política, "
                                "estoque zerado por muito tempo). O motivo não é público.",
                                "Trocar o produto ou o link no blog; o link atual não mostra mais o anúncio."),
    "Link quebrado": ("O link de afiliado não abriu (erro HTTP).", "Gerar o link de novo no painel ML Afiliados."),
    "Sem link de afiliado": ("O item do blog não tem link meli.la nem link de afiliado do ML.",
                             "Colocar o link de afiliado no item."),
    "Não verificado": ("O ML pediu verificação de robô ou não respondeu; nada foi burlado.",
                       "Rodar de novo mais tarde ou abrir o link no navegador."),
}


def baixar(url, tentativas=2):
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9",
                                               "Accept": "text/html,application/xhtml+xml"})
    ultimo = None
    for i in range(tentativas):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                return r.status, r.geturl(), r.read().decode("utf-8", errors="replace")
        except urllib.error.HTTPError as e:
            return e.code, url, ""
        except Exception as e:  # rede instável: tenta de novo
            ultimo = e
            time.sleep(3)
    return 0, url, f"erro: {ultimo}"


def limpa(s):
    return re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", "", s or ""))).strip()


def pagina_do_guia():
    pagina = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"
    try:
        pagina = json.load(open(CONFIG, encoding="utf-8")).get("pagina_blog") or pagina
    except Exception:
        pass
    return pagina


def itens_do_blog(t):
    itens = []
    marcas = list(re.finditer(r'<h2[^>]*id="item-(\d+)"[^>]*>(.*?)</h2>', t, re.S))
    for k, m in enumerate(marcas):
        fim = marcas[k + 1].start() if k + 1 < len(marcas) else len(t)
        trecho = t[m.start():fim]
        links = [html.unescape(u) for u in re.findall(r'href="([^"]+)"', trecho)
                 if "meli.la/" in u or "mercadolivre.com.br/social/" in u]
        h3 = re.search(r"<h3>(.*?)</h3>", trecho, re.S)
        nome = limpa(m.group(2))
        nome = re.sub(r"^\d+\.\s*", "", nome).split("⭐")[0].strip()
        itens.append({"item": int(m.group(1)), "nome_no_blog": nome,
                      "titulo_card": limpa(h3.group(1)).rstrip("…").strip() if h3 else "",
                      "link_afiliado": links[0] if links else ""})
    return itens


def catalogo_dos_backups():
    """affiliate_url -> (código do catálogo, título completo), lido do backup mais novo da página no WordPress."""
    pasta = os.path.join(BASE, "9_Manutenção_Blog", "2_DADOS", "Blog_WordPress", "backups")
    mapa = {}
    try:
        arquivos = sorted((os.path.join(pasta, a) for a in os.listdir(pasta) if a.startswith("pagina_")),
                          key=os.path.getmtime)
    except OSError:
        return mapa
    for caminho in arquivos:  # do mais antigo ao mais novo: o mais novo prevalece
        t = open(caminho, encoding="utf-8", errors="replace").read()
        for bloco in re.findall(r"wp:hostinger-affiliate-plugin/mercado-block (\{.*?\}) /-->", t):
            try:
                b = json.loads(bloco)
            except ValueError:
                continue
            url, asin = b.get("affiliate_url"), b.get("asin")
            if url and asin:
                mapa[url] = (asin, (b.get("items", {}).get(asin) or {}).get("title", ""))
    return mapa


def primeiro_card(t):
    """Dados do 1º polycard (o anúncio em destaque do link de afiliado)."""
    i = t.find('"polycards":[')
    if i < 0:
        return None
    trecho = t[i:i + 20000]
    meta = re.search(r'"metadata":\{"id":"(MLB\d+)"(?:,"product_id":"(MLB\d+)")?.*?"url":"([^"]+)"', trecho)
    if not meta:
        return None
    fim = trecho.find('"unique_id"', meta.end())
    card = trecho[:fim] if fim > 0 else trecho
    S = r'"((?:[^"\\]|\\.)*)"'  # string JSON com escapes
    titulo = re.search(r'"type":"title".*?"text":' + S, card)
    preco = re.search(r'"current_price":\{"value":([\d.]+)', card)
    pausado = re.search(r'"type":"paused".*?"text":' + S, card)
    avisos = [re.sub(r"\{[^}]*\}", "", a).strip() for a in
              re.findall(r'"type":"(?:paused|highlight)".*?"text":' + S, card)]

    def decod(s):
        try:
            return json.loads(f'"{s}"') if s else ""
        except ValueError:
            return s
    return {"anuncio_mlb": meta.group(1), "catalogo_mlb": meta.group(2) or "",
            "url_anuncio": "https://" + decod(meta.group(3)).split("#")[0].split("?")[0],
            "titulo_ml": decod(titulo.group(1)) if titulo else "",
            "preco_ml": float(preco.group(1)) if preco else None,
            "pausado": decod(pausado.group(1)) if pausado else "",
            "avisos": "; ".join(decod(a) for a in avisos if a)}


def verificar(item):
    r = dict(item)
    r.update({c: "" for c in COLUNAS if c not in r})
    if not item["link_afiliado"]:
        r["status"] = "Sem link de afiliado"
    else:
        cod, final, t = baixar(item["link_afiliado"])
        r["http"], r["url_final"] = cod, final
        card = primeiro_card(t) if cod == 200 else None
        if cod == 0 or "account-verification" in final or "captcha" in t[:5000].lower():
            r["status"] = "Não verificado"
        elif cod >= 400:
            r["status"] = "Link quebrado"
        elif not card:
            r["status"] = "Removido / indisponível"
            if "/lists" in final or "perfil ainda está vazio" in t:
                r["aviso_ml"] = "O link leva ao perfil de afiliado vazio (\"Este perfil ainda está vazio\"): o anúncio não existe mais."
            else:
                r["aviso_ml"] = "A página do link abriu sem o anúncio em destaque."
        else:
            r.update({k: card[k] for k in ("anuncio_mlb", "catalogo_mlb", "url_anuncio", "titulo_ml", "preco_ml")})
            r["aviso_ml"] = re.sub(r"\{[^}]*\}", "", card["pausado"] or card["avisos"]).strip()
            r["status"] = "Pausado" if card["pausado"] else "Ativo"
    r["motivo_provavel"], r["acao_sugerida"] = MOTIVOS[r["status"]]
    return r


def main(pausa=None):
    """pausa: segundos entre um anúncio e outro (o .exe do relatório chama main(pausa=1))."""
    if pausa is None:
        pausa = float(sys.argv[sys.argv.index("--pausa") + 1]) if "--pausa" in sys.argv else 2.0
    os.makedirs(PASTA, exist_ok=True)
    pagina = pagina_do_guia()
    cod, _, t = baixar(f"{pagina}?verificacao={int(time.time())}")
    if cod != 200:
        print(f"Não consegui abrir o guia ({cod}): {pagina}")
        return 1
    itens = itens_do_blog(t)
    print(f"Guia: {pagina} · {len(itens)} produtos")
    agora = datetime.now().strftime("%Y-%m-%d %H:%M")
    catalogo = catalogo_dos_backups()
    resultado = []
    for it in itens:
        r = verificar(it)
        asin, titulo = catalogo.get(it["link_afiliado"], ("", ""))
        r["catalogo_no_blog"] = asin
        if titulo and len(titulo) > len(r["titulo_card"]):
            r["titulo_card"] = titulo
        r["verificado_em"] = agora
        resultado.append(r)
        extra = f" · {r['aviso_ml']}" if r["aviso_ml"] else ""
        print(f"  {r['item']:>2}. {r['status']:<24} {r['anuncio_mlb'] or '-':<15} {r['nome_no_blog'][:45]}{extra}")
        time.sleep(pausa)
    nome = os.path.join(PASTA, datetime.now().strftime("status_anuncios_%Y-%m-%d_%Hh%M.csv"))
    for caminho, modo in ((nome, "w"), (HISTORICO, "a")):
        novo = modo == "w" or not os.path.exists(HISTORICO)
        with open(caminho, modo, newline="", encoding="utf-8-sig") as f:
            w = csv.DictWriter(f, fieldnames=COLUNAS, delimiter=";", extrasaction="ignore")
            if novo:
                w.writeheader()
            w.writerows(resultado)
    resumo = {}
    for r in resultado:
        resumo[r["status"]] = resumo.get(r["status"], 0) + 1
    print("Resumo:", " · ".join(f"{k}: {v}" for k, v in resumo.items()))
    print("Arquivo:", nome)
    return 0


if __name__ == "__main__":
    sys.exit(main())
