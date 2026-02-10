# LaTeX Thesis Conversion - Action Items

## Project Context

Converting PhD thesis from Word to LaTeX. Manual semi-automated process using pandoc with ongoing refinements.

**Target outputs:**

- `thesis_with_annex_digital_version.pdf` - Full thesis, colored links (digital submission)
- `thesis_digital_version.pdf` - Thesis only, colored links
- `annex_thesis_digital_version.pdf` - Annex only, colored links
- `thesis_with_annex_printed_version.pdf` - Full thesis, black links (print)


Only the **digital full thesis with annex** PDF (`output/thesis_with_annex_digital.pdf`) is included in the repository. 
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

To compile the **Annex** specifically:

```bash
# 1. Compile LaTeX
xelatex -output-directory=build build/annex_digital.tex

# 2. Process Bibliography
bibtex build/annex_digital

# 3. Final Compilation
xelatex -output-directory=build build/annex_digital.tex
xelatex -output-directory=build build/annex_digital.tex
```

To compile the **Combined Thesis and Annex** (Digital Version):

```bash
# 1. Compile LaTeX
xelatex -output-directory=build build/thesis_with_annex_digital.tex

# 2. Process Bibliography
bibtex build/thesis_with_annex_digital

# 3. Final Compilation
xelatex -output-directory=build build/thesis_with_annex_digital.tex
xelatex -output-directory=build build/thesis_with_annex_digital.tex
```

**Output:** The final PDFs will be at `build/thesis_digital.pdf` and `build/annex_digital.pdf`.

# For combined print version
# 1. Compile LaTeX
xelatex -output-directory=build build/thesis_with_annex_print.tex

# 2. Process Bibliography
bibtex build/thesis_with_annex_print

# 3. Final Compilation (Run twice for cross-references)
xelatex -output-directory=build build/thesis_with_annex_print.tex
xelatex -output-directory=build build/thesis_with_annex_print.tex

### Optional: printed cover and cover credits

You can add two extra pages **before** the titlepage (they do not affect main-body page numbering):

1. **Cover image** — full-page PDF (or image) in `source/figures/`, e.g. `cover_A4.pdf`
2. **Cover credits** — `source/frontmatter/printed_cover_credits.tex`

In the **build file** (e.g. `build/thesis_digital.tex` or `build/thesis_with_annex_print.tex`), set one or both flags before `\input{../main.tex}`:

```latex
\def\includecoverimage{true}   % include the cover image page
\def\includecovercredits{true} % include the cover credits page
```

- **Print version** (`thesis_with_annex_print.tex`) already has both set to `true`.
- Other build files leave them unset (no cover/credits). Add the lines above if you want them for a given build.
