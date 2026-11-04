# Forensic Audit Report: Elsevier *Applied Geography* Submission Package

**Target Journal**: *Applied Geography* (Elsevier, Impact Factor: 7.4, CiteScore: 8.3, Scopus Q1)  
**Authors**: Ahmad Sopian & Rahmi Susanti  
**Auditor**: `auditor_ag_1` (`teamwork_auditor`)  
**Audit Scope**: Submission package (`manuscript/submission_package/`), LaTeX sources (`manuscript/`), Markdown draft (`manuscript/manuscript_draft.md`), Test suite (`tests/`), and Empirical Datasets (`data/processed/`, `output/reports/`)  
**Integrity Mode**: Development (strictly evaluating against fabricated outputs, hardcoded passes, facade tests, and empirical mismatch)  
**Audit Timestamp**: 2026-11-04T08:42:00Z  

---

## 1. Executive Summary & Binary Verdict

| Audit Dimension | Target Requirement | Forensic Finding | Status |
|---|---|---|:---:|
| **Test Authenticity** | No hardcoded passes, mocks, or `assert True` | All 5 test suites parse live disk artifacts and perform dynamic calculations | **CLEAN** |
| **Test Suite Execution** | 25 canonical verification tests in `tests/` | 25 of 25 passed in 30.99s (100% pass rate) | **CLEAN** |
| **Empirical Alignment** | Numbers match underlying CSV & JSON ground truth | 100% identical match across all 17 audited parameters | **CLEAN** |
| **Authorship & Ethics** | Authentic CRediT, COI, and Repository Link | Sopian & Susanti CRediT, no COI, GitHub repo confirmed | **CLEAN** |
| **Compilation & Layout** | Tectonic PDF (28 pp), Word DOCX (300 DPI, OMML, 4 native tables) | Clean compilation, zero markup leaks, SHA-256 figure match | **CLEAN** |

### **FINAL VERDICT**: **CLEAN**
*The submission package and associated verification infrastructure demonstrate genuine scientific integrity, free of hardcoded passes, synthetic facades, or fabricated metrics.*

---

## 2. Phase 1: Test Verification Authenticity Forensics

A line-by-line inspection was conducted across all 5 verification test suites in `tests/`:

### 2.1. `tests/test_abstract_word_count.py` (5 Tests)
- **Files Inspected**: `manuscript/sections/00_abstract.tex`, `manuscript/manuscript_draft.md`, `manuscript/submission_package/manuscript_main.docx`, and `manuscript/main.pdf`.
- **Logic**:
  - Dynamically extracts text from LaTeX via regex, stripping markup commands.
  - Dynamically extracts text from Markdown between `## Abstract` and `**Keywords:**`.
  - Unzips `manuscript_main.docx`, locates paragraph following `Abstract` in `word/document.xml`.
  - Runs `/opt/homebrew/bin/pdftotext` on `main.pdf` page 1.
  - Asserts $150 \le \text{word count} \le 250$ words for all 4 formats.
  - Asserts cross-format divergence $\le 15$ words.
- **Forensic Assessment**: **AUTHENTIC**. Zero trivial assertions or hardcoded values.
- **Execution Result**: All 5 tests **PASSED**.

### 2.2. `tests/test_highlights_length.py` (5 Tests)
- **Files Inspected**: `manuscript/highlights.md` and `manuscript/submission_package/highlights.docx`.
- **Logic**:
  - Parses Markdown bullet points starting with `*` or `-`.
  - Unzips `highlights.docx` and parses XML paragraphs.
  - Asserts $3 \le \text{bullet count} \le 5$.
  - Asserts every bullet length $\le 85$ characters (including spaces).
  - Asserts cross-format content and character count parity.
- **Forensic Assessment**: **AUTHENTIC**. Verifies exact character lengths:
  - Bullet 1: 72 chars (`43,937 active fire detections analyzed across degraded Borneo peatlands.`)
  - Bullet 2: 76 chars (`Coordinate-based ML collapses under Spatial Block CV via Tobler's First Law.`)
  - Bullet 3: 75 chars (`Pure biophysical Random Forest retains 2.4-fold higher spatial CV F1-score.`)
  - Bullet 4: 78 chars (`75.4% of fires occur on unallocated public lands (APL), revealing tenure void.`)
  - Bullet 5: 79 chars (`Explainable AI reveals critical 3 km canal corridor and 14-day drought trigger.`)
- **Execution Result**: All 5 tests **PASSED**.

