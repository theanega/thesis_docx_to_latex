# Pipeline automática para Windows PowerShell
# Convierte tesis de Word a LaTeX y genera los 4 PDFs

param(
    [switch]$SkipConversion,
    [switch]$SkipSplit,
    [string]$Version = "all"
)

$ErrorActionPreference = "Stop"

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "PIPELINE AUTOMÁTICA: Tesis Word → LaTeX → PDF" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan

# Verificar que Pandoc está instalado
if (-not $SkipConversion) {
    try {
        $null = Get-Command pandoc -ErrorAction Stop
    } catch {
        Write-Host "[ERROR] Pandoc no está instalado o no está en el PATH" -ForegroundColor Red
        Write-Host "Instala Pandoc desde: https://pandoc.org/installing.html" -ForegroundColor Yellow
        exit 1
    }
}

# Verificar que XeLaTeX está instalado
try {
    $null = Get-Command xelatex -ErrorAction Stop
} catch {
    Write-Host "[ERROR] XeLaTeX no está instalado o no está en el PATH" -ForegroundColor Red
    Write-Host "Instala MiKTeX o TeX Live desde sus sitios oficiales" -ForegroundColor Yellow
    exit 1
}

# Fase 1: Conversión Word → LaTeX
if (-not $SkipConversion) {
    Write-Host "`n============================================================" -ForegroundColor Green
    Write-Host "FASE 1: Conversión Word → LaTeX" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    
    if (-not (Test-Path "input\thesis.docx")) {
        Write-Host "[ERROR] No se encuentra input\thesis.docx" -ForegroundColor Red
        exit 1
    }
    
    if (-not (Test-Path "input\annex_thesis.docx")) {
        Write-Host "[ERROR] No se encuentra input\annex_thesis.docx" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Convirtiendo thesis.docx..." -ForegroundColor Yellow
    pandoc input\thesis.docx `
        --standalone `
        --to=latex `
        --top-level-division=chapter `
        --extract-media=source\figures\thesis `
        --output=source\thesis_full.tex
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Falló la conversión de thesis.docx" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Convirtiendo annex_thesis.docx..." -ForegroundColor Yellow
    pandoc input\annex_thesis.docx `
        --standalone `
        --to=latex `
        --top-level-division=chapter `
        --extract-media=source\figures\annex `
        --output=source\annex_full.tex
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Falló la conversión de annex_thesis.docx" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "[OK] Conversión completada" -ForegroundColor Green
}

# Fase 2: División en capítulos
if (-not $SkipSplit) {
    Write-Host "`n============================================================" -ForegroundColor Green
    Write-Host "FASE 2: División en capítulos" -ForegroundColor Green
    Write-Host "============================================================" -ForegroundColor Green
    
    Write-Host "Dividiendo thesis_full.tex..." -ForegroundColor Yellow
    python split_thesis.py source\thesis_full.tex
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Falló la división de thesis_full.tex" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "Dividiendo annex_full.tex..." -ForegroundColor Yellow
    python split_thesis.py source\annex_full.tex
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[ERROR] Falló la división de annex_full.tex" -ForegroundColor Red
        exit 1
    }
    
    Write-Host "[OK] División completada" -ForegroundColor Green
}

# Fase 3: Compilación
Write-Host "`n============================================================" -ForegroundColor Green
Write-Host "FASE 3: Compilación de PDFs" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green

$versions = @(
    @{Name="thesis_with_annex_digital"; File="thesis_with_annex_digital.tex"},
    @{Name="thesis_digital"; File="thesis_digital.tex"},
    @{Name="annex_digital"; File="annex_digital.tex"},
    @{Name="thesis_with_annex_print"; File="thesis_with_annex_print.tex"}
)

if ($Version -ne "all") {
    $versions = $versions | Where-Object { $_.Name -eq $Version }
}

Push-Location build

foreach ($v in $versions) {
    Write-Host "`nCompilando $($v.Name)..." -ForegroundColor Yellow
    
    $baseName = $v.Name
    
    # XeLaTeX pasada 1
    xelatex -interaction=nonstopmode "$baseName.tex" | Out-Null
    
    # BibTeX (si existe)
    if (Test-Path "$baseName.aux") {
        bibtex "$baseName.aux" | Out-Null
    }
    
    # XeLaTeX pasadas 2 y 3
    xelatex -interaction=nonstopmode "$baseName.tex" | Out-Null
    xelatex -interaction=nonstopmode "$baseName.tex" | Out-Null
    
    # Mover PDF a output
    if (Test-Path "$baseName.pdf") {
        New-Item -ItemType Directory -Force -Path ..\output | Out-Null
        Copy-Item "$baseName.pdf" "..\output\$($v.Name).pdf" -Force
        Write-Host "[OK] $($v.Name).pdf generado" -ForegroundColor Green
    } else {
        Write-Host "[ERROR] No se generó $baseName.pdf" -ForegroundColor Red
    }
}

Pop-Location

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "Pipeline completada!" -ForegroundColor Cyan
Write-Host "PDFs disponibles en: output\" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
