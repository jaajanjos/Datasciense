# -*- coding: utf-8 -*-
"""
Copia a documentação gerada para:
  D:\\mercado_livre\\4- Celular_Whatsapp      (só o que é do WhatsApp/celular)
  E:\\OneDrive\\Download\\Divulgacao_Blog     (tudo, para abrir no celular pelo app OneDrive)
Rodar depois de gerar_divulgacao.py e gerar_artes_catalogo.py:  python -X utf8 _fonte\\sincronizar_copias.py
Só copia (nunca apaga nada no destino).
"""
import os
import shutil

ORIGEM = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WHATSAPP = r"D:\mercado_livre\4- Celular_Whatsapp"
ONEDRIVE = r"E:\OneDrive\Download\Divulgacao_Blog"
SO_WHATSAPP = ["08_PASSO_A_PASSO_WHATSAPP_NO_CELULAR.pdf", "06_CATALOGO_WHATSAPP", "07_PACOTE_DO_DIA",
               "03_TEXTOS_PRONTOS_PARA_COPIAR.txt", "05_LINKS_RASTREAVEIS.txt", "01_GUIA_COMPLETO_DIVULGACAO.pdf",
               "02_CHECKLISTS_IMPRIMIVEIS.pdf", "04_CALENDARIO_POSTS_NOV_DEZ.xlsx", "09_LOGO"]
TUDO = ["00_LEIA-ME_COMECE_AQUI.txt"] + SO_WHATSAPP + ["10_POST_BOAS_VINDAS", "11_INSTAGRAM_RESPOSTAS_SALVAS.txt"]  # post fixado do Instagram


def copia(nomes, destino):
    os.makedirs(destino, exist_ok=True)
    presos = []
    for n in nomes:
        o, d = os.path.join(ORIGEM, n), os.path.join(destino, n)
        try:
            if os.path.isdir(o):
                shutil.copytree(o, d, dirs_exist_ok=True)
            elif os.path.isfile(o):
                shutil.copy2(o, d)
        except (PermissionError, shutil.Error) as erro:  # arquivo aberto no PDF/Excel: segue com os outros
            presos.append(f"{n} ({str(erro)[:80]})")
    print("copiado para", destino, "| não copiados (arquivo aberto):" if presos else "", "; ".join(presos))


if __name__ == "__main__":
    copia(SO_WHATSAPP, WHATSAPP)
    if os.path.isdir(os.path.dirname(ONEDRIVE)):
        copia(TUDO, ONEDRIVE)
