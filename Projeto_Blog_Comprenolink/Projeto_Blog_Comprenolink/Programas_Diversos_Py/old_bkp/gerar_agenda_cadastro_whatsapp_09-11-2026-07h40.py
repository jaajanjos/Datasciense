# -*- coding: utf-8 -*-
"""Agenda .ics do cadastro das 7 categorias no WhatsApp (segunda 02/11/2026, depois das 10:00, já com o limite semanal do Claude renovado às 02:00).
Rodar:  python -X utf8 gerar_agenda_cadastro_whatsapp.py
Saída:  D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/agenda_cadastro_categorias_WhatsApp_2026-11-02.ics
"""
from datetime import datetime, timedelta, timezone

SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/agenda_cadastro_categorias_WhatsApp_2026-11-02.ics"
GUIA = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\Cadastrar_7_categorias_WhatsApp_2026-11-01.pdf"
TXT = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\Textos_7_categorias_WhatsApp_COPIAR.txt"
FOTOS = r"D:\Projeto_Blog_Comprenolink\4- Celular_Whatsapp\06_CATALOGO_WHATSAPP\CATEGORIAS\fotos"
DIA = (2026, 11, 2)
EVENTOS = [
    (10, 10, 20, "WhatsApp: cadastrar as categorias 1 a 3 (Tecnologia, Áudio & TV, Casa & Eletrodomésticos)",
     f"Fazer no WhatsApp Web, no computador: Ferramentas comerciais > Catálogo > Adicionar item.\nGuia: {GUIA}\nTextos para copiar (com emoji): {TXT}\nFotos: {FOTOS}\n"
     "Preço em branco. Link curto (limite de 75 caracteres). Cerca de 4 minutos por categoria."),
    (10, 30, 20, "WhatsApp: cadastrar as categorias 4 a 6 (Casa Cama & Decoração, Ferramentas, Esporte & Fitness)",
     f"Mesmo passo a passo. Guia: {GUIA}\nTextos: {TXT}"),
    (10, 50, 10, "WhatsApp: cadastrar a categoria 7 (Beleza & Saúde)",
     f"Última categoria. Guia: {GUIA}\nTextos: {TXT}"),
    (11, 0, 10, "WhatsApp: apagar o item CNL-111 (Kit Skincare Vitamina C Dermachem)",
     "O produto saiu do Mercado Livre. WhatsApp Business > Catálogo > toque no item > Excluir. O Claude não apaga itens (não tem volta)."),
    (11, 10, 10, "WhatsApp: sair do aparelho conectado do WhatsApp Web (se não for mais usar)",
     "WhatsApp Business no celular > Aparelhos conectados > toque no aparelho > Sair. Fecha o acesso que o Claude usou em 01/11 com a sua autorização."),
    (11, 20, 15, "Avisar o Claude: categorias cadastradas (ele valida no WhatsApp Web e atualiza a planilha)",
     "O limite semanal do Claude renova na segunda às 02:00, então ele já está disponível. Escreva: terminei as 7 categorias.\n"
     "Se autorizar de novo, o Claude confere o catálogo no WhatsApp Web, marca Cadastrado = S na planilha e atualiza o relatório."),
]
BRT = timezone(timedelta(hours=-3))


def esc(t):
    return t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def dobra(linha):
    partes, atual = [], b""
    for ch in linha:
        cb = ch.encode("utf-8")
        if len(atual) + len(cb) > (74 if partes else 75):
            partes.append(atual)
            atual = b""
        atual += cb
    partes.append(atual)
    return "\r\n ".join(p.decode("utf-8") for p in partes)


agora = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
L = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//comprenolink//Cadastro WhatsApp//PT-BR", "CALSCALE:GREGORIAN",
     "X-WR-CALNAME:Cadastro das categorias no WhatsApp", "X-WR-TIMEZONE:America/Sao_Paulo",
     "BEGIN:VTIMEZONE", "TZID:America/Sao_Paulo", "BEGIN:STANDARD", "DTSTART:19700101T000000", "TZOFFSETFROM:-0300",
     "TZOFFSETTO:-0300", "TZNAME:-03", "END:STANDARD", "END:VTIMEZONE"]
for i, (h, m, dur, tit, desc) in enumerate(EVENTOS, 1):
    ini = datetime(*DIA, h, m)
    fim = ini + timedelta(minutes=dur)
    L += ["BEGIN:VEVENT", f"UID:cadastro-whatsapp-{i}@comprenolink.net", f"DTSTAMP:{agora}",
          f"DTSTART;TZID=America/Sao_Paulo:{ini:%Y%m%dT%H%M%S}", f"DTEND;TZID=America/Sao_Paulo:{fim:%Y%m%dT%H%M%S}",
          f"SUMMARY:{esc(tit)}", f"DESCRIPTION:{esc(desc)}", "BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{esc(tit)}",
          "TRIGGER:-PT15M", "END:VALARM", "END:VEVENT"]
L.append("END:VCALENDAR")
with open(SAIDA, "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(dobra(x) for x in L) + "\r\n")
print(f"{len(EVENTOS)} eventos -> {SAIDA}")
