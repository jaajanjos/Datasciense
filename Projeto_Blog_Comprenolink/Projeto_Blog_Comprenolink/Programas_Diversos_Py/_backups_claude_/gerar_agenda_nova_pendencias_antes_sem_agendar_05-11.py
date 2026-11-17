# -*- coding: utf-8 -*-
"""Agenda ÚNICA do projeto, baseada no controle nova_pendencias.pdf (plano de execução por dia). Criada em 03/11/2026.
Rodar:  python -X utf8 gerar_agenda_nova_pendencias.py
Saída:  D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/agenda_nova_pendencias.ics
Regra do dono: nenhuma outra agenda; cada evento só aponta para a atividade do nova_pendencias.pdf (sem repetir o passo a passo).
Horários locais (sem fuso fixo), como nas agendas anteriores. Caminhos com barra normal.
"""
import glob
import os
import re
from datetime import date, datetime, time, timedelta

SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/agenda_nova_pendencias.ics"
PACOTES = "D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento/Celular_Whatsapp/07_PACOTE_DO_DIA"
PDF = "nova_pendencias.pdf"
L = []
n_ev = 0


def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def dobra(linha):
    b = linha.encode("utf-8")
    partes = []
    while len(b) > 74:
        corte = 74
        while (b[corte] & 0xC0) == 0x80:
            corte -= 1
        partes.append(b[:corte])
        b = b[corte:]
    partes.append(b)
    return "\r\n ".join(p.decode("utf-8") for p in partes)


def ev(chave, dia, ini, dur_min, titulo, desc, rrule=None, exdate=None, alarme=10):
    """dia: date; ini: time; dur_min: minutos."""
    global n_ev
    n_ev += 1
    a = datetime.combine(dia, ini)
    b = a + timedelta(minutes=dur_min)
    f = "%Y%m%dT%H%M%S"
    L.extend(["BEGIN:VEVENT", f"UID:{chave}@agenda-nova-pendencias", "DTSTAMP:20261104T223000Z", "SEQUENCE:2", f"DTSTART:{a.strftime(f)}",
              f"DTEND:{b.strftime(f)}", f"SUMMARY:{esc(titulo)}", f"DESCRIPTION:{esc(desc)}"])
    if rrule:
        L.append("RRULE:" + rrule)
    for x in (exdate or []):
        L.append("EXDATE:" + x)
    L.extend(["BEGIN:VALARM", f"TRIGGER:-PT{alarme}M", "ACTION:DISPLAY", f"DESCRIPTION:{esc(titulo)}", "END:VALARM", "END:VEVENT"])


def d(dd, mm):
    return date(2026, dd and mm, 1).replace(day=dd, month=mm)


def ref(n):
    return f"Veja a atividade {n} no {PDF}." if n else f"Veja o {PDF}."


# ------------------------------------------------------------------ dias do plano (iguais ao PDF)
ev("hoje-0311", d(3, 11), time(16, 0), 10, "Hoje: dizer sim ao botão Siga no Instagram e ao caminho do OneDrive (Word e Guia do sócio já feitos)",
   f"{ref(0)} Plano por dia, linha de 03/11. 2 minutos.")
ev("email-trial-2027", date(2027, 10, 3), time(10, 0), 10, "E-mail grátis Hostinger (alertas@): desligar a renovação automática ou decidir manter",
   f"{ref(4)} O teste grátis de 12 meses começou em 03/11/2026; depois a Hostinger cobra o plano Starter Business Email. Desligue a renovação automática no painel se não quiser manter.", alarme=60)
ev("ga4-0611", d(6, 11), time(10, 0), 15, "[6] Claude confere Google Analytics, Search Console e Bing (dados já processados)",
   f"{ref(6)} Escreva ao Claude: conferir analytics. 15 minutos.")
ev("maquinas-0511", d(5, 11), time(10, 0), 20, "Republicar o blog das máquinas (Google Sites)",
   f"{ref(0)} Anexo B (blog das máquinas). 20 minutos. Os 12 pedidos em revisão já foram conferidos.")
