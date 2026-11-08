"""
Gera a documentação (PDF) dos programas do Relatório Diário de Anúncios.

Saída: Relatorios_Diarios_Anuncios/docs_relatorio_diario_anuncio/
       DOCUMENTACAO_PROGRAMAS_RELATORIO_DIARIO_ANUNCIOS_DD_MM_AAAA.pdf
Uso:   python 9_gerar_documentacao_pdf.py
Quando mudar algum programa desta pasta, atualize as tabelas abaixo e rode de novo.
"""
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table,
                                TableStyle)

AQUI = os.path.dirname(os.path.abspath(__file__))
RELAT = os.path.dirname(AQUI)
PASTA_DOCS = os.path.join(RELAT, "docs_relatorio_diario_anuncio")
HOJE = datetime.now()
SAIDA = os.path.join(PASTA_DOCS, HOJE.strftime("DOCUMENTACAO_PROGRAMAS_RELATORIO_DIARIO_ANUNCIOS_%d_%m_%Y.pdf"))

pdfmetrics.registerFont(TTFont("Arial", "C:/Windows/Fonts/arial.ttf"))
pdfmetrics.registerFont(TTFont("Arial-B", "C:/Windows/Fonts/arialbd.ttf"))
pdfmetrics.registerFont(TTFont("Arial-I", "C:/Windows/Fonts/ariali.ttf"))
from reportlab.pdfbase.pdfmetrics import registerFontFamily  # noqa: E402
registerFontFamily("Arial", normal="Arial", bold="Arial-B", italic="Arial-I", boldItalic="Arial-B")

AZUL = colors.HexColor("#1F3A5F")
AZUL_CLARO = colors.HexColor("#E8EEF6")
CINZA = colors.HexColor("#F5F5F5")
LARANJA = colors.HexColor("#FFF3E0")

S = {
    "titulo": ParagraphStyle("t", fontName="Arial-B", fontSize=22, leading=27, textColor=AZUL, alignment=TA_CENTER),
    "sub": ParagraphStyle("s", fontName="Arial", fontSize=12, leading=16, alignment=TA_CENTER,
                          textColor=colors.HexColor("#444444")),
    "h1": ParagraphStyle("h1", fontName="Arial-B", fontSize=15, leading=19, textColor=AZUL, spaceBefore=6,
                         spaceAfter=6),
    "h2": ParagraphStyle("h2", fontName="Arial-B", fontSize=11.5, leading=15, textColor=AZUL, spaceBefore=8,
                         spaceAfter=4),
    "p": ParagraphStyle("p", fontName="Arial", fontSize=9.5, leading=13, spaceAfter=4),
    "cel": ParagraphStyle("c", fontName="Arial", fontSize=8, leading=10.2),
    "cab": ParagraphStyle("cb", fontName="Arial-B", fontSize=8.2, leading=10.2, textColor=colors.white),
}


def P(t, st="p"):
    return Paragraph(t, S[st])


def tabela(cabecalho, linhas, larguras, destaque_col0=True, fundo=None):
    dados = [[P(c, "cab") for c in cabecalho]] + [[P(str(c), "cel") for c in l] for l in linhas]
    t = Table(dados, colWidths=[w * cm for w in larguras], repeatRows=1)
    estilo = [
        ("BACKGROUND", (0, 0), (-1, 0), AZUL),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#B0B8C4")),
        ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4),
        ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3),
    ]
    for i in range(1, len(dados)):
        if i % 2 == 0:
            estilo.append(("BACKGROUND", (0, i), (-1, i), CINZA))
    if destaque_col0:
        estilo.append(("BACKGROUND", (0, 1), (0, -1), AZUL_CLARO))
    if fundo:
        estilo.append(("BACKGROUND", (0, 1), (-1, -1), fundo))
    t.setStyle(TableStyle(estilo))
    return t


def rodape(c, doc):
    c.saveState()
    c.setFont("Arial", 7.5)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(1.5 * cm, 0.9 * cm, "comprenolink.net · Documentação dos programas do Relatório Diário de Anúncios")
    c.drawRightString(landscape(A4)[0] - 1.5 * cm, 0.9 * cm,
                      f"Gerado em {HOJE:%d/%m/%Y %H:%M} · página {doc.page}")
    c.restoreState()


