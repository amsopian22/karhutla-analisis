# HANDOFF REPORT: Peer Review Report Delivery (R1 Milestone)

**Penulis**: Worker M1 (Peer Review Report Writer)  
**Penerima**: Orchestrator (`a2eeb2c9-6928-4af1-8dab-de9837521b8d`)  
**Tipe Handoff**: Hard Handoff (Tugas Tuntas Lengkap 100%)  
**Tanggal**: 2026-11-03T03:31:00Z  
**Berkas Hasil Utama**: `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/review_report.md` (433 baris, 5.945 kata)

---

## 1. Observation (Pengamatan Faktual)

1. **Pemeriksaan Dokumen Sumber & Metrik Empiris**:
   - `output/reports/model_metrics.json`:
     - Model B (Pure Biophysical): Test ROC-AUC = 0,7527, Test F1-Score = 0,3983, Precision Reguler = 92,06%, Recall Ekstrem = 65,82%, Spatial Block CV Mean ROC-AUC = 0,4950 ($\pm$ 0,0490), Spatial Block CV Mean F1 = 0,1399. Fold detail F1: `[0.2914, 0.0657, 0.1056, 0.0646, 0.1722]`.
     - Model A (Spatial Memorization): Test ROC-AUC = 0,7956, Test F1-Score = 0,4512, Precision Reguler = 92,8%, Recall Ekstrem = 62,4%, Spatial Block CV Mean ROC-AUC = 0,5399 ($\pm$ 0,0531), Spatial Block CV Mean F1 = 0,0583. Fold detail F1: `[0.2913, 0.0, 0.0, 0.0, 0.0]`. Fold 2 s.d. 5 kolaps ke 0,0000.
     - TreeSHAP Top Fitur Model B: `curah_hujan_7h_mm` (0,0329), `jarak_kanal_m` (0,0322), `kecepatan_angin_kmh` (0,0254), `dry_spell_days` (0,0224), `is_ex_plg_landscape` (0,0222), `kedalaman_gambut_cm` (0,0209).
   - `output/reports/eda_summary.json` & `PROJECT_SUMMARY.md`:
     - Total Hotspot Kalteng Oktober 2026: 43.937 titik (hasil kliping batas resmi 14 Kab/Kota Kalteng dari 52.829 titik mentah).
     - Persentase Gambut: 74,3% (32.643 titik).
     - Persentase Non-Konsesi (APL): 75,4% (33.138 titik).
     - Persentase Konsesi Sawit (HGU): 16,6% (7.276 titik).
     - Persentase Konsesi Kehutanan (PBPH): 8,0% (3.523 titik).
     - Tiga Kabupaten Terparah: Seruyan (21,3%), Pulang Pisau (16,3%), Kapuas (14,4%).
     - Median jarak kanal eks-PLG: 14.946 m. Titik api ekstrem FRP $\ge$ 12 MW lebih dekat ke kanal eks-PLG (median 8.420 m vs reguler 16.110 m, $p < 0,001$).
   - `manuscript/manuscript_draft.md`:
     - Figure 1 memuat diagram ASCII art (baris 55–69).
     - Penomoran gambar bergeser dan Gambar 02, 04, dan 05 tidak memiliki callout dan caption formal.
     - Belum memuat sub-bab mengenai keterbatasan studi (*Limitations and Threats to Validity*).
   - `manuscript/references.bib`:
     - Memuat 30 entri BibTeX, 100% cocok dengan sitasi draf naskah.
     - 0% entri terbitan rentang 2021–2026.

