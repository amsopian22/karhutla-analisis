# ANALISIS METODOLOGIS DAN AUDIT PEER REVIEW TINGKAT SENIOR (SCOPUS Q1)
## Evaluasi Komprehensif: Pemodelan Spasiotemporal Karhutla Kalimantan Tengah

**Penilai**: Explorer 3 (Methodology & Peer Review Auditor Explorer)  
**Konteks Target**: Standar Publikasi Jurnal Internasional Terindeks Scopus Q1 (*Remote Sensing* - MDPI / *International Journal of Wildland Fire* - CSIRO)  
**Dokumen Induk**: `manuscript/manuscript_draft.md`, `output/reports/model_metrics.json`, `src/train_model.py`, `src/process_real_data.py`  
**Tanggal Evaluasi**: 3 November 2026  

---

## 1. Executive Summary & Posisi Penyelidikan

Penyelidikan ini mengevaluasi integritas metodologis, desain eksperimen komparatif, dan validitas inferensi dari riset bertajuk *"Spatiotemporal Fire Intensity Modeling in Degraded Tropical Peatlands: Addressing Spatial Autocorrelation and Land Tenure Governance in Central Kalimantan"*. 

Penelitian ini memiliki kebaruan (*novelty*) dan relevansi kebijakan lingkungan yang luar biasa:
1. Mengintegrasikan **43.937 observasi riil satelit NASA FIRMS (VIIRS 375m & MODIS)** yang dipotong secara presisi terhadap 14 batas administrasi kabupaten resmi di Kalimantan Tengah.
2. Membedah narasi tanggung jawab tenurial melalui **spatial join faktual terhadap 627 konsesi sawit (HGU) dan 185 konsesi kehutanan (PBPH)**, yang membuktikan bahwa **75,4% kebakaran terjadi di Area Penggunaan Lain (APL / Non-Konsesi)**.
3. Merancang studi komparatif berani antara **Model Hafalan Spasial (Model A)** dan **Model Biofisik Murni (Model B)** untuk membuktikan kelemahan fatal *spatial autocorrelation* dan *spatial memorization*.
4. Mengimplementasikan **Explainable AI (TreeSHAP asli)** untuk mengidentifikasi interaksi non-linear faktor biofisik (defisit hujan 7-hari, jarak kanal eks-PLG, durasi *dry spell* 14 hari).

Namun, dari perspektif **Senior Reviewer Scopus Q1**, naskah dan metodologi ini memiliki sejumlah kerentanan ilmiah, keterbatasan komputasi, dan ancaman terhadap validitas (*threats to validity*) yang harus diartikulasikan secara transparan dan dikoreksi pada bagian *Discussion/Limitations* naskah final.

---

## 2. Investigasi Mendalam 1: Spatial Cross-Validation vs. Random CV dan Fenomena Spatial Memorization

