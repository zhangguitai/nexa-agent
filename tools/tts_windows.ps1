param(
  [Parameter(Mandatory = $true)][string]$TextFile,
  [Parameter(Mandatory = $true)][string]$OutputFile
)

$text = Get-Content -LiteralPath $TextFile -Raw -Encoding UTF8
$voice = New-Object -ComObject SAPI.SpVoice
$voices = $voice.GetVoices()
for ($index = 0; $index -lt $voices.Count; $index++) {
  $candidate = $voices.Item($index)
  if ($candidate.GetDescription() -match 'Huihui|Chinese') {
    $voice.Voice = $candidate
    break
  }
}

$voice.Rate = -1
$voice.Volume = 100

$stream = New-Object -ComObject SAPI.SpFileStream
$format = New-Object -ComObject SAPI.SpAudioFormat
$format.Type = 22
$stream.Format = $format
$stream.Open($OutputFile, 3, $false)
$voice.AudioOutputStream = $stream
$voice.Speak($text)
$stream.Close()
