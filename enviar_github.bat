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

:: [INTELIGÊNCIA DO SCRIPT] Checa se a pasta oculta .git existe. 
:: Se NÃO existir, ele roda os passos de recuperação sozinho!
if not exist "D:\Github_Area\.git" (
    echo [AVISO] Pasta .git nao encontrada! Reconfigurando repositorio... >> "%LOG_FILE%"
    git init >> "%LOG_FILE%" 2>&1
    git checkout -b master >> "%LOG_FILE%" 2>&1
    git remote add origin https://github.com/jaajanjos/Datasciense.git >> "%LOG_FILE%" 2>&1
    git pull origin master >> "%LOG_FILE%" 2>&1
)

:: Executa os comandos padrão de envio
git add . >> "%LOG_FILE%" 2>&1
git commit -m "Atualizacao automatica via BAT" >> "%LOG_FILE%" 2>&1
git push origin master >> "%LOG_FILE%" 2>&1

echo ===================================================
echo   PROCESSO CONCLUIDO! FECHANDO EM 5 SEGUNDOS...
echo ===================================================
timeout /t 5