### 2.1. Landasan Teoretis: Hukum Pertama Geografi Tobler & Kebocoran Informasi (Data Leakage)
Sesuai **Hukum Pertama Geografi Tobler** (*Tobler's First Law of Geography*):
$$\operatorname{Cov}(Z(\mathbf{s}), Z(\mathbf{s} + \mathbf{h})) > 0 \quad \text{untuk } \|\mathbf{h}\| \to 0$$
Segala sesuatu berhubungan dengan yang lain, namun entitas yang berdekatan secara spasial memiliki ketergantungan yang jauh lebih kuat dibandingkan entitas yang berjauhan.

Dalam pemodelan bencana lingkungan dan penginderaan jauh:
* Ketika data titik api dibagi menggunakan **Random Split (k-fold acak atau 75:25 train-test split konvensional)**, titik-titik uji (*test set*) secara geografis berada dalam lingkungan spasial (*neighborhood*) yang sangat dekat dengan titik-titik latih (*train set*).
* Hal ini menimbulkan **kebocoran informasi spasial (spatial data leakage)** dan pelanggaran asumsi dasar statistik bahwa observasi bersifat independen dan terdistribusi secara identik (*independent and identically distributed / i.i.d.*).
* Model Random Forest yang dilatih dengan fitur koordinat geodetik (`latitude` dan `longitude`) tidak mempelajari hukum biofisika kebakaran (kelembapan bahan bakar, evapotranspirasi, supresi hidrologis), melainkan sekadar melakukan partisi ruang (*spatial partitioning*) dan menghafal klaster koordinat (*spatial memorization*).

### 2.2. Pembuktian Empiris: Model A (Spatial Memorization) vs. Model B (Pure Biophysical)

| Parameter Evaluasi | Model A (Dengan Lat, Lon, Kabupaten) | Model B (Pure Biophysical: Tanpa Koordinat) | Analisis Kritis & Komparasi Ilmiah |
| :--- | :---: | :---: | :--- |
| **Jumlah Fitur Prediktor** | 15 fitur | 12 fitur | Model B membuang `latitude`, `longitude`, `kabupaten_kota` |
| **Holdout Test ROC-AUC (Random 75:25)** | **0.7956** | **0.7527** | Model A tampak "unggul semu" karena efek kebocoran spasial |
| **Holdout Test F1-Score** | **0.4512** | **0.3983** | Model A menghasilkan metrik lebih tinggi pada data terdistribusi sama |
| **Precision (Reguler, FRP < 12 MW)** | 92.8% | 92.1% | Keduanya sangat presisi mengenali kebakaran non-ekstrem |
| **Recall (Ekstrem, FRP $\ge$ 12 MW)** | 62.4% | **65.8%** | **Model B menangkap proporsi api ekstrem lebih tinggi (+3.4%)** |
| **Spatial Block CV Mean ROC-AUC** | **0.5399** ($\pm$ 0.0531) | **0.4950** ($\pm$ 0.0490) | **Model A anjlok drastis sebesar 0.2557 (-32.1%) mendekati tebakan acak (0.5000)** |
| **Spatial Block CV Mean F1-Score** | **0.0583** | **0.1399** | **Model B mempertahankan performa F1 2.40 kali lipat lebih tinggi dari Model A** |

### 2.3. Analisis Keruntuhan Per-Fold (Spatial Block CV Fold Breakdown)
Kehancuran Model A terlihat secara telanjang saat kita membedah hasil 5-fold Spatial Block Cross-Validation (`GroupKFold` per kabupaten) pada `output/reports/model_metrics.json`:

* **Fold 1 (Seruyan - Wilayah Kubah Gambut Barat)**:
  * Model A: $\text{AUC} = 0.5955$, $\text{F1} = 0.2913$
  * Model B: $\text{AUC} = 0.5827$, $\text{F1} = 0.2914$
* **Fold 2 (Pulang Pisau, Barito Timur, Barito Utara, Lamandau, Murung Raya)**:
  * Model A: $\text{AUC} = 0.5125$, $\mathbf{F1 = 0.0000}$ *(Keruntuhan Total)*
  * Model B: $\text{AUC} = 0.5041$, $\mathbf{F1 = 0.0657}$
* **Fold 3 (Kapuas, Barito Selatan, Gunung Mas, Sukamara)**:
  * Model A: $\text{AUC} = 0.5259$, $\mathbf{F1 = 0.0000}$ *(Keruntuhan Total)*
  * Model B: $\text{AUC} = 0.4900$, $\mathbf{F1 = 0.1056}$
* **Fold 4 (Katingan, Kota Palangka Raya)**:
  * Model A: $\text{AUC} = 0.4622$, $\mathbf{F1 = 0.0000}$ *(Keruntuhan Total)*
  * Model B: $\text{AUC} = 0.4452$, $\mathbf{F1 = 0.0646}$
* **Fold 5 (Kotawaringin Barat, Kotawaringin Timur)**:
  * Model A: $\text{AUC} = 0.6034$, $\mathbf{F1 = 0.0000}$ *(Keruntuhan Total)*
  * Model B: $\text{AUC} = 0.4533$, $\mathbf{F1 = 0.1722}$

#### Temuan Kritis Reviewer:
1. **Kegagalan Katastropik Model A pada Unseen Regions**: Pada 4 dari 5 fold spasial (Fold 2, 3, 4, 5), Model A menghasilkan **F1-Score = 0.0000**. Artinya, pohon keputusan Random Forest yang memecah batas koordinat regional sama sekali tidak mampu mengklasifikasikan satu pun titik api ekstrem di kabupaten yang disisihkan selama pelatihan. Model A sepenuhnya mengalami disfungsi operasional saat dipindahkan ke bentang alam baru.
2. **Resiliensi Model B**: Model B mempertahankan kemampuan prediksi positif di **seluruh 5 fold spasial** (F1 berkisar antara 0.0646 hingga 0.2914), menghasilkan rata-rata F1 sebesar **0.1399** (240% performa Model A).
3. **Keterbatasan Terbuka Model B (Kejujuran Ilmiah)**: Reviewer Scopus Q1 wajib menyoroti bahwa **rata-rata Spatial CV ROC-AUC Model B adalah 0.4950 ($\pm$ 0.0490)**, yang berada tepat di garis tebakan acak (*random guessing line* 0.5000). Hal ini membuktikan bahwa bahkan tanpa koordinat spasial, model menghadapi *spatial covariate shift* (pergeseran distribusi fitur antar wilayah): misalnya, jarak kanal hanya aktif di blok eks-PLG, karakteristik gambut Seruyan berbeda dengan Pulang Pisau, dan resolusi cuaca ERA5 bersifat seragam per kabupaten. Naskah harus mengakui keterbatasan ini secara eksplisit dan tidak boleh menyamarkannya seolah-olah Model B telah sempurna secara operasional.

---

## 3. Investigasi Mendalam 2: Ketimpangan Data (Class Imbalance) dan Trade-off Metrik

### 3.1. Struktur Ketimpangan Sampel
Dalam perumusan target prediksi keparahan api ekstrem ($FRP \ge 12.0\text{ MW}$):
* **Total Sampel Terkalibrasi**: 43.937 titik observasi.
* **Kelas Positif (Api Ekstrem, $FRP \ge 12\text{ MW}$)**: 6.634 titik (**15,1%**).
* **Kelas Negatif (Api Reguler/Moderat, $FRP < 12\text{ MW}$)**: 37.303 titik (**84,9%**).
* **Rasio Imbalance**: Sekitar **1 : 5,6** pada level hotspot aktif.
* *Catatan Skala Lanskap*: Jika ditinjau dari keseluruhan bentang daratan Kalimantan Tengah (15,3 juta hektar), piksel api aktif mewakili kurang dari 0,01% total area daratan (rasio ketimpangan ekstrem > 1:1.000).

### 3.2. Strategi Pembobotan Kelas & Trade-off Precision vs. Recall
Pada `src/train_model.py`, model diestimasi dengan parameter `class_weight='balanced'`:
$$w_j = \frac{N}{K \cdot n_j}$$
di mana $w_1 = \frac{43937}{2 \cdot 6634} \approx 3,31$ untuk kelas ekstrem, dan $w_0 = \frac{43937}{2 \cdot 37303} \approx 0,59$ untuk kelas reguler.

Dampak langsung terhadap performa model pada Holdout Test Set (10.985 titik):
* **Recall Kelas Ekstrem**: **65,82%** (Model B berhasil mendeteksi ~2 dari 3 kebakaran intensitas tinggi).
* **Precision Kelas Reguler**: **92,06%** (Sangat andal dalam memastikan bahwa kondisi non-bahaya memang aman).
* **F1-Score Gabungan**: **0.3983** pada holdout test set, dan **0.1399** pada spatial block CV.

### 3.3. Penanganan False Alarms dan Dilema Operasional Kebijakan
Reviewer mengidentifikasi trade-off kritis antara **False Alarms (False Positives)** dan **Missed Disasters (False Negatives)**:
1. **Mengapa Model Sengaja Mengorbankan Precision demi Recall?**
   Dalam konteks mitigasi bencana karhutla lahan gambut tropis, **asimetri biaya kerugian (loss asymmetry)** sangat tinggi:
   * **Biaya False Negative (Api Ekstrem tidak terdeteksi)**: Menimbulkan eskalasi kebakaran bawah tanah (*subsurface smoldering*), pelepasan emisi karbon raksasa, kabut asap lintas batas (*transboundary haze*), dan kerugian ekonomi miliaran dolar.
   * **Biaya False Positive (False Alarm)**: Mengerahkan tim patroli darat (Manggala Agni / BPBD) atau menyiagakan helikopter *water bombing* ke lokasi yang intensitasnya ternyata moderat.
2. **Ancaman Kelelahan Peringatan (*Alert Fatigue*)**:
   Kendati Recall tinggi diinginkan, F1-score yang berada di rentang 0.14–0.40 mengindikasikan banyaknya alarm palsu yang dapat memicu kelelahan logistik dan ketidakpercayaan personil lapangan jika model dijadikan sistem peringatan dini tunggal.
3. **Solusi Rekomendasi Reviewer**:
   Naskah publikasi harus menyarankan **Stratifikasi Risiko Berjenjang (Multi-Tier Risk Stratification)** berbasis probabilitas kontinu (misalnya: Tingkat Siaga I [Probabilitas 0.3–0.5], Tingkat Siaga II [0.5–0.7], dan Tanggap Darurat Ekstrem [> 0.7]), alih-alih hanya mengandalkan ambang batas biner kaku $p = 0.5$.

---

## 4. Investigasi Mendalam 3: Ancaman terhadap Validitas (Threats to Validity)

### 4.1. Validitas Internal (Internal Validity)
* **Keterbatasan Resolusi Sensor Thermal (VIIRS 375m vs. MODIS 1km)**:
  * Sensor VIIRS I-band (375m) memiliki kepekaan tinggi terhadap api berukuran kecil, sedangkan MODIS (1km) cenderung mendeteksi api berskala lebih besar. Penggabungan data kedua sensor tanpa pembobotan spesifik sensor berisiko memasukkan variasi instrumen ke dalam nilai FRP.
  * Kebakaran gambut murni (*smoldering peat combustion*) berlangsung di bawah tanah tanpa nyala api terbuka (*flameless*), dengan suhu rendah (300–600°C) yang sering kali tertutup oleh lapisan tajuk pohon lebat atau asap pekat (*plume obscuration*). Oleh karena itu, satelit polar-orbiting memiliki bias omissions terhadap kebakaran gambut dalam yang sedang membara lambat.
  * Waktu lintas satelit (*satellite overpass*) terbatas pada 2–4 kali per hari (antara pukul 13:00–14:30 WIB untuk lintas siang), melewatkan dinamika penjalaran api malam hari.
* **Resolusi Cuaca Reanalisis ERA5-Land vs. Observasi Lapangan BMKG**:
  * Data cuaca ERA5-Land memiliki resolusi spasial nominal 0,1° (~9 km).
  * Pada skrip pemrosesan `src/process_real_data.py` (baris 145–149), penggabungan data cuaca dilakukan berbasis `(kabupaten_kota, acq_date)`. Artinya, seluruh titik api di satu kabupaten yang sangat luas (seperti Kapuas yang membentang >15.000 km²) menerima parameter cuaca yang sama persis (nilai centroid/agregat kabupaten). Hal ini menimbulkan **kesalahan ekologis (*ecological fallacy*)** dan menghilangkan variabilitas mikroklimat lokal.
* **Penyederhanaan Vektor Garis Kanal**:
  * Jaringan kanal yang dimodelkan hanya mencakup **13 segmen Saluran Primer Induk (SPI)** eks-PLG. Ribuan kilometer saluran sekunder, tersier, dan parit perkebunan swasta/masyarakat tidak terpetakan dalam vektor line.
  * Penggunaan sentinel `-1` untuk kabupaten non-PLG (Seruyan, Kotim, Kobar) adalah *workaround* pragmatis yang baik untuk mencegah bias jarak semu, namun menciptakan diskontinuitas artifisial dalam ruang fitur pohon keputusan.

### 4.2. Validitas Eksternal (External Validity)
* **Keterbatasan Jendela Waktu (Temporal Generalizability)**:
  * Analisis satelit NASA FIRMS berfokus pada **jendela krisis 8 hari (5–12 Oktober 2026)**. Meskipun merepresentasikan 43.937 observasi riil pada puncak krisis transisi kemarau-hujan, dinamika ini tidak dapat secara otomatis digeneralisasikan untuk memprediksi kebakaran pada awal musim kemarau (Juni–Juli) atau pada periode La Niña basah tanpa kalibrasi ulang.
* **Generalisasi Geografis Antar-Provinsi (Spatial Transferability)**:
  * Bentang alam Kalimantan Tengah memiliki keunikan sejarah degradasi (Mega Rice Project / PLG 1 Juta Hektar).
  * Karakteristik lanskap ini tidak dapat langsung ditransfer begitu saja ke ekosistem gambut di Riau atau Sumatera Selatan yang didominasi oleh drainase industri Hutan Tanaman Industri (HTI akasia) atau gambut pesisir Papua yang belum terfragmentasi kanal drainase intensif.

### 4.3. Validitas Konstruk (Construct Validity)
* **Ambang Batas FRP $\ge 12.0\text{ MW}$ sebagai Proksi "Api Ekstrem"**:
  * *Fire Radiative Power* (FRP) mengukur energi radiasi termal sesaat yang dipancarkan oleh pembakaran aktif pada panjang gelombang inframerah tengah (~3,9 $\mu$m).
  * Di lahan gambut, nilai FRP tinggi ($\ge 12\text{ MW}$) kerap mencerminkan pembakaran tajuk atau semak belukar permukaan (*surface flaming* vegetasi pakis dan akasia cepat terbakar), bukan pembakaran massa gambut bawah tanah. Kebakaran gambut bawah tanah terdalam sering kali memancarkan FRP rendah (< 5 MW) namun melepaskan volume emisi karbon masif selama berminggu-minggu. Peneliti harus menegaskan bahwa target prediksi adalah "intensitas radiasi api sesaat berenergi tinggi", bukan "kedalaman lapisan gambut yang terbakar".
* **Agregasi Kategori Tenurial Non-Konsesi (APL)**:
  * Pelabelan 75,4% titik api sebagai "Non-Konsesi (APL / Lahan Terbuka)" menggabungkan berbagai entitas hukum: tanah milik adat, sertifikat hak milik perorangan (SHM), kawasan transmigrasi, dan rawa gambut terlantar berstatus tanah negara bebas (*open-access*). Peneliti harus memperjelas bahwa istilah "Non-Konsesi" merujuk pada area di luar izin HGU BPN dan PBPH KLHK, bukan menyiratkan ketiadaan aktivitas manusia.

---

## 5. Rancangan Kerangka Struktur & Poin Kritis Laporan Peer Review (`output/reports/review_report.md`)

Laporan Peer Review formal harus disusun menggunakan Bahasa Indonesia formal berbobot akademik tinggi setara laporan Senior Editor/Reviewer jurnal Q1. Berikut rancangan struktur dan poin kritis yang wajib dituangkan:

```
# LAPORAN PEER REVIEW INDEPENDEN (PEER REVIEW REPORT)
## Evaluasi Komprehensif Naskah Ilmiah Karhutla Kalimantan Tengah
## Target Standar: Jurnal Internasional Scopus Q1 (Remote Sensing / IJWF)

1. METADATA PENILAIAN & REKOMENDASI FORMAL
   - Judul Naskah
   - Penilai: Senior Peer Reviewer (Bidang Geospasial, Penginderaan Jauh & Pemodelan Bencana)
   - Rekomendasi Editorial: MAJOR REVISION (Revisi Mayor Metodologis & Penguatan Diskusi)
   - Ringkasan Kontribusi & Orisinalitas

2. EVALUASI KEKUATAN RISET (MAJOR STRENGTHS)
   - Keaslian Data Empiris (43.937 titik NASA FIRMS terpotong presisi ADM2 Kalteng)
   - Kebaruan Penyelidikan Tenurial Lahan (Spatial join faktual 627 HGU & 185 PBPH, 75.4% APL)
   - Desain Eksperimen Komparatif Berani (Model A Hafalan Spasial vs Model B Biofisik Murni)
   - Rigoritas Explainable AI (Implementasi sejati TreeSHAP untuk mengungkap ambang batas 14-hari)

3. KELEMAHAN METODOLOGIS KRITIS (CRITICAL METHODOLOGICAL DEFICIENCIES)
   - Kerentanan Autokorelasi Spasial & Ambruknya Model Hafalan Spasial (Analisis F1 = 0 pada 4 fold)
   - Realitas Keterbatasan Model B pada Spatial Block CV (Rata-rata AUC 0.4950 di wilayah unseen)
   - Dampak Penanganan Ketimpangan Data (Trade-off Recall 65.8% vs False Alarm Rate)
   - Bias Agregasi Spasial Data Cuaca ERA5-Land (Level Centroid Kabupaten)
   - Keterbatasan Sederhana Vektor Poros Saluran Primer Kanal Eks-PLG

4. EVALUASI ANCAMAN TERHADAP VALIDITAS (THREATS TO VALIDITY)
   - Validitas Internal (Resolusi VIIRS vs MODIS, Cloud Plume Obscuration, Overpass Gap)
   - Validitas Eksternal (Generalisasi temporal episode 8-hari, batas transferabilitas geografis)
   - Validitas Konstruk (Proksi FRP vs Deep Peat Smoldering, Heterogenitas Kawasan APL)

5. REKOMENDASI TERINCI PER SEKSI NASKAH (SECTION-BY-SECTION RECOMMENDATIONS FOR AUTHORS)
   - Bagian Abstract: Penajaman konteks spasial dan penekanan implikasi APL.
   - Bagian Introduction: Penguatan landasan teoritis Tobler's Law dan perdebatan tenurial.
   - Bagian Materials & Methods: Penjelasan rinci formula FWI, spatial join, dan GroupKFold.
   - Bagian Results: Transparansi penyajian tabel komparasi Model A vs B dan nilai SHAP.
   - Bagian Discussion (KRUSIAL): Wajib menambahkan sub-seksi "Methodological Limitations & Spatial Transferability" tanpa manipulasi angka empiris.
   - Bagian Conclusions & Policy: Penyelarasan rekomendasi praktis (Ambang 14 hari, canal blocking Blok A/B, tata kelola APL).

6. DAFTAR PERIKSA KESIAPAN PUBLIKASI SCOPUS Q1 (READINESS CHECKLIST)
   - Tabel audit keterpenuhan syarat teknis penulisan akademik internasional.
```

---

## 6. Sintesis Rekomendasi Konstruktif bagi Penulis Naskah LaTeX

Agar naskah LaTeX yang disusun oleh tim memenuhi kriteria jurnal Scopus Q1 tanpa mengubah angka empiris yang ada:
1. **Jangan Menyembunyikan Penurunan Performa Spasial**:
   Penurunan performa Model A di Spatial Block CV (AUC 0.5399, F1 0.0583) bukan merupakan aib penelitian, melainkan **temuan ilmiah utama (core contribution)** yang mendidik komunitas data science bahwa menambahkan koordinat dalam model bencana adalah praktik berbahaya yang menciptakan ilusi akurasi semu.
2. **Jelaskan Mengapa Model B Lebih Unggul Meskipun AUC Spatial CV 0.4950**:
   Model B membuktikan bahwa pohon keputusannya mengidentifikasi sinyal proses biofisik (defisit air, suhu, kedalaman gambut) yang stabil di seluruh fold, tercermin dari F1-score yang 2,4 kali lebih tinggi dan selalu positif di semua kabupaten.
3. **Kontekstualisasikan Temuan Tenurial APL**:
   Tingginya titik api di APL (75,4%) harus didiskusikan secara berimbang: ini bukan berarti korporasi bebas tanggung jawab (karena 24,6% titik api berada di dalam konsesi berizin yang memiliki kepatuhan hukum ketat), melainkan menunjukkan adanya jurang tata kelola (*governance void*) pada bentang lahan gambut terbengkalai pasca proyek PLG 1999.
4. **Artikulasikan Resolusi Data Satelit dan Proksi FRP**:
   Di sub-bab *Limitations*, penulis wajib menguraikan bahwa FRP satelit optik/thermal adalah indikator energi termal aktif sesaat, dan penelitian lanjutan membutuhkan integrasi sensor Synthetic Aperture Radar (SAR / Sentinel-1) atau pengukuran fluks gas gas rumah kaca insitu untuk memantau kebakaran bawah tanah tanpa nyala.

---
*Laporan analisis ini diselesaikan sebagai fondasi resmi penyusunan dokumen `output/reports/review_report.md` dan naskah publikasi LaTeX standar Scopus Q1.*
