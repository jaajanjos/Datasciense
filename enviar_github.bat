@echo off
echo ===================================================
echo   INICIANDO O ENVIO DOS ARQUIVOS PARA O GITHUB...
echo ===================================================

:: Define o arquivo de log
set LOG_FILE=D:\Github_Area\log_envio_github.txt

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

:: [INTELIGÊNCIA 2] Sincroniza com a nuvem ANTES de enviar para evitar rejeições
git pull origin master --rebase >> "%LOG_FILE%" 2>&1

:: Envia os dados atualizados de forma segura
git push origin master >> "%LOG_FILE%" 2>&1

echo ===================================================
echo   PROCESSO CONCLUIDO! FECHANDO EM 5 SEGUNDOS...
echo ===================================================
timeout /t 5