# -*- coding: utf-8 -*-
r"""GERA_GRAFICO_ANUNCIO_META.py  (criado em 21/11/2026; versão 2 de 21/11/2026, a pedido do dono)

PARA QUE SERVE: no momento em que roda, busca os números ATUAIS do anúncio na Meta e as visitas ATUAIS
do blog, atualiza os dados gerenciais e gera o gráfico de 4 quadros (mesmo modelo do de 16/11):
  1) Gasto acumulado por dia, com a verba total (linha tracejada)
  2) Por dia: visualizações da página contadas pela Meta x visitas reais do blog
  3) Meta (visualizações) x blog (visitas reais), total
  4) Custo por visita real, custo por visualização da Meta e a meta de custo

O QUE ELE FAZ, NESTA ORDEM (tudo só leitura na Meta e no site; não muda anúncio, verba nem limite):
  1. Meta (API oficial de Marketing, permissão ads_read): totais da campanha + números de cada dia.
     Usa a chave e os dados de LEITURA_ANUNCIO_META_config.json (o mesmo arquivo do LEITURA_ANUNCIO_META.py).
     Se o campaign_id estiver vazio, procura a campanha pelo nome (nome_campanha) na conta ad_account_id
     e grava o número encontrado na config.
  2. Blog: baixa agora os acessos do rastreador do site (o mesmo do painel de acessos) e salva a cópia
     acessos_AAAAMMDD_HHMM.csv em Relatorios_Diarios_Anuncios\dados_acessos.
  3. Dados gerenciais (pasta 0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog):
     - LEITURA_ANUNCIO_META_historico_<campaign_id>.csv  -> 1 linha por execução (mesmo formato do LEITURA_ANUNCIO_META.py)
     - DADOS_GERENCIAIS_ANUNCIO_META_<nome>.csv          -> 1 linha por dia (Meta + blog), refeita a cada execução
     - RESUMO_GERENCIAL_ANUNCIO_META_<nome>.csv          -> 1 linha por execução com os indicadores e o critério
  4. Gráfico GRAFICO_ANUNCIO_META_DD_MM_AAAA_HHhMM.png na mesma pasta. A versão anterior vai para old_bkp
     (fica só 1 versão na pasta).

Se a Meta não responder (chave vazia/vencida, sem internet), o programa AVISA, usa a última leitura gravada
e continua com as visitas do blog. Se o site não responder, usa o arquivo de acessos mais novo da pasta.

USO (funciona de qualquer pasta):
  python -X utf8 "D:\Projeto_Blog_Comprenolink\Programas_Diversos_Py\GERA_GRAFICO_ANUNCIO_META.py"
      -> anúncio atual (bf_26_entrada), dados do momento
  ... GERA_GRAFICO_ANUNCIO_META.py --sem-baixar   -> não busca nada; só refaz com os dados já gravados
  ... GERA_GRAFICO_ANUNCIO_META.py --teste        -> refaz o gráfico do teste de 11 a 13/11 (dados antigos)
  ... GERA_GRAFICO_ANUNCIO_META.py --meta-manual LEITURA_META_MANUAL.json
      -> sem a chave da API: usa a leitura feita no Gerenciador (gravada nesse JSON)
  Outras opções: --campanha NUMERO  --utm NOME  --verba 240  --meta-custo 0.35  --dias 60  --saida PASTA
"""
import argparse
import csv
import datetime as dt
import glob
import importlib.util
import json
import os
import shutil
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

plt.rcParams["text.parse_math"] = False

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import LEITURA_ANUNCIO_META as LM  # noqa: E402  (mesma pasta: leitura oficial da Meta e histórico)

PASTA_REL = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog"
PASTA_ACESSOS = r"D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\dados_acessos"
PROG_ACESSOS = r"D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\programas_fontes_python\3_relatorio_acessos_anuncios.py"
CSV_TESTE = os.path.join(PASTA_REL, "LEITURA_ANUNCIO_META_historico.csv")

