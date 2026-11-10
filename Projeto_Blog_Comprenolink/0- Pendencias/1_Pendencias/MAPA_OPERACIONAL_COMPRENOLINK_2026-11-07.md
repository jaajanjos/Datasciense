# MAPA OPERACIONAL DO COMPRENOLINK
Diagnóstico de 07/11/2026 (sábado, tarde). Autor: Claude. Finalidade: documentar e compreender a operação existente para a avaliação de continuidade com o ChatGPT.
**Este documento é um diagnóstico. Não é uma lista de pendências nem uma agenda.** A lista de pendências vigente continua sendo `nova_pendencias.pdf`; a agenda continua sendo `agenda_nova_pendencias.ics`.

## 0. Como este mapa foi feito e seus limites
- **Fontes consultadas:** `RELATORIO_MESTRE_CONTINUIDADE_COMPRENOLINK_2026-11-07.md`; os dois `HANDOVER_TECNICO_001_para_000_*` de 04/11 (lidos por inteiro o principal e até o fim do histórico o anexo); `agenda_nova_pendencias.ics` (títulos e datas de todos os eventos); o gerador `gerar_nova_pendencias.py` (ver aviso abaixo); anotações de memória do Claude; tarefas agendadas do Windows, tarefas agendadas do Claude, logs e listas de pastas.
- **Aviso sobre `nova_pendencias.pdf`:** o leitor de PDF do Claude **não funcionou neste computador** (falta o programa `pdftoppm`). Por isso o conteúdo foi lido **pelo gerador** (`Programas_Diversos_Py\gerar_nova_pendencias.py`), que tem o texto da versão de 04/11 com as correções de 05 e 06/11. O PDF em si é de 06/11/2026 09:11. **Pode haver diferença entre o gerador e o PDF**: não foi comparado.
- **O que foi executado:** somente leitura (listar pastas, ler arquivos e logs, consultar o Agendador de Tarefas do Windows e as tarefas do Claude). **Nenhum programa do projeto foi executado, nada foi alterado, movido, apagado, publicado ou agendado.** A única criação é este arquivo.
- **Sem segredos:** nenhuma senha, token, cookie, código ou conteúdo de arquivo de credencial aparece aqui. Só o **método** de autenticação e a **localização** das configurações.
- **Níveis de evidência usados:** **[V]** = verificado hoje (07/11/2026) neste mapa; **[R]** = registro anterior (memória, relatório, handover), com data; **[N]** = não verificado.
- **Correções encontradas em documentos anteriores (originais não alterados):** (a) o `RELATORIO_MESTRE` cita `Nova_Estrutura_diretorio_Mercado0_Livre.txt` como fonte da estrutura; esse nome **não existe mais na raiz**; o arquivo vigente é `D:\Projeto_Blog_Comprenolink\Estrutura_diretorio_Projeto_Blog_Comprenolink.txt` [V, gerado 07/11 17:10]. (b) O `RELATORIO_MESTRE` diz que o guia tem ~214 produtos; o log de hoje registra **213 produtos** (`atualizar_categorias.log`, 07/11 16:08) [V].
- **Contexto de governança (pedido do dono):** o Claude continua responsável pela operação até a avaliação GO/NO-GO de **13/11/2026**; a possível transferência começa em **16/11/2026**, só com aprovação; a reunião de replanejamento de **09/11/2026** pode atualizar o plano.

---

## 1. Visão geral das pastas de `D:\Projeto_Blog_Comprenolink`
Fonte da listagem: `Estrutura_diretorio_Projeto_Blog_Comprenolink.txt` + listas de pasta de hoje [V].

| Pasta | Finalidade | Uso atual |
|---|---|---|
| `0- Pendencias\1_Pendencias` | Documentos que o dono usa para operar: pendências, agenda, handovers, rotinas, guia do sócio, planilha semanal, relatório mestre, este mapa | **Em uso** [V] |
| `0- Pendencias\2_Analises_Anuncios` | Análise crítica de anúncios (27/10) e CSVs de sugestões de 30/10 | Referência; consulta [V existe; uso atual: N] |
| `0- Pendencias\3_Guia_Passo_a_Passo_Instagram_2026` | PDF do guia do Instagram (regerado 05/11) | Consulta [V] |
| `0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog` | PDFs diários de atividades do Claude (19 arquivos de 29/10 a 07/11) | **Em uso**: gerado a cada sessão [V] |
| `0- Pendencias\5_Plano_turbinar_anuncio_instagram` | Geradores do Plano Turbinar (PDF e quadro) | Consulta; decisão de 05/11 já aplicada nos geradores [R] |
| `Programas_Diversos_Py` | **Scripts do Claude** que geram PDFs, agendas, relatório e textos; `_backups_claude_` guarda cópias antes de cada mudança | **Em uso** [V] |
| `0- Pendencias\bkp_drp` | Histórico/backlog do que saiu do `nova_pendencias.pdf` (04/11) | Histórico [R] |
| `Relatorios_Diarios_Anuncios\programas_fontes_python` | 4 programas `.exe` (relatório de acessos, links, relatório SEO do blog, teste SEO) + `config_rastreio.json` + `dados_acessos` | **Em uso** (manual) [R + V existe] |
| `Planejamentos\Andamento\Verificar_Erros_Blog` | `testar_site_de_novo.bat`, `robots.txt`, `security_top.txt` | Em uso manual quando se testa o site [R] |
| `Planejamentos\Andamento\Divugação_WhastsApp_Instagram` (grafia exata, com erro) | **Fonte** da divulgação: guia, checklists, textos, calendário `04_CALENDARIO_POSTS_NOV_DEZ.xlsx`, links, catálogo, **`07_PACOTE_DO_DIA` (34 pastas de dia)**, logo, post de boas-vindas, respostas salvas, `_fonte` (geradores), `_backup_pacotes` | **Em uso** [V] |
| `Planejamentos\Andamento\Celular_Whatsapp` | **Cópia** da pasta 3 para uso no celular e **origem dos arquivos que o agendamento do Instagram lê** (copiados para pasta temporária antes do envio). Inclui `12_CANAL_CONVITE`, `old- Celular_Whatsapp`, `relatorio_atividade_tecnicas_executas_Whatsapp.md` (relatório técnico de outro PC/sessão, 30/10) | **Em uso** [V] |
| `Planejamentos\Andamento\Automação_Instagram` | Plano orgânico inicial (29/09): calendário e artes com preços | **Não vigente segundo registro de 26/10** ("usa preços, NÃO usar") [R]; conteúdo não reverificado hoje |
| `Cartao_Comercial` | Cartões A4 (colorido, preto e branco) e geradores | Material gráfico; uso atual: N [V existe] |
| `Planejamentos\Hold\Dados_Tiktok` | Checklist Turbinar Vendas (PDF), `Dados_Tiktok`, `Processo_1_Afiliados_ME`, scripts de PDFs, relatórios de teste do site | Referência [V existe] |
| `Logo` | Logotipos (perfil, horizontal, ícone) e vídeos TikTok | Referência; TikTok descartado em 03/11 [R] |
| `Gestao_Anuncios_Blog` | **Programas e dados do blog WordPress** (`1_PROGRAMAS`, `2_DADOS`, `3_DOCUMENTACAO`), pacote para outro PC (`4_PACOTE_OUTRO_PC*.zip`), atalhos `.bat`, `CentralBlog.exe`, PDF do processo de atualização, esboço de categorias, `9_ORIGINAIS_NAO_MEXER` | **Em uso** [V] |
| `Planejamentos\Andamento\Rastreamento_anuncios` | Rastreador UTM original (snippet PHP, `.exe` antigos, `links_anuncios.csv/html`) | Origem do rastreio; uso atual: N [V existe] |
| `11_Estrategias_Vendas` | 1 PDF: estratégia de retorno de 6 meses a 1 ano | Referência [V existe] |
| `Planejamentos\Andamento\Base_Contatos_WhatsApp` | Base de contatos com consentimento (`Base_Contatos_WhatsApp.xlsx`), regras, checklist de 30 dias, processo, agenda, `_fonte`, `_backups`, `IMPORTAR_NO_CELULAR` | **Em uso** [V]. **Contém dados pessoais: não enviar a nenhuma IA** |
| `Relatorios_Diarios_Anuncios` | **Painel de métricas**: `ATUALIZAR_PAINEL.bat`, `Painel de  Controle de Acesso.xlsx`, PDFs do painel (03, 04 e 05/11), `vendas_afiliados`, `vendas_historico`, `anuncios_status`, `historico_consolidado`, `_historico_relatorios`, `_backup_painel`, `log_painel.txt` | **Em uso** [V] |
| `python` | Fontes dos programas do painel e do rastreio (`2_`, `3_`, `4_atualizar_painel_controle.py`, `5_..ps1`, `6_verificar_anuncios.py`, `7_limpar_historico.py`, `8_rodar_com_log.ps1`) | **Em uso** (código-fonte) [V] |
| `css`, `img`, `js` | Recursos do site; uso atual: N | [V existe] |
| Raiz | Só 3 arquivos: `.gitignore`, `Gera_Estrutura_Diretorio.bat` e a listagem `Estrutura_diretorio_..._Claude.txt` | [V] |

