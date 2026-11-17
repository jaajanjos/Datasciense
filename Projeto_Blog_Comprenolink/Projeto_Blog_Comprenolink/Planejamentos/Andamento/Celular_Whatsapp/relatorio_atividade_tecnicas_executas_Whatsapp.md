# Relatório técnico — Automação WhatsApp Business (afiliado Mercado Livre)

**Projeto**: comprenolink.net (blog de afiliado Mercado Livre)
**Escopo desta atividade**: configuração e automação do canal WhatsApp Business (número (11) 99495-9657). O Instagram é tocado em paralelo por outra pessoa/sessão e está fora do escopo deste relatório, exceto onde há interseção de arquivos.
**Pasta de origem dos scripts**: `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Divugação_WhastsApp_Instagram\_fonte\`
**Pasta "fonte de verdade" para o celular**: `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Celular_Whatsapp\`
**Espelho no OneDrive (para o app OneDrive do celular)**: `C:\Users\kkk\OneDrive\Download\Divulgacao_Blog\`
**Período coberto**: 26/10/2026 a 30/10/2026.

---

## 1. Objetivo do projeto

Divulgar produtos de afiliado do Mercado Livre pelo WhatsApp Business, com:
- Perfil comercial configurado no número do blog.
- Catálogo de produtos navegável dentro do próprio WhatsApp.
- Canal de WhatsApp para broadcast de ofertas.
- Respostas rápidas para atendimento.
- Rotina de divulgação (Status, Canal, grupos, lista de transmissão) com conteúdo pré-gerado.
- Tudo rastreável por UTM para medir retorno.

Dado real de escala: o blog tinha **165 anúncios em 27/10**, crescendo (**169 em 28/10**, com uma categoria nova surgida), e a meta declarada pelo dono é passar de **500 anúncios**. Isso motivou a decisão arquitetural central (seção 3).

---

## 2. Estado inicial (antes desta atividade)

Já existia um pipeline de geração de conteúdo em Python (fora do escopo desta atividade, pré-existente):
- `dados_divulgacao.py` — lê produtos reais do blog via `gerenciar_blog.py` (em `D:\Projeto_Blog_Comprenolink\Gestao_Anuncios_Blog\1_PROGRAMAS\Blog_WordPress\`) e a árvore de categorias (`categorias.json`, mesmo diretório), monta textos e links com UTM.
- `gerar_artes_catalogo.py` — gerava catálogo do WhatsApp **por produto** (17 itens, Top 10 Black Friday + Top 10 Natal, com sobreposição) e o pacote diário de artes/textos (`07_PACOTE_DO_DIA\`).
- `gerar_divulgacao.py` — orquestrador; função `gera_guia(dados, arquivo, blocos, titulo, subtitulo, rotulo)` monta PDFs com ReportLab a partir de blocos de conteúdo (`("h1", texto)`, `("h2", texto)`, `("p", texto)`, `("passos", [...])`, `("lista", [...])`, `("tabela", [[...]])`, `("alerta", texto)`, `("dica", texto)`, `("quebra",)`).
- `conteudo_celular.py` — conteúdo (blocos) do guia `08_PASSO_A_PASSO_WHATSAPP_NO_CELULAR.pdf`.
- `conteudo_guia.py` — conteúdo do guia geral `01_GUIA_COMPLETO_DIVULGACAO.pdf`.
- `sincronizar_copias.py` — copiava arquivos para `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Celular_Whatsapp` e para o OneDrive.
- Ambiente Python: faltava a dependência `reportlab` (foi reinstalada nesta atividade: `pip install reportlab`, versão 5.1.0).

Usuário já havia configurado manualmente, antes/durante esta atividade: instalação do WhatsApp Business no número do blog, catálogo por produto (17 itens, CNL-xxx), Canal inicial (depois duplicado e corrigido — ver seção 5.3).

---

## 3. Decisão arquitetural central: catálogo por categoria

**Problema**: cadastrar catálogo item-a-item no app (17 produtos já é manual; 500+ é inviável).

**Solução adotada**: um item de catálogo por **categoria do blog** (não por produto), com o link apontando para a página da categoria (que já lista todos os produtos dela, atualizada pelo pipeline do blog, fora do WhatsApp). Assim, quando o blog ganha um anúncio novo, o catálogo do WhatsApp não precisa ser tocado.

Categorias detectadas (via `dados_divulgacao.carrega_arvore()`, fonte: `categorias.json`):
| slug | nome | emoji | qtd. produtos (28/10) |
|---|---|---|---|
| tecnologia-e-informatica | Tecnologia & Informática | 💻 | 17 |
| audio-e-tv | Áudio & TV | 🎧 | 17 |
| casa-e-eletrodomesticos | Casa & Eletrodomésticos | 🏠 | 17 |
| bebe-e-maternidade | Bebê & Maternidade | 🍼 | 18 (categoria nova, surgiu entre 27/10 e 28/10) |
| casa-cama-e-decoracao | Casa, Cama & Decoração | 🛋️ | 15 |
| ferramentas-e-utilidades | Ferramentas & Utilidades | 🔧 | 16 |
| esporte-e-fitness | Esporte & Fitness | 💪 | 17 |
| beleza-e-saude | Beleza & Saúde | 🌸 | 43 |

URL de categoria no blog: `https://comprenolink.net/<slug>/` (confirmado via navegação real, ex. `https://comprenolink.net/audio-e-tv/`).

