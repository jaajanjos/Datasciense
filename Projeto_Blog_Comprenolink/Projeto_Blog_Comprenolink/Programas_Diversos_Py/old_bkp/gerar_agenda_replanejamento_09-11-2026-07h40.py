# -*- coding: utf-8 -*-
"""Agenda do replanejamento de 02/11/2026: margem de segurança do limite do Claude e plano B manual.
Gera D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Agenda_Replanejamento_02-11-2026.ics (horários locais, sem fuso fixo).
Uso: python -X utf8 gerar_agenda_replanejamento.py
"""
import datetime as dt

SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/Agenda_Replanejamento_02-11-2026.ics"


def esc(s):
    return s.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def dobra(linha):
    """RFC 5545: linhas com no máximo 75 bytes; continuação começa com um espaço."""
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


def ev(uid, dia, hora, titulo, desc, dur=30, rrule=None, alarme=15):
    ini = dt.datetime.combine(dia, hora)
    fim = ini + dt.timedelta(minutes=dur)
    f = "%Y%m%dT%H%M%S"
    L = ["BEGIN:VEVENT", f"UID:{uid}@replanejamento-claude", "DTSTAMP:20261102T235900Z",
         f"DTSTART:{ini.strftime(f)}", f"DTEND:{fim.strftime(f)}", f"SUMMARY:{esc(titulo)}",
         f"DESCRIPTION:{esc(desc)}"]
    if rrule:
        L.append("RRULE:" + rrule)
    L += ["BEGIN:VALARM", f"TRIGGER:-PT{alarme}M", "ACTION:DISPLAY", f"DESCRIPTION:{esc(titulo)}", "END:VALARM", "END:VEVENT"]
    return L


D = dt.date
T = dt.time
E = []

# 1) Teto do uso extra e margem de segurança
E += ev("teto-uso-extra", D(2026, 11, 3), T(9, 0), "Claude: deixar o uso extra com teto mínimo (sem custo extra)",
        "Meta do dono: o replanejamento NÃO gera custo extra. Nas configurações da conta, deixar o teto do uso extra o menor possível (ou desligado) "
        "para nada ser cobrado além do plano. Se o limite semanal acabar, vale o plano B manual (pacotes prontos). O Claude não paga nem muda essa configuração por você.", 30)
E += ev("reuniao-turbinar", D(2026, 11, 3), T(10, 0), "Reunião com o sócio: Plano Turbinar e os anúncios",
        "Levar o Plano Turbinar (0- Pendencias/5_Plano_turbinar_anuncio_instagram) e o resultado da leitura dos termos do ML Afiliados. "
        "Remarcada de quinta 05/11 para terça 03/11.", 60, alarme=30)
E += ev("teto-black-friday", D(2026, 11, 23), T(18, 0), "Claude: confirmar teto do uso extra para a semana da Black Friday (24 a 30/11)",
        "Semana mais pesada: dois agendamentos por dia mais a tarefa diária. Sem custo extra: se o semanal estiver acima de 50% hoje, adiar o que não é essencial "
        "e preparar o plano B manual. Não aumentar o teto do uso extra.", 30)

# 2) Conferência de uso: toda segunda 10:00 (renova às 02:00) e toda sexta 12:00 (regra dos 70%)
E += ev("uso-segunda", D(2026, 11, 9), T(10, 0), "Claude: conferir uso (semanal renovou às 02:00)",
        "Pedir ao Claude: \"conferir uso\". Anotar % semanal e % das 5 horas. A tarefa diária do WhatsApp e os agendamentos dependem do limite.", 15,
        rrule="FREQ=WEEKLY;BYDAY=MO;UNTIL=20261222T000000")
E += ev("uso-sexta", D(2026, 11, 6), T(12, 0), "Claude: regra dos 70% - semanal acima de 70%?",
        "Para NÃO gerar custo extra: se o limite semanal passou de 70% antes de sexta, o Claude pausa o que não é essencial (ajustes no blog, relatórios extras) e mantém só "
        "a tarefa diária e os agendamentos. Se passar de 85%, só a tarefa diária; o resto vai para o plano B manual até a renovação (segunda 02:00).", 15,
        rrule="FREQ=WEEKLY;BYDAY=FR;UNTIL=20261222T000000")

