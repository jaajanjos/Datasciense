# -*- coding: utf-8 -*-
"""Calendário .ics da rotina do Instagram (lê 07_PACOTE_DO_DIA): 1 evento por dia de post + trocas de bio e destaques.
Gera 12_CALENDARIO_INSTAGRAM.ics e copia para E:\\OneDrive\\Download.  Rodar:  python -X utf8 _fonte\\gerar_calendario_instagram.py
"""
import os
import re
import shutil
from datetime import datetime, timedelta

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PACOTE = os.path.join(RAIZ, "07_PACOTE_DO_DIA")
SAIDA = os.path.join(RAIZ, "12_CALENDARIO_INSTAGRAM.ics")
COPIAS = [r"E:\OneDrive\Download", r"D:\mercado_livre\4- Celular_Whatsapp"]
UTC = timedelta(hours=3)  # Brasília = UTC-3 (sem horário de verão)


def esc(t):
    return t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def evento(uid, ini, minutos, titulo, desc, alarme=30):
    f = lambda d: (d + UTC).strftime("%Y%m%dT%H%M%SZ")
    return ["BEGIN:VEVENT", f"UID:{uid}@comprenolink.net", f"DTSTAMP:{f(datetime.now())}",
            f"DTSTART:{f(ini)}", f"DTEND:{f(ini + timedelta(minutes=minutos))}",
            f"SUMMARY:{esc(titulo)}", f"DESCRIPTION:{esc(desc)}",
            "BEGIN:VALARM", "ACTION:DISPLAY", f"DESCRIPTION:{esc(titulo)}", f"TRIGGER:-PT{alarme}M", "END:VALARM",
            "END:VEVENT"]


def main():
    ev, dias = [], []
    for pasta in sorted(os.listdir(PACOTE)):
        with open(os.path.join(PACOTE, pasta, "1_TEXTOS_DO_DIA.txt"), encoding="utf-8-sig") as f:
            txt = f.read()
        if "Instagram – Post no feed" not in txt:
            continue  # dia só de WhatsApp
        dia = datetime.strptime(pasta[:10], "%Y-%m-%d")
        produto = re.search(r"Post no feed.*?\n=+\n(.+?)\n", txt, re.S).group(1).strip(" 🔥🎄")
        dias.append(dia)
        ev += evento(f"ig-{pasta[:10]}", dia.replace(hour=18, minute=45), 30, f"📸 Instagram: post 19:00 + story 19:10 – {produto}",
                     f"Pasta do dia: 07_PACOTE_DO_DIA\\{pasta}\n"
                     "1) 18:45 – avise o Claude: ele mostra o post do feed e publica às 19:00 com o seu OK.\n"
                     "2) 19:10 – no CELULAR: Story com story.png + adesivo LINK (link está em 1_TEXTOS_DO_DIA.txt).\n"
                     "3) Responder no Direct quem comentou: digite bf (ou natal) e toque na resposta salva.")
    d3 = dias[2] if len(dias) > 2 else dias[-1]
    ev += evento("ig-destaques", d3.replace(hour=10), 20, "⭐ Instagram: criar os Destaques (celular)",
                 "Já existem stories publicados. Peça ao Claude o passo a passo: Black Friday, Categorias, Como comprar.")
    ano = dias[0].year
    ev += evento("ig-bio-natal", datetime(ano, 12, 1, 9), 15, "🎄 Instagram: trocar bio e link para Natal (celular)",
                 "Link 1 da bio: comprenolink.net/presentes-de-natal (título: Presentes de Natal – lista no blog).\n"
                 "Bio: versão DEZEMBRO em 03_TEXTOS_PRONTOS_PARA_COPIAR.txt (o Claude pode colar a bio pelo computador).\n"
                 "Search Console: pedir indexação de /presentes-de-natal/.")
    ev += evento("ig-bio-pos-natal", datetime(ano, 12, 26, 9), 15, "🔗 Instagram: trocar link da bio para o blog (celular)",
                 "Link 1 da bio: comprenolink.net (título: Achados por categoria). Peça ao Claude a bio nova.")
    ics = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//comprenolink//Instagram//PT-BR", "CALSCALE:GREGORIAN",
           "X-WR-CALNAME:Instagram comprenolink"] + ev + ["END:VCALENDAR"]
    with open(SAIDA, "w", encoding="utf-8", newline="\r\n") as f:
        f.write("\n".join(ics) + "\n")
    for c in COPIAS:
        if os.path.isdir(c):
            shutil.copy2(SAIDA, c)
    print(len(dias), "dias de post + 3 lembretes ->", SAIDA)


if __name__ == "__main__":
    main()
