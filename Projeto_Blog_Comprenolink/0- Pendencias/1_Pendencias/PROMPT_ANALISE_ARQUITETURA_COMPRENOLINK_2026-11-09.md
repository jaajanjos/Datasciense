# Prompt de análise de arquitetura — CompreNoLink

Gerado em 09/11/2026 pela conversa "BLOG- Day by Day". Parte 1: prompt preenchido com os dados do projeto (pronto para reutilizar).
Parte 2: a análise feita pelo Claude nessa data. Itens marcados com (confirmar) não foram conferidos.

---

## PARTE 1 — PROMPT

ATUE COMO UM ARQUITETO DE SOFTWARE, ESPECIALISTA EM WORDPRESS, PYTHON, SEO E AUTOMAÇÃO.

Vou fornecer informações do meu projeto.

**OBJETIVO DO PROJETO:**
Blog de afiliados comprenolink.net que indica produtos do Mercado Livre (guia "Os Melhores Produtos do Mercado Livre em 2026" + páginas de categoria) e gera comissão pelo programa ML Afiliados, com divulgação orgânica no Instagram (@compre.no.link) e no WhatsApp (Status, Canal e catálogo por categorias).

**TIPO DE PROJETO:**
Blog WordPress + Afiliados + Sistema Python local de gestão e automação.

**ESTRUTURA DE PASTAS** (raiz `D:\Projeto_Blog_Comprenolink`; listagem completa em `Estrutura_diretorio_Projeto_Blog_Comprenolink.txt`, 382 pastas):
```
0- Pendencias\            1_Pendencias, 2_Analises_Anuncios, 3_Guia_Passo_a_Passo_Instagram_2026,
                          4_Relatorio_Ativ_Claude_no_Blog, 5_Plano_turbinar_anuncio_instagram
0_Arquivos_Bat\           menu geral (main_menu.py), compilação dos .exe
Cartao_Comercial\         cartão de visita (PDF + gerador)
Gestao_Anuncios_Blog\     1_PROGRAMAS (gerenciar_blog.py, painel, categorias), 2_DADOS (credenciais,
                          categorias.json, backups da página), 3_DOCUMENTACAO, 4_PACOTE_OUTRO_PC,
                          5_ESBOCO_CATEGORIAS, 9_ORIGINAIS_NAO_MEXER
Logo\                     logos, ícone, vídeos TikTok
Planejamentos\Andamento\  Automação_Instagram, Base_Contatos_WhatsApp, Celular_Whatsapp,
                          Divugação_WhastsApp_Instagram (pacotes do dia, geradores), Estrategias_Vendas,
                          Rastreamento_anuncios, Verificar_Erros_Blog
Planejamentos\Hold\       Dados_Tiktok
Programas_Diversos_Py\    ~19 geradores (relatório de atividades, pendências, agendas .ics) + backups
Relatorios_Diarios_Anuncios\  painel (xlsx/PDF), _historico_relatorios, anuncios_status, vendas_*,
                          programas_fontes_python (relatório, verificador, painel, .exe),
                          atualiza_automatica_py_anuncios (rotina em 5 etapas)
Security_Control\         security_top.txt
```

**TECNOLOGIAS UTILIZADAS:**
WordPress (Hostinger), Python 3.14 (requests/urllib, openpyxl, reportlab, Pillow, PyInstaller), PowerShell e .bat, Excel (painel), CSV/JSON (dados), API REST do WordPress (senha de aplicativo), snippet PHP próprio de rastreio (tabela MySQL `wp_rastreio_acessos`), Claude Code + Claude in Chrome (agendamento no Instagram), Agendador de Tarefas do Windows.

