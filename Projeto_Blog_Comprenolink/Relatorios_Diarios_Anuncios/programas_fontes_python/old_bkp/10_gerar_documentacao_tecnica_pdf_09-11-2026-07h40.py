"""
Gera a DOCUMENTAÇÃO TÉCNICA (criação + desenho de infraestrutura) do Relatório Diário de Anúncios.

Saída: Relatorios_Diarios_Anuncios/docs_relatorio_diario_anuncio/
       DOCUMENTACAO_TECNICA_INFRA_RELATORIO_DIARIO_ANUNCIOS_DD_MM_AAAA.pdf
Uso:   python 10_gerar_documentacao_tecnica_pdf.py
Reaproveita estilos e tabelas do 9_gerar_documentacao_pdf.py (mesma pasta).
A chave secreta do config_rastreio.json NUNCA entra no PDF.
"""
import importlib
import os
import sys

from reportlab.graphics.shapes import Drawing, Line, Polygon, Rect, String
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer
from reportlab.lib.pagesizes import A4, landscape

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
base = importlib.import_module("9_gerar_documentacao_pdf")
P, tabela, HOJE, PASTA_DOCS = base.P, base.tabela, base.HOJE, base.PASTA_DOCS
AZUL, AZUL_CLARO, LARANJA = base.AZUL, base.AZUL_CLARO, base.LARANJA
SAIDA = os.path.join(PASTA_DOCS, HOJE.strftime("DOCUMENTACAO_TECNICA_INFRA_RELATORIO_DIARIO_ANUNCIOS_%d_%m_%Y.pdf"))

VERDE = colors.HexColor("#E6F4EA")
AMAR = colors.HexColor("#FFF8E1")
ROXO = colors.HexColor("#F3E8FD")
BORDA = colors.HexColor("#5A6B80")


def rodape(c, doc):
    c.saveState()
    c.setFont("Arial", 7.5)
    c.setFillColor(colors.HexColor("#666666"))
    c.drawString(1.5 * cm, 0.9 * cm, "comprenolink.net · Documentação técnica e desenho de infraestrutura")
    c.drawRightString(landscape(A4)[0] - 1.5 * cm, 0.9 * cm, f"Gerado em {HOJE:%d/%m/%Y %H:%M} · página {doc.page}")
    c.restoreState()


# ------------------------------------------------------------------ desenho
def caixa(d, x, y, w, h, titulo, linhas, fundo):
    d.add(Rect(x, y, w, h, rx=5, ry=5, fillColor=fundo, strokeColor=BORDA, strokeWidth=0.8))
    d.add(String(x + 6, y + h - 13, titulo, fontName="Arial-B", fontSize=8.5, fillColor=AZUL))
    for i, t in enumerate(linhas):
        d.add(String(x + 6, y + h - 26 - i * 10.5, t, fontName="Arial", fontSize=7.2, fillColor=colors.black))


def seta(d, x1, y1, x2, y2, rotulo="", dx=0, dy=4, cor=AZUL):
    d.add(Line(x1, y1, x2, y2, strokeColor=cor, strokeWidth=1.1))
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    p = 6
    d.add(Polygon([x2, y2, x2 - p * math.cos(a - 0.4), y2 - p * math.sin(a - 0.4),
                   x2 - p * math.cos(a + 0.4), y2 - p * math.sin(a + 0.4)], fillColor=cor, strokeColor=cor))
    if rotulo:
        d.add(String((x1 + x2) / 2 + dx, (y1 + y2) / 2 + dy, rotulo, fontName="Arial-I", fontSize=6.8,
                     fillColor=colors.HexColor("#333333"), textAnchor="middle"))


def zona(d, x, y, w, h, titulo, cor):
    d.add(Rect(x, y, w, h, rx=8, ry=8, fillColor=None, strokeColor=cor, strokeWidth=1.2, strokeDashArray=[4, 3]))
    d.add(String(x + 8, y + h - 12, titulo, fontName="Arial-B", fontSize=9, fillColor=cor))


def selo(d, x, y, n):
    from reportlab.graphics.shapes import Circle
    d.add(Circle(x, y, 7, fillColor=colors.HexColor("#C62828"), strokeColor=colors.white, strokeWidth=0.8))
    d.add(String(x, y - 3, str(n), fontName="Arial-B", fontSize=8, fillColor=colors.white, textAnchor="middle"))