# ------------------------------------------------------------------ conteúdo
B = "<b>"
FB = "</b>"

INVENTARIO = [
    ["ATUALIZAR_PAINEL.bat", "Arquivo de lote do Windows (<b>não é Python</b>). Clique duplo.",
     "É o <b>botão de partida</b> do painel. Python, PowerShell e Excel são programas separados; o .bat chama "
     "cada um na ordem certa, com as pastas certas, e para se algo der errado. Sem ele o dono teria de "
     "digitar 4 comandos no terminal.",
     "Roda as 5 etapas: (1) verifica anúncios no ML, (2) monta a planilha, (3) recalcula no Excel e gera o PDF, "
     "(4) limpa arquivos antigos, (5) abre o painel. Tudo o que aparece na tela vai para log_painel.txt.",
     "Nenhuma (só os dados das pastas).", "log_painel.txt + tudo o que as etapas geram."],
    ["8_rodar_com_log.ps1", "Script PowerShell (chamado pelo .bat).",
     "O .bat sozinho não consegue mostrar na tela <b>e</b> gravar em arquivo ao mesmo tempo, com acentos (UTF-8).",
     "Executa o próprio ATUALIZAR_PAINEL.bat de novo, copiando cada linha da tela para o log, e anota início, "
     "fim, duração e código de saída.", "Caminho do .bat e do log.", "Relatorios_Diarios_Anuncios\\log_painel.txt"],
    ["6_verificar_anuncios.py", "Python. Etapa 1 do .bat; também vai embutido no .exe do relatório.",
     "Anúncio do ML pode ser pausado ou removido sem aviso; o blog continuaria mandando o visitante para um "
     "link morto (venda perdida).",
     "Lê a página pública do guia, pega cada produto e abre o link de afiliado (meli.la). Registra: Ativo, Pausado, "
     "Removido ou Não verificado, nº do anúncio (MLB), catálogo, título, preço, aviso do ML e causa provável. "
     "Não burla captcha nem login.",
     "Página do guia no blog; backups da página em 9_Manutenção_Blog\\2_DADOS\\Blog_WordPress\\backups; "
     "config_rastreio.json (desta pasta).",
     "anuncios_status\\status_anuncios_AAAA-MM-DD_HHhMM.csv + linha no historico_status_anuncios.csv."],
    ["3_relatorio_acessos_anuncios.py", "Python. Código-fonte do <b>1_relatorio_acessos_anuncios.exe</b> "
     "(pasta 1- Gera_Relatorio).",
     "Mostrar, de graça e com dados do próprio WordPress, quem visitou o guia, de qual anúncio/campanha veio, "
     "em quais produtos clicou e quais vendas aprovadas do ML vieram do guia.",
     "Baixa os acessos do plugin de rastreio (wp-json/rastreio/v1/dados), filtra só a página do guia, calcula "
     "intenção de compra, cruza vendas do ML Afiliados com os cliques (produto + horário), verifica anúncios se a "
     "última verificação tiver mais de 12 h e gera o relatório HTML com os quadros \"Anúncios fora do ar\" e "
     "\"Substituição\". O .py também é importado pelo 4_ para montar o quadro de substituição.",
     "config_rastreio.json (desta pasta); vendas_afiliados; anuncios_status.",
     "_historico_relatorios\\relatorio_acessos_anuncios_*.html; cópias brutas em 1- Gera_Relatorio\\dados_acessos "
     "(acessos_*.json/csv, compras_atribuidas_*.csv)."],
    ["4_atualizar_painel_controle.py", "Python. Etapa 2 do .bat.",
     "Um relatório HTML mostra só um momento. O painel junta <b>todos os dias</b> numa planilha com fórmulas, "
     "gráficos, metas e histórico permanente de vendas.",
     "Lê todos os relatorio_acessos_anuncios_*.html (cada um vira um \"quadro\"), as vendas exportadas, a situação "
     "dos anúncios, faz backup da planilha anterior e remonta as abas. Preserva o que o dono digitou "
     "(observações, Ignorar S/N, vendas manuais, metas, análise do especialista). Guarda 1 HTML por dia.",
     "Pasta Relatorios_Diarios_Anuncios (HTMLs, vendas_afiliados, anuncios_status).",
     "Painel de  Controle de Acesso.xlsx; _backup_painel\\Painel_*.xlsx; vendas_historico\\historico_vendas.csv; "
     "historico_consolidado\\historico_quadros.csv."],
    ["5_recalcular_exportar_painel.ps1", "Script PowerShell. Etapa 3 do .bat.",
     "O Python grava as fórmulas mas não as calcula; só o Excel calcula e exporta o PDF com o visual certo.",
     "Abre o Excel escondido, recalcula tudo, conta células com erro (#), salva e exporta a aba Painel em PDF.",
     "Planilha .xlsx.", "Painel_conversao_performance_AAAA-MM-DD_HHhMM.pdf"],
    ["7_limpar_historico.py", "Python. Etapa 4 do .bat (só roda se o PDF do dia foi gerado).",
     "Cada execução gera PDF, HTML, backup e CSV; sem limpeza a pasta cresce sem parar (8 MB por limpeza).",
     "Manda para a <b>Lixeira</b> (recuperável) o que já está consolidado: PDFs (1 por dia, últimos N), HTMLs, "
     "backups, status CSV e cópias brutas. Quantos manter: aba Metas. Nunca apaga a planilha nem os históricos "
     "permanentes. Aceita --simular.",
     "Aba Metas (retenção) + pastas de histórico.", "Arquivos antigos na Lixeira; lista no log."],
    ["9_gerar_documentacao_pdf.py", "Python. Rodado só quando se quer atualizar esta documentação.",
     "Manter a explicação dos programas junto com eles e fácil de regerar.",
     "Monta este PDF.", "Tabelas escritas no próprio script.", "docs_relatorio_diario_anuncio\\*.pdf"],
    ["10_gerar_documentacao_tecnica_pdf.py", "Python. Rodado só quando se quer atualizar a documentação técnica.",
     "Registrar como o sistema foi construído e o desenho da infraestrutura (para manutenção futura).",
     "Monta o PDF técnico: diagramas de infraestrutura, fluxo e dependências, stack, API do WordPress, funções, "
     "algoritmos, formatos de dados, build e segurança.", "Tabelas do próprio script + estilos do 9_.",
     "docs_relatorio_diario_anuncio\\DOCUMENTACAO_TECNICA_INFRA_*.pdf"],
    ["11_compilar_exe_relatorio.bat", "Arquivo de lote (não é Python). Clique duplo quando mudar o 3_ ou o 6_.",
     "O 1_relatorio_acessos_anuncios.exe leva uma cópia do código; mudar o .py não muda o .exe.",
     "Compila com PyInstaller --onefile (3_ + 6_), guarda o .exe anterior em _backups_claude_30out, instala o novo "
     "em 1- Gera_Relatorio, testa --help e mostra o SHA-256.", "3_ e 6_ desta pasta.",
     "1- Gera_Relatorio\\1_relatorio_acessos_anuncios.exe + 1_relatorio_acessos_anuncios.spec (nesta pasta)."],
    ["1_relatorio_acessos_anuncios.spec", "Texto de configuração do PyInstaller (gerado pelo 11_).",
     "Registro exato de como o .exe foi montado.", "Não se executa; serve de referência.", "—", "—"],
    ["12_gerar_documentacao_exe_pdf.py", "Python. Rodar depois de recompilar o .exe.",
     "Documentar como o .exe foi gerado (arquivos, método, comando, recursos).",
     "Lê o .exe instalado (tamanho, SHA-256), o .spec e a pasta de build e monta o PDF.", ".exe, .spec, build.",
     "docs_relatorio_diario_anuncio\\DOCUMENTACAO_EXECUTAVEL_*.pdf"],
]

