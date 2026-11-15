$ErrorActionPreference = 'Stop'
$project_dir = Join-Path $PSScriptRoot 'master_preview_20261109'
$source_path = Join-Path $project_dir 'exports/master_preview_20261112_181441_native_charts_tables.pptx'
$target_dir = Join-Path $project_dir 'native_validation_v2'
New-Item -ItemType Directory -Force $target_dir | Out-Null
$output_path = Join-Path $target_dir 'edited_copy.pptx'
if (Test-Path $output_path) { throw '已有测试副本，不覆盖。' }
$original_hash = (Get-FileHash $source_path).Hash
$app = New-Object -ComObject PowerPoint.Application
$deck = $null
function Find-Title($shapes) {
    foreach ($shape in $shapes) {
        if ($shape.Type -eq 6) {
            $found = Find-Title $shape.GroupItems
            if ($null -ne $found) { return $found }
        } elseif ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.TextRange.Text.Contains('变成能验收')) { return $shape }
    }
    return $null
}
try {
    $deck = $app.Presentations.Open($source_path,-1,0,0)
    for ($i=1; $i -le 3; $i++) { $deck.Slides.Item($i).Export((Join-Path $target_dir ('slide_{0:D2}.png' -f $i)),'PNG',1280,720) }
    $title = Find-Title $deck.Slides.Item(1).Shapes
    if ($null -eq $title) { throw '未找到可编辑标题。' }
    $title.TextFrame.TextRange.Text += '（回存验证）'
    $table = $null
    foreach ($shape in $deck.Slides.Item(3).Shapes) { if ($shape.HasTable -eq -1) { $table=$shape; break } }
    if ($null -eq $table) { throw '未找到原生表格。' }
    $table_name=$table.Name
    $table.Table.Cell(2,2).Shape.TextFrame.TextRange.Text='周（验证）'
    $deck.SaveAs($output_path,24)
    $deck.Close()
    $deck=$app.Presentations.Open($output_path,-1,0,0)
    $title=Find-Title $deck.Slides.Item(1).Shapes
    $result=@{version=$app.Version;slides=$deck.Slides.Count;title_persisted=$title.TextFrame.TextRange.Text.Contains('回存验证');table_persisted=($deck.Slides.Item(3).Shapes.Item($table_name).Table.Cell(2,2).Shape.TextFrame.TextRange.Text -eq '周（验证）');original_unchanged=((Get-FileHash $source_path).Hash -eq $original_hash);sha256=$original_hash}
    $result | ConvertTo-Json | Set-Content (Join-Path $target_dir 'result.json') -Encoding utf8
    $result | ConvertTo-Json
} finally {
    if ($null -ne $deck) { $deck.Close() }
    if ($app.Presentations.Count -eq 0) { $app.Quit() }
}

