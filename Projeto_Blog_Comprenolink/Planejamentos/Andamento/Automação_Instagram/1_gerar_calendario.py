"""
Gera o CALENDÁRIO de conteúdo orgânico do Instagram para divulgar o blog
https://comprenolink.net/melhores-produtos-mercado-livre-2026/ (afiliados Mercado Livre).

Para cada dia gera: post do feed (Reels ou Carrossel) com legenda pronta,
roteiro, hashtags, palavra-chave para comentários e os links etiquetados (UTM)
de Stories e Direct — assim o relatório de acessos (python\\3_relatorio_acessos_anuncios.py)
mostra qual post trouxe cada visita.

Uso:
    python 1_gerar_calendario.py
    python 1_gerar_calendario.py --inicio 2026-10-12
    python 1_gerar_calendario.py --registrar-rastreio   # adiciona os links no config_rastreio.json

Saída (pasta saida\\):
    calendario_instagram_AAAA-MM-DD_HHhMM.html  -> abra no navegador, botão "Copiar" em cada legenda
    calendario_instagram_AAAA-MM-DD_HHhMM.csv   -> abre no Excel
    lembretes_instagram_AAAA-MM-DD_HHhMM.ics    -> importe no Google Agenda/Outlook (lembrete de cada postagem)
"""
import argparse
import csv
import html
import json
import os
import shutil
import sys
from datetime import date, datetime, timedelta
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

PASTA = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
RAIZ = "D:/Projeto_Blog_Comprenolink"
CONFIG_IG = os.path.join(PASTA, "config_instagram.json")
PRODUTOS = os.path.join(PASTA, "produtos.json")
CONFIG_RASTREIO = [os.path.join(RAIZ, "Relatorios_Diarios_Anuncios", "programas_fontes_python", "config_rastreio.json"),
                   os.path.join(RAIZ, "Planejamentos", "Andamento", "Rastreamento_anuncios", "config_rastreio.json")]
PAGINA_PADRAO = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"
PASTA_SAIDA = os.path.join(PASTA, "saida")
DIAS = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]


def montar_link(base, origem, meio, campanha, conteudo=""):
    partes = urlsplit(base)
    qs = dict(parse_qsl(partes.query))
    qs.update({"utm_source": origem, "utm_medium": meio, "utm_campaign": campanha})
    if conteudo:
        qs["utm_content"] = conteudo
    return urlunsplit((partes.scheme, partes.netloc, partes.path, urlencode(qs), ""))


def pagina_blog():
    for c in CONFIG_RASTREIO:
        if os.path.exists(c):
            with open(c, encoding="utf-8") as f:
                return json.load(f).get("pagina_blog") or PAGINA_PADRAO
    return PAGINA_PADRAO


def hashtags(cfg, prods):
    cats = [p["categoria"] for p in prods] or ["geral"]
    principal = max(set(cats), key=cats.count)
    tags = cfg["hashtags_base"] + cfg["hashtags_categoria"].get(principal, cfg["hashtags_categoria"]["geral"])
    return " ".join(dict.fromkeys(tags))  # 5-6 hashtags: o Instagram recomenda poucas e relevantes


def roteiro_reels(pauta, prods):
    linhas = [f"[0-3s] GANCHO na tela + fala: \"{pauta['titulo']}\""]
    if pauta.get("video"):
        linhas.append(f"Vídeo pronto: {pauta['video']} (o mesmo do TikTok: use o arquivo original, sem marca d'água)")
    t = 3
    for p in prods:
        linhas.append(f"[{t}-{t + 6}s] {p['nome']}: {p['selo'].lower()}, por volta de R$ {p['preco']}. Mostre o produto/print do anúncio.")
        t += 6
    linhas.append(f"[{t}-{t + 4}s] CTA: \"Comenta {pauta['palavra']} que eu te mando o link no direct!\"")
    linhas.append("Dicas: legenda na tela (muita gente assiste sem som), duração ideal 15-30s, áudio em alta.")
    return linhas