ORDEM = [
    ["0", "Quando houver vendas novas (manual, no navegador)", "Dono",
     "Painel ML Afiliados → exportar vendas (CSV/XLSX)",
     "Salvar o arquivo em Relatorios_Diarios_Anuncios\\vendas_afiliados.", "1 a 2 min"],
    ["1", "1ª tarefa do dia (ou quando quiser ver os acessos)", "Dono: clique duplo",
     "1- Gera_Relatorio\\1_relatorio_acessos_anuncios.exe (fonte: 3_relatorio_acessos_anuncios.py)",
     "Baixa acessos do WordPress, verifica anúncios se a última verificação tiver >12 h (6_ embutido), cruza "
     "vendas e grava o HTML do dia em _historico_relatorios.", "1 a 12 min"],
    ["2", "Logo depois do relatório", "Dono: clique duplo",
     "programas_fontes_python\\ATUALIZAR_PAINEL.bat", "Inicia o painel e chama o passo 2a.", "—"],
    ["2a", "Primeira coisa que o .bat faz", "ATUALIZAR_PAINEL.bat",
     "8_rodar_com_log.ps1", "Abre o log_painel.txt e roda o .bat de novo, agora gravando tudo.", "instantâneo"],
    ["2b", "Etapa [1/5]", "ATUALIZAR_PAINEL.bat", "6_verificar_anuncios.py --pausa 2",
     "Confere no ML cada anúncio do guia e grava anuncios_status. Sem internet: avisa e usa a última verificação.",
     "≈3 s por anúncio (≈10 min com 213)"],
    ["2c", "Etapa [2/5]", "ATUALIZAR_PAINEL.bat", "4_atualizar_painel_controle.py (importa o 3_ para o quadro "
     "Substituição)", "Monta a planilha. Se o Excel estiver com a planilha aberta, para com ERRO.", "≈10 s"],
    ["2d", "Etapa [3/5]", "ATUALIZAR_PAINEL.bat", "5_recalcular_exportar_painel.ps1",
     "Excel recalcula e exporta o PDF do painel do dia.", "≈20 s"],
    ["2e", "Etapa [4/5] (só se o PDF saiu)", "ATUALIZAR_PAINEL.bat", "7_limpar_historico.py",
     "Envia arquivos antigos para a Lixeira conforme a aba Metas.", "≈2 s"],
    ["2f", "Etapa [5/5]", "ATUALIZAR_PAINEL.bat", "(Excel)", "Abre o Painel de  Controle de Acesso.xlsx.",
     "—"],
    ["3", "Depois", "Dono", "Planilha / PDF",
     "Ler o painel, preencher observações e Ignorar (S/N); trocar anúncios fora do ar (link meli.la gerado pelo "
     "dono no ML Afiliados).", "livre"],
]

