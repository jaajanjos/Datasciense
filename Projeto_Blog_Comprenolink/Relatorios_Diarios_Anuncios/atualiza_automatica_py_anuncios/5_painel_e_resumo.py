# -*- coding: utf-8 -*-
"""ETAPA 5 - Fecha o dia: se houve troca no blog, gera o relatório de acessos de novo (verificando os anúncios no ML,
para confirmar os links novos); depois roda o ATUALIZAR_PAINEL.bat (planilha "Painel de  Controle de Acesso.xlsx" e
Painel_conversao_performance_AAAA-MM-DD_HHhMM.pdf) e grava o resumo_ultima_execucao.txt.

Uso:  python 5_painel_e_resumo.py            (executa)
      python 5_painel_e_resumo.py --simular  (não roda o painel; só monta o resumo com o que já existe)
      python 5_painel_e_resumo.py --abrir    (abre o PDF do painel no final)
"""
import csv
import glob
import os
import sys
from datetime import datetime

import comum


def mais_novo(padrao):
    arqs = glob.glob(padrao)
    return max(arqs, key=os.path.getmtime) if arqs else ""


def trocas_de_hoje():
    if not os.path.exists(comum.ARQ_HISTORICO):
        return []
    hoje = datetime.now().strftime("%Y-%m-%d")
    with open(comum.ARQ_HISTORICO, encoding="utf-8-sig", newline="") as f:
        return [r for r in csv.DictReader(f, delimiter=";") if r["data"].startswith(hoje)]


def main():
    simular = "--simular" in sys.argv
    c = comum.cfg()
    comum.abrir_log("atualiza")
    comum.titulo("ETAPA 5 - Relatório final, painel de conversão (PDF) e planilha de controle"
                 + (" [SIMULAÇÃO]" if simular else ""))
    rel_dir = c["pasta_relatorios"]
    publicadas = [r for r in trocas_de_hoje() if r["modo"] == "real" and r["resultado"] == "publicado"]
    codigo = 0
    if not simular:
        if publicadas:
            comum.log(f"{len(publicadas)} troca(s) publicada(s) hoje: gerando o relatório de novo e verificando os "
                      "anúncios no ML (confirma os links novos; ~10 min).")
            codigo = comum.rodar([sys.executable, "-X", "utf8", c["programa_relatorio"], "--verificar-anuncios"],
                                 cwd=c["pasta_fontes_painel"], tempo_limite=60 * 60)
        comum.log("Atualizando o painel (planilha + PDF). A verificação já foi feita: etapa 1 do .bat será pulada.")
        codigo |= comum.rodar(["cmd.exe", "/c", os.path.join(c["pasta_fontes_painel"], c["bat_painel"])],
                              cwd=c["pasta_fontes_painel"],
                              env_extra={"PAINEL_SEM_VERIFICAR": "1", "PAINEL_NAO_ABRIR": "1"},
                              tempo_limite=30 * 60)
    else:
        comum.log("[SIMULAÇÃO] Painel não executado.")

    pend = comum.ler_json(comum.ARQ_PENDENCIAS, {}) or {}
    subs = comum.ler_json(comum.ARQ_SUBSTITUICOES, {}) or {}
    html = mais_novo(os.path.join(rel_dir, "_historico_relatorios", "relatorio_acessos_anuncios_*.html"))
    pdf = mais_novo(os.path.join(rel_dir, "Painel_conversao_performance_*.pdf"))
    xlsx = os.path.join(rel_dir, "Painel de  Controle de Acesso.xlsx")
    linhas = [
        f"RESUMO DA ATUALIZAÇÃO AUTOMÁTICA DOS ANÚNCIOS - {datetime.now():%d/%m/%Y %H:%M}" + (" (SIMULAÇÃO)" if simular else ""),
        "",
        f"Última verificação no ML ......... {pend.get('ultima_verificacao_ml', '-')}",
        f"Anúncios ativos ................. {pend.get('anuncios_ativos', '-')} de {pend.get('anuncios_total', '-')}",
        f"Precisavam de substituto ........ {len(pend.get('pendentes') or [])}",
        f"Substituições válidas (IA) ...... {len(subs.get('substituicoes') or [])}",
        f"Não substituídos ................ {len(subs.get('nao_substituidos') or [])}",
        f"Trocas publicadas hoje no blog .. {len(publicadas)}",
        "",
        "Trocas publicadas hoje (VALIDAR link e produto):",
    ]
    linhas += [f"  item {r['item']}: {r['nome_antigo']} -> {r['nome_novo']} | {r['link_novo']} | {r['preco']} | "
               f"conferir: {r['conferir']}" for r in publicadas] or ["  (nenhuma)"]
    linhas += ["", "Não substituídos (motivo):"]
    linhas += [f"  item {n.get('item')}: {n.get('motivo')}" for n in subs.get("nao_substituidos") or []] or ["  (nenhum)"]
    linhas += ["", "Arquivos do dia:",
               f"  Relatório de acessos: {html or '-'}",
               f"  Painel (PDF) ........ {pdf or '-'}",
               f"  Planilha ............ {xlsx if os.path.exists(xlsx) else '-'}",
               f"  Histórico das trocas  {comum.ARQ_HISTORICO}",
               f"  Log desta execução .. {os.environ.get('ATUALIZA_LOG', '-')}",
               "", "Resultado: " + ("OK" if codigo == 0 else "COM ERRO (veja o log)")]
    if os.path.exists(comum.ARQ_RESUMO):
        comum.old_bkp(comum.ARQ_RESUMO)
    with open(comum.ARQ_RESUMO, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    for l in linhas:
        comum.log(l)
    if "--abrir" in sys.argv and pdf and not simular:
        os.startfile(pdf)
    return 1 if codigo else 0


if __name__ == "__main__":
    sys.exit(main())
