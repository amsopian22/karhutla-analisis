# LAPORAN PENGUJIAN EMPIRIS (HANDOFF REPORT) — CHALLENGER 1 (MILESTONE 1)

**Tanggal**: 3 November 2026  
**Agen Penguji**: Challenger 1 (`challenger_m1_1`)  
**Peran**: EMPIRICAL CHALLENGER (critic, specialist)  
**Dokumen yang Diuji**: `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/review_report.md`  
**Sumber Kebenaran Empiris**:
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/model_metrics.json`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/eda_summary.json`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/data/processed/karhutla_kalteng_2019_2026.csv`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/models/karhutla_rf_model.joblib`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/src/train_model.py`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/src/process_real_data.py`
- `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/figures/` (01 s.d. 07)

---

## 1. Observation (Observasi Empiris Langsung)

Pengujian empiris independen dijalankan menggunakan interpreter Python lingkungan conda resmi:
`/opt/anaconda3/envs/karhutla_env/bin/python` melalui dua skrip uji: `tests/test_empirical_metrics.py` dan `tests/audit_review_report_numbers.py`.

### 1.1. Metrik Model Machine Learning (Tabel 3 & Baris 100–121 di `review_report.md`)
Hasil pembacaan langsung dari `model_metrics.json` dan hasil reproduksi inferensi ulang model dari `output/models/karhutla_rf_model.joblib` pada data uji holdout ($n = 10.985$):
- **Model A (Baseline Hafalan Spasial / 15 Fitur)**:
  - Holdout Test ROC-AUC: `0,7956` (verbatim `review_report.md` L103: `0,7956`)
  - Holdout Test F1-Score: `0,4512` (verbatim `review_report.md` L104: `0,4512`)
  - Spatial Block CV Mean ROC-AUC: `0,5399` ($\pm$ `0,0531`) (verbatim L107)
  - Spatial Block CV Mean F1-Score: `0,0583` (verbatim L108)
  - Detail Fold 1 s.d. 5 Spatial CV Model A:
    - Fold 1 (Seruyan): ROC-AUC `0,5955`, F1 `0,2913` (verbatim L115)
    - Fold 2 (Pulpis, Bartim, Barut, Lamandau, Mura): ROC-AUC `0,5125`, F1 `0,0000` (verbatim L116)
    - Fold 3 (Kapuas, Barsel, Gumas, Sukamara): ROC-AUC `0,5259`, F1 `0,0000` (verbatim L117)
    - Fold 4 (Katingan, Palangka Raya): ROC-AUC `0,4622`, F1 `0,0000` (verbatim L118)
    - Fold 5 (Kobar, Kotim): ROC-AUC `0,6034`, F1 `0,0000` (verbatim L119)
- **Model B (Pure Biophysical / 12 Fitur)**:
  - Holdout Test ROC-AUC: `0,7527` (verbatim L103)
  - Holdout Test F1-Score: `0,3983` (verbatim L104)
  - Precision Reguler ($FRP < 12\text{ MW}$): `92,06%` $\to$ dibulatkan `92,1%` (verbatim L105)
  - Recall Ekstrem ($FRP \ge 12\text{ MW}$): `65,82%` (verbatim L106)
  - Spatial Block CV Mean ROC-AUC: `0,4950` ($\pm$ `0,0490`) (verbatim L107)
  - Spatial Block CV Mean F1-Score: `0,1399` (verbatim L108, rasio keunggulan $0,1399 / 0,0583 = 2,40\times$)
  - Detail Fold 1 s.d. 5 Spatial CV Model B:
    - Fold 1: ROC-AUC `0,5827`, F1 `0,2914` (verbatim L115)
    - Fold 2: ROC-AUC `0,5041`, F1 `0,0657` (verbatim L116)
    - Fold 3: ROC-AUC `0,4900`, F1 `0,1056` (verbatim L117)
    - Fold 4: ROC-AUC `0,4452`, F1 `0,0646` (verbatim L118)
    - Fold 5: ROC-AUC `0,4533`, F1 `0,1722` (verbatim L119)

