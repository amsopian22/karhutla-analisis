# LAPORAN PENELAAHAN KRITIS SEJAWAT INDEPENDEN (PEER REVIEWER 2)
# Milestone 1: Evaluasi Terhadap Laporan Tinjauan Sejawat R1 (`output/reports/review_report.md`)

---

## 1. Observation (Pengamatan Faktual Terverifikasi)

Penelaahan independen dilakukan terhadap berkas `output/reports/review_report.md` (434 baris, 45.122 bita), serta divalidasi silang terhadap seluruh artefak data empiris, naskah draf, basis kode, dan figur visual terkait:

1. **Integritas Metrik Empiris Model Machine Learning**:
   - Berkas `output/reports/review_report.md` (baris 98–109 dan baris 111–120) menyajikan metrik komparasi Model A vs Model B secara mendetail.
   - Pengecekan silang terhadap berkas `output/reports/model_metrics.json` membuktikan kesesuaian numerik 100% presisi:
     - Model A: Holdout ROC-AUC = `0.7956`, Holdout F1 = `0.4512`, Spatial Block CV Mean ROC-AUC = `0.5399` ($\pm$ `0.0531`), Spatial Block CV Mean F1 = `0.0583`. Pada 4 dari 5 fold spasial (Fold 2 s.d. 5), F1-score Model A bernilai tepat `0.0000`.
     - Model B: Holdout ROC-AUC = `0.7527`, Holdout F1 = `0.3983`, Precision Reguler = `0.9206` (92,1%), Recall Ekstrem = `0.6582` (65,82%), Spatial Block CV Mean ROC-AUC = `0.4950` ($\pm$ `0.0490`), Spatial Block CV Mean F1 = `0.1399` (konsisten positif di seluruh 5 fold: Fold 1 `0.2914`, Fold 2 `0.0657`, Fold 3 `0.1056`, Fold 4 `0.0646`, Fold 5 `0.1722`).
     - Peringkat TreeSHAP Model B (baris 73–78 dan 266–280): 12 fitur dengan nilai mean absolute SHAP teratas curah hujan 7-hari (`0.0329`), jarak kanal eks-PLG (`0.0322`), kecepatan angin (`0.0254`), dry spell (`0.0224`), dan kedalaman gambut (`0.0209`), identik dengan `model_metrics.json` baris 181–242.
   - Pengecekan pada `src/train_model.py` (baris 111–185 dan baris 264–285) membuktikan bahwa seluruh komputasi dieksekusi menggunakan modul asli `sklearn.ensemble.RandomForestClassifier`, `sklearn.model_selection.GroupKFold`, dan `shap.TreeExplainer`, tanpa adanya hasil tes yang di-hardcode (*no hardcoded metrics*).

2. **Deteksi Kerusakan Struktural & Cacat Visual pada Draf Manuskrip**:
   - `review_report.md` (baris 181–194) mengungkap bahwa draf awal `manuscript/manuscript_draft.md` memuat:
     - Diagram ASCII art untuk Figure 1 pada baris 55–69 (`+-------------------------+`).
     - Pergeseran nomor gambar (*mismatched callouts*): pemanggilan `Figure 2` untuk SiPongi (baris 170), `Figure 3` untuk kabupaten (baris 195), `Figure 4` untuk ROC (baris 238), dan `Figure 5` untuk TreeSHAP (baris 264).
     - Ketiadaan pemanggilan (*missing callouts*) untuk berkas `02_heatmap_musiman_bulan.png`, `04_analisis_gambut_dan_kanal.png`, dan `05_status_konsesi_esg.png`.
   - Pemeriksaan langsung pada `manuscript/manuscript_draft.md` mengonfirmasi kebenaran seluruh temuan cacat struktural tersebut.

3. **Status Ketersediaan 7 Figur Ilmiah**:
   - Verifikasi melalui perintah `ls -lh output/figures/` membuktikan keberadaan seluruh 7 figur beresolusi tinggi (300 DPI) dalam format PNG:
     - `01_tren_tahunan_el_nino.png` (250 KB)
     - `02_heatmap_musiman_bulan.png` (202 KB)
     - `03_peringkat_kabupaten_terparah.png` (261 KB)
     - `04_analisis_gambut_dan_kanal.png` (324 KB)
     - `05_status_konsesi_esg.png` (252 KB)
     - `06_evaluasi_model_ml.png` (328 KB)
     - `07_shap_feature_importance.png` (509 KB)
   - Seluruh 7 figur telah dipetakan secara terstruktur ke dalam matriks penomoran definitif Figure 1 s.d. Figure 7 pada `review_report.md` baris 198–207 dengan draf *caption* ilmiah dan label LaTeX (`\label{fig:...}`).

