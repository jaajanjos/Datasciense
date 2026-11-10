# RELATÓRIO MESTRE DE CONTINUIDADE DO PROJETO COMPRENOLINK
Data de corte: **07/11/2026 (sábado)**. Autor: Claude (assistente de IA que acompanhou o projeto, conversa "000- Análise Checklist Turbinar Vendas").
Destinatário: outra IA (ChatGPT Plus) que vai assumir a continuidade. Idioma do projeto: **português do Brasil**.

## AVISOS DE LEITURA (leia primeiro)
1. **Este documento é um retrato de 07/11/2026.** Cada fato vem de registros que o Claude tem: anotações de memória, relatórios de atividades, documentos em `D:\mercado_livre\0- Pendencias\1_Pendencias` e as conversas. Onde não há registro está escrito **"desconhecido"** ou **"a confirmar"**. Nada foi inventado.
2. **Fontes de verdade:** lista de pendências do dono = `nova_pendencias.pdf`; agenda = `agenda_nova_pendencias.ics`; estrutura de pastas = `D:\mercado_livre\Nova_Estrutura_diretorio_Mercado0_Livre.txt`. Este relatório não substitui esses arquivos.
3. **Reunião de replanejamento geral marcada pelo dono para segunda 09/11/2026 às 09:00** (escopo: replanejar TODAS as atividades até 31/12/2026, uso do plano do Claude, peso das tarefas). **Qualquer agenda descrita aqui pode mudar nessa reunião.** Não trate agendas antigas como automaticamente ativas.
4. **Não estão neste documento:** senhas, tokens, chaves, códigos de recuperação, números de cartão, nem nomes e telefones de contatos pessoais. O arquivo `wp_credenciais.json` (senha de aplicativo do WordPress) existe no PC do dono e **não deve ser copiado para nenhuma IA**.
5. O pedido original terminava em "REGRAS OBRIGATÓRIAS DO RELATÓRIO – Utilize..." e o texto foi cortado. Foram aplicadas as regras implícitas do próprio pedido: não incluir segredos, não inventar métricas, diferenciar executado de proposto, e marcar o que é desconhecido.

---

## 1. IDENTIFICAÇÃO E OBJETIVOS DO PROJETO

| Item | Informação |
|---|---|
| Nome comercial | **CompreNoLink** ("Compre no Link – Achados do Mercado Livre") |
| Dono | José Antônio dos Anjos (opera sozinho no dia a dia; usa a conversa do Claude como "braço direito"). Sócia/sócio participa de decisões (reunião do Turbinar em 05/11; chamada "sócio" nos documentos; o painel do ML Afiliados do blog já foi lido logado na conta de uma sócia do dono) |
| Modelo de negócio | **Marketing de afiliados do Mercado Livre**: o dono divulga produtos com links de afiliado (meli.la) e recebe comissão por compras feitas pelo link. O blog **não vê compras**; as vendas só aparecem no painel do ML Afiliados |
| Proposta de valor | "Achados" do Mercado Livre organizados por categoria, em um guia com ~214 produtos, com texto de venda honesto, sem preço, sem promessa, com aviso de link de afiliado |
| Público e segmentos | Consumidor brasileiro de compras online. Categorias do blog (9): Tecnologia & Informática, Áudio & TV, Casa & Eletrodomésticos, Casa/Cama & Decoração, Ferramentas & Utilidades, Esporte & Fitness, Beleza & Saúde, Bebê & Maternidade, Moda Infantil & Juvenil. Campanhas sazonais: **Black Friday (27/11/2026)** e **Natal** |
| Foco decidido em 03/11/2026 | **Só WhatsApp + Instagram + Mercado Livre (afiliados/anúncios) + ajustes do blog.** TikTok descartado; Telegram, YouTube, Facebook e Pinterest fora do foco (reavaliar após a Black Friday; não propor antes) |
| Divulgação (visão geral) | Instagram diário (post + Reels + Story), Status e Canal do WhatsApp, catálogo do WhatsApp por categoria, ManyChat (resposta automática a comentários), e-mail com consentimento, anúncio pago em teste |
| Aquisição e conversão | Tráfego do Instagram/WhatsApp → páginas do blog (guia e categorias) → clique no link meli.la → compra no Mercado Livre → comissão |
| Metas conhecidas | Curto: Black Friday e Natal; teste de anúncio pago (R$ 50). Médio: crescer o Canal com consentimento; medir cliques e vendas. Longo: decisão em janeiro/2027 com números (não há metas numéricas de vendas registradas) |
| Situação de operação | **Em operação.** Blog no ar, Instagram agendado até 04/12, Canal do WhatsApp ativo, conta de anúncios Meta criada (sem anúncio rodando), vendas ainda baixas |

**Números conhecidos (ML Afiliados, 02/11/2026, 180 dias):** 128 cliques, 2 compradores, 12 ordens, R$ 1.166,84 brutos, R$ 172,00 de ganho estimado (em revisão), 19 vendas na lista (12 em revisão, 7 canceladas). As 7 "recusadas por conta vinculada" (R$ 65,58) foram **compras do próprio dono**. Só uma venda orgânica real confirmada (Tampa de micro-ondas, comissão R$ 2,29). **Regra:** dono, família e sócio **não compram pelo link do blog** (sem comissão e risco à conta de afiliado).

---

## 2. ESTRUTURA DIGITAL E TECNOLÓGICA

### 2.1 Blog (WordPress)
| Campo | Detalhe |
|---|---|
| Endereço | `https://comprenolink.net` (guia principal: `/melhores-produtos-mercado-livre-2026/`; também `/black-friday/`, `/presentes-de-natal/`, 9 páginas de categoria, Sobre, Privacidade, Contato) |
| Plataforma | WordPress na **Hostinger**, tema Futurio, CDN/LiteSpeed (cache) |
| Plugins conhecidos | All in One SEO, LiteSpeed Cache, Code Snippets, WPForms Lite, **Fluent Forms** (form de inscrição id 4), Hostinger Affiliate Plugin (blocos de produto), Site Kit (GA4) |
| Finalidade | Vitrine e guia de produtos com links de afiliado; destino do tráfego |
| Implantado | Guia com ~214 produtos sem preço; 9 categorias; páginas Black Friday e Natal (Natal entra no menu em 01/12 automaticamente); formulário de e-mail com consentimento; botão do Canal do WhatsApp; backups automáticos; GA4; Search Console; sitemap; Bing Webmaster |
| Não implantado | Envio de e-mail das campanhas (sem ferramenta escolhida: Reach/Brevo/MailerLite); página `/canal`; e-mail do site não chega (Hostinger/Gmail sem senha de app) |
| Dependências | Hostinger, plugin de afiliado (renderiza título/foto ao vivo do ML), scripts Python locais, tarefas do Windows |
| Problemas conhecidos | Anúncios do ML saem do ar com frequência (painel avisa); numeração `#item-N` do guia muda quando se retira/inclui item (links dos pacotes podem apontar para o vizinho); links de catálogo `/p/MLB...` podem cair em anúncio pausado; "Search Console: dados em processamento" |
| Próximas ações | Conferir `/presentes-de-natal/` no Search Console (10/11); republicar categorias após novos anúncios; reler termos do ML (13/11) |