HISTORICO = [
    ["21/10/2026", "Base do rastreio", "Fontes do relatório de acessos, gerador de links e SEO; compilados em "
     ".exe (1- Gera_Relatorio)."],
    ["22/10/2026", "Recalcular e exportar", "Criado 5_recalcular_exportar_painel.ps1: Excel calcula e gera PDF."],
    ["23/10/2026", "1º painel de conversão", "Primeiro PDF conversao_e_performance_do_blog_2026-10-23.pdf."],
    ["29/10/2026", "Links dos anúncios", "Lista de links dos anúncios (gerador de links, em 10_Rastreamento_anuncios)."],
    ["30/10/2026", "Reorganização das pastas", "Caminhos dos .py ajustados à nova estrutura; criados "
     "7_limpar_historico.py (Lixeira, retenção na aba Metas) e 8_rodar_com_log.ps1 (log_painel.txt)."],
    ["02/11/2026", "Relatório no lugar certo + verificador", "HTML passa a ser gravado em _historico_relatorios; "
     "vendas lidas de vendas_afiliados; 6_verificar_anuncios.py embutido no .exe; quadros \"Anúncios fora do ar\" e "
     "\"Substituição\" no relatório e no painel; aba Resumo_ML."],
    ["03 a 07/11/2026", "Uso diário", "Painéis e status gerados diariamente (17 relatórios, 19 vendas no histórico)."],
    ["08/11/2026", "Pasta programas_fontes_python", "A pedido do dono, .bat e scripts do painel (3_ a 8_) saem de "
     "D:\\mercado_livre\\python e vão para Relatorios_Diarios_Anuncios\\programas_fontes_python. Todos os caminhos "
     "trocados de 99_Relatorios_Diarios (nome antigo, não existe mais) para Relatorios_Diarios_Anuncios. "
     ".exe do relatório recompilado com o caminho novo (antigo guardado em 99_Programas_PY\\_backups_claude_30out\\"
     "mover_painel_08-11). Teste completo: 5 etapas OK, 642 s, 213 anúncios (4 fora do ar). Criada esta "
     "documentação."],
]

