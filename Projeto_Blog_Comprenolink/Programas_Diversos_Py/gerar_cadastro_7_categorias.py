# -*- coding: utf-8 -*-
"""PDF "Cadastrar_7_categorias_WhatsApp": passo a passo e textos prontos das 7 categorias que faltam no catálogo do WhatsApp Business.
Lê nome e descrição de 06_CATALOGO_WHATSAPP/CATEGORIAS/CATALOGO_CATEGORIAS_TEXTOS.txt e monta o LINK CURTO (o campo Link do WhatsApp aceita 75 caracteres).
Rodar:  python -X utf8 gerar_cadastro_7_categorias.py
Saída:  D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Cadastrar_7_categorias_WhatsApp_2026-11-01.pdf
"""
import os
import re
import sys
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gerar_pendencias_detalhado as base  # noqa: E402
from gerar_pendencias_detalhado import (AZUL, LARANJA, LARANJA_C, P, VERDE, VERDE_C, VERMELHO, VERMELHO_C,  # noqa: E402
                                        bloco, caixa_texto, faixa, info, passos, tabela)
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer  # noqa: E402

CAT = "D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento/Celular_Whatsapp/06_CATALOGO_WHATSAPP/CATEGORIAS"
SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Cadastrar_7_categorias_WhatsApp_2026-11-01.pdf"
base.HOJE = date(2026, 11, 1)
FALTAM = ["tecnologia-e-informatica", "audio-e-tv", "casa-e-eletrodomesticos", "casa-cama-e-decoracao",
          "ferramentas-e-utilidades", "esporte-e-fitness", "beleza-e-saude"]
SITE = "https://comprenolink.net/"


def ler():
    txt = open(CAT + "/CATALOGO_CATEGORIAS_TEXTOS.txt", encoding="utf-8-sig").read()
    itens = {}
    for bloco_t in re.split(r"={20,}\n", txt):
        m = re.search(r"CÓDIGO: CAT-(\S+)\s+FOTO: (\S+)", bloco_t)
        if not m:
            continue
        resto = txt.split(bloco_t, 1)[1] if False else None  # noqa: F841
    # o arquivo alterna "cabeçalho" e "corpo" separados por linhas de ====
    partes = re.split(r"={20,}\n", txt)
    for i, p in enumerate(partes):
        m = re.search(r"CÓDIGO: CAT-(\S+)\s+FOTO: (\S+)", p)
        if m and i + 1 < len(partes):
            corpo = partes[i + 1]
            nome = re.search(r"NOME:\n(.+?)\n", corpo).group(1).strip()
            desc = re.search(r"DESCRIÇÃO:\n(.+?)\n\n", corpo, re.S).group(1).strip()
            itens[m.group(1)] = dict(nome=nome, desc=desc, foto=m.group(2))
    return itens


TXT = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Textos_7_categorias_WhatsApp_COPIAR.txt"


def sem_emoji(t):
    return re.sub(r"[\U00010000-\U0010ffff\u2600-\u27bf\ufe0f\u200d]", "", t).strip()


def grava_txt(itens):
    L = ["TEXTOS DAS 7 CATEGORIAS QUE FALTAM NO CATÁLOGO DO WHATSAPP (copiar e colar) – 01/11/2026",
         "Campos de cada item: foto, NOME, preço em branco, DESCRIÇÃO, LINK (curto, cabe nos 75 caracteres) e CÓDIGO.",
         "Este arquivo mantém os emojis do nome. Passo a passo no PDF Cadastrar_7_categorias_WhatsApp_2026-11-01.pdf.", ""]
    for s in FALTAM:
        d = itens[s]
        L += ["=" * 60, f"CÓDIGO: CAT-{s}      FOTO: {d['foto']}", "=" * 60, "NOME:", d["nome"], "", "PREÇO: (deixe em branco)", "",
              "DESCRIÇÃO:", d["desc"], "", "LINK:", f"{SITE}{s}/?utm_source=whatsapp", ""]
    open(TXT, "w", encoding="utf-8-sig").write("\n".join(L))