### 2.2 Instagram (@compre.no.link)
- Conta profissional "Compre no Link | Achados ML". Bio com 3 linhas; links da bio: `comprenolink.net/black-friday` e o WhatsApp do blog. Post de boas-vindas fixado (com automação ManyChat). 6 respostas salvas no app. Em dezembro trocar o link 1 da bio para `/presentes-de-natal` e a bio para versão Natal.
- **Rotina diária:** 1 post (19:00) + 1 Reels (19:05) agendados via Instagram web ("Programar conteúdo"), mais Story 19:10 com adesivo de link (Meta Business Suite).
- **Limite técnico:** só dá para agendar até ~29 dias à frente; a janela do dia D abre por volta das 20:00 do dia D-29. Hora mínima: daqui a 20 minutos.
- **Situação:** agendado de 02/11 até **04/12** (04/12 feito em 05/11 às 21:09: Perfume Árabe Sabah Al Ward). Faltam agendar: 07/12, 09/12, 11/12, 14/12, 16/12, 18/12, 21/12, 23/12 (ver agenda).
- Dias "de lista" (sem post): 01/12, 08/12, 15/12 e 22/12 (e terças de novembro).
- Não dá pelo computador: links da bio, fixar post, respostas salvas, destaques (são feitos no celular pelo dono).
- Dependências: Chrome com a extensão Claude conectada e Instagram logado (o Claude nunca digita senha).

### 2.3 WhatsApp
- **Número principal (WhatsApp Business):** (11) 99495-9657 (público no blog). Nome comercial, saudação, horário, 7 respostas rápidas (/canal /bf /natal /link /preço /pedido /obrigado), **catálogo apenas por categoria** (9 itens CAT-..., decisão de 06/11: produtos individuais não entram; os 17 produtos foram apagados pelo dono em 06/11).
- **Canal:** um só, "Compre no Link – Achados do Mercado Livre", link `https://whatsapp.com/channel/0029Vb9eTLd3rZZlBFjs8J3A`. Botão no blog (Contato, Início, Guia, Black Friday, Natal) e na bio. 2 seguidores em 04/11 (número atual: **desconhecido**). Segundo administrador: o dono disse em 05/11 que já está resolvido (**não verificado pelo Claude**).
- **Grupos:** o WhatsApp do blog não participa de nenhum; campanha de 12:00 em grupos foi removida do plano.
- **Segundo número (reserva), ativo desde 06/11/2026:** WhatsApp comum no mesmo celular (dual SIM). Regras: conversa normal e reserva; sem convites, sem mensagens em massa nos primeiros dias, sem migrar Canal/catálogo, sem automação.
- **Base de contatos:** `12_Base_Contatos_WhatsApp\Base_Contatos_WhatsApp.xlsx`, 500 linhas (origem: agenda de contatos do dono e da sócia). Somente contatos com **consentimento "Conhecido"** podem receber convite. 24 aprovados em 05/11 (23 aptos após uma exclusão por não ter WhatsApp). Os outros ~450 estão **fora da fila**.
- **Convites:** **só à mão, pelo celular, pelo dono**; até 5/dia na 1ª semana (06 a 12/11), até 9/dia depois; 3 minutos entre mensagens; 9h–20h; sem convites em 27/11. Parar 7 dias ao primeiro aviso do WhatsApp; parar o dia com 2 pedidos de saída ou 1 denúncia. **A automação de convites foi cancelada em 04/11** por risco de bloqueio do número.
- WhatsApp Web: o Claude usa (com autorização) para Status/Canal/catálogo; conectar exige QR do dono. **Armadilhas:** ENTER envia na hora; legenda de Status não aceita quebra de linha; campo "Link" do catálogo aceita só **75 caracteres**.

### 2.4 Mercado Livre Afiliados
- Links `meli.la` gerados pelo **dono** no painel de afiliados (Claude não loga). Link de produto de catálogo (`/p/MLB...`) devolve sempre o mesmo meli.la (pode cair em anúncio pausado); usar outro produto ou anúncio `/up/MLBU...`.
- Vendas: o ML **não tem botão de exportar**; o dono tira prints da aba Vendas e o Claude monta `vendas_ml_AAAA-MM-DD.csv` para o painel.
- **Termos oficiais lidos em 05/11 e 06/11** (`mercadolivre.com.br/ajuda/30228`, cláusula 4.4): mídia paga **permitida só em redes sociais** (Instagram/Facebook/TikTok/Pinterest Ads), a partir de conta do próprio afiliado já aprovada. **Proibido:** Google/Bing/YouTube Ads; palavras-chave com a marca ("Mercado Livre", "ML", "Meli", "Mercado Pago"); passar-se por canal oficial; mídia paga sobre conteúdo de creators; comprar pelo próprio link; anúncios que redirecionam sem ação do usuário.

### 2.5 Painel de métricas (local, Excel + Python)
`99_Relatorios_Diarios\ATUALIZAR_PAINEL.bat` (~10 min; fechar o Excel antes): verifica os 214 anúncios, lê relatórios de acesso, vendas e gera `Painel de Controle de Acesso.xlsx` + PDF. Aba Resumo_ML guarda os totais oficiais digitados. Atribui vendas a visitantes por semelhança de nome e data. Retenção: manda arquivos antigos para a Lixeira.

### 2.6 Medição
- **Google Analytics 4** (propriedade do comprenolink.net via Site Kit) e **Google Search Console** (propriedade `https://comprenolink.net/`): ficam no **Chrome lilás (perfil "comprenolink")**, onde a extensão do Claude **não** conecta. O Claude lê pela tela com o dono. No perfil "José Antônio" esses serviços aparecem vazios: **nunca clicar em "Começar a usar"**.
- **Bing Webmaster Tools:** logado no perfil José Antônio (2 mapas do site enviados, 30 URLs descobertas).
- Números de 06/11: Analytics 7 dias (até 05/11): 17 usuários, 21 sessões, 0 eventos principais; Direct 10, Organic Social 8, Organic Search 3; parte do tráfego (EUA) provavelmente robôs. Search Console: 0 cliques, indexação em processamento; home, guia e 9 categorias indexadas pela Inspeção de URL.

