# -*- coding: utf-8 -*-
"""Executa o processo completo, na ordem:
  1 verificar anúncios no ML + relatório de acessos (HTML)
  2 lista do que precisa de substituto
  3 substituição com o Claude (IA + seu Chrome logado no ML Afiliados)
  4 troca no guia do blog (com backup da página)
  5 relatório final + painel (PDF) + planilha + resumo

Uso:  python 0_executar_tudo.py                  (completo, publica no blog)
      python 0_executar_tudo.py --simular        (não chama o Claude, não publica e não roda o painel)
      python 0_executar_tudo.py --sem-verificar  (usa a última verificação do ML; mais rápido)
      python 0_executar_tudo.py --sem-claude     (faz tudo menos a substituição: relatório + painel)
"""
import os
import subprocess
import sys

import comum

ETAPAS = ["1_verificar_e_relatorio.py", "2_pendencias_substituicao.py", "3_substituir_com_claude.py",
          "4_aplicar_no_blog.py", "5_painel_e_resumo.py"]


def etapa(nome, *extra):
    return subprocess.call([sys.executable, "-X", "utf8", os.path.join(comum.AQUI, nome), *extra], cwd=comum.AQUI,
                           env=dict(os.environ, PYTHONUTF8="1"))


def main():
    a = sys.argv[1:]
    simular, sem_claude = "--simular" in a, "--sem-claude" in a
    caminho_log = comum.abrir_log("atualiza")
    comum.titulo("ATUALIZAÇÃO AUTOMÁTICA DOS ANÚNCIOS - início" + (" [SIMULAÇÃO]" if simular else ""))
    comum.log(f"Log: {caminho_log}")
    sim = ["--simular"] if simular else []

    if etapa(ETAPAS[0], *(["--sem-verificar"] if "--sem-verificar" in a or simular else [])) != 0:
        comum.log("PARADO: a etapa 1 falhou (relatório não gerado). Nada foi alterado no blog.")
        return 1
    if etapa(ETAPAS[1]) != 0:
        comum.log("PARADO: a etapa 2 falhou. Nada foi alterado no blog.")
        return 1
    erro = 0
    if sem_claude:
        comum.log("Substituição pulada (--sem-claude).")
    else:
        r3 = etapa(ETAPAS[2], *sim)
        if r3 == 0:
            erro |= etapa(ETAPAS[3], *sim)
        else:
            erro = 1
            comum.log("A substituição não foi feita (veja acima). O painel será atualizado mesmo assim.")
    erro |= etapa(ETAPAS[4], *sim)
    comum.titulo("FIM" + (" - com avisos/erros: veja o log" if erro else " - tudo OK"))
    comum.log(f"Resumo: {comum.ARQ_RESUMO}")
    return 1 if erro else 0


if __name__ == "__main__":
    sys.exit(main())
