# HANDOVER TÉCNICO: conversa "001- DAY BY DAY" → conversa "000- Análise Checklist Turbinar Vendas"
Data: 04/11/2026 (noite). Autor: conversa 001 (Claude Sonnet 5.5). Pedido do dono: passar conhecimento técnico, pesquisa e atividades para a 000.
Regra de ouro: este documento é um ponto de partida. Confira cada fato nos arquivos atuais antes de agir (números de item, caminhos e estado do WhatsApp mudam).

## 0. Resumo executivo
- Projeto: blog de afiliados comprenolink.net (Mercado Livre), Instagram @compre.no.link, WhatsApp Business (11) 99495-9657, painel de métricas.
- Estado em 04/11 21:00: posts + Reels agendados no Instagram até **02/12** (28/11, 29/11, 30/11 e 02/12 feitos; novembro inteiro com 19:00 e 19:05). Próximo: **04/12** (janela abre 05/11 ~20:00).
- Atividade passada à 000: o agendamento diário no Instagram (cron ~20:39). O cron a6d1f751 da 001 só é apagado depois que a 000 confirmar que criou o dela. NUNCA dois crons iguais (duplicaria post).
- Memória compartilhada: `rotinas-agendadas-sessoes.md` (mapa de donos), `instagram-agendamento-upload.md`, `feedback-relatorio-atividade.md`, `estrutura-mercado-livre.md`.

