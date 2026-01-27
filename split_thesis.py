#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script para dividir thesis_full.tex y annex_full.tex en archivos separados
por parte/capítulo/sección especial.
"""

import re
import sys
from pathlib import Path

def extract_section_content(content, start_marker, end_marker=None):
    """Extrae el contenido entre dos marcadores."""
    start_idx = content.find(start_marker)
    if start_idx == -1:
        return None, None
    
    if end_marker:
        end_idx = content.find(end_marker, start_idx + len(start_marker))
        if end_idx == -1:
            end_idx = len(content)
    else:
        end_idx = len(content)
    
    section_content = content[start_idx:end_idx]
    return section_content, end_idx

def clean_latex_content(content):
    """Limpia el contenido LaTeX de comandos innecesarios de Pandoc."""
    # Eliminar comandos \protect\phantomsection y labels innecesarios al inicio
    content = re.sub(r'\\protect\\phantomsection\\label\{[^}]+\}\{\}', '', content)
    # Limpiar espacios múltiples
    content = re.sub(r'\n{3,}', '\n\n', content)
    return content.strip()

def sanitize_filename(name):
    """Convierte un título en un nombre de archivo válido."""
    # Convertir a minúsculas y reemplazar espacios/espacios especiales
    name = name.lower()
    name = re.sub(r'[^\w\s-]', '', name)
    name = re.sub(r'[-\s]+', '_', name)
    name = name.strip('-_')
    return name

def split_thesis_file(tex_file, output_dir):
    """Divide el archivo .tex en múltiples archivos por sección/capítulo/parte."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    with open(tex_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Separar el preámbulo (todo antes de \begin{document})
    preamble_end = content.find('\\begin{document}')
    if preamble_end == -1:
        print(f"[ERROR] No se encontró \\begin{{document}} en {tex_file}")
        return False
    
    preamble = content[:preamble_end]
    body = content[preamble_end:]
    
    # Guardar el preámbulo para referencia (no lo usaremos directamente)
    # pero lo necesitamos para entender la estructura
    
    sections = []
    
    # Buscar frontmatter y sus secciones especiales
    frontmatter_start = body.find('\\frontmatter')
    if frontmatter_start != -1:
        mainmatter_start = body.find('\\mainmatter', frontmatter_start)
        frontmatter_content = body[frontmatter_start:mainmatter_start]
        
        # Extraer secciones especiales del frontmatter
        special_sections = [
            (r'Abstract', 'abstract'),
            (r'Resumen', 'resumen'),
            (r'Resum', 'resum'),
            (r'Acknowledgements', 'acknowledgements'),
            (r'List of Figures', 'list_of_figures'),
            (r'List of Tables', 'list_of_tables'),
            (r'List of Abbreviations', 'list_of_abbreviations'),
        ]
        
        for pattern, filename in special_sections:
            # Buscar el título de la sección
            # Construir el patrón escapando solo el patrón de búsqueda, no las barras de LaTeX
            pattern_escaped = re.escape(pattern)
            # Usar raw string pero construir el patrón correctamente
            regex = '\\\\protect\\\\phantomsection\\\\label\\{[^}]+\\}\\{\\}\\{' + pattern_escaped + '\\}'
            match = re.search(regex, frontmatter_content)
            if match:
                start_pos = match.start()
                # Buscar el siguiente título o el final del frontmatter
                next_match = re.search(r'\\protect\\phantomsection\\label\{[^}]+\}\{\}\{', frontmatter_content[start_pos+1:])
                if next_match:
                    end_pos = start_pos + 1 + next_match.start()
                else:
                    end_pos = len(frontmatter_content)
                
                section_content = frontmatter_content[start_pos:end_pos]
                section_content = clean_latex_content(section_content)
                
                sections.append({
                    'type': 'frontmatter_section',
                    'filename': f'{filename}.tex',
                    'content': section_content,
                    'order': len(sections)
                })
    
    # Buscar partes y capítulos en el mainmatter
    mainmatter_start = body.find('\\mainmatter')
    if mainmatter_start == -1:
        print("[ERROR] No se encontró \\mainmatter")
        return False
    
    mainmatter_content = body[mainmatter_start:]
    backmatter_start = mainmatter_content.find('\\backmatter')
    
    if backmatter_start != -1:
        mainmatter_content = mainmatter_content[:backmatter_start]
    
    # Buscar partes (están como texto con \protect\phantomsection)
    part_pattern = r'\\protect\\phantomsection\\label\{[^}]+\}\{\}\{Part\s+([IVX]+)\.\s*([^}]+)\}'
    part_matches = list(re.finditer(part_pattern, mainmatter_content))
    
    # Buscar capítulos
    chapter_pattern = r'\\chapter\{([^}]+)\}'
    chapter_matches = list(re.finditer(chapter_pattern, mainmatter_content))
    
    # Combinar partes y capítulos ordenados por posición
    divisions = []
    for match in part_matches + chapter_matches:
        divisions.append({
            'type': 'part' if 'Part' in match.group(0) else 'chapter',
            'match': match,
            'position': match.start()
        })
    
    divisions.sort(key=lambda x: x['position'])
    
    # Extraer contenido de cada división
    for i, div in enumerate(divisions):
        start_pos = div['position']
        end_pos = divisions[i+1]['position'] if i+1 < len(divisions) else len(mainmatter_content)
        
        section_content = mainmatter_content[start_pos:end_pos]
        section_content = clean_latex_content(section_content)
        
        if div['type'] == 'part':
            # Extraer número y título de la parte
            part_match = re.search(r'Part\s+([IVX]+)\.\s*([^\n]+)', section_content)
            if part_match:
                part_num = part_match.group(1)
                part_title = part_match.group(2).strip()
                filename = f'part_{part_num.lower()}_{sanitize_filename(part_title)}.tex'
            else:
                filename = f'part_{i+1}.tex'
            
            sections.append({
                'type': 'part',
                'filename': filename,
                'content': section_content,
                'order': len(sections)
            })
        
        elif div['type'] == 'chapter':
            # Extraer título del capítulo
            chapter_match = re.search(r'\\chapter\{([^}]+)\}', section_content)
            if chapter_match:
                chapter_title = chapter_match.group(1)
                # Limpiar comandos LaTeX del título
                chapter_title = re.sub(r'\\texorpdfstring\{[^}]+\}\{([^}]+)\}', r'\1', chapter_title)
                chapter_title = re.sub(r'\\[a-zA-Z]+\{', '', chapter_title)
                chapter_title = chapter_title.strip()
                
                # Extraer número del capítulo si está antes del título
                chapter_num_match = re.search(r'Chapter\s+(\d+)', section_content[:200])
                if chapter_num_match:
                    chapter_num = chapter_num_match.group(1)
                    filename = f'chapter_{chapter_num}_{sanitize_filename(chapter_title)}.tex'
                else:
                    filename = f'chapter_{len([s for s in sections if s["type"]=="chapter"])+1}_{sanitize_filename(chapter_title)}.tex'
            else:
                filename = f'chapter_{len([s for s in sections if s["type"]=="chapter"])+1}.tex'
            
            sections.append({
                'type': 'chapter',
                'filename': filename,
                'content': section_content,
                'order': len(sections)
            })
    
    # Guardar cada sección en un archivo separado
    saved_files = []
    for section in sections:
        filepath = output_dir / section['filename']
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(section['content'])
        saved_files.append(section['filename'])
        print(f"[OK] Guardado: {section['filename']} ({section['type']})")
    
    print(f"\n[OK] Total: {len(sections)} archivos creados en {output_dir}")
    return True

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso:")
        print("  python split_thesis.py <thesis_full.tex|annex_full.tex>")
        sys.exit(1)
    
    tex_file = sys.argv[1]
    
    if 'thesis' in tex_file.lower():
        output_dir = 'source/chapters/thesis'
    elif 'annex' in tex_file.lower():
        output_dir = 'source/chapters/annex'
    else:
        output_dir = 'source/chapters'
    
    success = split_thesis_file(tex_file, output_dir)
    
    if success:
        print(f"\n[OK] División completada exitosamente")
