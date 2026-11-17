# -*- coding: utf-8 -*-
"""Traz para a aba Base as inscricoes do formulario do blog (Fluent Forms, form 4) que informaram WhatsApp E marcaram a caixa de consentimento.
Uso:
  python -X utf8 importar_leads_formulario.py            -> so MOSTRA o que entraria (simulacao)
  python -X utf8 importar_leads_formulario.py --gravar   -> grava na planilha (feche o Excel antes; faz backup)
Regras: ignora numero ja existente na Base; ignora sem caixa marcada; normaliza o numero para 55 + DDD + numero.
"""
import sys, os, re, json, shutil, datetime
sys.path.insert(0, "D:/Projeto_Blog_Comprenolink/Gestao_Anuncios_Blog/1_PROGRAMAS/Blog_WordPress")
import gerenciar_blog as g
from openpyxl import load_workbook

PASTA = os.path.dirname(os.path.dirname(os.path.abspath(__file__))).replace("\\", "/")
XLSX = PASTA + "/Base_Contatos_WhatsApp.xlsx"
B0, B1 = 5, 504


def normaliza(tel):
    d = re.sub(r"\D", "", str(tel or ""))
    d = d.lstrip("0")
    if len(d) in (10, 11):
        d = "55" + d
    return d if (d.startswith("55") and len(d) in (12, 13)) else ""


def marcado(v):
    if isinstance(v, list):
        v = " ".join(map(str, v))
    return str(v).strip().lower() not in ("", "0", "false", "no", "não", "nao", "none", "null")


def ler_entradas(cfg):
    out, pagina = [], 1
    while True:
        r = g.requisitar(cfg, "GET", f"/wp-json/fluentform/v1/submissions?form_id=4&per_page=100&page={pagina}", None)
        dados = r.get("data", [])
        out += dados
        if not r.get("next_page_url") or not dados:
            break
        pagina += 1
    return out


def resposta(ent):
    resp = ent.get("response", ent)
    if isinstance(resp, str):
        try:
            resp = json.loads(resp)
        except Exception:
            resp = {}
    return resp if isinstance(resp, dict) else {}


def main():
    gravar = "--gravar" in sys.argv
    cfg = g.carregar_config()
    wb = load_workbook(XLSX)
    ws = wb["Base"]
    existentes = {str(ws.cell(row=r, column=3).value or "") for r in range(B0, B1 + 1)}
    livre = [r for r in range(B0, B1 + 1) if not ws.cell(row=r, column=2).value]
    novos, pulados = [], 0
    for ent in ler_entradas(cfg):
        rp = resposta(ent)
        tel = normaliza(rp.get("whatsapp"))
        if not tel or not marcado(rp.get("consentimento_whatsapp")) or tel in existentes:
            pulados += 1
            continue
        novos.append((str(rp.get("nome") or "").strip() or "Sem nome", tel, str(ent.get("created_at", ""))[:10], ent.get("id")))
        existentes.add(tel)
    print(f"Inscricoes lidas: {len(novos) + pulados} | entram: {len(novos)} | ignoradas (sem WhatsApp, sem caixa ou repetidas): {pulados}")
    for n in novos:
        print("  +", n[0], n[1], n[2], "entrada", n[3])
    if not gravar:
        print("Simulacao. Para gravar: --gravar")
        return
    if len(novos) > len(livre):
        print("Sem linhas livres na Base."); return
    if not novos:
        return
    os.makedirs(PASTA + "/_backups", exist_ok=True)
    shutil.copy2(XLSX, PASTA + "/_backups/Base_Contatos_WhatsApp_antes_import_" + datetime.datetime.now().strftime("%d-%m-%Y_%Hh%M") + ".xlsx")
    for (nome, tel, dia, eid), r in zip(novos, livre):
        d = datetime.datetime.strptime(dia, "%Y-%m-%d").date() if re.match(r"\d{4}-\d{2}-\d{2}", dia) else datetime.date.today()
        ws.cell(row=r, column=2, value=nome)
        ws.cell(row=r, column=3, value=int(tel))
        ws.cell(row=r, column=4, value="Blog - formulário")
        ws.cell(row=r, column=5, value=d)
        ws.cell(row=r, column=6, value="Sim")
        ws.cell(row=r, column=7, value=d)
        ws.cell(row=r, column=8, value=f"Formulário do blog, entrada nº {eid}: informou o WhatsApp e marcou a caixa de consentimento")
        ws.cell(row=r, column=9, value="Não sei")
        ws.cell(row=r, column=10, value="Não")
    wb.save(XLSX)
    print("Gravado:", len(novos), "contato(s).")


if __name__ == "__main__":
    main()
