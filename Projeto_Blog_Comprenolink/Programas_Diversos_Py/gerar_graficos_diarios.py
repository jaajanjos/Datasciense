# -*- coding: utf-8 -*-
"""Gera o PDF diario de graficos do anuncio Meta (teste_11a13_11_anuncio).

Fontes:
  - 4_Relatorio_Ativ_Claude_no_Blog\\LEITURA_ANUNCIO_META_historico.csv  (leituras acumuladas: data;hora;gasto;impressoes;alcance;resultados;status;observacao)
  - 1_Pendencias\\graficos_diarios\\dados_por_dia.csv                     (por dia: data;resultados;alcance;frequencia)
Saida: 1_Pendencias\\graficos_diarios\\Graficos_Metas_Anuncios_dd-mm-aa_HHhMM.pdf  (se ja existir, a versao antiga vai para old_bkp)
Uso: python -X utf8 gerar_graficos_diarios.py
"""
import csv, os, shutil, sys
from datetime import datetime
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
plt.rcParams["text.parse_math"] = False
from matplotlib.backends.backend_pdf import PdfPages

BASE = r"D:\Projeto_Blog_Comprenolink\0- Pendencias"
HIST = os.path.join(BASE, r"4_Relatorio_Ativ_Claude_no_Blog\LEITURA_ANUNCIO_META_historico.csv")
PASTA = os.path.join(BASE, r"1_Pendencias\graficos_diarios")
DIA = os.path.join(PASTA, "dados_por_dia.csv")
VERBA = 50.0
META_CPR = 0.35
AZ, LAR, VD, CZ = "#1f4e79", "#e07b00", "#2e8b57", "#666666"


def ler_hist():
    linhas = list(csv.DictReader(open(HIST, encoding="utf-8-sig"), delimiter=";"))
    out = []
    for r in linhas:
        t = datetime.strptime(r["data"] + " " + r["hora"].replace("h", ":"), "%d/%m/%Y %H:%M")
        out.append({"t": t, "gasto": float(r["gasto"]), "imp": int(r["impressoes"]), "alc": int(r["alcance"]),
                    "res": int(r["resultados"]), "status": r["status"]})
    out.sort(key=lambda x: x["t"])
    return out


def ler_dias():
    if not os.path.exists(DIA):
        return []
    out = []
    for r in csv.DictReader(open(DIA, encoding="utf-8-sig"), delimiter=";"):
        out.append({"d": datetime.strptime(r["data"], "%d/%m/%Y"), "res": int(r["resultados"]),
                    "alc": int(r["alcance"]), "freq": float(str(r["frequencia"]).replace(",", "."))})
    out.sort(key=lambda x: x["d"])
    return out


SITE_DIR = r"D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\dados_acessos"
CAMP = "teste_11a13_11"


def ler_site():
    """Visitas reais do blog vindas do anuncio (UTM campanha) + compras atribuidas. None se nao houver arquivo."""
    import glob
    arqs = sorted(glob.glob(os.path.join(SITE_DIR, "acessos_*.csv")))
    if not arqs:
        return None
    per, todos = {}, set()
    for r in csv.DictReader(open(arqs[-1], encoding="utf-8-sig"), delimiter=";"):
        if r.get("campanha") != CAMP:
            continue
        d = datetime.strptime(r["criado_em"][:10], "%Y-%m-%d")
        x = per.setdefault(d, {"d": d, "vis": 0, "uniq": set(), "cli": 0})
        if r["tipo"] == "visita":
            x["vis"] += 1
            x["uniq"].add(r["visitante"])
            todos.add(r["visitante"])
        elif r["tipo"] == "clique":
            x["cli"] += 1
    dias = sorted(per.values(), key=lambda z: z["d"])
    for z in dias:
        z["uniq"] = len(z["uniq"])
    compras, arq_c = 0, ""
    ac = sorted(glob.glob(os.path.join(SITE_DIR, "compras_atribuidas_*.csv")))
    if ac:
        arq_c = os.path.basename(ac[-1])
        compras = sum(1 for r in csv.DictReader(open(ac[-1], encoding="utf-8-sig"), delimiter=";") if r.get("campanha") == CAMP)
    return {"arq": os.path.basename(arqs[-1]), "arq_c": arq_c, "dias": dias, "vis": sum(z["vis"] for z in dias),
            "uniq": len(todos), "cli": sum(z["cli"] for z in dias), "compras": compras}


