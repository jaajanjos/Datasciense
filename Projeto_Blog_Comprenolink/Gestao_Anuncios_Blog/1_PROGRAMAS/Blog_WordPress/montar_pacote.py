#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deixa o pacote do outro PC pronto para levar (chamado pelo GERAR_EXE.bat, depois de compilar).

1. Tira do 4_PACOTE_OUTRO_PC qualquer wp_credenciais.json (a senha deste PC fica só em 2_DADOS):
   - se a pasta principal ainda não tem a senha, ela é MOVIDA para 2_DADOS\\Blog_WordPress;
   - se é igual à da pasta principal, a cópia do pacote é apagada;
   - se é diferente, fica guardada em 2_DADOS\\Blog_WordPress\\wp_credenciais_do_pacote_<data>.json.bak.
2. Refaz o 4_PACOTE_OUTRO_PC.zip a partir da pasta, sem nenhum arquivo de senha (instalação do zero).
3. Gera o 4_ATUALIZAR_OUTRO_PC.zip: só os programas (sem a pasta 2_DADOS) + ATUALIZAR_AQUI.bat, que
   copia por cima da instalação do outro PC sem nunca mexer na senha nem nos backups.

Uso:  python montar_pacote.py
"""
import os
import shutil
import sys
import zipfile
from datetime import datetime

RAIZ = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
PACOTE = os.path.join(RAIZ, "4_PACOTE_OUTRO_PC")
ZIP = PACOTE + ".zip"
DADOS = os.path.join(RAIZ, "2_DADOS", "Blog_WordPress")
CRED = os.path.join(DADOS, "wp_credenciais.json")
NUNCA_NO_PACOTE = ("wp_credenciais.json",)
ZIP_ATUALIZAR = os.path.join(RAIZ, "4_ATUALIZAR_OUTRO_PC.zip")
NOME_ATUALIZAR = "ATUALIZAR_OUTRO_PC"

# Rotina que roda NO OUTRO PC. Copia "arquivos" por cima da instalação, sem /MIR (não apaga nada)
# e pulando 2_DADOS inteiro: senha, backups e dados das máquinas ficam como estão.
BAT_ATUALIZAR = r"""@echo off
chcp 65001 >nul
setlocal
cd /d "%~dp0"
set "ORIGEM=%~dp0arquivos"
set "DESTINO=%~1"
echo ================================================================
echo   ATUALIZAR OS PAINEIS DOS BLOGS  (versao {versao})
echo   Troca so os programas. NAO mexe na senha nem nos backups.
echo ================================================================
echo.
if not exist "%ORIGEM%\1_PROGRAMAS\Blog_WordPress\PainelBlog.exe" (
  echo ERRO: extraia o .zip antes ^(botao direito ^> Extrair tudo^) e rode o ATUALIZAR_AQUI.bat de dentro da pasta extraida.
  goto fim
)
if defined DESTINO goto confere
for %%P in ("C:\4_PACOTE_OUTRO_PC" "C:\Blog_Manutencao" "C:\Blog_Manutencao\4_PACOTE_OUTRO_PC" "D:\4_PACOTE_OUTRO_PC" "%USERPROFILE%\Desktop\4_PACOTE_OUTRO_PC" "%USERPROFILE%\Documents\4_PACOTE_OUTRO_PC" "%USERPROFILE%\OneDrive\Desktop\4_PACOTE_OUTRO_PC") do (
  if not defined DESTINO if exist "%%~P\2_ABRIR_PAINEL_BLOG_WORDPRESS.bat" set "DESTINO=%%~P"
)
if defined DESTINO goto confere
echo Nao achei a pasta do painel sozinho.
echo Arraste para esta janela a pasta do painel (a que tem 2_ABRIR_PAINEL_BLOG_WORDPRESS.bat)
set /p "DESTINO=e aperte Enter: "
set "DESTINO=%DESTINO:"=%"
:confere
if "%DESTINO:~-1%"=="\" set "DESTINO=%DESTINO:~0,-1%"
if not exist "%DESTINO%\2_ABRIR_PAINEL_BLOG_WORDPRESS.bat" (
  echo ERRO: "%DESTINO%" nao e a pasta do painel ^(falta 2_ABRIR_PAINEL_BLOG_WORDPRESS.bat^). Nada foi alterado.
  goto fim
)
if exist "%DESTINO%\..\ATUALIZAR_AQUI.bat" (
  echo ERRO: essa e a pasta da propria atualizacao. Escolha a pasta do painel instalado. Nada foi alterado.
  goto fim
)
echo Pasta do painel: %DESTINO%
if exist "%DESTINO%\2_DADOS\Blog_WordPress\wp_credenciais.json" (echo Senha deste PC: encontrada, sera mantida) else (echo Senha deste PC: ainda nao cadastrada)
echo.
set "OK="
set /p "OK=Atualizar agora? (S/N): "
if /i not "%OK%"=="S" (echo Cancelado. Nada foi alterado. & goto fim)
echo.
echo Fechando o painel do WordPress, se estiver aberto...
taskkill /im PainelBlog.exe /f >nul 2>&1
ping -n 3 127.0.0.1 >nul
echo Copiando os programas novos...
robocopy "%ORIGEM%" "%DESTINO%" /E /XD 2_DADOS /XF wp_credenciais.json /R:3 /W:2 /NJH /NJS /NP /NFL /NDL >nul
if errorlevel 8 (
  echo ERRO ao copiar ^(algum arquivo em uso?^). Feche o painel e rode de novo. Seus dados nao foram tocados.
  goto fim
)
if not exist "%DESTINO%\2_DADOS\Blog_Maquinas" mkdir "%DESTINO%\2_DADOS\Blog_Maquinas"
if not exist "%DESTINO%\2_DADOS\Blog_WordPress\backups" mkdir "%DESTINO%\2_DADOS\Blog_WordPress\backups"
if not exist "%DESTINO%\2_DADOS\Blog_WordPress\wp_credenciais.exemplo.json" copy "%~dp0modelo\wp_credenciais.exemplo.json" "%DESTINO%\2_DADOS\Blog_WordPress\" >nul
echo.
echo PRONTO: programas atualizados para a versao {versao}.
if exist "%DESTINO%\2_DADOS\Blog_WordPress\wp_credenciais.json" (echo Senha e backups: mantidos.) else (echo Falta a senha: abra o atalho 2 e siga o passo 3 do LEIA-ME_COMO_INSTALAR_NO_OUTRO_PC.txt)
echo Abra o 2_ABRIR_PAINEL_BLOG_WORDPRESS.bat para conferir ^(deve aparecer "Conectado"^).
echo Depois pode apagar a pasta desta atualizacao.
:fim
echo.
pause
"""

LEIA_ATUALIZAR = """ATUALIZAR OS PAINÉIS NO OUTRO PC (versão {versao})
=================================================

