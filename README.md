# LaTeX Thesis Conversion - Action Items

## Project Context

Converting PhD thesis from Word to LaTeX. Manual semi-automated process using pandoc with ongoing refinements.

**Target outputs:**

- `thesis_with_annex_digital_version.pdf` - Full thesis, colored links (digital submission)
- `thesis_digital_version.pdf` - Thesis only, colored links
- `annex_thesis_digital_version.pdf` - Annex only, colored links
- `thesis_with_annex_printed_version.pdf` - Full thesis, black links (print)

**Project structure:**

```
thesis_docx_to_latex/
├── source/         # Main content (main_thesis.tex, annex.tex, chapters/, figures/, references.bib)
├── config/         # digital_config.tex, print_config.tex
├── build/          # Compilation files
├── output/         # Final PDFs
└── input/          # Original .docx files
```

## How to Build the PDF

This project uses a custom build pipeline. **Do not compile `main.tex` directly.**

To compile manually, run these commands from the **project root**:

```bash
# 1. Compile LaTeX
xelatex -output-directory=build build/thesis_digital.tex

# 2. Process Bibliography
bibtex build/thesis_digital

# 3. Final Compilation (Run twice for cross-references)
xelatex -output-directory=build build/thesis_digital.tex
xelatex -output-directory=build build/thesis_digital.tex
```

**Output:** The final PDF will be at `build/thesis_digital.pdf`.

---