def diagrama_infra():
    W, H = 760, 300
    d = Drawing(W, H)
    zona(d, 5, 130, 250, 165, "INTERNET / USUÁRIOS", colors.HexColor("#8A6D00"))
    zona(d, 270, 130, 250, 165, "HOSPEDAGEM HOSTINGER (comprenolink.net)", colors.HexColor("#1B7F3B"))
    zona(d, 535, 130, 220, 165, "MERCADO LIVRE (externo)", colors.HexColor("#B26A00"))
    zona(d, 5, 2, 750, 120, "MINI PC SVR_RYZEN · Windows 11 Pro · Ryzen 5 7430U · 32 GB · D:\\Projeto_Blog_Comprenolink",
         colors.HexColor("#5B2C83"))
    caixa(d, 15, 205, 230, 70, "Visitante (celular / PC)", [
        "Vem de TikTok, Instagram, WhatsApp, bio...", "Link com utm_source/medium/campaign",
        "Navegador roda o JavaScript do rastreador"], AMAR)
    caixa(d, 15, 137, 230, 58, "Dono (navegador)", [
        "Exporta vendas do painel ML Afiliados", "Gera links meli.la (afiliado)"], AMAR)
    caixa(d, 280, 205, 230, 70, "WordPress + Code Snippets", [
        "Snippet 'Rastreador de anúncios' (PHP+JS)", "POST /wp-json/rastreio/v1/evento (aberto)",
        "GET  /wp-json/rastreio/v1/dados (chave)"], VERDE)
    caixa(d, 280, 137, 230, 58, "MySQL: tabela wp_rastreio_acessos", [
        "1 linha por visita/clique · guarda 400 dias", "IP só como hash SHA-256 diário (12 car.)"], VERDE)
    caixa(d, 545, 205, 200, 70, "Páginas públicas do ML", [
        "meli.la/... → mercadolivre.com.br/social", "1º card: MLB, catálogo, preço, aviso",
        "Sem API/login (captcha = Não verificado)"], LARANJA)
    caixa(d, 545, 137, 200, 58, "Painel ML Afiliados", [
        "Vendas e comissões (CSV/XLSX)", "Exportação MANUAL pelo dono"], LARANJA)
    caixa(d, 15, 10, 175, 92, "1- Gera_Relatorio", [
        "1_relatorio_acessos_anuncios.exe", "(PyInstaller: 3_ + 6_ embutido)", "config_rastreio.json (site+chave)",
        "dados_acessos\\ (cópias brutas)"], ROXO)
    caixa(d, 205, 10, 200, 92, "programas_fontes_python", [
        "ATUALIZAR_PAINEL.bat (orquestrador)", "3_ 4_ 6_ 7_ (.py · Python 3.14)", "5_ 8_ (.ps1 · PowerShell)",
        "9_ 10_ (geram a documentação)"], ROXO)
    caixa(d, 420, 10, 155, 92, "Microsoft Excel (COM)", [
        "Microsoft 365 v16", "Recalcula fórmulas", "Exporta aba Painel → PDF", "chamado pelo 5_ .ps1"], ROXO)
    caixa(d, 590, 10, 155, 92, "Relatorios_Diarios_Anuncios", [
        "Painel .xlsx + PDF do dia", "_historico_relatorios (HTML)", "anuncios_status · vendas_*",
        "historico_consolidado · log"], ROXO)
    seta(d, 245, 240, 280, 240)
    seta(d, 395, 205, 395, 195)
    seta(d, 190, 56, 205, 56)
    seta(d, 405, 56, 420, 56)
    seta(d, 575, 56, 590, 56)
    selo(d, 262, 250, 1)
    selo(d, 405, 200, 2)
    selo(d, 180, 95, 3)
    selo(d, 395, 95, 4)
    selo(d, 735, 188, 5)
    selo(d, 412, 66, 6)
    selo(d, 582, 66, 7)
    return d


CONEXOES = [
    ["1", "Visitante → WordPress", "HTTPS POST /wp-json/rastreio/v1/evento (navigator.sendBeacon / fetch keepalive)",
     "A cada visita e a cada clique em produto"],
    ["2", "WordPress → MySQL", "INSERT na tabela wp_rastreio_acessos; 1 em 200 gravações apaga > 400 dias",
     "Contínuo"],
    ["3", "1_relatorio .exe → WordPress", "HTTPS GET /wp-json/rastreio/v1/dados?desde=... com cabeçalho "
     "X-Rastreio-Chave; resposta JSON", "Quando o dono roda o relatório"],
    ["4", "6_verificar (no .bat e no .exe) → ML", "HTTPS GET de cada link de afiliado (urllib, timeout 40 s, "
     "pausa 2 s), lê o 1º card", "Etapa [1/5] e no .exe se > 12 h"],
    ["5", "ML Afiliados → vendas_afiliados", "Dono baixa CSV/XLSX no navegador e salva na pasta (manual)",
     "Quando houver vendas"],
    ["6", "5_ .ps1 → Excel", "COM local (Excel.Application): CalculateFull, Save, ExportAsFixedFormat",
     "Etapa [3/5]"],
    ["7", "Programas → pastas de dados", "Arquivos locais (CSV ; UTF-8 BOM, XLSX, HTML, PDF, TXT); limpeza via "
     "Lixeira", "Etapas [2/5] a [4/5]"],
]


