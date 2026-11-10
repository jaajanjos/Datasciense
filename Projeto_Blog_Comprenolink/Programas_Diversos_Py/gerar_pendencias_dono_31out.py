# -*- coding: utf-8 -*-
"""PDF "Pendencias_Dono_Passo_a_Passo": tudo que o DONO precisa fazer a partir de 31/10/2026, com passo a passo.
Rodar:  python -X utf8 gerar_pendencias_dono_31out.py
Saída:  D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Pendencias_Dono_Passo_a_Passo_2026-10-31.pdf
        e cópia em \\\\lenovo\\D\\Projeto_Blog_Comprenolink\\0- Pendencias\\1_Pendencias (a pedido do dono).
Usa os componentes visuais de gerar_pendencias_detalhado.py (mesma pasta). Caminhos com barra normal.
"""
import glob
import os
import re
import shutil
import sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gerar_pendencias_detalhado as base  # noqa: E402
from gerar_pendencias_detalhado import (AZUL, AZUL_C, LARANJA, LARANJA_C, P, VERDE, VERDE_C, VERMELHO, VERMELHO_C,  # noqa: E402
                                        bloco, caixa_texto, faixa, info, passos, tabela)
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer  # noqa: E402

NOME = "Pendencias_Dono_Passo_a_Passo_2026-10-31.pdf"
SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/" + NOME
COPIA = r"\\lenovo\D\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias"
PACOTES = "D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento/Celular_Whatsapp/07_PACOTE_DO_DIA"
base.HOJE = date(2026, 10, 31)
ULTIMO_AGENDADO = date(2026, 11, 28)  # post e Reels já programados no Instagram até aqui (29/11 entra na noite de 31/10)


def dias_do_plano():
    """(data, dia da semana, produto) de cada pasta do pacote do dia que tem produto."""
    saida = []
    for pasta in sorted(glob.glob(PACOTES + "/2026-*")):
        m = re.match(r"(\d{4})-(\d{2})-(\d{2})_(\w+)", os.path.basename(pasta))
        arq = os.path.join(pasta, "1_TEXTOS_DO_DIA.txt")
        if not m or not os.path.exists(arq):
            continue
        txt = open(arq, encoding="utf-8-sig").read()
        cab = re.findall(r"^(\d\d:\d\d)\s+(.+)$", txt, flags=re.M)
        tem_post = any("Post no feed" in c for _, c in cab)
        envios = [f"{h} {re.sub(r'^(Instagram|WhatsApp) – ', '', c).split(' (')[0].split(' com ')[0]}" for h, c in cab
                  if "Post no feed" not in c and "Reels" not in c]
        produto = "Dia de lista (sem post no Instagram)"
        if tem_post:
            achou = re.search(r"[🔥🎄]\s*([^\n]+)", txt.split("Post no feed", 1)[1])
            produto = re.sub(r"^(Black Friday|Natal):\s*", "", achou.group(1).strip()) if achou else "?"
        saida.append((date(int(m[1]), int(m[2]), int(m[3])), m[4], produto, envios, tem_post))
    return saida


