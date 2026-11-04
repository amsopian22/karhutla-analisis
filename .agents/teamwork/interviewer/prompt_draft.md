Evaluate existing research results and manuscript draft, perform a thorough peer review identifying strengths and weaknesses, and produce a publication-ready LaTeX draft meeting Scopus Q1 journal standards.

Working directory: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis
Integrity mode: demo
The team must NOT: modify real empirical metrics from experiment results, copy external text without valid citations, or omit methodological limitations in the discussion.

## Requirements

### R1. Comprehensive Peer Review & Methodological Evaluation
Conduct a rigorous scientific evaluation of the existing research outputs, including the draft manuscript (`manuscript/manuscript_draft.md`), empirical metrics (`output/reports/model_metrics.json`), scientific figures (`output/figures/01_tren_tahunan_el_nino.png` through `07_shap_feature_importance.png`), and analysis scripts (`src/`). Produce a structured peer review report in `output/reports/review_report.md` written in Indonesian with the rigor of a Senior Journal Reviewer, detailing strengths, methodological weaknesses (specifically addressing spatial cross-validation, spatial memorization, and class imbalance), threats to validity, and concrete recommendations.

### R2. Publication-Ready LaTeX Manuscript
Prepare a complete, publication-ready scientific manuscript written in academic English formatted in LaTeX targeting Scopus Q1 journal standards (such as MDPI Remote Sensing or modular academic format, determined by the team based on manuscript fit). The manuscript must address the review findings by incorporating a thorough discussion of methodological limitations without altering the underlying empirical data. It must integrate all 7 scientific figures (`01_` to `07_`) with descriptive captions, and link all references to `manuscript/references.bib`.

## Acceptance Criteria

### Review Report Deliverable
- [ ] `output/reports/review_report.md` exists and contains a thorough peer review in structured Indonesian covering strengths, methodological limitations (spatial block CV, spatial memorization, data imbalance), and publication readiness.

### Manuscript Structure & Content
- [ ] A complete LaTeX manuscript file is created in academic English adhering to standard IMRaD structure (Title, Abstract, Introduction, Materials and Methods, Results, Discussion, Conclusion).
- [ ] Methodological limitations identified in the review are explicitly analyzed and discussed within the Discussion / Limitations section of the manuscript.
- [ ] All 7 scientific figures from `output/figures/` (`01_` to `07_`) are referenced in the text and embedded using LaTeX figure environments with comprehensive captions.
- [ ] All bibliographic citations in the LaTeX text correspond to valid keys present in `manuscript/references.bib` with zero undefined citation keys.

### LaTeX Verification
- [ ] Static validation confirms that LaTeX syntax is well-formed, all referenced labels, figures, and BibTeX keys resolve properly without errors or missing references.