ev("destaques-0711", d(7, 11), time(10, 0), 30, "Destaques do Instagram (celular)", f"{ref(0)} Anexo B. 30 minutos, no celular.")
ev("item77-0911", d(9, 11), time(11, 45), 10, "[8] Item 77 (Colágeno Verisol): conferir se continua pausado no ML",
   f"{ref(8)} Se continuar pausado, você traz o link novo e o Claude troca. 10 minutos.")
ev("decisoes-0911", d(9, 11), time(11, 15), 15, "Decisões de 09/11: QCY Shopee, nota antiga do painel das máquinas, divulgação de longo prazo e Telegram",
   f"{ref(0)} Anexo B. 15 minutos com o Claude.")
ev("catalogo-1011", d(10, 11), time(14, 0), 15, "Catálogo do WhatsApp: cadastrar Moda Infantil & Juvenil", f"{ref(0)} Anexo A. 15 minutos.")
ev("g1-0511", d(5, 11), time(10, 20), 10, "[14] Colar o convite do Canal nas respostas do Direct e do ManyChat (Claude deixa o texto pronto)",
   f"{ref(14)} Ação G1 do Anexo I. 10 minutos, logo depois de republicar o blog das máquinas e antes de aprovar os contatos das 10:30. O texto é o do Comente CANAL; sem automação de envio.")
ev("g7-0511", d(5, 11), time(11, 0), 30, "Claude: gancho de 2 segundos nos Reels, no gerador de vídeos (vale a partir do dia 04/12)",
   f"{ref(0)} Anexo I, ação G7. Só do Claude; você não precisa fazer nada.")
ev("g10-0611", d(6, 11), time(19, 10), 5, "Teste de enquete ou caixa de perguntas no Story (junto da rotina das 19:10)",
   f"{ref(0)} Anexo I, ação G10. Claude ou você. 2 a 5 minutos, dentro da rotina do dia.")
ev("g5-0711", d(7, 11), time(10, 40), 10, "Conferir a saudação, a ausência e as etiquetas do WhatsApp Business (celular)",
   f"{ref(0)} Anexo I, ação G5. 10 minutos, logo depois dos Destaques das 10:00.")
ev("manychat-1111", d(11, 11), time(18, 30), 5, "Confirmar os testes do ManyChat (BLACK e resposta no Direct)", f"{ref(0)} Anexo B. 5 minutos.")
ev("sync-1211", d(12, 11), time(10, 0), 10, "Ver se os dois computadores sincronizam a pasta de scripts", f"{ref(0)} Anexo B. 10 minutos.")
ev("bio-natal-0112", d(1, 12), time(10, 0), 5, "[13] Instagram: trocar a bio e o link 1 para o Natal (celular)", f"{ref(13)} 5 minutos.")
ev("bio-volta-2612", d(26, 12), time(10, 0), 5, "Instagram: o link 1 da bio volta para comprenolink.net (celular)", f"{ref(0)} Anexo B. 5 minutos.")

# ------------------------------------------------------------------ rotinas semanais
ev("seg-vendas", d(9, 11), time(10, 15), 15, "[6] Vendas do ML Afiliados por prints",
   f"{ref(0)} Anexo A. Prints da tabela de Vendas ao Claude e depois ATUALIZAR_PAINEL.bat. 15 minutos.",
   rrule="FREQ=WEEKLY;BYDAY=MO;UNTIL=20261221T235959", alarme=30)
ev("seg-numeros", d(9, 11), time(10, 45), 30, "[6] Reunião com os números e uma decisão",
   f"{ref(6)} Planilha_Semanal_Turbinar.xlsx. 30 minutos.", rrule="FREQ=WEEKLY;BYDAY=MO;UNTIL=20261221T235959")
ev("sex-seo", d(6, 11), time(14, 0), 60, "[6] Rotina de SEO (20 min se pedir rotina de sexta ao Claude)",
   f"{ref(6)} Em 27/11 não tem (dia da Black Friday): faça na segunda 30/11.",
   rrule="FREQ=WEEKLY;BYDAY=FR;UNTIL=20261218T235959", exdate=["20261127T140000"])
