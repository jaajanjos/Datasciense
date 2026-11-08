"""
Relatório de ACESSOS e VENDAS por ANÚNCIO da página https://comprenolink.net/melhores-produtos-mercado-livre-2026/
(grátis, dados do seu próprio WordPress + relatório do Mercado Livre Afiliados).

Considera SOMENTE a página do guia (config 'pagina_blog'): acessos de outras páginas do site
são ignorados. Mostra quem está acessando / acessou (de forma anônima), de qual anúncio veio,
quais produtos (links meli.la) foram clicados e as VENDAS APROVADAS feitas através do guia.

Uso:
    python 3_relatorio_acessos_anuncios.py              # últimos 30 dias
    python 3_relatorio_acessos_anuncios.py --dias 7
    python 3_relatorio_acessos_anuncios.py --demo       # dados de exemplo (para ver o relatório antes de instalar)
    python 3_relatorio_acessos_anuncios.py --arquivo dados_acessos/acessos_20260929_1200.json
    python 3_relatorio_acessos_anuncios.py --vendas "C:/Downloads/vendas_ml.xlsx"

COMPRAS:
  * Possível compra (estimativa): pontuação de intenção por visitante, calculada pelos cliques.
  * Compra confirmada: exporte o relatório de vendas do painel Mercado Livre Afiliados (CSV ou XLSX)
    para D:\\mercado_livre\\vendas_afiliados\\ — cada venda é cruzada com os cliques (produto + horário)
    para descobrir de qual anúncio ela veio.
"""
import argparse
import csv
import glob
import html
import json
import os
import random
import re
import sys
import time
import unicodedata
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from difflib import SequenceMatcher

# No .exe (PyInstaller) a pasta é a do próprio executável
PASTA = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
# Config (cópia única): programas_fontes_python\config_rastreio.json (os outros caminhos são só tolerância)
PASTA_FONTES = "D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios/programas_fontes_python"
PASTA_GERA = "D:/mercado_livre/1- Gera_Relatorio"
CONFIG = next((c for c in (os.path.join(PASTA_FONTES, "config_rastreio.json"),
                           os.path.join(PASTA, "config_rastreio.json"),
                           os.path.join(PASTA_GERA, "config_rastreio.json")) if os.path.exists(c)),
              os.path.join(PASTA_FONTES, "config_rastreio.json"))
# Cópias brutas dos acessos: sempre em 1- Gera_Relatorio\dados_acessos (o 7_limpar_historico limpa lá)
PASTA_DADOS = os.path.join(PASTA_GERA, "dados_acessos")
# Relatório HTML: sempre no histórico do painel diário (lido pelo ATUALIZAR_PAINEL.bat)
PASTA_SAIDA_HTML = "D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios/_historico_relatorios"
SAIDA_HTML = os.path.join(PASTA_SAIDA_HTML, "relatorio_acessos_anuncios.html")
PASTA_VENDAS = "D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios/vendas_afiliados"
# Situação dos anúncios no ML: gravada pelo 6_verificar_anuncios.py (também usado pelo ATUALIZAR_PAINEL.bat)
PASTA_STATUS = "D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios/anuncios_status"
HIST_STATUS = os.path.join(PASTA_STATUS, "historico_status_anuncios.csv")
HORAS_VERIFICACAO = 12   # verificação mais velha que isso: o relatório verifica de novo
DIAS_FORA_DO_AR = 15     # quadro "fora do ar" mostra o que caiu nos últimos N dias
FAIXA_PRECO = 0.20       # substituto: preço até 20% acima/abaixo do anterior

# Página analisada: o relatório considera SOMENTE acessos, cliques e vendas desta página
PAGINA_PADRAO = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"
SITE_PADRAO = "https://comprenolink.net"
# Endereços que a mesma página já teve (o histórico continua contando; config 'paginas_antigas')
PAGINAS_ANTIGAS = ["https://comprenolink.net/5-2/"]

# Situação da venda no painel de afiliados (verificado nesta ordem)
STATUS_CANCELADA = ["cancel", "devol", "estorn", "reembols", "recus", "rejeit", "chargeback", "refund", "invalid"]
STATUS_PENDENTE = ["pend", "aguard", "process", "analise", "a liberar", "retid", "bloque", "andamento", "pending", "review"]
STATUS_APROVADA = ["aprov", "pago", "paga", "confirm", "conclu", "liberad", "entreg", "disponivel", "efetuad",
                   "realizad", "finaliz", "complet", "approved", "paid", " ok "]
JANELA_COMPRA_HORAS = 24  # venda até X horas depois do clique é atribuída ao clique

MEIOS_PAGOS = {"cpc", "ppc", "paid", "pago", "ads", "anuncio", "anúncio", "paid_social", "display"}
REDES = {"tiktok", "instagram", "facebook", "kwai", "pinterest", "youtube", "whatsapp",
         "telegram", "x", "twitter", "linkedin", "snapchat"}
BUSCAS = {"google", "bing", "yahoo", "duckduckgo", "ecosia"}
DOMINIOS = [
    ("tiktok", "tiktok"), ("instagram", "instagram"), ("facebook", "facebook"), ("fb.", "facebook"),
    ("youtube", "youtube"), ("youtu.be", "youtube"), ("whatsapp", "whatsapp"), ("kwai", "kwai"),
    ("pinterest", "pinterest"), ("t.co", "x"), ("twitter", "x"), ("t.me", "telegram"),
    ("google", "google"), ("bing", "bing"), ("yahoo", "yahoo"), ("duckduckgo", "duckduckgo"),
    ("linkedin", "linkedin"), ("lnkd.in", "linkedin"),
]

TIPOS_TRAFEGO = [
    "Anúncio pago",
    "Divulgação (link etiquetado)",
    "Rede social (sem etiqueta)",
    "Busca orgânica",
    "Outro site",
    "Direto / desconhecido",
]


# ------------------------------------------------------------------ dados
def baixar_dados(cfg, dias):
    desde = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d")
    qs = f"desde={desde}&_={int(time.time())}"
    urls = [
        f"{cfg['site'].rstrip('/')}/wp-json/rastreio/v1/dados?{qs}",
        f"{cfg['site'].rstrip('/')}/?rest_route=/rastreio/v1/dados&{qs}",
    ]
    ultimo_erro = None
    for url in urls:
        req = urllib.request.Request(url, headers={
            "X-Rastreio-Chave": cfg["chave"],
            "User-Agent": "RelatorioAcessos/1.0",
            "Cache-Control": "no-cache",
        })
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.loads(r.read().decode("utf-8"))
        except urllib.error.HTTPError as e:
            ultimo_erro = e
            if e.code in (401, 403):
                raise SystemExit("❌ Chave recusada (401/403). Confira se 'chave' no config_rastreio.json "
                                 "é igual à RASTREIO_CHAVE do snippet no WordPress.")
            if e.code != 404:
                break
        except Exception as e:
            ultimo_erro = e
            break
    raise SystemExit(f"❌ Não foi possível baixar os dados: {ultimo_erro}\n"
                     "   Verifique se o snippet está ATIVO no Code Snippets.")


def dados_demo(dias):
    random.seed(7)
    agora = datetime.now()
    produtos = ["Fone JBL Bluetooth On-Ear", "Fone In-Ear QCY", "Amazon Echo Dot 5ª Geração",
                "Smart TV Philco 32\"", "Smart TV LG 32\"/50\"", "Console PlayStation 5",
                "Samsung Galaxy A15 128GB/256GB", "Carregador Turbo USB-C"]
    fontes = [
        (30, dict(origem="tiktok", meio="video", campanha="fones_jbl_vs_qcy", conteudo="01_fones_jbl_vs_qcy", app="TikTok")),
        (22, dict(origem="tiktok", meio="video", campanha="alexa_echo_dot_5", conteudo="02_alexa_echo_dot_5", app="TikTok")),
        (18, dict(origem="tiktok", meio="video", campanha="smart_tv_philco_vs_lg", conteudo="03_smart_tv_philco_vs_lg", app="TikTok")),
        (10, dict(origem="tiktok", meio="cpc", campanha="tiktok_ads_teste", conteudo="anuncio_pago", app="TikTok")),
        (8, dict(origem="", meio="", campanha="", conteudo="", app="Instagram")),
        (7, dict(origem="", meio="", campanha="", conteudo="", referencia="www.google.com")),
        (5, dict(origem="whatsapp", meio="social", campanha="grupos", conteudo="mensagem")),
        (10, dict(origem="", meio="", campanha="", conteudo="")),
    ]
    pesos = [f[0] for f in fontes]
    eventos, n = [], 0
    for v in range(260):
        fonte = random.choices(fontes, pesos)[0][1]
        vid = f"v{v:04d}{random.randint(1000, 9999)}"
        celular = random.random() < 0.85
        so = random.choice(["Android", "Android", "iOS"]) if celular else random.choice(["Windows", "macOS"])
        for s in range(random.choice([1, 1, 1, 2, 3])):
            t = agora - timedelta(days=random.uniform(0, dias), hours=random.uniform(0, 3))
            t = t.replace(hour=random.choice(range(7, 24)))
            if t > agora:
                t = agora - timedelta(minutes=random.randint(1, 600))
            base = dict(visitante=vid, sessao=f"{vid}s{s}", pagina="/melhores-produtos-mercado-livre-2026/", origem="", meio="", campanha="",
                        conteudo="", referencia="", app="", dispositivo="celular" if celular else "computador",
                        sistema=so, navegador="Chrome" if so != "iOS" else "Safari", ip_hash=vid[:12],
                        produto="", link="")
            base.update(fonte)
            n += 1
            eventos.append({**base, "id": n, "tipo": "visita", "criado_em": t.strftime("%Y-%m-%d %H:%M:%S")})
            for c in range(random.choices([0, 1, 2], [55, 35, 10])[0]):
                n += 1
                t2 = t + timedelta(seconds=random.randint(20, 240) * (c + 1))
                eventos.append({**base, "id": n, "tipo": "clique", "criado_em": t2.strftime("%Y-%m-%d %H:%M:%S"),
                                "produto": random.choice(produtos), "link": "https://meli.la/exemplo"})
    for i in range(40):  # acessos em OUTRAS páginas do site: devem ser ignorados pelo relatório
        n += 1
        t = agora - timedelta(days=random.uniform(0, dias))
        eventos.append({**base, "id": n, "visitante": f"outra{i}", "sessao": f"outra{i}", "tipo": "visita",
                        "pagina": random.choice(["/", "/sobre/", "/contato/"]),
                        "criado_em": t.strftime("%Y-%m-%d %H:%M:%S")})
    for m in (2, 9, 17):  # alguns acessando agora
        n += 1
        eventos.append({**base, "id": n, "visitante": f"agora{m}", "sessao": f"agora{m}", "tipo": "visita",
                        "criado_em": (agora - timedelta(minutes=m)).strftime("%Y-%m-%d %H:%M:%S")})
    eventos.sort(key=lambda e: e["criado_em"])
    return {"gerado_em": agora.strftime("%Y-%m-%d %H:%M:%S"), "total": len(eventos), "eventos": eventos}