AZUL, VERDE, CINZA, VERMELHO = "#2563eb", "#16a34a", "#9ca3af", "#dc2626"
COL_DIA = ["data", "gasto_dia", "gasto_acumulado", "impressoes", "alcance", "frequencia", "cliques_link",
           "resultados_meta", "visitas_reais", "visitantes_unicos", "cliques_saida", "custo_por_visita_dia"]
COL_RESUMO = ["data", "hora", "fonte_meta", "status", "verba", "gasto", "pct_verba", "saldo", "resultados_meta",
              "visitas_reais", "visitantes_unicos", "cliques_saida", "taxa_saida_pct", "custo_por_visita",
              "custo_por_clique_saida", "criterio", "arquivo_acessos"]


def reais(x):
    return LM.reais(x)


def num(v, tipo=float):
    try:
        return tipo(float(str(v).replace(",", ".")))
    except (TypeError, ValueError):
        return tipo(0)


# ---------------------------------------------------------------- 1. Meta
def achar_campanha(cfg):
    """Procura o número da campanha pelo nome, na conta de anúncios. Devolve o id ou None."""
    conta, nome = str(cfg.get("ad_account_id") or "").replace("act_", ""), cfg.get("nome_campanha")
    if not conta or not nome:
        return None
    filtro = json.dumps([{"field": "name", "operator": "EQUAL", "value": nome}])
    r = LM.chamar_api(cfg["api_version"], f"act_{conta}/campaigns",
                      {"fields": "id,name", "filtering": filtro, "limit": 10}, cfg["access_token"])
    achadas = r.get("data", [])
    return achadas[0]["id"] if achadas else None


def meta_por_dia(cfg):
    """Números de cada dia da campanha (insights com time_increment=1)."""
    r = LM.chamar_api(cfg["api_version"], f"{cfg['campaign_id']}/insights",
                      {"date_preset": "maximum", "time_increment": 1, "limit": 200,
                       "fields": "spend,impressions,reach,frequency,inline_link_clicks,actions"}, cfg["access_token"])
    dias = {}
    for i in r.get("data", []):
        acoes = {a.get("action_type"): float(a.get("value", 0)) for a in i.get("actions", [])}
        d = dt.datetime.strptime(i["date_start"], "%Y-%m-%d").date()
        dias[d] = {"gasto_dia": num(i.get("spend")), "impressoes": num(i.get("impressions"), int),
                   "alcance": num(i.get("reach"), int), "frequencia": num(i.get("frequency")),
                   "cliques_link": num(i.get("inline_link_clicks"), int),
                   "resultados_meta": int(acoes.get(cfg["acao_resultado"], 0))}
    return dias


def buscar_meta_agora(cfg, agora):
    """Lê a Meta agora. Devolve (totais, por_dia, aviso). Em erro: (None, {}, motivo) sem parar o programa."""
    tk = str(cfg.get("access_token") or "")
    if not tk or "COLE_AQUI" in tk:
        return None, {}, ("a chave da Meta (access_token) está vazia em LEITURA_ANUNCIO_META_config.json. "
                          "Sem ela o programa não consegue ler a Meta sozinho.")
    try:
        if not str(cfg.get("campaign_id", "")).isdigit():
            cid = achar_campanha(cfg)
            if not cid:
                return None, {}, f"não achei a campanha '{cfg.get('nome_campanha')}' na conta {cfg.get('ad_account_id')}."
            cfg["campaign_id"] = cid
            salvar_campaign_id(cid)
            print(f"Campanha encontrada pelo nome: {cfg.get('nome_campanha')} = {cid} (gravado na config)")
        totais = LM.buscar_meta(cfg)
        por_dia = meta_por_dia(cfg)
    except SystemExit as e:  # LM.chamar_api avisa e sai; aqui só avisamos e seguimos
        return None, {}, str(e)
    hist = os.path.join(PASTA_REL, f"LEITURA_ANUNCIO_META_historico_{cfg['campaign_id']}.csv")
    LM.gravar_linha(hist, agora, totais)
    print(f"Meta OK: gasto {reais(totais['gasto'])}, {totais['resultados']} visualizações, status {totais['status']}")
    print(f"Linha gravada em: {hist}")
    return totais, por_dia, ""


