# -*- coding: utf-8 -*-
"""PDF "Pesquisa_Google_Meta_Indexacao": consultas de 13/11/2026 sobre comprenolink.net e @compre.no.link (Transparência do Google,
Biblioteca de Anúncios da Meta, indexação) + checagem das 17 páginas do blog (ao vivo) + o que foi corrigido e o que falta.
Rodar:  python -X utf8 gerar_pesquisa_google_meta.py
Saída:  D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Pesquisa_Google_Meta_Indexacao_2026-11-13.pdf
"""
import html
import os
import re
import sys
import urllib.request
from datetime import date

AQUI = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, AQUI)
import gerar_pendencias_detalhado as base  # noqa: E402
from gerar_pendencias_detalhado import (AZUL, AZUL_C, LARANJA, LARANJA_C, P, VERDE, VERDE_C, VERMELHO, VERMELHO_C,  # noqa: E402
                                        bloco, faixa, info, passos, tabela)
from reportlab.lib.pagesizes import A4  # noqa: E402
from reportlab.lib.units import cm  # noqa: E402
from reportlab.platypus import PageBreak, SimpleDocTemplate, Spacer  # noqa: E402

SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Pesquisa_Google_Meta_Indexacao_2026-11-13.pdf"
SITE = "https://comprenolink.net"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Chrome/120 Safari/537.36"}
base.HOJE = date(2026, 11, 13)


def baixa(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90).read().decode("utf-8", "ignore")


def paginas():
    mapa = baixa(SITE + "/page-sitemap.xml")
    urls = re.findall(r"<loc><!\[CDATA\[(.*?)\]\]></loc>", mapa)
    linhas = []
    for u in urls:
        try:
            r = urllib.request.urlopen(urllib.request.Request(u, headers=UA), timeout=90)
            c = r.read().decode("utf-8", "ignore")
            st = r.status
        except Exception as e:  # noqa: BLE001
            linhas.append([u.replace(SITE, "") or "/", "erro", str(e)[:50], "0", ""])
            continue
        t = html.unescape(re.search(r"<title>(.*?)</title>", c).group(1)).replace(" - comprenolink.net", "") if re.search(r"<title>(.*?)</title>", c) else "?"
        d = re.search(r'<meta name="description" content="(.*?)"', c)
        linhas.append([u.replace(SITE, "") or "/", str(st), t[:58], str(len(d.group(1)) if d else 0), "melhor" if "melhor" in t.lower() else ""])
    return linhas