def slides_carrossel(pauta, prods):
    s = [f"CAPA: {pauta['titulo']} (arraste →)"]
    for i, t in enumerate(pauta.get("topicos", []), 1):
        s.append(f"{i}. {t}")
    for p in prods:
        s.append(f"{p['nome']} — {p['selo']} — a partir de R$ {p['preco']}")
    s.append(f"FINAL: Salva pra não perder + comenta {pauta['palavra']} que eu mando o link")
    return s


def legenda(cfg, pauta, prods):
    lista = "\n".join(f"• {p['nome']} ({p['selo']}) — a partir de R$ {p['preco']}" for p in prods)
    corpo = {
        "Comparativo": "Comparei os dois lado a lado pra você não gastar errado. Qual você escolheria? Me conta aqui 👇",
        "Lista": "Separei os que valem a pena de verdade. Salva esse post pra consultar na hora de comprar 📌",
        "Review": "Vale ou não vale? Te conto o que importa antes de você comprar.",
        "Guia": "Guia rápido pra acertar na compra — sem enrolação.",
        "Dica": "Dica rápida que faz diferença no dia a dia.",
        "Educativo": "Anota essas dicas antes da sua próxima compra online 📌",
        "Achado": "Achado bom e com preço justo 🔎",
        "Comunidade": "Juntei as perguntas que mais chegaram no direct. Manda a sua nos comentários!",
    }.get(pauta["pilar"], "")
    partes = [pauta["titulo"], corpo]
    if pauta.get("topicos"):
        partes.append("\n".join(f"{i}. {t}" for i, t in enumerate(pauta["topicos"], 1)))
    if lista:
        partes.append(lista)
    partes.append(f"💬 Comenta {pauta['palavra']} que eu te envio o link no direct\n"
                  f"🔗 Ou acesse a lista completa pelo link na bio ({cfg['site']})")
    partes.append(f"⚠️ {cfg['aviso_afiliado']}")
    partes.append(hashtags(cfg, prods))
    return "\n\n".join(p for p in partes if p)


def gerar(cfg, produtos, inicio, base):
    pautas = list(cfg["pautas"])
    dias_feed = set(cfg.get("dias_feed", [0, 1, 2, 3, 4]))
    h = cfg["horarios"]
    dias, n, d = [], 0, inicio
    while n < len(pautas) or d.weekday() != 0:  # vai até fechar a última semana (domingo)
        semana = (d - inicio).days // 7 + 1
        dia = {"data": d, "semana": semana, "post": None, "stories": []}
        if d.weekday() in dias_feed and n < len(pautas):
            pauta = pautas[n]
            n += 1
            prods = [produtos[i] for i in pauta["produtos"]]
            camp = f"ig{n:02d}_{pauta['palavra'].lower()}"
            post = dict(pauta, numero=n, campanha=camp, prods=prods,
                        horario=h.get(pauta["formato"], "12:00"),
                        legenda=legenda(cfg, pauta, prods),
                        link_stories=montar_link(base, "instagram", "stories", camp, "link_stories"),
                        link_dm=montar_link(base, "instagram", "dm", camp, f"comente_{pauta['palavra'].lower()}"),
                        roteiro=roteiro_reels(pauta, prods) if pauta["formato"] == "reels" else slides_carrossel(pauta, prods))
            dia["post"] = post
            alvo = prods[0]["nome"] if prods else "comprar online"
            dia["stories"] = [
                (h["stories"][0], f"Enquete/quiz sobre o tema de hoje: \"Você já errou ao {('escolher ' + alvo) if prods else 'comprar online'}?\" (Sim/Não)", ""),
                (h["stories"][1], f"Prévia do {post['formato']} de hoje + adesivo de LINK", post["link_stories"]),
                (h["stories"][2], "Repost do post no story + caixinha de perguntas \"Qual produto você quer que eu analise?\"", ""),
            ]
        elif d.weekday() == 5:
            dia["stories"] = [
                (h["stories"][1], f"Resumo da semana {semana}: 1 story por post, adesivo de LINK no último", montar_link(base, "instagram", "stories", f"resumo_semana{semana}", "link_stories")),
                (h["stories"][2], "Bastidores: como você escolhe os produtos (gera confiança)", ""),
            ]
        else:
            dia["stories"] = [
                (h["stories"][1], "Enquete: \"Qual comparativo você quer na próxima semana?\" (2 opções)", ""),
                (h["stories"][2], "Destaque da semana com adesivo de LINK para o blog", montar_link(base, "instagram", "stories", f"domingo_semana{semana}", "link_stories")),
            ]
        dias.append(dia)
        d += timedelta(days=1)
    return dias


