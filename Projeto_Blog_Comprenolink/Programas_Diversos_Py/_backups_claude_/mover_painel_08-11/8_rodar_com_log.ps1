# Roda um .bat mostrando tudo na tela E gravando o mesmo texto em um arquivo de log (UTF-8).
# Uso: powershell -NoProfile -ExecutionPolicy Bypass -File 8_rodar_com_log.ps1 "<arquivo.bat>" "<log.txt>"
# Chamado por Relatorios_Diarios_Anuncios\ATUALIZAR_PAINEL.bat (grava log_painel.txt na mesma pasta).
param([string]$Bat, [string]$Log)
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
$utf8 = New-Object System.Text.UTF8Encoding($true)
$sw = New-Object System.IO.StreamWriter($Log, $false, $utf8)
$sw.AutoFlush = $true
$inicio = Get-Date
$sw.WriteLine("LOG DO PAINEL - inicio " + $inicio.ToString("dd/MM/yyyy HH:mm:ss"))
$sw.WriteLine("Programa: " + $Bat)
$sw.WriteLine("=" * 70)
$env:PAINEL_LOG_ATIVO = "1"
try {
    & cmd.exe /c "`"$Bat`"" 2>&1 | ForEach-Object {
        $linha = "$_"
        Write-Host $linha
        $sw.WriteLine($linha)
    }
    $codigo = $LASTEXITCODE
} catch {
    $codigo = 1
    $sw.WriteLine("ERRO NO EXECUTOR: " + $_.Exception.Message)
    Write-Host ("ERRO NO EXECUTOR: " + $_.Exception.Message)
}
$fim = Get-Date
$sw.WriteLine("=" * 70)
$sw.WriteLine("Fim " + $fim.ToString("dd/MM/yyyy HH:mm:ss") + " | duracao " + [int]($fim - $inicio).TotalSeconds + " s | codigo de saida " + $codigo)
$sw.Close()
Write-Host ""
Write-Host ("Log gravado em: " + $Log)
exit $codigo
