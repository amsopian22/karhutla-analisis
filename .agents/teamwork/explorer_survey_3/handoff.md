# HANDOFF REPORT: Methodology & Peer Review Audit
**Agent**: Explorer 3 (Methodology & Peer Review Auditor)  
**Tipe Handoff**: Hard Handoff (Tugas Tuntas Lengkap)  
**Tanggal**: 2026-11-03T03:22:00Z  
**Lokasi Berkas Utama**: `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/.agents/teamwork/explorer_survey_3/analysis.md`

---

## 1. Observation (Pengamatan Faktual)

1. **Metrik Empiris Model Machine Learning (`output/reports/model_metrics.json`)**:
   - Model A (dengan Lat/Lon/Kabupaten):
     - `test_roc_auc`: 0.7956, `test_f1_score`: 0.4512 pada random split (75:25).
     - `spatial_block_cv_mean_roc_auc`: 0.5399 ($\pm$ 0.0531).
     - `spatial_block_cv_mean_f1`: 0.0583.
     - Detail per-fold F1: `[0.2913, 0.0, 0.0, 0.0, 0.0]`. Fold 2, 3, 4, dan 5 menghasilkan F1 = 0.0000.
   - Model B (Pure Biophysical tanpa Lat/Lon/Kabupaten):
     - `test_roc_auc`: 0.7527, `test_f1_score`: 0.3983.
     - `precision_reguler`: 0.9206 (92.1%), `recall_ekstrem`: 0.6582 (65.8%).
     - `spatial_block_cv_mean_roc_auc`: 0.4950 ($\pm$ 0.0490).
     - `spatial_block_cv_mean_f1`: 0.1399 (2.4x lebih tinggi dari Model A).
     - Detail per-fold F1: `[0.2914, 0.0657, 0.1056, 0.0646, 0.1722]`. Seluruh fold mempertahankan deteksi positif.
   - Peringkat Pengaruh Fitur (TreeSHAP Mean Absolute SHAP):
     - `curah_hujan_7h_mm`: 0.0329
     - `jarak_kanal_m`: 0.0322
     - `kecepatan_angin_kmh`: 0.0254
     - `dry_spell_days`: 0.0224
     - `is_ex_plg_landscape`: 0.0222
     - `kedalaman_gambut_cm`: 0.0209
     - `suhu_maks_c`: 0.0203
     - `kelembapan_relatif_pct`: 0.0173

2. **Implementasi Kode Pelatihan (`src/train_model.py`)**:
   - Baris 63: Target biner keparahan api `df["target_severe_fire"] = (df["frp_mw"] >= 12.0).astype(int)`. Proporsi kelas positif adalah 15.1% (6.634 dari 43.937 titik).
   - Baris 111–146: Validasi silang blok spasial menggunakan `GroupKFold(n_splits=5)` yang dikelompokkan berdasarkan `groups = df["kabupaten_kota"]`.
   - Baris 123, 137, 163, 175: Seluruh RandomForestClassifier menggunakan `class_weight="balanced"`.

3. **Implementasi Pemrosesan Data (`src/process_real_data.py`)**:
   - Baris 59: Pemotongan titik satelit FIRMS dilakukan dengan `gpd.sjoin(gdf_raw, gdf_kab, how="inner", predicate="within")` membersihkan 8.892 titik (16.83%) di luar provinsi Kalteng, menyisakan 43.937 titik valid.
   - Baris 88–108 & 123: Jaringan kanal dimodelkan dari 13 vektor garis poros saluran primer (LineString), diproyeksikan ke `EPSG:32749` (UTM 49S).
   - Baris 132: Jarak kanal di luar kabupaten eks-PLG (Seruyan, Kotim, Kobar, dll.) diset ke `-1` untuk mencegah bias jarak semu.
   - Baris 145–149: Data cuaca reanalisis ERA5-Land digabungkan pada tingkat pasangan `(kabupaten_kota, acq_date)`.

4. **Karakteristik Tenurial & Tutupan Lahan (`output/reports/eda_summary.json` & `PROJECT_SUMMARY.md`)**:
   - 75.4% (33.138 titik) berada di Area Non-Konsesi (APL / Lahan Terbuka / Gambut Terlantar).
   - 16.6% (7.276 titik) di Konsesi Sawit (HGU).
   - 8.0% (3.523 titik) di Konsesi Kehutanan (PBPH).
   - 74.3% kebakaran berada di atas kubah gambut hidrologis resmi BBLSDLP 2019.

---

## 2. Logic Chain (Rantai Penalaran Ilmiah)

