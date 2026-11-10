# -*- coding: utf-8 -*-
"""Guia do sócio: como pedir ao Claude para publicar quando o dono não puder (mesmo PC do blog). Criado em 03/11/2026.
Rodar:  python -X utf8 gerar_guia_socio.py
Saída:  D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Guia_Socio_Como_Pedir_ao_Claude.pdf
Usa os componentes visuais de gerar_pendencias_detalhado.py (mesma pasta). Caminhos com barra normal.
"""
import os
import sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gerar_pendencias_detalhado as base  # noqa: E402
from gerar_pendencias_detalhado import (AZUL, AZUL_C, LARANJA, LARANJA_C, P, VERDE, VERDE_C, VERMELHO, VERMELHO_C,  # noqa: E402
                                        bloco, faixa, info, passos, tabela)
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import KeepTogether, PageBreak, SimpleDocTemplate, Spacer  # noqa: E402

SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Guia_Socio_Como_Pedir_ao_Claude.pdf"
base.HOJE = date(2026, 11, 3)


def conteudo():
    st = [Spacer(1, 0.2 * cm), P("GUIA DO SÓCIO", "capa_t"), Spacer(1, 2),
          P("Como pedir ao Claude para publicar quando o dono não puder<br/>"
            "Instagram @compre.no.link • WhatsApp do blog (11) 99495-9657 • comprenolink.net", "capa_s"), Spacer(1, 6),
          info([("Para que serve", "Quando o dono não puder publicar, você escreve ao Claude (no aplicativo deste computador) e ele publica o que está na pasta do dia. "
                                    "Você não precisa mexer no Instagram nem no WhatsApp: só direcionar e conferir."),
                ("Horários do dia", "Post no feed 19:00 e Reels 19:05 (o Claude agenda na noite anterior). Story com link 19:10. Status do WhatsApp 19:15. Canal do WhatsApp 19:20."),
                ("Materiais", "D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Celular_Whatsapp\\07_PACOTE_DO_DIA\\AAAA-MM-DD_dia (feed.png, story.png, status.png, reels.mp4 e 1_TEXTOS_DO_DIA.txt).")]),
          Spacer(1, 6),
          faixa("1", "Antes de pedir (30 segundos)", "Se algum item faltar, o Claude não consegue publicar", AZUL), Spacer(1, 3),
          passos([("Computador ligado e sem suspender", "Não desligue nem deixe dormir."),
                  ("Aplicativo do Claude aberto", "Pode minimizar, mas não feche."),
                  ("Chrome aberto com o Instagram e o WhatsApp Web logados", "Instagram @compre.no.link e WhatsApp Web do número do blog. Não saia das contas e não feche o Chrome."),
                  ("Se alguma conta pedir senha ou código", "Pare e chame o dono. O Claude nunca digita senha nem código de verificação.")], AZUL),
          Spacer(1, 8),
          faixa("2", "O que escrever ao Claude", "Em português, com a data quando for o caso", VERDE), Spacer(1, 3),
          tabela(["Você quer", "Escreva exatamente", "O que o Claude faz"],
                 [["Agendar o post e o Reels de um dia", "agendar 12/11", "Programa o post (19:00) e o Reels (19:05) no Instagram"],
                  ["Publicar o Story com link de hoje", "publicar o Story de hoje", "Cria o Story com o adesivo de link e o texto do dia"],
                  ["Publicar no WhatsApp", "publicar o Status e o Canal de hoje", "Posta o Status (19:15) e o Canal (19:20) com a imagem e a legenda do dia"],
                  ["Responder quem comentou BLACK", "texto do Direct de 12/11", "Escreve a mensagem com o link rastreável do dia"],
                  ["Ver se tudo saiu", "conferir o dia de hoje", "Confere o que foi publicado e avisa o que falta"],
                  ["Ver o limite de uso do plano", "conferir uso", "Informa quanto do limite semanal já foi usado"]],
                 [0.3, 0.3, 0.4], cor=VERDE), Spacer(1, 8),
          bloco("Regras de ouro (valem para tudo que for publicado)", [
              "Sem preço e sem \"mais vendido\", \"líder\" ou \"oferta do mês\". Sem promessa de saúde ou estética.",
              "Sempre o aviso de link de afiliado (#publi). Os textos prontos já têm.",
              "Grupos de WhatsApp: só onde o administrador permite divulgar, no máximo 1 mensagem por semana em cada grupo.",
              "Nunca escreva senha, código de verificação ou dados de cartão na conversa com o Claude."], VERMELHO, VERMELHO_C),
          Spacer(1, 6),
          faixa("3", "Se algo der errado", "Quase tudo tem solução rápida", LARANJA), Spacer(1, 3),
          tabela(["O que aconteceu", "O que fazer"],
                 [["O Claude pede senha, código ou aceite de termos", "Chame o dono. Essa parte é sempre de uma pessoa: o Claude para e avisa."],
                  ["O Claude avisa que o Chrome está desconectado", "Abra o Chrome, abra o Instagram e o WhatsApp Web, confira se estão logados e escreva de novo o pedido."],
                  ["Instagram diz \"escolha uma data dentro dos próximos 29 dias\"", "É normal: a data ainda não abriu. O Claude espera cerca de 30 minutos e tenta de novo."],
                  ["O limite de uso do plano acabou", "O Claude não consegue publicar até renovar (a contagem renova na segunda de madrugada). Plano B: publicar à mão, abaixo."],
                  ["O post saiu errado ou com texto fora da regra", "Avise o dono e escreva ao Claude \"corrigir o post de hoje\". Nunca deixe no ar texto com preço ou \"mais vendido\"."]],
                 [0.4, 0.6], cor=LARANJA), Spacer(1, 8),
          faixa("4", "Plano B: publicar à mão (se o Claude não puder)", "Cerca de 10 minutos por dia", AZUL), Spacer(1, 3),
          passos([("Abra a pasta do dia", "D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Celular_Whatsapp\\07_PACOTE_DO_DIA\\AAAA-MM-DD_dia e o arquivo 1_TEXTOS_DO_DIA.txt."),
                  ("Leve as imagens para o celular", "story.png, status.png e feed.png (WhatsApp Web para a conversa \"Você\" é o jeito mais rápido)."),
                  ("19:10 Story", "Instagram > + > Story > story.png > adesivo Link (cole o link do bloco das 19:10) > Seu story."),
                  ("19:15 Status", "WhatsApp Business > Status > status.png > cole a legenda do bloco das 19:15 > enviar."),
                  ("19:20 Canal", "Atualizações > Canal > feed.png > cole a legenda do bloco das 19:20 (só nos dias em que o bloco existir).")], AZUL),
          Spacer(1, 8),
          bloco("Datas-chave da Black Friday (não pode faltar publicação)", [
              "Ter 10/11, 12:00: lista nos grupos de WhatsApp que permitem. Qua 11/11: 11.11 (post, Reels, Story e Status).",
              "18/11 a 26/11: esquenta, 2 a 3 envios por dia. Qui 26/11, 20:00: lembrete forte (amanhã é Black Friday).",
              "Sex 27/11: dia D, às 08:00, 12:00 e 19:00. Seg 30/11: Cyber Monday, último dia da campanha.",
              "Dúvida de texto, regra, conta ou computador: chame o dono. Mais detalhes na atividade 7 do nova_pendencias.pdf."], VERMELHO, VERMELHO_C)]
    return st


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Guia do sócio – como pedir ao Claude", author="comprenolink.net")
    doc.build(conteudo(), onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA)
    # cópia na raiz de 0- Pendencias, a pedido do dono (03/11/2026)
    import shutil
    copia = "D:/Projeto_Blog_Comprenolink/0- Pendencias/Guia_Socio_Como_Pedir_ao_Claude.pdf"
    shutil.copy2(SAIDA, copia)
    print("Cópia:", copia)


if __name__ == "__main__":
    main()
