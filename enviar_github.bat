@echo off
echo ===================================================
echo   INICIANDO O ENVIO DOS ARQUIVOS PARA O GITHUB...
echo ===================================================

:: Define o arquivo de log
set LOG_FILE=D:\Github_Area\log_envio_github.txt

:: Registra a data e hora iniciais no log
echo Instante do envio: %date% as %time% > "%LOG_FILE%"
echo --------------------------------------------------- >> "%LOG_FILE%"

:: EXECUTÁVEL CORRIGIDO: Força o Windows a capturar tanto o canal 1 (texto) quanto o canal 2 (status/erros) do Git Bash
"C:\Program Files\Git\git-bash.exe" --cd="D:\Github_Area" -c "git add . && git commit -m 'Atualizacao automatica via BAT' && git push" >> "%LOG_FILE%" 2>&1

echo ===================================================
echo   PROCESSO CONCLUIDO! FECHANDO EM 5 SEGUNDOS...
echo ===================================================
timeout /t 5