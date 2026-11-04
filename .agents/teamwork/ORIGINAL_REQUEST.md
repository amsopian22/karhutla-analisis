# Original User Request

## Initial Request — 2026-11-04T06:49:53Z

Audit and refine the writing, academic English quality, and formatting of the manuscript submission package to ensure full alignment with Elsevier's Applied Geography author guidelines and aims & scope.

Working directory: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis
Integrity mode: development

Target Journal & Manuscript Context:
- Target Journal: Applied Geography (Elsevier, Impact Factor: 7.4, CiteScore: 8.3, Scopus Q1)
- Context: Manuscript previously received an out-of-scope desk rejection from Ecological Modelling; it must be reframed to strongly emphasize applied spatial geography, GIScience, Tobler's First Law, spatial autocorrelation mitigation (Spatial Block CV), and land tenure governance (APL vs concessions).
- Authorship: Ahmad Sopian (First & Corresponding Author, Independent Researcher, Samarinda, Kalimantan Timur, Indonesia, ahmadsopian22@gmail.com), Rahmi Susanti (Co-Author, Faculty of Public Health, Universitas Mulawarman, Samarinda, Kalimantan Timur, Indonesia, rahmi.susanti@fkm.unmul.ac.id)
- Public Repository: https://github.com/amsopian22/karhutla-analisis

## Requirements

### R1. Manuscript Text & Submission Package Audit and Refinement
Audit and refine the writing quality, scientific tone, academic English fluency, coherence, and grammar across all key submission files:
- Main Manuscript Text: `manuscript/manuscript_draft.md`
- Submission Word Document: `manuscript/submission_package/manuscript_main.docx`
- LaTeX Source & PDF: `manuscript/main.tex` and `manuscript/main.pdf`
- Highlights: `manuscript/highlights.md` and `manuscript/submission_package/highlights.docx`
- Cover Letter: `manuscript/cover_letter.md` and `manuscript/submission_package/cover_letter.docx`

### R2. Elsevier Applied Geography Guidelines Verification
Verify and format the submission package according to Elsevier's Applied Geography Guide for Authors:
- Abstract word count must not exceed 250 words.
- Provide between 1 and 7 keywords aligned with the journal.
- Highlights must consist of 3 to 5 bullet points, each with a maximum of 85 characters including spaces.
- Format in-text table and figure citations, references, and CRediT authorship contribution statement according to Elsevier standards.

### R3. Visual and Tabular Rendering Integrity
Ensure all tables and embedded figures render cleanly without visual glitches, unparsed markdown/LaTeX markup, or ASCII placeholders across Markdown, LaTeX/PDF, and Word DOCX formats.

### R4. Thematic & Scope Alignment with Applied Geography
Reframe and strengthen the manuscript's narrative to emphasize applied spatial geography, Tobler's First Law, GIScience, spatial autocorrelation mitigation (Spatial Block CV), and land tenure governance (APL vs concessions) to fit the Aims & Scope of Applied Geography.

### R5. Complete Submission Package Compilation
Update all text source files (`manuscript_draft.md`, `main.tex`, `highlights.md`, `cover_letter.md`) and compile/generate both the final PDF (`main.pdf` via LaTeX) and Word documents (`manuscript_main.docx`, `highlights.docx`, `cover_letter.docx`).

## Verification Resources
The team must write and execute programmatic verification scripts (e.g. Python scripts) to objectively test abstract word count, highlights character length, reference and figure callout consistency, and document compilation.

## Acceptance Criteria

### Editorial Guidelines Compliance
- [ ] Abstract word count is <= 250 words, verified programmatically.
- [ ] Highlights contain between 3 and 5 bullet points, and each bullet point is <= 85 characters including spaces, verified programmatically.
- [ ] Manuscript contains between 1 and 7 keywords.
- [ ] CRediT authorship statement, data availability statement, and references are present and formatted according to Elsevier standards.

### Scope & Content Alignment
- [ ] Manuscript explicitly frames findings around applied spatial geography, Tobler's First Law, GIScience, spatial autocorrelation mitigation, and land governance (APL vs concessions).
- [ ] Cover letter clearly introduces the manuscript's fit for Applied Geography and explains its spatial geographic contributions.

### Document Compilation & Rendering
- [ ] LaTeX source `manuscript/main.tex` compiles successfully into `manuscript/main.pdf` without unparsed syntax or broken figure links.
- [ ] Word documents (`manuscript/submission_package/manuscript_main.docx`, `highlights.docx`, `cover_letter.docx`) are updated and open cleanly with proper table formatting and high-resolution figure embeds.
- [ ] All tables and figures are referenced in text and have no raw markup or ASCII placeholders.