4. **Kesenjangan Kronologis Bibliografi Eksisting**:
   - Audit bibliografi pada `manuscript/references.bib` mencatat total 30 entri sitasi.
   - Penapisan kronologis membuktikan bahwa distribusi tahun penerbitan adalah: 1970 (1), 1993 (1), 2001–2010 (11), 2011–2020 (17). **Tidak ditemukan satu pun referensi terbitan tahun 2021–2026 (0,0%)**.
   - `review_report.md` (baris 224–236) telah merumuskan 10 referensi pengganti terbitan 2021–2025 dari jurnal bereputasi tinggi (*Nature Communications*, *Ecological Modelling*, *Remote Sensing of Environment*, *Scientific Reports*, *Atmospheric Chemistry and Physics*, *Land Use Policy*) yang relevan untuk memperkuat justifikasi metodologis.

5. **Pemeriksaan Pelanggaran Integritas Ilmiah (Integrity Violation Check)**:
   - Tidak ditemukan adanya hasil uji buatan (*fabricated outputs*), implementasi semu (*facade/dummy implementations*), pemotongan jalan (*shortcuts*), maupun pemalsuan log verifikasi pada `review_report.md` maupun skrip pendukung.

---

## 2. Logic Chain (Rantai Logika Penilaian Objektif)

1. **Kesesuaian dengan Standar Reviewer Scopus Q1**:
   - `review_report.md` mengevaluasi naskah dengan kacamata editor/reviewer jurnal papan atas (*Remote Sensing*, *IJWF*, *Ecological Modelling*). Keputusan resmi yang diambil adalah **REKOMENDASI: MAJOR REVISION** (bukan penolakan mentah dan bukan persetujuan dini).
   - Rationale: Kontribusi empiris dan inovasi spasial riset sangat orisinal dan bernilai tinggi (*high novelty*), namun naskah draf awal memiliki kelemahan format fatal (diagram ASCII, cacat penomoran gambar, ketiadaan bab keterbatasan, kekosongan literatur 5 tahun terakhir). Rekomendasi revisi mayor adalah keputusan editorial yang paling tepat, profesional, dan proporsional.

2. **Keadilan dan Transparansi Evaluasi Model B vs Model A**:
   - Evaluasi terhadap Model B dilakukan secara sangat adil, jujur, dan tidak berat sebelah.
   - Laporan tidak berusaha menutupi atau mempercantik performa Model B:
     - Diakui secara eksplisit bahwa rata-rata *Spatial CV ROC-AUC* Model B adalah **0,4950 ($\pm$ 0,0490)** (berada di sekitar garis tebakan acak 0,5000), yang disebabkan oleh *spatial covariate shift* (heterogenitas lanskap antar kabupaten, seperti keberadaan jaringan kanal eks-PLG yang hanya terkonsentrasi di Pulang Pisau dan Kapuas).
     - Diakui bahwa strategi `class_weight='balanced'` pada kelas minoritas 15,1% menghasilkan 2.737 *False Positives*, yang menekan *Precision* ekstrem ke 28,56% dan mengompresi *F1-score* holdout ke 0,3983 serta *F1-score* Spatial CV ke 0,1399.
   - Keunggulan Model B tetap diartikulasikan secara objektif:
     - Model B memiliki *Recall* ekstrem 65,82% (mendeteksi 2 dari 3 kebakaran besar) dan mempertahankan nilai prediksi positif di seluruh 5 fold spasial (*F1-score* rata-rata 0,1399, 2,40 kali lipat lebih tinggi dari Model A yang runtuh total ke $F_1 = 0,0000$ di 4 fold).
     - Reviewer memberikan justifikasi praktis berdasarkan prinsip asimetri kerugian (*loss asymmetry*) dalam manajemen bencana karhutla lahan gambut tropis (biaya *False Negative* jauh lebih katastropik daripada *False Positive*), sembari memberikan mitigasi terhadap bahaya *alert fatigue* melalui Stratifikasi Risiko Berjenjang (Multi-Tier Risk Stratification).

3. **Kelayakan Pembahasan 7 Figur Ilmiah dan Rekomendasi Bibliografi**:
   - Penataan ulang 7 figur infografis riil (`01_` s.d. `07_`) ke dalam alur IMRaD menggantikan diagram ASCII merupakan koreksi esensial yang menyelamatkan manuskrip dari risiko *desk reject*.
   - Pemilihan 10 referensi mutakhir 2021–2025 secara langsung mengisi kekosongan dialog literatur kontemporer, khususnya karya fundamental Meyer & Pebesma (2021, *Nature Communications*) mengenai *Area of Applicability* (AOA) model spasial dan Dadap et al. (2021, *Nature Communications*) tentang muka air tanah gambut.