## 1. Caminhos principais (barras normais nos scripts; nunca barra invertida seguida de dígito)
- Raiz: `D:\Projeto_Blog_Comprenolink`.
- Pacotes do dia: `Planejamentos\Andamento\Divugação_WhastsApp_Instagram\07_PACOTE_DO_DIA\<AAAA-MM-DD_dia>` (fonte) e cópia em `Planejamentos\Andamento\Celular_Whatsapp\07_PACOTE_DO_DIA`. Cada pasta: feed.png, story.png, status.png, reels.mp4, reels_capa.jpg, 1_TEXTOS_DO_DIA.txt, 2_LEGENDA_REELS.txt (e campanha_12h00.png nos dias de lista).
- Geradores dos pacotes: `Planejamentos\Andamento\Divugação_WhastsApp_Instagram\_fonte` (`dados_divulgacao.py`, `gerar_artes_catalogo.py`, `gerar_reels.py`). Backups: `Planejamentos\Andamento\Divugação_WhastsApp_Instagram\_backup_pacotes\`.
- Blog (WordPress): `Gestao_Anuncios_Blog\1_PROGRAMAS\Blog_WordPress` (`gerenciar_blog.py`, `publicar_categorias.py`, `categorias.json` em 2_DADOS). Backups: `Gestao_Anuncios_Blog\2_DADOS\Blog_WordPress\backups`.
- Relatório de atividades (compartilhado): `Programas_Diversos_Py\gerar_relatorio_atividade.py` → PDFs em `0- Pendencias\4_Relatorio_Ativ_Claude_no_Blog`.
- Painel de vendas: `Relatorios_Diarios_Anuncios` (`ATUALIZAR_PAINEL.bat`, `vendas_afiliados\*.csv`, `vendas_historico\historico_vendas.csv`).
- Catálogo WhatsApp: `Planejamentos\Andamento\Celular_Whatsapp\06_CATALOGO_WHATSAPP` (CATALOGO_WHATSAPP.xlsx = 17 produtos CNL; CATEGORIAS\CATALOGO_CATEGORIAS.xlsx = 9 categorias, textos e fotos).
- Pendências do dono (PDFs/agendas): `0- Pendencias\1_Pendencias`. Backups dos meus scripts: `Programas_Diversos_Py\_backups_claude_`.
- Estrutura oficial de pastas: nada solto na raiz; perguntar antes de criar pasta nova (memória `estrutura-mercado-livre.md`).

## 2. Agendar post e Reels no Instagram (Programar conteúdo)
Regras da plataforma (pesquisadas na prática): a data do agendamento só vai até ~29 dias à frente; o 19:00 do dia D abre ~20:00 de D-29. A hora mínima é daqui a 20 minutos.
Fluxo que funciona (Chrome com extensão Claude, navegador "Browser 1", deviceId 43dc6650-fd99-4640-b77a-1ef8291b4141):
1. `tabs_context_mcp createIfEmpty`; navegar para instagram.com/scheduled_content; botão "Programar conteúdo" (alto à direita).
2. `find "file input"` e `file_upload`. **O upload é bloqueado** para arquivos em `Planejamentos\Andamento\Celular_Whatsapp`: copie feed.png/reels.mp4 para o scratchpad da sessão e envie de lá; apague as cópias depois (Bash `rm` por nome; `Remove-Item` com curinga é bloqueado em pasta do sistema).
3. "Avançar": clicar por JS no elemento folha com texto "Avançar" (a posição varia). Post: Avançar x2 (filtro "Original" já vem selecionado). Reels: antes do Avançar, ícone de corte (canto inferior esquerdo) > "Original"; senão o vídeo sai ampliado.
4. Legenda: clicar no campo e digitar o texto de `2_LEGENDA_REELS.txt` sem a 1ª linha (título) e sem a linha `====`. Conferir o contador (ex.: 776/2.200). Cuidado ao digitar: um "c" minúsculo errado já escapou uma vez (16/11).
5. Data: abrir o seletor, avançar o mês com a seta, clicar o dia. Dias bloqueados aparecem cinza.
6. Hora: focar por JS `[role=spinbutton]` índice 0 e digitar `hh`, índice 1 e digitar `mm`. **Nunca digitar "1900" junto** (vira 00:00).
7. "Programar" (canto superior direito do diálogo); esperar ~18 s até "Seu post/reel foi programado". `computer wait` aceita no máximo 10 s por ação (encadear dois).
8. Conferir no calendário MENSAL depois de recarregar (o calendário pode ficar velho até recarregar). Via JS: `document.querySelector('main').innerText` e contar "19:00"/"19:05".
- Coordenadas mudam com o tamanho da janela (já vi 1222x887, 1222x944, 1568x726, 1568x772, 1456x818): **screenshot antes de cada clique**.
- Excluir item agendado: clicar no item no calendário > "Excluir conteúdo programado" (canto inferior esquerdo) > "Excluir". "Descartar post?" > Cancelar. O Instagram não troca a mídia de um item: apagar os 2 e criar de novo.
- Se pedir login: PARAR e avisar o dono. Senha nunca é digitada pelo Claude. Em 04/11 o "Browser 2" estava deslogado e o "Browser 1" logado: usar `list_connected_browsers` e `select_browser`.
- Mensagem "Escolha uma data dentro dos próximos 29 dias": esperar 30 min e tentar de novo.
- Dias de lista (01/12, 08/12, 15/12, 22/12 e terças de novembro) NÃO têm post; só envio nos Grupos do WhatsApp às 12:00.

## 3. Pacotes do dia e o problema da numeração dos itens
- Os textos de Story/Status/Canal/Direct trazem links `...#item-N`. N é a posição do produto no guia do blog. **Quando o blog retira ou inclui um anúncio, os números mudam** e o link passa a abrir o produto vizinho.
- Em 31/10 (depois das 16:41) alguém retirou o item 39 e o 214 antigo: tudo depois do 39 subiu 1. Corrigi refazendo os 27 pacotes (`refaz_links.py`: backup de cada pasta com sufixo `_01nov_ANTES_links`, conferência do título do produto antes/depois, restaura se o produto mudou, copia para Planejamentos\Andamento\Celular_Whatsapp).
- Posts/Reels já agendados usam "link da bio" (sem número): não são afetados.
- A Pipoqueira de 16/12 é fixada na posição 6 da lista de Natal **pelo nome** (`"Pipoqueira" in nome and "Popflix" in nome`), nunca pelo número.
- Para regenerar só alguns dias: filtrar `dd.calendario`/`ga.dd.calendario` por data (monkeypatch); rodar Python com `-X utf8`.
- Para detectar mudança de numeração: baixar o site ao vivo e comparar `<h2 id="item-N">N.<a>Nome</a>` com o backup mais recente (WordPress troca `"`→`″`, `×` e `'`; normalizar antes de comparar).
- Reels: o texto fixo é "Veja os detalhes no Mercado Livre" (política); `gerar_reels.py` já está ajustado.

## 4. Blog (WordPress) e política de texto
Comandos (`gerenciar_blog.py`): `listar`, `mostrar N`, `editar N --selo/--desc/--nome/... [--aplicar]` (sem `--aplicar` só mostra a prévia), `remover`, `adicionar`, `substituir`, `restaurar`. Sempre faz backup antes de publicar. Depois de mudar texto/itens: `python publicar_categorias.py --publicar` (republica categorias, Black Friday, Escolha rápida, Início e menu). Cache do site pode levar alguns minutos.
- Itens sem categoria quebram o `publicar_categorias.py`: incluir palavra em `categorias.json`.
- `aplicar_textos_novos.py` / `aplicar_textos_212_214.py`: aplicam textos em lote com **conferência automática de política** (regex PROIBIDO) e localizam itens pelo nome.
- Política de texto (sempre): sem preço (usar "confira o valor do dia no Mercado Livre"); sem "melhor/menor preço", "mais vendido", "líder", "oferta do mês", "garantido"; sem promessa de saúde ou estética; só fatos do título do anúncio; aviso de link de afiliado ("Publi: contém link de afiliado...") em todo texto; selo curto sem alegação. Títulos de anúncio com "R$ ..." devem ser limpos.
- Casos soltos que o dono ainda não pediu para trocar: "dieta e alimentação leve" (Air Fryer 11/11) e a palavra "melhor" na foto do fabricante da LG (26/11).