def diagrama_fluxo():
    W, H = 760, 175
    d = Drawing(W, H)
    etapas = [
        ("A. Coleta", ["JS no blog envia", "visita/clique", "→ MySQL WP"], VERDE),
        ("B. Relatório", ["1_relatorio .exe", "baixa /dados, filtra", "guia, gera HTML"], ROXO),
        ("C. [1/5] 6_", ["verifica cada", "anúncio no ML", "→ anuncios_status"], LARANJA),
        ("D. [2/5] 4_", ["lê HTML+vendas+", "status, monta xlsx", "(importa 3_)"], ROXO),
        ("E. [3/5] 5_", ["Excel recalcula", "e exporta o", "PDF do painel"], ROXO),
        ("F. [4/5] 7_", ["envia antigos", "à Lixeira", "(retenção: Metas)"], ROXO),
        ("G. [5/5]", ["abre o painel", "no Excel", "para o dono"], AMAR),
    ]
    w, gap, y, h = 96, 12, 50, 80
    for i, (t, ls, cor) in enumerate(etapas):
        x = 5 + i * (w + gap)
        caixa(d, x, y, w, h, t, ls, cor)
        if i < len(etapas) - 1:
            seta(d, x + w, y + h / 2, x + w + gap, y + h / 2)
    d.add(String(5, 150, "A roda o tempo todo no servidor · B é disparado pelo dono · C a G rodam sozinhos após o "
                         "clique duplo no ATUALIZAR_PAINEL.bat (8_rodar_com_log.ps1 envolve C–G gravando o log)",
                 fontName="Arial", fontSize=8))
    d.add(String(5, 25, "Entradas: MySQL do WordPress (via API) · páginas públicas do ML · exportação manual do ML "
                        "Afiliados   |   Saídas: HTML · XLSX · PDF · CSVs de histórico · log_painel.txt",
                 fontName="Arial-I", fontSize=7.5))
    return d


def diagrama_dependencias():
    W, H = 760, 150
    d = Drawing(W, H)
    caixa(d, 5, 55, 150, 45, "ATUALIZAR_PAINEL.bat", ["cmd.exe · orquestrador"], AMAR)
    caixa(d, 200, 105, 140, 40, "8_rodar_com_log.ps1", ["relança o .bat c/ log"], ROXO)
    caixa(d, 200, 55, 140, 40, "6_verificar_anuncios", ["urllib → ML"], LARANJA)
    caixa(d, 200, 5, 140, 40, "5_ / 7_", ["Excel COM · Lixeira"], ROXO)
    caixa(d, 390, 55, 160, 45, "4_atualizar_painel", ["openpyxl → .xlsx"], ROXO)
    caixa(d, 600, 55, 155, 45, "3_relatorio_acessos", ["importado pelo 4_ · importa o 6_"], ROXO)
    caixa(d, 600, 5, 155, 40, "1_relatorio .exe", ["PyInstaller: 3_ + 6_"], VERDE)
    seta(d, 155, 85, 200, 120, "1º", dy=6)
    seta(d, 155, 77, 200, 75, "[1/5]", dy=4)
    seta(d, 155, 65, 200, 30, "[3/5][4/5]", dx=-5, dy=-8)
    seta(d, 155, 92, 390, 92, "[2/5]", dx=40, dy=4)
    seta(d, 550, 77, 600, 77, "import")
    seta(d, 677, 55, 677, 45, "")
    return d