**Observações de pastas [V hoje]:** não existe mais `99_Log_Relatorios (pasta antiga; hoje Relatorios_Diarios_Anuncios)` (citada em registros antigos). Existe um arquivo de bloqueio do Excel `99_Relatorios_Diarios (pasta antiga; hoje Relatorios_Diarios_Anuncios)\~$Painel de  Controle de Acesso.xlsx` com data de **31/10 16:02** e 165 bytes: pode ser sobra de um Excel que fechou mal ou um Excel aberto; **não verificado**. Se o Excel estiver aberto, o `ATUALIZAR_PAINEL.bat` pode falhar [R: handover §6].

---

## 2. Fontes oficiais (versão vigente)
**Critério:** "vigente" = indicado como oficial em registro do dono/Claude com data, ou gerado por programa e confirmado hoje. Nada foi marcado como obsoleto sem evidência.

| Tema | Arquivo vigente (caminho exato) | Tipo | Evidência |
|---|---|---|---|
| **Pendências** | `D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\nova_pendencias.pdf` | **Gerado** por `Programas_Diversos_Py\gerar_nova_pendencias.py` (editar o gerador, não o PDF) | [R] regra do dono 03/11: "único arquivo de pendências"; PDF de 06/11 09:11 [V] |
| **Agenda** | `D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\agenda_nova_pendencias.ics` | **Gerado** por `Programas_Diversos_Py\gerar_agenda_nova_pendencias.py`; importado no Google Agenda | [R] regra 03/11 "agenda única"; arquivo de 06/11 18:29 com 68 eventos [V]; **o Google Agenda não foi comparado hoje** |
| **Produtos e links de afiliado (guia)** | **No WordPress**, página `https://comprenolink.net/melhores-produtos-mercado-livre-2026/` (page id 5). Cada item = bloco do plugin de afiliado com link `meli.la` | **Original ao vivo** (fonte primária é o site) | [R] 21/10 e 23/10; 213 produtos [V no log de 07/11] |
| Cópias dos produtos/links | `Gestao_Anuncios_Blog\2_DADOS\Blog_WordPress\backups\` (páginas `.html/.json`) e `...\backups\automatico\`; `Planejamentos\Andamento\Rastreamento_anuncios\links_anuncios.csv`; `Relatorios_Diarios_Anuncios\anuncios_status\historico_status_anuncios.csv` | **Backups/históricos** (não editar) | [R]; backups mais recentes de 06/11 [V] |
| **Categorias** | `Gestao_Anuncios_Blog\2_DADOS\Blog_WordPress\categorias.json` (palavras por categoria, tags BF/Natal, textos de campanha) e `paginas_categorias.json` (ids das páginas) | **Original editável** (o site é gerado a partir dele: editar o WP direto é desfeito) | [R] 03/11; arquivos existem [V] |
| Estado das categorias | `...\2_DADOS\Blog_WordPress\atualizar_categorias_estado.json` e `atualizar_categorias.log` | **Gerados** | [V] log até 07/11 16:08 |
| **Contatos** | `D:\Projeto_Blog_Comprenolink\12_Base_Contatos_WhatsApp (pasta antiga; hoje Planejamentos\Andamento\Base_Contatos_WhatsApp)\Base_Contatos_WhatsApp.xlsx` (aba Base; Reserva removida em 05/11) | **Original**; **dados pessoais** | [R] 04–06/11; existe [V] |
| Regras/processo de contatos | `Planejamentos\Andamento\Base_Contatos_WhatsApp\processo_crescimento_canal_whatsapp.pdf`, `Regras_de_Uso_Base_Contatos_WhatsApp.pdf`, `regras_execução.pdf`, `guia_utilização_gerador_excel.pdf`, `checklist_execucao_30_dias.xlsx`, `agenda_crescimento_canal_whatsapp.ics` | Originais/gerados (v2 de 04/11) | [R]; existem [V] |
| Cópia para celular dos contatos | `Planejamentos\Andamento\Base_Contatos_WhatsApp\IMPORTAR_NO_CELULAR\` | **Cópia gerada** (`.vcf`, `_GOOGLE.csv`); pessoal | [R] 06/11 |
| Backups da base | `Planejamentos\Andamento\Base_Contatos_WhatsApp\_backups\` (16 itens; mais recente: `..._antes_registrar_envios_06-11_101055.xlsx`) | **Backups** | [V] |
| **Campanhas (conteúdo diário)** | `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Divugação_WhastsApp_Instagram\07_PACOTE_DO_DIA\<AAAA-MM-DD_dia>\` (34 pastas) com `feed.png`, `story.png`, `status.png`, `reels.mp4`, `reels_capa.jpg`, `1_TEXTOS_DO_DIA.txt`, `2_LEGENDA_REELS.txt` | **Original/gerado** (geradores em `Planejamentos\Andamento\Divugação_WhastsApp_Instagram\_fonte`) | [V 34 pastas] |
| Cópia para celular e para o agendamento | `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Celular_Whatsapp\07_PACOTE_DO_DIA\` | **Cópia** (script `_fonte\sincronizar_copias.py`) | [R]; a agenda do Instagram lê daqui [R] |
| Backups de pacotes | `Planejamentos\Andamento\Divugação_WhastsApp_Instagram\_backup_pacotes\` | **Backups** | [R] |
| Plano de postagens e marcação "Feito" | `Planejamentos\Andamento\Divugação_WhastsApp_Instagram\04_CALENDARIO_POSTS_NOV_DEZ.xlsx` | **Original** (Feito=S não é sobrescrito) | [R] |
| Catálogo do WhatsApp (categorias) | `Planejamentos\Andamento\Divugação_WhastsApp_Instagram\06_CATALOGO_WHATSAPP\CATEGORIAS\` (fotos, textos, `CATALOGO_CATEGORIAS.xlsx`, capas novas 06/11) | **Original**; estado real está no app do WhatsApp | [R] política de 06/11 |
| Campanha paga (Turbinar) | `0- Pendencias\5_Plano_turbinar_anuncio_instagram\` (geradores) e a seção "Turbinar" do `nova_pendencias.pdf`/agenda | Gerados | [R] decisão 05/11 |
| **Métricas** | `Relatorios_Diarios_Anuncios\Painel de  Controle de Acesso.xlsx` + PDFs `Painel_conversao_performance_*.pdf` (último: 05/11 10h05) | **Gerados** por `ATUALIZAR_PAINEL.bat` | [V] log: última execução 05/11 10:06, saída 0 |
| Vendas | `Relatorios_Diarios_Anuncios\vendas_afiliados\vendas_ml_2026-10-31.csv` (entrada) e `vendas_historico\historico_vendas.csv` (consolidado, 05/11 10:05) | Entrada manual + gerado | [V] **último CSV de vendas é de 31/10** |
| Métricas externas | Google Analytics 4 e Search Console (Chrome lilás); Bing Webmaster (Chrome José Antônio); ML Afiliados (painel do dono) | **Serviços externos** | [R] 06/11 |
| Relatórios de atividade | `0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog\*.pdf` e gerador `Programas_Diversos_Py\gerar_relatorio_atividade.py` | Gerados | [V] |
| Estrutura de pastas | `D:\Projeto_Blog_Comprenolink\Estrutura_diretorio_Projeto_Blog_Comprenolink.txt` | **Gerado** por `Gera_Estrutura_Diretorio.bat` | [V] 07/11 17:10 |
| Handovers | `0- Pendencias\1_Pendencias\HANDOVER_TECNICO_001_para_000_2026-11-04.md` e `..._ANEXO_historico_e_pendencias_2026-11-04.md` | **Originais** (retrato de 04/11) | [V] |
| Relatório mestre | `0- Pendencias\1_Pendencias\RELATORIO_MESTRE_CONTINUIDADE_COMPRENOLINK_2026-11-07.md` | Original (retrato de 07/11) | [V] |

**Sobre arquivos "históricos" ou "possivelmente superados" (sem classificar como obsoleto):** vários `.py` de pendências antigas em `Programas_Diversos_Py` (`gerar_cronograma_pendencias.py`, `gerar_pendencias_detalhado.py`, `gerar_pendencias_whatsapp.py`, `gerar_pendencias_dono_31out.py`, `gerar_agenda_novas_atividades.py`, `gerar_agenda_replanejamento.py`): o registro de 03/11 diz que os PDFs/agendas antigos foram para a Lixeira e que **o dono quer um só arquivo de pendências e uma só agenda**. Os geradores continuam na pasta. **Evidência de que ainda são usados: nenhuma**; evidência de que são obsoletos: **nenhuma**. `gerar_pendencias_detalhado.py` é importado por `gerar_nova_pendencias.py` (usa seus componentes visuais) [V no código], portanto **não pode ser removido**.

---

## 3. Rotinas em uso
Mecanismos existentes: **(M)** manual, **(W)** Agendador de Tarefas do Windows, **(CC)** tarefa agendada do Claude Desktop, **(CR)** cron de sessão do Claude (existe só enquanto a conversa estiver aberta).

| # | Rotina | Resp. | Frequência | Entrada (programa/comando) | Lê | Gera | Dependências | Como confirmar |
|---|---|---|---|---|---|---|---|---|
| 1 | **Agendar post e Reels do próximo dia de dezembro** | Claude | Todo dia ~21:09 quando a janela de 29 dias abriu | **(CR)** cron "20:39" na conversa maior (recriado em 06/11 [R]; **não verificado hoje que existe um só**) | `Planejamentos\Andamento\Celular_Whatsapp\07_PACOTE_DO_DIA\<dia>\` (copia `feed.png` e `reels.mp4` e `2_LEGENDA_REELS.txt` para pasta temporária) | Itens agendados no Instagram | App Claude aberto; PC ligado; Chrome "José Antônio" com extensão Claude e Instagram logado; expira ~7 dias | Calendário **mensal** de `instagram.com/scheduled_content` mostra 19:00 e 19:05; **falha**: tela de login, "Escolha uma data dentro dos próximos 29 dias", Chrome desconectado, app fechado |
| 2 | **Divulgação do dia: Status + Canal (e Story se faltar)** | Claude | Todo dia 19:12 | **(CC)** `divulgacao-diaria-whatsapp-story` [V]: cron `12 19 * * *`, ativa, última execução 06/11 19:14, próxima 07/11 19:14 | Pacote do dia, `1_TEXTOS_DO_DIA.txt`, calendário xlsx | Status e Canal publicados, marca Feito no calendário, atualiza relatório | App Claude aberto; Chrome com WhatsApp Web conectado (QR do dono) e Meta Business Suite; consome a cota do plano | Status/Canal visíveis no WhatsApp; relatório do dia; **falha** conhecida: ENTER envia mensagem solta; sessão do WhatsApp Web expirada |
| 3 | **Backup automático do blog** | Windows | A cada 30 min | **(W)** "Backup automatico blog comprenolink": `pythonw.exe -X utf8 ...\Gestao_Anuncios_Blog\1_PROGRAMAS\Blog_WordPress\backup_automatico.py` [V] | Site ao vivo (REST do WordPress) | Salva guia (id 5), Início (id 14), páginas e menu em `...\2_DADOS\Blog_WordPress\backups\automatico\` **só quando `modified` muda**; mantém 200 por página [R] | Internet; site no ar; senha de aplicativo em `wp_credenciais.json` | Agendador: última execução 07/11 16:55, resultado 0 [V]; `backup_automatico.log`. **Falhas registradas: 04/11 18:25, 05/11 11:55 e 15:55, 06/11 21:25 ("sem conexão com o site: getaddrinfo failed", erro de DNS)** [V] |
| 4 | **Atualizar categorias/campanhas** | Windows | A cada 3 h | **(W)** "Atualizar categorias blog comprenolink": `pythonw.exe -X utf8 ...\atualizar_categorias_auto.py` [V] | Guia ao vivo, `categorias.json`, estado | Republica páginas de categoria, Black Friday, Natal, menu, Início, aquece o cache; log | Internet; WordPress; senha de aplicativo; todo anúncio com categoria | Agendador: última 07/11 16:08, resultado 0; `atualizar_categorias.log`: "sem mudanças (213 produtos, destaque=black-friday\|natal_no_ar=True)" [V]. **Falha:** 06/11 22:09 (DNS) [V]; para com ERRO se algum item chegar sem categoria [R] |
| 5 | **Painel de métricas** | Dono/Claude | Segunda (semanal) e sob demanda | **(M)** `Relatorios_Diarios_Anuncios\ATUALIZAR_PAINEL.bat` (~10 min, 66 s na última) | Relatórios de acesso `.html`, vendas CSV, `6_verificar_anuncios.py` | `.xlsx` e PDF do painel, histórico, quadros "Anúncios fora do ar" | Excel **fechado**; internet; ML (verificação sem login) | `log_painel.txt`: última execução **05/11 10:06, saída 0** [V]; `.xlsx` sem erro de fórmula [R] |
| 6 | **Relatório de acessos** | Dono/Claude | Antes do painel | **(M)** `Relatorios_Diarios_Anuncios\programas_fontes_python\1_relatorio_acessos_anuncios.exe` | Servidor de rastreio do blog (snippet WP), `config_rastreio.json` | `relatorio_acessos_anuncios_*.html` em `Relatorios_Diarios_Anuncios\_historico_relatorios` | Snippet WP ativo; internet | HTML novo na pasta; [R] 02/11 |
| 7 | **Vendas do ML Afiliados** | Dono + Claude | Segunda 10:15 | **(M)** prints do dono → Claude monta `vendas_ml_AAAA-MM-DD.csv` → painel | Prints | CSV em `vendas_afiliados` | Dono logado no ML Afiliados | `historico_vendas.csv` atualizado; **último CSV 31/10 [V]** |
| 8 | **Editar produtos, links e textos do guia** | Claude (dono gera o link) | Quase todo dia em outubro; sob demanda | **(M)** `python gerenciar_blog.py editar N ... [--aplicar]` | Guia ao vivo, senha de aplicativo | Página publicada + backup | Internet; WordPress; Hostinger | `ultimo_diff.txt` (prévia); backup novo na pasta `backups`; conferir o site ao vivo |
| 9 | **Republicar categorias à mão** | Claude | Depois de mudar itens | **(M)** `python publicar_categorias.py --publicar` | `categorias.json` | Páginas, menu, Escolha rápida, Início | idem | Resposta do script; site ao vivo |
| 10 | **Gerar pacotes do dia** | Claude | Quando o produto/texto muda | **(M)** `Planejamentos\Andamento\Divugação_WhastsApp_Instagram\_fonte\gerar_artes_catalogo.py`, `gerar_reels.py` (ffmpeg), `sincronizar_copias.py` | Blog ao vivo, `dados_divulgacao.py`, cache de fotos | `feed/story/status.png`, `reels.mp4`, textos; cópia para pasta 4 | Internet; ffmpeg | Pastas atualizadas; conferência visual |
| 11 | **Pendências e agenda** | Claude | Quando o plano muda | **(M)** `gerar_nova_pendencias.py` e `gerar_agenda_nova_pendencias.py` (editar os dois e regerar) | Texto dos geradores | `nova_pendencias.pdf` e `agenda_nova_pendencias.ics` | ReportLab | PDF/ICS novos; importar o ICS no Google Agenda (**só com pedido**) |
| 12 | **Relatório de atividades** | Claude | Ao fim de cada sessão/agendamento | **(M)** `gerar_relatorio_atividade.py` (listas `ATIVIDADES`, `FALTA_AGENDAR`, `REEXECUCAO`) | O próprio script | `RELATORIO_ATIVIDADE_CLAUDE_BLOG_DD_MM_AAAA_HHhMM.pdf` | Arquivo compartilhado: já foi sobrescrito por outra conversa | PDF novo em `4_Relatorio_Ativ_Claude_no_Blog` |
| 13 | **Base de contatos / convites** | Dono (envia) + Claude (registra) | Dias úteis, 10:00 | **(M)** planilha aba Hoje; `importar_leads_formulario.py` (simula; `--gravar` só com Excel fechado) | Base, formulário do blog | Atualização da base | Excel fechado | Dono escreve "enviei..."; backup em `_backups` |
| 14 | **Backup das conversas do Claude** | Dono | Aproximadamente diário à noite (histórico: 04/11 20:21 e 21:24, 05/11 21:20, 06/11 22:02) | `E:\BKP_INTEGRA_CLAUDE\PRG_EXE\BACKUP_CLAUDE.exe` | Conversas do Claude | `BACKUPS\BKP_CLAUDE_*.zip` (rodízio de 5) + `FREEZE\` | Disco E: | `historico_backups.txt`: "falhas: 0" [V]. **Se é manual ou agendado: não verificado** |
| 15 | **Rodada semanal** | Dono + Claude | Segunda 10:00 | Agenda (eventos "[6]" e outros) | — | Decisões e relatório | — | Anotado na conversa; **o dono retira o evento da agenda** [R] |
| 16 | **Tarefas do Windows do sistema** (MareBackup, Backup...) | Windows | — | **(W)** | — | — | — | **Não são do projeto** [V]: só aparecem no filtro; são serviços do próprio Windows |

**Lacunas das rotinas:** não há alarme que avise o dono quando o item 3 ou 4 falha por DNS (só os logs); o item 1 depende de o cron existir (**não verificado**); o item 14 não tem registro de como dispara.

---

## 4. Dependências externas

| Dependência | O que depende dela | Efeito se faltar |
|---|---|---|
| **Computador ligado (PC "Svr_Ryzen", plano de energia sem suspensão na tomada [R 30/10])** | Tarefas do Windows (3 e 4), painel, geradores, agendamento do Claude | Backups e republicação param; o item 1 e 2 não rodam |
| **App Claude aberto** | Cron de sessão (item 1) e tarefa do Claude (item 2) | Não disparam; o cron se perde se o app fechar; o dono escreve "agendar DD/MM" |
| **Cota do plano do Claude** | Itens 1, 2, 8–12 | Acima de ~70% só o essencial (regra de sexta 12:00); **plano 80% em 06/11, renova segunda 02:00** [R] |
| **Chrome autenticado (perfil José Antônio)** com **extensão Claude conectada** | Instagram web (agendar), WhatsApp Web, Meta Business Suite, Google Agenda, Bing | Sem login/extensão o Claude **para** (nunca digita senha) |
| **Chrome lilás (perfil "comprenolink")** | ManyChat, Gmail do blog, Analytics, Search Console | O Claude **não opera** nele (sem extensão); só **vê a tela** com `computer-use` e guia o dono |
| **Internet/DNS** | Tarefas 3 e 4, painel, geradores com fotos ao vivo | Falhas de DNS já ocorreram (4 vezes no backup, 1 no de categorias) [V] |
| **WordPress / Hostinger** | Guia, categorias, formulário, backups via REST | Sem acesso, nada publica. **Hostinger: backups da hospedagem não estão registrados** [N] |
| **Mercado Livre** | Verificação de anúncios (sem login), conferência de meli.la, painel de afiliados (dono logado) | Captcha e API com token bloqueiam automações; o dono gera os links |
| **Instagram** | Agendamento (limite de 29 dias), Story com link (Business Suite) | Janela abre ~20:00 em D-29; sem login para |
| **WhatsApp** | Status, Canal e catálogo via WhatsApp Web | Exige **QR do dono**; ENTER envia; Status sem quebra de linha; campo link ≤ 75 caracteres |
| **Meta (anúncios)** | Teste de R$ 50 | Conta criada; nada rodando [R 06/11] |
| **Sincronização de arquivos** | Cópia pasta 3 → pasta 4; `E:\OneDrive\Downloads\Divulgacao_Blog` (cópia para o celular); suposta sincronização com outro PC ("lenovo") | Em 31/10 o gerador de relatório "voltou a uma versão antiga" e o dono vai conferir se há sincronização (agenda 12/11). **Estado atual: não verificado** [R] |
| **Outro computador (PC2)** | Pacote do painel do blog (`4_ATUALIZAR_OUTRO_PC.zip`) | Atualização a testar [R] |

---

## 5. Acesso do Claude (capacidades × funções dos scripts)

### 5.1 O que o Claude consegue fazer, por ferramenta
| Necessidade | Ferramenta do Claude | Observações |
|---|---|---|
| **Ler/gravar arquivos locais** | Ler, Escrever, Editar, Glob (buscar nomes), Grep (buscar texto) | Acesso às pastas autorizadas da sessão; escrever em pastas oficiais; leitura de PDF **depende de `pdftoppm`** (hoje não funciona) |
| **Executar programas** | Bash e PowerShell (rodar `.py`, `.bat`, Excel via COM, ReportLab, ffmpeg) | Pode rodar qualquer programa do projeto; scripts exigem `python -X utf8`; `.bat` com `< nul` mostra aviso inofensivo |
| **Controlar o Chrome** | **Extensão "Claude in Chrome"** (navegar, clicar, digitar, ler página, executar JavaScript, enviar arquivo) | **Só no perfil José Antônio** (deviceId `43dc6650-...`); upload só de pastas liberadas (usa pasta temporária da sessão); não digita senha; não resolve captcha |
| Ver a tela do computador | `computer-use` (captura de tela; Chrome em modo **leitura**: sem cliques) | Usado para guiar o dono no Chrome lilás |
| Navegador interno | Painel de navegador do app Claude | Perfil separado do Chrome do dono |
| **Agendar** | Cron de sessão (some ao fechar a conversa, expira ~7 dias) e tarefas agendadas do Claude Desktop (persistem, mas só com o app aberto) | Não substituem o Agendador do Windows |
| Falar com outras conversas | Mensagens entre sessões; listar/renomear/arquivar sessões | Usado em 07/11 |
| Pesquisar na internet | Busca na web e leitura de páginas públicas | Usado para os termos do ML (página oficial) |
| Enviar arquivo ao dono | Envio de arquivo (anexo) | — |

### 5.2 O que **scripts e serviços** fazem sem o Claude
- **Windows:** backup do blog (30 min) e atualização de categorias (3 h) [V].
- **Scripts manuais** (dono ou Claude disparam): painel, relatório de acessos, `gerenciar_blog.py`, `publicar_categorias.py`, geradores de pacotes, geradores de PDF/agenda, backup de conversas.
- **Plugins/serviços no site:** plugin de afiliado (preenche título/foto ao vivo do ML), Code Snippets (rastreio, cache, redirecionamento), Site Kit/GA4, AIOSEO, Fluent Forms.
- **ManyChat:** responde sozinho a comentários (BLACK, LINK, QUERO) no post fixado [R].
- **Instagram/WhatsApp:** publicam sozinhos o que foi agendado.

### 5.3 O que o Claude **não** faz (regras)
Não digita senhas, cartões, códigos; não resolve captcha nem aceita termos; não envia mensagens em massa; não apaga itens do catálogo/Canal; não edita/apaga eventos da agenda por iniciativa; só cria arquivo fora da estrutura com pergunta; apagar arquivos = Lixeira [R].

---

## 6. Manutenção do blog: fluxo completo (troca de produto ou link)
Fonte: handover §4, memória do blog e `substituicao-anuncios-ml` [R], com os caminhos conferidos hoje [V].

**Ordem das operações**
1. **Detectar** anúncio fora do ar: painel (`ATUALIZAR_PAINEL.bat` → quadros "Anúncios fora do ar" e "Substituição") ou aviso do dono.
2. **Escolher o substituto** (critérios: MercadoLíder/verde › Full › frete grátis › devolução grátis › garantia › nota ≥ 4,5 › preço ±20%; ler o **preço na página do produto**, não na lista; descartar "Internacional/Envio dos EUA").
3. **O dono gera o link** `meli.la` no ML Afiliados (Compartilhar → Gerar link). Link de catálogo `/p/MLB...` devolve sempre o mesmo meli.la; usar outro produto ou anúncio `/up/MLBU...`.
4. **Verificar o link:** abrir o meli.la e ler o primeiro cartão da página: tem de mostrar o produto novo, sem "Anúncio pausado".
5. **Prévia da edição:** `python gerenciar_blog.py editar N --link ... --nome ... --titulo-anuncio ... --imagem ... --desc ... --beneficios "a|b|c|d"` **sem** `--aplicar` mostra o diff e grava `...\2_DADOS\Blog_WordPress\ultimo_diff.txt`.
6. **Aplicar:** repetir com `--aplicar`. O programa **faz backup antes** (`pagina_AAAA-MM-DD_HHhMMSS.html/.json` em `...\backups\`) e publica pela REST do WordPress.
7. **Republicar páginas derivadas:** `python publicar_categorias.py --publicar` (categorias, Black Friday, Natal, Escolha rápida, Início, menu; com backup e aquecimento de cache). A tarefa do Windows de 3 em 3 horas também republica se o guia mudou.
8. **Conferir o site ao vivo** (HTML renderizado; o título do cartão é lido ao vivo do ML pelo plugin, então **não** confiar só no JSON do bloco). Para cache usar `?nc=` (`?m=` dá 404).
9. **Conferir a numeração `#item-N`:** comparar `<h2 id="item-N">` do site ao vivo com o último backup (o WordPress troca aspas e `×`; normalizar). Se a numeração mudou, **refazer os textos dos pacotes** (links de Story, Status, Canal e Direct); posts e Reels já agendados usam "link da bio" e não mudam [R handover §3].
10. **Materiais relacionados:** regenerar só os pacotes do dia afetados (`_fonte`), copiar para `Planejamentos\Andamento\Celular_Whatsapp`; catálogo do WhatsApp é **só por categoria** (não muda por produto); se um dia já está agendado no Instagram, **apagar os 2 itens e criar de novo** (o Instagram não troca a mídia).
11. **Painel e relatório:** rodar `ATUALIZAR_PAINEL.bat` (opcional `PAINEL_SEM_VERIFICAR=1`) e registrar no relatório de atividades.