PASTAS = [
    ["programas_fontes_python", "Todos os programas desta rotina (.bat, .py, .ps1).", "—", "Dono / .bat"],
    ["(raiz) Painel de  Controle de Acesso.xlsx", "O painel com todas as abas.", "4_ e 5_", "Dono"],
    ["(raiz) Painel_conversao_performance_*.pdf", "Foto do painel de cada dia.", "5_", "Dono"],
    ["(raiz) log_painel.txt", "Tudo o que apareceu na tela na última execução.", "8_", "Dono (diagnóstico)"],
    ["_historico_relatorios", "Relatórios HTML de acessos (1 por dia).", "1_relatorio .exe / 3_", "4_"],
    ["vendas_afiliados", "Exportações de vendas do ML Afiliados (entrada manual).", "Dono", "3_ e 4_"],
    ["vendas_historico\\historico_vendas.csv", "Histórico permanente: 1 linha por pedido, nunca duplica.", "4_",
     "4_"],
    ["historico_consolidado\\historico_quadros.csv", "Métricas de cada dia (1 linha por dia).", "4_", "4_ e 7_"],
    ["anuncios_status", "Situação dos anúncios a cada verificação + histórico permanente.", "6_", "3_ e 4_"],
    ["_backup_painel", "Cópia da planilha antes de cada atualização.", "4_", "Dono (recuperar)"],
    ["docs_relatorio_diario_anuncio", "Esta documentação.", "9_", "Dono"],
    ["..\\1- Gera_Relatorio", ".exe do relatório, config_rastreio.json (site + chave), dados_acessos (brutos).",
     "PyInstaller / 3_", "3_, 6_, 7_"],
]

ABAS = [
    ["Painel", "Resumo visual: acessos, cliques, vendas, conversão, gráficos e análise do especialista (texto "
     "preservado)."],
    ["Metas", "Metas e retenção da limpeza (\"Limpeza: manter ...\"). Valores da coluna B são preservados."],
    ["Quadros", "Um quadro por relatório/dia; coluna Observação preservada."],
    ["Campanhas / Produtos / Perfil / Diario", "Detalhes do relatório mais recente: de onde veio, o que clicou, "
     "aparelho, dia a dia."],
    ["Visitantes", "Visitantes anônimos; coluna Ignorar (S/N) para tirar os testes do dono."],
    ["Anuncios / Anuncios_Hist", "Situação atual de cada anúncio e o histórico de verificações; quadro Substituição."],
    ["Vendas / Resumo_ML", "Vendas aprovadas/pendentes/canceladas e de qual clique vieram; linhas \"manual\" "
     "preservadas."],
    ["Calc", "Cálculos auxiliares das fórmulas (não editar)."],
]

OPCOES = [
    ["PAINEL_SEM_LOG=1", "Roda sem gravar log_painel.txt."],
    ["PAINEL_SEM_VERIFICAR=1", "Pula a etapa 1 (usa a última verificação) — economiza ~10 min."],
    ["PAINEL_SEM_LIMPEZA=1", "Pula a etapa 4 (nada vai para a Lixeira)."],
    ["PAINEL_NAO_ABRIR=1", "Não abre o Excel no fim."],
    ["PAINEL_PASTA_VENDAS=...", "Lê as vendas de outra pasta."],
    ["PAINEL_PASTA_BRUTOS=...", "Outra pasta de dados brutos para a limpeza."],
]

