"""
Gera o PDF que documenta COMO o 1_relatorio_acessos_anuncios.exe foi gerado.

Saída: Relatorios_Diarios_Anuncios/docs_relatorio_diario_anuncio/
       DOCUMENTACAO_EXECUTAVEL_1_RELATORIO_ACESSOS_DD_MM_AAAA.pdf
Uso:   python 12_gerar_documentacao_exe_pdf.py
Lê dados reais: o .exe instalado (tamanho, data, SHA-256), o .spec desta pasta e, se existir,
a pasta de build do 11_compilar_exe_relatorio.bat (%TEMP%\\build_1_relatorio) para listar o que foi empacotado.
"""
import collections
import hashlib
import importlib
import os
import re
import sys
from datetime import datetime
from xml.sax.saxutils import escape

from reportlab.graphics.shapes import Drawing, Rect, String
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, Preformatted, SimpleDocTemplate, Spacer

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
base = importlib.import_module("9_gerar_documentacao_pdf")
tec = importlib.import_module("10_gerar_documentacao_tecnica_pdf")
P, tabela, HOJE, PASTA_DOCS = base.P, base.tabela, base.HOJE, base.PASTA_DOCS
AZUL, AZUL_CLARO, LARANJA = base.AZUL, base.AZUL_CLARO, base.LARANJA
VERDE, AMAR, ROXO = tec.VERDE, tec.AMAR, tec.ROXO

EXE = "D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios/programas_fontes_python/1_relatorio_acessos_anuncios.exe"
SPEC = os.path.join(AQUI, "1_relatorio_acessos_anuncios.spec")
BUILD = os.path.join(os.environ.get("TEMP", ""), "build_1_relatorio", "work", "1_relatorio_acessos_anuncios")
BKP = "D:/Projeto_Blog_Comprenolink/Programas_Diversos_Py/_backups_claude_"
SAIDA = os.path.join(PASTA_DOCS, HOJE.strftime("DOCUMENTACAO_EXECUTAVEL_1_RELATORIO_ACESSOS_%d_%m_%Y.pdf"))
MONO = ParagraphStyle("mono", fontName="Courier", fontSize=7.3, leading=8.8, backColor=colors.HexColor("#F4F6F8"),
                      borderPadding=5, borderColor=colors.HexColor("#B0B8C4"), borderWidth=0.4)


def rodape(c, doc):
    c.saveState()
    c.setFont("Arial", 7.5)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(1.5 * cm, 0.9 * cm, "comprenolink.net · Documentação do executável 1_relatorio_acessos_anuncios.exe")
    c.drawRightString(landscape(A4)[0] - 1.5 * cm, 0.9 * cm, f"Gerado em {HOJE:%d/%m/%Y %H:%M} · página {doc.page}")
    c.restoreState()


def mb(n):
    return f"{n / 1024 / 1024:.1f} MB".replace(".", ",")


def kb(n):
    return f"{n / 1024:,.0f} KB".replace(",", ".")


def dados_exe():
    st = os.stat(EXE)
    h = hashlib.sha256(open(EXE, "rb").read()).hexdigest()
    return st.st_size, datetime.fromtimestamp(st.st_mtime), h


def versoes():
    v = {"python": sys.version.split()[0]}
    for m in ("PyInstaller", "openpyxl", "numpy", "PIL", "yaml", "psutil"):
        try:
            v[m] = importlib.import_module(m).__version__
        except Exception:
            v[m] = "-"
    return v


def conteudo_build():
    """Lê os TOC do PyInstaller (se a pasta de build ainda existir)."""
    pyz_toc, pkg_toc = os.path.join(BUILD, "PYZ-00.toc"), os.path.join(BUILD, "PKG-00.toc")
    if not (os.path.exists(pyz_toc) and os.path.exists(pkg_toc)):
        return None
    pyz = open(pyz_toc, encoding="utf-8").read()
    mods = re.findall(r"\('([\w\.]+)',\s*'[^']*',\s*'PYMODULE'\)", pyz)
    pkg = re.findall(r"\('([^']+)',\s*'([^']*)',\s*'(\w+)'\)", open(pkg_toc, encoding="utf-8").read())
    itens = []
    for nome, cam, tipo in pkg:
        tam = os.path.getsize(cam) if os.path.exists(cam) else 0
        itens.append((nome, tipo, tam))
    pyz_tam = os.path.getsize(os.path.join(BUILD, "PYZ-00.pyz")) if os.path.exists(os.path.join(BUILD, "PYZ-00.pyz")) else 0
    return {"mods": mods, "top": collections.Counter(m.split(".")[0] for m in mods), "itens": itens,
            "pyz": pyz_tam, "tipos": collections.Counter(t for _, t, _ in itens)}


