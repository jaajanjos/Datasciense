# -*- coding: utf-8 -*-
"""ETAPA 1 - Verifica no Mercado Livre a situação de todos os anúncios do guia (ativo/pausado/removido) e gera o
relatorio_acessos_anuncios_AAAA-MM-DD_HHhMM.html em Relatorios_Diarios_Anuncios\\_historico_relatorios.

Reaproveita o 3_relatorio_acessos_anuncios.py do painel (o mesmo código do .exe), sem copiar nada.
Uso:  python 1_verificar_e_relatorio.py                 (verifica tudo agora no ML: ~10 min com 213 anúncios)
      python 1_verificar_e_relatorio.py --sem-verificar (usa a última verificação gravada; rápido)
"""
import glob
import os
import sys

import comum


def main():
    sem_verificar = "--sem-verificar" in sys.argv
    c = comum.cfg()
    comum.abrir_log("atualiza")
    comum.titulo("ETAPA 1 - Verificar anúncios no ML e gerar o relatório de acessos")
    pasta_hist = os.path.join(c["pasta_relatorios"], "_historico_relatorios")
    antes = set(glob.glob(os.path.join(pasta_hist, "relatorio_acessos_anuncios_*.html")))
    cmd = [sys.executable, "-X", "utf8", c["programa_relatorio"],
           "--sem-verificar-anuncios" if sem_verificar else "--verificar-anuncios"]
    codigo = comum.rodar(cmd, cwd=c["pasta_fontes_painel"], tempo_limite=60 * 60)
    novos = sorted(set(glob.glob(os.path.join(pasta_hist, "relatorio_acessos_anuncios_*.html"))) - antes)
    if codigo != 0 or not novos:
        comum.log("ERRO: o relatório de acessos não foi gerado (veja as mensagens acima).")
        return 1
    comum.log(f"Relatório gerado: {novos[-1]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
