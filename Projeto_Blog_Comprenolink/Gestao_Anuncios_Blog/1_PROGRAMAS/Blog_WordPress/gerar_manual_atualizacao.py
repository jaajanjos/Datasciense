# -*- coding: utf-8 -*-
"""Gera PROCESSO_DE_ATUALIZACAO_MANUTENCAO.pdf: como recompilar, validar e levar os painéis para o outro PC
sem a senha sair do lugar (processo criado em 29/10/2026)."""
import os

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, PageBreak, SimpleDocTemplate, Spacer, Table, TableStyle

# Mesmo visual dos outros manuais
from gerar_manual_pdf import (AMARELO, AZUL, CINZA, LINHA, VERDE, VERMELHO, P, base, caixa, capa_s, capa_t, cod, h1, h2,
                              lista, passo, peq, tela)

PASTA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(PASTA, "..", ".."))  # pasta Manutenção_Blog
SAIDA = os.path.join(RAIZ, "PROCESSO_DE_ATUALIZACAO_MANUTENCAO.pdf")  # sempre na raiz, junto dos atalhos
TITULO = "Processo de Atualização - Manutenção dos Blogs"


def tabela(linhas, larguras):
    dados = [[P(f"<b>{c}</b>", peq) for c in linhas[0]]] + [[P(c, peq) for c in l] for l in linhas[1:]]
    t = Table(dados, colWidths=[w * cm for w in larguras], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F0FA")), ("GRID", (0, 0), (-1, -1), 0.5, LINHA),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(CINZA)
    canvas.drawString(2 * cm, 1.2 * cm, TITULO)
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def montar():
    s = []
    # ------------------------------------------------------------------ capa
    s += [Spacer(1, 5 * cm), P("PROCESSO DE ATUALIZAÇÃO", capa_t), P("MANUTENÇÃO DOS BLOGS", capa_t), Spacer(1, 0.6 * cm),
          P("CentralBlog.exe, PainelBlog.exe e o pacote do outro PC", capa_s),
          P("Como recompilar, validar e atualizar sem a senha sair do lugar", capa_s), Spacer(1, 1.2 * cm),
          P(f"Pasta: {RAIZ}", capa_s), P("Versão de 29/10/2026 (pasta atualizada em 04/11/2026)", capa_s), Spacer(1, 3 * cm),
          caixa("Resumo em 3 linhas", [
              "<b>Mudou programa neste PC?</b> Rode o GERAR_EXE.bat (faz tudo e valida).",
              "<b>Atualizar o outro PC?</b> Leve o 4_ATUALIZAR_OUTRO_PC.zip, extraia e rode ATUALIZAR_AQUI.bat.",
              "<b>PC novo, sem o painel?</b> Use o 4_PACOTE_OUTRO_PC.zip (instalação do zero)."], VERDE),
          PageBreak()]

    # ------------------------------------------------------------------ 1. visão geral
    s += [P("1. Visão geral", h1),
          P("Existem dois lugares onde os painéis rodam. Cada um tem a <b>sua própria senha de aplicativo</b> do WordPress, "
            "guardada só na pasta de dados daquele computador."), Spacer(1, 6),
          tabela([["", "Este PC (Manutenção_Blog)", "Outro PC (pacote)"],
                  ["Programas", "CentralBlog.exe (todos os botões) + .py em 1_PROGRAMAS", "PainelBlog.exe + painel das máquinas (.html)"],
                  ["Senha", "2_DADOS\\Blog_WordPress\\wp_credenciais.json (senha \"Painel Blog\")",
                   "2_DADOS\\Blog_WordPress\\wp_credenciais.json do pacote (senha \"Painel Blog PC2\")"],
                  ["Backups", "2_DADOS\\Blog_WordPress\\backups (+ backup automático a cada 30 min)",
                   "2_DADOS\\Blog_WordPress\\backups do pacote (só antes de publicar)"],
                  ["Automático", "Categorias a cada 3 h + backup a cada 30 min", "Nenhum"]], [2.6, 6.9, 6.9]),
          Spacer(1, 10), P("Arquivos deste processo", h2),
          tabela([["Arquivo", "Para que serve"],
                  ["1_PROGRAMAS\\Blog_WordPress\\GERAR_EXE.bat", "Faz TUDO: recompila os 2 .exe, monta os 2 zips sem senha e valida."],
                  ["1_PROGRAMAS\\Blog_WordPress\\montar_pacote.py", "Usado pelo GERAR_EXE: tira senha do pacote, refaz o zip de instalação e gera o zip de atualização."],
                  ["4_VALIDAR_ESTRUTURA.bat (ou CentralBlog > Validar)", "Confere estrutura, senha, zips, .exe atualizados e conexão (só leitura)."],
                  ["4_PACOTE_OUTRO_PC.zip", "Instalação do ZERO num PC que ainda não tem o painel. Vai sem senha."],
                  ["4_ATUALIZAR_OUTRO_PC.zip", "ATUALIZAÇÃO do outro PC: só programas, sem a pasta 2_DADOS, com o ATUALIZAR_AQUI.bat."],
                  ["3_DOCUMENTACAO\\RELATORIO_VALIDACAO_*.txt", "Resultado de cada validação."],
                  ["PROCESSO_DE_ATUALIZACAO_MANUTENCAO.pdf (raiz)", "Este documento. Fica sempre na raiz da Manutenção_Blog."]],
                 [6.4, 10.0]),
          Spacer(1, 10),
          caixa("Regra de ouro", [
              "A senha (wp_credenciais.json) fica <b>somente</b> em 2_DADOS\\Blog_WordPress de cada PC.",
              "Ela <b>nunca</b> vai dentro de 4_PACOTE_OUTRO_PC, do 4_PACOTE_OUTRO_PC.zip nem do 4_ATUALIZAR_OUTRO_PC.zip. "
              "A validação acusa FALHA se isso acontecer, e o GERAR_EXE.bat limpa sozinho."], AMARELO),
          PageBreak()]

    # ------------------------------------------------------------------ 2. processo A
    s += [P("2. Processo A - Depois de mudar um programa (neste PC)", h1),
          P("Use sempre que algum .py de 1_PROGRAMAS mudar (painel, gerenciar_blog, central, validação) ou o painel das máquinas."),
          Spacer(1, 8),
          passo(1, "Feche os painéis abertos", lista([
              "Feche o CentralBlog e a janela preta do painel do WordPress, se estiverem abertos.",
              "Se esquecer, o GERAR_EXE avisa \"feche o CentralBlog e rode de novo\"."])),
          passo(2, "Rode o GERAR_EXE.bat", [P("Duplo clique em <b>1_PROGRAMAS\\Blog_WordPress\\GERAR_EXE.bat</b>. Ele mostra 5 passos:")] + lista([
              "<b>[1/5]</b> gera o PainelBlog.exe dentro de 4_PACOTE_OUTRO_PC",
              "<b>[2/5]</b> gera o CentralBlog.exe (numa pasta temporária) e copia para a raiz",
              "<b>[3/5]</b> copia o painel das máquinas para o pacote",
              "<b>[4/5]</b> tira qualquer senha do pacote, refaz o 4_PACOTE_OUTRO_PC.zip e gera o 4_ATUALIZAR_OUTRO_PC.zip",
              "<b>[5/5]</b> roda a validação completa"])),
          passo(3, "Confira a última linha", [tela([
              "[4/5] Limpando senha do pacote e refazendo o .zip...",
              "  4_PACOTE_OUTRO_PC.zip refeito (9.2 MB, sem senha)",
              "  4_ATUALIZAR_OUTRO_PC.zip gerado (9.2 MB, versão 29/10/2026 07h23, só programas, sem 2_DADOS)",
              "[5/5] Validando a organização...",
              "RESULTADO: TUDO CERTO  (1 aviso(s))",
              "Pronto: CentralBlog.exe, PainelBlog.exe e 4_PACOTE_OUTRO_PC.zip atualizados e validados."], quebra=True),
              Spacer(1, 4),
              P("Se aparecer <b>ATENCAO: algum passo deu erro</b>, leia as mensagens acima dela e veja a tabela do capítulo 5.")]),
          Spacer(1, 6),
          caixa("O que acontece com a senha no passo [4/5]", [
              "Se achar um wp_credenciais.json dentro do pacote:",
              "&bull; a pasta principal está sem senha: ele <b>move</b> a senha para 2_DADOS\\Blog_WordPress;",
              "&bull; é igual à da pasta principal: <b>apaga</b> a cópia do pacote;",
              "&bull; é diferente: guarda em 2_DADOS\\Blog_WordPress\\wp_credenciais_do_pacote_DATA.json.bak e avisa (confira e apague)."], VERDE),
          PageBreak()]

    # ------------------------------------------------------------------ 3. processo B
    s += [P("3. Processo B - Atualizar o outro PC (já tem o painel)", h1),
          P("Só troca os programas. A senha, os backups e os dados das máquinas (pasta 2_DADOS) <b>não são tocados</b> "
            "e nada é apagado."), Spacer(1, 8),
          passo(1, "Leve o zip de atualização", lista([
              f"Copie <b>{os.path.join(RAIZ, '4_ATUALIZAR_OUTRO_PC.zip')}</b> para o pendrive (ou mande por e-mail).",
              "Não use o 4_PACOTE_OUTRO_PC.zip para atualizar: ele é para instalação do zero."])),
          passo(2, "Extraia no outro PC", lista([
              "Botão direito no .zip &gt; <b>Extrair tudo...</b> &gt; Extrair (pode ser na Área de Trabalho).",
              "Fica uma pasta ATUALIZAR_OUTRO_PC com: ATUALIZAR_AQUI.bat, LEIA-ME_ATUALIZAR.txt, arquivos\\ e modelo\\."])),
          passo(3, "Rode o ATUALIZAR_AQUI.bat", lista([
              "Ele procura a pasta do painel sozinho: C:\\4_PACOTE_OUTRO_PC, C:\\Blog_Manutencao, D:\\4_PACOTE_OUTRO_PC, "
              "Área de Trabalho e Documentos.",
              "Se não achar, <b>arraste a pasta do painel</b> (a que tem 2_ABRIR_PAINEL_BLOG_WORDPRESS.bat) para a janela e aperte Enter.",
              "Confira a pasta mostrada e responda <b>S</b>. Com N, nada é alterado."]) + [Spacer(1, 4), tela([
              "  ATUALIZAR OS PAINEIS DOS BLOGS  (versao 29/10/2026 07h23)",
              "  Troca so os programas. NAO mexe na senha nem nos backups.",
              "Pasta do painel: C:\\4_PACOTE_OUTRO_PC",
              "Senha deste PC: encontrada, sera mantida",
              "Atualizar agora? (S/N): S",
              "Fechando o painel do WordPress, se estiver aberto...",
              "Copiando os programas novos...",
              "PRONTO: programas atualizados para a versao 29/10/2026 07h23.",
              "Senha e backups: mantidos."], quebra=True)]),
          passo(4, "Confira o painel", lista([
              "Abra o <b>2_ABRIR_PAINEL_BLOG_WORDPRESS.bat</b>: deve aparecer \"Conectado\" e a lista de produtos, sem pedir senha.",
              "Se o Windows mostrar \"O Windows protegeu o computador\": <b>Mais informações &gt; Executar assim mesmo</b> "
              "(normal com .exe novo)."])),
          passo(5, "Limpe", lista(["Pode apagar a pasta extraída e o .zip da atualização."])),
          Spacer(1, 4),
          caixa("Proteções da rotina", [
              "&bull; Recusa pasta errada (sem o atalho 2) e a própria pasta da atualização: \"Nada foi alterado\".",
              "&bull; Copia com robocopy sem apagar nada e pulando 2_DADOS inteiro e qualquer wp_credenciais.json.",
              "&bull; Cria 2_DADOS\\Blog_Maquinas, backups e o modelo wp_credenciais.exemplo.json só se estiverem faltando.",
              "&bull; Testada num PC simulado: senha, backup e dados das máquinas ficaram idênticos; o .exe foi trocado."], VERDE),
          Spacer(1, 14)]

    # ------------------------------------------------------------------ 4. processo C
    s += [P("4. Processo C - Instalar num PC novo (do zero)", h1),
          passo(1, "Copie e extraia", lista([
              "Leve o <b>4_PACOTE_OUTRO_PC.zip</b>, botão direito &gt; Extrair tudo &gt; por exemplo em C:\\.",
              "Confira que aparecem os atalhos 1_ e 2_ e as pastas 1_PROGRAMAS, 2_DADOS e 3_DOCUMENTACAO."])),
          passo(2, "Crie a senha própria do PC", lista([
              "wp-admin &gt; Usuários &gt; Perfil &gt; Senhas da aplicação &gt; nome <b>Painel Blog PC2</b> (ou PC3...).",
              "Abra o atalho 2 e cole: usuário <b>compre.no.link26@gmail.com</b>, a senha de 24 letras e página 5.",
              "Passo a passo completo: LEIA-ME_COMO_INSTALAR_NO_OUTRO_PC.txt (passo 3)."])),
          passo(3, "Próximas vezes", lista(["Daí em diante, para atualizar, use sempre o Processo B."])),
          Spacer(1, 6),
          caixa("Não faça", [
              "&bull; Não apague a pasta do outro PC para extrair o zip do zero: a senha PC2 e os backups se perdem.",
              "&bull; Não extraia um zip dentro da pasta antiga: cria uma subpasta 4_PACOTE_OUTRO_PC e mistura as cópias.",
              "&bull; Não use o painel do WordPress nos dois PCs ao mesmo tempo: o último a publicar sobrescreve o outro."], VERMELHO),
          Spacer(1, 12),

          # -------------------------------------------------------------- 5. validação
          P("5. Validação e o que fazer em cada resultado", h1),
          P("Rode o <b>4_VALIDAR_ESTRUTURA.bat</b> (ou CentralBlog &gt; Validar). O GERAR_EXE.bat já roda no fim. "
            "Cada linha sai como <b>[OK]</b>, <b>[AVISO]</b> (atenção, não impede) ou <b>[FALHA]</b> (corrigir)."), Spacer(1, 6),
          tabela([["Mensagem", "Causa", "O que fazer"],
                  ["[FALHA] wp_credenciais.json não deveria estar no pacote",
                   "A senha foi salva dentro de 4_PACOTE_OUTRO_PC.", "Rode o GERAR_EXE.bat (passo [4/5] tira a senha e refaz os zips)."],
                  ["[FALHA] nenhuma cópia extra do arquivo de senha",
                   "Existe outro wp_credenciais.json fora de 2_DADOS\\Blog_WordPress.", "Rode o GERAR_EXE.bat; se for fora do pacote, apague a cópia."],
                  ["[AVISO] wp_credenciais.json ainda não existe",
                   "A pasta principal está sem senha.", "Abra o atalho 3 e cole a senha de aplicativo (ou o GERAR_EXE move a do pacote)."],
                  ["[AVISO] atualização automática ... Faltam as credenciais",
                   "A tarefa de 3 em 3 h rodou sem senha.", "Corrija a senha; o aviso some na próxima rodada automática."],
                  ["[AVISO] ...zip atualizado com a pasta  &lt;- refaça",
                   "O pacote mudou depois do zip.", "Rode o GERAR_EXE.bat."],
                  ["[FALHA] ...exe gerado depois da última mudança nos .py",
                   "Um .py mudou e o .exe ficou velho.", "Rode o GERAR_EXE.bat."],
                  ["[FALHA] painel do pacote ... salva senha no 2_DADOS principal",
                   "A regra de pasta do gerenciar_blog.py foi alterada.", "Restaurar a função pasta_dados_de (capítulo 7)."],
                  ["ATENCAO: algum passo deu erro (GERAR_EXE)",
                   "Programa aberto, PyInstaller ou cópia falhou.", "Feche CentralBlog/painel e rode de novo; leia a mensagem do passo."]],
                 [5.6, 5.0, 5.8]),
          PageBreak()]

    # ------------------------------------------------------------------ 6. incidente
    s += [P("6. O que aconteceu em 29/10/2026 (por que este processo existe)", h1),
          tabela([["Hora", "Fato"],
                  ["06:47", "Atualização automática das categorias OK (senha na pasta principal)."],
                  ["06:55", "PainelBlog.exe do pacote recompilado."],
                  ["06:57", "Senha salva em 4_PACOTE_OUTRO_PC\\2_DADOS\\Blog_WordPress (painel do pacote aberto neste PC); "
                            "a pasta principal ficou sem senha."],
                  ["07:07 / 07:08", "Atualização automática falhou: \"Faltam as credenciais\"."],
                  ["07:08", "4_PACOTE_OUTRO_PC.zip refeito COM a senha dentro."],
                  ["07:09", "Validação: 2 FALHAS e 3 avisos."],
                  ["07:12", "Senha devolvida para 2_DADOS e zip refeito sem senha: TUDO CERTO."],
                  ["07:16 a 07:23", "Correção definitiva, GERAR_EXE completo e zip de atualização do outro PC testados."],
                  ["07:30", "Tarefa automática rodada de novo pelo Agendador: PUBLICADO (195 produtos, 9 categorias, "
                            "Black Friday, Escolha rápida, Início e menu). O aviso da validação sumiu."]], [3.0, 13.4]),
          Spacer(1, 4),
          P("Para não esperar as 3 h depois de corrigir a senha: Agendador de Tarefas &gt; \"Atualizar categorias blog "
            "comprenolink\" &gt; Executar (só publica se o guia ou as categorias mudaram).", peq),
          Spacer(1, 8), P("Causa", h2),
          P("O PainelBlog.exe grava a senha na pasta 2_DADOS ao lado dele. Aberto de dentro de 4_PACOTE_OUTRO_PC neste PC, "
            "a senha foi parar no pacote, e o zip feito em seguida levou a senha junto."),
          P("Correção definitiva", h2),
          lista(["O painel do pacote, quando está dentro da Manutenção_Blog, usa o 2_DADOS <b>principal</b>. "
                 "Copiado para o outro PC, usa o 2_DADOS dele (sem mudança lá).",
                 "O GERAR_EXE.bat faz todos os passos sozinho, limpa senha do pacote e valida no fim.",
                 "Novo 4_ATUALIZAR_OUTRO_PC.zip: atualização do outro PC sem risco de apagar senha ou backup.",
                 "Validação ganhou 3 conferências: regra de pasta do pacote, zip de atualização sem dados, zip de atualização em dia."]),
          Spacer(1, 6),
          caixa("Segurança: zip das 07:08", [
              "O 4_PACOTE_OUTRO_PC.zip das 07:08 tinha a senha deste PC. Se ele foi copiado para pendrive, outro PC ou e-mail: "
              "apague a cópia e troque a senha de aplicativo \"Painel Blog\" (wp-admin &gt; Usuários &gt; Perfil &gt; "
              "Senhas da aplicação &gt; Revogar &gt; criar nova &gt; colar no atalho 3).",
              "No outro PC, não reaproveite um wp_credenciais.json vindo desse zip: crie a senha própria do PC2."], VERMELHO),
          PageBreak()]

    # ------------------------------------------------------------------ 7. referência técnica
    s += [P("7. Referência técnica (para manutenção dos programas)", h1),
          P("gerenciar_blog.py - escolha da pasta de dados", h2),
          lista(["<b>BLOG_WP_DADOS</b> (variável definida pelo CentralBlog) tem prioridade.",
                 "<b>pasta_dados_de(pasta_programa)</b>: se a pasta acima de 1_PROGRAMAS se chama 4_PACOTE_OUTRO_PC e a pasta "
                 "de cima tem 2_DADOS\\Blog_WordPress, usa essa (pacote dentro da Manutenção_Blog). Senão usa "
                 "..\\..\\2_DADOS\\Blog_WordPress e, sem ela, a própria pasta do programa.",
                 "Testado em 3 cenários: pasta principal, pacote neste PC e pacote solto (outro PC)."]),
          P("montar_pacote.py", h2),
          lista(["limpar_senhas(): move / apaga / guarda como .json.bak (ver capítulo 2).",
                 "refazer_zip(): 4_PACOTE_OUTRO_PC.zip sem wp_credenciais.json; se a senha entrar, mantém o zip antigo e dá ERRO.",
                 "gerar_atualizacao(): 4_ATUALIZAR_OUTRO_PC.zip com ATUALIZAR_OUTRO_PC\\{ATUALIZAR_AQUI.bat, LEIA-ME_ATUALIZAR.txt, "
                 "modelo\\, arquivos\\ = pacote sem 2_DADOS}. O texto do .bat fica em BAT_ATUALIZAR e é gravado com quebra CRLF."]),
          P("ATUALIZAR_AQUI.bat (roda no outro PC)", h2),
          tela(['robocopy "arquivos" "<pasta do painel>" /E /XD 2_DADOS /XF wp_credenciais.json',
                "  (sem /MIR: não apaga nada; antes: taskkill /im PainelBlog.exe)"], quebra=True),
          P("validar_estrutura.py - conferências novas", h2),
          lista(["painel do pacote, rodando neste PC, salva senha e backups no 2_DADOS principal",
                 "4_ATUALIZAR_OUTRO_PC.zip só com programas (sem 2_DADOS nem senha)",
                 "4_ATUALIZAR_OUTRO_PC.zip atualizado com a pasta"]),
          P("Cuidados ao editar", h2),
          lista(["Arquivos .bat precisam de quebra de linha <b>CRLF</b> (Windows). Com LF o cmd corta os comandos "
                 "(\"'ho' não é reconhecido...\"). O GERAR_EXE.bat já está em CRLF.",
                 "Backups de .py não podem ficar em 2_DADOS (a validação acusa): use extensão .py.bak.",
                 "Depois de mudar qualquer .py: GERAR_EXE.bat. Refazer este PDF: python gerar_manual_atualizacao.py."]),
          ]
    return s


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=2.3 * cm, rightMargin=2.3 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                            title=TITULO, author="Blog comprenolink.net")
    plano = [f for x in montar() for f in (x if isinstance(x, list) else [x])]  # lista() devolve vários parágrafos
    doc.build(plano,onFirstPage=lambda c, d: None, onLaterPages=rodape)
    print("PDF gerado:", SAIDA)


if __name__ == "__main__":
    main()
