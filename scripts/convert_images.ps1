# PowerShell script to convert images to WebP and create responsive sizes
# Requires ImageMagick (magick) or Google cwebp installed and in PATH.

Param(
    [string]$SrcDir = "assets/img",
    [string]$OutDir = "assets/img/webp",
    [int[]]$Widths = @(400,800,1200),
    [int]$Quality = 80
)

Set-StrictMode -Version Latest

if (-not (Test-Path $SrcDir)) {
    Write-Error "Source directory '$SrcDir' not found. Run this script from the site root."
    exit 1
}

New-Item -ItemType Directory -Force -Path $OutDir | Out-Null

function Has-Command($name) {
    $null -ne (Get-Command $name -ErrorAction SilentlyContinue)
}

$useMagick = Has-Command magick
$useCwebp = Has-Command cwebp
if (-not ($useMagick -or $useCwebp)) {
    Write-Error "Neither 'magick' (ImageMagick) nor 'cwebp' found in PATH. Please install one and re-run."
    exit 2
}

$exts = @('*.jpg','*.jpeg','*.png')
$files = @()
foreach ($e in $exts) { $files += Get-ChildItem -Path $SrcDir -Recurse -Include $e -File }

foreach ($f in $files) {
    $rel = $f.FullName.Substring((Get-Location).Path.Length + 1).Replace('\','/')
    $name = [IO.Path]::GetFileNameWithoutExtension($f.Name)
    $dir = Join-Path $OutDir ($f.DirectoryName.Substring((Get-Location).Path.Length + 1).Replace('\','/'))
    if (-not (Test-Path $dir)) { New-Item -ItemType Directory -Force -Path $dir | Out-Null }

    foreach ($w in $Widths) {
        $outName = "${name}-${w}.webp"
        $outPath = Join-Path $dir $outName
        if ($useMagick) {
            magick "$($f.FullName)" -strip -quality $Quality -resize "${w}>" "$outPath"
        } else {
            # convert to temporary PNG/JPEG with width then run cwebp
            $tmp = [IO.Path]::GetTempFileName() + ".jpg"
            magick "$($f.FullName)" -resize "${w}>" "$tmp" 2>$null
            cwebp -q $Quality "$tmp" -o "$outPath" 2>$null
            Remove-Item $tmp -ErrorAction SilentlyContinue
        }
        Write-Host "Created $outPath"
    }

    # also create a full-size .webp
    $outFull = Join-Path $dir ("${name}.webp")
    if ($useMagick) { magick "$($f.FullName)" -strip -quality $Quality "$outFull" }
    else { cwebp -q $Quality "$($f.FullName)" -o "$outFull" }
    Write-Host "Created $outFull"
}

Write-Host "Conversion complete. WebP files output to: $OutDir"; exit 0