def salvar_campaign_id(cid):
    with open(LM.CONFIG, encoding="utf-8-sig") as fh:
        c = json.load(fh)
    c["campaign_id"] = str(cid)
    with open(LM.CONFIG, "w", encoding="utf-8") as fh:
        json.dump(c, fh, ensure_ascii=False, indent=2)


def ler_meta_manual(caminho):
    """Leitura feita à mão no Gerenciador (JSON): totais + dias. Mesmo formato que a API devolve."""
    with open(caminho, encoding="utf-8-sig") as fh:
        m = json.load(fh)
    totais = {"gasto": float(m["gasto"]), "impressoes": int(m["impressoes"]), "alcance": int(m["alcance"]),
              "resultados": int(m["resultados"]), "status": m.get("status", "Ativo"), "verba": m.get("verba"),
              "origem_verba": "leitura manual", "observacao": m.get("observacao", "Leitura manual no Gerenciador")}
    dias = {}
    for d, v in m.get("dias", {}).items():
        dias[dt.datetime.strptime(d, "%d/%m/%Y").date()] = {
            "gasto_dia": float(v["gasto_dia"]), "impressoes": int(v["impressoes"]), "alcance": int(v["alcance"]),
            "frequencia": round(v["impressoes"] / v["alcance"], 2) if v["alcance"] else 0,
            "cliques_link": v.get("cliques_link", 0), "resultados_meta": int(v["resultados"])}
    return totais, dias


# ---------------------------------------------------------------- 2. blog
def baixar_acessos(dias):
    """Baixa agora os acessos do rastreador do site; devolve o caminho do CSV novo ou None (com aviso)."""
    try:
        spec = importlib.util.spec_from_file_location("relatorio_acessos", PROG_ACESSOS)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        with open(mod.CONFIG, encoding="utf-8") as fh:
            cfg = json.load(fh)
        cfg.setdefault("site", mod.SITE_PADRAO)
        dados = mod.baixar_dados(cfg, dias)
        caminho = mod.salvar_copia(dados)
        print(f"Blog OK: {len(dados.get('eventos', []))} eventos baixados -> {caminho}")
        return caminho
    except (Exception, SystemExit) as e:
        print(f"AVISO: não consegui baixar os acessos do blog agora ({e}). Vou usar o arquivo mais novo da pasta.")
        return None


def visitas_por_dia(caminho, campanha):
    """Por dia (Brasília = horário do arquivo - 3 h): sessões (visitas), visitantes únicos e cliques de saída."""
    dias = {}
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        for l in csv.DictReader(f, delimiter=";"):
            if l.get("campanha") != campanha:
                continue
            t = dt.datetime.strptime(l["criado_em"], "%Y-%m-%d %H:%M:%S") - dt.timedelta(hours=3)
            x = dias.setdefault(t.date(), {"sess": set(), "vis": set(), "cli": 0})
            if l.get("tipo") == "visita":
                x["sess"].add(l["sessao"])
                x["vis"].add(l["visitante"])
            elif l.get("tipo") == "clique":
                x["cli"] += 1
    return dict(sorted(dias.items()))


# ---------------------------------------------------------------- 3. dados gerenciais
def ler_csv(caminho):
    if not os.path.exists(caminho):
        return []
    with open(caminho, encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter=";"))