---

## 4. Script criado: `gerar_catalogo_categorias.py`

**Caminho**: `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Divugação_WhastsApp_Instagram\_fonte\gerar_catalogo_categorias.py`
**Comando**: `python -X utf8 _fonte\gerar_catalogo_categorias.py` (a partir de `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Divugação_WhastsApp_Instagram`)

**Lógica**:
1. `dd.carrega_produtos()` → dados com `arvore["categorias"]` e `itens` (cada item tem `x["cat"]["slug"]`).
2. Agrupa itens por `cat.slug`.
3. Para cada categoria da árvore com pelo menos 1 item:
   - Foto de capa: primeiro produto da categoria, processado com `cartao_foto()` (reaproveitada de `gerar_artes_catalogo.py`) → `fotos/CAT-<slug>.jpg` (1080×1080, fundo branco, cantos arredondados).
   - Nome: `"{emoji} {nome}"` (ex. `"🍼 Bebê & Maternidade"`).
   - Descrição: `"{chamada capitalizada}. Confira as {qtd} opções com o valor do dia no Mercado Livre pelo link. Link de afiliado: posso ganhar comissão, sem custo extra para você."`, truncada em 300 caracteres (limite do campo Descrição do catálogo do WhatsApp Business) — **ajustado nesta atividade**: a primeira versão usava o campo `intro` (mais longo) e ultrapassava 300 caracteres; trocado para o campo `chamada` (mais curto).
   - Link: `dd.utm(f"{SITE}/{slug}/", "whatsapp", "catalogo", "categoria", f"cat_{slug}")` → ex. `https://comprenolink.net/bebe-e-maternidade/?utm_source=whatsapp&utm_medium=catalogo&utm_campaign=categoria&utm_content=cat_bebe-e-maternidade`.
   - Código do item: `CAT-<slug>`.
4. Saída: `06_CATALOGO_WHATSAPP\CATEGORIAS\fotos\CAT-<slug>.jpg`, `06_CATALOGO_WHATSAPP\CATEGORIAS\CATALOGO_CATEGORIAS.xlsx` (planilha, mesmo estilo do catálogo por produto), `06_CATALOGO_WHATSAPP\CATEGORIAS\CATALOGO_CATEGORIAS_TEXTOS.txt` (texto para copiar e colar, formato `CÓDIGO / FOTO / PRODUTOS HOJE` + blocos `NOME:` / `DESCRIÇÃO:` / `LINK:`).