### 2.7 Automação (ManyChat)
- Conta **grátis** conectada ao Instagram (recusar "Start Free Trial"). Automação **LIVE** "Autoenviar links a partir de comentários...": só no post de boas-vindas (plano grátis = 1 post por automação). Palavras: BLACK, LINK, QUERO. Responde 1 vez por pessoa; DM com botão para a lista no blog.
- **Não implantado:** "Comente CANAL" (precisa de um post que peça essa palavra e uma automação nova; texto do Direct já entregue ao dono). Teste com segunda conta pendente (11/11, dono).
- Dependência: ManyChat só abre no **Chrome lilás** (ou Edge); o painel do app é bloqueado por proteção do site.

### 2.8 Ferramentas de IA e infraestrutura local
- **Claude (Pro):** conversa principal "000- Análise Checklist Turbinar Vendas"; tarefas por cron de sessão, Chrome com extensão, leitura/escrita de arquivos locais, Excel via COM, geração de PDFs (ReportLab). Backup das conversas em `E:\BKP_INTEGRA_CLAUDE\BACKUPS` (rodízio de 5; último: 06/11/2026 22:02; pasta FREEZE de 04/11 não pode ser apagada).
- **Dois perfis do Chrome:** **José Antônio** (extensão Claude conectada; Instagram, WhatsApp Web, Google Agenda, Meta, Bing) e **lilás "comprenolink"** (ManyChat, Gmail do blog, Analytics, Search Console; sem extensão).
- **PC1** (Windows 11, "Svr_Ryzen", ligado e sem suspender) e **PC2** (pacote do painel do blog; atualização a testar).
- **Tarefas do Windows:** backup do blog a cada 30 min e atualização de categorias a cada 3 h (caminho corrigido em 02/11).
- **Blog das máquinas de cortar cabelo:** projeto à parte (Google Sites), painel HTML em `9_Manutenção_Blog\1_PROGRAMAS\Blog_Maquinas`. Republicar no Google Sites estava em andamento (situação atual: desconhecida).
- Outros projetos técnicos do dono (não fazem parte do CompreNoLink): kit de dublagem em PT-BR, laboratório PostgreSQL, app Nunvox, otimização do mini PC.

### 2.9 Integrações
| Integração | Estado |
|---|---|
| Blog ↔ Search Console / Bing / GA4 | Funcionando |
| Instagram ↔ ManyChat | Funcionando (1 automação) |
| Blog ↔ Instagram/WhatsApp (UTM) | Links com `utm_source/medium/campaign/content`; **sem visitas com UTM de Instagram/WhatsApp/ManyChat desde 31/10** (investigar em 09/11) |
| Painel ↔ ML Afiliados | Manual (prints → CSV) |
| E-mail do site (SMTP) | **Não funciona** (FluentSMTP instalado sem configuração) |
| Envio de campanhas de e-mail | Planejado, sem ferramenta |
| Google Agenda ↔ agenda .ics | Importado em 04/11 (69 eventos; hoje 68 após remoção de 9 lembretes) |

---

## 3. HISTÓRICO CRONOLÓGICO

Legenda de situação: **Concluída**, **Pendente**, **Em andamento**, **Cancelada**, **Decisão**, **Proposta**.

| Data | Atividade | Plataforma | Resultado | Situação |
|---|---|---|---|---|
| 29/09/2026 | Plano orgânico inicial do Instagram (20 pautas) | Local | Obsoleto (usava preços) | Substituído |
| 21/10 | Diagnóstico e ajuste do blog: home, guia, títulos, menu, páginas Sobre/Privacidade/Contato, CSS, snippets | WordPress | 105/110 visitas caíam na home vazia; corrigido | Concluída |
| 22–23/10 | Painel de acessos (Excel), backups automáticos, painéis do blog, pacote do outro PC | Local/Excel | Painel funcionando; backup a cada 30 min | Concluída |
| 23–26/10 | Cadastro em lote de anúncios (de 21 a 140 itens), tom de venda sem promessas, árvore de 9 categorias, campanhas BF/Natal programadas, atualização automática a cada 3 h | WordPress | Guia com 140 → 214 itens | Concluída |
| 26/10 | Pacote de divulgação (guia, checklists, 108 tarefas), catálogo, 34 pacotes diários, passo a passo do WhatsApp, logo | Local | Pronto | Concluída |
| 27/10 | Instagram profissional, bio, post de boas-vindas fixado, ManyChat conectado; Search Console configurado; histórico de vendas | Instagram/ManyChat/GSC | Operando | Concluída |
| 27–28/10 | PDFs: Plano Turbinar (R$ 30/135/235, substituído em 05/11), Guia Passo a Passo do Instagram, Análise Crítica dos anúncios | Local | Entregues | Concluída (valores atualizados em 05/11) |
| 29/10 | Agendamento no Instagram de 02/11 a 27/11; teste ManyChat; cartão comercial A4; relatório de atividades criado | Instagram | 28 de 28 itens de novembro | Concluída |
| 30/10 | Pesquisa de 37 anúncios novos, retirada de 17 repetidos, texto dos 37 novos, estrutura oficial de pastas; agendamento de 28/11 | WP/ML/IG | Guia: 194 → 177 → 214 | Concluída |
| 31/10 | Artes/Reels de novembro e dezembro refeitos sem "mais vendidos"; CSV de vendas: 19 vendas, R$ 172 pendentes | Instagram/Painel | Novembro completo | Concluída |
| 01/11 | Numeração `#item-N` mudou; refeitos 27 pacotes; links do catálogo (16) corrigidos no WhatsApp; calendário semanal de vendas | WhatsApp/Local | Corrigido | Concluída |
| 02/11 | 3 anúncios fora do ar substituídos; 7 categorias cadastradas no catálogo; Status/Canal/Story do dia; 10 Stories agendados; sync de anotações cancelada; tarefas do Windows corrigidas; Air Fryer/LG sem frases problemáticas | Vários | Concluída | Concluída |
| 03/11 | Reunião com sócio (sem verba paga por ora; sócio direciona o Claude); agenda única importada; pendências em arquivo único; vendas recusadas = compras do dono; botão do Canal no blog; página de Natal publicada antes; formulário no Fluent Forms; foco em WhatsApp+Instagram+ML | Vários | Decisões registradas | Concluída/Decisão |
| 04/11 | Atividade 9: Canal na bio/blog, Status de convite; **base de contatos criada**; **automação de convites cancelada** por risco; 02/12 agendado; handover 001→000; agenda importada | WhatsApp/IG/Local | Concluída | Concluída |
| 05/11 | Reunião Turbinar: **anúncio pago liberado** (teste R$ 50); conta de anúncios Meta criada, cartão e limite R$ 50; 24 contatos aprovados; descrição do Canal corrigida; docs corrigidos para R$ 50/155/255; termos do ML lidos; 04/12 agendado (21:09); limpeza (9 eventos, CSVs, aba Reserva); chip novo comprado | Vários | Concluída | Concluída |
| 06/11 | Catálogo só por categorias (17 produtos apagados pelo dono; 9 capas novas aplicadas; arte "Escolha sua categoria" no Canal); medição lida; indexação conferida; **segundo número ativo**; plano da semana; 3 substituições de anúncios; orçamento de uso do Claude | Vários | Concluída | Concluída |
| 07/11 | Conversas unificadas (fork renomeado, antiga a arquivar); este relatório | Claude | — | Em andamento |