# ------------------------------------------------------------------ tabelas
STACK = [
    ["Servidor do blog", "Hostinger · WordPress · plugin Code Snippets · LiteSpeed Cache · MySQL",
     "Recebe e guarda visitas e cliques"],
    ["Máquina local", "Mini PC Svr_Ryzen · Windows 11 Pro · AMD Ryzen 5 7430U · 32 GB RAM",
     "Roda relatório, painel e limpeza"],
    ["Linguagem", "Python 3.14.7 (pythoncore-3.14-64) · stdout UTF-8 (PYTHONUTF8=1)", "3_, 4_, 6_, 7_, 9_, 10_"],
    ["Bibliotecas externas", "openpyxl 3.1.5 (planilha, gráficos, formatação) · reportlab 5.0.1 (PDFs da "
     "documentação) · PyInstaller 6.22.3 (gera o .exe)", "Só essas 3; o resto é biblioteca padrão"],
    ["Biblioteca padrão", "urllib (HTTP), csv, json, html, re, difflib.SequenceMatcher (semelhança de nomes), "
     "unicodedata, glob, shutil, subprocess, argparse, importlib", "Sem requests/pandas: menos dependências"],
    ["Automação Windows", "cmd.exe (.bat) · PowerShell (5_, 8_) · Excel via COM (Excel.Application) · "
     "Lixeira via PowerShell/Shell", "Integra Python com Excel e log"],
    ["Excel", "Microsoft 365 · versão 16.0.20527", "Recalcular e exportar PDF"],
    ["Rede", "HTTPS de saída para comprenolink.net e mercadolivre.com.br / meli.la · timeout 40 s · 2 tentativas",
     "Sem portas abertas na máquina local"],
]

WP = [
    ["Snippet", "10_Rastreamento_anuncios\\1_snippet_wordpress_rastreador.php (320 linhas) · instalado em Snippets > "
     "\"Rastreador de anúncios\" · roda em todo o site"],
    ["Tabela", "wp_rastreio_acessos: id, criado_em, tipo (visita/clique), visitante, sessao, pagina, origem, meio, "
     "campanha, conteudo, referencia, app, dispositivo, sistema, navegador, ip_hash, produto, link · índice em "
     "criado_em"],
    ["Coleta (JS)", "Injetado no wp_footer. Gera id aleatório de visitante (localStorage) e sessão (sessionStorage), "
     "lê utm_*, ttclid/fbclid/gclid e app de origem; em clique num link meli.la registra produto e link. Envia por "
     "navigator.sendBeacon (ou fetch keepalive)."],
    ["POST /wp-json/rastreio/v1/evento", "Aberto (público). Valida e corta os campos, classifica o User-Agent "
     "(aparelho/sistema/navegador) e grava 1 linha. Em 1 de cada 200 gravações apaga registros com mais de 400 dias."],
    ["GET /wp-json/rastreio/v1/dados", "Protegido: só responde com o cabeçalho X-Rastreio-Chave igual a "
     "RASTREIO_CHAVE (comparação hash_equals). Parâmetro desde=AAAA-MM-DD (padrão 90 dias), até 100.000 linhas, "
     "JSON. Alternativa: /?rest_route=/rastreio/v1/dados."],
    ["Privacidade (LGPD)", "Sem nome, e-mail ou IP. IP vira SHA-256(IP + wp_salt + data) cortado em 12 caracteres, "
     "que muda todo dia. Administradores/editores logados não são contados."],
]

FUNCOES = [
    ["3_relatorio_acessos_anuncios.py (1.225 linhas)",
     "baixar_dados (API WP) · filtrar_pagina (só o guia) · canal / tipo_trafego / veio_de_anuncio (origem) · "
     "carregar_vendas + mapear_colunas (CSV/XLSX tolerante) · classificar_status · atribuir_vendas · "
     "filtrar_comprenolink · intencao_compra · verificacao_antiga + verificar_anuncios_agora (chama 6_) · "
     "situacao_anuncios + quadros_anuncios (fora do ar / substituição) · gerar (HTML) · salvar_copia / "
     "salvar_compras (dados_acessos) · main (argparse: --dias, --demo, --arquivo, --vendas, --verificar-anuncios, "
     "--sem-verificar-anuncios)"],
    ["4_atualizar_painel_controle.py (1.780 linhas)",
     "ler_relatorio (extrai cards e tabelas do HTML) · ler_vendas / normalizar_status / consolidar_vendas "
     "(histórico sem duplicar pedido) · atribuir_vendas + semelhanca · ler_status_anuncios · ler_preservados "
     "(o que o dono digitou) · montar (abas, fórmulas, gráficos BarChart/LineChart/DoughnutChart, formatação "
     "condicional) · situacao_substituicao (importa 3_) · backup · arquivar_relatorios (1 HTML/dia) · "
     "consolidar_quadros · main"],
    ["6_verificar_anuncios.py (227 linhas)",
     "baixar (urllib, timeout 40 s, 2 tentativas) · pagina_do_guia · itens_do_blog (lê os cards da página) · "
     "catalogo_dos_backups (catálogo pelos backups do WP) · primeiro_card (MLB, catálogo, título, preço, aviso) · "
     "verificar (define status) · main(pausa) grava CSV do dia + histórico"],
    ["7_limpar_historico.py (134 linhas)",
     "retencao (lê aba Metas) · dia_hora · ultimos_dias (1 por dia, o mais tarde) · para_lixeira (PowerShell → "
     "Lixeira) · main (--simular)"],
    ["5_recalcular_exportar_painel.ps1", "New-Object -ComObject Excel.Application · CalculateFull · conta células "
     "#erro (sai com código 3) · Save · ExportAsFixedFormat(0) da aba Painel · Quit + ReleaseComObject"],
    ["8_rodar_com_log.ps1", "StreamWriter UTF-8 com BOM · define PAINEL_LOG_ATIVO=1 (evita laço) · cmd /c do .bat · "
     "cada linha vai para tela e arquivo · grava duração e código de saída"],
]