ATENCAO = [
    ["Etapa 1 demorada", "Com 213 anúncios a verificação leva ~10 min. Para um painel rápido: "
     "set PAINEL_SEM_VERIFICAR=1 antes de rodar o .bat (o .exe do relatório já verifica se passou de 12 h)."],
    ["Excel aberto", "Feche a planilha antes do .bat; com ela aberta a etapa 2 para com ERRO."],
    ["Mudou o 3_ ou o 6_?", "Recompilar o .exe: clique duplo em 11_compilar_exe_relatorio.bat (compila, guarda o antigo e instala) "
     "e depois rodar o 12_gerar_documentacao_exe_pdf.py."],
    ["config_rastreio.json", "Fica em programas_fontes_python (fonte única: site, página do guia, chave da API). "
     "É a única cópia (a de 1- Gera_Relatorio foi removida em 08/11/2026): não apagar nem mover."],
    ["Não separar os arquivos", "O 4_ importa o 3_ e o 3_ importa o 6_; o .bat chama 5_, 6_, 7_ e 8_ na mesma "
     "pasta. Todos devem ficar juntos em programas_fontes_python."],
    ["Limites do ML", "O ML não mostra o MOTIVO de pausa/remoção (só ao vendedor) e pode pedir verificação de robô; "
     "nesses casos o anúncio fica \"Não verificado\". O script não burla isso (evita bloqueio)."],
    ["Lixeira", "A limpeza manda para a Lixeira do Windows: dá para recuperar até esvaziá-la."],
    ["Fora desta pasta", "Em D:\\mercado_livre\\python ficaram 2_gerar_links_anuncios.py, "
     "gerar_relatorio_blog_v4 e test_blog_seo.py (outras rotinas: links e SEO), que não fazem parte do painel."],
]


