#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Pipeline automática para convertir tesis de Word a LaTeX y generar los 4 PDFs.

Uso:
    python pipeline.py                    # Regenera todo desde los .docx
    python pipeline.py --skip-conversion   # Solo compila (sin convertir .docx)
    python pipeline.py --version digital  # Solo compila versión digital con anexo
"""

import subprocess
import sys
import os
from pathlib import Path

# Configuración
INPUT_DIR = Path("input")
SOURCE_DIR = Path("source")
BUILD_DIR = Path("build")
OUTPUT_DIR = Path("output")

THESIS_DOCX = INPUT_DIR / "thesis.docx"
ANNEX_DOCX = INPUT_DIR / "annex_thesis.docx"

THESIS_FULL_TEX = SOURCE_DIR / "thesis_full.tex"
ANNEX_FULL_TEX = SOURCE_DIR / "annex_full.tex"

CHAPTERS_THESIS_DIR = SOURCE_DIR / "chapters" / "thesis"
CHAPTERS_ANNEX_DIR = SOURCE_DIR / "chapters" / "annex"

BUILD_FILES = {
    "thesis_with_annex_digital": BUILD_DIR / "thesis_with_annex_digital.tex",
    "thesis_digital": BUILD_DIR / "thesis_digital.tex",
    "annex_digital": BUILD_DIR / "annex_digital.tex",
    "thesis_with_annex_print": BUILD_DIR / "thesis_with_annex_print.tex",
}

def run_command(cmd, description, check=True):
    """Ejecuta un comando y muestra el resultado."""
    print(f"\n{'='*60}")
    print(f"[PIPELINE] {description}")
    print(f"{'='*60}")
    print(f"Ejecutando: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(
            cmd,
            check=check,
            capture_output=False,  # Mostrar output en tiempo real
            text=True
        )
        if result.returncode == 0:
            print(f"[OK] {description} completado exitosamente")
            return True
        else:
            print(f"[ERROR] {description} falló con código {result.returncode}")
            return False
    except subprocess.CalledProcessError as e:
        print(f"[ERROR] {description} falló: {e}")
        return False
    except FileNotFoundError:
        print(f"[ERROR] Comando no encontrado. ¿Está instalado?")
        return False

def convert_docx_to_tex():
    """Convierte los archivos .docx a LaTeX usando Pandoc."""
    print("\n" + "="*60)
    print("FASE 1: Conversión Word → LaTeX")
    print("="*60)
    
    # Verificar que existen los archivos .docx
    if not THESIS_DOCX.exists():
        print(f"[ERROR] No se encuentra {THESIS_DOCX}")
        return False
    
    if not ANNEX_DOCX.exists():
        print(f"[ERROR] No se encuentra {ANNEX_DOCX}")
        return False
    
    # Crear directorios necesarios
    SOURCE_DIR.mkdir(exist_ok=True)
    
    # Convertir tesis principal
    cmd_thesis = [
        "pandoc",
        str(THESIS_DOCX),
        "--standalone",
        "--to=latex",
        "--top-level-division=chapter",
        "--extract-media=" + str(SOURCE_DIR / "figures" / "thesis"),
        "--output=" + str(THESIS_FULL_TEX)
    ]
    
    if not run_command(cmd_thesis, "Conversión de thesis.docx → LaTeX"):
        return False
    
    # Convertir anexo
    cmd_annex = [
        "pandoc",
        str(ANNEX_DOCX),
        "--standalone",
        "--to=latex",
        "--top-level-division=chapter",
        "--extract-media=" + str(SOURCE_DIR / "figures" / "annex"),
        "--output=" + str(ANNEX_FULL_TEX)
    ]
    
    if not run_command(cmd_annex, "Conversión de annex_thesis.docx → LaTeX"):
        return False
    
    print("\n[OK] Conversión Word → LaTeX completada")
    return True

def split_tex_files():
    """Divide los archivos .tex completos en capítulos separados."""
    print("\n" + "="*60)
    print("FASE 2: División en capítulos")
    print("="*60)
    
    # Verificar que existen los archivos .tex generados
    if not THESIS_FULL_TEX.exists():
        print(f"[ERROR] No se encuentra {THESIS_FULL_TEX}")
        print("       Ejecuta la conversión primero o usa --skip-conversion")
        return False
    
    if not ANNEX_FULL_TEX.exists():
        print(f"[ERROR] No se encuentra {ANNEX_FULL_TEX}")
        print("       Ejecuta la conversión primero o usa --skip-conversion")
        return False
    
    # Crear directorios de capítulos
    CHAPTERS_THESIS_DIR.mkdir(parents=True, exist_ok=True)
    CHAPTERS_ANNEX_DIR.mkdir(parents=True, exist_ok=True)
    
    # Dividir tesis
    cmd_split_thesis = [
        sys.executable,
        "split_thesis.py",
        str(THESIS_FULL_TEX)
    ]
    
    if not run_command(cmd_split_thesis, "División de thesis_full.tex en capítulos"):
        return False
    
    # Dividir anexo
    cmd_split_annex = [
        sys.executable,
        "split_thesis.py",
        str(ANNEX_FULL_TEX)
    ]
    
    if not run_command(cmd_split_annex, "División de annex_full.tex en capítulos"):
        return False
    
    print("\n[OK] División en capítulos completada")
    return True

def compile_pdf(version_name, build_file):
    """Compila un PDF específico usando XeLaTeX."""
    print("\n" + "="*60)
    print(f"FASE 3: Compilación de {version_name}")
    print("="*60)
    
    if not build_file.exists():
        print(f"[ERROR] No se encuentra {build_file}")
        return False
    
    # Cambiar al directorio build para compilar
    original_dir = os.getcwd()
    os.chdir(BUILD_DIR)
    
    try:
        base_name = build_file.stem
        
        # Primera pasada: XeLaTeX
        cmd_xelatex1 = ["xelatex", "-interaction=nonstopmode", f"{base_name}.tex"]
        if not run_command(cmd_xelatex1, f"XeLaTeX (pasada 1) - {version_name}", check=False):
            print("[WARNING] Primera pasada de XeLaTeX tuvo errores, continuando...")
        
        # BibTeX (si hay referencias)
        bib_file = BUILD_DIR / f"{base_name}.aux"
        if bib_file.exists():
            cmd_bibtex = ["bibtex", f"{base_name}.aux"]
            run_command(cmd_bibtex, f"BibTeX - {version_name}", check=False)
        
        # Segunda pasada: XeLaTeX
        cmd_xelatex2 = ["xelatex", "-interaction=nonstopmode", f"{base_name}.tex"]
        if not run_command(cmd_xelatex2, f"XeLaTeX (pasada 2) - {version_name}", check=False):
            print("[WARNING] Segunda pasada de XeLaTeX tuvo errores, continuando...")
        
        # Tercera pasada: XeLaTeX (para referencias cruzadas)
        cmd_xelatex3 = ["xelatex", "-interaction=nonstopmode", f"{base_name}.tex"]
        if not run_command(cmd_xelatex3, f"XeLaTeX (pasada 3) - {version_name}", check=False):
            print("[WARNING] Tercera pasada de XeLaTeX tuvo errores, continuando...")
        
        # Mover PDF al directorio output
        OUTPUT_DIR.mkdir(exist_ok=True)
        pdf_source = BUILD_DIR / f"{base_name}.pdf"
        pdf_dest = OUTPUT_DIR / f"{version_name}.pdf"
        
        if pdf_source.exists():
            import shutil
            shutil.copy2(pdf_source, pdf_dest)
            print(f"\n[OK] PDF generado: {pdf_dest}")
            return True
        else:
            print(f"[ERROR] No se generó el PDF: {pdf_source}")
            return False
    
    finally:
        os.chdir(original_dir)

def main():
    """Función principal de la pipeline."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Pipeline automática para convertir tesis Word → LaTeX → PDF"
    )
    parser.add_argument(
        "--skip-conversion",
        action="store_true",
        help="Saltar conversión Word → LaTeX (solo compilar)"
    )
    parser.add_argument(
        "--skip-split",
        action="store_true",
        help="Saltar división en capítulos (solo compilar)"
    )
    parser.add_argument(
        "--version",
        choices=["all", "thesis_with_annex_digital", "thesis_digital", "annex_digital", "thesis_with_annex_print"],
        default="all",
        help="Versión específica a compilar (default: all)"
    )
    
    args = parser.parse_args()
    
    print("="*60)
    print("PIPELINE AUTOMÁTICA: Tesis Word → LaTeX → PDF")
    print("="*60)
    
    # Fase 1: Conversión Word → LaTeX
    if not args.skip_conversion:
        if not convert_docx_to_tex():
            print("\n[ERROR] La conversión falló. Revisa los errores arriba.")
            sys.exit(1)
    else:
        print("\n[SKIP] Saltando conversión Word → LaTeX")
    
    # Fase 2: División en capítulos
    if not args.skip_split:
        if not split_tex_files():
            print("\n[ERROR] La división en capítulos falló. Revisa los errores arriba.")
            sys.exit(1)
    else:
        print("\n[SKIP] Saltando división en capítulos")
    
    # Fase 3: Compilación de PDFs
    print("\n" + "="*60)
    print("FASE 3: Compilación de PDFs")
    print("="*60)
    
    if args.version == "all":
        versions_to_build = BUILD_FILES.items()
    else:
        versions_to_build = [(args.version, BUILD_FILES[args.version])]
    
    success_count = 0
    for version_name, build_file in versions_to_build:
        if compile_pdf(version_name, build_file):
            success_count += 1
    
    # Resumen final
    print("\n" + "="*60)
    print("RESUMEN FINAL")
    print("="*60)
    print(f"PDFs generados exitosamente: {success_count}/{len(list(versions_to_build))}")
    
    if success_count == len(list(versions_to_build)):
        print("\n[OK] Pipeline completada exitosamente!")
        print(f"PDFs disponibles en: {OUTPUT_DIR.absolute()}")
    else:
        print("\n[WARNING] Algunos PDFs no se generaron correctamente.")
        print("Revisa los errores arriba para más detalles.")
        sys.exit(1)

if __name__ == "__main__":
    main()
