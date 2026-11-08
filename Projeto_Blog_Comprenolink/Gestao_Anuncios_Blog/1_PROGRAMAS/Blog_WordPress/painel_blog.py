# -*- coding: utf-8 -*-
"""
PAINEL DO BLOG - aplicação web local (sem instalar nada) para gerenciar
https://comprenolink.net/melhores-produtos-mercado-livre-2026/ sem usar linha de comando.

Abre um servidor só na sua máquina (http://127.0.0.1:8842) e o navegador sozinho.
Reaproveita toda a lógica de leitura/edição/publicação de gerenciar_blog.py (mesma pasta).

Uso:  duplo clique em PAINEL_BLOG.bat (ou no PainelBlog.exe compilado)
"""
import html
import json
import os
import re
import socket
import sys
import threading
import time
import webbrowser
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

PASTA = os.path.dirname(sys.executable if getattr(sys, "frozen", False) else os.path.abspath(__file__))
sys.path.insert(0, PASTA)
import gerenciar_blog as gb  # noqa: E402  (mesma pasta; reaproveita parsing/API/publicação)

PORTA = 8842
UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/120.0.0.0 Safari/537.36")


# ============================================================== busca no Mercado Livre
def _meta(texto, chave, attr="property"):
    for padrao in (rf'<meta[^>]*{attr}="{re.escape(chave)}"[^>]*content="([^"]*)"',
                   rf'<meta[^>]*content="([^"]*)"[^>]*{attr}="{re.escape(chave)}"'):
        m = re.search(padrao, texto, re.I)
        if m:
            return html.unescape(m.group(1)).strip()
    return ""


def _preco_formatado(texto):
    m = (re.search(r'"price":"?(\d+(?:\.\d+)?)"?', texto) or
         re.search(r'<meta[^>]*itemprop="price"[^>]*content="([\d.]+)"', texto))
    if not m:
        return ""
    try:
        v = float(m.group(1))
        return "R$ " + f"{v:,.2f}".replace(",", "§").replace(".", ",").replace("§", ".")
    except ValueError:
        return ""


def _caracteristicas(texto):
    pares = re.findall(
        r'class="andes-table__header[^"]*"[^>]*>\s*(?:<[^>]+>)*\s*([^<]{2,40}?)\s*(?:<[^>]+>)*\s*</th>'
        r'.*?class="andes-table__column[^"]*--value"[^>]*>\s*(?:<[^>]+>)*\s*([^<]{1,80}?)\s*(?:<[^>]+>)*\s*</td>',
        texto, re.S)
    itens = [f"{html.unescape(k).strip()}: {html.unescape(v).strip()}" for k, v in pares[:8]
             if k.strip() and v.strip()]
    return itens


def buscar_mercado_livre(link):
    if not re.match(r'^https?://', link or ""):
        raise gb.Erro("Cole um link que comece com http:// ou https:// (o link de afiliado ou o link do anúncio).")
    req = __import__("urllib.request", fromlist=["Request"]).Request(
        link, headers={"User-Agent": UA, "Accept-Language": "pt-BR,pt;q=0.9"})
    try:
        with __import__("urllib.request", fromlist=["urlopen"]).urlopen(req, timeout=20) as r:
            link_final = r.geturl()
            texto = r.read().decode("utf-8", "replace")
    except Exception as e:
        raise gb.Erro(f"Não consegui abrir esse link ({e}). Confira se ele está certo e se o site não está bloqueando "
                      "o acesso automático — nesse caso, preencha os campos manualmente.")
    nome = _meta(texto, "og:title")
    if not nome:
        m = re.search(r'<title>([^<]+)</title>', texto, re.I)
        nome = html.unescape(m.group(1)).strip() if m else ""
    if not nome:
        raise gb.Erro("Não encontrei um produto nessa página. Confira o link (copie de dentro do anúncio do Mercado "
                      "Livre, não da busca) ou preencha os campos manualmente.")
    imagem = _meta(texto, "og:image")
    descricao = _meta(texto, "og:description") or _meta(texto, "description", "name")
    if re.search(r'encontre todos os produtos de .* em um só lugar', descricao, re.I):
        descricao = ""  # página de rastreio/social, não a do produto: descrição genérica, descartar
    preco = _preco_formatado(texto)
    beneficios = _caracteristicas(texto)
    if not beneficios and descricao:
        partes = [p.strip(" .") for p in re.split(r'[|.]', descricao) if len(p.strip(" .")) > 3]
        beneficios = partes[:4]
    return {"link_final": link_final, "nome": nome, "imagem": imagem, "preco": preco,
            "descricao": descricao[:300], "beneficios": beneficios[:8]}


