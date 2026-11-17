# -*- coding: utf-8 -*-
"""Gera o PDF diario de graficos do anuncio Meta (teste_11a13_11_anuncio).

Fontes:
  - 4_Relatorio_Ativ_Claude_no_Blog\\LEITURA_ANUNCIO_META_historico.csv  (leituras acumuladas: data;hora;gasto;impressoes;alcance;resultados;status;observacao)
  - 1_Pendencias\\graficos_diarios\\dados_por_dia.csv                     (por dia: data;resultados;alcance;frequencia)
Saida: 1_Pendencias\\graficos_diarios\\graficos_DD-MM-AA.pdf  (se ja existir, a versao antiga vai para old_bkp)
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


def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def num(v):
    return f"{v:,}".replace(",", ".")


def estilo(ax):
    ax.grid(alpha=.25)
    for s in ("top", "right"):
        ax.spines[s].set_visible(False)
    ax.tick_params(labelsize=8)


def main():
    h = ler_hist()
    dias = ler_dias()
    if not h:
        print("Sem leituras no historico.")
        return 1
    ult = h[-1]
    ant = h[-2] if len(h) > 1 else None
    nome = f"graficos_{ult['t'].strftime('%d-%m-%y')}.pdf"
    destino = os.path.join(PASTA, nome)
    os.makedirs(os.path.join(PASTA, "old_bkp"), exist_ok=True)
    if os.path.exists(destino):
        shutil.move(destino, os.path.join(PASTA, "old_bkp", nome.replace(".pdf", f"_{datetime.now().strftime('%Hh%M%S')}.pdf")))

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
               "Confirmar visitas reais (relatório de acessos/Analytics, UTM) antes de subir a verba.",
               "Aumento de orçamento ou limite de gastos só com 'de acordo' do dono."]
        for c in txt:
            fig.text(.07, y, "• " + c, fontsize=10)
            y -= .027
        y -= .02
        fig.text(.07, y, "O que cada gráfico mostra (página 2)", fontsize=12, fontweight="bold", color=AZ)
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
                  "Gera este PDF graficos_DD-MM-AA.pdf (cópia anterior do mesmo dia vai para old_bkp).",
                  "Não altera orçamento, entrega nem limite da conta de anúncios."]:
            fig.text(.07, yy, "• " + c, fontsize=9)
            yy -= .024
        pdf.savefig(fig)
        plt.close(fig)
    print(destino)
    return 0


if __name__ == "__main__":
    sys.exit(main())
