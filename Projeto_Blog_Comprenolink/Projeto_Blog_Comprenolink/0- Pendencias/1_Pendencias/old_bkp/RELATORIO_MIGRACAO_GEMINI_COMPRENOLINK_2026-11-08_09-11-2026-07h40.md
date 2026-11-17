# RELATÓRIO TÉCNICO DE AUDITORIA E MIGRAÇÃO — COMPRENOLINK → AMBIENTE GEMINI
**Data de corte:** 08/11/2026 (domingo). **Autor:** Claude (assistente que operou o projeto de 21/10 a 08/11/2026).
**Origem:** `D:\Mercado_Livre` (no Windows é a mesma pasta que `D:\mercado_livre`). **Destino proposto:** `D:\Projeto_Blog_Comprenolink` (**ainda não existe**; nada foi movido).
**Idioma do projeto:** português do Brasil, linguagem simples, um passo por vez.

> ## LEIA PRIMEIRO (para o Gemini)
> 1. **Este relatório é um retrato de 08/11/2026.** Fatos marcados **[V]** foram verificados hoje no PC; **[R]** vêm de registros anteriores (memória, handovers, relatórios), com data; **[N]** não verificados. Nada foi inventado; o que não se sabe está escrito "desconhecido".
> 2. **Documentos-base que este relatório complementa (mesma pasta):** `RELATORIO_MESTRE_CONTINUIDADE_COMPRENOLINK_2026-11-07.md` (visão de negócio, 14 seções), `MAPA_OPERACIONAL_COMPRENOLINK_2026-11-07.md` (rotinas e evidências), `HANDOVER_TECNICO_001_para_000_2026-11-04.md` + `..._ANEXO_historico_e_pendencias_2026-11-04.md` (114 entradas de histórico).
> 3. **Fontes de verdade que NÃO mudam com este relatório:** pendências = `nova_pendencias.pdf`; agenda = `agenda_nova_pendencias.ics`; estrutura de pastas = `D:\mercado_livre\Estrutura_diretorio_Mercado_Livre_ComprenoLink_Claude.txt` (gerada por `Gera_Estrutura_Diretorio.bat`).
> 4. **Sem segredos:** nenhuma senha, token, cartão, CPF ou contato pessoal aparece aqui. `wp_credenciais.json` (senha de aplicativo do WordPress) e `Base_Contatos_WhatsApp.xlsx` (dados pessoais) **não devem ser enviados a nenhuma IA**.
> 5. **ALERTA DE CONFORMIDADE (pedido citou Google Ads):** pelos termos do ML Afiliados (cláusula 4.4, lida na fonte oficial em 05 e 06/11/2026), **Google Ads, Google Shopping, Bing Ads e YouTube Ads são PROIBIDOS** para afiliados. Mídia paga só em redes sociais (Instagram/Facebook/TikTok/Pinterest Ads) e **sem a marca "Mercado Livre/ML/Meli/Mercado Pago"** no anúncio. Ver seção 4.
> 6. **Reunião de replanejamento geral: segunda 09/11/2026 às 09:00.** Agendas aqui podem mudar nela. GO/NO-GO de transferência: **13/11**; transferência só a partir de **16/11** e só com aprovação do dono [R 07/11].
> 7. **Limite técnico do Gemini a confirmar antes de assumir:** o Claude operava **dentro do PC do dono** (disco D:, Excel via COM, Chrome com extensão, Agendador do Windows). Se o Gemini não tiver esse acesso, a operação vira "o Gemini instrui, o dono executa" (ver seção 7.4).

---

## 1. ESTRUTURA DE PASTAS ATUAL E MAPEAMENTO PARA O NOVO DIRETÓRIO

### 1.1 Árvore atual de `D:\Mercado_Livre` (primeiro e segundo nível) [V 08/11]
```
D:\mercado_livre
├── .gitignore                          (não é repositório Git: não há .git [V])
├── Gera_Estrutura_Diretorio.bat        (gera a listagem .txt da estrutura)
├── Estrutura_diretorio_Mercado_Livre_ComprenoLink_Claude.txt
├── 0- Pendencias
│   ├── 1_Pendencias                    (nova_pendencias.pdf, agenda_nova_pendencias.ics, handovers .md, guias, planilha semanal)
│   ├── 2_Analises_Anuncios
│   ├── 3_Guia_Passo_a_Passo_Instagram_2026
│   ├── 4_Relatorio_Ativ_Claude_no_Blog (PDFs diários de atividade)
│   ├── 5_Plano_turbinar_anuncio_instagram
│   ├── 99_Programas_PY                 (geradores do Claude) + _backups_claude_30out
│   ├── bkp_drp                         (backlog/histórico do que saiu das pendências)
│   └── Guia_Socio_Como_Pedir_ao_Claude.pdf
├── 1- Gera_Relatorio                   (4 .exe + config_rastreio.json + dados_acessos)
├── 2-Verificar_Erros_Blog              (testar_site_de_novo.bat, robots.txt, security_top.txt)
├── 3- Divugação_WhastsApp_Instagram    (grafia exata, com erro) 00..12, 06_CATALOGO_WHATSAPP, 07_PACOTE_DO_DIA, 09_LOGO, 10_POST_BOAS_VINDAS, _fonte, _backup_pacotes
├── 4- Celular_Whatsapp                 (cópia para celular; origem dos uploads do Instagram)
├── 5_Automação_Instagram               (plano de 29/09 com preços — NÃO USAR)
├── 6_Cartao_Comercial
├── 7_Docs                              (Checklist Turbinar, Dados_Tiktok, Processo_1_Afiliados_ME, teste_site_completo.py)
├── 8_Logo
├── 9_Manutenção_Blog                   (1_PROGRAMAS, 2_DADOS, 3_DOCUMENTACAO, 4_PACOTE_OUTRO_PC, 5_ESBOCO_CATEGORIAS, 9_ORIGINAIS_NAO_MEXER, atalhos 1..6 .bat, CentralBlog.exe, PROCESSO_DE_ATUALIZACAO_MANUTENCAO.pdf, 4_ATUALIZAR_OUTRO_PC.zip)
├── 10_Rastreamento_anuncios            (snippet PHP de rastreio UTM, .exe antigos, links_anuncios.csv)
├── 11_Estrategias_Vendas               (1 PDF de estratégia 6–12 meses)
├── 12_Base_Contatos_WhatsApp           (DADOS PESSOAIS: base, regras, checklist 30 dias, _fonte, _backups, IMPORTAR_NO_CELULAR)
├── 99_Relatorios_Diarios               (painel Excel/PDF, ATUALIZAR_PAINEL.bat, vendas_afiliados, vendas_historico, anuncios_status, historico_consolidado, _historico_relatorios, _backup_painel)
├── python                              (fontes do painel/rastreio: 2_..7_, 8_rodar_com_log.ps1)
├── css, img, js                        (recursos antigos do site; uso atual desconhecido)
```

### 1.2 Propósito, conteúdo e MOMENTO de uso de cada pasta

