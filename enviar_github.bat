@echo off
echo ===================================================
echo   INICIANDO O ENVIO DOS ARQUIVOS PARA O GITHUB...
echo ===================================================

:: Define o arquivo de log
set LOG_FILE=D:\Github_Area\log_envio_github.txt

:: O Windows entra na pasta do projeto
cd /d "D:\Github_Area"

:: Registra a data e hora iniciais no log
echo Instante do envio: %date% as %time% > "%LOG_FILE%"
echo --------------------------------------------------- >> "%LOG_FILE%"

:: Executa os comandos nativos do Git direto pelo Windows e grava tudo no log
git add . >> "%LOG_FILE%" 2>&1
git commit -m "Atualizacao automatica via BAT" >> "%LOG_FILE%" 2>&1
git push >> "%LOG_FILE%" 2>&1

echo ===================================================
echo   PROCESSO CONCLUIDO! FECHANDO EM 5 SEGUNDOS...
echo ===================================================
timeout /t 5