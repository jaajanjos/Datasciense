# -*- coding: utf-8 -*-
"""Gera DOCUMENTACAO_ATUALIZA_ANUNCIOS_DD_MM_AAAA.pdf: como executar, fluxo, arquivos, validação, riscos e atenção.
Rodar de novo sempre que algum programa desta pasta mudar:  python gerar_documentacao_pdf.py"""
import os
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import CondPageBreak, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

AQUI = os.path.dirname(os.path.abspath(__file__))
HOJE = datetime.now()
SAIDA = os.path.join(AQUI, HOJE.strftime("DOCUMENTACAO_ATUALIZA_ANUNCIOS_%d_%m_%Y.pdf"))
F = r"C:\Windows\Fonts"
pdfmetrics.registerFont(TTFont("Arial", os.path.join(F, "arial.ttf")))
pdfmetrics.registerFont(TTFont("Arial-B", os.path.join(F, "arialbd.ttf")))
AZUL, AZUL_C, LAR, VERM, VERDE = (colors.HexColor(c) for c in ("#2d3277", "#e8eaf6", "#e67e22", "#c0392b", "#1e8449"))
ST = {
    "t": ParagraphStyle("t", fontName="Arial-B", fontSize=18, leading=22, textColor=AZUL, spaceAfter=4),
    "h1": ParagraphStyle("h1", fontName="Arial-B", fontSize=13.5, leading=17, textColor=AZUL, spaceBefore=8, spaceAfter=5),
    "h2": ParagraphStyle("h2", fontName="Arial-B", fontSize=11, leading=14, textColor=LAR, spaceBefore=6, spaceAfter=3),
    "p": ParagraphStyle("p", fontName="Arial", fontSize=9.6, leading=13, spaceAfter=4),
    "c": ParagraphStyle("c", fontName="Arial", fontSize=8.6, leading=11),
    "cb": ParagraphStyle("cb", fontName="Arial-B", fontSize=8.6, leading=11, textColor=colors.white),
    "mono": ParagraphStyle("m", fontName="Courier", fontSize=8.2, leading=10.5, backColor=colors.HexColor("#f4f6f8"),
                           borderPadding=4, spaceAfter=6),
}


def P(t, s="p"):
    return Paragraph(t, ST[s])


def tab(cab, linhas, larg, cor=AZUL):
    dados = [[P(c, "cb") for c in cab]] + [[P(str(x), "c") for x in l] for l in linhas]
    t = Table(dados, colWidths=[w * cm for w in larg], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), cor), ("VALIGN", (0, 0), (-1, -1), "TOP"),
                           ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#b0b7c3")),
                           ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, AZUL_C]),
                           ("LEFTPADDING", (0, 0), (-1, -1), 4), ("RIGHTPADDING", (0, 0), (-1, -1), 4)]))
    return t


def rodape(c, d):
    c.saveState()
    c.setFont("Arial", 7.5)
    c.setFillColor(colors.grey)
    c.drawString(1.6 * cm, 1.0 * cm, "comprenolink.net · Atualização automática dos anúncios")
    c.drawRightString(A4[0] - 1.6 * cm, 1.0 * cm, f"Página {d.page} · gerado em {HOJE:%d/%m/%Y %H:%M}")
    c.restoreState()


