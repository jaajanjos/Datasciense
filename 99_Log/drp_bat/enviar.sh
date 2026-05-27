Bash
#!/bin/bash

# Força o script a ir para a pasta exata usando letras minúsculas (padrão do Git Bash)
cd /d/github_area

LOG_FILE="log_envio_github.txt"

echo "Instante do envio: $(date +'%d/%m/%Y as %H:%M:%S')" > "$LOG_FILE"
echo "---------------------------------------------------" >> "$LOG_FILE"

# Executa os comandos do Git e joga as respostas direto no log
{
    git add .
    echo "--- Arquivos preparados! ---"
    git commit -m "Atualizacao automatica via Script SH"
    echo "--- Commit realizado! ---"
    git push
} >> "$LOG_FILE" 2>&1