def gravar_csv(caminho, colunas, linhas, acrescentar=False):
    novo = not os.path.exists(caminho) or not acrescentar
    with open(caminho, "w" if novo else "a", encoding="utf-8-sig" if novo else "utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=colunas, delimiter=";", extrasaction="ignore")
        if novo:
            w.writeheader()
        w.writerows(linhas)


def atualizar_por_dia(caminho, meta_dia, site_dia):
    """Junta o que já estava gravado + Meta de hoje + blog de hoje. A Meta antiga fica se a Meta não respondeu."""
    base = {dt.datetime.strptime(r["data"], "%d/%m/%Y").date(): r for r in ler_csv(caminho)}
    for d, m in meta_dia.items():
        base.setdefault(d, {"data": f"{d:%d/%m/%Y}"}).update(m)
    for d, s in site_dia.items():
        base.setdefault(d, {"data": f"{d:%d/%m/%Y}"}).update(
            {"visitas_reais": len(s["sess"]), "visitantes_unicos": len(s["vis"]), "cliques_saida": s["cli"]})
    acum, linhas = 0.0, []
    for d in sorted(base):
        r = base[d]
        g = num(r.get("gasto_dia"))
        acum += g
        v = num(r.get("visitas_reais"), int)
        r.update({"gasto_dia": f"{g:.2f}", "gasto_acumulado": f"{acum:.2f}",
                  "custo_por_visita_dia": f"{g / v:.2f}" if v and g else ""})
        for c in COL_DIA:
            r.setdefault(c, "0")
        linhas.append(r)
    gravar_csv(caminho, COL_DIA, linhas)
    return linhas


def criterio(taxa, custo_cli):
    """Critério combinado do anúncio (só alerta; quem decide é o dono, junto com o Claude)."""
    if taxa >= 8 and custo_cli is not None and custo_cli < 1:
        return "APROVADO (saída >= 8% e custo por clique de saída < R$ 1)"
    if taxa < 3 or custo_cli is None or custo_cli > 3:
        return "ALERTA (saída < 3% ou custo por clique de saída > R$ 3) - conversar antes de mudar o anúncio"
    return "EM OBSERVAÇÃO (entre o alerta e a aprovação)"


# ---------------------------------------------------------------- 4. gráfico
def rotulos(ax, barras, fmt="{:.0f}"):
    for b in barras:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height(), fmt.format(b.get_height()), ha="center", va="bottom", fontsize=9)


def guardar_anteriores(pasta):
    """Deixa só 1 gráfico na pasta: os anteriores vão para old_bkp (nada é apagado)."""
    antigos = glob.glob(os.path.join(pasta, "GRAFICO_ANUNCIO_META_*.png"))
    if antigos:
        os.makedirs(os.path.join(pasta, "old_bkp"), exist_ok=True)
        for a in antigos:
            shutil.move(a, os.path.join(pasta, "old_bkp", os.path.basename(a)))


def desenhar(nome, verba, meta_custo, dias, gasto, visualiz, total_vis, saida_png, agora, aviso_meta, leituras=(), rot="resultados"):
    custo_vis = gasto / total_vis if total_vis else 0
    custo_meta = gasto / visualiz if visualiz else 0
    fig, ax = plt.subplots(2, 2, figsize=(14, 9))
    fig.suptitle(f"Anuncio Meta {nome} x visitas reais do blog ({agora:%d/%m/%Y %Hh%M})", fontsize=15, fontweight="bold")
    if aviso_meta:
        fig.text(0.5, 0.925, "Meta sem leitura nova nesta execucao: numeros da Meta = ultima leitura gravada",
                 ha="center", color=VERMELHO, fontsize=10)

    x = [r["data"][:5] for r in dias]
    if any(num(r["gasto_dia"]) for r in dias) or not leituras:
        ax[0][0].plot(x, [num(r["gasto_acumulado"]) for r in dias], marker="o", color=AZUL)
    else:  # sem os dias da Meta: usa as leituras gravadas no histórico
        ax[0][0].plot([f"{l['data'][:5]} {l['hora']}" for l in leituras], [l["gasto"] for l in leituras], marker="o", color=AZUL)
    if verba:
        ax[0][0].axhline(verba, color=VERMELHO, linestyle="--")
    ax[0][0].set_title(f"Gasto acumulado (verba R$ {verba:g})" if verba else "Gasto acumulado")
    ax[0][0].tick_params(axis="x", rotation=60, labelsize=8)

    pos = list(range(len(dias)))
    larg = 0.4
    b1 = ax[0][1].bar([p - larg / 2 for p in pos], [num(r.get("resultados_meta") or r.get("visualizacoes_pagina"), int) for r in dias], larg, color=AZUL, label=f"Meta: {rot}")
    b2 = ax[0][1].bar([p + larg / 2 for p in pos], [num(r["visitas_reais"], int) for r in dias], larg, color=VERDE, label="Site: visitas reais")
    rotulos(ax[0][1], b1)
    rotulos(ax[0][1], b2)
    ax[0][1].set_xticks(pos, x, rotation=60, fontsize=8)
    ax[0][1].legend(fontsize=8)
    ax[0][1].set_title("Por dia: Meta x visitas reais do blog")

    b = ax[1][0].bar([f"Meta: {rot}", "Site: visitas reais"], [visualiz, total_vis], color=[AZUL, VERDE])
    rotulos(ax[1][0], b)
    ax[1][0].set_title("Meta x blog (total)")

    b = ax[1][1].bar(["Custo/visita real", f"Custo/{rot} Meta", "Meta de custo"], [custo_vis, custo_meta, meta_custo], color=[VERDE, AZUL, CINZA])
    rotulos(ax[1][1], b, "{:.2f}")
    ax[1][1].set_title("Custo por visita (R$)")

    fig.tight_layout(rect=(0, 0, 1, 0.92))
    fig.savefig(saida_png, dpi=120)
    plt.close(fig)


