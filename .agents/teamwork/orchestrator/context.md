# Context: Evaluasi Riset Karhutla Kalteng & Penulisan Naskah LaTeX

## Latar Belakang Proyek
Proyek ini mengkaji kebakaran hutan dan lahan (karhutla) di Provinsi Kalimantan Tengah menggunakan data satelit NASA FIRMS (2019-2026), data resmi luasan SiPongi KLHK, jaringan kanal eks-PLG (Proyek Lahan Gambut), batas administrasi geoBoundaries 14 kabupaten/kota, serta status konsesi sawit dan kehutanan (PBPH).
Penelitian telah menghasilkan model prediktif (Random Forest), analisis SHAP, simulasi dispersi asap atmosferik, dan visualisasi berstandar tinggi.

## Artefak Kunci yang Tersedia
- `manuscript/manuscript_draft.md`: Draf naskah penelitian yang sudah disusun.
- `manuscript/references.bib`: Daftar referensi bibliografi dalam format BibTeX.
- `output/reports/model_metrics.json`: Metrik evaluasi empiris model (Model A vs Model B, Spatial GroupKFold CV vs Random CV, Precision, Recall, F1, ROC-AUC).
- `output/reports/eda_summary.json` & `eda_report.md`: Ringkasan temuan EDA dan statistik deskriptif.
- `output/figures/`:
  - `01_tren_tahunan_el_nino.png`
  - `02_heatmap_musiman_bulan.png`
  - `03_peringkat_kabupaten_terparah.png`
  - `04_analisis_gambut_dan_kanal.png`
  - `05_status_konsesi_esg.png`
  - `06_evaluasi_model_ml.png`
  - `07_shap_feature_importance.png`
- `src/`: Skrip Python analisis dan pemodelan (`process_real_data.py`, `spatial_join_concessions.py`, `eda_kalteng.py`, `train_model.py`, dll.)

## Aturan Khusus & Integritas
- Tidak mengubah metrik empiris nyata dari hasil eksperimen.
- Mengakui dan mendiskusikan secara mendalam keterbatasan metodologis (spatial cross-validation, spatial memorization, dan data imbalance).
- Semua sitasi LaTeX harus merujuk pada `manuscript/references.bib`.
- Lingkungan eksekusi Python: conda `karhutla_env` (/opt/anaconda3/envs/karhutla_env/bin/python).
