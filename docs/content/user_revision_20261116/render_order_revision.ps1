$ErrorActionPreference='Stop'
$base=(Resolve-Path -LiteralPath 'slides/projects/user_revision_ppt169_20261116').Path
$path=Join-Path $base 'exports/AI分享_28页顺序与幻觉修订版_20261116.pptx'
$app=New-Object -ComObject PowerPoint.Application
$deck=$app.Presentations.Open($path,-1,0,0)
try {
  for($i=1;$i -le $deck.Slides.Count;$i++) {
    $out=Join-Path $base ('preview/revised_{0:D2}.png' -f $i)
    $deck.Slides.Item($i).Export($out,'PNG',1280,720)
  }
  Write-Output ('Rendered '+$deck.Slides.Count+' pages using PowerPoint '+$app.Version)
} finally { $deck.Close() }
