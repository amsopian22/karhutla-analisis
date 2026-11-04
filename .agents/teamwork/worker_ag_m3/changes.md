# Changes Report: Milestone 3 (M3) Programmatic Verification Test Suite

**Agent**: `worker_ag_m3` (teamwork_worker)  
**Roles**: implementer, qa, specialist  
**Working Directory**: `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/worker_ag_m3/`  
**Execution Environment**: Conda `karhutla_env` (`/opt/anaconda3/envs/karhutla_env/bin/python`, Python 3.10.22, pytest 9.2.0)  
**Target Journal**: *Applied Geography* (Elsevier, IF: 7.4, CiteScore: 8.3, Scopus Q1)

---

## 1. Summary of Changes

Milestone 3 mandates the creation and execution of a robust, fully automated programmatic verification test suite to validate the manuscript submission package against all editorial and scientific requirements of Elsevier *Applied Geography*.

Five dedicated, genuine verification test suites have been designed, implemented, and placed under exclusive write ownership in `tests/`:

1. `tests/test_abstract_word_count.py`: Verifies abstract word count across LaTeX, Markdown, Word DOCX, and PDF ($\le 250$ words).
2. `tests/test_highlights_length.py`: Verifies highlights count (3–5 bullets) and length per bullet ($\le 85$ characters including spaces) across Markdown and DOCX.
3. `tests/test_keywords_alignment.py`: Verifies author keywords count (1–7 keywords, exactly 7) and domain taxonomy alignment with applied spatial geography and GIScience.
4. `tests/test_reference_figure_callout_consistency.py`: Verifies bidirectional consistency for Tables 1–4, Figures 1–7, absence of broken links/dangling refs, absence of mismatched figure numbers, and resolution of all LaTeX `\cite` keys against `references.bib`.
5. `tests/test_document_compilation_rendering.py`: Verifies Tectonic compilation into `main.pdf` (28 pages, exit code 0), and Word DOCX XML integrity (4 native `<w:tbl>`, 0 raw markdown pipes, OMML `<m:oMath>` equations, and 7 embedded 300 DPI figures matching master SHA-256 hashes 100%).

---

## 2. Detailed Implementation Specifications

### 2.1. `tests/test_abstract_word_count.py`
- **Objective**: Programmatically enforce Elsevier Applied Geography Guide for Authors rule: Abstract must not exceed 250 words across all publication formats.
- **Functions Implemented**:
  - `clean_words(text)`: Cleans and tokenizes text, removing markup artifacts while preserving hyphenated compounds.
  - `get_latex_abstract_text()`: Extracts abstract body between `\begin{abstract}` and `\vspace` / `\textbf{Keywords:}` / `\end{abstract}` in `manuscript/sections/00_abstract.tex`. Strips LaTeX macros (`\noindent`, `\texttt`, `\textit`, math symbols).
  - `get_markdown_abstract_text()`: Extracts abstract paragraph between `## Abstract` and `**Keywords:**` in `manuscript/manuscript_draft.md`. Strips Markdown formatting tokens.
  - `get_docx_abstract_text()`: Uses `zipfile` and `xml.etree.ElementTree` to parse `word/document.xml` from `manuscript/submission_package/manuscript_main.docx` and locate the abstract paragraph following the "Abstract" heading.
  - `get_pdf_abstract_text()`: Uses `/opt/homebrew/bin/pdftotext` to extract text from page 1 of `manuscript/main.pdf` and extract text between "Abstract" and "Keywords:".
  - `test_latex_abstract_word_count()`: Asserts $150 \le \text{words} \le 250$. Result: **244 words** (PASSED).
  - `test_markdown_abstract_word_count()`: Asserts $150 \le \text{words} \le 250$. Result: **246 words** (PASSED).
  - `test_docx_abstract_word_count()`: Asserts $150 \le \text{words} \le 250$. Result: **237 words** (PASSED).
  - `test_pdf_abstract_word_count()`: Asserts $150 \le \text{words} \le 250$. Result: **244 words** (PASSED).
  - `test_abstract_cross_format_consistency()`: Asserts all formats are mutually consistent ($\Delta \le 15$ words). Max diff: 9 words (PASSED).