**Executado × decidido × proposto:** *executado* = linhas com "Concluída"; *decidido pelo dono* = foco de canais (03/11), teste de R$ 50 e total máximo R$ 255 (05/11), catálogo só por categoria (06/11), sem automação de convites (04/11), "mantém tudo à noite sem alteração" (06/11); *proposto e não autorizado* = Telegram/outros canais após a BF; anúncio além do teste; ManyChat Pro (US$ 15, só se estourar o limite grátis); *cancelado* = automação de convites no WhatsApp, TikTok, campanha 12:00 em grupos, sincronização de anotações do Claude, envio em massa.

---

## 4. CRONOGRAMA E AGENDA OPERACIONAL

**Aviso:** a tabela abaixo é o que estava **vigente em 07/11**. **Confirmar após a reunião de 09/11 09:00.** Itens marcados (A) vieram de agenda antiga e precisam de confirmação.

### 4.1 Rotina diária
| Horário | Atividade | Plataforma | Responsável | Situação |
|---|---|---|---|---|
| 10:00 | Convites à mão (até 5/dia; 3 min entre eles) e depois avisar "enviei..." | WhatsApp (celular) | Dono | Vigente; execução de 06/11 **desconhecida** |
| 19:00 | Post do feed (já agendado até 04/12) | Instagram | Automático (agendado) | Vigente |
| 19:05 | Reels (idem) | Instagram | Automático | Vigente |
| 19:10 | Story com adesivo de link; **19:15 Status; 19:20 Canal** (conforme o "pacote do dia") | Meta Business Suite / WhatsApp Web | Claude (tarefa diária ~19:12 em **outra conversa**) ou dono | **A confirmar:** a tarefa 19:12 gasta cota do Claude; o dono vai reavaliar em 09/11 |
| 19:20 | Responder as pessoas | Instagram/WhatsApp | Dono | Vigente |
| 20:30 | Fechar o dia | — | Dono | Vigente |
| ~20:39 (dispara ~21:09) | **Agendar o post+Reels do próximo dia cuja janela de 29 dias abriu** | Instagram web | Claude (cron de sessão) | Vigente (cron recriado na conversa maior em 06/11; **conferir que existe UM só**) |
| 12:00 | Grupos de WhatsApp | — | — | **Cancelada** (3/11) |

### 4.2 Janelas de agendamento do Instagram (D-29, ~20:00)
04/12 (feito) · 07/12 abre 08/11 · 09/12 abre 10/11 · 11/12 abre 12/11 · 14/12 abre 15/11 · 16/12 abre 17/11 · 18/12 abre 19/11 · 21/12 abre 22/11 · 23/12 abre 24/11. Produtos: 07/12 Perfume Árabe Asad 100 ml Masculino; 09/12 Smartwatch T900 S10 Ultra Pro; 11/12 Fone JBL Tune 730; 14/12 Caixa JBL Go 5; 16/12 Pipoqueira Mondial Popflix 1200 W; 18/12 Máquina de Cortar Cabelo Nixzen; 21/12 Lençol Casal Percal 600 fios; 23/12 Cortina de LED 3x3 m. **Confirmar fotos/âncoras de 09/12, 14/12 e 18/12 antes de agendar.**

### 4.3 Rotina semanal e mensal
| Quando | Atividade | Responsável | Observação |
|---|---|---|---|
| Segunda 10:00 | Rodada semanal: seguidores do Canal, formulário do blog, prints de vendas → CSV → painel, anúncios fora do ar, links | Dono + Claude | Calendário semanal em `Calendario_Execucao_Semanal_WhatsApp_Vendas.ics` |
| Segunda 10:45 / sexta | Números e SEO (guia 13/11, 26/11, 11/12 conferir "Atualizado em") | Claude | Rotinas em `Roteiro_Rotinas_Segunda_e_Sexta.pdf` |
| Sexta 12:00 | Regra dos 70%: se o uso semanal do Claude passou de 70%, só o essencial | Claude | Orçamento semanal sugerido no memo do projeto |
| Todo dia 1º | Limite de gastos da conta de anúncios reinicia | — | Meta |

### 4.4 Datas fixas
| Data | Evento |
|---|---|
| 08/11 20:00 | Abre janela de 07/12 |
| 09/11 09:00 | **Reunião de replanejamento geral** |
| 09/11 | Rodada semanal pesada; Search Console/Bing; rascunho do anúncio (sem ativar); item 77 Colágeno; capas dos Destaques |
| 10/11 | Conferir `/presentes-de-natal/` no Search Console; revisar a página; agendar 09/12 |
| 11/11 | Teste do ManyChat (dono); **recriar o cron do Instagram** (expira ~12/11); Air Fryer no feed |
| 12/11 | Agendar 11/12 |
| 13/11 | Reler termos do ML; mostrar anúncio para aprovar; painel; links do guia; rotina de SEO |
| 16/11 | **Dono ativa o anúncio de teste (R$ 50, 16–18/11)** com apoio do Claude |
| 19/11 | Avaliação do teste (semáforo) |
| 20/11 | Se verde, subir limite de gastos para R$ 155 |
| 21–27/11 | Black Friday pago R$ 105 (**só se o teste deu verde**) |
| 27/11 | Black Friday (sem convites); campanha vale até 30/11 |
| 30/11 | Segunda avaliação; decidir Natal |
| 01/12 | Natal assume menu/home; pedir indexação de `/presentes-de-natal/`; bio de Natal |
| 04/12 | Se a BF se pagou, subir limite para R$ 100 |
| 05–14/12 | Natal pago R$ 100 (condicional) |
| 21/12 | Relatório final do Turbinar |
| Jan/2027 | Reunião de decisão com os números |

---

## 5. PROCESSOS OPERACIONAIS E EXECUÇÃO

**5.1 Escolher produtos.** Critério usado em 30/10: anúncio de catálogo, sem "Ad", sem vendedor internacional, sem recondicionado, nota ≥ 4,5, muitas vendas; para substituições, melhor política de venda (MercadoLíder/verde › Full › frete grátis › devolução grátis › garantia › nota ≥ 4,5 › preço ±20%). O dono inclui os anúncios no blog; o Claude trata os textos.

**5.2 Links de afiliado.** Só o **dono** gera o meli.la no ML Afiliados (botão Compartilhar → "Gerar link"). Verificar abrindo o meli.la e lendo o primeiro cartão da página: tem de mostrar o produto certo, sem "Anúncio pausado". Preço: ler **na página do produto**, não na lista (a lista pode mostrar parcela; descartar "Internacional/Envio dos EUA").