**PRINCIPAIS FUNCIONALIDADES:**
- Gestão do guia pela API (listar, editar, adicionar, remover, substituir item) com backup antes de publicar.
- Geração automática das páginas de categoria, Black Friday/Natal, Escolha rápida e menu.
- Rastreador próprio de visitas e cliques por anúncio/campanha (UTM) + relatório HTML de acessos e vendas.
- Verificação diária no ML dos 213 anúncios (ativo/pausado/removido) e quadro "Precisam de substituto".
- Painel de conversão e performance (planilha + PDF) com histórico de vendas.
- Pacotes diários de divulgação (feed, story, status, Reels, textos) e agendamento no Instagram.
- Base de contatos do WhatsApp com consentimento.

**PROBLEMAS ATUAIS:**
- Caminhos fixos nos programas (quebraram na mudança de pasta de 09/11/2026).
- Credenciais em texto puro (`wp_credenciais.json`, chave em `config_rastreio.json`).
- Sem controle de versão (Git) e sem backup externo do projeto.
- Muitos scripts soltos e de uso único; numeração duplicada; vários padrões de backup.
- Tarefas agendadas falham sem aviso.
- Guia único com 213 produtos (pesado e com tema diluído para SEO).
- Substituição de anúncios fora do ar é manual (a automação com IA foi descartada por custo).

**OBJETIVOS DE NEGÓCIO:**
Aumentar as vendas por afiliado (Black Friday e Natal 2026), crescer o tráfego orgânico (Google/Bing) e as redes sociais, validar o anúncio pago na Meta (teste R$ 50; teto R$ 255) e manter o custo de operação baixo (plano Claude Pro, sem custo extra).

**QUANTIDADE DE USUÁRIOS:**
Operação: 2 pessoas (dono e sócio). Público: tráfego ainda pequeno (19 vendas no histórico até 08/11/2026). (confirmar visitas/mês no Analytics)

**FLUXO DE TRABALHO:**
Diário (seg–sex): conferir anúncios e painel; dono publica Story/Status/Canal pelo celular com o pacote do dia. Semanal: segunda 20h o Claude agenda os posts/Reels do Instagram em lote; rodada de vendas (prints do ML Afiliados → CSV → painel). Sob demanda: trocar anúncios fora do ar (manual), novas categorias, ajustes no guia.

**AUTOMAÇÕES EXISTENTES:**
- Tarefa do Windows "Atualizar categorias blog comprenolink" (a cada 3 h).
- Tarefa do Windows "Backup automatico blog comprenolink".
- ATUALIZAR_PAINEL.bat (verificação + painel + PDF + limpeza).
- Rotina `atualiza_automatica_py_anuncios` (relatório + painel; substituição com IA desativada).
- Rotina agendada do Claude: segunda 20h, agendamento do Instagram em lote.
- Geradores de pacotes do dia, Reels, catálogo e agendas .ics.

**PLUGINS WORDPRESS** (conhecidos; confirmar a lista completa):
Rank Math SEO, Site Kit by Google, LiteSpeed Cache, Code Snippets (rastreador e ajustes), Hostinger Affiliate Plugin, FluentForms.

**SERVIDOR/HOSPEDAGEM:**
Hostinger (WordPress gerenciado, LiteSpeed, CDN Hostinger). Ferramentas: Google Search Console, Google Analytics, Bing Webmaster, ManyChat (Instagram), Meta Business Suite. Rotinas locais num mini PC Windows 11 (SRVRYZEN).

**ANALISE E FORNEÇA:**
1. Nota da arquitetura (0 a 10)
2. Nota da organização do projeto
3. Nota de segurança
4. Nota de escalabilidade
5. Nota de SEO
6. Nota de automação
7. Principais riscos
8. Oportunidades de melhoria
9. Refatorações recomendadas
10. Roadmap dos próximos 90 dias
11. Prioridades críticas
12. O que está faltando para tornar o projeto profissional

---

## PARTE 2 — ANÁLISE DO CLAUDE (09/11/2026)

### Notas

