# -*- coding: utf-8 -*-
"""Check completo do site comprenolink.net.

Testa cada página (status, título, descrição, H1, erros visíveis, imagens sem alt),
todos os links internos e todos os links de afiliado (meli.la) seguindo o redirecionamento.
Uso:  python teste_site_completo.py      → gera teste_site_<data>.html nesta pasta
"""
import html
import os
import re
import ssl
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
from urllib.parse import urljoin, urlparse

SITE = "https://comprenolink.net"
PAGINAS = ["/", "/melhores-produtos-mercado-livre-2026/", "/sobre/", "/contato/", "/politica-de-privacidade/"]
# Endereços que já receberam visita ou que existem por padrão no WordPress
EXTRAS = ["/hello-world/", "/5-2/", "/5.2/", "/inicio/", "/author/compre-no-link26/", "/category/uncategorized/",
          "/?s=fone", "/pagina-que-nao-existe/", "/sitemap.xml", "/robots.txt"]
ERROS_VISIVEIS = ["Hello world", "Não foi possível buscar", "Recent Posts", "Recent Comments",
                  "Orgulhosamente mantido", "ADICIONAR AO MENU", "Lorem ipsum", "Warning:", "Fatal error"]
UA = "Mozilla/5.0 (Linux; Android 14) AppleWebKit/537.36 Chrome/128 Mobile Safari/537.36 TesteSite/1.0"
CTX = ssl.create_default_context()
PASTA = os.path.dirname(os.path.abspath(__file__))


def baixar(url, metodo="GET"):
    """Devolve (status, url_final, texto, segundos, tamanho)."""
    sep = "&" if "?" in url else "?"
    pedido = urllib.request.Request(url if metodo == "HEAD" else f"{url}{sep}teste={int(time.time())}",
                                    headers={"User-Agent": UA, "Cache-Control": "no-cache"}, method=metodo)
    ini = time.time()
    try:
        with urllib.request.urlopen(pedido, timeout=30, context=CTX) as r:
            corpo = r.read() if metodo == "GET" else b""
            return r.status, r.geturl(), corpo.decode("utf-8", "replace"), time.time() - ini, len(corpo)
    except urllib.error.HTTPError as e:
        corpo = e.read()
        return e.code, url, corpo.decode("utf-8", "replace"), time.time() - ini, len(corpo)
    except Exception as e:  # noqa: BLE001 - registrar qualquer falha de rede
        return 0, url, str(e), time.time() - ini, 0


def texto_visivel(h):
    h = re.sub(r"(?is)<(script|style|noscript)[^>]*>.*?</\1>", " ", h)
    return html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", h)))


def analisar_pagina(caminho):
    url = urljoin(SITE, caminho)
    st, final, h, seg, tam = baixar(url)
    titulo = html.unescape((re.search(r"(?is)<title>(.*?)</title>", h) or [None, ""])[1].strip())
    desc = re.search(r'(?is)<meta name="description" content="(.*?)"', h)
    h1s = [texto_visivel(x).strip() for x in re.findall(r"(?is)<h1[^>]*>(.*?)</h1>", h)]
    vis = texto_visivel(h)
    erros = [e for e in ERROS_VISIVEIS if e.lower() in vis.lower()]
    imgs = re.findall(r"(?is)<img\b[^>]*>", h)
    sem_alt = [i for i in imgs if not re.search(r'alt="[^"]+"', i)]
    links = set()
    for href in re.findall(r'(?i)href="([^"#]+)', h):
        href = html.unescape(href)
        if href.startswith(("mailto:", "tel:", "javascript:")):
            continue
        absl = urljoin(url, href)
        if "wp-json" in absl or "xmlrpc" in absl or absl.endswith((".css", ".js")) or "/feed" in absl or "wp-content" in absl:
            continue
        if urlparse(absl).netloc in ("comprenolink.net", "meli.la") or "mercadolivre" in absl:
            links.add(absl.split("?utm")[0] if "comprenolink.net" in absl else absl)
    return dict(caminho=caminho, status=st, final=final, titulo=titulo, desc=html.unescape(desc[1]) if desc else "",
                h1=[x for x in h1s if x], erros=erros, imgs=len(imgs), sem_alt=len(sem_alt), seg=seg, kb=tam / 1024,
                links=links, cache=None)


def checar_link(url):
    st, final, _h, seg, _t = baixar(url)
    ok = 200 <= st < 400
    if "meli.la" in url:
        ok = ok and "mercadolivre" in final
    return url, st, final, ok, seg


