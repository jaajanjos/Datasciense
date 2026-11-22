# -*- coding: utf-8 -*-
r"""LEITURA_ANUNCIO_META.py - acompanhamento diario do anuncio Meta (Facebook/Instagram).

PARA QUE SERVE: no momento em que roda, busca na Meta (API oficial de Marketing, so leitura)
os numeros atuais da campanha, grava uma linha nova no historico CSV e gera o PDF do dia.

Uso:
  python -X utf8 LEITURA_ANUNCIO_META.py                 (busca na Meta + grava CSV + gera PDF)
  python -X utf8 LEITURA_ANUNCIO_META.py --sem-meta      (nao busca; so gera o PDF com o CSV atual)
  python -X utf8 LEITURA_ANUNCIO_META.py --campanha 1234567890   (outra campanha, sem mexer na config)
  python -X utf8 LEITURA_ANUNCIO_META.py --csv "caminho.csv"     (usar outro historico)

Configuracao: LEITURA_ANUNCIO_META_config.json (mesma pasta deste programa).
  access_token  -> chave de leitura da Meta (permissao ads_read). E SECRETA: nao enviar a ninguem.
  campaign_id   -> numero da campanha (Gerenciador de Anuncios, coluna/URL da campanha).
  orcamento     -> 0 = pegar a verba da propria Meta; ou um valor fixo em reais (ex.: 240).
  acao_resultado-> o que conta como "resultado" (padrao landing_page_view = visualizacao da pagina).
  api_version   -> versao da API (padrao v24.0).

Saidas (pasta 0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog):
  LEITURA_ANUNCIO_META_historico_<campaign_id>.csv  (historico da campanha; 1 linha por execucao)
  LEITURA_ANUNCIO_META_DD_MM_AAAA_HHhMM_DIARIO.pdf
Colunas do CSV: data;hora;gasto;impressoes;alcance;resultados;status;observacao (gasto com ponto decimal)
"""
import argparse, csv, datetime, json, os, sys, urllib.error, urllib.parse, urllib.request

AQUI = os.path.dirname(os.path.abspath(__file__))
PASTA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
CONFIG = os.path.join(AQUI, "LEITURA_ANUNCIO_META_config.json")
CSV_TESTE = os.path.join(PASTA, "LEITURA_ANUNCIO_META_historico.csv")   # campanha de teste (R$ 50, 11-16/11)
CABECALHO = ["data", "hora", "gasto", "impressoes", "alcance", "resultados", "status", "observacao"]
STATUS_PT = {"ACTIVE": "Ativo", "PAUSED": "Pausado", "CAMPAIGN_PAUSED": "Pausado", "ADSET_PAUSED": "Pausado",
             "DELETED": "Excluido", "ARCHIVED": "Arquivado", "IN_PROCESS": "Em analise", "WITH_ISSUES": "Com problema",
             "PENDING_REVIEW": "Em analise", "DISAPPROVED": "Reprovado", "COMPLETED": "Concluido"}


def reais(x):
    return f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def ler_config():
    if not os.path.exists(CONFIG):
        sys.exit(f"ERRO: falta o arquivo de configuracao:\n  {CONFIG}\n"
                 "Crie o arquivo com access_token, campaign_id, orcamento, acao_resultado e api_version.")
    with open(CONFIG, encoding="utf-8-sig") as fh:
        cfg = json.load(fh)
    cfg.setdefault("api_version", "v24.0")
    cfg.setdefault("acao_resultado", "landing_page_view")
    cfg.setdefault("orcamento", 0)
    return cfg


