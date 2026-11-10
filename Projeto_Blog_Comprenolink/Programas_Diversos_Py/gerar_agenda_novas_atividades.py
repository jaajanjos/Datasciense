# -*- coding: utf-8 -*-
"""Gera D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/agenda_novas_atividades.ics: o que o DONO faz a partir de 31/10/2026 (envios do dia, reunião,
confirmações) e os lembretes de que o Claude precisa do PC ligado. Os envios vêm do 1_TEXTOS_DO_DIA.txt de cada pasta do pacote.
Rodar:  python -X utf8 gerar_agenda_novas_atividades.py
Horários em UTC (Brasília = UTC-3), como as outras agendas .ics do projeto.
"""
import glob
import os
import re
from datetime import datetime, timedelta, timezone

PACOTES = "D:/Projeto_Blog_Comprenolink/Planejamentos/Andamento/Celular_Whatsapp/07_PACOTE_DO_DIA"
SAIDA = "D:/Projeto_Blog_Comprenolink/0- Pendencias/1_Pendencias/agenda_novas_atividades.ics"
PASTA_REL = r"D:\Projeto_Blog_Comprenolink\Planejamentos\Andamento\Celular_Whatsapp\07_PACOTE_DO_DIA"
BRT = timezone(timedelta(hours=-3))
AGORA = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
PDF = r"D:\Projeto_Blog_Comprenolink\0- Pendencias\1_Pendencias\Pendencias_Dono_Passo_a_Passo_2026-10-31.pdf"
LIMITE = datetime(2026, 10, 31, 17, 30, tzinfo=BRT)  # só eventos depois de agora


def esc(t):
    return t.replace("\\", "\\\\").replace(";", "\\;").replace(",", "\\,").replace("\n", "\\n")


def dobra(linha):
    """RFC 5545: linhas com mais de 75 bytes são dobradas (sem cortar caractere UTF-8)."""
    b, partes, atual = linha.encode("utf-8"), [], b""
    for ch in linha:
        cb = ch.encode("utf-8")
        if len(atual) + len(cb) > (74 if partes else 75):
            partes.append(atual)
            atual = b""
        atual += cb
    partes.append(atual)
    return "\r\n ".join(p.decode("utf-8") for p in partes)


