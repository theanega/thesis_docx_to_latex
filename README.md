# Word to LaTeX Thesis Conversion

## Goal
Convert thesis from Word to LaTeX and generate 4 PDF outputs:

    - thesis_with_annex_digital_version.pdf - Full thesis with colored links (digital submission)
    - thesis_digital_version.pdf - Thesis only, colored links
    - annex_thesis_digital_version.pdf - Annex only, colored links
    - thesis_with_annex_printed_version.pdf - Full thesis, black/white links except figures (for printing)

Pre-conversion checklist (in Word)

 Create folder structure
 Complete acknowledgements in main thesis
 Export all figures as PDF or high-res PNG
 Save figures to source/figures/main/ and source/figures/annex/
 Fix figure and table captions in annex
 Export Zotero bibliography as references.bib

Conversion steps
bash# Convert main thesis
pandoc original/thesis.docx --standalone --extract-media=source/figures/main -o source/main_thesis_raw.tex

# Convert annex
pandoc original/annex_thesis.docx --standalone --extract-media=source/figures/annex -o source/annex_raw.tex
Post-conversion

Clean up pandoc output
Integrate UPC template
Create 4 master .tex files in build/
Compile all versions
Proofread each chapter