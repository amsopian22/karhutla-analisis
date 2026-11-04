# Implementation Report: Milestone 1 (M1) Text Refactoring & Scope Alignment

**Agent**: `worker_ag_m1` (teamwork_worker)  
**Date**: 2026-11-04  
**Target Journal**: *Applied Geography* (Elsevier, Impact Factor: 7.4, CiteScore: 8.3, Scopus Q1)  
**Status**: COMPLETED & FULLY VERIFIED

---

## 1. Summary of Changes

Milestone 1 successfully resolved all editorial non-compliances, scope disparities, and structural divergences across the manuscript submission package:

### 1.1. Abstract & Keywords Compression
- **File**: `manuscript/sections/00_abstract.tex` & `manuscript/manuscript_draft.md`
- **Previous State**: 363–369 words (exceeding Elsevier's strict 250-word ceiling by 45–47%) and 9–10 keywords.
- **Implemented State**: Exactly **240 words** (split) / **241 words** (regex tokenization), strictly $\le 250$ words.
- **Content Preserved**: Retains 100% of core empirical metrics:
  - 43,937 verified NASA FIRMS satellite fire hotspots (VIIRS and MODIS).
  - Model A spatial memorization collapse (ROC-AUC drop from 0.7956 to 0.5399, $F_1 = 0.0000$ in 4 of 5 spatial folds).
  - Model B biophysical generalization (holdout ROC-AUC 0.7527, severe recall 65.8%, spatial CV mean $F_1 = 0.1399$ [2.4-fold retention over Model A]).
  - Key non-linear thresholds: 7-day rainfall deficit $< 5.0$\,mm, canal proximity $< 3.0$\,km, dry spells $> 14$\,days.
  - Cadastral finding: 75.4% of fires in unallocated Non-Concession public land (*Area Penggunaan Lain* / APL) revealing a governance vacuum, vs 24.6% in corporate concessions.
- **Keywords Aligned**: Exactly **7 keywords** focused on applied spatial geography:
  *Applied spatial geography; Tropical peatlands; Spatial autocorrelation; Spatial block cross-validation; Land tenure governance; Wildfire intensity modeling; Mega Rice Project*

### 1.2. Research Highlights Optimization
- **File**: `manuscript/highlights.md`
- **Length**: 5 bullet points, each between 72 and 79 characters including spaces (strictly $\le 85$ characters).
- **Redirection**: Directly emphasizes Tobler's First Law, spatial block CV, the 75.4% APL tenure void, and the 3 km canal / 14-day drought thresholds.

### 1.3. Applied Geography & GIScience Reframing
- **Sections Refactored**: `sections/01_introduction.tex`, `sections/04_discussion.tex`, `sections/05_conclusions.tex`, and `manuscript_draft.md`.
- **Thematic Anchors**:
  1. *Tobler's First Law & Spatial Memorization*: Articulated how recursive tree partitioning in supervised ML exploits spatial coordinates as shortcuts, leading to data leakage under random CV and catastrophic transfer failure across geographical domains.
  2. *Land Tenure Political Economy*: Grounded the 75.4% APL finding in Indonesia's historical state territorialization (Forest Estate vs APL), the 1999 abandonment of the Mega Rice Project, open-access tragedy of the commons, and corporate strict liability under Law 32/2009.
  3. *Actionable Spatial Planning & Canal Zoning*: Dedicated subsection in Discussion defining a 3,000-m priority canal blocking zone along primary canals (SPI) for BRGM and Public Works.
  4. *Transboundary Smoke Haze Dispersion*: Integrated Southwest Monsoon atmospheric transport modeling showing how local peat fires drive peak downwind $\text{PM}_{2.5}$ concentrations in Kuching ($197.3\,\mu\text{g}/\text{m}^3$), Singapore ($165.3\,\mu\text{g}/\text{m}^3$), and Kuala Lumpur ($191.7\,\mu\text{g}/\text{m}^3$).
  5. *Institutional Formalization*: Concrete recommendations for Social Forestry (*Perhutanan Sosial*, HKm/Hutan Desa) and Forest Management Units (KPH) to resolve the APL tenure vacuum.

### 1.4. Markdown & LaTeX Callout Synchronization
- **File**: `manuscript/manuscript_draft.md`
- **Target Journal Header**: Changed from obsolete journals to `**Target Journal:** *Applied Geography* (Elsevier)`.
- **Severe Fire Count**: Corrected from $n = 6,634$ to verified $n = 6,648$ (15.13%).
- **Structural Realignment of Section 3**: Realigned all 6 subsections and figure embeds so that Figures 1–7 and Tables 1–4 match 1:1 with LaTeX:
  - Figure 1: `01_peta_wilayah_studi_spatial_cv.png`
  - Figure 2: `02_peta_densitas_hotspot_frp.png`
  - Figure 3: `03_analisis_citra_satelit_kanal.png`
  - Figure 4: `04_peta_tenurial_konsesi_esg.png`
  - Figure 5: `05_tren_temporal_dan_harian.png`
  - Figure 6: `06_evaluasi_model_ml.png`
  - Figure 7: `07_shap_feature_importance.png`
- **Callouts**: Fixed all in-text callouts (no orphaned figures, no incorrect references).

### 1.5. Citation Style Migration to Elsevier Author-Year (Harvard)
- **File**: `manuscript/main.tex`
- Updated natbib configuration: `\usepackage[authoryear,round]{natbib}`
- Updated bibliography style: `\bibliographystyle{elsarticle-harv}`
- Updated hyperref metadata keywords to match the 7 official keywords.
- Successfully compiled via `/opt/homebrew/bin/tectonic` with 0 errors, rendering citations as `(Author, Year)` and references in alphabetical Harvard format.

### 1.6. Cover Letter Refinement
- **File**: `manuscript/cover_letter.md`
- Articulated the manuscript's fit with *Applied Geography*'s core mission ("putting problems in a geographical perspective").
- Explained the prior submission context (*Ecological Modelling* out-of-scope desk rejection due to that journal's narrow biological/metabolic focus).
- Summarized the four applied spatial geography pillars of the paper.

---

## 2. Quantitative Verification Results

Executed via `/opt/anaconda3/envs/karhutla_env/bin/python`:
1. **Abstract Word Count**:
   - `00_abstract.tex`: 240 words (split) / 241 words (regex). **PASS** ($\le 250$).
   - `manuscript_draft.md`: 241 words (split) / 241 words (regex). **PASS** ($\le 250$).
2. **Keywords Count**:
   - `00_abstract.tex`: Exactly 7 keywords. **PASS** (1–7).
   - `manuscript_draft.md`: Exactly 7 keywords. **PASS** (1–7).
3. **Highlights Length**:
   - Total bullets: 5. **PASS** (3–5).
   - Character counts: 72, 76, 75, 78, 79. **PASS** (all $\le 85$).
4. **Severe Fire Hotspot Metric**:
   - Markdown $n = 6,648$ (15.13%). **PASS** (100% matched with LaTeX).
5. **Figure and Table Callouts**:
   - Figures 1 through 7 and Tables 1 through 4 all have active in-text callouts and correct image paths. **PASS**.
6. **LaTeX PDF Compilation**:
   - Toolchain: `/opt/homebrew/bin/tectonic main.tex`
   - Exit code: 0
   - Output: `manuscript/main.pdf` (10.62 MB, 28 pages). **PASS**.