def gravar_site_csv(site, dias):
    """Acrescenta as colunas do site em dados_por_dia.csv e grava visitas_site_por_dia.csv (todos os dias da campanha)."""
    if not site:
        return
    mapa = {z["d"].strftime("%d/%m/%Y"): z for z in site["dias"]}
    if os.path.exists(DIA):
        linhas = list(csv.DictReader(open(DIA, encoding="utf-8-sig"), delimiter=";"))
        with open(DIA, "w", encoding="utf-8-sig", newline="") as f:
            w = csv.writer(f, delimiter=";")
            w.writerow(["data", "resultados", "alcance", "frequencia", "visitas_reais", "visitantes_unicos", "cliques_saida", "compras_atribuidas"])
            for r in linhas:
                z = mapa.get(r["data"])
                w.writerow([r["data"], r["resultados"], r["alcance"], r["frequencia"],
                            z["vis"] if z else 0, z["uniq"] if z else 0, z["cli"] if z else 0, ""])
    with open(os.path.join(PASTA, "visitas_site_por_dia.csv"), "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter=";")
        w.writerow(["data", "visitas_reais", "visitantes_unicos", "cliques_saida"])
        for z in site["dias"]:
            w.writerow([z["d"].strftime("%d/%m/%Y"), z["vis"], z["uniq"], z["cli"]])


def criterio_saida(site, gasto):
    """Criterio do teste de anuncio: aprovado (saida >= 8% e custo/clique de saida < R$ 1), parar cedo (saida < 3% ou custo > R$ 3)."""
    vis, cli = site["vis"], site["cli"]
    sa = cli / vis * 100 if vis else 0.0
    cc = gasto / cli if cli else None
    if sa >= 8 and cc is not None and cc < 1.0:
        return sa, cc, "APROVADO (saída >= 8% e custo por clique de saída < R$ 1)"
    if sa < 3 or cc is None or cc > 3.0:
        return sa, cc, "ALERTA: PARAR CEDO (saída < 3% ou custo por clique de saída > R$ 3). Quem pausa é o dono."
    return sa, cc, "EM OBSERVAÇÃO (entre o alerta e a aprovação)"


def leitura_site(site, dias, res_meta, gasto):
    """Texto dos 2 graficos novos (Meta x site, funil)."""
    s = site
    pico = max(s["dias"], key=lambda z: z["vis"])
    cpv = gasto / s["uniq"] if s["uniq"] else 0
    pct_saida = s["cli"] / s["vis"] * 100 if s["vis"] else 0
    sem_v = "VERDE" if s["uniq"] >= 150 and cpv <= META_CPR else "VERMELHO"
    sem_s = "VERDE" if pct_saida >= 5 else "VERMELHO"
    return [("5. Meta x site: resultados e visitas reais por dia",
             "Barras lado a lado: resultados que a Meta contou (visualizações da página) e visitas que o blog registrou pela campanha, em cada dia.",
             "Ver se o que a Meta diz bate com o que chega de fato ao blog, e achar os melhores dias.",
             f"O blog registrou {num(s['vis'])} visitas ({num(s['uniq'])} visitantes únicos) contra {num(res_meta)} resultados da Meta. Melhor dia no site: {pico['d'].strftime('%d/%m')} com {pico['vis']} visitas. Custo por visitante único: {brl(cpv)} (meta até {brl(META_CPR)}): semáforo {sem_v}.",
             "Tendência: quando as barras do site ficam acima das da Meta, a Meta está contando menos (mede por pixel); use o site como referência das visitas reais."),
            ("6. Funil do anúncio (escala logarítmica)",
             "Do total de exibições até a compra: impressões, resultados da Meta, visitantes no site, cliques de saída para o Mercado Livre e compras atribuídas.",
             "Achar onde as pessoas se perdem: se o problema é o anúncio (poucas visitas) ou o que vem depois do clique (poucos cliques de saída).",
             f"{num(s['cli'])} cliques de saída em {num(s['vis'])} visitas ({pct_saida:.1f}%): semáforo {sem_s} (referência: a home do blog fica em torno de 18%). Custo por clique de saída: {(brl(gasto / s['cli']) if s['cli'] else 'sem cliques de saída')}. Critério do teste: {criterio_saida(s, gasto)[2]} Compras atribuídas ao anúncio: {s['compras']} (arquivo {s['arq_c'] or 'não encontrado'}).",
             "Tendência: se visitas sobem e cliques de saída não, o gargalo é a página/entrada; o ML só confirma vendas em cerca de 60 dias, então compras zeradas ainda não são conclusivas.")]


def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def num(v):
    return f"{v:,}".replace(",", ".")


def leitura_graficos(h, dias, cpr):
    """Texto de cada grafico: o que e, para que serve, objetivo, análise e tendência (calculados com os dados)."""
    ult = h[-1]
    ant = h[-2] if len(h) > 1 else None
    ant2 = h[-3] if len(h) > 2 else None
    saldo = VERBA - ult["gasto"]
    out = []

    # 1) gasto acumulado
    if ant:
        hs = (ult["t"] - ant["t"]).total_seconds() / 3600
        ritmo = (ult["gasto"] - ant["gasto"]) / hs if hs > 0 else 0
    else:
        ritmo = 0
    tend = "sem base para comparar ainda."
    if ant2 and ant:
        hs2 = (ant["t"] - ant2["t"]).total_seconds() / 3600
        ritmo2 = (ant["gasto"] - ant2["gasto"]) / hs2 if hs2 > 0 else 0
        if ritmo > ritmo2 * 1.15:
            tend = f"gasto ACELERANDO ({brl(ritmo * 24)} por dia no ritmo atual, contra {brl(ritmo2 * 24)} antes)."
        elif ritmo < ritmo2 * 0.85:
            tend = f"gasto DESACELERANDO ({brl(ritmo * 24)} por dia no ritmo atual, contra {brl(ritmo2 * 24)} antes)."
        else:
            tend = f"gasto ESTÁVEL, em torno de {brl(ritmo * 24)} por dia."
    if saldo <= 0.01:
        prev = "a verba JÁ FOI TODA USADA."
    elif ritmo > 0:
        horas = saldo / ritmo
        prev = f"no ritmo atual o saldo de {brl(saldo)} acaba em cerca de {horas:.0f} h (por volta de {(ult['t'] + __import__('datetime').timedelta(hours=horas)).strftime('%d/%m %Hh')})."
    else:
        prev = "sem gasto novo desde a leitura anterior."
    out.append(("1. Gasto acumulado (R$)",
                "Mostra, a cada leitura, quanto dos R$ 50 de verba já foi gasto.",
                "Acompanhar o ritmo de consumo da verba e saber quando ela acaba, para decidir prorrogar ou não.",
                f"Gasto de {brl(ult['gasto'])} ({ult['gasto'] / VERBA * 100:.0f}% da verba); saldo de {brl(saldo)}. Entre as duas últimas leituras o ritmo foi de {brl(ritmo * 24)} por dia.",
                f"Tendência: {tend} Previsão: {prev}"))

    # 2) impressões, alcance, resultados
    freq = ult["imp"] / ult["alc"] if ult["alc"] else 0
    taxa = ult["res"] / ult["imp"] * 100 if ult["imp"] else 0
    if ant and ant["imp"]:
        taxa_ant = ant["res"] / ant["imp"] * 100
        tt = "subindo" if taxa > taxa_ant + .3 else ("caindo" if taxa < taxa_ant - .3 else "estável")
        cresc = ult["imp"] - ant["imp"]
        tend2 = f"audiência cresceu {num(cresc)} impressões desde a leitura anterior; taxa de resultados {tt} ({taxa_ant:.1f}% -> {taxa:.1f}%)."
    else:
        tend2 = "sem base para comparar ainda."
    aviso = " Cada pessoa viu o anúncio só uma vez (frequência 1,00): o anúncio está chegando a gente nova, sem repetir." if freq <= 1.05 else f" Frequencia de {freq:.2f}: parte do publico ja viu mais de uma vez."
    out.append(("2. Impressões, alcance e resultados (acumulado)",
                "Impressões = vezes que o anúncio apareceu; alcance = pessoas diferentes que viram; resultados = visualizações da página de destino (clique em 7 dias ou exibição em 1 dia).",
                "Medir o tamanho da audiência e quanto dela virou visualização da página; verificar se o anúncio não está saturando as mesmas pessoas.",
                f"{num(ult['imp'])} impressões, {num(ult['alc'])} pessoas alcançadas e {num(ult['res'])} resultados ({taxa:.1f}% das impressões)." + aviso,
                f"Tendência: {tend2} Lembrete: 'resultado' pode superestimar as visitas reais; conferir no Analytics/relatório de acessos."))

    # 3) custo por resultado
    atual = cpr[-1]
    if len(cpr) > 1:
        var = atual - cpr[-2]
        tt3 = "SUBINDO" if var > .01 else ("CAINDO" if var < -.01 else "ESTÁVEL")
        tend3 = f"custo {tt3} ({brl(cpr[-2])} -> {brl(atual)})."
    else:
        tend3 = "sem base para comparar ainda."
    folga = META_CPR - atual
    out.append(("3. Custo por resultado (R$)",
                "Gasto acumulado dividido pelos resultados: quanto custa cada visualização da página.",
                f"Saber se o anúncio é barato o bastante: a meta combinada é até {brl(META_CPR)} por resultado.",
                f"Custo atual de {brl(atual)}, " + (f"{brl(folga)} ABAIXO da meta (semáforo verde)." if folga >= 0 else f"{brl(-folga)} ACIMA da meta (semáforo vermelho)."),
                f"Tendência: {tend3} " + ("Se continuar subindo, a margem ate a meta diminui." if len(cpr) > 1 and cpr[-1] > cpr[-2] + .01 else "Sem sinal de piora no custo.")))

    # 4) por dia
    if dias:
        melhor = max(dias, key=lambda d: d["res"])
        ult_d = dias[-1]
        hoje = ult["t"].date()
        parcial = " (dia em andamento, número ainda parcial)" if ult_d["d"].date() == hoje else ""
        comp_dias = [d for d in dias if d["d"].date() != hoje] or dias
        media = sum(d["res"] for d in comp_dias) / len(comp_dias)
        if len(comp_dias) > 1:
            a, b = comp_dias[-1]["res"], comp_dias[-2]["res"]
            tend4 = f"entre os dois últimos dias fechados os resultados foram de {b} para {a} ({'alta' if a > b else ('queda' if a < b else 'estável')})."
        else:
            tend4 = "poucos dias fechados para comparar."
        out.append(("4. Resultados e alcance por dia",
                    "Barras com os resultados e o alcance de cada dia, vindos do Gerenciador de Anúncios (detalhamento por dia).",
                    "Ver o desempenho diário, achar os melhores dias e perceber se o anúncio está ganhando ou perdendo força.",
                    f"Melhor dia até agora: {melhor['d'].strftime('%d/%m')} com {melhor['res']} resultados. Média dos dias fechados: {media:.0f} resultados/dia. Último dia: {ult_d['d'].strftime('%d/%m')} com {ult_d['res']} resultados e alcance de {num(ult_d['alc'])}{parcial}.",
                    f"Tendência: {tend4}"))
    return out


def estilo(ax):
    ax.grid(alpha=.25)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)