# ---------------------------------------------------------------- Meta (somente leitura)
def chamar_api(versao, caminho, params, token):
    params = dict(params, access_token=token)
    url = f"https://graph.facebook.com/{versao}/{caminho}?" + urllib.parse.urlencode(params)
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            return json.load(resp)
    except urllib.error.HTTPError as e:
        try:
            err = json.load(e).get("error", {})
        except Exception:
            err = {}
        cod, msg = err.get("code"), err.get("message", str(e))
        dica = {190: "a chave (access_token) venceu ou esta errada; gere outra e troque na config.",
                200: "a chave nao tem a permissao ads_read para esta conta de anuncios.",
                10: "a chave nao tem a permissao ads_read para esta conta de anuncios.",
                100: "o numero da campanha (campaign_id) esta errado ou a chave nao enxerga essa campanha.",
                17: "limite de consultas da Meta atingido; espere alguns minutos e rode de novo.",
                4: "limite de consultas da Meta atingido; espere alguns minutos e rode de novo."}.get(cod, "")
        sys.exit(f"ERRO na Meta (codigo {cod}): {msg}\n{('O que fazer: ' + dica) if dica else ''}")
    except urllib.error.URLError as e:
        sys.exit(f"ERRO: sem conexao com a Meta ({e.reason}). Confira a internet e rode de novo.")


def verba_total(camp, conjuntos, cfg):
    """Verba em reais: config fixa > verba vitalicia > diaria x dias. Valores da Meta vem em centavos."""
    if float(cfg.get("orcamento") or 0) > 0:
        return float(cfg["orcamento"]), "definida na configuracao"
    fontes = [camp] if (camp.get("lifetime_budget") or camp.get("daily_budget")) else conjuntos
    vitalicio = sum(int(x.get("lifetime_budget") or 0) for x in fontes)
    if vitalicio:
        return vitalicio / 100, "vitalício (Meta)"
    diario = sum(int(x.get("daily_budget") or 0) for x in fontes)
    ini, fim = camp.get("start_time"), camp.get("stop_time")
    if diario and ini and fim:
        dias = max(1, (datetime.datetime.fromisoformat(fim[:10]) - datetime.datetime.fromisoformat(ini[:10])).days)
        return diario / 100 * dias, f"diario {reais(diario / 100)} x {dias} dias (Meta)"
    if diario:
        return None, f"diario {reais(diario / 100)} sem data de fim (Meta)"
    return None, "nao informada"


def buscar_meta(cfg):
    v, tk, cid = cfg["api_version"], cfg["access_token"], str(cfg["campaign_id"])
    camp = chamar_api(v, cid, {"fields": "name,effective_status,lifetime_budget,daily_budget,start_time,stop_time"}, tk)
    conj = chamar_api(v, f"{cid}/adsets", {"fields": "lifetime_budget,daily_budget", "limit": 100}, tk).get("data", [])
    ins = chamar_api(v, f"{cid}/insights", {"date_preset": "maximum",
                     "fields": "spend,impressions,reach,frequency,inline_link_clicks,ctr,cpm,actions"}, tk).get("data", [])
    i = ins[0] if ins else {}
    acoes = {a.get("action_type"): float(a.get("value", 0)) for a in i.get("actions", [])}
    resultados = int(acoes.get(cfg["acao_resultado"], 0))
    verba, origem = verba_total(camp, conj, cfg)
    status = STATUS_PT.get(camp.get("effective_status", ""), camp.get("effective_status", "?"))
    fim = camp.get("stop_time")
    if fim and status == "Ativo" and datetime.datetime.fromisoformat(fim[:10]).date() < datetime.date.today():
        status = "Concluido"
    obs = [f"Automatico (API Meta)",
           f"cliques no link {i.get('inline_link_clicks', '0')}",
           f"CTR {float(i.get('ctr', 0)):.2f}%".replace(".", ","),
           f"CPM {reais(float(i.get('cpm', 0)))}",
           f"frequencia {float(i.get('frequency', 0)):.2f}".replace(".", ",")]
    if fim:
        obs.append(f"termina {fim[8:10]}/{fim[5:7]}/{fim[:4]}")
    return {"nome": camp.get("name", cid), "verba": verba, "origem_verba": origem,
            "gasto": float(i.get("spend", 0)), "impressoes": int(i.get("impressions", 0) or 0),
            "alcance": int(i.get("reach", 0) or 0), "resultados": resultados, "status": status,
            "observacao": ", ".join(obs)}


