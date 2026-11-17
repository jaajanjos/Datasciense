# -*- coding: utf-8 -*-
r"""Copia os 3 ultimos relatorios diarios de anuncios para a pasta de consulta no OneDrive.

Origens (D:):
  - Relatorios_Diarios_Anuncios\Painel_conversao_performance_AAAA-MM-DD_HHhMM.pdf
  - 0- Pendencias\1_Pendencias\graficos_diarios\Graficos_Metas_Anuncios_dd-mm-aa_HHhMM.pdf (e os antigos graficos_DD-MM-AA)
Destino: E:\OneDrive\Projeto_Blog_Comprenolink_Consulta\Relatorios_Diarios_Anuncios
Mantem no destino so os 3 ultimos de cada tipo (apaga apenas as COPIAS antigas desses 2 tipos; as originais em D: ficam).
Uso: python -X utf8 sincronizar_relatorios_diarios.py
"""
import os, re, shutil, sys
from datetime import datetime

ORIGENS = [
    (r"D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios",
     re.compile(r"^Painel_conversao_performance_(\d{4})-(\d\d)-(\d\d)_(\d\d)h(\d\d)\.pdf$"), "ymd"),
    (r"D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\graficos_diarios",
     re.compile(r"^(?:graficos|Graficos_Metas_Anuncios)_(\d\d)-(\d\d)-(\d\d)(?:_(\d\d)h(\d\d))?\.pdf$"), "dmy"),
]
DESTINO = r"E:\OneDrive\Projeto_Blog_Comprenolink_Consulta\Relatorios_Diarios_Anuncios"
MANTER = 3


def chave(m, fmt):
    g = m.groups()
    if fmt == "ymd":
        a, mo, d = int(g[0]), int(g[1]), int(g[2])
    else:
        d, mo, a = int(g[0]), int(g[1]), 2000 + int(g[2])
    hh = int(g[3]) if g[3] else 0
    mm = int(g[4]) if g[4] else 0
    return datetime(a, mo, d, hh, mm)


def main():
    if not os.path.isdir(os.path.dirname(DESTINO)):
        print("Destino indisponivel (E: nao encontrado); nada copiado.")
        return 1
    os.makedirs(DESTINO, exist_ok=True)
    for pasta, rx, fmt in ORIGENS:
        if not os.path.isdir(pasta):
            continue
        itens = []
        for n in os.listdir(pasta):
            m = rx.match(n)
            if m:
                itens.append((chave(m, fmt), n))
        itens.sort()
        ultimos = [n for _, n in itens[-MANTER:]]
        for n in ultimos:
            src, dst = os.path.join(pasta, n), os.path.join(DESTINO, n)
            if not os.path.exists(dst) or os.path.getsize(dst) != os.path.getsize(src):
                shutil.copy2(src, dst)
                print("copiado:", n)
        # apaga so copias antigas do mesmo tipo
        for n in os.listdir(DESTINO):
            if rx.match(n) and n not in ultimos:
                try:
                    os.unlink(os.path.join(DESTINO, n))
                    print("removida copia antiga:", n)
                except OSError as e:
                    print("nao removida (aberta?):", n, e)
    return 0


if __name__ == "__main__":
    sys.exit(main())