**Como evitar sobrescrever alterações de outra pessoa ou automação**
- **Há duas automações que também escrevem no site:** a atualização de categorias (3 h) e o backup (somente lê). **Editar uma página de categoria direto no WordPress é desfeito** na próxima republicação: a mudança correta é no `categorias.json` [R 03/11].
- O backup automático detecta mudança pelo campo `modified` e guarda a versão antes (até 200 por página) [R]; o WordPress mantém **revisões** (guia 41+ em 23/10) [R].
- **Antes de editar:** (a) comparar com o backup mais recente (procedimento do handover §4); (b) não usar o painel do WordPress nos dois PCs ao mesmo tempo (texto do `nova_pendencias`); (c) fechar painéis antigos na porta 8842.
- **Não verificado:** se `gerenciar_blog.py` bloqueia a publicação quando o `modified` do site é mais novo do que o último que ele leu. **Não há trava (lock) registrada.** Tratar como risco.
- Credenciais: `Gestao_Anuncios_Blog\2_DADOS\Blog_WordPress\wp_credenciais.json` (existe [V]) guarda a **senha de aplicativo** do WordPress usada pela REST (método: autenticação básica por senha de aplicativo; existe também um modelo `wp_credenciais.exemplo.json`). **O conteúdo não foi lido para este mapa.** O pacote do outro PC deve ficar **sem** esse arquivo.

