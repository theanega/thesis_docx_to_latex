#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de prueba rápida para compilar una versión y detectar errores.
Útil para debugging antes de ejecutar la pipeline completa.
"""

import subprocess
import sys
from pathlib import Path

BUILD_DIR = Path("build")
OUTPUT_DIR = Path("output")

def test_compile(version_name):
    """Compila una versión específica para probar."""
    build_file = BUILD_DIR / f"{version_name}.tex"
    
    if not build_file.exists():
        print(f"[ERROR] No se encuentra {build_file}")
        return False
    
    print(f"\n{'='*60}")
    print(f"PRUEBA DE COMPILACIÓN: {version_name}")
    print(f"{'='*60}\n")
    
    # Cambiar al directorio build
    original_dir = Path.cwd()
    os.chdir(BUILD_DIR)
    
    try:
        base_name = build_file.stem
        
        # Primera pasada: XeLaTeX (mostrar errores)
        print("Ejecutando XeLaTeX (pasada 1)...")
        result = subprocess.run(
            ["xelatex", "-interaction=nonstopmode", f"{base_name}.tex"],
            capture_output=False
        )
        
        if result.returncode != 0:
            print(f"\n[ERROR] XeLaTeX falló con código {result.returncode}")
            print("Revisa los errores arriba.")
            return False
        
        print("\n[OK] Primera pasada completada")
        print("\nSi ves errores, revísalos antes de continuar.")
        print("Si todo está bien, puedes ejecutar la pipeline completa.")
        
        return True
    
    finally:
        os.chdir(original_dir)

if __name__ == "__main__":
    import os
    
    if len(sys.argv) < 2:
        print("Uso: python test_compile.py <nombre_version>")
        print("\nVersiones disponibles:")
        print("  - thesis_with_annex_digital")
        print("  - thesis_digital")
        print("  - annex_digital")
        print("  - thesis_with_annex_print")
        sys.exit(1)
    
    version = sys.argv[1]
    test_compile(version)
