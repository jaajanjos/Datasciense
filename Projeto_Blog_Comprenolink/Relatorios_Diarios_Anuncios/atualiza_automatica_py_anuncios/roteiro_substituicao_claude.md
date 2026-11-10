# Roteiro do Claude — substituição automática dos anúncios fora do ar (comprenolink.net)

Responda sempre em português do Brasil. Você está sendo chamado pelo programa `3_substituir_com_claude.py`.
O dono autorizou (09/11/2026) a substituição **automática, sem aprovação prévia**: ele valida depois cada link e
produto e, se houver erro, corrige pelos programas. Mesmo assim, siga as regras abaixo com rigor.

## Regras que nunca mudam
- **Nunca** digite senha, nunca faça login, nunca burle captcha. Se o ML pedir login/captcha, pare e registre.
- **Não** edite o blog: quem troca no WordPress é o programa `4_aplicar_no_blog.py`, lendo o arquivo que você grava.
- Ritmo humano: uma página por vez, sem abrir dezenas de abas. Feche as abas que abrir.
- Não invente dados: preço, título, imagem e textos vêm da página do anúncio.

## Entrada
Leia `pendencias_substituicao.json` (nesta pasta). Cada item de `pendentes` tem: item, nome_no_blog, titulo_no_ml,
categoria, situacao_ml, link_antigo, catalogo_mlb, preco_antes, preco_min, preco_max, busca_mesmo_produto e
busca_mesmo_tipo. Os requisitos estão em `requisitos_substituto`. Processe no máximo `MAX` itens (o programa informa).

## Navegador
Use as ferramentas `mcp__claude-in-chrome__*`. Primeiro `list_connected_browsers` e escolha o navegador deste
computador (o "Browser 1"/onThisComputer, com o ML Afiliados logado). Abra uma aba nova (`tabs_create_mcp`).
Se nenhum navegador estiver conectado ou o ML Afiliados não estiver logado (sem a barra "Afiliados" no topo da página do
produto), **não** tente contornar: grave o arquivo de saída com `"situacao_geral": "navegador_indisponivel"` e o motivo.

## Para cada item pendente
1. **Escolha do substituto**, nesta ordem (vale sempre a MELHOR política de venda):
   1. Mesmo produto (mesmo catálogo, outro vendedor) em `busca_mesmo_produto`. Se não houver anúncio ativo bom:
      mesmo tipo de produto e mesma categoria do guia em `busca_mesmo_tipo`.
   2. Anúncio **ativo**, produto **novo**, com estoque.
   3. Vendedor **MercadoLíder** (Platinum › Gold › Líder) ou reputação verde; envio **Full**; **frete grátis**;
      **devolução grátis**; garantia informada.
   4. Nota **4,5 ou mais**, muitas avaliações e vendas.
   5. Preço entre `preco_min` e `preco_max` (se houver). Empate: o de menor preço.
2. **Armadilhas já vistas (obrigatório conferir):**
   - Na LISTA do ML o preço grande pode ser a **parcela**. Confirme o preço **à vista** na página do anúncio.
   - Produto de **catálogo** (`/p/MLB...`): o "Gerar link" devolve sempre o mesmo meli.la do catálogo, que pode cair no
     anúncio PAUSADO antigo. Depois de gerar, **abra o meli.la** e confirme que cai num anúncio **ativo** e que o código
     `ref=`/anúncio de destino **não é o mesmo** do `link_antigo`. Se for o mesmo, escolha **outro produto/catálogo**.
   - Variação de cor: se precisar, abra o anúncio com o parâmetro da cor antes de gerar o link.
3. **Gerar o link de afiliado:** na página do anúncio escolhido, barra "Afiliados" (topo) → **Compartilhar** →
   **Gerar link** (etiqueta r20250720181444) → leia o `https://meli.la/...` do campo por JavaScript.
4. **Conferir o link:** abra o meli.la numa aba, confirme produto, anúncio ativo e preço. Anote a URL final.
5. **Colher os dados do cartão** (da própria página do anúncio): título do anúncio, preço à vista (formato
   `R$ 1.234,56`), URL da **imagem principal** (https, do ML), nº do anúncio (MLB), vendedor e política de venda.
6. **Textos do guia** (curtos, no mesmo estilo dos outros itens, atrativos para a compra, **sem inventar**: só o que a
   página do anúncio mostra): `nome` (nome curto do produto, como no guia), `selo` (2 a 5 palavras, ex.: "Boa opção
   de entrada"), `desc` (1 frase), `beneficios` (3 itens), `ideal` (2 a 3 perfis). Sem promessas de saúde nem
   "o melhor" absoluto.

## Saída (obrigatória) — grave `substituicoes_aprovadas.json` nesta pasta, UTF-8, exatamente neste formato
```json
{
  "gerado_em": "AAAA-MM-DD HH:MM",
  "situacao_geral": "ok | parcial | navegador_indisponivel | nada_a_fazer",
  "substituicoes": [
    {
      "item": 32,
      "link_antigo": "https://meli.la/xxxx",
      "nome": "Inalador Mesh Ultrassônico",
      "selo": "Silencioso e portátil",
      "desc": "Frase curta com o que o anúncio mostra.",
      "beneficios": ["...", "...", "..."],
      "ideal": ["...", "..."],
      "link": "https://meli.la/yyyy",
      "titulo_anuncio": "Título exato do anúncio no ML",
      "preco": "R$ 199,90",
      "imagem": "https://http2.mlstatic.com/....webp",
      "anuncio_mlb": "MLB0000000000",
      "url_final": "https://www.mercadolivre.com.br/...",
      "vendedor": "nome do vendedor",
      "politica": "MercadoLíder Gold · Full · frete grátis · devolução grátis · garantia 12 meses",
      "conferido": "meli.la aberto: anúncio ativo, destino diferente do antigo, preço à vista conferido"
    }
  ],
  "nao_substituidos": [
    {"item": 66, "motivo": "nenhum anúncio ativo da categoria dentro da faixa de preço"}
  ]
}
```
Todo item pendente processado deve aparecer em `substituicoes` **ou** em `nao_substituidos`.
Termine com um resumo curto (quantos trocados, quantos não, e por quê).