| Pasta | Propósito exato | Tipos de arquivo | Quem usa / fluxo | Momento exato na rotina |
|---|---|---|---|---|
| `0- Pendencias\1_Pendencias` | Documentos de comando do dono: lista única de pendências, agenda única, handovers, guia do sócio, roteiros | .pdf, .ics, .md, .xlsx | Claude gera → dono lê/importa no Google Agenda | Início do dia (dono lê o plano); ao mudar o plano (regerar PDF+ICS) |
| `0- Pendencias\2_Analises_Anuncios` | Análise crítica de anúncios (27/10), sugestões (30/10) | .pdf, .csv | Consulta | Só ao escolher produtos novos |
| `0- Pendencias\3_Guia_Passo_a_Passo_Instagram_2026` | Guia do Instagram (PDF regerado 05/11) | .pdf | Dono | Consulta pontual |
| `0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog` | Registro auditável do que a IA fez | `RELATORIO_ATIVIDADE_CLAUDE_BLOG_DD_MM_AAAA_HHhMM.pdf` | IA gera → dono recebe | **Fim de toda sessão/agendamento** (regra do dono) |
| `0- Pendencias\5_Plano_turbinar_anuncio_instagram` | Plano de anúncio pago (PDF 9 págs + quadro) e geradores | .pdf, .py | IA/dono | Reuniões Turbinar; 13/11, 19/11, 30/11, 21/12 |
| `0- Pendencias\99_Programas_PY` | **Geradores da IA** (pendências, agenda, relatório, guias, aplicar textos) | .py; `_backups_claude_30out` | IA executa (`python -X utf8`) | Sempre que o plano muda; fim de sessão (relatório) |
| `0- Pendencias\bkp_drp` | Histórico do que saiu das pendências | .txt, .pdf, .py | Arquivo morto | Nunca na rotina |
| `1- Gera_Relatorio` | Programas compilados de relatório: acessos (com verificação de anúncios), links UTM, relatório SEO, teste SEO | .exe, .json | Dono/IA executam | **Segunda 10:00** (antes do painel) e sob demanda |
| `2-Verificar_Erros_Blog` | Teste rápido do site | .bat, .txt | IA/dono | Depois de qualquer mudança no site |
| `3- Divugação_WhastsApp_Instagram` | **Fonte de toda a divulgação**: textos, calendário de posts, catálogo, 34 pacotes diários, logo, geradores `_fonte` | .png, .mp4, .txt, .xlsx, .py | IA gera → copia para pasta 4 | Quando produto/texto muda; planejamento mensal |
| `4- Celular_Whatsapp` | **Cópia** da pasta 3 para o celular e **origem dos arquivos do agendamento** (Instagram 21:09, divulgação 19:12) | idem | Rotinas automáticas leem daqui | **Todo dia 19:12 e ~21:09** |
| `5_Automação_Instagram` | Plano antigo com preços | .py, .json, .png | Ninguém | **Não usar** (viola política sem preço) |
| `6_Cartao_Comercial` | Cartão comercial A4 | .pdf, .py | Dono | Pontual |
| `7_Docs` | Checklist Turbinar Vendas, processo de afiliado, teste completo do site | .pdf, .py | Consulta/teste | Pontual |
| `8_Logo` | Logotipos e vídeos TikTok (TikTok descartado 03/11) | .png, .mp4 | Consulta | Pontual |
| `9_Manutenção_Blog` | **Programas e dados do WordPress**: `gerenciar_blog.py`, `publicar_categorias.py`, `atualizar_categorias_auto.py`, `backup_automatico.py`, `painel_blog.py`; `2_DADOS` (categorias.json, backups, **wp_credenciais.json**) | .py, .json, .html, .exe, .bat | Windows a cada 30 min/3 h; IA ao editar produtos | **Contínuo** (tarefas do Windows) + quando o dono cadastra anúncio |
| `10_Rastreamento_anuncios` | Rastreador UTM original (snippet WP + gerador de links) | .php, .exe, .csv | Origem do rastreio | Raro |
| `11_Estrategias_Vendas` | Estratégia de 6–12 meses | .pdf | Consulta | Reunião de janeiro/2027 |
| `12_Base_Contatos_WhatsApp` | Base com consentimento, regras de convite, checklist 30 dias | .xlsx, .pdf, .ics, .py | Dono envia à mão; IA registra | **Dias úteis 10:00** (convites, até 5/9 por dia) |
| `99_Relatorios_Diarios` | **Painel de métricas** (xlsx+PDF), vendas, status de anúncios, histórico | .bat, .xlsx, .pdf, .csv, .html | `ATUALIZAR_PAINEL.bat` | **Segunda 10:15–10:45** (vendas por prints → CSV → painel) |
| `python` | Código-fonte do painel e do rastreio | .py, .ps1 | Chamado pelo .bat e pelos .exe | Junto com o painel |
| `css`, `img`, `js` | Recursos antigos | — | Ninguém [N] | — |

### 1.3 Estrutura otimizada proposta para `D:\Projeto_Blog_Comprenolink`
**Princípios:** (1) separar **programas**, **dados**, **conteúdo gerado** e **documentos**; (2) nomes sem espaço, sem acento e sem "ç" (o `cmd` e o launch.json já falharam com "ç"); (3) um único ponto de configuração de caminhos; (4) dados pessoais e segredos isolados e fora de qualquer envio a IA.

```
D:\Projeto_Blog_Comprenolink
├── 00_COMANDO                    ← 0- Pendencias\1_Pendencias (pendências, agenda, handovers, este relatório)
│   ├── relatorios_atividade      ← 0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog
│   ├── planos                    ← 0- Pendencias\2_, 3_, 5_ e 11_Estrategias_Vendas
│   └── historico                 ← 0- Pendencias\bkp_drp
├── 01_PROGRAMAS
│   ├── config\caminhos.json      ← NOVO: única fonte de caminhos (ver 2.4)
│   ├── comum\caminhos.py         ← NOVO: módulo que lê caminhos.json
│   ├── geradores_ia              ← 0- Pendencias\99_Programas_PY
│   ├── blog_wordpress            ← 9_Manutencao_Blog\1_PROGRAMAS\Blog_WordPress
│   ├── blog_maquinas             ← 9_Manutencao_Blog\1_PROGRAMAS\Blog_Maquinas
│   ├── painel                    ← python\ (2_..8_)
│   ├── divulgacao                ← 3- Divugação...\_fonte
│   ├── contatos                  ← 12_Base_Contatos_WhatsApp\_fonte
│   ├── relatorios_exe            ← 1- Gera_Relatorio (.exe recompilados)
│   ├── testes_site               ← 2-Verificar_Erros_Blog + 7_Docs\teste_site_completo.py
│   └── atalhos                   ← os .bat 1..6 da Manutenção + ATUALIZAR_PAINEL.bat
├── 02_DADOS
│   ├── blog_wordpress            ← 9_Manutencao_Blog\2_DADOS\Blog_WordPress (categorias.json, estado, logs, backups)
│   ├── painel                    ← 99_Relatorios_Diarios (xlsx, vendas_afiliados, vendas_historico, anuncios_status, historico_consolidado)
│   └── rastreio                  ← 1- Gera_Relatorio\dados_acessos + config_rastreio.json
├── 03_CONTEUDO
│   ├── pacotes_do_dia            ← 3- Divugação...\07_PACOTE_DO_DIA
│   ├── catalogo_whatsapp         ← 06_CATALOGO_WHATSAPP
│   ├── textos_e_guias            ← 00..05, 08, 11, 12 da pasta 3
│   ├── marca                     ← 09_LOGO + 8_Logo + 6_Cartao_Comercial
│   └── celular                   ← 4- Celular_Whatsapp (cópia; manter como "saída")
├── 04_DOCUMENTACAO               ← 9_Manutencao_Blog\3_DOCUMENTACAO + 7_Docs + PROCESSO_DE_ATUALIZACAO_MANUTENCAO.pdf
├── 08_SENSIVEL                   ← NUNCA enviar a IA; excluir de qualquer zip
│   ├── credenciais               ← wp_credenciais.json
│   └── contatos_whatsapp         ← 12_Base_Contatos_WhatsApp (xlsx, _backups, IMPORTAR_NO_CELULAR)
├── 09_ARQUIVO_MORTO              ← 5_Automação_Instagram, 10_Rastreamento_anuncios, 9_ORIGINAIS_NAO_MEXER, css/img/js, _exe_antigos
└── 99_BACKUPS                    ← _backups_claude_30out, _backup_pacotes, _backup_painel
```

