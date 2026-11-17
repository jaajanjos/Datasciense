# Rastreamento de Acessos por Anúncio (100% grátis)

Mostra **quem está acessando / acessou** o blog `comprenolink.net/melhores-produtos-mercado-livre-2026/`, **de qual anúncio veio**
(vídeo do TikTok, bio, Instagram, WhatsApp, anúncio pago...), em qual aparelho, e **quais produtos
(links meli.la) foram clicados**. Os dados ficam no seu próprio WordPress — sem Google Analytics,
sem mensalidade.

> Privacidade (LGPD): ninguém é identificado por nome, e-mail ou IP. Cada visitante recebe um
> código aleatório no navegador, e o IP é guardado só como um hash que muda todo dia.
> Recomendado: adicionar na Política de Privacidade do blog uma frase como
> "usamos estatísticas anônimas de acesso para saber quais divulgações funcionam".

## Arquivos

| Arquivo | Onde | Para quê |
|---|---|---|
| `1_snippet_wordpress_rastreador.php` | `rastreamento_anuncios\` | Vai no WordPress. Registra visitas e cliques. |
| `config_rastreio.json` | `Relatorios_Diarios_Anuncios\programas_fontes_python\` | Site, chave secreta e lista dos seus anúncios (usado pelos `.py` e `.exe`). |
| `2_gerar_links_anuncios.py` | `python\` | Gera um link etiquetado (UTM) para cada anúncio. |
| `3_relatorio_acessos_anuncios.py` | `Relatorios_Diarios_Anuncios\programas_fontes_python\` | Baixa os dados e gera `D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\_historico_relatorios\relatorio_acessos_anuncios_AAAA-MM-DD_HHhMM.html`. |

Todos os scripts `.py` do projeto ficam em `D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\programas_fontes_python\`.

### Versão .exe (não precisa de Python)

| Executável | Equivale a |
|---|---|
| `gerar_links_anuncios.exe` | `python 2_gerar_links_anuncios.py` |
| `relatorio_acessos_anuncios.exe` | `python 3_relatorio_acessos_anuncios.py` |

Basta dar **duplo clique**. O `config_rastreio.json` precisa ficar **na mesma pasta** do `.exe`.
Opções também funcionam pelo terminal, ex.: `relatorio_acessos_anuncios.exe --dias 7` ou `--demo`.
Para recompilar após mudar os `.py` (rodar dentro de `D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\programas_fontes_python`):
clique duplo em `11_compilar_exe_relatorio.bat` (gera o `1_relatorio_acessos_anuncios.exe` nesta mesma pasta e guarda o anterior).

## Passo 1 — Instalar no WordPress (uma vez só)

1. Painel WordPress > **Plugins > Adicionar novo** > pesquise **Code Snippets** > Instalar > Ativar.
2. **Snippets > Adicionar novo**, título "Rastreador de anúncios".
3. Cole todo o conteúdo de `1_snippet_wordpress_rastreador.php`.
4. Na linha `define('RASTREIO_CHAVE', '...')` troque por uma senha longa sua (ex.: 30 letras/números).
5. Marque **Executar snippet em todo o site** > **Salvar e ativar**.
6. Coloque a **mesma senha** no campo `"chave"` do `config_rastreio.json`.
7. Se usar o plugin **LiteSpeed Cache** (Hostinger): LiteSpeed Cache > Purgar tudo.

Para você não "sujar" os números, suas visitas logado como administrador **não** são contadas.
Para testar, abra o blog numa janela anônima.

## Passo 2 — Um link diferente para cada anúncio

```
python 2_gerar_links_anuncios.py
```

Gera `D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\links_anuncios_AAAA-MM-DD_HHhMM.html` (e `.csv`) com um botão "Copiar" para cada link. Use cada link **só** no seu lugar:
vídeo 01 → link do vídeo 01, bio do TikTok → link da bio, etc.
Para um anúncio novo, adicione uma linha em `anuncios` no `config_rastreio.json` ou rode:

```
python 2_gerar_links_anuncios.py --origem kwai --meio video --campanha ps5 --conteudo 04_ps5
```

Mesmo sem o link etiquetado o sistema ainda reconhece: aberto **dentro do app TikTok/Instagram/Facebook**,
parâmetros de anúncio pago (`ttclid`, `fbclid`, `gclid`) e visitas vindas do Google.

## Passo 3 — Gerar o relatório

```
python 3_relatorio_acessos_anuncios.py            # últimos 30 dias
python 3_relatorio_acessos_anuncios.py --dias 7
python 3_relatorio_acessos_anuncios.py --demo     # exemplo com dados fictícios
```

Cada execução cria um arquivo novo com a data/hora da geração no nome e no topo do relatório (os anteriores ficam como histórico).

O relatório mostra:
- 🟢 quantos estão **acessando agora** (últimos 30 min)
- visitas, visitantes únicos, % vindas de anúncio, cliques em afiliado e taxa de clique
- tabela **por anúncio** (visitas, visitantes, cliques, taxa de clique) — mostra qual vídeo vende mais
- produtos mais clicados e de qual anúncio vieram os cliques
- visitas por dia e por horário (melhor horário para postar)
- aparelho, sistema e app
- lista de visitantes anônimos: quando entrou, de onde veio, o que clicou

Uma cópia dos dados (JSON + CSV para Excel) fica em `dados_acessos\`.

## Passo 4 — Vendas aprovadas feitas através de https://comprenolink.net/melhores-produtos-mercado-livre-2026/

O relatório analisa **somente a página `https://comprenolink.net/melhores-produtos-mercado-livre-2026/`** (campo `pagina_blog` do config).
Acessos e cliques de outras páginas do site são ignorados, e o topo do relatório informa quantos foram.

