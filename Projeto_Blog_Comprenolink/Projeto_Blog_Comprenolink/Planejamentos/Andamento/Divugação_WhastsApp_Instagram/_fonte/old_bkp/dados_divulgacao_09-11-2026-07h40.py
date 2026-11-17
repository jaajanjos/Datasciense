# -*- coding: utf-8 -*-
"""
Dados da divulgação: lê os produtos REAIS do blog (guia + categorias.json) e monta
posts, textos prontos e links rastreáveis (UTM). Usado por gerar_divulgacao.py.

Regras (iguais às do blog): sem preço, sem "menor/melhor preço", sem promessas de
saúde ou estética; só fatos que já estão no texto do produto no blog.
"""
import os
import sys
from datetime import date, timedelta

BLOG = r"D:\mercado_livre\9_Manutenção_Blog\1_PROGRAMAS\Blog_WordPress"
sys.path.insert(0, BLOG)
import gerenciar_blog as gb  # noqa: E402
from gerar_esboco_categorias import carrega_arvore, classifica, tags_do  # noqa: E402
from publicar_categorias import destaques  # noqa: E402

SITE = "https://comprenolink.net"
GUIA = SITE + "/melhores-produtos-mercado-livre-2026/"
PAG = {"black_friday": SITE + "/black-friday/", "natal": SITE + "/presentes-de-natal/"}
WHATSAPP = "(11) 99495-9657"
WHATSAPP_LINK = "https://wa.me/5511994959657?text=Ol%C3%A1%21%20Vim%20pelo%20Instagram%20do%20comprenolink.net"
AVISO = ("Publi: contém link de afiliado. Posso ganhar uma comissão, sem custo extra para você. "
         "Preços e estoque podem mudar no Mercado Livre.")
TAGS_BASE = ["#achadosmercadolivre", "#mercadolivre", "#achadinhos", "#compranolink"]
TAGS_CAMPANHA = {"black_friday": ["#blackfriday", "#blackfriday2026", "#ofertas"],
                 "natal": ["#presentesdenatal", "#natal2026", "#ideiasdepresente"]}
TAGS_CAT = {  # só hashtags gerais da categoria (sem marca/produto, para não sair #jbl num post de TV)
    "tecnologia-e-informatica": ["#tecnologia", "#gadgets", "#setup"],
    "audio-e-tv": ["#audioevideo", "#cinemaemcasa", "#tecnologia"],
    "casa-e-eletrodomesticos": ["#casapratica", "#utilidades", "#eletrodomesticos"],
    "bebe-e-maternidade": ["#enxovaldebebe", "#maternidade", "#bebe"],
    "casa-cama-e-decoracao": ["#decoracao", "#casadecorada", "#quarto"],
    "ferramentas-e-utilidades": ["#ferramentas", "#reforma", "#facavocemesmo"],
    "esporte-e-fitness": ["#fitness", "#treinoemcasa", "#academia"],
    "beleza-e-saude": ["#beleza", "#autocuidado", "#bemestar"],
}
PALAVRA = {"black_friday": "BLACK", "natal": "NATAL"}  # "comente BLACK que eu te mando o link"


def utm(url, origem, meio, campanha, conteudo, ancora=""):
    sep = "&" if "?" in url else "?"
    return f"{url}{sep}utm_source={origem}&utm_medium={meio}&utm_campaign={campanha}&utm_content={conteudo}{ancora}"


def slug(t):
    import re
    import unicodedata
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", "_", t).strip("_")[:40]


def carrega_produtos():
    cfg = gb.carregar_config()
    itens = gb.itens(gb.baixar_pagina(cfg).conteudo)
    arv = carrega_arvore()
    tags = {t["tag"]: t for t in arv["tags"]}
    for x in itens:
        cat, sub = classifica(x, arv)
        x["cat"], x["sub"], x["tags"] = cat, sub, tags_do(x, arv)
    bf = [x for x in itens if "black-friday" in x["tags"]]
    nt = [x for x in itens if "natal-presentes" in x["tags"]]
    top_bf, top_nt = destaques(tags["black-friday"], bf), destaques(tags["natal-presentes"], nt)
    resto = lambda ys, top: [y for y in ys if y not in top]
    return {"itens": itens, "arvore": arv,
            "black_friday": top_bf + resto(bf, top_bf), "natal": top_nt + resto(nt, top_nt),
            "top": {"black_friday": top_bf, "natal": top_nt}}


def hashtags(x, campanha):
    cat = TAGS_CAT.get(x["cat"]["slug"], []) if x.get("cat") else []
    return " ".join(TAGS_CAMPANHA[campanha] + cat[:3] + TAGS_BASE[:3])