# ------------------------------------------------------------------ classificação
def canal(e):
    if e.get("origem"):
        return e["origem"].lower()
    if e.get("app"):
        return e["app"].lower()
    ref = (e.get("referencia") or "").lower()
    for trecho, nome in DOMINIOS:
        if trecho in ref:
            return nome
    return ref or "direto"


def tipo_trafego(e):
    c = canal(e)
    if (e.get("meio") or "").lower() in MEIOS_PAGOS:
        return "Anúncio pago"
    if e.get("campanha"):
        return "Divulgação (link etiquetado)"
    if e.get("app") or c in REDES:
        return "Rede social (sem etiqueta)"
    if c in BUSCAS:
        return "Busca orgânica"
    if e.get("referencia"):
        return "Outro site"
    return "Direto / desconhecido"


def veio_de_anuncio(e):
    return tipo_trafego(e) in ("Anúncio pago", "Divulgação (link etiquetado)")


def quem(e):
    return e.get("visitante") or e.get("ip_hash") or "?"


def chave_grupo(e):
    return (tipo_trafego(e), canal(e), e.get("campanha") or "—", e.get("conteudo") or "—")


# ------------------------------------------------------------------ compras
PALAVRAS_VAZIAS = {"de", "da", "do", "das", "dos", "com", "para", "e", "o", "a", "em", "sem", "mais",
                   "vendido", "vendidos", "melhor", "oferta", "novo", "original", "lacrado", "cor", "unidade"}

# Palavras que identificam cada coluna no arquivo exportado do painel de afiliados (ordem importa)
COLUNAS_VENDAS = [
    ("comissao", ["comissao", "ganho", "ganhos", "comision", "commission", "receita afiliado"]),
    ("data", ["data", "fecha", "date", "dia", "criado"]),
    ("produto", ["produto", "titulo", "item", "anuncio", "descricao", "nome"]),
    ("status", ["status", "situacao", "estado"]),
    ("valor", ["valor", "preco", "total", "monto", "price"]),
]


# Cabeçalhos que indicam que a planilha informa DE ONDE veio a venda (link, etiqueta, canal)
PALAVRAS_ORIGEM = ["etiqueta", "tag", "canal", "fonte", "origem", "sub id", "subid"]


def normalizar(txt):
    txt = unicodedata.normalize("NFKD", str(txt or "")).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z0-9]+", " ", txt).strip()


def tokens(txt):
    return {t for t in normalizar(txt).split() if len(t) > 1 and t not in PALAVRAS_VAZIAS}


def similaridade(a, b):
    """0 a 1: quanto o título da venda parece com o produto clicado no blog."""
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    sobrepos = len(ta & tb) / min(len(ta), len(tb))
    return max(SequenceMatcher(None, normalizar(a), normalizar(b)).ratio(), sobrepos * 0.95)


def ler_data(v):
    """Devolve (datetime, tem_hora) ou (None, False)."""
    if isinstance(v, datetime):
        return v, (v.hour, v.minute, v.second) != (0, 0, 0)
    s = str(v or "").strip()
    for fmt, tem_hora in (("%d/%m/%Y %H:%M:%S", True), ("%d/%m/%Y %H:%M", True), ("%Y-%m-%d %H:%M:%S", True),
                          ("%Y-%m-%dT%H:%M:%S", True), ("%Y-%m-%d %H:%M", True), ("%d/%m/%Y", False),
                          ("%d/%m/%y", False), ("%Y-%m-%d", False), ("%d-%m-%Y", False)):
        try:
            return datetime.strptime(s[:19], fmt), tem_hora
        except ValueError:
            continue
    return None, False


def ler_valor(v):
    if isinstance(v, (int, float)):
        return float(v)
    s = re.sub(r"[^\d,.\-]", "", str(v or ""))
    if not s:
        return None
    if "," in s:
        s = s.replace(".", "").replace(",", ".")
    try:
        return float(s)
    except ValueError:
        return None


def ler_planilha(caminho):
    """Lê CSV ou XLSX e devolve lista de linhas (listas)."""
    if caminho.lower().endswith((".xlsx", ".xlsm")):
        import openpyxl
        wb = openpyxl.load_workbook(caminho, read_only=True, data_only=True)
        return [list(r) for r in wb.active.iter_rows(values_only=True)]
    for enc in ("utf-8-sig", "latin-1"):
        try:
            with open(caminho, encoding=enc, newline="") as f:
                amostra = f.read(4096)
                f.seek(0)
                try:
                    dialeto = csv.Sniffer().sniff(amostra, delimiters=";,\t")
                except csv.Error:
                    dialeto = csv.excel
                return [r for r in csv.reader(f, dialeto)]
        except UnicodeDecodeError:
            continue
    return []


def mapear_colunas(cabecalho, manual):
    nomes = [normalizar(c) for c in cabecalho]
    mapa, usados = {}, set()
    for campo, nome_manual in (manual or {}).items():
        if normalizar(nome_manual) in nomes:
            mapa[campo] = nomes.index(normalizar(nome_manual))
            usados.add(mapa[campo])
    for campo, palavras in COLUNAS_VENDAS:
        if campo in mapa:
            continue
        for i, nome in enumerate(nomes):
            if i not in usados and any(p in nome for p in palavras):
                mapa[campo] = i
                usados.add(i)
                break
    return mapa


def carregar_vendas(origem, manual=None):
    """Lê todos os CSV/XLSX de vendas (arquivo ou pasta). Tolerante ao formato do painel."""
    if not origem or not os.path.exists(origem):
        return [], []
    arquivos = [origem] if os.path.isfile(origem) else sorted(
        glob.glob(os.path.join(origem, "*.csv")) + glob.glob(os.path.join(origem, "*.xlsx")))
    vendas, avisos, vistos = [], [], set()
    for arq in arquivos:
        try:
            linhas = [r for r in ler_planilha(arq) if any(c not in (None, "") for c in r)]
        except Exception as e:
            avisos.append(f"{os.path.basename(arq)}: não foi possível ler ({e})")
            continue
        # o cabeçalho pode não estar na 1ª linha (planilhas com título)
        idx_cab, mapa = None, {}
        for i, r in enumerate(linhas[:15]):
            m = mapear_colunas([c if c is not None else "" for c in r], manual)
            if "data" in m and "produto" in m:
                idx_cab, mapa = i, m
                break
        if idx_cab is None:
            avisos.append(f"{os.path.basename(arq)}: não achei as colunas de DATA e PRODUTO "
                          "(configure 'colunas_vendas' no config_rastreio.json)")
            continue
        if "status" not in mapa:
            avisos.append(f"{os.path.basename(arq)}: sem coluna de STATUS — todas as vendas deste arquivo foram "
                          "consideradas aprovadas (configure 'colunas_vendas' → 'status' se o painel informar)")
        cab_norm = " | ".join(normalizar(c) for c in linhas[idx_cab] if c)
        tem_coluna_origem = any(p in cab_norm for p in PALAVRAS_ORIGEM)
        tem_melila = any("meli.la" in str(c).lower() for r in linhas[idx_cab + 1:] for c in r if c)
        for r in linhas[idx_cab + 1:]:
            pega = lambda campo: r[mapa[campo]] if campo in mapa and mapa[campo] < len(r) else None
            dt, tem_hora = ler_data(pega("data"))
            produto = str(pega("produto") or "").strip()
            if not dt or not produto:
                continue
            status = str(pega("status") or "").strip()
            situacao = classificar_status(status) if "status" in mapa else "aprovada"
            venda = {"dt": dt, "tem_hora": tem_hora, "produto": produto, "valor": ler_valor(pega("valor")),
                     "comissao": ler_valor(pega("comissao")),
                     "status": status if "status" in mapa else "(sem coluna de status)",
                     "situacao": situacao, "cancelada": situacao == "cancelada",
                     "arquivo": os.path.basename(arq),
                     # texto da linha inteira: usado para achar link meli.la / etiqueta do comprenolink
                     "linha_txt": " | ".join(str(c) for c in r if c not in (None, "")).lower(),
                     "tem_coluna_origem": tem_coluna_origem, "tem_melila": tem_melila}
            chave = (dt, normalizar(produto), venda["valor"])
            if chave not in vistos:
                vistos.add(chave)
                vendas.append(venda)
    vendas.sort(key=lambda v: v["dt"])
    return vendas, avisos


def classificar_status(status):
    """'aprovada', 'pendente' ou 'cancelada'. Status vazio/desconhecido = pendente (não conta como aprovada)."""
    s = f" {normalizar(status)} "
    if any(p in s for p in STATUS_CANCELADA):
        return "cancelada"
    if any(p in s for p in STATUS_PENDENTE):
        return "pendente"
    if any(p in s for p in STATUS_APROVADA):
        return "aprovada"
    return "pendente"


