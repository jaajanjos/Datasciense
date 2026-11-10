# -*- coding: utf-8 -*-
"""Guia passo a passo (datas, horários e o que fazer) do Instagram @compre.no.link – nov/dez 2026.
Gera D:\\Projeto_Blog_Comprenolink\\0- Pendencias\\3_Guia_Passo_a_Passo_Instagram_2026\\Guia_Passo_a_Passo_Instagram_2026.pdf. Lê os dias de post do 07_PACOTE_DO_DIA.
Rodar:  python -X utf8 gerar_guia_rotina_instagram.py
"""
import os
import re
import sys
from datetime import date

sys.path.insert(0, r"D:\Projeto_Blog_Comprenolink\0- Pendencias\5_Plano_turbinar_anuncio_instagram")
from gerar_pdf_plano_turbinar import (AMARELO, AZUL_C, CINZA, CLARO, ESCURO, LARANJA, LARANJA_C, S, VERDE,  # noqa: E402
                                      VERDE_C, VERMELHO, VERMELHO_C, caixa, tabela, LARG)
import gerar_pdf_plano_turbinar as base
from reportlab.lib import colors  # noqa: E402
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer  # noqa: E402

SAIDA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\3_Guia_Passo_a_Passo_Instagram_2026\Guia_Passo_a_Passo_Instagram_2026.pdf"
PACOTE = r"D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento/Divugação_WhastsApp_Instagram/07_PACOTE_DO_DIA"
SEM = ["seg", "ter", "qua", "qui", "sex", "sáb", "dom"]
ROXO_C = colors.HexColor("#EDE9FE")


def dias_de_post():
    out = []
    for pasta in sorted(os.listdir(PACOTE)):
        arq = os.path.join(PACOTE, pasta, "1_TEXTOS_DO_DIA.txt")
        if not os.path.exists(arq):
            continue
        with open(arq, encoding="utf-8-sig") as f:
            txt = f.read()
        m = re.search(r"Instagram – Post no feed.*?\n=+\n(.+?)\n", txt, re.S)
        if not m:
            continue
        d = date.fromisoformat(pasta[:10])
        palavra = "NATAL" if "Comente NATAL" in txt else "BLACK"
        out.append((d, pasta, re.sub(r"^[^\w\"]+", "", m.group(1)).strip(), palavra))  # tira o emoji do começo
    return out


def rodape(c, doc):
    c.saveState()
    c.setFillColor(AMARELO)
    c.rect(0, A4[1] - 0.45 * cm, A4[0], 0.45 * cm, fill=1, stroke=0)
    c.setFont("Arial", 8)
    c.setFillColor(CINZA)
    c.drawString(1.8 * cm, 1.1 * cm, "Guia Passo a Passo Instagram @compre.no.link – nov/dez 2026  •  27/10/2026")
    c.drawRightString(A4[0] - 1.8 * cm, 1.1 * cm, f"Página {doc.page}")
    c.restoreState()


def capa(c, doc):
    c.saveState()
    c.setFillColor(ESCURO)
    c.rect(0, A4[1] - 7 * cm, A4[0], 7 * cm, fill=1, stroke=0)
    c.setFillColor(AMARELO)
    c.rect(0, A4[1] - 7.25 * cm, A4[0], 0.25 * cm, fill=1, stroke=0)
    c.setFont("Arial-B", 30)
    c.drawCentredString(A4[0] / 2, A4[1] - 3.3 * cm, "compre no link")
    c.setFillColor(colors.white)
    c.setFont("Arial", 12)
    c.drawCentredString(A4[0] / 2, A4[1] - 4.3 * cm, "comprenolink.net  •  @compre.no.link  •  achados do Mercado Livre")
    c.restoreState()
    rodape(c, doc)


def P(t, e="p"):
    return Paragraph(t, S[e])


def passos(lista):
    return tabela([["Passo", "O que fazer"]] + [[f"<b>{i}</b>", t] for i, t in enumerate(lista, 1)], [0.1, 0.9])