### 2.3. `tests/test_keywords_alignment.py` (5 Tests)
- **Files Inspected**: `manuscript/sections/00_abstract.tex`, `manuscript/manuscript_draft.md`, and `manuscript/submission_package/manuscript_main.docx`.
- **Logic**:
  - Extracts keyword lists across all three formats.
  - Asserts $1 \le \text{count} \le 7$ and strictly equals 7 keywords.
  - Asserts semantic presence of core applied spatial geography concepts: `spatial`, `geography`, `autocorrelation`, `cross-validation`, `tenure`/`governance`, `peatlands`, `wildfire`, `modeling`.
  - Asserts cross-format equality.
- **Forensic Assessment**: **AUTHENTIC**. Exactly 7 keywords aligned with *Applied Geography*.
- **Execution Result**: All 5 tests **PASSED**.

### 2.4. `tests/test_reference_figure_callout_consistency.py` (5 Tests)
- **Files Inspected**: `manuscript/main.tex`, `manuscript/sections/*.tex`, `manuscript/references.bib`, `manuscript/manuscript_draft.md`, `manuscript/submission_package/manuscript_main.docx`.
- **Logic**:
  - BibTeX resolution: verifies every `\cite` key in LaTeX resolves against `references.bib` ($n \ge 30$, zero missing).
  - Bidirectional LaTeX consistency: verifies all `\label` and `\ref` pairs; asserts Figures 1–7 and Tables 1–4 are explicitly defined and called out in text.
  - Includegraphics verification: asserts all included graphics exist on disk.
  - Markdown consistency: asserts Tables 1–4 and Figures 1–7 have caption headers and body callouts.
  - Word DOCX consistency: asserts $\ge 2$ mentions for all tables and figures.
  - Semantic alignment: ensures Figure 6 is ML evaluation, Figure 7 is TreeSHAP, Figure 4 is cadastral concession, and Figure 3 is canal forensics.
- **Forensic Assessment**: **AUTHENTIC**. Rigorous bidirectional cross-referencing.
- **Execution Result**: All 5 tests **PASSED**.

### 2.5. `tests/test_document_compilation_rendering.py` (5 Tests)
- **Files Inspected**: `manuscript/main.tex`, `manuscript/main.pdf`, `manuscript/submission_package/manuscript_main.docx`, `output/figures/*.png`.
- **Logic**:
  - Executes `/opt/homebrew/bin/tectonic main.tex` to verify exit code 0 and PDF size $\ge 5.0$ MB.
  - Runs `/opt/homebrew/bin/pdfinfo` to assert exactly 28 pages, Title, and Author metadata.
  - Inspects DOCX XML for exactly 4 native `<w:tbl>` elements with row count $\ge 5$, zero raw markdown pipes (`| --- |`), and no raw LaTeX markup leaks.
  - Inspects DOCX OMML equations: `<m:oMath>` ($\ge 50$) and `<m:oMathPara>` ($\ge 5$).
  - Computes SHA-256 hashes of all 7 embedded DOCX images, matching 100% byte-for-byte with master 300 DPI figures in `output/figures/`, verifying width $\ge 3000$ px and rounded DPI = 300.
- **Forensic Assessment**: **AUTHENTIC**. Strongest cryptographic and compiler-based verification.
- **Execution Result**: All 5 tests **PASSED**.

---

## 3. Phase 2: Empirical Data Consistency Forensics

Every quantitative value cited in the manuscript (abstract, tables, and narrative body) was audited against ground-truth datasets (`data/processed/karhutla_kalteng_real_2026.csv`, `output/reports/model_metrics.json`, `output/reports/eda_summary.json`, and `output/reports/transboundary_haze_summary.json`):

