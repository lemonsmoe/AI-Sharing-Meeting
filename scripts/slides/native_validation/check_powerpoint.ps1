param([switch]$refresh_series)
$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$target_dir = Join-Path $root $(if ($refresh_series) {'slides/native_validation/explicit_refresh'} else {'slides/native_validation'})
New-Item -ItemType Directory -Force -Path $target_dir | Out-Null
$source_path = Join-Path $root 'slides/experiments/output/weekly_report_sample_v1.pptx'
$output_path = Join-Path $target_dir 'weekly_report_edited.pptx'
if (Test-Path -LiteralPath $output_path) { throw '验证输出已存在，请保留旧记录后另选路径。' }
$source_hash = (Get-FileHash -LiteralPath $source_path).Hash
$app = $null
$deck = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $version = $app.Version
    $deck = $app.Presentations.Open($source_path, -1, 0, 0)
    $text_shape = $null
    foreach ($shape in $deck.Slides.Item(2).Shapes) {
        if ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) { $text_shape = $shape; break }
    }
    if ($null -eq $text_shape) { throw '第2页未找到文本框。' }
    $original_text = $text_shape.TextFrame.TextRange.Text
    $text_shape_name = $text_shape.Name
    $text_shape.TextFrame.TextRange.Text = $original_text + '（原生编辑验证）'
    $chart = $null
    foreach ($shape in $deck.Slides.Item(3).Shapes) {
        if ($shape.HasChart -eq -1) { $chart = $shape.Chart; break }
    }
    if ($null -eq $chart) { throw '第3页未找到原生图表。' }
    $old_values = @($chart.SeriesCollection(1).Values)
    $chart.ChartData.Activate()
    $workbook = $chart.ChartData.Workbook
    $sheet = $workbook.Worksheets.Item(1)
    $sheet.Cells.Item(2,2).Value2 = 7.0
    if ($refresh_series) { $chart.SeriesCollection(1).Values = @([double]7, [double]6) }
    $workbook.Close($true)
    $chart.Refresh()
    $deck.SaveAs($output_path, 24)
    $deck.Close()
    $deck = $app.Presentations.Open($output_path, -1, 0, 0)
    $new_text = $deck.Slides.Item(2).Shapes.Item($text_shape_name).TextFrame.TextRange.Text
    $new_values = $null
    foreach ($shape in $deck.Slides.Item(3).Shapes) {
        if ($shape.HasChart -eq -1) { $new_values = @($shape.Chart.SeriesCollection(1).Values) }
    }
    for ($i=1; $i -le $deck.Slides.Count; $i++) {
        $deck.Slides.Item($i).Export((Join-Path $target_dir ('slide_{0:D2}.png' -f $i)), 'PNG', 1280, 720)
    }
    $result = @{version=$version; slides=$deck.Slides.Count; original_values=$old_values; reopened_values=$new_values; text_persisted=$new_text.Contains('原生编辑验证'); source_unchanged=((Get-FileHash -LiteralPath $source_path).Hash -eq $source_hash)}
    $result | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $target_dir 'result.json') -Encoding utf8
    $result | ConvertTo-Json -Depth 5
} finally {
    if ($null -ne $deck) { $deck.Close() }
    if ($null -ne $app -and $app.Presentations.Count -eq 0) { $app.Quit() }
}
