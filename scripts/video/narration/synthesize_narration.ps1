param(
    [Parameter(Mandatory=$true)][string]$input_path,
    [Parameter(Mandatory=$true)][string]$output_dir,
    [string]$voice_name = 'Microsoft Huihui'
)

$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Runtime.WindowsRuntime
[Windows.Media.SpeechSynthesis.SpeechSynthesizer, Windows.Media, ContentType=WindowsRuntime] | Out-Null
[Windows.Media.SpeechSynthesis.SpeechSynthesisStream, Windows.Media, ContentType=WindowsRuntime] | Out-Null
$async_method = [System.WindowsRuntimeSystemExtensions].GetMethods() | Where-Object {
    $_.Name -eq 'AsTask' -and $_.IsGenericMethod -and $_.GetParameters().Count -eq 1 -and
    $_.GetParameters()[0].ParameterType.Name -eq 'IAsyncOperation`1'
} | Select-Object -First 1
$speech_method = $async_method.MakeGenericMethod([Windows.Media.SpeechSynthesis.SpeechSynthesisStream])
$voice = [Windows.Media.SpeechSynthesis.SpeechSynthesizer]::AllVoices |
    Where-Object { $_.DisplayName -eq $voice_name -and $_.Language -eq 'zh-CN' } |
    Select-Object -First 1
if (-not $voice) { throw 'Requested Chinese voice is not installed.' }
$synth = New-Object Windows.Media.SpeechSynthesis.SpeechSynthesizer
$synth.Voice = $voice
$items = Get-Content -LiteralPath $input_path -Raw -Encoding UTF8 | ConvertFrom-Json
New-Item -ItemType Directory -Path $output_dir -Force | Out-Null
$results = @()
try {
    foreach ($item in $items) {
        if ($item.id -notmatch '^[a-z0-9_]+$') { throw 'Invalid segment id.' }
        $wave_path = Join-Path $output_dir ($item.id + '.wav')
        if (Test-Path -LiteralPath $wave_path) { throw 'Output already exists.' }
        $started_at = [DateTime]::UtcNow.ToString('o')
        $task = $speech_method.Invoke($null, @($synth.SynthesizeTextToStreamAsync($item.text)))
        $task.Wait()
        $speech_stream = $task.Result
        $audio_stream = [System.IO.WindowsRuntimeStreamExtensions]::AsStreamForRead($speech_stream)
        $file_stream = [System.IO.File]::Create($wave_path)
        try { $audio_stream.CopyTo($file_stream) }
        finally { $file_stream.Dispose(); $audio_stream.Dispose(); $speech_stream.Dispose() }
        $results += [pscustomobject]@{
            id = $item.id
            voice_name = $voice.DisplayName
            language = $voice.Language
            started_at = $started_at
            ended_at = [DateTime]::UtcNow.ToString('o')
            output = $wave_path
        }
    }
}
finally { $synth.Dispose() }
$results | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath (Join-Path $output_dir 'synthesis_manifest.json') -Encoding UTF8
