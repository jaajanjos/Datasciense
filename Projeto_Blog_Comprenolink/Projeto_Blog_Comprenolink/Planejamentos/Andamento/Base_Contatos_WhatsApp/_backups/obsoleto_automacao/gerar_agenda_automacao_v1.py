# -*- coding: utf-8 -*-
"""Gera agenda_automacao_whatsapp.ics com as atribuicoes do DONO (processo_automatização_whatsapp.pdf, itens 8 a 10).
Importar na agenda do dono (ele mesmo). UIDs fixos: importar de novo atualiza, nao duplica."""
import os, datetime

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
SAIDA = PASTA + "/agenda_automacao_whatsapp.ics"
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


ev("auto-valida-fila", "WhatsApp: validar a fila do dia (aba Hoje)", "20261110", "0950", "0955",
   "Abrir Base_Contatos_WhatsApp.xlsx > aba Hoje. Conferir nomes e mensagens. Garantir PC ligado, Chrome aberto e WhatsApp Web logado. Se algo estiver estranho, escrever pausar automação no chat. Vale quando a automação estiver ativada.", "FREQ=DAILY")
ev("auto-responder", "WhatsApp e Instagram: responder as pessoas", "20261105", "1920", "1925",
   "Responder quem escreveu depois da divulgação das 19:12 (WhatsApp, Direct e comentários). O Claude registra o resultado na aba Envios.", "FREQ=DAILY")
ev("auto-valida-dia", "WhatsApp: validação final do dia (checklist)", "20261110", "2030", "2035",
   "Ler o relatório do Claude. Aba Envios: nenhuma linha com ALERTA e no máximo 9 envios. Marcar V ou X no quadro de 14 dias do PDF processo_automatização_whatsapp.pdf (item 11).", "FREQ=DAILY")
ev("auto-semanal", "WhatsApp: revisão semanal do Canal e da automação", "20261109", "1030", "1045",
   "Claude importa o formulário e lê os seguidores do Canal. Decidir: subir, manter ou reduzir o ritmo. Ver indicadores do item 12 do PDF do processo. Pasta: D:\\Projeto_Blog_Comprenolink\\Planejamentos\\Andamento\\Base_Contatos_WhatsApp", "FREQ=WEEKLY;BYDAY=MO")
ev("auto-contatos-qui", "WhatsApp: aprovar contatos pessoais novos", "20261105", "1030", "1035",
   "Escolher quem pode receber o convite (conhecidos) e passar o número ao Claude. Só quem você conhece. Nunca lista comprada.", "FREQ=WEEKLY;BYDAY=TH")
ev("auto-mensal", "WhatsApp: revisão mensal de consentimentos e exclusões", "20261201", "1030", "1050",
   "Atender pedidos de exclusão, apagar dados, conferir a Base e guardar backup (pasta _backups).", "FREQ=MONTHLY;BYMONTHDAY=1")
ev("auto-autorizar", "WhatsApp: escrever a autorização da automação (se a base tem 9 aptos)", "20261110", "0900", "0910",
   "Só se a aba Hoje tiver pelo menos 9 contatos com SIM. Copiar o termo do item 6 do PDF para o chat com o Claude. Começa a fase 1 (3 envios por dia).")
ev("auto-fase2", "WhatsApp: decidir fase 2 (6 envios por dia)", "20261117", "0900", "0910",
   "Semana 1 sem alerta e com até 5% de pedidos de saída? Se sim, autorizar 6 por dia. Se não, manter 3.")
ev("auto-fase3", "WhatsApp: decidir fase 3 (9 envios por dia)", "20261124", "0900", "0910",
   "Semana 2 sem alerta e com até 5% de pedidos de saída? Se sim, autorizar 9 por dia. Se não, manter 6.")
ev("auto-pausa-bf", "WhatsApp: automação de convites PAUSADA (Black Friday)", "20261127", "0815", "0820",
   "Dia D da Black Friday: sem convites automáticos. Retoma em 28/11 se tudo estiver certo.", None, 0)
ev("auto-retoma-bf", "WhatsApp: retomar convites automáticos", "20261128", "0900", "0905",
   "Conferir a aba Hoje e o relatório de 27/11. Retomar na fase em que estava.", None, 10)

L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//comprenolink.net//Automacao WhatsApp//PT-BR", "CALSCALE:GREGORIAN", "METHOD:PUBLISH",
     "X-WR-CALNAME:comprenolink - Automação WhatsApp (dono)", "X-WR-TIMEZONE:" + TZ,
     "BEGIN:VTIMEZONE", "TZID:" + TZ, "BEGIN:STANDARD", "DTSTART:19700101T000000", "TZOFFSETFROM:-0300", "TZOFFSETTO:-0300", "TZNAME:-03", "END:STANDARD", "END:VTIMEZONE"]
for uid, tit, d, hi, hf, desc, rr, al in eventos:
    L += ["BEGIN:VEVENT", f"UID:{uid}-compre-no-link@comprenolink.net", f"DTSTAMP:{AGORA}",
          f"DTSTART;TZID={TZ}:{d}T{hi}00", f"DTEND;TZID={TZ}:{d}T{hf}00", "SUMMARY:" + esc(tit), "DESCRIPTION:" + esc(desc)]
    if rr:
        L.append("RRULE:" + rr)
    if al:
        L += ["BEGIN:VALARM", "ACTION:DISPLAY", "DESCRIPTION:" + esc(tit), f"TRIGGER:-PT{al}M", "END:VALARM"]
    L.append("END:VEVENT")
L.append("END:VCALENDAR")
open(SAIDA, "w", encoding="utf-8", newline="").write("\r\n".join(dobra(x) for x in L) + "\r\n")
print("OK:", SAIDA, "| eventos:", len(eventos))