ev("ter-pagina", d(10, 11), time(10, 0), 30, "[11] Revisar a página nova da semana",
   f"{ref(11)} Na segunda anterior você pede a página; na terça você revisa. 30 minutos.", rrule="FREQ=WEEKLY;BYDAY=TU;UNTIL=20261215T235959")
for dia, nome in ((d(13, 11), "13/11"), (d(26, 11), "26/11"), (d(11, 12), "11/12")):
    ev("guia-" + nome.replace("/", ""), dia, time(14, 30), 30, f"[8] Guia: conferir anúncios e atualizar a data ({nome})",
       f"{ref(8)} Rodar o painel, conferir anúncios e links e só então trocar Atualizado em.")
ev("claude-uso-seg", d(9, 11), time(10, 0), 15, "Claude: conferir uso do plano e a tarefa das 19:12",
   f"{ref(0)} Página C. Escreva conferir uso ao Claude. A contagem semanal renova na segunda às 02:00.",
   rrule="FREQ=WEEKLY;BYDAY=MO;UNTIL=20261221T235959")
ev("claude-uso-sex", d(6, 11), time(12, 0), 15, "Claude: regra dos 70% do uso semanal",
   f"{ref(0)} Página C. Se passou de 70%, o Claude pausa o que não é essencial.", rrule="FREQ=WEEKLY;BYDAY=FR;UNTIL=20261218T235959")

ev("venc-dominio-2027", date(2027, 8, 23), time(10, 0), 10, "Domínio comprenolink.net vence em 22/09/2027: conferir a renovação automática",
   f"{ref(3)} Vencimento confirmado no registro do domínio: 22/09/2027. Aviso 30 dias antes.", alarme=60)
ev("venc-hospedagem-2027", date(2027, 8, 23), time(10, 15), 10, "Hospedagem Hostinger vence em 22/09/2027: conferir a renovação automática",
   f"{ref(3)} Vencimento informado pelo dono: 22/09/2027, igual ao do domínio. Aviso 30 dias antes.", alarme=60)

# ------------------------------------------------------------------ Turbinar pago (decidido em 05/11)
ev("turbinar-claude-termos-1311", d(13, 11), time(10, 0), 20, "[Turbinar] Claude confere os termos do ML Afiliados e deixa o anúncio de teste pronto para aprovar",
   f"{ref(0)} A conta Meta já foi criada em 05/11 (cartão Visa e limite de R$ 50). Destino do anúncio: página do blog com UTM, nunca meli.la direto.")
ev("turbinar-limite-2011", d(20, 11), time(10, 0), 10, "[Turbinar] Se o teste ficou no verde: subir o limite de gastos da conta para R$ 155",
   f"{ref(0)} Faturamento e pagamentos > Limite de gastos da conta > R$ 155 (R$ 50 do teste + R$ 105 da Black Friday). Se o teste não ficou no verde, não suba o limite.")
ev("turbinar-limite-0412", d(4, 12), time(10, 0), 10, "[Turbinar] Se a Black Friday se pagou: subir o limite de gastos da conta para R$ 100 (dezembro)",
   f"{ref(0)} O limite reinicia no dia 1º de cada mês e volta a R$ 50. Para o Natal (05 a 14/12) suba para R$ 100. Se a Black Friday não se pagou, não suba.")
ev("turbinar-teste-1611", d(16, 11), time(11, 30), 20, "[Turbinar] Iniciar o teste de R$ 50 (16 a 18/11, orçamento total)",
   f"{ref(0)} Post com mais salvamentos e comentários. Orçamento total de R$ 50 até 18/11 (cerca de R$ 16,67 por dia). Pode parar a qualquer momento.")
ev("turbinar-aval1-1911", d(19, 11), time(10, 30), 30, "[Turbinar] Avaliação 1 do teste: semáforo (verde segue, amarelo ajusta, vermelho para)",
   f"{ref(0)} O Claude lê custo por clique e visitas pagas. Verde: segue para a Black Friday (R$ 105, 21 a 27/11).")
ev("turbinar-bf-2111", d(21, 11), time(9, 0), 15, "[Turbinar] Black Friday paga: R$ 105 em 21 a 27/11 (só se o teste ficou no verde)",
   f"{ref(0)} Se o teste não ficou no verde, não anuncia.")
