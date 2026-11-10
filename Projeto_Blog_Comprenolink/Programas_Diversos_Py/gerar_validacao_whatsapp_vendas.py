# -*- coding: utf-8 -*-
"""PDF "Validacao_WhatsApp_Vendas_Calendario": valida o que o dono concluiu (catálogo do WhatsApp, vendas do ML Afiliados,
painel) e traz o calendário de execução semanal (PDF + .ics).
Rodar:  python -X utf8 gerar_validacao_whatsapp_vendas.py
Saída:  D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Validacao_WhatsApp_Vendas_Calendario_2026-11-01.pdf
        D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Calendario_Execucao_Semanal_WhatsApp_Vendas.ics
Caminhos com barra normal.
"""
import csv
import os
import re
import sys
from datetime import date, datetime, timedelta, timezone

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
sys.path.insert(0, "D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento/Divugação_WhastsApp_Instagram/_fonte")
import gerar_pendencias_detalhado as base  # noqa: E402
from gerar_pendencias_detalhado import (AZUL, AZUL_C, LARANJA, LARANJA_C, P, VERDE, VERDE_C, VERMELHO, VERMELHO_C,  # noqa: E402
                                        bloco, faixa, info, passos, tabela)
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer  # noqa: E402
import openpyxl  # noqa: E402

PASTA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/"
SAIDA = PASTA + "Validacao_WhatsApp_Vendas_Calendario_2026-11-01.pdf"
ICS = PASTA + "Calendario_Execucao_Semanal_WhatsApp_Vendas.ics"
CAT = "D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento/Celular_Whatsapp/06_CATALOGO_WHATSAPP"
HIST = "D:/Projeto_Blog_Comprenolink/Relatorios_Diarios_Anuncios/vendas_historico/historico_vendas.csv"
base.HOJE = date(2026, 11, 1)
SEGUNDAS = [date(2026, 11, 2) + timedelta(weeks=i) for i in range(9)]  # 02/11 a 28/12
ATENCAO = {
    date(2026, 11, 2): "Rodada 0 (opcional): as vendas foram atualizadas em 31/10. Só mande prints se houver venda nova. À noite: Story 19:10 e envios do WhatsApp.",
    date(2026, 11, 9): "PRIMEIRA RODADA COMPLETA (daqui uma semana). Conferir também se os links dos pacotes seguem certos (etapa 5).",
    date(2026, 11, 16): "Rodada normal.",
    date(2026, 11, 23): "Semana da Black Friday (27/11): conferir no painel se os produtos da campanha seguem ativos.",
    date(2026, 11, 30): "Cyber Monday e virada para Natal: a página de Natal entra no ar em 01/12. Conferir o catálogo e as categorias.",
    date(2026, 12, 7): "Rodada normal. Conferir os produtos de Natal ativos.",
    date(2026, 12, 14): "Última segunda antes da semana do Natal: fechar pendências de anúncios.",
    date(2026, 12, 21): "Semana do Natal: rodada rápida (vendas e painel).",
    date(2026, 12, 28): "Fechamento de 2026: consolidar métricas do ano e decidir o plano de 2027.",
}
# etapas semanais: (hora, minuto, duração min, quem, título, descrição)
ETAPAS = [
    (10, 0, 10, "Você + Claude", "1. Blog: pedir \"gerar as categorias\"",
     "Se cadastrou ou retirou anúncios no blog na semana, peça ao Claude: gerar as categorias. Ele republica as páginas de categoria e a Black Friday."),
    (10, 15, 30, "Você", "2. ML Afiliados: prints das vendas",
     "mercadolivre.com.br/afiliados/dashboard na conta do blog (ganho estimado ~R$ 172 confirma a conta). Métricas > Vendas > Status: marcar as 4 opções (Aprovada, Em revisão, Recusada, Cancelada). "
     "Print de cada página da tabela e envie ao Claude. Não existe botão de exportar nessa conta."),
    (10, 45, 20, "Claude (você fecha o Excel)", "3. CSV e painel",
     "O Claude monta/atualiza vendas_ml_AAAA-MM-DD.csv em Relatorios_Diarios_Anuncios/vendas_afiliados, confere se o número de linhas bate com a tela e roda o ATUALIZAR_PAINEL.bat. "
     "Feche o Excel antes."),
    (11, 15, 15, "Você", "4. Conferir o PDF do painel",
     "Abra o Painel_conversao_performance mais recente (Relatorios_Diarios_Anuncios). Veja vendas, comissão pendente, conversão e anúncios fora do ar."),
    (11, 30, 20, "Você + Claude", "5. Catálogo do WhatsApp e links",
     "Peça ao Claude: rodar gerar_catalogo_categorias.py (categoria nova?). Confira no WhatsApp se algum item está \"em análise\" há mais de 24 h. "
     "Se o blog retirou ou incluiu anúncios, peça: conferir a numeração dos itens e refazer os links dos pacotes e do catálogo."),
]
BRT = timezone(timedelta(hours=-3))


