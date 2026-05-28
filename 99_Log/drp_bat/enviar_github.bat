@echo off
echo ===================================================
echo   INICIANDO O ENVIO DOS ARQUIVOS PARA O GITHUB...
echo ===================================================

:: 1. Limpa a data (considera formato DD/MM/AAAA)
set DATA_LIMPA=%DATE:~0,2%%DATE:~3,2%%DATE:~6,4%

:: 2. Limpa a hora e substitui espaços por zero (caso seja antes das 10h)
set HORA_ATUAL=%TIME: =0%
set HORA_LIMPA=%HORA_ATUAL:~0,2%%HORA_ATUAL:~3,2%%HORA_ATUAL:~6,2%

:: 3. Concatena tudo em uma única variável
set NOME_ARQUIVO=log_envio_github_%DATA_LIMPA%_%HORA_LIMPA%.txt

:: Define o arquivo de log
set LOG_FILE=D:\Github_Area\99_Log\%NOME_ARQUIVO%.txt

:: Força o Windows a entrar na pasta correta
cd /d "D:\Github_Area"

:: Registra a data e hora iniciais no log
echo Instante do envio: %date% as %time% > "%LOG_FILE%"
echo --------------------------------------------------- >> "%LOG_FILE%"

:: [INTELIGÊNCIA 1] Checa se a pasta oculta .git existe. Se nao existir, recupera.
if not exist "D:\Github_Area\.git" (
    echo [AVISO] Pasta .git nao encontrada! Reconfigurando repositorio... >> "%LOG_FILE%"
    git init >> "%LOG_FILE%" 2>&1
    git checkout -b master >> "%LOG_FILE%" 2>&1
    git remote add origin https://github.com/jaajanjos/Datasciense.git >> "%LOG_FILE%" 2>&1
    git pull origin master >> "%LOG_FILE%" 2>&1
)

:: Prepara os arquivos e cria o ponto de salvamento local
git add . >> "%LOG_FILE%" 2>&1
git commit -m "Atualizacao automatica via BAT" >> "%LOG_FILE%" 2>&1

:: [INTELIGÊNCIA 2](CORRIGIDO) Sincroniza com a nuvem guardando alterações pendentes para evitar o erro de rebase
git pull origin master --rebase >> "%LOG_FILE%" 2>&1

:: Envia os dados atualizados de forma segura
git push origin master >> "%LOG_FILE%" 2>&1

echo ==========================================================================================
echo   AGUARDE O FINAL DO PROCESSO  NÃO CANCELE ATE SER CONCLUIDO! FECHANDO EM 5 SEGUNDOS...
echo ==========================================================================================
timeout /t 5