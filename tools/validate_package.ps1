$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
Set-Location $root

$required = @(
    "README.md",
    "LICENSE",
    "NOTICE",
    "CREDITS.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    ".github/release.yml",
    "legends_cursor_filter.lua",
    "legends_cursor_filter.effect",
    "install_into_obs.ps1",
    "install_into_obs.cmd",
    "install_and_launch_obs.cmd",
    "assets/banner.webp",
    "assets/demo/legends-cursor-showcase.webp",
    "assets/demo/legends-cursor-demo.webp",
    "assets/demo/legends-cursor-demo.gif",
    "assets/demo/legends-cursor-showcase-4k60.webm",
    "assets/demo/legends-cursor-showcase-4k60.mp4",
    "assets/screenshots/momentum-ticks.png",
    "assets/screenshots/left-click-ripple.png",
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
$obsGuardIndex = $installer.IndexOf('$runningObs = Get-Process -Name "obs64", "obs32"')
$firstCopyIndex = $installer.IndexOf('Copy-Item -LiteralPath $SourceLua')
if ($obsGuardIndex -lt 0 -or $firstCopyIndex -lt 0 -or $obsGuardIndex -gt $firstCopyIndex) {
    throw "Installer must check whether OBS is running before copying script files."
}
if ($installer -notmatch '\$runningObs -and -not \$Force -and -not \$CopyOnly') {
    throw "Installer OBS-running guard must protect normal installs while allowing explicit CopyOnly refreshes."
}

$workflow = Get-Content -LiteralPath ".github/workflows/validate.yml" -Raw
if ($workflow -notmatch '(?m)^permissions:\s*\r?\n\s+contents:\s+read') {
    throw "GitHub Actions workflow must declare least-privilege contents: read permissions."
}
if ($workflow -match 'actions/checkout@v[0-9]+') {
    throw "GitHub Actions checkout must be pinned to a commit SHA, not a mutable version tag."
}
if ($workflow -notmatch 'actions/checkout@[0-9a-f]{40}') {
    throw "GitHub Actions checkout must use a 40-character commit SHA."
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