def esc(t):
    return t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def dobra(linha):
    partes, atual = [], b""
    for ch in linha:
        cb = ch.encode("utf-8")
        if len(atual) + len(cb) > (74 if partes else 75):
            partes.append(atual)
            atual = b""
        atual += cb
    partes.append(atual)
    return "\r\n ".join(p.decode("utf-8") for p in partes)


def gera_ics():
    agora = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//comprenolink//Execucao semanal//PT-BR", "CALSCALE:GREGORIAN",
         "X-WR-CALNAME:Execucao semanal WhatsApp e vendas", "X-WR-TIMEZONE:America/Sao_Paulo",
         "BEGIN:VTIMEZONE", "TZID:America/Sao_Paulo", "BEGIN:STANDARD", "DTSTART:19700101T000000", "TZOFFSETFROM:-0300",
         "TZOFFSETTO:-0300", "TZNAME:-03", "END:STANDARD", "END:VTIMEZONE"]
    for seg in SEGUNDAS:
        for h, m, dur, quem, tit, desc in ETAPAS:
            ini = datetime(seg.year, seg.month, seg.day, h, m)
            fim = ini + timedelta(minutes=dur)
            extra = ATENCAO.get(seg, "")
            d = f"{quem}.\n{desc}\n\nSemana de {seg:%d/%m}: {extra}\nPasso a passo: D:\\Projeto_Blog_Comprenolink\\0- Pendencias\\1_Pendencias\\PROCESSO_SEMANAL_VENDAS_WHATSAPP.pdf"
            L += ["BEGIN:VEVENT", f"UID:semanal-{seg:%Y%m%d}-{h}{m:02d}@comprenolink.net", f"DTSTAMP:{agora}",
                  f"DTSTART;TZID=America/Sao_Paulo:{ini:%Y%m%dT%H%M%S}", f"DTEND;TZID=America/Sao_Paulo:{fim:%Y%m%dT%H%M%S}",
                  f"SUMMARY:{esc('Semanal: ' + tit)}", f"DESCRIPTION:{esc(d)}", "BEGIN:VALARM", "ACTION:DISPLAY",
                  f"DESCRIPTION:{esc(tit)}", "TRIGGER:-PT15M", "END:VALARM", "END:VEVENT"]
    L.append("END:VCALENDAR")
    with open(ICS, "w", encoding="utf-8", newline="") as f:
        f.write("\r\n".join(dobra(x) for x in L) + "\r\n")
    return len(SEGUNDAS) * len(ETAPAS)


def norm(t):
    t = (t or "").replace("″", '"').replace("×", "x").replace("’", "'").replace("–", "-").replace("\u00a0", " ")
    return re.sub(r"\s+", " ", t).strip().lower()


def vendas():
    r = list(csv.DictReader(open(HIST, encoding="utf-8-sig"), delimiter=";"))
    res = {}
    for x in r:
        s = res.setdefault(x["status"], [0, 0.0, 0.0])
        s[0] += 1
        s[1] += float(x["valor"] or 0)
        s[2] += float(x["comissao"] or 0)
    return len(r), res


