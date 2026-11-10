#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Backup automático das páginas do blog comprenolink.net (só leitura: não publica nada).

Roda sozinho pelo Agendador de Tarefas do Windows (tarefa "Backup automatico blog comprenolink",
a cada 30 min) e também pode ser rodado à mão (atalho 5_BACKUP_AGORA.bat).
Guarda uma cópia em 2_DADOS\\Blog_WordPress\\backups\\automatico\\ SOMENTE quando a página mudou
desde a última cópia — assim mudanças feitas direto no WordPress também ficam salvas.
Mantém as MANTER cópias mais novas de cada página; as mais antigas são apagadas.

Uso:  python backup_automatico.py [--forcar]     (--forcar = salva mesmo sem mudança)
"""
import glob
import json
import os
import sys
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gerenciar_blog as gb  # noqa: E402

PAGINAS = {5: "guia", 14: "inicio"}
# + páginas de categoria e Black Friday criadas por publicar_categorias.py
_ids = os.path.join(gb.PASTA_DADOS, "paginas_categorias.json")
if os.path.exists(_ids):
    with open(_ids, encoding="utf-8") as _f:
        PAGINAS.update({pid: slug for slug, pid in json.load(_f).items()})
MANTER = 200
PASTA = os.path.join(gb.PASTA_BACKUP, "automatico")
LOG = os.path.join(PASTA, "backup_automatico.log")


def registra(texto):
    os.makedirs(PASTA, exist_ok=True)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(f"{datetime.now():%d/%m/%Y %H:%M:%S}  {texto}\n")
    print(texto)


def ultima(rotulo):
    arqs = sorted(glob.glob(os.path.join(PASTA, f"{rotulo}_*.json")))
    if not arqs:
        return None
    with open(arqs[-1], encoding="utf-8") as f:
        return json.load(f)


def limpa_antigos(rotulo):
    arqs = sorted(glob.glob(os.path.join(PASTA, f"{rotulo}_*.json")))
    for j in arqs[:-MANTER]:
        for f in (j, j[:-5] + ".html"):
            if os.path.exists(f):
                os.remove(f)


def salva(rotulo, conteudo, info):
    base = os.path.join(PASTA, f"{rotulo}_{datetime.now():%Y-%m-%d_%Hh%M%S}")
    with open(base + ".html", "w", encoding="utf-8", newline="") as f:
        f.write(conteudo)
    with open(base + ".json", "w", encoding="utf-8") as f:
        json.dump(info, f, ensure_ascii=False, indent=2)
    limpa_antigos(rotulo)
    return base + ".html"


def main():
    forcar = "--forcar" in sys.argv
    cfg = gb.carregar_config()
    os.makedirs(PASTA, exist_ok=True)
    salvos = 0
    try:
        for pid, rotulo in PAGINAS.items():
            d = gb.requisitar(cfg, "GET", f"/wp-json/wp/v2/pages/{pid}?context=edit")
            info = {"pagina_id": pid, "titulo": d["title"]["raw"], "modificado": d["modified"], "link": d["link"]}
            antes = ultima(rotulo)
            if forcar or not antes or antes.get("modificado") != info["modificado"]:
                arq = salva(rotulo, d["content"]["raw"], info)
                registra(f"{rotulo}: mudou (modificada em {info['modificado']}) -> {os.path.basename(arq)}")
                salvos += 1
        s = gb.requisitar(cfg, "GET", "/wp-json/wp/v2/settings")
        info = {"title": s.get("title"), "description": s.get("description"), "modificado": s.get("description")}
        antes = ultima("configuracoes")
        if forcar or not antes or antes.get("modificado") != info["modificado"]:
            salva("configuracoes", json.dumps(info, ensure_ascii=False, indent=2), info)
            registra("configuracoes (nome/subtítulo do site): mudou -> cópia salva")
            salvos += 1
        if not salvos:
            registra("nada mudou desde a última cópia")
    except Exception as e:  # noqa: BLE001  (sem internet etc.: tenta de novo na próxima vez)
        registra(f"ERRO: {type(e).__name__}: {str(e)[:200]}")
        return 1
    return 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    sys.exit(main())