| Área | Nota | Por quê |
|---|---|---|
| 1. Arquitetura | **5** | Funciona e as peças conversam, mas é um conjunto de scripts sem núcleo comum; cada um repete caminhos, leitura de config e acesso ao WordPress |
| 2. Organização | **6** | Estrutura nova clara, mas `Programas_Diversos_Py` mistura uso único com ferramentas fixas; numeração duplicada; vários padrões de backup |
| 3. Segurança | **4** | Senha de aplicativo e chave da API em texto puro; sem Git nem cópia fora do PC; já houve zip com senha circulando (29/10) |
| 4. Escalabilidade | **4** | Tudo num único mini PC; verificação de 213 anúncios ~10 min e cresce com o guia; dados em CSV/Excel; página única com 213 itens |
| 5. SEO | **5** | Base boa (Rank Math, Search Console, Bing, rel=sponsored, categorias), mas o guia gigante dilui o tema e pesa; poucas páginas por produto/intenção |
| 6. Automação | **7** | Ponto forte do projeto; falta monitorar falhas silenciosas |

### 7. Principais riscos
1. Perda de tudo: um único PC, sem Git e sem backup externo do código e dos dados.
2. Credenciais expostas em arquivos legíveis.
3. Bloqueio no ML: a verificação raspa páginas públicas.
4. Falhas silenciosas de tarefas agendadas e caminhos fixos.
5. Conhecimento espalhado em PDFs, anotações e handovers.
6. Página única: um erro no guia afeta os 213 produtos.

### 8. Oportunidades de melhoria
- Páginas de comparação e "melhor X até R$ Y" a partir dos produtos que vendem; o guia vira índice.
- Usar os cliques do rastreador para decidir destaque e páginas próprias.
- Schema `ItemList`/`Product` nas listas.
- Painel web simples no lugar do Excel.

### 9. Refatorações recomendadas
1. Pacote comum `comprenolink_core` (caminhos, config, cliente WordPress, CSV, log).
2. Configuração única; segredos no Gerenciador de Credenciais do Windows (`keyring`).
3. Separar `Programas_Diversos_Py` em ferramentas e arquivo (sem apagar nada).
4. `requirements.txt` + `venv`.
5. Um único padrão de backup (`old_bkp`).
6. Históricos em SQLite; Excel só como relatório.

### 10. Roadmap 90 dias

| Período | Foco | Entregas |
|---|---|---|
| Dias 1–15 | Segurança e continuidade | Git com `.gitignore` para segredos; trocar a senha de aplicativo do WordPress; segredos no `keyring`; backup semanal externo |
| Dias 16–45 | Organização técnica | `comprenolink_core` + config única; `requirements.txt`; reorganizar `Programas_Diversos_Py` (com "de acordo"); alerta de falha das tarefas |
| Dias 46–75 | SEO e conteúdo | Schema nas listas; 4 a 6 páginas de comparação/intenção; velocidade do guia; medir no Search Console |
| Dias 76–90 | Escala e decisão | Painel web simples; avaliar VPS se o volume crescer; revisão de Black Friday/Natal para 2027 |

### 11. Prioridades críticas
1. Backup externo e Git do projeto.
2. Tirar a senha do WordPress do arquivo e trocá-la.
3. Alerta de falha das tarefas agendadas.

### 12. O que falta para ficar profissional
Controle de versão, segredos protegidos, configuração única, dependências declaradas, monitoramento de falhas, documentação viva num lugar só (README), testes básicos nos programas que publicam no site e estratégia de conteúdo além do guia único.

### Conclusão e pontos de atenção
**Conclusão:** projeto acima da média para um blog de afiliados desse porte em automação e medição; o que segura é a base técnica frágil. Corrigindo os 3 itens críticos (~2 dias), segurança e organização sobem para ~7.

**Pontos de atenção:** reorganização de pastas só com "de acordo" e `old_bkp`; a troca da senha do WordPress é feita pelo dono; as refatorações são da conversa "BLOG- Pendência e ajustes em programas".