**5.3 Textos (política permanente).** Sem preço (usar "confira o valor do dia no Mercado Livre"); sem "melhor", "menor preço", "mais vendido", "líder", "oferta do mês", "garantido"; sem promessa de saúde ou estética; só fatos do título do anúncio; aviso "Publi: contém link de afiliado" em todo texto; atrativo para a compra, sem inventar dados.

**5.4 Publicar no blog.** `gerenciar_blog.py editar N ... [--aplicar]` (sem `--aplicar` só prévia), sempre com backup; depois `publicar_categorias.py --publicar`. Páginas de categoria e campanha são geradas por `categorias.json`: **editar direto no WP é desfeito**. Aquecer o cache depois (usar `?nc=`, não `?m=`).

**5.5 Instagram diário (roteiro que funciona).** (1) Chrome "Browser 1" com Instagram logado; (2) `instagram.com/scheduled_content`; (3) conferir no calendário **mensal** se o dia já tem 19:00 e 19:05 (evita duplicar); (4) copiar `feed.png`/`reels.mp4` do pacote do dia para a pasta temporária da sessão (upload é bloqueado a partir de `4- Celular_Whatsapp`); (5) "Programar conteúdo" → enviar arquivo → "Avançar" (no Reels antes escolher corte "Original"); (6) legenda = `2_LEGENDA_REELS.txt` sem a 1ª linha e sem a linha `====`, **digitada com o teclado (nunca colar via script: as quebras de linha somem)**; conferir contador (~800/2.200); (7) data: abrir o seletor, ir ao mês, clicar o dia; (8) hora: digitar `hh` e `mm` separados (nunca "1900" junto); (9) "Programar" e esperar ~18 s; (10) recarregar e conferir no calendário mensal. Se aparecer "Escolha uma data dentro dos próximos 29 dias", esperar 30 min e repetir; se pedir login, **parar e avisar o dono**.

**5.6 WhatsApp (Status, Canal, catálogo).** Pelo WhatsApp Web, com autorização e QR do dono. Status e Canal: imagem + legenda em **uma linha só** (ENTER envia). Catálogo: editar item por clique real; campo Link ≤ 75 caracteres; itens alterados ficam "em análise". **O Claude nunca apaga itens/posts do Canal ou do catálogo (irreversível); o dono faz.**

**5.7 Contatos e convites.** Seção 2.3. Marcar "Conhecido" só por aprovação explícita do dono, **nunca em lote**. Antes de cada convite, conferir nome/foto no chat (os números podem estar sem DDD no celular). Registro: o dono escreve "enviei Nome1, Nome2" e o Claude anota na Base.

**5.8 Medir.** Segunda: baixar relatório de acessos (`1_relatorio_acessos_anuncios.exe`), dono manda prints de vendas, Claude monta CSV, roda `ATUALIZAR_PAINEL.bat`. Usar visitantes únicos do GA4, não o contador do painel (inclui testes). Vendas: totais oficiais na aba Resumo_ML.

**5.9 Campanhas.** Seção 6. **5.10 Verificação de cada atividade:** conferir o resultado no calendário/arquivo/página (nunca só a mensagem "foi programado"); registrar no relatório diário.

**5.11 Relatório diário.** PDF `RELATORIO_ATIVIDADE_CLAUDE_BLOG_DD_MM_AAAA_HHhMM.pdf` em `0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog`, gerado por `99_Programas_PY\gerar_relatorio_atividade.py` (listas `ATIVIDADES`, `FALTA_AGENDAR`, `REEXECUCAO`); apagar só o PDF superado da própria conversa (Lixeira). O relatório **não lista pendências novas**: aponta para `nova_pendencias.pdf`.

---

## 6. MARKETING, ANÚNCIOS E INVESTIMENTOS

- **Orgânico:** Instagram diário, Status/Canal, catálogo por categoria, ManyChat, blog/SEO, e-mail com consentimento. Hashtags por categoria sem marca; aviso "Publi".
- **Pago (Meta/Instagram) — decisão de 05/11/2026:** conta de anúncios "Compre no Link – Anúncios" criada (pagador = dono, no cartão de crédito); **limite de gastos R$ 50**; cobrança ao atingir R$ 12 ou em 30/11.
  - **Teste:** R$ 50 no total (~R$ 16,67/dia), 16–18/11, objetivo Tráfego (visitas à página), **só Instagram**, Brasil, 18–45 anos, destino = página do guia com `?utm_source=instagram&utm_medium=pago&utm_campaign=teste_turbinar`. **Nunca** link meli.la direto; sem a marca Mercado Livre no anúncio.
  - **Black Friday:** R$ 105 (21–27/11) **só se o teste der verde**. **Natal:** R$ 100 (05–14/12) só se a BF se pagou. **Total máximo R$ 255.**
  - **Semáforo (custo por clique):** ≤ R$ 0,50 verde. Ponto de equilíbrio estimado com comissão média de R$ 9,05 (a estimativa foi considerada otimista: a venda orgânica real rendeu R$ 2,29).
  - **Limite de gastos:** sobe para R$ 155 em 20/11 (se verde) e para R$ 100 em 04/12 (se a BF se pagou). Reinicia no dia 1º de cada mês.
  - Estado em 06/11: saldo R$ 0,00, nada a pagar, nenhum anúncio criado.
- **Campanhas realizadas:** nenhuma paga. **Planejadas:** as três acima. **Canceladas:** Google Ads/Bing/YouTube (proibidos pelo ML).
- **Métricas disponíveis:** só as de blog (Analytics/Search Console/painel). **Alcance, impressões, CTR, CPC, conversões e ROI de anúncio: não existem ainda (nada rodou).** Vendas: ver seção 1.
- **Critérios:** aumentar só com semáforo verde; interromper se o teste não passar; nenhuma verba extra sem nova reunião.
- **Custo do próprio Claude (informativo):** plano Pro com uso extra e recarga automática; teto de ~R$ 100 de extra aceito até 08/11; a partir de 09/11 o dono quer só a assinatura (sem extra).

---

## 7. AUTOMAÇÕES E INTEGRAÇÕES

| Automação | Gatilho | Estado | Limite/Risco |
|---|---|---|---|
| Cron do Instagram (Claude) | Todo dia 20:39 (dispara ~21:09) | Ativo na conversa maior | Só com o app Claude aberto e o PC ligado; expira em ~7 dias (recriar ~11/11); **só UM cron** (senão duplica posts); se falhar, o dono escreve "agendar DD/MM" |
| Tarefa diária 19:12 (Status/Canal/Story) | Todo dia ~19:12 | Em **outra conversa**; validade a confirmar | Gasta cota do Claude; depende de Chrome e WhatsApp Web conectados |
| ManyChat "BLACK/LINK/QUERO" | Comentário no post fixado | LIVE | 1 post por automação (plano grátis); 2 visitas rastreadas em testes |
| Backup do blog | A cada 30 min (Windows) | Ativo | Pacote do outro PC não tem backup automático |
| Atualização de categorias | A cada 3 h (Windows) | Ativo | Para com ERRO se um anúncio chegar sem categoria |
| Convites WhatsApp | — | **Cancelada** | Risco de restrição do número |

