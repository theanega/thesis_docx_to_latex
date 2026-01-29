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

---

## PENDING ISSUES - Priority Order

### 🔴 CRITICAL: Pagination & Document Structure

**Issue 1.1: Part I pagination**
- **Problem:** Part I doesn't start on page 1; unnecessary blank page before it
- **Required fix:** 
  - Part I must start on page 1
  - Chapter 1 should start on page 3
  - Remove blank page before Part I
- **Files likely affected:** `main_thesis.tex`, preamble settings

**Issue 1.2: Blank pages throughout document**
- **Problem:** Unnecessary blank pages; some blank pages have headers
- **Rules to enforce:**
  - Blank pages only to ensure next page is odd (right-hand printing)
  - NO headers on blank pages ever
  - Remove unnecessary blank pages before Parts (especially Part IV)
- **Files likely affected:** Document class settings, `\cleardoublepage` commands

---

### 🟡 HIGH: Table of Contents Issues

**Issue 2.1: TOC link redirects**
- **Problem:** Clicking "List of Figures" redirects to "Acknowledgements"; same for "List of Tables"
- **Required fix:** Correct hyperref anchors
- **Files likely affected:** Front matter, hyperref configuration

**Issue 2.2: TOC color formatting**
- **Problem:** All TOC text currently one color
- **Required fix:** 
  - Main text: black
  - Page numbers: blue (clickable)
- **Files likely affected:** `hyperref` settings in config files

---

### 🟡 HIGH: Table Formatting

**Issue 3.1: Table 4.1 alignment**
- **Problem:** Column titles not centered; inconsistent line breaking
- **Required fix:**
  - Center all column headers (Cancer type, Modality, etc.)
  - Make headers consistent: if "Cancer type" spans 2 lines, also split "Technical validation", "Biological validation", "Clinical validation"
  - For "Biological validation": split entries like "Yes (histology)" into 2 lines OR abbreviate to "histo."
- **File:** Chapter 4

**Issue 3.2: Table 6.1 width**
- **Problem:** Table exceeds page bounds
- **Suggested fix:** Move "Median (IQR)" below "LCL" in first columns to reduce width
- **File:** Chapter 6

**Issue 3.3: Table 8.1 structure**
- **Problem:** Two extra empty columns after VHIO
- **Required fix:**
  - Only 3 centered columns: Variables | TCIA | VHIO
  - Move before Section 8.3.2
  - Should fit on one full page
- **File:** Chapter 8

**Issue 3.4: Table 8.2 placement**
- **Action:** Move before Section 8.3.5
- **File:** Chapter 8

**Issue 3.5: Table 8.3 placement & formatting**
- **Actions:**
  - Place after Figure 8.4
  - Remove bold from values in "HR [95% CI]" columns (keep header bold)
- **File:** Chapter 8

---

### 🟢 MEDIUM: Figure Placement

**Issue 4.1: Figures 3.2 and 3.3**
- **Problem:** Each on separate page unnecessarily
- **Required fix:**
  - Move Section 3.4 slightly higher
  - Place Figure 3.2 at top of page (not centered/middle)
  - Same for Figure 3.3
- **File:** Chapter 3

**Issue 4.2: Figures 5.2 and 5.3**
- **Problem:** Each on own page unnecessarily
- **Required fix:** Allow text flow around these figures
- **File:** Chapter 5

**Issue 4.3: Figure 7.2**
- **Problem:** On separate page, wrong position
- **Required fix:**
  - Place before Section 7.3.2
  - Does not need dedicated page
- **File:** Chapter 7

**Issue 4.4: Figure 9.1**
- **Problem:** Splits sentence mid-paragraph; title not bold
- **Required fix:**
  - Move to just before Section 9.3
  - Make figure title bold (match other figures)
- **File:** Chapter 9

---

### 🟢 MEDIUM: Spacing & Formatting

**Issue 5.1: Chapter 1, Section 1.3**
- **Problem:** Dash indentation inconsistent with rest of document
- **Required fix:** Indent dashes before "Prior O..." to match style in "Latacz et al., 2024 (POEM)" under "International research projects"
- **File:** Chapter 1

**Issue 5.2: Chapter 6 spacing**
- **Problem:** Inconsistent heading levels and bullet spacing, especially preface and Section 6.1
- **Required fix:** Standardize vertical spacing to match rest of document
- **File:** Chapter 6

**Issue 5.3: Chapter 7 contributions spacing**
- **Problem:** Too much vertical space between bullet points
- **Required fix:** Tighten to match Chapter 8 (current page 95)
- **File:** Chapter 7

**Issue 5.4: Chapter 8 section spacing**
- **Problem:** Sections 8.3.5 and 8.3.6 have incorrect heading spacing
- **Required fix:** Fix spacing to match other sections
- **File:** Chapter 8

---

### 🔵 LOW: Abbreviations & References

**Issue 6.1: Missing abbreviations**
- **Action:** Add 13 symbols and mpMRI metric names from Table 5.2 columns 1-2 to abbreviations list
- **Files:** Abbreviations section, possibly Chapter 5

**Issue 6.2: DOI links not clickable (OPTIONAL)**
- **Problem:** DOIs in references not hyperlinked
- **Possible fix:** Add to preamble:
```latex
\usepackage{url}
\makeatletter
\def\url@leostyle{%
  \@ifundefined{selectfont}{\def\UrlFont{\sf}}{\def\UrlFont{\small\ttfamily}}}
\makeatother
\urlstyle{leo}
```
- **Note:** Only fix if straightforward; low priority
- **Files:** Preamble, possibly `references.bib`

---

## Status Tracking
**Last updated:** [Date]  
**Progress:** [ ] 1.1 [ ] 1.2 [ ] 2.1 [ ] 2.2 [ ] 3.1 [ ] 3.2 [ ] 3.3 [ ] 3.4 [ ] 3.5 [ ] 4.1 [ ] 4.2 [ ] 4.3 [ ] 4.4 [ ] 5.1 [ ] 5.2 [ ] 5.3 [ ] 5.4 [ ] 6.1 [ ] 6.2
