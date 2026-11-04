## 2026-11-04T06:53:48Z
You are explorer_ag_survey_1, a teamwork_spec_miner agent.
Your working directory is: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_1/
You must read your instructions and original request file.

MANDATORY: You must read ORIGINAL_REQUEST.md located at:
/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/ORIGINAL_REQUEST.md
Do not start work until you have read that file.

Scope and Objective:
Mine and verify all formal specifications and requirements for Elsevier's *Applied Geography* (Impact Factor: 7.4, CiteScore: 8.3, Scopus Q1) submission package, and benchmark all existing manuscript files against these specifications:
1. Highlights:
   - Check `manuscript/highlights.md` and `manuscript/submission_package/highlights.docx`.
   - Elsevier Applied Geography rule: 3 to 5 bullet points, each bullet point maximum 85 characters INCLUDING spaces.
   - Measure the exact character length of each bullet point currently. Flag any violations.
2. Abstract:
   - Check `manuscript/sections/00_abstract.tex`, `manuscript/manuscript_draft.md`, and Word document.
   - Elsevier rule: Maximum 250 words.
   - Measure the exact word count currently. Flag if over 250 words.
3. Keywords:
   - Elsevier rule: 1 to 7 keywords.
   - Check existing keywords in `main.tex`, `00_abstract.tex`, and `manuscript_draft.md`. Are they aligned with Applied Geography (spatial geography, GIScience, peatland wildfires, spatial autocorrelation, land tenure, etc.)?
4. Reference & In-text Citation Style:
   - Verify reference formatting required by Applied Geography (Elsevier standard: author-year e.g. APA / Harvard or Elsevier standard). Check `main.tex` bibstyle and `references.bib`.
5. Statements & Front Matter:
   - CRediT authorship statement (`manuscript/credit_statement.md` and in manuscript). Verify roles for Ahmad Sopian and Rahmi Susanti.
   - Declaration of interest / Competing interests.
   - Data availability statement (pointing to GitHub: https://github.com/amsopian22/karhutla-analisis).
   - Cover letter requirements (`manuscript/cover_letter.md`) tailored to Applied Geography.
6. Acceptance Criteria from ORIGINAL_REQUEST.md:
   - Enumerate all editorial guidelines acceptance criteria and produce actionable verification rules.

Constraints:
- You are read-only. DO NOT modify any code or manuscript files.
- Python environment: `/opt/anaconda3/envs/karhutla_env/bin/python` if running any read-only check scripts.
- Write your detailed findings to `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_1/analysis.md`
- Write your final handoff to `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_1/handoff.md`
- Send a completion message to parent when finished.


## 2026-11-04T07:04:47Z
**Context**: Status inquiry - Survey Fase 0
**Content**: Bagaimana perkembangan investigasi spesifikasi Applied Geography? Mohon laporkan status terkini dan hasil temuan Anda.
**Action**: Kirimkan update status singkat atau segera rampungkan handoff.md jika analisis telah selesai.
