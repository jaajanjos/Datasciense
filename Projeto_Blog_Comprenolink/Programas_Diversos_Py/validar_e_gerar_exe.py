# -*- coding: utf-8 -*-
"""validar_e_gerar_exe.py  (criado em 22/11/2026 a pedido do dono)

FAZ SOZINHO, SEM AJUDA DO CLAUDE: valida o projeto e, SE estiver tudo certo, gera os executáveis (.exe).

Passos:
  1) VALIDA a estrutura (validar_estrutura.py). Se não terminar em "TUDO CERTO", PARA e não gera nada.
  2) Faz backup dos .exe atuais na pasta old_bkp de cada local (nada é apagado).
  3) Gera os 4 executáveis dos relatórios (os mesmos do menu, opção [4]) em Relatorios_Diarios_Anuncios\\programas_fontes_python.
  4) Gera PainelBlog.exe, CentralBlog.exe, atualiza o painel das máquinas no pacote e refaz o 4_PACOTE_OUTRO_PC.zip
     (usa o GERAR_EXE.bat já existente, sem esperar tecla).
  5) VALIDA de novo e confere se cada .exe existe e é novo.
  6) Grava o relatório em Gestao_Anuncios_Blog\\3_DOCUMENTACAO\\GERAR_EXE_AUTOMATICO_AAAA-MM-DD_HHhMM.txt

USO:  python -X utf8 validar_e_gerar_exe.py            (completo)
      python -X utf8 validar_e_gerar_exe.py --so-validar   (só o passo 1, não gera nada)
Código de saída: 0 = tudo certo; 1 = parou ou deu erro (veja o relatório).
Para clique duplo: D:\\Projeto_Blog_Comprenolink\\0_Arquivos_Bat\\6- VALIDAR_E_GERAR_EXE_AUTOMATICO.bat
"""
import datetime as dt
import os
import shutil
import subprocess
import sys

BASE = r"D:\Projeto_Blog_Comprenolink"
REL = os.path.join(BASE, "Relatorios_Diarios_Anuncios", "programas_fontes_python")
GEST = os.path.join(BASE, "Gestao_Anuncios_Blog")
WP = os.path.join(GEST, "1_PROGRAMAS", "Blog_WordPress")
VALIDAR = os.path.join(GEST, "1_PROGRAMAS", "validar_estrutura.py")
DOC = os.path.join(GEST, "3_DOCUMENTACAO")
CARIMBO = dt.datetime.now().strftime("%Y-%m-%d_%Hh%M")
ARQ_LOG = os.path.join(DOC, f"GERAR_EXE_AUTOMATICO_{CARIMBO}.txt")

# (script, nome do exe) - os mesmos da opção [4] do menu principal
EXES_REL = [
    ("3_relatorio_acessos_anuncios.py", "1_relatorio_acessos_anuncios"),
    ("2_gerar_links_anuncios.py", "2_gerar_links_anuncios"),
    ("3_gerar_relatorio_blog_v4.py", "3_gerar_relatorio_blog_v4"),
    ("4_test_blog_seo.py", "4_test_blog_seo"),
]
# onde os .exe finais ficam (para backup e conferência)
EXES_FINAIS = (
    [os.path.join(REL, n + ".exe") for _, n in EXES_REL]
    + [os.path.join(GEST, "CentralBlog.exe"), os.path.join(GEST, "4_PACOTE_OUTRO_PC", "1_PROGRAMAS", "Blog_WordPress", "PainelBlog.exe")]
)

linhas = []


def log(txt=""):
    print(txt, flush=True)
    linhas.append(txt)


def rodar(cmd, cwd=None, stdin_nulo=False):
    """Roda um comando, mostra e guarda a saída. Devolve (código, texto)."""
    p = subprocess.run(cmd, cwd=cwd, stdin=subprocess.DEVNULL if stdin_nulo else None, capture_output=True,
                       text=True, encoding="utf-8", errors="replace", env=dict(os.environ, PYTHONUTF8="1"))
    saida = (p.stdout or "") + (p.stderr or "")
    return p.returncode, saida


