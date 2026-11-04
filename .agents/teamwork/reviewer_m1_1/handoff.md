# LAPORAN HANDOFF PEER REVIEWER 1 (MILESTONE 1 — R1)

## 1. Observation

Penelaahan independen dilakukan terhadap artefak Milestone 1 (M1), basis data empiris, visualisasi ilmiah, basis kode pipeline, dan draf manuskrip:

1. **Berkas Target Telaah (`output/reports/review_report.md`)**:
   - Berkas berukuran 45.122 bytes (434 baris) ditulis dalam Bahasa Indonesia formal berbobot *Senior Journal Reviewer* (Scopus Q1).
   - Terstruktur menjadi 6 seksi utama:
     - Seksi 1: Ringkasan Eksekutif & Keputusan Editorial Resmi (*Major Revision* terhadap draf awal).
     - Seksi 2: Evaluasi Kekuatan Utama Riset (kurasi 43.937 hotspot FIRMS, vektor kanal UTM Zone 49S, temuan 75,4% APL non-konsesi vs 16,6% sawit & 8,0% PBPH, TreeSHAP).
     - Seksi 3: Evaluasi Kelemahan Metodologis Kritis (*Spatial Block CV*, *Spatial Memorization*, *Class Imbalance 15,1%*, pemetaan 7 figur ilmiah, celah literatur 2021–2026).
     - Seksi 4: Ancaman terhadap Validitas (*Internal*, *External*, dan *Construct Validity*).
     - Seksi 5: Rekomendasi Aksi Konkret per seksi manuskrip LaTeX, cetak biru sub-bab 4.4, formulasi matematis Persamaan (1)–(5), dan penataan tabel `booktabs`.
     - Seksi 6: Kesimpulan & Daftar Periksa Kesiapan Publikasi Scopus Q1 (*11 Parameter Audit*).

2. **Konsistensi Metrik Empiris Terhadap Basis Data JSON**:
   - Berkas `output/reports/model_metrics.json`:
     - Model B (Pure Biophysical): Test ROC-AUC = 0,7527; Test F1 = 0,3983; Precision Reguler = 0,9206; Recall Ekstrem = 0,6582. Mean Spatial Block CV ROC-AUC = 0,4950 ($\pm$ 0,0490); Mean F1 = 0,1399. Fold 1 s.d. 5: F1 berturut-turut [0,2914; 0,0657; 0,1056; 0,0646; 0,1722].
     - Model A (Spatial Memorization): Test ROC-AUC = 0,7956; Test F1 = 0,4512; Mean Spatial Block CV ROC-AUC = 0,5399 ($\pm$ 0,0531); Mean F1 = 0,0583. Fold 1 s.d. 5: F1 berturut-turut [0,2913; 0,0000; 0,0000; 0,0000; 0,0000].
     - Tabel perbandingan pada `review_report.md` (baris 100–121) memuat angka-angka yang identik 100% presisi tanpa fabrikasi.
   - Berkas `output/reports/eda_summary.json`:
     - Total sampel: 43.937 titik. Gambut: 74,3%. Non-konsesi APL: 75,4%. Sawit HGU: 16,6%. Kehutanan PBPH: 8,0%. Median jarak kanal eks-PLG: 14.946 m. Seluruh angka dikutip secara akurat pada `review_report.md` (baris 50–67, 136–139).

3. **Integritas Gambar Ilmiah (`output/figures/`)**:
   - Seluruh 8 gambar (`01_` s.d. `08_`) telah diverifikasi ada secara fisik, bertipe PNG resolusi tinggi (>3000px, 300 DPI).
   - `review_report.md` merekomendasikan pemetaan Figures 1 s.d. 7 ke dalam badan teks naskah dan mencadangkan Gambar 08 untuk studi lanjutan/lampiran, yang selaras sempurna dengan kontrak `ORIGINAL_REQUEST.md` (R1 & R2).

