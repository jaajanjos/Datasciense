# -*- coding: utf-8 -*-
"""Funções comuns da rotina atualiza_automatica_py_anuncios (caminhos, log, execução de programas, old_bkp)."""
import json
import os
import shutil
import subprocess
import sys
from datetime import datetime

AQUI = os.path.dirname(os.path.abspath(__file__))
CONFIG = os.path.join(AQUI, "config_atualiza.json")
PASTA_LOGS = os.path.join(AQUI, "logs")
ARQ_PENDENCIAS = os.path.join(AQUI, "pendencias_substituicao.json")
ARQ_SUBSTITUICOES = os.path.join(AQUI, "substituicoes_aprovadas.json")
ARQ_HISTORICO = os.path.join(AQUI, "historico_substituicoes.csv")
ARQ_RESUMO = os.path.join(AQUI, "resumo_ultima_execucao.txt")
ROTEIRO = os.path.join(AQUI, "roteiro_substituicao_claude.md")

try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass


def cfg():
    with open(CONFIG, encoding="utf-8") as f:
        c = json.load(f)
    for chave in ("raiz_projeto", "pasta_relatorios", "pasta_fontes_painel", "gerenciar_blog"):
        if not os.path.exists(c[chave]):
            raise SystemExit(f"ERRO: caminho do config_atualiza.json não existe: {chave} = {c[chave]}")
    return c


def agora(fmt="%d/%m/%Y %H:%M:%S"):
    return datetime.now().strftime(fmt)


_LOG = None


def abrir_log(nome):
    """Abre (ou reaproveita) o log do dia em logs\\."""
    global _LOG
    os.makedirs(PASTA_LOGS, exist_ok=True)
    caminho = os.environ.get("ATUALIZA_LOG") or os.path.join(PASTA_LOGS, f"{nome}_{datetime.now():%Y-%m-%d_%Hh%M}.txt")
    os.environ["ATUALIZA_LOG"] = caminho
    _LOG = open(caminho, "a", encoding="utf-8")
    return caminho


def log(msg=""):
    linha = f"[{agora('%H:%M:%S')}] {msg}" if msg else ""
    print(linha, flush=True)
    if _LOG:
        _LOG.write(linha + "\n")
        _LOG.flush()


def titulo(msg):
    log("=" * 70)
    log(msg)
    log("=" * 70)


def rodar(cmd, cwd=None, env_extra=None, tempo_limite=None):
    """Executa um programa mostrando a saída na tela e gravando no log. Devolve o código de saída."""
    env = dict(os.environ, PYTHONUTF8="1", PYTHONIOENCODING="utf-8")
    env.update(env_extra or {})
    log("Executando: " + " ".join(f'"{c}"' if " " in str(c) else str(c) for c in cmd))
    p = subprocess.Popen(cmd, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                         stdin=subprocess.DEVNULL, text=True, encoding="utf-8", errors="replace")
    try:
        for linha in p.stdout:
            linha = linha.rstrip("\r\n")
            print("   " + linha, flush=True)
            if _LOG:
                _LOG.write("   " + linha + "\n")
        p.wait(timeout=tempo_limite)
    except subprocess.TimeoutExpired:
        p.kill()
        log(f"ERRO: tempo limite de {tempo_limite} s esgotado; programa interrompido.")
        return 124
    if _LOG:
        _LOG.flush()
    log(f"Código de saída: {p.returncode}")
    return p.returncode


def old_bkp(caminho):
    """Regra do dono: antes de alterar um arquivo, copia o original para old_bkp\\ da mesma pasta."""
    if not os.path.exists(caminho):
        return None
    pasta, nome = os.path.split(caminho)
    base, ext = os.path.splitext(nome)
    destino_dir = os.path.join(pasta, "old_bkp")
    os.makedirs(destino_dir, exist_ok=True)
    destino = os.path.join(destino_dir, f"{base}_{datetime.now():%d-%m-%Y-%Hh%M}{ext}")
    n = 2
    while os.path.exists(destino):
        destino = os.path.join(destino_dir, f"{base}_{datetime.now():%d-%m-%Y-%Hh%M}_{n}{ext}")
        n += 1
    shutil.copy2(caminho, destino)
    return destino


def ler_json(caminho, padrao=None):
    if not os.path.exists(caminho):
        return padrao
    with open(caminho, encoding="utf-8-sig") as f:
        return json.load(f)


def gravar_json(caminho, dados):
    old_bkp(caminho)
    with open(caminho, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