Cada venda do arquivo do painel é classificada pelo **status**:
- ✅ **Aprovada** (aprovada, paga, liberada, concluída...) → entra nos totais e recebe o campo
  **"Efetuada pelo https://comprenolink.net/melhores-produtos-mercado-livre-2026/"** (também na coluna `efetuada_por` do CSV)
- ⏳ **Pendente** (pendente, em análise, a liberar...) → listada à parte, comissão "a confirmar"
- ❌ **Cancelada** (cancelada, devolvida, estornada...) → listada à parte, não conta

Se o arquivo não tiver coluna de status, as vendas são consideradas aprovadas e o relatório avisa.

O blog não enxerga o que acontece dentro do Mercado Livre. Por isso o relatório mostra dois tipos:

**🔥 Possíveis compras (estimativa automática).** Cada visitante ganha pontos: clicou no produto (+40),
clicou de novo no mesmo produto (+20), voltou outro momento e clicou (+20), saiu do blog direto para o
ML (+10), focou em um só produto (+10). **70 pontos ou mais = possível compra.**

**💰 Compras confirmadas.** No painel **Mercado Livre Afiliados**, exporte o relatório de vendas/ganhos
(CSV ou Excel) e salve em `D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\vendas_afiliados\`. Depois gere o relatório de novo.
Pode deixar vários arquivos na pasta; vendas repetidas são contadas uma vez só.

**Só entram as vendas que vieram do comprenolink:**
1. Se a planilha trouxer o **link `meli.la`**, só contam os links que estão na página do blog
   (o script lê a página `pagina_blog` para pegar a lista). Se você usa uma **etiqueta** própria para o
   blog no painel de afiliados, coloque em `"etiqueta_afiliado"` no `config_rastreio.json`.
2. Se a planilha **não** trouxer link nem etiqueta, só contam as vendas que batem com um **clique no
   blog no mesmo produto** até `janela_compra_horas` (padrão 24h) antes da venda.

Vendas de outros canais ficam fora dos totais, mas aparecem em "Ver as vendas descartadas" para
conferência. Vendas canceladas/devolvidas também não contam. O resultado completo (com o motivo de
cada venda entrar ou não) fica em `dados_acessos\compras_atribuidas_*.csv`.

Se o script não reconhecer as colunas da planilha, informe os nomes no config:
`"colunas_vendas": {"data": "Data da venda", "produto": "Título", "valor": "Preço", "comissao": "Ganhos"}`

## Dúvidas comuns

- **401/403 ao gerar relatório** → a chave do `config_rastreio.json` é diferente da do snippet.
- **404** → snippet não está ativo, ou o site bloqueia `/wp-json/` (o script tenta `?rest_route=` automaticamente).
- **Relatório vazio** → visite o blog numa janela anônima, espere 1 minuto e gere de novo.
- **Compra não apareceu** → confira se o arquivo do painel está em `vendas_afiliados\` e se a venda
  não caiu em "descartadas" (o motivo aparece ao lado).
