## 2026-11-04T07:27:24Z
You are worker_ag_m2, a teamwork_worker agent.
Your working directory is: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/worker_ag_m2/

MANDATORY INTEGRITY WARNING:
DO NOT CHEAT. All implementations must be genuine. DO NOT hardcode test results, create dummy/facade implementations, or circumvent the intended task. A teamwork_auditor will independently verify your work. Integrity violations WILL be detected and your work WILL be rejected.

MANDATORY: You must read ORIGINAL_REQUEST.md located at:
/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/ORIGINAL_REQUEST.md
Do not start work until you have read that file.

Input Reports:
- /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/orchestrator_1/SCOPE.md
- /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/worker_ag_m1/handoff.md
- /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_3/analysis.md

Exclusive File Write Ownership:
- `manuscript/submission_package/manuscript_main.docx`
- `manuscript/submission_package/highlights.docx`
- `manuscript/submission_package/cover_letter.docx`
- `manuscript/main.pdf`

Your Objectives for Milestone 2 (M2) Submission Package Compilation & Visual/Tabular Integrity:
1. Regenerate Word Documents via Pandoc:
   - Use `/opt/homebrew/bin/pandoc` to compile `manuscript/submission_package/manuscript_main.docx` from `manuscript/manuscript_draft.md`.
     Configure pandoc with `--citeproc --bibliography=manuscript/references.bib` so that all citations render cleanly without double-brackets.
   - Use pandoc to compile `manuscript/submission_package/highlights.docx` from `manuscript/highlights.md`.
   - Use pandoc to compile `manuscript/submission_package/cover_letter.docx` from `manuscript/cover_letter.md`.
2. Compile and Verify LaTeX PDF:
   - Inside `manuscript/`, run `/opt/homebrew/bin/tectonic main.tex` to compile `manuscript/main.pdf`. Ensure it succeeds with 0 errors and generates the updated 28-page PDF with author-year citations and 7 high-res figures.
3. Tabular, Visual, and Formatting Audit:
   - Verify that all 4 tables in `manuscript_main.docx` render as proper Word XML tables (`<w:tbl>`) without raw markdown pipes (`| --- |`) or ASCII art.
   - Verify that all math equations render cleanly (OMML `<m:oMath>`).
   - Verify that all 7 embedded figures are present, high-resolution (300 DPI from `output/figures/`), and match the numbering in the text.
   - Verify via Python script that the abstract word count in `manuscript_main.docx` is <= 250 words.
4. Output:
   - Write your implementation details to:
     `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/worker_ag_m2/changes.md`
   - Write your handoff report to:
     `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/worker_ag_m2/handoff.md`
   - Send completion message to parent when finished.
