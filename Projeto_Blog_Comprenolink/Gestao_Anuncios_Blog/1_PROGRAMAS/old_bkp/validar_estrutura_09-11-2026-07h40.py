#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Validação da organização da pasta Manutenção_Blog e do pacote do outro PC.

Confere se cada arquivo está no lugar certo, se os programas funcionam e se nenhuma senha
foi parar onde não deve. NÃO publica nada no site: o único acesso à internet é uma leitura
(teste de conexão), que pode ser pulada com --sem-internet.

Uso:  python validar_estrutura.py [--sem-internet]
Saída: tela + relatório em 3_DOCUMENTACAO\\RELATORIO_VALIDACAO_AAAA-MM-DD_HHhMM.txt
"""
import argparse
import json
import os
import re
import sys
from datetime import datetime

# BLOG_RAIZ: definido pelo CentralBlog.exe (dentro do .exe o __file__ não aponta para a pasta)
RAIZ = os.environ.get("BLOG_RAIZ") or os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PACOTE = os.path.join(RAIZ, "4_PACOTE_OUTRO_PC")
WP = os.path.join(RAIZ, "1_PROGRAMAS", "Blog_WordPress")

# O que precisa existir (caminhos relativos à pasta)
ESTRUTURA_PRINCIPAL = [
    "LEIA-ME_PRIMEIRO.txt",
    "PROCESSO_DE_ATUALIZACAO_MANUTENCAO.pdf",
    "1_ABRIR_PAINEL_BLOG_MAQUINAS.bat",
    "2_TREINAR_BLOG_WORDPRESS_SEM_MEXER_NO_SITE.bat",
    "3_ABRIR_PAINEL_BLOG_WORDPRESS.bat",
    "4_VALIDAR_ESTRUTURA.bat",
    "5_BACKUP_AGORA.bat",
    "6_ATIVAR_ATUALIZACAO_AUTOMATICA.bat",
    "CentralBlog.exe",
    "1_PROGRAMAS/Blog_WordPress/backup_automatico.py",
    "1_PROGRAMAS/Blog_WordPress/publicar_categorias.py",
    "1_PROGRAMAS/Blog_WordPress/atualizar_categorias_auto.py",
    "1_PROGRAMAS/Blog_WordPress/ativar_atualizacao_automatica.ps1",
    "2_DADOS/Blog_WordPress/categorias.json",
    "2_DADOS/Blog_WordPress/paginas_categorias.json",
    "1_PROGRAMAS/validar_estrutura.py",
    "1_PROGRAMAS/central_blog.py",
    "1_PROGRAMAS/Blog_Maquinas/painel-manutencao-anuncios.html",
    "1_PROGRAMAS/Blog_WordPress/painel_blog.py",
    "1_PROGRAMAS/Blog_WordPress/gerenciar_blog.py",
    "1_PROGRAMAS/Blog_WordPress/GERAR_EXE.bat",
    "2_DADOS/Blog_Maquinas/",
    "2_DADOS/Blog_WordPress/wp_credenciais.exemplo.json",
    "2_DADOS/Blog_WordPress/backups/",
    "2_DADOS/Blog_WordPress/treino/pagina_exemplo.html",
    "3_DOCUMENTACAO/Blog_Maquinas/GUIA_PASSO_A_PASSO.txt",
    "3_DOCUMENTACAO/Blog_WordPress/2_snippet_login_painel.php",
    "4_PACOTE_OUTRO_PC/",
    "9_ORIGINAIS_NAO_MEXER/",
]
ESTRUTURA_PACOTE = [
    "LEIA-ME_COMO_INSTALAR_NO_OUTRO_PC.txt",
    "1_ABRIR_PAINEL_BLOG_MAQUINAS.bat",
    "2_ABRIR_PAINEL_BLOG_WORDPRESS.bat",
    "1_PROGRAMAS/Blog_Maquinas/painel-manutencao-anuncios.html",
    "1_PROGRAMAS/Blog_WordPress/PainelBlog.exe",
    "2_DADOS/Blog_Maquinas/",
    "2_DADOS/Blog_WordPress/wp_credenciais.exemplo.json",
    "2_DADOS/Blog_WordPress/backups/",
    "3_DOCUMENTACAO/Blog_Maquinas/GUIA_PASSO_A_PASSO.txt",
]
# Não deve estar no pacote (só partes do navegador e nunca a senha)
PROIBIDOS_PACOTE = ["GerenciarBlog.exe", "wp_credenciais.json", "2_TREINAR_BLOG_WORDPRESS_SEM_MEXER_NO_SITE.bat"]
# Programa/dado fora do lugar: só pode ficar na pasta indicada
SO_EM = {".py": "1_PROGRAMAS", "wp_credenciais.json": "2_DADOS"}

linhas, falhas, avisos = [], [], []


def registra(ok, texto, aviso=False):
    marca = "OK   " if ok else ("AVISO" if aviso else "FALHA")
    linhas.append(f"  [{marca}] {texto}")
    if not ok:
        (avisos if aviso else falhas).append(texto)


def secao(titulo):
    linhas.append("")
    linhas.append(titulo)
    linhas.append("-" * len(titulo))


def confere_lista(base, lista):
    for rel in lista:
        cam = os.path.join(base, *rel.rstrip("/").split("/"))
        existe = os.path.isdir(cam) if rel.endswith("/") else os.path.isfile(cam)
        registra(existe, rel + ("" if existe else "  <- não encontrado"))


def fora_do_lugar(base, ignorar=()):
    for dirpath, dirnames, files in os.walk(base):
        rel_dir = os.path.relpath(dirpath, base)
        if rel_dir.split(os.sep)[0] in ignorar:
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d != "__pycache__"]
        for f in files:
            for chave, pasta in SO_EM.items():
                casa = f.endswith(chave) if chave.startswith(".") else f == chave
                if casa and rel_dir.split(os.sep)[0] != pasta:
                    registra(False, f"{os.path.join(rel_dir, f)} deveria ficar em {pasta}\\")


def main(argv=None):
    linhas.clear(); falhas.clear(); avisos.clear()  # a janela central pode rodar várias vezes
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--sem-internet", action="store_true", help="não faz o teste de conexão com o site")
    args = ap.parse_args(argv)
    agora = datetime.now()
    linhas.append("VALIDAÇÃO DA ESTRUTURA - MANUTENÇÃO DOS BLOGS")
    linhas.append(f"Data: {agora:%d/%m/%Y %H:%M}    Pasta: {RAIZ}")

    secao("1. Estrutura da pasta principal")
    confere_lista(RAIZ, ESTRUTURA_PRINCIPAL)
    fora_do_lugar(RAIZ, ignorar=("4_PACOTE_OUTRO_PC", "9_ORIGINAIS_NAO_MEXER"))

    secao("2. Estrutura do pacote do outro PC (só partes do navegador)")
    confere_lista(PACOTE, ESTRUTURA_PACOTE)
    for dirpath, _, files in os.walk(PACOTE):
        for f in files:
            if f in PROIBIDOS_PACOTE:
                registra(False, f"{os.path.relpath(os.path.join(dirpath, f), PACOTE)} não deveria estar no pacote")
    zipf = PACOTE + ".zip"
    if os.path.isfile(zipf):
        novo = max(os.path.getmtime(os.path.join(d, f)) for d, _, fs in os.walk(PACOTE) for f in fs)
        registra(os.path.getmtime(zipf) >= novo - 2, "4_PACOTE_OUTRO_PC.zip atualizado com a pasta"
                 + ("" if os.path.getmtime(zipf) >= novo - 2 else "  <- refaça o .zip"), aviso=True)
    else:
        registra(False, "4_PACOTE_OUTRO_PC.zip não existe (gere para levar no pendrive)", aviso=True)
    zip_atu = os.path.join(RAIZ, "4_ATUALIZAR_OUTRO_PC.zip")
    if os.path.isfile(zip_atu):
        import zipfile
        nomes = zipfile.ZipFile(zip_atu).namelist()
        dados = [n for n in nomes if "/2_DADOS/" in n or n.endswith("wp_credenciais.json")]
        registra(not dados and any(n.endswith("/ATUALIZAR_AQUI.bat") for n in nomes)
                 and any(n.endswith("/arquivos/1_PROGRAMAS/Blog_WordPress/PainelBlog.exe") for n in nomes),
                 "4_ATUALIZAR_OUTRO_PC.zip só com programas (sem 2_DADOS nem senha)" + (f": {dados[:3]}" if dados else ""))
        prog = max(os.path.getmtime(os.path.join(d, f)) for d, _, fs in os.walk(PACOTE) for f in fs
                   if os.sep + "2_DADOS" not in d)
        atual = os.path.getmtime(zip_atu) >= prog - 2
        registra(atual, "4_ATUALIZAR_OUTRO_PC.zip atualizado com a pasta" + ("" if atual else "  <- rode o GERAR_EXE.bat"),
                 aviso=True)
    else:
        registra(False, "4_ATUALIZAR_OUTRO_PC.zip não existe (rode o GERAR_EXE.bat)", aviso=True)
    src = [os.path.join(WP, f) for f in ("painel_blog.py", "gerenciar_blog.py")]
    for exe, extra in ((os.path.join(PACOTE, "1_PROGRAMAS", "Blog_WordPress", "PainelBlog.exe"), []),
                       (os.path.join(RAIZ, "CentralBlog.exe"),
                        [os.path.join(RAIZ, "1_PROGRAMAS", f) for f in ("central_blog.py", "validar_estrutura.py")])):
        fontes = [s for s in src + extra if os.path.isfile(s)]
        if os.path.isfile(exe) and fontes:
            atual = os.path.getmtime(exe) >= max(os.path.getmtime(s) for s in fontes) - 2
            registra(atual, f"{os.path.basename(exe)} gerado depois da última mudança nos .py"
                     + ("" if atual else "  <- rode 1_PROGRAMAS\\Blog_WordPress\\GERAR_EXE.bat"), aviso=True)

    secao("3. Programas (sem mexer no site)")
    sys.path.insert(0, WP)
    try:
        import gerenciar_blog as gb
        esperado = os.path.join(RAIZ, "2_DADOS", "Blog_WordPress")
        registra(os.path.normcase(gb.PASTA_DADOS) == os.path.normcase(esperado), "gerenciar_blog usa a pasta 2_DADOS\\Blog_WordPress")
        do_pacote = gb.pasta_dados_de(os.path.join(PACOTE, "1_PROGRAMAS", "Blog_WordPress"))
        registra(os.path.normcase(os.path.normpath(do_pacote)) == os.path.normcase(os.path.normpath(esperado)),
                 "painel do pacote, rodando neste PC, salva senha e backups no 2_DADOS principal")
        treino = os.path.join(RAIZ, "2_DADOS", "Blog_WordPress", "treino", "pagina_exemplo.html")
        with open(treino, encoding="utf-8-sig") as f:
            pagina = f.read()
        itens = gb.itens(pagina)
        registra(len(itens) > 0 and not gb.verificar(pagina), f"modo treino lê a cópia local ({len(itens)} produtos, estrutura OK)")
        novo, _ = gb.editar_item(pagina, 1, {"desc": "Teste da validação."})
        registra(gb.itens(novo)[0]["desc"] == "Teste da validação." and not gb.verificar(novo),
                 "edição simulada (só na memória) mantém a página consistente")
        novo, total = gb.remover_item(pagina, 1)
        novo = gb.normalizar(novo, "x")[0]
        registra(total == len(itens) - 1 and [x["n"] for x in gb.itens(novo)] == list(range(1, total + 1))
                 and not gb.verificar(novo), "remoção simulada (só na memória) renumera certo")
    except Exception as e:  # noqa: BLE001
        registra(False, f"gerenciar_blog: {type(e).__name__}: {e}")
    try:
        src_painel = open(os.path.join(WP, "painel_blog.py"), encoding="utf-8").read()
        for trecho, desc in (("SO_EXCLUSIVEADDRUSE", "painel não abre duas vezes na mesma porta"),
                             ("Tem certeza que você quer remover?", "remover pede confirmação"),
                             ("function mostrarForm", "Editar abre o formulário na tela"),
                             ("[A-Za-z0-9]{24}", "painel recusa senha que não é de aplicativo")):
            registra(trecho in src_painel, desc)
        compile(src_painel, "painel_blog.py", "exec")
        registra(True, "painel_blog.py sem erro de sintaxe")
    except Exception as e:  # noqa: BLE001
        registra(False, f"painel_blog.py: {e}")
    html_maq = open(os.path.join(RAIZ, "1_PROGRAMAS", "Blog_Maquinas", "painel-manutencao-anuncios.html"), encoding="utf-8").read()
    registra("Incluir novo produto" in html_maq and "function gerar()" in html_maq, "painel do blog das máquinas completo")
    try:
        registra('class="preco"' not in html_maq and "precoCard" not in html_maq, "painel das máquinas gera o blog sem preço")
        teste = gb.montar_secao(1, {"nome": "X", "link": "https://meli.la/x", "preco": "R$ 1,00"}, True)
        registra("product-price" not in teste and not re.search(r"R\$\s*\d", teste), "anúncio novo do WordPress sai sem preço")
    except Exception as e:  # noqa: BLE001
        registra(False, f"sem preço: {e}")
    copia = os.path.join(PACOTE, "1_PROGRAMAS", "Blog_Maquinas", "painel-manutencao-anuncios.html")
    if os.path.isfile(copia):
        registra(open(copia, encoding="utf-8").read() == html_maq, "painel das máquinas do pacote igual ao principal"
                 + ("" if open(copia, encoding="utf-8").read() == html_maq else "  <- rode GERAR_EXE.bat"), aviso=True)

    log = os.path.join(RAIZ, "2_DADOS", "Blog_WordPress", "backups", "automatico", "backup_automatico.log")
    if os.path.isfile(log):
        minutos = (datetime.now().timestamp() - os.path.getmtime(log)) / 60
        ultima_linha = open(log, encoding="utf-8").read().strip().splitlines()[-1]
        registra(minutos < 90 and "ERRO" not in ultima_linha,
                 f"backup automático rodou há {minutos:.0f} min: {ultima_linha[21:][:70]}"
                 + ("" if minutos < 90 else "  <- confira a tarefa 'Backup automatico blog comprenolink' no Agendador"), aviso=True)
    else:
        registra(False, "backup automático ainda não rodou (rode 5_BACKUP_AGORA.bat)", aviso=True)

    log = os.path.join(RAIZ, "2_DADOS", "Blog_WordPress", "atualizar_categorias.log")
    if os.path.isfile(log):
        horas = (datetime.now().timestamp() - os.path.getmtime(log)) / 3600
        ultima_linha = open(log, encoding="utf-8").read().strip().splitlines()[-1]
        registra(horas < 4 and "ERRO" not in ultima_linha,
                 f"atualização automática das categorias rodou há {horas:.1f} h: {ultima_linha[17:][:70]}"
                 + ("" if horas < 4 else "  <- rode 6_ATIVAR_ATUALIZACAO_AUTOMATICA.bat"), aviso=True)
    else:
        registra(False, "atualização automática das categorias ainda não rodou (rode 6_ATIVAR_ATUALIZACAO_AUTOMATICA.bat)", aviso=True)

    secao("4. Senha e segurança")
    cred = os.path.join(RAIZ, "2_DADOS", "Blog_WordPress", "wp_credenciais.json")
    if os.path.isfile(cred):
        c = json.load(open(cred, encoding="utf-8-sig"))
        senha = (c.get("senha_aplicativo") or "").replace(" ", "")
        registra(bool(re.fullmatch(r"[A-Za-z0-9]{24}", senha)), "senha salva tem formato de senha de aplicativo (24 caracteres)")
        registra(" " not in (c.get("usuario") or "") and bool(c.get("usuario")), f"usuário salvo: {c.get('usuario')}")
    else:
        registra(False, "wp_credenciais.json ainda não existe (abra o atalho 3 e cole a senha de aplicativo)", aviso=True)
    soltos = [os.path.relpath(os.path.join(d, f), RAIZ) for d, _, fs in os.walk(RAIZ) for f in fs
              if f == "wp_credenciais.json" and os.path.normcase(os.path.join(d, f)) != os.path.normcase(cred)]
    registra(not soltos, "nenhuma cópia extra do arquivo de senha" + (f": {soltos}" if soltos else ""))

    secao("5. Conexão com o site (só leitura)")
    if args.sem_internet:
        registra(True, "pulado (--sem-internet)", aviso=True)
    elif os.path.isfile(cred):
        # Chama direto (sem subprocesso) para funcionar também dentro do CentralBlog.exe
        try:
            import gerenciar_blog as gb
            r = gb.testar_conexao(gb.carregar_config())
            registra(not r["problemas"], f"WordPress aceita o login e o painel pode editar a página do guia "
                                         f"({r['total_itens']} produtos)")
            import urllib.request
            req = urllib.request.Request(r["link"] + ("&" if "?" in r["link"] else "?") + "validar=1",
                                         headers={"User-Agent": "ValidarEstrutura/1.0"})
            pagina = urllib.request.urlopen(req, timeout=60).read().decode("utf-8", "replace")
            # todo produto do guia precisa cair numa categoria (senão não aparece nas páginas de categoria)
            from gerar_esboco_categorias import carrega_arvore, classifica
            arv = carrega_arvore()
            sem_cat = [f'{x["n"]} {x["nome"][:30]}' for x in gb.itens(gb.baixar_pagina(gb.carregar_config()).conteudo)
                       if not classifica(x, arv)[0]]
            registra(not sem_cat, "todos os produtos do guia têm categoria" + (f"  <- sem categoria: {sem_cat} (peça 'gerar as categorias')" if sem_cat else ""))
            ids_cat = os.path.join(gb.PASTA_DADOS, "paginas_categorias.json")
            if os.path.isfile(ids_cat):
                for slug in json.load(open(ids_cat, encoding="utf-8")):
                    try:
                        st = urllib.request.urlopen(urllib.request.Request(f"https://comprenolink.net/{slug}/?validar=1",
                                                    headers={"User-Agent": "ValidarEstrutura/1.0"}), timeout=60).status
                    except Exception as ex:  # noqa: BLE001
                        st = str(ex)[:40]
                    registra(st == 200, f"página /{slug}/ no ar" + ("" if st == 200 else f"  <- {st}"))
            corpo = pagina[pagina.find("</head>"):]
            precos = len(re.findall(r'<div class="[^"]*product-price">', corpo))
            botoes = len(re.findall(r"product-buy-button", corpo))
            registra(precos == 0 and botoes > 0, f"site sem preço nos cartões ({botoes} cartões com botão)"
                     + ("" if precos == 0 else f"  <- {precos} cartões com preço: confira o snippet 'Sem preço nos cartões'"))
        except Exception as e:  # noqa: BLE001
            registra(False, f"WordPress aceita o login e o painel pode editar a página do guia  <- {str(e)[:160]}")
    else:
        registra(False, "pulado: falta a senha de aplicativo", aviso=True)

    linhas.append("")
    linhas.append("RESULTADO: " + ("TUDO CERTO" if not falhas else f"{len(falhas)} FALHA(S)")
                  + (f"  ({len(avisos)} aviso(s))" if avisos else ""))
    texto = "\n".join(linhas)
    print(texto)
    rel = os.path.join(RAIZ, "3_DOCUMENTACAO", f"RELATORIO_VALIDACAO_{agora:%Y-%m-%d_%Hh%M}.txt")
    with open(rel, "w", encoding="utf-8") as f:
        f.write(texto + "\n")
    print(f"\nRelatório salvo em: {rel}")
    return 1 if falhas else 0


if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        pass
    sys.exit(main())
