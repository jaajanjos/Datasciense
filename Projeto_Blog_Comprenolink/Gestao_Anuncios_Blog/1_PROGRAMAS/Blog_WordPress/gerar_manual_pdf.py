# -*- coding: utf-8 -*-
"""Gera Manual_Manutencao_Blog.pdf (passo a passo simples para quem vai usar o GerenciarBlog.exe)."""
import html
import os

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.platypus import (KeepTogether, PageBreak, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle)

PASTA = os.path.dirname(os.path.abspath(__file__))
RAIZ = os.path.normpath(os.path.join(PASTA, "..", ".."))  # pasta Gestao_Anuncios_Blog
SAIDA = os.path.join(RAIZ, "3_DOCUMENTACAO", "Blog_WordPress", "Manual_Manutencao_Blog.pdf")

AZUL = colors.HexColor("#0B5FA5")
CINZA = colors.HexColor("#444444")
AMARELO = colors.HexColor("#FFF4CC")
VERDE = colors.HexColor("#E6F4EA")
VERMELHO = colors.HexColor("#FDE8E8")
LINHA = colors.HexColor("#D0D7DE")

base = ParagraphStyle("base", fontName="Helvetica", fontSize=11.5, leading=16, textColor=colors.HexColor("#1a1a1a"))
h1 = ParagraphStyle("h1", parent=base, fontName="Helvetica-Bold", fontSize=20, leading=24, textColor=AZUL, spaceAfter=10)
h2 = ParagraphStyle("h2", parent=base, fontName="Helvetica-Bold", fontSize=14, leading=18, textColor=AZUL, spaceBefore=12, spaceAfter=6)
passo_t = ParagraphStyle("passo_t", parent=base, fontName="Helvetica-Bold", fontSize=13, leading=17, spaceAfter=3)
peq = ParagraphStyle("peq", parent=base, fontSize=10, leading=13.5, textColor=CINZA)
cod = ParagraphStyle("cod", parent=base, fontName="Courier", fontSize=10, leading=13)
capa_t = ParagraphStyle("capa_t", parent=h1, fontSize=30, leading=36, alignment=TA_CENTER)
capa_s = ParagraphStyle("capa_s", parent=base, fontSize=14, leading=20, alignment=TA_CENTER, textColor=CINZA)


def P(t, s=base):
    return Paragraph(t, s)


def lista(itens, s=base):
    return [Paragraph("&bull;&nbsp;&nbsp;" + i, ParagraphStyle("li", parent=s, leftIndent=14, firstLineIndent=-10, spaceAfter=2))
            for i in itens]


def caixa(titulo, linhas, cor):
    conteudo = [P(f"<b>{titulo}</b>", base)] + [P(l, base) for l in linhas]
    t = Table([[conteudo]], colWidths=[16.4 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), cor), ("BOX", (0, 0), (-1, -1), 0.6, LINHA),
                           ("LEFTPADDING", (0, 0), (-1, -1), 10), ("RIGHTPADDING", (0, 0), (-1, -1), 10),
                           ("TOPPADDING", (0, 0), (-1, -1), 7), ("BOTTOMPADDING", (0, 0), (-1, -1), 7)]))
    return t


cod_claro = ParagraphStyle("cod_claro", parent=cod, textColor=colors.HexColor("#E5E7EB"))
cod_resumo = ParagraphStyle("cod_resumo", parent=cod_claro, fontSize=8.6, leading=11.5, leftIndent=0)


def _linha_tela(l, quebra):
    if not quebra:
        return html.escape(l).replace(" ", "&nbsp;") or "&nbsp;"
    ident = len(l) - len(l.lstrip(" "))
    return "&nbsp;" * ident + html.escape(l.lstrip(" ")).replace("  ", " &nbsp;")


def tela(linhas, quebra=False):
    estilo = cod_resumo if quebra else cod_claro
    t = Table([[[P(_linha_tela(l, quebra) or "&nbsp;", estilo) for l in linhas]]], colWidths=[16.4 * cm])
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), colors.HexColor("#111827")),
                           ("LEFTPADDING", (0, 0), (-1, -1), 12), ("TOPPADDING", (0, 0), (-1, -1), 8),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    return t


