
param(
    [Parameter(Mandatory=$false)]
    [string]$BaseDir = "C:\Users\User\Desktop\salesbot_final\api\modules",
    [Parameter(Mandatory=$false)]
    [string]$ZipsDir = ".",
    [switch]$DryRun
)

$ModuleName = "upsell"
$Version    = "v1"

$Patterns = @(
    "^salesbot[_-]upsell.*\.zip$",
    "^salesbot[_-]PART[_-]upsell.*\.zip$",
    "^upsell[_-].*\.zip$"
)

$StagingDir = Join-Path -Path $env:TEMP -ChildPath ("upsell_stage_" + [guid]::NewGuid().ToString("N"))
New-Item -ItemType Directory -Path $StagingDir | Out-Null

$LogDir = Join-Path -Path $env:TEMP -ChildPath "upsell_assembly_logs"
New-Item -ItemType Directory -Path $LogDir -Force | Out-Null
$Log = Join-Path -Path $LogDir -ChildPath ("assembly_" + (Get-Date -Format "yyyyMMdd_HHmmss") + ".log")

function Write-Log($msg) {
    $ts = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $line = "[$ts] $msg"
    $line | Tee-Object -FilePath $Log -Append
}

Write-Log "=== UPSSELL Auto-Assembly started ==="
Write-Log "BaseDir = $BaseDir"
Write-Log "ZipsDir = $ZipsDir"
Write-Log "DryRun  = $DryRun"

$TargetRoot = Join-Path -Path $BaseDir -ChildPath (Join-Path $ModuleName $Version)
$TargetModulesDir = Join-Path -Path $BaseDir -ChildPath $ModuleName
if (-not (Test-Path $TargetModulesDir)) {
    if ($DryRun) { Write-Log "Would create: $TargetModulesDir" } else { New-Item -ItemType Directory -Path $TargetModulesDir -Force | Out-Null }
}
if (-not (Test-Path $TargetRoot)) {
    if ($DryRun) { Write-Log "Would create: $TargetRoot" } else { New-Item -ItemType Directory -Path $TargetRoot -Force | Out-Null }
}

function Matches-AnyPattern($name, $patterns) {
    foreach ($p in $patterns) {
        if ($name -imatch $p) { return $true }
    }
    return $false
}

$zipFiles = Get-ChildItem -Path $ZipsDir -Filter *.zip -File -Recurse
$zipFiles = $zipFiles | Where-Object { Matches-AnyPattern $_.Name $Patterns }

if ($zipFiles.Count -eq 0) {
    Write-Log "No matching ZIP files found in $ZipsDir"
    Write-Host "No matching ZIP files found. Make sure your upsell *.zip parts are in $ZipsDir"
    exit 1
}

Write-Log ("Found {0} ZIP(s):" -f $zipFiles.Count)
$zipFiles | ForEach-Object { Write-Log (" - " + $_.FullName) }

$ExpandedDirs = @()
foreach ($zip in $zipFiles) {
    $dest = Join-Path -Path $StagingDir -ChildPath ($zip.BaseName)
    Write-Log "Extracting $($zip.Name) -> $dest"
    if (-not $DryRun) {
        Expand-Archive -Path $zip.FullName -DestinationPath $dest -Force
    }
    $ExpandedDirs += ,$dest
}

function Merge-Tree($src, $dst) {
    if ($DryRun) {
        Write-Log "Would copy: $src -> $dst"
    } else {
        New-Item -ItemType Directory -Path $dst -Force | Out-Null
        Copy-Item -Path (Join-Path $src "*") -Destination $dst -Recurse -Force -ErrorAction Stop
    }
}

foreach ($dir in $ExpandedDirs) {
    $modulesUpsell = Join-Path -Path $dir -ChildPath "modules\upsell"
    if (Test-Path $modulesUpsell) {
        Write-Log "Detected modules\upsell inside: $dir"
        Merge-Tree -src $modulesUpsell -dst (Join-Path $BaseDir "upsell")
        continue
    }

    $modulesRoot = Join-Path -Path $dir -ChildPath "modules"
    if (Test-Path $modulesRoot) {
        Write-Log "Detected modules root in: $dir"
        Merge-Tree -src $modulesRoot -dst $BaseDir
        continue
    }

    Write-Log "Fallback copy into $TargetRoot for: $dir"
    Merge-Tree -src $dir -dst $TargetRoot
}

$currentLink = Join-Path -Path $TargetModulesDir -ChildPath "current"
try {
    if (Test-Path $currentLink) {
        $attributes = (Get-Item $currentLink).Attributes
        if ($attributes -band [System.IO.FileAttributes]::ReparsePoint) {
            if ($DryRun) { Write-Log "Would remove existing symlink: $currentLink" } else { Remove-Item $currentLink -Force }
        } else {
            if ($DryRun) { Write-Log "Would remove existing folder: $currentLink" } else { Remove-Item $currentLink -Recurse -Force }
        }
    }
    if ($DryRun) {
        Write-Log "Would create symlink: $currentLink -> $TargetRoot"
    } else {
        New-Item -ItemType SymbolicLink -Path $currentLink -Target $TargetRoot | Out-Null
        Write-Log "Symlink created: current -> $TargetRoot"
    }
} catch {
    Write-Log "Symlink creation failed (non-critical): $($_.Exception.Message)"
}

Write-Log "=== UPSSELL Auto-Assembly complete ==="
Write-Host "Done. Log: $Log"