**Testes e resultados:** link do ManyChat rastreado ok (2 visitas de teste); servidor de rastreio gravou evento de diagnóstico; verificação de 214 anúncios; painel 0 erros de fórmula. **Pendente:** teste do ManyChat com conta de terceiros; teste do `ATUALIZAR_AQUI.bat` no PC2.
**Recuperação:** backups de página do WP em `9_Manutenção_Blog\2_DADOS\Blog_WordPress\backups`; backups dos scripts do Claude em `0- Pendencias\99_Programas_PY\_backups_claude_30out`; WordPress mantém revisões.

---

## 8. ARQUIVOS, PASTAS, DOCUMENTAÇÃO E BACKUPS

**Raiz `D:\mercado_livre` (estrutura oficial; nada solto na raiz; perguntar antes de criar pasta; em Python usar barras normais):**
`0- Pendencias` (1_Pendencias, 2_Analises_Anuncios, 3_Guia_Passo_a_Passo_Instagram_2026, 4_Relatorio_Ativ_Claude_no_Blog [71 itens], 5_Plano_turbinar_anuncio_instagram, 99_Programas_PY) · `1- Gera_Relatorio` · `2-Verificar_Erros_Blog` · `3- Divugação_WhastsApp_Instagram` (grafia exata, com erro; fonte dos pacotes e geradores `_fonte`) · `4- Celular_Whatsapp` (cópia para celular; leitura do agendamento) · `5_Automação_Instagram` (plano antigo, não usar) · `6_Cartao_Comercial` · `7_Docs` · `8_Logo` · `9_Manutenção_Blog` · `10_Rastreamento_anuncios` · `11_Estrategias_Vendas` · `12_Base_Contatos_WhatsApp` · `99_Relatorios_Diarios` · `python`, `css`, `img`, `js`.

**Pacotes do dia:** `07_PACOTE_DO_DIA\<AAAA-MM-DD_dia>` com `feed.png`, `story.png`, `status.png`, `reels.mp4`, `reels_capa.jpg`, `1_TEXTOS_DO_DIA.txt`, `2_LEGENDA_REELS.txt`.
**Planilhas:** `Base_Contatos_WhatsApp.xlsx`, `checklist_execucao_30_dias.xlsx`, `Planilha_Semanal_Turbinar.xlsx`, `04_CALENDARIO_POSTS_NOV_DEZ.xlsx`, `CATALOGO_CATEGORIAS.xlsx`, `Painel de Controle de Acesso.xlsx`.
**Documentos-chave:** `nova_pendencias.pdf`, `agenda_nova_pendencias.ics`, `HANDOVER_TECNICO_001_para_000_2026-11-04.md` e o ANEXO (histórico completo até 04/11), `Guia_Socio_Como_Pedir_ao_Claude.pdf`, `Roteiro_Rotinas_Segunda_e_Sexta.pdf`, `processo_crescimento_canal_whatsapp.pdf`, `Regras_de_Uso_Base_Contatos_WhatsApp.pdf`, Plano Turbinar (PDF + quadro), `PROCESSO_DE_ATUALIZACAO_MANUTENCAO.pdf` (blog).
**Backups:** do blog (páginas, categorias, snippets), da base de contatos (`12_Base_Contatos_WhatsApp\_backups`), dos geradores, das conversas do Claude (`E:\BKP_INTEGRA_CLAUDE\BACKUPS`, 5 em rodízio + FREEZE).
**Observação:** apagar arquivos = **Lixeira do Windows**, nunca exclusão definitiva. Arquivos de contatos soltos (CSVs de origem) foram para a Lixeira em 05/11.
**Disponibilidade:** os caminhos acima foram verificados no PC do dono em 07/11 (existência das pastas principais, de `nova_pendencias.pdf`, da agenda e dos handovers). Qualquer outra IA **não terá acesso** a eles sem o dono enviar os arquivos.

---

## 9. SITUAÇÃO ATUAL E PENDÊNCIAS

Estados: Concluída e validada · Concluída sem validação · Em andamento · Planejada e aprovada · Aguardando dono · Bloqueada · Cancelada · Desconhecida.

| Atividade | Estado | Prioridade | Dependência | Próxima ação |
|---|---|---|---|---|
| Agendar Instagram até 04/12 | Concluída e validada | — | — | Manter |
| Agendar 07/12 a 23/12 | Planejada e aprovada | Alta | Janela D-29; cron/Chrome | 08/11 20:00 em diante |
| Recriar cron do Instagram | Planejada | Alta | Claude aberto | ~11/11 (expira ~12/11) |
| Reunião de replanejamento | Planejada | **Alta** | Dono | 09/11 09:00 |
| Convites do dia 06/11 | **Desconhecida** | Média | Dono avisa "enviei..." | Perguntar ao dono |
| Aprovar/ler mudanças do catálogo ("em análise") | Em andamento | Média | WhatsApp | Conferir 09/11 |
| "Comente CANAL" no ManyChat | Aguardando dono | Média | Post que peça a palavra | Quando houver o post |
| Teste do ManyChat com 2ª conta | Aguardando dono | Média | Dono | 11/11 |
| Segundo administrador do Canal | Concluída sem validação (dono diz resolvido) | Baixa | — | Confirmar |
| CNL-111 no catálogo | Concluída (apagado em 02/11; dono confirma que não existe) | — | — | — |
| Frases leves Air Fryer/LG | Concluída (02/11) | — | — | — |
| Anúncio Turbinar teste | Planejada e aprovada | Alta | Termos, destino com UTM, texto, aprovação | Rascunho 09/11; aprovação 13/11; ativação 16/11 |
| Conferir 6 itens de segurança do anúncio | Em andamento (1 e 3 feitos) | Alta | Dono escolher "agora" ou 13/11 | Faltam 2 (UTM), 4 (texto/imagem), 6 (aprovação) |
| UTM: nenhuma visita de Instagram/WhatsApp/ManyChat desde 31/10 | Em andamento | Alta | Claude | Investigar 09/11 |
| Search Console/Bing/Analytics | Em andamento | Média | Dono abre o Chrome lilás | 09/11 |
| `/presentes-de-natal/` no Search Console | Planejada | Média | — | 10/11 |
| Testar `ATUALIZAR_AQUI.bat` no PC2 | Aguardando dono | Baixa | PC2 | Sem data |
| Trocar senha "Painel Blog" se o zip saiu do PC | Concluída (dono diz que trocou; ordem em relação ao zip é incerta) | — | — | Confirmar |
| Decidir fim de agenda duplicada, relatórios antigos | Aguardando dono | Baixa | — | — |
| Arquivar a conversa antiga do Claude | Aguardando dono (fixada) | Baixa | Dono | Desafixar e arquivar |
| E-mail do site (SMTP) | Bloqueada | Baixa | Hostinger/Gmail sem senha de app | Adiado |
| Venda "em revisão" por compra própria | **Desconhecida** | Média | Dono confere os 12 pedidos | Marcar no painel |
| Publicar blog das máquinas no Google Sites | **Desconhecida** | Baixa | Dono | — |
| Envio de e-mail (campanhas) | Planejada, sem ferramenta | Baixa | Inscritos | Após a BF |