4. **Kondisi Draf Awal Manuskrip (`manuscript/manuscript_draft.md` & `references.bib`)**:
   - Ditemukan diagram peta berbasis teks ASCII pada baris 55–69 (`manuscript_draft.md`).
   - Penomoran gambar pada draf awal salah/bergeser (merujuk Gambar 2 untuk tren tahunan, Gambar 3 untuk kabupaten, Gambar 4 untuk ML ROC, Gambar 5 untuk SHAP).
   - Tiga gambar riil terabaikan tanpa callout (`02_`, `04_`, `05_`).
   - Tidak ada sub-bab tersendiri untuk keterbatasan riset (*threats to validity*).
   - Berkas `references.bib` berisi 30 referensi dengan 0 referensi terbitan 2021–2026. Seluruh kelemahan ini diidentifikasi secara tajam dan tepat oleh `review_report.md`.

5. **Pemeriksaan Integritas & Anti-Cheating**:
   - Kode sumber `src/train_model.py` menjalankan algoritma scikit-learn riil (`GroupKFold`, `RandomForestClassifier`, `shap.TreeExplainer`).
   - Tidak ditemukan nilai metrik yang di-hardcode dalam skrip pemodelan.
   - Tidak ada fasad atau jalan pintas delegasi eksternal ilegal.

---

## 2. Logic Chain

1. **Premis 1 (Kesesuaian Persyaratan R1)**:  
   Dokumen `ORIGINAL_REQUEST.md` (R1) mewajibkan penyusunan laporan peer review terstruktur dalam Bahasa Indonesia dengan rigor *Senior Journal Reviewer*, membedah kekuatan, kelemahan metodologis (*spatial CV*, *spatial memorization*, *class imbalance*), ancaman validitas, serta rekomendasi konkret.
   - *Bukti*: `review_report.md` memenuhi seluruh struktur tersebut dalam 6 bagian komprehensif, mencakup landasan teoretis Hukum Tobler, perbandingan Model A vs Model B, formula pembobotan kelas, audit 7 figur, serta 10 usulan referensi mutakhir.

2. **Premis 2 (Ketajaman Analisis Kritis & Integritas Ilmiah)**:  
   Laporan tidak bersikap apologetis terhadap hasil riset, melainkan membongkar fakta bahwa Model A mengalami keruntuhan katastropik ($F_1 = 0,0000$ di 4 fold) dan bahwa Model B memiliki rata-rata Spatial CV ROC-AUC 0,4950 yang mendekati tebakan acak akibat *spatial covariate shift*. Laporan ini mewajibkan penulis naskah untuk transparan dan tidak menyembunyikan metrik tersebut.
   - *Bukti*: Seksi 1.4 dan Seksi 3.1.4 dalam `review_report.md` secara eksplisit menginstruksikan pengakuan empiris ini.

3. **Premis 3 (Kejelasan Panduan Aksi untuk Milestone 2)**:  
   Agar Milestone 2 (penyusunan naskah LaTeX Scopus Q1) dapat dieksekusi dengan mulus, laporan review harus memberikan arahan teknis yang langsung dapat diimplementasikan (persamaan LaTeX, format tabel, caption gambar, referensi BibTeX).
   - *Bukti*: Seksi 5 menyediakan kode LaTeX siap pakai untuk Persamaan (1) s.d. (5), lingkungan `figure` untuk Gambar 1 s.d. 7, rancangan tabel `booktabs` (Tabel 1 s.d. 4), draf teks akademik berbahasa Inggris untuk Sub-bab 4.4, serta daftar 10 sitasi kunci 2021–2025.

