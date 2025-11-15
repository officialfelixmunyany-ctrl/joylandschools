# Safe sequential mover for announcement-related templates
# Usage: Open PowerShell in the backend directory and run:
#   .\scripts\move_templates.ps1

$ErrorActionPreference = 'Stop'
$ts = Get-Date -Format "yyyyMMdd_HHmmss"
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Definition
$backendRoot = Resolve-Path (Join-Path $scriptDir "..")
$backendRoot = $backendRoot.Path

$backupDir = Join-Path $backendRoot ".refactor_backups\templates_$ts"
New-Item -Path $backupDir -ItemType Directory -Force | Out-Null

$srcIncludes = Join-Path $backendRoot "templates\includes"
$dstCoreIncludes = Join-Path $backendRoot "templates\core\includes"
New-Item -Path $dstCoreIncludes -ItemType Directory -Force | Out-Null

$files = @(
    'announcements.html',
    'announcements_list.html',
    'announcement_form.html',
    'announcement_confirm_delete.html',
    'events_preview.html'
)

Write-Output "Backup directory: $backupDir"

foreach ($f in $files) {
    $s = Join-Path $srcIncludes $f
    if (Test-Path $s) {
        try {
            $b = Join-Path $backupDir $f
            Copy-Item -Path $s -Destination $b -Force
            Move-Item -Path $s -Destination $dstCoreIncludes -Force
            Write-Output "Moved: $f -> $dstCoreIncludes"
        } catch {
            Write-Error "Failed to move $f : $_"
        }
    } else {
        Write-Output "Not found (skipping): $s"
    }
}

# Move the archive template to templates/core
$archiveSrc = Join-Path $backendRoot "templates\announcements_archive.html"
$archiveDstDir = Join-Path $backendRoot "templates\core"
New-Item -Path $archiveDstDir -ItemType Directory -Force | Out-Null
if (Test-Path $archiveSrc) {
    try {
        Copy-Item -Path $archiveSrc -Destination (Join-Path $backupDir "announcements_archive.html") -Force
        Move-Item -Path $archiveSrc -Destination $archiveDstDir -Force
        Write-Output "Moved: announcements_archive.html -> $archiveDstDir"
    } catch {
        Write-Error "Failed to move announcements_archive.html : $_"
    }
} else {
    Write-Output "Not found (skipping): $archiveSrc"
}

Write-Output "Done. Check $backupDir for backups and verify templates/core/includes/ contains the moved files."