def salvar_csv(dias, caminho):
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["data", "dia", "semana", "tipo", "horario", "formato", "pilar", "titulo", "palavra_chave",
                    "legenda", "roteiro_ou_slides", "link"])
        for d in dias:
            p = d["post"]
            if p:
                w.writerow([d["data"].isoformat(), DIAS[d["data"].weekday()], d["semana"], "FEED", p["horario"], p["formato"],
                            p["pilar"], p["titulo"], p["palavra"], p["legenda"], "\n".join(p["roteiro"]), p["link_dm"]])
            for hora, desc, link in d["stories"]:
                w.writerow([d["data"].isoformat(), DIAS[d["data"].weekday()], d["semana"], "STORY", hora, "stories",
                            "", desc, "", "", "", link])


def salvar_ics(dias, caminho):
    def ics_txt(s):
        return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")
    ev = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//comprenolink//instagram//PT", "CALSCALE:GREGORIAN"]
    carimbo = datetime.now().strftime("%Y%m%dT%H%M%S")
    for d in dias:
        p = d["post"]
        if not p:
            continue
        hh, mm = map(int, p["horario"].split(":"))
        ini = datetime.combine(d["data"], datetime.min.time()).replace(hour=hh, minute=mm)
        ev += ["BEGIN:VEVENT", f"UID:ig{p['numero']:02d}-{d['data'].isoformat()}@comprenolink",
               f"DTSTAMP:{carimbo}", f"DTSTART:{ini:%Y%m%dT%H%M%S}", f"DTEND:{ini + timedelta(minutes=30):%Y%m%dT%H%M%S}",
               f"SUMMARY:{ics_txt('Instagram ' + p['formato'].upper() + ': ' + p['titulo'])}",
               f"DESCRIPTION:{ics_txt(p['legenda'])}",
               "BEGIN:VALARM", "TRIGGER:-PT30M", "ACTION:DISPLAY", "DESCRIPTION:Postar no Instagram", "END:VALARM",
               "END:VEVENT"]
    ev.append("END:VCALENDAR")
    with open(caminho, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(ev) + "\n")


