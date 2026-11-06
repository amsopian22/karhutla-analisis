# PANDUAN PENGEMBANGAN DAN HANDOVER AGEN AI (AGENTS.md)
# Proyek: Analisis Spasiotemporal Karhutla Kalimantan Tengah
# Naskah Ilmiah: "The Governance Void at Concession Frontiers: A Spatial Boundary Discontinuity Analysis of Peatland Wildfires in Central Kalimantan"
# Jurnal Target: Remote Sensing Applications: Society and Environment (RSASE, Elsevier, Scopus Q1)

Dokumen ini adalah instruksi operasional, konteks arsitektur, standar integritas data, dan panduan teknis bagi setiap Agen AI yang melanjutkan pekerjaan pada repositori ini di sesi berikutnya.

---

## 1. Aturan Lingkungan & Eksekusi (Environment Rules)

> [!IMPORTANT]
> **ATURAN WAJIB PENGGUNAAN CONDA & STANDAR KOMUNIKASI**:
> 1. Proyek ini berjalan pada lingkungan conda khusus: **`karhutla_env`** (Python 3.10.22).
> 2. Jalankan perintah Python melalui python binary di environment ini:
>    ```bash
>    /opt/anaconda3/envs/karhutla_env/bin/python <script.py>
>    # atau aktifkan conda
>    conda activate karhutla_env
>    ```
> 3. Jangan menginstal paket secara global atau menggunakan environment `base`.
> 4. Seluruh komunikasi dan penjelasan kepada pengguna **WAJIB menggunakan Bahasa Indonesia** yang terstruktur, berbasis data riil, dan berbobot *Senior Data Scientist / Principal GIS Researcher*.
> 5. Seluruh angka numerik dalam publikasi harus sinkron secara deterministik dengan ringkasan JSON dan dataset riil (Toleransi dummy data = 0%).

---

## 2. Profil Jurnal Target & Ketentuan Pengajuan (Submission Profile)

