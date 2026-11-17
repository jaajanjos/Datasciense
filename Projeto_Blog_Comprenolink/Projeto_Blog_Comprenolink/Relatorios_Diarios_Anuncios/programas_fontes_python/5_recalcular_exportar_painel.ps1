# Abre o painel no Excel (invisível), recalcula, salva e exporta a aba Painel em PDF.
# Uso: powershell -ExecutionPolicy Bypass -File 5_recalcular_exportar_painel.ps1 "<xlsx>" "<pdf>"
param([string]$Xlsx, [string]$Pdf)
$ErrorActionPreference = "Stop"
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$excel.DisplayAlerts = $false
try {
    $wb = $excel.Workbooks.Open($Xlsx)
    $excel.CalculateFull()
    $erros = 0
    foreach ($ws in $wb.Worksheets) {
        $used = $ws.UsedRange
        foreach ($c in $used.Cells) {
            if ($c.HasFormula -and ($c.Text -like "#*")) { $erros++; Write-Host ("  ! erro em " + $ws.Name + "!" + $c.Address(0,0) + " = " + $c.Text) }
        }
    }
    $wb.Save()
    if ($Pdf) {
        $wb.Worksheets.Item("Painel").ExportAsFixedFormat(0, $Pdf)
        Write-Host "PDF do painel: $Pdf"
    }
    $wb.Close($false)
    Write-Host "Recalculo concluido. Formulas com erro: $erros"
    if ($erros -gt 0) { exit 3 }
} finally {
    $excel.Quit()
    [System.Runtime.Interopservices.Marshal]::ReleaseComObject($excel) | Out-Null
}