def caminho_pagina(url_ou_caminho):
    """'https://comprenolink.net/melhores-produtos-mercado-livre-2026/?x=1' -> '/melhores-produtos-mercado-livre-2026'"""
    from urllib.parse import urlsplit
    caminho = urlsplit(str(url_ou_caminho or "")).path or "/"
    return "/" + caminho.strip("/") if caminho.strip("/") else "/"


def filtrar_pagina(eventos, pagina_alvo):
    """Mantém só os eventos da página analisada (ex.: /melhores-produtos-mercado-livre-2026/). Devolve (da_pagina, ignorados)."""
    alvos = {caminho_pagina(pagina_alvo)} | {caminho_pagina(p) for p in PAGINAS_ANTIGAS}
    da_pagina = [e for e in eventos if caminho_pagina(e.get("pagina")) in alvos]
    return da_pagina, len(eventos) - len(da_pagina)


def atribuir_vendas(vendas, cliques, janela_horas):
    """Liga cada venda ao clique no blog que mais provavelmente a gerou."""
    janela = timedelta(hours=janela_horas)
    for v in vendas:
        fim = v["dt"] if v["tem_hora"] else v["dt"].replace(hour=23, minute=59, second=59)
        inicio = (v["dt"] if v["tem_hora"] else v["dt"].replace(hour=0, minute=0, second=0)) - janela
        candidatos = [c for c in cliques if inicio <= c["_dt"] <= fim]
        v["clique"], v["sim"], v["confianca"] = None, 0.0, "Sem clique rastreado"
        if not candidatos:
            continue
        melhor = max(candidatos, key=lambda c: (similaridade(v["produto"], c.get("produto")), c["_dt"]))
        sim = similaridade(v["produto"], melhor.get("produto"))
        if sim >= 0.5:
            perto = v["tem_hora"] and fim - melhor["_dt"] <= timedelta(hours=6)
            v["clique"], v["sim"] = melhor, sim
            v["confianca"] = "Alta" if sim >= 0.7 and perto else "Média"
        else:
            # O ML também paga comissão de outros produtos comprados depois do clique
            v["clique"] = max(candidatos, key=lambda c: c["_dt"])
            v["sim"], v["confianca"] = sim, "Baixa"
    return vendas


def links_do_blog(cfg, cliques, pagina_alvo):
    """Códigos meli.la da página analisada (guia): lidos da própria página + cliques registrados nela."""
    codigos = set()
    for c in cliques:
        codigos.update(re.findall(r"meli\.la/([A-Za-z0-9]+)", c.get("link") or ""))
    for extra in cfg.get("links_blog_extra", []):
        codigos.update(re.findall(r"meli\.la/([A-Za-z0-9]+)", extra))
    try:
        req = urllib.request.Request(pagina_alvo, headers={"User-Agent": "Mozilla/5.0 RelatorioAcessos/1.0"})
        with urllib.request.urlopen(req, timeout=30) as r:
            codigos.update(re.findall(r"meli\.la/([A-Za-z0-9]+)", r.read().decode("utf-8", "ignore")))
    except Exception as e:
        print(f"   ⚠️ Não consegui ler os links de {pagina_alvo} ({e}); usando só os cliques registrados.")
    return {c.lower() for c in codigos}


def filtrar_comprenolink(vendas, codigos_blog, etiqueta):
    """Mantém SOMENTE as vendas que vieram da página analisada (guia). Devolve (da_pagina, descartadas)."""
    etiqueta = (etiqueta or "").lower().strip()
    do_blog, descartadas = [], []
    for v in vendas:
        txt = v.get("linha_txt", "")
        achou_link = next((c for c in codigos_blog if f"meli.la/{c}" in txt), None)
        achou_etq = bool(etiqueta) and etiqueta in txt
        if achou_link or achou_etq:
            v["prova"] = f"link meli.la/{achou_link}" if achou_link else f"etiqueta '{etiqueta}'"
            do_blog.append(v)
        elif v.get("tem_melila") or (etiqueta and v.get("tem_coluna_origem")):
            v["motivo"] = "a planilha informa o link/etiqueta e ele não é da página do guia"
            descartadas.append(v)
        elif v["clique"] and v["confianca"] in ("Alta", "Média"):
            v["prova"] = f"clique na página do guia no mesmo produto ({v['confianca'].lower()})"
            do_blog.append(v)
        else:
            v["motivo"] = ("sem clique na página do guia nas horas anteriores" if not v["clique"]
                           else "houve clique no guia, mas em outro produto")
            descartadas.append(v)
    return do_blog, descartadas


def intencao_compra(eventos_visitante):
    """Pontuação 0-100 de chance de compra, a partir do comportamento no blog."""
    evs = sorted(eventos_visitante, key=lambda e: e["_dt"])
    cl = [e for e in evs if e["tipo"] == "clique"]
    if not cl:
        return 0, []
    pontos, motivos = 40, ["clicou em produto"]
    por_prod = Counter(e.get("produto") for e in cl)
    if max(por_prod.values()) >= 2:
        pontos += 20
        motivos.append("clicou 2+ vezes no mesmo produto")
    if len({e.get("sessao") for e in cl}) >= 2:
        pontos += 20
        motivos.append("voltou outro momento e clicou de novo")
    if evs[-1]["tipo"] == "clique":
        pontos += 10
        motivos.append("saiu do blog direto para o Mercado Livre")
    if len(por_prod) == 1:
        pontos += 10
        motivos.append("focado em um único produto")
    return min(pontos, 100), motivos


def nivel_intencao(p):
    if p >= 70:
        return "alta", "🔥 Alta"
    if p >= 50:
        return "media", "Média"
    if p > 0:
        return "baixa", "Baixa"
    return "", "—"


