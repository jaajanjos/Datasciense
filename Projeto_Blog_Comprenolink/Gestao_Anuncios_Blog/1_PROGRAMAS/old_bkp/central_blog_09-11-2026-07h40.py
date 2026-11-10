#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
CentralBlog: uma janela só com tudo da manutenção dos blogs (vira CentralBlog.exe, na raiz da pasta).

  1. Painel do blog das máquinas (Google Sites)  -> abre o HTML no navegador
  2. Treinar o blog WordPress (sem mexer no site) -> menu do gerenciar_blog numa janela preta
  3. Painel do blog WordPress                     -> sobe o painel_blog aqui dentro e abre o navegador
  4. Validar a organização                        -> roda validar_estrutura e mostra o resultado

Uso interno: CentralBlog.exe --treino (é como o botão 2 abre a janela preta do treino).
"""
import contextlib
import io
import os
import subprocess
import sys
import threading
import webbrowser

# Pasta Manutenção_Blog: onde está o .exe, ou a pasta acima de 1_PROGRAMAS quando roda pelo .py
if getattr(sys, "frozen", False):
    RAIZ = os.path.dirname(sys.executable)
else:
    RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".."))
PROG = os.path.join(RAIZ, "1_PROGRAMAS")
DADOS_WP = os.path.join(RAIZ, "2_DADOS", "Blog_WordPress")
HTML_MAQUINAS = os.path.join(PROG, "Blog_Maquinas", "painel-manutencao-anuncios.html")
TREINO = os.path.join(DADOS_WP, "treino", "pagina_exemplo.html")

# Antes de importar os módulos: dados do WordPress em 2_DADOS e raiz para a validação
os.environ.setdefault("BLOG_WP_DADOS", DADOS_WP)
os.environ.setdefault("BLOG_RAIZ", RAIZ)
sys.path[:0] = [PROG, os.path.join(PROG, "Blog_WordPress")]

import gerenciar_blog as gb  # noqa: E402
import painel_blog  # noqa: E402
import validar_estrutura  # noqa: E402


# ----------------------------------------------------------------------------- treino (janela preta)
def modo_treino():
    """Roda o menu do gerenciar_blog em modo offline numa janela de console própria."""
    if sys.stdout is None:  # .exe sem console (--windowed): cria a janela preta e liga entrada/saída nela
        import ctypes
        k32 = ctypes.windll.kernel32
        if not k32.GetConsoleWindow():
            k32.AllocConsole()
        k32.SetConsoleTitleW("Treino do blog WordPress - nada é enviado ao site")
        k32.SetConsoleOutputCP(65001)
        ctypes.windll.kernel32.SetConsoleCP(65001)
        sys.stdout = sys.stderr = open("CONOUT$", "w", encoding="utf-8", buffering=1)
        sys.stdin = open("CONIN$", "r", encoding="utf-8")
    print("MODO TREINO: usa uma cópia local do guia. NADA é enviado ao site.")
    print(f"O resultado das alterações fica em {os.path.join(DADOS_WP, 'saida_offline.html')}\n")
    try:
        gb.main(["--offline", TREINO])
    finally:
        input("\nPressione Enter para fechar esta janela...")


# ----------------------------------------------------------------------------- janela central
def janela():
    import tkinter as tk
    from tkinter import messagebox, scrolledtext

    # .exe sem console: o servidor do painel escreve o log de cada pedido em sys.stderr (que seria None)
    if sys.stdout is None:
        sys.stdout = open(os.devnull, "w", encoding="utf-8")
    if sys.stderr is None:
        sys.stderr = open(os.devnull, "w", encoding="utf-8")

    estado = {"painel": None}
    raiz = tk.Tk()
    raiz.title("Central dos Blogs - manutenção")
    raiz.geometry("760x640")
    raiz.minsize(600, 520)
    raiz.configure(bg="#f5f6f7")

    tk.Label(raiz, text="Central dos Blogs", font=("Segoe UI", 20, "bold"), bg="#f5f6f7", fg="#1a2230").pack(pady=(18, 0))
    tk.Label(raiz, text="Clique no que quer fazer. Tudo fica nesta pasta: " + RAIZ, font=("Segoe UI", 9),
             bg="#f5f6f7", fg="#5b6474", wraplength=700).pack(pady=(2, 12))

    status = tk.StringVar(value="Pronto.")

    def abrir_maquinas():
        if not os.path.isfile(HTML_MAQUINAS):
            return messagebox.showerror("Não encontrado", f"Falta o arquivo:\n{HTML_MAQUINAS}")
        os.startfile(HTML_MAQUINAS)  # navegador padrão (o caminho tem "ç" e espaço)
        status.set("Painel do blog das máquinas aberto no navegador.")

    def abrir_treino():
        if not os.path.isfile(TREINO):
            return messagebox.showerror("Não encontrado", f"Falta a cópia de treino:\n{TREINO}")
        if getattr(sys, "frozen", False):  # o próprio .exe cria a janela preta (AllocConsole em modo_treino)
            subprocess.Popen([sys.executable, "--treino"], cwd=RAIZ)
        else:
            subprocess.Popen([sys.executable, os.path.abspath(__file__), "--treino"], cwd=RAIZ,
                             creationflags=getattr(subprocess, "CREATE_NEW_CONSOLE", 0))
        status.set("Modo treino aberto numa janela preta (não mexe no site).")

    def abrir_wordpress():
        url = f"http://127.0.0.1:{painel_blog.PORTA}/"
        if estado["painel"] and estado["painel"].is_alive():
            webbrowser.open(url)
            return status.set("O painel do WordPress já está rodando. Abri o navegador de novo.")
        # painel_blog.main() sobe o servidor (ou só abre o navegador se já houver um painel aberto)
        t = threading.Thread(target=painel_blog.main, daemon=True)
        t.start()
        estado["painel"] = t
        status.set(f"Painel do WordPress rodando em {url}  -  deixe esta janela aberta enquanto usa.")
        btn_wp.configure(text="🔧  Painel do blog WordPress  (rodando - clique para abrir de novo)")

    def validar():
        saida.configure(state="normal")
        saida.delete("1.0", "end")
        saida.insert("end", "Validando... (não publica nada no site)\n")
        saida.configure(state="disabled")
        status.set("Validando a organização...")
        btn_val.configure(state="disabled")

        def trabalho():
            buf = io.StringIO()
            try:
                with contextlib.redirect_stdout(buf):
                    cod = validar_estrutura.main([])
            except Exception as e:  # noqa: BLE001
                cod = 1
                buf.write(f"\nERRO na validação: {type(e).__name__}: {e}\n")
            raiz.after(0, lambda: mostrar(buf.getvalue(), cod))

        threading.Thread(target=trabalho, daemon=True).start()

    def mostrar(texto, cod):
        saida.configure(state="normal")
        saida.delete("1.0", "end")
        for linha in texto.splitlines():
            tag = "ok" if "[OK" in linha else "aviso" if "[AVISO" in linha else "falha" if "[FALHA" in linha else \
                  "titulo" if linha.startswith(("RESULTADO", "VALIDAÇÃO")) else ""
            saida.insert("end", linha + "\n", tag)
        saida.see("1.0")
        saida.configure(state="disabled")
        btn_val.configure(state="normal")
        status.set("Validação: TUDO CERTO." if cod == 0 else "Validação encontrou falhas - veja a lista abaixo.")

    def abrir_pasta():
        os.startfile(RAIZ)

    estilo = dict(font=("Segoe UI", 12, "bold"), anchor="w", padx=16, pady=10, relief="flat", cursor="hand2", bd=0)
    quadro = tk.Frame(raiz, bg="#f5f6f7")
    quadro.pack(fill="x", padx=24)
    botoes = [
        ("🪒  Painel do blog das máquinas  (Google Sites)", "#2c4a6b", abrir_maquinas),
        ("🎓  Treinar o blog WordPress  (sem mexer no site)", "#5b6474", abrir_treino),
        ("🔧  Painel do blog WordPress  (mexe no site)", "#1E8E5A", abrir_wordpress),
        ("✅  Validar a organização", "#a8321f", validar),
    ]
    feitos = []
    for texto, cor, acao in botoes:
        b = tk.Button(quadro, text=texto, bg=cor, fg="white", activebackground=cor, activeforeground="white",
                      command=acao, **estilo)
        b.pack(fill="x", pady=4)
        feitos.append(b)
    btn_wp, btn_val = feitos[2], feitos[3]
    tk.Button(quadro, text="📁  Abrir a pasta", command=abrir_pasta, font=("Segoe UI", 10), relief="groove",
              cursor="hand2").pack(anchor="e", pady=(6, 0))

    tk.Label(raiz, textvariable=status, font=("Segoe UI", 10, "bold"), bg="#f5f6f7", fg="#1a2230",
             wraplength=700, justify="left").pack(fill="x", padx=24, pady=(10, 4))
    saida = scrolledtext.ScrolledText(raiz, font=("Consolas", 9), height=12, state="disabled", wrap="word")
    saida.pack(fill="both", expand=True, padx=24, pady=(0, 18))
    saida.tag_configure("ok", foreground="#1f7a4a")
    saida.tag_configure("aviso", foreground="#9a5a00")
    saida.tag_configure("falha", foreground="#c0392b", font=("Consolas", 9, "bold"))
    saida.tag_configure("titulo", font=("Consolas", 10, "bold"))

    def fechar():
        if estado["painel"] and estado["painel"].is_alive():
            if not messagebox.askyesno("Fechar a Central?", "Fechar esta janela encerra o painel do WordPress "
                                                            "que está aberto no navegador.\n\nFechar mesmo assim?"):
                return
        raiz.destroy()

    raiz.protocol("WM_DELETE_WINDOW", fechar)
    raiz.mainloop()


if __name__ == "__main__":
    if "--treino" in sys.argv:
        modo_treino()
    else:
        janela()