REGRAS = [
    ["Intenção de compra (0–100)", "Só para quem clicou: 40 pontos base; +20 clicou 2+ vezes no mesmo produto; "
     "+20 voltou em outra sessão e clicou; +10 saiu do blog direto para o ML; +10 focado em um único produto. "
     "Máximo 100."],
    ["Atribuição de venda ao clique", "Janela de 24 h antes da venda (config janela_compra_horas). Se a venda não "
     "tem hora, usa o dia inteiro. Entre os cliques da janela escolhe o de maior semelhança de nome "
     "(SequenceMatcher + palavras em comum); semelhança ≥ 0,5 = venda ligada ao clique/anúncio."],
    ["Status da venda", "Estado do ML Afiliados → Aprovada / Pendente / Cancelada. Vazio ou desconhecido = Pendente "
     "(não conta como aprovada)."],
    ["Filtro da página", "Só eventos da página do guia (pagina_blog + paginas_antigas). Acessos de outras páginas "
     "são contados à parte (outras_paginas)."],
    ["Situação do anúncio", "Abre o link de afiliado e lê o 1º card: Ativo, Pausado, Removido ou Não verificado "
     "(captcha/erro). Registra aviso do ML, motivo provável e ação sugerida. O .exe só verifica de novo se a última "
     "verificação tiver mais de 12 h; quadro \"fora do ar\" mostra os últimos 15 dias; substituto sugerido na faixa "
     "de preço ±20%."],
    ["Consolidação diária", "_historico_relatorios guarda o ÚLTIMO relatório de cada dia; historico_quadros.csv "
     "guarda 1 linha de métricas por dia; historico_vendas.csv 1 linha por pedido (a importação mais nova atualiza)."],
    ["Retenção (limpeza)", "Padrão: PDF 3 dias · HTML 3 dias (só se o dia já está em historico_quadros) · backup "
     "5 · status 3 · dados brutos 3. Ajustável na aba Metas. Destino: Lixeira. Nunca apaga planilha nem históricos."],
]

FORMATOS = [
    ["anuncios_status\\historico_status_anuncios.csv", "; · UTF-8 com BOM · acumula (≈6.150 linhas)",
     "verificado_em; item; nome_no_blog; titulo_card; link_afiliado; status; aviso_ml; motivo_provavel; "
     "acao_sugerida; anuncio_mlb; catalogo_mlb; catalogo_no_blog; titulo_ml; preco_ml; url_anuncio; http; url_final"],
    ["anuncios_status\\status_anuncios_AAAA-MM-DD_HHhMM.csv", "mesmas colunas", "Foto de uma verificação"],
    ["historico_consolidado\\historico_quadros.csv", "; · UTF-8 com BOM · 1 linha/dia",
     "dia; arquivo; gerado; ao_vivo; visitas; visitantes; vindas_link; cliques; possiveis; aprovadas; pendentes; "
     "outras_paginas"],
    ["vendas_historico\\historico_vendas.csv", "; · UTF-8 com BOM · 1 linha/pedido",
     "pedido; data; produto; loja; campanha; status; estado_ml; qtd; valor; comissao; fonte; primeira_vez; "
     "atualizado_em"],
    ["1- Gera_Relatorio\\dados_acessos", "acessos_AAAAMMDD_HHMM.json/.csv · compras_atribuidas_*.csv",
     "id; criado_em; tipo; visitante; sessao; pagina; origem; meio; campanha; conteudo; referencia; app; "
     "dispositivo; sistema; navegador; produto; link"],
    ["_historico_relatorios\\relatorio_acessos_anuncios_AAAA-MM-DD_HHhMM.html", "HTML autônomo (CSS embutido)",
     "Cards e tabelas lidos pelo 4_ (ler_relatorio)"],
    ["config_rastreio.json", "JSON · ÚNICA cópia, em programas_fontes_python",
     "site; pagina_blog; paginas_antigas; janela_compra_horas; etiqueta_afiliado; chave (secreta — não divulgar); "
     "anuncios (lista usada pelo gerador de links)"],
]

