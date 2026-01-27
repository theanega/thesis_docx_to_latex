# Instrucciones de Compilación

## Estructura del Proyecto

```
thesis_docx_to_latex/
├── main.tex                    # Documento principal (no compilar directamente)
├── build/                      # Archivos de compilación para las 4 versiones
│   ├── thesis_with_annex_digital.tex
│   ├── thesis_digital.tex
│   ├── annex_digital.tex
│   └── thesis_with_annex_print.tex
├── config/                     # Configuraciones por versión
│   ├── digital_config.tex      # Links coloreados
│   └── print_config.tex        # Links negros
├── source/
│   ├── chapters/               # Capítulos divididos
│   │   ├── thesis/            # Capítulos de la tesis
│   │   └── annex/             # Capítulos del anexo
│   ├── frontmatter/           # Abstract, Resumen, Acknowledgements, etc.
│   ├── figures/               # Todas las figuras (PNG/PDF)
│   └── references.bib         # Bibliografía
└── output/                     # PDFs generados (no versionado)
```

## Compilación

### Requisitos Previos

1. **Python 3** (para scripts de automatización)
2. **Pandoc** instalado y en el PATH
   - Descargar desde: https://pandoc.org/installing.html
3. **XeLaTeX** o **LuaLaTeX** instalado (NO usar pdfLaTeX)
   - Windows: MiKTeX o TeX Live
   - macOS: MacTeX
   - Linux: TeX Live
4. **Fuente Roboto** instalada en el sistema
   - Windows: `C:/Windows/Fonts/Roboto-Regular.ttf` (se detecta automáticamente)
   - macOS: `/System/Library/Fonts/` o `/Library/Fonts/`
   - Linux: `/usr/share/fonts/truetype/roboto/`

### Pipeline Automática (Recomendado)

La forma más fácil de regenerar todos los PDFs desde los archivos Word:

#### Windows (PowerShell):
```powershell
# Regenerar todo desde los .docx
.\pipeline.ps1

# Solo compilar (sin convertir .docx)
.\pipeline.ps1 -SkipConversion -SkipSplit

# Compilar solo una versión específica
.\pipeline.ps1 -Version thesis_digital
```

#### Linux/macOS (Python):
```bash
# Regenerar todo desde los .docx
python pipeline.py

# Solo compilar (sin convertir .docx)
python pipeline.py --skip-conversion --skip-split

# Compilar solo una versión específica
python pipeline.py --version thesis_digital
```

### Compilación Manual

Si prefieres compilar manualmente:

```bash
# Versión 1: Tesis + Anexo (Digital)
cd build
xelatex thesis_with_annex_digital.tex
bibtex thesis_with_annex_digital
xelatex thesis_with_annex_digital.tex
xelatex thesis_with_annex_digital.tex

# Versión 2: Solo Tesis (Digital)
xelatex thesis_digital.tex
bibtex thesis_digital
xelatex thesis_digital.tex
xelatex thesis_digital.tex

# Versión 3: Solo Anexo (Digital)
xelatex annex_digital.tex
bibtex annex_digital
xelatex annex_digital.tex
xelatex annex_digital.tex

# Versión 4: Tesis + Anexo (Impresión)
xelatex thesis_with_annex_print.tex
bibtex thesis_with_annex_print
xelatex thesis_with_annex_print.tex
xelatex thesis_with_annex_print.tex
```

### Prueba Rápida

Para probar la compilación sin generar todos los PDFs:

```bash
# Windows
python test_compile.py thesis_digital

# Linux/macOS
python3 test_compile.py thesis_digital
```

## Configuración de Fuentes

Si Roboto no se encuentra automáticamente, edita `main.tex` y descomenta/ajusta las líneas 47-50 según tu sistema operativo.

## Próximos Pasos

1. **Completar el frontmatter**: Crear archivos en `source/frontmatter/` para:
   - `titlepage.tex` (portada)
   - `abstract.tex`
   - `resumen.tex`
   - `resum.tex`
   - `acknowledgements.tex`
   - `dedication.tex`

2. **Revisar y ajustar capítulos**: Los capítulos ya están divididos en `source/chapters/`, pero necesitan:
   - Reemplazar referencias a figuras de Pandoc con tus figuras (`fig_X_Y`)
   - Ajustar formato de tablas con `booktabs`
   - Verificar que todas las partes empiecen en página impar

3. **Configurar bibliografía**: Asegúrate de que `source/references.bib` esté completo y configurado correctamente.

4. **Probar compilación**: Intenta compilar una versión para identificar errores temprano.

## Notas Importantes

- **Páginas impares**: Todos los `\part{}` y `\chapter{}` deben empezar en página impar. Usa `\cleardoublepage` antes de cada uno.
- **Figuras**: Usa la nomenclatura `fig_X_Y` donde X es el capítulo e Y el número de figura.
- **Links**: En versiones digitales son azules y clickables. En versión impresa son negros e invisibles.