def main():
    print("Testando páginas...")
    with ThreadPoolExecutor(3) as ex:
        paginas = list(ex.map(analisar_pagina, PAGINAS))
        extras = list(ex.map(analisar_pagina, EXTRAS))
    todos = sorted(set().union(*[p["links"] for p in paginas]))
    print(f"Testando {len(todos)} links...")
    with ThreadPoolExecutor(4) as ex:
        res_links = list(ex.map(checar_link, todos))

    problemas = []
    for p in paginas:
        if p["status"] != 200:
            problemas.append(f"{p['caminho']}: status {p['status']}")
        if len(p["h1"]) != 1:
            problemas.append(f"{p['caminho']}: {len(p['h1'])} títulos H1 ({' / '.join(p['h1'])})")
        if not p["desc"]:
            problemas.append(f"{p['caminho']}: sem meta descrição")
        if p["titulo"].startswith(("-", " -")) or len(p["titulo"]) < 10:
            problemas.append(f"{p['caminho']}: título fraco '{p['titulo']}'")
        for e in p["erros"]:
            problemas.append(f"{p['caminho']}: texto indevido visível '{e}'")
        if p["sem_alt"]:
            problemas.append(f"{p['caminho']}: {p['sem_alt']} imagem(ns) sem texto alternativo")
    for e in extras:
        for x in e["erros"]:
            problemas.append(f"{e['caminho']}: texto indevido visível '{x}'")
    for url, st, final, ok, _s in res_links:
        if not ok:
            problemas.append(f"link com problema: {url} → {st} {final}")

    agora = datetime.now()
    linhas_p = "".join(
        f"<tr><td>{p['caminho']}</td><td class={'ok' if p['status'] == 200 else 'ruim'}>{p['status']}</td><td>{html.escape(p['titulo'])}</td>"
        f"<td>{html.escape(' / '.join(p['h1']))}</td><td>{'✔' if p['desc'] else '✘'}</td><td>{p['imgs']}</td><td>{p['seg']:.1f}s · {p['kb']:.0f} KB</td>"
        f"<td class={'ok' if not p['erros'] else 'ruim'}>{', '.join(p['erros']) or 'nenhum'}</td></tr>" for p in paginas)
    linhas_e = "".join(
        f"<tr><td>{e['caminho']}</td><td>{e['status']}</td><td>{html.escape(e['final'].split('?teste')[0])}</td><td>{html.escape(e['titulo'])}</td>"
        f"<td class={'ok' if not e['erros'] else 'ruim'}>{', '.join(e['erros']) or 'nenhum'}</td></tr>" for e in extras)
    linhas_l = "".join(
        f"<tr><td>{html.escape(u)}</td><td class={'ok' if ok else 'ruim'}>{st}</td><td>{html.escape(f[:90])}</td><td>{s:.1f}s</td></tr>"
        for u, st, f, ok, s in res_links)
    lista_prob = "".join(f"<li>{html.escape(x)}</li>" for x in problemas) or "<li class=ok>Nenhum problema encontrado.</li>"
    rel = f"""<!doctype html><html lang=pt-br><meta charset=utf-8><meta name=viewport content="width=device-width,initial-scale=1">
<title>Teste do site {agora:%d/%m/%Y %H:%M}</title>
<style>body{{font-family:Segoe UI,Arial,sans-serif;margin:24px;color:#1f2937}}h1{{color:#1F2A44}}table{{border-collapse:collapse;width:100%;margin:10px 0 28px;font-size:13px}}
th{{background:#1F2A44;color:#fff;text-align:left}}td,th{{border:1px solid #ddd;padding:6px;vertical-align:top}}.ok{{color:#2E7D32;font-weight:600}}.ruim{{color:#C62828;font-weight:700}}</style>
<h1>Check completo – comprenolink.net</h1><p>Gerado em {agora:%d/%m/%Y às %H:%M}. {len(paginas)} páginas, {len(extras)} endereços extras, {len(res_links)} links testados.</p>
<h2>Problemas ({len(problemas)})</h2><ul>{lista_prob}</ul>
<h2>Páginas</h2><table><tr><th>Página</th><th>Status</th><th>Título</th><th>H1</th><th>Descrição</th><th>Imagens</th><th>Tempo · tamanho</th><th>Textos indevidos</th></tr>{linhas_p}</table>
<h2>Endereços extras (antigos e padrão do WordPress)</h2><table><tr><th>Endereço</th><th>Status</th><th>Foi para</th><th>Título</th><th>Textos indevidos</th></tr>{linhas_e}</table>
<h2>Links</h2><table><tr><th>Link</th><th>Status</th><th>Destino final</th><th>Tempo</th></tr>{linhas_l}</table></html>"""
    saida = os.path.join(PASTA, f"teste_site_{agora:%Y-%m-%d_%Hh%M}.html")
    with open(saida, "w", encoding="utf-8") as f:
        f.write(rel)
    print(f"\n{len(problemas)} problema(s):")
    for x in problemas:
        print(" -", x)
    print("\nExtras:")
    for e in extras:
        print(f" {e['caminho']:28} {e['status']}  -> {e['final'].split('?teste')[0]}  | {e['titulo'][:60]} | {e['erros']}")
    print("\nRelatório:", saida)


if __name__ == "__main__":
    main()
