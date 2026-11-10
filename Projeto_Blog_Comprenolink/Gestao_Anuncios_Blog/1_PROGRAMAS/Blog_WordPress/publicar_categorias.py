#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Coloca em produção a arquitetura de categorias (a mesma do esboço em 5_ESBOCO_CATEGORIAS).

O guia (página 5) continua sendo a ÚNICA fonte dos produtos. A partir dele e de
2_DADOS\\Blog_WordPress\\categorias.json este programa:
  1. cria/atualiza uma página por Categoria Pai com pelo menos `minimo_para_publicar` produtos
     (as categorias fracas ficam só no guia), com subcategorias e cartões curtos;
  2. cria/atualiza a página Black Friday (tag black-friday);
  3. refaz a tabela "Escolha rápida" do guia (o melhor de cada subcategoria = 1º do ranking);
  4. refaz a lista "Escolha por categoria" da Início, apontando para as páginas de categoria;
  5. monta no "Menu principal" o item "Categorias" (com as páginas) e o item da campanha.
Campanhas (tags com "campanha_ate" no categorias.json): enquanto valem, a Início ganha um botão e as
páginas de categoria uma faixa apontando para a página da campanha (Top 10 + resto por categoria).
A Black Friday vale até 30/11 e a página fica no ar (em 2027 é só trocar o ano); a página de Natal só é
publicada a partir de "a_partir_de" (01/12) e então toma o lugar da Black Friday no menu.
Os ids das páginas criadas ficam em 2_DADOS\\Blog_WordPress\\paginas_categorias.json.
Antes de mudar qualquer coisa salva backup (páginas e menu) em 2_DADOS\\Blog_WordPress\\backups.

Uso:  python publicar_categorias.py             -> só mostra o plano (nada é publicado)
      python publicar_categorias.py --publicar  -> publica
      python publicar_categorias.py --previa    -> gera prévia local em 3_DOCUMENTACAO\\Blog_WordPress\\previa_campanha
      --data=AAAA-MM-DD                         -> simula outro dia (ex.: --previa --data=2026-12-01 mostra o Natal)