### 1.2. Matriks Konfusi dan Aritmetika Ketimpangan Kelas (Baris 144–163 di `review_report.md`)
Kalkulasi empiris dari `confusion_matrix(y_test, y_pred_b)` pada $n = 10.985$:
- $\text{TN} = 6.586$, $\text{FP} = 2.737$, $\text{FN} = 568$, $\text{TP} = 1.094$ (Total = $10.985$).
- $\text{Recall}_{\text{ekstrem}} = \frac{1094}{1094 + 568} = \frac{1094}{1662} = 65,8243\% \to 65,82\%$.
- $\text{Precision}_{\text{ekstrem}} = \frac{1094}{1094 + 2737} = \frac{1094}{3831} = 28,5565\% \to 28,56\%$.
- $\text{Precision}_{\text{reguler}} = \frac{6586}{6586 + 568} = \frac{6586}{7154} = 92,0603\% \to 92,06\% \approx 92,1\%$.
- $\text{F1}_{\text{holdout}} = 2 \times \frac{0,285565 \times 0,658243}{0,285565 + 0,658243} = 0,39832 \to 0,3983$.
- Pembobotan `class_weight='balanced'`:
  - $N = 43.937$, $n_1 = 6.648$ ($15,13\%$), $n_0 = 37.289$ ($84,87\%$).
  - $w_1 = \frac{43937}{2 \times 6648} = 3,3045$ (verbatim L146).
  - $w_0 = \frac{43937}{2 \times 37289} = 0,5891$ (verbatim L148).

### 1.3. Parameter Biofisik dan Tata Kelola Lahan (EDA)
Pengujian langsung terhadap `data/processed/karhutla_kalteng_2019_2026.csv` ($N = 43.937$ baris):
- **Proporsi Gambut**: 32.643 titik dari 43.937 = `74,30%` (verbatim `74,3%` di L4, L203, L416).
- **Kubah Gambut Dalam (> 200 cm)**: 23.085 titik = `52,54%` (verbatim `52,5%` di L203).
- **Distribusi Status Konsesi**:
  - Non-Konsesi (APL / Lahan Terbuka): 33.138 titik = `75,42%` (verbatim `75,4%` / `33.138` di L33, L64, L204).
  - Konsesi Perkebunan Sawit (HGU): 7.276 titik = `16,56%` (verbatim `16,6%` / `7.276` di L65, L204).
  - Konsesi Kehutanan (PBPH): 3.523 titik = `8,02%` (verbatim `8,0%` / `3.523` di L66, L204).
  - Jumlah total titik: $33.138 + 7.276 + 3.523 = 43.937$ (100% tepat).
- **Jarak Kanal Eks-PLG**: Median jarak ke vektor garis 13 poros kanal SPI eks-PLG dalam proyeksi metrik UTM Zone 49S ($EPSG:32749$) pada lanskap eks-PLG ($n = 16.645$) adalah `14.946 m` (~`14,9 km`) (verbatim L59, L203).
- **Top 3 Kabupaten**:
  - Seruyan: 9.358 titik (`21,29%` $\to$ `21,3%`)
  - Pulang Pisau: 7.143 titik (`16,26%` $\to$ `16,3%`)
  - Kapuas: 6.314 titik (`14,37%` $\to$ `14,4%`)
  - Kumulatif Top 3: 22.813 titik (`51,92%` $\to$ `51,9%`) (verbatim L202).
- **Filtrasi Batas Administrasi**: 52.829 titik mentah bounding box NASA FIRMS disaring batas resmi Kalteng geoBoundaries ADM2, membersihkan 8.892 titik (`16,83%`) luar provinsi sehingga menyisakan 43.937 titik (verbatim L31, L51).
- **Catatan Historis SiPongi KLHK**: 2019 seluas `317.749 ha`, 2023 seluas `165.896 ha` (verbatim L52, L200, L349).

### 1.4. Pemeringkatan Feature Importance TreeSHAP
Semua nilai atribusi marjinal pada L74–L78 dan Table 4 sesuai persis dengan array `shap_importance_ranking` pada `model_metrics.json`:
1. Curah Hujan 7H (`curah_hujan_7h_mm`): `0,0329`
2. Jarak Kanal Eks-PLG (`jarak_kanal_m`): `0,0322`
3. Kecepatan Angin (`kecepatan_angin_kmh`): `0,0254`
4. Hari Tanpa Hujan (`dry_spell_days`): `0,0224`
5. Lanskap Eks-PLG (`is_ex_plg_landscape`): `0,0222`
6. Kedalaman Gambut (`kedalaman_gambut_cm`): `0,0209`