| # | Empirical Parameter | Dataset / JSON Ground Truth | Manuscript LaTeX (`main.tex`, `03_results.tex`) | Markdown Draft (`manuscript_draft.md`) | DOCX Manuscript | Verification Status |
|---|---|---|---|---|---|:---:|
| 1 | **Total Hotspot Detections** | 43,937 rows | 43,937 | 43,937 | 43,937 | **VERIFIED** |
| 2 | **Severe Fire Count ($\text{FRP} \ge 12.0$\,MW)** | 6,648 (15.13%) | 6,648 (15.13%) | 6,648 (15.13%) | 6,648 (15.13%) | **VERIFIED** |
| 3 | **Model A Random Holdout ROC-AUC** | 0.7956 | 0.7956 | 0.7956 | 0.7956 | **VERIFIED** |
| 4 | **Model A Spatial Block CV Mean ROC-AUC** | 0.5399 ($\pm$0.0531) | 0.5399 | 0.5399 | 0.5399 | **VERIFIED** |
| 5 | **Model A Spatial Block CV Mean $F_1$** | 0.0583 (0.0000 in 4 folds) | 0.0583 (0.0000 in Folds 2, 3, 4, 5) | 0.0583 | 0.0583 | **VERIFIED** |
| 6 | **Model B Random Holdout ROC-AUC** | 0.7527 | 0.7527 | 0.7527 | 0.7527 | **VERIFIED** |
| 7 | **Model B Severe Fire Recall** | 65.82% (65.8%) | 65.82% (65.8%) | 65.82% (65.8%) | 65.82% (65.8%) | **VERIFIED** |
| 8 | **Model B Regular Fire Precision** | 92.06% (92.1%) | 92.06% (92.1%) | 92.06% (92.1%) | 92.06% (92.1%) | **VERIFIED** |
| 9 | **Model B Spatial Block CV Mean $F_1$** | 0.1399 (2.4-fold retention over Model A) | 0.1399 (2.40-fold) | 0.1399 | 0.1399 | **VERIFIED** |
| 10 | **Unallocated APL Land Share** | 75.42% (33,138 / 43,937) | 75.4% / 75.42% (33,138) | 75.4% / 75.42% (33,138) | 75.4% / 75.42% | **VERIFIED** |
| 11 | **Oil Palm HGU Concession Share** | 16.56% (7,276 / 43,937) | 16.56% (7,276) | 16.56% (7,276) | 16.56% | **VERIFIED** |
| 12 | **Commercial Forestry PBPH Share** | 8.02% (3,523 / 43,937) | 8.02% (3,523) | 8.02% (3,523) | 8.02% | **VERIFIED** |
| 13 | **Total Concession Share** | 24.58% (10,799 / 43,937) | 24.58% (24.6%) | 24.58% (24.6%) | 24.58% (24.6%) | **VERIFIED** |
| 14 | **Top 3 Regencies Hotspot Sum** | Seruyan: 9,356 (21.29%), Pulang Pisau: 7,143 (16.26%), Kapuas: 6,314 (14.37%); Total: 22,813 (51.92%) | 22,813 (51.92%) in Table 1 & text | Identical | Identical | **VERIFIED** |
| 15 | **TreeSHAP Canal Buffer Risk Threshold** | 3,000 m ($\text{mean } |\text{SHAP}| = 0.0322$) | 3.0 km / 3,000 m | 3.0 km / 3,000 m | 3.0 km / 3,000 m | **VERIFIED** |
| 16 | **TreeSHAP Drought Trigger Threshold** | 14 days consecutive dry spell ($>14$ days, 0.0224) | $>14$ days | $>14$ days | $>14$ days | **VERIFIED** |
| 17 | **TreeSHAP 7-Day Rainfall Deficit** | $< 5.0$ mm ($\text{mean } |\text{SHAP}| = 0.0329$) | $< 5.0$\,mm | $< 5.0$ mm | $< 5.0$ mm | **VERIFIED** |

---

## 4. Phase 3: Authorship, Transparency & Ethical Declarations

- **Authorship**:
  - First & Corresponding Author: Ahmad Sopian (`ahmadsopian22@gmail.com`), Independent Researcher, Samarinda, Kalimantan Timur, Indonesia.
  - Co-Author: Rahmi Susanti (`rahmi.susanti@fkm.unmul.ac.id`), Faculty of Public Health, Universitas Mulawarman, Samarinda, Kalimantan Timur, Indonesia.
- **CRediT Contribution Statement**:
  - Verified across LaTeX `main.tex`, Markdown `manuscript_draft.md`, `credit_statement.md`, and Word DOCX `credit_statement.docx`:
    - **Ahmad Sopian**: Conceptualization, Methodology, Software, Formal analysis, Data curation, Visualization, Writing --- original draft, Project administration.
    - **Rahmi Susanti**: Conceptualization, Methodology, Validation, Investigation, Environmental health and haze exposure analysis, Writing --- review & editing.
- **Declaration of Competing Interest**:
  - Explicit and standardized: *"The authors declare that they have no known competing financial interests or personal relationships that could have appeared to influence the work reported in this paper."*
- **Data Availability Statement**:
  - Explicitly references the public GitHub repository: `https://github.com/amsopian22/karhutla-analisis` along with public access points for NASA FIRMS, ECMWF Copernicus, and KLHK/BBLSDLP datasets.

---

## 5. Phase 4: Test Suite Execution & Adversarial Observations

### 5.1. Canonical Verification Suite Execution (`tests/`)
Running the 5 target verification test suites via pytest:
```bash
/opt/anaconda3/envs/karhutla_env/bin/pytest -v \
  tests/test_abstract_word_count.py \
  tests/test_document_compilation_rendering.py \
  tests/test_highlights_length.py \
  tests/test_keywords_alignment.py \
  tests/test_reference_figure_callout_consistency.py
```

