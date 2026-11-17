import os
import sys
import shutil
import subprocess
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
RELATORIOS_DIR = BASE_DIR / "Relatorios_Diarios_Anuncios"
PROGRAMAS_DIR = RELATORIOS_DIR / "programas_fontes_python"
BACKUP_DIR = RELATORIOS_DIR / "_backup_painel"
GESTAO_BLOG_DIR = BASE_DIR / "Gestao_Anuncios_Blog"

def rotacionar_backups(max_backups=5):
    if not BACKUP_DIR.exists(): return
    backups = sorted([f for f in BACKUP_DIR.glob("Painel_*.xlsx")], key=lambda x: x.stat().st_mtime, reverse=True)
    if len(backups) > max_backups:
        for arq in backups[max_backups:]:
            try: arq.unlink()
            except Exception: pass

def executar_bat(env_vars=None):
    bat_path = PROGRAMAS_DIR / "ATUALIZAR_PAINEL.bat"
    if not bat_path.exists():
        print(f"[ERRO] {bat_path} nao encontrado.")
        return
    env = os.environ.copy()
    if env_vars: env.update(env_vars)
    print("\n" + "="*60 + "\n Executando ativacao do painel...\n" + "="*60)
    subprocess.run(["cmd.exe", "/c", str(bat_path)], cwd=PROGRAMAS_DIR, env=env)
    rotacionar_backups(5)

def compilar_script(script_py, nome_exe):
    py_cmd = sys.executable
    print(f"\nCompilando {nome_exe}.exe...")
    subprocess.run([py_cmd, "-m", "PyInstaller", "--noconfirm", "--onefile", "--console", "--name", nome_exe, script_py], cwd=PROGRAMAS_DIR)
    origem = PROGRAMAS_DIR / "dist" / f"{nome_exe}.exe"
    destino = PROGRAMAS_DIR / f"{nome_exe}.exe"
    if origem.exists():
        if destino.exists():
            try: destino.unlink()
            except Exception: pass
        shutil.move(str(origem), str(destino))
        print(f"[OK] Movido para: {destino}")

def menu_compilacao():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("="*60)
        print("    RECOMPILACAO DE EXECUTAVEIS (.EXE) - COMPRENOLINK")
        print("="*60)
        print(" [1] Recompilar 1_relatorio_acessos_anuncios.exe")
        print(" [2] Recompilar 2_gerar_links_anuncios.exe")
        print(" [3] Recompilar 3_gerar_relatorio_blog_v4.exe")
        print(" [4] Recompilar 4_test_blog_seo.exe")
        print(" [5] Recompilar TODOS os 4 Executaveis")
        print(" [0] Voltar ao Menu Principal")
        print("="*60)
        sub_op = input("Opcao: ").strip()
        if sub_op == "1":
            compilar_script("3_relatorio_acessos_anuncios.py", "1_relatorio_acessos_anuncios")
            input("\nENTER...")
        elif sub_op == "2":
            compilar_script("2_gerar_links_anuncios.py", "2_gerar_links_anuncios")
            input("\nENTER...")
        elif sub_op == "3":
            compilar_script("3_gerar_relatorio_blog_v4.py", "3_gerar_relatorio_blog_v4")
            input("\nENTER...")
        elif sub_op == "4":
            compilar_script("4_test_blog_seo.py", "4_test_blog_seo")
            input("\nENTER...")
        elif sub_op == "5":
            compilar_script("3_relatorio_acessos_anuncios.py", "1_relatorio_acessos_anuncios")
            compilar_script("2_gerar_links_anuncios.py", "2_gerar_links_anuncios")
            compilar_script("3_gerar_relatorio_blog_v4.py", "3_gerar_relatorio_blog_v4")
            compilar_script("4_test_blog_seo.py", "4_test_blog_seo")
            print("\n[OK] Compilacao concluida e executaveis movidos!")
            input("\nENTER...")
        elif sub_op == "0": break

def menu_gestao_blog():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("="*60)
        print("    MANUTENCAO E GESTAO DE ANUNCIOS DO BLOG")
        print("="*60)
        print(" [1] Validar Estrutura e Senhas (_VALIDAR_ESTRUTURA.bat)")
        print(" [2] Recompilar e Gerar Pacotes do Blog (GERAR_EXE.bat)")
        print(" [3] Abrir Painel das Maquinas (CentralBlog.exe)")
        print(" [0] Voltar ao Menu Principal")
        print("="*60)
        op_b = input("Opcao: ").strip()
        if op_b == "1":
            bat_val = GESTAO_BLOG_DIR / "4_VALIDAR_ESTRUTURA.bat"
            if bat_val.exists():
                subprocess.run(["cmd.exe", "/c", str(bat_val)], cwd=GESTAO_BLOG_DIR)
            else: print("[ERRO] Ficheiro 4_VALIDAR_ESTRUTURA.bat nao encontrado.")
            input("\nENTER...")
        elif op_b == "2":
            bat_gerar = GESTAO_BLOG_DIR / "1_PROGRAMAS" / "Blog_WordPress" / "GERAR_EXE.bat"
            if bat_gerar.exists():
                subprocess.run(["cmd.exe", "/c", str(bat_gerar)], cwd=bat_gerar.parent)
            else: print("[ERRO] Ficheiro GERAR_EXE.bat nao encontrado.")
            input("\nENTER...")
        elif op_b == "3":
            exe_central = GESTAO_BLOG_DIR / "CentralBlog.exe"
            if exe_central.exists():
                subprocess.Popen([str(exe_central)], cwd=GESTAO_BLOG_DIR)
                print("[OK] CentralBlog iniciado!")
            else: print("[ERRO] CentralBlog.exe nao encontrado.")
            input("\nENTER...")
        elif op_b == "0": break

def exibir_menu():
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        print("="*60)
        print("    GESTAO DO ECOSSISTEMA COMPRENOLINK - MENU PRINCIPAL")
        print(f"    Raiz Ativa: {BASE_DIR}")
        print("="*60)
        print(" [1] Executar Atualizacao Completa (com verificacao ML^)")
        print(" [2] Executar Atualizacao Rapida (sem verificar ML^)")
        print(" [3] Executar Limpeza e Manutencao de Historicos")
        print(" [4] Gestao e Compilacao de Executaveis (.exe^)")
        print(" [5] Gestao de Anuncios e Manutencao do Blog")
        print(" [6] Ver Log da Ultima Execucao")
        print(" [0] Sair")
        print("="*60)
        op = input("Opcao: ").strip()
        if op == "1": executar_bat(); input("\nENTER...")
        elif op == "2": executar_bat({"PAINEL_SEM_VERIFICAR": "1"}); input("\nENTER...")
        elif op == "3":
            script_limpeza = PROGRAMAS_DIR / "7_limpar_historico.py"
            if not script_limpeza.exists(): script_limpeza = PROGRAMAS_DIR / "8_limpar_historico.py"
            subprocess.run([sys.executable, str(script_limpeza)], cwd=PROGRAMAS_DIR)
            rotacionar_backups(5)
            input("\nENTER...")
        elif op == "4": menu_compilacao()
        elif op == "5": menu_gestao_blog()
        elif op == "6":
            log = RELATORIOS_DIR / "log_painel.txt"
            if log.exists():
                print("\n".join(log.read_text(encoding="utf-8", errors="ignore").splitlines()[-30:]))
            else: print("Log nao encontrado.")
            input("\nENTER...")
        elif op == "0": break

if __name__ == "__main__": exibir_menu()
