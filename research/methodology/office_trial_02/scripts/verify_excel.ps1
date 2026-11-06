$ErrorActionPreference = 'Stop'
$trialRoot = Split-Path $PSScriptRoot -Parent
$excelApp = $null
$workbook = $null
$checkResult = [ordered]@{ started_utc = [DateTimeOffset]::UtcNow.ToString('o'); application = 'Microsoft Excel'; checks = @(); error = $null }
try {
    $excelApp = New-Object -ComObject Excel.Application
    $excelApp.Visible = $false
    $excelApp.DisplayAlerts = $false
    $checkResult.version = $excelApp.Version
    $workbook = $excelApp.Workbooks.Open((Join-Path $trialRoot 'first_output/meeting_follow_up.xlsx'), 0, $true)
    $checkResult.first_opened = $true
    $actions = $workbook.Worksheets.Item('行动清单')
    $records = $workbook.Worksheets.Item('决定与未决事项')
    foreach ($cellAddress in @('D6', 'D7', 'D8')) {
        $cell = $actions.Range($cellAddress)
        $checkResult.checks += @{ sheet = $actions.Name; cell = $cellAddress; value = $cell.Value2; display = $cell.Text; type = $cell.Value2.GetType().Name }
    }
    foreach ($cellAddress in @('B6', 'B9', 'D9', 'D10', 'D11', 'D12')) {
        $checkResult.checks += @{ sheet = $records.Name; cell = $cellAddress; value = $records.Range($cellAddress).Value2; is_empty = $null -eq $records.Range($cellAddress).Value2 }
    }
    $actions.Range('E6').Value2 = '回存验证临时值'
    $qaPath = Join-Path $trialRoot 'qa/excel_roundtrip.xlsx'
    $workbook.SaveAs($qaPath, 51)
    $workbook.Close($false)
    $workbook = $excelApp.Workbooks.Open($qaPath, 0, $false)
    $checkResult.edited_value_reopened = $workbook.Worksheets.Item('行动清单').Range('E6').Value2
    $workbook.Worksheets.Item('行动清单').Range('E6').Value2 = '待交付'
    $workbook.Save()
    $workbook.Close($false)
    $workbook = $null
    $checkResult.roundtrip_copy_restored = $true
} catch {
    $checkResult.error = $_.Exception.Message
} finally {
    if ($null -ne $workbook) { $workbook.Close($false) }
    if ($null -ne $excelApp) { $excelApp.Quit(); [Runtime.InteropServices.Marshal]::ReleaseComObject($excelApp) | Out-Null }
    $checkResult.finished_utc = [DateTimeOffset]::UtcNow.ToString('o')
    $checkResult | ConvertTo-Json -Depth 6 | Set-Content -Encoding utf8 (Join-Path $trialRoot 'qa/excel_roundtrip_report.json')
    $checkResult | ConvertTo-Json -Depth 6
}