ev("turbinar-aval2-3011", d(30, 11), time(10, 30), 30, "[Turbinar] Avaliação 2: a Black Friday se pagou? (decide o Natal de R$ 100)",
   f"{ref(0)} Vendas da Black Friday maiores ou iguais ao gasto: faz o Natal (05 a 14/12).")
ev("turbinar-natal-0512", d(5, 12), time(9, 0), 15, "[Turbinar] Natal pago: R$ 100 em 05 a 14/12 (só se a Black Friday se pagou)",
   f"{ref(0)} Se a Black Friday não se pagou, não anuncia.")
ev("turbinar-final-2112", d(21, 12), time(11, 30), 30, "[Turbinar] Relatório final do Turbinar (Claude faz)",
   f"{ref(0)} Gasto, visitas, cliques no Mercado Livre e vendas. Total máximo R$ 255.")

# ------------------------------------------------------------------ Black Friday
ev("bf-lembrete-2611", d(26, 11), time(20, 0), 15, "[7] Black Friday: lembrete forte (amanhã é o dia D)", f"{ref(7)} Bloco das 20:00 na pasta 2026-11-26_qui.")
for h, nome in ((8, "manhã"), (12, "almoço"), (19, "noite")):
    ev(f"bf-dia-d-{h}", d(27, 11), time(h, 0), 15, f"[7] Black Friday, dia D: disparo da {nome}", f"{ref(7)} Pasta 2026-11-27_sex. Se não puder, o sócio direciona o Claude.")
ev("cyber-3011", d(30, 11), time(8, 0), 15, "[7] Cyber Monday: último dia da campanha", f"{ref(7)} Pasta 2026-11-30_seg.")
ev("natal-troca-0112", d(1, 12), time(9, 0), 10, "Conferir que o menu e a home trocaram sozinhos para o Natal", f"{ref(0)} Página C (Claude confere também).")

# ------------------------------------------------------------------ rotina de cada dia (dos pacotes do dia)
pastas = sorted(glob.glob(PACOTES + "/2026-*"))
agendar = []
for p in pastas:
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})_(\w+)", os.path.basename(p))
    if not m:
        continue
    dia = date(int(m[1]), int(m[2]), int(m[3]))
    if dia < date(2026, 11, 3):
        continue
    nome = os.path.basename(p)
    if os.path.exists(os.path.join(p, "feed.png")):
        prod = ""
        arq = os.path.join(p, "1_TEXTOS_DO_DIA.txt")
        if os.path.exists(arq):
            tx = open(arq, encoding="utf-8-sig").read()
            k = tx.find("Post no feed")
            mm = re.search(r"[🔥🎄]\s*([^\n]+)", tx[k:]) if k >= 0 else None
            prod = re.sub(r"^(Black Friday|Natal):\s*", "", mm.group(1).strip()) if mm else ""
        ev("rotina-" + dia.strftime("%Y%m%d"), dia, time(19, 10), 10, "[7] Rotina do dia: Story 19:10, Status 19:15, Canal 19:20" + (f" – {prod[:40]}" if prod else ""),
           f"{ref(7)} Pasta {nome}. Post 19:00 e Reels 19:05 saem sozinhos. Se não puder, o sócio direciona o Claude (Guia do sócio).")
        if dia >= date(2026, 12, 2):
            abre = dia - timedelta(days=29)
            if abre >= date(2026, 11, 3):
                agendar.append((abre, dia))
for abre, dia in agendar:
    ev("agendar-" + dia.strftime("%Y%m%d"), abre, time(20, 0), 15, f"Chamar o Claude: agendar {dia:%d/%m} (post 19:00 e Reels 19:05)",
       f"{ref(7)} A janela de 29 dias do Instagram abre por volta de 20:00. Escreva: agendar {dia:%d/%m}.")

cab = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Claude//Agenda nova pendencias//PT", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
       "X-WR-CALNAME:Pendências comprenolink (agenda única)"]
with open(SAIDA, "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(dobra(x) for x in cab + L + ["END:VCALENDAR"]) + "\r\n")
print("eventos (séries contam 1):", n_ev, "->", SAIDA)
