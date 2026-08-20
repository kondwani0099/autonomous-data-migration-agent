# Uniplexity Migration Agent — Windows PowerShell Installer Script
$ErrorActionPreference = "Stop"

$AfacRef = "v1.0.0"

Write-Host "=========================================="
Write-Host "Installing Uniplexity Migration Agent ($AfacRef)"
Write-Host "=========================================="

Write-Host "[1/3] Setting up Python backend environment..."
if (Test-Path "backend") {
    Set-Location backend
    python -m venv venv
    .\venv\Scripts\Activate.ps1
    pip install --upgrade pip
    pip install -r requirements.txt
    Set-Location ..
}

Write-Host "[2/3] Setting up Node.js frontend environment..."
if (Test-Path "frontend") {
    Set-Location frontend
    npm install
    Set-Location ..
}

Write-Host "[3/3] Running workspace validation..."
python scripts/validate.py

Write-Host "Installation complete!"