def salvar_html(cfg, dias, caminho, bio_links):
    e = html.escape
    cards = []
    for d in dias:
        p = d["post"]
        corpo = []
        if p:
            cor = "#e1306c" if p["formato"] == "reels" else "#5851db"
            arte = f"saida/artes/ig{p['numero']:02d}_{p['palavra'].lower()}/"
            corpo.append(f"""
<div class="post"><div class="tag" style="background:{cor}">{e(p['formato'].upper())} · {e(p['horario'])}</div>
<span class="pilar">{e(p['pilar'])}</span>
<h3>#{p['numero']:02d} {e(p['titulo'])}</h3>
<p class="kw">Palavra-chave nos comentários: <b>{e(p['palavra'])}</b> → responder no direct com o link abaixo</p>
<details><summary>{'Roteiro do Reels' if p['formato'] == 'reels' else 'Slides do carrossel'} (artes em {e(arte)})</summary>
<ol>{''.join(f'<li>{e(r)}</li>' for r in p['roteiro'])}</ol></details>
<label>Legenda</label><textarea readonly>{e(p['legenda'])}</textarea>
<button onclick="copiar(this.previousElementSibling.value,this)">Copiar legenda</button>
<label>Link para o Direct (quem comentar {e(p['palavra'])})</label><div class="lk"><code>{e(p['link_dm'])}</code>
<button onclick="copiar('{e(p['link_dm'])}',this)">Copiar</button></div></div>""")
        st = "".join(
            f"<li><b>{e(h)}</b> {e(desc)}" + (f"<div class='lk'><code>{e(lk)}</code><button onclick=\"copiar('{e(lk)}',this)\">Copiar</button></div>" if lk else "") + "</li>"
            for h, desc, lk in d["stories"])
        corpo.append(f"<div class='stories'><label>Stories</label><ul>{st}</ul></div>")
        fds = " fds" if d["data"].weekday() >= 5 else ""
        cards.append(f"<section class='dia{fds}'><div class='data'>{DIAS[d['data'].weekday()]}<br><b>{d['data']:%d/%m}</b><small>Semana {d['semana']}</small></div><div class='conteudo'>{''.join(corpo)}</div></section>")
    bios = "".join(f"<li>Semana {s}: <code>{e(l)}</code> <button onclick=\"copiar('{e(l)}',this)\">Copiar</button></li>" for s, l in bio_links)
    doc = f"""<!doctype html><html lang="pt-BR"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Calendário Instagram</title><style>
:root{{--bg:#f6f7f9;--card:#fff;--tx:#1d1f23;--mut:#666;--bd:#e3e5e8}}
@media (prefers-color-scheme:dark){{:root{{--bg:#15171a;--card:#1f2226;--tx:#eceef1;--mut:#9aa0a6;--bd:#33373c}}}}
body{{margin:0;font-family:Segoe UI,Arial,sans-serif;background:var(--bg);color:var(--tx)}}
.wrap{{max-width:980px;margin:auto;padding:16px}} h1{{margin:.2em 0}} .sub{{color:var(--mut)}}
.dia{{display:flex;gap:14px;background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:14px;margin:12px 0}}
.dia.fds{{opacity:.85}} .data{{min-width:78px;text-align:center;color:var(--mut)}} .data b{{font-size:1.5em;color:var(--tx)}} .data small{{display:block}}
.conteudo{{flex:1;min-width:0}} .tag{{display:inline-block;color:#fff;border-radius:6px;padding:2px 8px;font-size:.8em;font-weight:600}}
.pilar{{margin-left:8px;color:var(--mut);font-size:.85em}} h3{{margin:.4em 0}} .kw{{margin:.3em 0;font-size:.9em}}
textarea{{width:100%;box-sizing:border-box;height:170px;background:var(--bg);color:var(--tx);border:1px solid var(--bd);border-radius:8px;padding:8px;font:inherit;font-size:.88em}}
label{{display:block;font-weight:600;font-size:.85em;margin-top:8px}} code{{font-size:.78em;word-break:break-all}}
.lk{{display:flex;gap:8px;align-items:center;background:var(--bg);border-radius:6px;padding:4px 8px;margin:4px 0}}
button{{background:#ffe600;border:0;border-radius:6px;padding:5px 10px;font-weight:600;cursor:pointer;white-space:nowrap;color:#222}}
ul{{padding-left:18px}} li{{margin:4px 0}} .box{{background:var(--card);border:1px solid var(--bd);border-radius:12px;padding:12px 16px}}
@media (max-width:600px){{.dia{{flex-direction:column}} .data{{text-align:left}}}}
</style></head><body><div class="wrap">
<h1>Calendário Instagram — {e(cfg['nome_marca'])}</h1>
<p class="sub">Gerado em {datetime.now():%d/%m/%Y %H:%M} · {sum(1 for d in dias if d['post'])} posts no feed · {len(dias)} dias · perfil {e(cfg['perfil'])}</p>
<div class="box"><b>Link da bio</b> (troque toda segunda-feira para saber qual semana trouxe mais visitas):<ul>{bios}</ul></div>
{''.join(cards)}
</div><script>
function copiar(t,b){{navigator.clipboard.writeText(t).then(()=>{{const o=b.textContent;b.textContent='Copiado!';setTimeout(()=>b.textContent=o,1200)}})}}
</script></body></html>"""
    with open(caminho, "w", encoding="utf-8") as f:
        f.write(doc)