### 2.2. `tests/test_highlights_length.py`
- **Objective**: Programmatically verify that research highlights contain 3 to 5 bullet points, each with a maximum of 85 characters including spaces.
- **Functions Implemented**:
  - `get_markdown_highlights()`: Parses lines starting with `*` or `-` in `manuscript/highlights.md`.
  - `get_docx_highlights()`: Parses bullet paragraphs from `manuscript/submission_package/highlights.docx` using `zipfile` and `xml.etree.ElementTree`.
  - `test_markdown_highlights_count()`: Asserts $3 \le \text{bullets} \le 5$. Result: **5 bullets** (PASSED).
  - `test_markdown_highlights_character_length()`: Asserts every bullet has $20 \le \text{chars} \le 85$. Lengths: 72, 76, 75, 78, 79 characters (PASSED).
  - `test_docx_highlights_count()`: Asserts $3 \le \text{bullets} \le 5$. Result: **5 bullets** (PASSED).
  - `test_docx_highlights_character_length()`: Asserts every bullet has $20 \le \text{chars} \le 85$. Lengths: 72, 76, 75, 78, 79 characters (PASSED).
  - `test_highlights_cross_format_parity()`: Asserts 100% equivalence between Markdown and DOCX highlights text and bullet counts (PASSED).

### 2.3. `tests/test_keywords_alignment.py`
- **Objective**: Programmatically verify that author keywords count is between 1 and 7 (strictly $\le 7$), and aligned with applied spatial geography and GIScience.
- **Functions Implemented**:
  - `get_latex_keywords()`: Parses keywords from `manuscript/sections/00_abstract.tex`.
  - `get_markdown_keywords()`: Parses keywords from `manuscript/manuscript_draft.md`.
  - `get_docx_keywords()`: Parses keywords from `manuscript/submission_package/manuscript_main.docx`.
  - `test_latex_keywords_count()`, `test_markdown_keywords_count()`, `test_docx_keywords_count()`: Asserts $1 \le \text{count} \le 7$. Result: Exactly **7 keywords** on all three formats (PASSED).
  - `test_keywords_exact_alignment_with_applied_geography()`: Verifies presence of core spatial geography anchors (`spatial`, `geography`, `autocorrelation`, `cross-validation`, `tenure`, `peatlands`, `governance`, `wildfire`, `modeling`) (PASSED).
  - `test_keywords_cross_format_parity()`: Asserts that normalized keywords lists are identical across LaTeX, Markdown, and DOCX:
    * *Applied spatial geography*
    * *Tropical peatlands*
    * *Spatial autocorrelation*
    * *Spatial block cross-validation*
    * *Land tenure governance*
    * *Wildfire intensity modeling*
    * *Mega Rice Project*
    Result: 100% identical (PASSED).

### 2.4. `tests/test_reference_figure_callout_consistency.py`
- **Objective**: Programmatically verify bidirectional consistency for tables, figures, image assets, and citations across LaTeX, Markdown, and DOCX without broken links, uncalled assets, or mismatched numbers.
- **Functions Implemented**:
  - `test_latex_bibtex_citations_resolve()`: Scans all `.tex` files for `\cite*` macros and resolves all 40 unique keys against `manuscript/references.bib`. Missing keys: 0 (PASSED).
  - `test_latex_figures_and_tables_bidirectional_consistency()`:
    * Verifies Figures 1 to 7 (`fig:study_area`, `fig:fire_density_frp`, `fig:satellite_canal_forensic`, `fig:tenurial_concession`, `fig:temporal_dynamics`, `fig:model_evaluation`, `fig:shap_importance`) are all defined and explicitly called via `Figure~\ref{...}` in text.
    * Verifies Tables 1 to 4 (`tab:regency_distribution`, `tab:decadal_sipongi`, `tab:model_comparison`, `tab:shap_ranking`) are all defined and called via `Table~\ref{...}` in text.
    * Verifies zero dangling `\ref` calls in LaTeX.
    * Verifies all 7 `\includegraphics` paths resolve to real files on disk.
  - `test_markdown_figures_and_tables_callouts()`:
    * Verifies Tables 1 to 4 have captions and at least 1 in-text body callout.
    * Verifies Figures 1 to 7 have markdown embeds (`![**Figure X...**](...)`) and at least 1 in-text body callout.
    * Verifies all image file paths resolve on disk.
  - `test_docx_figures_and_tables_callouts()`:
    * Verifies Tables 1 to 4 and Figures 1 to 7 are mentioned in DOCX paragraphs with at least 2 occurrences each (caption + callouts).
  - `test_semantic_figure_alignment_no_mismatches()`:
    * Asserts Model Evaluation is strictly associated with Figure 6 (NOT Figure 4 or 5).
    * Asserts TreeSHAP attribution is strictly associated with Figure 7 (NOT Figure 5).
    * Asserts Concession/Tenure is associated with Figure 4.
    * Asserts Canal Forensics is associated with Figure 3.
    Result: PASSED.

