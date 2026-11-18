import sys, json, datetime; sys.stdout.reconfigure(encoding="utf-8")
sys.path.insert(0, r"D:\Projeto_Blog_Comprenolink\Gestao_Anuncios_Blog\1_PROGRAMAS\Blog_WordPress")
import gerenciar_blog as g
cfg = g.carregar_config()
agora = datetime.datetime.now().strftime("%Y-%m-%d_%Hh%M%S")
lista = g.requisitar(cfg, "GET", "/wp-json/code-snippets/v1/snippets")
json.dump(lista, open(rf"D:\Projeto_Blog_Comprenolink\Gestao_Anuncios_Blog\2_DADOS\Blog_WordPress\backups\snippets_{agora}.json", "w", encoding="utf-8"), ensure_ascii=False)
print("backup snippets:", len(lista))
codigo = open(r"D:\Projeto_Blog_Comprenolink\Gestao_Anuncios_Blog\2_DADOS\Blog_WordPress\snippets_novos\meta_pixel_comprenolink.php", encoding="utf-8").read()
r = g.requisitar(cfg, "POST", "/wp-json/code-snippets/v1/snippets",
                 {"name": "Meta Pixel + aviso de cookies (comprenolink)", "code": codigo, "scope": "front-end", "active": False,
                  "desc": "Pixel 1128603339935423; evento SaidaML; carrega só após Aceitar. Criado 17/11/2026."})
print(r.get("id"), r.get("name"), r.get("active"), r.get("code_error"))