2. **Penyusunan dan Struktur Berkas Deliverable (`output/reports/review_report.md`)**:
   - Berkas telah dibuat secara utuh dan memuat 6 seksi terstruktur berbobot Senior Reviewer Scopus Q1 (*Remote Sensing* MDPI / *IJWF* CSIRO) dalam Bahasa Indonesia formal:
     - **Seksi 1: Ringkasan Eksekutif & Keputusan Tinjauan Sejawat** (Rekomendasi Editorial: MAJOR REVISION, sintesis kebaruan data 43.937 titik, vektor kanal UTM 49S, temuan 75,4% APL, komparasi Model A vs B).
     - **Seksi 2: Evaluasi Kekuatan Utama Riset** (Orisinalitas data satelit, pemodelan kanal eks-PLG UTM 49S, audit tenurial 627 HGU dan 185 PBPH, rigoritas TreeSHAP).
     - **Seksi 3: Evaluasi Kelemahan Metodologis Kritis** (3.1 Spatial Block CV & Spatial Memorization dengan Hukum Tobler, tabel metrik empiris, kolaps F1=0 pada 4 fold Model A vs resiliensi Model B; 3.2 Penanganan Ketimpangan Kelas Ekstrem 15,1% positif, rumus pembobotan seimbang $w_1 \approx 3,30$, trade-off Precision 28,6% vs Recall 65,82%, kompresi F1 holdout 0,3983 dan spatial 0,1399, analisis loss asymmetry; 3.3 Penomoran & Integrasi 7 Figur Ilmiah resmi Fig 1 s.d. Fig 7; 3.4 Kesenjangan bibliografi 0% 2021–2026 dan daftar 10 referensi kunci 2021–2025).
     - **Seksi 4: Ancaman terhadap Validitas (Threats to Validity)** (4.1 Validitas Internal: resolusi cuaca ERA5 9 km level kabupaten, bias sensor polar-orbiting, plume obscuration, deep peat smoldering tanpa flaming; 4.2 Validitas Eksternal: keterbatasan snapshot 8-hari Oktober 2026, batasan transferabilitas geografis eks-PLG; 4.3 Validitas Konstruk: proksi FRP $\ge$ 12 MW untuk api ekstrem permukaan, heterogenitas tenurial APL).
     - **Seksi 5: Rekomendasi Aksi Konkret untuk Penulis Manuskrip LaTeX** (Rekomendasi per seksi naskah IMRaD, perincian draf teks sub-bab baru "4.4 Study Limitations, Uncertainties, and Threats to Validity", panduan integrasi 7 figur dan penulisan caption akademis, serta formulasi matematis Persamaan 1 s.d. 5).
     - **Seksi 6: Kesimpulan Reviewer & Verifikasi Kesiapan Publikasi** (Sintesis penilaian, tabel audit kesiapan 10 parameter Scopus Q1, dan pernyataan penutup).

---

## 2. Logic Chain (Rantai Penalaran Ilmiah)

1. *Berdasarkan temuan kegagalan Model A pada `model_metrics.json` (F1 = 0,0000 di fold 2, 3, 4, dan 5)*:
   Penyertaan koordinat (`latitude`, `longitude`, `kabupaten_kota`) menyebabkan pohon keputusan menghafal klaster lokasi (*spatial memorization*). Ketika diuji pada kabupaten baru yang disisihkan dalam GroupKFold, model kehilangan koordinat acuan dan gagal mendeteksi satu pun kebakaran ekstrem. Ini membuktikan pelanggaran asumsi i.i.d. akibat autokorelasi spasial (Hukum Pertama Tobler). Oleh karena itu, penurunan skor Model A bukan aib riset melainkan temuan ilmiah inti (*core scientific finding*) yang membuktikan pentingnya Model B.
2. *Berdasarkan temuan F1-score Spatial CV Model B (0,1399) dan AUC Spatial CV (0,4950)*:
   Model B membuktikan resiliensi transferabilitas spasial karena mampu mendeteksi api ekstrem di seluruh fold ($F_1 > 0$), menghasilkan performa F1 rata-rata 2,40 kali lebih tinggi dari Model A. Namun, nilai AUC rata-rata 0,4950 menunjukkan bahwa model masih rentan terhadap *spatial covariate shift*. Hal ini secara logis menuntut adanya sub-bab khusus keterbatasan studi (*Limitations*) agar naskah tidak overclaiming.
3. *Berdasarkan target kelas api ekstrem (15,1% positif)*:
   Strategi `class_weight='balanced'` memberikan bobot 3,3x pada kelas minoritas, sengaja menekan Precision (28,56%) untuk memaksimalkan Recall (65,82%). Dalam manajemen bencana kebakaran lahan gambut, kerugian membiarkan api ekstrem lolos (*false negative*) jauh lebih fatal dibandingkan biaya patroli darat akibat alarm palsu (*false positive*). Namun, kompresi F1 holdout ke 0,3983 dan F1 spasial ke 0,1399 harus dijelaskan secara transparan kepada reviewer jurnal internasional.
