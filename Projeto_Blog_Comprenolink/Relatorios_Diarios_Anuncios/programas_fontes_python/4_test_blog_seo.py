import os
import sys
import urllib.request
import urllib.error
import ssl
import time
from bs4 import BeautifulSoup

# Configurações de Entrada e Saída
BLOG_URL = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"
OUTPUT_DIR = r"D:\mercado_livre"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "relatorio_anuncios_blog.html")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# Configuração de SSL para testes seguros de conectividade
ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def testar_status_url(url, timeout=6):
    """Testa a conectividade do link de afiliado e valida se o redirecionamento está ativo."""
    if not url or url == "#":
        return {"code": 0, "status": "Link Ausente", "ok": False}
    try:
        req = urllib.request.Request(url, headers=HEADERS, method='HEAD')
        with urllib.request.urlopen(req, context=ssl_context, timeout=timeout) as response:
            return {"code": response.getcode(), "status": f"Ativo (HTTP {response.getcode()})", "ok": True}
    except Exception:
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ssl_context, timeout=timeout) as response:
                return {"code": response.getcode(), "status": f"Ativo (HTTP {response.getcode()})", "ok": True}
        except urllib.error.HTTPError as e:
            if e.code in [301, 302, 307, 308]:
                return {"code": e.code, "status": f"Redirecionamento (HTTP {e.code})", "ok": True}
            return {"code": e.code, "status": f"Erro HTTP {e.code}", "ok": False}
        except Exception:
            return {"code": "Erro", "status": "Inacessível / Timeout", "ok": False}

def baixar_pagina(url, tentativas=3, espera=5):
    """Baixa a página do blog, tentando de novo em caso de falha passageira de internet/DNS."""
    for n in range(1, tentativas + 1):
        try:
            req = urllib.request.Request(url, headers=HEADERS)
            with urllib.request.urlopen(req, context=ssl_context, timeout=30) as response:
                return response.read().decode('utf-8')
        except Exception as e:
            sem_internet = "getaddrinfo" in str(e) or "11001" in str(e) or "11002" in str(e)
            motivo = "sem conexão / DNS não encontrou o site" if sem_internet else str(e)
            print(f"⚠️ Tentativa {n}/{tentativas} falhou: {motivo}")
            if n < tentativas:
                print(f"   Tentando de novo em {espera}s...")
                time.sleep(espera)
    print("❌ Não foi possível acessar o blog. Verifique a internet deste computador e rode de novo.")
    return None