**Dependem exclusivamente do dono:** gerar links meli.la; convites à mão; ativar o anúncio e digitar dados de cartão; apagar itens do catálogo/Canal; instalar chips/WhatsApp; entrar nos serviços (senhas, QR); ManyChat no Chrome lilás; aprovar contatos "Conhecido"; aprovar textos/arte de anúncio; limpar agenda/arquivos.

---

## 10. PLANEJAMENTO FUTURO

**Próximos 7 dias (07–14/11).** (Aprovado, salvo reunião de 09/11.) Sáb 07 e dom 08: só convites e rotina do dia; 08/11 20:00 agendar 07/12. Seg 09: reunião 09:00; rodada semanal; medição; rascunho do anúncio; Colágeno (item 77). Ter 10: Natal no Search Console; agendar 09/12. Qua 11: teste do ManyChat; recriar cron. Qui 12: agendar 11/12. Sex 13: termos do ML, aprovação do anúncio, painel e links. Sáb 14: leve. **Recursos:** cota do Claude (80% usada em 06/11; zera segunda 02:00). **Resultado esperado:** anúncio aprovado e dezembro agendado.

**Próximos 30 dias (até 07/12).** Teste 16–18/11 e avaliação 19/11; BF 21–27/11 (condicional); avaliação 30/11; Natal assume o menu 01/12; agendar dezembro dia a dia; semana da BF sem tarefas extras. **Compromissos aprovados:** teste R$ 50; sem verba extra. **Sugestões não autorizadas:** Telegram e outros canais após a BF; ManyChat Pro.

**Próximos 90 dias (até início de fevereiro/2027).** Natal pago 05–14/12 (condicional); relatório final 21/12; recesso/rotina de fim de ano (não definido); **janeiro: reunião de decisão com números.** Nada mais está planejado: **desconhecido**.

**Objetivos de longo prazo:** só a decisão de janeiro com base em visitas reais, cliques e comissão; meta numérica de vendas **não definida**.

---

## 11. DECISÕES, RESTRIÇÕES E PREFERÊNCIAS DO PROPRIETÁRIO

**Permanentes**
- **Idioma:** sempre PT-BR, linguagem simples.
- **Um passo por vez.** Muitos passos juntos o confundem ("não entendi nada"). Respostas curtas; objetivas.
- **Pontualidade:** cumprir horários combinados ("pontualidade britânica"); concluir **na data marcada, sem replanejar**; se der erro, corrigir e concluir.
- **Autonomia:** resolver sozinho o que é **óbvio e sem risco** (avisar depois em uma linha); **parar e dar opções** quando houver mais de um caminho, custo ou risco; **sempre perguntar** antes de: risco de bloqueio (WhatsApp/Instagram/afiliados), apagar dados, gastar dinheiro, falar em nome do dono.
- **Segurança:** avisar logo, em todo pedido, se há risco de bloqueio ou violação de termos e propor o caminho seguro; preservar contas e números.
- **Dinheiro:** controle financeiro; teste de baixo orçamento; nada de verba extra sem reunião.
- **Segredos:** o Claude **nunca** digita senha, cartão, CPF, endereço; o dono digita.
- **Dados:** relatório PDF ao fim de cada sessão/agendamento; registro do que foi feito; **uma lista de pendências só** (`nova_pendencias.pdf`) e **uma agenda só** (`agenda_nova_pendencias.ics`); não criar outros arquivos de pendência; apagar = Lixeira.
- **Agenda do Google:** o Claude **não edita, não marca FEITO e não apaga** eventos por iniciativa própria; só cria quando pedido; o dono retira o que concluiu depois de validar na conversa.
- **Evitar duplicidade:** um só cron de agendamento do Instagram; cada rotina tem uma conversa "dona".
- **Textos de produto:** atrativos mas sem inventar dados; política da seção 5.3.
- **Uso do Claude:** fazer só o essencial; pesado fica para segunda-feira; tarefas por tela são as mais caras.
- **Rotina noturna do Instagram:** "mantém todas sem alteração" (06/11); mudanças de horário só na reunião de 09/11.

**Específicas / com validade vencida:** teste de R$ 30 (agora R$ 50); "ADIADO" do Turbinar (liberado em 05/11); sócio direcionando o Claude em tudo (03/11; reavaliar); campanha de grupos (cancelada); catálogo por produto (encerrado em 06/11); automação de convites (cancelada); plano antigo `5_Automação_Instagram` (não usar).

---

## 12. RISCOS, PROBLEMAS E LIÇÕES APRENDIDAS

| Tema | O que ocorreu / risco | Prevenção |
|---|---|---|
| Bloqueio do WhatsApp | Envio em massa e automação podem restringir o número | Só convites à mão para conhecidos, limites diários, paradas automáticas; número reserva não usado para convites |
| Conta de afiliado do ML | Compras pelo próprio link (7 recusadas = compras do dono); anúncio de busca com a marca é proibido | Nunca comprar pelo link; anúncio só em Instagram/Facebook, sem a marca; reler termos antes de ativar |
| Anúncio pago | Gastar sem resultado | Limite de R$ 50; semáforo; reuniões de avaliação |
| Numeração `#item-N` | Itens retirados deslocam links dos pacotes | Conferir âncora pelo nome (`gerenciar_blog.py listar`); links "da bio" nos posts agendados |
| Instagram | Janela de 29 dias; login derruba a rotina; legenda colada por script perde quebras de linha; coordenadas mudam com o tamanho da janela | Digitar com teclado; screenshot antes de cada clique; conferir calendário mensal |
| WhatsApp Web | ENTER envia; legenda de Status sem quebra; link ≤ 75 caracteres; Canal só o dono apaga | Uma linha; conferir antes de enviar |
| Cron do Claude | Só com app aberto; expira em 7 dias; conversas duplicadas criaram risco de dois crons | Um só; recriar ~11/11; conferir `CronList` |
| Medição | Sem UTM de Instagram/WhatsApp desde 31/10; contador do painel inclui testes; muitos acessos de robôs | Usar GA4/visitantes únicos; investigar em 09/11 |
| Anúncios do ML | Saem do ar; catálogo `/p/` cai em anúncio pausado; lista mostra parcela como preço | Painel avisa; verificar abrindo o meli.la e o preço na página |
| E-mail do site | Não chega | Configurar SMTP quando houver tempo |
| Segredos | `wp_credenciais.json` já foi parar no pacote zip em 29/10 | Pacote agora sem senha; trocar a senha de aplicativo se o zip sair |
| Arquivos compartilhados | `gerar_relatorio_atividade.py` já foi sobrescrito por conversa paralela | Reler antes de editar; só acrescentar |
| Erros do Claude já corrigidos | Foto de produto trocada nos pacotes (5 fotos), `body` pegando categoria errada, legendas enviadas soltas no Canal (6/11), edição de evento recorrente na agenda sem conferência | Regras acima |
| Custos do Claude | Uso extra ativo | Orçamento semanal; só o essencial |

