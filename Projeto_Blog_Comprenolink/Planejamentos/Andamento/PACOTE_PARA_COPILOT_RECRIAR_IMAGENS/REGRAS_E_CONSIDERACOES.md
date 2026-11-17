# Regras e considerações — recriação das artes do comprenolink.net

Este arquivo vale para tudo o que for feito **dentro desta pasta** (`PACOTE_PARA_COPILOT_RECRIAR_IMAGENS`). Ela é uma cópia separada do material original. Leia também `LEIA_ME_COPILOT.txt` e `INVENTARIO_IMAGENS_PARA_COPILOT.txt`.

## 1. Separação do original (obrigatório)

- Trabalhe **somente nesta pasta**. Nunca grave, apague ou renomeie nada na pasta original `07_PACOTE_DO_DIA` nem em outras pastas do projeto.
- Os arquivos em `IMAGENS_ANUNCIOS/`, `ORIGINAIS_PRODUTOS/`, `REFERENCIAS_VISUAIS/` e `TEXTOS_DOS_DIAS/` são **somente leitura** (referência). Não os sobrescreva.
- Salve as novas artes em uma pasta nova, por exemplo `NOVAS_ARTES/<data_do_dia>/`, mantendo o nome do arquivo de origem (`feed`, `story`, `status`, `reels_capa`, `campanha_HHhMM`) e indicando a versão (`feed_v1.png`).
- Nada deve ser publicado, agendado ou enviado ao Instagram, ao WhatsApp ou ao blog. Esta etapa é só de criação para aprovação do dono.

## 2. Política editorial fixa (proibições)

- **Não mostrar preço**: nem "R$", nem parcelas, nem desconto em valor ou percentual, nem faixa de preço.
- **Não usar "mais vendido"**.
- **Não usar "melhor ..."** (melhor preço, melhor do ano etc.).
- **Não usar "líder"**, exceto o status factual **MercadoLíder**, quando confirmado.
- **Não usar "oferta do mês"**.
- **Não usar "garantido"**.
- **Não criar características** que não estejam comprovadas nos arquivos do pacote ou no anúncio do Mercado Livre.
- **Não criar benefícios de saúde** (nem sugerir cura, tratamento ou efeito).
- **Não inventar selo** ou etiqueta. Só usar o que consta em `selo_na_arte`; sem selo, não desenhar a pílula.
- **Informações variáveis** (estoque, prazo, frete, parcelamento, garantia, avaliação) só aparecem se forem conferidas de novo no anúncio.
- Manter a identificação de afiliado: `comprenolink.net • link de afiliado`.
- Manter a frase `Confira o valor do dia no Mercado Livre` no lugar de qualquer preço.

## 3. Fidelidade ao produto e aos dados

- Usar **somente** o nome do produto, o modelo, a marca e as características que estão no inventário (`produto`, `dados_do_produto_usados`, `descricao_do_dia`).
- Usar a **foto real** do produto (`ORIGINAIS_PRODUTOS/itemN.png`). Não gerar outro produto, outra cor, outro modelo ou acessórios que não existam.
- Os itens 54, 69 e 209 não têm foto no cache: **NÃO LOCALIZADO**. Não inventar imagem; pedir a foto ao dono.
- O número `#item-N` do guia mudou com o tempo. Conferir sempre **pelo nome do produto**, nunca só pelo número.
- Onde o inventário diz `NÃO LOCALIZADO`, não preencher por suposição.
- O texto de cada arte foi reconstruído sem OCR (a partir do código e dos textos do dia): **conferir visualmente** a imagem original antes de redesenhar.

## 4. Formatos e dimensões

| Uso | Arquivo | Dimensão | Proporção |
|---|---|---|---|
| Feed do Instagram | `feed` | 1080×1350 | 4:5 |
| Story do Instagram | `story` | 1080×1920 | 9:16 |
| Status do WhatsApp | `status` | 1080×1920 | 9:16 |
| Capa do Reels | `reels_capa` | 1080×1920 | 9:16 |
| Campanha (sem produto) | `campanha_HHhMM` | 1080×1920 | 9:16 |

- Preservar essas dimensões e proporções.
- Respeitar as **zonas seguras**: nos Stories, a parte inferior fica livre para o adesivo de link (`VER NO BLOG`), e os textos principais não ficam colados nas bordas.
- Entregar em PNG (ou JPG de alta qualidade para as capas), sem compressão visível.

## 5. Identidade visual

- Partir da identidade **já existente**: logotipos em `REFERENCIAS_VISUAIS/`, `post_boas_vindas.png` e as cores e a estrutura descritas em `LEIA_ME_COPILOT.txt` e em `gerar_artes_catalogo.py`.
- Preservar o que já está bom: faixa de campanha no topo (Black Friday em amarelo, Natal em vermelho com selo verde), cartão de foto com cantos arredondados, nome do produto legível e chamada clara.
- Pode propor uma direção de arte superior (hierarquia, contraste, respiro, enquadramento da foto, tipografia), mas **sem criar uma identidade nova** nem trocar o logotipo ou as cores de marca sem aprovação do dono.
- Texto sempre legível no celular: contraste alto, corpo grande e poucas linhas.
- Nada de elementos que sugiram preço, selo oficial do Mercado Livre ou promoção que não exista.

## 6. Textos nas artes

- Português do Brasil, simples e direto, com apelo de compra, **sem inventar dados** (ver seção 2).
- Nome do produto igual ao do inventário (pode ser encurtado só se continuar identificando o produto).
- A chamada deve seguir o canal: Feed `Link na bio • Comente BLACK` (ou `NATAL`), Story `Toque no link abaixo`, Status `Link na mensagem`.

## 7. Como entregar para aprovação

1. Uma imagem individual para cada anúncio selecionado, na pasta nova (seção 1).
2. Um arquivo curto de resumo, por imagem, com: o que foi mantido, o que mudou e por quê.
3. Uma lista final marcando qualquer dado que precise de nova conferência (`NÃO LOCALIZADO` ou variável).
4. Aguardar a aprovação do dono antes de qualquer uso das novas artes.

## 8. Em caso de dúvida

Não adivinhar. Registrar a dúvida e deixar o item como `NÃO LOCALIZADO` ou `A CONFERIR`, para o dono ou o Claude confirmarem no projeto.