**Cuidados da migração de pastas:**
- **Copiar, não mover**, e manter `D:\mercado_livre` intacto até o teste final passar (rollback = religar as tarefas antigas).
- `4_PACOTE_OUTRO_PC` depende de estar **dentro** da pasta de manutenção para usar o `2_DADOS` principal (`gerenciar_blog.pasta_dados_de()`); ao separar programas de dados, ajustar essa função e a env `BLOG_WP_DADOS`.
- `validar_estrutura.py` tem listas `ESTRUTURA_*` fixas: atualizar ou ele acusará erro.
- Backups de `.py` não podem ficar em `2_DADOS` (a validação acusa): usar `.py.bak` ou `99_BACKUPS`.
- `.bat` precisam de **CRLF** (com LF o `cmd` corta os comandos).

---

## 2. SISTEMAS DE APOIO, SCRIPTS E AGENDAMENTOS

### 2.1 Inventário de scripts (ativos)
**Não existem** scripts `.sh`, cron Linux nem fluxos Git no projeto [V]. Tudo é Windows: Python 3.14 (`-X utf8`), Batch, PowerShell, PyInstaller, ReportLab, Pillow, ffmpeg, Excel COM.

| Grupo | Script | Função |
|---|---|---|
| Blog WordPress (`9_Manutenção_Blog\1_PROGRAMAS\Blog_WordPress`) | `gerenciar_blog.py` | listar/editar/remover/restaurar itens do guia via REST (`editar N --link --nome --titulo-anuncio --imagem --desc --beneficios "a\|b" [--aplicar]`; sem `--aplicar` = prévia em `ultimo_diff.txt`) |
| | `publicar_categorias.py` | gera e publica 9 páginas de categoria, Black Friday, Natal, Escolha rápida, Início, menu; aquece cache (`--publicar`, `--previa --data=`) |
| | `atualizar_categorias_auto.py` | republica só se guia/categorias.json/fase da campanha mudou; para com ERRO se item sem categoria |
| | `backup_automatico.py` | salva páginas quando `modified` muda (200 por página); `--forcar` |
| | `painel_blog.py` | painel web local `http://127.0.0.1:8842` |
| | `central_blog.py`, `montar_pacote.py`, `validar_estrutura.py`, `gerar_categorias.py`, `gerar_esboco_categorias.py`, `gerar_manual_*.py` | central tkinter, pacote do PC2, validação, manuais |
| Atalhos (raiz Manutenção) | `1_..6_*.bat`, `GERAR_EXE.bat` | abrir painéis, treino offline, validar, backup agora, ativar tarefa de 3 h, recompilar .exe |
| Painel (`python\`) | `2_gerar_links_anuncios.py`, `3_relatorio_acessos_anuncios.py`, `4_atualizar_painel_controle.py`, `5_recalcular_exportar_painel.ps1`, `6_verificar_anuncios.py`, `7_limpar_historico.py`, `8_rodar_com_log.ps1` | links UTM, relatório de acessos, painel Excel, recalcular/exportar PDF, verificar anúncios, retenção (Lixeira) |
| | `99_Relatorios_Diarios\ATUALIZAR_PAINEL.bat` | orquestra 1/4 verificar → painel → PDF → limpeza (env `PAINEL_SEM_VERIFICAR`, `PAINEL_SEM_LIMPEZA`, `PAINEL_NAO_ABRIR`) |
| Divulgação (`3-...\_fonte`) | `gerar_divulgacao.py`, `dados_divulgacao.py`, `conteudo_guia.py`, `gerar_artes_catalogo.py`, `gerar_reels.py`, `gerar_catalogo_categorias.py`, `gerar_post_boas_vindas.py`, `gerar_logo.py`, `gerar_calendario_instagram.py`, `sincronizar_copias.py` | pacotes diários (feed/story/status/reels + textos), catálogo, logo, cópia para pasta 4 |
| Geradores da IA (`0- Pendencias\99_Programas_PY`) | `gerar_nova_pendencias.py`, `gerar_agenda_nova_pendencias.py`, `gerar_relatorio_atividade.py`, `aplicar_textos_novos.py`, `gerar_guia_socio.py`, `gerar_rotinas_semanais.py`, `gerar_guia_rotina_instagram.py` (+ antigos: `gerar_pendencias_detalhado.py` — **importado** pelo nova_pendencias, não remover) | pendências, agenda, relatório diário, aplicar textos com checagem de política |
| Contatos (`12_...\_fonte`) | `importar_leads_formulario.py`, `gerar_agenda_crescimento.py`, `gerar_checklist_xlsx.py`, `gerar_guia_pdf.py`, **`gerar_base_contatos.py` (APAGA a base — nunca rodar)** | leads do formulário, agenda e checklist |
| Testes | `2-Verificar_Erros_Blog\testar_site_de_novo.bat`, `7_Docs\teste_site_completo.py` | teste do site |
| Backup das conversas (fora do projeto) | `E:\BKP_INTEGRA_CLAUDE\PRG_EXE\BACKUP_CLAUDE.exe` / `RESTAURAR_CLAUDE.exe` | backup das conversas do Claude (rodízio 5 + FREEZE) — **não migra para o Gemini** |

### 2.2 Rotinas agendadas (O QUE / QUANDO / POR QUE)

| # | Rotina | a) O QUE executa | b) QUANDO | c) POR QUE (objetivo / impacto se falhar) |
|---|---|---|---|---|
| 1 | **Tarefa Windows "Backup automatico blog comprenolink"** [V] | `C:\Users\SVR_RYZEN_JAA\AppData\Local\Python\pythoncore-3.14-64\pythonw.exe -X utf8 "D:\mercado_livre\9_Manutenção_Blog\1_PROGRAMAS\Blog_WordPress\backup_automatico.py"` | A cada **30 min**, desde 23/10 14:55; último resultado 0 | Guarda versão anterior das páginas (guia, Início, categorias, Natal) a cada mudança. **Se falhar:** perde-se o ponto de restauração de edições feitas por engano. Falhas de DNS registradas 04/11 18:25, 05/11 11:55/15:55, 06/11 21:25 |
| 2 | **Tarefa Windows "Atualizar categorias blog comprenolink"** [V] | `C:\Users\SVR_RYZEN_JAA\AppData\Local\Microsoft\WindowsApps\pythonw.exe -X utf8 "D:\mercado_livre\9_Manutenção_Blog\1_PROGRAMAS\Blog_WordPress\atualizar_categorias_auto.py"` | A cada **3 h**, desde 29/10 07:08; último resultado 0 | Mantém páginas de categoria/campanha em sincronia com o guia (anúncio novo aparece na categoria; troca BF→Natal em 01/12 sozinha). **Se falhar:** categorias desatualizadas, produto novo invisível, Natal não entra no menu. Para com ERRO se item sem categoria (incluir palavra em `categorias.json`) |
| 3 | **Tarefa do Claude Desktop `divulgacao-diaria-whatsapp-story`** [V] (`C:\Users\SVR_RYZEN_JAA\.claude\scheduled-tasks\divulgacao-diaria-whatsapp-story\SKILL.md`) | Lê `D:\Mercado_Livre\4- Celular_Whatsapp\07_PACOTE_DO_DIA\<AAAA-MM-DD>_<dia>\1_TEXTOS_DO_DIA.txt`; confere o `#item-N` no blog; publica **Status 19:15** e **Canal 19:20** no WhatsApp Web (e Story 19:10 se não agendado); marca o calendário; atualiza relatório | **Todo dia 19:12** (cron `12 19 * * *`); só com o app Claude aberto | Presença diária no WhatsApp (único canal com venda orgânica). **Se falhar:** dia sem divulgação; o dono publica à mão. Consome cota do Claude — **em reavaliação na reunião de 09/11** |
| 4 | **Cron de sessão do Claude — agendar Instagram** [R 06/11] | Copia `feed.png`/`reels.mp4`/legenda do dia para a pasta temporária e agenda **post 19:00 + Reels 19:05** em `instagram.com` → "Programar conteúdo" | Todo dia **20:39** (dispara ~21:09), quando abre a janela D-29; expira em ~7 dias (recriar ~11/11) | O Instagram só permite agendar 29 dias à frente. **Se falhar:** dia sem post; dono escreve "agendar DD/MM". **Só UM cron pode existir** (dois = post duplicado) |
| 5 | Painel de métricas (manual) | `99_Relatorios_Diarios\ATUALIZAR_PAINEL.bat` (Excel fechado) | **Segunda 10:15–10:45** e sob demanda | Medir visitas, cliques, vendas e anúncios fora do ar. **Se não rodar:** decisões do Turbinar (semáforo) sem números |
| 6 | Relatório de acessos (manual) | `1- Gera_Relatorio\1_relatorio_acessos_anuncios.exe` (verifica anúncios se a última verificação > 12 h) | Segunda, antes do painel | Entrada do painel |
| 7 | Relatório de atividade (manual) | `python -X utf8 "0- Pendencias\99_Programas_PY\gerar_relatorio_atividade.py"` | **Fim de toda sessão** | Auditoria exigida pelo dono |
| 8 | Backup das conversas (manual) | `E:\BKP_INTEGRA_CLAUDE\PRG_EXE\BACKUP_CLAUDE.exe` | ~diário à noite (disparo não verificado) | Recuperar conversas do Claude |

**Agendas semanais (Google Agenda, do arquivo `agenda_nova_pendencias.ics`, 68 eventos):** segunda 10:00 rodada semanal; segunda 10:45 números; sexta 14:00 SEO; dias úteis 10:00 convites (dono); 19:10–19:20 divulgação; 20:30 fechar o dia.

### 2.3 Caminhos embutidos que precisam ser ajustados

**A. Fora do projeto (alterar manualmente):**
| Onde | O que mudar |
|---|---|
| Agendador do Windows — tarefa 1 e tarefa 2 | argumento com `D:\mercado_livre\9_Manutenção_Blog\1_PROGRAMAS\Blog_WordPress\...` → novo caminho. Recriar pelo `6_ATIVAR_ATUALIZACAO_AUTOMATICA.bat`/`ativar_atualizacao_automatica.ps1` (que também tem o caminho) |
| `C:\Users\SVR_RYZEN_JAA\.claude\scheduled-tasks\divulgacao-diaria-whatsapp-story\SKILL.md` | 3 ocorrências de `D:\Mercado_Livre\4- Celular_Whatsapp\...` (só se a tarefa do Claude continuar) |
| `C:\Users\SVR_RYZEN_JAA\.claude\launch.json` (config "painel-blog-wp") | já está **quebrado**: aponta para `D:\mercado_livre\Manutenção_Blog\...` (pasta antiga, sem "9_") |
| Memórias do Claude | citam `D:\mercado_livre` em todas as notas (atualizar só se o Claude continuar) |
| `.exe` compilados (`1- Gera_Relatorio\*.exe`, `CentralBlog.exe`, `PainelBlog.exe`) | têm caminhos **embutidos no binário**: recompilar com `python -m PyInstaller --onefile` (o 1º: `--paths python --hidden-import 6_verificar_anuncios`) depois de ajustar o .py |
| `E:\OneDrive\Download\Divulgacao_Blog` | destino de `sincronizar_copias.py` (já registrado como inexistente em 30/10 [R]) |

**B. Dentro do projeto — 41 arquivos com caminho absoluto `D:\mercado_livre` / `D:/mercado_livre` [V 08/11, excluindo backups e arquivo morto]:**
| Nº ocorr. | Arquivo |
|---|---|
| 1 | `0- Pendencias\99_Programas_PY\aplicar_textos_212_214.py` |
| 2 | `0- Pendencias\99_Programas_PY\aplicar_textos_novos.py` |
| 5 | `0- Pendencias\99_Programas_PY\gerar_agenda_cadastro_whatsapp.py` |
| 3 | `0- Pendencias\99_Programas_PY\gerar_agenda_nova_pendencias.py` |
| 6 | `0- Pendencias\99_Programas_PY\gerar_agenda_novas_atividades.py` |
| 2 | `0- Pendencias\99_Programas_PY\gerar_agenda_replanejamento.py` |
| 3 | `0- Pendencias\99_Programas_PY\gerar_analise_critica.py` |
| 5 | `0- Pendencias\99_Programas_PY\gerar_cadastro_7_categorias.py` |
| 1 | `0- Pendencias\99_Programas_PY\gerar_cronograma_pendencias.py` |
| 8 | `0- Pendencias\99_Programas_PY\gerar_guia_rotina_instagram.py` |
| 5 | `0- Pendencias\99_Programas_PY\gerar_guia_socio.py` |
| 3 | `0- Pendencias\99_Programas_PY\gerar_nova_pendencias.py` |
| 10 | `0- Pendencias\99_Programas_PY\gerar_pendencias_detalhado.py` |
| 8 | `0- Pendencias\99_Programas_PY\gerar_pendencias_dono_31out.py` |
| 5 | `0- Pendencias\99_Programas_PY\gerar_pendencias_whatsapp.py` |
| 8 | `0- Pendencias\99_Programas_PY\gerar_relatorio_atividade.py` |
| 7 | `0- Pendencias\99_Programas_PY\gerar_rotinas_semanais.py` |
| 9 | `0- Pendencias\99_Programas_PY\gerar_validacao_whatsapp_vendas.py` |
| 1 | `12_Base_Contatos_WhatsApp\_fonte\gerar_agenda_crescimento.py` |
| 1 | `12_Base_Contatos_WhatsApp\_fonte\gerar_checklist_xlsx.py` |
| 2 | `12_Base_Contatos_WhatsApp\_fonte\gerar_guia_pdf.py` |
| 1 | `12_Base_Contatos_WhatsApp\_fonte\importar_leads_formulario.py` |
| 1 | `2-Verificar_Erros_Blog\testar_site_de_novo.bat` |
| 1 | `3- Divugação_WhastsApp_Instagram\_fonte\conteudo_guia.py` |
| 1 | `3- Divugação_WhastsApp_Instagram\_fonte\dados_divulgacao.py` |
| 1 | `3- Divugação_WhastsApp_Instagram\_fonte\gerar_calendario_instagram.py` |
| 1 | `3- Divugação_WhastsApp_Instagram\_fonte\gerar_divulgacao.py` |
| 1 | `3- Divugação_WhastsApp_Instagram\_fonte\gerar_post_boas_vindas.py` |
| 2 | `3- Divugação_WhastsApp_Instagram\_fonte\sincronizar_copias.py` |
| 1 | `5_Automação_Instagram\1_gerar_calendario.py` (arquivo morto) |
| 1 | `6_Cartao_Comercial\gerar_cartao_a4.py` |
| 7 | `7_Docs\gerar_checklist_vendas_pdf.py` |
| 1 | `7_Docs\gerar_pdf_conversao_performance.py` |
| 1 | `99_Relatorios_Diarios\ATUALIZAR_PAINEL.bat` (só texto de ajuda) |
| 1 | `python\2_gerar_links_anuncios.py` |
| 5 | `python\3_relatorio_acessos_anuncios.py` (grava HTML em `99_Relatorios_Diarios\_historico_relatorios`) |
| 12 | `python\4_atualizar_painel_controle.py` |
| 1 | `python\gerar_relatorio_blog_v4_link_curto (2).py` |
| 1 | `python\test_blog_seo.py` |

Os programas do `9_Manutenção_Blog` usam **caminhos relativos** (`..\..\2_DADOS\Blog_WordPress` ou env `BLOG_WP_DADOS`/`BLOG_RAIZ`): migram sem trocar texto, **mas** a nova separação programas/dados exige ajustar a lógica de `pasta_dados_de()`.

**Além do prefixo, mudam também os nomes de subpastas** (`0- Pendencias\99_Programas_PY` → `01_PROGRAMAS\geradores_ia`, etc.): uma troca simples de `D:\mercado_livre` por `D:\Projeto_Blog_Comprenolink` **não basta** se a estrutura nova da seção 1.3 for adotada.

### 2.4 Refatoração recomendada de caminhos
1. Criar `01_PROGRAMAS\config\caminhos.json` (raiz + cada pasta lógica: `pacotes_do_dia`, `celular`, `dados_blog`, `painel`, `relatorios_atividade`, `comando`…).
2. Criar `01_PROGRAMAS\comum\caminhos.py` com `RAIZ = Path(os.environ.get("CNL_RAIZ", <lido do json>))` e funções `pasta("pacotes_do_dia")`.
3. Trocar nos 41 arquivos as constantes absolutas por `from caminhos import pasta`. **Em Python usar `/`** em caminhos Windows (um `\0` vira NUL e corrompe o script — já aconteceu).
4. `.bat`: usar `%~dp0` (pasta do próprio .bat) em vez de caminho absoluto; salvar com CRLF.
5. Recompilar os .exe, recriar as 2 tarefas do Windows, rodar `4_VALIDAR_ESTRUTURA.bat` e `testar_site_de_novo.bat`.
6. Teste de aceite: painel completo (`ATUALIZAR_PAINEL.bat` saída 0), `atualizar_categorias_auto.py` "sem mudanças", `backup_automatico.py --forcar`, `gerenciar_blog.py listar`, gerar o relatório de atividade, gerar um pacote do dia em pasta de teste.

---

## 3. ARQUITETURA DO BLOG (Hostinger / WordPress — comprenolink.net)

| Componente | Detalhe |
|---|---|
| Hospedagem | Hostinger (CDN hcdn + LiteSpeed). Renovação domínio/hospedagem: **22/09/2027** (agenda). Login Hostinger: só o dono (senha diferente da do WP) |
| Tema | **Futurio**; faixa `.full-head-img` reestilizada como hero; títulos vêm do tema (H1 tirado do conteúdo); rodapé próprio via snippet |
| CSS | Personalizar > CSS adicional, classes `cnl-*` (`.cnl-campanha-home`, `.cnl-faixa-campanha`) |
| Plugins | All in One SEO (sitemap `/sitemap.xml`, meta descrições), LiteSpeed Cache, Code Snippets, **Fluent Forms** (form id 4 — inscrições com consentimento LGPD + campo WhatsApp opcional), WPForms Lite (form 568, legado, não guarda entradas), **Hostinger Affiliate Plugin** (blocos `wp:hostinger-affiliate-plugin/mercado-block`: título/foto/preço **ao vivo** do ML), Site Kit (GA4 propriedade 562145071, G-RJXXKTBCB9), FluentSMTP (instalado **sem configuração**) |
| Snippets (Code Snippets) | **6** Cache-Control 10 min + 301 de `/5-2/` e `/5.2/` para o guia (preserva query) + autor/categoria + rodapé; **7** login do painel (X-WP-Auth); **8** "Sem preço nos cartões" (remove `div.product-price`); **9** verificação Search Console (**não apagar**); **11** esconde título duplicado; rastreio UTM próprio (snippet de `10_Rastreamento_anuncios`) |
| Páginas | Início (id 14, estática, vitrine de categorias + botão de campanha); **Guia** `/melhores-produtos-mercado-livre-2026/` (id 5, ~213 produtos, âncoras `#item-N`, Escolha rápida, FAQ, "Não compre se" no Top 10); 9 categorias (Tecnologia & Informática 111, Áudio & TV 112, Casa & Eletrodomésticos 113, Ferramentas & Utilidades 114, Esporte & Fitness 115, Casa/Cama & Decoração 170, Beleza & Saúde 173, Bebê & Maternidade 374, Moda Infantil & Juvenil 432); `/black-friday/` (116); `/presentes-de-natal/` (no ar desde 03/11; menu/home trocam em 01/12); Sobre (17), Privacidade (3), Contato (19, botão WhatsApp + e-mail) |
| Taxonomia | **Não usa categorias/tags nativas do WP**: as "categorias" são páginas geradas a partir de `categorias.json` (palavras-chave por subcategoria com borda à esquerda; mínimo 3 produtos; tags de campanha `black-friday`, `natal-presentes` com `campanha_ate`, `a_partir_de`, `destaques` Top 10, `html_apos_aviso`, `html_antes_guia`). **Editar essas páginas direto no WP é desfeito em até 3 h.** Armadilhas de palavras: "body" pega Bodybuilders; "feminino" pega perfume; "pote" pega "potes" de suplemento |
| Integração REST | `/wp-json/wp/v2/pages` com **senha de aplicativo** "Painel Blog" do usuário `compre.no.link26` (Basic Auth + cabeçalho X-WP-Auth); `/wp-json/aioseo/v1/post {id, description}` para meta descrição; `aioseo_meta_data.description` nas páginas |
| Webhooks | **Nenhum** configurado [R] |
| Medição | GA4 (Site Kit), Search Console (propriedade de prefixo, conta do blog), Bing Webmaster (importado do GSC). PageSpeed mobile do guia 91; página fora do cache leva ~12 s (aquecer após editar; quebra-cache `?nc=`, nunca `?m=` → 404) |
| E-mail | Não funciona (Hostinger bloqueado; Gmail do blog sem 2 etapas → sem senha de app) |
| Backups | Só conteúdo (páginas/menu/categorias/snippets). **Sem backup registrado de banco, mídia, plugins/tema ou da Hostinger** [N] — risco a tratar na migração |

---

## 4. FUNIL DE AFILIADOS E DIRETRIZES DE ANÚNCIOS

### 4.1 Desenho do funil
```
Tráfego                         Pre-lander (blog)                         Conversão
──────────────────────────────  ────────────────────────────────────────  ──────────────────────────
Instagram feed/Reels 19:00/05 ┐
  (link da bio → /black-friday)│
Story 19:10 (adesivo de link) ─┤→ Guia #item-N  ou  página de categoria  → botão do cartão (meli.la)
WhatsApp Status 19:15 / Canal ─┤   (texto de venda, sem preço, "confira     → anúncio no Mercado Livre
ManyChat (BLACK/LINK/QUERO) ───┤    o valor do dia", aviso de afiliado)     → compra (cookie do afiliado)
Catálogo WhatsApp (categorias)─┤                                           → comissão no ML Afiliados
Busca orgânica (Google/Bing) ──┤                                             (vendas só visíveis no painel
Anúncio pago Meta (teste) ─────┘                                              do ML; prints → CSV → painel)
```
**Regra de destino:** todo tráfego (orgânico e pago) vai para **uma página do blog com UTM**, nunca para `meli.la` direto em anúncio.

### 4.2 Conformidade — Programa de Afiliados do Mercado Livre (cláusula 4.4, `mercadolivre.com.br/ajuda/30228`, lida 05 e 06/11/2026)
- Mídia paga **permitida só em redes sociais** (Instagram, Facebook, TikTok, Pinterest Ads), a partir da conta do próprio afiliado aprovada.
- **Proibido:** Google Ads, Google Shopping, Bing Ads, YouTube Ads; palavras-chave/texto com "Mercado Livre", "Mercado Pago", "Meli", "ML"; passar-se por canal oficial; mídia paga sobre conteúdo de creators; **comprar pelo próprio link** (as 7 vendas recusadas "conta vinculada" foram compras do dono); anúncio que redireciona sem ação do usuário ou força instalação do app.
- CONAR: aviso "Publi: contém link de afiliado" em todo texto.
- **Reler a página oficial antes de cada ativação** (próxima: 13/11).
- **Ponto de atenção:** os posts **orgânicos** usam a hashtag `#mercadolivre` e `#achadosmercadolivre`. Isso é orgânico (permitido), mas **num anúncio pago essas hashtags/termos não podem aparecer** — remover ao "turbinar" um post.

### 4.3 Conformidade — Google Ads / Meta
- **Google Ads: não usar** (proibido pelo ML). SEO orgânico no Google é permitido e está em andamento.
- **Meta (Instagram) — plano aprovado em 05/11:** conta "Compre no Link - Anúncios" (BRL, fuso São Paulo, limite de gastos R$ 50, pagador = dono). Teste **R$ 50 em 16–18/11**, objetivo Tráfego, só Instagram, Brasil, 18–45 anos, destino guia com `?utm_source=instagram&utm_medium=pago&utm_campaign=teste_turbinar`. BF R$ 105 (21–27/11) e Natal R$ 100 (05–14/12) **só com semáforo verde** (CPC ≤ R$ 0,50). Total máximo **R$ 255**. Avaliações 19/11, 30/11; relatório final 21/12.
- Política de texto para evitar reprovação: sem preço, sem "melhor/menor preço", "desconto", "% off", "promoção", "mais vendido", "líder", "garantido"; sem promessa de saúde/estética; sem marca ML; imagem sem texto excessivo; página de destino com Privacidade e Contato publicados (já estão).

### 4.4 Rastreamento
| Camada | Padrão |
|---|---|
| UTM | `utm_source` = `instagram` \| `whatsapp`; `utm_medium` = `bio` \| `stories` \| `dm` \| `status` \| `canal` \| `grupos` \| `lista` \| `catalogo` \| `pago`; `utm_campaign` = `black_friday` \| `natal` \| `teste_turbinar`; `utm_content` = `AAAAMMDD_produto` (ex.: `20261109_samsung_galaxy_a17_5g_256gb`) ou `manychat`; categorias internas `cat_*` |
| Âncora | `#item-N` do guia (muda quando item entra/sai: **conferir pelo nome** com `gerenciar_blog.py listar` antes de publicar) |
| Link de afiliado | `meli.la/xxxx` gerado **pelo dono** no ML Afiliados (botão "Compartilhar" → "Gerar link"; etiqueta de afiliado do painel). Link de catálogo `/p/MLB...` devolve sempre o mesmo meli.la (pode cair em anúncio pausado) → usar outro produto ou `/up/MLBU...` |
| Sub-IDs | **Não usados** (o ML Afiliados do dono não oferece sub-id registrado) [R] |
| Redirecionamentos | 301 `/5-2/` e `/5.2/` → guia (snippet 6, preserva query, sem cache porque a CDN ignora `utm_` na chave) |
| Rastreio próprio | snippet WP grava acessos; `1_relatorio_acessos_anuncios.exe` lê; painel atribui vendas a visitantes por semelhança de nome (≥ 0,5) + janela de 7 dias. `127.0.0.1` = teste |
| Vendas | Sem exportação no ML: prints da aba Vendas (4 status, 180 dias) → `vendas_ml_AAAA-MM-DD.csv` em `vendas_afiliados` → painel. **Último CSV: 31/10** |
| Problema aberto | **Nenhuma visita com UTM de Instagram/WhatsApp/ManyChat desde 31/10** — investigar 09/11 |

---

## 5. PLANEJAMENTO DE ATIVIDADES E JUSTIFICATIVAS

### 5.1 Executado (resumo cronológico com o porquê)
| Período | O que foi feito | Por quê |
|---|---|---|
| 21/10 | Home real (antes "Hello world!"), guia com título, H2 com meli.la, Sobre/Privacidade/Contato, 301 de URL antiga | 105 de 110 visitas caíam numa home vazia; páginas legais exigidas para anúncios e confiança |
| 22–23/10 | Painel Excel, backup automático 30 min, painel do blog, cartões **sem preço** | Medir; poder voltar atrás; preço muda e gera reclamação/reprovação |
| 23–27/10 | Guia de 21 → 200 itens com texto de venda honesto; árvore de 9 categorias; campanhas BF/Natal programadas; atualização a cada 3 h | Variedade e SEO por categoria; páginas sazonais prontas antes do pico |
| 26–27/10 | Pacote de divulgação (34 dias), catálogo, logo, Instagram profissional, ManyChat, Search Console | Canal social com rotina fixa; automação oficial (sem bots) |
| 29–31/10 | Instagram agendado 02/11→27/11; textos sem "mais vendidos" | Constância; política do ML/CONAR |
| 01–03/11 | Correção de âncoras, substituição de anúncios fora do ar, GA4, foco só WhatsApp+Instagram+ML, lista e agenda únicas | Links quebrados perdem venda; dono se confundia com vários arquivos |
| 04/11 | Base de contatos com consentimento; **automação de convites cancelada** | Risco de bloqueio do número |
| 05/11 | Anúncio pago liberado (teste R$ 50), conta Meta criada, termos do ML lidos | Testar tráfego pago com baixo risco financeiro e dentro dos termos |
| 06/11 | Catálogo só por categoria; 2º número; medição lida; 3 substituições | Menos manutenção; reserva do número principal |
| 07/11 | Relatório mestre + mapa operacional | Avaliar continuidade em outra IA |

### 5.2 Por executar (vigente em 08/11, sujeito à reunião de 09/11)
| Data | Atividade | Por quê |
|---|---|---|
| 08/11 ~21:09 | Agendar 07/12 no Instagram | Janela D-29 abre |
| **09/11 09:00** | **Reunião de replanejamento geral** (até 31/12; uso da cota; peso das tarefas; tarefa 19:12) | Reduzir custo e retrabalho |
| 09/11 | Rodada semanal (vendas por prints, Canal, painel), Search Console/Bing, rascunho do anúncio (sem ativar), item 77 Colágeno, investigar UTM | Números para o semáforo |
| 10/11 | `/presentes-de-natal/` no Search Console; agendar 09/12 | Indexar antes do pico |
| 11/11 | Teste ManyChat (dono); recriar cron do Instagram | Cron expira ~12/11 |
| 12/11 | Agendar 11/12 | Janela |
| **13/11** | Reler termos do ML; aprovar anúncio; painel; **GO/NO-GO da transferência** | Conformidade; decisão de migração |
| 15–24/11 | Agendar 14/12, 16/12, 18/12, 21/12, 23/12 (janelas) | Dezembro completo |
| **16–18/11** | Teste pago R$ 50 (dono ativa) | Validar CPC |
| 19/11 / 20/11 | Avaliação; limite → R$ 155 se verde | Semáforo |
| 21–27/11 | BF paga R$ 105 (condicional); **27/11 Black Friday** (sem convites; campanha até 30/11) | Pico de vendas |
| 30/11 | 2ª avaliação | Decidir Natal |
| 01/12 | Natal assume menu/home (automático); bio de Natal; indexação | Sazonalidade |
| 04/12 / 05–14/12 | Limite R$ 100; Natal pago (condicional) | — |
| 21/12 | Relatório final do Turbinar | Fechamento |
| Jan/2027 | Reunião de decisão com números | Continuar/escalar/encerrar |
| A definir | **Migração para `D:\Projeto_Blog_Comprenolink`** (seção 7.3) | Pedido deste relatório |

---

## 6. SYSTEM PROMPTS, INSTRUÇÕES E PADRÕES DE CONTEÚDO

### 6.1 Instrução de sistema sugerida para o Gemini (consolidada das regras do dono)
```
Você é o assistente técnico e de marketing do CompreNoLink (blog de afiliados do Mercado Livre, comprenolink.net).
Responda SEMPRE em português do Brasil, linguagem simples, UM PASSO POR VEZ, respostas curtas.
Dono: José Antônio (opera sozinho; há um sócio que participa das decisões).

SEGURANÇA (prioridade máxima)
- Em todo pedido, avise logo se há risco de bloqueio de conta/número ou violação de termos e proponha o caminho seguro.
- Nunca peça nem digite senhas, códigos, cartão, CPF ou endereço. Nunca burle captcha.
- Nunca envie mensagens em massa nem automatize convites no WhatsApp. Convites só à mão pelo dono, para contatos "Conhecido", até 5/dia (1ª semana) e 9/dia depois, 3 min entre eles, 9h–20h.
- Nunca use Google Ads/Bing/YouTube Ads; anúncio pago só Instagram/Facebook, sem a marca Mercado Livre/ML/Meli, destino = página do blog com UTM.
- Dono, família e sócio não compram pelo link do blog.

AUTONOMIA
- Resolva sozinho o óbvio e sem risco (avise depois em 1 linha). Dê opções quando houver risco, custo ou ação irreversível.
- Sempre pergunte antes de: gastar dinheiro, apagar dados, publicar/enviar em nome do dono, mudar bio/links/catálogo, criar/editar eventos da agenda.
- Conclua na data combinada, sem replanejar; se der erro, corrija a causa e conclua.

ARQUIVOS
- Uma lista de pendências (nova_pendencias.pdf) e uma agenda (agenda_nova_pendencias.ics). Não crie outros arquivos de pendência/log.
- Não crie arquivo solto na raiz; pergunte antes de criar pasta. Apagar = Lixeira do Windows.
- Ao fim de cada sessão, gere o relatório de atividade (PDF) e envie ao dono.
- Em toda análise de números: termine com "Conclusão da performance" + "Pontos de atenção".
- Agenda do Google: não marque FEITO, não edite nem apague eventos; o dono retira.
- Nunca invente métricas, especificações ou preços.
```

### 6.2 Política de copywriting dos produtos (permanente)
- **Objetivo:** texto atrativo, benefício em primeiro lugar, linguagem de vantagem para quem compra, selos curtos e chamativos — **só com fatos do anúncio**.
- **Proibido** (regex de `aplicar_textos_novos.py`): `R$`, "reais", "barato", "menor preço", "melhor preço", "desconto", "% off", "promoção", "melhor/melhores", "mais vendido", "líder", "garantido", "oferta do mês"; "preço antes x agora"; promessas de saúde/estética (suplementos: só alegação permitida; nada de "antirrugas", "olheiras", "renovação celular").
- Frase padrão de preço: **"Confira o valor do dia direto no Mercado Livre."**
- Estrutura do cartão no guia: nome curto · selo · descrição (1 parágrafo `<p>`) · Benefícios (lista) · Ideal para (lista) · título do cartão · alt da foto · "Não compre se" (Top 10).
- Anúncio novo chega do WP com placeholder ("Olha o que eu encontrei!") e sem categoria: escrever textos e incluir palavras em `categorias.json`; mostrar antes de aplicar; backup sempre.

### 6.3 Modelo dos textos diários (`1_TEXTOS_DO_DIA.txt`, exemplo real de 09/11)
```
19:00 Instagram – Post (feed.png)
🔥 <Produto>
<1 frase de benefício>
✅ <benefício 1> ✅ <benefício 2> ✅ <benefício 3> ✅ <benefício 4>
💡 Ideal para: <público>.
👉 Comente BLACK que eu te mando o link no Direct, ou toque no link da bio.
Confira o valor do dia direto no Mercado Livre.
Publi: contém link de afiliado. Posso ganhar uma comissão, sem custo extra para você. Preços e estoque podem mudar no Mercado Livre.
#blackfriday #blackfriday2026 #ofertas #<categoria...> (hashtags por categoria, sem marca de produto)

19:10 Story: título + 1 linha + "Toque no link para ver no blog e conferir o valor do dia no Mercado Livre." + link UTM stories #item-N
19:15 WhatsApp Status: *negrito* + benefícios + link UTM status + "_Link de afiliado: posso ganhar comissão, sem custo extra para você._"
19:20 WhatsApp Canal: igual ao Status, UTM canal
```
- Reels: 11 s, 3 cenas a partir do `story.png` (ffmpeg); texto fixo "Veja os detalhes no Mercado Livre"; legenda = a do feed.
- Instagram: bio 3 linhas ("🛒 Achados do Mercado Livre por categoria / 🔥 Black Friday: Top 10 selecionado / 💬 Comente BLACK e receba o link 👇"); respostas salvas `bf, valor, zap, blog, obg, natal`; WhatsApp respostas rápidas `/canal /bf /natal /link /preco /pedido /obrigado`.
- Armadilhas técnicas: no WhatsApp Web **ENTER envia** (legenda numa linha só); campo link do catálogo ≤ 75 caracteres; no Instagram digitar a legenda com o teclado (colar por script perde as quebras); hora `hh` e `mm` separados.

### 6.4 SEO
- Meta descrições via AIOSEO para Início, guia e cada categoria (campo `meta_descricao` em `categorias.json`).
- Sitemap enviado ao GSC e Bing; indexação manual de páginas novas pela Inspeção de URL.
- Sem "mais vendido/líder" nas páginas; "Atualizado em" do guia só depois de conferir anúncios e links (rotinas 13/11, 26/11, 11/12).

---

## 7. STATUS DE EXECUÇÃO E PENDÊNCIAS

### 7.1 100% operacional e testado
- Blog no ar: guia ~213 produtos sem preço, 9 categorias, BF e Natal programados, Contato com WhatsApp, Canal do WhatsApp nos botões [V/R].
- Tarefas do Windows de backup (30 min) e categorias (3 h): resultado 0 hoje [V] (falhas pontuais de DNS se recuperam sozinhas).
- Instagram agendado de 02/11 até 04/12 (conferido no calendário) [R 05/11].
- Tarefa 19:12 de Status/Canal ativa [R 07/11].
- ManyChat 1 automação LIVE no post fixado [R].
- GA4, Search Console (home, guia e 9 categorias indexadas), Bing [R 06/11].
- Painel de métricas (última execução 05/11, saída 0) [R].
- Conta Meta de anúncios criada, limite R$ 50, nada gasto [R 06/11].
- Catálogo WhatsApp só com 9 categorias [R 06/11].

### 7.2 Pendente, com falha ou programado
| Item | Situação |
|---|---|
| Reunião 09/11 09:00 | Programada |
| Agendar Instagram 07/12 a 23/12 | Programado (janelas D-29) |
| Recriar cron do Instagram (~11/11); garantir um só | Programado |
| UTM de Instagram/WhatsApp sem visitas desde 31/10 | **Falha a investigar** |
| Vendas após 31/10 não importadas | Pendente (prints do dono) |
| Anúncio teste: faltam destino com UTM, texto/imagem, aprovação | Programado 09–13/11 |
| "Comente CANAL" no ManyChat; teste com 2ª conta | Aguardando dono |
| E-mail do site (SMTP) | **Bloqueado** |
| Backup completo do WordPress (banco/mídia/plugins) | **Inexistente** — criar antes da migração |
| `launch.json` aponta para pasta antiga | **Quebrado** |
| Restauração de backup nunca testada | Pendente |
| Testar `ATUALIZAR_AQUI.bat` no PC2 | Aguardando dono |
| Item 77 Colágeno pausado | Programado 09/11 |
| Blog das máquinas no Google Sites | Desconhecido |
| 12 vendas "em revisão": alguma compra própria? | Desconhecido (dono confere) |

### 7.3 Plano de migração para `D:\Projeto_Blog_Comprenolink` (proposto, não executado)
| Passo | Ação | Como validar |
|---|---|---|
| 0 | Dono aprova a estrutura da seção 1.3 (e a data — sugestão: **depois de 30/11**, fora da semana da Black Friday) | OK em chat |
| 1 | Backup completo: zip de `D:\mercado_livre` + backup do WordPress pela Hostinger (banco + arquivos) | Zip abre; backup listado no hPanel |
| 2 | Pausar as 2 tarefas do Windows e a tarefa 19:12 durante a cópia | Agendador "Desabilitado" |
| 3 | Copiar para a nova árvore (robocopy, sem `/MIR`), separando `08_SENSIVEL` | Contagem de arquivos igual |
| 4 | Criar `caminhos.json` + `caminhos.py`; refatorar os 41 arquivos | `grep mercado_livre` = 0 no código ativo |
| 5 | Ajustar `gerenciar_blog.pasta_dados_de()`, `validar_estrutura.py`, `.bat` (CRLF, `%~dp0`) | `4_VALIDAR_ESTRUTURA` TUDO CERTO |
| 6 | Recompilar .exe; recriar tarefas do Windows com o novo caminho | Execução manual com resultado 0 |
| 7 | Atualizar a tarefa 19:12/SKILL.md e o cron do Instagram (ou desligar se o Gemini assumir) | Uma execução assistida |
| 8 | Teste de aceite (seção 2.4 item 6) | Todos 0/OK |
| 9 | Rodar em paralelo 7 dias; depois arquivar `D:\mercado_livre` (não apagar) | Sem erro nos logs |

### 7.4 Divisão de trabalho recomendada se o Gemini não tiver acesso ao PC
| Frente | Quem |
|---|---|
| Estratégia, textos (com a política 6.2), análise de prints/relatórios, semáforo do anúncio | Gemini |
| Rodar `.bat`/`.py`, tarefas do Windows | Windows (automático) + dono |
| Agendar Instagram / publicar Status e Canal | Dono (ou ferramenta oficial Meta Business Suite) — **nunca duas ferramentas agendando o mesmo dia** |
| Gerar links meli.la, convites, cartão, senhas | Só o dono |

---

## CONCLUSÃO DA PERFORMANCE E PONTOS DE ATENÇÃO

**Conclusão:** a infraestrutura está madura (blog com ~213 produtos, categorias automáticas, backups, agenda e conteúdo diário prontos até dezembro), mas o resultado comercial ainda é pequeno: R$ 172,00 de comissão estimada em revisão em 180 dias, uma venda orgânica confirmada (R$ 2,29) e tráfego de ~17 usuários/semana (06/11). O gargalo é **tráfego**, não tecnologia.

**Pontos de atenção (prioridade):**
1. **Não migrar na semana da Black Friday (21–30/11)**: qualquer quebra de caminho derruba as tarefas automáticas no pico.
2. **Google Ads é proibido** pelo ML; usar só Meta, sem a marca e sem `#mercadolivre` nos anúncios pagos.
3. **Não existe backup completo do WordPress** (banco, mídia, plugins): fazer antes de qualquer migração.
4. A troca de caminhos não é só "buscar e substituir": 41 arquivos, 7 .exe com caminho embutido, 2 tarefas do Windows, 1 tarefa do Claude e a lógica do pacote do PC2.
5. **Agendamento duplicado** do Instagram se Claude e Gemini/dono agendarem ao mesmo tempo.
6. UTM de redes sociais sem registro desde 31/10: pode estar subestimando o tráfego social.
7. Dados sensíveis (`wp_credenciais.json`, base de contatos) não podem ir para nenhuma IA.