def moeda(v):
    return "R$ " + f"{v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def conteudo():
    import dados_divulgacao as dd
    dados = dd.carrega_produtos()
    itens = dados["itens"]
    por_cat = {}
    for x in itens:
        if x.get("cat"):
            por_cat[x["cat"]["slug"]] = por_cat.get(x["cat"]["slug"], 0) + 1
    wc = openpyxl.load_workbook(CAT + "/CATEGORIAS/CATALOGO_CATEGORIAS.xlsx").active
    cats = [r for r in wc.iter_rows(min_row=2, values_only=True) if r[0]]
    wp = openpyxl.load_workbook(CAT + "/CATALOGO_WHATSAPP.xlsx").active
    prods = [r for r in wp.iter_rows(min_row=2, values_only=True) if r[0]]
    fotos = [f for f in os.listdir(CAT + "/CATEGORIAS/fotos")]
    total, v = vendas()
    pend, canc = v.get("Pendente", [0, 0, 0]), v.get("Cancelada", [0, 0, 0])

    st = [Spacer(1, 0.4 * cm), P("VALIDAÇÃO E CALENDÁRIO DE EXECUÇÃO", "capa_t"), Spacer(1, 4),
          P("WhatsApp (catálogo) • vendas do ML Afiliados • painel • rotina semanal<br/>Conferido em domingo 01/11/2026", "capa_s"), Spacer(1, 8),
          info([("Resultado em uma frase", "Vendas e painel estão corretos e a rotina semanal faz sentido. Conferi também o WhatsApp Business no WhatsApp Web, com a sua autorização. "
                                           "Corrigi os 16 links do catálogo por produto. Falta cadastrar 7 das 9 categorias e apagar o CNL-111."),
                ("O que conferi no WhatsApp", "Catálogo (itens e links), Coleções, respostas rápidas, Perfil comercial e Canal. Não li nem enviei conversas. "
                                              "Troquei só o campo Link de 16 itens do catálogo."),
                ("Onde conferi", "06_CATALOGO_WHATSAPP/CATEGORIAS, vendas_afiliados/vendas_ml_2026-10-31.csv, o histórico e o painel, "
                                 "os PDFs PROCESSO_SEMANAL_VENDAS_WHATSAPP e Pendencias_WhatsApp, o blog ao vivo e os pacotes do dia.")]),
          Spacer(1, 8), P("Resultado por item", "h2"),
          tabela(["Item", "Situação", "Detalhe"],
                 [["Catálogo por categoria (pasta CATEGORIAS)", "OK",
                   f"9 itens e 9 fotos ({len(fotos)} arquivos), todos sem preço e com aviso de afiliado; Bebê & Maternidade e Moda Infantil & Juvenil estão na lista. "
                   "Os links são por categoria, então não quebram quando o blog muda."],
                  ["Categorias no catálogo do WhatsApp", "ATENÇÃO",
                   "Só 2 das 9 existem: Moda Infantil & Juvenil e Bebê & Maternidade. Faltam 7: Tecnologia, Áudio & TV, Casa & Eletrodomésticos, Casa Cama & Decoração, "
                   "Ferramentas, Esporte & Fitness e Beleza & Saúde. As Coleções estão vazias. Corrigi a planilha: S nas 2 existentes e N nas 7 (cópia anterior em _backups_claude_)."],
                  ["Contagem \"Produtos hoje\" das categorias", "Atenção",
                   "Está desatualizada (Bebê 43 e Beleza 43 na planilha; hoje o blog tem " + f"{por_cat.get('bebe-e-maternidade', 0)} e {por_cat.get('beleza-e-saude', 0)}). "
                   "Informativo: não muda o link. Rode gerar_catalogo_categorias.py para atualizar."],
                  ["Catálogo por produto (17 itens CNL)", "CORRIGIDO",
                   "O campo Link do WhatsApp aceita só 75 caracteres e cortava todos os links em \"...?utm_source=w\", sem o número do produto. Em 01/11 troquei 16 links por "
                   "links curtos com o número certo (#item-N). O CNL-111 (produto que saiu do Mercado Livre) continua lá: apague (página 3)."],
                  ["Respostas rápidas, Perfil e Canal", "OK",
                   "7 respostas rápidas (/canal já com o link do Canal, /bf, /natal, /link, /preço, /pedido, /obrigado). Perfil: nome, horário, categoria, site, e-mail e usuário. "
                   "Canal: um só, \"Compre no Link - Achados do Mercado Livre\", sem duplicado e ainda sem publicações."],
                  ["CSV de vendas (vendas_ml_2026-10-31.csv)", "OK",
                   f"19 linhas = 19 vendas no histórico. Pendentes: {pend[0]} ({moeda(pend[1])} em vendas, comissão {moeda(pend[2])}). "
                   f"Canceladas (recusada, conta vinculada): {canc[0]} (comissão perdida {moeda(canc[2])})."],
                  ["Conta do CSV é a do blog?", "OK",
                   "Sim: a comissão pendente de R$ 172,00 bate com o ganho estimado que o PROCESSO_SEMANAL manda usar para reconhecer a conta certa."],
                  ["Painel de controle", "OK",
                   "Atualizado em 01/11 às 11:20 com o relatório de acesso de 31/10 21:30: 19 vendas, 214 anúncios verificados (213 ativos, 1 pausado, 1 fora do ar) "
                   "e 0 fórmulas com erro."],
                  ["PROCESSO_SEMANAL_VENDAS_WHATSAPP.pdf", "OK com ajustes",
                   "Coerente com o que verifiquei (script, lembrete e passos existem). Ajustes na página 2."],
                  ["Itens novos do blog 212, 213 e 214", "Atenção",
                   "Entraram hoje com o texto padrão (\"Olha o que eu encontrei!\", \"Uso diário\"). Precisam de selo, descrição e benefícios dentro da política."]],
                 [0.3, 0.12, 0.58], cor=AZUL)]

    # ------------- Página 2: o que corrigi e ajustes
    st += [PageBreak(), faixa("2", "O que descobri e o que já corrigi", "Mudança de numeração no blog em 31/10, depois das 16:41", LARANJA), Spacer(1, 6),
           P("O blog numera os produtos (1 a 214) e os links usam essa numeração (#item-63, por exemplo). Depois de 31/10 às 16:41 alguém retirou o item 39 "
             "(Kit 3 Formas Antiaderentes) e o item 214 antigo (o link que levava a um perfil vazio) e incluiu 3 produtos no fim. Com a saída do item 39, "
             "todos os produtos depois dele subiram uma posição. Quem usava o número antigo passou a abrir o produto vizinho.", "p"),
           Spacer(1, 4),
           bloco("O que eu já corrigi hoje", [
               "Refiz os textos dos 27 pacotes do dia (02/11 a 23/12) com os números certos. Conferi: nenhum produto do dia mudou, só os links dos Stories, Status, Canal e Direct.",
               "Exemplo: o Story de 02/11 (Samsung 55\") passou de #item-64 para #item-63, que é o item certo no site hoje.",
               "Backup de cada pasta em Planejamentos/Andamento/Divugação_WhastsApp_Instagram/_backup_pacotes (nome termina em _01nov_ANTES_links) e cópia para Planejamentos\\Andamento\\Celular_Whatsapp.",
               "Os posts e Reels já agendados no Instagram não precisam mudar: a legenda manda para o \"link da bio\" e não usa número de item."],
                 VERDE, VERDE_C), Spacer(1, 6),
           bloco("O que ainda precisa de você", [
               "Se você já enviou algum Story, Status ou Canal com link de produto depois de 31/10 às 16:41, confira o destino do link (pode ter aberto o produto vizinho).",
               "Copie os textos novos das pastas do dia (os de 31/10 ficam obsoletos para os itens após o 39).",
               "Para evitar isso no futuro: sempre que retirar ou incluir um anúncio, peça ao Claude \"conferir a numeração e refazer os links\"."],
                 LARANJA, LARANJA_C), Spacer(1, 6),
           P("Ajustes que recomendo no PROCESSO_SEMANAL_VENDAS_WHATSAPP.pdf", "h2"),
           tabela(["Ponto", "O que o PDF diz", "Recomendação"],
                  [["Rodar o painel", "\"O rodar do programa é sempre manual (o Claude não pode...)\"",
                    "O Claude consegue rodar o ATUALIZAR_PAINEL.bat (foi feito em 31/10 às 16:37). Basta você fechar o Excel."],
                   ["Etapa nova", "Não existe",
                    "Incluir \"conferir a numeração dos itens e refazer os links\" depois de qualquer retirada ou inclusão de anúncio (etapa 5 do calendário)."],
                   ["Este PDF x Pendencias_WhatsApp.pdf", "Você citou o Pendencias_WhatsApp.pdf como a rotina semanal",
                    "O Pendencias_WhatsApp.pdf é a lista única de 30/10 (catálogo e Canal). A rotina semanal está no PROCESSO_SEMANAL_VENDAS_WHATSAPP.pdf, que eu validei."],
                   ["Quando", "Toda segunda, 10:15", "Está certo. O calendário abaixo organiza as 5 etapas entre 10:00 e 11:50."]],
                  [0.2, 0.36, 0.44], cor=LARANJA)]

    # ------------- Página 3: tabela dos itens CNL
    linhas = []
    for r in prods:
        cod, nome, link = r[0], r[1], r[4]
        m = re.search(r"#item-(\d+)", link or "")
        velho = int(m.group(1)) if m else None
        achou = [x for x in itens if norm(x["nome"])[:28] == norm(nome)[:28]]
        if not achou:
            linhas.append([cod, nome[:44], str(velho), "não existe mais", "Apagar do catálogo do WhatsApp"])
            continue
        novo = achou[0]["n"]
        acao = "Link certo, nada a fazer" if novo == velho else f"Trocar #item-{velho} por #item-{novo} no link"
        linhas.append([cod, nome[:44], str(velho), str(novo), acao])
    linhas = [[l[0], l[1], l[2], l[3], "Apagar (você)" if l[3].startswith("não") else "Corrigido em 01/11"] for l in linhas]
    st += [PageBreak(), faixa("3", "Catálogo por produto (17 itens CNL)", "16 links corrigidos em 01/11 • 1 item para você apagar", AZUL), Spacer(1, 6),
           P("O campo Link do catálogo do WhatsApp guarda no máximo 75 caracteres. Os links antigos (com utm) foram cortados em \"...?utm_source=w\" e abriam o topo do guia, sem o produto. "
             "Em 01/11 troquei os 16 por links curtos no formato https://comprenolink.net/melhores-produtos-mercado-livre-2026/#item-N (70 caracteres). "
             "Se o blog retirar ou incluir produtos, os números mudam: peça ao Claude \"conferir os links do catálogo\".", "p"),
           Spacer(1, 4), tabela(["Código", "Produto", "Número que estava no link", "Número agora", "Situação"], linhas, [0.1, 0.36, 0.14, 0.12, 0.28], cor=AZUL),
           Spacer(1, 6),
           passos([("Item CNL-111 (Kit Skincare Dermachem)", "O produto saiu do Mercado Livre. Apague o item: WhatsApp Business → Catálogo → toque no item → Excluir. Eu não apago itens, porque não tem volta."),
                   ("Categorias que faltam", "Cadastre as 7 categorias que não estão no catálogo (nome, descrição e link prontos em 06_CATALOGO_WHATSAPP/CATEGORIAS/CATALOGO_CATEGORIAS_TEXTOS.txt). "
                    "Atenção ao limite de 75 caracteres do campo Link: use o link curto da categoria, por exemplo https://comprenolink.net/audio-e-tv/."),
                   ("Depois", "Me avise e eu atualizo a coluna \"Cadastrado\" da planilha.")], AZUL)]

    # ------------- Página 4: calendário
    linhas = []
    for seg in SEGUNDAS:
        linhas.append([f"{seg:%d/%m} (seg)", ATENCAO[seg]])
    st += [PageBreak(), faixa("4", "Calendário de execução semanal", "Toda segunda-feira • 02/11 a 28/12 • 5 etapas das 10:00 às 11:50", VERDE), Spacer(1, 6),
           P("Rodada normal (cada segunda-feira)", "h2"),
           tabela(["Hora", "Quem", "O que fazer"],
                  [[f"{h:02d}:{m:02d}", quem, f"<b>{tit}</b><br/>{desc}"] for h, m, dur, quem, tit, desc in ETAPAS], [0.1, 0.17, 0.73], cor=VERDE), Spacer(1, 8),
           P("Datas e atenção de cada semana", "h2"),
           tabela(["Segunda", "Atenção da semana"], linhas, [0.16, 0.84], cor=VERDE), Spacer(1, 8),
           bloco("Como usar o arquivo de agenda", [
               "Arquivo: D:\\Projeto_Blog_Comprenolink\\0- Pendencias\\1_Pendencias\\Calendario_Execucao_Semanal_WhatsApp_Vendas.ics (45 eventos, com aviso 15 minutos antes).",
               "Importe uma vez no Google Agenda (Configurações → Importar e exportar) ou no Outlook (Arquivo → Abrir e exportar → Importar um arquivo iCalendar).",
               "Ele não substitui os lembretes antigos (LEMBRETE_SEMANAL_EXPORTAR_VENDAS e LEMBRETE_SEMANAL_GERAR_CATEGORIAS): se importar este, pode apagar aqueles dois para não duplicar.",
               "Os envios diários (Story, Status, Canal) continuam no arquivo agenda_novas_atividades.ics, em D:\\Projeto_Blog_Comprenolink."],
                 AZUL, AZUL_C)]

    # ------------- Página 5: pendências do dono
    st += [PageBreak(), faixa("5", "Resumo: o que você precisa fazer agora", "Em ordem de importância", VERMELHO), Spacer(1, 6),
           tabela(["Quando", "O que", "Detalhe"],
                  [["Concluído em 01/11", "Excel fechado, planilha das categorias marcada S e painel atualizado", "Nada a fazer. O PDF novo do painel é o Painel_conversao_performance_2026-11-01_11h20.pdf."],
                   ["Hoje à noite", "Deixar o PC, o app Claude e o Chrome ligados", "Eu agendo o dia 30/11 às 20:39 (se a rotina tiver se perdido, escreva \"agendar 30/11\" depois das 20:00)."],
                   ["Segunda 02/11, 19:10 a 19:20", "Story, Status e Canal", "Use os textos refeitos em Planejamentos/Andamento/Celular_Whatsapp/07_PACOTE_DO_DIA/2026-11-02_seg (link novo #item-63)."],
                   ["Quando puder", "Apagar o CNL-111 do catálogo e cadastrar as 7 categorias que faltam", "Página 3. Os 16 links dos produtos eu já corrigi."],
                   ["Quando puder", "Sair do aparelho conectado do WhatsApp Web (se não for mais usar)", "WhatsApp Business → Aparelhos conectados → toque no aparelho → Sair. Fecha o acesso que usei."],
                   ["Segunda 09/11, 10:00", "Primeira rodada semanal completa", "Calendário da página 4."]],
                  [0.2, 0.33, 0.47], cor=VERMELHO)]
    return st


def main():
    n = gera_ics()
    print(f"ICS: {ICS} ({n} eventos)")
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Validação WhatsApp, vendas e calendário (comprenolink.net)", author="comprenolink.net")
    doc.build(conteudo(), onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