BUILD = [
    ["Instalar dependências", "python -m pip install openpyxl reportlab pyinstaller"],
    ["Recompilar o .exe (após mudar 3_ ou 6_)", "Clique duplo em programas_fontes_python\\11_compilar_exe_relatorio.bat "
     "(PyInstaller --onefile; guarda o .exe antigo em _backups_claude_30out e instala o novo em 1- Gera_Relatorio). "
     "Depois rodar 12_gerar_documentacao_exe_pdf.py. Detalhes: DOCUMENTACAO_EXECUTAVEL_*.pdf"],
    ["Instalar/reinstalar o rastreador", "WordPress > Snippets > Adicionar novo > colar o .php > trocar "
     "RASTREIO_CHAVE pela mesma chave do config_rastreio.json > Executar em todo o site > Salvar e ativar > "
     "LiteSpeed Cache: Purgar tudo"],
    ["Testar sem efeitos", "set PAINEL_SEM_LIMPEZA=1 e set PAINEL_NAO_ABRIR=1 antes do .bat; 7_ aceita --simular; "
     "o .exe aceita --demo (dados de exemplo)"],
    ["Regerar documentação", "python 9_gerar_documentacao_pdf.py  ·  python 10_gerar_documentacao_tecnica_pdf.py  ·  "
     "python 12_gerar_documentacao_exe_pdf.py"],
    ["Recuperar", "Planilha: _backup_painel · arquivos limpos: Lixeira · versões anteriores dos scripts e do .exe: "
     "0- Pendencias\\99_Programas_PY\\_backups_claude_30out (mover_painel_08-11 = estado antes da mudança de pasta)"],
]

SEGURANCA = [
    ["Chave da API", "Só no config_rastreio.json local e no snippet. Não colocar em PDF, print, e-mail ou "
     "repositório. Se vazar: trocar no snippet do WordPress e no config de programas_fontes_python."],
    ["Endpoint aberto /evento", "Qualquer um pode enviar evento (necessário para o navegador). Campos são "
     "limitados em tamanho e sanitizados; impacto máximo é ruído nas estatísticas."],
    ["Mercado Livre", "Sem login e sem API: só páginas públicas, com pausa de 2 s entre anúncios e sem contornar "
     "captcha → baixo risco de bloqueio. Se o ML pedir verificação, o item fica \"Não verificado\"."],
    ["Escalabilidade", "Etapa 1 cresce linear com os produtos (≈3 s cada; 213 = ≈10 min). Tabela WP limitada a "
     "400 dias e exportação a 100.000 linhas."],
    ["Ponto único de falha", "Tudo roda no mini PC; o histórico permanente está em CSV/XLSX locais — incluir "
     "Relatorios_Diarios_Anuncios no backup regular."],
    ["Caminhos fixos", "3_ usa D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios fixo (o .exe roda de outra pasta). "
     "Os demais calculam a partir da própria pasta (RELAT = pasta de cima, BASE = D:\\Projeto_Blog_Comprenolink). Renomear "
     "pastas exige ajustar 3_ e recompilar."],
]

# Pedido do dono (08/11/2026): tudo o que é necessário para EXECUTAR fica junto em programas_fontes_python
NECESSARIOS = [
    ["ATUALIZAR_PAINEL.bat, 3_ a 8_ (.py/.ps1)", "SIM", "programas_fontes_python",
     "Os programas do painel. Precisam estar juntos: o .bat chama 5_–8_ pela própria pasta; 4_ importa 3_; 3_ importa 6_."],
    ["config_rastreio.json", "SIM", "programas_fontes_python (FONTE ÚNICA, copiado em 08/11/2026 de 1- Gera_Relatorio)",
     "Site, página do guia, páginas antigas, janela de compra, chave da API. Lido pelo 3_ (relatório) e pelo 6_ "
     "(página do guia), inclusive quando rodam dentro do .exe. É a ÚNICA cópia (sem reserva desde 08/11/2026). "
     "Se faltar, o relatório para com aviso \"Não encontrei o config_rastreio.json\"."],
    ["11_compilar_exe_relatorio.bat + 1_relatorio_acessos_anuncios.spec", "Só para compilar", "programas_fontes_python",
     "Recriam o .exe. O .spec é registro do último build."],
    ["9_, 10_, 12_ (geradores de PDF)", "Só para documentar", "programas_fontes_python",
     "Precisam das fontes Arial do Windows (C:\\Windows\\Fonts) e do reportlab."],
    ["1_relatorio_acessos_anuncios.exe", "SIM (relatório diário)", "1- Gera_Relatorio (fica lá)",
     "O dono usa por lá; o .exe procura o config primeiro em programas_fontes_python."],
]