# ============================================================== apoio aos dados
def _cfg_resumo():
    cfg = gb.carregar_config()
    return {"configurado": bool(cfg["usuario"] and cfg["senha_aplicativo"]),
            "usuario": cfg["usuario"], "site": cfg["site"], "pagina_id": cfg["pagina_id"]}


def api_testar():
    cfg = gb.carregar_config()
    return {"ok": True, **gb.testar_conexao(cfg)}


def api_listar():
    cfg = gb.carregar_config()
    p = gb.baixar_pagina(cfg)
    return {"titulo": p.titulo, "link": p.link, "itens": gb.itens(p.conteudo)}


def _campos_do_body(body):
    return {k: body.get(k) or None for k in
            ("nome", "link", "selo", "desc", "titulo_anuncio", "preco", "imagem")} | \
           {k: (body.get(k) or None) for k in ("beneficios", "ideal")}


def api_adicionar(body):
    cfg = gb.carregar_config()
    p = gb.baixar_pagina(cfg)
    d = _campos_do_body(body)
    if not d.get("nome") or not d.get("link"):
        raise gb.Erro("Nome e link são obrigatórios.")
    novo, pos, total = gb.adicionar_item(p.conteudo, d, body.get("posicao"), body.get("linha_tabela") or None)
    novo, titulo = gb.normalizar(novo, p.titulo)
    prob = gb.verificar(novo)
    if prob:
        raise gb.Erro("Não ficou consistente, nada foi publicado: " + "; ".join(prob))
    gb.publicar(cfg, p, novo, titulo)
    return {"ok": True, "posicao": pos, "total": total}


def api_editar(n, body):
    cfg = gb.carregar_config()
    p = gb.baixar_pagina(cfg)
    d = _campos_do_body(body)
    if not any(d.values()):
        raise gb.Erro("Nada para alterar.")
    novo, avisos = gb.editar_item(p.conteudo, n, d)
    prob = gb.verificar(novo)
    if prob:
        raise gb.Erro("Não ficou consistente, nada foi publicado: " + "; ".join(prob))
    gb.publicar(cfg, p, novo, p.titulo)
    return {"ok": True, "avisos": avisos}


def api_remover(n):
    cfg = gb.carregar_config()
    p = gb.baixar_pagina(cfg)
    nome_removido = gb.ler_item(p.conteudo[gb._sec(p.conteudo, n)["ini"]:gb._sec(p.conteudo, n)["fim"]])["nome"]
    novo, total = gb.remover_item(p.conteudo, n)
    novo, titulo = gb.normalizar(novo, p.titulo)
    prob = gb.verificar(novo)
    if prob:
        raise gb.Erro("Não ficou consistente, nada foi publicado: " + "; ".join(prob))
    gb.publicar(cfg, p, novo, titulo)
    return {"ok": True, "removido": nome_removido, "total": total}


def api_salvar_credenciais(body):
    usuario, senha = (body.get("usuario") or "").strip(), (body.get("senha_aplicativo") or "").strip()
    if not usuario or not senha:
        raise gb.Erro("Preencha usuário e senha de aplicativo.")
    # Engano comum: colocar o nome dado à senha ("Painel Blog") no lugar do usuário
    if " " in usuario:
        raise gb.Erro(f'"{usuario}" não é um usuário do WordPress (tem espaço). Use o login ou o e-mail de entrar '
                      "no WordPress, ex.: compre.no.link26@gmail.com. \"Painel Blog\" é só o nome da senha.")
    # A senha de aplicativo gerada pelo WordPress tem sempre 24 letras/números (mostrada em 6 grupos de 4)
    if not re.fullmatch(r"[A-Za-z0-9]{24}", senha.replace(" ", "")):
        raise gb.Erro(f"Isso não é uma senha de aplicativo (tem {len(senha.replace(' ', ''))} caracteres). "
                      "A senha de aplicativo tem 24 letras e números, em grupos de 4 (ex.: abcd efgh ijkl mnop qrst uvwx). "
                      "Não use a senha normal de entrar no WordPress: crie uma em Usuários > Perfil > Senhas da aplicação.")
    dados = {"site": (body.get("site") or "https://comprenolink.net").strip().rstrip("/"),
             "pagina_id": int(body.get("pagina_id") or 5), "usuario": usuario, "senha_aplicativo": senha}
    with open(gb.ARQ_CRED, "w", encoding="utf-8") as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)
    return {"ok": True}


# ============================================================== servidor HTTP
ROTAS_GET = {"/api/status": lambda qs: _cfg_resumo(), "/api/testar": lambda qs: api_testar(),
             "/api/itens": lambda qs: api_listar(),
             "/api/buscar": lambda qs: buscar_mercado_livre((qs.get("link") or [""])[0])}