def textos_produto(x, campanha, dia):
    """Legenda do feed, texto do story, resposta do Direct e mensagens de WhatsApp de um produto."""
    cont = f"{dia:%Y%m%d}_{slug(x['nome'])}"
    ancora = f"#item-{x['n']}"
    link_story = utm(GUIA, "instagram", "stories", campanha, cont, ancora)
    link_dm = utm(GUIA, "instagram", "dm", campanha, cont, ancora)
    link_wpp = {m: utm(GUIA, "whatsapp", m, campanha, cont, ancora) for m in ("status", "canal", "grupos", "lista")}
    nome_campanha = "Black Friday" if campanha == "black_friday" else "Natal"
    emoji = "🔥" if campanha == "black_friday" else "🎄"
    bens = "\n".join(f"✅ {b}" for b in x["beneficios"][:4])
    ideal = ", ".join(i.lower() if i[:2] != i[:2].upper() else i for i in x["ideal"][:3])
    palavra = PALAVRA[campanha]
    legenda = (f"{emoji} {x['nome']}\n\n{x['desc']}\n\n{bens}\n\n"
               f"💡 Ideal para: {ideal}.\n\n"
               f"👉 Comente {palavra} que eu te mando o link no Direct, ou toque no link da bio.\n"
               f"Confira o valor do dia direto no Mercado Livre.\n\n{AVISO}\n\n{hashtags(x, campanha)}")
    story = (f"{emoji} {nome_campanha}: {x['nome']}\n{x['selo']}\n"
             f"Toque no link para ver no blog e conferir o valor do dia no Mercado Livre.")
    dm = (f"Oi! Aqui está o link do {x['nome']} que você pediu 😊\n{link_dm}\n"
          f"Lá você vê os detalhes e confere o valor do dia no Mercado Livre. "
          f"(Link de afiliado: posso ganhar comissão, sem custo extra para você.)")
    wpp = (f"{emoji} *{nome_campanha} – {x['nome']}*\n\n{x['desc']}\n\n{bens}\n\n"
           f"👉 Veja no blog e confira o valor do dia: {{LINK}}\n\n"
           f"_Link de afiliado: posso ganhar comissão, sem custo extra para você._")
    return {"conteudo": cont, "legenda": legenda, "story": story, "dm": dm, "wpp": wpp,
            "link_story": link_story, "link_dm": link_dm, "link_wpp": link_wpp}


def calendario(dados):
    """Plano de 02/11 a 23/12, alinhado à agenda AGENDA_BLOG_2026.ics."""
    linhas = []
    fila = {"black_friday": list(dados["black_friday"]), "natal": list(dados["natal"])}
    pos = {"black_friday": 0, "natal": 0}

    def proximo(camp):
        xs = fila[camp]
        x = xs[pos[camp] % len(xs)]
        pos[camp] += 1
        return x

    def add(dia, hora, canal, formato, camp, x, texto, link, obs=""):
        linhas.append({"data": dia, "hora": hora, "canal": canal, "formato": formato, "campanha": camp,
                       "produto": x["nome"] if x else "Página da campanha", "item": x["n"] if x else "",
                       "texto": texto, "link": link, "obs": obs})

    d, fim = date(2026, 11, 2), date(2026, 12, 23)
    while d <= fim:
        camp = "black_friday" if d <= date(2026, 11, 30) else "natal"
        semana_bf = date(2026, 11, 23) <= d <= date(2026, 11, 30)
        dia_post = semana_bf or (d.weekday() in (0, 2, 4) and d not in (date(2026, 12, 1),))
        if d == date(2026, 12, 1):
            add(d, "09:00", "Blog", "Conferência", camp, None, "Conferir se 'Presentes de Natal' está no menu. Trocar o link da bio para o Natal.",
                utm(PAG["natal"], "instagram", "bio", "natal", "bio_dez"), "Se não aparecer, pedir ao Claude 'gerar as categorias'.")
        if dia_post:
            x = proximo(camp)
            t = textos_produto(x, camp, d)
            add(d, "19:00", "Instagram", "Post no feed (foto/carrossel)", camp, x, t["legenda"], "Link da bio (ver aba Links)",
                f"Responder quem comentar {PALAVRA[camp]} com o texto do Direct.")
            add(d, "19:10", "Instagram", "Story com adesivo de link", camp, x, t["story"], t["link_story"])
            add(d, "19:15", "WhatsApp", "Status", camp, x, t["wpp"].replace("{LINK}", t["link_wpp"]["status"]), t["link_wpp"]["status"])
            if d.weekday() in (0, 3) or semana_bf:
                add(d, "19:20", "WhatsApp", "Canal", camp, x, t["wpp"].replace("{LINK}", t["link_wpp"]["canal"]), t["link_wpp"]["canal"])
        if d.weekday() == 1 and d not in (date(2026, 11, 24),):  # grupos: 1 vez por semana, terça 12h
            link = utm(PAG[camp], "whatsapp", "grupos", camp, f"{d:%Y%m%d}_semanal")
            add(d, "12:00", "WhatsApp", "Grupos (só onde é permitido)", camp, None, MSG_GRUPO[camp].replace("{LINK}", link), link,
                "No máximo 1 mensagem por semana em cada grupo.")
        if d == date(2026, 11, 26):
            link = utm(PAG["black_friday"], "whatsapp", "grupos", "black_friday", "20261126_lembrete")
            add(d, "20:00", "WhatsApp + Stories", "Lembrete forte", camp, None, MSG_LEMBRETE.replace("{LINK}", link), link)
        if d == date(2026, 11, 27):
            for h, nome in (("08:00", "manha"), ("12:00", "almoco"), ("19:00", "noite")):
                link = utm(PAG["black_friday"], "whatsapp", "grupos", "black_friday", f"20261127_{nome}")
                add(d, h, "WhatsApp + Stories", "Disparo do dia D", camp, None, MSG_DIA_D.replace("{LINK}", link), link)
        if d == date(2026, 11, 30):
            link = utm(PAG["black_friday"], "whatsapp", "grupos", "black_friday", "20261130_cyber")
            add(d, "12:00", "WhatsApp + Stories", "Cyber Monday", camp, None, MSG_CYBER.replace("{LINK}", link), link)
        d += timedelta(days=1)
    return linhas


