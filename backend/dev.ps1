<#
Start the development server bound to 0.0.0.0 so the site is reachable on LAN.
This script expects the virtualenv to exist at `backend/.venv`.

It uses Django's autoreloader. Run from the project root (joylandschools).
#>
param(
    [string]$Host = '0.0.0.0',
    [int]$Port = 8000
)

Push-Location $PSScriptRoot
if (Test-Path -Path "$PSScriptRoot\.venv\Scripts\Activate.ps1") {
    & "$PSScriptRoot\.venv\Scripts\Activate.ps1"
} elseif (Test-Path -Path "..\.venv\Scripts\Activate.ps1") {
    & "..\.venv\Scripts\Activate.ps1"
}

python manage.py runserver $Host`:$Port
Pop-Location