class Handler(BaseHTTPRequestHandler):
    def log_message(self, fmt, *args):
        pass

    def _enviar(self, status, dados, tipo="application/json"):
        corpo = dados if isinstance(dados, bytes) else (json.dumps(dados, ensure_ascii=False) if tipo == "application/json" else dados).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", tipo + ("; charset=utf-8" if tipo.startswith("text") or tipo == "application/json" else ""))
        self.send_header("Content-Length", str(len(corpo)))
        self.end_headers()
        self.wfile.write(corpo)

    def _erro(self, e):
        status = 400 if isinstance(e, gb.Erro) else 500
        self._enviar(status, {"erro": str(e)})

    def _corpo_json(self):
        n = int(self.headers.get("Content-Length") or 0)
        return json.loads(self.rfile.read(n).decode("utf-8")) if n else {}

    def do_GET(self):
        caminho = urlparse(self.path)
        if caminho.path == "/":
            return self._enviar(200, PAGINA_HTML, "text/html")
        fn = ROTAS_GET.get(caminho.path)
        if not fn:
            return self._enviar(404, {"erro": "não encontrado"})
        try:
            self._enviar(200, fn(parse_qs(caminho.query)))
        except Exception as e:
            self._erro(e)

    def do_POST(self):
        caminho = urlparse(self.path).path
        try:
            body = self._corpo_json()
            if caminho == "/api/itens":
                return self._enviar(200, api_adicionar(body))
            if caminho == "/api/credenciais":
                return self._enviar(200, api_salvar_credenciais(body))
            self._enviar(404, {"erro": "não encontrado"})
        except Exception as e:
            self._erro(e)

    def do_PUT(self):
        m = re.match(r'^/api/itens/(\d+)$', urlparse(self.path).path)
        if not m:
            return self._enviar(404, {"erro": "não encontrado"})
        try:
            self._enviar(200, api_editar(int(m.group(1)), self._corpo_json()))
        except Exception as e:
            self._erro(e)

    def do_DELETE(self):
        m = re.match(r'^/api/itens/(\d+)$', urlparse(self.path).path)
        if not m:
            return self._enviar(404, {"erro": "não encontrado"})
        try:
            self._enviar(200, api_remover(int(m.group(1))))
        except Exception as e:
            self._erro(e)