Use isto quando o painel JÁ está instalado no outro PC.
Só troca os programas: a senha (wp_credenciais.json), os backups e os dados das
máquinas (pasta 2_DADOS) NÃO são tocados. Nada é apagado.

1. Copie o 4_ATUALIZAR_OUTRO_PC.zip para o outro PC (pendrive, e-mail...).
2. Botão direito no .zip > "Extrair tudo..." > Extrair (pode ser na Área de Trabalho).
3. Entre na pasta extraída e dê duplo clique em  ATUALIZAR_AQUI.bat
   - Ele acha sozinho a pasta do painel (C:\\4_PACOTE_OUTRO_PC, C:\\Blog_Manutencao,
     Área de Trabalho, Documentos). Se não achar, arraste a pasta do painel para a
     janela e aperte Enter.
   - Confira a pasta mostrada e responda S.
4. Abra o 2_ABRIR_PAINEL_BLOG_WORDPRESS.bat: deve aparecer "Conectado".
5. Pode apagar a pasta extraída e o .zip da atualização.

Primeira instalação (o PC ainda não tem o painel): use o 4_PACOTE_OUTRO_PC.zip.
"""


def limpar_senhas():
    for d, _, fs in os.walk(PACOTE):
        for f in fs:
            if f not in NUNCA_NO_PACOTE:
                continue
            achado = os.path.join(d, f)
            rel = os.path.relpath(achado, RAIZ)
            if not os.path.isfile(CRED):
                shutil.move(achado, CRED)
                print(f"  senha movida: {rel} -> {os.path.relpath(CRED, RAIZ)}")
            elif open(achado, "rb").read() == open(CRED, "rb").read():
                os.remove(achado)
                print(f"  cópia igual da senha apagada do pacote: {rel}")
            else:
                guarda = os.path.join(DADOS, f"wp_credenciais_do_pacote_{datetime.now():%Y-%m-%d_%Hh%M}.json.bak")
                shutil.move(achado, guarda)
                print(f"  senha DIFERENTE achada no pacote: guardada em {os.path.relpath(guarda, RAIZ)} (confira e apague)")


def refazer_zip():
    novo = ZIP + ".novo"
    with zipfile.ZipFile(novo, "w", zipfile.ZIP_DEFLATED) as z:
        for d, subs, fs in os.walk(PACOTE):
            rel_d = os.path.relpath(d, RAIZ)
            if not subs and not fs:
                z.write(d, rel_d + "/")
            for f in fs:
                if f not in NUNCA_NO_PACOTE and not f.endswith(".novo"):
                    z.write(os.path.join(d, f), os.path.join(rel_d, f))
        dentro = [n for n in z.namelist() if os.path.basename(n) in NUNCA_NO_PACOTE]
    if dentro:
        os.remove(novo)
        raise SystemExit(f"ERRO: senha entrou no zip ({dentro}); zip antigo mantido")
    os.replace(novo, ZIP)
    print(f"  {os.path.basename(ZIP)} refeito ({os.path.getsize(ZIP) / 1e6:.1f} MB, sem senha)")


def gerar_atualizacao():
    versao = datetime.now().strftime("%d/%m/%Y %Hh%M")
    crlf = lambda t: t.replace("\r\n", "\n").replace("\n", "\r\n").encode("utf-8")
    novo = ZIP_ATUALIZAR + ".novo"
    with zipfile.ZipFile(novo, "w", zipfile.ZIP_DEFLATED) as z:
        z.writestr(f"{NOME_ATUALIZAR}/ATUALIZAR_AQUI.bat", crlf(BAT_ATUALIZAR.replace("{versao}", versao)))
        z.writestr(f"{NOME_ATUALIZAR}/LEIA-ME_ATUALIZAR.txt", crlf(LEIA_ATUALIZAR.replace("{versao}", versao)))
        z.write(os.path.join(PACOTE, "2_DADOS", "Blog_WordPress", "wp_credenciais.exemplo.json"),
                f"{NOME_ATUALIZAR}/modelo/wp_credenciais.exemplo.json")
        for d, subs, fs in os.walk(PACOTE):
            rel = os.path.relpath(d, PACOTE)
            if rel.split(os.sep)[0] == "2_DADOS":
                subs[:] = []
                continue
            for f in fs:
                if f not in NUNCA_NO_PACOTE:
                    z.write(os.path.join(d, f), os.path.normpath(os.path.join(NOME_ATUALIZAR, "arquivos", rel, f)))
        ruins = [n for n in z.namelist() if "/2_DADOS/" in n.replace("\\", "/") or os.path.basename(n) in NUNCA_NO_PACOTE]
    if ruins:
        os.remove(novo)
        raise SystemExit(f"ERRO: dados entraram na atualização ({ruins[:3]}); zip antigo mantido")
    os.replace(novo, ZIP_ATUALIZAR)
    print(f"  {os.path.basename(ZIP_ATUALIZAR)} gerado ({os.path.getsize(ZIP_ATUALIZAR) / 1e6:.1f} MB, versão {versao}, "
          "só programas, sem 2_DADOS)")


def main():
    if not os.path.isdir(PACOTE):
        raise SystemExit(f"ERRO: pasta {PACOTE} não existe")
    print("Conferindo senha no pacote...")
    limpar_senhas()
    print("Refazendo o zip...")
    refazer_zip()
    print("Gerando o zip de atualização do outro PC...")
    gerar_atualizacao()


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    main()
