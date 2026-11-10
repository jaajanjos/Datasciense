# Cria (ou recria) a tarefa do Agendador que roda atualizar_categorias_auto.py a cada 3 horas.
# Rodar pelo atalho 6_ATIVAR_ATUALIZACAO_AUTOMATICA.bat (na raiz da Gestao_Anuncios_Blog).
$nome = "Atualizar categorias blog comprenolink"
$script = Join-Path $PSScriptRoot "atualizar_categorias_auto.py"
$py = (Get-Command pythonw.exe -ErrorAction SilentlyContinue).Source
if (-not $py) { $py = Join-Path (Split-Path (Get-Command python.exe).Source) "pythonw.exe" }
$acao = New-ScheduledTaskAction -Execute $py -Argument "-X utf8 `"$script`"" -WorkingDirectory $PSScriptRoot
$gatilho = New-ScheduledTaskTrigger -Once -At (Get-Date).AddMinutes(1) -RepetitionInterval (New-TimeSpan -Hours 3)
$cfg = New-ScheduledTaskSettingsSet -StartWhenAvailable -ExecutionTimeLimit (New-TimeSpan -Minutes 15) -MultipleInstances IgnoreNew
Register-ScheduledTask -TaskName $nome -Action $acao -Trigger $gatilho -Settings $cfg -Force `
  -Description "Atualiza categorias, Black Friday/Natal, Escolha rapida, Inicio e menu do comprenolink.net quando o guia muda. Log: 2_DADOS\Blog_WordPress\atualizar_categorias.log" | Out-Null
Start-ScheduledTask -TaskName $nome
Write-Host "Tarefa '$nome' ativada: roda agora e depois a cada 3 horas."
Write-Host "Python: $py"