def main():
    s = []
    s += [P("Atualização automática dos anúncios", "t"),
          P(f"Guia de uso, riscos e pontos de atenção · versão de {HOJE:%d/%m/%Y}"),
          P("<b>Para que serve:</b> todo dia, num só comando, verificar no Mercado Livre os anúncios do guia "
            "(pausados, removidos e outras situações fora do normal), gerar o relatório de acessos "
            "(relatorio_acessos_anuncios_AAAA-MM-DD_HHhMM.html), <b>substituir com a IA do Claude</b> os anúncios "
            "fora do ar, trocar no blog e terminar com o painel de conversão (Painel_conversao_performance_….pdf) e a "
            "planilha de controle atualizados."),
          P("<b>Combinado com o dono (09/11/2026):</b> a substituição é automática, sem aprovação prévia; o dono "
            "<b>valida depois</b> cada link e produto trocado e, se houver erro, corrige pelos programas.")]

    s += [P("1. Antes de executar (pré-requisitos)", "h1"),
          tab(["#", "O que precisa estar pronto", "Por quê"], [
              ["1", "PC ligado, internet e Python (já instalado).", "Todos os programas são Python."],
              ["2", "<b>Claude Code logado</b> neste PC. Em 09/11/2026 o login estava <b>expirado</b>: abra um "
                    "terminal, digite <font name='Courier'>claude</font> e siga o <font name='Courier'>/login</font> "
                    "(uma vez; vale por semanas).", "É o Claude que escolhe o substituto e gera o meli.la (etapa 3)."],
              ["3", "<b>Google Chrome aberto</b> com a <b>extensão Claude</b> conectada e <b>logado no ML "
                    "Afiliados</b> (o Claude não digita senha).", "Só o seu Chrome logado consegue gerar o link "
                    "de afiliado; sem ele o ML pede captcha/login."],
              ["4", "Planilha <b>Painel de  Controle de Acesso.xlsx fechada</b> no Excel.", "Com ela aberta o "
                    "painel não consegue gravar."],
              ["5", "Ter uso disponível no plano do Claude.", "A etapa 3 consome o seu plano (sem custo de API)."],
          ], [0.8, 10.2, 6.6])]

    s += [P("2. Como executar", "h1"),
          P("Clique duplo em <b>0_MENU_ATUALIZA_ANUNCIOS.bat</b> (nesta pasta) e escolha a opção:"),
          tab(["Opção", "O que faz", "Quando usar", "Tempo"], [
              ["1", "TUDO: verifica os 213 anúncios no ML, relatório, substituição com o Claude, troca no blog, "
                    "relatório final e painel", "Rotina do dia (recomendado)", "30 a 60 min"],
              ["2", "TUDO, usando a última verificação do ML", "Já verificou há pouco", "15 a 40 min"],
              ["3", "Só relatório + painel (sem substituição)", "Sem Chrome/Claude disponível", "~12 min"],
              ["4", "Só verificar no ML e gerar o relatório", "Quer só ver a situação", "~10 min"],
              ["5", "Só a lista do que precisa de substituto", "Conferir pendências", "segundos"],
              ["6", "Só substituir com o Claude e trocar no blog", "Depois da opção 4/5", "5 a 10 min por item"],
              ["7", "Só painel (PDF + planilha) e resumo", "Depois de trocar à mão", "~2 min"],
              ["8", "SIMULAÇÃO: não chama o Claude, não publica, não roda o painel", "Testar após qualquer mudança",
               "~1 min"],
              ["R / H / L / D", "Abrir: resumo, histórico das trocas, último log, esta documentação", "Validação", "—"],
          ], [2.2, 8.0, 4.6, 2.8]),
          P("Sem menu (para colocar no seu menu geral), o comando equivalente da opção 1 é:", "p"),
          P(r'python -X utf8 "D:\Projeto_Blog_Comprenolink\Relatorios_Diarios_Anuncios\atualiza_automatica_py_anuncios'
            r'\0_executar_tudo.py"', "mono"),
          P("Opções: <font name='Courier'>--sem-verificar</font> (usa a última verificação), "
            "<font name='Courier'>--sem-claude</font> (sem substituição), <font name='Courier'>--simular</font> "
            "(nada é publicado). Ou chame o próprio menu: <font name='Courier'>0_MENU_ATUALIZA_ANUNCIOS.bat</font>.")]

    s += [PageBreak(), P("3. O que acontece em cada etapa", "h1"),
          tab(["Etapa", "Programa", "O que faz", "Se der erro"], [
              ["1", "1_verificar_e_relatorio.py", "Roda o 3_relatorio_acessos_anuncios.py do painel: verifica cada "
               "anúncio no ML (ativo/pausado/removido) e gera o relatório HTML em _historico_relatorios.",
               "Para tudo; nada é alterado no blog."],
              ["2", "2_pendencias_substituicao.py", "Lista quem precisa de substituto (mesma regra do quadro do "
               "relatório), com faixa de preço ±20% e links de busca → pendencias_substituicao.json.",
               "Para tudo; nada é alterado."],
              ["3", "3_substituir_com_claude.py", "Chama o Claude Code com o roteiro_substituicao_claude.md: no seu "
               "Chrome, escolhe o substituto pela melhor política de venda, gera e confere o meli.la e grava "
               "substituicoes_aprovadas.json. Depois o programa VALIDA cada troca.", "Pula a troca no blog e "
               "atualiza só o painel."],
              ["4", "4_aplicar_no_blog.py", "Acha o item pelo LINK ANTIGO (o número muda), troca nome, link, selo, "
               "descrição, benefícios, ideal para, título e foto pelo gerenciar_blog.py, que faz backup da página "
               "antes de publicar. Registra tudo em historico_substituicoes.csv.", "O item com erro fica "
               "registrado; os outros seguem."],
              ["5", "5_painel_e_resumo.py", "Se houve troca, gera o relatório de novo verificando os links novos; "
               "roda o ATUALIZAR_PAINEL.bat (planilha + PDF) e grava resumo_ultima_execucao.txt.",
               "Resumo indica 'COM ERRO'; veja o log."],
          ], [1.3, 4.0, 8.4, 3.9]),
          P("Validação automática da etapa 3 (antes de qualquer publicação)", "h2"),
          P("Uma troca só é aplicada se: tem todos os campos; o item está na lista de pendentes; o link antigo "
            "confere; o link novo é <b>https://meli.la/…</b> e é <b>diferente do antigo</b> (armadilha do catálogo); "
            "a foto é https; o item não está repetido. Na etapa 4, também é pulada a troca cujo link novo já existe "
            "em outro item do guia. O que for recusado aparece em 'Não substituídos' com o motivo.")]

    s += [P("4. Sua validação depois de cada execução", "h1"),
          tab(["Passo", "Como"], [
              ["1", "Menu → <b>R</b> (resumo): veja 'Trocas publicadas hoje' e 'Não substituídos'."],
              ["2", "Menu → <b>H</b> (historico_substituicoes.csv): para cada troca, abra o link novo e confira "
                    "produto, preço, vendedor e se o anúncio está ativo."],
              ["3", "Abra o guia no site (item trocado) e confira foto, título e textos. Itens com cartão do plugin "
                    "Hostinger aparecem com 'confira foto/título/preço do cartão' na coluna 'conferir'."],
              ["4", "Se algo estiver errado: corrija pelo <b>gerenciar_blog.py</b> (editar o item ou restaurar o "
                    "backup da página em Gestao_Anuncios_Blog\\2_DADOS\\Blog_WordPress\\backups) ou peça ao Claude."],
              ["5", "Os anúncios que não foram substituídos continuam no quadro 'Precisam de substituto' do relatório "
                    "e do painel; rodam de novo na próxima execução."],
          ], [1.4, 16.2])]

    s += [PageBreak(), P("5. Riscos e pontos de atenção", "h1"),
          tab(["Risco", "Nível", "O que pode acontecer", "Como evitamos / o que fazer"], [
              ["Bloqueio no Mercado Livre", "MÉDIO", "Muitas buscas seguidas podem gerar captcha ou alerta na conta.",
               "Ritmo humano, uma página por vez, só no seu Chrome logado; sem senha, sem burlar captcha; no máximo "
               "10 trocas por rodada (config_atualiza.json). Se aparecer captcha, o Claude para e registra."],
              ["Troca sem aprovação prévia", "MÉDIO", "Produto ou texto escolhido pode não ser o ideal e ficar no ar "
               "até a sua validação.", "Validação automática + histórico das trocas + backup da página antes de "
               "cada publicação. Valide no mesmo dia (seção 4)."],
              ["Link de catálogo", "MÉDIO", "O meli.la do catálogo pode cair no anúncio pausado antigo.",
               "O roteiro manda abrir o meli.la e conferir; a validação recusa link igual ao antigo."],
              ["Preço da lista = parcela", "BAIXO", "Faixa de preço errada.", "O roteiro exige conferir o preço "
               "à vista na página do anúncio."],
              ["Claude sem login / sem Chrome", "BAIXO", "Etapa 3 não roda.", "O programa avisa, pula a troca e "
               "atualiza o painel mesmo assim. Faça /login no terminal (claude) ou conecte a extensão."],
              ["Uso do plano do Claude", "BAIXO", "A etapa 3 consome o seu limite semanal.", "Use a opção 3 em dias "
               "de pouco uso disponível; a substituição fica para o dia seguinte."],
              ["Excel aberto", "BAIXO", "O painel não grava.", "Feche a planilha antes; rode a opção 7 depois."],
              ["Tempo", "BAIXO", "A verificação de 213 anúncios leva ~10 min (duas vezes se houver troca).",
               "Use a opção 2 se a verificação for recente."],
              ["Termos do ML Afiliados", "ATENÇÃO", "Links de afiliado devem levar a anúncios reais e ativos; "
               "textos não podem prometer o que o anúncio não diz.", "O roteiro proíbe inventar dados e exige "
               "conferir o anúncio ativo; você valida o texto depois."],
          ], [3.1, 2.1, 5.2, 7.2], cor=VERM)]

    s += [P("6. Arquivos desta pasta", "h1"),
          tab(["Arquivo", "Para que serve"], [
              ["0_MENU_ATUALIZA_ANUNCIOS.bat / menu_atualiza.py", "Menu desta atividade."],
              ["0_executar_tudo.py", "Executa as 5 etapas em ordem (o que o seu menu geral deve chamar)."],
              ["1_ a 5_*.py", "As etapas (seção 3)."],
              ["comum.py", "Funções comuns: caminhos, log, execução, regra old_bkp."],
              ["config_atualiza.json", "Caminhos e limites. Se mudar pasta, ajuste SÓ aqui."],
              ["roteiro_substituicao_claude.md", "Instruções que o Claude segue na substituição."],
              ["pendencias_substituicao.json", "Gerado na etapa 2 (quem precisa de substituto)."],
              ["substituicoes_aprovadas.json", "Gerado na etapa 3 (trocas escolhidas e validadas)."],
              ["historico_substituicoes.csv", "Todas as trocas, para a sua validação."],
              ["resumo_ultima_execucao.txt", "Resumo da última execução."],
              ["logs\\", "Um log por execução (tudo o que apareceu na tela)."],
              ["old_bkp\\", "Cópia de cada arquivo antes de ser alterado (regra do dono)."],
              ["gerar_documentacao_pdf.py", "Gera esta documentação."],
          ], [6.6, 11.0]),
          P("Programas reaproveitados (não copiados): Relatorios_Diarios_Anuncios\\programas_fontes_python "
            "(3_relatorio_acessos_anuncios.py, 6_verificar_anuncios.py, ATUALIZAR_PAINEL.bat) e "
            "Gestao_Anuncios_Blog\\1_PROGRAMAS\\Blog_WordPress\\gerenciar_blog.py.")]

    s += [CondPageBreak(7 * cm), P("7. Testes feitos em 09/11/2026", "h1"),
          tab(["Teste", "Resultado"], [
              ["Simulação completa (opção 8)", "OK: relatório gerado; 4 anúncios fora do ar listados (itens 51, 182, "
               "191, 196); Claude não chamado; nada publicado."],
              ["Validação da IA com dados de teste", "OK: aceitou a troca correta; recusou link igual ao antigo, "
               "link que não é meli.la e item fora da lista."],
              ["Troca no blog em pré-visualização", "OK: item achado pelo link antigo; resumo da mudança correto; "
               "nada publicado. Aviso: os cartões estáticos não têm campo de preço (normal)."],
              ["Chamada do Claude Code", "Comando aceito; <b>login do Claude Code expirado</b> neste PC: fazer "
               "/login antes da primeira execução real."],
          ], [5.4, 12.2], cor=VERDE),
          P("<b>Conclusão:</b> o processo está pronto e validado em simulação. A primeira execução real deve ser "
            "feita com o dono presente (Chrome logado e Claude Code com login), validando as trocas logo em seguida.")]

    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=1.5 * cm,
                            bottomMargin=1.6 * cm, title="Atualização automática dos anúncios", author="Claude")
    doc.build(s, onFirstPage=rodape, onLaterPages=rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
