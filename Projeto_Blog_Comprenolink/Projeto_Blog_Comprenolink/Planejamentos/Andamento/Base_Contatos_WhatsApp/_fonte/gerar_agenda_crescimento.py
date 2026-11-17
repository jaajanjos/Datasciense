# -*- coding: utf-8 -*-
"""Gera agenda_crescimento_canal_whatsapp.ics (v2) com a rotina segura do DONO (processo_crescimento_canal_whatsapp.pdf).
Importar na agenda do dono (ele mesmo). UIDs fixos: importar de novo atualiza, nao duplica."""
import os, datetime

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
SAIDA = PASTA + "/agenda_crescimento_canal_whatsapp.ics"
TZ = "America/Sao_Paulo"
AGORA = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")


def dobra(linha):
    b = linha.encode("utf-8")
    if len(b) <= 74:
        return linha
    partes, atual = [], b""
    for ch in linha:
        cb = ch.encode("utf-8")
        if len(atual) + len(cb) > (74 if not partes else 73):
            partes.append(atual); atual = b""
        atual += cb
    partes.append(atual)
    return "\r\n ".join(p.decode("utf-8") for p in partes)


def esc(t):
    return t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


eventos = []


def ev(uid, titulo, data, hi, hf, desc, rrule=None, alarme=10):
    eventos.append((uid, titulo, data, hi, hf, desc, rrule, alarme))


ev("auto-convites-mao", "WhatsApp: convites à mão (até 5 na 1ª semana, depois até 9)", "20261106", "1000", "1015",
   "Abrir Base_Contatos_WhatsApp.xlsx > aba Hoje. Enviar PELO CELULAR, uma mensagem personalizada por pessoa, 3 minutos ou mais entre elas, só para quem você conhece. Nunca em massa. Ao primeiro aviso do WhatsApp, parar 7 dias. Depois escreva ao Claude: enviei Nome1, Nome2.", "FREQ=DAILY")
ev("auto-responder", "WhatsApp e Instagram: responder as pessoas", "20261105", "1920", "1925",
   "Responder quem escreveu depois da divulgação das 19:12 (WhatsApp, Direct e comentários). O Claude registra o resultado na aba Envios.", "FREQ=DAILY")
ev("auto-valida-dia", "WhatsApp: fechar o dia (2 min)", "20261106", "2030", "2035",
   "Anotar no Plano 30 dias do checklist: convites enviados, avisos do WhatsApp, pedidos de saída e entradas no Canal. Marcar V ou X. Se houve aviso do WhatsApp: parar os convites por 7 dias.", "FREQ=DAILY")
ev("auto-semanal", "WhatsApp: revisão semanal do Canal", "20261109", "1030", "1045",
   "Claude importa o formulário e lê os seguidores do Canal. Decidir: manter ou reduzir o ritmo dos convites. Ver indicadores no processo_crescimento_canal_whatsapp.pdf. Pasta: D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Base_Contatos_WhatsApp", "FREQ=WEEKLY;BYDAY=MO")
ev("auto-contatos-qui", "WhatsApp: aprovar contatos pessoais (Conhecido)", "20261105", "1030", "1035",
   "Escolher quem você conhece de verdade e mudar para Conhecido na aba Base. Nunca desconhecidos nem lista copiada.", "FREQ=WEEKLY;BYDAY=TH")
ev("auto-mensal", "WhatsApp: revisão mensal de consentimentos e exclusões", "20261201", "1030", "1050",
   "Atender pedidos de exclusão, apagar dados, conferir a Base e guardar backup (pasta _backups).", "FREQ=MONTHLY;BYMONTHDAY=1")

L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//comprenolink.net//Crescimento Canal WhatsApp//PT-BR", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
     "X-WR-CALNAME:comprenolink - Canal WhatsApp (dono)", "X-WR-TIMEZONE:" + TZ,
     "BEGIN:VTIMEZONE", "TZID:" + TZ, "BEGIN:STANDARD", "DTSTART:19700101T000000", "TZOFFSETFROM:-0300", "TZOFFSETTO:-0300", "TZNAME:-03", "END:STANDARD", "END:VTIMEZONE"]
for uid, tit, d, hi, hf, desc, rr, al in eventos:
    L += ["BEGIN:VEVENT", f"UID:{uid}-compre-no-link@comprenolink.net", f"DTSTAMP:{AGORA}", "SEQUENCE:2",
          f"DTSTART;TZID={TZ}:{d}T{hi}00", f"DTEND;TZID={TZ}:{d}T{hf}00", "SUMMARY:" + esc(tit), "DESCRIPTION:" + esc(desc)]
    if rr:
        L.append("RRULE:" + rr)
    if al:
        L += ["BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + esc(tit), f"TRIGGER:-PT{al}M", "END:VALARM"]
    L.append("END:VEVENT")
L.append("END:VCALENDAR")
open(SAIDA, "w", encoding="utf-8", newline="").write("\r\n".join(dobra(x) for x in L) + "\r\n")
print("OK:", SAIDA, "| eventos:", len(eventos))
