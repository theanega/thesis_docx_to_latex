# Word to LaTeX Thesis Conversion

## Goal
Convert thesis from Word to LaTeX and generate 4 PDF outputs:

    - thesis_with_annex_digital_version.pdf - Full thesis with colored links (digital submission)
    - thesis_digital_version.pdf - Thesis only, colored links
    - annex_thesis_digital_version.pdf - Annex only, colored links
    - thesis_with_annex_printed_version.pdf - Full thesis, black/white links except figures (for printing)

Pre-conversion I did: 
 Export all figures as PDF or high-res PNG
 Export Zotero bibliography as references.bib

Conversion: 
1. Hemos ejecutado esto: pandoc `
  input/thesis.docx `
  --standalone `
  --to=latex `
  --top-level-division=chapter `
  --extract-media=source/figures/thesis `
  --output=source/thesis_full.tex

input/thesis.docx: tu archivo Word de entrada.
--standalone: Pandoc genera un documento LaTeX completo (con \documentclass, \begin{document}, etc.). Después moveremos/integraremos el contenido en tu propio main.tex.
--to=latex: salida en LaTeX (por defecto sería similar, pero lo dejamos explícito).
--top-level-division=chapter: le dice a Pandoc que el nivel superior de estructura corresponde a capítulos (\chapter{}), muy importante para tu template tipo libro.
--extract-media=source/figures/thesis: extrae todas las imágenes incrustadas en el .docx a esa carpeta, y actualiza las referencias en el .tex para apuntar allí. Encaja con tu estructura de source/figures/.
--output=source/thesis_full.tex: nombre del .tex intermedio que contendrá toda la tesis













thesis_docx_to_latex/
├── source/
│   ├── main_thesis.tex          # Main thesis content
│   ├── annex.tex                # Annex content
│   ├── chapters/                # Individual chapter files
│   ├── figures/                 # All figures
│   └── references.bib           # Bibliography
├── config/
│   ├── digital_config.tex       # Digital version settings (colored links)
│   ├── print_config.tex         # Print version settings (black links)
│   └── upc_preamble.tex         # UPC template preamble
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

    ##### converting to latex
- This is the full list of different styles I have used in Word: 
  - Normal: for text
  - Part Heading: for the titles of the Parts (I have 5 in total) such as "Part III. Methodological Framework". I also used this title for the first few headings that are not chapters: List of Figures, List of Tables, List of Abbreviations, Acknowledgements, Resumen, Resum, Abstract
  - Chapter number: for the chapter number before the title such as "Chapter 1", "Chapter 2" etc
  - Heading 1: for the Chapter Titles such as "Motivation, Objectives, and Contributions" or "Colorectal Liver Metastases"
  - Heading 2: for the chatper's sections such as "1.1. Motivation" or "3.1. Background"
  - Heading 3: for the chapter's subsections such as 3.3.1 Resectable disease and 3.3.2. Unresectable disease
  - Heading 4: for the chapter's subsubsections such as 7.3.4.1. CT Configurations
  - quote: for quotes
  - caption text: for caption text
  - TitleCaption: for caption titles
  - Intense quote: for the thesis dedication


- I need that all pages contianing a heading 1 or Part Heading style are in an odd page
- I want to ensure clickable references, figures, and acronyms for the digital versions
- I want to standadrize all figures: centering, consistent captions. remember that i am not creating figures with latex, just embedding pngs or pdfs. I have numbered all my figures as "fig_X_Y" where X is the chapter number and Y the figure number so that the first figure of chapter 7 is fig_7_1. For the annex, I have five figurs adn they are fig_A_X where A, B C or D indicated teh annex and X the figure number.
- I want to create tables with Latex so taht all tables have the same aesthetics
- The printed version should have a first page right before the preamble saying that this thesis cover was crated by scientist and scietnific illutrstor Maria Balaguer 

Okay things that I need to solve by Wednesday 28.01.2026:
1. ttiel header do not include Chapter
2. abbreviations
3. LOF only titles also figs 8.5 and 8.6 wrong. figure titles hsould be bold
4. Tables in general (inlucding LOT and table captions)
5. Aesthetics: still umbers repeated for some subheadings, see font size of heading subheader etc, bullet points separated too specialy key points and contributions.
6. frontpage missing info perhaps? 
7. Then for each chapter
   1. tnego intro del chapter en todos? 
   2. typos (cahtper or chatper instead of chapter i think)
   3. cite (reference) the figures and tables and other sections + where is the figure adn the table (do not split text int he middle)
8. References
9.  Annex too..
10. Annex + thesis - resolution ok?
11. Anex + thesis printed version (black upc logo + MAria Balaguer) also separate header right and left where it is...
12. ornaments... with psvectorian.. solo en parts o quizas ne key poitns y en contributios? aunque es too much creo..