---

## 7. Recuperação

| Backup | Onde | O que cobre | Frequência | Restauração testada? |
|---|---|---|---|---|
| **Conteúdo das páginas do blog** | `Gestao_Anuncios_Blog\2_DADOS\Blog_WordPress\backups\` (**723** arquivos: páginas `.html/.json`, menu, `categorias_*.json`, snippets) [V] | O **texto/HTML** das páginas e a configuração das categorias, antes de cada alteração | A cada edição | **Sem registro de teste de restauração real.** Existe o comando `gerenciar_blog.py restaurar` [R]; a validação (22/10) só **simulou** editar/remover em memória e fez "publicação real sem mudanças (conteúdo idêntico)" [R] |
| **Backup automático** | `...\backups\automatico\` (**655** arquivos) [V] | Guia (id 5), Início (id 14), páginas de categoria e Natal; só quando `modified` muda; 200 por página | A cada 30 min (Windows) | Sem registro de teste |
| **Revisões do WordPress** | No próprio WordPress | Histórico de edições de páginas | Por edição | [N] |
| **Backup do próprio programa** | `Programas_Diversos_Py\_backups_claude_` e `_backups` de cada pasta | Cópias dos scripts, planilhas e PDFs antes de mudar | Por mudança | Cópias são arquivos simples; restauração = copiar de volta (não testada formalmente) |
| **Base de contatos** | `Planejamentos\Andamento\Base_Contatos_WhatsApp\_backups\` (16) [V] | Planilha antes de cada alteração | Por mudança | Sem registro |
| **Painel** | `Relatorios_Diarios_Anuncios\_backup_painel` [V existe] | Cópias do `.xlsx` | Por execução | Sem registro |
| **Conversas do Claude** | `E:\BKP_INTEGRA_CLAUDE\BACKUPS\` (último 06/11 22:02, 19 conversas, falhas 0) + `FREEZE\` (04/11) [V] | **Conversas**, notas e configurações do Claude. **Não** inclui arquivos do projeto, nem o site | Aproximadamente diário (disparo: N) | **Não há registro de restauração**: `historico_restauracoes.txt` **não existe** e `E:\RESTORE_BKP_INTEGRA_CLAUDE` tem só `desktop.ini` [V]. O manual descreve o procedimento (primeiro em `E:\RESTORE_...`, depois produção) |

**Diferença entre backup de conteúdo e backup completo do site**
- O que existe é **backup de conteúdo** (páginas, menu, categorias, snippets) e das ferramentas locais.
- **Não há registro** de: backup do **banco de dados** do WordPress, **uploads/mídia**, **plugins/tema** e configurações (tema Futurio, All in One SEO, Fluent Forms, WPForms, LiteSpeed), nem de backup da **hospedagem Hostinger** ou do **domínio** [N].
- **Backup da pasta `D:\Projeto_Blog_Comprenolink` como um todo:** **não há registro**. Existe `.gitignore` na raiz, mas **não foi verificado** se é um repositório Git [N]. Cópia parcial para `E:\OneDrive\Downloads\Divulgacao_Blog`: em 30/10 foi registrado que essa pasta não existia mais neste PC [R].
- Consequência: se o WordPress for perdido por inteiro, as **páginas** podem ser reconstruídas a partir dos backups, mas **não** foram identificadas cópias de mídia, plugins e configurações.

---

## 8. Limitações e dúvidas

### 8.1 Fatos verificados hoje (07/11/2026)
| Fato | Evidência |
|---|---|
| Estrutura de 17 pastas principais e 3 arquivos na raiz | Listagem de pastas; `Estrutura_diretorio_..._Claude.txt` (07/11 17:10) |
| 34 pastas em `07_PACOTE_DO_DIA` | Listagem |
| Tarefa Windows "Atualizar categorias blog comprenolink": última 07/11 16:08, resultado 0, próxima 19:08; "Backup automatico blog comprenolink": última 16:55, resultado 0, próxima 17:25 | Consulta ao Agendador |
| Tarefa do Claude `divulgacao-diaria-whatsapp-story`: ativa, 19:12 diário, última 06/11 19:14 | Consulta às tarefas do Claude |
| Guia com **213 produtos**; sem mudanças em 07/11 14:28 e 16:08; DNS falhou em 06/11 22:09 | `atualizar_categorias.log` |
| Backup automático com 4 falhas de DNS (04/11 18:25; 05/11 11:55 e 15:55; 06/11 21:25) | `backup_automatico.log` |
| Painel: última execução 05/11 10:06, saída 0, 66 s; último CSV de vendas 31/10 | `log_painel.txt`; listagem |
| Backup das conversas: 4 execuções registradas (04/11 ×2, 05/11, 06/11), sem falhas; sem histórico de restauração | `historico_backups.txt` |
| Agenda `.ics`: 68 eventos (datas de 03/11/2026 a 03/10/2027; os de 2027 são avisos de renovação de e-mail, domínio e hospedagem) | Leitura do arquivo |
| 723 arquivos em `backups` e 655 em `backups\automatico` | Contagem |
| `wp_credenciais.json` existe (conteúdo **não** lido) | Listagem |

### 8.2 Informações de registros anteriores (não reverificadas hoje)
Metas e decisões do dono; limites do WhatsApp/Instagram; termos do ML (cláusula 4.4, lidos em 05 e 06/11); números do ML Afiliados (02/11) e do Analytics (06/11); automação do ManyChat; ativação do segundo número (06/11); política de catálogo só por categoria (06/11); limite de gasto R$ 50 na conta Meta (06/11); histórico de substituições; tarefas do Windows corrigidas em 02/11; "a rotina noturna fica sem alteração" (06/11).

### 8.3 Pontos **não verificados** (e por quê)
1. **Conteúdo exato do `nova_pendencias.pdf` de 06/11** (leitor de PDF indisponível; lido o gerador).
2. **Se há um só cron do Instagram ativo** (a lista de crons é por conversa; a do Claude nesta conversa foi cancelada de propósito em 07/11).
3. **Se o Google Agenda corresponde ao `.ics`** (não consultado hoje).
4. **Existência de backup do banco de dados, mídia, plugins/tema e da Hostinger.**
5. **Se `gerenciar_blog.py` impede sobrescrever mudanças mais novas** (código não lido para este mapa).
6. **Como o backup das conversas é disparado** (manual ou agendado).
7. **Sincronização entre este PC e o outro** (e se existe cópia automática de scripts).
8. **Estado do arquivo de bloqueio `~$Painel...xlsx`** (31/10).
9. **Resultado dos convites de 06/11 e do estado atual dos seguidores do Canal.**
10. **Se `D:\Projeto_Blog_Comprenolink` é repositório Git.**

### 8.4 Divergências encontradas
- Nome da listagem de estrutura (seção 0) e contagem de produtos (213 × 214).
- `nova_pendencias.pdf` tem o cabeçalho "posição de 04/11/2026" no gerador, mas o PDF é de 06/11.

---

## 9. Parecer técnico (alternativas para uma futura operação com o ChatGPT)
**Premissas (não presumidas):** o ChatGPT **não** tem acesso garantido ao disco D: nem ao Chrome local. Qualquer capacidade de arquivos, navegador ou integrações do ChatGPT Plus **precisa ser confirmada** antes (inclusive o preço atual do plano: **não verificado**). Custos conhecidos: Claude Pro com uso extra (faturas de 29/10 a 03/11 somaram R$ 228,16 [R]; meta do dono é voltar a só a assinatura); ManyChat Pro cerca de US$ 15 (estimativa, hoje não contratado); teste de anúncio R$ 50, total máximo R$ 255 até dezembro; renovação de domínio e hospedagem em **22/09/2027** (agenda).

### Alternativa A: manter os programas locais e o Claude até haver prova de equivalência
- **Como:** nada muda; o ChatGPT só lê documentos e responde dúvidas.
- **Dependências:** Claude aberto, cota do plano, PC ligado.
- **Riscos:** concentração em uma ferramenta; cota do Claude é o limitador (80% em 06/11).
- **Testes:** nenhum além do GO/NO-GO.

### Alternativa B: ChatGPT como assistente, dono (ou outro executor) roda os programas locais
- **Como:** o ChatGPT escreve textos, analisa prints/relatórios e instrui; o dono executa `.bat`/`.py` e cola resultados.
- **Dependências:** dono disponível; envio de prints/arquivos ao ChatGPT.
- **Riscos:** mais passos manuais (o dono pede um passo por vez); sem agendamento automático do Instagram/Status/Canal.
- **Testes:** pedir ao ChatGPT para gerar o texto de 1 dia e conferir contra a política de textos; simular uma troca de link só com a prévia (sem `--aplicar`).

### Alternativa C: integrações (automação sem Claude)
- **Candidatas (a verificar):** agendador de nuvem ou automação no-code ligada ao WordPress (REST com senha de aplicativo), à API oficial do Instagram/Meta para agendamento, e a ferramentas de WhatsApp oficiais. **Nenhuma está configurada hoje** [N].
- **Dependências:** contas e permissões (Instagram profissional ligado a página/Meta, WhatsApp Business API ou ferramenta), custo mensal de ferramenta, tokens guardados com segurança (**nunca** em texto no chat).
- **Riscos:** bloqueio de conta por automação não oficial; regras do ML (anúncio só em redes sociais, sem a marca); custo e manutenção novos; o WhatsApp **Web** foi evitado por risco ao número [R].
- **Testes:** conta de teste ou página de rascunho no WordPress; Instagram em uma conta secundária; limites e termos de uso lidos antes.

### Alternativa D: dividir responsabilidades (recomendação inicial a validar)
| Frente | Quem | Observação |
|---|---|---|
| Estratégia, textos, análise de métricas, revisão de política | ChatGPT | Depende de receber o contexto (documentos da seção 10) |
| Execução no Chrome logado (Instagram, WhatsApp Web, ML) | **Dono** ou Claude (enquanto existir) | Chrome local é o ponto frágil |
| Tarefas automáticas (backup, categorias) | **Windows** (já independente de IA) | Manter; adicionar alerta de falha |
| Gerar PDFs/agenda/pacotes | Scripts locais (qualquer IA pode editar o código; execução local) | Mesmo código |
| Convites e contatos | Dono, à mão | Sem mudança |
| Anúncio pago | Dono ativa; IA apoia (texto, UTM, semáforo) | Termos do ML |

### Testes necessários antes de qualquer transferência (sugestão)
1. Ler `nova_pendencias.pdf` e a agenda e **resumir de volta** (conferir compreensão).
2. Gerar o texto de um dia (feed, Reels, Status) e passar na conferência de política (sem preço, sem "melhor/mais vendido", com aviso de afiliado).
3. Simular uma substituição de link **somente em prévia**.
4. Testar **restauração** de uma página a partir de um backup, em ambiente de teste (hoje sem registro).
5. Confirmar capacidades reais do ChatGPT (arquivos, navegador, integrações, agendamento, memória, custo).
6. Definir **quem agenda o Instagram** e **quem publica Status/Canal** a partir de 16/11, sem duas ferramentas ao mesmo tempo (já houve risco de cron duplicado).
7. Plano de volta: manter o Claude até o dono aprovar a transferência.

---

## 10. Próximos arquivos (essenciais, em ordem de prioridade)
**Não incluir:** `wp_credenciais.json`; `Base_Contatos_WhatsApp.xlsx` e `IMPORTAR_NO_CELULAR\` (dados pessoais); qualquer `.env`/token; conversas e cópias de segurança do Claude.

| Prioridade | Arquivo (caminho exato) | Por quê |
|---|---|---|
| 1 | `D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\nova_pendencias.pdf` (**ou o texto equivalente exportado**; o Claude não conseguiu ler o PDF hoje) | Plano e pendências vigentes |
| 2 | `D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\agenda_nova_pendencias.ics` | Datas e horários |
| 3 | `D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\RELATORIO_MESTRE_CONTINUIDADE_COMPRENOLINK_2026-11-07.md` e este `MAPA_OPERACIONAL_COMPRENOLINK_2026-11-07.md` | Visão geral e diagnóstico |
| 4 | `D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\HANDOVER_TECNICO_001_para_000_2026-11-04.md` e `..._ANEXO_historico_e_pendencias_2026-11-04.md` | Roteiros e histórico |
| 5 | `D:\Projeto_Blog_Comprenolink\Gestao_Anuncios_Blog\1_PROGRAMAS\Blog_WordPress\gerenciar_blog.py` | Edição de produtos/links (ver trava de sobrescrita) |
| 6 | `...\Blog_WordPress\publicar_categorias.py` e `atualizar_categorias_auto.py` | Republicação e automático de 3 h |
| 7 | `D:\Projeto_Blog_Comprenolink\Gestao_Anuncios_Blog\2_DADOS\Blog_WordPress\categorias.json` | Regras de categorias e campanhas (sem credenciais) |
| 8 | `...\Blog_WordPress\backup_automatico.py` e `D:\Projeto_Blog_Comprenolink\Gestao_Anuncios_Blog\PROCESSO_DE_ATUALIZACAO_MANUTENCAO.pdf` | Backup e processo do blog |
| 9 | `D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\programas_fontes_python\4_atualizar_painel_controle.py`, `6_verificar_anuncios.py` e `D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\ATUALIZAR_PAINEL.bat` | Painel e verificação de anúncios |
| 10 | `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Divugação_WhastsApp_Instagram\_fonte\dados_divulgacao.py` e `gerar_artes_catalogo.py` | Como nascem os pacotes do dia |
| 11 | Um pacote de exemplo: `...\07_PACOTE_DO_DIA\2026-12-04_sex\1_TEXTOS_DO_DIA.txt` e `2_LEGENDA_REELS.txt` | Modelo de texto vigente |
| 12 | `D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Base_Contatos_WhatsApp\processo_crescimento_canal_whatsapp.pdf` e `Regras_de_Uso_Base_Contatos_WhatsApp.pdf` | Regras de segurança do WhatsApp |
| 13 | `D:\Projeto_Blog_Comprenolink\Programas_Diversos_Py\gerar_relatorio_atividade.py` e o relatório mais recente em `4_Relatorio_Ativ_Claude_no_Blog` | Registro auditável |
| 14 | `D:\Projeto_Blog_Comprenolink\Estrutura_diretorio_Projeto_Blog_Comprenolink.txt` (182 KB; usar só se for preciso conferir caminhos) | Árvore completa |

*Nenhum pacote completo foi preparado nesta etapa, como solicitado.*