# ---------------------------------------------------------------- historico CSV
def ler_historico(caminho):
    """Le o CSV tolerando linhas vazias e ';' dentro da observacao."""
    linhas = []
    if not os.path.exists(caminho):
        return linhas
    with open(caminho, encoding="utf-8-sig", newline="") as fh:
        for n, campos in enumerate(csv.reader(fh, delimiter=";")):
            if n == 0 or not any(c.strip() for c in campos):
                continue
            campos += [""] * (8 - len(campos))
            obs = "; ".join(c for c in campos[7:] if c.strip())
            try:
                linhas.append({"data": campos[0], "hora": campos[1], "gasto": float(campos[2].replace(",", ".")),
                               "impressoes": campos[3], "alcance": campos[4], "resultados": int(float(campos[5] or 0)),
                               "status": campos[6], "observacao": obs})
            except ValueError:
                print(f"AVISO: linha {n + 1} do CSV ignorada (numero invalido): {';'.join(campos[:8])}")
    return linhas


def gravar_linha(caminho, agora, d):
    novo = not os.path.exists(caminho)
    with open(caminho, "a", encoding="utf-8-sig" if novo else "utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter=";")
        if novo:
            w.writerow(CABECALHO)
        w.writerow([f"{agora:%d/%m/%Y}", f"{agora:%Hh%M}", f"{d['gasto']:.2f}", d["impressoes"], d["alcance"],
                    d["resultados"], d["status"], d["observacao"].replace(";", ",")])


# ---------------------------------------------------------------- PDF
def gerar_pdf(linhas, nome, verba, origem_verba, pasta_saida, agora):
    from reportlab.lib.pagesizes import A4, landscape
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import cm
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    if not linhas:
        sys.exit("ERRO: o historico esta vazio; nao ha o que colocar no PDF.")
    saida = os.path.join(pasta_saida, f"LEITURA_ANUNCIO_META_{agora:%d_%m_%Y_%Hh%M}_DIARIO.pdf")
    s = getSampleStyleSheet()
    h = ParagraphStyle("h", parent=s["Title"], fontSize=17)
    h2 = ParagraphStyle("h2", parent=s["Heading2"], fontSize=12, spaceBefore=10)
    p = ParagraphStyle("p", parent=s["BodyText"], fontSize=10, leading=14)
    c = ParagraphStyle("c", parent=s["BodyText"], fontSize=7.5, leading=9)
    doc = SimpleDocTemplate(saida, pagesize=landscape(A4), leftMargin=1.5*cm, rightMargin=1.5*cm,
                            topMargin=1.5*cm, bottomMargin=1.5*cm, title="Acompanhamento diario do anuncio Meta")
    pct = lambda g: f"{g / verba * 100:.1f}%" if verba else "-"
    dados = [["Data", "Hora", "Gasto", "% da verba", "Impressões", "Alcance", "Visualiz. da página",
              "Custo/visualiz.", "Status", "Observação"]]
    for l in linhas:
        g, r = l["gasto"], l["resultados"]
        dados.append([l["data"], l["hora"], reais(g), pct(g), l["impressoes"], l["alcance"], str(r),
                      reais(g / r) if r else "-", l["status"], Paragraph(l["observacao"], c)])
    t = Table(dados, repeatRows=1, colWidths=[2*cm, 1.4*cm, 2*cm, 1.8*cm, 1.9*cm, 1.7*cm, 2.8*cm, 2.3*cm, 1.8*cm, 9*cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f2937")),
                           ("TEXTCOLOR", (0, 0), (-1, 0), colors.white), ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
                           ("FONTSIZE", (0, 0), (-1, -1), 8), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f3f4f6")]),
                           ("PADDING", (0, 0), (-1, -1), 3)]))
    u = linhas[-1]
    g, r = u["gasto"], u["resultados"]
    verba_txt = f"{reais(verba)} – {origem_verba}" if verba else f"não informada – {origem_verba}"
    situacao = f"Gasto: <b>{reais(g)}</b>"
    if verba:
        situacao += f" de {reais(verba)} (<b>{pct(g)}</b>) · saldo restante: <b>{reais(max(verba - g, 0))}</b>"
    situacao += f" · {r} visualizações da página" + (f" · custo por visualização {reais(g / r)}" if r else "") + "."
    e = [Paragraph(f"Acompanhamento diário do anúncio Meta – {nome}", h),
         Paragraph(f"Gerado em {agora:%d/%m/%Y às %Hh%M}. Verba total: {verba_txt}. "
                   f"Última leitura: {u['data']} {u['hora']} · status {u['status']}.", p),
         Paragraph("Situação atual", h2), Paragraph(situacao, p),
         Paragraph("Dia a dia (acumulado)", h2), t, Spacer(1, 8),
         Paragraph("Observação: o custo por visualização usa as visualizações da página que a Meta conta "
                   "(cliques em 7 dias ou visualização em 1 dia); confirmar as visitas reais no Google Analytics "
                   "(utm do anúncio).", p)]
    doc.build(e)
    return saida