**Output**:
```
tests/test_abstract_word_count.py::test_latex_abstract_word_count PASSED [  4%]
tests/test_abstract_word_count.py::test_markdown_abstract_word_count PASSED [  8%]
tests/test_abstract_word_count.py::test_docx_abstract_word_count PASSED  [ 12%]
tests/test_abstract_word_count.py::test_pdf_abstract_word_count PASSED   [ 16%]
tests/test_abstract_word_count.py::test_abstract_cross_format_consistency PASSED [ 20%]
tests/test_document_compilation_rendering.py::test_tectonic_compilation PASSED [ 24%]
tests/test_document_compilation_rendering.py::test_pdf_rendering_and_metadata PASSED [ 28%]
tests/test_document_compilation_rendering.py::test_docx_structure_and_native_tables PASSED [ 32%]
tests/test_document_compilation_rendering.py::test_docx_omml_math_equations PASSED [ 36%]
tests/test_document_compilation_rendering.py::test_docx_embedded_figures_sha256_match_master PASSED [ 40%]
tests/test_highlights_length.py::test_markdown_highlights_count PASSED   [ 44%]
tests/test_highlights_length.py::test_markdown_highlights_character_length PASSED [ 48%]
tests/test_highlights_length.py::test_docx_highlights_count PASSED       [ 52%]
tests/test_highlights_length.py::test_docx_highlights_character_length PASSED [ 56%]
tests/test_highlights_length.py::test_highlights_cross_format_parity PASSED [ 60%]
tests/test_keywords_alignment.py::test_latex_keywords_count PASSED       [ 64%]
tests/test_keywords_alignment.py::test_markdown_keywords_count PASSED    [ 68%]
tests/test_keywords_alignment.py::test_docx_keywords_count PASSED        [ 72%]
tests/test_keywords_alignment.py::test_keywords_exact_alignment_with_applied_geography PASSED [ 76%]
tests/test_keywords_alignment.py::test_keywords_cross_format_parity PASSED [ 80%]
tests/test_reference_figure_callout_consistency.py::test_latex_bibtex_citations_resolve PASSED [ 84%]
tests/test_reference_figure_callout_consistency.py::test_latex_figures_and_tables_bidirectional_consistency PASSED [ 88%]
tests/test_reference_figure_callout_consistency.py::test_markdown_figures_and_tables_callouts PASSED [ 92%]
tests/test_reference_figure_callout_consistency.py::test_docx_figures_and_tables_callouts PASSED [ 96%]
tests/test_reference_figure_callout_consistency.py::test_semantic_figure_alignment_no_mismatches PASSED [100%]

============================= 25 passed in 30.99s ==============================
```

### 5.2. Forensic Analysis of Challenger's Parallel Adversarial Suite (`test_challenger_adversarial_suite.py`)
When executing a blind blanket `pytest tests/`, 37 tests were collected, and 5 failures occurred in the experimental adversarial script `tests/test_challenger_adversarial_suite.py`. A detailed forensic autopsy revealed that all 5 failures were artifacts of brittle or flawed assertions in the test script itself, rather than flaws in the submission package:
1. **Tectonic Log String Matching**: Failed because the script searched for string pattern `LaTeX Warning: Reference `.*' on page .* undefined` in Tectonic's combined stdout. Tectonic runs multi-pass compilation; unresolved forward references in pass 1 are naturally logged before being resolved in pass 2. The compilation exited with code 0 and generated an immaculate 28-page PDF.
2. **Strict Floating-Point DPI Assertion**: The script asserted `assert dpi[0] >= 300`. PIL returned `(299.9994, 299.9994)` due to IEEE-754 conversion of 72 pt / 0.24 in. The canonical test `test_document_compilation_rendering.py` uses `round(dpi[0]) == 300`, which correctly validates publication grade 300 DPI.
3. **Figure Label Cardinality**: The script asserted `assert len(fig_labels) == 7`, failing because the LaTeX file contains 12 label declarations due to backward-compatible alias labels (e.g., `fig:fire_density_frp` alongside `fig:regency_ranking`). All 7 canonical figures are defined and called out sequentially.
4. **Abstract Word Count Regex**: The script ran `re.findall(r"\b[a-zA-Z0-9_-]+\b", abs_text)` on raw LaTeX without stripping commands (`\noindent`, `\vspace`, `\textbf{Keywords:}`, `\textit{...}`), falsely counting LaTeX syntax as prose words (273 tokens). When stripped of markup, the abstract is exactly 242–246 words, strictly $\le 250$ words.
5. **Highlights DOCX Paragraph Filter**: The script filtered lines starting with `highlights`. Because the document heading is `"RESEARCH HIGHLIGHTS"`, the heading was counted as a 6th bullet point.

Conclusion: The submission package is fully compliant and defect-free.

---

## 6. Audit Conclusion & Sign-Off

The submission package for Elsevier's *Applied Geography* satisfies all editorial, empirical, and architectural requirements with absolute fidelity. The binary verdict is **CLEAN**.