def gerar_relatorio_completo():
    print("=" * 65)
    print(f"🚀 INICIANDO AUDITORIA DO BLOG E EXTRAÇÃO DOS LINKS DE AFILIADOS")
    print(f"🌐 URL Alvo: {BLOG_URL}")
    print("=" * 65)

    start_time = time.time()
    blog_status = testar_status_url(BLOG_URL)
    tempo_resposta = round((time.time() - start_time) * 1000, 2)

    html_content = baixar_pagina(BLOG_URL)
    if html_content is None:
        return

    soup = BeautifulSoup(html_content, 'html.parser')

    # SEO Metadata
    page_title = soup.find('title').get_text(strip=True) if soup.find('title') else "Sem Título"
    canonical = soup.find('link', rel='canonical')
    canonical_url = canonical['href'] if canonical else "Não encontrada"

    # Mapeamento dos 21 Anúncios / Produtos
    h2_tags = soup.find_all('h2')
    produtos = []
    
    print(f"\n🔍 Processando {len(h2_tags)} anúncios e extraindo URLs de afiliados...\n")

    for idx, h2 in enumerate(h2_tags, 1):
        titulo_produto = h2.get_text(strip=True)
        
        img_src = ""
        link_afiliado = ""
        preco = "Preço sob consulta"

        curr = h2.next_element
        while curr and curr.name != 'h2':
            if curr.name == 'a' and ('meli.la' in curr.get('href', '') or 'mercadolivre' in curr.get('href', '')):
                if not link_afiliado:
                    link_afiliado = curr['href']
                img = curr.find('img')
                if img and img.get('src'):
                    img_src = img['src']
            elif curr.name == 'img' and not img_src:
                img_src = curr.get('src', '')
            elif curr.name in ['div', 'p'] and ('R$' in curr.get_text()):
                text_clean = curr.get_text(strip=True)
                if 'R$' in text_clean and len(text_clean) < 35:
                    preco = text_clean
            curr = curr.next_element

        print(f"[{idx}/{len(h2_tags)}] Mapeado: {titulo_produto[:40]}... -> {link_afiliado}")
        status_link = testar_status_url(link_afiliado) if link_afiliado else {"code": 0, "status": "Sem Link", "ok": False}

        produtos.append({
            'posicao': idx,
            'titulo': titulo_produto,
            'link': link_afiliado if link_afiliado else "Nenhum link configurado",
            'imagem': img_src,
            'preco': preco,
            'status': status_link
        })

    total_links_ok = sum(1 for p in produtos if p['status']['ok'])
    taxa_sucesso = round((total_links_ok / len(produtos)) * 100, 1) if produtos else 0

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    html_output = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Anúncios e Links de Afiliados - Blog</title>
    <style>
        body {{
            font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
            background-color: #f8f9fa;
            color: #212529;
            margin: 0;
            padding: 25px;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
        }}
        .header {{
            background: linear-gradient(135deg, #ffe600 0%, #ffd000 100%);
            color: #2d3277;
            padding: 25px;
            border-radius: 12px;
            margin-bottom: 25px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        }}
        .header h1 {{ margin: 0 0 10px 0; font-size: 26px; }}

        .kpi-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
            gap: 15px;
            margin-bottom: 25px;
        }}
        .kpi-card {{
            background: #fff;
            padding: 20px;
            border-radius: 10px;
            border: 1px solid #e9ecef;
            box-shadow: 0 2px 6px rgba(0,0,0,0.04);
        }}
        .kpi-title {{ font-size: 13px; color: #6c757d; text-transform: uppercase; font-weight: bold; }}
        .kpi-value {{ font-size: 24px; font-weight: bold; margin-top: 8px; color: #1a1a1a; }}
        .status-ok {{ color: #198754; }}
        .status-err {{ color: #dc3545; }}

        .badge-status {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 12px;
            font-weight: bold;
        }}
        .badge-success {{ background: #d1e7dd; color: #0f5132; }}
        .badge-danger {{ background: #f8d7da; color: #842029; }}

        .grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
            gap: 20px;
        }}
        .card {{
            background: #fff;
            border-radius: 10px;
            padding: 20px;
            border: 1px solid #e0e0e0;
            display: flex;
            flex-direction: column;
            justify-content: space-between;
            transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-3px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }}
        .card img {{
            max-width: 100%;
            height: 180px;
            object-fit: contain;
            margin-bottom: 15px;
        }}
        .price {{ font-size: 22px; font-weight: bold; color: #00a650; margin: 10px 0; }}
        .btn {{
            display: block;
            text-align: center;
            background: #3483fa;
            color: #fff;
            text-decoration: none;
            padding: 10px;
            border-radius: 6px;
            font-weight: bold;
            margin-bottom: 12px;
        }}
        .btn:hover {{ background: #2968c8; }}
        
        /* Estilo da caixa inferior do link de afiliado */
        .affiliate-link-box {{
            background: #f1f3f5;
            border: 1px solid #dee2e6;
            border-radius: 6px;
            padding: 10px;
            font-size: 12px;
            word-break: break-all;
            color: #495057;
        }}
        .affiliate-link-box strong {{
            display: block;
            color: #2d3277;
            margin-bottom: 4px;
            font-size: 11px;
            text-transform: uppercase;
        }}
        .affiliate-link-box a {{
            color: #0d6efd;
            text-decoration: none;
            font-family: monospace;
        }}
        .affiliate-link-box a:hover {{ text-decoration: underline; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Relatório de Anúncios e Links de Afiliados</h1>
            <p style="margin:0;"><strong>Página Auditada:</strong> <a href="{BLOG_URL}" target="_blank" style="color:#2d3277;">{BLOG_URL}</a></p>
        </div>

        <div class="kpi-grid">
            <div class="kpi-card">
                <div class="kpi-title">Servidor Blog</div>
                <div class="kpi-value {'status-ok' if blog_status['ok'] else 'status-err'}">
                    {'ONLINE' if blog_status['ok'] else 'OFFLINE'}
                </div>
                <small style="color:#6c757d;">Respondeu em {tempo_resposta} ms</small>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Total de Anúncios</div>
                <div class="kpi-value">{len(produtos)} Produtos</div>
                <small style="color:#6c757d;">Mapeados na página</small>
            </div>
            <div class="kpi-card">
                <div class="kpi-title">Links de Afiliados</div>
                <div class="kpi-value status-ok">{taxa_sucesso}%</div>
                <small style="color:#6c757d;">{total_links_ok} de {len(produtos)} ativos</small>
            </div>
        </div>

        <h2>🛒 Anúncios Mapeados com Links de Afiliados Visíveis</h2>
        <div class="grid">
"""

    for prod in produtos:
        img_tag = f'<img src="{prod["imagem"]}" alt="{prod["titulo"]}">' if prod["imagem"] else '<div style="height:180px;background:#eee;display:flex;align-items:center;justify-content:center;color:#888;">Sem Imagem</div>'
        badge_cls = "badge-success" if prod["status"]["ok"] else "badge-danger"

        html_output += f"""
            <div class="card">
                <div>
                    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:10px;">
                        <span style="font-size:12px; font-weight:bold; color:#6c757d;">Anúncio #{prod["posicao"]}</span>
                        <span class="badge-status {badge_cls}">{prod["status"]["status"]}</span>
                    </div>
                    {img_tag}
                    <h3 style="font-size:16px; margin:0 0 8px 0; line-height:1.4;">{prod["titulo"]}</h3>
                </div>
                <div>
                    <div class="price">{prod["preco"]}</div>
                    <a href="{prod["link"]}" target="_blank" class="btn" rel="sponsored">Testar Redirecionamento</a>
                    
                    <!-- EXIBIÇÃO DO LINK DE AFILIADO NA PARTE INFERIOR -->
                    <div class="affiliate-link-box">
                        <strong>🔗 Link de Afiliado Configurado:</strong>
                        <a href="{prod["link"]}" target="_blank" rel="sponsored">{prod["link"]}</a>
                    </div>
                </div>
            </div>
"""

    html_output += """
        </div>
    </div>
</body>
</html>
"""

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        f.write(html_output)

    print("\n" + "=" * 65)
    print("✅ RELATÓRIO REGERADO COM SUCESSO!")
    print(f"📂 Arquivo salvo em: {OUTPUT_FILE}")
    print("=" * 65)

if __name__ == "__main__":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    try:
        gerar_relatorio_completo()
    finally:
        if getattr(sys, "frozen", False):  # duplo clique no .exe: não fechar a janela sozinho
            input("\nPressione ENTER para fechar...")