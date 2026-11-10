#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Núcleo de manutenção do blog https://comprenolink.net/melhores-produtos-mercado-livre-2026/ (WordPress/Hostinger).

Lê a página do guia pela API oficial do WordPress (REST API) e sabe ler/editar/remover/adicionar anúncios
(produtos) dentro dela, mantendo tudo consistente: numeração, âncoras internas (#item-N), a tabela
"Escolha rápida" e o texto "reunimos N modelos" / "Atualizado em".

Este arquivo é a base usada por painel_blog.py (aplicação web). Também funciona sozinho por linha de
comando (ver --help), útil para automação ou depuração.

SEGURANÇA
  * Nada é enviado ao site sem confirmação explícita.
  * Antes de QUALQUER publicação o conteúdo atual do site é salvo em backups\\.
  * Usa "Senha de aplicativo" do WordPress (revogável), nunca a senha de login do WordPress/Hostinger.
    Guarde em wp_credenciais.json (copie de wp_credenciais.exemplo.json).
"""
import argparse
import base64
import difflib
import html
import json
import os
import re
import sys
import urllib.error
import urllib.request
from datetime import datetime

PASTA = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))


def pasta_dados_de(pasta_programa):
    # Estrutura Gestao_Anuncios_Blog: programas em 1_PROGRAMAS\Blog_WordPress, dados em 2_DADOS\Blog_WordPress.
    # O pacote do outro PC (4_PACOTE_OUTRO_PC) tem a mesma estrutura. Sem ela, os dados ficam ao lado do programa.
    base = os.path.normpath(os.path.join(pasta_programa, "..", ".."))
    # Pacote ainda dentro da Gestao_Anuncios_Blog (neste PC): usa o 2_DADOS principal, para a senha e os
    # backups nunca irem parar no pacote (e no .zip). Copiado para o outro PC, o pacote usa o próprio 2_DADOS.
    principal = os.path.join(os.path.dirname(base), "2_DADOS", "Blog_WordPress")
    if os.path.basename(base).upper() == "4_PACOTE_OUTRO_PC" and os.path.isdir(principal):
        return principal
    estruturada = os.path.join(base, "2_DADOS", "Blog_WordPress")
    return estruturada if os.path.isdir(estruturada) else pasta_programa


def _pasta_dados():
    if os.environ.get("BLOG_WP_DADOS"):
        return os.environ["BLOG_WP_DADOS"]
    return pasta_dados_de(PASTA)


PASTA_DADOS = _pasta_dados()
ARQ_CRED = os.path.join(PASTA_DADOS, "wp_credenciais.json")
PASTA_BACKUP = os.path.join(PASTA_DADOS, "backups")
ARQ_DIFF = os.path.join(PASTA_DADOS, "ultimo_diff.txt")


class Erro(Exception):
    pass


# ----------------------------------------------------------------------------- configuração / API
def carregar_config():
    cfg = {"site": "https://comprenolink.net", "pagina_id": 5, "usuario": "", "senha_aplicativo": ""}
    if os.path.exists(ARQ_CRED):
        with open(ARQ_CRED, encoding="utf-8-sig") as f:
            cfg.update(json.load(f))
    cfg["usuario"] = os.environ.get("WP_USER", cfg.get("usuario", ""))
    cfg["senha_aplicativo"] = os.environ.get("WP_APP_PASSWORD", cfg.get("senha_aplicativo", ""))
    cfg["site"] = cfg["site"].rstrip("/")
    return cfg


def requisitar(cfg, metodo, caminho, corpo=None):
    if not cfg["usuario"] or not cfg["senha_aplicativo"]:
        raise Erro("Faltam as credenciais. Copie wp_credenciais.exemplo.json para wp_credenciais.json e preencha "
                   "'usuario' e 'senha_aplicativo' (veja o LEIA-ME).")
    token = base64.b64encode(f'{cfg["usuario"]}:{cfg["senha_aplicativo"]}'.encode("utf-8")).decode("ascii")
    # X-WP-Auth: cópia do login para quando a hospedagem remove o Authorization (snippet 2_snippet_login_painel.php)
    cab = {"Accept": "application/json", "User-Agent": "ManutencaoBlog/1.0", "Authorization": "Basic " + token,
           "X-WP-Auth": "Basic " + token}
    dados = None
    if corpo is not None:
        dados = json.dumps(corpo).encode("utf-8")
        cab["Content-Type"] = "application/json"
    req = urllib.request.Request(cfg["site"] + caminho, data=dados, headers=cab, method=metodo)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        detalhe = e.read().decode("utf-8", "replace")[:300]
        if e.code == 401:
            codigo_wp = ""
            try:
                codigo_wp = json.loads(detalhe).get("code", "")
            except ValueError:
                pass
            # rest_forbidden_context também aparece quando ninguém autenticou: confirma em /users/me
            logado = False
            if codigo_wp == "rest_forbidden_context" and caminho != "/wp-json/wp/v2/users/me":
                try:
                    requisitar(cfg, "GET", "/wp-json/wp/v2/users/me")
                    logado = True
                except Erro:
                    pass
            if logado:
                raise Erro("401: a senha de aplicativo FUNCIONOU (autenticou certinho), mas esta conta do "
                           "WordPress não tem permissão para editar Páginas. No wp-admin, vá em Usuários, "
                           "abra esta conta e confira se a Função dela é Administrador ou Editor (Autor e "
                           "Colaborador não podem editar Páginas). " + detalhe)
            raise Erro("401: usuário/senha de aplicativo recusados — ou a hospedagem removeu o cabeçalho "
                       "Authorization (veja 'Se der erro 401' no LEIA-ME). " + detalhe)
        if e.code == 403:
            raise Erro("403: sem permissão para editar páginas (o usuário precisa ser Administrador/Editor) "
                       "ou o firewall bloqueou o pedido. " + detalhe)
        if e.code == 404:
            raise Erro("404: página não encontrada — confira 'pagina_id' em wp_credenciais.json. " + detalhe)
        raise Erro(f"Erro HTTP {e.code}: {detalhe}")
    except urllib.error.URLError as e:
        raise Erro(f"Sem conexão com o site: {e.reason}")


class Pagina:
    def __init__(self, titulo, conteudo, modificado="", link=""):
        self.titulo, self.conteudo, self.modificado, self.link = titulo, conteudo, modificado, link


def baixar_pagina(cfg, offline=None):
    if offline:
        with open(offline, encoding="utf-8-sig") as f:
            c = f.read()
        return Pagina(f"Os {len(secoes(c))} Melhores Produtos do Mercado Livre em 2026", c, "(offline)", offline)
    d = requisitar(cfg, "GET", f"/wp-json/wp/v2/pages/{cfg['pagina_id']}?context=edit"
                               "&_fields=id,link,modified,status,title,content")
    return Pagina(d["title"]["raw"], d["content"]["raw"], d["modified"], d["link"])


# ----------------------------------------------------------------------------- leitura da estrutura
RE_ITEM = re.compile(r'<h2\b[^>]*\bid="item-(\d+)"[^>]*>(.*?)</h2>', re.S)
RE_FAQ = re.compile(r'<h2\b[^>]*\bid="perguntas-frequentes"[^>]*>')
RE_COMENT_H = re.compile(r'<!--\s*wp:heading\b[^>]*-->\s*$')
RE_HEAD_INNER = re.compile(r'\s*(\d+)\.(\s*)<a\b([^>]*?)href="([^"]*)"([^>]*)>(.*?)</a>(.*)$', re.S)


def _inicio_bloco(s, pos):
    m = RE_COMENT_H.search(s[:pos])
    return m.start() if m else pos


def secoes(s):
    achados = list(RE_ITEM.finditer(s))
    if not achados:
        return []
    faq = RE_FAQ.search(s)
    if faq:
        fim_global = _inicio_bloco(s, faq.start())
    else:
        prox = re.compile(r'<h2\b').search(s, achados[-1].end())
        fim_global = _inicio_bloco(s, prox.start()) if prox else len(s)
    inicios = [_inicio_bloco(s, m.start()) for m in achados]
    res = []
    for i, m in enumerate(achados):
        fim = inicios[i + 1] if i + 1 < len(inicios) else fim_global
        res.append({"n": int(m.group(1)), "ini": inicios[i], "fim": fim})
    return res


def _sec(s, n):
    for x in secoes(s):
        if x["n"] == n:
            return x
    raise Erro(f"Não existe o item {n}. Itens atuais: 1 a {len(secoes(s))}.")


def _texto(trecho):
    return html.unescape(re.sub(r"<[^>]+>", "", trecho)).strip()


def _lista(texto, rotulo):
    m = re.search(r'<h3\b[^>]*>\s*' + re.escape(rotulo) + r'\s*</h3>', texto)
    if not m:
        return None
    u = re.compile(r'<ul\b[^>]*>(.*?)</ul>', re.S).search(texto, m.end())
    if not u:
        return None
    itens = [_texto(x) for x in re.findall(r'<li\b[^>]*>(.*?)</li>', u.group(1), re.S)]
    return u.start(1), u.end(1), itens, "wp:list-item" in u.group(1)


def ler_item(texto):
    h = RE_ITEM.search(texto)
    mh = RE_HEAD_INNER.match(h.group(2))
    d = {"n": int(h.group(1)), "nome": "", "link": "", "selo": "", "desc": "", "preco": "", "imagem": "",
         "titulo_anuncio": "", "beneficios": [], "ideal": []}
    if mh:
        d["nome"], d["link"] = _texto(mh.group(6)), html.unescape(mh.group(4))
        d["selo"] = re.sub(r'^[\s⭐]+', "", _texto(mh.group(7)))
    else:
        d["nome"] = _texto(h.group(2))
    p = re.search(r'<p\b[^>]*>(.*?)</p>', texto[h.end():], re.S)
    d["desc"] = _texto(p.group(1)) if p else ""
    m = re.search(r'product-price">\s*(.*?)\s*</div>', texto, re.S)
    d["preco"] = _texto(m.group(1)) if m else ""
    m = re.search(r'<img\b[^>]*\bsrc="([^"]*)"', texto)
    d["imagem"] = m.group(1) if m else ""
    m = re.search(r'product-title">.*?<h3>\s*(.*?)\s*</h3>', texto, re.S)
    d["titulo_anuncio"] = _texto(m.group(1)) if m else ""
    # Bloco dinâmico do plugin Hostinger Affiliate: foto/título ficam nos atributos JSON e o preço é
    # buscado no Mercado Livre na hora de mostrar a página (não fica salvo no conteúdo)
    d["preco_auto"] = False
    mb = re.search(r'<!--\s*wp:hostinger-affiliate-plugin/[\w-]+\s+(\{.*?\})\s*/?-->', texto, re.S)
    if mb:
        try:
            attrs = json.loads(mb.group(1))
        except ValueError:
            attrs = {}
        prod = next(iter((attrs.get("items") or {}).values()), {})
        d["imagem"] = d["imagem"] or prod.get("image_url", "")
        d["titulo_anuncio"] = d["titulo_anuncio"] or prod.get("title", "")
        d["preco_auto"] = not d["preco"]
    for chave, rot in (("beneficios", "Benefícios"), ("ideal", "Ideal para")):
        r = _lista(texto, rot)
        d[chave] = r[2] if r else []
    return d


def itens(s):
    return [ler_item(s[x["ini"]:x["fim"]]) for x in secoes(s)]


# ----------------------------------------------------------------------------- alterações (funções puras)
def _renumerar_titulos(s):
    """Garante que o 'N.' no início de cada <h2 id="item-N"> bate com o id."""
    def troca(m):
        n = m.group(1)
        inner = re.sub(r'^(\s*)\d+\.', lambda k: f"{k.group(1)}{n}.", m.group(2), count=1)
        return m.group(0).replace(m.group(2), inner, 1)
    return RE_ITEM.sub(troca, s)


def _linha_tabela(s, n):
    m = re.search(r'<tr>(?:(?!</tr>).)*?href="#item-%d"(?:(?!</tr>).)*?</tr>' % n, s, re.S)
    return (m.start(), m.end()) if m else None


def remover_item(s, n):
    x = _sec(s, n)
    total = len(secoes(s))
    s = s[:x["ini"]] + s[x["fim"]:]
    lt = _linha_tabela(s, n)
    if lt:
        s = s[:lt[0]] + s[lt[1]:]
    s = re.sub(r'(id="item-|href="#item-)(\d+)(")',
               lambda m: m.group(1) + str(int(m.group(2)) - 1 if int(m.group(2)) > n else int(m.group(2))) + m.group(3), s)
    return _renumerar_titulos(s), total - 1


def _ul(itens_txt, com_coment):
    partes = []
    for t in itens_txt:
        li = f"<li>{html.escape(t, quote=False)}</li>"
        partes.append(f"<!-- wp:list-item -->\n{li}\n<!-- /wp:list-item -->" if com_coment else li)
    return "\n\n".join(partes)


def _link_ok(url):
    if not re.match(r'^https?://[^\s"<>]+$', url or ""):
        raise Erro(f"Link inválido: {url!r} (use o link completo, ex.: https://meli.la/XXXX).")
    return url


def montar_secao(n, d, com_coment):
    c = lambda abre, corpo, fecha: (f"<!-- wp:{abre} -->\n{corpo}\n<!-- /wp:{fecha} -->" if com_coment else corpo)
    esc = lambda t: html.escape(t or "", quote=False)
    link = _link_ok(d["link"])
    selo = f"⭐ {esc(d['selo'])}" if d.get("selo") else ""
    partes = [c('heading {"level":2}',
                f'<h2 id="item-{n}" class="wp-block-heading">{n}.<a href="{link}" target="_blank" '
                f'rel="sponsored nofollow noopener">{esc(d["nome"])}</a>{selo}</h2>', "heading")]
    if d.get("desc"):
        partes.append(c("paragraph", f'<p class="wp-block-paragraph">{esc(d["desc"])}</p>', "paragraph"))
    tit = esc(d.get("titulo_anuncio") or d["nome"])
    rel = 'target="_blank" rel="sponsored noopener noreferrer"'
    card = '<div class="hostinger-affiliate-block-single-type">'
    if d.get("imagem"):
        card += (f'<div class="hostinger-affiliate-block-single-type__image"><a href="{link}" {rel}>'
                 f'<img decoding="async" src="{html.escape(d["imagem"])}" alt="{tit}"></a></div>')
    card += (f'<div class="hostinger-affiliate-block-single-type__product-data">'
             f'<div class="hostinger-affiliate-block-single-type__product-title"><a href="{link}" {rel}><h3>{tit}</h3></a></div>'
             f'<div class="hostinger-affiliate-block-single-type__product-actions">')
    # Sem preço no cartão (muda no Mercado Livre; o snippet "Sem preço nos cartões" tira também dos antigos)
    card += (f'<div class="hostinger-affiliate-block-single-type__product-button-wrap"><a href="{link}" '
             f'class="hostinger-affiliate-block-single-type__product-buy-button" {rel}>Compre agora</a></div>'
             f'</div></div></div>')
    partes.append(c("html", card, "html"))
    for chave, rot in (("beneficios", "Benefícios"), ("ideal", "Ideal para")):
        if d.get(chave):
            partes.append(c('heading {"level":3,"className":"cnl-sub"}',
                            f'<h3 class="wp-block-heading cnl-sub">{rot}</h3>', "heading"))
            partes.append(c("list", f'<ul class="wp-block-list">\n{_ul(d[chave], com_coment)}\n</ul>', "list"))
    return "\n\n".join(partes) + "\n\n"


def adicionar_item(s, d, posicao=None, linha_tabela=None):
    total = len(secoes(s))
    if total == 0:
        raise Erro("Não achei nenhum item (<h2 id=\"item-N\">) na página.")
    pos = total + 1 if not posicao else max(1, min(int(posicao), total + 1))
    s = re.sub(r'(id="item-|href="#item-)(\d+)(")',
               lambda m: m.group(1) + str(int(m.group(2)) + 1 if int(m.group(2)) >= pos else int(m.group(2))) + m.group(3), s)
    s = _renumerar_titulos(s)
    secs = secoes(s)
    ponto = next((x["ini"] for x in secs if x["n"] > pos), secs[-1]["fim"])
    nova = montar_secao(pos, d, "<!-- wp:" in s)
    s = s[:ponto] + nova + s[ponto:]
    if linha_tabela:
        tr = (f'<tr><td>{html.escape(linha_tabela, quote=False)}</td><td><a href="#item-{pos}">{html.escape(d["nome"], quote=False)}</a>'
              f'</td><td><a href="{d["link"]}" target="_blank" rel="sponsored nofollow noopener">Ver preço</a></td></tr>')
        i = s.find("</tbody>", s.find("escolha"))
        if i != -1:
            s = s[:i] + tr + s[i:]
    return s, pos, total + 1


def editar_item(s, n, c):
    """c: dict com nome, link, selo, desc, beneficios(list), ideal(list), titulo_anuncio, preco, imagem."""
    x = _sec(s, n)
    t = s[x["ini"]:x["fim"]]
    antigo = ler_item(t)
    avisos = []
    h = RE_ITEM.search(t)
    if any(c.get(k) for k in ("nome", "link", "selo")):
        mh = RE_HEAD_INNER.match(h.group(2))
        if not mh:
            avisos.append("Título do item fora do padrão: nome/link/selo não alterados (use 'substituir').")
        else:
            link = _link_ok(c["link"]) if c.get("link") else mh.group(4)
            nome = html.escape(c["nome"], quote=False) if c.get("nome") else mh.group(6)
            resto = mh.group(7)
            if c.get("selo"):
                resto = re.sub(r'^(\s*(?:⭐)?\s*).*$', lambda k: (k.group(1) or "⭐ ") + html.escape(c["selo"], quote=False),
                               resto, flags=re.S) if resto.strip() else "⭐ " + html.escape(c["selo"], quote=False)
            novo_inner = f'{mh.group(1)}.{mh.group(2)}<a{mh.group(3)}href="{link}"{mh.group(5)}>{nome}</a>{resto}'
            t = t[:h.start(2)] + novo_inner + t[h.end(2):]
            if c.get("link") and antigo["link"] and antigo["link"] != link:
                t = t.replace(antigo["link"], link)
                lt = _linha_tabela(s, n)
                if lt:
                    s = s[:lt[0]] + s[lt[0]:lt[1]].replace(antigo["link"], link) + s[lt[1]:]
                    x = _sec(s, n)
    if c.get("desc"):
        h = RE_ITEM.search(t)
        p = re.compile(r'(<p\b[^>]*>)(.*?)(</p>)', re.S).search(t, h.end())
        if p:
            t = t[:p.start(2)] + html.escape(c["desc"], quote=False) + t[p.end(2):]
        else:
            avisos.append("Descrição não encontrada neste item.")
    for chave, rot in (("beneficios", "Benefícios"), ("ideal", "Ideal para")):
        if c.get(chave):
            r = _lista(t, rot)
            if r:
                t = t[:r[0]] + "\n" + _ul(c[chave], r[3]) + "\n" + t[r[1]:]
            else:
                avisos.append(f"Lista '{rot}' não encontrada neste item.")
    for chave, padrao, nome_campo in (("preco", r'(product-price">\s*)(.*?)(\s*</div>)', "preço"),
                                      ("imagem", r'(<img\b[^>]*\bsrc=")([^"]*)(")', "imagem"),
                                      ("titulo_anuncio", r'(product-title">.*?<h3>\s*)(.*?)(\s*</h3>)', "título do anúncio")):
        if c.get(chave):
            m = re.search(padrao, t, re.S)
            if m:
                novo = html.escape(c[chave], quote=False) if chave != "imagem" else html.escape(c[chave])
                t = t[:m.start(2)] + novo + t[m.end(2):]
            else:
                avisos.append(f"Campo '{nome_campo}' não encontrado no cartão deste item (edite pelo editor do WordPress "
                              "ou use 'substituir').")
    return s[:x["ini"]] + t + s[x["fim"]:], avisos


def normalizar(s, titulo):
    n = len(secoes(s))
    hoje = datetime.now().strftime("%d/%m/%Y")
    s = re.sub(r'(Os\s+)\d+(\s+Melhores)', rf'\g<1>{n}\g<2>', s, count=1)
    s = re.sub(r'(reunimos\s+)\d+(\s+dos\s+modelos)', rf'\g<1>{n}\g<2>', s, count=1)
    s = re.sub(r'(Atualizado em\s+)\d{2}/\d{2}/\d{4}', rf'\g<1>{hoje}', s, count=1)
    titulo = re.sub(r'(Os\s+)\d+(\s+Melhores)', rf'\g<1>{n}\g<2>', titulo, count=1)
    return s, titulo


def verificar(s):
    """Confere a coerência da página; devolve lista de problemas (vazia = ok)."""
    sec = secoes(s)
    nums = [x["n"] for x in sec]
    prob = []
    if nums != list(range(1, len(nums) + 1)):
        prob.append(f"Numeração dos itens fora de ordem: {nums}")
    ids = re.findall(r'\bid="([^"]+)"', s)
    dup = {i for i in ids if ids.count(i) > 1}
    if dup:
        prob.append(f"ids repetidos: {sorted(dup)}")
    for m in re.finditer(r'href="#(item-\d+)"', s):
        if m.group(1) not in ids:
            prob.append(f"Âncora quebrada: #{m.group(1)}")
            break
    for x in sec:
        h = RE_ITEM.search(s[x["ini"]:x["fim"]])
        m = re.match(r'\s*(\d+)\.', h.group(2))
        if not m or int(m.group(1)) != x["n"]:
            prob.append(f"Título do item {x['n']} com número diferente do id.")
    return prob


# ----------------------------------------------------------------------------- publicar / backup / diff
def salvar_backup(p, rotulo="pagina"):
    os.makedirs(PASTA_BACKUP, exist_ok=True)
    base = os.path.join(PASTA_BACKUP, f"{rotulo}_{datetime.now():%Y-%m-%d_%Hh%M%S}")
    with open(base + ".html", "w", encoding="utf-8", newline="") as f:
        f.write(p.conteudo)
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump({"titulo": p.titulo, "modificado": p.modificado, "link": p.link}, f, ensure_ascii=False, indent=2)
    return base + ".html"


_ROTULOS = [("nome", "nome"), ("link", "link"), ("selo", "selo"), ("preco", "preço"),
            ("titulo_anuncio", "título do anúncio"), ("desc", "descrição"), ("beneficios", "benefícios"),
            ("ideal", "ideal para"), ("imagem", "imagem")]


def _cortar(t, n=70):
    t = " | ".join(t) if isinstance(t, list) else str(t or "")
    t = t or "(vazio)"
    return t if len(t) <= n else t[:n - 3] + "..."


def resumo_mudancas(antigo, novo):
    """Resumo em português do que mudou (para quem não lê HTML)."""
    a, b = itens(antigo), itens(novo)
    linhas = []

    def dif(x, y):
        for k, rot in _ROTULOS:
            if x[k] != y[k]:
                linhas.append(f"  Item {y['n']} ({_cortar(y['nome'], 28)}) - {rot}: {_cortar(x[k])}  ->  {_cortar(y[k])}")

    if len(a) == len(b):
        for x, y in zip(a, b):
            dif(x, y)
    else:
        la, lb = {x["link"]: x for x in a if x["link"]}, {y["link"]: y for y in b if y["link"]}
        for x in a:
            if x["link"] not in lb:
                linhas.append(f"  REMOVIDO:   item {x['n']} - {x['nome']}")
        for y in b:
            if y["link"] not in la:
                extra = "  ".join(v for v in (f"[{y['selo']}]" if y["selo"] else "", y["preco"]) if v)
                linhas.append(f"  ADICIONADO: item {y['n']} - {y['nome']}  {extra}".rstrip())
        mov = sum(1 for y in b if y["link"] in la and la[y["link"]]["n"] != y["n"])
        if mov:
            linhas.append(f"  {mov} anúncio(s) mantido(s) foram renumerados automaticamente.")
        for y in b:
            if y["link"] in la:
                dif(la[y["link"]], y)
    n_ant, n_nov = antigo.count("<tr>"), novo.count("<tr>")
    if n_ant != n_nov:
        linhas.append(f"  Tabela 'Escolha rápida': {n_ant - 1} -> {n_nov - 1} linha(s)")
    for padrao, rot in ((r'reunimos\s+(\d+)', "Texto 'reunimos N modelos'"), (r'Atualizado em\s+([\d/]+)', "Data 'Atualizado em'")):
        x, y = re.search(padrao, antigo), re.search(padrao, novo)
        if x and y and x.group(1) != y.group(1):
            linhas.append(f"  {rot}: {x.group(1)}  ->  {y.group(1)}")
    return linhas


def mostrar_diff(antigo, novo):
    d = list(difflib.unified_diff(antigo.splitlines(), novo.splitlines(), "site (atual)", "novo", lineterm="", n=1))
    with open(ARQ_DIFF, "w", encoding="utf-8") as f:
        f.write("\n".join(d))
    resumo = resumo_mudancas(antigo, novo)
    print("\n=== RESUMO DA MUDANÇA (leia antes de confirmar) ===")
    for linha in resumo or ["  Alteração de texto fora dos anúncios (detalhes técnicos no arquivo abaixo)."]:
        print(linha)
    print(f"(detalhes técnicos, se precisar: {ARQ_DIFF})")


def publicar(cfg, original, conteudo, titulo, offline=None):
    if offline:
        saida = os.path.join(PASTA_DADOS, "saida_offline.html")
        with open(saida, "w", encoding="utf-8", newline="") as f:
            f.write(conteudo)
        print(f"[offline] resultado gravado em {saida} (nada foi enviado ao site).")
        return
    bk = salvar_backup(original)
    print(f"Backup do conteúdo atual salvo em: {bk}")
    corpo = {"content": conteudo}
    if titulo and titulo != original.titulo:
        corpo["title"] = titulo
    r = requisitar(cfg, "POST", f"/wp-json/wp/v2/pages/{cfg['pagina_id']}", corpo)
    print(f"PUBLICADO. Página: {r.get('link')}  (modificada em {r.get('modified')})")
    aquecer_cache(r.get("link"))
    print("Obs.: o cache do site (LiteSpeed/Hostinger CDN) pode levar alguns minutos para mostrar a mudança.")


def aquecer_cache(url):
    """Depois de publicar, o LiteSpeed limpa o cache e o 1º visitante esperaria ~10 s para o Guia (200 cartões)
    ser montado. Visitamos a página uma vez aqui para que o visitante já receba a versão pronta do cache."""
    if not url:
        return
    import time
    import urllib.request
    for aparelho, ua in (("computador", "Mozilla/5.0 (Windows NT 10.0) Chrome/130"),
                         ("celular", "Mozilla/5.0 (Linux; Android 13) Chrome/130 Mobile")):  # o cache pode separar os dois
        t0 = time.time()
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": ua}), timeout=60) as resp:
                resp.read()
            print(f"cache aquecido ({aparelho}) em {time.time() - t0:.1f} s")
        except Exception as erro:  # não é crítico: só deixa o 1º visitante mais lento
            print(f"aviso: não consegui aquecer o cache ({aparelho}): {erro}")


def efetivar(cfg, args, original, conteudo, titulo, confirmar_agora=False):
    prob = verificar(conteudo)
    if prob:
        raise Erro("Verificação falhou, nada será publicado:\n  - " + "\n  - ".join(prob))
    if conteudo == original.conteudo and titulo == original.titulo:
        print("Nenhuma mudança a aplicar.")
        return
    mostrar_diff(original.conteudo, conteudo)
    if titulo != original.titulo:
        print(f"Título: {original.titulo!r} -> {titulo!r}")
    ok = args.aplicar
    if not ok and confirmar_agora:
        ok = input("\nAplicar no site AGORA? (s/N): ").strip().lower() in ("s", "sim")
    if ok:
        publicar(cfg, original, conteudo, titulo, args.offline)
    else:
        print("\n(Pré-visualização apenas. Para publicar, repita o comando com --aplicar.)")


# ----------------------------------------------------------------------------- comandos (linha de comando)
def _lista_pipe(v):
    return [x.strip() for x in v.split("|") if x.strip()] if v else None


def testar_conexao(cfg):
    """Tenta identificar o usuário (não essencial) e, principalmente, se ele consegue editar a página do
    guia — que é o que realmente importa. /users/me?context=edit exige a capacidade 'list_users' (só
    Administrador), então mesmo uma conta Editora válida falharia nele; por isso não é tratado como erro."""
    nome_usuario = None
    try:
        u = requisitar(cfg, "GET", "/wp-json/wp/v2/users/me&_fields=id,name")
        nome_usuario = u.get("name")
    except Erro:
        pass
    p = baixar_pagina(cfg)
    prob = verificar(p.conteudo)
    return {"nome_usuario": nome_usuario, "titulo_pagina": p.titulo, "total_itens": len(secoes(p.conteudo)),
            "modificado": p.modificado, "link": p.link, "problemas": prob}


def cmd_testar(cfg, args):
    r = testar_conexao(cfg)
    if r["nome_usuario"]:
        print(f"Conectado como: {r['nome_usuario']}")
    print(f"Consegue editar a página do guia: SIM (autenticação e permissão OK)")
    print(f"Página {cfg['pagina_id']}: {r['titulo_pagina']!r} — {r['total_itens']} itens — modificada em {r['modificado']}")
    print(f"Link: {r['link']}")
    print("Estrutura da página: OK" if not r["problemas"] else "Atenção: " + "; ".join(r["problemas"]))


def cmd_listar(cfg, args):
    p = baixar_pagina(cfg, args.offline)
    print(f"{p.titulo}  ({len(secoes(p.conteudo))} itens)  — {p.link}\n")
    for d in itens(p.conteudo):
        print(f"{d['n']:>2}. {d['nome']}  [{d['selo']}]  {d['preco'] or ('preço automático (ML)' if d.get('preco_auto') else '')}")
        print(f"      {d['link'] or '(sem link)'}")


def cmd_mostrar(cfg, args):
    p = baixar_pagina(cfg, args.offline)
    x = _sec(p.conteudo, args.n)
    print(p.conteudo[x["ini"]:x["fim"]])


def cmd_editar(cfg, args, confirmar=False):
    p = baixar_pagina(cfg, args.offline)
    campos = {"nome": args.nome, "link": args.link, "selo": args.selo, "desc": args.desc,
              "beneficios": _lista_pipe(args.beneficios), "ideal": _lista_pipe(args.ideal),
              "titulo_anuncio": args.titulo_anuncio, "preco": args.preco, "imagem": args.imagem}
    if not any(campos.values()):
        raise Erro("Informe pelo menos um campo para alterar (--nome, --link, --selo, --desc, --beneficios, "
                   "--ideal, --titulo-anuncio, --preco, --imagem).")
    novo, avisos = editar_item(p.conteudo, args.n, campos)
    for a in avisos:
        print("ATENÇÃO:", a)
    efetivar(cfg, args, p, novo, p.titulo, confirmar)


def cmd_remover(cfg, args, confirmar=False):
    p = baixar_pagina(cfg, args.offline)
    d = ler_item(p.conteudo[_sec(p.conteudo, args.n)["ini"]:_sec(p.conteudo, args.n)["fim"]])
    print(f"Removendo o item {args.n}: {d['nome']}  ({d['link']})")
    novo, total = remover_item(p.conteudo, args.n)
    novo, titulo = normalizar(novo, p.titulo)
    print(f"Os itens seguintes foram renumerados; agora são {total} itens.")
    efetivar(cfg, args, p, novo, titulo, confirmar)


def cmd_adicionar(cfg, args, confirmar=False):
    p = baixar_pagina(cfg, args.offline)
    if not args.nome or not args.link:
        raise Erro("Para adicionar informe pelo menos --nome e --link.")
    d = {"nome": args.nome, "link": args.link, "selo": args.selo, "desc": args.desc,
         "titulo_anuncio": args.titulo_anuncio, "preco": args.preco, "imagem": args.imagem,
         "beneficios": _lista_pipe(args.beneficios), "ideal": _lista_pipe(args.ideal)}
    novo, pos, total = adicionar_item(p.conteudo, d, args.posicao, args.linha_tabela)
    novo, titulo = normalizar(novo, p.titulo)
    print(f"Novo item entrará na posição {pos}; agora são {total} itens.")
    efetivar(cfg, args, p, novo, titulo, confirmar)


def cmd_substituir(cfg, args, confirmar=False):
    p = baixar_pagina(cfg, args.offline)
    qtd = p.conteudo.count(args.antigo)
    print(f"{qtd} ocorrência(s) de {args.antigo!r} na página.")
    if not qtd:
        return
    efetivar(cfg, args, p, p.conteudo.replace(args.antigo, args.novo), p.titulo, confirmar)


def cmd_backup(cfg, args):
    p = baixar_pagina(cfg, args.offline)
    print("Backup salvo em:", salvar_backup(p))


def cmd_restaurar(cfg, args, confirmar=False):
    p = baixar_pagina(cfg, args.offline)
    with open(args.arquivo, encoding="utf-8-sig") as f:
        conteudo = f.read()
    titulo = p.titulo
    j = os.path.splitext(args.arquivo)[0] + ".json"
    if os.path.exists(j):
        with open(j, encoding="utf-8") as f:
            titulo = json.load(f).get("titulo", titulo)
    efetivar(cfg, args, p, conteudo, titulo, confirmar)


# ----------------------------------------------------------------------------- menu interativo (opcional)
def _perg(rotulo, obrig=False, atual=None):
    while True:
        dica = f" [{atual}]" if atual else ""
        v = input(f"{rotulo}{dica}: ").strip()
        if v:
            return v
        if not obrig:
            return None
        print("  (obrigatório)")


def _ns(**kw):
    base = dict(offline=None, aplicar=False, n=None, nome=None, link=None, selo=None, desc=None, beneficios=None,
                ideal=None, titulo_anuncio=None, preco=None, imagem=None, posicao=None, linha_tabela=None,
                antigo=None, novo=None, arquivo=None)
    base.update(kw)
    return argparse.Namespace(**base)


def menu(cfg, offline):
    while True:
        print("\n=== MANUTENÇÃO DO BLOG comprenolink.net ===" + ("  [MODO OFFLINE]" if offline else ""))
        print(" 1) Testar conexão          5) Adicionar anúncio")
        print(" 2) Listar anúncios         6) Buscar e substituir texto")
        print(" 3) Editar anúncio          7) Fazer backup agora")
        print(" 4) Remover anúncio         8) Restaurar um backup")
        print(" 0) Sair")
        op = input("Escolha: ").strip()
        try:
            if op == "0":
                return
            elif op == "1":
                cmd_testar(cfg, _ns())
            elif op == "2":
                cmd_listar(cfg, _ns(offline=offline))
            elif op == "3":
                cmd_listar(cfg, _ns(offline=offline))
                n = int(_perg("\nNúmero do anúncio a editar", True))
                print("Deixe em branco o que NÃO quer mudar. Listas: separe itens com |")
                cmd_editar(cfg, _ns(offline=offline, n=n, nome=_perg("Novo nome (título do item)"),
                                    link=_perg("Novo link meli.la"), selo=_perg("Novo selo (ex.: Mais Vendido)"),
                                    desc=_perg("Nova descrição"), beneficios=_perg("Novos benefícios (a|b|c)"),
                                    ideal=_perg("Novo 'Ideal para' (a|b|c)"),
                                    titulo_anuncio=_perg("Novo título completo do anúncio (cartão)"),
                                    preco=_perg("Novo preço (ex.: R$ 299,90)"), imagem=_perg("Nova URL da imagem")),
                           confirmar=True)
            elif op == "4":
                cmd_listar(cfg, _ns(offline=offline))
                n = int(_perg("\nNúmero do anúncio a REMOVER", True))
                cmd_remover(cfg, _ns(offline=offline, n=n), confirmar=True)
            elif op == "5":
                print("Preencha os dados do novo anúncio. Listas: separe itens com |")
                cmd_adicionar(cfg, _ns(offline=offline, nome=_perg("Nome curto do produto", True),
                                       link=_perg("Link meli.la do produto", True), selo=_perg("Selo (ex.: Novo)"),
                                       desc=_perg("Descrição curta"), titulo_anuncio=_perg("Título completo do anúncio (cartão)"),
                                       preco=_perg("Preço (ex.: R$ 299,90)"), imagem=_perg("URL da imagem do produto"),
                                       beneficios=_perg("Benefícios (a|b|c)"), ideal=_perg("Ideal para (a|b|c)"),
                                       posicao=_perg("Posição (vazio = no final)"),
                                       linha_tabela=_perg("Categoria p/ tabela 'Escolha rápida' (vazio = não incluir)")),
                              confirmar=True)
            elif op == "6":
                cmd_substituir(cfg, _ns(offline=offline, antigo=_perg("Texto a procurar", True),
                                        novo=input("Trocar por: ")), confirmar=True)
            elif op == "7":
                cmd_backup(cfg, _ns(offline=offline))
            elif op == "8":
                arqs = sorted(f for f in os.listdir(PASTA_BACKUP) if f.endswith(".html")) if os.path.isdir(PASTA_BACKUP) else []
                for i, f in enumerate(arqs, 1):
                    print(f"  {i}) {f}")
                if arqs:
                    i = int(_perg("Número do backup a restaurar", True))
                    cmd_restaurar(cfg, _ns(offline=offline, arquivo=os.path.join(PASTA_BACKUP, arqs[i - 1])), confirmar=True)
                else:
                    print("Ainda não há backups.")
        except Erro as e:
            print("\nERRO:", e)
        except (ValueError, IndexError):
            print("\nEntrada inválida.")
        except KeyboardInterrupt:
            print("\nCancelado.")


# ----------------------------------------------------------------------------- main
def montar_parser():
    ap = argparse.ArgumentParser(description="Núcleo de manutenção do blog comprenolink.net (WordPress)")
    ap.add_argument("--offline", metavar="ARQ.html", help="treinar usando um arquivo HTML local (não toca no site)")
    sp = ap.add_subparsers(dest="cmd")
    sp.add_parser("menu")
    sp.add_parser("testar")
    sp.add_parser("listar")
    sp.add_parser("backup")
    m = sp.add_parser("mostrar"); m.add_argument("n", type=int)
    campos = argparse.ArgumentParser(add_help=False)
    for f in ("nome", "link", "selo", "desc", "beneficios", "ideal", "titulo-anuncio", "preco", "imagem"):
        campos.add_argument("--" + f)
    ap_ = argparse.ArgumentParser(add_help=False); ap_.add_argument("--aplicar", action="store_true")
    e = sp.add_parser("editar", parents=[campos, ap_]); e.add_argument("n", type=int)
    r = sp.add_parser("remover", parents=[ap_]); r.add_argument("n", type=int)
    a = sp.add_parser("adicionar", parents=[campos, ap_]); a.add_argument("--posicao", type=int); a.add_argument("--linha-tabela")
    s = sp.add_parser("substituir", parents=[ap_]); s.add_argument("antigo"); s.add_argument("novo")
    rs = sp.add_parser("restaurar", parents=[ap_]); rs.add_argument("arquivo")
    return ap


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stdin.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    args = montar_parser().parse_args(argv)
    cfg = carregar_config()
    try:
        if args.cmd in (None, "menu"):
            return menu(cfg, args.offline)
        if not hasattr(args, "aplicar"):
            args.aplicar = False
        {"testar": cmd_testar, "listar": cmd_listar, "mostrar": cmd_mostrar, "editar": cmd_editar,
         "remover": cmd_remover, "adicionar": cmd_adicionar, "substituir": cmd_substituir,
         "backup": cmd_backup, "restaurar": cmd_restaurar}[args.cmd](cfg, args)
    except Erro as e:
        print("ERRO:", e)
        return 1
    return 0


if __name__ == "__main__":
    if getattr(sys, "frozen", False) and sys.platform == "win32":
        os.system("chcp 65001 >nul")
    try:
        codigo = main()
    except Exception:
        import traceback
        traceback.print_exc()
        codigo = 1
        if getattr(sys, "frozen", False):
            input("\nOcorreu um erro inesperado. Pressione ENTER para fechar...")
    sys.exit(codigo)