def passo(num, titulo, corpo, extra=None):
    n = Table([[P(f"<font color='white'><b>{num}</b></font>", ParagraphStyle("n", parent=base, fontSize=16, alignment=TA_CENTER))]],
              colWidths=[1.1 * cm], rowHeights=[1.1 * cm])
    n.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, -1), AZUL), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                           ("ROUNDEDCORNERS", [8, 8, 8, 8])]))
    miolo = [P(titulo, passo_t)] + corpo
    t = Table([[n, miolo]], colWidths=[1.6 * cm, 14.8 * cm])
    t.setStyle(TableStyle([("VALIGN", (0, 0), (-1, -1), "TOP"), ("LEFTPADDING", (0, 0), (-1, -1), 0),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 8)]))
    ex = [] if extra is None else (extra if isinstance(extra, list) else [extra])
    return KeepTogether([t, Spacer(1, 2)] + ex + [Spacer(1, 10)])


def digitar(linhas):
    dados = [[P("<b>Quando a tela pedir...</b>", peq), P("<b>Você digita</b>", peq)]] + [[P(a, peq), P(b, peq)] for a, b in linhas]
    t = Table(dados, colWidths=[8.2 * cm, 8.2 * cm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F0FA")), ("GRID", (0, 0), (-1, -1), 0.5, LINHA),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 3),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]))
    return t


def rodape(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(CINZA)
    canvas.drawString(2 * cm, 1.2 * cm, "Manual - Manutenção do Blog comprenolink.net")
    canvas.drawRightString(A4[0] - 2 * cm, 1.2 * cm, f"Página {doc.page}")
    canvas.restoreState()


def montar():
    s = []
    # ------------------------------------------------------------------ capa
    s += [Spacer(1, 5 * cm), P("Manutenção do Blog", capa_t), Spacer(1, 6),
          P("Manual passo a passo para quem vai usar o programa", capa_s), Spacer(1, 4),
          P("comprenolink.net / melhores-produtos-mercado-livre-2026", capa_s), Spacer(1, 2.5 * cm),
          caixa("Com este programa você consegue, sem mexer no WordPress:",
                ["&bull; <b>Ver</b> a lista dos anúncios (produtos) do guia",
                 "&bull; <b>Alterar</b> link, preço, selo, texto e benefícios de um anúncio",
                 "&bull; <b>Apagar</b> um anúncio e <b>incluir</b> um novo",
                 "&bull; <b>Desfazer</b> qualquer mudança (backup automático)"], VERDE),
          PageBreak()]

    # ------------------------------------------------------------------ preparação
    s += [P("Antes de começar", h1),
          P("Você vai precisar de apenas 3 coisas:"), Spacer(1, 4)]
    s += lista(["A pasta <b>Pacote_Outro_PC</b> (contém: GerenciarBlog.exe, wp_credenciais.exemplo.json, TREINAR.bat, a pasta treino, LEIA-ME.txt e este manual).",
                "Internet no computador.",
                "Uma conta de <b>Administrador</b> no WordPress do site (comprenolink.net/wp-admin)."])
    s += [Spacer(1, 8),
          caixa("Não precisa instalar nada.",
                ["O programa funciona sozinho: não é preciso instalar Python nem outros programas."], VERDE),
          Spacer(1, 12), P("Parte 1 - Configuração (feita uma única vez)", h2)]

    s.append(passo(1, "Copie a pasta para o computador",
                   [P("Copie a pasta <b>Pacote_Outro_PC</b> inteira para um lugar fácil, por exemplo a Área de Trabalho. "
                      "Pode renomear a pasta se quiser (ex.: <b>Blog_Manutencao</b>).")]))
    s.append(passo(2, "Crie a \"senha de aplicativo\" no WordPress",
                   [P("É uma senha especial, só para este programa. Assim você <b>nunca</b> precisa informar a senha normal do site."),
                    Spacer(1, 3)] +
                   lista(["Abra no navegador: <b>comprenolink.net/wp-admin</b> e entre com o seu login.",
                          "No menu da esquerda clique em <b>Usuários</b> e depois em <b>Perfil</b>.",
                          "Role a página até <b>Senhas de aplicativo</b>.",
                          "Em <i>Novo nome da senha de aplicativo</i> digite: <b>Manutencao Blog</b> e clique em "
                          "<b>Adicionar nova senha de aplicativo</b>.",
                          "Aparece uma senha com várias letras separadas por espaço. <b>Copie agora</b>: ela só é mostrada uma vez."]) ))
    s.append(passo(3, "Preencha o arquivo de acesso",
                   lista(["Dentro da pasta, faça uma cópia do arquivo <b>wp_credenciais.exemplo.json</b> e mude o nome da cópia para "
                          "<b>wp_credenciais.json</b>.",
                          "Abra esse arquivo com o <b>Bloco de Notas</b> (botão direito &gt; Abrir com &gt; Bloco de Notas).",
                          "Em <b>usuario</b> deixe o login (ou e-mail) da sua conta do WordPress.",
                          "Em <b>senha_aplicativo</b> apague o texto de exemplo e cole a senha copiada no passo 2.",
                          "Salve (Ctrl + S) e feche. Mantenha as aspas e a vírgula como estão."]),
                   extra=tela(['{', '  "site": "https://comprenolink.net",', '  "pagina_id": 5,',
                               '  "usuario": "seu-login-ou-email",', '  "senha_aplicativo": "abcd efgh ijkl mnop qrst uvwx"', '}'])))
    s += [Spacer(1, 4),
          caixa("Cuidado com a senha de aplicativo",
                ["Não envie por WhatsApp, e-mail ou print. Se ela vazar, entre no mesmo lugar do passo 2 e clique em "
                 "<b>Revogar</b>: ela deixa de funcionar na hora (e você cria outra)."], AMARELO),
          PageBreak()]

    # ------------------------------------------------------------------ uso
    s += [P("Parte 2 - Usando o programa", h1)]
    s.append(passo(4, "Abra o programa e teste a conexão",
                   lista(["Dê <b>duplo clique</b> em <b>GerenciarBlog.exe</b>. Abre uma janela preta com o menu abaixo.",
                          "Digite <b>1</b> e aperte ENTER (Testar conexão).",
                          "Se aparecer <i>\"Conectado como: ... pode editar páginas: SIM\"</i>, está tudo certo. "
                          "Se aparecer ERRO, veja a página \"Se der erro\" deste manual."]),
                   extra=tela(['=== MANUTENÇÃO DO BLOG comprenolink.net ===', ' 1) Testar conexão          5) Adicionar anúncio',
                               ' 2) Listar anúncios         6) Buscar e substituir texto', ' 3) Editar anúncio          7) Fazer backup agora',
                               ' 4) Remover anúncio         8) Restaurar um backup', ' 0) Sair', 'Escolha: _'])))
    s += [Spacer(1, 2),
          caixa("Regra de ouro",
                ["Toda mudança mostra primeiro <b>o que vai mudar</b> e pergunta <b>\"Aplicar no site AGORA? (s/N)\"</b>. "
                 "Leia o resumo. Digite <b>s</b> para publicar ou apenas ENTER para cancelar. "
                 "Antes de publicar, o programa guarda automaticamente uma cópia do site na pasta <b>backups</b>."], VERDE),
          Spacer(1, 10)]

    s.append(passo(5, "Ver os anúncios (opção 2)",
                   [P("Mostra cada anúncio com seu <b>número</b>, nome, selo, preço e link. O número é o que você usa nas outras opções.")]))
    s.append(passo(6, "Alterar um anúncio (opção 3)",
                   lista(["Digite <b>3</b>, depois o <b>número</b> do anúncio.",
                          "O programa pergunta cada campo. <b>Deixe em branco (ENTER) o que não quer mudar.</b>",
                          "Campos: <b>nome</b> (título do item), <b>link</b> (link meli.la), <b>selo</b> (ex.: Mais Vendido), "
                          "<b>descrição</b>, <b>benefícios</b> e <b>ideal para</b> (separe os itens com o sinal | ), "
                          "<b>título do anúncio</b>, <b>preço</b> e <b>imagem</b> (as 3 últimas são do cartão do produto).",
                          "Confira o resumo e responda <b>s</b>."]),
                   extra=tela(['Novo nome (título do item): ', 'Novo link meli.la: https://meli.la/ABC123', 'Novo selo: Oferta do Mês',
                               'Novos benefícios (a|b|c): Bateria forte|Som nítido|Leve', 'Novo preço: R$ 289,90'])))
    s.append(passo(7, "Apagar um anúncio (opção 4)",
                   lista(["Digite <b>4</b> e o <b>número</b> do anúncio. Confirme com <b>s</b>.",
                          "Os anúncios seguintes são <b>renumerados sozinhos</b> (links internos, tabela \"Escolha rápida\" e "
                          "contagem no título também)."])))
    s.append(passo(8, "Incluir um novo anúncio (opção 5)",
                   lista(["Digite <b>5</b> e responda: <b>nome</b> e <b>link</b> são obrigatórios; o resto é opcional, mas "
                          "quanto mais completo, melhor o anúncio.",
                          "<b>Posição</b>: o número onde o anúncio deve entrar (vazio = no final).",
                          "<b>Categoria para a tabela</b>: se preencher, o produto também entra na tabela \"Escolha rápida\" no topo.",
                          "Dica: para a imagem, no Mercado Livre clique com o botão direito na foto do produto &gt; "
                          "<i>Copiar endereço da imagem</i> e cole."])))
    s.append(passo(9, "Trocar um texto em toda a página (opção 6)",
                   [P("Útil para corrigir um erro de digitação ou trocar um link que aparece em vários lugares. Informe o texto "
                      "antigo e o novo; o programa diz quantas vezes ele aparece antes de você confirmar.")]))
    s.append(passo(10, "Desfazer (opções 7 e 8)",
                   lista(["<b>7</b> faz um backup do site agora, quando você quiser.",
                          "<b>8</b> mostra a lista de backups; escolha o número e confirme para <b>voltar o site àquela versão</b>."])))

    # ------------------------------------------------------------------ cenário
    s += [PageBreak(), P("Parte 3 - Exemplo completo (cenário)", h1),
          P("<b>Situação:</b> é segunda-feira da Black Friday e o guia precisa de 3 mudanças. Os links e preços abaixo são "
            "<b>inventados para o exemplo</b>. As telas foram geradas pelo próprio programa em <b>modo treino</b>, sem tocar no site."),
          Spacer(1, 6),
          caixa("As 3 tarefas do dia",
                ["1. O <b>Echo Dot</b> (anúncio 4) baixou de preço e você gerou um link novo: trocar o link e o preço.",
                 "2. A <b>Soundbar</b> (anúncio 7) saiu de estoque: apagar do guia.",
                 "3. Surgiu uma oferta: incluir o <b>JBL Tune 520BT</b> em 2º lugar do guia."], AMARELO),
          Spacer(1, 10)]
    s.append(passo(1, "Trocar link e preço do Echo Dot (opção 3)",
                   [P("Nos campos que você não quer mudar, apenas aperte ENTER."), Spacer(1, 4)],
                   extra=[digitar([("Escolha:", "<b>3</b>"), ("Número do anúncio a editar:", "<b>4</b>"),
                                   ("Novo nome (título do item):", "(só ENTER)"),
                                   ("Novo link meli.la:", "<b>https://meli.la/EXEMPLO4</b>"),
                                   ("Novo selo, nova descrição, benefícios, ideal para, título do anúncio:", "(só ENTER em cada um)"),
                                   ("Novo preço (ex.: R$ 299,90):", "<b>R$ 279,00</b>"), ("Nova URL da imagem:", "(só ENTER)"),
                                   ("Aplicar no site AGORA? (s/N):", "<b>s</b>")]), Spacer(1, 4),
                          tela(["=== RESUMO DA MUDANÇA (leia antes de confirmar) ===",
                                "  Item 4 (Amazon Echo Dot 5ª Geração) - link: https://meli.la/1AXvaMV  ->  https://meli.la/EXEMPLO4",
                                "  Item 4 (Amazon Echo Dot 5ª Geração) - preço: R$ 449,00  ->  R$ 279,00",
                                "(detalhes técnicos, se precisar: ...\\ultimo_diff.txt)"], quebra=True)]))
    s.append(passo(2, "Apagar a Soundbar (opção 4)",
                   [P("O programa mostra a lista; você só informa o número."), Spacer(1, 4)],
                   extra=[digitar([("Escolha:", "<b>4</b>"), ("Número do anúncio a REMOVER:", "<b>7</b>"),
                                   ("Aplicar no site AGORA? (s/N):", "<b>s</b>")]), Spacer(1, 4),
                          tela(["Removendo o item 7: Soundbar  (https://meli.la/1Qeyqb3)",
                                "Os itens seguintes foram renumerados; agora são 20 itens.", "",
                                "=== RESUMO DA MUDANÇA (leia antes de confirmar) ===",
                                "  REMOVIDO:   item 7 - Soundbar",
                                "  14 anúncio(s) mantido(s) foram renumerados automaticamente.",
                                "  Texto 'reunimos N modelos': 21  ->  20",
                                "  Data 'Atualizado em': 21/10/2026  ->  22/10/2026",
                                "Título: 'Os 21 Melhores Produtos do Mercado Livre em 2026' -> 'Os 20 Melhores Produtos ...'"], quebra=True)]))
    s.append(passo(3, "Incluir o JBL Tune 520BT em 2º lugar (opção 5)",
                   [P("Só <b>nome</b> e <b>link</b> são obrigatórios. Listas (benefícios e ideal para) usam o sinal <b>|</b> entre os itens."),
                    Spacer(1, 4)],
                   extra=[digitar([("Escolha:", "<b>5</b>"), ("Nome curto do produto:", "<b>JBL Tune 520BT</b>"),
                                   ("Link meli.la do produto:", "<b>https://meli.la/EXEMPLO520</b>"),
                                   ("Selo:", "<b>Oferta Black Friday</b>"),
                                   ("Descrição curta:", "<b>Headphone Bluetooth com som JBL Pure Bass, leve e dobrável.</b>"),
                                   ("Título completo do anúncio (cartão):", "<b>Fone de Ouvido JBL Tune 520BT Bluetooth On-Ear</b>"),
                                   ("Preço:", "<b>R$ 199,90</b>"), ("URL da imagem do produto:", "(só ENTER, ou cole o endereço da imagem)"),
                                   ("Benefícios:", "<b>Som JBL Pure Bass|Bateria de longa duração|Leve e dobrável</b>"),
                                   ("Ideal para:", "<b>Música|Viagem|Uso diário</b>"), ("Posição:", "<b>2</b>"),
                                   ("Categoria p/ tabela 'Escolha rápida':", "<b>Fone JBL em oferta</b>"),
                                   ("Aplicar no site AGORA? (s/N):", "<b>s</b>")]), Spacer(1, 4),
                          tela(["Novo item entrará na posição 2; agora são 21 itens.", "",
                                "=== RESUMO DA MUDANÇA (leia antes de confirmar) ===",
                                "  ADICIONADO: item 2 - JBL Tune 520BT  [Oferta Black Friday]  R$ 199,90",
                                "  19 anúncio(s) mantido(s) foram renumerados automaticamente.",
                                "  Tabela 'Escolha rápida': 7 -> 8 linha(s)",
                                "  Texto 'reunimos N modelos': 20  ->  21"], quebra=True)]))
    s.append(passo(4, "Conferir o resultado (opção 2)",
                   [P("Depois de publicar, a lista mostra tudo já atualizado e renumerado:"), Spacer(1, 4)],
                   extra=[tela([" 1. Fone JBL Bluetooth On-Ear  [Mais Vendido]  R$ 319,00",
                                " 2. JBL Tune 520BT  [Oferta Black Friday]  R$ 199,90          <- NOVO",
                                " 3. Fone In-Ear QCY  [Melhor Custo-Benefício]  R$ 319,00",
                                " 4. Caixa de Som Bluetooth  [Preferida para Uso Externo]",
                                " 5. Amazon Echo Dot 5ª Geração  [Melhor Assistente Virtual]  R$ 279,00   <- NOVO PREÇO",
                                " ...   (a Soundbar saiu da lista e os números seguintes foram ajustados)"], quebra=True)]))
    s += [caixa("Quer repetir este exemplo sem risco?",
                ["Dê duplo clique em <b>TREINAR.bat</b> (na pasta do programa). Ele abre o menu em <b>modo treino</b>: aparece "
                 "<b>[MODO OFFLINE]</b> no título, usa uma cópia do guia (pasta <b>treino</b>) e <b>nada é enviado ao site</b>. "
                 "O resultado fica no arquivo saida_offline.html. No uso real, o mesmo roteiro publica no site e guarda o backup antes."],
                VERDE), Spacer(1, 6),
          caixa("Depois de publicar de verdade",
                ["Aguarde alguns minutos e atualize a página do blog com <b>Ctrl + F5</b> (o cache do site demora um pouco). "
                 "Se algo ficou errado, use a opção <b>8</b> para voltar ao backup."], AMARELO)]
    s.append(PageBreak())

    # ------------------------------------------------------------------ problemas
    s += [P("Se der erro", h1)]
    linhas = [[P("<b>Mensagem</b>"), P("<b>O que fazer</b>")],
              [P("Faltam as credenciais"), P("O arquivo <b>wp_credenciais.json</b> não existe ou está vazio. Refaça o passo 3 "
                                              "(ele precisa ficar na mesma pasta do .exe).")],
              [P("401 - usuário/senha recusados"), P("Confira usuário e senha de aplicativo (sem aspas extras). Se estiverem certos, "
                                                      "a hospedagem pode estar bloqueando o acesso: veja o item \"401\" no <b>LEIA-ME.txt</b> "
                                                      "(3 linhas no arquivo .htaccess).")],
              [P("403 - sem permissão"), P("A conta precisa ser <b>Administrador</b> ou <b>Editor</b>. Um plugin de segurança também pode estar bloqueando.")],
              [P("404 - página não encontrada"), P("O número em <b>pagina_id</b> (arquivo wp_credenciais.json) não é o da página do guia. O correto hoje é <b>5</b>.")],
              [P("Sem conexão com o site"), P("Verifique a internet e se comprenolink.net abre no navegador.")],
              [P("Windows/antivírus bloqueou o .exe"), P("Programas novos sem assinatura digital às vezes são bloqueados por engano. "
                                                          "Se a origem é confiável, escolha \"Executar assim mesmo\" ou libere a pasta no antivírus.")],
              [P("Verificação falhou, nada será publicado"), P("O programa percebeu que a mudança deixaria a página inconsistente e "
                                                                "se recusou a publicar. Nada foi alterado no site. Tente de novo ou fale com quem mantém o programa.")]]
    t = Table(linhas, colWidths=[5.2 * cm, 11.2 * cm], repeatRows=1)
    t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8F0FA")), ("GRID", (0, 0), (-1, -1), 0.5, LINHA),
                           ("VALIGN", (0, 0), (-1, -1), "TOP"), ("TOPPADDING", (0, 0), (-1, -1), 6),
                           ("BOTTOMPADDING", (0, 0), (-1, -1), 6)]))
    s += [t, Spacer(1, 14), P("Cuidados importantes", h2)]
    s += lista(["<b>Preço não se atualiza sozinho.</b> Quando o preço mudar no Mercado Livre, use a opção 3 para atualizar.",
                "<b>Pode demorar uns minutos</b> para o site mostrar a mudança (existe cache). Atualize com Ctrl + F5.",
                "O programa <b>só mexe na página do guia</b>. Home, Sobre, Contato, menu e plugins não são alterados.",
                "O texto de SEO (meta descrição do All in One SEO) <b>não</b> é alterado: se ele citar \"21 produtos\", ajuste no WordPress.",
                "Não compartilhe o arquivo <b>wp_credenciais.json</b> nem a pasta <b>backups</b> com outras pessoas."])
    s += [Spacer(1, 10),
          caixa("Quer só treinar, sem risco?",
                ["Use o <b>TREINAR.bat</b> (veja a Parte 3). Nesse modo nada é enviado ao site."], VERDE)]
    return s


def main():
    doc = SimpleDocTemplate(SAIDA, pagesize=A4, leftMargin=2.3 * cm, rightMargin=2.3 * cm, topMargin=2 * cm, bottomMargin=2 * cm,
                            title="Manual - Manutenção do Blog comprenolink.net", author="Blog comprenolink.net")
    doc.build(montar(), onFirstPage=lambda c, d: None, onLaterPages=rodape)
    # O pacote do outro PC leva só os painéis do navegador; este manual (menu/treino) fica só aqui
    print("PDF gerado:", SAIDA)


if __name__ == "__main__":
    main()