def conteudo():
    pg = paginas()
    com_melhor = sum(1 for x in pg if x[4])
    st = [Spacer(1, 0.4 * cm), P("PESQUISA: GOOGLE, META E INDEXAÇÃO", "capa_t"), Spacer(1, 4),
          P("comprenolink.net e @compre.no.link<br/>Consultas e correções de sexta 13/11/2026", "capa_s"), Spacer(1, 8),
          bloco("Conclusão", [
              "<b>Google Ads: nenhum anúncio.</b> A Central de Transparência do Google não tem anúncio ligado ao blog (0 resultados em todas as consultas).",
              "<b>Meta: 1 anúncio ativo do perfil.</b> A Biblioteca de Anúncios mostra um anúncio patrocinado \"Compre no Link\" no <b>Instagram</b>, ativo desde 12/11/2026. "
              "Bate com o teste de R$ 50 publicado em 12/11, que termina hoje às 23:59.",
              f"<b>Blog pronto para o Google:</b> as {len(pg)} páginas do mapa do site respondem 200, sem bloqueio, com título, descrição e endereço canônico.",
              "<b>Search Console já está configurado.</b> O diário de bordo registra que a página /presentes-de-natal/ está no Google (12/11) e que a indexação de /fones-bluetooth/ foi solicitada. "
              "Pelo lado de fora não consegui confirmar: o Google pediu captcha (não contorno) e o Bing não mostrou páginas do blog."], VERDE, VERDE_C),
          Spacer(1, 6),
          bloco("Corrigido hoje (13/11)", [
              "Item 14 (Motorola Moto G24): \"Melhor custo-benefício\" em \"Ideal para\" virou \"Uso no dia a dia\".",
              "Item 63 (Caixa Amplificada Mondial CM-700): selo \"Festa Garantida\" virou \"Som para Festas\".",
              "Páginas de categoria, Black Friday, Início e menu republicados. Backup do guia: pagina_2026-11-13_13h5819 e 13h5836.",
              "Pacote do dia 23/11 (Smartwatch): o link #item-212 apontava para outro produto e foi trocado por #item-209. Os outros pacotes de 16/11 a 23/12 já estavam certos.",
              "Títulos das páginas (Início, Guia e 9 categorias) e frase do site sem \"melhor\"; menu e botões trocados; textos dos itens 14 e 63 e introduções de 4 categorias ajustados, com backup. O endereço do guia não mudou.",
              "Cópia de celular dos pacotes de 09/12, 11/12 e 14/12 sincronizada com a pasta de divulgação (produtos novos: Árvore de Natal, Perfume Khamrah e Pisca LED)."],
                VERDE, VERDE_C), Spacer(1, 6),
          bloco("Ainda falta (precisa da sua decisão)", [
              (f"Títulos das páginas com \"melhor\" ou \"melhores\": {com_melhor} de {len(pg)}. Sugestão: trocar por algo neutro. Só altero com o seu OK." if com_melhor else
               "Rodapé do tema Futurio ainda mostra \"Melhores Produtos 2026\": dono troca em Aparência > Personalizar > Rodapé para \"Guia de Produtos 2026\"."),
              "Descrições de Contato, Sobre e Privacidade com 336 a 385 caracteres (o Google corta em cerca de 160) e 2 títulos H1 na página inicial.",
              "Catálogo do WhatsApp: vocês trabalham só com categorias, mas o catálogo ainda tem 16 itens de produto (CNL), com links desatualizados e o Smartwatch já fora do blog. Apagar é com você.",
              "A Black Friday é em 27/11: confira no Search Console se /black-friday/ e o guia estão indexados."], LARANJA, LARANJA_C),
          Spacer(1, 8), P("Resumo das consultas", "h2"),
          tabela(["Fonte", "O que consultei", "Resultado"],
                 [["Google, Transparência de Anúncios", "comprenolink.net por anunciante e por domínio, Brasil", "0 resultados"],
                  ["Google, Transparência de Anúncios", "\"Compre no Link\" (nome) e tópico Propaganda política", "0 resultados"],
                  ["Meta, Biblioteca de Anúncios", "compre.no.link, Brasil, todos os anúncios", "1 anúncio ativo do perfil (Instagram, desde 12/11/2026)"],
                  ["Google, busca site:comprenolink.net", "Páginas indexadas", "Não foi possível: captcha do Google"],
                  ["Bing, busca site:comprenolink.net", "Indício de indexação", "Nenhuma página do blog (inconclusivo)"],
                  ["Blog, robots.txt e sitemap", "Bloqueios e mapa do site", f"Liberado; sitemap com {len(pg)} páginas"]],
                 [0.27, 0.43, 0.3], cor=AZUL)]

    st += [PageBreak(), faixa("1", "Meta: anúncio ativo no Instagram", "Biblioteca de Anúncios da Meta • compre.no.link • Brasil", AZUL), Spacer(1, 6),
           info([("Anunciante", "Compre no Link (Patrocinado)"),
                 ("Situação", "ATIVO, veiculação iniciada em 12 de novembro de 2026"),
                 ("Plataforma", "Instagram"),
                 ("Identificação da biblioteca", "2192958427965624 (o anúncio tem várias versões)"),
                 ("Texto do anúncio", "\"Fones, caixas de som, TVs e acessórios reunidos por categoria. Compare com calma e escolha o que combina com o seu dia a dia. "
                                      "Toque em Saiba mais e veja no site.\" • \"Publicidade · Contém link de afiliado: posso receber comissão sem custo extra para você.\""),
                 ("Título e botão", "Título \"Tecnologia sem complicação\"; botão mostrado como \"Learn More\" (em inglês na Biblioteca)")]),
           Spacer(1, 6),
           bloco("O que está bom", ["Traz o aviso de publicidade e de link de afiliado.",
                                    "Sem preço, sem \"melhor\", sem \"mais vendido\" e sem promessa de saúde ou estética."], VERDE, VERDE_C), Spacer(1, 6),
           bloco("O que conferir", [
               "O período: o teste vai de 12/11 a 13/11 às 23:59 (R$ 50). A Biblioteca ainda mostra \"Ativo\" porque hoje é o último dia.",
               "O botão em inglês (\"Learn More\"): conferir se aparece assim para o público.",
               "Resultado: alcance, cliques e custo por clique no Gerenciador de Anúncios. A avaliação está marcada para 16/11 às 20:40.",
               "Termos do ML Afiliados: confirmar se anúncio pago com link de afiliado é permitido.",
               "Limite desta consulta: a busca por palavra-chave traz mais de 50 mil anúncios sem relação. Vi o primeiro bloco; para ver todos, filtre pelo anunciante \"Compre no Link\"."],
                 LARANJA, LARANJA_C)]

    st += [PageBreak(), faixa("2", "Google: anúncios e indexação", "Central de Transparência de Anúncios, Search Console e busca", VERDE), Spacer(1, 6),
           P("A) Central de Transparência de Anúncios do Google", "h2"),
           P("Mostra só anúncios do Google (Pesquisa, YouTube, Display). Em todas as consultas o resultado foi <b>0</b>: nenhum anúncio do Google aponta para comprenolink.net, "
             "nenhum anunciante chamado \"Compre no Link\" e nenhum anúncio político ligado ao domínio. É o esperado para um blog que divulga de forma orgânica. "
             "Ela não traz visita nem venda: serve só para conferir.", "p"),
           P("B) O blog está liberado para o Google?", "h2"),
           tabela(["Teste", "Resultado"],
                  [["robots.txt", "Libera tudo, só protege a área de administração, e aponta para o sitemap."],
                   ["Marcação noindex", "Não existe. As páginas têm só \"max-image-preview:large\"."],
                   ["sitemap.xml", f"Funciona e lista {len(pg)} páginas (All in One SEO). Deu 403 só para um falso Googlebot."],
                   ["Search Console", "Já configurado pelo dono. /presentes-de-natal/ está no Google; indexação de /fones-bluetooth/ solicitada em 12/11."]],
                  [0.28, 0.72], cor=VERDE), Spacer(1, 6),
           P("C) Próximos passos no Search Console", "h2"),
           passos([("Abra o Search Console", "https://search.google.com/search-console, na conta do blog."),
                   ("Confira o mapa do site", "Menu <b>Sitemaps</b>: sitemap.xml deve estar com status \"Sucesso\"."),
                   ("Peça a indexação", "Menu <b>Inspeção de URL</b> > <b>Solicitar indexação</b> para: /black-friday/, a página inicial e o guia /melhores-produtos-mercado-livre-2026/."),
                   ("Acompanhe", "Menu <b>Páginas</b>: quais estão indexadas e quais têm erro. A Black Friday é em 27/11.")], VERDE)]

    st += [PageBreak(), faixa("3", f"Checagem técnica das {len(pg)} páginas", "Todas as páginas do sitemap • lidas ao vivo em 13/11/2026", LARANJA), Spacer(1, 6),
           P("A coluna \"Descrição\" mostra os caracteres da meta descrição (o Google mostra cerca de 155 a 160). A coluna \"Atenção\" marca títulos com \"melhor\".", "p"),
           Spacer(1, 4), tabela(["Página", "Status", "Título", "Descrição", "Atenção"], pg, [0.27, 0.08, 0.45, 0.1, 0.1], cor=LARANJA), Spacer(1, 6),
           bloco("Ajustes sugeridos (só com o seu OK)", [
               "Padrão neutro para os títulos, por exemplo \"Achados do Mercado Livre por categoria\" e \"Categoria: ofertas selecionadas do Mercado Livre\".",
               "Encurtar as descrições de Contato, Sobre e Privacidade para cerca de 155 caracteres.",
               "Deixar um só título H1 na página inicial."], AZUL, AZUL_C)]
    return st


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=2.2 * cm, bottomMargin=1.5 * cm,
                            title="Pesquisa Google, Meta e indexação (comprenolink.net)", author="comprenolink.net")
    doc.build(conteudo(), onFirstPage=base.cabecalho_rodape, onLaterPages=base.cabecalho_rodape)
    print("PDF:", SAIDA)


if __name__ == "__main__":
    main()
