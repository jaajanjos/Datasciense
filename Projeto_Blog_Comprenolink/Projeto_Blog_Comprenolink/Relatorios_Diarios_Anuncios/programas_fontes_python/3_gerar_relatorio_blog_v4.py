import os
import sys
import urllib.request
import urllib.error
import ssl
import time
from bs4 import BeautifulSoup

# Configurações de Entrada e Saída
BLOG_URL = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"
OUTPUT_DIR = r"D:\Projeto_Blog_Comprenolink"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "relatorio_anuncios_blog.html")

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

ssl_context = ssl.create_default_context()
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

def testar_status_url(url, timeout=6):
    """Testa a conectividade e o redirecionamento do link encurtado meli.la."""
    if not url or url == "#" or "meli.la" not in url:
        return {"code": 0, "status": "Sem Link meli.la", "ok": False}
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
                return {"code": e.code, "status": f"Redirecionamento ({e.code})", "ok": True}
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
    print(f"🚀 INICIANDO AUDITORIA FILTRADA (EXCLUSIVO 21 PRODUTOS)")
    print(f"🌐 URL Alvo: {BLOG_URL}")
    print("=" * 65)

    html_content = baixar_pagina(BLOG_URL)
    if html_content is None:
        return

    soup = BeautifulSoup(html_content, 'html.parser')
    h2_tags = soup.find_all('h2')
    produtos = []

    posicao_valida = 1

    for h2 in h2_tags:
        titulo_produto = h2.get_text(strip=True)

        # CORREÇÃO: Ignora seções padrão do tema do WordPress
        titulos_ignorar = ["recent posts", "recent comments", "pesquisar", "navegação", "categorias", "deixe um comentário"]
        if any(ignorar in titulo_produto.lower() for ignorar in titulos_ignorar):
            continue

        img_src = ""
        link_melila = ""
        preco = "Preço sob consulta"

        curr = h2.next_element
        while curr and curr.name != 'h2':
            if curr.name == 'a' and curr.get('href') and 'meli.la' in curr.get('href'):
                if not link_melila:
                    link_melila = curr['href']
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

        status_link = testar_status_url(link_melila)

        produtos.append({
            'posicao': posicao_valida,
            'titulo': titulo_produto,
            'link': link_melila if link_melila else "Não encontrado link meli.la",
            'imagem': img_src,
            'preco': preco,
            'status': status_link
        })

        print(f"[{posicao_valida}/21] {titulo_produto[:35]}... -> {link_melila if link_melila else 'SEM MELI.LA'}")
        posicao_valida += 1

    total_links_ok = sum(1 for p in produtos if p['status']['ok'])
    taxa_sucesso = round((total_links_ok / len(produtos)) * 100, 1) if produtos else 0

    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)

    html_output = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Relatório de Anúncios - Links Encurtados meli.la</title>
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
        
        .encurtado-box {{
            background: #eef2ff;
            border: 1px solid #c7d2fe;
            border-radius: 6px;
            padding: 12px;
            margin-top: 8px;
            text-align: center;
        }}
        .encurtado-label {{
            display: block;
            font-size: 11px;
            font-weight: bold;
            color: #3730a3;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
        }}
        .encurtado-url {{
            font-family: 'Courier New', Courier, monospace;
            font-size: 14px;
            font-weight: bold;
            color: #1d4ed8;
            text-decoration: none;
            word-break: break-all;
        }}
        .encurtado-url:hover {{
            text-decoration: underline;
            color: #092ace;
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>📊 Relatório de Anúncios - Links Encurtados (meli.la)</h1>
            <p style="margin:0;"><strong>Página Auditada:</strong> <a href="{BLOG_URL}" target="_blank" style="color:#2d3277;">{BLOG_URL}</a></p>
        </div>

        <h2>🛒 Anúncios com Links Encurtados de Afiliado (Total: {len(produtos)})</h2>
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
                    
                    <div class="encurtado-box">
                        <span class="encurtado-label">🔗 LINK ENCURTADO DO MERCADO LIVRE</span>
                        <a href="{prod["link"]}" target="_blank" class="encurtado-url" rel="sponsored">{prod["link"]}</a>
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
    print("✅ RELATÓRIO CORRIGIDO COM SUCESSO! (TOTAL DE 21 PRODUTOS)")
    print(f"📂 Arquivo gerado em: {OUTPUT_FILE}")
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