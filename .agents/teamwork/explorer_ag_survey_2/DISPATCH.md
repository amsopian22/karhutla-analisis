## 2026-11-04T06:54:02Z
You are explorer_ag_survey_2, a teamwork_explorer agent.
Your working directory is: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_2/
You must read your instructions and original request file.

MANDATORY: You must read ORIGINAL_REQUEST.md located at:
/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/ORIGINAL_REQUEST.md
Do not start work until you have read that file.

Scope and Objective:
Perform an in-depth audit of the manuscript text, academic English quality, and thematic alignment for Elsevier's *Applied Geography* (Impact Factor: 7.4, CiteScore: 8.3, Scopus Q1):
1. Context & Scope Reframing:
   - The manuscript previously received an out-of-scope desk rejection from Ecological Modelling.
   - It must be reframed to strongly emphasize Applied Spatial Geography, GIScience, Tobler's First Law ("everything is related to everything else, but near things are more related than distant things"), Spatial Autocorrelation mitigation (Spatial Block CV), and Land Tenure Governance (APL / non-concession vs concessions).
   - Check where and how each section (`manuscript/manuscript_draft.md` and `manuscript/sections/*.tex`: 01_introduction, 02_materials_methods, 03_results, 04_discussion, 05_conclusions) and `manuscript/cover_letter.md` must be enhanced with spatial geographic literature, terminology, and concepts.
2. Thematic Anchors:
   - Tobler's First Law & Spatial Autocorrelation: How Model A suffers from spatial memorization (geodetic coordinates overfitting) while Model B (Pure Biophysical) generalizes across spatial blocks.
   - Land Tenure Geography: The critical spatial finding that 75.4% of fire hotspots occur on unallocated public lands (Area Penggunaan Lain - APL) rather than formal corporate concessions (oil palm 19.3%, forestry PBPH 5.3%), revealing tenure governance voids.
   - Canal drainage vectors: 13 primary canal line vectors in the Ex-Mega Rice Project (PLG) and distance-to-canal decay effect on fire radiative power.
   - Applied Policy & Spatial Planning: Rewetting, spatial zoning, and fire prevention prioritization in high-risk geographic clusters.
3. Academic English & Scientific Tone Audit:
   - Evaluate writing fluency, conciseness, precision of terminology, coherence, transitions, and native academic English style.
   - Identify weak phrasing, redundancies, passive voice overuse, or awkward sentences across draft.md, sections/*.tex, and cover_letter.md.
4. Output:
   - Document section-by-section analysis, specific paragraphs needing reframing, and proposed concrete text revisions in:
     `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_2/analysis.md`
   - Provide a structured handoff report in:
     `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_ag_survey_2/handoff.md`
   - Send a completion message to parent when finished.

Constraints:
- You are read-only. DO NOT modify any code or manuscript files.
- Python environment: `/opt/anaconda3/envs/karhutla_env/bin/python` if running any read-only check scripts.
