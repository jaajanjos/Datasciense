# -*- coding: utf-8 -*-
"""ETAPA 3 - Substituição com IA: chama o Claude Code (com o Claude in Chrome, no seu Chrome logado no ML Afiliados)
para escolher o substituto de cada anúncio fora do ar, gerar o meli.la e gravar substituicoes_aprovadas.json.
Depois VALIDA o arquivo (campos, link meli.la novo e diferente do antigo, imagem, item pendente).

Requisitos: Chrome aberto com a extensão Claude conectada e logado no ML Afiliados. Usa o seu plano do Claude.
Uso:  python 3_substituir_com_claude.py             (executa)
      python 3_substituir_com_claude.py --simular   (só mostra o que faria; não chama o Claude)
"""
import os
import re
import sys
from datetime import datetime

import comum

CAMPOS = ("item", "link_antigo", "nome", "link", "titulo_anuncio", "preco", "imagem")


def validar(saida, pendentes):
    """Devolve (válidas, recusadas) conferindo cada substituição com a lista de pendentes."""
    por_item = {str(p["item"]): p for p in pendentes}
    validas, recusadas, vistos = [], list(saida.get("nao_substituidos") or []), set()
    for s in saida.get("substituicoes") or []:
        it = str(s.get("item"))
        falta = [c for c in CAMPOS if not str(s.get(c) or "").strip()]
        p = por_item.get(it)
        motivo = None
        if falta:
            motivo = "faltam campos: " + ", ".join(falta)
        elif p is None:
            motivo = "item não está na lista de pendentes"
        elif it in vistos:
            motivo = "item repetido"
        elif s["link_antigo"] != p["link_antigo"]:
            motivo = "link_antigo diferente do que está fora do ar"
        elif not re.match(r"^https://meli\.la/[A-Za-z0-9]+$", s["link"].strip()):
            motivo = f"link não é um meli.la válido: {s['link']}"
        elif s["link"].strip() == (p["link_antigo"] or "").strip():
            motivo = "link novo igual ao antigo (armadilha do catálogo)"
        elif not s["imagem"].startswith("https://"):
            motivo = "imagem sem https"
        if motivo:
            recusadas.append({"item": s.get("item"), "motivo": "recusado pela validação: " + motivo})
        else:
            vistos.add(it)
            validas.append(s)
    return validas, recusadas


def main():
    simular = "--simular" in sys.argv
    c = comum.cfg()
    comum.abrir_log("atualiza")
    comum.titulo("ETAPA 3 - Substituição dos anúncios com o Claude (IA + seu Chrome logado no ML Afiliados)")
    pend = comum.ler_json(comum.ARQ_PENDENCIAS)
    if not pend:
        comum.log("ERRO: pendencias_substituicao.json não existe. Rode a etapa 2 primeiro.")
        return 1
    pendentes = pend.get("pendentes") or []
    if not pendentes:
        comum.log("Nada a substituir hoje (nenhum anúncio fora do ar). Etapa pulada.")
        comum.gravar_json(comum.ARQ_SUBSTITUICOES, {"gerado_em": datetime.now().strftime("%Y-%m-%d %H:%M"),
                                                    "situacao_geral": "nada_a_fazer", "substituicoes": [],
                                                    "nao_substituidos": []})
        return 0
    maximo = int(c.get("max_substituicoes_por_rodada", 10))
    comum.log(f"{len(pendentes)} anúncio(s) para substituir (máximo por rodada: {maximo}).")

    claude = c.get("claude_exe") or "claude"
    if not os.path.exists(claude):
        comum.log(f"ERRO: Claude Code não encontrado em {claude}. Ajuste 'claude_exe' no config_atualiza.json.")
        return 1
    instrucao = (f"Siga exatamente o roteiro do arquivo {comum.ROTEIRO}. A pasta de trabalho é {comum.AQUI}. "
                 f"Leia {comum.ARQ_PENDENCIAS}, processe no máximo MAX={maximo} itens e grave o resultado em "
                 f"{comum.ARQ_SUBSTITUICOES}. Hoje é {datetime.now():%d/%m/%Y %H:%M}.")
    cmd = [claude, "-p", instrucao, "--chrome", "--add-dir", comum.AQUI,
           "--allowedTools", "mcp__claude-in-chrome", "Read", "Write", "Edit", "Glob", "Grep", "ToolSearch",
           "--permission-mode", "acceptEdits"]
    if simular:
        comum.log("[SIMULAÇÃO] O Claude NÃO foi chamado. Comando que seria executado:")
        comum.log("   " + " ".join(f'"{x}"' if " " in x else x for x in cmd))
        return 0

    # guarda o resultado anterior em old_bkp e começa limpo (para nunca reaproveitar substituição velha)
    if os.path.exists(comum.ARQ_SUBSTITUICOES):
        comum.old_bkp(comum.ARQ_SUBSTITUICOES)
        os.remove(comum.ARQ_SUBSTITUICOES)
    inicio = datetime.now()
    # se o programa for chamado de dentro do aplicativo do Claude, não herdar a autenticação interna do app:
    # o Claude Code usa o SEU login (feito com /login no terminal)
    for v in [k for k in os.environ if k.startswith(("ANTHROPIC_", "CLAUDE")) or k in ("USE_LOCAL_OAUTH", "USE_STAGING_OAUTH")]:
        os.environ.pop(v, None)
    codigo = comum.rodar(cmd, cwd=comum.AQUI, tempo_limite=int(c.get("claude_tempo_limite_min", 90)) * 60)
    saida = comum.ler_json(comum.ARQ_SUBSTITUICOES)
    if not saida:
        comum.log(f"ERRO: o Claude terminou (código {codigo}) sem gravar substituicoes_aprovadas.json.")
        comum.log("  Confira: (1) o Claude Code está logado? Abra um terminal, digite  claude  e use /login se pedir "
                  "(mensagem 'Failed to authenticate' no log = login expirado); (2) Chrome aberto, extensão Claude "
                  "conectada e ML Afiliados logado.")
        return 1
    if datetime.fromtimestamp(os.path.getmtime(comum.ARQ_SUBSTITUICOES)) < inicio:
        comum.log("ERRO: substituicoes_aprovadas.json é antigo (não foi gravado nesta rodada).")
        return 1
    if saida.get("situacao_geral") == "navegador_indisponivel":
        comum.log("ATENÇÃO: o Claude não conseguiu usar o navegador (Chrome/extensão/login do ML Afiliados).")
        for n in saida.get("nao_substituidos") or []:
            comum.log(f"   item {n.get('item')}: {n.get('motivo')}")
        return 2

    validas, recusadas = validar(saida, pendentes)
    saida["substituicoes"], saida["nao_substituidos"] = validas, recusadas
    saida["validado_em"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    comum.gravar_json(comum.ARQ_SUBSTITUICOES, saida)
    for s in validas:
        comum.log(f"  OK  item {s['item']}: {s['nome']} · {s['preco']} · {s['link']}")
    for n in recusadas:
        comum.log(f"  --  item {n.get('item')}: {n.get('motivo')}")
    comum.log(f"{len(validas)} substituição(ões) válida(s); {len(recusadas)} não substituído(s).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
