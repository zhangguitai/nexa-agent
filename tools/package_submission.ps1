$ErrorActionPreference = "Stop"

$workspace = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$destination = Join-Path $workspace "NEXA-Agent-Workspace-传智杯提交包.zip"

if (Test-Path -LiteralPath $destination) {
  Remove-Item -LiteralPath $destination -Force
}

Get-ChildItem -Path $workspace -Directory -Recurse -Filter "__pycache__" |
  Remove-Item -Recurse -Force

$items = @(
  "index.html",
  "package.json",
  "server.mjs",
  "README.md",
  "CONTRIBUTING.md",
  "requirements-dev.txt",
  "Dockerfile",
  ".editorconfig",
  ".dockerignore",
  ".env.example",
  ".gitignore",
  "assets",
  "docs",
  "output",
  "screenshots",
  "tests",
  "tools",
  ".github"
) | ForEach-Object { Join-Path $workspace $_ }

Compress-Archive -Path $items -DestinationPath $destination -CompressionLevel Optimal

$zip = Get-Item -LiteralPath $destination
Write-Host "Submission package created:"
Write-Host $zip.FullName
Write-Host ("Size: {0:N2} MB" -f ($zip.Length / 1MB))
