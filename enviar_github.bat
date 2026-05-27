@echo off
echo ===================================================
echo   INICIANDO O ENVIO DOS ARQUIVOS PARA O GITHUB...
echo ===================================================

:: Abre o Git Bash e manda ele executar o script nativo .sh
"C:\Program Files\Git\git-bash.exe" --cd="D:\Github_Area" -c "./enviar.sh"

echo Processo concluido! Verifique o arquivo de log_envio_github.txt
pause