def utc(dt):
    return dt.astimezone(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


eventos = []


def evento(uid, inicio, minutos, resumo, descricao, alarme=15):
    eventos.append((uid, inicio, inicio + timedelta(minutes=minutos), resumo, descricao, alarme))


def d(dia, mes, h, mi=0):
    return datetime(2026, mes, dia, h, mi, tzinfo=BRT)


# ---------------- Claude / PC ligado
evento("claude-2910", d(31, 10, 20, 0), 45, "PC ligado: o Claude agenda 29/11 às 20:39",
       "Deixe ligados: computador (sem suspender), app Claude aberto e Chrome aberto no Instagram @compre.no.link logado.\n"
       "O Claude agenda o post (19:00) e o Reels (19:05) de 29/11. Se falhar, escreva \"agendar 29/11\" ao Claude.\nPasso a passo: " + PDF, 30)
evento("claude-3011", d(1, 11, 20, 0), 45, "PC ligado: o Claude agenda 30/11 às 20:39",
       "Mesmo cuidado de ontem: PC ligado, app Claude e Chrome abertos, Instagram logado.\nO Claude agenda 30/11 (post 19:00 e Reels 19:05).", 30)
evento("claude-recriar", d(6, 11, 20, 0), 30, "Claude: recriar a rotina diária de agendamento",
       "A rotina diária dura 7 dias e expira depois de 05/11. Abra o app Claude e peça: recriar a rotina de agendamento do Instagram.\n"
       "Depois disso o Claude segue agendando um dia por noite até 23/12.", 30)

# ---------------- Reunião e confirmações
evento("reuniao-0511", d(5, 11, 10, 0), 60, "Reunião: Turbinar e termos do ML Afiliados",
       "Levar: Plano Turbinar (0- Pendencias\\5_Plano_turbinar_anuncio_instagram), painel de conversão (Relatorios_Diarios_Anuncios) e o resultado das vendas "
       "(19 vendas no histórico: 12 pendentes e 7 recusadas por conta vinculada; comissão pendente R$ 172,00).\n"
       "Decidir: usar o Turbinar? verba por dia? por que 7 vendas foram recusadas? quem publica quando o dono não puder?\n"
       "Depois: contar as decisões ao Claude. Passo a passo: " + PDF, 60 * 24)
evento("confirma-csv", d(2, 11, 9, 0), 20, "Confirmar: a conta do CSV de vendas é a do blog?",
       "No ML Afiliados (login do comprenolink.net), compare com o arquivo vendas_ml_2026-10-31.csv: 19 vendas e R$ 172,00 de comissão pendente.\n"
       "Escreva ao Claude: \"é a do blog\" ou \"não é\". (Data sugerida; mude se preferir.)", 30)
evento("confirma-sync", d(2, 11, 9, 30), 20, "Verificar sincronização entre os PCs (SVR e lenovo)",
       "Em 31/10 o gerador do relatório voltou sozinho a uma versão antiga. Veja no outro PC se há OneDrive, Syncthing, tarefa agendada ou script "
       "(como sincronizar_copias.py) copiando D:\\Projeto_Blog_Comprenolink. Avise o Claude para ele ajustar. (Data sugerida.)", 30)

# ---------------- Envios do dono, lidos de cada pacote do dia
for pasta in sorted(glob.glob(PACOTES + "/2026-*")):
    m = re.match(r"(\d{4})-(\d{2})-(\d{2})_(\w+)", os.path.basename(pasta))
    arq = os.path.join(pasta, "1_TEXTOS_DO_DIA.txt")
    if not m or not os.path.exists(arq):
        continue
    ano, mes, dia = int(m[1]), int(m[2]), int(m[3])
    txt = open(arq, encoding="utf-8-sig").read()
    cab = re.findall(r"^(\d\d):(\d\d)\s+(.+)$", txt, flags=re.M)
    produto = "dia de lista"
    if any("Post no feed" in c for _, _, c in cab):
        ach = re.search(r"[🔥🎄]\s*([^\n]+)", txt.split("Post no feed", 1)[1])
        if ach:
            produto = re.sub(r"^(Black Friday|Natal):\s*", "", ach.group(1).strip())
    for hh, mm, c in cab:
        if "Post no feed" in c or "Reels" in c:
            continue
        ini = datetime(ano, mes, dia, int(hh), int(mm), tzinfo=BRT)
        if ini < LIMITE:
            continue
        canal = re.sub(r"^(Instagram|WhatsApp) – ", lambda x: x.group(1) + " ", c).split(" (")[0]
        desc = (f"Dia {dia:02d}/{mes:02d}: {produto}.\nPasta: {PASTA_REL}\\{os.path.basename(pasta)}\n"
                f"Abra o 1_TEXTOS_DO_DIA.txt e use o bloco \"{hh}:{mm} {c}\" (texto e imagem indicados nele).\n"
                "Regras: sem preço, sem \"mais vendido/melhor preço\", sempre o aviso de link de afiliado.")
        if "Story" in c:
            desc += "\nStory: + > Story > story.png > adesivo Link > cole o link do bloco > publicar."
        evento(f"envio-{ano}{mes:02d}{dia:02d}-{hh}{mm}", ini, 10, f"{canal}: {produto}", desc, 10)

# ---------------- grava
linhas = ["BEGIN:VCALENDAR", "VERSION:2.0", "PRODID:-//comprenolink//Novas atividades//PT-BR", "CALSCALE:GREGORIAN",
          "X-WR-CALNAME:Novas atividades comprenolink", "X-WR-TIMEZONE:America/Sao_Paulo"]
for uid, ini, fim, resumo, desc, alarme in sorted(eventos, key=lambda e: e[1]):
    linhas += ["BEGIN:VEVENT", f"UID:{uid}@comprenolink.net", f"DTSTAMP:{AGORA}", f"DTSTART:{utc(ini)}", f"DTEND:{utc(fim)}",
               f"SUMMARY:{esc(resumo)}", f"DESCRIPTION:{esc(desc)}", "BEGIN:VALARM", "ACTION:DISPLAY",
               f"DESCRIPTION:{esc(resumo)}", f"TRIGGER:-PT{alarme}M", "END:VALARM", "END:VEVENT"]
linhas.append("END:VCALENDAR")
with open(SAIDA, "w", encoding="utf-8", newline="") as f:
    f.write("\r\n".join(dobra(l) for l in linhas) + "\r\n")
print(f"{len(eventos)} eventos -> {SAIDA}")
primeiro = min(eventos, key=lambda e: e[1])
ultimo = max(eventos, key=lambda e: e[1])
print("de", primeiro[1].strftime("%d/%m %H:%M"), "até", ultimo[1].strftime("%d/%m %H:%M"))