def validar(etapa):
    log(f"--- {etapa}: validando a estrutura ---")
    cod, saida = rodar([sys.executable, "-X", "utf8", VALIDAR], cwd=GEST)
    ult = [l for l in saida.splitlines() if l.strip()][-4:]
    for l in ult:
        log("   " + l)
    ok = cod == 0 and "TUDO CERTO" in saida
    log(f"   => {'VALIDAÇÃO OK' if ok else 'VALIDAÇÃO COM PROBLEMA'}")
    return ok


def backup_exes():
    log("--- Backup dos .exe atuais (old_bkp de cada pasta; nada é apagado) ---")
    for exe in EXES_FINAIS:
        if os.path.exists(exe):
            pasta = os.path.join(os.path.dirname(exe), "old_bkp")
            os.makedirs(pasta, exist_ok=True)
            nome, ext = os.path.splitext(os.path.basename(exe))
            destino = os.path.join(pasta, f"{nome}_{CARIMBO}{ext}")
            shutil.copy2(exe, destino)
            log(f"   copiado: {os.path.basename(exe)} -> {destino}")
        else:
            log(f"   (não existia ainda: {os.path.basename(exe)})")


def gerar_exes_relatorios():
    erros = 0
    for script, nome in EXES_REL:
        log(f"--- Gerando {nome}.exe ---")
        cod, saida = rodar([sys.executable, "-m", "PyInstaller", "--noconfirm", "--onefile", "--console", "--name", nome, script], cwd=REL)
        origem = os.path.join(REL, "dist", nome + ".exe")
        destino = os.path.join(REL, nome + ".exe")
        if cod == 0 and os.path.exists(origem):
            try:
                if os.path.exists(destino):
                    os.remove(destino)
                shutil.move(origem, destino)
                log(f"   OK: {destino}")
            except Exception as e:
                erros += 1
                log(f"   ERRO ao mover o .exe (programa aberto? feche e rode de novo): {e}")
        else:
            erros += 1
            log(f"   ERRO ao gerar {nome}.exe (código {cod}). Últimas linhas:")
            for l in saida.splitlines()[-6:]:
                log("      " + l)
    return erros


def gerar_pacotes():
    log("--- Gerando PainelBlog.exe, CentralBlog.exe e refazendo o pacote do outro PC (GERAR_EXE.bat) ---")
    bat = os.path.join(WP, "GERAR_EXE.bat")
    cod, saida = rodar(["cmd.exe", "/c", bat], cwd=WP, stdin_nulo=True)
    for l in [x for x in saida.splitlines() if x.strip()][-8:]:
        log("   " + l)
    ok = "Pronto:" in saida and "ATENCAO" not in saida
    log(f"   => {'OK' if ok else 'COM PROBLEMA: leia as mensagens acima'}")
    return 0 if ok else 1


def conferir_exes(antes):
    log("--- Conferência final dos .exe (precisam existir e ser mais novos que o início) ---")
    erros = 0
    for exe in EXES_FINAIS:
        if os.path.exists(exe) and os.path.getmtime(exe) >= antes:
            log(f"   OK   {os.path.basename(exe)}  ({dt.datetime.fromtimestamp(os.path.getmtime(exe)):%d/%m %H:%M}, {os.path.getsize(exe)//1024} KB)")
        else:
            erros += 1
            log(f"   FALHA {os.path.basename(exe)}: não existe ou não foi atualizado")
    return erros


def main():
    antes = dt.datetime.now().timestamp()
    log(f"VALIDAR E GERAR EXE (automático) - {dt.datetime.now():%d/%m/%Y %H:%M}")
    if not validar("Antes"):
        log("PARADO: a validação tem problema. Nenhum .exe foi gerado ou trocado.")
        return fim(1)
    if "--so-validar" in sys.argv:
        log("Só validação (--so-validar): nada gerado.")
        return fim(0)
    backup_exes()
    erros = gerar_exes_relatorios()
    erros += gerar_pacotes()
    erros += conferir_exes(antes)
    if not validar("Depois"):
        erros += 1
    log("RESULTADO: " + ("TUDO CERTO, executáveis gerados e validados." if erros == 0 else f"{erros} problema(s). Os .exe anteriores estão no old_bkp."))
    return fim(1 if erros else 0)


def fim(cod):
    os.makedirs(DOC, exist_ok=True)
    with open(ARQ_LOG, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print(f"Relatório salvo em: {ARQ_LOG}")
    return cod


if __name__ == "__main__":
    sys.exit(main())