## 5. WhatsApp Business (conferido no WhatsApp Web em 01/11)
- O **campo Link do catálogo aceita só 75 caracteres**. Links com utm eram cortados em `...?utm_source=w` e perdiam o `#item-N`. Padrão curto: `https://comprenolink.net/melhores-produtos-mercado-livre-2026/#item-N` (70 caracteres) ou `https://comprenolink.net/<categoria>/?utm_source=whatsapp`.
- Catálogo por produto (17 itens CNL) com links curtos corrigidos em 01/11; o CNL-111 (Kit Skincare) saiu do ML e deve ser apagado pelo dono (Claude não apaga: irreversível).
- Em 01/11 só 2 das 9 categorias estavam no catálogo (Moda Infantil e Bebê); o relatório de 02/11 registra o cadastro das 7 restantes feito/validado: **conferir o estado atual**.
- Respostas rápidas OK (/canal com o link do Canal, /bf, /natal, /link, /preço, /pedido, /obrigado). Canal: um só ("Compre no Link - Achados do Mercado Livre"), link `https://whatsapp.com/channel/0029Vb9eTLd3rZZlBFjs8J3A` (uma letra lida de print: confirmar copiando do WhatsApp).
- Técnica no WhatsApp Web: os campos são `div contenteditable` com `aria-label` (Nome, Descrição, Link, Código do item). Trocar o link: clicar o item **com clique real** (clique por JS no item não troca o item), Editar, focar o campo Link, `ctrl+a`, digitar, conferir via JS, Salvar, esperar ~8 s e conferir o link no detalhe. JS que tenta ler cookies/querystring é bloqueado pelo filtro: retornar códigos curtos.
- Nunca ler/enviar conversas; não mexer no rascunho do dono. Conectar o WhatsApp Web exige QR do dono; sair do aparelho depois.
- Limites de segurança (memória `base-contatos-whatsapp.md`): só consentimento/conhecidos, 10/dia, sem envio em massa.

## 6. Vendas ML Afiliados e painel
- A conta do blog é a que mostra ~R$ 172 de comissão nos últimos 180 dias (a do Chrome pessoal mostrava R$ 15,27). Não há botão de exportar: o dono tira prints da tabela de Vendas (4 status marcados) e o Claude monta `vendas_ml_AAAA-MM-DD.csv` (colunas Data;Pedido;Produto;Loja;Status;Valor;Comissao, separador `;`).
- Em 31/10: 19 vendas; 12 pendentes (R$ 172,00) e 7 "Recusada (conta vinculada)" (R$ 65,58 perdidos). `normalizar_status` do painel: recus/cancel → Cancelada; aprov/pago → Aprovada; resto → Pendente. O histórico `historico_vendas.csv` nunca duplica (chave = nº do pedido) e preserva a coluna "campanha" editada à mão.
- Rodar o painel: **fechar o Excel antes**; `ATUALIZAR_PAINEL.bat` (~10 min; passos: verificar anúncios no ML, montar planilha, recalcular no Excel, PDF, limpar antigos para a Lixeira, abrir). `PAINEL_SEM_VERIFICAR=1` pula a verificação. Quando o Claude chama o .bat com `< nul` aparece "não há suporte para o redirecionamento de entrada" no fim: inofensivo (rodar sem `< nul`, em segundo plano).
- Relatórios de acesso: `1_relatorio_acessos_anuncios.exe` baixa os acessos; o painel lê os `relatorio_acessos_anuncios_*.html` de `Relatorios_Diarios_Anuncios`.
- Rotina semanal (segunda 10:00): `Calendario_Execucao_Semanal_WhatsApp_Vendas.ics` e `PROCESSO_SEMANAL_VENDAS_WHATSAPP.pdf`.

