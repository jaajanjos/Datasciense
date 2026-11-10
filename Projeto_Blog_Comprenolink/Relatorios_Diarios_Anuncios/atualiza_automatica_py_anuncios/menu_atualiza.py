# -*- coding: utf-8 -*-
"""Menu da atualização automática dos anúncios (clique duplo em 0_MENU_ATUALIZA_ANUNCIOS.bat)."""
import glob
import os
import subprocess
import sys

import comum

OPCOES = [
    ("1", "Rodar TUDO (verificar ML, relatório, substituir com o Claude, trocar no blog, painel)", "0_executar_tudo.py", []),
    ("2", "Rodar TUDO usando a última verificação do ML (mais rápido)", "0_executar_tudo.py", ["--sem-verificar"]),
    ("3", "Só relatório + painel (sem substituição)", "0_executar_tudo.py", ["--sem-claude"]),
    ("4", "Só verificar no ML e gerar o relatório de acessos", "1_verificar_e_relatorio.py", []),
    ("5", "Só ver o que precisa de substituto", "2_pendencias_substituicao.py", []),
    ("6", "Só substituir com o Claude e trocar no blog (usa a última lista)", None, []),
    ("7", "Só atualizar o painel (PDF + planilha) e o resumo", "5_painel_e_resumo.py", []),
    ("8", "SIMULAÇÃO completa (não chama o Claude, não publica, não roda o painel)", "0_executar_tudo.py", ["--simular", "--sem-verificar"]),
]


def rodar(prog, extra):
    subprocess.call([sys.executable, "-X", "utf8", os.path.join(comum.AQUI, prog), *extra], cwd=comum.AQUI)


def abrir(caminho):
    if caminho and os.path.exists(caminho):
        os.startfile(caminho)
    else:
        print("Arquivo ainda não existe.")


def main():
    while True:
        os.environ.pop("ATUALIZA_LOG", None)
        print("\n" + "=" * 72)
        print("  ATUALIZAÇÃO AUTOMÁTICA DOS ANÚNCIOS - comprenolink.net")
        print("  Antes da opção 1, 2 ou 6: Chrome aberto, extensão Claude conectada e ML Afiliados logado.")
        print("=" * 72)
        for k, txt, _, _ in OPCOES:
            print(f" [{k}] {txt}")
        print(" [R] Abrir o resumo da última execução")
        print(" [H] Abrir o histórico das trocas (para validar link e produto)")
        print(" [L] Abrir o último log")
        print(" [D] Abrir a documentação (PDF)")
        print(" [0] Sair")
        op = input("\nEscolha: ").strip().upper()
        if op == "0":
            return
        if op == "6":
            rodar("3_substituir_com_claude.py", [])
            os.environ.pop("ATUALIZA_LOG", None)
            rodar("4_aplicar_no_blog.py", [])
        elif op == "R":
            abrir(comum.ARQ_RESUMO)
        elif op == "H":
            abrir(comum.ARQ_HISTORICO)
        elif op == "L":
            logs = glob.glob(os.path.join(comum.PASTA_LOGS, "*.txt"))
            abrir(max(logs, key=os.path.getmtime) if logs else "")
        elif op == "D":
            docs = glob.glob(os.path.join(comum.AQUI, "DOCUMENTACAO_ATUALIZA_ANUNCIOS_*.pdf"))
            abrir(max(docs, key=os.path.getmtime) if docs else "")
        else:
            esc = next((o for o in OPCOES if o[0] == op), None)
            if not esc:
                print("Opção inválida.")
                continue
            rodar(esc[2], esc[3])
        input("\nENTER para voltar ao menu...")


if __name__ == "__main__":
    main()
