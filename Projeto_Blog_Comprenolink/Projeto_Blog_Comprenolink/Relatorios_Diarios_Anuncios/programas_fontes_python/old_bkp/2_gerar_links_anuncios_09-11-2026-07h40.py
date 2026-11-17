"""
Gera um link ETIQUETADO (UTM) para cada anúncio/vídeo/rede, apontando para
https://comprenolink.net/melhores-produtos-mercado-livre-2026/.
Cada lugar onde você divulga o blog deve usar o SEU link — é assim que o
relatório sabe de qual anúncio cada visitante veio.

Uso:
    python 2_gerar_links_anuncios.py
    python 2_gerar_links_anuncios.py --origem kwai --meio video --campanha ps5 --conteudo 04_ps5
"""
import argparse
import csv
import html
import json
import os
import sys
from datetime import datetime
from urllib.parse import urlencode, urlsplit, urlunsplit, parse_qsl

# No .exe (PyInstaller) a pasta é a do próprio executável
PASTA = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
# Config: ao lado do script/.exe; se não houver, usa o da pasta exe_gera_relatorio
CONFIG = os.path.join(PASTA, "config_rastreio.json")
if not os.path.exists(CONFIG):
    CONFIG = os.path.join(os.path.dirname(PASTA), "exe_gera_relatorio", "config_rastreio.json")
# Todos os links levam para esta página (config 'pagina_blog')
PAGINA_PADRAO = "https://comprenolink.net/melhores-produtos-mercado-livre-2026/"
# Saída em D:\Projeto_Blog_Comprenolink (pasta acima), com data/hora da geração no nome
PASTA_SAIDA = os.path.dirname(PASTA)
AGORA = datetime.now()
SAIDA_HTML = os.path.join(PASTA_SAIDA, AGORA.strftime("links_anuncios_%Y-%m-%d_%Hh%M.html"))
SAIDA_CSV = os.path.join(PASTA_SAIDA, AGORA.strftime("links_anuncios_%Y-%m-%d_%Hh%M.csv"))


def montar_link(base, origem, meio, campanha, conteudo=""):
    partes = urlsplit(base)
    qs = dict(parse_qsl(partes.query))
    qs.update({"utm_source": origem, "utm_medium": meio, "utm_campaign": campanha})
    if conteudo:
        qs["utm_content"] = conteudo
    return urlunsplit((partes.scheme, partes.netloc, partes.path, urlencode(qs), ""))


def main():
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Gera links UTM por anúncio")
    ap.add_argument("--origem")
    ap.add_argument("--meio", default="video")
    ap.add_argument("--campanha")
    ap.add_argument("--conteudo", default="")
    args = ap.parse_args()

    with open(CONFIG, encoding="utf-8") as f:
        cfg = json.load(f)
    base = cfg.get("pagina_blog") or PAGINA_PADRAO
    print(f"🔗 Página de destino dos links: {base}\n")

    if args.origem and args.campanha:
        print(montar_link(base, args.origem.lower(), args.meio.lower(), args.campanha, args.conteudo))
        print("\nDica: adicione este anúncio em config_rastreio.json para ele aparecer na lista.")
        return

    linhas = []
    for a in cfg["anuncios"]:
        link = montar_link(base, a["origem"], a["meio"], a["campanha"], a.get("conteudo", ""))
        linhas.append({**a, "link": link})
        print(f"[{a['origem']:>9} | {a.get('conteudo', '')}]\n  {link}\n")

    with open(SAIDA_CSV, "w", newline="", encoding="utf-8-sig") as f:
        w = csv.DictWriter(f, fieldnames=["origem", "meio", "campanha", "conteudo", "link"], delimiter=";")
        w.writeheader()
        w.writerows(linhas)

    itens = "".join(
        f"""<tr><td><b>{html.escape(l['origem'])}</b><br><small>{html.escape(l['meio'])}</small></td>
<td>{html.escape(l['campanha'])}<br><small>{html.escape(l.get('conteudo', ''))}</small></td>
<td><code>{html.escape(l['link'])}</code></td>
<td><button onclick="copiar(this)" data-l="{html.escape(l['link'])}">Copiar</button></td></tr>"""
        for l in linhas
    )
    with open(SAIDA_HTML, "w", encoding="utf-8") as f:
        f.write(f"""<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><title>Links por Anúncio — {AGORA:%d/%m/%Y %H:%M}</title>
<style>
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#f8f9fa;color:#212529;margin:0;padding:24px}}
.c{{max-width:1100px;margin:0 auto}}
h1{{background:linear-gradient(135deg,#ffe600,#ffd000);color:#2d3277;padding:20px;border-radius:12px;font-size:22px}}
table{{width:100%;border-collapse:collapse;background:#fff;border-radius:10px;overflow:hidden}}
td,th{{padding:12px;border-bottom:1px solid #eee;text-align:left;vertical-align:top}}
th{{background:#2d3277;color:#fff}} code{{word-break:break-all;color:#1d4ed8}} small{{color:#6c757d}}
button{{background:#3483fa;color:#fff;border:0;border-radius:6px;padding:8px 14px;font-weight:bold;cursor:pointer}}
.dica{{background:#fff8d6;border:1px solid #ffe07a;padding:14px;border-radius:8px;margin:16px 0}}
</style></head><body><div class="c">
<h1>🔗 Links Etiquetados por Anúncio<br><small style="color:#2d3277;font-size:15px">📅 Gerado em: {AGORA:%d/%m/%Y às %H:%M}</small></h1>
<div class="dica">Use <b>um link diferente em cada anúncio/vídeo/bio</b>. Se o TikTok não permitir link no vídeo,
coloque o link da bio e mencione o vídeo — ou use o encurtador que preferir apontando para o link abaixo.</div>
<table><tr><th>Origem</th><th>Campanha / Anúncio</th><th>Link para usar</th><th></th></tr>{itens}</table>
</div><script>
function copiar(b){{navigator.clipboard.writeText(b.dataset.l).then(function(){{b.textContent='Copiado ✓';setTimeout(function(){{b.textContent='Copiar'}},1500)}})}}
</script></body></html>""")

    print("=" * 60)
    print(f"✅ {len(linhas)} links gerados")
    print(f"📄 {SAIDA_HTML}")
    print(f"📄 {SAIDA_CSV}")


if __name__ == "__main__":
    try:
        main()
    except SystemExit as e:
        if e.code not in (None, 0):
            print(e.code)
    finally:
        if getattr(sys, "frozen", False):  # duplo clique no .exe: não fechar a janela sozinho
            input("\nPressione ENTER para fechar...")