---

## 13. INVENTÁRIO DE INFORMAÇÕES FALTANTES

**Confirmadas:** estrutura de pastas; política de texto; termos do ML (4.4); limites do WhatsApp; regras do Instagram; decisões do Turbinar; números do ML até 02/11; Instagram agendado até 04/12; catálogo só por categoria; número reserva ativo; formulário e GA4 no ar.
**Incompletas:** número atual de seguidores do Canal e do Instagram; resultado dos convites de 06/11 e dos dias seguintes; resultado do WhatsApp para as 9 capas novas ("em análise"); status do blog das máquinas no Google Sites; vendas após 02/11; segundo administrador do Canal; origem do tráfego após 31/10; custo real do Claude por tarefa.
**A atualizar:** `nova_pendencias.pdf` e a agenda (após a reunião de 09/11); números do painel (rodar `ATUALIZAR_PAINEL.bat`); relatório de acessos; vendas (novos prints).
**Documentos a enviar à outra IA (pelo dono):** `nova_pendencias.pdf`; `agenda_nova_pendencias.ics`; os dois HANDOVER; este relatório; `processo_crescimento_canal_whatsapp.pdf`; Plano Turbinar + quadro; guia do blog (lista de categorias); modelos de textos do `07_PACOTE_DO_DIA` de 1 dia; `Nova_Estrutura_diretorio...txt`.
**Só o dono pode esclarecer:** quem é "o sócio" e qual o papel em cada tarefa; se alguma das 12 vendas "em revisão" foi compra própria; se a cota/gasto com IA permite continuar com o Claude em paralelo ao ChatGPT; se aceitará anúncios além do teste; quais canais (Telegram etc.) depois da BF; meta de vendas; se a tarefa das 19:12 continua; qual é a conta Google/ML correta para cada serviço.

---

## 14. INSTRUÇÕES DE TRANSFERÊNCIA PARA O CHATGPT PLUS

**1. Visão geral.** Blog de afiliados do Mercado Livre (comprenolink.net) + Instagram + Canal e catálogo no WhatsApp Business + um teste pequeno de anúncio no Instagram. Dono único operando; foco em **segurança de conta e de número** antes de crescimento.

**2. Arquitetura.** Blog WordPress/Hostinger com scripts Python locais; Instagram agendado pelo navegador; WhatsApp Web/Business; ManyChat grátis; GA4/Search Console/Bing; painel Excel; geradores de PDF. **Atenção:** o Claude operava **no PC do dono** (arquivos locais, Excel, Chrome com extensão, tarefas agendadas). **Verifique o que o ChatGPT Plus consegue fazer:** provavelmente não tem acesso direto ao PC nem ao Chrome do dono. Sem isso, ele precisará **guiar o dono passo a passo**, escrever textos e scripts para o dono rodar, e analisar prints.

**3. Estado real.** Blog: no ar (214 anúncios). Instagram: agendado até 04/12. WhatsApp: Canal ativo, catálogo por categoria, número reserva ativo, base de 500 contatos com 24 aprovados. ManyChat: 1 automação. Anúncio pago: conta criada, nada rodando. Vendas: baixas. Tráfego: ainda pequeno e sem UTM de rede social registrado.

**4. Agenda.** Seção 4, **a confirmar após a reunião de 09/11 09:00**.

**5. Últimas atividades comprovadas.** 04/12 agendado (05/11 21:09, conferido no calendário); documentos do Turbinar corrigidos; termos do ML lidos (05 e 06/11); conta Meta com R$ 0,00 e limite R$ 50 (06/11); catálogo só com as 9 categorias (06/11); segundo número ativo (06/11); medição lida (06/11).

**6. Pendências prioritárias.** (1) Reunião de 09/11; (2) agendar 07/12 (08/11 20:00) e os demais; (3) recriar o agendamento diário (~11/11) ou assumir o fluxo com o dono; (4) rascunho do anúncio para aprovação (13/11); (5) investigar a ausência de UTM; (6) registrar os convites do dono.

**7. Próxima atividade recomendada.** Antes de qualquer outra coisa: **ler `nova_pendencias.pdf`, esta seção e a seção 4; perguntar ao dono o que mudou na reunião de 09/11 e se ele confirma a divisão de trabalho com o ChatGPT.** Depois, 08/11 20:00: agendar 07/12.

**8. Exigem autorização do dono:** qualquer gasto (anúncio, ferramenta paga); anúncio ativo; envio de mensagens/convites; apagar dados ou itens; mudar bio/links/catálogo; incluir contatos na fila; criar/alterar eventos da agenda; criar arquivos novos fora da estrutura; qualquer coisa que possa causar bloqueio ou violar termos.

**9. Para não repetir trabalho.** Conferir antes de agir: calendário do Instagram (já agendado?), pacote do dia, `nova_pendencias.pdf`, relatório mais recente em `4_Relatorio_Ativ_Claude_no_Blog`, memória/histórico do `HANDOVER ANEXO` (114 entradas). Itens **concluídos e não repetir:** substituição dos 3 anúncios (02/11) e dos 3 de 06/11; CNL-111; frases leves; fotos trocadas (02/11); documentos do Turbinar; limpeza de agenda/CSVs.

**10. Confirmar antes de executar:** quem faz o quê (ChatGPT × Claude × dono) e **quem fica dono do agendamento diário** (nunca dois ao mesmo tempo); estado atual do Canal e dos convites; se a reunião de 09/11 mudou horários; se os limites de gasto do anúncio continuam; qual perfil do Chrome tem cada serviço.

**Regras de ouro finais:** português simples, um passo por vez; segurança antes de velocidade; nunca inventar métricas; nunca pedir senha ao dono em texto; nunca enviar mensagens em massa; sempre registrar o que foi feito e conferir o resultado.
