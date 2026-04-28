$ErrorActionPreference = "Stop"

$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $projectRoot

if (-not (Test-Path ".venv")) {
    python -m venv .venv
}

$python = Join-Path $projectRoot ".venv\Scripts\python.exe"
if (-not (Test-Path $python)) {
    throw "Python venv is missing at .venv"
}

& $python -m pip install --upgrade pip
& $python -m pip install -r requirements.txt

Push-Location (Join-Path $projectRoot "core")
& $python -m maturin develop --release
Pop-Location

Write-Host "Setup completed. Run .\\run.ps1"