# Validação de 08/11/2026: comparação por nome e SHA-256 de todos os arquivos da pasta com D:\Projeto_Blog_Comprenolink
VALIDACAO = [
    ["10_Rastreamento_anuncios\\relatorio_acessos_anuncios.exe", "Cópia antiga (21/10) do .exe do relatório, "
     "idêntica ao backup _ANTES_02nov; gravava nos caminhos antigos", "Enviado à Lixeira"],
    ["anuncios_status\\links_anuncios_2026-10-29_06h48.csv", "Idêntico a 10_Rastreamento_anuncios\\links_anuncios.csv "
     "(pertence ao gerador de links; nenhum programa do painel lia)", "Enviado à Lixeira"],
    ["1- Gera_Relatorio\\config_rastreio.json", "Reserva idêntica ao config de programas_fontes_python",
     "Enviado à Lixeira; .exe testado e lê só o de programas_fontes_python"],
    ["python\\__pycache__\\3_/4_/6_/7_*.pyc", "Cache dos scripts que saíram de D:\\Projeto_Blog_Comprenolink\\python",
     "Enviado à Lixeira"],
    ["0- Pendencias\\99_Programas_PY\\_backups_claude_30out\\...", "Backups de versões ANTERIORES (conteúdo "
     "diferente do atual)", "Mantidos de propósito (recuperação)"],
    ["10_Rastreamento_anuncios\\config_rastreio.json", "Config do gerador de links (outra rotina, conteúdo "
     "diferente)", "Mantido"],
    ["Gera_Estrutura_Diretorio - Copia.bat (raiz)", "Mesmo nome, conteúdo diferente (lista a raiz)", "Mantido"],
]

NAO_NECESSARIOS = [
    ["Planilha, PDFs, CSVs, HTMLs (anuncios_status, vendas_*, historico_*, _historico_relatorios, _backup_painel)",
     "São DADOS, não programas. Ficam nas subpastas de Relatorios_Diarios_Anuncios; os programas acham pela pasta "
     "de cima (RELAT)."],
    ["1- Gera_Relatorio\\dados_acessos", "Cópias brutas geradas pelo relatório (o 3_ grava sempre lá, rodando como "
     ".exe ou .py). Dados, não execução."],
    ["10_Rastreamento_anuncios\\config_rastreio.json", "Versão antiga, usada pelo gerador de links (outra rotina). "
     "Não é lida pelo painel."],
    ["10_Rastreamento_anuncios\\1_snippet_wordpress_rastreador.php", "Roda no WordPress (Hostinger), não no PC. "
     "É a fonte do rastreador, para reinstalar se preciso."],
    ["9_Manutenção_Blog\\2_DADOS\\Blog_WordPress\\backups\\pagina_*", "Opcional: o 6_ lê para preencher o código de "
     "catálogo; sem eles a verificação funciona e só a coluna catalogo_no_blog fica vazia."],
    ["Bibliotecas Python (openpyxl, reportlab, PyInstaller)", "Instaladas no Python da máquina (pip), não são "
     "arquivos do projeto."],
    ["D:\\Projeto_Blog_Comprenolink\\python (2_gerar_links, gerar_relatorio_blog_v4, test_blog_seo, __pycache__)",
     "Outras rotinas (links e SEO). Não fazem parte do painel."],
    ["__pycache__ em programas_fontes_python", "Criado sozinho pelo Python; pode ser apagado sem problema."],
]


