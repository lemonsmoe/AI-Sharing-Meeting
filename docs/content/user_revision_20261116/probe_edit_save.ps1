$ErrorActionPreference='Stop'
$source=(Resolve-Path -LiteralPath 'slides/projects/user_revision_ppt169_20261116/exports/AI分享_28页顺序与幻觉修订版_20261116.pptx').Path
$probe=[IO.Path]::GetFullPath((Join-Path (Get-Location).Path 'slides/projects/user_revision_ppt169_20261116/validation/edit_save_probe.pptx'))
$before=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
Copy-Item -LiteralPath $source -Destination $probe
function Find-Texts($items) {
  foreach($s in $items) {
    if($s.Type -eq 6){Find-Texts $s.GroupItems}
    elseif($s.HasTextFrame -eq -1 -and $s.TextFrame.HasText -eq -1){$s}
  }
}
$app=New-Object -ComObject PowerPoint.Application
$deck=$app.Presentations.Open($probe,0,0,0)
$expected='这份 PPT，就是咱们用 AI 做出来的'
$changed='编辑验证：三页样稿'
try {
  $shape=Find-Texts $deck.Slides.Item(2).Shapes | Where-Object {$_.TextFrame.TextRange.Text -eq $expected} | Select-Object -First 1
  if(-not $shape){throw 'Native title not found'}
  $shape.TextFrame.TextRange.Text=$changed
  $deck.Save()
} finally {$deck.Close()}
$deck=$app.Presentations.Open($probe,-1,0,0)
try {
  $shape=Find-Texts $deck.Slides.Item(2).Shapes | Where-Object {$_.TextFrame.TextRange.Text -eq $changed} | Select-Object -First 1
  if(-not $shape){throw 'Edit did not persist'}
} finally {$deck.Close()}
$after=(Get-FileHash -LiteralPath $source -Algorithm SHA256).Hash
if($before -ne $after){throw 'Original unexpectedly changed'}
@{native_edit_save_reopen='passed';original_unchanged=$true;powerpoint_version=$app.Version;source_sha256=$after} | ConvertTo-Json | Set-Content -LiteralPath 'docs/content/user_revision_20261116/edit_verification.json' -Encoding utf8
Write-Output 'Native title edit / save / reopen passed; delivery file unchanged.'