def diagrama_metodo():
    d = Drawing(760, 150)
    passos = [
        ("1. Fontes .py", ["3_relatorio (entrada)", "6_verificar (oculto)", "+ bibliotecas"], AMAR),
        ("2. Análise", ["PyInstaller segue", "todos os import", "(modulegraph)"], ROXO),
        ("3. PYZ", ["bytecode .pyc", "comprimido (zlib)", "de 700+ módulos"], ROXO),
        ("4. PKG", ["PYZ + DLLs + .pyd", "+ python314.dll", "+ base_library.zip"], ROXO),
        ("5. EXE", ["bootloader run.exe", "+ PKG anexado", "= 1 arquivo só"], VERDE),
        ("6. Instalar", ["copiar para", "Relatorios_Diarios_Anuncios\\programas_fontes_python", "(backup do antigo)"], LARANJA),
    ]
    w, gap = 112, 17
    for i, (t, ls, cor) in enumerate(passos):
        x = 5 + i * (w + gap)
        tec.caixa(d, x, 40, w, 72, t, ls, cor)
        if i < len(passos) - 1:
            tec.seta(d, x + w, 76, x + w + gap, 76)
    d.add(String(5, 128, "Método: PyInstaller em modo --onefile (empacota o interpretador Python, as bibliotecas e o "
                         "código num único .exe; quem roda não precisa ter Python instalado)", fontName="Arial",
                 fontSize=8.5))
    d.add(String(5, 18, "Ao executar: o bootloader extrai o PKG numa pasta temporária (%TEMP%\\_MEIxxxxxx), carrega "
                        "python314.dll, roda o 3_ como __main__ e apaga a pasta temporária ao sair.",
                 fontName="Arial-I", fontSize=7.8))
    return d