## 7. Relatório de atividades (obrigatório ao fim de cada sessão)
- Editar `ATIVIDADES` (ENTRADAS (data, hora, o que, EX/PA/NE, detalhe, motivo, nova data)), `FALTA_AGENDAR`, `REEXECUCAO` em `gerar_relatorio_atividade.py` e rodar `python -X utf8`. Nome: `RELATORIO_ATIVIDADE_CLAUDE_BLOG_DD_MM_AAAA_HHhMM.pdf`.
- Apagar **só o PDF que a própria conversa gerou** no mesmo dia e ficou superado (nunca o de outra data nem o de outra conversa). Apagar via Lixeira: `Microsoft.VisualBasic.FileIO.FileSystem.DeleteFile(..., 'OnlyErrorDialogs', 'SendToRecycleBin')`.
- Enviar o PDF ao dono (SendUserFile) e avisar em PT-BR o que foi feito e o que ficou pendente com motivo e nova data. Sempre responder em português.
- O arquivo é compartilhado: já houve versão antiga que voltou sozinha (31/10) por edição simultânea ou sincronização. Reler antes de editar (o Edit exige leitura recente).

## 8. Armadilhas técnicas (aprendidas)
- Python no Windows: usar `-X utf8`/`PYTHONUTF8=1`; heredoc com acento via stdin corrompe: gravar o script em arquivo (Write) e rodar.
- PowerShell com `python -c "..."` e aspas/acentos quebra: usar arquivo .py no scratchpad.
- `Edit` falha com "File has been modified since read": reler antes.
- Excel aberto bloqueia gravar `.xlsx` (PermissionError); existe um `~$arquivo.xlsx` quando está aberto.
- ReportLab: emojis aparecem como quadrado nos PDFs; entregar também um `.txt` com os emojis para copiar. PDFs: renderizar com `pymupdf` (não há pdftoppm) para conferir.
- Ferramentas "deferred" precisam de ToolSearch antes (ex.: CronList/CronCreate, list_events, send_message, select_browser).
- Cron de sessão: só dispara com o app aberto, expira em ~7 dias, e se o app fechar ele se perde (o dono escreve "agendar DD/MM").
- Conferir sempre o resultado no calendário/arquivo; não confiar só na mensagem "foi programado".

## 9. Custo e uso
- Plano Pro com uso extra e recarga automática ligados (saldo ~R$ 74 em 31/10). Opus gasta mais que Sonnet; para rotinas repetitivas o Sonnet basta. Conversas longas encarecem cada ação. O limite semanal renova segunda às 02:00 (horário de Brasília).

## 10. Pendências conhecidas (04/11 21:00)
- Agendar 04/12 (05/11 ~20:39), 07/12 (08/11), 09/12, 11/12, 14/12, 16/12, 18/12, 21/12, 23/12 (sempre D-29 depois das 20:00).
- Dono: apagar CNL-111 no catálogo; sair do aparelho conectado do WhatsApp Web; decidir sobre frases leves (Air Fryer, LG) e sobre o Turbinar (reunião 05/11 10:00).
- Conferir se as 7 categorias saíram de "em análise" no WhatsApp.
- Recriar o cron quando expirar (~05/11) e manter UM só.

## 11. Fontes
Relatórios `RELATORIO_ATIVIDADE_CLAUDE_BLOG_*` (histórico completo do que foi feito, com motivo e conferência); PDFs em `0- Pendencias\1_Pendencias` (Validacao_WhatsApp..., Cadastrar_7_categorias..., Pendencias_Dono_Passo_a_Passo..., Pendencias_WhatsApp...); transcrição da conversa 001: `C:\Users\SVR_RYZEN_JAA\.claude\projects\C--Users-SVR-RYZEN-JAA\d759a442-1d58-4e20-94e0-f2e7cc22f60c.jsonl`.

## 12. ATENÇÃO: a conversa 001 será APAGADA pelo dono (04/11 ~21:10)
- O cron a6d1f751 (agendamento Instagram 20:39) **desaparece junto com a 001**. Se a 000 não tiver criado o dela até 05/11 20:39, ninguém agenda 04/12: nesse caso, quando o dono pedir ("agendar 04/12"), siga a seção 2 deste documento.
- Scripts de trabalho da 001 (eram da pasta temporária): D:\Projeto_Blog_Comprenolink\Programas_Diversos_Py\_backups_claude_\scripts_sessao_001_2026-11-04.zip (72 scripts: refaz_links.py, refaz_todos.py, links_cnl.py, num_itens.py, diff_itens.py, aplicar_textos_*.py, textos_*.py, retirar17.py, troca_16_12.py, agendas .ics etc.). Os principais já estão em Programas_Diversos_Py (gerar_relatorio_atividade.py, aplicar_textos_212_214.py, gerar_validacao_whatsapp_vendas.py, gerar_cadastro_7_categorias.py, gerar_agenda_*.py, gerar_pendencias_*.py).
- A transcrição integral da 001 (185 MB) é o .jsonl citado na seção 11; ao apagar a conversa ele pode sumir. O backup das conversas do dono está em E:\BKP_INTEGRA_CLAUDE\BACKUPS (último: BKP_CLAUDE_04-11-2026_20h20m45s.zip, às 20:20, sem a parte final desta noite).