**Validação feita**: rodado em 27/10 (gerou 7 categorias) e de novo em 28/10 (detectou a 8ª categoria — Bebê & Maternidade — automaticamente, sem edição de código), confirmando que o mecanismo de escala funciona como projetado.

**Status no WhatsApp real**: as 8 categorias foram cadastradas manualmente pelo usuário no app (confirmado por print de tela, incluindo o estado "em análise" do WhatsApp para item novo, que é normal e dura até 24h).

---

## 5. Bugs encontrados e corrigidos

### 5.1 Caminho do OneDrive incorreto em `sincronizar_copias.py`
- **Sintoma**: a pasta `Divulgacao_Blog` nunca era sincronizada; a Parte 0 do guia do celular instruía abrir uma pasta que não existia.
- **Causa raiz**: constante `ONEDRIVE = r"E:\OneDrive\Downloads\Divulgacao_Blog"`. Nesta máquina, **não existe `E:\OneDrive`**; o OneDrive real do usuário está montado em `C:\Users\kkk\OneDrive`.
- **Correção**: `ONEDRIVE = r"C:\Users\kkk\OneDrive\Download\Divulgacao_Blog"`.
- Mesma correção aplicada em strings de documentação dentro de `gerar_divulgacao.py` (texto do `00_LEIA-ME_COMECE_AQUI.txt` e menção à agenda `.ics`) e em `conteudo_celular.py` (Parte 0 do PDF do celular).

### 5.2 Pastas duplicadas/divergentes no OneDrive
- **Sintoma**: existiam 3 pastas diferentes e parcialmente divergentes no OneDrive: `C:\Users\kkk\OneDrive\Divulgacao_Blog`, `C:\Users\kkk\OneDrive\Download\Planejamentos\Andamento\Celular_Whatsapp` (com uma subpasta lixo `Divulgacao_Blog` dentro, só com logos duplicados) e `C:\Users\kkk\OneDrive\Download\Divulgacao_Blog`.
- Havia também uma subpasta lixo `Divulgacao_Blog` dentro da própria pasta real `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Celular_Whatsapp` (mesma causa: logos duplicados de uma execução anterior mal direcionada).
- **Correção** (autorizada explicitamente pelo usuário antes de executar): removidas as 3 ocorrências de lixo/duplicata; mantida só `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Celular_Whatsapp` (fonte de verdade) e `C:\Users\kkk\OneDrive\Download\Divulgacao_Blog` (espelho), recriado do zero como cópia exata da pasta real (confirmado por `diff` de listagem de arquivos — 166 arquivos idênticos).

### 5.3 `sincronizar_copias.py` reescrito para lógica de espelho
- **Antes**: duas listas de nomes de arquivo (`SO_WHATSAPP` para a pasta real, `TUDO` para o OneDrive) que podiam divergir silenciosamente (causa raiz do bug 5.2).
- **Depois**: `copia()` leva a origem (`_fonte\..`) para a pasta real (`WHATSAPP`); `espelha()` copia a pasta real inteira para o OneDrive e **remove do destino qualquer item que não exista mais na origem** — garante que as duas pastas nunca mais divirjam.
- Tratamento de exceção mantido/generalizado: `PermissionError`/`shutil.Error` (arquivo aberto no celular ou no Excel) é ignorado por arquivo, sem interromper a cópia dos demais.

### 5.4 Conflito de edição concorrente em `sincronizar_copias.py`
- **Causa**: outra sessão de Claude Code, trabalhando em paralelo na automação do **Instagram** (mesmo usuário, mesmo projeto), edita o mesmo arquivo `sincronizar_copias.py` para incluir seus próprios itens (`10_POST_BOAS_VINDAS`, `11_INSTAGRAM_RESPOSTAS_SALVAS.txt`, depois também `12_CALENDARIO_INSTAGRAM.ics`), e em pelo menos duas ocasões sobrescreveu reversões para o caminho antigo (`E:\OneDrive`) e a lógica antiga de duas listas.
- **Mitigação aplicada**: o script foi re-mesclado múltiplas vezes nesta sessão, preservando os itens do Instagram da outra sessão dentro da nova lógica de espelho (lista `WHATSAPP_ITENS` + `INSTAGRAM_ITENS`, copiados via parâmetro `extras_origem` de `espelha()`).
- **Risco residual não eliminado**: por ser um arquivo compartilhado entre duas automações tocadas por sessões diferentes, o conflito pode voltar a ocorrer. **Recomendação explícita ao usuário**: coordenar com quem cuida do Instagram para não editar `sincronizar_copias.py` simultaneamente, ou dividir em dois scripts independentes (um por canal) que só compartilham a função `espelha()`.