def diagrama_estrutura(tam_exe, c):
    d = Drawing(760, 95)
    if c:
        partes = collections.OrderedDict()
        for nome, tipo, tam in c["itens"]:
            n = nome.lower()
            if "openblas" in n or n.startswith("numpy"):
                k = "numpy (arrastado pelo openpyxl)"
            elif n.startswith("pil"):
                k = "Pillow/PIL (arrastado)"
            elif "python314" in n or n == "python3.dll" or "vcruntime" in n:
                k = "Python 3.14 + runtime C"
            elif "libssl" in n or "libcrypto" in n or "_ssl" in n or "_hashlib" in n:
                k = "OpenSSL (HTTPS)"
            elif tipo == "PYZ":
                continue
            else:
                k = "outros .pyd / dados / scripts"
            partes[k] = partes.get(k, 0) + tam
        partes["PYZ: bytecode (3_, 6_, openpyxl, stdlib...)"] = c["pyz"]
    else:
        partes = {"conteúdo (rode o 11_ para detalhar)": tam_exe}
    total = sum(partes.values()) or 1
    paleta = [colors.HexColor(x) for x in ("#8E9AAF", "#CBC0D3", "#5B8E7D", "#F4A259", "#BC4B51", "#4A6FA5")]
    x = 5
    for i, (k, v) in enumerate(partes.items()):
        w = max(750 * v / total, 2)
        d.add(Rect(x, 45, w, 30, fillColor=paleta[i % len(paleta)], strokeColor=colors.white))
        x += w
    for i, (k, v) in enumerate(partes.items()):
        lx, ly = 5 + (i % 3) * 250, 28 - (i // 3) * 13
        d.add(Rect(lx, ly, 8, 8, fillColor=paleta[i % len(paleta)], strokeColor=None))
        d.add(String(lx + 11, ly + 1, f"{k}: {mb(v)}", fontName="Arial", fontSize=7))
    d.add(String(5, 82, f"Composição aproximada (antes da compressão final) — .exe instalado: {mb(tam_exe)}",
                 fontName="Arial-B", fontSize=8, fillColor=AZUL))
    return d


def montar():
    tam, data, h = dados_exe()
    v = versoes()
    c = conteudo_build()
    os.makedirs(PASTA_DOCS, exist_ok=True)
    doc = SimpleDocTemplate(SAIDA, pagesize=landscape(A4), leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                            topMargin=1.2 * cm, bottomMargin=1.5 * cm,
                            title="Documentação do executável 1_relatorio_acessos_anuncios.exe",
                            author="comprenolink.net")
    st = [Spacer(1, 2.2 * cm), P("1_relatorio_acessos_anuncios.exe", "titulo"), Spacer(1, 6),
          P("Como o executável foi gerado: arquivos que o compõem, método, comando e recursos utilizados", "sub"),
          Spacer(1, 4), P(f"Versão de {HOJE:%d/%m/%Y}", "sub"), Spacer(1, 0.8 * cm)]
    st.append(tabela(["Item", "Valor"], [
        ["Arquivo", "D:\\Projeto_Blog_Comprenolink\\Relatorios_Diarios_Anuncios\\programas_fontes_python\\1_relatorio_acessos_anuncios.exe"],
        ["O que é", "Versão \"clique duplo\" do 3_relatorio_acessos_anuncios.py: gera o relatório HTML de acessos e "
                    "vendas por anúncio sem precisar ter Python instalado"],
        ["Tamanho / data", f"{mb(tam)} ({tam:,} bytes) · compilado em {data:%d/%m/%Y %H:%M}".replace(",", ".")],
        ["SHA-256", h],
        ["Ferramenta", f"PyInstaller {v['PyInstaller']} · modo --onefile · console (janela preta)"],
        ["Interpretador embutido", f"Python {v['python']} 64 bits (python314.dll)"],
        ["Código-fonte", "D:\\Projeto_Blog_Comprenolink\\Relatorios_Diarios_Anuncios\\programas_fontes_python\\"
                         "3_relatorio_acessos_anuncios.py + 6_verificar_anuncios.py"],
        ["Como recompilar", "Clique duplo em programas_fontes_python\\11_compilar_exe_relatorio.bat"],
    ], [5.0, 21.5]))
    st.append(PageBreak())

    # 1. arquivos que compõem
    st.append(P("1. Arquivos .py e componentes que formam o executável", "h1"))
    st.append(P("Só <b>dois</b> arquivos .py do projeto entram no .exe. O resto são bibliotecas Python e DLLs que o "
                "PyInstaller encontrou seguindo os import."))
    st.append(tabela(["Componente", "Como entra no .exe", "Para que serve no relatório"], [
        ["3_relatorio_acessos_anuncios.py (1.225 linhas)", "Script de ENTRADA (PYSOURCE): é o que roda ao dar clique "
         "duplo", "Todo o relatório: baixa os acessos do WordPress, filtra o guia, cruza vendas, gera o HTML"],
        ["6_verificar_anuncios.py (227 linhas)", "Import OCULTO (--hidden-import): o 3_ o carrega com "
         "importlib.import_module(\"6_verificar_anuncios\"), que o PyInstaller não enxerga sozinho; vai no PYZ como "
         "bytecode", "Verifica no ML se os anúncios do guia estão ativos (quando a última verificação tem > 12 h)"],
        ["openpyxl " + v["openpyxl"], "Import tardio dentro de ler_planilha() do 3_; detectado na análise",
         "Ler a exportação de vendas do ML Afiliados quando ela vem em .xlsx"],
        ["Dependências do openpyxl: numpy " + v["numpy"] + ", Pillow " + v["PIL"] + ", PyYAML " + v["yaml"] +
         ", et_xmlfile, defusedxml", "Arrastadas automaticamente porque o openpyxl as importa de forma opcional",
         "Não são usadas pelo relatório; são a maior parte do tamanho (ver seção 5 e pontos de atenção)"],
        ["psutil " + v["psutil"] + ", charset_normalizer", "Arrastadas por outras bibliotecas instaladas",
         "Não usadas diretamente"],
        ["Biblioteca padrão do Python", "base_library.zip + PYZ: urllib, json, csv, html, re, difflib, argparse, "
         "datetime, unicodedata, importlib...", "Rede (HTTPS), leitura de CSV/JSON, comparação de nomes, opções"],
        ["python314.dll, python3.dll, VCRUNTIME140(_1).dll", "BINARY", "O interpretador Python e o runtime C"],
        ["libssl-3.dll, libcrypto-3.dll, _ssl.pyd, _hashlib.pyd", "BINARY / EXTENSION", "HTTPS para comprenolink.net "
         "e mercadolivre.com.br"],
        ["Bootloader run.exe do PyInstaller", "Cabeça do .exe", "Extrai e inicia o Python embutido"],
        ["config_rastreio.json", "NÃO entra no .exe. Lido na hora de rodar, de programas_fontes_python (única cópia; "
         "a de 1- Gera_Relatorio (pasta antiga; hoje Relatorios_Diarios_Anuncios\\programas_fontes_python) foi removida em 08/11/2026)",
         "Site, página do guia, chave da API, janela de compra. Pode ser editado sem recompilar"],
    ], [6.5, 9.5, 10.5]))
    if c:
        st.append(Spacer(1, 0.3 * cm))
        top = ", ".join(f"{k} ({n})" for k, n in c["top"].most_common(12))
        st.append(P(f"<b>Medido no último build:</b> {len(c['mods'])} módulos Python no PYZ "
                    f"({mb(c['pyz'])}); {c['tipos'].get('EXTENSION', 0)} extensões .pyd; "
                    f"{c['tipos'].get('BINARY', 0)} DLLs. Pacotes com mais módulos: {escape(top)}."))
    st.append(PageBreak())

    # 2. método
    st.append(P("2. Método utilizado: PyInstaller --onefile", "h1"))
    st.append(diagrama_metodo())
    st.append(Spacer(1, 0.2 * cm))
    st.append(tabela(["Etapa", "O que o PyInstaller faz"], [
        ["Análise", "Lê o 3_, segue cada import (inclusive dentro de funções) e monta a lista de módulos, DLLs e "
                    "dados necessários. Grava avisos em warn-*.txt e o mapa em xref-*.html."],
        ["PYZ", "Compila os módulos Python puros para bytecode (.pyc) e os junta num arquivo comprimido."],
        ["PKG", "Junta o PYZ, o script de entrada, as DLLs (Python, OpenSSL, runtime C), as extensões .pyd e o "
                "base_library.zip num pacote (CArchive)."],
        ["EXE", "Copia o bootloader run.exe (console, 64 bits) e anexa o PKG no final: resultado é 1 arquivo. UPX "
                "estava ativado no spec, mas o UPX não está instalado, então nada foi comprimido com ele."],
        ["Execução", "Clique duplo → bootloader extrai em %TEMP%\\_MEIxxxxxx → carrega python314.dll → roda o 3_ "
                     "com sys.frozen=True → ao fechar, apaga a pasta temporária."],
        ["Diferença rodando como .exe", "No 3_: PASTA = pasta do .exe (por isso config_rastreio.json e dados_acessos "
         "ficam em Relatorios_Diarios_Anuncios\\programas_fontes_python); saída do HTML em caminho fixo D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios/"
         "_historico_relatorios; o 6_ embutido recebe os caminhos da estrutura oficial (v.BASE, v.PASTA)."],
    ], [5.0, 21.5]))
    st.append(PageBreak())

    # 3. comando
    st.append(P("3. Comando de compilação e significado de cada parâmetro", "h1"))
    st.append(Preformatted(
        "cd D:\\Projeto_Blog_Comprenolink\\Relatorios_Diarios_Anuncios\\programas_fontes_python\n"
        "python -m PyInstaller --onefile --noconfirm --clean --name 1_relatorio_acessos_anuncios --paths . "
        "--hidden-import 6_verificar_anuncios\n"
        "       --distpath %TEMP%\\build_1_relatorio\\dist --workpath %TEMP%\\build_1_relatorio\\work "
        "--specpath %TEMP%\\build_1_relatorio 3_relatorio_acessos_anuncios.py", MONO))
    st.append(Spacer(1, 0.25 * cm))
    st.append(tabela(["Parâmetro", "Significado", "Por que foi usado"], [
        ["python -m PyInstaller", "Roda o PyInstaller instalado no Python 3.14", "Garante a mesma versão de Python "
         "que roda os scripts"],
        ["--onefile", "Gera um único .exe", "Fácil de copiar e de dar clique duplo; sem pasta _internal"],
        ["--noconfirm / --clean", "Sobrescreve sem perguntar / limpa cache de builds anteriores",
         "Build automático e sempre do zero"],
        ["--name 1_relatorio_acessos_anuncios", "Nome do .exe", "Mantém o nome que o dono já usa"],
        ["--paths .", "Inclui a pasta atual na busca de módulos", "Para achar o 6_verificar_anuncios.py"],
        ["--hidden-import 6_verificar_anuncios", "Força a inclusão de um módulo", "O 3_ importa o 6_ por importlib "
         "(nome começa com número), invisível para a análise"],
        ["--distpath / --workpath / --specpath", "Onde ficam o .exe, os temporários e o .spec",
         "Em %TEMP%, para não sujar a pasta dos fontes nem a de Relatorios_Diarios_Anuncios\\programas_fontes_python"],
        ["3_relatorio_acessos_anuncios.py", "Script de entrada", "É o programa principal"],
    ], [6.5, 9.0, 11.0]))
    st.append(PageBreak())

    st.append(P("4. Arquivo de especificação (.spec) usado", "h1"))
    st.append(P("Gerado pelo PyInstaller a partir do comando acima e guardado em programas_fontes_python\\"
                "1_relatorio_acessos_anuncios.spec (registro exato do build)."))
    spec = open(SPEC, encoding="utf-8").read() if os.path.exists(SPEC) else "(spec não encontrado)"
    st.append(Preformatted(spec.strip(), MONO))
    st.append(PageBreak())

    st.append(P("5. Recursos utilizados", "h1"))
    st.append(tabela(["Recurso", "Detalhe"], [
        ["Máquina", "Mini PC Svr_Ryzen · Windows 11 Pro · AMD Ryzen 5 7430U · 32 GB RAM"],
        ["Python", f"{v['python']} 64 bits em C:\\Users\\SVR_RYZEN_JAA\\AppData\\Local\\Python\\pythoncore-3.14-64 "
                   "(só necessário para COMPILAR; quem usa o .exe não precisa)"],
        ["PyInstaller", f"{v['PyInstaller']} (python -m pip install pyinstaller)"],
        ["Bibliotecas instaladas", f"openpyxl {v['openpyxl']} · numpy {v['numpy']} · Pillow {v['PIL']} · "
                                   f"PyYAML {v['yaml']} · psutil {v['psutil']}"],
        ["Automação", "11_compilar_exe_relatorio.bat (cmd.exe): compila, guarda o .exe anterior, instala, testa "
                      "--help e mostra o SHA-256 (certutil, nativo do Windows)"],
        ["Tempo / espaço", "≈ 30 s de compilação; ≈ 60 MB temporários em %TEMP%\\build_1_relatorio"],
        ["Feito por", "Claude (assistente de IA) na sessão do Claude Code, a pedido do dono"],
    ], [5.0, 21.5]))
    st.append(Spacer(1, 0.4 * cm))
    st.append(diagrama_estrutura(tam, c))
    st.append(PageBreak())

    st.append(P("6. Histórico de compilações", "h1"))
    st.append(tabela(["Data", "Motivo", "Cópia do .exe anterior"], [
        ["09/2026", "1ª versão (relatorio_acessos_anuncios.exe, em 10_Rastreamento_anuncios (pasta antiga; hoje Planejamentos\\Andamento\\Rastreamento_anuncios); a cópia de 21/10 que "
                    "ainda estava lá foi para a Lixeira em 08/11/2026)",
         "10_Rastreamento_anuncios (pasta antiga; hoje Planejamentos\\Andamento\\Rastreamento_anuncios)\\_exe_antigos_2026-09"],
        ["21/10/2026", "Renomeado para 1_relatorio_acessos_anuncios.exe e levado para 1- Gera_Relatorio (pasta antiga; hoje Relatorios_Diarios_Anuncios\\programas_fontes_python)",
         "_backups_claude_\\1_relatorio_acessos_anuncios_ANTES_02nov.exe"],
        ["02/11/2026", "HTML passa a ser gravado em _historico_relatorios; vendas lidas da pasta certa; 6_verificar "
                       "embutido (--paths python --hidden-import 6_verificar_anuncios); quadros \"fora do ar\" e "
                       "\"Substituição\"", "(mesma cópia acima)"],
        ["08/11/2026 10h18", "Fontes movidos para programas_fontes_python; caminho fixo trocado de "
                             "Relatorios_Diarios_Anuncios para Relatorios_Diarios_Anuncios",
         "_backups_claude_\\mover_painel_08-11\\1_relatorio_acessos_anuncios_ANTES_08nov.exe"],
        ["08/11/2026 10h29", "Teste do novo 11_compilar_exe_relatorio.bat (mesmo código, build reprodutível)",
         "_backups_claude_\\1_relatorio_acessos_anuncios_ANTES_2026-11-08_10h29.exe"],
        ["08/11/2026 10h33", "config_rastreio.json passa a ser lido de programas_fontes_python (fonte única); "
                             "dados_acessos sempre em 1- Gera_Relatorio (pasta antiga; hoje Relatorios_Diarios_Anuncios\\programas_fontes_python). Testado com dados reais (relatório 10h34)",
         "_backups_claude_\\1_relatorio_acessos_anuncios_ANTES_2026-11-08_10h33.exe"],
    ], [3.5, 15.0, 8.0]))
    st.append(Spacer(1, 0.4 * cm))
    st.append(P("7. Como verificar se o .exe está correto", "h2"))
    st.append(tabela(["Teste", "Como"], [
        ["Abre e mostra as opções", "No Prompt: \"1_relatorio_acessos_anuncios.exe\" --help → lista --dias, --demo, "
                                   "--arquivo, --vendas, --verificar-anuncios, --sem-verificar-anuncios"],
        ["Relatório de exemplo", "--demo gera um HTML com dados fictícios em _historico_relatorios (apagar depois)"],
        ["Caminho certo", "Depois de rodar, o HTML novo deve aparecer em Relatorios_Diarios_Anuncios\\"
                          "_historico_relatorios; NÃO deve surgir a pasta antiga 99_Relatorios_Diarios (pasta antiga; hoje Relatorios_Diarios_Anuncios)"],
        ["Integridade", "certutil -hashfile <exe> SHA256 deve bater com o SHA-256 da capa deste documento"],
    ], [5.0, 21.5]))
    st.append(PageBreak())

    st.append(P("8. Pontos de atenção", "h1"))
    st.append(tabela(["Ponto", "Explicação / recomendação"], [
        ["Mudou o 3_ ou o 6_? Recompile", "O .exe leva uma CÓPIA do código do momento da compilação. Alterar o .py "
         "não muda o .exe até rodar o 11_compilar_exe_relatorio.bat. O ATUALIZAR_PAINEL.bat usa os .py direto "
         "(não precisa recompilar para o painel)."],
        ["SHA-256 muda a cada build", "Mesmo sem mudar o código, o PyInstaller grava data/hora: cada compilação tem "
         "hash diferente. Regenere este PDF (12_) depois de recompilar."],
        ["Tamanho (≈ 28 MB)", "numpy/OpenBLAS e Pillow somam ≈ 37 MB dos ≈ 62 MB antes da compressão, arrastados "
         "pelo openpyxl e não usados. Opcional: --exclude-module numpy --exclude-module PIL reduziria bastante o .exe "
         "(não aplicado; testar a leitura de .xlsx de vendas antes)."],
        ["Antivírus", "Executáveis PyInstaller às vezes são marcados como suspeitos por heurística. Se acontecer, "
         "liberar o arquivo de Relatorios_Diarios_Anuncios\\programas_fontes_python no Windows Defender."],
        ["config_rastreio.json", "Precisa ficar na mesma pasta do .exe. Contém a chave secreta da API: não "
         "compartilhar."],
        ["Caminho fixo", "O HTML vai para D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios/_historico_relatorios. Se a "
         "pasta for renomeada, ajustar PASTA_SAIDA_HTML/PASTA_VENDAS/PASTA_STATUS no 3_ e recompilar."],
        ["Primeira execução mais lenta", "O bootloader extrai ≈ 60 MB em %TEMP% a cada abertura (1–3 s)."],
    ], [5.5, 21.0], fundo=LARANJA))
    doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    montar()