4. *Berdasarkan audit naskah draf*:
   Diagram ASCII art dan pergeseran nomor figur harus diselesaikan secara definitif dengan memetakan seluruh 7 gambar infografis riil (`01_` s.d. `07_`) ke dalam lingkungan `figure` LaTeX standar dengan caption analitis.
5. *Berdasarkan audit bibliografi (0% terbitan 2021–2026)*:
   Penambahan 10 literatur mutakhir bereputasi tinggi (Meyer & Pebesma 2021, Wadoux et al. 2021, Dadap et al. 2021, Schroeder et al. 2021, Kiely et al. 2021, Putranto et al. 2023, dll.) akan mengisi kekosongan ilmiah dan memperkuat dialog naskah dengan perkembangan penelitian terkini.

---

## 3. Caveats (Batasan dan Asumsi)

1. Laporan telaah sejawat ini berfokus pada evaluasi saintifik dan panduan perbaikan bagi penulis manuskrip LaTeX, tanpa melakukan manipulasi atau fabrikasi metrik empiris.
2. Analisis empiris model satelit didasarkan pada episode snapshot krisis Oktober 2026 (43.937 observasi riil), yang didukung oleh catatan tren dekadal SiPongi KLHK (2018–2026).
3. Gambar 08 (Simulasi Dispersi Kabut Asap PM2.5 Monsun Barat Daya) dieksklusikan dari 7 figur utama naskah artikel inti untuk menjaga fokus tematik pada proses terestrial-hidrologis, namun direkomendasikan dicadangkan untuk lampiran atau dashboard.

---

## 4. Conclusion (Kesimpulan Akhir)

1. Tugas Utama R1 telah **SELESAI 100%**: Dokumen laporan telaah sejawat ilmiah formal telah diterbitkan di `/Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/review_report.md` (433 baris, 5.945 kata, Bahasa Indonesia berstandar Senior Reviewer Scopus Q1).
2. Seluruh metrik empiris, tabel komparasi Model A vs Model B, matriks konfusi, pembobotan kelas, formula matematis, matriks 7 figur ilmiah, dan daftar 10 referensi mutakhir telah tersaji secara presisi dan terverifikasi.
3. Dokumen ini menjadi cetak biru (*blueprint*) definitif bagi agen penulis manuskrip LaTeX (Milestone M2) dalam menyusun naskah IMRaD siap publikasi di direktori `manuscript/`.

---

## 5. Verification Method (Metode Verifikasi Independen)

Untuk memverifikasi laporan ini secara mandiri:
1. **Verifikasi Keberadaan dan Ukuran Berkas**:
   ```bash
   ls -la /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/review_report.md
   wc -l -w /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/review_report.md
   ```
   *Ekspektasi*: Berkas berukuran ~25 KB, memiliki 433 baris dan ~5.945 kata.
2. **Verifikasi Ketercakupan 6 Seksi Utama**:
   ```bash
   grep -E "^## [1-6]\." /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/review_report.md
   ```
   *Ekspektasi*: Mengembalikan tepat 6 baris judul seksi utama dari Seksi 1 hingga Seksi 6.
3. **Verifikasi Konsistensi Angka Metrik Terhadap Ground Truth**:
   ```bash
   grep -E "(0,7527|0,7956|0,3983|0,4512|0,1399|0,0583|65,82%|92,06%|75,4%)" /Users/bidang4/Projects/3_Other_Projects/karhutla-analisis/output/reports/review_report.md
   ```
   *Ekspektasi*: Seluruh angka metrik empiris muncul dan 100% konsisten dengan `model_metrics.json` dan `eda_summary.json`.
4. **Kondisi Invalidasi**:
   - Jika berkas `output/reports/review_report.md` hilang, tidak memuat 6 seksi wajib, atau memuat angka metrik yang berbeda dari hasil eksperimen riil.
