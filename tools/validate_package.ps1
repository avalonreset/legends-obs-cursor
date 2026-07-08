$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$required = @(
    "README.md",
    "LICENSE",
    "CREDITS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "legends_cursor_filter.lua",
    "legends_cursor_filter.effect",
    "install_into_obs.ps1",
    "install_into_obs.cmd",
    "install_and_launch_obs.cmd",
    "assets/banner.webp",
    "assets/screenshots/momentum-ticks.png",
    "assets/screenshots/right-click-diamond.png"
)

foreach ($path in $required) {
    if (-not (Test-Path -LiteralPath $path)) {
        throw "Missing required file: $path"
    }
}

$lua = Get-Content -LiteralPath "legends_cursor_filter.lua" -Raw
if ($lua -notmatch 'filter_def\.id\s*=\s*"legends_cursor_filter"') {
    throw "Lua filter id must remain legends_cursor_filter."
}
if ($lua -notmatch 'return "Legends Cursor Filter"') {
    throw "Lua filter display name must remain Legends Cursor Filter."
}
if ($lua -notmatch 'rotating_ticks') {
    throw "Original rotating tick shader path is missing."
}
if ($lua -notmatch 'diamond_click') {
    throw "Original right-click diamond shader path is missing."
}
if ($lua -notmatch 'enable_floaty_follow') {
    throw "Floaty follow setting is missing."
}

$installer = Get-Content -LiteralPath "install_into_obs.ps1" -Raw
if ($installer -match 'legends_cursor_filter_momentum_v1') {
    throw "Installer must not install the replacement momentum id."
}
if ($installer -match 'Legends Momentum Cursor Filter') {
    throw "Installer must preserve the original filter display name."
}
if ($installer -notmatch 'Copy-Item -LiteralPath \$ScenePath -Destination \$BackupPath') {
    throw "Installer must backup the OBS scene collection before editing."
}

$trackedLeakPatterns = @(
    ('C:' + '\\Users\\rccol'),
    ('E:' + '\\legends-obs-cursor'),
    ('\bAvalon Reset ' + 'Pro\b'),
    'gho_[A-Za-z0-9_]+',
    'KIE_API_KEY\s*='
)

$scanFiles = Get-ChildItem -Recurse -File |
    Where-Object {
        $_.FullName -notmatch '\\.git\\' -and
        $_.FullName -notmatch '\\assets\\' -and
        $_.Extension -in ".md", ".lua", ".ps1", ".cmd", ".yml", ".yaml", ".txt"
    }

foreach ($file in $scanFiles) {
    $text = Get-Content -LiteralPath $file.FullName -Raw
    foreach ($pattern in $trackedLeakPatterns) {
        if ($text -match $pattern) {
            throw "Potential private path or secret pattern '$pattern' found in $($file.FullName)."
        }
    }
}

Write-Host "Package validation passed."
