$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$target_dir = Join-Path $root 'slides/review_v3/excel_validation'
New-Item -ItemType Directory -Force -Path $target_dir | Out-Null
$source_path = Join-Path $root 'outputs/leadership_review_v3/materials/meeting_actions.xlsx'
$output_path = Join-Path $target_dir 'edited_copy.xlsx'
if (Test-Path -LiteralPath $output_path) { throw '已有测试副本，不能覆盖。' }
$source_hash = (Get-FileHash -LiteralPath $source_path).Hash
$app = $null
$book = $null
try {
    $app = New-Object -ComObject Excel.Application
    $app.DisplayAlerts = $false
    $app.EnableEvents = $false
    $app.AutomationSecurity = 3
    $book = $app.Workbooks.Open($source_path, 0, $true)
    $sheet = $book.Worksheets.Item(1)
    $deadline = $sheet.Range('D6').Text
    $demo_date = $sheet.Range('D12').Text
    $missing = [string]::IsNullOrEmpty($sheet.Range('C7').Text) -and [string]::IsNullOrEmpty($sheet.Range('D7').Text)
    if ($deadline -ne '2026-11-09 18:00' -or $demo_date -ne '2026-11-12') { throw '原生应用显示日期不符。' }
    $sheet.Range('G6').Value2 = '副本回存验证'
    $book.SaveAs($output_path, 51)
    $book.Close($false)
    $book = $null
    $book = $app.Workbooks.Open($output_path, 0, $true)
    $sheet = $book.Worksheets.Item(1)
    $result = @{
        application = 'Microsoft Excel'
        version = $app.Version
        deadline_display = $deadline
        demo_date_display = $demo_date
        date_values = @($sheet.Range('D6').Value2, $sheet.Range('D12').Value2)
        dates_persisted = ($sheet.Range('D6').Text -eq $deadline -and $sheet.Range('D12').Text -eq $demo_date)
        text_persisted = ($sheet.Range('G6').Text -eq '副本回存验证')
        missing_fields_preserved = $missing
        original_hash = $source_hash
        original_unchanged = ((Get-FileHash -LiteralPath $source_path).Hash -eq $source_hash)
        scope = '原生文本显示与副本保存重开；不等于WPS或现场设备检查'
    }
    $result | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $target_dir 'result.json') -Encoding utf8
    $result | ConvertTo-Json
} finally {
    if ($null -ne $book) { $book.Close($false) }
    if ($null -ne $app -and $app.Workbooks.Count -eq 0) { $app.Quit() }
}
