$ErrorActionPreference = 'Stop'
$root = (Get-Location).Path
$target_dir = Join-Path $root 'slides/review_v3/native_validation'
New-Item -ItemType Directory -Force -Path $target_dir | Out-Null
$source_path = Join-Path $root 'outputs/leadership_review_v3/leadership_review_v3.pptx'
$output_path = Join-Path $target_dir 'edited_copy.pptx'
if (Test-Path -LiteralPath $output_path) { throw '已有测试副本，不能覆盖。' }
$source_hash = (Get-FileHash -LiteralPath $source_path).Hash
$app = $null
$deck = $null
try {
    $app = New-Object -ComObject PowerPoint.Application
    $deck = $app.Presentations.Open($source_path, -1, 0, 0)
    for ($i=1; $i -le $deck.Slides.Count; $i++) {
        $deck.Slides.Item($i).Export((Join-Path $target_dir ('slide_{0:D2}.png' -f $i)), 'PNG', 1280, 720)
    }
    $title = $deck.Slides.Item(30).Shapes.Item(1)
    $title.TextFrame.TextRange.Text = '交流与问题（回存验证）'
    $table_shape = $null
    foreach ($shape in $deck.Slides.Item(8).Shapes) {
        if ($shape.HasTable -eq -1) { $table_shape = $shape; break }
    }
    if ($null -eq $table_shape) { throw '第8页没有原生表格。' }
    $table_name = $table_shape.Name
    $table_shape.Table.Cell(2,4).Shape.TextFrame.TextRange.Text = '6天（验证）'
    $deck.SaveAs($output_path,24)
    $deck.Close()
    $deck = $app.Presentations.Open($output_path,-1,0,0)
    $result = @{
        version=$app.Version
        slides=$deck.Slides.Count
        title_persisted=$deck.Slides.Item(30).Shapes.Item(1).TextFrame.TextRange.Text.Contains('回存验证')
        table_persisted=($deck.Slides.Item(8).Shapes.Item($table_name).Table.Cell(2,4).Shape.TextFrame.TextRange.Text -eq '6天（验证）')
        original_hash=$source_hash
        original_unchanged=((Get-FileHash -LiteralPath $source_path).Hash -eq $source_hash)
        chart_scope='V3没有原生图表；旧4页样例图表同步限制仍保留。'
    }
    $result | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $target_dir 'result.json') -Encoding utf8
    $result | ConvertTo-Json
} finally {
    if ($null -ne $deck) { $deck.Close() }
    if ($null -ne $app -and $app.Presentations.Count -eq 0) { $app.Quit() }
}