Depois de novos cadastros: rode de novo (com --publicar) para atualizar tudo.
"""
import html
import json
import os
import re
import sys
import urllib.request
from datetime import date, datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerenciar_blog as gb  # noqa: E402
from gerar_categorias import nome_curto, troca_lista, troca_tabela  # noqa: E402
from gerar_esboco_categorias import carrega_arvore, classifica, tags_do, tem  # noqa: E402

SITE = "https://comprenolink.net"
GUIA = SITE + "/melhores-produtos-mercado-livre-2026/"
PAGINA_INICIO = 14
MENU = 4
ARQ_IDS = os.path.join(gb.PASTA_DADOS, "paginas_categorias.json")
UTM = "?utm_source=site&amp;utm_medium=home&amp;utm_campaign=botao_home&amp;utm_content="
e = lambda t: html.escape(str(t or ""), quote=True)
REL = 'target="_blank" rel="sponsored nofollow noopener"'

ESTILO = """<style>
.cnl-hub-grade{display:grid;grid-template-columns:repeat(auto-fill,minmax(220px,1fr));gap:16px;margin:12px 0 28px}
.cnl-hub-card{background:#fff;border:1px solid #e3e6ea;border-radius:14px;padding:14px;display:flex;flex-direction:column;gap:6px;box-shadow:0 2px 10px rgba(17,24,39,.05)}
.cnl-hub-card img{width:100%;height:160px;object-fit:contain}
.cnl-hub-card h3{font-size:16px!important;margin:0!important;line-height:1.3!important}
.cnl-hub-selo{font-size:12px;font-weight:700;color:#8a5a00;background:#fff4d6;border-radius:999px;padding:2px 10px;align-self:flex-start}
.cnl-hub-card p{font-size:14px;color:#5b6474;margin:0!important;flex:1}
.cnl-hub-botoes{display:flex;flex-wrap:wrap;gap:8px;margin-top:6px}
.cnl-hub-preco{background:#0B5FA5;color:#fff!important;border-radius:10px;padding:9px 14px;font-weight:700;font-size:14px;text-decoration:none!important}
.cnl-hub-det{border:1px solid #e3e6ea;border-radius:10px;padding:9px 14px;font-weight:600;font-size:14px;color:#1a2230!important;text-decoration:none!important}
.cnl-hub-outras a{display:inline-block;margin:4px 10px 4px 0}
.cnl-hub-card{position:relative}
.cnl-hub-rank{position:absolute;top:10px;left:10px;background:#111827;color:#ffd54a;font-weight:800;font-size:13px;border-radius:999px;padding:3px 10px}
</style>"""
# faixa da campanha (fica antes do ESTILO, por isso o estilo vai junto)
ESTILO_FAIXA = ('background:#111827;color:#fff;border-radius:12px;padding:12px 16px;font-weight:600;margin:0 0 16px')
ESTILO_FAIXA_LINK = 'color:#ffd54a;font-weight:800;white-space:nowrap'
RE_CAMP_HOME = re.compile(r'\n*<!-- wp:html -->\n<div class="cnl-campanha-home".*?<!-- /wp:html -->', re.S)
PASTA_PREVIA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "3_DOCUMENTACAO", "Blog_WordPress", "previa_campanha")


def hoje():
    m = re.search(r"--data=(\d{4}-\d{2}-\d{2})", " ".join(sys.argv))
    return date.fromisoformat(m.group(1)) if m else date.today()


def tem_pagina(tag, dia):
    # Black Friday fica sempre no ar; o Natal só aparece a partir de "a_partir_de"
    return not tag.get("a_partir_de") or dia >= date.fromisoformat(tag["a_partir_de"])


def valendo(tag, dia):
    return tem_pagina(tag, dia) and (not tag.get("campanha_ate") or dia <= date.fromisoformat(tag["campanha_ate"]))


def link_campanha(camp, origem):
    return f'{url_pagina(camp["slug"])}?utm_source=site&amp;utm_medium={origem}&amp;utm_campaign={camp["slug"].replace("-", "_")}'


def faixa(camp):
    return bloco("paragraph", f'<p class="cnl-faixa-campanha" style="{ESTILO_FAIXA}">{e(camp["emoji"])} {e(camp["faixa"])} '
                              f'<a href="{link_campanha(camp, "categoria")}" style="{ESTILO_FAIXA_LINK}">Ver agora →</a></p>',
                 '{"className":"cnl-faixa-campanha"}')


def chamada_inicio(raw, camp):
    raw = RE_CAMP_HOME.sub("", raw)
    if not camp:
        return raw
    botao = bloco("html", f'<div class="cnl-campanha-home" style="text-align:center;margin:4px 0 22px">'
                          f'<a href="{link_campanha(camp, "home")}&amp;utm_content=botao_campanha" style="display:inline-block;'
                          'background:#111827;color:#ffd54a;font-weight:800;font-size:18px;padding:14px 28px;border-radius:12px;'
                          f'text-decoration:none">{e(camp["emoji"])} {e(camp["botao"])}</a></div>')
    k = raw.find("<!-- /wp:buttons -->")  # logo abaixo do botão principal
    if k < 0:
        raise gb.Erro("Início sem o botão principal: não sei onde pôr o botão da campanha")
    k += len("<!-- /wp:buttons -->")
    return raw[:k] + "\n\n" + botao + raw[k:]


def carrega_ids():
    if os.path.exists(ARQ_IDS):
        with open(ARQ_IDS, encoding="utf-8") as f:
            return json.load(f)
    return {}


def salva_ids(ids):
    with open(ARQ_IDS, "w", encoding="utf-8") as f:
        json.dump(ids, f, ensure_ascii=False, indent=2)


def url_pagina(slug):
    return f"{SITE}/{slug}/"


def bloco(tipo, corpo, attrs=""):
    return f"<!-- wp:{tipo}{(' ' + attrs) if attrs else ''} -->\n{corpo}\n<!-- /wp:{tipo} -->"


def cartao(x, rank=0):
    img = (f'<a href="{e(x["link"])}" {REL}><img decoding="async" loading="lazy" src="{e(x["imagem"])}" alt="{e(x["nome"])}"></a>'
           if x["imagem"] else "")
    selo = f'<span class="cnl-hub-selo">⭐ {e(x["selo"])}</span>' if x["selo"] else ""
    desc = x["desc"] if len(x["desc"]) <= 150 else x["desc"][:147].rsplit(" ", 1)[0] + "…"
    num = f'<span class="cnl-hub-rank">#{rank}</span>' if rank else ""
    return (f'<div class="cnl-hub-card">{num}{img}{selo}<h3>{e(x["nome"])}</h3><p>{e(desc)}</p><div class="cnl-hub-botoes">'
            f'<a class="cnl-hub-preco" href="{e(x["link"])}" {REL}>Ver preço no Mercado Livre</a>'
            f'<a class="cnl-hub-det" href="{GUIA}#item-{x["n"]}">Ver detalhes</a></div></div>')


def aviso_afiliado():
    return bloco("paragraph", '<p class="cnl-aviso">Este site participa do programa de Afiliados do Mercado Livre: ao comprar pelos '
                              'nossos links podemos receber uma comissão, sem custo extra para você. Preços e estoque podem mudar '
                              f'no Mercado Livre. <a href="{SITE}/politica-de-privacidade/">Política de Privacidade</a>.</p>',
                 '{"className":"cnl-aviso"}')


def conteudo_categoria(cat, ys_por_sub, publicadas, camp=None):
    partes = [bloco("paragraph", f'<p class="cnl-migalhas"><a href="{SITE}/">Início</a> › {e(cat["nome"])}</p>', '{"className":"cnl-migalhas"}')]
    if camp:
        partes.append(faixa(camp))
    partes += [bloco("paragraph", f'<p class="cnl-intro">{e(cat["intro"])}</p>', '{"className":"cnl-intro"}'),
               aviso_afiliado(), bloco("html", ESTILO)]
    for sub, ys in ys_por_sub:
        ancora = re.sub(r"[^a-z0-9]+", "-", sub["nome"].lower().encode("ascii", "ignore").decode()).strip("-")
        partes.append(bloco("heading", f'<h2 id="{ancora}" class="wp-block-heading">{e(sub["nome"])}</h2>', f'{{"anchor":"{ancora}"}}'))
        partes.append(bloco("html", '<div class="cnl-hub-grade">' + "".join(cartao(y) for y in ys) + "</div>"))
    outras = " ".join(f'<a href="{url_pagina(c["slug"])}">{e(c["emoji"])} {e(c["nome"])}</a>' for c in publicadas if c is not cat)
    partes.append(bloco("heading", '<h2 class="wp-block-heading">Veja também</h2>'))
    partes.append(bloco("paragraph", f'<p class="cnl-hub-outras">{outras} <a href="{GUIA}">📋 Lista completa de 2026</a></p>',
                        '{"className":"cnl-hub-outras"}'))
    return "\n\n".join(partes)


def destaques(tag, ys):
    # Top N na ordem de "destaques" (cada palavra pega o 1º produto da tag que a tem no nome)
    top = []
    for p in tag.get("destaques", []):
        y = next((y for y in ys if y not in top and tem(y["nome"].lower(), [p])), None)
        if y:
            top.append(y)
    return top


def conteudo_tag(tag, ys, cats_com_itens, aviso=""):
    partes = [bloco("paragraph", f'<p class="cnl-migalhas"><a href="{SITE}/">Início</a> › {e(tag.get("rotulo", "Black Friday"))}</p>', '{"className":"cnl-migalhas"}')]
    if aviso:
        partes.append(aviso)
    partes += [bloco("paragraph", f'<p class="cnl-intro">{e(tag["intro"])}</p>', '{"className":"cnl-intro"}'),
               aviso_afiliado(), bloco("html", ESTILO)]
    if tag.get("html_apos_aviso"):  # ex.: contagem regressiva da Black Friday
        partes.append(bloco("html", tag["html_apos_aviso"]))
    top = destaques(tag, ys)
    resto = [y for y in ys if y not in top]
    if top:
        partes.append(bloco("heading", f'<h2 id="top-10" class="wp-block-heading">{e(tag["titulo_top"])}</h2>', '{"anchor":"top-10"}'))
        partes.append(bloco("html", '<div class="cnl-hub-grade">' + "".join(cartao(y, k) for k, y in enumerate(top, 1)) + "</div>"))
        if resto:
            partes.append(bloco("heading", f'<h2 id="mais-ofertas" class="wp-block-heading">{e(tag["titulo_resto"])}</h2>', '{"anchor":"mais-ofertas"}'))
            for cat, xs in cats_com_itens:
                zs = [y for y in resto if y in xs]
                if zs:
                    partes.append(bloco("heading", f'<h3 class="wp-block-heading">{e(cat["emoji"])} {e(cat["nome"])}</h3>', '{"level":3}'))
                    partes.append(bloco("html", '<div class="cnl-hub-grade">' + "".join(cartao(y) for y in zs) + "</div>"))
    else:
        partes.append(bloco("html", '<div class="cnl-hub-grade">' + "".join(cartao(y) for y in ys) + "</div>"))
    if tag.get("html_antes_guia"):  # ex.: "Como saber se o desconto é real"
        partes.append(bloco("html", tag["html_antes_guia"]))
    partes.append(bloco("paragraph", f'<p class="cnl-hub-outras"><a href="{GUIA}">📋 Ver a lista completa de 2026</a></p>', '{"className":"cnl-hub-outras"}'))
    return "\n\n".join(partes)


def aviso_fim(bf, natal):
    return bloco("paragraph", f'<p class="cnl-faixa-campanha" style="{ESTILO_FAIXA}">{e(bf["aviso_fim"])} '
                              f'<a href="{link_campanha(natal, "black_friday")}" style="{ESTILO_FAIXA_LINK}">{e(natal["emoji"])} {e(natal["rotulo"])} →</a></p>',
                 '{"className":"cnl-faixa-campanha"}')


def tabela_escolha(grupos):
    linhas = ""
    for cat, sub, ys in grupos:
        y = ys[0]
        linhas += (f'<tr><td>{e(cat["emoji"])} {e(sub["nome"])}</td><td><a href="#item-{y["n"]}">{e(nome_curto(y["nome"]))}</a></td>'
                   f'<td><a href="{e(y["link"])}" {REL}>Ver preço</a></td></tr>')
    return ('<!-- wp:table {"className":"cnl-escolha"} -->\n<figure class="wp-block-table cnl-escolha"><table class="has-fixed-layout">'
            '<thead><tr><th>Categoria</th><th>Nossa escolha</th><th>Oferta</th></tr></thead>'
            f'<tbody>{linhas}</tbody></table></figure>\n<!-- /wp:table -->')


def lista_inicio(cats_com_itens, publicadas):
    itens = []
    for cat, xs in cats_com_itens:
        nomes = [e(nome_curto(x["nome"])) for x in xs[:3]]
        resto = len(xs) - len(nomes)
        txt = ", ".join(nomes) + (f" e mais {resto} {'opção' if resto == 1 else 'opções'}" if resto else "")
        if cat in publicadas:
            destino, rotulo = f'{url_pagina(cat["slug"])}{UTM}cat_{cat["slug"]}', f'Ver {cat["nome"]}'
        else:
            destino, rotulo = f'{GUIA}{UTM}cat_{cat["slug"]}#item-{xs[0]["n"]}', "Ver no guia"
        itens.append(f'<!-- wp:list-item -->\n<li><strong>{e(cat["emoji"])} {e(cat["nome"])}</strong> – {e(cat.get("chamada") or cat["intro"].split(":")[0])}: '
                     f'{txt}. <a href="{destino}">{e(rotulo)}</a></li>\n<!-- /wp:list-item -->')
    return '<!-- wp:list -->\n<ul class="wp-block-list">' + "\n\n".join(itens) + "</ul>\n<!-- /wp:list -->"


def salva_backup(nome, conteudo):
    os.makedirs(gb.PASTA_BACKUP, exist_ok=True)
    arq = os.path.join(gb.PASTA_BACKUP, f"{nome}_{datetime.now():%Y-%m-%d_%Hh%M%S}.html")
    with open(arq, "w", encoding="utf-8", newline="") as f:
        f.write(conteudo)
    return arq


def publica_pagina(cfg, ids, slug, titulo, conteudo, meta=""):
    extra = {"aioseo_meta_data": {"description": meta}} if meta else {}  # descrição do Google (All in One SEO)
    pid = ids.get(slug)
    if not pid:
        achadas = gb.requisitar(cfg, "GET", f"/wp-json/wp/v2/pages?slug={slug}&status=publish,draft&context=edit")
        pid = achadas[0]["id"] if achadas else None
    if pid:
        atual = gb.requisitar(cfg, "GET", f"/wp-json/wp/v2/pages/{pid}?context=edit")
        print("   backup:", salva_backup(f"pagina{pid}_{slug}", atual["content"]["raw"]))
        gb.requisitar(cfg, "POST", f"/wp-json/wp/v2/pages/{pid}", {"title": titulo, "content": conteudo, "status": "publish", **extra})
        print(f"   atualizada: {url_pagina(slug)} (id {pid})")
    else:
        r = gb.requisitar(cfg, "POST", "/wp-json/wp/v2/pages", {"title": titulo, "slug": slug, "content": conteudo, "status": "publish", **extra})
        pid = r["id"]
        print(f"   criada: {r.get('link')} (id {pid})")
    ids[slug] = pid
    salva_ids(ids)
    return pid


def monta_menu(cfg, ids, publicadas, camp_menu):
    itens = gb.requisitar(cfg, "GET", f"/wp-json/wp/v2/menu-items?menus={MENU}&per_page=100&context=edit")
    arq = os.path.join(gb.PASTA_BACKUP, f"menu_principal_{datetime.now():%Y-%m-%d_%Hh%M%S}.json")
    with open(arq, "w", encoding="utf-8") as f:
        json.dump(itens, f, ensure_ascii=False, indent=2)
    print("   backup do menu:", arq)
    titulo = lambda i: html.unescape(re.sub("<[^>]+>", "", i["title"]["rendered"] if isinstance(i["title"], dict) else i["title"])).strip()
    topo = [i for i in itens if i["parent"] == 0]
    pai = next((i for i in topo if titulo(i) == "Categorias"), None)
    if not pai:
        pai = gb.requisitar(cfg, "POST", "/wp-json/wp/v2/menu-items",
                            {"title": "Categorias", "url": f"{SITE}/#categorias", "menus": MENU, "parent": 0, "status": "publish", "type": "custom"})
        print("   menu: criado 'Categorias'")
    filhos = {i.get("object_id"): i for i in itens if i["parent"] == pai["id"]}
    for k, c in enumerate(publicadas, 1):
        pid = ids[c["slug"]]
        dados = {"title": c["nome"], "menus": MENU, "parent": pai["id"], "menu_order": k, "status": "publish",
                 "type": "post_type", "object": "page", "object_id": pid}
        if pid in filhos:
            gb.requisitar(cfg, "POST", f"/wp-json/wp/v2/menu-items/{filhos[pid]['id']}", dados)
        else:
            gb.requisitar(cfg, "POST", "/wp-json/wp/v2/menu-items", dados)
    for pid, i in filhos.items():  # categoria que deixou de ter página
        if pid not in [ids[c["slug"]] for c in publicadas]:
            gb.requisitar(cfg, "DELETE", f"/wp-json/wp/v2/menu-items/{i['id']}?force=true")
    # um único item de campanha no topo: Black Friday até 30/11, depois Presentes de Natal (mesmo item, troca a página)
    rotulos = ("Black Friday", "Presentes de Natal")
    bf = next((i for i in topo if titulo(i) in rotulos), None)
    dados = {"title": camp_menu["rotulo"], "menus": MENU, "parent": 0, "status": "publish", "type": "post_type",
             "object": "page", "object_id": ids[camp_menu["slug"]]}
    if not bf:
        bf = gb.requisitar(cfg, "POST", "/wp-json/wp/v2/menu-items", dados)
        print(f"   menu: criado '{camp_menu['rotulo']}'")
    elif titulo(bf) != camp_menu["rotulo"] or bf.get("object_id") != ids[camp_menu["slug"]]:
        bf = gb.requisitar(cfg, "POST", f"/wp-json/wp/v2/menu-items/{bf['id']}", dados)
        print(f"   menu: item trocado para '{camp_menu['rotulo']}'")
    # ordem do topo: Início, Categorias, campanha, e o resto como estava
    ordem = sorted([i for i in topo if i["id"] not in (pai["id"], bf["id"] if bf else 0)], key=lambda i: i["menu_order"])
    inicio = [i for i in ordem if titulo(i) == "Início"]
    resto = [i for i in ordem if titulo(i) != "Início"]
    for k, i in enumerate(inicio + [pai] + ([bf] if bf else []) + resto, 1):
        gb.requisitar(cfg, "POST", f"/wp-json/wp/v2/menu-items/{i['id']}", {"menu_order": k, "menus": MENU})
    print(f"   menu: Categorias com {len(publicadas)} páginas + {camp_menu['rotulo']}")


def main():
    publicar = "--publicar" in sys.argv
    cfg = gb.carregar_config()
    arvore = carrega_arvore()
    minimo = arvore.get("minimo_para_publicar", 3)
    guia = gb.baixar_pagina(cfg)
    itens = gb.itens(guia.conteudo)
    info = {x["n"]: (classifica(x, arvore), tags_do(x, arvore)) for x in itens}
    sem = [x for x in itens if not info[x["n"]][0][0]]
    if sem:
        raise gb.Erro("Produtos sem categoria (inclua uma palavra no categorias.json): " + "; ".join(f"{x['n']} {x['nome']}" for x in sem))

    cats_com_itens, grupos_sub, publicadas, paginas = [], [], [], []
    for cat in arvore["categorias"]:
        xs = [x for x in itens if info[x["n"]][0][0] is cat]
        if not xs:
            continue
        cats_com_itens.append((cat, xs))
        por_sub = [(s, [x for x in xs if info[x["n"]][0][1] is s]) for s in cat["subcategorias"]]
        por_sub = [(s, ys) for s, ys in por_sub if ys]
        grupos_sub += [(cat, s, ys) for s, ys in por_sub]
        if len(xs) >= minimo:
            publicadas.append(cat)
            paginas.append((cat, por_sub))
    cats_com_itens.sort(key=lambda t: t[1][0]["n"])
    grupos_sub.sort(key=lambda t: t[2][0]["n"])
    dia = hoje()
    tag = {t["tag"]: t for t in arvore["tags"]}
    bf, natal = tag["black-friday"], tag.get("natal-presentes")
    ys_de = lambda t: [x for x in itens if t["tag"] in info[x["n"]][1]]
    # páginas de campanha no ar hoje (Black Friday sempre; Natal a partir de 01/12)
    campanhas = [t for t in (bf, natal) if t and tem_pagina(t, dia)]
    camp = next((t for t in (bf, natal) if t and valendo(t, dia)), None)  # botão na Início + faixa nas categorias
    camp_menu = natal if natal in campanhas and not valendo(bf, dia) else bf
    aviso_bf = aviso_fim(bf, natal) if natal in campanhas and not valendo(bf, dia) else ""

    print(f"{len(itens)} produtos | páginas de categoria: {[c['nome'] for c in publicadas]}")
    print(f"só no guia (menos de {minimo}): {[c['nome'] for c, xs in cats_com_itens if c not in publicadas]}")
    for t in campanhas:
        print(f"{t['rotulo']}: {len(ys_de(t))} produtos (Top {len(destaques(t, ys_de(t)))})")
    print(f"dia {dia:%d/%m/%Y} | campanha em destaque: {camp['rotulo'] if camp else 'nenhuma'} | menu: {camp_menu['rotulo']}"
          f" | Escolha rápida: {len(cats_com_itens)} linhas")

    conteudos = {cat["slug"]: (f"{cat['nome']}: as melhores ofertas do Mercado Livre", conteudo_categoria(cat, por_sub, publicadas, camp),
                               cat.get("meta_descricao", "")) for cat, por_sub in paginas}
    for t in campanhas:
        conteudos[t["slug"]] = (t["titulo"], conteudo_tag(t, ys_de(t), cats_com_itens, aviso_bf if t is bf else ""), t.get("meta_descricao", ""))
    d = gb.requisitar(cfg, "GET", f"/wp-json/wp/v2/pages/{PAGINA_INICIO}?context=edit")
    novo_inicio = troca_lista(d["content"]["raw"], lista_inicio(cats_com_itens, publicadas))
    novo_inicio = novo_inicio.replace(">Escolha por categoria</h2>", ' id="categorias">Escolha por categoria</h2>', 1) \
        if 'id="categorias"' not in novo_inicio else novo_inicio
    novo_inicio = chamada_inicio(novo_inicio, camp)

    if "--previa" in sys.argv:
        gera_previa(conteudos, novo_inicio, dia)
        return 0
    if not publicar:
        print("Nada foi publicado. Para publicar: python publicar_categorias.py --publicar")
        return 0

    ids = carrega_ids()
    for slug, (titulo, conteudo, meta) in conteudos.items():
        print(f"- {titulo}")
        publica_pagina(cfg, ids, slug, titulo, conteudo, meta)

    print("- Guia: Escolha rápida")
    # uma linha por Categoria Pai (o melhor = 1º do ranking); por subcategoria ficava longa demais
    grupos_pai = [(cat, {"nome": cat["nome"]}, xs) for cat, xs in cats_com_itens]
    novo_guia = troca_tabela(guia.conteudo, tabela_escolha(grupos_pai))
    if gb.verificar(novo_guia):
        raise gb.Erro("Guia ficaria inconsistente: " + "; ".join(gb.verificar(novo_guia)))
    gb.publicar(cfg, guia, novo_guia, guia.titulo)

    print("- Início: Escolha por categoria" + (f" + botão {camp['rotulo']}" if camp else ""))
    print("   backup:", salva_backup("pagina14_inicio", d["content"]["raw"]))
    gb.requisitar(cfg, "POST", f"/wp-json/wp/v2/pages/{PAGINA_INICIO}", {"content": novo_inicio})

    print("- Menu principal")
    monta_menu(cfg, ids, publicadas, camp_menu)
    print("Pronto. Limpe o cache do site (LiteSpeed > Limpar tudo) para ver na hora.")
    return 0


def renderiza(conteudo):
    # aproximação do que o WordPress mostra: tira os comentários dos blocos
    return re.sub(r"<!-- /?wp:.*? -->\n?", "", conteudo)


def gera_previa(conteudos, inicio, dia):
    pasta = os.path.join(PASTA_PREVIA, f"{dia:%Y-%m-%d}")
    os.makedirs(pasta, exist_ok=True)
    baixa = lambda url: urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "previa"}), timeout=60).read().decode("utf-8")
    casca = baixa(url_pagina("black-friday"))  # mesmo tema/estilo das páginas do site
    paginas = [("inicio", baixa(SITE + "/"), None, inicio)] + [(s, casca, t, c) for s, (t, c, _) in conteudos.items()]
    links = []
    for slug, pag, titulo, conteudo in paginas:
        m = re.search(r'(<div class="single-entry-summary">)(.*?)(</div>\s*<div id="comments")', pag, re.S)
        if not m:
            raise gb.Erro(f"prévia: não achei o conteúdo da página {slug}")
        novo = pag[:m.start(2)] + renderiza(conteudo) + pag[m.end(2):]
        if titulo:
            novo = re.sub(r'(<h1 class="single-title[^>]*>).*?(</h1>)', lambda k: k.group(1) + e(titulo) + k.group(2), novo, count=1, flags=re.S)
            novo = re.sub(r"<title>.*?</title>", f"<title>PRÉVIA - {e(titulo)}</title>", novo, count=1, flags=re.S)
        novo = novo.replace("<body", '<body data-previa="1"', 1).replace(
            "</body>", '<div style="position:fixed;bottom:0;left:0;right:0;background:#b00020;color:#fff;text-align:center;'
                       f'padding:6px;font:600 14px sans-serif;z-index:9999">PRÉVIA LOCAL ({dia:%d/%m/%Y}) — nada disto foi publicado</div></body>', 1)
        arq = os.path.join(pasta, f"{slug}.html")
        with open(arq, "w", encoding="utf-8") as f:
            f.write(novo)
        links.append(arq)
    print("Prévia gerada (nada publicado):")
    for a in links:
        print("  ", os.path.abspath(a))


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    try:
        sys.exit(main())
    except gb.Erro as erro:
        print("ERRO:", erro)
        sys.exit(1)