def montar():
    os.makedirs(PASTA_DOCS, exist_ok=True)
    doc = SimpleDocTemplate(SAIDA, pagesize=landscape(A4), leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                            topMargin=1.2 * cm, bottomMargin=1.5 * cm,
                            title="Documentação técnica e infraestrutura - Relatório Diário de Anúncios",
                            author="comprenolink.net")
    st = [Spacer(1, 3 * cm), P("Relatório Diário de Anúncios", "titulo"), Spacer(1, 6),
          P("Documentação técnica de criação e desenho de infraestrutura", "sub"), Spacer(1, 4),
          P("Complementa a DOCUMENTACAO_PROGRAMAS (visão para o usuário)", "sub"), Spacer(1, 4),
          P(f"Versão de {HOJE:%d/%m/%Y}", "sub"), Spacer(1, 1 * cm)]
    st.append(tabela(["Seção", "Conteúdo"], [
        ["1", "Desenho de infraestrutura (onde cada peça roda e como se comunicam)"],
        ["2", "Fluxo de dados ponta a ponta e dependências entre programas"],
        ["3", "Stack tecnológica e versões"],
        ["4", "Componente WordPress: snippet, tabela, API e privacidade"],
        ["5", "Módulos: principais funções de cada programa"],
        ["6", "Algoritmos e regras de negócio"],
        ["7", "Formatos de dados e configuração"],
        ["8", "Build, instalação, testes e recuperação"],
        ["9", "Segurança, limites e riscos"],
        ["10", "Arquivos necessários para execução (o que fica junto e o que não precisa)"]], [2, 24.5]))
    st.append(PageBreak())

    st.append(P("1. Desenho de infraestrutura", "h1"))
    st.append(diagrama_infra())
    st.append(Spacer(1, 0.25 * cm))
    st.append(tabela(["Nº", "Conexão", "Protocolo / como", "Quando"], CONEXOES, [1.0, 6.0, 13.5, 6.0]))
    st.append(PageBreak())

    st.append(P("2. Fluxo de dados ponta a ponta", "h1"))
    st.append(diagrama_fluxo())
    st.append(Spacer(1, 0.3 * cm))
    st.append(P("Dependências entre programas (quem chama / importa quem)", "h2"))
    st.append(diagrama_dependencias())
    st.append(PageBreak())

    st.append(P("3. Stack tecnológica e versões", "h1"))
    st.append(tabela(["Camada", "Tecnologia / versão", "Papel"], STACK, [4.0, 15.0, 7.5]))
    st.append(Spacer(1, 0.4 * cm))
    st.append(P("4. Componente WordPress (rastreador)", "h1"))
    st.append(tabela(["Item", "Detalhe"], WP, [5.5, 21.0]))
    st.append(PageBreak())

    st.append(P("5. Módulos: principais funções", "h1"))
    st.append(tabela(["Programa", "Funções / técnicas"], FUNCOES, [6.0, 20.5]))
    st.append(PageBreak())

    st.append(P("6. Algoritmos e regras de negócio", "h1"))
    st.append(tabela(["Regra", "Como funciona"], REGRAS, [5.5, 21.0]))
    st.append(PageBreak())

    st.append(P("7. Formatos de dados e configuração", "h1"))
    st.append(tabela(["Arquivo", "Formato", "Colunas / campos"], FORMATOS, [7.5, 5.5, 13.5]))
    st.append(PageBreak())

    st.append(P("8. Build, instalação, testes e recuperação", "h1"))
    st.append(tabela(["Tarefa", "Como fazer"], BUILD, [5.5, 21.0]))
    st.append(Spacer(1, 0.4 * cm))
    st.append(P("9. Segurança, limites e riscos", "h1"))
    st.append(tabela(["Tema", "Situação / cuidado"], SEGURANCA, [5.0, 21.5], fundo=LARANJA))
    st.append(PageBreak())

    st.append(P("10. Arquivos necessários para execução", "h1"))
    st.append(P("Regra (pedido do dono, 08/11/2026): tudo o que é necessário para EXECUTAR os programas fica junto "
                "em <b>Relatorios_Diarios_Anuncios\\programas_fontes_python</b>. O que não precisa estar lá está "
                "listado na segunda tabela, com o motivo."))
    st.append(tabela(["Arquivo", "Necessário?", "Onde fica", "Observação"], NECESSARIOS, [6.0, 2.8, 6.2, 11.5]))
    st.append(Spacer(1, 0.4 * cm))
    st.append(P("Não precisam ficar em programas_fontes_python", "h2"))
    st.append(tabela(["Arquivo / pasta", "Por quê"], NAO_NECESSARIOS, [9.0, 17.5]))
    st.append(Spacer(1, 0.4 * cm))
    st.append(P("Validação de duplicatas (08/11/2026)", "h2"))
    st.append(P("Todos os arquivos de Relatorios_Diarios_Anuncios foram comparados por nome e por conteúdo (SHA-256) "
                "com toda a estrutura D:\\Projeto_Blog_Comprenolink. Resultado: nenhuma duplicata dentro da pasta; fora dela, o "
                "que foi encontrado e o que foi feito:"))
    st.append(tabela(["Arquivo encontrado", "O que era", "Ação"], VALIDACAO, [8.0, 11.5, 7.0]))
    doc.build(st, onFirstPage=rodape, onLaterPages=rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    montar()