MSG_GRUPO = {
    "black_friday": ("🔥 *Black Friday 2026: lista pronta!*\n\nSeparei as ofertas que valem a pena acompanhar no Mercado Livre, "
                     "com Top 10 e tudo por categoria (tecnologia, TV, casa, ferramentas, fitness e beleza).\n\n"
                     "👉 {LINK}\n\nSalve o link e confira o valor do dia direto no Mercado Livre.\n"
                     "_Link de afiliado: posso ganhar comissão, sem custo extra para você._"),
    "natal": ("🎄 *Presentes de Natal: ideias que agradam*\n\nMontei uma lista com presentes para todos os gostos: "
              "perfumes, JBL, skincare, smartwatch, enxoval e decoração.\n\n👉 {LINK}\n\n"
              "Confira o valor do dia direto no Mercado Livre.\n_Link de afiliado: posso ganhar comissão, sem custo extra para você._"),
}
MSG_LEMBRETE = ("⏰ *Amanhã é Black Friday!*\n\nDeixei a lista pronta com as ofertas que valem a pena acompanhar. "
                "Salve o link para abrir amanhã cedo:\n👉 {LINK}\n\n_Link de afiliado: posso ganhar comissão, sem custo extra para você._")
MSG_DIA_D = ("🔥 *É hoje: Black Friday!*\n\nTop 10 e mais ofertas por categoria, tudo em um lugar só:\n👉 {LINK}\n\n"
             "Confira o valor do dia direto no Mercado Livre.\n_Link de afiliado: posso ganhar comissão, sem custo extra para você._")
MSG_CYBER = ("⚡ *Último dia: Cyber Monday*\n\nAinda dá tempo de conferir a lista da Black Friday:\n👉 {LINK}\n\n"
             "_Link de afiliado: posso ganhar comissão, sem custo extra para você._")

LINKS_FIXOS = [
    (f"WhatsApp do blog {WHATSAPP} – 2º link da bio do Instagram (abre a conversa)", WHATSAPP_LINK),
    ("Instagram – link da bio (novembro)", utm(PAG["black_friday"], "instagram", "bio", "black_friday", "bio_nov")),
    ("Instagram – link da bio (dezembro)", utm(PAG["natal"], "instagram", "bio", "natal", "bio_dez")),
    ("Instagram – link da bio (depois de 25/12)", utm(SITE + "/", "instagram", "bio", "perfil", "link_na_bio")),
    ("WhatsApp Business – site no perfil", utm(SITE + "/", "whatsapp", "perfil", "perfil", "site_no_perfil")),
    ("WhatsApp – grupos (Black Friday)", utm(PAG["black_friday"], "whatsapp", "grupos", "black_friday", "mensagem")),
    ("WhatsApp – grupos (Natal)", utm(PAG["natal"], "whatsapp", "grupos", "natal", "mensagem")),
    ("WhatsApp – Canal (Black Friday)", utm(PAG["black_friday"], "whatsapp", "canal", "black_friday", "mensagem")),
    ("WhatsApp – Canal (Natal)", utm(PAG["natal"], "whatsapp", "canal", "natal", "mensagem")),
    ("WhatsApp – lista de transmissão (Black Friday)", utm(PAG["black_friday"], "whatsapp", "lista", "black_friday", "mensagem")),
    ("WhatsApp – lista de transmissão (Natal)", utm(PAG["natal"], "whatsapp", "lista", "natal", "mensagem")),
]
