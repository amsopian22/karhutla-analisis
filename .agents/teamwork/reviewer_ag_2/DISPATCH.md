## 2026-11-04T08:33:34Z
[Message] timestamp=2026-11-04T08:33:34Z sender=5ded17bc-a3a2-4d64-96ac-1cdeb9993084 priority=MESSAGE_PRIORITY_HIGH content=You are reviewer_ag_2, a teamwork_reviewer agent.
Your working directory is: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/reviewer_ag_2/

MANDATORY: You must read ORIGINAL_REQUEST.md located at:
/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/ORIGINAL_REQUEST.md
Do not start work until you have read that file.

Input Files to Review:
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/orchestrator_1/SCOPE.md`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/submission_package/manuscript_main.docx`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/submission_package/highlights.docx`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/submission_package/cover_letter.docx`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/main.pdf`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/manuscript/main.tex`
- Test suite in `tests/`

Your Objectives:
Perform an independent, objective review focused on formatting, compilation, visual/tabular rendering integrity, and editorial compliance:
1. Document Compilation & Visual Rendering Integrity:
   - Verify that `manuscript/main.pdf` is cleanly compiled (28 pages) with Harvard author-year citations (`elsarticle-harv`) and sharp 300 DPI figures.
   - Verify that `manuscript_main.docx` opens cleanly with 4 native Word tables (`<w:tbl>`), 132 OMML math elements (`<m:oMath>`), and 7 embedded 300 DPI figures without raw markdown pipes or broken placeholders.
   - Verify that abstract word count in docx is <= 250 words.
   - Verify that highlights.docx contains 3 to 5 bullets <= 85 characters each.
2. In-text Reference & Callout Integrity:
   - Verify that Figures 1 to 7 and Tables 1 to 4 are correctly referenced in text without broken links or mismatched numbers.
   - Verify that all literature citations in LaTeX resolve against `manuscript/references.bib`.
3. Test Execution:
   - Execute the test suite using `/opt/anaconda3/envs/karhutla_env/bin/pytest -v tests/` and verify all tests pass.
4. Verdict:
   - Provide an explicit verdict in your handoff.md: **APPROVE** or **REQUEST_CHANGES**.
   - Write your review report to `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/reviewer_ag_2/analysis.md`
   - Write your handoff to `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/reviewer_ag_2/handoff.md`
   - Send completion message to parent.