---

## 6. Documentos gerados nesta atividade

### 6.1 PDF do passo a passo do celular (`08_PASSO_A_PASSO_WHATSAPP_NO_CELULAR.pdf`)
- Fonte: `conteudo_celular.py` (lista `CELULAR`), consumida por `gerar_divulgacao.gera_guia()`.
- Alteração: Parte 3 ("Catálogo") reescrita de uma única opção (por produto) para duas opções lado a lado — **Opção A (recomendada): catálogo por categoria** e **Opção B: catálogo por produto** — com passo a passo completo de cada uma.
- Regenerado via chamada direta (não via `main()` completo, para não tocar na planilha de calendário):
  ```python
  gera_guia(dados, os.path.join(PASTA, '08_PASSO_A_PASSO_WHATSAPP_NO_CELULAR.pdf'), CELULAR,
            'Passo a passo no celular<br/>WhatsApp Business',
            'Instalação, perfil, catálogo, respostas rápidas,<br/>Canal e a rotina de cada dia',
            'Passo a passo no celular')
  ```

### 6.2 PDF de estratégia (`09_ESTRATEGIA_WHATSAPP_VENDAS.pdf`) — documento novo
- Fonte nova: `conteudo_estrategia_whatsapp.py` (lista `ESTRATEGIA_WHATSAPP`), mesmo formato de blocos, consumida pelo mesmo `gera_guia()`.
- Conteúdo (13 páginas na versão final):
  1. Objetivo do plano.
  2. Fase 1 — Configuração do número (checklist do que já foi feito: perfil, catálogo, Canal, respostas rápidas).
  3. Fase 2 — Estratégia de catálogo por categoria (o porquê, tabela de quando precisa de atenção).
  4. Fase 3 — Rotina de divulgação semanal (Status 19:15, Canal, Grupos terças 12:00, Lista de transmissão).
  5. Fase 4 — Atendimento e conversão (tabela de fluxo de resposta, boas práticas).
  6. Fase 5 — Escala e manutenção (tabela gatilho → ação → script).
  7. Fase 6 — Métricas (tabela de utm_medium por canal, rotina de acompanhamento mensal).
  8. **Anexo A** — documentação de cada script, revisada a pedido do usuário para incluir: tabela cronológica de execução (A.0, com data/horário recomendado por script — rotina semanal às segundas 10:00–10:10, em ordem: `gerar_catalogo_categorias.py` → `gerar_artes_catalogo.py` → `gerar_divulgacao.py` → `sincronizar_copias.py`), e para cada script: "Para que serve" (detalhado), "Exemplo real" (com dados concretos desta sessão) e "Quando rodar".
  9. Anexo B — checklist de conformidade (regras de ouro: sem preço fixo, sem promessa de saúde, aviso de afiliado, limites de grupos/lista, proibição de automação de envio em massa).
- Registrado em `sincronizar_copias.WHATSAPP_ITENS` para ser sincronizado automaticamente dali em diante.

---

## 7. Estado atual do WhatsApp Business (confirmado pelo usuário, com prints)