def montar():
    dias = dias_de_post()
    st = [Spacer(1, 6.3 * cm),
          Paragraph("Guia Passo a Passo<br/>Instagram @compre.no.link", S["capa_t"]), Spacer(1, 10),
          Paragraph("O que fazer, em que data e em que horário – novembro e dezembro de 2026", S["capa_s"]),
          Spacer(1, 24),
          tabela([
              ["Item", "Informação"],
              ["Perfil", "@compre.no.link  •  blog comprenolink.net  •  WhatsApp (11) 99495-9657"],
              ["Período", f"27/10/2026 a 26/12/2026  •  {len(dias)} dias de post no Instagram"],
              ["Horário fixo dos dias de post", "<b>19:00</b> post • <b>19:05</b> Reels • <b>19:10</b> story com link"],
              ["Seu tempo por dia de post", "cerca de 5 a 10 minutos (story + automação + responder comentários)"],
              ["Documento gerado em", "27/10/2026"],
          ], [0.32, 0.68]), Spacer(1, 16),
          caixa("<b>Como usar:</b> siga as seções na ordem. A seção 1 é desta semana (preparação). A seção 5 é a "
                "rotina que se repete em todo dia de post. A seção 7 traz a lista de todos os dias, com o produto e "
                "a palavra (BLACK ou NATAL)."),
          PageBreak()]

    # 1. esta semana
    st += [P("1. Esta semana: preparação (até sábado 31/10)", "h1"),
           tabela([
               ["Quando", "O que fazer", "Tempo", "Seção"],
               ["<b>qua 28/10 ou qui 29/10</b>", "Reconectar a extensão Claude no Chrome e avisar \"reconectei\"", "5 min", "2"],
               ["logo em seguida", "Aprovar a amostra do dia 02/11; o Claude agenda os posts e Reels dos 27 dias", "5 min (você)", "2"],
               ["<b>até sáb 31/10</b>", "Testar a automação do ManyChat: comentar BLACK com outra conta", "5 min", "3"],
               ["<b>até sáb 31/10</b>", "WhatsApp Business: item Bebê & Maternidade no catálogo + criar o Canal", "15 min", "4"],
               ["<b>até qui 05/11</b>", "Reunião com o sócio sobre o Turbinar (plano em 0- Pendencias\\5_Plano_turbinar_anuncio_instagram)", "30 min", "6"],
           ], [0.22, 0.56, 0.12, 0.1], extra=[("BACKGROUND", (0, 1), (-1, 2), LARANJA_C)]),
           Spacer(1, 10),
           P("2. Reconectar o Chrome (para o Claude agendar os posts)", "h1"),
           passos([
               "Na barra de tarefas, clique no <b>Google Chrome</b> (ícone redondo vermelho/amarelo/verde/azul). "
               "<b>Não</b> é o Edge (onda azul e verde).",
               "No canto de cima à direita, procure o ícone do <b>Claude</b> (estrelinha laranja). Se não estiver, clique no "
               "<b>quebra-cabeça</b> e depois no <b>alfinete</b> ao lado de \"Claude\".",
               "Se não existir \"Claude\" na lista, instale: chromewebstore.google.com → procure \"Claude\" → "
               "<b>Usar no Chrome</b> → <b>Adicionar extensão</b>.",
               "Clique no ícone Claude. No painel da direita, entre com a <b>mesma conta</b> do app Claude.",
               "Deixe o Chrome aberto (pode minimizar) e escreva ao Claude: <b>\"reconectei\"</b>.",
               "O Claude mostra a amostra do dia 02/11 (post 19:00 + Reels 19:05). Responda <b>\"ok\"</b> e ele agenda os 27 dias "
               "(opção \"Programar conteúdo\" do Instagram). Os posts passam a sair sozinhos.",
           ]),
           PageBreak()]

    # 3. teste
    st += [P("3. Testar a automação do ManyChat (até 31/10)", "h1"),
           P("A automação já está <b>ativa (LIVE)</b> no post fixado de boas-vindas. O teste precisa ser feito com "
             "<b>outra conta</b> (a compre.no.link não dispara a própria automação).", "p"),
           passos([
               "No celular, abra o Instagram com a sua <b>conta pessoal</b> (ou peça ao sócio/amigo).",
               "Toque na <b>lupa</b>, procure <b>compre.no.link</b> e abra o <b>post fixado</b> (com o alfinete).",
               "Comente <b>BLACK</b> e publique.",
               "Em 1 a 2 minutos deve aparecer a resposta \"Te mandei no Direct!\" embaixo do comentário.",
               "Abra o <b>Direct</b> (avião de papel) da conta pessoal – se não estiver lá, veja <b>Solicitações</b>.",
               "Toque em <b>Quero o link</b> → chega o botão <b>Ver a lista no blog</b> → toque e confira se abre a página da Black Friday.",
               "Mande um print ao Claude. <b>Se não chegou:</b> na conta compre.no.link, vá em ☰ → Configurações e atividade → "
               "Mensagens e respostas a stories → Ferramentas conectadas → ligue <b>Permitir acesso às mensagens</b> e teste de novo.",
           ]),
           P("4. WhatsApp Business (até 31/10)", "h1"),
           tabela([
               ["Tarefa", "Onde está o material"],
               ["Cadastrar 1 item no catálogo: <b>Bebê & Maternidade</b> (preço em branco)",
                "OneDrive → Divulgacao_Blog → 06_CATALOGO_WHATSAPP → CATEGORIAS → CAT-bebe-e-maternidade"],
               ["Criar o <b>Canal</b> do WhatsApp e mandar o link ao Claude", "08_PASSO_A_PASSO_WHATSAPP_NO_CELULAR.pdf – Parte 6"],
           ], [0.5, 0.5]),
           PageBreak()]

    # 5. rotina do dia de post
    st += [P("5. Rotina de cada dia de post (a partir de seg 02/11)", "h1"),
           P("O alarme do calendário (12_CALENDARIO_INSTAGRAM.ics) toca às <b>18:15</b>. Com os posts agendados, "
             "o post e o Reels saem sozinhos – você cuida do story e da automação.", "p"),
           tabela([
               ["Hora", "Quem", "O que fazer"],
               ["<b>19:00</b>", "Instagram (agendado)", "Post de foto sai sozinho no feed"],
               ["<b>19:05</b>", "Instagram (agendado)", "Reels sai sozinho (é o que mais alcança quem não segue)"],
               ["<b>19:10</b>", "Você – celular", "Publicar o <b>story com link</b> (passo a passo 5A)"],
               ["<b>19:15</b>", "Você – Edge", "Criar a <b>automação do ManyChat</b> para o Reels do dia (passo a passo 5B)"],
               ["até 22:00", "Você", "Responder comentários e Direct; onde não houver automação, digite <b>bf</b> (ou <b>natal</b>) no Direct"],
           ], [0.12, 0.22, 0.66], extra=[("BACKGROUND", (0, 3), (-1, 4), AMARELO)]),
           P("5A. Story com adesivo de link (celular, 2 minutos)", "h2"),
           passos([
               "Abra o <b>OneDrive</b> → Download → Divulgacao_Blog → 07_PACOTE_DO_DIA → <b>pasta do dia</b>.",
               "Abra <b>story.png</b> → <b>Salvar</b> (vai para a galeria).",
               "Abra <b>1_TEXTOS_DO_DIA.txt</b> e copie o link do bloco \"Instagram – Story com adesivo de link\".",
               "No Instagram compre.no.link: <b>+</b> → <b>Story</b> → escolha o story.png.",
               "Toque no ícone de <b>adesivo</b> (carinha, em cima) → <b>Link</b> → cole o link → texto do adesivo: <b>VER NO BLOG</b>.",
               "Arraste o adesivo para cima do retângulo amarelo da arte (\"adesivo VER NO BLOG aqui\").",
               "Toque em <b>Seu story</b>.",
           ]),
           PageBreak(),
           P("5B. Automação do ManyChat para o post do dia (Edge, 2 minutos)", "h2"),
           P("No plano grátis, cada automação vale para <b>1 publicação</b>. Por isso, em cada dia de post, crie uma "
             "nova para o <b>Reels</b> do dia (onde vêm mais comentários).", "p"),
           passos([
               "No Edge, abra <b>app.manychat.com</b> → menu <b>Automação</b> → <b>+ Nova automação</b> / modelo "
               "<b>\"Autoenviar links a partir de comentários\"</b>.",
               "<b>Publicação:</b> \"uma publicação ou Reels específico\" → escolha o <b>Reels do dia</b> → Próximo.",
               "<b>Palavras:</b> BLACK, LINK, QUERO (em dezembro: <b>NATAL, LINK, QUERO</b>) e ligue \"interagir com os comentários\".",
               "<b>Respostas públicas:</b> \"Te mandei no Direct!\" • \"Enviado! Confere sua caixa de mensagens\" • "
               "\"Pronto! O link está no seu Direct\" → Próximo.",
               "<b>DM de boas-vindas:</b> \"Oi! Que bom te ver por aqui! Separei os achados mais vendidos e bem avaliados do "
               "Mercado Livre pra você. Toque no botão abaixo que eu te mando o link agora\" • botão: <b>Quero o link</b>.",
               "<b>DM com o link:</b> \"Aqui está: a lista da Black Friday com o Top 10 e as ofertas por categoria... (Link de "
               "afiliado: posso ganhar comissão, sem custo extra para você.)\" • botão <b>Ver a lista no blog</b> • link abaixo.",
               "Deixe <b>desligadas</b> as opções com etiqueta <b>PRO</b>. Clique em <b>Ativar</b>. Nunca clique em "
               "\"Start Free Trial\" (cobra no cartão).",
           ]),
           tabela([
               ["Campanha", "Link do botão \"Ver a lista no blog\""],
               ["Black Friday (nov)", "https://comprenolink.net/black-friday/?utm_source=instagram&amp;utm_medium=dm&amp;utm_campaign=black_friday&amp;utm_content=manychat"],
               ["Natal (dez)", "https://comprenolink.net/presentes-de-natal/?utm_source=instagram&amp;utm_medium=dm&amp;utm_campaign=natal&amp;utm_content=manychat"],
           ], [0.2, 0.8]),
           Spacer(1, 6),
           caixa("No Natal troque também o texto da DM com o link: \"Aqui estão os presentes de Natal mais vendidos e bem "
                 "avaliados... (Link de afiliado: posso ganhar comissão, sem custo extra para você.)\"", LARANJA_C, LARANJA),
           PageBreak()]

    # 6. datas especiais
    st += [P("6. Datas especiais", "h1"),
           tabela([
               ["Data", "O que fazer", "Quem"],
               ["<b>qui 05/11</b>", "Reunião Turbinar (valor máximo e quem paga) + ler termos do ML Afiliados + republicar blog das máquinas", "Você + sócio"],
               ["<b>sex 06/11</b>", "Criar os <b>Destaques</b> no celular (Black Friday, Categorias, Como comprar) – pedir o passo a passo ao Claude", "Você"],
               ["<b>seg 09/11</b>", "Decisões: QCY Shopee, nota antiga no painel das máquinas, divulgação de longo prazo", "Você"],
               ["05/11 (feito)", "Conta de anúncios Meta criada, cartão do dono e limite de R$ 50", "Você"],
               ["16 a 18/11", "Turbinar – teste R$ 50 (liberado em 05/11) • avaliação qui 19/11", "Você + Claude"],
               ["21 a 27/11", "Turbinar – Black Friday R$ 105 (se o teste deu verde) • avaliação seg 30/11", "Você + Claude"],
               ["<b>sex 27/11</b>", "Fim da Black Friday no blog", "–"],
               ["<b>ter 01/12</b>", "Bio: versão Natal (Claude) • link 1 da bio → comprenolink.net/presentes-de-natal (você, celular) • "
                "automações passam a usar NATAL • Search Console: pedir indexação de /presentes-de-natal/", "Você + Claude"],
               ["05 a 14/12", "Turbinar – Natal R$ 100 (se a Black Friday se pagou)", "Sócio"],
               ["até seg 21/12", "Relatório final do Turbinar", "Claude"],
               ["<b>sáb 26/12</b>", "Link 1 da bio volta para comprenolink.net", "Você (celular)"],
           ], [0.15, 0.65, 0.2]),
           PageBreak()]

    # 7. lista dos dias
    linhas = [["Data", "Produto do dia", "Palavra", "Pasta do dia"]]
    extra = []
    for i, (d, pasta, prod, pal) in enumerate(dias, 1):
        linhas.append([f"<b>{d:%d/%m}</b> {SEM[d.weekday()]}", prod, f"<b>{pal}</b>", pasta])
        extra.append(("BACKGROUND", (0, i), (-1, i), ROXO_C if pal == "NATAL" else (CLARO if i % 2 else colors.white)))
    st += [P(f"7. Todos os dias de post ({len(dias)} dias)", "h1"),
           P("Em cada dia: post 19:00 • Reels 19:05 • story 19:10 • automação ManyChat com a palavra indicada. "
             "Linhas roxas = campanha de Natal.", "pq"),
           tabela(linhas, [0.13, 0.55, 0.11, 0.21], zebra=False, extra=extra),
           PageBreak(),
           P("8. Onde estão os arquivos", "h1"),
           tabela([
               ["O quê", "No computador", "No celular (OneDrive)"],
               ["Pacote de cada dia (post, story, Reels, textos)", "D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Divugação_WhastsApp_Instagram\\07_PACOTE_DO_DIA",
                "Download → Divulgacao_Blog → 07_PACOTE_DO_DIA"],
               ["Respostas salvas do Direct (bf, natal, blog, valor, zap, obg)", "...\\11_INSTAGRAM_RESPOSTAS_SALVAS.txt",
                "Download → Divulgacao_Blog → 11_INSTAGRAM_RESPOSTAS_SALVAS.txt"],
               ["Links com rastreio", "...\\05_LINKS_RASTREAVEIS.txt", "Download → Divulgacao_Blog → 05_LINKS_RASTREAVEIS.txt"],
               ["Calendário do Instagram (.ics)", "...\\12_CALENDARIO_INSTAGRAM.ics", "Download → 12_CALENDARIO_INSTAGRAM.ics"],
               ["Plano Turbinar", "D:\\Projeto_Blog_Comprenolink\\0- Pendencias\\5_Plano_turbinar_anuncio_instagram", "–"],
               ["Cronograma de pendências", "D:\\Projeto_Blog_Comprenolink\\0- Pendencias\\1_Pendencias", "–"],
               ["Este guia", "D:\\Projeto_Blog_Comprenolink\\0- Pendencias\\3_Guia_Passo_a_Passo_Instagram_2026\\Guia_Passo_a_Passo_Instagram_2026.pdf", "–"],
           ], [0.3, 0.4, 0.3]),
           Spacer(1, 10),
           P("Regras de ouro", "h2"),
           tabela([
               ["Sempre", "Nunca"],
               ["Aviso de link de afiliado nos textos", "Preço, \"menor preço\" ou \"melhor preço\""],
               ["\"Confira o valor do dia no Mercado Livre\"", "Promessas de saúde ou estética"],
               ["Responder comentários e mensagens no mesmo dia", "Comprar seguidores, seguir/deixar de seguir em massa, robôs"],
               ["Plano Free do ManyChat (sem cartão)", "Clicar em \"Start Free Trial\" ou \"Experimente 14 dias\" do ManyChat"],
           ], [0.5, 0.5], extra=[("BACKGROUND", (0, 0), (0, 0), VERDE), ("BACKGROUND", (1, 0), (1, 0), VERMELHO)])]
    return st


if __name__ == "__main__":
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.8 * cm, rightMargin=1.8 * cm, topMargin=1.6 * cm,
                            bottomMargin=1.8 * cm, title="Guia Passo a Passo Instagram 2026", author="comprenolink.net")
    doc.build(montar(), onFirstPage=capa, onLaterPages=rodape)
    print("PDF:", SAIDA)
