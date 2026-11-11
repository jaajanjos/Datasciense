import os
from datetime import datetime

# Diretório raiz do projeto
RAIZ_PROJETO = r"D:\Projeto_Blog_Comprenolink"
ARQUIVO_SAIDA = os.path.join(RAIZ_PROJETO, "arquivo_Projeto_Comprenolink.md")

# Extensões de arquivos lidos na íntegra (inclui scripts Python e configurações)
EXTENSOES_LEITURA = {".py", ".md", ".txt", ".json", ".yaml", ".yml", ".ini", ".env", ".env.example", ".bat", ".ps1", ".sh"}

# Pastas e arquivos ignorados
IGNORAR_PASTAS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache", ".idea", ".vscode", "node_modules", "dist", "build"}
IGNORAR_ARQUIVOS = {"arquivo_Projeto_Comprenolink.md", "gerar_inventario.py"}

def gerar_arvore(dir_path, prefix=""):
    """Gera a representação visual da estrutura de pastas e arquivos."""
    linhas = []
    try:
        itens = sorted(os.listdir(dir_path))
    except PermissionError:
        return []
    
    itens = [i for i in itens if i not in IGNORAR_PASTAS and i not in IGNORAR_ARQUIVOS]
    for index, item in enumerate(itens):
        caminho_completo = os.path.join(dir_path, item)
        ultimo = (index == len(itens) - 1)
        conector = "└── " if ultimo else "├── "
        linhas.append(f"{prefix}{conector}{item}")
        
        if os.path.isdir(caminho_completo):
            extensao_prefix = "    " if ultimo else "│   "
            linhas.extend(gerar_arvore(caminho_completo, prefix + extensao_prefix))
    return linhas

def analisar_execucao_python(caminho_relativo, conteudo):
    """Mapeia o modo provável de execução de cada script Python."""
    dicas_execucao = []
    if "if __name__ == '__main__':" in conteudo or 'if __name__ == "__main__":':
        dicas_execucao.append(f"`python {caminho_relativo}`")
    if "import streamlit" in conteudo:
        dicas_execucao.append(f"`streamlit run {caminho_relativo}`")
    if "import flask" in conteudo or "import fastapi" in conteudo:
        dicas_execucao.append("API/Servidor Web")
    if "schedule" in conteudo or "apscheduler" in conteudo:
        dicas_execucao.append("Rotina Agendada (Cron / Agendador de Tarefas)")
    
    if not dicas_execucao:
        dicas_execucao.append(f"`python {caminho_relativo}` (Módulo)")
    return dicas_execucao

def executar_auditoria():
    data_execucao = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    programas_python = []
    
    with open(ARQUIVO_SAIDA, "w", encoding="utf-8") as out:
        # 1. Cabeçalho Principal
        out.write("# AUDITORIA E INVENTÁRIO SISTÊMICO COMPLETO DO PROJETO\n\n")
        out.write(f"- **Projeto:** `Projeto_Blog_Comprenolink`\n")
        out.write(f"- **Caminho Raiz:** `{RAIZ_PROJETO}`\n")
        out.write(f"- **Data de Geração:** `{data_execucao}`\n\n")
        out.write("---\n\n")
        
        # 2. Árvore de Diretórios
        out.write("## 1. Mapeamento da Estrutura de Pastas e Arquivos\n\n")
        out.write("```text\n")
        out.write("D:\\Projeto_Blog_Comprenolink\n")
        linhas_arvore = gerar_arvore(RAIZ_PROJETO)
        out.write("\n".join(linhas_arvore) + "\n")
        out.write("```\n\n")
        out.write("---\n\n")
        
        # 3. Leitura e Inventário Detalhado
        out.write("## 2. Inventário Detalhado, Conteúdo e Módulos Python\n\n")
        
        contador_arquivos = 0
        for raiz, pastas, arquivos in os.walk(RAIZ_PROJETO):
            pastas[:] = [p for p in pastas if p not in IGNORAR_PASTAS]
            
            for arq in sorted(arquivos):
                if arq in IGNORAR_ARQUIVOS:
                    continue
                
                caminho_completo = os.path.join(raiz, arq)
                rel_path = os.path.relpath(caminho_completo, RAIZ_PROJETO)
                _, ext = os.path.splitext(arq)
                
                contador_arquivos += 1
                tamanho_kb = os.path.getsize(caminho_completo) / 1024
                
                out.write(f"### 📄 Arquivo: `{rel_path}`\n")
                out.write(f"- **Caminho Absoluto:** `{caminho_completo}`\n")
                out.write(f"- **Tamanho:** `{tamanho_kb:.2f} KB`\n")
                out.write(f"- **Extensão:** `{ext}`\n\n")
                
                if ext.lower() in EXTENSOES_LEITURA:
                    lang = "python" if ext.lower() == ".py" else ext.replace(".", "")
                    try:
                        with open(caminho_completo, "r", encoding="utf-8") as f:
                            conteudo = f.read()
                    except UnicodeDecodeError:
                        try:
                            with open(caminho_completo, "r", encoding="latin-1") as f:
                                conteudo = f.read()
                        except Exception as e:
                            conteudo = f"# ERRO ao ler arquivo: {e}"
                    except Exception as e:
                        conteudo = f"# ERRO ao ler arquivo: {e}"
                    
                    if ext.lower() == ".py":
                        exec_info = analisar_execucao_python(rel_path, conteudo)
                        programas_python.append({
                            "rel_path": rel_path,
                            "full_path": caminho_completo,
                            "size": f"{tamanho_kb:.2f} KB",
                            "exec_info": exec_info
                        })
                        out.write("**Instruções de Execução:**\n")
                        for info in exec_info:
                            out.write(f"- {info}\n")
                        out.write("\n")

                    out.write(f"```{lang}\n")
                    out.write(conteudo if conteudo.strip() else "# [Arquivo Vazio]")
                    out.write("\n```\n\n")
                else:
                    out.write("*[Conteúdo binário ou não listado para leitura direta]*\n\n")
                
                out.write("---\n\n")
        
        # 4. Resumo Exclusivo dos Programas Python
        out.write("## 3. Resumo dos Programas Python (Localização e Execução)\n\n")
        if programas_python:
            out.write("| Script Python | Localização Relativa | Tamanho | Como Executar |\n")
            out.write("| :--- | :--- | :--- | :--- |\n")
            for py in programas_python:
                exec_str = "<br>".join(py["exec_info"])
                out.write(f"| `{os.path.basename(py['rel_path'])}` | `{py['rel_path']}` | `{py['size']}` | {exec_str} |\n")
            out.write("\n")
        else:
            out.write("Nenhum arquivo `.py` encontrado no momento da varredura.\n\n")

        # 5. Resumo Final
        out.write("## 4. Resumo Geral da Auditoria\n\n")
        out.write(f"- Total de arquivos mapeados/processados: **{contador_arquivos}**\n")
        out.write(f"- Scripts Python catalogados: **{len(programas_python)}**\n")
        out.write("- Arquivo consolidado pronto para fornecimento ao Copilot/IA.\n")

    print(f"✅ Inventário atualizado com sucesso em: {ARQUIVO_SAIDA}")

if __name__ == "__main__":
    executar_auditoria()