### 2.5. `tests/test_document_compilation_rendering.py`
- **Objective**: Programmatically verify end-to-end compilation with Tectonic into `main.pdf` (28 pages, exit code 0) and XML structural integrity of `manuscript_main.docx`.
- **Functions Implemented**:
  - `test_tectonic_compilation()`: Compiles `manuscript/main.tex` with `/opt/homebrew/bin/tectonic`. Asserts exit code == 0, PDF generated, size > 5 MB (10.62 MB).
  - `test_pdf_rendering_and_metadata()`: Uses `/opt/homebrew/bin/pdfinfo` to verify page count == 28, Title, Author, Page Size (A4).
  - `test_docx_structure_and_native_tables()`: Opens `manuscript_main.docx` via `zipfile`/`ElementTree`. Asserts exactly 4 `<w:tbl>` native tables with valid rows/cells. Asserts 0 raw markdown pipes (`| --- |`, `| :--- |`, `|:---|`). Asserts 0 leaking raw markdown/LaTeX markup.
  - `test_docx_omml_math_equations()`: Verifies presence of OMML equations (`<m:oMath>` count >= 50, actual: 132; `<m:oMathPara>` count >= 5, actual: 9).
  - `test_docx_embedded_figures_sha256_match_master()`:
    * Extracts all 7 media files in `word/media/`.
    * Computes SHA-256 for each media file and matches 100% against `output/figures/` master figures (`01_peta_wilayah_studi_spatial_cv.png` through `07_shap_feature_importance.png`).
    * Verifies with `PIL.Image` that all master figures are 300 DPI and high resolution (width >= 3000 px).
    Result: PASSED.

---

## 3. Test Suite Execution Results

Running the complete test suite with `/opt/anaconda3/envs/karhutla_env/bin/pytest`:

```
============================= test session starts ==============================
platform darwin -- Python 3.10.22, pytest-9.2.0, pluggy-1.7.0 -- /opt/anaconda3/envs/karhutla_env/bin/python3.10
cachedir: .pytest_cache
rootdir: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis
collected 25 items

tests/test_abstract_word_count.py::test_latex_abstract_word_count PASSED [  4%]
tests/test_abstract_word_count.py::test_markdown_abstract_word_count PASSED [  8%]
tests/test_abstract_word_count.py::test_docx_abstract_word_count PASSED  [ 12%]
tests/test_abstract_word_count.py::test_pdf_abstract_word_count PASSED   [ 16%]
tests/test_abstract_word_count.py::test_abstract_cross_format_consistency PASSED [ 20%]
tests/test_highlights_length.py::test_markdown_highlights_count PASSED   [ 24%]
tests/test_highlights_length.py::test_markdown_highlights_character_length PASSED [ 28%]
tests/test_highlights_length.py::test_docx_highlights_count PASSED       [ 32%]
tests/test_highlights_length.py::test_docx_highlights_character_length PASSED [ 36%]
tests/test_highlights_length.py::test_highlights_cross_format_parity PASSED [ 40%]
tests/test_keywords_alignment.py::test_latex_keywords_count PASSED       [ 44%]
tests/test_keywords_alignment.py::test_markdown_keywords_count PASSED    [ 48%]
tests/test_keywords_alignment.py::test_docx_keywords_count PASSED        [ 52%]
tests/test_keywords_alignment.py::test_keywords_exact_alignment_with_applied_geography PASSED [ 56%]
tests/test_keywords_alignment.py::test_keywords_cross_format_parity PASSED [ 60%]
tests/test_reference_figure_callout_consistency.py::test_latex_bibtex_citations_resolve PASSED [ 64%]
tests/test_reference_figure_callout_consistency.py::test_latex_figures_and_tables_bidirectional_consistency PASSED [ 68%]
tests/test_reference_figure_callout_consistency.py::test_markdown_figures_and_tables_callouts PASSED [ 72%]
tests/test_reference_figure_callout_consistency.py::test_docx_figures_and_tables_callouts PASSED [ 76%]
tests/test_reference_figure_callout_consistency.py::test_semantic_figure_alignment_no_mismatches PASSED [ 80%]
tests/test_document_compilation_rendering.py::test_tectonic_compilation PASSED [ 84%]
tests/test_document_compilation_rendering.py::test_pdf_rendering_and_metadata PASSED [ 88%]
tests/test_document_compilation_rendering.py::test_docx_structure_and_native_tables PASSED [ 92%]
tests/test_document_compilation_rendering.py::test_docx_omml_math_equations PASSED [ 96%]
tests/test_document_compilation_rendering.py::test_docx_embedded_figures_sha256_match_master PASSED [100%]

============================= 25 passed in 55.02s ==============================
```

All 25 tests passed with 100% exit code 0.