# 3) Medir o custo real da tarefa diária
E += ev("uso-antes", D(2026, 11, 4), T(19, 0), "Claude: anotar % de uso ANTES da tarefa diária (19:14)",
        "Pedir \"conferir uso\" e anotar semanal e 5 horas. Depois da execução (19:30) anotar de novo; a diferença é o custo real de um dia.", 10)
E += ev("uso-depois", D(2026, 11, 4), T(19, 30), "Claude: anotar % de uso DEPOIS da tarefa diária e conferir Status e Canal",
        "Conferir no WhatsApp Web se o Status e o Canal de 04/11 saíram e pedir \"conferir uso\". Registrar o custo de um dia e ajustar a estimativa.", 15)

# 4) Agendar dezembro: a janela de 29 dias abre ~20:00 em cada data
dezembro = [("02/12", D(2026, 11, 3)), ("04/12", D(2026, 11, 5)), ("07/12", D(2026, 11, 8)), ("09/12", D(2026, 11, 10)),
            ("11/12", D(2026, 11, 12)), ("14/12", D(2026, 11, 15)), ("16/12", D(2026, 11, 17)), ("18/12", D(2026, 11, 19)),
            ("21/12", D(2026, 11, 22)), ("23/12", D(2026, 11, 24))]
for post, dia in dezembro:
    E += ev("agendar-" + post.replace("/", ""), dia, T(20, 0), f"Chamar o Claude: agendar {post} (post 19:00, Reels 19:05 e Story 19:10)",
            "A janela do Instagram abre por volta das 20:00 desta data. Pedir: \"agendar " + post + "\". "
            "Se o Claude estiver sem limite (sem custo extra), agendar à mão com o pacote do dia (4- Celular_Whatsapp/07_PACOTE_DO_DIA).", 45)

# 5) Plano B manual: semana da Black Friday e dias de Status e Canal
E += ev("plano-b-bf", D(2026, 11, 24), T(19, 40), "Plano B: conferir se o Status e o Canal das 19:14 saíram",
        "Se o Claude parou (limite do plano acabou, sem uso extra, ou app fechado): publicar à mão. Abrir a pasta do dia em 4- Celular_Whatsapp/07_PACOTE_DO_DIA, "
        "abrir 1_TEXTOS_DO_DIA.txt, copiar o texto do Status (19:15) e do Canal (19:20) com a imagem status.png e feed.png. "
        "O Status do WhatsApp não aceita quebra de linha: cole numa linha só com o link no fim.", 20, rrule="FREQ=DAILY;COUNT=7")
E += ev("plano-b-geral", D(2026, 11, 4), T(19, 40), "Plano B: conferir se o Status e o Canal das 19:14 saíram (dias de post)",
        "Dias de post: 04/11 e depois 06, 09, 11, 13, 16, 18, 20, 23/11. Se não saiu, publicar à mão com o pacote do dia (ver descrição do evento de 24/11).", 20,
        rrule="FREQ=WEEKLY;BYDAY=MO,WE,FR;UNTIL=20261120T235959")

# 6) Black Friday (manual, se o Claude estiver parado)
E += ev("lembrete-forte", D(2026, 11, 26), T(20, 0), "WhatsApp: lembrete forte (amanhã é Black Friday)",
        "Texto em 07_PACOTE_DO_DIA/2026-11-26_qui/1_TEXTOS_DO_DIA.txt (bloco 20:00). Publicar à mão se o Claude estiver sem limite.", 15)
for h in (8, 12, 19):
    E += ev(f"dia-d-{h}", D(2026, 11, 27), T(h, 0), f"WhatsApp: disparo do dia D das {h:02d}:00",
            "Texto em 07_PACOTE_DO_DIA/2026-11-27_sex/1_TEXTOS_DO_DIA.txt. Publicar à mão se o Claude estiver sem limite.", 15)

linhas = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//Claude//Replanejamento 02-11-2026//PT", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
          "X-WR-CALNAME:Replanejamento Claude 02/11/2026"] + E + ["END:VCALENDAR"]
with open(SAIDA, "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(dobra(l) for l in linhas) + "\r\n")
print("eventos:", sum(1 for l in linhas if l == "BEGIN:VEVENT"), "->", SAIDA)
