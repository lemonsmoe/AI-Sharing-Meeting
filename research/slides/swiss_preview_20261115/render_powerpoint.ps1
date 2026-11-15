param(
    [string]$Source,
    [string]$Out,
    [string]$Prefix = 'slide',
    [int]$Width = 1280,
    [string]$EditCopy
)
$ErrorActionPreference = 'Stop'
$sourcePath = (Resolve-Path -LiteralPath $Source).Path
$outPath = [IO.Path]::GetFullPath((Join-Path (Get-Location).Path $Out))
New-Item -ItemType Directory -Force -Path $outPath | Out-Null
$app = New-Object -ComObject PowerPoint.Application
$deck = $app.Presentations.Open($sourcePath, -1, 0, 0)
try {
    $height = [Math]::Round($Width * $deck.PageSetup.SlideHeight / $deck.PageSetup.SlideWidth)
    foreach ($slide in $deck.Slides) {
        $name = '{0}_{1:00}.png' -f $Prefix, $slide.SlideIndex
        $slide.Export((Join-Path $outPath $name), 'PNG', $Width, $height)
    }
    Write-Output ("PowerPoint {0}, {1} slides, {2}x{3}" -f $app.Version,$deck.Slides.Count,$Width,$height)
} finally {
    $deck.Close()
}

if ($EditCopy) {
    function Get-SlideTextBoxes($shapes) {
        foreach ($shape in $shapes) {
            if ($shape.Type -eq 6) {
                Get-SlideTextBoxes $shape.GroupItems
            } elseif ($shape.HasTextFrame -eq -1 -and $shape.TextFrame.HasText -eq -1) {
                $shape
            }
        }
    }

    $copyPath = [IO.Path]::GetFullPath((Join-Path (Get-Location).Path $EditCopy))
    Copy-Item -LiteralPath $sourcePath -Destination $copyPath
    $deck = $app.Presentations.Open($copyPath, 0, 0, 0)
    $originalText = '把「做个 PPT」说具体'
    $newText = '把 PPT 的需求说具体'
    try {
        $title = Get-SlideTextBoxes $deck.Slides.Item(2).Shapes |
            Where-Object { $_.TextFrame.TextRange.Text -eq $originalText } |
            Select-Object -First 1
        if (-not $title) { throw 'Editable slide 2 title was not found' }
        $titleRange = $title.TextFrame.TextRange
        $latinFont = $titleRange.Characters(7, 3).Font.NameAscii
        $eastAsianFont = $titleRange.Characters(1, 1).Font.NameFarEast
        Write-Output "PowerPoint title font ASCII=$latinFont FarEast=$eastAsianFont size=$($titleRange.Font.Size)"
        $titleRange.Text = $newText
        $deck.Save()
    } finally {
        $deck.Close()
    }
    $deck = $app.Presentations.Open($copyPath, -1, 0, 0)
    try {
        $savedTitle = Get-SlideTextBoxes $deck.Slides.Item(2).Shapes |
            Where-Object { $_.TextFrame.TextRange.Text -eq $newText } |
            Select-Object -First 1
        if (-not $savedTitle) { throw 'Edited slide 2 title did not persist' }
        Write-Output 'Native title edit, save and reopen passed'
    } finally {
        $deck.Close()
    }
}
