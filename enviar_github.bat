@echo off
echo ===================================================
echo   INICIANDO O ENVIO DOS ARQUIVOS PARA O GITHUB...
echo ===================================================

:: Define o arquivo de log
set LOG_FILE=D:\Github_Area\log_envio_github.txt

:: Registra a data e hora iniciais no log
echo Instante do envio: %date% as %time% > "%LOG_FILE%"
echo --------------------------------------------------- >> "%LOG_FILE%"

:: Roda os comandos e joga a resposta do Git Bash para dentro do log correto
"C:\Program Files\Git\git-bash.exe" --cd="D:\Github_Area" -c "git add . && git commit -m 'Atualizacao automatica via BAT' && git push" >> "%LOG_FILE%" 2>&1

echo ===================================================
echo   PROCESSO CONCLUIDO! FECHANDO EM 5 SEGUNDOS...
echo ===================================================
timeout /t 5