def conteudo():
    plano = dias_do_plano()
    st = [Spacer(1, 0.4 * cm), P("O QUE VOCÊ PRECISA FAZER", "capa_t"), Spacer(1, 4),
          P("A partir de sábado 31/10/2026, com passo a passo<br/>Instagram @compre.no.link • WhatsApp (11) 99495-9657 • comprenolink.net", "capa_s"),
          Spacer(1, 8),
          info([("Em uma frase", "Hoje à noite, só deixe o computador ligado. A partir de segunda 02/11, nos dias de post, publique o Story e os dois "
                                 "envios de WhatsApp. Quinta 05/11 tem a reunião."),
                ("O que já está pronto", "Post e Reels agendados no Instagram de 02/11 a 28/11 (19:00 e 19:05). WhatsApp Business configurado, "
                                         "link do Canal recebido (31/10 17:04). Painel de vendas atualizado em 31/10 16:37 (19 vendas)."),
                ("Onde estão os arquivos", "D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Celular_Whatsapp\\07_PACOTE_DO_DIA (uma pasta por dia, com feed.png, story.png, "
                                           "status.png, reels.mp4 e 1_TEXTOS_DO_DIA.txt)."),
                ("Dúvida?", "Escreva ao Claude com um print da tela. Se a rotina de agendamento falhar, escreva \"agendar DD/MM\".")]),
          Spacer(1, 8), P("Resumo em ordem de data", "h2"),
          tabela(["Quando", "Quem", "O que", "Tempo"],
                 [["Sáb 31/10, noite (~20:39)", "Claude (você só deixa ligado)", "Agendar 29/11 no Instagram. Computador ligado, app Claude e Chrome abertos", "0 min"],
                  ["Dom 01/11, noite", "Claude (você só deixa ligado)", "Agendar 30/11. O mesmo cuidado", "0 min"],
                  ["Seg 02/11, 19:10 a 19:20", "Você", "Story com link (19:10), Status do WhatsApp (19:15) e Canal (19:20)", "10 min"],
                  ["Dias de post seguintes", "Você", "A mesma rotina das 19:10 às 19:20 (veja o calendário na parte 3)", "10 min"],
                  ["Dias de lista (ex.: ter 03/11)", "Você", "12:00 nos Grupos do WhatsApp onde é permitido (parte 2, item E)", "5 min"],
                  ["Qui 05/11, 10:00", "Você + sócio", "Reunião sobre o Turbinar e os termos do ML Afiliados", "reunião"],
                  ["Quando puder", "Você", "Confirmar a conta do CSV de vendas e a sincronização entre os PCs", "10 min"]],
                 [0.23, 0.2, 0.47, 0.1], cor=LARANJA), Spacer(1, 6),
          bloco("Regras de ouro (em todo texto que você mandar)", [
              "Sem preço e sem \"menor/melhor preço\": use \"confira o valor do dia no Mercado Livre\".",
              "Sem \"mais vendido\", \"líder\" ou \"oferta do mês\", e sem promessa de saúde ou estética.",
              "Sempre o aviso de link de afiliado (já está nos textos prontos).",
              "Use os textos exatamente como estão em 1_TEXTOS_DO_DIA.txt: eles já foram revisados."], VERMELHO, VERMELHO_C)]

    # ---------------- Parte 1
    st += [PageBreak(), faixa("1", "Deixar tudo ligado para o Claude agendar", "Hoje 31/10 e amanhã 01/11 • sem trabalho, só cuidado", AZUL), Spacer(1, 6),
           P("Todas as noites, por volta das 20:39, o Claude abre o Instagram no Chrome e programa o post (19:00) e o Reels (19:05) do dia que acabou de "
             "entrar na janela dos 29 dias. Para isso funcionar, estes quatro itens precisam estar assim:"),
           passos([
               ("Computador ligado e sem suspender", "Não deixe o Windows entrar em suspensão nem hibernar. Está configurado para nunca suspender na tomada: "
                "só não desligue nem feche a tampa/tela de forma que ele durma."),
               ("App Claude aberto", "O agendamento é uma rotina do app. Se o app for fechado, a rotina se perde. Pode minimizar, mas não feche."),
               ("Chrome aberto, com o Instagram logado em @compre.no.link", "Não feche o Chrome nem saia da conta. Se o Instagram pedir login ou "
                "código, entre e avise o Claude."),
               ("Não use o Chrome entre 20:30 e 21:00", "Se precisar usar o computador, use outro navegador. O Claude vai clicar na aba do Instagram.")], AZUL),
           Spacer(1, 6),
           bloco("Se algo der errado", [
               "Mensagem do Claude dizendo \"Escolha uma data dentro dos próximos 29 dias\": é normal, ele espera 30 minutos e tenta de novo.",
               "Se ele avisar que o Chrome está desconectado: abra o Chrome, abra o Instagram e escreva \"agendar DD/MM\" para ele repetir.",
               "Nada é publicado fora do horário: a programação só marca a data, e o Instagram publica sozinho às 19:00 e 19:05 do dia."],
                LARANJA, LARANJA_C)]

    # ---------------- Parte 2
    st += [PageBreak(), faixa("2", "Rotina dos dias de post (das 19:10 às 19:20)", "A partir de seg 02/11 • 10 minutos por dia", VERDE), Spacer(1, 6),
           P("O post do feed (19:00) e o Reels (19:05) saem sozinhos. Você cuida do Story, do Status e, em alguns dias, do Canal, todos com a pasta do dia aberta. "
             "<b>Na véspera ou de manhã:</b> garantir que as imagens do dia estão no seu celular. "
             "Alguns dias têm um envio extra (por exemplo 26/11 às 20:00, \"lembrete forte\"): nesse caso siga o bloco do mesmo horário no 1_TEXTOS_DO_DIA.txt.", "p"),
           P("A) Preparar o celular (faça uma vez por dia de post, de manhã)", "h2"),
           passos([
               ("Abra a pasta do dia no computador", "D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Celular_Whatsapp\\07_PACOTE_DO_DIA\\AAAA-MM-DD_dia (por exemplo 2026-11-02_seg)."),
               ("Leve estes 3 arquivos para o celular", "<b>story.png</b>, <b>status.png</b> e <b>feed.png</b>. Jeito mais rápido: no computador, abra "
                "web.whatsapp.com com o número do blog, abra a conversa com você mesmo (\"Você\"), anexe os 3 arquivos e envie. No celular, abra cada imagem e salve na galeria. "
                "(Outros jeitos: e-mail para você mesmo ou cabo USB.)"),
               ("Deixe o arquivo de textos aberto", "<b>1_TEXTOS_DO_DIA.txt</b> da mesma pasta. É dele que você copia os textos e o link do Story.")], VERDE),
           Spacer(1, 6),
           P("B) 19:10 • Story no Instagram, com adesivo de link", "h2"),
           passos([
               ("Abra o Instagram @compre.no.link no celular", "Confira no canto da tela se é a conta certa."),
               ("Crie o Story", "Toque no <b>+</b> → <b>Story</b> → escolha <b>story.png</b> na galeria."),
               ("Copie o link do adesivo", "No <b>1_TEXTOS_DO_DIA.txt</b>, bloco \"19:10 Instagram – Story com adesivo de link\", linha <b>Link para o adesivo:</b>. "
                "Copie a linha inteira, do https até o final (#item-xx)."),
               ("Coloque o adesivo de link", "Toque no ícone do adesivo (carinha) → <b>Link</b> → cole o link → <b>Concluído</b>. Arraste o adesivo para uma área vazia da imagem."),
               ("Publique às 19:10", "Toque em <b>Seu story</b>. Se o adesivo de Link não aparecer, tire um print da tela e mande ao Claude.")], VERDE),
           Spacer(1, 6),
           P("C) 19:15 • Status do WhatsApp", "h2"),
           passos([
               ("Abra o WhatsApp Business → Status → câmera/lápis", "Escolha <b>status.png</b> na galeria."),
               ("Legenda", "Copie do <b>1_TEXTOS_DO_DIA.txt</b> o bloco \"19:15 WhatsApp – Status\" (do título do produto até a linha do aviso de afiliado) e cole na legenda."),
               ("Envie", "Toque na seta verde. Fica no ar por 24 horas.")], VERDE),
           P("D) 19:20 • Canal do WhatsApp", "h2"),
           passos([
               ("Abra o Canal \"Compre no Link – Achados do Mercado Livre\"", "Aba <b>Atualizações</b> → Canais."),
               ("Anexe <b>feed.png</b>", "Toque no clipe → Galeria → feed.png."),
               ("Legenda", "Copie o bloco \"19:20 WhatsApp – Canal\" do 1_TEXTOS_DO_DIA.txt (do título do produto até o aviso de afiliado), cole e envie. "
                "<b>O Canal só tem envio nos dias em que a tabela da parte 3 mostra \"19:20 Canal\".</b>")], VERDE),
           Spacer(1, 6),
           P("E) Dias de lista (por exemplo 03/11, 10/11 e 17/11): 12:00 nos Grupos do WhatsApp", "h2"),
           passos([
               ("Quando", "Nesses dias não há post no Instagram. O envio é só nos Grupos, às 12:00, e <b>só nos grupos onde você tem permissão para divulgar</b>."),
               ("Arquivos", "Na pasta do dia: <b>campanha_12h00.png</b> e o bloco \"12:00 WhatsApp – Grupos\" do 1_TEXTOS_DO_DIA.txt."),
               ("Como enviar", "Abra o grupo permitido, anexe a imagem, cole o texto (com o link) e envie. Um grupo por vez, sem adicionar pessoas e sem envio em massa: "
                "o WhatsApp bloqueia o número.")], VERDE),
           Spacer(1, 6),
           bloco("E quem comentar BLACK no post?", [
               "O post diz \"Comente BLACK que eu te mando o link no Direct\". Quem comentar deve receber uma mensagem direta com o link do produto.",
               "Se quiser, peça ao Claude: <b>\"texto do Direct de DD/MM\"</b>. Ele gera na hora a mensagem com o link rastreável do dia.",
               "Responda no mesmo dia, de preferência até às 21:00, e nunca prometa preço."], AZUL, AZUL_C)]

    # ---------------- Parte 3: calendário
    linhas = []
    for d, sem, prod, envios, tem_post in plano:
        if not tem_post:
            sit = "Sem agendamento (só você envia)"
        else:
            sit = "Agendado (19:00 e 19:05)" if d <= ULTIMO_AGENDADO else "A agendar pelo Claude"
        linhas.append([f"{d:%d/%m}", sem, prod, "<br/>".join(envios) or "-", sit])
    st += [PageBreak(), faixa("3", "Calendário de cada dia", "02/11 a 23/12 • produto, seus envios e situação do agendamento", LARANJA), Spacer(1, 6),
           P("A coluna <b>Seus envios</b> mostra o que é com você em cada dia (leia o bloco de mesmo horário no 1_TEXTOS_DO_DIA.txt da pasta do dia). "
             "O post do feed e o Reels são do Claude. Os dias \"A agendar\" o Claude programa nas noites seguintes, um dia por noite, "
             "quando a janela de 29 dias do Instagram abre.", "p"), Spacer(1, 4),
           tabela(["Data", "Dia", "Produto ou atividade", "Seus envios", "Situação"], linhas, [0.08, 0.07, 0.35, 0.28, 0.22], cor=LARANJA, tam="cel")]

    # ---------------- Parte 4: reunião
    st += [PageBreak(), faixa("4", "Reunião de quinta 05/11, às 10:00", "Com o sócio • Turbinar e ML Afiliados", VERMELHO), Spacer(1, 6),
           P("A) O que levar", "h2"),
           passos([
               ("Plano Turbinar (PDF)", "D:\\Projeto_Blog_Comprenolink\\0- Pendencias\\5_Plano_turbinar_anuncio_instagram."),
               ("Painel de conversão e performance", "D:\\Projeto_Blog_Comprenolink\\Relatorios_Diarios_Anuncios (o PDF mais recente: Painel_conversao_performance_2026-10-31_16h37.pdf)."),
               ("Resultado das vendas", "19 vendas no histórico: 12 pendentes e 7 recusadas por \"conta vinculada\". Comissão pendente: R$ 172,00."),
               ("Termos do ML Afiliados sobre anúncio pago", "Leia antes a parte dos termos que trata de divulgação paga (Turbinar). Anote a dúvida e traga.")], VERMELHO),
           Spacer(1, 6),
           P("B) O que decidir", "h2"),
           tabela(["Decisão", "Perguntas para responder"],
                  [["Usar o Turbinar?", "Qual verba por dia? Quais produtos primeiro? Por quantos dias antes de avaliar?"],
                   ["Conta vinculada", "Por que 7 vendas foram recusadas (\"conta vinculada\")? Há algo a ajustar na conta do afiliado?"],
                   ["Texto das legendas", "Manter as legendas atuais (sem preço, sem \"mais vendido\")? Sim, é a recomendação."],
                   ["Quem faz o quê", "Quem publica os Stories e os envios do WhatsApp quando você não puder?"]],
                  [0.22, 0.78], cor=VERMELHO),
           Spacer(1, 6),
           P("C) Depois da reunião", "h2"),
           passos([("Me conte as decisões", "Escreva ao Claude em poucas linhas. Ele atualiza o plano e o diário de bordo."),
                   ("Recriar a rotina diária", "Depois de 05/11 a rotina de agendamento expira (dura 7 dias). O Claude recria e avisa.")], VERMELHO)]

    # ---------------- Parte 5: abertos
    st += [PageBreak(), faixa("5", "Confirmações e decisões em aberto", "Sem data fixa • quando puder", AZUL), Spacer(1, 6),
           P("A) A conta do CSV de vendas é a do blog?", "h2"),
           passos([
               ("Entre no ML Afiliados", "Com o login que você usa para o comprenolink.net."),
               ("Compare", "A lista de vendas deve ter as mesmas 19 vendas do arquivo vendas_ml_2026-10-31.csv e o total de comissão pendente de R$ 172,00."),
               ("Me avise", "Escreva \"é a do blog\" ou \"não é\". Se não for, me diga qual conta usar.")], AZUL),
           Spacer(1, 6),
           P("B) Os dois PCs estão sincronizando pastas?", "h2"),
           passos([
               ("Por que importa", "Em 31/10 o arquivo gerar_relatorio_atividade.py voltou sozinho a uma versão antiga. Algo pode estar copiando a pasta "
                "Programas_Diversos_Py de um PC para o outro e apagando alterações."),
               ("Verifique", "No outro PC (lenovo), veja se existe tarefa agendada, OneDrive, Syncthing ou script (como sincronizar_copias.py) que copie D:\\Projeto_Blog_Comprenolink."),
               ("Me avise", "Diga se existe e em que direção copia. Eu ajusto para não sobrescrever os arquivos novos.")], AZUL),
           Spacer(1, 6),
           P("C) Textos leves que não foram trocados (só se você quiser)", "h2"),
           tabela(["Onde", "O que aparece", "Sugestão"],
                  [["Air Fryer (11/11), legenda", "\"Ideal para: famílias, dieta e alimentação leve\"", "Trocar por \"famílias, quem tem pouco tempo\""],
                   ["Smart TV LG (26/11), foto", "A foto do fabricante traz a palavra \"melhor\"", "Manter (é imagem do fabricante) ou trocar a foto"]],
                  [0.25, 0.4, 0.35], cor=AZUL),
           P("Para trocar, escreva ao Claude \"troque o texto de 11/11\" (ou de 26/11). Ele altera o blog com backup, refaz o pacote e reagenda o dia.", "p"),
           Spacer(1, 6),
           bloco("Resumo do que o Claude faz sozinho", [
               "Agenda um dia por noite (~20:39) até 23/12 e confere no calendário do Instagram.",
               "Atualiza o diário de bordo em PDF ao fim de cada sessão (pasta 4_Relatorio_Ativ_Claude_no_Blog).",
               "Avisa em português quando terminar a atividade do dia ou quando algo travar.",
               "Nunca altera o blog sem backup e nunca posta nada fora do horário combinado."], VERDE, VERDE_C)]
    return st


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="O que o dono precisa fazer (comprenolink.net)", author="comprenolink.net")
    doc.build(conteudo(), onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA)
    try:
        os.makedirs(COPIA, exist_ok=True)
        shutil.copy2(SAIDA, os.path.join(COPIA, NOME))
        print("Cópia em:", os.path.join(COPIA, NOME))
    except OSError as e:
        print("Não consegui copiar para o lenovo:", e)


if __name__ == "__main__":
    main()
