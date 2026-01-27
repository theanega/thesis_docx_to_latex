#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para mapear figuras extraídas por Pandoc a las figuras reales del usuario.
Genera un reporte y permite crear un archivo de mapeo.
"""

import re
import sys
from pathlib import Path

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

def extract_figures_from_tex(tex_file):
    """Extrae todas las referencias a figuras del archivo .tex generado por Pandoc."""
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Patrón para encontrar \includegraphics con su caption asociado
    # Buscamos bloques figure o referencias directas a imágenes
    figures = []
    
    # Buscar bloques \begin{figure}...\end{figure}
    figure_pattern = r'\\begin\{figure\}.*?\\includegraphics.*?\{([^}]+)\}.*?\\caption\{([^}]+(?:\}[^}]*)*)\}.*?\\end\{figure\}'
    matches = re.finditer(figure_pattern, content, re.DOTALL)
    
    for match in matches:
        img_path = match.group(1)
        caption = match.group(2)
        # Limpiar caption de caracteres especiales de LaTeX
        caption = re.sub(r'\\textbar\{\}', '|', caption)
        caption = re.sub(r'\\textbackslash', '', caption)
        caption = re.sub(r'\{|\}', '', caption)
        caption = caption.strip()
        
        figures.append({
            'path': img_path,
            'caption': caption,
            'type': 'figure_block'
        })
    
    # Buscar también \includegraphics sueltos (sin figure block)
    standalone_pattern = r'\\includegraphics.*?\{([^}]+)\}'
    standalone_matches = re.finditer(standalone_pattern, content)
    
    for match in standalone_matches:
        img_path = match.group(1)
        # Verificar que no esté ya en la lista (dentro de un figure block)
        if not any(f['path'] == img_path for f in figures):
            # Buscar contexto alrededor (líneas antes/después)
            start_pos = match.start()
            context_start = max(0, start_pos - 200)
            context_end = min(len(content), start_pos + 200)
            context = content[context_start:context_end]
            
            figures.append({
                'path': img_path,
                'caption': f"[Sin caption - contexto: {context[:100]}...]",
                'type': 'standalone'
            })
    
    return figures

def list_user_figures(figures_dir):
    """Lista todas las figuras del usuario en source/figures/"""
    figures_path = Path(figures_dir)
    user_figures = []
    
    # Buscar archivos de imagen (excluyendo las carpetas thesis/annex/media)
    for ext in ['*.png', '*.pdf', '*.jpg', '*.jpeg']:
        for fig_file in figures_path.rglob(ext):
            # Excluir las carpetas media de Pandoc
            if 'media' not in str(fig_file):
                user_figures.append(fig_file.name)
    
    return sorted(user_figures)

def generate_mapping_report(pandoc_figures, user_figures, output_file):
    """Genera un reporte con todas las figuras para facilitar el mapeo manual."""
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("REPORTE DE MAPEO DE FIGURAS\n")
        f.write("=" * 80 + "\n\n")
        
        f.write("FIGURAS EXTRAÍDAS POR PANDOC:\n")
        f.write("-" * 80 + "\n")
        for i, fig in enumerate(pandoc_figures, 1):
            f.write(f"\n{i}. {fig['path']}\n")
            f.write(f"   Caption: {fig['caption'][:150]}\n")
            f.write(f"   Tipo: {fig['type']}\n")
        
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("FIGURAS DEL USUARIO (source/figures/):\n")
        f.write("-" * 80 + "\n")
        for i, fig_name in enumerate(user_figures, 1):
            f.write(f"{i}. {fig_name}\n")
        
        f.write("\n\n" + "=" * 80 + "\n")
        f.write("PLANTILLA DE MAPEO (edita manualmente):\n")
        f.write("-" * 80 + "\n")
        f.write("# Formato: pandoc_path|usuario_path\n")
        f.write("# Ejemplo: source/figures/thesis/media/image2.png|fig_2_1.png\n\n")
        
        for fig in pandoc_figures:
            f.write(f"{fig['path']}|\n")
    
    print(f"[OK] Reporte generado en: {output_file}")
    print(f"  - {len(pandoc_figures)} figuras de Pandoc encontradas")
    print(f"  - {len(user_figures)} figuras del usuario disponibles")

def apply_mapping(tex_file, mapping_file, output_file):
    """Aplica el mapeo al archivo .tex."""
    # Leer mapeo
    mapping = {}
    with open(mapping_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                parts = line.split('|')
                if len(parts) == 2 and parts[1]:  # Tiene mapeo
                    pandoc_path = parts[0].strip()
                    user_path = parts[1].strip()
                    mapping[pandoc_path] = user_path
    
    if not mapping:
        print("[WARNING] No se encontraron mapeos en el archivo. Asegurate de haber editado el archivo de mapeo.")
        return False
    
    # Leer y reemplazar en el .tex
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    replacements = 0
    for pandoc_path, user_path in mapping.items():
        # Reemplazar la ruta completa
        old_pattern = pandoc_path.replace('\\', '\\\\')
        new_path = f"source/figures/{user_path}"
        content = content.replace(pandoc_path, new_path)
        replacements += 1
    
    # Guardar
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"[OK] Mapeo aplicado: {replacements} figuras reemplazadas")
    print(f"  Archivo guardado en: {output_file}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python map_figures.py report <thesis_full.tex>")
        print("    → Genera reporte de figuras para mapeo manual")
        print("  python map_figures.py apply <thesis_full.tex> <mapping.txt> <output.tex>")
        print("    → Aplica el mapeo al archivo .tex")
        sys.exit(1)
    
    command = sys.argv[1]
    
    if command == 'report':
        if len(sys.argv) < 3:
            print("Error: falta el archivo .tex")
            sys.exit(1)
        
        tex_file = sys.argv[2]
        pandoc_figures = extract_figures_from_tex(tex_file)
        user_figures = list_user_figures('source/figures')
        
        output_report = 'figure_mapping_report.txt'
        generate_mapping_report(pandoc_figures, user_figures, output_report)
        
    elif command == 'apply':
        if len(sys.argv) < 5:
            print("Error: falta archivo .tex, archivo de mapeo o archivo de salida")
            sys.exit(1)
        
        tex_file = sys.argv[2]
        mapping_file = sys.argv[3]
        output_file = sys.argv[4]
        apply_mapping(tex_file, mapping_file, output_file)
    
    else:
        print(f"Error: comando desconocido '{command}'")
        sys.exit(1)