- ✅ App instalado no número (11) 99495-9657, nome "Compre no Link".
- ✅ Perfil comercial: descrição, site, e-mail preenchidos.
- ✅ Mensagem de saudação e de ausência ativadas.
- ✅ Etiquetas: "Quer ofertas", "Pediu link".
- ✅ Catálogo por categoria: 8 itens cadastrados (confirmado por print; item novo "Bebê & Maternidade" em análise, aguardando aprovação do WhatsApp — até 24h, comportamento normal).
- ✅ Catálogo por produto: 17 itens (Top 10 Black Friday + Top 10 Natal, com sobreposição) cadastrados anteriormente.
- ✅ Canal "Compre no Link – Achados do Mercado Livre" criado (um duplicado foi criado por engano e removido pelo usuário, com orientação).
- ⏳ **Pendência não confirmada nesta sessão**: se o link do Canal já foi de fato colado na resposta rápida `/canal` (o usuário recebeu instrução, mas a confirmação final não veio por texto).
- ✅ 7 respostas rápidas criadas: `/bf`, `/natal`, `/link`, `/preco`, `/pedido`, `/canal`, `/obrigado`.

---

## 8. Validações técnicas realizadas nesta sessão (reprodutíveis)

```bash
# Confirma que o pipeline lê o blog ao vivo e detecta categorias
cd "D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento/Divugação_WhastsApp_Instagram"
python -X utf8 -c "
import sys; sys.path.insert(0, '_fonte')
import dados_divulgacao as dd
dados = dd.carrega_produtos()
print(len(dados['itens']), 'itens;', [c['slug'] for c in dados['arvore']['categorias']])
"

# Gera/atualiza o catálogo por categoria
python -X utf8 _fonte/gerar_catalogo_categorias.py

# Sincroniza pasta real + OneDrive (modo espelho)
python -X utf8 _fonte/sincronizar_copias.py

# Confirma espelho idêntico (usado para validar o bug 5.2)
diff <(cd "D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento/Celular_Whatsapp" && find . -type f | sort) \
     <(cd "C:/Users/kkk/OneDrive/Download/Divulgacao_Blog" && find . -type f | sort)
```

Dependência instalada nesta sessão (estava faltando no ambiente): `pip install reportlab` (v5.1.0).

---

## 9. O que NÃO foi feito / fora do escopo

- Nenhuma configuração do WhatsApp Business foi feita programaticamente — não existe API acessível para isso neste contexto; tudo foi feito pelo usuário na interface do app, guiado passo a passo.
- Não foi implementada nenhuma automação de envio de mensagens (bot, resposta automática além das nativas do WhatsApp Business) — avaliado e descartado nesta atividade por risco de banimento do número (automação de UI) ou custo/complexidade desproporcional (WhatsApp Cloud API oficial).
- Scripts do lado Instagram (`gerar_calendario_instagram.py`, `gerar_post_boas_vindas.py`, `gerar_reels.py`) não foram criados, revisados nem validados por esta atividade — pertencem à outra frente de trabalho.
- Não há dados reais de conversão/venda ainda; a Fase 6 (Métricas) do documento de estratégia define como e quando coletá-los (sugestão: só tirar conclusões após 4–6 semanas de execução consistente).

---

## 10. Para quem for validar/continuar este trabalho

1. Todos os scripts têm docstring no topo explicando o que fazem e o comando exato para rodar.
2. A ordem de execução segura é: `gerar_catalogo_categorias.py` → `gerar_artes_catalogo.py` → `gerar_divulgacao.py` (só a chamada específica do PDF que mudou, não `main()` inteiro, a menos que vários documentos tenham mudado) → `sincronizar_copias.py` (sempre por último).
3. Antes de editar `sincronizar_copias.py`, verificar se há mudanças recentes de outra sessão (ver seção 5.4) — ler o arquivo antes de editar, não assumir o conteúdo da última versão conhecida.
4. O documento `09_ESTRATEGIA_WHATSAPP_VENDAS.pdf` e sua fonte `conteudo_estrategia_whatsapp.py` são a referência viva da estratégia — qualquer mudança de estratégia deve ser refletida lá, não só em chat.
5. Este relatório descreve o estado até 30/10/2026. Para o estado atual, reexecutar o bloco de validação da seção 8.
