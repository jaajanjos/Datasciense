@echo off
echo ===================================================
echo   INICIANDO O ENVIO DOS ARQUIVOS PARA O GITHUB...
echo ===================================================

:: Define o arquivo de log
set LOG_FILE=D:\Github_Area\log_envio_github.txt

:: Registra a data e hora no log usando o prompt do Windows
echo Instante do envio: %date% as %time% > "%LOG_FILE%"
echo --------------------------------------------------- >> "%LOG_FILE%"

:: Abre o Git Bash na pasta certa, executa os comandos em linha e joga o resultado no log
"C:\Program Files\Git\git-bash.exe" --cd="D:\Github_Area" -c "git add . && git commit -m 'Atualizacao automatica via BAT' && git push" >> "%LOG_FILE%" 2>&1

echo ===================================================
echo   PROCESSO CONCLUIDO! FECHANDO EM 5 SEGUNDOS...
echo ===================================================
timeout /t 5