def main():
    h = ler_hist()
    dias = ler_dias()
    site = ler_site()
    gravar_site_csv(site, dias)
    if not h:
        print("Sem leituras no historico.")
        return 1
    ult = h[-1]
    ant = h[-2] if len(h) > 1 else None
    nome = f"Graficos_Metas_Anuncios_{datetime.now().strftime('%d-%m-%y_%Hh%M')}.pdf"
    destino = os.path.join(PASTA, nome)
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    if os.path.exists(destino):
        _bk = os.path.join(PASTA, "old_bkp", nome.replace(".pdf", f"_{datetime.now().strftime('%Hh%M%S')}.pdf"))
        shutil.copy2(destino, _bk)
        try:
            os.unlink(destino)
        except PermissionError:
            # arquivo aberto em outro programa: grava com hora no nome
            destino = destino.replace('.pdf', f"_{datetime.now().strftime('%Hh%M')}.pdf")

    t = [x["t"] for x in h]
    gasto = [x["gasto"] for x in h]
    imp = [x["imp"] for x in h]
    alc = [x["alc"] for x in h]
    res = [x["res"] for x in h]
    cpr = [g / r if r else 0 for g, r in zip(gasto, res)]
    pct = ult["gasto"] / VERBA * 100
    saldo = VERBA - ult["gasto"]
    taxa = ult["res"] / ult["imp"] * 100 if ult["imp"] else 0

    with PdfPages(destino) as pdf:
        # ---------- pagina 1: resumo
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(.07, .95, "Anúncio Meta teste_11a13_11_anuncio", fontsize=18, fontweight="bold", color=AZ)
        fig.text(.07, .925, f"Gráficos diários · dados até {ult['t'].strftime('%d/%m/%Y %H:%M')} · gerado em {datetime.now().strftime('%d/%m/%Y %H:%M')}", fontsize=10, color=CZ)
        linhas = [
            ("Status", ult["status"]),
            ("Gasto acumulado", f"{brl(ult['gasto'])}  ({pct:.1f}% da verba de {brl(VERBA)})"),
            ("Saldo restante", brl(saldo)),
            ("Impressões / alcance", f"{num(ult['imp'])} / {num(ult['alc'])}" + ("  (cada pessoa viu 1 vez)" if ult["imp"] == ult["alc"] else "")),
            ("Resultados (vis. da página)", f"{num(ult['res'])}  ({taxa:.1f}% das impressões)"),
            ("Custo por resultado", f"{brl(cpr[-1])}  (meta até {brl(META_CPR)})"),
        ]
        if site:
            linhas += [("Visitas reais (site)", f"{num(site['vis'])} visitas, {num(site['uniq'])} visitantes únicos  ({brl(ult['gasto'] / site['uniq'] if site['uniq'] else 0)} por visitante)"),
                       ("Cliques de saída p/ ML", f"{num(site['cli'])}  ({site['cli'] / site['vis'] * 100 if site['vis'] else 0:.1f}% das visitas)"),
                       ("Custo por clique de saída", (brl(ult['gasto'] / site['cli']) if site['cli'] else "sem cliques de saída")),
                       ("Critério do teste", criterio_saida(site, ult['gasto'])[2].split(' (')[0].split('.')[0]),
                       ("Compras atribuídas", f"{site['compras']}")]
        y = .875
        for k, v in linhas:
            fig.text(.07, y, k, fontsize=11, fontweight="bold")
            fig.text(.45, y, v, fontsize=11)
            y -= .033
        y -= .01
        fig.text(.07, y, "Comparação com a leitura anterior", fontsize=12, fontweight="bold", color=AZ)
        y -= .033
        if ant:
            dt = (ult["t"] - ant["t"]).total_seconds() / 3600
            comp = [f"Leitura anterior: {ant['t'].strftime('%d/%m %H:%M')}  (há {dt:.0f} h)",
                    f"Gasto: +{brl(ult['gasto'] - ant['gasto'])}   ·   Impressões: +{num(ult['imp'] - ant['imp'])}   ·   Resultados: +{num(ult['res'] - ant['res'])}"]
            for c in comp:
                fig.text(.07, y, c, fontsize=10.5)
                y -= .028
        y -= .015
        fig.text(.07, y, "Conclusão e pontos de atenção", fontsize=12, fontweight="bold", color=AZ)
        y -= .033
        sem = "VERDE" if cpr[-1] <= META_CPR else "VERMELHO"
        txt = [f"Semáforo de custo: {sem} (custo por resultado {brl(cpr[-1])} x meta {brl(META_CPR)}).",
               f"Verba: {pct:.0f}% usada; saldo de {brl(saldo)}." + (" Verba esgotada." if saldo <= 0.01 else ""),
               "'Resultado' = visualização da página (clique 7 dias ou exibição 1 dia): pode superestimar.",
               ("Visitas reais do blog (UTM) conferidas na página 3: use-as, não só o 'resultado', antes de subir a verba." if site else "Confirmar visitas reais (relatório de acessos/Analytics, UTM) antes de subir a verba."),
               "Aumento de orçamento ou limite de gastos só com 'de acordo' do dono."]
        for c in txt:
            fig.text(.07, y, "• " + c, fontsize=10)
            y -= .027
        y -= .02
        fig.text(.07, y, "O que cada gráfico mostra (págs. 2 a 4)", fontsize=12, fontweight="bold", color=AZ)
        y -= .033
        for c in ["Gasto acumulado: quanto da verba de R$ 50 já foi usado em cada leitura.",
                  "Impressões, alcance e resultados acumulados: tamanho da audiência e das visualizações.",
                  "Custo por resultado: gasto ÷ resultados; abaixo da linha da meta é bom.",
                  "Resultados e alcance por dia: quanto o anúncio rendeu em cada dia (dados do Gerenciador)."]:
            fig.text(.07, y, "• " + c, fontsize=10)
            y -= .026
        pdf.savefig(fig)
        plt.close(fig)

        # ---------- pagina 2: graficos
        fig, ax = plt.subplots(2, 2, figsize=(11.69, 8.27))
        fig.suptitle(f"Gráficos do anúncio — leitura de {ult['t'].strftime('%d/%m/%Y %H:%M')}", fontsize=13, fontweight="bold")
        a = ax[0][0]
        a.plot(t, gasto, marker="o", color=AZ, lw=2.5)
        a.axhline(VERBA, color=LAR, ls="--")
        a.text(t[0], VERBA + 1, f"Verba {brl(VERBA)}", color=LAR, fontsize=8)
        for x, v in zip(t, gasto):
            a.annotate(brl(v), (x, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
        a.set_title("Gasto acumulado (R$)", fontsize=10)
        a.set_ylim(0, VERBA * 1.15)
        a = ax[0][1]
        a.plot(t, imp, marker="o", color=AZ, lw=2.2, label="Impressões")
        a.plot(t, alc, marker="^", color=LAR, lw=1.6, ls="--", label="Alcance")
        a.plot(t, res, marker="s", color=VD, lw=2.2, label="Resultados")
        a.set_title("Impressões, alcance e resultados (acumulado)", fontsize=10)
        a.legend(fontsize=8, loc="upper left")
        a = ax[1][0]
        a.plot(t, cpr, marker="o", color=LAR, lw=2.5)
        a.axhline(META_CPR, color=CZ, ls="--")
        a.text(t[0], META_CPR + .01, f"Meta até {brl(META_CPR)}", color=CZ, fontsize=8)
        for x, v in zip(t, cpr):
            a.annotate(brl(v), (x, v), textcoords="offset points", xytext=(0, 7), ha="center", fontsize=8)
        a.set_title("Custo por resultado (R$)", fontsize=10)
        a.set_ylim(0, max(META_CPR * 1.3, max(cpr) * 1.25))
        a = ax[1][1]
        if dias:
            x = list(range(len(dias)))
            a.bar([i - .2 for i in x], [d["res"] for d in dias], width=.4, color=VD, label="Resultados")
            a2 = a.twinx()
            a2.bar([i + .2 for i in x], [d["alc"] for d in dias], width=.4, color=AZ, label="Alcance")
            a.set_xticks(x)
            a.set_xticklabels([d["d"].strftime("%d/%m") for d in dias])
            for i, d in enumerate(dias):
                a.annotate(str(d["res"]), (i - .2, d["res"]), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8, color=VD)
                a2.annotate(num(d["alc"]), (i + .2, d["alc"]), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8, color=AZ)
            a.set_ylabel("Resultados", color=VD, fontsize=8)
            a2.set_ylabel("Alcance", color=AZ, fontsize=8)
            a2.spines["top"].set_visible(False)
        a.set_title("Resultados e alcance por dia", fontsize=10)
        for a in ax.flat:
            estilo(a)
        for a in (ax[0][0], ax[0][1], ax[1][0]):
            a.set_xticks(t)
            a.set_xticklabels([x.strftime("%d/%m\n%Hh%M") for x in t], fontsize=7)
        fig.tight_layout(rect=[0, 0, 1, .95])
        pdf.savefig(fig)
        plt.close(fig)

        # ---------- pagina 3: Meta x site e funil
        import textwrap
        if site and site["dias"]:
            fig, ax = plt.subplots(2, 1, figsize=(8.27, 11.69))
            fig.suptitle("Meta x site e funil do anúncio", fontsize=14, fontweight="bold", color=AZ)
            datas = sorted({z["d"] for z in site["dias"]} | {d["d"] for d in dias})
            mv = {z["d"]: z["vis"] for z in site["dias"]}
            mr = {d["d"]: d["res"] for d in dias}
            x = list(range(len(datas)))
            a = ax[0]
            a.bar([i - .2 for i in x], [mr.get(d, 0) for d in datas], width=.4, color=VD, label="Resultados (Meta)")
            a.bar([i + .2 for i in x], [mv.get(d, 0) for d in datas], width=.4, color=AZ, label="Visitas reais (site)")
            for i, d in enumerate(datas):
                a.annotate(str(mr.get(d, 0)), (i - .2, mr.get(d, 0)), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8, color=VD)
                a.annotate(str(mv.get(d, 0)), (i + .2, mv.get(d, 0)), textcoords="offset points", xytext=(0, 3), ha="center", fontsize=8, color=AZ)
            a.set_xticks(x)
            a.set_xticklabels([d.strftime("%d/%m") for d in datas])
            a.set_title("Resultados da Meta x visitas reais do site, por dia", fontsize=10)
            a.legend(fontsize=8)
            estilo(a)
            et = ["Impressões", "Resultados (Meta)", "Visitantes no site", "Cliques p/ o ML", "Compras"]
            vl = [ult["imp"], ult["res"], site["uniq"], site["cli"], site["compras"]]
            a = ax[1]
            a.barh(et[::-1], vl[::-1], color=["#9ca3af", AZ, AZ, "#c0392b", "#9ca3af"][::-1])
            a.set_xscale("symlog")
            from matplotlib.ticker import FixedLocator, FixedFormatter
            a.xaxis.set_major_locator(FixedLocator([0, 1, 10, 100, 1000, 10000]))
            a.xaxis.set_major_formatter(FixedFormatter(["0", "1", "10", "100", "1.000", "10.000"]))
            for i, v in enumerate(vl[::-1]):
                a.text(max(v, 1) * 1.15, i, num(v), va="center", fontsize=9)
            a.set_title("Funil (escala logarítmica: cada degrau vale 10 vezes o anterior)", fontsize=10)
            estilo(a)
            fig.tight_layout(rect=[0, .42, 1, .96])
            y = .385
            for tit, serve, obj, anal, tend in leitura_site(site, dias, ult["res"], ult["gasto"]):
                fig.text(.07, y, tit, fontsize=11, fontweight="bold", color=AZ)
                y -= .022
                for rot, tx in (("Para que serve: ", serve), ("Objetivo: ", obj), ("Análise: ", anal), ("", tend)):
                    for l_ in textwrap.wrap(rot + tx, 105):
                        fig.text(.08, y, l_, fontsize=8.3)
                        y -= .0165
                    y -= .003
                y -= .012
            fig.text(.07, .012, f"Fonte do site: {site['arq']} (campanha {CAMP}); compras: {site['arq_c'] or 'sem arquivo'}", fontsize=7.5, color=CZ)
            pdf.savefig(fig)
            plt.close(fig)

        # ---------- pagina 2b: leitura de cada grafico
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(.07, .955, "Leitura de cada gráfico", fontsize=16, fontweight="bold", color=AZ)
        fig.text(.07, .932, f"Resumo, para que serve, objetivo, análise e tendência · dados até {ult['t'].strftime('%d/%m/%Y %H:%M')}", fontsize=9.5, color=CZ)
        y = .895
        for tit, serve, obj, anal, tend in leitura_graficos(h, dias, cpr):
            fig.text(.07, y, tit, fontsize=12, fontweight="bold", color=AZ)
            y -= .026
            for rot, tx in (("Para que serve: ", serve), ("Objetivo: ", obj), ("Análise: ", anal), ("", tend)):
                linhas_ = textwrap.wrap(rot + tx, 105)
                for i_, l_ in enumerate(linhas_):
                    fig.text(.08, y, l_, fontsize=9, fontweight=("bold" if (i_ == 0 and rot == "" and tx.startswith("Tendencia")) else "normal"))
                    y -= .0195
                y -= .004
            y -= .018
        pdf.savefig(fig)
        plt.close(fig)

        # ---------- pagina 3: tabelas
        fig = plt.figure(figsize=(8.27, 11.69))
        fig.text(.07, .95, "Dados coletados", fontsize=16, fontweight="bold", color=AZ)
        ax1 = fig.add_axes([.07, .62, .86, .30])
        ax1.axis("off")
        cab = ["Leitura", "Gasto", "% verba", "Impressões", "Alcance", "Resultados", "R$/result."]
        corpo = [[x["t"].strftime("%d/%m %H:%M"), brl(x["gasto"]), f"{x['gasto'] / VERBA * 100:.0f}%", num(x["imp"]),
                  num(x["alc"]), num(x["res"]), brl(c)] for x, c in zip(h, cpr)]
        tb = ax1.table(cellText=corpo[-14:], colLabels=cab, loc="upper center", cellLoc="center")
        tb.auto_set_font_size(False)
        tb.set_fontsize(8)
        tb.scale(1, 1.5)
        for (r_, c_), cel in tb.get_celld().items():
            if r_ == 0:
                cel.set_facecolor(AZ)
                cel.set_text_props(color="white", fontweight="bold")
        fig.text(.07, .60, "Por dia (Gerenciador de Anúncios)", fontsize=12, fontweight="bold", color=AZ)
        ax2 = fig.add_axes([.07, .30, .86, .28])
        ax2.axis("off")
        if dias:
            tb2 = ax2.table(cellText=[[d["d"].strftime("%d/%m/%Y"), num(d["res"]), num(d["alc"]), f"{d['freq']:.2f}".replace(".", ",")] for d in dias],
                            colLabels=["Dia", "Resultados", "Alcance", "Frequência"], loc="upper center", cellLoc="center")
            tb2.auto_set_font_size(False)
            tb2.set_fontsize(8)
            tb2.scale(1, 1.5)
            for (r_, c_), cel in tb2.get_celld().items():
                if r_ == 0:
                    cel.set_facecolor(AZ)
                    cel.set_text_props(color="white", fontweight="bold")
        fig.text(.07, .22, "Como a coleta é feita (todo dia às 10:00)", fontsize=12, fontweight="bold", color=AZ)
        yy = .195
        for c in ["Lê o Gerenciador de Anúncios (visão 'Acompanhamento Teste Campanha') no Chrome com a extensão Claude.",
                  "Acrescenta a leitura ao LEITURA_ANUNCIO_META_historico.csv e atualiza dados_por_dia.csv.",
                  "Lê os acessos do blog (campanha teste_11a13_11) e junta visitas reais, cliques de saída e compras atribuídas.",
                  "Gera este PDF Graficos_Metas_Anuncios_dd-mm-aa_HHhMM.pdf (5 páginas: resumo, gráficos, Meta x site e funil, leitura de cada gráfico, tabelas).",
                  "Não altera orçamento, entrega nem limite da conta de anúncios."]:
            fig.text(.07, yy, "• " + c, fontsize=9)
            yy -= .024
        pdf.savefig(fig)
        plt.close(fig)
    print(destino)
    try:
        import sincronizar_relatorios_diarios as _sync
        _sync.main()
    except Exception as e:
        print('Sincronizacao com o OneDrive nao feita:', e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