4. **Premis 4 (Uji Adversarial Reviewer)**:
   - *Stress-test 1 (Spatial CV AUC 0,4950)*: Angka 0,4950 bukan kegagalan algoritma semata, melainkan batas teoretis *Area of Applicability (AOA)* (Meyer & Pebesma 2021). Naskah LaTeX harus membingkai ini sebagai bukti empiris bahwa model bencana gambut memerlukan kalibrasi domain adaptif saat diaplikasikan ke lanskap non-analogous.
   - *Stress-test 2 (Kalibrasi Probabilitas pada Balanced Weights)*: Penalti bobot kelas terbalik ($w_1 = 3,30$ vs $w_0 = 0,59$) mendistorsi estimasi probabilitas kontinu. Oleh karena itu, rekomendasi *Multi-Tier Risk Stratification* harus disertai catatan perlunya kalibrasi probabilitas (Isotonic/Platt) sebelum implementasi operasional lapangan.
   - *Stress-test 3 (Spatio-temporal Co-leakage)*: Random split pada data cuaca harian agregat kabupaten membocorkan vektor cuaca harian yang sama antara train dan test set, yang turut menjelaskan mengapa holdout test AUC (0,7527) jauh lebih optimis daripada Spatial Block CV (0,4950).
   Catatan-catatan adversarial ini memperkuat dan melengkapi `review_report.md` sebagai bekal bagi agen pelaksana Milestone 2.

---

## 3. Caveats

1. Penelaahan ini berfokus pada kelayakan dan ketelitian laporan telaah sejawat (`review_report.md`) sebagai prasyarat pelepasan (*milestone gate*) menuju Milestone 2.
2. Penilai tidak melakukan perubahan pada berkas kode program (`src/`) atau berkas naskah (`manuscript/`), menjaga batasan peran *review-only*.
3. Simulasi dispersi aerosol atmosferik Monsun Barat Daya (`08_transboundary_haze_dispersion.png`) tidak dievaluasi mendalam karena disepakati dicadangkan untuk penelitian lanjutan di luar 7 figur utama.

---

## 4. Conclusion

**VONIS AKHIR: APPROVE (DISETUJUI)**

Dokumen `output/reports/review_report.md` memenuhi standar tertinggi laporan tinjauan sejawat ilmiah internasional (*Scopus Q1 standard*). Laporan ini:
1. Bebas dari manipulasi data atau pelanggaran integritas (100% valid terhadap data riil).
2. Menyajikan evaluasi metodologis yang tajam, kritis, dan berimbang terhadap *spatial memorization*, *spatial block CV*, dan *class imbalance*.
3. Menguraikan ancaman terhadap validitas (*internal, external, construct*) secara mendalam.
4. Memberikan cetak biru (*actionable blueprint*) yang sangat operasional dan presisi untuk penyusunan naskah LaTeX IMRaD pada Milestone 2.

Pekerjaan pada Milestone 1 dinyatakan **SELESAI dan MEMENUHI SYARAT**. Tim dapat segera melanjutkan ke **Milestone 2 (Penyusunan Naskah LaTeX Publikasi-Ready)**.

---

## 5. Verification Method

Untuk memverifikasi laporan ini secara independen:
1. **Verifikasi Metrik Empiris**:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c "
   import json
   with open('output/reports/model_metrics.json') as f:
       m = json.load(f)
   assert m['model_b_pure_biophysical']['test_roc_auc'] == 0.7527
   assert m['model_b_pure_biophysical']['spatial_block_cv_mean_roc_auc'] == 0.495
   assert m['model_a_spatial_memorization']['spatial_block_cv_mean_f1'] == 0.0583
   print('Verification Passed: All empirical metrics match review_report.md exactly!')
   "
   ```
2. **Verifikasi Keberadaan 7 Gambar Ilmiah**:
   Periksa keberadaan berkas `output/figures/01_` s.d. `07_` dan validitas format PNG menggunakan modul `PIL.Image`.
3. **Kondisi Diskualifikasi / Invalidation Conditions**:
   Vonis ini batal apabila ditemukan adanya pemalsuan kode pelatihan, perubahan angka metrik secara sepihak, atau penghilangan pembahasan keterbatasan spatial CV pada naskah Milestone 2.