def montar():
    os.makedirs(PASTA_DOCS, exist_ok=True)
    doc = SimpleDocTemplate(SAIDA, pagesize=landscape(A4), leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                            topMargin=1.3 * cm, bottomMargin=1.5 * cm,
                            title="Documentação dos programas - Relatório Diário de Anúncios",
                            author="comprenolink.net")
    st = []
    st += [Spacer(1, 3.2 * cm), P("Relatório Diário de Anúncios", "titulo"), Spacer(1, 6),
           P("Documentação dos programas da pasta <b>programas_fontes_python</b>", "sub"), Spacer(1, 4),
           P("D:\\mercado_livre\\Relatorios_Diarios_Anuncios · comprenolink.net", "sub"), Spacer(1, 4),
           P(f"Versão de {HOJE:%d/%m/%Y}", "sub"), Spacer(1, 1.2 * cm)]
    st.append(tabela(["Em uma frase"], [[
        "Todo dia o dono gera o <b>relatório de acessos</b> (.exe) e depois dá clique duplo no "
        "<b>ATUALIZAR_PAINEL.bat</b>. O .bat confere se os anúncios do guia ainda estão no ar, junta todos os "
        "relatórios e vendas numa planilha, gera o PDF do painel, limpa o que é antigo e abre o resultado."]],
        [26.5], destaque_col0=False, fundo=AZUL_CLARO))
    st.append(Spacer(1, 0.6 * cm))
    st.append(tabela(["Seção", "Conteúdo"], [
        ["1", "Para que serve cada arquivo (.bat, .py, .ps1)"],
        ["2", "Ordem cronológica de execução — em que momento cada um roda"],
        ["3", "Histórico do que foi realizado (por data)"],
        ["4", "Pastas e arquivos de dados: quem grava, quem lê"],
        ["5", "Abas da planilha e opções do .bat"],
        ["6", "Pontos de atenção e conclusão"]], [2, 24.5]))
    st.append(PageBreak())

    st.append(P("1. Para que serve cada arquivo", "h1"))
    st.append(P("O número no início do nome segue a numeração original do projeto (o 2_gerar_links_anuncios.py, de "
                "outra rotina, ficou em D:\\mercado_livre\\python). <b>Por que existe</b> = o problema que o arquivo "
                "resolve; <b>o que faz na prática</b> = o que acontece quando ele roda."))
    st.append(tabela(["Arquivo", "Tipo / quem chama", "Por que existe", "O que faz na prática", "Lê", "Grava"],
                     INVENTARIO, [3.6, 3.4, 5.0, 7.0, 3.7, 3.8]))
    st.append(PageBreak())

    st.append(P("2. Ordem cronológica de execução", "h1"))
    st.append(P("Sequência de um dia normal. Os passos 2a a 2f acontecem sozinhos depois do clique duplo no .bat; "
                "a tela mostra [1/5] ... [5/5]."))
    st.append(tabela(["Passo", "Quando", "Quem dispara", "Arquivo executado", "O que acontece", "Tempo"],
                     ORDEM, [1.3, 4.2, 3.2, 6.2, 8.6, 3.0]))
    st.append(Spacer(1, 0.4 * cm))
    st.append(P("Fluxo resumido", "h2"))
    st.append(tabela(["Entrada", "→", "Processamento", "→", "Resultado"], [[
        "WordPress (acessos e cliques do guia) · ML Afiliados (vendas) · páginas públicas do ML (situação dos "
        "anúncios)", "→",
        "1_relatorio .exe (3_ + 6_) → ATUALIZAR_PAINEL.bat → 8_ → 6_ → 4_ (+3_) → 5_ (Excel) → 7_", "→",
        "Relatório HTML do dia · Painel .xlsx · PDF do painel · históricos permanentes · log"]],
        [7.0, 0.7, 10.0, 0.7, 8.1], destaque_col0=False))
    st.append(PageBreak())

    st.append(P("3. Histórico do que foi realizado", "h1"))
    st.append(P("Datas pela criação/última alteração dos arquivos e pelos registros do projeto."))
    st.append(tabela(["Data", "Entrega", "O que foi feito"], HISTORICO, [3.0, 5.0, 18.5]))
    st.append(PageBreak())

    st.append(P("4. Pastas e arquivos de dados", "h1"))
    st.append(P("Todas dentro de D:\\mercado_livre\\Relatorios_Diarios_Anuncios, exceto a última linha."))
    st.append(tabela(["Pasta / arquivo", "O que guarda", "Quem grava", "Quem lê"], PASTAS, [7.0, 11.0, 4.3, 4.2]))
    st.append(PageBreak())

    st.append(P("5. Abas da planilha e opções do .bat", "h1"))
    st.append(tabela(["Aba", "Para que serve"], ABAS, [6.0, 20.5]))
    st.append(Spacer(1, 0.4 * cm))
    st.append(KeepTogether([
        P("Opções do ATUALIZAR_PAINEL.bat (avançado)", "h2"),
        P("Digite no Prompt de Comando, na pasta programas_fontes_python, antes de rodar o .bat. "
          "Ex.: <i>set PAINEL_SEM_VERIFICAR=1</i> e depois <i>ATUALIZAR_PAINEL.bat</i>."),
        tabela(["Variável", "Efeito"], OPCOES, [6.0, 20.5])]))
    st.append(PageBreak())

    st.append(P("6. Pontos de atenção", "h1"))
    st.append(tabela(["Ponto", "O que saber / fazer"], ATENCAO, [5.0, 21.5], fundo=LARANJA))
    st.append(Spacer(1, 0.5 * cm))
    st.append(P("Conclusão de performance", "h2"))
    st.append(P("Na execução de 08/11/2026 a partir da nova pasta, a rotina completa rodou sem erros em 642 s: "
                "213 anúncios verificados (4 fora do ar), 17 relatórios consolidados, 19 vendas no histórico e PDF "
                "do painel gerado. Quase todo o tempo (≈ 10 min) é da etapa 1, que cresce com o número de produtos do "
                "guia; as demais etapas somam menos de 1 minuto. A estrutura agora está concentrada: programas em "
                "programas_fontes_python, dados nas subpastas e documentação em docs_relatorio_diario_anuncio."))
    doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    montar()