---

## 2. Logic Chain (Rantai Penalaran)

1. **Premis Kebenaran Faktual**: Sumber kebenaran empiris proyek ini terdokumentasi dalam berkas `model_metrics.json`, `eda_summary.json`, dan dataset master `data/processed/karhutla_kalteng_2019_2026.csv`.
2. **Pengujian Mandiri Model**: Eksekusi mandiri terhadap model terkompilasi (`karhutla_rf_model.joblib`) mengonfirmasi bahwa prediksi holdout menghasilkan matriks konfusi $\text{TN}=6586, \text{FP}=2737, \text{FN}=568, \text{TP}=1094$. Seluruh formula turunan ($\text{Recall} = 65,82\%$, $\text{Precision} = 92,06\%$, $\text{F1} = 0,3983$) identik dengan teks ulasan.
3. **Pengujian Tabulasi Spasial**: Eksekusi kalkulasi spasial terhadap poligon batas kabupaten dan izin konsesi membuktikan bahwa angka 75,4% APL, 16,6% Sawit, 8,0% PBPH, 74,3% Gambut, dan median kanal 14.946 m adalah fakta matematis murni tanpa distorsi.
4. **Verifikasi Kutipan Narasi Review**: Pemeriksaan baris demi baris pada teks `review_report.md` menunjukkan bahwa seluruh angka metrik dipaparkan secara presisi, jujur, dan tidak ada angka yang dipalsukan, ditutup-tutupi (misalnya nilai Spatial CV ROC-AUC 0,4950 diakui secara transparan), atau salah kutip.
5. **Keselarasan dengan Tujuan Peer Review Scopus Q1**: Reviewer mengidentifikasi secara tepat seluruh kelemahan metodologis (spatial memorization pada Model A, kompresi F1 akibat class imbalance, ketiadaan literatur 2021–2026, dan diagram ASCII) serta merumuskan rekomendasi perbaikan yang konkret dan terstruktur.

---

## 3. Caveats (Batasan Evaluasi)

- Penilaian ini difokuskan secara ketat pada **integritas faktual, konsistensi numerik, dan validitas metodologis** laporan peer review `output/reports/review_report.md`.
- Evaluasi ini tidak mengubah berkas kode pipeline di `src/` maupun dokumen laporan itu sendiri sesuai batasan peran *Review-only*.
- Tidak ada kelemahan atau anomali numerik yang belum teridentifikasi.

---

## 4. Conclusion & Final Verdict (Kesimpulan & Vonis Akhir)

Berdasarkan pengujian empiris yang komprehensif, independen, dan dapat direproduksi 100%:

$$\mathbf{VONIS\ AKHIR:\ APPROVE\ (DISETUJUI)}$$

Laporan peer review `output/reports/review_report.md` dinyatakan **LULUS UJI EMPIRIS PENUH (100% PASS)**:
1. Tidak ditemukan satu pun angka yang bertentangan atau salah kutip terhadap `model_metrics.json` dan `eda_summary.json`.
2. Seluruh metrik spasial, kurva ROC-AUC, matriks konfusi, bobot kelas, analisis tenurial, kedalaman gambut, dan jarak kanal eks-PLG konsisten dan akurat.
3. Laporan memenuhi standar penelaahan ilmiah berbobot *Senior Peer Reviewer* untuk jurnal internasional Scopus Q1.

---

## 5. Verification Method (Metode Verifikasi Independen)

Untuk mereproduksi dan memverifikasi pengujian ini secara mandiri:

```bash
# Aktifkan lingkungan conda karhutla_env
conda activate karhutla_env

# 1. Jalankan pengujian empiris model dan dataset
/opt/anaconda3/envs/karhutla_env/bin/python tests/test_empirical_metrics.py

# 2. Jalankan audit komprehensif seluruh angka pada review_report.md
/opt/anaconda3/envs/karhutla_env/bin/python tests/audit_review_report_numbers.py
```

Kondisi kegagalan (invalidation conditions): Uji ini akan gagal jika terdapat satu angka metrik yang berubah pada `model_metrics.json`, `eda_summary.json`, atau `review_report.md`.