def registrar_rastreio(dias, bio_links):
    novos = [{"origem": "instagram", "meio": "bio", "campanha": "perfil", "conteudo": f"semana{s}"} for s, _ in bio_links]
    for d in dias:
        p = d["post"]
        if p:
            novos.append({"origem": "instagram", "meio": "stories", "campanha": p["campanha"], "conteudo": "link_stories"})
            novos.append({"origem": "instagram", "meio": "dm", "campanha": p["campanha"], "conteudo": f"comente_{p['palavra'].lower()}"})
    for c in CONFIG_RASTREIO:
        if not os.path.exists(c):
            continue
        with open(c, encoding="utf-8") as f:
            cfg = json.load(f)
        existentes = {(a["origem"], a["meio"], a["campanha"], a.get("conteudo", "")) for a in cfg.get("anuncios", [])}
        add = [a for a in novos if (a["origem"], a["meio"], a["campanha"], a["conteudo"]) not in existentes]
        if not add:
            print(f"   {c}: nada novo")
            continue
        shutil.copy2(c, c + ".bak")
        cfg.setdefault("anuncios", []).extend(add)
        with open(c, "w", encoding="utf-8") as f:
            json.dump(cfg, f, ensure_ascii=False, indent=2)
        print(f"   {c}: +{len(add)} links (backup em .bak)")


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Gera o calendário orgânico do Instagram")
    ap.add_argument("--inicio", help="data da 1ª postagem (AAAA-MM-DD); padrão: data_inicio do config")
    ap.add_argument("--registrar-rastreio", action="store_true", help="adiciona os links UTM no config_rastreio.json")
    args = ap.parse_args()

    with open(CONFIG_IG, encoding="utf-8") as f:
        cfg = json.load(f)
    with open(PRODUTOS, encoding="utf-8") as f:
        produtos = {p["id"]: p for p in json.load(f)["produtos"]}
    faltando = {i for pa in cfg["pautas"] for i in pa["produtos"]} - produtos.keys()
    if faltando:
        sys.exit(f"❌ Produtos não encontrados em produtos.json: {', '.join(sorted(faltando))}")

    inicio = date.fromisoformat(args.inicio or cfg["data_inicio"])
    base = pagina_blog()
    dias = gerar(cfg, produtos, inicio, base)
    bio_links = [(s, montar_link(base, "instagram", "bio", "perfil", f"semana{s}")) for s in sorted({d["semana"] for d in dias})]

    os.makedirs(PASTA_SAIDA, exist_ok=True)
    carimbo = datetime.now().strftime("%Y-%m-%d_%Hh%M")
    arq_html = os.path.join(PASTA_SAIDA, f"calendario_instagram_{carimbo}.html")
    arq_csv = os.path.join(PASTA_SAIDA, f"calendario_instagram_{carimbo}.csv")
    arq_ics = os.path.join(PASTA_SAIDA, f"lembretes_instagram_{carimbo}.ics")
    salvar_html(cfg, dias, arq_html, bio_links)
    salvar_csv(dias, arq_csv)
    salvar_ics(dias, arq_ics)

    posts = [d for d in dias if d["post"]]
    print(f"📅 {inicio:%d/%m/%Y} a {dias[-1]['data']:%d/%m/%Y} · {len(posts)} posts no feed "
          f"({sum(d['post']['formato'] == 'reels' for d in posts)} Reels, {sum(d['post']['formato'] == 'carrossel' for d in posts)} carrosséis)")
    print(f"✅ {arq_html}\n✅ {arq_csv}\n✅ {arq_ics}")
    if args.registrar_rastreio:
        print("🔗 Registrando links no rastreamento:")
        registrar_rastreio(dias, bio_links)
    else:
        print("Dica: rode com --registrar-rastreio para os links aparecerem no gerar_links_anuncios.")


if __name__ == "__main__":
    main()