# ============================================================== página (HTML + CSS + JS)
PAGINA_HTML = r"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Painel do Blog - comprenolink.net</title>
<style>
:root{--bg:#fff;--text:#1a1a1a;--dim:#555;--blue:#0B5FA5;--blue-bg:#E8F0FA;--gold:#B8860B;--green:#1E8E5A;
--green-bg:#E6F4EA;--red:#C0392B;--red-bg:#FDECEA;--border:#e0e0e0;--radius:10px}
*{box-sizing:border-box}
body{font-family:'Segoe UI',Tahoma,Geneva,Verdana,sans-serif;background:var(--bg);color:var(--text);margin:0;line-height:1.6}
header{background:linear-gradient(135deg,#1a1a1a,#0d0d0d);color:#fff;padding:1.6rem 1.5rem;text-align:center}
header h1{margin:0;font-size:1.5rem}
header p{margin:.3rem 0 0;color:#bbb;font-size:.9rem}
.container{max-width:900px;margin:0 auto;padding:1.5rem}
.card{background:#fff;border:1px solid var(--border);border-radius:var(--radius);padding:1.3rem;margin-bottom:1.2rem;
box-shadow:0 2px 8px rgba(0,0,0,.04)}
.btn{display:inline-block;border:none;border-radius:8px;padding:.7rem 1.3rem;font-size:.95rem;font-weight:600;
cursor:pointer;text-decoration:none}
.btn-blue{background:var(--blue);color:#fff}
.btn-blue:hover{background:#094a82}
.btn-green{background:var(--green);color:#fff}
.btn-outline{background:#fff;border:1px solid var(--border);color:var(--text)}
.btn-red{background:var(--red-bg);color:var(--red);border:1px solid #f3c6c1}
.btn-red-forte{background:var(--red);color:#fff}
.modal-fundo{position:fixed;inset:0;background:rgba(0,0,0,.55);display:flex;align-items:center;justify-content:center;
  padding:16px;z-index:1000}
.modal{background:#fff;border-radius:var(--radius);max-width:30rem;width:100%;padding:1.5rem;box-shadow:0 12px 40px rgba(0,0,0,.3)}
.modal h2{margin:0 0 .6rem;font-size:1.3rem}
.modal p{margin:.4rem 0;color:var(--dim)}
.modal .alvo{display:flex;gap:.8rem;align-items:center;background:#f7f7f7;border-radius:8px;padding:.7rem;margin:.8rem 0}
.modal .alvo img{width:56px;height:56px;object-fit:contain}
.modal .linha-botoes{justify-content:flex-end}
.btn:disabled{opacity:.55;cursor:default}
.linha-botoes{display:flex;gap:.6rem;flex-wrap:wrap;margin-top:.6rem}
label{display:block;font-weight:600;font-size:.85rem;margin:.8rem 0 .3rem}
label .op{font-weight:400;color:var(--dim)}
input[type=text],textarea{width:100%;padding:.6rem .7rem;border:1px solid var(--border);border-radius:8px;
font-size:.95rem;font-family:inherit}
textarea{resize:vertical;min-height:2.4rem}
.aviso{background:var(--blue-bg);border:1px solid #cfe0f3;border-radius:8px;padding:.8rem 1rem;font-size:.9rem;
color:var(--dim);margin-bottom:1rem}
.erro{background:var(--red-bg);border:1px solid #f3c6c1;color:var(--red);border-radius:8px;padding:.8rem 1rem;
font-size:.9rem;margin:.8rem 0}
.sucesso{background:var(--green-bg);border:1px solid #bfe3cd;color:#1b6b45;border-radius:8px;padding:.8rem 1rem;
font-size:.9rem;margin:.8rem 0}
.spinner{display:inline-block;width:14px;height:14px;border:2px solid #cfe0f3;border-top-color:var(--blue);
border-radius:50%;animation:girar .7s linear infinite;vertical-align:middle;margin-right:.4rem}
@keyframes girar{to{transform:rotate(360deg)}}
.produto{border:1px solid var(--border);border-radius:var(--radius);padding:1rem;margin-bottom:.9rem;
display:flex;gap:1rem;align-items:flex-start}
.produto img{width:64px;height:64px;object-fit:contain;background:#f7f7f7;border-radius:6px;flex-shrink:0}
.produto .info{flex:1;min-width:0}
.produto .nome{font-weight:700;margin:0 0 .2rem}
.produto .meta{font-size:.85rem;color:var(--dim)}
.selo{display:inline-block;background:#fff6e0;color:var(--gold);border-radius:20px;padding:.1rem .6rem;
font-size:.75rem;font-weight:600;margin-left:.4rem}
.prev-card{border:2px solid var(--blue);border-radius:var(--radius);padding:1rem;margin-top:1rem;background:#fafcff}
.prev-card img{max-width:140px;display:block;margin-bottom:.6rem;border-radius:6px}
.oculto{display:none}
.lista-beneficios{margin:.3rem 0;padding-left:1.2rem}
.lista-beneficios li{font-size:.9rem;color:var(--dim)}
.topo-secao{display:flex;justify-content:space-between;align-items:center;margin-bottom:.8rem}
.topo-secao h2{font-size:1.1rem;margin:0}
.chip-remove{color:var(--red);cursor:pointer;font-size:.8rem;margin-left:.4rem}
.rodape-form{display:flex;gap:.6rem;margin-top:1.2rem}
small.ajuda{color:var(--dim);display:block;margin-top:.2rem}
</style>
</head>
<body>
<header>
  <h1>🛠️ Painel do Blog</h1>
  <p>comprenolink.net — gerenciar os produtos do guia sem mexer em código</p>
</header>
<div class="container" id="app">Carregando…</div>

<script>
const API = location.origin;
const app = document.getElementById('app');
let ESTADO = {configurado:false, itens:[], editando:null};

async function chamar(metodo, caminho, corpo){
  const r = await fetch(API+caminho, {method:metodo, headers: corpo?{'Content-Type':'application/json'}:{},
    body: corpo?JSON.stringify(corpo):undefined});
  const d = await r.json().catch(()=>({}));
  if(!r.ok) throw new Error(d.erro || ('Erro ' + r.status));
  return d;
}

function esc(s){ return (s||'').replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c])); }

async function iniciar(){
  try{
    const st = await chamar('GET', '/api/status');
    ESTADO.configurado = st.configurado;
    if(!st.configurado) return telaConfig(st);
    await carregarItens();
  }catch(e){
    app.innerHTML = `<div class="card erro">Não consegui iniciar: ${esc(e.message)}</div>`;
  }
}

function telaConfig(st, aviso){
  app.innerHTML = `
  <div class="card">
    <h2>${aviso ? 'Trocar senha de aplicativo' : 'Primeira configuração'}</h2>
    ${aviso && aviso.trim() ? `<div class="erro">${esc(aviso)}</div>` : ''}
    <div class="aviso">Crie uma <b>senha de aplicativo</b> (não é a senha normal do WordPress): entre em
      <a href="${esc(st.site)}/wp-admin" target="_blank">${esc(st.site)}/wp-admin</a> → Usuários → Perfil →
      role até "Senhas de aplicativo" → dê um nome (ex: Painel Blog) → copie a senha gerada e cole abaixo.</div>
    <label>Usuário do WordPress (login ou e-mail)</label>
    <input type="text" id="cfg-usuario" value="${esc(st.usuario||'compre.no.link26@gmail.com')}">
    <label>Senha de aplicativo</label>
    <input type="text" id="cfg-senha" placeholder="abcd efgh ijkl mnop qrst uvwx">
    <label>Id da página do guia <span class="op">(normalmente 5, não mude se não souber)</span></label>
    <input type="text" id="cfg-pagina" value="${st.pagina_id||5}">
    <div id="cfg-msg"></div>
    <div class="linha-botoes"><button class="btn btn-blue" onclick="salvarConfig()">Salvar e continuar</button></div>
  </div>`;
}

async function salvarConfig(){
  const msg = document.getElementById('cfg-msg');
  msg.innerHTML = '';
  try{
    await chamar('POST', '/api/credenciais', {usuario: document.getElementById('cfg-usuario').value,
      senha_aplicativo: document.getElementById('cfg-senha').value, pagina_id: document.getElementById('cfg-pagina').value});
    msg.innerHTML = '<div class="sucesso">Salvo! Testando a conexão…</div>';
    const t = await chamar('GET', '/api/testar');
    const quem = t.nome_usuario ? `Conectado como <b>${esc(t.nome_usuario)}</b> — ` : 'Conectado — ';
    msg.innerHTML = `<div class="sucesso">${quem}${t.total_itens} itens na página. Pode editar: SIM.</div>`;
    setTimeout(carregarItens, 900);
  }catch(e){ msg.innerHTML = `<div class="erro">${esc(e.message)}</div>`; }
}

async function carregarItens(){
  app.innerHTML = '<div class="card"><span class="spinner"></span>Carregando os produtos do blog…</div>';
  try{
    const d = await chamar('GET', '/api/itens');
    ESTADO.itens = d.itens;
    desenhar(d);
  }catch(e){
    // Login recusado: a senha salva está errada (ou foi revogada) — abre direto a tela para trocar
    if(/401/.test(e.message)) return abrirConfig('O WordPress recusou a senha salva. Crie uma senha de aplicativo nova e cole abaixo.');
    app.innerHTML = `<div class="card erro">Não consegui carregar: ${esc(e.message)}<br><br>
      <button class="btn btn-outline" onclick="carregarItens()">Tentar de novo</button>
      <button class="btn btn-outline" onclick="abrirConfig()">Trocar senha de aplicativo</button></div>`;
  }
}

async function abrirConfig(aviso){
  const st = await chamar('GET', '/api/status').catch(() => ({site: 'https://comprenolink.net'}));
  telaConfig(st, aviso);
}

function desenhar(d){
  app.innerHTML = `
  <div class="card">
    <div class="topo-secao"><h2>${esc(d.titulo)}</h2>
      <a href="${esc(d.link)}" target="_blank" class="btn btn-outline">Ver no blog ↗</a></div>
    <div class="linha-botoes"><button class="btn btn-green" onclick="telaNovo()">+ Adicionar novo produto</button>
      <button class="btn btn-outline" onclick="abrirConfig(' ')">Trocar senha de aplicativo</button></div>
  </div>
  <div class="card"><div id="lista-itens"></div></div>
  <div id="form-area"></div>`;
  const lista = document.getElementById('lista-itens');
  lista.innerHTML = ESTADO.itens.map(p => `
    <div class="produto">
      ${p.imagem ? `<img src="${esc(p.imagem)}">` : '<div class="produto img" style="width:64px;height:64px;background:#f7f7f7;border-radius:6px"></div>'}
      <div class="info">
        <p class="nome">${p.n}. ${esc(p.nome)} ${p.selo?`<span class="selo">⭐ ${esc(p.selo)}</span>`:''}</p>
        <p class="meta">${esc(p.link)}</p>
      </div>
      <div class="linha-botoes" style="margin-top:0">
        <button class="btn btn-outline" onclick="telaEditar(${p.n})">Editar</button>
        <button class="btn btn-red" onclick="removerItem(${p.n}, '${esc(p.nome).replace(/'/g,"\\'")}')">Remover</button>
      </div>
    </div>`).join('') || '<p>Nenhum produto encontrado.</p>';
}

// Caixa de confirmação do próprio painel (a janelinha confirm() do navegador passa despercebida e pode ser
// bloqueada pelo navegador, respondendo "Cancelar" sozinha). Devolve true só se clicar no botão de confirmar.
function perguntar({titulo, texto, item, sim, perigo}){
  return new Promise(resolve => {
    const fundo = document.createElement('div');
    fundo.className = 'modal-fundo';
    fundo.innerHTML = `<div class="modal" role="dialog" aria-modal="true" aria-labelledby="modal-titulo">
      <h2 id="modal-titulo">${esc(titulo)}</h2>
      ${item ? `<div class="alvo">${item.imagem ? `<img src="${esc(item.imagem)}" alt="">` : ''}<b>${esc(item.texto)}</b></div>` : ''}
      ${(texto||[]).map(t => `<p>${esc(t)}</p>`).join('')}
      <div class="linha-botoes">
        <button class="btn btn-outline" data-r="nao">Cancelar</button>
        <button class="btn ${perigo ? 'btn-red-forte' : 'btn-green'}" data-r="sim">${esc(sim)}</button>
      </div></div>`;
    const fechar = r => { document.removeEventListener('keydown', tecla); fundo.remove(); resolve(r); };
    const tecla = e => { if(e.key === 'Escape') fechar(false); };
    fundo.addEventListener('click', e => {
      if(e.target === fundo) return fechar(false);
      const b = e.target.closest('button[data-r]'); if(b) fechar(b.dataset.r === 'sim');
    });
    document.addEventListener('keydown', tecla);
    document.body.appendChild(fundo);
    fundo.querySelector('[data-r="nao"]').focus();  // Enter sem querer = Cancelar
  });
}

async function removerItem(n, nome){
  const p = ESTADO.itens.find(x => x.n === n) || {};
  const ok = await perguntar({titulo: 'Tem certeza que você quer remover?', perigo: true, sim: 'Sim, remover do blog',
    item: {texto: `${n}. ${p.nome || nome}`, imagem: p.imagem},
    texto: ['O produto sai do blog na hora. Os itens seguintes são renumerados sozinhos.',
            'Um backup da página é salvo antes (pasta 2_DADOS > Blog_WordPress > backups).']});
  if(!ok) return;
  try{
    app.insertAdjacentHTML('afterbegin', '<div class="card"><span class="spinner"></span>Removendo…</div>');
    await chamar('DELETE', '/api/itens/'+n);
    await carregarItens();
    app.insertAdjacentHTML('afterbegin', `<div class="sucesso">"${esc(p.nome || nome)}" foi removido do blog.</div>`);
  }catch(e){
    await carregarItens();
    app.insertAdjacentHTML('afterbegin', `<div class="erro">Não consegui remover: ${esc(e.message)}</div>`);
  }
}

function campoForm(rotulo, id, valor, ajuda, area){
  const tag = area ? 'textarea' : 'input type="text"';
  const fechaTag = area ? 'textarea' : 'input';
  return `<label>${rotulo}</label><${tag} id="${id}" ${area?'':`value="${esc(valor||'')}"`}>${area?esc(valor||''):''}</${fechaTag}>
    ${ajuda?`<small class="ajuda">${ajuda}</small>`:''}`;
}

function telaNovo(){
  ESTADO.editando = null;
  document.getElementById('form-area').innerHTML = `
  <div class="card">
    <h2>Adicionar novo produto</h2>
    <div class="aviso">Cole o link do produto (o de afiliado que você já tem, ou o link comum do anúncio) e clique em
      Buscar — nome, foto, preço e características vêm sozinhos do Mercado Livre. Depois é só revisar e publicar.</div>
    <label>Link do Mercado Livre</label>
    <input type="text" id="f-buscar-link" placeholder="https://meli.la/XXXX ou o link do anúncio">
    <div class="linha-botoes">
      <button class="btn btn-blue" onclick="buscarML()">🔍 Buscar no Mercado Livre</button>
      <button class="btn btn-outline" onclick="mostrarFormCompleto()">Preencher manualmente</button>
    </div>
    <div id="busca-msg"></div>
    <div id="form-completo" class="oculto"></div>
  </div>`;
  mostrarForm();
}

async function buscarML(){
  const link = document.getElementById('f-buscar-link').value.trim();
  const msg = document.getElementById('busca-msg');
  if(!link){ msg.innerHTML = '<div class="erro">Cole um link primeiro.</div>'; return; }
  msg.innerHTML = '<div class="aviso"><span class="spinner"></span>Buscando os dados do produto…</div>';
  try{
    const d = await chamar('GET', '/api/buscar?link=' + encodeURIComponent(link));
    msg.innerHTML = '<div class="sucesso">Encontrado! Revise os campos abaixo antes de publicar.</div>';
    mostrarFormCompleto({nome: d.nome, link: d.link_final, imagem: d.imagem, preco: d.preco,
      desc: d.descricao, titulo_anuncio: d.nome, beneficios: d.beneficios});
  }catch(e){
    msg.innerHTML = `<div class="erro">${esc(e.message)}</div>`;
    mostrarFormCompleto({link});
  }
}

function mostrarFormCompleto(dados){
  dados = dados || {};
  const div = document.getElementById('form-completo');
  div.classList.remove('oculto');
  const beneficios = (dados.beneficios||[]).join('\n');
  div.innerHTML = `
    ${dados.imagem?`<img src="${esc(dados.imagem)}" style="max-width:120px;border-radius:8px;margin:.6rem 0;display:block">`:''}
    ${campoForm('Nome curto (aparece como título do item — edite para ficar enxuto)','f-nome',dados.nome,'Ex.: "Fone JBL Bluetooth On-Ear" em vez do nome completo do anúncio')}
    ${campoForm('Link do produto (de afiliado)','f-link',dados.link)}
    ${campoForm('Selo de destaque','f-selo',dados.selo,'Ex.: Mais Vendido, Oferta do Mês, Melhor Custo-Benefício')}
    ${campoForm('Descrição curta','f-desc',dados.desc,'','area')}
    ${campoForm('Título completo do anúncio (aparece no cartão com o botão)','f-titulo','', '', 'area')}
    <div class="aviso">O cartão não mostra preço (o preço muda no site oficial).</div>
    ${campoForm('URL da imagem','f-imagem',dados.imagem)}
    ${campoForm('Benefícios (um por linha)','f-beneficios',beneficios,'Cada linha vira um item da lista "Benefícios"','area')}
    ${campoForm('Ideal para (um por linha)','f-ideal','','Ex.: Música / Viagem / Uso diário','area')}
    <label>Posição <span class="op">(vazio = no final da lista)</span></label>
    <input type="text" id="f-posicao" placeholder="ex.: 3">
    <label>Categoria para a tabela "Escolha rápida" <span class="op">(vazio = não incluir nessa tabela)</span></label>
    <input type="text" id="f-linha-tabela" placeholder="ex.: Fone barato com cancelamento de ruído">
    <div id="pub-msg"></div>
    <div class="rodape-form">
      <button class="btn btn-green" onclick="publicarNovo()">Publicar no blog</button>
      <button class="btn btn-outline" onclick="document.getElementById('form-area').innerHTML=''">Cancelar</button>
    </div>`;
  document.getElementById('f-titulo').value = dados.titulo_anuncio || '';
}

function linhas(id){
  return document.getElementById(id).value.split('\n').map(s=>s.trim()).filter(Boolean);
}

async function publicarNovo(){
  const corpo = {nome: document.getElementById('f-nome').value, link: document.getElementById('f-link').value,
    selo: document.getElementById('f-selo').value, desc: document.getElementById('f-desc').value,
    titulo_anuncio: document.getElementById('f-titulo').value, preco: '',
    imagem: document.getElementById('f-imagem').value, beneficios: linhas('f-beneficios'), ideal: linhas('f-ideal'),
    posicao: document.getElementById('f-posicao').value, linha_tabela: document.getElementById('f-linha-tabela').value};
  if(!corpo.nome || !corpo.link){ document.getElementById('pub-msg').innerHTML = '<div class="erro">Nome e link são obrigatórios.</div>'; return; }
  if(!await perguntar({titulo: 'Publicar este produto no blog?', sim: 'Sim, publicar', item: {texto: corpo.nome, imagem: corpo.imagem},
    texto: ['Ele aparece no blog na hora. Um backup da página é salvo antes.']})) return;
  const msg = document.getElementById('pub-msg');
  msg.innerHTML = '<div class="aviso"><span class="spinner"></span>Publicando…</div>';
  try{
    await chamar('POST', '/api/itens', corpo);
    msg.innerHTML = '<div class="sucesso">Publicado! Atualizando a lista…</div>';
    setTimeout(carregarItens, 900);
  }catch(e){ msg.innerHTML = `<div class="erro">${esc(e.message)}</div>`; }
}

function telaEditar(n){
  const p = ESTADO.itens.find(x=>x.n===n);
  ESTADO.editando = n;
  document.getElementById('form-area').innerHTML = `
  <div class="card">
    <h2>Editar item ${n}</h2>
    <div class="aviso">Mude só o que quiser: o que ficar igual não é alterado.</div>
    ${p.imagem?`<img src="${esc(p.imagem)}" style="max-width:120px;border-radius:8px;margin-bottom:.6rem;display:block">`:''}
    ${campoForm('Nome','e-nome',p.nome)}
    ${campoForm('Link do produto','e-link',p.link)}
    ${campoForm('Selo de destaque','e-selo',p.selo)}
    ${campoForm('Descrição curta','e-desc',p.desc,'','area')}
    ${p.preco_auto ? `<div class="aviso">Foto, preço e título do anúncio deste produto vêm <b>automaticamente do Mercado Livre</b>
      (cartão do plugin Hostinger). Para trocar de produto, troque o <b>Link do produto</b> acima.</div>` : `
    ${campoForm('Título completo do anúncio (cartão)','e-titulo',p.titulo_anuncio,'','area')}
    ${campoForm('URL da imagem','e-imagem',p.imagem)}`}
    <div class="aviso">O cartão não mostra preço (o preço muda no site oficial).</div>
    ${campoForm('Benefícios (um por linha — deixe em branco para manter os atuais)','e-beneficios','','','area')}
    ${campoForm('Ideal para (um por linha — deixe em branco para manter)','e-ideal','','','area')}
    <div id="edit-msg"></div>
    <div class="rodape-form">
      <button class="btn btn-green" onclick="publicarEdicao(${n})">Salvar alterações</button>
      <button class="btn btn-outline" onclick="document.getElementById('form-area').innerHTML=''">Cancelar</button>
    </div>
  </div>`;
  mostrarForm(n);
}

// Coloca o formulário logo abaixo do produto clicado (ou no topo, para "Adicionar") e mostra na tela;
// no fim da lista de 21 itens parecia que o botão não fazia nada
function mostrarForm(n){
  const f = document.getElementById('form-area');
  const ancora = n ? document.querySelectorAll('#lista-itens .produto')[n - 1] : app.querySelector('.card');
  if(ancora) ancora.after(f);
  f.scrollIntoView({block:'start'});
  const primeiro = f.querySelector('input, textarea');
  if(primeiro) setTimeout(() => primeiro.focus({preventScroll:true}), 400);
}

async function publicarEdicao(n){
  const p = ESTADO.itens.find(x=>x.n===n);
  const val = id => { const el = document.getElementById(id); return el ? el.value.trim() : ''; };
  // Só manda o que mudou (campo igual ao atual vai vazio = "manter")
  const mudou = (id, atual) => { const v = val(id); return v && v !== (atual||'').trim() ? v : ''; };
  const corpo = {nome: mudou('e-nome', p.nome), link: mudou('e-link', p.link), selo: mudou('e-selo', p.selo),
    desc: mudou('e-desc', p.desc), titulo_anuncio: mudou('e-titulo', p.titulo_anuncio), preco: mudou('e-preco', p.preco),
    imagem: mudou('e-imagem', p.imagem), beneficios: linhas('e-beneficios'), ideal: linhas('e-ideal')};
  const msg = document.getElementById('edit-msg');
  if(!Object.values(corpo).some(v => Array.isArray(v) ? v.length : v)){
    msg.innerHTML = '<div class="aviso">Nada foi alterado: mude algum campo antes de salvar.</div>'; return;
  }
  if(!await perguntar({titulo: 'Salvar estas alterações no blog?', sim: 'Sim, salvar e publicar',
    item: {texto: `${n}. ${p.nome}`, imagem: p.imagem}, texto: ['A mudança aparece no blog na hora. Um backup da página é salvo antes.']})) return;
  msg.innerHTML = '<div class="aviso"><span class="spinner"></span>Publicando…</div>';
  try{
    const r = await chamar('PUT', '/api/itens/'+n, corpo);
    const av = (r.avisos||[]).length ? `<div class="aviso">Atenção: ${r.avisos.map(esc).join('<br>')}</div>` : '';
    msg.innerHTML = '<div class="sucesso">Salvo e publicado no blog!' + (av ? '' : ' Atualizando a lista…') + '</div>' + av;
    if(!av) setTimeout(carregarItens, 1200);
    else msg.insertAdjacentHTML('beforeend', '<button class="btn btn-outline" onclick="carregarItens()">Voltar para a lista</button>');
  }catch(e){ msg.innerHTML = `<div class="erro">${esc(e.message)}</div>`; }
}

iniciar();
</script>
</body>
</html>"""


# ============================================================== main
class ServidorExclusivo(ThreadingHTTPServer):
    # No Windows, SO_REUSEADDR deixa dois painéis escutarem a mesma porta (e um antigo responder no lugar
    # do novo). Com SO_EXCLUSIVEADDRUSE a segunda abertura falha e reaproveitamos o painel já aberto.
    allow_reuse_address = False

    def server_bind(self):
        if hasattr(socket, "SO_EXCLUSIVEADDRUSE"):
            self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_EXCLUSIVEADDRUSE, 1)
        super().server_bind()


def main():
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    try:
        servidor = ServidorExclusivo(("127.0.0.1", PORTA), Handler)
    except OSError:
        print(f"O painel já está aberto em outra janela. Abrindo http://127.0.0.1:{PORTA}/ no navegador...")
        print("Se a página não carregar, feche as outras janelas pretas do painel e abra o atalho de novo.")
        webbrowser.open(f"http://127.0.0.1:{PORTA}/")
        time.sleep(4)
        return
    print(f"Painel do blog rodando em http://127.0.0.1:{PORTA}/")
    print("Deixe esta janela aberta enquanto estiver usando o painel.")
    print("Para encerrar: feche esta janela ou pressione Ctrl+C.\n")
    threading.Thread(target=lambda: (time.sleep(0.6), webbrowser.open(f"http://127.0.0.1:{PORTA}/")), daemon=True).start()
    try:
        servidor.serve_forever()
    except KeyboardInterrupt:
        print("\nEncerrado.")


if __name__ == "__main__":
    main()