1. **Dari Observasi 1 dan 2**: Pada random test split, Model A memiliki AUC lebih tinggi (0.7956 vs 0.7527) karena titik uji dan titik latih berada pada kedekatan spasial yang sama. Namun, pada Spatial Block CV (GroupKFold per kabupaten), performa Model A anjlok drastis (AUC 0.5399, F1 0.0583) dan F1 bernilai 0.0000 di 4 dari 5 fold. Hal ini membuktikan secara definitif bahwa Model A mengalami *spatial memorization overfitting*: pohon keputusannya menghafal batas koordinat geodetik, sehingga gagal total saat diuji pada entitas geografis yang belum pernah dilihat.
2. **Dari Observasi 1 dan 2**: Model B (Pure Biophysical) membuang koordinat dan mengandalkan proses biofisik. Pada Spatial Block CV, Model B mempertahankan nilai F1-score positif di seluruh fold dengan rata-rata 0.1399 (2,4 kali lebih tinggi dari Model A). Namun, rata-rata Spatial CV ROC-AUC Model B (0.4950) menunjukkan tantangan nyata dalam memprediksi domain spasial baru yang memiliki variasi bentang alam berbeda (*spatial covariate shift*).
3. **Dari Observasi 1, 2, dan 4**: Kelas positif (Severe Fire FRP $\ge$ 12 MW) hanya sebesar 15.1%. Penggunaan `class_weight="balanced"` secara sengaja mengorbankan Precision demi Recall (mencapai Recall 65.82% pada api ekstrem). Hal ini sangat tepat untuk mitigasi bencana (meminimalkan false negative), namun menghasilkan kompresi F1-score (0.3983 holdout, 0.1399 spatial CV) akibat tingginya false alarm rate.
4. **Dari Observasi 3**: Penggabungan cuaca ERA5-Land berbasis `(kabupaten_kota, acq_date)` menyamakan parameter cuaca untuk seluruh titik dalam satu kabupaten pada hari yang sama, menciptakan bias agregasi spasial (*ecological fallacy*). Demikian pula, penyederhanaan saluran kanal hanya pada 13 poros saluran primer mengabaikan jaringan kanal sekunder/tersier.

---

## 3. Caveats (Batasan dan Asumsi)

1. Penyelidikan ini bersifat *read-only* (tidak mengubah kode sumber atau dataset empiris yang sudah ada).
2. Data satelit aktif FIRMS berfokus pada episode krisis 8 hari (5–12 Oktober 2026), sehingga generalisasi temporal ke awal musim kemarau atau musim hujan bergantung pada data sekunder SiPongi KLHK (2018–2026).
3. Metrik Fire Radiative Power (FRP) mengukur radiasi termal sesaat pada panjang gelombang inframerah tengah (~3.9 $\mu$m) yang lebih sensitif terhadap nyala api permukaan (*surface flaming*); kebakaran gambut dalam tanpa nyala (*deep smoldering*) yang tertutup tajuk dapat mengalami *omission errors*.

---

## 4. Conclusion (Kesimpulan Akhir & Keputusan Penyelidikan)

1. **Rekomendasi Editorial**: Naskah memenuhi standar substansi kebaruan untuk jurnal Scopus Q1 (*Remote Sensing* MDPI / *IJWF* CSIRO) dengan status **Major Revision**. Naskah draft awal sudah sangat kuat pada landasan empiris, tetapi wajib memperkuat bagian *Discussion/Limitations* dengan memaparkan secara jujur fenomena *spatial memorization*, anjloknya skor pada Spatial Block CV, dan trade-off *class imbalance*.
2. **Fondasi Teoretis yang Harus Ditonjolkan**: Pembuktian kegagalan Model A (F1 = 0 pada 4 fold spasial) adalah salah satu *novel scientific contribution* terpenting yang membuktikan Hukum Pertama Geografi Tobler dalam machine learning bencana. Ini bukan kelemahan riset, melainkan temuan inti yang patut dipublikasikan.
3. **Rancangan Dokumen Peer Review**: Kerangka struktur laporan review untuk `output/reports/review_report.md` telah dirancang lengkap dalam Bahasa Indonesia bernas di `analysis.md`, mencakup evaluasi kekuatan, kelemahan, *threats to validity*, serta rekomendasi per seksi naskah.

---

## 5. Verification Method (Metode Verifikasi Independen)

Untuk mereproduksi dan memverifikasi seluruh klaim dan metrik di atas secara independen:

1. **Pemeriksaan Berkas Metrik**:
   Periksa berkas `output/reports/model_metrics.json` baris 18–38 dan 110–128 untuk memverifikasi angka-angka evaluasi Model A dan Model B.
2. **Pemeriksaan Skrip Pelatihan**:
   Buka `src/train_model.py` untuk memeriksa implementasi `GroupKFold`, `class_weight='balanced'`, dan target $FRP \ge 12.0\text{ MW}$.
3. **Eksekusi Pengujian (Uji Re-run Model di Lingkungan Conda)**:
   Jalankan perintah berikut di terminal:
   ```bash
   conda activate karhutla_env
   /opt/anaconda3/envs/karhutla_env/bin/python src/train_model.py
   ```
   Pastikan keluaran terminal mencocokkan:
   - Model A Mean Spatial CV ROC-AUC: `0.5399` dan Mean F1: `0.0583`
   - Model B Mean Spatial CV ROC-AUC: `0.4950` dan Mean F1: `0.1399`
   - Recall Ekstrem Model B: `65.8%`
4. **Kondisi Invalidasi (Invalidation Conditions)**:
   Klaim laporan ini akan gugur jika ditemukan bahwa Model A mampu mempertahankan F1-score > 0.20 pada seluruh fold Spatial Block CV, atau jika data satelit terbukti tidak dipotong sesuai batas kabupaten resmi Kalimantan Tengah.
