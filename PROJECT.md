# Project: Evaluasi Riset Karhutla Kalteng & Manuskrip Publikasi Scopus Q1

## Architecture
- **Konteks Riset**: Analisis spasiotemporal pemodelan intensitas karhutla di lahan gambut tropis Kalimantan Tengah, mengatasi autokorelasi spasial (*spatial memorization*) dan tata kelola tenurial lahan.
- **Data Sumber**:
  - Satelit NASA FIRMS VIIRS/MODIS (43.937 titik terkalibrasi di Kalteng)
  - Jaringan Kanal Eks-PLG (13 LineString primer dalam proyeksi UTM 49S `EPSG:32749`)
  - Batas Administrasi Resmi geoBoundaries ADM2 (14 Kabupaten/Kota)
  - Peta Kubah Gambut BBLSDLP 2019
  - Poligon Konsesi Riil (627 HGU Sawit & 185 PBPH Kehutanan)
  - Data Historis Luasan Karhutla SiPongi KLHK (2018–2026)
  - Data Cuaca Reanalisis ERA5-Land
- **Model Inti**:
  - Model A (Baseline): Random Forest dengan koordinat geodetik (mengalami *spatial memorization overfitting*; F1 spasial anjlok ke 0,0583 dan 0,0000 di 4 fold).
  - Model B (Utama): Random Forest *Pure Biophysical* tanpa koordinat (Holdout ROC-AUC 0,7527, F1 spasial 0,1399 konsisten positif di semua 5 fold, Recall ekstrem 65,82%).
- **Aliran Dokumen**:
  1. Survey & Analisis Awal (Fase 0) -> Selesai.
  2. Peer Review Report (`output/reports/review_report.md`) -> Selesai & Lulus Gate M1 (434 baris, Bahasa Indonesia standar Senior Reviewer Q1).
  3. Manuskrip Ilmiah LaTeX (`manuscript/`) -> Selesai & Lulus Gate M2 (Bahasa Inggris akademik, IMRaD modular, integrasi 7 figur ilmiah 300 DPI, `references.bib` 40 entri, sub-bab Section 4.4 Study Limitations, terkompilasi bebas galat menjadi `manuscript/main.pdf` 26 halaman).
  4. Verifikasi Statis & Audit Integritas Forensik (M3) -> Selesai & Terverifikasi CLEAN.

## Feature Inventory
| # | Feature / Deliverable | Description | Milestone | Source | Status |
|---|-----------------------|-------------|-----------|--------|:------:|
| 1 | Evaluasi Metodologis Spatial Block CV | Analisis kegagalan Model A (spatial memorization) vs keunggulan generalisasi Model B | M1 | Survey E1/E3 | DONE |
| 2 | Evaluasi Metodologis Class Imbalance | Analisis target api ekstrem ($FRP \ge 12\text{ MW}$, 15,1%), balanced weights, trade-off Precision 92% vs Recall 65,8% | M1 | Survey E1/E3 | DONE |
| 3 | Evaluasi Validitas & Keterbatasan | Pembahasan threats to internal, external, construct validity (resolusi cuaca, sensor FRP, krisis Oktober 2026) | M1 | Survey E3 | DONE |
| 4 | Laporan Peer Review Formal | Dokumen terstruktur 6 bagian dalam Bahasa Indonesia berbobot Senior Reviewer di `output/reports/review_report.md` | M1 | ORIGINAL_REQUEST R1 | DONE |
| 5 | Pembaruan Bibliografi BibTeX | Penambahan 10 literatur bereputasi tinggi 2021–2025 ke `manuscript/references.bib` (total 40 entri aktif) | M2 | Survey E2 | DONE |
| 6 | Naskah LaTeX Format Scopus Q1 | Naskah IMRaD lengkap di `manuscript/main.tex` & `manuscript/sections/` berstandar MDPI / standar akademik Q1 | M2 | ORIGINAL_REQUEST R2 | DONE |
| 7 | Integrasi 7 Figur Ilmiah | Penyisipan Figures 1 s.d. 7 (`01_` s.d. `07_`) dengan caption ilmiah komprehensif tanpa ASCII art | M2 | ORIGINAL_REQUEST R2 | DONE |
| 8 | Sub-bab Keterbatasan Riset (Section 4.4) | Pembahasan jujur dan mendalam terkait limitasi spasial, cuaca, dan data tanpa mengubah data empiris riil | M2 | ORIGINAL_REQUEST R2 | DONE |
| 9 | Verifikasi Statis Bebas Galat | Validasi sintaks LaTeX, 100% resolusi sitasi `\cite{}`, referensi `\ref{}`, dan keberadaan file figur | M3 | Acceptance Criteria | DONE |
| 10 | Audit Integritas Forensik | Verifikasi keaslian metrik empiris, ketiadaan plagiasi, dan kepatuhan terhadap batasan studi (Vonis CLEAN) | M3 | Acceptance Criteria | DONE |

## Milestones
| # | Name | Scope | Dependencies | Status |
|---|------|-------|-------------|:------:|
| M0 | Survey & Scoping | Pemetaan metrik empiris, kode, draf manuskrip, bibliografi, dan figur ilmiah | none | DONE |
| M1 | Peer Review Report (R1) | Penyusunan laporan peer review formal komprehensif di `output/reports/review_report.md` (Bahasa Indonesia) | M0 | DONE |
| M2 | Publication-Ready LaTeX Manuscript (R2) | Penyusunan naskah IMRaD lengkap siap publikasi dalam format LaTeX standar Scopus Q1, penataan 7 figur, pembaruan `references.bib`, kompilasi PDF | M1 | DONE |
| M3 | Static Verification & Forensic Audit | Validasi statis integritas LaTeX, cross-references, BibTeX keys, dan audit integritas forensik (Vonis CLEAN) | M2 | DONE |

## Code Layout
- `output/reports/review_report.md`: Laporan telaah sejawat (peer review) formal dalam Bahasa Indonesia (SELESAI - 434 baris).
- `manuscript/`:
  - `main.tex`: Berkas naskah utama LaTeX (SELESAI).
  - `sections/`: Berkas bab modular (`00_abstract.tex`, `01_introduction.tex`, `02_materials_methods.tex`, `03_results.tex`, `04_discussion.tex`, `05_conclusions.tex`) (SELESAI).
  - `references.bib`: Berkas bibliografi BibTeX (40 entri valid bereputasi tinggi) (SELESAI).
  - `main.pdf`: Dokumen cetak naskah PDF 26 halaman terkompilasi bebas galat (SELESAI - 2,14 MB).
- `tests/`:
  - `verify_latex.py`: Skrip verifikasi statis kelayakan naskah LaTeX (0 error, 0 warning).
  - `test_empirical_metrics.py`: Skrip verifikasi metrik empiris model (100% match).
  - `check_latex_metrics.py`: Skrip verifikasi konsistensi numerik teks naskah (100% pass).
- `output/figures/`:
  - `01_tren_tahunan_el_nino.png` -> Figure 1
  - `02_heatmap_musiman_bulan.png` -> Figure 2
  - `03_peringkat_kabupaten_terparah.png` -> Figure 3
  - `04_analisis_gambut_dan_kanal.png` -> Figure 4
  - `05_status_konsesi_esg.png` -> Figure 5
  - `06_evaluasi_model_ml.png` -> Figure 6
  - `07_shap_feature_importance.png` -> Figure 7