| Parameter | Spesifikasi Resmi Elsevier RSASE |
|:---|:---|
| **Nama Jurnal** | *Remote Sensing Applications: Society and Environment* (RSASE) |
| **Penerbit** | Elsevier B.V. (ISSN: 2352-9385) |
| **Portal Pengajuan** | `https://www.editorialmanager.com/rsase/default.aspx` |
| **Indeksasi & Reputasi** | **Scopus Q1** (CiteScore: **7.9**); Clarivate JCR Impact Factor: **4.5 – 4.9** |
| **Model Publikasi** | **Hybrid Journal** $\rightarrow$ Rute **Subscription ($0 USD APC / Tanpa Biaya Publikasi)** |
| **Panjang Abstrak** | 150 – 250 kata (Naskah saat ini terkalibrasi di **246 kata**) |
| **Highlights** | 3–5 butir, maksimal 85 karakter per butir termasuk spasi (Terkalibrasi 5 butir $\le 77$ karakter) |
| **Kata Kunci (Keywords)** | 7 kata kunci terkalibrasi: `Remote sensing applications; Satellite active fires; Tropical peatlands; Spatial boundary discontinuity; Spatial block cross-validation; Land tenure governance; Fire Radiative Power.` |
| **Penulis & Afiliasi** | 1. **Ahmad Sopian** (Corresponding Author, Independent Researcher, `ahmadsopian22@gmail.com`)<br>2. **Rahmi Susanti** (Faculty of Public Health, Universitas Mulawarman, `rahmi.susanti@fkm.unmul.ac.id`) |
| **Repositori Kode & Data** | [https://github.com/amsopian22/karhutla-analisis](https://github.com/amsopian22/karhutla-analisis) (Terbuka & Reproducible) |

---

## 3. Struktur Proyek & Inventaris Berkas (File Inventory)

```
karhutla-analisis/
├── AGENTS.md                                # [DOKUMEN INI] Panduan teknis & handover agen AI
├── PLAN.md                                  # Rencana eksekusi terstruktur dan roadmap proyek
├── README.md                                # Dokumentasi publik repositori GitHub
├── PROJECT_SUMMARY.md                       # Ringkasan eksekutif hasil analisis & audit ilmiah
├── data/
│   ├── raw/                                 # DATA MENTAH (RAW DATASETS)
│   │   ├── firms_real_kalteng_latest_7d.csv # Data mentah NASA FIRMS bounding box (52.829 titik)
│   │   ├── batas_kabupaten_kalteng.geojson  # Poligon batas resmi 14 Kabupaten/Kota Kalteng (geoBoundaries ADM2)
│   │   ├── jaringan_kanal_plg_kalteng.geojson # Vektor garis (LineString) poros kanal eks-PLG Blok A, B, C, D
│   │   ├── sipongi_luas_karhutla_kalteng_2018_2026.csv # Data resmi luasan kebakaran SiPongi KLHK (2018–2026)
│   │   ├── konsesi_sawit_kalteng_real.geojson # Poligon riil HGU Perkebunan Sawit Kalteng (627 izin)
│   │   └── konsesi_kehutanan_pbph_real.geojson # Poligon riil PBPH Kehutanan Nasional (185 izin Kalteng)
│   └── processed/                           # DATA TERPROSES & MASTER
│       ├── karhutla_kalteng_2019_2026.csv   # DATASET MASTER: 43.937 titik valid hasil kliping batas resmi Kalteng
│       ├── karhutla_kalteng_real_2026.csv   # Dataset terproses episode 2026 (43.937 titik)
│       └── transboundary_pm25_haze_2026.csv # Data simulasi dispersi PM2.5 atmosferik Monsun Barat Daya
├── manuscript/                              # NASKAH PUBLIKASI ILMIAH
│   ├── main.tex                             # LaTeX Master File (Elsevier format, Tectonic compiler)
│   ├── main.pdf                             # Naskah Terkompilasi PDF (32 halaman, resolusi cetak)
│   ├── references.bib                       # Basis data bibliografi BibTeX (45 referensi terverifikasi)
│   ├── cover_letter.md                      # Surat pengantar resmi ke Editor-in-Chief RSASE
│   ├── title_page.md                        # Halaman judul lengkap dengan rincian penulis
│   ├── highlights.md                        # Research highlights (5 butir, <= 85 karakter)
│   ├── credit_statement.md                  # CRediT Author Statement
│   ├── declaration_of_interest.md           # Pernyataan bebas konflik kepentingan
│   ├── suggested_reviewers.md               # 4 Pakar internasional independen
│   ├── manuscript_draft.md                  # Naskah lengkap Markdown dengan nama penulis
│   ├── manuscript_without_author_details.md # Naskah anonim untuk Double-Blind Peer Review
│   ├── sections/                            # Bab naskah LaTeX
│   │   ├── 00_abstract.tex                  # Abstrak terkalibrasi (246 kata) & kata kunci
│   │   ├── 01_introduction.tex              # Pendahuluan, latar belakang, dan hipotesis (H1, H2, H2a, H2b)
│   │   ├── 02_materials_methods.tex         # Data, Spatial BDD, ML, Spatial Block CV, TreeSHAP
│   │   ├── 03_results.tex                   # Hasil empiris, Spatial BDD +56,5%, evaluasi ML, TreeSHAP
│   │   ├── 04_discussion.tex                # Pembahasan hidrologi, tata kelola, bias Tobler, limitasi
│   │   └── 05_conclusions.tex               # Kesimpulan ilmiah dan 4 rekomendasi kebijakan
│   └── submission_package/                  # PAKET PENGAJUAN SIAP UNGGAH
│       ├── manuscript_main.docx             # Naskah Word dengan detail penulis
│       ├── manuscript_without_author_details.docx # Naskah Word anonim (Double-Blind)
│       ├── title_page.docx                  # Title Page Word
│       ├── cover_letter.docx & .pdf         # Cover letter Word & PDF
│       ├── highlights.docx                  # Highlights Word
│       ├── credit_statement.docx            # CRediT Word
│       ├── declaration_of_interest.docx     # Declaration of Interest Word
│       └── figures/                         # Gambar naskah bernomor urut Figure_01 s.d. Figure_08
├── output/
│   ├── figures/                             # Master Visualisasi Publikasi (300 DPI)
│   │   ├── 01_peta_wilayah_studi_spatial_cv.png # Gambar 1: Wilayah studi, 14 kabupaten & 5 blok CV
│   │   ├── 02_peta_densitas_hotspot_frp.png     # Gambar 2: Peta densitas hotspot & FRP
│   │   ├── 03_analisis_citra_satelit_kanal.png  # Gambar 3: Analisis citra satelit & jarak kanal
│   │   ├── 04_peta_tenurial_konsesi_esg.png     # Gambar 4: Sebaran tenurial konsesi HGU & PBPH
│   │   ├── 09_spatial_boundary_discontinuity.png # Gambar 5: Spatial BDD Kurva diskontinuitas perbatasan
│   │   ├── 05_tren_temporal_dan_harian.png      # Gambar 6: Tren SiPongi (2018–2026) & dinamika harian
│   │   ├── 06_evaluasi_model_ml.png             # Gambar 7: Kurva ROC & Matriks Konfusi Model B
│   │   ├── 07_shap_feature_importance.png       # Gambar 8: TreeSHAP beeswarm plot
│   │   └── peta_interaktif_karhutla_kalteng.html # Peta interaktif Folium multi-layer
│   ├── models/
│   │   └── karhutla_rf_model.joblib         # Model Random Forest, Encoders, & Spatial CV Metrics
│   └── reports/
│       ├── mathematical_validation_audit.json # Ringkasan audit presisi matematis 11 persamaan formal
│       ├── spatial_bdd_summary.json         # Metrik lengkap Spatial BDD & 3 Robustness Checks
│       ├── model_metrics.json               # Metrik evaluasi model Random Forest & Spatial CV
│       └── eda_summary.json                 # Metrik statistik ringkasan EDA
├── src/                                     # PIPELINE PEMROSESAN & PEMODELAN
│   ├── process_real_data.py                 # Kliping batas 14 Kab/Kota, vektor kanal UTM 49S, cuaca
│   ├── spatial_join_concessions.py          # Penaut spasial ke 627 HGU sawit & 185 PBPH
│   ├── spatial_boundary_discontinuity.py    # Perhitungan Spatial BDD, bandwidth & placebo test
│   ├── train_model.py                       # Random Forest, Spatial Block CV (GroupKFold), TreeSHAP
│   ├── generate_map.py                      # Render peta interaktif Folium
│   └── transboundary_haze_analysis.py       # Model dispersi aerosol Monsun Barat Daya
└── tests/                                   # HARNESS PENGUJIAN OTOMATIS (53 UNIT TES)
    ├── test_abstract_word_count.py          # Uji kepatuhan panjang abstrak (<= 250 kata)
    ├── test_highlights_length.py            # Uji panjang karakter highlights (<= 85 char)
    ├── test_keywords_alignment.py           # Uji keselarasan kata kunci terhadap RSASE
    ├── test_data_integrity_and_metrics.py   # Uji deterministik data 43.937 titik & BDD +56,5%
    ├── test_mathematical_formulations.py    # Uji deterministik 11 persamaan formal, statistik & ML
    ├── test_document_compilation_rendering.py # Uji kompilasi Tectonic & integritas DOCX/XML
    ├── test_reference_figure_callout_consistency.py # Uji sitasi BibTeX & urutan gambar/tabel
    └── test_challenger_adversarial_suite.py # Uji stres komprehensif adversarial
```

---

## 4. Alur Kerja Reproduksi Pipeline (Step-by-Step Runbook)

Untuk mereproduksi seluruh pipeline dari data mentah hingga kompilasi paket pengajuan:

```bash
# 0. Aktifkan lingkungan conda
conda activate karhutla_env

# 1. Pemrosesan titik api NASA FIRMS, kliping batas 14 kabupaten, dan jarak kanal (UTM Zone 49S)
python src/process_real_data.py

# 2. Tautkan spasial ke poligon konsesi sawit (627 HGU) & kehutanan (185 PBPH)
python src/spatial_join_concessions.py

# 3. Hitung Spatial Boundary Discontinuity Design (Spatial BDD) dan 3 Robustness Checks
python src/spatial_boundary_discontinuity.py

# 4. Latih model Random Forest, evaluasi 5-fold Spatial Block CV, dan hitung TreeSHAP
python src/train_model.py

# 5. Render peta interaktif HTML dengan legenda mengambang
python src/generate_map.py

# 6. Kompilasi naskah LaTeX PDF menggunakan Tectonic
tectonic manuscript/main.tex

# 7. Kompilasi paket dokumen Word (.docx) menggunakan Pandoc
pandoc manuscript/manuscript_draft.md --resource-path=.:output/figures --bibliography=manuscript/references.bib --citeproc -o manuscript/submission_package/manuscript_main.docx
pandoc manuscript/manuscript_without_author_details.md --resource-path=.:output/figures --bibliography=manuscript/references.bib --citeproc -o manuscript/submission_package/manuscript_without_author_details.docx
pandoc manuscript/title_page.md -o manuscript/submission_package/title_page.docx
pandoc manuscript/cover_letter.md -o manuscript/submission_package/cover_letter.docx
pandoc manuscript/cover_letter.md --pdf-engine=/opt/homebrew/bin/tectonic -o manuscript/submission_package/cover_letter.pdf
pandoc manuscript/highlights.md -o manuscript/submission_package/highlights.docx

# 8. Jalankan seluruh unit tes (Wajib 53/53 PASSED)
pytest tests/ -v
```

---

## 5. Kaidah Ilmiah & Pelajaran Teknis Penting (*Methodological Pitfalls*)

1. **Harmonisasi Penomoran Hipotesis**:
   - Selalu pertahankan pemisahan: $\mathbf{H_1}$ adalah *Spatial Boundary Discontinuity Hypothesis* (+56,5% lonjakan di batas legal). $\mathbf{H_2}$ adalah *Biophysical Transferability Hypothesis*, yang dipecah menjadi $\mathbf{H_{2a}}$ (*Spatial Memorization Collapse* pada Model A) dan $\mathbf{H_{2b}}$ (*Biophysical Operational Retention* pada Model B). Jangan pernah menyebut Model A vs Model B sebagai $H_1$ vs $H_2$.
2. **Nilai Sentinel Jarak Kanal (`jarak_kanal_m`)**:
   - Titik api di luar lanskap ex-PLG (misalnya Seruyan dan Kotim) diberi jarak asimptotik **$99.999\text{ meter}$** (bukan $-1$) untuk mencerminkan bahwa kubah gambut pesisir barat terputus secara hidrologis dari kanal eks-PLG. Analisis TreeSHAP jarak kanal dievaluasi pada sampel fokal ex-PLG ($n = 16.645$).
3. **Pembingkaian Jujur Nilai ROC-AUC Spasial Model B (0,4950)**:
   - Nilai Spatial CV ROC-AUC 0,4950 merefleksikan pergeseran kovariat spasial (*spatial covariate shift*) ekstrem antara lanskap gambut berkanal (Pulang Pisau/Kapuas) dan kubah gambut pesisir alami tanpa kanal (Seruyan).
   - Keunggulan operasional Model B terletak pada **ketahanan ambang operasional**: penghapusan koordinat menyelamatkan model dari *total recall collapse* ($F_1 = 0,0000$) yang dialami Model A di 4 dari 5 blok, mempertahankan rata-rata operasional $F_1 = 0,1399$ (retensi 2,40x lebih tinggi).
4. **Validitas Spatial BDD & Robustness Checks**:
   - Selalu pertahankan 3 uji ketahanan pada Spatial BDD:
     * *Bandwidth Sensitivity*: $\pm 1\text{ km}$ (+12,0%), $\pm 2\text{ km}$ (+31,9%), $\pm 3\text{ km}$ (+56,5%).
     * *Placebo Test*: Pergeseran semu $-1\text{ km}$ ke interior menghasilkan rasio 1,084 (tidak ada lompatan semu).
     * *Concession Decomposition*: Kerapatan APL frontier ($0,2864/\text{km}^2$) melampaui HGU sawit ($0,2268/\text{km}^2$) dan PBPH kehutanan ($0,0766/\text{km}^2$).
5. **Skala Ekstraksi Cuaca ERA5-Land ($0,1^\circ \approx 9\text{ km}$)**:
   - Ekstraksi cuaca pada centroid 14 kabupaten/kota dibenarkan karena selaras dengan skala hierarki komando penanggulangan bencana BPBD dan Manggala Agni Daops tingkat kabupaten, dengan tetap mengakui keterbatasan mikroklimat sub-grid di bab limitasi.
6. **Integritas Batas Dokumen & Format Elsevier**:
   - Abstrak: Maksimal 250 kata.
   - Highlights: Maksimal 85 karakter per butir termasuk spasi.
   - File Size PDF: $>5\text{ MB}$ karena memuat gambar 300 DPI resolusi tinggi.