def conteudo():
    itens = ler()
    grava_txt(itens)
    itens = {k: dict(v, nome=sem_emoji(v["nome"])) for k, v in itens.items()}
    st = [Spacer(1, 0.4 * cm), P("CADASTRAR AS 7 CATEGORIAS NO WHATSAPP", "capa_t"), Spacer(1, 4),
          P("Catálogo do WhatsApp Business • textos prontos para copiar<br/>Preparado em 01/11/2026", "capa_s"), Spacer(1, 8),
          info([("Situação", "Conferido no WhatsApp Web em 01/11: o catálogo tem os 17 produtos e só 2 categorias (Moda Infantil & Juvenil e Bebê & Maternidade). Faltam 7."),
                ("Tempo", "Cerca de 4 minutos por categoria, 30 minutos no total. Pode fazer em dias diferentes."),
                ("Onde fazer", "No computador, pelo WhatsApp Web (mais fácil, a foto vem direto da pasta) ou no celular."),
                ("Fotos", "D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Celular_Whatsapp\\06_CATALOGO_WHATSAPP\\CATEGORIAS\\fotos (uma por categoria, nome CAT-....jpg)."),
                ("Atenção", "O campo Link do WhatsApp aceita só 75 caracteres. Os links abaixo já cabem. Não use os links longos com utm."),
                ("Para copiar", "Textos com emoji no arquivo Textos_7_categorias_WhatsApp_COPIAR.txt (mesma pasta). O PDF não mostra emoji; copie o NOME do .txt.")]),
          Spacer(1, 8), P("Lista das 7 categorias", "h2"),
          tabela(["Nº", "Categoria", "Foto", "Link (cabe nos 75 caracteres)"],
                 [[str(i), itens[s]["nome"], itens[s]["foto"], f"{SITE}{s}/?utm_source=whatsapp"] for i, s in enumerate(FALTAM, 1)],
                 [0.05, 0.3, 0.32, 0.33], cor=VERDE), Spacer(1, 6),
          bloco("Regras de ouro", ["Preço: deixar em branco (o valor muda no Mercado Livre).",
                                   "Não mudar os textos: já têm o aviso de link de afiliado e estão dentro da política.",
                                   "O item pode ficar \"em análise\" por até 24 h. Isso é normal. Se for recusado, apague e me avise."], VERMELHO, VERMELHO_C),
          PageBreak(), faixa("1", "Passo a passo (vale para as 7)", "No WhatsApp Web, no computador", AZUL), Spacer(1, 6),
          passos([("Abra o WhatsApp Web", "web.whatsapp.com, com o WhatsApp Business conectado. Clique no ícone da loja (Ferramentas comerciais) → <b>Catálogo</b>."),
                  ("Clique em Adicionar item", "Primeiro botão da lista, com o sinal de +."),
                  ("Foto", "Clique em <b>Adicionar imagens</b> e escolha o arquivo da categoria na pasta de fotos (nome na caixa da categoria)."),
                  ("Nome", "Copie o <b>NOME</b> da caixa, com o emoji."),
                  ("Preço", "<b>Deixe em branco.</b>"),
                  ("Descrição", "Copie a <b>DESCRIÇÃO</b> da caixa."),
                  ("Link", "Copie o <b>LINK</b> da caixa (é o curto). Confira que ficou inteiro."),
                  ("Código do item", "Copie o <b>CÓDIGO</b> (CAT-...). Ele ajuda a achar o item depois."),
                  ("Salve", "Clique em <b>Salvar</b> e espere alguns segundos até o item aparecer na lista.")], AZUL),
          Spacer(1, 6), bloco("Como saber que deu certo", ["O catálogo passa a mostrar 9 itens de categoria (2 de hoje + 7 novos) e os 17 produtos.",
                                                         "Toque no item e confira se o link abre a página da categoria no blog."], VERDE, VERDE_C)]
    for i, s in enumerate(FALTAM, 1):
        d = itens[s]
        texto = (f"CÓDIGO DO ITEM: CAT-{s}\nFOTO: {d['foto']}\n\nNOME:\n{d['nome']}\n\nPREÇO: deixar em branco\n\nDESCRIÇÃO:\n{d['desc']}\n\n"
                 f"LINK:\n{SITE}{s}/?utm_source=whatsapp")
        st += [PageBreak() if i % 2 == 1 else Spacer(1, 12), faixa(str(i + 1), d["nome"], "Categoria " + str(i) + " de 7", LARANJA), Spacer(1, 6),
               caixa_texto("Copie cada campo do quadro abaixo", texto)]
    st += [Spacer(1, 10), P("Lista de conferência", "h2"),
           tabela(["OK", "Categoria", "Feito em"], [["[   ]", itens[s]["nome"], "___/___"] for s in FALTAM], [0.08, 0.67, 0.25], cor=VERDE), Spacer(1, 6),
           bloco("Depois que terminar", ["Me avise. Eu atualizo a planilha (Cadastrado = S) e confiro o catálogo no WhatsApp Web se você autorizar de novo.",
                                         "Apague também o item CNL-111 (Kit Skincare): WhatsApp Business → Catálogo → item → Excluir."], VERDE, VERDE_C)]
    return st


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Cadastrar as 7 categorias no WhatsApp (comprenolink.net)", author="comprenolink.net")
    doc.build(conteudo(), onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