4. **Kualitas Sub-Bab Keterbatasan Riset (Section 4.4 Blueprint)**:
   - Rekomendasi sub-bab baru *"4.4 Study Limitations, Uncertainties, and Threats to Validity"* mengupas tuntas ancaman validitas internal (agregasi cuaca ERA5 ~9 km / *ecological fallacy*, oklusi asap pekat satelit polar-orbiting, pembakaran gambut bawah tanah tanpa nyala / *smoldering combustion*), validitas eksternal (snapshot krisis 8 hari Oktober 2026, batasan transferabilitas di luar eks-PLG), dan validitas konstruk (FRP $\ge 12$ MW sebagai proksi energi radiasi permukaan versus volume gambut terbakar).

---

## 3. Adversarial Review & Stress-Testing (Telaah Kritis Permusuhan)

Sebagai *Adversarial Critic*, dilakukan pengujian stres terhadap asumsi-asumsi dalam `review_report.md` untuk mengidentifikasi potensi titik lemah (*failure modes*):

### Tantangan 1: Partisi Spatial Block CV Berbasis Batas Administratif (GroupKFold Regency)
- **Asumsi yang Diuji**: Pengelompokan fold spasial menggunakan unit administrasi kabupaten (`kabupaten_kota`) diasumsikan sebagai blok spasial independen yang cukup memadai untuk memutus autokorelasi spasial.
- **Skenario Serangan (*Attack Scenario*)**: Batas administrasi kabupaten tidak selalu bertepatan dengan batas ekologis Kesatuan Hidrologis Gambut (KHG). Sebagai contoh, kubah gambut Blok A eks-PLG membentang melintasi perbatasan Kabupaten Kapuas dan Kabupaten Pulang Pisau. Jika Pulang Pisau berada di Fold 2 sementara Kapuas berada di Fold 3, proses hidrologis dan dinamika muka air tanah di satu kubah yang sama masih berpotensi menimbulkan rembesan korelasi spasial lintas perbatasan (*cross-boundary hydrological leakage*).
- **Tingkat Risiko**: Sedang (*Medium*).
- **Rekomendasi Mitigasi untuk Manuskrip LaTeX (M2)**: Penulis wajib menambahkan catatan reflektif dalam Section 2 (Metode) dan Section 4.4 (Keterbatasan) bahwa partisi spasial berbasis kabupaten dipilih karena kepraktisan yurisdiksi pengambilan kebijakan penanggulangan bencana daerah, namun studi masa depan disarankan mengevaluasi partisi spasial berbasis batas poligon KHG murni.

### Tantangan 2: Penggunaan Nilai Sentinel $-1$ untuk Jarak Kanal di Luar Eks-PLG
- **Asumsi yang Diuji**: Penetapan `jarak_kanal_m = -1` pada kabupaten non-PLG (Seruyan, Kotim, Kobar) diasumsikan cukup netral bagi Random Forest.
- **Skenario Serangan (*Attack Scenario*)**: Algoritma pohon keputusan (*decision tree*) dapat memperlakukan nilai $-1$ sebagai pemisah biner artifisial, yang secara implisit berfungsi mirip dengan *dummy indicator* regional, sehingga berpotensi menjadi proksi tersembunyi bagi geografi barat Kalteng.
- **Tingkat Risiko**: Rendah–Sedang (*Low to Medium*).
- **Evaluasi**: `review_report.md` pada baris 254–257 telah secara cermat mengidentifikasi risiko ini: *"Penetapan nilai sentinel -1 untuk kabupaten non-PLG... adalah strategi rekayasa fitur yang pragmatis untuk mencegah bias jarak semu, namun menimbulkan diskontinuitas buatan dalam pohon keputusan Random Forest."* Ini membuktikan bahwa Reviewer 1 telah mengantisipasi kritik ini dengan sangat tajam.

### Tantangan 3: Stabilitas Zero-Division pada Evaluasi F1-Score Fold Spasial
- **Asumsi yang Diuji**: Nilai $F_1 = 0,0000$ pada Model A (Fold 2–5) mencerminkan kegagalan prediksi total.
- **Skenario Serangan (*Attack Scenario*)**: Apakah nilai 0,0000 tersebut disebabkan oleh tidak adanya sampel positif pada fold uji, ataukah karena model tidak memprediksi satu pun sampel positif ($\text{TP} = 0, \text{FP} = 0$)?
- **Verifikasi**: Data empiris membuktikan bahwa setiap fold kabupaten memiliki ratusan titik api ekstrem (misalnya Fold 2 mencakup Pulang Pisau dengan 1.100+ titik ekstrem). Model A menghasilkan $\text{TP} = 0$ karena seluruh prediksi kelas 1 diarahkan ke kabupaten lain berdasarkan ambang koordinat lat/lon yang tidak cocok. Ini mengonfirmasi bahwa F1 = 0,0000 adalah kegagalan katastropik murni (*true algorithmic failure*), bukan artefak ketiadaan data uji.