def vendas_demo(cliques):
    random.seed(11)
    vendas = []
    for c in random.sample(cliques, max(1, len(cliques) // 12)):
        dt = c["_dt"] + timedelta(minutes=random.randint(3, 60 * 20))
        if dt > datetime.now():
            continue
        valor = round(random.uniform(60, 3500), 2)
        vendas.append({"dt": dt, "tem_hora": True, "produto": f"{c['produto']} Original Lacrado",
                       "valor": valor, "comissao": round(valor * random.choice([0.04, 0.06, 0.08]), 2),
                       "status": random.choice(["Aprovada"] * 6 + ["Pendente"] * 2 + ["Cancelada"]), "arquivo": "DEMO"})
    vendas.append({"dt": datetime.now() - timedelta(days=3), "tem_hora": True, "produto": "Air Fryer Mondial 4L",
                   "valor": 399.9, "comissao": 23.99, "status": "Aprovada", "arquivo": "DEMO"})
    for v in vendas:
        v["situacao"] = classificar_status(v["status"])
        v["cancelada"] = v["situacao"] == "cancelada"
    vendas.sort(key=lambda v: v["dt"])
    return vendas


def brl(v):
    return "—" if v is None else "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# ------------------------------------------------------------------ html helpers
esc = lambda s: html.escape(str(s if s is not None else ""))


def barras(contagem, total=None, cor="#3483fa", limite=12):
    total = total or sum(contagem.values()) or 1
    maior = max(contagem.values(), default=1) or 1
    linhas = []
    for nome, v in contagem.most_common(limite):
        linhas.append(f"""<div class="barra"><span class="rot">{esc(nome)}</span>
<span class="trilho"><span class="enche" style="width:{v / maior * 100:.1f}%;background:{cor}"></span></span>
<span class="val">{v} <small>({v / total * 100:.0f}%)</small></span></div>""")
    return "".join(linhas) or '<p class="vazio">Sem dados</p>'


def colunas(serie, cor="#3483fa"):
    maior = max((v for _, v in serie), default=1) or 1
    cols = "".join(
        f'<div class="col" title="{esc(r)}: {v}"><span class="cv">{v or ""}</span>'
        f'<span class="cb" style="height:{v / maior * 100:.1f}%;background:{cor}"></span>'
        f'<span class="cr">{esc(r)}</span></div>'
        for r, v in serie
    )
    return f'<div class="colunas">{cols}</div>'


# ------------------------------------------------------------------ relatório
# ---------------------------------------------------------------- anúncios fora do ar + substituição
# Categorias da tabela "Escolha rápida" do guia; o item é classificado pelo nome (1ª regra que bater)
CATEGORIAS = [
    ("🍼 Bebê & Maternidade", "bebe|recem nascid|maternidade|naninha|mobile|trocador|ninho|enxoval|swaddle"),
    ("👕 Moda Infantil & Juvenil", "infantil|juvenil|menina|menino|calcinha|meia 5 dedinhos"),
    ("🌸 Beleza & Saúde", "perfume|colageno|omega|magnesio|vitamina|coenzima|licopeno|propolis|resveratrol|multivitam|"
                         "barbeador|cortar cabelo|secador|prancha|skincare|hidratante|oleo|pressao arterial|nebulizador|"
                         "glucosamina|joint fix|renovadores"),
    ("🎧 Áudio & TV", "fone|headset|caixa de som|caixa amplificada|soundbar|smart tv|projetor|tela de projecao|receptor|"
                     "echo dot|alexa|fire tv|boombox"),
    ("💻 Tecnologia & Informática", "notebook|monitor|mouse|teclado|teclas|ssd|impressora|tablet|kindle|smartphone|"
                                   "motorola|xiaomi|galaxy|carregador|power bank|smartwatch|camera|capinha|capa para|pelicula"),
    ("💪 Esporte & Fitness", "bicicleta|bike|halter|yoga|legging|academia|whey|creatina|bola|barra fixa|joelheira|"
                            "tornozeleira|treino|bermuda|maio|tenis|mochila|elastico"),
    ("🔧 Ferramentas & Utilidades", "parafusadeira|furadeira|esmerilhadeira|chave|bits|ferramentas|trena|nivel a laser|"
                                   "lavadora|compressor|motosserra|soprador|silicone|torneira"),
    ("🛋️ Casa, Cama & Decoração", "cama|colcha|cobre leito|coberta|cobertor|lencol|fronha|travesseiro|toalha|cabeceira|"
                                  "espelho|arara|cortina|natal|natalin|pisca|rede de dormir|solitario|tacas|kit festa"),
    ("🏠 Casa & Eletrodomésticos", "air fryer|fritadeira|liquidificador|cafeteira|panela|chaleira|pipoqueira|churrasqueira|"
                                  "marmita|mixer|cozedor|aspirador|mop|ventilador|pote|forma|assadeira|tempero|garrafa|"
                                  "copo termico|pano de prato|micro ondas|lixeira"),
]
# Ordem de prioridade para escolher o substituto: sempre a MELHOR política de venda
REQUISITOS_SUBSTITUTO = [
    "<b>Mesmo produto</b> (mesmo código de catálogo, outro vendedor). Só se não houver: mesmo tipo de produto e mesma categoria do guia.",
    "Anúncio <b>ativo</b>, produto <b>novo</b> e com estoque.",
    "<b>Melhor política de venda</b>, nesta ordem: vendedor <b>MercadoLíder</b> (Platinum › Gold › Líder) ou reputação "
    "<b>verde</b>; envio <b>Full</b>; <b>frete grátis</b>; <b>devolução grátis</b>; <b>garantia</b> informada (de fábrica ou do vendedor).",
    "Nota <b>4,5 ou mais</b>, com muitas avaliações e muitas unidades vendidas.",
    f"Preço até <b>{FAIXA_PRECO:.0%}</b> acima ou abaixo do anúncio anterior. Empate na política de venda: o de menor preço.",
    "Gerar o link no <b>ML Afiliados</b> (Gerar link → copiar o meli.la) e trocar no item do guia, no botão e na foto.",
]


def categoria_do_item(nome):
    n = f" {normalizar(nome)} "
    for cat, chaves in CATEGORIAS:
        if any(f" {c}" in n for c in chaves.split("|")):
            return cat
    return "—"


def verificacao_antiga(horas=HORAS_VERIFICACAO):
    """True se a última verificação dos anúncios no ML tiver mais de N horas (ou não existir)."""
    if not os.path.exists(HIST_STATUS):
        return True
    return time.time() - os.path.getmtime(HIST_STATUS) > horas * 3600


def verificar_anuncios_agora():
    """Roda o 6_verificar_anuncios.py (embutido no .exe) e grava em anuncios_status."""
    import importlib
    if not getattr(sys, "frozen", False):
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    try:
        v = importlib.import_module("6_verificar_anuncios")
    except ImportError as e:
        print(f"   ⚠️ Verificador de anúncios não encontrado ({e}); será usada a última verificação.")
        return False
    # no .exe o __file__ do módulo fica numa pasta temporária: aponta os caminhos para a estrutura oficial
    v.BASE = "D:/mercado_livre"
    v.PASTA, v.HISTORICO = PASTA_STATUS, HIST_STATUS
    if os.path.exists(CONFIG):
        v.CONFIG = CONFIG
    try:
        return v.main(pausa=1) == 0
    except Exception as e:  # sem internet etc.: o relatório continua com a última verificação
        print(f"   ⚠️ Não consegui verificar agora ({e}); será usada a última verificação.")
        return False


def preco_float(v):
    try:
        return float(str(v).replace(",", "."))
    except ValueError:
        return None


def situacao_anuncios(dias=DIAS_FORA_DO_AR):
    """Lê o histórico de verificações e devolve o que ficou fora do ar nos últimos N dias e o que já foi trocado."""
    if not os.path.exists(HIST_STATUS):
        return None
    with open(HIST_STATUS, encoding="utf-8-sig", newline="") as f:
        linhas = list(csv.DictReader(f, delimiter=";"))
    if not linhas:
        return None
    ultima = max(r["verificado_em"] for r in linhas)
    limite = (datetime.now() - timedelta(days=dias)).strftime("%Y-%m-%d %H:%M")
    atual = [r for r in linhas if r["verificado_em"] == ultima]
    atual_link = {r["link_afiliado"]: r for r in atual if r["link_afiliado"]}
    ultimo_preco = {}  # último preço conhecido de cada link (anúncio removido não mostra preço)
    primeira_vez = {}  # quando cada link apareceu no guia pela 1ª vez
    for r in sorted(linhas, key=lambda r: r["verificado_em"]):
        primeira_vez.setdefault(r["link_afiliado"], r["verificado_em"])
        if preco_float(r.get("preco_ml")):
            ultimo_preco[r["link_afiliado"]] = preco_float(r["preco_ml"])
    usados = set()  # cada link novo só substitui um anúncio
    episodios = {}
    for r in sorted(linhas, key=lambda r: r["verificado_em"]):
        if r["verificado_em"] < limite or r["status"] in ("Ativo", "Não verificado"):
            continue
        chave = r["link_afiliado"] or f"item-{r['item']}"
        ep = episodios.setdefault(chave, {"desde": r["verificado_em"], "item": r["item"]})
        ep["ultimo"] = r
    fora, trocados = [], []
    for chave, ep in episodios.items():
        r = ep["ultimo"]
        reg = {"item": r["item"], "nome": r["nome_no_blog"] or r["titulo_card"], "titulo": r["titulo_card"],
               "categoria": categoria_do_item(f"{r['nome_no_blog']} {r['titulo_card']}"),
               "status": r["status"], "aviso": r["aviso_ml"], "desde": ep["desde"], "ate": r["verificado_em"],
               "catalogo": r["catalogo_mlb"] or r["catalogo_no_blog"], "anuncio": r["anuncio_mlb"],
               "link": r["link_afiliado"], "preco": ultimo_preco.get(r["link_afiliado"])}
        cur = atual_link.get(r["link_afiliado"]) if r["link_afiliado"] else None
        if cur is not None:
            if cur["status"] == "Ativo":
                outro = cur["anuncio_mlb"] and r["anuncio_mlb"] and cur["anuncio_mlb"] != r["anuncio_mlb"]
                reg["hoje"] = ("voltou", "Voltou ao ar" + (f" (o ML passou o link para outro vendedor: {cur['anuncio_mlb']})"
                                                           if outro else " (mesmo anúncio, o vendedor reativou)"))
            else:
                reg["hoje"] = ("fora", f"Ainda fora do ar ({cur['status'].lower()})")
                reg.update(status=cur["status"], aviso=cur["aviso_ml"], ate=cur["verificado_em"])
        else:
            # link saiu do guia. Os itens são renumerados quando entra/sai produto, então o nº do item não basta:
            # substituto = link que entrou no guia depois que o antigo caiu, da mesma categoria, no nº mais próximo
            num = int(r["item"]) if str(r["item"]).isdigit() else 0
            candidatos = [c for c in atual if c["link_afiliado"] and c["link_afiliado"] not in usados
                          and primeira_vez.get(c["link_afiliado"], "") > ep["desde"]
                          and categoria_do_item(f"{c['nome_no_blog']} {c['titulo_card']}") == reg["categoria"]]
            candidatos.sort(key=lambda c: (-round(similaridade(reg["nome"], c["nome_no_blog"] or c["titulo_card"]), 1),
                                           abs((int(c["item"]) if str(c["item"]).isdigit() else 0) - num)))
            novo = candidatos[0] if candidatos and reg["categoria"] != "—" else None
            if novo:
                usados.add(novo["link_afiliado"])
                reg["item_novo"] = novo["item"]
            if novo and novo["status"] == "Ativo":
                reg["hoje"] = ("trocado", f"Substituído no guia (item {novo['item']})")
                reg["novo"] = {"nome": novo["nome_no_blog"] or novo["titulo_card"], "titulo": novo["titulo_ml"] or novo["titulo_card"],
                               "anuncio": novo["anuncio_mlb"], "preco": preco_float(novo["preco_ml"]),
                               "url": novo["url_anuncio"], "link": novo["link_afiliado"]}
                trocados.append(reg)
            elif novo:
                reg["hoje"] = ("fora", "Trocado no guia, mas o novo anúncio também está fora do ar")
            else:
                reg["hoje"] = ("voltou", "Link retirado do guia (sem substituto da mesma categoria)")
        fora.append(reg)
    ordem = {"fora": 0, "trocado": 1, "voltou": 2}
    fora.sort(key=lambda x: (ordem[x["hoje"][0]], int(x["item"]) if str(x["item"]).isdigit() else 0))
    return {"ultima": ultima, "total": len(atual), "ativos": sum(r["status"] == "Ativo" for r in atual),
            "fora": fora, "pendentes": [x for x in fora if x["hoje"][0] == "fora"], "trocados": trocados, "dias": dias}


def slug_busca(nome):
    palavras = [p for p in normalizar(re.sub(r"[–—(].*", "", nome)).split() if len(p) > 1][:7]
    return "-".join(palavras)


def quadros_anuncios(info):
    """HTML dos quadros 'Anúncios fora do ar' e, logo abaixo, 'Substituição'."""
    if info is None:
        return ('<div class="card"><h2>📉 Anúncios fora do ar</h2><p class="vazio">Ainda não há verificação dos anúncios '
                f'no ML (<code>{esc(HIST_STATUS)}</code>). Rode o relatório com internet ou o ATUALIZAR_PAINEL.bat.</p></div>')
    data = datetime.strptime(info["ultima"], "%Y-%m-%d %H:%M")
    selo = {"fora": "pago", "trocado": "on", "voltou": "etq"}
    linhas = "".join(
        f'<tr><td class="n">{esc(x["item"])}</td><td>{esc(x["nome"])}<br><small>{esc(x["titulo"])}</small></td>'
        f'<td>{esc(x["categoria"])}</td><td>{esc(x["status"])}<br><small>{esc(x["aviso"])}</small></td>'
        f'<td>{datetime.strptime(x["desde"], "%Y-%m-%d %H:%M"):%d/%m %H:%M}</td>'
        f'<td><span class="selo {selo[x["hoje"][0]]}">{esc(x["hoje"][1])}</span></td></tr>' for x in info["fora"])
    q1 = (f'<div class="card"><h2>📉 Anúncios que ficaram fora do ar (últimos {info["dias"]} dias)</h2>'
          f'<p><small>Última verificação no ML: <b>{data:%d/%m/%Y %H:%M}</b> · {info["ativos"]} de {info["total"]} anúncios '
          f'ativos · {len(info["pendentes"])} ainda fora do ar · {len(info["trocados"])} já substituído(s).</small></p>'
          '<table><tr><th>Item</th><th>Produto no guia</th><th>Categoria</th><th>O que o ML mostrou</th>'
          f'<th>Fora do ar desde</th><th>Situação hoje</th></tr>'
          f'{linhas or "<tr><td colspan=6 class=vazio>✔ Nenhum anúncio do guia ficou fora do ar no período.</td></tr>"}'
          '</table></div>')

    req = "".join(f"<li>{r}</li>" for r in REQUISITOS_SUBSTITUTO)
    pend = ""
    for x in info["pendentes"]:
        faixa = (f'{brl(x["preco"])}<br><small>aceitar {brl(x["preco"] * (1 - FAIXA_PRECO))} a '
                 f'{brl(x["preco"] * (1 + FAIXA_PRECO))}</small>') if x["preco"] else "<small>preço não disponível</small>"
        onde = []
        if x["catalogo"]:
            onde.append(f'<a href="https://www.mercadolivre.com.br/p/{esc(x["catalogo"])}/s" target="_blank">'
                        f'1º · Mesmo produto, outros vendedores ({esc(x["catalogo"])})</a>')
        onde.append(f'<a href="https://lista.mercadolivre.com.br/{esc(slug_busca(x["titulo"] or x["nome"]))}" target="_blank">'
                    f'{"2º" if x["catalogo"] else "1º"} · Buscar o mesmo tipo de produto</a>')
        if x["link"]:
            onde.append(f'<small>Link atual (fora do ar): {esc(x["link"])}</small>')
        pend += (f'<tr><td class="n">{esc(x["item"])}</td><td>{esc(x["nome"])}<br><small>{esc(x["categoria"])} · '
                 f'{esc(x["status"])}</small></td><td class="n">{faixa}</td><td>{"<br>".join(onde)}</td>'
                 f'<td><small>Escolher pelos requisitos acima → gerar o meli.la no ML Afiliados → trocar no item '
                 f'{esc(x["item"])} do guia → rodar este relatório de novo para confirmar.</small></td></tr>')
    troc = "".join(
        f'<tr><td class="n">{esc(x["item"])} → {esc(x["item_novo"])}</td><td>{esc(x["nome"])}<br><small>{esc(x["status"])} · '
        f'{esc(x["anuncio"] or "sem nº")}</small></td><td>{esc(x["novo"]["nome"])}<br><small>'
        + (f'<a href="{esc(x["novo"]["url"])}" target="_blank">{esc(x["novo"]["anuncio"])}</a>' if x["novo"]["url"]
           else esc(x["novo"]["anuncio"])) +
        f'</small></td><td class="n">{brl(x["novo"]["preco"]) if x["novo"]["preco"] else "—"}'
        + (f'<br><small>antes {brl(x["preco"])}</small>' if x["preco"] else "") +
        f'</td><td><span class="selo on">Ativo</span></td></tr>' for x in info["trocados"])
    q2 = ('<div class="card"><h2>🔁 Substituição dos anúncios fora do ar</h2>'
          '<p><b>Requisitos do substituto</b> (siga a ordem; vale sempre o de <b>melhor política de venda</b>):</p>'
          f'<ol>{req}</ol>'
          '<h3 style="color:#2d3277;font-size:15px">Precisam de substituto</h3>'
          '<table><tr><th>Item</th><th>Anúncio fora do ar</th><th>Preço antes / faixa</th>'
          f'<th>Onde procurar o substituto</th><th>Como trocar</th></tr>'
          f'{pend or "<tr><td colspan=5 class=vazio>✔ Nenhum anúncio precisa de substituto agora.</td></tr>"}</table>'
          '<h3 style="color:#2d3277;font-size:15px;margin-top:18px">Já substituídos</h3>'
          '<table><tr><th>Item</th><th>Saiu (fora do ar)</th><th>Entrou (substituto)</th><th>Preço</th><th>Situação</th></tr>'
          f'{troc or "<tr><td colspan=5 class=vazio>Nenhuma substituição registrada no período.</td></tr>"}</table>'
          '<p><small>"Já substituídos" é identificado automaticamente: link que entrou no guia depois que o antigo caiu, '
          'da mesma categoria e com o nome mais parecido.</small></p>'
          '<p><small>Os links de busca abrem no seu navegador. A escolha final e o link de afiliado são feitos por você no '
          'ML Afiliados (exige o seu login).</small></p></div>')
    return q1 + q2


def gerar(dados, origem_dados, vendas=None, avisos_vendas=None, janela_horas=JANELA_COMPRA_HORAS, demo_vendas=False,
          codigos_blog=None, etiqueta="", pagina_alvo=PAGINA_PADRAO, anuncios=None):
    # Só a página analisada (https://comprenolink.net/melhores-produtos-mercado-livre-2026/) entra no relatório
    eventos, ignorados = filtrar_pagina(dados.get("eventos", []), pagina_alvo)
    for e in eventos:
        e["_dt"] = datetime.strptime(e["criado_em"], "%Y-%m-%d %H:%M:%S")
    gerado = datetime.strptime(dados.get("gerado_em") or datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                               "%Y-%m-%d %H:%M:%S")

    visitas = [e for e in eventos if e["tipo"] == "visita"]
    cliques = [e for e in eventos if e["tipo"] == "clique"]
    sessoes = {e["sessao"] for e in visitas if e.get("sessao")}
    sessoes_clique = {e["sessao"] for e in cliques if e.get("sessao")}
    visitantes = {quem(e) for e in visitas}
    online = {quem(e) for e in eventos if gerado - e["_dt"] <= timedelta(minutes=30)}
    vis_anuncio = [e for e in visitas if veio_de_anuncio(e)]
    taxa = len(sessoes_clique & sessoes) / len(sessoes) * 100 if sessoes else 0

    # --- compras confirmadas (arquivo do painel ML) e possíveis compras (intenção)
    if demo_vendas:
        vendas = vendas_demo(cliques) if cliques else []
    vendas_todas = atribuir_vendas(vendas or [], cliques, janela_horas)
    if codigos_blog is None:
        codigos_blog = {c.lower() for e in cliques for c in re.findall(r"meli\.la/([A-Za-z0-9]+)", e.get("link") or "")}
    # Só contam as compras que vieram da página do guia ...
    vendas, descartadas = filtrar_comprenolink(vendas_todas, codigos_blog, etiqueta)
    # ... e, nos totais, só as APROVADAS
    validas = [v for v in vendas if v["situacao"] == "aprovada"]
    pendentes = [v for v in vendas if v["situacao"] == "pendente"]
    canceladas = [v for v in vendas if v["situacao"] == "cancelada"]
    comissao_total = sum(v["comissao"] or 0 for v in validas)
    valor_total = sum(v["valor"] or 0 for v in validas)
    comissao_pendente = sum(v["comissao"] or 0 for v in pendentes)
    compradores = {quem(v["clique"]): v for v in validas if v["clique"]}

    evs_vis = defaultdict(list)
    for e in eventos:
        evs_vis[quem(e)].append(e)
    intencao = {vid: intencao_compra(evs) for vid, evs in evs_vis.items()}
    possiveis = {vid for vid, (p, _) in intencao.items() if p >= 70 and vid not in compradores}

    # --- por anúncio
    grupos = defaultdict(lambda: {"visitas": 0, "vis": set(), "ses": set(), "cliques": 0, "ses_c": set(),
                                  "possiveis": set(), "compras": 0, "comissao": 0.0})
    for v in validas:
        if v["clique"]:
            g = grupos[chave_grupo(v["clique"])]
            g["compras"] += 1
            g["comissao"] += v["comissao"] or 0
    for vid in possiveis:
        ultimo_clique = max((e for e in evs_vis[vid] if e["tipo"] == "clique"), key=lambda e: e["_dt"])
        grupos[chave_grupo(ultimo_clique)]["possiveis"].add(vid)
    for e in eventos:
        g = grupos[chave_grupo(e)]
        if e["tipo"] == "visita":
            g["visitas"] += 1
            g["vis"].add(quem(e))
            g["ses"].add(e.get("sessao"))
        else:
            g["cliques"] += 1
            g["ses_c"].add(e.get("sessao"))
    ordem_tipo = {t: i for i, t in enumerate(TIPOS_TRAFEGO)}
    linhas_anuncio = ""
    for (tt, cn, camp, cont), g in sorted(grupos.items(), key=lambda kv: (ordem_tipo[kv[0][0]], -kv[1]["visitas"])):
        tx = len(g["ses_c"] & g["ses"]) / len(g["ses"]) * 100 if g["ses"] else 0
        selo = "pago" if tt == "Anúncio pago" else ("etq" if tt.startswith("Divulga") else "org")
        linhas_anuncio += (f'<tr><td><span class="selo {selo}">{esc(tt)}</span></td><td><b>{esc(cn)}</b></td>'
                           f'<td>{esc(camp)}<br><small>{esc(cont)}</small></td><td class="n">{g["visitas"]}</td>'
                           f'<td class="n">{len(g["vis"])}</td><td class="n">{g["cliques"]}</td>'
                           f'<td class="n">{tx:.0f}%</td><td class="n">{len(g["possiveis"]) or ""}</td>'
                           f'<td class="n"><b>{g["compras"] or ""}</b></td>'
                           f'<td class="n">{brl(g["comissao"]) if g["compras"] else ""}</td></tr>')

    # --- tabelas de vendas do guia (aprovadas / pendentes / canceladas)
    selo_sit = {"aprovada": ("on", "✅ Aprovada"), "pendente": ("int-media", "⏳ Pendente"),
                "cancelada": ("pago", "❌ Cancelada")}

    def linha_venda(v):
        c = v["clique"]
        conf = {"Alta": "on", "Média": "etq", "Baixa": "org"}.get(v["confianca"], "org")
        origem_txt = (f'<b>{esc(canal(c))}</b><br><small>{esc(c.get("campanha") or tipo_trafego(c))}</small>'
                      if c else '<small>link do guia (sem clique rastreado)</small>')
        clique_txt = (f'{c["_dt"]:%d/%m %H:%M} <code>#{esc(quem(c)[-6:])}</code><br><small>{esc(c.get("produto"))}</small>'
                      if c else "—")
        cls, rot = selo_sit[v["situacao"]]
        efetuada = (f'<span class="selo on">✅ Efetuada pelo</span><br><a href="{esc(pagina_alvo)}" target="_blank">'
                    f'{esc(pagina_alvo)}</a>' if v["situacao"] == "aprovada" else
                    f'<small>Feita pelo {esc(pagina_alvo)}<br>(ainda não aprovada)</small>')
        return (f'<tr><td>{v["dt"].strftime("%d/%m/%Y %H:%M" if v["tem_hora"] else "%d/%m/%Y")}</td>'
                f'<td>{esc(v["produto"])}</td><td>{efetuada}</td><td class="n">{brl(v["valor"])}</td>'
                f'<td class="n"><b>{brl(v["comissao"])}</b></td>'
                f'<td><span class="selo {cls}">{rot}</span><br><small>{esc(v["status"])}</small></td><td>{origem_txt}</td>'
                f'<td>{clique_txt}</td><td><span class="selo {conf}">{esc(v["confianca"])}</span>'
                f'<br><small>{esc(v.get("prova", ""))}</small></td></tr>')

    cab_vendas = ('<table><tr><th>Data da venda</th><th>Produto vendido</th><th>Efetuada por</th><th>Valor</th><th>Comissão</th>'
                  '<th>Situação</th><th>Anúncio de origem</th><th>Clique no guia</th><th>Veio do guia porque</th></tr>')
    ordem = lambda lst: sorted(lst, key=lambda v: v["dt"], reverse=True)
    linhas_compras = "".join(linha_venda(v) for v in ordem(validas))
    linhas_pendentes = "".join(linha_venda(v) for v in ordem(pendentes))
    linhas_canceladas = "".join(linha_venda(v) for v in ordem(canceladas))

    linhas_descartadas = "".join(
        f'<tr><td>{v["dt"].strftime("%d/%m/%Y %H:%M" if v["tem_hora"] else "%d/%m/%Y")}</td><td>{esc(v["produto"])}</td>'
        f'<td class="n">{brl(v["valor"])}</td><td class="n">{brl(v["comissao"])}</td><td><small>{esc(v["motivo"])}</small></td></tr>'
        for v in sorted(descartadas, key=lambda v: v["dt"], reverse=True))

    # --- tabela de possíveis compras (estimativa)
    linhas_possiveis = ""
    for vid in sorted(possiveis, key=lambda x: (-intencao[x][0], -max(e["_dt"] for e in evs_vis[x]).timestamp())):
        cl = [e for e in evs_vis[vid] if e["tipo"] == "clique"]
        ult = max(cl, key=lambda e: e["_dt"])
        prim_vis = next((e for e in sorted(evs_vis[vid], key=lambda e: e["_dt"]) if e["tipo"] == "visita"), ult)
        pts, motivos = intencao[vid]
        prods = list(dict.fromkeys(e.get("produto") for e in cl if e.get("produto")))
        linhas_possiveis += (f'<tr><td><code>#{esc(vid[-6:])}</code></td><td>{ult["_dt"]:%d/%m %H:%M}</td>'
                             f'<td>{esc("; ".join(prods[:3]))}</td>'
                             f'<td><b>{esc(canal(prim_vis))}</b><br><small>{esc(prim_vis.get("campanha") or tipo_trafego(prim_vis))}</small></td>'
                             f'<td class="n"><b>{pts}</b></td><td><small>{esc(", ".join(motivos))}</small></td></tr>')

    if vendas_todas:
        resumo = (f'<div class="resumo-vendas">'
                  f'<div><b class="ok">{len(validas)}</b><span>✅ aprovadas</span></div>'
                  f'<div><b class="pend">{len(pendentes)}</b><span>⏳ pendentes</span></div>'
                  f'<div><b class="canc">{len(canceladas)}</b><span>❌ canceladas</span></div>'
                  f'<div><b class="fora">{len(descartadas)}</b><span>🚫 de outros canais (ignoradas)</span></div></div>'
                  f'<p>Das {len(vendas_todas)} vendas do arquivo, <b>{len(vendas)}</b> foram feitas através de '
                  f'<b>{esc(pagina_alvo)}</b>. Somente as <b>aprovadas</b> entram nos totais.</p>')
        tabela = (cab_vendas + linhas_compras + '</table>' if validas else
                  '<div class="aviso">Nenhuma venda <b>aprovada</b> feita através do guia no período.</div>')
        bloco_vendas = (resumo + tabela +
                        f'<p><small>Conta como venda do guia: a planilha traz um link meli.la que está nessa página (ou a '
                        f'etiqueta configurada) <b>ou</b> houve clique no guia no mesmo produto até {janela_horas}h antes da venda '
                        f'(confiança <b>Alta</b>: até 6h; <b>Média</b>: produto parecido).</small></p>')
        if pendentes:
            bloco_vendas += (f'<details open><summary>⏳ {len(pendentes)} vendas do guia aguardando aprovação '
                             f'({brl(comissao_pendente)} de comissão a confirmar)</summary>'
                             f'{cab_vendas}{linhas_pendentes}</table></details>')
        if canceladas:
            bloco_vendas += (f'<details><summary>❌ {len(canceladas)} vendas do guia canceladas/devolvidas</summary>'
                             f'{cab_vendas}{linhas_canceladas}</table></details>')
        if descartadas:
            bloco_vendas += (f'<details><summary>🚫 Ver as {len(descartadas)} vendas de outros canais (não vieram do guia)</summary>'
                             f'<table><tr><th>Data</th><th>Produto</th><th>Valor</th><th>Comissão</th><th>Motivo</th></tr>'
                             f'{linhas_descartadas}</table></details>')
    else:
        bloco_vendas = (f'<div class="aviso">Nenhum arquivo de vendas encontrado. Para ver as <b>compras confirmadas</b> e de '
                        f'qual anúncio vieram: no painel <b>Mercado Livre Afiliados</b>, exporte o relatório de vendas/ganhos '
                        f'(CSV ou Excel) e salve em <code>{esc(PASTA_VENDAS)}</code>. Depois gere este relatório de novo.</div>')
    if avisos_vendas:
        bloco_vendas += '<div class="aviso">⚠️ ' + "<br>".join(esc(a) for a in avisos_vendas) + "</div>"

    # --- produtos clicados
    por_produto = defaultdict(Counter)
    for e in cliques:
        por_produto[e.get("produto") or "(sem nome)"][canal(e) + (" · " + e["campanha"] if e.get("campanha") else "")] += 1
    linhas_prod = "".join(
        f'<tr><td>{i}</td><td>{esc(p)}</td><td class="n"><b>{sum(c.values())}</b></td>'
        f'<td>{esc(", ".join(f"{k} ({v})" for k, v in c.most_common(3)))}</td></tr>'
        for i, (p, c) in enumerate(sorted(por_produto.items(), key=lambda kv: -sum(kv[1].values())), 1)
    ) or '<tr><td colspan="4" class="vazio">Nenhum clique ainda</td></tr>'

    # --- visitantes anônimos
    pv = defaultdict(lambda: {"prim": None, "ult": None, "visitas": 0, "cliques": 0, "e": None, "prods": []})
    for e in eventos:
        v = pv[quem(e)]
        v["prim"] = min(filter(None, [v["prim"], e["_dt"]]))
        v["ult"] = max(filter(None, [v["ult"], e["_dt"]]))
        if e["tipo"] == "visita":
            v["visitas"] += 1
            v["e"] = v["e"] or e
        else:
            v["cliques"] += 1
            if e.get("produto") and e["produto"] not in v["prods"]:
                v["prods"].append(e["produto"])
    linhas_vis = ""
    for vid, v in sorted(pv.items(), key=lambda kv: kv[1]["ult"], reverse=True)[:150]:
        e = v["e"] or {}
        agora = ' <span class="selo on">online</span>' if vid in online else ""
        if vid in compradores:
            selo_int = '<span class="selo on">💰 Compra confirmada</span>'
        else:
            cls, rot = nivel_intencao(intencao[vid][0])
            selo_int = f'<span class="selo int-{cls}">{rot}</span>' if cls else "—"
        linhas_vis += (f'<tr><td><code>#{esc(vid[-6:])}</code>{agora}</td><td>{v["ult"]:%d/%m %H:%M}</td>'
                       f'<td>{v["prim"]:%d/%m %H:%M}</td><td><b>{esc(canal(e))}</b><br><small>{esc(e.get("campanha") or tipo_trafego(e))}</small></td>'
                       f'<td>{esc(e.get("dispositivo", ""))}<br><small>{esc(e.get("sistema", ""))} · {esc(e.get("app") or e.get("navegador", ""))}</small></td>'
                       f'<td class="n">{v["visitas"]}</td><td class="n">{v["cliques"]}</td>'
                       f'<td><small>{esc("; ".join(v["prods"][:3]))}</small></td><td>{selo_int}</td></tr>')

    # --- séries
    dias = sorted({e["_dt"].date() for e in visitas})
    if dias:
        d0, d1 = dias[0], gerado.date()
        cont_dia = Counter(e["_dt"].date() for e in visitas)
        serie_dia = [(f"{d0 + timedelta(i):%d/%m}", cont_dia[d0 + timedelta(i)]) for i in range((d1 - d0).days + 1)][-45:]
    else:
        serie_dia = []
    cont_hora = Counter(e["_dt"].hour for e in visitas)
    serie_hora = [(f"{h}h", cont_hora[h]) for h in range(24)]

    tt_cont = Counter(tipo_trafego(e) for e in visitas)
    canal_cont = Counter(canal(e) for e in visitas)
    disp_cont = Counter(e.get("dispositivo") or "?" for e in visitas)
    so_cont = Counter(e.get("sistema") or "?" for e in visitas)
    app_cont = Counter(e.get("app") or "Navegador comum" for e in visitas)

    periodo = f"{min(e['_dt'] for e in eventos):%d/%m/%Y} a {gerado:%d/%m/%Y}" if eventos else "—"

    doc = f"""<!DOCTYPE html>
<html lang="pt-BR"><head><meta charset="UTF-8"><meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Acessos por Anúncio — {datetime.now():%d/%m/%Y %H:%M}</title>
<style>
body{{font-family:'Segoe UI',system-ui,-apple-system,sans-serif;background:#f8f9fa;color:#212529;margin:0;padding:24px}}
.c{{max-width:1200px;margin:0 auto}}
.header{{background:linear-gradient(135deg,#ffe600 0%,#ffd000 100%);color:#2d3277;padding:24px;border-radius:12px;margin-bottom:22px;box-shadow:0 4px 12px rgba(0,0,0,.08)}}
.header h1{{margin:0 0 8px;font-size:26px}} .header p{{margin:2px 0}}
.kpis{{display:grid;grid-template-columns:repeat(auto-fit,minmax(160px,1fr));gap:14px;margin-bottom:22px}}
.kpi{{background:#fff;border:1px solid #e0e0e0;border-radius:10px;padding:16px}}
.kpi .v{{font-size:30px;font-weight:700;color:#2d3277}} .kpi .l{{font-size:13px;color:#6c757d}}
.kpi.destaque{{border-color:#00a650}} .kpi.destaque .v{{color:#00a650}}
.card{{background:#fff;border:1px solid #e0e0e0;border-radius:10px;padding:20px;margin-bottom:22px;overflow-x:auto}}
.card h2{{margin:0 0 14px;font-size:18px;color:#2d3277}}
.grid2{{display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:22px}}
table{{width:100%;border-collapse:collapse;font-size:14px}}
th{{background:#2d3277;color:#fff;text-align:left;padding:10px;font-weight:600;white-space:nowrap}}
td{{padding:9px 10px;border-bottom:1px solid #eee;vertical-align:top}} td.n{{text-align:right;font-variant-numeric:tabular-nums}}
small{{color:#6c757d}} code{{color:#1d4ed8}}
.selo{{display:inline-block;padding:3px 9px;border-radius:10px;font-size:11px;font-weight:700;white-space:nowrap}}
.selo.pago{{background:#fde2e1;color:#9b1c1c}} .selo.etq{{background:#dbeafe;color:#1e40af}}
.selo.org{{background:#eef0f3;color:#475569}} .selo.on{{background:#d1e7dd;color:#0f5132}}
.selo.int-alta{{background:#ffedd5;color:#9a3412}} .selo.int-media{{background:#fef9c3;color:#854d0e}}
.selo.int-baixa{{background:#eef0f3;color:#475569}}
.kpi.dinheiro{{border-color:#f59e0b}} .kpi.dinheiro .v{{color:#b45309}}
.kpi.aprovada{{border:2px solid #00a650;background:#f0fbf4}} .kpi.aprovada .v{{color:#00a650;font-size:36px}}
.destaque-vendas{{border:2px solid #00a650}}
.resumo-vendas{{display:grid;grid-template-columns:repeat(auto-fit,minmax(130px,1fr));gap:10px;margin-bottom:12px}}
.resumo-vendas div{{background:#f8f9fa;border-radius:8px;padding:10px;text-align:center}}
.resumo-vendas b{{display:block;font-size:26px}} .resumo-vendas span{{font-size:12px;color:#6c757d}}
.ok{{color:#00a650}} .pend{{color:#b45309}} .canc{{color:#9b1c1c}} .fora{{color:#64748b}}
details{{margin-top:12px}} summary{{cursor:pointer;color:#2d3277;font-weight:600;padding:6px 0}}
.barra{{display:grid;grid-template-columns:minmax(110px,1.3fr) 3fr auto;gap:10px;align-items:center;margin:7px 0;font-size:14px}}
.trilho{{background:#eef0f3;border-radius:6px;height:14px;overflow:hidden}} .enche{{display:block;height:100%;border-radius:6px}}
.val{{white-space:nowrap;font-variant-numeric:tabular-nums}}
.colunas{{display:flex;align-items:flex-end;gap:3px;height:180px;padding-top:18px}}
.col{{flex:1;display:flex;flex-direction:column;justify-content:flex-end;align-items:center;height:100%;min-width:0}}
.cb{{width:100%;border-radius:4px 4px 0 0;min-height:1px}} .cv{{font-size:10px;color:#6c757d}}
.cr{{font-size:10px;color:#6c757d;margin-top:4px;white-space:nowrap;overflow:hidden;max-width:100%}}
.vazio{{color:#888;text-align:center}}
.aviso{{background:#fff8d6;border:1px solid #ffe07a;border-radius:8px;padding:12px 14px;font-size:13px;margin-bottom:22px}}
@media (max-width:600px){{body{{padding:16px}} .kpi .v{{font-size:24px}}}}
</style></head><body><div class="c">
<div class="header">
  <h1>📈 Relatório de Acessos e Vendas por Anúncio</h1>
  <p><strong>🔗 Página analisada:</strong> <a href="{esc(pagina_alvo)}" target="_blank" style="color:#2d3277">{esc(pagina_alvo)}</a></p>
  <p><strong>📅 Relatório gerado em:</strong> {datetime.now():%d/%m/%Y às %H:%M}</p>
  <p><strong>Período dos dados:</strong> {esc(periodo)}</p>
  <p><small style="color:#2d3277">Fonte: {esc(origem_dados)}{f" · {ignorados} acessos de outras páginas do site foram ignorados" if ignorados else ""}</small></p>
</div>
{'<div class="aviso">⚠️ <b>Modo demonstração</b> — dados fictícios, só para ver o formato do relatório.</div>' if origem_dados == "DEMO" else ""}
<div class="kpis">
  <div class="kpi destaque"><div class="v">{len(online)}</div><div class="l">🟢 Acessando agora (últimos 30 min)</div></div>
  <div class="kpi"><div class="v">{len(visitas)}</div><div class="l">Visitas (páginas vistas)</div></div>
  <div class="kpi"><div class="v">{len(visitantes)}</div><div class="l">Visitantes únicos</div></div>
  <div class="kpi"><div class="v">{len(vis_anuncio)}</div><div class="l">Visitas vindas de anúncio/link ({len(vis_anuncio) / len(visitas) * 100 if visitas else 0:.0f}%)</div></div>
  <div class="kpi"><div class="v">{len(cliques)}</div><div class="l">Cliques em link de afiliado</div></div>
  <div class="kpi"><div class="v">{taxa:.0f}%</div><div class="l">Visitas que clicaram em produto</div></div>
</div>
<div class="kpis">
  <div class="kpi aprovada"><div class="v">{len(validas) if vendas_todas else "—"}</div><div class="l">✅ <b>Vendas APROVADAS</b> feitas através do guia{f"<br>Comissão: <b>{brl(comissao_total)}</b> · Vendido: {brl(valor_total)}" if vendas_todas else "<br>importe o relatório de vendas do ML Afiliados"}</div></div>
  <div class="kpi"><div class="v">{len(pendentes) if vendas_todas else "—"}</div><div class="l">⏳ Vendas pendentes do guia{f"<br>{brl(comissao_pendente)} a confirmar" if pendentes else ""}</div></div>
  <div class="kpi dinheiro"><div class="v">{len(possiveis)}</div><div class="l">🔥 Possíveis compras (alta intenção, estimativa)</div></div>
</div>
{quadros_anuncios(anuncios)}

<div class="card"><h2>🎯 Desempenho por anúncio / origem</h2>
<table><tr><th>Tipo</th><th>Canal</th><th>Campanha / Anúncio</th><th>Visitas</th><th>Visitantes</th><th>Cliques</th><th>Taxa de clique</th><th>Possíveis compras</th><th>Vendas aprovadas</th><th>Comissão aprovada</th></tr>
{linhas_anuncio or '<tr><td colspan="10" class="vazio">Sem dados</td></tr>'}</table></div>

<div class="card destaque-vendas"><h2>✅ Vendas aprovadas e efetuadas através de {esc(pagina_alvo)}</h2>
{bloco_vendas}</div>

<div class="card"><h2>🔥 Possíveis compras — visitantes com alta intenção (estimativa)</h2>
<p><small>O blog não vê o que acontece dentro do Mercado Livre. Esta lista é uma <b>estimativa</b> baseada no comportamento:
clicar no produto (+40), clicar de novo no mesmo produto (+20), voltar outro momento e clicar (+20), sair do blog direto
para o ML (+10), focar em um só produto (+10). A partir de 70 pontos = possível compra.</small></p>
<table><tr><th>Visitante</th><th>Último clique</th><th>Produto(s)</th><th>Veio de</th><th>Pontos</th><th>Motivos</th></tr>
{linhas_possiveis or '<tr><td colspan="6" class="vazio">Nenhum visitante com alta intenção no período</td></tr>'}</table></div>

<div class="grid2">
  <div class="card"><h2>De onde vêm as visitas</h2>{barras(tt_cont, cor="#2d3277")}</div>
  <div class="card"><h2>Canal</h2>{barras(canal_cont)}</div>
</div>

<div class="card"><h2>🛒 Produtos mais clicados (links meli.la)</h2>
<table><tr><th>#</th><th>Produto</th><th>Cliques</th><th>Principais origens</th></tr>{linhas_prod}</table></div>

<div class="card"><h2>📅 Visitas por dia</h2>{colunas(serie_dia) if serie_dia else '<p class="vazio">Sem dados</p>'}</div>
<div class="card"><h2>🕒 Visitas por horário</h2>{colunas(serie_hora, "#00a650")}</div>

<div class="grid2">
  <div class="card"><h2>Dispositivo</h2>{barras(disp_cont, cor="#00a650")}</div>
  <div class="card"><h2>Sistema</h2>{barras(so_cont, cor="#00a650")}</div>
  <div class="card"><h2>Aberto dentro do app</h2>{barras(app_cont, cor="#00a650")}</div>
</div>

<div class="card"><h2>👤 Visitantes (anônimos) — mais recentes primeiro</h2>
<p><small>Cada visitante recebe um código aleatório no navegador dele. Não há nome, e-mail nem IP guardado (LGPD).</small></p>
<table><tr><th>Visitante</th><th>Último acesso</th><th>1º acesso</th><th>Veio de</th><th>Aparelho</th><th>Visitas</th><th>Cliques</th><th>Produtos clicados</th><th>Intenção de compra</th></tr>
{linhas_vis or '<tr><td colspan="9" class="vazio">Sem dados</td></tr>'}</table></div>
</div></body></html>"""

    # Data/hora da geração no nome: cada execução gera um arquivo novo (histórico)
    sufixo = datetime.now().strftime("_%Y-%m-%d_%Hh%M") + ("_DEMO" if origem_dados == "DEMO" else "")
    saida = SAIDA_HTML.replace(".html", f"{sufixo}.html")
    os.makedirs(PASTA_SAIDA_HTML, exist_ok=True)
    with open(saida, "w", encoding="utf-8") as f:
        f.write(doc)
    return {"visitas": len(visitas), "visitantes": len(visitantes), "cliques": len(cliques),
            "anuncio": len(vis_anuncio), "online": len(online), "saida": saida,
            "possiveis": len(possiveis), "vendas": vendas, "validas": len(validas), "comissao": comissao_total,
            "vendas_todas": vendas_todas, "descartadas": len(descartadas), "ignorados": ignorados,
            "pendentes": len(pendentes), "canceladas": len(canceladas), "comissao_pendente": comissao_pendente}


def salvar_compras(vendas, pagina_alvo=PAGINA_PADRAO):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    caminho = os.path.join(PASTA_DADOS, datetime.now().strftime("compras_atribuidas_%Y%m%d_%H%M.csv"))
    with open(caminho, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["data_venda", "produto", "efetuada_por", "valor", "comissao", "status", "confianca", "canal", "campanha",
                    "conteudo", "visitante", "data_clique", "produto_clicado", "arquivo", "da_pagina_5_2", "motivo",
                    "situacao"])
        for v in vendas:
            c = v["clique"] or {}
            if not v.get("prova"):
                efetuada = "outro canal (não foi pelo guia)"
            elif v.get("situacao") == "aprovada":
                efetuada = f"Efetuada pelo {pagina_alvo}"
            else:
                efetuada = f"Feita pelo {pagina_alvo} ({v.get('situacao')})"
            w.writerow([v["dt"].strftime("%d/%m/%Y %H:%M"), v["produto"], efetuada, v["valor"], v["comissao"], v["status"],
                        v["confianca"], canal(c) if c else "", c.get("campanha", ""), c.get("conteudo", ""),
                        quem(c) if c else "", c["_dt"].strftime("%d/%m/%Y %H:%M") if c else "",
                        c.get("produto", ""), v["arquivo"], "sim" if v.get("prova") else "nao",
                        v.get("prova") or v.get("motivo", ""), v.get("situacao", "")])
    return caminho


def salvar_copia(dados):
    os.makedirs(PASTA_DADOS, exist_ok=True)
    carimbo = datetime.now().strftime("%Y%m%d_%H%M")
    caminho_json = os.path.join(PASTA_DADOS, f"acessos_{carimbo}.json")
    with open(caminho_json, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False)
    campos = ["id", "criado_em", "tipo", "visitante", "sessao", "pagina", "origem", "meio", "campanha",
              "conteudo", "referencia", "app", "dispositivo", "sistema", "navegador", "produto", "link"]
    caminho_csv = os.path.join(PASTA_DADOS, f"acessos_{carimbo}.csv")
    with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=campos, delimiter=";", extrasaction="ignore")
        w.writeheader()
        w.writerows(dados.get("eventos", []))
    return caminho_csv


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Relatório de acessos ao blog por anúncio")
    ap.add_argument("--dias", type=int, default=30)
    ap.add_argument("--demo", action="store_true", help="usa dados fictícios")
    ap.add_argument("--arquivo", help="gera a partir de um JSON salvo antes")
    ap.add_argument("--vendas", help="arquivo ou pasta com o relatório de vendas do ML Afiliados (CSV/XLSX)")
    ap.add_argument("--verificar-anuncios", action="store_true",
                    help="verifica agora no ML se os anúncios do guia estão ativos (mesmo com verificação recente)")
    ap.add_argument("--sem-verificar-anuncios", action="store_true",
                    help="não verifica no ML; usa a última verificação gravada")
    args = ap.parse_args()

    cfg = {}
    if os.path.exists(CONFIG):
        with open(CONFIG, encoding="utf-8") as f:
            cfg = json.load(f)
    cfg.setdefault("site", SITE_PADRAO)
    pagina_alvo = cfg.get("pagina_blog") or PAGINA_PADRAO
    PAGINAS_ANTIGAS[:] = cfg.get("paginas_antigas", PAGINAS_ANTIGAS)
    janela = int(cfg.get("janela_compra_horas", JANELA_COMPRA_HORAS))

    print("=" * 65)
    print("🚀 RELATÓRIO DE ACESSOS E VENDAS POR ANÚNCIO")
    print(f"🔗 Página analisada: {pagina_alvo}")
    print("=" * 65)

    if args.demo:
        dados, fonte = dados_demo(args.dias), "DEMO"
    elif args.arquivo:
        with open(args.arquivo, encoding="utf-8") as f:
            dados, fonte = json.load(f), args.arquivo
    else:
        if not os.path.exists(CONFIG):
            raise SystemExit(f"❌ Não encontrei o config_rastreio.json ({CONFIG}).")
        if cfg["chave"].startswith("TROQUE"):
            raise SystemExit("❌ Defina a 'chave' em config_rastreio.json (a mesma do snippet do WordPress).")
        print(f"🌐 Baixando dados de {cfg['site']} (últimos {args.dias} dias)...")
        dados, fonte = baixar_dados(cfg, args.dias), cfg["site"]
        print(f"💾 Cópia salva em: {salvar_copia(dados)}")

    vendas, avisos = [], []
    if not args.demo:
        origem_vendas = args.vendas or cfg.get("pasta_vendas") or PASTA_VENDAS
        vendas, avisos = carregar_vendas(origem_vendas, cfg.get("colunas_vendas"))
        print(f"💰 Vendas lidas de {origem_vendas}: {len(vendas)}")
        for a in avisos:
            print(f"   ⚠️ {a}")

    codigos = None
    if vendas:
        da_pagina, _ = filtrar_pagina(dados.get("eventos", []), pagina_alvo)
        codigos = links_do_blog(cfg, [e for e in da_pagina if e.get("tipo") == "clique"], pagina_alvo)
        print(f"🔗 Links meli.la da página do guia: {len(codigos)}")

    if not args.demo and not args.sem_verificar_anuncios and (args.verificar_anuncios or verificacao_antiga()):
        print(f"🔎 Verificando no ML se os anúncios do guia estão ativos (a última verificação tem mais de "
              f"{HORAS_VERIFICACAO} h; leva alguns minutos)...")
        verificar_anuncios_agora()
    anuncios = situacao_anuncios()
    r = gerar(dados, fonte, vendas, avisos, janela, demo_vendas=args.demo,
              codigos_blog=codigos, etiqueta=cfg.get("etiqueta_afiliado", ""), pagina_alvo=pagina_alvo,
              anuncios=anuncios)
    if anuncios:
        print(f"📉 Anúncios fora do ar ...... {len(anuncios['pendentes'])} precisam de substituto · "
              f"{len(anuncios['trocados'])} já substituído(s) (últimos {anuncios['dias']} dias)")
    if r["ignorados"]:
        print(f"↪️  Acessos de outras páginas ignorados: {r['ignorados']}")
    print(f"🟢 Acessando agora ......... {r['online']}")
    print(f"👁  Visitas ................. {r['visitas']}")
    print(f"👤 Visitantes únicos ....... {r['visitantes']}")
    print(f"🎯 Vindas de anúncio/link .. {r['anuncio']}")
    print(f"🛒 Cliques em afiliado ..... {r['cliques']}")
    print(f"🔥 Possíveis compras ....... {r['possiveis']}  (estimativa)")
    if r["vendas_todas"]:
        print(f"✅ VENDAS APROVADAS guia ... {r['validas']}  ({brl(r['comissao'])} de comissão)")
        print(f"⏳ Pendentes guia .......... {r['pendentes']}  ({brl(r['comissao_pendente'])} a confirmar)")
        print(f"❌ Canceladas guia ......... {r['canceladas']}")
        print(f"🚫 Vendas de outros canais . {r['descartadas']}  (não entram nos totais)")
        if not args.demo:
            print(f"💾 Compras atribuídas: {salvar_compras(r['vendas_todas'], pagina_alvo)}")
    print("=" * 65)
    print(f"✅ Relatório: {r['saida']}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code not in (None, 0):
            print(e.code)
    finally:
        if getattr(sys, "frozen", False):  # duplo clique no .exe: não fechar a janela sozinho
            input("\nPressione ENTER para fechar...")
