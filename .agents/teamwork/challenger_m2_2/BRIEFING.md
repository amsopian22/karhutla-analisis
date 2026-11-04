# BRIEFING — 2026-11-03T03:56:00Z

## Mission
Verifikasi empiris dan audit adversasial terhadap seluruh angka metrik empiris pada naskah publikasi LaTeX Scopus Q1 (manuscript/sections/ 02_materials_methods.tex, 03_results.tex, 04_discussion.tex) terhadap berkas sumber data resmi (output/reports/model_metrics.json, output/reports/eda_summary.json, data master CSV).

## 🔒 My Identity
- Archetype: empirical-challenger
- Roles: critic, specialist
- Working directory: /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/challenger_m2_2
- Original parent: a2eeb2c9-6928-4af1-8dab-de9837521b8d
- Milestone: Milestone 2 (Naskah Publikasi LaTeX Scopus Q1)
- Instance: 2 of 2

## 🔒 Key Constraints
- Review-only — do NOT modify implementation or manuscript code directly
- Must run empirical verification code (generators, oracles, automated consistency checkers)
- Every metric must be 100% verified against raw/processed source files
- No smoothed or fabricated numbers permitted
- Bahasa Indonesia untuk seluruh laporan dan penjelasan

## Current Parent
- Conversation ID: a2eeb2c9-6928-4af1-8dab-de9837521b8d
- Updated: not yet

## Review Scope
- **Files to review**: `manuscript/sections/` (00_abstract.tex, 01_introduction.tex, 02_materials_methods.tex, 03_results.tex, 04_discussion.tex, 05_conclusions.tex, main.tex)
- **Source empirical files**: `output/reports/model_metrics.json`, `output/reports/eda_summary.json`, `data/processed/karhutla_kalteng_2019_2026.csv`, `data/raw/sipongi_luas_karhutla_kalteng_2018_2026.csv`
- **Review criteria**: Exact numerical consistency, adversarial auditing of smoothed/outdated draft numbers, confusion matrix validation, spatial block CV verification.

## Attack Surface
- **Hypotheses tested**:
  - H1: Seluruh angka metrik ML (Model A vs Model B) 100% konsisten dengan `model_metrics.json` -> PARTIALLY CONFIRMED (ROC-AUC, F1, Spatial CV, dan 5 Folds 100% konsisten, namun Holdout Recall Model A di Tabel 4 tertulis 62.4% padahal model riil menghasilkan 66.37%).
  - H2: Matriks konfusi Model B (TN=6.586, FP=2.737, FN=568, TP=1.094) 100% konsisten -> CONFIRMED (100% akurat terhadap data uji 10.985 titik).
  - H3: Angka EDA (43.937 titik, 75.4% APL, 74.3% gambut, median kanal 14.946 m) konsisten -> CONFIRMED untuk metrik agregat makro, tapi FAILED pada rincian kabupaten (Tabel 2) dan dinamika temporal harian.
  - H4: Ketiadaan angka yang dihaluskan/diubah -> FAILED (ditemukan 4 angka/tabel yang disalin dari mock draft lama tanpa sinkronisasi ke dataset riil).
- **Vulnerabilities found**:
  1. Tabel 2 (`03_results.tex`): Angka kabupaten 4–8 dan "Other 6" keliru dan kontradiktif dengan Gambar 3.
  2. Dinamika Harian (`03_results.tex` Baris 47 & 51): Angka 7-8 Okt (18.628 / 42.4%) keliru vs riil (15.667 / 35.66%) dan kontradiktif dengan Gambar 2.
  3. Klaim Median Jarak Kanal Univariat (`03_results.tex` Baris 112): Klaim 8.420 m vs 16.110 m ($p < 0.001$) tidak didukung data riil (median api ekstrem riil = 17.085 m vs reguler 14.571 m, $p = 0.2545$).
  4. Tabel 4 Recall Model A (`03_results.tex` Baris 153): Tertulis 62.4% padahal riil 66.37%.
- **Untested angles**: Analisis dispersi aerosol WRF-Chem/Gauss (tidak dijadikan tabel utama naskah, hanya narasi pendukung).

## Loaded Skills
- None requested

## Key Decisions Made
- Memberikan vonis **REQUEST_CHANGES** karena terdapat kesalahan empiris faktual pada naskah yang bertentangan dengan dataset master dan figur ilmiah yang terpasang di sampingnya.
- Menyusun laporan handoff formal lengkap dengan delta perbaikan baris-per-baris agar tim penulis dapat langsung menerapkan perbaikan presisi.

## Artifact Index
- `DISPATCH.md` — Log pesan masuk
- `BRIEFING.md` — Status kesadaran situasional
- `progress.md` — Heartbeat & log kemajuan
- `tests/verify_empirical_metrics.py` — Skrip verifikasi empiris dataset master
- `tests/check_latex_metrics.py` — Skrip audit otomatis metrik LaTeX vs JSON
- `handoff.md` — Laporan akhir audit adversasial
