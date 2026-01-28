# Word to LaTeX Thesis Conversion

## Goal

Convert thesis from Word to LaTeX and generate 4 PDF outputs:
    - thesis_with_annex_digital_version.pdf - Full thesis with colored links (digital submission)
    - thesis_digital_version.pdf - Thesis only, colored links
    - annex_thesis_digital_version.pdf - Annex only, colored links
    - thesis_with_annex_printed_version.pdf - Full thesis, black/white links except figures (for printing)

thesis_docx_to_latex/
├── source/
│   ├── main_thesis.tex          # Main thesis content
│   ├── annex.tex                # Annex content
│   ├── chapters/                # Individual chapter files
│   ├── figures/                 # All figures
│   └── references.bib           # Bibliography
├── config/
│   ├── digital_config.tex       # Digital version settings (colored links)
│   └── print_config.tex         # Print version settings (black links)
├── build/
│   ├── thesis_with_annex_digital.tex
│   ├── thesis_digital.tex
│   ├── annex_digital.tex
│   └── thesis_with_annex_print.tex
├── output/
│   ├── thesis_with_annex_digital_version.pdf
│   ├── thesis_digital_version.pdf
│   ├── annex_thesis_digital_version.pdf
│   └── thesis_with_annex_printed_version.pdf
└── input/
    ├── thesis.docx
    └── annex_thesis.docx

I tried to generate an automatic pipeline to convert the docx to latex but didnt work, I am rtweaking things semiautomatically  (manually!).

### ToDos

1. Fix figure and table titles so that they have the same font as the number (which is different from caption texts).
2. Finish fixing the tables of the Annex. We shoudl delete all tables from Annexes (C:\Users\oprio\Documents\thesis_docx_to_latex\source\chapters\annex) and import these instead C:\Users\oprio\Documents\thesis_docx_to_latex\source\annex_tables.tex
3. References shouldn't be numbers, they should be in the format [Author, Year] and the references should be sorted alphabetically. I like this style: 14. How do you get nicely formatted URLs in the bibliography?
Answer
Use the url package by Donald Arseneau.

Example usage
In the preamble:

\usepackage{url}

%% Define a new 'leo' style for the package that will use a smaller font.
\makeatletter
\def\url@leostyle{%
  \@ifundefined{selectfont}{\def\UrlFont{\sf}}{\def\UrlFont{\small\ttfamily}}}
\makeatother
%% Now actually use the newly defined style.
\urlstyle{leo}

In a BibTeX entry:

@misc{
    c.elmohamed,
    author = "Saleh Elmohamed",
    title = "Examples in {H}igh {P}erformance {F}ortran",
    howpublished = "Website",
    year = {1996},
    note = {\url{<http://www.npac.syr.edu/projects/>
                    cpsedu/summer98summary/ examples/hpf/hpf.html}}
}

1. The headers shouldn't have a line, I prefer just the title wihtout a line. In addition, odd-numbered pages should have the header title in the right and even-numbered pafes should have the title in the left.
2. The list of abbreviations should be one page only ideally, perhaps in two columns.
3. The references should be listed in the tabel of contents at the end, right after the conclusions and without a number of course.
Once we have done all of this, we will compile the thesis_digital.tex and then I will go manually chapter by chapter fixing structure, typos, references (abbreivations, citations, figures, tables adn other chatpers/sections) with your help. Then we will do the same for the annex and finally we will compile the thesis_with_annex_digital.tex and the thesis_with_annex_printed_version.tex.
If time allows, we will add some ornaments with psvectorian for the five Parts, the dedication and the funding page.
The printed version should have a first page right before the preamble saying that this thesis cover was crated by scientist and scietnific illutrstor Maria Balaguer.