# ---------------------------------------------------------------- execução
def main():
    ap = argparse.ArgumentParser(description="Busca os dados atuais (Meta + blog), atualiza os dados gerenciais e gera o gráfico.")
    ap.add_argument("--sem-baixar", action="store_true", help="não busca na Meta nem no site; usa o que já está gravado")
    ap.add_argument("--teste", action="store_true", help="refaz o gráfico do teste de 11 a 13/11 (dados antigos)")
    ap.add_argument("--campanha", help="número da campanha na Meta (substitui o da config nesta execução)")
    ap.add_argument("--utm", help="utm_campaign usada para contar as visitas do blog")
    ap.add_argument("--verba", type=float, help="verba total em reais (padrão: a da Meta)")
    ap.add_argument("--meta-custo", type=float, help="meta de custo por visita em reais (padrão 0,35)")
    ap.add_argument("--dias", type=int, default=60, help="quantos dias de acessos baixar do site (padrão 60)")
    ap.add_argument("--saida", default=PASTA_REL)
    ap.add_argument("--meta-manual", help="JSON com a leitura feita no Gerenciador (usado quando a API nao responde)")
    a = ap.parse_args()
    agora = dt.datetime.now()

    with open(LM.CONFIG, encoding="utf-8-sig") as fh:
        cfg = json.load(fh)
    cfg.setdefault("api_version", "v24.0")
    cfg.setdefault("acao_resultado", "landing_page_view")
    if a.campanha:
        cfg["campaign_id"] = a.campanha
    if a.teste:
        cfg.update({"campaign_id": "", "nome_campanha": "teste_11a13_11", "utm_campanha": "teste_11a13_11"})
    nome = cfg.get("nome_campanha") or "anuncio"
    utm = a.utm or cfg.get("utm_campanha") or nome
    meta_custo = a.meta_custo if a.meta_custo is not None else float(cfg.get("meta_custo_visita") or 0.35)

    # 1. Meta
    totais, meta_dia, aviso = None, {}, ""
    if a.teste or a.sem_baixar:
        aviso = "leitura da Meta não pedida nesta execução (--teste ou --sem-baixar)."
    else:
        print("Buscando os dados atuais na Meta...")
        totais, meta_dia, aviso = buscar_meta_agora(cfg, agora)
    meta_api = bool(totais)
    if not totais and a.meta_manual:
        totais, meta_dia = ler_meta_manual(a.meta_manual)
        hist_m = os.path.join(PASTA_REL, f"LEITURA_ANUNCIO_META_historico_{cfg.get('campaign_id')}.csv")
        LM.gravar_linha(hist_m, agora, totais)
        print(f"Meta (leitura manual do Gerenciador) usada: gasto {reais(totais['gasto'])} -> {hist_m}")
        aviso = ""
    if aviso:
        print("AVISO META:", aviso)

    # 2. blog
    arq = None if (a.teste or a.sem_baixar) else baixar_acessos(a.dias)
    arq = arq or max(glob.glob(os.path.join(PASTA_ACESSOS, "acessos_*.csv")), key=os.path.getmtime)
    site_dia = visitas_por_dia(arq, utm)

    # 3. dados gerenciais
    hist = CSV_TESTE if a.teste else os.path.join(PASTA_REL, f"LEITURA_ANUNCIO_META_historico_{cfg.get('campaign_id')}.csv")
    leituras = LM.ler_historico(hist)
    ult = leituras[-1] if leituras else None
    if totais:
        gasto, visualiz, status, verba = totais["gasto"], totais["resultados"], totais["status"], totais["verba"]
    elif ult:
        gasto, visualiz, status, verba = ult["gasto"], ult["resultados"], ult["status"], None
    else:
        gasto, visualiz, status, verba = 0.0, 0, "sem leitura", None
    verba = a.verba or verba or float(cfg.get("orcamento") or 0) or (50.0 if a.teste else 240.0)

    os.makedirs(a.saida, exist_ok=True)
    arq_dia = os.path.join(a.saida, f"DADOS_GERENCIAIS_ANUNCIO_META_{nome}.csv")
    dias = atualizar_por_dia(arq_dia, meta_dia, site_dia)
    total_vis = sum(len(s["sess"]) for s in site_dia.values())
    unicos = len(set().union(*[s["vis"] for s in site_dia.values()])) if site_dia else 0
    cliques = sum(s["cli"] for s in site_dia.values())
    taxa = cliques / total_vis * 100 if total_vis else 0.0
    custo_cli = gasto / cliques if cliques else None
    crit = criterio(taxa, custo_cli) if gasto > 0 else "SEM AVALIAÇÃO (falta a leitura do gasto na Meta)"
    resumo = {"data": f"{agora:%d/%m/%Y}", "hora": f"{agora:%Hh%M}", "fonte_meta": ("leitura manual Gerenciador" if a.meta_manual and not meta_api else "API agora") if totais else "ultima leitura gravada",
              "status": status, "verba": f"{verba:.2f}", "gasto": f"{gasto:.2f}", "pct_verba": f"{gasto / verba * 100:.1f}" if verba else "",
              "saldo": f"{max(verba - gasto, 0):.2f}" if verba else "", "resultados_meta": visualiz, "visitas_reais": total_vis,
              "visitantes_unicos": unicos, "cliques_saida": cliques, "taxa_saida_pct": f"{taxa:.1f}",
              "custo_por_visita": f"{gasto / total_vis:.2f}" if total_vis else "",
              "custo_por_clique_saida": f"{custo_cli:.2f}" if custo_cli else "", "criterio": crit,
              "arquivo_acessos": os.path.basename(arq)}
    arq_resumo = os.path.join(a.saida, f"RESUMO_GERENCIAL_ANUNCIO_META_{nome}.csv")
    gravar_csv(arq_resumo, COL_RESUMO, [resumo], acrescentar=True)

    # 4. gráfico
    guardar_anteriores(a.saida)
    png = os.path.join(a.saida, f"GRAFICO_ANUNCIO_META_{agora:%d_%m_%Y_%Hh%M}.png")
    desenhar(nome, verba, meta_custo, dias, gasto, visualiz, total_vis, png, agora, bool(aviso), leituras, cfg.get("rotulo_resultado") or "resultados")

    print("=" * 70)
    print("GRAFICO:", png)
    print("DADOS POR DIA:", arq_dia)
    print("RESUMO GERENCIAL:", arq_resumo)
    print(f"{nome} | status {status} | gasto {reais(gasto)} de {reais(verba)} | visualizações Meta {visualiz} | "
          f"visitas reais {total_vis} | únicos {unicos} | cliques de saída {cliques} ({taxa:.1f}%)")
    print("Critério:", crit)
    if aviso:
        print("ATENÇÃO: números da Meta SEM leitura nova ->", aviso)
    return 0


if __name__ == "__main__":
    sys.exit(main())