def main(argv=None):
    ap = argparse.ArgumentParser(description="Le o anuncio na Meta e gera o PDF diario.")
    ap.add_argument("--sem-meta", action="store_true", help="nao busca na Meta; so gera o PDF com o CSV")
    ap.add_argument("--campanha", help="numero da campanha (substitui o da config nesta execucao)")
    ap.add_argument("--csv", help="caminho do historico CSV")
    ap.add_argument("--pasta-saida", default=PASTA, help="pasta do PDF (padrao: 4_Relatorio_Ativ_Claude_no_Blog)")
    a = ap.parse_args(argv)
    agora = datetime.datetime.now()

    if a.sem_meta:
        cfg = {}
        if os.path.exists(CONFIG):
            with open(CONFIG, encoding="utf-8-sig") as fh:
                cfg = json.load(fh)
        cid = a.campanha or str(cfg.get("campaign_id") or "")
        csv_path = a.csv or (os.path.join(PASTA, f"LEITURA_ANUNCIO_META_historico_{cid}.csv") if cid else CSV_TESTE)
        if not os.path.exists(csv_path):
            csv_path = CSV_TESTE
        if csv_path == CSV_TESTE:
            nome, verba, origem = "teste_11a13_11_anuncio", 50.0, "teste encerrado"
        else:
            nome = cfg.get("nome_campanha") or f"campanha {cid}"
            verba = float(cfg.get("orcamento") or 0) or None
            origem = "definida na configuracao" if verba else "sem leitura da Meta"
        linhas = ler_historico(csv_path)
    else:
        cfg = ler_config()
        if a.campanha:
            cfg["campaign_id"] = a.campanha
        if not cfg.get("access_token") or "COLE_AQUI" in cfg["access_token"] or not str(cfg.get("campaign_id", "")).isdigit():
            sys.exit(f"ERRO: preencha access_token e campaign_id em\n  {CONFIG}")
        print("Buscando os dados atuais na Meta...")
        d = buscar_meta(cfg)
        csv_path = a.csv or os.path.join(PASTA, f"LEITURA_ANUNCIO_META_historico_{cfg['campaign_id']}.csv")
        gravar_linha(csv_path, agora, d)
        print(f"Linha gravada em: {csv_path}")
        print(f"  {d['nome']}: gasto {reais(d['gasto'])}, impressoes {d['impressoes']}, alcance {d['alcance']}, "
              f"resultados {d['resultados']}, status {d['status']}")
        nome, verba, origem = d["nome"], d["verba"], d["origem_verba"]
        linhas = ler_historico(csv_path)

    saida = gerar_pdf(linhas, nome, verba, origem, a.pasta_saida, agora)
    print(f"PDF gerado: {saida}")
    return saida


if __name__ == "__main__":
    main()