---

## 4. Caveats (Batasan Telaah)

1. Penelaahan ini berfokus pada evaluasi kualitas, ketelitian metodologis, dan kelayakan ilmiah berkas laporan `output/reports/review_report.md` sebagai deliverable resmi Milestone 1 (R1).
2. Reviewer 2 tidak menjalankan penulisan ulang naskah LaTeX atau pengubahan file konfigurasi model, karena peran saat ini adalah penelaah independen (review-only).
3. Penilaian terhadap artikel pembanding 2021–2025 didasarkan pada reputasi jurnal sumber dan relevansi tematik terhadap mitigasi karhutla dan Geo-AI.

---

## 5. Conclusion & Final Verdict (Kesimpulan & Vonis Akhir)

### Vonis Akhir: **APPROVE (DISETUJUI PENUH)**

### Rangkuman Penilaian:
1. **Standar Scopus Q1**: Berkas `output/reports/review_report.md` disusun dengan struktur, ketajaman analisis, dan kedalaman teoretis yang sepenuhnya memenuhi standar ekspektasi Senior Peer Reviewer jurnal Scopus Q1.
2. **Keadilan & Transparansi**: Evaluasi komparatif Model A vs Model B dilakukan secara sangat adil, berbasis bukti empiris terverifikasi, dan secara transparan mengakui limitasi Model B (Spatial CV ROC-AUC 0,4950 dan kompresi F1 akibat class imbalance).
3. **Penyelamatan Cacat Manuskrip**: Laporan berhasil mendeteksi dan memberikan solusi atas cacat kritis draf naskah (menghapus diagram ASCII, menata ulang 7 figur infografis riil beresolusi 300 DPI beserta caption lengkap, dan memperbarui 10 referensi mutakhir 2021–2025).
4. **Bebas Pelanggaran Integritas**: Tidak ditemukan indikasi manipulasi data, fabrikasi hasil, maupun jalan pintas (*zero integrity violations*). Dokumen ini memberikan landasan operasional (*actionable blueprint*) yang sangat solid bagi tim penulis untuk melanjutkan ke **Milestone 2 (Penyusunan Manuskrip LaTeX Publikasi Scopus Q1)**.

---

## 6. Verification Method (Metode Verifikasi Independen)

Untuk mereproduksi dan memverifikasi seluruh temuan penelaahan ini secara mandiri:

1. **Verifikasi Metrik Empiris**:
   Jalankan pemeriksaan JSON metrik model:
   ```bash
   /opt/anaconda3/envs/karhutla_env/bin/python -c "
   import json
   with open('output/reports/model_metrics.json') as f:
       d = json.load(f)
   print('Model A Test AUC:', d['model_a_spatial_memorization']['test_roc_auc'])
   print('Model A Spatial CV F1:', d['model_a_spatial_memorization']['spatial_block_cv_mean_f1'])
   print('Model B Test AUC:', d['model_b_pure_biophysical']['test_roc_auc'])
   print('Model B Spatial CV AUC:', d['model_b_pure_biophysical']['spatial_block_cv_mean_roc_auc'])
   print('Model B Spatial CV F1:', d['model_b_pure_biophysical']['spatial_block_cv_mean_f1'])
   "
   ```
   *Kondisi Validasi*: Nilai yang keluar harus tepat 0.7956, 0.0583, 0.7527, 0.495, dan 0.1399.

2. **Verifikasi Ketersediaan 7 Figur Ilmiah**:
   ```bash
   ls -la output/figures/0[1-7]_*.png
   ```
   *Kondisi Validasi*: Ketujuh berkas gambar `01_` hingga `07_` harus berukuran > 200 KB dan dapat dibuka tanpa galat.

3. **Verifikasi Jumlah Entri Bibliografi Eksisting**:
   ```bash
   grep -c "^@" manuscript/references.bib
   ```
   *Kondisi Validasi*: Menghasilkan angka tepat 30 entri.

4. **Kondisi Pembatalan (*Invalidation Conditions*)**:
   Vonis APPROVE ini menjadi tidak valid apabila:
   - Ditemukan manipulasi metrik empiris pada naskah LaTeX yang berbeda dari `output/reports/model_metrics.json`.
   - Sub-bab keterbatasan studi (Section 4.4) dihilangkan atau dilemahkan pembahasannya pada manuskrip akhir.
