# -*- coding: utf-8 -*-
"""
Limpa os arquivos acumulados em Relatorios_Diarios_Anuncios depois que o painel foi consolidado.

O que sai (vai para a LIXEIRA do Windows, dá para recuperar):
  - Painel_conversao_performance_*.pdf ........ fica 1 por dia, dos últimos N dias
  - _historico_relatorios\\relatorio_*.html .... ficam os dos últimos N dias; um HTML só sai se as métricas
                                                 do dia dele já estão em historico_consolidado\\historico_quadros.csv
  - relatorio_*.html da pasta principal ......... saem quando já existe a cópia idêntica em _historico_relatorios
  - _backup_painel\\Painel_*.xlsx ............... ficam os últimos N
  - anuncios_status\\status_anuncios_*.csv ...... ficam os últimos N (o historico_status_anuncios.csv fica sempre)
  - Relatorios_Diarios_Anuncios\\dados_acessos ............ cópias brutas dos últimos N dias (cada uma já tem os 30 dias)
Nunca mexe em: a planilha, historico_quadros.csv, historico_vendas.csv, historico_status_anuncios.csv,
vendas_afiliados e conversao_e_performance_do_blog_*.pdf.

Quantos manter: aba Metas da planilha (linhas "Limpeza: ..."). Padrão 3 / 3 / 5 / 3.
Uso:  python 7_limpar_historico.py [pasta_relatorios] [--simular]
"""
import csv
import glob
import os
import re
import subprocess
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
args = [a for a in sys.argv[1:] if not a.startswith("--")]
SIMULAR = "--simular" in sys.argv
PASTA = args[0] if args else os.path.join(BASE, "Relatorios_Diarios_Anuncios")
ARQ = os.path.join(PASTA, "Painel de  Controle de Acesso.xlsx")
PASTA_DADOS_BRUTOS = (os.environ.get("PAINEL_PASTA_BRUTOS")  # cópias do gerador de relatório
                      or os.path.join(BASE, "Relatorios_Diarios_Anuncios\\programas_fontes_python", "dados_acessos"))
PADRAO = {"pdf": 3, "html": 3, "backup": 5, "status": 3, "dados": 3}
ROTULOS = {"pdf": "Limpeza: manter PDFs do painel", "html": "Limpeza: manter relatórios HTML",
           "backup": "Limpeza: manter backups da planilha", "status": "Limpeza: manter verificações de anúncios",
           "dados": "Limpeza: manter cópias brutas de acessos"}


def retencao():
    valores = dict(PADRAO)
    try:
        from openpyxl import load_workbook
        ws = load_workbook(ARQ, read_only=True)["Metas"]
        for r in ws.iter_rows(min_row=4, values_only=True):
            for chave, rot in ROTULOS.items():
                if r and r[0] and str(r[0]).startswith(rot) and isinstance(r[1], (int, float)) and r[1] >= 1:
                    valores[chave] = int(r[1])
    except Exception as e:  # planilha aberta/ausente: usa o padrão
        print("  (usando retenção padrão:", e, ")")
    return valores


def dia_hora(nome):
    m = re.search(r"(\d{4})-?(\d{2})-?(\d{2})_(\d{2})h?(\d{2})", os.path.basename(nome))
    return (f"{m.group(1)}-{m.group(2)}-{m.group(3)}", m.group(4) + m.group(5)) if m else (None, None)


def ultimos_dias(arquivos, n, um_por_dia):
    """Arquivos a manter: dos n dias mais recentes (1 por dia = o mais tarde do dia)."""
    por_dia = {}
    for a in arquivos:
        d, h = dia_hora(a)
        if d:
            por_dia.setdefault(d, []).append((h, a))
    manter = set()
    for d in sorted(por_dia)[-n:]:
        itens = sorted(por_dia[d])
        manter.update(a for _, a in (itens[-1:] if um_por_dia else itens))
    sem_data = {a for a in arquivos if not dia_hora(a)[0]}
    return manter | sem_data


def para_lixeira(caminhos):
    if not caminhos or SIMULAR:
        return
    lista = "\n".join(caminhos)
    script = ("Add-Type -AssemblyName Microsoft.VisualBasic; $input | ForEach-Object { if ($_ -and (Test-Path -LiteralPath $_)) "
              "{ [Microsoft.VisualBasic.FileIO.FileSystem]::DeleteFile($_, 'OnlyErrorDialogs', 'SendToRecycleBin') } }")
    subprocess.run(["powershell", "-NoProfile", "-Command", script], input=lista, text=True, encoding="utf-8",
                   check=True, capture_output=True)


def main():
    if not os.path.exists(ARQ):
        print("Planilha não encontrada; nada foi limpo.")
        return 1
    n = retencao()
    sair = []

    # PDFs do painel
    pdfs = glob.glob(os.path.join(PASTA, "Painel_conversao_performance_*.pdf"))
    sair += [a for a in pdfs if a not in ultimos_dias(pdfs, n["pdf"], True)]

    # HTML: só sai se o dia já está consolidado
    consolidados = set()
    hist = os.path.join(PASTA, "historico_consolidado", "historico_quadros.csv")
    if os.path.exists(hist):
        consolidados = {r["dia"] for r in csv.DictReader(open(hist, encoding="utf-8-sig"), delimiter=";")}
    pasta_hist = os.path.join(PASTA, "_historico_relatorios")
    htmls = glob.glob(os.path.join(pasta_hist, "relatorio_acessos_anuncios_*.html"))
    manter = ultimos_dias(htmls, n["html"], True)
    sair += [a for a in htmls if a not in manter and dia_hora(a)[0] in consolidados]
    # pasta principal: o painel já leu e consolidou; a cópia do dia fica em _historico_relatorios
    dias_arquivados = {dia_hora(a)[0] for a in htmls}
    for a in glob.glob(os.path.join(PASTA, "relatorio_acessos_anuncios_*.html")):
        if dia_hora(a)[0] in consolidados and dia_hora(a)[0] in dias_arquivados:
            sair.append(a)

    # backups, verificações avulsas e cópias brutas do gerador de relatório
    for padrao, chave in ((os.path.join(PASTA, "_backup_painel", "Painel_*.xlsx"), "backup"),
                          (os.path.join(PASTA, "anuncios_status", "status_anuncios_*.csv"), "status")):
        arqs = sorted(glob.glob(padrao), key=lambda a: dia_hora(a))
        sair += arqs[:-n[chave]] if len(arqs) > n[chave] else []
    brutos = glob.glob(os.path.join(PASTA_DADOS_BRUTOS, "acessos_*.*")) + \
        glob.glob(os.path.join(PASTA_DADOS_BRUTOS, "compras_atribuidas_*.csv"))
    sair += [a for a in brutos if a not in ultimos_dias(brutos, n["dados"], False)]

    sair = sorted(set(sair))
    total = sum(os.path.getsize(a) for a in sair)
    print(f"Retenção: PDFs {n['pdf']} dia(s) · HTML {n['html']} dia(s) · backups {n['backup']} · verificações "
          f"{n['status']} · cópias brutas {n['dados']} dia(s)")
    if not sair:
        print("Nada a limpar.")
        return 0
    for a in sair:
        print(("  [simulação] " if SIMULAR else "  → Lixeira: ") + os.path.relpath(a, PASTA))
    para_lixeira(sair)
    print(f"{len(sair)} arquivo(s), {total / 1024 / 1024:.1f} MB {'seriam liberados' if SIMULAR else 'enviados para a Lixeira'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
